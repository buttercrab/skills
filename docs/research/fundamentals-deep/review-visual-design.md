# Independent source review: visual-design dossier

Review date: 2026-11-07. Reviewer: UX/product-flow research lane. Reviewed artifacts: visual-design.md and visual-design.sources.jsonl. Scope: six targeted claim groups, including reopening underlying papers and official guidance. No visual-design files changed; no UI experiment or accessibility conformance audit performed.

## Result

**No material contradiction found in the checked claims.** The dossier consistently distinguishes empirical observations, design-system conventions, contextual taste, and proposed evaluation. It correctly avoids claiming that screenshot appeal proves usability, that observed fastest-font differences are deployed gains, or that AAA criteria are required for AA conformance.

Three small precision improvements were sent to the visual author:

1. Spell out both reflow orientations rather than stating only 320 CSS px.
2. Clarify that Wallace's five-font assignment included fixed baselines and preference-dependent selection, rather than implying a random sample.
3. Distinguish Baughan's retained search sample from the smaller recall-analysis sample.

These do not require a change to the main conclusion. The notes below refer to the reviewed snapshot; the author may subsequently incorporate them.

## 1. WCAG text adaptation and reflow

**Checked location:** visual-design.md, accessibility table, reviewed lines 60–61; VIS-08–10.

**Sources reopened:** [normative WCAG 2.2 2024-12-12](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), SC 1.4.10 and 1.4.12; [Understanding Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html), Success Criterion, Note 1, Author Responsibility; [Understanding Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), Success Criterion and Intent.

**Supported:** text-spacing values describe tolerance of user overrides, not compulsory authored defaults. The script/property exception is explicit. Reflow permits meaning-dependent two-dimensional content, while text in individual table cells still needs consideration.

**Precision note:** replace the shorthand “equivalent 320 CSS px” with “vertical-scrolling content at width equivalent to 320 CSS px; horizontal-scrolling content at height equivalent to 256 CSS px.” The report's intended common horizontal-writing case is sound, but its later cross-script discussion makes orientation worth naming.

**No stronger inference:** neither criterion establishes the best authored body size, line length, spacing scale, or card/table conversion.

## 2. WCAG focus, motion, and non-text contrast

**Checked location:** accessibility table, reviewed lines 63–65; VIS-12–14.

**Sources reopened:** normative SC 2.4.13 and 2.3.3; [Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html), Success Criterion, Minimum area, Exceptions; [Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html), Success Criterion and Intent; [Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), state/focus/hover discussion.

**Supported:** Focus Appearance and Animation from Interactions are AAA. Focus area can equal a two-CSS-pixel perimeter without using that exact outline implementation. Motion triggered by interaction differs from automatic motion, and essential movement is scoped separately. Non-text contrast compares required information with adjacent colors; it is not a blanket comparison between every control's focused and unfocused fill.

**Boundary to preserve:** a system may voluntarily target stronger behavior while claiming AA, but must not describe AAA-only requirements as AA obligations. Likewise, exceptions from a specific criterion do not establish overall accessibility. The dossier already makes this distinction.

## 3. Wallace font study: within-reader contrast, selection, and transfer

**Checked location:** typography paragraph, reviewed line 34; VIS-02.

