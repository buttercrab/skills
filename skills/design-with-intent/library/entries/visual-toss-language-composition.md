---
{
  "id": "visual-toss-language-composition",
  "kind": "example",
  "title": "Toss: one photographic identity across English and Korean",
  "summary": "A public language switch exposes how large English and Hangul headlines occupy the same photographic brand composition.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "explain",
      "localize",
      "choose-direction"
    ],
    "contexts": [
      "consumer",
      "localization",
      "financial-product-marketing"
    ],
    "platforms": [
      "web"
    ],
    "character": [
      "photographic",
      "large-type",
      "restrained"
    ]
  },
  "sources": [
    {
      "url": "https://toss.im/",
      "title": "Toss primary public page",
      "locator": "Public desktop hero in English and Korean; visible ENG/KOR language navigation",
      "revision": "not-versioned; live page inspected 2026-11-07"
    },
    {
      "url": "https://toss.im/en-us",
      "title": "Toss English public website",
      "locator": "English hero and ENG language menu",
      "revision": "not-versioned; live page inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "visual-inspected",
      "source-inspected",
      "interaction-tested"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "English and Korean public hero screenshots viewed. Visible ENG menu opened and KOR selected; title and URL changed to Korean. No financial feature, download, account or transaction was used."
  },
  "visual_evidence": [
    {
      "url": "https://toss.im/",
      "locator": "Public desktop hero in English and Korean; visible ENG/KOR language navigation",
      "observed": "A rounded photographic hero and restrained top navigation support large bottom-aligned text; English forms a sentence while Korean distributes a short Hangul statement across the width.",
      "method": "CUA Chrome screenshot viewed directly on 2026-11-07; approximately 1552px-wide desktop viewport."
    }
  ],
  "reuse": "Source links and original annotations only. No third-party images, fonts, logos, source packages or media redistributed; asset reuse rights not established.",
  "related": [
    "visual-headspace-service-branches",
    "visual-things-task-hierarchy",
    "principle-multilingual-layout",
    "pattern-uswds-language"
  ],
  "flow_evidence": [
    {
      "url": "https://toss.im/",
      "locator": "Public language selector in header",
      "sequence": [
        "English public page",
        "Open ENG choices",
        "Choose KOR",
        "Korean title and URL"
      ],
      "method": "Actual native Chrome public navigation; no form submission/account change."
    }
  ],
  "interaction_evidence": [
    {
      "url": "https://toss.im/",
      "actions": [
        "Open visible ENG language menu",
        "Choose KOR"
      ],
      "observed": "Page title changed from Toss to 토스; URL changed from /en-us to /; Korean navigation and headline displayed.",
      "method": "CUA documented click and fresh AX state followed by screenshot, 2026-11-07."
    }
  ]
}
---

# Toss: one photographic identity across English and Korean

## When to use

Use when a visual direction must survive different scripts and language lengths. It supplies a concrete comparison rather than assuming Latin line breaks, tracking and headline proportions transfer unchanged.

## What to inspect

Inspect both public language versions and the photographic hero. The initial visit redirected to the English URL; choosing the visible Korean option returned the Korean page. Compare the hierarchy and placement of the headline, not merely a translated string.

## What to borrow and adapt

Borrow the separation between stable identity and language-specific composition. Preserve the intended image/content relationship while allowing script, wrapping and spacing to differ. For a multilingual community site, real local-language text should shape the layout early.

Ask native readers about meaning and naturalness where those judgments matter. The public language control shows a narrow navigation behavior; it does not establish that every locale has identical content or features.

## Mismatches and limits

No app, banking operation, financial claim, accessibility conformance or mobile layout was evaluated. The page's product promises are not recommendations here. A large photographic hero can compete with urgent working information. The card does not supply photography, typography assets or a universal Korean visual style.

## Related resource roles

- [principle-multilingual-layout](principle-multilingual-layout.md): Use language/layout guidance when adapting the viewed composition; the observed language switch does not establish a localized end-to-end journey.
- [pattern-uswds-language](pattern-uswds-language.md): Compare a documented language-selection pattern with the narrowly observed public switch.
