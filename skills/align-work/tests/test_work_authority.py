from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "planning_packet.py"
sys.path.insert(0, str(SKILL / "scripts"))

import work_authority


class WorkAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="work-authority-")
        self.repo = (Path(self.temp.name) / "repo").resolve()
        self.repo.mkdir()
        self.coordinator = str(uuid.uuid4())

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stderr or result.stdout)
        return json.loads(result.stdout if code == 0 else result.stderr)

    def state(self, packet):
        return json.loads((packet / "state.json").read_text())

    def fence(self, packet):
        state = self.state(packet)
        return (
            "--expected-revision", str(state["packet_revision"]),
            "--expected-epoch", str(state["active_coordinator"]["epoch"]),
            "--expected-generation", str(state["state_generation"]),
            "--coordinator-id", state["active_coordinator"]["id"],
        )

    def approved_packet(self, task="sample-task"):
        initialized = self.cli(
            "init", "--repo", self.repo, "--task-id", task,
            "--title", "Sample task", "--coordinator-id", self.coordinator,
        )
        packet = Path(initialized["packet"])
        for name in ("facts.md", "decisions.md", "plan.md"):
            path = packet / name
            path.write_text(path.read_text().replace("<!-- align-work-required-content -->", "Authored fixture content."))
        self.cli("transition", packet, *self.fence(packet), "--to", "drafting")
        self.cli("seal", packet, *self.fence(packet), "--status", "awaiting_approval", "--authority", "R,T")
        self.cli(
            "transition", packet, *self.fence(packet), "--to", "approved",
            "--approval-id", str(uuid.uuid4()), "--authority", "R,T",
            "--approval-evidence", "current user approved exact digest",
        )
        return packet

    def authority(self, request, packet=None, *, mode="packet", sequence=0, classification="existing-packet"):
        binding = None
        if packet is not None:
            binding = work_authority.binding_from_state(self.repo, packet, self.state(packet))
        return {
            "schema_version": "work_authority/v1",
            "work_id": str(uuid.uuid4()),
            "sequence": sequence,
            "original_request_sha256": hashlib.sha256(request.encode()).hexdigest(),
            "alignment_mode": mode,
            "gateway_classification": classification,
            "repository_root": str(self.repo),
            "packet_binding": binding,
        }

    def code(self, function):
        with self.assertRaises(work_authority.WorkAuthorityError) as caught:
            function()
        return caught.exception.code

    def test_valid_packet_and_none_modes(self):
        request = "Implement the approved packet."
        packet = self.approved_packet()
        result = work_authority.validate_current(
            self.authority(request, packet), original_request=request, repository=self.repo
        )
        self.assertEqual("packet", result["alignment_mode"])

        other = (Path(self.temp.name) / "other").resolve()
        other.mkdir()
        plain = {
            "schema_version": "work_authority/v1",
            "work_id": str(uuid.uuid4()),
            "sequence": 0,
            "original_request_sha256": hashlib.sha256(b"Fix the typo.").hexdigest(),
            "alignment_mode": "none",
            "gateway_classification": "none",
            "repository_root": str(other),
            "packet_binding": None,
        }
        self.assertEqual(
            "none",
            work_authority.validate_current(plain, original_request="Fix the typo.", repository=other)["alignment_mode"],
        )

    def test_explicit_invocation_and_existing_packet_reject_forged_none(self):
        request = "Use $align-work for this change."
        none = self.authority(request, None, mode="none", classification="none")
        self.assertEqual(
            "E_ALIGNMENT_DISAGREEMENT",
            self.code(lambda: work_authority.validate_current(none, original_request=request, repository=self.repo)),
        )
        packet = self.approved_packet()
        request = "Continue the task."
        none = self.authority(request, None, mode="none", classification="none")
        self.assertEqual(
            "E_ALIGNMENT_DISAGREEMENT",
            self.code(lambda: work_authority.validate_current(none, original_request=request, repository=self.repo)),
        )
        self.assertTrue(packet.exists())

    def test_cross_root_symlink_stale_generation_and_changed_request_fail(self):
        packet = self.approved_packet()
        request = "Continue the approved packet."
        authority = self.authority(request, packet)

        changed = copy.deepcopy(authority)
        changed["repository_root"] = str(self.repo.parent)
        self.assertEqual(
            "E_REPOSITORY_ROOT",
            self.code(lambda: work_authority.validate_current(changed, original_request=request, repository=self.repo)),
        )

        changed = copy.deepcopy(authority)
        changed["packet_binding"]["state_generation"] -= 1
        self.assertEqual(
            "E_PACKET_FENCE_STALE",
            self.code(lambda: work_authority.validate_current(changed, original_request=request, repository=self.repo)),
        )

        changed = copy.deepcopy(authority)
        changed["packet_binding"]["approval_id"] = str(uuid.uuid4())
        self.assertEqual(
            "E_PACKET_FENCE_STALE",
            self.code(lambda: work_authority.validate_current(changed, original_request=request, repository=self.repo)),
        )

        self.assertEqual(
            "E_ORIGINAL_REQUEST_CHANGED",
            self.code(lambda: work_authority.validate_current(authority, original_request=request + " changed", repository=self.repo)),
        )

        link = self.repo / ".planning" / "linked-task"
        link.symlink_to(packet, target_is_directory=True)
        changed = copy.deepcopy(authority)
        changed["packet_binding"]["task_id"] = "linked-task"
        changed["packet_binding"]["packet_path"] = ".planning/linked-task"
        self.assertEqual(
            "E_PACKET_PATH",
            self.code(lambda: work_authority.validate_current(changed, original_request=request, repository=self.repo)),
        )

    def test_protected_artifact_change_invalidates_approved_authority(self):
        packet = self.approved_packet()
        request = "Continue the approved packet."
        authority = self.authority(request, packet)
        (packet / "plan.md").write_text(
            (packet / "plan.md").read_text() + "\nUnapproved protected change.\n"
        )
        self.assertEqual(
            "E_PACKET_CURRENT_STATE",
            self.code(lambda: work_authority.validate_current(
                authority, original_request=request, repository=self.repo
            )),
        )

    def test_lifecycle_status_is_bound_to_receipt_kind(self):
        packet = self.approved_packet()
        request = "Continue the approved packet."
        accepted = self.authority(request, packet, sequence=1)
        work_authority.validate_current(
            accepted, original_request=request, repository=self.repo, update_status="accepted"
        )
        self.assertEqual(
            "E_PACKET_STATUS",
            self.code(lambda: work_authority.validate_current(
                accepted, original_request=request, repository=self.repo, update_status="progress"
            )),
        )
        self.cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--authorization-evidence", "current session execution approval",
        )
        progress = self.authority(request, packet, sequence=2)
        work_authority.validate_current(
            progress, original_request=request, repository=self.repo, update_status="progress"
        )
        self.assertEqual(
            "E_PACKET_STATUS",
            self.code(lambda: work_authority.validate_current(
                progress, original_request=request, repository=self.repo, update_status="complete"
            )),
        )
        self.cli("transition", packet, *self.fence(packet), "--to", "verifying")
        complete = self.authority(request, packet, sequence=3)
        work_authority.validate_current(
            complete, original_request=request, repository=self.repo, update_status="complete"
        )

    def test_helper_transfer_receipt_is_current_and_stale_after_second_handoff(self):
        packet = self.approved_packet()
        first = self.cli(
            "handoff", packet, *self.fence(packet),
            "--to-coordinator-id", str(uuid.uuid4()), "--evidence", "orderly transfer",
        )["transfer_receipt"]
        result = work_authority.validate_transfer_current(first, self.repo)
        self.assertTrue(result["authoritative"])
        self.assertEqual("paused", result["status"])

        malformed = copy.deepcopy(first)
        malformed["unexpected"] = True
        self.assertEqual(
            "E_TRANSFER_RECEIPT_SCHEMA",
            self.code(lambda: work_authority.validate_transfer_current(malformed, self.repo)),
        )
        changed = copy.deepcopy(first)
        changed["receipt_sha256"] = "0" * 64
        self.assertEqual(
            "E_TRANSFER_RECEIPT_HASH",
            self.code(lambda: work_authority.validate_transfer_current(changed, self.repo)),
        )

        self.cli(
            "handoff", packet, *self.fence(packet),
            "--to-coordinator-id", str(uuid.uuid4()), "--evidence", "second orderly transfer",
        )
        self.assertEqual(
            "E_TRANSFER_RECEIPT_STALE",
            self.code(lambda: work_authority.validate_transfer_current(first, self.repo)),
        )

    def test_cancellation_after_handoff_requires_current_fencing(self):
        packet = self.approved_packet()
        request = "Cancel safely if ownership changes."
        self.cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--authorization-evidence", "current execution authority",
        )
        stale = self.authority(request, packet, sequence=2)
        self.cli(
            "handoff", packet, *self.fence(packet),
            "--to-coordinator-id", str(uuid.uuid4()), "--evidence", "orderly transfer",
        )
        self.assertEqual(
            "E_PACKET_FENCE_STALE",
            self.code(lambda: work_authority.validate_current(
                stale, original_request=request, repository=self.repo, update_status="failed"
            )),
        )
        self.cli(
            "transition", packet, *self.fence(packet), "--to", "executing",
            "--authorization-evidence", "new coordinator reauthorized",
        )
        self.cli("transition", packet, *self.fence(packet), "--to", "cancelled")
        current = self.authority(request, packet, sequence=3)
        work_authority.validate_current(
            current, original_request=request, repository=self.repo, update_status="cancelled"
        )


if __name__ == "__main__":
    unittest.main()
