---
{
  "id": "system-fluent2",
  "kind": "system",
  "title": "Fluent 2",
  "summary": "Microsoft-oriented design/development system with explicit web and native platform routes.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "navigate",
      "operate",
      "compose"
    ],
    "contexts": [
      "enterprise",
      "productivity",
      "cross-platform"
    ],
    "platforms": [
      "web",
      "ios",
      "android",
      "windows",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://fluent2.microsoft.design/",
      "title": "Fluent 2",
      "locator": "Overview; platform routes; design and development tools",
      "revision": "live documentation; not pinned to a source commit"
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
    "pattern-fluent-dialog",
    "system-carbon"
  ]
}
---

# Fluent 2

## When to use

Use when a productivity product needs to align with Microsoft ecosystem conventions or when comparing systems with web and native implementation routes. Ask which platform library the project actually uses and what consistency must mean across those platforms.

## What to inspect

Inspect the platform route before selecting a component. The homepage separates web, iOS, Android and Windows resources and connects design and development tooling. Read the individual component guidance, status and implementation instead of assuming a single API spans every platform.

## What to borrow and adapt

Borrow the practice of carrying a product’s intent across platform-specific components. For an internal approval tool, define the decision, required information and recovery path first, then choose the supported dialog or page pattern for each client. Document which tokens and interaction expectations remain shared and which follow the host platform.

## Mismatches and limits

Fluent’s ecosystem fit can be valuable without making its house style universally appropriate. A branded editorial experience or a specialist creative canvas may need different references. Homepage inspection did not verify visual assets, library runtime behavior or accessibility across platforms. The companion dialog card examines one web React guideline; it does not establish that other implementations have identical dismissal and focus behavior.
