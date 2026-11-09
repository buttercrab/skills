---
{
  "id": "principle-multilingual-layout",
  "kind": "foundation",
  "title": "Adapt layout to script, direction and content",
  "summary": "Use semantic direction and script-specific layout guidance to preserve hierarchy and reading order across RTL, Hangul and mixed text instead of reproducing Latin line breaks.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "localize",
      "typography",
      "responsive-design"
    ],
    "contexts": [
      "rtl",
      "hangul",
      "mixed-script",
      "internationalization"
    ],
    "platforms": [
      "web",
      "mobile-web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/International/questions/qa-html-dir",
      "title": "Structural markup and right-to-left text in HTML",
      "locator": "Quick answer; base direction; forms; tables",
      "revision": "Live W3C guidance accessed 2026-11-07"
    },
    {
      "url": "https://www.w3.org/TR/2026/DNOTE-klreq-20260321/",
      "title": "Requirements for Hangul Text Layout and Typography",
      "locator": "Status; section 4.1 fonts; section 7.1 line breaking and restrictions",
      "revision": "W3C Group Note Draft, 21 March 2026"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Official explanatory RTL guidance and versioned Hangul draft inspected. Draft status and unfinished sections preserved; no native-reader or browser conformance test."
  },
  "reuse": "Original annotation and primary-source links only; no standard text, paper, figures or third-party assets redistributed. Preserve W3C/author source-specific terms for substantial reproduction.",
  "related": [
    "principle-global-name-fields",
    "standard-text-adaptation"
  ]
}
---

# Adapt layout to script, direction and content

## When to use

Use when a direction relies on uppercase labels, tight tracking, manual line breaks, fixed Latin-width columns or hardcoded left/right positioning and must work in another script.

## What to inspect

Read base direction separately from language tagging, and distinguish structural layout from inline bidirectional content. In the Hangul document, inspect the draft status before using its font metrics, breaking or punctuation discussions.

## What to borrow and adapt

Preserve intended relationships and prominence while letting actual strings shape the layout. Use semantic direction and logical positioning where appropriate. Test mixed identifiers, numbers, punctuation, fallback fonts, long labels and localized errors.

A comparison card may retain its hierarchy while changing wrapping and alignment. Matching the English screenshot's line count is less important than readable grouping and correct order.

## Mismatches and limits

The Hangul publication is a Group Note Draft, not an endorsed Recommendation, and some sections remain unfinished. Language and direction are different properties; a blanket mirrored screenshot can mishandle icons, numbers or mixed text. These sources do not replace native-reader review or establish a single typographic style for all speakers of a language.
