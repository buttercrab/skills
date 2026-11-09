# Fundamentals skills: synthesis of the deep investigation

Research date: 2026-11-07, Asia/Seoul. This replaces the initial brief as the main synthesis. Domain dossiers and source registries preserve the underlying detail. The proposed instructions and skill boundaries remain research-derived candidates, not tested or installed skills.

## What this investigation establishes

The library should teach how to make and verify consequential decisions in context. It should preserve original evidence, meaningful exceptions, and examples that show the mechanism behind a choice. Its taxonomy should evolve with the work it actually supports.

This recommendation now rests on original studies and methodological limits, code-backed maintenance/architecture cases, first-party design reversals and incidents, real writing revisions, and inspection of existing skill/evaluation implementations. Those are different evidence types. They support specific conclusions rather than a universal ranking of good design, architecture, prose, or repositories.

The investigation has not run new agent trials, reproduced the cited experiments, tested live product flows, built the inspected projects, or evaluated the proposed catalog. It supplies a much deeper foundation for that next stage and identifies what the stage must measure.

## Eight findings that should shape the library

### 1. Context belongs inside a principle

The domain research repeatedly exposes advice whose apparent simplicity comes from omitting a decisive condition:

| Advice encountered | Condition a useful skill must retain | Example from the dossiers |
| --- | --- | --- |
| Use one thing per screen | Knowledge, frequency, dependencies, interruption and correction cost | GOV.UK's repeated-expert-work exception and related-field grouping; checkout field burden versus raw steps. |
| Simplify by hiding controls | How often users inspect the current state, not just invoke the action | Figma restored visible blend-mode state and a direct clip-content checkbox after UI3 feedback. |
| Choose the best font | Reader, script, size normalization, task and rendering | Wallace's within-reader observed speed contrast does not establish a universally fastest font or deployable percentage gain. |
| Prefer a monolith or services | Domain uncertainty, release independence, operating capacity and boundary-change cost | Fowler and Tilkov retain a genuine disagreement about preserving boundaries; neither supplies a theorem choosing every system's topology. |
| Use active voice | Whether identifying an actor helps the reader | Google explicitly permits passive constructions in appropriate contexts. |
| Increase test coverage | Supported configuration, relevant failure class, assertion/oracle strength and existing project gates | SQLite's risk justifies extensive coverage while its guide still distinguishes instrumentation, fuzz defenses and delivered builds. |

Sources and precise limits: [UX](ux-flows.md), [visual design](visual-design.md), [architecture](architecture.md), [writing](writing.md), [verification](verification.md).

The instruction format should make the condition actionable. A useful rule can supply a default and explain the signal that would change it. This is different from presenting a menu of every technique or requiring the agent to rediscover the whole field each time.

### 2. Good diagrams, prose and repository trees expose meaningful relationships

These artifacts share an important function: helping a reader reason about something they cannot see all at once. Their surface neatness is insufficient evidence of quality.

A repository tree becomes informative when it reveals editing authority, dependency constraints, release units, and validation routes. An architecture diagram becomes informative when it identifies responsibilities, guarantees and relevant interactions. An article structure becomes informative when each section changes the reader's understanding and supplies the support the argument needs.

Concrete traces make this distinction visible:

- Kubernetes staging is an authoritative editing location for modules published elsewhere; treating the copies as ordinary duplication would suggest the wrong edit.
- uv's stdout generation mode, freshness-comparison mode, and build-time generation answer different questions. Following validation and publication workflows resolved an initially suspicious configuration.
- SQLite's historical pager branch preserves a conditional synchronization step omitted by a retrieved documentation passage; a simplified commit diagram must declare flags, modes and omitted paths.
- Actual Distill momentum revisions replace a formula-first sequence with explicit bottleneck/eigencomponent reasoning and expand an analogy into questions the model must answer.

See the exact revisions and evidence boundaries in [repository cases](repositories.md), [architecture cases](architecture.md), and [writing revision analysis](writing.md). These examples support tracing the relationship behind an artifact; they do not imply that every task needs a large map or written rationale.

The [code and contracts investigation](code-and-contracts.md) adds caller-level questions: what an interface promises, what remains observable after failure, which error identity a caller may depend on, and what survives a representation change. Its three pinned cases connect contracts to implementations and test callers. The [coordinator source check](review-code-and-contracts.md) corroborates selected branches without claiming runtime verification.

### 3. Quality has dimensions that should not silently compensate for one another

Many attractive proxies are useful but incomplete: screenshot ratings, reading preference, step count, coverage, complexity scores, task pass rates, instruction compliance, and fluent prose.

The deeper source reading makes several distinctions consequential:

