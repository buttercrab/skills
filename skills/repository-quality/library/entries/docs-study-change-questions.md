---
{
  "id": "docs-study-change-questions",
  "kind": "study",
  "title": "Sillito et al.: inspect connected change questions, not just the tree",
  "summary": "Use qualitative observations of maintenance work to probe whether contributors can locate and connect the information a real change requires.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "navigate",
      "contribute",
      "quality"
    ],
    "contexts": [
      "program-comprehension",
      "maintenance-tasks"
    ],
    "languages": [
      "language-agnostic",
      "java"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://www.cs.ubc.ca/~murphy/papers/other/asking-answering-fse06.pdf",
      "title": "Questions Programmers Ask During Software Evolution Tasks",
      "locator": "Sections 3.1–3.2 methods; 4–5 question/answer categories; 7.1–7.2 limitations",
      "revision": "FSE 2006 primary author PDF"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Primary PDF methods, results categories and limitations freshly read. Historical qualitative evidence; no participant data reanalysis or repository experiment."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "docs-github-contribution-entry",
    "repo-small-p-limit"
  ]
}
---

# Sillito et al.: inspect connected change questions, not just the tree

## When to use

Use when a repository assessment equates neat folders with easy maintenance.

## What to inspect

Two qualitative studies observed nine newcomers in paired Java tasks and sixteen industrial programmers in their normal settings. The authors categorized 44 kinds of questions and connected searches. Tasks and tool contexts varied; completion improvement was not measured.

## What to borrow and adapt

Trace one realistic change from a domain term or error message through callers, related data, tests and ownership. Record where navigation loses the relationships already discovered. A short contributor map may address that gap better than a broad directory rename.

## Mismatches and limits

The paper does not establish a preferred tree, universal question checklist or causal benefit from a new tool. Pairing, think-aloud observation, complex tasks and historical tool environments limit transfer. The authors did not rank questions by importance. This card freshly inspected methods and limitations; no task study was reproduced.
