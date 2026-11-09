---
{
  "id": "flow-airbnb-collaborative-wishlist",
  "kind": "example",
  "title": "Airbnb: shared shortlists and planning context",
  "summary": "A consumer collaboration example separating saving, shared deliberation, view-only links and actual booking availability.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "save",
      "compare",
      "collaborate",
      "plan"
    ],
    "contexts": [
      "consumer",
      "travel",
      "group-decisions"
    ],
    "platforms": [
      "web",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.airbnb.com/help/article/1236",
      "title": "Airbnb Help: Use wishlists to save listings",
      "locator": "Save to a wishlist; Collaborate; collaborative/view-only sharing; unavailable listings",
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
      "url": "https://www.airbnb.com/help/article/1236",
      "locator": "Save to a wishlist; Collaborate; collaborative/view-only sharing; unavailable listings",
      "sequence": [
        "Save listing into a chosen list",
        "Invite planning collaborators or share view-only",
        "Add notes/votes and adjust trip context",
        "Recheck availability before booking"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-notion-view-sharing",
    "flow-spotify-jam"
  ]
}
---

# Airbnb: shared shortlists and planning context

## When to use

Use when people gather options and decide together over time: trips, venues, reading selections or equipment. Saving an option and committing to it must remain distinguishable.

## What to inspect

Read how dates remain attached to saved entries, what collaborators can change, and the difference between collaboration and view-only sharing. The removal/link caveat matters because removing a participant does not necessarily revoke an already distributed link.

## What to borrow and adapt

Attach the context that made an option attractive: date, party size, budget assumption or purpose. Give shared notes and preference expression without forcing immediate purchase. For a club choosing a venue, a shortlist can preserve members’ observations while the organizer checks current availability. Describe sharing scope honestly and separate selection votes from a binding decision.

## Mismatches and limits

Only the public documented flow was inspected. No account, invitation or reservation was created. A saved item can become unavailable, and a planning link is not a complete privacy model. The product’s exact limits and sharing rules should be rechecked before reuse. Compare Notion’s personal/shared view state and Spotify’s host/participant controls.
