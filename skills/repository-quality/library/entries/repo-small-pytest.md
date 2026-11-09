---
{
  "id": "repo-small-pytest",
  "kind": "repository",
  "title": "pytest: a test harness with explicit in-process and subprocess boundaries",
  "summary": "A mature Python test framework uses its own isolated test-workspace helper and distinct documentation/doctest paths to make plugin and runner behavior inspectable.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test",
      "document",
      "navigate",
      "maintain-api"
    ],
    "contexts": [
      "framework",
      "plugins",
      "test-isolation",
      "generated-reference"
    ],
    "languages": [
      "python"
    ],
    "scale": [
      "single-package",
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/CONTRIBUTING.rst",
      "title": "pytest-dev/pytest: CONTRIBUTING.rst",
      "locator": "reproduction guidance and documentation build/autodoc notes",
      "revision": "171c924acfd66d03ab51d08da2509461da6233a7"
    },
    {
      "url": "https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/pyproject.toml",
      "title": "pytest-dev/pytest: pyproject.toml",
      "locator": "build backend and pytest testpaths/norecursedirs",
      "revision": "171c924acfd66d03ab51d08da2509461da6233a7"
    },
    {
      "url": "https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/src/_pytest/pytester.py",
      "title": "pytest-dev/pytest: src/_pytest/pytester.py",
      "locator": "Pytester, runpytest and runpytest_subprocess",
      "revision": "171c924acfd66d03ab51d08da2509461da6233a7"
    },
    {
      "url": "https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/testing/test_pytester.py",
      "title": "pytest-dev/pytest: testing/test_pytester.py",
      "locator": "makepyfile and inline-run module-cleanup tests",
      "revision": "171c924acfd66d03ab51d08da2509461da6233a7"
    },
    {
      "url": "https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/tox.ini",
      "title": "pytest-dev/pytest: tox.ini",
      "locator": "testenv command and doctesting factor",
      "revision": "171c924acfd66d03ab51d08da2509461da6233a7"
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
    "docs-study-coverage-limits",
    "repo-small-click"
  ]
}
---

# pytest: a test harness with explicit in-process and subprocess boundaries

## When to use

Use for frameworks, plugin systems and command runners whose tests need to create temporary projects and exercise a public execution boundary. It helps assess whether a large test collection is organized around meaningful scenarios rather than simply mirroring every implementation function.

## What to inspect

Contributor guidance asks for reproductions and explains the documentation build and generated API reference. The test configuration points at testing, excludes fixture/example directories from ordinary recursion and explicitly notes that documentation is tested separately. Pytester creates an isolated workspace and offers in-process and subprocess execution. The test file exercises generated source contents and module-state cleanup; tox’s doctesting factor adds documentation and module doctests beyond the default path.

## Change path

Trigger: change how a plugin/runner invocation preserves or isolates module state. Follow src/_pytest/pytester.py workspace setup, runpytest dispatch and runpytest_subprocess’s separate temporary directory and plugin-name constraints. Follow testing/test_pytester.py inline-run cleanup scenarios and source-file creation tests. Inspect pyproject.toml collection rules before assuming a fixture file is a runnable suite. A documentation/API change also reaches docstrings and the configured docs/doctest path, which is not the same claim as an ordinary test run.

## What to borrow and adapt

Provide a small scenario-building harness when many tests otherwise repeat temporary projects and process setup. Name which isolation is provided and which process/environment behavior remains shared. Keep fixture corpora outside accidental ordinary test collection while leaving their role discoverable. A small plugin can reuse the testing idea without copying pytest’s full contributor workflow, fixture machinery, dependency factors or release process.

## Mismatches and limits

Pytester is specialized infrastructure for testing pytest/plugins, not a universal isolation or sandbox solution. The exact module-cleanup and process paths inspected are bounded; other fixture features and platform behavior were not audited. All test examples and configuration were read only. No subprocess, Python interpreter matrix, docs build or pytest command was run, and source organization alone cannot demonstrate coverage adequacy.

