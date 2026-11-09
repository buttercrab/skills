---
{
  "id": "pattern-strangler-transitional-architecture",
  "kind": "pattern",
  "title": "Strangler migration: design coexistence and removal, not just the target",
  "summary": "Use seams and observable stages to compare incremental replacement with a justified simpler cutover.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "migrate",
      "compare",
      "trace",
      "diagram"
    ],
    "contexts": [
      "legacy-modernization",
      "transitional-architecture",
      "routing-seams"
    ],
    "qualities": [
      "evolvability",
      "availability",
      "operability"
    ],
    "scale": [
      "single-deployment",
      "multi-deployment",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://martinfowler.com/bliki/StranglerFigApplication.html",
      "title": "Fowler: Strangler Fig",
      "locator": "outcomes, seams, transitional architecture and incremental learning",
      "revision": "revised 2024-08-22 article; inspected 2026-11-07"
    },
    {
      "url": "https://martinfowler.com/articles/patterns-legacy-displacement/",
      "title": "Cartwright, Horn and Lewis: Patterns of Legacy Displacement",
      "locator": "four activities; middleware-removal seam, routing and contract account",
      "revision": "2024-03-05 practitioner account; inspected 2026-11-07"
    },
    {
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig",
      "title": "Microsoft: Strangler Fig pattern",
      "locator": "façade routing; coexistence dependencies; decommissioning and suitability",
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
    "foundation-decision-records",
    "pattern-ports-and-adapters"
  ]
}
---

# Strangler migration: design coexistence and removal, not just the target

## When to use

Use when replacing a consequential legacy system while behavior must continue, especially if a proposal shows only an attractive final topology.

## What to inspect

Read the desired-outcome and seam arguments alongside the specific middleware migration account. Microsoft makes façade dependencies, routing and decommissioning conditions explicit, and notes cases where interception is unavailable or a small replacement is simpler. These are documented approaches, not a reproduced modernization result.

## What to borrow and adapt

Define the smallest useful behavior to move, how old and new implementations coexist, and the contract consumers must retain. Identify state ownership during transition, routing criteria, reconciliation and an actual rollback boundary. A rollback of traffic is insufficient once state has changed incompatibly. Specify evidence for progressing, retiring adapters and eventually removing the old path; transitional cost is part of the comparison.

## Diagram implications

Draw current, transitional and target views separately, with routing and state-ownership changes labeled. Mark temporary components and their removal conditions. A sequence can expose cross-system effects that a static target drawing omits.

## Mismatches and limits

No source system, migration or rollback was executed. Original accounts do not guarantee that seams exist or behavior is fully known. Do not require a service split, proxy or platform replacement for a small system with a safer direct cutover. Organizational constraints remain project facts, not inferred from a diagram.
