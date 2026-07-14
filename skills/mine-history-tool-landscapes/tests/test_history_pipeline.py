from __future__ import annotations

import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILL = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


indexer = load_module("history_indexer", SKILL / "scripts" / "index_agent_history.py")
validator = load_module("history_validator", SKILL / "scripts" / "validate_history_evidence.py")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


class HistoryPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="history-synthetic-")
        self.base = Path(self.temp.name)
        self.source_root = self.base / "sources"
        self.source_root.mkdir()
        self.source_path = self.source_root / "normalized.jsonl"
        self.key = self.base / "id-key"
        self.key.write_bytes(b"synthetic-key-material-32-bytes!!")
        self.key.chmod(0o600)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def default_rows(self) -> list[dict]:
        return [
            {
                "native_session_id": "hist-root-0001",
                "native_aliases": ["hist-alias-0001"],
                "started_at": "2026-01-01T00:00:00Z",
                "role": "root",
                "recurrence_class": "user-intent",
                "classification_basis": "reducer-reviewed",
                "namespace": "history-namespace",
                "root_intent_hash": "a" * 16,
                "project_family_hash": "b" * 16,
                "source_locator": "root-locator",
            },
            {
                "native_session_id": "hist-child-0001",
                "native_parent_id": "hist-root-0001",
                "started_at": "2026-01-01T00:01:00Z",
                "role": "child",
                "recurrence_class": "delegated",
                "classification_basis": "native-metadata",
                "namespace": "history-namespace",
                "source_locator": "child-locator",
            },
            {
                "native_session_id": "active-root-0001",
                "started_at": "2026-02-01T00:00:00Z",
                "role": "root",
                "recurrence_class": "user-intent",
                "classification_basis": "reducer-reviewed",
                "namespace": "active-namespace",
                "root_intent_hash": "c" * 16,
                "project_family_hash": "d" * 16,
                "source_locator": "active-locator",
            },
        ]

    def source_contract(self, *, origin="local", state="frozen", authorization=None, cutoff="2026-02-01T00:00:00Z") -> dict:
        if authorization is None:
            authorization = {"kind": "local-default"}
        return {
            "schema_version": "history-sources/v2",
            "cutoff_at": cutoff,
            "cutoff_attestation": {
                "kind": "pre-discovery",
                "attested_at": "2026-02-02T00:00:00Z",
                "authority": "synthetic-test",
            },
            "retention": {"disposition": "delete-after-validation"},
            "sources": [
                {
                    "source_id": "local-source",
                    "platform": "codex",
                    "kind": "normalized-jsonl",
                    "path": str(self.source_path),
                    "authorized_root": str(self.source_root),
                    "state": state,
                    "origin": origin,
                    "authorization": authorization,
                }
            ],
        }

    def campaign_contract(self, *, start="2026-02-01T00:00:00Z") -> dict:
        return {
            "schema_version": "active-campaign/v2",
            "platform": "codex",
            "root_native_id": "active-root-0001",
            "root_aliases": [],
            "campaign_start": start,
        }

    def build(self, *, rows=None, source=None, campaign=True, name="index") -> Path:
        write_jsonl(self.source_path, rows or self.default_rows())
        source_path = self.base / f"sources-{name}.json"
        campaign_path = self.base / f"campaign-{name}.json"
        write_json(source_path, source or self.source_contract())
        if campaign:
            write_json(campaign_path, self.campaign_contract())
        out = self.base / name
        indexer.build(source_path, campaign_path if campaign else None, self.key, out)
        return out

    def valid_lineage(self, index: Path):
        roots = read_jsonl(index / "roots.jsonl")
        children = read_jsonl(index / "children.jsonl")
        root = roots[0]
        child = children[0]
        source = read_jsonl(index / "source-ledger.jsonl")[0]
        locator_hash = hashlib.sha256(b"root-locator\0role").hexdigest()
        evidence = {
            "schema_version": "history-evidence/v2",
            "mode": "lineage",
            "artifacts": [],
            "claims": [
                {
                    "id": "claim-root",
                    "statement": "A historical root was observed.",
                    "observed_at": "2026-02-02T00:00:00Z",
                    "evidence": [
                        {
                            "evidence_type": "agent-history",
                            "record_id": root["record_id"],
                            "state": "frozen",
                            "locator": {
                                "field": "role",
                                "ordinal": 1,
                                "source_id": source["source_id"],
                                "source_hash": source["snapshot_hash"],
                                "locator_hash": locator_hash,
                            },
                        }
                    ],
                }
            ],
            "conflicts": [],
            "recurrence": [
                {
                    "candidate_id": "candidate-one",
                    "support_record_ids": [root["record_id"]],
                    "root_intent_count": 1,
                    "project_family_count": 1,
                    "evidence_claim_ids": ["claim-root"],
                }
            ],
            "lineage_scope": {
                "target_record_ids": [root["record_id"]],
                "target_artifact_ids": [],
                "record_closure": sorted([root["record_id"], child["record_id"]]),
            },
            "lineage_edges": [
                {
                    "id": "edge-child",
                    "from": {"kind": "record", "id": root["record_id"]},
                    "to": {"kind": "record", "id": child["record_id"]},
                    "edge_type": "native",
                    "confidence": "high",
                    "evidence_claim_ids": ["claim-root"],
                }
            ],
        }
        manifest = read_json(index / "manifest.json")
        publication = {
            "schema_version": "history-publication/v2",
            "mode": "lineage",
            "summary": "Synthetic historical lineage.",
            "claim_ids": ["claim-root"],
            "record_ids": [root["record_id"]],
            "artifact_ids": [],
            "counts": {
                "roots": manifest["counts"]["included_roots"],
                "children": manifest["counts"]["included_children"],
                "unresolved": manifest["counts"]["included_unresolved"],
                "excluded": manifest["counts"]["primary_exclusions"],
                "project_families": manifest["counts"]["included_project_families"],
            },
            "source_manifest": [
                {
                    "source_id": source["source_id"],
                    "snapshot_hash": source["snapshot_hash"],
                    "state": source["state"],
                    "origin": source["origin"],
                }
            ],
            "provenance_ledger": [{"claim_id": "claim-root", "reference_count": 1}],
            "state_labels": {"live": 0, "frozen": 1},
            "lineage_scope": evidence["lineage_scope"],
            "lineage_edge_ids": ["edge-child"],
        }
        return evidence, publication

    def error_codes(self, index: Path, evidence: dict, publication: dict) -> set[str]:
        return {error["code"] for error in validator.Validator(index, evidence, publication).validate()}

    def test_valid_pipeline_and_strict_permissions(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        self.assertEqual([], validator.Validator(index, evidence, publication).validate())
        self.assertEqual(0o700, stat_mode(index))
        self.assertEqual(0o600, stat_mode(index / "manifest.json"))
        self.assertEqual(0o700, stat_mode(index / "private"))
        self.assertEqual(0o600, stat_mode(index / "private" / "native-map.jsonl"))

    def test_publication_redaction_rejects_security_payloads_and_keys(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        payloads = [
            ("github_pat_" + "A" * 24, "secret-leak"),
            ("-----BEGIN PRIVATE KEY-----", "secret-leak"),
            ("/secret", "path-leak"),
            (r"\\server\share\file", "path-leak"),
            ("hist-root-0001", "native-id-leak"),
            ("data:text/plain;base64,U2Vuc2l0aXZl", "url-leak"),
            ("custom-app:private-payload", "url-leak"),
            ("x:sensitive-payload", "url-leak"),
        ]
        for payload, code in payloads:
            with self.subTest(payload=payload):
                candidate = copy.deepcopy(publication)
                candidate["summary"] = payload
                self.assertIn(code, self.error_codes(index, evidence, candidate))
        candidate = copy.deepcopy(publication)
        candidate["github_pat_" + "B" * 24] = "value"
        codes = self.error_codes(index, evidence, candidate)
        self.assertIn("schema-keys", codes)
        self.assertIn("secret-leak", codes)

    def test_manifest_paths_are_rejected_before_digest(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        manifest = read_json(index / "manifest.json")
        manifest["file_hashes"]["/dev/zero"] = "0" * 64
        write_json(index / "manifest.json", manifest)
        (index / "manifest.json").chmod(0o600)
        with mock.patch.object(validator.Validator, "index_digest", side_effect=AssertionError("must not open")):
            codes = self.error_codes(index, evidence, publication)
        self.assertIn("index-file-set", codes)

    def test_metadata_smuggling_and_symlink_source_are_rejected(self):
        rows = self.default_rows()
        rows[0]["native_session_id"] = "github_pat_" + "A" * 24
        with self.assertRaises(indexer.ContractError):
            self.build(rows=rows, name="smuggle")
        write_jsonl(self.source_path, self.default_rows())
        target = self.source_root / "target.jsonl"
        self.source_path.replace(target)
        self.source_path.symlink_to(target)
        source_path = self.base / "symlink-source.json"
        write_json(source_path, self.source_contract())
        campaign_path = self.base / "symlink-campaign.json"
        write_json(campaign_path, self.campaign_contract())
        with self.assertRaises(indexer.ContractError):
            indexer.build(source_path, campaign_path, self.key, self.base / "symlink-index")

    def test_unhashable_alias_is_a_contract_error(self):
        rows = self.default_rows()
        rows[0]["native_aliases"] = [{"not": "a-string"}]
        with self.assertRaises(indexer.ContractError):
            self.build(rows=rows, name="bad-alias")

    def test_post_cutoff_descendant_cannot_seed_namespace(self):
        rows = [
            {
                "native_session_id": "historical-root-b",
                "started_at": "2026-02-01T12:00:00Z",
                "role": "root",
                "recurrence_class": "user-intent",
                "classification_basis": "reducer-reviewed",
                "namespace": "namespace-b",
                "root_intent_hash": "a" * 16,
                "source_locator": "history-b",
            },
            {
                "native_session_id": "active-root-0001",
                "started_at": "2026-02-01T00:00:00Z",
                "role": "root",
                "recurrence_class": "user-intent",
                "classification_basis": "reducer-reviewed",
                "namespace": "namespace-a",
                "root_intent_hash": "b" * 16,
                "source_locator": "active-a",
            },
            {
                "native_session_id": "after-cutoff-child",
                "native_parent_id": "active-root-0001",
                "started_at": "2026-02-03T00:00:00Z",
                "role": "child",
                "recurrence_class": "delegated",
                "classification_basis": "native-metadata",
                "namespace": "namespace-b",
                "source_locator": "future-b",
            },
        ]
        source = self.source_contract(cutoff="2026-02-02T00:00:00Z")
        index = self.build(rows=rows, source=source, name="cutoff")
        roots = read_jsonl(index / "roots.jsonl")
        self.assertEqual(1, len(roots))
        private = read_jsonl(index / "private" / "native-map.jsonl")
        included_id = roots[0]["record_id"]
        native = {row["record_id"]: row["native_session_id"] for row in private}
        self.assertEqual("historical-root-b", native[included_id])

    def test_campaign_chronology_and_key_permissions(self):
        write_jsonl(self.source_path, self.default_rows())
        source_path = self.base / "chronology-source.json"
        write_json(source_path, self.source_contract())
        campaign_path = self.base / "chronology-campaign.json"
        write_json(campaign_path, self.campaign_contract(start="2026-02-01T00:00:01Z"))
        with self.assertRaises(indexer.ContractError):
            indexer.build(source_path, campaign_path, self.key, self.base / "chronology")
        self.key.chmod(0o644)
        with self.assertRaises(indexer.ContractError):
            indexer.build(source_path, None, self.key, self.base / "bad-key")

    def test_ids_are_salted_per_index(self):
        first = self.build(name="first")
        second = self.build(name="second")
        first_root = read_jsonl(first / "roots.jsonl")[0]
        second_root = read_jsonl(second / "roots.jsonl")[0]
        self.assertNotEqual(first_root["record_id"], second_root["record_id"])
        self.assertNotEqual(first_root["namespace_hash"], second_root["namespace_hash"])
        self.assertNotEqual(first_root["root_intent_hash"], second_root["root_intent_hash"])

    def test_remote_receipt_must_be_frozen_and_hash_bound(self):
        source = self.source_contract(origin="remote-snapshot", state="live", authorization={"kind": "approved-snapshot"})
        with self.assertRaises(indexer.ContractError):
            self.build(source=source, name="remote-live")
        source = self.source_contract(
            origin="remote-snapshot",
            state="frozen",
            authorization={
                "kind": "approved-snapshot",
                "source_id": "local-source",
                "snapshot_sha256": "0" * 64,
                "approved_by": "synthetic-test",
                "captured_at": "2026-02-01T23:59:59Z",
                "approved_at": "2026-02-02T00:00:00Z",
                "scope": "history-metadata",
            },
        )
        with self.assertRaises(indexer.ContractError):
            self.build(source=source, name="remote-hash")

    def test_validator_inputs_reject_symlinks_special_files_and_oversize(self):
        real = self.base / "evidence-real.json"
        write_json(real, {"synthetic": True})
        linked = self.base / "evidence-link.json"
        linked.symlink_to(real)
        with self.assertRaises(ValueError):
            validator.read_json(linked)
        with self.assertRaises(ValueError):
            validator.read_json(self.source_root)
        oversize = self.base / "oversize.json"
        oversize.write_text(json.dumps({"payload": "x" * 128}), encoding="utf-8")
        old_limit = validator.MAX_PUBLIC_INPUT_BYTES
        try:
            validator.MAX_PUBLIC_INPUT_BYTES = 64
            with self.assertRaises(ValueError):
                validator.read_json(oversize)
        finally:
            validator.MAX_PUBLIC_INPUT_BYTES = old_limit

    def test_duplicate_json_keys_fail_closed_at_every_boundary(self):
        rows = self.default_rows()
        write_jsonl(self.source_path, rows)
        source_doc = self.source_contract()
        source_path = self.base / "duplicate-root-source.json"
        root_duplicate = json.dumps(source_doc)[:-1] + ',"schema_version":"history-sources/v2"}'
        source_path.write_text(root_duplicate, encoding="utf-8")
        out = self.base / "duplicate-root-index"
        argv = [
            "index_agent_history.py",
            "--source-contract",
            str(source_path),
            "--id-key-file",
            str(self.key),
            "--out",
            str(out),
        ]
        capture = io.StringIO()
        with mock.patch.object(indexer.sys, "argv", argv), contextlib.redirect_stdout(capture):
            self.assertEqual(2, indexer.main())
        self.assertFalse(out.exists())
        self.assertFalse(json.loads(capture.getvalue())["ok"])

        nested_path = self.base / "duplicate-nested-source.json"
        nested_text = json.dumps(source_doc, sort_keys=True).replace(
            '"authority": "synthetic-test"',
            '"authority": "synthetic-test", "authority": "duplicate"',
        )
        nested_path.write_text(nested_text, encoding="utf-8")
        with self.assertRaises(indexer.ContractError):
            indexer.build(nested_path, None, self.key, self.base / "duplicate-nested-index")
        self.assertFalse((self.base / "duplicate-nested-index").exists())

        duplicate_row_path = self.source_root / "duplicate-row.jsonl"
        duplicate_row_path.write_text(json.dumps(rows[0])[:-1] + ',"role":"root"}\n', encoding="utf-8")
        row_source = self.source_contract()
        row_source["sources"][0]["path"] = str(duplicate_row_path)
        row_source_path = self.base / "duplicate-row-source.json"
        write_json(row_source_path, row_source)
        with self.assertRaises(indexer.ContractError):
            indexer.build(row_source_path, None, self.key, self.base / "duplicate-row-index")
        self.assertFalse((self.base / "duplicate-row-index").exists())

        index = self.build(name="strict-json-index")
        evidence, publication = self.valid_lineage(index)
        evidence_path = self.base / "duplicate-evidence.json"
        publication_path = self.base / "strict-publication.json"
        evidence_path.write_text(json.dumps(evidence)[:-1] + ',"mode":"lineage"}', encoding="utf-8")
        write_json(publication_path, publication)
        capture = io.StringIO()
        argv = ["validate_history_evidence.py", "--index", str(index), "--evidence", str(evidence_path), "--publication", str(publication_path)]
        with mock.patch.object(validator.sys, "argv", argv), contextlib.redirect_stdout(capture):
            self.assertEqual(2, validator.main())
        self.assertEqual("read-error", json.loads(capture.getvalue())["errors"][0]["code"])

        write_json(evidence_path, evidence)
        publication_path.write_text(json.dumps(publication)[:-1] + ',"summary":"duplicate"}', encoding="utf-8")
        capture = io.StringIO()
        with mock.patch.object(validator.sys, "argv", argv), contextlib.redirect_stdout(capture):
            self.assertEqual(2, validator.main())
        self.assertEqual("read-error", json.loads(capture.getvalue())["errors"][0]["code"])

        manifest_path = index / "manifest.json"
        manifest = read_json(manifest_path)
        manifest_path.write_text(json.dumps(manifest)[:-1] + ',"schema_version":"history-index/v2"}', encoding="utf-8")
        manifest_path.chmod(0o600)
        codes = self.error_codes(index, evidence, publication)
        self.assertIn("index-read", codes)

    def test_index_integrity_exclusion_and_permission_checks(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        root_id = publication["record_ids"][0]
        exclusions = read_jsonl(index / "exclusion-ledger.jsonl")
        exclusions.append({"record_id": root_id, "reasons": ["after_cutoff"]})
        write_jsonl(index / "exclusion-ledger.jsonl", exclusions)
        (index / "exclusion-ledger.jsonl").chmod(0o600)
        manifest = read_json(index / "manifest.json")
        manifest["file_hashes"]["exclusion-ledger.jsonl"] = hashlib.sha256((index / "exclusion-ledger.jsonl").read_bytes()).hexdigest()
        core = {key: value for key, value in manifest.items() if key != "corpus_hash"}
        manifest["corpus_hash"] = hashlib.sha256(validator.canonical_json(core)).hexdigest()
        write_json(index / "manifest.json", manifest)
        (index / "manifest.json").chmod(0o600)
        self.assertIn("included-and-excluded", self.error_codes(index, evidence, publication))
        index.chmod(0o755)
        self.assertIn("unsafe-permissions", self.error_codes(index, evidence, publication))

    def test_private_observation_counts_reconcile_duplicates(self):
        rows = self.default_rows()
        rows.insert(1, copy.deepcopy(rows[0]))
        index = self.build(rows=rows, name="duplicate-observation")
        evidence, publication = self.valid_lineage(index)
        private_path = index / "private" / "native-map.jsonl"
        private_rows = read_jsonl(private_path)
        duplicate_row = next(row for row in private_rows if len(row["observations"]) == 2)
        duplicate_row["observations"].pop()
        write_jsonl(private_path, private_rows)
        private_path.chmod(0o600)
        manifest = read_json(index / "manifest.json")
        manifest["file_hashes"]["private/native-map.jsonl"] = hashlib.sha256(private_path.read_bytes()).hexdigest()
        core = {key: value for key, value in manifest.items() if key != "corpus_hash"}
        manifest["corpus_hash"] = hashlib.sha256(validator.canonical_json(core)).hexdigest()
        write_json(index / "manifest.json", manifest)
        (index / "manifest.json").chmod(0o600)
        self.assertIn("accounting-mismatch", self.error_codes(index, evidence, publication))

    def test_locator_must_match_observation(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        evidence["claims"][0]["evidence"][0]["locator"]["ordinal"] = 999999
        self.assertIn("unobserved-locator", self.error_codes(index, evidence, publication))
        evidence, publication = self.valid_lineage(index)
        evidence["claims"][0]["evidence"][0]["locator"]["field"] = "namespace"
        self.assertIn("unobserved-locator", self.error_codes(index, evidence, publication))

    def test_native_lineage_must_be_complete(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        evidence["lineage_edges"] = []
        publication["lineage_edge_ids"] = []
        self.assertIn("lineage-mismatch", self.error_codes(index, evidence, publication))

    def test_native_id_matching_required_schema_key_does_not_false_positive(self):
        rows = self.default_rows()
        rows[0]["native_session_id"] = "roots"
        rows[0]["native_aliases"] = []
        rows[1]["native_parent_id"] = "roots"
        index = self.build(rows=rows, name="schema-key-native")
        evidence, publication = self.valid_lineage(index)
        self.assertEqual([], validator.Validator(index, evidence, publication).validate())

    def test_deep_lineage_is_iterative(self):
        rows = [
            {
                "native_session_id": "deep-root-0000",
                "started_at": "2026-01-01T00:00:00Z",
                "role": "root",
                "recurrence_class": "user-intent",
                "classification_basis": "reducer-reviewed",
                "root_intent_hash": "a" * 16,
                "source_locator": "deep-loc-0000",
            }
        ]
        for index in range(1, 1100):
            rows.append(
                {
                    "native_session_id": f"deep-child-{index:04d}",
                    "native_parent_id": "deep-root-0000" if index == 1 else f"deep-child-{index - 1:04d}",
                    "started_at": "2026-01-01T00:00:00Z",
                    "role": "child",
                    "recurrence_class": "delegated",
                    "classification_basis": "native-metadata",
                    "source_locator": f"deep-loc-{index:04d}",
                }
            )
        rows.append(self.default_rows()[2])
        index = self.build(rows=rows, name="deep-lineage")
        self.assertEqual(1099, read_json(index / "manifest.json")["counts"]["included_children"])

    def test_standalone_artifact_is_grounded_without_fake_record(self):
        index = self.build(rows=[self.default_rows()[0]], campaign=False, name="artifact-index")
        manifest = read_json(index / "manifest.json")
        source = read_jsonl(index / "source-ledger.jsonl")[0]
        artifact_hash = "e" * 64
        evidence = {
            "schema_version": "history-evidence/v2",
            "mode": "lineage",
            "artifacts": [
                {
                    "id": "artifact-one",
                    "kind": "artifact",
                    "state": "frozen",
                    "snapshot_hash": artifact_hash,
                    "observed_at": "2026-02-02T00:00:00Z",
                }
            ],
            "claims": [
                {
                    "id": "claim-artifact",
                    "statement": "A frozen artifact was observed.",
                    "observed_at": "2026-02-02T00:00:00Z",
                    "evidence": [
                        {
                            "evidence_type": "artifact",
                            "artifact_id": "artifact-one",
                            "state": "frozen",
                            "locator": {"field": "metadata", "ordinal": 0, "snapshot_hash": artifact_hash},
                        }
                    ],
                }
            ],
            "conflicts": [],
            "recurrence": [],
            "lineage_scope": {
                "target_record_ids": [],
                "target_artifact_ids": ["artifact-one"],
                "record_closure": [],
            },
            "lineage_edges": [],
        }
        publication = {
            "schema_version": "history-publication/v2",
            "mode": "lineage",
            "summary": "Synthetic artifact evidence.",
            "claim_ids": ["claim-artifact"],
            "record_ids": [],
            "artifact_ids": ["artifact-one"],
            "counts": {
                "roots": manifest["counts"]["included_roots"],
                "children": manifest["counts"]["included_children"],
                "unresolved": manifest["counts"]["included_unresolved"],
                "excluded": manifest["counts"]["primary_exclusions"],
                "project_families": manifest["counts"]["included_project_families"],
            },
            "source_manifest": [
                {
                    "source_id": source["source_id"],
                    "snapshot_hash": source["snapshot_hash"],
                    "state": source["state"],
                    "origin": source["origin"],
                }
            ],
            "provenance_ledger": [{"claim_id": "claim-artifact", "reference_count": 1}],
            "state_labels": {"live": 0, "frozen": 1},
            "lineage_scope": evidence["lineage_scope"],
            "lineage_edge_ids": [],
        }
        self.assertEqual([], validator.Validator(index, evidence, publication).validate())
        evidence["artifacts"].append(
            {
                "id": "artifact-ungrounded",
                "kind": "artifact",
                "state": "frozen",
                "snapshot_hash": "c" * 64,
                "observed_at": "2026-02-02T00:00:00Z",
            }
        )
        evidence["lineage_scope"]["target_artifact_ids"].append("artifact-ungrounded")
        self.assertIn("ungrounded-lineage-target", self.error_codes(index, evidence, publication))
        evidence["lineage_scope"]["target_artifact_ids"].pop()
        evidence["artifacts"].pop()
        evidence["claims"][0]["evidence"][0]["locator"]["snapshot_hash"] = "f" * 64
        self.assertIn("artifact-mismatch", self.error_codes(index, evidence, publication))

    def test_optional_campaign_retention_and_source_bounds(self):
        rows = [self.default_rows()[0]]
        index = self.build(rows=rows, campaign=False, name="cutoff-only")
        self.assertEqual("trusted-cutoff", read_json(index / "manifest.json")["exclusion_basis"])
        source = self.source_contract()
        source.pop("retention")
        with self.assertRaises(indexer.ContractError):
            self.build(rows=rows, source=source, campaign=False, name="no-retention")
        old_limit = indexer.MAX_SOURCE_BYTES
        try:
            indexer.MAX_SOURCE_BYTES = 64
            with self.assertRaises(indexer.ContractError):
                self.build(rows=rows, campaign=False, name="oversize")
        finally:
            indexer.MAX_SOURCE_BYTES = old_limit

    def test_aggregate_source_limits_and_in_place_mutation(self):
        rows = [self.default_rows()[0]]
        write_jsonl(self.source_path, rows)
        source = self.source_contract()
        second = copy.deepcopy(source["sources"][0])
        second["source_id"] = "second-source"
        source["sources"].append(second)
        source_path = self.base / "many-sources.json"
        write_json(source_path, source)
        old_sources = indexer.MAX_SOURCES
        try:
            indexer.MAX_SOURCES = 1
            with self.assertRaises(indexer.ContractError):
                indexer.build(source_path, None, self.key, self.base / "many-index")
        finally:
            indexer.MAX_SOURCES = old_sources
        old_total = indexer.MAX_TOTAL_SOURCE_BYTES
        try:
            indexer.MAX_TOTAL_SOURCE_BYTES = 10
            with self.assertRaises(indexer.ContractError):
                self.build(rows=rows, campaign=False, name="aggregate-bytes")
        finally:
            indexer.MAX_TOTAL_SOURCE_BYTES = old_total
        write_jsonl(self.source_path, rows)
        with self.assertRaises(indexer.ContractError):
            with indexer.open_beneath(self.source_path, self.source_root) as handle:
                handle.read()
                self.source_path.write_text("{}\n", encoding="utf-8")

    def test_workflow_duplicate_decisions_and_publication_completeness(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        evidence["mode"] = "workflow-mining"
        evidence.pop("lineage_scope")
        evidence["capability_inventory"] = [
            {"id": "cap-one", "name": "Capability", "kind": "skill", "snapshot_hash": "a" * 64}
        ]
        evidence["overlap_map"] = [
            {
                "id": "overlap-one",
                "candidate_id": "candidate-one",
                "matched_capability_ids": ["cap-one"],
                "assessment": "partial",
                "rationale": "Partial overlap.",
                "evidence_claim_ids": ["claim-root"],
            }
        ]
        decision = {
            "candidate_id": "candidate-one",
            "decision": "reject",
            "recurrence_candidate_id": "candidate-one",
            "overlap_id": "overlap-one",
            "evidence_claim_ids": ["claim-root"],
        }
        evidence["decisions"] = [decision, copy.deepcopy(decision)]
        publication["mode"] = "workflow-mining"
        publication.pop("lineage_scope")
        publication.pop("lineage_edge_ids")
        publication["capability_ids"] = ["cap-one"]
        publication["overlap_ids"] = ["overlap-one"]
        publication["decision_candidate_ids"] = ["candidate-one"]
        self.assertIn("duplicate-decision", self.error_codes(index, evidence, publication))
        publication.pop("source_manifest")
        self.assertIn("schema-keys", self.error_codes(index, evidence, publication))

    def test_workflow_recurrence_candidate_cannot_be_orphaned(self):
        index = self.build()
        evidence, publication = self.valid_lineage(index)
        evidence["mode"] = "workflow-mining"
        evidence.pop("lineage_scope")
        evidence["recurrence"].append(
            {
                "candidate_id": "orphan-candidate",
                "support_record_ids": evidence["recurrence"][0]["support_record_ids"],
                "root_intent_count": 1,
                "project_family_count": 1,
                "evidence_claim_ids": ["claim-root"],
            }
        )
        evidence["capability_inventory"] = [
            {"id": "cap-one", "name": "Capability", "kind": "skill", "snapshot_hash": "a" * 64}
        ]
        evidence["overlap_map"] = [
            {
                "id": "overlap-one",
                "candidate_id": "candidate-one",
                "matched_capability_ids": ["cap-one"],
                "assessment": "partial",
                "rationale": "Partial overlap.",
                "evidence_claim_ids": ["claim-root"],
            }
        ]
        evidence["decisions"] = [
            {
                "candidate_id": "candidate-one",
                "decision": "reject",
                "recurrence_candidate_id": "candidate-one",
                "overlap_id": "overlap-one",
                "evidence_claim_ids": ["claim-root"],
            }
        ]
        publication["mode"] = "workflow-mining"
        publication.pop("lineage_scope")
        publication.pop("lineage_edge_ids")
        publication["capability_ids"] = ["cap-one"]
        publication["overlap_ids"] = ["overlap-one"]
        publication["decision_candidate_ids"] = ["candidate-one"]
        self.assertIn("orphan-candidate", self.error_codes(index, evidence, publication))

    def test_synthetic_roots_cannot_satisfy_create_threshold(self):
        rows = []
        for number, intent in enumerate(("1", "2", "3"), 1):
            rows.append(
                {
                    "native_session_id": f"synthetic-root-{number}",
                    "started_at": f"2026-01-0{number}T00:00:00Z",
                    "role": "root",
                    "recurrence_class": "synthetic",
                    "classification_basis": "reducer-reviewed",
                    "root_intent_hash": intent * 16,
                    "source_locator": f"synthetic-locator-{number}",
                }
            )
        rows.append(self.default_rows()[2])
        index = self.build(rows=rows, name="synthetic-roots")
        roots = read_jsonl(index / "roots.jsonl")
        self.assertEqual([False, False, False], [row["eligible_for_recurrence"] for row in roots])
        source = read_jsonl(index / "source-ledger.jsonl")[0]
        claims = []
        for ordinal, record in enumerate(sorted(roots, key=lambda row: row["started_at"]), 1):
            claims.append(
                {
                    "id": f"claim-synthetic-{ordinal}",
                    "statement": f"Synthetic observation {ordinal}.",
                    "observed_at": "2026-02-02T00:00:00Z",
                    "evidence": [
                        {
                            "evidence_type": "agent-history",
                            "record_id": record["record_id"],
                            "state": "frozen",
                            "locator": {
                                "field": "role",
                                "ordinal": ordinal,
                                "source_id": source["source_id"],
                                "source_hash": source["snapshot_hash"],
                                "locator_hash": hashlib.sha256(f"synthetic-locator-{ordinal}\0role".encode()).hexdigest(),
                            },
                        }
                    ],
                }
            )
        claim_ids = [claim["id"] for claim in claims]
        evidence = {
            "schema_version": "history-evidence/v2",
            "mode": "workflow-mining",
            "artifacts": [],
            "claims": claims,
            "conflicts": [],
            "lineage_edges": [],
            "recurrence": [
                {
                    "candidate_id": "synthetic-candidate",
                    "support_record_ids": [row["record_id"] for row in roots],
                    "root_intent_count": 3,
                    "project_family_count": 0,
                    "evidence_claim_ids": claim_ids,
                }
            ],
            "capability_inventory": [
                {"id": "cap-one", "name": "Capability", "kind": "skill", "snapshot_hash": "a" * 64}
            ],
            "overlap_map": [
                {
                    "id": "overlap-synthetic",
                    "candidate_id": "synthetic-candidate",
                    "matched_capability_ids": ["cap-one"],
                    "assessment": "partial",
                    "rationale": "Synthetic overlap.",
                    "evidence_claim_ids": claim_ids,
                }
            ],
            "decisions": [
                {
                    "candidate_id": "synthetic-candidate",
                    "decision": "create",
                    "recurrence_candidate_id": "synthetic-candidate",
                    "overlap_id": "overlap-synthetic",
                    "evidence_claim_ids": claim_ids,
                }
            ],
        }
        manifest = read_json(index / "manifest.json")
        publication = {
            "schema_version": "history-publication/v2",
            "mode": "workflow-mining",
            "summary": "Synthetic traffic classification check.",
            "claim_ids": claim_ids,
            "record_ids": [row["record_id"] for row in roots],
            "artifact_ids": [],
            "counts": {
                "roots": manifest["counts"]["included_roots"],
                "children": manifest["counts"]["included_children"],
                "unresolved": manifest["counts"]["included_unresolved"],
                "excluded": manifest["counts"]["primary_exclusions"],
                "project_families": manifest["counts"]["included_project_families"],
            },
            "source_manifest": [
                {"source_id": source["source_id"], "snapshot_hash": source["snapshot_hash"], "state": source["state"], "origin": source["origin"]}
            ],
            "provenance_ledger": [{"claim_id": claim_id, "reference_count": 1} for claim_id in sorted(claim_ids)],
            "state_labels": {"live": 0, "frozen": 3},
            "capability_ids": ["cap-one"],
            "overlap_ids": ["overlap-synthetic"],
            "decision_candidate_ids": ["synthetic-candidate"],
        }
        codes = self.error_codes(index, evidence, publication)
        self.assertIn("ineligible-support", codes)
        self.assertIn("insufficient-recurrence", codes)


def stat_mode(path: Path) -> int:
    return path.stat().st_mode & 0o777


if __name__ == "__main__":
    unittest.main()
