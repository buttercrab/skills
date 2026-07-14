# Front Agent Orchestration

Front Agent pairs a human-facing gateway agent with a separate main implementation agent. It uses the Rust/PostgreSQL Agent Mail HTTP service for durable mail and stores only local runtime state under `.front-agent/`.

## Requirements

Go 1.22 or newer is required. `scripts/front-agent` always runs the current source, so a stale generated binary can never shadow repository changes.

```bash
export AGENT_MAIL_URL=https://agent-mail.cc
export AGENT_MAIL_TOKEN=...
```

## Build And Test

```bash
go test ./... -count=1 -timeout=30s
scripts/smoke_front_agent_protocol.sh
```

The smoke is always offline: it builds a fresh binary, uses a process-shared local mailbox, cleans up its detached waiter, and never loads credentials or contacts Agent Mail. Live integration checks require a separately authorized test plan.

## Use

```bash
scripts/front-agent main --root <project-root>
scripts/front-agent gateway <main-identity> --root <project-root>
scripts/front-agent listen --identity <id> --root <project-root>
scripts/front-agent listen --timeout 0 --identity <gateway-id> --root <project-root>
scripts/front-agent send "Subject" --identity <id> --root <project-root>
```

The CLI stores participant credentials with mode `0600` below the private, git-ignored `.front-agent/` runtime directory. Do not publish that directory.

See `SKILL.md` and `references/protocol.md` for the protocol rules.
