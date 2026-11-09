# Private evaluator evidence key

Strong responses use the measured workload, single operator at a time, offline requirement, and explicit maintenance ceiling to justify a small deployment; do not reward service count or distributed scaffolding. A single application with transactional embedded storage is sufficient, but another comparably simple supported design can pass. Avoid prescribing a language or UI toolkit.

Current: preview and approval are separate; source shows transactional replacement, not persistence of previews. Backup configuration shows an intention and a dated drill, not continuous proof of every backup. Proposed: resilient approval boundaries, validation, backup status, restore handling, or simpler operator UX as justified. Inferred: the ceiling is easily manageable locally; do not invent precise performance measurements. Unknown: preview lifetime and whether a new import can replace an unapproved preview; these can be stated as design assumptions without stopping.

Diagram must communicate operator approval, storage, backup dependency, and validation/crash or backup-unavailable behavior. It need not include separate deployment/sequence diagrams. Assessment should distinguish transactional failure recovery from restoring a lost disk, and backup unavailability from inventory unavailability. Overclaiming durability from a Python context manager or claiming network share availability is guaranteed is a defect.

No scripted human answer is necessary: core policy is inspectable. No-answer fallback: state a conservative preview-lifetime assumption and mark it proposed. No preferred brand or folder tree is required.
