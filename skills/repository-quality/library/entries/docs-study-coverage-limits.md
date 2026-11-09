---
{
  "id": "docs-study-coverage-limits",
  "kind": "study",
  "title": "Inozemtseva and Holmes: coverage is an incomplete quality signal",
  "summary": "Keep coverage, test-suite size and fault-detection evidence separate when deciding which tests a repository needs.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "metrics",
      "test-selection",
      "quality"
    ],
    "contexts": [
      "coverage",
      "regression-confidence"
    ],
    "languages": [
      "java"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://cs.uwaterloo.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf",
      "title": "Coverage Is Not Strongly Correlated with Test Suite Effectiveness",
      "locator": "Section 3 methods; results controlling suite size; section 6 threats",
      "revision": "ICSE 2014 primary author PDF; method inspection retained from earlier 2026-11-07 REP-24 dossier"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Historical substantive method/result inspection attributed to earlier repositories dossier REP-24; this lane refreshed opening pages only, then method/limits reads repeatedly timed out. No fresh full-method or empirical replication claim."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "quality-python-distribution-checks",
    "repo-large-django"
  ]
}
---

# Inozemtseva and Holmes: coverage is an incomplete quality signal

## When to use

Use when a percentage threshold is proposed as proof of repository quality or a substitute for selecting relevant failure scenarios.

## What to inspect

The retained study record describes sampled suites across five large Java systems, with fault detection approximated using mutation and suite size controlled. Its headline association changes after controlling for size.

## What to borrow and adapt

Use uncovered changed behavior as an investigation lead. Ask which assertion distinguishes a real regression and which supported environment matters. A high percentage with weak assertions can still miss the contract; a lower aggregate does not establish that a particular patch is untested.

## Mismatches and limits

This is not evidence that coverage is useless or that a team's existing gate should be lowered. Generated suites, mutants and sampled Java systems limit transfer. Substantive methods/results evidence is retained from the earlier same-day dossier; this lane fetched the opening but repeated method-section reads timed out. It did not independently revalidate those methods or reproduce the experiment.
