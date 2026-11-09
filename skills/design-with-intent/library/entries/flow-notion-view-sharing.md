---
{
  "id": "flow-notion-view-sharing",
  "kind": "example",
  "title": "Notion: personal versus shared database views",
  "summary": "A multi-view workspace case for distinguishing presentation state, underlying records and changes that affect other collaborators.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "filter",
      "compare",
      "organize",
      "configure"
    ],
    "contexts": [
      "collaboration",
      "operations",
      "expert-repeated"
    ],
    "platforms": [
      "desktop-web",
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.notion.com/help/views-filters-and-sorts",
      "title": "Notion Help: Views, filters, sorts and groups",
      "locator": "View settings; Open pages in; Filters; Sorts",
      "revision": "not-versioned; documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Relevant first-party documented sequence/state account inspected; no authenticated live product workflow exercised."
  },
  "flow_evidence": [
    {
      "url": "https://www.notion.com/help/views-filters-and-sorts",
      "locator": "View settings; Open pages in; Filters; Sorts",
      "sequence": [
        "Choose a database view",
        "Change layout/filter/sort",
        "Keep a personal change or save for everyone",
        "Open item detail while retaining or leaving list context"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-airbnb-collaborative-wishlist",
    "flow-linear-triage-decisions"
  ]
}
---

# Notion: personal versus shared database views

## When to use

Use for dashboards or collaborative collections with several ways to inspect the same records. It is especially useful when a personal filtering action could unexpectedly change a shared working view.

## What to inspect

Read the per-view settings scope, filter/sort save-for-everyone choice and side/center/full-page item opening. The source describes multiple scopes; it should not be flattened into one global filter state.

## What to borrow and adapt

Model records, view definitions and temporary personal state separately. In a volunteer roster, someone finding their own shift should not silently alter the coordinator’s default overview. Make the audience of a saved view change explicit. Choose detail opening from the need to compare adjacent records, inspect a focused object or navigate deeply; preserve a clear return path.

## Mismatches and limits

Documentation and described states were read; no workspace or permission configuration was tested. A filtered view is not, by itself, an authorization boundary. The case does not recommend every display mode or the product’s database model for small lists. Airbnb wishlists provide a contrasting collaboration flow where members intentionally contribute to shared planning.
