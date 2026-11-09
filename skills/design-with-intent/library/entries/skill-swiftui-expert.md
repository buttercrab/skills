---
{
  "id": "skill-swiftui-expert",
  "kind": "skill",
  "title": "SwiftUI expert: native layout and state review",
  "summary": "A native Apple implementation router covering layout proposals, state ownership, identity, accessibility, API migrations and measured performance.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "implement",
      "adapt",
      "verify"
    ],
    "contexts": [
      "native-app",
      "adaptive-layout",
      "components"
    ],
    "platforms": [
      "ios",
      "macos",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/AvdLee/SwiftUI-Agent-Skill/blob/62bd760f005093d1e2e4de5db156e456a5f96400/skills/swiftui-expert-skill/SKILL.md",
      "title": "skills/swiftui-expert-skill/SKILL.md",
      "locator": "Workflow; reference router; layout-best-practices.md relative layout, context-agnostic views and safe areas",
      "revision": "62bd760f005093d1e2e4de5db156e456a5f96400"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Pinned entrypoint and first 125 lines of layout-best-practices.md inspected; MIT license inspected. No simulator, profiling or API compilation performed."
  },
  "reuse": "Repository LICENSE inspected as MIT. Original annotation only; validate copied examples and dependencies independently.",
  "related": [
    "skill-android-adaptive",
    "skill-vercel-react-performance",
    "system-apple-hig"
  ]
}
---

# SwiftUI expert: native layout and state review

## When to use

Choose this when a SwiftUI design must become a resilient native interface, or when a view breaks during resizing, navigation or changing text. It helps connect a proposed design to state ownership and platform layout behavior; it does not supply a brand or research the audience.

## What to inspect

Read the router and the topic-specific reference before applying a change. The inspected layout reference emphasizes the size offered to the view, local environment values, safe-area ownership and preservation of identity. Match its API advice to the project deployment target and SDK; the pinned source includes emerging platform-version claims that this curation did not independently verify.

## What to borrow and adapt

Borrow the distinction between a decision about available space and a decision about device capability. Check how a card behaves in a sheet, a split window and a full screen, rather than assuming a device-sized frame. Preserve navigation and reading state through layout changes. The entrypoint avoids imposing an architecture such as MVVM and restricts Liquid Glass adoption to explicit requests.

## Mismatches and limits

This is a large implementation knowledge router, not evidence that a resulting app is usable or visually successful. Profiling and recording paths can invoke scripts and processes; selection is not authorization to run them. Do not mechanically turn every fixed dimension into a percentage or every suggestion into a performance requirement. Inspect relevant references and actual runtime behavior before claiming acceptance.

## Related resource roles

- [system-apple-hig](system-apple-hig.md): Connect the implementation method to native interaction guidance and the actual supported system version.
