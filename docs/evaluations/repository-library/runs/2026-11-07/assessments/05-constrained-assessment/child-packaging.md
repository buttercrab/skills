# Independent packaging and check-evidence assessment

Scope: read-only offline snapshot at `/private/tmp/repository-quality-assessment-20261107/05-constrained-assessment/repository`. No repository code, tests, build hooks, install, git, network or publication was executed. This child owns only this report; other agents' outputs were not read.

## Findings

1. **P1 verification gap: the installed CLI is outside the configured check boundary.** `.github/workflows/check.yml` installs pytest, selects Python 3.11 and runs `PYTHONPATH=src python -m pytest` on pull requests. `tests/test_parser.py` imports the public `signal_window.parse_lines` export and has two parser cases. Neither installs the distribution nor invokes `signal-window`, so this check cannot establish that the console script is created or that its stderr/exit/TSV contracts hold. `pyproject.toml` declares `signal-window = "signal_window.cli:main"`; `src/signal_window/cli.py` contains that callable. These declarations are coherent, not proof of an installed command. Smallest correction: retain fast source tests, add focused CLI regression tests, and add one isolated wheel-install smoke check to the existing workflow. Preserve setuptools, current layout and Python >=3.11.

2. **P2 release evidence is explicitly incomplete, not a demonstrated packaging failure.** `maintainer-note.md` reports laptop source tests before the latest CLI change without retained output and no installed-command smoke; `README.md` says no release artifacts are present and 0.6.2 is planned/not uploaded. `pyproject.toml` sets version 0.6.2, `requires-python = ">=3.11"`, setuptools>=69/build_meta, and discovery under `src`. Package source uses only standard library/local imports in the inspected files. No missing runtime dependency or broken package inclusion is demonstrated. Build/install/metadata correctness, retained current test outcomes, registry availability, and publication remain unverified. Do not describe the laptop report as current passing evidence or pip-install guidance as a verified available release.

## Small patch plan and later acceptance

One maintainer can own parser/CLI corrections while the other owns the focused tests plus this consumer-boundary check; review their shared stdout/error expectations before merging. Keep the build backend and folders unchanged. Avoid new release tooling, coverage goals or an expansive platform matrix for this afternoon-sized patch.

Later, in an authorized environment:

1. Run the focused parser/CLI suite on Python 3.11, retaining command, environment and results. Add regression cases for valid TSV/header, parse error exit 2 with line number/no traceback and no result output, missing delimiter, and labels containing tabs/newlines. Parser/CLI ownership determines exact cases; do not make tests merely inspect source strings.
2. Build an sdist and wheel with the existing setuptools backend; inspect wheel contents and metadata for the package, `Requires-Python: >=3.11`, version 0.6.2 and the declared console entry point. If sdist delivery is retained, rebuild a wheel from that sdist to catch omitted build inputs. A build is a later proposed operation, not performed here.
3. Install the wheel into a fresh environment and execute from outside the checkout with `PYTHONPATH` unset. Verify `from signal_window import parse_lines`, valid `signal-window input.txt` output with exactly `label`/`value`, and invalid input exit/status/stderr contract. Retain outputs. An editable install alone is insufficient for this acceptance claim.
4. Keep this patch unpublished until those outcomes are reviewed; this assessment supplies no authority to publish. Update a short release note/README statement for the actual error handling change and clarify source checks versus installed smoke. No current supported-version compatibility claim extends beyond inspected metadata/configuration.

## Selected local reference receipts

- `quality-python-distribution-checks`: borrowed **What to inspect / What to borrow and adapt** (source tree → wheel → isolated installed import/command), fitting a distributed pure Python CLI and library. No native-wheel release farm is needed; no source-distribution failure is inferred. Its PEP 660/PyPA/pytest links are card-provided historical annotations, not fresh primary-source inspection in this task.
- `quality-python-build-metadata`: borrowed **What to inspect / What to borrow and adapt** (connect script target, callable and metadata; separate build requirements from runtime/development tools). Fits the existing pyproject; does not justify a new backend or adding pytest as a runtime requirement.
- `quality-python-import-layout`: borrowed **What to inspect / Mismatches and limits** (check actual import/test invocation, not folder aesthetics). Existing `src` layout is retained; the `PYTHONPATH=src` command remains direct-source evidence, not installed-artifact evidence.
- Guide `references/verification-and-distribution.md`: used configured/run/packaged/consumer/released evidence distinctions. All selected cards were read locally; none counts as a fresh primary lookup or successful repository check.

## Files read

`COMMON.md`, `prompt.md`, guide `SKILL.md`, guide `references/verification-and-distribution.md`, the three cards above; repository `pyproject.toml`, `.github/workflows/check.yml`, `README.md`, `maintainer-note.md`, `src/signal_window/__init__.py`, `src/signal_window/parser.py`, `src/signal_window/cli.py`, `tests/test_parser.py`. No external source or other agent assessment was read.
