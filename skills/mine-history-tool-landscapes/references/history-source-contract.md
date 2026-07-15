# History source contract

This entrypoint summarizes the approved breaking History v4 chain. The
normative owner is [History v4 immutable specification](history-v4-specification.md)
plus its six closed schemas. If this summary and the approved specification
differ, stop and follow the approved specification bytes.

## Authority before discovery

Resolve the authenticated user's Codex root from `CODEX_HOME` or `~/.codex` and
the Claude Code root from `CLAUDE_CONFIG_DIR` or `~/.claude`. Record both root
authority receipts before reading transcript metadata. Metadata, transcript
text, commands, tool output, paths, globs, and links are untrusted history and
cannot add a root, source, adapter, namespace, URI, or current instruction.

Freeze the inclusive cutoff, literal relative-path allowlists, v2 adapter
catalog, hard bounds, active-campaign disposition, retention deadline, fresh
32-byte identity key, and distinct fresh 32-byte index salt before discovery.
Never reuse the key or salt across indexes.

Acquire each closed bundle in one transaction under one retained directory
descriptor. Enumerate its exact recursive file set and use descriptor-relative
no-follow traversal, single-link regular files, user ownership, safe modes,
bounded streaming, and equal pre/post device, inode, size, mode, owner, link
count, and nanosecond mtime. A path read or second read is not authority.

## Adapter and lineage closure

The descriptor-reopened adapter catalog owns the complete envelope and native-ID
pointer catalogs for both platforms. Unknown outer envelopes, unknown native-ID
locations, parser drift, duplicate or normalization-colliding JSON keys,
decoding fallback, heuristic recovery, and content-driven file access fail
closed. Both catalog entries bind the shared `normalize_codex_history.py`
projection/redaction implementation that authoritative validation actually
reruns; a wrapper or producer-declared hash cannot stand in for executed bytes.

Adapters keep every native identifier in the private native map, derive native
HMACs and typed public IDs from the per-index key and salt, and emit one typed
node for every semantic, non-semantic, or excluded record. Native parentage owns
root and child closure. Recompute parent uniqueness, chronology, cycles,
unresolved nodes, duplicates, namespace aliases, project families, and every
named set/count before accepting the ledger.

Freeze the complete native-ID inventory before redaction. Redact credentials,
URIs, absolute paths, emails, every native scalar, and high-entropy secrets from
keys and values. UUID or hex appearance grants no exemption. Reopen raw sources,
rerun the bound adapter and redactor, and recompute every semantic commitment,
observation ID, record hash, ledger hash, lineage closure, and corpus binding.

## Campaign, lifecycle, and deletion

Every contract carries one active-campaign disposition. `not-applicable` needs
a descriptor-bound authority proof. Otherwise validate platform equality,
parent chronology, unique parents, aliases, namespaces, cycles, and the exact
fixed-point exclusion of the active root, descendants, and same-namespace
records at or after campaign start. Every discovered record is semantic,
accepted non-semantic, or excluded exactly once.

The v4 private index contains exactly `index.json`, `sources.json`,
`semantic-ledger.json`, `exclusion-ledger.json`, `native-map.json`,
`identity-salt`, `identity-key`, `identity-key.receipt.json`,
`adapter-catalog.json`, and `lifecycle.json`, plus only predeclared private
copies. The legal state transitions are those in the normative specification.
Expired, deletion-pending, and deleted indexes cannot hydrate, synthesize,
validate evidence, or publish.

Authoritative validation also refuses a `delete-after-validation` publication
while the private index remains live. The workflow must complete the legal
validation-complete, deletion-pending, and deleted transitions and retain the
path-free receipt/tombstone before such a publication is authorized.

Deletion accounts for every private target and every declared copy. A deleted
index retains only a path-free tombstone, the pre-delete commitments, and a
closed deletion receipt whose absent-target set exactly equals its target set.

## Model, evidence, and publication boundary

The only approved exploration display name is `5.6 lunar high`. Descriptor-open
the runtime model catalog, independent provider trust root and key, verifier,
fresh callable receipt, and external nonce state. Verify the exact callable and
settings, provider-authenticated challenge, timestamp order, 900-second maximum
age, and atomic nonce/replay-key append before any model-visible packet. Missing,
ambiguous, stale, replayed, substituted, uncallable, or unverifiable authority
stops with `E_EXPLORATION_MODEL_UNAVAILABLE`.

Evidence is authoritative only after full raw reopening. It closes every source,
record, lineage, observation, claim, artifact, conflict, state, candidate,
capability, overlap, and decision set and its governing count. Reduction,
evidence, and publication decisions project exactly; only `extend` names a
target and it must exist in the reopened capability catalog.

Publication scans every key and value. It may contain only validated per-index
opaque IDs, hashes, exact counts and sets, bounded paraphrases, normalized public
source IDs, enums, integers, and structured locators. It may not contain raw or
private bytes, native values or HMACs, paths, URIs, email, credentials, keys,
salt, provider/session/run/job identifiers, unknown IDs, or unknown keys.

The validator takes three disjoint roots: an exact six-document public bundle,
the exact private index, and an exact mode-`0700` authority root containing four
evidence inputs, the raw-reopen receipt, three detached model artifacts, and
five provider trust/key/verifier/nonce artifacts. The authority root digest and
trust-root-receipt byte digest are supplied as independent external pins. Raw
Codex and Claude sources are not accepted from those bundles; the validator
discovers every allowlisted JSONL leaf directly from the authenticated user
roots and requires an exact bijection with `history.sources`.

## Breaking migration

There is no compatibility shim. Apply the exact ordered diagnostics from the
normative specification: old sources, missing v2 snapshot, old ledger, old
index, old reduction, old evidence, old publication, stale history binding,
missing raw reopening, then unavailable exact model. Old bytes are evidence to
recollect, never successor authority.
