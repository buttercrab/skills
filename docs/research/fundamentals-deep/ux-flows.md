# UX, product flows, and interaction judgment: deep research

Research date: 2026-11-07. Scope: foundations for an evolving skill library; no skills created or changed. Owner of this report and its source ledger: UX research lane. Adjacent visual craft and numerical accessibility standards belong to another research lane.

## Main conclusion

The reusable foundation is **choosing and verifying an interaction for a particular task, population, and consequence**. Good flow design cannot be reduced to fewer screens, fewer options, hidden complexity, a checklist of fashionable patterns, or a fixed number of research participants.

This conclusion is synthesis, not a result measured by one study. The sources support different parts of it, with unequal evidence strength. The clearest discoveries are conditional: an unfamiliar, occasional transaction and a repeatedly used professional tool often need different structures; a control that looks simpler can make state harder to inspect; completion, speed, accuracy, autonomy, and informed choice can disagree.

The initial design categories should remain provisional. A likely split is experience framing and flow design, interaction architecture, and evaluation. Visual direction is related but has different evidence and output. Content is part of the interaction model rather than a finishing stage. Research methods can begin as shared references and become an independent skill if actual tasks justify the split.

## Evidence boundary and reading method

The accompanying [source ledger](ux-flows.sources.jsonl) has 33 records: 29 marked inspected, one partial, two inaccessible, and one discovery-only. “Inspected” means the relevant underlying sections were opened; it does not mean every page of every long paper was read. The 29 include a correction and several sources from the same institution or product; they are not 29 independent replications.

The deeper method/result readings include Faulkner's original timesheet experiment and resampling; the methods and disagreements of two choice-overload meta-analyses; Larson/Czerwinski's information hierarchy experiment; menu-model calibration; Medhi's exploratory desktop and later mobile comparisons; Android permission field-study sampling and exit interviews; Duolingo's participant selection and historical-test caveats; and the scope of the Human-AI guidelines validation. Practitioner product cases are retained as documented reasoning, not upgraded to controlled experiments.

No live application was installed, executed, or usability-tested. Public product descriptions are historical observations. No private account material was accessed. Local Taster and ui.sh files were inspected in the earlier discovery pass, but are not counted as empirical internet sources here.

Evidence labels used:

- **Empirical:** measured outcomes with a described method; population, task, apparatus, sampling, and analysis limit transfer.
- **Documented practice:** an organization recommends or implements something; establishes practice and reasoning, not universal superiority.
- **Framework:** a useful way to formulate or inspect a problem; its usefulness still needs task-level validation.
- **First-party case:** a product team's account of decisions and results; internal data may be undisclosed.
- **Synthesis / candidate instruction:** our proposed generalization to be forward-tested. It is not automatically a demonstrated best practice.

### Search and citation trails

Searches deliberately moved beyond “good UX” and current design-skill catalogs:

| Search family | Representative terms | Followed trail / boundary |
|---|---|---|
| Service scope and flows | “whole problem user journeys”; “experience mapping”; “question protocol”; “one thing per page” | GOV.UK standard → form structure → actual pattern/code → exceptions and correction routes. |
| Research sample folklore | “Faulkner beyond five-user assumption”; Nielsen five users | Publisher abstract → full five-page publisher PDF → method, Tables 1–2, discussion → original recommendation's iteration/group qualifications. Earlier mirror timed out. |
| Choice and information architecture | “choice overload meta analysis”; “Hick menu familiar”; “breadth depth scent” | 2010 author PDF → 2015 author-uploaded paper → published corrigendum; original menu and hierarchy studies. Hick original full PDF unavailable. |
| Consumer learning | “Duolingo path redesign science”; “proficiency path whitepaper” | Launch rationale → first-party efficacy report → content differences, participant selection, historical tests. |
| Professional tools | “Figma UI3 redesign feedback toolbar” | Initial first-party rationale → post-beta reversal account. Public complaints used as discovery leads, not empirical proof. |
| Commerce | “checkout fields versus steps”; “Shopify one page three page conversion” | Baymard public research summary → examples; Shopify selected customer claims. Premium data and randomization details not inspected. |
| Context and modality | “Android permissions contextual integrity”; “low-literacy interfaces”; “names worldwide” | Current platform workflow → original field-study method; original ICTD/ToCHI papers → task/modalities/assistance limits; W3C internationalization examples. |
| Measurement and agency | “HEART goals signals metrics”; “Human-AI guidelines”; “dark patterns at scale” | Official publication routes → original papers; measurement goals, guideline evaluation scope, crawl coverage and limitations. |

