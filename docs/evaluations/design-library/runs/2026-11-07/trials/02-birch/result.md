# Flood-response desk: reference and decision packet

Use a compact, full-width request table, with a separate crew review and dispatch action. Carry the portfolio reference's polish into alignment, typography and restrained surfaces; reserve space for comparing operational facts.

This is a proposed screen/content outline, not an implemented or usability-tested system. The brief settles the audience, task and principal tradeoff; no style interview is needed. Existing status labels remain **New, Acknowledged, Assigned, Resolved**.

## Reference matches

| Reference / inspected scope | Useful fit | Decisive mismatch | Selected application |
| --- | --- | --- | --- |
| [Carbon data table: sizing](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines#sizing), placement, sorting, actions. Primary text read; native Chrome sizing table and xs/sm/md comparison diagrams viewed. | A real density vocabulary and stable column comparison, with separate row action targets. | General enterprise data, no field dispatch semantics; its exact dimensions are system conventions. Static diagrams do not establish eight-hour comfort. | Start with 32px single-line rows and visible columns; grow rows for wrapping/overrides. Give the queue the full width. No bulk dispatch. |
| [Figma UI3: blend modes and clip content](https://www.figma.com/blog/our-approach-to-designing-ui3/). Historical first-party account read; images not inspected in this task. | Describes the repeated cost of hiding a frequently inspected setting and restoring a more explicit control. | Drawing properties differ from emergency operations; no measured dispatch benefit. | Crew, status and stale information stay visible. Hide occasional history detail, never the value needed to compare requests. |
| [Linear Triage: Take actions](https://linear.app/docs/triage#take-actions). Current first-party documentation read; no live workspace or visual inspection. | Explicit decisions have distinct consequences. | Accepting moves an issue into a default status; snooze can hide work from colleagues. Neither is the desk's workflow. | Write each transition and result explicitly. Retain the four supplied labels; do not add Accept, Snoozed or Declined, or hide unresolved requests. |
| [Slack: unread messages](https://slack.com/help/articles/226410907-View-all-your-unread-messages), mark read/undo and refresh. Official page redirected to Japanese; relevant text read. | Separates acknowledgement, returning to the source, and loading new items; offers recovery. | Reading state is not business completion. Undoing a read marker cannot recall a physical crew. | Keep acknowledgement separate from dispatch. Show recent changes and persistent recovery access; use server-confirmed reversal for assignment. |
| [Fluent 2 dialog](https://fluent2.microsoft.design/components/web/react/core/dialog/usage), types, focus and content. Primary text read; no component operated. | Gives the deliberate dispatch review a focused interruption, clear consequence and return focus. | React component documentation, marked Preview; no requirement to adopt Fluent or interrupt every operation. | Use one focused dispatch review, specific action labels, Cancel, and focus restoration. Acknowledge stays inline. |

The library had useful operational analogues but no inspected flood-dispatch workflow. A targeted primary-source expansion found [PagerDuty incident statuses and timeline](https://docs.pagerduty.com/incident-management/incidents/overview#incident-statuses). Its documented acknowledgement claims ownership and halts escalation: **do not transfer that meaning here**. Borrow only timestamped change history. A request's acknowledgement must not allocate a crew, send a dispatch instruction or silently stop operational escalation.

The sparse portfolio dashboard is unnamed, so no particular portfolio screen was inspected. Its requested quality can guide finish, but not prove task fit. Large cards, oversized metrics and extensive gutters would make approximately 30 requests harder to compare at 1280px. Preserve polish through crisp column baselines, quiet separators, consistent button weights, tabular numerals and readable text. Avoid a decorative map, hero greeting or chart strip above the queue.

## Main queue at 1280px

A compact top bar holds “Flood response”, service/data freshness and the current operator. Below: “Requests”, visible result count, search by request/location, status and severity filters, “Stale only”, and a persistent “Recent changes” control with unseen count. Use ordinary labeled filter controls; active filters remain visible with Clear filters. Default view includes all unresolved requests; Resolved remains accessible through the same status filter.

Use 24px page margins, leaving a proposed 1232px table. The following is a width budget, not a rendered fit claim:

| Column | Width budget | Always-visible content |
| --- | ---: | --- |
| Severity | 56 | Shape plus S1/S2/S3; full meaning in accessible name and visible legend |
| Request | 80 | Stable linked request ID |
| Age | 72 | Elapsed since received, e.g. 38m; exact received timestamp in detail |
| Location | 280 | Address/landmark; wrap long values rather than silently clipping decisive location |
| People | 72 | Count; “Unknown” rather than zero for missing data |
| Assigned crew | 168 | Crew name or “Unassigned”; no hover needed |
| Status | 144 | New / Acknowledged / Assigned / Resolved |
| Last update | 136 | Elapsed, explicit “Stale” where applicable, exact timestamp in detail |
| Actions | 224 | State-appropriate labeled actions, separated targets |

These budgets total 1232px and include cell padding. Start at 14px body text with 32px minimum rows, a neutral sans serif and tabular numeric columns. Use sufficient text contrast; secondary timestamps must still be readable. A row hover helps tracking across columns, with a separate visible focus outline. Status is plain text in a restrained tag; severity gets stronger emphasis. No pulsating rows or perpetual flashing. Full location and notes remain accessible by keyboard in detail; wrapped content increases height.

Thirty minimum-height rows require 960px before headers and controls. The brief specifies width, not height: this design does **not** promise 30 rows simultaneously visible on a typical laptop. Keep the roughly 30 requests in one scrollable table, with sticky headers and no pagination that splits comparison. Offer a comfortable density option; do not reduce text to force all rows into one viewport.

Illustrative records, not operational data:

| Severity | Request | Age | Location | People | Assigned crew | Status | Last update | Actions |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| ▲ S1 | F-1042 | 38m | Riverside Rd / north bridge | 6 | Unassigned | New | Stale · 18m | Acknowledge · Assign crew… |
| ◆ S2 | F-1035 | 52m | Eastbank community hall | 18 | Boat 03 | Assigned | 2m | View assignment |
| ● S3 | F-1027 | 1h 12m | West depot access road | Unknown | Unassigned | Acknowledged | 4m | Assign crew… |

S1/S2/S3 are provisional display codes, highest to lowest; retain the service's approved severity names/definitions when supplied. The shapes and text must remain distinct in grayscale. “Stale” is an independent freshness flag, never a fifth status. Request age and time since authoritative update are different clocks. Staleness thresholds and which updates reset them must come from operations policy; no safety threshold is invented here.

Default proposed sort is severity, then oldest received within severity, with request ID as a stable tie break. Expose the active sort in text. Operator sorting by age/location/crew remains explicit. This priority order is a reviewable assumption, not a flood-response policy.

## State and action contract

| Trigger | Proposed result | Visible proof / recovery |
| --- | --- | --- |
| Activate Acknowledge on New | On confirmed write: Acknowledged. No crew assignment or dispatch side effect. | Row updates in place; “F-1042 acknowledged by [operator] at [time]. No crew dispatched.” Event retained in history. Failure retains New. |
| Activate Assign crew… | Open review; request status unchanged. Selecting a crew is a draft only. | Title “Assign crew to F-1042”; request ID, severity, location, people and current status repeated alongside available crew facts. |
| Activate “Dispatch Boat 07” in review | Revalidate request/crew and submit once. On confirmed authoritative success: Assigned, Boat 07. | “F-1042 assigned to Boat 07 at [time]”; separate dispatch-delivery result. Assignment confirmation never implies crew receipt or arrival. |
| Activate Resolve from request detail | Follow the service's authorized resolution policy; require deliberate confirmation with request context. | Confirmed status becomes Resolved, resolution event remains accessible. No automatic resolution from acknowledgement, assignment or elapsed time. |

Proposed dispatch review: request summary first, crew selector second, consequences last: “Dispatch Boat 07 to F-1042, Riverside Rd / north bridge, affecting 6 people.” Show crew availability/capabilities only if supplied by authoritative data; otherwise label unknown. No default crew. Footer: Cancel and “Dispatch Boat 07”, unavailable until a valid explicit selection. Opening from New does not silently acknowledge: acknowledgement and assignment events stay distinct. The permitted direct New → Assigned transition is a provisional policy decision; if operations requires acknowledgement first, explain that prerequisite and keep dispatch unavailable until it is confirmed.

Focus starts in the crew selector; Tab/Shift+Tab stay inside the modal; Escape/Cancel closes without committing and restores the originating action's focus. Enter in a search/select field selects or edits; it must not implicitly dispatch. Dispatch commits only through explicit activation of the dispatch button. Avoid a second generic “Are you sure?” dialog: the review already names the request, crew and consequence.

While submitting, retain the summary, disable repeat submission, and say “Confirming assignment…”. A confirmed assignment with dispatch delivery pending shows “Assigned · dispatch delivery pending” as ancillary text, preserving Assigned as the status label. Never claim “Crew notified” from assignment alone. If transmission outcome is unknown, say “Dispatch result unknown. Checking latest state”; block duplicate dispatch until reconciled. Distinguish confirmed failure (“No assignment made”) from unknown outcome. Crew taken or request changed by another dispatcher returns a conflict with the latest values; preserve the draft for review, require revalidation and explicit dispatch again. No silent overwrite.

## Recent changes and accidental assignment recovery

Keep the selected row, scroll position and current filters stable during incoming updates. New requests appear in a persistent “3 new requests · Review” indicator, not by moving a focused row. Update known rows' facts visibly with “Changed [time]” and old → new detail in the change log. A changed priority exposes “Order changed · Refresh order” while preserving the active interaction. New highest-severity work must receive a persistent high-priority change notice even while sorting is held; no claim is made about alerting protocol beyond this outline. Opening recent changes shows request ID, actor/source, time, field, previous value and current value. Reading the change log does not acknowledge the request.

After assignment show a persistent row/detail action “Undo assignment” plus the same entry in recent changes. Do not make a short-lived toast the only route. Proposed confirmation: “Undo Boat 07 assignment to F-1042?” State the actual operational effect before the button.

An undo is a new audited operation, not deletion of history. Revalidate the current assignment/version and permission. If no dispatch instruction has escaped and reversal is supported, confirm removal and restore the prior New or Acknowledged state from the recorded prior version; update crew to Unassigned. Keep the original assignment and reversal events. If the crew has already received or acted on dispatch, do not promise immediate recall: present “Request cancellation” only if supported, show cancellation pending and retain Assigned until authoritative confirmation. If cancellation is unsupported, show the approved manual contact/escalation route rather than a fake Undo success. Subsequent reassignment or resolution blocks stale undo and names the newer event. Failed undo leaves the assignment visible and the recovery action available; unknown outcomes reconcile before retry.

This recovery contract requires backend cancellation, version checks and an operational recall policy. It is a requirement to resolve before implementation, not a claim that those capabilities exist.

## Keyboard, accessibility and exceptional states

Use a semantic table with named header sorting buttons, request links and real buttons. Tab moves through controls in a predictable order; request links open detail; Enter/Space activate the focused control. No single-letter dispatch shortcut. If optional shortcuts are added later, expose them in Help and allow disabling character shortcuts. Provide a skip link to the queue. Restoring focus uses request ID rather than row index so concurrent updates do not redirect an action.

Use a visible severity legend and programmatic labels such as “Severity 1, highest”. Announce confirmed acknowledgement/assignment, errors and new-request counts without forcing focus; do not announce every minute tick. Keep focus out from under sticky headers or banners. At zoom/text-spacing overrides, allow row height growth and scroll the essential two-dimensional table while surrounding controls reflow. The selected [WCAG 2.2 Recommendation](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) supplies criteria for color independence, keyboard access, focus, contrast, status messages and target size; the concept establishes no conformance claim.

| Cause | Proposed screen/content |
| --- | --- |
| Initial load | Labeled queue loading state; actions unavailable until authoritative records arrive. |
| Filtered empty | “No requests match these filters” with active filters and Clear filters. Distinguish from no active requests. |
| No unresolved requests | “No unresolved requests” with access to Resolved; avoid celebratory completion claims during an ongoing incident. |
| Connection/data stale | Keep last known rows with “Last synced [time]; data may be outdated.” Distinguish service freshness from each request's stale flag. Disable dispatch if authoritative validation cannot be obtained; preserve the draft. |
| Missing permission / recovery failure | Keep viewable context, name the unavailable action and provide the configured supervisor/contact path. Never invent a named supervisor or phone number. |

## Checks and remaining decisions

Actual checks: brief-to-outline review covered the five comparison facts, three non-color severity levels, unchanged four labels, separate acknowledgement/dispatch, visible result, keyboard route, recent changes and accidental assignment recovery. Column arithmetic totals 1232px; row arithmetic exposes the height limitation. Documentation and one source's static density visuals were inspected; no app, assets or prototype was built. No dispatcher task test, contrast measurement, screen-reader check or eight-hour fatigue evidence exists.

Before implementation, confirm operational severity names, stale thresholds, dispatch acknowledgement/delivery semantics, direct assignment policy, and actual cancellation authority. These do not prevent the reference packet but prevent treating the outline as an executable operational specification.

Future acceptance tasks: with realistic 30-row data at 1280px, locate the oldest stale high-severity request, compare crew allocation across records, acknowledge without generating any dispatch event, dispatch deliberately with confirmed result, and recover an accidental assignment before and after crew receipt. Include long locations, unknown people counts, concurrent changes, connection loss and keyboard-only completion. Measure missed requests, assignment errors and recovery success; visual preference alone cannot establish operational performance.

## Direction update: larger request cards

New feedback: “The sparse option looks the most polished. Could we make every request a huge card like that?” This changes the proposed density direction but leaves the dispatch/state requirements intact. No named sparse source or image has been supplied, so its exact visual treatment remains uninspected.

Two concrete adaptations are available. A large card per request can give location, people, notes and assignment context greater emphasis while handling one request. An illustrative 180px card height would require at least 5400px for 30 requests before gaps and controls; separate cards also weaken column alignment when comparing crew, age and stale status across requests. That is a design tradeoff, not a tested performance result.

A compact comparison queue can carry the preferred finish through stronger location typography, carefully aligned values, restrained borders and a more spacious selected-request detail card. This preserves the full-width comparison structure while giving the active request more breathing room. The large detail card would repeat ID, severity, age, location, people, crew, status and freshness and keep Acknowledge separate from Assign crew…; its visual emphasis would never imply dispatch.

Working assumption, explicitly unsettled: retain the compact full-width queue as the default and provide a large selected-request detail card. The follow-up permits a reasonable assumption rather than blocking the outline; it does not settle the density preference. This choice preserves the original priority of comparing about 30 requests while applying the requested polish to the focused request. A large-card default remains an alternative for later review.


### Applied selected-request card

Activating a request ID opens a full-width detail region below the queue, without narrowing its comparison columns. The region is a large, quiet card with a strong location heading, a compact ID/severity/status line and a labeled facts band: received/age, people affected, assigned crew and last update/stale flag. Notes and change history follow in readable paragraphs. The card height follows content; the illustrative 180px figure above is a comparison estimate, not a fixed specification. Avoid decorative blank height and faint metadata.

The card header exposes Close detail and a clear return-to-request link; opening moves focus to its named heading, closing restores focus to the originating request ID, and filters/scroll position are preserved. Acknowledge is a secondary action for New; Assign crew… opens the separate dispatch review already specified. Assigned requests expose View assignment and the conditional Undo assignment recovery path. The current request ID and location remain prominent throughout review. Reading or closing the large card changes no workflow state.

This arrangement temporarily uses more vertical space for one chosen request, rather than multiplying that cost across every record. Operators can close detail to recover the full queue workspace. The assumed composition, actual card placement and prolonged-shift comfort still need rendered and dispatcher-task evaluation; no further approval is needed to complete this source/outline packet.
