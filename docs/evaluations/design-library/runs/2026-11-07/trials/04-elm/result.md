# Museum volunteer rota: reference packet and three-screen outline

Use a quiet, date-grouped noticeboard with a clear request → review → decision flow. The transaction completed at submission is **sending a request**, not securing a shift. This is a proposed content/interaction outline; no app or assets have been built.

## Direction carried through

Confirmed direction after the reference shortlist: “I’d rather keep the noticeboard character even if the most useful recovery reference is visually loud.” Treat visual character and interaction structure as separate transfer decisions: keep the museum’s calm surface while borrowing explicit correction, status and retained-contact behavior.

Preserve the existing paper-noticeboard character: warm off-white surface, dark ink, restrained rules, generous but compact date headings, and one muted accent for the primary action. Use readable body text and a modest editorial heading; keep the existing museum typography if available. Avoid decorative travel imagery, price-like scarcity badges, celebratory booking language and a colorful calendar grid. Exact colors and type are provisional because the existing interface was described, not supplied.

Prioritize comparing two-hour shifts, checking one choice, and understanding what the coordinator has decided. Contact details survive both editing and a lost-place recovery. No automatic waitlist, paid priority or automatic assignment is proposed.

## Reference matches

| Reference and inspected evidence | Transfer to the rota | Mismatch / boundary |
| --- | --- | --- |
| [GOV.UK Check answers](https://design-system.service.gov.uk/patterns/check-answers/), first-party text and HTML; “Let users go back and change their answers” | A grouped shift/contact summary, specific change links, prefilled editing and direct return to review | Borrow the correction contract, not government branding. Documentation is not evidence that this museum flow works. |
| [GOV.UK Confirmation pages](https://design-system.service.gov.uk/patterns/confirmation-pages/), first-party pattern and example | Screen 3 states what was received, the next decision, useful contact information and a record the person can return to | The museum has completed intake only. Replace “Application complete” with an explicit pending state. No email, response deadline or reference number is asserted unless the service supplies it. |
| [Meetup waitlist](https://help.meetup.com/hc/en-us/articles/41229648295181-How-to-Join-an-Event-Waitlist-on-Meetup), first-party state/transition documentation | Separate awaiting a place from confirmed attendance; label status explicitly | Meetup documents automatic promotion, paid membership priority and some contexts with no waiting label. None transfers: this rota needs coordinator approval and visible Pending / Approved / Unavailable text. |
| [GOV.UK Error summary](https://design-system.service.gov.uk/components/error-summary/), first-party text and markup | Contact validation gets a focused summary linked to matching field messages | Capacity loss is a changed circumstance, not a volunteer's input mistake. Use a factual unavailable notice and a shift recovery action. |

A further candidate, [Google Docs suggestions](https://support.google.com/docs/answer/6033474), was inspected as first-party documentation. Its proposal/owner-acceptance distinction supports the coordinator authority model, but its inline editing and comment-thread UI do not help choose shifts; do not use them as the screen structure.

The colorful travel-calendar screenshot is a described preference, not an inspected source: no image, product or URL was supplied. Its attraction does not establish review or recovery behavior. The brief already settles the important tradeoff in favor of confirmation accuracy and the current character; no screenshot is needed to complete this outline.

## Three screens

All example dates, roles and contact values below are illustrative. Display real museum-local dates, times and timezone where ambiguity is possible.

### 1. Choose a shift

**Heading:** “Choose your volunteer shift”

**Intro:** “Choose one two-hour shift. You’ll check your choice before sending it to the coordinator. Sending a request does not reserve a place.”

A date-grouped list replaces the travel grid. Each row contains an explicit single-choice radio, weekday/date, start–end time, role/location if relevant, and availability text. Example: “Saturday 14 November · 10am–12pm · Welcome desk · Available to request.” Selection reads “Selected for your request,” never “Reserved.” Full rows remain readable as “Unavailable” and cannot be selected. Display exact place counts only if the service can supply trustworthy counts; even then they are not holds.

Below the list, a “Your contact details” section collects name and the museum's actual required contact method. Email is a provisional example, not a new requirement. Do not collect unrelated profile information. Primary action: **“Check your request.”** It proceeds only with one valid shift and required contact information. Missing input gets a linked error summary and precise field messages, with valid values retained.

If no shifts are available, say “There are no shifts available to request.” Preserve contact details already entered; show the real coordinator contact route rather than inventing a waitlist or promising future availability.

### 2. Check your request

**Heading:** “Check your shift request”

Two compact label/value sections: **Requested shift** (full date, two-hour start/end, relevant role/location) and **Contact details**. Actions have specific names: “Change shift” and “Change contact details.” Each opens the relevant portion of Screen 1 with existing values; “Return to check your request” brings the volunteer directly here. Contact edits never clear the selected shift; shift edits never clear contact details.

Immediately above the main action: **“The coordinator must approve your request. This shift is not reserved and may become unavailable.”** Main action: **“Send request for approval.”** Secondary link: “Back to choose a shift.” No payment, booking confirmation or extra compulsory confirmation checkbox.

Recheck availability when sending. If the shift is already full, keep the person on this review context with “This shift is no longer available. Your contact details are saved for choosing another shift.” Replace the send action with **“Choose a different shift.”** That opens Screen 1's recovery variant below. Do not show a pending receipt if intake was not accepted.

### 3. Request status (three variants of the same screen)

| State / trigger | Heading and essential content | Next action |
| --- | --- | --- |
| **Pending** — service has acknowledged receipt | “Request received — pending approval.” Show requested shift and submitted contact details. “Your shift is not reserved. The coordinator will review your request.” Give the actual decision/contact route and response timing only when established. | View/return to the current status through the service's supported access route. Do not offer a second shift submission as if the first were absent. |
| **Approved** — coordinator has approved and the service has committed the place | “Shift approved.” “You’re confirmed for [date], [start–end].” Show actual arrival/location instructions and coordinator contact. | Read the confirmed shift details. Only expose change/cancel controls if those operations exist. |
| **Unavailable** — another request takes the last place before approval | “This shift is no longer available.” “Another request took the last place. Please choose a different shift. Your contact details are saved.” Keep the old shift visible, labelled Unavailable. | **“Choose a different shift”** opens Screen 1 with contact fields populated, prior date context retained and no valid shift selected. |

Pending is shown as plain text with a muted label, Approved with an explicit confirmation sentence, and Unavailable with a clear explanation and recovery action. Color may reinforce these meanings but never carries them alone. Avoid a large success-green receipt for Pending.

## Recovery and state contract

`Choose → Check → Send → Pending → Approved OR Unavailable`

`Check: capacity lost → Choose (details retained) → Check updated shift → Send → Pending`

`Unavailable after submission → Choose (details retained) → Check updated shift → Send replacement request → Pending`

The old request remains Unavailable until a replacement is actually accepted; merely opening the chooser must not create a new request. The replacement is linked to the old request and explicitly shows the newly chosen shift before submission. A new choice still requires coordinator approval. Availability must be checked again at submission and approval; two requests must not both receive the last place. This is a proposed service requirement, not verified backend behavior.

Retention must cover the recovery route after a coordinator decision, not just browser Back in one session. The implementation must connect that route to the correct submitted contact details, using an appropriately protected request-return mechanism already supported or added by the service. The outline does not assume accounts, a particular email mechanism or indefinite browser storage. Establish the real contact/return channel and retention duration before implementation; never publish contact details on the public rota.

If sending has an unknown outcome, do not assert “not sent” or invite a blind duplicate: show “We could not confirm whether your request was received,” retain details, and use a supported status lookup or the actual coordinator contact. Pending appears only after known receipt.

## Outline checks completed and future acceptance checks

The outline was checked against the brief: exactly three screen types; one two-hour choice; explicit review; submission separate from reservation; pending, approved and unavailable distinct; both capacity-loss timings lead back with contact details retained. Reference transfer is structural; museum visual character remains intact.

Before shipping, exercise these proposed behaviors with real implementation evidence:

1. Edit only the shift from review; contact details persist and the revised shift is reviewed again.
2. Lose the last place during submission and after Pending; each route retains contact details without falsely confirming attendance.
3. Approve a request against current capacity; show Approved only when a place is committed, with no over-allocation.
4. Navigate selection, validation, review and recovery by keyboard; focus enters page headings or error summaries predictably, controls have full date/time names, and status changes are announced.
5. Check narrow screens, zoom and long contact/shift text: stack rows and change links in reading order; no clipped dates, horizontal calendar dependency or color-only status.

No live rota, screenshot, browser interaction, accessibility conformance or user test was checked. Sources were inspected as text/HTML through read-only public HTTPS. This packet establishes a proposed flow, not proven usability or compatibility.
