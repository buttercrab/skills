---
{
  "id": "pattern-uswds-language",
  "kind": "system",
  "title": "USWDS: language access by translation coverage",
  "summary": "Choose equivalent-page switching or selected-content access according to what is actually translated.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "choose-language",
      "navigate",
      "understand"
    ],
    "contexts": [
      "multilingual",
      "public-service",
      "partial-translation"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://designsystem.digital.gov/patterns/select-a-language/",
      "title": "Select a language",
      "locator": "Two languages; three or more; selected content; preferred-language routes",
      "revision": "live documentation; not pinned to a source commit"
    },
    {
      "url": "https://designsystem.digital.gov/patterns/select-a-language/three-or-more-languages/",
      "title": "Three or more languages",
      "locator": "When to use; guidance; accessibility; latest updates",
      "revision": "Published 2022-11-14; preview-link update 2024-04-11; live page read"
    },
    {
      "url": "https://designsystem.digital.gov/patterns/select-a-language/selected-content/",
      "title": "Selected multilingual content",
      "locator": "When to use; coverage distinction; meaningful destination and menu guidance",
      "revision": "live documentation; not pinned to a source commit"
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
    "system-uswds",
    "system-govuk",
    "principle-multilingual-layout",
    "visual-toss-language-composition"
  ],
  "flow_evidence": [
    {
      "url": "https://designsystem.digital.gov/patterns/select-a-language/three-or-more-languages/",
      "locator": "Guidance: equivalent destination; selected-content alternative",
      "sequence": [
        "Locate language control",
        "Choose desired language",
        "Reach equivalent meaningful content when available",
        "For partial coverage, use explicitly labeled translated-content destination"
      ],
      "method": "Maintainer documentation sequence read as text; not executed."
    }
  ]
}
---

# USWDS: language access by translation coverage

## When to use

Use when people must find content in a language they can use. Ask exactly which pages and tasks are translated, whether a language choice should switch the current page or reveal a collection, and who maintains translation parity.

## What to inspect

Read the complete-coverage and selected-content branches together. The multi-language pattern points to an equivalent page; the partial-coverage pattern exposes a distinct route to available translated material. Both address placement, native language names, right-to-left layout, and avoiding misleading country flags or automatic redirection.

## What to borrow and adapt

Borrow a truthful coverage model. A library site with fully translated account flows can offer equivalent-page switching, while additional translated guides can live behind an explicitly labeled content route. Specify what happens when the current item lacks a translation. Include document-language metadata and real usable destinations; the visible selector alone does not create language access.

## Mismatches and limits

This is a source-described transition, not a tested translation or selector. Exact wording and placement reflect the system and need local comprehension checks. Region, currency and communication preference are different choices and may require separate controls. A preference stored for future messages should not silently imply that all current content is translated. No demo link, language switch or right-to-left rendering was executed here.

## Related resource roles

- [principle-multilingual-layout](principle-multilingual-layout.md): Selection controls and localized layout/script behavior need separate evidence.
- [visual-toss-language-composition](visual-toss-language-composition.md): A narrow observed public language switch provides a comparison, not full accessibility or localization acceptance.
