---
{
  "id": "evidence-detector-bias",
  "kind": "study",
  "title": "Treat detector scores as uncertain signals, never authorship verdicts",
  "summary": "Historical detector tests reveal population bias and sensitivity to surface language changes.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "evaluate",
      "preserve-voice"
    ],
    "genres": [
      "essay",
      "article",
      "research-summary"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "authorship-claims",
      "english-as-additional-language",
      "evaluation-bias"
    ]
  },
  "sources": [
    {
      "url": "https://arxiv.org/html/2304.02819v3",
      "title": "GPT detectors are biased against non-native English writers — Liang and colleagues",
      "locator": "Results: TOEFL versus US essays and rewriting sensitivity; Discussion: limitations; Materials and Methods (historical access/model/corpus limits)",
      "revision": "arXiv:2304.02819v3, July 2023"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Fresh reading of sample provenance, seven-detector comparisons, rewriting sensitivity and stated limitations; no current detector evaluation or evasion experiment."
  },
  "reuse": "Original annotations and links only; no upstream prose, poems, datasets or study materials redistributed.",
  "related": [
    "evidence-poetry-readers-and-labels",
    "practice-ap-ai-source-accountability"
  ]
}
---

## When to use

Use when someone calls writing AI-generated because it is predictable, polished or simple. Clarify whether the real concern is unsupported claims, blandness, undisclosed assistance, or suspected misconduct.

## What to inspect

Seven historical detectors were compared on 91 human TOEFL essays from a Chinese educational forum and 88 US eighth-grade essays from another dataset. False positives were markedly higher for the TOEFL set; language transformations changed detector outcomes. These are nonmatched populations and materials, not a clean causal estimate of nationality or language proficiency.

## What to borrow and adapt

Our application: diagnose concrete reader problems directly. Show an unsupported sentence, repeated idea, missing example or unclear inference, and suggest a revision tied to that defect. When provenance matters, seek relevant process evidence with appropriate authorization rather than infer it from prose texture.

## Mismatches and limits

Small historical corpora and mostly older detector architectures cannot establish present-day rankings or a universal false-positive rate. Dataset differences complicate causal interpretation. The paper's rewriting tests show instability; they are not instructions to disguise authorship. Neither a positive nor a negative detector score proves who wrote a passage.

