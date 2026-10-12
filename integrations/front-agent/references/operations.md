> Legacy Agent Mail gateway runtime documentation. This is not the native-subagent responsive coordinator. Any `$front-agent-orchestration` examples describe the retired entrypoint; use `../OPERATIONS.md` and the preserved CLI for maintenance. Align helpers are in `../../../legacy/align-work/` relative to this reference directory.

# Front Agent Operations

## Requirements and launcher behavior

Go 1.22 or newer is required. `scripts/front-agent` builds and runs the current source in a private cache; a stale generated `scripts/front-agent-bin` never shadows repository changes.

Real mail requires `AGENT_MAIL_URL` and `AGENT_MAIL_TOKEN`. Local verification must use the memory backend described in the entrypoint and must not load real credentials.

## Build and offline verification

Run from the runtime directory:

```bash
go test ./... -count=1 -timeout=60s
scripts/smoke_front_agent_protocol.sh
```

The smoke is offline. It builds a fresh binary, uses a process-shared local mailbox, cleans up its detached waiter, and never contacts Agent Mail. Live integration checks require a separately authorized plan.

## Runtime state

The CLI stores participant credentials with mode `0600` below the private `.front-agent/` directory and writes a local `.gitignore` there. Never publish, copy, or reuse that runtime directory across repository roots. Resolve the launcher from the loaded skill directory, not from the user's current working directory.
