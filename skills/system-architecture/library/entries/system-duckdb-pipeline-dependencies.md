---
{
  "id": "system-duckdb-pipeline-dependencies",
  "kind": "system",
  "title": "DuckDB: query stages and execution dependency graphs",
  "summary": "Separate syntax/semantic planning from pipeline state and dependency scheduling; a logical query tree is not the runtime task graph.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "trace",
      "diagram"
    ],
    "contexts": [
      "query-processing",
      "pipeline-execution",
      "dependency-graphs"
    ],
    "qualities": [
      "correctness",
      "parallelism",
      "evolvability"
    ],
    "scale": [
      "single-process"
    ]
  },
  "sources": [
    {
      "url": "https://duckdb.org/docs/2.0/internals/overview",
      "title": "DuckDB internals overview",
      "locator": "Parser/binder/logical optimizer/physical-plan stages",
      "revision": "Stable URL redirected to documentation 2.0 on 2026-11-07; distinct from pinned source HEAD"
    },
    {
      "url": "https://github.com/duckdb/duckdb/blob/d4eea3f208d42ca4ee522aca23f5ea76f902b0ca/src/parallel/executor.cpp",
      "title": "duckdb/duckdb: src/parallel/executor.cpp",
      "locator": "ScheduleEventsInternal event construction, dependencies, cycle checks and initial scheduling, lines 52–155",
      "revision": "d4eea3f208d42ca4ee522aca23f5ea76f902b0ca"
    },
    {
      "url": "https://github.com/duckdb/duckdb/blob/d4eea3f208d42ca4ee522aca23f5ea76f902b0ca/src/parallel/pipeline_executor.cpp",
      "title": "duckdb/duckdb: src/parallel/pipeline_executor.cpp",
      "locator": "PipelineExecutor construction: local/global source/sink state, operators and DataChunk setup, lines 32–115",
      "revision": "d4eea3f208d42ca4ee522aca23f5ea76f902b0ca"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh version-2.0 primary overview and selected pinned executor/pipeline implementation inspected. No query execution, benchmark, pipeline graph capture or rendered diagram."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "pattern-backpressure-and-bounded-work",
    "diagram-c4-runtime-scenario"
  ]
}
---

# DuckDB: query stages and execution dependency graphs

## When to use

Use when a diagram collapses the query’s logical transformations and parallel runtime scheduling into one undifferentiated pipeline. It illustrates why the same system can need two different dependency views.

## What to inspect

The versioned internals overview distinguishes parser, binder and plan transformations; the parser does not resolve the catalog or types. The pinned executor constructs stage events, wires dependencies and checks the scheduled graph for cycles. PipelineExecutor separately initializes source/sink/operator state and chunks. The docs version and development source are not asserted to be a perfectly synchronized release.

## Architecture trace

A query moves from syntactic representation to catalog/type-aware binding and logical/physical planning in the documented model. The selected runtime code builds or reuses a pipeline schedule, rejects a cyclic scheduled graph, adds event dependencies and schedules ready events. Local operator/source/sink state is initialized by a different execution object. These are source-level responsibilities, not observed throughput or runtime traces.

## What to borrow and adapt

Distinguish the representation being transformed from the work scheduled to perform it. A document-processing or build pipeline can benefit from naming stages and explicit dependency completion without copying database operators. Consider where blocking/global state creates a pipeline boundary rather than assuming every logical edge can stream independently.

## Diagram implications

Use one transformation view for parser/binder/plan representations and another task-dependency view for runtime stages. Label dependencies as ordering/completion, not network communication. Mark local versus shared execution state when relevant; do not infer processes, machines, batch sizes or performance from class names.

## Mismatches and limits

An initial guessed executor location returned 404; inspection used the owning src/parallel path. The selected source contains development features absent from a simplified overview. No query, plan, cycle test, scheduling trace, benchmark or parallelism claim was reproduced. A pipeline abstraction is not a reason to replace a simple sequential application.
