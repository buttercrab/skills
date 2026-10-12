# Personal agent skills

Six rebuilt task-focused skills, plus three reporting/dashboard skills preserved from a concurrent upstream commit. Each works independently; there is no portfolio router or required planning framework.

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

## Responsive coordination

Invoke `$responsive-coordinator` or ask to turn responsive coordination on. The mode stays active in that chat until you turn it off. Creating, reviewing, or discussing the skill does not activate it.

The main agent handles discussion, scope, assignments, steering, and synthesis. Workers perform exploration, detailed planning, changes, research, testing, and review. Native subagents are preferred; no Agent Mail service, Go runtime, or second user-owned chat is required. On deactivation, the coordinator reconciles workers before returning to normal execution. Host blocking calls can still delay responses; the skill cannot guarantee a response time.

## Install and migrate

```bash
./install.sh --list
./install.sh
./install.sh --only research-with-evidence,responsive-coordinator
./install.sh --exclude responsive-coordinator
```

Python 3 is the only installer prerequisite. Full installation links the nine available skills into `~/.agents/skills` and `~/.codex/skills` and retires known links owned by this repository for the seven removed skill names. Selective `--only` or `--exclude` installations do not retire old links unless `--migrate` is supplied:

```bash
./install.sh --only research-with-evidence --migrate
```

Retirement recognizes absolute and relative links, including dangling links, only when their lexical target is this checkout's exact former skill path. Foreign retired links and real directories are preserved and reported. Selected active non-link targets are rejected. Replaced active links and retired links remain in same-filesystem backup directories. Both install targets share one lock, durable journal, rollback, and crash recovery; legacy install-only journals remain recoverable. Inspect the printed backup paths before any manual removal.

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
