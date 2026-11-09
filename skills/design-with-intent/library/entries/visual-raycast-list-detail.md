---
{
  "id": "visual-raycast-list-detail",
  "kind": "example",
  "title": "Raycast: compact list and preview within a desktop metaphor",
  "summary": "An embedded launcher example pairs a searchable result list with a detail preview and action cues in one compact surface.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "find",
      "inspect",
      "choose"
    ],
    "contexts": [
      "expert-work",
      "desktop-tools",
      "repeated-use"
    ],
    "platforms": [
      "web",
      "desktop",
      "macos"
    ],
    "character": [
      "compact",
      "dark",
      "product-led",
      "desktop-metaphor"
    ]
  },
  "sources": [
    {
      "url": "https://www.raycast.com/",
      "title": "Raycast primary public page",
      "locator": "Take shortcuts, not detours section; clipboard-history product scene",
      "revision": "not-versioned; live page inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "visual-inspected",
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "live-at-inspection",
    "scope": "Own native Chrome public HTTPS tab; desktop screenshot viewed directly. Public composition only; no account/product workflow or efficacy tested."
  },
  "visual_evidence": [
    {
      "url": "https://www.raycast.com/",
      "locator": "Take shortcuts, not detours section; clipboard-history product scene",
      "observed": "A desktop-framed scene shows a left list of clipboard entries, a selected color with a larger right preview and metadata, a top filter, and bottom action/keyboard cues.",
      "method": "CUA Chrome screenshot viewed directly on 2026-11-07; approximately 1552px-wide desktop viewport."
    }
  ],
  "reuse": "Source links and original annotations only. No third-party images, fonts, logos, source packages or media redistributed; asset reuse rights not established.",
  "related": [
    "visual-linear-product-proof",
    "visual-poolsuite-retro-player",
    "flow-figma-ui3-state-visibility"
  ]
}
---

# Raycast: compact list and preview within a desktop metaphor

## When to use

Use when people repeatedly find an item and need to inspect it without losing their place in a result list. The reference is particularly useful for a compact command or object-selection surface.

## What to inspect

Inspect the clipboard-history scene below the opening headline. Compare the row selection, right-side preview, metadata and bottom action hints. This is an embedded product representation; no clipboard content or launcher installation was accessed.

## What to borrow and adapt

Borrow the relationship between list, selected object and relevant next action. A snippet chooser or asset picker can preserve scanning context while showing enough detail to disambiguate a choice. Adapt the preview to the object: an image, document, command and person require different information.

Decide whether keyboard cues help the actual audience. The composition is a useful contrast to a full-page overview or a series of large browsing cards. It does not require a dark theme or a global command palette.

## Mismatches and limits

The image does not prove selection speed, keyboard behavior, platform integration or accessibility. A compact desktop surface may fail on touch or narrow displays. Avoid copying product imagery, shortcuts or system-looking controls without implementing their behavior. No downloads or app actions were performed.

## Related resource roles

- [flow-figma-ui3-state-visibility](flow-figma-ui3-state-visibility.md): Compare repeated state inspection and detail access; the visual example alone does not establish task frequency.
