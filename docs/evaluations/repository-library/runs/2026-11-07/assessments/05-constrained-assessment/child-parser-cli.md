# Independent parser/CLI review

Scope: read-only source review for the planned 0.6.2 patch. No repository code, commands, tests, builds, installation, network or publication ran. Read COMMON.md, prompt.md, repository-quality SKILL.md and the six assigned snapshot files. Preserve `parse_lines(lines)`, `main()`, Python >=3.11 and TSV columns `label`, `value`.

## Priorities

1. **Fix the documented parse-error boundary.** `repository/src/signal_window/parser.py` unpacks `line.strip().split("=", 1)` before its error wrapper. A nonblank line without `=` therefore raises a bare unpacking ValueError without the documented line number. `repository/src/signal_window/cli.py` does not catch parser ValueError at all; malformed integers, empty labels and missing separators propagate out of `main()`, conflicting with `repository/README.md`'s exit-2/no-traceback promise. Small correction: explicitly validate the separator, retain physical input line numbering, and translate parser ValueError at the CLI boundary using the existing argparse parser's error route. Keep public signatures unchanged. Continue parsing the entire file before printing the header, preserving the present avoidance of partial TSV on parse errors.

2. **Reject embedded label delimiters.** The parser accepts a label such as `a\tb` or `a\nb` when supplied in one input string; the CLI directly interpolates labels into TSV. This can create extra columns or rows. `repository/maintainer-note.md` explicitly says tabs/newlines inside labels were never intentionally supported and should be rejected with ValueError if relevant. Validate label delimiters before emitting rows; preserve the existing line-ending handling rather than treating each ordinary file newline as a forbidden label character. Add line-numbered ValueError coverage. No unresolved product decision is needed.

3. **Test the cross-boundary promises.** `repository/tests/test_parser.py` contains only valid/blank/negative-integer and invalid-integer cases; the latter checks only that the message contains `line 1`. It has no separator, empty-label, embedded-delimiter or CLI assertions. Add focused parser regressions and CLI subprocess checks through the declared `signal-window` entry point after building and installing the wheel. Assert exact successful `label\tvalue` columns, blank skipping, signed values, physical line numbers following blank lines, exit 2, useful stderr without traceback and empty stdout on parse errors. A README example and retained test evidence should accompany the patch.

## Representative maintenance path

README input/error contract → exported `parse_lines` in `src/signal_window/__init__.py` → separator/label/value handling in `src/signal_window/parser.py` → file opening, argparse and TSV rendering in `src/signal_window/cli.py` → parser regressions and new CLI tests → packaging owner's installed console-command smoke check. Retain the existing small source tree and argparse; no new CLI framework or structural refactor is needed.

## Reference transfer and limits

- Read `guide/library/entries/repo-small-click.md`, especially “Change path”, “What to borrow and adapt”, and “Mismatches and limits”. Transfer scenario-specific behavior assertions and the distinction between source tests and compatibility environments. Mismatch: this project uses argparse and supplies no custom runner API; do not introduce Click, its process-global helpers or its matrix.
- Read `guide/library/entries/quality-versioning-and-human-release-notes.md`, “What to inspect” and “What to borrow and adapt”. Transfer explicit command/output/API contracts and a short human-readable patch note. The version number alone proves no compatibility; copying release automation is outside scope.
- These were local card reads only, not fresh upstream primary inspection. No checks passed on the basis of reading them.

## Evidence uncertainty

The maintainer note reports source tests passed before the latest CLI change, with no retained output, and no installed-command check. This is historical testimony rather than a reproduced pass. No package or release artifact was inspected. `int(raw)` accepts more spellings than strictly ASCII digits; the phrase “decimal integers” alone does not establish a defect or authorize narrowing established input acceptance in this patch. File-system and UTF-8 failure policy is not specified; do not equate those open questions with the demonstrated parse-error defects.
