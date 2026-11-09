---
{
  "id": "system-bazel-dependency-evaluation",
  "kind": "system",
  "title": "Bazel Skyframe: declared dependencies and restartable evaluation",
  "summary": "Incremental recomputation relies on dependency-aware evaluation, not merely storing outputs in a cache.",
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
      "incremental-builds",
      "dependency-tracking",
      "derived-state"
    ],
    "qualities": [
      "correctness",
      "evolvability",
      "incrementality"
    ],
    "scale": [
      "single-process",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://bazel.build/reference/skyframe",
      "title": "Bazel Skyframe documentation",
      "locator": "Data model, evaluation, requested dependencies, invalidation/hermeticity",
      "revision": "Live documentation read 2026-11-07; not a frozen release"
    },
    {
      "url": "https://github.com/bazelbuild/bazel/blob/a765dc177f48efb4c9e1b980609b838c9ba27f42/src/main/java/com/google/devtools/build/skyframe/SkyFunction.java",
      "title": "bazelbuild/bazel: src/main/java/com/google/devtools/build/skyframe/SkyFunction.java",
      "locator": "Interface contract: direct dependency access, missing values/restarts, exception enrichment and compute",
      "revision": "a765dc177f48efb4c9e1b980609b838c9ba27f42"
    },
    {
      "url": "https://github.com/bazelbuild/bazel/blob/a765dc177f48efb4c9e1b980609b838c9ba27f42/src/main/java/com/google/devtools/build/skyframe/SkyValue.java",
      "title": "bazelbuild/bazel: src/main/java/com/google/devtools/build/skyframe/SkyValue.java",
      "locator": "Return-value interface and debug/lifecycle methods",
      "revision": "a765dc177f48efb4c9e1b980609b838c9ba27f42"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh pinned core interfaces and live first-party evaluation/model documentation inspected. No build or cache/invalidation experiment, generated graph or visual rendering."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "system-rust-analyzer-derived-state",
    "foundation-information-hiding"
  ]
}
---

# Bazel Skyframe: declared dependencies and restartable evaluation

## When to use

Use when a tool computes derived state repeatedly and needs to know which changes invalidate which results. It also helps expose why reading an untracked input can undermine an incremental model even if a diagram contains a cache.

## What to inspect

The first-party model describes keyed values, functions and a dependency graph. SkyFunction’s pinned interface requires dependency access through its Environment and permits restarting compute when required values are missing. The SkyValue interface is small; documented immutability is not a type-level proof that every implementation has no mutable behavior.

## Architecture trace

A requested value selects a computation that asks for dependencies. Missing dependency values can cause a null return and later re-invocation after those dependencies are computed. The resulting relationship graph is part of the incremental model. Failure can propagate or gain context through the compute contract. This is distinct from a one-shot call stack, and distinct again from a verified hermetic build configuration.

## What to borrow and adapt

Identify all inputs that determine a derived result and make the relevant dependencies observable to the evaluation mechanism. A linter, code analyzer or content generator can borrow explicit invalidation boundaries without adopting the entire build system. Treat hidden environment/file reads and side effects as design questions, not automatically solved properties of an immutable-value vocabulary.

## Diagram implications

Draw a dependency DAG with edge meaning stated—“requires value of,” not “sends network request to.” A sequence can separately show a missing dependency and evaluation restart. Runtime workers, remote caches and execution machines need their own actual evidence; they cannot be inferred from SkyFunction/SkyValue interfaces.

## Mismatches and limits

An initial guessed source package omitted lib and returned 404; the corrected executor file was discovery only, and its import list is not cited as architecture proof. This card relies on the two actual core interfaces and live model documentation. No build, invalidation test, hermeticity check, remote execution or performance experiment was run. Small one-shot computations may not justify this machinery.
