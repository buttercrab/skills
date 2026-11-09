---
{
  "id": "foundation-causal-order",
  "kind": "foundation",
  "title": "Logical clocks: distinguish causality from timestamp order",
  "summary": "Use message and process relationships without inferring causality from a smaller timestamp alone.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "diagram",
      "verify"
    ],
    "contexts": [
      "distributed-events",
      "logical-clocks"
    ],
    "qualities": [
      "correctness",
      "observability"
    ],
    "scale": [
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/Time-Clocks-and-the-Ordering-of-Events-in-a-Distributed-System.pdf",
      "title": "Lamport: Time, Clocks, and the Ordering of Events in a Distributed System",
      "locator": "pp.558–560: partial ordering, event granularity, Clock Condition and its non-converse",
      "revision": "CACM 21(7), 1978; original author-publication PDF"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh original partial-order, event-granularity and Clock Condition sections read as text. Figures not viewed; no tracing/clock implementation or measurements verified."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-linearizability-histories",
    "pattern-request-reply-versus-messaging"
  ]
}
---

# Logical clocks: distinguish causality from timestamp order

## When to use

Use when logs from several processes are arranged into a definitive causal story or an ordering guarantee.

## What to inspect

Read process order, message send/receive and transitivity, then the Clock Condition. Increasing logical-clock values preserve happened-before; their numerical ordering does not imply its converse. The chosen event granularity also matters.

## What to borrow and adapt

Our application: an upload log and a later-numbered indexing log need a correlated message or operation relationship before concluding that this upload caused this indexing action. Keep concurrent events unresolved rather than assigning causality from display order.

## Diagram implications

Distinguish process progression and message edges from physical-time placement. Label the observational basis for an edge. A visually earlier node on another lane is not necessarily a predecessor.

## Mismatches and limits

Logical timestamps are not elapsed time, synchronized wall clocks or latency measurements. The selected sections do not verify a tracing implementation, solve crash recovery, or prove an application's history complete. No source figures were visually inspected.
