# Design-with-intent development smoke check

Simulated deliverables only. No real product, image, upstream page or browser was inspected. Local skill guidance and selected catalog cards were read. Card receipts describe earlier library work; they are not observations made during this check.

## A. Museum event-flow trial for a reusable skill

### Next response

I'll use the museum example to test how the reference skill handles a concrete state distinction, then return the findings to the skill. The supplied listing has date and title only; the trial below adds proposed availability language and compares the implications. This stops at a review artifact—there is no museum implementation target here.

### Bounded trial artifact

**Purpose:** test whether the skill can connect a reference mechanism to a real information gap without taking over the example product.

**Known entry:** a visitor scans an event listing. **Trial completion:** the visitor can distinguish available, sold-out and waitlist events before opening details. Booking, payment and waitlist enrollment are outside this trial.

Illustrative content, not actual museum inventory:

| Current card | Proposed listing specimen | Detail handoff |
| --- | --- | --- |
| 14 Nov · Night at the Museum | 14 Nov · Night at the Museum · **Available** | Open event details; do not promise a reserved place. |
| 15 Nov · Curator's Tour | 15 Nov · Curator's Tour · **Sold out** | Keep event information reachable; no booking implication. |
| 16 Nov · Print Workshop | 16 Nov · Print Workshop · **Waitlist** | Open details explaining what joining the waitlist means before any commitment. |

Place the text status next to the date/title group, using the museum's existing typography if eventually applied. Color can reinforce it but must not carry the distinction alone. The supplied facts do not establish live capacity data, actual join controls or promotion rules; no automatic promotion or confirmation copy is specified.

**Reference comparison:**

| Resource read | Useful mechanism | Decisive mismatch | Transfer into this trial |
| --- | --- | --- | --- |
| `flow-meetup-waitlist`, local annotation and documented sequence | Waiting and confirmed attendance are separate states. | Meetup's eligibility, priority and promotion rules are not museum facts; its live workflow was not tested here. | Keep “Waitlist” distinct from “Available”; require actual museum rules before designing enrollment or notifications. |
| `pattern-carbon-empty-states`, local annotation | Explain state by its cause and provide a real next action. | This is not an event-listing example and says little about museum visual character. | A sold-out card remains an informative event record; it is not a missing-data empty state. |

**Return to the parent skill:** this trial yields a candidate worked example: “availability is information people inspect while browsing; show it at the listing, then preserve the distinction at the action boundary.” A useful reference card should record which states are supported, which transitions are documented, and which business rules cannot transfer. A card with only a beautiful event thumbnail would not substantiate those transitions. No skill change has been made.

**Remaining work:** source/flow inspection would be needed to establish the museum's actual states, update timing and waitlist meaning. A rendered specimen could then check long titles and text-only status recognition. The bounded artifact is complete; it establishes no usability improvement.

**References read:** `SKILL.md`; `references/discovery-and-selection.md`; `references/flows-and-craft.md`; relevant index regions; `library/entries/flow-meetup-waitlist.md`; `library/entries/pattern-carbon-empty-states.md`. All paths are relative to `/Users/jaeyong/skills/skills/design-with-intent/`. No upstream source followed.

## B. Visual browsing and collecting supersedes the provisional task-first sketch

### Next response

Your answer makes visual browsing and collecting the main path. I'll replace the displayed task-first entry with previews and a direct way to save favorites, keeping the existing shortlist and compare view available. The earlier “guided matching or comparison?” question is superseded. The three supplied openings are descriptions, so the outline below uses labeled preview slots rather than claiming a visual selection.

### Revised compact screen / flow outline

**Browse**

```
Patterns                         Saved (3)   Compare
[Search patterns…]   [optional visual/category filters]

[Photo-led opening]      [Product-screen opening]    [Short input-led opening]
 Description supplied     Description supplied       Description supplied
 Preview unavailable      Preview unavailable        Preview unavailable
 [Open] [Save]            [Open] [Saved]              [Open] [Save]

Continue browsing…
```

This is a schematic of the revised entry, not a screenshot or functioning prototype. In the real catalog, retain its working previews in these positions; show the missing-preview label only for samples lacking actual images. Do not manufacture images for the three descriptions or rank their visual quality.

1. Enter Browse directly. Show existing previews before asking for a task. Optional filters help people narrow exploration without becoming a questionnaire.
2. Save a pattern from its card; expose the resulting saved state and current collection count. Reuse the existing shortlist as the collection rather than creating a second competing store.
3. Open a pattern to inspect its larger existing preview, source and suitability notes. The supplied descriptions can distinguish *what the opening contains*: a photograph, a product screen or a short input. They cannot establish composition, craft or visual appeal. Save/unsave stays available in detail.
4. Return to the same browse position and filters. Saved opens the existing shortlist with preview-led revisiting and removal.
5. From Saved, people may choose candidates for the working Compare view. Preserve its current capabilities and selection rules. Comparison remains optional; saving an appealing pattern does not declare it the best task match.

