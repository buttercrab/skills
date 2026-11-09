---
{
  "id": "repo-small-flask",
  "kind": "repository",
  "title": "Flask: framework tests are not a mandatory application layout",
  "summary": "A Python framework separates source, tests and packaged documentation while testing client/session behavior without imposing that repository structure on downstream applications.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "organize",
      "test",
      "package",
      "document"
    ],
    "contexts": [
      "framework",
      "application-boundary",
      "dependency-compatibility"
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
      "url": "https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/README.md",
      "title": "pallets/flask: README.md",
      "locator": "project-layout stance and simple application example",
      "revision": "49943b5a94413a530761350f04e896f76e8d620e"
    },
    {
      "url": "https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/pyproject.toml",
      "title": "pallets/flask: pyproject.toml",
      "locator": "dependencies, Flit packaging, tests-min/tests-dev and docs/typing",
      "revision": "49943b5a94413a530761350f04e896f76e8d620e"
    },
    {
      "url": "https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/src/flask/testing.py",
      "title": "pallets/flask: src/flask/testing.py",
      "locator": "session_transaction and open",
      "revision": "49943b5a94413a530761350f04e896f76e8d620e"
    },
    {
      "url": "https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/tests/test_testing.py",
      "title": "pallets/flask: tests/test_testing.py",
      "locator": "session transaction, IPv6 and context cases",
      "revision": "49943b5a94413a530761350f04e896f76e8d620e"
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
    "quality-python-import-layout",
    "repo-large-django"
  ]
}
---

# Flask: framework tests are not a mandatory application layout

## When to use

Use when someone copies a framework’s own repository into an application scaffold, or treats an easy introductory app as evidence that framework maintenance is equally simple. The contrast helps ask which boundary belongs to the maintained library and which belongs to its users.

## What to inspect

The README explicitly leaves application tools and project layout to developers. In contrast, the framework repository has a src package, tests and package metadata with documentation/examples/test sdist inclusions. The tox configuration distinguishes ordinary testing from minimum-dependency and development-dependency environments. Read the session_transaction context manager and related tests: this helper interacts with request context, cookies and session storage rather than being only a convenience wrapper.

## Change path

Trigger: change how the test client stores a session across requests. Follow src/flask/testing.py session_transaction into its cookie/request-context steps and tests/test_testing.py session and IPv6 cases. A change to preserved request contexts also reaches FlaskClient.open and its cleanup/re-push logic. pyproject.toml supplies test selection, wheel packaging and dependency-variant environments. The observed path identifies relevant tests and compatibility questions; it does not establish any test has passed.

## What to borrow and adapt

Explain the owner and purpose of each structural boundary. A framework’s compatibility suite can justify dedicated tests and dependency variants; a two-route application may need a much smaller arrangement. Keep examples discoverable without letting example simplicity erase library constraints. For a dependency-sensitive change, choose the minimum/latest or development dependency checks that actually exercise it instead of equating one environment with all supported combinations.

## Mismatches and limits

The card concerns maintenance of Flask itself, not deployment architecture or a prescribed Flask application structure. A published sdist was not built or inspected, and CI/environment availability was not checked. Source/test sections were read at one development revision; no HTTP request, test client or command was executed. The source does not prove that unrelated projects benefit from Flit, tox or the same directory names.

