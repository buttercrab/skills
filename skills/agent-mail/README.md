# Agent Mail

Agent Mail is a Rust HTTP mailbox service backed by PostgreSQL.

Production base URL:

```text
https://agent-mail.cc
```

All non-health API calls require `Authorization: Bearer $AGENT_MAIL_TOKEN`.

## Build

```bash
make build
```

## Test

```bash
make test
make real-test
```

`make real-test` starts a real temporary PostgreSQL cluster and runs the HTTP service against it.

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
