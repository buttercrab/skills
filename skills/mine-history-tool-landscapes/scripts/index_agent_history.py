#!/usr/bin/env python3
"""Materialize and validate one exact private history-index/v4 bundle."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

import history_v4
from strict_json import canonical_bytes


INPUTS = {
    "sources.json": "source-contract",
    "semantic-ledger.json": "semantic-ledger",
    "exclusion-ledger.json": "exclusion-ledger",
    "native-map.json": "native-map",
    "identity-salt": "identity-salt",
    "identity-key": "identity-key",
    "identity-key.receipt.json": "identity-key-receipt",
    "adapter-catalog.json": "adapter-catalog",
    "lifecycle.json": "lifecycle",
    "index-template.json": "template",
}


def _private_write(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        raise


def _target_id(key: bytes, salt: bytes, role: str, relative: str) -> str:
    native = history_v4.derive_native_hmac(key, salt, "private-bundle", role, relative)
    return history_v4.derive_public_id(key, salt, "deletion-target", "target", native)


def _lineage(ledger: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    source = deepcopy(ledger["lineage_accounting"])
    source["platforms"] = ["claude-code", "codex"]
    source["edge_ids"] = sorted(template.get("edge_ids", []), key=lambda item: item.encode())
    source["counts"]["edges"] = len(source["edge_ids"])
    source["counts_sha256"] = history_v4.D(
        "history-index-lineage-accounting/v4",
        history_v4.without(source, "counts_sha256"),
    )
    return source


def build(input_root: Path, out: Path, *, max_file_bytes: int, max_total_bytes: int) -> dict[str, Any]:
    acquired = history_v4.acquire_exact_bundle(
        input_root,
        INPUTS,
        max_file_bytes=max_file_bytes,
        max_total_bytes=max_total_bytes,
    )
    history = history_v4.load_document(acquired["sources.json"][1], "sources.json")
    ledger = history_v4.load_document(acquired["semantic-ledger.json"][1], "semantic-ledger.json")
    template = history_v4.load_document(acquired["index-template.json"][1], "index-template.json")
    lifecycle_seed = history_v4.load_document(acquired["lifecycle.json"][1], "lifecycle.json")
    history_v4.validate_ledger(ledger)
    history_v4.validate_sources(history, ledger)
    key = acquired["identity-key"][1]
    salt = acquired["identity-salt"][1]
    if len(key) != 32 or len(salt) != 32:
        history_v4.fail("E_INDEX_IDENTITY_MATERIAL")

    output_payloads = {
        relative: acquired[relative][1]
        for relative in INPUTS
        if relative != "index-template.json"
    }
    roles = {relative: role for relative, role in INPUTS.items() if role != "template"}
    members = [
        {
            "target_id": _target_id(key, salt, "manifest", "index.json"),
            "relative_path": "index.json",
            "role": "manifest",
            "size": None,
            "content_sha256": None,
            "hash_kind": "normalized-manifest",
            "mode": "0600",
            "nlink": 1,
        }
    ]
    for relative in sorted(output_payloads, key=lambda item: item.encode()):
        payload = output_payloads[relative]
        members.append(
            {
                "target_id": _target_id(key, salt, roles[relative], relative),
                "relative_path": relative,
                "role": roles[relative],
                "size": len(payload),
                "content_sha256": history_v4.sha256_bytes(payload),
                "hash_kind": "raw-bytes",
                "mode": "0600",
                "nlink": 1,
            }
        )
    members = sorted(members, key=lambda item: item["relative_path"].encode())
    exact = {
        "schema_version": "history-private-file-set/v4",
        "state": "live",
        "directory_mode": "0700",
        "file_mode": "0600",
        "member_count": len(members),
        "members_sha256": "",
        "members": members,
    }
    exact["members_sha256"] = history_v4.D("exact-file-set/v2", deepcopy(members))
    targets = [
        {
            "target_id": item["target_id"],
            "relative_path_sha256": history_v4.sha256_bytes(item["relative_path"].encode()),
            "role": item["role"],
            "member_sha256": item["content_sha256"],
            "hash_kind": item["hash_kind"],
        }
        for item in members
    ]
    transitions = lifecycle_seed.get("transitions") or [
        {
            "from": "collecting",
            "to": "live",
            "at": lifecycle_seed.get("captured_at", template["created_at"]),
            "reason": "collection-complete",
            "receipt_sha256": history_v4.D(
                "history-lifecycle-transition/v2",
                {
                    "index_id": history["index_id"],
                    "from": "collecting",
                    "to": "live",
                    "at": lifecycle_seed.get("captured_at", template["created_at"]),
                    "reason": "collection-complete",
                },
            ),
        }
    ]
    lifecycle = {
        "schema_version": "history-private-lifecycle/v2",
        "retention_disposition": lifecycle_seed.get(
            "retention_disposition", history["retention"]["disposition"]
        ),
        "delete_by": lifecycle_seed.get("delete_by", history["retention"]["delete_by"]),
        "state": "live",
        "transitions": transitions,
        "deletion_targets": targets,
        "deletion_receipt": None,
    }
    native_hmacs = sorted(item["native_hmac"] for item in ledger["native_nodes"])
    public_ids: set[str] = set()
    for field in history_v4.LINEAGE_COUNT_FIELDS.values():
        public_ids.update(ledger["lineage_accounting"].get(field, []))
    index = {
        "schema_version": "history-index/v4",
        "index_id": history["index_id"],
        "history_contract_id": history["contract_id"],
        "history_contract_sha256": history_v4.D("history-sources/v4", history),
        "created_at": template["created_at"],
        "identity": {
            "schema_version": "history-identity/v2",
            "index_salt_receipt_sha256": history_v4.sha256_bytes(salt),
            "identity_key_receipt_sha256": history_v4.sha256_bytes(output_payloads["identity-key.receipt.json"]),
            "native_map_sha256": history_v4.sha256_bytes(output_payloads["native-map.json"]),
            "native_hmac_set_sha256": history_v4.D("history-native-hmac-set/v2", native_hmacs),
            "public_id_set_sha256": history_v4.D("history-public-id-set/v2", sorted(public_ids)),
        },
        "exact_file_set": exact,
        "bindings": {
            "raw_source_manifest_sha256": history["raw_manifest"]["sha256"],
            "semantic_ledger_sha256": ledger["semantic_ledger_sha256"],
            "native_lineage_closure_sha256": ledger["native_lineage_closure_sha256"],
            "exclusion_ledger_sha256": history["exclusion_ledger"]["sha256"],
            "corpus_sha256": history["corpus"]["sha256"],
            "adapter_catalog_sha256": history["adapter_catalog"]["catalog_sha256"],
            "specification_sha256": history_v4.sha256_bytes(history_v4.SPEC_PATH.read_bytes()),
        },
        "lineage": _lineage(ledger, template),
        "lifecycle": lifecycle,
        "history_index_sha256": "",
    }
    index["history_index_sha256"] = history_v4.D("history-index/v4", history_v4.without(index, "history_index_sha256"))
    history_v4.validate_index(index, history, ledger)

    raw_parent = out.parent.absolute()
    parent = out.parent.resolve(strict=True)
    if raw_parent != parent or out.parent.is_symlink() or any((item / ".git").exists() for item in (parent, *parent.parents)):
        history_v4.fail("E_OUTPUT_PARENT_UNSAFE", str(out))
    if out.exists():
        history_v4.fail("E_OUTPUT_EXISTS", str(out))
    temp = Path(tempfile.mkdtemp(prefix=f".{out.name}-", dir=parent))
    try:
        temp.chmod(0o700)
        for relative, payload in output_payloads.items():
            _private_write(temp / relative, payload)
        _private_write(temp / "index.json", canonical_bytes(index) + b"\n")
        temp.replace(out)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    return index


def validate(index_root: Path, *, max_file_bytes: int, max_total_bytes: int) -> dict[str, Any]:
    descriptor, payload = history_v4.acquire_file(
        index_root, "index.json", max_bytes=max_file_bytes
    )
    index = history_v4.load_document(payload, "index.json")
    declared = [item["relative_path"] for item in index["exact_file_set"]["members"]]
    acquired = history_v4.acquire_exact_bundle(
        index_root,
        declared,
        max_file_bytes=max_file_bytes,
        max_total_bytes=max_total_bytes,
    )
    for member in index["exact_file_set"]["members"]:
        if member["role"] == "manifest":
            continue
        actual_descriptor, actual = acquired[member["relative_path"]]
        if member["size"] != len(actual) or member["content_sha256"] != actual_descriptor["sha256"]:
            history_v4.fail("E_PRIVATE_FILE_SET_MISMATCH", member["relative_path"])
    history = history_v4.load_document(acquired["sources.json"][1], "sources.json")
    ledger = history_v4.load_document(acquired["semantic-ledger.json"][1], "semantic-ledger.json")
    history_v4.validate_ledger(ledger)
    history_v4.validate_sources(history, ledger)
    history_v4.validate_index(index, history, ledger)
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("build")
    create.add_argument("--input-root", required=True, type=Path)
    create.add_argument("--out", required=True, type=Path)
    check = sub.add_parser("validate")
    check.add_argument("index", type=Path)
    for item in (create, check):
        item.add_argument("--max-file-bytes", type=int, default=64 * 1024 * 1024)
        item.add_argument("--max-total-bytes", type=int, default=256 * 1024 * 1024)
    args = parser.parse_args()
    try:
        result = (
            build(args.input_root, args.out, max_file_bytes=args.max_file_bytes, max_total_bytes=args.max_total_bytes)
            if args.command == "build"
            else validate(args.index, max_file_bytes=args.max_file_bytes, max_total_bytes=args.max_total_bytes)
        )
    except (history_v4.HistoryV4Error, OSError) as exc:
        code = exc.code if isinstance(exc, history_v4.HistoryV4Error) else "E_IO"
        print(json.dumps(history_v4.diagnostic_document(code, str(exc)), sort_keys=True, separators=(",", ":")))
        return 1
    print(json.dumps({"ok": True, "authoritative": True, "index": result}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
