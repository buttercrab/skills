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
        description = frontmatter["description"]
        for phrase in (
            "$align-work",
            "lightweight alignment",
            "proactively ask decision-changing questions",
            "observable acceptance invariants",
            "implementation and verification mechanisms without reapproval",
            "durable packet mode",
            "existing Align packet",
            "destructive",
            "externally mutating",
            "continuity across sessions or agents",
            "audit-technical-work",
        ):
            self.assertIn(phrase, description)

    def test_openai_yaml(self):
        text = (SKILL / "agents" / "openai.yaml").read_text()
        data = yaml.safe_load(text)
        self.assertEqual(data["interface"]["display_name"], "Align Work")
        short = data["interface"]["short_description"]
        self.assertGreaterEqual(len(short), 25)
        self.assertLessEqual(len(short), 64)
        prompt = data["interface"]["default_prompt"]
        self.assertIn("$align-work", prompt)
        self.assertIn("proactively", prompt)
        self.assertIn("seek one approval", prompt)
        self.assertIn("proof mechanisms", prompt)
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
                "references/write-alignment.md",
                "references/write-plan.md",
                "references/review-plan.md",
                "references/execute-aligned-work.md",
                "references/work-authority-v1.schema.json",
                "references/work-authority-v2.schema.json",
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

    def test_proactive_questioning_without_plan_interrogation(self):
        skill = (SKILL / "SKILL.md").read_text()
        explore = (SKILL / "references" / "explore-and-align.md").read_text()
        for phrase in (
            "roughly three to seven high-value questions",
            "recommended default",
            "goal, must-have requirements, non-goals, acceptance evidence, constraints and authority, and tradeoff priorities",
            "Do not ask for discoverable facts or implementation-plan choices.",
            "Ask a focused follow-up only when an answer creates a new material ambiguity.",
        ):
            self.assertIn(phrase, skill)
        self.assertIn("Do not impose a hard round count", explore)
        self.assertIn("Do not ask the user to select architecture", explore)

    def test_direct_children_receive_mandatory_no_delegation_preamble(self):
        preamble = "You are a direct child. Do not spawn or delegate to any other agent."
        self.assertIn(preamble, (SKILL / "SKILL.md").read_text())
        self.assertIn(preamble, (SKILL / "references" / "review-plan.md").read_text())
        self.assertIn(preamble, (SKILL / "references" / "execute-aligned-work.md").read_text())

    def test_risky_one_step_work_is_an_independent_trigger(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("destructive, irreversible, production-facing", text)
        self.assertIn("Choose durable mode when any condition holds", text)

    def test_step_count_and_read_only_work_do_not_overtrigger_alignment(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("step count alone do not trigger Align or durable mode", text)
        self.assertIn("A read-only request alone is insufficient", text)
        self.assertNotIn("If uncertain, treat the task as nontrivial", text)
        self.assertIn("ordinary bounded delegation does not", text)
        self.assertIn("Front selection alone does not activate Align", text)
        packet = (SKILL / "references" / "packet-contract.md").read_text()
        self.assertIn("Front work with no independent Align trigger uses native authority", packet)
        self.assertNotIn("Front Agent always uses durable mode", text + packet)

    def test_alignment_not_plan_is_user_approved(self):
        skill = (SKILL / "SKILL.md").read_text()
        alignment = (SKILL / "references" / "write-alignment.md").read_text()
        plan = (SKILL / "references" / "write-plan.md").read_text()
        self.assertIn("The user approves the goal and completion boundary, not the implementation plan.", skill)
        self.assertIn("acceptance checklist defines what counts as done", alignment)
        self.assertIn("never the implementation plan", alignment)
        self.assertIn("The plan belongs to the agent and is never a user-approval artifact.", plan)
        self.assertIn("Updating them never requires user approval", plan)

    def test_durable_v3_and_legacy_contract_are_explicit(self):
        skill = (SKILL / "SKILL.md").read_text()
        packet = (SKILL / "references" / "packet-contract.md").read_text()
        self.assertIn("New durable packets use schema version 3.", skill)
        self.assertIn("`alignment.md` is the sole approval-bound artifact", skill)
        self.assertIn("Schema version 3 is the default", packet)
        self.assertIn("Schema versions 1 and 2 remain valid", packet)
        self.assertIn("Legacy versions retain `needs_reapproval`", packet)
        self.assertIn("work-authority v2", packet)
        self.assertIn("packet schema versions 2 and 3", packet)

    def test_plan_preflight_and_execution_baseline_are_explicit(self):
        plan = (SKILL / "references" / "write-plan.md").read_text()
        for phrase in (
            "referenced path, symbol, command",
            "dependency order",
            "Map every acceptance check",
            "realistic from the stated working directory",
            "Simulate one representative path",
        ):
            self.assertIn(phrase, plan)
        execute = (SKILL / "references" / "execute-aligned-work.md").read_text()
        for phrase in (
            "repository guidance",
            "dirty-worktree baseline",
            "explicitly owned paths",
            "unrelated user changes",
            "partial mutations",
            "Never blind-revert",
        ):
            self.assertIn(phrase, execute)

    def test_human_facing_approval_contract(self):
        skill = (SKILL / "SKILL.md").read_text()
        packet = (SKILL / "references" / "packet-contract.md").read_text()
        execute = (SKILL / "references" / "execute-aligned-work.md").read_text()
        front = (SKILL.parent / "front-agent-orchestration" / "SKILL.md").read_text()
        front_protocol = (SKILL.parent / "front-agent-orchestration" / "references" / "protocol.md").read_text()
        goal_loop = (SKILL.parent / "execute-goal-loop" / "SKILL.md").read_text()
        self.assertIn("Preserve alignment and execution boundaries", skill)
        self.assertIn("Keep machine receipts internal", skill)
        self.assertIn("Keep packet identity, revision, digest", packet)
        self.assertIn("Keep machine receipts internal", execute)
        self.assertIn("Use one human approval", front)
        self.assertIn("alignment-contract approval", front)
        self.assertIn("alignment-contract approval", front_protocol)
        self.assertIn("approval of the goal and completion boundary", goal_loop)
        self.assertNotIn("plain-language plan approval", front + front_protocol)
        self.assertNotIn("durable plan approval", goal_loop)

    def test_v3_templates_separate_alignment_and_plan(self):
        alignment = (SKILL / "assets" / "packet-templates" / "alignment.md").read_text()
        plan = (SKILL / "assets" / "packet-templates" / "plan.md").read_text()
        state = (SKILL / "assets" / "packet-templates" / "state.json").read_text()
        for heading in (
            "## Goal",
            "## Requirements",
            "## Non-goals",
            "## Constraints and authority",
            "## Acceptance checklist",
        ):
            self.assertIn(heading, alignment)
        for heading in ("## Current state", "## Approach", "## Steps", "## Verification strategy"):
            self.assertIn(heading, plan)
        self.assertNotIn("## Approval scope", plan)
        self.assertIn('"schema_version": 3', state)

    def test_alignment_change_precedes_contract_repair(self):
        execute = (SKILL / "references" / "execute-aligned-work.md").read_text()
        transition = execute.index("Transition the packet to `needs_alignment`")
        revise = execute.index("Revise `alignment.md`")
        self.assertLess(transition, revise)
        self.assertIn("do not ask the user to approve a revised plan", (SKILL / "SKILL.md").read_text())

    def test_plan_change_never_reopens_alignment(self):
        skill = (SKILL / "SKILL.md").read_text()
        plan = (SKILL / "references" / "write-plan.md").read_text()
        execute = (SKILL / "references" / "execute-aligned-work.md").read_text()
        self.assertIn("A changed plan is never an alignment event.", skill)
        self.assertIn("never changes the protected alignment digest", plan)
        self.assertIn("Continue without user involvement.", execute)
        self.assertIn("never a reason to reopen alignment by itself", execute)

    def test_equally_strong_proof_substitution_stays_in_plan(self):
        skill = (SKILL / "SKILL.md").read_text()
        alignment = (SKILL / "references" / "write-alignment.md").read_text()
        plan = (SKILL / "references" / "write-plan.md").read_text()
        packet = (SKILL / "references" / "packet-contract.md").read_text()
        template = (SKILL / "assets" / "packet-templates" / "alignment.md").read_text()
        self.assertIn("Seal observable invariants and minimum evidence strength", skill)
        self.assertIn("Apply the substitution test", alignment)
        for forbidden_mechanism in ("merge methods", "commit ancestry", "commands", "tools"):
            self.assertIn(forbidden_mechanism, alignment)
        self.assertIn("squash merging prevents PR-head ancestry", plan)
        self.assertIn("byte-for-byte tree equivalence", plan)
        self.assertIn("Substitute equal-or-stronger evidence without entering `needs_alignment`", packet)
        self.assertIn("equally strong proof substitutions belong in the mutable plan", template)

    def test_front_failure_precedes_approval_clearing_alignment_transition(self):
        front = (SKILL.parent / "front-agent-orchestration" / "SKILL.md").read_text()
        protocol = (SKILL.parent / "front-agent-orchestration" / "references" / "protocol.md").read_text()
        packet = (SKILL / "references" / "packet-contract.md").read_text()
        for text in (front, protocol, packet):
            self.assertIn("before", text)
            self.assertIn("needs_alignment", text)
            self.assertIn("approval-cleared", text)

    def test_one_alignment_approval_starts_agent_planning_and_execution(self):
        skill = (SKILL / "SKILL.md").read_text()
        packet = (SKILL / "references" / "packet-contract.md").read_text()
        execute = (SKILL / "references" / "execute-aligned-work.md").read_text()
        self.assertIn("one plain-language alignment contract", skill)
        self.assertIn("do not ask a second", skill)
        self.assertIn("--reuse-approval", packet)
        self.assertIn("file-recorded approval alone is insufficient", execute)
        self.assertIn("do not ask the user to approve the plan", execute)

    def test_required_resources_exist_without_freezing_package_inventory(self):
        required = {
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/planning_packet.py",
            "scripts/preservation_journal.py",
            "scripts/work_authority.py",
            "references/packet-contract.md",
            "references/explore-and-align.md",
            "references/write-alignment.md",
            "references/write-plan.md",
            "references/review-plan.md",
            "references/execute-aligned-work.md",
            "references/work-authority-v1.schema.json",
            "references/work-authority-v2.schema.json",
            "references/packet-transfer-receipt-v1.schema.json",
            "assets/packet-templates/alignment.md",
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
        self.assertTrue(required.issubset(actual), sorted(required - actual))


if __name__ == "__main__":
    unittest.main()
