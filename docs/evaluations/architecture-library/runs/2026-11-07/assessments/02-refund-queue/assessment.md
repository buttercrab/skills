# Refund processing: source-only assessment and proposed decision

Adopt a database-owned refund lifecycle with request deduplication, a transactional outbox, and a durable provider-attempt ledger. Reuse the existing database and queue. Preserve uncertain outcomes for reconciliation instead of interpreting timeout as failure. This is a proposal; no implementation, deployed topology, runtime behavior or performance has been verified.

## Current behavior and inferred failure windows

All snapshot references below are relative to `/private/tmp/system-architecture-assessment-20261107/02-refund-queue/`.

| Inspected current behavior | Inferred consequence under the supplied contracts |
| --- | --- |
| Handler commits a `requested` row, publishes separately, then returns its ID (`snapshot/worker.py:12–16`). | Crash after line 14 but before publication can leave a durable approved request with no queued work. Publication failure or a lost response can also cause creation retries. |
| `client_request_id` is ignored (`snapshot/policy.md:3`); no request identity constraint exists (`snapshot/contracts.md:6`). | A creation retry can make a second business operation, even if each worker later deduplicates by refund ID. |
| Worker skips only `paid`; otherwise calls provider without a key before recording success (`snapshot/worker.py:3–9`). | Crash/timeout after provider success but before line 8 permits a duplicate external refund on redelivery. Two workers can both observe a non-paid row and call. |
| Queue is at least once; lease is 45 seconds and may overlap workers; acknowledgment only removes a delivery (`snapshot/contracts.md:2`). | Lease renewal or moving acknowledgment alone cannot establish duplicate-safe business processing. Crash after line 8 but before line 9 is harmless only if the subsequent read sees committed `paid`; concurrency remains unsafe. |
| No attempt record exists (`snapshot/contracts.md:6`), while audit requires 180 days (`snapshot/policy.md:5`). | The shown schema/path supplies no complete attempt audit. This is a source coverage gap, not proof about unprovided production logs. |

The illustrative function is explicitly not a standalone program (`snapshot/worker.py:1`). These are source-supported failure possibilities, not observed incidents. Authorization/charge validation, isolation level, persistence settings and deployed components are not supplied.

## Proposed authority and commit boundaries

The database owns the approved intent, immutable business payload, delivery intent, attempt identity, next recovery action, and locally known outcome. The payment provider owns the actual external refund effect. The queue carries wake-ups, not truth. Neither local transactions nor broker acknowledgments include the provider (`snapshot/contracts.md:2,4,6`).

There are three distinct points:

1. **Acceptance commit:** atomically insert the unique request identity, approved charge/amount, refund ID, initial status and outbox intent. Only after commit return the stable ID and an accepted status. This promises durable responsibility, not completed payment. Deduplicate using a documented caller/account-scoped `client_request_id`; identical payload returns the existing ID, changed payload conflicts. Store the original payload and approval evidence. The exact caller scope is a contract detail to settle before implementation.
2. **Business effect commit:** the provider actually creates the refund. A response may be lost afterward. It is not atomic with our database. **Local completion commit:** after positive response or lookup evidence, atomically record provider ID, evidence, attempt audit and `succeeded`. This is our authoritative recorded completion, not the physical instant money changed hands. Never mark success merely because POST was sent or timed out.
3. **Acknowledgment:** acknowledge only after local completion, a definitive terminal decision, or a durable handoff to recovery has committed. Recovery handoff must atomically record `unknown`/`held`, next lookup/review action and an outbox task or database-scan obligation. If that commit fails, do not acknowledge. An acknowledged ambiguous job remains visible and recoverable in the database. A duplicate delivery that finds a terminal row can acknowledge immediately; one that finds an active/due obligation may acknowledge only when that obligation is durable and a sweeper guarantees recovery.

An outbox relay publishes the refund ID, waits for the queue's durable acceptance confirmation, then marks publication. A crash between send and mark republishes. Queue durability confirmation semantics and publish timeout behavior are unknown and must be established; leave unconfirmed entries pending. A database sweeper scans unsent intents, expired claims and overdue reconciliation/review records, so delayed or lost wake-ups do not silently lose work. An outbox closes the shown acceptance gap, not the external-effect gap.

## Proposed execution and recovery rules

Persist one stable provider idempotency key and the exact approved payload **before the first possible POST**, with a unique relationship to the business refund. Keep attempt rows separately for each network invocation/observation; retries do not become new business refunds or new keys. Record earliest possible dispatch time conservatively before sending, outcomes, errors, provider IDs, lookup evidence, claim/version and next due action. Retain complete evidence and final finance decisions for 180 days (`snapshot/policy.md:5`), including after the provider forgets keys.

Use an atomic database claim/compare-and-set to choose a worker and reject stale state writes. Do not hold a database transaction over a network call. A claim token fences database updates; it cannot recall an external request. Every possible POST for that refund uses the same key and immutable payload. On claim expiration, reconcile the persisted attempt first. The 45-second broker lease is not an execution lock. Concurrent same-key provider behavior, maximum request lifetime and retention boundary semantics need confirmation before enabling overlapping or boundary-adjacent retries; local serialization alone cannot fence a stale remote call.

On a timeout or crash after send-intent, record or recover into `unknown`. GET by the same key can establish success; a negative lookup inside the first 90 seconds is inconclusive (`snapshot/contracts.md:4`). Continue scheduled lookup/backoff, retaining evidence. Do not infer a definitive failure from an empty lookup after 90 seconds either: the contract provides no negative finality rule for a still-running request. Within a verified safe retention interval, a same-key/same-payload POST may be retried under the stated idempotency contract, with one retry owner and bounded backoff/jitter. A changed-payload key conflict goes to review, never rekeying. Definitive provider rejection can become a recorded rejection only if its response contract establishes no effect; those response details are absent here.

