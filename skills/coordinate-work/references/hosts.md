# Host mappings

Use only tools the host lists; load deferred tools before calling them. If a call fails, re-check the name — hosts change.

## T3 Code (direct and with lead)

| Operation | Tool |
|---|---|
| Own thread id (for the brief) | `currentThreadId` in a `t3_thread_list` result |
| Create lead | `t3_thread_launch` with `workspaceStrategy` `existing_worktree` (a worktree made by the repository's convention) or `worktree`. `create_threads` stays in the current checkout. |
| Message a thread | `t3_thread_send`. Routine reports use `mode: "queue"`; `steer` updates a running turn; `restart` interrupts and restarts; `auto` steers a running turn, so avoid it for routine reports. |
| Stop the lead | `t3_thread_interrupt` |
| Read the lead | `t3_thread_read` with low `limit` and `maxCharsPerItem` |
| Wait for a thread | `t3_thread_wait` — for the lead or a short bounded wait only; the coordinator relies on the lead's messages instead |
| Dispatch a worker or lane | `delegate_task`: async by default; `isolation: "worktree"` prepares a checkout from the dispatcher's current commit (no base parameter); other providers via `target`, listed by `orchestrator_capabilities`. Children can delegate further. |
| Learn a lane finished | its completion wakes the dispatcher; never poll `task_status` on a running task |
| Cancel a lane | `task_cancel` (also cancels that lane's own delegates) |
| PR | `link_pull_request`; `watch_pull_request` wakes the caller on PR changes and expects it to end its turn — the lead owns watches for PRs it merges |
| Heartbeat | `schedule_task` with `{type: "interval", everyMs ≥ 60000}`; runs post into the creating thread by default, so create it from the coordinator |

The lead reports with `t3_thread_send` to the coordinator's thread id from the brief. A thread created with `t3_thread_launch` is not a delegate: nothing else wakes the coordinator when it finishes, so the brief must tell it to report.

## Claude Code

**Direct:** `Agent` runs background workers by default and notifies you on completion; `SendMessage` continues one; `TaskStop` stops one; `Monitor` watches PR checks or logs (default 5 minutes, at most 30 — set the timeout and re-arm only if still needed). A worker can start its own workers only if its agent type includes `Agent`. Built-in worktree isolation may not follow the user's worktree convention; prefer the convention when one exists.

**With lead:** the lead is a second, independent Claude Code session on the same machine. Documented in the `SendMessage` and `ListAgents` tools, not yet tried end to end in this skill:

1. The coordinator cannot open an interactive session for the user. Prepare the brief, including the coordinator's session name (the header of a `ListAgents` result), and ask the user to start a session in the lead's worktree and paste it.
2. Find the lead with `ListAgents` and send an opening message with `SendMessage` and `notify_when_idle: true`. The lead replies with `SendMessage` to the `from` address it received.
3. `notify_when_idle` is one-shot: subscribe again after each notice. Only the main conversation can subscribe; a subagent's cross-session messages go out under its parent's address.
4. Run both sessions in the same permission mode, or messages wait for approval on the other side.
5. As a main session, the lead dispatches its own `Agent` lanes.

A background `Agent` is not a lead: the user cannot open it, and it lives inside this session.

## Codex

Not verified. The skill is explicit-only in Codex, so it loads only when invoked by name. Run direct with the worker tools Codex lists, after confirming their names and whether a spawned agent can spawn its own. For a lead, ask the user to open a second session and relay messages until a verified mechanism exists.

## Any host

If no worker can be dispatched, say so and ask whether to leave coordinator mode; do not silently do the work yourself.
