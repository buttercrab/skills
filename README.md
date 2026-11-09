# Personal agent skills

Thirteen task-focused skills, including catalog-backed design, repository-quality, system-architecture and writing libraries. Each works independently; there is no portfolio router or required planning framework.

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `audit-technical-work` | Check technical claims against current evidence and report defects or missing proof. | Normal discovery |
| `refactor-by-invariant` | Preserve behavior while simplifying ownership and dependencies. | Normal discovery |
| `propagate-contract-changes` | Carry a changed contract across definitions, producers, boundaries, and consumers. | Normal discovery |
| `write-task-handoff` | Prepare a restartable continuation with current state, decisions, and evidence. | Normal discovery |
| `research-with-evidence` | Synthesize supplied sources or discover and compare options. | Normal discovery |
| `responsive-coordinator` | Keep the main agent conversational while workers execute the task. | Explicit opt-in only |
| `maintain-project-dashboard` | Maintain a durable project dashboard with current evidence. | Normal discovery |
| `prioritize-important-information` | Surface decision-changing information before activity detail. | Normal discovery |
| `write-daily-report` | Summarize a day with material outcomes and one next action. | Normal discovery |
| `design-with-intent` | Discover and compare design resources, elicit human direction, and apply selected ideas through flows, craft and verification. | Normal discovery |
| `repository-quality` | Assess repository maintenance paths, select contextual examples, and make bounded structure/docs/validation improvements. | Normal discovery |
| `system-architecture` | Compare system boundaries, state and failure tradeoffs, then explain the decision with purpose-specific diagrams. | Normal discovery |
| `writing-with-intent` | Shape and revise articles around human purpose, reader needs, evidence and author voice using contextual craft references. | Normal discovery |

## Design resource library

Browse the [annotated library](skills/design-with-intent/library/index.md) for design skills, product/screen/flow examples, systems/patterns, foundations and tools. Cards explain applicability, what to inspect, what to borrow/adapt, mismatches, source versions and actual evidence scope. The generated index is a view of canonical Markdown cards; the package and optional search commands use no runtime service.

`design-with-intent` asks about consequential missing direction, preserves detailed briefs, and accepts creative delegation. It surveys relevant resources, investigates promising matches, helps the person refine the choice, and carries selected ideas into the requested work. Visual inspection, documented flows and tested interactions remain distinct claims. See the [curation and coverage record](docs/research/design-library/index.md) and [matching evaluation](docs/evaluations/design-library/results.md) for scope and limits. The [earlier execution pilot](docs/evaluations/design-pilot/results.md), including its invalidated browser comparisons, is retained separately.

From the repository root:

```bash
python3 skills/design-with-intent/scripts/catalog.py facets --status curated
python3 skills/design-with-intent/scripts/catalog.py find "onboarding" --status curated
python3 skills/design-with-intent/scripts/catalog.py show flow-discord-community-onboarding
```

## Repository-quality resource library

Browse the [repository library](skills/repository-quality/library/index.md) for annotated repository cases, guides, standards, studies and tools. Entries connect concrete change paths to source authority, contributor documentation, validation and distribution, with explicit context mismatches. The skill asks about consequential maintenance goals and release promises rather than imposing one folder tree, document list or quality score.

See [research coverage](docs/research/repository-library/index.md) and [assessment results](docs/evaluations/repository-library/results.md) for inspected sources and limits. Read/search works without a server or dependency installation:

```bash
python3 skills/repository-quality/scripts/catalog.py facets --status curated
python3 skills/repository-quality/scripts/catalog.py find "generated" --status curated
python3 skills/repository-quality/scripts/catalog.py list --language python --status curated
```

## System architecture and diagrams

The [architecture library](skills/system-architecture/library/index.md) connects system cases, patterns, foundations, notation and tools to explicit architectural questions. The skill starts from behavior, invariants and operating constraints, compares mechanisms with their limits, and keeps current, proposed and unknown system facts distinct. Diagrams expose relevant ownership, relationships and failure behavior; no mandatory microservices or diagram suite is prescribed.

See [research coverage](docs/research/architecture-library/index.md), [assessment results](docs/evaluations/architecture-library/results.md) and [original diagram examples](skills/system-architecture/references/diagram-contract.md). Optional local discovery uses Python's standard library:

```bash
python3 skills/system-architecture/scripts/catalog.py facets --status curated
python3 skills/system-architecture/scripts/catalog.py find "retry" --status curated
python3 skills/system-architecture/scripts/catalog.py list --quality durability --status curated
```

## Writing and editorial references

The [writing library](skills/writing-with-intent/library/index.md) combines annotated article/revision examples, craft guidance, source/editorial practices, AI-writing studies and optional tool limits. The skill asks consequential author/reader questions, preserves complete briefs and narrow edits, produces the requested piece, and revises substance without inventing anecdotes or treating detector scores as quality evidence.

