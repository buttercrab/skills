# Independent source sample: Raft integration and Kubernetes reconciliation

Date: 2026-11-07. Reviewed only `system-raft-host-integration` and `system-kubernetes-reconciliation`, then freshly fetched their owning primary material. Five exact-pinned repository files and one live controller-guide URL were inspected through selected sections. No source, test, generator, simulator, cluster, transport/storage adapter or diagram renderer was executed. Cards/examples were not edited; assessment fixtures were not read.

## Judgment

The cards' central distinctions are supported: a consensus core does not supply a complete durable/application service, and controller requests/expectation expiry are not successful observed workload completion. No material claim of executed behavior or exactly-once external effects is demonstrated in the current annotations.

One source-level ambiguity should be exposed more explicitly in the Raft card: the same pinned README and Ready field comments describe different apparent same-batch entry/message ordering. The card currently avoids a fixed recipe, which limits the risk, but “use the selected mode's actual contract” alone does not tell the reader that those two ordinary-mode sources disagree. Two further diagram clarifications are useful but do not correct demonstrated runtime falsehoods.

## Raft: supported obligations and precise ambiguity

All three files are pinned to `c51f010c851edd0dada5af41bafbf68e54617767`:

| Inspected source | Supported relationship / limit |
| --- | --- |
| [README.md](https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/README.md#L115), host processing steps and proposal caveat | Core leaves disk/network IO to its host; persistence, peer messaging, apply and progress notification have responsibilities. A proposal is not guaranteed to commit. Adoption/performance claims were not independently verified. |
| [node.go](https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/node.go#L52), Ready fields plus Node.Ready/Advance | Durable write versus permissible non-durable write is represented by MustSync; committed entries, outbound messages and async append/apply messages are distinct. Prior-batch committed entries/snapshots must finish applying before next-batch application. AsyncStorageWrites forbids calling Advance; completion response messages take its place. |
| [storage.go](https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/storage.go#L42), Storage contracts | Host owns storage/recovery integration and must respect slice/entry ownership. Interface comments state the inoperable-instance/recovery consequence; individual methods also define errors and temporary unavailability. The card's qualified “can make” phrasing does not turn every special return into one universal failure rule. |

**Recommended precision edit:** [README step2, line119](https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/README.md#L119) permits peer messages while entries from the same Ready batch persist, after its stated HardState/previous-batch conditions. [node.go Entries/Messages comments, lines74 and98](https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/node.go#L74) state the ordinary path's messages follow entry appending. Record that documentation tension and avoid presenting the card as a complete optimized integration recipe; this review does not resolve it by running a host or auditing the algorithm implementation.

For diagrams, explicitly distinguish ordinary Advance from asynchronous storage response messages. [Node.Advance, line176](https://github.com/etcd-io/raft/blob/c51f010c851edd0dada5af41bafbf68e54617767/node.go#L176) forbids Advance in async mode. Do not impose “apply always completes before Advance” as an unconditional order either: the inspected ordinary API describes an optimization allowing progress notification while current application work continues, subject to inter-batch application ordering.

The card correctly separates committed log state, application effects and client completion. No sampled artifact implements an embedding client's durable-effect/ACK policy, so the review cannot certify one. Its warning that external payments/emails are not automatically exactly once is an application-boundary interpretation, not an observed downstream integration.

## Kubernetes: supported requests, observations and expiry

Pinned code revision: `ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8`.

- [ReplicaSet source](https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/pkg/controller/replicaset/replica_set.go#L631): processNextWorkItem rate-limits a requeue after sync errors; manageReplicas bounds bursts, records expected creates/deletes before pod controls and reduces skipped/failed-operation accounting. Delete observations have a separate event path. These selected branches support the card without proving convergence.
- [syncReplicaSet, line793 onward](https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/pkg/controller/replicaset/replica_set.go#L793): expectation satisfaction gates replica management; status still follows its own update path. This keeps action issuance, cached observation and readiness/availability distinct.
- [controller_utils.go, SatisfiedExpectations/isExpired](https://github.com/kubernetes/kubernetes/blob/ac8d3ed1cdf6c8bb11e9d3eda8acf2a9f03915b8/pkg/controller/controller_utils.go#L195): fulfillment, expiration, missing state or lookup error can allow progress. Expiration compares elapsed time when checked; these reviewed methods do not themselves schedule a future sync. That does not establish absence of scheduling elsewhere.
- [Live controller guide](https://kubernetes.io/docs/concepts/architecture/controller/), Controller pattern / Control via API server / Direct control / Desired versus current state: controllers can act directly or request API changes; the Job example does not execute its Pods itself. The guide is mutable documentation, not the exact pinned controller's release contract or observed cluster topology.

**Optional wording refinement:** replace “Do not draw an API call as direct execution by a controller” with an explicit distinction between a create-Pod API request and the controller directly running that Pod. The current wording's intended boundary is supported, but its subject can be clearer. Likewise, an expiration arrow should not imply an automatically scheduled timer unless its actual scheduling source is inspected.

No request acceptance, expectation decrement or expiry is demonstrated as workload success. No controller/informer/API-server execution, actual retry timing, cluster state or test outcome was observed. The selected mechanics are a useful reconciler model, not an exactly-once or whole-cluster correctness proof.
