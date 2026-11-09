# Revised reimbursement screen outline

Keep the current visual design, navigation, component styling and order: heading → amount → receipt → primary action → feedback banner. No new page or review step.

## Content and states

| State | Content in the existing screen | Behavior to specify |
| --- | --- | --- |
| Ready | Heading: **Submit reimbursement request**. Keep the amount and receipt controls. Primary button: **Submit request**. | Submit creates a request for finance review. Preserve existing validation rules; no new amount limits or attachment requirements are assumed. |
| Submitting | Button: **Submitting request…**. | Retain amount and attachment; prevent repeated activation while pending. Do not show success before the server confirms creation or retrieves the already-created request. |
| Confirmed success | Existing success banner title: **Request submitted**. Body: **Request R-1842 is awaiting finance review. Finance usually replies within three working days. No payment has been made.** Button: **Request submitted**, disabled for this completed submission. | Keep the receipt and amount visible as the submitted record. Replace “Paid!” completely. Preserve navigation; do not invent tracking, email, payment or support actions. Use the actual returned ID; R-1842 is the supplied example. |
| Confirmed submission failure | Existing feedback banner in its error state: **Request not submitted**. Body: **Your amount and receipt are still here. Try submitting again.** Button: **Try again**. | Use only when failure without creation is established. Keep amount and attachment intact and available for correction. Retry the same logical submission safely. |
| Unknown outcome, such as a timeout | Feedback banner: **Submission not confirmed**. Body: **We couldn’t confirm whether your request was submitted. Your amount and receipt are still here. Try again to confirm or complete this submission.** Button: **Try again**. | Do not imply the request failed or ask the person to start a fresh request. A retry must return the existing request if one was already created, otherwise complete the same submission once. Then show the confirmed success state. |

If existing field validation rejects an answer, show the actual correction beside that field, preserve the other entered information, and announce the error. Do not label a service failure as an invalid amount or receipt. No specific validation copy is invented because the existing rules were not supplied.

## Recovery requirement

Repeated clicks and retries must refer to one logical request. The integration must retain a stable submission identity and enforce deduplication on the server (for example, an idempotency key), returning the same request ID after an accepted request whose response was lost. Disabling the button alone cannot prevent duplicates. This is a required behavior specification, **not a verified existing backend capability**. The unknown-outcome retry copy assumes that contract is implemented; otherwise safe retry is unresolved and must be implemented before that action is offered.

Use the existing accessible feedback behavior to announce submission progress and results. Associate field errors with their controls. These are proposed requirements; no keyboard, assistive technology or rendered-state test was performed.

## Brief rationale and reference match

“Submit request” describes the actual action; “awaiting finance review” separates successful submission from approval and payment. The reference confirms what was created, and “usually” preserves the supplied expectation without promising a deadline. Failure and uncertain outcome need different messages so a lost response does not encourage duplicate requests.

The [GOV.UK confirmation pattern](https://design-system.service.gov.uk/patterns/confirmation-pages/) supports including a transaction reference and what happens next and when. Borrow those content duties inside the existing banner; its separate page, official styling, email example and extra links are outside this repair. The [GOV.UK error summary guidance](https://design-system.service.gov.uk/components/error-summary/) supports precise errors associated with affected inputs. Its full page-level summary pattern is not imposed on this two-control screen. Neither source establishes this product’s backend recovery behavior.

Checked against the brief: layout/navigation preserved; no payment claim; R-1842 and three working days included; amount/attachment retained on failure; duplicate-safe retry explicitly required. Outline only—no implementation or usability claim.
