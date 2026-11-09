# Independent source check: verification research

Reviewed 2026-11-07. Scope: five consequential claims in verification.md and its ledger, checked against the underlying primary sources. No tests, benchmarks, restores, incident interventions or external code ran. Only this review file was written.

## Result

Four claims are supported at their stated historical/documentary boundaries. The performance comparison is supported with a qualification and a source-locator correction. None of these sources independently verifies current production behavior or proves that a proposed skill improves outcomes.

## 1. Cloudflare: functional checks did not cover execution cost or recovery access

**Report location:** verification.md, case 1; ledger VER-13.

**Judgment: supported.** The operator account distinguishes approved/tested rule delivery from the staged software process. It attributes resource exhaustion to backtracking and lists missing CPU protection/detection. Recovery was obstructed by dependence on Access; termination and single-city checks are reported interventions, not merely coincident metrics. [Primary source, “What went wrong” items 1–5 and 9; timeline 14:00–14:52; “How Cloudflare operates”](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/).

**Precision recommendation:** “the rule SOP allowed global delivery without the staged software rollout” is clearer than “bypassed,” which can imply someone violated procedure. The source explicitly describes following the existing process. The report already presents the operational teaching as an inference, which is appropriate. Do not promote its emergency-path counterexample into a claimed observation from this incident.

## 2. GitLab: logical backups were absent, but recovery data was not universally absent

**Report location:** case 2; VER-14.

**Judgment: supported.** The account separates failed version-selected logical backups, rejected notification mail, wiped replicas, a usable LVM snapshot, and staging's removed webhooks. It reports reconstructing webhooks from a separately restored snapshot; slow staging disks constrained copying. Regular restore-test ownership was explicitly missing. [Primary source, “Database backups using pg_dump,” “LVM snapshots,” “Recovering GitLab.com,” root-cause Problem 2 items 4–8](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/).

**Boundary preserved:** the report correctly avoids saying that all backups were absent or that webhook removal made final recovery impossible. Backup creation failure, silent alert failure, application-semantic completeness and elapsed recovery time remain distinct observations. This is the operator's reconstruction, not an independent causal replication.

## 3. SQLite: coverage/defensive-code tension is explicitly documented

**Report location:** case 3, coverage/fuzzing claim; VER-25.

**Judgment: supported.** The guide expressly discusses the tension, says defensive code should be retained, and describes differing macro forms for normal, assertion and coverage runs. Coverage statements apply to the core/default configuration, with extensions excluded. [Primary source, §§4.1.6, 7 and 7.2](https://www.sqlite.org/testing.html).

**Boundary preserved:** this is a project-specific documented strategy. It does not show that high coverage causes vulnerability in arbitrary codebases, or that defensive paths may be excluded silently from any project metric. The report's recommendation to preserve a defense is sensible synthesis, not a measured effect of its proposed exercise.

## 4. SQLite: a coverage-instrumented build and delivered build supply different evidence

**Report location:** case 3, delivery compiler options; VER-25 §7.5 locator.

**Judgment: supported.** Section 7.5 explicitly distinguishes checking the suite's coverage from recompiling with delivery options and rerunning; it also calls for matching outputs. [Primary source, §7.5](https://www.sqlite.org/testing.html).

**Uncertainty:** the guide was read, not the actual release process executed. Documentation of a second run is not evidence that every release/configuration currently receives it. The report makes the right distinction by describing documented practice rather than a freshly observed pass.

## 5. Performance: smaller reference-input variation is not absence of consequential bias

**Report location:** case 6; VER-11 and VER-12.

**Judgment: supported with qualification.** Mytkowicz et al. explicitly use train inputs for their repeated SPEC experiments. [Original paper, §3.1, printed p.267 / physical PDF p.3](https://www2.ccs.neu.edu/racket/Performance/mytkowicz.pdf).

Kalibera/Jones reproduce training-input sensitivity and find smaller reference-input variation, yet report statistically significant mean slowdowns of 3.3% and 6.8% for two reference benchmarks. Their training runs omit LTO; reference runs use LTO, on one platform. [Accepted manuscript, §8.2, physical PDF pp.8–9](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf).

**Required locator correction:** code-layout results are in §8/§8.2, not §7. The related-work paragraph points to §7.2, but the direct experimental section is §8.2 in the inspected manuscript.

**Recommended wording:** “Their reference-workload experiment found less layout-induced variation overall, while retaining significant mean shifts for two benchmarks; platform and compilation details also differed.” This avoids attributing the contrast solely to input size. The two papers do not support either a universal dramatic-bias estimate or a claim that full-sized workloads remove meaningful bias.

The report's hierarchy/repetition recommendation remains appropriate. A narrow noise interval cannot eliminate a systematic shift, and many measurements from one setup do not establish portability to another setup.

## Changes relayed to the coordinator

1. Correct the Kalibera/Jones layout locator to §8.2.
2. Preserve the distinction between variation and mean shifts in the performance comparison, including compilation/platform scope.
3. Optionally replace Cloudflare “bypassed” with “the rule SOP allowed” to avoid implying unauthorized procedural deviation.

No edits were applied to the source dossier or ledger by this reviewer.
