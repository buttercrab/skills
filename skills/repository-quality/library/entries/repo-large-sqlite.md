---
{
  "id": "repo-large-sqlite",
  "kind": "repository",
  "title": "SQLite: the distributed amalgamation is not the source-authoring boundary",
  "summary": "The source README, amalgamation generator and make targets distinguish authored inputs, generated distribution, development tests, release tests and Fossil authority.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "source-authority",
      "generated-files",
      "distribution",
      "test-selection"
    ],
    "contexts": [
      "native-library",
      "source-distribution",
      "repository-mirror"
    ],
    "languages": [
      "c",
      "tcl"
    ],
    "scale": [
      "large-project",
      "single-package"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/sqlite/sqlite/blob/425bfb8aa82e2fd7829d055335f164eaf617eae0/README.md",
      "title": "sqlite/sqlite: README.md",
      "locator": "Version control, compilation and source tree map, first 200 lines",
      "revision": "425bfb8aa82e2fd7829d055335f164eaf617eae0"
    },
    {
      "url": "https://github.com/sqlite/sqlite/blob/425bfb8aa82e2fd7829d055335f164eaf617eae0/manifest.uuid",
      "title": "sqlite/sqlite: manifest.uuid",
      "locator": "Canonical Fossil check-in associated with the inspected Git mirror",
      "revision": "425bfb8aa82e2fd7829d055335f164eaf617eae0"
    },
    {
      "url": "https://github.com/sqlite/sqlite/blob/425bfb8aa82e2fd7829d055335f164eaf617eae0/tool/mksqlite3c.tcl",
      "title": "sqlite/sqlite: tool/mksqlite3c.tcl",
      "locator": "Generator prerequisites, generated parser inputs and core-only output, first 120 lines",
      "revision": "425bfb8aa82e2fd7829d055335f164eaf617eae0"
    },
    {
      "url": "https://github.com/sqlite/sqlite/blob/425bfb8aa82e2fd7829d055335f164eaf617eae0/main.mk",
      "title": "sqlite/sqlite: main.mk",
      "locator": "sqlite3.c target around line 1146; test/releasetest targets around lines 1937–1948",
      "revision": "425bfb8aa82e2fd7829d055335f164eaf617eae0"
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
    "quality-reproducible-build-evidence"
  ]
}
---

# SQLite: the distributed amalgamation is not the source-authoring boundary

## When to use

Use for a native library distributed as generated source, or when a convenient Git mirror can be mistaken for the authoritative contribution surface. SQLite is a strong counterexample to equating the artifact a consumer compiles with the file a maintainer should edit.

## What to inspect

The README identifies Fossil as the source authority and explains that Git mirror identifiers differ from official check-in names. The pinned mirror's `manifest.uuid` supplies the corresponding canonical identifier. It distinguishes repository source documentation from user documentation and notes additional tests/documentation managed elsewhere.

The amalgamation generator expects a prepared source directory containing authored and generated inputs, including parser products. `main.mk` makes `sqlite3.c` depend on that source preparation, headers and the generator. Its test aliases distinguish development tests from a release-test runner.

## Change path

Trigger: alter core/parser behavior intended for source distribution → owning `src/` input or grammar and relevant tests → generated intermediate source preparation → `tool/mksqlite3c.tcl` through the `sqlite3.c` make target → consumer amalgamation. Choose development or release qualification deliberately. The generator/target relationship was inspected; the full grammar generation, package contents and separate test infrastructure were not executed or audited.

## What to borrow and adapt

Document both contributor and consumer entrypoints. A single-file distribution can have a richly structured authoring repository; replacing that structure with the distribution file would erase authority and maintenance context. Preserve canonical identifiers across mirrors, especially when communicating a reproduction or reviewing a fix.

Keep a quick development check separate from release qualification. Clear target names and prerequisites are more useful than one undifferentiated “all tests” claim.

## Mismatches and limits

No Fossil operation, source verification, generation, compilation, Tcl test or release test was run. The canonical identifier was read from the Git snapshot, not independently reconciled against a live Fossil view. The README's legal/distribution statements are project documentation, not legal advice. Additional/private test suites were not inspected; their absence from this survey is not evidence of absence.

