# Architecture and system diagrams: deep research

Research date: 2026-11-07. This is a research brief, not an installed skill or a claim that an architectural style is universally best. The companion [source ledger](architecture.sources.jsonl) contains 30 substantively inspected sources and one inaccessible original. Sources from the same author or project are grouped as related evidence, not independent corroboration.

The release snapshots below are intentionally historical, reproducible case studies. They are **not current-version recommendations**. Repository tag references were resolved through the GitHub API, with Kubernetes's annotated tag dereferenced to its underlying commit.

| System | Historical snapshot | Resolved commit | Inspection scope |
| --- | --- | --- | --- |
| SQLite | 3.46.1 | f3d536d37825302e31ed0eddd811c689f38f85a3 | Pager state comments and selected sync, finalization and rollback branches |
| PostgreSQL | 17.0 | d7ec59a63d745ba74fba0e280bbf85dc6d1caa3e | Postmaster rationale and backend startup |
| Kubernetes | 1.31.0 | 9edcffcde5595e8a5b1a35f88c421764e575afce | ReplicaSet sync, expectations utilities and selected test bodies |
| rust-analyzer | 2024-01-01 | 9db515503f11bda7812cdfb9c2839f70f4cb1fdd | Architecture document and syntax dependency manifest |

No builds, benchmarks, tests, deployment checks or failure injections were run. “Implementation corroboration” below means reading selected implementation branches; it does not establish whole-system correctness.

## What changes in the original skill proposal

Architecture and diagramming should begin together, because selecting a representation is part of deciding what matters. A diagram-only skill risks producing attractive boxes whose boundaries have no operational meaning. Conversely, code-only advice can miss consistency, coordination, ownership and failure behavior.

The evidence suggests a shared decision method with conditional references:

1. Identify a concrete behavior, change or quality requirement.
2. Describe the boundaries and guarantees that make it possible.
3. Compare plausible alternatives under the actual constraints.
4. Verify the important claims using code, contracts, scenarios or measurements.

This is our synthesis. It is deliberately more stable than “use microservices,” “use clean architecture,” or “draw all four C4 levels.” The library can change its skill boundaries as evaluation reveals separate recurring jobs.

A source can play several roles, but those roles must remain explicit:

| Evidence class | What it can establish | What it cannot establish alone |
| --- | --- | --- |
| Formal result | A conclusion under a stated model | A product choice outside that model |
| Original design argument | A useful decomposition or function-placement argument | Comparative success across all workloads |
| First-party system paper | Reported design, conditions and measurements | Current service behavior or independently reproduced results |
| Architecture documentation | Maintainer intent, vocabulary and rationale | That implementation still obeys every statement |
| Selected implementation/test code | A particular branch or assertion exists at a revision | That it executes in the relevant deployment or passes its tests |

## Foundations: keep the conditions behind the slogans

### Information hiding concerns decisions, not folder names

Parnas's KWIC comparison treats a module as an assignment of responsibility. It contrasts dividing by processing stage with concealing design choices and explicitly considers implementation overhead. [ARC-01, pp.1054–1057](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf)

**Candidate instruction, our inference:** Before extracting a module, name the decision it owns and a plausible change it should contain. A new directory or interface without a protected decision may increase navigation cost without improving independence. Conversely, a short function can enforce a valuable boundary even if the final compiled representation contains no obvious “module.”

This does not imply that every possible future change deserves abstraction now. A useful exercise compares the cost of the current dependency against the cost of the proposed indirection.

### End-to-end correctness is different from lower-level assistance

Saltzer, Reed and Clark show why application knowledge can be necessary for complete correctness; their duplicate-suppression example includes duplicates originating above the network. Lower-level mechanisms can still improve performance. [ARC-02, PDF pp.2–6](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf)

**Candidate instruction:** For every claimed guarantee, identify the endpoints and what each layer actually knows. “The queue deduplicates” is insufficient unless the deduplication scope covers the business operation being promised. Equally, moving every concern into application code would discard useful infrastructure without justification.

The transferable skill is locating the missing knowledge, not mechanically pushing everything upward.

### CAP terminology must not replace a workload model

Gilbert and Lynch's formal model defines consistency as linearizability and availability as eventual response from non-failing nodes. Its asynchronous impossibility result is not a definition of ACID consistency or a latency SLO. [ARC-03, §§2–3](https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/cap-proof.pdf)

