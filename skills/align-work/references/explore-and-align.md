# Explore and Align

Read this reference during discovery and after new information reopens the problem space.

## Repeat the loop

1. Inspect the authorized repository, docs, tests, runtime, logs, UI, or external evidence needed for the current uncertainty.
2. Record each material observation in `facts.md` before asking the next question round.
3. Separate observation, inference, working assumption, and unknown.
4. Ask only questions whose answers can change outcome, scope, architecture, authority, safety, risk, acceptance criteria, or the plan.
5. Record the question, meaningful options, user answer, rationale, consequences, and provenance in `decisions.md`.
6. Explore the new search space opened by the answer instead of immediately converging.
7. Append an alignment-round entry with facts and decisions added, contrary evidence checked, remaining open question IDs, and advancement verdict.

For ambiguity-driven entry, do not declare alignment immediately after the first answer. Run another exploration/reflection pass and ask a second question round when any decision-changing space remains. Do not manufacture ceremonial questions: a round may close with no outgoing question when evidence or the user's answer genuinely eliminates the remaining decision space.

## Question discipline

Explore a fact when it can be safely discovered from the authorized environment. Ask the user when the answer expresses intent, preference, authority, risk tolerance, or a decision that evidence cannot settle.

Do not batch every conceivable question. Ask a small set of highest-leverage questions, update the packet, explore their implications, then reassess.

Classify every question as answered, user-delegated, explicitly assumed with user acceptance, declined, deferred/blocking, or still open. Reassess after each round; continue only while another round could materially change the plan. Treat stateful tests, UI actions, connector calls, paid requests, and external reads with side effects as mutations requiring matching authority, not as read-only exploration.

## Stop rule

Advance to planning only when:

- no decision-changing question remains open;
- material facts have evidence and volatility labels;
- consequential assumptions are confirmed or explicitly accepted;
- meaningful alternatives and contrary evidence were checked; and
- the latest round records why planning is now justified.
