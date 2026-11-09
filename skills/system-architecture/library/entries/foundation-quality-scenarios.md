---
{
  "id": "foundation-quality-scenarios",
  "kind": "foundation",
  "title": "Quality scenarios: make architectural priorities assessable",
  "summary": "Replace broad quality adjectives with concrete runtime or change scenarios and meaningful response measures.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "document",
      "verify"
    ],
    "contexts": [
      "quality-attributes",
      "stakeholder-priorities"
    ],
    "qualities": [
      "evolvability",
      "reliability",
      "operability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://docs.arc42.org/section-10/",
      "title": "arc42: Quality Requirements",
      "locator": "§10.1 overview; §10.2 usage/change scenarios and short/long forms",
      "revision": "Unversioned method documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh method-author overview and scenario forms read. No project scenario validation, empirical comparison or ISO standard text inspected."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-slo-measurement",
    "diagram-arc42-consistent-views"
  ]
}
---

# Quality scenarios: make architectural priorities assessable

## When to use

Use when alternatives are compared using vague words such as scalable, maintainable or reliable.

## What to inspect

Read usage versus change scenarios, context/stimulus/response measures, and the option to skip detailed scenarios when the overview is already precise. The method is guidance, not measured sufficiency.

## What to borrow and adapt

Our application: for an offline field tool, ask which capture must remain possible without connectivity and which review action may wait. For an extension request, identify who changes what and what effort is acceptable. Choose a small consequential set rather than copying every quality label.

## Diagram implications

Annotate the path or boundary a scenario exercises and the environment where it applies. Keep response measures separate from topology; a latency label is a requirement until measured.

## Mismatches and limits

A completed template does not establish architectural quality. Thresholds and stakeholder priorities remain project decisions; not every small task needs a utility tree or the entire arc42 document.
