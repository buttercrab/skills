---
{
  "id": "diagram-structurizr-model-views",
  "kind": "tool",
  "title": "Structurizr DSL: share a model across selected views",
  "summary": "Reuse named elements and relationships across static, dynamic and deployment views while checking parser context, implied relationships and export limits.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "diagram",
      "document",
      "verify"
    ],
    "contexts": [
      "model-based-diagrams",
      "multiview-documentation"
    ],
    "qualities": [
      "evolvability",
      "understandability"
    ],
    "scale": [
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://docs.structurizr.com/dsl/language",
      "title": "Structurizr DSL language reference",
      "locator": "model/views; dynamic/deployment scope; stable view keys; export style notes",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.structurizr.com/dsl/identifiers",
      "title": "Structurizr Identifiers",
      "locator": "Element/relationship references and flat versus hierarchical scope",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.structurizr.com/dsl/implied-relationships",
      "title": "Structurizr Implied relationships",
      "locator": "Default creation and configurable strategies",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.structurizr.com/dsl/cookbook/dynamic-view/",
      "title": "Structurizr Dynamic view cookbook",
      "locator": "Two feature views over one static relationship",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.structurizr.com/dsl/cookbook/deployment-view/",
      "title": "Structurizr Deployment view cookbook",
      "locator": "Environment and instance mapping",
      "revision": "Mutable official documentation inspected 2026-11-07"
    },
    {
      "url": "https://docs.structurizr.com/dsl/parser",
      "title": "Structurizr DSL parser",
      "locator": "Local/export versus browser feature support",
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
    "diagram-c4-runtime-scenario",
    "diagram-arc42-consistent-views"
  ]
}
---

# Structurizr DSL: share a model across selected views

## When to use

Use when several maintained views should refer to the same system vocabulary, or a team's independently drawn pictures keep diverging. It can be a better fit than duplicating element declarations in unrelated diagram files; a one-off sketch may not justify a model/toolchain.

## What to inspect

The DSL separates model elements/relationships from views. Dynamic views show ordered instances of static relationships with scenario-specific wording; deployment views map software instances into a named environment. Explicit identifiers support reuse; generated view keys are not guaranteed stable. Implied relationships can appear through configured rules rather than explicit model lines.

Inspect the parser feature matrix: browser environments differ from local/export contexts for includes, documentation, plugins and scripts. Rendering/export styles can lose information across formats. The same text therefore does not guarantee identical output in every tool route.

## Diagram implications

Keep element identity, abstraction and environment consistent. Review an implied edge's actual derivation before describing it as a separately observed dependency. Give durable views explicit keys if manual layout must survive. Check exported artifacts for loss of meaning, especially if a style or icon carries an essential distinction.

## What to borrow and adapt

Model a small core of known relationships, then select the views that support current decisions. Add source/revision and proposed/observed status to the surrounding evidence record. A shared authored model can improve consistency without becoming an authoritative discovery system for the running infrastructure.

## Mismatches and limits

A valid DSL does not prove deployment truth, complete contracts or correct failure handling. Includes, scripts, plugins and publication routes can read or execute beyond a simple diagram; selecting this resource does not authorize those effects. No parser, renderer, export, hosted workspace or script was run. The initial guessed cookbook identifier path was unavailable; the linked official Identifiers page was used instead.
