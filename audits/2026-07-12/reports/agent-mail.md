# Agent Mail Audit

Initial verdict: fail. Final local verdict: pass.

## Findings

- P1 identity/authentication: `src/http.rs:92-155`, `src/mcp.rs:228-242`, and `src/store.rs:181-200` trusted caller-selected identities behind one shared token.
- P1 notification drift: HTTP mutations bypassed the MCP resource notifier.
- P1 readiness: `src/http.rs:50-52` returned healthy without checking PostgreSQL.
- P1 production mutation: `scripts/public_mcp_smoke.sh:172-213` created persistent live records without an explicit gate.
- P2 retry and lifecycle: MCP start was not idempotent; sessions/subscriptions were unbounded; local PostgreSQL scripts hard-coded a missing Homebrew 17 path.
- P2 validation: payloads lacked size limits, JSON-RPC request-shape errors were misclassified, and clippy failed on five warnings.

## Fixes

Implemented participant bearer credentials with server-derived senders, session-bound MCP resources, migration-only credential rotation, idempotent sends, bounded cursor pagination, HTTP-to-MCP notifications, `/live` and database-backed `/ready`, session caps/TTL/delete, payload limits, portable PostgreSQL discovery, strict production-smoke confirmation, and focused Rust/integration regressions. Removed the redundant skill README after moving unique operational content.

## Evidence

- `make -C skills/agent-mail check`: pass, including 5 Rust tests and clippy with warnings denied.
- `make -C skills/agent-mail real-test`: pass for HTTP and MCP against temporary PostgreSQL.
- Live public smoke: not run; separate production authority required.
