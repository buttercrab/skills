---
name: align-work
description: Use as the outer alignment and approval workflow for coding when the user invokes $align-work, a material decision changes outcome or authority, an existing Align packet resumes, or work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, externally mutating, cross-session, or cross-agent. Default to lightweight alignment with no packet for local reversible work; inspect enough, ask at most one decision-changing clarification round, present one approval-ready recommendation, and execute on approval. Escalate to durable packet mode for existing packets or the listed continuity and risk triggers. Align owns approval and any packet state; front-agent-orchestration remains the human gateway and always uses durable mode. Read-only audits route to audit-technical-work. Domain skills own mechanics and execute-goal-loop may overlay persistence. Do not auto-trigger for ordinary clear bounded coding, simple answers, or low-risk mechanical edits unless explicitly invoked.
---

# Align Work

Align only as much as the work requires. Keep one approval owner, but do not make routine alignment pay the cost of durable recovery machinery.

## Classify ownership and mode

Use Align when the user explicitly invokes `$align-work`, a material unresolved decision changes the accepted outcome or authority, an existing packet must resume, or the work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, externally mutating, cross-session, or cross-agent.

Explicit `$align-work` selects Align ownership, not durable mode by itself. A read-only request alone is insufficient: route bounded technical audits to `audit-technical-work`, open discovery to `map-technical-landscapes`, and fixed supplied resources to `brief-linked-evidence`. When Align is not explicitly invoked, bypass it for simple answers, ordinary clear bounded coding, and low-risk reversible mechanical edits. Uncertainty about complexity and step count alone do not trigger Align or durable mode.

Choose durable mode when any condition holds:

- a matching packet exists;
- the user asks for durable planning, resume, recovery, handoff, or work spanning sessions or agents;
- the work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating; or
- Front Agent is the selected gateway. Front Agent always uses durable mode.

Otherwise use lightweight mode. Never downgrade explicit `$align-work` or a matching packet. Domain skills such as `skill-creator`, `refactor-by-invariant`, and `propagate-contract-changes` own mechanics only. `execute-goal-loop` is an explicit persistence overlay and cannot broaden Align authority.

## Use lightweight mode by default

Do not create `.planning/`, load packet machinery, or request adversarial review for lightweight work.

1. Inspect only enough discoverable reality to identify the decision and a safe recommendation.
2. Ask nothing when the answer is discoverable or the user delegated judgment. Otherwise ask one concise round containing only questions that materially change outcome, authority, safety, or acceptance.
3. After the answer, converge. Do not ask a second lightweight clarification round. Present the best bounded recommendation with explicit assumptions; if authority or safety still blocks action, state the single blocker instead of reopening exploration.
4. Present one plain-language approval envelope covering outcome, concrete scope, relevant architecture or fallback, verification, external effects, and rollback. An unqualified approval starts execution immediately; do not ask a second “start?” question.
5. Implement and verify within the approved envelope. Stop for a new approval only if outcome, scope, authority, trust, material risk, required gates, or partial-work disposition changes.

Read [references/explore-and-align.md](references/explore-and-align.md) only when a decision-changing ambiguity remains. If interruption, transfer, or expanded risk makes durable recovery necessary, stop and escalate before further mutation.

## Escalate to durable mode when required

Read [references/packet-contract.md](references/packet-contract.md) before creating, resuming, sealing, approving, transferring, or repairing a packet. Create or resume exactly one packet at `<repo>/.planning/<task-id>/` with `scripts/planning_packet.py`; do not hand-author machine state. If durable mode is necessary but the user forbids its files, ask permission once and remain read-only if denied.

Use the durable stages:

1. Explore with [references/explore-and-align.md](references/explore-and-align.md) and persist material facts and decisions.
2. Write the self-contained plan with [references/write-plan.md](references/write-plan.md).
3. Use [references/review-plan.md](references/review-plan.md) only when its durable-risk threshold is met.
4. Seal the packet and ask once for the plain-language approval envelope. Approval authorizes immediate execution unless the user limits it to planning.
5. Execute and verify with [references/execute-approved-plan.md](references/execute-approved-plan.md).

