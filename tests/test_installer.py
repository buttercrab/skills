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

    def fake_go(self, environment: dict, *, fail: bool = False):
        binary = Path(environment["HOME"]) / "bin"
        binary.mkdir()
        log = binary / "go.log"
        go = binary / "go"
        go.write_text(
            "#!/bin/sh\n"
            'printf "%s\\n" "$*" >>"$GO_LOG"\n'
            + ("exit 42\n" if fail else "exit 0\n")
        )
        go.chmod(0o755)
        environment["GO_LOG"] = str(log)
        environment["PATH"] = f"{binary}:{environment.get('PATH', '')}"
        return log

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
            os.symlink("/original/align-work", directory / "align-work")

    def assert_original_links(self, agent: Path, codex: Path):
        for directory in (agent, codex):
            target = directory / "align-work"
            self.assertTrue(target.is_symlink())
            self.assertEqual("/original/align-work", os.readlink(target))

    def test_list_and_closed_selection(self):
        result = self.run_installer(["--list"])
        self.assertEqual(CATALOG, result.stdout.splitlines())

        environment, agent, codex, _ = self.fixture("selection")
        self.run_installer(
            ["--only", "align-work,agent-mail", "--exclude", "agent-mail"],
            environment=environment,
        )
        self.assert_link(agent, "align-work")
        self.assert_link(codex, "align-work")
        self.assertFalse((agent / "agent-mail").exists())

        invalid, *_ = self.fixture("invalid")
        result = self.run_installer(["--only", "unknown-skill"], environment=invalid, expected=1)
        self.assertIn("unknown skill", result.stderr)

    def test_front_build_is_selected_and_preflighted_before_targets(self):
        environment, agent, codex, _ = self.fixture("no-front")
        self.remove_go(environment)
        self.run_installer(["--only", "align-work"], environment=environment)
        self.assert_link(agent, "align-work")

        failed, failed_agent, failed_codex, _ = self.fixture("front-failure")
        log = self.fake_go(failed, fail=True)
        result = self.run_installer(
            ["--only", "front-agent-orchestration"],
            environment=failed,
            expected=1,
        )
        self.assertIn("offline Front Agent preflight failed", result.stderr)
        self.assertTrue(log.is_file())
        self.assertFalse(failed_agent.exists())
        self.assertFalse(failed_codex.exists())

    def test_missing_go_skips_front_and_installs_other_selected_skills(self):
        default, default_agent, default_codex, _ = self.fixture("missing-go-default")
        self.remove_go(default)
        result = self.run_installer(environment=default)
        self.assertIn("Skipping front-agent-orchestration because Go was not found", result.stderr)
        for name in CATALOG:
            if name == "front-agent-orchestration":
                self.assertFalse((default_agent / name).exists())
                self.assertFalse((default_codex / name).exists())
            else:
                self.assert_link(default_agent, name)
                self.assert_link(default_codex, name)

        mixed, mixed_agent, mixed_codex, _ = self.fixture("missing-go-mixed")
        self.remove_go(mixed)
        result = self.run_installer(
            ["--only", "align-work,front-agent-orchestration"],
            environment=mixed,
        )
        self.assertIn("continuing with the other selected skills", result.stderr)
        self.assert_link(mixed_agent, "align-work")
        self.assert_link(mixed_codex, "align-work")
        self.assertFalse((mixed_agent / "front-agent-orchestration").exists())
        self.assertFalse((mixed_codex / "front-agent-orchestration").exists())

    def test_missing_go_fails_when_front_is_the_only_selected_skill(self):
        environment, agent, codex, _ = self.fixture("missing-go-front-only")
        self.remove_go(environment)
        result = self.run_installer(
            ["--only", "front-agent-orchestration"],
            environment=environment,
            expected=1,
        )
        self.assertIn(
            "cannot install front-agent-orchestration because Go was not found",
            result.stderr,
        )
        self.assertFalse(agent.exists())
        self.assertFalse(codex.exists())

    def test_default_install_all_and_excluded_front_needs_no_go(self):
        environment, agent, codex, _ = self.fixture("default")
        log = self.fake_go(environment)
        self.run_installer(environment=environment)
        self.assertTrue(log.is_file())
        for name in CATALOG:
            self.assert_link(agent, name)
            self.assert_link(codex, name)

        excluded, excluded_agent, excluded_codex, _ = self.fixture("excluded")
        self.remove_go(excluded)
        self.run_installer(["--exclude", "front-agent-orchestration"], environment=excluded)
        self.assertFalse((excluded_agent / "front-agent-orchestration").exists())
        self.assertFalse((excluded_codex / "front-agent-orchestration").exists())

    def test_nonlink_and_symlink_parent_fail_before_other_target_mutation(self):
        environment, agent, codex, state = self.fixture("hostile")
        agent.mkdir()
        (agent / "align-work").write_text("user owned")
        result = self.run_installer(["--only", "align-work"], environment=environment, expected=1)
        self.assertIn("non-link target", result.stderr)
        self.assertEqual("user owned", (agent / "align-work").read_text())
        self.assertFalse(codex.exists())
        self.assertFalse((state / "journal.json").exists())

        linked_env, linked_agent, linked_codex, _ = self.fixture("symlink-parent")
        real = self.root / "symlink-parent" / "real"
        real.mkdir()
        parent = self.root / "symlink-parent" / "linked"
        parent.symlink_to(real, target_is_directory=True)
        linked_env["AGENT_SKILLS_DIR"] = str(parent / "skills")
        result = self.run_installer(["--only", "align-work"], environment=linked_env, expected=1)
        self.assertIn("symlink component", result.stderr)
        self.assertFalse(linked_codex.exists())
        self.assertFalse(linked_agent.exists())

    def test_hostile_target_types_are_never_replaced(self):
        for kind in ("directory", "fifo"):
            with self.subTest(kind=kind):
                environment, agent, codex, state = self.fixture(f"hostile-{kind}")
                agent.mkdir()
                target = agent / "align-work"
                if kind == "directory":
                    target.mkdir()
                else:
                    os.mkfifo(target)
                result = self.run_installer(
                    ["--only", "align-work"], environment=environment, expected=1
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
            [sys.executable, "-B", str(HELPER), "--repo", str(ROOT), "--only", "align-work"],
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
            ["--only", "align-work"], environment=environment, expected=1
        )
        self.assertIn("all-target lock", second.stderr)
        stdout, stderr = process.communicate(timeout=5)
        self.assertEqual(0, process.returncode, stderr or stdout)
        self.assert_link(agent, "align-work")
        self.assert_link(codex, "align-work")

    def test_backup_collision_refuses_before_mutation(self):
        environment, agent, codex, state = self.fixture("collision")
        self.original_links(agent, codex)
        (agent / ".skills-install-backup-fixed").mkdir()
        environment["SKILLS_INSTALL_TXID"] = "fixed"
        result = self.run_installer(["--only", "align-work"], environment=environment, expected=1)
        self.assertIn("backup collision", result.stderr)
        self.assert_original_links(agent, codex)
        self.assertFalse((state / "journal.json").exists())

    def test_replaced_links_keep_same_filesystem_backups(self):
        environment, agent, codex, state = self.fixture("retained-backups")
        self.original_links(agent, codex)
        environment["SKILLS_INSTALL_TXID"] = "retained"
        result = self.run_installer(
            ["--only", "align-work"], environment=environment
        )
        self.assertIn("Retained same-filesystem backup", result.stdout)
        for directory in (agent, codex):
            self.assert_link(directory, "align-work")
            backup_root = directory / ".skills-install-backup-retained"
            backup = backup_root / "align-work"
            self.assertTrue(backup.is_symlink())
            self.assertEqual("/original/align-work", os.readlink(backup))
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
                    ["--only", "align-work"], environment=environment, expected=1
                )
                self.assertIn("rollback completed", result.stderr)
                self.assert_original_links(agent, codex)
                self.assertFalse((state / "journal.json").exists())
                archives = list(state.glob("failed-*.json"))
                self.assertEqual(1, len(archives))
                data = json.loads(archives[0].read_text())
                self.assertEqual("skills-install-transaction/v1", data["schema_version"])

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
                    ["--only", "align-work"], environment=environment, expected=1
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
                    ["--only", "align-work"], environment=crashed, expected=97
                )
                self.assertTrue((state / "journal.json").is_file())
                recovered = environment.copy()
                recovered["SKILLS_INSTALL_TXID"] = txid
                result = self.run_installer(
                    ["--only", "align-work"], environment=recovered
                )
                self.assertIn("Recovered interrupted installer transaction", result.stdout)
                self.assert_link(agent, "align-work")
                self.assert_link(codex, "align-work")
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
        result = self.run_installer(["--only", "align-work"], environment=failed, expected=1)
        self.assertIn("rollback failed", result.stderr)
        self.assertTrue((state / "journal.json").is_file())

        recovered = environment.copy()
        recovered["SKILLS_INSTALL_TXID"] = "reinstall-after-recovery"
        result = self.run_installer(["--only", "align-work"], environment=recovered)
        self.assertIn("Recovered interrupted installer transaction", result.stdout)
        self.assert_link(agent, "align-work")
        self.assert_link(codex, "align-work")
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
            [sys.executable, "-B", str(HELPER), "--repo", str(ROOT), "--only", "align-work"],
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        desired = str((ROOT / "skills" / "align-work").resolve())
        deadline = time.time() + 5
        while time.time() < deadline:
            if (agent / "align-work").is_symlink() and os.readlink(agent / "align-work") == desired:
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


if __name__ == "__main__":
    unittest.main()
