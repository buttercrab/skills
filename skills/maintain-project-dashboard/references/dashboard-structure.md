# Project dashboard structure

Use the smallest structure that supports real decisions. Add a section only when it has a distinct owner and purpose.

## Recommended base

### 1. Goal

- Current milestone
- Success condition
- Exact named evaluation or acceptance gate
- Explicit non-goals or constraints that prevent scope drift

Keep this stable. Change it only when the user changes the objective, priority, acceptance condition, or active constraint.

### 2. Current truth

Show a compact status table:

| Item | Current state | Why it matters | Evidence | Verified at |
|---|---|---|---|---|

Lead with achieved, not achieved, blocked, contradicted, or unknown. Avoid percentages that lack a measurable denominator.

For an evaluation, name the instrument, required cells or datasets, reference basis, metric, and coverage. For example, `ASR sheet: 29/45 sets, 16 pending (as of 2026-07-19)` is precise and time-bounded; `evals passed` is not.

### 3. Requirements and design

Keep durable requirements, architecture, data contracts, definitions, and accepted design decisions here. Link to deeper specifications instead of copying them.

### 4. Decisions and blockers

For every open decision or blocker, record:

- the exact question or failed gate;
- its effect on the goal or critical path;
- the owner or external dependency;
- the evidence needed to resolve it; and
- the next review or stopping condition.

Do not list resolved blockers as current. Move their outcome to the decision log.

### 5. Critical path

Show only the ordered steps required to reach the current milestone. Separate parallel support and parked work so they cannot silently displace the critical path.

End with one next action and a concrete done condition.

### 6. Evidence and log

Use links to runs, reports, artifacts, commits, dashboards, or receipts needed to audit material claims. Keep detailed chronological history in an append-only log, not in the current status section.

## Stable versus living examples

| Fact | Layer | Reason |
|---|---|---|
| Product goal | Stable | Changes only with a deliberate objective change |
| Accepted architecture | Stable | Durable decision until explicitly superseded |
| Current job state | Living | Volatile runtime evidence |
| Active blocker | Living | Must disappear when resolved |
| Why an alternative was rejected | Stable decision log | Preserves rationale without polluting current status |
| Agent heartbeat | Usually omit | Operational detail unless it changes trust or ETA |

## Freshness policy

- Assign a project-specific staleness window to volatile fields.
- Treat a living field without a verification time as unverified, not current.
- Recheck a volatile fact before every material dashboard update.
- For volatile runtime facts, display current live evidence and mark older runtime prose stale or superseded.
- Do not let observed activity override governing intent: the latest user instruction or ratified decision remains authoritative for goals, priorities, acceptance gates, and constraints. Show conflicting activity as scope drift.
- Never refresh only the visually prominent section when the same living fact appears elsewhere.

## Patterns grounded in Omni Model Base

The [Omni Model Base](https://app.notion.com/p/39ee125e3555809aa2e2e10eb09f2965) demonstrates the intended separation:

- requirements and pinned design remain stable prose;
- verdicts and experiment state live in structured row properties;
- evaluation-instrument status has one structured owner rather than duplicated prose;
- decisions append to a log and supersede earlier decisions explicitly;
- raw metrics and live job state remain canonical outside the narrative page; and
- unknown facts are written as `TBD`, never guessed.

The [July 19 Daily Report](https://app.notion.com/p/3a2e125e35558035afe0fcd750bf4b49) shows why exact evaluation identity and coverage matter: the ASR sheet was 29 of 45 sets with 16 pending. Narrower completed evaluations could not truthfully change that gate to done. The durable dashboard owns that current gate state; the daily report owns the time-bounded explanation of what changed.

## No-slop check

Before publishing, remove any sentence that cannot answer at least one question:

- What decision changes?
- Is the goal achieved or at risk?
- What must happen next?
- What is blocked, missing, or uncertain?
- What evidence makes this trustworthy?

Move supporting detail to evidence links. Delete generic claims such as `good progress`, `work continues`, `several improvements`, or `the team is focused` unless they are replaced with a verified outcome.
