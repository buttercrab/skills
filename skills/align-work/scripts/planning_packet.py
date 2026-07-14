#!/usr/bin/env python3
"""Create and guard align-work planning packets."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import struct
import sys
import uuid


EXIT_INVALID = 3
EXIT_CONFLICT = 4
EXIT_UNSAFE = 5
EXIT_IO = 6

TASK_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
QUESTION_ID_RE = re.compile(r"^Q-[0-9]{3,}$")
HEX_RE = re.compile(r"^[0-9a-f]{64}$")
MARKER_RE = re.compile(r"^<!-- align-work-attempt (\{.*\}) -->$")
TEMPLATE_RE = re.compile(r"\{\{[^{}]+\}\}")
AUTHORITY_CLASS_RE = re.compile(r"^(?:P|R|T|I|G|E|D)(?:[0-9]+)?$")
DRAFT_MARKER = "<!-- align-work-required-content -->"

PROTECTED = ("decisions.md", "facts.md", "plan.md")
STATUSES = {
    "discovery",
    "drafting",
    "reviewing",
    "awaiting_approval",
    "approved",
    "executing",
    "verifying",
    "needs_reapproval",
    "blocked",
    "paused",
    "complete",
    "cancelled",
    "invalid",
}
EXECUTION_STATUSES = {"executing", "verifying", "needs_reapproval", "blocked", "complete"}
ATTEMPT_STATUSES = {"started", "passed", "failed", "blocked", "rolled_back", "skipped"}
STATE_FIELDS = {
    "schema_version",
    "packet_id",
    "repository_root",
    "task_id",
    "packet_revision",
    "protected_digest",
    "status",
    "open_question_ids",
    "active_coordinator",
    "coordinator_history",
    "state_generation",
    "resume_status",
    "requested_authority_classes",
    "runtime_authorization_evidence",
    "rollback_mode",
    "execution_head",
    "pending_execution_hash",
    "approval",
    "last_transition_at",
}
APPROVAL_FIELDS = {
    "id",
    "packet_id",
    "repository_root",
    "packet_revision",
    "protected_digest",
    "authority_classes",
    "portable",
    "user_evidence",
    "recorded_at",
    "partial_work_disposition",
}
COORDINATOR_EVENT_FIELDS = {"event", "from", "to", "recorded_at", "evidence", "disposition"}
ATTEMPT_FIELDS = {
    "attempt_id",
    "packet_id",
    "packet_revision",
    "protected_digest",
    "approval_id",
    "previous_hash",
    "step_id",
    "actor_id",
    "model",
    "status",
    "started_at",
    "ended_at",
    "actions",
    "mutations",
    "evidence",
    "verification",
    "disposition",
    "entry_hash",
}
ALLOWED_TRANSITIONS = {
    "discovery": {"drafting", "paused", "cancelled"},
    "drafting": {"reviewing", "awaiting_approval", "paused", "cancelled"},
    "reviewing": {"drafting", "awaiting_approval", "paused", "cancelled"},
    "awaiting_approval": {"discovery", "drafting", "approved", "paused", "cancelled"},
    "approved": {"executing", "needs_reapproval", "paused", "cancelled"},
    "executing": {"verifying", "needs_reapproval", "blocked", "paused", "cancelled"},
    "needs_reapproval": {"approved", "executing", "drafting", "cancelled"},
    "verifying": {"complete", "executing", "needs_reapproval", "blocked", "paused"},
    "blocked": set(),
    "paused": set(),
    "complete": set(),
    "cancelled": set(),
    "invalid": set(),
}


class PacketError(Exception):
    def __init__(self, code: int, invariant: str, expected=None, observed=None):
        super().__init__(invariant)
        self.code = code
        self.invariant = invariant
        self.expected = expected
        self.observed = observed


def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def as_uuid(value: str, field: str) -> str:
    try:
        return str(uuid.UUID(value))
    except (ValueError, AttributeError) as exc:
        raise PacketError(EXIT_INVALID, f"{field} must be a UUID", "UUID", value) from exc


def parse_time(value: object, field: str) -> None:
    if not isinstance(value, str):
        raise PacketError(EXIT_INVALID, f"{field} must be RFC3339 text", "string", type(value).__name__)
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PacketError(EXIT_INVALID, f"{field} must be RFC3339", "timestamp with offset", value) from exc
    if parsed.tzinfo is None:
        raise PacketError(EXIT_INVALID, f"{field} needs a timezone offset", "timezone-aware", value)


def parse_classes(value: str | None) -> list[str]:
    if not value:
        return []
    items = [part.strip() for part in value.split(",") if part.strip()]
    if not items or len(items) != len(set(items)):
        raise PacketError(EXIT_INVALID, "authority classes must be nonempty and unique", "comma-separated unique values", value)
    invalid = [item for item in items if not AUTHORITY_CLASS_RE.fullmatch(item)]
    if invalid:
        raise PacketError(EXIT_INVALID, "unknown authority class", AUTHORITY_CLASS_RE.pattern, invalid)
    return sorted(items)


def success(command: str, **fields) -> None:
    payload = {"command": command, "ok": True, **fields}
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def fail(command: str, error: PacketError) -> int:
    payload = {
        "command": command,
        "ok": False,
        "invariant": error.invariant,
        "expected": error.expected,
        "observed": error.observed,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=sys.stderr)
    return error.code


def _lstat_regular(path: Path, required: bool = True) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        if required:
            raise PacketError(EXIT_UNSAFE, "required packet file is missing", str(path), "missing")
        return
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise PacketError(EXIT_UNSAFE, "packet file must be a regular non-symlink", "regular file", str(path))
    if info.st_nlink != 1:
        raise PacketError(EXIT_UNSAFE, "packet file must not be hard-linked", "link count 1", {"path": str(path), "links": info.st_nlink})


def packet_path(value: str | Path, require_state: bool = True) -> Path:
    raw = Path(value).expanduser().absolute()
    for path in (raw.parent, raw):
        if path.is_symlink():
            raise PacketError(EXIT_UNSAFE, "planning paths may not be symlinks", "real directory", str(path))
    try:
        packet = raw.resolve(strict=True)
    except OSError as exc:
        raise PacketError(EXIT_UNSAFE, "packet path cannot be resolved safely", "existing real path", str(raw)) from exc
    if packet.parent.name != ".planning":
        raise PacketError(EXIT_UNSAFE, "packet must be <repo>/.planning/<task-id>", ".planning parent", str(packet))
    if not packet.is_dir():
        raise PacketError(EXIT_UNSAFE, "packet directory is missing", str(packet), "missing")
    if require_state:
        _lstat_regular(packet / "state.json")
    return packet


def read_json(path: Path) -> dict:
    _lstat_regular(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PacketError(EXIT_INVALID, "JSON file is unreadable", "valid UTF-8 JSON", str(path)) from exc
    if not isinstance(value, dict):
        raise PacketError(EXIT_INVALID, "JSON root must be an object", "object", type(value).__name__)
    return value


def atomic_json(path: Path, value: dict) -> None:
    data = (json.dumps(value, indent=2, sort_keys=False) + "\n").encode("utf-8")
    temp = path.parent / f".{path.name}.tmp.{os.getpid()}.{uuid.uuid4()}"
    fd = None
    try:
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb", closefd=True) as handle:
            fd = None
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if os.environ.get("ALIGN_WORK_TEST_CRASH") == "before-replace":
            raise OSError("injected crash before replace")
        if path.exists():
            os.chmod(temp, stat.S_IMODE(path.stat().st_mode))
        else:
            os.chmod(temp, 0o644)
        os.replace(temp, path)
        if os.environ.get("ALIGN_WORK_TEST_CRASH") == "after-replace":
            raise OSError("injected crash after replace")
        dir_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except OSError as exc:
        if fd is not None:
            os.close(fd)
        with contextlib.suppress(FileNotFoundError):
            temp.unlink()
        raise PacketError(EXIT_IO, "atomic state write failed", str(path), str(exc)) from exc


@contextlib.contextmanager
def packet_lock(packet: Path):
    lock = packet / ".state.lock"
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(lock, flags, 0o600)
    except OSError as exc:
        raise PacketError(EXIT_UNSAFE, "lock file cannot be opened safely", "single-link regular file", str(lock)) from exc
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise PacketError(EXIT_UNSAFE, "lock file must be a single-link regular file", "regular file with link count 1", str(lock))
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def compute_digest(packet: Path) -> str:
    digest = hashlib.sha256()
    for name in PROTECTED:
        path = packet / name
        _lstat_regular(path)
        name_bytes = name.encode("utf-8")
        data = path.read_bytes()
        digest.update(b"align-work-packet-v1\0")
        digest.update(struct.pack(">Q", len(name_bytes)))
        digest.update(name_bytes)
        digest.update(struct.pack(">Q", len(data)))
        digest.update(data)
    return digest.hexdigest()


def _validate_coordinator(value: object) -> None:
    if value is None:
        return
    if not isinstance(value, dict) or set(value) != {"id", "epoch"}:
        raise PacketError(EXIT_INVALID, "active_coordinator schema is invalid", ["epoch", "id"], value)
    as_uuid(value["id"], "active_coordinator.id")
    if type(value["epoch"]) is not int or value["epoch"] < 1:
        raise PacketError(EXIT_INVALID, "coordinator epoch must be positive", ">=1", value["epoch"])


def _validate_coordinator_history(events: object, active: object) -> None:
    if not isinstance(events, list):
        raise PacketError(EXIT_INVALID, "coordinator_history must be an array", "array", type(events).__name__)
    for index, event in enumerate(events):
        if not isinstance(event, dict) or set(event) != COORDINATOR_EVENT_FIELDS:
            raise PacketError(EXIT_INVALID, "coordinator history event schema is invalid", sorted(COORDINATOR_EVENT_FIELDS), {"index": index, "event": event})
        if event["event"] not in {"claim", "handoff", "recover"}:
            raise PacketError(EXIT_INVALID, "unknown coordinator event", ["claim", "handoff", "recover"], event["event"])
        _validate_coordinator(event["from"])
        _validate_coordinator(event["to"])
        if event["to"] is None:
            raise PacketError(EXIT_INVALID, "coordinator event needs destination", "coordinator", event)
        parse_time(event["recorded_at"], "coordinator_history.recorded_at")
        if event["evidence"] is not None and not isinstance(event["evidence"], str):
            raise PacketError(EXIT_INVALID, "coordinator evidence must be text or null", "text or null", event["evidence"])
        if not isinstance(event["disposition"], str) or not event["disposition"].strip():
            raise PacketError(EXIT_INVALID, "coordinator disposition must be nonempty text", "nonempty text", event["disposition"])
        source = event["from"]
        destination = event["to"]
        if event["event"] == "claim":
            if source is not None or destination["epoch"] != 1:
                raise PacketError(EXIT_INVALID, "claim must start an unowned epoch-1 chain", {"from": None, "to_epoch": 1}, event)
        elif source is None or destination["epoch"] != source["epoch"] + 1:
            raise PacketError(EXIT_INVALID, "handoff/recover must increment the prior coordinator epoch", "to.epoch = from.epoch + 1", event)
        if index and source != events[index - 1]["to"]:
            raise PacketError(EXIT_INVALID, "coordinator history is disconnected", events[index - 1]["to"], source)
    if events:
        if active != events[-1]["to"]:
            raise PacketError(EXIT_INVALID, "active coordinator differs from history head", events[-1]["to"], active)
    elif active is not None and active["epoch"] != 1:
        raise PacketError(EXIT_INVALID, "coordinator epoch above one requires history", "history ending at active coordinator", active)


def validate_state(state: dict, packet: Path) -> None:
    unknown = set(state) - STATE_FIELDS
    missing = STATE_FIELDS - set(state)
    if unknown or missing:
        raise PacketError(EXIT_INVALID, "state fields do not match schema", sorted(STATE_FIELDS), {"missing": sorted(missing), "unknown": sorted(unknown)})
    if type(state["schema_version"]) is not int or state["schema_version"] != 1:
        raise PacketError(EXIT_INVALID, "unsupported schema_version", 1, state["schema_version"])
    as_uuid(state["packet_id"], "packet_id")
    expected_root = str(packet.parent.parent)
    if state["repository_root"] != expected_root:
        raise PacketError(EXIT_UNSAFE, "packet moved to a different repository", state["repository_root"], expected_root)
    if not isinstance(state["task_id"], str) or not TASK_ID_RE.fullmatch(state["task_id"]):
        raise PacketError(EXIT_INVALID, "invalid task_id", TASK_ID_RE.pattern, state["task_id"])
    if state["task_id"] != packet.name:
        raise PacketError(EXIT_INVALID, "packet directory must match task_id", packet.name, state["task_id"])
    for field in ("packet_revision", "state_generation"):
        if type(state[field]) is not int or state[field] < 0:
            raise PacketError(EXIT_INVALID, f"{field} must be nonnegative", ">=0", state[field])
    if state["status"] not in STATUSES:
        raise PacketError(EXIT_INVALID, "unknown status", sorted(STATUSES), state["status"])
    if state["protected_digest"] is not None and (not isinstance(state["protected_digest"], str) or not HEX_RE.fullmatch(state["protected_digest"])):
        raise PacketError(EXIT_INVALID, "protected_digest must be null or lowercase SHA-256", "64 lowercase hex", state["protected_digest"])
    if not isinstance(state["open_question_ids"], list) or len(state["open_question_ids"]) != len(set(state["open_question_ids"])):
        raise PacketError(EXIT_INVALID, "open_question_ids must be a unique array", "unique array", state["open_question_ids"])
    for item in state["open_question_ids"]:
        if not isinstance(item, str) or not QUESTION_ID_RE.fullmatch(item):
            raise PacketError(EXIT_INVALID, "invalid open question ID", QUESTION_ID_RE.pattern, item)
    _validate_coordinator(state["active_coordinator"])
    _validate_coordinator_history(state["coordinator_history"], state["active_coordinator"])
    if state["resume_status"] is not None and state["resume_status"] not in STATUSES - {"paused", "blocked", "invalid"}:
        raise PacketError(EXIT_INVALID, "invalid resume_status", "safe status or null", state["resume_status"])
    if state["status"] not in {"paused", "blocked"} and state["resume_status"] is not None:
        raise PacketError(EXIT_INVALID, "resume_status only belongs to paused/blocked", None, state["resume_status"])
    for field in ("requested_authority_classes",):
        if not isinstance(state[field], list) or any(not isinstance(x, str) or not AUTHORITY_CLASS_RE.fullmatch(x) for x in state[field]) or sorted(set(state[field])) != state[field]:
            raise PacketError(EXIT_INVALID, f"{field} must be sorted known authority classes", AUTHORITY_CLASS_RE.pattern, state[field])
    if state["runtime_authorization_evidence"] is not None and not isinstance(state["runtime_authorization_evidence"], str):
        raise PacketError(EXIT_INVALID, "runtime_authorization_evidence must be text or null", "string or null", state["runtime_authorization_evidence"])
    if not isinstance(state["rollback_mode"], bool):
        raise PacketError(EXIT_INVALID, "rollback_mode must be boolean", "boolean", state["rollback_mode"])
    if state["execution_head"] is not None and (not isinstance(state["execution_head"], str) or not HEX_RE.fullmatch(state["execution_head"])):
        raise PacketError(EXIT_INVALID, "execution_head must be null or SHA-256", "64 lowercase hex", state["execution_head"])
    if state["pending_execution_hash"] is not None and (not isinstance(state["pending_execution_hash"], str) or not HEX_RE.fullmatch(state["pending_execution_hash"])):
        raise PacketError(EXIT_INVALID, "pending_execution_hash must be null or SHA-256", "64 lowercase hex", state["pending_execution_hash"])
    rollback_status_ok = state["status"] in {"executing", "verifying"} or (
        state["status"] in {"paused", "blocked"}
        and state["resume_status"] in {"executing", "verifying"}
    )
    if state["rollback_mode"] and not rollback_status_ok:
        raise PacketError(EXIT_INVALID, "rollback_mode is valid only during active or paused rollback", "executing/verifying or paused/blocked resume", state["status"])
    if state["status"] in {"approved", "executing", "verifying", "complete"} and state["approval"] is None and not state["rollback_mode"]:
        raise PacketError(EXIT_INVALID, "active or completed execution needs approval record", "approval object", None)
    if state["status"] in {"executing", "verifying"} and (not isinstance(state["runtime_authorization_evidence"], str) or not state["runtime_authorization_evidence"].strip()):
        raise PacketError(EXIT_INVALID, "active execution needs runtime authorization evidence", "nonempty text", state["runtime_authorization_evidence"])
    parse_time(state["last_transition_at"], "last_transition_at")
    validate_approval(state)


def validate_approval(state: dict) -> None:
    approval = state["approval"]
    if approval is None:
        return
    if not isinstance(approval, dict) or set(approval) != APPROVAL_FIELDS:
        raise PacketError(EXIT_INVALID, "approval schema is invalid", sorted(APPROVAL_FIELDS), approval)
    as_uuid(approval["id"], "approval.id")
    if approval["packet_id"] != state["packet_id"]:
        raise PacketError(EXIT_INVALID, "approval packet identity mismatch", state["packet_id"], approval["packet_id"])
    if approval["repository_root"] != state["repository_root"]:
        raise PacketError(EXIT_INVALID, "approval repository identity mismatch", state["repository_root"], approval["repository_root"])
    if approval["packet_revision"] != state["packet_revision"]:
        raise PacketError(EXIT_INVALID, "approval revision is stale", state["packet_revision"], approval["packet_revision"])
    if approval["protected_digest"] != state["protected_digest"]:
        raise PacketError(EXIT_INVALID, "approval digest is stale", state["protected_digest"], approval["protected_digest"])
    if approval["portable"] is not False:
        raise PacketError(EXIT_INVALID, "approval must be nonportable", False, approval["portable"])
    authorities = approval["authority_classes"]
    if not isinstance(authorities, list) or not authorities or sorted(set(authorities)) != authorities or any(not isinstance(x, str) or not AUTHORITY_CLASS_RE.fullmatch(x) for x in authorities):
        raise PacketError(EXIT_INVALID, "approval authority must be sorted known values", AUTHORITY_CLASS_RE.pattern, authorities)
    if authorities != state["requested_authority_classes"]:
        raise PacketError(EXIT_INVALID, "approval authority differs from requested authority", state["requested_authority_classes"], authorities)
    if not isinstance(approval["user_evidence"], str) or not approval["user_evidence"].strip():
        raise PacketError(EXIT_INVALID, "approval needs user evidence", "nonempty text", approval["user_evidence"])
    if approval["partial_work_disposition"] is not None and (
        not isinstance(approval["partial_work_disposition"], str)
        or not approval["partial_work_disposition"].strip()
    ):
        raise PacketError(EXIT_INVALID, "partial_work_disposition must be nonempty text or null", "nonempty string or null", approval["partial_work_disposition"])
    parse_time(approval["recorded_at"], "approval.recorded_at")


def validate_markdown(packet: Path, state: dict) -> None:
    requirements = {
        "facts.md": ("# Facts:", "## Observed facts", "## Inferences", "## Unknowns"),
        "decisions.md": ("# Decisions:", "## Confirmed decisions", "## Open questions", "## Alignment rounds"),
        "plan.md": ("# Plan:", "## Outcome", "## Consumed facts and decisions", "## Scope and authority", "## Implementation sequence", "## Acceptance gates", "## Risks and rollback", "## Approval"),
    }
    task_marker = f"Task ID: `{state['task_id']}`"
    for name, headings in requirements.items():
        path = packet / name
        _lstat_regular(path)
        text = path.read_text(encoding="utf-8")
        if TEMPLATE_RE.search(text):
            raise PacketError(EXIT_INVALID, "protected file contains unresolved template marker", "no {{...}} marker", name)
        if task_marker not in text:
            raise PacketError(EXIT_INVALID, "protected file task ID mismatch", task_marker, name)
        for heading in headings:
            if heading == "## Open questions" and not state["open_question_ids"]:
                continue
            if heading.startswith("## "):
                label = re.escape(heading.removeprefix("## "))
                label_patterns = {
                    "## Inferences": r"(?:Inferences|Design inferences)(?:\s+[^\n]*)?",
                    "## Unknowns": r"(?:Unknowns|Known unknowns)(?:\s+[^\n]*)?",
                    "## Alignment rounds": r"(?:Alignment rounds|Alignment-round ledger)(?:\s+[^\n]*)?",
                }
                suffix = label_patterns.get(heading, rf"{label}(?:\s+[^\n]*)?")
                pattern = rf"(?m)^## (?:[0-9]+\. )?{suffix}$"
            else:
                pattern = rf"(?m)^{re.escape(heading)}(?:\s+[^\n]*)?$"
            if not re.search(pattern, text):
                raise PacketError(EXIT_INVALID, "protected file lacks required heading", heading, name)


def canonical_json(value: dict) -> bytes:
    # ASCII escaping keeps every execution marker on one physical line even
    # when payload text contains Unicode line/paragraph separators.
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def attempt_hash(payload: dict) -> str:
    return hashlib.sha256(b"align-work-execution-v1\0" + canonical_json(payload)).hexdigest()


def validate_attempt_record(record: object) -> dict:
    if not isinstance(record, dict) or set(record) != ATTEMPT_FIELDS:
        raise PacketError(EXIT_INVALID, "execution record schema is invalid", sorted(ATTEMPT_FIELDS), record)
    as_uuid(record["attempt_id"], "attempt_id")
    as_uuid(record["packet_id"], "attempt.packet_id")
    if type(record["packet_revision"]) is not int or record["packet_revision"] < 1:
        raise PacketError(EXIT_INVALID, "execution packet_revision must be positive", ">=1", record["packet_revision"])
    if not isinstance(record["protected_digest"], str) or not HEX_RE.fullmatch(record["protected_digest"]):
        raise PacketError(EXIT_INVALID, "execution protected_digest is invalid", "SHA-256", record["protected_digest"])
    if record["approval_id"] is not None:
        as_uuid(record["approval_id"], "attempt.approval_id")
    for field in ("step_id", "actor_id", "model"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise PacketError(EXIT_INVALID, f"execution {field} must be nonempty text", "nonempty text", record[field])
        if record[field].splitlines() != [record[field]]:
            raise PacketError(EXIT_INVALID, f"execution {field} must be single-line text", "single-line text", record[field])
    if record["status"] not in ATTEMPT_STATUSES:
        raise PacketError(EXIT_INVALID, "unknown execution status", sorted(ATTEMPT_STATUSES), record["status"])
    for field in ("started_at", "ended_at"):
        parse_time(record[field], field)
    started = dt.datetime.fromisoformat(record["started_at"].replace("Z", "+00:00"))
    ended = dt.datetime.fromisoformat(record["ended_at"].replace("Z", "+00:00"))
    if ended < started:
        raise PacketError(EXIT_INVALID, "execution timestamps are reversed", "ended_at >= started_at", {"started_at": record["started_at"], "ended_at": record["ended_at"]})
    for field in ("actions", "mutations", "evidence"):
        if not isinstance(record[field], list) or any(not isinstance(item, str) or not item.strip() for item in record[field]):
            raise PacketError(EXIT_INVALID, f"execution {field} must be nonempty strings", "string array", record[field])
    for field in ("verification", "disposition"):
        if record[field] is not None and not isinstance(record[field], str):
            raise PacketError(EXIT_INVALID, f"execution {field} must be text or null", "text or null", record[field])
    if record["previous_hash"] is not None and (not isinstance(record["previous_hash"], str) or not HEX_RE.fullmatch(record["previous_hash"])):
        raise PacketError(EXIT_INVALID, "execution previous_hash is invalid", "null or SHA-256", record["previous_hash"])
    if not isinstance(record["entry_hash"], str) or not HEX_RE.fullmatch(record["entry_hash"]):
        raise PacketError(EXIT_INVALID, "execution entry_hash is invalid", "SHA-256", record["entry_hash"])
    return record


def parse_execution(packet: Path, state: dict, enforce_head: bool = True) -> tuple[list[dict], str | None]:
    path = packet / "execution.md"
    if not path.exists():
        if state["execution_head"] is not None or state["status"] in EXECUTION_STATUSES:
            raise PacketError(EXIT_INVALID, "execution ledger is required", "execution.md", state["status"])
        return [], None
    _lstat_regular(path)
    records: list[dict] = []
    dangling_marker = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if "<!-- align-work-attempt" not in line:
            continue
        match = MARKER_RE.fullmatch(line)
        if not match:
            dangling_marker = True
            continue
        try:
            record = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise PacketError(EXIT_INVALID, "execution marker contains invalid JSON", "valid JSON", line) from exc
        validate_attempt_record(record)
        entry = record["entry_hash"]
        payload = {key: value for key, value in record.items() if key != "entry_hash"}
        if not isinstance(entry, str) or attempt_hash(payload) != entry:
            raise PacketError(EXIT_INVALID, "execution record hash mismatch", attempt_hash(payload), entry)
        expected_previous = records[-1]["entry_hash"] if records else None
        if payload.get("previous_hash") != expected_previous:
            raise PacketError(EXIT_INVALID, "execution chain previous_hash mismatch", expected_previous, payload.get("previous_hash"))
        if any(existing["entry_hash"] == entry for existing in records):
            raise PacketError(EXIT_INVALID, "duplicate execution hash", "unique entry hashes", entry)
        records.append(record)
    if dangling_marker:
        raise PacketError(EXIT_INVALID, "execution ledger contains a torn marker", "complete marker", str(path))
    head = records[-1]["entry_hash"] if records else None
    if enforce_head and head != state["execution_head"]:
        raise PacketError(EXIT_INVALID, "execution head mismatch", state["execution_head"], head)
    return records, head


def validate_packet(packet: Path, state: dict, enforce_digest: bool = True) -> str | None:
    validate_state(state, packet)
    validate_markdown(packet, state)
    actual = compute_digest(packet)
    if enforce_digest and state["protected_digest"] is not None and actual != state["protected_digest"]:
        raise PacketError(EXIT_INVALID, "protected digest mismatch", state["protected_digest"], actual)
    if state["status"] in {"awaiting_approval", "approved", "executing", "verifying", "needs_reapproval", "blocked", "complete"} and state["protected_digest"] is None:
        raise PacketError(EXIT_INVALID, "sealed status requires protected_digest", "SHA-256", None)
    parse_execution(packet, state, enforce_head=True)
    if state["status"] == "invalid":
        raise PacketError(EXIT_INVALID, "packet is marked invalid", "guarded repair", "invalid")
    return actual


def load_packet(value: str | Path) -> tuple[Path, dict]:
    packet = packet_path(value)
    state = read_json(packet / "state.json")
    return packet, state


def guard(state: dict, args) -> None:
    if state["packet_revision"] != args.expected_revision:
        raise PacketError(EXIT_CONFLICT, "stale packet revision", state["packet_revision"], args.expected_revision)
    coordinator = state["active_coordinator"]
    if coordinator is None:
        raise PacketError(EXIT_CONFLICT, "packet has no active coordinator", "claim first", None)
    if coordinator["epoch"] != args.expected_epoch:
        raise PacketError(EXIT_CONFLICT, "stale coordinator epoch", coordinator["epoch"], args.expected_epoch)
    if state["state_generation"] != args.expected_generation:
        raise PacketError(EXIT_CONFLICT, "stale state generation", state["state_generation"], args.expected_generation)
    requested = as_uuid(args.coordinator_id, "coordinator-id")
    if coordinator["id"] != requested:
        raise PacketError(EXIT_CONFLICT, "coordinator is not active owner", coordinator["id"], requested)


def bump_generation(state: dict) -> None:
    state["state_generation"] += 1
    state["last_transition_at"] = now()


def template_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "packet-templates"


def render_template(name: str, values: dict[str, str]) -> str:
    text = (template_dir() / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    if TEMPLATE_RE.search(text):
        raise PacketError(EXIT_INVALID, "template has unresolved marker", "all markers rendered", name)
    return text


def command_init(args) -> None:
    if not TASK_ID_RE.fullmatch(args.task_id):
        raise PacketError(EXIT_UNSAFE, "unsafe task-id", TASK_ID_RE.pattern, args.task_id)
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir() or repo.is_symlink():
        raise PacketError(EXIT_UNSAFE, "repo must be a real directory", "non-symlink directory", str(repo))
    planning = repo / ".planning"
    if planning.exists() and planning.is_symlink():
        raise PacketError(EXIT_UNSAFE, ".planning may not be a symlink", "real directory", str(planning))
    planning.mkdir(mode=0o755, exist_ok=True)
    packet = planning / args.task_id
    coordinator = as_uuid(args.coordinator_id, "coordinator-id") if args.coordinator_id else str(uuid.uuid4())
    created = now()
    title = args.title or args.task_id.replace("-", " ")
    packet_id = str(uuid.uuid4())
    values = {
        "TASK_ID": args.task_id,
        "TITLE": title,
        "CREATED_AT": created,
        "COORDINATOR_ID": coordinator,
        "PACKET_ID": packet_id,
        "REPOSITORY_ROOT": str(repo),
    }
    try:
        packet.mkdir(mode=0o755)
        for name in ("facts.md", "decisions.md", "plan.md"):
            (packet / name).write_text(render_template(name, values), encoding="utf-8")
        state = {
            "schema_version": 1,
            "packet_id": packet_id,
            "repository_root": str(repo),
            "task_id": args.task_id,
            "packet_revision": 0,
            "protected_digest": None,
            "status": "discovery",
            "open_question_ids": [],
            "active_coordinator": {"id": coordinator, "epoch": 1},
            "coordinator_history": [],
            "state_generation": 0,
            "resume_status": None,
            "requested_authority_classes": [],
            "runtime_authorization_evidence": None,
            "rollback_mode": False,
            "execution_head": None,
            "pending_execution_hash": None,
            "approval": None,
            "last_transition_at": created,
        }
        atomic_json(packet / "state.json", state)
        validate_packet(packet, state)
    except Exception:
        if packet.exists():
            shutil.rmtree(packet)
        raise
    success("init", packet=str(packet), coordinator_id=coordinator, epoch=1, revision=0)


def command_validate(args) -> None:
    packet, state = load_packet(args.packet)
    actual = validate_packet(packet, state)
    success("validate", packet=str(packet), valid=True, status=state["status"], revision=state["packet_revision"], digest=actual)


def command_seal(args) -> None:
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_state(state, packet)
        guard(state, args)
        if state["status"] not in {"discovery", "drafting", "reviewing"}:
            raise PacketError(EXIT_INVALID, "seal source must be an active planning state", ["discovery", "drafting", "reviewing"], state["status"])
        validate_markdown(packet, state)
        parse_execution(packet, state, enforce_head=True)
        incomplete = [name for name in PROTECTED if DRAFT_MARKER in (packet / name).read_text(encoding="utf-8")]
        if incomplete:
            raise PacketError(EXIT_INVALID, "protected files still contain required-content markers", "remove markers after authoring real content", incomplete)
        if args.status not in {"drafting", "reviewing", "awaiting_approval"}:
            raise PacketError(EXIT_INVALID, "seal target must be a planning state", ["drafting", "reviewing", "awaiting_approval"], args.status)
        authorities = parse_classes(args.authority)
        if args.status == "awaiting_approval":
            if state["open_question_ids"]:
                raise PacketError(EXIT_INVALID, "open questions block approval", [], state["open_question_ids"])
            if not authorities:
                raise PacketError(EXIT_INVALID, "awaiting approval requires authority classes", "nonempty --authority", authorities)
        state["packet_revision"] += 1
        state["protected_digest"] = compute_digest(packet)
        state["status"] = args.status
        state["requested_authority_classes"] = authorities
        state["approval"] = None
        state["runtime_authorization_evidence"] = None
        state["rollback_mode"] = False
        state["resume_status"] = None
        bump_generation(state)
        atomic_json(packet / "state.json", state)
    success("seal", packet=str(packet), revision=state["packet_revision"], digest=state["protected_digest"], status=state["status"], authority=authorities)


def command_repair(args) -> None:
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_state(state, packet)
        guard(state, args)
        if args.status not in {"drafting", "reviewing"}:
            raise PacketError(EXIT_INVALID, "repair target must be drafting/reviewing", ["drafting", "reviewing"], args.status)
        validate_markdown(packet, state)
        actual_digest = compute_digest(packet)
        digest_changed = state["protected_digest"] is not None and actual_digest != state["protected_digest"]
        records, actual_head = parse_execution(packet, state, enforce_head=False)
        pending = state["pending_execution_hash"]
        execution_repaired = False
        if pending is not None and actual_head == state["execution_head"]:
            state["pending_execution_hash"] = None
            execution_repaired = True
        elif pending is not None and actual_head == pending:
            prior = records[-2]["entry_hash"] if len(records) > 1 else None
            if prior != state["execution_head"]:
                raise PacketError(EXIT_INVALID, "pending execution tail does not extend current head", state["execution_head"], prior)
            state["execution_head"] = actual_head
            state["pending_execution_hash"] = None
            execution_repaired = True
        elif actual_head != state["execution_head"]:
            raise PacketError(EXIT_INVALID, "execution repair requires matching pending hash", pending, actual_head)
        if not digest_changed and not execution_repaired and state["status"] != "invalid":
            raise PacketError(EXIT_INVALID, "repair requires a recognized digest, invalid-state, or pending-attempt fault", "repairable fault", "valid packet")
        state["packet_revision"] += 1
        state["protected_digest"] = actual_digest
        state["status"] = args.status
        state["approval"] = None
        state["requested_authority_classes"] = []
        state["runtime_authorization_evidence"] = None
        state["rollback_mode"] = False
        state["resume_status"] = None
        bump_generation(state)
        atomic_json(packet / "state.json", state)
    success("repair", packet=str(packet), revision=state["packet_revision"], digest=state["protected_digest"], status=state["status"], execution_head=state["execution_head"])


def coordinator_event(event: str, old, new, evidence: str | None, disposition: str) -> dict:
    return {"event": event, "from": old, "to": new, "recorded_at": now(), "evidence": evidence, "disposition": disposition}


def command_claim(args) -> None:
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_packet(packet, state)
        if state["packet_revision"] != args.expected_revision or state["state_generation"] != args.expected_generation:
            raise PacketError(EXIT_CONFLICT, "stale claim state", {"revision": state["packet_revision"], "generation": state["state_generation"]}, {"revision": args.expected_revision, "generation": args.expected_generation})
        if state["active_coordinator"] is not None:
            raise PacketError(EXIT_CONFLICT, "packet already has a coordinator", None, state["active_coordinator"])
        coordinator = as_uuid(args.coordinator_id, "coordinator-id") if args.coordinator_id else str(uuid.uuid4())
        new = {"id": coordinator, "epoch": 1}
        state["active_coordinator"] = new
        state["coordinator_history"].append(coordinator_event("claim", None, new, args.evidence, "claimed unowned packet"))
        bump_generation(state)
        atomic_json(packet / "state.json", state)
    success("claim", packet=str(packet), coordinator=new)


def command_handoff(args) -> None:
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_packet(packet, state)
        guard(state, args)
        new_id = as_uuid(args.to_coordinator_id, "to-coordinator-id") if args.to_coordinator_id else str(uuid.uuid4())
        old = dict(state["active_coordinator"])
        new = {"id": new_id, "epoch": old["epoch"] + 1}
        state["active_coordinator"] = new
        state["coordinator_history"].append(coordinator_event("handoff", old, new, args.evidence, "orderly handoff"))
        if state["status"] in {"executing", "verifying"}:
            state["resume_status"] = state["status"]
            state["status"] = "paused"
        state["runtime_authorization_evidence"] = None
        bump_generation(state)
        validate_packet(packet, state)
        atomic_json(packet / "state.json", state)
    success("handoff", packet=str(packet), coordinator=new)


def command_recover(args) -> None:
    if not args.evidence.strip():
        raise PacketError(EXIT_INVALID, "recover requires user takeover/reauthorization evidence", "nonempty --evidence", args.evidence)
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_state(state, packet)
        if state["active_coordinator"] is None:
            raise PacketError(EXIT_CONFLICT, "unowned packet must be claimed, not recovered", "claim command", None)
        expected = {"revision": state["packet_revision"], "epoch": state["active_coordinator"]["epoch"], "generation": state["state_generation"]}
        observed = {"revision": args.expected_revision, "epoch": args.expected_epoch, "generation": args.expected_generation}
        if expected != observed:
            raise PacketError(EXIT_CONFLICT, "stale recovery fence", expected, observed)
        old = dict(state["active_coordinator"])
        new_id = as_uuid(args.new_coordinator_id, "new-coordinator-id") if args.new_coordinator_id else str(uuid.uuid4())
        new = {"id": new_id, "epoch": old["epoch"] + 1}
        state["active_coordinator"] = new
        state["coordinator_history"].append(coordinator_event("recover", old, new, args.evidence, "user-mediated recovery"))
        if state["status"] in {"executing", "verifying"}:
            state["resume_status"] = state["status"]
            state["status"] = "paused"
        state["runtime_authorization_evidence"] = None
        bump_generation(state)
        validate_packet(packet, state)
        atomic_json(packet / "state.json", state)
    success("recover", packet=str(packet), coordinator=new)


def ensure_execution_file(packet: Path, state: dict) -> None:
    path = packet / "execution.md"
    if path.exists():
        _lstat_regular(path)
        return
    plan_first = (packet / "plan.md").read_text(encoding="utf-8").splitlines()[0]
    title = plan_first.removeprefix("# Plan:").strip() or state["task_id"].replace("-", " ")
    values = {"TASK_ID": state["task_id"], "TITLE": title, "CREATED_AT": now(), "COORDINATOR_ID": state["active_coordinator"]["id"]}
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(render_template("execution.md", values))
        handle.flush()
        os.fsync(handle.fileno())


def transition_authorization(state: dict, args, *, allow_reuse: bool, context: str) -> str:
    if args.reuse_approval and args.authorization_evidence is not None:
        raise PacketError(
            EXIT_INVALID,
            "approval reuse conflicts with fresh authorization evidence",
            "exactly one of --reuse-approval or --authorization-evidence",
            "both supplied",
        )
    if args.reuse_approval:
        if not allow_reuse or state["approval"] is None or state["rollback_mode"]:
            raise PacketError(
                EXIT_INVALID,
                "approval reuse needs a valid active approval outside rollback",
                "valid approval and non-rollback execution",
                {"approval": state["approval"], "rollback_mode": state["rollback_mode"]},
            )
        return "approval:" + state["approval"]["id"]
    if not args.authorization_evidence or not args.authorization_evidence.strip():
        raise PacketError(
            EXIT_INVALID,
            context,
            "--authorization-evidence or --reuse-approval",
            None,
        )
    return args.authorization_evidence.strip()


def command_transition(args) -> None:
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_packet(packet, state)
        guard(state, args)
        current = state["status"]
        target = args.to
        authorization_transition = (
            target == "executing" and current in {"approved", "needs_reapproval"}
        ) or (
            current in {"paused", "blocked"} and target in {"executing", "verifying"}
        )
        if (args.reuse_approval or args.authorization_evidence is not None) and not authorization_transition:
            raise PacketError(
                EXIT_INVALID,
                "execution authorization flags are invalid for this transition",
                "approved/needs_reapproval to executing or paused/blocked active resume",
                f"{current}->{target}",
            )
        if current in {"paused", "blocked"}:
            if target != state["resume_status"]:
                raise PacketError(EXIT_INVALID, "paused/blocked may resume only to recorded status", state["resume_status"], target)
        elif target not in ALLOWED_TRANSITIONS[current]:
            raise PacketError(EXIT_INVALID, "illegal state transition", sorted(ALLOWED_TRANSITIONS[current]), f"{current}->{target}")
        if target in {"drafting", "reviewing", "awaiting_approval"} and state["open_question_ids"]:
            raise PacketError(EXIT_INVALID, "open questions block planning advancement", [], state["open_question_ids"])
        if target == "approved":
            if not args.approval_id or not args.approval_evidence or not args.approval_evidence.strip():
                raise PacketError(EXIT_INVALID, "approval transition needs ID and evidence", "--approval-id and --approval-evidence", None)
            authorities = parse_classes(args.authority)
            if authorities != state["requested_authority_classes"] or not authorities:
                raise PacketError(EXIT_INVALID, "approved authority must equal requested authority", state["requested_authority_classes"], authorities)
            if current == "needs_reapproval" and (
                not args.partial_work_disposition or not args.partial_work_disposition.strip()
            ):
                raise PacketError(EXIT_INVALID, "reapproval requires partial-work disposition", "--partial-work-disposition", None)
            state["approval"] = {
                "id": as_uuid(args.approval_id, "approval-id"),
                "packet_id": state["packet_id"],
                "repository_root": state["repository_root"],
                "packet_revision": state["packet_revision"],
                "protected_digest": state["protected_digest"],
                "authority_classes": authorities,
                "portable": False,
                "user_evidence": args.approval_evidence,
                "recorded_at": now(),
                "partial_work_disposition": args.partial_work_disposition,
            }
        if target == "executing":
            if current == "approved":
                if args.rollback or args.partial_work_disposition:
                    raise PacketError(EXIT_INVALID, "rollback flags are valid only from needs_reapproval", "no rollback flags", current)
                state["runtime_authorization_evidence"] = transition_authorization(
                    state,
                    args,
                    allow_reuse=True,
                    context="execution needs current user authorization or trusted same-task approval reuse",
                )
                state["rollback_mode"] = False
            elif current == "needs_reapproval":
                if (
                    not args.rollback
                    or not args.partial_work_disposition
                    or not args.partial_work_disposition.strip()
                ):
                    raise PacketError(EXIT_INVALID, "needs_reapproval may execute only an authorized recorded rollback", "--rollback, --partial-work-disposition, and --authorization-evidence", None)
                rollback_authorization = transition_authorization(
                    state,
                    args,
                    allow_reuse=False,
                    context="rollback needs current user authorization evidence",
                )
                state["runtime_authorization_evidence"] = (
                    rollback_authorization
                    + " | partial-work disposition: "
                    + args.partial_work_disposition.strip()
                )
                state["rollback_mode"] = True
            ensure_execution_file(packet, state)
        if current in {"paused", "blocked"} and target in {"executing", "verifying"}:
            state["runtime_authorization_evidence"] = transition_authorization(
                state,
                args,
                allow_reuse=True,
                context="resuming active work needs current user authorization or trusted same-task approval reuse",
            )
        if target == "needs_reapproval":
            # A material discovery may happen after approval but before execution.
            # Create the ledger here as well so every needs-reapproval packet has
            # a durable place for partial-effect and rollback receipts.
            ensure_execution_file(packet, state)
            state["approval"] = None
            state["runtime_authorization_evidence"] = None
            state["rollback_mode"] = False
        if target in {"paused", "blocked"}:
            state["resume_status"] = current
        elif current in {"paused", "blocked"}:
            state["resume_status"] = None
        if target in {"complete", "cancelled"}:
            if target == "complete":
                records, _ = parse_execution(packet, state, enforce_head=True)
                current_receipt = bool(
                    records
                    and records[-1]["packet_id"] == state["packet_id"]
                    and records[-1]["packet_revision"] == state["packet_revision"]
                    and records[-1]["protected_digest"] == state["protected_digest"]
                    and state["approval"] is not None
                    and records[-1]["approval_id"] == state["approval"]["id"]
                )
                if state["rollback_mode"] or not current_receipt or records[-1]["status"] != "passed" or not records[-1]["verification"]:
                    raise PacketError(EXIT_INVALID, "completion requires a current-revision passed verification receipt outside rollback", "last execution record matches packet identity/revision/digest and passed with verification text", records[-1] if records else None)
            state["runtime_authorization_evidence"] = None
            if target == "cancelled":
                state["rollback_mode"] = False
        state["status"] = target
        bump_generation(state)
        validate_packet(packet, state)
        atomic_json(packet / "state.json", state)
    success("transition", packet=str(packet), previous=current, status=target, revision=state["packet_revision"], epoch=state["active_coordinator"]["epoch"], generation=state["state_generation"])


def command_questions(args) -> None:
    questions = sorted(set(args.set or []))
    for item in questions:
        if not QUESTION_ID_RE.fullmatch(item):
            raise PacketError(EXIT_INVALID, "invalid open question ID", QUESTION_ID_RE.pattern, item)
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_packet(packet, state)
        guard(state, args)
        if state["status"] not in {"discovery", "drafting", "reviewing"}:
            raise PacketError(EXIT_INVALID, "questions may change only during alignment/planning", ["discovery", "drafting", "reviewing"], state["status"])
        state["open_question_ids"] = questions
        bump_generation(state)
        atomic_json(packet / "state.json", state)
    success("questions", packet=str(packet), open_question_ids=questions, generation=state["state_generation"])


def command_record_attempt(args) -> None:
    if args.status not in ATTEMPT_STATUSES:
        raise PacketError(EXIT_INVALID, "unknown attempt status", sorted(ATTEMPT_STATUSES), args.status)
    packet = packet_path(args.packet)
    with packet_lock(packet):
        state = read_json(packet / "state.json")
        validate_packet(packet, state)
        guard(state, args)
        attempt_states = {"executing", "verifying"}
        if state["status"] not in attempt_states:
            raise PacketError(EXIT_INVALID, "attempts require active authorized execution state", sorted(attempt_states), state["status"])
        if state["pending_execution_hash"] is not None:
            raise PacketError(EXIT_INVALID, "pending execution receipt requires repair", None, state["pending_execution_hash"])
        ensure_execution_file(packet, state)
        records, head = parse_execution(packet, state, enforce_head=True)
        started = args.started_at or now()
        ended = args.ended_at or now()
        parse_time(started, "started_at")
        parse_time(ended, "ended_at")
        payload = {
            "attempt_id": str(uuid.uuid4()),
            "packet_id": state["packet_id"],
            "packet_revision": state["packet_revision"],
            "protected_digest": state["protected_digest"],
            "approval_id": state["approval"]["id"] if state["approval"] is not None else None,
            "previous_hash": head,
            "step_id": args.step_id,
            "actor_id": args.actor_id,
            "model": args.model,
            "status": args.status,
            "started_at": started,
            "ended_at": ended,
            "actions": args.action or [],
            "mutations": args.mutation or [],
            "evidence": args.evidence or [],
            "verification": args.verification,
            "disposition": args.disposition,
        }
        entry = attempt_hash(payload)
        record = {**payload, "entry_hash": entry}
        validate_attempt_record(record)
        title = f"\n## {args.step_id} — {args.status}\n\n"
        details = f"- Attempt: `{payload['attempt_id']}`\n- Actor: `{args.actor_id}`\n- Model: `{args.model}`\n- Started: {started}\n- Ended: {ended}\n\n"
        marker = "<!-- align-work-attempt " + canonical_json(record).decode("utf-8") + " -->\n"
        path = packet / "execution.md"
        state["pending_execution_hash"] = entry
        bump_generation(state)
        atomic_json(packet / "state.json", state)
        flags = os.O_WRONLY | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(path, flags)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            os.close(fd)
            raise PacketError(EXIT_UNSAFE, "execution ledger must be a single-link regular file", "regular file with link count 1", str(path))
        with os.fdopen(fd, "a", encoding="utf-8") as handle:
            handle.write(title + details + marker)
            handle.flush()
            os.fsync(handle.fileno())
        state["execution_head"] = entry
        state["pending_execution_hash"] = None
        bump_generation(state)
        atomic_json(packet / "state.json", state)
    success("record-attempt", packet=str(packet), attempt_id=payload["attempt_id"], entry_hash=entry, previous_hash=head)


def add_fence(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--expected-revision", type=int, required=True)
    parser.add_argument("--expected-epoch", type=int, required=True)
    parser.add_argument("--expected-generation", type=int, required=True)
    parser.add_argument("--coordinator-id", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--repo", required=True)
    init.add_argument("--task-id", required=True)
    init.add_argument("--title")
    init.add_argument("--coordinator-id")
    init.set_defaults(func=command_init)

    validate = sub.add_parser("validate")
    validate.add_argument("packet")
    validate.set_defaults(func=command_validate)

    for name, func in (("seal", command_seal), ("repair", command_repair)):
        item = sub.add_parser(name)
        item.add_argument("packet")
        add_fence(item)
        item.add_argument("--status", required=True)
        if name == "seal":
            item.add_argument("--authority")
        item.set_defaults(func=func)

    claim = sub.add_parser("claim")
    claim.add_argument("packet")
    claim.add_argument("--expected-revision", type=int, required=True)
    claim.add_argument("--expected-generation", type=int, required=True)
    claim.add_argument("--coordinator-id")
    claim.add_argument("--evidence")
    claim.set_defaults(func=command_claim)

    handoff = sub.add_parser("handoff")
    handoff.add_argument("packet")
    add_fence(handoff)
    handoff.add_argument("--to-coordinator-id")
    handoff.add_argument("--evidence")
    handoff.set_defaults(func=command_handoff)

    recover = sub.add_parser("recover")
    recover.add_argument("packet")
    recover.add_argument("--expected-revision", type=int, required=True)
    recover.add_argument("--expected-epoch", type=int, required=True)
    recover.add_argument("--expected-generation", type=int, required=True)
    recover.add_argument("--new-coordinator-id")
    recover.add_argument("--evidence", required=True)
    recover.set_defaults(func=command_recover)

    transition = sub.add_parser("transition")
    transition.add_argument("packet")
    add_fence(transition)
    transition.add_argument("--to", required=True, choices=sorted(STATUSES - {"invalid"}))
    transition.add_argument("--approval-id")
    transition.add_argument("--authority")
    transition.add_argument("--approval-evidence")
    transition.add_argument("--authorization-evidence")
    transition.add_argument("--reuse-approval", action="store_true")
    transition.add_argument("--partial-work-disposition")
    transition.add_argument("--rollback", action="store_true")
    transition.set_defaults(func=command_transition)

    questions = sub.add_parser("questions")
    questions.add_argument("packet")
    add_fence(questions)
    questions.add_argument("--set", action="append")
    questions.set_defaults(func=command_questions)

    attempt = sub.add_parser("record-attempt")
    attempt.add_argument("packet")
    add_fence(attempt)
    attempt.add_argument("--step-id", required=True)
    attempt.add_argument("--actor-id", required=True)
    attempt.add_argument("--model", required=True)
    attempt.add_argument("--status", required=True)
    attempt.add_argument("--started-at")
    attempt.add_argument("--ended-at")
    attempt.add_argument("--action", action="append")
    attempt.add_argument("--mutation", action="append")
    attempt.add_argument("--evidence", action="append")
    attempt.add_argument("--verification")
    attempt.add_argument("--disposition")
    attempt.set_defaults(func=command_record_attempt)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except PacketError as error:
        return fail(args.command, error)
    except OSError as error:
        wrapped = PacketError(EXIT_IO, "filesystem operation failed", None, str(error))
        return fail(args.command, wrapped)
    except UnicodeError as error:
        wrapped = PacketError(EXIT_INVALID, "packet text is not valid UTF-8", "UTF-8 text", str(error))
        return fail(args.command, wrapped)


if __name__ == "__main__":
    raise SystemExit(main())
