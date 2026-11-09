# Independent review of skills-evaluation research

Review date: 2026-11-07. Scope: five consequential claims in `skills-evaluation.md` and its source ledger, checked against underlying papers and pinned public code. This is a bounded source review, not a benchmark rerun. No models, external code, or graders were executed.

## Verdict

Four claims are supported at the report's stated scope. The fifth—baseline isolation—needs a small distinction between the paper's protocol and the narrower cleanup observed in code. No demonstrated benchmark contamination or evidence overturning the report's central recommendation was found.

The code review strengthens the ACES contract claim beyond implementation documentation. It also confirms that the OpenSkillEval discrepancy persists through the inspected wrappers. Neither result justifies rescoring published experiments without their actual scorer revisions and traces.

| Claim | Assessment | Relevant limit |
| --- | --- | --- |
| ACES current accuracy excludes skill naming and computes five verdicts. | Supported by implemented scorer and staged verifier, not only docs. | Historical cap is documented; published aggregate was not rescored. |
| OpenSkillEval README and executing score formula differ. | Supported in pinned web-design path. | Five candidate dimensions may be absent; average is over those present. |
| SkillsBench size buckets do not prove causal benefits of shortening one skill. | Supported methodological reading. | Different tasks populate buckets; comprehensive bucket has five tasks. |
| SWE-Skills-Bench explicitly invokes the target and cleans pre-existing skills. | Activation supported in paper and proxies; cleanup qualified. | Inspected code specifically removes repository .claude trees, not every possible skill location. |
| Reusable-workflow example conflicts with requested paths and public score falls 100→12.5. | Supported across task, skill, verifier, CSV and reported trace analysis. | CSV is one configuration/requirement cell, not independent causal proof. |

## 1. ACES documented contract versus implemented contract

The [paper §4.3](https://arxiv.org/html/2608.20614) includes skill identification among five accuracy criteria. Current [guide lines 626–656](https://github.com/NVIDIA/SkillEvaluator/blob/d136a597c54784ad8a0ce28542c208602b397a5c/docs/tier3-live-evaluation.mdx#L626) explains its replacement and non-comparability.

More directly, [shared judge lines 620–632 and 740–777](https://github.com/NVIDIA/SkillEvaluator/blob/d136a597c54784ad8a0ce28542c208602b397a5c/src/skillevaluator/tier3/eval_core/llm_judge.py#L620) defines five outcome verdicts, ignores the deprecated identification argument, validates Boolean keys, and computes the fraction. The [staged verifier](https://github.com/NVIDIA/SkillEvaluator/blob/d136a597c54784ad8a0ce28542c208602b397a5c/src/skillevaluator/tier3/harbor/templates/eval.py#L2992) repeats that implementation at 2992–3157 and dispatches it at 3867–3877.

**Narrow improvement:** add those code locators to SKI-22. Calling the guide “implementation documentation” is accurate; the source now supports the stronger claim that this behavior is implemented. Do not infer a numerical correction to any paper aggregate.

## 2. OpenSkillEval score formula and wrapper follow-through

The [README scoring section](https://github.com/ALEX-nlp/OpenSkillEval/blob/d0e109283eee79216284cdf09ee59bf63239fb13/eval/webdesign-eval/README.md#L58) specifies weighted dimensions. The [judge lines 534–548](https://github.com/ALEX-nlp/OpenSkillEval/blob/d0e109283eee79216284cdf09ee59bf63239fb13/eval/webdesign-eval/code/vlm_judge_ext.py#L534) selects five candidate keys, omits absent dimensions, rescales pass rates, and averages available scores.

The [wrapper lines 137–155](https://github.com/ALEX-nlp/OpenSkillEval/blob/d0e109283eee79216284cdf09ee59bf63239fb13/eval/webdesign-eval/scripts/judge_single.sh#L137) merges metadata with the scorer object; [pipeline lines 588–602](https://github.com/ALEX-nlp/OpenSkillEval/blob/d0e109283eee79216284cdf09ee59bf63239fb13/eval/webdesign-eval/scripts/pipeline.py#L588) serializes results without recalculation.

**Assessment:** confirmed source discrepancy in this path. Prefer “up to five available dimensions” for maximal precision. It remains unknown whether a published trial used this exact revision and route.

## 3. SkillsBench length and quantity evidence

[Appendix F Tables 8–9](https://arxiv.org/html/2602.12670v4) partitions tasks by attached skill count and documentation size; it does not rewrite the same skill to randomized lengths. Bucket populations differ. The report's causal caveat is therefore warranted despite the paper's stronger “ablation” language.

**Assessment:** supported. An ideal skill-size cap, a maximum useful skill count, and the benefit of deleting an arbitrary paragraph remain unestablished. The report does not make those claims.

Appendix K and §5.1 distinguish task-specific from harness-bundled guidance. A no-task-skill baseline should not be presented as an agent receiving no other instructions or capabilities.

## 4. SWE activation and baseline cleanup

[Paper §§3.3–3.4](https://arxiv.org/html/2603.15401v2) describes explicit native activation and removal of pre-existing skill directories. [Claude proxy 160–175](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/src/proxy/claude_code_proxy.py#L160) and [Codex proxy 104–113](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/src/proxy/codex_proxy.py#L104) corroborate prompt-prefix activation in one-skill mode.

However, the inspected [lifecycle cleanup 936–945](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/src/orchestrator/lifecycle.py#L936) removes repository directories named `.claude`. Staging is selective at 516–632 and 703–741. This trace does not prove all possible native discovery surfaces were absent.

**Narrow correction:** say the paper reports cleanup; inspected code supports selective provisioning and .claude cleanup. No affected repository, contaminated trial, or changed score has been demonstrated. Discovery remains a different question from utility after explicit invocation.

This qualification was sent to the source author. It is evidence-scope refinement, not a claim that the benchmark's comparison is invalid.

## 5. Public reusable-workflow regression

The [task destinations](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/tasks/batch8/github-actions-templates.md) and [tests 18–36](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/tests/batch8/test_github_actions_templates.py#L18) require `ci/`; the [skill 211–244](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/skills/github-actions-templates/SKILL.md#L211) illustrates another location. The [Haiku CSV row 249](https://github.com/ControllableModel/SWE-Skills-Bench/blob/4d3450d9216a590a8726fcb3604b5143daca776b/results/final_results/claude__haiku-4-5_cells.csv#L249) records 100.00 versus 12.50.

[Paper §4.2 / Figure 5](https://arxiv.org/html/2603.15401v2) reports the displaced-output trace and 14 failing checks out of 16.

**Assessment:** supported as reported mechanism with corroborating artifacts. No local replay or independent full trajectory audit was performed. The study does not establish that templates generally hurt; it demonstrates a configuration-specific failure to preserve a requested destination.

## Residual limits

This review sampled five claims rather than auditing all 26 registry entries. Other papers, saved SkillClash records, public skill licenses, and the pivot-artifact case were not independently rechecked here. Paths and formulas were read, but runtime dependencies, model variability, scorer fallbacks, and full aggregate reconstruction remain outside scope.

The suggested corrections were communicated to the author; this reviewer did not edit the source dossier or its ledger.

