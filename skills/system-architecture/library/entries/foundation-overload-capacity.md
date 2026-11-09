---
{
  "id": "foundation-overload-capacity",
  "kind": "foundation",
  "title": "Capacity and queues: model resources and feedback",
  "summary": "Treat capacity as workload-sensitive resource consumption and bound waiting rather than assume more buffering creates throughput.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "model-failure",
      "compare",
      "verify"
    ],
    "contexts": [
      "overload",
      "queues",
      "resource-limits"
    ],
    "qualities": [
      "latency",
      "availability",
      "operability"
    ],
    "scale": [
      "single-process",
      "distributed",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://sre.google/sre-book/handling-overload/",
      "title": "Google SRE: Handling Overload",
      "locator": "The Pitfalls of Queries per Second; resource-cost model and per-customer limits",
      "revision": "SRE book chapter21, online text inspected 2026-11-07"
    },
    {
      "url": "https://sre.google/sre-book/addressing-cascading-failures/",
      "title": "Google SRE: Addressing Cascading Failures",
      "locator": "Resource Exhaustion; Queue Management; Load Shedding and Graceful Degradation",
      "revision": "SRE book chapter22, online text inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh first-party capacity, resource-exhaustion, queue-management and degradation sections read. No load tests, simulations or current Google topology verified."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "pattern-backpressure-and-bounded-work",
    "pattern-retry-budget-and-breaker"
  ]
}
---

# Capacity and queues: model resources and feedback

## When to use

Use when a design assumes a queue or replica count will absorb arbitrary growth, or quotes one QPS capacity without request-cost context.

## What to inspect

Compare resource-cost capacity with QPS proxies, then read queue waiting/memory and feedback examples. Steady and bursty traffic can justify different queue behavior. The operational examples do not supply universal thresholds.

## What to borrow and adapt

Our application: image transforms vary by input size. Track admitted work, in-flight resource cost, queue age and expired jobs; decide whether to reject, delay or degrade each class. Test that decision at representative costs instead of copying an online numeric queue rule.

## Diagram implications

Show admission, bounded waiting, service capacity, deadlines and rejection/degradation routes. Include retry or failover feedback that can add load. A queue icon alone promises neither throughput nor durability.

## Mismatches and limits

Google's examples are practitioner reasoning and reported experience, not a benchmark reproduced here. Overload strategies themselves add complexity. The card establishes no particular service capacity, load-test result or safe queue length.
