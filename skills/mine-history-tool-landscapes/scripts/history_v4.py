#!/usr/bin/env python3
"""History v4 security, identity, migration, and reconciliation primitives.

The module is dependency-free except for optional JSON Schema validation.  It
never treats a producer-declared hash as authority: callers must reopen bytes
through :func:`acquire_file` and pass the acquired payload into validation.
"""

from __future__ import annotations

from copy import deepcopy
import datetime as dt
import errno
import hashlib
import hmac
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import unicodedata
from typing import Any, Callable, Iterable

from strict_json import StrictJSONError, canonical_bytes, loads_strict


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / "references"
SPEC_PATH = REFERENCE_ROOT / "history-v4-specification.md"
SCHEMA_PATHS = {
    "history-sources/v4": REFERENCE_ROOT / "history-sources-v4.schema.json",
    "semantic-observation-ledger/v2": REFERENCE_ROOT / "semantic-observation-ledger-v2.schema.json",
    "history-index/v4": REFERENCE_ROOT / "history-index-v4.schema.json",
    "capability-reduction/v3": REFERENCE_ROOT / "capability-reduction-v3.schema.json",
    "history-evidence/v1": REFERENCE_ROOT / "history-evidence-v1.schema.json",
    "history-publication/v3": REFERENCE_ROOT / "history-publication-v3.schema.json",
}

MIGRATION_ORDER = (
    ("history", "history-sources/v4", "E_HISTORY_SOURCES_VERSION_UNSUPPORTED"),
    ("raw_snapshot", "raw-source-manifest/v2", "E_RAW_SNAPSHOT_REBUILD_REQUIRED"),
    ("ledger", "semantic-observation-ledger/v2", "E_SEMANTIC_LEDGER_REBUILD_REQUIRED"),
    ("index", "history-index/v4", "E_HISTORY_INDEX_REBUILD_REQUIRED"),
    ("reduction", "capability-reduction/v3", "E_CAPABILITY_REDUCTION_VERSION_UNSUPPORTED"),
    ("evidence", "history-evidence/v1", "E_HISTORY_EVIDENCE_VERSION_UNSUPPORTED"),
    ("publication", "history-publication/v3", "E_HISTORY_PUBLICATION_VERSION_UNSUPPORTED"),
)

LINEAGE_COUNT_FIELDS = {
    "sources": "source_ids",
    "records": "record_ids",
    "semantic_records": "semantic_record_ids",
    "excluded_records": "excluded_record_ids",
    "nonsemantic_records": "nonsemantic_record_ids",
    "observations": "observation_ids",
    "nodes": "node_ids",
    "roots": "root_ids",
    "children": "child_ids",
    "unresolved": "unresolved_ids",
    "duplicate_exports": "duplicate_export_ids",
    "nonsemantic": "nonsemantic_ids",
    "excluded": "excluded_ids",
    "namespaces": "namespace_ids",
    "project_families": "project_family_ids",
}

PUBLICATION_FORBIDDEN = (
    re.compile(r"(?:^|\s)/(?:Users|home|private|var|tmp)/"),
    re.compile(r"(?:https?|file|ssh)://", re.I),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    re.compile(r"\b(?:sk-|gh[pousr]_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{12,}"),
    re.compile(r"\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]", re.I),
)

REQUIRED_PRIVATE_MEMBERS = {
    "index.json": "manifest",
    "sources.json": "source-contract",
    "semantic-ledger.json": "semantic-ledger",
    "exclusion-ledger.json": "exclusion-ledger",
    "native-map.json": "native-map",
    "identity-salt": "identity-salt",
    "identity-key": "identity-key",
    "identity-key.receipt.json": "identity-key-receipt",
    "adapter-catalog.json": "adapter-catalog",
    "lifecycle.json": "lifecycle",
}

LIFECYCLE_TRANSITIONS = {
    ("collecting", "live"),
    ("live", "validation-complete"),
    ("live", "expired"),
    ("validation-complete", "deletion-pending"),
    ("expired", "deletion-pending"),
    ("deletion-pending", "deleted"),
}

OPAQUE_ID = re.compile(r"(?:[a-z][a-z0-9-]{2,31}-[0-9a-f]{32,64}|obs-[0-9a-f]{64})")


