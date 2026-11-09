---
{
  "id": "tool-axe-core",
  "kind": "tool",
  "title": "axe-core: state-scoped accessibility checks",
  "summary": "A browser accessibility engine whose context, rule selection and result categories support targeted checks of actual rendered states.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "verify",
      "audit",
      "recover"
    ],
    "contexts": [
      "accessibility",
      "forms",
      "components"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/dequelabs/axe-core/blob/develop/doc/API.md",
      "title": "Axe JavaScript Accessibility API",
      "locator": "Getting Started; API Notes; axe.run context/options/results",
      "revision": "develop, inspected 2026-11-07; not-pinned"
    },
    {
      "url": "https://playwright.dev/docs/accessibility-testing",
      "title": "Playwright accessibility testing",
      "locator": "Introduction disclaimer; Scanning a specific part of a page",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "API documentation and example test sequence inspected. The engine was not installed or executed."
  },
  "reuse": "Documentation linked with original annotation. Library redistribution/license not audited in this card; obtain relevant terms before copying packages.",
  "related": [
    "skill-fixing-accessibility",
    "tool-playwright",
    "tool-lighthouse",
    "standard-wcag-conformance",
    "principle-native-semantics"
  ]
}
---

# axe-core: state-scoped accessibility checks

## When to use

Select axe-core as one verification instrument when an implemented web interface needs repeatable checks for automatically detectable accessibility problems. It fits an existing browser-testing workflow and can target a changed component or state instead of treating the whole application as one static screenshot.

## What to inspect

Read the API Notes and `axe.run` context/options/results contract. The Playwright guide gives a concrete sequence that opens a menu, waits for its visible state and scans that region. Check current integration versions before adding tooling to the project.

## What to borrow and adapt

Borrow state-scoped testing: reach the relevant state first, run the appropriate checks, retain the result categories and inspect the referenced elements. Apply this to an error summary, expanded menu, open dialog or dynamically filtered result. Choose rules and exclusions according to the claim being made, documenting meaningful exclusions rather than suppressing unexplained failures.

Keep a route for incomplete results needing human review. Complement the scan with keyboard, focus, content and intended-user checks; tool output is one evidence source.

## Mismatches and limits

The API checks rendered content, so a clean initial-page scan does not cover hidden menus or future errors. Automated checks cannot establish all WCAG requirements, reader comprehension or task usability. No scan ran during this curation pass. Selecting this card does not authorize an installation, accessing a prohibited page, or treating an unavailable browser as permission to try another route.

## Related resource roles

- [standard-wcag-conformance](standard-wcag-conformance.md): An automated scan cannot by itself establish complete-process conformance.
- [principle-native-semantics](principle-native-semantics.md): Control semantics and keyboard behavior complement automatically detectable findings.
