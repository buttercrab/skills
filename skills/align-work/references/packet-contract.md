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
python3 scripts/planning_packet.py transition <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --to executing --reuse-approval
```

Use `handoff` for an orderly coordinator transfer. Use `recover` only after the user authorizes takeover from an unavailable coordinator. A handoff or recovery during active work pauses it and clears runtime authorization. The same explicit user recovery/resume message may authorize both takeover and resume; never ask twice for that transition. Use `repair` only when validation reports structural/digest invalidity; it clears approval and seals a new unapproved revision.

## Approval

Show the user the packet ID, repository root, exact revision, digest, requested authority classes, and a concise description of the approval envelope. A plain approval in direct response is sufficient; the user need not repeat the digest or classes. Unless the user explicitly says to approve without starting, use that same message to record approval and transition immediately to execution with `--reuse-approval`. Do not ask a second “start?” question.

Approval evidence in `state.json` is an audit record, not authenticated authority. `--reuse-approval` is valid only for trusted same-task continuity: the same visible Codex task, a valid packet/approval identity, matching coordinator state, no open question, and no out-of-envelope discovery. The helper checks structure, not conversational continuity; the coordinator must enforce this boundary.

## Resume

1. Validate packet structure, digest, and execution chain.
2. Confirm the packet path and task ID; do not guess among multiple packets.
3. Read volatile-fact recheck rules and `execution.md` without mutating; identify any incomplete pending attempt.
4. Determine continuity. Compaction, automatic continuation, or a later turn in the same visible Codex task may reuse a valid approval without a prompt. A fresh Codex task requires an explicit user continue/resume/implement instruction; that instruction itself is reauthorization, so ask only when it is absent.
5. Acquire, hand off, or recover coordinator ownership with the expected fencing epoch. Unexpected recovery still requires genuine user takeover authority, but the same user message may also authorize resume.
6. Revalidate volatile facts and compare current repository/global state to the approved baseline.
7. Reconcile incomplete attempts and select the next eligible plan step. Use `--reuse-approval` only for trusted same-task continuity; otherwise pass the current user instruction as `--authorization-evidence`.

If protected bytes disagree with the stored digest, stop ordinary mutation. Reconcile the ledgers, run guarded `repair`, and return to planning or review without approval.

Execution markers are the authoritative hash-chained records; surrounding Markdown is presentation only. Every marker binds packet ID, revision, protected digest, and approval ID. `record-attempt` writes a pending hash to state before appending, then anchors that exact hash. `repair` may clear an unappended pending hash or anchor exactly one complete tail matching it; it never accepts an arbitrary unannounced tail. Completion requires a final passed verification record bound to the current packet revision and approval. Rollback receipts and receipts from superseded revisions cannot complete the task.
