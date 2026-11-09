# Eliciting human creative direction for the design pilot

Research date: 2026-11-07. Scope: human direction, requirements, questions, examples, critique, and initiative in a design skill. No skill edits or behavioral trials performed by this research lane.

## Decision for the pilot

**Let the human establish the meaningful direction, and let the agent do the design work within it.** When creative context is missing, ask a consequential, answerable question before committing to a global visual direction. When a detailed brief or explicit creative delegation already supplies that authority, proceed within it and make material assumptions visible.

This is a proposed operating policy, shaped by the user's stated preference and the research below. No paper proves this exact policy or an optimal universal number of questions. The evidence supports conditional dialogue, grounded examples, shared interpretation, and adaptation; it also shows why a long questionnaire or approval after every screen is not justified.

A human can lead by supplying a story, purpose, audience, reference, rejection, tradeoff, constraint, or permission to explore. They need not choose every font weight, produce a finished art direction, or become a UI specialist.

## What was inspected

The [ledger](questioning.sources.jsonl) records 17 sources: 14 inspected and three partial. Relevant sections were read rather than every page of every paper. The set covers mixed-initiative HCI, requirements methods, participatory design, practitioner interviewing/framing, prototype critique, preference elicitation, communication grounding, and computational clarification.

The three partial sources are deliberately separated: a scanned design-fixation paper with inadequate extraction; a search-clarification study whose later methods retrieval timed out; and a 2026 creative-AI timing study whose full publisher routes returned 403. No precise effect or universal timing rule rests on those access gaps.

Empirical design studies are bounded by their tasks, people, tools, and outcomes. Research participants in a usability session, a paying project owner, a creative collaborator, and future end users are different roles. Asking the owner what expresses their brand does not establish what end users need or whether the resulting interface works.

## Findings that matter to implementation

### 1. Ask to improve the decision, with a useful answer in reach

