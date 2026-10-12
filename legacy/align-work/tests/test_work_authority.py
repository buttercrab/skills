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

    def approved_packet(
        self,
        task="sample-task",
        *,
        legacy=False,
        packet_schema_version=3,
        legacy_authority="R,T",
    ):
        initialized = self.cli(
            "init", "--repo", self.repo, "--task-id", task,
            "--title", "Sample task", "--coordinator-id", self.coordinator,
        )
        packet = Path(initialized["packet"])
        if legacy or packet_schema_version == 2:
            state = self.state(packet)
            state["schema_version"] = 1 if legacy else 2
            if legacy:
                state["requested_authority_classes"] = []
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
        for name in ("alignment.md", "facts.md", "decisions.md", "plan.md"):
            path = packet / name
            if path.exists():
                path.write_text(path.read_text().replace("<!-- align-work-required-content -->", "Authored fixture content."))
        self.cli("transition", packet, *self.fence(packet), "--to", "drafting")
        if legacy:
            self.cli(
                "seal", packet, *self.fence(packet), "--status", "awaiting_approval",
                "--authority", legacy_authority,
            )
            self.cli(
                "transition", packet, *self.fence(packet), "--to", "approved",
                "--approval-id", str(uuid.uuid4()), "--authority", legacy_authority,
                "--approval-evidence", "current user approved exact digest",
            )
        else:
            self.cli("seal", packet, *self.fence(packet), "--status", "awaiting_approval")
            self.cli(
                "transition", packet, *self.fence(packet), "--to", "approved",
                "--approval-id", str(uuid.uuid4()),
                "--approval-evidence", "current user approved exact digest",
            )
        return packet

    def authority(self, request, packet=None, *, mode="packet", sequence=0, classification="existing-packet"):
        binding = None
        schema_version = "work_authority/v2"
        if packet is not None:
            state = self.state(packet)
            binding = work_authority.binding_from_state(self.repo, packet, state)
            schema_version = work_authority.work_schema_from_state(state)
        return {
            "schema_version": schema_version,
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
        binding = work_authority.binding_from_state(self.repo, packet, self.state(packet))
        self.assertEqual(3, binding["packet_schema_version"])
        self.assertNotIn("authority_classes", binding)

        other = (Path(self.temp.name) / "other").resolve()
        other.mkdir()
        plain = {
            "schema_version": "work_authority/v2",
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

    def test_legacy_packet_protocol_remains_isolated_and_valid(self):
        request = "Continue the approved legacy packet."
        packet = self.approved_packet("legacy-task", legacy=True)
        authority = self.authority(request, packet)
        self.assertEqual("work_authority/v1", authority["schema_version"])
        self.assertEqual(["R", "T"], authority["packet_binding"]["authority_classes"])
        self.assertNotIn("packet_schema_version", authority["packet_binding"])
        result = work_authority.validate_current(
            authority, original_request=request, repository=self.repo
        )
        self.assertEqual("packet", result["alignment_mode"])

    def test_legacy_packet_protocol_accepts_full_historical_authority_domain(self):
        request = "Continue the approved legacy packet."
        packet = self.approved_packet(
            "legacy-full-domain",
            legacy=True,
            legacy_authority="D2,E,G7,I,P,R,T10",
        )
        authority = self.authority(request, packet)
        self.assertEqual(
            ["D2", "E", "G7", "I", "P", "R", "T10"],
            authority["packet_binding"]["authority_classes"],
        )
        result = work_authority.validate_current(
            authority, original_request=request, repository=self.repo
        )
        self.assertEqual("packet", result["alignment_mode"])

    def test_current_protocol_remains_valid_for_packet_schema_v2(self):
        request = "Continue the approved schema-v2 packet."
        packet = self.approved_packet("v2-task", packet_schema_version=2)
        authority = self.authority(request, packet)
        self.assertEqual("work_authority/v2", authority["schema_version"])
        self.assertEqual(2, authority["packet_binding"]["packet_schema_version"])
        result = work_authority.validate_current(
            authority, original_request=request, repository=self.repo
        )
        self.assertEqual("packet", result["alignment_mode"])

    def test_current_and_legacy_protocol_shapes_cannot_be_mixed(self):
        request = "Continue the approved packet."
        current = self.approved_packet("current-task")
        current_authority = self.authority(request, current)
        changed = copy.deepcopy(current_authority)
        changed["schema_version"] = "work_authority/v1"
        self.assertEqual(
            "E_SCHEMA",
            self.code(lambda: work_authority.validate_current(changed, original_request=request, repository=self.repo)),
        )

        legacy = self.approved_packet("legacy-mixed", legacy=True)
        legacy_authority = self.authority(request, legacy)
        changed = copy.deepcopy(legacy_authority)
        changed["schema_version"] = "work_authority/v2"
        self.assertEqual(
            "E_SCHEMA",
            self.code(lambda: work_authority.validate_current(changed, original_request=request, repository=self.repo)),
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

    def test_clear_or_negated_plan_language_does_not_force_align(self):
        requests = (
            "Refactor the architecture to the specified modular design without changing scope.",
            "Do not change scope or acceptance criteria; implement the supplied patch.",
            "Fix the permission error in the local test fixture.",
        )
        for request in requests:
            with self.subTest(request=request):
                none = self.authority(request, None, mode="none", classification="none")
                result = work_authority.validate_current(
                    none, original_request=request, repository=self.repo
                )
                self.assertEqual("none", result["alignment_mode"])

    def test_explicit_unresolved_choice_still_forces_align(self):
        request = "We need your decision: choose between strict and permissive validation."
        none = self.authority(request, None, mode="none", classification="none")
        self.assertEqual(
            "E_ALIGNMENT_DISAGREEMENT",
            self.code(lambda: work_authority.validate_current(
                none, original_request=request, repository=self.repo
            )),
        )

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
        (packet / "alignment.md").write_text(
            (packet / "alignment.md").read_text() + "\nUnapproved alignment change.\n"
        )
        self.assertEqual(
            "E_PACKET_CURRENT_STATE",
            self.code(lambda: work_authority.validate_current(
                authority, original_request=request, repository=self.repo
            )),
        )

    def test_mutable_plan_change_preserves_approved_authority(self):
        packet = self.approved_packet()
        request = "Continue the approved packet."
        (packet / "plan.md").write_text(
            (packet / "plan.md").read_text() + "\nAgent-owned plan revision.\n"
        )
        authority = self.authority(request, packet)
        result = work_authority.validate_current(
            authority, original_request=request, repository=self.repo
        )
        self.assertEqual("packet", result["alignment_mode"])

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

    def test_alignment_needed_state_cannot_be_bound_as_work_authority(self):
        packet = self.approved_packet()
        request = "Continue the approved packet."
        self.cli("transition", packet, *self.fence(packet), "--to", "needs_alignment")
        self.assertEqual(
            "E_PACKET_CURRENT_STATE",
            self.code(lambda: work_authority.binding_from_state(
                self.repo, packet, self.state(packet)
            )),
        )
        forged = {
            "schema_version": "work_authority/v2",
            "work_id": str(uuid.uuid4()),
            "sequence": 1,
            "original_request_sha256": hashlib.sha256(request.encode()).hexdigest(),
            "alignment_mode": "packet",
            "gateway_classification": "existing-packet",
            "repository_root": str(self.repo),
            "packet_binding": {
                "packet_schema_version": 3,
                "packet_id": self.state(packet)["packet_id"],
                "task_id": packet.name,
                "packet_path": f".planning/{packet.name}",
                "packet_revision": self.state(packet)["packet_revision"],
                "protected_digest": self.state(packet)["protected_digest"],
                "approval_id": str(uuid.uuid4()),
                "coordinator_id": self.state(packet)["active_coordinator"]["id"],
                "coordinator_epoch": self.state(packet)["active_coordinator"]["epoch"],
                "state_generation": self.state(packet)["state_generation"],
                "lifecycle_status": "needs_alignment",
                "execution_head": self.state(packet)["execution_head"],
            },
        }
        self.assertEqual(
            "E_PACKET_STATUS",
            self.code(lambda: work_authority.validate_current(
                forged,
                original_request=request,
                repository=self.repo,
                update_status="failed",
            )),
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
