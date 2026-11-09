# Fundamentals skill library: first research pass

Research date: 2026-11-07 (Asia/Seoul).

Deep follow-up: [full research index](fundamentals-deep/index.md) and [revised synthesis](fundamentals-deep/synthesis.md). The initial survey below is retained as an earlier research snapshot.

Status: research and provisional recommendations. No skills created, replaced, installed, or evaluated in this pass.

## Decision

Keep both the taxonomy and individual rules revisable. Research should produce contextual decision guidance, examples, and verification methods before it produces permanent skill boundaries. The initial design/repository/architecture/writing categories are search areas, not a committed catalog.

Distinguish a broad research collection from the much smaller instructions an agent loads to complete a task. More collected knowledge does not automatically justify more injected instructions.

## Scope and method

Four subagents independently researched design, repositories, architecture, and writing. The coordinator researched skill authoring and evaluation, reconciled findings, and inspected this repository's existing research, refactoring, and audit skills. Sources included official standards and design systems, original research manuscripts, practitioner accounts, actual repository structures/manifests, and local ui.sh/Taster guidance.

This was a bounded foundational survey, not an exhaustive internet review. Repository commands and example flows were not executed; no comparative skills trial or user study was performed. Mutable repository branches, wikis, and local files were inspected without freezing revisions. Pin examples before treating them as maintained case studies. The DevRelay tools were unavailable in this session; no claim of community consensus is made.

## What changed from the initial proposal

| Initial framing | Evidence-informed revision |
| --- | --- |
| Collect best practices for each topic | Collect decisions, conditions, counterexamples, and ways to verify the result. |
| One UI/UX skill, or a fixed split into two | Experience design, visual direction, and implementation/verification are distinct capabilities; actual usage should determine packaging. |
| Repository structure and docs form one area | Contributor navigation, technical documentation, and change review have different triggers and overlap with architecture/writing. |
| Architecture plus a standard diagram pack | Select views by the question; include failure behavior and measurable change/quality scenarios. |
| Improve writing by removing AI style | Improve purpose, evidence, specificity, structure, and voice; treat generic prose as one editing failure. |
| Keep expanding research into skills | Retain broad sources separately; promote only guidance that improves real task outcomes. |

These are recommendations from the survey, not experimentally established skill boundaries.

## Design: durable requirements and contextual choices

### Concrete contradictions in existing guidance

Local ui.sh [typography guidance](/Users/jaeyong/.agents/skills/design/guidelines/typography.md:8) forbids bold headings and mandates InterVariable at line 17. Local Taster [brand guidance](/Users/jaeyong/Development/Github/taster/skills/taster/references/brand.md:21) treats Inter and other common faces as defaults to replace with IBM Plex, with a brand override. Atlassian's official [typography system](https://atlassian.design/foundations/typography) distinguishes brand and product fonts and uses bold heading tokens.

Inference: these are contextual house styles. Importing them as universal fundamentals creates contradictory instructions. Taster itself says a clean detector establishes only the absence of listed patterns, not good design: [local skill](/Users/jaeyong/Development/Github/taster/skills/taster/SKILL.md:131).

The inspected [Anthropic frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) connects visual choices to subject matter and allows brief-specific exceptions to generic-design warnings. Its changing list of aesthetic tells is an example of a mutable heuristic, not evidence that a style is inherently bad.

### Candidate guidance and supporting sources

