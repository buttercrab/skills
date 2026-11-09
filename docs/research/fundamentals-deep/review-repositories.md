# Independent evidence review: repository research

Reviewed 2026-11-07. Scope: six consequential claim groups in [repositories.md](repositories.md) and its [ledger](repositories.sources.jsonl). This is a source review, not a repository audit. External code was read only; no generator, tests, publishing workflow or installer ran.

**Finding:** The selected claims are supported by the inspected source versions. No demonstrated implementation defect or materially unsupported conclusion was found. Two empirical-source limitations deserve explicit preservation when converting the research into skill rules.

## Claim checks and receipts

### 1. uv: generated reference authority and modes — supported

At the recorded revision, the CLI generator derives output from Cli::command(), calls build() before inspection, and distinguishes stdout, comparison and writing. The default Mode is Write. These support the report's distinction between generation success and checked-in freshness.

Receipts: [generate_cli_reference.rs L38–101](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/crates/uv-dev/src/generate_cli_reference.rs#L38-L101), [generate_all.rs L17–27](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/crates/uv-dev/src/generate_all.rs#L17-L27).

Boundary: selected generator behavior was inspected. It does not prove all generators implement their modes identically.

### 2. uv: validation and publication chains — supported, with a useful endpoint distinction

The generated-files workflow uses DryRun broadly and selected Check calls. Both documentation workflows regenerate four references before strict MkDocs builds. Publication subsequently copies output into a separate docs repository, creates a PR and conditionally merges it for explicit release plans.

Receipts: [generated-files L43 onward](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/check-generated-files.yml#L43), [check-docs L37–45](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/check-docs.yml#L37-L45), [publish-docs L48 onward](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/publish-docs.yml#L48), especially L84, L107, L120 and L146.

No drift-enforcement defect follows from DryRun alone. Equally, configured regeneration does not establish a successful run or live-site freshness. The existing evidence boundary states this appropriately.

### 3. Django: optional renderer coverage — supported

The exact commit contains six changed files covering two templates, widget behavior, tests, reference and release notes. The helper catches missing jinja2, conditionally constructs its renderer and conditionally exercises it. The Django renderer still runs.

Receipts: [six-file commit](https://github.com/django/django/commit/a1f2b45ce5a327f42437bdb620a817839d0bd067), [helper L4–36](https://github.com/django/django/blob/a1f2b45ce5a327f42437bdb620a817839d0bd067/tests/forms_tests/widget_tests/base.py#L4-L36).

This supports “test scope depends on installed dependencies.” It does not show that the actual CI environment omitted Jinja2 or missed the regression. The report does not make that stronger claim.

### 4. Kubernetes: independent publication checks — supported as configuration

The client-go destination specifies branch dependencies and smoke scripts containing standalone build and test commands. That supports the report's release-unit distinction.

Receipt: [publishing/rules.yaml L118–197](https://github.com/kubernetes/kubernetes/blob/3a92e6afd51585de38b0916494c7bf7c638b1b74/staging/publishing/rules.yaml#L118-L197).

Missing execution evidence is not a defect. This check did not inspect publishing-bot scheduling or smoke-test interpretation, run those commands, or confirm mirror synchronization. “Configured standalone smoke steps” is more precise than “publication verified.”

### 5. Coverage study: suite size and effectiveness — supported

The 2014 paper samples 31,000 suites across five Java systems, measures mutation-based effectiveness and controls suite size. Its limitations acknowledge assumed-equivalent mutants and restricted high-coverage sampling.

Receipt: [original paper, abstract, §§3.3–3.4 and 6](https://cs.uwaterloo.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf).

The report correctly avoids treating weak association as proof that relevant tests or coverage have no value. Another limitation worth retaining is that rare very-high-coverage suites restrict conclusions about that region. No target-specific coverage gate should be removed on this evidence alone.

### 6. Complexity studies: limited proxies, not quality certificates — supported with source ambiguity

The 2020 meta-analysis separates time, ratings and correctness. It explicitly lacks a supported threshold; most snippets have low Cognitive Complexity and only two constituent studies include values over 15.

Receipt: [original HTML, §§3.2,5.1–5.3](https://arxiv.org/html/2007.12520).

The early-career paper reports weak severity correlations but does not support severity prediction. Its Table 9 labels and adjacent scale-description prose use opposite directions, so a directional interpretation needs clarification from underlying data.

Receipt: [original version 2 HTML, Tables 8–10, §5.3 and conclusion](https://arxiv.org/html/2303.07722v2).

The current broad conclusion—metrics as investigative leads—is defensible. Avoid translating either study into a universal threshold or inferring “more complex means more severe” from this evidence.

## Actionable refinements

1. Add the low-complexity/high-value sampling caveat to REP-26 before using that study to justify metric thresholds. This is an evidence limitation, not a refutation of the reported correlations.
2. Record REP-27's severity-coding ambiguity if directional severity claims are introduced. The existing weak-association summary does not require reversal.
3. Preserve the configured/run/published distinction in any condensed skill. The repository report already does this; a short derivative could accidentally erase it.
4. Link uv's workflow files directly in the narrative near the cross-workflow claim, not only through additional_urls in the ledger. The underlying evidence is present; this improves verification cost.

No source files or repository-research artifacts were changed during this review.

