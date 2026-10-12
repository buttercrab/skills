# Six-skill migration

The rewrite retains capabilities that add specific task expertise and removes redundant agent-governance instructions. Removal decisions reflect redundancy or specialized scope, not measured invocation frequency.

| Former package | Disposition |
| --- | --- |
| `align-work` | Standalone skill removed; legacy helpers/templates/schemas and behavior tests retained under `legacy/align-work/`. |
| `execute-goal-loop` | Removed; useful completion discipline incorporated where relevant. |
| `audit-technical-work` | Rewritten in place: current evidence, supported findings, proportional completion accounting. |
| `refactor-by-invariant` | Rewritten in place: preserved behavior and demonstrably simpler ownership. |
| `propagate-contract-changes` | Rewritten in place: real contract boundaries and applicable compatibility checks. |
| `write-task-handoff` | Rewritten in place: restartable current state and authorization provenance. |
| `brief-linked-evidence` | Merged into `research-with-evidence`; optional former-format validator retained under `tools/evidence-brief/`. |
| `map-technical-landscapes` | Merged into `research-with-evidence`; optional former-format validator retained under `tools/technical-landscape/`. |
| `mine-history-tool-landscapes` | Retired from installation; source processing and privacy checks retained under `tools/agent-history/`. |
| `agent-mail` | Retired from installation; service preserved under `integrations/agent-mail/`. |
| `front-agent-orchestration` | Replaced by explicit-only `responsive-coordinator`; old runtime preserved under `integrations/front-agent/`. |

Removed generated routing catalogs, generators, gate/trial governance receipts, and instructional phrase tests. Retained actual preservation, isolation, installer recovery, and runtime tests. Preserved tools have usage documents rather than discoverable SKILL.md files.

## Existing state and compatibility

No packet schema, message protocol, deployed service, credential, or operational state was migrated. Legacy instructions describe compatibility operations, not a prerequisite for new work. Existing packets can still use their original helper semantics. The old Front runtime remains a gateway/main protocol and is not the responsive coordinator.

For local installations, a full install migrates only verified links to former `skills/<name>` paths in this checkout. It does not remove another checkout's links, foreign packages, or real directories. Selective installation requires `--migrate` to perform retirement. The installer backs up retired/replaced links in the target filesystem, recovers interrupted v1 and v2 journals, and preserves conflicting concurrent changes rather than overwriting them during rollback.

## Research influences

These are design inspirations, not copied instruction text or evidence of measured effectiveness:

- [Matt Pocock's review](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md): independent review questions.
- [Dennis Rongo's authoring](https://github.com/dennisrongo/claude-skills/blob/d740b6145a5e92aed8f100578b8e361f4524855d/skills/write-a-skill/SKILL.md): compare skill-assisted behavior with baseline decisions when useful.
- [mimukit's handoff](https://github.com/mimukit/skills/blob/9064eb09a4b8747b07c5f0c97d844d05b67e2859/skills/handoffkit/SKILL.md): carry decisions and reference existing artifacts.
- [Superpowers' subagent workflow](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/subagent-driven-development/SKILL.md): bounded briefs and clear ownership.

The collection does not require those repositories or their tools.