[Horvitz's mixed-initiative principles](https://erichorvitz.com/chi99horvitz.pdf), principles 5–11, connect dialogue with key uncertainty, interruption cost, direct user control, refinement, and memory of recent interaction. This is a principles/prototype account, not a creative-brief trial. [QUE-01]

[Zhang and Choi](https://aclanthology.org/2025.findings-naacl.306.pdf), §2 and §4, distinguish uncertainty from predictions that clarification can actually improve. Their QA/translation/inference evaluation uses annotation-derived oracle question/answer pairs and interaction budgets; it does not measure a person's effort in a creative conversation. [QUE-11]

**Pilot implication:** before asking, identify which design choice depends on the answer. Ask for human-owned context or preference the human can supply. Discover available facts directly. Do not ask the user to fix the agent's lack of research, rendering knowledge, or professional judgment.

A useful question may take effort. The objective is useful collaboration, not the fewest question marks. Conversely, a question that repeats the brief, merely ratifies an already chosen template, or cannot change the work adds little value.

### 2. A brief is developed and interpreted, not mechanically collected

[Nuseibeh/Easterbrook](https://www.cs.toronto.edu/~sme/papers/2000/ICSE2000.pdf), §4.1–4.3, combine document analysis, interviews, contextual techniques, and prototypes; §4.3 explicitly allows technique selection rather than a full rigid method. §8 treats requirements as evolving. [QUE-02]

[Goguen/Linde](https://lectureweb.github.io/CS865DistributedandOperatingSystems/CS775/Papers/goguen_techniques.pdf), §2–3 and §7, analyze how introspection and fixed questionnaires can miss tacit knowledge and shared meaning. This is methodological argument with examples, not a controlled ranking of techniques. [QUE-03]

**Pilot implication:** inspect existing content, design systems, source, product context, and prior answers before asking. Treat a vague word such as “friendly” as a direction requiring interpretation, not permission to invent an entire brand. Interpret it through the product's audience and purpose, and clarify only where different interpretations would lead to materially different results.

Questions can reveal a problem; they do not automatically settle its solution. A good answer should be reflected in an actual design decision.

### 3. Human creativity needs ways to express itself

[Sanders/Stappers](https://coactproject.eu/wp-content/uploads/2022/11/Co-creation-and-the-new-landscapes-of-design-1.pdf) describe participants contributing to informing, ideation, and conceptualization, rather than merely evaluating concepts supplied by professionals. This is a conceptual account of co-design; it does not establish that every participant wants the same responsibilities. [QUE-04]

[IDEO.org's framing method](https://www.designkit.org/methods/frame-your-design-challenge.html) links outcomes, audience, context, and constraints while retaining multiple solutions. Its [co-creation method](https://www.designkit.org/methods/co-creation-session.html) invites people to make and reshape ideas. These are practitioner recipes, not experiments or mandatory chat rituals. [QUE-05, QUE-17]

**Pilot implication:** offer forms of participation matched to the person and task. A non-designer may explain what a place feels like, identify a reference detail, describe an audience, rearrange priorities, or reject an association. The agent should translate these contributions into design work without forcing the person to master abstract style vocabulary.

“Humans lead” should not mean “the human must answer every professional design question.” Explicit delegation is also a human decision.

### 4. Alternatives support critique, but do not automatically produce new design ideas

[Tohidi et al.](https://www.billbuxton.com/rightDesign.pdf) compared one versus three thermostat paper prototypes with 48 students/recent graduates. Multiple alternatives changed ratings and criticism, but did not significantly increase substantial redesign suggestions. Lower ratings do not alone prove that feedback became objectively truer. [QUE-09]

[Dow et al.](https://hci.stanford.edu/publications/2010/parallel-prototyping/ParallelPrototyping2010-final.pdf), §3, held prototype count, feedback amount, and time constant for 33 nonprofessional designers creating web ads. Parallel work improved several measured outcomes. One client, experimenter-selected critique, and ad metrics limit transfer. [QUE-08]

**Pilot implication:** use alternatives when they reveal a real unresolved direction; present them as provisional. Ask which specific qualities to retain, change, combine, or reject. The agent remains responsible for proposing coherent solutions and interpreting feedback.

These studies do not justify three compulsory options, a vote on every component, or stopping after every screen. They also do not prove that any generated alternatives are meaningfully different.

### 5. Examples can reveal preferences and constrain them

[Viappiani/Faltings/Pu](https://arxiv.org/pdf/1110.0026), §3 and §5, discuss narrow examples trapping search locally and evaluate suggestions that elicit additional preferences. The supervised apartment-search comparison involved 40 mostly undergraduate users; its preferred-choice measurement belongs to a finite catalog, not open-ended art direction. [QUE-10]

[IDEO.org Conversation Starters](https://www.designkit.org/methods/conversation-starters.html) treats concepts as disposable prompts and follows the person's interpretation. That is exploratory practice, not neutral preference measurement. [QUE-06]

**Pilot implication:** show enough difference to make an important tradeoff discussable, and leave room for an answer outside the offered set. Ask what aspect of a reference matters before copying its whole aesthetic. Do not assume that choosing an option reveals a complete or permanent preference.

No presentation can be guaranteed free of influence. Avoid artificially making one option look finished, prestigious, or sensible while alternatives are implausible. Explain a recommendation as a reasoned proposal rather than a default the user must accept.

### 6. Shared understanding can be sufficient and revisable

[Clark/Brennan](https://web.stanford.edu/~clark/1990s/Clark%2C%20H.H.%20_%20Brennan%2C%20S.E.%20_Grounding%20in%20communication_%201991.pdf) describes understanding sufficient for the current purpose and minimizing combined communication effort. Their human-dialogue theory supports a useful analogy; applying it to agent state is our proposal. [QUE-14]

[GOV.UK interview guidance](https://www.gov.uk/service-manual/user-research/using-in-depth-interviews), “Do the interview,” favors open neutral prompts, actual stories/examples, and adaptive follow-ups rather than rigid adherence to a guide. It concerns research, so do not copy its session length or consent procedure into a routine creative chat. [QUE-07]

**Pilot implication:** use short, concrete interpretations when an answer is ambiguous. Let the human correct them. Preserve partial answers and proceed with independent work; return to only the unresolved consequential choice. Do not reopen settled preferences or require perfect upfront specification.

## Proposed discover / ask / proceed process

This is original synthesis for the pilot, not a measured algorithm. It should be implemented as judgment, not a scored checklist.

| Situation | Appropriate move | Example |
|---|---|---|
| The brief already gives purpose, audience, references and constraints | Proceed within the brief | Keep the supplied brand and direction; do not start a generic taste interview. |
| A relevant fact exists in source, assets or project documents | Discover it | Read the existing navigation, copy, tokens and supported interaction patterns. |
| The missing answer would change product meaning or global creative direction, and the human has not delegated it | Ask before committing to that choice | “What should this community feel like to someone arriving for the first time?” |
| The person cannot verbalize taste yet | Ground the question in concrete possibilities | Show contextual references or small concepts and ask what draws them in or pushes them away. |
| The person explicitly delegates creative decisions | Propose and execute within that scope | Choose a coherent direction from product/audience evidence and state material assumptions. |
| A small, reversible implementation choice remains | Use professional judgment | Choose a consistent spacing value or native control without a new preference poll. |
| Answers conflict in a way that prevents a coherent decision | Expose the particular tradeoff | Ask which outcome has priority; do not silently discard one requirement. |
| An answer is partial | Retain it and narrow the unresolved issue | Preserve “warm and quiet”; clarify only if “quiet” could mean visually restrained or low-interruption behavior. |

The important distinction is whether the agent has enough direction for the next consequential decision. It is not whether every field in an intake form has a value.

An unanswered question is still unanswered. Time passing does not establish a preference. Continue work that does not depend on it; if useful, label a reversible exploration as provisional. Do not treat that exploration as an approved final direction.

## Question construction: make the human's contribution concrete

These examples are invented exercises, not source quotations or mandatory templates.

### Ask about the job before visual vocabulary when the job is unknown

Weak: “Minimal, modern, or playful?”

Better: “Who is coming here, and what should they be able to understand or do before they leave?”

If the product and task are already known, do not ask again. Ask about the remaining creative uncertainty instead.

### Elicit the intended impression through this product's world

Weak: “Do you want a beautiful, friendly design?”

Better: “Should this local language club feel more like an invitation from a welcoming host or a practical guide to nearby sessions? What would feel wrong for it?”

The alternatives here correspond to the actual product's communication problem. They remain incomplete possibilities; a person may want both, neither, or another metaphor.

### Ask what a reference contributes

Weak: “We will use this site's design.”

Better: “Which part of this reference matters here: its calm hierarchy, photography, conversational copy, or something else?”

Carry forward the identified qualities. Do not infer permission to copy a logo, proprietary assets, interaction model, or every stylistic detail.

### Turn critique into an interpretable change

Weak: “Do you like option B?”

Better: “What makes B feel closer to your intent, and what should we leave behind?”

If the human says “too corporate,” connect the criticism to an observable feature or association. Offer a specific interpretation such as stock imagery, formal language, rigid symmetry, or lack of local character. Do not automatically translate it into more saturated colors or rounded cards.

### Help with uncertainty without forcing a preference

A person saying “I don't know” may mean they need examples, have no preference on that axis, or want the agent to decide. Those are different. Respond with a small concrete proposal or make the local scope explicit. A local delegation about type does not erase a clear constraint about audience or tone.

## Preference elicitation without hiding the agent's influence

The pilot should make selection meaningful while preserving the human's ability to reject the framing.

- Keep alternatives comparable enough in fidelity and content that polish alone does not determine the result.
- Describe substantive tradeoffs and avoid a “good answer” beside obviously inferior decoys.
- Allow free expression, combination, rejection, and “no preference.” Do not force a complete brand into one label.
- Ask about relevant qualities rather than prestige of a reference brand.
- Separate what the person explicitly chose from what the agent inferred.
- If the interaction surface requires a recommended choice, explain its contextual reason; do not present a taste preference as a fact.
- Treat a reaction to a deliberately provocative example as exploratory evidence, not a binding requirement.
- Avoid persisting a task-specific answer as a cross-project personal preference without authorization.

These are proposed safeguards. The survey does not establish that they remove anchoring, social desirability, or power imbalance. Actual pilot trials should include people rejecting the offered options.

## Recording and honoring direction

Use the existing brief, task notes, or chat state; a new file or elaborate schema is not mandatory. The important information is:

- what was explicitly requested and for which task/surface;
- what was discovered in existing artifacts;
- what the human delegated;
- what the agent inferred provisionally;
- which consequential questions remain open;
- what later feedback changed.

A short interpretation can be useful: “Warm, local and quiet; keep the existing blue; use actual gathering photos; explore the layout independently.” If the human corrects it, update the affected decisions. Do not ask them to approve the same direction again on each screen.

“Honoring” should be visible in outputs. A preference that never changes layout, copy, imagery, hierarchy, or interaction has not meaningfully influenced the design. Conversely, an instruction such as “keep the brand” must survive subsequent autonomous polishing.

When new feedback changes direction, preserve unaffected constraints. A new layout request does not cancel agreed content; rejecting a photo does not reject the entire visual identity.

## How to learn from critique

Distinguish at least three kinds of feedback by their consequence, without requiring the person to use these labels:

1. **Mismatch of purpose or audience:** revisit the premise and affected flows.
2. **Mismatch of character or reference interpretation:** revise the direction and the visual decisions carrying it.
3. **Local execution issue:** improve the component or detail without restarting discovery.

These categories are a proposed diagnostic aid. Do not make the person classify their own feedback. An apparently local comment may reveal a global problem; ask a targeted follow-up if that distinction changes the work.

Keep a coherent design rather than combining every liked fragment mechanically. If two requested qualities conflict, explain the specific conflict and offer a concrete resolution. User leadership includes the right to reject the agent's rationale and choose a tradeoff.

## Counterevidence and claims to avoid

The [commercial spoken-language study](https://arxiv.org/pdf/2109.12451), §1 and §4, treats redundant clarification as a cost and evaluates context-aware ask decisions. It is offline classification on spoken-agent data, not a creative workflow intervention. [QUE-12]

Three partially accessible studies give useful leads but should not carry a pilot guarantee:

- [Jansson/Smith](https://www.sciencedirect.com/science/article/abs/pii/0142694X9190003F) reports design-fixation experiments. Detailed method verification failed in this pass, so do not attach precise rates or ban all references. [QUE-15]
- [Zou et al.](https://irlab.science.uva.nl/wp-content/papercite-data/pdf/zou2022asking.pdf) reports effects of question-quality trajectories with 89 search participants. Search tasks and incomplete method access limit transfer. [QUE-13]
- [Jung et al. 2026](https://doi.org/10.1145/3803784.3816856) reports 30 text/image-task participants and perceived effort/trust effects. Full study protocol was inaccessible; greater trust is not proof of better accuracy, creativity, or calibration. [QUE-16]

Do not teach:

- always ask first;
- never ask because autonomy matters;
- ask exactly a fixed number of questions;
- let humans choose from three preselected aesthetics;
- more questions necessarily produce more creativity;
- approval after every component demonstrates human leadership;
- more praise or expressed confidence proves a better design;
- a human owner's preference is evidence of end-user usability;
- clarification can resolve missing domain knowledge or impossible constraints.

## Pilot evaluation cases

These are proposed tests for observable behavior. They are not yet trial results.

| Input case | Expected behavior | Failure signal |
|---|---|---|
| A rich brief with brand, audience, reference qualities and clear constraints | Works within it, preserving answers | Repeats generic intake questions or restyles the brand. |
| “Build a site” with no product or audience | Elicits consequential context before global direction | Produces a generic SaaS landing template. |
| Product/audience known, mood missing | Asks a concrete contextual question | Uses abstract style labels as the only creative input. |
| “You choose the direction; keep our logo and copy” | Exercises delegated judgment within those constraints | Repeated approvals or unauthorized logo/copy changes. |
| Human responds with a story or one reference detail | Extracts implications and marks uncertainty | Demands a complete questionnaire or copies the whole reference. |
| Partial answer plus “I don't know about fonts” | Retains known direction and handles the local uncertainty | Treats unknown font as missing all direction. |
| User rejects every offered alternative | Reopens the framing and accepts new input | Forces a choice or reoffers the same aesthetic set. |
| “Too corporate” after a preview | Identifies what causes the mismatch and revises affected decisions | Random cosmetic changes without interpreting the feedback. |
| A previously answered constraint is relevant again | Reuses it | Reasks or contradicts it during later screens. |
| Tiny reversible spacing fix | Makes a consistent local decision | Starts a full creative interview. |
| Answer would not repair the agent's technical uncertainty | Researches or narrows its claim | Asks the user to choose an unsupported technical answer. |
| Owner's taste conflicts with observed task difficulty | Explains the consequence and a concrete alternative | Silently discards preference or declares usability solved by approval. |

Assess question relevance, answerability, use of existing context, preservation of explicit choices, interpretation quality, breadth of genuine alternatives, proportionate initiative, and correction after feedback. Count questions only as a diagnostic; a lower or higher count is not the goal by itself.

Meaningful human-led creativity also requires artifact inspection: can reviewers trace specific user contributions to design decisions? Are proposals distinct because of the product and brief? Does critique change the outcome while retaining the constraints the person kept?

## Research coverage, searches and gaps

Search families: mixed-initiative uncertainty/dialogue/attention; requirements elicitation and tacit context; participatory/co-design roles; creative challenge/brief framing; open neutral interviewing; parallel prototypes and multiple-design critique; example-critiquing and anchoring; clarification usefulness and interaction cost; grounding, reference and repair.

Citation trails followed original papers from university/author sites rather than adopting secondary lists. The Dow paper led to Tohidi's experiment and its negative result on substantial suggestions. Preference-search work led to its explicit local-optimum concern and study method. The NLP clarification paper led to its oracle-generation design, preventing a false claim of observed live-human behavior.

Access failures: UCL and teaching mirrors of the requirements roadmap timed out; the author's Toronto copy supplied relevant sections. Sanders/Stappers' first PDF loaded, later section fetches timed out, publisher full HTML returned403, and the old author-site route was unavailable; only inspected introductory/definition material is relied upon. Tohidi's ronbaecker.com mirror redirected unsuccessfully; Buxton's author copy worked. Jansson's scan did not yield sufficient usable text or screenshot transport for detailed methods. Zou's manuscript later timed out; the full methodology is not claimed. The 2026 timing DOI and full HTML returned403 despite indexed publisher excerpts.

Remaining gaps:
- Direct evaluation of real human-agent visual-design briefing, including experts, novices and people with different communication needs.
- Long-term retention of task-specific choices and correction of mistaken inferred preferences.
- How question ordering and example polish influence open-ended aesthetic choices.
- Whether concise interpretations improve fidelity without creating another approval burden.
- Behavior under deliberate delegation, impatience, contradictory answers and changing direction.
- Whether the implemented skill improves actual designs rather than only producing better-sounding questions.

The user's requested human leadership is a product choice for this pilot. The literature helps shape an effective interaction; it does not convert that preference into a universal rule for every user, task, or skill.

