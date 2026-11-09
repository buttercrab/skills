---
{
  "id": "pattern-fluent-dialog",
  "kind": "system",
  "title": "Fluent 2: dialog interruption and focus",
  "summary": "Choose modal, nonmodal and alert interruptions by consequence, then specify dismissal and focus.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "confirm",
      "edit",
      "interrupt",
      "recover"
    ],
    "contexts": [
      "enterprise",
      "productivity",
      "consequential-action"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://fluent2.microsoft.design/components/web/react/core/dialog/usage",
      "title": "Dialog usage",
      "locator": "Types; behavior; dismissal; accessibility; form and scrolling guidance",
      "revision": "Web React core dialog; preview status at inspection"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-fluent2",
    "pattern-radix-dialog"
  ],
  "flow_evidence": [
    {
      "url": "https://fluent2.microsoft.design/components/web/react/core/dialog/usage",
      "locator": "Behavior and accessibility",
      "sequence": [
        "Activate dialog trigger",
        "Move focus into dialog; contain focus for modal type",
        "Act or dismiss by supported means",
        "Restore focus to trigger or appropriate continuation"
      ],
      "method": "Maintainer documentation sequence read as text; not executed."
    }
  ]
}
---

# Fluent 2: dialog interruption and focus

## When to use

Use when an action may justify interrupting the current task. Ask whether the person must decide now, whether background interaction should remain available, and what happens to unfinished input on dismissal.

## What to inspect

Read modal, nonmodal and alert distinctions alongside alternatives such as a toast or popover. Inspect focus entry, modal containment, restoration, scrolling content and the guidance against nested dialogs. Check the preview status and actual installed implementation before treating every behavior as stable.

## What to borrow and adapt

Borrow a written interruption contract. For a destructive project action, state the consequence, offer clear action labels, define Escape and outside-click behavior, and return focus to a meaningful place afterward. For a lengthy form, decide whether a full page would provide better navigation and recovery. Keep a dialog’s purpose and the underlying transaction separate.

## Mismatches and limits

The inspected page describes a React web component, not a guarantee for all Fluent libraries. Exact initial-focus choices require content-aware accessibility review; a complex dialog can need a different starting target than a small form. No live dialog was opened here. Compare the tested Radix demo for a narrow interaction receipt, while retaining Fluent’s own implementation contract if that is the chosen stack.
