---
{
  "id": "tool-penpot",
  "kind": "tool",
  "title": "Penpot: explicit prototype boards, triggers and flows",
  "summary": "A design/prototyping environment with documented board connections, overlay actions and multiple flow starting points.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "prototype",
      "compare",
      "plan"
    ],
    "contexts": [
      "design-system",
      "collaboration",
      "flows"
    ],
    "platforms": [
      "web",
      "cross-platform"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://help.penpot.app/user-guide/prototyping-testing/prototyping/",
      "title": "Penpot prototyping",
      "locator": "Connect boards; interaction triggers/actions; flow starting points",
      "revision": "live documentation inspected 2026-11-07"
    },
    {
      "url": "https://penpot.app/features",
      "title": "Penpot features",
      "locator": "Design/prototyping; flex/grid layout; collaboration",
      "revision": "live documentation inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Official prototyping guide and feature documentation inspected; no prototype viewed or interacted with."
  },
  "reuse": "Original annotation and links only. No upstream software, screenshots, templates or proprietary assets redistributed.",
  "related": [
    "tool-excalidraw",
    "tool-ui-sh-picker"
  ]
}
---

# Penpot: explicit prototype boards, triggers and flows

## When to use

Select Penpot when the person needs an editable visual prototype to discuss screen relationships, navigation or alternate starting points before committing to production behavior. It can support a collaborative artifact where rearranging and comparing screens is easier than discussing abstract style labels.

## What to inspect

Read board connections, triggers/actions and flows in the current guide. Identify the task’s actual entry point and relevant error/recovery branches before wiring screens. Check whether an overlay, previous-screen action or separate flow reflects the intended model.

## What to borrow and adapt

Borrow explicit representation of an interaction: origin, trigger, action and destination. Include meaningful alternate paths rather than only a presentation tour. A first-time signup and an existing member’s return can have distinct start points while sharing components and brand. Keep the prototype’s fidelity and missing behavior clear to the human reviewer.

## Mismatches and limits

A connected board can mimic navigation without implementing validation, persistence, permissions or responsive behavior. A prototype is therefore not proof of a working service. Sharing links, uploading assets, creating teams or installing/self-hosting the software are separate actions. The public guide was read, but no Penpot file, prototype interaction or account was opened in this curation.
