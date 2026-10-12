from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts" / "install_skills.py"
CATALOG = sorted(
    path.name
    for path in (ROOT / "skills").iterdir()
    if path.is_dir() and (path / "SKILL.md").is_file()
)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-installer-")
        self.root = Path(self.temp.name).resolve()

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self, name: str = "fixture"):
        base = self.root / name
        home = base / "home"
        temporary = base / "tmp"
        state = base / "state"
        agent = base / "agent"
        codex = base / "codex"
        for path in (home, temporary):
            path.mkdir(parents=True)
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(home),
                "TMPDIR": str(temporary),
                "SKILLS_INSTALL_STATE_DIR": str(state),
                "AGENT_SKILLS_DIR": str(agent),
                "CODEX_SKILLS_DIR": str(codex),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        return environment, agent, codex, state

    def run_installer(self, arguments=(), *, environment=None, expected=0):
        result = subprocess.run(
            [sys.executable, "-B", str(HELPER), "--repo", str(ROOT), *arguments],
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stderr or result.stdout)
        return result

    def remove_go(self, environment: dict):
        binary = Path(environment["HOME"]) / "empty-bin"
        binary.mkdir()
        environment["PATH"] = str(binary)

    def assert_link(self, directory: Path, name: str):
        target = directory / name
        self.assertTrue(target.is_symlink(), target)
        self.assertEqual(str((ROOT / "skills" / name).resolve()), os.readlink(target))

    def original_links(self, agent: Path, codex: Path):
        for directory in (agent, codex):
            directory.mkdir(parents=True, exist_ok=True)
            os.symlink("/original/audit-technical-work", directory / "audit-technical-work")

    def assert_original_links(self, agent: Path, codex: Path):
        for directory in (agent, codex):
            target = directory / "audit-technical-work"
            self.assertTrue(target.is_symlink())
            self.assertEqual("/original/audit-technical-work", os.readlink(target))

    def test_list_and_closed_selection(self):
        result = self.run_installer(["--list"])
        self.assertEqual(CATALOG, result.stdout.splitlines())

        environment, agent, codex, _ = self.fixture("selection")
        self.run_installer(
            ["--only", "audit-technical-work,write-task-handoff", "--exclude", "write-task-handoff"],
            environment=environment,
        )
        self.assert_link(agent, "audit-technical-work")
        self.assert_link(codex, "audit-technical-work")
        self.assertFalse((agent / "write-task-handoff").exists())

        invalid, *_ = self.fixture("invalid")
        result = self.run_installer(["--only", "unknown-skill"], environment=invalid, expected=1)
        self.assertIn("unknown skill", result.stderr)

    def test_no_go_dependency_and_default_install_all(self):
        environment, agent, codex, _ = self.fixture("no-go-default")
        self.remove_go(environment)
        result = self.run_installer(environment=environment)
        self.assertNotIn("Go", result.stderr)
        for name in CATALOG:
            self.assert_link(agent, name)
            self.assert_link(codex, name)

        excluded, excluded_agent, excluded_codex, _ = self.fixture("excluded")
        self.remove_go(excluded)
        self.run_installer(["--exclude", "responsive-coordinator"], environment=excluded)
        self.assertFalse((excluded_agent / "responsive-coordinator").exists())
        self.assertFalse((excluded_codex / "responsive-coordinator").exists())
        for directory in (excluded_agent, excluded_codex):
            self.assert_link(directory, "audit-technical-work")

    def test_nonlink_and_symlink_parent_fail_before_other_target_mutation(self):
        environment, agent, codex, state = self.fixture("hostile")
        agent.mkdir()
        (agent / "audit-technical-work").write_text("user owned")
        result = self.run_installer(["--only", "audit-technical-work"], environment=environment, expected=1)
        self.assertIn("non-link target", result.stderr)
        self.assertEqual("user owned", (agent / "audit-technical-work").read_text())
        self.assertFalse(codex.exists())
        self.assertFalse((state / "journal.json").exists())

        linked_env, linked_agent, linked_codex, _ = self.fixture("symlink-parent")
        real = self.root / "symlink-parent" / "real"
        real.mkdir()
        parent = self.root / "symlink-parent" / "linked"
        parent.symlink_to(real, target_is_directory=True)
        linked_env["AGENT_SKILLS_DIR"] = str(parent / "skills")
        result = self.run_installer(["--only", "audit-technical-work"], environment=linked_env, expected=1)
        self.assertIn("symlink component", result.stderr)
        self.assertFalse(linked_codex.exists())
        self.assertFalse(linked_agent.exists())

    def test_hostile_target_types_are_never_replaced(self):
        for kind in ("directory", "fifo"):
            with self.subTest(kind=kind):
                environment, agent, codex, state = self.fixture(f"hostile-{kind}")
                agent.mkdir()
                target = agent / "audit-technical-work"
                if kind == "directory":
                    target.mkdir()
                else:
                    os.mkfifo(target)
                result = self.run_installer(
                    ["--only", "audit-technical-work"], environment=environment, expected=1
                )
                self.assertIn("non-link target", result.stderr)
                self.assertTrue(target.exists())
                self.assertFalse(codex.exists())
                self.assertFalse((state / "journal.json").exists())

    def test_all_target_lock_rejects_concurrent_invocation(self):
        environment, agent, codex, state = self.fixture("concurrent")
        first_env = environment.copy()
        first_env["SKILLS_INSTALL_HOLD_LOCK_SECONDS"] = "2"
        process = subprocess.Popen(
            [sys.executable, "-B", str(HELPER), "--repo", str(ROOT), "--only", "audit-technical-work"],
            cwd=ROOT,
            env=first_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        deadline = time.time() + 2
        while not (state / "lock").exists() and time.time() < deadline:
            time.sleep(0.01)
        time.sleep(0.05)
        second = self.run_installer(
            ["--only", "audit-technical-work"], environment=environment, expected=1
        )
        self.assertIn("all-target lock", second.stderr)
        stdout, stderr = process.communicate(timeout=5)
        self.assertEqual(0, process.returncode, stderr or stdout)
        self.assert_link(agent, "audit-technical-work")
        self.assert_link(codex, "audit-technical-work")

    def test_backup_collision_refuses_before_mutation(self):
        environment, agent, codex, state = self.fixture("collision")
        self.original_links(agent, codex)
        (agent / ".skills-install-backup-fixed").mkdir()
        environment["SKILLS_INSTALL_TXID"] = "fixed"
        result = self.run_installer(["--only", "audit-technical-work"], environment=environment, expected=1)
        self.assertIn("backup collision", result.stderr)
        self.assert_original_links(agent, codex)
        self.assertFalse((state / "journal.json").exists())

    def test_replaced_links_keep_same_filesystem_backups(self):
        environment, agent, codex, state = self.fixture("retained-backups")
        self.original_links(agent, codex)
        environment["SKILLS_INSTALL_TXID"] = "retained"
        result = self.run_installer(
            ["--only", "audit-technical-work"], environment=environment
        )
        self.assertIn("Retained same-filesystem backup", result.stdout)
        for directory in (agent, codex):
            self.assert_link(directory, "audit-technical-work")
            backup_root = directory / ".skills-install-backup-retained"
            backup = backup_root / "audit-technical-work"
            self.assertTrue(backup.is_symlink())
            self.assertEqual("/original/audit-technical-work", os.readlink(backup))
            self.assertEqual(directory.stat().st_dev, backup_root.stat().st_dev)
        self.assertFalse((state / "journal.json").exists())

    def test_handled_failures_rollback_every_mutation_boundary(self):
        boundaries = [
            "after-journal",
            "after-backup-dir:1",
            "after-backup-dir:2",
            "after-backup:1",
            "after-link:1",
            "after-backup:2",
            "after-link:2",
            "before-cleanup",
        ]
        for number, boundary in enumerate(boundaries):
            with self.subTest(boundary=boundary):
                environment, agent, codex, state = self.fixture(f"failure-{number}")
                self.original_links(agent, codex)
                environment.update(
                    {
                        "SKILLS_INSTALL_TXID": f"failure-{number}",
                        "SKILLS_INSTALL_FAIL_AT": boundary,
                    }
                )
                result = self.run_installer(
                    ["--only", "audit-technical-work"], environment=environment, expected=1
                )
                self.assertIn("rollback completed", result.stderr)
                self.assert_original_links(agent, codex)
                self.assertFalse((state / "journal.json").exists())
                archives = list(state.glob("failed-*.json"))
                self.assertEqual(1, len(archives))
                data = json.loads(archives[0].read_text())
                self.assertEqual("skills-install-transaction/v2", data["schema_version"])

    def test_missing_target_directory_boundaries_rollback(self):
        for number, boundary in enumerate(("after-target-dir:1", "after-target-dir:2")):
            with self.subTest(boundary=boundary):
                environment, agent, codex, state = self.fixture(f"target-dir-{number}")
                environment.update(
                    {
                        "SKILLS_INSTALL_TXID": f"target-dir-{number}",
                        "SKILLS_INSTALL_FAIL_AT": boundary,
                    }
                )
                result = self.run_installer(
                    ["--only", "audit-technical-work"], environment=environment, expected=1
                )
                self.assertIn("rollback completed", result.stderr)
                self.assertFalse(agent.exists())
                self.assertFalse(codex.exists())
                self.assertFalse((state / "journal.json").exists())

    def test_crash_recovery_at_each_operation_boundary(self):
        boundaries = [
            "after-journal",
            "after-target-dir:1",
            "after-target-dir:2",
            "after-backup-dir:1",
            "after-backup-dir:2",
            "after-backup:1",
            "after-link:1",
            "after-backup:2",
            "after-link:2",
            "before-cleanup",
        ]
        for number, boundary in enumerate(boundaries):
            with self.subTest(boundary=boundary):
                environment, agent, codex, state = self.fixture(f"crash-{number}")
                if not boundary.startswith("after-target-dir"):
                    self.original_links(agent, codex)
                txid = f"crash-{number}"
                crashed = environment.copy()
                crashed.update(
                    {"SKILLS_INSTALL_TXID": txid, "SKILLS_INSTALL_CRASH_AT": boundary}
                )
                self.run_installer(
                    ["--only", "audit-technical-work"], environment=crashed, expected=97
                )
                self.assertTrue((state / "journal.json").is_file())
                recovered = environment.copy()
                recovered["SKILLS_INSTALL_TXID"] = txid
                result = self.run_installer(
                    ["--only", "audit-technical-work"], environment=recovered
                )
                self.assertIn("Recovered interrupted installer transaction", result.stdout)
                self.assert_link(agent, "audit-technical-work")
                self.assert_link(codex, "audit-technical-work")
                self.assertTrue((state / f"recovered-{txid}.json").is_file())
                self.assertFalse((state / "journal.json").exists())

    def test_failed_rollback_preserves_journal_then_recovers(self):
        environment, agent, codex, state = self.fixture("rollback-failure")
        self.original_links(agent, codex)
        failed = environment.copy()
        failed.update(
            {
                "SKILLS_INSTALL_TXID": "rollback-failure",
                "SKILLS_INSTALL_FAIL_AT": "after-link:1",
                "SKILLS_INSTALL_FAIL_ROLLBACK_AT": "1",
            }
        )
        result = self.run_installer(["--only", "audit-technical-work"], environment=failed, expected=1)
        self.assertIn("rollback failed", result.stderr)
        self.assertTrue((state / "journal.json").is_file())

        recovered = environment.copy()
        recovered["SKILLS_INSTALL_TXID"] = "reinstall-after-recovery"
        result = self.run_installer(["--only", "audit-technical-work"], environment=recovered)
        self.assertIn("Recovered interrupted installer transaction", result.stdout)
        self.assert_link(agent, "audit-technical-work")
        self.assert_link(codex, "audit-technical-work")
        self.assertFalse((state / "journal.json").exists())

    def test_signal_after_first_link_rolls_back(self):
        environment, agent, codex, state = self.fixture("signal")
        self.original_links(agent, codex)
        environment.update(
            {
                "SKILLS_INSTALL_TXID": "signal",
                "SKILLS_INSTALL_HOLD_AT": "after-link:1",
                "SKILLS_INSTALL_HOLD_SECONDS": "10",
            }
        )
        process = subprocess.Popen(
            [sys.executable, "-B", str(HELPER), "--repo", str(ROOT), "--only", "audit-technical-work"],
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        desired = str((ROOT / "skills" / "audit-technical-work").resolve())
        deadline = time.time() + 5
        while time.time() < deadline:
            if (agent / "audit-technical-work").is_symlink() and os.readlink(agent / "audit-technical-work") == desired:
                break
            time.sleep(0.01)
        else:
            process.kill()
            self.fail("installer did not reach the held mutation boundary")
        process.send_signal(signal.SIGTERM)
        stdout, stderr = process.communicate(timeout=5)
        self.assertEqual(1, process.returncode, stderr or stdout)
        self.assertIn("rollback completed", stderr)
        self.assert_original_links(agent, codex)
        self.assertFalse((state / "journal.json").exists())

    def retired_links(self, agent, codex, name="align-work"):
        for directory in (agent, codex):
            directory.mkdir(parents=True, exist_ok=True)
            # Canonical old install location may no longer exist.
            os.symlink(str(ROOT / "skills" / name), directory / name)

    def test_default_migrates_owned_absolute_relative_and_dangling_links(self):
        environment, agent, codex, state = self.fixture("migration")
        self.retired_links(agent, codex)
        for directory in (agent, codex):
            os.symlink(os.path.relpath(ROOT / "skills" / "agent-mail", directory),
                       directory / "agent-mail")
        result = self.run_installer(environment=environment)
        self.assertIn("Retired 4 owned links", result.stdout)
        for directory in (agent, codex):
            for name in ("align-work", "agent-mail"):
                self.assertFalse(os.path.lexists(directory / name))
            for name in CATALOG:
                self.assert_link(directory, name)
        self.assertFalse((state / "journal.json").exists())
        second = self.run_installer(environment=environment)
        self.assertIn("already installed", second.stdout)

    def test_migration_preserves_foreign_links_and_real_directories(self):
        environment, agent, codex, _ = self.fixture("migration-user-owned")
        for directory in (agent, codex):
            directory.mkdir()
            os.symlink("/foreign/align-work", directory / "align-work")
            (directory / "agent-mail").mkdir()
            (directory / "agent-mail" / "user-data").write_text("keep")
            # Resolving through a foreign symlink does not confer ownership.
            alias = directory / "foreign-repo"
            alias.symlink_to(ROOT, target_is_directory=True)
            (directory / "execute-goal-loop").symlink_to(alias / "skills" / "execute-goal-loop")
        result = self.run_installer(["--only", "audit-technical-work", "--migrate"],
                                    environment=environment)
        self.assertEqual(6, result.stderr.count("Skipping retirement"))
        for directory in (agent, codex):
            self.assertEqual("/foreign/align-work", os.readlink(directory / "align-work"))
            self.assertEqual("keep", (directory / "agent-mail" / "user-data").read_text())
            self.assertTrue((directory / "execute-goal-loop").is_symlink())

    def test_selective_install_requires_explicit_migration_and_preserves_unselected(self):
        for index, arguments in enumerate((["--only", "audit-technical-work"],
                                            ["--exclude", "responsive-coordinator"])):
            environment, agent, codex, _ = self.fixture(f"selective-migrate-{index}")
            self.retired_links(agent, codex)
            for directory in (agent, codex):
                (directory / "responsive-coordinator").symlink_to("/user/coordinator")
            self.run_installer(arguments, environment=environment)
            for directory in (agent, codex):
                self.assertEqual(str(ROOT / "skills" / "align-work"),
                                 os.readlink(directory / "align-work"))
                self.assertEqual("/user/coordinator", os.readlink(directory / "responsive-coordinator"))
            result = self.run_installer([*arguments, "--migrate"], environment=environment)
            self.assertIn("Retired 2 owned links", result.stdout)
            for directory in (agent, codex):
                self.assertFalse(os.path.lexists(directory / "align-work"))
                self.assertEqual("/user/coordinator", os.readlink(directory / "responsive-coordinator"))

    def test_migration_only_with_empty_selection(self):
        environment, agent, codex, _ = self.fixture("retirement-only")
        self.retired_links(agent, codex)
        self.run_installer(["--only", "audit-technical-work", "--exclude", "audit-technical-work",
                            "--migrate"], environment=environment)
        for directory in (agent, codex):
            self.assertFalse(os.path.lexists(directory / "align-work"))
            self.assertFalse(os.path.lexists(directory / "audit-technical-work"))

    def test_migration_failure_rolls_back_installs_and_retirements_in_both_targets(self):
        for index, boundary in enumerate(("after-retire:2", "after-retire:4", "before-cleanup")):
            environment, agent, codex, state = self.fixture(f"retire-failure-{index}")
            self.retired_links(agent, codex)
            self.original_links(agent, codex)
            environment["SKILLS_INSTALL_FAIL_AT"] = boundary
            result = self.run_installer(["--only", "audit-technical-work", "--migrate"],
                                        environment=environment, expected=1)
            self.assertIn("rollback completed", result.stderr)
            self.assert_original_links(agent, codex)
            for directory in (agent, codex):
                self.assertEqual(str(ROOT / "skills" / "align-work"), os.readlink(directory / "align-work"))
            self.assertFalse((state / "journal.json").exists())

    def test_crash_after_retirement_recovers_then_migrates(self):
        environment, agent, codex, state = self.fixture("retire-crash")
        self.retired_links(agent, codex)
        crashed = environment.copy()
        crashed.update({"SKILLS_INSTALL_CRASH_AT": "after-retire:4", "SKILLS_INSTALL_TXID": "retire-crash"})
        self.run_installer(["--only", "audit-technical-work", "--migrate"],
                           environment=crashed, expected=97)
        self.assertTrue((state / "journal.json").is_file())
        result = self.run_installer(["--only", "audit-technical-work", "--migrate"], environment=environment)
        self.assertIn("Recovered interrupted", result.stdout)
        for directory in (agent, codex):
            self.assertFalse(os.path.lexists(directory / "align-work"))
            self.assert_link(directory, "audit-technical-work")
        self.assertTrue((state / "recovered-retire-crash.json").is_file())

    def test_legacy_v1_install_only_journal_recovery(self):
        environment, agent, codex, state = self.fixture("legacy-recovery")
        self.original_links(agent, codex)
        crashed = environment.copy()
        crashed.update({"SKILLS_INSTALL_CRASH_AT": "after-link:1", "SKILLS_INSTALL_TXID": "legacy"})
        self.run_installer(["--only", "audit-technical-work"], environment=crashed, expected=97)
        journal = state / "journal.json"
        value = json.loads(journal.read_text())
        value["schema_version"] = "skills-install-transaction/v1"
        for operation in value["operations"]:
            del operation["action"]
        journal.write_text(json.dumps(value))
        result = self.run_installer(["--only", "audit-technical-work"], environment=environment)
        self.assertIn("Recovered interrupted", result.stdout)
        for directory in (agent, codex):
            self.assert_link(directory, "audit-technical-work")

    def test_legacy_journal_for_retired_source_recovers_without_source_directory(self):
        environment, agent, codex, state = self.fixture("legacy-retired")
        state.mkdir(mode=0o700)
        operations = []
        roots = []
        source = str(ROOT / "skills" / "align-work")
        for directory in (agent, codex):
            directory.mkdir()
            backup_root = directory / ".skills-install-backup-old-retired"
            backup_root.mkdir()
            roots.append(str(backup_root))
            target = directory / "align-work"
            backup = backup_root / "align-work"
            target.symlink_to(source)
            backup.symlink_to("/original/align-work")
            operations.append({"name": "align-work", "source": source,
                               "target": str(target), "backup": str(backup),
                               "original": {"kind": "symlink", "target": "/original/align-work"}})
        (state / "journal.json").write_text(json.dumps({
            "schema_version": "skills-install-transaction/v1", "transaction_id": "old-retired",
            "repository_root": str(ROOT), "created_directories": [],
            "backup_roots": roots, "operations": operations,
        }))
        result = self.run_installer(["--only", "audit-technical-work"], environment=environment)
        self.assertIn("Recovered interrupted", result.stdout)
        for directory in (agent, codex):
            self.assertEqual("/original/align-work", os.readlink(directory / "align-work"))
            self.assert_link(directory, "audit-technical-work")
        self.assertTrue((state / "recovered-old-retired.json").is_file())

    def test_retirement_recovery_refuses_concurrent_replacement(self):
        environment, agent, codex, state = self.fixture("retire-concurrent")
        self.retired_links(agent, codex)
        crashed = environment.copy()
        crashed.update({"SKILLS_INSTALL_CRASH_AT": "after-retire:4", "SKILLS_INSTALL_TXID": "concurrent-retire"})
        self.run_installer(["--only", "audit-technical-work", "--migrate"],
                           environment=crashed, expected=97)
        # Even an identical newly created link must not be removed by rollback.
        (codex / "align-work").symlink_to(ROOT / "skills" / "align-work")
        result = self.run_installer(["--only", "audit-technical-work", "--migrate"],
                                    environment=environment, expected=1)
        self.assertIn("both original and backup", result.stderr)
        self.assertEqual(str(ROOT / "skills" / "align-work"), os.readlink(codex / "align-work"))
        self.assertTrue((state / "journal.json").is_file())

    def test_malformed_retirement_journal_is_rejected_without_mutation(self):
        environment, agent, codex, state = self.fixture("malformed-retirement")
        self.retired_links(agent, codex)
        crashed = environment.copy()
        crashed.update({"SKILLS_INSTALL_CRASH_AT": "after-journal", "SKILLS_INSTALL_TXID": "malformed"})
        self.run_installer(["--only", "audit-technical-work", "--migrate"],
                           environment=crashed, expected=97)
        journal = state / "journal.json"
        value = json.loads(journal.read_text())
        operation = next(op for op in value["operations"] if op["action"] == "retire")
        operation["original"]["target"] = "/foreign/align-work"
        journal.write_text(json.dumps(value))
        result = self.run_installer(["--only", "audit-technical-work", "--migrate"],
                                    environment=environment, expected=1)
        self.assertIn("not an owned retired link", result.stderr)
        self.assertTrue(journal.is_file())
        for directory in (agent, codex):
            self.assertEqual(str(ROOT / "skills" / "align-work"), os.readlink(directory / "align-work"))
            self.assertFalse(os.path.lexists(directory / "audit-technical-work"))


if __name__ == "__main__":
    unittest.main()
