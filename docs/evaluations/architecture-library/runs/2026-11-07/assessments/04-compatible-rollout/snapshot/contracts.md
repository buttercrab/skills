# Existing consumers and compatibility boundary
Current GET /attachments/{opaque_id} accepts an account session cookie and returns 200 bytes, 404 if absent or not owned, or 503 during storage failure. Some mobile clients released in 2024 are still supported until 2027-04-01; their download code cannot follow redirects, cannot send new headers, and retries 503 up to twice. URLs are stored in exported reports and must remain valid for their owner during the retention period.

New internal gateway contract: authorize(account_id, attachment_id) returns allow, deny, or unavailable. Only allow authorizes a read. unavailable must not be treated as allow. Denials must preserve the old public non-disclosure behavior. Gateway deployment is owned by another team and its availability target is 99.9%; its latency budget is 150 ms p95, not an observed result.

Target policy: revoke access within 60 seconds after a sharing policy change. No public object URLs. Existing cookie/session verification remains authoritative for identity.
