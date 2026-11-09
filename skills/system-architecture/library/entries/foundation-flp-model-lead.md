---
{
  "id": "foundation-flp-model-lead",
  "kind": "foundation",
  "title": "FLP original proof: model inspection remains a prerequisite",
  "summary": "An original consensus impossibility lead whose deeper model/proof could not be freshly inspected.",
  "status": "candidate",
  "availability": "partial",
  "facets": {
    "tasks": [
      "compare",
      "model-failure"
    ],
    "contexts": [
      "consensus",
      "asynchrony"
    ],
    "qualities": [
      "availability",
      "correctness"
    ],
    "scale": [
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf",
      "title": "Fischer, Lynch and Paterson: Impossibility of Distributed Consensus with One Faulty Process",
      "locator": "First page/abstract freshly retrieved; detailed model/proof follow-ups unavailable",
      "revision": "JACM32(2), 1985; original author/institution PDF"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "partial"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh opening/abstract only; original model/proof requests and technical-report follow-up repeatedly timed out. Candidate lead, not full-paper inspection."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-cap-model",
    "system-raft-host-integration"
  ]
}
---

# FLP original proof: model inspection remains a prerequisite

## When to use

Treat this as a discovery lead when a proposal invokes FLP or claims that consensus is impossible in practice.

## What to inspect

The retrieved opening states a possible nonterminating execution with one faulty process. The exact model and proof must be inspected before applying that result; repeated fresh follow-ups here timed out.

## What to borrow and adapt

Our application question: which timing, failure and progress assumptions does the proposed design actually make? Do not reject a consensus implementation or invent a liveness guarantee from this incomplete receipt.

## Diagram implications

A future model should separate failure assumptions, message delivery and a requested progress property. No proof-specific schedule or visually inspected figure is supplied by this card.

## Mismatches and limits

Candidate only. No substantive fresh model/proof review, retained earlier review, simulation or implementation verification supports a decision here. Read the original before promoting a specific impossibility claim.
