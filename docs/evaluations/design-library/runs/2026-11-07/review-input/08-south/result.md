# Provisional capture, senior review and sync conflict discussion packet

Use this outline to discuss the work with conservators. It is an unbuilt proposal, not a validated interface or a hardware recommendation.

**Evidence boundary:** No credible reference for the combined glove / dim-archive / offline workflow was found in this 107-resource library survey. Its offline and review examples are adjacent mechanisms. Broader discovery added ODK’s documented field-data and parallel-update workflows, but none of the inspected sources establishes control usability with gloves, safe handling of fragile objects, suitable illumination, or compatibility with an unchosen device. No visual sample or product interaction was inspected in this pass.

## Direction carried into the outline

The recorder captures **object ID, observation note, tentative material and optional photo**. A provisional record is not an approved finding. Both versions of a sync conflict stay available; **only the senior reviewer resolves it, with no automatic overwriting**. These are supplied requirements, not borrowed product behavior.

**Explicit discussion assumption:** A senior can mark review complete while retaining an uncertain identification. “Review complete — material still tentative” means the documentation has been reviewed; it does not mean the material was confirmed. If approval requires confirmation locally, keep the record “Awaiting identification” instead. This policy remains unsettled and does not block provisional capture.

## Reference match packet

All source pages below were read as public first-party text on 2026-11-07. Their documentation describes mechanisms; their interfaces were not exercised.

