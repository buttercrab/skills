# Execute an Approved Plan

Read this reference only after current-session approval of the sealed packet or after fresh-session reauthorization.

## Start or resume

1. Validate packet digest, state, coordinator epoch, and execution chain.
2. Confirm current-session authority classes. File-recorded approval alone is insufficient in a fresh session.
3. Read applicable repository guidance and inspect the current branch, worktree, generated state, and relevant external state.
4. Record the dirty-worktree baseline, explicitly owned paths, unrelated user changes to preserve, and any partial mutation already present.
5. Revalidate volatile facts and compare live state to the approved baseline. Stop for reapproval if drift is material.
6. Reconcile incomplete attempts and partial mutations before choosing the next eligible step. Never blind-revert or clean state that the packet does not own.
7. Transition to `executing` and record every attempt through the packet helper.

Before each writable slice that can overlap existing work, run `scripts/preservation_journal.py snapshot` for every owned path and store it in the active packet's mode-0700 `private-preimages/` area. After mutation, record the exact postimages and owned patch with `record-post`. Use `rollback` only when its all-path preflight proves every current path still equals the recorded postimage; otherwise stop without overwriting concurrent work.

## Implement

- Keep changes inside approved scope and preserve unrelated user work.
- Give direct children bounded, non-overlapping ownership. Begin every assignment with: `You are a direct child. Do not spawn or delegate to any other agent.` Include packet ID, revision, digest, exact step, allowed paths/actions, and required receipt. This is a non-expandable delegation of the coordinator's current authority, not portable approval or a new human-facing session. Prohibit canonical packet edits and invalidate any result that attempts subdelegation.
- Use isolated worktrees or explicitly owned paths for writable children.
- Run local compilers, temporary services, and integration tests through the repository's approved hermetic runner when the sealed plan requires it. A missing offline dependency or unavailable technical isolation is an incomplete gate, never permission to use ambient caches or network.
- Use cheap/fast models only for bounded approved implementation; record the actual model. Keep alignment, planning, review, high-risk work, synthesis, and final verification on a strong reasoning model.
- Use `execute-goal-loop` only when the user explicitly requested or approved a persistent loop. Derive its objective and gates from the sealed packet; its state cannot broaden scope, replace packet gates, or mark packet completion.

## Material discovery

If a material change appears:

1. Stop new product mutation. Preserve the diff and receipts; allow only read-only diagnosis and necessary safety containment.
2. Immediately transition the packet to `needs_reapproval`. This clears stale approval before any more planning work.
3. Record the discovery, partial effects, rollback options, and newly open questions in `facts.md` and `decisions.md`.
4. Revise `plan.md`, then use guarded `repair` to acknowledge the intentional protected-file rewrite and return to `drafting` or `reviewing`. Do not leave a digest-mismatched packet waiting on a reviewer.
5. Complete any required bounded review, reseal the packet with a new revision and digest, and return to `awaiting_approval`.
6. Ask the user to approve the new digest and partial-work disposition or choose rollback. Never resume implementation from the superseded approval.

## Verify and complete

Run every required gate and attach its command, interaction, artifact, and result to `execution.md`. Optional strengthening checks may be skipped only with a reason and residual-risk note. Transition to `complete` only when all required gates pass and no required work remains.
