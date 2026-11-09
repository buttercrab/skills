---
{
  "id": "repo-large-godot",
  "kind": "repository",
  "title": "Godot: test discovery includes generated force-linking, not just test files",
  "summary": "The C++ test build recursively discovers sources, generates force-link declarations/calls and explicitly invokes them from the test entrypoint.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test-discovery",
      "generated-files",
      "navigate",
      "contribute"
    ],
    "contexts": [
      "game-engine",
      "native-build",
      "linker-registration"
    ],
    "languages": [
      "cpp",
      "python"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/godotengine/godot/blob/c51ff06e8836a70ea905701c081bf94124dcd6ce/CONTRIBUTING.md",
      "title": "godotengine/godot: CONTRIBUTING.md",
      "locator": "Bug reproduction, feature routing and focused contributions, first 120 lines",
      "revision": "c51ff06e8836a70ea905701c081bf94124dcd6ce"
    },
    {
      "url": "https://github.com/godotengine/godot/blob/c51ff06e8836a70ea905701c081bf94124dcd6ce/tests/SCsub",
      "title": "godotengine/godot: tests/SCsub",
      "locator": "Recursive sources, force_link.gen.h generation and tests library",
      "revision": "c51ff06e8836a70ea905701c081bf94124dcd6ce"
    },
    {
      "url": "https://github.com/godotengine/godot/blob/c51ff06e8836a70ea905701c081bf94124dcd6ce/tests/test_builders.py",
      "title": "godotengine/godot: tests/test_builders.py",
      "locator": "force_link_builder generated declarations and calls",
      "revision": "c51ff06e8836a70ea905701c081bf94124dcd6ce"
    },
    {
      "url": "https://github.com/godotengine/godot/blob/c51ff06e8836a70ea905701c081bf94124dcd6ce/tests/test_main.cpp",
      "title": "godotengine/godot: tests/test_main.cpp",
      "locator": "test_main invokes ForceLink::force_link_tests, around line 81",
      "revision": "c51ff06e8836a70ea905701c081bf94124dcd6ce"
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
    "repo-large-llvm",
    "docs-github-codeowners"
  ]
}
---

# Godot: test discovery includes generated force-linking, not just test files

## When to use

Use when tests rely on static registration, link-time retention or generated aggregation and a new test compiles but might not be discoverable. This is a useful native-project contrast to languages where directory discovery alone registers every test.

## What to inspect

`tests/SCsub` finds recursive C++ test sources and generates `force_link.gen.h` from their names, with a dependency on the builder implementation. `test_builders.py` emits declarations and calls for those force-link functions. `test_main.cpp` invokes the generated aggregation before running tests. It also explicitly notes module tests still use a different generated include path.

The contributor entry asks for a minimal reproduction project and routes feature proposals separately from bug reports. These mechanisms solve different maintenance problems and should not be collapsed into a generic “add a tests folder” recommendation.

## Change path

Trigger: add or move a C++ test compilation unit → discovered source set in `tests/SCsub` → generated force-link declarations/calls from `tests/test_builders.py` → explicit call in `test_main` → linked test library and relevant test run. The source path was traced; no build or discoverability run was performed.

## What to borrow and adapt

Follow test registration all the way to the executable's entrypoint. A source file's existence, successful compilation and actual execution are different claims. When the build generates registration, record the authoritative inputs and dependency edges so a file move does not leave stale discovery. Preserve the distinction between general test registration and exceptional module paths.

A small command-line utility without linker-based registration may need none of this machinery; a native plugin system may need only one explicit registration table.

## Mismatches and limits

No Godot build, generated header, native test executable, editor or game interaction was exercised. The guessed `tests/README.md` path returned 404 and supports no claim. Separate third-party provenance documentation was sampled during discovery, but this card does not claim that renderer/vendor updates are covered by the inspected unit-test registration path.

