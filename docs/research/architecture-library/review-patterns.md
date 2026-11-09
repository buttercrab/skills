# Independent primary-source sample: outbox and saga cards

Date: 2026-11-07. Reviewed only `pattern-transactional-outbox.md` and `pattern-saga-compensation.md` against their four cited primary guidance pages. Reviewer authored system cases, not these pattern cards, and did not read assessment fixtures. No source program, broker, transaction, compensation, renderer, failure injection or deployment was executed; no cards or example systems were edited.

## Judgment

No demonstrated material attribution or guarantee overclaim in the sampled cards. Both preserve the important boundary between an architectural mechanism and an observed operational result. Their proposed diagram implications are supported interpretations of text; no upstream picture was viewed in this review.

## Transactional outbox and consumer effect scope

Freshly read [Richardson's outbox page](https://microservices.io/patterns/data/transactional-outbox.html), Context/Forces/Solution/Result context, and [idempotent consumer page](https://microservices.io/patterns/communication-style/idempotent-consumer.html), Context/Solution.

The original description joins business-state change and message intent in the database transaction, with a separate relay. It explicitly identifies a publish-before-recording crash that can republish. The consumer example puts processing identity into its transaction and uses a unique subscriber/message pair. The card correctly adapts these local boundaries rather than promising that an outbox or a consumer deduplication table makes an unrelated provider effect atomic.

Ordering deserves the existing qualification: the outbox source discusses ordering for transactions updating the same aggregate across instances, not universal total order over all consumers. The card's request to define actual ordering scope, retry/backlog/retention and provider idempotency or reconciliation is appropriate. Source statements that messages are guaranteed on commit remain conditional on a working realization; the card's explicit live relay/storage/operation assumption prevents treating a table's presence as evidence that delivery succeeded.

The suggested transaction boundary, separate relay publication/completion marker, duplicate delivery and consumer-effect boundary expose the actual failure window. No fixed implementation, polling versus log-tailing choice, whole-system event-sourcing rewrite or distributed exactly-once claim is imported.

## Saga compensation and isolation

Freshly read [Richardson's saga page](https://microservices.io/patterns/data/saga.html), Solution/Examples/Resulting context, and [Microsoft's saga guidance](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga), Solution/Key concepts/Problems and considerations/Data anomalies. Microsoft's page included an authorization banner but exposed the cited article sections through the normal public read; no sign-in or alternate access route was used.

Richardson separates choreography and orchestration, identifies explicit compensation rather than automatic rollback, and calls out absent isolation. Microsoft additionally discusses compensation failure, irreversible local commits, pivot/retry modeling and concurrency anomalies. These support the card's distinction between local committed outcomes, domain compensation, uncertain effects and recovery responsibility.

The reservation/charge example is an original adaptation, not an inspected deployment. The card correctly treats pivot/retry labels as modeling aids, compares a suitable single-owner transaction, and does not infer that every external action can be undone or that all cross-owner invariants tolerate temporary divergence. A backward rollback arrow would therefore overstate the mechanism; the suggested sequence/state view instead includes local commits, compensating actions and unresolved/manual recovery.

## Limits

This is a textual/source-guidance review, not implementation or semantic proof of a particular outbox/saga. Linked example implementations, product features, runtime guarantees, diagrams, standards, books and referenced talks were not inspected. The two cards are suitable contextual references within that declared scope; no claim covers the rest of the pattern lane or comparative architectural effectiveness.
