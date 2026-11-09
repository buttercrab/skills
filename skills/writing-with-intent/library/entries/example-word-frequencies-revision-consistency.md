---
{
  "id": "example-word-frequencies-revision-consistency",
  "kind": "example",
  "title": "Word-frequency tutorial revision: propagate a prerequisite correction",
  "summary": "Treat runnable examples and their data assumptions as part of explanatory writing.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "revise",
      "explain",
      "verify"
    ],
    "genres": [
      "tutorial",
      "explanation"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "revision-artifacts",
      "code-examples"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/programminghistorian/jekyll/commit/3aef10a619b0a20f4b9ee5ab8110c371c710b8f2",
      "title": "Programming Historian — Counting Word Frequencies with Python revision",
      "locator": "en/lessons/counting-frequencies.md two diff hunks at old lines 254 and 376; surrounding integration instructions",
      "revision": "3aef10a619b0a20f4b9ee5ab8110c371c710b8f2 versus parent 30ee8a59e8a66eca851ae5402d1b80e5f192058c; 2021-11-17"
    },
    {
      "url": "https://github.com/programminghistorian/jekyll/blob/3aef10a619b0a20f4b9ee5ab8110c371c710b8f2/en/lessons/counting-frequencies.md",
      "title": "Pinned revised lesson source",
      "locator": "Lesson Goals; source lines 226–275 and 346–397 around the two integrated examples",
      "revision": "3aef10a619b0a20f4b9ee5ab8110c371c710b8f2"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Pinned patch and surrounding source passages read; complete lesson and runtime not tested."
  },
  "reuse": "Original craft analysis and links only. Do not redistribute the article or imitate the author’s distinctive voice.",
  "related": [
    "craft-diataxis-reader-purpose",
    "practice-ori-technical-paraphrase"
  ]
}
---

## When to use

When an explanation has repeated complete examples that depend on the same input representation.

## What to inspect

The two affected integration examples and their preceding instructions, not only the commit message.

## Craft trace

Reader question: how do these earlier pieces combine into a complete program? The inspected patch adds an explicit decoding step at both input boundaries before text processing. The matching changes are observable; successful execution is not established by the diff.

## Revision implications

Our proposed transfer: inventory every complete example and identify shared prerequisites. When one changes, update each dependent example and explain the relevant representation at its first use. Decide separately what runtime verification is needed.

## What to borrow and adapt

Borrow propagation discipline: a revision to an assumption may require several passages, snippets and expected outputs to stay consistent.

## Mismatches and limits

This is a technical tutorial revision, not evidence of a prose-style improvement or current compatibility. Old tools and remote inputs may have changed. No upstream program was executed and no completion claim rests on this patch alone.

