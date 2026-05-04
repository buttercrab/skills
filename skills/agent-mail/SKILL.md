---
name: agent-mail
description: Use the Rust/PostgreSQL Agent Mail service for durable cross-agent instructions, handoffs, blockers, decisions, and status messages in project mailboxes. Use when Codex needs Agent Mail participants, project namespaces, cross-project mail, participant inboxes, or the deployed HTTP mailbox service.
---

# Agent Mail

Agent Mail is a Rust HTTP mailbox service backed by PostgreSQL. Use it for durable cross-session coordination, not routine logs or locks.

The supported v1 runtime is the Rust `agent-mail-server` with PostgreSQL. The deployed Lightsail service runs in `us-west-2` against Lightsail managed PostgreSQL and is reached at:

```text
https://agent-mail.cc
```

Use `https://agent-mail.cc` as the default `AGENT_MAIL_URL` for clients. The public edge is Cloudflare-proxied HTTPS on `agent-mail.cc`; nginx on the Lightsail instance terminates the Cloudflare origin certificate and proxies to the Rust server on `127.0.0.1:8787`. Port `8787` is private and should not be exposed publicly.

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

Use `make real-test` before deployment. It starts a real temporary PostgreSQL cluster and exercises the Rust HTTP server over localhost.

Check the deployed service:

```bash
curl -fsS https://agent-mail.cc/health
```

## HTTP API

All endpoints except `GET /health` require:

```text
Authorization: Bearer $AGENT_MAIL_TOKEN
```

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
- Lightsail managed PostgreSQL
- bearer-token authentication
- Cloudflare-proxied HTTPS at `https://agent-mail.cc`
- nginx on the instance proxying HTTPS traffic to `127.0.0.1:8787`
- public instance ports `80` and `443`; no public `8787`

See `docs/lightsail.md` for the deployment shape and validation gate.

## Safety Rules

- Do not store secrets, raw environment dumps, `.flow/events/`, or sensitive brainstorming unless confirmed.
- Do not assume HTTP reads mark messages read.
- Use `mark_read` explicitly for read-state changes.
