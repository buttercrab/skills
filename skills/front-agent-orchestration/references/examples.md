# Examples

## Good Main Startup

```text
Main identity: steady-path-461

Open the gateway session and say:

$front-agent-orchestration gateway steady-path-461 --root "/repo"

Pairing waiter is detached; gateway should pair without another main-side command.
After pairing, main should run:
front-agent listen --identity steady-path-461 --root "/repo"
```

Good because main starts the waiter, gives gateway the tokenless command, and immediately listens after pairing.

## Good Gateway Startup

```text
$front-agent-orchestration gateway steady-path-461 --root "/repo"
Gateway identity: clear-river-1234
Paired with main identity: steady-path-461
Gateway is paired and ready for human input.
```

Gateway should return to the human after pairing. It should drain pending main mail with `listen --timeout 0` at the start of a later human-facing turn.

## Good Gateway Work Message

```yaml
method: work
from_role: gateway
to_role: main
summary: "Add in-app failure notifications."
human_confirmed: true
requirements:
  - "Show an in-app notification when a background job fails."
  - "Persist unread notifications until dismissed."
constraints:
  - "Do not add email or mobile push."
acceptance_criteria:
  - "Focused tests cover failure notifications."
```

Good because the human-approved task is explicit, scoped, and carries enough repo-aware context for main to orchestrate work.

## Good Main Question

```yaml
method: question
from_role: main
to_role: gateway
summary: "Choose invalid input behavior."
question: "Should invalid input be rejected inline or accepted with a warning?"
default_if_timeout: "Reject inline."
```

Good because main asks the human through gateway instead of asking directly in the main session.

## Good Gateway Answer

```yaml
method: answer
from_role: gateway
to_role: main
summary: "Invalid input decision confirmed."
human_confirmed: true
answer: "Reject invalid input inline."
```

Send with `--responds-to <question-id>`. Good because the answer is approved by the human and tied to exactly one main question.

## Good Main Update

```yaml
method: update
from_role: main
to_role: gateway
summary: "Implementation complete."
status: complete
result: "Added failure notifications and focused tests."
tests:
  - "npm test -- notification-panel"
```

Good because gateway can relay the useful result without exposing raw implementation chatter.

## Bad Competing Listener

```text
front-agent listen --identity steady-path-461 --root "/repo"
front-agent listen --identity steady-path-461 --root "/repo"
```

Bad because each identity has a single listener owner. The second command should fail clearly.

## Bad Gateway Work Without Approval

```yaml
method: work
from_role: gateway
to_role: main
summary: "Start work."
requirements:
  - "Do the thing."
```

Bad because gateway-originated messages require `human_confirmed: true`.
