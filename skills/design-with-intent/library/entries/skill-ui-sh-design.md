---
{
  "id": "skill-ui-sh-design",
  "kind": "skill",
  "title": "ui.sh design guideline workflow (optional local resource)",
  "summary": "An installed guideline system for Tailwind UI authoring with component-specific references and strong house typography conventions.",
  "status": "curated",
  "availability": "local-only",
  "facets": {
    "tasks": [
      "design",
      "implement",
      "polish"
    ],
    "contexts": [
      "components",
      "design-system",
      "product-interface"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "local:ui-sh/design/SKILL.md",
      "title": "User-supplied ui.sh design skill",
      "locator": "Activation; Load First; Workflow; typography companion rules",
      "revision": "installed/user-supplied snapshot inspected 2026-11-07; upstream version unknown"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "unknown",
    "scope": "User-provided/installed instruction body and typography reference inspected locally. Upstream equivalence and execution unverified."
  },
  "reuse": "Local provenance/license unresolved. Optional link identifier and original annotation only; no local skill text bundled.",
  "related": [
    "skill-anthropic-frontend-design",
    "skill-baseline-ui",
    "tool-ui-sh-picker",
    "skill-taster"
  ]
}
---

# ui.sh design guideline workflow (optional local resource)

## When to use

Select this only when the relevant ui.sh skill bundle is available and the project wants that design system or its component-authoring conventions. It can support consistent implementation after a human has selected a direction; it does not itself provide a broad reference library.

## What to inspect

Read the supplied activation boundaries, design-guidelines index and the applicable component rules. Verify the installed bundle before relying on it: the exact public upstream source/version and local license were not established. A public ui.sh homepage would not prove it matches these installed instructions.

## What to borrow and adapt

Borrow using established project conventions and loading the relevant component guidance before writing code. Preserve the difference between a source rule and a chosen brand convention. Use the guideline index selectively for the actual surface, rather than importing a large unrelated rule set into a narrow correction.

## Mismatches and limits

The inspected typography rules mandate InterVariable and disallow bold headings, while other legitimate systems choose differently. Those are house choices, not general fundamentals. Its broad loading and source-of-truth language cannot override the user’s chosen direction. This optional entry is not a portable dependency: when the bundle is absent, use public alternatives or request the actual source instead of inventing its contents. No UI was built or inspected visually.

## Related resource roles

- [skill-taster](skill-taster.md): The typography house rules differ; resolve against the chosen brand instead of combining incompatible mandates.
