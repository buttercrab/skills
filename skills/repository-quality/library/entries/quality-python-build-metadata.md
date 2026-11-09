---
{
  "id": "quality-python-build-metadata",
  "kind": "guide",
  "title": "Python: separate build inputs, package metadata and development tools",
  "summary": "Make pyproject.toml ownership explicit so build requirements, installed dependencies and development configuration do not become interchangeable lists.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "configure",
      "package",
      "document"
    ],
    "contexts": [
      "build-metadata",
      "dependency-boundaries"
    ],
    "languages": [
      "python"
    ],
    "scale": [
      "single-package",
      "multi-package"
    ]
  },
  "sources": [
    {
      "url": "https://packaging.python.org/en/latest/guides/writing-pyproject-toml/",
      "title": "PyPA: Writing your pyproject.toml",
      "locator": "Build backend; project/dependency groups/tool tables; scripts; requires-python; README/license fields",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://peps.python.org/pep-0517/",
      "title": "PEP 517: build-system interface",
      "locator": "build_wheel/build_sdist hooks; optional requirements hooks; build environment",
      "revision": "Final packaging PEP; substantive hook/environment sections read 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Primary documentation sections read. No build, package installation, test, generator, publishing command, authentication change or upstream script executed."
  },
  "reuse": "Original annotations and source links only. Upstream source, standards text, binaries and assets are not redistributed; this is not a legal opinion.",
  "related": [
    "quality-python-import-layout",
    "quality-python-distribution-checks"
  ]
}
---

# Python: separate build inputs, package metadata and development tools

## When to use

Use when a repository mixes developer setup with package installation requirements, changes a CLI entry point, or replaces a build backend. This is a metadata and distribution boundary question before it is a tool-choice question.

## What to inspect

Read the selected backend and its required build environment, the package's installed requirements, developer groups and tool-specific tables separately. The PyPA guide explains these roles; PEP 517 defines the frontend/backend hook boundary and build-requirement availability. Neither establishes that a repository's current declarations are complete merely because the file parses.

## What to borrow and adapt

For a new command, connect its declared script target to the owning callable, installed dependencies and the README's invocation. A useful acceptance path builds the distributable and checks the command in the environment promised to users. Keep development-only linters out of runtime requirements unless the product actually imports them. Conversely, a test environment that happens to contain a missing runtime dependency must not be mistaken for a complete package contract.

Preserve one authoritative version source where the backend supports it and document how derived metadata is obtained. Choose a backend based on the package's real build needs; a pure Python library and a compiled extension need not adopt the same machinery.

## Mismatches and limits

These documents do not recommend migrating every existing project or deleting valid legacy configuration. Backend-specific capabilities and supported metadata versions still need inspection. PEP 517 isolation concerns build requirements; it does not by itself reproduce every supported runtime or supply permission to run packaging hooks from an untrusted repository.
