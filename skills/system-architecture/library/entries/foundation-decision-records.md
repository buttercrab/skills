---
{
  "id": "foundation-decision-records",
  "kind": "foundation",
  "title": "Decision records: retain forces, consequences and supersession",
  "summary": "Record a significant decision and the conditions that could make it worth revisiting.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "compare",
      "migrate"
    ],
    "contexts": [
      "decision-history",
      "tradeoffs"
    ],
    "qualities": [
      "evolvability",
      "understandability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions",
      "title": "Michael Nygard: Documenting Architecture Decisions",
      "locator": "Context; Decision; Status; Consequences; Experience Report",
      "revision": "Original practice proposal, 2011-11-15"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh original practice proposal, record fields and short experience report read. No adoption intervention, project history or outcome study verified."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-quality-scenarios",
    "pattern-strangler-transitional-architecture"
  ]
}
---

# Decision records: retain forces, consequences and supersession

## When to use

Use when future maintainers need to distinguish a deliberate compromise from an unexplained accident.

## What to inspect

Read the small-record proposal, decision forces, status, positive/negative/neutral consequences and supersession. The early experience report is not comparative proof of effectiveness.

## What to borrow and adapt

Our application: record choosing one process and one transactional store because two maintainers need a simple recovery path. Include the rejected distribution option, its coordination cost and what changed workload or ownership might reopen the decision. Do not present a diagram of that proposal as current deployment evidence.

## Diagram implications

Link a view to the decision and its status. Keep as-is, proposed and superseded models explicit so a future reader does not combine incompatible snapshots.

## Mismatches and limits

The original path/naming convention is a local proposal, not mandatory repository layout. Avoid a record for every trivial change or treating an accepted status as evidence that the predicted consequences occurred.
