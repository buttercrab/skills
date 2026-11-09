---
{
  "id": "flow-duolingo-guided-path",
  "kind": "example",
  "title": "Duolingo: guided progression with review and migration",
  "summary": "A historical learning-path case for deciding how recommended next steps coexist with review, progress transfer and learner choice.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "learn",
      "progress",
      "review",
      "return"
    ],
    "contexts": [
      "learning",
      "consumer",
      "first-use"
    ],
    "platforms": [
      "native-mobile"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://blog.duolingo.com/new-duolingo-home-screen-design/",
      "title": "Introducing the new Duolingo learning path",
      "locator": "Quick overview; learning-path explanation; progress-transfer and return-to-lesson FAQs",
      "revision": "2022 launch account; source inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "documented-flow",
      "visual-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Relevant first-party documented sequence/state account inspected; no authenticated live product workflow exercised."
  },
  "flow_evidence": [
    {
      "url": "https://blog.duolingo.com/new-duolingo-home-screen-design/",
      "locator": "Quick overview; learning-path explanation; progress-transfer and return-to-lesson FAQs",
      "sequence": [
        "Follow recommended next lesson",
        "Complete or revisit levels",
        "Use guidebooks/practice",
        "Return to current position after scrolling"
      ],
      "method": "First-party documentation read; sequence summarizes its described states, not an interaction test."
    }
  ],
  "reuse": "Original annotation and source links only. No upstream assets or instructions redistributed; page-specific reuse rights not established.",
  "related": [
    "flow-discord-community-onboarding"
  ],
  "visual_evidence": [
    {
      "url": "https://blog.duolingo.com/new-duolingo-home-screen-design/",
      "locator": "Quick overview before/after tree and path image",
      "observed": "Historical screenshots contrast a branching grid of skill icons with a vertically progressing path and an explicit Start marker.",
      "method": "Own Chrome HTTPS tab; screenshot visually inspected using CUA on 2026-11-07."
    }
  ]
}
---

# Duolingo: guided progression with review and migration

## When to use

Use for a course, guided onboarding curriculum or practice product where novices struggle to choose the next useful step. It also helps examine the cost of replacing a familiar navigational model.

## What to inspect

Read the historical progression and review explanations, then the migration FAQ. Inspect the before/after image and distinguish what it shows from the claims made about learning. The page announces a 2022 rollout; it is not a current app specification.

## What to borrow and adapt

Preserve an explicit next action while designing return, review and orientation routes. For a local learning club, a recommended introductory sequence could coexist with a searchable session library. Ask whether the person needs guidance, known-item retrieval or free exploration before enforcing one path. Account for existing progress when changing the model.

## Mismatches and limits

The published comparison images and described states were inspected, but no lesson was opened or completed. The article is product-team rationale; navigation, practice and content changed together, so it cannot isolate a layout effect or prove linear progression universally better. Compare Discord onboarding when users should shape their own initial destinations.
