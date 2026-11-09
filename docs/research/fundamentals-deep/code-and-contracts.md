# Code and contract design: fundamentals research

Research date: 2026-11-07. This dossier fills the code-level gap left by a distributed-systems-heavy architecture survey. It is research, not an installed skill. The [ledger](code-and-contracts.sources.jsonl) contains 18 inspected source bundles: original design arguments, official API/format guidance, pinned implementation branches and test callers. Multiple files from one project are related evidence, not independent confirmations.

**Decision implication:** A useful code-design skill should teach how a caller can use, misuse, recover from and upgrade an interface. Its unit of reasoning is a behavior and its supported observations—not a class, file, design pattern or layer count.

## Scope and evidence classes

Three implementation cases were intentionally pinned to historical releases. These are reproducible examples, not recommendations to install these versions or claims about the latest release.

| Case | Snapshot | Commit | What was inspected |
| --- | --- | --- | --- |
| Rust exact-read contract | Rust 1.81.0 | eeb90cda1969383f56a2637cbd3037bdf598841c | I/O trait documentation, default implementation, slice specialization and selected tests |
| Go error wrapping | Go 1.23.0 | 6885bad7dd86880be6929c02085e5c7a67ff2887 | errors inspection, fmt.Errorf implementation and external-package test callers |
| Protobuf binary/JSON evolution | protobuf-go 1.34.2 | c33baa8f3a0d35fd5a39e43c22a50a050f707d34 | Binary/JSON decoder branches and public-API test fixtures |

GitHub tag references were resolved to commits; Rust's annotated tag was dereferenced. Live documentation was read separately and is labeled by retrieval date. Pinned source comments establish the historical contract where version-specific interpretation matters.

No source code, tests, generators or installers were executed. No proposed API was compiled. Static branch tracing supports narrower claims than an executed experiment, and test code records an intended assertion rather than a passing run.

## Design from callers, not an implementation-shaped interface

Bloch's original slides advocate writing caller examples early, specifying effects and exposing diagnostics programmatically. His closing slide presents the advice as heuristics. [COD-01, slides 11, 21, 30–35, 49](https://www.cin.ufpe.br/~if669/files/MaterialDeEnsino/Referencias/api-design-oopsla-2006.pdf)

**Candidate method, synthesized:** Before adding an interface, write a realistic ordinary call, an invalid-input call and a recovery path. For an extension point, exercise a genuinely different implementation. Count conceptual obligations the caller must understand, not just the number of parameters or lines of wrapper code.

A small signature can conceal a large state machine. A builder can make many optional settings legible, but does not by itself define which settings conflict or whether partially built objects can escape. A short helper can improve an API when it removes an obligation the module can reliably own; a forwarding wrapper with no new guarantee can simply add navigation.

A callback or plug-in interface also has two audiences: callers and implementors. Making a method convenient for callers can add an obligation to every implementor. That distinction needs deliberate evaluation rather than a universal interface-per-class rule.

## Type design: distinguish interpretation from validity

