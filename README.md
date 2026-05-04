# Skills

This repository contains authored Codex skills and their implementation code.

## Skills

- `skills/agent-mail` - Rust/PostgreSQL Agent Mail service and deployment docs.
- `skills/front-agent-orchestration` - Human-facing gateway and main-agent orchestration protocol over Agent Mail.

## Repository Layout

- `skills/` - skill source directories.
- `.env/` - local deployment environment, credentials, SSH keys, and certificates. This directory is intentionally gitignored.
- `install.sh` - links repo skills into `~/.agents/skills`.

## Install

```bash
./install.sh
```

The install script links included skills into `~/.agents/skills`.

## Validate

```bash
make -C skills/agent-mail test
make -C skills/agent-mail real-test
(cd skills/front-agent-orchestration && go test ./... -count=1 -timeout=30s)
(cd skills/front-agent-orchestration && scripts/smoke_front_agent_protocol.sh)
```

Agent Mail deployment secrets and operational state live under `.env/agent-mail/` in this repository and are not tracked.
