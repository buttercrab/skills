from pathlib import Path
import re
import unittest

import yaml


SKILL = Path(__file__).resolve().parents[1]


class SkillContractCase(unittest.TestCase):
    def test_frontmatter_and_folder(self):
        text = (SKILL / "SKILL.md").read_text()
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = yaml.safe_load(match.group(1))
        self.assertEqual(set(frontmatter), {"name", "description"})
        self.assertEqual(frontmatter["name"], SKILL.name)
        self.assertIsInstance(frontmatter["description"], str)
        description = frontmatter["description"]
        for phrase in (
            "$align-work",
            "existing align-work packet",
            "unresolved decisions",
            "destructive",
            "externally mutating",
            "ordinary clear bounded coding",
            "simple answers",
            "low-risk mechanical edits",
            "audit-technical-work",
            "front-agent-orchestration",
        ):
            self.assertIn(phrase, description)
        self.assertNotIn("completion requires at least three", description)

    def test_openai_yaml(self):
        text = (SKILL / "agents" / "openai.yaml").read_text()
        data = yaml.safe_load(text)
        self.assertEqual(data["interface"]["display_name"], "Align Work")
        short = data["interface"]["short_description"]
        self.assertGreaterEqual(len(short), 25)
        self.assertLessEqual(len(short), 64)
        self.assertIn("$align-work", data["interface"]["default_prompt"])
        self.assertIs(data["policy"]["allow_implicit_invocation"], True)
        for line in text.splitlines():
            if ":" in line and line.strip().split(":", 1)[0] in {"display_name", "short_description", "default_prompt"}:
                self.assertRegex(line, r': ".*"$')

    def test_direct_references_resolve(self):
        text = (SKILL / "SKILL.md").read_text()
        links = re.findall(r"\]\((references/[^)]+)\)", text)
        self.assertEqual(
            set(links),
            {
                "references/packet-contract.md",
                "references/explore-and-align.md",
                "references/write-plan.md",
                "references/review-plan.md",
                "references/execute-approved-plan.md",
                "references/work-authority-v1.schema.json",
                "references/packet-transfer-receipt-v1.schema.json",
            },
        )
        for link in links:
            self.assertTrue((SKILL / link).is_file(), link)

    def test_no_authoring_leakage(self):
        for path in [SKILL / "SKILL.md", *(SKILL / "references").glob("*.md")]:
            text = path.read_text()
            self.assertNotIn("TODO", text, path)
            self.assertNotRegex(text, r"\[TODO")
        self.assertLess(len((SKILL / "SKILL.md").read_text().splitlines()), 500)

    def test_direct_children_receive_mandatory_no_delegation_preamble(self):
        preamble = "You are a direct child. Do not spawn or delegate to any other agent."
        self.assertIn(preamble, (SKILL / "SKILL.md").read_text())
        self.assertIn(preamble, (SKILL / "references" / "review-plan.md").read_text())
        self.assertIn(
            preamble,
            (SKILL / "references" / "execute-approved-plan.md").read_text(),
        )

    def test_risky_one_step_work_is_an_independent_trigger(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("even if the requested action is clear and one-step", text)

    def test_step_count_and_read_only_work_do_not_overtrigger_alignment(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("step count alone does not", text)
        self.assertIn("A read-only request alone is insufficient", text)
        self.assertIn("Uncertainty about complexity alone does not trigger", text)
        self.assertNotIn("If uncertain, treat the task as nontrivial", text)

    def test_explicit_align_under_front_preserves_packet_contract(self):
        text = (SKILL / "SKILL.md").read_text()
        for phrase in (
            "gateway must run this packet workflow",
            "exact packet path, task ID, revision, digest, authority classes",
            "Main validates that identity read-only",
            "never writes the packet",
        ):
            self.assertIn(phrase, text)

    def test_plan_preflight_and_execution_baseline_are_explicit(self):
        plan = (SKILL / "references" / "write-plan.md").read_text()
        for phrase in (
            "referenced path, symbol, command",
            "dependency order",
            "Map every requirement",
            "realistic from the stated working directory",
            "requested authority",
            "Simulate one representative path",
        ):
            self.assertIn(phrase, plan)
        execute = (SKILL / "references" / "execute-approved-plan.md").read_text()
        for phrase in (
            "repository guidance",
            "dirty-worktree baseline",
            "explicitly owned paths",
            "unrelated user changes",
            "partial mutations",
            "Never blind-revert",
        ):
            self.assertIn(phrase, execute)

    def test_plan_never_embeds_its_own_sealed_identity(self):
        text = (SKILL / "references" / "write-plan.md").read_text()
        self.assertIn("never insert them into protected `plan.md`", text)
        self.assertNotIn("Populate revision", text)

    def test_authority_classes_are_closed_and_documented(self):
        text = (SKILL / "references" / "packet-contract.md").read_text()
        for family in ("P", "R", "T", "I", "G", "E", "D"):
            self.assertRegex(text, rf"- `{family}`:")
        self.assertIn("helper rejects unknown class syntax", text)

    def test_material_change_clears_approval_before_replanning(self):
        text = (SKILL / "references" / "execute-approved-plan.md").read_text()
        transition = text.index("transition the packet to `needs_reapproval`")
        revise = text.index("Revise `plan.md`")
        self.assertLess(transition, revise)
        self.assertIn("Do not leave a digest-mismatched packet waiting on a reviewer", text)

    def test_required_resources_only(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/planning_packet.py",
            "scripts/preservation_journal.py",
            "scripts/work_authority.py",
            "references/packet-contract.md",
            "references/explore-and-align.md",
            "references/write-plan.md",
            "references/review-plan.md",
            "references/execute-approved-plan.md",
            "references/work-authority-v1.schema.json",
            "references/packet-transfer-receipt-v1.schema.json",
            "assets/packet-templates/facts.md",
            "assets/packet-templates/decisions.md",
            "assets/packet-templates/plan.md",
            "assets/packet-templates/state.json",
            "assets/packet-templates/execution.md",
            "tests/test_planning_packet.py",
            "tests/test_skill_contract.py",
            "tests/test_work_authority.py",
        }
        actual = {str(path.relative_to(SKILL)) for path in SKILL.rglob("*") if path.is_file() and "__pycache__" not in path.parts}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
