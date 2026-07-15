---
name: align-work
description: Use as the default outer workflow for coding work when the user explicitly invokes $align-work, an existing align-work packet must be resumed, user intent is unclear, completion requires at least three dependent reasoning or decision steps, or work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or externally mutating. Explore and align in repeated rounds, persist facts and decisions in a planning packet, write and optionally adversarially review a self-contained plan, wait for approval, then implement and verify. Do not use for noncoding tasks, simple factual answers, low-risk exact mechanical edits, or an explicitly selected workflow that already owns end-to-end human alignment and approval.
---

# Align Work

Turn nontrivial coding requests into a context-independent, user-approved execution contract. Keep one state owner from discovery through verification; use the referenced stages rather than attempting to invoke other skills as an automatic pipeline.

## Classify the task

Use this workflow when either condition holds:

1. User intent is unclear.
2. Completion requires at least three dependent judgments, where a later choice relies on an earlier finding.
3. The work is destructive, irreversible, production-facing, security/privacy-sensitive, costly, or writes to an external system, even if the requested action is clear and one-step.

If uncertain, treat the task as nontrivial. Explicit invocation and an existing packet trigger it unless an already-active Front Agent gateway owns the same task. Bypass this workflow for noncoding work, simple facts, and low-risk reversible exact mechanical edits.

Respect explicit precedence. An already-active Front Agent gateway owns human alignment and any shared packet for its paired task, even if `align-work` is also named; do not create a second packet in the main session. Otherwise `align-work` owns the execution contract. Domain skills such as `skill-creator` own only mechanics inside it. Use `execute-goal-loop` only when the user explicitly requests persistent iteration or approves a loop contract; the sealed packet remains canonical, goal state cannot broaden it, and material discoveries return to `align-work` reapproval.

## Establish the packet

Read [references/packet-contract.md](references/packet-contract.md) before creating, resuming, sealing, approving, or repairing a packet.

Create or resume exactly one packet at:

```text
<repo>/.planning/<task-id>/
```

Use `scripts/planning_packet.py`; do not hand-author `state.json`. Treat `facts.md` and `decisions.md` as the evidence and decision ledgers. Keep `plan.md` independently understandable and bind approval to its sealed packet revision.

If the user forbids all file creation or edits, do not create `.planning/`. Ask permission for the durable packet only when it is necessary; if permission is denied, remain read-only and state that durable resume and implementation are unavailable.

After compaction, interruption, coordinator transfer, or a fresh task, reconstruct task knowledge from the packet and revalidate volatile facts. A valid approval remains usable across compaction, automatic continuation, and later turns in the same visible Codex task when packet identity, coordinator state, and the approved envelope still match. In a fresh Codex task, file-recorded approval alone is insufficient: an explicit user instruction to continue, resume, or implement is lightweight reauthorization; ask once only when the user has not supplied such direction.

## Use one approval envelope

Define the approval envelope as the outcome and concrete scope, architecture and fallback bounds, security/privacy/trust boundary, cost or time ceiling, required verification strength, and rollback or partial-work rules. The normal prompt budget is one human approval per envelope. An unqualified approval of the presented implementation plan authorizes immediate execution; use the same user message for approval and execution authorization and do not ask a second “start?” question.

Preauthorize bounded fallback branches when they are reasonably foreseeable. Retries, step reordering, reversible implementation mechanics inside approved paths, named fallbacks inside their bounds, stronger verification, and ordinary in-scope bug fixes stay inside the envelope. New authority or surfaces, unplanned outcome/scope/architecture, expanded risk or trust, cost above the ceiling, weaker required gates, or an unapproved partial-work disposition leave the envelope and require a new approval.

## Keep audit receipts internal

Present approval in plain language: state the intended outcome and next actions, what will and will not change, and any material external effect, risk, cost, or rollback implication. Ask one concise contextual question. Accept an unambiguous response such as “yes,” “approve,” or “go ahead”; never prescribe an exact reply formula.

Do not normally show packet IDs, repository roots, revisions, digests, fact/decision/step IDs, approval IDs, execution hashes, or other machine receipts. Reveal the minimum needed only when the user requests audit details or an integrity ambiguity requires identifying the exact packet. This presentation rule overrides approval wording copied into older packets: translate legacy prose instead of repeating it.

## Run the stages

1. **Explore and align:** read [references/explore-and-align.md](references/explore-and-align.md). Explore discoverable reality while asking only decision-changing questions. Update the packet before sending the next question round.
2. **Write the plan:** when no decision-changing question remains, read [references/write-plan.md](references/write-plan.md). Produce a self-contained plan with exact scope, authority, steps, gates, risks, and rollback.
3. **Review when warranted:** read [references/review-plan.md](references/review-plan.md). Prefer fresh adversarial review for complex or risky plans; record why a simple plan skipped it.
4. **Request approval:** seal the protected packet, then describe the concrete approval scope using the plain-language presentation rule above. Do not mutate product, repository, global, or external state before approval. Unless the user explicitly limits approval to planning, treat approval as permission to execute immediately within the envelope.
5. **Execute and verify:** after approval or explicit fresh-task reauthorization, read [references/execute-approved-plan.md](references/execute-approved-plan.md). Record attempts, use bounded delegation, stop for out-of-envelope changes, and complete only when required gates have receipts.

## Enforce hard boundaries

- Never rely on conversation history for a material fact, decision, authority, step, or gate.
- Treat helper validation as structural integrity evidence, never proof of semantic completeness or authenticated human authority.
- Keep machine receipts in the packet and helper output; do not copy them into normal user-facing status, approval, reapproval, resume, or completion messages.
- Keep one active coordinator as the only canonical packet writer.
- Use direct children only. Begin every child assignment with: `You are a direct child. Do not spawn or delegate to any other agent.` Treat attempted subdelegation as an invalid result. Prefer read-only isolation for exploration and review; otherwise hash canonical files before and after each child run and reject mutated results.
- Ask the user only about decisions that can change outcome, scope, architecture, authority, safety, risk, acceptance criteria, or the plan. Discover safely inspectable facts instead.
- Treat packet approval as nonportable evidence across Codex tasks. Within the same visible task, reuse a still-valid approval without another prompt. In a fresh task, treat the user's explicit continue/resume/implement instruction as reauthorization; otherwise ask one concise question.
- Use cheap or fast models only for bounded, approved implementation. Use strong reasoning for alignment, planning, synthesis, adversarial review, high-risk work, and final verification.
- Freeze protected planning files after approval. Record in-envelope discoveries and mechanics in `execution.md`, not `facts.md`, `decisions.md`, or `plan.md`. If work leaves the envelope, stop new mutation, preserve partial work and receipts, record rollback options, revise the protected packet, and request reapproval. Unexpected protected-byte drift remains an integrity fault and invalidates approval.
- Do not escalate to a plugin, hook, MCP server, custom runtime, publication, deployment, or other external action without new authority.
- Before approval, prefer a read-only sandbox or read-only children. If the current surface still exposes write tools, record hashes for protected product/global surfaces and fail on unexpected mutation; instruction-level policy is not a technical sandbox.

## Report completion

Return the implemented outcome first, followed by required gate receipts, unrun optional checks and residual risk, packet status, and any remaining external action. Never call the task complete with a skipped or failed required gate.
