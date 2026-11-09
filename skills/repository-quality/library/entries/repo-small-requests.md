---
{
  "id": "repo-small-requests",
  "kind": "repository",
  "title": "Requests: follow a security-sensitive behavior beyond the friendly entry example",
  "summary": "A compact user-facing API leads to session implementation, local and HTTP fixture tests, packaging metadata and distinct interpreter/environment declarations.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "test",
      "maintain-api",
      "package",
      "check-compatibility"
    ],
    "contexts": [
      "library",
      "http",
      "security-boundary",
      "integration-tests"
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
      "url": "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/README.md",
      "title": "psf/requests: README.md",
      "locator": "usage and supported-version statement",
      "revision": "3c7baaa05ab4aa49cc819ce3a819d260de19c157"
    },
    {
      "url": "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/pyproject.toml",
      "title": "psf/requests: pyproject.toml",
      "locator": "project metadata, src package discovery and test dependencies",
      "revision": "3c7baaa05ab4aa49cc819ce3a819d260de19c157"
    },
    {
      "url": "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/tox.ini",
      "title": "psf/requests: tox.ini",
      "locator": "interpreter/extras environments and pytest target",
      "revision": "3c7baaa05ab4aa49cc819ce3a819d260de19c157"
    },
    {
      "url": "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py",
      "title": "psf/requests: src/requests/sessions.py",
      "locator": "rebuild_auth and merge_setting",
      "revision": "3c7baaa05ab4aa49cc819ce3a819d260de19c157"
    },
    {
      "url": "https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/tests/test_requests.py",
      "title": "psf/requests: tests/test_requests.py",
      "locator": "redirect authentication and should_strip_auth cases",
      "revision": "3c7baaa05ab4aa49cc819ce3a819d260de19c157"
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
    "quality-python-build-metadata",
    "repo-small-click"
  ]
}
---

# Requests: follow a security-sensitive behavior beyond the friendly entry example

## When to use

Use when a deceptively simple API has behavior crossing network, credentials and environment boundaries. It is a useful repository-assessment example for separating a quick-start example from the source and fixture infrastructure needed to safely change semantics.

## What to inspect

The manifest discovers packages under src and derives the version from the package. Its test dependency group includes HTTP and TLS-related fixtures; tox defines interpreter and optional-encoding combinations. Read rebuild_auth and its removal/reapplication of Authorization across redirects, then the tests for downgrade, same-host and host-change behavior. merge_setting separately shows request/session precedence, including removal of keys set to None.

## Change path

Trigger: alter whether redirecting a request retains authentication. Follow src/requests/sessions.py rebuild_auth and should_strip_auth callers to tests/test_requests.py around the HTTP-downgrade, same-host and direct should_strip_auth tests. The HTTP test relies on httpbin/TLS fixture setup while direct helper tests do not exercise that same boundary. tox invokes pytest across configured variants; the pyproject test group describes additional fixture dependencies. Version metadata and source packaging remain separate maintenance concerns.

## What to borrow and adapt

Make dependency-sensitive fixtures and direct unit scenarios discoverable as distinct evidence. An agent assessing a repository should identify which test crosses the changed trust boundary before selecting commands. Also compare declarations rather than flattening them: this revision lists Python 3.15 in project classifiers, while the inspected tox interpreter list stops at 3.14. That difference calls for inspecting the remaining CI configuration before making a support or coverage claim.

## Mismatches and limits

The interpreter-list difference is not a demonstrated defect; classifiers and tox serve different roles, and other checks may exist. A friendly README, download claim or narrow API does not establish implementation simplicity or security. No live request, local fixture server, credential transmission, CI run, build or installed distribution was exercised. Commands in the README are source material, not research instructions.

