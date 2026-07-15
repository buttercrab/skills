# Capability reduction contract

Apply this contract in capability mode after the complete History v4 source,
ledger, and index chain is live. The normative owner is
[History v4 immutable specification](history-v4-specification.md) and the closed
[capability-reduction-v3 schema](capability-reduction-v3.schema.json).

## Bind authority before disclosure

Bind one exact live `history-sources/v4`, `semantic-observation-ledger/v2`, and
`history-index/v4`. Reopen the runtime catalog, independent provider trust
catalog and key, verifier, nonce state, callable-verification receipt, and
capability catalog through one descriptor-safe authority transaction. Resolve
exactly one callable `5.6 lunar high` entry with the approved settings. Do not
guess an alias or substitute another model.

The exploration model may receive only one bounded redacted source-bound
`capability-packet/v3`. It may classify, summarize, and cluster that packet. It
may not select sources, plan or widen the campaign, access another packet,
adjudicate overlap, choose a target skill, decide create/extend/reject, approve a
gate, mutate state, or write final synthesis. The primary coordinator owns those
actions.

## Close schedule, results, and hydration

Freeze the schedule, immutable packets, attempts, accepted results, provider
receipts, settings, prompts, schemas, and bounds before execution. Every
observation is an exact projection of the live ledger. Retain unknown or
cross-packet references only as dropped quality evidence with zero authority.

Retries preserve the packet. Split children form an exact disjoint partition of
their parent. Every terminal packet has exactly one accepted result. Hydration
reopens the same unexpired ledger and exact accepted set. The primary synthesis
input is the canonical accepted result/receipt set plus the hydration output and
receipt.

Each reducer-reviewed, independently rooted `user-root` contributes at most one
recurrence credit per candidate. Delegated, retry, continuation, test, replay,
synthetic, system, duplicate-export, non-semantic, excluded, and active-campaign
records contribute zero. Keep independent-root and project-family sets and
counts separate and exact.

## Decide and project exactly

Candidate IDs equal the decision candidate-ID projection. Every candidate has
exactly one `create`, `extend`, or `reject` decision. Only `extend` carries a
target, and the target must exist in the descriptor-reopened capability
catalog. Decision evidence collectively covers the candidate's accepted
hydrated observations.

Evidence copies every reduction decision ID, candidate, disposition, target,
and observation set byte-for-byte and binds its reduction decision hash. It may
only add its closed claim, capability, and overlap reference sets. Publication
copies the evidence decision and may only add its bounded rationale and
publication decision hash. No stage may synthesize, drop, duplicate, retarget,
or reorder a decision.

Run `validate_history_v4.py` with the exact six-document `--bundle-root`, live
`--private-index-root`, independent exact `--authority-root`, and both
out-of-band `--trusted-provider-root-authority-sha256` and
`--trusted-trust-root-receipt-sha256` pins before any synthesis or publication.
The validator discovers every allowlisted raw JSONL leaf from the authenticated
Codex and Claude roots and reruns the shared adapter/redactor. A diagnostic-only
run is closed, non-authoritative, exits nonzero, and cannot advance hydration,
synthesis, evidence, or publication. Reject every earlier reduction family
with `E_CAPABILITY_REDUCTION_VERSION_UNSUPPORTED` and rebuild under the live v4
chain.
