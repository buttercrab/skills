---
name: execute-goal-loop
description: Use when the user explicitly asks Codex to set or execute a goal, persist or iterate until measurable gates pass, or repeat plan, implementation, verification, and review cycles under an explicit loop contract. Compose with align-work when unresolved decisions or human approval are required, and with domain skills for technical mechanics. This skill does not replace either. Do not auto-trigger for ordinary bounded implementation, a standalone review, tests or quality requests alone, or a one-off commit, push, pull request, merge, deploy, or submission. Delivery actions belong to this skill only when explicitly authorized inside an active goal loop. For skill work, skill-creator owns skill mechanics.
---

# Execute Goal Loop

Use this skill to turn an open-ended task into a hard execution contract with real evidence. The point is not to keep working forever; it is to make "done" measurable, attack the biggest remaining gap, verify honestly, and repeat until the goal is complete or genuinely blocked.

Compose rather than compete. `align-work` owns unresolved decisions, durable plan approval, and reapproval; domain skills own technical mechanics; this skill owns explicit persistence and completion pressure. A goal cannot broaden the authority or scope owned by either.

## Goal Contract

When the user explicitly asks to set a goal, use Codex goal tools if available. Do not create a goal for ordinary tasks that only imply work.

Write the goal as one concrete objective with:

- **Outcome**: the user-visible or repo-visible result.
- **Scope**: the paths, product surfaces, branches, deploys, submissions, or artifacts involved.
- **Quality bar**: what must be true before stopping.
- **Verification gates**: required acceptance gates, optional strengthening checks, and the receipts each should produce.
- **Publish/submit gate**: each commit, push, PR, merge, deploy, or submission action must trace to explicit user authorization. A generated goal may preserve that authority but may not add or broaden it.
- **Stop rule**: complete only when every required gate passes; never treat an unavailable required gate as skipped-and-complete.

Prefer hard wording:

```text
Implement <specific slice> end to end in <repo/path>, verify with <tests/checks/UI/benchmarks>, run a critical review pass, fix any blocking findings, and perform only the explicitly authorized publish action if the evidence meets <threshold>.
```

Avoid vague wording:

```text
Improve the app as much as possible.
```

### Goal-tool lifecycle

1. Call `get_goal` before `create_goal`.
2. Create a goal only when the user explicitly requests one and `get_goal` confirms that no unfinished goal exists. Continue an unfinished goal that already covers the work. If it does not cover the work, do not replace it implicitly; report the conflict and request direction.
3. Set `token_budget` only when the user explicitly requests a budget.
4. Call `update_goal` with `complete` only after every required gate passes and no required work remains. For a budgeted goal, report the final token usage returned by the tool.
5. Call `update_goal` with `blocked` only after the same blocking condition persists for at least three consecutive goal turns, counting the originating turn, and no meaningful progress is possible without external input or state. After a blocked goal resumes, start a fresh three-turn audit. Do not leave a qualifying goal active while repeatedly reporting the same blocker.

## Loop

Run a bounded loop. Before each iteration, name one implementation slice, its required gates, and the current baseline. Each iteration must produce a changed artifact or new verification evidence.

1. **Inspect reality**: read the relevant files, docs, prior decisions, current UI, logs, failing tests, benchmark output, or live state before choosing work.
2. **Plan the gap**: identify the single highest-leverage gap against the goal, with a narrow implementation slice and explicit verification.
3. **Use independent review when useful**: for broad, ambiguous, risky, product-sensitive, or quality-sensitive work, use subagent/multi-agent tools only when they are available and authorized by user and system constraints. Define required reviewers before spawning. Otherwise perform clearly separated review passes yourself.
4. **Implement the slice**: keep edits scoped to the goal and existing repo patterns. Preserve user constraints such as read-only, no edits, no publish, or ask-before-submit.
5. **Verify with evidence**: run the chosen tests/checks. For UI/product work, include real browser, simulator, device, or Computer Use checks when available and relevant. For performance work, measure before/after and keep raw numbers.
6. **Review harshly**: run code review, UX review, verifier review, benchmark review, or devil's-advocate review against the original goal. Treat findings as blockers if they break the quality bar.
7. **Decide**: complete only if all required gates pass. Optional strengthening checks may be skipped only with a reason and residual-risk note. If a required gate is unavailable, keep the goal incomplete and apply the blocker rule. If an iteration produces no new evidence or improvement, replan once instead of repeating the same action; count the underlying blocker even when tactics differ.

## Verification Ladder

Choose the strongest practical evidence for the task. Do not accept a weaker gate when a stronger one is cheap and relevant. Record each required gate as `pass` or `fail` with its command, interaction, or artifact receipt; `skipped` is valid only for optional checks.

