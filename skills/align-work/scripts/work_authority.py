#!/usr/bin/env python3
"""Validate current and legacy work-authority seams and packet transfers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import uuid
from pathlib import Path
from typing import Any

import planning_packet


AUTHORITY_FIELDS = {
    "schema_version",
    "work_id",
    "sequence",
    "original_request_sha256",
    "alignment_mode",
    "gateway_classification",
    "repository_root",
    "packet_binding",
}
PACKET_COMMON_FIELDS = {
    "packet_id",
    "task_id",
    "packet_path",
    "packet_revision",
    "protected_digest",
    "approval_id",
    "coordinator_id",
    "coordinator_epoch",
    "state_generation",
    "lifecycle_status",
    "execution_head",
}
PACKET_FIELDS_BY_VERSION = {
    "work_authority/v1": PACKET_COMMON_FIELDS | {"authority_classes"},
    "work_authority/v2": PACKET_COMMON_FIELDS | {"packet_schema_version"},
}
TRANSFER_FIELDS = {
    "schema_version",
    "receipt_id",
    "packet_id",
    "repository_root",
    "packet_path",
    "packet_revision",
    "protected_digest",
    "approval_id",
    "old_coordinator",
    "new_coordinator",
    "state_generation",
    "status",
    "resume_status",
    "runtime_authorization_cleared",
    "execution_head",
    "issued_at",
    "receipt_sha256",
}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
TASK_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
CLASSIFICATIONS = {
    "explicit-invocation",
    "existing-packet",
    "material-decision",
    "destructive",
    "production",
    "security-privacy",
    "costly",
    "external-mutation",
    "none",
}
PACKET_STATUSES = {
    "approved",
    "executing",
    "verifying",
    "needs_reapproval",
    "blocked",
    "cancelled",
    "complete",
}
TERMINAL_PACKET_STATUSES = {"complete", "cancelled"}
RECEIPT_STATUS = {
    "accepted": {"approved"},
    "progress": {"executing", "verifying"},
    "blocked": {"executing", "verifying", "blocked"},
    "failed": {"executing", "verifying", "blocked", "needs_reapproval"},
    "cancelled": {"cancelled"},
    "complete": {"verifying"},
}


class WorkAuthorityError(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def fail(code: str, detail: str = "") -> None:
    raise WorkAuthorityError(code, detail)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def domain_hash(domain: str, value: object) -> str:
    return hashlib.sha256(domain.encode("ascii") + b"\0" + canonical_json(value)).hexdigest()


def _unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            fail("E_STRICT_JSON", f"duplicate key {key!r}")
        result[key] = value
    return result


def load_strict(path: Path) -> dict[str, Any]:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        fail("E_INPUT_UNSAFE", str(path))
    try:
        value = json.loads(
            path.read_text(encoding="utf-8", errors="strict"),
            object_pairs_hook=_unique,
            parse_float=lambda value: (_ for _ in ()).throw(WorkAuthorityError("E_STRICT_JSON", f"float {value}")),
            parse_constant=lambda value: (_ for _ in ()).throw(WorkAuthorityError("E_STRICT_JSON", value)),
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail("E_STRICT_JSON", str(exc))
    if not isinstance(value, dict):
        fail("E_SCHEMA", "root must be an object")
    return value


def _uuid(value: object, field: str) -> str:
    if not isinstance(value, str):
        fail("E_SCHEMA", field)
    try:
        return str(uuid.UUID(value))
    except ValueError:
        fail("E_SCHEMA", field)


def _hash(value: object, field: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or HASH_RE.fullmatch(value) is None:
        fail("E_SCHEMA", field)


def canonical_repository(value: str | Path) -> Path:
    raw = Path(value).expanduser().absolute()
    try:
        resolved = raw.resolve(strict=True)
    except OSError as exc:
        fail("E_REPOSITORY_ROOT", str(exc))
    if raw != resolved or raw.is_symlink() or not resolved.is_dir():
        fail("E_REPOSITORY_ROOT", str(raw))
    return resolved


def validate_authority_shape(authority: dict[str, Any]) -> None:
    if set(authority) != AUTHORITY_FIELDS:
        fail("E_SCHEMA", f"work authority fields {sorted(set(authority) ^ AUTHORITY_FIELDS)}")
    work_schema = authority["schema_version"]
    if work_schema not in PACKET_FIELDS_BY_VERSION:
        fail("E_WORK_AUTHORITY_VERSION")
    _uuid(authority["work_id"], "work_id")
    if type(authority["sequence"]) is not int or authority["sequence"] < 0:
        fail("E_SCHEMA", "sequence")
    _hash(authority["original_request_sha256"], "original_request_sha256")
    if authority["alignment_mode"] not in {"packet", "none"}:
        fail("E_ALIGNMENT_MODE")
    if authority["gateway_classification"] not in CLASSIFICATIONS:
        fail("E_GATEWAY_CLASSIFICATION")
    if not isinstance(authority["repository_root"], str) or not authority["repository_root"].startswith("/"):
        fail("E_REPOSITORY_ROOT")
    binding = authority["packet_binding"]
    if authority["alignment_mode"] == "none":
        if binding is not None or authority["gateway_classification"] != "none":
            fail("E_ALIGNMENT_MODE", "none must have null packet and none classification")
        return
    if not isinstance(binding, dict) or authority["gateway_classification"] == "none":
        fail("E_ALIGNMENT_MODE", "packet requires binding and trigger classification")
    expected_packet_fields = PACKET_FIELDS_BY_VERSION[work_schema]
    if set(binding) != expected_packet_fields:
        fail("E_SCHEMA", f"packet binding fields {sorted(set(binding) ^ expected_packet_fields)}")
    _uuid(binding["packet_id"], "packet_id")
    _uuid(binding["approval_id"], "approval_id")
    _uuid(binding["coordinator_id"], "coordinator_id")
    if not isinstance(binding["task_id"], str) or TASK_RE.fullmatch(binding["task_id"]) is None:
        fail("E_SCHEMA", "task_id")
    if binding["packet_path"] != f".planning/{binding['task_id']}":
        fail("E_PACKET_PATH", str(binding["packet_path"]))
    for field, minimum in (("packet_revision", 1), ("coordinator_epoch", 1), ("state_generation", 0)):
        if type(binding[field]) is not int or binding[field] < minimum:
            fail("E_SCHEMA", field)
    _hash(binding["protected_digest"], "protected_digest")
    _hash(binding["execution_head"], "execution_head", nullable=True)
    if work_schema == "work_authority/v1":
        classes = binding["authority_classes"]
        if not isinstance(classes, list) or not classes or classes != sorted(set(classes)) or not set(classes) <= {"P", "R", "T"}:
            fail("E_AUTHORITY_CLASSES")
    elif binding["packet_schema_version"] != 2:
        fail("E_PACKET_SCHEMA", "current work authority requires packet schema version 2")
    if binding["lifecycle_status"] not in PACKET_STATUSES:
        fail("E_PACKET_STATUS")


def active_packets(repository: Path) -> list[Path]:
    planning = repository / ".planning"
    if not planning.exists():
        return []
    if planning.is_symlink() or not planning.is_dir():
        fail("E_PACKET_DISCOVERY_UNSAFE", str(planning))
    result: list[Path] = []
    for child in sorted(planning.iterdir(), key=lambda item: item.name):
        if child.is_symlink() or not child.is_dir():
            continue
        state_path = child / "state.json"
        if not state_path.exists():
            continue
        try:
            state = load_strict(state_path)
        except WorkAuthorityError as exc:
            fail("E_PACKET_DISCOVERY_UNSAFE", f"{state_path}: {exc}")
        if state.get("repository_root") == str(repository) and state.get("status") not in TERMINAL_PACKET_STATUSES:
            result.append(child)
    return result


def classify_request(original_request: str, repository: Path) -> str:
    lowered = original_request.casefold()
    if re.search(r"(?:\$|\b)align-work\b", lowered):
        return "explicit-invocation"
    if active_packets(repository):
        return "existing-packet"
    patterns = (
        ("material-decision", r"\b(?:decide|decision|choose|ambiguity|ambiguous|architecture|scope|acceptance criteria)\b"),
        ("security-privacy", r"\b(?:security|privacy|credential|secret|permission|authorization)\b"),
        ("destructive", r"\b(?:delete|destroy|drop|purge|irreversible|force push|reset --hard)\b"),
        ("production", r"\b(?:production|deploy|release|live traffic)\b"),
        ("costly", r"\b(?:costly|paid|purchase|billing|expensive)\b"),
        ("external-mutation", r"\b(?:send|publish|push|merge|external mutation)\b"),
    )
    for classification, pattern in patterns:
        if re.search(pattern, lowered):
            return classification
    return "none"


def binding_from_state(repository: Path, packet: Path, state: dict[str, Any]) -> dict[str, Any]:
    approval = state.get("approval")
    coordinator = state.get("active_coordinator")
    if not isinstance(approval, dict) or not isinstance(coordinator, dict):
        fail("E_PACKET_CURRENT_STATE", "approval and coordinator required")
    binding = {
        "packet_id": state["packet_id"],
        "task_id": state["task_id"],
        "packet_path": str(packet.relative_to(repository)),
        "packet_revision": state["packet_revision"],
        "protected_digest": state["protected_digest"],
        "approval_id": approval["id"],
        "coordinator_id": coordinator["id"],
        "coordinator_epoch": coordinator["epoch"],
        "state_generation": state["state_generation"],
        "lifecycle_status": state["status"],
        "execution_head": state["execution_head"],
    }
    if state.get("schema_version") == 1:
        classes = approval.get("authority_classes")
        if not isinstance(classes, list):
            fail("E_PACKET_CURRENT_STATE", "legacy approval classes required")
        binding["authority_classes"] = sorted(classes)
    elif state.get("schema_version") == 2:
        binding["packet_schema_version"] = 2
    else:
        fail("E_PACKET_SCHEMA", str(state.get("schema_version")))
    return binding


def work_schema_from_state(state: dict[str, Any]) -> str:
    if state.get("schema_version") == 1:
        return "work_authority/v1"
    if state.get("schema_version") == 2:
        return "work_authority/v2"
    fail("E_PACKET_SCHEMA", str(state.get("schema_version")))


def validate_current(
    authority: dict[str, Any],
    *,
    original_request: str,
    repository: Path,
    update_status: str | None = None,
) -> dict[str, Any]:
    validate_authority_shape(authority)
    repository = canonical_repository(repository)
    if authority["repository_root"] != str(repository):
        fail("E_REPOSITORY_ROOT", "authority disagrees with current root")
    expected_request_hash = hashlib.sha256(original_request.encode("utf-8")).hexdigest()
    if authority["original_request_sha256"] != expected_request_hash:
        fail("E_ORIGINAL_REQUEST_CHANGED")
    independent = classify_request(original_request, repository)
    if authority["alignment_mode"] == "none":
        if independent != "none":
            fail("E_ALIGNMENT_DISAGREEMENT", independent)
        if update_status is not None and update_status not in RECEIPT_STATUS:
            fail("E_UPDATE_STATUS", update_status)
        return {"alignment_mode": "none", "classification": independent}
    binding = authority["packet_binding"]
    packet = repository / binding["packet_path"]
    if packet.parent != repository / ".planning" or packet.is_symlink():
        fail("E_PACKET_PATH", str(packet))
    try:
        canonical_packet = planning_packet.packet_path(packet)
        state = planning_packet.read_json(canonical_packet / "state.json")
        planning_packet.validate_packet(canonical_packet, state)
    except planning_packet.PacketError as exc:
        fail("E_PACKET_CURRENT_STATE", exc.invariant)
    expected_work_schema = work_schema_from_state(state)
    if authority["schema_version"] != expected_work_schema:
        fail("E_PACKET_SCHEMA", f"{authority['schema_version']} cannot bind packet schema {state['schema_version']}")
    expected = binding_from_state(repository, canonical_packet, state)
    if binding != expected:
        fail("E_PACKET_FENCE_STALE")
    if authority["sequence"] == 0:
        if state["status"] != "approved":
            fail("E_PACKET_STATUS", "initial work requires approved")
    elif update_status is None:
        fail("E_UPDATE_STATUS", "sequence greater than zero requires update status")
    if update_status is not None:
        allowed = RECEIPT_STATUS.get(update_status)
        if allowed is None or state["status"] not in allowed:
            fail("E_PACKET_STATUS", f"{update_status} cannot bind {state['status']}")
    return {
        "alignment_mode": "packet",
        "classification": independent,
        "packet_id": state["packet_id"],
        "status": state["status"],
        "state_generation": state["state_generation"],
    }


def transfer_receipt_hash(receipt: dict[str, Any]) -> str:
    body = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    return domain_hash("packet-transfer-receipt/v1", body)


def validate_transfer_shape(receipt: dict[str, Any]) -> None:
    if set(receipt) != TRANSFER_FIELDS or receipt.get("schema_version") != "packet-transfer-receipt/v1":
        fail("E_TRANSFER_RECEIPT_SCHEMA")
    _uuid(receipt["receipt_id"], "receipt_id")
    _uuid(receipt["packet_id"], "packet_id")
    if receipt["approval_id"] is not None:
        _uuid(receipt["approval_id"], "approval_id")
    for field in ("old_coordinator", "new_coordinator"):
        coordinator = receipt[field]
        if not isinstance(coordinator, dict) or set(coordinator) != {"id", "epoch"}:
            fail("E_TRANSFER_RECEIPT_SCHEMA", field)
        _uuid(coordinator["id"], f"{field}.id")
        if type(coordinator["epoch"]) is not int or coordinator["epoch"] < 1:
            fail("E_TRANSFER_RECEIPT_SCHEMA", field)
    if receipt["new_coordinator"]["epoch"] != receipt["old_coordinator"]["epoch"] + 1:
        fail("E_TRANSFER_RECEIPT_SCHEMA", "epoch")
    if receipt["status"] != "paused" or receipt["runtime_authorization_cleared"] is not True:
        fail("E_TRANSFER_RECEIPT_SCHEMA", "paused/cleared")
    _hash(receipt["protected_digest"], "protected_digest")
    _hash(receipt["execution_head"], "execution_head", nullable=True)
    _hash(receipt["receipt_sha256"], "receipt_sha256")
    if receipt["receipt_sha256"] != transfer_receipt_hash(receipt):
        fail("E_TRANSFER_RECEIPT_HASH")


def validate_transfer_current(receipt: dict[str, Any], repository: Path) -> dict[str, Any]:
    validate_transfer_shape(receipt)
    repository = canonical_repository(repository)
    if receipt["repository_root"] != str(repository):
        fail("E_REPOSITORY_ROOT")
    packet = repository / receipt["packet_path"]
    try:
        packet = planning_packet.packet_path(packet)
        state = planning_packet.read_json(packet / "state.json")
        planning_packet.validate_packet(packet, state)
    except planning_packet.PacketError as exc:
        fail("E_PACKET_CURRENT_STATE", exc.invariant)
    approval = state.get("approval")
    current = {
        "packet_id": state["packet_id"],
        "packet_revision": state["packet_revision"],
        "protected_digest": state["protected_digest"],
        "approval_id": approval["id"] if isinstance(approval, dict) else None,
        "new_coordinator": state["active_coordinator"],
        "state_generation": state["state_generation"],
        "status": state["status"],
        "resume_status": state["resume_status"],
        "execution_head": state["execution_head"],
    }
    expected = {key: receipt[key] for key in current}
    if current != expected or state["runtime_authorization_evidence"] is not None:
        fail("E_TRANSFER_RECEIPT_STALE")
    history = state["coordinator_history"]
    if not history or history[-1].get("event") != "handoff" or history[-1].get("from") != receipt["old_coordinator"] or history[-1].get("to") != receipt["new_coordinator"]:
        fail("E_TRANSFER_RECEIPT_STALE", "coordinator history")
    return {"packet_id": state["packet_id"], "status": "paused", "authoritative": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    work = sub.add_parser("validate-work")
    work.add_argument("--authority", type=Path, required=True)
    work.add_argument("--original-request", type=Path, required=True)
    work.add_argument("--repo", type=Path, required=True)
    update = sub.add_parser("validate-update")
    update.add_argument("--authority", type=Path, required=True)
    update.add_argument("--original-request", type=Path, required=True)
    update.add_argument("--repo", type=Path, required=True)
    update.add_argument("--status", required=True)
    transfer = sub.add_parser("validate-transfer")
    transfer.add_argument("--receipt", type=Path, required=True)
    transfer.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-transfer":
            result = validate_transfer_current(load_strict(args.receipt), args.repo)
        else:
            request = args.original_request.read_text(encoding="utf-8", errors="strict")
            result = validate_current(
                load_strict(args.authority),
                original_request=request,
                repository=args.repo,
                update_status=args.status if args.command == "validate-update" else None,
            )
    except (WorkAuthorityError, OSError, UnicodeError) as exc:
        code = exc.code if isinstance(exc, WorkAuthorityError) else "E_IO"
        print(json.dumps({"ok": False, "code": code, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, **result}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
