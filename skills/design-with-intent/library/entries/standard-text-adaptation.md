---
{
  "id": "standard-text-adaptation",
  "kind": "foundation",
  "title": "Accessible text: contrast, overrides and reflow",
  "summary": "Interpret contrast and text-adaptation requirements together without converting tolerance tests into fixed visual defaults or replacing every table with cards.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "typography",
      "accessibility",
      "responsive-design"
    ],
    "contexts": [
      "zoom",
      "user-overrides",
      "readability",
      "dense-information"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/TR/2024/REC-WCAG22-20241212/",
      "title": "WCAG 2.2",
      "locator": "SC 1.4.3, 1.4.10, 1.4.11 and 1.4.12",
      "revision": "Recommendation 12 December 2024"
    },
    {
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html",
      "title": "Understanding Text Spacing",
      "locator": "SC; notes; Author Responsibility",
      "revision": "Informative explanation accessed 2026-11-07"
    },
    {
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/reflow.html",
      "title": "Understanding Reflow",
      "locator": "SC; two-dimensional exceptions; reflowing applications",
      "revision": "Informative explanation accessed 2026-11-07"
    },
    {
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html",
      "title": "Understanding Contrast Minimum",
      "locator": "Thresholds; large text; incidental and logo exceptions; rendering notes",
      "revision": "Informative explanation accessed 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Versioned normative criteria and live explanatory text inspected. No contrast measurements or rendered adaptation tests of a product."
  },
  "reuse": "Original annotation and primary-source links only; no standard text, paper, figures or third-party assets redistributed. Preserve W3C/author source-specific terms for substantial reproduction.",
  "related": [
    "standard-wcag-conformance"
  ]
}
---

# Accessible text: contrast, overrides and reflow

## When to use

Use when a visual direction includes small or faint text, fixed-size cards, long translated labels, dense tables, or typography that must survive zoom and reader overrides.

## What to inspect

Read the relevant normative criteria and explanatory exceptions. Text Spacing defines tolerance for user overrides, not compulsory authored spacing. Reflow distinguishes vertical-scrolling width from horizontal-scrolling height and preserves essential two-dimensional content exceptions.

## What to borrow and adapt

Treat typography, layout and state as a connected system. Check actual foreground/background pairs, meaningful text roles, content-driven dimensions and enlarged text. Preserve access to labels, errors, controls and comparison information when content wraps.

For a dense table, assess cells and surrounding controls rather than automatically converting every row into a card. For an expressive heading, preserve its character while testing real long text and fallback rendering.

## Mismatches and limits

Meeting a nominal color ratio does not establish comfortable reading, and an exception for a logo or inactive element does not excuse unrelated text. Do not require the override test values as default CSS or infer complete accessibility from a screenshot. This is a scoped standard resource, not a palette, universal font-size rule or evidence of product conformance.
