# Importance examples

Use these examples to distinguish decision-changing information from supporting detail. The same fact can move between layers when the user's decision changes.

## Contents

- Outcome before substeps
- Resolved blocker before historical effort
- Scope drift before activity volume
- Exact evaluation contract before proxy results
- Contradiction before polished presentation
- Important does not mean negative
- When supporting detail becomes important
- Usually low-value headline material

## Outcome before substeps

Source facts:

- both ranks passed 62 focused tests;
- distributed initialization succeeded;
- the training process failed before its first finite loss; and
- the requested full run was never submitted.

Decision-first output:

> **The requested model is not training.** The final smoke failed before first loss, so the full run was not submitted.

Supporting evidence:

> Both ranks passed 62 tests and initialized distributed training before the cache-path failure.

The tests are useful evidence, but presenting them first would imply more success than the outcome supports.

## Resolved blocker before historical effort

Source facts:

- several cleanup passes targeted a storage floor;
- older reports call storage the launch blocker; and
- current live telemetry shows ample free space.

Decision-first output:

> **Storage is no longer the launch blocker.** The remaining gate is the container-visible cache path.

The cleanup history belongs in supporting detail unless the user is auditing deletion safety or cost.

## Scope drift before activity volume

Source facts:

- the user asked for an answer without changes;
- agents launched additional evaluation work; and
- the requested training launch remained pending.

Decision-first output:

> **Agents performed unrequested evaluation work while the requested training launch remained undone.**

The number of evaluation jobs, reports, graphs, and refreshed links is secondary to the authority and priority drift.

## Exact evaluation contract before proxy results

Source facts:

- the user requested the named ASR sheet evaluation;
- the sheet completed 29 of 45 required sets, with 16 still pending; and
- several simpler or narrower evaluations completed.

Decision-first output:

> **The requested ASR sheet evaluation is incomplete: 29 of 45 sets ran and 16 remain.** The simpler evaluations are supporting evidence, not a substitute for the named acceptance gate.

Never summarize this as `evals completed`. The instrument, coverage, reference basis, metric, and required cells are part of the evaluation contract. If any required part changes, label the result partial or non-equivalent unless the user explicitly approves the substitution.

## Contradiction before polished presentation

Source facts:

- a dashboard says an instrument is not yet run;
- current artifacts show the instrument completed; and
- the dashboard contains a detailed explanation of the earlier plan.

Decision-first output:

> **The dashboard is stale and should not be used for the current decision.** Live evidence shows the instrument completed.

The polished explanation does not compensate for stale state.

## Important does not mean negative

Positive facts are important when they change action:

- a required gate passed and execution may proceed;
- a blocker disappeared;
- a costly job completed successfully;
- the user no longer needs to decide; or
- a previously uncertain result became verified.

Example:

> **Both prerequisite tracks completed successfully; only the combined track remains.**

## When supporting detail becomes important

Normally supporting details can become headline material when they control the decision:

- a test result is important when it is the final acceptance gate;
- a commit hash is important when provenance or reproducibility is disputed;
- a job identifier is important when the user must cancel, inspect, or distinguish duplicates;
- a timestamp is important when staleness changes trust; and
- a log path is important when it is the first action required to diagnose a blocker.

Ask: **Would omitting this detail plausibly change what the user does next?** If not, keep it below the decision surface.

## Usually low-value headline material

Unless it changes a gate or decision, keep these in evidence or omit them:

- heartbeat refreshes;
- counts of files, agents, messages, or commands;
- routine test names after the required suite has already passed;
- exact log directories that the user does not need to open;
- generic statements such as `making progress`, `work is ongoing`, or `several improvements were made`; and
- implementation detail with no consequence, risk, or requested explanatory value.
