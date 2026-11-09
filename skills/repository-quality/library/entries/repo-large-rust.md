---
{
  "id": "repo-large-rust",
  "kind": "repository",
  "title": "Rust: stage-aware bootstrap and revision-specific diagnostic tests",
  "summary": "Compiler diagnostics are owned alongside multi-revision UI tests, while bootstrap stages and repository/submodule routing constrain the relevant validation path.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "bootstrap",
      "test-selection",
      "navigate",
      "ownership"
    ],
    "contexts": [
      "compiler",
      "generated-expectations",
      "submodules"
    ],
    "languages": [
      "rust",
      "python"
    ],
    "scale": [
      "large-project",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/rust-lang/rust/blob/e30d778f3029b78bb9c2e0dbe11a3b7389b652c4/CONTRIBUTING.md",
      "title": "rust-lang/rust: CONTRIBUTING.md",
      "locator": "Compiler/std guides and submodule/subtree routing",
      "revision": "e30d778f3029b78bb9c2e0dbe11a3b7389b652c4"
    },
    {
      "url": "https://github.com/rust-lang/rust/blob/e30d778f3029b78bb9c2e0dbe11a3b7389b652c4/src/bootstrap/README.md",
      "title": "rust-lang/rust: src/bootstrap/README.md",
      "locator": "Introduction, build phases and directory layout",
      "revision": "e30d778f3029b78bb9c2e0dbe11a3b7389b652c4"
    },
    {
      "url": "https://github.com/rust-lang/rust/blob/e30d778f3029b78bb9c2e0dbe11a3b7389b652c4/bootstrap.example.toml",
      "title": "rust-lang/rust: bootstrap.example.toml",
      "locator": "Profiles, config change tracking and LLVM options, first 140 lines",
      "revision": "e30d778f3029b78bb9c2e0dbe11a3b7389b652c4"
    },
    {
      "url": "https://github.com/rust-lang/rust/blob/e30d778f3029b78bb9c2e0dbe11a3b7389b652c4/tests/ui/codegen/virtual-function-elimination/invalid-lto.rs",
      "title": "rust-lang/rust: tests/ui/codegen/virtual-function-elimination/invalid-lto.rs",
      "locator": "Three LTO revisions and backend exclusion",
      "revision": "e30d778f3029b78bb9c2e0dbe11a3b7389b652c4"
    },
    {
      "url": "https://github.com/rust-lang/rust/blob/e30d778f3029b78bb9c2e0dbe11a3b7389b652c4/tests/ui/codegen/virtual-function-elimination/invalid-lto.lto_thin.stderr",
      "title": "rust-lang/rust: tests/ui/codegen/virtual-function-elimination/invalid-lto.lto_thin.stderr",
      "locator": "Expected diagnostic",
      "revision": "e30d778f3029b78bb9c2e0dbe11a3b7389b652c4"
    },
    {
      "url": "https://github.com/rust-lang/rust/commit/e30d778f3029b78bb9c2e0dbe11a3b7389b652c4",
      "title": "rust-lang/rust: pinned change",
      "locator": "UnstableVirtualFunctionElimination diagnostic wording and three revision-specific stderr files",
      "revision": "e30d778f3029b78bb9c2e0dbe11a3b7389b652c4"
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
    "quality-cargo-workspace-selection",
    "repo-small-ripgrep"
  ]
}
---

# Rust: stage-aware bootstrap and revision-specific diagnostic tests

## When to use

Use for compiler/toolchain repositories where “build the project” hides stage, target and backend choices, or where contributions cross separately maintained components. It is a counterexample to assuming a root manifest alone defines a contributor's work.

## What to inspect

The contributor guide routes compiler and standard-library work to different guides, and distinguishes submodule changes from subtree changes. The bootstrap README explains the stage0 toolchain used to build later compiler/library stages and separates generated output directories from source. The configuration example records profile and configuration-change semantics.

For a concrete path, inspect the diagnostic diff and the invalid-LTO UI test. The test defines missing/no/thin LTO revisions, excludes the GCC backend, and matches the requirement for fat LTO in separate expected stderr outputs.

## Change path

Trigger: clarify or alter the virtual-function-elimination LTO error → diagnostic declaration in `compiler/rustc_session/src/diagnostics.rs` → the revision matrix in `tests/ui/codegen/virtual-function-elimination/invalid-lto.rs` → appropriate expected diagnostics → a deliberately selected bootstrap/harness stage/backend. The inspected sources describe these relationships; they do not show the harness having run.

## What to borrow and adapt

Expose build-stage and backend assumptions before choosing checks. For a diagnostic change, inspect multiple relevant option configurations rather than refreshing one golden output and assuming all paths agree. Treat the expected output as a reviewed contract, not a license to bless whatever the current executable emits.

Route edits to the owner of a component even when a larger checkout makes that component visible. Use the same principle for a small repository with a vendored or separately released dependency, without reproducing a full compiler bootstrap framework.

## Mismatches and limits

No Rust bootstrap, UI harness, download, submodule update or test blessing was executed. The bootstrap README is internal documentation and explicitly points elsewhere for tool usage; this card does not invent a complete command recipe. The guessed compiletest README was unavailable, so no claim depends on it. Costs, current CI health and release compatibility remain unmeasured.

