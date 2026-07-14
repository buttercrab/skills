# Final Verification Receipts

Run from `/Users/jaeyong/skills` on 2026-07-12.

## Package and Python gates

```text
quick_validate.py: Skill is valid! x 6
brief-linked-evidence: Ran 18 tests ... OK
map-technical-landscapes: Ran 33 tests ... OK
mine-history-tool-landscapes: Ran 23 tests ... OK
```

## Agent Mail

```text
cargo fmt --all -- --check: pass
cargo clippy --workspace --all-targets -- -D warnings: pass
cargo test --workspace: 5 passed; 0 failed
real_postgres_http_test.sh: real postgres/http test passed
real_postgres_mcp_test.sh: real postgres/mcp test passed
```

The live public MCP smoke was not run. Its guard was tested locally; actual execution requires separate authority because it creates deployed records.

## Front Agent

```text
gofmt: clean
go vet ./...: pass
go test ./... -count=1: pass
go test -race ./... -count=1: pass
go test ./... -shuffle=on -count=3: pass
scripts/smoke_front_agent_protocol.sh: front-agent smoke passed
generated front-agent-bin: absent
```

## Repository

```text
isolated HOME with Go: 7 .agents links + 7 .codex links; second install idempotent
isolated HOME without Go: refused before either destination was created
README inventory vs skills/*/SKILL.md: exact match, 7 discoverable skills
Markdown relative links in root docs and six audited skills: all resolved
git diff --check: pass
__pycache__ in the six audited skill directories: none
```

`align-work` was not validated, tested, link-checked, or remediated. Its pre-existing ignored caches were left untouched.

## Excluded `align-work` preservation

The late-discovered directory has a 15-resource pre-audit manifest. After the user excluded it, all five interrupted audit edits were reversed. A concurrent external/user writer then continued changing the directory: six resources differed at independent review time and ten at a later path-and-hash-only observation. The excluded end hashes are therefore marked unstable instead of being chased. No content review, rollback, test, or quality verdict was performed; no new non-cache resource appeared at the last observation.

The fresh consolidated receipt is in `raw/final-verification.txt`; the repository and exclusion transcript is in `raw/repository-final.txt`.

## Trigger routing

`trigger-matrix.tsv` contains 24 static prompt cases: positive, negative, ambiguous-overlap, and misuse for each of the six audited skills. Each row records expected ownership, the observed frontmatter rule, result, and false-positive/false-negative risk. All rows pass static reconciliation; no fresh-agent routing behavior is claimed.
