---
{
  "id": "repo-small-go-cmp",
  "kind": "repository",
  "title": "go-cmp: compact package boundaries and reasoned comparison cases",
  "summary": "A Go comparison library combines a small module surface with scenario reasons, golden presentation tests and an explicit warning that diagnostic output is not a stable machine interface.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test",
      "maintain-api",
      "document",
      "check-compatibility"
    ],
    "contexts": [
      "library",
      "diagnostics",
      "golden-tests",
      "public-api"
    ],
    "languages": [
      "go"
    ],
    "scale": [
      "single-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/CONTRIBUTING.md",
      "title": "google/go-cmp: CONTRIBUTING.md",
      "locator": "local review and contribution terms",
      "revision": "5deca1c7dab7d33c102d8d7a26794da148485563"
    },
    {
      "url": "https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/go.mod",
      "title": "google/go-cmp: go.mod",
      "locator": "module identity and Go directive",
      "revision": "5deca1c7dab7d33c102d8d7a26794da148485563"
    },
    {
      "url": "https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/cmp/compare.go",
      "title": "google/go-cmp: cmp/compare.go",
      "locator": "Equal, Diff and comparison invariants",
      "revision": "5deca1c7dab7d33c102d8d7a26794da148485563"
    },
    {
      "url": "https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/cmp/compare_test.go",
      "title": "google/go-cmp: cmp/compare_test.go",
      "locator": "TestDiff scenario reasons, panic expectations and golden updates",
      "revision": "5deca1c7dab7d33c102d8d7a26794da148485563"
    },
    {
      "url": "https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/.github/workflows/test.yml",
      "title": "google/go-cmp: .github/workflows/test.yml",
      "locator": "race tests, formatting and interpreter/platform matrix",
      "revision": "5deca1c7dab7d33c102d8d7a26794da148485563"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh primary repository metadata and selected substantive source/configuration/test/documentation sections inspected at the pinned commit. No upstream code, command, CI, build or release was executed."
  },
  "reuse": "Original annotations and primary-source links only; no upstream implementation, images or packages redistributed. License declarations are source facts, not legal advice.",
  "related": [
    "quality-go-module-workspace-boundaries",
    "docs-study-coverage-limits"
  ]
}
---

# go-cmp: compact package boundaries and reasoned comparison cases

## When to use

Use when a library exposes both semantic results and human-readable diagnostics. It is helpful for assessing whether tests protect the intended public promise while avoiding accidental commitment to a debug representation as a machine protocol.

## What to inspect

The module identity and code live in a small, conventional Go surface. Equal and Diff share comparison machinery, but the Diff documentation explicitly warns that its textual output is not a stable programmatic interface. TestDiff draws from multiple scenario groups; cases carry expected equality/panic outcomes and a required reason, with golden output comparison and a distinct update path. CI configures race-enabled tests and formatting checks rather than proving they currently pass.

## Change path

Trigger: change how a comparison reports or handles an unexported field. Follow cmp/compare.go’s Equal/Diff and struct comparison to the relevant cmp/compare_test.go scenario groups. Preserve semantic outcome, expected panic behavior and the case’s reason separately from the golden text. Inspect the custom Reporter alternative before consumers parse a display string. The configured validation path is go test with race checking and formatting; go.mod’s directive and the CI toolchain matrix are separate declarations, not automatically the same minimum-supported claim.

## What to borrow and adapt

Require meaningful reasons for non-obvious compatibility scenarios, and make intentional golden updates explicit review work. Keep a small package boundary when it reveals the change path well; additional layers would need a concrete benefit. Distinguish output useful to a reader from a serialized contract. A test may assert particular local formatting without promising that every future library version keeps it stable.

## Mismatches and limits

Reflection-based comparison and golden diagnostics have specialized edge cases; copying the entire scenario harness may burden a tiny helper unnecessarily. Source and selected test cases were inspected, not executed, and no installed package or current CI status was checked. The repository’s contribution agreement/review rules are local governance facts, not requirements to import into unrelated projects.

