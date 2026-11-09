# Flood-response coordination desk: reference and decision packet

Use a compact, stable comparison table with an explicit assignment workspace on the same page. Achieve the requested polish through alignment, readable hierarchy, restrained surfaces and precise state feedback. Preserve operational information before adding breathing room.

This is an unbuilt design outline. No product interaction, visual inspection, usability test or accessibility conformance assessment was performed.

## Direction and authority

Trained dispatchers compare about 30 requests repeatedly over eight-hour shifts at 1280px. Age, location, people affected, assigned crew and stale status remain visible together. Keep the exact lifecycle labels **New, Acknowledged, Assigned, Resolved**. Acknowledgement changes only acknowledgement; opening an item or preparing an assignment has no dispatch effect.

The supplied follow-up establishes that requests can be reassigned, undo is available for 30 seconds unless the crew has accepted, and acceptance arrives asynchronously. Once acceptance occurs, the correction path is a reassignment request whose pending state stays visible. All 30 requests remain reachable on the same page.

No further human direction is needed for this outline. Severity names, staleness policy, available crew attributes and reassignment authority are not supplied: preserve existing operational definitions when implementation begins. Draft examples below are illustrative, never incident records or recommended emergency policy.

## Reference matches and boundaries

| Candidate and evidence inspected in this run | Useful transfer | Mismatch and selection |
| --- | --- | --- |
| [Carbon data table guidelines](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines), text: Overview, Sizing, variants and toolbar | Task-driven row sizing, explicit column hierarchy, a toolbar for search/filtering and contextual details | Selected as structural reference. Its component sizes are options rather than a mandate. No batch dispatch: Carbon's generic multi-record actions do not justify that risk here. No sorting/keyboard/demo execution performed. |
| [Figma UI3 design account](https://www.figma.com/blog/our-approach-to-designing-ui3/), text: blend-mode and clip-content reversals | Keep repeatedly inspected state readable without opening a tooltip or menu | Selected for visible crew, stale flag and acceptance/reassignment text. This 2024 retrospective concerns creative work; it neither validates emergency dispatch nor establishes current Figma behavior. |
| [Slack unread help](https://slack.com/help/articles/226410907-View-all-your-unread-messages), official Japanese redirect, desktop mark-read/undo and refresh sections | Distinguish acknowledgement, acting on the underlying item, recovery and arrival of new information | Selected as a mechanism analogy. Message read state has lower consequences than dispatch. Do not copy swipes, bulk mark-read or treat Slack undo as evidence that a crew can be recalled. Recovery policy comes from the user. |
| [WCAG 2.2, dated Recommendation](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), text: Use of Color, Contrast, Focus Visible and Focus Not Obscured | Text/shape severity, visible keyboard focus and readable contrast across the full process | Selected as requirements basis. A normative standard is not an aesthetic reference or evidence that this concept conforms. |
| [Linear public page](https://linear.app/), local card `visual-linear-product-proof` only | Candidate for restrained framing around substantive product information | Deferred visual source: no current page or screenshot inspected in this run. Its card describes a marketing representation, not a dispatch workflow. Do not claim its dark surface, sparse outer margins or product performance fit this desk. |

The supplied appeal-versus-task card (`principle-appeal-task-distinction`) was also read as a caution; its original papers were not inspected, so no empirical conclusion is drawn here. The user's sparse portfolio references are unspecified and uninspected. Their desired finish can be honored, but copying sparse cards, oversized metrics or hidden-on-hover controls would obstruct this brief's explicit comparison task. A generous single-request card view is therefore rejected as the main queue; a detail workspace remains useful for deliberate assignment.

## Main queue outline

**Top strip:** “Flood response / Request queue”; connection text “Live · last synced 14:32:08” or the appropriate failure state; a persistent “Recent changes (4)” control. Use a small heading rather than a hero or decorative map. No invented throughput or response-time metrics.

**Toolbar:** search by request/location/crew; labeled status and severity filters; “Clear filters”; visible “30 requests” or “12 of 30 · filters applied”; sort control with direction. Counts derive from real data. Proposed initial ordering: severity then oldest first, with stable ID as a tie break. Preserve operator-selected sorting. When data changes, update visible values but do not unexpectedly move the focused row; offer “Apply updated order (3)” and flag new arrivals. Never defer a critical changed value merely to preserve position.

**Comparison table:** 16px outer gutters leave 1248px at 1280px. Proposed width budget below includes cell padding; it is a sketch budget, not measured rendering. Sticky column headings and a stable table caption identify the active sort and filters.

| Column | Proposed width | Visible content |
| --- | ---: | --- |
| Severity | 110px | Distinct shape plus full severity name/code |
| Request | 96px | Focusable request ID; opens details without acknowledging |
| Age | 76px | Elapsed since receipt, e.g. “27m”; received time available in details |
| Location | 250px | Street/site plus locality; wrap a long location rather than hide essential differences |
| People affected | 88px | Number, or “Unknown”; distinguish unknown from zero |
| Assigned crew | 152px | Crew identifier or “Unassigned”; acceptance subtext when applicable |
| Status | 130px | Exact lifecycle label; secondary pending qualifier where needed |
| Freshness | 140px | “Stale · 18m” or “Updated 2m ago”; source timestamp in details |
| Action | 206px | Named action appropriate to state; never an ambiguous icon |

Start with approximately 32px single-line rows and allow taller rows for wrapping or important qualifiers. Use 14px body text as a prototype starting point; regular weight for data, semibold IDs and exceptions, tabular numerals for ages and counts. Test actual legibility rather than shrinking text to force a viewport fit. Thirty 32px rows already require 960px before chrome: the brief gives width, not height. Keep one continuously scrollable same-page queue, with all 30 records present; no pagination, separate detail page or “next page” barrier.

Illustrative row content:

| Severity | Request | Age | Location | People affected | Assigned crew | Status | Freshness | Action |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| ▲ S1 Highest | FR-218 | 27m | East Quay / pumping station | 6 | Unassigned | New | Stale · 18m | Acknowledge |
| ◆ S2 Medium | FR-219 | 19m | Riverside school / west gate | Unknown | Unassigned | Acknowledged | Updated 2m ago | Prepare assignment |
| ● S3 Lowest | FR-220 | 12m | Mill Road / bridge approach | 2 | Crew B7 · accepted | Assigned | Updated 1m ago | Request reassignment |

These severity labels/codes are provisional presentation examples; map the actual three operational levels without changing their meanings. Shape, code and readable name provide redundant noncolor information. Status uses words; staleness includes “Stale” and elapsed report age. Color may reinforce these but never carries their sole meaning. Request age and report freshness use separate timestamps. Apply the existing staleness threshold; if none is configured, show elapsed report age and “Staleness rule unavailable” rather than inventing a cutoff.

Use pale neutral page/table surfaces, strong text, subtle horizontal rules and one restrained action accent. Selected, keyboard-focused, recently changed and severe rows must have different noncolor cues: selection marker, focus outline, “Changed” text and severity symbol/name respectively. No pulsing alarms or animated row movement. A calm appearance must retain these distinctions.

## Assignment workspace and visible results

Open an inline, full-width workspace above the table from “Prepare assignment.” It retains the queue below at its full comparison width, scroll position and selected row. The workspace can collapse without losing a draft. A visible “Return to FR-219 in queue” control restores focus to the originating row; no navigation to a separate page. Avoid squeezing the table into an illegible narrow remainder behind a side panel.

1. **Acknowledge:** activating “Acknowledge” changes New → Acknowledged after success. Row remains in place. Result: “FR-218 acknowledged by [operator] at [time]. No crew dispatched.” Failure leaves New with an inline retry/error message. Do not acknowledge on selection or focus.
2. **Prepare:** show immutable request ID, severity, full location, people, freshness and current assignment beside a labeled crew selector. No preselected crew. Selecting a crew creates only a draft. Show known crew availability/capability data only if supplied by the actual system; unknown values remain explicit.
3. **Review and dispatch:** selected crew plus request summary stays visible directly above the specifically labeled button “Dispatch Crew B7 to FR-219.” Supporting copy: “This sends the assignment to Crew B7.” Cancel returns to the unchanged request. Dispatch requires activating this distinct button; Enter in a search field cannot submit it. No extra generic “Are you sure?” dialog is needed when this review step already names the consequence.
4. **Result:** while sending, show “Sending assignment…” and prevent duplicate submission. Only confirmed success changes to Assigned and Crew B7. Show “Assigned to Crew B7 at 14:32:12 · awaiting crew acceptance” in both row and workspace, with a persistent recent-change entry. Do not imply “accepted” merely because dispatch succeeded.
5. **Asynchronous acceptance:** when acceptance arrives, update crew subtext to “Accepted at [time]” and the change history, without stealing focus or changing the lifecycle label. Announce the selected request's important outcome in a concise status message; aggregate background changes rather than reading every tick aloud.

New requests require acknowledgement before assignment in this proposed flow; that is a reversible interaction assumption for review, not a claim about a supplied backend. Acknowledgement still never dispatches. Resolved remains the existing terminal label; its criteria are outside the supplied assignment scope and are not invented here.

## Assignment recovery and concurrency

| Cause/state | Visible state and action | Result contract |
| --- | --- | --- |
| Confirmed assignment; under 30 seconds; crew has not accepted | Assigned; “Awaiting acceptance”; persistent “Undo assignment · 24s remaining” in row/workspace and recent changes | Server checks eligibility atomically. On confirmed undo, restore the preassignment acknowledgement state and prior crew where applicable; record the reversal. Do not optimistically erase the current assignment. |
| Crew accepts before timer ends | Assigned; “Accepted at [time]”; replace undo eligibility with explanation and “Request reassignment” | An already-started undo must still be checked against server acceptance. Race loss says “Crew B7 accepted before undo completed. Assignment remains active.” Offer the reassignment path. |
| Thirty seconds expire without acceptance | Assigned; “Awaiting acceptance · undo window ended”; “Request reassignment” | Expiration does not imply crew acceptance. Recovery continues through reassignment. |
| Reassignment requested | Assigned; “Reassignment pending: B7 → C2 · requested by [operator], [time]”; keep B7 as current crew | Selecting C2 and activating “Request reassignment” creates a pending request. Do not display C2 as the active crew until the authoritative reassignment succeeds. Show pending in queue, workspace and history. |
| Reassignment succeeds or is declined/fails | Show confirmed current crew and a durable outcome entry; on decline/failure retain prior assignment and draft choice | Explain the actual returned reason and permitted next action. Reassignment authority/approval mechanism remains an integration fact, not an invented role. |

The 30-second clock begins at the authoritative successful assignment timestamp. Eligibility comes from the server, including crew acceptance; the client countdown is an aid. If undo becomes unavailable while focused, keep the focused control in place with an unavailable explanation until the operator moves or chooses the next action, rather than making focus disappear. Pending reassignment is a qualifier of Assigned, never a replacement lifecycle label.

Provide an activity entry per action with request, old/new values, operator and time. Recovery must be reachable from the record/history after a transient notification disappears. Do not make a toast the only route to undo. When assignment outcome is unknown after a timeout, say “Assignment result not confirmed. Checking current assignment…”; retain the draft and block duplicate dispatch until reconciled. A failed send known to have had no effect can offer retry. If another dispatcher changed the record during review, show the difference and require review of the current assignment before sending.

## Recent changes, keyboard and degraded states

**Recent changes:** an expandable same-page list shows “14:32:12 · FR-219 · unassigned → Crew B7 · [operator]” and acceptance, undo and pending-reassignment entries. Clicking an entry reveals that request in the queue, even when filtered, without silently clearing filters; explain that it is temporarily revealed. “Changed since you last reviewed” is separate from New and from Stale. Keep timestamps and text after a brief highlight fades. Data updates can continue; automatic sorting waits for explicit application when it would move active work.

**Keyboard:** use a semantic table with real header relationships and native sort buttons, request links and action buttons. Tab/Shift+Tab reaches controls in visual order; Enter/Space activates the focused control. Do not make the entire row a hidden action or turn the table into a custom spreadsheet without implementing and testing its keyboard model. Provide skip links to Queue, Assignment workspace and Recent changes. Opening the workspace focuses its heading/first relevant control; closing restores row focus. Crew selection works with native select or a fully specified accessible search-combobox; keyboard selection alone never dispatches. No global single-letter shortcut triggers dispatch. Sticky chrome and inline messages must not hide focus.

**Recovery content:** initial load says “Loading requests”; empty filters say “No requests match these filters” with Clear filters; a genuinely empty feed says “No requests received.” If refreshing fails, retain the last known rows with a prominent “Connection lost · last synced [time]” banner and per-record timestamps. Dispatch is unavailable until crew/request freshness can be revalidated; do not silently queue dispatch while offline. Permission denial explains the unavailable action while keeping readable request context when allowed.

## Checks and handoff

Performed: source/card reading, brief-to-outline consistency review, width arithmetic (columns total 1248px), exact lifecycle-label check, review of acknowledgement/dispatch separation and recovery branches against the supplied follow-up. All are document checks.

Before acceptance of a future build, test these five scenarios:

1. At 1280px, compare all required columns across 30 realistic records, including long locations, unknown people and pending reassignment. Reach the 30th record without paging. Check zoom/text-spacing and horizontal table behavior separately from surrounding control reflow.
2. With keyboard only, acknowledge, prepare, cancel, dispatch and return to the same row. Verify visible focus and no dispatch from selection, crew search or acknowledgement.
3. Dispatch, undo within 30 seconds, then race undo against asynchronous crew acceptance. Confirm the authoritative winner, visible result and stable focus.
4. Let the timer expire or accept the assignment, request reassignment, observe pending, then success/decline. Confirm that current crew remains accurate throughout.
5. Introduce concurrent edits, new arrivals, stale data, filtered changes and an unknown send outcome. Verify clear reconciliation, no duplicate dispatch and a durable change history.

For implementation, target applicable WCAG 2.2 A/AA criteria across the entire queue/assignment/recovery process, including keyboard, color, contrast, focus, status messages and timing. The operational 30-second rule does not by itself establish a timing exception; assess the applicable timing criteria and retain the later reassignment route. No compliance or eight-hour fatigue outcome is established by this outline; observe trained dispatchers in realistic repeated tasks before claiming those results.

## Feedback revision: polish and large request cards

The follow-up explicitly favors the sparse option's polish and asks about making every request a huge card. No sparse source screenshot was inspected in this run; this preference is relayed human direction, not visual evidence. It changes the proposed presentation, while the previously supplied comparison and recovery requirements remain in force until the user changes them.

| Concrete option | What it supports | Cost at this desk |
| --- | --- | --- |
| Large card for every request | More space for each location, crew, full timestamps and individual actions; clear separation between requests | Far fewer requests visible together and more scrolling between comparable values. For illustration, 30 cards at 180px each require 5400px before gaps and chrome, versus 960px for 30 single-line 32px rows. Those are sketch arithmetic, not a rendered comparison or measured usability outcome. |
| Compact comparison queue plus a spacious selected-request card | All required columns remain aligned; the selected request gets generous spacing, full context and deliberate assignment controls | Only the selected record has the large-card presentation. The overview remains information-dense. |

Recommendation: retain the aligned queue, refine its typography/rules/spacing, and replace the selected-request workspace's plain summary with one spacious card. Place the card above the full-width table; keep request identity, crew, acceptance and pending reassignment visible in the row. The card has a clear “Return to FR-219 in queue” control and contains the unchanged acknowledgement/dispatch/recovery controls. This proposal preserves the stated comparison task while applying the new preference to the area used for individual decisions.

Provisional assumption, following the user’s instruction to proceed: rapid comparison remains the primary task, because the initial brief explicitly names comparison of about 30 requests and says keyboard use, recent changes and recovery matter more than empty space. Apply the sparse polish to the selected-request card and the queue’s restrained typography, alignment and surfaces. Keep all 30 records in the same-page table. This is a designer-selected working assumption, not a settled user preference. If later feedback prioritizes one-at-a-time inspection, revisit the overview composition; preserve the exact lifecycle labels, separate acknowledgement/dispatch actions, asynchronous acceptance and recovery rules. The outline is complete under this assumption; no reply is required to use it.
