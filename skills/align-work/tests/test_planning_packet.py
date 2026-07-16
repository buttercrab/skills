from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "planning_packet.py"
SPEC = importlib.util.spec_from_file_location("planning_packet", SCRIPT)
packet_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(packet_module)


class PacketCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.coordinator = str(uuid.uuid4())

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, code=0, env=None):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        self.assertEqual(result.returncode, code, result.stderr or result.stdout)
        stream = result.stdout if code == 0 else result.stderr
        return json.loads(stream)

    def init(self, task="sample-task"):
        data = self.run_cli(
            "init",
            "--repo",
            self.repo,
            "--task-id",
            task,
            "--title",
            "Sample task",
            "--coordinator-id",
            self.coordinator,
        )
        return Path(data["packet"])

    def init_legacy(self, task="legacy-task"):
        packet = self.init_v2(task)
        state = self.state(packet)
        state["schema_version"] = 1
        state["requested_authority_classes"] = []
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet)
        return packet

    def init_v2(self, task="v2-task"):
        packet = self.init(task)
        state = self.state(packet)
        state["schema_version"] = 2
        (packet / "state.json").write_text(json.dumps(state))
        (packet / "plan.md").write_text(
            "\n".join(
                (
                    "# Plan: Sample task",
                    "",
                    f"<!-- Task ID: `{task}` -->",
                    "",
                    "<!-- align-work-required-content -->",
                    "",
                    "## Outcome",
                    "Legacy outcome.",
                    "## Current state and decisions",
                    "Legacy state.",
                    "## Scope and boundaries",
                    "Legacy scope.",
                    "## Implementation approach",
                    "Legacy implementation.",
                    "## Verification",
                    "Legacy verification.",
                    "## Risks and rollback",
                    "Legacy risks.",
                    "## Approval scope",
                    "Legacy approval scope.",
                    "",
                )
            )
        )
        self.run_cli("validate", packet)
        return packet

    @staticmethod
    def state(packet):
        return json.loads((packet / "state.json").read_text())

    def fence(self, packet):
        state = self.state(packet)
        return (
            "--expected-revision",
            str(state["packet_revision"]),
            "--expected-epoch",
            str(state["active_coordinator"]["epoch"]),
            "--expected-generation",
            str(state["state_generation"]),
            "--coordinator-id",
            state["active_coordinator"]["id"],
        )

    def to_drafting(self, packet):
        self.run_cli("transition", packet, *self.fence(packet), "--to", "drafting")

    @staticmethod
    def complete_required_content(packet):
        for name in ("alignment.md", "facts.md", "decisions.md", "plan.md"):
            path = packet / name
            if path.exists():
                path.write_text(path.read_text().replace("<!-- align-work-required-content -->", "Authored fixture content."))

    def seal_for_approval(self, packet):
        self.complete_required_content(packet)
        self.to_drafting(packet)
        return self.run_cli(
            "seal",
            packet,
            *self.fence(packet),
            "--status",
            "awaiting_approval",
        )

    def approve(self, packet):
        return self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "approved",
            "--approval-id",
            str(uuid.uuid4()),
            "--approval-evidence",
            "current user approved exact digest",
        )

    def seal_legacy_for_approval(self, packet):
        self.complete_required_content(packet)
        self.to_drafting(packet)
        return self.run_cli(
            "seal",
            packet,
            *self.fence(packet),
            "--status",
            "awaiting_approval",
            "--authority",
            "R,T",
        )

    def approve_legacy(self, packet, authority=None):
        args = [
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "approved",
            "--approval-id",
            str(uuid.uuid4()),
            "--approval-evidence",
            "current user approved exact digest",
        ]
        if authority is not None:
            args.extend(("--authority", authority))
        return self.run_cli(*args)

    def execute(self, packet):
        return self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "executing",
            "--authorization-evidence",
            "current session user authorization",
        )

    def execute_reusing_approval(self, packet):
        return self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "executing",
            "--reuse-approval",
        )

    def test_init_validate_and_no_overwrite(self):
        packet = self.init()
        result = self.run_cli("validate", packet)
        self.assertEqual(result["status"], "discovery")
        state = self.state(packet)
        self.assertEqual(state["schema_version"], 3)
        self.assertTrue((packet / "alignment.md").is_file())
        self.assertNotIn("requested_authority_classes", state)
        self.assertIsNone(state["protected_digest"])
        failure = self.run_cli(
            "init",
            "--repo",
            self.repo,
            "--task-id",
            "sample-task",
            code=6,
        )
        self.assertIn("filesystem operation failed", failure["invariant"])

    def test_untouched_templates_cannot_be_sealed(self):
        packet = self.init()
        self.to_drafting(packet)
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval", code=3,
        )

    def test_v3_state_approval_and_output_omit_legacy_class_fields(self):
        packet = self.init()
        sealed = self.seal_for_approval(packet)
        self.assertNotIn("authority", sealed)
        self.approve(packet)
        state = self.state(packet)
        self.assertNotIn("requested_authority_classes", state)
        self.assertNotIn("authority_classes", state["approval"])
        self.run_cli("validate", packet)

    def test_schema_versions_reject_hybrid_field_sets(self):
        packet = self.init()
        state = self.state(packet)
        state["requested_authority_classes"] = []
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

        packet = self.init_legacy("legacy-missing-field")
        state = self.state(packet)
        del state["requested_authority_classes"]
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

        packet = self.init("v3-hybrid-approval")
        self.seal_for_approval(packet)
        self.approve(packet)
        state = self.state(packet)
        state["approval"]["authority_classes"] = ["R"]
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

        packet = self.init_legacy("v1-hybrid-approval")
        self.seal_legacy_for_approval(packet)
        self.approve_legacy(packet)
        state = self.state(packet)
        del state["approval"]["authority_classes"]
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

    def test_normal_cli_help_hides_legacy_authority_option(self):
        for command in ("seal", "transition"):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), command, "--help"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("--authority", result.stdout)

    def test_v3_rejects_legacy_authority_option_atomically(self):
        packet = self.init()
        self.complete_required_content(packet)
        self.to_drafting(packet)
        before = (packet / "state.json").read_bytes()
        failure = self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
            "--authority", "R,T", code=3,
        )
        self.assertIn("legacy schema version 1", failure["invariant"])
        self.assertEqual((packet / "state.json").read_bytes(), before)

        self.run_cli("seal", packet, *self.fence(packet), "--status", "awaiting_approval")
        before = (packet / "state.json").read_bytes()
        failure = self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "approved",
            "--approval-id", str(uuid.uuid4()), "--approval-evidence", "current user approved",
            "--authority", "R,T", code=3,
        )
        self.assertIn("legacy schema version 1", failure["invariant"])
        self.assertEqual((packet / "state.json").read_bytes(), before)

    def test_legacy_v1_lifecycle_accepts_approval_without_repeated_flag(self):
        packet = self.init_legacy()
        sealed = self.seal_legacy_for_approval(packet)
        self.assertEqual(sealed["authority"], ["R", "T"])
        self.approve_legacy(packet)
        state = self.state(packet)
        self.assertEqual(state["approval"]["authority_classes"], ["R", "T"])
        self.execute_reusing_approval(packet)
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "LEGACY-IMPLEMENT",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "legacy implementation passed",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "verifying")
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "LEGACY-VERIFY",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--evidence", "legacy gates passed", "--verification", "legacy packet verified",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete")
        self.assertEqual(self.state(packet)["status"], "complete")

    def test_legacy_v1_mismatch_repair_and_recovery_remain_supported(self):
        packet = self.init_legacy("legacy-recovery")
        self.seal_legacy_for_approval(packet)
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "approved",
            "--approval-id", str(uuid.uuid4()), "--approval-evidence", "current user approved",
            "--authority", "R", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)
        self.approve_legacy(packet)
        self.execute(packet)
        current = self.state(packet)
        self.run_cli(
            "recover", packet,
            "--expected-revision", str(current["packet_revision"]),
            "--expected-epoch", str(current["active_coordinator"]["epoch"]),
            "--expected-generation", str(current["state_generation"]),
            "--new-coordinator-id", str(uuid.uuid4()),
            "--evidence", "user authorized legacy recovery",
        )
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--authorization-evidence", "current user resumed legacy execution",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        with (packet / "plan.md").open("a") as handle:
            handle.write("\nLegacy replan fixture.\n")
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting")
        state = self.state(packet)
        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(state["requested_authority_classes"], [])
        self.run_cli("validate", packet)

    def test_legacy_numbered_plan_headings_are_valid(self):
        packet = self.init_v2()
        plan = (packet / "plan.md").read_text()
        replacements = {
            "## Outcome": "## 1. Outcome",
            "## Current state and decisions": "## 2. Consumed facts and decisions",
            "## Scope and boundaries": "## 3. Scope and authority",
            "## Implementation approach": "## 4. Implementation sequence",
            "## Verification": "## 5. Acceptance gates",
            "## Risks and rollback": "## 6. Risks and rollback",
            "## Approval scope": "## 7. Approval protocol",
        }
        for old, new in replacements.items():
            plan = plan.replace(old, new)
        (packet / "plan.md").write_text(plan)
        self.run_cli("validate", packet)

    def test_v3_plan_template_uses_agent_execution_headings(self):
        packet = self.init()
        plan = (packet / "plan.md").read_text()
        for heading in (
            "## Current state",
            "## Approach",
            "## Steps",
            "## Verification strategy",
            "## Risks and rollback",
        ):
            self.assertIn(heading, plan)
        self.assertNotIn("## Consumed facts and decisions", plan)
        self.assertNotIn("## Approval scope", plan)
        self.assertNotIn("stable step IDs", plan)
        self.run_cli("validate", packet)

    def test_v3_alignment_template_is_the_approval_contract(self):
        packet = self.init()
        alignment = (packet / "alignment.md").read_text()
        for heading in (
            "## Goal",
            "## Requirements",
            "## Non-goals",
            "## Constraints and authority",
            "## Acceptance checklist",
        ):
            self.assertIn(heading, alignment)
        self.assertNotIn("## Steps", alignment)
        self.run_cli("validate", packet)

    def test_semantic_heading_aliases_and_empty_open_questions_are_valid(self):
        packet = self.init()
        facts = (packet / "facts.md").read_text()
        facts = facts.replace("## Inferences", "## Design inferences to validate")
        facts = facts.replace("## Unknowns", "## Known unknowns at approval time")
        (packet / "facts.md").write_text(facts)
        decisions = (packet / "decisions.md").read_text()
        decisions = decisions.replace("## Open questions\n\n", "")
        decisions = decisions.replace("## Alignment rounds", "## Alignment-round ledger")
        (packet / "decisions.md").write_text(decisions)
        self.run_cli("validate", packet)

    def test_unsafe_slug_and_symlinked_planning(self):
        self.run_cli("init", "--repo", self.repo, "--task-id", "../escape", code=5)
        other = Path(self.temp.name) / "other"
        other.mkdir()
        (self.repo / ".planning").symlink_to(other, target_is_directory=True)
        self.run_cli("init", "--repo", self.repo, "--task-id", "safe-task", code=5)

    def test_golden_digest_vector(self):
        packet = self.repo / ".planning" / "vector"
        packet.mkdir(parents=True)
        (packet / "decisions.md").write_bytes(b"D\n")
        (packet / "facts.md").write_bytes(b"F\n")
        (packet / "plan.md").write_bytes(b"P\n")
        self.assertEqual(
            packet_module.compute_digest(packet),
            "a3aabbf6e45c71eccf898988a0c91ded833effa82cf15809d3a20a127e0a1a1b",
        )
        (packet / "plan.md").write_bytes(b"P\r\n")
        self.assertNotEqual(
            packet_module.compute_digest(packet),
            "a3aabbf6e45c71eccf898988a0c91ded833effa82cf15809d3a20a127e0a1a1b",
        )

    def test_v3_digest_covers_alignment_only(self):
        packet = self.init()
        self.complete_required_content(packet)
        original = packet_module.compute_digest(packet, 3)
        (packet / "plan.md").write_text((packet / "plan.md").read_text() + "\nAgent plan revision.\n")
        (packet / "facts.md").write_text((packet / "facts.md").read_text() + "\nNew fact.\n")
        self.assertEqual(original, packet_module.compute_digest(packet, 3))
        (packet / "alignment.md").write_text((packet / "alignment.md").read_text() + "\nNew requirement.\n")
        self.assertNotEqual(original, packet_module.compute_digest(packet, 3))

    def test_v3_seals_alignment_before_plan_and_requires_plan_for_execution(self):
        packet = self.init()
        alignment = packet / "alignment.md"
        alignment.write_text(alignment.read_text().replace("<!-- align-work-required-content -->", "Aligned fixture content."))
        self.to_drafting(packet)
        self.run_cli("seal", packet, *self.fence(packet), "--status", "awaiting_approval")
        self.approve(packet)
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--reuse-approval", code=3,
        )
        plan = packet / "plan.md"
        plan.write_text(plan.read_text().replace("<!-- align-work-required-content -->", "Agent-authored fixture plan."))
        self.execute_reusing_approval(packet)

    def test_open_questions_block_advancement(self):
        packet = self.init()
        self.run_cli("questions", packet, *self.fence(packet), "--set", "Q-001")
        self.run_cli("transition", packet, *self.fence(packet), "--to", "drafting", code=3)
        self.run_cli("questions", packet, *self.fence(packet))
        self.to_drafting(packet)

    def test_invalid_question_id_is_rejected(self):
        packet = self.init()
        self.run_cli("questions", packet, *self.fence(packet), "--set", "question-one", code=3)

    def test_approval_execution_and_attempt_chain(self):
        packet = self.init()
        sealed = self.seal_for_approval(packet)
        self.assertRegex(sealed["digest"], r"^[0-9a-f]{64}$")
        self.approve(packet)
        self.execute(packet)
        attempt = self.run_cli(
            "record-attempt",
            packet,
            *self.fence(packet),
            "--step-id",
            "S1",
            "--actor-id",
            "root",
            "--model",
            "strong-model",
            "--status",
            "passed",
            "--action",
            "implemented fixture",
            "--evidence",
            "unit receipt",
            "--verification",
            "passed",
        )
        self.assertRegex(attempt["entry_hash"], r"^[0-9a-f]{64}$")
        valid = self.run_cli("validate", packet)
        self.assertEqual(valid["status"], "executing")
        self.assertEqual(self.state(packet)["execution_head"], attempt["entry_hash"])

    def test_execution_markdown_is_readable_and_marker_stays_authoritative(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli(
            "record-attempt",
            packet,
            *self.fence(packet),
            "--step-id",
            "S-SECRET-001",
            "--actor-id",
            "private-actor",
            "--model",
            "private-model",
            "--status",
            "passed",
            "--action",
            "Updated <helper> <!-- align-work-attempt {forged}",
            "--mutation",
            "Changed approval rendering",
            "--evidence",
            "All tests passed",
            "--verification",
            "Verified readable output",
        )
        text = (packet / "execution.md").read_text()
        visible = "\n".join(line for line in text.splitlines() if "<!-- align-work-attempt " not in line)
        marker_line = next(line for line in text.splitlines() if line.startswith("<!-- align-work-attempt "))
        marker = json.loads(packet_module.MARKER_RE.fullmatch(marker_line).group(1))
        self.assertIn("## Updated &lt;helper&gt;", visible)
        self.assertIn("- Status: **Passed**", visible)
        self.assertIn("Changed approval rendering", visible)
        self.assertIn("Verified readable output", visible)
        self.assertNotIn("S-SECRET-001", visible)
        self.assertNotIn("private-actor", visible)
        self.assertNotIn("private-model", visible)
        self.assertNotRegex(visible, r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
        self.assertEqual(marker["step_id"], "S-SECRET-001")
        self.assertEqual(marker["actor_id"], "private-actor")
        self.assertEqual(marker["model"], "private-model")
        self.run_cli("validate", packet)

    def test_approval_can_start_and_resume_without_a_second_user_event(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        approval_id = self.state(packet)["approval"]["id"]
        self.execute_reusing_approval(packet)
        self.assertEqual(
            self.state(packet)["runtime_authorization_evidence"],
            f"approval:{approval_id}",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "paused")
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--reuse-approval",
        )
        resumed = self.state(packet)
        self.assertEqual(resumed["status"], "executing")
        self.assertEqual(resumed["runtime_authorization_evidence"], f"approval:{approval_id}")

    def test_reuse_approval_rejects_conflicts_and_rollback(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--reuse-approval", "--authorization-evidence", "duplicate event", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)

        self.execute_reusing_approval(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--rollback", "--partial-work-disposition", "roll back partial work",
            "--reuse-approval", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)

    def test_reused_approval_can_complete_a_verified_task(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute_reusing_approval(packet)
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--action", "implemented approved work", "--verification", "implementation passed",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "verifying")
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "VERIFY",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--evidence", "required gates passed", "--verification", "verified current revision",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete")
        self.assertEqual(self.state(packet)["status"], "complete")

    def test_stale_generation_and_wrong_owner_are_rejected(self):
        packet = self.init()
        stale = self.fence(packet)
        self.run_cli("questions", packet, *stale, "--set", "Q-001")
        self.run_cli("questions", packet, *stale, code=4)
        current = list(self.fence(packet))
        current[-1] = str(uuid.uuid4())
        self.run_cli("questions", packet, *current, code=4)

    def test_digest_mismatch_is_read_only_then_repair_clears_approval(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        before = (packet / "state.json").read_bytes()
        with (packet / "alignment.md").open("a") as handle:
            handle.write("\nmaterial revision\n")
        self.run_cli("validate", packet, code=3)
        self.assertEqual((packet / "state.json").read_bytes(), before)
        repaired = self.run_cli(
            "repair",
            packet,
            *self.fence(packet),
            "--status",
            "drafting",
        )
        self.assertEqual(repaired["status"], "drafting")
        self.assertIsNone(self.state(packet)["approval"])
        self.run_cli("validate", packet)

    def test_handoff_fences_old_coordinator(self):
        packet = self.init()
        old_fence = self.fence(packet)
        new_id = str(uuid.uuid4())
        self.run_cli(
            "handoff",
            packet,
            *old_fence,
            "--to-coordinator-id",
            new_id,
            "--evidence",
            "orderly test handoff",
        )
        self.run_cli("questions", packet, *old_fence, code=4)
        self.assertEqual(self.state(packet)["active_coordinator"]["id"], new_id)

    def test_pause_resumes_only_to_recorded_state(self):
        packet = self.init()
        self.run_cli("transition", packet, *self.fence(packet), "--to", "paused")
        self.run_cli("transition", packet, *self.fence(packet), "--to", "drafting", code=3)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "discovery")
        self.assertIsNone(self.state(packet)["resume_status"])

    def test_recover_requires_evidence_and_increments_epoch(self):
        packet = self.init()
        state = self.state(packet)
        self.run_cli(
            "recover",
            packet,
            "--expected-revision",
            "0",
            "--expected-epoch",
            "1",
            "--expected-generation",
            "0",
            "--evidence",
            "",
            code=3,
        )
        result = self.run_cli(
            "recover",
            packet,
            "--expected-revision",
            "0",
            "--expected-epoch",
            "1",
            "--expected-generation",
            "0",
            "--evidence",
            "user authorized recovery",
        )
        self.assertEqual(result["coordinator"]["epoch"], state["active_coordinator"]["epoch"] + 1)

    def test_illegal_transition_and_v2_approval_option_rejection(self):
        packet = self.init()
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete", code=3)
        self.seal_for_approval(packet)
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "approved",
            "--approval-id",
            str(uuid.uuid4()),
            "--authority",
            "R",
            "--approval-evidence",
            "wrong authority",
            code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)

    def test_torn_execution_marker_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        with (packet / "execution.md").open("a") as handle:
            handle.write("\n<!-- align-work-attempt {torn\n")
        self.run_cli("validate", packet, code=3)

    def test_missing_execution_entry_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli(
            "record-attempt",
            packet,
            *self.fence(packet),
            "--step-id",
            "S1",
            "--actor-id",
            "root",
            "--model",
            "strong-model",
            "--status",
            "passed",
        )
        lines = (packet / "execution.md").read_text().splitlines()
        (packet / "execution.md").write_text("\n".join(line for line in lines if "align-work-attempt" not in line) + "\n")
        self.run_cli("validate", packet, code=3)

    def test_symlinked_protected_file_is_rejected(self):
        packet = self.init()
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("outside")
        (packet / "facts.md").unlink()
        (packet / "facts.md").symlink_to(outside)
        self.run_cli("validate", packet, code=5)

    def test_portable_or_malformed_approval_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        state = self.state(packet)
        state["approval"]["portable"] = True
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

    def test_unknown_state_field_is_rejected(self):
        packet = self.init()
        state = self.state(packet)
        state["unexpected"] = True
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

    def test_atomic_state_write_crash_boundaries_leave_complete_state(self):
        packet = self.init()
        before = (packet / "state.json").read_bytes()
        env = dict(os.environ, ALIGN_WORK_TEST_CRASH="before-replace")
        self.run_cli("questions", packet, *self.fence(packet), "--set", "Q-001", code=6, env=env)
        self.assertEqual((packet / "state.json").read_bytes(), before)
        json.loads((packet / "state.json").read_text())

        env = dict(os.environ, ALIGN_WORK_TEST_CRASH="after-replace")
        self.run_cli("questions", packet, *self.fence(packet), "--set", "Q-001", code=6, env=env)
        after = json.loads((packet / "state.json").read_text())
        self.assertEqual(after["open_question_ids"], ["Q-001"])

    def test_one_unanchored_tail_can_be_repaired(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        payload = {
            "attempt_id": str(uuid.uuid4()),
            "packet_id": self.state(packet)["packet_id"],
            "packet_revision": self.state(packet)["packet_revision"],
            "protected_digest": self.state(packet)["protected_digest"],
            "approval_id": self.state(packet)["approval"]["id"],
            "previous_hash": None,
            "step_id": "S1",
            "actor_id": "root",
            "model": "strong-model",
            "status": "passed",
            "started_at": "2026-07-12T12:00:00+09:00",
            "ended_at": "2026-07-12T12:01:00+09:00",
            "actions": [],
            "mutations": [],
            "evidence": ["receipt"],
            "verification": "passed",
            "disposition": None,
        }
        record = {**payload, "entry_hash": packet_module.attempt_hash(payload)}
        state = self.state(packet)
        state["pending_execution_hash"] = record["entry_hash"]
        (packet / "state.json").write_text(json.dumps(state))
        with (packet / "execution.md").open("a") as handle:
            handle.write("\n<!-- align-work-attempt " + packet_module.canonical_json(record).decode() + " -->\n")
        self.run_cli("validate", packet, code=3)
        repaired = self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting")
        self.assertEqual(repaired["execution_head"], record["entry_hash"])

    def test_cross_repository_packet_copy_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        other = Path(self.temp.name) / "other-repo"
        target = other / ".planning" / packet.name
        target.parent.mkdir(parents=True)
        shutil.copytree(packet, target)
        self.run_cli("validate", target, code=5)

    def test_dangling_lock_symlink_cannot_create_outside_target(self):
        packet = self.init()
        outside = Path(self.temp.name) / "outside-lock"
        (packet / ".state.lock").symlink_to(outside)
        self.run_cli("questions", packet, *self.fence(packet), "--set", "Q-001", code=5)
        self.assertFalse(outside.exists())

    def test_hard_linked_execution_ledger_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        ledger = packet / "execution.md"
        outside = Path(self.temp.name) / "outside-execution.md"
        outside.write_bytes(ledger.read_bytes())
        ledger.unlink()
        os.link(outside, ledger)
        before = outside.read_bytes()
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--evidence", "receipt", "--verification", "passed", code=5,
        )
        self.assertEqual(outside.read_bytes(), before)

    def test_forged_minimal_execution_tail_cannot_be_repaired(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        payload = {"previous_hash": None}
        entry = packet_module.attempt_hash(payload)
        record = {**payload, "entry_hash": entry}
        state = self.state(packet)
        state["pending_execution_hash"] = entry
        (packet / "state.json").write_text(json.dumps(state))
        with (packet / "execution.md").open("a") as handle:
            handle.write("\n<!-- align-work-attempt " + packet_module.canonical_json(record).decode() + " -->\n")
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting", code=3)

    def test_rollback_requires_current_authorization(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--rollback", "--partial-work-disposition", "roll back partial change", code=3,
        )

    def test_preexecution_material_change_creates_valid_ledger(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.assertFalse((packet / "execution.md").exists())
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        self.assertTrue((packet / "execution.md").is_file())
        result = self.run_cli("validate", packet)
        self.assertEqual(result["status"], "needs_alignment")
        self.assertIsNone(self.state(packet)["approval"])

    def test_needs_alignment_rejects_execution_attempts(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "passed", code=3,
        )

    def test_old_revision_receipt_cannot_complete_realigned_work(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "old revision passed",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        with (packet / "alignment.md").open("a") as handle:
            handle.write("\nMaterially revised requirement.\n")
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting")
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
        )
        self.approve(packet)
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "verifying")
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete", code=3)

    def test_recover_active_execution_pauses_and_requires_new_authorization(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        before = self.state(packet)
        self.run_cli(
            "recover", packet,
            "--expected-revision", str(before["packet_revision"]),
            "--expected-epoch", str(before["active_coordinator"]["epoch"]),
            "--expected-generation", str(before["state_generation"]),
            "--new-coordinator-id", str(uuid.uuid4()),
            "--evidence", "user authorized fresh-session recovery",
        )
        recovered = self.state(packet)
        self.assertEqual(recovered["status"], "paused")
        self.assertEqual(recovered["resume_status"], "executing")
        self.assertIsNone(recovered["runtime_authorization_evidence"])
        self.run_cli("transition", packet, *self.fence(packet), "--to", "executing", code=3)
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--authorization-evidence", "current session user reauthorized execution",
        )

    def test_rollback_verification_cannot_complete_original_task(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--rollback", "--partial-work-disposition", "roll back partial work",
            "--authorization-evidence", "current user authorized rollback",
        )
        self.assertIn("partial-work disposition: roll back partial work", self.state(packet)["runtime_authorization_evidence"])
        self.run_cli("transition", packet, *self.fence(packet), "--to", "verifying")
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "ROLLBACK-VERIFY",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "rollback verified",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete", code=3)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")

    def test_seal_rejects_torn_existing_execution_ledger(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        with (packet / "alignment.md").open("a") as handle:
            handle.write("\nRealigned requirement.\n")
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting")
        with (packet / "execution.md").open("a") as handle:
            handle.write("\n<!-- align-work-attempt {torn\n")
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval", code=3,
        )

    def test_multiline_execution_identity_is_rejected_before_append(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        before = (packet / "execution.md").read_bytes()
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1\n<!-- align-work-attempt {torn",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "passed", code=3,
        )
        self.assertEqual((packet / "execution.md").read_bytes(), before)

    def test_unicode_line_separator_is_safe_in_execution_records(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        before = (packet / "execution.md").read_bytes()
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1\u2028forged",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "passed", code=3,
        )
        self.assertEqual((packet / "execution.md").read_bytes(), before)
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--action", "observed\u2028continued", "--verification", "passed\u2028verified",
        )
        self.run_cli("validate", packet)
        marker = next(
            line for line in (packet / "execution.md").read_text().splitlines()
            if line.startswith("<!-- align-work-attempt ")
        )
        self.assertIn("\\u2028", marker)

    def test_whitespace_approval_evidence_is_rejected_atomically(self):
        packet = self.init()
        self.seal_for_approval(packet)
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "approved",
            "--approval-id", str(uuid.uuid4()),
            "--approval-evidence", "   ", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)

    def test_new_approval_evidence_is_concise_single_line_and_atomic(self):
        packet = self.init()
        self.seal_for_approval(packet)
        before = (packet / "state.json").read_bytes()
        for evidence in (
            "first line\nsecond line",
            "contains\ta control",
            "x" * (packet_module.MAX_AUDIT_EVIDENCE_LENGTH + 1),
        ):
            failure = self.run_cli(
                "transition",
                packet,
                *self.fence(packet),
                "--to",
                "approved",
                "--approval-id",
                str(uuid.uuid4()),
                "--approval-evidence",
                evidence,
                code=3,
            )
            self.assertNotIn(evidence, json.dumps(failure))
            self.assertEqual((packet / "state.json").read_bytes(), before)
        self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "approved",
            "--approval-id",
            str(uuid.uuid4()),
            "--approval-evidence",
            "  사용자가 이 작업을 승인함  ",
        )
        self.assertEqual(self.state(packet)["approval"]["user_evidence"], "사용자가 이 작업을 승인함")

    def test_approval_reuse_error_does_not_disclose_approval_object(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "approved",
            "--approval-id",
            str(uuid.uuid4()),
            "--approval-evidence",
            "sensitive approval reference",
        )
        saved_approval = self.state(packet)["approval"]
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        state = self.state(packet)
        state["approval"] = saved_approval
        (packet / "state.json").write_text(json.dumps(state))
        failure = self.run_cli(
            "transition",
            packet,
            *self.fence(packet),
            "--to",
            "executing",
            "--rollback",
            "--partial-work-disposition",
            "roll back partial work",
            "--reuse-approval",
            code=3,
        )
        serialized = json.dumps(failure)
        self.assertNotIn("sensitive approval reference", serialized)
        self.assertNotIn("user_evidence", serialized)
        self.assertEqual(failure["observed"]["approval_present"], True)

    def test_whitespace_partial_disposition_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "approved",
            "--approval-id", str(uuid.uuid4()),
            "--approval-evidence", "current user reapproved",
            "--partial-work-disposition", "   ", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--rollback", "--partial-work-disposition", "   ",
            "--authorization-evidence", "current user authorized rollback", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)

    def test_whitespace_execution_authorization_has_no_side_effect(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--authorization-evidence", "   ", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)
        self.assertFalse((packet / "execution.md").exists())
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--rollback", "--partial-work-disposition", "not applicable",
            "--authorization-evidence", "current session authorization", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)
        self.assertFalse((packet / "execution.md").exists())

    def test_disconnected_coordinator_history_is_rejected(self):
        packet = self.init()
        state = self.state(packet)
        state["coordinator_history"] = [{
            "event": "handoff",
            "from": {"id": str(uuid.uuid4()), "epoch": 99},
            "to": {"id": str(uuid.uuid4()), "epoch": 1},
            "recorded_at": state["last_transition_at"],
            "evidence": "forged",
            "disposition": "forged disconnected history",
        }]
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

    def test_complete_requires_final_passed_verification_receipt(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "verifying")
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete", code=3)

    def test_terminal_state_cannot_be_resealed_and_valid_packet_cannot_be_repaired(self):
        packet = self.init()
        self.complete_required_content(packet)
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting", code=3)
        self.to_drafting(packet)
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval"
        )
        self.approve(packet)
        self.execute(packet)
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "GATE-1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--evidence", "receipt", "--verification", "passed",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "verifying")
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete")
        self.run_cli("seal", packet, *self.fence(packet), "--status", "drafting", code=3)

    def test_boolean_integer_and_unknown_authority_are_rejected(self):
        packet = self.init()
        state = self.state(packet)
        state["packet_revision"] = True
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

        packet = self.init_legacy("authority-task")
        self.complete_required_content(packet)
        self.to_drafting(packet)
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
            "--authority", "UNKNOWN", code=3,
        )

    def test_malformed_utf8_and_unowned_recover_have_structured_errors(self):
        packet = self.init()
        state = self.state(packet)
        state["active_coordinator"] = {"wrong": "shape"}
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli("validate", packet, code=3)

        packet = self.init("utf8-task")
        (packet / "facts.md").write_bytes(b"\xff")
        self.run_cli("validate", packet, code=3)

        packet = self.init("unowned-task")
        state = self.state(packet)
        state["active_coordinator"] = None
        (packet / "state.json").write_text(json.dumps(state))
        self.run_cli(
            "recover", packet, "--expected-revision", "0", "--expected-epoch", "1",
            "--expected-generation", "0", "--evidence", "user authorized recovery", code=4,
        )


if __name__ == "__main__":
    unittest.main()
