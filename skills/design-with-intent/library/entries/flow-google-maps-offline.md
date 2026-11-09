---
{
  "id": "flow-google-maps-offline",
  "kind": "example",
  "title": "Google Maps: select, store and refresh offline areas",
  "summary": "A degraded-connectivity journey distinguishing downloaded coverage, available capabilities, storage and expiring information.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "prepare",
      "download",
      "navigate",
      "recover"
    ],
    "contexts": [
      "consumer",
      "travel",
      "offline"
    ],
    "platforms": [
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://support.google.com/maps/answer/6291838?hl=en",
      "title": "Google Maps Help: Download areas and navigate offline",
      "locator": "Select your own map; Use offline maps; Manage/update offline maps",
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
      "url": "https://support.google.com/maps/answer/6291838?hl=en",
      "locator": "Select your own map; Use offline maps; Manage/update offline maps",
      "sequence": [
        "Choose area while connected",
        "Adjust coverage and download",
        "Use supported offline capabilities within coverage",
        "Inspect expiry and update or remove stored area"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-slack-catch-up"
  ]
}
---

# Google Maps: select, store and refresh offline areas

## When to use

Use for fieldwork, travel or any mobile product that must explain what remains possible without a connection. The useful analogy is a prepared local subset with known limits, not simply an offline badge.

## What to inspect

Read the geographic-coverage requirement, unavailable offline functions and update paths. Source instructions differ by platform; this card specifically inspected Android guidance.

## What to borrow and adapt

Expose preparation state before the user loses connectivity. For a field checklist, distinguish stored tasks from live inventory or weather that cannot refresh. Explain scope, freshness and missing capabilities at the point they affect decisions. Let people manage stored regions/items and recover from expiration without assuming a background update succeeded. Plan the disconnected path as its own experience.

## Mismatches and limits

The guide was read; no map was downloaded and no navigation performed. Regional availability and route functions are product-specific. Cached data cannot automatically stand in for current truth. Avoid promising safety or live accuracy from this analogy. Slack’s catch-up queue offers a related example of explicitly refreshing rather than silently treating an older view as complete.
