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
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/validation"))
import state_manifest as receipts
PRESERVATION_PATH = ROOT / "legacy/align-work/scripts/preservation_journal.py"
HERMETIC_RUNNER = ROOT / "tools/validation/hermetic_run.sh"
AMBIENT_CAPTURE = ROOT / "tools/validation/ambient_baseline.py"
AGENT_HTTP = ROOT / "integrations/agent-mail/scripts/real_postgres_http_test.sh"
AGENT_MCP = ROOT / "integrations/agent-mail/scripts/real_postgres_mcp_test.sh"

def load_preservation_module():
    spec = importlib.util.spec_from_file_location("preservation_journal", PRESERVATION_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StateManifestTests(unittest.TestCase):
    def test_manifest_binds_file_and_symlink_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "file").write_text("before")
            os.symlink("file", root / "link")
            first = receipts.build_manifest(root, ["file", "link", "absent"])
            (root / "file").write_text("after")
            self.assertNotEqual(receipts.digest_value(first), receipts.digest_value(receipts.build_manifest(root, ["file", "link", "absent"])))
            os.unlink(root / "link")
            os.symlink("absent", root / "link")
            second = receipts.build_manifest(root, ["file", "link", "absent"])
            self.assertNotEqual(first["entries"], second["entries"])

    def test_strict_json_rejects_duplicates_and_nonfinite_numbers(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "value.json"
            for value in ('{"a":1,"a":2}', '{"a":NaN}'):
                path.write_text(value)
                with self.assertRaises(receipts.ContractError):
                    receipts.strict_load(path)

    def test_manifest_rejects_parent_symlink_and_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "real").mkdir()
            os.symlink("real", root / "link")
            for value in ("link/file", "../outside"):
                with self.assertRaises(receipts.ContractError):
                    receipts.build_manifest(root, [value])