**Relevant alternate states:** no saved patterns → “Save patterns as you browse” with a return-to-browse action. A search/filter with zero results → retain query/filters and offer clearing them. Missing imagery → show the description and an honest missing-preview state; do not treat it as a viewed visual sample. Unsave leaves the browse context intact.

**Resource choices:** the local `visual-pudding-story-index` card suggests item-specific specimens within stable browsing structure; this informs preview prominence, without adopting its dark palette or expressive type. The `flow-airbnb-collaborative-wishlist` card separates collecting from commitment; this informs retaining the shortlist without a forced winner. Travel collaboration, votes and sharing rules do not transfer. Both are card-level readings here, not fresh image or flow inspection.

**Decision record:** human answer = browse visually and collect. Displayed task-first variant = observed display state only, not endorsement. Retired dependencies = task-first entry, mandatory task filters and the guided-matching-versus-comparison question. Preserved = previews, shortlist and working compare view.

**Remaining work:** replace the provisional schematic in the actual UI only if implementation is requested; inspect the supplied images when available before judging visual matches; exercise save, return position and optional compare if built. This outline makes no claim of measured usability.

**References read:** `SKILL.md`; `references/eliciting-direction.md`; `references/discovery-and-selection.md`; `references/flows-and-craft.md`; relevant index regions; `library/entries/visual-pudding-story-index.md`; `library/entries/flow-airbnb-collaborative-wishlist.md`. Paths use the same skill root as A. No upstream sources or images opened.

## C. Compact expert screen: row removal and empty recovery

### Next response

I'll keep the existing brand, dense comparison rows and single selected detail. Here's the keyboard and recovery outline, with removal treated as removing an item from the comparison. If the product uses “remove” to delete an underlying record, that operation needs its existing destructive-action rules; this outline does not define record deletion.

### Interaction outline

**Populated screen:** retain the current comparison rows and detail panel. Use the existing row-action position for a native button named “Remove [item name] from comparison.” Keep focus visibly identifiable using the existing component styling. Tab reaches the action; Enter or Space invokes it. Do not add a global Delete shortcut or change table navigation just for this action.

**After successful removal:**

| Situation | Detail selection | Keyboard focus |
| --- | --- | --- |
| Remove an unselected row | Keep the selected item's detail. | Next remaining row's corresponding Remove button; previous row's if the removed row was last. |
| Remove selected row, others remain | Select the next row in the current order; use previous row if last. Update the one detail panel. | That row's Remove button. |
| Remove final row | Clear the old detail; show compact empty content. | Focus the empty-state heading with temporary programmatic focus, then let Tab reach an existing recovery action. |

A polite status announcement says, for example, “Curator's Tour removed from comparison. 2 items remain.” Avoid moving focus into the detail panel after every removal. Keep sort/filter state and the surviving rows' order.

**Empty recovery:**

- Removal emptied the comparison: “No items in comparison.” Offer the product's existing route for choosing items, using its actual label. If that route does not exist, do not draw a working-looking button; the implementation needs a real recovery destination. No Undo is promised without an existing reversible operation.
- Existing filters hide all remaining items, if this screen has filters: “No items match these filters.” Keep the controls and provide the established clear-filter action. Do not imply the comparison itself was deleted.
- A removal request fails, if removal is remote: retain or restore the row and selected detail, preserve focus on its action, and announce that removal failed. Re-enable the action when appropriate. Do not show the empty-success message while the outcome is unknown.

**Implementation boundary:** use existing components and native button behavior; no new dependencies, brand changes or card conversion. This is a proposed outline, not an implemented accessibility result.

**Acceptance examples for later implementation:** keyboard-remove a middle unselected row; remove the selected last row while other rows remain; remove the final row and reach the real recovery action; trigger an actual supported failure. Verify visible focus, announced outcome, selected-detail consistency and no focus loss to the document body. Use the project's existing validation tools.

**Resource choices:** `pattern-carbon-data-table` supports retaining a deliberate expert density and explicit row actions, not importing Carbon sizing or components. `pattern-carbon-empty-states` supplies the cause-specific recovery distinction. `principle-native-semantics` informs choosing a native button and testing its actual behavior rather than attaching a role to a generic element. No upstream interaction was exercised.

**Remaining work:** verify the actual removal meaning and recovery destination in the owning product before implementation, then test the outlined state changes in its current UI. No additional design interview is needed for the already-settled brand, density or dependency constraints.

**References read:** `SKILL.md`; `references/flows-and-craft.md`; `library/entries/pattern-carbon-data-table.md`; `library/entries/pattern-carbon-empty-states.md`; `library/entries/principle-native-semantics.md`. Paths use the same skill root as A. No live browser, real project or upstream page inspected.
