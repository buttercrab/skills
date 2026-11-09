---
{
  "id": "pattern-ports-and-adapters",
  "kind": "pattern",
  "title": "Ports and adapters: protect a purposeful application boundary",
  "summary": "Separate application policy from external interaction where alternate drivers or tests justify it; the hexagon does not mandate six ports.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "verify",
      "diagram"
    ],
    "contexts": [
      "application-boundary",
      "external-dependencies",
      "test-isolation"
    ],
    "qualities": [
      "testability",
      "evolvability"
    ],
    "scale": [
      "single-process",
      "single-deployment",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://alistair.cockburn.us/hexagonal-architecture",
      "title": "Cockburn: original Hexagonal Architecture article",
      "locator": "Intent; Nature of the Solution; Structure; application notes",
      "revision": "HaT Technical Report 2005.02, v0.9; inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh primary sections read as architectural guidance. No upstream implementation, diagram rendering/viewing, test, benchmark, failure injection or deployed service was exercised."
  },
  "reuse": "Original contextual annotations and primary links only. No upstream text, code, diagrams or assets redistributed; reuse rights for those artifacts are not inferred.",
  "related": [
    "foundation-information-hiding",
    "pattern-strangler-transitional-architecture"
  ]
}
---

# Ports and adapters: protect a purposeful application boundary

## When to use

Use when business behavior is trapped inside UI, database or external-service integration, obstructing an actual alternate driver or test.

## What to inspect

Read the inside/outside distinction and purposeful conversations. The original article allows several adapters per port; the six-sided drawing provides room, not a required port count.

## What to borrow and adapt

For a pricing operation needed by a CLI and UI, identify the shared policy and isolate technology translation. A test adapter can exercise that boundary without the live database. Keep interfaces as narrow as the actual conversation; do not create one adapter for every class.

## Diagram implications

Label application responsibility, ports and concrete adapters. Distinguish dependency direction from runtime calls. A drawn boundary requires an implementation or verification plan.

## Mismatches and limits

A design argument, not comparative evidence. Extra indirection may add little to a script. No example or diagram was executed or viewed.
