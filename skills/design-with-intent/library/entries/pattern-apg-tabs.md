---
{
  "id": "pattern-apg-tabs",
  "kind": "system",
  "title": "WAI-ARIA APG: tabs and activation",
  "summary": "Separate tab focus from panel activation and keep page panels distinct from app destinations.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "switch",
      "inspect",
      "navigate"
    ],
    "contexts": [
      "layered-content",
      "component-behavior"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/WAI/ARIA/apg/patterns/tabs/",
      "title": "Tabs pattern",
      "locator": "About; keyboard interaction; automatic activation note; roles/states/properties",
      "revision": "live documentation; not pinned to a source commit"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "pattern-material-navigation-bar",
    "pattern-apg-combobox"
  ],
  "flow_evidence": [
    {
      "url": "https://www.w3.org/WAI/ARIA/apg/patterns/tabs/",
      "locator": "Keyboard interaction and activation note",
      "sequence": [
        "Focus a tab",
        "Move among tabs using the documented keyboard model",
        "Activate manually or automatically according to the chosen latency-appropriate model",
        "Display associated panel; navigate into its content"
      ],
      "method": "Maintainer documentation sequence read as text; not executed."
    }
  ]
}
---

# WAI-ARIA APG: tabs and activation

## When to use

Use when a single page presents peer panels and only one needs to be displayed at a time. Ask whether these really are panels of one context or separate destinations that need routing, deep links and navigation history.

## What to inspect

Read focus movement, manual activation and automatic activation together. The guidance connects automatic activation with panel-display latency: moving focus should not unexpectedly force a slow load at every stop. Inspect the role relationships between the tab list, selected tab and its panel.

## What to borrow and adapt

Borrow explicit focus and activation decisions. In an inspector with Properties and History panels, arrows can explore tabs while the chosen activation model controls when content changes. Specify the selected state, loading behavior, focusable panel content and return path. Test keyboard behavior alongside pointer behavior and confirm that hidden panels do not leave confusing active controls.

## Mismatches and limits

Tabs are not a decorative name for any horizontal navigation. Compare the Material navigation-bar card for stable app destinations. A platform’s native tab control may have established behavior that should be retained. This inspection read the APG text; it did not execute examples, measure latency or test screen readers. Automatic activation is conditional guidance, not a universal preference for faster-looking interfaces.
