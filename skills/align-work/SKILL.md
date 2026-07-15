---
name: align-work
description: Use as the outer alignment and approval workflow for coding work when the user explicitly invokes $align-work, an existing align-work packet must resume, scoped inspection finds unresolved decisions that materially change the accepted outcome, scope, architecture, authority, safety, or acceptance criteria, or work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating. Align exclusively owns packet state, approval, guarded transfer, and recovery. Under front-agent-orchestration, Front remains the human gateway while Align retains packet ownership. Read-only audits route to audit-technical-work. Domain skills provide mechanics and execute-goal-loop may overlay persistence, but neither changes authority. Do not auto-trigger for ordinary clear bounded coding, simple answers, or low-risk mechanical edits.
---

# Align Work

Turn approval-sensitive coding requests into a context-independent execution contract. Keep one state owner from discovery through verification; use the referenced stages rather than attempting to invoke other skills as an automatic pipeline.

## Classify the task

Use this workflow when any condition holds:

1. The user invokes `$align-work` or an existing packet must be resumed.
2. Scoped read-only inspection reveals an unresolved decision that can materially change the accepted outcome, scope, architecture, authority, safety, risk, acceptance criteria, or plan. Several dependent unresolved decisions strengthen the trigger, but step count alone does not.
3. The work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or writes to an external system, even if the requested action is clear and one-step.

Inspect only enough to classify safely. Uncertainty about complexity alone does not trigger this workflow. A read-only request alone is insufficient: use `audit-technical-work` for bounded technical audits, `map-technical-landscapes` for open-ended discovery, and `brief-linked-evidence` for fixed resource sets. Bypass this workflow for noncoding work, simple facts, ordinary clear bounded coding, and low-risk reversible mechanical edits.

Respect explicit precedence. A selected Front Agent gateway owns the human-facing conversation, but `align-work` remains the exclusive owner of packet state, approval, guarded transfer, and recovery. Never downgrade explicit `$align-work`, a matching packet, or another Align trigger because Front Agent is active. Do not create a second packet in the main session. The gateway must run this packet workflow and its approved `work` requirements must carry the exact packet path, task ID, revision, digest, authority classes, and coordinator fencing values. Main validates that identity read-only, never writes the packet, and stops if the transport cannot preserve it. Otherwise `align-work` owns the execution contract. Domain skills such as `skill-creator`, `refactor-by-invariant`, or `propagate-contract-changes` own only mechanics inside it. Use `execute-goal-loop` only when the user explicitly requests persistent iteration or approves a loop contract; the sealed packet remains canonical, goal state cannot broaden it, and material discoveries return to `align-work` reapproval.

Every Front `work` message uses the closed [work authority v1 schema](references/work-authority-v1.schema.json), includes the exact original request and its SHA-256, declares `alignment_mode: packet | none`, and starts at sequence zero. Main independently classifies the request and canonical root with `scripts/work_authority.py validate-work`; omitted, forged `none`, mixed-version, cross-root, symlinked, stale, or invalid-approval work is rejected. Packet acceptance binds `approved`, mutation progress binds `executing`, and final completion evidence binds `verifying`. Every return repeats the same work ID with a strictly increasing sequence and current fencing.

`planning_packet.py handoff` is the only transfer producer. It pauses the packet, clears runtime authority, increments coordinator fencing, and emits the closed [packet transfer receipt v1 schema](references/packet-transfer-receipt-v1.schema.json). A summary or delivery without a current receipt validated by `scripts/work_authority.py validate-transfer` is informational only.

## Establish the packet

Read [references/packet-contract.md](references/packet-contract.md) before creating, resuming, sealing, approving, or repairing a packet.

Create or resume exactly one packet at:

```text
<repo>/.planning/<task-id>/
```

Use `scripts/planning_packet.py`; do not hand-author `state.json`. Treat `facts.md` and `decisions.md` as the evidence and decision ledgers. Keep `plan.md` independently understandable and bind approval to its sealed packet revision.

If the user forbids all file creation or edits, do not create `.planning/`. Ask permission for the durable packet only when it is necessary; if permission is denied, remain read-only and state that durable resume and implementation are unavailable.

After compaction, interruption, coordinator transfer, or a fresh session, reconstruct task knowledge from the packet and revalidate volatile facts. A fresh session must ask the user to reauthorize before any mutation even if the packet records prior approval.

