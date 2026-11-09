---
{
  "id": "skill-fixing-motion-performance",
  "kind": "skill",
  "title": "Fixing motion performance",
  "summary": "A rendering-work checklist for diagnosing jank while retaining purposeful motion and the existing animation system.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "optimize",
      "repair",
      "verify"
    ],
    "contexts": [
      "motion",
      "performance",
      "components"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/ibelick/ui-skills/blob/00db7d656719c399c091f3ea138c6f42a7fa4d98/skills/fixing-motion-performance/SKILL.md",
      "title": "skills/fixing-motion-performance/SKILL.md",
      "locator": "Rendering glossary; choose mechanism; measurement; scroll; layers; tool boundaries",
      "revision": "00db7d656719c399c091f3ea138c6f42a7fa4d98"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Full pinned instruction body inspected; no animation/profiling execution."
  },
  "reuse": "Repository LICENSE inspected as MIT at the recorded revision. Original annotation and source links; no upstream code or full instructions copied.",
  "related": [
    "tool-lighthouse",
    "skill-vercel-react-performance"
  ]
}
---

# Fixing motion performance

## When to use

Select this when a specific transition or scroll-linked effect is visibly expensive or technically suspect. It fits a constrained performance repair after the purpose of the motion is understood; it is not a reason to animate an otherwise settled interface.

## What to inspect

Read the rendering glossary, mechanism choice and measurement sections together. Inspect the actual animated surface, frequency and interruption requirements. The layer section explicitly says not to assume compositor promotion; verify the relevant behavior with suitable tools when performance matters.

## What to borrow and adapt

Borrow batching of measurements/writes, bounded execution, off-screen stopping and cheaper alternative mechanisms. Preserve the interaction’s meaning while reducing unnecessary work. A small local affordance and a continuously changing full-screen surface need different cost analysis. Trace the existing library before changing its API or mixing another system into the same component.

## Mismatches and limits

Timing, blur limits and View Transition restrictions are opinionated guidelines rather than universal browser guarantees. Transforming an element can change layout semantics or hit targets even if it is cheap to composite. Choose techniques against measured behavior and current browser support. No animation, trace or benchmark was executed for this card; the evidence establishes the procedure’s contents only.
