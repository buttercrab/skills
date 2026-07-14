# Full Skill Audit and Remediation Plan

Date: 2026-07-12

## Goal contract

Audit the six skills discovered in the planning inventory under `skills/*/SKILL.md`, plus the repository surfaces that install and describe them. Fix every validated in-scope finding, then re-run the strongest practical verification and critical review until no blocking finding remains. Keep diagnosis read-only until the initial findings are reconciled; centralize later edits to avoid cross-agent write conflicts. Treat external service checks, commits, and publication as separate authorization gates.

`align-work` appeared after the planning snapshot. On 2026-07-12 the user explicitly excluded it from this audit. It receives no audit verdict, remediation, validator run, fixture ledger, or report. Repository discovery and installer reconciliation may count it as a present skill, and the preservation ledger records its exclusion and hashes, but its contents remain outside the audit scope.

The audit is complete only when, for the six in-scope skills:

1. every discovered skill has one report and one reconciled evidence record;
2. every report covers metadata, trigger behavior, instructions, resources, deterministic validation, safety, and realistic usage;
3. every finding has severity, file and line evidence, impact, and a concrete recommendation;
4. repository-wide discovery, installation, documentation, and cross-skill overlap are checked;
5. every validated in-scope finding is fixed or explicitly documented as requiring unavailable external authority;
6. all affected deterministic checks pass after remediation; and
7. a separate critical review finds no missing skill, ungrounded conclusion, regression, or unreported skipped gate.

## Scope snapshot and preservation boundary

The planning inventory found six skills:

| Skill | Git state at planning time | Primary implementation surface |
| --- | --- | --- |
| `agent-mail` | tracked | Rust service, shell integration tests, deployment docs |
| `brief-linked-evidence` | untracked directory | skill contract, JSON schema, Python validator |
| `execute-goal-loop` | tracked | skill contract and reviewer prompts |
| `front-agent-orchestration` | tracked | Go CLI, shell smoke test, protocol references |
| `map-technical-landscapes` | untracked directory | skill contract, JSON schema, Python validator |
| `mine-history-tool-landscapes` | untracked directory | skill contract, indexer, validator, source contract |

Preserve all existing tracked and untracked work. Audit the three untracked skill directories at full depth, but do not stage, delete, rename, or rewrite them. Do not expose `.env` contents, tokens, credentials, private indexes, native history identifiers, or signed URLs. Use temporary directories outside the repository for generated fixtures and runtime state.

## Audit rubric

Apply the same core rubric to every skill. Record `pass`, `conditional`, `fail`, or `not applicable` for each category; do not average away a blocking failure.

1. **Packaging and discovery**
   - Folder name equals frontmatter `name`; naming and YAML are valid.
   - `SKILL.md` is concise, imperative, self-contained, and under the progressive-disclosure limit.
   - `agents/openai.yaml` is well-formed, quoted, current, and consistent with the skill.
   - `short_description` is 25–64 characters and `default_prompt` explicitly names `$skill-name`.
2. **Trigger contract and ownership**
   - Description says what the skill does, positive triggers, important exclusions, and delegation boundaries.
   - Positive, negative, ambiguous, and overlap prompts route predictably.
   - The skill does not claim work owned by another skill, connector, or execution layer.
3. **Instruction quality**
   - Workflow is executable in order, with explicit inputs, outputs, stop rules, and failure behavior.
   - Fragile operations have low-ambiguity guardrails; flexible work retains appropriate freedom.
   - References are linked directly from `SKILL.md` with clear conditions for reading them.
4. **Safety and authorization**
   - Read-only, mutation, remote access, secret handling, privacy, publication, and production boundaries are explicit.
   - Embedded or historical content is treated as untrusted data where relevant.
   - Claims of completion require receipts or reproducible evidence.
5. **Bundled resources**
   - Every referenced path resolves; every bundled file is necessary and discoverable.
   - Scripts have valid syntax, useful CLI errors/help, safe path handling, deterministic output, and appropriate executable bits.
   - Schemas, docs, examples, and implementations agree; stale generated binaries and auxiliary READMEs are assessed explicitly.
6. **Deterministic correctness**
   - Run the strongest local tests available.
   - Exercise validators with valid fixtures and adversarial invalid fixtures, not syntax checks alone.
   - Check that tests fail for the intended reason and do not create fake-green results.
