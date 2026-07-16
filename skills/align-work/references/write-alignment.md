# Write the Alignment Contract

Read this reference after proactive questioning closes the material intent gaps.

## Required content

Write `alignment.md` as the complete user-approved outcome contract:

- goal and user-visible outcome;
- must-have functional and quality requirements;
- explicit non-goals;
- preservation constraints and authority boundaries, including exact destructive or external targets when relevant;
- trust, security, privacy, data, cost, and time limits; and
- an acceptance checklist of observable checks and required evidence.

The acceptance checklist defines what counts as done. It is not an implementation sequence. Do not include architecture, file lists, dependencies, step ordering, fallback mechanics, or other agent-owned planning detail unless the user explicitly makes one a requirement or constraint.

## Approval readiness

Before sealing:

1. Resolve every open question that can materially change the goal, requirements, non-goals, constraints or authority, tradeoff priorities, or acceptance checklist.
2. Confirm every requirement maps to at least one observable acceptance check.
3. Confirm every acceptance check names the evidence that will prove it.
4. Make assumptions explicit and distinguish delegated agent judgment from user-owned choices.
5. Verify exact external targets, destructive allowlists, cost ceilings, and trust boundaries against discoverable reality.

Ask once in plain language for approval of this alignment contract, never the implementation plan. State that approval authorizes the agent to create and revise its own plan and execute immediately. Never ask the user to repeat packet identity, revision, or digest data.

## Alignment changes

After approval, change `alignment.md` only when the aligned goal, requirements, non-goals, constraints or authority, or acceptance checklist must change. Enter `needs_alignment` before rewriting it, preserve partial-work evidence, repair and reseal the new alignment revision, and ask once about the exact contract delta and partial-work disposition.
