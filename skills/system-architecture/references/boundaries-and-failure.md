# Boundaries, state and failure reasoning

Use this when evaluating responsibility boundaries, coordination, persistent state or migration. Follow one operation end to end before multiplying components.

## Make boundaries meaningful

Name what each boundary owns: a change-prone decision, public contract, state transition, transaction, deployment, trust relationship or operational responsibility. Different boundary kinds answer different questions. Draw the one needed for the decision and label it; physical folders or service nouns alone are insufficient.

Identify who can authoritatively change each important state. A derived index, cache or read model needs an update/rebuild path and a staleness policy. Separate the authoritative write from projections and notifications. A shared database can provide useful local transactions while coupling schema ownership; separate databases do not create independent business invariants automatically.

Trace a concrete input through validation, coordination, state mutation, external effect and response. Note where control returns, durability is assumed and failure can leave an uncertain result. Check the actual implementation/configuration contract rather than inferring guarantees from an API name or architecture diagram.

## Treat coordination claims precisely

For asynchronous work, distinguish:

- Request accepted from durable state committed.
- Event/message persisted from delivered or processed.
- Handler returned from external side effect confirmed.
- Acknowledgment from the underlying business operation's outcome.

Repeated delivery can be harmless under an operation-specific idempotency contract; a delivery mechanism's deduplication window is not necessarily that contract. A local inbox/outbox transaction does not automatically include an external provider. A timeout can mean unknown result, not proof of failure. Reconciliation may be needed before another external attempt; inventing a refund/cancellation API does not make an irreversible effect reversible.

Specify which consistency property matters to which operation under which failure model. Linearizable observation, transactional atomicity, replica convergence, availability, latency and durability are distinct. “CAP chooses two” or “eventual consistency” is too vague to decide single-use redemption, stale browsing, inventory reservation or offline edits. State exact assumptions before applying a theorem or a product claim.

Queueing, retries and caches can move or amplify load. Identify admission/rate limits, bounded capacity, retry/backoff policy and the observed signal for overload if relevant. Do not claim unbounded retry fixes reliability or a new queue creates throughput. Report workload assumptions and what measurement would discriminate alternatives.

## Evolve without skipping the transition

Map current/proposed/intermediate states. Identify authoritative data during migration, compatibility between old/new producers and consumers, cutover conditions and what can be rolled back. Dual writes, backfills, shadow reads and replay each have failure and reconciliation assumptions; they are not automatically safer than a smaller in-place change.

Preserve public behavior and operator capacity when requested. A strangler boundary may isolate a change, but does not settle state ownership or guarantee zero downtime. A new dependency/service requires a contextual benefit, owner and failure plan. An assessment can stop at the evidence needed to choose that transition; it does not authorize executing it.

Use exact [system cases and pattern cards](../library/index.md) for specific mechanisms, including explicit mismatches and source versions. Do not import a distributed platform's entire operating model into a small tool because one coordination idea is useful.
