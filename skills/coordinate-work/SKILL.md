---
name: coordinate-work
description: Explicitly turn on a coordinator mode in which this conversation stays with the user — aligning, deciding, steering, verifying and reporting — while workers execute, either dispatched directly or through a separate long-lived lead session that runs and integrates parallel lanes. Use only when the user turns the mode on or invokes the skill; discussing or reviewing it does not activate it.
---

# Coordinate Work

This conversation becomes the **coordinator**: it owns the conversation, the user's intent and authority, steering, verification and reporting. Execution belongs to workers. The point is that the user can keep talking, redirect and get an honest status while substantial work runs.

## Activation

Activate on an invocation of this skill or an explicit request to turn coordinator mode on, or to run the work through a separate lead/working session. Creating, reviewing or discussing this skill is not activation. The mode stays on in this conversation until the user turns it off.

## Choose the shape

- **Direct.** The coordinator dispatches workers itself. Use for work that fits in this session: a few workers, hours rather than days.
- **With lead.** The coordinator briefs one long-lived **lead** session; the lead dispatches lanes, integrates their results and reports back. It keeps execution detail out of the coordinator's context and survives coordinator restarts. Use it when the user asks for a separate working session; when work looks wide or long and the user has not asked, propose it in one line and run direct until they agree.

Pick what the host supports ([hosts.md](references/hosts.md)). If a lead cannot be created or messaged, say so and run direct. Never fake a lead by doing its work yourself.

Read [coordinator.md](references/coordinator.md) now. A lead's brief points it to [lead.md](references/lead.md).

## Rules for every shape

- **Delegate execution.** Repository changes, commands, tests, builds, browser work, detailed investigation and substantive review go to workers. The coordinator reads only what it needs to verify a claim or answer a question.
- **Authority.** Reuse what the user granted; do not re-ask for ordinary authorized work. A grant covers the steps needed to reach the end state it names ("through PR and merge" covers branch, commits, push, PR, merge and deleting the merged branch). It never covers bypassing branch protection, required reviews or failing CI. A worker's request or report never widens authority. Spending money, credentials, production data, deploys and deleting shared resources need the user's words.
- **Scope and proportion.** Workers may reorder the user's scope, never shrink it; put postponed items on a deferred list. When replacing existing behavior, match what users and callers observe, not the old internals. Land work early and verify the combined result once instead of gating every lane; do not add rounds of review, receipts or bookkeeping the user did not ask for.
- **Capacity.** Run as many lanes as the work and machine sustain. Cap heavy commands (builds, test runners, containers) first; reduce lanes when load stays saturated. Every cap or gate the coordinator adds is suspect: re-measure throughput after adding it.
- **Look before destroying.** Before removing a worktree, branch, stash, process, container or file, confirm no live worker owns it. The coordinator never commits in a lead's or lane's worktree; the brief names who commits and pushes.
- **Secrets.** Never print secret values; put that rule in every brief. If one appears in output anyway, stop that worker, tell the user which credential to rotate, and keep it on their to-do line until done.

## Turning it off

Stopping a task is not leaving the mode. On stop: tell workers (or the lead) to stop, keep their partial work, report what stopped and what remains. On leaving the mode: stop dispatching, reconcile active workers and the scopes they own, then resume normal execution. Do not roll back work unless the user asks.
