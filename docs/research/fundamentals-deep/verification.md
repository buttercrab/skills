# Verification fundamentals: testing, debugging, reliability, security, and performance

Research date: 2026-11-07 (Asia/Seoul). Research artifact only; no skills installed or changed.

## What the evidence changes

The useful capability is selecting evidence that can distinguish a consequential defect from a plausible alternative explanation. Running more tests, collecting more telemetry, or increasing a score can help, but none supplies the missing definition of correct behavior.

This suggests distinct task capabilities for test design, causal debugging, performance measurement, and risk-based security/reliability verification. They share an evidence discipline but have different inputs, stopping conditions, and costs. This taxonomy is a research hypothesis, not a final catalog.

The [source ledger](verification.sources.jsonl) records inspected sections, evidence classes, versions, limitations, and failed access. A paper, a standards document, and a company's retrospective are not interchangeable kinds of evidence. No source code, test suite, benchmark, production system, or incident was executed or reproduced for this investigation.

## Investigation method and evidence map

The research followed several trails rather than collecting introductions to tools:

| Trail | Materials inspected | Question pursued |
| --- | --- | --- |
| Test correctness | Oracle survey, original QuickCheck, metamorphic-testing survey, Csmith, ASan | What makes a generated input or assertion meaningful? |
| Test-suite quality | Original real-fault/mutation and coverage studies; Google practice; SQLite | Which metrics are supported proxies, and where do they fail? |
| Nondeterminism | Apache flaky-test study, Google measurements and mitigations | Does a passing rerun explain the failure or only suppress it? |
| Causal diagnosis | Original author's delta-debugging chapter; Google troubleshooting; incident interventions | What observation could falsify the current explanation? |
| Recovery and release | Cloudflare, GitLab, GitHub first-party postmortems; FoundationDB and Jepsen | Which boundaries make component-level proof insufficient? |
| Performance | Mytkowicz; Kalibera/Jones; Gregg; benchmark tool documentation | What is the experimental unit, workload, bottleneck, and uncertainty? |
| Security | Released ASVS requirements, SSDF 1.1, OWASP threat modeling | What is applicable to this system and who owns verifying it? |

These are purposive examples, not a representative statistical sample of engineering practice. Multiple Google publications remain one organizational family; repository documentation and related company papers are not independent corroboration of their production claims.

## Six detailed cases

### 1. Cloudflare: a tested configuration change became a global performance failure

Cloudflare reports that its July 2019 WAF change passed review and tests; its rule SOP allowed global delivery without the staged software rollout. A backtracking expression exhausted CPU; an earlier refactor had removed protection, tests lacked excessive-CPU detection, and recovery access depended on the affected service. Its account includes CPU/strace evidence, recovery after disabling WAF, and positive/negative tests in one city before re-enabling. Those interventions strengthen the reported diagnosis, but this research did not reproduce them. [VER-13: timeline and “What went wrong”](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/).

**Teaching decision:** a proposed rule test should ask what property could fail under real inputs and what rollout bounds its consequences. Matching expected strings is insufficient for a resource-sensitive rule. Configuration and policy changes deserve verification proportional to their execution effects.

**Counterexample:** demanding full staged delay for every emergency protective update can impose another risk. Preserve an explicit emergency path and its compensating evidence rather than a universal prohibition on global changes.

**Candidate exercise:** give the agent a passing functional suite, a slow nonmatching input, and a rule-distribution diagram. Success means identifying complexity and rollout/recovery dependencies, not merely adding more matching examples.

### 2. GitLab: backup generation, notification, and usable recovery were separate contracts

GitLab's 2017 postmortem reports absent logical backups: an application host selected `pg_dump` 9.2 for PostgreSQL 9.6; failure emails were rejected because their sender lacked DMARC configuration. Replicas could not recover the wiped data. A staging snapshot existed, but staging had removed webhooks and its slow disks prolonged restoration. The report identifies missing ownership for regular recovery testing. These are the operator's reconstructed findings, not independently replayed facts. [VER-14: “Broken recovery procedures,” “Recovering GitLab.com,” and root-cause analysis](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/).

