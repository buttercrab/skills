---
{
  "id": "repo-large-llvm",
  "kind": "repository",
  "title": "LLVM: small regression inputs, generated checks and whole-program tests serve different claims",
  "summary": "A vectorizer regression links a minimal IR specimen, a precise RUN pipeline, generated FileCheck expectations and separately scoped unit/whole-program suites.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test-selection",
      "generated-files",
      "navigate",
      "regression-design"
    ],
    "contexts": [
      "compiler",
      "monorepo",
      "performance-sensitive"
    ],
    "languages": [
      "cpp",
      "llvm-ir",
      "python"
    ],
    "scale": [
      "large-project",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/llvm/llvm-project/blob/42c167cdcb873f16783bd8a2c68c527e1f82e2e9/llvm/docs/GettingStarted.md",
      "title": "llvm/llvm-project: llvm/docs/GettingStarted.md",
      "locator": "Build project selection and check targets, first 120 lines",
      "revision": "42c167cdcb873f16783bd8a2c68c527e1f82e2e9"
    },
    {
      "url": "https://github.com/llvm/llvm-project/blob/42c167cdcb873f16783bd8a2c68c527e1f82e2e9/llvm/docs/TestingGuide.md",
      "title": "llvm/llvm-project: llvm/docs/TestingGuide.md",
      "locator": "Unit/regression/test-suite organization and subset execution, first 160 lines",
      "revision": "42c167cdcb873f16783bd8a2c68c527e1f82e2e9"
    },
    {
      "url": "https://github.com/llvm/llvm-project/blob/42c167cdcb873f16783bd8a2c68c527e1f82e2e9/llvm/test/Transforms/SLPVectorizer/X86/reassociate-ops.ll",
      "title": "llvm/llvm-project: llvm/test/Transforms/SLPVectorizer/X86/reassociate-ops.ll",
      "locator": "RUN line, generated-check annotation and semantic comments, first 65 lines",
      "revision": "42c167cdcb873f16783bd8a2c68c527e1f82e2e9"
    },
    {
      "url": "https://github.com/llvm/llvm-project/blob/42c167cdcb873f16783bd8a2c68c527e1f82e2e9/llvm/utils/update_test_checks.py",
      "title": "llvm/llvm-project: llvm/utils/update_test_checks.py",
      "locator": "Expected-check regeneration workflow and tool selection, first 95 lines",
      "revision": "42c167cdcb873f16783bd8a2c68c527e1f82e2e9"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned primary source/configuration/documentation and specified diff portions read. No upstream code, generator, test, build, CI, publication or remote mutation executed."
  },
  "reuse": "Original annotations and source links only. No upstream files or media redistributed; project-specific license statements are evidence, not legal advice.",
  "related": [
    "repo-large-go",
    "repo-small-bat"
  ]
}
---

# LLVM: small regression inputs, generated checks and whole-program tests serve different claims

## When to use

Use when a compiler, optimizer or other transformation system has snapshot-like expected output and several test scales. It helps avoid equating an updated golden file with a justified behavioral change.

## What to inspect

The testing guide distinguishes in-tree unit tests and small regression specimens from whole programs in the separate `llvm-test-suite` repository. It prefers regression tests for IR transformations and explains targeted lit execution. The representative SLP vectorizer file declares its actual opt/FileCheck pipeline and says its assertions were generated; nearby comments describe the reassociation/wrap-flag behavior being protected.

The update script documents refreshing a baseline, rebuilding with the intended change and reviewing the resulting diff. The guide's older `.rst` paths failed at this revision; current owning files are Markdown and were inspected instead.

## Change path

Trigger: change vectorizer reassociation behavior → owning transformation implementation (not audited here) → small IR regression specimen and its RUN configuration → reviewed FileCheck updates using the appropriate tool binary → relevant regression subset; whole-program correctness/performance requires a different, explicitly selected suite. The current commit's test diff was read, not executed.

## What to borrow and adapt

Keep the reproduction small enough to explain the invariant, including target flags and semantic assumptions. Generated assertions are maintained artifacts: inspect their input and generation route, then review changes against intended behavior. Preserve the distinction between compilation, unit/regression correctness and workload-level performance.

A small source transformer can use the same separation with a few hand-maintained examples; it does not need LLVM's complete CMake, lit and multi-project infrastructure.

## Mismatches and limits

No LLVM build, opt invocation, FileCheck run, expected-output refresh or benchmark occurred. The transformation source and complete generator implementation were not audited. Passing a regression specimen would not establish language-wide correctness, CPU performance or whole-program coverage. Generated output should not be blindly accepted merely because the generator is part of the project.

