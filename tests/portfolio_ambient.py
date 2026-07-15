#!/usr/bin/env python3
"""Capture and validate the installed-link and source Python-cache baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


SCHEMA_VERSION = "portfolio-ambient-baseline/v1"


class AmbientError(ValueError):
    pass


def digest_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode()


def strict_load(path: Path) -> dict:
    def pairs(items: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise AmbientError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(AmbientError(f"non-finite number: {value}")),
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AmbientError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AmbientError("JSON root must be an object")
    return value


def regular_state(path: Path, relative: str) -> dict:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise AmbientError(f"Python cache file must be one regular link: {relative}")
    return {
        "path": relative,
        "mode": f"{stat.S_IMODE(info.st_mode):04o}",
        "size": info.st_size,
        "nlink": info.st_nlink,
        "sha256": digest_file(path),
    }


def capture(repo_value: str, agent_root_value: str, codex_root_value: str) -> dict:
    supplied_repo = Path(repo_value).expanduser().absolute()
    if supplied_repo.is_symlink() or not supplied_repo.is_dir():
        raise AmbientError("repository root must be a real directory")
    repo = supplied_repo.resolve(strict=True)
    catalog_path = repo / "tests" / "portfolio-routing-v1.json"
    catalog = strict_load(catalog_path)
    skills = catalog.get("portfolio_skills")
    if not isinstance(skills, list) or not skills or any(not isinstance(item, str) for item in skills):
        raise AmbientError("routing catalog skill list is invalid")

    links: list[dict] = []
    for label, root_value in (("agents", agent_root_value), ("codex", codex_root_value)):
        installed_root = Path(root_value).expanduser().absolute()
        for skill in skills:
            path = installed_root / skill
            info = path.lstat()
            if not stat.S_ISLNK(info.st_mode):
                raise AmbientError(f"installed entry is not a symlink: {label}/{skill}")
            target = os.readlink(path)
            resolved = (path.parent / target).resolve(strict=True)
            expected = (repo / "skills" / skill).resolve(strict=True)
            if resolved != expected:
                raise AmbientError(f"installed target differs: {label}/{skill}")
            links.append(
                {
                    "root": label,
                    "skill": skill,
                    "target": target,
                    "device": info.st_dev,
                    "inode": info.st_ino,
                    "mode": f"{stat.S_IMODE(info.st_mode):04o}",
                    "nlink": info.st_nlink,
                    "uid": info.st_uid,
                    "gid": info.st_gid,
                    "size": info.st_size,
                    "mtime_ns": info.st_mtime_ns,
                }
            )

    pycache_directories: list[dict] = []
    pyc_files: list[dict] = []
    for base_name in ("skills", "scripts", "tests"):
        base = repo / base_name
        if not base.exists():
            continue
        for current, directories, files in os.walk(base, topdown=True, followlinks=False):
            directories.sort(key=os.fsencode)
            files.sort(key=os.fsencode)
            current_path = Path(current)
            if current_path.name == "__pycache__":
                info = current_path.lstat()
                pycache_directories.append(
                    {
                        "path": current_path.relative_to(repo).as_posix(),
                        "mode": f"{stat.S_IMODE(info.st_mode):04o}",
                        "device": info.st_dev,
                        "inode": info.st_ino,
                        "mtime_ns": info.st_mtime_ns,
                    }
                )
            for name in files:
                if not name.endswith(".pyc"):
                    continue
                path = current_path / name
                pyc_files.append(regular_state(path, path.relative_to(repo).as_posix()))

    body = {
        "schema_version": SCHEMA_VERSION,
        "repository_root": str(repo),
        "routing_catalog_sha256": digest_file(catalog_path),
        "installed_links": links,
        "pycache_directories": sorted(pycache_directories, key=lambda item: os.fsencode(item["path"])),
        "pyc_files": sorted(pyc_files, key=lambda item: os.fsencode(item["path"])),
    }
    body["content_digest"] = hashlib.sha256(canonical_bytes(body)).hexdigest()
    return body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capture", "validate"))
    parser.add_argument("--repo", required=True)
    parser.add_argument("--agent-root", required=True)
    parser.add_argument("--codex-root", required=True)
    parser.add_argument("--manifest")
    args = parser.parse_args(argv)
    try:
        observed = capture(args.repo, args.agent_root, args.codex_root)
        if args.command == "validate":
            if not args.manifest:
                raise AmbientError("validate requires --manifest")
            expected = strict_load(Path(args.manifest))
            if expected != observed:
                raise AmbientError("ambient baseline differs")
        print(json.dumps(observed, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (AmbientError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "valid": False}, sort_keys=True), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
