---
{
  "id": "foundation-end-to-end-guarantees",
  "kind": "foundation",
  "title": "End-to-end arguments: locate the knowledge needed for correctness",
  "summary": "Separate transport assistance from the application knowledge needed to fulfill an end-to-end promise.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "trace",
      "model-failure"
    ],
    "contexts": [
      "function-placement",
      "remote-effects"
    ],
    "qualities": [
      "correctness",
      "reliability"
    ],
    "scale": [
      "distributed",
      "cross-scale"
    ]
  },
  "sources": [
    {
      "url": "https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf",
      "title": "Saltzer, Reed and Clark: End-to-End Arguments in System Design",
      "locator": "PDF pp.2–7: careful file transfer, performance tradeoffs, duplicate suppression and sequencing",
      "revision": "TOCS 2(4), 1984 revised paper"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh original-paper argument, duplicate suppression and sequencing sections read. No current infrastructure, code path or runtime experiment inspected."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "pattern-transactional-outbox",
    "system-nats-delivery-effects"
  ]
}
---

# End-to-end arguments: locate the knowledge needed for correctness

## When to use

Use when a lower layer is said to guarantee a business operation, delivery or deduplication outcome.

## What to inspect

Read the application-knowledge argument and duplicate-message example. Related mechanisms at different layers can have different scopes; lower-layer assistance can still be valuable.

## What to borrow and adapt

Our application: a document submission retried after a lost response needs an operation identity understood by the recipient. A reliable connection alone cannot decide whether a newly originated request means the same submission. Put the ownership and reconciliation decision where that information exists.

## Diagram implications

Trace the user's operation through the transport and durable effect. Distinguish delivery, processing, commit and acknowledgement. Show where a retry can originate, not merely a bidirectional network arrow.

## Mismatches and limits

This is a function-placement argument, not a prohibition on infrastructure reliability or layered protection. No current queue/service guarantee follows from the paper, and no duplicate-processing experiment was run here.
