# Writing library catalog tooling

Date: 2026-11-08 (Asia/Seoul). Adapted the portable architecture catalog into an independent writing-with-intent package. Existing skill packages were not modified. No final writing index was generated while curators wrote cards.

## Interface and integrity

`skills/writing-with-intent/scripts/catalog.py` uses Python standard library only. Commands: build, validate, list, find, facets and show. Writing kinds: example/guide/foundation/study/tool. Facets: tasks/genres/languages/contexts, with exact flags --task/--genre/--language/--context. --root precedes the subcommand; ordinary operation locates the package relative to its own script.

Strict JSON frontmatter, duplicate-key/NaN rejection, IDs/filenames, sources/dates/modes, related-resource existence, required substantive sections and portable internal links are validated. Example cards require both Craft trace and Revision implications; other kinds need only the common sections. Architecture-specific conditional sections were removed. Optional visual/flow/interaction claims retain their receipt requirements from the common format. Source inspection does not imply reader testing or causal editorial improvement.

Deterministic Markdown/JSON views include canonical card SHA-256, enabling annotation as well as metadata drift detection. Canonical and generated paths have containment and symlink guards before reads/writes. Source URLs reject embedded credentials and unsupported/control-character forms. These are declaration/path checks, not article truth, source-access, copyright or writing-quality validation.

Search is literal all-terms AND with explicit matched fields. Repeated task/genre/language/context filters require all supplied values; repeated kind/status/availability filters permit alternatives within each field. No semantic affinity, popularity, author or quality score is computed. `facets` exposes actual vocabulary; vocabulary notes do not invent final curator labels.

## Validation performed

`python3 -B -m unittest discover -s tests -p test_writing_library.py`: **24 tests passed**. Tests use synthetic temporary packages, not expected final card counts or instruction wording. They cover deterministic generation/drift, curated-versus-discovery evidence, optional receipts, relationships, strict JSON, source URL safety, identities, local links/symlinks, generated-output guards in build and check modes, example-only craft/revision obligations, genre/language CLI and repeated-filter semantics, matched source/evidence fields, generated-link bootstrapping, vocabulary discovery, malformed metadata and relocated execution without original repository/dependencies. A writing-specific Unicode test checks Korean annotation generation, literal search and exact language filtering.

CLI help passed. An initial adapted conditional-section test omitted Craft trace in its supposed valid example; that test fixture was corrected before the successful run. No active source/card failure was masked, and no source wording assertions were added.

No dependency installs, upstream article/tool execution, publication, fixture assessment reads or real-project edits were performed. Final whole-library build/validation belongs to the coordinator after curation and relation reconciliation.
