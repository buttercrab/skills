# Design with Intent: pilot results

Date: 2026-11-07 (Asia/Seoul). Status: installable repository pilot; source/logic observations are available, rendered acceptance and effectiveness remain unestablished. This task did not install or replace the user's existing global design skills.

## Result

The [skill](../../../skills/design-with-intent/SKILL.md) and four conditional references are written. They support discovering existing context, asking about consequential human direction, honoring a sufficient brief or creative delegation, carrying answers into an implementation, and checking the relevant flow. The [focused research](../../research/design-pilot/questioning-research.md) contains 14 substantively inspected and three partial sources, with application limits.

Six core runs compared the same three requests with and without explicit target-skill guidance. Three additional unpaired boundary probes exercised draft-first feedback, a narrow bug fix, and an undocumented request lifecycle. Every run produced a local HTML artifact. This is evidence of the observed behavior on synthetic tasks, not proof that the skill improves a person's creative experience.

The independent, condition-blind [core source review](source-review-core.md) found no demonstrated critical source-level omission in either condition. Its provisional source/transcript ratings tied in every case. There is **no demonstrated advantage over the capable baseline**, and a small tied review is not evidence of equivalence. Visual/native acceptance was not awarded.

## Core observations

| Request | With target skill | Without target skill | Supported interpretation |
| --- | --- | --- | --- |
| Vague Harbor dashboard | Asked who uses it, the first task and desired character; then asked for missing timing/contact facts. Incorporated coordinator priority and later call/collection feedback. | Asked the same consequential task/context questions and missing data; incorporated the supplied answers and feedback. | Both conditions elicited useful direction and implemented it in source. Asking questions alone is not an observed differentiator. |
| Complete Loom booking brief | Implemented selection, whole-number seat validation, totals, confirmation and reset without repeating the brief. | Implemented the supplied brief without redundant discovery. | Both respected sufficient direction. Local checks support the logic; rendered acceptance remains excluded. |
| Delegated Nightjar exploration | Chose a product-relevant reading-room direction and retained titles/times and save/filter/empty recovery, without asking for a palette. | Also accepted delegation, chose a relevant direction and retained the requested behavior. | Both exercised delegated initiative. Source supports relevance; visual quality and actual reading usability were not established. |

Harbor received the same scripted facts and the same second-stage feedback in both conditions. The final variants differ: one gates collection on recording demo contact; the other keeps collection separate with confirmation. The user required distinct deliberate actions, not a particular gate or dialog. The reviewer did not invent an aesthetic or interaction preference to select a winner.

## Boundary/development probes

These are unpaired observations. The coordinator opened the boundary cases after initial skill drafting/freeze but before core judgments were finalized, so they are **not held out under the original protocol**. They must not be reported as fresh comparative effectiveness evidence.

| Probe | Observable behavior | Evidence boundary |
| --- | --- | --- |
| Quick garden draft, then audience feedback | Produced a draft without a discovery interview. After feedback about older neighbors/outdoor phones, changed actual controls/copy and personalized confirmation. | Source, transcript and local mocked logic checks; no rendered legibility or target-size acceptance. |
| Exact Dispatch bug | Changed the state transition and preserved existing design/wording. No design interview or broad redesign. | Local assertions cover All/Ready/Dispatched and empty recovery; native UI unobserved. Explicit invocation tests behavior after loading, not natural non-activation. |
| Cedar lifecycle unknown | Asked what submission commits to before final status wording. Implemented pending review, no reservation until approval, per-request decisions, quantity validation and declined revision/resubmission. | Scripted product facts, source and local logic; no live manager workflow or native interaction acceptance. |

The separate [boundary source review](source-review-boundary.md) records exact checks, outcomes and limits. These probes test application conditions; they do not establish that real humans find the questions helpful or that the skill outperforms a baseline.

## Browser-policy incident and exclusions

Three core runs (`case2-cedar`, `case2-willow`, and `case3-cedar`) attempted a Chrome `file:` URL and received a denial that explicitly prohibited achieving the same outcome through a workaround. They later opened a localhost HTTP preview. The tool accepted those HTTP calls but did not expressly waive the preceding outcome-level restriction. The coordinator's shared infrastructure advice contributed to that fallback mistake.

