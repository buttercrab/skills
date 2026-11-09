---
{
  "id": "system-sqlite-commit-boundaries",
  "kind": "system",
  "title": "SQLite: rollback commit, WAL commit and checkpoint are different boundaries",
  "summary": "Separate logical completion, durable ordering and recovery state instead of drawing one generic write-to-database arrow.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "embedded-storage",
      "transaction-boundaries",
      "recovery"
    ],
    "qualities": [
      "atomicity",
      "durability",
      "consistency"
    ],
    "scale": [
      "single-process",
      "single-deployment"
    ]
  },
  "sources": [
    {
      "url": "https://sqlite.org/atomiccommit.html",
      "title": "Atomic Commit in SQLite",
      "locator": "Introduction and hardware assumptions; single-file commit 3.7–3.11; rollback; persistent journals",
      "revision": "Live documentation read 2026-11-07; not a frozen release"
    },
    {
      "url": "https://github.com/sqlite/sqlite/blob/425bfb8aa82e2fd7829d055335f164eaf617eae0/src/pager.c",
      "title": "sqlite/sqlite: src/pager.c",
      "locator": "Pager state comments around WRITER_FINISHED/ERROR and UNKNOWN_LOCK, selected lines 260–410",
      "revision": "425bfb8aa82e2fd7829d055335f164eaf617eae0"
    },
    {
      "url": "https://github.com/sqlite/sqlite/blob/425bfb8aa82e2fd7829d055335f164eaf617eae0/src/wal.c",
      "title": "sqlite/sqlite: src/wal.c",
      "locator": "File-format/commit-marker, checkpoint barrier and reader algorithm comments, lines 13–150",
      "revision": "425bfb8aa82e2fd7829d055335f164eaf617eae0"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh selected pinned pager/WAL comments and live first-party rollback documentation inspected. Source-contract interpretation only; no code, crash test, storage experiment or diagram rendering."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "foundation-transaction-isolation",
    "diagram-mermaid-state-ownership"
  ]
}
---

# SQLite: rollback commit, WAL commit and checkpoint are different boundaries

## When to use

Use when explaining where a storage operation becomes committed and what a crash can leave behind. It is a concrete contrast to treating a database API return, an operating-system write and a durable transaction as the same event.

## What to inspect

The rollback article explicitly excludes WAL. Read its flush and journal-finalization sequence, then the pinned pager state contract. Read wal.c separately: commit-marked frames and checkpoints answer different questions. The live article contains historical implementation discussions; the pinned source is the inspected contemporary mirror snapshot, not proof that every historical detail still applies.

## Architecture trace

For rollback mode, changed pages depend on journal protection and synchronization before journal finalization makes the transaction committed. The selected pager comments distinguish a fully written transaction awaiting finalization from ERROR state, where further use fails until references drain and state is reloaded. In WAL mode the source comments instead describe commit markers in frames and later transfer into the database during checkpoint. No commit branch, crash or filesystem was executed.

## What to borrow and adapt

Name the completion point and prerequisites of each state transition. A proposed storage design should identify which layer owns recovery and which ordering comes from its filesystem interface. Keep a specific failure scenario—such as interruption before finalization—beside its corresponding recovery obligation. Do not transplant SQLite’s exact file protocol into an unrelated application.

## Diagram implications

Prefer a state/sequence view with process cache, journal or WAL, database file and filesystem boundary. Label writes versus synchronization and commit versus checkpoint. Show rollback and WAL as alternatives or separate views; combining both finalization mechanisms into one linear happy path is misleading. A component overview alone cannot establish durability.

## Mismatches and limits

The guarantee depends on documented hardware/VFS assumptions and configuration; this is not an independent proof of atomicity on a particular device. Selected comments and public documentation were read, not all pager branches or tests. The GitHub repository is a mirror; no canonical Fossil identity reconciliation, runtime fault injection, benchmark or current deployed database inspection occurred.
