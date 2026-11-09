---
{
  "id": "foundation-cap-model",
  "kind": "foundation",
  "title": "CAP: preserve the formal model behind a partition tradeoff",
  "summary": "Use the original operation and failure definitions instead of choosing two architecture buzzwords.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "model-failure",
      "verify"
    ],
    "contexts": [
      "partitions",
      "replicated-state"
    ],
    "qualities": [
      "consistency",
      "availability"
    ],
    "scale": [
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/cap-proof.pdf",
      "title": "Gilbert and Lynch: Brewer’s Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services",
      "locator": "§2 formal model; §3.1 theorem and partitioned read/write construction; §4.2–4.3",
      "revision": "SIGACT News 33(2), 2002; original paper in university copy"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh original model, theorem construction and partial-synchrony sections read. Formal result retained under stated assumptions; no implementation or failure injection."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-linearizability-histories",
    "foundation-flp-model-lead"
  ]
}
---

# CAP: preserve the formal model behind a partition tradeoff

## When to use

Use when a design is justified as CP/AP or claims uninterrupted linearizable access through arbitrary partitions.

## What to inspect

The model uses atomic/linearizable objects and eventual response at non-failing nodes; that availability definition is not a latency SLO. Inspect the partitioned write-then-read proof and timing assumptions.

## What to borrow and adapt

Our application: separate a stale-acceptable product description from a single-use redemption. Specify each operation's invariant and allowed partition response before choosing replication behavior. A whole-system two-letter label conceals those different contracts.

## Diagram implications

Mark partition boundaries, the completed write and subsequent remote read. Distinguish waiting/rejection from a stale response and identify which property is relaxed. A replication arrow alone states no consistency model.

## Mismatches and limits

CAP consistency is not ACID consistency. The result does not choose a database, eliminate normal-operation latency tradeoffs, or predict an application's observed availability. No partition test was performed.
