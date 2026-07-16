# Write the Plan

Read this reference after alignment closes and whenever review or new evidence requires replanning.

## Required content

Write `plan.md` so a fresh strong agent can reproduce the intended result using only the packet and referenced reality. Include:

- outcome and completion definition;
- execution-relevant evidence and decisions restated in plain language, without a visible ledger-ID manifest;
- current system/repository state and volatile rechecks;
- scope, non-goals, preservation boundaries, and exact authorized surfaces described in concrete language;
- architecture and fallback bounds, security/privacy/trust boundary, cost or time ceiling, required verification strength, and rollback or partial-work rules that form the approval envelope;
- descriptively titled implementation steps, dependencies, ownership, and concrete file or system surfaces;
- exact verification commands/interactions, expected receipts, and required versus optional gates;
- risks, failure behavior, rollback, and external-action boundaries;
- model and delegation policy when relevant; and
- approval-scope section describing what approval permits and excludes in plain language.

Never write “as discussed above,” “use the prior context,” or any equivalent dependency on conversation history.

Keep stable fact, decision, round, and step identifiers in internal ledgers and machine state. Do not require a reader of `plan.md` to decode or repeat them.

## Approval-envelope rubric

Write the envelope to authorize the outcome and its material boundaries, not to freeze every implementation detail. Reapproval is exceptional. Treat a change as outside the envelope only when the executor can name concrete new user authority it needs: a new externally visible outcome or unauthorized system/repository surface; a destructive or irreversible action not already approved; a wider trust/security/privacy/data boundary; a higher approved cost or time ceiling; a weakened required gate; or an unapproved rollback or partial-work disposition. A difference from the plan text, file list, architecture, dependency choice, or step sequence is insufficient by itself.

Keep scope-neutral file changes, internal architecture or refactors, implementation substitutions, bounded dependency adjustments within the approved trust boundary, retries, step insertion or removal, step reordering, reversible mechanics, named fallback branches inside their stated bounds, stronger verification, and ordinary in-scope bug fixes inside the envelope. If classification is uncertain, continue when the change is local or otherwise authorized, reversible, preserves the outcome and acceptance gates, and does not widen external effects, trust, risk, or cost. List only genuinely material exclusions; do not enumerate every permissible contingency.

Treat exact destructive allowlists, named namespaces, publication or deployment targets, and other sealed external scopes literally. A live target outside an exact set always needs new approval rather than an inferred expansion.

Freeze `facts.md`, `decisions.md`, and `plan.md` after approval. Record in-envelope discoveries, operational plan deltas, mechanics, and receipts in `execution.md` rather than editing the protected snapshot or seeking approval merely to make the snapshot match execution. Change protected files only when new authority changes the envelope or when repairing an integrity fault.

## Approval readiness

Before sealing, preflight the plan against current reality:

1. Verify every referenced path, symbol, command, entry point, and external surface that can be inspected safely.
2. Check dependency order and ensure each step's prerequisites exist before that step executes.
3. Map every requirement to at least one required gate and every gate to a concrete expected receipt.
4. Confirm each command or interaction is realistic from the stated working directory and environment.
5. Confirm the described approval scope covers every planned mutation and no step silently expands it.
6. Simulate one representative path read-only when that is cheap and materially tests executability.

Do not seal for approval until open decision-changing question IDs are empty, preflight defects are repaired, required gates have concrete receipts defined, and every scope, rollback, and external-effect boundary is explicit. Ask once in plain language for the concrete outcome, actions, boundaries, and material effects. State that an unqualified approval starts execution immediately, so a second “start?” prompt is unnecessary. Never prescribe an exact reply or surface the sealed machine receipt unless the user requests it or integrity disambiguation requires it.
