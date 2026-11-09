# Foundations curation notes

Date: 2026-11-07. Scope: selection-ready design foundations, original research, accessibility and internationalization guidance. Operational cards live inside the installable package; this file is an editorial receipt, not a runtime dependency.

## Delivered collection

Created 22 `foundation` cards under `skills/design-with-intent/library/entries/`, using the reserved `principle-*` and `standard-*` filenames. They contain approximately 4,643 words of original body annotation, 42 source links and 40 distinct URLs. URL count is not an independent-study count: standards explanations, related papers, publisher records and author copies can share an evidential origin.

| Selection job | Cards | Why these are distinct resources |
| --- | --- | --- |
| Human direction and iteration | `principle-mixed-initiative`, `principle-contextual-elicitation`, `principle-comparative-critique`, `principle-preference-critiquing`, `principle-grounding-feedback` | Decide whether to ask; uncover the work; compare alternatives; revise a search profile; preserve shared direction after critique. |
| Choice, navigation and evidence | `principle-choice-context`, `principle-navigation-learning`, `principle-usability-sampling`, `principle-goals-signals-metrics` | Distinguish decision burden, retrieval/learning, formative discovery and outcome measurement. |
| Visual reasoning and reading | `principle-reading-typography`, `principle-appeal-task-distinction`, `principle-perceptual-grouping` | Separate font preference/metrics/performance; appeal/task outcomes; content relationships/perception theory. These are not visual-reference cards. |
| Automation, access and agency | `principle-human-ai-control`, `principle-contextual-permissions`, `principle-informed-choice` | Expectation/correction, permission timing/denial, and choice architecture have different failure modes and sources. |
| Diverse audiences and scripts | `principle-low-literacy-modalities`, `principle-global-name-fields`, `principle-multilingual-layout` | Local task evidence, culturally valid data collection, and script/direction layout must be considered separately. |
| Accessibility interpretation | `standard-wcag-conformance`, `standard-text-adaptation`, `standard-focus-motion`, `principle-native-semantics` | Define the claim, preserve text adaptation, interpret focus/motion levels, and implement the semantics promised by controls. Related criteria are bundled by design decision rather than padded into one card per clause. |

Each card provides when to use, precise material to inspect, a transferable mechanism with an application example, and mismatches/limits. Related IDs connect complementary or competing reasoning within this lane. The parent curator can add cross-lane patterns and examples without duplicating these foundations.

## Evidence and source handling

This lane used the existing same-day research as a deliberately explicit seed: UX-06–18 and UX-25–27, VIS-01–16 and VIS-40–41, QUE-01–14, and the independent visual review. It did not treat those ledger rows as finished catalog entries. Papers were grouped around decisions, their methods and limitations were retained, and the annotation explains how an agent might use the resource.

Primary source refreshes included the original Horvitz, Nuseibeh/Easterbrook, Tohidi, Dow, Viappiani, Scheibehenne, Faulkner, Larson/Czerwinski, Amershi, Reinecke/Gajos, Baughan, Palmer/Rock, Peterson, Medhi, Wijesekera, Mathur and Clark/Brennan materials; Google Research's HEART publication entry and linked author version; Android permission guidance; the versioned WCAG 2.2 Recommendation; relevant W3C Understanding documents; ARIA APG; and W3C names, RTL and Hangul guidance.

“Refreshed” is not a claim to re-read every page or rerun an experiment. Relevant methods/results/qualifications from the same-day original research and independent reviews remain explicitly identified in card scope. Current primary retrieval checked source identity and availability where successful. No experiment, source code, UI prototype or browser/assistive-technology test was executed in this curation lane.

No card claims `visual-inspected` or `interaction-tested`, and all character facets are empty. Perception research can support a reasoning question without being a screenshot match. Product appearance and live flow claims belong to appropriately inspected examples elsewhere in the library.

## Search and access trail

The investigation followed original sources from three prior query families rather than repeating generic best-practice searches:

- mixed initiative → elicitation → prototype critique → example-based preferences → communication grounding;
- choice overload and conflicting meta-analysis → hierarchy/menu learning → formative sampling → user-centered metrics;
- typography/perception and critiques → novice/low-literacy mobile methods → contextual permissions/agency → normative and explanatory accessibility → internationalization.

Source aliases were used to identify the same work, not counted as additional corroboration. The HEART author paper is a third-party-hosted copy directly linked by its official Google Research publication entry. The font study's coauthor-hosted copy and the jdobr.es copy represent the same TOCHI work. The expanded Medhi journal study is distinguished from its earlier conference manuscript.

Current access gaps are visible:

- The Canterbury menu-model endpoint timed out. The navigation card has `availability: partial` and retains the precise prior inspected methods/version, not a fresh claim about exact model constants.
- Both typography-paper PDF endpoints timed out and the Legge/Bigelow PMC route returned a browser challenge. The typography card is partial-access and requires reopening originals before quoting exact results. This is a benign fetch/access failure, not a browser-policy bypass opportunity.
- The 2015 choice meta-analysis and correction are retained from the same-day detailed source review; their original publisher links and locators remain in the card. They do not become independent replications merely because they have separate URLs.

No CUA browser was used, no blocked browser outcome was retried through another surface, and no remote assets or full source texts were downloaded into the package.

## Important distinctions preserved

The cards avoid universal menu counts, participant counts, typefaces, body sizes or motion recipes. They distinguish observed font extremes from deployable personalization gains; screenshot appeal from interactive usability; assisted completion from unassisted success; access logs from user judgments; guideline relevance from causal user benefit; and a choice taxonomy from intent, persuasion effect or legal classification.

WCAG conformance scope remains distinct from design-system conventions and overall usability. Text-spacing values are tolerance tests rather than required authored defaults. Reflow has orientation-specific dimensions and essential two-dimensional exceptions. Focus Visible is AA; Focus Appearance and Animation from Interactions are AAA. The Hangul publication is a Group Note Draft, not a Recommendation. APG roles do not implement keyboard behavior or certify compatibility.

Questioning methods remain conditional. Explicit creative delegation can be honored, and people need not invent finished art direction. Alternatives can expose criticism without guaranteeing substantial new suggestions. Preference models can change, and a partial answer should not restart an entire interview.

## Validation and remaining coverage

Local checks parsed all 22 JSON frontmatters, verified required fields/sections, unique filename-matching IDs, inspection dates, empty unclaimed-character facets and existing related IDs. There are no mandatory links to the repository research directory or hardcoded personal paths. Global generated views and cross-lane validation are owned by the package-tooling/coordinator lanes.

The collection is strongest in web/HCI reasoning and selected historical research. Remaining depth opportunities include original pointing/steering models, accessible game interaction, contemporary native-device studies, longitudinal design outcomes, disability-led research beyond guideline interpretation, and more non-English empirical work. These gaps should shape future curation; they do not justify replacing the current limits with universal laws.
