---
{
  "id": "docs-github-codeowners",
  "kind": "guide",
  "title": "GitHub CODEOWNERS: routing and enforced review are separate",
  "summary": "Inspect pattern precedence, branch identity and actual rules before claiming a committed owner map enforces review.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "ownership",
      "review"
    ],
    "contexts": [
      "github-hosting",
      "review-routing"
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
      "url": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners",
      "title": "GitHub Docs: About code owners",
      "locator": "file location/base branch; syntax/last matching pattern; branch protection and multiple owners",
      "revision": "Live official documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official feature semantics freshly read, including syntax and enforcement sections; no repository settings, permissions or sample PR tested."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "docs-github-contribution-entry",
    "quality-scorecard-diagnostic-limits"
  ]
}
---

# GitHub CODEOWNERS: routing and enforced review are separate

## When to use

Use when reviewers are difficult to find or a team wants to check whether its ownership map actually protects changes.

## What to inspect

Check the file location GitHub selects, the pull request's base branch and the last matching pattern. Owners require suitable access; syntax errors or inaccessible teams can defeat intended routing. Requiring owner approval is a separate repository-rule configuration. Multiple owners on one rule do not mean all must approve.

## What to borrow and adapt

Map a sample changed path to the intended maintainers, then verify the hosted rule and permissions when making enforcement claims. A small team may need a short ownership explanation rather than many patterns.

## Mismatches and limits

This is GitHub-specific mutable behavior. Reading CODEOWNERS establishes declared routing, not enabled protection, response capacity or review quality. This card inspected the documentation, not any repository's live settings; adding the file alone should not be reported as completing enforcement.
