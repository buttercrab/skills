---
{
  "id": "repo-large-django",
  "kind": "repository",
  "title": "Django: carry a widget contract through renderers, docs and release notes",
  "summary": "A six-file feature change exposes a maintainable path across implementation, two template engines, regression helper, reference and release communication.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "navigate",
      "test-selection",
      "document",
      "release-notes"
    ],
    "contexts": [
      "framework",
      "multiple-renderers",
      "public-api"
    ],
    "languages": [
      "python",
      "html"
    ],
    "scale": [
      "large-project"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/django/django/blob/a1f2b45ce5a327f42437bdb620a817839d0bd067/CONTRIBUTING.rst",
      "title": "django/django: CONTRIBUTING.rst",
      "locator": "Contribution entry and Trac routing",
      "revision": "a1f2b45ce5a327f42437bdb620a817839d0bd067"
    },
    {
      "url": "https://github.com/django/django/blob/a1f2b45ce5a327f42437bdb620a817839d0bd067/tests/forms_tests/widget_tests/base.py",
      "title": "django/django: tests/forms_tests/widget_tests/base.py",
      "locator": "WidgetTest.setUpClass and check_html",
      "revision": "a1f2b45ce5a327f42437bdb620a817839d0bd067"
    },
    {
      "url": "https://github.com/django/django/blob/a1f2b45ce5a327f42437bdb620a817839d0bd067/tests/runtests.py",
      "title": "django/django: tests/runtests.py",
      "locator": "Imports, warnings and test-module discovery",
      "revision": "a1f2b45ce5a327f42437bdb620a817839d0bd067"
    },
    {
      "url": "https://github.com/django/django/commit/a1f2b45ce5a327f42437bdb620a817839d0bd067",
      "title": "django/django: pinned change",
      "locator": "Textarea input_type addition across implementation, Django/Jinja templates, regression, reference and 6.2 notes",
      "revision": "a1f2b45ce5a327f42437bdb620a817839d0bd067"
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
    "repo-small-flask",
    "quality-python-distribution-checks"
  ]
}
---

# Django: carry a widget contract through renderers, docs and release notes

## When to use

Use for a mature framework or library whose public behavior has several rendering/adaptor implementations and user documentation. A change that looks like one property assignment may cross several contracts.

## What to inspect

The pinned commit changes `Textarea.input_type`, both Django and Jinja2 textarea templates, tests, reference documentation and release notes. Read the shared `WidgetTest` helper as well: it creates and exercises Jinja2 only if that dependency imports successfully. This qualifies what a successful local run could establish. The contributor entry routes nontrivial patches through Trac; it does not make that tracker appropriate for unrelated projects.

## Change path

Trigger: allow a textarea widget's input type to participate in hidden rendering → implementation in `django/forms/widgets.py` → two owning template files → `tests/forms_tests/widget_tests/test_textarea.py` through `WidgetTest.check_html` → documented property in `docs/ref/forms/widgets.txt` and versioned communication in `docs/releases/6.2.txt`. The test launcher discovers suites and treats relevant warnings as errors; the inspected launcher prefix does not establish coverage of every backend.

## What to borrow and adapt

Map all maintained presentations of a public contract before editing. Keep implementation and focused regression traceable even when they live in separate trees. Follow test helpers far enough to understand optional dependencies and renderer coverage; “the tests passed” should name the exercised environment. Put durable reference semantics and release-specific communication in their respective places instead of duplicating both into a top-level README.

For a single-renderer internal service, one implementation and an existing local test path may be sufficient. Add release communication only where consumers need it.

## Mismatches and limits

The actual six-file diff and helper were inspected, not executed. No browser output, database matrix, Jinja installation or green CI is claimed. A missing dependency narrows a run; it does not prove a repository defect. Django's tracker, governance and version policy are local choices, not a mandatory contribution template.

