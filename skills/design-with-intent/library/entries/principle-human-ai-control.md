---
{
  "id": "principle-human-ai-control",
  "kind": "foundation",
  "title": "Design understandable, correctable AI behavior",
  "summary": "Use the Human–AI Interaction guidelines to examine expectations, dismissal, correction and adaptation in AI features, with their original evaluation limits intact.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "interaction-design",
      "evaluate",
      "correct"
    ],
    "contexts": [
      "human-ai",
      "uncertainty",
      "automation"
    ],
    "platforms": [
      "cross-platform"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf",
      "title": "Guidelines for Human-AI Interaction",
      "locator": "Table 1; development/validation sections; Discussion and Future Work",
      "revision": "Amershi et al., CHI 2019; DOI 10.1145/3290605.3300233"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Original guideline synthesis and practitioner-evaluation paper refreshed. Relevance/clarity evaluation is not causal proof of end-user improvement or generative-agent coverage."
  },
  "reuse": "Original annotation and links to original material; no paper, illustrations or third-party software redistributed. Check source-specific terms before substantial reproduction.",
  "related": [
    "principle-mixed-initiative",
    "principle-contextual-permissions",
    "principle-informed-choice"
  ]
}
---

# Design understandable, correctable AI behavior

## When to use

Use for an interface that predicts, recommends, generates or acts with uncertainty, especially when a person needs to correct a result or understand changing behavior.

## What to inspect

Read the guideline groups across first encounter, normal use, mistakes and longer-term adaptation. Inspect the validation method and domain gaps before adopting the paper's broad phrasing as evidence that every guideline applies identically.

## What to borrow and adapt

Make capabilities and likely limits intelligible at the point they matter. Provide efficient dismissal, correction and control. Explain a consequential change without requiring a person to reverse-engineer it, and preserve their ability to recover when automation guesses poorly.

For a suggested meeting plan, distinguish a proposal from a committed booking and make edits local and inspectable. If the system learns from a correction, explain the scope of that adaptation rather than silently changing unrelated work.

## Mismatches and limits

The paper predates contemporary generative-agent workflows. Its practitioner assessment does not prove a numerical productivity or trust benefit for this application. More explanation is not always better, and an explanation does not make a bad action correct. A checklist cannot replace a task/failure model, domain requirements, meaningful user control or actual evaluation.
