# Private evaluator evidence key

Expected reconciliation: blobs are in object storage; metadata/text in DB; queue is a task queue; parser is a separate workload sharing the same release, not necessarily a separately owned service; supplied deployment is Region A with 2 HTTP replicas and 1 worker; client polls. README's socket, blob-in-DB, region-B, multi-replica-for-all, and active-active claims conflict with stronger dated/source-linked evidence. Do not imply that absence from the scoped inventory proves no other accounts or regions exist.

Evidence ranking should be claim-specific: implementation source supports behavior; deployment inventory plus release record supports captured placement/version, not current liveness today. README does not outweigh those facts merely because it is documentation. Both API and worker share revision but entrypoints and scaling differ.

Failure paths: upload's put/DB/send is not atomic and may leave a blob or pending record after failures; queue errors retry then DLQ; no demonstrated failed-status update explains polling timeout/manual check. Mentioning these in the diagram or annotation is useful. Do not draw failed status as implemented, or invent automatic redrive, cross-region failover, or websocket connections.

Diagrams must remain documentation of supported current behavior. Proposed repairs can be listed separately if useful, but are not required. Unknown global routing/DR should appear as explicitly unknown or out of captured scope, rather than invented nodes. No human answer needed; no-answer fallback is to preserve scoped uncertainty and request scoped live inventory only as a next verification step. No production access is authorized.
