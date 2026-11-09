---
{
  "id": "foundation-slo-measurement",
  "kind": "foundation",
  "title": "SLOs: connect architectural effort to observable user outcomes",
  "summary": "Separate the desired service outcome, its measurement implementation and the decision policy around it.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "verify",
      "document"
    ],
    "contexts": [
      "service-objectives",
      "measurement-boundaries"
    ],
    "qualities": [
      "reliability",
      "latency",
      "observability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://sre.google/workbook/implementing-slos/",
      "title": "Google SRE Workbook: Implementing SLOs",
      "locator": "Getting Started; Reliability Targets and Error Budgets; What to Measure; SLI specification versus implementation",
      "revision": "SRE Workbook chapter2, online text inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh first-party stakeholder, ratio, measurement-implementation and coverage/cost sections read. No SLO adopted, telemetry inspected or reliability outcome measured."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-overload-capacity",
    "system-valkey-persistence-policy"
  ]
}
---

# SLOs: connect architectural effort to observable user outcomes

## When to use

Use when “high availability” or a target percentage is being used to select architecture without an agreed user outcome or measurement boundary.

## What to inspect

Read outcome-based good/total event ratios, stakeholder ownership and error-budget policy. The chapter distinguishes an SLI specification from measurement implementations with different coverage and cost.

## What to borrow and adapt

Our application: define whether a search is good by response time, freshness and the result actually reaching the client. Server logs omit failures that never reach the server; a browser probe has different blind spots. Choose evidence for the promise, then obtain the actual acceptable target rather than inventing one.

## Diagram implications

Mark the measurement points, request/data path and dependencies relevant to the outcome. Label what the observer cannot see. A healthy internal component is not automatically a successful user interaction.

## Mismatches and limits

The chapter concerns service reliability practice, not a universal tolerance for correctness or safety failures. No target, telemetry quality, current reliability or policy effectiveness was measured here.
