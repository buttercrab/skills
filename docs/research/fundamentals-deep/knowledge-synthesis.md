# Turning deep research into usable judgment

Date: 2026-11-07. Coordinator investigation. This report concerns how to synthesize the domain research and later test instructions; it does not establish that a particular new skill works.

## Main finding

The research collection and the skill library serve different purposes. The collection preserves breadth, disagreement, provenance, and examples. An activated skill should help with a coherent task by changing consequential decisions. A rule is worth retaining when its application conditions, observable effect, and failure modes are understood—not because it is frequently repeated or sounds fundamental.

Human learning research offers hypotheses for designing examples, not evidence that an LLM learns like a human. Direct model research offers stronger evidence about particular prompting setups, but those experiments also have task, model, and date boundaries. The proposed translation process must preserve that distinction.

## Original evidence and limits

### Examples must teach the relevant relation

[Gick and Holyoak, 1983](https://gwern.net/doc/psychology/1983-gick.pdf), especially Part II, compared human transfer from story analogies. Diagram-plus-story exposure did not reliably produce the intended abstraction; comparisons between analogs helped under studied conditions. This supports testing whether a teaching example exposes a decision mechanism, rather than assuming that an attractive diagram makes it transferable. It does not prove effectiveness for agents.

[Gentner, Loewenstein and Thompson, 2003](https://groups.psych.northwestern.edu/gentner/papers/GentnerLoewensteinThompson03.pdf), Experiment 2, randomly assigned undergraduates to compare negotiation cases or study them separately. Comparison improved transfer in that task. Their coding procedures and subsequent face-to-face experiment make this more informative than an isolated maxim about examples, while leaving professional and long-term transfer unresolved.

The classic [Chi/Feltovich/Glaser paper](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog0502_2) is a useful lead on principle-based versus surface categorization. Only its abstract was substantively available here. It should not carry a detailed methodological claim in this collection until the full paper is inspected.

### Guidance depends on what the learner already knows

[Collins, Brown and Newman, 1987](https://files.eric.ed.gov/fulltext/ED284181.pdf), selected framework sections, propose making expert strategies visible through modeling, articulation, and reflection. [Kalyuga and colleagues, 2003](https://www.davidlewisphd.com/courses/EDD8121/readings/2003-Kalyuga_et_al.pdf), especially the spreadsheet example and conclusions, review cases in which useful novice support becomes redundant or counterproductive with expertise. Neither establishes a transformer mechanism. Our inference is to measure added value over the actual agent baseline.

[Sweller and Cooper, 1985](https://onderwijs.felienne.nl/vakdidactiek/materiaal/sweller_worked_examples.pdf) report worked-example effects with structural limits. Only introductory material was successfully inspected; deeper retrieval timed out. The record remains partial rather than converting a familiar citation into a fully reviewed finding.

### Model examples are interventions, not neutral illustrations

[Min and colleagues, 2022](https://aclanthology.org/2022.emnlp-main.759.pdf), Sections 3–5, distinguish the roles of labels, input distribution, and formatting in classification/multiple-choice demonstrations. Six LMs are evaluated with two inference methods; this should not be described as twelve independently trained models. The results do not justify supplying incorrect coding examples.

[Lu and colleagues, 2022](https://aclanthology.org/2022.acl-long.556.pdf), Section 2, vary the order of the same classification examples and compare models. [Liu and colleagues, 2024](https://aclanthology.org/2024.tacl-1.9.pdf), Sections 2–5, vary relevant-information position and retrieval context. Both suggest useful perturbation tests. Neither establishes a universal present-day prompt layout, optimal skill length, or outcome for end-to-end agents.

### Good evidence is question-specific

The [ACM SIGSOFT empirical standards](https://www2.sigsoft.org/EmpiricalStandards/docs/standards) distinguish standards for different research methods and warn against mechanical review criteria. The [ASA statement](https://errorstatistics.com/wp-content/uploads/2019/01/wasserstein-lazar-asa-statement-pub.pdf) separates statistical significance from effect size, importance, and hypothesis truth. We should examine study design, uncertainty, and practical relevance before changing an instruction.

[Baltes and colleagues' LLM research guidance](https://link.springer.com/article/10.1007/s10664-026-10922-3), Sections 5.2–5.8, treats the system, traces, baseline, measures, and limitations as part of the evaluation. Its online publication date is 3 November 2026 despite its 2027 volume assignment. A local skill trial can adopt proportionate reporting without pretending to reproduce a full research benchmark.

[Gelman and Loken, 2013](https://stat.columbia.edu/~gelman/research/unpublished/forking.pdf), introductory framework, explain how data-dependent choices can distort confirmatory interpretation without conscious cherry-picking. Our application: keep exploratory revisions distinct from an untouched comparison set. An evolving taxonomy is compatible with disciplined evaluation; it does not require fixing all research questions forever.

[Rittel and Webber, 1973](https://marshallviliesis.com/wp-content/uploads/2020/08/rittel-1973-wicked-problems.pdf), pp.160–164, concern public-planning problems with contested framing and value judgments. They help explain why some design goals require explicit judgment. They do not erase correct answers in bounded engineering tasks or justify never finishing a research assignment.

The [Kitchenham/Charters review protocol](https://homepages.dcc.ufmg.br/~figueiredo/disciplinas/papers/guidelines-kitchenham.pdf) was only partially retrieved, and Platt's original essay endpoint failed. Those records preserve access boundaries; this investigation is not presented as a registered systematic review.

## Four original example structures to test

These are proposed teaching/evaluation artifacts, not observed experimental findings.

| Structure | Example | Decision it tests |
| --- | --- | --- |
| Similar appearance, different mechanism | Two empty tables: one has no records, another has a filter hiding existing records. | Does the agent choose a useful action based on the cause instead of copying the same empty-state card? |
| Different appearance, same mechanism | A payment timeout and a job-submission timeout, each after a remote side effect may have committed. | Can the agent recognize an unknown outcome, identify retry ownership, and avoid assuming failure means no effect? |
| Same task, changed constraint | A novice's occasional setup form versus an expert's repeated data-entry workflow. | Does advice change when frequency, knowledge, keyboard use, and interruption costs change? |
| Plausible pattern, no justified intervention | A small flat library whose public API, tests, and release command are already discoverable. | Can the agent leave a suitable structure alone instead of imposing a monorepo template? |

For each pair, explain the decisive difference, retain irrelevant similarities, and test a new instance. A copied answer is weaker evidence than recognizing why a superficially similar answer would be wrong.

## Proposed research-to-instruction process

### Preserve findings before prescribing behavior

A source record should distinguish what the source establishes from what we propose to do with it. A standard, controlled experiment, retrospective incident, repository policy, practitioner argument, and taste preference can all be useful, but they answer different questions. Avoid a single credibility score that hides those differences.

When sources disagree, first compare definitions, population, task, revision, and outcome. A difference between a first-use usability study and repeated expert work may be a boundary condition rather than an unresolved contradiction. Multiple pages repeating the same study are one evidential origin.

### Promote guidance with an application condition

Prefer a testable instruction such as “When a remote side effect has an uncertain outcome, determine the operation's identity and reconciliation path before retrying” over a universal architectural prescription. Stronger evidence for a mechanism can justify confidence in that condition; it still does not choose every concrete implementation.

For creative work, state the desired effect and relevant constraints. “Use a distinctive typeface” does not identify the reader, brand, script support, reading task, performance budget, or fallback behavior. A preference can still be valuable when explicitly chosen for a project. It should remain a preference.

### Keep examples illustrative rather than authoritative

Mark placeholders and variable paths. Include a case where the pictured solution is inappropriate. Avoid accidental anchors such as framework choice, directory names, made-up business numbers, or a single author's tone. An example should expose reasoning while leaving room for the current user's actual constraints.

### Evaluate more than instruction compliance

Define the outcome separately from the procedure. The agent naming a skill, following a checklist, or producing every requested heading is not equivalent to a good result. A technically correct implementation may still fail the user's workflow; polished writing may still recommend something false; a diagram may render successfully while inventing a component.

Keep behavioral checks and judgment criteria distinct. For a UI, examine completion/recovery and visual appropriateness separately. For prose, examine truth/support and authorial quality separately. For architecture, examine scenario behavior and the accuracy of the described structure. Show the evidence available for each judgment.

### Test composition and non-activation

A skill should improve relevant work without attracting unrelated requests. Use realistic activation requests, near misses, and combinations. A writing skill should not rewrite strings during a narrow bug fix merely because text exists in the file. A security reference should not impose a full application threat model on a typo correction.

Compare against the actual baseline configuration, including already active instructions. If existing audit/refactoring guidance already causes the desired behavior, duplicating it may add no benefit. Pin the instruction revision and record which skills loaded.

## Original maintenance proposal

Keep three related artifacts where useful: the source record, the guidance derived from it, and the tasks that would expose a bad application. Their relationship should remain inspectable without loading every research report during ordinary work.

Revise when evidence changes an application condition, a case reveals a failure, or the actual tools/frameworks/standards drift. Remove rules that mostly restate baseline knowledge, conflict with user intent, cause irrelevant work, or optimize a proxy rather than the task. Preserve superseded reasoning when it explains a consequential decision; do not require elaborate version machinery for every sentence edit.

Separate research examples from held-out evaluation cases. Once an example has influenced a skill draft, success on it measures regression resistance rather than fresh generalization. Repeat comparisons when nondeterminism could plausibly change a decision; record uncertainty instead of turning one win into a universal claim.

## Search trail and remaining gaps

Search families covered expert/novice categorization, schema induction, analogical transfer, cognitive apprenticeship, worked examples, expertise reversal, planning problem formulation, software-engineering research standards/reviews, statistical interpretation, LLM demonstration format/order, and long-context retrieval. Primary full texts were preferred; mirrors were used for original content when author/publisher endpoints failed. Bibliographic aliases were treated as one work.

Read depth was selective and reported: Gick Part II, Gentner Experiments 2–3 methods/results, apprenticeship framework, expertise-reversal examples/conclusions, LLM study setup/controlled manipulations, and methodological guideline sections. Chi, Sweller, and Kitchenham remain partial. No human-learning finding was treated as proof of agent learning.

Further empirical work needed: real agent trials across current models/tools, realistic multi-skill combinations, delayed outcomes of architectural decisions, human judgments of voice and visual relevance, and evaluation cost/benefit. This report proposes a way to use the domain evidence; it does not validate that proposal experimentally.
