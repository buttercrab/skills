# Pebble Post — a little voice letter from the shore

Choose **a quiet coastal post office hosted by Pip, an original pebble creature**. A smooth, lopsided stone body, tiny arms and expressive eyebrows give Pip a recognizable silhouette without a childish costume. Pip is an interested language partner: invites an everyday story, listens, responds to its meaning, and offers one small improvement. Adults get warmth and room to hesitate, with no scores, streak pressure or cluttered dashboard. Scripted feedback confirms the expressive partner direction: missed days must never disappoint Pip, and corrections must never become a red failure screen.

This is a proposed design outline, not a built or tested app. Creative choices are delegated; no color, font or species decision is needed from the user. For concrete copy, assume an adult beginner practicing English, with explanations in English; actual language pair, script coverage and proficiency would be configured before implementation.

## Reference / match packet

| Reference and inspected evidence | Transfer into Pebble Post | Boundary / mismatch |
| --- | --- | --- |
| [Finch](https://finchcare.com/) · library ID `visual-finch-companion`. Read full local card; directly viewed public desktop hero in native Chrome on 2026-11-07. Blue sky, green ground, two dressed birds and an outlined headline form one illustrated setting around the invitation. | Make shore, postbox, creature and voice-letter metaphor one coherent world. Pip occupies the prompt scene instead of floating beside unrelated dashboard cards. | Public marketing composition only. No app task, wellbeing outcome or usability established. Do not copy birds, landscape assets, ratings or the pet-care obligation. |
| [Duolingo](https://www.duolingo.com/) · `visual-duolingo-welcome`. Read full card; directly viewed public desktop first viewport in native Chrome on 2026-11-07. A bright cast sits beside a rounded heading and prominent green start action, with an outlined returning action. | Let a character carry invitation while one obvious action carries the task. Record, listen and send each receive priority at their own stage. Friendly direct copy and restrained choice count. | Hero is not evidence for a lesson or recorder. Avoid copying owl, cast, green brand, proprietary type or progression/reward mechanics. |
| [Android runtime permissions](https://developer.android.com/training/permissions/requesting) · `principle-contextual-permissions`. Read card and official source text, Basic principles / Workflow, lines 72–96. | Ask for microphone access at Record; explain its purpose and preserve the selected prompt after denial. | Android-specific guidance is not proof of iOS/web behavior. No device or permission interaction tested. Study linked in card was not opened and is not used as empirical support. |
| [Kagi](https://kagi.com/) · `visual-kagi-search-character`. Full local card read; original page not opened. | Comparison only: a smaller character presence may help during the precise review step. | Not selected as a governing visual source: search-first tool is too restrained for the delegated expressive direction. Card evidence is historical-to-this-task, not my own live visual inspection. |

No source demonstrates the complete voice loop. Recording safety, deletion, review gating and correction behavior below are decisions derived from the supplied brief.

## Visual and creature commitments

Warm shell-paper background, deep ink text, tidal teal for primary actions, apricot for Pip's cheek marks and small environmental accents. Use a rounded humanist sans for short headings and a clear system sans for prompts, explanations and controls, with native script fallbacks. Color combinations require rendered contrast checks later; these are roles, not validated tokens.

A small illustrated shore scene fills the upper third of the prompt screen. Below it, real prompts receive the space. During recording, Pip becomes a quiet small listener at the top; the timer and Stop control take over. During review, the sound player dominates. Correction appears as a voice letter unfolding on paper, not a report card. Motion is a brief envelope arrival or eyebrow response; no continuous bouncing, compulsory sound or moving recording target. Reduced motion uses static expressions and immediate state changes.

Pip never looks disappointed when a person misses a day, deletes, declines permission or stops. Returning after any gap uses the same warm “What shall we talk about?” invitation: no neglected-creature pose, guilt copy, broken streak or catch-up debt. On departure: “Thanks for the story. See you when you feel like talking.” The character offers encouragement; it does not pretend to be a human or imply that it needs care. Introduce it plainly as a fictional practice companion with generated replies. Recording status is literal interface text, never conveyed only through Pip's face.

## Applied screens and content

### 1. Choose a prompt — the post office doorstep

Top: Pebble Post wordmark, compact “English · beginner” context and change control. Pip leans over a low postbox: **“What shall we talk about?”** Three tappable prompt rows show an everyday topic plus its actual question:

- A small pleasure — “What made you smile today?”
- A meal — “What did you eat yesterday?”
- Tomorrow — “What would you like to do tomorrow?”

Selecting one opens its recording page; no automatic microphone activation. A short explanation says “A voice message, up to 45 seconds. Listen before you send.” There is no lesson map or statistics landing screen.

### 2. Record — one prompt stays visible

Example chosen prompt: **“What did you eat yesterday?”** Pip: “One or two sentences is plenty.” Optional starter: “Yesterday, I…” The large bottom action is **Record message**. On first use, explain “Microphone access lets you record your message. You can listen and delete it before sending,” then invoke the platform request at this action boundary.

Active state: literal **Recording**, elapsed timer `00:12 / 00:45`, simple waveform and a stationary **Stop recording** button. No press-and-hold requirement. At 45 seconds stop automatically and go to review, with “45-second limit reached. Your message is ready to review.” Zero-length capture returns to ready with “No recording yet. Tap Record message to start.” Never auto-send.

### 3. Review — an unsent voice letter

Heading **“Listen before you send”**; explicit badge **Unsent**; selected prompt, duration, Play/Pause and scrubber with elapsed/total time. Pip's line: “Take a listen. You can keep it or start fresh.”

**Send to Pip** remains disabled until playback reaches the end once, with visible explanation “Listen to the full message to enable Send.” Scrubbing to the end alone does not count. Replay remains available afterward. This deliberately implements the brief's listen-before-send requirement; it is a proposed interaction, not a reference-derived usability finding.

**Delete recording** is a visible text button below the player, separate from Send. It opens “Delete this unsent recording?” with **Keep recording** and **Delete recording**. Confirming removes the captured audio, resets the playback gate, keeps the chosen prompt and returns focus to Record message. No audio is sent by deletion. **Record again** uses the same discard confirmation before replacing an existing take. Back navigation with audio offers Keep editing / Delete and leave; never silently loses the take.

Proposed data rule: unsent audio stays on the device until explicit Send; discard clears that local take. This privacy behavior must be implemented and verified before the product promises it. Session-only draft retention is assumed; persistence across app termination is outside this outline.

### 4. Send and receive — one encouraging correction

On explicit Send, disable repeat submission and show **“Sending your message…”**. After server acknowledgment, mark **Sent** and show **“Pip is preparing a reply…”**; do not say sent before acknowledgment. Proposed response contains a short playable message with matching text, followed by exactly one correction.

Illustrative exchange for the meal prompt:

> Learner: “Yesterday I eat noodles with my sister.”
>
> Pip: “Noodles with your sister sounds lovely. One small change: ‘Yesterday I **ate** noodles with my sister.’ Use **ate** for something that happened yesterday.”

The correction block labels **One thing to try**, highlights only eat → ate with an ink underline on warm paper, and provides **Play example**. Keep Pip engaged and interested; no red failure panel, cross mark, alarm sound or disappointed pose. The correction is a normal part of the same conversation, not an error destination. Do not grade every error or invent a mistake if the utterance is already suitable; in that case offer one optional natural phrasing, clearly labeled as optional. A low-confidence transcription should ask for clarification instead of confidently correcting a misheard word. Generated feedback accuracy remains unvalidated.

### 5. Try again or stop — a complete stopping point

Two explicit choices: **Try that sentence again** and **Done for now**, both visible without scrolling past a reward animation. Retry opens the same prompt with the suggested sentence visible; it makes a new unsent take and repeats record → review → send. The sent original remains separate. Done shows a still Pip waving and “One voice letter sent. Thanks for the story.” No demand for another prompt. Finishing after the reply is a successful session.

## Failure state: microphone denied

Cause: the platform denied or revoked microphone access when Record was invoked. Preserve the selected meal prompt and starter; there is no audio to recover. Show **“Microphone is off. Recording needs microphone access.”** Offer **View microphone help** and **Back to prompts**. Help describes the appropriate platform settings path only after platform detection; do not repeatedly reopen the permission request or promise a universal settings shortcut. Pip stays calm: “We can come back to this.” Prompt browsing still works. Choosing Record after permission becomes available rechecks it before starting.

For send uncertainty, the implementation must preserve the take and distinguish confirmed rejection from unknown delivery. Do not offer a blind duplicate send or claim “nothing was sent” without evidence. Exact reconciliation is a later technical contract, not a capability established here.

## Phone behavior and verification boundary

Use a single column with controls near the lower reachable area and safe-area padding. Keep the prompt visible while recording; allow scrolling and growing text instead of clipping translated sentences. Target at least 48×48 CSS pixels for key controls as a design target, with separation around Delete. Use text labels, semantic buttons, visible focus, accessible timer/status announcements at meaningful transitions rather than each second, and an accessible player. The reply has text so listening is optional; speaking remains intrinsic to this product. Wide screens keep a narrow conversation column rather than adding metrics panels.

Completed checks: traced every required step, 45-second stop, mandatory review, unsent deletion, retry, voluntary stop and a caused failure state into the outline; compared character prominence across prompt/record/review; separated live visual observations from local-card-only evidence. No app, assets or prototype generated. No recording, device, responsive rendering, assistive technology, accessibility conformance or usability test performed. Before build acceptance, exercise the full loop and denial/deletion paths on actual supported phones, with long prompts and the intended language scripts.
