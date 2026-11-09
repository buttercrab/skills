---
{
  "id": "skill-android-adaptive",
  "kind": "skill",
  "title": "Android adaptive Compose: layouts across form factors",
  "summary": "Google-authored operational guidance for adaptive navigation, panes, input, foldable posture and state preservation, with explicit migration prerequisites.",
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
      "android",
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://github.com/android/skills/blob/bf68e2d66a992a1e6aeb7e9263293cc23fcbf475/jetpack-compose/adaptive/SKILL.md",
      "title": "jetpack-compose/adaptive/SKILL.md",
      "locator": "Prerequisites; eight-step workflow; experimental API warnings; screenshot baseline instructions; foldable-tabletop.md",
      "revision": "bf68e2d66a992a1e6aeb7e9263293cc23fcbf475"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Full pinned entrypoint and foldable-tabletop.md inspected; root Apache 2.0 license opening inspected. No build, migration, screenshot or device test."
  },
  "reuse": "Root LICENSE.txt identifies Apache 2.0; original annotation/source links only. Inspect individual referenced material and dependencies before reuse.",
  "related": [
    "skill-swiftui-expert",
    "tool-playwright",
    "pattern-material-navigation-bar"
  ]
}
---

# Android adaptive Compose: layouts across form factors

## When to use

Choose this for an existing Compose application that needs coherent phone, tablet, foldable or desktop behavior. Its strongest design question is which content and controls belong together as available space, posture and input change; wider screens should not merely stretch the phone view.

## What to inspect

Read prerequisites first: the workflow expects Compose throughout and Navigation 3. Then inspect the relevant pane, state, desktop-input or tabletop reference. The pinned entrypoint includes experimental Grid, FlexBox and MediaQuery guidance; verify the precise dependencies and supported versions before adopting examples. The tabletop reference distinguishes rearranging identical content from layouts requiring different controls.

## What to borrow and adapt

Borrow the inventory of list/detail relationships, the preservation of input, selection, navigation, scroll and playback state, and the demand to inspect multiple form factors. Ask which content benefits from simultaneous viewing and whether keyboard or pointer use changes the interaction. Follow actual hinge geometry and local coordinates when controls need to avoid a fold.

## Mismatches and limits

The source contains strong migration prescriptions, experimental API adoption and screenshot-test setup. Those are project decisions, not automatic consequences of choosing this reference. It also contains conflicting baseline directions: an earlier step records new references while the final step says not to update references before user review. Preserve diffs for review and resolve that conflict explicitly. No Android build, screenshot test, device interaction or generated layout was verified here.

## Related resource roles

- [pattern-material-navigation-bar](pattern-material-navigation-bar.md): For a bottom-navigation decision, compare the documented platform pattern while checking adaptive API and SDK compatibility separately.
