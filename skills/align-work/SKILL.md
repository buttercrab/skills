---
name: align-work
description: Use as the outer alignment and approval workflow for coding when the user invokes $align-work, a material unresolved decision changes the outcome contract or authority, an existing Align packet resumes, or work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating. Default to lightweight alignment for local reversible work; inspect facts, proactively ask decision-changing questions with recommended defaults, align the goal, requirements, non-goals, constraints and authority, and observable acceptance invariants, then obtain one approval. After approval, let the agent own and revise implementation and verification mechanisms without reapproval. Use durable packet mode for existing packets, explicit continuity across sessions or agents, Front work when Align applies, or high-risk/external work. Reopen user alignment only when the approved outcome contract itself must change. Read-only audits route to audit-technical-work; domain skills own mechanics.
---

# Align Work

Align the outcome contract with the user, then let the agent own execution. The user approves the goal and completion boundary, not the implementation plan.

## Classify ownership and mode

Use Align when the user explicitly invokes `$align-work`, a material unresolved decision changes the accepted outcome or authority, an existing packet must resume, or the work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating. Cross-session or cross-agent execution triggers Align only when the user asks for durable shared alignment, continuity, recovery, or handoff; ordinary bounded delegation does not.

Explicit `$align-work` selects Align ownership, not durable mode by itself. A read-only request alone is insufficient: route bounded technical audits to `audit-technical-work`, open discovery to `map-technical-landscapes`, and fixed supplied resources to `brief-linked-evidence`. When Align is not explicitly invoked, bypass it for simple answers, ordinary clear bounded coding, and low-risk reversible mechanical edits. Uncertainty about complexity and step count alone do not trigger Align or durable mode.

Choose durable mode when any condition holds:

- a matching packet exists;
- the user asks for durable planning, resume, recovery, handoff, or alignment continuity spanning sessions or agents;
- the work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating; or
- Front Agent is the selected gateway for work that independently triggers Align. When Align applies under Front Agent, use durable mode. Front selection alone does not activate Align.

Otherwise use lightweight mode. Never downgrade explicit `$align-work` or a matching packet. Domain skills such as `skill-creator`, `refactor-by-invariant`, and `propagate-contract-changes` own mechanics only. `execute-goal-loop` is an explicit persistence overlay and cannot broaden Align authority.

## Use lightweight mode by default

Do not create `.planning/`, load packet machinery, or request adversarial review for lightweight work.

1. Inspect discoverable reality before questioning the user.
2. Proactively ask a compact set of roughly three to seven high-value questions when the answers are not already explicit. Cover the goal, must-have requirements, non-goals, acceptance evidence, constraints and authority, and tradeoff priorities. Include a recommended default when useful. Do not ask for discoverable facts or implementation-plan choices.
3. Ask a focused follow-up only when an answer creates a new material ambiguity. Each round must close named alignment gaps; stop questioning as soon as the alignment contract is complete.
4. Present one plain-language alignment contract containing the goal, requirements, non-goals, constraints and authority, and acceptance checklist. An unqualified approval authorizes the agent to plan and execute toward that contract immediately; do not ask a second “start?” question.
5. Own and revise the plan autonomously. Change architecture, files, dependencies, sequencing, fallbacks, tests, and internal rollback mechanics without user reapproval while the alignment contract remains satisfied. Return to the user only when the approved goal, requirements, non-goals, constraints or authority, or acceptance checklist must change or cannot all be honored.

Read [references/explore-and-align.md](references/explore-and-align.md) before preparing alignment questions. If interruption, transfer, or expanded risk makes durable recovery necessary, stop and escalate before further mutation.

## Escalate to durable mode when required

Read [references/packet-contract.md](references/packet-contract.md) before creating, resuming, sealing, approving, transferring, or repairing a packet. Create or resume exactly one packet at `<repo>/.planning/<task-id>/` with `scripts/planning_packet.py`; do not hand-author machine state. If durable mode is necessary but the user forbids its files, ask permission once and remain read-only if denied.

New durable packets use schema version 3. Use the durable stages:

1. Explore with [references/explore-and-align.md](references/explore-and-align.md) and persist material facts and decisions.
2. Write the user-facing contract with [references/write-alignment.md](references/write-alignment.md).
3. Seal the alignment and ask once for approval. Approval authorizes immediate agent planning and execution unless the user limits it.
4. Write and continuously maintain the agent-owned plan with [references/write-plan.md](references/write-plan.md).
5. Use [references/review-plan.md](references/review-plan.md) only when its durable-risk threshold is met; review never creates a user plan-approval gate.
6. Execute and verify with [references/execute-aligned-work.md](references/execute-aligned-work.md).

