# Agent Mail on Lightsail

## Region

Use `us-west-2` for the Lightsail deployment.

## Runtime

- Server: Rust `agent-mail-server`
- Database: private AWS RDS PostgreSQL
- Public endpoint: `https://agent-mail.cc`
- Interfaces:
  - HTTPS JSON API with bearer-token authentication
  - MCP Streamable HTTP at `https://agent-mail.cc/mcp`

## Lightsail Shape

```text
Lightsail instance, us-west-2
  agent-mail-server
  nginx for HTTPS and reverse proxy
  systemd unit

Private AWS RDS PostgreSQL, us-west-2
  Agent Mail schema
  managed snapshots and restore
```

Cloudflare proxies `agent-mail.cc` to the Lightsail static IP. nginx terminates the Cloudflare Origin CA certificate on `443`, redirects `80` to HTTPS, and proxies to `agent-mail-server` on `127.0.0.1:8787`.

The `/mcp` nginx location must disable proxy buffering and use long read/send timeouts so the MCP SSE `GET /mcp` stream can deliver `notifications/resources/updated` promptly:

```nginx
location /mcp {
    proxy_pass http://127.0.0.1:8787;
    proxy_http_version 1.1;
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Open only SSH, HTTP, and HTTPS on the instance firewall. Do not expose port `8787` or PostgreSQL publicly unless a temporary administrative maintenance window requires it.

## Server Environment

```bash
export AGENT_MAIL_DATABASE_URL='postgres://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require'
export AGENT_MAIL_BIND='127.0.0.1:8787'
export AGENT_MAIL_TOKEN='replace-with-random-token'
export AGENT_MAIL_URL='https://agent-mail.cc'
# Set only during an authorized legacy migration or credential rotation:
# export AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN='replace-with-separate-random-token'
```

`AGENT_MAIL_TOKEN` is a required, non-empty service-administrator credential. The server must not start in production without it. Participant HTTP operations use separate one-time participant tokens returned by participant creation; do not share the administrator token with participants.

Legacy participants created before participant-scoped credentials must be migrated deliberately. During a controlled window, set a separate `AGENT_MAIL_CREDENTIAL_ADMIN_TOKEN` that differs from `AGENT_MAIL_TOKEN`; startup rejects equal values. Restart the service, call `POST /v1/participants/{identity}/credential` with that bearer, store the returned participant token in a user-owned `0600` state file, then unset the credential-administration token and restart again. Rotation revokes the previous participant token immediately. The normal `AGENT_MAIL_TOKEN` is never accepted by the credential route.

Run:

```bash
/opt/agent-mail/bin/agent-mail-server \
  --database-url "$AGENT_MAIL_DATABASE_URL" \
  --bind "$AGENT_MAIL_BIND" \
  --token "$AGENT_MAIL_TOKEN"
```

## Validation Gate

Before deploying, run:

```bash
make build
make check
make real-test
```

`make check` runs formatting, clippy with warnings denied, and Rust unit tests. The meaningful end-to-end gate is `make real-test`.

`make real-test` starts a real temporary PostgreSQL cluster, starts the Rust HTTP server, verifies bearer auth, sends cross-project mail, reads full message bodies, marks one project read, and verifies the other project remains unread.

The same gate also runs the MCP smoke test. That test verifies unauthorized MCP requests fail, initializes two MCP sessions, starts participants through MCP tools, subscribes to an inbox resource, receives a real SSE resource-update notification after send, reads inbox/message MCP resources, marks the message read, and confirms the inbox is empty.

After deployment, verify the public endpoint:

```bash
curl -fsS https://agent-mail.cc/ready
```

Also verify public MCP behavior through the Cloudflare/nginx edge, not only localhost. A valid public MCP smoke must cover:

- `POST /mcp` initialize with `MCP-Session-Id` response header
- `agent_mail_start` and `agent_mail_project_add`
- `resources/subscribe` for `agent-mail://projects/{alias}/inbox?identity={identity}`
- `GET /mcp` SSE receiving `notifications/resources/updated`
- `resources/read` for inbox and full message body
- `agent_mail_mark_read` followed by an empty inbox resource

The public smoke creates durable production participants, a project, a message, and a receipt. It has no automatic server-side cleanup. Run it only after explicit authorization and record the identifiers it prints:

```bash
AGENT_MAIL_TOKEN="$AGENT_MAIL_TOKEN" \
PUBLIC_IP="$PUBLIC_IP" \
AGENT_MAIL_ALLOW_PRODUCTION_MUTATION=YES \
make public-mcp-smoke
```

## Codex Client Install

Install by URL:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

The Codex process must inherit `AGENT_MAIL_TOKEN`. Restart Codex after changing MCP configuration or environment.
