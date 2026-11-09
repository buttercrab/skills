---
{
  "id": "foundation-conway-coordination",
  "kind": "foundation",
  "title": "Conway: include communication constraints in boundary choices",
  "summary": "Treat team coordination as architectural context without making organization charts a deterministic quality rule.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "compare",
      "migrate"
    ],
    "contexts": [
      "team-boundaries",
      "coordination"
    ],
    "qualities": [
      "evolvability",
      "operability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://www.melconway.com/Home/pdf/committees.pdf",
      "title": "Conway: How Do Committees Invent?",
      "locator": "pp.28–31: delegation, system/design graphs, systems image their design groups, conclusion",
      "revision": "Datamation, April1968; original author-hosted PDF"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh original author-hosted PDF argument/examples/conclusion read. Initial HTML depth requests timed out; no empirical organizational intervention or source figure viewing."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "pattern-bounded-context-and-state-ownership",
    "pattern-coarse-boundaries-before-distribution"
  ]
}
---

# Conway: include communication constraints in boundary choices

## When to use

Use when independent service ownership is proposed without considering who must negotiate or operate its interfaces.

## What to inspect

Read the original delegation and communication argument, examples and conclusion about organizational flexibility. Its reasoning is conceptual and anecdotal, not an experimentally calibrated prediction of every organization.

## What to borrow and adapt

Our application: before splitting billing and entitlement, identify which changes require both owners, who responds to partial failure and how compatibility decisions are made. Compare that actual coordination burden with the promised delivery independence. A new repository or API does not supply that operating agreement.

## Diagram implications

Keep semantic, process and ownership boundaries distinguishable. A team overlay can explain responsibility; do not imply each team must equal one service or transaction.

## Mismatches and limits

Do not infer architecture quality or prescribe a reorganization from an org chart alone. The paper does not establish contemporary productivity rates or a universal team size. No organization or current deployment was observed.
