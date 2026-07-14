# Skills

This repository contains authored Codex skills and their implementation code.

## Skills

- `skills/agent-mail` - Rust/PostgreSQL Agent Mail service and deployment docs.
- `skills/align-work` - Alignment-first planning, approval, execution, and resumable evidence workflow for nontrivial coding tasks.
- `skills/brief-linked-evidence` - Cross-provider evidence reconciliation and validated provenance briefs.
- `skills/front-agent-orchestration` - Human-facing gateway and main-agent orchestration protocol over Agent Mail.
- `skills/execute-goal-loop` - Goal-driven execution loop with hard verification and review gates.
- `skills/map-technical-landscapes` - Bounded technical ecosystem discovery, canonicalization, and comparison.
- `skills/mine-history-tool-landscapes` - Privacy-preserving history lineage and recurring-capability analysis.

## Repository Layout

- `skills/` - skill source directories.
- `.env/` - local deployment environment, credentials, SSH keys, and certificates. This directory is intentionally gitignored.
- `install.sh` - links repo skills into `~/.agents/skills` and `~/.codex/skills`.

## Install

```bash
./install.sh
```

Go is required. The installer builds Front Agent before changing either skill directory, then links every `skills/*/SKILL.md` directory into `~/.agents/skills` and `~/.codex/skills`.

Agent Mail also needs the remote MCP server installed by URL:

```bash
codex mcp add agent-mail --url https://agent-mail.cc/mcp --bearer-token-env-var AGENT_MAIL_TOKEN
```

Start Codex with `AGENT_MAIL_TOKEN` in the environment so the MCP client can authenticate.

## Validate

```bash
for d in skills/*; do
  [[ -f "$d/SKILL.md" ]] || continue
  python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$d"
done
make -C skills/agent-mail test
make -C skills/agent-mail real-test
(cd skills/front-agent-orchestration && go test ./... -count=1 -timeout=30s)
(cd skills/front-agent-orchestration && FRONT_AGENT_MAIL_BACKEND=memory scripts/smoke_front_agent_protocol.sh)
python3 -m unittest discover -s skills/brief-linked-evidence/tests -p 'test_*.py'
python3 -m unittest discover -s skills/align-work/tests -p 'test_*.py'
python3 -m unittest discover -s skills/map-technical-landscapes/tests -p 'test_*.py'
python3 -m unittest discover -s skills/mine-history-tool-landscapes/tests -p 'test_*.py'
```

Agent Mail deployment secrets and operational state live under `.env/agent-mail/` in this repository and are not tracked.

`make -C skills/agent-mail public-mcp-smoke` is a live post-deployment check, not a local validation command. It creates persistent test records in the deployed service and must only run with explicit production authorization and the script's live-confirmation gate.