**Teaching decision:** define a recoverability claim through an isolated restore, usable application state, expected data loss window, elapsed time, and a working failure signal. A scheduled command, object count, or successful snapshot copy is narrower evidence.

**Counterexample:** a small disposable local cache may not warrant production-grade recovery drills. Its declared disposability and regeneration path are the relevant contract. A skill must discover the durability requirement rather than infer it from the presence of a database.

**Candidate exercise:** supply synthetic backup configuration, a version-selection function, failure mail logs, and a restore checklist. The agent should separate creation, alert delivery, semantic completeness, and recovery time. It must not destroy or restore live data.

### 3. SQLite: strong coverage has a context, and still needs different evidence

SQLite documents full branch/MC/DC coverage of its defined core configuration, plus fault injection and fuzzing. Its §4.1.6 discusses tension: coverage goals can discourage unreachable defensive code, while fuzzing benefits from defenses. §7 describes `ALWAYS`/`NEVER` and condition markers; §7.5 distinguishes an instrumented coverage run from rerunning with delivery compiler options. It explicitly justifies extensive testing for widely deployed durable infrastructure. [VER-25: testing guide](https://www.sqlite.org/testing.html).

**Teaching decision:** record the subject, build, configuration, exclusions, and property behind a verification claim. Treat a suite-quality check and a delivery-artifact check as separate observations. Do not erase defensive code to improve a reported percentage.

**Counterexample:** neither “100% coverage is always required” nor “high coverage targets are always wasteful” survives this example. Risk, supported platforms, persistence, lifetime, and verification cost matter.

**Candidate exercise:** show an agent a high-coverage report, delivery flags, and a defensive branch reached by malformed input. Ask which claims are demonstrated and which require another check. Passing means preserving the defense and explaining remaining scope precisely.

### 4. QuickCheck and flaky tests: generation and execution conditions are part of the test

The original QuickCheck paper's unification case initially exercised a trivial condition in over 95% of accepted generated inputs; a targeted generator changed that distribution. It also found mistaken specifications. This is authors' case-study experience, not a controlled superiority estimate. [VER-02: §§2.4, 5.1.3–5.1.4](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf).

The Apache flaky-test study traces an HBase test from a fixed two-second sleep to waiting on the server condition with a bounded timeout. Its sample came from keyword-selected fixing commits, so its cause frequencies are not general prevalence estimates. [VER-06: case example and §6](https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf).

**Teaching decision:** distinguish the intended property, valid input domain, exercised distribution, environmental condition, and observation timeout. A random seed and generated-case count do not prove useful coverage. A timeout prevents hanging; it does not replace the event being awaited.

**Counterexample:** nondeterminism can be legitimate. Sorting or fixing a seed may conceal a required concurrency property. The oracle should accept the intended set of outcomes while preserving evidence about unexpected ones.

**Candidate exercise:** an ordering property passes thousands of mostly empty cases while a concurrent fixture occasionally fails. The agent should repair the generator and synchronization without retry-until-green or silently weakening assertions.

### 5. Mutation and coverage studies: assess the proxy's construct validity

Just et al. studied 357 real faults in five well-tested Java programs, controlled coverage in comparisons, and found mutation detection associated with real-fault detection. They also report unsupported fault classes and bug/commit linkage bias. [VER-03: §§2.6, 3.2–3.4](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf).

Inozemtseva/Holmes generated 31,000 suites for five Java systems and found weaker coverage/effectiveness association after controlling suite size. Their effectiveness measure used mutants and treated survivors of the full suite as equivalent, an acknowledged validity threat. Correlation did not establish causality. [VER-10: §§3, 5–6](https://cs.uwaterloo.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf).

**Teaching decision:** use a surviving relevant mutant to interrogate a missing behavioral distinction; do not equate mutation score with production correctness. Use uncovered consequential paths to guide attention; do not equate execution with adequate assertions.

**Counterexample:** surviving mutants can be equivalent, irrelevant, or outside the supported domain. Adding a test merely to satisfy a tool can create maintenance work without new confidence.

**Candidate exercise:** two suites have equal branch coverage; one cannot distinguish a wrong refund calculation. The agent should identify the missing oracle and independently derive an expected result. It should also reject an equivalent mutant without inventing a behavioral requirement.

### 6. Performance papers: a later study qualified a dramatic earlier result

Mytkowicz et al. demonstrate layout-dependent measurement bias and use setup randomization; their experiments include SPEC CPU2006 C workloads and older hardware. [VER-12: §§2–3, 7](https://www2.ccs.neu.edu/racket/Performance/mytkowicz.pdf).

Kalibera/Jones found smaller relative variation in their reference-size experiments, yet randomized layouts still significantly worsened mean performance for xalancbmk (3.3%) and mcf (6.8%). Training used P3/P4/P5 without LTO; reference used P3 with LTO for both randomized and baseline builds. The comparison therefore does not isolate input size as the cause. Their hierarchy separates builds, executions, and iterations when allocating repetition and reporting uncertainty. [VER-11: §8.2, PDF pp.8–9; §§9–11](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf).

**Teaching decision:** identify the workload and independent experimental unit before selecting a statistical summary. Many inner-loop samples from one process cannot automatically represent variation between builds or deployments. A significant microbenchmark change does not establish user-visible improvement.

**Counterexample:** thorough statistical reporting is disproportionate for every local tuning experiment. Exploratory results can be useful if labeled as such; stronger performance claims require stronger designs. Performance-critical safety and latency constraints may need worst-case reasoning beyond average speedup.

**Candidate exercise:** two versions differ by 2% in a noisy single-process benchmark but overlap across independent executions. The agent should state the unresolved claim, inspect timing boundaries and actual work, and design the next discriminating measurement rather than announce a win.

## Complementary evidence that changes the procedure

| Evidence | Consequence for a future skill | Scope or exception |
| --- | --- | --- |
| [VER-01: oracle survey](https://philmcminn.com/publications/barr2015.pdf) distinguishes full, partial, specified, derived, and human oracle information. | State where expected behavior comes from; label partial checks honestly. | This pass read introductory/classification material, not all surveyed studies. |
| [VER-04: Zeller's reduction chapter](https://www.debuggingbook.org/html/DeltaDebugger.html) preserves a failure predicate and distinguishes 1-minimal reduction. | Minimize the same failure, including validity and exception identity; keep unresolved outcomes distinct. | A smaller crashing input can exhibit another bug; reduction is not automatically global minimization or a full causal explanation. |
| [VER-05: Csmith](https://web.stanford.edu/class/cs343/resources/finding-bugs-compilers.pdf) avoids undefined/unspecified behavior for differential comparison and examines unverified CompCert boundaries. | Check comparable semantics and trusted boundaries before blaming disagreement on one implementation. | Agreement is not proof; formal verification has a specified scope rather than being useless. |
| [VER-07: Google mitigation account](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html), [VER-08: size analysis](https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html). | Reruns and quarantine are mitigations needing retained signal, ownership, and followup. | Historical internal data; correlations do not establish that deleting integration tests improves quality. |
| [VER-09: Google coverage guidance](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html). | Use coverage as risk/gap evidence with domain-specific targets. | An internal rule or existing release gate remains a real project requirement; a skill must not unilaterally lower it. |
| [VER-15: GitHub 2018 analysis](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/) reports a short partition, divergent writes, and recovery decisions prioritizing integrity. | Verify recovery transitions and backlog/reconciliation, not only availability after a node returns. | One historical operator account, not proof of today's GitHub behavior. |
| [VER-16: SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/), [VER-17: troubleshooting](https://sre.google/sre-book/effective-troubleshooting/). | Separate symptoms from hypothesized causes; use observations or bounded interventions to discriminate. | System knowledge matters; telemetry correlation alone does not identify cause. |
| [VER-18: SLO alerting](https://sre.google/workbook/alerting-on-slos/) discusses low traffic and synthetic-signal masking. | Evaluate alert precision, recall, detection/reset time, and actual user impact. | Copying burn-rate windows can misfit a low-volume or high-value service. |
| [VER-19: ASVS 5.0.0](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.json), [VER-20: SSDF 1.1](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf), [VER-21: threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html). | Tie a control to an asset, trust boundary, threat, requirement version, owner, and observable check. | These are normative/practitioner guidance, not an audit of a product or a universal mandatory checklist. |
| [VER-22: USE](https://www.brendangregg.com/usemethod.html), [VER-23: active benchmarking](https://www.brendangregg.com/activebenchmarking.html). | Ask resource/bottleneck questions and observe what the benchmark actually exercises. | Resource saturation is one lens; it cannot explain every algorithmic or interaction problem. |
| [VER-24: benchmark tool guide](https://google.github.io/benchmark/user_guide.html) warns `DoNotOptimize` need not preserve evaluating a known expression. | Inspect generated work, timing boundaries, setup effects, and chosen clock. | A helper API does not validate experiment design. |
| [VER-26: metamorphic survey](https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf). | Use necessary relations between executions when exact answers are unavailable; specify transformation preconditions. | A passing relation is partial evidence; an incorrect assumed relation is an oracle defect. |
| [VER-27: FoundationDB paper](https://www.foundationdb.org/files/fdb-paper.pdf) explains deterministic faults, tuned state distributions, and simulation exclusions. | Use repeatable schedules plus recovery oracles; test omitted real dependencies separately. | Simulation cannot reliably establish performance or correctness of unmodeled OS/library behavior. |
| [VER-28: Jepsen Redis-Raft](https://jepsen.io/analyses/redis-raft-1b3fbf6) states exact revisions, cluster/fault settings, and unknown causes. | Preserve histories, checker semantics, configuration, and uncertainty even when a failure is demonstrated. | Historical development revisions and selected operations; not a current blanket verdict on Redis. |
| [VER-29: ASan paper](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf) separates instrumented scope and library limitations. | Match an instrumented run to the defect classes it can observe. | Historical implementation/performance results are not today's overhead guarantees; clean runs are not proof of no memory defects. |

## Proposed decision procedure

This is original synthesis for later behavioral trials:

1. State the claim at the right boundary: input/output behavior, state transition, user outcome, security property, recovery requirement, or performance effect.
2. Identify the oracle and its independence from the implementation. List relevant assumptions and the supported input/environment domain.
3. Choose the smallest discriminating observation or intervention. Include a consequential negative path where the claim requires it; preserve seeds, versions, configuration, artifacts, and unresolved outcomes.
4. Inspect whether the check exercised the intended distinction. A green run can still use a trivial generator, mocked-away boundary, optimized-away workload, or assertion copied from the same faulty logic.
5. Report demonstrated result and remaining scope. Broaden only when a new failure, unverified requirement, or material uncertainty justifies it.

The procedure should not require a written ledger for a typo or one-line mechanical change. For risky or expensive operations, a reviewable experiment and clear stopping condition may be necessary. This research does not grant permission to run chaos experiments, restore data, or attack a live service.

## Provisional capability boundaries

| Capability | Natural trigger | Expected artifact | Conditional material |
| --- | --- | --- | --- |
| Design meaningful verification | New behavior or missing confidence in an existing claim | Oracle, representative cases, boundary evidence | Property/metamorphic/differential checks, instrumentation, mutation, browser/contract integration |
| Diagnose a failure | Reproducible or intermittent incorrect behavior | Competing hypotheses, discriminating observation, same-failure reproducer | Reduction, scheduling, environment isolation, logs/traces |
| Measure performance | A speed/cost/latency claim or optimization decision | Workload and timing definition, profile, comparison with uncertainty | Warmup, hierarchical repetition, load generation, tail latency, memory |
| Verify recovery/reliability | Durable state or service failure/release boundary | Failure/recovery scenario and resulting state | Restore rehearsal, fault injection, SLOs, rollout and reconciliation |
| Assess applicable security properties | Trust boundary, sensitive asset, adversarial input, security review | Threat/control/check mapping and limitations | Versioned ASVS controls, secure build/supply chain, authorization, attack-specific validation |

Keep these as candidate units until realistic tasks reveal whether splits improve routing. Existing local `audit-technical-work`, `refactor-by-invariant`, and `propagate-contract-changes` already cover bounded evidence and behavior preservation; do not duplicate them under new names merely to complete the catalog.

## Evaluation cases for future skills

| Task fixture | What success must distinguish | Failure of the skill |
| --- | --- | --- |
| Refund implementation plus self-confirming test | Independent arithmetic oracle; cancellation and invalid input | Calling production code to generate all expected values |
| Passing generated ordering tests with mostly empty inputs | Valid-domain generation and nontrivial input distribution | Increasing sample count without examining accepted cases |
| Intermittent async test | Wait for a defined event with a bounded failure path | Longer sleep, unlimited reruns, or suppression of a race |
| Backup scripts, tool versions, rejected error mail, altered staging snapshot | Creation, usable restore, alert delivery, state completeness, time | Claiming recoverability from a schedule or replica alone |
| Passing WAF match suite plus pathological input | Resource failure, staged exposure, independent recovery access | Treating configuration as harmless data |
| Equivalent coverage with a surviving mutation | Relevant missed distinction versus equivalent or unsupported mutant | Chasing score with assertions that encode accidental behavior |
| Noisy microbenchmark with a known constant expression | Actual work, experimental unit, setup, practically meaningful effect | Declaring a speedup from one best run |
| Multi-tenant API with a mocked repository | Cross-tenant authorization at a reachable boundary | Reporting secure because each mock expectation passed |
| Simulated recovery succeeds while external filesystem behavior differs | Model assumptions versus actual dependency contract | Declaring the whole system verified by simulation |

These are proposed fixtures, not executed experiments. Start paired trials on the same task/settings without and with candidate instructions. Include a small task where the correct result is avoiding extra machinery, and an infrastructure case where intensive verification is justified. Evaluate task completion, false certainty, scope expansion, unnecessary work, and preserved user constraints. A syntax validator or checklist score cannot establish decision quality.

## Advice that should not become unconditional rules

- No universal coverage percentage, fixed pyramid ratio, mutation threshold, rerun count, or minimum benchmark duration.
- No assumption that a flaky test is merely bad test code, or that deterministic behavior is always the product requirement.
- No inference from a named consensus protocol, formal proof, simulator, sanitizer, or standards checklist to whole-product correctness.
- No demand for live fault injection or full threat modeling on every edit; scope the method to the claim and environment.
- No claim that “all tests pass,” “backup configured,” “HTTP 200,” or “faster on average” answers a broader user-outcome question without checking the missing boundary.

## Search trail, exclusions, and next gaps

Representative query families used: original test-oracle survey; original QuickCheck; mutants versus real faults; flaky-test fixing commits; code coverage with suite-size controls; delta debugging and failure predicates; Csmith semantic validity; rigorous performance repetition; measurement bias and refutations; first-party Cloudflare/GitLab/GitHub incident chains; SRE symptom/cause and SLO limits; ASVS/SSDF and threat-model scope; SQLite crash/fuzz/coverage interactions; FoundationDB simulation limitations; Jepsen histories; ASan instrumentation boundaries.

Search results from third-party summaries, Wikipedia, Reddit, aggregators, and tool marketing were discovery leads, not load-bearing evidence. The selected primary materials were opened and relevant sections followed. An original university Csmith endpoint timed out; the same author paper was inspected through a Stanford-hosted copy. The original delta-debugging paper endpoints timed out/returned 502, so the detailed author's book chapter supplies the inspected reduction guidance. The 1998 metamorphic report's extracted text was garbled; no detailed claim relies on it. CISA endpoints returned 403; no mirror was used to claim the primary guidance had been read. ASVS paths returning 404 were replaced with its tagged, machine-readable release. Several PDF follow-up fetches timed out, and corresponding coverage is explicit in the ledger.

Coverage is strongest for automated functional verification, persistent infrastructure, and systems performance. It is weaker for mobile/hardware timing, visual/perceptual oracles, safety-critical certification, usability of testing processes, organizations without specialist infrastructure, and current agent-written tests. Security is scoped to verification design and selected standards—not comprehensive secure engineering or penetration testing. Future work should sample these underrepresented areas and test candidate guidance before expanding skill instructions.

One later claim merits a separate owning-source audit: the architecture researcher found a potential mismatch between SQLite atomic-commit prose and a conditional sync branch at a historical pinned revision. This report does not promote that into a present-day defect or a completed runtime finding.
