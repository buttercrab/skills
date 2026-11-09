---
{
  "id": "system-carbon",
  "kind": "system",
  "title": "Carbon Design System",
  "summary": "IBM-oriented system selection for data-heavy products, including components, patterns and visualization guidance.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "inspect",
      "compare",
      "operate"
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
      "url": "https://www.carbondesignsystem.com/",
      "title": "Carbon Design System",
      "locator": "System overview; foundations/components/patterns/data visualization; future v12 notice",
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
    "pattern-carbon-data-table",
    "pattern-carbon-empty-states"
  ]
}
---

# Carbon Design System

## When to use

Use as a candidate when teams need coherent conventions for a substantial operational product. Ask about operator expertise, data volume, repetition, accessibility support and the cost of adopting an existing component family.

## What to inspect

Start at components and patterns for the real job, then check implementation and version. The inspected homepage exposes foundations, data visualization and related building blocks; it also discusses future v12 work. An announcement about future visuals does not identify the behavior of the currently installed library.

## What to borrow and adapt

Borrow the method of connecting tokens, interaction guidance and task patterns. For an inventory console, compare the data-table guidance with empty states before choosing density and actions. Write a local mapping from supported user tasks to selected components, and use that mapping to avoid inventing slightly different controls on every screen.

## Mismatches and limits

Carbon carries IBM product and brand assumptions. A public cultural publication or casual mobile game may need a different reference family. The homepage establishes ecosystem scope, not measured usability, complete accessibility conformance or a rendered visual match. Read the specific component implementation and test its composed behavior. The companion table and empty-state cards provide narrower entry points.
