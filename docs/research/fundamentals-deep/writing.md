# Writing fundamentals: deep research dossier

Research date: 2026-11-07. This is research for designing skills, not a skill or proof of improved agent behavior. Companion registry: [writing.sources.jsonl](writing.sources.jsonl).

## Decision implications

**Teach substantive judgment before surface polish.** The evidence supports a shared writing foundation with genre-specific procedures, rather than a universal “human-sounding writing” rulebook. Keep research and examples extensible while keeping executable instructions small. This organization is a recommendation inferred from the sources, not a tested taxonomy.

The initial investigation covers 30 core works: 29 substantively inspected sources and one partially inspected EEG preprint. A targeted second round adds two non-English official guides, three inspected historical commit diffs for an existing article (one grouped artifact record), and a later author-hosted version of an already included experiment. Reading included original papers, author accounts, worked revisions, concrete explanatory articles, and technical/product guidance. Five additional registry entries record partial, inaccessible or discovery-only leads. The registry therefore has 39 entries: 33 inspected, two partial, three inaccessible and one discovery-only; these are records, not 39 independent corroborating works. “Inspected” means the relevant body sections and qualifications were read; it does not mean every appendix, interactive widget or cited paper was independently verified. Related chapters from Google, GOV.UK and Julia Evans are explicitly grouped by source family; they are not independent corroboration.

Three boundaries matter:

| Writing job | Primary question | Useful observable outcome | Common category error |
|---|---|---|---|
| Article or argument | What should the reader now believe, question or understand differently? | A defensible point, relevant evidence and fair treatment of objections | A polished survey that has no point |
| Explanation or technical documentation | What knowledge is missing for this reader to understand or perform the task? | Accurate mental model or successful task completion | Replacing necessary terminology with cute analogies |
| Product/service/brand content | What decision or next action must this person make in this situation? | Correct expectations, comprehensible options and feasible recovery | Importing an essay's suspense or a brand's humor into an error state |

A personal essay may explore ambiguity without resolving a task. A reference document may intentionally repeat terminology. A product message may need a short direct answer. None should be forced into the same opening, length or conclusion formula.

## 1. Writing is also a way of finding the idea