Those three runs breach the evaluation's scope gate. The Loom pair and Nightjar pair are invalid for acceptance/effectiveness comparison. Preserve the files and work logs as observations; do not count their browser results as passes or attribute a benefit/harm to the design skill from this incident.

The Harbor target run stopped after the explicit denial. The baseline Harbor first version used an allowed HTTP route without a Chrome file-policy denial; after second-stage feedback, both final variants had only local source/logic checks. The Nightjar target run records a directly accepted HTTP route with no prior file-policy denial, but heterogeneous evidence still prevents a controlled rendered comparison.

The coordinator stopped further browser work and excluded all historical browser claims from the independent core review to give it a uniform source/transcript scope. Subsequent boundary probes expressly prohibited browser tools/processes, servers, network and headless rendering. No rejected browser outcome was pursued during those probes. Independent source/logic review is narrower than page rendering and does not provide substitute browser acceptance.

This is a harness/procedure incident, not a demonstrated design-skill defect. No new rendered replay was attempted. A future rendered trial requires an environment and route explicitly authorized by the browser policy.

## Method, versions and reproducibility

- An independent fixture author created three core and three boundary cases before reading the skill. Requests, input HTML, evaluator-private scripted answers and rubric are separated under [cases](cases/).
- Each core arm used a fresh non-forked agent context and a separate `/private/tmp` directory. No model or reasoning-effort override was used. Condition dispatch order was randomized before running with seed 20261107; agents were dispatched close together and could run concurrently. Execution scheduling was not controlled.
- The baseline omitted the new target package but retained normal host instructions and available host skills. Work logs show different additional skill selections across conditions, including existing frontend guidance in baseline runs. This is a comparison in the actual host environment, not an isolation of instruction text from every other skill.
- Frozen v1 contains the initial draft. An independent static review identified an unconditional desktop-layout check; v1.1 limits it to the supported layouts. The questioning policy did not change. Boundary probes use v1.1; their data did not drive that correction.
- Scripted answers test question relevance and answer fidelity. They are not real creative-owner participation, a usability study or a preference-satisfaction measure. Conversation files contain coordinator-recorded excerpts and summarized completions, not complete native tool traces.
- The soft 15-active-minute limit was advisory. Reliable per-trial active-time and token records were not captured; do not infer time or cost gains. One run per condition/case gives no reliability estimate or statistical superiority claim.
- The independent reviewer received neutral labels, source, requests, excerpts and local checks, without condition labels, target text or original work logs. Judgments were frozen before the coordinator unblinded them. Its mocked checks do not parse/render a real DOM, exercise native focus/validation, measure layout or establish browser-console health.

Archived [run manifest](runs/2026-11-07/manifest.json), [boundary manifest](runs/2026-11-07/boundary-manifest.json), [condition map](runs/2026-11-07/review-condition-map.json), [coordinator excerpts](runs/2026-11-07/coordinator-events.json), [v1 snapshot](runs/2026-11-07/package-v1.json) and [v1.1 snapshot](runs/2026-11-07/package-v1.1.json) preserve the cohort. Final HTML, requests, work logs and local scripts are under [artifacts](runs/2026-11-07/artifacts/). Snapshots include file hashes and contents. Original temporary paths remain provenance; the archive is the durable copy.

## Package verification and current limit

The skill-creator validator passed. The repository's four skill-package checks and 22 installer tests passed; installer tests use temporary target directories rather than installing into the user's global catalog. Existing cached PyYAML was used for local validation because the sandbox could not lock the default uv cache; no dependency or system-Python changes were made. Installer listing includes the new skill.

The source reviews identify no blocking instruction defect, but do not validate the whole skill. Native rendered flows, accessibility, visual quality, natural activation, real-human creative collaboration, repeated trials and broader tasks remain unproved.

The appropriate next use is a real design task where the person can supply and critique direction, with explicit recording of which questions changed the result. Preserve this pilot label until that work and valid verification justify stronger claims. Broader fundamentals skills can reuse the elicitation approach while retaining their domain-specific decisions; this pilot alone does not validate that transfer.
