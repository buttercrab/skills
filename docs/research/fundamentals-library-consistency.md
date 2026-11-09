# Fundamentals library integration review

Reviewed 2026-11-08 against the working-tree files. This is a static integration review of `design-with-intent`, `repository-quality`, `system-architecture` and `writing-with-intent`, not a behavioral evaluation or verification of upstream sources.

**Result: no material defects supported in the inspected integration paths.** No severity-ranked correction is warranted. The libraries consistently connect task intent to real local resource cards, consequential human direction, scoped evidence and the original deliverable. Their differences serve their domains rather than impose incompatible workflows.

## Scope and method

Read each `SKILL.md`, the root README's four library sections, each `library/FORMAT.md`, the three existing `library/PATHS.md` files, discovery/library-usage references, and relevant question/evidence/maintenance references. Inspected one concrete resource route per library: Discord onboarding, p-limit, SQLite commit boundaries and the Momentum revision. Read command-parser declarations only to compare documented entry points with the static interface.

A shell file-existence pass over relative Markdown `.md` links in the root README and all four skill directories produced no missing targets. This checks local Markdown destinations, not external URLs, anchors, generated-view consistency or runtime behavior. No catalog scripts, tests, upstream programs, installs, network requests, native applications or production access were used. No skills or example projects were edited.

## Evidence by integration question

| Question | Concrete evidence | Assessment |
| --- | --- | --- |
| Does discovery route to resources rather than remain abstract advice? | `README.md:23–32`, `37–44`, `49–56`, `61–68` link the actual indexes and give scoped optional commands. Design's `references/discovery-and-selection.md:7–17` and `62` require cards, primary portions and actual IDs. The other `references/library-usage.md` files route to their indexes/PATHS and exact IDs: repository `3–19`, architecture `3–19`, writing `3–19`. | Consistent. Direct reading is usable without a helper or service. Local `.md` destinations exist; external source availability is not established here. |
| Are questions consequential while complete briefs, delegation and narrow tasks can proceed? | Design `SKILL.md:22–32`, repository `SKILL.md:14–18`, architecture `SKILL.md:14–18`, writing `SKILL.md:14–18`. Narrow-work limits appear in design `SKILL.md:38`, repository `references/library-usage.md:3`, architecture `references/library-usage.md:3`, writing `SKILL.md:26` and `references/library-usage.md:21`. | Consistent. None requires an additional interview or style vote after enough direction exists. Each distinguishes discoverable technical facts from human-owned intent. |
| Do answers alter the work rather than become an interview record? | Design `SKILL.md:30–32`, `54–60`; repository `SKILL.md:18`; architecture `SKILL.md:18` and `references/context-and-tradeoffs.md:29`; writing `SKILL.md:18` and `references/author-and-reader.md:25–33`. | Consistent. Delayed answers replace dependent provisional choices; merely opening a reference is not endorsement. |
| Is source inspection distinct from validation? | Design `SKILL.md:42`, `76–78`; repository `SKILL.md:26–28`, `50–52`; architecture `SKILL.md:28`, `48`, `54`; writing `SKILL.md:28`, `42`, `56–58`. Each FORMAT also distinguishes modes: design `22–36`, repository `14`, `22–24`, architecture `13`, `18–24`, writing `13`, `18–22`. | Consistent. Card reading, source/configuration inspection, interaction/rendering, runtime guarantees, releases and measured outcomes are not interchangeable. |
| Is the parent skill/library preserved when a product or article is only an example? | Design `SKILL.md:10–12` and `references/evidence-and-maintenance.md:34`; repository `SKILL.md:10` and `references/evidence-and-maintenance.md:17–19`; architecture `SKILL.md:10` and `references/verification-and-evolution.md:28–32`; writing `SKILL.md:10` and `references/ai-writing-and-evaluation.md:36–38`. | Consistent. Each explicitly returns bounded trial findings to the parent deliverable and avoids silently converting inspection into product maintenance or publication. |

Paths in this table are repository-relative; unqualified `SKILL.md` and `references/...` paths belong to the library named in that cell.

## Concrete resource routes inspected

These are checks of the local annotations and locators, not repetition of curator observations or fresh verification of external sources.

| Route | Evidence present in the actual card | Preserved limit |
| --- | --- | --- |
| README design command → `flow-discord-community-onboarding` | `skills/design-with-intent/library/entries/flow-discord-community-onboarding.md:27–55` identifies the source, precise sections and documented sequence; `72–78` supplies inspection/adaptation guidance. | `80–82` explicitly says no live server/role/permission change or screenshot viewing occurred. Documented flow is not presented as interaction-tested. |
| Repository PATHS small-tree row → `repo-small-p-limit` | `skills/repository-quality/library/PATHS.md:7`; card `sources` at `30–66` pins actual file locators; `90–100` traces the public maintenance path. | `68–74`, `92–96` distinguish read code/CI declarations from executed tests and observed package contents, including a conditional test skip. |
| Architecture PATHS state-authority row → `system-sqlite-commit-boundaries` | `skills/system-architecture/library/PATHS.md:8`; card `30–56` records pinned comments plus live documentation; `72–86` traces commit distinctions into diagram implications. | `88–90` limits the guarantee to documented assumptions and distinguishes source-contract interpretation from crash testing or actual device behavior. |
| Writing PATHS revision row → `example-momentum-revision-reader-questions` | `skills/writing-with-intent/library/PATHS.md:10`; card `27–47` records actual before/after commit identities and selected published passages; `61–71` separates observed edits from proposed transfer. | `77–79` disclaims proof of improved comprehension, inferred editorial motives, formula/widget testing or whole-article coverage. |

## Differences that do not warrant correction

Design uses `references/discovery-and-selection.md` instead of a separate PATHS document; it already exposes progressive discovery, search, roles, contrasts and application (`7–13`, `36–64`). No caller points to a nonexistent design PATHS file. Adding one for symmetry would not repair a broken route.

The FORMAT metadata deliberately differs by domain: design uses tasks/contexts/platforms/character (`16`), repository uses tasks/contexts/languages/scale (`12`), architecture uses tasks/contexts/qualities/scale (`11`), and writing uses tasks/genres/languages/contexts (`11`). Their usage references explain actual exact-match facets and query limits. A universal field merge would discard useful distinctions without addressing a demonstrated defect.

The domain-specific trace sections also have distinct jobs: repository Change path (`FORMAT.md:18–20`), architecture Architecture trace and Diagram implications (`FORMAT.md:18–20`), writing Craft trace and Revision implications (`FORMAT.md:18`). Design's visual/flow receipt rules (`FORMAT.md:28–36`) address its own evidence risks. None conflicts with the shared requirement to inspect relevant primary material and preserve claim boundaries.

## Limits and warranted next step

No correction is recommended from this static integration review. It does not establish that agents reliably follow these instructions, that questions improve outcomes, that matching has broad recall, that search helpers execute correctly, or that upstream resources remain available. Those claims need their own appropriately scoped evidence. This review supplies no basis for a router, merged schema, mandatory questionnaire or additional shared framework.
