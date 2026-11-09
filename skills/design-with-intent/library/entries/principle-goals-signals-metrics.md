---
{
  "id": "principle-goals-signals-metrics",
  "kind": "foundation",
  "title": "HEART: connect user goals to signals and metrics",
  "summary": "Choose evidence from the experience goal and its possible interpretations, rather than treating activity or a dashboard metric as the design objective.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "evaluate",
      "measure",
      "frame"
    ],
    "contexts": [
      "product-metrics",
      "experiments",
      "user-outcomes"
    ],
    "platforms": [
      "web",
      "cross-platform"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/",
      "title": "Measuring the User Experience on a Large Scale",
      "locator": "Official publication entry and linked author-version paper",
      "revision": "Rodden, Hutchinson and Fu, CHI 2010"
    },
    {
      "url": "https://blog.kleros.io/content/files/pub-tools-public-publication-data/pdf/36299.pdf",
      "title": "HEART metrics author version",
      "locator": "PULSE comparison; HEART; Goals–Signals–Metrics process and cases",
      "revision": "Author version linked by Google Research; 2010"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Official publication entry and linked four-page author paper inspected; framework/practitioner examples, not a controlled validation of every metric."
  },
  "reuse": "Original annotation and links to original material; no paper, illustrations or third-party software redistributed. Check source-specific terms before substantial reproduction.",
  "related": [
    "principle-usability-sampling",
    "principle-human-ai-control"
  ]
}
---

# HEART: connect user goals to signals and metrics

## When to use

Use when deciding what would demonstrate that a redesign helped, or when the team is optimizing clicks, sessions or retention without a clear user outcome.

## What to inspect

Read the Goals–Signals–Metrics process and the examples alongside the HEART categories. Inspect how behavioral traces and attitudinal evidence complement each other. The resource's company-scale setting does not make every category mandatory.

## What to borrow and adapt

State the intended user outcome, identify plausible observable signals and alternative explanations, then choose measures that can distinguish them. Keep important dimensions separate.

For a first-event signup, more return visits might mean useful engagement or confusion about where to attend. Completion, correction, arrival confidence and support questions may reveal different aspects of the experience. A concise evaluation can be enough if it addresses the actual decision.

## Mismatches and limits

HEART is a framework with practitioner cases, not a certification or an automatically correct analytics dashboard. It does not prove causal impact from a before/after chart or require instrumenting every available event. Avoid optimizing a proxy whose increase can result from the problem itself. Protect the distinction between reported company experience and measurements collected for the current product.
