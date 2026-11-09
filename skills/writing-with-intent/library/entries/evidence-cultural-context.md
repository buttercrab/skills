---
{
  "id": "evidence-cultural-context",
  "kind": "study",
  "title": "Check which cultural details an assistant replaces",
  "summary": "A cross-cultural autocomplete experiment makes cultural context an explicit editing question.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "frame",
      "revise",
      "preserve-voice"
    ],
    "genres": [
      "essay",
      "article",
      "personal-essay"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "cross-cultural-writing",
      "english-as-additional-language",
      "autocomplete"
    ]
  },
  "sources": [
    {
      "url": "https://arxiv.org/html/2409.11360v3",
      "title": "AI Suggestions Homogenize Writing Toward Western Styles and Diminish Cultural Nuances — Agarwal, Naaman and Vashistha",
      "locator": "§§3–3.5 design and measures; §§4.2–4.4 findings; §5.4 limitations",
      "revision": "arXiv:2409.11360v3, 12 March 2025; CHI 2025"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Fresh reading of assignment, nationality-based cohorts, embedding/classifier analyses, cultural examples, authors' suggested mitigation and limitations; no rerun."
  },
  "reuse": "Original annotations and links only; no upstream prose, poems, datasets or study materials redistributed.",
  "related": [
    "practice-korean-public-language",
    "evidence-creativity-and-diversity"
  ]
}
---

## When to use

Use when a rewrite makes locally specific writing sound broadly familiar. Ask the author which language variety, cultural references, family terms or social assumptions should survive the edit.

## What to inspect

The between-subjects study included 118 participants: 60 Indian and 58 American, writing culturally grounded English tasks with or without GPT-4o inline suggestions. Group-level embedding and classification analyses found convergence, stronger toward American patterns for Indian writing. The paper also examines cultural examples and grammar-correction alternatives.

## What to borrow and adapt

Our application: make a small preservation list from the user's actual text. Review proposed substitutions against it and ask about unfamiliar details rather than normalizing them automatically. Let the user decide whether explanation, translation, or deliberate unfamiliarity serves their reader. Keep a rejected substitution when it reveals a recurring assumption.

## Mismatches and limits

Nationality proxies do not represent a whole culture; the authors acknowledge subcultures and small samples. Group comparisons cannot reconstruct what an individual would have written unaided. Other languages, models and interfaces remain separate questions. Personalized examples and added friction are proposed mitigations, not demonstrated cures.

