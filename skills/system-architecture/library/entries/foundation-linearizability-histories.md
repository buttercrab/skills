---
{
  "id": "foundation-linearizability-histories",
  "kind": "foundation",
  "title": "Linearizability: reason about operation histories",
  "summary": "Check legal object behavior and real-time precedence without confusing logical effect with response time.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "verify",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "concurrent-objects",
      "operation-histories"
    ],
    "qualities": [
      "correctness",
      "consistency"
    ],
    "scale": [
      "single-process",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf",
      "title": "Herlihy and Wing: Linearizability: A Correctness Condition for Concurrent Objects",
      "locator": "§1.2 FIFO histories; §2.1–2.3 histories, pending operations and definition; §3.1 locality",
      "revision": "TOPLAS 12(3), 1990; coauthor-hosted original PDF"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh coauthor-hosted original histories, definition and locality statement read. CMU follow-up failed; Brown copy supplied substantive sections. No proof mechanization or runtime test."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "foundation-cap-model",
    "foundation-transaction-isolation"
  ]
}
---

# Linearizability: reason about operation histories

## When to use

Use when concurrent reads/writes or a timeout are being interpreted as a simple sequence of completed effects.

## What to inspect

Read invocation/response histories, the legal sequential specification and real-time ordering condition. Pending invocations may have taken effect even when no response has returned. The examples distinguish overlapping from nonoverlapping operations.

## What to borrow and adapt

Our application: after a timed-out enqueue, neither “definitely absent” nor “safe to create another logical item” follows solely from the timeout. Record the operation interval and reconcile its identity against the queue's actual API. Inspect implementation evidence separately.

## Diagram implications

Draw intervals or explicit invocation/response events. Preserve overlaps and pending calls instead of inventing a total chronology. Label an inferred effect point as an interpretation, not an observed instruction.

## Mismatches and limits

A sequential-looking diagram does not prove linearizability. Object semantics matter; this card does not establish transaction atomicity across several business objects, durability or a running system's implementation correctness.
