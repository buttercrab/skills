from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
SCRIPTS = SKILL / "scripts"
GATE = REPO / ".planning" / "harden-skill-portfolio" / "gate-b-r2"
POSITIVE = GATE / "fixtures" / "positive"
AUTHORITY = GATE / "fixtures" / "authority"
sys.path.insert(0, str(SCRIPTS))

import history_v4


def load(name: str) -> dict:
    return json.loads((POSITIVE / name).read_text(encoding="utf-8"))


def assert_code(test: unittest.TestCase, code: str, callback) -> None:
    with test.assertRaises(history_v4.HistoryV4Error) as caught:
        callback()
    test.assertEqual(caught.exception.code, code)


class CapabilityReductionV3Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.history = load("history-sources-v4.valid.json")
        self.ledger = load("semantic-observation-ledger-v2.valid.json")
        self.index = load("history-index-v4.valid.json")
        self.reduction = load("capability-reduction-v3.valid.json")
        self.evidence = load("history-evidence-v1.valid.json")
        self.publication = load("history-publication-v3.valid.json")
        self.detached = {
            "runtime-model-catalog": (AUTHORITY / "runtime-model-catalog.json").read_bytes(),
            "provider-trust-catalog": (AUTHORITY / "provider-trust-catalog.json").read_bytes(),
            "callable-verification-receipt": (AUTHORITY / "callable-verification-receipt.json").read_bytes(),
        }
        truth = json.loads((GATE / "authority-ground-truth-catalog.json").read_text())
        descriptors = {
            item["role"]: item["descriptor"] for item in truth["authority_artifacts"]
        }
        model = self.reduction["model_resolution"]
        self.detached_descriptors = {
            "runtime-model-catalog": model["runtime_catalog"]["descriptor"],
            "provider-trust-catalog": model["provider_trust"]["descriptor"],
            "callable-verification-receipt": model["callable_verification"]["descriptor"],
        }
        self.authority = {
            role: (descriptors[path], (AUTHORITY / path).read_bytes())
            for role, path in {
                "provider-trust-root-receipt": "provider-trust-root-receipt.json",
                "provider-verification-key": "provider-verification.key",
                "provider-verifier": "provider-verifier.py",
                "nonce-state-before": "nonce-state.before.json",
                "nonce-state-after": "nonce-state.after.json",
            }.items()
        }
        self.provider_root_pin = truth["provider_root_authority_sha256"]
        self.trust_root_pin = history_v4.sha256_bytes(
            (AUTHORITY / "provider-trust-root-receipt.json").read_bytes()
        )

    def verify_model(self, reduction: dict, *, authority=None, root_pin=None) -> None:
        history_v4.verify_model_resolution(
            reduction,
            detached=self.detached,
            detached_descriptors=self.detached_descriptors,
            authority=self.authority if authority is None else authority,
            trusted_provider_root_authority_sha256=(
                self.provider_root_pin if root_pin is None else root_pin
            ),
            trusted_trust_root_receipt_sha256=self.trust_root_pin,
        )

    def test_exact_model_authority_passes(self) -> None:
        self.verify_model(self.reduction)

    def test_substituted_model_is_rejected(self) -> None:
        changed = deepcopy(self.reduction)
        changed["model_resolution"]["display_name"] = "substitute"
        assert_code(
            self,
            "E_EXPLORATION_MODEL_UNAVAILABLE",
            lambda: self.verify_model(changed),
        )

    def test_replayed_model_receipt_is_rejected(self) -> None:
        authority = deepcopy(self.authority)
        replayed = json.loads(authority["nonce-state-before"][1])
        receipt = self.reduction["model_resolution"]["callable_verification"]
        replayed["used_challenge_nonce_sha256s"] = [receipt["challenge_nonce_sha256"]]
        replayed["used_receipt_replay_key_sha256s"] = [receipt["response_sha256"]]
        authority["nonce-state-before"] = (
            authority["nonce-state-before"][0],
            history_v4.canonical_bytes(replayed),
        )
        assert_code(
            self,
            "E_CALLABLE_VERIFICATION_MISMATCH",
            lambda: self.verify_model(self.reduction, authority=authority),
        )

    def test_bundle_cannot_supply_its_own_provider_root_pin(self) -> None:
        assert_code(
            self,
            "E_CALLABLE_VERIFICATION_MISMATCH",
            lambda: self.verify_model(self.reduction, root_pin="0" * 64),
        )

    def test_expired_ledger_cannot_reduce(self) -> None:
        changed = deepcopy(self.index)
        changed["lifecycle"]["state"] = "expired"
        changed["lifecycle"]["transitions"].append(
            {
                "from": "live",
                "to": "expired",
                "at": "2026-07-01T00:00:01Z",
                "reason": "retention-expired",
                "receipt_sha256": "0" * 64,
            }
        )
        changed["history_index_sha256"] = history_v4.D(
            "history-index/v4", history_v4.without(changed, "history_index_sha256")
        )
        assert_code(
            self,
            "E_LEDGER_EXPIRED",
            lambda: history_v4.validate_index(changed, self.history, self.ledger),
        )

    def test_missing_extension_target_is_rejected(self) -> None:
        changed = deepcopy(self.reduction)
        decision = changed["decisions"][0]
        decision["disposition"] = "extend"
        decision["target_skill_id"] = "skill-" + "f" * 64
        decision["decision_sha256"] = history_v4.D(
            "capability-decision/v3",
            history_v4.without(decision, "decision_sha256"),
        )
        changed["reduction_sha256"] = history_v4.D(
            "capability-reduction/v3",
            history_v4.without(changed, "reduction_sha256"),
        )
        assert_code(
            self,
            "E_EXTENSION_TARGET_UNKNOWN",
            lambda: history_v4.validate_reduction(changed, self.index, self.ledger),
        )

    def test_accepted_native_identifier_leak_is_rejected(self) -> None:
        truth = json.loads((GATE / "authority-ground-truth-catalog.json").read_text())
        native = truth["native_envelopes"][0]["raw_utf8"]
        changed = deepcopy(self.publication)
        changed["summary"] = native
        changed["publication_sha256"] = history_v4.D(
            "history-publication/v3",
            history_v4.without(changed, "publication_sha256"),
        )
        assert_code(
            self,
            "E_PUBLICATION_PRIVATE_DATA",
            lambda: history_v4.validate_publication(changed, self.evidence, [native]),
        )

    def test_native_parent_chronology_conflict_is_rejected(self) -> None:
        changed = load("semantic-observation-ledger-v2.active-campaign.valid.json")
        child = next(item for item in changed["native_nodes"] if item["parent_id"] is not None)
        child["occurred_at"] = "2026-06-30T00:00:00Z"
        assert_code(self, "E_LINEAGE_CHRONOLOGY", lambda: history_v4.validate_ledger(changed))

    def test_adapter_parser_drift_is_rejected_after_producer_reseal(self) -> None:
        adapters = self.history["adapter_catalog"]["adapters"]
        acquired = {
            item["adapter_id"]: (
                item["implementation"],
                b"changed parser bytes",
            )
            for item in adapters
        }
        assert_code(
            self,
            "E_ADAPTER_IMPLEMENTATION_DRIFT",
            lambda: history_v4.verify_adapter_implementations(self.history, acquired),
        )

    def test_evidence_decision_cannot_retarget_or_drop(self) -> None:
        changed = deepcopy(self.evidence)
        decision = changed["decisions"][0]
        decision["decision_id"] = "decision-" + "f" * 32
        decision["evidence_decision_sha256"] = history_v4.D(
            "history-evidence-decision/v1",
            history_v4.without(decision, "evidence_decision_sha256"),
        )
        changed["reconciliation"]["decision_ids"] = [decision["decision_id"]]
        changed["evidence_sha256"] = history_v4.D(
            "history-evidence/v1", history_v4.without(changed, "evidence_sha256")
        )
        assert_code(
            self,
            "E_DECISION_SET_MISMATCH",
            lambda: history_v4.validate_evidence(changed, self.reduction, self.index, self.ledger),
        )

    def test_publication_decision_cannot_retarget_after_reseal(self) -> None:
        changed = deepcopy(self.publication)
        decision = changed["decisions"][0]
        decision["disposition"] = "extend"
        decision["target_skill_id"] = "skill-" + "f" * 64
        decision["publication_decision_sha256"] = history_v4.D(
            "history-publication-decision/v3",
            history_v4.without(decision, "publication_decision_sha256"),
        )
        changed["publication_sha256"] = history_v4.D(
            "history-publication/v3", history_v4.without(changed, "publication_sha256")
        )
        assert_code(
            self,
            "E_PUBLICATION_SET_MISMATCH",
            lambda: history_v4.validate_publication(changed, self.evidence),
        )


if __name__ == "__main__":
    unittest.main()
