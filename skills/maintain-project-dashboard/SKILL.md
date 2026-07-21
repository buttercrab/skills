---
name: maintain-project-dashboard
description: Create or refresh a durable project operating dashboard or base that separates stable knowledge from timestamped living state and shows current, important information with evidence or an explicit unknown or unverified label. Use for project control towers, operating bases, Notion-style dashboards, exact acceptance-gate status, or removal of stale status, AI-generated filler, duplicated prose, and useless progress. This skill owns dashboard information architecture and current-state maintenance, not frontend UI implementation, daily reports, technical verification, task authority, or unapproved external writes.
---

# Maintain Project Dashboard

Maintain a compact decision surface for operating a project. The dashboard should answer what the goal is, what is true now, what matters, and what happens next.

## Establish target and authority

1. Identify the dashboard, audience, project boundary, latest explicit user instruction, exact acceptance gates, and requested operation: create, refresh, restructure, or audit.
2. Determine whether the user authorized an external write. If not, remain read-only and provide a proposed structure or patch.
3. Declare project-specific source precedence before changing living state.
4. Read the current dashboard before proposing replacement text. Preserve useful stable structure and user-authored intent.

Use installed provider capabilities for provider-specific reads and writes. Never infer private access or publication authority from the dashboard request alone.

## Separate stable and living state

Keep two layers:

- **Stable:** goal, exact success and evaluation criteria, requirements, architecture, durable decisions, definitions, active constraints, and rationale.
- **Living:** current milestone status, gate coverage, blockers, decisions needed, critical path, active run or experiment state, next action, evidence or explicit unknown state, owner, and verification time.

Store rapidly changing state in structured fields or databases when the surface supports them. Do not maintain the same living fact in several prose sections.

Read [references/dashboard-structure.md](references/dashboard-structure.md) when creating a new base, repairing stale structure, or deciding whether a field belongs in stable or living state.

## Establish current truth

Assign authority by fact type instead of applying one global source order:

1. the latest explicit user instruction and ratified decision record own goals, priorities, exact acceptance gates, and active constraints;
2. live system or runtime evidence owns what is actually running or happened;
3. raw artifacts and versioned metric outputs own measured results and coverage;
4. structured project databases own declared status, verdicts, and instrument state when the project assigns them that role; and
5. hand-written prose, historical reports, and session memory provide context but do not override their canonical owners.

When observed activity conflicts with governing intent, show both and label the mismatch as scope drift. Active unrequested evals are not progress toward a requested ASR sheet gate. Record an `as of` time for volatile state. Preserve high-impact unknowns with `unknown`, `not verified`, or `TBD`; do not omit them merely because evidence is missing.

## Select what belongs on the dashboard

Apply this compact gate even when `prioritize-important-information` is unavailable:

- Does the fact change a decision, goal status, next action, risk, ETA, or trust?
- Is it needed to operate the project rather than reconstruct its history?
- Does it satisfy the exact named acceptance gate, or is it only proxy evidence?

Use `prioritize-important-information` for deeper triage. Put bad news, missing work, contradictions, and decisions above routine activity. Preserve detailed evidence behind links or in an append-only log instead of crowding the decision surface.

## Refresh without AI slop

- Replace or explicitly supersede stale living state; never mix it silently with current state.
- Show progress only when it changes a gate, ETA, decision, or next action.
- Remove generic summaries, duplicated roadmap prose, speculative filler, and exhaustive agent-activity inventories.
- Give each live status an owner or source, evidence locator, and verification time when practical.
- Keep one visible critical path and one concrete next action with a done condition.
- Preserve meaningful blocked and unknown states instead of making every section look healthy.
- Keep the specified evaluation instrument `not done` or partial until its required cells, basis, metric, and coverage complete; never substitute an easier eval silently.

## Verify the resulting surface

After an authorized write, refetch or reopen the dashboard and verify that current status, links, structured properties, and important constraints survived. Check that no stale status remains in another living section. Report what changed and any evidence surface that could not be refreshed.

Use `write-daily-report` for today's concise execution handoff. Use a frontend or UI skill when the request is to implement visual dashboard software rather than maintain project truth.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "maintain-project-dashboard"
- `routing_role`: "content"
- `portfolio_position`: "Durable project operating-base structure and current-state maintenance."
- `positive_request_classes`: ["project control tower","durable operating base","Notion-style project dashboard","stale, duplicated, or useless progress cleanup","exact acceptance-gate and evaluation-instrument status"]
- `triggers`: ["The user asks to create or refresh a durable project dashboard or operating base.","Current project truth must replace stale narrative while preserving stable design knowledge.","Governing intent, observed activity, proxy evidence, and exact acceptance-gate status must remain distinct."]
- `exclusions`: ["frontend dashboard software implementation","daily report","technical audit","external writes without explicit authority"]
- `state_owner`: "Owns dashboard information architecture and the representation of living project state, including explicit unknowns and exact gate coverage; owns neither canonical product state nor task authority."
- `precedence`: ["The latest explicit instruction and ratified decisions own goals, priorities, constraints, and exact acceptance gates; live evidence owns what actually happened.","When observed activity conflicts with governing intent, show both and label the mismatch as scope drift.","Prioritize Important Information owns deeper consequence ranking; Write Daily Report owns today's time-bounded report."]
- `legal_compositions`: [{"route":"prioritize-important-information","relation":"content-owner"}]
- `fallbacks`: [{"condition":"The request is only today's update.","route":"write-daily-report","result":"Use the daily report owner."},{"condition":"The request is to build visual dashboard software.","route":"native-codex","result":"Use the relevant frontend or UI implementation workflow."}]
- `forbidden_actions`: ["present untimestamped stale status as current","show generic activity as progress","omit a consequential unknown because evidence is missing","substitute an easier evaluation for the exact named gate","duplicate living state across prose sections","write externally without explicit authority"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
