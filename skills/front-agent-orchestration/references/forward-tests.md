# Forward Tests

Use fresh agents where possible. Do not give them hidden expected answers.

1. Main startup: ask an agent to use `$front-agent-orchestration main`. It should run `main`, give the tokenless gateway command, poll `state` until `pairing_state` is `paired`, then run one-shot `"$FRONT_AGENT" listen --identity <main-id>`.
2. Gateway startup: ask an agent to use the exact printed `$front-agent-orchestration gateway <main-id>` command. It should pair, announce readiness, and avoid blocking the human-facing session if human input is pending.
3. Gateway initial work: give the gateway a vague request. It should inspect relevant repo docs/code/tests when useful, then ask clarifying questions before sending a `work` message.
4. Gateway approval gate: after clarification, gateway should summarize a plain-language intent preview and wait for explicit human approval before sending private YAML with `human_confirmed: true`.
5. Main receives work: main `listen` should show the full `work` body and main should treat it as the task source while preserving high-level orchestration state.
6. Main asks human: give main a real ambiguity. It should send `method: question`, not ask the human directly.
7. Gateway answers: gateway should answer a main `question` with `method: answer`, only after human approval, and only with `--responds-to <question-id>`.
8. Main updates: main should send progress, blocker, failure, or completion as `method: update`, and gateway should relay useful parts to the human.
9. Repeat loop: after pairing and after every handled message, main should run or explicitly restart one-shot `"$FRONT_AGENT" listen`; gateway should drain with `listen --timeout 0` at human-turn boundaries.
10. Same-root setup: start gateway in the wrong directory and confirm pairing fails clearly; repeat with the original printed `--root` and confirm success.
11. Multiple state files: after creating more than one state, commands should require or document `--identity`.
12. Full-body listen: `"$FRONT_AGENT" listen --timeout 0` should print full valid unread protocol message bodies, not only inbox summary lines.
13. Sender spoofing: a second unpaired participant must not be able to get messages printed by paired `listen`.
14. Fenced YAML: unfenced, malformed, nested-fence, or wrong-method bodies must be rejected.
15. Missing confirmation: gateway-originated messages without `human_confirmed: true` must be rejected.
16. Direct-to-main after setup: send task instructions to the main session after pairing. It should route through gateway or remind that gateway is the active human-facing session.
17. Long work segment: main may work without listening during a bounded local segment, but it should send progress for long work and return to `listen` at the next protocol boundary.
18. Competing listener guard: start two `front-agent listen` commands for the same identity. The second should fail clearly with an already-running listener error; a stale listener lock should be cleaned automatically.
19. Raw YAML hiding: gateway should not show raw protocol YAML to the human unless the human asks for it or a protocol/debug failure requires it.
20. Removed token flag: old gateway commands containing `--token` should fail clearly and tell the user to rerun main/use the tokenless command.
21. Missing waiter: start gateway without a live main `wait-ready`; gateway should fail clearly before sending readiness mail.
22. Restarted waiter: create a valid unread gateway readiness mail, then restart `wait-ready`; main should consume the existing unread readiness and complete pairing.
23. Queued drain: queue multiple valid unread messages, then run one-shot `listen --timeout 0`; it should print all currently available valid messages within the documented 10-page scan bound before exiting.
24. Gateway human availability: after gateway pairing, before a first task is approved, gateway should return control to the human instead of blocking in a long foreground listen.
25. Main delegation: for implementation work with available subagents, main should spawn explorers/workers/verifiers and summarize their results instead of doing broad code reading itself.
26. Gateway repo exploration: before sending a nontrivial task, gateway should read relevant repo docs/code/tests and include discovered facts, likely scope, suggested tests, and assumptions in the approval preview and private request.
27. Durable answer uniqueness: consume a valid answer, then attempt a second answer to the same question; the second must fail. Race two answer sends and confirm exactly one succeeds.
28. Paired-state convergence: inject a process stop between acknowledgement delivery and local state completion, rerun the appropriate pairing command, and confirm both sides converge on the same peer and `paired_at` state.
29. Rejected read state: send a stale or malformed protocol message, listen twice, and confirm it is rejected once and then absent from unread mail.
30. Output failure: inject a listener output error and confirm the valid message remains unread and is delivered on retry with the same message ID.
31. Metadata injection: send from an unpaired participant with newline-bearing subject metadata and confirm typed sender validation rejects it; CR/LF subjects from `front-agent send` must fail before transport.
32. Top-level YAML: nest `method`, role, summary, or `human_confirmed` under another key and confirm each is rejected as missing at the top level.
33. Terminal lifecycle: send `complete`, `failed`, and `cancelled` updates and confirm gateway relays the result and stops; invalid or missing update statuses must fail.
34. Offline smoke safety: resolve `scripts/smoke_front_agent_protocol.sh` from the loaded skill directory and run that absolute path without credentials; confirm it passes using only the process-shared local backend, leaves no waiter process, and creates no live Agent Mail data.
35. HTTP pagination: mock more than one inbox page, confirm the client passes each opaque `next_cursor` unchanged, enforces the 10-page bound, and applies one outer timeout to project creation, inbox pages, and per-message reads.
36. Source freshness: confirm the launcher requires Go and runs source directly; no optional generated binary may shadow current code.
