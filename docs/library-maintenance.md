# Maintain a resource library

Use this path to add a reference, correct an annotation or refresh a changed source. Work from the repository root. Browsing and catalog maintenance require Python 3's standard library; no global skill installation is needed.

## 1. Find the authoritative files

| Library | Canonical cards | Schema and labels | Helper tests |
| --- | --- | --- | --- |
| Design | [entries](../skills/design-with-intent/library/entries/) | [FORMAT](../skills/design-with-intent/library/FORMAT.md), [VOCABULARY](../skills/design-with-intent/library/VOCABULARY.md) | `test_design_library.py` |
| Repository quality | [entries](../skills/repository-quality/library/entries/) | [FORMAT](../skills/repository-quality/library/FORMAT.md), [VOCABULARY](../skills/repository-quality/library/VOCABULARY.md) | `test_repository_library.py` |
| System architecture | [entries](../skills/system-architecture/library/entries/) | [FORMAT](../skills/system-architecture/library/FORMAT.md), [VOCABULARY](../skills/system-architecture/library/VOCABULARY.md) | `test_architecture_library.py` |
| Writing | [entries](../skills/writing-with-intent/library/entries/) | [FORMAT](../skills/writing-with-intent/library/FORMAT.md), [VOCABULARY](../skills/writing-with-intent/library/VOCABULARY.md) | `test_writing_library.py` |

Edit `library/entries/<id>.md`, whose frontmatter is strict JSON between `---` lines. `library/index.md` and `library/index.json` are generated views; changing either directly will be lost on the next build. `SKILL.md` owns operating guidance; `references/` holds conditional detail. Change these only when the finding affects how an agent should work, rather than for every new resource.

The four schemas intentionally differ. Read the selected FORMAT rather than copying another library's facets or required trace sections. Use an existing card from the same library and resource kind as a structural example, not as evidence for the new source.

## 2. Add or refresh the evidence

Search for an existing source before creating an ID. Preserve stable IDs and `related` references when updating; do not delete a card while other cards or reading paths still point to it. A source mirror or changed title is not automatically a new independent resource.

Read the actual primary material needed for the claim. Record the source version or inspection date, precise locator, access limits, what transfers and what does not. Source/configuration inspection, visual inspection, tested interaction and empirical outcomes are distinct evidence. Keep original annotations and source links; do not bundle third-party article bodies or assets.

Choose `candidate` for a lead that has not earned its proposed claim. Use `needs-review` when an existing annotation needs reassessment, and `retired` when retaining an entry for history rather than current use. Availability and freshness describe different facts from curation status. A blocked URL or a changed date alone neither validates nor invalidates the underlying claim. Follow the chosen schema's evidence requirements before promoting an entry to `curated`; a successful validator cannot make that editorial decision.

For substantial research or a changed claim, keep a concise dated receipt under `docs/research/` with inspected scope, unresolved gaps and the resulting card/guidance change. Preserve existing frozen evaluation records; a later correction does not upgrade an original result. Small spelling or link corrections do not need a new research dossier.

## 3. Regenerate and inspect the result

This concrete example selects the writing library. Change `skill_library` to the directory name from the table for another library.

```bash
skill_library=writing-with-intent
python3 "skills/$skill_library/scripts/catalog.py" facets
python3 "skills/$skill_library/scripts/catalog.py" build
python3 "skills/$skill_library/scripts/catalog.py" validate
```

`build` validates the cards and writes both indexes. `validate` checks cards, local references and generated-view drift without rebuilding. If it reports stale views after a card edit, inspect and rebuild them; do not fix the generated text by hand or weaken validation. Other errors need correction at their owning card or reference first.

Check that the changed resource is actually findable. For the writing example:

```bash
python3 skills/writing-with-intent/scripts/catalog.py show craft-wisconsin-reverse-outline
python3 skills/writing-with-intent/scripts/catalog.py find "reverse outline" --status curated
```

Use the ID and terms relevant to your change. Search is literal matching, not semantic ranking; exact facet filters use the labels exposed by `facets`. `show` reads a card directly and can inspect a candidate; a curated-only query deliberately omits other statuses.

Review `git status --short` and the affected card, generated views and reading paths. New untracked cards do not appear in ordinary `git diff`; open them too. Check meaningful output changes and related links, not just successful command exits. Building and validating establish structural consistency, not current source truth, reference fit or measured user benefit.

## 4. Run checks proportional to the change

A card-only update needs catalog validation, inspection of the changed source/annotation and the resulting browse/search path. If helper code changes, run the selected library's test file from the table. For writing:

```bash
python3 -B -m unittest discover -s tests -p test_writing_library.py
```

These helper tests use temporary packages and Python's standard library. They check schema/path behavior, queries and generation; they do not judge resource quality. For skill metadata or linked-resource changes, use the package checks in an isolated dependency environment:

```bash
uv run --with pyyaml python -B -m unittest discover -s tests -p test_skill_packages.py
```

The broader [repository validation instructions](../README.md#validate) cover other components. A library annotation edit does not require running unrelated legacy services or production smoke tests. Behavior-changing instructions warrant an appropriate actual-task check; preserve its scope and observed limitations rather than testing for the presence of preferred wording.

## 5. Understand what consumers receive

Each skill is a portable directory containing its instructions, references, cards, helper and generated indexes. Keep required resources within that directory; research and evaluation archives stay outside the installed package. Optional private/local references must remain explicitly labeled, with no required personal filesystem path in the portable workflow.

Read-only discovery is:

```bash
./install.sh --list
```

The [installer](../scripts/install_skills.py) creates directory symlinks into this checkout. An existing link to the same checkout exposes edited files on a fresh filesystem read; it does not establish that an already-running agent has reloaded its instructions. A copied package or a link to another checkout does not receive these edits. Installation and migration change user-level directories; they are separate from maintaining a card. See [installation behavior](../README.md#install-and-migrate) before deliberately changing those links.