**Ten-day delay has two cases.** A request demonstrably never dispatched can wait ten days and then start its first attempt with its persisted key; queue age itself does not consume the provider's retention. A persisted send-intent, even if the worker died before actually sending, means a call might have happened. Count its safe window conservatively from the earliest possible first dispatch; never reset that clock on retries. A seven-day window cannot make an uncertain effect safe after ten days (`snapshot/contracts.md:4`; `snapshot/policy.md:6`). Use a conservative safety margin once provider expiry/time semantics and maximum in-flight duration are established; do not invent a numeric margin. Without these facts, fall back to lookup/review rather than making a boundary-risk POST.

**Finance direction received through root:** “Finance requires holding the refund as unresolved and escalating for evidence-based manual reconciliation. No automatic new-key refund is permitted without a recorded finance decision.” Thus expired unresolved attempts transition to durable `held`, alert finance and retain their identity. No automatic resend under a fresh key, no automatic declaration of failure, and no silent abandonment. Manual decisions must record actor, evidence, approved action and linkage to the original refund before any authorized follow-up. Evidence can close the original as succeeded or definitively rejected; a recorded finance decision is required for any other business action. The no-answer fallback was the same unresolved hold; the received answer resolves this policy branch. No provider ledger, compensation API or callback reliability is invented.

## Choice, alternatives and operating cost

| Option | Decision under this brief |
| --- | --- |
| Keep worker, change acknowledgment timing | Reject: cannot close the DB/publication gap, duplicate creation or uncertain external effect. |
| Database state machine + outbox + existing queue | Select as proposal: existing components, atomic local acceptance, durable recovery and provider-key discipline; requires relay/sweeper ownership and attempt audit. |
| Database-only polling worker | Viable simpler alternative if the queue can be retired and polling capacity meets the supplied five-minute target. It removes relay/broker coordination but retains identity, attempt ledger, reconciliation and expiry hold. No workload evidence selects polling cadence or proves capacity. |
| Durable workflow platform, event-sourced rewrite or more services | Defer: two maintainers and existing DB/queue (`snapshot/policy.md:7`); added platform operations do not extend provider retention or establish duplicate-safe external effects. |

Measure accepted-to-known-completion against the provided **99% of normal requests within five minutes** target, with normal/ambiguous classification explicit (`snapshot/policy.md:4`). Also expose oldest pending intent, overdue claim/lookup, unknowns nearing expiry, held case age, duplicate suppression, attempt counts and finance review ownership. Do not claim this design already meets the SLO. Bound retry concurrency and rate during the provider incident; service capacity, traffic and quotas are unknown, so no numeric throughput/timeout settings are proposed.

## Safe transition and evidence required

1. Specify caller identity scope, immutable-payload conflict behavior, provider result semantics and safe key lifetime. Add constraints/ledger/outbox and recovery ownership before enabling keyed writes. These are proposed changes only.
2. Quiesce old unkeyed workers and drain or classify in-flight work before new dispatch. Existing `requested` rows may already have caused an unrecorded effect; do not blindly backfill keys and replay them. Classify with provider/finance evidence, otherwise hold. Existing duplicates need business reconciliation before uniqueness backfill.
3. Enable atomic acceptance and new workers together through a controlled compatibility cutover; keep IDs and status reads compatible. Backfill recovery tasks only for classified rows. Reverting to old unkeyed workers can repeat external effects; a safe rollback disables dispatch while retaining durable records and review/reconciliation.
4. Before release, authorized fault checks should cover crash after acceptance/before publish, relay send-before-mark, lost create response, two workers/lease expiry, provider success-before-local-commit, timeout with delayed lookup, crash before actual send, seven-day expiry/ten-day delay, and recovery-commit failure before acknowledgment. Validate audit retention, actual transaction/claim constraints, provider concurrent-key behavior and recovery monitoring. None was executed here.

## Reference transfers and limits

The frozen library index and five full cards were read locally. Only their annotations were inspected in this run; their claimed curator primary/visual checks were **not repeated**. No external source was fetched under the run's network prohibition.

| Local card | Transferred mechanism | Decisive mismatch / adaptation |
| --- | --- | --- |
| `guide/library/entries/pattern-transactional-outbox.md`, “What to inspect” and “Mismatches and limits” | Local refund + message intent commit; relay may duplicate. | External payment is outside that transaction; add attempt identity/reconciliation rather than claim exactly once. |
| `guide/library/entries/pattern-retry-budget-and-breaker.md`, “What to borrow and adapt” | Preserve caller intent across timeout; one bounded retry owner. | No copied timeouts/breaker settings; use the actual seven-day/90-second contract. |
| `guide/library/entries/system-temporal-replay-activities.md`, “What to borrow and adapt” | Durable coordination does not make external activities exactly once. | Do not import a workflow service for this small team; compare existing database state machine. |
| `guide/library/entries/foundation-end-to-end-guarantees.md`, “What to borrow and adapt” | Business identity belongs at the application/effect boundary. | A conceptual argument proves no current queue or provider behavior; supplied contracts carry those facts. |
| `guide/library/entries/diagram-mermaid-sequence-outcomes.md`, “Diagram implications” | Label ordered observations, timeout and alternate recovery. | Not a rendered trace or syntax verification of the new diagrams. |

Actual checks: line-by-line snapshot read; failure-window and transaction-boundary trace; manual prose/diagram consistency review. Editable diagram source is in `diagrams.md`. No fixture execution, parser, rendering, tests, build, install, network, provider call or infrastructure change occurred. Remaining technical unknowns above constrain implementation guarantees; they do not authorize reissuing an uncertain refund.
