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

## Responses

Only `answer` is response-shaped. It must be sent with:

```bash
front-agent send "Decision confirmed" --identity <gateway-id> --responds-to <question-id>
```

The referenced message must be a valid main-to-gateway `question`. The CLI rejects duplicate valid answers for the same question.

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
