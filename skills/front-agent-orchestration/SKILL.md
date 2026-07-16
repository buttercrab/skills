---
name: front-agent-orchestration
description: Use when the user explicitly requests a dedicated human-facing gateway while a separate main agent implements work through validated two-way Agent Mail messages. Front owns the gateway conversation and protocol transport only; the main independently classifies align-work, audit-technical-work, or native authority, and Align exclusively owns any planning packet. Do not use for routine built-in subagent delegation or direct Agent Mail workflows. If the required Front or Agent Mail capability is unavailable, stop; use built-in collaboration only after the user approves that architecture change.
---

# Front Agent Orchestration

Front Agent runs a paired two-session workflow:

```text
Human <-> Gateway Agent <-> front-agent protocol <-> Agent Mail HTTP <-> Main Agent
```

Front owns the human-facing gateway and protocol transport. It does not own planning packets or implementation authority. The main agent independently classifies the original request and canonical repository state into `align-work`, `audit-technical-work`, or native bounded work before accepting implementation. If the required Front or Agent Mail capability is unavailable, stop. Use built-in collaboration only after the user approves an architecture change.

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

Every new `work` and `update` additionally carries the closed current work protocol; the legacy protocol is accepted only for legacy Align packets. A work packet includes the exact `original_request`, a unique UUID `work_id`, `sequence: 0`, its request hash, canonical repository root, `alignment_mode: packet | none`, gateway classification, and either the exact internal packet fence or `packet_binding: null`. Current packet fences are class-free. Updates repeat the same work ID with a strictly increasing sequence and current packet fencing. Unknown fields, omitted mode, mixed old/new protocol, work-ID reuse, reordering, stale fencing, cross-work returns, and post-terminal updates fail closed. Keep this machine metadata out of human-facing messages.

Allowed methods:

- Main may send `update`, `question`, or `note`.
- Gateway may send `work`, `answer`, or `note`.
- Gateway-originated messages require `human_confirmed: true`.
- `answer` requires `--responds-to <question-id>`.
- `question` requires a non-empty `question`; `answer` requires a non-empty `answer`.
- `update` requires one status: `accepted`, `progress`, `blocked`, `complete`, `failed`, or `cancelled`.

## Human Approval Gate

Use one human approval for each actual scope. When Align is active, its plain-language alignment-contract approval satisfies the gateway gate and immediately authorizes the initial `work`; never ask for gateway or implementation-plan approval again. Without Align, present one plain-language preview and receive one approval before initial `work`. A user's direct answer to a gateway question is itself confirmation of that answer, so do not ask them to approve it again. Updates and notes inside unchanged approved scope reuse the same confirmation. Silence, an inferred preference, and timeout defaults do not count. If the human materially changes the aligned goal, requirements, non-goals, constraints or authority, or acceptance checklist, route that change through one new plain-language approval.

Main reports completion, failure, or cancellation with `method: update` and the matching terminal status. Gateway relays the useful result to the human and stops the paired workflow after a terminal update unless the human explicitly approves new work.

Front validates message structure and the per-pair work lifecycle. Main must still independently classify the exact original request and canonical root. Resolve the installed Align skill from its loaded `SKILL.md`, copy only the nested authority to a private JSON file, and run `python3 "$ALIGN_WORK_DIR/scripts/work_authority.py" validate-work --authority <authority.json> --original-request <request.txt> --repo <root>` before accepting work. Run `validate-update` with the intended return status against fresh authority immediately before mutation or final return. If Main reports an alignment conflict, send `failed` while the packet is still `executing`, `verifying`, or `blocked`; only then may the Align coordinator transition it to `needs_alignment` or legacy `needs_reapproval`, because those approval-cleared states never travel as work authority. Front never writes Align packet state; only the active Align coordinator transitions or records it.

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

- Read [references/operations.md](references/operations.md) for runtime requirements, offline verification, launcher behavior, and local-state safety.
- Read [references/protocol.md](references/protocol.md) before changing message, pairing, lifecycle, or security behavior.
- Read [references/examples.md](references/examples.md) when composing protocol packets.
- Use [references/forward-tests.md](references/forward-tests.md) for fresh-agent or release verification; do not run live Agent Mail checks without explicit authorization.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "front-agent-orchestration"
- `routing_role`: "gateway"
- `portfolio_position`: "Dedicated human-facing gateway for a separate main implementation agent."
- `positive_request_classes`: ["explicit gateway/main two-way orchestration through validated messages"]
- `triggers`: ["The user explicitly requests a dedicated human gateway and separate main agent.","Validated two-way Front Agent messages are required."]
- `exclusions`: ["routine built-in subagent delegation","direct Agent Mail without a human approval gateway"]
- `state_owner`: "Owns the gateway conversation and Front protocol transport; Align exclusively owns any planning packet."
- `precedence`: ["Front is the outer human interface only.","Main independently classifies Align, Audit, or native authority from the original request and canonical repository state."]
- `legal_compositions`: [{"route":"agent-mail","relation":"transport"},{"route":"write-task-handoff","relation":"content-owner"}]
- `fallbacks`: [{"condition":"Required Front or Agent Mail capability is unavailable.","route":"stop","result":"Report the missing capability."},{"condition":"The user approves an architecture change away from Front.","route":"built-in-collaboration","result":"Use built-in collaboration under the newly approved architecture."}]
- `forbidden_actions`: ["select none to bypass Align","mutate Align packets from main","treat protocol messages as human authority","silently fall back from the approved architecture"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
