---
name: front-agent-orchestration
description: Use when a human needs a dedicated gateway agent while a separate main agent implements work through validated two-way Agent Mail messages. Do not use for ordinary built-in subagent delegation or direct Agent Mail workflows that do not need a human approval gateway.
---

# Front Agent Orchestration

Front Agent runs a paired two-session workflow:

```text
Human <-> Gateway Agent <-> front-agent protocol <-> Agent Mail HTTP <-> Main Agent
```

Agent Mail is the durable mailbox. Front Agent is the application protocol on top of it. Mail is stored in the Agent Mail PostgreSQL service. Local `.front-agent/` files contain private pairing state, participant credentials, locks, logs, a bounded question-validation cache, and answer-deduplication state. The CLI creates `.front-agent/.gitignore`; never publish or copy this runtime directory.

Required environment for real mail:

```bash
export AGENT_MAIL_URL=https://agent-mail.cc
export AGENT_MAIL_TOKEN=...
```

For local tests only, `FRONT_AGENT_MAIL_BACKEND=memory` uses an in-process mailbox. Add `FRONT_AGENT_MEMORY_SHARED=1` for subprocess tests that need a process-shared mailbox under the temporary root. Never use either memory mode for real work.

## Commands

Resolve the absolute directory containing this loaded `SKILL.md`, then set `FRONT_AGENT` to its launcher. Do not resolve `scripts/front-agent` from the user's current project:

```bash
FRONT_AGENT="<front-agent-orchestration-skill-dir>/scripts/front-agent"
```

```bash
"$FRONT_AGENT" main [--root <path>]
"$FRONT_AGENT" gateway <main-identity> [--root <path>] [--timeout 24h]
"$FRONT_AGENT" listen [--root <path>] [--identity <id>] [--timeout 24h] [--stream]
"$FRONT_AGENT" send "Subject" [--root <path>] [--identity <id>] [--responds-to <message-id>]
"$FRONT_AGENT" state [--root <path>] [--identity <id>]
```

`send` reads a fenced YAML body from stdin. Use `--` before a subject that starts with `-`.

## Pairing

Main starts first:

```bash
"$FRONT_AGENT" main --root <project-root>
```

Main prints a gateway command and starts a detached pairing waiter. The gateway runs the printed command with the same root:

```bash
"$FRONT_AGENT" gateway <main-id> --root <project-root>
```

Main checks pairing completion with `state`; wait until `pairing_state` is `paired`, then immediately run:

```bash
"$FRONT_AGENT" listen --identity <main-id> --root <project-root>
```

Gateway should return control to the human after pairing. At the start of each human-facing turn, gateway drains pending main messages with:

```bash
"$FRONT_AGENT" listen --timeout 0 --identity <gateway-id> --root <project-root>
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
- `question` requires a non-empty `question`; `answer` requires a non-empty `answer`.
- `update` requires one status: `accepted`, `progress`, `blocked`, `complete`, `failed`, or `cancelled`.

## Human Approval Gate

Before gateway sends `work`, `answer`, or `note`, it must inspect the relevant repository context for nontrivial requests, present a plain-language intent or decision preview, and wait for explicit human approval of that exact scope. Only then may it set `human_confirmed: true`. Silence, an inferred preference, a timeout default, or approval of an earlier scope does not count. If the human changes scope, present the revised preview and obtain approval again.

Main reports completion, failure, or cancellation with `method: update` and the matching terminal status. Gateway relays the useful result to the human and stops the paired workflow after a terminal update unless the human explicitly approves new work.

## Operating Rules

- Main and gateway must use the same `--root`.
- If multiple front-agent states exist, pass `--identity`.
- Pairing is tokenless. Old `--token` commands are invalid.
- Gateway must fail fast if no live main pairing waiter exists.
- Do not repair protocol state with raw Agent Mail. Use `front-agent` commands.
- `listen` validates sender, peer, role direction, method, freshness, and fenced YAML before printing messages. Invalid messages are rejected and marked read.
- `listen` is single-owner per identity and fails if another live listener owns the identity.
- Use one-shot `listen` as the notification boundary. `--stream` is for deliberate debugging.
- Treat delivery as at-least-once: if output or acknowledgement fails, rerun `listen` and deduplicate by message ID.
- HTTP sends persist a stable idempotency key before the first attempt and reuse it after ambiguous failures. After output succeeds, an intentional identical non-response packet starts a new logical send; response packets remain unique by `responds_to`. Never delete idempotency state merely to force a retry.
- HTTP inbox polling requests 100-message pages, follows at most 10 opaque cursors per poll, caps response bodies, and applies one outer deadline to project, page, and message requests. If the scan bound is reached, drain or archive unrelated unread mail before retrying.

## Resources

- Read [references/protocol.md](references/protocol.md) before changing message, pairing, lifecycle, or security behavior.
- Read [references/examples.md](references/examples.md) when composing protocol packets.
- Use [references/forward-tests.md](references/forward-tests.md) for fresh-agent or release verification; do not run live Agent Mail checks without explicit authorization.
