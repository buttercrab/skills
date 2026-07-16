# Alignment Packet Contract

This reference is durable-mode only. Read it before creating, resuming, sealing, approving, transferring, or repairing a packet.

## Schema version 3

Schema version 3 is the default for new packets. It separates user alignment from agent planning:

- `alignment.md`: the sole approval-bound artifact. It contains the goal, requirements, non-goals, constraints and authority, and acceptance checklist.
- `facts.md`: coordinator-owned evidence, inference, unknowns, and volatility notes. It may evolve after approval.
- `decisions.md`: coordinator-owned questions, answers, rationale, provenance, and alignment rounds. It may evolve after approval.
- `plan.md`: the mutable agent execution plan. It may change at any time without user approval while `alignment.md` remains satisfied.
- `state.json`: machine state, packet and repository identity, alignment revision and digest, open questions, coordinator fencing, approval evidence, and execution-chain head. Never edit it manually.
- `execution.md`: hash-chained attempt and resume ledger created when execution starts or aligned work first enters `needs_alignment`.

For version 3, `protected_digest` is the SHA-256 digest of `alignment.md` only. Approval binds packet identity, repository root, alignment revision, and that digest. Changes to facts, decisions, or plan do not clear approval or change the digest. The helper still validates their structure and task identity.

Before execution, replace the required-content marker in `plan.md` with an agent-authored plan. This is execution readiness, not a user approval gate.

## Legacy packet compatibility

Schema versions 1 and 2 remain valid only for existing packets. Do not silently migrate them.

- Version 2 is class-free but preserves the historical digest over `decisions.md`, `facts.md`, and `plan.md`, plus the `needs_reapproval` lifecycle.
- Version 1 also preserves that historical digest and retains `requested_authority_classes` plus approval `authority_classes`. Its legacy parser accepts `P`, `R`, `T`, `I`, `G`, `E`, and `D`, each optionally followed by digits.

For legacy version 1 only, resealing may use `--authority` with the intended comma-separated values. Do not use authority codes for versions 2 or 3.

## Core commands

```bash
python3 scripts/planning_packet.py init --repo <repo> --task-id <slug> --title <title>
python3 scripts/planning_packet.py validate <packet>
python3 scripts/planning_packet.py questions <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --set Q-001
python3 scripts/planning_packet.py seal <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --status awaiting_approval
python3 scripts/planning_packet.py transition <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --to approved --approval-id <uuid> --approval-evidence <text>
python3 scripts/planning_packet.py transition <packet> --expected-revision <n> --expected-epoch <n> --expected-generation <n> --coordinator-id <uuid> --to executing --reuse-approval
```

Use `handoff` for orderly coordinator transfer and `recover` only after the user authorizes takeover from an unavailable coordinator. A transfer during active work pauses the packet and clears runtime authorization. The same explicit recovery/resume message may authorize takeover and resume; never ask twice.

Use `repair` only for protected alignment digest mismatch, invalid state, or a recognized pending-attempt fault. In version 3, ordinary edits to facts, decisions, or plan do not require repair.

## Approval and alignment renewal

Ask the user to approve the plain-language `alignment.md` contract, never the implementation plan. A contextual approval such as “yes,” “approve,” or “go ahead” is sufficient. Unless the user limits approval to alignment only, use that same message to authorize agent planning and execution; do not ask a second “start?” question.

Approval evidence is an internal audit record, not authenticated authority. Store a concise, non-sensitive, single-line reference to the user event. Keep packet identity, revision, digest, approval ID, and ledger IDs out of normal user prompts.

Version 3 enters `needs_alignment` only when the approved goal, requirements, non-goals, constraints or authority, or acceptance checklist must change or cannot all be honored. Preserve partial effects, revise only the alignment contract that actually changed, repair and reseal it, and ask once for the exact delta and partial-work disposition. Never enter `needs_alignment` for a plan change.

Legacy versions retain `needs_reapproval` and their historical protected-plan behavior.

## Resume

1. Validate packet structure, protected digest, and execution chain.
2. Confirm the exact packet path and task ID; do not guess among multiple packets.
3. Read volatile-fact rechecks, the current mutable plan, and `execution.md`; identify incomplete attempts.
4. Determine continuity. Compaction or a later turn in the same visible Codex task may reuse a valid approval. A fresh task requires an explicit continue/resume/implement instruction, which is itself reauthorization.
5. Acquire, hand off, or recover coordinator ownership with the expected fencing epoch.
6. Revalidate facts and compare current reality to `alignment.md`.
7. Reconcile partial mutations, refresh the agent plan, and continue without asking for plan approval.

If protected alignment bytes disagree with the stored digest, stop ordinary mutation and use guarded repair. A version-3 plan change never creates this condition.

Execution markers are the authoritative hash-chained records. Every marker binds packet identity, alignment revision, protected digest, and approval ID. Completion requires a final passed verification record bound to the current approved alignment revision.

## Front and transfer integration

Front Agent always uses durable mode because it separates the human gateway from the implementing main agent. The gateway runs the packet workflow; Main validates packet identity read-only and never writes the packet.

New Front work uses [work-authority v2](work-authority-v2.schema.json), which accepts class-free packet schema versions 2 and 3. Legacy packet schema version 1 uses [work-authority v1](work-authority-v1.schema.json). Both bind the request, canonical repository root, packet and approval identity, lifecycle, fencing, and execution head. Version 3 binds the alignment-only protected digest.

Every `handoff` emits a closed [packet-transfer receipt v1](packet-transfer-receipt-v1.schema.json). Validate it against current packet reality with `scripts/work_authority.py validate-transfer`; stale, fabricated, malformed, cross-root, or incomplete receipts never transfer authority.
