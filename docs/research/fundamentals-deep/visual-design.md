# Visual craft, accessibility, and distinctive interface design

Research date: 2026-11-07. Status: research synthesis; no skills created or evaluated.

## Main conclusion

A useful visual-design skill should make a design appropriate, coherent, legible, adaptable, and testable. It should preserve room for a distinctive point of view. Neither an aesthetic blacklist nor compliance with a design-system token file establishes those outcomes.

This investigation separates four questions that existing skills often collapse:

1. What must remain perceivable and operable for the intended audience?
2. What visual relationships communicate hierarchy, grouping, state, and action?
3. What character fits this subject, brand, content, and setting?
4. What implementation and verification preserve these decisions under change?

These are capabilities and review lenses, not yet a proposal for four separate installed skills.

## Evidence boundary and research method

The accompanying [source ledger](visual-design.sources.jsonl) records 42 sources: 38 inspected, two partial, one inaccessible, and one discovery-only. Multiple WCAG explanations belong to one standards family; multiple Encore accounts belong to one practitioner lineage. These counts do not represent 38 independent corroborations.

Research followed three trails beyond an initial source survey: typography recommendations into actual experimental methods and limitations; design-system announcements into migrations and later retrospectives; and aesthetic skill prohibitions into conflicting instructions and the actual accessibility requirements they sometimes approximate.

Methods/results/limits were inspected selectively in the original Wallace, Reinecke/Gajos, Baughan, and Palmer/Rock publications and Peterson's critique. Official guidance was read at relevant clauses and examples. Local skill files and selected references were inspected. A live browser was used to visually inspect Stripe's original contrast-comparison figure and Carbon's density table. This was not a live product usability study, accessibility audit, or controlled skill comparison. No downloaded code or skill detector ran.

Search families included: visual complexity/prototypicality first impressions; typography size normalization and reading effectiveness; cross-cultural aesthetic preferences; perceptual grouping and critiques; display clutter/expertise; exact WCAG criteria; Hangul/RTL typography; design-system migrations and retrospectives; public design-skill instructions and licenses. Original author PDFs were preferred over summaries; inaccessible publisher routes were followed to author/institutional alternatives where available.

## What the underlying research supports

### Typography is a relationship between reader, task, glyphs, and rendering

[Legge and Bigelow](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/) distinguish visual angle, type body, and x-height. Their review and historical surveys connect reading performance to a fluent size range, with different considerations for low vision. This is not evidence for a universal CSS body-size number. See VIS-01, metrics and fluent-range sections.

