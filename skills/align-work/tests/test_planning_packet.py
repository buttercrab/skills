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
        for name in ("facts.md", "decisions.md", "plan.md"):
            path = packet / name
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
            "--authority",
            "R,T",
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
            "--authority",
            "R,T",
            "--approval-evidence",
            "current user approved exact digest",
        )

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

    def test_init_validate_and_no_overwrite(self):
        packet = self.init()
        result = self.run_cli("validate", packet)
        self.assertEqual(result["status"], "discovery")
        self.assertIsNone(self.state(packet)["protected_digest"])
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
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
            "--authority", "R,T", code=3,
        )

    def test_numbered_hierarchical_plan_headings_are_valid(self):
        packet = self.init()
        plan = (packet / "plan.md").read_text()
        replacements = {
            "## Outcome": "## 1. Outcome",
            "## Consumed facts and decisions": "## 2. Consumed facts and decisions",
            "## Scope and authority": "## 3. Scope and authority",
            "## Implementation sequence": "## 4. Implementation sequence",
            "## Acceptance gates": "## 5. Acceptance gates",
            "## Risks and rollback": "## 6. Risks and rollback",
            "## Approval": "## 7. Approval protocol",
        }
        for old, new in replacements.items():
            plan = plan.replace(old, new)
        (packet / "plan.md").write_text(plan)
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
        with (packet / "plan.md").open("a") as handle:
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

    def test_illegal_transition_and_stale_approval(self):
        packet = self.init()
        self.run_cli("transition", packet, *self.fence(packet), "--to", "complete", code=3)
        self.seal_for_approval(packet)
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
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--rollback", "--partial-work-disposition", "roll back partial change", code=3,
        )

    def test_preexecution_material_change_creates_valid_ledger(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.assertFalse((packet / "execution.md").exists())
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        self.assertTrue((packet / "execution.md").is_file())
        result = self.run_cli("validate", packet)
        self.assertEqual(result["status"], "needs_reapproval")
        self.assertIsNone(self.state(packet)["approval"])

    def test_needs_reapproval_rejects_execution_attempts(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "passed", code=3,
        )

    def test_old_revision_receipt_cannot_complete_replanned_work(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli(
            "record-attempt", packet, *self.fence(packet), "--step-id", "S1",
            "--actor-id", "root", "--model", "strong-model", "--status", "passed",
            "--verification", "old revision passed",
        )
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        with (packet / "plan.md").open("a") as handle:
            handle.write("\nMaterially revised implementation detail.\n")
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting")
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
            "--authority", "R,T",
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
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
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
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")

    def test_seal_rejects_torn_existing_execution_ledger(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.execute(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        with (packet / "plan.md").open("a") as handle:
            handle.write("\nReplanned.\n")
        self.run_cli("repair", packet, *self.fence(packet), "--status", "drafting")
        with (packet / "execution.md").open("a") as handle:
            handle.write("\n<!-- align-work-attempt {torn\n")
        self.run_cli(
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
            "--authority", "R,T", code=3,
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
            "--approval-id", str(uuid.uuid4()), "--authority", "R,T",
            "--approval-evidence", "   ", code=3,
        )
        self.assertEqual((packet / "state.json").read_bytes(), before)

    def test_whitespace_partial_disposition_is_rejected(self):
        packet = self.init()
        self.seal_for_approval(packet)
        self.approve(packet)
        self.run_cli("transition", packet, *self.fence(packet), "--to", "needs_reapproval")
        before = (packet / "state.json").read_bytes()
        self.run_cli(
            "transition", packet, *self.fence(packet), "--to", "approved",
            "--approval-id", str(uuid.uuid4()), "--authority", "R,T",
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
            "seal", packet, *self.fence(packet), "--status", "awaiting_approval", "--authority", "R,T"
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

        packet = self.init("authority-task")
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
