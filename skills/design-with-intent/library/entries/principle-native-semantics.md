---
{
  "id": "principle-native-semantics",
  "kind": "foundation",
  "title": "Semantics are promises about behavior",
  "summary": "Use APG to understand custom-control obligations and accessible names, while preferring suitable native behavior and testing relevant browser/assistive-technology combinations.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "components",
      "accessibility",
      "implement",
      "evaluate"
    ],
    "contexts": [
      "keyboard",
      "custom-widgets",
      "assistive-technology"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/WAI/ARIA/apg/about/introduction/",
      "title": "APG Introduction",
      "locator": "APG is Not a Normative Standard; Exercise Caution If Deviating; APG is not a UI Design System",
      "revision": "Live APG introduction inspected 2026-11-07"
    },
    {
      "url": "https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/",
      "title": "APG Read Me First",
      "locator": "A role is a promise; browser/assistive-technology support; mobile/touch limits",
      "revision": "Live APG guidance accessed 2026-11-07"
    },
    {
      "url": "https://www.w3.org/WAI/ARIA/apg/patterns/button/",
      "title": "APG Button Pattern",
      "locator": "Keyboard interaction; roles/states/properties; toggle-label alternatives",
      "revision": "Live pattern accessed 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "APG Introduction, Read Me First and button pattern inspected, not executed. Informative patterns illustrate permitted variations; they are not a production-ready design system or universal compatibility guarantees."
  },
  "reuse": "Original annotation and primary-source links only; no standard text, paper, figures or third-party assets redistributed. Preserve W3C/author source-specific terms for substantial reproduction.",
  "related": [
    "standard-focus-motion"
  ]
}
---

# Semantics are promises about behavior

## When to use

Use when a design introduces a custom button, menu, tab or other widget, or when a code rubric demands attributes and keyboard handlers without examining the actual element.

## What to inspect

Read the APG Introduction's scope and variation cautions before copying a pattern, then Read Me First and the relevant control's keyboard, name, role and state model. The button pattern also distinguishes a stable-label toggle from a label-changing command.

## What to borrow and adapt

Start with semantics appropriate to the operation. A native button already supplies behaviors that a styled generic element does not. If a custom role is necessary, implement and verify its promised interactions and focus management. Choose an accessible name from content or an appropriate relationship rather than requiring one attribute everywhere.

For a Save action, decide whether it is a stateful toggle or an action whose label changes. Preserve that model consistently for visual and assistive-technology users.

## Mismatches and limits

ARIA changes exposed semantics; it does not automatically add keyboard behavior or styling. Adding a role or label can also override useful native information. APG is informative, has no conformance model, and is not a comprehensive design system or production-ready component library. Its examples illustrate choices; variation still needs consistency with relevant specifications, practices and established keyboard conventions. APG notes mobile/touch and compatibility limits, so example code is not blanket production acceptance or a standalone conformance audit.
