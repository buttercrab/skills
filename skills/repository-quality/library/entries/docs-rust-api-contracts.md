---
{
  "id": "docs-rust-api-contracts",
  "kind": "guide",
  "title": "Rust API documentation: examples and failure contracts",
  "summary": "Connect public API examples to error, panic and safety obligations while keeping Rust-specific conventions contextual.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "api-contracts",
      "verify"
    ],
    "contexts": [
      "public-library",
      "executable-examples"
    ],
    "languages": [
      "rust"
    ],
    "scale": [
      "single-package",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://rust-lang.github.io/api-guidelines/documentation.html",
      "title": "Rust API Guidelines: Documentation",
      "locator": "C-CRATE-DOC, C-EXAMPLE, C-QUESTION-MARK, C-FAILURE and C-RELNOTES",
      "revision": "Live primary guidelines inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Primary Rust API documentation guidance freshly read; no compilation, current Cargo-metadata audit or API completeness measurement."
  },
  "reuse": "Original annotation and source links only; no upstream files, screenshots, paper figures or tooling redistributed. Source-specific reuse terms must be checked before copying.",
  "related": [
    "repo-small-go-cmp",
    "docs-google-change-review"
  ]
}
---

# Rust API documentation: examples and failure contracts

## When to use

Use for a public Rust crate whose symbols are documented but whose intended usage, failures or safety obligations are unclear.

## What to inspect

Read the qualification on example coverage, the explanation of why an example matters, and separate Errors/Panics/Safety guidance. The page allows links to a shared relevant example rather than mechanically duplicating one for every item. Hidden rustdoc setup and error propagation also affect copied examples.

## What to borrow and adapt

For a fallible parser, pair a realistic call with its error conditions. For an unsafe operation, explain the caller's invariant. Make reference links and significant release changes discoverable from the crate entry. Verify examples against the crate's supported environment before claiming they work.

## Mismatches and limits

This page contains language/ecosystem conventions, not universal Markdown or manifest requirements. Its illustrative metadata advice is not a current Cargo validation specification. No rustdoc or doctest was run, and example compilation alone would not prove that the narrative is useful or all failure modes covered.
