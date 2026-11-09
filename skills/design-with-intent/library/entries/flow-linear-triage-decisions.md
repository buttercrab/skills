---
{
  "id": "flow-linear-triage-decisions",
  "kind": "example",
  "title": "Linear Triage: accept, decline, duplicate or snooze",
  "summary": "Match an intake queue where unresolved items require explicit disposition and temporary deferral remains distinguishable from rejection.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "review",
      "prioritize",
      "defer",
      "resolve"
    ],
    "contexts": [
      "operations",
      "collaboration",
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
      "url": "https://linear.app/docs/triage",
      "title": "Linear Docs: Triage",
      "locator": "Basics → Create issues / Take actions; Configure",
      "revision": "not-versioned; live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Relevant first-party text and described transitions inspected; no authenticated product interaction or visual inspection."
  },
  "flow_evidence": [
    {
      "url": "https://linear.app/docs/triage",
      "locator": "Basics → Create issues / Take actions; Configure",
      "sequence": [
        "Incoming issue enters triage",
        "Review context",
        "Accept to team default status, decline, merge duplicate, or snooze",
        "Snoozed issue returns at time or earlier activity"
      ],
      "method": "First-party documented workflow/account read through web tool; not interaction-tested."
    }
  ],
  "reuse": "Link and original annotation only. No upstream screenshots, assets or instructions redistributed; page-specific copying terms not established.",
  "related": [
    "flow-figma-ui3-state-visibility",
    "pattern-carbon-data-table",
    "principle-goals-signals-metrics"
  ]
}
---

# Linear Triage: accept, decline, duplicate or snooze

## When to use

Use for support intake, editorial submissions, exception handling, or requests that need a human decision before entering normal work. It is particularly relevant when “not now,” “not valid,” and “already represented” should remain separate outcomes.

## What to inspect

Read the creation rules and Take actions section. Inspect the snooze return conditions, the canceled result for declined/duplicate work, and the scope of visibility. Also note that configured templates can alter entry behavior; the product's default is not the whole contract.

## What to borrow and adapt

Write a small disposition model before choosing queue controls. For example, an organizer reviewing volunteer applications may need a request-for-information state and a reminder without implying rejection. Make each outcome's next destination and ownership explicit. Preserve a canonical item when consolidating duplicates, including relevant attachments or context.

Adapt the available actions to the domain's promises. Keyboard shortcuts are useful implementation detail for repeated work, but should not become the only discoverable route. Pair the queue with enough context to make a decision instead of optimizing only for clearing the count.

## Mismatches and limits

The current documentation was read, not an authenticated workspace exercised. Paid automation and AI suggestions are outside this case; no recommendation depends on purchasing them. Snooze visibility and defaults are product-specific. A personal reading list or a checkout form may not need four dispositions. Compare Figma's state-visibility case when the important job is continuous inspection rather than intake resolution.

## Related resource roles

- [pattern-carbon-data-table](pattern-carbon-data-table.md): Use table and batch-context guidance when the intake task requires comparing several items.
- [principle-goals-signals-metrics](principle-goals-signals-metrics.md): Choose outcome evidence beyond the number of items cleared from a queue.
