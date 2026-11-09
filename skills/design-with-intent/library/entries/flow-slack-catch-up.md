---
{
  "id": "flow-slack-catch-up",
  "kind": "example",
  "title": "Slack: catch up, skip and undo",
  "summary": "A mobile/desktop attention queue where acknowledgement, deferral, recovery and the source conversation are distinct actions.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "review",
      "catch-up",
      "defer",
      "recover"
    ],
    "contexts": [
      "collaboration",
      "messaging",
      "repeated-use"
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
      "url": "https://slack.com/help/articles/226410907-View-all-your-unread-messages",
      "title": "Slack Help: View all your unread messages",
      "locator": "View/Navigate unread messages; Mark as read; Refresh; Reply",
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
      "url": "https://slack.com/help/articles/226410907-View-all-your-unread-messages",
      "locator": "View/Navigate unread messages; Mark as read; Refresh; Reply",
      "sequence": [
        "Open unread/catch-up view",
        "Review a conversation preview",
        "Mark read or skip",
        "Undo premature acknowledgement",
        "Return to original conversation"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-linear-triage-decisions",
    "flow-google-maps-offline"
  ]
}
---

# Slack: catch up, skip and undo

## When to use

Use for an activity feed, operational notification inbox or mobile catch-up experience. The relevant mechanism is processing attention without confusing “seen,” “done,” and “deferred.”

## What to inspect

Read mobile swipe/undo behavior alongside desktop acknowledgement and collapse behavior. Note how new messages appear and how users enter the original conversation. English and Japanese official text were read; neither app was operated.

## What to borrow and adapt

Give a reversible acknowledgement and a separate way to leave work for later. In a neighborhood event feed, dismissing a notice should not enroll the person or complete an organizer task. Preserve enough preview context to decide, with an escape to the original item. Make gesture actions discoverable and provide equivalent controls; measure repeated review rather than only swipe speed.

## Mismatches and limits

This documents product behavior, not its effectiveness. Desktop and mobile controls differ; do not copy a swipe model into a keyboard-only work queue. Read state is not a reliable substitute for business completion or responsibility. Compare Linear Triage for explicit dispositions with durable workflow consequences.
