# Provisional capture, review and conflict discussion packet

Use this outline to discuss the record states with conservators. It is an unbuilt proposal, with no recommended hardware and no validated glove or dim-light interaction.

## Evidence boundary

**The library did not supply a credible combined glove/dim-light/offline match.** A scoped search of its index and entry text found one relevant offline example, but no conservation capture or record-sync-conflict example. This does not establish that such evidence does not exist elsewhere.

The three references below are adjacent workflow references. Their usability does not carry over to gloved work. No source visuals or live product interactions were inspected; the evidence is first-party documented flow text. Neither ordinary mobile usage nor a sufficiently large-looking control establishes glove compatibility. No control size, gesture, display theme, brightness, target device or input method is prescribed here.

## Reference matches and deliberate limits

| Reference / inspected locator | Justified transfer | Mismatch / excluded transfer | Applied decision |
| --- | --- | --- | --- |
| [Google Maps: offline areas](https://support.google.com/maps/answer/6291838?hl=en), “Select your own map,” “Use offline maps,” “Update offline maps” | Make preparation, available local content and freshness explicit; downloaded data has bounded capabilities. | Android navigation documentation, not editable conservation records. Does not demonstrate durable local capture, attachment sync, conflicts, gloves or dim light. Do not copy expiry/deletion behavior into observation retention. | Before archive work, show which records/reference data are stored locally and when refreshed. During work, identify local versus shared state. |
| [Google Docs: suggest edits](https://support.google.com/docs/answer/6033474), “Suggest changes,” “Accept or reject suggestions,” preview | Distinguish proposed content from authoritative content and expose the result to a decision-maker. | Document editing, primarily computer instructions inspected; no conservation authority model, offline conflict evidence or gloved interaction. Do not import bulk acceptance or its color-only markup. | “Provisional — not an approved finding” remains visible; review has a distinct decision and resulting-record preview. |
| [Linear: Triage](https://linear.app/docs/triage), “Create issues,” “Take actions,” “Triage responsibility” | Intake precedes normal work; requesting more information differs from final disposition; ownership matters. | Issue-tracker defaults and queue-clearing outcomes do not define conservation review. Do not copy canceled/declined status, shortcuts, snooze hiding, AI or duplicate merge. | Review queue distinguishes awaiting review, more information requested and reviewed. Senior reviewer ownership is explicit. |

No selected source directly justifies a sync-conflict resolution design. The proposal below comes from the user's requirements to retain both versions, prohibit automatic overwriting and reserve resolution for senior reviewers.

## Settled direction and labeled assumptions

Settled: capture object ID, observation note, tentative material and optional photo. Provisional is not approved. Records must remain usable offline. Conflicts retain both versions; only a senior reviewer resolves them; no automatic overwrite. Hardware remains undecided.

**Discussion assumptions:** a senior reviewer may record “Reviewed — material still uncertain” with a reason, rather than inventing a definitive identification. This is distinct from an approved material finding. The institution must settle approval terminology and authority before implementation. The proposal also assumes identifiable staff and stable record/revision identifiers so provenance and conflict permissions can be explained. Neither identity availability offline nor persistence technology has been established.

## Applied flow and content outline

### 1. Local records / archive preparation

Purpose: know what is available before disconnecting and return to ongoing work afterward.

- Show object identifiers and locally available observations; name the local scope, reference-data refresh time and optional photos available locally. Do not imply the complete collection is stored.
- Keep separate labels for **record review** (“Provisional,” “Awaiting review,” “More information requested,” “Reviewed — material still uncertain,” or institution-approved finding status) and **transfer** (“Saved locally,” “Waiting to sync,” “Sync confirmed,” “Conflict — senior review needed”). One combined “Done” badge would hide important differences.
- Primary proposed route: “New observation.” Existing local records open without connection. If object context is unavailable locally, explain that limit; do not silently substitute stale remote content or fabricate an object match.
- Sample copy: “Offline. Showing records stored here. Shared changes may be newer.” A refresh timestamp describes freshness, not correctness.

Local preparation must not expire or remove captured observations merely because downloaded reference data becomes old. Maps supplies a bounded-cache analogy, not this retention rule.

### 2. Capture observation

Content order: object ID → observation note → tentative material → optional photo → save outcome. Keep object ID and provisional status visible when returning to edit.

| Content / action | Proposed behavior and wording |
| --- | --- |
| Object ID | Identify the object without assuming barcode hardware or scanning. Proposed required field; unresolved or duplicate identifiers need an explicit correction path rather than guessing. |
| Observation note | Preserve what was observed separately from interpretation. Proposed required field; retain entered text after validation errors. |
| Tentative material | Label “Tentative material — not confirmed.” Allow “Unidentified” or “Uncertain” with a free-text hypothesis; never force a confident material choice to save. No automated identification is proposed. |
| Optional photo | Omission does not block capture. Imaging permissions, lighting and acceptable handling are institution decisions. Show attachment-local-save and attachment-transfer state independently where different from the note. No flash, camera or photo quality recommendation. |
| “Save provisional observation” | Request a local save. Only after verified local persistence show “Saved locally. Provisional — not an approved finding.” If saving fails, retain the entry on screen and say it is not saved; offer a retry only when its outcome is known. Do not show success based on connectivity or a queued request. |

Saving locally returns to a readable local record with its stable identifier, author/time provenance, tentative wording and current attachment status. “Waiting to sync” must never imply shared availability. Leaving an unsaved entry preserves a draft if supported; otherwise a clear leave decision must identify what would be lost. This is a required implementation discussion, not a working recovery promise.

### 3. Senior review

Entry: locally available review queue or synced record, marked with the version reviewed and the last known shared state. An offline queue is explicitly a local snapshot and may be incomplete.

1. Open observation context: object ID, original note, tentative material, available photo, contributor and revision provenance. Show missing local attachments as unavailable, not absent from the record.
2. Compare the proposed finding with the captured observation. Retain original observations and review history; a reviewer correction does not erase the original statement.
3. Offer domain-specific proposed dispositions: “Request more information,” “Record review — material still uncertain,” and an institution-defined approval action. Show the resulting wording before committing a review. Assumption: review can acknowledge uncertainty; approval policy remains unsettled.
4. After a locally saved review, say “Review saved locally; shared status not yet confirmed.” If the base changed, route to conflict handling before describing the shared finding as final. Do not let synchronization itself approve a provisional record.

Capture staff can see review outcome and the next owner. No bulk approval is proposed. Senior conflict resolution and approval are distinct decisions: choosing between two provisional versions does not automatically approve either.

### 4. Synchronization and conflict detail

A proposed synchronization attempt checks record/review revisions and attachment outcomes. Detecting a competing version must preserve the local and shared versions and place the record in “Conflict — senior review needed.” Avoid claims that timestamps alone establish which version is correct.

Conflict detail presents the following in reading order; a handheld layout can stack the versions rather than rely on a wide side-by-side view:

- Object/record ID and explanation: “Two versions changed since the last shared version. Both have been retained. No version has overwritten the other.” Only use this explanation when that cause is actually detected.
- “Local version” and “Shared version,” each with author, recorded time, version ID, note, tentative material, review state and photo availability. Show the common prior version when actually available; otherwise state that it is unavailable.
- A field-level account of differences. Example, clearly illustrative: local tentative material “Possibly wood”; shared tentative material “Possibly leather.” Preserve uncertainty in both. Do not describe the newer timestamp as the recommended answer.
- Capture-staff view: “Only a senior reviewer can resolve this conflict.” They can read both versions and continue unrelated capture. If shared conflict content is not available offline, keep the local record usable and explain what must be retrieved later; do not offer a blind resolution.
- Senior-reviewer view: inspect both; choose one as the resulting working version or compose a reconciled version with a reason; preview all resulting fields, then explicitly confirm resolution. Neither original is deleted. If another revision arrives before confirmation, retain the proposed resolution and require another comparison. Permission uncertainty offline leaves the conflict unresolved rather than granting authority.

After resolution, show the decision, reviewer, reason, resulting version and access to both prior versions. A locally saved resolution remains “Waiting to sync” until acknowledged by the shared system. Partial attachment transfer or an unknown server outcome stays explicit. Retry uses the same record identity and must not silently create duplicate observations; the persistence/sync contract needs engineering validation.

## Physical-context decisions intentionally deferred

The content outline favors explicit labels, persistent state and recoverable edits because loss of context matters. These are proposals to test, not a claim of glove or dim-light usability. Avoid hidden-only gestures or color-only status as a provisional design commitment; even labeled controls still require validation.

Before selecting hardware or interaction dimensions, observe representative conservators using the actual permitted glove types and archive illumination, with safe stand-ins for fragile objects. Establish handling constraints, hands available for input, allowable illumination/imaging and whether text entry or photo capture is practical. Compare candidate input arrangements only after those facts are known. A dark palette is not assumed to improve dim-light work.

## Discussion checks and actual verification

Actual checks: supplied brief and scripted replies traced to the four screens; three full library cards and their relevant first-party text inspected; local search checked for glove/dim-light/offline/conflict fit; prohibited automatic overwrite absent from this proposal. No implementation, hardware test, visual inspection, accessibility audit, offline persistence test or live conflict exercise was performed.

Before acceptance, exercise at least these scenarios with an implementation: save/reopen uncertain observation offline; local save failure; optional photo absent or partially transferred; senior review retaining uncertainty; two competing edits; unauthorized resolution attempt; new edit arriving during resolution; reconnect with unknown prior sync outcome. Evaluate whether staff correctly distinguish local save, shared sync, review and conflict completion. These are future checks, not passed results.

**Next discussion decision:** confirm whether “Reviewed — material still uncertain” is an allowed review outcome and define how it differs from the institution's approved finding.
