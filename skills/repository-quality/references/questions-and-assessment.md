# Questions and a grounded repository assessment

Use this when the request is broad, the intended repository users are unclear, or an assessment needs a defensible starting point. There is no mandatory interview or scoring form.

## Resolve context from evidence first

Inspect applicable local instructions, manifests, entry docs, actual source layout, validation definitions and publication configuration. Separate the repository's present behavior from its intended audience or future promises. Discover the language, toolchain and scripts yourself; ask about consequential intent that files cannot settle.

| Decision | Evidence to inspect | Human-owned uncertainty worth asking about |
| --- | --- | --- |
| Reader journey | README, examples, API/reference docs, contribution entry | Is the immediate problem consumer adoption, contributor setup or ongoing maintenance? |
| Supported artifact | Manifest exports, build inputs, distribution config | Is this source-only/internal work, a deployed app, or a versioned package with external consumers? |
| Compatibility | Version support, tests and release notes | Which existing users or downstream workflows must remain compatible? |
| Collaboration | Current contribution/ownership route | Will occasional external contributors participate, or is this maintained by a small known team? |
| Maintenance cost | Existing commands/CI, generators, tools | Which additional recurring work is acceptable, and which friction should improve first? |

For example, ask: “Should a new user install a released package, or do collaborators run this directly from the checkout? That changes whether an installed-artifact check is relevant.” Do not ask which folder name they prefer before establishing that distinction.

Keep partial answers, delegation and established constraints in force. A pending answer is not resolved by time passing; label independent provisional work. Do not issue the same question through multiple channels or preserve questions whose branch was superseded by a later answer. If the person asks only for an assessment, deliver findings and a bounded proposal rather than implementing them automatically.

## Select a representative task

Choose one or a few paths proportional to the requested scope. Examples: add a CLI option; fix an exported function; update an event-processing contract; revise a tutorial; correct a packaging omission. Use real supplied tasks when available; label an inferred example.

Trace:

1. Where a contributor discovers the owning source and prerequisites.
2. Which file is authoritative, including generated/schema inputs and ownership boundaries.
3. Which implementation, tests, docs and distribution declarations change together.
4. Which relevant checks exist, which were run, and what a consumer actually receives.

Do not require physical co-location for every related artifact. A conventional split can be navigable through clear names, explicit commands and cross-links. Conversely, folders named `domain/`, `services/` and `tests/` do not demonstrate coherent dependencies or useful coverage.

## Make a finding reviewable

Tie a finding to inspected evidence and its practical consequence. “The contribution guide names a removed command; the manifest and CI use its replacement” is stronger than “docs need improvement.” “No release artifact was inspected” is an unknown, not proof that publishing is broken.

A useful assessment can distinguish:

- **Observed obstacle:** contradictory instructions, an orphaned generated output, missing published entry, or a confirmed unusable path.
- **Supported risk:** source-only validation may miss a consumer boundary; whether it does so here remains to be tested.
- **Contextual option:** a different layout or workflow could reduce demonstrated friction, with a stated migration cost.
- **Unknown:** no current run, permissions, protection configuration or actual distributed artifact was inspected.

Do not aggregate these into an arbitrary repository score. Prioritize by affected people, likely frequency, cost of failure and reversibility. Respect a request for a small recommendation set. Keep “retain the current structure and repair the entry path” available when it resolves the problem.

## Illustrative contrast

A forty-line internal reporting script with one known maintainer may need a truthful run example and a clear input contract, not a package workspace, release automation and a contribution hierarchy. A small library consumed through wheels or npm packages may justify artifact-boundary checks even with very few source files. The number of folders or contributors alone does not settle that distinction.
