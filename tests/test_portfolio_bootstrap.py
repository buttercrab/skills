from __future__ import annotations

import copy
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

from jsonschema import Draft202012Validator

import portfolio_receipts as receipts


ROOT = Path(__file__).resolve().parents[1]
PRESERVATION_PATH = ROOT / "skills" / "align-work" / "scripts" / "preservation_journal.py"
HERMETIC_RUNNER = ROOT / "tests" / "hermetic_run.sh"
AMBIENT_CAPTURE = ROOT / "tests" / "portfolio_ambient.py"
AGENT_HTTP = ROOT / "skills" / "agent-mail" / "scripts" / "real_postgres_http_test.sh"
AGENT_MCP = ROOT / "skills" / "agent-mail" / "scripts" / "real_postgres_mcp_test.sh"
HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64


def load_preservation_module():
    spec = importlib.util.spec_from_file_location("preservation_journal", PRESERVATION_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def common(receipt_type: str) -> dict:
    return {
        "receipt_type": receipt_type,
        "schema_version": 1,
        "receipt_id": str(uuid.uuid4()),
        "packet_id": str(uuid.uuid4()),
        "packet_revision": 1,
        "protected_digest": HASH_A,
        "repository_root": "/tmp/example-repository",
        "manifest_algorithm_version": receipts.MANIFEST_VERSION,
        "timestamp": "2026-07-14T00:00:00Z",
    }


def gate_c(trial_component: dict | None = None, evaluation_component: dict | None = None) -> dict:
    value = common("gate-approval/v1")
    value.update(
        {
            "gate_id": "C",
            "profile": "immutable-evaluation-snapshot",
            "artifact_manifest_digest": HASH_B,
            "approver_evidence": "approved exact Gate C components",
            "scope": ["routing-trials", "routing-evaluation"],
            "trial_component": trial_component
            or {"id": str(uuid.uuid4()), "digest": HASH_A},
            "evaluation_component": evaluation_component
            or {"id": str(uuid.uuid4()), "digest": HASH_B},
        }
    )
    return value


def run_binding(case_id: str = "case-a", run_ordinal: int = 1) -> dict:
    return {
        "case_id": case_id,
        "run_ordinal": run_ordinal,
        "prompt_digest": HASH_A,
        "output_schema_digest": HASH_B,
        "isolation_digest": HASH_C,
        "runner_digest": HASH_A,
        "runner_schema_version": "gate-c-isolated-codex-runner/v2",
        "command_policy_digest": HASH_B,
        "retry_policy_digest": HASH_C,
        "status_policy_digest": HASH_A,
        "tool_policy_digest": HASH_B,
        "data_policy_digest": HASH_C,
        "network_policy_digest": HASH_A,
        "mutation_policy_digest": HASH_B,
        "model": "test-model",
        "reasoning_effort": "high",
        "local_run_id": str(uuid.uuid4()),
        "provider_thread_id": str(uuid.uuid4()),
        "fresh_session_marker": str(uuid.uuid4()),
        "attempt_number": 1,
        "automatic_retry": False,
        "run_manifest_digest": HASH_C,
        "event_stream_digest": HASH_A,
        "raw_batch_output_hash": HASH_B,
        "raw_output_hash": HASH_C,
        "pre_state_digest": HASH_A,
        "post_state_digest": HASH_A,
    }


def trial_for(gate: dict, binding: dict | None = None) -> dict:
    value = common("trial-receipt/v1")
    for field in ("packet_id", "packet_revision", "protected_digest", "repository_root"):
        value[field] = gate[field]
    value.update(
        {
            "trial_component_id": gate["trial_component"]["id"],
            "trial_component_digest": gate["trial_component"]["digest"],
            "source_digest": HASH_A,
            "package_manifest_digest": HASH_B,
            "routing_case_digest": HASH_C,
            "trial_id": str(uuid.uuid4()),
            **(binding or run_binding()),
        }
    )
    return value


def evaluation_for(
    gate: dict,
    trial: dict,
    rubric_digest: str = HASH_C,
    binding: dict | None = None,
) -> dict:
    value = common("evaluation-receipt/v1")
    for field in ("packet_id", "packet_revision", "protected_digest", "repository_root"):
        value[field] = gate[field]
    value.update(
        {
            "evaluation_component_id": gate["evaluation_component"]["id"],
            "evaluation_component_digest": gate["evaluation_component"]["digest"],
            "trial_receipt_id": trial["receipt_id"],
            "trial_receipt_hash": receipts.digest_value(trial),
            "evaluator_id": str(uuid.uuid4()),
            "source_digest": HASH_A,
            **(binding or run_binding(trial["case_id"], trial["run_ordinal"])),
            "rubric_keys": ["outer-owner"],
            "rubric_digest": rubric_digest,
            "dispositions": [
                {"rubric_key": "outer-owner", "verdict": "pass", "evidence": "selected align-work"}
            ],
        }
    )
    return value


class ReceiptContractTests(unittest.TestCase):
    def test_schema_files_are_closed_strict_json(self):
        for path in sorted((ROOT / "tests" / "contracts").glob("*.schema.json")):
            with self.subTest(path=path.name):
                schema = json.loads(path.read_text())
                self.assertFalse(schema["additionalProperties"])
                self.assertEqual(schema["type"], "object")

    def test_trial_and_evaluation_fixtures_match_closed_schemas(self):
        gate = gate_c()
        trial = trial_for(gate)
        evaluation = evaluation_for(gate, trial)
        Draft202012Validator(json.loads((ROOT / "tests/contracts/trial-receipt-v1.schema.json").read_text())).validate(trial)
        Draft202012Validator(json.loads((ROOT / "tests/contracts/evaluation-receipt-v1.schema.json").read_text())).validate(evaluation)

    def test_run_binding_rejects_nonfresh_retry_mutation_and_identity_collision(self):
        gate = gate_c()
        trial = trial_for(gate)
        for field, value in (
            ("attempt_number", 2),
            ("automatic_retry", True),
            ("post_state_digest", HASH_B),
            ("provider_thread_id", trial["local_run_id"]),
        ):
            with self.subTest(field=field):
                changed = copy.deepcopy(trial)
                changed[field] = value
                with self.assertRaises(receipts.ContractError):
                    receipts.validate_trial(changed, gate=gate)

    def test_gate_profiles_are_disjoint(self):
        gate_a = common("gate-approval/v1")
        gate_a.update(
            {
                "gate_id": "A",
                "profile": "authorized-delta",
                "artifact_manifest_digest": HASH_A,
                "approver_evidence": "approved",
                "scope": ["routing-contract"],
                "authorized_delta_digest": HASH_B,
            }
        )
        receipts.validate_gate(gate_a)
        gate_b = common("gate-approval/v1")
        gate_b.update(
            {
                "gate_id": "B",
                "profile": "immutable-specification",
                "artifact_manifest_digest": HASH_A,
                "approver_evidence": "approved",
                "scope": ["history-specification"],
            }
        )
        receipts.validate_gate(gate_b)
        invalid_b = copy.deepcopy(gate_b)
        invalid_b["authorized_delta_digest"] = HASH_B
        with self.assertRaises(receipts.ContractError):
            receipts.validate_gate(invalid_b)
        invalid_a = copy.deepcopy(gate_a)
        del invalid_a["authorized_delta_digest"]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_gate(invalid_a)

    def test_trial_schema_rejects_evaluator_only_fields(self):
        gate = gate_c()
        trial = trial_for(gate)
        receipts.validate_trial(trial, gate=gate)
        for field, value in (
            ("rubric_digest", HASH_A),
            ("expected_answer", "align-work"),
            ("dispositions", []),
            ("evaluator_id", str(uuid.uuid4())),
            ("evaluation_component_id", gate["evaluation_component"]["id"]),
        ):
            with self.subTest(field=field):
                invalid = copy.deepcopy(trial)
                invalid[field] = value
                with self.assertRaises(receipts.ContractError):
                    receipts.validate_trial(invalid, gate=gate)

    def test_rubric_successor_reuses_immutable_trial(self):
        trial_component = {"id": str(uuid.uuid4()), "digest": HASH_A}
        gate_v1 = gate_c(trial_component=trial_component)
        trial = trial_for(gate_v1)
        evaluation_v1 = evaluation_for(gate_v1, trial)
        receipts.validate_trial(trial, gate=gate_v1)
        receipts.validate_evaluation(evaluation_v1, trial=trial, gate=gate_v1)

        gate_v2 = gate_c(
            trial_component=trial_component,
            evaluation_component={"id": str(uuid.uuid4()), "digest": HASH_C},
        )
        for field in ("packet_id", "packet_revision", "protected_digest", "repository_root"):
            gate_v2[field] = gate_v1[field]
        receipts.validate_trial(trial, gate=gate_v2)
        with self.assertRaises(receipts.ContractError):
            receipts.validate_evaluation(evaluation_v1, trial=trial, gate=gate_v2)
        evaluation_v2 = evaluation_for(gate_v2, trial, rubric_digest=HASH_A)
        receipts.validate_evaluation(evaluation_v2, trial=trial, gate=gate_v2)

    def test_changed_trial_component_invalidates_trial_and_evaluation(self):
        gate_v1 = gate_c()
        trial = trial_for(gate_v1)
        evaluation = evaluation_for(gate_v1, trial)
        gate_v2 = gate_c(
            trial_component={"id": str(uuid.uuid4()), "digest": HASH_C},
            evaluation_component=gate_v1["evaluation_component"],
        )
        for field in ("packet_id", "packet_revision", "protected_digest", "repository_root"):
            gate_v2[field] = gate_v1[field]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_trial(trial, gate=gate_v2)
        with self.assertRaises(receipts.ContractError):
            receipts.validate_evaluation(evaluation, trial=trial, gate=gate_v2)

    def test_trial_and_evaluation_input_bindings_reject_changed_inputs(self):
        gate = gate_c()
        trial = trial_for(gate)
        trial_inputs = {
            field: trial[field]
            for field in receipts.TRIAL_INPUT_FIELDS
        }
        receipts.validate_trial_inputs(trial, trial_inputs)
        for field in trial_inputs:
            with self.subTest(trial_field=field):
                changed = copy.deepcopy(trial_inputs)
                original = changed[field]
                if isinstance(original, bool):
                    changed[field] = not original
                elif isinstance(original, int):
                    changed[field] = 2 if original == 1 else 1
                elif field in receipts.RUN_UUID_FIELDS:
                    changed[field] = str(uuid.uuid4())
                elif isinstance(original, str) and len(original) == 64:
                    changed[field] = HASH_B if original != HASH_B else HASH_C
                else:
                    changed[field] = f"changed-{original}"
                with self.assertRaises(receipts.ContractError):
                    receipts.validate_trial_inputs(trial, changed)

        evaluation = evaluation_for(gate, trial)
        evaluation_inputs = {
            field: evaluation[field]
            for field in receipts.EVALUATION_INPUT_FIELDS
        }
        receipts.validate_evaluation_inputs(evaluation, evaluation_inputs)
        for field in evaluation_inputs:
            changed = copy.deepcopy(evaluation_inputs)
            original = changed[field]
            if isinstance(original, bool):
                changed[field] = not original
            elif isinstance(original, int):
                changed[field] = 2 if original == 1 else 1
            elif isinstance(original, list):
                changed[field] = ["other-key"]
            elif field in receipts.RUN_UUID_FIELDS:
                changed[field] = str(uuid.uuid4())
            elif isinstance(original, str) and len(original) == 64:
                changed[field] = HASH_B if original != HASH_B else HASH_C
            else:
                changed[field] = f"changed-{original}"
            with self.assertRaises(receipts.ContractError):
                receipts.validate_evaluation_inputs(evaluation, changed)
        receipts.validate_trial(trial, gate=gate)

    def test_receipt_batch_rejects_replay_crosswire_and_identity_collision(self):
        gate = gate_c()
        trials = []
        evaluations = []
        for ordinal in (1, 2, 3):
            trial_run = run_binding("case-a", ordinal)
            evaluation_run = run_binding("case-a", ordinal)
            for case_id in ("case-a", "case-b"):
                trial_binding = {**trial_run, "case_id": case_id, "raw_output_hash": HASH_A if case_id == "case-a" else HASH_B}
                trial = trial_for(gate, trial_binding)
                evaluation_binding = {
                    **evaluation_run,
                    "case_id": case_id,
                    "raw_output_hash": HASH_B if case_id == "case-a" else HASH_C,
                }
                trials.append(trial)
                evaluations.append(evaluation_for(gate, trial, binding=evaluation_binding))
        receipts.validate_receipt_batch(trials, evaluations, gate=gate)

        duplicate_trial = copy.deepcopy(trials[1])
        duplicate_trial["trial_id"] = trials[0]["trial_id"]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_receipt_batch(
                [trials[0], duplicate_trial, *trials[2:]], evaluations, gate=gate
            )

        reused_evaluator = copy.deepcopy(evaluations[1])
        reused_evaluator["evaluator_id"] = evaluations[0]["evaluator_id"]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_receipt_batch(
                trials, [evaluations[0], reused_evaluator, *evaluations[2:]], gate=gate
            )

        crosswired = copy.deepcopy(evaluations[0])
        crosswired["trial_receipt_id"] = trials[1]["receipt_id"]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_receipt_batch(
                trials, [crosswired, *evaluations[1:]], gate=gate
            )

        repeated_threads = copy.deepcopy(trials)
        for item in repeated_threads[2:4]:
            item["provider_thread_id"] = repeated_threads[0]["provider_thread_id"]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_receipt_batch(repeated_threads, evaluations, gate=gate)

        colliding_evaluator_threads = copy.deepcopy(evaluations)
        for item in colliding_evaluator_threads[:2]:
            item["provider_thread_id"] = trials[0]["provider_thread_id"]
        with self.assertRaises(receipts.ContractError):
            receipts.validate_receipt_batch(trials, colliding_evaluator_threads, gate=gate)

    def test_systematic_failure_aggregation_overrides_case_passes(self):
        records = []
        for case_id, family in (("one", "family-a"), ("two", "family-a"), ("three", "family-b")):
            for index in range(3):
                records.append(
                    {
                        "case_id": case_id,
                        "family": family,
                        "kind": "ordinary",
                        "trial_id": str(uuid.uuid4()),
                        "dispositions": [
                            {
                                "rubric_key": "outer-owner",
                                "verdict": "fail" if index == 0 else "pass",
                            }
                        ],
                    }
                )
        result = receipts.aggregate_routing_evaluations(records)
        self.assertEqual("fail", result["verdict"])
        self.assertEqual(["outer-owner"], result["systematic_failure_keys"])
        self.assertTrue(all(item["verdict"] == "pass" for item in result["case_results"]))

        boundary = [item for item in records if item["case_id"] != "three"]
        boundary_result = receipts.aggregate_routing_evaluations(boundary)
        self.assertEqual("pass", boundary_result["verdict"])
        self.assertEqual([], boundary_result["systematic_failure_keys"])

    def test_manifest_binds_file_and_symlink_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "file.txt").write_text("one")
            os.symlink("file.txt", root / "link")
            first = receipts.build_manifest(root, ["file.txt", "link", "absent"])
            (root / "file.txt").write_text("two")
            second = receipts.build_manifest(root, ["file.txt", "link", "absent"])
            self.assertNotEqual(receipts.digest_value(first), receipts.digest_value(second))

    def test_strict_loader_rejects_duplicate_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as temp:
            duplicate = Path(temp) / "duplicate.json"
            duplicate.write_text('{"a":1,"a":2}')
            with self.assertRaises(receipts.ContractError):
                receipts.strict_load(duplicate)
            nonfinite = Path(temp) / "nonfinite.json"
            nonfinite.write_text('{"a":NaN}')
            with self.assertRaises(receipts.ContractError):
                receipts.strict_load(nonfinite)


