---
{
  "id": "system-atlassian",
  "kind": "system",
  "title": "Atlassian Design System",
  "summary": "Product-system guidance with useful distinctions between brand expression, product typography and token roles.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compose",
      "read",
      "operate"
    ],
    "contexts": [
      "enterprise",
      "collaboration",
      "productivity"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://atlassian.design/",
      "title": "Atlassian Design System",
      "locator": "Foundations; components; tokens and accessibility routes",
      "revision": "live documentation; not pinned to a source commit"
    },
    {
      "url": "https://atlassian.design/foundations/typography",
      "title": "Typography",
      "locator": "Typefaces; product versus brand use; typography tokens; legacy and fallback considerations",
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
    "system-primer",
    "system-carbon"
  ]
}
---

# Atlassian Design System

## When to use

Use when comparing systems for collaborative product UI or establishing typography roles in an existing application. Ask whether the work is a brand campaign, a product screen, or both, and what font licensing and platform fallback constraints already exist.

## What to inspect

Read the typography chapter’s separation of brand and product fonts, role tokens and fallback treatment. The source discusses Charlie Sans for brand contexts and Atlassian Sans/Mono for product work. Inspect the foundation and component routes for the specific surface; the homepage alone is not an adoption guide.

## What to borrow and adapt

Borrow the decision structure rather than the font names. For a planning application, define reading, heading, code and metadata roles, connect them to tokens, and test realistic content lengths. Keep marketing expression and dense working screens related through identity without requiring identical typographic treatment. Resolve hierarchy and scanning with representative tasks before choosing weights.

## Mismatches and limits

This source is a useful counterexample to universal prohibitions on bold headings or particular font categories: coherent systems make contextual decisions. It is not permission to redistribute Atlassian’s fonts or copy its brand. No typography screenshots were visually inspected and no package was executed. Accessibility requires rendered size, contrast, zoom, language and content checks in the resulting product.
