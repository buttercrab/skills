# Explore and Align

Read this reference when preparing the alignment question set. Converge as soon as the goal, requirements, non-goals, constraints and authority, tradeoff priorities, and acceptance checklist are complete.

## Inspect before asking

1. Inspect the authorized repository, docs, tests, runtime, logs, UI, or external evidence needed for the current uncertainty.
2. Separate observation, inference, working assumption, and unknown.
3. Resolve safely discoverable facts directly. Ask the user for intent, preference, authority, risk tolerance, completion evidence, or another choice evidence cannot settle.
4. Proactively frame a compact set of roughly three to seven high-value questions. Cover missing goal detail, must-have requirements, non-goals, acceptance evidence, constraints and authority, and tradeoff priorities. Include a recommended default when useful.
5. Do not ask the user to select architecture, files, dependencies, sequencing, fallbacks, or other implementation-plan details unless one is itself a user requirement or constraint.

Stateful tests, UI actions, connector calls, paid requests, and external reads with side effects are mutations, not discovery, and require matching authority.

## Converge after answers

Ask a focused follow-up when an answer creates a new material ambiguity. Every round must name the alignment gap it closes and the materially different consequences of the available answers. Do not impose a hard round count, but do not reopen questions merely because another implementation option exists.

User-delegated judgment closes non-authority questions. Stop questioning when the alignment contract can state the goal, requirements, non-goals, constraints and authority, and acceptance checklist without a decision-changing unknown.

## Persist only in durable mode

Before asking in durable mode, record each material observation in `facts.md`. After the answer, record the decision, meaningful options, rationale, consequences, provenance, contrary evidence, and remaining open questions in `decisions.md`. Ledger IDs are internal recovery aids; never make the user reference them.

Advance to the alignment contract when no decision-changing question remains, consequential assumptions are explicit, and the required acceptance evidence is clear. Durable mode also requires volatility labels and an alignment-round advancement verdict. Write the agent plan only after alignment approval.
