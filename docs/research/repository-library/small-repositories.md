# Repository cases: compact libraries, CLIs and their maintenance boundaries

Research date: 2026-11-07. Twelve curated repository cards trace 70 selected substantive source files across JavaScript/TypeScript, Python, Rust and Go. These are purposive contrasts, not a ranking, a random sample, 70 independent studies or proof of ecosystem prevalence. The `repo-small-*` ID prefix identifies this curation lane; uv and pytest retain multi-package/large-project applicability where appropriate.

## Method and evidence boundary

For each case, fetched the current branch commit through the connected GitHub API, read the exact-revision root listing to establish actual paths, then followed entry/contribution guidance, source/manifest inputs and tests/configuration/generation/distribution boundaries. Repository cards cite exact commit URLs and narrow sections. For large files, inspected the named functions and surrounding cases rather than claiming to audit every line. An authoring script created only original annotations in this skill workspace; no upstream source was cloned, installed, executed, tested or edited.

The earlier repositories dossier supplied candidate leads and useful contrasts. Every curated current claim here was checked against fresh pinned owning files. p-limit and uv resolve to the same commits as that earlier dossier; they were re-read, not silently relabeled as new evidence. Metadata/statistics about popularity were not used as quality evidence. Maintainer instructions are inspected source facts, not active instructions for this research.

## Pinned inventory and inspected portions

### sindresorhus/p-limit

Card: [repo-small-p-limit](../../../skills/repository-quality/library/entries/repo-small-p-limit.md). Commit: `a8a6fbec4e0e866d6d779b10889bb4f5567e70eb`.