| Property | Different property it does not establish |
| --- | --- |
| Appealing first impression | Successful repeated task performance or accessible interaction |
| Preferred typeface | Highest reading effectiveness for that reader |
| Fewer visible controls | Less work to inspect and modify relevant state |
| Higher human-rated recommendation quality | Correct recommendation |
| More executed branches | An oracle that distinguishes the important defect |
| Skill read and procedure followed | Improved user outcome |
| Rendered system diagram | True components, relationships and guarantees |

Our recommendation is to keep a task-specific scorecard before inventing an overall score. Some requirements may be gates: a critical flow must work, an important factual claim must be supported, a public contract must remain compatible. The appropriate gate follows the task, not a universal production-readiness checklist.

### 4. The evidence behind the recipe matters as much as the recipe

The research found material examples where a source's public framing, methods, or implementation required qualification:

- Choice-overload meta-analyses disagree in aggregate and in moderator interpretation; a corrigendum changes reported notation. Neither justifies a universal maximum option count.
- Faulkner's five-user investigation resamples a finite observed problem set. It demonstrates variability within that setup, not a universal participant count for every population.
- Duolingo's proficiency comparison involves selected participants, historical tests, and bundled content/practice changes. It does not isolate navigation layout as the cause.
- Doshi/Hauser's analyzed sample includes a no-AI control; describing all participants as receiving AI ideas would misstate the treatment.
- The main Wallace study samples five fonts per reader from a larger set and compares observed fastest/slowest performance. It is not a trial of a deployed personalized-font system.
- The SkillsBench size/module comparisons bucket different tasks. They do not causally establish an ideal length or module count for a rewrite of one skill.

The domain reports retain methods, dates, revisions and limitations rather than repeating headlines. Some records remain partial or inaccessible. A familiar citation is not a receipt for inspecting its full evidence.

### 5. Evaluation machinery can reward the wrong thing

The skills lane followed papers into public tasks, skill files, verifiers, result records and scoring code. Two examples directly affect how this library should be tested:

At an inspected NVIDIA SkillEvaluator revision, the runtime documentation says an older accuracy criterion required identifying the skill, capping a correct skill-free baseline at 0.8. The changed contract separates skill execution from five outcome criteria and declares the scores non-comparable. This does not independently quantify how a published aggregate would change after rescoring.

At an inspected OpenSkillEval revision, a README describes eight weighted dimensions, while the selected judge code averages five available dimensions. That is a documentation/implementation discrepancy in that path, not proof that every published experiment used that revision or path.

Exact receipts and independent source review are in [skills evaluation](skills-evaluation.md) and [its review](review-skills-evaluation.md). The lesson is to preserve the grader's actual contract and revision. A measure named accuracy, quality, or overall is not self-defining.

### 6. Examples can teach mechanisms and also create accidental instructions

Public evaluation artifacts show a task requesting files under `ci/` while a relevant skill example uses `.github/workflows/`; paper trace analysis reports that the agent followed the example location instead. Separate multi-skill studies show examples displacing compatible requirements as well as resolving explicit conflicts. Those results are specific to their evaluated setups, not proof that examples are inherently harmful.

Human analogical-learning research supplies a complementary hypothesis: comparisons can expose a useful relationship that a lone polished example does not. That research concerns humans. Direct agent trials must determine whether a particular teaching format helps this library.

Our proposal is to include contrasting cases when they expose a real decision: same appearance/different mechanism, different appearance/same mechanism, and a changed constraint that changes the appropriate answer. Label replaceable paths, names, framework choices and invented numbers. A good example should not quietly override the current task.

See [skills evaluation](skills-evaluation.md) and [knowledge synthesis](knowledge-synthesis.md).

### 7. Existing skills contain valuable mechanisms and contextual policies

The inspected skills are useful material to learn from. Their tool integration, reference routing, before/after examples, diagnostic patterns, and evaluation loops can address real gaps. Their aesthetic bans, preferred stack, approval sequence, mandatory process, and brand voice may have narrower applicability.

For example, ui.sh and Taster disagree about Inter; actual design systems use their own product/brand typography. A picker implementation helps compare rendered options but does not decide which directions are appropriate. Vercel's detailed barrel-import guidance includes exceptions and alternatives that a one-line prohibition would lose.

Distinguish studying an idea from copying code, instructions, fonts or assets. Preserve license/provenance boundaries. Mutable remote references also need an inspected version when reproducibility matters. These observations do not rank libraries by popularity or measured performance.

### 8. Maintenance should allow subtraction and reframing

The original writing-process research and actual article revisions support revisiting a claim as the work develops. Product redesign corrections show similar reframing in interaction decisions. Standards, dependency behavior, tool capability and model baselines also change.