- **Code correctness**: unit tests, integration tests, typecheck, lint, targeted regression tests.
- **End-to-end behavior**: real CLI smoke, API request, browser flow, simulator/device interaction, generated artifact open/visual inspection.
- **UI/product quality**: screenshots, responsive viewports, actual interaction from the normal entry point, empty/error/loading states, accessibility-relevant checks where applicable.
- **Performance/solver quality**: stable benchmark harness, repeated baseline where useful, predefined improvement/no-regression thresholds, candidate comparison, platform result feedback.
- **Publish readiness**: clean worktree scope, CI checks, unresolved review threads, branch protection, deploy health, merged main when requested.

AI-driven checks and Computer Use are valid acceptance surfaces when they inspect the real app or artifact. They do not replace deterministic tests that are available and relevant.

For UI/product goals, do not treat app launch, rendered screens, protocol wiring, debug panes, or green tests as sufficient. The primary user workflow must work in the real interface.

For benchmark/performance goals, define the benchmark target, baseline command, environment, input size, raw-output capture, and minimum meaningful improvement before implementation. Reject gains that are inside measurement noise unless repeated runs support them.

## Subagents

Read [references/reviewer-prompts.md](references/reviewer-prompts.md) when the task needs reusable subagent prompts.

When authorized, use subagents for:

- gap planning on a large or ambiguous goal,
- harsh review after implementation,
- independent verification-plan critique,
- UX/product critique,
- performance or algorithm critique,
- read-only audits where edits are forbidden.

Pass subagents the minimum safe raw artifacts and task-local context they need. Do not pass secrets, unrelated private data, your intended answer, or a request to rubber-stamp the plan. Wait for every required review before synthesizing. If a required reviewer fails or is unavailable, retry safely or leave that review gate unpassed; never synthesize it as a pass.

## Progress Discipline

Keep the user informed without treating status as completion.

- State the current goal and active gate before long work.
- Maintain a short checklist for substantial goals.
- Record exact commands/checks run and their outcomes.
- Explain skipped optional checks and their residual risk. Treat an unavailable required gate as unpassed.
- Preserve unrelated user changes in the worktree.
- In read-only mode, retain the `audit-technical-work` evidence-surface boundary even when that skill is not the outer workflow: do not edit, generate, stage, commit, publish, submit, run stateful tests, or make side-effectful external calls. Pure in-memory evaluation is allowed only when it creates no persistent cache, bytecode, artifact, or external effect. Return findings, exact next edits, and verification gates.
- Never call a goal complete because time, tokens, or patience ran low.

## Completion Audit

Treat completion as unproven until a current requirement-to-receipt audit passes.

1. Re-derive the complete requirement set from the current goal, user request, approved plan or packet, named artifacts, and any accepted material revisions.
2. Give every required item a stable identifier and map it to authoritative current-state evidence at matching scope.
3. Reject a receipt when it comes from a superseded plan or revision, observes state that has since changed materially, proves only a narrower layer, or substitutes a mock for required live behavior.
4. Recheck volatile facts and cheap current-state gates immediately before completion.
5. Mark each item `pass`, `fail`, or `incomplete`. Missing, uncertain, indirect, inaccessible, or unaccounted evidence is not a pass.
6. Complete only when every required item passes, every blocking review finding is resolved or correctly refuted, and no required work remains.

## Completion Report

End with:

- what changed or what was learned,
- evidence that the goal gates passed,
- a required-gate-to-receipt table with no skipped required gate,
- remaining risk or unrun checks,
- publish/submission/merge status if applicable,
- exact blocker and next required input if not complete.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "execute-goal-loop"
- `routing_role`: "overlay"
- `portfolio_position`: "Persistence and iteration overlay for explicit measurable goal loops."
- `positive_request_classes`: ["explicit goal creation or execution","persist until measurable gates pass","repeat plan, implement, verify, and review cycles"]
- `triggers`: ["The user explicitly asks to set or execute a goal.","The user explicitly requests persistence or iteration until measurable gates pass."]
- `exclusions`: ["ordinary bounded work","standalone review or test","vague continue request","one-off delivery action"]
- `state_owner`: "Owns goal progress and completion pressure only; never owns user authority, packet state, or domain state."
- `precedence`: ["The selected outer workflow retains approval and mutation authority.","Domain skills retain technical mechanics."]
- `legal_compositions`: [{"route":"skill-creator","relation":"mechanics"},{"route":"propagate-contract-changes","relation":"mechanics"},{"route":"refactor-by-invariant","relation":"mechanics"}]
- `fallbacks`: [{"condition":"No explicit goal or loop contract exists.","route":"native-codex","result":"Use the applicable outer workflow without creating goal state."}]
- `forbidden_actions`: ["expand scope","bypass approval gates","replace Align, Audit, or domain mechanics","mark incomplete work complete"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
