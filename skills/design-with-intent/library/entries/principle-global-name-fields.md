---
{
  "id": "principle-global-name-fields",
  "kind": "foundation",
  "title": "Design name fields for actual naming practices",
  "summary": "Use W3C internationalization guidance to question assumed name components, ordering and validation before imposing a local naming model on a global audience.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "forms",
      "data-modeling",
      "localize",
      "content-design"
    ],
    "contexts": [
      "personal-names",
      "internationalization",
      "identity"
    ],
    "platforms": [
      "web",
      "mobile-web",
      "cross-platform"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.w3.org/International/questions/qa-personal-names",
      "title": "Personal names around the world",
      "locator": "Scenarios; examples of differences; implications for field design",
      "revision": "Live W3C internationalization guidance accessed 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Original explanatory scenarios and field-design implications inspected. Not an exhaustive cultural survey or empirical comparison of this product's forms."
  },
  "reuse": "Original annotation and primary-source links only; no standard text, paper, figures or third-party assets redistributed. Preserve W3C/author source-specific terms for substantial reproduction.",
  "related": [
    "principle-multilingual-layout"
  ]
}
---

# Design name fields for actual naming practices

## When to use

Use when designing registration, event attendance, shipping, account display or another flow that collects or displays people's names across locales.

## What to inspect

Read the scenarios as well as the examples. Distinguish a single-language form used globally from a localized form, and inspect why the application needs each component. The source explicitly warns that naming practices vary within cultures.

## What to borrow and adapt

Collect only the structure the actual task needs. Preserve characters and meaningful ordering, avoid inferring address forms from a presumed Western first/last split, and let people correct how their name is displayed.

For a local club signup, a display name may be enough. A regulated record may have different requirements. Separate those use cases instead of imposing the most elaborate structure on everyone.

## Mismatches and limits

There is no perfect universal field arrangement in this introductory guidance. Do not turn its examples into a closed list of allowed cultures, infer a person's preferred address from nationality, or equate accepting Unicode with complete localization. Security, identity verification and legal record requirements need their own owning sources. This is design/data-model guidance, not evidence that a particular product is culturally inclusive.
