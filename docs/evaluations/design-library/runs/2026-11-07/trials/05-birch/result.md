# Instrument-loan kiosk reference and applied outline

Use a short, guided checkout and return flow with Arabic/English parity, explicit transaction confirmation, and a clean public screen at completion or timeout. This is an unbuilt design outline, not a tested kiosk or a claim of current legal compliance.

## Direction now settled

The current room policy governs this outline: after checkout/return, display **only instrument ID and a non-personal receipt code**. Clear names/contact details at completion and after 60 seconds idle. Warn at 45 seconds and offer continuation. Staff must not photograph borrower details. Staff assistance uses a separate authenticated console. Timeout never completes a loan or return. The device is touch operated; no keyboard is assumed. Arabic and English are required.

The older workshop photograph instruction is superseded for this design. Its documentation goal can be served by the permitted non-personal code or authenticated staff lookup; it does not justify leaving borrower information on the shared success screen. The handout and room policy were supplied as statements, not documents independently inspected.

## What responsibly matches

**The catalog has no good complete kiosk/return/session match.** Its correction and multilingual resources are useful parts, not a finished instrument-loan precedent. Literal searches for kiosk, timeout and Counterpoint returned no matches; broader return/session/direction searches yielded neighboring patterns. Public discovery did not establish a source for “Counterpoint Kiosk 2027.” Similar CounterPoint names refer to other products. The name may be wrong or unavailable; do not invent its return flow or call it perfect.

