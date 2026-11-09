---
{
  "id": "pattern-radix-dialog",
  "kind": "system",
  "title": "Radix: dialog composition and Escape return",
  "summary": "A bounded live receipt for opening and dismissing a demo modal, plus implementation anatomy.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "edit",
      "dismiss",
      "compose"
    ],
    "contexts": [
      "custom-design-system",
      "modal-form"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.radix-ui.com/primitives/docs/components/dialog",
      "title": "Dialog",
      "locator": "Demo; anatomy; features; API; keyboard interactions; controlled async example",
      "revision": "Component version 1.2.0 displayed at inspection"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow",
      "visual-inspected",
      "interaction-tested"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "API documentation read; public demo opened, initial field focus observed, Escape dismissal and trigger-focus return observed in native Chrome. No edit, Save or persistence test."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-radix",
    "pattern-fluent-dialog",
    "standard-focus-motion",
    "tool-axe-core"
  ],
  "visual_evidence": [
    {
      "url": "https://www.radix-ui.com/primitives/docs/components/dialog",
      "locator": "Public Edit profile demo in open state",
      "observed": "Centered title/description panel, labeled Name and Username fields, close control and Save button over a darkened background.",
      "method": "Native Chrome screenshot viewed through CUA after opening public demo."
    }
  ],
  "flow_evidence": [
    {
      "url": "https://www.radix-ui.com/primitives/docs/components/dialog",
      "locator": "Public demo",
      "sequence": [
        "Activate Edit profile",
        "Dialog opens and Name field receives focus",
        "Press Escape",
        "Dialog closes and Edit profile trigger regains focus"
      ],
      "method": "Actual public demo interaction through native Chrome CUA; accessibility tree and screenshot inspected."
    }
  ],
  "interaction_evidence": [
    {
      "url": "https://www.radix-ui.com/primitives/docs/components/dialog",
      "actions": [
        "Clicked public Edit profile demo trigger",
        "Pressed Escape while Name field was focused"
      ],
      "observed": "Dialog opened, Name was focused; after Escape dialog disappeared and Edit profile trigger was focused. No fields edited or Save action invoked.",
      "method": "Native Chrome public HTTPS tab controlled using CUA, with state snapshots after actions."
    }
  ]
}
---

# Radix: dialog composition and Escape return

## When to use

Use when evaluating a custom-styled React modal or checking whether a proposed wrapper preserves the primitive’s basic interaction. Ask about dismissal, unsaved input, asynchronous completion and where focus should continue.

## What to inspect

Read Root, Trigger, Portal, Overlay, Content, Title, Description and Close together with the focus and dismissal hooks. Inspect controlled state when completion depends on an asynchronous result. The public demo was opened and dismissed: Name received focus, and Escape closed the dialog with focus back on Edit profile.

## What to borrow and adapt

Borrow the explicit composition contract and verify it after applying local styling. For an account editor, connect the title and description, label fields, state how cancellation treats edits, and close only at the chosen transaction outcome. Test keyboard navigation, error reporting, zoom and background interaction in the composed application. An API example is a starting hypothesis for that test.

## Mismatches and limits

The demo’s Save button was not activated; no values were changed and no persistence or network outcome was tested. The receipt covers one open/Escape cycle, not a focus-trap audit or screen-reader conformance. The viewed centered panel and dim overlay are example styling rather than mandatory Radix visual design. A long or complex workflow may deserve a page instead.

## Related resource roles

- [standard-focus-motion](standard-focus-motion.md): A narrowly exercised dialog receipt and broader focus/motion requirements answer different verification questions.
- [tool-axe-core](tool-axe-core.md): Use automated checks only for relevant implemented states, with manual/native evidence where required.
