---
{
  "id": "diagram-c4-runtime-scenario",
  "kind": "notation",
  "title": "C4 dynamic views: order one consequential scenario",
  "summary": "Explain how known elements collaborate for a particular feature while keeping structural relationships distinct from timed runtime events.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "diagram",
      "trace",
      "model-failure"
    ],
    "contexts": [
      "runtime-scenarios",
      "interaction-order"
    ],
    "qualities": [
      "reliability",
      "understandability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://c4model.com/diagrams/dynamic",
      "title": "C4 Dynamic diagram",
      "locator": "Scope, numbered ordering, recommendations and collaboration/sequence styles",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.arc42.org/section-6/",
      "title": "arc42 Runtime view",
      "locator": "Representative use, external-interface, operations and error scenarios",
      "revision": "Mutable official documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh official documentation text and selected source examples inspected. No source diagram image was visually viewed, and no parser, renderer, installed tool, generated output or system interaction was executed in this curation."
  },
  "reuse": "Original annotations and source links only. No upstream images, manuals, implementations or packages redistributed; source-specific asset reuse rights must be checked before copying.",
  "related": [
    "diagram-mermaid-sequence-outcomes",
    "pattern-transactional-outbox"
  ]
}
---

# C4 dynamic views: order one consequential scenario

## When to use

Use when a static arrow hides a consequential order, acknowledgment or recovery step. A request that commits before the client sees a response needs a different explanation from a page showing that an API depends on a database.

## What to inspect

C4 dynamic diagrams describe one feature/use case with numbered interactions, in either collaboration or sequence style. The official recommendation is selective use rather than a diagram for every feature. arc42's runtime section includes operation and exception scenarios and emphasizes architectural relevance over scenario count.

## Diagram implications

Reuse the static model's identities and choose one level of abstraction. State the scenario's precondition and observation point. Number or sequence the interactions, including the important failure branch: the store can commit while a response is lost. Label whether a response means accepted, committed or completed; never let an arrow silently promise all three. Ordering in the authored scenario is not a measured timeline.

## What to borrow and adapt

For an asynchronous export, first show acceptance and the eventual result as different interactions. A second small scenario can examine restart or lost acknowledgment if that changes the decision. Keep routine steps in prose when a diagram adds no clarity. Use a state view instead when the main question concerns legal transitions of one owned record.

## Mismatches and limits

A selected scenario is not a complete protocol specification or proof of liveness. Neither source establishes your system's retry, timeout, idempotency or cancellation behavior; find the owning contract or mark a proposal. The interaction descriptions were read, not executed or visually inspected. This card does not justify a mandatory sequence-diagram suite.
