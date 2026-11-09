---
{
  "id": "pattern-saga-compensation",
  "kind": "pattern",
  "title": "Sagas: coordinate local commits without pretending they are global rollback",
  "summary": "Model compensation, concurrency and terminal outcomes for work that genuinely spans independent owners.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "model-failure",
      "compare",
      "diagram"
    ],
    "contexts": [
      "cross-service-transactions",
      "compensation",
      "workflow-coordination"
    ],
    "qualities": [
      "consistency",
      "operability",
      "availability"
    ],
    "scale": [
      "multi-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://microservices.io/patterns/data/saga.html",
      "title": "Richardson: Saga",
      "locator": "choreography/orchestration; explicit compensation; lack of isolation; client outcome",
      "revision": "mutable original-author catalog; inspected 2026-11-07"
    },
    {
      "url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/saga",
      "title": "Microsoft: Saga distributed transactions",
      "locator": "local commits, pivot concepts, compensation failures and data anomalies",
      "revision": "mutable first-party guidance; inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh primary sections read as architectural guidance. No upstream implementation, diagram rendering/viewing, test, benchmark, failure injection or deployed service was exercised."
  },
  "reuse": "Original contextual annotations and primary links only. No upstream text, code, diagrams or assets redistributed; reuse rights for those artifacts are not inferred.",
  "related": [
    "pattern-transactional-outbox",
    "foundation-transaction-isolation"
  ]
}
---

# Sagas: coordinate local commits without pretending they are global rollback

## When to use

Use when a business operation must coordinate independently owned state and cannot simply use one appropriate local transaction.

## What to inspect

Read choreography versus orchestration, explicit compensation and absent automatic isolation. Microsoft’s considerations include failed compensation and concurrency anomalies. Treat its pivot/retry vocabulary as a modeling aid, not a guarantee that every real action can be undone or retried.

## What to borrow and adapt

For reservation followed by charging, identify the owner and committed result of each step, the action that compensates it, and what happens if compensation cannot finish. Separate infrastructure failures, business rejection and an unknown outcome. Define stable operation identity, pending/recovery states and who reconciles them. Compare a single-owner transaction before introducing coordination machinery.

## Diagram implications

Use a sequence or state view with local commit points, messages, compensating actions and unresolved/manual recovery. Show whether an orchestrator commands transitions or participants react to events. A backward arrow labeled rollback cannot erase a committed external action.

## Mismatches and limits

No workflow or recovery was executed. A saga is not an isolated distributed ACID transaction; compensation is domain-specific and can fail. Message delivery, scheduling and eventual progress need concrete assumptions. The sources do not prove that all cross-service invariants can tolerate temporary divergence.
