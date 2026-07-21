---
name: prioritize-important-information
description: Rank available facts by their effect on the user's decision, goal, next action, risk, or trust, then surface consequential information before activity detail. Use when the user asks what matters, source material is verbose, important failures or missing work may be buried, or an agent-chosen proxy may be replacing an exact user-named acceptance gate. It can order existing audit, report, or dashboard material but does not own technical verification, audit scope, task authority, daily-report format, dashboard state, or external writes.
---

# Prioritize Important Information

Select and order information from the user's point of view. Optimize for correct decisions, not for demonstrating agent activity.

## Establish the governing intent

1. Identify the latest explicit user instruction, the current goal, and the decision or next action the user faces.
2. Treat a newer conflicting instruction as superseding the older one. Do not accumulate incompatible historical requests into one scope.
3. Identify every exact acceptance gate, named evaluation instrument, and active constraint. A proxy, simpler check, partial run, or agent-preferred metric does not replace the specified gate.
4. Separate the requested outcome from work performed. Activity is not success.
5. Keep explicit user priorities even when they score lower under a generic rubric.

If the goal, latest instruction, or reporting audience is genuinely ambiguous, ask one short question before ranking. Do not invent a priority that could reverse the user's decision.

## Apply the importance test

A fact is important when omitting it could cause a wrong decision or action. Surface a fact when it materially changes at least one of:

- the decision the user should make;
- whether the goal or milestone is achieved, on track, or late;
- the next action, owner, dependency, or stopping condition;
- risk, cost, safety, irreversibility, or ETA; or
- trust in a prior claim, result, source, or agent action.

An active prohibition or exact acceptance condition is material whenever forgetting it could authorize the wrong work or create a false completion claim.

Importance and confidence are separate. A high-impact uncertain fact remains important; label the uncertainty instead of hiding the fact.

Do not rank information higher because it was difficult, recent, verbose, technically interesting, or expensive for the agent to produce.

## Search for negative space

Before writing, explicitly check for:

- requested outcomes that did not happen;
- required evidence or gates that are missing;
- failures hidden behind successful substeps;
- current evidence that contradicts an earlier report;
- unrequested work that displaced the critical path;
- a requested evaluation or acceptance gate replaced by an easier proxy;
- active constraints or prohibitions missing from the reported state;
- stale, partial, contaminated, or unverified information; and
- decisions silently made on the user's behalf.

Absence can be more important than activity. State `not done`, `not verified`, or `unknown` plainly.

## Produce a decision-first hierarchy

Use three layers:

1. **Headline:** the single fact that most changes the user's understanding or next action.
2. **Material facts:** usually no more than five outcomes, blockers, contradictions, risks, constraints, or decisions, each with a short `why it matters` implication when it is not obvious.
3. **Supporting evidence:** tests, commands, identifiers, implementation details, and links needed to trust or act on the material facts.

Put bad news before reassuring substeps when both concern the same outcome. Preserve evidence without forcing it into the headline.

The five-item target is not permission to hide material information. If more than five facts independently change a decision or action, name every material fact on the visible decision surface. Group them only when every distinct consequence remains explicit. Links may hold supporting evidence, never unnamed material facts. Never demote a decision-changing fact merely to satisfy a length target.

Read [references/importance-examples.md](references/importance-examples.md) when the ranking is disputed, the source material is verbose, or concrete counterexamples would help.

## Preserve ownership boundaries

- Verify claims with current authoritative evidence or the relevant domain skill; this skill does not turn an assertion into proof.
- Let `write-daily-report` own the daily format and `maintain-project-dashboard` own durable dashboard structure and state.
- Treat the user-specified evaluation as the acceptance gate. Label proxy results as supporting evidence and keep the specified gate `not done` or partial until the complete named contract—required cells or datasets, reference basis, metric, and coverage—is satisfied.
- Do not edit, publish, message, launch, cancel, or otherwise mutate an external system merely because information was prioritized.
- Do not suppress supporting evidence; move it below the decision surface.
- Do not manufacture urgency, certainty, failure, or conflict to make an output appear decisive.

<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->
## Portfolio routing contract (generated)

This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.

- `skill`: "prioritize-important-information"
- `routing_role`: "content"
- `portfolio_position`: "Decision-relevance filter for status, reporting, and decision surfaces."
- `positive_request_classes`: ["requests to identify what matters","verbose status or evidence needing decision-first triage","hidden failures, missing work, contradictions, uncertainty, or scope drift","information ordering by consequence rather than activity","agent-chosen proxy work presented in place of an exact user-named acceptance gate"]
- `triggers`: ["The user asks what is important, what matters, or what is being hidden.","Verbose material needs bad-news-first ordering and an explicit negative-space check.","A simpler, partial, or different evaluation may be replacing the exact requested evaluation contract."]
- `exclusions`: ["performing technical verification or owning audit scope","daily report formatting","durable dashboard maintenance","external mutation or publication"]
- `state_owner`: "Owns the selected and ranked information hierarchy, including consequential omissions; owns neither source verification nor product state."
- `precedence`: ["The latest explicit user instruction and current goal govern the ranking.","The user-named evaluation instrument and acceptance conditions govern completion; proxy evidence remains supporting evidence.","Write Daily Report owns the daily format and Project Dashboard owns durable current-state structure."]
- `legal_compositions`: []
- `fallbacks`: [{"condition":"The request is a simple answer containing one already-confirmed fact.","route":"native-codex","result":"Answer directly without invoking a ranking workflow."}]
- `forbidden_actions`: ["rank information by agent effort or activity volume","bury bad news below successful substeps","substitute an easier evaluation for a user-named acceptance gate","turn uncertain facts into certainty","mutate or publish externally"]
<!-- END GENERATED PORTFOLIO ROUTING v1 -->
