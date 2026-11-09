---
{
  "id": "flow-meetup-waitlist",
  "kind": "example",
  "title": "Meetup: waitlisted versus attending",
  "summary": "A community-capacity case showing why joining a queue, promotion rules and confirmed attendance need distinct meanings.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "join",
      "wait",
      "cancel",
      "track-status"
    ],
    "contexts": [
      "community",
      "events",
      "consumer"
    ],
    "platforms": [
      "web",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://help.meetup.com/hc/en-us/articles/41229648295181-How-to-Join-an-Event-Waitlist-on-Meetup",
      "title": "Meetup Help: How to Join an Event Waitlist",
      "locator": "What is a Waitlist; joining; promotion order; mandatory fees; status",
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
      "url": "https://help.meetup.com/hc/en-us/articles/41229648295181-How-to-Join-an-Event-Waitlist-on-Meetup",
      "locator": "What is a Waitlist; joining; promotion order; mandatory fees; status",
      "sequence": [
        "Event full",
        "Join waitlist",
        "Remain waiting or leave",
        "Eligible vacancy triggers promotion",
        "Notification and Going state"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-shopify-checkout-layout",
    "flow-discord-community-onboarding",
    "pattern-govuk-error-summary"
  ]
}
---

# Meetup: waitlisted versus attending

## When to use

Use for limited-capacity groups, workshops or appointments where interest does not immediately reserve a place. It helps expose assumptions hidden behind a reassuring confirmation.

## What to inspect

Read eligibility, party-size handling and ordering, not merely the join button. The document distinguishes paid membership priority and mandatory-fee events. Those business rules are context, not universal queue design advice.

## What to borrow and adapt

Write separate status language for requested, waiting and confirmed. Explain whether promotion is automatic, who is eligible, how a group is fitted, and how someone leaves. For a local event, choose a fair ordering rule deliberately and tell people what notification means. An explicit waiting label may be clearer than requiring users to infer it from absence of an attending badge.

## Mismatches and limits

The source was read, not the event experience tested. Do not infer a strict FIFO queue or copy paid-priority rules into an unrelated community. A queue notification is not proof that everyone has seen it. The Eventbrite discovery lead in this library is not yet inspected enough to serve as a vetted alternative.

## Related resource roles

- [pattern-govuk-error-summary](pattern-govuk-error-summary.md): A complementary recovery pattern; preserve the event’s actual capacity and waitlist promises rather than importing a generic error flow.
