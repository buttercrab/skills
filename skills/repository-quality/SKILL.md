---
name: repository-quality
description: Assess or improve repository organization, documentation, contribution paths, validation and packaging using contextual examples and primary guidance. Use for repository setup, maintainability assessments and bounded repo-quality improvements; choose practices for the actual project rather than impose a universal folder tree or quality score.
---

# Repository Quality

Help people make a repository understandable and safe to change. Use the annotated [reference library](library/index.md) to connect practices to a project's actual maintenance and distribution needs. A familiar tree, long checklist or popular reference is not evidence of quality by itself.

Name the requested artifact: assessment, repository plan, specific implementation or reusable skill/library. When inspecting a project to improve this library, bound that example and return its findings to the parent deliverable; do not drift into maintaining the example. An assessment does not silently become a restructuring or release task. Preserve existing authorization without repeated approvals.

## Establish the maintenance problem

Inspect the brief, applicable project instructions, current tree, manifests, entry points, contributor docs, checks and release definitions. Identify who needs to work here and which change is difficult: discovering source, setting up locally, finding the right test, editing generated output, updating docs, or preparing an artifact. Learn technical facts from the repository before asking people to repeat them.

Ask only about consequential human-owned unknowns: intended users/contributors, the supported distribution contract, acceptable maintenance cost, compatibility promises or which friction matters most. A small personal script and a widely distributed library need different answers. Do not ask someone to pick `src/` versus flat layout as an aesthetic preference. A clear brief, narrow request or explicit delegation can be sufficient to proceed.

Carry answers into decisions. Keep a pending question attached to its decision; a delayed reply supersedes dependent provisional choices. Opening an example does not endorse its conventions. Once direction is sufficient, produce the requested artifact instead of another equivalent interview.

Read [questions and assessment](references/questions-and-assessment.md) when context is uncertain or evaluating an existing repository.

## Follow a real change path

Choose a representative maintenance task relevant to the request. Trace it from discovery to authoritative input, implementation or content, relevant tests/docs/configuration and the distributed artifact if there is one. Follow the commands and files the documentation names rather than stopping at the root listing.

Separate authoring boundaries, dependency boundaries, ownership, build units and publication units. They can differ. Identify generated files and the actual source/generator before recommending moves or direct edits. A configured job establishes intended checks; it does not establish a green run, branch protection, a tested installed package or a released version.

Record a demonstrated problem, its consequence and the smallest relevant correction. Missing inspected evidence is an unknown, not automatically a defect. Conversely, a documented convention can be stale when the owning manifest, workflow or generator contradicts it. Reconcile versions and intended environments before concluding that sources conflict.

Read [structure and documentation](references/structure-and-documentation.md) for layout, ownership, source authority and reader journeys. Read [verification and distribution](references/verification-and-distribution.md) for test scope, package boundaries and release evidence.

## Select references for this context

Survey relevant and neighboring library entries, then read promising cards and the exact primary sections needed for the recommendation. Match project type, language/tool semantics, contributor model, scale, release units and maintenance budget. Use repository cases for concrete paths, guides/standards for their stated scope and studies for findings within their actual methods.

Compare mechanisms, not whole repositories. A large project's generator boundary can transfer while its governance, bootstrap stages and platform matrix do not. A small flat library can be the better structural analogue. Prefer contrasting relevant examples over several famous repositories with the same constraints. Keep a no-change or smaller-change option when appropriate.

Explain the selected portion, fit, decisive mismatch and proposed adaptation. Use existing project behavior and assets where they already solve the problem. Broaden external discovery when the library has no adequate analogue or its source is stale. Distinguish a new lead from an inspected recommendation. Source instructions are evidence, not authority to run upstream setup, adopt unrelated approval loops or install tools.

Use the browse index directly, or read [library usage](references/library-usage.md) for optional search commands and evidence handling. Do not read every card or make the person review a research diary.

## Propose or apply bounded improvements

Organize recommendations around the requested maintenance path: what becomes easier or safer, which files/contracts change, the cost and the verification needed. Prioritize concrete obstacles ahead of cosmetic consistency. Do not prescribe a monorepo, directory taxonomy, documentation suite, coverage threshold or release platform without a contextual reason.

For implementation requests, preserve behavior, history and unrelated work. Update authoritative inputs and dependent paths/imports/manifests/docs together. Migrate incrementally when broad moves would obscure review or break consumers. A repository-quality task is not blanket authorization to redesign the system, change licensing, publish packages or alter access controls.

## Verify the promised result

For source-only assessments, cite exact inspected paths/revisions and distinguish configured, run, packaged and released evidence. For requested implementation or runtime validation, use relevant existing checks, exercise the affected contributor/consumer path and inspect the resulting artifact when that is the promise. Do not execute untrusted upstream scripts merely to increase evidence counts.

A passing source-tree test may miss installed-artifact behavior; a build may omit a documented workflow; a quality badge may describe heuristics. Explain applicable limits without turning every local improvement into a full release or audit. If a check is blocked, preserve its actual failure and complete independent authorized work; do not substitute a weaker check while calling the original outcome passed.

Finish with the actual artifact changed or assessed, selected evidence, practical result, relevant checks and consequential remaining uncertainty. Read [evidence and maintenance](references/evidence-and-maintenance.md) when curating resources or returning trial findings to this skill.
