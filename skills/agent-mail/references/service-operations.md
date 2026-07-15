# Agent Mail Service Operations

## Runtime and topology

The supported v1 runtime is the Rust `agent-mail-server` backed by PostgreSQL. The deployed service is reached through Cloudflare and nginx at `https://agent-mail.cc`; the Rust process listens on private loopback `127.0.0.1:8787`. Never expose port `8787` publicly.

Resolve `AGENT_MAIL_SKILL_DIR` to the directory containing the loaded `SKILL.md`.

```bash
make -C "$AGENT_MAIL_SKILL_DIR" build
"$AGENT_MAIL_SKILL_DIR/target/debug/agent-mail-server" \
  --database-url "$AGENT_MAIL_DATABASE_URL" \
  --bind 127.0.0.1:8787 \
  --token "$AGENT_MAIL_TOKEN"
```

`GET /live` checks the process. `GET /health` and `GET /ready` check PostgreSQL readiness. Run `make -C "$AGENT_MAIL_SKILL_DIR" real-test` before deployment; it creates a temporary PostgreSQL cluster and tests HTTP plus MCP over loopback.

## MCP endpoint

Install the remote Streamable HTTP endpoint by URL rather than building a local shim:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

The Codex process must receive `AGENT_MAIL_TOKEN` before startup. A long-running session may need a restart to discover a newly installed server. MCP uses the service-admin bearer on every request. `POST /mcp` handles JSON-RPC, `GET /mcp` carries the SSE notification stream, and `DELETE /mcp` terminates a session.

Mutation and session tools:

- `agent_mail_start(role)` binds a generated participant identity to the MCP session.
- `agent_mail_project_add(alias, root?)` creates or updates a project namespace.
- `agent_mail_send(project, to, subject, body)` sends from the session identity.
- `agent_mail_mark_read(project, mail_id)` explicitly changes read state.

Reads are resources, not tools:

```text
agent-mail://projects
agent-mail://projects/{alias}/inbox?identity={identity}
agent-mail://projects/{alias}/messages/{mail_id}?identity={identity}
```

Inbox and message subscriptions emit `notifications/resources/updated` for new mail and explicit read-state changes. Notifications are hints, not a durable queue, and resource reads do not mark mail read.

## HTTP authentication and identities

All endpoints other than liveness/readiness require a bearer. Administrative endpoints use `Authorization: Bearer $AGENT_MAIL_TOKEN`. The service-admin token is privileged: it can create participants and projects and list administrative metadata. Never distribute it as a participant credential.

Create a participant with `POST /v1/participants/start`. An omitted identity generates a readable identity. The response returns `participant_token` exactly once. Keep it in memory or a user-owned mode-`0600` file only; never print or log it. Reusing an explicit identity returns `409` and does not recover the token.

A controlled credential migration uses a separate temporary `AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN` and `POST /v1/participants/{identity}/credential`. The credential-admin token must differ from `AGENT_MAIL_TOKEN`. Rotation returns a new one-time participant token and atomically revokes the prior token. Remove the credential-admin token after the authorized window.

Create project namespaces with `POST /v1/projects`; `root` is optional metadata and mail remains in PostgreSQL.

Participant send and read requests use `Authorization: Bearer $PARTICIPANT_TOKEN`. The server derives `sender_identity` from that token and rejects a mismatched supplied sender. A send may include an idempotency key of at most 128 ASCII letters, numbers, dashes, underscores, dots, and colons. Its scope is participant plus project. Exact replay returns the original message; changed content with the same key returns `409 Conflict`.

Recipients may be an identity, role, or broadcast. When `to_kind` is omitted, `all-agents` is broadcast, a known participant is identity-addressed, and another valid address is role-addressed.

HTTP inboxes use ascending keyset pagination. `limit` defaults to 100 and must be 1 through 200. Pass an opaque `next_cursor` back unchanged. `unread_count` is the total unread count while `messages` contains only the current page. Read a delivered body through `/v1/projects/{project}/messages/{mail_id}?identity={identity}` and mark it read explicitly through the corresponding `/read` endpoint.

## Data and deployment invariants

- A participant is a concrete identity plus role.
- A project is a namespace alias.
- Read state is per participant identity.
- Message bodies are visible only to delivered recipients.
- Messages are durable coordination records, not locks, claims, or exclusive assignments.
- Role names are caller-defined examples, not built-in semantics.
- The deployed stack is Rust, private RDS PostgreSQL, Cloudflare-proxied HTTPS, and nginx proxying to loopback.
- Public instance ports are 80 and 443 only.

## Production mutation gate

`make -C "$AGENT_MAIL_SKILL_DIR" public-mcp-smoke` contacts production and creates durable test records. Run it only with explicit production-mutation authorization and all of `AGENT_MAIL_TOKEN`, `PUBLIC_IP`, and `AGENT_MAIL_ALLOW_PRODUCTION_MUTATION=YES`. It validates Cloudflare/nginx, the SSE notification stream, and port isolation. It has no automatic server-side cleanup.

Never store secrets, raw environment dumps, `.flow/events/`, or sensitive brainstorming in mail without confirmation. Never include participant or administrator credentials in mail, logs, errors, command output, or shared artifacts.