- Frame the relevant journey around the user's outcome and handoffs. Incremental delivery remains compatible with understanding a whole problem. [GOV.UK service standard, point 2](https://www.gov.uk/service-manual/service-standard/point-2-solve-a-whole-problem).
- Justify information collection before choosing form layout. GOV.UK's default of one thing per page includes exceptions for repeated tasks; related questions can be grouped when research supports it. [Form structure](https://www.gov.uk/service-manual/design/form-structure), [question pages](https://design-system.service.gov.uk/patterns/question-pages/).
- Include correction paths and preserve answers. Review placement varies with transaction size. [Check answers](https://design-system.service.gov.uk/patterns/check-answers/).
- Choose empty-state content from its cause and available action. First use, no results, and errors need different treatment; small empty areas may not need illustrations. [IBM Carbon empty states](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states).
- Keep a standard's actual scope and exceptions. WCAG 2.2 AA target-size minimum has a 24-by-24 CSS pixel criterion and exceptions, including spacing and inline cases; that differs from a universal minimum-button-size slogan. [W3C explanatory guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

Visual appeal and task behavior need separate examination. NN/g describes observed cases where aesthetic reactions obscured interaction problems; this is practitioner evidence, not a controlled experiment conducted for this project. [Aesthetic–usability effect](https://www.nngroup.com/articles/aesthetic-usability-effect/).

Useful example candidates: grouped passport fields versus a multi-screen form; check answers → edit populated field → return; the same empty table after first use, filtering, completion, and missing permissions. These would need implementation and observation before becoming tested examples.

Packaging hypothesis: experience design, visual direction, and interface implementation/verification. Accessibility and content apply throughout. The supplied `ideas` skill is a picker implementation mechanism, not a source of design principles; its activation rules explicitly distinguish those jobs.

Coverage gap: strongest evidence here concerns service forms and enterprise interfaces. Consumer, commerce, editorial, game, and cross-cultural design need further sampling.

## Repositories: make the next change understandable and verifiable

Three contrasting examples undermine a universal folder tree:

| Repository | Observed maintenance surface | Interpretation |
| --- | --- | --- |
| [p-limit](https://github.com/sindresorhus/p-limit) | Root-level implementation, declarations, runtime/type tests, README, and recipes; its [manifest](https://raw.githubusercontent.com/sindresorhus/p-limit/main/package.json) aggregates validation and limits published files. | A small library can remain comprehensible with a flat structure. |
| [VS Code organization guide](https://github.com/microsoft/vscode/wiki/Source-Code-Organization) | Layers, contributions, runtime environments, and documented dependency directions. | Folder names matter because they reflect constraints; copying names does not reproduce those constraints. |
| [Rust](https://github.com/rust-lang/rust) | Compiler, library, tools/bootstrap, tests; its [contribution guide](https://raw.githubusercontent.com/rust-lang/rust/main/CONTRIBUTING.md) routes different work to specialized guides. | A compact entrypoint can make substantial distributed documentation navigable. |

These observations do not establish comparative productivity or prove the workflows pass.

[Diátaxis's workflow](https://diataxis.fr/how-to-use-diataxis/) explicitly treats its documentation structure as a guide, discourages empty four-section scaffolds, and recommends small improvements from which structure emerges. Its [compass](https://diataxis.fr/compass/) helps distinguish learning, task execution, reference, and conceptual understanding. This supports choosing documentation by reader need without prescribing a documentation website or directory layout.

[Google's review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html) addresses design, behavior, complexity, tests, and relevant documentation; its [review standard](https://google.github.io/eng-practices/review/reviewer/standard.html) favors improving code health without demanding perfection.

Candidate instructions: discover build/test/release entrypoints before reorganizing; identify ownership, runtime, API, and generated-output boundaries; document dependency rules a tree cannot express; verify documented commands against manifests and actual behavior when execution is in scope. The VS Code wiki and current manifest raise a package-manager consistency question, but this survey did not demonstrate a broken command.

Packaging hypothesis: repository maintainability, technical documentation, and change review may be separate capabilities. Compare against existing audit/refactor skills before adding overlap. Language-specific layouts belong in conditional references.

## Architecture: decisions, failure behavior, and useful views

[Parnas's original modularity paper](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf), pp. 1054–1057, contrasts decomposition by processing steps with hiding changeable design decisions. It also discusses implementation efficiency costs. A useful teaching exercise asks which callers and representations change when a storage format or algorithm changes; it does not require an interface around every detail.

[C4's diagram overview](https://c4model.com/diagrams) explicitly says to use only useful levels, often context and container. Its [FAQ](https://c4model.com/diagrams/faq) addresses arrow meaning and the maintenance cost of detail. Its [review checklist](https://c4model.com/diagrams/checklist) checks scope, purpose, relationships, and notation. Syntax-valid Mermaid alone would not meet those criteria.

[arc42 runtime guidance](https://docs.arc42.org/section-6/) recommends significant scenarios, including errors and external interactions, mapped to static building blocks; text is an acceptable form. Its [quality requirements guidance](https://docs.arc42.org/section-10/) asks for measurable scenarios. Our application: test a proposed design against a concrete failure or change, rather than praising it as scalable or modular.

[Nygard's ADR guidance](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) preserves context, status, and consequences, including superseded decisions. It is practitioner guidance, not controlled proof of ADR effectiveness.

Preserve disagreement: [Fowler's Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) emphasizes uncertain early boundaries and distribution cost, while acknowledging sparse evidence. [Tilkov's opposing argument](https://martinfowler.com/articles/dont-start-monolith.html) emphasizes known domains and independent delivery. A skill should ask which conditions apply instead of encoding either title as an unconditional rule.

The [rust-analyzer architecture guide](https://rust-analyzer.github.io/book/contributing/architecture.html) distinguishes internal representations, facade APIs, and process isolation. Selective manifest inspection corroborated only narrow dependency facts, not the entire architecture. This is a candidate case study for deliberate boundaries, not a crate layout to copy.

The [AWS Builders' Library on retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) explains retry amplification and why a timeout does not establish whether a side effect happened. A constructed payment example could trace success, timeout after commit, duplicate attempt, and reconciliation. This would be a teaching example, not an audited payment system.

Packaging hypothesis: one system-design capability with conditional diagram, decision-record, and distributed-failure references. Keep behavior-preserving refactoring distinct. Split diagram authoring only if it frequently appears as an independent task.

## Writing: improve meaning before surface style

Different genres require different outcomes. [Google's audience guidance](https://developers.google.com/tech-writing/one/audience) starts from reader knowledge gaps. [GOV.UK user-needs guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/) serves actionable service needs. [UNC's argument guide](https://writingcenter.unc.edu/tips-and-tools/argument/) emphasizes claims, appropriate evidence, and counterarguments. Requiring every essay to end in a task would overextend the service-writing guidance.

Style advice also needs exceptions. [Google permits passive voice](https://developers.google.com/style/voice) where actor identity is irrelevant or the object deserves emphasis. [Mailchimp distinguishes voice from situational tone](https://styleguide.mailchimp.com/voice-and-tone/). [Orwell's essay](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/) argues against prefabricated wording while allowing exceptions to its rules; it is an authorial argument, not empirical evidence for banned-word lists.

Original empirical sources complicate the claim that AI writing is simply bad:

- [Doshi and Hauser's manuscript](https://arxiv.org/pdf/2312.00506) studies GPT-4 starting ideas for short stories: average creativity-related ratings improved while collective similarity increased. It concerns assisted eight-sentence stories and online participants, not arbitrary full articles or professional authors.
- [Agarwal, Naaman, and Vashistha](https://arxiv.org/html/2409.11360v3) studied GPT-4o suggestions with 118 Indian/US participants. They report culturally homogenizing effects under that setting; this does not establish effects for all cultures or models.
- [Noy and Zhang's March 2023 working paper](https://economics.mit.edu/sites/default/files/inline-files/Noy_Zhang_1_0.pdf) reports productivity and rated-quality benefits on bounded professional writing tasks. This pass inspected the earlier working paper, not the later published version; do not mix their sample or effect sizes. Context-heavy real work is a generalization limit.

Candidate workflow, our synthesis: diagnose reader/purpose/source material; revise claims, evidence, omissions, and structure; then edit specificity, rhythm, repetition, and tone. Preserve supported detail and authorial choices instead of polishing them into interchangeable prose.

Original teaching pair: “Our powerful workflow transforms team productivity” → “Review a pull request, assign an owner, and see unresolved comments in one view.” The second version is only acceptable if those capabilities are real; specificity must not become fabrication.

Packaging hypothesis: one writing skill with article/argument, technical-documentation, and product-content references initially. Evaluate usefulness, accuracy, coherence, and voice, not whether a detector calls it human.

## What belongs in a skill, and how to update it

[Agent Skills authoring guidance](https://agentskills.io/skill-creation/best-practices) recommends coherent task units, non-obvious knowledge, moderate detail, context-sensitive control, and progressive disclosure. Its [evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills) recommends realistic cases and comparisons against no skill or an earlier version. These support a compact entrypoint with references loaded for actual needs.

Two original benchmark papers show why collecting advice is insufficient:

- [SkillsBench v4](https://arxiv.org/html/2602.12670v4) reports substantial aggregate gains from curated skills across 87 tasks and 18 configurations, with focused bundles outperforming exhaustive ones. It studies terminal/container tasks and notes selection, generalization, and attribution limits; it does not prove aesthetic or writing improvement.
- [SWE-Skills-Bench v2](https://arxiv.org/html/2603.15401v2) reports no significant effect for 92 of 98 sampled skills and a small aggregate improvement. It documents template anchoring that displaced explicit task paths. Requirements were derived from skills, each paired evaluation ran once per configuration, and verifier/coverage limits remain.

These are different samples and protocols, not directly contradictory effect estimates. Neither is proof of how this proposed library will perform. Both motivate local comparison rather than assuming usefulness from the presence of a skill.

Proposed evidence record, kept only where it changes a decision:

| Field | Purpose |
| --- | --- |
| Guidance and intended decision | State what the agent should do differently. |
| Source, locator, date/version | Make the basis inspectable and refreshable. |
| Evidence type and applicable context | Separate standards, empirical results, documented conventions, practitioner experience, and taste. |
| Counterexample or competing approach | Prevent a contextual default becoming an unjustified prohibition. |
| Trial and observed result | Show whether the instruction improves outcomes and respects user constraints. |

Suggested progression:

1. Research realistic tasks across the initial areas; let concepts and overlaps emerge.
2. Draft the smallest coherent instructions that address demonstrated weaknesses; keep source detail in references.
3. Compare against the same tasks without the new skill, including a context where the default advice should not apply.
4. Revise from traces and artifacts; retain good changes and remove instructions causing irrelevant work or regressions.
5. Refresh when standards, dependencies, evidence, user needs, or observed outcomes change. Split/merge skills when actual routing and task coherence justify it.

Trials should preserve comparable model/tool/task settings, record cost and time, and use task-specific criteria. For design and writing, blinded comparison and human judgment can complement behavioral checks; deterministic tests alone cannot establish taste or voice. Avoid loading unrelated skill stacks in a baseline, and do not treat one successful run as causal proof.

## Concrete next research slice

Use one realistic end-to-end product task as a pilot: design a settings flow with failure/recovery states, document its system boundaries, implement or inspect its repository paths, and explain a consequential design choice. Evaluate the relevant capabilities separately before deciding which deserve independent skills. Keep a contrasting article-writing task so service-content assumptions do not silently dominate the writing foundation.

This pilot is a recommendation only. This research pass has not executed it or frozen the library taxonomy.
