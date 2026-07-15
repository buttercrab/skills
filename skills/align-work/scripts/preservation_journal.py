#!/usr/bin/env python3
"""Snapshot, finalize, and safely roll back plan-owned file slices."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import uuid


SCHEMA_VERSION = "align-preservation-journal/v1"


class JournalError(ValueError):
    pass


def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_value(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def safe_root(value: str | Path) -> Path:
    raw = Path(value).expanduser().absolute()
    if raw.is_symlink():
        raise JournalError(f"repository root must not be a symlink: {raw}")
    try:
        root = raw.resolve(strict=True)
    except OSError as exc:
        raise JournalError(f"repository root is unavailable: {raw}") from exc
    if not root.is_dir():
        raise JournalError(f"repository root is not a directory: {root}")
    return root


def normalized_relative(value: str) -> str:
    if "\x00" in value:
        raise JournalError("path contains NUL")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise JournalError(f"path must be normalized repository-relative POSIX text: {value!r}")
    if path.as_posix() != value:
        raise JournalError(f"path is not normalized: {value!r}")
    return value


def safe_path(root: Path, relative: str, create_parents: bool = False) -> Path:
    relative = normalized_relative(relative)
    current = root
    parts = PurePosixPath(relative).parts
    for part in parts[:-1]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if not create_parents:
                break
            current.mkdir(mode=0o755)
            continue
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise JournalError(f"unsafe parent path: {current}")
    return root.joinpath(*parts)


def path_state(root: Path, relative: str) -> dict:
    path = safe_path(root, relative)
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"type": "absent"}
    mode = f"{stat.S_IMODE(info.st_mode):04o}"
    if stat.S_ISREG(info.st_mode):
        if info.st_nlink != 1:
            raise JournalError(f"regular file must not be hard-linked: {relative}")
        return {
            "type": "regular",
            "mode": mode,
            "sha256": digest_file(path),
            "size": info.st_size,
        }
    if stat.S_ISLNK(info.st_mode):
        target = os.fsencode(os.readlink(path))
        return {
            "type": "symlink",
            "mode": mode,
            "sha256": hashlib.sha256(target).hexdigest(),
            "target": os.fsdecode(target),
        }
    raise JournalError(f"planned path must be regular, symlink, or absent: {relative}")


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_json(path: Path, value: dict, mode: int = 0o600) -> None:
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temp = path.parent / f".{path.name}.tmp.{os.getpid()}.{uuid.uuid4()}"
    descriptor = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        os.chmod(path, mode)
        fsync_directory(path.parent)
    except Exception:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass
        raise


def load_journal(path: Path) -> dict:
    try:
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise JournalError("journal must be one regular non-linked file")
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise JournalError(f"journal is unreadable: {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise JournalError("unsupported preservation journal")
    return value


def strict_load_object(path: Path) -> dict:
    def reject_constant(value: str) -> None:
        raise JournalError(f"non-finite JSON number is forbidden: {value}")

    def pairs(items: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise JournalError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise JournalError(f"JSON input must be one regular non-linked file: {path}")
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=pairs,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise JournalError(f"JSON input is unreadable: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise JournalError(f"JSON input must contain an object: {path}")
    return value


def validate_packet_dir(root: Path, value: str | Path) -> Path:
    raw = Path(value).expanduser().absolute()
    try:
        packet = raw.resolve(strict=True)
    except OSError as exc:
        raise JournalError(f"packet directory is unavailable: {raw}") from exc
    expected_parent = root / ".planning"
    if packet.parent != expected_parent or packet.is_symlink() or not packet.is_dir():
        raise JournalError("packet must be a direct non-symlink child of <repo>/.planning")
    return packet


def packet_member(packet: Path, value: str | Path, *, directory: bool = False) -> Path:
    raw = Path(value).expanduser().absolute()
    try:
        relative = raw.relative_to(packet)
    except ValueError as exc:
        raise JournalError(f"packet artifact escapes packet directory: {raw}") from exc
    current = packet
    for part in relative.parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as exc:
            raise JournalError(f"packet artifact is unavailable: {current}") from exc
        if stat.S_ISLNK(info.st_mode):
            raise JournalError(f"packet artifact path contains a symlink: {current}")
    info = raw.lstat()
    expected = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode) and info.st_nlink == 1
    if not expected:
        kind = "directory" if directory else "single-link regular file"
        raise JournalError(f"packet artifact must be a {kind}: {raw}")
    return raw


def manifest_file_state(path: Path, relative: str) -> dict:
    info = path.lstat()
    mode = f"{stat.S_IMODE(info.st_mode):04o}"
    if stat.S_ISREG(info.st_mode):
        return {
            "path": relative,
            "type": "regular",
            "mode": mode,
            "size": info.st_size,
            "nlink": info.st_nlink,
            "sha256": digest_file(path),
        }
    if stat.S_ISLNK(info.st_mode):
        target = os.fsencode(os.readlink(path))
        return {
            "path": relative,
            "type": "symlink",
            "mode": mode,
            "sha256": hashlib.sha256(target).hexdigest(),
        }
    raise JournalError(f"approved manifest path must be regular or symlink: {relative}")


def reconstruct_applied(
    repo: str,
    packet_value: str,
    slice_id: str,
    source_journal_value: str,
    approved_manifest_value: str,
    candidate_root_value: str,
) -> tuple[Path, dict]:
    """Reconstruct an append-only rollback journal from approved immutable evidence."""

    root = safe_root(repo)
    packet = validate_packet_dir(root, packet_value)
    source_path = packet_member(packet, source_journal_value)
    manifest_path = packet_member(packet, approved_manifest_value)
    candidate_root = packet_member(packet, candidate_root_value, directory=True)
    source = load_journal(source_path)
    if Path(source.get("repository_root", "")) != root:
        raise JournalError("source journal repository root differs")
    if source.get("post_recorded_at") is not None:
        raise JournalError("reconstruction is only for an unapplied historical journal")
    if not slice_id or "/" in slice_id or slice_id in {".", ".."}:
        raise JournalError("slice ID must be one safe path component")

    manifest_wrapper = strict_load_object(manifest_path)
    if set(manifest_wrapper) != {"digest", "manifest"} or not isinstance(manifest_wrapper["manifest"], dict):
        raise JournalError("approved artifact manifest wrapper is not closed")
    manifest = manifest_wrapper["manifest"]
    if digest_value(manifest) != manifest_wrapper["digest"]:
        raise JournalError("approved artifact manifest digest mismatch")
    if manifest.get("repository_root") != str(root) or not isinstance(manifest.get("entries"), list):
        raise JournalError("approved artifact manifest repository or entries differ")
    indexed: dict[str, dict] = {}
    for entry in manifest["entries"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise JournalError("approved artifact manifest entry is malformed")
        if entry["path"] in indexed:
            raise JournalError(f"duplicate approved artifact manifest path: {entry['path']}")
        indexed[entry["path"]] = entry

    source_relative = source_path.relative_to(root).as_posix()
    source_manifest_entry = indexed.get(source_relative)
    if source_manifest_entry is None or source_manifest_entry != manifest_file_state(source_path, source_relative):
        raise JournalError("approved manifest does not bind the source journal bytes")

    candidate_relative_root = candidate_root.relative_to(root).as_posix()
    private_root = packet / "private-preimages"
    private_root.mkdir(mode=0o700, exist_ok=True)
    os.chmod(private_root, 0o700)
    slice_root = private_root / slice_id
    try:
        slice_root.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise JournalError(f"slice already has a preservation journal: {slice_id}") from exc
    backups = slice_root / "backups"
    backups.mkdir(mode=0o700)
    entries: list[dict] = []
    try:
        for source_entry in source["entries"]:
            relative = normalized_relative(source_entry["path"])
            candidate_path = safe_path(candidate_root, relative)
            candidate_manifest_path = f"{candidate_relative_root}/{relative}"
            approved_entry = indexed.get(candidate_manifest_path)
            if approved_entry is None or approved_entry != manifest_file_state(candidate_path, candidate_manifest_path):
                raise JournalError(f"approved manifest does not bind candidate postimage: {relative}")
            candidate_state = path_state(candidate_root, relative)
            observed_state = path_state(root, relative)
            if observed_state != candidate_state:
                raise JournalError(f"current postimage differs from approved candidate: {relative}")

            entry = {
                "path": relative,
                "preimage": source_entry["preimage"],
                "postimage": observed_state,
            }
            if source_entry["preimage"]["type"] == "regular":
                backup_relative = source_entry.get("backup")
                if not isinstance(backup_relative, str) or PurePosixPath(backup_relative).parts[:1] != ("backups",):
                    raise JournalError(f"source backup path is malformed: {relative}")
                source_backup = source_path.parent.joinpath(*PurePosixPath(backup_relative).parts)
                info = source_backup.lstat()
                if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise JournalError(f"source backup is unsafe: {relative}")
                expected_hash = source_entry.get("backup_sha256")
                if digest_file(source_backup) != expected_hash or source_entry["preimage"].get("sha256") != expected_hash:
                    raise JournalError(f"source backup integrity failure: {relative}")
                backup_name = hashlib.sha256(relative.encode("utf-8")).hexdigest()
                destination = backups / backup_name
                descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with source_backup.open("rb") as input_handle, os.fdopen(descriptor, "wb", closefd=True) as output_handle:
                    shutil.copyfileobj(input_handle, output_handle)
                    output_handle.flush()
                    os.fsync(output_handle.fileno())
                if digest_file(destination) != expected_hash:
                    raise JournalError(f"reconstructed backup integrity failure: {relative}")
                entry["backup"] = f"backups/{backup_name}"
                entry["backup_sha256"] = expected_hash
            entries.append(entry)

        fsync_directory(backups)
        journal = {
            "schema_version": SCHEMA_VERSION,
            "slice_id": slice_id,
            "repository_root": str(root),
            "created_at": now(),
            "entries": entries,
            "post_recorded_at": now(),
            "patch_sha256": None,
            "reconstructed_from": {
                "source_journal": source_relative,
                "source_journal_sha256": digest_file(source_path),
                "approved_manifest": manifest_path.relative_to(root).as_posix(),
                "approved_manifest_digest": manifest_wrapper["digest"],
                "candidate_root": candidate_relative_root,
            },
        }
        journal_path = slice_root / "journal.json"
        atomic_json(journal_path, journal)
        fsync_directory(slice_root)
        return journal_path, journal
    except Exception:
        shutil.rmtree(slice_root, ignore_errors=True)
        raise


def snapshot(repo: str, packet_value: str, slice_id: str, paths: list[str]) -> tuple[Path, dict]:
    root = safe_root(repo)
    packet = validate_packet_dir(root, packet_value)
    normalized = [normalized_relative(item) for item in paths]
    if not normalized or len(normalized) != len(set(normalized)):
        raise JournalError("snapshot paths must be nonempty and unique")
    if not slice_id or "/" in slice_id or slice_id in {".", ".."}:
        raise JournalError("slice ID must be one safe path component")
    private_root = packet / "private-preimages"
    private_root.mkdir(mode=0o700, exist_ok=True)
    if private_root.is_symlink():
        raise JournalError("private-preimages must not be a symlink")
    os.chmod(private_root, 0o700)
    slice_root = private_root / slice_id
    try:
        slice_root.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise JournalError(f"slice already has a preservation journal: {slice_id}") from exc
    backups = slice_root / "backups"
    backups.mkdir(mode=0o700)
    entries: list[dict] = []
    try:
        for relative in sorted(normalized, key=lambda item: item.encode("utf-8")):
            preimage = path_state(root, relative)
            entry: dict[str, object] = {"path": relative, "preimage": preimage}
            if preimage["type"] == "regular":
                backup_name = hashlib.sha256(relative.encode("utf-8")).hexdigest()
                backup_path = backups / backup_name
                source = safe_path(root, relative)
                descriptor = os.open(backup_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                try:
                    with source.open("rb") as input_handle, os.fdopen(descriptor, "wb", closefd=True) as output_handle:
                        shutil.copyfileobj(input_handle, output_handle)
                        output_handle.flush()
                        os.fsync(output_handle.fileno())
                except Exception:
                    try:
                        backup_path.unlink()
                    except FileNotFoundError:
                        pass
                    raise
                backup_hash = digest_file(backup_path)
                if backup_hash != preimage["sha256"]:
                    raise JournalError(f"backup hash mismatch: {relative}")
                entry["backup"] = f"backups/{backup_name}"
                entry["backup_sha256"] = backup_hash
            entries.append(entry)
        fsync_directory(backups)
        journal = {
            "schema_version": SCHEMA_VERSION,
            "slice_id": slice_id,
            "repository_root": str(root),
            "created_at": now(),
            "entries": entries,
            "post_recorded_at": None,
            "patch_sha256": None,
        }
        journal_path = slice_root / "journal.json"
        atomic_json(journal_path, journal)
        fsync_directory(slice_root)
        return journal_path, journal
    except Exception:
        shutil.rmtree(slice_root, ignore_errors=True)
        raise


def record_post(journal_path: Path, patch: Path | None) -> dict:
    journal = load_journal(journal_path)
    root = safe_root(journal["repository_root"])
    if journal.get("post_recorded_at") is not None:
        raise JournalError("post-state is already recorded")
    for entry in journal["entries"]:
        entry["postimage"] = path_state(root, entry["path"])
    if patch is not None:
        if not patch.is_file() or patch.is_symlink():
            raise JournalError("owned patch must be a regular file")
        journal["patch_sha256"] = digest_file(patch)
    journal["post_recorded_at"] = now()
    atomic_json(journal_path, journal)
    return journal


def state_equal(left: dict, right: dict) -> bool:
    return left == right


def restore_regular(root: Path, relative: str, entry: dict, journal_path: Path) -> None:
    backup_relative = entry.get("backup")
    if not isinstance(backup_relative, str):
        raise JournalError(f"regular preimage lacks backup: {relative}")
    backup = journal_path.parent / backup_relative
    if digest_file(backup) != entry.get("backup_sha256") or entry["preimage"]["sha256"] != entry.get("backup_sha256"):
        raise JournalError(f"backup integrity failure: {relative}")
    target = safe_path(root, relative, create_parents=True)
    temp = target.parent / f".{target.name}.rollback.{uuid.uuid4()}"
    descriptor = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with backup.open("rb") as input_handle, os.fdopen(descriptor, "wb", closefd=True) as output_handle:
            shutil.copyfileobj(input_handle, output_handle)
            output_handle.flush()
            os.fsync(output_handle.fileno())
        os.chmod(temp, int(entry["preimage"]["mode"], 8))
        if target.exists() or target.is_symlink():
            target.unlink()
        os.replace(temp, target)
        fsync_directory(target.parent)
    except Exception:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass
        raise


def rollback(journal_path: Path) -> dict:
    journal = load_journal(journal_path)
    root = safe_root(journal["repository_root"])
    if journal.get("post_recorded_at") is None:
        raise JournalError("rollback requires recorded post-state")
    for entry in journal["entries"]:
        observed = path_state(root, entry["path"])
        if not state_equal(observed, entry.get("postimage")):
            raise JournalError(f"unsafe rollback; current state drifted: {entry['path']}")
    for entry in journal["entries"]:
        relative = entry["path"]
        target = safe_path(root, relative, create_parents=True)
        preimage = entry["preimage"]
        if preimage["type"] == "absent":
            if target.exists() or target.is_symlink():
                target.unlink()
                fsync_directory(target.parent)
        elif preimage["type"] == "regular":
            restore_regular(root, relative, entry, journal_path)
        elif preimage["type"] == "symlink":
            if target.exists() or target.is_symlink():
                target.unlink()
            os.symlink(preimage["target"], target)
            fsync_directory(target.parent)
        else:
            raise JournalError(f"unsupported preimage type: {preimage['type']}")
    journal["rolled_back_at"] = now()
    journal["rollback_digest"] = digest_value(
        {entry["path"]: path_state(root, entry["path"]) for entry in journal["entries"]}
    )
    atomic_json(journal_path, journal)
    return journal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--repo", required=True)
    snapshot_parser.add_argument("--packet", required=True)
    snapshot_parser.add_argument("--slice-id", required=True)
    snapshot_parser.add_argument("--path", action="append", required=True)
    post_parser = subparsers.add_parser("record-post")
    post_parser.add_argument("journal")
    post_parser.add_argument("--patch")
    rollback_parser = subparsers.add_parser("rollback")
    rollback_parser.add_argument("journal")
    reconstruct_parser = subparsers.add_parser("reconstruct-applied")
    reconstruct_parser.add_argument("--repo", required=True)
    reconstruct_parser.add_argument("--packet", required=True)
    reconstruct_parser.add_argument("--slice-id", required=True)
    reconstruct_parser.add_argument("--source-journal", required=True)
    reconstruct_parser.add_argument("--approved-manifest", required=True)
    reconstruct_parser.add_argument("--candidate-root", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "snapshot":
            journal_path, journal = snapshot(args.repo, args.packet, args.slice_id, args.path)
        elif args.command == "record-post":
            journal_path = Path(args.journal).expanduser().absolute()
            journal = record_post(journal_path, Path(args.patch).expanduser().absolute() if args.patch else None)
        elif args.command == "rollback":
            journal_path = Path(args.journal).expanduser().absolute()
            journal = rollback(journal_path)
        else:
            journal_path, journal = reconstruct_applied(
                args.repo,
                args.packet,
                args.slice_id,
                args.source_journal,
                args.approved_manifest,
                args.candidate_root,
            )
        output = {
            "command": args.command,
            "digest": digest_value(journal),
            "journal": str(journal_path),
            "ok": True,
        }
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
        return 0
    except (JournalError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"command": args.command, "error": str(exc), "ok": False}, sort_keys=True), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