- [package.json](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/package.json) — exports, scripts.test, files and engines.
- [index.js](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/index.js) — clearQueue and map error handling.
- [index.d.ts](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/index.d.ts) — public API declarations.
- [test.js](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/test.js) — clearQueue, iterable-error and concurrency scenarios.
- [readme.md](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/readme.md) — API: rejectOnClear, map, clearQueue.
- [.github/workflows/main.yml](https://github.com/sindresorhus/p-limit/blob/a8a6fbec4e0e866d6d779b10889bb4f5567e70eb/.github/workflows/main.yml) — Node matrix and npm test.

### pallets/click

Card: [repo-small-click](../../../skills/repository-quality/library/entries/repo-small-click.md). Commit: `8abb77a8432e03ed14a95f972b44f905279415a7`.

- [README.md](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/README.md) — usage and contributing route.
- [pyproject.toml](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/pyproject.toml) — Flit sdist, tox environments, pytest stress selection and typing.
- [src/click/testing.py](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/src/click/testing.py) — CliRunner.invoke and isolated_filesystem deprecation/warning.
- [tests/test_testing.py](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/tests/test_testing.py) — test_isolated_runner, replacement pattern and thread-safety explanation.
- [.github/workflows/tests.yaml](https://github.com/pallets/click/blob/8abb77a8432e03ed14a95f972b44f905279415a7/.github/workflows/tests.yaml) — platform/interpreter matrix and typing job.

### pallets/flask

Card: [repo-small-flask](../../../skills/repository-quality/library/entries/repo-small-flask.md). Commit: `49943b5a94413a530761350f04e896f76e8d620e`.

- [README.md](https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/README.md) — project-layout stance and simple application example.
- [pyproject.toml](https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/pyproject.toml) — dependencies, Flit packaging, tests-min/tests-dev and docs/typing.
- [src/flask/testing.py](https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/src/flask/testing.py) — session_transaction and open.
- [tests/test_testing.py](https://github.com/pallets/flask/blob/49943b5a94413a530761350f04e896f76e8d620e/tests/test_testing.py) — session transaction, IPv6 and context cases.

### psf/requests

Card: [repo-small-requests](../../../skills/repository-quality/library/entries/repo-small-requests.md). Commit: `3c7baaa05ab4aa49cc819ce3a819d260de19c157`.

- [README.md](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/README.md) — usage and supported-version statement.
- [pyproject.toml](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/pyproject.toml) — project metadata, src package discovery and test dependencies.
- [tox.ini](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/tox.ini) — interpreter/extras environments and pytest target.
- [src/requests/sessions.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/src/requests/sessions.py) — rebuild_auth and merge_setting.
- [tests/test_requests.py](https://github.com/psf/requests/blob/3c7baaa05ab4aa49cc819ce3a819d260de19c157/tests/test_requests.py) — redirect authentication and should_strip_auth cases.

### pytest-dev/pytest

Card: [repo-small-pytest](../../../skills/repository-quality/library/entries/repo-small-pytest.md). Commit: `171c924acfd66d03ab51d08da2509461da6233a7`.

- [CONTRIBUTING.rst](https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/CONTRIBUTING.rst) — reproduction guidance and documentation build/autodoc notes.
- [pyproject.toml](https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/pyproject.toml) — build backend and pytest testpaths/norecursedirs.
- [src/_pytest/pytester.py](https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/src/_pytest/pytester.py) — Pytester, runpytest and runpytest_subprocess.
- [testing/test_pytester.py](https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/testing/test_pytester.py) — makepyfile and inline-run module-cleanup tests.
- [tox.ini](https://github.com/pytest-dev/pytest/blob/171c924acfd66d03ab51d08da2509461da6233a7/tox.ini) — testenv command and doctesting factor.

### BurntSushi/ripgrep

Card: [repo-small-ripgrep](../../../skills/repository-quality/library/entries/repo-small-ripgrep.md). Commit: `91f5d22ef48bde459d90a8c7dbeab416e97d0f2b`.

- [Cargo.toml](https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/Cargo.toml) — binary target, autotests=false, explicit integration target and workspace members.
- [CONTRIBUTING.md](https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/CONTRIBUTING.md) — route to project contribution policy.
- [crates/core/flags/defs.rs](https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/crates/core/flags/defs.rs) — Follow/Hidden definitions, negated names, docs and parser tests.
- [tests/tests.rs](https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/tests/tests.rs) — integration modules and feature/regression routing.
- [tests/feature.rs](https://github.com/BurntSushi/ripgrep/blob/91f5d22ef48bde459d90a8c7dbeab416e97d0f2b/tests/feature.rs) — encoding scenarios using Dir/TestCommand.

### sharkdp/fd

Card: [repo-small-fd](../../../skills/repository-quality/library/entries/repo-small-fd.md). Commit: `39886c0cb34453cda21163df0c0c76fc9c011a21`.

- [CONTRIBUTING.md](https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/CONTRIBUTING.md) — contribution expectations and behavioral changelog boundary.
- [Cargo.toml](https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/Cargo.toml) — binary path, feature flags and test dependencies.
- [src/cli.rs](https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/src/cli.rs) — Opts hidden/follow flags, conflicts and negations.
- [tests/tests.rs](https://github.com/sharkdp/fd/blob/39886c0cb34453cda21163df0c0c76fc9c011a21/tests/tests.rs) — test_hidden, Windows attribute case, test_follow and filesystem boundaries.

### sharkdp/bat

Card: [repo-small-bat](../../../skills/repository-quality/library/entries/repo-small-bat.md). Commit: `c231941daa363e67657216922135e3cc2d5a4f93`.

- [CONTRIBUTING.md](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/CONTRIBUTING.md) — functional regression, syntax testing and changelog guidance.
- [Cargo.toml](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/Cargo.toml) — build script, excluded asset sources and application features.
- [src/syntax_mapping/builtins/README.md](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/src/syntax_mapping/builtins/README.md) — authored TOML organization and platform-specific inclusion.
- [build/main.rs](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/build/main.rs) — mapping generation and application-only man/completion generation.
- [doc/assets.md](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/doc/assets.md) — syntax source/highlighted regression workflow.
- [assets/create.sh](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/assets/create.sh) — cache clearing, patches and asset generation.
- [tests/snapshot_tests.rs](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/tests/snapshot_tests.rs) — feature-gated style snapshot scenarios.
- [.github/workflows/CICD.yml](https://github.com/sharkdp/bat/blob/c231941daa363e67657216922135e3cc2d5a4f93/.github/workflows/CICD.yml) — updated syntax/theme build and ignored-by-default checks.

### astral-sh/uv

Card: [repo-small-uv](../../../skills/repository-quality/library/entries/repo-small-uv.md). Commit: `5ce34500b8a3d16d24bc7576bd8ac64879091cea`.

- [CONTRIBUTING.md](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/CONTRIBUTING.md) — snapshot testing and Documentation section.
- [.cargo/config.toml](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.cargo/config.toml) — cargo dev alias.
- [crates/uv-cli/src/lib.rs](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/crates/uv-cli/src/lib.rs) — Cli, TopLevelArgs and command argument declarations.
- [crates/uv-dev/src/generate_cli_reference.rs](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/crates/uv-dev/src/generate_cli_reference.rs) — Mode handling, Clap build and reference rendering.
- [.github/workflows/check-generated-files.yml](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/check-generated-files.yml) — DryRun versus selected Check calls.
- [.github/workflows/check-docs.yml](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/check-docs.yml) — reference regeneration followed by strict docs build.
- [.github/workflows/publish-docs.yml](https://github.com/astral-sh/uv/blob/5ce34500b8a3d16d24bc7576bd8ac64879091cea/.github/workflows/publish-docs.yml) — release documentation generation and publication inputs.

### google/go-cmp

Card: [repo-small-go-cmp](../../../skills/repository-quality/library/entries/repo-small-go-cmp.md). Commit: `5deca1c7dab7d33c102d8d7a26794da148485563`.

- [CONTRIBUTING.md](https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/CONTRIBUTING.md) — local review and contribution terms.
- [go.mod](https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/go.mod) — module identity and Go directive.
- [cmp/compare.go](https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/cmp/compare.go) — Equal, Diff and comparison invariants.
- [cmp/compare_test.go](https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/cmp/compare_test.go) — TestDiff scenario reasons, panic expectations and golden updates.
- [.github/workflows/test.yml](https://github.com/google/go-cmp/blob/5deca1c7dab7d33c102d8d7a26794da148485563/.github/workflows/test.yml) — race tests, formatting and interpreter/platform matrix.

### spf13/cobra

Card: [repo-small-cobra](../../../skills/repository-quality/library/entries/repo-small-cobra.md). Commit: `adbc8813901bba65827259daa8e22ff94ec1f30e`.

- [CONTRIBUTING.md](https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/CONTRIBUTING.md) — reproduction context and documented test commands.
- [go.mod](https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/go.mod) — module/dependency and Go directive.
- [command.go](https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/command.go) — ExecuteC and InitDefaultHelpCmd.
- [command_test.go](https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/command_test.go) — help command, shadowed flags and unknown-command scenarios.
- [Makefile](https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/Makefile) — test/richtest and install_deps.
- [.github/workflows/test.yml](https://github.com/spf13/cobra/blob/adbc8813901bba65827259daa8e22ff94ec1f30e/.github/workflows/test.yml) — test platforms/toolchains and macOS linker flags.

### stretchr/testify

Card: [repo-small-testify](../../../skills/repository-quality/library/entries/repo-small-testify.md). Commit: `87a7b9d57689f6579db2da795ab8deeab29cb724`.

- [CONTRIBUTING.md](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/CONTRIBUTING.md) — API usefulness, maintenance expectations and review context.
- [go.mod](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/go.mod) — module identity and supported-version comment.
- [assert/assertions.go](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/assert/assertions.go) — Equal behavior and argument validation.
- [assert/assertions_test.go](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/assert/assertions_test.go) — TestEqual table of semantic cases.
- [require/requirements.go](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/require/requirements.go) — go:generate directive.
- [require/require.go.tmpl](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/require/require.go.tmpl) — fatal wrapper template.
- [require/require.go](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/require/require.go) — generated header and Equal forwarding.
- [_codegen/main.go](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/_codegen/main.go) — source parsing and generation entrypoint.
- [.ci.gogenerate.sh](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/.ci.gogenerate.sh) — generation and git-diff failure condition.
- [.github/workflows/main.yml](https://github.com/stretchr/testify/blob/87a7b9d57689f6579db2da795ab8deeab29cb724/.github/workflows/main.yml) — generation, format, vet and race-test routes.

## Material contrasts

- **Flat does not mean incomplete:** p-limit exposes runtime, declarations, runtime/declaration tests and a manifest distribution list in a tiny tree. Additional layers need a maintenance benefit, not a count target.
- **A supported version is not one configuration field:** Requests' classifier list reaches Python 3.15 while its inspected tox environment list ends at 3.14; go-cmp and Cobra likewise separate module directives from tested toolchain choices. These are scope differences requiring more evidence, not demonstrated support failures.
- **A helper name does not prove isolation:** Click's source explicitly deprecates its working-directory helper and explains process-global state. Tests include replacement patterns and distinguish parallel processes from concurrent invoke calls in one process. pytest separately exposes in-process and subprocess test modes and avoids accidental fixture/doctest collection.
- **A framework's repository is not an application scaffold:** Flask's source maintenance structure and dependency variants serve its framework consumers, while its own README leaves application layout open.
- **Tests belong to different contracts:** ripgrep has argument-order unit cases beside flag definitions plus explicit binary integration routing. fd checks observed file lists and names platform-gated filesystem cases. Co-location and separate fixture suites solve different navigation/test problems.
- **Generation has inputs and effects:** Testify's authored assertions/templates feed generated fatal wrappers and a CI diff check. bat's asset script can clear the local bat cache, update submodules interactively, apply/reverse patches and regenerate caches. Reading a generation script does not authorize running it.
- **Do not stop at one workflow:** uv's generated-files job uses broad DryRun plus selected Check calls, while its docs validation and publication regenerate references before strict builds. Checked-in equality and built documentation freshness are different claims.
- **Human-readable diagnostics can remain unstable:** go-cmp separately explains semantic equality, human-readable diff and the custom Reporter route. Golden tests do not automatically promise a stable machine protocol.
- **A test target may fetch dependencies:** Cobra's Makefile test/richtest depends on install_deps and go get; its CI supplies environment flags. A documented test-command name is not a complete account of its side effects or coverage.

## Access gaps and excluded inferences

- A guessed uv `.github/workflows/docs.yml` path returned 404. The actual pinned workflow directory led to `check-docs.yml` and `publish-docs.yml`, both inspected. No absence/automation-defect claim follows from the failed guess.
- ripgrep's short CONTRIBUTING file points to `AI_POLICY.md`; the full policy was not inspected for its card. No terms are inferred beyond that routing fact.
- Click and Flask route contribution guidance to the Pallets website. That external guide was not opened in this lane, so repository-specific contribution/legal claims are not made from it.
- Requests' `setup.py` was retrieved but not relied on for a substantive card claim; it is not included in the 70-file count. pyproject remains the inspected packaging source.
- No workflow run, current status check, branch protection, external credential/permission, release artifact or installed package was inspected. Source configuration establishes intended mechanics. No runtime, coverage adequacy, security certification, benchmark advantage or publication success is claimed.
- The sample favors maintained open-source libraries/tooling with inspectable source. Private-service repositories, data/ML reproducibility and constrained/offline teams need additional cases; those gaps do not justify extrapolating this layout to them.

## Promotion and maintenance

All twelve cards are curated for their narrowly stated source mechanisms, with `source-inspected` evidence only. Their Change path sections are read-only traces, not executed flows. Recheck current mutable instructions before applying them to a real project; preserve the pinned case as historical evidence when it changes. Do not import local contribution policies, toolchains or generation side effects merely because an analogous repository uses them. The coordinating agent will add cross-family relations and generated views after reconciliation.
