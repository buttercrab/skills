# Frozen boundary/development source review

Three additional unpaired boundary/development probes; NOT held-out and NOT paired efficacy evidence. Core judgments remain unchanged.

Read only boundary-items.json, designated probe dirs and original boundary private criteria; source/transcript plus audited local mocked logic. No browser, servers, network, headless rendering, installs, target skill, condition map or root manifests.

Condition labels remain unknown. No comparison or efficacy conclusion is drawn. Core review files were not changed.

## Evidence and scores

**Pass** denotes a recorded excerpt fact, artifact existence or local check execution. **Source-supported** denotes supported implementation/logic, not a rendered pass. All native/rendered acceptance is **unobserved**. No critical source-level failure was demonstrated.

| Probe | Human direction | States/recovery | Creative relevance/scope | Friction/autonomy |
| --- | --- | --- | --- | --- |
| probe-04 | 3 | 2 | 2 | 3 |
| probe-05 | 3 | 2 | 3 | 3 |
| probe-06 | 3 | 2 | 2 | 3 |

Scores are source/transcript-limited. Functional gaps reflect unavailable native verification, not demonstrated workflow defects. Probe-05 scope fit is directly assessable because the user requested preservation and a minimal state repair, rather than visual design. No total/ranking is inferred.

## probe-04 — 04-fast-draft

Artifact: `/private/tmp/design-with-intent-pilot-20261107/review-input/probe-04/index.html`

Transcript evidence:
- conversation.md first-draft records a runnable draft before discovery interview, then user feedback specifying neighbors aged 65+, outdoor older-phone use, bigger controls, plain language and name/shift confirmation.
- conversation.md final records the implemented revision and logic checks. The initial draft artifact and full native trace are not supplied, so its runnability cannot be independently reconstructed.

| Concrete outcome | Judgment | Evidence |
| --- | --- | --- |
| Recorded draft-first then feedback sequence | pass | Excerpt contains first-draft, user feedback and final revision in that order; no preceding discovery question is included. |
| Initial draft independently runnable before feedback | unobserved | Only final HTML is supplied; the initial stage is coordinator-recorded, not independently executable here. |
| Feedback changes implemented in actual controls | source-supported | Later CSS overrides set labels/input/select/button text to 22px and controls to minimum 64px; single-column fields and direct plain signup instructions replace the earlier decorative composition. |
| Welcoming without decorative interference | source-supported | Final markup removes the large garden illustration and decorative headline composition; small local brand SVG remains. Actual distraction/visual readability cannot be judged. |
| Blank/whitespace name gives useful recoverable error | source-supported | Submit uses trimmed name, sets aria-invalid, error class, named guidance and focus call; reviewer mock exercises whitespace input. |
| Correction succeeds and removes error state | source-supported | Valid trimmed name flips aria-invalid false, removes error class, adds success class and updates the message; reviewer mock passes. |
| Personal confirmation names participant and chosen shift | source-supported | Confirmation interpolates trimmed name and shift.value. Reviewer mock exercises both shifts with Robin. |
| Both original shifts retained | source-supported | Final select retains 09:00 — Watering and 11:00 — Harvest. |
| Local working final artifact and script syntax | pass | Final index.html exists; inline script parses; mocked final logic checks pass. |
| Outdoor legibility, phone tap usability and rendered narrow verification | unobserved | CSS intent is measurable but no rendering/native tests are admissible; older-phone support and outdoor readability are not established. |

Details and omissions:
- No demonstrated critical source-level omission in final feedback implementation.
- Old draft CSS remains before the overriding final rules, including unused illustration selectors. This is residual local code, not proof that removed artwork remains visible or that revision failed.
- Do not treat 22px/64px as rubric requirements; they are evidence this artifact actually changed its controls, not a universal acceptance threshold.
- reviewer-boundary-checks.cjs: inspected/written locally, passes whitespace-name validation, correction, both shift confirmations and classes. Values/events/classList/focus are mocked.

## probe-05 — 05-narrow-bugfix

Artifact: `/private/tmp/design-with-intent-pilot-20261107/review-input/probe-05/index.html`

Transcript evidence:
- conversation.md final records fixing dispatch state before rendering, no questions, unchanged design wording, local assertions and no rendered/native verification.
- request.md explicitly limits scope to dispatch state/filter bug and preserves design/wording.