Existing schema-version 1 or 2 packets retain their legacy protected-file and `needs_reapproval` semantics. Resume them without silently migrating or weakening their recorded approval.

The Front gateway remains the human-facing interface while Align exclusively owns packet state, approval, guarded transfer, and recovery. Main validates packet identity read-only and never writes it. The packet contract contains the work-authority and transfer protocol details.

For durable Front work, load the [current work-authority schema](references/work-authority-v2.schema.json), the [legacy schema](references/work-authority-v1.schema.json) only for legacy packets, and the [packet-transfer receipt schema](references/packet-transfer-receipt-v1.schema.json) only for ownership transfer.

## Preserve alignment and execution boundaries

- Ask proactively about user intent, completion evidence, constraints, authority, and tradeoffs before approval. User-delegated judgment closes non-authority questions, and implementation details remain agent-owned.
- Seal observable invariants and minimum evidence strength, not agent-chosen proof mechanisms. The acceptance checklist is never an ordered implementation task list; if equally strong evidence can prove the same invariant, substitute it through the mutable plan without reapproval.
- Once approved, keep planning and execution autonomous. A changed plan is never an alignment event.
- Enter `needs_alignment` only when the approved alignment contract itself must change, is internally conflicting, or cannot be completed with the recorded authority. State the exact conflict or missing authority; do not ask the user to approve a revised plan.
- Exact destructive allowlists, named namespaces, publication or deployment targets, and other aligned external scopes remain literal. A live target outside them changes the alignment contract.
- In lightweight mode, restate material assumptions in the alignment contract. In durable schema version 3, `alignment.md` is the sole approval-bound artifact; facts, decisions, and plans remain coordinator-owned and mutable.
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
- `portfolio_position`: "Outer outcome-alignment and execution-approval workflow with a lightweight default and durable packet escalation for authority-sensitive coding work."
- `positive_request_classes`: ["explicit Align invocation","matching packet resume","decision-changing ambiguity in the goal, requirements, non-goals, constraints or authority, tradeoffs, or acceptance checklist","explicit durable, resumable, handoff, or continuity-preserving cross-session or cross-agent work","destructive or irreversible work","production, security, privacy, costly, or external mutation"]
- `triggers`: ["The user explicitly invokes $align-work.","An existing matching Align packet must resume.","A material unresolved choice changes the goal, requirements, non-goals, constraints or authority, tradeoff priorities, or acceptance checklist.","The work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating."]
- `exclusions`: ["ordinary clear bounded coding","simple answers","low-risk reversible mechanical edits","read-only technical audits"]
- `state_owner`: "Owns the user-approved alignment contract while the agent owns the mutable implementation plan; in durable mode Align is the sole owner of packet state, coordinator fencing, execution chain, guarded transfer, and recovery."
- `precedence`: ["Wins over domain mechanics when an Align trigger applies.","Under Front, when an Align trigger applies, Front remains the human gateway while Align uses durable mode and retains exclusive packet ownership.","A goal loop never changes authority."]
- `legal_compositions`: [{"route":"front-agent-orchestration","relation":"gateway"},{"route":"execute-goal-loop","relation":"overlay"},{"route":"audit-technical-work","relation":"evidence-lens"},{"route":"skill-creator","relation":"mechanics"},{"route":"propagate-contract-changes","relation":"mechanics"},{"route":"refactor-by-invariant","relation":"mechanics"},{"route":"agent-mail","relation":"transport"},{"route":"write-task-handoff","relation":"content-owner"}]
- `fallbacks`: [{"condition":"No Align trigger applies.","route":"native-codex","result":"Use the native bounded workflow."},{"condition":"The request is a bounded read-only technical audit.","route":"audit-technical-work","result":"Audit owns the read-only outer contract."}]
- `forbidden_actions`: ["delegate packet mutation to Front, Handoff, Goal Loop, or domain skills","infer external authority","create a durable packet solely because Align was explicitly invoked when no durable trigger applies","cap proactive alignment to one clarification round when material intent remains unresolved","ask the user to approve an implementation plan","reopen alignment solely because the agent-owned plan changes","seal an agent-chosen implementation or verification mechanism as an acceptance requirement","downgrade explicit Align or matching packet state"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
