---
{
  "id": "repo-small-click",
  "kind": "repository",
  "title": "Click: test helpers, process-global state and migration evidence",
  "summary": "A src-layout Python library links test-runner behavior, deprecation guidance, replacement examples and distinct test environments instead of assuming its helper is safe in every parallel setting.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test",
      "document",
      "maintain-api",
      "package"
    ],
    "contexts": [
      "library",
      "cli",
      "compatibility",
      "test-isolation"
    ],
    "languages": [
      "python"
    ],
    "scale": [
      "single-package",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/README.md",
      "title": "pallets/click: README.md",
      "locator": "usage and contributing route",
      "revision": "8abb77a8432e03ed14a95f972b44f905279415a7"
    },
    {
      "url": "https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/pyproject.toml",
      "title": "pallets/click: pyproject.toml",
      "locator": "Flit sdist, tox environments, pytest stress selection and typing",
      "revision": "8abb77a8432e03ed14a95f972b44f905279415a7"
    },
    {
      "url": "https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/src/click/testing.py",
      "title": "pallets/click: src/click/testing.py",
      "locator": "CliRunner.invoke and isolated_filesystem deprecation/warning",
      "revision": "8abb77a8432e03ed14a95f972b44f905279415a7"
    },
    {
      "url": "https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/tests/test_testing.py",
      "title": "pallets/click: tests/test_testing.py",
      "locator": "test_isolated_runner, replacement pattern and thread-safety explanation",
      "revision": "8abb77a8432e03ed14a95f972b44f905279415a7"
    },
    {
      "url": "https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/.github/workflows/tests.yaml",
      "title": "pallets/click: .github/workflows/tests.yaml",
      "locator": "platform/interpreter matrix and typing job",
      "revision": "8abb77a8432e03ed14a95f972b44f905279415a7"
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
    "quality-python-distribution-checks",
    "repo-small-requests"
  ]
}
---

# Click: test helpers, process-global state and migration evidence

## When to use

Use when a library provides test infrastructure that manipulates environment, working directory or standard streams, or when contributors need to distinguish a quick local test command from the compatibility matrix. It also illustrates how a legacy helper can remain present while its recommended use changes.

## What to inspect

The README supplies a small entry example and routes contribution guidance outside this repository. The manifest separates tests, randomized/stress tests, typing and docs environments, uses a wheel in tox, and declares the sdist inclusions. Current source warns that isolated_filesystem changes process-global working directory and invoke redirects process-global streams. The helper is deprecated in favor of temporary directories accessed through absolute paths; the tests contain both legacy behavior and an explicit replacement example.

## Change path

Trigger: change filesystem-isolation behavior or its supported replacement. Follow src/click/testing.py isolated_filesystem and invoke to tests/test_testing.py around test_isolated_runner, test_tempdir_replacement_pattern and the thread-safety explanation. Check the public docstring/deprecation message as part of the API. pyproject.toml defines ordinary, randomized, stress, typing and documentation paths; .github/workflows/tests.yaml wires normal tests and typing to a particular interpreter/platform matrix. The source explains process-based parallelism; no concurrency experiment was run here.

## What to borrow and adapt

Treat test helpers as production APIs with their own environmental promises. Keep a replacement example beside legacy coverage, and distinguish a behavior migration from deleting the old function. Name what a test environment covers: stress cases are deselected by the default pytest option, so a default pass would not establish the stress path. A small team can adopt that distinction without copying the entire matrix or development tooling.

## Mismatches and limits

The inspected revision is development code and includes a planned removal boundary; do not describe it as behavior of every installed Click release. The helper’s name alone is not evidence of thread isolation. Workflow paths ignore docs-only changes and other workflows were not exhaustively audited. No contributor command or upstream code was executed; external Pallets contribution guidance was not inspected for this card.

