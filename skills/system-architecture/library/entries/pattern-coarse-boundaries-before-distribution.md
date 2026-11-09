---
{
  "id": "pattern-coarse-boundaries-before-distribution",
  "kind": "pattern",
  "title": "Coarse boundaries versus independent delivery: preserve the disputed premise",
  "summary": "Compare early distribution against evolving boundaries and operational cost without treating either practitioner position as a universal rule.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "decompose",
      "migrate"
    ],
    "contexts": [
      "greenfield",
      "independent-delivery",
      "domain-uncertainty"
    ],
    "qualities": [
      "evolvability",
      "operability",
      "delivery-independence"
    ],
    "scale": [
      "single-deployment",
      "multi-deployment"
    ]
  },
  "sources": [
    {
      "url": "https://martinfowler.com/bliki/MonolithFirst.html",
      "title": "Fowler: Monolith First",
      "locator": "boundary uncertainty, alternatives and tentative-evidence caveat",
      "revision": "2015-06-03 article; inspected 2026-11-07"
    },
    {
      "url": "https://martinfowler.com/articles/dont-start-monolith.html",
      "title": "Tilkov: Don’t start with a monolith",
      "locator": "independent delivery, known domains, small-team exception and boundary-refactoring cost",
      "revision": "2015-06-09 article; inspected 2026-11-07"
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
    "pattern-bounded-context-and-state-ownership"
  ]
}
---

# Coarse boundaries versus independent delivery: preserve the disputed premise

## When to use

Use when a team proposes microservices for an unproven product, or assumes a monolith can always be divided cheaply later.

## What to inspect

Fowler emphasizes uncertainty, learning speed and distribution overhead, explicitly calling his evidence sparse. Tilkov challenges the ability to preserve separability inside one process; his argument prioritizes independent delivery when the domain is understood and acknowledges small-system exceptions. These are competing practitioner arguments, not comparative trials.

## What to borrow and adapt

Compare concrete options: one deployment with deliberate internal boundaries; a few coarse independently delivered subsystems; or a staged split around a demonstrated bottleneck. For a two-person internal tool, ask what benefit pays for coordination and operations before adding a network boundary. For a replacement whose stable domains need separate delivery, do not assume starting together makes later extraction easy. Keep the unresolved premise visible rather than selecting the more familiar slogan.

## Diagram implications

Distinguish modules, processes and independently deployed units. Label shared state and cross-boundary transactions. Show a proposed future split separately from the current system; an outline around a module does not establish deployability.

## Mismatches and limits

The articles supply historical experience and reasoning, not a measured probability of success. Neither supports a universal service count, traffic threshold or team-size formula. Boundary stability, operational capability and delivery needs remain project facts to establish.
