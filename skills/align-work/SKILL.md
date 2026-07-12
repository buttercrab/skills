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

After compaction, interruption, coordinator transfer, or a fresh session, reconstruct task knowledge from the packet and revalidate volatile facts. A fresh session must ask the user to reauthorize before any mutation even if the packet records prior approval.

## Run the stages

1. **Explore and align:** read [references/explore-and-align.md](references/explore-and-align.md). Explore discoverable reality while asking only decision-changing questions. Update the packet before sending the next question round.
2. **Write the plan:** when no decision-changing question remains, read [references/write-plan.md](references/write-plan.md). Produce a self-contained plan with exact scope, authority, steps, gates, risks, and rollback.
3. **Review when warranted:** read [references/review-plan.md](references/review-plan.md). Prefer fresh adversarial review for complex or risky plans; record why a simple plan skipped it.
4. **Request approval:** seal the protected packet and show the user its revision, digest, and authority classes. Do not mutate product, repository, global, or external state before approval.
5. **Execute and verify:** after current-session approval, read [references/execute-approved-plan.md](references/execute-approved-plan.md). Record attempts, use bounded delegation, stop for material changes, and complete only when required gates have receipts.

## Enforce hard boundaries

- Never rely on conversation history for a material fact, decision, authority, step, or gate.
- Treat helper validation as structural integrity evidence, never proof of semantic completeness or authenticated human authority.
- Keep one active coordinator as the only canonical packet writer.
- Use direct children only. Begin every child assignment with: `You are a direct child. Do not spawn or delegate to any other agent.` Treat attempted subdelegation as an invalid result. Prefer read-only isolation for exploration and review; otherwise hash canonical files before and after each child run and reject mutated results.
- Ask the user only about decisions that can change outcome, scope, architecture, authority, safety, risk, acceptance criteria, or the plan. Discover safely inspectable facts instead.
- Treat packet approval as nonportable evidence. Reconfirm authority in every fresh session.
- Use cheap or fast models only for bounded, approved implementation. Use strong reasoning for alignment, planning, synthesis, adversarial review, high-risk work, and final verification.
- If a protected file changes after approval, invalidate approval. For a material change, stop new mutation, preserve partial work and receipts, record rollback options, revise the packet, and request reapproval.
- Do not escalate to a plugin, hook, MCP server, custom runtime, publication, deployment, or other external action without new authority.
- Before approval, prefer a read-only sandbox or read-only children. If the current surface still exposes write tools, record hashes for protected product/global surfaces and fail on unexpected mutation; instruction-level policy is not a technical sandbox.

## Report completion

Return the implemented outcome first, followed by required gate receipts, unrun optional checks and residual risk, packet status, and any remaining external action. Never call the task complete with a skipped or failed required gate.
