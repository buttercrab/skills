---
{
  "id": "repo-small-fd",
  "kind": "repository",
  "title": "fd: CLI declarations and filesystem fixtures with platform limits",
  "summary": "A Rust CLI keeps argument rules discoverable in one definition surface and validates user-visible filesystem behavior through reusable integration fixtures with explicit operating-system limits.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test",
      "document",
      "maintain-api",
      "navigate"
    ],
    "contexts": [
      "cli",
      "filesystem",
      "platform-support"
    ],
    "languages": [
      "rust"
    ],
    "scale": [
      "single-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/CONTRIBUTING.md",
      "title": "sharkdp/fd: CONTRIBUTING.md",
      "locator": "contribution expectations and behavioral changelog boundary",
      "revision": "39886c0cb34453cda21163df0c0c76fc9c011a21"
    },
    {
      "url": "https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/Cargo.toml",
      "title": "sharkdp/fd: Cargo.toml",
      "locator": "binary path, feature flags and test dependencies",
      "revision": "39886c0cb34453cda21163df0c0c76fc9c011a21"
    },
    {
      "url": "https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/src/cli.rs",
      "title": "sharkdp/fd: src/cli.rs",
      "locator": "Opts hidden/follow flags, conflicts and negations",
      "revision": "39886c0cb34453cda21163df0c0c76fc9c011a21"
    },
    {
      "url": "https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/tests/tests.rs",
      "title": "sharkdp/fd: tests/tests.rs",
      "locator": "test_hidden, Windows attribute case, test_follow and filesystem boundaries",
      "revision": "39886c0cb34453cda21163df0c0c76fc9c011a21"
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
    "repo-small-ripgrep",
    "quality-cargo-package-boundary"
  ]
}
---

# fd: CLI declarations and filesystem fixtures with platform limits

## When to use

Use for filesystem tools where path rules, symlinks and operating-system attributes matter more than an attractive folder layout. It helps assess whether contributor guidance leads to concrete input/output scenarios and whether platform-specific limitations are visible.

## What to inspect

The manifest names the fd executable separately from the fd-find package and declares optional features and test dependencies. Opts in src/cli.rs combines argument help and behavior constraints, including hidden-file and follow/negation settings. tests/tests.rs uses TestEnv and assert_output to create a known corpus and check results. It separately tests the Windows hidden attribute and marks filesystem-boundary behavior Unix-only, including conditions where that scenario returns without exercising the intended boundary.

## Change path

Trigger: change which hidden files or symlink descendants appear. Follow src/cli.rs hidden/follow definitions and negative flags to tests/tests.rs test_hidden, test_hidden_file_attribute and test_follow. Where the implementation changes rather than only parsing, follow the actual traversal owner before editing. Contributor guidance distinguishes behavioral changelog entries from documentation typo fixes. The configured package/binary and feature boundaries inform which command/build is relevant; this card does not provide a tested build recipe.

## What to borrow and adapt

Make scenario fixtures express what a user observes, and record which platform or environment makes a scenario meaningful. A green suite can contain platform-gated or skipped execution; inspect those conditions before claiming cross-platform equivalence. Match release communication to the kind of change instead of requiring changelog entries for every edit. Contribution policies are local source facts to consult when contributing upstream, not automatic rules for unrelated repositories.

## Mismatches and limits

The file layout is a case for a single CLI package, not proof that every command-line project needs a similarly broad fixture tree. Only selected argument/test sections were read; neither all traversal implementation nor CI was audited. No upstream script, generator, test or binary was executed. The contribution guide’s legal and AI-use statements are not a legal conclusion or permission to publish work.

