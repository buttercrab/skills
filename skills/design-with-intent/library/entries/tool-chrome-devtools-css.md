---
{
  "id": "tool-chrome-devtools-css",
  "kind": "tool",
  "title": "Chrome DevTools: inspect applied CSS rather than infer tokens",
  "summary": "An implementation-inspection route for applied declarations, box geometry and pseudostates, useful when reconstructing a design from real rendering.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "inspect",
      "repair",
      "document"
    ],
    "contexts": [
      "existing-product",
      "design-system",
      "components"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://developer.chrome.com/docs/devtools/css",
      "title": "View and change CSS",
      "locator": "Applied styles; class/pseudostate toggles; box model",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official CSS inspection tutorial read; no DevTools or target page interaction performed."
  },
  "reuse": "Original annotation and links only. No upstream software, screenshots, templates or proprietary assets redistributed.",
  "related": [
    "skill-create-design-md",
    "tool-lighthouse"
  ]
}
---

# Chrome DevTools: inspect applied CSS rather than infer tokens

## When to use

Select DevTools CSS inspection when an authorized rendered page must be understood at the level of applied declarations or layout geometry. It helps distinguish exact implementation observations from visual estimates while investigating a mismatch or reconstructing limited design guidance.

## What to inspect

Read the applied-style, pseudostate and box-model examples. Inspect the actual element and state in the intended viewport, with its cascade and relevant stylesheet. A declared custom property is not necessarily the value currently used by the element.

## What to borrow and adapt

Borrow evidence from the rendered consumer: which rule wins, what changes under a state, and which dimensions derive from content or constraints. Connect repeated values to their actual owners before calling them a shared token system. A locally toggled declaration can test a small hypothesis; preserve its provisional status and implement the real fix in source only when requested.

## Mismatches and limits

One element’s computed value does not establish a site-wide intention, reusable scale or accessibility outcome. Browser overrides can mask source defects and disappear on reload. Access to a browser inspection tool does not authorize reading unrelated private tabs or bypassing URL policy. This card inspected the official tutorial only; no page, computed style or visual was examined during this curation.
