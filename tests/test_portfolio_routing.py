from __future__ import annotations

import importlib.util
import copy
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tests" / "validate_portfolio_routing.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_portfolio_routing", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortfolioRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_canonical_contract_and_all_projections_match(self):
        self.assertEqual(self.validator.validate(ROOT), [])

    def test_projection_generator_reports_clean_state(self):
        result = subprocess.run(
            ["python3", str(ROOT / "scripts" / "sync_portfolio_routing.py"), "--check"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_reporting_composition_edges_are_direct(self):
        contract = json.loads((ROOT / "tests" / "portfolio-routing-v1.json").read_text())
        rows = {row["skill"]: row for row in contract["rows"]}
        required = {
            ("audit-technical-work", "prioritize-important-information", "content-owner"),
            ("write-daily-report", "prioritize-important-information", "content-owner"),
            ("maintain-project-dashboard", "prioritize-important-information", "content-owner"),
        }
        for source, target, relation in required:
            with self.subTest(source=source, target=target):
                self.assertIn(
                    {"route": target, "relation": relation},
                    rows[source]["legal_compositions"],
                )

    def test_missing_required_reporting_edge_fails_closed(self):
        contract = json.loads((ROOT / "tests" / "portfolio-routing-v1.json").read_text())
        daily = next(row for row in contract["rows"] if row["skill"] == "write-daily-report")
        daily["legal_compositions"] = []
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "tests" / "portfolio-routing-v1.json"
            target.parent.mkdir(parents=True)
            target.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(
                any("missing required direct composition edge" in error for error in errors),
                errors,
            )

    def test_projection_writer_preserves_existing_source_modes(self):
        contract = json.loads((ROOT / "tests" / "portfolio-routing-v1.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            target_root = Path(directory)
            for relative in (
                "tests/portfolio-routing-v1.json",
                "tests/portfolio-routing-cases-v1.json",
                "tests/portfolio-routing-prompts-v1.json",
                "tests/portfolio-routing-rubrics-v1.json",
            ):
                target = target_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            for row in contract["rows"]:
                for suffix in ("SKILL.md", "agents/openai.yaml"):
                    relative = Path("skills") / row["skill"] / suffix
                    target = target_root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / relative, target)

            prompt = target_root / "tests/portfolio-routing-prompts-v1.json"
            prompt.write_text(prompt.read_text() + "\n", encoding="utf-8")
            prompt.chmod(0o644)
            result = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts" / "sync_portfolio_routing.py"),
                    "--root",
                    str(target_root),
                    "--write",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(0o644, stat.S_IMODE(prompt.stat().st_mode))

    def test_generator_updates_body_and_metadata_from_same_canonical_row(self):
        contract = json.loads((ROOT / "tests" / "portfolio-routing-v1.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            target_root = Path(directory)
            for relative in (
                "tests/portfolio-routing-v1.json",
                "tests/portfolio-routing-cases-v1.json",
                "tests/portfolio-routing-prompts-v1.json",
                "tests/portfolio-routing-rubrics-v1.json",
            ):
                target = target_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            for row in contract["rows"]:
                for suffix in ("SKILL.md", "agents/openai.yaml"):
                    relative = Path("skills") / row["skill"] / suffix
                    target = target_root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / relative, target)

            audit = next(row for row in contract["rows"] if row["skill"] == "audit-technical-work")
            audit["state_owner"] += " Mutation sentinel."
            (target_root / "tests/portfolio-routing-v1.json").write_text(
                json.dumps(contract, indent=2) + "\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts" / "sync_portfolio_routing.py"),
                    "--root",
                    str(target_root),
                    "--write",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            skill_text = (
                target_root / "skills/audit-technical-work/SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn(self.validator.render_routing_block(audit), skill_text)
            digest = hashlib.sha256(
                json.dumps(
                    audit,
                    ensure_ascii=False,
                    allow_nan=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            agent_text = (
                target_root / "skills/audit-technical-work/agents/openai.yaml"
            ).read_text(encoding="utf-8")
            self.assertIn(f"# portfolio-routing-v1-row-sha256: {digest}", agent_text)

    def test_frontmatter_drift_fails_closed(self):
        source = ROOT / "skills" / "align-work" / "SKILL.md"
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "skills" / "align-work" / "SKILL.md"
            target.parent.mkdir(parents=True)
            text = source.read_text(encoding="utf-8")
            target.write_text(text.replace("description:", "description: drift ", 1), encoding="utf-8")
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(any("frontmatter description diverges" in error for error in errors), errors)

    def test_generated_routing_block_rejects_missing_duplicate_and_hand_edits(self):
        source = ROOT / "skills" / "audit-technical-work" / "SKILL.md"
        contract = json.loads((ROOT / "tests" / "portfolio-routing-v1.json").read_text())
        row = next(item for item in contract["rows"] if item["skill"] == "audit-technical-work")
        block = self.validator.render_routing_block(row)
        mutations = {
            "missing": "",
            "duplicate": block + "\n\n" + block,
            "hand-edited": block.replace(
                '`routing_role`: "outer"',
                '`routing_role`: "hand-edited"',
                1,
            ),
        }
        for label, replacement in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                overlay = Path(directory)
                target = overlay / "skills" / "audit-technical-work" / "SKILL.md"
                target.parent.mkdir(parents=True)
                target.write_text(
                    source.read_text(encoding="utf-8").replace(block, replacement, 1),
                    encoding="utf-8",
                )
                errors = self.validator.validate(ROOT, overlay)
                self.assertTrue(
                    any("generated routing block" in error for error in errors),
                    errors,
                )

    def test_generated_routing_block_rejects_every_routing_fact_class_mutation(self):
        source = ROOT / "skills" / "audit-technical-work" / "SKILL.md"
        contract = json.loads((ROOT / "tests" / "portfolio-routing-v1.json").read_text())
        row = next(item for item in contract["rows"] if item["skill"] == "audit-technical-work")
        block = self.validator.render_routing_block(row)
        fields = (
            "routing_role",
            "portfolio_position",
            "positive_request_classes",
            "triggers",
            "exclusions",
            "state_owner",
            "precedence",
            "legal_compositions",
            "fallbacks",
            "forbidden_actions",
        )
        for field in fields:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                mutated = copy.deepcopy(row)
                value = mutated[field]
                if isinstance(value, str):
                    mutated[field] = value + " Mutation sentinel."
                elif field == "legal_compositions":
                    value[0]["relation"] = "overlay"
                elif field == "fallbacks":
                    value[0]["condition"] += " Mutation sentinel."
                else:
                    value[0] += " Mutation sentinel."
                overlay = Path(directory)
                target = overlay / "skills" / "audit-technical-work" / "SKILL.md"
                target.parent.mkdir(parents=True)
                target.write_text(
                    source.read_text(encoding="utf-8").replace(
                        block,
                        self.validator.render_routing_block(mutated),
                        1,
                    ),
                    encoding="utf-8",
                )
                errors = self.validator.validate(ROOT, overlay)
                self.assertTrue(
                    any("stale or hand-edited" in error for error in errors),
                    errors,
                )

    def test_evaluator_case_route_must_be_cataloged(self):
        source = ROOT / "tests" / "portfolio-routing-cases-v1.json"
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "tests" / source.name
            target.parent.mkdir(parents=True)
            text = source.read_text(encoding="utf-8")
            target.write_text(text.replace('"outer_owner": "align-work"', '"outer_owner": "not-a-skill"', 1), encoding="utf-8")
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(any("unknown routes" in error for error in errors), errors)

    def test_raw_prompt_catalog_contains_no_evaluator_fields(self):
        catalog = json.loads(
            (ROOT / "tests" / "portfolio-routing-prompts-v1.json").read_text()
        )
        self.assertEqual("trial-input", catalog["visibility"])
        for case in catalog["cases"]:
            self.assertEqual({"id", "kind", "family", "prompt"}, set(case))
            self.assertFalse(
                {"expected", "rubric", "rubric_keys", "dispositions", "evaluator_id"}
                & set(case)
            )

    def test_raw_prompt_must_match_evaluator_projection(self):
        source = ROOT / "tests" / "portfolio-routing-prompts-v1.json"
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "tests" / source.name
            target.parent.mkdir(parents=True)
            text = source.read_text(encoding="utf-8")
            target.write_text(text.replace("Use $align-work", "Silently bypass Align", 1), encoding="utf-8")
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(any("differs from the evaluator case raw projection" in error for error in errors), errors)

    def test_known_but_illegal_composition_route_fails(self):
        source = ROOT / "tests" / "portfolio-routing-cases-v1.json"
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "tests" / source.name
            target.parent.mkdir(parents=True)
            text = source.read_text(encoding="utf-8")
            target.write_text(
                text.replace('"overlays": []', '"overlays": ["brief-linked-evidence"]', 1),
                encoding="utf-8",
            )
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(any("not allowed in overlays" in error for error in errors), errors)

    def test_route_cannot_be_duplicated_across_allowed_roles(self):
        source = ROOT / "tests" / "portfolio-routing-cases-v1.json"
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "tests" / source.name
            target.parent.mkdir(parents=True)
            text = source.read_text(encoding="utf-8")
            target.write_text(
                text.replace(
                    '"outer_owner": "audit-technical-work",\n        "gateways": [],\n        "overlays": [],\n        "evidence_lenses": []',
                    '"outer_owner": "audit-technical-work",\n        "gateways": [],\n        "overlays": [],\n        "evidence_lenses": ["audit-technical-work"]',
                    1,
                ),
                encoding="utf-8",
            )
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(any("duplicates routes across roles" in error for error in errors), errors)

    def test_directional_composition_must_reach_every_supporting_route(self):
        source = ROOT / "tests" / "portfolio-routing-cases-v1.json"
        with tempfile.TemporaryDirectory() as directory:
            overlay = Path(directory)
            target = overlay / "tests" / source.name
            target.parent.mkdir(parents=True)
            text = source.read_text(encoding="utf-8")
            target.write_text(
                text.replace(
                    '"outer_owner": "align-work",\n        "gateways": [],\n        "overlays": [],\n        "evidence_lenses": [],\n        "mechanics": [],\n        "transports": [],\n        "content_owners": [\n          "write-task-handoff"',
                    '"outer_owner": "audit-technical-work",\n        "gateways": [],\n        "overlays": [],\n        "evidence_lenses": [],\n        "mechanics": [],\n        "transports": [],\n        "content_owners": [\n          "write-task-handoff"',
                    1,
                ),
                encoding="utf-8",
            )
            errors = self.validator.validate(ROOT, overlay)
            self.assertTrue(any("directional legal compositions" in error for error in errors), errors)

    def test_rubric_policy_rejects_unknown_keys_and_cases(self):
        source = ROOT / "tests" / "portfolio-routing-rubrics-v1.json"
        for old, new, expected in (
            ('"authority-boundary"', '"unknown-rubric"', "unknown keys"),
            ('"case_id": "align-audit-goal"', '"case_id": "unknown-case"', "unknown case"),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                overlay = Path(directory)
                target = overlay / "tests" / source.name
                target.parent.mkdir(parents=True)
                target.write_text(source.read_text().replace(old, new, 1))
                errors = self.validator.validate(ROOT, overlay)
                self.assertTrue(any(expected in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
