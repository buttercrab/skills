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
    "prioritize-important-information": {
        "SKILL.md",
        "agents/openai.yaml",
        "references/importance-examples.md",
    },
    "write-daily-report": {
        "SKILL.md",
        "agents/openai.yaml",
    },
    "maintain-project-dashboard": {
        "SKILL.md",
        "agents/openai.yaml",
        "references/dashboard-structure.md",
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
            "prioritize-important-information": [
                "A fact is important when omitting it could cause a wrong decision or action.",
                "Importance and confidence are separate.",
                "Activity is not success.",
                "A proxy, simpler check, partial run, or agent-preferred metric does not replace the specified gate.",
                "keep the specified gate `not done` or partial until the complete named contract",
                "Links may hold supporting evidence, never unnamed material facts.",
                "Never demote a decision-changing fact merely to satisfy a length target.",
            ],
            "write-daily-report": [
                "Give exactly one action, its owner, its done condition",
                "Preparing a report is read-only project work.",
                "Run a named evaluation only when the user separately requested or authorized that exact evaluation contract",
                "State one current commitment, its done condition, and any still-active constraint",
                "Invocation of this skill alone never authorizes an external write or any evidence-generating project work.",
                "Put simpler evaluations under supporting evidence; never promote them to completion of the named gate.",
            ],
            "maintain-project-dashboard": [
                "Maintain a compact decision surface for operating a project.",
                "If not, remain read-only and provide a proposed structure or patch.",
                "Show progress only when it changes a gate, ETA, decision, or next action.",
                "Assign authority by fact type instead of applying one global source order:",
                "never substitute an easier eval silently.",
            ],
        }
        for name, phrases in expectations.items():
            text = (SKILLS / name / "SKILL.md").read_text()
            for phrase in phrases:
                with self.subTest(skill=name, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_reporting_contract_examples_are_pinned(self):
        importance = (SKILLS / "prioritize-important-information" / "SKILL.md").read_text()
        daily = (SKILLS / "write-daily-report" / "SKILL.md").read_text()
        importance_examples = (
            SKILLS
            / "prioritize-important-information"
            / "references"
            / "importance-examples.md"
        ).read_text()
        dashboard_reference = (
            SKILLS
            / "maintain-project-dashboard"
            / "references"
            / "dashboard-structure.md"
        ).read_text()

        self.assertNotIn("at most five", importance.lower())
        self.assertNotIn("at most five", daily.lower())
        self.assertNotIn("disclose the exact overflow", importance.lower())
        self.assertNotIn("disclose the exact overflow", daily.lower())
        self.assertIn("name every material fact on the visible decision surface", importance)
        self.assertIn("name every material delta inline", daily)
        self.assertIn("29 of 45 required sets", importance_examples)
        self.assertIn("16 remain", importance_examples)
        self.assertIn("The simpler evaluations are supporting evidence", importance_examples)
        self.assertIn(
            "ASR sheet: 29/45 sets, 16 pending (as of 2026-07-19)",
            dashboard_reference,
        )
        self.assertIn("Omni Model Base", dashboard_reference)

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
