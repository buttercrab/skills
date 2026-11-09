---
{
  "id": "pattern-cache-aside-authority",
  "kind": "pattern",
  "title": "Cache-aside: keep freshness and authority visible",
  "summary": "Use a cache as a conditional read optimization while preserving source authority, staleness and fallback load limits.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "model-failure",
      "compare",
      "diagram"
    ],
    "contexts": [
      "caching",
      "state-ownership",
      "read-heavy"
    ],
    "qualities": [
      "latency",
      "consistency",
      "availability"
    ],
    "scale": [
      "single-process",
      "multi-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside",
      "title": "Microsoft: Cache-Aside pattern",
      "locator": "read miss and update/invalidate sequence; consistency and applicability",
      "revision": "mutable first-party guidance; inspected 2026-11-07"
    },
    {
      "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching",
      "title": "Microsoft: Caching guidance",
      "locator": "private/shared cache; source authority; fallback load; eventual-consistency population",
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
    "system-rust-analyzer-derived-state",
    "pattern-cqrs-model-separation"
  ]
}
---

# Cache-aside: keep freshness and authority visible

## When to use

Use when repeated reads justify considering caching, or a topology drawing presents cache replication as a guarantee of fresh authoritative data.

## What to inspect

Read miss/load/populate and update-then-invalidate behavior, private-cache divergence and explicit lack of consistency guarantees. Caching guidance notes that fallback can overwhelm the origin and that a stale replica can populate an old value. The source’s broad CAP shorthand is not used as a formal model here.

## What to borrow and adapt

Specify authoritative state, allowable staleness, cache key/tenant scope and the path that must bypass stale data. For a product catalog, cached descriptions may be acceptable while a reservation decision uses authoritative stock. Decide expiration/invalidation behavior and whether the origin can bear cache failure or cold-start load. Compare no cache when hit rate, volatility or operational cost do not justify another copy.

## Diagram implications

Show hit/miss reads, origin loading, writes and invalidation as different arrows. Label private versus shared copies and their freshness limits. Do not draw write-through or cache-aside as an atomic cross-store commit without an actual protocol.

## Mismatches and limits

No latency, hit rate or failure was measured. The maintained guide’s sample expiration is not a recommended constant. Correct update/invalidation ordering does not by itself prove all concurrent-read races safe. A cache is not automatically a durable record or authorization source.
