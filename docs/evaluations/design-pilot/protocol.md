# Design pilot evaluation protocol

## Scope and information boundaries

This is a small local behavioral pilot, not a general benchmark or a claim that every host skill is absent. Compare **with the target skill** against **without the target skill** while holding the rest of the host environment, tools, model, effort, time budget and task artifacts constant. Record host skill availability and loading policy in the run manifest. Do not review the proposed target skill when authoring or judging fixture requirements.

Runner-visible input is only the case's `prompt.md` and `input/index.html`, plus the common sandbox instruction below. `evaluator-private.md`, this protocol, the rubric, sibling cases, trial labels and earlier results are evaluator-only. Place copies in a fresh `/private/tmp` sandbox; never expose the original case tree or its parent as the runner workspace. If a tool can read arbitrary absolute paths, instruct the runner not to discover or inspect evaluation materials beyond supplied inputs, and record any breach. For stronger separation use an isolated filesystem/container. A prompt instruction alone is not an access-control guarantee.

Common sandbox instruction, identical in both conditions:

> Edit the supplied standalone page locally. You may inspect its source and use available local browser tools to run and verify it. Use no dependency installations, external assets, external messages, publishing, real purchases or live backend writes. Keep all generated artifacts in this sandbox. Do not inspect other trials or evaluator materials. If essential information is missing, ask the user; the evaluator will relay their answer. Report the resulting file and what you actually verified.

## Cases

| ID | Role | Decisive pressure |
| --- | --- | --- |
| 01-vague-operations | Core | Discover coordinator work before choosing direction; implement a second feedback stage |
| 02-detailed-brief | Core | Execute an already sufficient brief without repeating answered discovery questions |
| 03-delegated-exploration | Core | Accept creative delegation, make a relevant choice and preserve behavior |
| 04-fast-draft | Boundary / held out | Deliver reversible draft first, then implement concrete audience feedback |
| 05-narrow-bugfix | Boundary / held out | Fix the requested state bug while respecting no-redesign scope |
| 06-material-unknown | Boundary / held out | Resolve unknown lifecycle meaning before finalizing statuses and flow |

Use 01–03 as the initial pilot. Reserve 04–06 unopened until the target skill text and initial trial judgments are frozen if reporting held-out results. If any held-out case has already influenced revision, label it boundary/development instead. Do not silently keep calling it held out.

## Execution

1. Prepare paired independent copies of each input. Use unique sandbox paths with neutral labels. Start a fresh runner context for every trial; do not reuse a context after running the paired condition. Randomize condition order within each pair and record the order before running.
2. Give the exact same prompt, common instruction and source to both conditions. The treatment change is access/instruction to use the target skill; retain all other host capabilities. Record model, loaded skills, tool availability, start/end time, and fixed resource limit. A feasible default is 15 active minutes per case excluding human-answer latency; choose and freeze the limit before the first pair.
3. Relay private scripted answers only when their trigger occurs. Match semantic intent, not wording, format or a question count. If a message bundles relevant and irrelevant questions, provide the relevant scripted facts and say unspecified minor details are delegated. Do not coach one condition toward a better question. Log every relay and its trigger.
4. For 01 and 04, send the second-stage feedback once a runnable first version is available. A first final is a stage boundary, not the trial end. Give both runners the same chance to revise. Stop only after the second response is complete or the fixed limit expires. For other cases, stop at final deliverable or limit. A blocked consequential question may end a turn but does not end the trial: answer it and resume.
5. Save the transcript, changed HTML, available screenshots/browser observations and verification record. Judge anonymized final artifacts plus the question/answer trace using `rubric.md`; do not let fluency substitute for executed behavior. Serve the page locally with existing tools if needed; never install dependencies to test it.

## Independent verification

Open final HTML in an actual browser when available. Exercise the state transitions named in the private outcomes. Record viewport, action, observed result, and whether evidence is evaluator-observed or merely runner-claimed. Review source only to clarify behavior or scope, not as a substitute for rendered interaction. If browser tooling is unavailable, retain a source-review result with verification unobserved; do not invent a pass. Do not click a `tel:` link that opens a real call application; inspect its demo affordance instead.

Use the same verification actions and viewport sizes within each pair. Suggested standard sizes: 360×800 phone and 1280×900 desktop; case 01 also 768×1024 tablet. These are test conditions, not mandatory implementation breakpoints. Do not grade an unrequested screenshot format, framework or test file.

## Reporting and limits

Report dimension scores, acceptance failures and concrete evidence per case, followed by paired differences. Separately identify completion, failed behavior, question friction and relevant creative execution; do not hide a broken workflow behind an average. Report iteration count, elapsed active time and tool errors as descriptive context. Keep sandbox failures or unavailable tools separate from design failures.

One run per condition/case is exploratory evidence only. Repeat paired trials with fresh contexts if assessing reliability; freeze changes between measured runs. Do not claim causal reliability from three favorable examples. If the target skill changes after seeing results, start a new revision cohort, label the previous cases development data, and preserve all failures.