7. **Realistic behavior**
   - Walk representative happy paths, boundary cases, failure paths, and misuse prompts.
   - Verify that outputs satisfy the skill’s stated contract and that stop conditions are measurable.
   - Fresh-agent forward tests remain optional and require separate user authorization; without it, use isolated fixtures plus a clearly separated second review pass.
8. **Maintainability and repository fit**
   - Check duplicated rules, contradictions, version drift, undocumented dependencies, and test gaps.
   - Reconcile root `README.md`, `install.sh`, installed link behavior, and the actual skill inventory.

## Execution phases

### Phase 1: Freeze the inventory and evidence format

- Capture `git status --short --branch`, tracked/untracked ownership, skill paths, file hashes, file modes, tool versions, and applicable repository instructions.
- Create the audit output under `audits/2026-07-12/`:
  - `inventory.tsv`: one row per discovered skill and resource;
  - `commands.tsv`: command, scope, exit status, and evidence-file locator;
  - `reports/<skill>.md`: one rubric-based report per skill;
  - `cross-skill.md`: overlap, discovery, install, and documentation findings;
  - `summary.md`: severity-ranked conclusions, skipped gates, and remediation order.
- Re-run discovery at the end and fail reconciliation if the start and end inventories differ without explanation. The explained end delta is the late-discovered, user-excluded `align-work` directory.

### Phase 2: Repository-wide static checks

- Run the canonical skill validator against the six in-scope skill directories. Do not include `align-work`:

  ```bash
  for name in agent-mail brief-linked-evidence execute-goal-loop front-agent-orchestration map-technical-landscapes mine-history-tool-landscapes; do
    d="skills/$name"
    python3 /Users/jaeyong/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$d"
  done
  ```

- Parse all YAML and Markdown links, verify relative targets, inspect executable bits and shebangs, and flag orphaned or unexplained resources.
- Validate `agents/openai.yaml` field constraints and alignment with each `SKILL.md`.
- Exercise `install.sh` in an isolated temporary `HOME`; verify all seven currently discoverable symlinks, backup behavior, idempotence, paths with spaces, and absence of writes to the real home. This is repository integration coverage, not an `align-work` audit.
- Compare the real inventory with root documentation and validation commands.

### Phase 3: Per-skill deterministic validation

#### `agent-mail`

- Review the HTTP/MCP contract, authentication, recipient authorization, read-state semantics, resource notifications, error mapping, data validation, and deployment documentation against the Rust implementation.
- Run:

  ```bash
  cargo fmt --manifest-path skills/agent-mail/Cargo.toml --all -- --check
  cargo clippy --manifest-path skills/agent-mail/Cargo.toml --workspace --all-targets -- -D warnings
  cargo test --manifest-path skills/agent-mail/Cargo.toml --workspace
  ```

- Run the temporary local PostgreSQL HTTP and MCP integration tests only if their dependency and cleanup preflight passes.
- Do not run `public_mcp_smoke.sh`, deploy, or mutate the live service without separate authorization and an explicit cleanup/accounting plan.

#### `front-agent-orchestration`

- Reconcile `SKILL.md`, protocol references, CLI parsing, state ownership, lock handling, pairing, sender validation, message validation, and Agent Mail behavior.
- Run:

  ```bash
  test -z "$(gofmt -l skills/front-agent-orchestration)"
  (cd skills/front-agent-orchestration && go vet ./...)
  (cd skills/front-agent-orchestration && go test ./... -count=1 -timeout=30s)
  (cd skills/front-agent-orchestration && FRONT_AGENT_MAIL_BACKEND=memory scripts/smoke_front_agent_protocol.sh)
  ```

- Map the 26 documented forward scenarios to deterministic tests, marking each covered, partially covered, uncovered, or requiring authorized fresh-agent testing.
- Check whether the bundled `front-agent-bin` is intentional, reproducible, portable, current, and appropriately tracked or ignored.

#### `execute-goal-loop`

- Test goal-tool gating, plan/implement/verify/review sequencing, blocker thresholds, read-only behavior, publish boundaries, and completion evidence through prompt scenarios.
- Verify reviewer prompts do not leak desired conclusions and that their use rules are compatible with environments where subagents are unavailable or unauthorized.

#### `brief-linked-evidence`

