---
{
  "id": "system-temporal-replay-activities",
  "kind": "system",
  "title": "Temporal Go SDK: replayable coordination versus external activities",
  "summary": "Separate durable workflow decisions from effects, retries and cancellation observations; procedural syntax does not remove distributed execution boundaries.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "durable-workflows",
      "replay",
      "external-effects"
    ],
    "qualities": [
      "reliability",
      "recoverability",
      "evolvability"
    ],
    "scale": [
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/temporalio/sdk-go/blob/72dabe87bba70ab346a4688c13b974dc181aa892/workflow/doc.go",
      "title": "temporalio/sdk-go: workflow/doc.go",
      "locator": "Overview, deterministic implementation restrictions and SDK time/concurrency alternatives, selected lines 1–210",
      "revision": "72dabe87bba70ab346a4688c13b974dc181aa892"
    },
    {
      "url": "https://github.com/temporalio/sdk-go/blob/72dabe87bba70ab346a4688c13b974dc181aa892/activity/doc.go",
      "title": "temporalio/sdk-go: activity/doc.go",
      "locator": "Activity implementation, cancellation/heartbeat, errors and timeout contracts, selected lines 1–150",
      "revision": "72dabe87bba70ab346a4688c13b974dc181aa892"
    },
    {
      "url": "https://github.com/temporalio/sdk-go/blob/72dabe87bba70ab346a4688c13b974dc181aa892/workflow/workflow.go",
      "title": "temporalio/sdk-go: workflow/workflow.go",
      "locator": "ExecuteActivity Future/error/cancellation contract and local-activity differences around lines 289 onward",
      "revision": "72dabe87bba70ab346a4688c13b974dc181aa892"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh selected pinned workflow/activity documentation and ExecuteActivity wrapper contracts inspected. No SDK execution, replay, server, workflow history or external-effect testing."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "pattern-event-sourcing-replay",
    "pattern-retry-budget-and-breaker"
  ]
}
---

# Temporal Go SDK: replayable coordination versus external activities

## When to use

Use for long-running coordination that must resume across worker failures or wait for external work. It is a counterexample to drawing a single function call as one reliable local transaction.

## What to inspect

Workflow docs impose replay-oriented restrictions on time, concurrency and side effects. Activity docs permit ordinary service code and describe failure/cancellation observations. ExecuteActivity returns a Future; local activities have different scheduling/heartbeat constraints from ordinary activities. Read these as the pinned SDK’s contracts, not a test of any deployed service or every server version.

## Architecture trace

Workflow code expresses coordination while the framework/service records the information needed to recreate state on a worker. An activity represents external/business work and returns success or failure asynchronously. The wrapper documents distinct error causes and version-dependent cancellation delivery: supported servers can deliver cancellation directly, while older paths may depend on heartbeat observation. Requested cancellation therefore is not automatically observed or completed cancellation.

## What to borrow and adapt

Name the durable coordination state and isolate effects that replay must not repeat as ordinary workflow code. Specify an activity’s retry/idempotency and cancellation promises at the business boundary; do not infer exactly-once effects from workflow persistence. Compare the operational cost with a simpler job/state-machine design before adopting a workflow platform.

## Diagram implications

A sequence should show coordination history/service, workflow worker, activity worker/effect owner and completion/error signals. Distinguish a command request, its durable record and the external effect’s observed outcome. If using local activities, label that alternative explicitly rather than preserving the same topology and guarantees by assumption.

## Mismatches and limits

The inspected Go docs are version-pinned development source and describe contracts with server-capability conditions. A workflow example is not proof of business-level duplicate safety or safe evolution of arbitrary old histories. No replay, timeout, cancellation, worker recovery, activity retry or service deployment was executed, and no server operational behavior was inspected.
