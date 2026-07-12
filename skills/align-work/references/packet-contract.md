# Planning Packet Contract

Read this reference before creating, resuming, sealing, approving, transitioning, or repairing a packet.

## Files

- `facts.md`: observed facts with stable IDs, exact evidence, verification time, volatility, and recheck rule. Keep inference and unknowns separate.
- `decisions.md`: stable decision IDs, questions, meaningful options, user-confirmed choices, rationale, consequences, provenance, supersession, and alignment rounds.
- `plan.md`: context-independent execution snapshot that lists consumed fact and decision IDs and restates everything needed to act.
- `state.json`: machine state, random packet ID, canonical repository root, packet revision/digest, open questions, active coordinator/fencing epoch, approval evidence, and execution-chain head/pending hash. Never edit it manually.
- `execution.md`: hash-chained attempt and resume ledger created when execution starts or when an approved packet first enters `needs_reapproval`.

Protected files are `decisions.md`, `facts.md`, and `plan.md`. Sealing computes the documented SHA-256 digest over their exact bytes and clears prior approval. Approval also binds the packet ID and canonical repository root, so copying the packet to another repository is invalid.

## Authority classes

Use only these class families; a numeric suffix narrows a family when the plan defines multiple separately approved surfaces:

- `P`: planning-packet writes;
- `R`: repository/product writes;
- `T`: local tests, temporary state, and disposable fixtures;
- `I`: local installation or link changes;
- `G`: personal/global configuration;
- `E`: external-service reads or writes;
- `D`: publish, deploy, destructive, irreversible, or production action.

The protected plan must define the exact scope of every requested code such as `G1` or `E2`. The helper rejects unknown class syntax but validates structure only; it cannot authenticate a user event.

## Core commands

```bash
python3 scripts/planning_packet.py init --repo <repo> --task-id <slug> --title <title>
python3 scripts/planning_packet.py validate <packet>
python3 scripts/planning_packet.py questions <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --set Q-001
python3 scripts/planning_packet.py seal <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --status awaiting_approval --authority R,T
python3 scripts/planning_packet.py transition <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --to approved --approval-id <uuid> --authority R,T --approval-evidence <text>
```

Use `handoff` for an orderly coordinator transfer. Use `recover` only after the user authorizes takeover from an unavailable coordinator. A handoff or recovery during active work pauses it, clears runtime authorization, and requires current-session authorization before resume. Use `repair` only when validation reports structural/digest invalidity; it clears approval and seals a new unapproved revision.

## Approval

Show the user the packet ID, repository root, exact revision, digest, and requested authority classes. Approval evidence in `state.json` is an audit record, not authenticated authority. A fresh human-facing coordinator must show this identity and ask the user to reauthorize before coordinator takeover or other mutation.

## Resume

1. Validate packet structure, digest, and execution chain.
2. Confirm the packet path and task ID; do not guess among multiple packets.
3. Read volatile-fact recheck rules and `execution.md` without mutating; identify any incomplete pending attempt.
4. In a fresh human-facing session, show packet identity and reconfirm authority.
5. Only after reauthorization, acquire or recover coordinator ownership with the expected fencing epoch.
6. Revalidate volatile facts and compare current repository/global state to the approved baseline.
7. Reconcile incomplete attempts and select the next eligible plan step.

If protected bytes disagree with the stored digest, stop ordinary mutation. Reconcile the ledgers, run guarded `repair`, and return to planning or review without approval.

Execution markers are the authoritative hash-chained records; surrounding Markdown is presentation only. Every marker binds packet ID, revision, protected digest, and approval ID. `record-attempt` writes a pending hash to state before appending, then anchors that exact hash. `repair` may clear an unappended pending hash or anchor exactly one complete tail matching it; it never accepts an arbitrary unannounced tail. Completion requires a final passed verification record bound to the current packet revision and approval. Rollback receipts and receipts from superseded revisions cannot complete the task.