Excluded from the claim-bearing set: unattributed “laws of UX” summaries, AI-style word/pattern blacklists, unsolicited Reddit verdicts, promotional conversion statistics without necessary method, duplicated mirrors as independent evidence, and screenshots as proof of a working flow.

## Evidence map

IDs resolve to full URLs, access notes, claims, contexts, and limits in the ledger. Locators below are durable section/page names rather than tool-generated result IDs.

| ID | Underlying source | Relevant reading |
|---|---|---|
| UX-01 | [GOV.UK whole-problem standard](https://www.gov.uk/service-manual/service-standard/point-2-solve-a-whole-problem) | Why it matters; scope and incremental delivery. |
| UX-02 | [GOV.UK structuring forms](https://www.gov.uk/service-manual/design/form-structure) | Question protocol; segmentation and expert-work exception. |
| UX-03 | [Question pages](https://design-system.service.gov.uk/patterns/question-pages/) | Related-question grouping and passport code example. |
| UX-04 | [Check answers](https://design-system.service.gov.uk/patterns/check-answers/) | Placement; correction, prepopulation, accessible link targets. |
| UX-05 | [Carbon empty states](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states) | Causes, actions, space constraints, optional illustration. |
| UX-06 | [Faulkner 2003](https://link.springer.com/content/pdf/10.3758/BF03195514.pdf) | pp.379–382, method, results, Tables 1–2, interpretation. |
| UX-07 | [Nielsen's original five-user advice](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/) | Iterative Design; When To Test More Users. |
| UX-08 | [Scheibehenne et al. 2010](https://scheibehenne.de/ScheibehenneGreifenederTodd2010.pdf) | pp.412–414 and 417–419: selection, analysis, heterogeneous outcomes. |
| UX-09 | [Chernev et al. 2015](https://myscp.onlinelibrary.wiley.com/doi/abs/10.1016/j.jcps.2014.08.002) | Full paper through author upload; pp.339–340,344–348,352–353; Appendix B. |
| UX-10 | [Chernev corrigendum](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2015.07.001) | Corrected coefficient/test-statistic notation for p.348. |
| UX-11 | [Larson and Czerwinski 1998](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/chi98_webdesign.pdf) | pp.27–30, methods/results and scent/depth interpretation. |
| UX-12 | [Cockburn et al. 2007](https://www.csse.canterbury.ac.nz/andrew.cockburn/papers/paper191-cockburn.pdf) | Model; pp.630–632 calibration and menu design definitions; alternate mirror in ledger. |
| UX-13 | [Miller 1956, university transcription](https://psychclassics.yorku.ca/Miller/) | Absolute judgment, immediate memory, chunks, recoding. |
| UX-14 | [Android runtime permissions](https://developer.android.com/training/permissions/requesting) | Basic principles and request/denial workflow. |
| UX-15 | [Wijesekera et al. 2015](https://arxiv.org/pdf/1504.03747) | §3 method and §5 expectations/blocking; arXiv v1. |
| UX-16 | [W3C personal names](https://www.w3.org/International/questions/qa-personal-names) | Scenarios, examples, field design and character support. |
| UX-17 | [Medhi et al. ICTD manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/medhi_ictd2006.pdf) | Context, iterative design, small exploratory tests and qualitative limits. |
| UX-18 | [Medhi et al. ToCHI 2011](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ToCHI2711_Medhi.pdf) | Table I; §4 banking, §5 health entry, §6 interpretation. |
| UX-19 | [Duolingo path explanation](https://blog.duolingo.com/new-duolingo-home-screen-design/) | Change description, review routes, progress, labels, long scrolling. |
| UX-20 | [Duolingo efficacy report](https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_language_read_listen_write_speak_2024.pdf) | §1.1 bundled changes, §2.1 selection, §3.1.1/§4.1 comparison caveats. |
| UX-21 | [Figma initial UI3 rationale](https://www.figma.com/blog/behind-our-redesign-ui3/) | Properties, layout, ergonomics and optional labels. |
| UX-22 | [Figma post-beta corrections](https://www.figma.com/blog/our-approach-to-designing-ui3/) | Docked panels; blend-mode state; clip-content control. |
| UX-23 | [Baymard checkout effort](https://baymard.com/research-articles/checkout-flow-average-form-fields) | Field burden versus steps, examples and recovery. |
| UX-24 | [Shopify one-page checkout](https://www.shopify.com/enterprise/blog/one-page-checkout) | Configuration, selected customer claims, B2B, measurement and caveats. |
| UX-25 | [HEART original publication](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/) | Official Download leads to author-version PDF; PULSE, HEART, Goals–Signals–Metrics. |
| UX-26 | [Human-AI guidelines](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf) | Table 1; validation process; §7 limitations. |
| UX-27 | [Mathur et al. 2019 v2](https://arxiv.org/html/1907.07032v2) | §3–5 taxonomy, method/examples; §6.4 limitations. |
| UX-28 | [Experience mapping](https://www.gov.uk/service-manual/user-research/creating-an-experience-map) | When useful; user evidence; different stages and separate maps. |
| UX-29 | [Service landscape and user journey](https://www.gov.uk/service-manual/design/map-a-users-whole-problem) | Organizational scope, backstage versus user view, actionable changes. |

## Decision cases and counterexamples

These cases combine source observations with proposed reasoning and verification. Proposed tests have not been performed. The objective is to preserve the conditions that made a choice sensible, rather than making the observed answer compulsory.

### Case 1: Break a form into screens, or let users work in one view?

**Competing designs:** a sequence of focused questions, a grouped task form, or one-page checkout.

GOV.UK recommends beginning with one thing per page, while explicitly allowing grouping for repeated expert work; its passport pattern groups related questions. Its question protocol starts with the information's purpose rather than its visual placement. [UX-02](https://www.gov.uk/service-manual/design/form-structure), [UX-03](https://design-system.service.gov.uk/patterns/question-pages/).

Baymard's public research summary emphasizes what people must consider and enter over raw step count, including irrelevant membership fields and recovery burden. The complete premium evidence was unavailable. Shopify promotes one-page checkout and reports selected merchant gains, but describes both layouts and bundles autofill, wallets, shipping visibility, and other changes. It does not establish that changing page count alone caused a general conversion lift. [UX-23](https://baymard.com/research-articles/checkout-flow-average-form-fields), [UX-24](https://www.shopify.com/enterprise/blog/one-page-checkout).

**Synthesis:** task segmentation should follow uncertainty, dependencies, frequency, interruption, and consequences. A page boundary can focus an unfamiliar decision or add pointless overhead to repeated entry. Screen count and click count are incomplete proxies for effort.

**Candidate instruction:** before choosing a wizard, identify which inputs are necessary, conditional, prefillable, difficult, sensitive, or usually corrected together. Compare complete task variants with the same required information. Do not automatically turn a public-service form into one-page commerce checkout, or copy a checkout pattern into an expert scheduling tool.

**Verification:** observe completion and recovery, typing, irrelevant decisions, backtracking, and preserved answers. Test keyboard/mobile use and interrupted return. For production comparisons, segment new/returning users and device; include error and cancellation outcomes. Do not infer causal success from before/after conversion without controlling concurrent changes.

### Case 2: Simplify a professional interface by hiding controls?

**Competing designs:** icon-only control, labeled stateful control, nested menu, and direct checkbox.

Figma's initial UI3 account describes preserving familiar geometry and optional labels for professional users. Its October follow-up acknowledges reversals: floating panels harmed work on small screens; blend-mode icons concealed the current value until a tooltip; clip content in a dropdown introduced an extra click, so a checkbox returned. This is an unusually useful public failure-and-correction record, though effect sizes and test protocols are undisclosed. [UX-21](https://www.figma.com/blog/behind-our-redesign-ui3/), [UX-22](https://www.figma.com/blog/our-approach-to-designing-ui3/).

**Synthesis:** visual quietness and task simplicity are different. A compact control can impose repeated inspection, navigation, and state-reconstruction costs. An expert workflow may benefit from more persistent information, even if a marketing screenshot becomes denser.

**Candidate instruction:** distinguish “users rarely need this action” from “users frequently need to see this state.” Hide an action only after considering the inspection cost. Preserve meaningful learned locations where change adds little user value. Offer contextual labels or shortcuts without requiring every user to become an expert.

**Verification:** measure repeated inspection and adjustment, not just whether a first-time participant can discover an icon. Include small displays, split screens, nondefault values, bulk edits, and switching between modes. A single successful click is insufficient evidence.

**Counterexample:** persistent controls also consume scarce space and may overwhelm unfamiliar users. The useful rule is to compare task cost and state visibility, not “never use icons” or “never use progressive disclosure.”

### Case 3: Guide the next action, or preserve exploration and learner choice?

**Competing designs:** a branching library/tree, a recommended next step, and a mandatory linear path.

Duolingo's 2022 explanation describes arranging lessons, practice, and stories into a guided path, with ways to revisit completed lessons and return to the current position. The 2024 report measures 257 selected adult Spanish/French course completers. Historical outcomes use different tests; content, mandatory practice, and sequence also changed. The report itself characterizes better-teaching comparisons as tentative. [UX-19](https://blog.duolingo.com/new-duolingo-home-screen-design/), [UX-20](https://duolingo-papers.s3.amazonaws.com/reports/Duolingo_whitepaper_language_read_listen_write_speak_2024.pdf).

**Synthesis:** this case supports explicitly designing guidance, review, navigation, and progress migration. It does not establish that all learning tools should force a linear path, or that layout produced the measured proficiency differences.

**Candidate instruction:** identify whether the uncertainty is “what should I do next?”, “where is the thing I already know I need?”, or “what can I explore?”. A next-action recommendation may solve the first without removing retrieval or review routes needed by the others. If the sequence is mandatory, explain its basis and preserve justified return/skip mechanisms.

**Verification:** test novice progression, knowledgeable users finding a specific item, review after a long gap, existing progress migration, and course completion. Track domain outcomes alongside return rate and usage. A design can increase sessions because practice improved or because navigation became harder; logs alone do not identify which.

### Case 4: Reduce choices to satisfy a cognitive law?

**Competing designs:** fewer top-level categories with more levels, a broad menu, stable locations, or adaptive ordering.

Miller's review distinguishes immediate-memory chunks from absolute judgment. It does not specify a universal menu length. Larson/Czerwinski's 19-user experiment used 512 encyclopedia leaves: deeper structure performed worse, while the broadest and moderate conditions were not significantly different in search time. Materials and categories constrained interpretation. [UX-13](https://psychclassics.yorku.ca/Miller/), [UX-11](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/chi98_webdesign.pdf).

Cockburn's model combines pointing, search, and learning; calibration used eight right-handed graduate computer-science students. Familiar stable menus differed from randomized ones. This warrants treating user knowledge and location stability as variables, not exporting its constants to arbitrary screens. [UX-12](https://www.csse.canterbury.ac.nz/andrew.cockburn/papers/paper191-cockburn.pdf).

**Synthesis:** navigation is a retrieval problem involving labels, categories, distribution, familiarity, and motor/visual cost. Counting visible items loses most of that information.

**Candidate instruction:** compare structures with realistic target-finding tasks and labels. Separate first-use discovery from repeated retrieval. Do not add hierarchy merely to fit seven items or move controls merely because a frequency model predicts they will be popular.

**Verification:** include ambiguous categories, exact known-item retrieval, browsing, switching targets, repeated use, wrong turns, and escape paths. Inspect first choice and eventual success. Compare with search when the content/task warrants it.

**Further caution:** the experiment's paper task reference reduced memory demands. Different task cues could yield different findings; realistic external references are part of the interaction environment, not noise to erase automatically.

### Case 5: “Less choice is better” versus “choice overload is a myth”

The 2010 meta-analysis pooled 63 conditions from 50 published/unpublished experiments (N=5,036), finding a near-zero mean and heterogeneous effects. Some approximate nonsignificant results were coded zero. The 2015 analysis used 99 observations in 53 published studies (N=7,202), modeled contextual moderators and nested observations, and reached different conditional conclusions. A corrigendum corrects statistic notation. [UX-08](https://scheibehenne.de/ScheibehenneGreifenederTodd2010.pdf), [UX-09](https://myscp.onlinelibrary.wiley.com/doi/abs/10.1016/j.jcps.2014.08.002), [UX-10](https://myscp.onlinelibrary.wiley.com/doi/10.1016/j.jcps.2015.07.001).

**Synthesis:** the literature does not support a universal option cap or a blanket dismissal of overload. Neither study directly establishes how many SaaS pricing plans a particular audience needs. Selection criteria, outcome definitions, and modeling choices matter.

**Candidate instruction:** diagnose preference uncertainty, comparison difficulty, attribute alignment, and decision goal. Consider comparison aids, filters, recommendations, grouping, or delayed decisions before removing meaningful options. A specialist seeking an exact configuration may value breadth that a beginner cannot evaluate.

**Verification:** compare correct fit, comprehension, deferral, regret, and ability to find an uncommon option. Conversion alone may reward hiding alternatives or costs; “more purchases” is not by itself informed-choice quality.

### Case 6: Can a five-person usability test certify a flow?

Faulkner tested one timesheet task with 60 users in three experience groups, then drew 100 resamples per size against 45 known problems. Five-user samples ranged widely, with 55% as the observed minimum; this is not a bound on undiscovered problems or future products. Nielsen's original recommendation prioritizes iterative rounds and separately treats distinct populations. [UX-06](https://link.springer.com/content/pdf/10.3758/BF03195514.pdf), [UX-07](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/).

**Synthesis:** research for quickly discovering repairable obstacles and research for estimating failure rates or supporting consequential release claims are different assignments. Five sessions can be useful without certifying coverage.

**Candidate instruction:** state the decision the research must support, recruit the relevant users, and name the limitations before choosing sample size. Preserve iteration when it can resolve immediate obstacles. Increase coverage when roles, abilities, contexts, or consequences differ; use complementary methods for issues ordinary sessions may miss.

**Verification:** the research report should distinguish observed problems, inferred causes, proposed changes, and retested outcomes. Do not report “85% of issues found” without evidence about the unknown population of problems. No participant count guarantees that a multi-actor permission, recovery, or migration path was exercised.

### Case 7: Ask for permission at onboarding, or at the action?

Android's official guidance requests permission in task context, permits cancellation, and describes denial/revocation handling. Its workflow first asks whether permission can be avoided. The 2015 instrumented field study followed 36 people for a week; its exit survey asked about sampled accesses, finding preferences connected to relevance and expectations. It measured retrospective preferences, not a randomized consent-interface improvement. [UX-14](https://developer.android.com/training/permissions/requesting), [UX-15](https://arxiv.org/pdf/1504.03747).

**Synthesis:** a permission is a continuing capability/state relationship, not a one-time onboarding checkbox. Good flow design includes refusal, limited access, return from settings, revocation, and changes in purpose.

**Candidate instruction:** connect the request to a user-understandable capability. Offer the least access that accomplishes the task where the platform supports it. Preserve useful independent functions after denial. Do not use repeated instructional prompts to pressure a different answer.

**Verification:** exercise granted, denied, revoked, partial/scoped access, unavailable device capability, and return flows. Check that the interface accurately explains the purpose and current state, and that permission is rechecked when needed. Platform behavior must be verified against current OS documentation, not copied from 2015.

### Case 8: Make the interface “obvious” with familiar icons or voice?

Medhi's early ethnographic/prototype work emphasizes local interpretation, audio, and consistent help; its small quantitative tests were explicitly exploratory. The later mobile study compared 58 first-time banking users: graphical completion was 20/20 and voice 13/18 with experimenter prompting permitted; graphical completers received more prompts on average. Successful voice users were faster, but speech was Wizard-of-Oz and assistance/experience affected results. A separate 13-person health-entry comparison evaluated accuracy, not navigation completion. [UX-17](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/medhi_ictd2006.pdf), [UX-18](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ToCHI2711_Medhi.pdf).

**Synthesis:** a symbol understood by its designer can be meaningless or literal to another population. Translation cannot compensate for an unfamiliar service concept. Speed among completers can conceal exclusion.

**Candidate instruction:** distinguish language, literacy, domain knowledge, interaction experience, sensory/motor needs, and trust in the technology. Validate the actual vocabulary and symbols with intended users. Consider assistance and alternate channels when they solve the task better than another digital screen.

**Verification:** report completion and accuracy alongside speed, help received, and who gave up. State when a prototype uses simulated intelligence or a human operator; do not infer production speech-recognition quality from it. First-use evidence does not predict long-term expert performance.

### Case 9: Collect names “cleanly,” or represent people accurately?

W3C describes variation in name components, order, script, punctuation, mononyms, and preferred address. A full-name field may suit some uses; separate components can be necessary for a specific purpose but cannot assume a universal first/last order. Localized presentation does not remove data-model complexity. [UX-16](https://www.w3.org/International/questions/qa-personal-names).

**Synthesis:** UX and schema design share an ownership boundary. An interface cannot repair a backend that cannot store a legitimate value; validation can manufacture garbage data instead of quality.

**Candidate instruction:** identify why each component is needed and preserve the user's supplied name. Make downstream distinctions explicit rather than silently parsing, title-casing, or assuming a family name. When a legal or delivery process imposes a specific format, explain and model that actual requirement rather than generalizing it.

**Verification:** use concrete diverse fixtures across collection, storage, display, search, and export. Include mononyms, apostrophes, spaces, multi-part names, non-Latin scripts, long values, and differing display order. A form that accepts a value but mangles the confirmation is not a passing flow.

## What user and system diagrams should mean

Three mapping artifacts answer different questions:

1. A **journey/experience map** describes the user's goals, actions, knowledge, and evidenced difficulties over time.
2. A **screen flow** describes entry, branches, actions, state changes, return routes, and completion across the interface.
3. A **service/process view** exposes actors, delivery responsibilities, channels, and backstage dependencies.

GOV.UK's mapping guidance builds from researched experiences and separates maps when groups traverse materially different stages. It identifies experience mapping as especially useful for longer, multi-step, multi-person services. Its service-landscape guidance distinguishes user and delivery views and acknowledges that detailed whole-journey work may belong above an individual feature team. [UX-28](https://www.gov.uk/service-manual/user-research/creating-an-experience-map), [UX-29](https://www.gov.uk/service-manual/design/map-a-users-whole-problem).

**Our recommendation:** choose the smallest artifact that resolves the actual ambiguity. A two-state control rarely needs a service blueprint. A multi-week account recovery involving support staff may need more than a tidy screen map. Separate observed current state from proposed future state, label assumptions, and never fabricate emotional curves or persona details to fill a template.

Flow diagrams should not disguise uncertainty. A line labeled “submit” must say what may happen next. A user-visible timeout can correspond to a successful server action. This specific distributed-state concern needs architecture-lane evidence; this report identifies the UX seam rather than claiming an audited implementation.

## States, content, measurement, and agency

Carbon distinguishes first-use, user-action outcomes, and errors; image and primary action are optional and context-dependent. A “create your first item” prompt is wrong when a filter hid existing items or permission prevents creation. [UX-05](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states).

The check-answers pattern preserves supplied values and makes edit targets understandable; it scales review placement to transaction size. It does not imply that every reversible setting needs a confirmation screen. [UX-04](https://design-system.service.gov.uk/patterns/check-answers/).

The Human-AI guidelines cover initial expectations, context, correction, dismissal, and adaptation. Their multi-stage practitioner evaluation supports clarity and relevance, not a proven causal effect on user outcomes; the authors name non-GUI and high-risk domain gaps. [UX-26](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf).

HEART links goals, signals, and metrics; it warns that page views or revenue can have ambiguous UX meaning and complements metrics with research. It is an experience-derived framework, not a mandate to instrument every dimension. [UX-25](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/).

The dark-patterns paper documents text-based shopping patterns through a bounded crawl and expert classification. It provides a taxonomy of agency-distorting mechanisms, not a contemporary prevalence estimate or a measured effect of each mechanism. [UX-27](https://arxiv.org/html/1907.07032v2).

**Synthesis for skills:** content labels, validation, consent, state feedback, and recovery belong in flow design. “Polish copy later” can freeze the wrong interaction. Evaluate whether users can understand, choose, refuse, correct, and recover, alongside whether the business's preferred action is completed.

## Candidate task-based skill boundaries

These are recommendations to test, not finished skill names or a fixed taxonomy.

| Capability | Trigger / actual job | Useful output | Exclusion to prevent overreach |
|---|---|---|---|
| Frame and design a product experience | New feature, service, onboarding, or substantial flow problem | Task/outcome brief, actors/context, key assumptions, focused flow alternatives | Do not require personas/journey maps for a local UI fix. |
| Design interaction architecture | Navigation, forms, professional controls, states, cross-screen consistency | Interaction/state model, chosen pattern with tradeoffs, example tasks | Do not prescribe one screen count, aesthetic, or universal navigation limit. |
| Evaluate and improve an experience | User-testing plan, usability problem, recovery audit, comparison of variants | Evidence-linked findings, proportionate research/check plan, observed result | Do not treat heuristic inspection or an automated agent as human user research. |
| Specialized references on demand | Commerce, learning, expert work, mobile permission, international/literacy contexts, AI assistance | Context-specific constraints and cases | Do not load every domain on every task. |

Content design and accessibility should run through the relevant capabilities. A writing skill may own argument, editorial voice, and long-form prose, while product interaction work owns action naming, meaning, and recovery language. Visual craft owns expression and composition; the interaction skill supplies task and state requirements.

## Candidate instructions to forward-test

The source-to-instruction move is our inference. The following are deliberately outcome-oriented and contextual.

1. **Establish the decision.** Name who is doing what, how often, with what knowledge and constraints, and what happens if it fails. State material assumptions as assumptions.
2. **Inspect the existing experience.** Identify real entry points, content, conventions, interfaces, support routes, and limitations before proposing a replacement. Preserve useful learned behavior unless a change has a reason.
3. **Model only the consequential branches.** Include completion, correction, interruption/return, denial and failure appropriate to the feature. Do not force a giant universal state checklist onto every small component.
4. **Compare interaction cost, not screenshot neatness.** Look at decisions, information gathering, typing, inspection, navigation, uncertainty, and recovery. Do not claim that fewer screens or controls necessarily means less work.
5. **Design collection and validation from the data's purpose.** Remove unjustified requests, preserve legitimate values, and test collection-to-confirmation behavior rather than isolated form acceptance.
6. **Use content to express the model.** Actions and state feedback should make the next result intelligible. An icon-only shortcut must not hide frequently needed state without a justified tradeoff.
7. **Preserve meaningful agency.** Make alternatives, consequences, refusal, and reversibility understandable. Business conversion is one outcome; it does not by itself establish informed user success.
8. **Test the relevant population and scenario.** Choose methods and participant coverage from the question and consequences. Do not invent universal issue-discovery percentages.
9. **Separate evidence from proposed fixes.** An observed hesitation does not prove its cause; a plausible redesign is not validated until relevant behavior is checked.
10. **Report practical limits.** Distinguish source guidance, prototype behavior, automated checks, observed user behavior, and production outcomes. Preserve counterexamples that materially affect the rule.

## Example artifacts worth building later

These are proposed original teaching artifacts, not copied proprietary UI or tested examples.

### A. Paired transaction flows

Use the same information requirements in three forms: an infrequent public application, repeat professional entry, and consumer checkout. Annotate each boundary and field with its purpose and cost. Keep the initial evidence equal so an evaluator can see whether the skill adapts to changed context rather than imposing a template.

### B. Stateful professional control comparison

Show icon+tooltip, dropdown, and direct control variants with identical data. Include default and unusual states. Ask the agent to explain inspection versus action cost and propose what evidence would distinguish them.

### C. Entry, refusal, and recovery model

Create an original mobile photo-upload flow that can use a scoped picker or broader access. Include cancel, denial, limited selection, revocation, return, upload failure, and successful completion only where applicable. The outcome should remain understandable after interruption.

### D. Evidence-linked journey and screen flow

Provide anonymized fictional interview/task notes explicitly labeled as fixtures. Ask for a current-state map, a future-state proposal, and an assumption list. Correct outputs must not manufacture user emotions, invent actors, or merge different journeys merely to fill one diagram.

### E. Cultural-data trace

Supply the same diverse name fixtures to a signup screen, stored representation, account header, exported roster, and support search. Teach that all surfaces form one experience and that a “clean” frontend can still corrupt identity downstream.

## Meaningful evaluation cases

Evaluate behavior and reasoning, not whether headings or fashionable phrases appear. A future skill pass should be compared with a no-skill baseline on the same task context, with independent review where available.

| Evaluation task | What a passing response demonstrates | Failure signal |
|---|---|---|
| Public application vs expert repeat-entry form | Chooses segmentation from task/knowledge and explains exceptions | Same wizard generated for both. |
| Figma-like state-heavy control | Distinguishes seeing a value from changing it | Hides all complexity behind icons and calls it simpler. |
| 60-item catalog navigation | Investigates labels, targets, hierarchy and search | Cuts to seven because of Miller/Hick. |
| Beginner learning app with expert return users | Supports guidance and meaningful retrieval/review | Claims Duolingo proves mandatory linear navigation. |
| Five sessions reveal no new issues | Reports observed scope and remaining uncertainty | Certifies fixed percentage coverage or production readiness. |
| Global signup with constrained schema | Finds data/interaction mismatch and preserves real names | Rejects mononyms or silently title-cases names. |
| Permission declined after previous grant | Models denial/revocation and useful fallback | Repeated nagging or an irrelevant full-app blockade. |
| Empty search result in a populated workspace | Explains filter/search cause and useful recovery | Prompts creation as though the workspace has no data. |
| AI assistant makes a wrong suggestion | Provides correction/dismissal and honest capability state | Treats all output as deterministic success. |
| Checkout variant boosts orders but hides fees | Inspects comprehension and choice quality | Declares UX success from conversion alone. |

Proposed evaluation dimensions: task-model accuracy, evidence fidelity, justified alternatives, branch/state coverage, population fit, ability to preserve agency, proportionate artifact choice, and clarity about verification limits. Human testing is necessary for claims about actual human comprehension; an agent review can assess traceability and missing branches but cannot substitute for it.

## Updates: what should change, and what should remain stable

The stable unit should be a decision record with the task context, alternatives, evidence, consequence, counterexample, and verification approach. Do not preserve an initial folder taxonomy at the cost of accumulating overlapping instructions.

Revisit guidance when:
- underlying platform behavior or product evidence changes;
- a new population or workflow violates a current assumption;
- a real application of the skill creates repeated friction or omission;
- a counterexample undermines a universal formulation;
- evaluation shows the skill adds ceremony without improving decisions.

Update process proposal: re-open the owning source; check correction/version and scope; state the changed claim; revise only affected instructions/examples; run relevant paired tasks; retain the limitation. Fresh aesthetic trends may change quickly, while core agency or information-purpose principles can remain useful without pretending to be timeless laws.

## Unresolved gaps and priority follow-ups

1. **Disability-specific interaction evidence:** this lane includes literacy, language, and cultural representation but does not deeply cover screen-reader, motor, cognitive-disability, or neurodivergent task studies. Numerical WCAG and visual accessibility are in the adjacent lane; conformance alone will not close these interaction gaps.
2. **Current platform verification:** Android documentation is current as accessed, but permission flows were not executed on devices; Apple onboarding body was unavailable. OS-specific behavior should be rechecked during implementation.
3. **Longitudinal use:** first-use studies and product redesign accounts do not fully establish retained expert performance, learning, habit formation, or the long-term consequences of simplification.
4. **Product evidence access:** Baymard underlying premium data, Figma internal metrics, and Shopify customer-study protocols were not available. Retain them as bounded practitioner cases.
5. **IA research breadth:** original Hick full methods and contemporary cross-device/assistive navigation comparisons remain open. Do not replace those gaps with catchy law summaries.
6. **Assisted service delivery:** the older live-operator evidence is useful as a counterexample to software-only thinking, but economics, privacy, capacity, and current speech systems need fresh domain-specific investigation.
7. **Skill efficacy:** no actual skill was created, no comparative forward-test ran, and no improvement in model or user outcomes has yet been demonstrated.

## Access failures, provenance, and exclusions

- Faulkner publisher HTML exposed only an abstract; an earlier GeoCities mirror loaded initially but repeated section reads timed out. The publisher PDF subsequently loaded and supplied method/results.
- Cockburn's Canterbury PDF loaded but follow-up retrievals timed out. A teaching mirror supplied model/calibration/design sections; the full later empirical evaluation was not completely retrieved. The calibration claim used here is narrower.
- The 2015 choice-overload publisher page exposed abstract/references. An author-uploaded full PDF on ResearchGate was inspected; the publisher corrigendum was inspected. The supplementary endpoint returned 403, but Appendix B is in the full paper. No independent reanalysis was performed.
- Google Research's legacy PDF route failed; the official publication page's Download link led to the inspected author-version PDF on a different host. This is one paper, not two sources.
- Apple HIG returned a JavaScript placeholder. Its explicit Markdown link was unsupported by the web reader; shell fetch failed DNS. Search excerpts are discovery only, and Apple guidance is excluded from recommendations.
- The original Hick university PDF route returned 404. The paper was discovered, not read. The original Shneiderman PDF repeatedly timed out. Neither is counted as inspected evidence.
- The Sellen mode-error official abstract loaded; linked CiteSeer PDF returned 403. Its two-experiment description is partial access, not a full methods review.
- The Princeton project page returned 403 on open; the versioned arXiv full paper supplied the underlying source. The obsolete June draft found in search has different counts and was excluded.
- A guessed Shopify help route was inaccessible; the inspected current Shopify article documents available configurations. No admin settings were accessed or changed.
- Public discussion threads surfaced counterexample leads. They were not treated as representative complaint rates or causal evidence.
- Tool search timestamps were not used as publication dates. Source dates and explicit version information were preferred.

The report contains original synthesis and short paraphrases with attribution. It does not copy source manuals, reproduce copyrighted interface assets, or imply that a public source licenses its UI for unrestricted reuse.

