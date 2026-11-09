# Museum volunteer rota — reference packet and applied outline

Use a quiet, date-led noticeboard with three screens: **Choose → Check → Request status**. Submission confirms receipt of a request; only coordinator approval confirms a place. This is a proposed outline, not a built or tested service.

## Direction carried through

After the shortlist, you confirmed: “I’d rather keep the noticeboard character even if the most useful recovery reference is visually loud.” The selection therefore transfers recovery and review mechanisms only; source color, imagery and visual intensity do not set the museum’s style. The quiet date-led rows and plain status language remain the direction across all three screens.

The brief settles the audience, one two-hour shift, coordinator approval, non-reserving submission, retained contact details and restrained paper character. The unnamed travel-calendar screenshot was not supplied or inspected. Its attractiveness is not evidence for confirmation or recovery. No style vote is needed to preserve the stated direction.

Keep the museum’s existing typography and identity if available. Proposed composition: warm paper background, dark readable text, thin rules, generous line spacing and date-grouped shift rows. Use one quiet accent for actions; write states in words as well as any accent color. No travel imagery, urgency counters or festive “booking confirmed” treatment. These visual choices come from the brief, not observed source visuals.

## Reference matches

All source inspections below were public documentation text/HTML on 7 November 2026. No source screenshot was inspected in this task and no live product interaction was tested. Card-reported visual inspections are not adopted as this task’s evidence.

