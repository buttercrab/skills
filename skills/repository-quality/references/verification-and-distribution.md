# Verify the maintenance and consumer promise

Use this for test selection, generated artifacts, packaging and release guidance. Source inspection and actual execution support different claims. This is a conditional menu, not a demand to run every check or perform a release.

## Evidence layers

| Evidence | Supports | Does not establish |
| --- | --- | --- |
| Documented command | The guide describes this workflow at its inspected version. | The command still exists, succeeds or covers all promised environments. |
| Manifest/workflow/source read | The inspected configuration or implementation specifies these mechanics. | A green run, enforced review, current permissions or a deployed artifact. |
| Local check run | This command returned this result under the recorded environment. | Unrun optional dependencies, other platforms, distribution integrity or publication. |
| Package/build inspection | These inspected contents and exports are present in this artifact. | Real installation or consumer execution, provenance, or registry availability. |
| Consumer-boundary exercise | This artifact works for this specific installed/consuming scenario. | Compatibility across all supported versions, or a shipped release. |
| Release observation | The specific publication/version was observed from its owning source. | That all consumers received it or production behavior is healthy. |

For each consequential check, state why it reaches the affected contract. A default test command may omit an optional renderer, backend, compiler target or native dependency. A workflow may run a generation smoke test without comparing checked-in files; another step may regenerate them before publication. Follow the whole relevant chain before declaring drift enforcement broken.

## Test changes, not a metric target

Choose focused checks for behavior, public contracts and failure modes changed by the work. Read existing fixtures and assertions rather than treating test count or coverage as a quality score. High execution coverage can still miss assertions or input classes; a low global figure does not identify the correct new test by itself.

Inspect the actual scope of a successful run. Preserve optional skips and unavailable environments. Do not create tests that simply search for the wording of a new README or mirror an implementation. Navigation/link or generated-output consistency checks can be meaningful when they protect the relevant boundary.

Avoid blindly executing setup or package listing commands from a reference. Build/packaging tools can run project hooks; inspect what will execute and follow the task's authorization and environment restrictions. A read-only source assessment can remain useful without running upstream software.

## Source tree versus distribution

When consumers install an artifact, trace the included source, type declarations, package data, generated files, exports and compatibility metadata. Compare that boundary with what local tests import or load. Source-checkout success can be misleading when tests bypass the package entirely; a source-only internal tool may not need a distribution stage at all.

For workspaces, identify authoritative modules, shared development resolution and independent consumer requirements. Check that a local cross-package link is not the only reason an import resolves. The appropriate artifact/install check depends on the language and actual distribution route; use the relevant primary card instead of importing another ecosystem's commands.

A reproducible artifact, a signed attestation, dependency scanning and runtime behavior answer different questions. Inspect their inputs and verification expectations before recommending them. Provenance records do not prove that source is benign or functionality correct. Repository security heuristics are investigative leads; unknown permissions or unavailable signals are not demonstrated configuration defects.

## Releases without accidental publication

Find how release units, versioning, compatibility commitments and user-facing change notes align. Semantic versioning is meaningful only against a defined public contract. Changelog and release orchestration practices can help communicate changes, but do not require a multi-package release platform for an unpublished script.

Assessing or improving a repository does not itself request a release, new credentials, signing access, altered protections or external publication. Record a proposed validation/release sequence at the requested scope. Separate prepared artifacts, passing checks, published versions and observed deployment. A blocked download is a setup failure, not a passing type check; once resolved, run the original promised check rather than substituting an easier one.