class HistoryV4Error(ValueError):
    """Stable, closed diagnostic failure."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def fail(code: str, detail: str = "") -> None:
    raise HistoryV4Error(code, detail)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def D(domain: str, value: object) -> str:
    return sha256_bytes(domain.encode("ascii") + b"\0" + canonical_bytes(value))


def without(value: dict[str, Any], *fields: str) -> dict[str, Any]:
    result = deepcopy(value)
    for field in fields:
        result.pop(field, None)
    return result


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def parse_time(value: object, field: str) -> dt.datetime:
    if not isinstance(value, str):
        fail("E_TIMESTAMP_INVALID", field)
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail("E_TIMESTAMP_INVALID", field)
    if parsed.tzinfo is None:
        fail("E_TIMESTAMP_INVALID", field)
    return parsed.astimezone(dt.timezone.utc)


def normalized_relative(value: object) -> str:
    if not isinstance(value, str) or not value or "\0" in value or "\\" in value:
        fail("E_DESCRIPTOR_PATH", repr(value))
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        fail("E_DESCRIPTOR_PATH", value)
    normalized = "/".join(unicodedata.normalize("NFC", part) for part in path.parts)
    if len(set(path.parts)) != len(set(unicodedata.normalize("NFC", part) for part in path.parts)):
        fail("E_DESCRIPTOR_PATH", "normalized component collision")
    return normalized


def root_authority(root: Path, expected_uid: int) -> str:
    return D(
        "descriptor-root-authority/v2",
        {"canonical_root_sha256": sha256_bytes(str(root).encode()), "effective_uid": expected_uid},
    )


def _facts(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        info.st_nlink,
        stat.S_IFMT(info.st_mode),
        stat.S_IMODE(info.st_mode),
        info.st_uid,
    )


def _mode(info: os.stat_result) -> str:
    return f"0{stat.S_IMODE(info.st_mode):03o}"


def acquire_file(
    root: Path,
    relative: str,
    *,
    max_bytes: int,
    aggregate: list[int] | None = None,
    max_total_bytes: int | None = None,
    expected_uid: int | None = None,
    cutoff_ns: int | None = None,
    captured_at: str | None = None,
    post_read_hook: Callable[[int], None] | None = None,
) -> tuple[dict[str, Any], bytes]:
    """Acquire one leaf once through a retained descriptor-relative chain."""

    if not hasattr(os, "O_NOFOLLOW") or not os.supports_dir_fd:
        fail("E_DESCRIPTOR_PLATFORM_UNSAFE")
    relative = normalized_relative(relative)
    raw_root = root.expanduser().absolute()
    if raw_root.is_symlink():
        fail("E_DESCRIPTOR_SYMLINK", str(raw_root))
    canonical_root = raw_root.resolve(strict=True)
    expected_uid = os.geteuid() if expected_uid is None else expected_uid
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    root_fd = os.open(canonical_root, flags)
    current_fd = root_fd
    leaf_fd: int | None = None
    try:
        parts = relative.split("/")
        for part in parts[:-1]:
            info = os.stat(part, dir_fd=current_fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                fail("E_DESCRIPTOR_SYMLINK", relative)
            if not stat.S_ISDIR(info.st_mode):
                fail("E_DESCRIPTOR_NOT_REGULAR", relative)
            next_fd = os.open(part, flags, dir_fd=current_fd)
            if current_fd != root_fd:
                os.close(current_fd)
            current_fd = next_fd
        before_path = os.stat(parts[-1], dir_fd=current_fd, follow_symlinks=False)
        if stat.S_ISLNK(before_path.st_mode):
            fail("E_DESCRIPTOR_SYMLINK", relative)
        leaf_fd = os.open(
            parts[-1], os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW, dir_fd=current_fd
        )
        before = os.fstat(leaf_fd)
        if _facts(before_path) != _facts(before):
            fail("E_DESCRIPTOR_SWAP", relative)
        if not stat.S_ISREG(before.st_mode):
            fail("E_DESCRIPTOR_NOT_REGULAR", relative)
        if before.st_nlink != 1:
            fail("E_DESCRIPTOR_HARD_LINK", relative)
        if before.st_uid != expected_uid:
            fail("E_DESCRIPTOR_OWNER", relative)
        if stat.S_IMODE(before.st_mode) & 0o022:
            fail("E_DESCRIPTOR_UNSAFE_MODE", relative)
        if before.st_size > max_bytes:
            fail("E_DESCRIPTOR_SIZE_LIMIT", relative)
        if cutoff_ns is not None and before.st_mtime_ns > cutoff_ns:
            fail("E_DESCRIPTOR_AFTER_CUTOFF", relative)
        chunks: list[bytes] = []
        actual = 0
        while True:
            chunk = os.read(leaf_fd, min(1024 * 1024, max_bytes - actual + 1))
            if not chunk:
                break
            actual += len(chunk)
            if actual > max_bytes:
                fail("E_DESCRIPTOR_SIZE_LIMIT", relative)
            if aggregate is not None:
                aggregate[0] += len(chunk)
                if max_total_bytes is not None and aggregate[0] > max_total_bytes:
                    fail("E_DESCRIPTOR_AGGREGATE_LIMIT", relative)
            chunks.append(chunk)
        if post_read_hook is not None:
            post_read_hook(leaf_fd)
        after = os.fstat(leaf_fd)
        if _facts(before) != _facts(after) or actual != before.st_size:
            fail("E_DESCRIPTOR_SWAP", relative)
        payload = b"".join(chunks)
        descriptor = {
            "schema_version": "descriptor-file/v2",
            "root_authority_sha256": root_authority(canonical_root, expected_uid),
            "relative_path_sha256": sha256_bytes(relative.encode()),
            "device": before.st_dev,
            "inode": before.st_ino,
            "size": before.st_size,
            "mode": _mode(before),
            "uid": before.st_uid,
            "nlink": before.st_nlink,
            "mtime_ns": before.st_mtime_ns,
            "captured_at": captured_at or iso_now(),
            "sha256": sha256_bytes(payload),
            "open_flags": ["O_RDONLY", "O_CLOEXEC", "O_NOFOLLOW"],
        }
        return descriptor, payload
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.EMLINK}:
            fail("E_DESCRIPTOR_SYMLINK", relative)
        fail("E_DESCRIPTOR_OPEN", f"{relative}: {exc}")
    finally:
        if leaf_fd is not None:
            os.close(leaf_fd)
        if current_fd != root_fd:
            os.close(current_fd)
        os.close(root_fd)


def acquire_exact_bundle(
    root: Path,
    declared: Iterable[str],
    *,
    max_file_bytes: int,
    max_total_bytes: int,
    expected_uid: int | None = None,
) -> dict[str, tuple[dict[str, Any], bytes]]:
    """Enumerate and acquire one exact recursive set under one retained root FD."""

    if not hasattr(os, "O_NOFOLLOW") or not os.supports_dir_fd:
        fail("E_DESCRIPTOR_PLATFORM_UNSAFE")
    declared_set = {normalized_relative(item) for item in declared}
    raw_root = root.expanduser().absolute()
    if raw_root.is_symlink():
        fail("E_DESCRIPTOR_SYMLINK", str(raw_root))
    canonical_root = raw_root.resolve(strict=True)
    expected_uid = os.geteuid() if expected_uid is None else expected_uid
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    root_fd = os.open(canonical_root, directory_flags)

    def enumerate_at(directory_fd: int, prefix: str = "") -> set[str]:
        result: set[str] = set()
        for name in os.listdir(directory_fd):
            relative = f"{prefix}/{name}" if prefix else name
            normalized_relative(relative)
            info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                fail("E_DESCRIPTOR_SYMLINK", relative)
            if stat.S_ISDIR(info.st_mode):
                child = os.open(name, directory_flags, dir_fd=directory_fd)
                try:
                    result.update(enumerate_at(child, relative))
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode):
                result.add(relative)
            else:
                fail("E_DESCRIPTOR_NOT_REGULAR", relative)
        return result

    def read_at(relative: str, aggregate: list[int]) -> tuple[dict[str, Any], bytes]:
        current = os.dup(root_fd)
        leaf_fd: int | None = None
        try:
            parts = relative.split("/")
            for part in parts[:-1]:
                info = os.stat(part, dir_fd=current, follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    fail("E_DESCRIPTOR_SYMLINK", relative)
                if not stat.S_ISDIR(info.st_mode):
                    fail("E_DESCRIPTOR_NOT_REGULAR", relative)
                child = os.open(part, directory_flags, dir_fd=current)
                os.close(current)
                current = child
            before_path = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
            leaf_fd = os.open(
                parts[-1],
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
                dir_fd=current,
            )
            before = os.fstat(leaf_fd)
            if _facts(before_path) != _facts(before):
                fail("E_DESCRIPTOR_SWAP", relative)
            if not stat.S_ISREG(before.st_mode):
                fail("E_DESCRIPTOR_NOT_REGULAR", relative)
            if before.st_nlink != 1:
                fail("E_DESCRIPTOR_HARD_LINK", relative)
            if before.st_uid != expected_uid:
                fail("E_DESCRIPTOR_OWNER", relative)
            if stat.S_IMODE(before.st_mode) & 0o022:
                fail("E_DESCRIPTOR_UNSAFE_MODE", relative)
            if before.st_size > max_file_bytes:
                fail("E_DESCRIPTOR_SIZE_LIMIT", relative)
            chunks: list[bytes] = []
            actual = 0
            while True:
                chunk = os.read(leaf_fd, min(1024 * 1024, max_file_bytes - actual + 1))
                if not chunk:
                    break
                actual += len(chunk)
                aggregate[0] += len(chunk)
                if actual > max_file_bytes:
                    fail("E_DESCRIPTOR_SIZE_LIMIT", relative)
                if aggregate[0] > max_total_bytes:
                    fail("E_DESCRIPTOR_AGGREGATE_LIMIT", relative)
                chunks.append(chunk)
            after = os.fstat(leaf_fd)
            if _facts(before) != _facts(after) or actual != before.st_size:
                fail("E_DESCRIPTOR_SWAP", relative)
            payload = b"".join(chunks)
            descriptor = {
                "schema_version": "descriptor-file/v2",
                "root_authority_sha256": root_authority(canonical_root, expected_uid),
                "relative_path_sha256": sha256_bytes(relative.encode()),
                "device": before.st_dev,
                "inode": before.st_ino,
                "size": before.st_size,
                "mode": _mode(before),
                "uid": before.st_uid,
                "nlink": before.st_nlink,
                "mtime_ns": before.st_mtime_ns,
                "captured_at": iso_now(),
                "sha256": sha256_bytes(payload),
                "open_flags": ["O_RDONLY", "O_CLOEXEC", "O_NOFOLLOW"],
            }
            return descriptor, payload
        finally:
            if leaf_fd is not None:
                os.close(leaf_fd)
            os.close(current)

    try:
        actual = enumerate_at(root_fd)
        if actual != declared_set:
            fail(
                "E_PRIVATE_FILE_SET_MISMATCH",
                f"missing={sorted(declared_set-actual)} extra={sorted(actual-declared_set)}",
            )
        aggregate = [0]
        acquired = {
            relative: read_at(relative, aggregate)
            for relative in sorted(declared_set, key=lambda item: item.encode())
        }
        if enumerate_at(root_fd) != actual:
            fail("E_DESCRIPTOR_SWAP", "exact file set changed during acquisition")
        return acquired
    finally:
        os.close(root_fd)


def _history_path_matches(relative: str, pattern: str) -> bool:
    """Match the deliberately small History v4 JSONL allowlist grammar."""

    relative = normalized_relative(relative)
    pattern = normalized_relative(pattern)
    recursive_suffix = "/**/*.jsonl"
    direct_suffix = "/*.jsonl"
    if pattern.endswith(recursive_suffix):
        prefix = pattern[: -len(recursive_suffix)]
        suffix = relative[len(prefix) + 1 :] if relative.startswith(prefix + "/") else ""
        return bool(suffix) and suffix.endswith(".jsonl")
    if pattern.endswith(direct_suffix):
        prefix = pattern[: -len(direct_suffix)]
        suffix = relative[len(prefix) + 1 :] if relative.startswith(prefix + "/") else ""
        return bool(suffix) and "/" not in suffix and suffix.endswith(".jsonl")
    fail("E_USER_ROOT_AUTHORITY", f"unsupported allowlist pattern {pattern!r}")


def acquire_allowed_tree(
    root: Path,
    allowlist: Iterable[str],
    *,
    max_file_bytes: int,
    max_total_bytes: int,
    expected_uid: int | None = None,
) -> dict[str, tuple[dict[str, Any], bytes]]:
    """Discover and reopen every allowlisted history leaf under one retained root FD.

    The root and every traversed directory stay descriptor-relative.  A second
    enumeration after all reads makes source-set additions and removals fail
    closed instead of silently producing an incomplete history snapshot.
    """

    patterns = tuple(normalized_relative(item) for item in allowlist)
    if not patterns:
        fail("E_USER_ROOT_AUTHORITY", "empty history allowlist")
    prefixes = {item.split("/", 1)[0] for item in patterns}
    if any("*" in prefix for prefix in prefixes):
        fail("E_USER_ROOT_AUTHORITY", "wildcard root prefix")
    if not hasattr(os, "O_NOFOLLOW") or not os.supports_dir_fd:
        fail("E_DESCRIPTOR_PLATFORM_UNSAFE")
    raw_root = root.expanduser().absolute()
    if raw_root.is_symlink():
        fail("E_DESCRIPTOR_SYMLINK", str(raw_root))
    canonical_root = raw_root.resolve(strict=True)
    expected_uid = os.geteuid() if expected_uid is None else expected_uid
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    root_fd = os.open(canonical_root, directory_flags)

    def enumerate_matching() -> set[str]:
        result: set[str] = set()

        def walk(directory_fd: int, prefix: str) -> None:
            for name in os.listdir(directory_fd):
                relative = f"{prefix}/{name}"
                normalized_relative(relative)
                info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    fail("E_DESCRIPTOR_SYMLINK", relative)
                if stat.S_ISDIR(info.st_mode):
                    child = os.open(name, directory_flags, dir_fd=directory_fd)
                    try:
                        walk(child, relative)
                    finally:
                        os.close(child)
                elif stat.S_ISREG(info.st_mode):
                    if any(_history_path_matches(relative, pattern) for pattern in patterns):
                        result.add(relative)
                else:
                    fail("E_DESCRIPTOR_NOT_REGULAR", relative)

        for prefix in sorted(prefixes, key=lambda item: item.encode()):
            try:
                info = os.stat(prefix, dir_fd=root_fd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            if stat.S_ISLNK(info.st_mode):
                fail("E_DESCRIPTOR_SYMLINK", prefix)
            if not stat.S_ISDIR(info.st_mode):
                fail("E_DESCRIPTOR_NOT_REGULAR", prefix)
            child = os.open(prefix, directory_flags, dir_fd=root_fd)
            try:
                walk(child, prefix)
            finally:
                os.close(child)
        return result

    def read_at(relative: str, aggregate: list[int]) -> tuple[dict[str, Any], bytes]:
        current = os.dup(root_fd)
        leaf_fd: int | None = None
        try:
            parts = relative.split("/")
            for part in parts[:-1]:
                info = os.stat(part, dir_fd=current, follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    fail("E_DESCRIPTOR_SYMLINK", relative)
                if not stat.S_ISDIR(info.st_mode):
                    fail("E_DESCRIPTOR_NOT_REGULAR", relative)
                child = os.open(part, directory_flags, dir_fd=current)
                os.close(current)
                current = child
            before_path = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
            leaf_fd = os.open(
                parts[-1], os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW, dir_fd=current
            )
            before = os.fstat(leaf_fd)
            if _facts(before_path) != _facts(before):
                fail("E_DESCRIPTOR_SWAP", relative)
            if not stat.S_ISREG(before.st_mode):
                fail("E_DESCRIPTOR_NOT_REGULAR", relative)
            if before.st_nlink != 1:
                fail("E_DESCRIPTOR_HARD_LINK", relative)
            if before.st_uid != expected_uid:
                fail("E_DESCRIPTOR_OWNER", relative)
            if stat.S_IMODE(before.st_mode) & 0o022:
                fail("E_DESCRIPTOR_UNSAFE_MODE", relative)
            if before.st_size > max_file_bytes:
                fail("E_DESCRIPTOR_SIZE_LIMIT", relative)
            chunks: list[bytes] = []
            actual = 0
            while True:
                chunk = os.read(leaf_fd, min(1024 * 1024, max_file_bytes - actual + 1))
                if not chunk:
                    break
                actual += len(chunk)
                aggregate[0] += len(chunk)
                if actual > max_file_bytes:
                    fail("E_DESCRIPTOR_SIZE_LIMIT", relative)
                if aggregate[0] > max_total_bytes:
                    fail("E_DESCRIPTOR_AGGREGATE_LIMIT", relative)
                chunks.append(chunk)
            after = os.fstat(leaf_fd)
            if _facts(before) != _facts(after) or actual != before.st_size:
                fail("E_DESCRIPTOR_SWAP", relative)
            payload = b"".join(chunks)
            return (
                {
                    "schema_version": "descriptor-file/v2",
                    "root_authority_sha256": root_authority(canonical_root, expected_uid),
                    "relative_path_sha256": sha256_bytes(relative.encode()),
                    "device": before.st_dev,
                    "inode": before.st_ino,
                    "size": before.st_size,
                    "mode": _mode(before),
                    "uid": before.st_uid,
                    "nlink": before.st_nlink,
                    "mtime_ns": before.st_mtime_ns,
                    "captured_at": iso_now(),
                    "sha256": sha256_bytes(payload),
                    "open_flags": ["O_RDONLY", "O_CLOEXEC", "O_NOFOLLOW"],
                },
                payload,
            )
        finally:
            if leaf_fd is not None:
                os.close(leaf_fd)
            os.close(current)

    try:
        discovered = enumerate_matching()
        aggregate = [0]
        acquired = {
            relative: read_at(relative, aggregate)
            for relative in sorted(discovered, key=lambda item: item.encode())
        }
        if enumerate_matching() != discovered:
            fail("E_DESCRIPTOR_SWAP", "history source set changed during acquisition")
        return acquired
    finally:
        os.close(root_fd)


def derive_native_hmac(key: bytes, salt: bytes, platform: str, native_type: str, native_value: str) -> str:
    if len(key) != 32 or len(salt) != 32:
        fail("E_INDEX_IDENTITY_MATERIAL", "key and salt must be exactly 32 bytes")
    message = b"history-native-id/v2\0" + salt + b"\0" + f"{platform}:{native_type}:{native_value}".encode()
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def derive_public_id(key: bytes, salt: bytes, public_type: str, prefix: str, native_hmac: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", native_hmac):
        fail("E_INDEX_IDENTITY_MATERIAL", "native HMAC")
    message = (
        b"history-public-id/v2\0"
        + salt
        + b"\0"
        + public_type.encode()
        + b"\0"
        + bytes.fromhex(native_hmac)
    )
    return f"{prefix}-{hmac.new(key, message, hashlib.sha256).hexdigest()}"


def select_user_root(platform: str, *, home: Path, environment: dict[str, str] | None = None) -> tuple[Path, dict[str, Any]]:
    """Select the actual authenticated-user root, never transcript metadata."""

    if platform not in {"codex", "claude-code"}:
        fail("E_USER_ROOT_AUTHORITY", platform)
    environment = os.environ if environment is None else environment
    variable = "CODEX_HOME" if platform == "codex" else "CLAUDE_CONFIG_DIR"
    default = ".codex" if platform == "codex" else ".claude"
    present = variable in environment and bool(environment[variable])
    selected = Path(environment[variable]).expanduser() if present else home / default
    raw = selected.absolute()
    if raw.is_symlink():
        fail("E_USER_ROOT_AUTHORITY", str(raw))
    canonical = raw.resolve(strict=True)
    receipt = {
        "platform": platform,
        "effective_uid": os.geteuid(),
        "canonical_user_home_sha256": sha256_bytes(str(home.resolve(strict=True)).encode()),
        "environment_variable": variable,
        "environment_present": present,
        "environment_value_sha256": (
            sha256_bytes(environment[variable].encode()) if present else None
        ),
        "selected_root_sha256": sha256_bytes(str(canonical).encode()),
        "selection_basis": "host-resolved-environment" if present else "authenticated-user-home-default",
        "captured_at": iso_now(),
    }
    return canonical, receipt


def load_document(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = loads_strict(payload.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, StrictJSONError) as exc:
        fail("E_SCHEMA", f"{label}: {exc}")
    if not isinstance(value, dict):
        fail("E_SCHEMA", f"{label}: expected object")
    return value


def validate_schema(document: dict[str, Any]) -> None:
    """Validate one successor document when jsonschema is available."""

    version = document.get("schema_version")
    path = SCHEMA_PATHS.get(version)
    if path is None:
        fail("E_SCHEMA", f"unknown successor version {version!r}")
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        fail("E_VALIDATOR_DEPENDENCY", "jsonschema is required for closed-schema validation")
    schema = load_document(path.read_bytes(), path.name)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        first = errors[0]
        fail("E_SCHEMA", f"{version}:{list(first.absolute_path)}: {first.message}")


def ordered_migration_diagnostic(
    documents: dict[str, dict[str, Any] | None],
    *,
    authoritative_raw_reopen: bool,
    exact_history_binding: bool,
    exact_model_available: bool,
) -> str | None:
    """Return the first normative migration diagnostic before schema checks."""

    for key, version, diagnostic in MIGRATION_ORDER:
        document = documents.get(key)
        if key == "raw_snapshot":
            history = documents.get("history") or {}
            raw = history.get("raw_manifest") if isinstance(history, dict) else None
            if not isinstance(raw, dict) or raw.get("schema_version") != version:
                return diagnostic
        elif document is None or document.get("schema_version") != version:
            return diagnostic
    if not exact_history_binding:
        return "E_HISTORY_BINDING_REQUIRED"
    if not authoritative_raw_reopen:
        return "E_RAW_REOPEN_REQUIRED"
    if not exact_model_available:
        return "E_EXPLORATION_MODEL_UNAVAILABLE"
    return None


def _sorted_unique(values: object, label: str) -> list[Any]:
    if not isinstance(values, list):
        fail("E_SET_COUNT_MISMATCH", label)
    canonical = [canonical_bytes(item) for item in values]
    if canonical != sorted(canonical) or len(canonical) != len(set(canonical)):
        fail("E_SET_COUNT_MISMATCH", label)
    return values


def _sorted_ids(values: Iterable[str]) -> list[str]:
    return sorted(values, key=lambda item: item.encode())


def _ids(values: Iterable[dict[str, Any]], field: str) -> list[str]:
    result = [item[field] for item in values]
    if len(result) != len(set(result)):
        fail("E_SET_COUNT_MISMATCH", field)
    return _sorted_ids(result)


def _require_subset(values: Iterable[str], population: set[str], label: str) -> None:
    if not set(values) <= population:
        fail("E_EVIDENCE_DANGLING_REFERENCE", label)


def collect_typed_opaque_ids(value: object, trail: str = "") -> list[dict[str, str]]:
    """Collect every public opaque identifier together with its field type."""

    result: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            result.extend(collect_typed_opaque_ids(child, trail + "/" + key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            result.extend(collect_typed_opaque_ids(child, trail + f"/{index}"))
    elif isinstance(value, str) and OPAQUE_ID.fullmatch(value):
        result.append({"type": trail.rsplit("/", 1)[-1], "id": value})
    return result


def _descriptor_matches(claimed: dict[str, Any], actual: dict[str, Any]) -> bool:
    """Require every normative descriptor fact to equal the one reopened now."""

    if set(claimed) != set(actual) or "captured_at" not in claimed:
        return False
    if without(claimed, "captured_at") != without(actual, "captured_at"):
        return False
    try:
        return parse_time(claimed["captured_at"], "claimed captured_at") <= parse_time(
            actual["captured_at"], "actual captured_at"
        )
    except HistoryV4Error:
        return False


def validate_lineage_accounting(accounting: dict[str, Any], *, domain: str) -> None:
    counts = accounting.get("counts")
    if not isinstance(counts, dict):
        fail("E_NATIVE_LINEAGE_MISMATCH", "counts")
    for count_field, set_field in LINEAGE_COUNT_FIELDS.items():
        values = _sorted_unique(accounting.get(set_field), set_field)
        if counts.get(count_field) != len(values):
            fail("E_NATIVE_LINEAGE_MISMATCH", set_field)
    expected = D(domain, without(accounting, "counts_sha256"))
    if accounting.get("counts_sha256") != expected:
        fail("E_NATIVE_LINEAGE_MISMATCH", "counts_sha256")


def validate_ledger(ledger: dict[str, Any]) -> None:
    validate_schema(ledger)
    nodes = ledger["native_nodes"]
    by_node = {item["node_id"]: item for item in nodes}
    if len(by_node) != len(nodes):
        fail("E_NATIVE_LINEAGE_MISMATCH", "duplicate node")
    by_source_ordinal = {
        (item["source_id"], item["source_record_ordinal"]): item for item in nodes
    }
    if len(by_source_ordinal) != len(nodes):
        fail("E_LINEAGE_PARENT_CONFLICT", "duplicate source ordinal")
    for node in nodes:
        parent = node.get("parent_id")
        if parent == node["node_id"]:
            fail("E_LINEAGE_CYCLE", node["node_id"])
        if parent is not None and parent in by_node:
            parent_node = by_node[parent]
            if parent_node["platform"] != node["platform"]:
                fail("E_LINEAGE_PARENT_CONFLICT", node["node_id"])
            if node.get("parent_native_hmac") != parent_node.get("native_hmac"):
                fail("E_LINEAGE_PARENT_CONFLICT", node["node_id"])
            if parse_time(node["occurred_at"], "occurred_at") < parse_time(parent_node["occurred_at"], "parent.occurred_at"):
                fail("E_LINEAGE_CHRONOLOGY", node["node_id"])
        seen: set[str] = set()
        current = node
        while current.get("parent_id") in by_node:
            if current["node_id"] in seen:
                fail("E_LINEAGE_CYCLE", node["node_id"])
            seen.add(current["node_id"])
            current = by_node[current["parent_id"]]
        expected_root = current.get("root_id")
        if expected_root is None or node.get("root_id") != expected_root:
            fail("E_NATIVE_LINEAGE_MISMATCH", f"root closure {node['node_id']}")
    records_by_id = {item["record_id"]: item for item in ledger["records"]}
    if len(records_by_id) != len(ledger["records"]):
        fail("E_LEDGER_BINDING_MISMATCH", "duplicate record")
    for record in ledger["records"]:
        node = by_source_ordinal.get((record["source_id"], record["source_record_ordinal"]))
        if node is None or any(
            record.get(record_field) != node.get(node_field)
            for record_field, node_field in (
                ("record_id", "record_id"),
                ("root_id", "root_id"),
                ("namespace_id", "namespace_id"),
                ("project_family_id", "project_family_id"),
                ("platform", "platform"),
                ("classification", "classification"),
                ("classification_basis", "classification_basis"),
            )
        ):
            fail("E_NATIVE_LINEAGE_MISMATCH", record.get("record_id", ""))
        lineage = record["lineage"]
        if any(
            lineage.get(field) != node.get(field)
            for field in ("node_id", "parent_id", "occurred_at")
        ) or node.get("record_disposition") != "semantic":
            fail("E_NATIVE_LINEAGE_MISMATCH", record.get("record_id", ""))
        if node.get("observation_id") != record.get("observation_id"):
            fail("E_NATIVE_LINEAGE_MISMATCH", record.get("record_id", ""))
        locator = record["locator"]
        if locator["sha256"] != D("semantic-locator/v2", without(locator, "sha256")):
            fail("E_LEDGER_BINDING_MISMATCH", record.get("record_id", ""))
        if record["redacted_text_sha256"] != sha256_bytes(record["redacted_text"].encode()):
            fail("E_LEDGER_BINDING_MISMATCH", record.get("record_id", ""))
        body = without(record, "observation_id", "semantic_commitment_sha256", "ledger_record_sha256")
        commitment = D("semantic-observation/v2", body)
        if record["semantic_commitment_sha256"] != commitment or record["observation_id"] != "obs-" + commitment:
            fail("E_LEDGER_BINDING_MISMATCH", record.get("record_id", ""))
        if record["ledger_record_sha256"] != D("semantic-ledger-record/v2", without(record, "ledger_record_sha256")):
            fail("E_LEDGER_BINDING_MISMATCH", record.get("record_id", ""))
    ordered = sorted(
        deepcopy(ledger["records"]),
        key=lambda item: tuple(str(item[field]).encode() for field in ("source_id", "raw_sha256", "record_id", "field", "ordinal")),
    )
    if ledger["semantic_ledger_sha256"] != D("semantic-observation-ledger/v2", ordered):
        fail("E_SEMANTIC_LEDGER_REBUILD_REQUIRED")
    native_nodes = sorted(
        deepcopy(nodes),
        key=lambda item: tuple(str(item[field]).encode() for field in ("platform", "source_id", "source_record_ordinal", "native_type", "native_hmac", "node_id")),
    )
    if ledger["native_lineage_closure_sha256"] != D("history-native-lineage-closure/v2", native_nodes):
        fail("E_NATIVE_LINEAGE_MISMATCH", "closure")
    accounting = ledger["lineage_accounting"]
    validate_lineage_accounting(accounting, domain="history-lineage-accounting/v2")
    derived = {
        "record_ids": _sorted_ids(item["record_id"] for item in nodes),
        "semantic_record_ids": _sorted_ids(records_by_id),
        "excluded_record_ids": _sorted_ids(
            item["record_id"] for item in nodes if item["record_disposition"] == "excluded"
        ),
        "nonsemantic_record_ids": _sorted_ids(
            item["record_id"] for item in nodes if item["record_disposition"] == "non-semantic"
        ),
        "observation_ids": _sorted_ids(records["observation_id"] for records in ledger["records"]),
        "node_ids": _sorted_ids(by_node),
        "root_ids": _sorted_ids({item["root_id"] for item in nodes}),
        "child_ids": _sorted_ids(
            item["node_id"] for item in nodes if item.get("parent_id") in by_node
        ),
        "unresolved_ids": _sorted_ids(
            item["node_id"]
            for item in nodes
            if item.get("parent_id") is not None and item.get("parent_id") not in by_node
        ),
        "duplicate_export_ids": _sorted_ids(
            item["node_id"] for item in nodes if item["classification"] == "duplicate-export"
        ),
        "nonsemantic_ids": _sorted_ids(
            item["node_id"] for item in nodes if item["record_disposition"] == "non-semantic"
        ),
        "excluded_ids": _sorted_ids(
            item["node_id"] for item in nodes if item["record_disposition"] == "excluded"
        ),
        "namespace_ids": _sorted_ids({item["namespace_id"] for item in nodes}),
        "project_family_ids": _sorted_ids({item["project_family_id"] for item in nodes}),
    }
    for field, values in derived.items():
        if accounting[field] != values:
            fail("E_NATIVE_LINEAGE_MISMATCH", field)
    inventory = ledger["native_id_inventory"]
    if inventory.get("complete") is not True:
        fail("E_NATIVE_ID_INVENTORY_INCOMPLETE")
    typed_hmacs: dict[str, set[str]] = {key: set() for key in inventory["by_type"]}
    for node in nodes:
        typed_hmacs.setdefault(node["native_type"], set()).add(node["native_hmac"])
        if node.get("parent_native_hmac"):
            typed_hmacs.setdefault(node["native_type"], set()).add(node["parent_native_hmac"])
        namespace_type = "namespace" if node["platform"] == "codex" else "session"
        typed_hmacs.setdefault(namespace_type, set()).add(node["namespace_native_hmac"])
    computed_by_type = {key: len(typed_hmacs.get(key, set())) for key in inventory["by_type"]}
    all_hmacs = _sorted_ids({value for values in typed_hmacs.values() for value in values})
    if inventory["by_type"] != computed_by_type or inventory["total_count"] != len(all_hmacs):
        fail("E_NATIVE_ID_INVENTORY_INCOMPLETE")
    if inventory["native_hmac_set_sha256"] != D("history-native-hmac-set/v2", all_hmacs):
        fail("E_NATIVE_ID_INVENTORY_INCOMPLETE")


def validate_active_campaign(history: dict[str, Any], ledger: dict[str, Any]) -> None:
    campaign = history["active_campaign"]
    if campaign["disposition"] == "not-applicable":
        if campaign.get("basis") not in {
            "cutoff-predates-campaign",
            "authorized-roots-cannot-contain-campaign",
        } or not campaign.get("authority_receipt_sha256"):
            fail("E_ACTIVE_CAMPAIGN_INCOMPLETE")
        return
    nodes = ledger["native_nodes"]
    platform = campaign.get("platform")
    if platform not in {item["platform"] for item in history["sources"]}:
        fail("E_ACTIVE_CAMPAIGN_PLATFORM")
    aliases = _sorted_unique(campaign.get("alias_hmacs"), "active alias hmacs")
    namespaces = _sorted_unique(campaign.get("namespace_hmacs"), "active namespace hmacs")
    if campaign.get("root_native_hmac") in aliases or set(aliases) & set(namespaces):
        fail("E_ACTIVE_CAMPAIGN_AMBIGUOUS")
    roots = [
        item
        for item in nodes
        if item["platform"] == platform
        and item["native_hmac"] == campaign.get("root_native_hmac")
    ]
    if len(roots) != 1:
        fail("E_ACTIVE_CAMPAIGN_AMBIGUOUS")
    root = roots[0]
    started = parse_time(campaign["started_at"], "active_campaign.started_at")
    if parse_time(root["occurred_at"], "active root occurred_at") < started:
        fail("E_LINEAGE_CHRONOLOGY")
    by_parent: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        if node.get("parent_id") is not None:
            by_parent.setdefault(node["parent_id"], []).append(node)
    descendants: set[str] = set()
    frontier = [root["node_id"]]
    while frontier:
        parent = frontier.pop()
        for child in by_parent.get(parent, []):
            if child["node_id"] not in descendants:
                descendants.add(child["node_id"])
                frontier.append(child["node_id"])
    same_namespace = {
        item["node_id"]
        for item in nodes
        if item["platform"] == platform
        and item["namespace_native_hmac"] in set(namespaces)
        and parse_time(item["occurred_at"], "active namespace occurred_at") >= started
        and not item["after_cutoff"]
    }
    descendant_nodes = {
        item["node_id"]
        for item in nodes
        if item["node_id"] in descendants and not item["after_cutoff"]
    }
    descendant_only = descendant_nodes - same_namespace
    reasons: dict[str, str] = {root["record_id"]: "active_root"}
    for node in nodes:
        if node["node_id"] == root["node_id"]:
            continue
        if node["after_cutoff"]:
            reasons[node["record_id"]] = "after_cutoff"
        elif node["node_id"] in same_namespace:
            reasons[node["record_id"]] = "active_namespace"
        elif node["node_id"] in descendant_only:
            reasons[node["record_id"]] = "active_descendant"
    closure = campaign["closure"]
    expected = {
        "root_ids": [root["record_id"]],
        "descendant_ids": _sorted_ids(
            by_node["record_id"] for by_node in nodes if by_node["node_id"] in descendant_only
        ),
        "namespace_record_ids": _sorted_ids(
            by_node["record_id"]
            for by_node in nodes
            if by_node["node_id"] in same_namespace
            and by_node["node_id"] != root["node_id"]
        ),
        "excluded_record_ids": _sorted_ids(reasons),
        "reason_counts": {
            reason: sum(value == reason for value in reasons.values())
            for reason in ("active_descendant", "active_namespace", "active_root", "after_cutoff")
        },
    }
    for field, value in expected.items():
        if closure.get(field) != value:
            fail("E_ACTIVE_CAMPAIGN_INCOMPLETE", field)
    if closure["fixed_point_sha256"] != D(
        "active-campaign-fixed-point/v4", without(closure, "fixed_point_sha256")
    ):
        fail("E_ACTIVE_CAMPAIGN_INCOMPLETE", "fixed point")
    exclusion = history["exclusion_ledger"]
    if {
        item["record_id"]: item["reason"] for item in exclusion["records"]
    } != reasons or exclusion["reason_counts"] != expected["reason_counts"]:
        fail("E_ACTIVE_CAMPAIGN_INCOMPLETE", "exclusion ledger")


def validate_sources(history: dict[str, Any], ledger: dict[str, Any]) -> None:
    validate_schema(history)
    if {item["platform"] for item in history["user_roots"]} != {"codex", "claude-code"}:
        fail("E_USER_ROOT_SET_MISMATCH")
    for root in history["user_roots"]:
        if root["selection_basis"] not in {"authenticated-user-home-default", "host-resolved-environment"}:
            fail("E_USER_ROOT_AUTHORITY")
    roots_by_id = {item["root_id"]: item for item in history["user_roots"]}
    if len(roots_by_id) != len(history["user_roots"]):
        fail("E_USER_ROOT_SET_MISMATCH")
    for source in history["sources"]:
        root = roots_by_id.get(source["user_root_id"])
        if root is None or root["platform"] != source["platform"]:
            fail("E_USER_ROOT_AUTHORITY")
    for adapter in history["adapter_catalog"]["adapters"]:
        if adapter["envelope_catalog_sha256"] != D("history-envelope-catalog/v2", adapter["envelope_catalog"]):
            fail("E_ADAPTER_IMPLEMENTATION_DRIFT")
        if adapter["native_id_catalog_sha256"] != D("history-native-id-catalog/v2", adapter["native_id_catalog"]):
            fail("E_ADAPTER_IMPLEMENTATION_DRIFT")
        if adapter["entry_sha256"] != D("history-adapter-entry/v2", without(adapter, "entry_sha256")):
            fail("E_ADAPTER_IMPLEMENTATION_DRIFT")
    if history["adapter_catalog"]["catalog_sha256"] != D(
        "history-adapter-catalog/v2", without(history["adapter_catalog"], "catalog_sha256")
    ):
        fail("E_ADAPTER_IMPLEMENTATION_DRIFT")
    accounting = history["source_accounting"]
    if accounting["source_ids"] != sorted((item["source_id"] for item in history["sources"]), key=lambda item: item.encode()):
        fail("E_SOURCE_ACCOUNTING_MISMATCH")
    expected_counts = {
        "source_count": len(history["sources"]),
        "parsed_record_count": sum(item["parsed_record_count"] for item in history["sources"]),
        "semantic_record_count": sum(item["semantic_record_count"] for item in history["sources"]),
        "nonsemantic_record_count": sum(item["nonsemantic_record_count"] for item in history["sources"]),
        "excluded_record_count": sum(item["excluded_record_count"] for item in history["sources"]),
    }
    if any(accounting.get(key) != value for key, value in expected_counts.items()):
        fail("E_SOURCE_ACCOUNTING_MISMATCH")
    if accounting["parsed_record_count"] != accounting["semantic_record_count"] + accounting["nonsemantic_record_count"] + accounting["excluded_record_count"]:
        fail("E_SOURCE_ACCOUNTING_MISMATCH")
    if accounting["source_accounting_sha256"] != D(
        "history-source-accounting/v4", without(accounting, "source_accounting_sha256")
    ):
        fail("E_SOURCE_ACCOUNTING_MISMATCH")
    ordered_sources = sorted(
        deepcopy(history["sources"]),
        key=lambda item: (item["source_id"].encode(), item["relative_path_sha256"].encode()),
    )
    raw = history["raw_manifest"]
    if raw["count"] != len(ordered_sources) or raw["sha256"] != D(
        "raw-source-manifest/v2", ordered_sources
    ):
        fail("E_RAW_SNAPSHOT_REBUILD_REQUIRED")
    exclusion = history["exclusion_ledger"]
    ordered_exclusions = sorted(
        deepcopy(exclusion["records"]),
        key=lambda item: (item["record_id"].encode(), item["reason"].encode()),
    )
    expected_reasons = {
        reason: sum(item["reason"] == reason for item in ordered_exclusions)
        for reason in ("active_descendant", "active_namespace", "active_root", "after_cutoff")
    }
    if (
        exclusion["count"] != len(ordered_exclusions)
        or exclusion["reason_counts"] != expected_reasons
        or exclusion["sha256"] != D("history-exclusion-ledger/v2", ordered_exclusions)
    ):
        fail("E_SOURCE_ACCOUNTING_MISMATCH", "exclusion ledger")
    lineage = ledger["lineage_accounting"]
    if accounting["source_ids"] != lineage["source_ids"]:
        fail("E_LINEAGE_SET_MISMATCH", "source_ids")
    if accounting["semantic_record_count"] != len(lineage["semantic_record_ids"]):
        fail("E_SOURCE_ACCOUNTING_MISMATCH", "semantic records")
    if accounting["excluded_record_count"] != len(lineage["excluded_record_ids"]):
        fail("E_SOURCE_ACCOUNTING_MISMATCH", "excluded records")
    if accounting["nonsemantic_record_count"] != len(lineage["nonsemantic_record_ids"]):
        fail("E_SOURCE_ACCOUNTING_MISMATCH", "nonsemantic records")
    if history["semantic_ledger"]["sha256"] != ledger["semantic_ledger_sha256"]:
        fail("E_SEMANTIC_LEDGER_REBUILD_REQUIRED")
    if history["semantic_ledger"]["native_lineage_closure_sha256"] != ledger["native_lineage_closure_sha256"]:
        fail("E_NATIVE_LINEAGE_MISMATCH")
    if history["semantic_ledger"]["count"] != len(ledger["records"]):
        fail("E_SEMANTIC_LEDGER_REBUILD_REQUIRED")
    corpus_body = {
        "history_contract_id": history["contract_id"],
        "raw_source_manifest_sha256": raw["sha256"],
        "semantic_ledger_sha256": ledger["semantic_ledger_sha256"],
        "native_lineage_closure_sha256": ledger["native_lineage_closure_sha256"],
        "exclusion_ledger_sha256": exclusion["sha256"],
        "semantic_commitments": _sorted_ids(
            item["semantic_commitment_sha256"] for item in ledger["records"]
        ),
        "root_ids": _sorted_ids({item["root_id"] for item in ledger["records"]}),
        "project_family_ids": _sorted_ids(
            {item["project_family_id"] for item in ledger["records"]}
        ),
    }
    corpus = history["corpus"]
    if (
        corpus["sha256"] != D("history-corpus/v4", corpus_body)
        or corpus["observation_count"] != len(ledger["records"])
        or corpus["root_count"] != len(corpus_body["root_ids"])
        or corpus["project_family_count"] != len(corpus_body["project_family_ids"])
    ):
        fail("E_HISTORY_BINDING_REQUIRED", "corpus")
    validate_active_campaign(history, ledger)


def verify_adapter_implementations(
    history: dict[str, Any],
    acquired: dict[str, tuple[dict[str, Any], bytes]],
) -> None:
    """Bind each catalog entry to the independently acquired parser bytes."""

    expected_ids = {item["adapter_id"] for item in history["adapter_catalog"]["adapters"]}
    if set(acquired) != expected_ids:
        fail("E_ADAPTER_IMPLEMENTATION_DRIFT", "adapter set")
    for adapter in history["adapter_catalog"]["adapters"]:
        descriptor, payload = acquired[adapter["adapter_id"]]
        if not _descriptor_matches(adapter["implementation"], descriptor):
            fail("E_ADAPTER_IMPLEMENTATION_DRIFT", adapter["adapter_id"])
        expected_sha256 = adapter.get(
            "implementation_sha256", adapter["implementation"].get("sha256")
        )
        if expected_sha256 != sha256_bytes(payload):
            fail("E_ADAPTER_IMPLEMENTATION_DRIFT", adapter["adapter_id"])


def validate_index(index: dict[str, Any], history: dict[str, Any], ledger: dict[str, Any]) -> None:
    validate_schema(index)
    if index["history_contract_sha256"] != D("history-sources/v4", history):
        fail("E_HISTORY_BINDING_REQUIRED")
    if index["history_index_sha256"] != D("history-index/v4", without(index, "history_index_sha256")):
        fail("E_HISTORY_INDEX_REBUILD_REQUIRED")
    members = index["exact_file_set"]["members"]
    ordered = sorted(deepcopy(members), key=lambda item: ((item.get("relative_path") or "").encode(), item["target_id"].encode()))
    if index["exact_file_set"]["member_count"] != len(members) or index["exact_file_set"]["members_sha256"] != D("exact-file-set/v2", ordered):
        fail("E_PRIVATE_FILE_SET_MISMATCH")
    lifecycle = index["lifecycle"]
    state = lifecycle["state"]
    file_state = index["exact_file_set"]["state"]
    roles = [item["role"] for item in members]
    if len(roles) != len(set(roles)):
        fail("E_PRIVATE_FILE_SET_MISMATCH", "duplicate role")
    if state == "deleted":
        if file_state != "tombstone" or any(item["relative_path"] is not None for item in members):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "deleted tombstone")
    else:
        actual = {item["relative_path"]: item["role"] for item in members}
        if len(actual) != len(members):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "duplicate path")
        for path, role in REQUIRED_PRIVATE_MEMBERS.items():
            if actual.get(path) != role:
                fail("E_PRIVATE_FILE_SET_MISMATCH", path)
        if any(
            path not in REQUIRED_PRIVATE_MEMBERS and role != "declared-private-copy"
            for path, role in actual.items()
        ):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "undeclared private copy")
        if file_state != "live" or any(
            item["mode"] != "0600" or item["nlink"] != 1 for item in members
        ):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "live file topology")
    transitions = lifecycle["transitions"]
    if not transitions or transitions[0]["from"] != "collecting":
        fail("E_LIFECYCLE_TRANSITION")
    if any(
        (item["from"], item["to"]) not in LIFECYCLE_TRANSITIONS for item in transitions
    ) or any(left["to"] != right["from"] for left, right in zip(transitions, transitions[1:])):
        fail("E_LIFECYCLE_TRANSITION")
    if transitions[-1]["to"] != state:
        fail("E_LIFECYCLE_TRANSITION", "terminal state")
    target_by_id = {item["target_id"]: item for item in lifecycle["deletion_targets"]}
    member_by_id = {item["target_id"]: item for item in members}
    if len(target_by_id) != len(lifecycle["deletion_targets"]) or set(target_by_id) != set(member_by_id):
        fail("E_PRIVATE_FILE_SET_MISMATCH", "deletion target set")
    for target_id, member in member_by_id.items():
        target = target_by_id[target_id]
        if target["role"] != member["role"] or target["hash_kind"] != member["hash_kind"] or target["member_sha256"] != member["content_sha256"]:
            fail("E_PRIVATE_FILE_SET_MISMATCH", target_id)
        if state != "deleted" and target["relative_path_sha256"] != sha256_bytes(member["relative_path"].encode()):
            fail("E_PRIVATE_FILE_SET_MISMATCH", target_id)
    receipt = lifecycle["deletion_receipt"]
    if state == "deleted":
        if not isinstance(receipt, dict):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "missing deletion receipt")
        target_ids = set(target_by_id)
        if (
            set(receipt["target_ids"]) != target_ids
            or set(receipt["post_delete_absent_target_ids"]) != target_ids
            or {item["target_id"] for item in receipt["attempts"]} != target_ids
            or {item["target_id"] for item in receipt["targets"]} != target_ids
            or any(item["result"] != "absent" for item in receipt["attempts"])
        ):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "deletion proof")
        if receipt["transitions"] != transitions:
            fail("E_LIFECYCLE_TRANSITION", "receipt transitions")
        if receipt["post_delete_absence_sha256"] != D(
            "history-private-absence/v2", _sorted_ids(target_ids)
        ):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "absence commitment")
        if set(receipt["identity_material_target_ids"]) != set(
            receipt["destroyed_identity_material_target_ids"]
        ):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "identity destruction")
        if receipt["receipt_sha256"] != D(
            "history-private-deletion-receipt/v2", without(receipt, "receipt_sha256")
        ):
            fail("E_PRIVATE_FILE_SET_MISMATCH", "deletion receipt commitment")
    elif receipt is not None:
        fail("E_PRIVATE_FILE_SET_MISMATCH", "live deletion receipt")
    if state in {"expired", "deletion-pending"}:
        fail("E_LEDGER_EXPIRED", state)
    if state in {"live", "validation-complete"} and parse_time(
        lifecycle["delete_by"], "delete_by"
    ) <= dt.datetime.now(dt.timezone.utc):
        fail("E_LEDGER_EXPIRED")
    if lifecycle["retention_disposition"] == "delete-after-validation" and state == "validation-complete":
        fail("E_LEDGER_EXPIRED", "delete-after-validation requires deletion-pending")
    validate_lineage_accounting(index["lineage"], domain="history-index-lineage-accounting/v4")
    for field in LINEAGE_COUNT_FIELDS.values():
        if index["lineage"][field] != ledger["lineage_accounting"][field]:
            fail("E_LINEAGE_SET_MISMATCH", field)


def verify_model_resolution(
    reduction: dict[str, Any],
    *,
    detached: dict[str, bytes],
    detached_descriptors: dict[str, dict[str, Any]],
    authority: dict[str, tuple[dict[str, Any], bytes]],
    trusted_provider_root_authority_sha256: str,
    trusted_trust_root_receipt_sha256: str,
) -> None:
    """Verify exact model authority from independently pinned reopened inputs."""

    if not re.fullmatch(r"[0-9a-f]{64}", trusted_provider_root_authority_sha256) or not re.fullmatch(
        r"[0-9a-f]{64}", trusted_trust_root_receipt_sha256
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "missing independent trust pins")
    required_authority = {
        "provider-trust-root-receipt",
        "provider-verification-key",
        "provider-verifier",
        "nonce-state-before",
        "nonce-state-after",
    }
    if set(authority) != required_authority:
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "authority artifact set")
    model = reduction["model_resolution"]
    if model["display_name"] != "5.6 lunar high":
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    runtime = load_document(detached["runtime-model-catalog"], "runtime-model-catalog")
    receipt = load_document(detached["callable-verification-receipt"], "callable-verification-receipt")
    trust = load_document(detached["provider-trust-catalog"], "provider-trust-catalog")
    if without(model["runtime_catalog"], "descriptor") != runtime:
        fail("E_RUNTIME_CATALOG_MISMATCH")
    if without(model["callable_verification"], "descriptor") != receipt:
        fail("E_CALLABLE_VERIFICATION_MISMATCH")
    if without(model["provider_trust"], "descriptor") != trust:
        fail("E_CALLABLE_VERIFICATION_MISMATCH")
    bindings = {
        "runtime-model-catalog": model["runtime_catalog"]["descriptor"],
        "provider-trust-catalog": model["provider_trust"]["descriptor"],
        "callable-verification-receipt": model["callable_verification"]["descriptor"],
    }
    if any(not _descriptor_matches(bindings[role], detached_descriptors.get(role, {})) for role in bindings):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "detached descriptors")
    trust_descriptor, trust_bytes = authority["provider-trust-root-receipt"]
    key_descriptor, provider_key = authority["provider-verification-key"]
    verifier_descriptor, verifier_bytes = authority["provider-verifier"]
    before_descriptor, before_bytes = authority["nonce-state-before"]
    after_descriptor, after_bytes = authority["nonce-state-after"]
    for descriptor in (
        trust_descriptor,
        key_descriptor,
        verifier_descriptor,
        before_descriptor,
        after_descriptor,
    ):
        if descriptor["root_authority_sha256"] != trusted_provider_root_authority_sha256:
            fail("E_CALLABLE_VERIFICATION_MISMATCH", "authority root")
    if sha256_bytes(trust_bytes) != trusted_trust_root_receipt_sha256:
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "trust-root pin")
    trust_root = load_document(trust_bytes, "provider-trust-root-receipt")
    if trust_root.get("receipt_sha256") != D(
        "provider-trust-root-receipt/v1", without(trust_root, "receipt_sha256")
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "trust-root receipt")
    if (
        trust_root.get("root_authority_sha256") != trusted_provider_root_authority_sha256
        or trust_root.get("provider_key_sha256") != sha256_bytes(provider_key)
        or trust_root.get("verifier_sha256") != sha256_bytes(verifier_bytes)
        or len(provider_key) != 32
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "trust-root bindings")
    authority_receipt = model["authority_validation"]
    authority_bindings = {
        "trust_root_receipt": trust_descriptor,
        "provider_key": key_descriptor,
        "verifier": verifier_descriptor,
        "nonce_state": after_descriptor,
    }
    if any(not _descriptor_matches(authority_receipt[field], value) for field, value in authority_bindings.items()):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "authority descriptors")
    if any(
        authority_receipt[field] != value
        for field, value in {
            "trust_root_receipt_sha256": sha256_bytes(trust_bytes),
            "provider_key_sha256": sha256_bytes(provider_key),
            "verifier_sha256": sha256_bytes(verifier_bytes),
            "nonce_state_before_sha256": sha256_bytes(before_bytes),
            "nonce_state_after_sha256": sha256_bytes(after_bytes),
        }.items()
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "authority byte bindings")
    if authority_receipt["receipt_sha256"] != D(
        "callable-authority-validation/v1", without(authority_receipt, "receipt_sha256")
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "authority receipt")
    nonce_state_before = load_document(before_bytes, "nonce-state-before")
    nonce_state_after = load_document(after_bytes, "nonce-state-after")
    for state in (nonce_state_before, nonce_state_after):
        if state.get("state_sha256") != D("model-nonce-state/v1", without(state, "state_sha256")):
            fail("E_CALLABLE_VERIFICATION_MISMATCH", "nonce state commitment")
        for field in ("used_challenge_nonce_sha256s", "used_receipt_replay_key_sha256s"):
            _sorted_unique(state[field], field)
    if (
        nonce_state_before["registry_id"] != nonce_state_after["registry_id"]
        or nonce_state_after["generation"] != nonce_state_before["generation"] + 1
        or nonce_state_before["used_challenge_nonce_sha256s"] != authority_receipt["used_nonce_sha256s"]
        or nonce_state_before["used_receipt_replay_key_sha256s"] != authority_receipt["used_receipt_sha256s"]
        or authority_receipt["used_nonce_count"] != len(authority_receipt["used_nonce_sha256s"])
        or authority_receipt["used_receipt_count"] != len(authority_receipt["used_receipt_sha256s"])
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "nonce state before")
    ordinal = model["selected_entry_ordinal"]
    entries = runtime.get("entries", [])
    exact_entries = [item for item in entries if item.get("display_name") == "5.6 lunar high"]
    if not isinstance(ordinal, int) or ordinal < 1 or ordinal > len(entries) or len(exact_entries) != 1:
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    selected = entries[ordinal - 1]
    if selected.get("status") != "callable" or any(model.get(field) != selected.get(field) for field in ("display_name", "callable_id", "provider")):
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    if selected.get("supported_settings_sha256") != model.get("settings_sha256"):
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    if (
        model.get("selected_entry_sha256") != selected.get("entry_sha256")
        or receipt.get("selected_entry_sha256") != selected.get("entry_sha256")
        or receipt.get("catalog_sha256") != model["runtime_catalog"]["descriptor"]["sha256"]
        or any(receipt.get(field) != model.get(field) for field in ("display_name", "callable_id", "provider", "settings_sha256"))
    ):
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    if selected.get("entry_sha256") != D("runtime-model-entry/v2", without(selected, "entry_sha256")):
        fail("E_RUNTIME_CATALOG_MISMATCH")
    if runtime.get("catalog_sha256") != D(
        "runtime-model-catalog/v2", without(runtime, "catalog_sha256", "descriptor")
    ):
        fail("E_RUNTIME_CATALOG_MISMATCH")
    if trust.get("catalog_sha256") != D(
        "provider-verifier-trust/v1", without(trust, "catalog_sha256", "descriptor")
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH")
    for entry in trust.get("entries", []):
        if entry.get("entry_sha256") != D("provider-verifier-entry/v1", without(entry, "entry_sha256")):
            fail("E_CALLABLE_VERIFICATION_MISMATCH")
    trusted_entries = [
        entry
        for entry in trust.get("entries", [])
        if entry.get("entry_sha256") == receipt.get("verifier_entry_sha256")
    ]
    if len(trusted_entries) != 1:
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "verifier entry")
    trusted_entry = trusted_entries[0]
    if (
        trusted_entry.get("provider") != model.get("provider")
        or trusted_entry.get("verification_algorithm") != "hmac-sha256/v1"
        or not _descriptor_matches(trusted_entry.get("verification_key", {}), key_descriptor)
        or not _descriptor_matches(trusted_entry.get("verifier", {}), verifier_descriptor)
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "trusted verifier")
    request = parse_time(receipt.get("requested_at"), "requested_at")
    captured = parse_time(receipt.get("captured_at"), "captured_at")
    resolved = parse_time(model.get("resolved_at"), "resolved_at")
    expires = parse_time(receipt.get("expires_at"), "expires_at")
    if not (request <= captured <= resolved < expires) or (expires - request).total_seconds() > 900:
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    validated = parse_time(authority_receipt.get("validated_at"), "validated_at")
    if not (captured <= validated <= expires) or authority_receipt.get("max_age_seconds") != 900:
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    if not (
        parse_time(trust_root.get("issued_at"), "trust_root.issued_at")
        <= validated
        < parse_time(trust_root.get("expires_at"), "trust_root.expires_at")
    ):
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    nonce = receipt.get("challenge_nonce_sha256")
    replay_key = receipt.get("response_sha256")
    if nonce in nonce_state_before.get("used_challenge_nonce_sha256s", []) or replay_key in nonce_state_before.get("used_receipt_replay_key_sha256s", []):
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    if nonce_state_after["used_challenge_nonce_sha256s"] != _sorted_ids(
        [*nonce_state_before["used_challenge_nonce_sha256s"], nonce]
    ) or nonce_state_after["used_receipt_replay_key_sha256s"] != _sorted_ids(
        [*nonce_state_before["used_receipt_replay_key_sha256s"], replay_key]
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "nonce atomic append")
    challenge_body = {
        field: receipt[field]
        for field in (
            "catalog_sha256",
            "selected_entry_sha256",
            "display_name",
            "callable_id",
            "provider",
            "settings_sha256",
            "verification_protocol",
            "verifier_entry_sha256",
            "authority_validation_receipt_sha256",
            "challenge_nonce_sha256",
            "request_sha256",
            "response_sha256",
            "command_status",
            "verifier_version",
            "requested_at",
            "captured_at",
            "expires_at",
            "callable",
        )
    }
    if (
        receipt.get("authority_validation_receipt_sha256") != authority_receipt["receipt_sha256"]
        or receipt.get("challenge_message_sha256") != D(
            "provider-authenticated-challenge/v1", challenge_body
        )
        or receipt.get("receipt_sha256") != D(
            "callable-verification/v2", without(receipt, "receipt_sha256", "descriptor")
        )
        or receipt.get("callable") is not True
        or receipt.get("command_status") != 0
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "callable receipt")
    challenge = bytes.fromhex(receipt["challenge_message_sha256"])
    expected_mac = hmac.new(provider_key, challenge, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_mac, receipt.get("provider_mac_hex", "")):
        fail("E_EXPLORATION_MODEL_UNAVAILABLE")
    if model.get("resolution_sha256") != D(
        "exploration-model-resolution/v2", without(model, "resolution_sha256")
    ):
        fail("E_CALLABLE_VERIFICATION_MISMATCH", "model resolution")


def _walk_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def validate_reduction(reduction: dict[str, Any], index: dict[str, Any], ledger: dict[str, Any]) -> None:
    validate_schema(reduction)
    binding = reduction["history_binding"]
    if binding["history_index_sha256"] != index["history_index_sha256"] or binding["semantic_ledger_sha256"] != ledger["semantic_ledger_sha256"]:
        fail("E_HISTORY_BINDING_REQUIRED")
    if (
        binding["ledger_state"] != "live"
        or ledger["lifecycle_state"] != "live"
        or index["lifecycle"]["state"] != "live"
        or reduction["hydration"]["ledger_state"] != "live"
    ):
        fail("E_LEDGER_EXPIRED")
    expected_binding = {
        "history_contract_id": index["history_contract_id"],
        "history_contract_sha256": index["history_contract_sha256"],
        "index_id": index["index_id"],
        "history_index_sha256": index["history_index_sha256"],
        "raw_manifest_sha256": index["bindings"]["raw_source_manifest_sha256"],
        "semantic_ledger_sha256": ledger["semantic_ledger_sha256"],
        "native_lineage_closure_sha256": ledger["native_lineage_closure_sha256"],
        "exclusion_ledger_sha256": index["bindings"]["exclusion_ledger_sha256"],
        "corpus_sha256": index["bindings"]["corpus_sha256"],
        "ledger_state": "live",
        "delete_by": index["lifecycle"]["delete_by"],
    }
    if any(binding.get(field) != value for field, value in expected_binding.items()):
        fail("E_HISTORY_BINDING_REQUIRED", "reduction binding")
    if binding["binding_sha256"] != D(
        "capability-history-binding/v3", without(binding, "binding_sha256")
    ):
        fail("E_HISTORY_BINDING_REQUIRED", "binding commitment")
    if reduction["reduction_sha256"] != D("capability-reduction/v3", without(reduction, "reduction_sha256")):
        fail("E_CAPABILITY_REDUCTION_VERSION_UNSUPPORTED")
    decisions = reduction["decisions"]
    candidate_ids = sorted(item["candidate_id"] for item in reduction["candidates"])
    if sorted(item["candidate_id"] for item in decisions) != candidate_ids or len({item["decision_id"] for item in decisions}) != len(decisions):
        fail("E_DECISION_SET_MISMATCH")
    catalog = set(reduction["capability_catalog"]["skill_ids"])
    for decision in decisions:
        if (decision["disposition"] == "extend") != (decision["target_skill_id"] is not None):
            fail("E_EXTENSION_TARGET_UNKNOWN")
        if decision["disposition"] == "extend" and decision["target_skill_id"] not in catalog:
            fail("E_EXTENSION_TARGET_UNKNOWN")
        if decision["decision_sha256"] != D(
            "capability-decision/v3", without(decision, "decision_sha256")
        ):
            fail("E_DECISION_SET_MISMATCH", decision["decision_id"])
    schedule = reduction["schedule"]
    if schedule["snapshot_sha256"] != D(
        "capability-schedule/v3", without(schedule, "snapshot_sha256")
    ):
        fail("E_LEDGER_BINDING_MISMATCH", "schedule")
    for packet in reduction["packets"]:
        if packet["input_sha256"] != D("capability-packet/v3", without(packet, "input_sha256")):
            fail("E_LEDGER_BINDING_MISMATCH", packet["packet_id"])
    for result in reduction["results"]:
        if result["output_sha256"] != D("capability-result/v3", without(result, "output_sha256")):
            fail("E_LEDGER_BINDING_MISMATCH", result["result_id"])
    hydration = reduction["hydration"]
    if hydration["output_sha256"] != D(
        "capability-hydration/v3", without(hydration, "output_sha256", "receipt_sha256")
    ) or hydration["receipt_sha256"] != D(
        "capability-hydration-receipt/v3", without(hydration, "receipt_sha256")
    ):
        fail("E_LEDGER_BINDING_MISMATCH", "hydration")
    synthesis = reduction["synthesis"]
    accepted = set(synthesis["accepted_result_ids"])
    expected_input = {
        "accepted_result_ids": synthesis["accepted_result_ids"],
        "accepted_results": [
            {
                "result_id": item["result_id"],
                "output_sha256": item["output_sha256"],
                "provider_receipt_sha256": item["provider_receipt_sha256"],
            }
            for item in reduction["results"]
            if item["result_id"] in accepted
        ],
        "hydration_output_sha256": hydration["output_sha256"],
        "hydration_receipt_sha256": hydration["receipt_sha256"],
    }
    if synthesis["input_sha256"] != D("capability-primary-input/v3", expected_input) or synthesis[
        "output_sha256"
    ] != D("capability-synthesis/v3", without(synthesis, "output_sha256")):
        fail("E_LEDGER_BINDING_MISMATCH", "synthesis")


def validate_evidence(
    evidence: dict[str, Any],
    reduction: dict[str, Any],
    index: dict[str, Any],
    ledger: dict[str, Any],
    history: dict[str, Any] | None = None,
) -> None:
    validate_schema(evidence)
    if evidence["authoritative"] is not True:
        fail("E_RAW_REOPEN_REQUIRED")
    if evidence["evidence_sha256"] != D("history-evidence/v1", without(evidence, "evidence_sha256")):
        fail("E_HISTORY_EVIDENCE_VERSION_UNSUPPORTED")
    bindings = evidence["bindings"]
    expected_bindings = {
        "index_id": index["index_id"],
        "history_contract_id": index["history_contract_id"],
        "history_contract_sha256": index["history_contract_sha256"],
        "history_index_sha256": index["history_index_sha256"],
        "raw_manifest_sha256": index["bindings"]["raw_source_manifest_sha256"],
        "semantic_ledger_sha256": ledger["semantic_ledger_sha256"],
        "native_lineage_closure_sha256": ledger["native_lineage_closure_sha256"],
        "exclusion_ledger_sha256": index["bindings"]["exclusion_ledger_sha256"],
        "corpus_sha256": index["bindings"]["corpus_sha256"],
    }
    if any(bindings.get(field) != value for field, value in expected_bindings.items()):
        fail("E_HISTORY_BINDING_REQUIRED")
    raw_receipt = bindings["raw_reopen_receipt"]
    if raw_receipt["receipt_sha256"] != D(
        "raw-reopen-receipt/v2", without(raw_receipt, "receipt_sha256", "descriptor")
    ) or bindings["raw_reopen_receipt_sha256"] != raw_receipt["receipt_sha256"]:
        fail("E_RAW_REOPEN_REQUIRED")
    input_set = bindings["exact_input_file_set"]
    ordered_inputs = sorted(
        deepcopy(input_set["members"]),
        key=lambda item: item["relative_path_sha256"].encode(),
    )
    if (
        input_set["member_count"] != len(ordered_inputs)
        or input_set["members_sha256"] != D("history-evidence-input-set/v1", ordered_inputs)
        or bindings["exact_input_file_set_sha256"] != input_set["members_sha256"]
    ):
        fail("E_EVIDENCE_INPUT_SET_MISMATCH")
    source_accounting = evidence["source_accounting"]
    if source_accounting["source_accounting_sha256"] != D(
        "history-evidence-source-accounting/v1",
        without(source_accounting, "source_accounting_sha256"),
    ):
        fail("E_LINEAGE_SET_MISMATCH", "source accounting commitment")
    counts = evidence["counts"]
    owners = {
        "sources": (evidence["source_accounting"], "source_ids"),
        "included_records": (evidence["source_accounting"], "included_record_ids"),
        "excluded_records": (evidence["source_accounting"], "excluded_record_ids"),
        "nonsemantic_records": (evidence["source_accounting"], "nonsemantic_record_ids"),
        "observations": (evidence["source_accounting"], "observation_ids"),
        "scope_roots": (evidence["lineage"], "scope_root_ids"),
        "lineage_nodes": (evidence["lineage"], "node_ids"),
        "roots": (evidence["lineage"], "root_ids"),
        "children": (evidence["lineage"], "child_ids"),
        "unresolved": (evidence["lineage"], "unresolved_ids"),
        "excluded": (evidence["lineage"], "excluded_ids"),
        "duplicate_exports": (evidence["lineage"], "duplicate_export_ids"),
        "namespaces": (evidence["lineage"], "namespace_ids"),
        "project_families": (evidence["lineage"], "project_family_ids"),
        "edges": (evidence["lineage"], "edges"),
        **{field: (evidence, field) for field in ("claims", "artifacts", "conflicts", "states", "capabilities", "overlaps", "candidates", "decisions")},
    }
    for count, (owner, field) in owners.items():
        values = owner.get(field, [])
        if counts.get(count) != len(values) or len(values) != len(
            {canonical_bytes(item) for item in values}
        ):
            fail("E_LINEAGE_SET_MISMATCH", count)
    partition = [
        set(source_accounting[field])
        for field in ("included_record_ids", "excluded_record_ids", "nonsemantic_record_ids")
    ]
    if any(left & right for index_, left in enumerate(partition) for right in partition[index_ + 1 :]) or set().union(*partition) != set(index["lineage"]["record_ids"]):
        fail("E_LINEAGE_SET_MISMATCH", "record partition")
    if source_accounting["source_ids"] != index["lineage"]["source_ids"] or source_accounting[
        "observation_ids"
    ] != ledger["lineage_accounting"]["observation_ids"]:
        fail("E_LINEAGE_SET_MISMATCH", "source or observation closure")
    if history is not None and source_accounting["exclusion_reason_counts"] != history[
        "exclusion_ledger"
    ]["reason_counts"]:
        fail("E_LINEAGE_SET_MISMATCH", "exclusion reasons")
    lineage_projection = {
        "node_ids": "node_ids",
        "root_ids": "root_ids",
        "child_ids": "child_ids",
        "unresolved_ids": "unresolved_ids",
        "excluded_ids": "excluded_ids",
        "duplicate_export_ids": "duplicate_export_ids",
        "namespace_ids": "namespace_ids",
        "project_family_ids": "project_family_ids",
    }
    for evidence_field, index_field in lineage_projection.items():
        if evidence["lineage"][evidence_field] != index["lineage"][index_field]:
            fail("E_LINEAGE_SET_MISMATCH", evidence_field)
    _require_subset(evidence["lineage"]["scope_root_ids"], set(index["lineage"]["root_ids"]), "scope roots")
    populations = {
        "observation": set(source_accounting["observation_ids"]),
        "root": set(evidence["lineage"]["root_ids"]),
        "project": set(evidence["lineage"]["project_family_ids"]),
        "node": set(evidence["lineage"]["node_ids"]),
        "claim": set(_ids(evidence["claims"], "claim_id")),
        "artifact": set(_ids(evidence["artifacts"], "artifact_id")),
        "conflict": set(_ids(evidence["conflicts"], "conflict_id")),
        "state": set(_ids(evidence["states"], "state_id")),
        "capability": set(_ids(evidence["capabilities"], "capability_id")),
        "overlap": set(_ids(evidence["overlaps"], "overlap_id")),
        "candidate": set(_ids(evidence["candidates"], "candidate_id")),
        "decision": set(_ids(evidence["decisions"], "decision_id")),
        "catalog_skill": set(
            reduction["capability_catalog"]["skill_ids"]
            if evidence["mode"] == "capability"
            else []
        ),
    }
    for recurrence in evidence["recurrence"]:
        if recurrence["root_count"] != len(recurrence["root_ids"]) or recurrence[
            "project_family_count"
        ] != len(recurrence["project_family_ids"]):
            fail("E_RECURRENCE_SET_COUNT_MISMATCH")
        _require_subset(recurrence["observation_ids"], populations["observation"], "recurrence observations")
        _require_subset(recurrence["root_ids"], populations["root"], "recurrence roots")
        _require_subset(recurrence["project_family_ids"], populations["project"], "recurrence projects")
        if recurrence["candidate_id"] not in populations["candidate"]:
            fail("E_EVIDENCE_DANGLING_REFERENCE", "recurrence candidate")
    for claim in evidence["claims"]:
        _require_subset(claim["observation_ids"], populations["observation"], "claim observations")
        _require_subset(claim["artifact_ids"], populations["artifact"], "claim artifacts")
        _require_subset(claim["conflict_ids"], populations["conflict"], "claim conflicts")
        _require_subset(claim["state_ids"], populations["state"], "claim states")
    for artifact in evidence["artifacts"]:
        _require_subset(artifact["observation_ids"], populations["observation"], "artifact observations")
        if artifact["state_id"] not in populations["state"]:
            fail("E_EVIDENCE_DANGLING_REFERENCE", "artifact state")
    for state in evidence["states"]:
        _require_subset(state["observation_ids"], populations["observation"], "state observations")
    for capability in evidence["capabilities"]:
        _require_subset(capability["observation_ids"], populations["observation"], "capability observations")
        _require_subset(capability["candidate_ids"], populations["candidate"], "capability candidates")
        _require_subset(capability["catalog_skill_ids"], populations["catalog_skill"], "capability catalog")
    for overlap in evidence["overlaps"]:
        _require_subset(overlap["observation_ids"], populations["observation"], "overlap observations")
        if overlap["left_capability_id"] not in populations["capability"] or overlap[
            "right_capability_id"
        ] not in populations["capability"]:
            fail("E_EVIDENCE_DANGLING_REFERENCE", "overlap capabilities")
    for candidate in evidence["candidates"]:
        _require_subset(candidate["observation_ids"], populations["observation"], "candidate observations")
        _require_subset(candidate["root_ids"], populations["root"], "candidate roots")
        _require_subset(candidate["project_family_ids"], populations["project"], "candidate projects")
        _require_subset(candidate["capability_ids"], populations["capability"], "candidate capabilities")
        _require_subset(candidate["overlap_ids"], populations["overlap"], "candidate overlaps")
    if evidence["mode"] == "lineage":
        if any(evidence[field] for field in ("recurrence", "capabilities", "overlaps", "candidates", "decisions")) or bindings.get("reduction_id") is not None or bindings.get("reduction_sha256") is not None:
            fail("E_DECISION_SET_MISMATCH", "lineage mode")
    else:
        if bindings.get("reduction_id") != reduction["reduction_id"] or bindings.get(
            "reduction_sha256"
        ) != reduction["reduction_sha256"]:
            fail("E_HISTORY_BINDING_REQUIRED", "reduction")
        reduction_decisions = {item["decision_id"]: item for item in reduction["decisions"]}
        if set(reduction_decisions) != populations["decision"] or {
            item["candidate_id"] for item in evidence["decisions"]
        } != populations["candidate"]:
            fail("E_DECISION_SET_MISMATCH")
        closure_ids = {
            "claim_ids": _sorted_ids(populations["claim"]),
            "capability_ids": _sorted_ids(populations["capability"]),
            "overlap_ids": _sorted_ids(populations["overlap"]),
        }
        for decision in evidence["decisions"]:
            source = reduction_decisions.get(decision["decision_id"])
            if source is None or any(
                decision[field] != source[field]
                for field in (
                    "candidate_id",
                    "disposition",
                    "target_skill_id",
                    "evidence_observation_ids",
                )
            ) or decision["reduction_decision_sha256"] != source["decision_sha256"]:
                fail("E_DECISION_SET_MISMATCH")
            if any(decision[field] != values for field, values in closure_ids.items()):
                fail("E_DECISION_SET_MISMATCH", "decision closure")
            if decision["evidence_decision_sha256"] != D(
                "history-evidence-decision/v1", without(decision, "evidence_decision_sha256")
            ):
                fail("E_DECISION_SET_MISMATCH", "decision commitment")
    reconciliation = evidence["reconciliation"]
    expected_reconciliation = {
        "claim_ids": _sorted_ids(populations["claim"]),
        "artifact_ids": _sorted_ids(populations["artifact"]),
        "conflict_ids": _sorted_ids(populations["conflict"]),
        "state_ids": _sorted_ids(populations["state"]),
        "capability_ids": _sorted_ids(populations["capability"]),
        "overlap_ids": _sorted_ids(populations["overlap"]),
        "candidate_ids": _sorted_ids(populations["candidate"]),
        "decision_ids": _sorted_ids(populations["decision"]),
        "decision_candidate_ids": _sorted_ids(
            {item["candidate_id"] for item in evidence["decisions"]}
        ),
        "catalog_skill_ids": _sorted_ids(populations["catalog_skill"]),
        "dangling_reference_ids": [],
        "complete": True,
    }
    if any(reconciliation.get(field) != value for field, value in expected_reconciliation.items()):
        fail("E_EVIDENCE_DANGLING_REFERENCE", "reconciliation")


def validate_publication(publication: dict[str, Any], evidence: dict[str, Any], native_values: Iterable[str] = ()) -> None:
    validate_schema(publication)
    if publication["evidence_sha256"] != evidence["evidence_sha256"]:
        fail("E_PUBLICATION_SET_MISMATCH")
    if publication["publication_sha256"] != D("history-publication/v3", without(publication, "publication_sha256")):
        fail("E_HISTORY_PUBLICATION_VERSION_UNSUPPORTED")
    strings = list(_walk_strings(publication))
    for value in native_values:
        if value and any(value in item for item in strings):
            fail("E_PUBLICATION_PRIVATE_DATA")
    for value in strings:
        if any(pattern.search(value) for pattern in PUBLICATION_FORBIDDEN):
            fail("E_PUBLICATION_PRIVATE_DATA")
    if publication["evidence_id"] != evidence["evidence_id"] or publication["index_id"] != evidence[
        "bindings"
    ]["index_id"] or publication["mode"] != evidence["mode"]:
        fail("E_PUBLICATION_SET_MISMATCH", "identity")
    if publication["source_accounting_sha256"] != evidence["source_accounting"][
        "source_accounting_sha256"
    ]:
        fail("E_PUBLICATION_SET_MISMATCH", "source accounting commitment")
    for field in ("source_ids", "included_record_ids", "excluded_record_ids", "nonsemantic_record_ids", "observation_ids"):
        if publication[field] != evidence["source_accounting"][field]:
            fail("E_PUBLICATION_SET_MISMATCH", field)
    for field in ("node_ids", "root_ids", "child_ids", "unresolved_ids", "excluded_ids", "duplicate_export_ids", "namespace_ids", "project_family_ids", "edges"):
        if publication["lineage"][field] != evidence["lineage"][field]:
            fail("E_PUBLICATION_SET_MISMATCH", field)
    owners = {
        "sources": (publication, "source_ids"),
        "included_records": (publication, "included_record_ids"),
        "excluded_records": (publication, "excluded_record_ids"),
        "nonsemantic_records": (publication, "nonsemantic_record_ids"),
        "observations": (publication, "observation_ids"),
        "lineage_nodes": (publication["lineage"], "node_ids"),
        "roots": (publication["lineage"], "root_ids"),
        "children": (publication["lineage"], "child_ids"),
        "unresolved": (publication["lineage"], "unresolved_ids"),
        "excluded": (publication["lineage"], "excluded_ids"),
        "duplicate_exports": (publication["lineage"], "duplicate_export_ids"),
        "namespaces": (publication["lineage"], "namespace_ids"),
        "project_families": (publication["lineage"], "project_family_ids"),
        "edges": (publication["lineage"], "edges"),
        **{
            field: (publication, field)
            for field in (
                "claims",
                "artifacts",
                "conflicts",
                "states",
                "capabilities",
                "overlaps",
                "candidates",
                "decisions",
            )
        },
    }
    for count, (owner, field) in owners.items():
        values = owner[field]
        if publication["counts"].get(count) != len(values) or len(values) != len(
            {canonical_bytes(item) for item in values}
        ):
            fail("E_PUBLICATION_SET_MISMATCH", count)
    expected_recurrence = [
        without(item, "classification", "classification_basis")
        for item in evidence["recurrence"]
    ]
    if publication["recurrence"] != expected_recurrence:
        fail("E_PUBLICATION_SET_MISMATCH", "recurrence")
    if publication["artifacts"] != evidence["artifacts"] or publication["conflicts"] != evidence[
        "conflicts"
    ] or publication["states"] != evidence["states"] or publication["capabilities"] != evidence[
        "capabilities"
    ] or publication["overlaps"] != evidence["overlaps"]:
        fail("E_PUBLICATION_SET_MISMATCH", "object projections")
    expected_claims = [
        {
            **without(item, "summary"),
            "paraphrase": item["summary"],
        }
        for item in evidence["claims"]
    ]
    if publication["claims"] != expected_claims:
        fail("E_PUBLICATION_SET_MISMATCH", "claims")
    if len(publication["candidates"]) != len(evidence["candidates"]):
        fail("E_PUBLICATION_SET_MISMATCH", "candidates")
    for actual, source in zip(publication["candidates"], evidence["candidates"]):
        if without(actual, "summary") != source:
            fail("E_PUBLICATION_SET_MISMATCH", "candidate projection")
    evidence_decisions = {item["decision_id"]: item for item in evidence["decisions"]}
    if set(evidence_decisions) != {item["decision_id"] for item in publication["decisions"]}:
        fail("E_PUBLICATION_SET_MISMATCH", "decision set")
    for decision in publication["decisions"]:
        source = evidence_decisions[decision["decision_id"]]
        expected = {
            "decision_id": source["decision_id"],
            "candidate_id": source["candidate_id"],
            "disposition": source["disposition"],
            "target_skill_id": source["target_skill_id"],
            "observation_ids": source["evidence_observation_ids"],
            "claim_ids": source["claim_ids"],
            "capability_ids": source["capability_ids"],
            "overlap_ids": source["overlap_ids"],
            "evidence_decision_sha256": source["evidence_decision_sha256"],
        }
        if any(decision.get(field) != value for field, value in expected.items()):
            fail("E_PUBLICATION_SET_MISMATCH", "decision projection")
        if decision["publication_decision_sha256"] != D(
            "history-publication-decision/v3",
            without(decision, "publication_decision_sha256"),
        ):
            fail("E_PUBLICATION_SET_MISMATCH", "decision commitment")
    public_body = without(publication, "allowed_opaque_ids_sha256", "publication_sha256")
    typed_public = sorted(
        collect_typed_opaque_ids(public_body), key=lambda item: (item["type"], item["id"])
    )
    if publication["allowed_opaque_ids_sha256"] != D(
        "history-publication-opaque-ids/v3", typed_public
    ):
        fail("E_PUBLICATION_PRIVATE_DATA", "opaque allowlist commitment")
    typed_evidence = {
        (item["type"], item["id"]) for item in collect_typed_opaque_ids(evidence)
    }
    if any(
        (item["type"], item["id"]) not in typed_evidence
        and item["type"] != "publication_id"
        for item in typed_public
    ):
        fail("E_PUBLICATION_PRIVATE_DATA", "unrecognized opaque id")


def diagnostic_document(code: str, detail: str = "") -> dict[str, Any]:
    """Closed output for non-authoritative inspection; never a success result."""

    return {
        "schema_version": "history-diagnostic/v1",
        "authoritative": False,
        "diagnostic": code,
        "detail": detail,
    }


def validate_successor_chain(
    documents: dict[str, dict[str, Any]],
    *,
    authoritative_raw_reopen: bool,
    exact_model_available: bool,
    native_values: Iterable[str] | None = None,
) -> None:
    diagnostic = ordered_migration_diagnostic(
        documents,
        authoritative_raw_reopen=authoritative_raw_reopen,
        exact_history_binding=True,
        exact_model_available=exact_model_available,
    )
    if diagnostic is not None:
        fail(diagnostic)
    if native_values is None:
        fail("E_RAW_REOPEN_REQUIRED", "private native map was not reopened")
    history = documents["history"]
    ledger = documents["ledger"]
    index = documents["index"]
    reduction = documents["reduction"]
    evidence = documents["evidence"]
    publication = documents["publication"]
    if history["retention"]["disposition"] == "delete-after-validation":
        fail(
            "E_LEDGER_EXPIRED",
            "delete-after-validation cannot authorize publication while private state is live",
        )
    validate_ledger(ledger)
    validate_sources(history, ledger)
    validate_index(index, history, ledger)
    validate_reduction(reduction, index, ledger)
    validate_evidence(evidence, reduction, index, ledger, history)
    validate_publication(publication, evidence, native_values)
