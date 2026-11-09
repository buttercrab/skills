---
{
  "id": "repo-large-go",
  "kind": "repository",
  "title": "Go: distinguish compiler rule inputs from generated rewrites and target tests",
  "summary": "A RISC-V lowering change links handwritten rules/operations, generated Go, backend emission and architecture-specific code-generation expectations.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "generated-files",
      "navigate",
      "test-selection",
      "bootstrap"
    ],
    "contexts": [
      "compiler",
      "cross-compilation",
      "language-runtime"
    ],
    "languages": [
      "go",
      "shell"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/golang/go/blob/3568f0bb1559a1d395f599af61ddb1c0e9b02201/CONTRIBUTING.md",
      "title": "golang/go: CONTRIBUTING.md",
      "locator": "Contribution and issue-context entry",
      "revision": "3568f0bb1559a1d395f599af61ddb1c0e9b02201"
    },
    {
      "url": "https://github.com/golang/go/blob/3568f0bb1559a1d395f599af61ddb1c0e9b02201/src/make.bash",
      "title": "golang/go: src/make.bash",
      "locator": "Bootstrap/environment contract, first 180 lines",
      "revision": "3568f0bb1559a1d395f599af61ddb1c0e9b02201"
    },
    {
      "url": "https://github.com/golang/go/blob/3568f0bb1559a1d395f599af61ddb1c0e9b02201/src/run.bash",
      "title": "golang/go: src/run.bash",
      "locator": "dist test invocation and test environment",
      "revision": "3568f0bb1559a1d395f599af61ddb1c0e9b02201"
    },
    {
      "url": "https://github.com/golang/go/blob/3568f0bb1559a1d395f599af61ddb1c0e9b02201/src/cmd/compile/internal/ssa/rewrite/riscv64latelower/rewriteRISCV64latelower.go",
      "title": "golang/go: src/cmd/compile/internal/ssa/rewrite/riscv64latelower/rewriteRISCV64latelower.go",
      "locator": "Generated-source header and dispatcher",
      "revision": "3568f0bb1559a1d395f599af61ddb1c0e9b02201"
    },
    {
      "url": "https://github.com/golang/go/commit/3568f0bb1559a1d395f599af61ddb1c0e9b02201",
      "title": "golang/go: pinned change",
      "locator": "BSET/BSETI rules, operation declarations, backend support, generated rewrites and target-profile codegen tests",
      "revision": "3568f0bb1559a1d395f599af61ddb1c0e9b02201"
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
    "quality-generated-source-authority",
    "repo-small-cobra"
  ]
}
---

# Go: distinguish compiler rule inputs from generated rewrites and target tests

## When to use

Use when generated code is checked in beside handwritten compiler or protocol rules, especially where one target or feature level needs different expected behavior. The example helps locate authority before a superficial generated-file cleanup.

## What to inspect

The commit adds RISC-V BSET/BSETI support in backend emission and operation declarations, introduces lowering rules, updates generated Go and adjusts tests for rva20/rva22/rva23 profiles. The generated rewrite file explicitly identifies its rule input and generation mechanism. Read `make.bash` and `run.bash` separately: one establishes a bootstrap/toolchain build, the other invokes `go tool dist test -rebuild` with controlled environment. Their scopes are not interchangeable.

## Change path

Trigger: recognize a single-bit set on a supported RISC-V profile → `_gen/RISCV64Ops.go` and `_gen/RISCV64latelower.rules` → generated rewrite and operation code → `riscv64/ssa.go` emission support → architecture/profile assertions in `test/codegen/bits.go` and `mathbits.go`. Build and test environment selection determines whether those target paths can actually be exercised.

## What to borrow and adapt

Mark generated authority and follow it backwards. A committed generated artifact may still require changes when its input changes; the answer is not to ignore generated files or hand-edit them as primary source. Keep lower-feature-level expectations visible when adding a newer instruction, so a feature-gated optimization does not silently alter older targets.

Document which toolchain is building the repository and which platform is being tested. For a small Go module, ordinary package tests may be the right check; Go's own bootstrap/dist machinery serves a different product.

## Mismatches and limits

No generator, compiler, cross-target binary or test was run. Commit assertions state intended output, not proved performance or correctness. The inspected build script's bootstrap version belongs to this snapshot and must be rechecked when used. Host and target support, builders and release qualification were not exhaustively audited.

