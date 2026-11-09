---
{
  "id": "diagram-c4-context-container",
  "kind": "notation",
  "title": "C4: separate system context from container responsibility",
  "summary": "Use distinct zoom levels for people/external systems and internal applications/data stores without confusing C4 containers with runtime infrastructure.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "diagram",
      "decompose",
      "document"
    ],
    "contexts": [
      "system-context",
      "logical-structure"
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
      "url": "https://c4model.com/diagrams/system-context",
      "title": "C4 System context diagram",
      "locator": "Scope, primary/supporting elements and intended audience",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://c4model.com/diagrams/container",
      "title": "C4 Container diagram",
      "locator": "Container definition, scope and deployment limitation",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://c4model.com/diagrams/notation",
      "title": "C4 Notation",
      "locator": "Diagrams, elements and relationships",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://c4model.com/diagrams/checklist",
      "title": "C4 Review checklist",
      "locator": "Scope/type and relationship meaning",
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
    "foundation-information-hiding",
    "system-postgresql-process-isolation"
  ]
}
---

# C4: separate system context from container responsibility

## When to use

Use when a conversation mixes the system's outside commitments with internal responsibilities. A newcomer, product stakeholder and operator may need different zoom levels; a single dense diagram can obscure which question is being answered.

## What to inspect

The context page limits its primary scope to one software system and its directly connected people/systems. The container page zooms into applications and data stores, not Docker instances. Its notes explicitly defer clustering, replication and failover to deployment views. Notation/review guidance makes relationship intent and abstraction type explicit rather than relying on colors or familiar icons.

## Diagram implications

Give each view a scope and status such as current-source model or proposal. In a context view, show who submits a job and which outside service receives a result. In the container view, explain which application accepts the request, which store owns the job and how the worker communicates. Keep stable names across views; label dependency/data/control relationships deliberately. A box surrounding several components is not evidence of an isolation or transaction boundary.

## What to borrow and adapt

Borrow the zoom discipline and responsibility descriptions. For a local utility, one context plus a small internal map may be enough; do not create four levels just because the vocabulary exists. For an existing product, map names to inspected code/configuration before labeling the diagram as current. If the relevant decision is a single boundary, show only that part with surrounding context.

## Mismatches and limits

These are diagramming recommendations, not evidence that the depicted architecture is deployed or effective. The site's recommendation to use particular diagrams does not make them mandatory for every task. Communication labels cannot prove latency, delivery semantics or data durability. No example image or live system was viewed here.
