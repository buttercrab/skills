---
{
  "id": "docs-google-change-review",
  "kind": "guide",
  "title": "Google review guidance: code health, scope and nonblocking preferences",
  "summary": "Review concrete design, behavior, useful tests and affected documentation while separating requirements from optional polish.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "review",
      "document",
      "quality"
    ],
    "contexts": [
      "maintainer-review",
      "incremental-improvement"
    ],
    "languages": [
      "language-agnostic"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://google.github.io/eng-practices/review/reviewer/looking-for.html",
      "title": "What to look for in a code review",
      "locator": "Design; Complexity; Tests; Style; Documentation; Exceptions",
      "revision": "Live primary guidance inspected 2026-11-07"
    },
    {
      "url": "https://google.github.io/eng-practices/review/reviewer/standard.html",
      "title": "The standard of code review",
      "locator": "Continuous code-health improvement; Principles; Resolving Conflicts",
      "revision": "Live primary guidance inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Two official review-guidance pages freshly read; no change review or organizational rollout executed."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "docs-study-google-review",
    "repo-small-p-limit"
  ]
}
---

# Google review guidance: code health, scope and nonblocking preferences

## When to use

Use when review debates drift into preferences, a large cleanup obscures behavior, or contributors cannot tell which feedback blocks their change.

## What to inspect

Read review criteria together with the balancing standard. The guidance discusses overall code health and progress, useful assertions, overengineering, changed user/developer behavior and documentation. It explicitly separates optional style suggestions from established rules and permits bounded review scopes.

## What to borrow and adapt

Tie a finding to a concrete change consequence and an applicable project rule. Label educational or cosmetic suggestions as optional. A change to a build command should carry its relevant contributor documentation; unrelated reformatting can be separate. Ask whether a test would catch the defect, rather than accepting it solely because a test file exists.

## Mismatches and limits

These are published practices from a particular engineering culture, not evidence that its approval structure fits every team. The guidance is not an instruction to block a reversible local task on invented approvals. Source review, a demonstration and an executed regression test support different claims; preserve the scope actually reviewed.