The Rust API Guidelines use distinct types to separate interpretations of the same representation and deliberate types to make arguments meaningful. [COD-02, C-NEWTYPE/C-CUSTOM-TYPE](https://rust-lang.github.io/api-guidelines/type-safety.html)

**Our inference:** A newtype can prevent swapping UserId and OrderId while still permitting an empty or malformed value if its construction is unchecked. Static distinction, validated construction and current authorization are different guarantees.

| Desired guarantee | Candidate mechanism | What still needs checking |
| --- | --- | --- |
| Do not swap two kinds of identifier | Distinct types | Parsing and whether the identifier exists |
| Reject malformed external data | Fallible constructor/parser | Every path that bypasses that constructor |
| Represent mutually exclusive choices | Sum/enum representation | Version evolution and unknown choices |
| Make a legal call sequence visible | State-specific interface | Persistence, concurrent changes and stale state |
| Keep caller-owned data available | Explicit ownership/borrowing contract | Aliasing, lifetime and mutation on failure |

This table is a proposed reasoning aid, not a prescription to create five type layers. Its purpose is to expose missing guarantees. For a tiny internal function whose callers change together, documentation or existing language types may be enough.

The future-proofing guidance explains why public fields and implementation-shaped return types commit to representation, while explicitly allowing public fields for passive data structures. Sealing an extension point preserves some evolution freedom but public-method changes remain consequential. [COD-03](https://rust-lang.github.io/api-guidelines/future-proofing.html)

**Candidate instruction:** State what users may inspect, construct, mutate or implement. Hide details when their freedom conflicts with a real invariant or anticipated evolution. Do not add getters, setters or sealing solely to conform to a style.

## Case 1: Rust exact reads—one failure result can conceal different partial effects

**Question:** Can a caller assume that a failed exact read leaves its buffer and input position unchanged?

At the pinned revision, Read::read returns a count and allows short successful reads. read_exact promises a full buffer on success, retries Interrupted and leaves error-buffer contents and consumed-byte count unspecified. [COD-06, trait documentation L675–756 and L912–963](https://github.com/rust-lang/rust/blob/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/io/mod.rs#L912)

The default helper loops, advances after successful reads, ignores interruption and errors if input ends early. The slice specialization can exhaust short input and return without copying into the destination. [Default L556–568](https://github.com/rust-lang/rust/blob/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/io/mod.rs#L556), [slice L288–309](https://github.com/rust-lang/rust/blob/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/io/impls.rs#L288)

Selected tests use a chained reader and short slices; the short-slice test asserts an untouched destination for that optimized path. [COD-07, L154–187](https://github.com/rust-lang/rust/blob/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/io/tests.rs#L154)

**What this teaches, our synthesis:**

- Success shape and failure effects need separate specifications.
- A property asserted for one implementation is not automatically part of the trait contract.
- Returning an error does not establish rollback of input consumption.
- A caller that needs resumable progress must select or design a suitable contract.

This is a useful limit on the blanket heuristic “every method must be failure-atomic.” An interface may intentionally choose partial progress and leave some state unspecified. The design work is deciding whether that fits the caller's recovery needs and documenting it clearly.

**Proposed evaluation:** Supply a parser that retries read_exact after an error as if nothing was consumed. Ask an agent to identify its assumption, inspect both implementation paths and propose a contract-compatible recovery strategy. Penalize inferring a universal guarantee from the slice test or claiming an unexecuted test passed.

## Case 2: Go errors—the same text can expose a different API

**Question:** Does adding error context preserve or expand what a caller may depend on?

The Go 1.13 explanation distinguishes contextual formatting from exposing an underlying error. Wrapping can make a database-specific error part of the package contract; whether to expose it depends on the abstraction. [COD-08, “Whether to Wrap”](https://go.dev/blog/go1.13-errors)

In the pinned fmt implementation, Errorf selects a plain error, unary wrapper or multi-error wrapper according to formatting. External-package tests distinguish the rendered message from the unwrap shape. [COD-11, errors.go L22–78 and associated tests](https://github.com/golang/go/blob/6885bad7dd86880be6929c02085e5c7a67ff2887/src/fmt/errors.go#L22)

The pinned errors.Is handles equality, custom matching and unary/multi-error traversal; errors.Unwrap alone recognizes only the unary method. Tests include nested and multi-error callers. [COD-10, wrap.go L17–77](https://github.com/golang/go/blob/6885bad7dd86880be6929c02085e5c7a67ff2887/src/errors/wrap.go#L17)

**Trace to compare:**

| Interface choice | Caller-facing question |
| --- | --- |
| Context plus ordinary formatted error | What diagnostic text is shown? |
| Context plus wrapped implementation error | Can callers classify using an implementation-specific sentinel/type? |
| Context plus package-owned classification | Which stable conditions does this package promise? |
| Joined/multi-error result | Does caller inspection traverse the supported tree shape? |

The table is a design comparison, not a claim that one choice always wins. A caller-provided reader can make its underlying errors relevant to the caller. A private storage implementation may warrant a package-owned classification instead.

**Important distinction:** Avoiding wrapping does not redact the text or constitute a security boundary. The point here is machine-inspectable identity; presentation and information disclosure need their own decisions.

The original error-inspection proposal records design rationale, but proposed details must not be treated as shipped behavior. The later implementation's multiple-error shape also means a 2019 chain-only account is incomplete for the selected 2024 snapshot. [COD-09](https://go.googlesource.com/proposal/+/master/design/29934-error-values.md)

**Proposed evaluation:** Ask the agent to replace a storage implementation while preserving the public “not found” behavior. Provide callers using string matching, sentinel equality and errors.Is. Reward identifying which dependencies are promised versus accidental, and a minimal adaptation plan. Penalize “always wrap every error” and “never expose errors.”

## Case 3: Protobuf—parseability, preserved information and meaning diverge

**Question:** Can an old intermediary relay a new field without losing information?

The proto3 guide distinguishes binary-safe evolution from source compatibility and warns that JSON conversion or field-by-field reconstruction can lose unknown fields. [COD-12, “Updating A Message Type” and “Retaining Unknown Fields”](https://protobuf.dev/programming-guides/proto3/)

The field-presence note shows that explicit zero and absence differ. A message round trip through an implicit-presence peer can lose the original presence even while both peers accept the wire data. [COD-13, “Considerations for change-compatibility”](https://protobuf.dev/programming-guides/field_presence/)

ProtoJSON uses field/enum names and defaults to rejecting unknown fields; ignoring unknowns is an option rather than preservation. Its compatibility rules therefore differ from binary rules. [COD-14, JSON Wire Safety and Options](https://protobuf.dev/programming-guides/json/)

**Pinned implementation trace:**

| Path | Observed branch |
| --- | --- |
| Binary dispatcher | Can select generated methods or a reflective slow path. |
| Binary slow path | Consumes an unknown field and appends raw bytes unless DiscardUnknown is set. |
| JSON decoder | Unknown field produces an error, or is skipped when DiscardUnknown is set. |

Receipts: [COD-15, binary L85–121 and L175–186](https://github.com/protocolbuffers/protobuf-go/blob/c33baa8f3a0d35fd5a39e43c22a50a050f707d34/proto/decode.go#L85), [JSON L201–210](https://github.com/protocolbuffers/protobuf-go/blob/c33baa8f3a0d35fd5a39e43c22a50a050f707d34/encoding/protojson/decode.go#L201). Generated fast-path internals were not audited.

Fixtures encode retained/discarded unknown binary data and unknown JSON rejection/skipping; the test harness invokes public options. [COD-16, binary fixtures L1054–1079](https://github.com/protocolbuffers/protobuf-go/blob/c33baa8f3a0d35fd5a39e43c22a50a050f707d34/proto/testmessages_test.go#L1054), [JSON fixtures L1554 and L2539 onward](https://github.com/protocolbuffers/protobuf-go/blob/c33baa8f3a0d35fd5a39e43c22a50a050f707d34/encoding/protojson/decode_test.go#L2539). These tests were read, not run.

**Original teaching diagram of a possible relay, not a traced production deployment:**

~~~mermaid
flowchart LR
    N["New producer"] --> B["Binary old reader"]
    B --> R["Binary re-encoding"]
    B --> J["JSON conversion"]
    R --> C["New consumer"]
    J --> C
~~~

Each edge needs a representation and option declaration. “Old reader” alone says too little. Unknown bytes, field presence and unknown enum handling are separate questions; a relay that preserves one need not preserve all three.

**Proposed evaluation:** Give the agent an old/new schema pair, a binary relay and a JSON side channel. Ask which paths preserve an added field and an explicit zero, then require the necessary mixed-version test cases. Penalize “adding an optional field is always safe,” or an ignore-unknown option presented as lossless forwarding.

## Compatibility requires a caller model

AIP 180 separates source, wire and semantic compatibility and explicitly scopes its strict guidance to independently updated consumers. Limited/co-deployed internal clients may have different requirements. [COD-18, Guidance and scope note](https://google.aip.dev/180)

Hyrum's original account warns that consumers can depend on observable implementation details. It is a practitioner's observation from migrations, not a proof that change is impossible. [COD-17](https://www.hyrumslaw.com/)

**Candidate contract inventory, synthesized:**

| Dimension | An observation to inspect |
| --- | --- |
| Source/interface | Can an old caller still construct, implement, name and match the API? |
| Representation | Do old readers accept, retain and re-emit the value? |
| Semantics | Does absence/default/error/order mean the same thing? |
| Effects and lifecycle | Does failure consume input, mutate state, cancel work or retain ownership? |
| Operational assumptions | Does the caller depend on latency, resource cost, environment or minimum toolchain? |

Not every edit requires an exhaustive inventory. Select the dimensions exposed by the changed behavior. A purely local helper may allow an atomic call-site migration; a public library or persisted message can require compatibility across time and independently updated peers.

Rust RFC 1105 helps explain the distinction between every theoretical downstream break and versioning policy, but it is a historical document with then-unimplemented features. [COD-04](https://rust-lang.github.io/rfcs/1105-api-evolution.html)

For present Rust-specific classification, the maintained Cargo guide describes major, minor and possibly-breaking changes. Exhaustive enum additions and later construction restrictions have concrete caller implications. Its own introduction treats runtime consequences as judgment-dependent. [COD-05](https://doc.rust-lang.org/cargo/reference/semver.html)

**Our inference:** “It only adds something” is not sufficient reasoning. Adding a variant can break exhaustive matching; adding a required input can invalidate old callers; adding output can overwhelm a consumer or trigger an unknown-field rejection. The relevant check is an actual old caller or reader under the promised compatibility scope.

## Candidate rules to test, not install yet

1. **Start with a caller task and recovery path.** A signature is successful when a caller can complete the intended job without inventing hidden sequencing or parsing diagnostic strings.
2. **Choose precise guarantees.** Distinguish interpretation, validated values, runtime authority and preserved state. Specify effects on success, failure and partial completion.
3. **Limit commitments deliberately.** Exposed fields, error identities, extension points and representation types can become promises. Hide only what has a meaningful reason to remain changeable.
4. **Trace changed contracts through their real boundaries.** Include alternate encodings, persistence and old consumers when applicable. A matching generated type is not evidence that every path preserves the value.
5. **Verify meaningful outcomes.** Use real caller examples and discriminating old/new scenarios. Keep accidental implementation behavior separate from the supported contract.

These instructions should remain conditional. They do not imply maximum abstraction, wrapping every scalar, exhaustive migration plans for private helpers, or a fixed number of layers.

## Relationship to existing skills

The local [propagate-contract-changes](../../../skills/propagate-contract-changes/SKILL.md) already covers following requested semantics through producers, boundaries and consumers. The local [refactor-by-invariant](../../../skills/refactor-by-invariant/SKILL.md) covers moving responsibility while preserving behavior.

This research adds reasons and examples for deciding what the contract should be before propagation and how to recognize a meaningful caller-facing invariant before refactoring. It should not duplicate those workflows into a giant automatic “code quality” skill.

A provisional organization is:

- A compact **design-code-and-contracts** entrypoint for API/type/error/state decisions.
- Conditional references for language-specific extension and compatibility rules.
- Annotated examples organized by the mistake they expose: partial effects, abstraction leakage, representation loss and accidental commitments.
- Existing change-propagation/refactoring workflows retained for their distinct jobs.

This is a hypothesis about useful boundaries. It needs evaluation on actual tasks, including small edits where needless ceremony is the failure mode.

## Research trail, gaps and future checks

Search vocabulary included caller-oriented API design, Rust type safety and API evolution, Go error inspection/wrapping, protobuf binary versus JSON evolution, field presence and implicit interfaces. Follow-through used original Bloch slides, project-maintained guidance, original Go proposal rationale and exact release source/test paths.

The versioned Rust 1.81 online rustdoc URL could not be retrieved. The contract was instead read directly from the matching pinned source comments; newer online rustdoc was reconnaissance, not substituted for version identity. Bloch's slide deck was read from a university-hosted copy; it is author material, not a secondary summary.

Remaining gaps:

1. No code was executed, no new API compiled and no mixed-version round trip was run.
2. This is not an empirical comparison of programming paradigms or languages; most principles are expert/project guidance.
3. Rust ownership/unsafe invariants, C ABI, JavaScript structural typing, cancellation and asynchronous resource cleanup need further focused cases.
4. Protobuf-Go generated fast paths and full format conformance were not audited; the presence example remains documented semantics rather than a reproduced experiment.
5. API usability needs evaluation with realistic callers. Neither a shorter signature nor more type wrappers establishes reduced user error.

A useful next research step is to run the three proposed tasks independently with and without candidate guidance, while holding supplied source artifacts constant. Score justified guarantees, caller complexity and compatibility errors before evaluating polish or terminology.

