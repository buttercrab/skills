# Independent source sample: p-limit and Click cards

Date: 2026-11-07. Reviewed only `repo-small-p-limit.md` and `repo-small-click.md`, then independently fetched their exact pinned primary source artifacts through the GitHub connector. No assessment fixtures, sibling reviews or lane notes were read. No upstream code, test, installation or packaging command was executed; no card or example repository was edited.

## Result

No demonstrated material source-to-change-path misattribution. Both cards correctly separate inspected configuration/tests from a passing run or observed distribution. Two small precision improvements would make the selected mechanisms harder to overread:

1. **p-limit — preserve the Node 20 test exclusion.** Add a sentence near the queue-clearing verification path: the rejection-specific clearQueue tests are conditionally skipped on Node 20 because of a documented AVA/DOMException issue. The current statement that CI selects Node versions is accurate, but its juxtaposition with the clearQueue trigger could be read as the same scenario running across the whole matrix. This is a scope clarification, not evidence that the implementation fails on Node 20. Receipt: [test.js line 197](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/test.js#L197), with the matrix in [main.yml](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/.github/workflows/main.yml).
2. **Click — describe the filesystem replacement as a combination.** In “What to inspect,” replace “temporary directories or absolute paths” with “temporary directories accessed through absolute paths” (or the named TemporaryDirectory/tmp_path alternatives). The deprecation guidance combines storage isolation with avoiding process-global cwd changes. It does not make concurrent `CliRunner.invoke` thread-safe. The card's other passages already preserve that stream-state limit. Receipts: [testing.py line 807](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/src/click/testing.py#L807), [replacement test line 589](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/tests/test_testing.py#L589), [thread-safety test explanation line 610](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/tests/test_testing.py#L610).

## p-limit: independently supported chain

Revision: `a8a6fbec4e0e866d6d779b10889bb4f5567e70eb`. All six cited artifacts retrieved successfully: package.json, index.js, index.d.ts, test.js, readme.md and .github/workflows/main.yml.

- Manifest exports separate runtime/type entrypoints; its aggregate test command invokes xo, ava and tsd. The explicit files list is inspected packaging intent, as the card says, not an observed npm tarball.
- The clearQueue branch separates dropping queued work from rejecting pending promises when configured; declarations and README describe the same opt-in boundary without claiming cancellation of already-running work.
- The map catch branch attaches rejection observers to already-scheduled promises when iterable construction throws. [The named test at line 298](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/test.js#L298) waits for queued work and checks the associated outcome; adjacent tests separately preserve iterable-error precedence and scheduled execution. The card's scenario attribution is supported.
- Workflow configuration invokes the aggregate command on Node 20/22/24, with the scenario-specific skip above. No CI logs, published package or benchmark was inspected.

The adaptation remains appropriately narrow: a small maintenance surface is a counterexample to compulsory layering, not proof of low coupling or universal flat-layout suitability.

## Click: independently supported chain

Revision: `8abb77a8432e03ed14a95f972b44f905279415a7`. All five cited artifacts retrieved successfully: README.md, pyproject.toml, src/click/testing.py, tests/test_testing.py and .github/workflows/tests.yaml.

- README routes contribution guidance to the Pallets site. This review did not follow that external guide; the card accurately states the same gap.
- pyproject.toml identifies development version `8.6.0.dev`, Flit sdist inclusion/exclusion intent and a wheel-based tox package. Distinct random/stress/typing/docs configurations are present. [Default pytest options at line 91](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/pyproject.toml#L91) exclude stress; the stress environment explicitly overrides that default. The ordinary workflow is not represented as covering stress or every documented environment.
- isolated_filesystem actually changes cwd and restores it in a finally block. Its current warning explains process-global cwd/stream state; deprecation and tests demonstrate a suggested migration rather than removal of the legacy helper.
- Workflow source declares the interpreter/platform matrix, typing job and docs/README path exclusions. It does not prove actual successful CI, wheel/sdist contents or compatibility of installed releases. The card's development-revision caveat is important and supported.

## Confidence and remaining gaps

High confidence in the sampled textual/configuration attributions; no runtime or distribution acceptance claim. Selected source/test sections were read closely, not every helper or every unrelated test. Type declaration-test contents, external contributor sites, release records, actual branch settings and downstream artifacts were outside this bounded review. Neither a successful fetch nor this review establishes that the configured commands succeed. The two recommended edits can be applied without expanding the cards or changing the library's scope.
