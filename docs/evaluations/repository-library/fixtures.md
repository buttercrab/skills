# Repository-library assessment fixtures

These fictional offline snapshots are task data, never active skills or working example repositories. Each case includes a user-facing `prompt.md`, a `repository/` snapshot, private `evaluator-notes.md`, and `SHA256SUMS`. No package installations, network access, repository commands, or fixture script execution are needed. A missing file in a snapshot is genuinely absent; omitted external history, artifacts, registry state, and CI runs remain unknown.

## Evaluation handling

Expose the prompt and snapshot to the assessed workflow. Keep evaluator notes, answer scripts, and checksums out of its context. Evaluator notes describe acceptable reasoning and evidence limits; they are not gold folder trees or fixed wording. Where notes supply human answers, provide them only in response to a material question and use the documented fallback if no answer is available. Most cases can proceed without clarification.

Judge concrete paths, source/configuration versus observed execution versus publication evidence, proportional corrective actions, contextual reference fit, and preservation of the parent skill/library scope. Additional documents, fashionable tools, blanket coverage targets, and arbitrary layouts are not success criteria. Assessment requests do not authorize implementation. Only case 05 explicitly requests bounded read-only subagent work if available.

## Cases and frozen hashes

`SHA256SUMS` hashes every prompt, snapshot file, and evaluator note using raw UTF-8 file bytes. Each digest below hashes the corresponding `SHA256SUMS` file, whose lines are sorted by relative path. The checksum file itself is excluded from its own entries. This file is excluded from case hashes.

| Case ID | Hashed files | SHA-256 of SHA256SUMS |
| --- | ---: | --- |
| `01-tiny-script` | 6 | `f33a0d7f1304998287649b459485d792a0973e64ee7b714c4ab0079c0d0beb16` |
| `02-python-artifact` | 10 | `8db3cf49d704362242d77857d83ea350db86c16e64d4701857183522c1d8b7fb` |
| `03-contract-monorepo` | 12 | `9a0b3939b403f80eef1aae25b9d5753a4ad2acdac15e687219d78dbf16a213d1` |
| `04-community-docs` | 11 | `cae9e91c43e7bdf619d0ff61a2bae51481c58dc77ee5cb1dd15b2f5ff74b62e6` |
| `05-constrained-assessment` | 10 | `f8728a3ac0f2eddf295c3ab6c24c104b507fe8e71cd9f4cb044b017abdce1737` |
