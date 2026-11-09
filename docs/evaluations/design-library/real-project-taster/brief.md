# Taster: first real-project design-library trial

Date: 2026-11-07. Status: initial diagnosis exploration superseded by the user’s explicit selection of **pattern browsing and choosing**. Retained below as exploration history, not the active scope. See [gallery trial](gallery-trial.md). No product code edits or deployment.

## Scope and settled facts

The user accepted trying the new library on a real project, following a proposal to start with Taster. The provisional bounded target is diagnosis results: submit site → understand findings → choose a next improvement. A question about diagnosis, first visit or pattern browsing remains pending; this provisional focus is not a recorded human selection.

Local checkout `/Users/jaeyong/Development/Github/taster` is clean at `d29fb63`. It is older than the observed deployment: the live page has revised privacy/caveat/comparison copy absent from local `web/app/diagnose.tsx`. Do not overwrite those deployed changes from an older source. Establish the owning current revision before editing product files. The checkout is outside this task's writable roots; prepare any requested patch concretely before a write escalation.

The local source exposes URL, measured/rulesHit/findings, widths, rule severity/name/fix/fix_patterns, up to three distinct selector findings per rule, optional screenshots and unmeasured rules. The result is an ephemeral run; no durable saved issue queue or automatic code-fix confirmation is established.

## Observed current journey

Own in-app browser public HTTPS page at https://taster-six.vercel.app/. Entry and result screenshots actually viewed at the existing approximately 695px-wide viewport. No mobile/desktop breakpoint matrix or native app inspection.

1. Selected the site's supplied slop fixture, then submitted `https://taster-six.vercel.app/fixtures/slop.html` once. No private/customer URL was supplied.
2. Running state disabled the diagnose button and announced elapsed seconds.
3. Completion focused the result region and reported 66 of 85 measurable rules hit, plus three eye-only rules. These counts belong to this intentionally problematic fixture and run.
4. Results show two large annotated capture figures before the long rule list. Rule rows expose counts/severity, plain-text pattern IDs and expandable evidence. The live page explicitly cautions that a hit does not prove AI authorship.

This provides a concrete design hypothesis: visitors may have difficulty connecting a finding, its visual/source evidence and a next action. No user task/comprehension test has demonstrated that difficulty; do not call it a measured usability failure.

## Resource survey and decisions

Surveyed local catalog diagnostic/review families and read three complete cards: `tool-lighthouse`, `flow-linear-triage-decisions`, `visual-raycast-list-detail`. Broad literal review search is noisy because mismatch/body mentions also match; discovery required inspecting actual role/context.

| Resource | Inspected scope | Useful portion | Mismatch / disposition |
| --- | --- | --- | --- |
| [Lighthouse overview](https://developer.chrome.com/docs/lighthouse/overview) | Fresh primary text: report/audit explanation; card read | Audit → why it matters → how to improve | Broad automated quality is different from Taster's editorial heuristics. Use explanation mechanism; avoid borrowing an aggregate beauty score. |
| [Chrome DevTools Issues](https://developer.chrome.com/docs/devtools/issues) | Fresh primary text: View items / affected resources / context | Finding title, explanation, affected resources, further guidance grouped together | Outside the catalog; live documentation has historical update date and experimental-feature caveats. Use documented information relationship, no claim to have used current DevTools UI. |
| [Linear Triage](https://linear.app/docs/triage) | Fresh primary text: Take actions; local flow card read | Separate inspect/review from authoritative disposition | Taster has no durable team queue/resolution backend. Reject accept/decline/snooze workflow for this first change; no “fixed” claim without rerun. |
| [Raycast](https://www.raycast.com/) | Catalog card only; underlying visual not viewed this trial | Possible future list/selected-detail composition | Desktop metaphor and compactness need validation; not a visually verified chosen reference in this trial. |

No third-party skill installed or automatically activated. DevTools is a new inspected lead here, not silently added to the frozen catalog.

## Two substantive directions for human critique

### A. Explain the findings

For a person who needs to understand what the rule means before acting.

Result heading and scope → readable issue index → selected issue's plain explanation, count by width, example evidence and relevant pattern link → optional full captures → rerun.

Show rule IDs as supporting detail. Keep engine severity distinct from a recommendation about what matters to this particular site. Preserve eye-only and AI-authorship caveats near the summary. Link patterns only after verifying route/ID mapping. Do not invent a preferred fix among unrelated taxonomy suggestions. On narrow layouts use an in-flow detail region/back-to-list, not tiny side-by-side panels.

Source transfer: Lighthouse's why/how mechanism, DevTools' affected-resource/context relationship. Proposed improvement is explanation and evidence locality, not a new scoring model.

### B. Inspect the evidence

For a developer who wants to locate and assess many findings rapidly.

Result heading and scope → compact rule list with actual counts/severity → selected rule's selector/evidence and width controls alongside or immediately before the matching capture → real pattern-detail links → rerun.

Keep position in the list when inspecting. Existing report captures outline all findings, so do not promise per-rule image highlighting without changing capture/rect data. Existing payload trims selector samples, so say examples rather than all affected elements. No fixed/resolved state without a new diagnostic result. On narrow layouts move list → one detail → back while retaining selection.

Source transfer: DevTools' structured issue detail. Raycast remains a candidate for visual comparison if B is selected; no dark desktop styling is assumed.

A mixture could keep B's scannable index and A's explanations. Neither changes detector criteria, automatic repair, storage or branding by default.

## Decision and verification boundary

Pending human-owned direction: prioritize helping newcomers interpret results, or helping developers inspect evidence? The earlier project-area question may supersede both directions. No target audience, mascot, visual personality or redesign preference was invented.

After selection: inspect current owning source revision; verify pattern routes and summary contracts; implement bounded result presentation; test populated/zero/eye-only/missing-capture/error states and keyboard/narrow layouts. Preserve deployment-only copy. Report source relationships, implementation behavior and actual user evaluation separately.

Learning to take back to the library: diagnostic-report interaction was a sparse region; the external DevTools source supplied a closer mechanism than a generic queue. Ask about the user's next decision before treating a selected visual layout as the answer. Keep this development case separate from the frozen eight-case cohort.
