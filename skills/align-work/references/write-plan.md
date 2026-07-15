# Write the Plan

Read this reference after alignment closes and whenever review or new evidence requires replanning.

## Required content

Write `plan.md` so a fresh strong agent can reproduce the intended result using only the packet and referenced reality. Include:

- outcome and completion definition;
- consumed fact and decision IDs plus their execution-relevant content;
- current system/repository state and volatile rechecks;
- scope, non-goals, preservation boundaries, and authority classes;
- ordered step IDs, dependencies, ownership, and concrete file or system surfaces;
- exact verification commands/interactions, expected receipts, and required versus optional gates;
- risks, failure behavior, rollback, and external-action boundaries;
- model and delegation policy when relevant; and
- approval section defining requested authority classes and their exact scope. Display revision/digest from `state.json` after sealing; never insert them into protected `plan.md`.

Never write “as discussed above,” “use the prior context,” or any equivalent dependency on conversation history.

## Material-change rubric

Treat a change as material when it changes user-visible outcome or scope, architecture commitment, external authority, trust boundary, security/privacy/data handling, reversibility/risk tier, cost/time class, acceptance criteria, or required verification strength.

Treat reversible internal mechanics as nonmaterial only while they remain inside the approved files, scope, authority, outcome, risk, and gates. Record nonmaterial execution details in `execution.md` rather than editing the protected plan.

## Approval readiness

Before sealing, preflight the plan against current reality:

1. Verify every referenced path, symbol, command, entry point, and external surface that can be inspected safely.
2. Check dependency order and ensure each step's prerequisites exist before that step executes.
3. Map every requirement to at least one required gate and every gate to a concrete expected receipt.
4. Confirm each command or interaction is realistic from the stated working directory and environment.
5. Confirm requested authority covers every planned mutation and no step silently expands it.
6. Simulate one representative path read-only when that is cheap and materially tests executability.

Do not seal for approval until open decision-changing question IDs are empty, preflight defects are repaired, required gates have concrete receipts defined, and rollback and authority boundaries are explicit.
