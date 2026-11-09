---
{
  "id": "pattern-apple-onboarding",
  "kind": "system",
  "title": "Apple HIG: contextual onboarding",
  "summary": "Choose optional introduction, safe interactive teaching or contextual tips according to the actual learning need.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "start",
      "learn",
      "configure"
    ],
    "contexts": [
      "consumer-app",
      "first-use",
      "creative-tool"
    ],
    "platforms": [
      "ios",
      "ipados",
      "macos",
      "watchos",
      "tvos",
      "visionos",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://developer.apple.com/design/human-interface-guidelines/onboarding",
      "title": "Onboarding",
      "locator": "Best practices; tutorials; tips; setup and permissions",
      "revision": "Visible change log: 2024-06-10 clarification; 2023-06-21 visionOS"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Onboarding text inspected in native Chrome; source-described learning paths only; no native tutorial or permission interaction."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "system-apple-hig",
    "pattern-carbon-empty-states"
  ],
  "flow_evidence": [
    {
      "url": "https://developer.apple.com/design/human-interface-guidelines/onboarding",
      "locator": "Tutorials and contextual learning",
      "sequence": [
        "Launch into useful experience",
        "Offer skippable teaching when needed or show contextual help at relevant feature",
        "Try a safe task",
        "Continue independently; find help again later"
      ],
      "method": "Native Chrome accessibility-tree reading of maintainer guidance; sequence synthesized from documented options, not one executed app."
    }
  ]
}
---

# Apple HIG: contextual onboarding

## When to use

Use when people need help reaching a first useful outcome in a native app. Ask what they already understand, what can be learned safely through use, which setup is essential, and what can wait until the relevant feature is requested.

## What to inspect

Read the distinctions among a brief introduction, interactive tutorial and contextual help. The guidance favors optional, focused learning and postponing nonessential setup. It differentiates permissions required for the initial experience from permissions that can be requested later in context.

## What to borrow and adapt

Borrow a sequence organized around a person doing something meaningful. A drawing app could let someone make a harmless first mark, show the related tool tip, and leave help discoverable later. If a tutorial exists, define its skip path and how it can be found again. Track progress toward the user outcome rather than equating completion of slides with understanding.

## Mismatches and limits

This is maintainer guidance, not a comparative study of onboarding conversion. A regulated or safety-critical tool may require mandatory training whose conditions must be established separately. Native Chrome inspection read the text and saw an introductory illustration; it did not exercise a native tutorial or permission prompt. No claim about a particular app’s retention, accessibility or visual character follows.
