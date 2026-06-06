---
name: execute-goal-loop
description: Use when the user asks Codex to set or execute a goal, loop, iterate until, plan then implement then review, use subagents for planning/review, be harsh/devil/critic, reach production-level quality, run hard tests/benchmarks/computer-use checks, complete an end-to-end task, or continue until commit/PR/merge/submission. Turns broad execution requests into measurable goal contracts and repeated plan/implement/verify/review loops.
---

# Execute Goal Loop

Use this skill to turn an open-ended task into a hard execution contract with real evidence. The point is not to keep working forever; it is to make "done" measurable, attack the biggest remaining gap, verify honestly, and repeat until the goal is complete or genuinely blocked.

## Goal Contract

When the user explicitly asks to set a goal, use Codex goal tools if available and no active goal already covers the work. Respect tool rules: do not create a goal for ordinary tasks that only imply work.

Write the goal as one concrete objective with:

- **Outcome**: the user-visible or repo-visible result.
- **Scope**: the paths, product surfaces, branches, deploys, submissions, or artifacts involved.
- **Quality bar**: what must be true before stopping.
- **Verification gates**: commands, UI checks, benchmarks, simulator/device checks, browser/computer-use checks, CI, or artifact inspection.
- **Publish/submit gate**: commit, PR, merge, deploy, or submission only when the user requested it or the current goal explicitly includes it.
- **Stop rule**: complete only when gates pass; blocked only after the same real blocker repeats and no meaningful progress remains.

Prefer hard wording:

```text
Implement <specific slice> end to end in <repo/path>, verify with <tests/checks/UI/benchmarks>, run a critical review pass, fix any blocking findings, and finish with <commit/PR/merge/submission/artifact> only if the evidence meets <threshold>.
```

Avoid vague wording:

```text
Improve the app as much as possible.
```

## Loop

Run a bounded loop. Each iteration should leave the system in a better, verified state.

1. **Inspect reality**: read the relevant files, docs, prior decisions, current UI, logs, failing tests, benchmark output, or live state before choosing work.
2. **Plan the gap**: identify the single highest-leverage gap against the goal, with a narrow implementation slice and explicit verification.
3. **Use independent review when useful**: for broad, ambiguous, risky, product-sensitive, or quality-sensitive work, use available subagent/multi-agent tools for planning and review. If no subagent tool is available, perform clearly separated review passes yourself.
4. **Implement the slice**: keep edits scoped to the goal and existing repo patterns. Preserve user constraints such as read-only, no edits, no publish, or ask-before-submit.
5. **Verify with evidence**: run the chosen tests/checks. For UI/product work, include real browser, simulator, device, or Computer Use checks when available and relevant. For performance work, measure before/after and keep raw numbers.
6. **Review harshly**: run code review, UX review, verifier review, benchmark review, or devil's-advocate review against the original goal. Treat findings as blockers if they break the quality bar.
7. **Decide**: complete if all gates pass; otherwise choose the next bounded slice and repeat. If blocked, document the exact blocker, attempts, and what external input/state is required.

## Verification Ladder

Choose the strongest practical evidence for the task. Do not accept a weaker gate when a stronger one is cheap and relevant.

- **Code correctness**: unit tests, integration tests, typecheck, lint, targeted regression tests.
- **End-to-end behavior**: real CLI smoke, API request, browser flow, simulator/device interaction, generated artifact open/visual inspection.
- **UI/product quality**: screenshots, responsive viewports, actual interaction from the normal entry point, empty/error/loading states, accessibility-relevant checks where applicable.
- **Performance/solver quality**: stable benchmark harness, repeated baseline where useful, predefined improvement/no-regression thresholds, candidate comparison, platform result feedback.
- **Publish readiness**: clean worktree scope, CI checks, unresolved review threads, branch protection, deploy health, merged main when requested.

AI-driven checks and Computer Use are valid acceptance surfaces when they inspect the real app or artifact. They do not replace deterministic tests that are available and relevant.

For UI/product goals, do not treat app launch, rendered screens, protocol wiring, debug panes, or green tests as sufficient. The primary user workflow must work in the real interface.

For benchmark/performance goals, define the benchmark target, baseline command, environment, input size, raw-output capture, and minimum meaningful improvement before implementation. Reject gains that are inside measurement noise unless repeated runs support them.

## Subagents

Read `references/reviewer-prompts.md` when the task needs reusable subagent prompts.

Use subagents for:

- gap planning on a large or ambiguous goal,
- harsh review after implementation,
- independent verification-plan critique,
- UX/product critique,
- performance or algorithm critique,
- read-only audits where edits are forbidden.

Pass subagents raw artifacts and the task-local context they need. Do not pass your intended answer or ask them to rubber-stamp your plan. Wait for all required reviews before synthesizing.

## Progress Discipline

Keep the user informed without treating status as completion.

- State the current goal and active gate before long work.
- Maintain a short checklist for substantial goals.
- Record exact commands/checks run and their outcomes.
- Explain skipped gates and why they were not applicable or could not run.
- Preserve unrelated user changes in the worktree.
- In read-only mode, do not edit, generate, stage, commit, publish, or submit; return findings, exact next edits, and verification gates.
- Never call a goal complete because time, tokens, or patience ran low.

## Completion Report

End with:

- what changed or what was learned,
- evidence that the goal gates passed,
- remaining risk or unrun checks,
- publish/submission/merge status if applicable,
- exact blocker and next required input if not complete.
