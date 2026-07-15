from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
REPO = SKILL.parents[1]
GATE = REPO / ".planning" / "harden-skill-portfolio" / "gate-b-r2"
POSITIVE = GATE / "fixtures" / "positive"
AUTHORITY = GATE / "fixtures" / "authority"
sys.path.insert(0, str(SCRIPTS))

import history_v4
import index_agent_history
import normalize_codex_history
import validate_history_v4
from strict_json import StrictJSONError, canonical_bytes, loads_strict


def load(name: str) -> dict:
    return json.loads((POSITIVE / name).read_text(encoding="utf-8"))


class HistoryV4PipelineTests(unittest.TestCase):
    def test_all_successor_schemas_and_semantics_accept_positive_chain(self) -> None:
        history = load("history-sources-v4.valid.json")
        ledger = load("semantic-observation-ledger-v2.valid.json")
        index = load("history-index-v4.valid.json")
        reduction = load("capability-reduction-v3.valid.json")
        evidence = load("history-evidence-v1.valid.json")
        publication = load("history-publication-v3.valid.json")
        for document in (history, ledger, index, reduction, evidence, publication):
            history_v4.validate_schema(document)
        history_v4.validate_ledger(ledger)
        history_v4.validate_sources(history, ledger)
        history_v4.validate_index(index, history, ledger)
        history_v4.validate_reduction(reduction, index, ledger)
        history_v4.validate_evidence(evidence, reduction, index, ledger)
        history_v4.validate_publication(publication, evidence)

    def test_strict_json_normalizes_values_and_rejects_key_collisions(self) -> None:
        value = loads_strict('{"value":"e\\u0301"}')
        self.assertEqual(canonical_bytes(value), '{"value":"é"}'.encode())
        with self.assertRaisesRegex(StrictJSONError, "normalized JSON object key collision"):
            loads_strict('{"é":1,"e\\u0301":2}')
        with self.assertRaisesRegex(StrictJSONError, "duplicate JSON object key"):
            loads_strict('{"x":1,"x":2}')

    def test_per_index_identity_is_unlinkable_and_full_length(self) -> None:
        key1, key2 = b"a" * 32, b"b" * 32
        salt1, salt2 = b"c" * 32, b"d" * 32
        native1 = history_v4.derive_native_hmac(key1, salt1, "codex", "session", "native")
        native2 = history_v4.derive_native_hmac(key2, salt2, "codex", "session", "native")
        public1 = history_v4.derive_public_id(key1, salt1, "session", "session", native1)
        public2 = history_v4.derive_public_id(key2, salt2, "session", "session", native2)
        self.assertNotEqual(native1, native2)
        self.assertNotEqual(public1, public2)
        self.assertRegex(public1, r"^session-[0-9a-f]{64}$")

    def test_descriptor_read_rejects_symlink_hardlink_unsafe_mode_and_swap(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "source.json"
            target.write_text("{}", encoding="utf-8")
            target.chmod(0o600)
            descriptor, payload = history_v4.acquire_file(root, "source.json", max_bytes=10)
            self.assertEqual(payload, b"{}")
            self.assertEqual(descriptor["nlink"], 1)

            link = root / "link.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_DESCRIPTOR_SYMLINK"):
                history_v4.acquire_file(root, "link.json", max_bytes=10)

            hard = root / "hard.json"
            os.link(target, hard)
            with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_DESCRIPTOR_HARD_LINK"):
                history_v4.acquire_file(root, "source.json", max_bytes=10)
            hard.unlink()

            target.chmod(0o666)
            with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_DESCRIPTOR_UNSAFE_MODE"):
                history_v4.acquire_file(root, "source.json", max_bytes=10)
            target.chmod(0o600)

            def mutate(_: int) -> None:
                target.write_text("changed", encoding="utf-8")
                target.chmod(0o600)

            with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_DESCRIPTOR_SWAP"):
                history_v4.acquire_file(root, "source.json", max_bytes=20, post_read_hook=mutate)

    def test_exact_bundle_rejects_copied_private_state_and_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for name in ("one", "two"):
                (root / name).write_text(name, encoding="utf-8")
                (root / name).chmod(0o600)
            with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_PRIVATE_FILE_SET_MISMATCH"):
                history_v4.acquire_exact_bundle(
                    root, ["one"], max_file_bytes=10, max_total_bytes=20
                )
            (root / "two").unlink()
            acquired = history_v4.acquire_exact_bundle(
                root, ["one"], max_file_bytes=10, max_total_bytes=20
            )
            self.assertEqual(acquired["one"][1], b"one")

    def test_adapter_projection_redacts_every_native_value(self) -> None:
        row = {
            "type": "session_meta",
            "timestamp": "2026-07-01T00:00:00Z",
            "payload": {
                "id": "native-session-secret",
                "instructions": "Handle native-session-secret at https://private.invalid",
            },
        }
        payload = canonical_bytes(row) + b"\n"
        projection = normalize_codex_history.project(
            platform="codex",
            source_id="source-" + "1" * 32,
            descriptor={"sha256": history_v4.sha256_bytes(payload)},
            payload=payload,
            identity_key=b"k" * 32,
            index_salt=b"s" * 32,
        )
        text = projection["records"][0]["redacted_text"]
        self.assertNotIn("native-session-secret", text)
        self.assertNotIn("https://", text)
        self.assertIn("[REDACTED:NATIVE_ID]", text)

    def test_claude_leaf_uuid_is_inventoried_and_unknown_native_fields_fail_closed(self) -> None:
        row = {
            "type": "user",
            "sessionId": "claude-session-secret",
            "uuid": "claude-message-secret",
            "leafUuid": "claude-leaf-secret",
            "timestamp": "2026-07-01T00:00:00Z",
            "message": {"content": "Review claude-leaf-secret."},
        }
        payload = canonical_bytes(row) + b"\n"
        projection = normalize_codex_history.project(
            platform="claude-code",
            source_id="source-" + "2" * 32,
            descriptor={"sha256": history_v4.sha256_bytes(payload)},
            payload=payload,
            identity_key=b"k" * 32,
            index_salt=b"s" * 32,
        )
        self.assertIn(
            "claude-leaf-secret",
            {item["native_value"] for item in projection["native_map"]},
        )
        self.assertNotIn(
            "claude-leaf-secret", projection["records"][0]["redacted_text"]
        )

        hostile = deepcopy(row)
        hostile["message"]["mysteryUuid"] = "uncataloged-native-secret"
        with self.assertRaisesRegex(
            history_v4.HistoryV4Error, "E_NATIVE_ID_INVENTORY_INCOMPLETE"
        ):
            normalize_codex_history.project(
                platform="claude-code",
                source_id="source-" + "2" * 32,
                descriptor={"sha256": "0" * 64},
                payload=canonical_bytes(hostile) + b"\n",
                identity_key=b"k" * 32,
                index_salt=b"s" * 32,
            )

    def test_allowed_history_tree_discovers_complete_jsonl_set(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "sessions" / "2026").mkdir(parents=True)
            (root / "archived_sessions").mkdir()
            (root / "sessions" / "2026" / "one.jsonl").write_text("{}\n")
            (root / "archived_sessions" / "two.jsonl").write_text("{}\n")
            (root / "sessions" / "ignored.txt").write_text("ignored")
            for path in root.rglob("*"):
                if path.is_file():
                    path.chmod(0o600)
            acquired = history_v4.acquire_allowed_tree(
                root,
                ["sessions/**/*.jsonl", "archived_sessions/*.jsonl"],
                max_file_bytes=1024,
                max_total_bytes=2048,
            )
            self.assertEqual(
                set(acquired),
                {"sessions/2026/one.jsonl", "archived_sessions/two.jsonl"},
            )

    def test_raw_replay_rejects_changed_transcript_bytes(self) -> None:
        history = load("history-sources-v4.valid.json")
        ledger = load("semantic-observation-ledger-v2.valid.json")
        evidence = load("history-evidence-v1.valid.json")
        documents = {"history": history, "ledger": ledger, "evidence": evidence}
        private = GATE / "fixtures" / "private-bundle"
        native_map = json.loads((private / "native-map.json").read_text())["entries"]
        key = (private / "identity-key").read_bytes()
        salt = (private / "identity-salt").read_bytes()
        old_codex = os.environ.get("CODEX_HOME")
        old_claude = os.environ.get("CLAUDE_CONFIG_DIR")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            codex_root = root / "codex"
            claude_root = root / "claude"
            codex_path = codex_root / "sessions" / "2026" / "07" / "codex.jsonl"
            claude_path = claude_root / "projects" / "fixture" / "claude.jsonl"
            codex_path.parent.mkdir(parents=True)
            claude_path.parent.mkdir(parents=True)
            shutil.copyfile(AUTHORITY / "raw" / "codex.jsonl", codex_path)
            shutil.copyfile(AUTHORITY / "raw" / "claude-code.jsonl", claude_path)
            codex_path.chmod(0o600)
            claude_path.chmod(0o600)
            os.environ["CODEX_HOME"] = str(codex_root)
            os.environ["CLAUDE_CONFIG_DIR"] = str(claude_root)
            try:
                home = Path.home().resolve(strict=True)
                by_platform = {item["platform"]: item for item in history["user_roots"]}
                for platform in ("codex", "claude-code"):
                    selected, receipt = history_v4.select_user_root(platform, home=home)
                    expected = by_platform[platform]
                    for field, value in receipt.items():
                        if field != "captured_at":
                            expected[field] = value
                    allowlist = expected["relative_path_allowlist"]
                    acquired = history_v4.acquire_allowed_tree(
                        selected,
                        allowlist,
                        max_file_bytes=history["limits"]["max_file_bytes"],
                        max_total_bytes=history["limits"]["max_total_bytes"],
                    )
                    self.assertEqual(len(acquired), 1)
                    relative, (descriptor, _) = next(iter(acquired.items()))
                    source = next(
                        item for item in history["sources"] if item["platform"] == platform
                    )
                    source["relative_path_sha256"] = history_v4.sha256_bytes(
                        relative.encode()
                    )
                    source["snapshot"] = descriptor
                adapter_descriptor, _ = history_v4.acquire_file(
                    SCRIPTS,
                    "normalize_codex_history.py",
                    max_bytes=history["limits"]["max_file_bytes"],
                )
                for adapter in history["adapter_catalog"]["adapters"]:
                    adapter["implementation"] = adapter_descriptor
                raw_receipt = evidence["bindings"]["raw_reopen_receipt"]
                raw_receipt["source_descriptor_sha256s"] = sorted(
                    item["snapshot"]["sha256"] for item in history["sources"]
                )
                body = history_v4.without(raw_receipt, "receipt_sha256", "descriptor")
                raw_receipt["receipt_sha256"] = history_v4.D(
                    "raw-reopen-receipt/v2", body
                )
                evidence["bindings"]["raw_reopen_receipt_sha256"] = raw_receipt[
                    "receipt_sha256"
                ]
                native_values = validate_history_v4._replay_raw_sources(
                    documents,
                    key=key,
                    salt=salt,
                    private_native_map=native_map,
                )
                self.assertIn("codex-native-session-1", native_values)

                codex_path.write_bytes(codex_path.read_bytes() + b" ")
                codex_path.chmod(0o600)
                with self.assertRaisesRegex(
                    history_v4.HistoryV4Error, "E_RAW_SNAPSHOT_REBUILD_REQUIRED"
                ):
                    validate_history_v4._replay_raw_sources(
                        documents,
                        key=key,
                        salt=salt,
                        private_native_map=native_map,
                    )
            finally:
                if old_codex is None:
                    os.environ.pop("CODEX_HOME", None)
                else:
                    os.environ["CODEX_HOME"] = old_codex
                if old_claude is None:
                    os.environ.pop("CLAUDE_CONFIG_DIR", None)
                else:
                    os.environ["CLAUDE_CONFIG_DIR"] = old_claude

    def test_active_campaign_platform_and_fixed_point_mutations_fail(self) -> None:
        history = load("history-sources-v4.active-campaign.valid.json")
        ledger = load("semantic-observation-ledger-v2.active-campaign.valid.json")
        root_record_id = history["active_campaign"]["closure"]["root_ids"][0]
        root_node = next(
            item for item in ledger["native_nodes"] if item["record_id"] == root_record_id
        )
        history["active_campaign"]["root_native_hmac"] = root_node["native_hmac"]
        history["active_campaign"]["namespace_hmacs"] = [
            root_node["namespace_native_hmac"]
        ]
        history_v4.validate_active_campaign(history, ledger)
        changed = deepcopy(history)
        changed["active_campaign"]["platform"] = "unknown"
        with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_ACTIVE_CAMPAIGN_PLATFORM"):
            history_v4.validate_active_campaign(changed, ledger)
        changed = deepcopy(history)
        changed["active_campaign"]["closure"]["excluded_record_ids"] = []
        with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_ACTIVE_CAMPAIGN_INCOMPLETE"):
            history_v4.validate_active_campaign(changed, ledger)

    def test_deleted_tombstone_validates_and_illegal_transition_fails(self) -> None:
        history = load("history-sources-v4.valid.json")
        ledger = load("semantic-observation-ledger-v2.valid.json")
        deleted = load("history-index-v4.deleted.valid.json")
        history_v4.validate_index(deleted, history, ledger)
        changed = deepcopy(deleted)
        changed["lifecycle"]["transitions"][1]["from"] = "collecting"
        changed["history_index_sha256"] = history_v4.D(
            "history-index/v4", history_v4.without(changed, "history_index_sha256")
        )
        with self.assertRaisesRegex(history_v4.HistoryV4Error, "E_LIFECYCLE_TRANSITION"):
            history_v4.validate_index(changed, history, ledger)

    def test_index_builder_materializes_and_reopens_exact_ten_member_bundle(self) -> None:
        private = GATE / "fixtures" / "private-bundle"
        temp_parent = Path(tempfile.gettempdir()).resolve()
        with tempfile.TemporaryDirectory(dir=temp_parent) as raw:
            root = Path(raw) / "input"
            root.mkdir(mode=0o700)
            sources = {
                "sources.json": POSITIVE / "history-sources-v4.valid.json",
                "semantic-ledger.json": POSITIVE / "semantic-observation-ledger-v2.valid.json",
                "exclusion-ledger.json": private / "exclusion-ledger.json",
                "native-map.json": private / "native-map.json",
                "identity-salt": private / "identity-salt",
                "identity-key": private / "identity-key",
                "identity-key.receipt.json": private / "identity-key.receipt.json",
                "adapter-catalog.json": private / "adapter-catalog.json",
                "lifecycle.json": private / "lifecycle.json",
            }
            for name, source in sources.items():
                shutil.copyfile(source, root / name)
                (root / name).chmod(0o600)
            (root / "index-template.json").write_text(
                json.dumps({"created_at": "2026-07-01T00:00:00Z", "edge_ids": []}),
                encoding="utf-8",
            )
            (root / "index-template.json").chmod(0o600)
            out = Path(raw) / "output"
            built = index_agent_history.build(
                root,
                out,
                max_file_bytes=64 * 1024 * 1024,
                max_total_bytes=256 * 1024 * 1024,
            )
            self.assertEqual(built["exact_file_set"]["member_count"], 10)
            checked = index_agent_history.validate(
                out,
                max_file_bytes=64 * 1024 * 1024,
                max_total_bytes=256 * 1024 * 1024,
            )
            self.assertEqual(checked["history_index_sha256"], built["history_index_sha256"])

    def test_ordered_migration_precedes_schema_failure_and_raw_bypass(self) -> None:
        documents = {
            "history": {"schema_version": "history-sources/v3"},
            "ledger": None,
            "index": None,
            "reduction": None,
            "evidence": None,
            "publication": None,
        }
        self.assertEqual(
            history_v4.ordered_migration_diagnostic(
                documents,
                authoritative_raw_reopen=False,
                exact_history_binding=False,
                exact_model_available=False,
            ),
            "E_HISTORY_SOURCES_VERSION_UNSUPPORTED",
        )
        documents = {
            "history": {"schema_version": "history-sources/v4", "raw_manifest": {"schema_version": "raw-source-manifest/v2"}},
            "ledger": {"schema_version": "semantic-observation-ledger/v2"},
            "index": {"schema_version": "history-index/v4"},
            "reduction": {"schema_version": "capability-reduction/v3"},
            "evidence": {"schema_version": "history-evidence/v1"},
            "publication": {"schema_version": "history-publication/v3"},
        }
        self.assertEqual(
            history_v4.ordered_migration_diagnostic(
                documents,
                authoritative_raw_reopen=False,
                exact_history_binding=True,
                exact_model_available=True,
            ),
            "E_RAW_REOPEN_REQUIRED",
        )

    def test_diagnostic_only_cli_is_non_authoritative_and_nonzero(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPTS / "validate_history_v4.py"),
                "--bundle-root",
                str(POSITIVE),
                "--diagnostic-without-raw-reopen",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        value = json.loads(result.stdout)
        self.assertFalse(value["authoritative"])
        self.assertEqual(value["diagnostic"], "E_RAW_REOPEN_REQUIRED")


if __name__ == "__main__":
    unittest.main()
