---
{
  "id": "tool-lighthouse",
  "kind": "tool",
  "title": "Lighthouse: scoped page-quality diagnostics",
  "summary": "An automated page-audit tool for performance, accessibility and other diagnostics, useful as one bounded source of implementation evidence.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "audit",
      "verify",
      "optimize"
    ],
    "contexts": [
      "performance",
      "accessibility",
      "product-interface"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://developer.chrome.com/docs/lighthouse/overview",
      "title": "Introduction to Lighthouse",
      "locator": "Workflow options; audit interpretation; local/authenticated DevTools; report sharing",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official overview and audit/workflow scope inspected. Lighthouse was not executed."
  },
  "reuse": "Original annotation and links only. No upstream software, screenshots, templates or proprietary assets redistributed.",
  "related": [
    "tool-axe-core",
    "skill-vercel-react-performance"
  ]
}
---

# Lighthouse: scoped page-quality diagnostics

## When to use

Select Lighthouse when a working web page needs repeatable diagnostics of loading or automatically checkable quality properties. It can help investigate why an otherwise coherent design feels slow or exposes avoidable technical problems.

## What to inspect

Read the workflow options and audit references rather than treating the aggregate score as the result. Choose an authorized local, authenticated or public-page route appropriate to the task. Check the tool/browser version and test conditions before comparing reports.

## What to borrow and adapt

Borrow using a failed diagnostic as a question with a traceable element or mechanism. Connect the result to the intended user path: a shifted action, delayed content, missing name or blocking script has a specific consequence. Preserve the report configuration so a later comparison measures the same conditions. Keep local reports local unless sharing is requested.

## Mismatches and limits

A good score does not establish task completion, accessibility conformance, comprehension or visual relevance. A single page-load run also omits many later states. The official documentation includes optional hosted analysis and report-sharing operations; selecting this resource does not authorize sending a private URL or report to them. No audit, installation, report upload or real page test was performed during curation.
