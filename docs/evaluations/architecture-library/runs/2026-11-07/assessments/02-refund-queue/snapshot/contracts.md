# Queue and payment contracts
Queue: delivery is at least once. A lease expires after 45 seconds. A worker can terminate at any instruction. Acknowledgment removes that delivery; it does not commit database state. Multiple workers may receive the same refund while a lease expires.

Payment API: POST /refund accepts charge ID and minor-unit amount. An optional caller-generated idempotency key is retained for seven calendar days. Reusing the same key and payload returns the original result. Reusing a key with a different payload returns a conflict. A timed-out call can have succeeded. GET /refunds/by-key is available during the same retention window, with eventual visibility up to 90 seconds; “not found” before then is inconclusive. There is no distributed transaction with the caller's database. No callback delivery guarantee is offered.

Database: transactions are atomic within this database. Refund IDs are stable. Current schema has no request-id unique constraint, no provider-attempt record, and no outbox table.
