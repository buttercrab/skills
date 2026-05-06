# Agent Mail

Agent Mail is a Rust/PostgreSQL mailbox service with a JSON HTTP API and a remote MCP Streamable HTTP endpoint.

Production base URL:

```text
https://agent-mail.cc
```

All non-health API calls require `Authorization: Bearer $AGENT_MAIL_TOKEN`.
The server requires `AGENT_MAIL_TOKEN` at startup.

MCP endpoint:

```text
https://agent-mail.cc/mcp
```

Codex MCP install:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

Set `AGENT_MAIL_TOKEN` before starting Codex. Long-running Codex sessions may need restart before newly installed MCP tools/resources are visible.

## Build

```bash
make build
```

## Test

```bash
make test
make real-test
make public-mcp-smoke
```

`make test` is the Rust compile/unit-test gate. It currently has no Rust unit tests.

`make real-test` starts a real temporary PostgreSQL cluster and runs both the HTTP and MCP smoke tests against it.

`make mcp-test` runs the real PostgreSQL MCP smoke test. It verifies bearer auth, MCP session IDs, tool calls, resource reads, SSE subscription notification, and explicit read-state changes.

`make public-mcp-smoke` verifies the deployed `https://agent-mail.cc/mcp` endpoint through Cloudflare/nginx, including SSE resource notifications.

## Run

```bash
agent-mail-server \
  --database-url "$AGENT_MAIL_DATABASE_URL" \
  --bind "$AGENT_MAIL_BIND" \
  --token "$AGENT_MAIL_TOKEN"
```

## Deployment State

Local deployment environment, SSH keys, and Cloudflare origin certificates live in the repo-local ignored directory:

```text
../../.env/agent-mail/
```

The tracked deployment notes are in `docs/lightsail.md`.

## MCP Model

MCP mutations are tools:

- `agent_mail_start(role)`
- `agent_mail_project_add(alias, root?)`
- `agent_mail_send(project, to, subject, body)`
- `agent_mail_mark_read(project, mail_id)`

MCP reads are resources:

- `agent-mail://projects`
- `agent-mail://projects/{alias}/inbox?identity={identity}`
- `agent-mail://projects/{alias}/messages/{mail_id}?identity={identity}`

Subscribe to inbox/message resources to receive `notifications/resources/updated` on the SSE `GET /mcp` stream.
