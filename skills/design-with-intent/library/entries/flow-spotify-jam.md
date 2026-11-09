---
{
  "id": "flow-spotify-jam",
  "kind": "example",
  "title": "Spotify Jam: shared queue with host control",
  "summary": "A co-present/remote collaboration flow where joining, contribution, playback authority and leaving have different scopes.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "join",
      "collaborate",
      "queue",
      "control"
    ],
    "contexts": [
      "consumer",
      "music",
      "group-decisions"
    ],
    "platforms": [
      "desktop-web",
      "native-mobile",
      "tv",
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://support.spotify.com/na-en/article/jam/",
      "title": "Spotify Support: Start or join a Jam",
      "locator": "Start/share; Join/add tracks; participant controls; host settings",
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
      "url": "https://support.spotify.com/na-en/article/jam/",
      "locator": "Start/share; Join/add tracks; participant controls; host settings",
      "sequence": [
        "Host starts a session",
        "Guest follows link/QR or proximity entry",
        "Choose local/remote context",
        "Join and add/reorder content within controls",
        "Host manages participation or ends session"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-airbnb-collaborative-wishlist",
    "flow-steam-family-roles",
    "principle-low-literacy-modalities"
  ]
}
---

# Spotify Jam: shared queue with host control

## When to use

Use for collaborative queues, co-present workshops or shared sessions where participants contribute but one device or person retains responsibility. Joining the session and controlling its effects are separate permissions.

## What to inspect

Read entry routes and host controls for the relevant platform; do not merge TV, car and phone behavior into one universal interface. Subscription and proximity requirements are access conditions, not design recommendations.

## What to borrow and adapt

Make the current session and output destination visible. For a shared presentation queue, explain who may add items, reorder them or change the active display. Offer an intentional joining route even when convenience discovery exists. Provide host controls and a clear exit rather than treating every participant as an equal administrator. Revisit which controls belong to personal devices and which affect everyone.

## Mismatches and limits

The public workflow was inspected without starting a session or changing playback. No current-device behavior or latency was tested. Automatic proximity entry may be inappropriate for private or consequential work; the source’s entertainment context does not establish informed consent elsewhere. Compare Airbnb for asynchronous deliberation and Steam for role-based authority.

## Related resource roles

- [principle-low-literacy-modalities](principle-low-literacy-modalities.md): A contrasting modality/access lens; shared listening is not evidence that every audience benefits from a voice-first interface.
