This is preserved service operating documentation, not an installed skill. Native subagents are the default for current-chat coordination. The service and deployed semantics have not changed.


# Agent Mail

Agent Mail is a durable Rust/PostgreSQL mailbox and remote MCP service. Use it for durable cross-session coordination, not routine logs or locks. Routine current-task subagent coordination belongs to built-in collaboration. Front Agent uses Agent Mail only when the user explicitly selected that gateway architecture.

Resolve `AGENT_MAIL_SKILL_DIR` to the directory containing this `OPERATIONS.md`; never assume the caller's current working directory is this repository.

## Choose the interface

- For ordinary Codex mailbox work, prefer the installed Agent Mail MCP tools and resources. Start a session identity before sending or reading.
- For service development, privileged HTTP work, credentials, local integration tests, or deployment, read [references/service-operations.md](references/service-operations.md) before acting.
- For infrastructure changes, also read [docs/lightsail.md](docs/lightsail.md).
- If the required durable service or authenticated capability is unavailable, report the missing capability. Do not silently replace durable coordination with ephemeral messaging.

The remote MCP endpoint is `https://agent-mail.cc/mcp`. Install it by URL, not through a local shim:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

## Mailbox workflow

1. Start or reuse the session-bound participant identity.
2. Select the exact project namespace and recipient identity, role, or broadcast.
3. For a mutation, state the intended durable message or read-state change and use a stable idempotency key when response loss could cause a retry.
4. Read inboxes and full messages through resources. Reads do not mark mail read.
5. Call the explicit mark-read mutation only when that state change is intended.
6. Treat notifications as wake-up hints and the mailbox as authoritative durable state.

Messages are coordination records, not locks, claims, approval, packet transfer, or exclusive assignment. Agent Mail owns mailbox transport and service data only. It never becomes the planning or approval workflow, and a mail message never substitutes for direct human authority.

## Safety

- Keep service-admin, credential-admin, and participant tokens out of mail, logs, errors, command output, and shared artifacts.
- Persist a participant token only when reuse is required, in a user-owned mode-`0600` file.
- Do not assume HTTP or MCP reads mark messages read.
- Do not store secrets, raw environment dumps, `.flow/events/`, or sensitive brainstorming unless confirmed.
- The public MCP smoke mutates production and leaves durable records. Run it only with explicit production-mutation authorization and the required confirmation environment described in the operations reference.
- Never use the service-admin token where a participant token is required.
