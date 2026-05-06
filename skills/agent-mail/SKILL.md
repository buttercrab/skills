---
name: agent-mail
description: Use the Rust/PostgreSQL Agent Mail service for durable cross-agent instructions, handoffs, blockers, decisions, and status messages in project mailboxes. Use when Codex needs Agent Mail participants, project namespaces, cross-project mail, participant inboxes, MCP resources, or the deployed HTTP mailbox service.
---

# Agent Mail

Agent Mail is a Rust HTTP mailbox service backed by PostgreSQL. It also exposes a remote MCP Streamable HTTP endpoint. Use it for durable cross-session coordination, not routine logs or locks.

The supported v1 runtime is the Rust `agent-mail-server` with PostgreSQL. The deployed service runs on a Lightsail Nano app host in `us-west-2` against private AWS RDS PostgreSQL and is reached at:

```text
https://agent-mail.cc
```

Use `https://agent-mail.cc` as the default `AGENT_MAIL_URL` for clients. The public edge is Cloudflare-proxied HTTPS on `agent-mail.cc`; nginx on the Lightsail Nano instance terminates the Cloudflare origin certificate and proxies to the Rust server on `127.0.0.1:8787`. Port `8787` is private and should not be exposed publicly.

Build the server:

```bash
make -C skills/agent-mail build
```

Run the server against PostgreSQL:

```bash
skills/agent-mail/target/debug/agent-mail-server \
  --database-url "$AGENT_MAIL_DATABASE_URL" \
  --bind 127.0.0.1:8787 \
  --token "$AGENT_MAIL_TOKEN"
```

Use `make real-test` before deployment. It starts a real temporary PostgreSQL cluster and exercises both the JSON HTTP API and the MCP endpoint over localhost.

Use `make public-mcp-smoke` after deployment with `AGENT_MAIL_TOKEN` set. It exercises the public `https://agent-mail.cc/mcp` endpoint through Cloudflare/nginx, including the SSE notification stream.

Check the deployed service:

```bash
curl -fsS https://agent-mail.cc/health
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

MCP uses bearer authentication on every request. `POST /mcp` handles JSON-RPC requests and `GET /mcp` is the SSE stream used for `notifications/resources/updated`.

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

## HTTP API

All endpoints except `GET /health` require:

```text
Authorization: Bearer $AGENT_MAIL_TOKEN
```

The Rust server requires a token at startup; missing `AGENT_MAIL_TOKEN` is a configuration error.

Create or activate a participant:

```http
POST /v1/participants/start
{ "identity": "reviewer-001", "role": "reviewer" }
```

`identity` is optional. Omit it to generate a readable identity.

Add project namespaces before sending or reading mail:

```http
POST /v1/projects
{ "alias": "flow", "root": "/path/to/flow" }
```

`root` is optional metadata. Mail is stored in PostgreSQL, not in the project directory.

Send mail:

```http
POST /v1/messages
{
  "sender_identity": "sender-001",
  "project": "flow",
  "to_kind": "role",
  "to": "reviewer",
  "subject": "Review result",
  "body": "Ready for review."
}
```

`to_kind` may be `identity`, `role`, or `broadcast`. If omitted, `all-agents` becomes a broadcast, a known participant identity becomes identity-addressed mail, and any other valid address becomes role-addressed mail.

Read unread mail for a participant:

```http
GET /v1/projects/{project}/participants/{identity}/inbox
```

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

See `docs/lightsail.md` for the deployment shape and validation gate.

## Safety Rules

- Do not store secrets, raw environment dumps, `.flow/events/`, or sensitive brainstorming unless confirmed.
- Do not assume HTTP reads mark messages read.
- Use `mark_read` explicitly for read-state changes.
