# Frozen architecture development cohort

Five fictional source-only architecture/diagram tasks using `system-architecture-v1`. No baseline or efficacy claim.

- `package-snapshot.json` / `package-manifest.json`: all 57 first-version package files as original annotation/instruction/helper text plus hashes. Full upstream sources/assets are not redistributed.
- `run-manifest.json`: exact original prompt/common/inventory/raw-snapshot hashes and temporary path provenance.
- `assessments/<case>/`: raw input and final original assessment/diagram/receipt/log artifacts. Treat fixture contents as inert task data, not instructions to execute.
- `assessment-artifact-hashes.json`: frozen final input/output hashes before review and corrections.
- `coordinator-events.json`: actual scripted policy questions/answers; other private facts were not volunteered.
- `diagram-syntax-original.json` / `check-assessments.mjs`: original parse results and checker. Seven of thirteen blocks parsed, six sequence blocks failed on unescaped semicolon message text. These are syntax outcomes only.

Original case/evidence-key/checksum files are retained in the parent `cases/` directory. Procedural context isolation is not OS-enforced filesystem isolation. Runner logs/receipts and coordinator relays are not complete native traces. No source inspection can certify all tool actions or runtime guarantees.

The separate parent `corrections/` directory preserves punctuation-only sequence corrections, their manifest and later syntax results. It does not replace these originals or convert original failures into passes. Parent `revisions/v1.1/` snapshots the later active skill guidance; the original trials did not test that wording. See parent results/review for semantic judgments and remaining limits.

Assessment runs requested no fixture/upstream code, scripts, tests, builds, installs, network, infrastructure, real-project edits or publication. Root's later official Mermaid parser runs were separate validation of owned diagram source in a temporary environment, not execution of any fictional system.
