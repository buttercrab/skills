---
{
  "id": "repo-small-ripgrep",
  "kind": "repository",
  "title": "ripgrep: flag ownership, co-located parsing tests and binary integration suites",
  "summary": "A Rust CLI workspace connects declarative flag semantics and nearby parser tests with an explicitly registered integration suite, rather than relying on an undifferentiated tests directory.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "organize",
      "test",
      "document",
      "navigate"
    ],
    "contexts": [
      "cli",
      "workspace",
      "public-api",
      "integration-tests"
    ],
    "languages": [
      "rust"
    ],
    "scale": [
      "multi-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/Cargo.toml",
      "title": "BurntSushi/ripgrep: Cargo.toml",
      "locator": "binary target, autotests=false, explicit integration target and workspace members",
      "revision": "91f5d22ef48bde459d90a8c7dbeab416e97d0f2b"
    },
    {
      "url": "https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/CONTRIBUTING.md",
      "title": "BurntSushi/ripgrep: CONTRIBUTING.md",
      "locator": "route to project contribution policy",
      "revision": "91f5d22ef48bde459d90a8c7dbeab416e97d0f2b"
    },
    {
      "url": "https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/crates/core/flags/defs.rs",
      "title": "BurntSushi/ripgrep: crates/core/flags/defs.rs",
      "locator": "Follow/Hidden definitions, negated names, docs and parser tests",
      "revision": "91f5d22ef48bde459d90a8c7dbeab416e97d0f2b"
    },
    {
      "url": "https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/tests/tests.rs",
      "title": "BurntSushi/ripgrep: tests/tests.rs",
      "locator": "integration modules and feature/regression routing",
      "revision": "91f5d22ef48bde459d90a8c7dbeab416e97d0f2b"
    },
    {
      "url": "https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/tests/feature.rs",
      "title": "BurntSushi/ripgrep: tests/feature.rs",
      "locator": "encoding scenarios using Dir/TestCommand",
      "revision": "91f5d22ef48bde459d90a8c7dbeab416e97d0f2b"
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
    "quality-cargo-workspace-selection",
    "repo-large-rust"
  ]
}
---

# ripgrep: flag ownership, co-located parsing tests and binary integration suites

## When to use

Use for a CLI whose argument model, help text and application behavior must change together, particularly when it shares reusable implementation crates. It provides a concrete reason for both co-located unit tests and separately organized binary-level tests.

## What to inspect

The manifest names the rg binary under crates/core, enumerates reusable workspace members and disables automatic test discovery in favor of an explicit tests/tests.rs integration target. Follow and Hidden put names, negations, descriptions and parser-state updates together; their nearby tests check default and argument-order behavior. The integration entrypoint routes feature, JSON, binary, multiline and regression modules and explicitly explains where a new feature likely belongs. Selected feature tests create files and invoke a test command rather than only checking parser state.

## Change path

Trigger: change --follow or --hidden argument semantics. Start in crates/core/flags/defs.rs, update the flag definition/documented meaning and nearby parse_low_raw cases, including positive/negated ordering. For a traversal or output effect, follow the relevant implementation crate and add an appropriate binary-level scenario through tests/tests.rs; this card inspected the integration wiring and encoding examples, not every traversal test. Cargo.toml establishes how the integration suite is registered. Generated help/man output is suggested by the generate flag but its full pipeline was not traced here.

## What to borrow and adapt

Keep each kind of invariant at the owning layer: parser semantics near argument definitions, externally visible filesystem behavior at a command boundary. Document test-routing exceptions such as explicit targets, because a conventional filename does not guarantee discovery. Reusable crates can remain inside one repository without making every change a workspace-wide architectural refactor.

## Mismatches and limits

The reusable crate split reflects a substantial search tool and is not a template for a small script. CONTRIBUTING points to a separate AI policy whose full terms were not inspected in this card; do not infer them from its filename. No tests, traversals, generated pages, benchmarks or release artifacts were exercised. The integration encoding examples establish test style, not coverage of the selected follow/hidden behavior.

