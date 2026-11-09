---
{
  "id": "tool-storybook",
  "kind": "tool",
  "title": "Storybook: component state catalog and interaction fixtures",
  "summary": "A development catalog for rendering component variants/states and attaching interaction checks to explicit initial conditions.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "compare",
      "verify",
      "compose"
    ],
    "contexts": [
      "components",
      "design-system",
      "regression-testing"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://storybook.js.org/docs/writing-stories",
      "title": "How to write stories",
      "locator": "Story definition; args; CSF; state examples",
      "revision": "Docs version 10.6 inspected 2026-11-07"
    },
    {
      "url": "https://storybook.js.org/docs/writing-tests/interaction-testing",
      "title": "Interaction tests",
      "locator": "Initial state; play function; assertions",
      "revision": "Docs version 10.6 inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official 10.6 story and interaction-test documentation inspected; no component rendered."
  },
  "reuse": "Original annotation and links only. No upstream software, screenshots, templates or proprietary assets redistributed.",
  "related": [
    "skill-shadcn-project-guidance",
    "tool-playwright"
  ]
}
---

# Storybook: component state catalog and interaction fixtures

## When to use

Select Storybook when a component family needs an inspectable state vocabulary, shared review surface or repeatable interaction fixture. It is useful after a design direction exists and the team needs to see whether its controls work across meaningful content and states.

## What to inspect

Read how a story defines initial arguments/context and how an interaction test acts on that state. Inspect representative local stories instead of assuming a component gallery covers the real product. Match the documentation version to the project’s installed version.

## What to borrow and adapt

Borrow making selected, disabled, loading, error, empty and long-content cases explicit where the component supports them. Use a compact set of meaningful variants rather than an exhaustive visual matrix with no tasks. A booking control’s error recovery or a table’s empty-filter state can become a reviewable fixture with a clear expected transition.

## Mismatches and limits

Component isolation can hide routing, authentication, data ownership and page-level layout problems. A polished gallery is not an end-to-end flow or proof of design quality. Mock data and providers must represent the relevant conditions honestly. Publishing stories or adding hosted visual-testing services are separate actions. Documentation was inspected; no Storybook build, play function or visual suite ran.
