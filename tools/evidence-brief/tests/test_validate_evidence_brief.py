from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_evidence_brief.py"
SPEC = importlib.util.spec_from_file_location("validate_evidence_brief", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def valid_brief() -> dict:
    return {
        "schema_version": "evidence-brief-v1",
        "question": "What does the supplied source establish?",
        "requested_resources": [
            {
                "id": "request-1",
                "input_locator": "https://example.test/document",
                "source_id": "source-1",
            }
        ],
        "sources": [
            {
                "id": "source-1",
                "provenance_class": "requested-resource",
                "kind": "web-page",
                "title": "Example document",
                "resource_locator": "https://example.test/document",
                "mutability": "mutable",
                "authority": "primary",
                "access_scope": "public",
                "acquisition": {
                    "status": "acquired",
                    "method": "public-web",
                    "receipt": {
                        "provider": "example",
                        "resource_id": "opaque-source-1",
                        "retrieved_at": "2026-07-12T00:00:00+00:00",
                        "details": {"content_type": "text/html"},
                    },
                },
                "version_context": {
                    "observed_at": "2026-07-12T00:00:00+00:00",
                    "updated_at": "2026-07-11T00:00:00+00:00",
                    "timezone": "UTC",
                    "version": "2026-07-11",
                },
            }
        ],
        "answer": {
            "status": "answered",
            "fact_ids": ["fact-1"],
            "unknown_ids": [],
        },
        "facts": [
            {
                "id": "fact-1",
                "assertion_key": "example.value",
                "value": 1,
                "claim": "The example value is one.",
                "citations": [
                    {
                        "source_id": "source-1",
                        "locator": {"kind": "section", "value": "Results"},
                    }
                ],
            }
        ],
        "inferences": [],
        "unknowns": [],
        "conflicts": [],
        "context_map": [],
        "actions": [],
        "decision": None,
    }


def errors(data: object) -> list[tuple[str, str, str]]:
    return VALIDATOR.Validator(data).validate()


def error_codes(data: object) -> set[str]:
    return {code for _, code, _ in errors(data)}


class ValidatorTests(unittest.TestCase):
    def run_cli_raw(self, raw: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "evidence-brief.json"
            path.write_text(raw, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_valid_baseline(self) -> None:
        self.assertEqual(errors(valid_brief()), [])

    def test_cli_accepts_valid_brief(self) -> None:
        completed = self.run_cli_raw(json.dumps(valid_brief()))
        self.assertEqual(completed.returncode, 0)
        self.assertIn("VALID evidence-brief-v1", completed.stdout)

    def test_malformed_reference_types_never_crash(self) -> None:
        for value in (None, True, 7, [], {}):
            with self.subTest(value=value):
                brief = valid_brief()
                brief["answer"]["fact_ids"] = [value]
                self.assertIn("E020", error_codes(brief))

    def test_malformed_ids_never_crash(self) -> None:
        for value in (None, True, 7, [], {}):
            with self.subTest(value=value):
                brief = valid_brief()
                brief["sources"][0]["id"] = value
                self.assertIn("E014", error_codes(brief))

    def test_answer_status_uses_root_ledger(self) -> None:
        brief = valid_brief()
        brief["unknowns"] = [
            {
                "id": "unknown-1",
                "question": "What is not established?",
                "reason": "Not acquired",
                "related_source_ids": ["source-1"],
                "related_fact_ids": [],
            }
        ]
        self.assertIn("E027", error_codes(brief))

        brief = valid_brief()
        brief["unknowns"] = [
            {
                "id": "unknown-1",
                "question": "What is not established?",
                "reason": "Not acquired",
                "related_source_ids": ["source-1"],
                "related_fact_ids": [],
            }
        ]
        brief["answer"] = {
            "status": "insufficient-evidence",
            "fact_ids": [],
            "unknown_ids": ["unknown-1"],
        }
        self.assertIn("E027", error_codes(brief))

    def test_secret_and_signed_locator_bypasses_are_rejected(self) -> None:
        mutations = [
            ("requested_resources", "https://example.test/#access_token=dummy-secret-value"),
            ("sources", "https://example.test/?client_secret=dummy-secret-value"),
            ("sources", "https://example.test/%253Faccess_token%253Ddummy-secret-value"),
            ("details", "xoxb-" + "123456789012-123456789012-abcdefghijklmnop"),
            ("details", "github_pat_1234567890abcdefghijklmnop"),
        ]
        for target, value in mutations:
            with self.subTest(target=target, value=value):
                brief = valid_brief()
                if target == "requested_resources":
                    brief[target][0]["input_locator"] = value
                elif target == "sources":
                    brief[target][0]["resource_locator"] = value
                else:
                    brief["sources"][0]["acquisition"]["receipt"]["details"]["auth"] = value
                self.assertIn("E034", error_codes(brief))

    def test_sensitive_key_and_private_receipt_content_are_rejected(self) -> None:
        brief = valid_brief()
        details = brief["sources"][0]["acquisition"]["receipt"]["details"]
        details["password"] = "short-secret"
        details["apiKey"] = "another-short-secret"
        details["body"] = "private source text"
        found = errors(brief)
        self.assertGreaterEqual(sum(code == "E034" for _, code, _ in found), 3)

    def test_explicit_redaction_is_allowed(self) -> None:
        brief = valid_brief()
        brief["sources"][0]["acquisition"]["receipt"]["details"]["token"] = "<redacted>"
        self.assertEqual(errors(brief), [])

    def test_locator_kinds_are_validated(self) -> None:
        valid = {
            "page": "12-14",
            "line-range": "L20-L24",
            "json-path": "$.items[0].name",
            "table-cell": "Sheet1!B12",
            "timestamp": "01:02:03.5",
            "custom": "provider:opaque-location",
        }
        invalid = {
            "page": "-1",
            "line-range": "tomorrow",
            "json-path": "$",
            "table-cell": "row twelve",
            "timestamp": "tomorrow",
            "custom": "opaque-location",
        }
        for kind, value in valid.items():
            with self.subTest(kind=kind, valid=True):
                brief = valid_brief()
                brief["facts"][0]["citations"][0]["locator"] = {"kind": kind, "value": value}
                self.assertEqual(errors(brief), [])
        for kind, value in invalid.items():
            with self.subTest(kind=kind, valid=False):
                brief = valid_brief()
                brief["facts"][0]["citations"][0]["locator"] = {"kind": kind, "value": value}
                self.assertIn("E023", error_codes(brief))

    def test_cross_collection_id_collision_is_rejected(self) -> None:
        brief = valid_brief()
        brief["inferences"] = [
            {
                "id": "fact-1",
                "statement": "An inference",
                "based_on_fact_ids": ["fact-1"],
                "reasoning": "The fact supports it.",
                "confidence": "low",
            }
        ]
        brief["decision"] = {
            "recommendation": "Proceed",
            "basis_ids": ["fact-1"],
            "next_action_ids": [],
        }
        self.assertIn("E015", error_codes(brief))

    def test_conflict_fixture_is_consistent_and_required(self) -> None:
        brief = valid_brief()
        second_source = copy.deepcopy(brief["sources"][0])
        second_source.update(
            id="source-2",
            title="Second source",
            resource_locator="https://example.test/second",
            authority="secondary",
        )
        second_source["acquisition"]["receipt"]["resource_id"] = "opaque-source-2"
        brief["sources"].append(second_source)
        brief["requested_resources"].append(
            {
                "id": "request-2",
                "input_locator": "https://example.test/second",
                "source_id": "source-2",
            }
        )
        second_fact = copy.deepcopy(brief["facts"][0])
        second_fact.update(id="fact-2", value=2, claim="The example value is two.")
        second_fact["citations"][0]["source_id"] = "source-2"
        brief["facts"].append(second_fact)
        brief["answer"]["fact_ids"].append("fact-2")
        brief["conflicts"] = [
            {
                "id": "conflict-1",
                "fact_ids": ["fact-1", "fact-2"],
                "status": "unresolved",
                "explanation": "The primary and secondary sources disagree.",
            }
        ]
        brief["context_map"] = [
            {
                "from_source_id": "source-1",
                "to_source_id": "source-2",
                "relationship": "contradicts",
            }
        ]
        self.assertEqual(errors(brief), [])
        brief["conflicts"] = []
        self.assertIn("E025", error_codes(brief))

    def test_inference_requires_valid_fact_grounding(self) -> None:
        brief = valid_brief()
        brief["inferences"] = [
            {
                "id": "inference-1",
                "statement": "An inference",
                "based_on_fact_ids": ["missing-fact"],
                "reasoning": "No valid basis.",
                "confidence": "low",
            }
        ]
        found = error_codes(brief)
        self.assertIn("E020", found)
        self.assertIn("E024", found)

    def test_acquired_source_requires_valid_receipt(self) -> None:
        brief = valid_brief()
        del brief["sources"][0]["acquisition"]["receipt"]["provider"]
        self.assertIn("E031", error_codes(brief))

    def test_source_provenance_fields_are_required_for_every_status(self) -> None:
        for field in ("mutability", "authority", "access_scope", "version_context"):
            with self.subTest(field=field):
                brief = valid_brief()
                del brief["sources"][0][field]
                self.assertTrue(error_codes(brief) & {"E012", "E013"})

        brief = valid_brief()
        brief["facts"] = []
        brief["sources"][0]["acquisition"] = {
            "status": "blocked",
            "reason": {"code": "no-access", "detail": "Connector unavailable"},
        }
        brief["sources"][0]["version_context"] = {}
        brief["unknowns"] = [
            {
                "id": "unknown-1",
                "question": "What does the source contain?",
                "reason": "Blocked",
                "related_source_ids": ["source-1"],
                "related_fact_ids": [],
            }
        ]
        brief["answer"] = {
            "status": "insufficient-evidence",
            "fact_ids": [],
            "unknown_ids": ["unknown-1"],
        }
        self.assertEqual(errors(brief), [])
        del brief["sources"][0]["version_context"]
        self.assertIn("E012", error_codes(brief))

    def test_github_source_requires_version_or_update_context(self) -> None:
        brief = valid_brief()
        source = brief["sources"][0]
        source["kind"] = "github-resource"
        source["version_context"] = {
            "observed_at": "2026-07-12T00:00:00+00:00",
        }
        self.assertIn("E016", error_codes(brief))
        source["version_context"]["commit_context"] = "deadbeef"
        self.assertEqual(errors(brief), [])

    def test_completed_action_requires_anchor_receipt_and_ordering(self) -> None:
        brief = valid_brief()
        action = {
            "id": "action-1",
            "operation": "delete",
            "resource_id": "opaque-target",
            "status": "completed",
            "authorization": {
                "source": {"kind": "user-message", "resource_id": "opaque-message"},
                "scope": "delete this target",
                "operation": "delete",
                "resource_id": "opaque-target",
                "authorized_at": "2026-07-12T00:00:00+00:00",
            },
            "receipt": {
                "provider": "example",
                "receipt_id": "opaque-receipt",
                "operation": "delete",
                "resource_id": "opaque-target",
                "completed_at": "2026-07-12T00:01:00+00:00",
            },
        }
        brief["actions"] = [action]
        self.assertEqual(errors(brief), [])

        action["authorization"]["source"] = "assistant-generated"
        self.assertIn("E029", error_codes(brief))
        action["authorization"]["source"] = {
            "kind": "user-message",
            "resource_id": "opaque-message",
        }
        del action["receipt"]["receipt_id"]
        self.assertIn("E028", error_codes(brief))
        action["receipt"]["receipt_id"] = "opaque-receipt"
        action["receipt"]["completed_at"] = "2026-07-11T23:59:00+00:00"
        self.assertIn("E028", error_codes(brief))

    def test_strict_json_rejects_duplicate_keys_and_nonfinite_numbers(self) -> None:
        raw = json.dumps(valid_brief(), separators=(",", ":"))
        cases = [
            raw.replace('"status":"answered"', '"status":"partial","status":"answered"', 1),
            raw.replace('"value":1', '"value":NaN', 1),
            raw.replace('"value":1', '"value":Infinity', 1),
            raw.replace('"value":1', '"value":-Infinity', 1),
            raw.replace('"value":1', '"value":1e9999', 1),
        ]
        for raw_case in cases:
            with self.subTest(raw=raw_case[-120:]):
                completed = self.run_cli_raw(raw_case)
                self.assertEqual(completed.returncode, 1)
                self.assertIn("E001 /: invalid JSON", completed.stderr)
                self.assertNotIn("VALID", completed.stdout)

    def test_help(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--help"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn("usage:", completed.stdout)


if __name__ == "__main__":
    unittest.main()
