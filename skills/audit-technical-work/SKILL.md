---
name: audit-technical-work
description: Perform bounded, read-only technical audits that verify architecture, implementation, or completion claims against current authoritative evidence and return severity-ordered findings with exact locations, missing proof, and explicit dispositions. Use as the outer evidence-and-reporting contract when the user explicitly asks for diagnosis, technical review, gap audit, or requirement-matched completion audit without authorizing fixes. Combine it with a domain skill when that skill supplies the audit lens. audit-technical-work owns read-only scope and reporting, while the domain skill owns technical criteria. Do not auto-trigger for provider-specific pull request review, UI-only visual QA, an active execute-goal-loop review or completion gate, or an align-work plan review.
---

# Audit Technical Work

Run a bounded audit without converting review authority into implementation authority. Prefer current source and runtime evidence over plans, status claims, or earlier receipts.

## Establish the audit contract

1. Restate the question, bounded scope, requested review dimensions, and expected output limit.
2. Inventory every claim, requirement, or acceptance criterion being audited. Preserve stable identifiers when the source provides them.
3. Record the permitted evidence surfaces and keep the task read-only. Treat stateful tests, external calls with side effects, generated-file updates, cleanup, and fixes as mutations requiring separate authority. Pure in-memory evaluation is permitted when it creates no persistent cache, bytecode, artifact, or external effect; record how that was ensured.
4. Name applicable domain skills. This skill owns evidence discipline and reporting; a domain skill may supply technical criteria without gaining mutation authority.

## Build the evidence map

1. Inspect the current source, tests, configuration, diff, generated artifacts, runtime state, logs, documentation, and external receipts needed for the declared scope.
2. Separate observed facts, supported inference, unresolved unknowns, and inaccessible surfaces.
3. Map every material claim or requirement to authoritative evidence at matching scope. A narrow unit check cannot prove an end-to-end requirement.
4. Reject evidence from superseded revisions, obsolete plans, changed volatile state, mocks standing in for required live behavior, or unverifiable summaries.
5. Attempt to disprove each apparent pass. Do not convert failure to find a problem into proof of correctness.

For architecture/ownership, security/privacy, or specification/completion auditing, read only the applicable section of [references/audit-lenses.md](references/audit-lenses.md).

## Adjudicate and report

Classify each requirement as `pass`, `fail`, or `incomplete`. Classify each candidate finding as `supported`, `refuted`, `duplicate`, `out-of-scope`, or `unresolved`; never silently omit an in-scope item.

Use severity for impact, not confidence: `blocker` prevents safe completion or invalidates the audit target, `high` breaks a core contract or safety boundary, `medium` causes material but bounded failure, and `low` is a limited defect. Use `fail` when current evidence demonstrates a requirement violation; use `incomplete` when required proof is missing or inaccessible without a demonstrated violation.

For every supported finding, provide:

- severity and affected requirement;
- hostile or failing trigger;
- observed unsafe or incorrect outcome;
- exact file, symbol, command, interaction, or receipt;
- evidence versus inference;
- concrete correction and the check that would verify it.

Answer the audit question first, then include requirement-to-evidence accounting, severity-ordered findings, refuted candidates when useful, inspected and uninspected scope, missing proof, and residual risk. Do not edit, stage, commit, publish, or imply that a proposed correction was applied.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "audit-technical-work"
- `routing_role`: "outer"
- `portfolio_position`: "Outer read-only technical audit and completion-accounting contract."
- `positive_request_classes`: ["diagnosis","architecture or implementation review","gap audit","requirement-matched completion audit without fix authority"]
- `triggers`: ["The user requests a bounded technical diagnosis or review without authorizing fixes.","Current authoritative evidence must be mapped to claims or requirements."]
- `exclusions`: ["authorized implementation or repair","provider-specific pull request review","UI-only visual QA","an active outer Align or Goal review gate"]
- `state_owner`: "Owns audit scope, finding severity, evidence mapping, dispositions, and pass/fail/incomplete accounting; owns no product state."
- `precedence`: ["Outer owner for standalone read-only technical audits.","Inside Align or Goal, supplies the evidence lens without creating a second outer workflow.","Prioritize Important Information may order audit findings by consequence without changing audit scope, severity, or proof requirements."]
- `legal_compositions`: [{"route":"front-agent-orchestration","relation":"gateway"},{"route":"execute-goal-loop","relation":"overlay"},{"route":"brief-linked-evidence","relation":"content-owner"},{"route":"prioritize-important-information","relation":"content-owner"},{"route":"propagate-contract-changes","relation":"mechanics"},{"route":"refactor-by-invariant","relation":"mechanics"}]
- `fallbacks`: [{"condition":"The user authorizes fixes and an Align trigger applies.","route":"align-work","result":"Align owns approval and mutation."},{"condition":"The user authorizes an ordinary bounded fix without an Align trigger.","route":"native-codex","result":"Use native bounded implementation."}]
- `forbidden_actions`: ["implement fixes","mutate packet or product","claim proof outside inspected scope"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
