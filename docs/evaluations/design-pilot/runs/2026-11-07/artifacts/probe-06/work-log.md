# Cedar request-flow work log

## Scope and discovery
- Read `request.md` and existing `index.html` in probe-06 only. Existing demo merely appended “Submitted”; no review or reservation policy was documented.
- Read target-v1.1 `SKILL.md` and references `eliciting-direction.md`, `flows-and-craft.md`, and `verification.md`.
- Host skills read: `i-have-adhd`, `polylane`, `devrelay-community-wisdom`. Polylane live-system checks do not apply to this standalone local file. External community research was omitted under the explicit no-network sandbox constraint.
- Asked coordinator to relay missing product facts before selecting status or confirmation language.

## User direction received
Submission joins a review queue. A studio manager checks stock and approves or declines. Nothing is reserved until approval. Demo must simulate both decisions per pending request. Declined requests support quantity revision and resubmission. Quantities are whole numbers 1–20.

## Implementation
- Edited only sandbox `index.html`; retained Cedar name, green/paper palette, Clay and Glaze choices, and local in-memory behavior.
- Added explicit review process, reservation boundary, “Send for review,” pending confirmation and per-request statuses.
- Added clearly labeled manager decision simulations. Approval and decline cannot be applied to already decided requests.
- Added inline revision/resubmission on declined requests; the same request returns to pending. Preserved revision drafts when list re-renders for another action.
- Added quantity validation on initial and revised submissions, error descriptions, focus to invalid controls, semantic forms, live confirmation, focus after status changes, empty state, and narrow-layout CSS.
- Stated that all demo state resets on refresh; no real orders, stock checks, or reservations occur.

## Assumptions
- Item choices remain the supplied Clay/Glaze; measurement units were not invented.
- No review turnaround, email notification, pickup instructions, partial approval, or decline reason invented.
- Status is visible in the local list; the page explicitly describes this as demo behavior.
- Revisions update the same declined record rather than creating duplicate requests; only quantity changes.

## Checks actually run
- Ran `node check.cjs` successfully. This compiles and evaluates the inline JavaScript using a minimal local DOM stand-in.
- Checked invalid blank, zero, negative, >20, decimal, nonnumeric and infinite values; preserved input and invalid-field focus; accepted boundary values 1 and 20.
- Exercised initial pending submission, decline, invalid revision, preserving revision draft across another submission, valid resubmission to pending, approval, and rejecting a second decision on an approved record.
- Checked confirmation reservation language and absence of remote scripts/styles/network API calls in source.
- Reviewed source for semantic labels, error descriptions, live announcements, focus handling and responsive CSS.

Rendered desktop/mobile UI, actual native browser input/event behavior, keyboard interaction, visual contrast, screen-reader behavior and console execution in a browser remain unobserved. No browser tools/processes, server, network, installs, backend writes, publishing or external messages were used.
