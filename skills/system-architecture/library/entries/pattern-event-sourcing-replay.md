---
{
  "id": "pattern-event-sourcing-replay",
  "kind": "pattern",
  "title": "Event sourcing: make replay, concurrency and external effects explicit",
  "summary": "Use an event history as authority only when reconstruction and audit needs justify event evolution and replay responsibilities.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "event-history",
      "replay",
      "projections",
      "external-effects"
    ],
    "qualities": [
      "auditability",
      "consistency",
      "evolvability"
    ],
    "scale": [
      "single-process",
      "single-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://martinfowler.com/eaaDev/EventSourcing.html",
      "title": "Fowler: Event Sourcing",
      "locator": "How it Works; External Updates/Queries; Code Changes; applicability",
      "revision": "2005-12-12 draft explicitly not actively maintained; inspected 2026-11-07"
    },
    {
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing",
      "title": "Microsoft: Event Sourcing pattern",
      "locator": "system of record; concurrency; versioning; complex-pattern warning",
      "revision": "mutable first-party guidance; inspected 2026-11-07"
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
    "system-temporal-replay-activities",
    "pattern-cqrs-model-separation"
  ]
}
---

# Event sourcing: make replay, concurrency and external effects explicit

## When to use

Use when state reconstruction, temporal queries or an authoritative event history are actual requirements, rather than merely because the application sends notifications.

## What to inspect

Read the distinction between event history and current projections. Fowler’s historical draft explains why replay must control external updates and historical query inputs. Microsoft emphasizes event schema evolution and concurrent append conflicts; its illustrated queue topology is one design, not proof that acknowledgement means durable business commit.

## What to borrow and adapt

Define the event stream’s authority and append/concurrency contract. For inventory, decide which stream owns a reservation and how competing commands are rejected or reevaluated. Plan projection rebuilds and event-version compatibility. Replaying history must not send a second payment or email unintentionally; preserve required external inputs or an equivalent historical-data contract. Compare ordinary state plus an audit log when full reconstruction is unnecessary.

## Diagram implications

Distinguish durable append, live publication, projection update and replay. Mark external effects and whether they are suppressed, reconciled or separately deduplicated during rebuild. Show the exact success/acknowledgement boundary instead of a generic queue arrow.

## Mismatches and limits

No event store, recovery or benchmark was exercised. An append-only log alone does not establish isolation, exactly-once business effects or a safe rebuild. Current guidance and a historical draft describe alternatives, not a universal architecture or migration-cost estimate.
