---
{
  "id": "pattern-primer-action-menu",
  "kind": "system",
  "title": "Primer: action menu boundaries",
  "summary": "Keep command menus distinct from form inputs, and make hierarchy and disabled reasons understandable.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "act",
      "select",
      "configure"
    ],
    "contexts": [
      "developer-tools",
      "command-menu"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://primer.style/product/components/action-menu/guidelines/",
      "title": "Action menu guidelines",
      "locator": "Usage; content; hierarchy; disabled items; trailing visuals",
      "revision": "live documentation; not pinned to a source commit"
    },
    {
      "url": "https://primer.style/product/components/action-menu/",
      "title": "Action menu",
      "locator": "Composition and use cases",
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
    "pattern-apg-combobox",
    "pattern-fluent-dialog"
  ]
}
---

# Primer: action menu boundaries

## When to use

Use when contextual commands need a compact entry point. Ask whether users are executing actions, choosing a value, searching a long set, or filling out a form; those jobs may require different controls.

## What to inspect

Read the boundaries around nested inputs, filterable options and dialog alternatives. Inspect hierarchy, trailing visuals, icon conventions and disabled-item explanations. Primer’s guidance keeps disabled items focusable and provides explanation inline rather than relying on a nested tooltip; adopt this with the selected implementation’s complete keyboard model.

## What to borrow and adapt

Borrow an explicit menu-content contract. For a repository action list, group commands by purpose, use labels that predict results, and reserve trailing space consistently for its chosen meaning. If an item cannot run, explain why at the point of encounter. Move a multi-field setup into a suitable form surface. Compare APG combobox when the true task is supplying an input value.

## Mismatches and limits

Checkmarks, icons and focus treatment must remain coherent with the host system; mixing conventions can make selection and command state ambiguous. Primer-specific icon consistency is a house rule, not proof that every menu needs icons. This card records source guidance only: the menu, submenus, focus navigation and disabled explanations were not exercised. Touch and assistive-technology behavior require composed-product testing.
