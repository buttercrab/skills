#!/usr/bin/env python3
"""Authoritatively reopen and validate one complete History v4 chain."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
from typing import Any

import history_v4
import normalize_codex_history


DOCUMENT_PATHS = {
    "history": "history-sources-v4.json",
    "ledger": "semantic-observation-ledger-v2.json",
    "index": "history-index-v4.json",
    "reduction": "capability-reduction-v3.json",
    "evidence": "history-evidence-v1.json",
    "publication": "history-publication-v3.json",
}

EVIDENCE_INPUT_PATHS = {
    "history": "evidence-inputs/history-sources-v4.json",
    "ledger": "evidence-inputs/semantic-observation-ledger-v2.json",
    "index": "evidence-inputs/history-index-v4.json",
    "reduction": "evidence-inputs/capability-reduction-v3.json",
}

DETACHED_MODEL_PATHS = {
    "runtime-model-catalog": "runtime-model-catalog.json",
    "provider-trust-catalog": "provider-trust-catalog.json",
    "callable-verification-receipt": "callable-verification-receipt.json",
}

PROVIDER_AUTHORITY_PATHS = {
    "provider-trust-root-receipt": "provider-trust-root-receipt.json",
    "provider-verification-key": "provider-verification.key",
    "provider-verifier": "provider-verifier.py",
    "nonce-state-before": "nonce-state.before.json",
    "nonce-state-after": "nonce-state.after.json",
}

RAW_REOPEN_RECEIPT_PATH = "raw-reopen-receipt.json"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--bundle-root",
        required=True,
        type=Path,
        help="exact six-document public successor bundle",
    )
    result.add_argument(
        "--private-index-root",
        type=Path,
        help="exact private history-index/v4 directory",
    )
    result.add_argument(
        "--authority-root",
        type=Path,
        help="exact independent evidence and provider-authority directory",
    )
    result.add_argument(
        "--trusted-provider-root-authority-sha256",
        help="out-of-band descriptor root pin for --authority-root",
    )
    result.add_argument(
        "--trusted-trust-root-receipt-sha256",
        help="out-of-band SHA-256 pin for provider-trust-root-receipt.json",
    )
    result.add_argument("--max-file-bytes", type=int, default=64 * 1024 * 1024)
    result.add_argument("--max-total-bytes", type=int, default=256 * 1024 * 1024)
    result.add_argument(
        "--diagnostic-without-raw-reopen",
        action="store_true",
        help="emit a closed non-authoritative E_RAW_REOPEN_REQUIRED diagnostic",
    )
    return result


def _load_set(
    acquired: dict[str, tuple[dict[str, Any], bytes]],
    paths: dict[str, str],
) -> dict[str, dict[str, Any]]:
    return {
        role: history_v4.load_document(acquired[path][1], path)
        for role, path in paths.items()
    }


def _require_private_directory(root: Path) -> None:
    raw = root.expanduser().absolute()
    if raw.is_symlink():
        history_v4.fail("E_DESCRIPTOR_SYMLINK", str(raw))
    info = raw.resolve(strict=True).stat()
    if (
        not stat.S_ISDIR(info.st_mode)
        or stat.S_IMODE(info.st_mode) != 0o700
        or info.st_uid != os.geteuid()
    ):
        history_v4.fail("E_PRIVATE_FILE_SET_MISMATCH", "private root topology")


def _reopen_private_index(
    root: Path,
    documents: dict[str, dict[str, Any]],
    *,
    max_file_bytes: int,
    max_total_bytes: int,
) -> tuple[bytes, bytes, list[dict[str, str]]]:
    _require_private_directory(root)
    _, index_payload = history_v4.acquire_file(
        root, "index.json", max_bytes=max_file_bytes
    )
    private_index = history_v4.load_document(index_payload, "private index.json")
    if private_index != documents["index"]:
        history_v4.fail("E_HISTORY_BINDING_REQUIRED", "private index document")
    if private_index["lifecycle"]["state"] != "live":
        history_v4.fail("E_LEDGER_EXPIRED", "private index is not usable")
    declared = [
        item["relative_path"] for item in private_index["exact_file_set"]["members"]
    ]
    if any(not isinstance(path, str) for path in declared):
        history_v4.fail("E_PRIVATE_FILE_SET_MISMATCH", "live member path")
    acquired = history_v4.acquire_exact_bundle(
        root,
        declared,
        max_file_bytes=max_file_bytes,
        max_total_bytes=max_total_bytes,
    )
    for member in private_index["exact_file_set"]["members"]:
        descriptor, payload = acquired[member["relative_path"]]
        if member["role"] == "manifest":
            if history_v4.load_document(payload, "private index.json") != private_index:
                history_v4.fail("E_PRIVATE_FILE_SET_MISMATCH", "manifest bytes")
            continue
        if (
            member["size"] != len(payload)
            or member["content_sha256"] != descriptor["sha256"]
            or member["mode"] != descriptor["mode"]
            or member["nlink"] != descriptor["nlink"]
        ):
            history_v4.fail(
                "E_PRIVATE_FILE_SET_MISMATCH", member["relative_path"]
            )

    private_documents = {
        "history": history_v4.load_document(acquired["sources.json"][1], "sources.json"),
        "ledger": history_v4.load_document(
            acquired["semantic-ledger.json"][1], "semantic-ledger.json"
        ),
    }
    for role, value in private_documents.items():
        if value != documents[role]:
            history_v4.fail("E_HISTORY_BINDING_REQUIRED", f"private {role}")
    exclusion = history_v4.load_document(
        acquired["exclusion-ledger.json"][1], "exclusion-ledger.json"
    )
    adapter_catalog = history_v4.load_document(
        acquired["adapter-catalog.json"][1], "adapter-catalog.json"
    )
    if exclusion != documents["history"]["exclusion_ledger"]:
        history_v4.fail("E_HISTORY_BINDING_REQUIRED", "private exclusion ledger")
    if adapter_catalog != documents["history"]["adapter_catalog"]:
        history_v4.fail("E_ADAPTER_IMPLEMENTATION_DRIFT", "private adapter catalog")

    key = acquired["identity-key"][1]
    salt = acquired["identity-salt"][1]
    if len(key) != 32 or len(salt) != 32:
        history_v4.fail("E_INDEX_IDENTITY_MATERIAL")
    key_receipt = history_v4.load_document(
        acquired["identity-key.receipt.json"][1], "identity-key.receipt.json"
    )
    if (
        key_receipt.get("receipt_sha256")
        != history_v4.D(
            "history-identity-key-receipt/v1",
            history_v4.without(key_receipt, "receipt_sha256"),
        )
        or key_receipt.get("key_sha256") != history_v4.sha256_bytes(key)
        or key_receipt.get("salt_sha256") != history_v4.sha256_bytes(salt)
        or key_receipt.get("key_bytes") != 32
        or key_receipt.get("salt_bytes") != 32
    ):
        history_v4.fail("E_INDEX_IDENTITY_MATERIAL", "identity receipt")
    identity = documents["index"]["identity"]
    policy = documents["history"]["identity_policy"]
    if (
        identity["index_salt_receipt_sha256"] != history_v4.sha256_bytes(salt)
        or identity["identity_key_receipt_sha256"]
        != acquired["identity-key.receipt.json"][0]["sha256"]
        or policy["index_salt_receipt_sha256"] != history_v4.sha256_bytes(salt)
        or policy["identity_key_receipt_sha256"]
        != acquired["identity-key.receipt.json"][0]["sha256"]
    ):
        history_v4.fail("E_INDEX_IDENTITY_MATERIAL", "identity binding")

    native_map = history_v4.load_document(
        acquired["native-map.json"][1], "native-map.json"
    )
    entries = native_map.get("entries")
    if native_map.get("schema_version") != "history-native-map/v2" or not isinstance(
        entries, list
    ):
        history_v4.fail("E_NATIVE_ID_INVENTORY_INCOMPLETE", "private native map")
    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for item in entries:
        try:
            identity_tuple = (
                item["platform"],
                item["native_type"],
                item["native_value"],
            )
            expected_hmac = history_v4.derive_native_hmac(
                key, salt, *identity_tuple
            )
        except (KeyError, TypeError):
            history_v4.fail(
                "E_NATIVE_ID_INVENTORY_INCOMPLETE", "private native map entry"
            )
        if identity_tuple in unique or item.get("native_hmac") != expected_hmac:
            history_v4.fail(
                "E_NATIVE_ID_INVENTORY_INCOMPLETE", "private native map commitment"
            )
        unique[identity_tuple] = item
    if documents["index"]["identity"]["native_map_sha256"] != acquired[
        "native-map.json"
    ][0]["sha256"]:
        history_v4.fail("E_NATIVE_ID_INVENTORY_INCOMPLETE", "native map binding")
    return key, salt, list(unique.values())


def _reopen_authority(
    root: Path,
    documents: dict[str, dict[str, Any]],
    *,
    trusted_provider_root_authority_sha256: str,
    trusted_trust_root_receipt_sha256: str,
    max_file_bytes: int,
    max_total_bytes: int,
) -> tuple[dict[str, tuple[dict[str, Any], bytes]], dict[str, tuple[dict[str, Any], bytes]]]:
    _require_private_directory(root)
    paths = {
        *EVIDENCE_INPUT_PATHS.values(),
        *DETACHED_MODEL_PATHS.values(),
        *PROVIDER_AUTHORITY_PATHS.values(),
        RAW_REOPEN_RECEIPT_PATH,
    }
    acquired = history_v4.acquire_exact_bundle(
        root,
        paths,
        max_file_bytes=max_file_bytes,
        max_total_bytes=max_total_bytes,
    )
    actual_root_authority = history_v4.root_authority(
        root.expanduser().absolute().resolve(strict=True), os.geteuid()
    )
    if actual_root_authority != trusted_provider_root_authority_sha256:
        history_v4.fail("E_CALLABLE_VERIFICATION_MISMATCH", "independent root pin")

    expected_members = documents["evidence"]["bindings"]["exact_input_file_set"][
        "members"
    ]
    actual_inputs = {
        role: acquired[path] for role, path in EVIDENCE_INPUT_PATHS.items()
    }
    if len(expected_members) != len(actual_inputs):
        history_v4.fail("E_EVIDENCE_INPUT_SET_MISMATCH", "member count")
    expected_by_path_hash = {
        item["relative_path_sha256"]: item for item in expected_members
    }
    if len(expected_by_path_hash) != len(expected_members):
        history_v4.fail("E_EVIDENCE_INPUT_SET_MISMATCH", "duplicate descriptor")
    for role, (descriptor, payload) in actual_inputs.items():
        claimed = expected_by_path_hash.get(descriptor["relative_path_sha256"])
        if claimed is None or not history_v4._descriptor_matches(claimed, descriptor):
            history_v4.fail("E_EVIDENCE_INPUT_SET_MISMATCH", role)
        if history_v4.load_document(payload, EVIDENCE_INPUT_PATHS[role]) != documents[
            role
        ]:
            history_v4.fail("E_EVIDENCE_INPUT_SET_MISMATCH", f"{role} bytes")

    raw_descriptor, raw_payload = acquired[RAW_REOPEN_RECEIPT_PATH]
    raw_receipt = history_v4.load_document(raw_payload, RAW_REOPEN_RECEIPT_PATH)
    claimed_raw = documents["evidence"]["bindings"]["raw_reopen_receipt"]
    if (
        raw_receipt != history_v4.without(claimed_raw, "descriptor")
        or not history_v4._descriptor_matches(
            claimed_raw["descriptor"], raw_descriptor
        )
    ):
        history_v4.fail("E_RAW_REOPEN_REQUIRED", "raw reopen receipt bytes")

    detached = {
        role: acquired[path][1] for role, path in DETACHED_MODEL_PATHS.items()
    }
    detached_descriptors = {
        role: acquired[path][0] for role, path in DETACHED_MODEL_PATHS.items()
    }
    provider_authority = {
        role: acquired[path] for role, path in PROVIDER_AUTHORITY_PATHS.items()
    }
    history_v4.verify_model_resolution(
        documents["reduction"],
        detached=detached,
        detached_descriptors=detached_descriptors,
        authority=provider_authority,
        trusted_provider_root_authority_sha256=trusted_provider_root_authority_sha256,
        trusted_trust_root_receipt_sha256=trusted_trust_root_receipt_sha256,
    )
    return acquired, actual_inputs


def _verify_user_root(
    expected: dict[str, Any], actual: dict[str, Any]
) -> None:
    for field in (
        "platform",
        "effective_uid",
        "canonical_user_home_sha256",
        "environment_variable",
        "environment_present",
        "environment_value_sha256",
        "selected_root_sha256",
        "selection_basis",
    ):
        if expected.get(field) != actual.get(field):
            history_v4.fail("E_USER_ROOT_AUTHORITY", field)


def _replay_raw_sources(
    documents: dict[str, dict[str, Any]],
    *,
    key: bytes,
    salt: bytes,
    private_native_map: list[dict[str, str]],
) -> list[str]:
    history = documents["history"]
    ledger = documents["ledger"]
    roots = {item["platform"]: item for item in history["user_roots"]}
    acquired_by_key: dict[
        tuple[str, str], tuple[str, dict[str, Any], bytes]
    ] = {}
    home = Path.home().resolve(strict=True)
    for platform in ("codex", "claude-code"):
        selected, receipt = history_v4.select_user_root(platform, home=home)
        expected_root = roots.get(platform)
        if expected_root is None:
            history_v4.fail("E_USER_ROOT_SET_MISMATCH", platform)
        _verify_user_root(expected_root, receipt)
        allowed = (
            ["sessions/**/*.jsonl", "archived_sessions/*.jsonl"]
            if platform == "codex"
            else ["projects/**/*.jsonl"]
        )
        if expected_root["relative_path_allowlist"] != allowed:
            history_v4.fail("E_USER_ROOT_AUTHORITY", "relative path allowlist")
        acquired = history_v4.acquire_allowed_tree(
            selected,
            allowed,
            max_file_bytes=history["limits"]["max_file_bytes"],
            max_total_bytes=history["limits"]["max_total_bytes"],
        )
        for relative, (descriptor, payload) in acquired.items():
            key_tuple = (platform, descriptor["relative_path_sha256"])
            acquired_by_key[key_tuple] = (relative, descriptor, payload)

    sources_by_key = {
        (item["platform"], item["relative_path_sha256"]): item
        for item in history["sources"]
    }
    if len(sources_by_key) != len(history["sources"]):
        history_v4.fail("E_RAW_SNAPSHOT_REBUILD_REQUIRED", "duplicate source path")
    if set(acquired_by_key) != set(sources_by_key):
        history_v4.fail(
            "E_RAW_SNAPSHOT_REBUILD_REQUIRED", "live source set is not exact"
        )

    scripts_root = Path(__file__).resolve().parent
    adapter_descriptor, adapter_payload = history_v4.acquire_file(
        scripts_root,
        "normalize_codex_history.py",
        max_bytes=history["limits"]["max_file_bytes"],
    )
    history_v4.verify_adapter_implementations(
        history,
        {
            "codex-history-jsonl": (adapter_descriptor, adapter_payload),
            "claude-code-history-jsonl": (adapter_descriptor, adapter_payload),
        },
    )

    nodes = {
        (item["source_id"], item["source_record_ordinal"]): item
        for item in ledger["native_nodes"]
    }
    semantic_records = {
        (item["source_id"], item["source_record_ordinal"]): item
        for item in ledger["records"]
    }
    cutoff = history_v4.parse_time(history["cutoff"]["inclusive_at"], "cutoff")
    excluded_record_ids = {
        item["record_id"] for item in history["exclusion_ledger"]["records"]
    }
    projected_native: dict[tuple[str, str, str], dict[str, str]] = {}
    total_records = 0
    actual_source_sha256s: list[str] = []
    for source_key in sorted(sources_by_key):
        source = sources_by_key[source_key]
        relative, descriptor, payload = acquired_by_key[source_key]
        if (
            source["relative_path_sha256"] != descriptor["relative_path_sha256"]
            or source["snapshot"]["relative_path_sha256"]
            != descriptor["relative_path_sha256"]
            or not history_v4._descriptor_matches(source["snapshot"], descriptor)
        ):
            history_v4.fail("E_RAW_SNAPSHOT_REBUILD_REQUIRED", relative)
        projection = normalize_codex_history.project(
            platform=source["platform"],
            source_id=source["source_id"],
            descriptor=descriptor,
            payload=payload,
            identity_key=key,
            index_salt=salt,
        )
        total_records += projection["record_count"]
        if total_records > history["limits"]["max_records"]:
            history_v4.fail("E_ADAPTER_RECORD_LIMIT")
        actual_source_sha256s.append(descriptor["sha256"])
        source_nodes = [
            item for item in ledger["native_nodes"] if item["source_id"] == source["source_id"]
        ]
        dispositions = {
            "semantic": sum(item["record_disposition"] == "semantic" for item in source_nodes),
            "nonsemantic": sum(
                item["record_disposition"] == "non-semantic" for item in source_nodes
            ),
            "excluded": sum(item["record_disposition"] == "excluded" for item in source_nodes),
        }
        if (
            source["parsed_record_count"] != projection["record_count"]
            or source["parsed_record_count"] != len(source_nodes)
            or source["semantic_record_count"] != dispositions["semantic"]
            or source["nonsemantic_record_count"] != dispositions["nonsemantic"]
            or source["excluded_record_count"] != dispositions["excluded"]
        ):
            history_v4.fail("E_SOURCE_ACCOUNTING_MISMATCH", source["source_id"])
        for item in projection["native_map"]:
            identity_tuple = (
                item["platform"], item["native_type"], item["native_value"]
            )
            previous = projected_native.setdefault(identity_tuple, item)
            if previous != item:
                history_v4.fail(
                    "E_NATIVE_ID_INVENTORY_INCOMPLETE", "native identity collision"
                )
        for projected in projection["records"]:
            identity_tuple = (source["source_id"], projected["source_record_ordinal"])
            node = nodes.get(identity_tuple)
            if node is None:
                history_v4.fail("E_NATIVE_LINEAGE_MISMATCH", str(identity_tuple))
            expected_node_fields = {
                "platform": source["platform"],
                "native_type": projected["native_type"],
                "native_hmac": projected["native_hmac"],
                "parent_native_hmac": projected["parent_native_hmac"],
                "node_id": projected["node_id"],
                "record_id": projected["record_id"],
                "parent_id": projected["parent_id"],
                "namespace_id": projected["namespace_id"],
                "project_family_id": projected["project_family_id"],
                "classification": projected["classification"],
                "classification_basis": projected["classification_basis"],
                "occurred_at": projected["timestamp"],
            }
            if any(node.get(field) != value for field, value in expected_node_fields.items()):
                history_v4.fail("E_NATIVE_LINEAGE_MISMATCH", node["node_id"])
            after_cutoff = history_v4.parse_time(
                projected["timestamp"], "raw record timestamp"
            ) > cutoff
            expected_disposition = (
                "excluded"
                if after_cutoff or projected["record_id"] in excluded_record_ids
                else ("semantic" if projected["redacted_text"] is not None else "non-semantic")
            )
            if (
                node["after_cutoff"] is not after_cutoff
                or node["record_disposition"] != expected_disposition
            ):
                history_v4.fail(
                    "E_SOURCE_ACCOUNTING_MISMATCH", "raw disposition projection"
                )
            if projected["root_id"] is not None and node["root_id"] != projected["root_id"]:
                history_v4.fail("E_NATIVE_LINEAGE_MISMATCH", "root derivation")
            record = semantic_records.get(identity_tuple)
            if node["record_disposition"] == "semantic":
                if record is None:
                    history_v4.fail("E_SEMANTIC_LEDGER_REBUILD_REQUIRED", node["record_id"])
                expected_record_fields = {
                    "record_id": projected["record_id"],
                    "platform": source["platform"],
                    "raw_sha256": descriptor["sha256"],
                    "field": projected["field"],
                    "redacted_text": projected["redacted_text"],
                    "classification": projected["classification"],
                    "classification_basis": projected["classification_basis"],
                    "namespace_id": projected["namespace_id"],
                    "project_family_id": projected["project_family_id"],
                }
                if any(
                    record.get(field) != value
                    for field, value in expected_record_fields.items()
                ) or any(
                    record["locator"].get(field) != value
                    for field, value in {
                        "source_id": source["source_id"],
                        "event_ordinal": projected["source_record_ordinal"],
                        "line": projected["source_record_ordinal"],
                        "field": projected["field"],
                        "json_pointer": projected["json_pointer"],
                        "raw_sha256": descriptor["sha256"],
                        "adapter_id": source["adapter_id"],
                        "adapter_version": source["adapter_version"],
                    }.items()
                ):
                    history_v4.fail(
                        "E_SEMANTIC_LEDGER_REBUILD_REQUIRED", node["record_id"]
                    )
                if len(record["redacted_text"].encode()) > history["limits"][
                    "max_text_bytes"
                ]:
                    history_v4.fail("E_ADAPTER_TEXT_LIMIT", node["record_id"])
            elif record is not None:
                history_v4.fail("E_SEMANTIC_LEDGER_REBUILD_REQUIRED", node["record_id"])

    expected_private = {
        (item["platform"], item["native_type"], item["native_value"]): item
        for item in private_native_map
    }
    if len(expected_private) != len(private_native_map) or projected_native != expected_private:
        history_v4.fail("E_NATIVE_ID_INVENTORY_INCOMPLETE", "raw/native-map bijection")

    raw_receipt = documents["evidence"]["bindings"]["raw_reopen_receipt"]
    expected_receipt_body = {
        "schema_version": "raw-reopen-receipt/v2",
        "source_descriptor_sha256s": sorted(actual_source_sha256s),
        "source_ids": sorted(item["source_id"] for item in history["sources"]),
    }
    expected_receipt_body["receipt_sha256"] = history_v4.D(
        "raw-reopen-receipt/v2", expected_receipt_body
    )
    if history_v4.without(raw_receipt, "descriptor") != expected_receipt_body:
        history_v4.fail("E_RAW_REOPEN_REQUIRED", "live source receipt")
    return [item["native_value"] for item in private_native_map]


def main() -> int:
    args = parser().parse_args()
    if args.diagnostic_without_raw_reopen:
        print(
            json.dumps(
                history_v4.diagnostic_document(
                    "E_RAW_REOPEN_REQUIRED",
                    "authoritative validation requires descriptor reopening",
                ),
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2
    try:
        if (
            args.private_index_root is None
            or args.authority_root is None
            or args.trusted_provider_root_authority_sha256 is None
            or args.trusted_trust_root_receipt_sha256 is None
        ):
            history_v4.fail(
                "E_RAW_REOPEN_REQUIRED",
                "private index and independently pinned authority roots are required",
            )
        public_acquired = history_v4.acquire_exact_bundle(
            args.bundle_root,
            DOCUMENT_PATHS.values(),
            max_file_bytes=args.max_file_bytes,
            max_total_bytes=args.max_total_bytes,
        )
        documents = _load_set(public_acquired, DOCUMENT_PATHS)
        key, salt, native_map = _reopen_private_index(
            args.private_index_root,
            documents,
            max_file_bytes=args.max_file_bytes,
            max_total_bytes=args.max_total_bytes,
        )
        _reopen_authority(
            args.authority_root,
            documents,
            trusted_provider_root_authority_sha256=args.trusted_provider_root_authority_sha256,
            trusted_trust_root_receipt_sha256=args.trusted_trust_root_receipt_sha256,
            max_file_bytes=args.max_file_bytes,
            max_total_bytes=args.max_total_bytes,
        )
        native_values = _replay_raw_sources(
            documents,
            key=key,
            salt=salt,
            private_native_map=native_map,
        )
        history_v4.validate_successor_chain(
            documents,
            authoritative_raw_reopen=True,
            exact_model_available=True,
            native_values=native_values,
        )
    except (history_v4.HistoryV4Error, OSError) as exc:
        code = exc.code if isinstance(exc, history_v4.HistoryV4Error) else "E_IO"
        print(
            json.dumps(
                history_v4.diagnostic_document(code, str(exc)),
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 1
    print(
        json.dumps(
            {
                "schema_version": "history-validation-result/v4",
                "authoritative": True,
                "ok": True,
                "index_id": documents["index"]["index_id"],
                "history_index_sha256": documents["index"]["history_index_sha256"],
                "evidence_sha256": documents["evidence"]["evidence_sha256"],
                "publication_sha256": documents["publication"]["publication_sha256"],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
