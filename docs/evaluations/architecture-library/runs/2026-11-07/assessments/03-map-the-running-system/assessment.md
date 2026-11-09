# Document ingestion: source-only architecture assessment

This assessment reconciles the supplied revision `7f12a6b` and captured deployment inventory for incident responders. It describes the current captured model, not independently verified live production. Editable runtime and deployment views are in [diagrams.md](diagrams.md). No application or infrastructure changes are proposed or made.

## Evidence and status

All locators below are relative to this run's `snapshot/` directory. `intake.ts` is directly inspected implementation. `deployment.yaml` is a supplied rendered inventory captured at 2026-11-05 09:00Z, scoped to the intake application account (lines 1–3, 22). `client-and-operations.md` records client behavior, queue contract, operational practice and completed rollout; the actual client, queue adapter, rollout logs and live environment were not inspected. The README is documented historical intent maintained in June 2025, not current placement proof (`README.md:2–4`). There are no local architecture-card annotations or external primary-source claims in this assessment.

## Representative runtime and state ownership

1. `upload` awaits writing bytes to object storage, inserting a metadata record containing `blobKey` and `pending`, then sending `recordId` to the task queue; only after send resolves does it return `{status: 202, id}` (`intake.ts:2–6`). This response establishes the source's completed acceptance sequence, not parsing completion. Storage-provider durability guarantees and HTTP wrapper behavior are not supplied.
2. `parseJob` reads metadata, retrieves the blob, invokes `deps.parser.parse`, and updates metadata/text to `ready` (`intake.ts:10–14`). The database owns the captured status and parsed text; the object store holds original bytes. Parser internals and whether `deps.parser` is local or remote are unknown.
3. The captured queue contract acknowledges handler success, allows redelivery after thrown errors and visibility timeout, then moves a job to `intake-failed` after four deliveries (`client-and-operations.md:4`). Configuration lists 120 seconds visibility and four deliveries (`deployment.yaml:13–15`). Successful completion and acknowledgment are distinct; an interrupted or lost acknowledgment after the database write can permit repeated execution. No deduplication or execution-time bound is evidenced.
4. `status` reads the database (`intake.ts:8`). Captured client evidence says GET `/documents/:id` every three seconds until `ready` or `failed`, stopping after two minutes with “Check again” (`client-and-operations.md:2`). That is a client waiting limit, not cancellation or a proven processing deadline. The supplied source does not establish route wiring or authentication.

## Failure path and incident implications

A thrown parse-job error does not write `failed`; the handler has no catch or failure-state write (`intake.ts:10–15`; captured queue contract `client-and-operations.md:4`). After four failed deliveries the queue moves the message to `intake-failed`; operations reviews that queue each weekday and no automatic redrive is configured (same locator). A dead-lettered document can therefore remain `pending` if no ready write occurred. A `ready` row is also possible if a write took effect before an uncertain return/acknowledgment; dead-letter placement alone does not prove the document's recorded state. No failure-state writer appears anywhere in the supplied implementation, despite the client recognizing `failed`.

Upload writes are separately awaited, with no encompassing transaction, outbox or compensation shown (`intake.ts:3–6`). Failure after blob storage can leave a blob without metadata; failure after insertion can leave a pending row without a confirmed enqueue. A send timeout can leave enqueue outcome unknown, so retry safety is not established. These are source-supported possible partial outcomes, not observed incidents. Cleanup, caller retries, request deduplication, reconciliation and queue-send persistence guarantees are unknown.

## Discrepancies

| Disputed claim | Reconciled captured model | Supporting evidence and limit |
| --- | --- | --- |
| Gateway stores uploaded documents in database | Bytes go to object storage; DB holds blob key/status and parsed text | `README.md:2` vs `intake.ts:3–4,14`; `deployment.yaml:17–18` names the configured stores |
| Every upload is published to an event stream | Source sends a task containing record ID; successful upload response follows send | `README.md:2` vs `intake.ts:5–6`; `deployment.yaml:19–21`; failure before send defeats “every upload” |
| Separate parser service in Region B | Captured queue-consumer workload is parse-runner, one replica in Region A | `README.md:2` vs `deployment.yaml:3,9–12`; parser dependency's own process/location is unresolved (`intake.ts:13`) |
| Results pushed over persistent sockets | Captured client entrypoint polls status | `README.md:2` vs `client-and-operations.md:2`; does not prove no other clients use sockets |
| All services have multiple replicas, active-active in two regions | Captured intake has two replicas; parse-runner has one; inventory names Region A | `README.md:2` vs `deployment.yaml:3–12`; account scope and absent cross-account inventory prevent a global absence claim (`deployment.yaml:22`; `client-and-operations.md:6`) |
| Client terminal `failed` status implies dead-letter changes document state | Queue failure and document status are separate; supplied worker never writes failed | `client-and-operations.md:2,4`; `intake.ts:10–15` |

## Unknowns and next evidence

Current live topology, route bindings, parser placement, network/trust boundaries, DB transactions/durability, task delivery/ack persistence, idempotency and concurrency behavior are unverified. The captured inventory does not settle global routing, disaster recovery or third-party storage replication (`client-and-operations.md:6`). Responders should reconcile queue messages with database state and source revision before interpreting `pending` or dead-letter status as a definitive business outcome. Read-only live inspection would be a separate authorized follow-up, not a check performed here.

Decision: retain the implementation-derived flow and account-scoped captured deployment as the documentation model, with visible uncertainties. Do not carry forward README claims contradicted by stronger supplied evidence. No redesign alternative is selected because this request is documentation only.

## Actual checks

Read all four listed snapshot files with line numbers, read the supplied skill and its diagram-contract/boundaries-and-failure guides, and manually cross-checked each diagram's actors, order, status semantics, replica counts, queue failure path and evidence references against those inputs. Mermaid source is editable but was not parser-checked or rendered. No code, tests, builds, generators, network calls or live queries were executed. No runtime or visual verification is claimed.