| Reference and precise inspected part | Fit | Decisive mismatch | Applied decision |
|---|---|---|---|
| [GOV.UK Check answers](https://design-system.service.gov.uk/patterns/check-answers/#let-users-go-back-and-change-their-answers), card `pattern-govuk-check-answers`; correction section and summary-list HTML | Specific change links, prefilled answers and direct return to review | Public-service identity is not the museum identity; example submission is not capacity approval | Screen 2 separates shift and contact summaries. Change shift preserves contact details and returns directly to review. |
| [GOV.UK Error summary](https://design-system.service.gov.uk/components/error-summary/#how-it-works), card `pattern-govuk-error-summary`; focus and field-link guidance | Recoverable field errors have a clear destination | A shift filling is a system/state change, not a volunteer’s invalid input | Required-field errors use a focused linked summary and matching inline messages. Capacity loss gets its own explanation and choose-again action. |
| [Meetup waitlist](https://help.meetup.com/hc/en-us/articles/41229648295181-How-to-Join-an-Event-Waitlist-on-Meetup), card `flow-meetup-waitlist`; waitlist, Going and promotion sections | Distinguishes expressing interest from confirmed attendance | Automatic promotion, paid priority and absence of an explicit waiting label do not fit coordinator approval | Borrow the state distinction; reject the queue and promotion rules. Always display Pending approval or Approved explicitly. |
| [Google Docs suggestions](https://support.google.com/docs/answer/6033474), card `flow-google-docs-suggestions`; introduction and accept/reject section | Proposal and authoritative change belong to different decision-makers | Document editing has no limited shift capacity | Volunteer sends a proposal; coordinator’s approval alone changes it to an assignment. No bulk-approval or editing UI is imported. |
| [GOV.UK Confirmation pages](https://design-system.service.gov.uk/patterns/confirmation-pages/#how-it-works), external addition found through Check answers navigation; next steps and bookmarked receipts | Receipt can describe what happens after submission and support return visits | A transaction-complete heading can overstate the wider outcome | Screen 3 says Request received / Pending approval, shows the requested shift, and explains the next decision. It never says the shift is booked while pending. |

The useful transfer crosses visual domains: the review loop is closer to an application form than a travel checkout. A full calendar is unnecessary for choosing a single shift; date-grouped rows keep the two-hour choices and availability text readable. If many dates later make comparison difficult, assess an added date filter without changing this state contract.

## Three-screen outline

Illustrative content only: “Saturday 14 November 2026, 10:00–12:00 — Welcome desk.” Use the actual museum location and local time convention. Do not publish invented capacity counts, response times or coordinator contact details.

### 1. Choose a shift

**Order:** museum/rota title → short explanation → date groups and shift choices → contact details → Continue to check.

- Heading: **Choose one volunteer shift**. Intro: “Each shift lasts two hours. Your request needs coordinator approval. Sending a request does not reserve a place.”
- Single-selection radio rows: full date, start/end time, role/location where relevant and availability text. For example, “Available to request” or “Unavailable — no places left.” A selected row reads “Selected”; this is not Pending or Approved. Unavailable rows remain readable with no selection action. No count unless reliable data supports it.
- Contact section: **Your contact details**. Retain existing required fields. For this outline, assume name and email; replace email with the museum’s established contact method if different. Explain its actual use. Do not add an account, telephone requirement or consent promise without a reason.
- Action: **Continue to check**. Missing required information leaves all entered values intact, shows a linked error summary and inline correction text. Nothing has been submitted yet.
- Recovery variant: heading notice **That shift is no longer available**. “Another request took the last place for [full shift]. Choose a different shift. Your contact details are still here.” Preserve the old date context and contact values; clear the invalid choice, mark its row unavailable and require an explicit new selection. Never silently choose an alternative.

**Layout:** desktop rows may align date/time, role and state across columns; narrow screens stack each row in that reading order, keeping its radio and label together. Preserve a simple list rather than squeezing a month grid.

### 2. Check your request

**Order:** Back → **Check your shift request** → Requested shift summary → Contact details summary → approval notice → submission action.

Summary rows show the exact date, two-hour interval, role/location, name and contact destination. Provide **Change shift** and **Change contact details** with distinct accessible names. Each opens the relevant part of Screen 1 prefilled; its **Return to check** action comes directly back here. Contact edits do not clear the shift unless new availability information makes it invalid.

Notice beside the final action: **“This is a request for coordinator approval. It does not reserve a place.”** Primary action: **Send request for approval**. The title and button distinguish checking from sending; no extra “Are you sure?” dialog.

Proposed service boundary: recheck availability when continuing and sending, and enforce capacity at approval. A stale display must not create an approval promise. If capacity is already exhausted at send time, show the unavailable variant on Screen 1 with contact data preserved; do not show Request received unless the service actually accepted a request. If a pending request later loses capacity, use Screen 3’s unavailable state.

While sending, show **Sending request…** and prevent repeated activation. On a known failed send, retain everything and offer **Try sending again**. If the outcome is unknown, say **“We could not confirm whether your request was received.”** Preserve the draft; reconcile its status before allowing a duplicate submission. These are proposed requirements, not existing capabilities.

### 3. Request status

Use the same restrained receipt/status layout for all three outcomes. Show the full shift, contact details, and a real request reference if one exists. Avoid public display of other volunteers’ details.

| State / cause | Heading and explanation | Next action / retained information |
|---|---|---|
| Pending: service accepted the request, coordinator has not approved | **Request received — Pending approval.** “Your request for [shift] is awaiting coordinator approval. This does not reserve a place. Wait for approval before treating this as an assigned shift.” | Show actual next-step/contact information. Preserve request and contact details. Do not promise an email, deadline, position in a queue or automatic promotion unless supported. |
| Approved: coordinator accepted and capacity was committed | **Shift approved.** “You are approved for [full shift].” | Show actual arrival/location instructions and coordinator contact. This is the first point at which an assignment is promised. |
| Unavailable: another approved request took the last place while this request was pending | **This shift is no longer available.** “Another request took the last place for [shift]. Choose a different shift. You will not need to enter your contact details again.” | **Choose another shift** opens Screen 1’s recovery variant with retained details. New choice → Screen 2 for fresh review → explicit submission → Pending. Keep the old request marked unavailable; link the replacement internally so it cannot leave duplicate active requests. No automatic reassignment or waitlist. |

A return-to-status route is needed for asynchronous approval. Proposed requirement: preserve the request and its contact data server-side and provide a private return route using the museum’s established access method. Its authentication, retention period and delivery channel need service confirmation before implementation. Do not imply that browser memory alone satisfies recovery after a later coordinator decision. The outline does not promise cancellation, editing an approved shift or a notification system that has not been established.

## Flow and consistency checks

1. **Normal path:** choose one two-hour shift + details → check exact selection → send → Pending. Coordinator approval → Approved. Receipt and assignment are separate.
2. **Correction:** Change shift → choose again with details still present → check updated summary → send. Back and forward retain the draft.
3. **Capacity race:** if detected before acceptance, return to choose-again with details; if after acceptance, Pending → Unavailable → choose-again → check → send new request. Never show Approved for the losing request.
4. **No alternatives:** “No shifts are currently available to request.” Preserve details in the recovery context and show the museum’s real contact route, if available. Do not invent alerts or a waiting list.
5. **Uncertain status:** failure to load availability or receipt is not “Unavailable” or “Approved.” Say the status cannot be checked, preserve information and offer a real retry/status-reconciliation route.

These paths were checked as a written state model against the brief. Proposed accessibility acceptance checks: keyboard radio selection, visible focus, explicit labels, focus to error/recovery heading after navigation, announced state changes, no reliance on color, and readable stacked content at narrow width/zoom. No usability, accessibility conformance, responsive-rendering or live-behavior result is claimed.

Before implementation, establish the actual contact/notification and private return mechanism, retention policy, response-time wording and coordinator allocation rule. None changes the three-screen outline; each controls which promises may appear in it.
