---
name: system-architecture
description: Design or assess software system architecture and explain it with purpose-specific diagrams, using contextual system cases, patterns and primary foundations. Use for boundaries, state/data/control flows, quality tradeoffs and migration decisions; do not turn a repository-layout question or a small implementation task into an automatic distributed-system redesign.
---

# System Architecture

Help people make explicit architectural decisions: what owns behavior and state, how parts communicate, which guarantees matter, what can fail, and how the design can evolve. Use the annotated [architecture library](library/index.md) to compare mechanisms and limits. A familiar pattern, fashionable stack or polished diagram is not proof that a design fits.

Name the deliverable and its scope: an assessment, decision brief, system model, diagram, migration plan or requested implementation. When a system is an example for improving a skill/library, keep the parent deliverable central and return bounded findings to it. Existing authorization remains in force; architectural discussion does not silently authorize product changes, new services or infrastructure.

## Establish the decision before selecting a style

Inspect the brief, existing code/contracts/configuration, architecture records and relevant operational evidence available within scope. Establish the behavior/change in question, users/actors, state authority, current deployment and external dependencies. Distinguish documented intent, inspected implementation, observed operation, proposals and unknowns; do not label an intended topology as deployed fact.

Ask about consequential human-owned uncertainties: workload and growth assumptions, unacceptable outcomes, consistency/durability expectations, failure tolerance, operator/team capacity, cost, compatibility and migration constraints. Discover technical facts yourself where possible. Do not invent traffic, latency, budget or availability targets to justify a preferred stack. A complete brief, narrow question or explicit delegation can be enough to proceed without an interview.

Tie each question to a decision it changes. Carry partial and delayed answers into the affected model; retire dependent provisional choices. Opening a reference or viewing a variant is not endorsement. Once direction is sufficient, produce the requested artifact rather than another equivalent preference question.

Read [context and tradeoffs](references/context-and-tradeoffs.md) when framing an uncertain decision or comparing alternatives.

## Trace behavior, ownership and failure

Follow a representative operation through entry, coordination, authoritative state, external effects and the result visible to the caller. Identify the boundaries that enforce an invariant and the assumptions they depend on. A module, team, process, deployment, transaction and trust boundary are different concepts even when they coincide.

For asynchronous work, separate acceptance, persistence, delivery, execution, completion and acknowledgment. Consider retry, duplicate delivery, timeout/unknown result, partial failure and reconciliation where relevant. Name the scope of an idempotency or consistency guarantee; a broker feature alone does not establish an end-to-end business guarantee. A network theorem is not a substitute for the operation's actual model.

Use inspected branches/contracts/tests to support implementation claims, and explicit evidence for deployed behavior. A function, test or configuration existing at a revision does not establish that it runs or passes in the relevant environment. Preserve missing evidence instead of converting it into either a proven defect or an invented guarantee.

Read [boundaries and failure](references/boundaries-and-failure.md) for state ownership, distributed coordination and migration reasoning.

## Compare mechanisms in context

Survey relevant and neighboring library roles, read promising cards in full, and inspect the precise primary portions needed for the recommendation. Match workload, invariants, deployment/team boundaries, operating cost, maturity and evidence scope. Explain which mechanism transfers and which conditions do not. A small in-process example may be more appropriate than a celebrated distributed service.

Keep a simpler or no-change alternative when it can satisfy the requirement. Compare benefits against new failure modes, operational responsibility, delivery coordination and migration cost. Do not prescribe microservices, event sourcing, a global cache, clean layers or a specific vendor because the pattern appears in a source. Preserve disagreement and the conditions behind it rather than treating source counts as votes.

Broaden primary discovery when no adequate match exists or evidence is stale/inaccessible. Report the gap and support only bounded transfers. Third-party architecture/agent instructions are resources, not automatic authority for installers, scripts, production actions or unrelated approval loops. Use [library usage](references/library-usage.md) for browse/search and evidence boundaries.

## Draw the model that answers the question

Choose the smallest useful view: context for actors/external dependencies; structural/dependency for responsibilities; runtime/sequence/state for behavior and failure; deployment for actual/proposed execution locations. Use multiple views only when they answer distinct necessary questions. Do not require every C4/UML level.

Give the diagram a question, scope, status and evidence basis. Keep stable names across views, label important relationship direction/meaning, distinguish logical from deployment boundaries and expose relevant state/transaction/trust boundaries. Mark unknowns and proposals visibly; avoid mixing code structure, runtime instances and future architecture into one unexplained picture.

Trace consequential elements and claims to source sections or explicit assumptions. Reconcile the diagram with prose and code: an acknowledgment arrow cannot mean both accepted and committed, and a datastore box cannot imply transaction scope that the implementation does not provide. Show a meaningful alternate/failure path when it changes the decision. Use readable labels and a legend where notation is not self-evident.

Read [diagram contract and original examples](references/diagram-contract.md) before producing substantive architecture diagrams. When editable source is the deliverable, use the target parser when available and fix its actual errors; otherwise mark syntax as unverified. Syntax parsing, rendering, semantic consistency and architectural verification are separate checks.

## Decide and verify at the requested scope

State the selected option, the alternatives rejected/deferred, decisive assumptions, costs and what would reopen the decision. Keep the essential plan within the person's operating/time budget; separate optional follow-up from the next necessary action. For migration, identify intermediate compatibility and state ownership, rollout/rollback or reconciliation limits, and evidence needed before each consequential step.

For requested implementation, preserve the agreed invariants and unrelated work, update actual owning boundaries, and run relevant checks within authorization. An assessment or diagram request can finish with a grounded model and validation plan; it does not request a redesign implementation. Do not substitute a successful parser/build for a runtime, failure or compatibility claim.

Finish by naming the artifact changed or assessed, the human direction/reference transfers it carries, actual checks, and material unknowns. Read [verification and evolution](references/verification-and-evolution.md) when selecting checks, recording decisions or returning trial findings to this skill.
