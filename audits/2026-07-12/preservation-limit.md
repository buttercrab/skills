# Preservation Evidence Limitation

The planning pass recorded the exact initial path inventory and Git state, but did not hash the three pre-existing untracked skill directories before remediation began. Their original content hashes therefore cannot be reconstructed honestly.

What is proven:

- the initial tool receipt listed every original path under `brief-linked-evidence`, `map-technical-landscapes`, and `mine-history-tool-landscapes`;
- every one of those original paths remains present in the end inventory;
- unrelated `.planning/` content was not read or modified;
- tracked-file start hashes are derived from `HEAD` and end hashes are recorded;
- `align-work`, discovered later, has a complete baseline hash manifest in `align-work-baseline.tsv`; the user then excluded it. All five original audit-edited resources were restored before a concurrent external/user writer continued changing the directory. Six resources differed at the passing independent review; ten differed at a later path-and-hash-only observation. Because that writer remained active, `resource-inventory.tsv` marks all excluded end hashes as intentionally unstable rather than chasing them. No content review or audit verdict is assigned.

What is not proven:

- byte-for-byte preservation of the original contents of the three pre-existing untracked skill directories before their authorized remediation.

This is a historical evidence gap, not a green check. It remains disclosed in the completion report rather than being silently replaced with post-edit hashes.
