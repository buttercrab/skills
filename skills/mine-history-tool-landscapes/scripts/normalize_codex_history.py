#!/usr/bin/env python3
"""Emit one descriptor-bound v2 adapter projection for Codex or Claude Code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

import history_v4
from strict_json import canonical_bytes, loads_strict, StrictJSONError


NATIVE_FIELDS = {
    "id": "session",
    "session_id": "session",
    "sessionId": "session",
    "uuid": "message",
    "leafUuid": "message",
    "parent_id": "parent",
    "parentUuid": "parent",
    "project_id": "project",
    "projectId": "project",
    "tool_call_id": "tool",
    "call_id": "tool",
    "user_id": "user",
    "organization_id": "organization",
    "workspace_id": "workspace",
    "namespace": "namespace",
    "task_id": "task",
    "thread_id": "thread",
    "run_id": "run",
    "job_id": "job",
    "artifact_id": "artifact",
    "requestId": "provider_specific",
    "request_id": "provider_specific",
    "agentId": "provider_specific",
    "parentToolUseID": "tool",
}

NATIVE_LIKE_FIELD = re.compile(
    r"(?:^|_)(?:id|ids|uuid|uuids)$|(?:Id|ID|Uuid|UUID)$"
)

REDACTIONS = (
    (re.compile(r"-----BEGIN .*?PRIVATE KEY-----.*?-----END .*?PRIVATE KEY-----", re.I | re.S), "[REDACTED:CREDENTIAL]"),
    (re.compile(r"\b(?:sk-|gh[pousr]_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{12,}"), "[REDACTED:CREDENTIAL]"),
    (re.compile(r"\b(?:https?|file|ssh)://\S+", re.I), "[REDACTED:URI]"),
    (re.compile(r"(?:^|\s)/(?:Users|home|private|var|tmp)/\S+"), " [REDACTED:ABSOLUTE_PATH]"),
    (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[REDACTED:EMAIL]"),
)


def _native_values(value: object, found: dict[str, set[str]], trail: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in NATIVE_FIELDS and isinstance(child, str) and child:
                found[NATIVE_FIELDS[key]].add(child)
            elif (
                key not in NATIVE_FIELDS
                and NATIVE_LIKE_FIELD.search(key)
                and child not in (None, "", [], {})
            ):
                history_v4.fail("E_NATIVE_ID_INVENTORY_INCOMPLETE", trail + "/" + key)
            _native_values(child, found, trail + "/" + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _native_values(child, found, trail + f"/{index}")


def _text(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    if isinstance(value, list):
        parts = []
        for child in value:
            if isinstance(child, str):
                parts.append(child)
            elif isinstance(child, dict):
                for key in ("text", "input_text", "output_text", "content"):
                    if isinstance(child.get(key), str):
                        parts.append(child[key])
                        break
        return "\n".join(parts) or None
    if isinstance(value, dict):
        for key in ("text", "input_text", "output_text", "content", "message", "summary"):
            candidate = _text(value.get(key))
            if candidate:
                return candidate
    return None


def _redact(value: str, native_values: list[str]) -> str:
    result = value
    for native in sorted(native_values, key=lambda item: (-len(item.encode()), item.encode())):
        result = result.replace(native, "[REDACTED:NATIVE_ID]")
    for pattern, replacement in REDACTIONS:
        result = pattern.sub(replacement, result)
    if any(native and native in result for native in native_values):
        history_v4.fail("E_REDACTION_INCOMPLETE")
    if any(pattern.search(result) for pattern, _ in REDACTIONS):
        history_v4.fail("E_REDACTION_INCOMPLETE")
    return result


def _rows(payload: bytes) -> list[dict[str, Any]]:
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        history_v4.fail("E_ADAPTER_UTF8", str(exc))
    lines = text.splitlines()
    if not lines or any(not line for line in lines):
        history_v4.fail("E_ADAPTER_ENVELOPE", "blank JSONL line")
    result = []
    for ordinal, line in enumerate(lines, 1):
        try:
            value = loads_strict(line)
        except StrictJSONError as exc:
            history_v4.fail("E_ADAPTER_ENVELOPE", f"line {ordinal}: {exc}")
        if not isinstance(value, dict):
            history_v4.fail("E_ADAPTER_ENVELOPE", f"line {ordinal}")
        result.append(value)
    return result


def project(
    *,
    platform: str,
    source_id: str,
    descriptor: dict[str, Any],
    payload: bytes,
    identity_key: bytes,
    index_salt: bytes,
) -> dict[str, Any]:
    rows = _rows(payload)
    inventory = {field: set() for field in set(NATIVE_FIELDS.values())}
    for row in rows:
        _native_values(row, inventory)
    all_native = sorted({item for values in inventory.values() for item in values})
    projections = []
    native_map = [
        {
            "platform": platform,
            "native_type": native_type,
            "native_value": native,
            "native_hmac": history_v4.derive_native_hmac(
                identity_key, index_salt, platform, native_type, native
            ),
        }
        for native_type in sorted(inventory)
        for native in sorted(inventory[native_type], key=lambda item: item.encode())
    ]
    for ordinal, row in enumerate(rows, 1):
        if platform == "codex":
            if set(row) != {"type", "timestamp", "payload"} or not isinstance(row.get("payload"), dict):
                history_v4.fail("E_ADAPTER_ENVELOPE", f"codex line {ordinal}")
            body = row["payload"]
            timestamp = row["timestamp"]
            native = body.get("id") or body.get("session_id")
            parent = body.get("parent_id")
            namespace = body.get("namespace") or body.get("session_id")
            candidate = body.get("instructions") or body.get("content") or body.get("message")
            field = "root-intent" if body.get("instructions") else "user-message"
            pointer = "/payload/instructions" if body.get("instructions") else "/payload/content"
            native_type = "session"
        else:
            allowed = {"type", "sessionId", "uuid", "parentUuid", "timestamp", "cwd", "message", "isSidechain", "userType", "version", "gitBranch", "slug", "summary", "leafUuid", "toolUseResult", "requestId", "agentId", "parentToolUseID"}
            if not set(row) <= allowed or not {"type", "timestamp"} <= set(row):
                history_v4.fail("E_ADAPTER_ENVELOPE", f"claude line {ordinal}")
            timestamp = row["timestamp"]
            native = row.get("uuid") or row.get("sessionId")
            parent = row.get("parentUuid")
            namespace = row.get("sessionId")
            candidate = row.get("message") or row.get("summary")
            field = "user-message"
            pointer = "/message/content" if row.get("message") is not None else "/summary"
            native_type = "message"
        history_v4.parse_time(timestamp, f"line {ordinal}.timestamp")
        if not isinstance(native, str) or not native:
            history_v4.fail("E_NATIVE_ID_INVENTORY_INCOMPLETE", f"line {ordinal}")
        native_hmac = history_v4.derive_native_hmac(identity_key, index_salt, platform, native_type, native)
        namespace_value = namespace if isinstance(namespace, str) and namespace else native
        namespace_native_type = "namespace" if platform == "codex" else "session"
        namespace_hmac = history_v4.derive_native_hmac(
            identity_key,
            index_salt,
            platform,
            namespace_native_type,
            namespace_value,
        )
        record_id = history_v4.derive_public_id(identity_key, index_salt, "record", "record", native_hmac)
        node_id = history_v4.derive_public_id(identity_key, index_salt, native_type, native_type, native_hmac)
        root_id = history_v4.derive_public_id(identity_key, index_salt, "root", "root", native_hmac)
        namespace_id = history_v4.derive_public_id(identity_key, index_salt, "namespace", "namespace", namespace_hmac)
        project_id = history_v4.derive_public_id(identity_key, index_salt, "project-family", "project", namespace_hmac)
        parent_hmac = history_v4.derive_native_hmac(identity_key, index_salt, platform, native_type, parent) if isinstance(parent, str) and parent else None
        parent_id = history_v4.derive_public_id(identity_key, index_salt, native_type, native_type, parent_hmac) if parent_hmac else None
        text = _text(candidate)
        projections.append(
            {
                "source_record_ordinal": ordinal,
                "timestamp": timestamp,
                "native_type": native_type,
                "native_hmac": native_hmac,
                "parent_native_hmac": parent_hmac,
                "node_id": node_id,
                "record_id": record_id,
                "parent_id": parent_id,
                "root_id": root_id if parent_id is None else None,
                "namespace_id": namespace_id,
                "project_family_id": project_id,
                "classification": "user-root" if parent_id is None and text else ("continuation" if text else "non-semantic"),
                "classification_basis": "platform-native",
                "field": field if text else None,
                "json_pointer": pointer if text else None,
                "redacted_text": _redact(text, all_native) if text else None,
            }
        )
    by_type = {kind: len(values) for kind, values in sorted(inventory.items())}
    return {
        "schema_version": "history-adapter-projection/v2",
        "platform": platform,
        "adapter_id": "codex-history-jsonl" if platform == "codex" else "claude-code-history-jsonl",
        "adapter_version": "v2",
        "source_id": source_id,
        "source_descriptor": descriptor,
        "raw_sha256": descriptor["sha256"],
        "record_count": len(rows),
        "native_id_inventory": {
            "complete": True,
            "by_type": by_type,
            "total_count": sum(by_type.values()),
            "native_hmac_set_sha256": history_v4.D("history-native-hmac-set/v2", sorted(item["native_hmac"] for item in native_map)),
        },
        "records": projections,
        "native_map": native_map,
        "projection_sha256": history_v4.D("history-adapter-projection/v2", projections),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--platform", choices=("codex", "claude-code"), default="codex")
    result.add_argument("--root", required=True, type=Path)
    result.add_argument("--relative-path", required=True)
    result.add_argument("--source-id", required=True)
    result.add_argument("--identity-root", required=True, type=Path)
    result.add_argument("--identity-key-relative", default="identity-key")
    result.add_argument("--index-salt-relative", default="identity-salt")
    result.add_argument("--max-file-bytes", type=int, default=64 * 1024 * 1024)
    return result


def main_for_args(args: argparse.Namespace) -> int:
    try:
        descriptor, payload = history_v4.acquire_file(args.root, args.relative_path, max_bytes=args.max_file_bytes)
        identity = history_v4.acquire_exact_bundle(
            args.identity_root,
            [args.identity_key_relative, args.index_salt_relative],
            max_file_bytes=32,
            max_total_bytes=64,
        )
        key = identity[history_v4.normalized_relative(args.identity_key_relative)][1]
        salt = identity[history_v4.normalized_relative(args.index_salt_relative)][1]
        if len(key) != 32 or len(salt) != 32:
            history_v4.fail("E_INDEX_IDENTITY_MATERIAL", "key and salt must be 32 bytes")
        result = project(platform=args.platform, source_id=args.source_id, descriptor=descriptor, payload=payload, identity_key=key, index_salt=salt)
    except (history_v4.HistoryV4Error, OSError) as exc:
        code = exc.code if isinstance(exc, history_v4.HistoryV4Error) else "E_IO"
        print(json.dumps(history_v4.diagnostic_document(code, str(exc)), sort_keys=True, separators=(",", ":")))
        return 1
    print(canonical_bytes(result).decode())
    return 0


def main() -> int:
    return main_for_args(parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
