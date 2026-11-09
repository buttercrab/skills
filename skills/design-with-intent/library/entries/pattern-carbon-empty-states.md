---
{
  "id": "pattern-carbon-empty-states",
  "kind": "system",
  "title": "Carbon: empty states by cause",
  "summary": "Separate first use, user-driven empty results and errors before choosing explanation and action.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "start",
      "recover",
      "search"
    ],
    "contexts": [
      "enterprise",
      "first-use",
      "no-results"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states",
      "title": "Empty states",
      "locator": "Types; content; illustration and call-to-action guidance",
      "revision": "Page updated 2026-08-11; not pinned"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-carbon",
    "pattern-carbon-data-table",
    "flow-linear-triage-decisions"
  ]
}
---

# Carbon: empty states by cause

## When to use

Use when a region contains no useful data and the agent is tempted to place the same illustration and “Get started” button everywhere. Ask whether there is genuinely no data, a filter excludes it, access is restricted, or retrieval failed.

## What to inspect

Read the cause distinctions and the guidance on content, available space and actions. The source distinguishes initial states, user outcomes and errors. It does not require a large image in every empty region. This inspection read the text, not the visual examples.

## What to borrow and adapt

Borrow a cause-to-next-step decision. A first project can invite creation; a filtered table can offer filter adjustment; an unavailable service may need retry or support. For each, explain the situation using facts the system actually knows. Match the amount of illustration and explanation to the surrounding task and region size, and preserve the controls needed to recover.

## Mismatches and limits

An empty state cannot fix missing authorization logic, indistinguishable loading/failure responses, or a lack of useful product functionality. Illustration style and brand voice need separate references and user direction. Do not promise a retry succeeds or imply data was deleted without evidence. This card offers a state-classification method; it is not an experimentally validated claim that one composition converts better.

## Related resource roles

- [flow-linear-triage-decisions](flow-linear-triage-decisions.md): Queue completion, filtering and deferred items can all appear empty while requiring different explanations.
