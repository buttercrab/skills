---
{
  "id": "system-radix",
  "kind": "system",
  "title": "Radix Primitives",
  "summary": "Low-level React behavior primitives for teams that will supply their own visual system and composed UX.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compose",
      "implement",
      "customize"
    ],
    "contexts": [
      "custom-design-system",
      "component-engineering"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.radix-ui.com/primitives/docs/overview/introduction",
      "title": "Radix Primitives introduction",
      "locator": "Unstyled primitives; composition; controlled state; accessibility design goals",
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
    "pattern-radix-dialog",
    "pattern-apg-combobox",
    "pattern-fluent-dialog"
  ]
}
---

# Radix Primitives

## When to use

Use when the team needs reusable behavior under a custom visual identity and has the capacity to compose and test a product UI. Ask who owns styling, content, state, focus and integration across primitive boundaries.

## What to inspect

Read the introduction’s unstyled approach, composition and controlled-state model, then the exact primitive API. Inspect how a trigger, portal, content, labels and state callbacks cooperate. The companion dialog card includes one narrow demo interaction, which is stronger evidence than the introduction’s general capability claims.

## What to borrow and adapt

Borrow a separation between component behavior and visual tokens. For a bespoke research tool, use a primitive for a familiar interaction while defining clear names, task-specific actions and a coherent type/spacing system locally. Record how custom wrappers preserve semantics and ref/focus behavior. Choose the smallest abstraction that the project can maintain.

## Mismatches and limits

Primitives do not provide an information architecture, screen flow, brand or finished accessibility result. Styling and composition can undermine their intended behavior. The vendor’s accessibility goals are source claims rather than an independent audit. A team wanting ready-composed application pages should compare a fuller system. This card does not recommend introducing React or replacing an adequate native HTML control merely to use a primitive.