class PreservationJournalTests(unittest.TestCase):
    def setUp(self):
        self.module = load_preservation_module()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".planning" / "task").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_restore_regular_symlink_deleted_and_created_paths(self):
        (self.root / "regular.txt").write_text("before")
        (self.root / "delete.txt").write_text("restore me")
        os.symlink("regular.txt", self.root / "link")
        journal_path, _ = self.module.snapshot(
            str(self.root),
            str(self.root / ".planning" / "task"),
            "slice-1",
            ["regular.txt", "delete.txt", "link", "created.txt"],
        )
        (self.root / "regular.txt").write_text("after")
        (self.root / "delete.txt").unlink()
        (self.root / "link").unlink()
        os.symlink("delete.txt", self.root / "link")
        (self.root / "created.txt").write_text("new")
        self.module.record_post(journal_path, None)
        self.module.rollback(journal_path)
        self.assertEqual((self.root / "regular.txt").read_text(), "before")
        self.assertEqual((self.root / "delete.txt").read_text(), "restore me")
        self.assertEqual(os.readlink(self.root / "link"), "regular.txt")
        self.assertFalse((self.root / "created.txt").exists())

    def test_rename_rolls_back_when_destination_was_snapshotted_absent(self):
        (self.root / "old.txt").write_text("rename")
        journal_path, _ = self.module.snapshot(
            str(self.root),
            str(self.root / ".planning" / "task"),
            "slice-rename",
            ["old.txt", "new.txt"],
        )
        (self.root / "old.txt").rename(self.root / "new.txt")
        self.module.record_post(journal_path, None)
        self.module.rollback(journal_path)
        self.assertEqual((self.root / "old.txt").read_text(), "rename")
        self.assertFalse((self.root / "new.txt").exists())

    def test_concurrent_change_refuses_rollback(self):
        path = self.root / "file.txt"
        path.write_text("before")
        journal_path, _ = self.module.snapshot(
            str(self.root),
            str(self.root / ".planning" / "task"),
            "slice-drift",
            ["file.txt"],
        )
        path.write_text("owned postimage")
        self.module.record_post(journal_path, None)
        path.write_text("concurrent user edit")
        with self.assertRaises(self.module.JournalError):
            self.module.rollback(journal_path)
        self.assertEqual(path.read_text(), "concurrent user edit")

    def test_reconstruct_applied_binds_approved_candidate_and_preserves_source(self):
        source_file = self.root / "file.txt"
        source_file.write_text("before")
        source_journal, _ = self.module.snapshot(
            str(self.root), str(self.root / ".planning" / "task"), "historical", ["file.txt", "new.txt"]
        )
        source_hash = self.module.digest_file(source_journal)
        candidate_root = self.root / ".planning" / "task" / "gate-b" / "candidate"
        candidate_root.mkdir(parents=True)
        (candidate_root / "file.txt").write_text("approved after")
        (candidate_root / "new.txt").write_text("approved new")
        source_file.write_text("approved after")
        (self.root / "new.txt").write_text("approved new")
        paths = [
            source_journal.relative_to(self.root).as_posix(),
            (candidate_root / "file.txt").relative_to(self.root).as_posix(),
            (candidate_root / "new.txt").relative_to(self.root).as_posix(),
        ]
        manifest = receipts.build_manifest(self.root, paths)
        manifest_path = self.root / ".planning" / "task" / "approved-manifest.json"
        manifest_path.write_text(json.dumps({"digest": receipts.digest_value(manifest), "manifest": manifest}))

        recovered_path, recovered = self.module.reconstruct_applied(
            str(self.root),
            str(self.root / ".planning" / "task"),
            "recovered",
            str(source_journal),
            str(manifest_path),
            str(candidate_root),
        )
        self.assertEqual(self.module.digest_file(source_journal), source_hash)
        self.assertIsNotNone(recovered["post_recorded_at"])
        self.assertEqual(recovered["reconstructed_from"]["source_journal_sha256"], source_hash)
        self.module.rollback(recovered_path)
        self.assertEqual(source_file.read_text(), "before")
        self.assertFalse((self.root / "new.txt").exists())

    def test_reconstruct_applied_rejects_current_candidate_mismatch(self):
        source_file = self.root / "file.txt"
        source_file.write_text("before")
        source_journal, _ = self.module.snapshot(
            str(self.root), str(self.root / ".planning" / "task"), "historical", ["file.txt"]
        )
        candidate_root = self.root / ".planning" / "task" / "gate-b" / "candidate"
        candidate_root.mkdir(parents=True)
        (candidate_root / "file.txt").write_text("approved after")
        source_file.write_text("different current bytes")
        paths = [
            source_journal.relative_to(self.root).as_posix(),
            (candidate_root / "file.txt").relative_to(self.root).as_posix(),
        ]
        manifest = receipts.build_manifest(self.root, paths)
        manifest_path = self.root / ".planning" / "task" / "approved-manifest.json"
        manifest_path.write_text(json.dumps({"digest": receipts.digest_value(manifest), "manifest": manifest}))
        with self.assertRaises(self.module.JournalError):
            self.module.reconstruct_applied(
                str(self.root),
                str(self.root / ".planning" / "task"),
                "recovered",
                str(source_journal),
                str(manifest_path),
                str(candidate_root),
            )