A source refresh can narrow an instruction, expose an exception, invalidate a recipe, or show that a capable baseline no longer needs it. A new skill can interfere with an existing one. Therefore the library must allow instructions to shrink, split, merge, or retire.

This is a proposed maintenance policy, not a demonstrated outcome of an implemented system. Avoid converting every research discovery into another always-on instruction.

## Provisional capabilities and existing ownership

This table describes work the eventual library could support. It does not commit to these exact names or to one skill per row.

| Capability | Main decisions and artifacts | Packaging question to test |
| --- | --- | --- |
| Experience and flow design | User outcome, journey boundary, information architecture, state/correction paths and content | Whether interaction evaluation is a recurring independent task or supporting reference. |
| Visual direction and interface craft | Relevant character, hierarchy, typography, composition, responsive content and accessibility | How much belongs in a shared entrypoint versus context-specific implementation guidance. |
| System and code design | Ownership, interfaces, guarantees, data/failure behavior, useful diagrams and alternatives | Whether API/contracts work activates independently often enough to split. |
| Repository maintainability | Contributor/change routes, editing authority, generated/mirrored artifacts, build/test/release boundaries | Whether documentation authoring shares enough workflow to stay together. |
| Writing and explanation | Reader purpose, claims, evidence, structure, voice, revision and examples | Start with genre references; split only if actual task behavior warrants it. |
| Verification and diagnosis | Oracles, causal hypotheses, test selection, measurement, recovery and risk | Separate debugging, test design and performance measurement when their triggers and procedures diverge. |

Security, reliability, accessibility, content, and evidence appraisal are cross-cutting concerns with specialized depth available when relevant. Cross-cutting does not mean every small task should load every checklist.

Existing local skills already own important mechanics:

- `research-with-evidence`: source discovery, evidence alignment, disagreement and coverage limits.
- `audit-technical-work`: bounded read-only assessment, demonstrated defects versus missing proof.
- `refactor-by-invariant`: behavior-preserving ownership change, migration and verification.
- `propagate-contract-changes`: authoritative definitions, producers, boundaries and consumers.

New fundamentals guidance should add decisions/examples those owners lack, rather than duplicate or overrule them. User constraints and authorization remain authoritative; a sourced preference is not permission to expand work.

## A concrete form for a candidate rule

The following is an original example of the proposed format, not an installed instruction or a claim of tested benefit.

**Decision:** choosing an action for an empty results view.

**When it applies:** a user sees no records and needs to understand whether to create, change a query, wait, seek access, or recognize completion.

**Procedure:** inspect the actual cause, the user's permission, and the available action. Preserve entered filters and relevant context. Choose the explanation and control that fit that state.

**Counterexample:** an empty filtered result must not imply that the account has no data. An illustration and “create your first item” button can be misleading even when visually polished.

**Evidence:** documented empty-state patterns and correction/flow guidance; no universal experimentally optimal layout asserted.

**Original trial:** provide the same table component in four causally different states, including a user who lacks creation permission. Judge the action and recovery path separately from appearance. A held-out case uses delayed asynchronous results.

This form retains the useful distinction, makes the boundary visible, and supplies a way to detect a bad application. It need not become a mandatory long template for every rule.

## Proposed development sequence after research

1. Select realistic tasks from actual work, with artifacts and constraints. Avoid choosing only tasks that make a favorite rule succeed.
2. Draft a small coherent instruction set using the relevant cases. Keep deep research and specialized mechanics accessible without loading them all.
3. Compare against the actual capable-agent baseline. Distinguish explicit use, natural activation, false positives, and combinations with existing skills.
4. Inspect outputs and traces, including failures and cost. Calibrate any automatic grader against the property it claims to measure; include intended-user or expert judgment where needed.
5. Revise based on the responsible cause. Preserve fresh tasks for forward evaluation; treat reused cases as regression tests. Recheck when source/tool/model changes could alter the decision.

These are recommended next implementation steps. No trial results, installed skills, or effectiveness claims are implied by writing this sequence.

## Coverage that remains incomplete

The corpus is strongest in web/service/enterprise interaction, openly documented software projects, technical explanation, selected systems papers, and public agent evaluations. It remains weaker in games, native mobile/embedded/data-pipeline maintenance, private-team constraints, professional literary work, non-English/cross-cultural studies, disabled users' complete workflows, longitudinal effects, and independent reproduction of the skill benchmarks.

Those are meaningful research priorities, not reasons to discard the findings above. The immediate evidence gap for the library itself is behavioral: whether its candidate instructions improve real tasks under the user's actual constraints. More sources from the same institutional families cannot answer that question alone.
