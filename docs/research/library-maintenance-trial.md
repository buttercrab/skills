# Real repository task: resource maintenance

2026-11-08. The parent goal remains the reusable skills/library. The bounded task was to improve this repository's resource-maintenance path; no example product, publication or global installation was changed.

## Finding and correction

Starting at README's browse sections led to generated indexes and canonical cards, but the route did not directly expose FORMAT or exact regeneration/validation commands. The functionality already existed in all four helpers. Independent read-only inspection confirmed discoverability friction rather than a catalog/installer correctness defect.

Added [library maintenance](../library-maintenance.md) and a README entry. The guide links each existing schema/vocabulary, names authoritative versus generated files, explains evidence/status updates, gives concrete build/validate/show/find commands, scopes optional tests and distinguishes installed directory symlinks from agent reload behavior. It does not impose a new schema, router, CI setup, approval loop or universal repository convention.

The repository-quality library provided two selected mechanisms: [contribution entrypoints](../../skills/repository-quality/library/entries/docs-github-contribution-entry.md) for the shortest useful contributor path, and [generated-source authority](../../skills/repository-quality/library/entries/quality-generated-source-authority.md) for the card-to-index boundary. The precise upstream sections were re-opened: [GitHub's contributor-guideline locations and surfaced links](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors), and the historical [Go generation account's explicit generation/author-consumer distinction](https://go.dev/blog/generate). Their mechanisms informed the local documentation; this personal Python/Markdown catalog does not need GitHub ceremony or Go tooling. This was a targeted primary lookup, not a new ecosystem survey or external workflow execution.

## Verification

A temporary copy of the actual 56-file writing package validated initially. A simulated status edit from curated to needs-review caused the expected stale-index failure. Build regenerated both views; validation passed; show and status-filtered literal search exposed the changed card correctly. Restoring the original card and rebuilding reproduced all 56 original file hashes. The temporary copy was removed and the active package remained unchanged. This exercises real current catalog data through a simulated maintenance edit; it is not a source reinspection or a judgment that the selected card actually needs review.

Read-only installer discovery listed thirteen skills. Installer source establishes directory-symlink creation, not whether an already-running agent reloads instructions. A separate read-only review of the finished guide found no material errors or unnecessary workflow burden. Structural/path checks and source reads do not establish contributor satisfaction, reference quality, current external-source availability beyond the inspected sections or broad skill effectiveness.

## Lesson returned to the master library

The existing repository-quality workflow led to the source/generator/consumer boundary and a proportional correction. The concrete gap belonged in this repository's maintainer entry path, so the correction is documentation. No operating-skill rewrite is warranted by this task, and no old evaluation result is upgraded. The reusable collection now has a direct maintenance route for subsequent research updates.
