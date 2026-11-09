---
{
  "id": "diagram-arc42-consistent-views",
  "kind": "notation",
  "title": "arc42 views: connect context, structure, runtime and deployment",
  "summary": "Select mutually consistent views for a concrete architecture question, with traceable building blocks and explicit quality scenarios.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "diagram",
      "document",
      "trace"
    ],
    "contexts": [
      "multiview-documentation",
      "quality-scenarios"
    ],
    "qualities": [
      "understandability",
      "evolvability",
      "operability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://docs.arc42.org/section-3/",
      "title": "arc42 Context and scope",
      "locator": "Business versus technical context, interfaces and tabular alternatives",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.arc42.org/section-5/",
      "title": "arc42 Building block view",
      "locator": "Whitebox/blackbox responsibility, interfaces and code columns",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.arc42.org/section-6/",
      "title": "arc42 Runtime view",
      "locator": "Representative behavior and exception scenarios",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.arc42.org/section-7/",
      "title": "arc42 Deployment view",
      "locator": "Infrastructure and software mapping",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.arc42.org/section-10/",
      "title": "arc42 Quality requirements",
      "locator": "Specific usage/change scenarios and response measures",
      "revision": "Mutable official documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Fresh official documentation text and selected source examples inspected. No source diagram image was visually viewed, and no parser, renderer, installed tool, generated output or system interaction was executed in this curation."
  },
  "reuse": "Original annotations and source links only. No upstream images, manuals, implementations or packages redistributed; source-specific asset reuse rights must be checked before copying.",
  "related": [
    "foundation-quality-scenarios",
    "diagram-c4-runtime-scenario"
  ]
}
---

# arc42 views: connect context, structure, runtime and deployment

## When to use

Use when a design document has plausible pictures that disagree about names, responsibilities, environments or guarantees. It is a useful organizing reference for an existing-system assessment or a proposal that must explain both behavior and structure.

## What to inspect

Read the distinction between domain-facing context and technical channels. Building-block descriptions can connect responsibility and interface to code locations. Runtime scenarios expose selected interactions, including exceptions. Deployment maps software onto infrastructure. Quality scenarios make an important stimulus, context and response measurable; the template also permits concise tabular descriptions.

## Diagram implications

Choose views for the questions being answered rather than fill every heading. Reconcile identifiers and interfaces across them. A runtime actor should map to a known building block or be marked external; an environment-specific instance should map to a logical role. Put an unresolved quality requirement beside the relevant boundary instead of attaching an invented performance number to an arrow.

## What to borrow and adapt

For an offline capture tool, context can explain sync partners, the runtime scenario can show local save versus acknowledged sync, and a small mapping can identify which device owns each state. If the task concerns only module ownership, a responsibility/interface/code table can be more economical. Preserve the reason for the selected decomposition and a real validation question.

## Mismatches and limits

arc42 describes a documentation framework; its internal mandatory-language conventions are not authority to expand a small user request into a full architecture document. Consistent naming does not establish correct implementation or operational guarantees. The sections and examples' source text were inspected, not the example systems or rendered diagrams. Foundation-level architecture evaluation is a separate resource role.
