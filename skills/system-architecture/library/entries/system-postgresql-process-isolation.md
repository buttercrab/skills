---
{
  "id": "system-postgresql-process-isolation",
  "kind": "system",
  "title": "PostgreSQL: supervisor reliability and per-connection backend boundaries",
  "summary": "A supervising process can stay outside ordinary request/locking work while backend processes own client sessions and share database infrastructure.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "decompose",
      "trace",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "client-server",
      "process-isolation",
      "native-runtime"
    ],
    "qualities": [
      "availability",
      "fault-isolation",
      "operability"
    ],
    "scale": [
      "single-deployment"
    ]
  },
  "sources": [
    {
      "url": "https://www.postgresql.org/docs/current/tutorial-arch.html",
      "title": "PostgreSQL Architectural Fundamentals",
      "locator": "Client/server placement and per-connection process explanation",
      "revision": "Page resolved to PostgreSQL 18 documentation on 2026-11-07; distinct from source HEAD"
    },
    {
      "url": "https://github.com/postgres/postgres/blob/0607aa61090ac1b574f8bafe854c684195b31e16/src/backend/postmaster/postmaster.c",
      "title": "postgres/postgres: src/backend/postmaster/postmaster.c",
      "locator": "Opening architectural rationale, initialization/synchronization/recovery notes, lines 1–65",
      "revision": "0607aa61090ac1b574f8bafe854c684195b31e16"
    },
    {
      "url": "https://github.com/postgres/postgres/blob/0607aa61090ac1b574f8bafe854c684195b31e16/src/backend/tcop/backend_startup.c",
      "title": "postgres/postgres: src/backend/tcop/backend_startup.c",
      "locator": "BackendMain/BackendInitialize; startup packet, shared-memory process registration and PostgresMain handoff",
      "revision": "0607aa61090ac1b574f8bafe854c684195b31e16"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh pinned supervisor/startup source and first-party version-18 tutorial text inspected. No operating-system process or deployed server observed; no rendered upstream diagram."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "diagram-c4-context-container",
    "diagram-c4-deployment-mapping"
  ]
}
---

# PostgreSQL: supervisor reliability and per-connection backend boundaries

## When to use

Use when deciding what a supervisor must avoid doing if it is expected to recover failed request workers. The case also helps distinguish logical database responsibility from an operating-system process boundary.

## What to inspect

Read the tutorial’s frontend/server placement, postmaster.c’s stated reason for avoiding shared-memory lock participation, and BackendMain’s actual initialization handoff. The tutorial resolved to version 18; the pinned source is a later development snapshot. They are related evidence at different version boundaries, not a single verified deployed topology.

## Architecture trace

A client connects through the supervising server, which starts a backend. The pinned opening comment assigns authentication and request work to the child rather than blocking the supervisor. BackendMain performs connection setup, creates its per-backend PGPROC representation, switches memory context and calls PostgresMain. The postmaster rationale links limited shared-memory participation to recovery after a backend crash; that is maintainer reasoning and selected source, not a reproduced failure experiment.

## What to borrow and adapt

Separate the minimum control-plane responsibility from request execution and shared-state access. Explain which worker failures the supervisor is meant to tolerate and what cleanup/recovery must follow. If proposing a different threading/process model, compare memory sharing, connection cost, library blocking and recovery responsibilities rather than copying a process count.

## Diagram implications

Draw process boundaries explicitly: client, supervising postmaster and session backend are not three independently deployed services by default. Label startup/authentication and the later direct session path. Shared memory is a shared resource boundary, not evidence that the supervisor performs ordinary lock-manager work. Show where recovery resets state rather than promising all sessions survive.

## Mismatches and limits

This is a database-specific mature native architecture; it does not establish that process-per-connection is best for a small web service. Background/parallel workers and platform-specific startup paths extend the simplified view. Only selected source and tutorial portions were inspected; no server, authentication, crash recovery, capacity or production state was tested.
