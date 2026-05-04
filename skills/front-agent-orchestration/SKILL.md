---
name: front-agent-orchestration
description: Use when a human should work through a human-facing gateway agent while a separate main agent performs implementation through validated two-way Agent Mail messages.
---

# Front Agent Orchestration

Front Agent runs a paired two-session workflow:

```text
Human <-> Gateway Agent <-> front-agent protocol <-> Agent Mail HTTP <-> Main Agent
```

Agent Mail is the durable mailbox. Front Agent is the application protocol on top of it. Mail is stored in the Agent Mail PostgreSQL service; local `.front-agent/` files are only pairing state, locks, logs, and a small sent-message validation cache.

Required environment for real mail:

```bash
export AGENT_MAIL_URL=https://agent-mail.cc
export AGENT_MAIL_TOKEN=...
```

For local protocol tests only, `FRONT_AGENT_MAIL_BACKEND=memory` uses an in-process mailbox.

## Commands

```bash
scripts/front-agent main [--root <path>]
scripts/front-agent gateway <main-identity> [--root <path>] [--timeout 24h]
scripts/front-agent listen [--root <path>] [--identity <id>] [--timeout 24h] [--stream]
scripts/front-agent send "Subject" [--root <path>] [--identity <id>] [--responds-to <message-id>]
scripts/front-agent state [--root <path>] [--identity <id>]
```

`send` reads a fenced YAML body from stdin. Use `--` before a subject that starts with `-`.

## Pairing

Main starts first:

```bash
scripts/front-agent main --root <project-root>
```

Main prints a gateway command and starts a detached pairing waiter. The gateway runs the printed command with the same root:

```bash
scripts/front-agent gateway <main-id> --root <project-root>
```

After pairing, main immediately runs:

```bash
scripts/front-agent listen --identity <main-id> --root <project-root>
```

Gateway should return control to the human after pairing. At the start of each human-facing turn, gateway drains pending main messages with:

```bash
scripts/front-agent listen --timeout 0 --identity <gateway-id> --root <project-root>
```

## Message Body

All non-ready messages are fenced YAML mappings.

Main to gateway:

```yaml
method: question
from_role: main
to_role: gateway
summary: "Need a product decision."
question: "Which behavior should invalid input use?"
```

Gateway to main:

```yaml
method: answer
from_role: gateway
to_role: main
summary: "Decision confirmed."
human_confirmed: true
answer: "Reject invalid input with inline validation."
```

Allowed methods:

- Main may send `update`, `question`, or `note`.
- Gateway may send `work`, `answer`, or `note`.
- Gateway-originated messages require `human_confirmed: true`.
- `answer` requires `--responds-to <question-id>`.

## Operating Rules

- Main and gateway must use the same `--root`.
- If multiple front-agent states exist, pass `--identity`.
- Pairing is tokenless. Old `--token` commands are invalid.
- Gateway must fail fast if no live main pairing waiter exists.
- Do not repair protocol state with raw Agent Mail. Use `front-agent` commands.
- `listen` validates sender, peer, role direction, method, freshness, and fenced YAML before printing messages. Invalid messages are rejected and marked read.
- `listen` is single-owner per identity and fails if another live listener owns the identity.
- Use one-shot `listen` as the notification boundary. `--stream` is for deliberate debugging.
