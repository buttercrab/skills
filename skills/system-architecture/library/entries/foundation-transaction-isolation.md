---
{
  "id": "foundation-transaction-isolation",
  "kind": "foundation",
  "title": "Transaction isolation: define the actual database contract",
  "summary": "Distinguish snapshots, serializable execution and application retry responsibilities at a versioned database boundary.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "compare",
      "trace",
      "model-failure"
    ],
    "contexts": [
      "transactions",
      "database-boundaries"
    ],
    "qualities": [
      "consistency",
      "correctness"
    ],
    "scale": [
      "single-deployment",
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://www.postgresql.org/docs/18/transaction-iso.html",
      "title": "PostgreSQL 18: Transaction Isolation",
      "locator": "Table13.1; §§13.2.1–13.2.3; complete-transaction retry and concurrent sum/insertion example",
      "revision": "PostgreSQL 18 documentation; inspected 2026-11-07"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected",
      "conceptual"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh version18 official isolation table, level definitions, anomaly example and retry sections read. No server, transaction or external effect tested."
  },
  "reuse": "Original annotation and links only. No papers, figures, source packages or upstream assets redistributed; copying terms not adjudicated.",
  "related": [
    "pattern-saga-compensation",
    "system-sqlite-commit-boundaries"
  ]
}
---

# Transaction isolation: define the actual database contract

## When to use

Use when “transactional” or “consistent snapshot” is being treated as a complete description of concurrent business behavior.

## What to inspect

Read the version's actual phenomena table and isolation sections. PostgreSQL Repeatable Read prevents phantoms but can allow serialization anomalies. Serializable can abort transactions; the application must handle the documented retry boundary.

## What to borrow and adapt

Our application: two editors validate a shared capacity limit before inserting independent reservations. Model the competing reads/writes and the rule that must hold; select a database-supported enforcement strategy, then account for abort/retry without duplicating any external notification.

## Diagram implications

Show transaction boundaries, commit/abort and which snapshot each read uses. Keep an external message separate from a database commit; a line inside a drawn box does not make it transactional.

## Mismatches and limits

These are PostgreSQL18 contracts, not every engine's interpretation of similarly named levels. The source notes special cases such as sequences. No concurrency experiment, schema review or actual database configuration was performed.
