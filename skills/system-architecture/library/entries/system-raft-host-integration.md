---
{
  "id": "system-raft-host-integration",
  "kind": "system",
  "title": "etcd Raft: consensus core versus host persistence and transport",
  "summary": "A deterministic consensus library delegates critical storage, transport and application ordering obligations to its embedding host.",
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
      "replicated-state-machine",
      "host-integration",
      "consensus"
    ],
    "qualities": [
      "consistency",
      "durability",
      "availability"
    ],
    "scale": [
      "distributed"
    ]
  },
  "sources": [
    {
      "url": "https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/README.md",
      "title": "etcd-io/raft: README.md",
      "locator": "Minimal core philosophy; Node.Ready host responsibilities, persistence/message/apply/Advance ordering; clock-dependent lease-read caveat",
      "revision": "c51f010c851edd0dada5af41bafbf68e54617767"
    },
    {
      "url": "https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/node.go",
      "title": "etcd-io/raft: node.go",
      "locator": "Ready fields, Messages/CommittedEntries/MustSync and AsyncStorageWrites exceptions, around lines 52–122",
      "revision": "c51f010c851edd0dada5af41bafbf68e54617767"
    },
    {
      "url": "https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/storage.go",
      "title": "etcd-io/raft: storage.go",
      "locator": "Storage interface error/recovery and ownership contracts, selected lines 38–100",
      "revision": "c51f010c851edd0dada5af41bafbf68e54617767"
    }
  ],
  "evidence": {
    "mode": [
      "source-inspected"
    ],
    "inspected_at": "2026-11-07",
    "freshness": "versioned",
    "scope": "Fresh pinned README, Ready and Storage contracts inspected. No algorithm execution, formal proof reproduction, transport/storage integration or runtime fault testing."
  },
  "reuse": "Original contextual annotations and exact source links only. No upstream code, diagrams, assets or packages redistributed; no license or operational assurance inferred.",
  "related": [
    "foundation-linearizability-histories",
    "diagram-c4-deployment-mapping"
  ]
}
---

# etcd Raft: consensus core versus host persistence and transport

## When to use

Use when a design assumes that linking a consensus library automatically supplies durable storage, reliable networking or correct application integration. It also helps explain why an abstract algorithm and an operational service need different diagrams.

## What to inspect

The README places network and disk IO outside the consensus core and gives the host a Ready-processing sequence. Read the Ready type too: its field contracts distinguish ordinary handling from AsyncStorageWrites messages and preconditions. Storage’s interface documents what errors and returned entries mean. At this pin, README step 2 permits peer messaging while entries from the same Ready batch persist after its stated HardState/previous-batch conditions; Ready Entries/Messages comments describe a stricter append-before-message order. This documentation tension is not resolved by this source trace, so the card is not a complete integration recipe. The README’s historical adoption statements are not independently verified or used as quality evidence.

## Architecture trace

Inputs include proposals, received messages and ticks. The core emits entries/state, outbound messages and committed work for the host. In the ordinary integration path, persistence and message/application ordering are part of the safety contract; asynchronous-storage mode represents dependencies through storage messages instead. Storage errors can make an instance inoperable, leaving cleanup/recovery to the application. This trace inspects those contracts, not a fully integrated service.

## What to borrow and adapt

Write down which layer owns persistence, message delivery, application state and recovery. Use the selected mode’s actual ordering contract instead of copying a simplified loop or assuming every write/message can run in parallel. Separate committed log position from application side effects and client-visible completion. A replicated state machine does not by itself make an external payment or email exactly once.

## Diagram implications

Draw the host adapter and durable store outside the deterministic core. A sequence should distinguish storage completion, peer messages, apply and Advance, labeling any asynchronous mode rather than mixing both into one unconditional order. AsyncStorageWrites forbids Advance and uses storage response messages instead; ordinary-mode progress/apply overlap also needs its actual inter-batch contract rather than an unconditional apply-before-Advance arrow. A deployment view additionally needs actual node/failure-domain evidence; the library API alone supplies none.

## Mismatches and limits

This is an integration case, not a recommendation to implement consensus for ordinary CRUD. Exact read guarantees depend on the selected read path; the README notes clock assumptions for lease-based reads. No consensus proof, storage adapter, network partition, member change or downstream service was exercised. Source HEAD is a pinned snapshot, not a certified release or running deployment.
