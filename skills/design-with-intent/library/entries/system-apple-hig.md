---
{
  "id": "system-apple-hig",
  "kind": "system",
  "title": "Apple Human Interface Guidelines",
  "summary": "Platform and pattern routing for Apple experiences; inspected through the onboarding guidance, not a whole-system audit.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "start",
      "navigate",
      "learn"
    ],
    "contexts": [
      "native-app",
      "consumer-app",
      "platform-conventions"
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
      "url": "https://developer.apple.com/design/human-interface-guidelines/",
      "title": "Human Interface Guidelines",
      "locator": "Platform and topic navigation; route to onboarding",
      "revision": "live documentation; not pinned to a source commit"
    },
    {
      "url": "https://developer.apple.com/design/human-interface-guidelines/onboarding",
      "title": "Onboarding",
      "locator": "Best practices; tutorials; setup and permissions; change log",
      "revision": "Live guidance; visible change-log entries 2024-06-10 and 2023-06-21"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Source text inspected; no visual inspection or live component execution."
  },
  "reuse": "Original annotation and source links only. No third-party code, fonts, brand assets or screenshots redistributed. License and asset-specific reuse terms were not verified; inspect the applicable upstream terms before copying.",
  "related": [
    "pattern-apple-onboarding",
    "pattern-material-navigation-bar"
  ]
}
---

# Apple Human Interface Guidelines

## When to use

Use when the experience belongs on an Apple platform and platform behavior matters to recognition, input or system integration. Ask which platforms, window sizes, assistive technologies and system surfaces are actually in scope.

## What to inspect

Use the platform and topic navigation to find the relevant guidance, then inspect a specific pattern and its implementation documentation. This review read the onboarding body and navigation in native Chrome. It did not inspect every foundation, component or platform-specific chapter.

## What to borrow and adapt

Borrow platform-aware questions before choosing a layout: what does the operating system already teach, which system control should carry an action, and where can learning occur in context? For a small creative utility, examine whether direct manipulation with lightweight help would teach better than a prerequisite presentation. Use the companion onboarding card as a focused starting point.

## Mismatches and limits

HIG is guidance for Apple ecosystems, not a complete web design system or an implementation library. A native-looking control does not prove native behavior. Cross-platform products may require shared product concepts with different platform presentations. The source was readable in native Chrome after the text extractor returned a JavaScript shell; no native application was launched and no full visual identity was evaluated.
