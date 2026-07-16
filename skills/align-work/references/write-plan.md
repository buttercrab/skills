# Write and Maintain the Agent Plan

Read this reference after the alignment contract is approved. The plan belongs to the agent and is never a user-approval artifact.

## Required content

Write `plan.md` so a fresh strong agent can continue execution against `alignment.md`. Include:

- the current execution objective;
- execution-relevant state, assumptions, and volatile rechecks;
- current architecture, implementation strategy, and bounded fallbacks;
- descriptively titled steps, dependencies, ownership, and current file or system surfaces;
- a mapping from every alignment acceptance check to concrete verification and expected evidence;
- risks, failure behavior, rollback mechanics, and preservation measures; and
- model and delegation policy when relevant.

Never write “as discussed above,” “use the prior context,” or another dependency on conversation history. Keep stable fact, decision, round, and step identifiers in internal ledgers and machine state.

## Autonomous revision

Continuously revise `plan.md` as evidence changes. Architecture, files, dependencies, sequencing, fallbacks, tests, internal rollback mechanics, retries, and ordinary in-scope fixes are agent-owned decisions. Updating them never requires user approval and never changes the protected alignment digest.

When new evidence reveals that the approved alignment cannot be satisfied, do not disguise a contract change as planning. Enter `needs_alignment`, state the exact conflict or missing authority, and follow the alignment-change path.

## Preflight

Before execution:

1. Verify every referenced path, symbol, command, entry point, and external surface that can be inspected safely.
2. Check dependency order and ensure each step's prerequisites exist.
3. Map every acceptance check to at least one required gate and every gate to expected evidence.
4. Confirm each command or interaction is realistic from the stated working directory and environment.
5. Simulate one representative path read-only when cheap and materially useful.

Keep the plan current enough for recovery, but do not stop productive execution merely to make prose mirror every tactical adjustment. Record material actions and receipts in `execution.md`.