class HermeticRunnerTests(unittest.TestCase):
    def run_hermetic(
        self,
        repo: Path,
        receipt: Path,
        command: list[str],
        network: str = "deny",
        runner_options: list[str] | None = None,
    ):
        run_root = receipt.parent / f"run-{uuid.uuid4()}"
        profile = receipt.parent / f"watch-profile-{uuid.uuid4()}.json"
        categories = sorted(receipts.REQUIRED_AMBIENT_CATEGORIES)
        profile.write_text(
            json.dumps(
                {
                    "schema_version": receipts.AMBIENT_PROFILE_VERSION,
                    "required_categories": categories,
                    "entries": [
                        {"category": category, "base": "absolute", "path": str(receipt.parent / f"watch-{category}")}
                        for category in categories
                    ],
                }
            )
        )
        result = subprocess.run(
            [
                str(HERMETIC_RUNNER),
                "--repo",
                str(repo),
                "--receipt",
                str(receipt),
                "--run-root",
                str(run_root),
                "--network",
                network,
                "--watch-profile",
                str(profile),
                *(runner_options or []),
                "--",
                *command,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        return result, run_root

    def test_runner_requires_watch_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            result = subprocess.run(
                [str(HERMETIC_RUNNER), "--repo", str(repo), "--receipt", str(base / "r.json"), "--", "/bin/true"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 64)

    def test_runner_allows_only_owned_run_root_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            (repo / "source.txt").write_text("stable")
            receipt = base / "receipt.json"
            result, run_root = self.run_hermetic(
                repo,
                receipt,
                ["/bin/bash", "-c", 'printf ok >"$RUN_ROOT/owned.txt"'],
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(run_root.exists())
            data = json.loads(receipt.read_text())
            self.assertEqual(data["verdict"], "passed")
            self.assertTrue(data["state_unchanged"])
            self.assertTrue(data["pre_state"]["watched"])
            self.assertRegex(data["watch_profile_digest"], r"^[0-9a-f]{64}$")
    def test_runner_denies_write_outside_run_root(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            outside = repo / "forbidden.txt"
            receipt = base / "receipt.json"
            result, _ = self.run_hermetic(
                repo,
                receipt,
                ["/bin/bash", "-c", f'printf unsafe >"{outside}"'],
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(outside.exists())
            data = json.loads(receipt.read_text())
            self.assertEqual(data["verdict"], "failed")
            self.assertTrue(data["state_unchanged"])

    def test_offline_unavailable_exit_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            receipt = base / "receipt.json"
            result, _ = self.run_hermetic(repo, receipt, ["/bin/bash", "-c", "exit 2"])
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(receipt.read_text())["verdict"], "incomplete")

    def test_local_cache_seed_is_copied_into_run_root(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            seed = base / "cargo-seed"
            seed.mkdir()
            (seed / "marker").write_text("local")
            receipt = base / "receipt.json"
            result, _ = self.run_hermetic(
                repo,
                receipt,
                ["/bin/bash", "-c", 'test "$(cat "$CARGO_HOME/marker")" = local'],
                runner_options=["--seed-cargo-home", str(seed)],
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_loopback_network_is_available_without_external_network(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            receipt = base / "receipt.json"
            program = (
                "import socket; "
                "server=socket.socket(); server.bind(('127.0.0.1',0)); server.listen(); "
                "client=socket.socket(); client.connect(server.getsockname()); "
                "peer,_=server.accept(); client.send(b'x'); "
                "assert peer.recv(1)==b'x'; peer.close(); client.close(); server.close()"
            )
            result, _ = self.run_hermetic(repo, receipt, ["python3", "-B", "-c", program], network="loopback")
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_agent_mail_scripts_require_runner_and_have_no_tmp_escape(self):
        for path in (AGENT_HTTP, AGENT_MCP):
            with self.subTest(path=path.name):
                text = path.read_text()
                self.assertIn("HERMETIC_RUN_ACTIVE", text)
                self.assertIn("$RUN_ROOT/agent-mail-", text)
                self.assertNotIn("mktemp -d /tmp/agent-mail", text)

    def test_agent_mail_failure_before_postgres_stays_hermetic(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            for script in (AGENT_HTTP, AGENT_MCP):
                with self.subTest(script=script.name):
                    receipt = base / f"{script.stem}-before.json"
                    result, run_root = self.run_hermetic(
                        ROOT,
                        receipt,
                        [
                            "/usr/bin/env",
                            "AGENT_MAIL_TEST_FAIL_AT=before-postgres",
                            "/bin/bash",
                            str(script),
                        ],
                        network="loopback",
                    )
                    self.assertEqual(result.returncode, 97, result.stderr)
                    self.assertFalse(run_root.exists())
                    data = json.loads(receipt.read_text())
                    self.assertEqual(data["verdict"], "failed")
                    self.assertTrue(data["state_unchanged"])
                    self.assertLessEqual(len(data["failure_summary"]), 4096)

    @unittest.skipUnless(shutil.which("pg_config") or shutil.which("initdb"), "PostgreSQL tools unavailable")
    def test_agent_mail_failure_after_postgres_stays_hermetic(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            for script in (AGENT_HTTP, AGENT_MCP):
                with self.subTest(script=script.name):
                    receipt = base / f"{script.stem}-after.json"
                    result, run_root = self.run_hermetic(
                        ROOT,
                        receipt,
                        [
                            "/usr/bin/env",
                            "AGENT_MAIL_TEST_FAIL_AT=after-postgres",
                            "/bin/bash",
                            str(script),
                        ],
                        network="loopback",
                    )
                    self.assertEqual(result.returncode, 98, result.stderr)
                    self.assertFalse(run_root.exists())
                    data = json.loads(receipt.read_text())
                    self.assertEqual(data["verdict"], "failed")
                    self.assertTrue(data["state_unchanged"])


class AmbientBaselineTests(unittest.TestCase):
    def test_capture_rejects_symlink_repository_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            repo.mkdir()
            linked_repo = root / "linked-repo"
            os.symlink(repo, linked_repo)
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(AMBIENT_CAPTURE),
                    "capture",
                    "--repo",
                    str(linked_repo),
                    "--agent-root",
                    str(root / "agents"),
                    "--codex-root",
                    str(root / "codex"),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 3)
            self.assertIn("repository root must be a real directory", result.stderr)

    def test_capture_and_validate_detects_link_or_pyc_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            (repo / "tests").mkdir(parents=True)
            (repo / "skills" / "one").mkdir(parents=True)
            (repo / "scripts" / "__pycache__").mkdir(parents=True)
            (repo / "tests" / "portfolio-routing-v1.json").write_text(
                json.dumps({"portfolio_skills": ["one"]})
            )
            pyc = repo / "scripts" / "__pycache__" / "one.pyc"
            pyc.write_bytes(b"stable")
            agent_root = root / "agents"
            codex_root = root / "codex"
            agent_root.mkdir()
            codex_root.mkdir()
            os.symlink(repo / "skills" / "one", agent_root / "one")
            os.symlink(repo / "skills" / "one", codex_root / "one")
            manifest = root / "ambient.json"
            command = [
                sys.executable,
                "-B",
                str(AMBIENT_CAPTURE),
                "capture",
                "--repo",
                str(repo),
                "--agent-root",
                str(agent_root),
                "--codex-root",
                str(codex_root),
            ]
            captured = subprocess.run(command, text=True, capture_output=True, check=True)
            manifest.write_text(captured.stdout)
            validation = command.copy()
            validation[3] = "validate"
            validation.extend(["--manifest", str(manifest)])
            valid = subprocess.run(validation, text=True, capture_output=True, check=False)
            self.assertEqual(valid.returncode, 0, valid.stderr)
            pyc.write_bytes(b"drift")
            invalid = subprocess.run(validation, text=True, capture_output=True, check=False)
            self.assertEqual(invalid.returncode, 3)


if __name__ == "__main__":
    unittest.main()
