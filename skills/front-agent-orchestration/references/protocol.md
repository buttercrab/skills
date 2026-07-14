# Protocol Reference

Front Agent uses one validated message contract, `front_message`, plus an internal `front_ready` pairing handshake. Users interact with `front-agent send`; the CLI sets the mail metadata and stores the body as fenced YAML.

## Body Format

Every non-ready message body must be a fenced YAML mapping:

```yaml
method: work
from_role: gateway
to_role: main
summary: "Implement the approved change."
human_confirmed: true
requirements:
  - "Keep the existing behavior unless specified."
```

Do not include a protocol version field. The current protocol is defined by the CLI validator and the allowed method matrix below.

## Methods

Main may send:

- `update`: progress, completion, blocker, or result.
- `question`: a human decision or clarification needed through gateway.
- `note`: non-blocking context.

Gateway may send:

- `work`: approved human task or scope change.
- `answer`: approved answer to a main question.
- `note`: approved non-blocking human context.

Gateway-originated messages must include `human_confirmed: true`.

Gateway may set that field only after presenting the exact intent or decision preview to the human and receiving explicit approval. Silence, an inferred preference, and timeout defaults are not approval.

`question` requires a non-empty `question` field. `answer` requires a non-empty `answer` field. `update` requires one status:

- `accepted`: main accepted the work packet.
- `progress`: nonterminal progress.
- `blocked`: nonterminal work that needs input or external state.
- `complete`: terminal success.
- `failed`: terminal failure.
- `cancelled`: terminal cancellation approved by the human.

## Responses

Only `answer` is response-shaped. It must be sent with:

```bash
"$FRONT_AGENT" send "Decision confirmed" --identity <gateway-id> --responds-to <question-id>
```

The referenced message must be a valid main-to-gateway `question`. The CLI serializes answer sends per question and records sent answers locally; Agent Mail also enforces durable uniqueness. A consumed/read answer still prevents a second answer.

Before every HTTP send, the client persists a stable idempotency key. Retrying an ambiguous send reuses that key and Agent Mail returns the original message. After successful CLI output, an intentional identical non-response packet receives a new generation key; response keys remain bound to `responds_to`, and changed recipient, subject, or body is rejected. Do not delete local idempotency state after an ambiguous response.

## Lifecycle

Pairing moves through waiting, acknowledgement, and paired states. `"$FRONT_AGENT" state --identity <main-id>` is the main-side synchronization surface; start normal listening only after `pairing_state` becomes `paired`. Gateway pairing is resumable from locally persisted readiness state if acknowledgement was delivered before a process failure.

`complete`, `failed`, and `cancelled` updates are terminal. Gateway relays the result and stops unless the human explicitly approves a new work packet. No field authorizes an automatic decision on timeout.

## Safety Rules

- Use the same `--root` for both agents.
- Pairing is tokenless; old token flags are invalid.
- Main `wait-ready` owns a live waiter lock while pairing. Gateway fails before sending readiness if that waiter is absent.
- Pairing is complete only after both sides record `paired_at`.
- Use one-shot `listen` for normal work. It exits after printing available valid messages or after the first waited delivery.
- Gateway `listen` requires explicit `--timeout`; use `--timeout 0` for human-turn drains.
- Do not run more than one `listen` for the same identity.
- Do not use raw Agent Mail for protocol repair.
- Invalid sender, peer, role direction, method, freshness, or YAML is rejected and marked read.
- Metadata is validated from typed Agent Mail fields; subjects cannot contain newlines, participant credentials authenticate sender identity, and protocol security fields must be direct top-level YAML scalars.
- Valid messages are printed before they are marked read. A write failure leaves the message unread, so delivery is at-least-once and consumers deduplicate by message ID.
- Inbox reads use server keyset pagination (`limit=100` and opaque `next_cursor`), follow at most 10 pages per poll, cap response size, and share the listen deadline across project, page, and message requests.
