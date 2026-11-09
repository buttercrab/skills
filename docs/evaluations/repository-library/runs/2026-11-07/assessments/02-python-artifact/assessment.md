# riverfmt installed-content assessment

Prioritize declaring and testing the bundled alias table. The inspected source has a packaging configuration gap and a verification path that cannot catch it. The snapshot does **not** establish whether the actual 1.4.0 release archives contain the table or work for installed users.

## Scope and evidence

This is an assessment and prioritized plan for the fictional, supplied repository snapshot at `/private/tmp/repository-quality-assessment-20261107/02-python-artifact/repository`. No repository code, tests, builds, installers, helper scripts, git commands or network requests were executed. File reads and source/configuration tracing were the only checks. No implementation changes were made.

The README identifies downstream installers as the audience: `pip install riverfmt`, Python 3.10+, and `normalize("QTY") == "quantity"` using bundled defaults (`README.md:2`). There is sufficient intent to assess that contract without a human clarification.

## Representative change path

For an alias-table update, edit `src/riverfmt/defaults.json:1`, keep its behavior covered through `tests/test_labels.py:1-5`, and preserve the documented result in `README.md:2`. The public import is exported at `src/riverfmt/__init__.py:1-2`; `src/riverfmt/labels.py:5-7` opens the resource from the installed `riverfmt` package on **every call**. The publication unit is the `riverfmt` distribution, version 1.4.0, discovered under `src` by `pyproject.toml:5-15`. The release path is a locally built, manually uploaded distribution (`README.md:5`), not the configured source-tests job.

## Findings

1. **High priority — required runtime resource has no positive packaging declaration.** `pyproject.toml:11-15` discovers Python packages under `src` but explicitly sets `include-package-data = false`; no explicit `package-data` rule, manifest or alternative build hook appears in the supplied snapshot. `defaults.json` is a non-Python runtime input, and `labels.py:6` unconditionally reads it. This configuration provides no visible inclusion path for it; an ordinary build from these inputs is expected to omit it from the wheel unless an unobserved mechanism supplies it. If omitted, invoking `normalize`, even for an unrecognized value, fails at the resource read rather than providing the documented normalization. This is a demonstrated configuration gap with a concrete failure mechanism, **not an inspected-wheel result or confirmation that published 1.4.0 is broken**. The supplied guide cards do not provide a freshly inspected setuptools package-data specification, so exact backend/version behavior remains a verification item.

2. **High priority — configured validation bypasses the consumer boundary.** Both `README.md:4` and `.github/workflows/check.yml:11-12` run `PYTHONPATH=src python -m pytest`. The sole test (`tests/test_labels.py:5`) usefully asserts the promised QTY alias, but imports it from the source path, where the JSON file exists. The workflow installs pytest, not a built riverfmt artifact; it neither builds nor inspects nor installs a wheel/sdist. Consequently, even a future green run of this job would not show that the JSON reaches installed consumers. No run result is available here.

3. **Release confidence is unresolved; the release text is not artifact evidence.** `release-record.txt:1-5` is explicitly a fixture transcription. It names tag v1.4.0, release-page wording asserting retained bundled defaults, and wheel/sdist filenames. These agree with the manifest version but contain no archive bytes, hashes, logs or consumer results. They support the existence of the supplied recorded claims, not registry availability, artifact contents, source-to-release correspondence or successful installation. The README's manual workflow is not itself a defect; its artifact evidence is missing from this snapshot.

The existing small `src/riverfmt` plus external `tests` structure is navigable and appropriate. Keep it. A directory migration, backend replacement, release orchestration platform, coverage target or larger documentation hierarchy would not address the observed resource boundary.

## Prioritized plan (proposed, not executed)

1. **Make the resource part of the distribution contract.** In `pyproject.toml`, retain the existing layout/backend and add an explicit setuptools package-data declaration for `riverfmt = ["defaults.json"]` under `[tool.setuptools.package-data]`, subject to checking the selected setuptools version's exact semantics. Keep the resource authoritative in `src/riverfmt/defaults.json`; do not duplicate it into tests or a manually maintained distribution folder. Success means both the directly built wheel and a wheel built from the sdist carry the resource. This is a small configuration change; build evidence is still required before accepting it.

2. **Add a focused artifact check beside fast source tests.** Extend `.github/workflows/check.yml` and its README instructions to build wheel and sdist, inspect their members and metadata, install the wheel into a clean environment, and run a public-API smoke scenario from outside the checkout with `PYTHONPATH` unset. Assert `normalize("QTY") == "quantity"` and `normalize("Unit Price") == "price"`; also assert an ordinary whitespace/case fallback such as `normalize(" Other ") == "other"`. Check that the imported module comes from the installed environment. Independently build a wheel from the unpacked sdist and repeat the installed checks, so the sdist route cannot inherit files accidentally from the checkout. Record artifact identity and interpreter. These are proposed acceptance checks, not commands run in this assessment.

3. **Connect the manual release to the validated files.** Add a short release checklist to the existing README: retain archive contents, hashes, build environment and installed smoke results for the exact files intended for upload; after any separately authorized publication, compare the distributed files with those validated artifacts. For a future fix, describe the bundled-defaults effect in human release notes and select a new version through the existing release policy. Do not replace already published 1.4.0 files based on this assessment. If 1.4.0 archives later become available, inspect them before claiming a released defect or recovery.

4. **Cover the stated interpreter floor proportionately.** The README and `requires-python` promise Python 3.10+, but the configured job selects only 3.12 (`.github/workflows/check.yml:10`). Add at least an artifact smoke check on 3.10 and the project's chosen current supported interpreter, alongside existing source tests. This is a support-evidence gap, not a demonstrated incompatibility or a requirement to copy a large framework's full platform matrix.

## Reference choices and limits

| Local card and portion read | Fit and adaptation | Decisive mismatch / limit |
| --- | --- | --- |
| `quality-python-distribution-checks`, What to inspect / What to borrow and adapt / Mismatches | Its resource → artifact → installed invocation chain directly matches riverfmt; use it to design wheel and sdist consumer checks. | Editable-install guidance alone cannot prove regular artifact contents. Only the local card was read; its linked PyPA, pytest and PEP sources were not freshly fetched. |
| `quality-python-import-layout`, What to inspect / What to borrow and adapt / Mismatches | Explains why `PYTHONPATH=src` and the directory name do not establish installed-package coverage. Retain `src`, repair validation. | This project already uses `src`; a migration offers no relevant benefit. No primary tool documentation was freshly read. |
| `quality-python-build-metadata`, What to inspect / What to borrow and adapt / Mismatches | Keeps setuptools/wheel build requirements separate from runtime and development needs; preserve the existing backend. | Does not specify exact setuptools JSON inclusion semantics. That detail needs backend documentation and an actual artifact check later. |
| `repo-small-flask`, What to inspect / What to borrow and adapt / Mismatches | Neighboring Python library example reinforces separate source/test/packaging purposes and support-specific validation. | Flask's Flit backend, framework complexity and dependency matrix should not transfer. Pinned upstream files were not independently inspected. |
| `repo-small-p-limit`, What to borrow and adapt / Mismatches | Small-library counterexample supports keeping the tree compact while making the distributed-file contract explicit. | Node/npm exports, declarations and commands do not apply to setuptools. No upstream tarball or primary repository was inspected. |

The cards are contextual secondary guidance read locally, not fresh primary inspection or successful checks. Network and upstream execution were prohibited; their source receipts were not promoted into this assessment's own evidence. Backend-specific claims remain bounded accordingly.
