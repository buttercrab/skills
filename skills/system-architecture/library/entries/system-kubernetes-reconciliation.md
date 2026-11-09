---
{
  "id": "system-kubernetes-reconciliation",
  "kind": "system",
  "title": "Kubernetes: desired state, observed state and expiring expectations",
  "summary": "A reconciliation loop needs explicit observation and retry semantics; issuing a create/delete request is not the same as observing the resulting state.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "control-loops",
      "eventual-observation",
      "resource-ownership"
    ],
    "qualities": [
      "availability",
      "convergence",
      "operability"
    ],
    "scale": [
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://kubernetes.io/docs/concepts/architecture/controller/",
      "title": "Kubernetes controllers",
      "locator": "Controller pattern; API-server and direct-control paths; desired/current state; ownership",
      "revision": "Live documentation read 2026-11-07; not a frozen release"
    },
    {
      "url": "https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/pkg/controller/replicaset/replica_set.go",
      "title": "kubernetes/kubernetes: pkg/controller/replicaset/replica_set.go",
      "locator": "manageReplicas creation/deletion, expectations and skipped-operation accounting; selected lines 650–770",
      "revision": "ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8"
    },
    {
      "url": "https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/pkg/controller/controller_utils.go",
      "title": "kubernetes/kubernetes: pkg/controller/controller_utils.go",
      "locator": "ControllerExpectations interface; SatisfiedExpectations expiration/error behavior and SetExpectations",
      "revision": "ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh selected pinned ReplicaSet/expectation implementation and live controller documentation inspected. No controller/test execution, convergence proof or deployed cluster observation."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "foundation-end-to-end-guarantees",
    "diagram-mermaid-state-ownership"
  ]
}
---

# Kubernetes: desired state, observed state and expiring expectations

## When to use

Use for a controller or reconciler operating on state observed through caches/events, especially when duplicate actions are possible before observations catch up. It is more specific than saying the system is “event driven.”

## What to inspect

The first-party guide separates desired resource state, controller requests and the components that realize those requests. The ReplicaSet branch sets expected creations/deletions before invoking pod controls and reduces expectations for skipped/failed operations. ControllerExpectations can permit another sync after fulfillment, expiration or missing/error state. These are selected mechanics, not a proof that convergence always occurs.

## Architecture trace

ReplicaSet reconciliation compares active observations with the desired replica count, limits each burst, records expected effects and invokes create/delete operations. A later observation can discharge an expectation. Expiration is also a deliberate escape from waiting forever; it is not evidence that the effect occurred. The controller may requeue after errors, so a request, observed object and completed workload must remain distinct.

## What to borrow and adapt

Name the authoritative desired state, observation source, action owner and conditions for retry. Ensure the business operation tolerates repeated reconciliation or records a durable identity where needed. Model stale observation and timeout separately from successful completion. A small local reconciler may borrow this distinction without adopting a cluster scheduler.

## Diagram implications

Use a feedback-loop view with desired object, cached/watch observation, controller and action target. Label requested actions and observed updates separately, including the checked-expiration and actual retry path. A checked expiration does not by itself establish a scheduled timer. Distinguish a create-Pod API request from the controller directly running that Pod, and object creation from readiness of its underlying workload.

## Mismatches and limits

Kubernetes has many interacting controllers and ownership rules; this selected ReplicaSet path is not a description of every controller. Expiring expectations do not guarantee exactly-once effects or application correctness. No controller, informer, API server, retry scenario, test or cluster behavior was executed; actual deployment/version/configuration remains unknown.
