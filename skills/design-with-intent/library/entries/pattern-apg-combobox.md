---
{
  "id": "pattern-apg-combobox",
  "kind": "system",
  "title": "WAI-ARIA APG: combobox decision and behavior",
  "summary": "Distinguish editable suggestions from constrained selection and choose the popup model deliberately.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "search",
      "select",
      "enter"
    ],
    "contexts": [
      "forms",
      "typeahead",
      "constrained-input"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/WAI/ARIA/apg/patterns/combobox/",
      "title": "Combobox pattern",
      "locator": "About; keyboard interaction; roles/states/properties; editable and select-only distinctions",
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
    "system-radix",
    "pattern-primer-action-menu"
  ]
}
---

# WAI-ARIA APG: combobox decision and behavior

## When to use

Use when the input may combine typing and choosing, especially when a large option set tempts the agent to build a custom autocomplete. Ask whether arbitrary values are valid, whether suggestions are optional, and whether a native select already solves the task.

## What to inspect

Read editable and select-only distinctions before keyboard details. Inspect the popup type and associated focus/state expectations: listbox, grid, tree and dialog are not interchangeable presentation skins. Expansion and selection rules must match the actual interaction contract.

## What to borrow and adapt

Borrow a state model that distinguishes typed text, active suggestion, committed value, expanded state and validation. For a city picker, decide whether the person must choose a known location or may supply a new one; that choice changes the implementation and error messages. Write and test keyboard paths for opening, moving, committing and cancelling, including no results and slow suggestions.

## Mismatches and limits

ARIA attributes alone do not create working behavior. APG is pattern guidance, and the exact example still needs browser and assistive-technology testing in the product. No combobox demo was executed here. Do not import all optional keyboard behaviors into a simple control or replace adequate native HTML without a task-based reason. Compare an action menu when the items execute commands rather than supply an input value.
