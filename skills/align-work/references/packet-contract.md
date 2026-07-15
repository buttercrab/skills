# Planning Packet Contract

This reference is durable-mode only. Do not create or resume a packet for lightweight Align work. Read it before creating, resuming, sealing, approving, transitioning, transferring, or repairing a packet.

## Files

- `facts.md`: observed facts with stable IDs, exact evidence, verification time, volatility, and recheck rule. Keep inference and unknowns separate.
- `decisions.md`: stable decision IDs, questions, meaningful options, user-confirmed choices, rationale, consequences, provenance, supersession, and alignment rounds.
- `plan.md`: context-independent, human-readable execution snapshot that restates everything needed to act without requiring readers to decode ledger IDs.
- `state.json`: machine state, random packet ID, canonical repository root, packet revision/digest, open questions, active coordinator/fencing epoch, approval evidence, and execution-chain head/pending hash. Never edit it manually.
- `execution.md`: hash-chained attempt and resume ledger created when execution starts or when an approved packet first enters `needs_reapproval`.

Protected files are `decisions.md`, `facts.md`, and `plan.md`. Sealing computes the documented SHA-256 digest over their exact bytes and clears prior approval. Approval also binds the packet ID and canonical repository root, so copying the packet to another repository is invalid.

## Approval scope and schema versions

Schema version 2 is the default. It stores approval scope only in the protected plain-language plan and binds approval to that plan's digest. Its state and approval records contain no duplicate scope classification, and normal seal and approval commands take no scope-code flag.

Validation uses exact field sets for each schema version. Do not add version-1 fields to a version-2 packet or remove them from a version-1 packet. Do not migrate an existing packet merely to change its schema version.

### Legacy schema version 1

Version-1 packets retain `requested_authority_classes` in state and `authority_classes` in approval records. When resealing an existing version-1 packet, pass `--authority` with its intended comma-separated legacy values. Approval may omit the flag and reuse the list stored at seal time; if supplied, the list must match. The legacy parser accepts the families `P`, `R`, `T`, `I`, `G`, `E`, and `D`, each optionally followed by digits. This compatibility path exists only to resume old packets; do not use it for new work.

## Core machine commands

```bash
python3 scripts/planning_packet.py init --repo <repo> --task-id <slug> --title <title>
python3 scripts/planning_packet.py validate <packet>
python3 scripts/planning_packet.py questions <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --set Q-001
python3 scripts/planning_packet.py seal <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --status awaiting_approval
python3 scripts/planning_packet.py transition <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --to approved --approval-id <uuid> --approval-evidence <text>
python3 scripts/planning_packet.py transition <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --to executing --reuse-approval
```

Use `handoff` for an orderly coordinator transfer. Use `recover` only after the user authorizes takeover from an unavailable coordinator. A handoff or recovery during active work pauses it and clears runtime authorization. The same explicit user recovery/resume message may authorize both takeover and resume; never ask twice for that transition. Use `repair` only when validation reports structural/digest invalidity; it clears approval and seals a new unapproved revision.

Every `handoff` emits a closed `packet-transfer-receipt/v1` in its JSON result. The receipt binds repository and packet identity, revision and digest, approval, old and new coordinator fencing, resulting generation, paused and resume status, cleared runtime authority, and execution-chain head. Validate it against current reality with `scripts/work_authority.py validate-transfer`; a stale, fabricated, malformed, cross-root, or incomplete receipt never transfers authority.

New Front Agent work uses the current class-free work protocol. The legacy protocol remains valid only for legacy packets that already contain authority classes. The gateway declares `packet` or `none` from the original request and local packet discovery. Main independently reclassifies the exact request and canonical root, then runs the helper read-only. Packet mode binds the current regular packet beneath `<root>/.planning`, packet format, packet and approval identity, coordinator epoch and generation, lifecycle status, and execution head. Sequence zero requires `approved`; updates carry current fencing and a lifecycle-appropriate status. Front validates structure and replay order; Main revalidates current packet reality before each mutation boundary. These fields are internal transport data and must not appear in normal user-facing prompts or receipts.

## Front and transfer integration

Front Agent always uses durable mode because it separates the human gateway from the implementing main agent. The gateway runs the packet workflow and carries packet identity and fencing in hidden transport metadata. Main validates that identity read-only, never writes the packet, and stops if the transport cannot preserve it. Current packet bindings are class-free; legacy bindings retain their historical classes only for compatibility.

Every new Front `work` message uses the closed [current work authority schema](work-authority-v2.schema.json); [work-authority v1](work-authority-v1.schema.json) is accepted only for legacy packets. Both bind the exact request and SHA-256, `alignment_mode: packet | none`, sequence, canonical root, approval, lifecycle, and fencing. Validate with `scripts/work_authority.py validate-work`; omitted, forged `none`, mixed-version, cross-root, symlinked, stale, or invalid-approval work fails closed. Every return keeps the same work ID, strictly increases sequence, and carries current fencing.

`planning_packet.py handoff` is the only transfer producer. It pauses the packet, clears runtime authority, increments coordinator fencing, and emits the closed [packet transfer receipt v1](packet-transfer-receipt-v1.schema.json). A summary or delivery without a current receipt validated by `scripts/work_authority.py validate-transfer` is informational only.

## Approval

After sealing, keep packet identity, repository root, revision, and digest in machine state. Ask for approval by describing the intended outcome and next actions, concrete write/read surfaces, exclusions, and any material external effect, risk, cost, or rollback implication. Do not normally expose machine receipts or ask the user to repeat them. Reveal only the minimum needed when the user requests audit details or an integrity ambiguity requires identifying the packet.

A plain, unambiguous approval in direct response is sufficient. Accept contextual language such as “yes,” “approve,” or “go ahead”; never prescribe an exact reply formula. Unless the user explicitly says to approve without starting, use that same message to record approval and transition immediately to execution with `--reuse-approval`. Do not ask a second “start?” question. If an older packet contains machine-oriented approval prose, translate it under this current rule instead of reproducing it.

Approval evidence in `state.json` is an audit record, not authenticated authority. For new approvals, record a concise, non-sensitive, single-line reference to the user event rather than quoting the message. `--reuse-approval` is valid only for trusted same-task continuity: the same visible Codex task, a valid packet/approval identity, matching coordinator state, no open question, and no out-of-envelope discovery. The helper checks structure, not conversational continuity; the coordinator must enforce this boundary.

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
