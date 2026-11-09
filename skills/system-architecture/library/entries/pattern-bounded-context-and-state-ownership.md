---
{
  "id": "pattern-bounded-context-and-state-ownership",
  "kind": "pattern",
  "title": "Model context, data ownership and deployment are separate boundaries",
  "summary": "Use vocabulary and state ownership to find boundaries without equating a bounded context with a process or a physical database.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "trace",
      "diagram"
    ],
    "contexts": [
      "domain-models",
      "state-ownership",
      "cross-service-invariants"
    ],
    "qualities": [
      "evolvability",
      "consistency",
      "delivery-independence"
    ],
    "scale": [
      "single-process",
      "single-deployment",
      "multi-deployment"
    ]
  },
  "sources": [
    {
      "url": "https://martinfowler.com/bliki/BoundedContext.html",
      "title": "Fowler: Bounded Context",
      "locator": "polysemes, context relationships and context maps",
      "revision": "2014-01-15 interpretation; inspected 2026-11-07"
    },
    {
      "url": "https://microservices.io/patterns/data/database-per-service.html",
      "title": "Richardson: Database per service",
      "locator": "private tables/schema/server variants; cross-service transactions and queries",
      "revision": "mutable original-author catalog; inspected 2026-11-07"
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
    "foundation-conway-coordination",
    "pattern-coarse-boundaries-before-distribution"
  ]
}
---

# Model context, data ownership and deployment are separate boundaries

## When to use

Use when teams share words such as customer or account but assign them different meanings, or when nominally separate services write one another’s data.

## What to inspect

Fowler explains internally coherent models and explicit mappings, including different representations inside one application. Richardson describes private persistence reached through the owning service and distinguishes private tables, schemas and servers. Semantic ownership therefore does not determine physical topology by itself.

## What to borrow and adapt

Name each model’s vocabulary, authoritative mutations and integration contract. For billing versus support, map identifiers and the particular facts exchanged rather than force one universal customer object. If independent services are justified, identify how data encapsulation is enforced and how cross-owner queries or invariants are handled. A shared server can still contain separate ownership areas; separate database servers do not by themselves remove semantic coupling.

## Diagram implications

Use a context map for meaning and translation; use a deployment view for processes/hosts. Mark state ownership and permitted reads/writes instead of drawing an unlabeled database beside each noun.

## Mismatches and limits

Fowler is an interpretation of DDD, not the original Evans book. The attempted Evans reference PDF returned 403 and was not read. Richardson’s CAP shorthand is not used here as proof that distributed transactions are impossible. No access enforcement, runtime integration or current deployment was tested.
