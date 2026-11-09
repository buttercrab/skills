# Evaluator notes — contract-monorepo
Private assessment fixture, not an active skill.

Expected roles: map schema authority, generator/output boundary, gateway producer, console assumption, and independent SDK/gateway release units. The committed SDK omits the schema's optional source field under the stated generation specification. Console assumes source is always a string, which gateway currently supplies; do not assert a demonstrated console crash for the gateway path. Non-gateway producer behavior is a stated possibility rather than observed traffic. Compileall cannot show schema synchronization or consumer compatibility. Gateway check depends on a label, with no contract-path trigger or enforcement shown. No successful runs, published versions, or actual deployments are evidenced.

Prioritize regeneration/drift verification and representative producer-consumer compatibility checks, including optional source, plus reliable contract-triggered checks. Keep releases independent; propose compatibility policy and sequencing rather than a single compulsory version. The omitted generator means executing or certifying its determinism is out of scope.

Material human decision: whether SDK should reject or preserve unknown fields, and whether source should remain optional. An assessment may ask one compact policy question after delivering known findings. Scripted answer if asked: "Keep source optional; preserve unknown fields for round trips, but document known fields. Keep independent releases." No-answer fallback: retain current optional schema and independent units, flag unknown-field policy as pending, and offer conditional policy branches. Never invent approval for required source or coupled releases.

Do not prescribe a monorepo platform, global build rewrite, or gold folder tree. Cross-contract references should serve actual producer/boundary/consumer checks. No edits to real repositories or active skill/library content.
