# Private evaluator evidence key

Required risks: DB-commit/publish gap; provider-success/DB-write gap; duplicate or concurrent queue delivery; duplicate API creation; timeout is not failure; queue acknowledgment is distinct from durable business completion. The API's seven-day limit conflicts with the ten-day incident delay and must influence recovery. Do not require any named messaging product or one canonical table design.

Strong proposals make intent and transitions durable, bind a stable key/payload to one business operation, coordinate concurrent attempts, reconcile ambiguous outcomes within documented visibility limits, and acknowledge only after durable ownership/outcome suitable for recovery. Atomic outbox/inbox patterns are possible, not mandatory; database polling could also meet the constraints if justified. A database transaction alone cannot make the external effect atomic. “Exactly once” without a bounded claim and mechanism fails.

Scripted answer, only if asked what finance permits after the retention window: “Finance requires holding the refund as unresolved and escalating for evidence-based manual reconciliation. No automatic new-key refund is permitted without a recorded finance decision.” Do not proactively reveal this block to the assessed agent.

No-answer fallback: preserve unresolved state, stop automatic new external effects, surface aged uncertainty, and ask finance for the decision policy. Do not invent a provider endpoint, assume lookup remains available indefinitely, or declare not-found definitive before 90 seconds. Diagrams should show commit, dispatch/claim, external uncertainty, durable outcome, acknowledgment, and recovery with appropriate alternatives; multiple diagrams are optional.

Current/proposed separation matters: no outbox or unique request key exists today. Calling that proposed architecture current is incorrect. Performance guarantees cannot be measured from this snapshot.
