---
{
  "id": "principle-mixed-initiative",
  "kind": "foundation",
  "title": "Mixed initiative: ask, act, and preserve human control",
  "summary": "Choose when clarification or automation helps by examining consequential uncertainty, interruption cost, correction, and the person's ability to redirect the work.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "frame",
      "clarify",
      "collaborate"
    ],
    "contexts": [
      "human-ai",
      "creative-direction",
      "uncertain-intent"
    ],
    "platforms": [
      "cross-platform"
    ],
    "character": []
  },
  "sources": [
    {
      "url": "https://erichorvitz.com/chi99horvitz.pdf",
      "title": "Principles of Mixed-Initiative User Interfaces",
      "locator": "pp.1–2, principles 2–11; LookOut account",
      "revision": "CHI 1999; DOI 10.1145/302979.303030"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Original principles/prototype paper inspected; relevant dialogue, control, refinement and memory sections refreshed. No new experiment or current agent trial."
  },
  "reuse": "Original selection annotation with a link to author-hosted paper; no paper text, diagrams or software redistributed. Recheck terms before substantial reuse.",
  "related": [
    "principle-contextual-elicitation",
    "principle-grounding-feedback",
    "principle-human-ai-control"
  ]
}
---

# Mixed initiative

## When to use

Use when an agent could either interrupt for direction or make a provisional decision: a vague design request, an ambiguous critique, a delegated exploration, or a high-cost action. This is a decision framework, not a visual reference.

## What to inspect

Read principles 5–11 together: dialogue, direct invocation/termination, costly guesses, precision under uncertainty, refinement and interaction history. The LookOut example supplies context for what those principles meant; the numbered list alone can sound more universal than the paper establishes.

## What to borrow and adapt

Identify the choice whose answer could change the result, whether the person can answer it, and the consequence of guessing. Ask about that choice while continuing independent work. Preserve settled answers and let the person reject, narrow or terminate a proposal.

For example, a community site may need a question about first-event confidence before a global direction is chosen. A person explicitly delegating typography has already answered who should make that choice. Treat those situations differently.

## Mismatches and limits

The paper presents principles and a historical scheduling prototype; it does not prove an optimal number of questions or a modern agent interview policy. It also does not imply that software should guess irreversible product facts, or that every uncertain implementation detail belongs to the person. Adapt the interruption/recovery tradeoff to the actual task and available controls.
