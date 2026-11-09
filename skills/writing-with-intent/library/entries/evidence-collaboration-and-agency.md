---
{
  "id": "evidence-collaboration-and-agency",
  "kind": "study",
  "title": "Inspect the collaboration process instead of counting final words alone",
  "summary": "CoAuthor provides interaction traces for asking who steers a writing session.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "frame",
      "revise",
      "preserve-voice",
      "evaluate"
    ],
    "genres": [
      "essay",
      "argument",
      "article"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "human-agency",
      "collaborative-writing",
      "interaction-traces"
    ]
  },
  "sources": [
    {
      "url": "https://cs.stanford.edu/~minalee/pdf/chi2022-coauthor.pdf",
      "title": "CoAuthor: Designing a Human-AI Collaborative Writing Dataset for Exploring Language Model Capabilities — Lee, Liang and Yang",
      "locator": "§§4.2–4.3; §§5.1.3–5.2; §§6.1–6.2",
      "revision": "CHI 2022 author-hosted paper, doi:10.1145/3491102.3502030"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Fresh reading of task/interface design, curation, collaboration measures, ownership correlations and authors' causal limits; no dataset download or replay claim."
  },
  "reuse": "Original annotations and links only; no upstream prose, poems, datasets or study materials redistributed.",
  "related": [
    "evidence-creativity-and-diversity",
    "evidence-cultural-context"
  ]
}
---

## When to use

Use when an author feels that a draft is polished but no longer theirs. Ask which decisions they want to own: angle, examples, wording, structure or final judgment.

## What to inspect

CoAuthor records 1,445 creative and argumentative English sessions from 63 crowd workers with four GPT-3 instances/configurations. Writers could request suggestions, accept, dismiss and edit them. The paper distinguishes interaction measures from final-text shares. Ownership correlated with human-written share; these are observational relationships within the dataset, not a randomized ownership intervention.

## What to borrow and adapt

Our application: agree on the assistant's role, invite the writer's own material, and leave consequential choices visible. If the author rejects an option, preserve the reason for the next revision. When reviewing an existing draft, ask about intent and decisions rather than assuming that a percentage of human words captures agency.

## Mismatches and limits

Short prompted crowd-worker sessions are not a professional author's long-term practice. Requirements encouraged collaboration, and model/settings/interface affect behavior. The paper explicitly says interventions are needed to test causal hypotheses. More editing, more human words, more accepted suggestions or greater satisfaction alone cannot certify a better collaboration.

