---
{
  "id": "system-rust-analyzer-derived-state",
  "kind": "system",
  "title": "rust-analyzer: input facts, derived models and cancellable snapshots",
  "summary": "Protect syntax and semantic API boundaries while separating changing input state from lazily derived analysis and editor-facing results.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "trace",
      "diagram",
      "verify"
    ],
    "contexts": [
      "incremental-analysis",
      "developer-tools",
      "api-boundaries"
    ],
    "qualities": [
      "evolvability",
      "responsiveness",
      "testability"
    ],
    "scale": [
      "single-process",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/rust-lang/rust-analyzer/blob/55effabb762bbd0a21c5af530ea447bd6772881d/docs/book/src/contributing/architecture.md",
      "title": "rust-lang/rust-analyzer: docs/book/src/contributing/architecture.md",
      "locator": "Bird’s Eye View; parser/syntax/base-db/hir/ide invariants and API boundaries, selected first 220 lines",
      "revision": "55effabb762bbd0a21c5af530ea447bd6772881d"
    },
    {
      "url": "https://github.com/rust-lang/rust-analyzer/blob/55effabb762bbd0a21c5af530ea447bd6772881d/crates/syntax/src/lib.rs",
      "title": "rust-lang/rust-analyzer: crates/syntax/src/lib.rs",
      "locator": "Module contract and Parse tree-plus-errors representation, lines 1–140",
      "revision": "55effabb762bbd0a21c5af530ea447bd6772881d"
    },
    {
      "url": "https://github.com/rust-lang/rust-analyzer/blob/55effabb762bbd0a21c5af530ea447bd6772881d/crates/ide/src/lib.rs",
      "title": "rust-lang/rust-analyzer: crates/ide/src/lib.rs",
      "locator": "IDE-centric API contract; AnalysisHost::analysis/apply_change and snapshot cancellation",
      "revision": "55effabb762bbd0a21c5af530ea447bd6772881d"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh pinned architecture prose and selected syntax/IDE implementation contracts inspected. Referenced image not viewed; no runtime, query-performance or diagram-rendering observation."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "foundation-information-hiding",
    "pattern-cache-aside-authority"
  ]
}
---

# rust-analyzer: input facts, derived models and cancellable snapshots

## When to use

Use for an editor, compiler-assisted tool or other continuously updated analysis system where incomplete input must remain useful. It provides a counterexample to making every internal module a stable public interface.

## What to inspect

The architecture document names intended absences as invariants: syntax does not need semantic context, and base-db does not encode a specific build tool or filesystem path API. The syntax source explicitly represents a tree plus errors, including invalid files. The IDE API and AnalysisHost implementation show editor-facing values, snapshots and change application. Some names in the architecture prose are historical; inspect actual owning APIs before copying its code map.

## Architecture trace

A client supplies file/project facts; the documented query model derives semantic information on demand. syntax produces a representation even when text is invalid, rather than requiring a complete successful compilation. AnalysisHost owns the current database; analysis creates a query snapshot, while apply_change updates state and documents cancellation of outstanding snapshots. The selected implementation corroborates that API contract, not every incremental invalidation or latency property.

## What to borrow and adapt

Choose explicit input facts and stable consumer-facing values; let internal query/model boundaries vary where appropriate. For an interactive tool, make cancellation and incomplete-state behavior part of the contract. Do not expose every internal identifier or derived structure merely because a language server eventually needs a string or text range.

## Diagram implications

A dependency/component view should distinguish input facts, derived queries, syntax, semantic façade and editor-facing API. A separate change/snapshot sequence can show an update invalidating a prior observation. Do not turn crate boundaries into process/service boundaries, or draw IO arrows inside a documented analysis boundary without implementation evidence.

## Mismatches and limits

This is not a generic prescription for transactional business state or a reason to adopt the same incremental engine. The source document’s linked picture was not viewed; this card concerns text/source contracts only. No IDE, snapshot race, incremental test, responsiveness measurement or full architecture-conformance check was executed.
