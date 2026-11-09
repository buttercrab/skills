---
{
  "id": "flow-steam-family-roles",
  "kind": "example",
  "title": "Steam Families: role-aware requests and shared access",
  "summary": "A gaming-household case distinguishing who requests, who authorizes and which state belongs to each account.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "invite",
      "request",
      "approve",
      "manage-access"
    ],
    "contexts": [
      "games",
      "household",
      "role-based"
    ],
    "platforms": [
      "desktop-web",
      "native-mobile",
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://help.steampowered.com/en/faqs/view/054C-3167-DD7F-49D4?l=english",
      "title": "Steam Support: Steam Families User Guide and FAQ",
      "locator": "Feature overview; setup; adult/child roles; purchase requests; sharing limitations",
      "revision": "not-versioned; documentation inspected 2026-11-07"
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
    "scope": "Relevant first-party documented sequence/state account inspected; no authenticated live product workflow exercised."
  },
  "flow_evidence": [
    {
      "url": "https://help.steampowered.com/en/faqs/view/054C-3167-DD7F-49D4?l=english",
      "locator": "Feature overview; setup; adult/child roles; purchase requests; sharing limitations",
      "sequence": [
        "Create family",
        "Invite adult or child role",
        "Invitee receives alert",
        "Child requests an action",
        "Adult reviews/authorizes according to the feature"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-signal-usernames",
    "flow-spotify-jam"
  ],
  "visual_evidence": [
    {
      "url": "https://help.steampowered.com/en/faqs/view/054C-3167-DD7F-49D4?l=english",
      "locator": "Setting up a Steam Family embedded account-menu screenshot",
      "observed": "Help image highlights Account details and then Family Management, followed by textual create/invite/role steps.",
      "method": "Own approved public HTTPS Chrome tab; CUA screenshot visually inspected 2026-11-07. No account interaction."
    }
  ]
}
---

# Steam Families: role-aware requests and shared access

## When to use

Use for a shared household or supervised group where requesters and decision-makers have different powers. It is useful when an action offered to one person should not imply authority to complete the whole transaction.

## What to inspect

Read the role distinction and setup instructions, then the specific request feature needed. An embedded setup screenshot was viewed: account menu leads to Account details and Family Management. It is help imagery, not a live account workflow.

## What to borrow and adapt

Model who sees a request, who may decide, and where the result appears. For shared equipment, a member could request access while a designated owner authorizes it. Keep personal progress and shared availability distinct. Explain unavailable resources and waiting honestly instead of showing every item as immediately usable. Choose role labels people understand before copying permission structures.

## Mismatches and limits

No family was created, role changed, account recovered or purchase attempted. The source’s household rules, restrictions and cooldowns are specific and mutable. This is not parental-control, security or purchasing advice. Do not generalize one account’s authority to every collaborator. Compare Signal for identity/discoverability and Spotify for session-level controls.
