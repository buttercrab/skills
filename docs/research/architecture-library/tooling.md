# Architecture catalog tooling

Date: 2026-11-07. Adapted the independently portable repository-quality helper into `skills/system-architecture/scripts/catalog.py`. Existing design/repository packages were not changed. No final architecture indexes were generated during curation.

## Interface and structural guarantees

The package-local Python-standard-library helper supports `build`, `validate`, `list`, `find`, `facets` and `show`. Kinds are system/pattern/foundation/notation/tool. Exact facet flags are `--task`, `--context`, `--quality` and `--scale`; text search uses all case-insensitive literal terms and exposes match fields. It does not rank architecture quality or source strength. The generated JSON stores each canonical card's SHA-256; human/agent views remain deterministic.

Strict JSON parsing rejects duplicate keys and non-JSON constants. Validation checks metadata, IDs, dates, source URLs, required substantive sections, related IDs/internal links, receipt declarations, generated-view drift and path/symlink containment before writes or reads. System cards require Architecture trace and Diagram implications; notation cards require Diagram implications. Pattern/foundation/tool cards need only the four common sections. Ordinary source inspection does not require a flow receipt or imply execution. Optional documented-flow, visual and interaction modes preserve explicit receipt obligations, including a flow sequence for interaction-tested cards.

These are structural guarantees only: metadata and annotation text cannot prove a cited source is truthful, a diagram rendered, a relationship operationally correct or a deployment observed.

## Checks performed

`python3 -B -m unittest discover -s tests -p test_architecture_library.py`: **23 tests passed**. Tests use temporary synthetic packages, not counts/wording in current curator entries. They exercise deterministic views, source/body hash drift, evidence/status boundaries, optional receipts, relationships, strict JSON, unsafe URLs, filename identity, missing/escaping links, symlink-safe generated paths in build and check modes, conditional system/notation sections, exact quality/scale filters, source/evidence match fields, facet discovery, malformed metadata handling and a relocated copy without external executables/dependencies.

`python3 skills/system-architecture/scripts/catalog.py --help` succeeded. No parser/rendering/runtime claim follows from those checks. No tests execute upstream system code, diagram tools, builds or network requests. Final package/index validation remains the coordinator's step after card curation and reconciliation.
