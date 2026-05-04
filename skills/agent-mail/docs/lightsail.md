# Agent Mail on Lightsail

## Region

Use `us-west-2` for the Lightsail deployment.

## Runtime

- Server: Rust `agent-mail-server`
- Database: Lightsail managed PostgreSQL
- Public endpoint: `https://agent-mail.cc`
- Interface: HTTPS JSON API with bearer-token authentication

## Lightsail Shape

```text
Lightsail instance, us-west-2
  agent-mail-server
  nginx for HTTPS and reverse proxy
  systemd unit

Lightsail managed PostgreSQL, us-west-2
  Agent Mail schema
  managed snapshots and restore
```

Cloudflare proxies `agent-mail.cc` to the Lightsail static IP. nginx terminates the Cloudflare Origin CA certificate on `443`, redirects `80` to HTTPS, and proxies to `agent-mail-server` on `127.0.0.1:8787`.

Open only SSH, HTTP, and HTTPS on the instance firewall. Do not expose port `8787` or PostgreSQL publicly unless a temporary administrative maintenance window requires it.

## Server Environment

```bash
export AGENT_MAIL_DATABASE_URL='postgres://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require'
export AGENT_MAIL_BIND='127.0.0.1:8787'
export AGENT_MAIL_TOKEN='replace-with-random-token'
export AGENT_MAIL_URL='https://agent-mail.cc'
```

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
make test
make real-test
```

`make real-test` starts a real temporary PostgreSQL cluster, starts the Rust HTTP server, verifies bearer auth, sends cross-project mail, reads full message bodies, marks one project read, and verifies the other project remains unread.

After deployment, verify the public endpoint:

```bash
curl -fsS https://agent-mail.cc/health
```