[Wallace et al.](https://jdobr.es/pdf/Wallace-etal-2022-Font-Individuals.pdf), §4.4–7.3, normalize perceived size and compare preference with reading effectiveness. In the main test, 352 retained participants read five of sixteen fonts: Times, Noto Sans, their preferred font, and two randomly selected others. This was not a simple random sample of five. The 35% is the average observed fastest-versus-slowest contrast, not a deployed intervention gain. Font was nonsignificant across the overall population model. Preference did not predict speed. English/US sampling excluded reading disabilities; remote sizing/timing, differing font anatomy, and incomplete pair sampling limit transfer. See VIS-02.

Our inference: choose sensible defaults, evaluate actual text at its intended rendering, preserve overrides, and investigate personalization when prolonged reading justifies it. This research does not require a font picker in every application, prove a preferred brand font is wrong, or establish a single causal feature such as serif/sans, x-height, or weight. A hierarchy or CTA task is also different from passage-reading speed.

### Appeal, search, comprehension, and memorability are distinct outcomes

[Reinecke and Gajos](https://www.eecs.harvard.edu/~kgajos/papers/2014/reinecke14visual.pdf), methods pp.3–4 and limitations p.9, used 500ms screenshot ratings and English instructions. Their diverse sample supports variation in aesthetic preferences; self-selection, cultural filtering, and noncausal group comparisons constrain interpretation. This cannot justify prescribing a style to an individual from nationality. See VIS-03.

[Tuch et al.](https://research.google/pubs/the-role-of-visual-complexity-and-prototypicality-regarding-first-impression-of-websites-working-towards-understanding-aesthetic-judgments/) report effects after brief screenshot exposure. Only the original abstract was accessible; VIS-04 remains partial. Do not convert this into “users decide whether an entire product is usable in 17ms.”

[Baughan et al.](https://talaugust.github.io/assets/pdf/Baughan2020KeepIS.pdf), methods pp.2–4 and limitations p.8, studied rapid target finding with 165 retained participants. The recall analysis excluded “I don't know” answers, leaving answered questions from 121 participants. Lower-complexity screenshots performed better, with preference-related differences. Stimuli were different real websites, not controlled variants of one interface; other features could explain part of the effect. Forced search limits transfer to creative exploration and expert work. See VIS-05.

Our inference: distinguish unnecessary competition for attention from necessary information density. Removing information can reduce search noise, but can also remove comparison context, force navigation, or conceal essential distinctions. Evaluate a specific user operation before applying an “airy” default.

### Grouping mechanisms help explain relationships, not fixed spacing values

[Palmer and Rock](https://link.springer.com/content/pdf/10.3758/BF03200760.pdf), especially pp.29–42, demonstrate competing grouping cues and propose an organizational theory. [Peterson's commentary](https://link.springer.com/content/pdf/10.3758/BF03210956.pdf) disputes its serial interpretation. These are useful reminders that perceptual effects and explanations have different evidence status. Neither supplies a universal eight-pixel grid or requires cards. See VIS-06–07.

Our inference: inspect which elements look related before deciding whether spacing, alignment, a shared background, or a boundary should communicate that relationship. A decorative card around each sentence can imply separate objects when the content is one argument. Conversely, insufficient separation can imply that unrelated actions belong together. Ask someone to identify groups and primary actions; do not grade grouping solely by token conformity.

## Accessibility: preserve the actual requirement

The inspected normative baseline is [WCAG 2.2, Recommendation 2024-12-12](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) (VIS-08). The following Understanding documents are informative explanations. A future skill must label conformance level, scope, and exceptions separately from a preferred implementation.

| Requirement | Precise distinction worth retaining |
| --- | --- |
| [Text spacing, AA](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html), VIS-09 | Required tolerance for user overrides includes line/paragraph/letter/word spacing values. These are not obligatory authored defaults; script exceptions apply. |
| [Reflow, AA](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), VIS-10 | Vertically scrolling content must work at equivalent 320 CSS px width; horizontally scrolling content at equivalent 256 CSS px height, without two-dimensional scrolling. Meaning-dependent two-dimensional content can be excepted; surrounding controls and cells still matter. |
| [Text contrast, AA](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), VIS-11 | Normal and large text have different thresholds and scoped exceptions. Nominal color ratios do not eliminate thin-glyph rendering concerns. |
| [Non-text contrast, AA](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), VIS-12 | Required identifying/state information differs from decoration. Not every card border or change between nonadjacent states must meet 3:1. |
| [Focus Appearance, AAA](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html), VIS-13 | Minimum indicator area and state contrast differ from the basic requirement for visible focus. The two-pixel-perimeter equivalent is an area condition, not one mandatory outline style. |
| [Animation from Interactions, AAA](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html), VIS-14 | Disabling nonessential interaction-triggered motion differs from rules for automatically moving content. Essential animation is excepted. |

For semantic implementation, [APG's introduction](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) explains that ARIA roles do not implement keyboard behavior and examples require audience-relevant browser/assistive-technology checks. The [button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/) permits accessible names from text, `aria-labelledby`, or `aria-label`. See VIS-40–41. A skill should ask whether the control has the right accessible name and behavior rather than insist that one attribute or manually added keyboard handler appears everywhere.

Conformance checks, practical accessibility, visual craft, and overall usability overlap but are not interchangeable completion claims.

## Localization changes the visual problem

The [Hangul layout document](https://www.w3.org/TR/2026/DNOTE-klreq-20260321/), §4.1 and §7.1, addresses mixed-script metrics, character/word wrapping, and punctuation restrictions. It is explicitly a Group Note Draft, not a Recommendation, and contains unfinished sections (VIS-15).

[W3C RTL guidance](https://www.w3.org/International/questions/qa-html-dir) distinguishes language from base direction and recommends semantic `dir` plus logical layout properties; runtime content needs direction handling (VIS-16).

Our inference: a Latin `ch` width, aggressive negative tracking, uppercase eyebrow, centered headline, or manual line break does not transfer automatically across scripts. A localized design should be tested using real strings, mixed identifiers and numbers, fallback fonts, long labels, and actual wrapping. Preserving language shape and reading order can be more important than matching a screenshot's line count. Specialist native-reader review remains necessary for judgments this survey cannot establish.

## Seven comparative cases for teaching judgment

The cases below combine documented examples with proposed original exercises. The proposed variants and evaluation procedures have not been built or tested.

### 1. Typography migration: preserve intention as rendering changes

GOV.UK's [current scale](https://design-system.service.gov.uk/styles/type-scale/) pairs type roles with line heights; its [migration guide](https://design-system.service.gov.uk/get-started/new-type-scale/) requires retesting custom spacing and positioning. The [earlier rationale](https://designnotes.blog.gov.uk/2022/12/12/making-the-gov-uk-frontend-typography-scale-more-accessible/) explains the planned removal of tiny sizes and mobile downscaling. See VIS-17–19; this is first-party rationale, not a controlled universal-size trial.

**Exercise:** increase body size while retaining a long page title, labels, error summaries, inline help, and browser zoom. Compare a component that derives height from text with one that assumes a fixed line count. The better outcome preserves hierarchy and access to information. Do not reward a visually identical crop if content is clipped below it.

### 2. Dense expert table versus spacious browsing cards

[Carbon](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines) documents density variants, wide/condensed placement, and context-sensitive visibility of row actions (VIS-20). Its live sizing table was visually inspected. These are design-system conventions, not proof that a particular row height improves performance.

**Exercise:** give an operator forty resources with names, owners, states, and dates. Ask for comparison, batch selection, and finding an anomalous row. Compare an aligned table against spacious cards using the same information. Record errors, navigation/scrolling, and successful comparison. Repeat with touch/zoom and a novice interpretation task. Necessary density should be justified by the operation; compact controls do not get an accessibility exemption merely because users are experts.

The relevant financial-display study was located but full access failed (VIS-37). This report therefore makes no causal claim that experts are helped by clutter.

### 3. Accessible palette: preserve role and character together

[Stripe's case](https://stripe.com/blog/accessible-color-systems) describes a failed darken-one-step approach, perceptual palette tooling, and coordinated foreground/background changes. Its historical contrast-comparison figure was visually inspected in the browser (VIS-22). The account's pairing guarantees belong to that constructed palette.

**Exercise:** repair a status badge and chart legend under light/dark themes while retaining recognizable hue roles. Compare local overrides with semantic foreground/background pairs. Measure actual colors in every relevant state; check labels and non-color cues. A passing pair on white is insufficient evidence for tinted, hovered, selected, or dark surfaces. Conversely, a palette need not become gray to become readable.

### 4. Expressive specimen versus transactional interface

[Locomotive's Editorial New case](https://locomotive.ca/en/work/editorial-new) links retro expression and interactive typography to demonstrating a variable typeface (VIS-24). This is a designer's account; awards are not usability evidence.

**Exercise:** use the same typographic animation once to demonstrate a font feature and once above a payment correction form. Ask what meaning the motion communicates in each setting. Brand relevance and reader task should explain the choice. A general ban on serif display, unusual composition, or expressive motion would erase relevant design opportunities; indiscriminate novelty can make routine work harder.

### 5. Functional motion with an equivalent reduced variant

[WebKit's historical examples](https://webkit.org/blog/7551/responsive-design-for-motion/) show alternatives to scaling, parallax, spinning, and plane shifts, while distinguishing predictable direct manipulation (VIS-23). This is implementation guidance, not a current compatibility test.

**Exercise:** animate expanding a selected row so the changed relationship remains clear. Provide a reduced-motion variant preserving state and focus. Check that content does not remain hidden waiting for an entrance animation and that interrupting the transition works. Review dynamic changes to the preference when the implementation supports them. Removing all animation globally should not silently break completion callbacks or state transitions.

### 6. A design system that evolves beyond its launch story

Airbnb's [original account](https://medium.com/airbnb-design/building-a-visual-language-behind-the-scenes-of-our-airbnb-design-system-224748775e4e) describes auditing real screens, iterating foundations, and later regretting insufficient row patterns and documentation (VIS-25).

Encore's [2020 introduction](https://www.shaunbent.co.uk/blog/reimagining-design-systems-at-spotify/) explains autonomy/platform goals; its [2022 retrospective](https://www.shaunbent.co.uk/blog/encore-design-system-three-years-on/) reports limits of flexibility and nonsemantic tokens (VIS-26–27). The [cross-platform account](https://www.designsystems.com/how-spotifys-design-system-goes-beyond-platforms/) preserves platform-specific states inside a shared component language (VIS-29).

In [October 2026](https://53degrees.studio/posts/building-a-system-of-systems-what-we-didnt-know/), the former leader described mismatched promises under a shared brand. [November's follow-up](https://53degrees.studio/posts/building-a-system-of-systems-what-we-didnt-see-coming/) discusses ownership, maintenance, and promotion costs, alongside a successful denser business subsystem (VIS-42/28). These are related firsthand narratives, not independent replications or audited causal outcomes.

**Exercise:** change a brand token used as both background and text. Ask the agent to find affected roles and propose a migration. A second exercise changes a component's maintainer. Does its documentation still promise support no one provides? Reuse decisions need ownership and a change path, not only matching token names.

### 7. Same visual idea across Latin, Hangul, and RTL content

**Exercise:** design a heading, navigation, and numeric comparison in three scripts with real strings. Compare hardcoded line breaks/left offsets and one Latin font against semantic direction, logical spacing, script coverage, and content-driven dimensions. Preserve the intended grouping and prominence while allowing different wrapping. Native-reader evaluation can detect unnatural punctuation and spacing a CSS validator misses.

## Existing design skills: applicability and provenance

This is an instruction comparison, not a ranking by popularity or measured effectiveness.

| Sample | Useful capability | Boundary or conflict |
| --- | --- | --- |
| Local [ui.sh design](/Users/jaeyong/.agents/skills/design/SKILL.md), VIS-30 | Detailed Tailwind authoring and component-specific guidance. | Mandatory Inter, non-bold headings, and tracking rules are house choices. Broad eager-loading can inject unrelated guidance. Local license/provenance not established. |
| Local [ideas](/Users/jaeyong/.agents/skills/ideas/SKILL.md), VIS-31 | Implemented-option picker and cleanup lifecycle. | Explicitly excludes creating visual directions; external script is a dependency. Local license not established. |
| Local [Taster](/Users/jaeyong/Development/Github/taster/skills/taster/SKILL.md), VIS-32 | Taxonomy, token coherence, detector levels, and original-content preservation. | Font replacement, fixed approvals, and aesthetic bans are contextual. Clean detector is not design quality. Clean checkout at `d29fb63275483fda52303b6c65ecd9428e5a2a05`; root MIT license inspected. |
| [Anthropic frontend-design](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md), VIS-33 | Brief-specific visual intent and explicit exceptions to generic-pattern warnings. | Studio-style novelty and one memorable element are creative strategies, not universal requirements. Per-skill Apache-2.0 license inspected. |
| [Baseline UI](https://raw.githubusercontent.com/ibelick/ui-skills/main/skills/baseline-ui/SKILL.md), VIS-34 | Concrete cleanup prompts and code-level findings. | Prescribed stack, timing limits, tracking prohibition, and aesthetic bans exceed evidence here. Root MIT license inspected. |
| [Vercel review skill](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/web-design-guidelines/SKILL.md) and [loaded rubric](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md), VIS-35–36 | Code review spans semantics, state, dynamic content, theming, and layout. | Remote rules can change independently; Title Case conflicts with Taster's sentence case. Blanket keyboard-handler/attribute recipes need semantic interpretation. Attempted license paths failed; reuse terms unresolved. |

License observations identify inspected text and scope, not legal conclusions. Referencing ideas differs from copying instruction text, source code, images, or proprietary fonts. The remote skill versions above remain mutable `main` snapshots because commit API access failed. Local ui.sh contents were read but their origin/version was not established.

## Candidate instructions to test

These are original synthesis from the evidence, not validated skill instructions:

1. Establish audience, task, real content, brand constraints, viewing context, and existing system before selecting visual treatments. A bounded spacing fix needs only the relevant context.
2. Explain hierarchy and grouping through the content relationships they express. Remove repeated decoration when it does not encode useful distinctions; retain purposeful character.
3. Treat typography as coordinated roles, metrics, language coverage, wrapping, and user adaptation. Font novelty alone neither improves nor ruins reading.
4. Select density from comparison and manipulation needs. Test what the person must see together before introducing extra cards, pagination, disclosure, or scrolling.
5. Define color roles and verify actual pairs/states. Palette names, equal numeric steps, and detector scores do not establish contrast or perceptual equality.
6. Require accessible outcomes and cite exact criteria; keep preferred techniques and stronger targets visibly separate from minimum conformance.
7. Make motion communicate a relationship or response, preserve interruption and reduced-motion behavior, and avoid content dependence on decorative sequences.
8. Test realistic content variation, localization, zoom, keyboard/focus, target size, themes, and asynchronous states before judging the work from a screenshot.
9. Explain retained conventions and justified exceptions. Respect explicit brand/context choices rather than restyling them to satisfy a generic anti-slop identity.
10. Report what was inspected and observed. Source-code review, screenshot critique, automated accessibility checks, assistive-technology tests, and user task results establish different things.

## Evaluation set and failure criteria

Evaluate against the same briefs without the skill and against prior versions; include cases where a default should be rejected. Do not make examples hidden answer keys.

| Task | Evidence to collect | Reject the instruction if… |
| --- | --- | --- |
| Preserve an established Inter/bold brand | Brief adherence, hierarchy, source/visual inspection | It replaces fonts or weakens hierarchy merely to remove an AI tell. |
| Repair a dense operational comparison | Correct comparisons, errors, scrolling/navigation, keyboard/touch access | It creates spacious cards that make the comparison harder or hides necessary data. |
| Design a typeface specimen | Brief relevance, legibility, accessible controls, reduced variant | It applies transaction-form minimalism and removes the demonstration's purpose. |
| Update typography with long/localized strings | No clipped content, stable useful grouping, zoom/spacing overrides | It preserves screenshot proportions by hiding text or disabling adaptation. |
| Implement an icon action with existing visible label relation | Correct computed name and native behavior | It adds redundant handlers/labels that conflict with native behavior or existing naming. |
| Repair contrast across themes/states | Actual foreground/background pairs, non-color information | It passes one screenshot but fails hover/selection/dark backgrounds. |
| Review “AA compliant” claims | Correct levels, scope, exceptions and evidence | It calls AAA requirements AA or mistakes an informative technique for the only valid implementation. |

For subjective craft, use blinded side-by-side assessment with a supplied brief and a rubric for appropriateness, hierarchy, coherence, distinction, and readability. Collect disagreement instead of forcing one aesthetic score to represent every audience. Pair that assessment with actual task and accessibility checks. Neither AI-authorship detectors nor pattern absence should be the success metric.

## Access gaps, exclusions, and next research needs

- Tuch's original abstract was inspected, but Google's full PDF was inaccessible; University of Basel exposed metadata without a downloadable full text in the retrieved page. No full-method claim adopted.
- Wallace's first author-hosted PDF timed out twice; a coauthor-hosted original was inspected. The publisher and ETH financial-clutter full texts returned 403. MIT clutter pages timed out/returned 502. Discovery is recorded separately from reading.
- Apple's typography shell linked Markdown that the web tool could not consume. No HIG typography claim was adopted. GitHub commit API access failed; remote skills need immutable revision capture before maintained reuse.
- Search directories, award lists, generic redesign galleries, and secondary summaries were used for discovery only. A source's popularity, brand prestige, or claim of success is not efficacy evidence.
- Strong coverage: Latin typography, web conformance, public-service/enterprise systems, selected consumer-system histories. Weaker coverage: Arabic shaping, Japanese/Thai/Khmer reading, low-vision/dyslexia-specific trials, game UI, visual arts/editorial craft beyond the specimen case, and prolonged expert operations.
- An especially valuable next step is matched-content density testing and cross-script type testing. This would answer where generic visual rules actually improve or damage the user's work. No behavioral claims about the proposed skill are justified before those trials.

## Provisional packaging

Keep a compact visual-direction workflow with references for typography, composition/grouping, color, motion, localization, and contextual case studies. Interface verification should be available independently when the request is an audit. Flow/content design remains tightly connected but need not load the entire visual research collection. Stack-specific recipes and house styles should be optional profiles, not fundamentals. Split or merge capabilities when real requests and traces reveal which guidance belongs together.