class PreservationJournalTests(unittest.TestCase):
    def setUp(self):
        self.module = load_preservation_module()
        self.temp = tempfile.TemporaryDirectory()
        # macOS exposes /var through /private/var. The preservation helper
        # canonicalizes repository roots, so keep the fixture root canonical too.
        self.root = Path(self.temp.name).resolve()
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
        self.module.record_post(self.root, self.root / ".planning" / "task", journal_path, None)
        self.module.rollback(self.root, self.root / ".planning" / "task", journal_path)
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
        self.module.record_post(self.root, self.root / ".planning" / "task", journal_path, None)
        self.module.rollback(self.root, self.root / ".planning" / "task", journal_path)
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
        self.module.record_post(self.root, self.root / ".planning" / "task", journal_path, None)
        path.write_text("concurrent user edit")
        with self.assertRaises(self.module.JournalError):
            self.module.rollback(self.root, self.root / ".planning" / "task", journal_path)
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
        self.module.rollback(self.root, self.root / ".planning" / "task", recovered_path)
        self.assertEqual(source_file.read_text(), "before")
        self.assertFalse((self.root / "new.txt").exists())

    def test_record_and_rollback_reject_journal_outside_authorized_packet(self):
        target = self.root / "important.txt"
        target.write_text("must survive")
        forged = self.root / "forged.json"
        forged.write_text(json.dumps({
            "schema_version": self.module.SCHEMA_VERSION,
            "slice_id": "forged",
            "repository_root": str(self.root),
            "created_at": self.module.now(),
            "entries": [{
                "path": "important.txt",
                "preimage": {"type": "absent"},
                "postimage": self.module.path_state(self.root, "important.txt"),
            }],
            "post_recorded_at": self.module.now(),
            "patch_sha256": None,
        }))
        packet = self.root / ".planning" / "task"
        with self.assertRaises(self.module.JournalError):
            self.module.rollback(self.root, packet, forged)
        self.assertEqual(target.read_text(), "must survive")

    def test_journal_cannot_be_reused_under_a_different_packet(self):
        target = self.root / "file.txt"
        target.write_text("before")
        packet = self.root / ".planning" / "task"
        journal_path, _ = self.module.snapshot(
            str(self.root), str(packet), "bound-slice", ["file.txt"]
        )
        target.write_text("after")
        self.module.record_post(self.root, packet, journal_path, None)
        other = self.root / ".planning" / "other"
        other.mkdir()
        with self.assertRaises(self.module.JournalError):
            self.module.rollback(self.root, other, journal_path)
        self.assertEqual(target.read_text(), "after")

    def test_corrupt_later_backup_fails_before_any_rollback_mutation(self):
        first = self.root / "a.txt"
        second = self.root / "b.txt"
        first.write_text("first before")
        second.write_text("second before")
        packet = self.root / ".planning" / "task"
        journal_path, journal = self.module.snapshot(
            str(self.root), str(packet), "preflight-all", ["a.txt", "b.txt"]
        )
        first.write_text("first after")
        second.write_text("second after")
        self.module.record_post(self.root, packet, journal_path, None)
        second_entry = next(entry for entry in journal["entries"] if entry["path"] == "b.txt")
        (journal_path.parent / second_entry["backup"]).write_text("corrupt")
        with self.assertRaises(self.module.JournalError):
            self.module.rollback(self.root, packet, journal_path)
        self.assertEqual(first.read_text(), "first after")
        self.assertEqual(second.read_text(), "second after")

    def test_journal_loader_rejects_duplicate_keys_and_unknown_fields(self):
        packet = self.root / ".planning" / "task"
        private = packet / "private-preimages" / "strict"
        private.mkdir(parents=True)
        journal_path = private / "journal.json"
        journal_path.write_text(
            '{"schema_version":"align-preservation-journal/v1",'
            '"schema_version":"align-preservation-journal/v1"}'
        )
        with self.assertRaises(self.module.JournalError):
            self.module.authorized_journal(self.root, packet, journal_path)

        journal_path.write_text(json.dumps({
            "schema_version": self.module.SCHEMA_VERSION,
            "slice_id": "strict",
            "repository_root": str(self.root),
            "created_at": self.module.now(),
            "entries": [{"path": "file.txt", "preimage": {"type": "absent"}}],
            "post_recorded_at": None,
            "patch_sha256": None,
            "unexpected": True,
        }))
        with self.assertRaises(self.module.JournalError):
            self.module.authorized_journal(self.root, packet, journal_path)

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
    def setUp(self):
        if self._testMethodName.startswith("test_runner_requires") or self._testMethodName.startswith("test_agent_mail_scripts"):
            return
        if not shutil.which("sandbox-exec"):
            self.skipTest("technical isolation unavailable: sandbox-exec missing")
        probe = subprocess.run(["sandbox-exec", "-p", "(version 1)(allow default)", "/usr/bin/true"], capture_output=True)
        if probe.returncode:
            self.skipTest("sandbox-exec unavailable: " + probe.stderr.decode(errors="replace").strip())

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

    def test_deny_network_blocks_loopback_bind(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            receipt = base / "receipt.json"
            program = "import socket; s=socket.socket(); s.bind(('127.0.0.1',0))"
            result, _ = self.run_hermetic(repo, receipt, ["python3", "-B", "-c", program])
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(receipt.read_text())["verdict"], "failed")

    def test_loopback_policy_denies_external_connection(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "repo"
            repo.mkdir()
            receipt = base / "receipt.json"
            program = "import socket\ns=socket.socket(); s.settimeout(0.25)\ntry: s.connect(('192.0.2.1',80))\nexcept OSError as e: assert e.errno == 1, repr(e)\nelse: raise AssertionError('external networking allowed')"
            result, _ = self.run_hermetic(repo, receipt, ["python3", "-B", "-c", program], network="loopback")
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
            repo = base / "repo"
            repo.mkdir()
            for script in (AGENT_HTTP, AGENT_MCP):
                with self.subTest(script=script.name):
                    receipt = base / f"{script.stem}-before.json"
                    result, run_root = self.run_hermetic(
                        repo,
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
            repo = base / "repo"
            repo.mkdir()
            for script in (AGENT_HTTP, AGENT_MCP):
                with self.subTest(script=script.name):
                    receipt = base / f"{script.stem}-after.json"
                    result, run_root = self.run_hermetic(
                        repo,
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
            (repo / "skills" / "one" / "SKILL.md").write_text("fixture")
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
