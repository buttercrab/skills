#!/usr/bin/env python3
"""Validate history-index integrity, evidence grounding, and publication redaction."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from strict_json import loads_strict


INDEX_SCHEMA = "history-index/v2"
EVIDENCE_SCHEMA = "history-evidence/v2"
PUBLICATION_SCHEMA = "history-publication/v2"
ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
RECORD_RE = re.compile(r"^h-[0-9a-f]{24}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
DERIVED_RE = {
    "namespace_hash": re.compile(r"^n-[0-9a-f]{24}$"),
    "root_intent_hash": re.compile(r"^i-[0-9a-f]{24}$"),
    "project_family_hash": re.compile(r"^f-[0-9a-f]{24}$"),
}
OPAQUE_RE = re.compile(r"\bh-[0-9a-f]{24}\b")
URL_RE = re.compile(r"(?:https?|s3|r2|file|ssh|slack|gs)://\S+", re.I)
URI_SCHEME_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9+.-]{0,31}:[^\s]", re.I)
ABS_PATH_RE = re.compile(r"(?<![:A-Za-z0-9_.-])/(?:[A-Za-z0-9_.~%-]+(?:/[A-Za-z0-9_.~% -]+)*)")
WINDOWS_PATH_RE = re.compile(r"(?:\b[A-Za-z]:\\|\\\\[^\\\s]+\\[^\\\s]+)")
SECRET_RE = re.compile(
    r"(?:-----BEGIN [A-Z ]*PRIVATE KEY-----|github_pat_[A-Za-z0-9_]{16,}|"
    r"(?:sk|ghp|xox[baprs])[-_][A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16}|"
    r"(?:token|password|secret|api[_-]?key)\s*[:=]\s*[^\s,}]{8,})",
    re.I,
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+\d{7,15}|\+\d[\d ()-]{6,}\d|\(\d{2,4}\)[\d -]{5,}\d|\d{3}[- .]\d{3}[- .]\d{4})(?!\w)")
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
PUBLIC_FILES = {
    "source-ledger.jsonl",
    "roots.jsonl",
    "children.jsonl",
    "unresolved.jsonl",
    "exclusion-ledger.jsonl",
    "private/native-map.jsonl",
}
ROOT_FILES = {"manifest.json", "source-ledger.jsonl", "roots.jsonl", "children.jsonl", "unresolved.jsonl", "exclusion-ledger.jsonl", "private"}
RECORD_FIELDS = {
    "record_id",
    "platform",
    "parent_record_id",
    "parent_resolution",
    "started_at",
    "role",
    "namespace_hash",
    "root_intent_hash",
    "project_family_hash",
    "recurrence_class",
    "classification_basis",
    "source_ids",
    "source_hashes",
    "eligible_for_recurrence",
}
OBSERVATION_FIELDS = {
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
RECURRENCE_CLASSES = {"user-intent", "delegated", "retry", "continuation", "test", "replay", "synthetic", "system"}
CLASSIFICATION_BASES = {"native-metadata", "reducer-reviewed"}
MAX_PUBLIC_INPUT_BYTES = 16 * 1024 * 1024
EXCLUSION_REASONS = {
    "after_cutoff",
    "campaign_root",
    "campaign_descendant",
    "campaign_namespace_after_start",
    "descendant_of_namespace_seed",
}


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def read_json(path: Path) -> object:
    if path.is_symlink():
        raise ValueError(f"{path} must not be a symlink")
    before = path.stat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f"{path} must be a regular file")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino) or not stat.S_ISREG(opened.st_mode):
            raise ValueError(f"{path} changed before open")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, min(1024 * 1024, MAX_PUBLIC_INPUT_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_PUBLIC_INPUT_BYTES:
                raise ValueError(f"{path} exceeds {MAX_PUBLIC_INPUT_BYTES} bytes")
        after = os.fstat(fd)
        if (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError(f"{path} changed during read")
    finally:
        os.close(fd)
    return loads_strict(b"".join(chunks).decode("utf-8"))


def parse_time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo is not None else None


def in_git_tree(path: Path) -> bool:
    current = path.resolve(strict=False)
    while True:
        if (current / ".git").exists():
            return True
        if current == current.parent:
            return False
        current = current.parent


def unique_string_list(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) for item in value)
        and len(value) == len(set(value))
    )


class Validator:
    def __init__(self, index: Path, evidence: object, publication: object):
        self.index = index
        self.evidence = evidence
        self.publication = publication
        self.errors: list[dict[str, str]] = []
        self.records: dict[str, dict] = {}
        self.all_record_ids: set[str] = set()
        self.excluded: set[str] = set()
        self.native_values: set[str] = set()
        self.source_hash_by_id: dict[str, str] = {}
        self.source_state_by_id: dict[str, str] = {}
        self.source_rows: list[dict] = []
        self.manifest_counts: dict[str, int] = {}
        self.claim_ids: set[str] = set()
        self.claim_record_ids: dict[str, set[str]] = {}
        self.claim_artifact_ids: dict[str, set[str]] = {}
        self.claim_refs: dict[str, list[dict]] = {}
        self.artifacts: dict[str, dict] = {}
        self.observations: dict[tuple[str, str, str], set[tuple[int, str]]] = {}
        self.lineage_edges: dict[str, dict] = {}
        self.capability_ids: set[str] = set()
        self.overlap_ids: set[str] = set()
        self.decision_candidate_ids: set[str] = set()
        self.index_identity: tuple[int, int] | None = None
        self.private_observation_counts: dict[str, int] = {}

    def err(self, path: str, code: str, message: str) -> None:
        self.errors.append({"path": path, "code": code, "message": message})

    def exact_keys(self, value: dict, required: set[str], path: str) -> bool:
        missing = required - set(value)
        extra = set(value) - required
        if missing or extra:
            self.err(path, "schema-keys", f"missing={sorted(missing)}, extra={sorted(extra)}")
            return False
        return True

    def safe_layout(self) -> bool:
        try:
            if not self.index.is_absolute() or self.index.is_symlink() or in_git_tree(self.index):
                self.err("/index", "unsafe-index-location", "index must be an absolute non-symlink directory outside git")
                return False
            info = self.index.stat()
            if not stat.S_ISDIR(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o700 or info.st_uid != os.getuid():
                self.err("/index", "unsafe-permissions", "index must be user-owned mode 0700")
                return False
            self.index_identity = (info.st_dev, info.st_ino)
            actual_root = {entry.name for entry in self.index.iterdir()}
            if actual_root != ROOT_FILES:
                self.err("/index", "index-file-set", f"unexpected index entries: {sorted(actual_root ^ ROOT_FILES)}")
                return False
            private = self.index / "private"
            private_info = private.lstat()
            if private.is_symlink() or not stat.S_ISDIR(private_info.st_mode) or stat.S_IMODE(private_info.st_mode) != 0o700 or private_info.st_uid != os.getuid():
                self.err("/index/private", "unsafe-permissions", "private directory must be user-owned mode 0700")
                return False
            if {entry.name for entry in private.iterdir()} != {"native-map.jsonl"}:
                self.err("/index/private", "index-file-set", "private directory must contain only native-map.jsonl")
                return False
            for name in ["manifest.json", *sorted(PUBLIC_FILES)]:
                path = self.index / name
                file_info = path.lstat()
                if path.is_symlink() or not stat.S_ISREG(file_info.st_mode) or stat.S_IMODE(file_info.st_mode) != 0o600 or file_info.st_uid != os.getuid():
                    self.err(f"/index/{name}", "unsafe-permissions", "index files must be user-owned regular non-symlink files mode 0600")
                    return False
        except OSError as exc:
            self.err("/index", "index-read", str(exc))
            return False
        return True

    def index_bytes(self, name: str, *, maximum: int = 128 * 1024 * 1024) -> bytes:
        if name not in {"manifest.json", *PUBLIC_FILES}:
            raise ValueError(f"unsafe index member {name!r}")
        nofollow = getattr(os, "O_NOFOLLOW", 0)
        root_fd = os.open(self.index, os.O_RDONLY | os.O_DIRECTORY | nofollow)
        directory_fd = root_fd
        private_fd: int | None = None
        file_fd: int | None = None
        try:
            root_info = os.fstat(root_fd)
            if self.index_identity != (root_info.st_dev, root_info.st_ino):
                raise ValueError("index directory changed after validation")
            parts = name.split("/")
            if len(parts) == 2:
                private_fd = os.open(parts[0], os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=root_fd)
                directory_fd = private_fd
            file_fd = os.open(parts[-1], os.O_RDONLY | nofollow, dir_fd=directory_fd)
            info = os.fstat(file_fd)
            if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_uid != os.getuid():
                raise ValueError("index member changed or has unsafe permissions")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = os.read(file_fd, min(1024 * 1024, maximum + 1 - total))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > maximum:
                    raise ValueError(f"index member exceeds {maximum} bytes")
            return b"".join(chunks)
        finally:
            if file_fd is not None:
                os.close(file_fd)
            if private_fd is not None:
                os.close(private_fd)
            os.close(root_fd)

    def index_json(self, name: str) -> object:
        return loads_strict(self.index_bytes(name).decode("utf-8"))

    def index_jsonl(self, name: str) -> list[dict]:
        result: list[dict] = []
        for line_number, line in enumerate(self.index_bytes(name).decode("utf-8").splitlines(), 1):
            if not line.strip():
                continue
            value = loads_strict(line)
            if not isinstance(value, dict):
                raise ValueError(f"{name}:{line_number}: row must be an object")
            result.append(value)
        return result

    def index_digest(self, name: str) -> str:
        return hashlib.sha256(self.index_bytes(name)).hexdigest()

    def load_index(self) -> None:
        if not self.safe_layout():
            return
        try:
            manifest = self.index_json("manifest.json")
        except Exception as exc:
            self.err("/index/manifest.json", "index-read", str(exc))
            return
        required_manifest = {
            "schema_version",
            "run_salt",
            "cutoff_at",
            "cutoff_attestation",
            "retention",
            "source_contract_hash",
            "campaign_contract_hash",
            "exclusion_basis",
            "counts",
            "file_hashes",
            "corpus_hash",
        }
        if not isinstance(manifest, dict) or not self.exact_keys(manifest, required_manifest, "/index/manifest.json"):
            return
        if manifest.get("schema_version") != INDEX_SCHEMA or not HASH_RE.fullmatch(str(manifest.get("run_salt", ""))):
            self.err("/index/manifest.json", "schema", "invalid history index v2 manifest")
        if parse_time(manifest.get("cutoff_at")) is None:
            self.err("/index/manifest.json/cutoff_at", "invalid-timestamp", "cutoff must be timezone-aware")
        retention = manifest.get("retention")
        if not isinstance(retention, dict) or retention.get("disposition") not in {"delete-after-validation", "delete-by"}:
            self.err("/index/manifest.json/retention", "invalid-retention", "retention disposition is required")
        elif retention.get("disposition") == "delete-by":
            expires = parse_time(retention.get("expires_at"))
            if expires is None:
                self.err("/index/manifest.json/retention/expires_at", "invalid-timestamp", "expiry must be timezone-aware")
            elif expires <= datetime.now(timezone.utc):
                self.err("/index/manifest.json/retention", "retention-expired", "private index has reached its deletion deadline")
        file_hashes = manifest.get("file_hashes")
        if not isinstance(file_hashes, dict) or set(file_hashes) != PUBLIC_FILES or any(not HASH_RE.fullmatch(str(value)) for value in file_hashes.values()):
            self.err("/index/manifest.json/file_hashes", "index-file-set", "file hashes must cover the exact index file set")
            return
        # Names are now an exact constant set before any path is opened.
        for name in sorted(PUBLIC_FILES):
            actual = self.index_digest(name)
            if actual != file_hashes[name]:
                self.err(f"/index/{name}", "hash-mismatch", "indexed file hash changed")
        corpus_hash = manifest.get("corpus_hash")
        manifest_core = {key: value for key, value in manifest.items() if key != "corpus_hash"}
        expected_corpus = hashlib.sha256(canonical_json(manifest_core)).hexdigest()
        if corpus_hash != expected_corpus:
            self.err("/index/manifest.json/corpus_hash", "hash-mismatch", "manifest corpus hash does not reconcile")
        if not HASH_RE.fullmatch(str(manifest.get("source_contract_hash", ""))):
            self.err("/index/manifest.json/source_contract_hash", "schema", "source contract hash must be 64-hex")
        campaign_hash = manifest.get("campaign_contract_hash")
        basis = manifest.get("exclusion_basis")
        if campaign_hash is not None and not HASH_RE.fullmatch(str(campaign_hash)):
            self.err("/index/manifest.json/campaign_contract_hash", "schema", "campaign contract hash must be null or 64-hex")
        if basis not in {"trusted-cutoff", "campaign-and-cutoff"} or (basis == "trusted-cutoff") != (campaign_hash is None):
            self.err("/index/manifest.json/exclusion_basis", "schema", "exclusion basis and campaign hash disagree")
        attestation = manifest.get("cutoff_attestation")
        if not isinstance(attestation, dict) or set(attestation) != {"kind", "attested_at", "authority"} or attestation.get("kind") != "pre-discovery" or parse_time(attestation.get("attested_at")) is None or not isinstance(attestation.get("authority"), str) or not attestation["authority"].strip():
            self.err("/index/manifest.json/cutoff_attestation", "schema", "invalid cutoff attestation")

        try:
            source_rows = self.index_jsonl("source-ledger.jsonl")
        except Exception as exc:
            self.err("/index/source-ledger.jsonl", "index-read", str(exc))
            source_rows = []
        source_fields = {"source_id", "platform", "kind", "state", "origin", "record_count", "snapshot_hash"}
        for index, row in enumerate(source_rows):
            path = f"/index/source-ledger.jsonl/{index}"
            if not self.exact_keys(row, source_fields, path):
                continue
            source_id = row.get("source_id")
            if (
                not isinstance(source_id, str)
                or not ID_RE.fullmatch(source_id)
                or source_id in self.source_hash_by_id
                or not isinstance(row.get("platform"), str)
                or not ID_RE.fullmatch(row["platform"])
                or row.get("kind") != "normalized-jsonl"
                or row.get("state") not in {"live", "frozen"}
                or row.get("origin") not in {"local", "remote-snapshot"}
                or (row.get("origin") == "remote-snapshot" and row.get("state") != "frozen")
                or not isinstance(row.get("record_count"), int)
                or row["record_count"] < 0
                or not HASH_RE.fullmatch(str(row.get("snapshot_hash", "")))
            ):
                self.err(path, "invalid-source", "invalid source ledger row")
                continue
            self.source_hash_by_id[source_id] = row["snapshot_hash"]
            self.source_state_by_id[source_id] = row["state"]
            self.source_rows.append(row)

        counts_by_role = {"root": 0, "child": 0, "unresolved": 0}
        for filename, expected_role in (("roots.jsonl", "root"), ("children.jsonl", "child"), ("unresolved.jsonl", "unresolved")):
            try:
                rows = self.index_jsonl(filename)
            except Exception as exc:
                self.err(f"/index/{filename}", "index-read", str(exc))
                continue
            for index, row in enumerate(rows):
                path = f"/index/{filename}/{index}"
                self.exact_keys(row, RECORD_FIELDS, path)
                ident = row.get("record_id")
                if not isinstance(ident, str) or not RECORD_RE.fullmatch(ident) or ident in self.records:
                    self.err(f"{path}/record_id", "duplicate-record", f"invalid or duplicate record {ident!r}")
                    continue
                if row.get("role") != expected_role:
                    self.err(f"{path}/role", "role-mismatch", f"expected {expected_role}")
                if not isinstance(row.get("platform"), str) or not ID_RE.fullmatch(row["platform"]):
                    self.err(f"{path}/platform", "invalid-platform", "platform must be normalized")
                if parse_time(row.get("started_at")) is None:
                    self.err(f"{path}/started_at", "invalid-timestamp", "timestamp must be timezone-aware")
                parent = row.get("parent_record_id")
                if parent is not None and (not isinstance(parent, str) or not RECORD_RE.fullmatch(parent)):
                    self.err(f"{path}/parent_record_id", "invalid-parent", "parent must be an opaque record ID")
                if row.get("parent_resolution") not in {"none", "missing", "resolved"}:
                    self.err(f"{path}/parent_resolution", "invalid-parent", "invalid parent resolution")
                for field, pattern in DERIVED_RE.items():
                    value = row.get(field)
                    if value is not None and (not isinstance(value, str) or not pattern.fullmatch(value)):
                        self.err(f"{path}/{field}", "invalid-derived-id", f"invalid {field}")
                source_ids = row.get("source_ids")
                hashes = row.get("source_hashes")
                if not unique_string_list(source_ids, nonempty=True) or not isinstance(hashes, dict) or set(hashes) != set(source_ids):
                    self.err(f"{path}/source_ids", "invalid-source-map", "record source mapping is invalid")
                else:
                    for source_id in source_ids:
                        if self.source_hash_by_id.get(source_id) != hashes.get(source_id):
                            self.err(f"{path}/source_hashes", "unknown-source-hash", "record source hash does not match ledger")
                if row.get("recurrence_class") not in RECURRENCE_CLASSES or row.get("classification_basis") not in CLASSIFICATION_BASES:
                    self.err(path, "invalid-recurrence-class", "record needs a closed recurrence classification and basis")
                expected_eligible = expected_role == "root" and row.get("recurrence_class") == "user-intent" and row.get("classification_basis") == "reducer-reviewed"
                if row.get("eligible_for_recurrence") is not expected_eligible:
                    self.err(f"{path}/eligible_for_recurrence", "eligibility-mismatch", "included roots alone are recurrence eligible")
                self.records[ident] = row
                counts_by_role[expected_role] += 1

        try:
            exclusion_rows = self.index_jsonl("exclusion-ledger.jsonl")
        except Exception as exc:
            self.err("/index/exclusion-ledger.jsonl", "index-read", str(exc))
            exclusion_rows = []
        for index, row in enumerate(exclusion_rows):
            path = f"/index/exclusion-ledger.jsonl/{index}"
            self.exact_keys(row, {"record_id", "reasons"}, path)
            ident, reasons = row.get("record_id"), row.get("reasons")
            if not isinstance(ident, str) or not RECORD_RE.fullmatch(ident) or ident in self.excluded:
                self.err(f"{path}/record_id", "duplicate-exclusion", "exclusion IDs must be unique opaque IDs")
                continue
            if ident in self.records:
                self.err(f"{path}/record_id", "included-and-excluded", "record cannot be both included and excluded")
            if not unique_string_list(reasons, nonempty=True) or any(reason not in EXCLUSION_REASONS for reason in reasons):
                self.err(f"{path}/reasons", "invalid-exclusion", "invalid exclusion reasons")
            self.excluded.add(ident)

        try:
            private_rows = self.index_jsonl("private/native-map.jsonl")
        except Exception as exc:
            self.err("/index/private/native-map.jsonl", "index-read", str(exc))
            private_rows = []
        private_ids: set[str] = set()
        private_fields = {"record_id", "platform", "native_session_id", "native_aliases", "native_parent_id", "namespace", "observations"}
        observation_fields = {"source_id", "field_locator_hashes", "line", "path"}
        seen_observations: set[tuple[str, str, int]] = set()
        for index, row in enumerate(private_rows):
            path = f"/index/private/native-map.jsonl/{index}"
            self.exact_keys(row, private_fields, path)
            ident = row.get("record_id")
            if not isinstance(ident, str) or not RECORD_RE.fullmatch(ident) or ident in private_ids:
                self.err(f"{path}/record_id", "duplicate-private-record", "private record IDs must be unique")
                continue
            private_ids.add(ident)
            for field in ("native_session_id", "native_parent_id", "namespace"):
                value = row.get(field)
                if isinstance(value, str) and value:
                    self.native_values.add(value)
            aliases = row.get("native_aliases")
            if not isinstance(aliases, list):
                self.err(f"{path}/native_aliases", "invalid-private-row", "aliases must be an array")
                aliases = []
            for alias in aliases:
                if isinstance(alias, str) and alias:
                    self.native_values.add(alias)
            observations = row.get("observations")
            if not isinstance(observations, list) or not observations:
                self.err(f"{path}/observations", "invalid-private-row", "observations must be non-empty")
                continue
            for obs_index, observation in enumerate(observations):
                obs_path = f"{path}/observations/{obs_index}"
                if not isinstance(observation, dict) or not self.exact_keys(observation, observation_fields, obs_path):
                    continue
                source_id = observation.get("source_id")
                field_hashes = observation.get("field_locator_hashes")
                line = observation.get("line")
                source_path = observation.get("path")
                if (
                    source_id not in self.source_hash_by_id
                    or not isinstance(field_hashes, dict)
                    or not field_hashes
                    or any(field not in OBSERVATION_FIELDS or not HASH_RE.fullmatch(str(value)) for field, value in field_hashes.items())
                    or not isinstance(line, int)
                    or line < 1
                    or not isinstance(source_path, str)
                    or not source_path.startswith("/")
                ):
                    self.err(obs_path, "invalid-observation", "invalid private observation")
                    continue
                self.native_values.add(source_path)
                observation_key = (ident, source_id, line)
                if observation_key in seen_observations:
                    self.err(obs_path, "duplicate-observation", "record/source/line observations must be unique")
                    continue
                seen_observations.add(observation_key)
                self.private_observation_counts[source_id] = self.private_observation_counts.get(source_id, 0) + 1
                for field, locator_hash in field_hashes.items():
                    self.observations.setdefault((ident, source_id, field), set()).add((line, locator_hash))

        self.all_record_ids = set(self.records) | self.excluded
        if private_ids != self.all_record_ids:
            self.err("/index/private/native-map.jsonl", "private-map-mismatch", "private map must cover every included or excluded record exactly once")
        for record_id, row in self.records.items():
            observed_sources = {source_id for observed_record, source_id, _field in self.observations if observed_record == record_id}
            if observed_sources != set(row.get("source_ids", [])):
                self.err(f"/index/records/{record_id}/source_ids", "observation-source-mismatch", "public and private source observations disagree")
            parent = row.get("parent_record_id")
            if row.get("parent_resolution") == "resolved" and parent not in self.all_record_ids:
                self.err(f"/index/records/{record_id}/parent_record_id", "unknown-parent", "resolved parent is absent")

        declared = manifest.get("counts")
        self.manifest_counts = declared if isinstance(declared, dict) else {}
        expected_count_keys = {
            "source_observations",
            "duplicates_collapsed",
            "unique_sessions",
            "included_roots",
            "included_children",
            "included_unresolved",
            "primary_exclusions",
            "included_project_families",
        }
        if not isinstance(declared, dict) or set(declared) != expected_count_keys or any(not isinstance(value, int) or value < 0 for value in declared.values()):
            self.err("/index/manifest.json/counts", "accounting-mismatch", "manifest count schema is invalid")
            return
        actual = {
            "included_roots": counts_by_role["root"],
            "included_children": counts_by_role["child"],
            "included_unresolved": counts_by_role["unresolved"],
            "primary_exclusions": len(self.excluded),
            "included_project_families": len({row["project_family_hash"] for row in self.records.values() if row.get("role") == "root" and row.get("project_family_hash")}),
        }
        for key, value in actual.items():
            if declared.get(key) != value:
                self.err("/index/manifest.json/counts", "accounting-mismatch", f"{key} must equal {value}")
        if declared["unique_sessions"] != sum(value for key, value in actual.items() if key != "included_project_families"):
            self.err("/index/manifest.json/counts", "accounting-mismatch", "unique session accounting does not reconcile")
        if declared["source_observations"] != declared["duplicates_collapsed"] + declared["unique_sessions"]:
            self.err("/index/manifest.json/counts", "accounting-mismatch", "observation accounting does not reconcile")
        if declared["source_observations"] != sum(row["record_count"] for row in self.source_rows):
            self.err("/index/source-ledger.jsonl", "accounting-mismatch", "source record counts do not reconcile")
        if declared["source_observations"] != sum(self.private_observation_counts.values()):
            self.err("/index/private/native-map.jsonl", "accounting-mismatch", "private observation count does not reconcile")
        for row in self.source_rows:
            if self.private_observation_counts.get(row["source_id"], 0) != row["record_count"]:
                self.err(f"/index/source-ledger.jsonl/{row['source_id']}", "accounting-mismatch", "per-source private observation count does not reconcile")

    def validate_evidence(self) -> None:
        if not isinstance(self.evidence, dict):
            self.err("/evidence", "wrong-type", "evidence must be an object")
            return
        mode = self.evidence.get("mode")
        common = {"schema_version", "mode", "claims", "conflicts", "recurrence", "artifacts", "lineage_edges"}
        expected = common | ({"capability_inventory", "overlap_map", "decisions"} if mode == "workflow-mining" else {"lineage_scope"})
        self.exact_keys(self.evidence, expected, "/evidence")
        if self.evidence.get("schema_version") != EVIDENCE_SCHEMA:
            self.err("/evidence/schema_version", "schema", f"must equal {EVIDENCE_SCHEMA}")
        if mode not in {"lineage", "workflow-mining"}:
            self.err("/evidence/mode", "invalid-mode", "must be lineage or workflow-mining")

        artifacts = self.evidence.get("artifacts")
        if not isinstance(artifacts, list):
            self.err("/evidence/artifacts", "wrong-type", "artifacts must be an array")
            artifacts = []
        artifact_fields = {"id", "kind", "state", "snapshot_hash", "observed_at"}
        for index, artifact in enumerate(artifacts):
            path = f"/evidence/artifacts/{index}"
            if not isinstance(artifact, dict) or not self.exact_keys(artifact, artifact_fields, path):
                continue
            ident = artifact.get("id")
            if not isinstance(ident, str) or not ID_RE.fullmatch(ident) or ident in self.artifacts:
                self.err(f"{path}/id", "invalid-id", "artifact IDs must be unique normalized IDs")
                continue
            if artifact.get("kind") not in {"git-history", "artifact"} or artifact.get("state") not in {"live", "frozen"} or not HASH_RE.fullmatch(str(artifact.get("snapshot_hash", ""))) or parse_time(artifact.get("observed_at")) is None:
                self.err(path, "invalid-artifact", "artifact needs kind, state, hash, and observed_at")
            self.artifacts[ident] = artifact

        claims = self.evidence.get("claims")
        if not isinstance(claims, list) or not claims:
            self.err("/evidence/claims", "missing-field", "claims must be a non-empty array")
            claims = []
        claim_fields = {"id", "statement", "observed_at", "evidence"}
        for index, claim in enumerate(claims):
            path = f"/evidence/claims/{index}"
            if not isinstance(claim, dict) or not self.exact_keys(claim, claim_fields, path):
                continue
            ident = claim.get("id")
            if not isinstance(ident, str) or not ID_RE.fullmatch(ident) or ident in self.claim_ids:
                self.err(f"{path}/id", "invalid-id", "claim IDs must be unique normalized IDs")
                continue
            self.claim_ids.add(ident)
            self.claim_record_ids[ident] = set()
            self.claim_artifact_ids[ident] = set()
            self.claim_refs[ident] = []
            if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
                self.err(f"{path}/statement", "missing-field", "claim statement must be non-empty")
            if parse_time(claim.get("observed_at")) is None:
                self.err(f"{path}/observed_at", "invalid-timestamp", "claim needs timezone-aware observed_at")
            refs = claim.get("evidence")
            if not isinstance(refs, list) or not refs:
                self.err(f"{path}/evidence", "missing-evidence", "claim needs evidence")
                continue
            for ref_index, ref in enumerate(refs):
                ref_path = f"{path}/evidence/{ref_index}"
                if not isinstance(ref, dict):
                    self.err(ref_path, "wrong-type", "reference must be an object")
                    continue
                evidence_type = ref.get("evidence_type")
                if evidence_type == "agent-history":
                    self.exact_keys(ref, {"evidence_type", "record_id", "state", "locator"}, ref_path)
                    record_id = ref.get("record_id")
                    locator = ref.get("locator")
                    if not isinstance(record_id, str) or record_id not in self.records:
                        self.err(f"{ref_path}/record_id", "unknown-record", "record is unknown or excluded")
                    if ref.get("state") not in {"live", "frozen"}:
                        self.err(f"{ref_path}/state", "invalid-state", "invalid evidence state")
                    locator_fields = {"field", "ordinal", "source_id", "source_hash", "locator_hash"}
                    if not isinstance(locator, dict) or not self.exact_keys(locator, locator_fields, f"{ref_path}/locator"):
                        continue
                    source_id = locator.get("source_id")
                    ordinal = locator.get("ordinal")
                    locator_hash = locator.get("locator_hash")
                    locator_field = locator.get("field")
                    if not isinstance(locator_field, str) or locator_field not in OBSERVATION_FIELDS or not isinstance(ordinal, int) or ordinal < 1 or not HASH_RE.fullmatch(str(locator_hash)):
                        self.err(f"{ref_path}/locator", "invalid-locator", "invalid structured source locator")
                    if not isinstance(source_id, str) or self.source_hash_by_id.get(source_id) != locator.get("source_hash"):
                        self.err(f"{ref_path}/locator/source_hash", "unknown-source-hash", "source ID and hash do not match")
                    elif isinstance(record_id, str) and record_id in self.records and source_id not in self.records[record_id].get("source_ids", []):
                        self.err(f"{ref_path}/locator/source_id", "record-source-mismatch", "source did not observe record")
                    if not isinstance(source_id, str) or self.source_state_by_id.get(source_id) != ref.get("state"):
                        self.err(f"{ref_path}/state", "state-mismatch", "state must match source ledger")
                    if isinstance(record_id, str) and record_id in self.records and isinstance(source_id, str) and isinstance(locator_field, str) and (ordinal, locator_hash) not in self.observations.get((record_id, source_id, locator_field), set()):
                        self.err(f"{ref_path}/locator", "unobserved-locator", "locator does not match an indexed observation")
                    if record_id in self.records:
                        self.claim_record_ids[ident].add(record_id)
                elif isinstance(evidence_type, str) and evidence_type in {"git-history", "artifact"}:
                    self.exact_keys(ref, {"evidence_type", "artifact_id", "state", "locator"}, ref_path)
                    artifact_id = ref.get("artifact_id")
                    artifact = self.artifacts.get(artifact_id) if isinstance(artifact_id, str) else None
                    locator = ref.get("locator")
                    if artifact is None or artifact.get("kind") != evidence_type:
                        self.err(f"{ref_path}/artifact_id", "unknown-artifact", "reference must name an indexed artifact of matching kind")
                    if not isinstance(locator, dict) or not self.exact_keys(locator, {"field", "ordinal", "snapshot_hash"}, f"{ref_path}/locator"):
                        continue
                    if not isinstance(locator.get("field"), str) or not ID_RE.fullmatch(locator["field"]) or not isinstance(locator.get("ordinal"), int) or locator["ordinal"] < 0:
                        self.err(f"{ref_path}/locator", "invalid-locator", "artifact locator is invalid")
                    if artifact is not None and (locator.get("snapshot_hash") != artifact.get("snapshot_hash") or ref.get("state") != artifact.get("state")):
                        self.err(ref_path, "artifact-mismatch", "artifact state/hash mismatch")
                    if artifact is not None:
                        self.claim_artifact_ids[ident].add(artifact_id)
                else:
                    self.err(f"{ref_path}/evidence_type", "invalid-type", "invalid evidence type")
                self.claim_refs[ident].append(ref)

        conflicts = self.evidence.get("conflicts")
        if not isinstance(conflicts, list):
            self.err("/evidence/conflicts", "wrong-type", "conflicts must be an array")
        else:
            for index, conflict in enumerate(conflicts):
                path = f"/evidence/conflicts/{index}"
                if not isinstance(conflict, dict) or not self.exact_keys(conflict, {"claim_ids", "explanation"}, path):
                    continue
                ids = conflict.get("claim_ids")
                if not unique_string_list(ids) or len(ids) < 2 or any(ident not in self.claim_ids for ident in ids):
                    self.err(f"{path}/claim_ids", "invalid-conflict", "conflict needs distinct valid claims")
                if not isinstance(conflict.get("explanation"), str) or not conflict["explanation"].strip():
                    self.err(f"{path}/explanation", "missing-field", "conflict needs explanation")

        lineage_edges = self.evidence.get("lineage_edges")
        if not isinstance(lineage_edges, list):
            self.err("/evidence/lineage_edges", "wrong-type", "lineage_edges must be an array")
            lineage_edges = []
        edge_fields = {"id", "from", "to", "edge_type", "confidence", "evidence_claim_ids"}
        for index, edge in enumerate(lineage_edges):
            path = f"/evidence/lineage_edges/{index}"
            if not isinstance(edge, dict) or not self.exact_keys(edge, edge_fields, path):
                continue
            ident = edge.get("id")
            if not isinstance(ident, str) or not ID_RE.fullmatch(ident) or ident in self.lineage_edges:
                self.err(f"{path}/id", "invalid-id", "edge IDs must be unique normalized IDs")
                continue
            endpoints: list[tuple[str, str] | None] = []
            for endpoint_name in ("from", "to"):
                endpoint = edge.get(endpoint_name)
                endpoint_path = f"{path}/{endpoint_name}"
                if not isinstance(endpoint, dict) or not self.exact_keys(endpoint, {"kind", "id"}, endpoint_path):
                    endpoints.append(None)
                    continue
                kind, endpoint_id = endpoint.get("kind"), endpoint.get("id")
                if (
                    kind not in {"record", "artifact"}
                    or not isinstance(endpoint_id, str)
                    or (kind == "record" and endpoint_id not in self.records)
                    or (kind == "artifact" and endpoint_id not in self.artifacts)
                ):
                    self.err(endpoint_path, "invalid-lineage-edge", "endpoint must resolve to an included record or indexed artifact")
                    endpoints.append(None)
                else:
                    endpoints.append((kind, endpoint_id))
            if len(endpoints) == 2 and endpoints[0] is not None and endpoints[0] == endpoints[1]:
                self.err(path, "invalid-lineage-edge", "edge endpoints must be distinct")
            if edge.get("edge_type") not in {"native", "artifact", "heuristic"} or edge.get("confidence") not in {"high", "medium", "low"}:
                self.err(path, "invalid-lineage-edge", "edge needs type and confidence")
            if edge.get("edge_type") == "native":
                if (
                    len(endpoints) != 2
                    or endpoints[0] is None
                    or endpoints[1] is None
                    or endpoints[0][0] != "record"
                    or endpoints[1][0] != "record"
                    or self.records.get(endpoints[1][1], {}).get("parent_record_id") != endpoints[0][1]
                ):
                    self.err(path, "invalid-lineage-edge", "native edge must match an indexed record parent relationship")
            claim_ids = edge.get("evidence_claim_ids")
            if not unique_string_list(claim_ids, nonempty=True) or any(claim_id not in self.claim_ids for claim_id in claim_ids):
                self.err(f"{path}/evidence_claim_ids", "unknown-claim", "edge needs valid evidence claims")
            self.lineage_edges[ident] = edge

        if mode == "lineage":
            scope = self.evidence.get("lineage_scope")
            closure: set[str] = set()
            if not isinstance(scope, dict) or not self.exact_keys(scope, {"target_record_ids", "target_artifact_ids", "record_closure"}, "/evidence/lineage_scope"):
                self.err("/evidence/lineage_scope", "invalid-lineage-scope", "lineage mode needs an exact target and closure")
            else:
                target_records = scope.get("target_record_ids")
                target_artifacts = scope.get("target_artifact_ids")
                closure_values = scope.get("record_closure")
                if (
                    not unique_string_list(target_records)
                    or not unique_string_list(target_artifacts)
                    or not unique_string_list(closure_values)
                    or not target_records and not target_artifacts
                    or any(record_id not in self.records for record_id in target_records)
                    or any(artifact_id not in self.artifacts for artifact_id in target_artifacts)
                    or any(record_id not in self.records for record_id in closure_values)
                    or not set(target_records).issubset(set(closure_values))
                ):
                    self.err("/evidence/lineage_scope", "invalid-lineage-scope", "targets and closure must resolve to included records or indexed artifacts")
                grounded_artifacts = set().union(*self.claim_artifact_ids.values()) if self.claim_artifact_ids else set()
                if not set(target_artifacts).issubset(grounded_artifacts):
                    self.err("/evidence/lineage_scope/target_artifact_ids", "ungrounded-lineage-target", "every artifact target must be grounded by a claim")
                closure = set(closure_values)
                adjacency: dict[str, set[str]] = {record_id: set() for record_id in self.records}
                for record_id, row in self.records.items():
                    parent = row.get("parent_record_id")
                    if parent in self.records:
                        adjacency[record_id].add(parent)
                        adjacency[parent].add(record_id)
                expected_closure: set[str] = set()
                pending = list(target_records)
                while pending:
                    record_id = pending.pop()
                    if record_id in expected_closure:
                        continue
                    expected_closure.add(record_id)
                    pending.extend(adjacency.get(record_id, set()) - expected_closure)
                if closure != expected_closure:
                    self.err("/evidence/lineage_scope/record_closure", "lineage-mismatch", "record closure must be the complete connected native lineage of every record target")
            expected_native_edges = {
                (row["parent_record_id"], record_id)
                for record_id, row in self.records.items()
                if record_id in closure and row.get("parent_record_id") in closure
            }
            declared_native_edges = {
                (edge.get("from", {}).get("id"), edge.get("to", {}).get("id"))
                for edge in self.lineage_edges.values()
                if edge.get("edge_type") == "native" and isinstance(edge.get("from"), dict) and isinstance(edge.get("to"), dict)
            }
            if declared_native_edges != expected_native_edges:
                self.err("/evidence/lineage_edges", "lineage-mismatch", "native edges must exactly cover the declared record closure")

        recurrence = self.evidence.get("recurrence")
        if not isinstance(recurrence, list):
            self.err("/evidence/recurrence", "wrong-type", "recurrence must be an array")
            recurrence = []
        recurrence_by_candidate: dict[str, dict] = {}
        eligible_intent_count_by_candidate: dict[str, int] = {}
        recurrence_fields = {"candidate_id", "support_record_ids", "root_intent_count", "project_family_count", "evidence_claim_ids"}
        for index, item in enumerate(recurrence):
            path = f"/evidence/recurrence/{index}"
            if not isinstance(item, dict) or not self.exact_keys(item, recurrence_fields, path):
                continue
            candidate_id = item.get("candidate_id")
            if not isinstance(candidate_id, str) or not ID_RE.fullmatch(candidate_id) or candidate_id in recurrence_by_candidate:
                self.err(f"{path}/candidate_id", "duplicate-candidate", "candidate IDs must be unique normalized IDs")
                continue
            recurrence_by_candidate[candidate_id] = item
            supports = item.get("support_record_ids")
            if not unique_string_list(supports):
                self.err(f"{path}/support_record_ids", "duplicate-support", "supports must be a unique array")
                supports = []
            eligible: set[str] = set()
            intents: set[str] = set()
            families: set[str] = set()
            for support_index, record_id in enumerate(supports):
                record = self.records.get(record_id)
                if record is None or record.get("role") != "root" or not record.get("eligible_for_recurrence"):
                    self.err(f"{path}/support_record_ids/{support_index}", "ineligible-support", "only eligible roots may support recurrence")
                elif not record.get("root_intent_hash"):
                    self.err(f"{path}/support_record_ids/{support_index}", "empty-intent", "support root needs intent hash")
                else:
                    eligible.add(record_id)
                    intents.add(record["root_intent_hash"])
                    if record.get("project_family_hash"):
                        families.add(record["project_family_hash"])
            if len(intents) != len(eligible):
                self.err(f"{path}/support_record_ids", "duplicate-intent", "support roots need distinct normalized intents")
            eligible_intent_count_by_candidate[candidate_id] = len(intents)
            if item.get("root_intent_count") != len(intents) or item.get("project_family_count") != len(families):
                self.err(path, "recurrence-mismatch", "intent and project-family counts must reconcile")
            evidence_claims = item.get("evidence_claim_ids")
            if not unique_string_list(evidence_claims, nonempty=True) or any(claim_id not in self.claim_ids for claim_id in evidence_claims):
                self.err(f"{path}/evidence_claim_ids", "unknown-claim", "recurrence needs valid evidence claims")
            else:
                grounded = set().union(*(self.claim_record_ids.get(claim_id, set()) for claim_id in evidence_claims))
                if not eligible.issubset(grounded):
                    self.err(f"{path}/evidence_claim_ids", "ungrounded-recurrence", "claims must ground every supporting root")

        if mode == "workflow-mining":
            inventory = self.evidence.get("capability_inventory")
            if not isinstance(inventory, list) or not inventory:
                self.err("/evidence/capability_inventory", "missing-field", "workflow mining needs capability inventory")
                inventory = []
            for index, item in enumerate(inventory):
                path = f"/evidence/capability_inventory/{index}"
                if not isinstance(item, dict) or not self.exact_keys(item, {"id", "name", "kind", "snapshot_hash"}, path):
                    continue
                ident = item.get("id")
                if not isinstance(ident, str) or not ID_RE.fullmatch(ident) or ident in self.capability_ids:
                    self.err(f"{path}/id", "invalid-capability", "capability ID must be unique")
                    continue
                self.capability_ids.add(ident)
                if not isinstance(item.get("name"), str) or not item["name"].strip() or item.get("kind") not in {"skill", "plugin", "agent", "script", "workflow"} or not HASH_RE.fullmatch(str(item.get("snapshot_hash", ""))):
                    self.err(path, "invalid-capability", "invalid capability")
            overlaps = self.evidence.get("overlap_map")
            if not isinstance(overlaps, list) or not overlaps:
                self.err("/evidence/overlap_map", "missing-field", "workflow mining needs overlap map")
                overlaps = []
            overlap_by_id: dict[str, dict] = {}
            candidate_overlap: set[str] = set()
            overlap_fields = {"id", "candidate_id", "matched_capability_ids", "assessment", "rationale", "evidence_claim_ids"}
            for index, item in enumerate(overlaps):
                path = f"/evidence/overlap_map/{index}"
                if not isinstance(item, dict) or not self.exact_keys(item, overlap_fields, path):
                    continue
                ident, candidate_id = item.get("id"), item.get("candidate_id")
                if not isinstance(ident, str) or not ID_RE.fullmatch(ident) or ident in overlap_by_id or not isinstance(candidate_id, str) or not ID_RE.fullmatch(candidate_id) or candidate_id in candidate_overlap:
                    self.err(path, "duplicate-overlap", "overlap and candidate IDs must be unique")
                    continue
                overlap_by_id[ident] = item
                candidate_overlap.add(candidate_id)
                self.overlap_ids.add(ident)
                matches = item.get("matched_capability_ids")
                assessment = item.get("assessment")
                if not unique_string_list(matches) or any(match not in self.capability_ids for match in matches):
                    self.err(f"{path}/matched_capability_ids", "unknown-capability", "invalid capability matches")
                    matches = []
                if assessment not in {"none", "partial", "substantial"} or not isinstance(item.get("rationale"), str) or not item["rationale"].strip() or (assessment == "none") != (not matches):
                    self.err(path, "invalid-overlap", "assessment, rationale, and matches disagree")
                refs = item.get("evidence_claim_ids")
                if not unique_string_list(refs, nonempty=True) or any(ref not in self.claim_ids for ref in refs):
                    self.err(f"{path}/evidence_claim_ids", "unknown-claim", "overlap needs valid claims")
            decisions = self.evidence.get("decisions")
            if not isinstance(decisions, list) or not decisions:
                self.err("/evidence/decisions", "missing-field", "workflow mining needs decisions")
                decisions = []
            seen_decisions: set[str] = set()
            decision_fields = {"candidate_id", "decision", "recurrence_candidate_id", "overlap_id", "evidence_claim_ids"}
            for index, decision in enumerate(decisions):
                path = f"/evidence/decisions/{index}"
                if not isinstance(decision, dict) or not self.exact_keys(decision, decision_fields, path):
                    continue
                candidate_id = decision.get("candidate_id")
                if not isinstance(candidate_id, str) or not ID_RE.fullmatch(candidate_id) or candidate_id in seen_decisions:
                    self.err(f"{path}/candidate_id", "duplicate-decision", "one decision is allowed per candidate")
                    continue
                seen_decisions.add(candidate_id)
                self.decision_candidate_ids.add(candidate_id)
                if decision.get("decision") not in {"create", "extend", "reject"}:
                    self.err(f"{path}/decision", "invalid-decision", "invalid decision")
                recurrence_item = recurrence_by_candidate.get(candidate_id)
                if decision.get("recurrence_candidate_id") != candidate_id or recurrence_item is None:
                    self.err(f"{path}/recurrence_candidate_id", "missing-recurrence", "decision must reference its recurrence")
                overlap = overlap_by_id.get(decision.get("overlap_id"))
                if overlap is None or overlap.get("candidate_id") != candidate_id:
                    self.err(f"{path}/overlap_id", "missing-overlap", "decision must reference its unique overlap")
                refs = decision.get("evidence_claim_ids")
                recurrence_claims = (recurrence_item or {}).get("evidence_claim_ids", [])
                overlap_claims = (overlap or {}).get("evidence_claim_ids", [])
                required_claims = (
                    set(recurrence_claims) if unique_string_list(recurrence_claims) else set()
                ) | (
                    set(overlap_claims) if unique_string_list(overlap_claims) else set()
                )
                if not unique_string_list(refs, nonempty=True) or any(ref not in self.claim_ids for ref in refs) or not required_claims.issubset(set(refs)):
                    self.err(f"{path}/evidence_claim_ids", "ungrounded-decision", "decision needs recurrence and overlap evidence")
                if decision.get("decision") in {"create", "extend"} and eligible_intent_count_by_candidate.get(candidate_id, 0) < 3:
                    self.err(path, "insufficient-recurrence", "create or extend needs three independent intents")
            candidate_sets = (set(recurrence_by_candidate), candidate_overlap, seen_decisions)
            if not (candidate_sets[0] == candidate_sets[1] == candidate_sets[2]):
                self.err("/evidence", "orphan-candidate", "every workflow candidate needs exactly one recurrence, overlap, and decision")

    def scan_publication(self) -> None:
        if not isinstance(self.publication, dict):
            self.err("/publication", "wrong-type", "publication must be an object")
            return
        mode = self.publication.get("mode")
        common = {
            "schema_version",
            "mode",
            "summary",
            "claim_ids",
            "record_ids",
            "artifact_ids",
            "counts",
            "source_manifest",
            "provenance_ledger",
            "state_labels",
        }
        expected = common | ({"lineage_edge_ids", "lineage_scope"} if mode == "lineage" else {"capability_ids", "overlap_ids", "decision_candidate_ids"})
        self.exact_keys(self.publication, expected, "/publication")
        if self.publication.get("schema_version") != PUBLICATION_SCHEMA:
            self.err("/publication/schema_version", "schema", f"must equal {PUBLICATION_SCHEMA}")
        if mode not in {"lineage", "workflow-mining"} or mode != (self.evidence.get("mode") if isinstance(self.evidence, dict) else None):
            self.err("/publication/mode", "invalid-mode", "publication mode must match evidence")
        if not isinstance(self.publication.get("summary"), str) or not self.publication["summary"].strip():
            self.err("/publication/summary", "missing-field", "publication needs summary")
        claim_ids = self.publication.get("claim_ids")
        if not unique_string_list(claim_ids, nonempty=True) or any(claim_id not in self.claim_ids for claim_id in claim_ids):
            self.err("/publication/claim_ids", "unknown-claim", "publication needs unique validated claims")
            claim_ids = []
        required_records = set().union(*(self.claim_record_ids.get(claim_id, set()) for claim_id in claim_ids)) if claim_ids else set()
        required_artifacts = set().union(*(self.claim_artifact_ids.get(claim_id, set()) for claim_id in claim_ids)) if claim_ids else set()
        record_ids, artifact_ids = self.publication.get("record_ids"), self.publication.get("artifact_ids")
        if not unique_string_list(record_ids) or set(record_ids) != required_records:
            self.err("/publication/record_ids", "ungrounded-publication", "record IDs must exactly match published claim support")
        if not unique_string_list(artifact_ids) or set(artifact_ids) != required_artifacts:
            self.err("/publication/artifact_ids", "ungrounded-publication", "artifact IDs must exactly match published claim support")
        expected_counts = {
            "roots": self.manifest_counts.get("included_roots"),
            "children": self.manifest_counts.get("included_children"),
            "unresolved": self.manifest_counts.get("included_unresolved"),
            "excluded": self.manifest_counts.get("primary_exclusions"),
            "project_families": self.manifest_counts.get("included_project_families"),
        }
        if self.publication.get("counts") != expected_counts:
            self.err("/publication/counts", "accounting-mismatch", f"must equal {expected_counts}")
        expected_sources = [
            {"source_id": row["source_id"], "snapshot_hash": row["snapshot_hash"], "state": row["state"], "origin": row["origin"]}
            for row in sorted(self.source_rows, key=lambda item: item["source_id"])
        ]
        if self.publication.get("source_manifest") != expected_sources:
            self.err("/publication/source_manifest", "source-manifest-mismatch", "source manifest must exactly match the index")
        expected_provenance = [
            {"claim_id": claim_id, "reference_count": len(self.claim_refs.get(claim_id, []))}
            for claim_id in sorted(claim_ids)
        ]
        if self.publication.get("provenance_ledger") != expected_provenance:
            self.err("/publication/provenance_ledger", "provenance-mismatch", "provenance ledger must reconcile published claims")
        states = {"live": 0, "frozen": 0}
        for claim_id in claim_ids:
            for ref in self.claim_refs.get(claim_id, []):
                if ref.get("state") in states:
                    states[ref["state"]] += 1
        if self.publication.get("state_labels") != states:
            self.err("/publication/state_labels", "state-mismatch", "state label counts must reconcile claim references")
        if mode == "lineage":
            if self.publication.get("lineage_scope") != (self.evidence.get("lineage_scope") if isinstance(self.evidence, dict) else None):
                self.err("/publication/lineage_scope", "lineage-mismatch", "publication lineage scope must match validated evidence")
            scope = self.evidence.get("lineage_scope", {}) if isinstance(self.evidence, dict) else {}
            if isinstance(scope, dict):
                target_records = scope.get("target_record_ids")
                target_artifacts = scope.get("target_artifact_ids")
                if unique_string_list(target_records) and unique_string_list(target_artifacts) and (
                    not set(target_records).issubset(required_records)
                    or not set(target_artifacts).issubset(required_artifacts)
                ):
                    self.err("/publication/lineage_scope", "ungrounded-lineage-target", "lineage targets must be supported by published claims")
            edge_ids = self.publication.get("lineage_edge_ids")
            if not unique_string_list(edge_ids) or set(edge_ids) != set(self.lineage_edges):
                self.err("/publication/lineage_edge_ids", "lineage-mismatch", "publication must report the complete validated lineage")
        elif mode == "workflow-mining":
            capability_ids = self.publication.get("capability_ids")
            overlap_ids = self.publication.get("overlap_ids")
            decision_ids = self.publication.get("decision_candidate_ids")
            if not unique_string_list(capability_ids) or set(capability_ids) != self.capability_ids:
                self.err("/publication/capability_ids", "capability-mismatch", "publication must report complete capability inventory")
            if not unique_string_list(overlap_ids) or set(overlap_ids) != self.overlap_ids:
                self.err("/publication/overlap_ids", "overlap-mismatch", "publication must report complete overlap map")
            if not unique_string_list(decision_ids) or set(decision_ids) != self.decision_candidate_ids:
                self.err("/publication/decision_candidate_ids", "decision-mismatch", "publication must report every candidate decision")

        def scan_string(value: str, path: str, *, check_native: bool = True) -> None:
            if URL_RE.search(value) or URI_SCHEME_RE.search(value):
                self.err(path, "url-leak", "publication contains a URL or private URI")
            if ABS_PATH_RE.search(value) or WINDOWS_PATH_RE.search(value):
                self.err(path, "path-leak", "publication contains an absolute machine path")
            if SECRET_RE.search(value) or JWT_RE.search(value):
                self.err(path, "secret-leak", "publication contains credential-like content")
            if EMAIL_RE.search(value) or PHONE_RE.search(value):
                self.err(path, "personal-data-leak", "publication contains email or phone-like personal data")
            if check_native:
                for native in self.native_values:
                    if native and native in value:
                        self.err(path, "native-id-leak", "publication contains a private native identifier or path")
                        break
            for opaque_id in OPAQUE_RE.findall(value):
                if opaque_id not in self.records:
                    self.err(path, "unknown-opaque-id", f"unknown opaque identifier {opaque_id}")

        def walk(value: object, path: str) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    scan_string(str(key), f"{path}/<key>", check_native=False)
                    walk(child, f"{path}/{key}")
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    walk(child, f"{path}/{index}")
            elif isinstance(value, str):
                scan_string(value, path)

        walk(self.publication, "/publication")

    def validate(self) -> list[dict[str, str]]:
        self.load_index()
        self.validate_evidence()
        self.scan_publication()
        return sorted(self.errors, key=lambda error: (error["path"], error["code"], error["message"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--publication", type=Path, required=True)
    args = parser.parse_args()
    try:
        evidence = read_json(args.evidence)
        publication = read_json(args.publication)
        errors = Validator(args.index, evidence, publication).validate()
    except Exception as exc:
        errors = [{"path": "/", "code": "read-error", "message": str(exc)}]
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
