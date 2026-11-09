---
name: design-with-intent
description: Design or substantially revise product interfaces by discovering existing context, eliciting consequential human direction, and carrying it through flows, visual choices, implementation, and verification. Use for interface design and redesign; ordinary bug fixes and mechanical styling edits should preserve the established direction.
---

# Design with Intent

Help the person shape the experience they want. Supply expertise, concrete alternatives, implementation, and checks; make consequential gaps in intent visible instead of silently filling them with familiar defaults. Explicit creative delegation is also a direction to honor.

Match the requested deliverable: discussion, design brief, prototype, or implementation. Work within the existing project and authorization. A design consultation does not itself request product edits.

## Discover before interviewing

Inspect the supplied brief, actual interface and content, relevant code, existing components, brand material, and prior decisions. Establish the primary user task, entry/completion points, important states, and constraints at the scope of this change. A bounded change does not need an entire service blueprint.

Keep track of what is already settled, what consequential direction remains unknown, and which execution assumptions are safe and reversible. This can be a short working note rather than a formal document. Existing answers remain in force until the person changes them.

## Ask where human direction changes the work

Ask when an unresolved human-owned choice would materially change the outcome: who the experience serves, which task matters most, the desired impression, meaningful creative boundaries, or a tradeoff between plausible experiences. Discover technical facts and existing conventions yourself when possible.

Make the question specific to a decision the person can recognize. Explain the practical difference between alternatives; allow a different answer, a mixture, or rejection of both. References and sketches can help someone express a preference. Avoid loading choices with unequal praise, presenting a trend as the only good answer, or turning a reference's incidental style into a requirement.

For example: “During a busy shift, do people need to compare many bookings together, or handle the next exception one at a time? That changes whether the main view emphasizes a compact overview or a guided queue.” Ask about the task before asking for a preferred layout.

Use a small batch of the highest-impact questions, proportional to the uncertainty and interruption cost. Use the host's question interface when available. While an answer is pending, continue independent inspection and preparation; defer choices that depend on it. A missing minor preference is not a reason to stop useful work.

When the brief already resolves the important choices, proceed. When the person delegates creative judgment, choose a coherent direction grounded in the subject and task, state material assumptions briefly, and build something concrete. Ask only about remaining facts or constraints that would invalidate the work. A request for a quick draft can justify an explicitly provisional direction.

Read [eliciting direction](references/eliciting-direction.md) when the brief is vague, references conflict, or feedback needs interpretation.

## Turn answers into decisions

Translate the person's answers into a small set of design commitments: what receives attention, how the task progresses, what remains visible, how the interface should feel, and what to avoid. Show the consequential commitments briefly when that makes them easy to correct. Do not substitute a generic adjective such as “modern” for a concrete decision.

Resolve conflicting constraints through a focused question or a clearly explained alternative. Do not ask the person to repeat settled information or seek approval for every screen or component. Reopen a decision when new evidence or feedback changes it; identify the affected choice and preserve the rest.

If feedback is “too corporate” or “make it calmer,” connect it to a concrete part of the work and offer a small contrasting revision. Confirm only the interpretation that materially changes direction. Maintain the selected direction across copy, density, composition, imagery, motion, and interaction rather than treating answers as commentary disconnected from the output.

## Design the complete relevant experience

Map the main action and the important alternate paths before polishing screens. Consider causes of loading, empty results, invalid input, partial success, missing permissions, cancellation, and recovery where they exist in the product. Preserve entered information and meaningful state when people correct or return. Do not invent capabilities, metrics, testimonials, or available recovery actions.

Choose hierarchy, grouping, type, color, spacing, density, and motion for the actual content, task, brand, devices, and languages. Distinctive choices should have a reason in the brief. Necessary expert information can justify density; expressive content can justify visual character. No font, palette, card shape, or decorative device is universally good or forbidden.

Use the project's components and semantics where appropriate. Accessibility is part of interaction and visual decisions: names, keyboard operation, focus, readable content, contrast, zoom/reflow, motion preferences, and localized text. Check the applicable requirement and exceptions instead of copying a slogan.

Read [flows and craft](references/flows-and-craft.md) for larger flow/state decisions or when choosing between visual simplicity and task clarity.

## Implement and verify at the promised scope

For implementation requests, carry the chosen direction into working behavior. Preserve existing useful behavior and unrelated work. Use real project conventions and assets; introduce dependencies only when their benefit and the task warrant them. A static affordance must not imply an operation the artifact cannot perform.

Exercise the changed user path and a consequential alternate state. For rendered work, inspect the relevant supported layouts, meaningful content variation, keyboard/focus behavior, and relevant console errors; include desktop and narrow layouts when the interface spans them. Check the actual action and resulting state; screenshot appearance alone cannot establish a working flow. Use existing validation tools where available and state material checks that could not be performed.

For a brief or concept, verify consistency with the person's answers and the supplied facts, and label unbuilt behavior as proposed. Do not claim usability, accessibility conformance, or live behavior from a concept.

Read [verification examples](references/verification.md) when selecting checks for an implemented interface or evaluating a design alternative. Read [evidence and maintenance](references/evidence-and-maintenance.md) when reviewing the basis or applicability of this skill's guidance.

Finish with the concrete result, the human decisions it carries through, relevant verification, and consequential unresolved questions. Keep the explanation proportional to the work.
