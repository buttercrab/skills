---
{
  "id": "system-spectrum",
  "kind": "system",
  "title": "Adobe Spectrum: creative-product ecosystem routing",
  "summary": "A route into Adobe-oriented foundations and current implementation families, with explicit version/access gaps.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compose",
      "operate",
      "inspect"
    ],
    "contexts": [
      "creative-tool",
      "professional-product",
      "design-system"
    ],
    "platforms": [
      "web"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://spectrum.adobe.com/",
      "title": "Spectrum",
      "locator": "System overview; React/Web Components status; iOS/Android availability routes",
      "revision": "live documentation; not pinned to a source commit"
    },
    {
      "url": "https://spectrum.adobe.com/web/rsp/components/accordion",
      "title": "Accordion component route",
      "locator": "Anatomy/options/states/behaviors/usage navigation only",
      "revision": "Current routed documentation; implementation not pinned"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Landing-page ecosystem and status text inspected; current accordion wrapper navigation inspected, embedded guidance partial. No component behavior or visual appearance evaluated."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-carbon",
    "system-apple-hig"
  ]
}
---

# Adobe Spectrum: creative-product ecosystem routing

## When to use

Consider Spectrum when a professional or creative tool needs a shared product language and the team wants to examine Adobe’s system organization. Ask about working density, tool expertise, input devices and which implementation family is viable.

## What to inspect

The inspected landing page distinguishes React and Web Components areas and their beta status, while native routes were marked coming soon. Follow the exact current route and check readiness before implementation. The inspected accordion wrapper exposes several guidance sections, but its embedded usage material was only partially readable through this research tool.

## What to borrow and adapt

Borrow an investigation plan: map a creative task to controls, inspect states and behaviors, and compare the resulting composition with the local product’s input and content needs. For a media inspector, examine whether disclosure and grouping help the real adjustment task; do not infer that the Adobe association alone makes a pattern suitable. Use current implementation docs to resolve the question.

## Mismatches and limits

This card is curated as an ecosystem-routing reference, not a component recommendation or a visual match. An older action-group URL returned 404 and no action-group guidance is represented here. No Spectrum component was executed or visually inspected. The source’s implementation and accessibility claims still require exact-version and application testing. Readiness differs by platform; do not generalize web availability to native libraries.
