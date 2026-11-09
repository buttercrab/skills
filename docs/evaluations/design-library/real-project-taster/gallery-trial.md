# Taster: pattern discovery and selection trial

Date: 2026-11-07. Active user-selected outcome: **browse visually and collect patterns they like**. This supersedes the provisional diagnosis target and purpose-first prototype. The two-file gallery change is applied locally and gallery QA is complete, including a keyboard-focus fix. Dependencies are installed; no deployment. The final QA section supersedes the earlier validation blocker.

## Actual inspection

Read local gallery, server catalog mapper, studio selection state, board, board server mapper and detail source. Local checkout at d29fb63 is clean. Retrieved current public main gallery.tsx using GitHub connector: blob SHA f4c7c45ecd3c355a87b1103b6bc1c0c386d647e2. Current gallery retains source differences from local, including frame pausing and h2 headings. No claim that this blob identifies the entire deployed revision.

Fresh own in-app public HTTPS browser observations:

1. `/components` shows 144 components, brand controls, screen/family filters and search. Actually viewed current gallery screenshot.
2. Search `hero` returns 11 items, including Button/Input/Location map alongside hero components. This follows broad literal metadata matching; it is not evidence of semantic search failure or a measured user-task failure. Cards expose title/category, but not their already-available summary.
3. Added Product hero and Split form hero to comparison. Tray correctly reports two picks and navigates to a two-item board.
4. Board displays both runnable previews. Selecting Product hero changes its pressed label and generates a handoff naming the component/theme. Preview content and selected state observed; did not submit example forms, copy to clipboard, install code or contact another service.

Existing browser viewport is approximately 695px wide. No full responsive, keyboard, assisted-technology or user-comprehension acceptance test performed. These are agent-created sample selections, not the user's preference or chosen production design.

## What the library contributed

- **Choice-context foundation**, card inspected: make alternatives comparable using purpose and prerequisites; do not hide resources to meet an arbitrary choice count. Underlying papers were not reopened this trial; no empirical improvement claim.
- **Preference-critiquing foundation**, card inspected: show substantively different examples and allow changed criteria rather than demand an abstract style vote. The paper's apartment-search results are not design-product evidence.
- Existing **Raycast list/detail** card was considered but remains card-only this trial; no underlying visual/view or selected visual styling claim.
- Taster's own first-party catalog, pattern INDEX summaries and live flow provide the actual implementation substrate. No new framework, recommendation service or third-party skill activation is needed for this prototype.

## Applied prototype

Two in-conversation exploratory variants use three real Taster hero components and original Korean summaries/adaptation notes:

- **Find by purpose:** product explanation, first input or relevant photography → matching pattern and preparation/check notes → real component detail link → local shortlist and difference summary. Picking survives local purpose-filter changes. All three remain available through All.
- **Compare differences:** same-job candidates compared by first message, required content and reason to reconsider → local choice and preparation/check handoff. Selection can be cleared.

The prototype covers three examples, not the full 144-component catalog. It uses actual component detail URLs. It does not fabricate screenshot previews, duplicate Taster's running component engine, claim that every source pattern's optional sequence is implemented, or promise automatic matching across the catalog. The copy is an editorial proposal, not measured suitability or a user-selected brand direction.

Prototype file: `/Users/jaeyong/.codex/visualizations/2026/11/07/01a1b4d7-eb7a-7291-a63e-f00c21aba861/taster-pattern-choices.html`. JavaScript syntax checked and fragment read back. Runtime/rendering, responsive acceptance and task benefit remain unverified. No host follow-up messages or external writes are triggered by prototype controls.

## Implementation boundary after human reaction

A bounded initial implementation can expose existing summaries, carry purpose/context into board item data and preserve the existing preview/brand/shortlist behavior. Broader task-based discovery needs trustworthy task labels/aliases and an explicit no-match/escape route; it should not be presented as intelligent search merely by adding a free-text field. Preserve source/live differences and establish the current owning revision before applying any product patch.

