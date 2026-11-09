---
{
  "id": "tool-figma-mcp",
  "kind": "tool",
  "title": "Figma MCP: design context and code mappings",
  "summary": "An integration surface for obtaining scoped design context, screenshots and component mappings, with distinct read and write capabilities.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "inspect",
      "implement",
      "document"
    ],
    "contexts": [
      "handoff",
      "design-system",
      "components"
    ],
    "platforms": [
      "web",
      "cross-platform"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/",
      "title": "Figma MCP tools and prompts",
      "locator": "Read/write indexes; get_design_context; screenshot; metadata; Code Connect; remote-only distinctions",
      "revision": "live documentation inspected 2026-11-07"
    },
    {
      "url": "https://www.figma.com/dev-mode/",
      "title": "Figma Dev Mode",
      "locator": "Design-to-development context and component connection",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official public tool index and Dev Mode explanation inspected. No connected account, design file or MCP execution."
  },
  "reuse": "Original annotation and links only. No upstream software, screenshots, templates or proprietary assets redistributed.",
  "related": [
    "skill-create-design-md",
    "tool-chrome-devtools-css"
  ]
}
---

# Figma MCP: design context and code mappings

## When to use

Select this when the person has an accessible Figma artifact and the task is to carry its real design context into an implementation or compare design and code ownership. It can be more appropriate than reconstructing exact values from a screenshot.

## What to inspect

Read the current read/write tool index, platform availability and relevant tool contracts. Identify the exact file, layer or selection and which Code Connect mappings apply. Access, account entitlement and connector availability must be checked in the actual environment.

## What to borrow and adapt

Borrow scoped retrieval: use an outline to locate relevant nodes, then obtain the design context or screenshot needed for the decision. Distinguish an observed value from a declared reusable component mapping. Preserve the person’s design intent and adapt code to the real project rather than treating generated snippets as a ready production contract.

## Mismatches and limits

The current documentation includes canvas-writing and asset-download tools as well as reads; a catalog match does not authorize mutation or redistribution. The integration cannot resolve missing product purpose or prove an implementation works. No account/file was accessed, connector installed, asset downloaded or canvas changed during this curation; only public documentation was inspected.
