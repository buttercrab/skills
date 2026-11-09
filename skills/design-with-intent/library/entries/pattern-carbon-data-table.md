---
{
  "id": "pattern-carbon-data-table",
  "kind": "system",
  "title": "Carbon: data table density and actions",
  "summary": "Task-based table sizing, selection, expansion and batch actions for operational data.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "select",
      "inspect",
      "batch-edit"
    ],
    "contexts": [
      "enterprise",
      "data-heavy",
      "expert-use"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines",
      "title": "Data table guidelines",
      "locator": "Sizing; selection and batch actions; expandable rows; toolbar; loading",
      "revision": "Stable; page updated 2026-09-30; React context inspected"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow",
      "visual-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Guidelines text and native Chrome sizing section inspected. Static density comparisons viewed; no live table actions executed."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-carbon",
    "pattern-carbon-empty-states"
  ],
  "visual_evidence": [
    {
      "url": "https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines#sizing",
      "locator": "Sizing table and five row-height comparison diagrams",
      "observed": "Examples distinguish several header/cell heights and associate row sizes with different use conditions.",
      "method": "Public HTTPS page viewed in native Chrome using CUA screenshot and accessibility tree."
    }
  ],
  "flow_evidence": [
    {
      "url": "https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines",
      "locator": "Selection and batch actions",
      "sequence": [
        "Select one or more rows",
        "Show batch-action bar; disable row-level actions in batch mode",
        "Execute a chosen batch action or cancel",
        "Leave selection mode"
      ],
      "method": "Maintainer documentation sequence read as text; not executed."
    }
  ]
}
---

# Carbon: data table density and actions

## When to use

Use when people compare records and act on one or several of them. Ask which columns support decisions, whether touch is common, how many rows are scanned, and whether users need spreadsheet-style editing or a record-oriented table.

## What to inspect

Inspect the sizing comparison, toolbar versus row actions, selection-to-batch-action transitions and expansion limits. The viewed sizing section compares five row sizes and their intended uses. Read its loading and overflow guidance before drawing a single idealized populated table.

## What to borrow and adapt

Borrow a deliberate relationship between density and work. In a moderation queue, keep identifying information visible, reveal batch actions only after selection, and define how cancellation returns to normal operation. Use a detail destination when expanded content no longer fits comfortably. Specify empty, loading, selection and permission states alongside the default view.

## Mismatches and limits

Carbon-specific sizing and action placement belong to its system; they are not universal pixel requirements. The documented pattern is not a full spreadsheet. Native Chrome inspection viewed the sizing guidance and comparison diagrams, but did not execute sorting, expansion or batch actions. The batch sequence below is documentation evidence. Large-data performance, responsive behavior and keyboard handling remain application verification tasks.