The Front gateway remains the human-facing interface while Align exclusively owns packet state, approval, guarded transfer, and recovery. Main validates packet identity read-only and never writes it. The packet contract contains the work-authority and transfer protocol details.

For durable Front work, load the [current work-authority schema](references/work-authority-v2.schema.json), the [legacy schema](references/work-authority-v1.schema.json) only for legacy packets, and the [packet-transfer receipt schema](references/packet-transfer-receipt-v1.schema.json) only for ownership transfer.

## Preserve approval and execution boundaries

- Ask only about decisions that can materially change outcome, scope, architecture, authority, safety, risk, acceptance criteria, or the plan. User-delegated judgment closes non-authority questions.
- In lightweight mode, restate material assumptions in the approval envelope. In durable mode, the packet is canonical and protected planning files freeze after approval.
- Treat helper validation as structural integrity evidence, never authenticated human authority or semantic proof.
- Keep machine receipts internal. Do not make the user repeat packet IDs, digests, ledger IDs, or approval IDs.
- Use direct children only. Begin every child assignment with: `You are a direct child. Do not spawn or delegate to any other agent.` Reject attempted subdelegation and unexpected canonical-file mutation.
- Do not infer external authority or escalate to a plugin, hook, MCP server, custom runtime, publication, deployment, or other external action without matching approval.
- Report the implemented outcome first, required verification results next, then optional checks, residual risk, durable packet status when applicable, and remaining external actions. Never claim completion with a skipped or failed required gate.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "align-work"
- `routing_role`: "outer"
- `portfolio_position`: "Outer alignment and approval workflow with a lightweight default and durable packet escalation for authority-sensitive coding work."
- `positive_request_classes`: ["explicit Align invocation","matching packet resume","decision-changing coding ambiguity","explicit durable, resumable, handoff, cross-session, or cross-agent work","destructive or irreversible work","production, security, privacy, costly, or external mutation"]
- `triggers`: ["The user explicitly invokes $align-work.","An existing matching Align packet must resume.","A material unresolved choice changes outcome, scope, architecture, authority, safety, or acceptance.","The work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating."]
- `exclusions`: ["ordinary clear bounded coding","simple answers","low-risk reversible mechanical edits","read-only technical audits"]
- `state_owner`: "Owns the Align approval envelope; in durable mode it is the sole owner of packet state, coordinator fencing, execution chain, guarded transfer, and recovery."
- `precedence`: ["Wins over domain mechanics when an Align trigger applies.","Under Front, Front remains the human gateway while Align uses durable mode and retains exclusive packet ownership.","A goal loop never changes authority."]
- `legal_compositions`: [{"route":"front-agent-orchestration","relation":"gateway"},{"route":"execute-goal-loop","relation":"overlay"},{"route":"audit-technical-work","relation":"evidence-lens"},{"route":"skill-creator","relation":"mechanics"},{"route":"propagate-contract-changes","relation":"mechanics"},{"route":"refactor-by-invariant","relation":"mechanics"},{"route":"agent-mail","relation":"transport"},{"route":"write-task-handoff","relation":"content-owner"}]
- `fallbacks`: [{"condition":"No Align trigger applies.","route":"native-codex","result":"Use the native bounded workflow."},{"condition":"The request is a bounded read-only technical audit.","route":"audit-technical-work","result":"Audit owns the read-only outer contract."}]
- `forbidden_actions`: ["delegate packet mutation to Front, Handoff, Goal Loop, or domain skills","infer external authority","create a durable packet solely because Align was explicitly invoked when no durable trigger applies","repeat lightweight clarification without a named unresolved decision that changes the approval envelope","downgrade explicit Align or matching packet state"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