- Reconcile the acquisition/reconciliation workflow with `evidence-brief-schema.md` and the validator.
- Run Python syntax/help checks plus a fixture matrix covering valid briefs, blocked sources, conflicts, inference grounding, action authorization, secret-bearing locators, broken IDs, and invalid receipts.
- Require every invalid fixture to be rejected for the intended invariant.

#### `map-technical-landscapes`

- Reconcile the scope/stopping/canonicalization workflow with `landscape-schema.md` and the validator.
- Run Python syntax/help checks plus valid and invalid fixtures for candidate counts, aliases, merge/split decisions, field typing, unknowns, source strength, taxonomy symmetry, failed searches, and stop assessment.
- Verify the validator proves internal consistency without overstating factual completeness.

#### `mine-history-tool-landscapes`

- Reconcile `SKILL.md`, the source contract, the indexer, and the evidence/publication validator.
- Use synthetic histories only. Test cutoff handling, active-campaign fixed-point exclusion, aliases, cycles, chronology, duplicates, source accounting, HMAC IDs, permissions, symlink escapes, remote authorization, root-only recurrence, redaction, overlap decisions, and publication reconciliation.
- Verify no raw transcripts, native IDs, absolute paths, or secrets escape the private index boundary or publication validator.

### Phase 4: Cross-skill trigger and handoff audit

- Build a prompt matrix with at least four cases per skill: clear positive, clear negative, ambiguous overlap, and adversarial/misuse.
- Audit these high-risk boundaries explicitly:
  - `brief-linked-evidence` vs provider-specific research skills;
  - `map-technical-landscapes` vs quick comparison, tutoring, and implementation;
  - `mine-history-tool-landscapes` vs memory lookup, git archaeology, and live GPU diagnosis;
  - `execute-goal-loop` vs ordinary bounded implementation;
  - `agent-mail` vs `front-agent-orchestration` and built-in collaboration;
  - audit/planning behavior vs `skill-creator` ownership of later skill edits.
- Record false-positive risk, false-negative risk, conflicting instructions, and the recommended ownership rule for each overlap.

### Phase 5: Critical evidence review

- Perform a separate, conclusion-blind review using the raw inventory, command receipts, and reports.
- Check for missing skills, commands that did not test the claimed property, invalid fixture expectations, ungrounded severity, concealed skipped checks, and recommendations that exceed audit authority.
- Re-run every cheap failed or flaky check once from a clean temporary state. Preserve both receipts and label environmental failures separately from product failures.

### Phase 6: Remediate validated findings

- Fix findings in dependency order: shared repository/discovery issues, security and correctness, validator/indexer behavior, skill instructions and trigger boundaries, metadata, then documentation and polish.
- Keep one central writer for canonical files. Preserve existing behavior unless the finding demonstrates that the behavior violates the skill contract.
- Add or strengthen deterministic regression tests for every corrected script or service defect. Use temporary fixtures for audit-only checks and repository tests for durable behavior that could regress.
- After each bounded slice, run the narrowest relevant checks before moving to the next slice.
- Do not weaken validators, delete difficult tests, suppress warnings, or redefine acceptance criteria merely to obtain green output.

### Phase 7: Verify and deliver the completed audit

- Deliver a one-page summary first, followed by the per-skill ledger and cross-skill report.
- Rank findings:
  - `P0`: credible secret exposure, destructive behavior, unauthorized external action, or privacy breach;
  - `P1`: core workflow or safety contract can be wrong while appearing successful;
  - `P2`: material coverage, usability, maintainability, or documentation gap;
  - `P3`: localized clarity or polish issue.
- For each finding provide file/line, observed evidence, impact, recommended change, and exact verification gate.
- Re-run all affected local checks and the canonical skill validator after remediation, then perform the separate critical evidence review.
- Do not stage, commit, push, deploy, or run live external checks unless the user explicitly authorizes that separate publication or production phase.

## Required final evidence

- Six per-skill reports and one cross-skill report.
- Start/end inventory reconciliation with six planned skills and the explained, explicitly excluded `align-work` delta.
- Command receipts with exit codes and raw outputs for every deterministic check.
- Valid/invalid fixture ledger for each validator or indexer.
- Coverage mapping for all documented Front Agent forward scenarios.
- Explicit list of unrun external or fresh-agent checks and why each was skipped.
- Critical-review verdict confirming that every conclusion is supported by the recorded evidence.
- Final remediation ledger mapping every validated finding to its patch and passing regression gate.
