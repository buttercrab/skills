---
{
  "id": "pattern-transactional-outbox",
  "kind": "pattern",
  "title": "Transactional outbox: join the local commit and message intent",
  "summary": "Close the database-to-message intent gap while retaining relay duplication, ordering and consumer-effect limits.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "model-failure",
      "diagram",
      "verify"
    ],
    "contexts": [
      "transactional-messaging",
      "dual-write",
      "message-relay"
    ],
    "qualities": [
      "consistency",
      "durability",
      "operability"
    ],
    "scale": [
      "single-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://microservices.io/patterns/data/transactional-outbox.html",
      "title": "Richardson: Transactional outbox",
      "locator": "forces; sender/database/outbox/relay; duplicate relay publication",
      "revision": "mutable original-author catalog; inspected 2026-11-07"
    },
    {
      "url": "https://microservices.io/patterns/communication-style/idempotent-consumer.html",
      "title": "Richardson: Idempotent Consumer",
      "locator": "processed-message identity and transactional duplicate detection",
      "revision": "mutable original-author catalog; inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh primary sections read as architectural guidance. No upstream implementation, diagram rendering/viewing, test, benchmark, failure injection or deployed service was exercised."
  },
  "reuse": "Original contextual annotations and primary links only. No upstream text, code, diagrams or assets redistributed; reuse rights for those artifacts are not inferred.",
  "related": [
    "system-nats-delivery-effects",
    "pattern-saga-compensation"
  ]
}
---

# Transactional outbox: join the local commit and message intent

## When to use

Use when a domain update and an external publication can diverge because a process crashes between independent writes.

## What to inspect

The outbox records domain state and message intent in one local transaction, then relays messages separately. The relay can republish after a send-before-mark crash. The consumer pattern records processing identity with its local effects; neither mechanism automatically covers effects in an unrelated external service.

## What to borrow and adapt

For an order notification, commit the order change and outbox entry together. Define relay retries, backlog visibility, retention and the ordering scope actually required. Give consumers a stable identity and an atomic duplicate-check/effect boundary where applicable. If delivery ultimately calls an external provider, trace that provider’s idempotency or reconciliation contract instead of declaring end-to-end exactly-once behavior.

## Diagram implications

Place domain update and outbox insert inside the same transaction boundary. Draw relay publication and its completion marker separately. Include duplicate delivery and the consumer’s effect boundary; a single DB-to-broker arrow hides the important crash window.

## Mismatches and limits

No implementation, durable log or fault scenario was run. Delivery depends on live relay/storage/operations assumptions, not the presence of an outbox table alone. Ordering across aggregates and idempotency-retention policy require their own contract. This local solution does not require a global event-sourced rewrite.
