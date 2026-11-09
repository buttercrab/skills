# Skills as interventions: evidence, composition, and evaluation

Research date: 2026-11-07. Scope: primary skill-evaluation studies, selected public evaluation artifacts, existing skill libraries, and the validity of tests for a fundamentals library. This report is research, not a newly authored skill or an executed benchmark.

## Main finding

A fundamentals library should separate knowledge worth retaining from instructions worth injecting. Research can justify keeping a source, explanation, or case study without justifying a mandatory procedure. The relevant test is whether the instructions improve a particular agent's work under realistic constraints, preserve the user's task, and compose with its other guidance.

The evidence supports four distinctions: discovery versus use after activation; task success versus adherence to an opinionated workflow; artifact quality versus process compliance; and isolated skill behavior versus interaction with other skills. Those are separate questions, not interchangeable metrics.

The source registry has 26 substantively inspected source units. Several units are explicitly multi-file repository cases. They are not 26 independent experiments or independent organizations. The registry records versions, locators, evidence classes, context, and limits. The studies below were read in their methods, results, relevant appendices, and limitations; repository inspection was selective. No external code was executed, no skill was installed, and no new paired trials were run.

## 1. What the empirical studies actually measure

| Study | Design and inspected evidence | What it supports—and what it does not |
| --- | --- | --- |
| [SkillsBench v4](https://arxiv.org/html/2602.12670v4), SKI-01 | 87 tasks, 18 model/harness configurations, matched skill/no-task-skill arms; deterministic verification; §§3–6, Appendices F/J/K/N. | Curated procedural packages helped on this selected terminal-task distribution. Length and skill-count comparisons group different tasks; they do not isolate the causal effect of shortening one skill. Harness-bundled skills remain part of the harness. This is not evidence for a universal size cap or visual-design quality. |
| [SWE-Skills-Bench v2](https://arxiv.org/html/2603.15401v2), SKI-02 | 98 public skills, ten reverse-engineered requirements each, four configurations; pinned repositories; skill explicitly invoked; paper reports cleanup of preexisting skills; §§3–5. | Most sampled skills had no statistically detected benefit; that does not establish zero effect. Requirements derive from the skills. One run per requirement/configuration limits noise assessment. It tests post-activation utility, not discovery. Cross-review found repository `.claude` cleanup and target staging in code; exhaustive baseline isolation remains unestablished, without demonstrated contamination. |
| [OpenSkillEval v2](https://arxiv.org/html/2605.23657v2), SKI-03 | 677 artifact-derived tasks, 30 adoption-filtered skills, five artifact categories. VLM judgments and interaction/data checks; §§2–4, Appendix A. | Relevant to multimodal quality, cost, and observed workflow use. Front-end targets come partly from design-award/landing-page sources. Human reviewers assessed cases and score/rationale reasonableness under the same rubrics; this is not independent user testing or proof of design quality across genres. |
| [A Framework for Evaluating Agentic Skills at Scale](https://arxiv.org/html/2606.17819), SKI-04 | Approximately 500 skills and 1,000 generated tasks; separate instruction-following and goal-completion rubrics; one Sonnet judge; §§2–6. | Skills encode choices absent from a baseline; the paper explicitly notes instruction-following gains are partly favored by construction. It reveals relevance and excludes difficult environments such as existing repositories, MCP, multi-turn/stateful work. A high combined score does not independently prove better general engineering. |
| [ACES](https://arxiv.org/html/2608.20614), SKI-05 | Static scans of 145 skills; live subset 58/64 production skills, 947 scored paired cases; mixed process/outcome metrics; §§4–7 and appendices. | Scan quality and live behavior differ. Headline composite lift includes skill-use/process criteria. Creative domains are underrepresented; live human/inter-judge calibration remains unmeasured. Current implementation changed the accuracy contract, so older published metrics require revision-aware interpretation; see §2. |
| [One Skill Too Many v2](https://arxiv.org/html/2610.11647), SKI-06 | Reconstructed public installations; 312 confirmed similar-skill pairs, three main models, additional platform check; completion and exclusive-core-function fidelity; §§3–6. | Co-installation can change which guidance runs while tasks still pass. Public installations omit private skills. First-read identity is observed; a separate guard experiment intervenes there. Individual configuration/pair cells mostly ran once, and core functions are extracted/normatively selected. |
| [SkillClash v1](https://arxiv.org/html/2610.25064), SKI-07 | Six-rule synthetic skill pairs for 16 jobs; controlled conflicts and examples; rule checkers and achievable reference outputs; §§3–7 and appendices. | Useful mechanistic evidence that worked examples can displace compatible rules when both skills are loaded. The synthetic, system-injected setting removes selection and is not a natural installed-skill distribution. Correct combined examples helped here; merging everything into one universal skill is not established. |

These results should not be pooled into a universal “skills help by X%” claim: selection, tasks, activation, baseline state, scorers, and aggregates differ. The same distinction matters locally. A style preference can be valuable to a user even when ordinary task pass rates stay constant, while perfect procedure adherence can coexist with a poor result.

## 2. Going beyond papers: scorer and documentation drift

### Outcome scoring must not reward merely naming the intervention

The ACES paper's accuracy definition includes identification of the correct skill. The pinned current [SkillEvaluator runtime guide](https://github.com/NVIDIA/SkillEvaluator/blob/d136a597c54784ad8a0ce28542c208602b397a5c/docs/tier3-live-evaluation.mdx#L626-L656), SKI-22, explicitly says the older `SKILL_IDENTIFIED` criterion capped an otherwise correct skill-free baseline at 0.8. Its new contract grades both arms using five outcome criteria without that condition. The old and new scores are declared non-comparable.

Implication: keep activation metrics for diagnosis, but calculate outcome lift from a symmetric rubric. Do not use a skill-reading requirement as evidence that task quality improved. This finding does not quantify how much the paper's entire aggregate changes under rescoring; that would require the frozen traces and exact grader reruns.

The same guide documents evidence budgets, omitted history, and exclusion of lift metrics when the two arms fall back to different judge models. Those details make scorer configuration part of the experimental artifact, rather than an incidental CLI setting.

Independent cross-review also corroborated the new criteria in [the judge implementation](https://github.com/NVIDIA/SkillEvaluator/blob/d136a597c54784ad8a0ce28542c208602b397a5c/src/skillevaluator/tier3/eval_core/llm_judge.py#L620-L632) and [staged verifier](https://github.com/NVIDIA/SkillEvaluator/blob/d136a597c54784ad8a0ce28542c208602b397a5c/src/skillevaluator/tier3/harbor/templates/eval.py#L3099). This strengthens the current-contract observation; it still does not rescore the paper.

### A README is not the executing score formula

At OpenSkillEval revision `d0e109283eee79216284cdf09ee59bf63239fb13`, its [web-design README](https://github.com/ALEX-nlp/OpenSkillEval/blob/d0e109283eee79216284cdf09ee59bf63239fb13/eval/webdesign-eval/README.md#L58-L76) describes eight weighted dimensions. The inspected [judge code](https://github.com/ALEX-nlp/OpenSkillEval/blob/d0e109283eee79216284cdf09ee59bf63239fb13/eval/webdesign-eval/code/vlm_judge_ext.py#L534-L548), SKI-23, averages five available dimensions. The shell wrapper injects metadata, and the pipeline merges results without recomputing that formula. This is a confirmed documentation/implementation discrepancy in the inspected path, not proof that published experiments used this exact revision/path.

Implication: preserve scorer code revisions and reward definitions alongside benchmark outputs. A metric named “overall” does not define what it measures.

## 3. Concrete instruction-to-outcome case studies

### Case A: a useful capability gap is a specific artifact mechanism

The SkillsBench [sales-pivot task](https://github.com/benchflow-ai/skillsbench/blob/f860ecf02ef53412a030f8661c83d644b739ff01/tasks/sales-pivot-analysis/task.md) requires actual Excel pivot tables, not merely numbers arranged like one. Its [skill](https://github.com/benchflow-ai/skillsbench/blob/f860ecf02ef53412a030f8661c83d644b739ff01/tasks/sales-pivot-analysis/environment/skills/xlsx/SKILL.md) explains pivot API construction; its [verifier](https://github.com/benchflow-ai/skillsbench/blob/f860ecf02ef53412a030f8661c83d644b739ff01/tasks/sales-pivot-analysis/verifier/test_outputs.py) inspects pivot fields and aggregation. These files form SKI-26. Inspection supports the task/skill/verifier alignment, while the paper—not a rerun here—supplies the reported outcome comparison.

Candidate lesson: retain non-obvious artifact semantics and verify them directly. Before generalizing the skill's very strong library-specific cache guidance, check supported library versions. A worked example can solve a real gap and still contain conventions that should not become timeless rules.

### Case B: a correct template can be wrong for the user's destination

SWE-Skills-Bench's pinned [batch8 task](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/tasks/batch8/github-actions-templates.md) names `ci/` destinations. The sampled [skill](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/skills/github-actions-templates/SKILL.md#L211-L244) includes `.github/workflows/` in its reusable-workflow example. The [tests](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/tests/batch8/test_github_actions_templates.py#L18-L36) require the task's paths. The public [Haiku cell data](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/results/final_results/claude__haiku-4-5_cells.csv) records batch8 falling from 100 to 12.5. This is SKI-24; path-displacement causality comes from the paper's trace analysis, not inference from CSV alone.

Candidate lesson: label example paths and constants as replaceable, and use a test whose requested destination intentionally differs. General-purpose skills should not quietly redefine the user's deliverables.

### Case C: examples can suppress compatible requirements

For SkillClash's commit-message pair, the pinned [A](https://github.com/prazmara/skillclash/blob/2c48d277dbf7a959dd802217ac80ab50da42df8f/skills/commit/A.md) and [B](https://github.com/prazmara/skillclash/blob/2c48d277dbf7a959dd802217ac80ab50da42df8f/skills/commit/B.md) define competing first lines plus largely compatible body requirements. In the [public GPT-4.1 records](https://github.com/prazmara/skillclash/blob/2c48d277dbf7a959dd802217ac80ab50da42df8f/runs/gpt41/diag.jsonl), task 0 under `AB` keeps B's shape while omitting A's exclusive fields. SKI-25 inspected the actual request, output, and saved rule flags; it is not a local model rerun.

Candidate lesson: include composition cases with compatible-but-easy-to-lose requirements, not only obvious contradictions. These records also emit a tested-status claim without test evidence in the supplied request. A formatting checker can establish format adherence while leaving factual grounding untested; do not equate those outcomes.

### Case D: a completed handoff can still violate an installed convention

One Skill Too Many's Figure 1 compares a handoff/checkpoint skill forbidding git-state changes with a similar skill that commits. Both complete the broad handoff task, but only one preserves the intended constraint. The source is SKI-06; this case was inspected in the paper's abridged trace, not independently replayed.

Candidate lesson: define which user/project constraints must survive the workflow and score them independently. A test that only checks the resulting handoff file would miss the important distinction. The skill's own preferences must still yield to the user's current authorization and task.

### Case E: attractive output is not one scalar capability

OpenSkillEval's inspected visual rubric uses screenshot-based appearance checks, while its interaction scores come from a separate eval report. It crops/truncates image bundles and averages available dimensions. SKI-23 establishes these implementation details. It does not establish accessibility, comprehension, or completion for real users.

Candidate lesson: a design skill needs distinct checks for content/interaction/state behavior, accessibility, and visual direction. Do not let excellent screenshots compensate arithmetically for a broken critical task; use task-specific non-compensable requirements where the user's outcome demands them.

## 4. What existing skill libraries teach—and where their advice conflicts

The following are inspected authoring patterns, not measured rankings of library quality.

| Sample | Observed mechanism | Candidate use and caution |
| --- | --- | --- |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/SKILL.md), SKI-16 | Iterative examples, traces, human review, baseline comparisons, optional blind comparisons, trigger optimization. | Useful authoring loop; broad trigger encouragement and repeated tuning need false-positive tests. Reusing the same holdout to choose revisions weakens its role as a final untouched test. |
| [Anthropic comparator and grader](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/agents/comparator.md), SKI-17 | Anonymous A/B outputs, task-derived rubrics, evidence-backed assertions, critique of weak tests. Comparator urges decisive winners. | Blind identity helps, but cannot remove order or stylistic bias. Preserve meaningful ties and uncertainty for near-equal outputs rather than forcing a winner. |
| [Superpowers writing-skills](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/writing-skills/SKILL.md), SKI-18 | Baseline failures, pressure scenarios, minimal instruction, repetitions, observed predicate-based conditions. Strong prohibitions for discipline failures. | Valuable attention to actual failure modes. Its absolute process requirements and firsthand wording claims are conventions/experience, not universal empirical laws. |
| [Superpowers debugging](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/systematic-debugging/SKILL.md), SKI-19 | Root-cause investigation, comparison, hypotheses, implementation; companion completion skill demands fresh evidence. | Supplies operational behaviors. Scale investigation/verification to the claim and task; do not import all “always” language into unrelated work. |
| [Vercel React rules](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/react-best-practices/SKILL.md), SKI-20 | Priority-ordered rules with incorrect/correct examples and optional detailed files. | Strong packaging example. Individual performance claims need workload/version evidence; a priority label is not a measurement for the current app. |
| [Vercel web-design-guidelines](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/web-design-guidelines/SKILL.md), SKI-21 | Tiny entrypoint fetches a mutable remote rules document each review. | Freshness is useful, but reproducibility requires recording which content was applied. Fetching an external instruction document is not permission to expand task scope. |

A useful detail in Vercel's [barrel-import rule](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/react-best-practices/rules/bundle-barrel-imports.md): its slogan recommends direct imports, but its Next.js path preserves standard imports with package optimization, and it warns about missing deep-import types. This is a good reason to keep explanation and exceptions reachable, rather than extracting only a one-line ban.

The [Agent Skills specification](https://agentskills.io/specification), SKI-12, defines packaging and progressive disclosure. Its [best-practices guide](https://agentskills.io/skill-creation/best-practices), SKI-13, recommends coherent task units and non-obvious knowledge. Those are interface/authoring guidance, not controlled proof that a particular library's rules improve outcomes. The [evaluation guide](https://agentskills.io/skill-creation/evaluating-skills), SKI-14, recommends realistic paired cases; the [description guide](https://agentskills.io/skill-creation/optimizing-descriptions), SKI-15, includes near-miss negatives and held-out queries. Apply the general methods without treating its example sample sizes or thresholds as validated constants.

License observations: Superpowers' inspected LICENSE is MIT; Vercel's README and React frontmatter declare MIT; Anthropic's pinned README reports Apache 2.0 including recently relicensed document skills; SkillEvaluator's inspected LICENSE is Apache 2.0. Some root LICENSE fetches returned unavailable results, so declarations are distinguished from verified per-file terms. No third-party skill text is copied into a new skill in this research.

## 5. Judging the judges

[MT-Bench's original study](https://arxiv.org/html/2306.05685v4), SKI-08, tests position sensitivity and repeated-list verbosity attacks; it also notes limited evidence for self-preference. Its agreement figures concern those models and conversational tasks. [Length-Controlled AlpacaEval](https://arxiv.org/html/2404.04475v2), SKI-09, models length as a confounder and treats crowd preference as a silver standard. Neither establishes that equal-length responses are always preferable or that crowd preference equals factual accuracy.

[Judging the Judges (2026)](https://arxiv.org/html/2604.23178), SKI-10, measures several mitigations with controlled style/length pairs; assumptions about semantically equivalent pairs and mandatory ties affect interpretation. [Reliability without Validity](https://arxiv.org/html/2606.19544), SKI-11, distinguishes repeated consistency from agreement and bias. It finds small verbosity association under its chosen rubric, unlike earlier settings. The implication is rubric- and population-specific calibration, not a timeless claim that every judge favors length.

For writing and design, the owner/user's actual criteria need explicit representation. A judge trained to favor polished conventional outputs can punish a distinctive but appropriate solution. Conversely, distinctiveness alone can conceal missing content or unusable interaction. These are risks to test with deliberately constructed comparisons; this survey does not measure their prevalence in the proposed library.

## 6. A realistic evaluation plan for a fundamentals library

The plan below is a research-derived proposal, not an executed experiment or a requirement that every small change run an elaborate harness.

### Establish the contribution before choosing a score

For a proposed skill, name the behavior it is supposed to improve. Is it supplying a forgotten procedure, a project convention, a reasoning lens, or a tool capability? Record what an otherwise capable agent does without it. If the ordinary agent already handles a behavior well, research may belong in references or human explanation instead of active instructions.

Use tasks drawn independently from the instructions, ideally real requests and artifacts. Include at least one context where the attractive default should be rejected: a dense expert interface, a tiny flat repository, a justified passive sentence, or an intentionally local implementation without a reusable abstraction. These evaluate judgment rather than rote compliance.

### Keep the comparison attributable

Hold prompt, input artifacts, permissions, model settings, tools, dependency state, and resource budget fixed. Record every discoverable skill and baseline policy. A “no target skill” baseline may still include host instructions and unrelated installed skills; describe it accurately. Use clean workspaces and prevent the target skill from leaking through a copied project guide.

Evaluate both explicit invocation and natural discovery. The first tests the contents once loaded; the second tests whether the description selects it when useful. Near-miss prompts test false positives. A broad description that improves recall while loading irrelevant obligations may be a regression.

Use repeated trials appropriate to observed variability and cost. Analyze by task, not as if thousands of correlated assertions were independent tasks. Report differences and uncertainty, including failures, timeouts, missing artifacts, and unevaluated cells. Reordering arms helps limit time-dependent service effects; preserve provider/model versions and avoid silently changing graders between arms.

### Use a scorecard before a composite

| Dimension | Useful observation | Failure a single overall score can hide |
| --- | --- | --- |
| User outcome | Task-specific functional/semantic checks | A beautiful, compliant artifact that does not solve the task. |
| Constraint fidelity | Explicit user/project constraints and permitted scope | Successful output accompanied by unrequested restructuring or side effects. |
| Reasoning/decision quality | Relevant alternatives, conditions, source/implementation fit | A fluent explanation defending an arbitrary default. |
| Artifact craft | Genre-specific human assessment and objective checks | Generic polish, factual errors, inaccessible or broken states. |
| Operational cost | Time, tool calls, tokens, dependencies, user interruptions | Modest improvement bought with disproportionate work. |

Some requirements should be gates: preserved user data, a working critical flow, a correct public contract, or factual support for an important claim. Passing many minor style checks should not compensate for failing such a requirement. Which gates matter depends on the requested task; do not invent production obligations for a concept sketch.

Keep important invariants even when both arms always pass them. A nondifferentiating check can still detect a later regression; distinguish guardrails from checks intended to measure marginal skill benefit.

### Inspect the evaluator itself

Write small calibration pairs: an accurate concise answer versus polished unsupported prose; a visually strong page with broken recovery versus a plainer complete flow; a clean diagram with a false dependency versus a less elaborate accurate one. Include a true tie and identical outputs. Randomize labels, swap order, and check whether explanations cite observable evidence. Preserve disagreements instead of averaging them away.

Use human review where taste, voice, cultural context, or meaningful usefulness is central. Domain experts and intended users answer different questions from general annotators. Automated checks can validate text reflow, chart values, keyboard access, file schemas, or endpoint behavior but cannot settle every qualitative choice.

### Test composition, then change one thing at a time

Test the skill alone, with its necessary support, and with a plausible overlapping skill. Check all important compatible constraints, not just whether the target was read. Treat examples as active instructions: verify they demonstrate the current rule and remain appropriate when filenames, brands, technology, genre, or permissions differ.

When a failure appears, separate missing knowledge, unclear trigger, overly rigid workflow, misleading example, unavailable tools, and bad grader. Fix the responsible cause. A bigger skill is not a default remedy. Hold back fresh tasks from repeated authoring cycles; a reused “test” set becomes development data.

## 7. Consequences for the library's organization and maintenance

The evidence does not identify an ideal number of skills. Keep domains broad enough for useful research and task entrypoints narrow enough for precise activation. Let observed independent requests, loading overhead, composition failures, and shared artifacts determine splits.

Candidate separation: research sources/cases; active decision instructions; specialized recipes/tools; evaluation tasks and observed results. This is conceptual separation, not a mandate for four directories in every skill. A short skill may need no additional files.

Promote a rule with a provenance note, context, and counterexample. Mark whether it is a standard, documented convention, measured finding, expert judgment, or personal preference. Keep exact standards and tool-specific claims versioned. A good example can remain useful even when its particular framework recommendation expires.

Reevaluate when a model/harness update changes baseline behavior, a tool/library invalidates a recipe, a new real task reveals an exception, or overlapping skills are added. Remove rules that no longer improve outcomes. A skill should be allowed to shrink, split, merge, or retire.

## 8. Search record, exclusions, and remaining gaps

Query families included: skill utility benchmarks and evaluation frameworks; skill conflict/composition; official authoring/discovery/evaluation docs; public skill libraries and evaluation artifacts; LLM judge position/style/length bias and validity. Citation trails from the original two papers led to OpenSkillEval, Tessl, ACES, and the two conflict studies. Paper case descriptions were followed into actual public tasks, skill text, verifiers, result CSVs, scoring code, and saved outputs.

Inspected repositories were pinned through GitHub metadata at these revisions: Anthropic `2c5958ecac7cee2b583967a2c4981d0f4a75c579`; Superpowers `22f0b463e7a5e579904dd6211a520321035526f7`; Vercel agent-skills `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62`; NVIDIA SkillEvaluator `d136a597c54784ad8a0ce28542c208602b397a5c`; SkillsBench `f860ecf02ef53412a030f8661c83d644b739ff01`; SWE-Skills-Bench `4d3450d9216a590a8726fcb3604b5143daca776b`; OpenSkillEval `d0e109283eee79216284cdf09ee59bf63239fb13`; SkillClash `2c48d277dbf7a959dd802217ac80ab50da42df8f`. These are research snapshots, not claims that the studies ran these exact revisions.

Search-discovered mirrors, news summaries, directory popularity, Reddit anecdotes, and surveys were not treated as independent evidence for effectiveness. OpenSkill's self-evolution project was a discovered adjacent topic, not evaluated in this lane. Failed root LICENSE paths were not interpreted as an absence of licensing. Large trajectory collections were selectively sampled; no aggregate was independently recomputed.

Remaining gaps: independent reproductions of the skill papers; real-user longitudinal quality/productivity; intended-user evaluations of design/writing; multi-turn collaborative skill use; cross-cultural evaluation rubrics; discovery across a realistic private catalog; causal same-task ablations of rule length, number, examples, and references; robust security review of retrieved reference chains. None of the inspected results establishes that a universal fundamentals compendium outperforms a small collection of task-focused guidance.
