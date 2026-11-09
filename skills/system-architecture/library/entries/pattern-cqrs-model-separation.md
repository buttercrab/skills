---
{
  "id": "pattern-cqrs-model-separation",
  "kind": "pattern",
  "title": "CQRS: separate models only where their differences justify the cost",
  "summary": "Compare one shared model with distinct command/read models while preserving consistency and recovery implications.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "decompose",
      "trace",
      "diagram"
    ],
    "contexts": [
      "read-write-asymmetry",
      "domain-models",
      "projections"
    ],
    "qualities": [
      "evolvability",
      "latency",
      "consistency"
    ],
    "scale": [
      "single-process",
      "single-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://martinfowler.com/bliki/CQRS.html",
      "title": "Fowler: CQRS",
      "locator": "model separation; variations; When to use it",
      "revision": "2011-07-14 practitioner account; inspected 2026-11-07"
    },
    {
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs",
      "title": "Microsoft: CQRS pattern",
      "locator": "single versus separate data stores; problems; applicability",
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
    "pattern-event-sourcing-replay",
    "foundation-transaction-isolation"
  ]
}
---

# CQRS: separate models only where their differences justify the cost

## When to use

Use when reads and writes need materially different models or optimization, especially if a proposal bundles CQRS with mandatory event sourcing and a broker.

## What to inspect

Fowler warns about risky complexity and local applicability. Microsoft distinguishes model separation in one data store from separate read/write stores and states that messaging is not required. Its guidance is a design account, not a benchmark proving the advertised benefits for this workload.

## What to borrow and adapt

Identify the specific query/update conflict before adding another model. For a complex search view, compare a focused reporting projection with separating every query. If a projection is asynchronous, define acceptable lag, read-after-write behavior, replay/rebuild, version compatibility and failure reporting. Keep a simpler shared-model alternative when the overlap is large.

## Diagram implications

Show command validation and authoritative writes, query-serving model and any projection update. Label shared versus independent stores and lag-bearing arrows. Separate models are not automatically separate processes.

## Mismatches and limits

No throughput, correctness or availability result was reproduced. CQRS is not synonymous with event sourcing, a separate database, or eventual consistency in every form. The source’s broad use-case claims do not establish that a particular UI or security boundary requires it.
