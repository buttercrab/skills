---
{
  "id": "quality-python-import-layout",
  "kind": "guide",
  "title": "Python: layout should expose the import boundary",
  "summary": "Choose src or flat layout by which code tests import and what developers must install, rather than imposing one directory tree.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "organize",
      "test",
      "package"
    ],
    "contexts": [
      "import-boundaries",
      "developer-setup"
    ],
    "languages": [
      "python"
    ],
    "scale": [
      "small-project",
      "single-package"
    ]
  },
  "sources": [
    {
      "url": "https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/",
      "title": "PyPA: src layout vs flat layout",
      "locator": "Behavior differences: installation, current-directory imports and editable path exposure",
      "revision": "Live documentation read 2026-11-07; not a pinned implementation revision"
    },
    {
      "url": "https://docs.pytest.org/en/stable/explanation/goodpractices.html",
      "title": "pytest: Good Integration Practices",
      "locator": "Choosing a test layout; tests outside application code; import modes",
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
    "repo-small-flask",
    "quality-python-build-metadata"
  ]
}
---

# Python: layout should expose the import boundary

## When to use

Use when a Python library works from a checkout but fails for an installed user, or when deciding whether a growing package should move under `src/`. A small private script with no distribution promise has different needs from a package used by strangers.

## What to inspect

Read the actual import path and test invocation along with package discovery configuration. PyPA describes the installation step introduced by src layout and the way root imports can shadow the installed distribution. pytest discusses both external and in-package tests and distinguishes editable, installed and direct-source runs. These are alternatives with different purposes, not a universal rule that tests must occupy one folder.

## What to borrow and adapt

For a library whose missing resource escaped tests, trace: resource declaration → build inclusion → installed import → resource lookup. Propose an isolated artifact smoke check alongside fast editable development. If moving directories, include package discovery, test configuration, documentation commands and import assumptions in the same change path. Merely renaming a directory does not establish that the installed artifact is being exercised.

For an internal one-file tool, retain the simpler layout unless a concrete import or distribution problem warrants migration. The useful property is an explicit import boundary, not the string `src`.

## Mismatches and limits

The guidance was read, not tried against a package. Src layout reduces particular shadowing risks; it cannot prove correct wheel contents or successful downstream installation. Flat layout is not a demonstrated defect. Test invocation and interpreter environment can change which copy is imported even when the tree looks conventional.
