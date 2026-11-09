---
{
  "id": "standard-wcag-conformance",
  "kind": "foundation",
  "title": "WCAG 2.2: define the accessibility claim",
  "summary": "Use the versioned normative standard to identify applicable success criteria, level, process scope and evidence before claiming accessibility conformance.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "evaluate",
      "accessibility",
      "requirements"
    ],
    "contexts": [
      "web-accessibility",
      "complete-process",
      "conformance"
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
      "title": "Web Content Accessibility Guidelines 2.2",
      "locator": "Introduction; Conformance Requirements 5.2.1–5.2.5; full-pages responsive-variation Note 3; Conformance Claims",
      "revision": "W3C Recommendation, 12 December 2024"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Versioned normative standard and conformance sections inspected. No application audit or assistive-technology testing performed."
  },
  "reuse": "Original annotation and link to W3C standard; no standard text or examples redistributed. Follow the source's W3C terms for substantial reproduction.",
  "related": [
    "standard-text-adaptation",
    "standard-focus-motion",
    "principle-native-semantics"
  ]
}
---

# WCAG conformance scope

## When to use

Use when a design brief includes an accessibility target, a review needs clear acceptance criteria, or a team is about to describe an interface as compliant. Start here before extracting a few convenient color or focus rules.

## What to inspect

Read the normative criterion and its level, then the conformance requirements concerning complete pages, complete processes, accessibility-supported technologies and non-interference. Level AA includes all Level A and AA criteria, or the specified conforming-alternate-version route. Full-page scope includes automatically presented responsive variations; each must conform or have the required conforming alternate. Use Understanding documents for explanation while preserving their distinction from the standard.

## What to borrow and adapt

Create a scoped requirement/evidence map for the actual journey. A booking flow can span choice, correction, confirmation and cancellation; testing only its opening card does not establish the process. State which version, level, pages, responsive variations, states and technologies were assessed and what remains unobserved.

Apply checks relevant to the chosen target without turning an example technique into the only permitted implementation. Preserve the person's brand and task goals while finding a conforming design.

## Mismatches and limits

WCAG conformance is not a universal score for usability, attractiveness or every disability-related need. A validator output or screenshot does not establish complete-process conformance. This card is not legal advice, a certification or evidence that any cataloged product conforms. A current project may have additional platform, contractual or user requirements.
