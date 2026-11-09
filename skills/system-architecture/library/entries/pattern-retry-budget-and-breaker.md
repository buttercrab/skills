---
{
  "id": "pattern-retry-budget-and-breaker",
  "kind": "pattern",
  "title": "Retry budgets and circuit breakers: reason about amplification and unknown results",
  "summary": "Choose retry ownership, timeout scope and failure response before adding resilience mechanisms or copying thresholds.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "model-failure",
      "compare",
      "trace",
      "diagram"
    ],
    "contexts": [
      "remote-calls",
      "overload",
      "retries",
      "idempotency"
    ],
    "qualities": [
      "availability",
      "latency",
      "operability",
      "consistency"
    ],
    "scale": [
      "multi-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf",
      "title": "Brooker: Timeouts, retries, and backoff with jitter",
      "locator": "PDF pp.2–5: timeout scope, layered retries, token buckets, jitter",
      "revision": "2019 original PDF; inspected 2026-11-07"
    },
    {
      "url": "https://d1.awsstatic.com/builderslibrary/pdfs/making-retries-safe-with-idempotent-apis-malcolm-featonby.pdf",
      "title": "Featonby: Making retries safe with idempotent APIs",
      "locator": "PDF pp.2–4, 6–8: caller intent, atomic token/effect, late arrivals and mismatches",
      "revision": "2020 original PDF; inspected 2026-11-07"
    },
    {
      "url": "https://martinfowler.com/bliki/CircuitBreaker.html",
      "title": "Fowler: Circuit Breaker",
      "locator": "closed/open/half-open example; error scope and client fallback",
      "revision": "2014-03-06 practitioner article; inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "historical",
    "scope": "Fresh primary sections read as architectural guidance. No upstream implementation, diagram rendering/viewing, test, benchmark, failure injection or deployed service was exercised."
  },
  "reuse": "Original contextual annotations and primary links only. No upstream text, code, diagrams or assets redistributed; reuse rights for those artifacts are not inferred.",
  "related": [
    "foundation-overload-capacity",
    "foundation-end-to-end-guarantees"
  ]
}
---

# Retry budgets and circuit breakers: reason about amplification and unknown results

## When to use

Use when a retry is assumed harmless, several call layers retry independently, or a breaker is proposed without a caller-visible recovery contract.

## What to inspect

Brooker explains retry amplification, timeout coverage and jitter, while warning about breaker modal behavior. Fowler explains breaker transitions and clients’ responsibility to respond to an open circuit. Featonby connects a stable caller request identity to atomic effect recording, response meaning, retention and mismatched intent.

## What to borrow and adapt

Choose a retry owner and bounded end-to-end budget from the operation’s needs. A timed-out create may already have committed; preserve identity across retries or reconcile, rather than issue a new operation blindly. Decide what is retryable and what the user sees when attempts end. Evaluate breaker recovery behavior alongside simpler retry throttling; measure the dependency before copying example timeouts or percentages.

## Diagram implications

Show the caller deadline, attempts and budget owner, commit-versus-response gap and identity lifetime. If using a breaker, model closed/open/probe transitions and fallback/reconciliation; label timeout as an observation, not evidence of no effect.

## Mismatches and limits

No current SDK, service or benchmark was tested. The practitioner accounts are not controlled comparisons; their numeric examples are contextual. Broker deduplication, retry throttling and application idempotence cover different boundaries. An identifier with no durable atomic enforcement cannot establish the promised effect guarantee.
