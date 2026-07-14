---
name: agent-mail
description: Use the Rust/PostgreSQL Agent Mail service for durable cross-session or cross-project instructions, handoffs, blockers, decisions, and status messages in project mailboxes. Use for Agent Mail participants, namespaces, inbox resources, or the deployed mailbox service. Do not use it for routine current-task subagent coordination, logs, or locks; use built-in collaboration unless durable mailbox persistence is required.
---

# Agent Mail

Agent Mail is a Rust HTTP mailbox service backed by PostgreSQL. It also exposes a remote MCP Streamable HTTP endpoint. Use it for durable cross-session coordination, not routine logs or locks.

Resolve `AGENT_MAIL_SKILL_DIR` to the directory containing this `SKILL.md`; do not assume the caller's current working directory is this repository.

The supported v1 runtime is the Rust `agent-mail-server` with PostgreSQL. The deployed service runs on a Lightsail Nano app host in `us-west-2` against private AWS RDS PostgreSQL and is reached at:

```text
https://agent-mail.cc
```

Use `https://agent-mail.cc` as the default `AGENT_MAIL_URL` for clients. The public edge is Cloudflare-proxied HTTPS on `agent-mail.cc`; nginx on the Lightsail Nano instance terminates the Cloudflare origin certificate and proxies to the Rust server on `127.0.0.1:8787`. Port `8787` is private and should not be exposed publicly.

Build the server:

```bash
make -C "$AGENT_MAIL_SKILL_DIR" build
```

Run the server against PostgreSQL:

```bash
"$AGENT_MAIL_SKILL_DIR/target/debug/agent-mail-server" \
  --database-url "$AGENT_MAIL_DATABASE_URL" \
  --bind 127.0.0.1:8787 \
  --token "$AGENT_MAIL_TOKEN"
```

Use `make -C "$AGENT_MAIL_SKILL_DIR" real-test` before deployment. It starts a real temporary PostgreSQL cluster and exercises both the JSON HTTP API and the MCP endpoint over localhost.

The public smoke mutates production and leaves durable test artifacts. Run `make -C "$AGENT_MAIL_SKILL_DIR" public-mcp-smoke` only after explicit authorization, with `AGENT_MAIL_TOKEN`, `PUBLIC_IP`, and `AGENT_MAIL_ALLOW_PRODUCTION_MUTATION=YES` set. It exercises the public `https://agent-mail.cc/mcp` endpoint through Cloudflare/nginx, including the SSE notification stream and port-isolation gate.

Check the deployed service:

```bash
curl -fsS https://agent-mail.cc/ready
```

## MCP

The remote MCP endpoint is:

```text
https://agent-mail.cc/mcp
```

Codex should install it by URL, not by building a local shim:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

The Codex process must have `AGENT_MAIL_TOKEN` in its environment before it starts. Existing long-running Codex sessions may not discover a newly installed MCP server until restarted.

MCP uses the service-admin bearer on every request. `POST /mcp` handles JSON-RPC requests, `GET /mcp` is the SSE stream used for `notifications/resources/updated`, and `DELETE /mcp` terminates a session. Inbox and message resource identities must match the participant bound by `agent_mail_start`.

MCP tools are only for mutations or session setup:

- `agent_mail_start(role)`: generate and bind this MCP session's participant identity.
- `agent_mail_project_add(alias, root?)`: create or update a project namespace.
- `agent_mail_send(project, to, subject, body)`: send from the session-bound identity.
- `agent_mail_mark_read(project, mail_id)`: explicitly mark a delivered message read.

Inbox and message reads are MCP resources, not tools:

```text
agent-mail://projects
agent-mail://projects/{alias}/inbox?identity={identity}
agent-mail://projects/{alias}/messages/{mail_id}?identity={identity}
```

Clients can subscribe to the inbox and message resources. New mail and explicit read-state changes emit `notifications/resources/updated`; subscriptions are live MCP hints, not a durable queue.

## Privileged HTTP API

`GET /live` checks only the process. `GET /health` and `GET /ready` check PostgreSQL readiness. All other endpoints require a bearer credential.

Administrative endpoints use:

```text
Authorization: Bearer $AGENT_MAIL_TOKEN
```

The Rust server requires a non-empty service-admin token at startup; missing or empty `AGENT_MAIL_TOKEN` is a configuration error. Treat it as a privileged credential: it can create participants and projects and list administrative metadata. Do not distribute it as a participant credential.

Create or activate a participant:

```http
POST /v1/participants/start
{ "identity": "reviewer-001", "role": "reviewer" }
```