See [research coverage](docs/research/writing-library/index.md) and [writing trials](docs/evaluations/writing-library/results.md). Browse directly or use the local stdlib helper:

```bash
python3 skills/writing-with-intent/scripts/catalog.py facets --status curated
python3 skills/writing-with-intent/scripts/catalog.py find "revision" --status curated
python3 skills/writing-with-intent/scripts/catalog.py list --language korean --status curated
```

The [cross-library integration review](docs/research/fundamentals-library-consistency.md) checks resource routes, human questions, evidence boundaries and example-task scope across these four packages. It is a static review, separate from their behavioral trials.

## Responsive coordination

Invoke `$responsive-coordinator` or ask to turn responsive coordination on. The mode stays active in that chat until you turn it off. Creating, reviewing, or discussing the skill does not activate it.

The main agent handles discussion, scope, assignments, steering, and synthesis. Workers perform exploration, detailed planning, changes, research, testing, and review. Native subagents are preferred; no Agent Mail service, Go runtime, or second user-owned chat is required. On deactivation, the coordinator reconciles workers before returning to normal execution. Host blocking calls can still delay responses; the skill cannot guarantee a response time.

## Maintain the libraries

To add or refresh a resource, follow the [library maintenance path](docs/library-maintenance.md): canonical cards, source evidence, regenerated indexes, focused checks and installed-package behavior.

## Install and migrate

```bash
./install.sh --list
./install.sh
./install.sh --only research-with-evidence,responsive-coordinator
./install.sh --exclude responsive-coordinator
```

Python 3 is the only installer prerequisite. Full installation links the thirteen available skills into `~/.agents/skills`, `~/.codex/skills` and `~/.claude/skills` and retires known links owned by this repository for the seven removed skill names. Selective `--only` or `--exclude` installations do not retire old links unless `--migrate` is supplied:

```bash
./install.sh --only research-with-evidence --migrate
```

Claude Code discovers personal skills in `~/.claude/skills` and supports symlinked skill folders ([official documentation](https://code.claude.com/docs/en/skills#choose-where-skills-load)). The installer links each complete skill directory, including its reference library. Override target paths with `AGENT_SKILLS_DIR`, `CODEX_SKILLS_DIR` or `CLAUDE_SKILLS_DIR` when needed.

Retirement recognizes absolute and relative links, including dangling links, only when their lexical target is this checkout's exact former skill path. Foreign retired links and real directories are preserved and reported. Selected active non-link targets are rejected. Replaced active links and retired links remain in same-filesystem backup directories. All three install targets share one lock, durable journal, rollback, and crash recovery; legacy install-only journals remain recoverable. Inspect the printed backup paths before any manual removal.

## Preserved software

The installable catalog is only `skills/*/SKILL.md`. Retiring instructions did not remove their useful software or change deployed services:

- `integrations/agent-mail/`: Rust/PostgreSQL service and operational documentation.
- `integrations/front-agent/`: legacy gateway/main protocol runtime; separate from the new coordinator.
- `legacy/align-work/`: existing packet validation, recovery, transfer, and preservation helpers.
- `tools/agent-history/`: private normalized-history index and validators.
- `tools/evidence-brief/` and `tools/technical-landscape/`: optional validators for the former structured formats.
- `tools/validation/`: isolated local runner, state manifests, and baseline checks.

Credentials and operational state remain in the ignored `.env/`, `.agent-mail/`, and `.planning/` locations. Preserved software is not installed as a skill. See [migration details](docs/migration.md) and [validation evidence](docs/validation.md).

## Validate

Use an isolated dependency environment rather than modifying the system Python:

```bash
uv run --with pyyaml --with jsonschema python -B -m unittest discover -s tests
uv run --with pyyaml --with jsonschema python -B -m unittest discover -s legacy/align-work/tests
uv run --with pyyaml --with jsonschema python -B -m unittest discover -s tools/agent-history/tests
uv run --with pyyaml --with jsonschema python -B -m unittest discover -s tools/evidence-brief/tests
uv run --with pyyaml --with jsonschema python -B -m unittest discover -s tools/technical-landscape/tests
(cd integrations/front-agent && GOPROXY=off go test ./... -count=1 -timeout=60s)
cargo test --locked --manifest-path integrations/agent-mail/Cargo.toml
```

Use the installed skill-creator's `quick_validate.py` on each active skill. Packaging checks validate metadata, discovery policy, and resource links. Behavioral trials inspect actual agent decisions and task outcomes; text matching is not behavioral proof.

The isolation runner needs macOS `sandbox-exec`; PostgreSQL integration checks additionally need local PostgreSQL tools. See `tools/validation/README.md`. Public MCP smoke creates persistent production records and requires separate production authorization; it is not a local validation step.