**Underlying paper reopened:** [Wallace et al., coauthor-hosted original](https://jeffhuang.com/papers/Readability_TOCHI22.pdf), §5.1.2, Figure 9, §6.1.1–6.1.2, §6.2.1/6.2.4–6.2.5, §7.3. The dossier's jdobr.es copy loaded initially but follow-up section retrievals timed out; this is the same paper via an alternate coauthor.

**Supported:** 352 retained participants; five reading-effectiveness fonts per reader; the reported average 35% compares each reader's observed fastest and slowest tested fonts. Font was nonsignificant in the population model. Preference did not identify fastest fonts reliably. Sampling excluded reported learning/reading disabilities.

**Precision note:** identify the fixed Noto Sans/Times baselines plus preference-dependent/random selections. Font-to-passage assignment was randomized, but the five fonts were not simply a random sample of sixteen.

**Methodological inference:** selecting observed extremes can include measurement variation. The report is right to avoid promising the same gain from a prospective font-selection intervention; it should retain that caution. Passage reading is also not a direct test of CTA hierarchy or interface target-finding.

## 4. First impressions versus task performance

**Checked locations:** visual-appeal section, reviewed lines 40–44; VIS-03–05.

**Sources reopened:** [Reinecke/Gajos](https://www.eecs.harvard.edu/~kgajos/papers/2014/reinecke14visual.pdf), Method, Procedure, Data Preparation; [Baughan et al.](https://talaugust.github.io/assets/pdf/Baughan2020KeepIS.pdf), Statistical Analysis, Results, Limitations and Future Work. Tuch's inaccessible full text was not independently reconstructed.

**Supported:** Reinecke used 500ms screenshot ratings and English instructions. The dossier appropriately treats those as appeal measures, not interactive usability tests or a nationality-based prescription. Baughan explicitly limits its speed-oriented task and acknowledges that different real websites differed in features besides complexity.

**Precision note:** Baughan's 165 is the retained main sample. The recall analysis removed “I don't know” answers, leaving 738 answers from 121 participants. State that distinction if attaching one sample size to both results.

**No stronger inference:** neither result establishes the optimal density of a trained operator's working interface, creative exploration, or a specific redesign with matched content.

## 5. Density and typography as design-system conventions

**Checked locations:** dense-table case, reviewed lines 91–95; system comparison and VIS-20–21.

**Sources reopened:** [Carbon data-table guidelines](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines), Overview/When not to use/Sizing; [Atlassian typography](https://atlassian.design/foundations/typography), Brand fonts, App fonts, Heading token table.

**Supported:** Carbon documents five row sizes with different intended uses and explicitly excludes replacing a spreadsheet application. Atlassian separates brand/product font roles and uses bold heading tokens. These establish documented system policies, not causal superiority.

**Assessment:** the dossier correctly labels its table-versus-card exercise as proposed, not demonstrated. Its refusal to derive “experts benefit from clutter” from an inaccessible paper is appropriate. A compact expert table still needs usable controls and text adaptation; familiarity is not an automatic standards exemption.

No correction requested.

## 6. Existing skill rules and version attribution

**Checked locations:** existing-skills comparison, reviewed lines 135–142; VIS-30–36.

**Local checks:** ui.sh typography lines 8,11,17 explicitly prescribe non-bold headings, negative tracking, and InterVariable. Taster brand reference lines 21–24 describes replacing certain common faces with IBM Plex and restoring genuine brand choices. Its current local HEAD is d29fb63275483fda52303b6c65ecd9428e5a2a05, with no short-status output. This confirms the dossier's local snapshot claim.

**Public sources reopened:** [Anthropic frontend-design](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md), Process and Restraint; [Baseline UI](https://raw.githubusercontent.com/ibelick/ui-skills/main/skills/baseline-ui/SKILL.md), Stack, Components, Animation, Typography, Design; [Vercel loaded rubric](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md), Accessibility and Content & Copy.

**Supported:** Anthropic's inspected version explicitly permits brief-appropriate uses of listed generic traits; older blanket-ban summaries would misattribute this version. Baseline UI prescribes stack/motion/tracking choices. Vercel's loaded rubric requires Title Case and explicit keyboard handlers, supporting the report's warning about copying attribute/handler recipes literally.

**Version limit:** raw main URLs are mutable; the dossier labels them as access-date snapshots rather than immutable releases. This is adequate for a bounded research comparison, but maintained copied examples should capture an immutable revision or exact content hash. I did not independently re-review all license texts, so the dossier's license observations are outside this six-check assessment.

## Remaining review limits

This is a source-level spot review, not endorsement of every unexamined source, a global literature review, or proof that the proposed instructions improve output. I did not repeat the visual author's browser inspection of figures, inspect all accessibility criteria, run any detector, or test with assistive technology. The three precision notes improve traceability and transfer boundaries; none supports rejecting the report's main findings.

