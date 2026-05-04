# Front Agent Orchestration

Front Agent pairs a human-facing gateway agent with a separate main implementation agent. It uses the Rust/PostgreSQL Agent Mail HTTP service for durable mail and stores only local runtime state under `.front-agent/`.

## Requirements

```bash
export AGENT_MAIL_URL=https://agent-mail.cc
export AGENT_MAIL_TOKEN=...
```

## Build And Test

```bash
go test ./... -count=1 -timeout=30s
FRONT_AGENT_MAIL_BACKEND=memory scripts/smoke_front_agent_protocol.sh
```

## Use

```bash
scripts/front-agent main --root <project-root>
scripts/front-agent gateway <main-identity> --root <project-root>
scripts/front-agent listen --identity <id> --root <project-root>
scripts/front-agent send "Subject" --identity <id> --root <project-root>
```

See `SKILL.md` and `references/protocol.md` for the protocol rules.
