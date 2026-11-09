---
{
  "id": "tool-playwright",
  "kind": "tool",
  "title": "Playwright: interaction and visual comparison evidence",
  "summary": "Browser automation with explicit actions/assertions, accessibility integration and environment-sensitive screenshot comparison.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "verify",
      "compare",
      "inspect"
    ],
    "contexts": [
      "components",
      "forms",
      "regression-testing",
      "accessibility"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://playwright.dev/docs/accessibility-testing",
      "title": "Accessibility testing",
      "locator": "Introduction limitations; state activation before scan",
      "revision": "live documentation inspected 2026-11-07"
    },
    {
      "url": "https://playwright.dev/docs/test-snapshots",
      "title": "Visual comparisons",
      "locator": "Introduction; environment warning; generating/updating screenshots",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official accessibility and visual-comparison documentation inspected. No browser test or screenshot comparison executed."
  },
  "reuse": "Original annotation and links only. No upstream software, screenshots, templates or proprietary assets redistributed.",
  "related": [
    "tool-axe-core",
    "tool-storybook"
  ]
}
---

# Playwright: interaction and visual comparison evidence

## When to use

Select Playwright when the task needs repeatable evidence that an implemented interaction reaches the expected state or a known design changed unexpectedly. It is a verification capability match, not a source of brand or flow design.

## What to inspect

Read the action/assertion guidance relevant to the flow, the accessibility example’s state setup, and the screenshot-environment warnings. Confirm the repository’s existing framework and browser setup before introducing another test path. A screenshot baseline is a versioned artifact whose origin matters.

## What to borrow and adapt

Borrow observable sequences: select, submit, encounter an error, correct, confirm and reset. Assert the meaningful state at each consequential transition. Reach hidden content before scanning it. Use screenshots to compare composition under controlled rendering conditions, then inspect whether a detected difference is expected. Separate automation, manual accessibility review and intended-user testing.

## Mismatches and limits

A passing pixel comparison can preserve a bad design; a failing one can reflect fonts, operating system or hardware rather than a product regression. Automated accessibility scans catch only part of the problem. Tool access must be explicitly permitted; a browser denial is not permission to retry by another route. No package, browser or test was installed/executed for this card.
