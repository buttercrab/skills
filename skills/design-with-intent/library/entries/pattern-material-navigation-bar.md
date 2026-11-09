---
{
  "id": "pattern-material-navigation-bar",
  "kind": "system",
  "title": "Material 3: primary navigation bar",
  "summary": "Stable top-level destinations for compact and medium layouts, with important implementation and version caveats.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "navigate",
      "switch"
    ],
    "contexts": [
      "consumer-app",
      "primary-navigation"
    ],
    "platforms": [
      "android",
      "flutter",
      "mobile-web",
      "web",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://m3.material.io/components/navigation-bar/overview",
      "title": "Navigation bar overview",
      "locator": "Usage; M3 Expressive update; availability; example navigation",
      "revision": "Live page; M3 Expressive update May 2025; baseline identified as no longer recommended"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "visual-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Native Chrome overview text and static news-app illustration inspected; no working application navigation exercised."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "pattern-apg-tabs",
    "system-apple-hig",
    "skill-android-adaptive"
  ],
  "visual_evidence": [
    {
      "url": "https://m3.material.io/components/navigation-bar/overview",
      "locator": "Overview hero: phone news screen and bottom navigation",
      "observed": "Four labeled icon destinations are shown; For you has a selected pill around its star icon.",
      "method": "Public HTTPS page screenshot and accessibility tree viewed in native Chrome through CUA."
    }
  ]
}
---

# Material 3: primary navigation bar

## When to use

Consider this when a consumer application has a small stable set of peer destinations. Ask which places people revisit, what state should survive a switch, and how compact and wider windows change the navigation surface.

## What to inspect

Read destination count, stable placement, selected-state treatment and the current Expressive guidance together. The inspected page describes three to five peer destinations. It marks the older baseline as no longer recommended and lists web implementations as unavailable; confirm the target implementation before recommending a package.

## What to borrow and adapt

Borrow persistent orientation across views. For a reading app, distinguish Library, Discover and Saved as destinations and preserve useful per-destination position where appropriate. The viewed news example uses labeled icons and a pill-like selected indicator. Adapt the shape, motion and typography to the chosen brand and platform instead of treating the screenshot as a complete style specification.

## Mismatches and limits

A workflow stepper, transient command menu and within-page tabs solve different problems. Compare APG tabs when panels share a page rather than serving as primary app destinations. The example was visually inspected in native Chrome; no destination switching, back-stack behavior or accessibility interaction was tested. Android/Flutter availability does not establish web support, and May 2025 guidance is a source snapshot requiring refresh.

## Related resource roles

- [skill-android-adaptive](skill-android-adaptive.md): An implementation resource with its own SDK and experimental-API boundaries; platform resemblance is not compatibility evidence.