`identity` is optional. Omit it to generate a readable identity. The response includes `participant_token` exactly once. Persist it only when later processes must reuse the identity, in a private file owned by the user with mode `0600`; never print or log it. A duplicate explicit identity returns `409` and does not recover its token.

For a controlled upgrade from the legacy shared-token HTTP model, configure a separate temporary `AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN` and call `POST /v1/participants/{identity}/credential` with that credential. It must differ from `AGENT_MAIL_TOKEN`; the server rejects equal values at startup. The response returns a new one-time `participant_token` and atomically revokes any prior participant token. Never use `AGENT_MAIL_TOKEN` for this route. Remove `AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN` from the server after migration or planned credential rotation.

Add project namespaces before sending or reading mail:

```http
POST /v1/projects
{ "alias": "flow", "root": "/path/to/flow" }
```

`root` is optional metadata. Mail is stored in PostgreSQL, not in the project directory.

Participant send/read operations use `Authorization: Bearer $PARTICIPANT_TOKEN`, not the service-admin token. Send mail:

```http
POST /v1/messages
{
  "project": "flow",
  "to_kind": "role",
  "to": "reviewer",
  "subject": "Review result",
  "body": "Ready for review.",
  "idempotency_key": "answer:mail-20260712-001"
}
```

The server derives `sender_identity` from the participant token. A supplied, mismatched sender is rejected. `idempotency_key` is optional and may contain at most 128 ASCII letters, numbers, dashes, underscores, dots, and colons. Its uniqueness scope is authenticated participant plus project. Retrying the same key with the same resolved recipient, subject, and body returns the original message with the same ID and timestamp and creates no second delivery. Reusing the key in that project with different content returns `409 Conflict`. Use a deterministic key for operations that must survive response loss, such as an answer keyed by its original question ID.

`to_kind` may be `identity`, `role`, or `broadcast`. If omitted, `all-agents` becomes a broadcast, a known participant identity becomes identity-addressed mail, and any other valid address becomes role-addressed mail.

Read unread mail for a participant:

```http
GET /v1/projects/{project}/participants/{identity}/inbox?limit=100&cursor={cursor}
```

HTTP inboxes use ascending keyset pagination by creation nanoseconds and message ID. `limit` is optional, defaults to `100`, and must be between `1` and `200`. `cursor` is an optional opaque string returned by the previous page; pass it back unchanged and never construct or parse it. The response keeps `project`, `identity`, `role`, `unread_count`, and `messages`; `unread_count` is the total unread count across the inbox, while `messages` contains only the current page. `next_cursor` is present only when another page exists. Omitting both query parameters remains compatible for inboxes of up to 100 unread messages; larger inboxes require following `next_cursor`.

Read a full delivered message body:

```http
GET /v1/projects/{project}/messages/{mail_id}?identity={identity}
```

Mark a delivered message read:

```http
POST /v1/projects/{project}/messages/{mail_id}/read
{ "identity": "reviewer-001" }
```

## Data Model

- participant: concrete identity plus role
- project: namespace alias
- recipient kind: `identity`, `role`, or `broadcast`
- broadcast recipient: `all-agents`
- read state: per participant identity
- message bodies: readable only for delivered mail
- HTTP participant identity: derived from a one-time participant token; path/query/body identities must match it
- HTTP send idempotency: optional key, unique per participant and project, with exact-payload replay

Role names such as `reviewer`, `worker/frontend`, and `main-orchestrator` are examples, not built-in semantics.

Messages are not locks, claims, or exclusive assignments. Treat them as durable coordination records.

## Deployment

The Lightsail deployment uses:

- Rust `agent-mail-server`
- private AWS RDS PostgreSQL
- bearer-token authentication
- Cloudflare-proxied HTTPS at `https://agent-mail.cc`
- nginx on the instance proxying HTTPS traffic to `127.0.0.1:8787`
- public instance ports `80` and `443`; no public `8787`

Read [docs/lightsail.md](docs/lightsail.md) before deployment for the infrastructure shape, environment, and validation gate.

## Safety Rules

- Do not store secrets, raw environment dumps, `.flow/events/`, or sensitive brainstorming unless confirmed.
- Do not run `public-mcp-smoke` without explicit live-mutation authorization; it creates persistent production records and has no automatic server-side cleanup.
- Keep participant tokens in memory or a user-owned `0600` state file only. Never include them in mail, logs, errors, command output, or shared artifacts.
- Keep the separate credential-administration token unset except during an authorized migration or rotation window; rotating a participant token immediately revokes the previous token.
- Do not assume HTTP reads mark messages read.
- Use `mark_read` explicitly for read-state changes.
