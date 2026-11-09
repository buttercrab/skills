---
{
  "id": "example-momentum-revision-reader-questions",
  "kind": "example",
  "title": "Momentum revision: expose the unanswered questions and model boundary",
  "summary": "Use a real source diff to inspect structural revision beyond sentence polish.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "revise",
      "explain",
      "structure"
    ],
    "genres": [
      "explanation",
      "article"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "mathematical-models",
      "revision-artifacts"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/distillpub/post--momentum/commit/c4077ce909583530b9066cd136ba70bad17592cf",
      "title": "Distill — Why Momentum Really Works source revision",
      "locator": "public/index.html hunks around 183–205 and 1692–1725; active prose distinguished from HTML comments",
      "revision": "c4077ce909583530b9066cd136ba70bad17592cf versus parent 21f9e0b9d95ecdef2422003f1e5297af9f2fd2af; 2017-04-02"
    },
    {
      "url": "https://distill.pub/2017/momentum/",
      "title": "Gabriel Goh — Why Momentum Really Works",
      "locator": "Published opening, through first model introduction",
      "revision": "Published 2017-04-04; inspected 2026-11-08"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Actual pinned before/after patch read; published opening inspected, not whole article or interactive behavior."
  },
  "reuse": "Original craft analysis and links only. Do not redistribute the article or imitate the author’s distinctive voice.",
  "related": [
    "craft-gopen-swan-information-order",
    "craft-wisconsin-reverse-outline"
  ]
}
---

## When to use

When a technical introduction offers a familiar analogy without making the need for a new explanation clear.

## What to inspect

The pinned introduction and stochastic-gradient hunks; compare active paragraphs, not commented alternatives. Also compare the published opening at the linked article.

## Craft trace

Reader question: what does the analogy fail to predict? The diff adds concrete unanswered questions and a stated route through a simpler model. A later hunk explains an existing simplifying noise assumption more explicitly. These are visible textual changes, not inferred editorial motives.

## Revision implications

Our proposed transfer: add the question the reader could not answer with their current model, then state the replacement model’s limits. Keep an assumption adjacent to the result that depends on it.

## What to borrow and adapt

Inspect revision by function: motivation, bridge, assumption, consequence. Keep a compact decision log of why a proposed change serves this reader.

## Mismatches and limits

The patch does not prove comprehension improved or identify who requested each edit. Formula correctness and widgets were not tested. This selected revision is not a summary of the complete article.

