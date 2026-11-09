---
{
  "id": "repo-large-cpython",
  "kind": "repository",
  "title": "CPython: pair native error-path changes with regression and generated-file scope",
  "summary": "Trace a C-extension exception-path fix into Python regression coverage while distinguishing targeted tests from configured regeneration, ABI and platform jobs.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "navigate",
      "test-selection",
      "generated-files"
    ],
    "contexts": [
      "native-extension",
      "language-runtime",
      "multi-platform"
    ],
    "languages": [
      "c",
      "python"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/python/cpython/blob/6026791c977a1df2ff8a427aad294388992ae078/README.rst",
      "title": "python/cpython: README.rst",
      "locator": "Build instructions and contribution routing",
      "revision": "6026791c977a1df2ff8a427aad294388992ae078"
    },
    {
      "url": "https://github.com/python/cpython/blob/6026791c977a1df2ff8a427aad294388992ae078/.github/workflows/build.yml",
      "title": "python/cpython: .github/workflows/build.yml",
      "locator": "check-generated-files, check-autoconf-regen and platform job conditions",
      "revision": "6026791c977a1df2ff8a427aad294388992ae078"
    },
    {
      "url": "https://github.com/python/cpython/blob/6026791c977a1df2ff8a427aad294388992ae078/Lib/test/test_tcl.py",
      "title": "python/cpython: Lib/test/test_tcl.py",
      "locator": "test_setvar_evil, lines 604–627",
      "revision": "6026791c977a1df2ff8a427aad294388992ae078"
    },
    {
      "url": "https://github.com/python/cpython/commit/6026791c977a1df2ff8a427aad294388992ae078",
      "title": "python/cpython: pinned change",
      "locator": "Modules/_tkinter.c AsObjNested/SetVar diff and paired Python regression",
      "revision": "6026791c977a1df2ff8a427aad294388992ae078"
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
    "repo-large-node",
    "docs-study-coverage-limits"
  ]
}
---

# CPython: pair native error-path changes with regression and generated-file scope

## When to use

Use when a language runtime, native binding or extension crosses a language exception boundary and the maintainer needs a route from a low-level fix to user-visible behavior. It is also a useful contrast to a repository where a single language's default test command is sufficient.

## What to inspect

Read the pinned exception-path commit, `Lib/test/test_tcl.py::test_setvar_evil`, and the workflow's change detection, regeneration and platform branches. The C diff checks a failed conversion before continuing into Tcl; the Python regression supplies an object whose string conversion raises and checks both the error and absence of a created variable. The README names additional platform/dependency requirements; it is not evidence that every optional standard-library module builds in every environment.

## Change path

Trigger: `setvar` receives an object whose `__str__` raises → C conversion/error handling in `Modules/_tkinter.c` → Python-facing regression in `Lib/test/test_tcl.py` → a build with the relevant Tcl/Tk support and the targeted test suite. Separately, a generated-file/build-input change reaches configured regeneration and ABI checks. The workflow gates these jobs through a reusable change-context job; that referenced job's full decision logic was not audited here.

## What to borrow and adapt

Connect the reproduction to the smallest maintained boundary that must preserve it. A test can assert the failed operation did not leave state behind, not just that an exception occurred. Make optional build prerequisites explicit so a skipped module is not mistaken for exercised coverage. Record relevant configured jobs separately from local results and current remote run status.

The transferable structure is discoverability between authoritative native code, Python tests and build obligations—not the exact directory names or entire CI matrix.

## Mismatches and limits

Source/diff/configuration inspection only: no CPython build, Tcl execution, regeneration, ABI check or CI run occurred. The project has platform and compatibility obligations that a small pure-Python utility may not share. Do not copy its regeneration matrix merely because a project contains C, or infer current branch protections from workflow YAML.

