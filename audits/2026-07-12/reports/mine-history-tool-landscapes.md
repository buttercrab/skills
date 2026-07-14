# Mine History Tool Landscapes Audit

Initial verdict: fail. Final verdict: pass.

## Findings

- P0 local access: `validate_history_evidence.py:78-86` followed attacker-controlled manifest filenames, including absolute paths and devices.
- P0 publication privacy: redaction missed credentials, PEM data, short native IDs, arbitrary URI schemes, root/UNC paths, dictionary keys, and private source identifiers.
- P1 source safety: metadata could smuggle transcripts/secrets; allowlist checks had a symlink-swap window; HMAC keys lacked ownership/mode checks.
- P1 accounting: post-cutoff descendants seeded campaign namespaces; chronology was unchecked; run IDs were linkable; manifest/exclusion integrity was forgeable.
- P1 grounding: observation locators, artifacts, git evidence, and publication modes were not tied to the private index.
- P2 large-input, recurrence-classification, lineage-edge, retention, family-accounting, and cross-corpus-linkability contracts were incomplete.

## Fixes

Migrated to strict v2 source/evidence/publication contracts; added descriptor-based bounded reads, no-follow and mutation checks, secure HMAC keys, per-index salts, correct cutoff/campaign closure, exact file/hash/permission reconciliation, typed observation/artifact/lineage grounding, reducer-reviewed root recurrence, closed mode-specific publications, and comprehensive key/value redaction.

## Evidence

`python3 -m unittest discover -s skills/mine-history-tool-landscapes/tests -p 'test_*.py'`: 23 synthetic tests passed, including duplicate-key fail-closed checks across every JSON boundary. Both CLI help paths and canonical skill validation pass. Real histories and remote sources were intentionally not accessed.
