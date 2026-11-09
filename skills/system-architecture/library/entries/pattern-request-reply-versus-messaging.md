---
{
  "id": "pattern-request-reply-versus-messaging",
  "kind": "pattern",
  "title": "Request/reply versus messaging: decide temporal coupling and outcome semantics",
  "summary": "Compare synchronous collaboration and queued work using actual completion, latency, failure and operating requirements.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "service-collaboration",
      "messaging",
      "request-reply"
    ],
    "qualities": [
      "availability",
      "latency",
      "operability"
    ],
    "scale": [
      "multi-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://microservices.io/patterns/communication-style/rpi.html",
      "title": "Richardson: Remote Procedure Invocation",
      "locator": "Solution; resulting-context benefits/drawbacks; discovery",
      "revision": "mutable original-author catalog; inspected 2026-11-07"
    },
    {
      "url": "https://microservices.io/patterns/communication-style/messaging.html",
      "title": "Richardson: Messaging",
      "locator": "interaction styles; runtime decoupling; broker/request-reply costs",
      "revision": "mutable original-author catalog; inspected 2026-11-07"
    },
    {
      "url": "https://www.enterpriseintegrationpatterns.com/patterns/messaging/Messaging.html",
      "title": "Enterprise Integration Patterns: Messaging",
      "locator": "public pattern excerpt on asynchronous integration",
      "revision": "public excerpt, not full book chapter; inspected 2026-11-07"
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
    "diagram-mermaid-sequence-outcomes"
  ]
}
---

# Request/reply versus messaging: decide temporal coupling and outcome semantics

## When to use

Use when a queue is proposed as an automatic reliability improvement, or a chain of remote calls is presented as equivalent to local function calls.

## What to inspect

Read the request/reply availability coupling and messaging’s distinct notification, request/response and eventual-response styles. Broker buffering changes when participants must be available but adds a dependency and request/reply coordination. The Enterprise Integration Patterns web page is an excerpt; its full chapter was not inspected.

## What to borrow and adapt

Define what the caller needs to know now. A checkout may require an authoritative reservation result; a receipt notification may tolerate delayed processing. Specify accepted, durably recorded and completed as different states where applicable. Compare timeout/unknown-result recovery for direct calls with queue capacity, delivery, ordering, retry and consumer failure behavior. One application can use both mechanisms for different operations.

## Diagram implications

Label request/reply arrows separately from asynchronous publication. Show which response acknowledges receipt versus domain completion. Include broker and result-correlation/state-query responsibility when the workflow depends on them.

## Mismatches and limits

The catalog describes mechanisms and examples, not measured latency or uptime. A buffer cannot guarantee permanent acceptance, processing or business correctness. Historic example frameworks are not current tool recommendations, and none was installed or executed.
