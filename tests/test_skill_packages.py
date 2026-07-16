from pathlib import Path
import json
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "audit-technical-work": {
        "SKILL.md",
        "agents/openai.yaml",
        "references/audit-lenses.md",
    },
    "refactor-by-invariant": {
        "SKILL.md",
        "agents/openai.yaml",
    },
    "propagate-contract-changes": {
        "SKILL.md",
        "agents/openai.yaml",
    },
    "write-task-handoff": {
        "SKILL.md",
        "agents/openai.yaml",
    },
    "align-work": {
        "SKILL.md",
        "agents/openai.yaml",
        "assets/packet-templates/alignment.md",
        "assets/packet-templates/decisions.md",
        "assets/packet-templates/execution.md",
        "assets/packet-templates/facts.md",
        "assets/packet-templates/plan.md",
        "assets/packet-templates/state.json",
        "references/execute-aligned-work.md",
        "references/explore-and-align.md",
        "references/packet-contract.md",
        "references/review-plan.md",
        "references/write-alignment.md",
        "references/write-plan.md",
        "references/work-authority-v1.schema.json",
        "references/work-authority-v2.schema.json",
        "references/packet-transfer-receipt-v1.schema.json",
        "scripts/preservation_journal.py",
        "scripts/planning_packet.py",
        "scripts/work_authority.py",
        "tests/test_planning_packet.py",
        "tests/test_skill_contract.py",
        "tests/test_work_authority.py",
    },
    "execute-goal-loop": {
        "SKILL.md",
        "agents/openai.yaml",
        "references/reviewer-prompts.md",
        "tests/test_skill_contract.py",
    },
    "mine-history-tool-landscapes": {
        "SKILL.md",
        "agents/openai.yaml",
        "references/history-source-contract.md",
        "scripts/index_agent_history.py",
        "scripts/strict_json.py",
        "scripts/validate_history_evidence.py",
        "tests/test_history_pipeline.py",
    },
}


class SkillPackageTests(unittest.TestCase):
    def test_all_affected_packages_have_exact_resources(self):
        for name, expected in EXPECTED.items():
            with self.subTest(skill=name):
                skill = SKILLS / name
                actual = {
                    str(path.relative_to(skill))
                    for path in skill.rglob("*")
                    if path.is_file() and "__pycache__" not in path.parts
                }
                self.assertEqual(actual, expected)
                self.assertFalse(any(path.is_symlink() for path in skill.rglob("*")))

    def test_frontmatter_and_metadata_contract(self):
        for name in EXPECTED:
            with self.subTest(skill=name):
                skill = SKILLS / name
                text = (skill / "SKILL.md").read_text()
                match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
                self.assertIsNotNone(match)
                frontmatter = yaml.safe_load(match.group(1))
                self.assertEqual(set(frontmatter), {"name", "description"})
                self.assertEqual(frontmatter["name"], name)
                self.assertTrue(frontmatter["description"].strip())
                self.assertNotIn("TODO", text)
                self.assertLess(len(text.splitlines()), 500)

                metadata_text = (skill / "agents" / "openai.yaml").read_text()
                metadata = yaml.safe_load(metadata_text)
                self.assertTrue(set(metadata) <= {"interface", "policy"})
                interface = metadata["interface"]
                self.assertEqual(
                    set(interface),
                    {"display_name", "short_description", "default_prompt"},
                )
                self.assertGreaterEqual(len(interface["short_description"]), 25)
                self.assertLessEqual(len(interface["short_description"]), 64)
                self.assertIn(f"${name}", interface["default_prompt"])
                for line in metadata_text.splitlines():
                    key = line.strip().split(":", 1)[0]
                    if key in {"display_name", "short_description", "default_prompt"}:
                        self.assertRegex(line, r': ".*"$')

    def test_every_reference_is_linked_directly_and_resolves(self):
        for name, expected in EXPECTED.items():
            with self.subTest(skill=name):
                skill = SKILLS / name
                text = (skill / "SKILL.md").read_text()
                links = set(re.findall(r"\]\((references/[^)]+)\)", text))
                references = {item for item in expected if item.startswith("references/")}
                self.assertEqual(links, references)
                for link in links:
                    self.assertTrue((skill / link).is_file())

    def test_json_resources_are_strict_json(self):
        for name, expected in EXPECTED.items():
            for relative in expected:
                if relative.endswith(".json"):
                    with self.subTest(skill=name, resource=relative):
                        json.loads((SKILLS / name / relative).read_text())

    def test_new_skill_semantic_boundaries_are_pinned(self):
        expectations = {
            "audit-technical-work": [
                "Pure in-memory evaluation is permitted",
                "Use severity for impact, not confidence",
                "Do not edit, stage, commit, publish",
            ],
            "refactor-by-invariant": [
                "independent test oracles",
                "test helpers must not reimplement the production acceptance decision",
                "behavioral coverage",
            ],
            "propagate-contract-changes": [
                "atomic change set",
                "approved compatibility window",
                "do not land a knowingly broken intermediate contract",
            ],
            "write-task-handoff": [
                "without changing protected content",
                "planning_packet.py handoff",
                "label the transfer incomplete",
                "front-agent send",
                "`owned`, `unrelated`, or `unknown`",
                "prior approval as nonportable",
                "reproducible snapshot marker",
            ],
        }
        for name, phrases in expectations.items():
            text = (SKILLS / name / "SKILL.md").read_text()
            for phrase in phrases:
                with self.subTest(skill=name, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_trial_and_evaluator_catalogs_are_separate(self):
        self.assertFalse((ROOT / "tests" / "forward_test_cases.json").exists())
        prompts = json.loads((ROOT / "tests" / "portfolio-routing-prompts-v1.json").read_text())
        expected = json.loads((ROOT / "tests" / "portfolio-routing-cases-v1.json").read_text())
        rubrics = json.loads((ROOT / "tests" / "portfolio-routing-rubrics-v1.json").read_text())
        self.assertEqual("trial-input", prompts["visibility"])
        self.assertEqual("evaluator-only", expected["visibility"])
        self.assertEqual("evaluator-only", rubrics["visibility"])
        self.assertEqual(
            [case["id"] for case in prompts["cases"]],
            [case["id"] for case in expected["cases"]],
        )

    def test_progressive_disclosure_has_one_canonical_owner(self):
        front = SKILLS / "front-agent-orchestration"
        front_text = (front / "SKILL.md").read_text()
        operations = (front / "references" / "operations.md").read_text()
        self.assertFalse((front / "README.md").exists())
        self.assertIn(
            "[references/operations.md](references/operations.md)",
            front_text,
        )
        self.assertIn("Go 1.22 or newer", operations)
        self.assertIn("never contacts Agent Mail", operations)

        agent_mail = SKILLS / "agent-mail"
        entry = (agent_mail / "SKILL.md").read_text()
        service = (agent_mail / "references" / "service-operations.md").read_text()
        self.assertLess(len(entry.splitlines()), 90)
        self.assertIn(
            "[references/service-operations.md](references/service-operations.md)",
            entry,
        )
        self.assertIn("public MCP smoke mutates production", entry)
        self.assertIn("AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN", service)
        self.assertIn("idempotency key", service)

        ignores = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn(
            "skills/front-agent-orchestration/scripts/front-agent-bin",
            ignores,
        )


if __name__ == "__main__":
    unittest.main()
