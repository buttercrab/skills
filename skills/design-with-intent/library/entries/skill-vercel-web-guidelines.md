---
{
  "id": "skill-vercel-web-guidelines",
  "kind": "skill",
  "title": "Vercel Web Interface Guidelines review",
  "summary": "A lightweight review entrypoint that fetches a larger current rubric and returns concrete file/line findings.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "audit",
      "critique",
      "verify"
    ],
    "contexts": [
      "components",
      "product-interface",
      "accessibility"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/web-design-guidelines/SKILL.md",
      "title": "skills/web-design-guidelines/SKILL.md",
      "locator": "How It Works; Guidelines Source; Usage",
      "revision": "1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62"
    },
    {
      "url": "https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md",
      "title": "Web Interface Guidelines",
      "locator": "Accessibility; Typography; Content; Motion; anti-patterns",
      "revision": "mutable main; inspected in prior evidence pass 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned entrypoint inspected; prior same-day rubric evidence retained. No review execution or rendered output inspected."
  },
  "reuse": "Link and original annotation only. License declaration for Vercel React is inspected separately; do not infer identical terms for every remote rubric.",
  "related": [
    "skill-fixing-accessibility",
    "tool-axe-core",
    "tool-lighthouse"
  ]
}
---

# Vercel Web Interface Guidelines review

## When to use

Select this for a bounded review of existing web-interface code when the immediate need is actionable findings rather than a new visual world. It complements a design direction by checking implementation details across semantics, content, layout robustness and interaction.

## What to inspect

Read the entrypoint and then the linked rubric actually in force. Record the loaded rubric revision or content date separately: pinning the entrypoint does not pin its remote dependency. The inspected entrypoint asks for target files when none are identified.

## What to borrow and adapt

Borrow a concise evidence-to-fix report: locate a concrete element or declaration, explain its consequence, and propose a scoped repair. Apply the relevant checks to the changed surface. For a settings form, this can expose a missing control name or misleading loading label while retaining the established brand and layout.

## Mismatches and limits

The procedure is a review mechanism, not a source of distinctive art direction. Its instruction to fetch and obey every remote rule must yield to task scope and higher-priority constraints. Never treat a current fetch as proven current runtime behavior. This curation inspected instructions; it did not execute the review or establish the rubric’s measured effectiveness.
