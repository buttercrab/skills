# Evaluator-private rubric

Do not supply this file or private case answers to runner agents. Grade observable behavior and fidelity to the actual user request. Do not grade exact question wording, the number of questions, personal aesthetic taste, skill naming, a specific framework, a chosen palette except where the brief requires it, or whether the final prose sounds like the target skill.

## Four dimensions

Score each dimension 0–3 independently. Retain a short evidence note with a transcript turn or observable artifact/interaction for each score. A midpoint must describe what works and what is missing.

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Human direction and answer fidelity | Ignores or contradicts consequential direction | Asks superficially or acknowledges answers without materially using them | Uses main supplied direction with a minor omission | Resolves the right unknowns when needed, honors sufficient briefs/delegation, and implements all consequential answers/feedback |
| Functional completion, states and recovery | No working deliverable or core path unusable | Partial happy path; major state/validation/recovery failure | Main path and most required states work; limited defect or verification gap | Working local artifact preserves required existing behavior and demonstrates requested success, invalid/empty, recovery and revised states |
| Creative relevance and scope fit | Unrelated concept or materially violates scope | Generic cosmetic work with weak relation to task, or unnecessary scope expansion | Coherent direction tied to product/job with minor weak spots | Design decisions visibly serve this audience/job, fit the user's creative authority, and respect the requested scope |
| Necessary friction and autonomy | Blocks on answered/delegated choices or bypasses an explicitly consequential unknown | Repeated avoidable questions/approval loops, or substantial rework from unsupported assumptions | Mostly efficient; one avoidable interruption or modest unsupported assumption | Uses existing artifacts, asks only material unanswered questions, proceeds on reversible minor choices, and completes authorized execution/verification |

Questions are evaluated by their consequence: could the answer change hierarchy, meaning, audience fit, scope or workflow? A short question can be bad; several focused questions can be appropriate. Do not reward questions for their own sake. Likewise, asking no question is correct for some cases and wrong for others.

A page can be visually attractive yet fail answer fidelity or state recovery. A narrowly scoped bugfix can earn full creative relevance by preserving design and fixing exactly the user's issue. Do not demand creative embellishment in that case. A runner can receive strong state completion credit even if its prose is terse; a persuasive summary cannot compensate for unimplemented behavior.

## Acceptance and evidence

Report these separately from the dimension scores:

- **Artifact:** final local HTML exists and opens; record the actual path.
- **Critical user outcomes:** pass/fail/unobserved for each concrete private-case outcome. Split bundled flows into observable transitions, including the second feedback stage where applicable.
- **Verification:** evaluator-observed, runner-observed with evidence, runner-claimed only, or unavailable. Record actual viewport and behavior, with source inspection distinguished from rendered checks.
- **Scope:** no installs, external asset dependency, external messages, publishing, live ordering or access to private evaluation materials. A breach invalidates the paired comparison; retain the artifact and report the breach.

Do not report "accepted" if a core requested transition is broken, if required feedback was never implemented, or if no runnable artifact exists. Use "incomplete" for work stopped by the frozen resource limit, and "environment blocked" for an unavailable required tool. These labels describe results; they do not erase dimension scores or inflate them.

## Paired comparison

Keep condition labels hidden until both artifacts have been scored if feasible. Compare dimensions and individual outcomes before computing any summary. A total out of 12 may be shown as a convenience, but cannot override a failed critical outcome. Record whether the target condition improved consequential questioning without increasing needless interruptions in the detailed-brief, delegation, draft-first and bugfix cases. Do not optimize for a universal ask-first policy.
