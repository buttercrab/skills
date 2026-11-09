# Diagram semantics review

Date: 2026-11-07. Read-only review of the four original examples in `skills/system-architecture/references/diagram-contract.md`, after the coordinator's sequence-label syntax simplification. No assessment fixtures were read. No diagrams were rendered or visually viewed, no parser was run by this reviewer, and no runtime behavior, tool installation or real-system configuration was tested. The coordinator's Mermaid syntax checks are separate evidence.

The reviewer authored the diagram-library lane but did not author these four operating-reference examples. The two source samples below are fresh rechecks of authored card claims, not an independent curator audit of those cards.

## Concrete correction recommended

**Minimal context — relationship label and declared arrow meaning differ.** The reviewed source has `F["Local CSV file"] -->|reads records| I`. Read in its declared direction, the file appears to read the importer; the accompanying caption says arrows mean data transfer. Keep the file → importer data direction and label it `supplies records` or `record data`, or reverse the edge if the intended view is read-access dependency. This is a semantic labeling issue even if the source parses.

The same caption declares only data transfer while the operator → importer edge says `runs with local input`, which describes invocation/control. Retain the useful edge but describe the mixed, explicitly labeled invocation/data relationships, or make the operator's input relationship unambiguously data-oriented. No extra infrastructure is needed to correct either point.

These observations preserve the reviewed pre-correction wording; any subsequent coordinator correction should be recorded as reconciliation rather than silently erasing the finding.

## Four-example assessment

| Example | Semantic finding and limit |
| --- | --- |
| Minimal offline context | Clearly proposed, small in scope and free of invented cloud infrastructure. The arrow/caption precision correction above is needed. Safe file replacement is explicitly outside the view, so no durability/atomic-replacement guarantee is inferred. |
| Accepted operation / uncertain external effect | Local operation+outbox atomicity is an explicit assumption; acceptance follows local commit and differs from external completion. Timeout records unknown rather than success or failure; no automatic provider retry is promised. The result/ack ordering is consistent with the stated limit. This is one schematic delivery/attempt, not a complete redelivery/recovery protocol: it does not prove serialization, relay persistence or operation-key enforcement before external effects. Its prose explicitly preserves those gaps and the lost-ack policy. A future complete protocol would need those gates, not a new exactly-once arrow label. |
| Operation state | The operation store is named as state owner; known rejection and uncertain timeout/interruption differ. Reconciliation reaches a terminal outcome only after evidence. No unknown→automatic-retry transition is drawn, and cancellation/refund are expressly unresolved. The scenario and state model agree about confirmed outcome versus unknown observation. The sequence omits some state updates/branches, which is acceptable for its declared illustrative scope and not proof of exhaustive conformance. |
| Deployment proposal | Host/process/storage roles and undecided database location are labeled as a separate proposal; runtime access is distinguished from imports. No current-production replicas, network policy, redundancy or failover is asserted. Treat this as its own illustration, not a complete deployment mapping of the preceding API/relay/broker/worker sequence; the heading's separate-proposal status supports that reading. |

No additional demonstrated semantic defect or hidden operational guarantee was found within those explicit proposal/partial-view boundaries. That is not a proof that the proposed system is correct or safe to implement unchanged.

## Two primary-source rechecks

1. **Card `diagram-c4-context-container`: logical C4 container versus deployment.** Freshly read [C4 Container diagram](https://c4model.com/diagrams/container), definition/scope and Notes (official mutable page, 2026-11-07). It defines application/data-store roles and explicitly leaves clustering, replication and failover to environment-specific deployment views. The card's distinction is supported. This does not establish any particular runtime placement or mandate every C4 level.
2. **Card `diagram-structurizr-model-views`: authored relationships and derived views.** Freshly read [Structurizr language reference, Dynamic view](https://docs.structurizr.com/dsl/language#dynamic-view) and [Implied relationships](https://docs.structurizr.com/dsl/implied-relationships) (official mutable pages, 2026-11-07). Dynamic views use ordered relationship instances from the static model with scenario wording; default/configurable implied-edge rules can derive higher-level relationships. The card correctly warns that a derived edge is not separately observed infrastructure evidence. No DSL parser, generated view or exporter was exercised.

## Review boundary

This is semantic source/prose inspection plus two textual documentation rechecks. It does not assess rendered layout, accessibility, diagram comprehension, model checking, real deployment, transaction implementation or provider guarantees. The four diagrams are original proposals; primary documentation supports notation/model distinctions rather than the truth of a deployed design. No active source/card file was edited by this review.
