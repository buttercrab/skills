---
{
  "id": "skill-fixing-accessibility",
  "kind": "skill",
  "title": "Fixing accessibility: targeted interface repair",
  "summary": "A narrow code-review skill connecting accessible names, native semantics, keyboard/focus behavior and form recovery to small concrete fixes.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "audit",
      "repair",
      "verify"
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
      "url": "https://github.com/ibelick/ui-skills/blob/00db7d656719c399c091f3ea138c6f42a7fa4d98/skills/fixing-accessibility/SKILL.md",
      "title": "skills/fixing-accessibility/SKILL.md",
      "locator": "Rule categories; quick reference; tool boundaries; common fixes",
      "revision": "00db7d656719c399c091f3ea138c6f42a7fa4d98"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Full pinned skill instructions and examples inspected; no assistive-technology or browser testing."
  },
  "reuse": "Repository LICENSE inspected as MIT at the recorded revision. Original annotation and source links; no upstream code or full instructions copied.",
  "related": [
    "tool-axe-core",
    "tool-playwright",
    "skill-vercel-web-guidelines"
  ]
}
---

# Fixing accessibility: targeted interface repair

## When to use

Select this when an implemented control, form, dialog or navigation element needs accessibility repair while preserving the surrounding design. Its bounded focus is more useful than re-running a broad aesthetic workflow for an unlabeled button or lost-focus problem.

## What to inspect

Read the relevant names, keyboard, focus, semantics or forms category and its tool-boundary section. Follow complex-widget questions into the applicable platform pattern or normative requirement. Priorities in this skill are a working review order, not conformance levels.

## What to borrow and adapt

Borrow the connection from a concrete failure to a minimal change: native control where possible, correct name/state, associated error information, and intelligible focus movement. For a failed signup, inspect whether the error identifies a fix, whether the field retains input, and whether the recovery is operable without a pointer.

## Mismatches and limits

Prescriptive language such as every interaction being reachable by Tab needs widget-specific interpretation; composite widgets may use a tab stop plus arrow navigation. Attribute presence alone does not establish accessible naming or announcements. Do not add redundant ARIA where native semantics already provide the contract. No screen reader, browser or audit was run here, so this is a source-inspected repair procedure rather than accessibility acceptance.
