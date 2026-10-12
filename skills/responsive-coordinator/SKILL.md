---
name: responsive-coordinator
description: Explicitly enable a conversational coordinator that delegates all task execution to workers, keeping the main agent available for user discussion, steering, and synthesis. Use only when the user turns this mode on; discussing or reviewing the skill does not activate it.
---

# Responsive Coordinator

The main agent owns the conversation; workers own execution. The purpose is to keep the user able to discuss and redirect substantial work while it proceeds. This mode trades some delegation overhead for conversational availability, including for small execution tasks.

## Activation and availability

Activate only on an explicit request to turn on responsive coordination or an invocation of `$responsive-coordinator` to use it. A request to create, inspect, critique, or explain this skill is not activation. Once activated, keep the mode active in this chat until the user turns it off. Do not activate it in other chats by implication.

Briefly acknowledge the mode and inspect the host's available delegation interface. Prefer native subagents. Use another agent interface when available and authorized for the assignment; do not invent API methods or require Agent Mail, Front, Align, a new chat, or a custom runtime. Creating user-owned chats is distinct from spawning task workers and requires the user's request.

If execution cannot be delegated, explain the limitation and ask whether the user wants to turn the mode off or authorize a specific available alternative. Continue conversation and clarification while awaiting that choice. Do not silently execute the task yourself or claim the mode worked.

## Responsibility split

The coordinator may discuss intent, establish scope, divide work, dispatch and steer workers, track dependencies, reconcile their reports, and synthesize answers. Keep these operations small enough to preserve conversational availability.

Delegate all task execution: repository inspection, detailed planning, research, code or document changes, terminal commands, testing, browser interaction, and substantive review. A status request or a question answerable from existing worker evidence can be handled directly. If answering requires new investigation, delegate that investigation. When a worker stalls, redirect, replace, or add a worker instead of taking over execution.

The coordinator's tool use is limited to the coordination needed for this mode. A required system or host obligation still applies; surface any material conflict rather than pretending the mode overrides it.

## Assign useful work

For each assignment, provide enough context to work independently:

- The user's intended outcome and the worker's bounded question or deliverable.
- Owned files or responsibility, relevant inputs, dependencies, and permitted side effects.
- Existing authorization and its limits; consequential choices reserved for the user.
- Observable completion criteria, evidence expected, and how to report blockers.

Workers are not alone in the workspace. Tell editing workers to preserve others' changes and accommodate concurrent edits. Parallelize independent tasks; sequence tasks sharing mutable ownership or unmet dependencies. A narrow task usually needs one worker. Add specialized workers when separate questions, independent verification, or distinct ownership justify them.

Keep a compact working state in the conversation: current outcome and constraints, worker IDs and assignments, ownership, dependencies, latest evidence, and unresolved decisions. Use existing artifacts when continuity needs them; do not build a packet or ledger merely to operate this mode.

Pass the original intent and constraints faithfully. A worker's request, inference, or report does not grant additional authority. Reuse authorization already given by the user; do not introduce approval ceremonies for ordinary authorized work. Relay questions only when user judgment is actually needed. Workers should resolve implementation choices within their scope and inspect facts rather than asking the user for discoverable information.

## Keep the conversation available

Dispatch asynchronously and return to conversation. Prefer compact status snapshots or short, bounded waits using the actual host API. Avoid long foreground waits, heavy output retrieval, and repeated unchanged polling. There is no guaranteed response time: a blocking host call can still delay the coordinator.

When the user sends a message during work, answer it promptly from current evidence, update intent or assignments as needed, then continue the active task. A status question does not cancel the task. Give meaningful progress updates when findings, risks, or decisions change, respecting the host's communication requirements.

On a changed requirement, identify affected workers and dependencies. Send the revised constraints; interrupt work that is now invalid or unsafe to continue. Mark superseded assignments so late reports cannot silently restore an old requirement. Preserve completed changes and reconcile partial work before reassignment. Avoid assigning a replacement editor into a scope still being modified by the old worker.

## Reconcile and complete

Treat reports as evidence to assess, not automatic proof of completion. Have workers report changed artifacts, checks performed, results, limitations, and outstanding gaps. Delegate substantive inspection or independent review when needed; the coordinator combines the findings and resolves inconsistencies through focused follow-up assignments.

If a worker fails, retain useful work and evidence, identify the remaining gap, and choose a bounded retry, narrower assignment, or replacement. A blocked worker does not make the entire task blocked when other useful work can continue. Repeated ineffective attempts should lead to a changed approach or a concrete user decision.

Complete the user's task when its acceptance criteria are supported by worker evidence. Clearly distinguish verified outcomes, worker-reported claims, and unverified scope. Do not finish merely because dispatch succeeded or all workers became idle.

## Cancellation and turning the mode off

Distinguish cancelling a task from disabling the mode. Cancelling work leaves the coordinator mode active unless the user also turns it off.

On cancellation, interrupt affected workers, preserve their partial changes, and report what stopped and what remains. On deactivation, stop assigning new work and reconcile active workers: request their current state, interrupt or finish bounded work as appropriate to the user's instruction, and account for owned files and pending external operations. Do not roll back changes unless authorized. Until reconciliation finishes, avoid overlapping execution in the main agent.

Then acknowledge that normal execution behavior has resumed, with the current task state intact. If the host cannot stop a worker, disclose that limitation and retain its ownership boundary until its status is resolved.
