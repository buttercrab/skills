---
{
  "id": "pattern-govuk-task-list",
  "kind": "system",
  "title": "GOV.UK: complete multiple tasks",
  "summary": "A resumable overview for genuinely long transactions with tasks, dependencies and meaningful status.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "resume",
      "navigate",
      "complete"
    ],
    "contexts": [
      "public-service",
      "multi-session",
      "complex-forms"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://design-system.service.gov.uk/patterns/complete-multiple-tasks/",
      "title": "Complete multiple tasks",
      "locator": "When to use; How it works; task status and dependencies",
      "revision": "live documentation; not pinned to a source commit"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-govuk",
    "pattern-govuk-check-answers"
  ],
  "flow_evidence": [
    {
      "url": "https://design-system.service.gov.uk/patterns/complete-multiple-tasks/",
      "locator": "How it works",
      "sequence": [
        "Open task overview",
        "Enter an available task",
        "Return to updated task status",
        "Resume remaining work on a later visit",
        "Complete the transaction"
      ],
      "method": "Maintainer documentation sequence read as text; not executed."
    }
  ]
}
---

# GOV.UK: complete multiple tasks

## When to use

Use for a transaction that realistically spans several tasks or sessions, such as preparing a grant application with separate evidence sections. First ask whether the service can be simplified, which tasks can be independent, and what must be retained between visits.

## What to inspect

Read the eligibility conditions before the task-list component. Inspect grouping, the start/return overview, the smallest useful status vocabulary, and unavailable dependent tasks. The guidance reserves the pattern for substantial work and distinguishes completed tasks from tasks requiring attention.

## What to borrow and adapt

Borrow an overview whose status reflects saved application state. Define what “complete” means for every task and whether later edits can invalidate another task. A resumed application should tell a person what remains, let them re-enter an allowed task, and give a clear route back. Model dependencies in the service, then expose them in readable language.

## Mismatches and limits

A task list is not evidence of autosave or recovery: those mechanisms must be implemented and tested. It is a poor fit for a short linear form where an overview adds navigation overhead. The source describes returning to and completing tasks; no persistence or multi-session application was exercised here. Compare check-answers when the actual need is final review rather than work orchestration.
