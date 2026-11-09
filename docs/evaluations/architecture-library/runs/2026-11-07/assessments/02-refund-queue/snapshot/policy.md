# Business and operations policy
- A customer-approved refund must not be silently lost and must never intentionally issue the same business refund twice.
- Callers may retry creation after a lost HTTP response; current requests carry client_request_id, but the handler ignores it.
- 99% of normal requests should finish within five minutes. Ambiguous cases may await human review.
- Retain a complete audit of requested amount, approved charge, provider attempts, and final decision for 180 days.
- Refund jobs can be delayed for ten days during a provider incident.
- Two application engineers maintain this system. A database and queue already exist.
- Finance has not approved the action for an unresolved provider outcome after the seven-day lookup/idempotency window.
