---
{
  "id": "skill-baseline-ui",
  "kind": "skill",
  "title": "Baseline UI: opinionated cleanup checklist",
  "summary": "An implementation-oriented cleanup skill for spacing, hierarchy and common interface defects, with strong stack and aesthetic prescriptions.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "polish",
      "audit",
      "implement"
    ],
    "contexts": [
      "components",
      "product-interface"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/ibelick/ui-skills/blob/00db7d656719c399c091f3ea138c6f42a7fa4d98/skills/baseline-ui/SKILL.md",
      "title": "skills/baseline-ui/SKILL.md",
      "locator": "Stack; Components; Interaction; Animation; Typography; Design",
      "revision": "00db7d656719c399c091f3ea138c6f42a7fa4d98"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Full pinned instruction body inspected. No tool execution or visual output inspected."
  },
  "reuse": "Repository LICENSE inspected as MIT at the recorded revision. Original annotation and source links; no upstream code or full instructions copied.",
  "related": [
    "skill-ui-sh-design",
    "skill-fixing-accessibility",
    "skill-fixing-motion-performance"
  ]
}
---

# Baseline UI: opinionated cleanup checklist

## When to use

Select this for a fast, scoped cleanup of an existing web surface when the project already resembles the supported component and Tailwind ecosystem. It can supply concrete review leads when “make it polished” has not yet been translated into inspectable defects.

## What to inspect

Read the target-file review contract and the exact category relevant to the issue. Inspect existing primitives before adopting the stack section. The checklist combines semantic/behavioral concerns with conventions about gradients, tracking, timing, shadows and accent usage.

## What to borrow and adapt

Borrow the requirement to identify the offending snippet, explain the user consequence and suggest a code-level fix. Preserve the project’s components and test actual focus/error/empty behavior. For a crowded settings panel, use the hierarchy and local-error prompts to investigate legibility and recovery, then select only repairs justified by that panel.

## Mismatches and limits

The mandatory library choices and broad aesthetic prohibitions are house policy. They conflict with other legitimate visual directions, including intentionally expressive briefs. Fixed timing or blanket attribute recipes need contextual and standards checks. A clean checklist does not demonstrate usable behavior or absence of generic design. No cleanup was executed or visual result judged in this curation.
