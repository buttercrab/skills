---
{
  "id": "evidence-entity-coherence",
  "kind": "study",
  "title": "Check whether supported facts describe the same subject",
  "summary": "D-FActScore exposes a paragraph-level error that isolated fact checks can miss.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "verify",
      "revise",
      "evaluate"
    ],
    "genres": [
      "article",
      "research-summary",
      "explanation"
    ],
    "languages": [
      "english"
    ],
    "contexts": [
      "entity-ambiguity",
      "factual-verification",
      "paragraph-coherence"
    ]
  },
  "sources": [
    {
      "url": "https://aclanthology.org/2024.findings-acl.160.pdf",
      "title": "Merging Facts, Crafting Fallacies: Evaluating the Contradictory Nature of Aggregated Factual Claims in Long-Form Generations — Chiang and Lee",
      "locator": "§§3–4.3, Table 3; Limitations",
      "revision": "Findings of ACL 2024, pp. 2734–2751"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "empirical"
    ],
    "inspected_at": "2026-11-08",
    "freshness": "versioned",
    "scope": "Fresh reading of entity ambiguity examples, grouping definition, human annotation procedure, 300-paragraph results and scope limitations; no model rerun."
  },
  "reuse": "Original annotations and links only; no upstream prose, poems, datasets or study materials redistributed.",
  "related": [
    "evidence-claim-verification",
    "craft-unc-paragraph-development"
  ]
}
---

## When to use

Use when several individually sourced details form a biography, company profile or account of an event. Ask whether every detail refers to the same person, entity, time period and setting.

## What to inspect

The study examines biographies with ambiguous names. Human annotation covers 300 paragraphs from ChatGPT, Llama-13b-chat and Tulu-v2-13b-dpo. Facts can be individually supported by Wikipedia yet produce a misleading combined biography by mixing people. D-FActScore groups facts as a reader would associate them and verifies each group against one linked entity.

## What to borrow and adapt

Our application: after checking individual claims, make a second pass through the paragraph's referents. Follow each pronoun, name, date and organizational relationship back to its source. If two entities share a name, introduce enough distinction before using either person's achievements as evidence. Apply the same question to merged studies with different populations.

## Mismatches and limits

The demonstrated metric failure is entity ambiguity in biography generation using Wikipedia, not every kind of misleading argument. Extending the check to studies, companies or timelines is our editorial analogy, not a tested intervention. Human grouping and automated extraction can themselves err. A higher disambiguation score does not establish completeness, fairness or readable prose.

