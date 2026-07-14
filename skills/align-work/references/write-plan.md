# Write the Plan

Read this reference after alignment closes and whenever review or new evidence requires replanning.

## Required content

Write `plan.md` so a fresh strong agent can reproduce the intended result using only the packet and referenced reality. Include:

- outcome and completion definition;
- consumed fact and decision IDs plus their execution-relevant content;
- current system/repository state and volatile rechecks;
- scope, non-goals, preservation boundaries, authority classes, and exact authorized surfaces;
- architecture and fallback bounds, security/privacy/trust boundary, cost or time ceiling, required verification strength, and rollback or partial-work rules that form the approval envelope;
- ordered step IDs, dependencies, ownership, and concrete file or system surfaces;
- exact verification commands/interactions, expected receipts, and required versus optional gates;
- risks, failure behavior, rollback, and external-action boundaries;
- model and delegation policy when relevant; and
- approval section defining requested authority classes and their exact scope. Display revision/digest from `state.json` after sealing; never insert them into protected `plan.md`.

Never write “as discussed above,” “use the prior context,” or any equivalent dependency on conversation history.

## Approval-envelope rubric

Treat a change as outside the approved envelope when it adds outcome or scope, chooses an unplanned architecture, adds an authority class or surface, expands a trust/security/privacy/data boundary, raises reversibility or risk, exceeds an approved cost/time ceiling, weakens a required gate, or needs an unapproved rollback or partial-work disposition. Stop and obtain a new approval for those changes.

Keep retries, step reordering, reversible internal mechanics inside approved paths, named fallback branches inside their stated bounds, stronger verification, and ordinary in-scope bug fixes inside the envelope. When useful, list these bounded contingencies explicitly so execution can continue without another question.

Freeze `facts.md`, `decisions.md`, and `plan.md` after approval. Record in-envelope discoveries, mechanics, and receipts in `execution.md` rather than editing the protected snapshot. Change protected files only when the envelope must change or when repairing an integrity fault.

## Approval readiness

Do not seal for approval until open decision-changing question IDs are empty, required gates have concrete receipts defined, and every envelope boundary is explicit. Ask once for the exact sealed envelope. State that an unqualified approval starts execution immediately, so a second “start?” prompt is unnecessary.
