---
{
  "id": "repo-small-bat",
  "kind": "repository",
  "title": "bat: authored syntax inputs, derived assets and specialized test routes",
  "summary": "A Rust CLI separates built-in syntax mapping inputs, binary assets and regression representations, with configuration that distinguishes ordinary tests from asset-refresh checks.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "generated-files",
      "test",
      "document",
      "package"
    ],
    "contexts": [
      "cli",
      "embedded-assets",
      "code-generation",
      "platform-support"
    ],
    "languages": [
      "rust",
      "shell"
    ],
    "scale": [
      "single-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/CONTRIBUTING.md",
      "title": "sharkdp/bat: CONTRIBUTING.md",
      "locator": "functional regression, syntax testing and changelog guidance",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/Cargo.toml",
      "title": "sharkdp/bat: Cargo.toml",
      "locator": "build script, excluded asset sources and application features",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/src/syntax_mapping/builtins/README.md",
      "title": "sharkdp/bat: src/syntax_mapping/builtins/README.md",
      "locator": "authored TOML organization and platform-specific inclusion",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/build/main.rs",
      "title": "sharkdp/bat: build/main.rs",
      "locator": "mapping generation and application-only man/completion generation",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/doc/assets.md",
      "title": "sharkdp/bat: doc/assets.md",
      "locator": "syntax source/highlighted regression workflow",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/assets/create.sh",
      "title": "sharkdp/bat: assets/create.sh",
      "locator": "cache clearing, patches and asset generation",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/tests/snapshot_tests.rs",
      "title": "sharkdp/bat: tests/snapshot_tests.rs",
      "locator": "feature-gated style snapshot scenarios",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
    },
    {
      "url": "https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/.github/workflows/CICD.yml",
      "title": "sharkdp/bat: .github/workflows/CICD.yml",
      "locator": "updated syntax/theme build and ignored-by-default checks",
      "revision": "c231941daa363e67657216922135e3cc2d5a4f93"
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
    "quality-generated-source-authority",
    "quality-cargo-package-boundary"
  ]
}
---

# bat: authored syntax inputs, derived assets and specialized test routes

## When to use

Use when a repository embeds generated resources, syntax definitions, themes or platform-specific metadata and contributors are tempted to edit the resulting binary files directly. It also illustrates why “run the generator” may have meaningful side effects beyond writing one output file.

## What to inspect

Built-in mapping documentation defines TOML inputs grouped for maintainability, with platform directories selecting what is embedded. The Cargo build entry invokes mapping generation and, for application builds, man/completion generation. Asset documentation separates source syntax examples from their generated highlighted regressions. The CI asset-refresh job rebuilds/reinstalls with updated assets, then runs ordinary and explicitly ignored checks; style snapshot tests themselves are gated by the git feature.

## Change path

Trigger: add a filename-to-syntax mapping or update a built-in syntax. For mappings, start in src/syntax_mapping/builtins and follow build/main.rs’s mapping-generation call; inspect the owning generator further if changing inclusion logic. For syntax assets, doc/assets.md routes a source fixture to generated highlighted output and manual review. assets/create.sh clears the local bat cache, may initialize submodules in an interactive invocation, applies patches with an exit trap and builds binary caches. The CI configuration shows the broader refresh/test route. These scripts were read, not executed.

## What to borrow and adapt

Identify authored input, generated result, validation representation and distribution packaging separately. Describe side effects before treating generation as a harmless check. Keep snapshot/asset refresh paths distinct from ordinary tests, including feature gates and ignored-by-default scenarios. Use local grouping rules that explain why files split: the built-in mapping guide explicitly permits maintainability-based grouping rather than a supposedly fundamental directory hierarchy.

## Mismatches and limits

A syntax-highlighting CLI has licensed embedded resources and platform-sensitive generation needs that a text-only library may not share. The generator implementation below its entry calls was not exhaustively audited, and no assets, cache, submodules, scripts or tests were modified/run. Source exclusions in Cargo.toml are packaging intent, not a verified published archive. Do not infer that every project should track generated snapshots or adopt this asset pipeline.

