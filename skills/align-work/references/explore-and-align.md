# Explore and Align

Read this reference only when a decision-changing ambiguity remains. Converge as soon as evidence and delegated judgment support a bounded recommendation.

## Inspect before asking

1. Inspect the authorized repository, docs, tests, runtime, logs, UI, or external evidence needed for the current uncertainty.
2. Separate observation, inference, working assumption, and unknown.
3. Resolve safely discoverable facts directly. Ask only for intent, preference, authority, risk tolerance, or another choice evidence cannot settle.
4. Frame the smallest question set whose answers can materially change outcome, scope, architecture, authority, safety, risk, acceptance criteria, or the approval envelope.

Stateful tests, UI actions, connector calls, paid requests, and external reads with side effects are mutations, not discovery, and require matching authority.

## Converge after the answer

Lightweight mode permits at most one clarification round. After the answer, present the best bounded recommendation with its assumptions. Do not reopen exploration merely because another option exists. If authority or safety remains genuinely unresolved, state the single blocker; do not manufacture a second round.

User-delegated judgment closes non-authority questions. A further round is permitted only in durable mode, and only when the coordinator can name the unresolved decision, the materially different consequences of its options, and why a safe assumption cannot resolve it.

## Persist only in durable mode

Before asking in durable mode, record each material observation in `facts.md`. After the answer, record the decision, meaningful options, rationale, consequences, provenance, contrary evidence, and remaining open questions in `decisions.md`. Ledger IDs are internal recovery aids; never make the user reference them.

Advance to the plan when no decision-changing question remains, consequential assumptions are explicit, and the evidence is sufficient for the mode's approval envelope. Durable mode also requires volatility labels and an alignment-round advancement verdict. There is no minimum number of rounds in either mode.
