---
{
  "id": "practice-proselint",
  "kind": "tool",
  "title": "proselint: select English usage checks without erasing uncertainty",
  "summary": "Treat configurable English usage findings as optional revision questions, especially when rules conflict with the evidence.",
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
      "research-summary"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "optional-tool",
      "usage",
      "house-style"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/amperser/proselint/blob/dbed789caae662d06c7c8a5a13dd31f1acd36f5c/README.md",
      "title": "proselint README",
      "locator": "Installation, Usage, Configuring, Check selection, Per-file checks and beginning of Checks table (lines 1–340)",
      "revision": "dbed789caae662d06c7c8a5a13dd31f1acd36f5c"
    },
    {
      "url": "https://github.com/amperser/proselint/blob/dbed789caae662d06c7c8a5a13dd31f1acd36f5c/pyproject.toml",
      "title": "proselint project metadata",
      "locator": "Python requirement, dependencies, entry point, build backend and development tasks",
      "revision": "dbed789caae662d06c7c8a5a13dd31f1acd36f5c"
    },
    {
      "url": "https://github.com/amperser/proselint/blob/dbed789caae662d06c7c8a5a13dd31f1acd36f5c/.pre-commit-hooks.yaml",
      "title": "proselint pre-commit declaration",
      "locator": "Python hook, file types and check argument",
      "revision": "dbed789caae662d06c7c8a5a13dd31f1acd36f5c"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Inspected metadata and documentation, not full checker implementation or dependencies. No installation, hook setup or lint run."
  },
  "reuse": "Original annotations and links only; no copied passages, full-article paraphrase, or style-cloning instructions.",
  "related": [
    "practice-vale",
    "practice-write-good"
  ]
}
---

# proselint: select English usage checks without erasing uncertainty

## When to use
An English draft needs a selective pass for recurring usage or typography issues after argument and evidence review.

## What to inspect
The pinned README documents per-file check selection and a first-found configuration search. Its table includes a hedging check; that is a reason to inspect policy fit, not to delete uncertainty. Project metadata requires Python 3.10 or later and declares dependencies, a PDM build backend, and a CLI entry point. The hook invokes checking for several text formats.

## What to borrow and adapt
Name the revision question before selecting checks. Exempt quotations, intentional voice and scientifically necessary qualifications when appropriate. Record why a rule is disabled. Review contextual accuracy independently; a cleaner sentence can still misstate the source.

## Mismatches and limits
This is an English prose linter, not a Korean editor, fact checker, plagiarism judge or quality score. No local behavior was measured. Package installation changes the Python environment and installs dependencies; adding a hook changes future commit-time behavior. Development formatting tasks are separate from prose checking. This card authorizes none of those actions and supplies no execution recipe. A dependency/security audit was not performed.