**Candidate instruction:** Specify the operation, invariant, observation and failure assumptions before invoking a theorem. A design that tolerates stale catalog reads but requires single-use redemption needs operation-specific reasoning. Categorizing the whole system with two letters can hide the important choice.

No claim in this brief establishes which consistency model a particular user application should select.

### Organizational structure is architectural context

Conway relates subsystem interfaces to communication among design groups. The original is a conceptual argument, not an experimentally calibrated law predicting every organization. [ARC-07, “A basic relationship”](https://www.melconway.com/Home/Committees_Paper.html)

Fowler's bounded-context account explains how shared words can have incompatible meanings in different models; a context map makes mappings explicit. Evans's original reference could not be read here, so this is labeled interpretation rather than original-author evidence. [ARC-08](https://martinfowler.com/bliki/BoundedContext.html), [inaccessible ARC-31](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)

**Candidate instruction:** Ask who changes and operates a boundary, which vocabulary they use, and how coordination happens. A semantic boundary, a team boundary, a process boundary and a transaction boundary may coincide, but they are different decisions. Do not infer “one microservice per noun” or “one team per bounded context.”

### Expert disagreement is useful training material

Fowler argues that uncertain early boundaries and distribution overhead favor starting coarse-grained, while explicitly calling his evidence sparse and tentative. [ARC-10](https://martinfowler.com/bliki/MonolithFirst.html)

Tilkov argues that independently delivered subsystems can enforce separation when the domain is understood and delivery independence matters; he acknowledges both small-system exceptions and expensive boundary changes. [ARC-11](https://martinfowler.com/articles/dont-start-monolith.html)

**Reconciliation, our inference:** These sources disagree about the practical ability to preserve boundaries inside a monolith. They largely agree that distribution needs justification. A skill should preserve that unresolved empirical question and compare team experience, domain uncertainty, operating costs and independent release requirements. Counting recommendations for either style would conceal the disputed premise.

### Evolving architecture needs explicit protected properties

The inspected evolutionary-architecture excerpt distinguishes focused and holistic checks and discusses conflicting quality goals. It uses selected examples rather than a controlled study of outcomes. [ARC-09, “Combining Fitness Function Categories,” “Conflicting Goals”](https://www.thoughtworks.com/content/dam/thoughtworks/documents/books/bk_building_evolutionary_architectures_en.pdf)

arc42 makes quality requirements assessable through specific usage and change scenarios. [ARC-16, §10.2](https://docs.arc42.org/section-10/)

**Candidate instruction:** Name what a proposed change must preserve and choose the cheapest credible evidence. A dependency-direction check can protect an import rule; it cannot demonstrate that a cross-region purchase completes within a deadline. A latency measurement cannot show whether a duplicate purchase is semantically safe.

A check should remain a proxy with a known coverage boundary. Passing it is not a certificate of architectural quality.

## Six contrasting system cases

### 1. SQLite: where a commit becomes durable, and what a diagram can omit

**Question:** How should a model explain interruption between writing data and declaring a transaction committed?

The architecture page identifies SQL compilation/bytecode execution and storage responsibilities. This case deliberately zooms into the pager rather than extending that component overview into an unreadable full-system sequence. [ARC-19](https://sqlite.org/arch.html)

**Documented mechanism:** The atomic-commit article concerns rollback journaling, excludes WAL, describes hot-journal recovery and explains filesystem assumptions and simulated crash tests. [ARC-20, §§1–4,8–9](https://sqlite.org/atomiccommit.html)

**Observed branches at the historical commit:**

| Locator in pager.c | Narrow observation |
| --- | --- |
| [L6437 onward](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L6437) | Phase one branches between WAL and rollback handling. |
| [L6570 onward](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L6570) | Rollback path synchronizes journal before page writes; database sync is conditional. |
| [L6674 onward](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L6674) | Phase two delegates finalization; an unchanged exclusive/PERSIST transaction can return early. |
| [L2067–2079](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c#L2067-L2079) | Nonempty TRUNCATE journal: successful truncation plus fullSync triggers journal sync. |

[ARC-21](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/src/pager.c)

**Demonstrated representation discrepancy:** Retrieved article §7.6 says TRUNCATE is not followed by fsync; the selected implementation has the conditional sync above. This establishes a discrepancy between that prose and that revision under those flags. It does not establish a defect in today's runtime or every configuration. The article contains historical passages and is not a specification pinned to 3.46.1.

The teaching opportunity is more important than the discrepancy itself: a diagram marked “TRUNCATE commit” without synchronization flags and mode has silently erased a meaningful condition.

The observed call requests synchronization through the VFS abstraction. It is not a receipt that a particular operating-system fsync ran. The fullSync configuration condition is distinct from a platform-specific full-fsync syscall option.

**Original teaching model of the normal successful rollback path, derived from the selected evidence; not a reproduction of SQLite's diagrams:**

~~~mermaid
flowchart LR
    A["Rollback-mode phase one"] --> B["Journal durability"]
    B --> C["Database pages"]
    C --> D["Database durability"]
    D --> E["Journal finalization"]
    E --> F["Commit complete"]
    D -. "interruption before finalization" .-> G["Recovery decision"]
~~~

The arrows express a simplified ordering, not every function call. WAL, atomic-write optimizations, noSync and exclusive-mode fast paths are intentionally outside this model. The associated evaluation must require the agent to declare those omissions.

**Exercise:** Give the learner the article plus selected code and ask what happens at two interruption points. Reward locating a recovery decision and flag dependency. Penalize an unconditional “write succeeded, therefore committed.” A useful follow-up asks how the answer changes under WAL; the right response is to inspect that path rather than reuse the rollback explanation.

### 2. Kubernetes: reconciliation tolerates delayed observation, not magic exactly-once execution

**Question:** What prevents repeated reconciliation from creating unnecessary resources while observations lag?

Kubernetes documents controllers as loops comparing desired and current state, with actions and reported state communicating through APIs or external systems. [ARC-25](https://kubernetes.io/docs/concepts/architecture/controller/)

The historical ReplicaSet implementation checks expectations before listing cached Pods, gates replica mutation, still updates status, decrements expectations for skipped/failed creations, and rate-limits unsuccessful work items. [ARC-26, L547–751](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set.go#L547)

Its utility accepts fulfilled **or expired** expectations; the selected expiry is five minutes. This is a liveness mechanism, not durable deduplication. [ARC-28, L70, L186–220](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/controller_utils.go#L186)

Expiration is evaluated when the expectation check runs; the five-minute comparison does not itself schedule a new reconciliation.

Selected test bodies assert dormancy without duplicate creates, recovery after create failure, expectation-before-list ordering, and stopping slow-start batches after failure. They were read, not executed. [ARC-27, L278–387, L1105–1135, L1776–1845](https://github.com/kubernetes/kubernetes/blob/9edcffcde5595e8a5b1a35f88c421764e575afce/pkg/controller/replicaset/replica_set_test.go#L307)

**Original explanatory model:**

~~~mermaid
flowchart LR
    W["Work item"] --> E["Compute expectation flag"]
    E --> O["Observe cached Pods"]
    O --> M{"Mutate replicas?"}
    M --> S["Update status"]
    M -. "failure" .-> R["Rate-limited retry"]
    S -. "new observations" .-> W
~~~

The simplified view omits deletion, adoption and several status/error branches. The expectation flag includes expiry and gates mutation, not observation/status; “observe” does not mean an instantaneous globally authoritative snapshot.

**What the learner should reason about:** An API action and observing its result are separate events. Waiting forever sacrifices liveness; proceeding immediately can act on stale knowledge. The source preserves progress through explicit bookkeeping, ordering and retry choices. Calling the loop “idempotent” without describing these conditions would conceal its hard part.

**Alternative paths to preserve:** no expectations, unfulfilled expectations, expiration, successful create with delayed observation, immediate create error, and deletion in progress. An evaluation should ask the learner to trace a subset and identify where the evidence ends. It must not reward claiming this implementation guarantees exactly-once resource creation.

### 3. PostgreSQL: process structure and transactional guarantees are different views

The versioned architecture overview describes a client/server model with per-connection backends. The pinned postmaster's startup path launches the backend; its introduction explains why the supervisor avoids client blocking and much shared-memory activity. [ARC-22](https://www.postgresql.org/docs/17/tutorial-arch.html), [ARC-24, file introduction and L3544 onward](https://github.com/postgres/postgres/blob/d7ec59a63d745ba74fba0e280bbf85dc6d1caa3e/src/backend/postmaster/postmaster.c#L3544)

The isolation contract distinguishes snapshot-based Repeatable Read from Serializable behavior and requires application handling of serialization failures, including retrying the whole transaction. [ARC-23, Table13.1 and §13.2.3](https://www.postgresql.org/docs/17/transaction-iso.html)

**Our inference:** A process diagram can explain fault/connection ownership while telling the reader little about whether two concurrent business operations preserve an invariant. A transaction schedule can expose that problem without showing every server process.

**Exercise:** Draw a minimal process view and a separate two-transaction history for a supplied invariant. Require the learner to name the chosen isolation semantics and the boundary of a retry. Penalize deriving isolation guarantees from “uses PostgreSQL,” or assuming a retried statement reconstructs all decisions made earlier in a failed transaction. This brief did not inspect the isolation engine, so its guarantees remain documented contracts rather than independently verified implementation behavior.

### 4. rust-analyzer: document what the code must not know

At the pinned revision, the architecture document labels syntax as an API boundary and distinguishes internal HIR representations from façade APIs. It explains some intentionally absent dependencies, information that a directory listing cannot convey. [ARC-29, “Code Map”](https://github.com/rust-lang/rust-analyzer/blob/9db515503f11bda7812cdfb9c2839f70f4cb1fdd/docs/dev/architecture.md#L91)

The matching syntax manifest has no direct Salsa or LSP dependency. That corroborates only this narrow separation; it does not prove an absence of all indirect coupling or runtime I/O. [ARC-30, L15–31](https://github.com/rust-lang/rust-analyzer/blob/9db515503f11bda7812cdfb9c2839f70f4cb1fdd/crates/syntax/Cargo.toml#L15)

**Our inference:** An architecture document should distinguish promises at boundaries from freedom within them. Applying the same “perfect public API” rule to every internal data structure can preserve accidental interfaces and impede useful change.

**Exercise:** Supply a requested editor feature and ask which boundary it should cross. The learner must inspect the actual types and callers before proposing a new dependency. A diagram should mark the asserted API boundary and cite the matching revision; a fully detailed class graph is unnecessary unless the question requires it.

### 5. Dynamo: availability has application-visible consequences

The original Dynamo paper describes object versioning and application reconciliation. Its shopping-cart merge example preserves additions while allowing deleted items to reappear. [ARC-04, §4.4](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

**Our inference:** “Eventual consistency” is too vague as a skill instruction. The relevant design artifact is a conflict history and reconciliation rule with business-visible consequences. A shopping cart may tolerate a consequence that a financial reservation cannot.

**Exercise:** Give two concurrent add/remove histories and ask the learner to propose, compare and explain reconciliation semantics. Reward explicit loss/resurrection behavior and unsupported-claim boundaries. No current DynamoDB behavior should be inferred from this 2007 Dynamo case.

### 6. Spanner versus Helland: avoid turning a position paper into an impossibility proof

Helland explores application patterns while assuming no large-scale distributed transactions; the work is explicitly a position paper. [ARC-05, introduction and message-processing sections](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf)

Spanner reports a contrasting system using replicated transaction state, two-phase commit and time uncertainty. Its evaluation reports workload-specific measurements rather than a free, universally available abstraction. [ARC-06, §§2.1–2.3,4.2.1 and Table4](https://www.usenix.org/system/files/conference/osdi12/osdi12-final-16.pdf)

**Our inference:** The comparison invalidates “distributed transactions are impossible” as a distilled rule. It does not show that application-level coordination is obsolete. The design question concerns infrastructure, workload, latency, operational cost and the application complexity moved between layers.

**Exercise:** Ask the learner to compare a local transaction, asynchronous entity workflow and distributed transaction for a supplied business invariant. Require costs on both sides. An answer that cites CAP without reconciling its precise model should fail.

## Diagrams as reasoning artifacts

C4 distinguishes multiple levels and advises using only useful views. Its FAQ discusses differing rates of staleness; its checklist checks meaningful elements and relationships. [ARC-12](https://c4model.com/diagrams), [ARC-13](https://c4model.com/diagrams/faq), [ARC-14](https://c4model.com/diagrams/checklist)

arc42 asks for a representative selection of significant runtime/error scenarios and accepts text as well as diagrams. [ARC-15, Content/Form](https://docs.arc42.org/section-6/)

A proposed skill should select the artifact by its question:

| Question | Useful representation | Likely owning evidence |
| --- | --- | --- |
| Who depends on the system, and what is outside its scope? | Context view | Interfaces, stakeholder requirements, service catalog |
| Which components run separately and own data? | Runtime/deployment view | Deployment definitions and runtime configuration |
| What assumptions make this module independently changeable? | Responsibility/dependency view | APIs, imports, representations and ADRs |
| What happens after partial success or delayed observation? | Sequence, state machine or event history | Handler/state code, contracts, failure tests |
| Which combinations of concurrent operations are allowed? | Transaction history or state invariant | Isolation contract and concurrency evidence |

“Authoritative representation” needs a precise meaning. A deployment file can own declared desired deployment; it does not prove the actual running deployment. An imported dependency graph can own syntactic imports; it does not fully capture shared schema, timing or semantic coupling.

A practical consistency protocol, proposed here:

1. **Declare the question and status.** Label an existing-system view, a proposed change or a teaching model. Include scope, relevant modes and revision/environment.
2. **Map claims to evidence.** Connect named nodes and edges to specific modules, interfaces, schemas, configuration or observed runtime facts. Mark inferred/unverified relationships.
3. **Review semantics.** Check arrow direction and meaning; distinguish calls, data flow, ownership, happens-before and deployment containment. A bidirectional line should not silently promise synchronous communication.
4. **Check change impact.** When a boundary changes, inspect affected views and decisions. Regenerate mechanical detail when useful; manually review meaning and omitted paths.

Mermaid rendering only establishes renderability. Generated edges are only as complete as their extraction source. A diagram can be internally tidy while describing the wrong version or erasing a decisive flag, as the SQLite case shows.

## Provisional decision rules for a future skill

These are recommendations synthesized from the evidence, not quotations or demonstrated universal laws.

| Trigger | Reasoning to perform | Avoid |
| --- | --- | --- |
| Proposed abstraction | Identify the decision hidden and an actual change it contains | Interface/folder creation as evidence of modularity |
| New remote boundary | Identify added latency, partial outcomes, ownership and recovery | Treating a local call as remote without revisiting semantics |
| Retry or repeated delivery | Define business operation identity and retry owner; model unknown outcomes | Assuming an error proves no effect occurred |
| Shared model across teams | Compare meanings, invariants and coordination needs | Assuming identical field names imply one canonical model |
| “Make it scalable” request | State workload and measurable target; compare current bottleneck evidence | Introducing distribution before defining the requirement |
| Architecture migration | Preserve necessary properties and plan incremental evidence | Replacing a style merely because another is fashionable |
| System diagram request | Select a question, audience, evidence source and maintenance boundary | Mandatory diagram packs or unexplained boxes |
| Claimed architecture quality | Test a usage/change/failure scenario with stated limits | Inferring quality from source count or diagram polish |

AWS's retry-amplification and ambiguous-side-effect examples support treating retry behavior as a system-level decision. [ARC-18](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

Nygard's proposal supports recording significant decisions, consequences and supersession. Its short early experience report should not be inflated into universal efficacy evidence. [ARC-17](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

An appropriate future decision record would include: the concrete problem; present constraints; options considered; expected benefits and costs; evidence or assumptions; and a condition that would justify revisiting it. Most small code changes do not need such a record.

## Provisional skill boundaries

The research does not justify freezing a taxonomy yet.

1. **Design and evolve systems:** structural and behavioral decisions; boundaries, state, concurrency, failure and quality scenarios; diagrams selected as part of reasoning.
2. **Refactor while preserving behavior:** a different job from designing new behavior. Its evidence should focus on preserved contracts and observable results.
3. **Explain and review architecture:** potentially a distinct invocation when the user wants an account of an existing system, not changes. It should make undocumented/inferred relationships visible.
4. **Conditional domain references:** distributed coordination, persistence/transactions, interactive incremental tools, and diagrams. These have distinct failure models and should load when needed.
5. **Shared evidence/update practice:** source classification, revision pinning, disagreement and realistic skill evaluations can support multiple domains without duplicating every source in every skill.

A “diagram skill” is justified if independently requested diagram work recurs enough to require its own workflow. An “architecture fundamentals” catchall that activates on all code editing would likely load irrelevant theory and overcomplicate routine work. That prediction needs behavioral evaluation rather than confident assertion.

## Meaningful evaluation tasks

These are proposed evaluations; none has been executed.

| Task | Required observable output | Failure condition |
| --- | --- | --- |
| SQLite doc/code disagreement | Names revision, journaling mode and conditional sync branch; separates documentation from execution | Repeats unqualified prose or claims latest runtime was tested |
| ReplicaSet delayed observation | Traces expectation gate, mutation/status separation, error handling and expiry; distinguishes tests read from tests run | Claims exactly-once behavior or ignores stale observation |
| Domain-model integration | Defines conflicting meanings, mapping ownership and update/release constraints | Creates one universal shared type without examining semantics |
| Greenfield deployment choice | Compares coarse/local and distributed alternatives against supplied requirements; preserves counterargument | Selects a style by slogan or treats an opinion as proof |
| Existing-system explanation | Maps every consequential diagram claim to a source or explicit inference; includes representative failure behavior | Invents services or presents proposed topology as running fact |

Run the same task with and without a candidate skill, keep its source material constant, and evaluate the artifact using a rubric written before inspecting the outputs. Include small projects where extra process is the failure mode and legacy projects where consistency and ownership matter more than a fresh folder tree. More references are not a success metric.

A useful rule should improve a decision or expose a missing assumption. If it only increases report length or introduces boilerplate diagrams, remove or narrow it.

## Search trail and stopping boundary

The investigation used multiple source families and followed originals behind familiar slogans.

| Query family / route | Inspected destination | Consequential result or gap |
| --- | --- | --- |
| Parnas modular decomposition; end-to-end original paper | University-hosted Parnas original; MIT author-hosted end-to-end paper | Context and implementation caveats survive the slogans |
| CAP proof; Dynamo reconciliation; distributed transactions | Gilbert/Lynch paper; author-hosted Dynamo; CIDR Helland; USENIX Spanner | Distinguishes theorem, position and implemented system report |
| Conway original; bounded-context original/reference | Conway author page; Fowler interpretation; Evans original attempted | Evans PDF and landing page returned HTTP403; no original-content claim made |
| C4/arc42/ADRs/evolutionary architecture | Method-author sites; Nygard original; authorized book sample | Distinguishes useful views, traceable decisions and targeted checks |
| First-party docs → repository release refs → selected implementation/tests | SQLite, PostgreSQL, Kubernetes and rust-analyzer | Four pinned examples; two deep behavioral traces; one scoped documentation/code discrepancy |

CAP author-hosted download timed out; the same original paper was read from a university course copy. A Princeton Dynamo copy returned HTTP403; the author-hosted original was inspected. Google's Spanner archive fetch failed; the USENIX original was inspected. These failures are access observations, not evidence against the underlying ideas.

C4's overview, FAQ and checklist are one method family, not three independent confirmations. The same applies to multiple Kubernetes files and to SQLite's docs/code. PostgreSQL's versioned documentation is not a byte-for-byte snapshot of 17.0; only the explicitly pinned implementation is.

The survey stops after covering original boundary/function-placement reasoning, formal distributed limits, contrasting transaction assumptions, socio-technical context, architectural evolution, representation practices and four code-correlated cases. It is not an exhaustive history of software architecture.

## Remaining uncertainty and next research

The largest remaining need is behavioral validation on the user's own tasks. None of this research proves that a proposed skill improves an agent's output. That requires examples, independent evaluation and revisions based on observed failures.

Technical coverage is also incomplete: security/threat modeling, streaming/backpressure, resource ownership in concurrent programs, real-time/safety-critical systems, mobile/offline synchronization and hardware-specific architecture require separate source sets. They should not be filled in by extrapolating from backend services.

The case studies are selected because they expose different design pressures, not because their popularity proves excellence. They do not establish comparative performance, code quality or broad representativeness. Production observation and current support policy remain outside scope.

Future updates should revisit mutable documentation and resolve fresh revisions before making current claims. Preserve older cases when they explain change, but label them historical. Add counterexamples and remove rules that fail realistic tasks. Do not convert every newly encountered pattern into another mandatory instruction.

