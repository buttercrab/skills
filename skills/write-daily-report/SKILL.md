---
name: write-daily-report
description: Write a concise, decision-useful daily report from existing project evidence, with today's goal, active constraints, material changes, missing or blocked work, parallel work, exact evaluation-gate coverage, and one next action with an owner and done condition. Use for daily reports, standup updates, end-of-day reports, or today's execution handoff. Report preparation is read-only and never authorizes new evals, training, jobs, settings changes, merges, or implementation. This skill owns the daily format, not technical verification, durable dashboard state, restartable handoffs, or external publication; write externally only with explicit authority.
---

# Write Daily Report

Turn current evidence into a short execution handoff for one day. Report outcomes and decisions, not a diary of agent activity.

## Establish today's frame

1. Identify the report date, reporting window, current goal, and latest explicit user instruction.
2. Record the exact acceptance gates, named evaluation instruments, and still-active constraints that govern today's work.
3. Read the previous report only to preserve continuity and detect changes. Do not copy stale status forward.
4. Recheck volatile claims against current authoritative evidence before presenting them as current.
5. Separate critical-path work, parallel support, and parked work.

If the request supplies facts rather than live access, state that evidence boundary. Do not imply that uninspected systems were verified.

Preparing a report is read-only project work. Do not launch evals, training, jobs, settings changes, implementation, commits, merges, or other project mutations merely to fill an evidence gap. Run a named evaluation only when the user separately requested or authorized that exact evaluation contract; otherwise report `not verified` and the evidence needed.

## Select material information

Apply this compact gate even when `prioritize-important-information` is unavailable:

- Does the fact change a decision, goal status, next action, risk, ETA, or trust?
- Is it requested but not done, failed, contradictory, stale, uncertain, or outside scope?
- Did an easier proxy, partial run, or different metric get presented in place of the exact requested gate?

Use `prioritize-important-information` for deeper ranking when the source material is verbose or the user says important information has been hidden. Preserve the daily format here; the importance skill owns the detailed ranking rubric.

## Use the daily format

Write these sections in this order:

### Today

State one current commitment, its done condition, and any still-active constraint whose omission could authorize the wrong work. Do not restate the whole roadmap.

### What materially changed

Usually list no more than five verified deltas that affect the decision, milestone, critical path, risk, or ETA. Lead with the outcome, then give only the evidence needed to trust it. If more than five deltas independently change action, name every material delta inline and group only when every distinct consequence remains explicit. Links may hold supporting evidence, never unnamed material deltas.

### Not done or blocked

State requested work that remains incomplete, the exact blocker, contradictions, unverified claims, active constraints at risk, and scope drift. Say who or what can unblock it. Do not hide failure behind successful substeps.

Evaluation fidelity is literal. If the requested ASR sheet evaluation did not complete, write `ASR sheet evaluation: not done` or the exact partial coverage. Put simpler evaluations under supporting evidence; never promote them to completion of the named gate.

### In parallel

Include only useful work that does not compete with the current commitment. Omit routine agent activity and passive monitoring unless it changes the outcome.

### Next

Give exactly one action, its owner, its done condition, and a concrete ETA when one can be supported. If no action is possible, give the single external change required to unblock progress.

## Keep the report clean

- Use plain language and explain necessary acronyms or symbols.
- Prefer current outcomes over implementation detail.
- Do not duplicate the project dashboard, roadmap, experiment inventory, or full evidence ledger.
- Do not include generic progress such as `working on`, `making progress`, or `many tasks completed` without a material consequence.
- Do not mix superseded and current facts without labeling the older fact.
- Do not collapse different evaluation instruments, datasets, reference bases, metrics, or coverage into the generic claim `evals passed`.
- Do not end with several choices or an open-ended offer.

## Respect publication authority

Draft in chat unless the user explicitly authorizes writing to a named page, document, or external system. When a live report is authorized, read the current destination first, preserve its recognizable structure, update only the authorized surface, and verify the resulting content. Invocation of this skill alone never authorizes an external write or any evidence-generating project work.

Use `maintain-project-dashboard` when the request is to create or refresh the durable operating base rather than today's report. Use `write-task-handoff` when a fresh executor needs a restartable cross-session artifact.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "write-daily-report"
- `routing_role`: "content"
- `portfolio_position`: "Time-bounded daily execution report format with one next action."
- `positive_request_classes`: ["daily report","standup-style update","end-of-day report","today's execution handoff","reporting exact evaluation-gate coverage without creating new project work"]
- `triggers`: ["The user explicitly asks for a daily report, standup update, or end-of-day report.","Current evidence must be reduced to today's material changes, active constraints, and one next action.","A named evaluation gate and any non-equivalent proxy results must be reported separately."]
- `exclusions`: ["durable project dashboard refresh","restartable cross-session handoff","technical audit","external publication without explicit authority"]
- `state_owner`: "Owns daily report structure and content; owns neither truth verification, durable dashboard state, nor external publication authority."
- `precedence`: ["Owns the time-bounded daily format.","Report preparation is read-only project work and never authorizes evidence-generating evals, training, jobs, or implementation.","Prioritize Important Information owns deeper consequence ranking; Project Dashboard owns durable current state."]
- `legal_compositions`: [{"route":"prioritize-important-information","relation":"content-owner"}]
- `fallbacks`: [{"condition":"The requested artifact is a durable operating base rather than today's update.","route":"maintain-project-dashboard","result":"Use the project dashboard owner."}]
- `forbidden_actions`: ["duplicate the roadmap or durable dashboard","end with multiple next actions","hide requested work that is not done","launch evals, training, jobs, settings changes, merges, or implementation merely to fill a report evidence gap","present a simpler or partial evaluation as completion of the exact requested gate","write externally without explicit authority"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
