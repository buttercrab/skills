---
{
  "id": "practice-write-good",
  "kind": "tool",
  "title": "write-good: make heuristic flags contestable",
  "summary": "Use narrow English wording checks as suggestions while preserving purposeful passive voice, rhythm and qualification.",
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
      "essay",
      "tutorial"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "optional-tool",
      "heuristics",
      "voice"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/btford/write-good/blob/6940b034c6f5a7e101c01a24d651a778fc3fe435/README.md",
      "title": "write-good README",
      "locator": "API, CLI, Checks, Extensions and installation examples",
      "revision": "6940b034c6f5a7e101c01a24d651a778fc3fe435"
    },
    {
      "url": "https://github.com/btford/write-good/blob/6940b034c6f5a7e101c01a24d651a778fc3fe435/package.json",
      "title": "write-good package manifest",
      "locator": "Scripts, dependencies and CLI bin declarations",
      "revision": "6940b034c6f5a7e101c01a24d651a778fc3fe435"
    },
    {
      "url": "https://github.com/btford/write-good/blob/6940b034c6f5a7e101c01a24d651a778fc3fe435/bin/write-good.js",
      "title": "write-good CLI source",
      "locator": "Default checks, E-Prime opt-in and custom module loading, lines 1–160",
      "revision": "6940b034c6f5a7e101c01a24d651a778fc3fe435"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Read README, manifest and selected CLI source; no dependency inspection, install, test, lint or remote-shell command executed."
  },
  "reuse": "Original annotations and links only; no copied passages, full-article paraphrase, or style-cloning instructions.",
  "related": [
    "practice-vale",
    "craft-google-passive-exceptions"
  ]
}
---

# write-good: make heuristic flags contestable

## When to use
A writer wants prompts about repeated wording patterns in an English draft, without making a style checker the editor.

## What to inspect
The tool describes itself as a naive English linter. Checks are configurable; E-Prime is opt-in. The CLI can load custom checks as Node modules. The manifest's development lint script uses a fixing flag, and its test task invokes that lint script before tests.

## What to borrow and adapt
Choose a few checks and assess each alert against intended emphasis. Passive voice can keep attention on the known event when the actor is irrelevant or unknown. Adverbs can carry necessary precision or voice. Keep a rationale for intentional exceptions rather than optimizing the alert count.

## Mismatches and limits
Flags establish neither grammatical error nor poor writing, factual accuracy or machine authorship. Default checks do not establish Korean support; uninspected third-party extensions add separate behavior. Global installation modifies the tool environment; on-demand execution can obtain a package; custom checks execute module code. Upstream tests are not a harmless prose review because their lint step may edit repository files. Nothing was run here; this is not a dependency/security audit or an instruction to install.