| Resource / inspected scope | Useful transfer | Decisive mismatch / decision |
|---|---|---|
| Catalog `pattern-govuk-check-answers`; [GOV.UK Check answers](https://design-system.service.gov.uk/patterns/check-answers/), live correction section and HTML text | Retain entered values, target a correction, return directly to review | Public application pattern, not kiosk privacy. Borrow correction mechanics for loan review; do not copy official branding or success details. |
| Catalog `principle-multilingual-layout`; [W3C structural direction](https://www.w3.org/International/questions/qa-html-dir) plus [inline bidi](https://www.w3.org/International/articles/inline-bidi-markup/), live text | Separate language from direction; logical placement and isolated mixed text | Guidance is not Arabic rendering proof. Apply to every transaction/error/timeout state and require native-reader checks later. |
| Catalog `pattern-uswds-language`; [USWDS language access overview](https://designsystem.digital.gov/patterns/select-a-language/), live text | Distinguish complete translated tasks from selected translated content | No executed selector. Both required languages must cover the whole kiosk journey; a translated welcome alone is insufficient. |
| External [HMRC Service timeout](https://design.tax.service.gov.uk/hmrc-design-patterns/service-timeout/), warning/options/end-page documentation | Warn before expiry; clear continuation and ending choices; explain the result | Its 13/15 minute tax-service schedule does not fit this room. Use the supplied 45/60 second policy. No package installation or code adoption. |
| External [W3C Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html), extension branch and kiosk discussion | Check warning response time and extension behavior | The extension branch specifies at least 20 seconds and at least ten extensions. Current policy leaves 15 seconds; flag this conflict, not a conformance claim. |
| External [Bethel Park self-check instructions](https://www.bethelparklibrary.org/selfcheck.htm), checkout steps and return FAQ | Identify borrower, scan item, finish, then receipt | Explicitly excludes returns at its kiosks. Useful checkout analogue only; reject it as a return-flow reference. |
| External [Bibliotheca smartShelf announcement](https://www.bibliotheca.com/press-release-bibliotheca-launches-smartshelf-borrow-to-global-library-market/), dated 21 June 2023 | Distinguish physical item return from account update | Vendor description of specialized shelf technology, not tested interaction or instrument compatibility. Do not inherit automatic recirculation of returned instruments. |

### Source age and language limits after your feedback

Keep the useful mechanisms, while treating the current room policy as the controlling product requirement. Bibliotheca’s announcement is dated **21 June 2023**; its physical-return/account-update concept survives, but its age and lack of evidence about this room’s policy prevent transferring receipt visibility or privacy behavior. The Bethel Park instructions inspected here are English and provide no Arabic/RTL demonstration; retain only their checkout sequence. GOV.UK correction guidance likewise supplies the correction loop, not an Arabic kiosk example or proof of this room’s privacy rules. HMRC documents English/Welsh content and a different timeout schedule; that does not demonstrate Arabic or satisfy the room’s 45/60-second behavior.

The exact dates of the room policy and workshop handout were not supplied, and several live documentation pages have no verified publication date from this inspection. A fresh access date does not establish that their design advice postdates the policy. No source’s date overrides the supplied current policy. W3C explicitly covers RTL and mixed-direction mechanisms, but neither those text instructions nor USWDS’s language-access overview prove this kiosk works in Arabic. **Unresolved:** native Arabic translation/comprehension, actual RTL rendering and mixed identifiers, touch recovery, privacy clearing, and timing behavior all require later implementation evidence. No complete Arabic instrument-kiosk example was verified.

All upstream inspections above were public HTML **text**. No actual source screen visual, source interaction, translation switch, scanner, or return mechanism was tested. Catalog historic screenshot annotations are not visual evidence from this task. There is no selected visual imitation: the proposal uses readable task headings, large labeled touch controls, grouped item rows, text status plus color, and limited decoration because identification and transaction status matter most here.

## Applied checkout outline

Reasonable assumptions: an existing loan register can identify borrowers and instrument IDs; each instrument has a readable tag; staff are available for exceptions. A scan is preferred where hardware exists. A touch numeric pad is proposed only if IDs are numeric; otherwise provide a suitable touch input or staff route after confirming the actual identifier format. No external keyboard dependency.

| State | Screen content and touch actions | Result / important alternate path |
|---|---|---|
| Welcome | “Borrow an instrument” / “Return an instrument”; English / العربية; “Ask staff for help.” No prior session data. | Selecting Borrow begins a fresh session. No automatic authentication or transaction. |
| Identify borrower | “Scan your borrower card”; hardware-dependent manual-ID touch option. Collect only fields required by the existing register. | Failed/unrecognized ID: preserve current input while active, explain next action, offer retry/help/end. Do not disclose another person's account or loan history. Authentication strength remains an implementation fact to establish. |
| Identify instrument | “Scan the instrument ID”; show ID, instrument description and current availability during the active session. One visible item row per intended loan; “Remove” and “Add another” if supported. | Unknown or unavailable item stays uncommitted. Explain whether to rescan or ask staff. A repeated scan must not duplicate a loan. |
| Review | “Check this loan”; selected instrument IDs, actual due date/terms from the register; minimum borrower identity needed to verify the intended account. “Change borrower”, “Change instruments”, “Confirm checkout”, “End session.” | Corrections retain other active-session values and return directly here. Do not invent a loan duration, eligibility rule, or fee. Confirm is the explicit transaction boundary. |
| Confirming → completion | While recording, prevent repeated submission. Only a confirmed register response permits the completion state. Show instrument ID(s) and a non-personal receipt code only; labeled “End session” control. | At confirmed completion immediately remove all borrower name/contact information from visible UI, hidden summaries and input state. No due date, borrower ID, name, contact, personal QR code, or photo prompt on this restricted success screen. Timeout cannot substitute for Confirm. |

The “End session” control is required navigation, not extra receipt information. A generic state heading such as “Checkout recorded” may identify the outcome; the variable receipt content remains strictly instrument ID/code. Due date is presented before confirmation; any private follow-up delivery is outside this outline until an approved existing channel is known.

## Applied return outline

Assumption: return by **instrument ID alone**, without requesting a borrower name/contact/card. The register locates the active loan internally; the kiosk never exposes whose loan it is. This keeps return usable when a different person brings the instrument back. Room staff should confirm this operational permission before implementation.

| State | Screen content and touch actions | Result / important alternate path |
|---|---|---|
| Identify return | “Scan the instrument ID”; show the identified instrument and ID; “Wrong instrument” / retry / help / end. | Not found: rescan or staff help. Already returned/no active loan: neutral item status; no new return entry and no past borrower data. |
| Handover / review | “Check the instrument you are returning”; show ID and item description; show the actual designated handover location once known. “Confirm return” / “Change instrument.” | The physical handover rule and sensor/staff requirement are hardware-specific unknowns. A scan alone must not imply custody transfer. If the kiosk cannot verify or record the room's required handover, use “Staff assistance required,” not a false returned state. |
| Confirming | Explicit Confirm return records receipt only when the actual handover rule is satisfied. | Proposed register statuses distinguish “received, awaiting staff inspection” from available to borrow. Condition/accessory exceptions go to staff; do not promise acceptance, fee waiver or immediate availability. |
| Completion | Only after confirmed record update, show instrument ID and non-personal receipt code; End session. | Clear any borrower details immediately even if returned by another person. Do not show loan owner, contact, condition narrative or staff-photo instructions. A code should not function as a public credential for retrieving personal records. |

For multiple items, show item-level outcomes during the active session. Never collapse “one received, one failed” into full success. If the backend cannot support safe item-level commits, assume one instrument per transaction until that contract is known.

## Timeout and transaction boundaries

| Trigger / timing | Proposed behavior and copy |
|---|---|
| Start / activity | Track inactivity from the last deliberate touch or accepted scan; background polling, animations and network responses do not count as presence. Provide End session throughout. Switch language while preserving the current active step and entered values. |
| At 45 seconds idle | Mask the underlying personal content; focus the touch dialog: “Are you still here? This session ends in 15 seconds. Unconfirmed checkout or return will not be completed.” Buttons: “Continue session” / “End session.” Announce the warning without reading every countdown tick. |
| Continue | Preserve the exact step and values, restore focus to the invoking context, restart the idle clock. Proposed: permit repeated extensions, including at least ten; no hidden maximum was supplied. Background activity cannot silently extend. |
| At 60 seconds idle, or explicit End | End the public session; clear name/contact details, borrower identifiers, entered fields, personalized errors, overlays, history restoration and transient session access. Return to a neutral welcome/end state. Proposed copy: “Session ended. Start a new session.” No name, item-linked personal history or receipt remains at the next user's welcome. |
| Expiry during a pending request | Never automatically confirm, cancel a committed transaction, or claim “nothing happened.” Clear the public session on schedule; the register must resolve the original operation independently. Separate authenticated staff lookup handles an uncertain outcome. Do not offer blind resubmission or a public personal-record lookup. |

Ending the kiosk session removes transient public-session information; it does not erase the authorized loan register. Server idempotency and reconciliation are proposed implementation requirements: one deliberate confirmation should create at most one recorded loan/return despite duplicate scans, taps, retries or late responses. These capabilities are not demonstrated by any source inspection.

**Timing issue to resolve before implementation:** 45-to-60 seconds gives a 15-second warning. That does not meet the 20-second response window in the cited W3C extension branch. Keep the user's schedule explicit in this outline; propose changing the warning to 40 seconds while retaining the 60-second clearing deadline. That is a policy amendment requiring the room's decision. Do not silently change the deadline, claim a security exception, or claim current conformance. Other timing-adjustment alternatives require their own assessment.

## Arabic / English layout and content contract

1. Offer **English / العربية** on welcome and within the active flow, using names rather than flags. Translate review, errors, availability, help, timeout, pending and completion text; keep the same transaction state when switching. Reset to the room's approved neutral language choice on a fresh session rather than remembering the prior borrower.
2. For English use `lang="en"`, `dir="ltr"`; Arabic `lang="ar"`, `dir="rtl"`. Align labels and groups to inline-start and spacing to logical start/end. Keep logical reading/focus order tied to task sequence. Directional navigation arrows can adapt to reading direction; never mirror instrument photographs, barcodes, logos or the characters within IDs.
3. Isolate runtime names/descriptions using direction-aware markup; isolate known Latin IDs/codes as LTR runs inside Arabic. Test punctuation and numbers adjacent to Arabic, not only translated headings. No forced Latin line lengths or uppercase-dependent hierarchy. Arabic wording remains a translation task for a qualified native reader, not supplied verified copy here.
4. Use large, labeled touch targets with spacing, visible focus, readable contrast and wrapping labels; avoid hover-only help, drag-only actions or icons without text. Provide scanner-free touch/staff recovery appropriate to hardware. Do not assume built-in Arabic keyboard, audio, printer, RFID or receipt delivery.
5. Use one clear action area per step and stable placement within each locale. Fit long translated errors without covering End session or Continue. The timeout dialog masks personal content and retains usable touch controls at zoom and large text sizes. Verify DOM/focus order separately from visual mirroring if implemented for the web.

## Actual checks and remaining evidence

Checked the source/outline consistency against the relayed policy: both transactions need explicit confirmation; completion content is restricted; name/contact clear at completion and 60 seconds idle; warning appears at 45 seconds; no staff photographs; separate staff console; Arabic/English and touch input appear across the flow. Checked that unknown outcomes and partial results are not represented as success. JSON receipts are syntactically validated.

No app or assets were built. No behavioral, accessibility-conformance, legal, compatibility, translation-quality or usability acceptance is established. Before implementation, the essential checks are: touch operation and Arabic mixed text on the actual kiosk; warning/extension and exact privacy clearing including back/reload/late-response cases; commit-versus-timeout races and duplicate submissions; actual handover/inspection rules; and native Arabic comprehension plus full-process accessibility assessment.

Next decision: resolve the 15-second warning conflict with the room policy owner. The remaining hardware and register assumptions are labeled rather than presented as installed capabilities.