## Run the stages

1. **Explore and align:** read [references/explore-and-align.md](references/explore-and-align.md). Explore discoverable reality while asking only decision-changing questions. Update the packet before sending the next question round.
2. **Write the plan:** when no decision-changing question remains, read [references/write-plan.md](references/write-plan.md). Produce a self-contained plan with exact scope, authority, steps, gates, risks, and rollback.
3. **Review when warranted:** read [references/review-plan.md](references/review-plan.md). Prefer fresh adversarial review for complex or risky plans; record why a simple plan skipped it.
4. **Request approval:** seal the protected packet and show the user its revision, digest, and authority classes. Do not mutate product, repository, global, or external state before approval.
5. **Execute and verify:** after current-session approval, read [references/execute-approved-plan.md](references/execute-approved-plan.md). Record attempts, use bounded delegation, stop for material changes, and complete only when required gates have receipts.

## Enforce hard boundaries

- Never rely on conversation history for a material fact, decision, authority, step, or gate.
- Treat helper validation as structural integrity evidence, never proof of semantic completeness or authenticated human authority.
- Keep one active coordinator as the only canonical packet writer.
- Use direct children only. Begin every child assignment with: `You are a direct child. Do not spawn or delegate to any other agent.` Treat attempted subdelegation as an invalid result. Prefer read-only isolation for exploration and review; otherwise hash canonical files before and after each child run and reject mutated results.
- Ask the user only about decisions that can change outcome, scope, architecture, authority, safety, risk, acceptance criteria, or the plan. Discover safely inspectable facts instead.
- Treat packet approval as nonportable evidence. Reconfirm authority in every fresh session.
- Use cheap or fast models only for bounded, approved implementation. Use strong reasoning for alignment, planning, synthesis, adversarial review, high-risk work, and final verification.
- If a protected file changes after approval, invalidate approval. For a material change, stop new mutation, preserve partial work and receipts, record rollback options, revise the packet, and request reapproval.
- Do not escalate to a plugin, hook, MCP server, custom runtime, publication, deployment, or other external action without new authority.
- Before approval, prefer a read-only sandbox or read-only children. If the current surface still exposes write tools, record hashes for protected product/global surfaces and fail on unexpected mutation; instruction-level policy is not a technical sandbox.

## Report completion

Return the implemented outcome first, followed by required gate receipts, unrun optional checks and residual risk, packet status, and any remaining external action. Never call the task complete with a skipped or failed required gate.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "align-work"
- `routing_role`: "outer"
- `portfolio_position`: "Outer alignment, approval, and durable planning-packet workflow for authority-sensitive coding work."
- `positive_request_classes`: ["explicit Align invocation","matching packet resume","decision-changing coding ambiguity","destructive or irreversible work","production, security, privacy, costly, or external mutation"]
- `triggers`: ["The user explicitly invokes $align-work.","An existing matching Align packet must resume.","A material unresolved choice changes outcome, scope, architecture, authority, safety, or acceptance.","The work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating."]
- `exclusions`: ["ordinary clear bounded coding","simple answers","low-risk reversible mechanical edits","read-only technical audits"]
- `state_owner`: "Sole owner of Align packet state, coordinator fencing, approval, execution chain, guarded transfer, and recovery."
- `precedence`: ["Wins over domain mechanics when an Align trigger applies.","Under Front, Front remains the human gateway while Align retains exclusive packet ownership.","A goal loop never changes authority."]
- `legal_compositions`: [{"route":"front-agent-orchestration","relation":"gateway"},{"route":"execute-goal-loop","relation":"overlay"},{"route":"audit-technical-work","relation":"evidence-lens"},{"route":"skill-creator","relation":"mechanics"},{"route":"propagate-contract-changes","relation":"mechanics"},{"route":"refactor-by-invariant","relation":"mechanics"},{"route":"agent-mail","relation":"transport"},{"route":"write-task-handoff","relation":"content-owner"}]
- `fallbacks`: [{"condition":"No Align trigger applies.","route":"native-codex","result":"Use the native bounded workflow."},{"condition":"The request is a bounded read-only technical audit.","route":"audit-technical-work","result":"Audit owns the read-only outer contract."}]
- `forbidden_actions`: ["delegate packet mutation to Front, Handoff, Goal Loop, or domain skills","infer external authority","downgrade explicit Align or matching packet state"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
