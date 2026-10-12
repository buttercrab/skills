---
name: write-task-handoff
description: Create a restartable continuation prompt or artifact for work moving across sessions, agents, or context limits. Capture current state, decisions, evidence, authorization provenance, and the first resume action without requiring the original conversation.
---

# Write Task Handoff

A handoff should let a fresh executor continue the task safely and efficiently. Preserve decisions and unfinished work; link existing artifacts instead of reproducing their full contents.

## Establish current state

Use the requested destination and format. When none is specified, provide a continuation artifact in the conversation or choose a durable workspace location if saving is part of the request.

Inspect the current checkout and relevant task artifacts before reporting them as current. Record a revision, observation time, or other reproducible state marker appropriate to the task. Label earlier receipts as historical when they no longer match the current state. Refresh only facts that matter to resumption; do not rerun expensive verification merely to decorate the handoff.

If the task has an existing plan, packet, or checkpoint, reference it and summarize what changed since it was written. Do not create a competing mutable ledger or modify coordination state merely to write a summary. A handoff document alone does not acquire a lock or transfer operational ownership; use the existing coordination mechanism when an actual transfer is required.

## Include what the next executor needs

Scale detail to the task. Preserve:

- The requested outcome and observable completion conditions.
- Scope, constraints, consequential decisions and their rationale, and unresolved choices.
- Exact repository/worktree, branch or revision, relevant artifacts, and current runtime state when needed.
- Completed changes and partial effects. Identify task-owned dirty paths and unrelated or uncertain changes the next executor must preserve.
- Verification already performed: relevant commands or interactions, results, revision/environment, and limitations. Distinguish suggested, attempted, failed, and passed checks.
- Remaining work, blockers, dependencies, and the first concrete resume action.
- Volatile facts that must be refreshed before acting, such as deployed versions, remote state, or another worker's ownership.

Carry the provenance and scope of existing authorization: what the user actually requested or approved, any subsequent narrowing or cancellation, and actions still outside that scope. A handoff must neither erase valid authorization merely because the executor changes nor imply a broader grant from a summary or worker recommendation. If authorization cannot be established in the receiving environment, name that uncertainty and the dependent action rather than imposing a blanket restart approval.

Separate observation, user decision, inference, and assumption where the distinction affects the next step. Include exact errors and identifiers only when useful and safe; exclude credentials, signed URLs, tokens, and unnecessary sensitive history.

## Make continuation unambiguous

Use current facts and concrete paths rather than “as discussed above” or “finish the remaining items.” End with the first resume action and its prerequisite check, if any. Link stable artifacts; summarize mutable remote facts with their observation time instead of implying they remain live.

Creating a document and delivering it are different outcomes. State where it was saved and whether requested delivery occurred. Do not message another person or agent merely because a handoff was prepared; use the user's authorized destination and transport. Report any unfinished ownership transfer separately from the completed writing work.
