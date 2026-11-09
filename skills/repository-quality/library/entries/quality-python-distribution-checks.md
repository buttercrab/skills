---
{
  "id": "quality-python-distribution-checks",
  "kind": "guide",
  "title": "Python: test the distributed artifact as well as editable code",
  "summary": "Separate rapid source-tree feedback from checks that installation, metadata, entry points and packaged resources reach downstream users.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test",
      "package",
      "verify"
    ],
    "contexts": [
      "editable-installs",
      "artifact-boundaries"
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
      "url": "https://peps.python.org/pep-0660/",
      "title": "PEP 660: editable installs",
      "locator": "Terminology/goals; build_editable metadata; changes requiring reinstallation",
      "revision": "Final PEP 660; sections read 2026-11-07"
    },
    {
      "url": "https://packaging.python.org/en/latest/flow/",
      "title": "PyPA: The Packaging Flow",
      "locator": "Source tree/configuration → sdist/wheel → distribution service → installation",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://docs.pytest.org/en/stable/explanation/goodpractices.html",
      "title": "pytest: Good Integration Practices",
      "locator": "External tests against installed or editable packages; in-package tests with --pyargs",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
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
    "repo-small-click",
    "docs-study-coverage-limits"
  ]
}
---

# Python: test the distributed artifact as well as editable code

## When to use

Use when source tests pass but installed consumers lose a data file, executable or dependency, and when release confidence depends on more than a developer's working environment.

## What to inspect

Follow the specific artifact consumers receive. PyPA distinguishes the source tree, source distribution and wheel. PEP 660 expects editable imports/metadata to resemble regular installation but permits backend-dependent differences and identifies configuration changes that require reinstallation. pytest describes ways to run external or included tests against an installed package. These sources jointly explain why an editable run and artifact check answer different questions.

## What to borrow and adapt

For a command that reads a packaged template, retain fast source tests for parsing logic and add a consumer-shaped check of the built package: import the public entry, invoke the command and load that template in an isolated environment. Ensure the working directory does not accidentally supply the checkout package. If source distributions are a supported delivery route, check that their required build inputs are present too.

Record which interpreter, artifact and dependency conditions were reached. A pure Python wheel may need a different validation sample from native wheels whose compatibility depends on interpreter, OS and architecture. Select the matrix from support promises and changed risk rather than copying a mature project's full release farm.

## Mismatches and limits

No package was built or installed during this research. A proposed artifact smoke test is not evidence that publication succeeded, that every native wheel works, or that the runtime is fully isolated. A local script that is not distributed as a package may not need a wheel workflow at all.