Learning for the skill: an inspectable compare board does not itself supply comparison criteria. A concrete shortlist can reveal what the person needs explained. Keep this development example separate from the frozen cohort; no resource card was promoted from this experiment.

## Human direction received: visual browsing and collection

The user answered the pending question: **“Browse visually and collect patterns they like.”** This controls the active design. An earlier carousel event selected the purpose-first variant, but carousel navigation was not an authored preference; the explicit answer takes precedence.

Revised the prototype accordingly:

- Preview images lead; task questions and suitability paragraphs no longer gate entry.
- Name search, a saved-only view and removable thumbnail collection support browsing and collecting.
- Enlarged inspection returns to the gallery; purpose and implementation notes remain optional details.
- Three actual local Taster registry preview JPEGs were viewed and embedded unchanged: `marketing-product-hero.dark.jpg`, `marketing-split-form-hero.dark.jpg`, `marketing-photo-hero.dark.jpg`. These are repository sample previews, not newly rendered product screenshots. The Photo hero asset explicitly includes a photo placeholder; no real-photo claim.
- Uses the existing shortlist concept rather than inventing a recommendation score or requiring an interview before browsing. The three-item prototype is not the complete gallery or live component runtime.

Current response prototype: `/Users/jaeyong/.codex/visualizations/2026/11/07/01a1b4d7-eb7a-7291-a63e-f00c21aba861/taster-visual-collection.html`. Three embedded assets, approximately 163 KB, JavaScript syntax checked. No rendered/runtime acceptance or real-person task success claimed. Earlier purpose-first prototype is retained as a rejected entry framing; do not offer that as the preferred direction again unless the user changes their intent.

Skill-development observation: asking about the decision goal changed the proposed artifact substantially. That is an observed revision in this development example, not proof that questioning improves all creative work. Production implementation remains outstanding; the concept should not be described as a deployed or source-code change.


## Local implementation after the explicit direction

Applied the prepared two-file patch to `/Users/jaeyong/Development/Github/taster`:

- `web/app/components/gallery.tsx`: collapsed optional brand controls; visible Browse/Collected views; collection ignores temporary browsing filters while preserving them on return; item-specific removal via a thumbnail list; existing comparison link and pick order retained. Empty collection has a return route. No forced task questions or expanded suitability paragraphs on visual cards.
- `web/app/components/gallery.css`: token-based layout for the optional controls and collection thumbnails; wrapping items and existing 44px interaction targets.

Patch: [visual-collection.patch](visual-collection.patch). Before/after source hashes: [visual-collection-hashes.json](visual-collection-hashes.json). Source hashes were checked before applying; the checkout was clean beforehand. Local/deployed source differences outside this patch were preserved, including newer upstream preview-frame logic not present in the local base; no whole-file upstream synchronization was attempted.

The current visual companion is `taster-visual-collection.html` in the conversation visualization directory. Its static preview assets come from Taster's existing repository and were viewed before embedding unchanged. It is a three-example demonstration, not the running 144-item gallery.

Validation: `git diff --check` passed; exactly two product files changed. Before/after hashes verified after applying. Production graph lookup returned no Taster nodes; that does not prove no deployed resources exist. No production change occurred.

Validation blocked: locked dependency installation in the isolated source copy failed (sandbox DNS failure, then escalated network timeout); an offline attempt confirmed the missing `csstype` tarball. No complete TypeScript, build or local browser acceptance run was possible. An overlapping install was started before the initial installer exited; both exited, and no install was performed in the actual checkout. Do not call this implementation runtime-verified. The prototype JavaScript passed a syntax check, which does not validate the React implementation or interaction behavior.

Remaining work: once dependency downloads work, run the existing web typecheck/build, then inspect the real gallery at desktop/narrow widths and exercise collection across filters, removal/empty state, reload persistence and comparison navigation. Preserve current source work; no commit, push, deployment or global skill installation was made.

## Completed gallery QA — 2026-11-07

The user explicitly requested fixing dependency installation and finishing gallery testing. This section supersedes the earlier validation blocker; those attempts remain historical records.

