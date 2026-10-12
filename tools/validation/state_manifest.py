#!/usr/bin/env python3
"""Canonical source manifests and ambient state snapshots for isolated checks."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

# Retain wire versions for existing preservation-journal manifests.
MANIFEST_VERSION = "portfolio-source-manifest/v1"
AMBIENT_PROFILE_VERSION = "portfolio-ambient-watch-profile/v1"
REQUIRED_AMBIENT_CATEGORIES = {"python", "go", "cargo", "postgresql", "installer", "shell-config", "network-policy"}


class ContractError(ValueError):
    pass

def _reject_constant(value: str) -> None:
    raise ContractError(f"non-finite JSON number is forbidden: {value}")

def _pairs(items: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in items:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def strict_load(path: Path) -> dict:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("JSON root must be an object")
    return value

def canonical_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"value is not canonical JSON: {exc}") from exc

def digest_value(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def digest_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def _relative_path(value: str) -> str:
    if "\x00" in value:
        raise ContractError("path contains NUL")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ContractError(f"path must be normalized repository-relative POSIX text: {value!r}")
    normalized = path.as_posix()
    if normalized != value:
        raise ContractError(f"path is not normalized: {value!r}")
    return normalized

def _root(value: str | Path) -> Path:
    raw = Path(value).expanduser().absolute()
    if raw.is_symlink():
        raise ContractError(f"repository root must not be a symlink: {raw}")
    try:
        root = raw.resolve(strict=True)
    except OSError as exc:
        raise ContractError(f"repository root is unavailable: {raw}") from exc
    if not root.is_dir():
        raise ContractError(f"repository root is not a directory: {root}")
    return root

def _reject_symlink_parents(root: Path, relative: str) -> Path:
    current = root
    parts = PurePosixPath(relative).parts
    for part in parts[:-1]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(info.st_mode):
            raise ContractError(f"intermediate path is a symlink: {current}")
        if not stat.S_ISDIR(info.st_mode):
            raise ContractError(f"intermediate path is not a directory: {current}")
    return root.joinpath(*parts)

def manifest_entry(root: Path, relative: str) -> dict:
    relative = _relative_path(relative)
    path = _reject_symlink_parents(root, relative)
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"path": relative, "type": "absent"}
    mode = f"{stat.S_IMODE(info.st_mode):04o}"
    if stat.S_ISREG(info.st_mode):
        return {
            "path": relative,
            "type": "regular",
            "mode": mode,
            "sha256": digest_file(path),
            "size": info.st_size,
            "nlink": info.st_nlink,
        }
    if stat.S_ISLNK(info.st_mode):
        target = os.fsencode(os.readlink(path))
        return {
            "path": relative,
            "type": "symlink",
            "mode": mode,
            "sha256": hashlib.sha256(target).hexdigest(),
            "size": len(target),
        }
    raise ContractError(f"manifest inputs must be regular files, symlinks, or absent: {relative}")

def build_manifest(root_value: str | Path, paths: list[str]) -> dict:
    root = _root(root_value)
    normalized = [_relative_path(item) for item in paths]
    if not normalized or len(normalized) != len(set(normalized)):
        raise ContractError("manifest paths must be nonempty and unique")
    entries = [manifest_entry(root, item) for item in sorted(normalized, key=lambda item: item.encode("utf-8"))]
    return {
        "schema_version": MANIFEST_VERSION,
        "repository_root": str(root),
        "entries": entries,
    }

def tree_manifest(path_value: str | Path, excluded_names: set[str] | None = None) -> dict:
    path = Path(path_value).expanduser().absolute()
    excluded = excluded_names or set()
    if not path.exists() and not path.is_symlink():
        return {"root": str(path), "type": "absent", "entries": []}
    if path.is_symlink():
        target = os.fsencode(os.readlink(path))
        return {
            "root": str(path),
            "type": "symlink",
            "entries": [{"path": ".", "type": "symlink", "sha256": hashlib.sha256(target).hexdigest()}],
        }
    if path.is_file():
        info = path.lstat()
        return {
            "root": str(path),
            "type": "regular",
            "entries": [
                {
                    "path": ".",
                    "type": "regular",
                    "mode": f"{stat.S_IMODE(info.st_mode):04o}",
                    "sha256": digest_file(path),
                    "size": info.st_size,
                }
            ],
        }
    if not path.is_dir():
        raise ContractError(f"snapshot root must be a file, symlink, directory, or absent: {path}")
    entries: list[dict] = []
    for current, directories, files in os.walk(path, topdown=True, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(
            [name for name in directories if name not in excluded],
            key=lambda item: os.fsencode(item),
        )
        names = sorted(directories + files, key=lambda item: os.fsencode(item))
        for name in names:
            child = current_path / name
            relative = child.relative_to(path).as_posix()
            info = child.lstat()
            mode = f"{stat.S_IMODE(info.st_mode):04o}"
            if stat.S_ISLNK(info.st_mode):
                target = os.fsencode(os.readlink(child))
                entries.append(
                    {
                        "path": relative,
                        "type": "symlink",
                        "mode": mode,
                        "sha256": hashlib.sha256(target).hexdigest(),
                    }
                )
            elif stat.S_ISREG(info.st_mode):
                entries.append(
                    {
                        "path": relative,
                        "type": "regular",
                        "mode": mode,
                        "sha256": digest_file(child),
                        "size": info.st_size,
                    }
                )
            elif stat.S_ISDIR(info.st_mode):
                entries.append({"path": relative, "type": "directory", "mode": mode})
            else:
                entries.append({"path": relative, "type": "special", "mode": mode})
    return {"root": str(path), "type": "directory", "entries": entries}

def state_snapshot(repo: str | Path, watches: list[str]) -> dict:
    repository = tree_manifest(repo, excluded_names={".git", ".planning"})
    watched = [tree_manifest(path) for path in watches]
    return {
        "schema_version": "portfolio-state-snapshot/v1",
        "repository": {"root": repository["root"], "digest": digest_value(repository)},
        "watched": [
            {"root": item["root"], "digest": digest_value(item)}
            for item in watched
        ],
    }

def resolve_ambient_watch_profile(
    profile_path: Path,
    *,
    repo: str | Path,
    host_home: str | Path,
    host_tmpdir: str | Path,
) -> list[str]:
    profile = strict_load(profile_path)
    _exact_keys(profile, {"schema_version", "required_categories", "entries"})
    if profile["schema_version"] != AMBIENT_PROFILE_VERSION:
        raise ContractError("unsupported ambient watch profile")
    categories = profile["required_categories"]
    if not isinstance(categories, list) or set(categories) != REQUIRED_AMBIENT_CATEGORIES or len(categories) != len(set(categories)):
        raise ContractError("ambient watch profile must name every required category exactly once")
    entries = profile["entries"]
    if not isinstance(entries, list) or not entries:
        raise ContractError("ambient watch profile entries must be nonempty")
    bases = {
        "repo": Path(repo).expanduser().absolute(),
        "home": Path(host_home).expanduser().absolute(),
        "tmp": Path(host_tmpdir).expanduser().absolute(),
    }
    observed_categories: set[str] = set()
    resolved: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ContractError("ambient watch entry must be an object")
        _exact_keys(entry, {"category", "base", "path"})
        category = entry["category"]
        base = entry["base"]
        value = entry["path"]
        if category not in REQUIRED_AMBIENT_CATEGORIES:
            raise ContractError(f"unknown ambient watch category: {category}")
        if base not in {"repo", "home", "tmp", "absolute"}:
            raise ContractError(f"unknown ambient watch base: {base}")
        if not isinstance(value, str) or not value or "\x00" in value or "\n" in value or "\r" in value:
            raise ContractError("ambient watch path must be nonempty single-line text")
        path = Path(value)
        if base == "absolute":
            if not path.is_absolute():
                raise ContractError("absolute ambient watch path must be absolute")
            target = path
        else:
            if path.is_absolute() or any(part in {"", ".", ".."} for part in PurePosixPath(value).parts):
                raise ContractError("relative ambient watch path must be normalized and traversal-free")
            target = bases[base].joinpath(*PurePosixPath(value).parts)
        observed_categories.add(category)
        resolved.append(str(target.absolute()))
    if observed_categories != REQUIRED_AMBIENT_CATEGORIES:
        raise ContractError("ambient watch entries do not cover every required category")
    if len(resolved) != len(set(resolved)):
        raise ContractError("ambient watch paths must resolve uniquely")
    return resolved

def _exact_keys(value: dict, expected: set[str]) -> None:
    actual = set(value)
    if actual != expected:
        raise ContractError(
            f"closed object fields differ; missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
        )

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    manifest = commands.add_parser("manifest")
    manifest.add_argument("--root", required=True)
    manifest.add_argument("path", nargs="+")
    hash_command = commands.add_parser("hash")
    hash_command.add_argument("json_file")
    state = commands.add_parser("state")
    state.add_argument("--repo", required=True)
    state.add_argument("--watch", action="append", default=[])
    watch = commands.add_parser("watch-paths")
    for name in ("repo", "profile", "host-home", "host-tmpdir"):
        watch.add_argument("--" + name, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "manifest":
            value = build_manifest(args.root, args.path)
            result = {"manifest": value, "digest": digest_value(value)}
        elif args.command == "hash":
            result = {"digest": digest_value(strict_load(Path(args.json_file)))}
        elif args.command == "state":
            result = state_snapshot(args.repo, args.watch)
        else:
            for path in resolve_ambient_watch_profile(Path(args.profile), repo=args.repo, host_home=args.host_home, host_tmpdir=args.host_tmpdir):
                print(path)
            return 0
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (ContractError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())
