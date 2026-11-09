# Instrument-loan kiosk: applied reference packet

Use a short guided checkout and a staff-confirmed return, with English/Arabic direction set per session and personal details removed on completion. This is a proposed outline, not a built or tested kiosk.

## Decisions carried forward

The clarified room policy governs this design: success shows only instrument ID and a non-personal receipt code; name/contact details clear immediately at completion and at 60 seconds idle. Warn at 45 seconds and offer Continue. Timeout never completes a loan or return. Staff help uses a separate authenticated console. The older workshop suggestion to leave borrower details visible for photographs is rejected because it conflicts with the supplied current policy. Neither original handout nor policy document was supplied; their authority here comes from the user's explicit clarification, not independent document inspection.

Arabic and English, touch input, and no assumed physical keyboard are required. Other details are provisional: one instrument per transaction; existing room borrower credential scanned for checkout; instrument tag scanned or entered with an on-screen keypad; staff acknowledge physical receipt before a return becomes complete. If scanner or credential support is absent, show staff assistance rather than imply unsupported self-service authentication. No scanner, locker, sensor, printer, or electronic receipt delivery is established by the brief.

## What the catalog can responsibly supply

**There is no good end-to-end instrument-loan kiosk match in the supplied catalog.** Searches for kiosk, Counterpoint, and timeout returned zero matches. “Return” produced 22 broad matches, largely unrelated navigation or return-to-source patterns. Use these narrow references without presenting them as a proven kiosk flow:

