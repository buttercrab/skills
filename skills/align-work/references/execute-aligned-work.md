# Execute Aligned Work

Read this reference after the user approves `alignment.md` or gives an explicit fresh-task continue/resume/implement instruction for an existing aligned packet.

## Start or resume

1. Validate the alignment digest, packet state, coordinator epoch, and execution chain.
2. Confirm alignment continuity. Reuse approval without another prompt only inside the same visible Codex task; in a fresh task, the user's explicit continue/resume/implement instruction is reauthorization, while file-recorded approval alone is insufficient.
3. Read applicable repository guidance and inspect the current branch, worktree, generated state, and relevant external state.
4. Record the dirty-worktree baseline, explicitly owned paths, unrelated user changes to preserve, and any partial mutation already present.
5. Revalidate volatile facts against the approved alignment. Continue through plan changes; stop only when the alignment contract cannot be honored.
6. Reconcile incomplete attempts and partial mutations before choosing the next eligible step. Never blind-revert or clean state the packet does not own.
7. Create or refresh the agent-owned `plan.md`. Transition to `executing` with the existing approval; do not ask the user to approve the plan or ask “start?” again.
8. Record every attempt through the packet helper.

Before each writable slice that can overlap existing work, run `scripts/preservation_journal.py snapshot` for every owned path and store it in the active packet's mode-0700 `private-preimages/` area. After mutation, record exact postimages and the owned patch with `record-post`. Use `rollback` only when its all-path preflight proves every current path still equals the recorded postimage; otherwise stop without overwriting concurrent work.

## Implement autonomously

- Keep changes consistent with `alignment.md` and preserve unrelated user work.
- Revise architecture, files, dependencies, sequencing, fallbacks, tests, retries, refactors, and internal rollback mechanics without user approval.
- Give direct children bounded, non-overlapping ownership. Begin every assignment with: `You are a direct child. Do not spawn or delegate to any other agent.` Include packet identity, alignment revision and digest, exact step, allowed paths/actions, and required receipt. Prohibit canonical packet edits and invalidate attempted subdelegation.
- Use isolated worktrees or explicitly owned paths for writable children.
- Use `execute-goal-loop` only when explicitly requested or approved. Derive its objective and gates from `alignment.md`; the loop cannot broaden the alignment contract or mark packet completion without its acceptance evidence.

## Discoveries during execution

### Plan change

Continue without user involvement. Update `plan.md` when useful and record material actions and receipts in `execution.md`. A different architecture, file set, dependency, step order, verification tactic, fallback, or in-scope fix is never a reason to reopen alignment by itself.

### Alignment change

Enter `needs_alignment` only when the approved goal, requirements, non-goals, constraints or authority, or acceptance checklist must change, conflict, or cannot all be satisfied. Exact destructive allowlists and aligned external targets remain literal.

1. Stop new product mutation and preserve the diff, receipts, and partial effects. Allow read-only diagnosis and necessary safety containment.
2. Transition the packet to `needs_alignment`, clearing stale approval.
3. Record the concrete contract conflict, missing authority, partial effects, and disposition options in `facts.md` and `decisions.md`.
4. Revise `alignment.md`, then use guarded `repair` to acknowledge the protected change and return to alignment drafting or review. `plan.md` may also change, but it is not part of the approval digest.
5. Reseal the new alignment revision and ask once for the exact contract delta and partial-work disposition. Keep machine receipts internal.
6. After approval, refresh the agent plan and resume without a separate plan or start prompt.

## Verify and complete

Run every acceptance check from `alignment.md` and attach its command, interaction, artifact, and result to `execution.md`. Optional strengthening checks may be skipped only with a reason and residual-risk note. Transition to `complete` only when every required acceptance check passes and no required work remains.
