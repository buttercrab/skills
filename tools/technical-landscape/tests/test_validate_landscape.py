from __future__ import annotations

import copy
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_landscape.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.dont_write_bytecode = True
MODULE = runpy.run_path(str(SCRIPT))
Validator = MODULE["Validator"]
TOP_KEYS = MODULE["TOP_KEYS"]


def valid_landscape() -> dict:
    return json.loads((FIXTURES / "valid_landscape.json").read_text(encoding="utf-8"))


class LandscapeValidatorTests(unittest.TestCase):
    def errors(self, data: dict) -> list[dict[str, str]]:
        return Validator(copy.deepcopy(data)).validate()

    def assert_has_code(self, errors: list[dict[str, str]], code: str) -> None:
        self.assertIn(code, {error["code"] for error in errors}, errors)

    def test_valid_v2_fixture(self) -> None:
        self.assertEqual([], self.errors(valid_landscape()))

    def test_machine_schema_root_matches_validator(self) -> None:
        schema = json.loads((ROOT / "references" / "landscape-v2.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(TOP_KEYS, set(schema["required"]))
        self.assertEqual(TOP_KEYS, set(schema["properties"]))

    def test_valid_fixture_passes_full_machine_schema(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is not installed")
        schema = json.loads((ROOT / "references" / "landscape-v2.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(valid_landscape(), schema)

    def test_cli_accepts_valid_fixture(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(FIXTURES / "valid_landscape.json")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])

    def test_cli_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("usage: validate_landscape.py", result.stdout)

    def test_cli_rejects_non_json_nan(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(FIXTURES / "invalid_nan.json")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("parse-error", json.loads(result.stdout)["errors"][0]["code"])

    def assert_cli_rejects_duplicate_key(self, content: str) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "duplicate.json"
            path.write_text(content, encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path)], check=False, capture_output=True, text=True)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["valid"])
        self.assertEqual("duplicate-key", payload["errors"][0]["code"])
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_rejects_duplicate_root_key(self) -> None:
        self.assert_cli_rejects_duplicate_key(
            '{"schema_version":"map-technical-landscapes/v1","schema_version":"map-technical-landscapes/v2"}'
        )

    def test_cli_rejects_duplicate_nested_key(self) -> None:
        self.assert_cli_rejects_duplicate_key(
            '{"schema_version":"map-technical-landscapes/v2","scope":{"question":"first","question":"shadow"}}'
        )

    def test_direct_validator_rejects_nonfinite_number(self) -> None:
        data = valid_landscape()
        data["candidates"][0]["comparison"]["latency"]["value"] = float("nan")
        self.assert_has_code(self.errors(data), "ungrounded-cell")

    def test_duplicate_alias_is_rejected_after_normalization(self) -> None:
        data = valid_landscape()
        data["candidates"][0]["aliases"] = ["Alias", "  ALIAS  "]
        self.assert_has_code(self.errors(data), "duplicate-value")

    def test_alias_requires_identity_decision_and_discovery_record(self) -> None:
        data = valid_landscape()
        data["candidates"][0]["aliases"] = ["System 1"]
        self.assert_has_code(self.errors(data), "missing-alias-decision")

    def test_unknown_cell_requires_matching_unknown_field_gap(self) -> None:
        data = valid_landscape()
        data["coverage"]["gaps"].append(
            {
                "id": "wrong-gap",
                "kind": "coverage-other",
                "description": "Not field-specific",
                "candidate_ids": ["system-one"],
                "claim_ids": [],
                "source_ids": [],
                "search_ids": [],
                "field_ids": ["latency"],
            }
        )
        data["candidates"][0]["comparison"]["latency"] = {
            "status": "unknown",
            "value": None,
            "claim_ids": [],
            "gap_ids": ["wrong-gap"],
            "note": "Unknown",
        }
        self.assert_has_code(self.errors(data), "invalid-unknown")

    def test_not_applicable_cell_requires_candidate_and_field_claim(self) -> None:
        data = valid_landscape()
        data["claims"][0]["field_id"] = None
        data["candidates"][0]["comparison"]["latency"] = {
            "status": "not-applicable",
            "value": None,
            "claim_ids": ["claim-latency"],
            "gap_ids": [],
            "note": "Not applicable",
        }
        self.assert_has_code(self.errors(data), "invalid-not-applicable")

    def test_inference_requires_distinct_source_equivalence_groups(self) -> None:
        data = valid_landscape()
        data["sources"][1]["equivalence_group"] = "paper-one"
        data["claims"][0]["epistemic_status"] = "inferred"
        data["claims"][0]["source_ids"] = ["source-paper", "source-repo"]
        data["candidates"][0]["comparison"]["latency"]["status"] = "inferred"
        self.assert_has_code(self.errors(data), "insufficient-independent-evidence")

    def test_duplicate_locator_is_rejected(self) -> None:
        data = valid_landscape()
        data["sources"][1]["locator"] = {"type": "doi", "value": "10.1234/EXAMPLE.1"}
        self.assert_has_code(self.errors(data), "duplicate-locator")

    def test_password_only_url_is_rejected(self) -> None:
        data = valid_landscape()
        data["sources"][1]["locator"] = {"type": "url", "value": "https://:secret@example.com/repository"}
        self.assert_has_code(self.errors(data), "invalid-locator")

    def test_secret_query_and_fragment_parameters_are_rejected(self) -> None:
        for value in (
            "https://example.com/repository?access_token=secret",
            "https://example.com/repository#api_key=secret",
        ):
            with self.subTest(value=value):
                data = valid_landscape()
                data["sources"][1]["locator"] = {"type": "url", "value": value}
                self.assert_has_code(self.errors(data), "invalid-locator")

    def test_timestamp_without_seconds_is_rejected(self) -> None:
        data = valid_landscape()
        data["scope"]["frozen_at"] = "2026-07-12T12:00+09:00"
        self.assert_has_code(self.errors(data), "invalid-timestamp")

    def test_commit_locator_requires_repository_context(self) -> None:
        data = valid_landscape()
        data["sources"][1]["locator"] = {"type": "commit", "value": "a" * 40}
        errors = self.errors(data)
        self.assert_has_code(errors, "missing-field")
        self.assert_has_code(errors, "unknown-field")

    def test_failed_search_cannot_prove_stop_even_with_gap(self) -> None:
        data = valid_landscape()
        search = data["coverage"]["searches"][0]
        search["status"] = "failed"
        search["hit_count"] = None
        search["note"] = "Network failure"
        data["coverage"]["gaps"].append(
            {
                "id": "failed-search-gap",
                "kind": "failed-search",
                "description": "Search failed",
                "candidate_ids": [],
                "claim_ids": [],
                "source_ids": [],
                "search_ids": ["search-name-paper"],
                "field_ids": [],
            }
        )
        self.assert_has_code(self.errors(data), "invalid-stop-evidence")

    def test_stop_evidence_must_be_chronological(self) -> None:
        data = valid_landscape()
        data["coverage"]["stop_assessment"]["search_ids"].reverse()
        self.assert_has_code(self.errors(data), "unordered-stop-evidence")

    def test_stop_evidence_must_include_latest_completed_search(self) -> None:
        data = valid_landscape()
        later = copy.deepcopy(data["coverage"]["searches"][1])
        later["id"] = "search-later"
        later["started_at"] = "2026-07-12T12:30:00+09:00"
        later["hit_count"] = 1
        later["new_candidate_ids"] = ["system-one"]
        data["coverage"]["searches"].append(later)
        self.assert_has_code(self.errors(data), "stale-stop-evidence")

    def test_stop_evidence_cannot_omit_middle_completed_search(self) -> None:
        data = valid_landscape()
        middle = copy.deepcopy(data["coverage"]["searches"][0])
        middle["id"] = "search-middle"
        middle["started_at"] = "2026-07-12T12:15:00+09:00"
        middle["hit_count"] = 1
        middle["new_candidate_ids"] = ["system-one"]
        data["coverage"]["searches"].append(middle)
        errors = self.errors(data)
        self.assert_has_code(errors, "incomplete-stop-evidence")
        self.assert_has_code(errors, "no-saturation")

    def test_search_requires_query_and_family_fields(self) -> None:
        data = valid_landscape()
        del data["coverage"]["searches"][0]["query"]
        self.assert_has_code(self.errors(data), "missing-field")

    def test_identity_name_has_only_one_decision(self) -> None:
        data = valid_landscape()
        data["candidates"][0]["aliases"] = ["System 1"]
        decision = {
            "observed_name": "System 1",
            "decision": "merged",
            "canonical_candidate_ids": ["system-one"],
            "reason": "Same system",
            "source_ids": ["source-paper"],
        }
        data["identity_decisions"] = [decision, copy.deepcopy(decision)]
        data["discovery_records"].append(
            {
                "id": "discovery-system-alias",
                "observed_name": "System 1",
                "resolution": "merged",
                "candidate_ids": ["system-one"],
                "reason": "Alias record",
                "source_ids": ["source-paper"],
            }
        )
        data["coverage"]["counts"]["discovered_records"] = 2
        data["coverage"]["counts"]["merged_records"] = 1
        self.assert_has_code(self.errors(data), "contradictory-identity-decision")

    def test_technique_requires_name_and_description(self) -> None:
        data = valid_landscape()
        del data["taxonomy"]["techniques"][0]["description"]
        self.assert_has_code(self.errors(data), "missing-field")

    def test_technique_claim_must_cover_assigned_candidate(self) -> None:
        data = valid_landscape()
        data["claims"][0]["candidate_ids"] = []
        errors = self.errors(data)
        self.assert_has_code(errors, "taxonomy-claim-mismatch")

    def test_discovery_counts_are_derived(self) -> None:
        data = valid_landscape()
        data["coverage"]["counts"]["canonical_candidates"] = 99
        self.assert_has_code(self.errors(data), "accounting-mismatch")

    def test_boolean_counts_are_rejected(self) -> None:
        data = valid_landscape()
        data["coverage"]["counts"] = {
            "discovered_records": True,
            "canonical_candidates": True,
            "merged_records": False,
            "included": True,
            "excluded": False,
            "unresolved_records": False,
        }
        self.assert_has_code(self.errors(data), "invalid-count")

    def test_secondary_gap_references_must_match_claim(self) -> None:
        data = valid_landscape()
        data["sources"][0]["source_class"] = "secondary"
        data["claims"][0]["source_strength"] = "secondary"
        data["field_catalog"].append({"id": "throughput", "label": "Throughput", "value_type": "number", "required": False})
        data["coverage"]["gaps"].append(
            {
                "id": "secondary-gap",
                "kind": "secondary-only-evidence",
                "description": "Only secondary evidence",
                "candidate_ids": ["system-one"],
                "claim_ids": ["claim-latency"],
                "source_ids": ["source-paper"],
                "search_ids": [],
                "field_ids": ["throughput"],
            }
        )
        self.assert_has_code(self.errors(data), "gap-reference-mismatch")

    def test_malformed_types_return_errors_without_crashing(self) -> None:
        mutations = {
            "unit": lambda data: data["scope"].__setitem__("unit_of_analysis", []),
            "field-type": lambda data: data["field_catalog"][0].__setitem__("value_type", []),
            "source-class": lambda data: data["sources"][0].__setitem__("source_class", []),
            "access-status": lambda data: data["sources"][0].__setitem__("access_status", []),
            "locator-type": lambda data: data["sources"][0].__setitem__("locator", {"type": []}),
            "claim-state": lambda data: data["claims"][0].__setitem__("epistemic_status", []),
            "claim-candidates": lambda data: data["claims"][0].__setitem__("candidate_ids", {}),
            "candidate-name": lambda data: data["candidates"][0].__setitem__("name", []),
            "candidate-aliases": lambda data: data["candidates"][0].__setitem__("aliases", {}),
            "candidate-status": lambda data: data["candidates"][0].__setitem__("status", []),
            "candidate-techniques": lambda data: data["candidates"][0].__setitem__("technique_ids", {}),
            "cell-status": lambda data: data["candidates"][0]["comparison"]["latency"].__setitem__("status", []),
            "search-status": lambda data: data["coverage"]["searches"][0].__setitem__("status", []),
            "discovery-resolution": lambda data: data["discovery_records"][0].__setitem__("resolution", []),
            "identity-decision": lambda data: data["identity_decisions"].append(
                {"observed_name": "X", "decision": [], "canonical_candidate_ids": ["system-one"], "reason": "test", "source_ids": ["source-paper"]}
            ),
            "relationship-kind": lambda data: data["candidate_relationships"].append(
                {"id": "bad-relation", "from_candidate_id": "system-one", "to_candidate_id": "system-one", "relationship": [], "reason": "test", "source_ids": ["source-paper"]}
            ),
            "gap-kind": lambda data: data["coverage"]["gaps"].append(
                {"id": "bad-gap", "kind": [], "description": "test", "candidate_ids": ["system-one"], "claim_ids": [], "source_ids": [], "search_ids": [], "field_ids": []}
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                data = valid_landscape()
                mutate(data)
                self.assertTrue(self.errors(data))

    def test_cli_returns_json_for_malformed_structured_type(self) -> None:
        data = valid_landscape()
        data["scope"]["unit_of_analysis"] = []
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "malformed.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path)], check=False, capture_output=True, text=True)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)["valid"])
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_nested_property_is_rejected(self) -> None:
        data = valid_landscape()
        data["claims"][0]["source_strenght"] = "primary"
        self.assert_has_code(self.errors(data), "unknown-field")


if __name__ == "__main__":
    unittest.main()
