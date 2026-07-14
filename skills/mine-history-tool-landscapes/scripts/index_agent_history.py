#!/usr/bin/env python3
"""Build a private, publication-safe index from normalized agent-history metadata."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import stat
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterator


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from strict_json import StrictJSONError, loads_strict


SOURCE_SCHEMA = "history-sources/v2"
CAMPAIGN_SCHEMA = "active-campaign/v2"
INDEX_SCHEMA = "history-index/v2"
ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
HEX_RE = re.compile(r"^[0-9a-f]{16,64}$")
SECRET_RE = re.compile(
    r"(?:-----BEGIN [A-Z ]*PRIVATE KEY-----|github_pat_[A-Za-z0-9_]{16,}|"
    r"(?:sk|ghp|xox[baprs])-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16})",
    re.I,
)
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_LINE_BYTES = 1024 * 1024
MAX_ROWS = 1_000_000
MAX_SOURCES = 128
MAX_TOTAL_SOURCE_BYTES = 256 * 1024 * 1024
MAX_TOTAL_ROWS = 2_000_000
MAX_UNIQUE_SESSIONS = 1_000_000
MAX_NATIVE_ID = 512
MAX_NAMESPACE = 512
MAX_LOCATOR = 2048
PUBLIC_FILES = {
    "source-ledger.jsonl",
    "roots.jsonl",
    "children.jsonl",
    "unresolved.jsonl",
    "exclusion-ledger.jsonl",
    "private/native-map.jsonl",
}
RECURRENCE_CLASSES = {"user-intent", "delegated", "retry", "continuation", "test", "replay", "synthetic", "system"}
CLASSIFICATION_BASES = {"native-metadata", "reducer-reviewed"}


class ContractError(Exception):
    pass


def parse_time(value: object, label: str) -> datetime:
    if not isinstance(value, str):
        raise ContractError(f"{label} must be a timezone-aware RFC 3339 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"invalid {label}: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def in_git_tree(path: Path) -> bool:
    current = path.resolve(strict=False)
    if not current.is_dir():
        current = current.parent
    while True:
        if (current / ".git").exists():
            return True
        if current == current.parent:
            return False
        current = current.parent


def validate_identifier(value: object, label: str, *, maximum: int = MAX_NATIVE_ID, minimum: int = 4) -> str:
    if not isinstance(value, str) or not (minimum <= len(value) <= maximum):
        raise ContractError(f"{label} must be a {minimum}-{maximum} character string")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ContractError(f"{label} contains control characters")
    if SECRET_RE.search(value):
        raise ContractError(f"{label} contains credential-like content")
    return value


def validate_exact_keys(value: dict, required: set[str], optional: set[str], label: str) -> None:
    missing = required - set(value)
    extra = set(value) - required - optional
    if missing or extra:
        raise ContractError(f"{label} keys mismatch: missing={sorted(missing)}, extra={sorted(extra)}")


def opaque(key: bytes, run_salt: bytes, domain: str, *parts: str, prefix: str = "h") -> str:
    message = "\0".join((domain, *parts)).encode("utf-8")
    token = hmac.new(key, run_salt + b"\0" + message, hashlib.sha256).hexdigest()[:24]
    return f"{prefix}-{token}"


def load_json_snapshot(path: Path) -> tuple[dict, str]:
    try:
        if path.is_symlink():
            raise ContractError(f"{path} must not be a symlink")
        before = path.stat()
        if not stat.S_ISREG(before.st_mode):
            raise ContractError(f"{path} must be a regular file")
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino) or not stat.S_ISREG(opened.st_mode):
                raise ContractError(f"{path} changed before snapshot read")
            raw = handle.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise ContractError(f"{path} exceeds the 1 MiB contract limit")
            after = os.fstat(handle.fileno())
        if (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise ContractError(f"{path} changed during snapshot read")
        value = loads_strict(raw.decode("utf-8"))
    except ContractError:
        raise
    except (OSError, UnicodeError, StrictJSONError) as exc:
        raise ContractError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{path} must contain a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


@contextmanager
def open_beneath(path: Path, root: Path) -> Iterator[BinaryIO]:
    """Open a regular file beneath root without following any path-component symlink."""
    if not path.is_absolute() or not root.is_absolute():
        raise ContractError("source path and authorized root must be absolute")
    if root.is_symlink():
        raise ContractError("authorized root must not be a symlink")
    try:
        root_stat = root.stat()
    except OSError as exc:
        raise ContractError(f"cannot stat authorized root: {exc}") from exc
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ContractError("authorized root must be a directory")
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ContractError("source escapes its authorized root") from exc
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise ContractError("source path has unsafe components")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | nofollow)
    file_fd: int | None = None
    try:
        opened_root = os.fstat(directory)
        if (root_stat.st_dev, root_stat.st_ino) != (opened_root.st_dev, opened_root.st_ino):
            raise ContractError("authorized root changed before open")
        for component in relative.parts[:-1]:
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=directory)
            os.close(directory)
            directory = next_fd
        file_fd = os.open(relative.parts[-1], os.O_RDONLY | nofollow, dir_fd=directory)
        opened = os.fstat(file_fd)
        if not stat.S_ISREG(opened.st_mode):
            raise ContractError("normalized source must be a regular file")
        with os.fdopen(file_fd, "rb", closefd=True) as handle:
            file_fd = None
            before_read = os.fstat(handle.fileno())
            yield handle
            after_read = os.fstat(handle.fileno())
            if (before_read.st_dev, before_read.st_ino, before_read.st_size, before_read.st_mtime_ns) != (
                after_read.st_dev,
                after_read.st_ino,
                after_read.st_size,
                after_read.st_mtime_ns,
            ):
                raise ContractError("normalized source changed during streamed read")
    except OSError as exc:
        raise ContractError(f"cannot safely open normalized source: {exc}") from exc
    finally:
        if file_fd is not None:
            os.close(file_fd)
        os.close(directory)


def read_key(path: Path) -> bytes:
    if not path.is_absolute():
        raise ContractError("id key path must be absolute")
    if path.is_symlink() or in_git_tree(path):
        raise ContractError("id key must be a non-symlink file outside git")
    try:
        info = path.stat()
    except OSError as exc:
        raise ContractError(f"cannot stat id key: {exc}") from exc
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_uid != os.getuid():
        raise ContractError("id key must be owned by the current user with mode 0600")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (info.st_dev, info.st_ino) != (opened.st_dev, opened.st_ino) or not stat.S_ISREG(opened.st_mode) or stat.S_IMODE(opened.st_mode) != 0o600 or opened.st_uid != os.getuid():
                raise ContractError("id key changed before open or has unsafe permissions")
            key = handle.read(4097)
    except OSError as exc:
        raise ContractError(f"cannot read id key: {exc}") from exc
    if not (32 <= len(key) <= 4096):
        raise ContractError("id key must contain 32-4096 bytes")
    return key


def parse_retention(value: object) -> dict:
    if not isinstance(value, dict):
        raise ContractError("retention must be an object")
    disposition = value.get("disposition")
    if disposition == "delete-after-validation":
        validate_exact_keys(value, {"disposition"}, set(), "retention")
    elif disposition == "delete-by":
        validate_exact_keys(value, {"disposition", "expires_at"}, set(), "retention")
        if parse_time(value["expires_at"], "retention.expires_at") <= datetime.now(timezone.utc):
            raise ContractError("retention.expires_at must be in the future")
    else:
        raise ContractError("retention.disposition must be delete-after-validation or delete-by")
    return value


def parse_cutoff_attestation(value: object, cutoff: datetime) -> dict:
    if not isinstance(value, dict):
        raise ContractError("cutoff_attestation must be an object")
    validate_exact_keys(value, {"kind", "attested_at", "authority"}, set(), "cutoff_attestation")
    if value.get("kind") != "pre-discovery" or not isinstance(value.get("authority"), str) or not value["authority"].strip():
        raise ContractError("cutoff_attestation must be a pre-discovery attestation with authority")
    if parse_time(value["attested_at"], "cutoff_attestation.attested_at") < cutoff:
        raise ContractError("cutoff attestation cannot predate the cutoff")
    return value


def iter_source_rows(handle: BinaryIO, source_id: str) -> tuple[list[tuple[int, dict]], str, int]:
    digest = hashlib.sha256()
    rows: list[tuple[int, dict]] = []
    total = 0
    line_no = 0
    while True:
        line = handle.readline(MAX_LINE_BYTES + 1)
        if not line:
            break
        line_no += 1
        total += len(line)
        if total > MAX_SOURCE_BYTES:
            raise ContractError(f"source {source_id} exceeds {MAX_SOURCE_BYTES} bytes")
        if len(line) > MAX_LINE_BYTES:
            raise ContractError(f"source {source_id}:{line_no} exceeds {MAX_LINE_BYTES} bytes")
        digest.update(line)
        if not line.strip():
            continue
        if len(rows) >= MAX_ROWS:
            raise ContractError(f"source {source_id} exceeds {MAX_ROWS} rows")
        try:
            value = loads_strict(line.decode("utf-8"))
        except (UnicodeError, StrictJSONError) as exc:
            raise ContractError(f"{source_id}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ContractError(f"{source_id}:{line_no}: row must be an object")
        rows.append((line_no, value))
    return rows, digest.hexdigest(), total


def validate_remote_authorization(source: dict, snapshot_hash: str) -> None:
    authorization = source.get("authorization")
    if source["origin"] == "local":
        if authorization != {"kind": "local-default"}:
            raise ContractError(f"local source {source['source_id']} needs local-default authorization")
        return
    if source["state"] != "frozen" or not isinstance(authorization, dict):
        raise ContractError(f"remote source {source['source_id']} must be a frozen approved snapshot")
    required = {"kind", "source_id", "snapshot_sha256", "approved_by", "captured_at", "approved_at", "scope"}
    validate_exact_keys(authorization, required, set(), f"authorization for {source['source_id']}")
    if (
        authorization.get("kind") != "approved-snapshot"
        or authorization.get("source_id") != source["source_id"]
        or authorization.get("snapshot_sha256") != snapshot_hash
        or authorization.get("scope") != "history-metadata"
        or not isinstance(authorization.get("approved_by"), str)
        or not authorization["approved_by"].strip()
    ):
        raise ContractError(f"remote authorization receipt does not bind source {source['source_id']} and snapshot")
    captured = parse_time(authorization.get("captured_at"), f"authorization for {source['source_id']}.captured_at")
    approved = parse_time(authorization.get("approved_at"), f"authorization for {source['source_id']}.approved_at")
    if approved < captured:
        raise ContractError(f"remote authorization for {source['source_id']} predates capture")


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_json(value))
    path.chmod(0o600)


def write_jsonl(path: Path, values: list[dict]) -> None:
    with path.open("wb") as handle:
        for value in values:
            handle.write(canonical_json(value))
    path.chmod(0o600)


def build(source_contract: Path, campaign_contract: Path | None, key_path: Path, out: Path) -> None:
    if not out.is_absolute():
        raise ContractError("output directory must be absolute")
    if out.is_symlink() or (out.exists() and (not out.is_dir() or any(out.iterdir()))):
        raise ContractError("output directory must not exist or must be an empty non-symlink directory")
    if in_git_tree(out):
        raise ContractError("private index must be outside a git worktree")
    key = read_key(key_path)
    run_salt = secrets.token_bytes(32)

    source_doc, source_contract_hash = load_json_snapshot(source_contract)
    validate_exact_keys(
        source_doc,
        {"schema_version", "cutoff_at", "cutoff_attestation", "retention", "sources"},
        set(),
        "source contract",
    )
    if source_doc.get("schema_version") != SOURCE_SCHEMA:
        raise ContractError("unsupported source contract schema")
    cutoff = parse_time(source_doc.get("cutoff_at"), "cutoff_at")
    cutoff_attestation = parse_cutoff_attestation(source_doc.get("cutoff_attestation"), cutoff)
    retention = parse_retention(source_doc.get("retention"))

    campaign: dict | None = None
    campaign_contract_hash: str | None = None
    campaign_start: datetime | None = None
    if campaign_contract is not None:
        campaign, campaign_contract_hash = load_json_snapshot(campaign_contract)
        validate_exact_keys(
            campaign,
            {"schema_version", "platform", "root_native_id", "root_aliases", "campaign_start"},
            set(),
            "campaign contract",
        )
        if campaign.get("schema_version") != CAMPAIGN_SCHEMA:
            raise ContractError("unsupported campaign contract schema")
        if not isinstance(campaign.get("platform"), str) or not ID_RE.fullmatch(campaign["platform"]):
            raise ContractError("campaign platform must be a normalized ID")
        validate_identifier(campaign.get("root_native_id"), "campaign root_native_id")
        aliases = campaign.get("root_aliases")
        if not isinstance(aliases, list) or any(not isinstance(alias, str) for alias in aliases) or len(aliases) != len(set(aliases)):
            raise ContractError("campaign root_aliases must be unique")
        for index, alias in enumerate(aliases):
            validate_identifier(alias, f"campaign root_aliases[{index}]")
        campaign_start = parse_time(campaign.get("campaign_start"), "campaign_start")

    sources = source_doc.get("sources")
    if not isinstance(sources, list) or not sources or len(sources) > MAX_SOURCES:
        raise ContractError(f"source contract needs 1-{MAX_SOURCES} sources")

    observations = 0
    canonical: dict[tuple[str, str], dict] = {}
    source_rows: list[dict] = []
    native_sources: dict[tuple[str, str], list[dict]] = {}
    seen_source_ids: set[str] = set()
    aggregate_source_bytes = 0
    aggregate_rows = 0
    required_source = {"source_id", "platform", "kind", "path", "authorized_root", "state", "origin", "authorization"}
    for source_index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ContractError("source rows must be objects")
        validate_exact_keys(source, required_source, set(), f"sources[{source_index}]")
        source_id, platform = source.get("source_id"), source.get("platform")
        if not isinstance(source_id, str) or not ID_RE.fullmatch(source_id) or source_id in seen_source_ids:
            raise ContractError("source_id must be unique and normalized")
        if not isinstance(platform, str) or not ID_RE.fullmatch(platform):
            raise ContractError(f"source {source_id} platform must be normalized")
        seen_source_ids.add(source_id)
        if source.get("kind") != "normalized-jsonl" or source.get("state") not in {"frozen", "live"} or source.get("origin") not in {"local", "remote-snapshot"}:
            raise ContractError(f"unsupported source kind/state/origin for {source_id}")
        path, root = Path(str(source.get("path"))), Path(str(source.get("authorized_root")))
        with open_beneath(path, root) as handle:
            parsed_rows, snapshot_hash, source_bytes = iter_source_rows(handle, source_id)
        aggregate_source_bytes += source_bytes
        aggregate_rows += len(parsed_rows)
        if aggregate_source_bytes > MAX_TOTAL_SOURCE_BYTES or aggregate_rows > MAX_TOTAL_ROWS:
            raise ContractError("aggregate source byte or row limit exceeded")
        validate_remote_authorization(source, snapshot_hash)
        source_count = 0
        for line_no, row in parsed_rows:
            allowed_fields = {
                "native_session_id",
                "native_aliases",
                "native_parent_id",
                "started_at",
                "role",
                "namespace",
                "root_intent_hash",
                "project_family_hash",
                "recurrence_class",
                "classification_basis",
                "source_locator",
            }
            unknown_fields = set(row) - allowed_fields
            if unknown_fields:
                raise ContractError(f"{source_id}:{line_no}: unknown or content-bearing fields forbidden: {sorted(unknown_fields)}")
            native_id = validate_identifier(row.get("native_session_id"), f"{source_id}:{line_no}:native_session_id")
            role = row.get("role")
            if role not in {"root", "child", "unresolved"}:
                raise ContractError(f"{source_id}:{line_no}: invalid role")
            started = parse_time(row.get("started_at"), f"{source_id}:{line_no}:started_at")
            parent = row.get("native_parent_id")
            if parent is not None:
                parent = validate_identifier(parent, f"{source_id}:{line_no}:native_parent_id")
            if role == "root" and parent is not None:
                raise ContractError(f"{source_id}:{line_no}: root may not have a parent")
            namespace = row.get("namespace")
            if namespace is not None:
                namespace = validate_identifier(namespace, f"{source_id}:{line_no}:namespace", maximum=MAX_NAMESPACE)
            aliases = row.get("native_aliases", [])
            if not isinstance(aliases, list) or any(not isinstance(alias, str) for alias in aliases) or len(aliases) > 128 or len(aliases) != len(set(aliases)):
                raise ContractError(f"{source_id}:{line_no}: native_aliases must be at most 128 unique strings")
            aliases = [validate_identifier(alias, f"{source_id}:{line_no}:native_alias") for alias in aliases]
            intent_hash = row.get("root_intent_hash")
            if intent_hash is not None and (not isinstance(intent_hash, str) or not HEX_RE.fullmatch(intent_hash)):
                raise ContractError(f"{source_id}:{line_no}: invalid root_intent_hash")
            family_hash = row.get("project_family_hash")
            if family_hash is not None and (not isinstance(family_hash, str) or not HEX_RE.fullmatch(family_hash)):
                raise ContractError(f"{source_id}:{line_no}: invalid project_family_hash")
            recurrence_class = row.get("recurrence_class")
            classification_basis = row.get("classification_basis")
            if not isinstance(recurrence_class, str) or recurrence_class not in RECURRENCE_CLASSES:
                raise ContractError(f"{source_id}:{line_no}: invalid recurrence_class")
            if not isinstance(classification_basis, str) or classification_basis not in CLASSIFICATION_BASES:
                raise ContractError(f"{source_id}:{line_no}: invalid classification_basis")
            locator = row.get("source_locator")
            if locator is not None:
                locator = validate_identifier(locator, f"{source_id}:{line_no}:source_locator", maximum=MAX_LOCATOR, minimum=1)
            key_tuple = (platform, native_id)
            normalized = {
                "platform": platform,
                "native_session_id": native_id,
                "native_parent_id": parent,
                "started_at": started.isoformat().replace("+00:00", "Z"),
                "role": role,
                "namespace": namespace,
                "native_aliases": aliases,
                "root_intent_hash": intent_hash,
                "project_family_hash": family_hash,
                "recurrence_class": recurrence_class,
                "classification_basis": classification_basis,
            }
            comparable_fields = (
                "native_parent_id",
                "started_at",
                "role",
                "namespace",
                "native_aliases",
                "root_intent_hash",
                "project_family_hash",
                "recurrence_class",
                "classification_basis",
            )
            comparable = {field: normalized[field] for field in comparable_fields}
            if key_tuple in canonical:
                previous = {field: canonical[key_tuple][field] for field in comparable_fields}
                if previous != comparable:
                    raise ContractError(f"conflicting duplicate observations for {platform}:{native_id}")
            else:
                canonical[key_tuple] = normalized
                if len(canonical) > MAX_UNIQUE_SESSIONS:
                    raise ContractError(f"unique session limit {MAX_UNIQUE_SESSIONS} exceeded")
            native_sources.setdefault(key_tuple, []).append(
                {
                    "source_id": source_id,
                    "field_locator_hashes": {
                        field: hashlib.sha256(f"{locator or ''}\0{field}".encode()).hexdigest()
                        for field in sorted(row)
                    },
                    "line": line_no,
                    "path": str(path),
                }
            )
            observations += 1
            source_count += 1
        source_rows.append(
            {
                "source_id": source_id,
                "platform": platform,
                "kind": source["kind"],
                "state": source["state"],
                "origin": source["origin"],
                "record_count": source_count,
                "snapshot_hash": snapshot_hash,
            }
        )

    alias_map: dict[tuple[str, str], tuple[str, str]] = {}
    for key_tuple, row in canonical.items():
        for alias in [row["native_session_id"], *row["native_aliases"]]:
            alias_key = (row["platform"], alias)
            if alias_key in alias_map and alias_map[alias_key] != key_tuple:
                raise ContractError(f"ambiguous native alias {row['platform']}:{alias}")
            alias_map[alias_key] = key_tuple
    children: dict[tuple[str, str], list[tuple[str, str]]] = {key: [] for key in canonical}
    for key_tuple, row in canonical.items():
        parent = row["native_parent_id"]
        if parent is not None:
            parent_key = alias_map.get((row["platform"], parent), (row["platform"], parent))
            if parent_key in canonical:
                if parse_time(row["started_at"], "started_at") < parse_time(canonical[parent_key]["started_at"], "parent started_at"):
                    raise ContractError("child starts before its resolved parent")
                children[parent_key].append(key_tuple)

    colors: dict[tuple[str, str], int] = {}
    for start in canonical:
        if colors.get(start) == 2:
            continue
        stack: list[tuple[tuple[str, str], bool]] = [(start, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                colors[node] = 2
                continue
            if colors.get(node) == 1:
                raise ContractError("cycle detected in session lineage")
            if colors.get(node) == 2:
                continue
            colors[node] = 1
            stack.append((node, True))
            for child in reversed(children[node]):
                if colors.get(child) == 1:
                    raise ContractError("cycle detected in session lineage")
                if colors.get(child) != 2:
                    stack.append((child, False))

    excluded: dict[tuple[str, str], set[str]] = {}

    def exclude(node: tuple[str, str], reason: str) -> bool:
        before = len(excluded.get(node, set()))
        excluded.setdefault(node, set()).add(reason)
        return len(excluded[node]) != before

    for key_tuple, row in canonical.items():
        if parse_time(row["started_at"], "started_at") > cutoff:
            exclude(key_tuple, "after_cutoff")

    campaign_key: tuple[str, str] | None = None
    if campaign is not None and campaign_start is not None:
        campaign_matches = {
            alias_map[(campaign["platform"], alias)]
            for alias in [campaign["root_native_id"], *campaign["root_aliases"]]
            if (campaign["platform"], alias) in alias_map
        }
        if len(campaign_matches) != 1:
            raise ContractError("campaign root does not resolve exactly once")
        campaign_key = next(iter(campaign_matches))
        campaign_root = canonical[campaign_key]
        if campaign_root["role"] != "root":
            raise ContractError("campaign root is not classified as a root")
        if campaign_start > parse_time(campaign_root["started_at"], "campaign root started_at"):
            raise ContractError("campaign_start must not be later than campaign root started_at")
        exclude(campaign_key, "campaign_root")
        campaign_reasons = {"campaign_root", "campaign_descendant", "campaign_namespace_after_start", "descendant_of_namespace_seed"}
        changed = True
        while changed:
            changed = False
            for parent, child_nodes in children.items():
                if parent in excluded and excluded[parent] & campaign_reasons:
                    reason = "campaign_descendant" if "campaign_root" in excluded[parent] else "descendant_of_namespace_seed"
                    for child in child_nodes:
                        changed |= exclude(child, reason)
            namespaces = {
                canonical[key]["namespace"]
                for key, reasons in excluded.items()
                if canonical[key]["namespace"]
                and parse_time(canonical[key]["started_at"], "started_at") <= cutoff
                and reasons & campaign_reasons
            }
            for key_tuple, row in canonical.items():
                if (
                    row["namespace"] in namespaces
                    and parse_time(row["started_at"], "started_at") >= campaign_start
                    and parse_time(row["started_at"], "started_at") <= cutoff
                ):
                    changed |= exclude(key_tuple, "campaign_namespace_after_start")

    public_rows: dict[str, list[dict]] = {"root": [], "child": [], "unresolved": []}
    exclusion_rows: list[dict] = []
    private_rows: list[dict] = []
    seen_public: set[str] = set()
    source_hash_by_id = {row["source_id"]: row["snapshot_hash"] for row in source_rows}
    for key_tuple in sorted(canonical):
        row = canonical[key_tuple]
        record_id = opaque(key, run_salt, "record", row["platform"], row["native_session_id"])
        if record_id in seen_public:
            raise ContractError("opaque record ID collision")
        seen_public.add(record_id)
        resolved_parent = alias_map.get((row["platform"], row["native_parent_id"])) if row["native_parent_id"] else None
        parent_record_id = (
            opaque(key, run_salt, "record", canonical[resolved_parent]["platform"], canonical[resolved_parent]["native_session_id"])
            if resolved_parent
            else None
        )
        observed_source_ids = sorted({item["source_id"] for item in native_sources[key_tuple]})
        public = {
            "record_id": record_id,
            "platform": row["platform"],
            "parent_record_id": parent_record_id,
            "parent_resolution": "resolved" if resolved_parent else ("missing" if row["native_parent_id"] else "none"),
            "started_at": row["started_at"],
            "role": row["role"],
            "namespace_hash": opaque(key, run_salt, "namespace", row["namespace"], prefix="n") if row["namespace"] else None,
            "root_intent_hash": opaque(key, run_salt, "intent", row["root_intent_hash"], prefix="i") if row["root_intent_hash"] else None,
            "project_family_hash": opaque(key, run_salt, "family", row["project_family_hash"], prefix="f") if row["project_family_hash"] else None,
            "recurrence_class": row["recurrence_class"],
            "classification_basis": row["classification_basis"],
            "source_ids": observed_source_ids,
            "source_hashes": {source_id: source_hash_by_id[source_id] for source_id in observed_source_ids},
            "eligible_for_recurrence": row["role"] == "root" and row["recurrence_class"] == "user-intent" and row["classification_basis"] == "reducer-reviewed" and key_tuple not in excluded,
        }
        private_rows.append(
            {
                "record_id": record_id,
                "platform": row["platform"],
                "native_session_id": row["native_session_id"],
                "native_aliases": row["native_aliases"],
                "native_parent_id": row["native_parent_id"],
                "namespace": row["namespace"],
                "observations": native_sources[key_tuple],
            }
        )
        if key_tuple in excluded:
            exclusion_rows.append({"record_id": record_id, "reasons": sorted(excluded[key_tuple])})
        else:
            public_rows[row["role"]].append(public)

    temp_parent = out.parent
    temp_parent.mkdir(parents=True, exist_ok=True)
    if temp_parent.is_symlink() or in_git_tree(temp_parent):
        raise ContractError("output parent must be a real directory outside git")
    temp = Path(tempfile.mkdtemp(prefix=f".{out.name}-", dir=temp_parent))
    try:
        temp.chmod(0o700)
        (temp / "private").mkdir(mode=0o700)
        write_jsonl(temp / "source-ledger.jsonl", sorted(source_rows, key=lambda row: row["source_id"]))
        write_jsonl(temp / "roots.jsonl", sorted(public_rows["root"], key=lambda row: row["record_id"]))
        write_jsonl(temp / "children.jsonl", sorted(public_rows["child"], key=lambda row: row["record_id"]))
        write_jsonl(temp / "unresolved.jsonl", sorted(public_rows["unresolved"], key=lambda row: row["record_id"]))
        write_jsonl(temp / "exclusion-ledger.jsonl", sorted(exclusion_rows, key=lambda row: row["record_id"]))
        write_jsonl(temp / "private" / "native-map.jsonl", sorted(private_rows, key=lambda row: row["record_id"]))
        included_families = {
            row["project_family_hash"]
            for row in public_rows["root"]
            if row["project_family_hash"]
        }
        counts = {
            "source_observations": observations,
            "duplicates_collapsed": observations - len(canonical),
            "unique_sessions": len(canonical),
            "included_roots": len(public_rows["root"]),
            "included_children": len(public_rows["child"]),
            "included_unresolved": len(public_rows["unresolved"]),
            "primary_exclusions": len(exclusion_rows),
            "included_project_families": len(included_families),
        }
        if counts["source_observations"] != counts["duplicates_collapsed"] + counts["unique_sessions"]:
            raise ContractError("observation accounting failed")
        if counts["unique_sessions"] != counts["included_roots"] + counts["included_children"] + counts["included_unresolved"] + counts["primary_exclusions"]:
            raise ContractError("session accounting failed")
        content_hashes = {
            name: file_hash(temp / name)
            for name in sorted(PUBLIC_FILES)
        }
        manifest_core = {
            "schema_version": INDEX_SCHEMA,
            "run_salt": run_salt.hex(),
            "cutoff_at": cutoff.isoformat().replace("+00:00", "Z"),
            "cutoff_attestation": cutoff_attestation,
            "retention": retention,
            "source_contract_hash": source_contract_hash,
            "campaign_contract_hash": campaign_contract_hash,
            "exclusion_basis": "campaign-and-cutoff" if campaign_key else "trusted-cutoff",
            "counts": counts,
            "file_hashes": content_hashes,
        }
        manifest_core["corpus_hash"] = hashlib.sha256(canonical_json(manifest_core)).hexdigest()
        write_json(temp / "manifest.json", manifest_core)
        if out.exists():
            out.rmdir()
        temp.replace(out)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-contract", type=Path, required=True)
    parser.add_argument("--campaign-contract", type=Path)
    parser.add_argument("--id-key-file", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args.source_contract, args.campaign_contract, args.id_key_file, args.out)
    except (ContractError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"ok": True, "output_name": args.out.name, "manifest": "manifest.json"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
