# Front Agent Orchestration Audit

Initial verdict: fail. Final verdict: pass.

## Findings

- P0 metadata injection: `agentmail.go:450-522` rendered and reparsed raw multiline subjects, allowing an unpaired sender to overwrite trusted `from`, `to`, and contract fields.
- P1 identity: the shared Agent Mail bearer authenticated no participant identity.
- P1 protocol parsing: nested YAML keys satisfied required top-level method, role, summary, and confirmation fields.
- P1 state safety: runtime paths and individual identity-state reads followed symlinks; state files lacked owner/mode/regular-file checks; stale-lock cleanup raced; predictable logs could truncate other files.
- P1 delivery: messages were marked read before output; answer uniqueness and send retry were not atomic or idempotent.
- P1 false-green smoke: the documented memory smoke required a live token and exited zero when skipped.
- P2 polling and coverage: HTTP inbox polling could overrun deadlines, several focused client/state variants lacked tests, and the ignored fallback binary lacked freshness proof.

## Fixes

Implemented participant credential persistence at mode `0600`, server-derived sender use, retry-safe generation-aware idempotency, typed metadata, single-document top-level YAML schemas, descriptor-based `O_NOFOLLOW` identity-state reads with current-owner/private-mode/regular-file checks and a 64 KiB cap, FD-backed locks, bounded atomic caches, output-before-read acknowledgment, durable answer uniqueness, pairing recovery, bounded cursor pagination under one outer deadline, and a process-shared offline mailbox smoke. Canonical docs now carry explicit human approval, lifecycle, ownership, and resource rules. The generated binary fallback was removed in favor of current source execution.

## Evidence

Formatting, vet, unit, race, shuffled repetition, shell syntax, offline smoke, launcher checks, skill validation, and diff checks passed. Focused tests cover per-identity state symlinks, unsafe state modes, non-regular state files, pagination/read/mark deadlines, streaming, both note directions, nested root discovery, corrupted state and locks, multi-document YAML, and ambiguous versus intentional repeated sends.
