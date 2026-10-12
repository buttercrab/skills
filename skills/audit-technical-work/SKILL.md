---
name: audit-technical-work
description: Audit technical claims, diagnose failures, or assess architecture and completion against current source and runtime evidence. Use for a bounded technical review; distinguish demonstrated defects from missing proof without silently applying fixes.
---

# Audit Technical Work

Answer the requested question with evidence at the same scope as the claim. A green unit test is evidence for that unit, not proof of a working deployment or complete user flow.

## Choose the evidence

- Establish the target revision, runtime, or artifact and the question being assessed. Inspect discoverable facts before asking questions; clarify only consequential scope or access ambiguities.
- Trace the relevant entry points, state changes, callers, configuration, and failure paths. Use source and actual behavior to check status reports rather than treating reports as independent verification.
- For completion audits, map each requested requirement to evidence and mark it satisfied, violated, or unverified. For a focused diagnosis, investigate the causal path instead of constructing a portfolio-wide ledger.
- Read the applicable section of [audit lenses](references/audit-lenses.md) for architecture, security, or completion work.

## Investigate without applying fixes

An audit permits inspection and proportionate local diagnostics. Ordinary tests, builds, and reproductions may create caches or temporary outputs; use an isolated workspace when they could change the reviewed checkout or data. Inspect unfamiliar test/setup commands for external effects before running them. A read-only request does not authorize migrations, live traffic changes, destructive fixtures, deployment, or editing the reviewed product.

For each candidate defect:

1. Find the concrete trigger, affected path, and incorrect result. Follow the caller to establish that the path is reachable.
2. Try the strongest plausible alternative explanation: intended compatibility, upstream validation, a guard elsewhere, or stale runtime state.
3. Reproduce when useful and permitted. Keep the command, revision, relevant output, and environment needed to repeat it; a speculative test suggestion is not an executed receipt.
4. Separate demonstrated behavior, inference, and unavailable evidence. Missing proof can block a completion claim without demonstrating a product bug.

Refresh volatile state when the conclusion depends on it. Report an inaccessible surface or unknown boundary explicitly; do not invent corroboration from a summary of the same original source.

## Report useful findings

Lead with the answer. Present supported findings in impact order, each with the failing condition, consequence, exact location, supporting evidence, and a focused correction or verification step. Severity describes impact; confidence describes evidence strength.

Include unresolved questions and inspected scope where they limit the answer. For completion audits, include the unmet or unverified requirements. Mention refuted candidates only when they explain a likely misunderstanding or important tradeoff. No finding is preferable to a speculative defect, but “no supported findings in the inspected scope” does not prove universal correctness.

If fixes are already authorized, use these findings to guide that work; do not create another approval ceremony. If the task is review only, report recommendations without applying them.
