# Flow and craft decisions

Use the relevant section; a component fix does not require a full journey exercise.

## Select a view by the task

Define the user outcome, necessary information, important handoffs, and completion condition. Choose screens and navigation from dependencies, familiarity, repetition, correction cost, device, and consequences. A page count or click count omits much of the effort.

A guided form can support an unfamiliar occasional transaction. Repeated expert entry may benefit from related information together. An overview supports comparison; a queue supports handling a prioritized item. Neither is universally simpler. If the choice is unresolved, ask about the actual work occasion rather than asking the person to choose an interface pattern name.

Distinguish actions people rarely invoke from state they frequently inspect. Hiding an infrequent action can save space; hiding a frequent state can add repeated inspection and navigation. Preserve relevant labels, nondefault values, and learned locations when they support the task.

## Define the states that change the answer

For each consequential path, identify what caused the state, what information remains trustworthy, what the person can do, and what happens next.

| Similar appearance | Different cause | Appropriate decision |
| --- | --- | --- |
| Empty table | No records exist | Explain first use and offer creation only when available. |
| Empty table | Filters hide existing records | Preserve the filters; make clearing or editing them easy. |
| Empty table | Permission prevents access | Explain the access boundary and a real next step. |
| Empty table | Work completed | Acknowledge completion without implying data was lost. |
| Failed request | Outcome unknown after a side effect | Avoid claiming nothing happened or offering an unsafe duplicate action. |

Use the product's actual state model. Do not fabricate errors, permissions, or recovery operations to fill a template. A review/edit/return path should preserve data and put the person back into an intelligible context.

## Establish a visual direction people can recognize

Connect the direction to the subject, real content, audience, and chosen experience. Identify a few consequential choices: information hierarchy, composition, typographic roles, density, color roles, imagery, and motion when it adds meaning. The choices should reinforce each other.

An “anti-generic” detector cannot establish relevance or quality. A familiar visual device can suit a brief; an unusual device can obstruct it. Avoid mandatory font, weight, capitalization, palette, or card bans. Preserve existing brand choices unless changing them is part of the task.

Prefer meaningful content to invented filler. Placeholder data should be clearly illustrative. A crafted screen must still accommodate long names, real error text, empty or partial data, locale-specific numbers, and different languages where relevant.

## Accessibility and responsive behavior

Start with semantic controls and logical content order. Ensure the actual name, role, state and keyboard behavior fit the control. Adding ARIA does not implement interaction. Focus should remain visible and move predictably after errors, dialogs, or changes of context.

Check readable typography and meaningful foreground/background combinations in real states. Preserve content and controls under zoom, reflow, text-spacing overrides and relevant motion preferences. Density does not excuse unusable targets or clipped text. Content-driven dimensions and logical direction often survive localization better than fixed line counts and manual breaks.

For exact obligations, consult the applicable standard/version/conformance level and its exceptions. For example, WCAG text-spacing values describe tolerance for overrides, not compulsory default styling; Focus Appearance and Animation from Interactions are AAA criteria. See the source links in [evidence and maintenance](evidence-and-maintenance.md).
