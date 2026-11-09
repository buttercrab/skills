---
{
  "id": "system-nats-delivery-effects",
  "kind": "system",
  "title": "NATS JetStream: delivery acknowledgments are not business-effect completion",
  "summary": "Keep durable stream state, consumer pending/redelivery state and a handler’s external effects separate when reasoning about retries.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "message-processing",
      "redelivery",
      "worker-pools"
    ],
    "qualities": [
      "reliability",
      "backpressure",
      "consistency"
    ],
    "scale": [
      "single-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://docs.nats.io/learn/jetstream/delivery-and-acknowledgment",
      "title": "NATS delivery and acknowledgment",
      "locator": "Consumer ack/redelivery loop and source of at-least-once delivery",
      "revision": "Live documentation read 2026-11-07; not a frozen release"
    },
    {
      "url": "https://docs.nats.io/learn/jetstream/acknowledgment",
      "title": "NATS ack responses and redelivery",
      "locator": "AckWait, ack/nak/term/in-progress, consumer policy, MaxDeliver and advisory limits",
      "revision": "Live documentation read 2026-11-07; not a frozen release"
    },
    {
      "url": "https://github.com/nats-io/nats-server/blob/59bf235aea63881477dd485af3579be2ffc32b0c/server/consumer.go",
      "title": "nats-io/nats-server: server/consumer.go",
      "locator": "ConsumerConfig fields; AckPolicy constants around 353; processNak; checkPending around 6268",
      "revision": "59bf235aea63881477dd485af3579be2ffc32b0c"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh first-party delivery/ack text and selected pinned consumer source inspected. Old route redirect recorded. No broker, external side effect, upstream program or rendered diagram executed."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "pattern-transactional-outbox",
    "foundation-end-to-end-guarantees"
  ]
}
---

# NATS JetStream: delivery acknowledgments are not business-effect completion

## When to use

Use when a worker may finish an external effect and fail before acknowledging its message. It makes the missing application-level duplicate/reconciliation decision visible instead of relying on a broker label.

## What to inspect

Read the consumer delivery loop and response meanings, then the pinned consumer state/configuration and checkPending/processNak branches. The latter computes deadlines/backoff, considers delivery limits and queues expired pending entries. AckNone, AckAll, AckExplicit and internal flow-control handling are distinct policies; do not generalize explicit-ack examples to every consumer.

## Architecture trace

A consumer records a delivered message as pending while the handler works. Timeout or a negative response can cause redelivery, with timing and limits determined by configured policy. The inspected server branch schedules expired pending sequences; it has no knowledge that an arbitrary external payment or notification already completed. A stream-retention action and stopping this consumer’s delivery are also distinct.

## What to borrow and adapt

State when the handler acknowledges relative to a durable business outcome, how duplicate attempts are identified and what happens to exhausted or permanently invalid work. Treat those as application requirements, not features inferred from an ACK arrow. Preserve a path for reconciliation when the handler cannot know whether an external effect succeeded.

## Diagram implications

Use a sequence with stream/consumer, worker, effect owner and acknowledgment. Mark the failure window after effect completion but before ACK and a possible redelivery. Add pending/backoff/terminal states when that is the decision. Neither a broker box nor a “reliable” edge demonstrates exactly-once business execution.

## Mismatches and limits

The previous consumer documentation route redirected to a pull-consumer tutorial. This card cites the actual inspected delivery/response pages and selected development source instead of assuming old locators remain current. No consumer was created, broker run, handler executed or delivery guarantee tested. Actual retention, replicas, persistence and client/server compatibility must be established for the target system.
