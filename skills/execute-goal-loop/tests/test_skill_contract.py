from pathlib import Path
import re
import unittest

import yaml


SKILL = Path(__file__).resolve().parents[1]


class ExecuteGoalLoopContractTests(unittest.TestCase):
    def test_frontmatter_has_narrow_explicit_trigger(self):
        text = (SKILL / "SKILL.md").read_text()
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = yaml.safe_load(match.group(1))
        self.assertEqual(set(frontmatter), {"name", "description"})
        self.assertEqual(frontmatter["name"], SKILL.name)
        description = frontmatter["description"]
        for phrase in (
            "explicitly asks",
            "explicit loop contract",
            "Compose with align-work",
            "domain skills",
            "Do not auto-trigger",
            "standalone review",
            "one-off commit",
            "Delivery actions",
            "skill-creator owns skill mechanics",
        ):
            self.assertIn(phrase, description)

    def test_completion_audit_matches_current_requirements_to_receipts(self):
        text = (SKILL / "SKILL.md").read_text()
        audit = text[text.index("## Completion Audit") : text.index("## Completion Report")]
        for phrase in (
            "Re-derive the complete requirement set",
            "current-state evidence at matching scope",
            "superseded plan or revision",
            "changed materially",
            "substitutes a mock",
            "Recheck volatile facts",
            "Missing, uncertain, indirect, inaccessible, or unaccounted evidence",
            "every required item passes",
        ):
            self.assertIn(phrase, audit)

    def test_reference_and_metadata_contract(self):
        text = (SKILL / "SKILL.md").read_text()
        links = re.findall(r"\]\((references/[^)]+)\)", text)
        self.assertEqual(links, ["references/reviewer-prompts.md"])
        self.assertTrue((SKILL / links[0]).is_file())
        metadata = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text())
        self.assertEqual(metadata["interface"]["display_name"], "Execute Goal Loop")
        self.assertIn("$execute-goal-loop", metadata["interface"]["default_prompt"])
        self.assertGreaterEqual(len(metadata["interface"]["short_description"]), 25)
        self.assertLessEqual(len(metadata["interface"]["short_description"]), 64)

    def test_read_only_loop_retains_audit_mutation_boundary(self):
        text = (SKILL / "SKILL.md").read_text()
        for phrase in (
            "retain the `audit-technical-work` evidence-surface boundary",
            "stateful tests",
            "side-effectful external calls",
            "no persistent cache, bytecode, artifact, or external effect",
        ):
            self.assertIn(phrase, text)

    def test_required_resources_only(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "references/reviewer-prompts.md",
            "tests/test_skill_contract.py",
        }
        actual = {
            str(path.relative_to(SKILL))
            for path in SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(actual, expected)
        self.assertNotIn("TODO", (SKILL / "SKILL.md").read_text())
        self.assertLess(len((SKILL / "SKILL.md").read_text().splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
