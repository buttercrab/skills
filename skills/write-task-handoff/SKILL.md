---
name: write-task-handoff
description: Create a self-contained, restartable handoff for a task moving across sessions, agents, context limits, or ownership boundaries. Use for an explicit handoff, continuation prompt, resume artifact, or transfer package. Handoff owns artifact content and export only. When an align-work packet exists, export from it; only Align may mutate, transfer, or recover the packet, and an actual transfer must be proven by a helper-produced transfer receipt. Agent Mail may transport the payload and Front Agent may coordinate delivery. Do not use for ordinary status summaries, current-task subagent coordination, or to grant mutation or publication authority.
---

# Write Task Handoff

Produce a restartable task artifact that a fresh executor can use without the conversation. Preserve canonical state and authority boundaries instead of creating a competing record.

## Select the source of truth

1. Identify the target executor, intended use, and durable destination if the user requested a file.
2. If an `align-work` packet exists, validate it and use it as canonical. Export a handoff from a sealed or approved packet without changing protected content. Only `align-work` may mutate, transfer, or recover its packet. This skill validates and consumes the helper-produced transfer receipt; it never runs the packet transfer itself. Only Align may run `planning_packet.py handoff`; this skill never invokes it. Do not create a second canonical ledger.
3. If a Front Agent pairing is active, compose the payload here but let that workflow own delivery through `front-agent send`; do not bypass its sender, direction, method, or human-confirmation fences with raw Agent Mail. Otherwise, when Agent Mail is requested, compose the payload here and let `agent-mail` own transport.
4. Treat prior approval as nonportable. State what a fresh executor must reauthorize before mutation.

Distinguish an informational export from an ownership transfer. An export reads current canonical state and creates no execution authority. For an actual coordinator or session transfer of an `align-work` packet, require Align's helper-produced `packet-transfer-receipt/v1` binding the expected revision, epoch, generation, old and new coordinator IDs, paused state, cleared runtime authority, and execution head. Resolve the installed Align skill from its loaded `SKILL.md` and run `python3 "$ALIGN_WORK_DIR/scripts/work_authority.py" validate-transfer --receipt <receipt.json> --repo <canonical-root>` read-only. If that receipt is absent, malformed, stale, cross-root, or invalid, label the transfer incomplete and give the fresh executor the guarded recovery and reauthorization path; never imply that a summary moved packet ownership.

## Reconstruct the task

Inspect current authoritative artifacts and include:

- goal and completion definition;
- scope, non-goals, constraints, and preservation boundaries;
- decisions, rationale, rejected alternatives, and unresolved choices;
- exact repository, branch, worktree, runtime, deployment, artifact, or external state;
- changed files and partial effects, classifying every dirty path as `owned`, `unrelated`, or `unknown` without hiding user work;
- completed checks with commands, interactions, receipts, and observation times;
- blockers, failures, unknowns, risks, and unrun checks;
- ordered next actions with dependencies and stopping conditions;
- volatile facts to recheck and authority required for future actions.

Separate observation, inference, assumption, and user decision. Use exact paths, identifiers, error text, versions, and hashes when they are safe and materially useful. Never include credentials, signed URLs, private tokens, or raw sensitive history.

Record an observation time and a reproducible snapshot marker such as a commit, packet revision/digest, manifest hash, or current-state command set. If inputs change while preparing the handoff, rerun affected checks and replace stale receipts rather than presenting mixed snapshots.

## Make restart possible

Write the handoff so it never depends on “as discussed above,” hidden chat context, or an executor guessing which state is current. Link to canonical artifacts instead of duplicating mutable detail when a link is sufficient. End with the first safe resume step and the checks that must precede it.

Creating or delivering the handoff does not authorize implementation, installation, publication, deployment, or destructive action. Report where the canonical state lives and whether delivery was merely prepared or actually completed by an authorized transport workflow.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "write-task-handoff"
- `routing_role`: "content"
- `portfolio_position`: "Restartable handoff artifact content and export workflow."
- `positive_request_classes`: ["explicit handoff","continuation prompt","resume artifact","transfer package"]
- `triggers`: ["The user explicitly asks for a restartable artifact across sessions, agents, context limits, or ownership boundaries."]
- `exclusions`: ["ordinary status summary","current-task subagent coordination","granting mutation or publication authority"]
- `state_owner`: "Owns handoff content and export only; Align exclusively owns packet mutation, transfer, and recovery."
- `precedence`: ["When an Align packet exists, export from it and consume a helper-produced transfer receipt for actual transfers.","Agent Mail owns transport and Front owns gateway delivery."]
- `legal_compositions`: [{"route":"agent-mail","relation":"transport"}]
- `fallbacks`: [{"condition":"Only a simple status summary is requested.","route":"native-codex","result":"Provide a native summary without a handoff workflow."}]
- `forbidden_actions`: ["mutate Align packet state","perform packet transfer or recovery","imply ownership transfer from export","carry portable execution authority"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
