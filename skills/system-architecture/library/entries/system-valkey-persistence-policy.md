---
{
  "id": "system-valkey-persistence-policy",
  "kind": "system",
  "title": "Valkey: persistence policy, rewrite state and acknowledged-data risk",
  "summary": "Model snapshots, append-only increments, manifest replacement and synchronization policy as distinct durability decisions.",
  "status": "curated",
  "availability": "public",
  "facets": {
    "tasks": [
      "trace",
      "compare",
      "model-failure",
      "diagram"
    ],
    "contexts": [
      "in-memory-state",
      "persistence",
      "recovery"
    ],
    "qualities": [
      "durability",
      "latency",
      "operability"
    ],
    "scale": [
      "single-deployment"
    ]
  },
  "sources": [
    {
      "url": "https://valkey.io/topics/persistence/",
      "title": "Valkey persistence documentation",
      "locator": "RDB/AOF/no-persistence choices; multi-part AOF rewrite; fsync policy and truncation behavior",
      "revision": "Live documentation read 2026-11-07; not a frozen release"
    },
    {
      "url": "https://github.com/valkey-io/valkey/blob/aa7545348b688b469d073a01ce4836ed637577f9/src/aof.c",
      "title": "valkey-io/valkey: src/aof.c",
      "locator": "Opening AOF manifest implementation: BASE/INCR/HISTORY ownership and rewrite lifecycle, lines 65–170",
      "revision": "aa7545348b688b469d073a01ce4836ed637577f9"
    },
    {
      "url": "https://github.com/valkey-io/valkey/blob/aa7545348b688b469d073a01ce4836ed637577f9/valkey.conf",
      "title": "valkey-io/valkey: valkey.conf",
      "locator": "appendfsync everysec and no-appendfsync-on-rewrite policy commentary/settings, around lines 1723–1790",
      "revision": "aa7545348b688b469d073a01ce4836ed637577f9"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh selected pinned AOF/configuration sections and live first-party persistence text inspected. Intended mechanisms only; no deployment, disk experiment or upstream execution."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "foundation-slo-measurement",
    "foundation-transaction-isolation"
  ]
}
---

# Valkey: persistence policy, rewrite state and acknowledged-data risk

## When to use

Use when a design says “the cache is persistent” without specifying loss tolerance, acknowledgment and restart behavior. It is a useful mechanism-level comparison between periodic snapshots and logged updates.

## What to inspect

Read the documented persistence choices and rewrite process, then the source’s manifest roles and the pinned configuration’s synchronization options. BASE is the last rewrite snapshot, ordered INCR files carry later writes and HISTORY files become cleanup candidates. The configuration explicitly exposes a speed/data-safety choice; it is not proof that any deployment uses that default.

## Architecture trace

During multi-part AOF rewriting, a new base and ongoing increments are coordinated through manifest state rather than treated as one overwritten file. The selected aof.c comments define which files remain authoritative; the configuration and live documentation explain when disk synchronization is requested and how a rewrite-related option can weaken that policy. Source/configuration inspection did not observe a write acknowledgment, fsync completion, restart or recovery.

## What to borrow and adapt

Ask what loss window the product can tolerate and identify which acknowledged operations may not yet have crossed a durable boundary. Model rewrite/compaction as a lifecycle with old and new authoritative sets, not a background operation assumed to be harmless. Keep backup/recovery verification separate from persistence and from replication.

## Diagram implications

Show memory, base snapshot, incremental log files, manifest and disk synchronization as separate concepts. Annotate the selected policy and rewrite handoff. A replication arrow would not by itself demonstrate disk durability. A sequence or state view can expose interruption between producing a new base and publishing its manifest.

## Mismatches and limits

Public documentation includes broad durability shorthand; this card does not treat it as a universal data-loss upper bound across storage, OS and configuration failures. The inspected source is a pinned development snapshot and the docs are mutable. No current cluster configuration, replication guarantee, fault injection, backup restoration or performance comparison was tested.
