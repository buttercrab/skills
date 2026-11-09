---
{
  "id": "skill-create-design-md",
  "kind": "skill",
  "title": "Create DESIGN.md from observed governing evidence",
  "summary": "A design-document extraction skill separating repository authority from a reconstructed public-site observation, with a strict output/export contract.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "document",
      "inspect",
      "maintain"
    ],
    "contexts": [
      "design-system",
      "existing-product",
      "handoff"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/ibelick/ui-skills/blob/00db7d656719c399c091f3ea138c6f42a7fa4d98/skills/create-design-md/SKILL.md",
      "title": "skills/create-design-md/SKILL.md",
      "locator": "Choose the mode; Shared evidence pipeline; Trace evidence; Write; Validate",
      "revision": "00db7d656719c399c091f3ea138c6f42a7fa4d98"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Full pinned skill instruction and schema/export sections inspected; no generated document or CLI execution."
  },
  "reuse": "Repository LICENSE inspected as MIT at the recorded revision. Original annotation and source links; no upstream code or full instructions copied.",
  "related": [
    "tool-chrome-devtools-css",
    "tool-figma-mcp",
    "tool-awesome-design-md"
  ]
}
---

# Create DESIGN.md from observed governing evidence

## When to use

Select this when the task is to preserve an existing product’s design language in a document that other agents can use. It is particularly relevant when repeated local styling risks being mistaken for intentional shared design decisions.

## What to inspect

Read repository versus URL mode, evidence promotion, output schema and validation/export requirements. Repository mode traces governing tokens and owners. URL mode requires rendered and computed evidence and labels the result reconstructed; a screenshot cannot supply exact token names or hidden rationale.

## What to borrow and adapt

Borrow the discipline of recording source, role, scope, recurrence and uncertainty before promoting a design rule. In an existing application, distinguish a shared semantic token from a one-off literal. Preserve accepted design choices and expose conflicts separately. The product owner can then correct a grounded interpretation instead of reviewing an invented brand manifesto.

## Mismatches and limits

The particular DESIGN.md schema and Google export commands are dependencies of this workflow, not universal documentation requirements. Its instruction to install/run current tooling is not authorized by catalog selection. Its strict output gates should not prevent a requested evidence report when the user did not request that format. No document extraction, lint or export was executed here.
