---
{
  "id": "system-primer",
  "kind": "system",
  "title": "GitHub Primer",
  "summary": "Choose Product UI, Brand UI and supporting tokens according to the surface rather than copying one GitHub look everywhere.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compose",
      "read",
      "operate"
    ],
    "contexts": [
      "developer-tools",
      "product-ui",
      "brand-ui"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://primer.style/",
      "title": "Primer",
      "locator": "Product UI; Brand UI; Octicons; accessibility; token routes",
      "revision": "live documentation; not pinned to a source commit"
    },
    {
      "url": "https://primer.style/product/components/action-menu/",
      "title": "Action menu",
      "locator": "Component composition; availability and guideline routes",
      "revision": "live documentation; not pinned to a source commit"
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
    "pattern-primer-action-menu",
    "system-atlassian"
  ]
}
---

# GitHub Primer

## When to use

Use when studying a developer-oriented product system or separating an organization’s application and marketing references. Ask what task belongs in a working product and what belongs in a brand or promotional surface.

## What to inspect

Inspect the Product UI and Brand UI routes before reading components. Then check component implementation availability and the linked guidelines. The inspected action-menu route connects an overlay and action list; its existence does not establish that any arbitrary menu composition is suitable.

## What to borrow and adapt

Borrow the surface distinction and a common vocabulary of roles. For a deployment tool, choose operational components for frequent commands and status reading, while allowing the launch page its own composition within the broader identity. Keep icon, token and accessibility decisions consistent across the selected product family. The companion action-menu card supplies a more specific decision about commands versus input.

## Mismatches and limits

GitHub’s interaction and visual conventions are not neutral defaults for every audience. A novice public service or expressive publication may need different references. No rendered Primer screen or React/Rails implementation was tested here. Product and Brand routes are related resources, not independent validation of one another. Package readiness, exact API support and downstream accessibility must be checked for the project’s version.
