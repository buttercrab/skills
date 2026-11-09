# Revised reimbursement outline

Keep the existing visual design, navigation, field order and banner location. Change only the content and state behavior described below. This is a proposed outline, not an implemented screen.

## Default screen

1. Heading: **Submit reimbursement request**
2. Supporting text: **Submit your expenses for finance review. Finance usually replies within three working days.**
3. Existing **Amount** field.
4. Existing **Receipt attachment** control.
5. Primary button: **Submit request** (replaces “Send”).

## State outline

| State | Visible content | Action and retained state |
| --- | --- | --- |
| Submitting | Button: **Submitting…** | Prevent repeat activation while pending. Keep amount and attachment. Do not show a success banner until the server confirms creation or recovers the existing request. |
| Confirmed success | Existing success banner title: **Request submitted**. Body: **Request R-1842 is awaiting finance review. Finance usually replies within three working days. No payment has been made.** | Disable the submission action for this completed request; retain the visible amount and attachment as the submitted details. Keep existing navigation. Do not imply approval or payment. |
| Confirmed submission failure | Existing banner area: **Request not submitted**. Body: **Your amount and receipt attachment are still here. Try submitting again.** | Existing button position: **Try again**. Keep both inputs intact. Retry the same submission operation. |
| Connection lost or result unknown | Existing banner area: **Submission not confirmed**. Body: **We couldn’t confirm whether your request was submitted. Your amount and receipt attachment are still here. Try again to confirm your submission.** | Button: **Try again**. Preserve inputs and the same operation identity. Do not assert that no request exists. If the original succeeded, retry resolves to that request and shows its reference. |
| Invalid input, if existing validation rejects a field | Show a specific error beside the affected field, based on the actual validation rule. Keep the other entered information. | Allow correction and resubmission. Do not invent receipt, currency, size or amount restrictions. |

R-1842 is the supplied example reference. Display the actual server-confirmed ID, including when an earlier successful submission is recovered.

## Safe retry requirement

“Try again” must not create a second request. Associate the original submission with a stable operation/idempotency identifier and reuse it on retries, including after a timeout. The backend must return the original request if it already exists and create at most one if it does not. Disabling the button alone does not satisfy this requirement. This is a required behavior to verify, not a claim about the current backend.

Keep the payload for an unresolved attempt intact until its outcome is known; do not submit changed details as a new operation while the old one might have succeeded. A confirmed validation rejection can return to editing. Announce status changes through the existing accessible status/error mechanism; this outline does not establish accessibility conformance.

## Brief rationale and reference match

“Submit request” names the operation the backend performs. “Request submitted” confirms that operation, while “awaiting finance review” and the usual reply interval explain what follows. “No payment has been made” corrects the previous “Paid!” implication. Confirmed failure and unknown outcome need different wording because a lost response can follow a successful creation.

Selected reference: [GOV.UK confirmation pages](https://design-system.service.gov.uk/patterns/confirmation-pages/), reached through the library’s `system-govuk` card. Its textual guidance connects a confirmed transaction to a reference and next steps/timing; those mechanisms shaped the R-1842 and finance-review banner. Its full-page government pattern and branding are a mismatch for this narrow repair, so neither layout, navigation nor institutional extras are adopted. Inspected: local card and live primary documentation text, including the example markup and “How it works” section; no rendered sample or interaction was inspected. Duplicate prevention comes from the supplied requirement, not this reference.

## Checks and limits

Checked the outline against all supplied facts: request creation only; R-1842; usual reply within three working days; preserved amount and attachment; duplicate-free retry requirement. Checked every success label for payment/approval implications and separated uncertain outcomes from confirmed failure. No app, backend, screenshot or live submission was supplied or tested. Safe retry and status announcements require implementation verification. No additional user decision is needed for this bounded wording repair.
