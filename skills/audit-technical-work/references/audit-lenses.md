# Audit Lenses

Use the relevant lens rather than loading every criterion into every review.

## Architecture and ownership

Trace who owns a decision or invariant, who supplies inputs, and who consumes its result. Look for duplicated production decisions, competing state, reverse dependencies, and wrappers that conceal duplication. Evaluate an abstraction by responsibilities and dependencies removed, not file counts or names. Preserve independent test oracles: a second implementation used to derive an expected result may be valuable evidence rather than redundant product logic.

## Security and privacy

Trace identities, trust, permissions, sensitive data, and the boundaries where they change. Support an exploit finding with a reachable trigger and unsafe result; distinguish an unverified risk from a demonstrated exploit. For fail-closed contracts, check whether absent or untrusted metadata actually denies access through every relevant seam. Verify mitigations with negative cases as well as successful requests. Keep secrets and sensitive payloads out of reports and test output.

## Completion and specification

Extract the normative requirements relevant to the requested assessment, including failure behavior and examples that promise observable semantics. Match each to current evidence of appropriate scope. Inspect the actual required path when integration, deployment, or user behavior is claimed; mocks and narrow tests may support components but cannot replace that path. Mark missing evidence unverified, and demonstrated violations failed. Avoid vacuous passes such as an empty suite, skipped test, or fixture that repeats the implementation's answer.