The historical process literature challenges a one-way pipeline in which an already finished thought is merely translated and then polished. Flower and Hayes describe nested, goal-directed composing processes; their theory is grounded in protocol analysis and presented as a working account, not an experimentally proven universal method. [WRI-09, pp.365–375](https://eva.fic.udelar.edu.uy/pluginfile.php/26559/mod_resource/content/1/Flower%20y%20Hayes%201981.pdf).

Sommers' 1980 study distinguishes lexical revision from reconsidering an argument and readership. Its Methodology describes twenty students and twenty experienced adults writing and revising three essay types. This is an observational comparison, not evidence that following a fixed sequence causes expertise. [WRI-10, pp.380–387](https://www.pedagoguepodcast.com/uploads/4/1/9/0/41908851/revision_strategies_sommers__1980_.pdf).

**Operational implication, our synthesis:** use a provisional claim or question; permit research and drafting to change it. When a draft is weak, diagnose whether the missing element is reporting, reasoning, organization or wording. Do not keep paraphrasing a paragraph whose underlying point is unresolved.

A practical diagnostic is to write a short margin note for each paragraph stating what it does: establish a fact, explain a mechanism, supply an example, answer an objection, or advance the narrative. If the notes do not form a coherent sequence, reorganize before line editing. Yong describes outlining and reverse outlining as tools for this kind of troubleshooting. His “99 percent” formulation is craft rhetoric, not a measured incidence rate. [WRI-17, structure question](https://magazine.catapult.co/dont-write-alone/stories/interview-with-journalist-ed-yong-writing-process-advice-for-science-writers).

## 2. Reader modeling should change content, not just vocabulary

Google distinguishes role from proximity to a subject; Google’s document chapter organizes material around readers' questions. Their advice is especially useful for avoiding both missing prerequisites and unnecessary re-explanation. These are publisher practices, not comparative outcome studies. [WRI-01](https://developers.google.com/tech-writing/one/audience), [WRI-02](https://developers.google.com/tech-writing/one/documents).

GOV.UK's valid-user-need test is deliberately about service tasks and resists justifying a predetermined tool. It does not establish that all writing must produce an action. Its error-message guidance offers a narrower example where a concrete correction is essential. [WRI-04, good/bad examples](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/), [WRI-05, Writing error messages](https://design-system.service.gov.uk/components/error-message/).

**Procedure candidate:** before drafting, record the reader's relevant prior knowledge, current question, desired change and reading conditions. For an API tutorial, ask what environment and concepts can be assumed. For an essay, identify the interesting tension. For an error, determine what recovery action is actually available. Do not manufacture a persona when the request already supplies sufficient context.

## 3. Argument quality and sentence quality are separate

UNC's argument guidance requires evidence appropriate to the actual claim and recommends engaging serious objections rather than caricatures. Its scope is academic argumentation; the transferable principle is claim/evidence alignment, not a mandatory thesis paragraph for every format. [WRI-06, Evidence and Counterargument](https://writingcenter.unc.edu/tips-and-tools/argument/).

A writing skill should track at least four different failure classes:

1. A statement is unsupported or false.
2. The facts are individually defensible but do not support the conclusion.
3. A real limitation or alternative explanation is omitted.
4. The reasoning is sound but inaccessible to the intended reader.

These need different repairs. Adding citations does not repair an inference that those citations do not support. Making a sentence shorter does not add missing evidence.

**Proposed claim check:** distinguish observation, sourced factual claim, interpretation, recommendation and illustrative fiction. Verify consequential factual statements against their owning sources. Check whether quantities share units, dates and populations. Check that references to a person or system continue to refer to the same entity. Read the argument as a whole after checking its parts.

The FActScore → D-FActScore → VeriScore trail is valuable precisely because later work exposes limitations of earlier decomposition. FActScore separates supported claims within fluent text; D-FActScore shows how entity mixing can defeat independent checks; VeriScore describes contextual and complex assertions that search snippets may not settle. These are metric studies, not validated editorial workflows. [WRI-26, §§2–3](https://aclanthology.org/2023.emnlp-main.741.pdf), [WRI-27, Figure 1](https://aclanthology.org/2024.findings-acl.160.pdf), [WRI-28, §4.4 and Limitations](https://arxiv.org/html/2406.19276v1).

## 4. Style defaults need reasons and exceptions

Gopen and Swan's worked revisions emphasize information order and reader expectations. Their revised examples also expose connections the original author had left ambiguous. They explicitly warn against reducing the approach to a mechanical old/new-information rule. The revisions depend on an interpretation of author intent. [WRI-11, Topic Position and Perceiving Logical Gaps](https://www.cs.tufts.edu/comp/105-2015s/readings/sci.html).

Google's active-voice guidance allows passive voice when the actor is irrelevant or object emphasis matters. Mailchimp separates enduring voice from situational tone; its particular personality is a brand choice. [WRI-03, Exceptions](https://developers.google.com/style/voice), [WRI-07, Tone](https://styleguide.mailchimp.com/voice-and-tone/).

**Procedure candidate:** preserve the intended meaning and voice first. Then examine unclear agents, nominalizations, disconnected sentences, repetition that adds no information and generic praise. Retain exact technical terms when they help the reader reason or search. Do not impose a ban on long sentences, passive voice, first person, humor, cultural detail or rhetorical repetition merely because they can be misused.

Evans' diagnostic catalog is useful because it turns vague virtues into recognizable failures: uneven assumptions about knowledge, strained analogies, unrealistic examples and omitted reasoning. Her comics process separately highlights selecting a useful idea before drawing. These are complementary observations from one practitioner, not independent experimental findings. [WRI-14](https://jvns.ca/blog/confusing-explanations/), [WRI-15](https://jvns.ca/blog/2020/12/05/how-i-write-useful-programming-comics/).

## 5. Five annotated case analyses

These are deliberately different forms, selected for inspectable craft decisions. Their quality assessments and transfer recommendations are ours. No hidden drafts or reader-testing results are assumed.

### A. John McPhee, “Structure” — arranging reported material

[WRI-12](https://www.newyorker.com/magazine/2013/01/14/structure), opening; note-card examples; Hoving portrait; truck journey.

The opening problem leads to alternative arrangements of reported material, including reconsidered chronology. Evidence is the author’s own decisions. Transfer: compare candidate structures against the central question; do not mandate elaborate outlining. This is craft analysis, not an outcome experiment. Diagrams and unpublished drafts were not inspected.

### B. Paul Graham, “Putting Ideas into Words” — testing a claim through exceptions

[WRI-13](https://www.paulgraham.com/words.html), complete essay, especially the stranger-reader test and architecture concession.

**Structure:** a familiar experience introduces a claim; a reader test makes it concrete; formal reasoning and other ways of exploring ideas complicate it; the ending advances a stronger proposition. **Evidence:** experience and analogy, not measurement. **Revision lesson:** anticipate what a reader cannot infer and sacrifice attractive sentences if necessary. Our caution: the ending's universal necessity claim should be evaluated independently of the persuasive voice. A skill should preserve the specificity of the test without adopting the author's generalization as established fact. No historical draft comparison was inspected.

### C. Gabriel Goh, “Why Momentum Really Works” — explanation beyond an analogy

[WRI-18](https://distill.pub/2017/momentum/), opening; polynomial regression; dynamics; stochastic gradients; acknowledgments.

**Structure:** a familiar physical analogy raises unanswered questions; a tractable model supports derivations; examples attach meaning to the mathematics; later sections discuss limits and noise. **Evidence:** equations, examples and citations rather than aesthetic authority. **Revision evidence:** acknowledgments identify editorial input, and three actual historical diffs were inspected in the second round below. **Transfer:** use a small faithful model when an analogy stops explaining; connect each representation to a specific question. Interactivity should support reasoning. Controls were not exercised and derivations were not independently reproduced, so this is craft analysis rather than mathematical validation.

#### Direct revision evidence for the Distill case

These comparisons use the actual `patch` fields returned by GitHub for three commits, not commit-message inference. They show changed text and organization; they do not establish the editor's unrecorded motives or improved reader performance. Same-day timestamps are UTC.

| Inspected diff | Earlier visible organization | Revised visible organization | Why it is substantive |
|---|---|---|---|
| [8bed760eb1383196173f737f9259d62629c7c10b](https://github.com/distillpub/post--momentum/commit/8bed760eb1383196173f737f9259d62629c7c10b), 2017-02-14; `index.html`, “Choosing A Step-size” | Admissible interval precedes an optimizer formula with little verbal bridge. | Interval moves into a footnote; a rate function and the slowest component come first; the explanation connects equal extreme-component rates to the prior observation. | Adds the missing reasoning between observation and formula rather than substituting synonyms. Mathematical correctness was not independently checked. |
| [21f9e0b9d95ecdef2422003f1e5297af9f2fd2af](https://github.com/distillpub/post--momentum/commit/21f9e0b9d95ecdef2422003f1e5297af9f2fd2af), 2017-04-02 08:44; `public/index.html`, introduction | Starts directly with gradient descent's speed limitation and update. | Introduces the physical analogy and its incompleteness before returning to the algorithm. Several alternative questions remain HTML comments and are not yet visible prose. | Changes the reader's entry point; commented alternatives must not be mistaken for the published argument. |
| [c4077ce909583530b9066cd136ba70bad17592cf](https://github.com/distillpub/post--momentum/commit/c4077ce909583530b9066cd136ba70bad17592cf), 2017-04-02 10:30; same file, introduction and stochastic section | Prior commit's visible introduction leaves the incompleteness fairly general. | Specific overshoot/step-size questions become visible, followed by a model-based promise; stochastic discussion explicitly identifies a simplifying noise model. | Clarifies what the article will explain and the assumptions behind a later argument. This is more than a grammar pass. |

Source record [WRI-36](https://github.com/distillpub/post--momentum/commit/c4077ce909583530b9066cd136ba70bad17592cf) groups the related diffs as one historical artifact family. It does not increase the independent source-family count.

**Proposed transferable edit:** when an exposition jumps from a result to a formula, write the missing bridge. When an introduction only says an account is incomplete, name the unanswered question. When an argument depends on a simplifying model, reveal that boundary. None of these requires copying this article's language or using its exact structure.

### D. Julia Evans, “Inside .git” — inspectable examples and bounded scope

[WRI-16](https://jvns.ca/blog/2024/01/26/inside-git/), HEAD through blobs; remote-tracking branches; refs note; closing scope sections.

**Structure:** an explicit inventory leads through small concrete artifacts, then distinctions and qualifications. **Evidence:** file contents and command output let a reader inspect the model. **Revision choice:** the text version expands a comic in response to a reader request; no drafts were compared. **Transfer:** retain real names and show the object being explained before building a larger abstraction. A reusable skill should not silently turn a focused introduction into exhaustive documentation. Commands were not run, and the article's technical claims were not independently audited; copy its explanatory method, not unverified current implementation details.

### E. George Orwell, “Politics and the English Language” — criticism demonstrated on specimens

[WRI-08](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/), specimens; diagnosed habits; concrete-to-inflated transformation; final qualifications.

**Structure:** a proposition about language is followed by specimens, classifications, demonstrations and recommendations. **Evidence:** readers can inspect the quoted failures and the author's transformations; his wider social diagnosis remains argumentative. **Transfer:** demonstrate how an edit changes meaning or conceals agency instead of merely labeling prose bad. The essay's own exception rule and restriction of scope prevent turning it into universal stylistic law. This is a useful counterexample to instructions that remove every unusual phrase or abstract concept. The text was inspected, not its manuscript history.

## 6. What empirical research does and does not say about AI writing

### Quality can improve while distinctiveness falls

Doshi and Hauser's inspected manuscript analyzes 293 writers across randomly assigned no-idea, one-idea and up-to-five-idea conditions, with optional GPT-4 access in treatment arms, and uses 600 evaluators. Story ratings improved while between-story similarity increased. It concerns short human-authored stories with suggested starting points, not arbitrary AI articles. [WRI-19, methods and discussion](https://arxiv.org/pdf/2312.00506).

Agarwal and colleagues compare GPT-4o inline autocomplete across 118 Indian/US participants on culturally grounded English tasks. Effects varied by group and included movement toward American patterns. Two countries and group-level comparisons cannot establish a universal cultural effect. [WRI-20, §§3.3.2 and 5.4](https://arxiv.org/html/2409.11360v3).

**Design implication:** preserve author-supplied observations, framing, cultural context and judgments; distinguish them from model-supplied connective prose. Ask for missing substance instead of inventing personal experience. This is a proposed intervention, not one proven by these experiments.

### Rated recommendation quality can improve while decisions remain wrong

Noy and Zhang's March working paper reports benefits on bounded professional writing. A later author-hosted manuscript has 453 rather than 444 professionals, identifies GPT-3.5, and explicitly says tasks did not require precise factual accuracy or context-specific knowledge. These versions concern the same experiment, not independent replications. [WRI-39, PDF pp.3,6–7](https://shakkednoy.com/Noy%20Zhang%20NBER%20SI.pdf). Dell'Acqua and colleagues find higher human-rated Recommendation Quality even for incorrect recommendations; decision correctness decreased on their selected outside-capability task. Recommendation Quality is the study's rubric-based construct, not an isolated measure of prose or style. These are different tasks and drafts, not a contradiction resolved by declaring AI helpful or harmful overall. [WRI-21, Discussion](https://economics.mit.edu/sites/default/files/inline-files/Noy_Zhang_1_0.pdf), [WRI-22, printed pp.13–15; physical PDF pp.17–19](https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf).

**Design implication:** score accuracy, reasoning, reader usefulness and expression separately. A single “writing quality” grade can hide an important failure.

### Offloading evidence does not establish permanent cognitive harm

Lee and colleagues survey 319 knowledge workers, collecting 936 use examples. Confidence and reported thinking effort are associated; the limitations discuss self-report conflation and sample/language restrictions. This is not a causal test of deteriorating intelligence. [WRI-24, §6.3](https://advait.org/files/lee_2025_ai_critical_thinking_survey.pdf).

The EEG preprint compares small groups across repeated essay sessions: 54 initial participants, 18 in crossover. Only selected sections of the mirrored paper and the [author project overview](https://www.media.mit.edu/projects/your-brain-on-chatgpt/overview/) were inspected; later PDF reads timed out. Neural measures and task recall do not by themselves establish lasting injury or a general learning effect. [WRI-23](https://openlab.macaulay.cuny.edu/cali-mhc/wp-content/uploads/sites/125/2026/03/Your-Brain-on-ChatGPT-compressed.pdf).

**Design implication:** if learning is the goal, evaluate later unaided explanation or transfer as well as the assisted artifact. This is an evaluation proposal, not an inferred clinical claim.

### Reader preference, provenance and truth are different variables

Porter and Machery use English poems and nonexpert readers; their studies separate authorship judgments from ratings under manipulated framing. AI samples could be preferred while human labels raised ratings. König and colleagues' German nutrition-text experiment, by contrast, finds little label effect and substantial failure to notice labels. Different genres, populations and manipulations limit direct comparison. [WRI-30, Study 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC11564748/), [WRI-29, Results and Source neglect](https://pmc.ncbi.nlm.nih.gov/articles/PMC13641973/).

**Design implication:** do not equate sounding human with being good. Blind evaluation helps isolate the artifact, while a separate provenance review checks honest attribution. Label preferences do not justify concealing AI involvement.

### Detection is unsuitable as a quality target

Liang and colleagues evaluate seven historical detectors using TOEFL and US school essays and find unequal false positives plus rewriting sensitivity. Dataset differences and dated tools limit generalization. [WRI-25, Results and Data](https://arxiv.org/html/2304.02819v3).

**Design implication:** neither detector success nor detector avoidance belongs in the writing-quality acceptance criteria. Do not encourage deliberate errors to simulate a human writer.

## 6a. A bounded non-English contrast

Two official sources expose limits of simply exporting English style prescriptions. These are selected Korean/Japanese administrative practices, not global coverage or empirical proof about national writing styles.

The Korean National Institute guide distinguishes useful omission from omission that obscures meaning, with examples restoring a missing actor. It also addresses Korean constituent agreement, particles and translation-like constructions, and asks for a respectful public-facing register. [WRI-37, printed pp.12–20](https://www.korean.go.kr/front/etcData/etcDataView.do?etc_seq=399&mn_id=208). This is a 2014 craft guide; its embedded legal references are historical, not evidence of current law.

The Japanese Council's 2022 recommendation distinguishes document purposes and readers; it allows more accessible notation for explanatory/public-facing material and discusses respectful register. [WRI-38, basic principles and orthography](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf). It is administrative guidance, not an experimentally validated rule for Japanese essays.

**Our inference:** preserve reader orientation and precision as shared goals, but choose syntax, register and orthography within the target language. A blanket “make every actor explicit” or “sound casually friendly” rule can be harmful. Test for actual ambiguity and inappropriate distance instead.

Original Korean evaluation example: edit a public notice such as “신청서를 확인하고 결과 안내 예정” when the responsible office is known. A useful revision could specify that office and delivery channel; the agent must not invent either. Conversely, an ordinary conversational reply whose subject is already clear should not gain a repeated name in every sentence merely to satisfy an English-derived actor checklist.

## 7. Candidate working procedure, to be tested

This is our synthesis rather than a prescription directly validated by any one source.

1. **Frame the writing job.** Identify genre, reader, purpose, supplied voice and constraints. Separate a live question from a settled thesis. Keep this proportional: one sentence can suffice for a short message.
2. **Build the substance.** Gather observations, examples and support. Mark unsupported premises and missing source material. Decide which uncertainty changes the reader's conclusion.
3. **Choose an arrangement.** Try an answer-first structure for task guidance, a mechanism sequence for explanation, a tension/evidence sequence for argument, or a scene/theme structure for narrative. These are options, not genre laws.
4. **Draft and revisit meaning.** Allow the claim and outline to change. Reverse-outline a struggling draft. Return to research when the structure reveals missing support.
5. **Edit and verify.** Check factual support and inference separately; then improve coherence, rhythm, terminology and tone. Preserve authorial choices that serve the piece. Exercise instructions or examples when appropriate. Test reader comprehension against the original purpose.

Entrypoint instructions should contain this decision logic and routing. Detailed study summaries, case analyses and genre examples belong in references. The registry records provenance; it should not be loaded wholesale on every writing task.

## 8. Original before/after examples

These examples are authored for this dossier. Claims are hypothetical and must not be treated as observations about an existing product.

| Failure | Before | After | What changed |
|---|---|---|---|
| Empty claim | “Our platform revolutionizes collaborative work.” | “Assign each review comment to an owner and filter the comments that still need a reply.” | Describes a capability; no invented impact metric. |
| Unsupported causality | “Retention rose after launch, proving the redesign worked.” | “Retention rose after launch. The same week, we changed onboarding emails, so this comparison cannot isolate the redesign's effect.” | Separates observation from causal inference. |
| Wrong audience bridge | “A branch is cheaper than in older version-control tools.” | “A branch records a commit ID; creating one does not copy every project file.” | Supplies the relevant model without requiring historical knowledge. Verify implementation context before publishing. |
| Hidden recovery | “Invalid input.” | “Enter a date in the form DD/MM/YYYY, for example 08/11/2026.” | Specifies a fix, assuming that format is actually accepted. |
| Erased experience | “The event was a meaningful celebration of togetherness.” | “My aunt set an extra bowl beside the stove for my grandfather, as she had every year since he died.” | Illustrates specificity in a fictional memoir example; an agent must never invent such a memory for a real author. |

The last example is not “better” for every purpose. It would be irrelevant in a factual service notice. Its role is to test whether editing preserves relevant experience rather than replacing it with interchangeable praise.

## 9. Meaningful evaluation cases

| Test input | Observable acceptance | Failure exposed |
|---|---|---|
| A persuasive launch essay with attractive prose and an unsupported 40% savings claim | Removes, qualifies or requests evidence for the number while retaining a useful argument | Polish hiding fabrication |
| An accurate paragraph with two same-name people blended together | Resolves identity throughout the paragraph; preserves remaining supported claims | Atomic facts falsely implying one coherent biography |
| A developer tutorial for users who know Python but not the deployment system | Explains missing deployment prerequisites, keeps familiar Python concepts brief, and produces executable steps | Role-based audience assumptions |
| A short cultural/personal essay with distinctive expressions and deliberate repetition | Improves confusion without replacing concrete experiences or imposing foreign idioms | Homogenization disguised as professionalism |
| An error-state message where the user cannot retry | Gives a real available next action; does not invent a retry affordance | Generic recovery advice disconnected from product behavior |
| An essay whose strongest counterexample invalidates its thesis | Revises the claim and structure instead of adding a cosmetic caveat | Confirmation-oriented research |
| A learning exercise followed later by an unaided explanation of a new example | Evaluates transfer separately from assisted output quality | Confusing finished work with learning |
| Identical text presented with and without an AI label | Records artifact scores blind, with provenance handled separately | Label bias contaminating craft evaluation |

Before claiming the skill helps, compare it with an ordinary capable-agent baseline on held-out tasks. Use the same source packets and constraints, blind assessment when feasible, and explicit failure examples. Record factual errors, unsupported inferences, reader-task success and preservation of supplied voice separately. Small evaluations can find regressions but do not establish universal superiority.

## 10. Search coverage, exclusions and version conflicts

Representative queries used (including targeted follow-through):

- `A Cognitive Process Theory of Writing pdf Flower Hayes 1981`; `Revision Strategies of Student Writers and Experienced Adult Writers pdf`; `The Science of Scientific Writing Gopen Swan original`.
- `site.jvns.ca writing explanations`; `site.niemanstoryboard.org Ed Yong annotation writing process`; `site.newyorker.com Structure McPhee`; `site.paulgraham.com Putting Ideas into Words`; `site.distill.pub Why Momentum Really Works`.
- `AI writing cognitive offloading Your Brain on ChatGPT essay EEG MIT paper`; `AI writing readers trust AI labels bias study experiment original`; `LLM generated text detection unreliable non native English writers detectors paper`.
- `FActScore long form factuality`; followed the methodological trail to entity ambiguity and VeriScore; `Microsoft generative AI critical thinking knowledge workers survey`; `Navigating Jagged Technological Frontier`.
- `AI generated poetry indistinguishable human written preferred readers Porter Machery`; official Google, GOV.UK and Mailchimp guidance searches.

- `site.github.com/distillpub/post--momentum draft edit`; GitHub REST commit history followed to three exact diffs after browser history URLs failed.
- `site.korean.go.kr 공공언어 요건 정확성 소통성 문장`; `쉬운 공공언어 쓰기 길잡이 2014`; `site.bunka.go.jp 公用文 作成 考え方 読み手 分かりやすく`.

These searches cover several independent evidence families but are not a systematic review or exhaustive survey. Selection favors openly accessible English-language work and inspectable primary artifacts. Search snippets were used to discover sources, not treated as full-text receipts.

**Conflicts and access limits that affect conclusions:**

- The 1980 Sommers journal article specifies twenty students plus twenty experienced adults. The 1982 ERIC report abstract lists eight plus seven. These are distinct records; the latter was not read in full and their samples must not be merged. [WRI-33](https://eric.ed.gov/?id=ED220839).
- Noy/Zhang's March 10 working paper has 444 participants and explicitly says it is not peer reviewed. The published Science DOI returned 403. Targeted review located the author-hosted 19-page NBER SI manuscript (WRI-39), which has 453 participants; its exact revision date and equivalence to the publisher version remain unverified. Sample figures are kept version-specific; percentage effects are not combined. [WRI-31](https://doi.org/10.1126/science.adh2586).
- Doshi/Hauser's published DOI returned 403; the full arXiv author manuscript was used. Its findings should be cited with that version boundary.
- Graham's current page differs from the text rendered in a search result; case analysis follows the opened current page. It is not evidence of the historical editing sequence.
- The EEG compressed mirror was accessible once; later targeted reads timed out. Its exact equivalence to the current arXiv revision is unverified; it remains partial evidence.
- An APA creative-writing label study, SPJ guidance, and a recent Nature diversity briefing were discovered but inaccessible or insufficiently inspected. They do not contribute substantive findings here. See WRI-32, WRI-34 and WRI-35.

## 11. Targeted next research and update policy

The largest remaining gaps are multilingual writing beyond English, expert long-form literary evaluation, realistic editing with the author's source packet, provenance requirements by publication context, and independent tests of the proposed workflow. Additional manuals from similar institutions would add less value than those investigations.

Prioritize these follow-ups:

1. Extend the initial Distill diff analysis to a second genre with a public draft history and substantive edits. Three selected commits now provide direct revision evidence; they do not establish the full process or its effect on readers.
2. Extend the two official non-English administrative sources to Korean and English authored articles with explicit audience context. Preserve language-specific rhetoric; the current guides do not cover literary or personal prose.
3. Add expert versus lay-reader evaluation for longer literary prose. The poetry results do not settle article quality.
4. Refresh AI studies by task and model version; seek replications and unaided follow-up outcomes before strengthening claims about cognition or learning.
5. Run the held-out skill evaluations above and remove rules that repeatedly harm correct, distinctive writing.

For future updates, record the source, scope and reason for each proposed rule change. Maintain separate labels for empirical result, documented practice and our inference. New evidence should be able to narrow or remove a rule. Do not expand the skill merely to increase reference count.