### Dependency recovery

Official npm registry access succeeded with authorized network access. A fresh isolated source copy installed the exact locked web dependencies (48 packages) and the documented production engine dependencies (98 packages). The same verified cache then installed both into the actual checkout offline. No package manifest, lockfile or dependency version changed. Commands use `npm ci --ignore-scripts --no-audit --no-fund`; engine also uses `--omit=dev`. Dependency downloads are complete; ordinary development commands now work from the actual checkout.

### Defect found and fixed

Keyboard activation of a collection removal button originally unmounted the focused element and dropped focus to BODY. The tested fix in `gallery.tsx` restores focus after React commits: tray removal returns to its summary while picks remain; last-item removal and clearing return to the stable Collected-view control; card removal in Collected view also returns there. Initial hydration and ordinary additions do not move focus. A transient ref records only the requested focus destination.

### Final checks

| Check | Result and scope |
| --- | --- |
| `npm run typecheck` | Passed in the actual checkout after the final fix. |
| `npm run build` | Passed in the actual checkout; Next.js compiled and generated all 151 routes/pages. |
| `npm test` | 11 passed, zero failed/skipped in the actual checkout with required loopback permission and engine dependencies. Earlier sandbox EPERM and missing-engine-package runs are setup failures, not passes. |
| Source consistency | Exactly gallery.tsx/gallery.css modified; `git diff --check` passed; final source bytes match the tested QA copy; manifests/locks match the initial copy. |
| Page identity / visible content / framework overlay | Correct `/components` title and substantive gallery in production mode; no error overlay observed. |
| Console | No warning/error entries observed during the tested gallery → board → gallery sequence. |
| Desktop | In-app browser, 1440×900. Three-column grid and two selected preview cards visually inspected; loaded preview images confirmed. |
| Narrow layouts | 390×844 visually inspected; document width equals viewport at both 390 and 320×740. No horizontal overflow in tested states; collection and card action targets measured 44px high at 390px. |
| Empty/recovery | Empty Collected view, return to browsing, clear-to-empty and last-item removal exercised. |
| Collection/filter relationship | Collected view includes picks despite unrelated search; query `hero`, screen `landing` and family `sections` restore when returning to browsing. |
| Limit / order / persistence | Six-pick cap disables unselected items; chosen insertion order retained in comparison URL; existing picks restored after reload/hydration. |
| Brand/theme | Keyboard opens collapsed brand controls; light theme changes preview URL and comparison theme; dark restored. No site-brand extraction submitted. |
| Keyboard focus | Final build exercised tray removal, Collected-card removal, clearing and final removal; focus returns to the expected live summary/button. |
| Comparison / handoff | Two selected components reach the board in order; Product hero selection produces the expected handoff text; live frames render. No clipboard write, installation command, external form submission or message sending. |

Browser interactions used the available native CUA in-app browser; the separate Browser plugin/skill was not listed. No headless or alternative browser fallback was needed. Tests used the actual built checkout on `http://127.0.0.1:3240`; temporary viewport overrides were reset, agent QA tabs closed, and the test server stopped. One screenshot taken immediately after a viewport change was inconsistent with layout; it was not used as final evidence. The final desktop capture followed an explicit 1440px viewport/1440px document-width and three-column geometry check.

Final source artifacts: [tested patch](visual-collection-tested.patch), [tested source hashes](visual-collection-tested-hashes.json). Earlier `visual-collection.patch` remains the pre-QA proposal. Final screenshots are `/Users/jaeyong/.codex/visualizations/2026/11/07/01a1b4d7-eb7a-7291-a63e-f00c21aba861/taster-gallery-tested-desktop.jpg` and `taster-gallery-tested-mobile.jpg` in the same directory. Logs remain under `/private/tmp/taster-gallery-checkout-{build,tests}.log`.

This is bounded gallery-flow validation in one browser engine, not complete acceptance of every component, automated accessibility conformance, other browsers or real-user preference/task research. No commit, push or deployment occurred.