| Reference / inspected scope | Useful match | Decisive mismatch / application boundary | Selected use |
| --- | --- | --- | --- |
| Library `flow-google-maps-offline`: [Download and use offline maps](https://support.google.com/maps/answer/6291838?hl=en), Android preparation, offline limits and update sections | Downloaded scope and freshness are explicit; offline availability has boundaries | Route coverage is not writable conservation data or conflict handling; no glove evidence | Before entering the archive, show which object records and attachments are stored locally and when they were refreshed. Do not borrow map expiry periods. |
| Library `flow-google-docs-suggestions`: [Suggest edits](https://support.google.com/docs/answer/6033474), proposing, individual decisions and preview | A proposal remains distinct from accepted content | Desktop document edits do not establish conservation authority, offline review or handheld usability | Label tentative material as tentative; show recorder evidence beside the senior’s eventual decision. Do not import bulk acceptance or Docs permissions. |
| Library `pattern-govuk-check-answers`: [Check answers](https://design-system.service.gov.uk/patterns/check-answers/#let-users-go-back-and-change-their-answers), correction/return section | Existing answers survive correction and users return to the summary | Occasional service submission differs from repeated field capture | Make summary fields directly editable without repeating other entries. Do not require a separate confirmation screen for every local save. |
| External addition `external-odk-collect-forms`: [Managing Forms in Collect](https://docs.getodk.org/collect-forms/#editing-drafts), draft, finalization and sending sections | Drafts can be saved and edited later; sending is a separate state | ODK finalization and configured edit rules are product-specific; finalization is not senior approval | Separate local persistence, transmission and review status. Keep uncertain material saveable. This is a workflow reference, not a recommendation to adopt ODK or its platform. |
| External addition `external-odk-entity-conflicts`: [Managing Entity conflicts](https://docs.getodk.org/central-entities/#managing-entity-conflicts), parallel updates and conflict handling | Shared base versions explain why two offline edits diverged; warnings expose reconciliation work | Central applies incoming updates in arrival order and can dismiss warnings over current values. That behavior conflicts with this brief | Borrow the explanation of parallel edits and version provenance only. Explicitly reject automatic winning values and warning dismissal as resolution. |

**Considered but not selected:** `flow-linear-triage-decisions` ([upstream locator](https://linear.app/docs/triage), not opened), card only. Explicit dispositions are adjacent to review, but accepting, declining, duplicating and snoozing software issues would import unnecessary outcomes. No upstream Linear inspection is claimed.

**Accessibility boundary:** [W3C’s Target Size (Minimum) explanation](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) describes the web AA target-size criterion and its exceptions. It does not establish that a given target works with gloves. No target dimension, dark palette, voice input, stylus, gesture or device is endorsed by this packet.

## Applied screen and content outline

The proposed screens below are original adaptations for discussion. They do not assert existing software capability.

### 1. Archive work list / offline preparation

Keep object identity, local availability, save state and review state visible together. Example row, using illustrative data:

> Object AR-104 — observation OBS-017  
> Provisional · Saved on this device · Not yet synced  
> Material: possibly parchment — tentative  
> Photo: none attached

A preparation section lists locally available object records, notes, photos and identification vocabulary, plus “Last refreshed [time]”. Missing attachments say “Not stored on this device” rather than appearing empty. An uncached object ID can be entered manually and marked “Object link not yet verified”; this must not fabricate an authoritative object record. Pending local observations remain accessible regardless of connection.

Proposed actions: **New observation**, open a local observation, and inspect **Sync status**. Before field use, conservators must specify what information is needed locally; a green connection badge alone cannot establish readiness.

### 2. Capture observation

Show the object ID at the top throughout capture. Present labeled fields in this order:

| Content | Proposed behavior |
| --- | --- |
| Object ID | Carry it from the chosen object; allow correction. If unresolved, retain the entered identifier and its unverified state. |
| Observation note | Record what was observed, separate from material interpretation. Retain incomplete notes on local save. |
| Tentative material | Plain label “Tentative material — not a confirmed identification”. Permit an uncertain value or “Not identified”; uncertainty is not a validation error. |
| Optional photo | Attach only if archive practice permits it. Capture method, lighting, handling and photo quality remain unresolved; no flash or camera behavior is prescribed. |

Primary proposed action: **Save provisional observation**. Persist a stable observation ID locally before displaying “Saved on this device at [time] — provisional; not yet reviewed”. A separate **Ready for senior review** action queues the saved revision; offline copy says “Queued on this device — reviewer has not received this revision”. Sending it later does not approve it.

If required identity/note content is missing, preserve the entry as an incomplete local draft and explain what prevents readiness for review. Exact local validation rules need agreement. If storage fails, show “Could not save on this device”, retain entered content on screen, and offer retry; never show successful saving or syncing. Navigating back to edit a saved observation returns to its summary with values intact, adapting GOV.UK’s correction loop.

### 3. Senior review detail

A queue shows object ID, recorder, observation date, tentative material, review state and conflict state. Opening an item reveals the original recorder’s note and interpretation, photo availability, revision provenance and any subsequent changes. Distinguish “No photo attached” from “Photo not available offline”.

Proposed senior actions: **Request clarification**, **Mark review complete — uncertainty remains**, or **Record confirmed finding** when the senior supplies the appropriate evidence. Keep the original observation and reviewer rationale, identity and reviewed revision together. Do not infer material certainty from an approval stamp. A returned observation remains preserved and editable as a subsequent revision.

Offline review may inspect locally stored evidence and save a proposed review decision. Until the latest shared revision is checked and the decision is acknowledged, label it “Review decision saved locally — pending sync”; do not announce shared approval. A stale or conflicted revision cannot silently become the approved finding.

### 4. Sync status and senior conflict resolution

Keep sync state separate from review state: **Local only → queued → sending → acknowledged**, with **retry needed** and **conflict requires senior review** as explicit alternatives. Acknowledged means the shared service received that revision, not that a senior approved it. If acknowledgement is lost, say “Receipt not confirmed”; reconcile by stable revision identity before resending so recovery does not create a second observation.

Illustrative conflict summary:

> OBS-017 has two edits based on revision 3. Neither edit has replaced the other.  
> **Recorder’s local version:** “possibly parchment”, note A, photo A; based on revision 3.  
> **Other submitted version:** “possibly paper”, note B, no photo; based on revision 3.  
> **Shared base:** revision 3; show its values and reviewed status.

Use matched field labels in stacked comparison groups on handheld layouts; retain full text and distinguish absent, unchanged and changed values. Show author, source device label if available, base revision and recorded/submitted times. Time order is context, never the rule for deciding truth. A separately captured observation about the same object is not automatically a conflicting edit to this observation.

The recorder can inspect both versions and keep working on other records, but sees “Senior reviewer must resolve this conflict.” The senior compares base/local/other values, preserves or combines evidence into a **new resolution revision**, supplies a rationale and previews the result. Resolving a sync conflict does not itself confirm the material identification. Preserve both input versions and their attachments in history; do not overwrite either.

Before committing a resolution, recheck the shared base. If another edit arrived, preserve the proposed resolution and show the new divergence for another review. An offline resolution remains a saved proposal until acknowledged against the current shared revision. **Leave unresolved** preserves the comparison and routes the item back to the conflict queue. Never replace that decision with “dismiss warning”.

## Discussion and verification boundary

Text checks completed: all four requested capture fields appear; provisional saving survives uncertain material; local save, sync receipt, review and identification certainty have separate meanings; only the senior resolves conflicts; both versions survive; cited mechanisms have explicit mismatches. No app, assets, account, device test, network-loss test, usability study, visual inspection or accessibility conformance assessment was performed.

Before selecting hardware or treating controls as usable, observe conservators’ actual sequence and constraints, including permitted gloves, hand availability, lighting rules and interruptions. Later evaluate candidate input arrangements with approved representative tasks and surrogate objects: entering an uncertain observation, interrupting/reopening offline, returning for review, and understanding a seeded conflict. Measure missed/accidental actions, recovery, legibility and correct interpretation of save/review states. Preserve this as a validation plan; it is not supporting evidence today.

Next discussion decision: can review be completed while material identification remains uncertain, with the explicit label proposed above?