| Resource and evidence inspected in this run | Transfer into this outline | Mismatch / excluded use |
| --- | --- | --- |
| `pattern-govuk-check-answers`: card plus first-party [Check answers](https://design-system.service.gov.uk/patterns/check-answers/), especially “When to use” and “Let users go back and change their answers” | A final checkout review, specific change actions, prefilled corrections, direct return to review | Application form guidance, not loan hardware, shared-screen privacy, Arabic, or a working return. No GOV.UK branding copied. Its personal-data example is not success-screen content. |
| `principle-multilingual-layout`: card plus W3C [structural direction](https://www.w3.org/International/questions/qa-html-dir), Quick answer; companion [inline bidi guidance](https://www.w3.org/International/articles/inline-bidi-markup/), Quick answer | Semantic base direction, logical alignment, isolated mixed-direction instrument and receipt identifiers | Technical guidance, not evidence that this kiosk works for Arabic readers. Hangul guidance linked by the card is irrelevant here and was not opened. |
| `standard-wcag-conformance`: card plus [versioned WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), sections 2.1.1, 2.2.1 and 2.5.8 | Timing conflict made explicit; input, target and full-process checks included in acceptance plan | Not legal authority for this room; no kiosk conformance established. |

The source boundary remains explicit after your feedback: the inspected GOV.UK example is English; retain only its review/correction mechanism. It provides no demonstrated Arabic translation, RTL arrangement, touch-kiosk operation or session-clearing behavior. The W3C direction articles supply technical guidance rather than a verified bilingual loan flow. WCAG is the dated 12 December 2024 version. The room policy has no supplied publication date, so chronology relative to any source is not established; retrieving a page today does not establish that its design postdates the policy. Even if a source predates it, its useful mechanism may transfer, while the explicit current room policy controls success content and privacy clearing. Arabic content, actual directional rendering, touch access and timing remain unresolved verification work.

An exact-name public search for “Counterpoint Kiosk 2027” yielded unrelated search results, not a verifiable primary design source. The name remains unverified; this does not prove it never existed or identify a corrected name. No return-flow claims, visual cues, or authority are borrowed from it. Catalog metadata's prior visual-inspection claims belong to the catalog authors: this run inspected source text only, with no visual or interaction inspection.

## Applied screens and transaction states

### Shared composition and content

A calm music-room tool: one task heading, one instrument block, one main action, persistent End session and Staff help touch controls. Status words and explicit labels carry meaning; color is secondary. Use spacious text and touch targets (provisional design target 48 CSS px, subject to physical-screen testing), visible pressed/disabled states, and no hover-only, swipe-only, drag, or keyboard-shortcut requirements. Keep help in the same logical location throughout. Avoid decorative instrument photography that might imply the wrong item.

At idle show both self-named language choices, **English / العربية**, and no previous user's data. Selecting Arabic establishes `lang="ar" dir="rtl"`; English uses `lang="en" dir="ltr"`. Task labels and review rows follow reading direction through logical start/end alignment. Back/forward directional affordances follow the locale, while instrument photos, tag symbols, receipt character order and physical scanner-location diagrams do not blindly mirror. Keep the actual hardware diagram accurate in both locales.

Instrument ID `VI-024` and receipt `R7K-28Q` are illustrative. Treat such canonical identifiers as isolated LTR runs inside Arabic text; unknown names use direction-aware isolation. Do not reverse stored strings. Arabic labels may wrap and need different font metrics; no forced English line counts, tracking or uppercase styling. Language switching retains the active transaction and edits, translates all errors/warnings, and never submits. Preserve the selected language through the session; reset to bilingual entry at its end. Arabic translations beyond the language selector require fluent-reader review; English sample copy below is a content specification, not translation-ready approval.

### Checkout

| Screen / cause | Visible content and action | Result / alternate path |
| --- | --- | --- |
| Entry | “Borrow an instrument” / “Return an instrument”; concise notice: “This screen clears after 60 seconds without activity.” | Start a fresh session; no borrower lookup list. |
| Identify borrower | “Scan your room credential”; explain why identification is required. Display only the minimum confirmation needed, not full contact details by default. | Valid credential moves forward. Unrecognized/unsupported credential: retry scan or ask staff. No arbitrary person search on public screen. |
| Identify instrument | “Scan the instrument tag”; recognized ID and instrument type; touch keypad fallback only if supported | Unknown tag: “Instrument not found. Check the tag or ask staff.” Unavailable item: explain it cannot be borrowed; do not show another borrower's identity. |
| Review | Instrument ID/type and due date from the actual loan rules; minimal borrower confirmation; “Change instrument” and, if required, “Change borrower.” “The loan is not complete yet.” Main action: “Confirm loan.” | Corrections preserve unrelated session data and return here. Due dates and eligibility are supplied by the service, not invented by this concept. End session clears draft without creating a loan. |
| Submit | “Recording loan…”; prevent repeat confirmation | Only authoritative service acknowledgement yields success. Known rejection returns to review with recoverable error. Unknown outcome goes to staff resolution, with no blind retry. |
| Complete | “Loan recorded”; **instrument ID + non-personal receipt code only**; “Done” | Immediately clear name/contact and invalidate public borrower context before rendering this screen. No due date, borrower name, photo, contact, credential or account link on success. Done returns to bilingual entry. |

### Return

| Screen / cause | Visible content and action | Result / alternate path |
| --- | --- | --- |
| Identify item | “Scan the instrument tag”; instrument ID/type | No borrower identity needed for provisional return intake. Unknown tag: staff help. Already returned: neutral status, no new return event. |
| Check item | Confirm instrument and any included accessories from real inventory; “This does not complete the return.” Actions: “Continue to return” / “Change instrument” | Wrong item can be corrected without recording a return. Missing accessory/damage directs to staff; no invented fine or automated clearance. |
| Handoff pending | “Give instrument [ID] to staff. Return not complete until staff confirm receipt.” | Staff use the separate authenticated console to verify receipt and resolve exceptions. This explicit staff-assisted assumption avoids equating a scan with physical return. No photograph of borrower details. |
| Recording / outcome | Staff acknowledgement is matched to this transaction and recorded by service | Success only after acknowledgement. If acknowledgement is unavailable, display “Return not confirmed. Ask staff before leaving”; do not clear the loan just because the user tapped or time expired. |
| Complete | “Return recorded”; **instrument ID + non-personal receipt code only**; “Done” | Clear personal session data immediately and return to bilingual entry on Done. Receipt is a reference, not a public credential for retrieving borrower details. |

### Timeout, completion and recovery

| Event | Proposed behavior |
| --- | --- |
| Active session, 0–44 seconds idle | Preserve current draft for correction. Idle time is measured from the last deliberate touch/entry or recognized user scan, not animation, polling or server updates. Reading alone still risks expiry; disclose the timer early. |
| 45 seconds idle | Obscure personal details behind a warning: “Still using this kiosk? This session ends in 15 seconds.” Large touch actions: “Continue session” and “End session.” Continue restores the current step and resets idle time; it never confirms a loan/return. No background tap should activate underlying controls. |
| 60 seconds idle, or explicit End session | Clear name/contact, credential context and local draft; dismiss keypad/warning; invalidate public session access; return to bilingual entry. Proposed teardown includes DOM/state, navigation history/back restoration, autofill and cached session views. Public restart cannot reopen the old user's details. Backend records needed for completed or unresolved operations are a separate authenticated staff concern. |
| Request submitted before expiry; result late/unknown | Timeout clears the public session but is not a submit, cancel or success event. A previously authorized request may finish independently. Reconcile through transaction identity/idempotency at the service and the authenticated staff console; a late response must not repopulate the new public session. No instruction to submit again until outcome is known. |
| Success | Clear personal details immediately, without waiting for 60 seconds. Proposed receipt screen may remain until Done or idle reset; only the two policy-permitted values are present. No staff-photo mode. |

**Timing conflict requiring policy review before accessibility acceptance:** the mandated 45/60 timing gives only 15 seconds. WCAG 2.2.1's extension route requires at least 20 seconds and at least ten extensions, with other routes/exceptions defined separately. Do not claim a generic privacy exception. Preserve the requested 45-second warning and 60-second clearing in this outline; propose an additional initial warning at 40 seconds, with the 45-second reminder retained, for the room owner to consider. That extra warning is not represented as approved policy. A separate staff console does not by itself establish conformance or an equivalent accessible journey.

## Checks and limits

Performed: catalog query/result review; selected card and first-party text inspection; consistency review against the relayed policy, Arabic/English, touch constraint, correction, unknown outcome and timeout invariants. No installation, app build, asset generation, native source screenshot, source interaction, kiosk test or legal assessment occurred. Public primary pages opened successfully; no policy denial occurred.

Before implementation acceptance: test both languages on actual touch hardware with Arabic readers, long Arabic labels and mixed identifiers; verify translated warning/error copy, physical reach, text size, contrast, magnification, available assistive input and scanner/keypad behavior. Exercise checkout correction, staff return acknowledgement, unknown/duplicate/late outcomes, 45-second Continue, 60-second expiry and success privacy clearing; verify back/reload cannot disclose old details. Confirm warning timing policy, credential capabilities, due-date rules, staff-console acknowledgement and backend reconciliation contract. These are open verification items, not tested outcomes.
