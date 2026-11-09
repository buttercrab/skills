---
{
  "id": "standard-focus-motion",
  "kind": "foundation",
  "title": "Focus and motion: preserve control across interaction changes",
  "summary": "Distinguish visible focus, stronger focus appearance, automatic motion and interaction-triggered animation, retaining each criterion's conformance level and exceptions.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "accessibility",
      "interaction-design",
      "motion",
      "evaluate"
    ],
    "contexts": [
      "keyboard",
      "reduced-motion",
      "state-changes"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/TR/2024/REC-WCAG22-20241212/",
      "title": "WCAG 2.2",
      "locator": "SC 2.4.7, 2.4.13, 2.2.2 and 2.3.3",
      "revision": "Recommendation 12 December 2024"
    },
    {
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html",
      "title": "Understanding Focus Visible",
      "locator": "SC and mode-of-operation explanation",
      "revision": "Level AA; accessed 2026-11-07"
    },
    {
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html",
      "title": "Understanding Focus Appearance",
      "locator": "SC; minimum area; contrast; exceptions",
      "revision": "Level AAA; accessed 2026-11-07"
    },
    {
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html",
      "title": "Understanding Animation from Interactions",
      "locator": "SC; essential exception; relation to automatic movement",
      "revision": "Level AAA; accessed 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Normative and informative clauses inspected. No keyboard, vestibular-accessibility or browser compatibility test performed."
  },
  "reuse": "Original annotation and primary-source links only; no standard text, paper, figures or third-party assets redistributed. Preserve W3C/author source-specific terms for substantial reproduction.",
  "related": [
    "standard-wcag-conformance",
    "principle-native-semantics"
  ]
}
---

# Focus and motion: preserve control across interaction changes

## When to use

Use when designing animated navigation, expanding content, dialogs, drag feedback or focus treatments that accompany state changes.

## What to inspect

Compare AA Focus Visible with AAA Focus Appearance rather than merging them. For motion, distinguish automatically moving content from nonessential interaction-triggered animation and preserve essential-motion exceptions. Read the criterion's actual scope before choosing a technique.

## What to borrow and adapt

Keep the current interaction point perceivable, preserve meaningful focus after changes, and offer an appropriate reduced-motion experience without losing state or functionality. A reduced transition should still communicate completion and keep controls available.

For a row expansion, the selected object and newly exposed content should remain understandable with less movement. A decorative entrance sequence should not hide essential content indefinitely when animation is disabled or interrupted.

## Mismatches and limits

The two-pixel-perimeter equivalent is an area condition, not one mandatory outline style. AAA criteria are not automatically AA requirements, although a project may choose stronger behavior. Disabling all animations can break poorly coupled state callbacks; verify the resulting operation. This card does not certify accessible motion or replace platform/user research.
