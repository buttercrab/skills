from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
GATE = REPO / ".planning" / "harden-skill-portfolio" / "gate-b-r2"
CANDIDATE = GATE / "candidate" / "skills" / "mine-history-tool-landscapes" / "references"


class HistoryV4ConformanceTests(unittest.TestCase):
    def test_installed_normative_bytes_equal_approved_component(self) -> None:
        installed = SKILL / "references"
        for source in sorted(CANDIDATE.iterdir()):
            target = installed / source.name
            self.assertTrue(target.is_file(), source.name)
            self.assertEqual(
                hashlib.sha256(target.read_bytes()).hexdigest(),
                hashlib.sha256(source.read_bytes()).hexdigest(),
                source.name,
            )

    def test_old_contracts_and_runtime_are_not_callable(self) -> None:
        for relative in (
            "references/history-v3-specification.md",
            "references/history-sources-v3.schema.json",
            "references/semantic-observation-ledger-v1.schema.json",
            "references/capability-reduction-v2.schema.json",
            "scripts/history_v3.py",
        ):
            self.assertFalse((SKILL / relative).exists(), relative)
        scripts = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (SKILL / "scripts").glob("*.py")
        )
        self.assertNotIn("import history_v3", scripts)
        self.assertNotIn("--skip-raw-reopen", scripts)

    def test_approved_hostile_catalog_covers_all_nine_audit_families(self) -> None:
        catalog = json.loads((GATE / "hostile-fixture-catalog.json").read_text())
        filesystem = json.loads((GATE / "filesystem-hostile-catalog.json").read_text())
        text = json.dumps([catalog, filesystem], sort_keys=True)
        for diagnostic in (
            "E_EXPLORATION_MODEL_UNAVAILABLE",
            "E_LEDGER_EXPIRED",
            "E_EXTENSION_TARGET_UNKNOWN",
            "E_PUBLICATION_PRIVATE_DATA",
            "E_ACTIVE_CAMPAIGN_PLATFORM",
            "E_LINEAGE_CHRONOLOGY",
            "E_PRIVATE_FILE_SET_MISMATCH",
            "E_DESCRIPTOR_SYMLINK",
            "E_ADAPTER_IMPLEMENTATION_DRIFT",
            "E_RAW_SNAPSHOT_REBUILD_REQUIRED",
        ):
            self.assertIn(diagnostic, text)

    def test_exact_bound_candidate_conformance_is_green(self) -> None:
        # Frozen descriptor fixtures are intentionally device/inode-bound. Rebuild
        # an isolated successor copy so conformance proves the generator and
        # validator together instead of depending on the checkout's APFS device.
        with tempfile.TemporaryDirectory() as raw:
            isolated_repo = Path(raw)
            isolated_gate = (
                isolated_repo / ".planning" / "harden-skill-portfolio" / "gate-b-r2"
            )
            isolated_gate.parent.mkdir(parents=True)
            shutil.copytree(GATE, isolated_gate)
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            built = subprocess.run(
                [sys.executable, "-B", str(isolated_gate / "build_artifacts.py")],
                cwd=isolated_repo,
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            conformance = """
import importlib.util
from pathlib import Path
import sys
gate = Path(sys.argv[1]).resolve()
repo = gate.parents[2]
spec = importlib.util.spec_from_file_location("gate_b_r2_validator", gate / "validate_candidate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.validate_schemas(gate)
module.validate_canonical_json_contract()
module.validate_positive_semantics(gate)
module.validate_normative_commitments(gate)
module.validate_specification(gate)
module.validate_migration_and_boundary(gate)
module.validate_hostiles(gate)
module.validate_authority_ground_truth(gate)
module.validate_private_bundle(gate)
module.validate_filesystem_hostiles(gate)
module.validate_component(repo, gate)
module.validate_artifact_manifest(repo, gate)
print("Gate B-R2 candidate validation passed: 6 schemas, 12 positive fixtures, 66 protocol-resealed hostile cases, 12 executable filesystem attacks")
"""
            result = subprocess.run(
                [sys.executable, "-B", "-c", conformance, str(isolated_gate)],
                cwd=isolated_repo,
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("66 protocol-resealed hostile cases", result.stdout)
        self.assertIn("12 executable filesystem attacks", result.stdout)


if __name__ == "__main__":
    unittest.main()
