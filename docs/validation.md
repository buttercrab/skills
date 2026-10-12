# Validation evidence

Validation performed October 13, 2026 (Asia/Seoul). This records inspected outcomes, not a claim that every future agent invocation will behave identically.

## Behavioral trials

Fresh agents loaded the actual rewritten skills with isolated toy workspaces and raw user requests. Expected outcomes were not supplied to the agents. Trials changed no canonical repository files and accessed no production systems or private accounts.

| Trial | Observed outcome |
| --- | --- |
| Supplied-source research | Chose an option meeting local/durable requirements; reconciled v1/v2 documentation; marked a missing source; rejected incomparable benchmark numbers; distinguished documented fit from tested behavior. No clarification or edits. |
| Refactor + propagation + handoff | Centralized pricing ownership without changing public behavior; propagated priority across producer/storage/loader/presentation; rejected invalid and boolean priorities; defaulted old records; preserved unrelated notes. Baseline 2 tests and final 7 tests passed. Restartable handoff produced. |
| Completion audit | Ran current local checks without editing the target; mapped requirements to evidence; distinguished tested behavior from unverified historical equivalence and reported provenance limits. 7 tests passed. |
| Responsive coordinator | Explicit activation dispatched a native worker. A scripted status/range-change turn updated 1–120 to 1–60 before edits; coordinator answered and routed steering without performing task execution. Worker reported 3 passing tests. A subsequent scripted deactivation reconciled the completed worker, preserved changes, and resumed normal execution. |

Coordinator evidence is a real nested-worker trial with scripted parent messages, not a human UI latency measurement. Acknowledgments were observed at 03:04:43 and 03:05:51 KST. No request-to-response latency was calculated because a matching send-time record was not captured. The coordinator inspected only its skill and used coordination/clock tools; task execution remained in its worker. No background-service scheduling or hard response-time guarantee is claimed.

These are bounded behavioral trials, not a matched-model statistical comparison against the former skills or native behavior. Smaller skills and passing examples alone do not establish universal superiority. Future regressions should be tested against concrete task outcomes.

## Automated checks

| Check | Result |
| --- | --- |
| Six active skills: skill-creator quick validation | All valid |
| Root package, installer, preservation and isolation tests | 51 total: 50 passed, 1 skipped |
| Legacy Align behavior tests | 74 passed |
| History-processing tests | 23 passed |
| Optional evidence-brief validator tests | 18 passed |
| Optional landscape validator tests (JSON Schema dependency supplied) | 33 passed |
| Legacy Front Go runtime (`GOPROXY=off go test ./...`) | Passed; 58 test functions |
| Agent Mail Rust (`cargo test --locked`) | 5 passed |
| Independent read-only final review | No supported defects in inspected skills, installer, preserved source semantics, or local links |
| `git diff --check` | Passed |

The root skip is the post-start PostgreSQL failure-isolation case: local PostgreSQL tools are unavailable. Pre-start failure isolation, real sandbox write denial, network denial, and loopback-only enforcement passed. No production smoke or real database integration suite was run. Cargo's initial offline attempt lacked cached dependencies; the subsequent locked local test downloaded dependencies and passed. Preserved runtime implementations were compared with the prior tracked versions; no message/service/packet contract change was made.

## Installed state

Full local migration succeeded in both `/Users/jaeyong/.agents/skills` and `/Users/jaeyong/.codex/skills`: all six active links resolved to this checkout, and all seven retired names were absent in each target (14 links retired). Explicit-only coordinator metadata was validated. Foreign installed skills were outside the migration scope.

Retired-link backups were retained in each target under `.skills-install-backup-aab901e0-27ce-4ac6-baa4-6ec6657fe2d9`. Restoring these links alone does not restore retired skill files; the pre-rewrite repository revision is also needed. No commit, publication, deployment, credential operation, or operational-state migration occurred.
