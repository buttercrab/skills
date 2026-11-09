# Additional captured evidence
Client source revision 7f12a6b calls GET /documents/:id every three seconds until status is ready or failed; it stops polling after two minutes and offers “Check again.” No socket client is in the captured entrypoint.

Queue adapter contract: handler success acknowledges delivery; thrown errors leave it eligible for redelivery after visibility timeout. After four deliveries, queue moves it to intake-failed. Current parseJob has no catch or failure-state write. Operations reviews intake-failed each weekday; no automatic redrive is configured.

Release record: revision 7f12a6b completed rollout 2026-11-05 at 09:00Z. No live probes or cross-account inventory were supplied. No evidence covers regional disaster recovery, global routing, or third-party storage replication.
