# Skills

This repository contains authored Codex skills and their implementation code.

## Skills

- `skills/agent-mail` - Rust/PostgreSQL Agent Mail service and deployment docs.
- `skills/align-work` - Approval workflow for coding tasks with material unresolved decisions or elevated mutation risk.
- `skills/audit-technical-work` - Bounded read-only technical audits with requirement-to-evidence accounting.
- `skills/brief-linked-evidence` - Cross-provider evidence reconciliation and validated provenance briefs.
- `skills/front-agent-orchestration` - Human-facing gateway and main-agent orchestration protocol over Agent Mail.
- `skills/execute-goal-loop` - Explicit goal-driven persistence with hard verification and review gates.
- `skills/map-technical-landscapes` - Bounded technical ecosystem discovery, canonicalization, and comparison.
- `skills/mine-history-tool-landscapes` - Privacy-preserving history lineage and recurring-capability analysis.
- `skills/propagate-contract-changes` - Canonical contract propagation across producers, boundaries, consumers, and proof surfaces.
- `skills/refactor-by-invariant` - Structural refactoring around explicit invariants and canonical ownership.
- `skills/write-task-handoff` - Restartable cross-session handoffs that preserve canonical state and authority boundaries.

## Repository Layout

- `skills/` - skill source directories.
- `.env/` - local deployment environment, credentials, SSH keys, and certificates. This directory is intentionally gitignored.
- `install.sh` - links repo skills into `~/.agents/skills` and `~/.codex/skills`.

## Install

```bash
./install.sh
```

No arguments preserves install-all behavior. Selection is deterministic and accepts only cataloged skill names:

```bash
./install.sh --list
./install.sh --only align-work,execute-goal-loop
./install.sh --exclude front-agent-orchestration
```

Python 3 is required. Go is used only for the offline `front-agent-orchestration` build preflight. When Go is unavailable in a default or mixed selection, the installer skips that skill, reports the reason, and installs the remaining skills successfully. A Front-only selection still fails because no requested skill can be installed, and a build failure with Go present remains a hard preflight failure before either target changes. The installer rejects non-symlink targets and symlinked parent directories, takes one lock for both Agent and Codex targets, writes and fsyncs a recovery journal before mutation, and keeps replaced symlinks in same-filesystem backup directories. A handled failure rolls back both targets and preserves a failure journal; a later invocation recovers an interrupted journal before starting new work.

Agent Mail also needs the remote MCP server installed by URL:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

Start Codex with `AGENT_MAIL_TOKEN` in the environment so the MCP client can authenticate.

## Canonical portfolio routing

`tests/portfolio-routing-v1.json` is the only editable source of portfolio routing truth. Package descriptions, agent metadata, generated routing contract blocks, and evaluator-only cases are validated projections. Every `SKILL.md` contains exactly one delimited generated routing block covering triggers, exclusions, ownership, precedence, legal compositions, fallbacks, and forbidden actions. Each `agents/openai.yaml` also carries a generated `portfolio-routing-v1-row-sha256` comment that binds every field of its canonical row. Update the canonical contract first, run `scripts/sync_portfolio_routing.py --write`, and then run `tests/validate_portfolio_routing.py`; editing a projection alone is contract drift. `scripts/sync_portfolio_routing.py --check` verifies every generated routing projection without changing files.

The routing contract classifies all eleven skills, closes precedence and fallback rules, and binds separate trial and evaluator catalogs. Its role grammar is exclusive: exactly one of native Codex, Align, or standalone Audit owns the task envelope, while Front remains a gateway, Goal Loop an overlay, nested Audit an evidence lens, Agent Mail or built-in collaboration a transport, package and contract skills mechanics, and handoff or research workflows content owners. A selected route appears in only one role and every supporting route must be reachable from the outer owner through a directional composition edge.

`tests/portfolio-routing-prompts-v1.json` is the only catalog copied into an isolated trial root; its closed schema permits only case identity, family, kind, and raw prompt text. The trial also receives the canonical role grammar, external route profiles such as `skill-creator`, and the candidate packages, but no case-specific expected route. Expected routes and rubrics remain evaluator-only in `tests/portfolio-routing-cases-v1.json` and `tests/portfolio-routing-rubrics-v1.json`, and are never copied into the trial root.

## Validate

```bash
python3 -m venv /tmp/skills-validation-venv
/tmp/skills-validation-venv/bin/python -m pip install PyYAML==6.0.3 jsonschema==4.26.0
PY=/tmp/skills-validation-venv/bin/python
for d in skills/*; do
  [[ -f "$d/SKILL.md" ]] || continue
  "$PY" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$d"
done
make -C skills/agent-mail test
make -C skills/agent-mail real-test
(cd skills/front-agent-orchestration && go test ./... -count=1 -timeout=30s)
(cd skills/front-agent-orchestration && FRONT_AGENT_MAIL_BACKEND=memory scripts/smoke_front_agent_protocol.sh)
"$PY" -B tests/validate_portfolio_routing.py --root .
"$PY" -B scripts/sync_portfolio_routing.py --check
"$PY" -m unittest discover -s skills/brief-linked-evidence/tests -p 'test_*.py'
"$PY" -m unittest discover -s skills/align-work/tests -p 'test_*.py'
"$PY" -m unittest discover -s skills/execute-goal-loop/tests -p 'test_*.py'
"$PY" -m unittest discover -s skills/map-technical-landscapes/tests -p 'test_*.py'
"$PY" -m unittest discover -s skills/mine-history-tool-landscapes/tests -p 'test_*.py'
"$PY" -m unittest discover -s tests -p 'test_*.py'
```

Agent Mail deployment secrets and operational state live under `.env/agent-mail/` in this repository and are not tracked.

`make -C skills/agent-mail public-mcp-smoke` is a live post-deployment check, not a local validation command. It creates persistent test records in the deployed service and must only run with explicit production authorization and the script's live-confirmation gate.
