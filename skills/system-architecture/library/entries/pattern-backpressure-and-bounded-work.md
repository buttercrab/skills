---
{
  "id": "pattern-backpressure-and-bounded-work",
  "kind": "pattern",
  "title": "Backpressure and bounded work: include demand and overflow semantics",
  "summary": "Distinguish asynchronous execution from actual admission control, bounded buffering and slow-consumer behavior.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "model-failure",
      "trace",
      "diagram",
      "compare"
    ],
    "contexts": [
      "stream-processing",
      "queues",
      "overload",
      "admission-control"
    ],
    "qualities": [
      "availability",
      "latency",
      "resource-bounds"
    ],
    "scale": [
      "single-process",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/reactive-streams/reactive-streams-jvm/blob/a625d3aba756e9842ad1291a5b73f5db280b6168/README.md",
      "title": "Reactive Streams JVM specification",
      "locator": "Goals/Scope; API protocol; Publisher 1.1 and Subscriber 2.8",
      "revision": "a625d3aba756e9842ad1291a5b73f5db280b6168; inspected 2026-11-07"
    },
    {
      "url": "https://doc.akka.io/libraries/akka-core/current/stream/stream-flows-and-basics.html",
      "title": "Akka Streams: basics",
      "locator": "Core concepts; Back-pressure explained; materialization",
      "revision": "page labels 2.10.24; current URL inspected 2026-11-07"
    },
    {
      "url": "https://doc.akka.io/libraries/akka-core/current/stream/stream-rate.html",
      "title": "Akka Streams: buffers and rate",
      "locator": "internal buffers; explicit overflow strategies; uncontrollable producers",
      "revision": "page labels 2.10.24; current URL inspected 2026-11-07"
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
    "foundation-overload-capacity",
    "system-duckdb-pipeline-dependencies"
  ]
}
---

# Backpressure and bounded work: include demand and overflow semantics

## When to use

Use when a diagram says async or queue but the workload can outpace consumers, or when a proposal assumes buffering guarantees unlimited acceptance.

## What to inspect

Reactive Streams bounds delivered elements by signaled demand and permits cancellation propagation delay. Akka documents bounded stages, prefetch/internal buffers and explicit backpressure/drop/fail overflow choices. Buffer counts are elements, not necessarily byte bounds. These are specified/documented mechanics, not a conformance test of an application.

## What to borrow and adapt

Name admission, in-flight limits, buffering and the response when capacity is exhausted. For sensor processing, decide whether the source can slow, whether aggregation/drop is permitted, and which data must survive. Trace demand through every boundary instead of adding a queue while leaving an upstream unbounded collection. Include cancellation and teardown; retained or in-flight work may not vanish instantly.

## Diagram implications

Draw data flow and reverse demand/control flow as distinct labeled relationships. Mark capacity units and overflow policy, plus bridges to producers that cannot be slowed. An asynchronous boundary is not proof of throughput or bounded total process memory.

## Mismatches and limits

The JVM specification does not define all stream transformations or persistent message delivery. Akka documentation is version-labeled and does not authorize dependency adoption or a hosted repository token. No stream, TCK, saturation test or failure was run. The inaccessible Reactive Streams homepage was replaced by the exact-pinned owning specification, not inferred from a snippet.
