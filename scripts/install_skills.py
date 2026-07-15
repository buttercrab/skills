#!/usr/bin/env python3
"""Selective, offline-preflighted, recoverable skill installer."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import uuid


JOURNAL_VERSION = "skills-install-transaction/v1"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
TX_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,79}$")


class InstallError(RuntimeError):
    pass


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def canonical_absolute(value: str | Path, label: str) -> Path:
    text = os.fspath(value)
    if "\x00" in text:
        raise InstallError(f"{label} contains NUL")
    path = Path(os.path.abspath(os.path.expanduser(text)))
    if not path.is_absolute():
        raise InstallError(f"{label} must be absolute")
    return path


def inspect_directory_chain(path: Path, label: str) -> list[Path]:
    """Reject symlink or non-directory components and return absent directories."""
    path = canonical_absolute(path, label)
    current = Path(path.anchor)
    missing: list[Path] = []
    for part in path.parts[1:]:
        current = current / part
        if lexists(current):
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode):
                raise InstallError(f"{label} contains a symlink component: {current}")
            if not stat.S_ISDIR(info.st_mode):
                raise InstallError(f"{label} contains a non-directory component: {current}")
        else:
            missing.append(current)
    return missing


def make_missing_directories(paths: list[Path], boundary) -> None:
    for index, path in enumerate(paths, 1):
        if lexists(path):
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise InstallError(f"directory path changed during transaction: {path}")
            continue
        path.mkdir(mode=0o755)
        fsync_directory(path.parent)
        boundary(f"after-target-dir:{index}")


def ensure_private_state_directory(path: Path) -> None:
    missing = inspect_directory_chain(path, "installer state directory")
    for item in missing:
        item.mkdir(mode=0o700)
        fsync_directory(item.parent)
    if path.is_symlink() or not path.is_dir():
        raise InstallError(f"unsafe installer state directory: {path}")
    info = path.stat()
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
        raise InstallError(f"installer state directory must be user-owned mode 0700: {path}")


def strict_json(path: Path) -> dict:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise InstallError(f"unsafe transaction journal: {path}")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InstallError(f"duplicate journal key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InstallError(f"invalid transaction journal: {exc}") from exc
    if not isinstance(value, dict):
        raise InstallError("transaction journal root must be an object")
    return value


def write_journal(path: Path, value: dict) -> None:
    payload = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    temporary = path.parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(temporary, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)
    os.replace(temporary, path)
    fsync_directory(path.parent)


def archive_journal(path: Path, prefix: str, txid: str) -> Path:
    destination = path.parent / f"{prefix}-{txid}.json"
    if lexists(destination):
        raise InstallError(f"journal archive collision: {destination}")
    os.replace(path, destination)
    fsync_directory(path.parent)
    return destination


def exact_link(path: Path, target: str) -> bool:
    return path.is_symlink() and os.readlink(path) == target


def validate_journal(value: dict, repo: Path) -> None:
    expected = {
        "schema_version",
        "transaction_id",
        "repository_root",
        "created_directories",
        "backup_roots",
        "operations",
    }
    if set(value) != expected or value.get("schema_version") != JOURNAL_VERSION:
        raise InstallError("closed transaction journal fields differ")
    if value.get("repository_root") != str(repo):
        raise InstallError("pending transaction belongs to another repository")
    if not isinstance(value.get("transaction_id"), str) or TX_RE.fullmatch(value["transaction_id"]) is None:
        raise InstallError("invalid journal transaction ID")
    for field in ("created_directories", "backup_roots", "operations"):
        if not isinstance(value.get(field), list):
            raise InstallError(f"journal {field} must be a list")
    for operation in value["operations"]:
        if not isinstance(operation, dict) or set(operation) != {
            "name", "source", "target", "backup", "original"
        }:
            raise InstallError("invalid journal operation")
        if NAME_RE.fullmatch(operation.get("name", "")) is None:
            raise InstallError("invalid journal skill name")
        original = operation.get("original")
        if not isinstance(original, dict) or original.get("kind") not in {"absent", "symlink"}:
            raise InstallError("invalid journal original target")
        if original["kind"] == "absent" and set(original) != {"kind"}:
            raise InstallError("invalid absent journal target")
        if original["kind"] == "symlink" and (
            set(original) != {"kind", "target"} or not isinstance(original["target"], str)
        ):
            raise InstallError("invalid symlink journal target")
        for field in ("source", "target", "backup"):
            path = canonical_absolute(operation[field], f"journal {field}")
            if str(path) != operation[field]:
                raise InstallError(f"journal {field} is not normalized")


def rollback(value: dict, *, inject_failure: bool) -> None:
    fail_at = os.environ.get("SKILLS_INSTALL_FAIL_ROLLBACK_AT") if inject_failure else None
    for index, operation in enumerate(reversed(value["operations"]), 1):
        if fail_at == str(index):
            raise InstallError(f"injected rollback failure at operation {index}")
        target = Path(operation["target"])
        source = operation["source"]
        backup = Path(operation["backup"])
        original = operation["original"]
        if original["kind"] == "absent":
            if exact_link(target, source):
                target.unlink()
                fsync_directory(target.parent)
            elif lexists(target):
                raise InstallError(f"rollback refused concurrent target change: {target}")
            if lexists(backup):
                raise InstallError(f"unexpected backup for originally absent target: {backup}")
            continue

        original_target = original["target"]
        if lexists(backup):
            if not backup.is_symlink() or os.readlink(backup) != original_target:
                raise InstallError(f"rollback backup changed: {backup}")
            if exact_link(target, source):
                target.unlink()
            elif lexists(target):
                if exact_link(target, original_target):
                    raise InstallError(f"rollback found both original and backup: {target}")
                raise InstallError(f"rollback refused concurrent target change: {target}")
            os.replace(backup, target)
            fsync_directory(backup.parent)
            fsync_directory(target.parent)
        elif not exact_link(target, original_target):
            raise InstallError(f"rollback cannot reconstruct original target: {target}")

    for text in reversed(value["backup_roots"]):
        path = Path(text)
        if path.is_dir() and not path.is_symlink():
            try:
                path.rmdir()
                fsync_directory(path.parent)
            except OSError as exc:
                raise InstallError(f"rollback backup directory is not empty: {path}") from exc
        elif lexists(path):
            raise InstallError(f"unsafe rollback backup root: {path}")
    for text in reversed(value["created_directories"]):
        path = Path(text)
        if path.is_dir() and not path.is_symlink():
            try:
                path.rmdir()
                fsync_directory(path.parent)
            except OSError as exc:
                raise InstallError(f"rollback created directory is not empty: {path}") from exc
        elif lexists(path):
            raise InstallError(f"unsafe rollback directory: {path}")


def parse_names(values: list[str], option: str, catalog: set[str]) -> set[str]:
    result: set[str] = set()
    for value in values:
        for name in value.split(","):
            if not name or NAME_RE.fullmatch(name) is None:
                raise InstallError(f"{option} contains an invalid skill name: {name!r}")
            if name not in catalog:
                raise InstallError(f"{option} names an unknown skill: {name}")
            result.add(name)
    return result


def discover_catalog(repo: Path) -> dict[str, Path]:
    skills = repo / "skills"
    if skills.is_symlink() or not skills.is_dir():
        raise InstallError(f"unsafe repository skill directory: {skills}")
    result: dict[str, Path] = {}
    for child in sorted(skills.iterdir(), key=lambda item: os.fsencode(item.name)):
        if NAME_RE.fullmatch(child.name) is None:
            continue
        if child.is_symlink() or not child.is_dir():
            continue
        entry = child / "SKILL.md"
        if entry.is_symlink() or not entry.is_file():
            continue
        result[child.name] = child.resolve(strict=True)
    if not result:
        raise InstallError("repository contains no installable skills")
    return result


def preflight_front_build(front: Path, go: str) -> None:
    build_root = Path(tempfile.mkdtemp(prefix="skills-install-front-"))
    try:
        environment = os.environ.copy()
        environment.update({"GOTOOLCHAIN": "local", "GOPROXY": "off", "GOSUMDB": "off"})
        result = subprocess.run(
            [go, "build", "-o", str(build_root / "front-agent-bin"), "./cmd/front-agent"],
            cwd=front,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[-4096:]
            raise InstallError(f"offline Front Agent preflight failed: {detail}")
    finally:
        shutil.rmtree(build_root, ignore_errors=True)


def make_boundary():
    fail_at = os.environ.get("SKILLS_INSTALL_FAIL_AT")
    crash_at = os.environ.get("SKILLS_INSTALL_CRASH_AT")
    hold_at = os.environ.get("SKILLS_INSTALL_HOLD_AT")
    hold_seconds = float(os.environ.get("SKILLS_INSTALL_HOLD_SECONDS", "10"))

    def boundary(name: str) -> None:
        if crash_at == name:
            os._exit(97)
        if fail_at == name:
            raise InstallError(f"injected installer failure at {name}")
        if hold_at == name:
            time.sleep(hold_seconds)

    return boundary


def acquire_lock(state_dir: Path):
    lock_path = state_dir / "lock"
    if lock_path.is_symlink():
        raise InstallError(f"unsafe installer lock: {lock_path}")
    descriptor = os.open(
        lock_path,
        os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    info = os.fstat(descriptor)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid():
        os.close(descriptor)
        raise InstallError(f"unsafe installer lock: {lock_path}")
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        os.close(descriptor)
        raise InstallError("another installer transaction holds the all-target lock") from exc
    return descriptor


def build_transaction(
    repo: Path,
    selected: list[str],
    catalog: dict[str, Path],
    target_dirs: list[Path],
    txid: str,
) -> dict:
    created: list[Path] = []
    for target_dir in target_dirs:
        for path in inspect_directory_chain(target_dir, "skill target directory"):
            if path not in created:
                created.append(path)

    operations: list[dict] = []
    backup_roots: list[Path] = []
    for target_dir in target_dirs:
        backup_root = target_dir / f".skills-install-backup-{txid}"
        if lexists(backup_root):
            raise InstallError(f"backup collision: {backup_root}")
        target_operations: list[dict] = []
        for name in selected:
            source = str(catalog[name])
            target = target_dir / name
            if exact_link(target, source):
                continue
            if lexists(target) and not target.is_symlink():
                raise InstallError(f"refusing to replace user-owned non-link target: {target}")
            original = (
                {"kind": "symlink", "target": os.readlink(target)}
                if target.is_symlink()
                else {"kind": "absent"}
            )
            target_operations.append(
                {
                    "name": name,
                    "source": source,
                    "target": str(target),
                    "backup": str(backup_root / name),
                    "original": original,
                }
            )
        if target_operations:
            backup_roots.append(backup_root)
            operations.extend(target_operations)
    return {
        "schema_version": JOURNAL_VERSION,
        "transaction_id": txid,
        "repository_root": str(repo),
        "created_directories": [str(path) for path in created],
        "backup_roots": [str(path) for path in backup_roots],
        "operations": operations,
    }


def verify_original(operation: dict) -> None:
    target = Path(operation["target"])
    original = operation["original"]
    if original["kind"] == "absent":
        if lexists(target):
            raise InstallError(f"target changed after preflight: {target}")
    elif not exact_link(target, original["target"]):
        raise InstallError(f"target changed after preflight: {target}")


def apply_transaction(value: dict, boundary) -> None:
    make_missing_directories([Path(item) for item in value["created_directories"]], boundary)
    for index, text in enumerate(value["backup_roots"], 1):
        root = Path(text)
        if lexists(root):
            raise InstallError(f"backup root appeared during transaction: {root}")
        root.mkdir(mode=0o700)
        if root.stat().st_dev != root.parent.stat().st_dev:
            raise InstallError(f"backup is not on the target filesystem: {root}")
        fsync_directory(root.parent)
        boundary(f"after-backup-dir:{index}")

    for index, operation in enumerate(value["operations"], 1):
        verify_original(operation)
        target = Path(operation["target"])
        backup = Path(operation["backup"])
        if operation["original"]["kind"] == "symlink":
            os.replace(target, backup)
            fsync_directory(backup.parent)
            fsync_directory(target.parent)
        boundary(f"after-backup:{index}")
        if lexists(target):
            raise InstallError(f"target unexpectedly exists before linking: {target}")
        os.symlink(operation["source"], target)
        fsync_directory(target.parent)
        boundary(f"after-link:{index}")
    boundary("before-cleanup")


def install(args) -> int:
    repo = Path(args.repo).resolve(strict=True)
    catalog = discover_catalog(repo)
    names = set(catalog)
    if args.list_mode:
        if args.only or args.exclude:
            raise InstallError("--list cannot be combined with --only or --exclude")
        for name in sorted(names):
            print(name)
        return 0

    only = parse_names(args.only, "--only", names)
    excluded = parse_names(args.exclude, "--exclude", names)
    selected = sorted((only if args.only else names) - excluded)
    if not selected:
        print("No skills selected; no target directories changed.")
        return 0

    for name in selected:
        source = catalog[name]
        if source.is_symlink() or not source.is_dir() or not (source / "SKILL.md").is_file():
            raise InstallError(f"selected source failed preflight: {source}")
    if "front-agent-orchestration" in selected:
        go = shutil.which("go")
        if go is None:
            if selected == ["front-agent-orchestration"]:
                raise InstallError(
                    "cannot install front-agent-orchestration because Go was not found"
                )
            selected.remove("front-agent-orchestration")
            print(
                "Skipping front-agent-orchestration because Go was not found; "
                "continuing with the other selected skills.",
                file=sys.stderr,
            )
        else:
            preflight_front_build(catalog["front-agent-orchestration"], go)

    home = canonical_absolute(os.environ.get("HOME", str(Path.home())), "HOME")
    agent_dir = canonical_absolute(
        os.environ.get("AGENT_SKILLS_DIR", str(home / ".agents" / "skills")),
        "Agent skill directory",
    )
    codex_dir = canonical_absolute(
        os.environ.get("CODEX_SKILLS_DIR", str(home / ".codex" / "skills")),
        "Codex skill directory",
    )
    if agent_dir == codex_dir:
        raise InstallError("Agent and Codex skill directories must be distinct")
    if agent_dir in codex_dir.parents or codex_dir in agent_dir.parents:
        raise InstallError("Agent and Codex skill directories must not overlap")
    inspect_directory_chain(agent_dir, "Agent skill directory")
    inspect_directory_chain(codex_dir, "Codex skill directory")

    state_dir = canonical_absolute(
        os.environ.get("SKILLS_INSTALL_STATE_DIR", str(home / ".skills-install-state")),
        "installer state directory",
    )
    ensure_private_state_directory(state_dir)
    lock_descriptor = acquire_lock(state_dir)
    boundary = make_boundary()
    journal_path = state_dir / "journal.json"
    try:
        boundary("after-lock")
        hold = os.environ.get("SKILLS_INSTALL_HOLD_LOCK_SECONDS")
        if hold:
            time.sleep(float(hold))

        if lexists(journal_path):
            pending = strict_json(journal_path)
            validate_journal(pending, repo)
            rollback(pending, inject_failure=False)
            archived = archive_journal(
                journal_path, "recovered", pending["transaction_id"]
            )
            print(f"Recovered interrupted installer transaction; journal: {archived}")

        txid = os.environ.get("SKILLS_INSTALL_TXID", str(uuid.uuid4()))
        if TX_RE.fullmatch(txid) is None:
            raise InstallError("SKILLS_INSTALL_TXID is invalid")
        transaction = build_transaction(
            repo, selected, catalog, [agent_dir, codex_dir], txid
        )
        if not transaction["operations"]:
            print("Selected skills are already installed in both targets.")
            return 0

        validate_journal(transaction, repo)
        write_journal(journal_path, transaction)
        try:
            boundary("after-journal")
            apply_transaction(transaction, boundary)
        except BaseException as original_error:
            try:
                rollback(transaction, inject_failure=True)
                archived = archive_journal(journal_path, "failed", txid)
                raise InstallError(
                    f"transaction failed; rollback completed; journal preserved at {archived}: {original_error}"
                ) from original_error
            except InstallError as rollback_error:
                if "rollback completed" in str(rollback_error):
                    raise
                raise InstallError(
                    f"transaction failed and rollback failed; recovery journal preserved at {journal_path}: "
                    f"original={original_error}; rollback={rollback_error}"
                ) from rollback_error

        for text in transaction["backup_roots"]:
            root = Path(text)
            if root.is_dir() and not any(root.iterdir()):
                root.rmdir()
                fsync_directory(root.parent)
        journal_path.unlink()
        fsync_directory(journal_path.parent)
        print(
            f"Installed {len(selected)} selected skills into {agent_dir} and {codex_dir}."
        )
        retained = [path for path in transaction["backup_roots"] if Path(path).is_dir()]
        for path in retained:
            print(f"Retained same-filesystem backup: {path}")
        return 0
    finally:
        fcntl.flock(lock_descriptor, fcntl.LOCK_UN)
        os.close(lock_descriptor)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help=argparse.SUPPRESS)
    parser.add_argument("--list", dest="list_mode", action="store_true", help="list installable skill names")
    parser.add_argument("--only", action="append", default=[], metavar="NAME[,NAME]", help="install only named skills")
    parser.add_argument("--exclude", action="append", default=[], metavar="NAME[,NAME]", help="exclude named skills")
    args = parser.parse_args(argv)

    def interrupted(signum, _frame):
        raise InstallError(f"installer interrupted by signal {signum}")

    for name in ("SIGINT", "SIGTERM", "SIGHUP"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), interrupted)
    try:
        return install(args)
    except (InstallError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"install.sh: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
