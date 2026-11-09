---
{
  "id": "docs-study-google-review",
  "kind": "study",
  "title": "Sadowski et al.: review practices and tools co-evolve",
  "summary": "Use the Google case to examine review context and analyzer feedback, without copying reviewer counts or turnaround targets as universal standards.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "review",
      "quality",
      "ownership"
    ],
    "contexts": [
      "review-process",
      "automated-feedback"
    ],
    "languages": [
      "language-agnostic"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf",
      "title": "Modern Code Review: A Case Study at Google",
      "locator": "Sections 3.2–3.4 methods/limits; 5 review mechanics; 7.1–7.3 interpretation",
      "revision": "ICSE-SEIP 2018; DOI 10.1145/3183519.3183525"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Primary PDF methods, review mechanics, analyzer feedback and limitations freshly read; historical observational mixed-method evidence."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "docs-google-change-review",
    "docs-github-codeowners"
  ]
}
---

# Sadowski et al.: review practices and tools co-evolve

## When to use

Use when a team proposes a review policy or analyzer gate by copying a large organization's headline practice.

## What to inspect

The study combines twelve interviews, forty-four survey responses and filtered logs of roughly nine million reviews. Its single-company setting, self-selection and coding/robot-filter heuristics limit generalization. Review, ownership and tool integration evolved together.

## What to borrow and adapt

Distinguish blocker, optional feedback and understanding questions. Inspect whether noisy automated comments have a feedback owner and can be improved. Measure local review delay or recurring misunderstanding before imposing a reviewer count, change-size target or new mandatory gate.

## Mismatches and limits

Small-change and fast-review observations are not a randomized demonstration that one policy causes better quality. Critique's analyzer feedback loop is a historical documented mechanism, not an available tool recommendation or a current Google-process audit. No review-log analysis or organizational intervention was reproduced.
