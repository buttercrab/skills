---
{
  "id": "skill-vercel-react-performance",
  "kind": "skill",
  "title": "Vercel React best practices",
  "summary": "Prioritized React/Next.js implementation rules with detailed incorrect/correct examples and important version-specific qualifications.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "implement",
      "optimize",
      "verify"
    ],
    "contexts": [
      "components",
      "performance",
      "product-interface"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/react-best-practices/SKILL.md",
      "title": "skills/react-best-practices/SKILL.md",
      "locator": "Rule categories; Quick Reference; How to Use",
      "revision": "1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned instruction body and priority categories inspected; no React app or benchmark executed."
  },
  "reuse": "Skill frontmatter declares MIT. Original annotation/source link only; inspect individual dependencies and terms before copying code.",
  "related": [
    "tool-playwright",
    "tool-lighthouse",
    "skill-fixing-motion-performance"
  ]
}
---

# Vercel React best practices

## When to use

Select this after React or Next.js is actually part of the project and the design has implementation consequences for loading, responsiveness or repeated rendering. It is useful for a data-heavy interface whose layout is coherent but whose work arrives late or blocks interaction.

## What to inspect

Start with the relevant priority category, then read the individual rule and its context. A short slogan about imports or caching is not enough. Inspect the project’s framework/version and existing data lifecycle before transferring an example.

## What to borrow and adapt

Borrow prioritization by the actual bottleneck and examples that explain the mechanism. Check independent requests, component boundaries, serialization, loading state and resource cost. Tie a proposed optimization to an observable user path and measure what changes. A dashboard that fetches unrelated panels sequentially raises a different question from an expensive repeated table render.

## Mismatches and limits

It does not choose the product flow, brand voice or visual hierarchy. Listed impact levels are author-maintained priorities, not measurements for this application. React-specific recipes should not migrate an unrelated stack or replace working code without benefit. Some detailed rules include alternatives that a blanket ban would erase. Instructions were read, not benchmarked here.
