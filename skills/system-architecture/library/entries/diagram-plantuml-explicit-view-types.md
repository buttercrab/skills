---
{
  "id": "diagram-plantuml-explicit-view-types",
  "kind": "tool",
  "title": "PlantUML: choose structural, deployment or sequence meaning",
  "summary": "Use source-controlled component/interface, infrastructure and interaction notation as distinct views rather than treating every box/arrow as interchangeable.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "diagram",
      "document",
      "compare"
    ],
    "contexts": [
      "source-controlled-diagrams",
      "uml-style-views"
    ],
    "qualities": [
      "understandability",
      "evolvability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://plantuml.com/component-diagram",
      "title": "PlantUML Component diagrams",
      "locator": "Components, aliases, interfaces and basic relationships",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://plantuml.com/deployment-diagram",
      "title": "PlantUML Deployment diagrams",
      "locator": "Element kinds, nesting and aliases",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://plantuml.com/sequence-diagram",
      "title": "PlantUML Sequence diagrams",
      "locator": "Participants/messages, grouping and sequence-specific arrow behavior",
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
    "diagram-c4-deployment-mapping",
    "diagram-structurizr-model-views"
  ]
}
---

# PlantUML: choose structural, deployment or sequence meaning

## When to use

Use when a team already works with textual UML-style diagrams or needs an explicit contrast between logical components, runtime nodes and interaction participants. It is a representation choice, not a reason to remodel the architecture into a particular style.

## What to inspect

Component syntax provides named components/interfaces and aliases. Deployment syntax offers node/artifact/process and nested-element forms. Sequence syntax supplies participant ordering, messages and grouped alternatives/loops. Arrow interpretation differs across diagram types; do not infer that a familiar line style has one global meaning.

## Diagram implications

State the view type and scope, then choose the appropriate elements. A nested node is not inherently a security boundary, and an interface symbol is not proof of a tested contract. Use explicit labels and a legend for conventions the audience may not know. Keep optional detail out of the main view when it prevents the reader from following the important boundary.

## What to borrow and adapt

For a design review, use a component view to discuss responsibility, then a small sequence for a selected timeout or cancellation path only if needed. Keep IDs/source and the reason for the view beside the text. Authoring source can be reviewed with code; changed output still deserves visual inspection when readability is promised.

## Mismatches and limits

Tool documentation does not demonstrate diagram comprehension, architecture correctness or current system behavior. Hosted rendering routes receive diagram source; use an authorized route for the actual data. Nothing here requires uploading a private model, installing the advertised browser extension or invoking external includes. Syntax/examples were read; no tool, image, extension or rendered result was inspected or executed.