| Concrete outcome | Judgment | Evidence |
| --- | --- | --- |
| Direct narrow execution without design interview | pass | No clarification questions in supplied excerpts; final source implements the requested state mutation. |
| Dispatch mutates only identified parcel | source-supported | queue.onclick finds matching dataset.id then sets p.state='Dispatched'; reviewer mock confirms P-81 changes while P-82 remains Ready. |
| All shows Dispatched and removes its Dispatch action | source-supported | Existing render emits current state and only generates Dispatch button for Ready; mock verifies P-81 status/action removal. |
| Ready excludes dispatched parcel | source-supported | Filter compares p.state with filter.value; mock verifies P-81 absent and P-82 present. |
| Dispatched includes dispatched parcel | source-supported | Mock verifies Dispatched view shows P-81 and not Ready P-82. |
| Dispatching both yields Ready empty state | source-supported | Mock dispatches second parcel while Ready filtered; output is No parcels in this view. |
| Switching All recovers both records | source-supported | Mock changes filter to All and confirms both Dispatched rows without Dispatch buttons. |
| Confirmation names parcel | source-supported | notice.textContent=p.id+' dispatched.'; mock verifies P-81 dispatched. |
| Existing design, wording and narrow scope preserved | source-supported | Final artifact retains the fixture structure, CSS, labels, views, confirmation and empty wording. The behavioral repair is the added state assignment; no redesign, persistence, backend, unrelated new controls or refactor is introduced. |
| Final artifact, parse and local logic checks | pass | index.html exists and script parses; reviewer mock exercises requested transitions. |
| Rendered state/filter and native event behavior | unobserved | Mock provides queue/filter/notice globals directly; native named-element globals, DOM event target behavior and rendering remain untested. |

Details and omissions:
- No demonstrated source-level omission or scope expansion.
- No visual redesign was requested; preserving the existing design and limiting the implementation earns scope-fit credit without demanding embellishment.
- reviewer-boundary-checks.cjs passes identified parcel isolation, All/Ready/Dispatched, action removal, named confirmation, empty and All recovery. Mock uses supplied globals instead of a native DOM.

## probe-06 — 06-material-unknown

Artifact: `/private/tmp/design-with-intent-pilot-20261107/review-input/probe-06/index.html`

Transcript evidence:
- conversation.md question targets who reviews, decline/change outcomes, result communication and when materials are reserved or guaranteed; this resolves the prompt’s consequential lifecycle unknown.
- conversation.md answer defines review queue, stock check, per-request approve/decline, no reservation until approval, declined revision/resubmit and whole-number 1–20 quantity.
- conversation.md final reports those requirements implemented with Node logic checks and no rendered/native verification.

| Concrete outcome | Judgment | Evidence |
| --- | --- | --- |
| Targeted lifecycle question before implementation final | pass | Recorded question precedes supplied answer and final; asks meaning/commitment rather than cosmetic preferences. |
| Submission meaning and no reservation before approval clear in source | source-supported | Intro/process/form/list copy distinguishes request, pending review and manager stock check; confirmations explicitly say no materials reserved while pending. |
| Valid new request is pending review, not guaranteed | source-supported | Submit creates status:'pending'; render badge/detail and announce show pending review, not approved. Supplied mock confirms. |
| Per-request demo approval and decline produce distinct states | source-supported | Each pending row constructs two bound button handlers using record.id; setDecision updates only pending matching record and rerenders distinct badge/detail. Mock exercises decline and approval with another record present. |
| Declined request supports quantity revision and resubmission | source-supported | Declined row includes its own revision form; valid submit updates same record quantity, returns status to pending, increments attempts, rerenders and announces renewed review; mock passes decline/revise/resubmit. |
| Empty/0/21/fraction quantities cannot create request | source-supported | validQuantity requires nonempty integer 1–20; failed validate returns before creation. Audited mock exercises these plus negative/nonnumeric/Infinity; records remain empty. |
| Useful invalid correction, draft preservation and boundaries | source-supported | Error gives whole-number 1–20 instruction, sets aria-invalid/focus, preserves input; revision.draft persists across unrelated renders. Mock verifies invalid revision stays declined, other request does not clear draft, and 1/20 bounds. |
| Approval is guarded and remains simulated | source-supported | setDecision returns unless pending; approved copy says real reservation not made. Mock confirms attempted decline after approval has no effect. |
| Final artifact, syntax and audited supplied local logic checks | pass | index.html exists; check.cjs uses only local fs/vm/assert and DOM stand-ins; reviewer execution passes all assertions. |
| Actual native controls, focus, revised-state rendering and responsive usability | unobserved | No browser/rendering allowed. Mock checks method calls and generated state, not native DOM controls or layout. |

Details and omissions:
- No demonstrated critical source-level omission. Result communication is local request status and demo controls, clearly described as local only.
- New form retains entered values after successful submission; clearing them was not requested. No duplicate-prevention requirement was supplied.
- Initial empty list/count come from static HTML; no initial render() call is necessary for this fixture to show empty state.
- probe-06/check.cjs inspected before execution: reads sibling index.html, constructs local DOM stand-ins, runs inline script via VM and asserts state/markup. Passed. It does not prove actual selector/event/native validity or CSS behavior.

## Limitations

- Conversation excerpts are coordinator-selected summaries, not full native tool traces.
- Final HTML only: initial draft runnability in probe-04 cannot be independently reconstructed.
- Mock DOM tests bypass HTML parsing, real selectors, native number/select/form/dialog behavior, event delivery and focus.
- All native/rendered/layout/viewport/visual usability acceptance remains unobserved. Source-supported absence of outbound integrations does not prove every historic tool action respected scope.
- Root handles policy incidents separately. No superiority, causal effect or general reliability inference is made.
