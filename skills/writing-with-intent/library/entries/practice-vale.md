---
{
  "id": "practice-vale",
  "kind": "tool",
  "title": "Vale: make an agreed style selective and reviewable",
  "summary": "Inspect configuration, selected styles and script rules before using lint alerts as editorial prompts.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "revise",
      "evaluate",
      "preserve-voice"
    ],
    "genres": [
      "article",
      "tutorial",
      "explanation"
    ],
    "languages": [
      "english",
      "korean"
    ],
    "contexts": [
      "optional-tool",
      "house-style",
      "multilingual"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/vale-cli/vale/blob/66bbb85a1a78a5b5497331e04d4033357caced4d/README.md",
      "title": "Vale README",
      "locator": "Install; Quickstart; Styles; Why Vale",
      "revision": "66bbb85a1a78a5b5497331e04d4033357caced4d"
    },
    {
      "url": "https://docs.vale.sh/topics/.vale.ini",
      "title": "Vale configuration reference",
      "locator": "Core settings; sections/rules; search and layering",
      "revision": "Live docs inspected 2026-11-08; may differ from pinned binary"
    },
    {
      "url": "https://docs.vale.sh/keys/packages",
      "title": "Vale Packages",
      "locator": "Naming a package and sync install destination",
      "revision": "Live docs inspected 2026-11-08"
    },
    {
      "url": "https://docs.vale.sh/checks/script",
      "title": "Vale script extension",
      "locator": "Tengo script example and scope execution",
      "revision": "Live docs inspected 2026-11-08"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Read README and documented config/install/script effects only. No binary, package, sync, script or lint command installed/executed; no complete upstream security audit."
  },
  "reuse": "Original annotations and links only; no copied passages, full-article paraphrase, or style-cloning instructions.",
  "related": [
    "practice-proselint",
    "craft-google-passive-exceptions"
  ]
}
---

# Vale: make an agreed style selective and reviewable

## When to use
A team has agreed terminology or document conventions worth checking repeatedly.

## What to inspect
Resolve project and user configuration, file globs, language-appropriate styles and exclusions. Inspect each package before adoption: synchronization downloads or copies assets into the configured styles directory; rules can include Tengo scripts compiled and run for their scope. Readability or sentence-length thresholds express a selected policy.

## What to borrow and adapt
Start with a small advisory rule set and document intentional exceptions. Check each alert against audience, genre and evidence. Keep valid uncertainty even if a style dislikes hedging. Separate Korean files and rules deliberately; configuring a tokenizer does not validate Korean grammar. Freeze versions for reproducible team use and review rule changes.

## Mismatches and limits
Alerts are not truth checks, proof of quality, accessibility acceptance, or authorship detection. No performance or local compatibility was tested. Installation changes the tool environment; sync writes style assets and can fetch remote archives. No commands are being recommended for automatic execution. Built-in offline operation is not a guarantee about arbitrary extensions or downloaded packages. Do not auto-apply every available fix.
