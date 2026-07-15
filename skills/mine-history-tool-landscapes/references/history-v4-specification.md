# History v4 immutable specification

This is the normative Gate B-R2 contract for `history-sources/v4`,
`semantic-observation-ledger/v2`, `history-index/v4`,
`capability-reduction/v3`, `history-evidence/v1`, and
`history-publication/v3`. The six schemas are closed structural contracts.
This specification defines the cross-document, acquisition, identity, lineage,
privacy, model-authority, reconciliation, and lifecycle invariants that an
independent validator must recompute. Producer-declared hashes are claims, not
proof.

## Canonical bytes and approved component

All JSON uses `canonical-json/v1`: strict UTF-8, NFC strings, duplicate-key
rejection, integer numbers only, no non-finite values, and RFC 8785 ordering.
Parsing rejects exact duplicate object keys before normalization. The
canonicalizer NFC-normalizes every key and string value, but it must retain the
complete parsed key sequence and reject an object when two distinct parsed keys
normalize to the same scalar sequence. A normalized-key collision is an error;
a map construction that silently keeps either value is forbidden. Every formula
is SHA-256 over the ASCII domain, one NUL byte, and the stated canonical bytes.
Lowercase hexadecimal is required. Array order is significant unless this
specification explicitly sorts it.

The Gate B-R2 artifact manifest binds this file, all six schemas, the migration
table, privacy/model boundary, positive fixtures, hostile fixture catalog, and
the executable diagnostic evaluator used by every hostile receipt.
Any changed bound byte requires a new Gate B-R2 approval. Gate B-R2 authorizes
no implementation delta.

## Normative commitments and reconciliation

Define `D(domain, value)` as
`sha256(ASCII(domain) || NUL || canonical-json(value))`. A field described as
"without itself" is removed entirely before canonicalization; setting it to an
empty value is not equivalent. UTF-8 ID sorting is bytewise. A *closure set* is
an array declared below as the complete population of a fact class. Every
closure set is sorted, duplicate-free, and equals the producer-independent
projection that defines it; its named governing count equals its array length.
A *reference set* is a sorted, duplicate-free foreign-key projection and has no
independent count unless a schema names one. Reference sets must be subsets of
their closed target populations. An arbitrary array is not a closed population
merely because it has `uniqueItems`.

The exact commitments are:

```text
adapter.entry_sha256 = D("history-adapter-entry/v2", adapter without entry_sha256)
adapter.envelope_catalog_sha256 = D(
  "history-envelope-catalog/v2", adapter.envelope_catalog
)
adapter.native_id_catalog_sha256 = D(
  "history-native-id-catalog/v2", adapter.native_id_catalog
)
adapter_catalog.catalog_sha256 = D(
  "history-adapter-catalog/v2", adapter_catalog without catalog_sha256
)
raw_source_manifest_sha256 = D("raw-source-manifest/v2", sorted source records)
source_accounting.source_accounting_sha256 = D(
  "history-source-accounting/v4",
  source accounting without source_accounting_sha256
)
exclusion_ledger_sha256 = D("history-exclusion-ledger/v2", sorted exclusion records)
exact_file_set.members_sha256 = D("exact-file-set/v2", sorted member records)
history_contract_sha256 = D("history-sources/v4", complete history source contract)
```

The index manifest alone owns the complete exact file set; upstream source and
ledger documents do not bind the downstream index or its file-set digest. This
keeps the authority graph acyclic: source contract to ledger to index to
reduction to evidence to publication. To avoid an impossible self-reference,
the `index.json` member has role `manifest`, `size=null`,
`content_sha256=null`, and `hash_kind=normalized-manifest`; every other member
has its actual descriptor-read byte size and hash with `hash_kind=raw-bytes`.
Then:

```text
history_index_sha256 = D("history-index/v4", index without history_index_sha256)
```

The actual `index.json` bytes must parse to that document and pass the embedded
commitment. The authoritative acquisition receipt independently binds the
actual byte hash and descriptor facts; it is not embedded back into the index.

For each semantic record, define `semantic_body` as the complete record with
`observation_id`, `semantic_commitment_sha256`, and `ledger_record_sha256`
removed. This order avoids an identity/commitment cycle:

```text
semantic_commitment_sha256 = D("semantic-observation/v2", semantic_body)
observation_id = "obs-" || semantic_commitment_sha256
ledger_record_sha256 = D(
  "semantic-ledger-record/v2", full record without ledger_record_sha256
)
semantic_ledger_sha256 = D(
  "semantic-observation-ledger/v2",
  records sorted by source_id, raw_sha256, record_id, field, ordinal
)
corpus_sha256 = D("history-corpus/v4", {
  history_contract_id,
  raw_source_manifest_sha256,
  semantic_ledger_sha256,
  native_lineage_closure_sha256,
  exclusion_ledger_sha256,
  semantic_commitments: sorted semantic_commitment_sha256 values,
  root_ids: sorted root IDs,
  project_family_ids: sorted project-family IDs
})
native_lineage_closure_sha256 = D(
  "history-native-lineage-closure/v2",
  native_nodes sorted by platform, source_id, source_record_ordinal,
  native_type, native_hmac, node_id
)
lineage_accounting.counts_sha256 = D(
  "history-lineage-accounting/v2",
  lineage accounting without counts_sha256
)
history_index.lineage.counts_sha256 = D(
  "history-index-lineage-accounting/v4",
  index lineage without counts_sha256
)
active_campaign.fixed_point_sha256 = D(
  "active-campaign-fixed-point/v4", exact seed, descendant, namespace,
  excluded-record, and reason-count sets
)
```

Every reduction commitment excludes its own field and uses the named domain:

```text
history_binding.binding_sha256 = D("capability-history-binding/v3", history_binding without binding_sha256)
runtime_catalog.entry_sha256 = D("runtime-model-entry/v2", entry without entry_sha256)
runtime_catalog.catalog_sha256 = D("runtime-model-catalog/v2", runtime catalog without catalog_sha256 and descriptor)
provider_trust.entry_sha256 = D("provider-verifier-entry/v1", entry without entry_sha256)
provider_trust.catalog_sha256 = D("provider-verifier-trust/v1", trust catalog without catalog_sha256 and descriptor)
authority_validation.receipt_sha256 = D(
  "callable-authority-validation/v1",
  authority_validation without receipt_sha256
)
callable_verification.challenge_message_sha256 = D(
  "provider-authenticated-challenge/v1", catalog, selected entry, display name,
  callable ID, provider, settings, protocol, verifier entry, nonce, request,
  response, status, verifier version, authority-validation receipt,
  request/capture/expiry times, callable
)
callable_verification.provider_mac_hex = hmac_sha256(
  independently trusted provider verification key,
  32 bytes decoded from callable_verification.challenge_message_sha256 hex
)
callable_verification.receipt_sha256 = D("callable-verification/v2", callable verification without receipt_sha256 and descriptor)
model_resolution.resolution_sha256 = D("exploration-model-resolution/v2", model_resolution without resolution_sha256)
schedule.snapshot_sha256 = D("capability-schedule/v3", schedule without snapshot_sha256)
packet.input_sha256 = D("capability-packet/v3", packet without input_sha256)
result.output_sha256 = D("capability-result/v3", result without output_sha256)
hydration.output_sha256 = D("capability-hydration/v3", hydration without output_sha256 and receipt_sha256)
hydration.receipt_sha256 = D("capability-hydration-receipt/v3", hydration without receipt_sha256)
synthesis.input_sha256 = D("capability-primary-input/v3", {
  accepted_result_ids,
  accepted result output and receipt hashes,
  hydration_output_sha256,
  hydration_receipt_sha256
})
synthesis.output_sha256 = D("capability-synthesis/v3", synthesis without output_sha256)
reduction decision.decision_sha256 = D(
  "capability-decision/v3", reduction decision without decision_sha256
)
reduction_sha256 = D("capability-reduction/v3", reduction without reduction_sha256)
```

Evidence and publication use the same non-self-referential rule:

```text
raw_reopen_receipt.receipt_sha256 = D("raw-reopen-receipt/v2", receipt without receipt_sha256 and descriptor)
exact_input_file_set.members_sha256 = D("history-evidence-input-set/v1", descriptor records sorted by relative_path_sha256)
evidence.source_accounting.source_accounting_sha256 = D(
  "history-evidence-source-accounting/v1",
  evidence source accounting without source_accounting_sha256
)
evidence decision.evidence_decision_sha256 = D(
  "history-evidence-decision/v1",
  evidence decision without evidence_decision_sha256
)
evidence_sha256 = D("history-evidence/v1", evidence without evidence_sha256)
publication decision.publication_decision_sha256 = D(
  "history-publication-decision/v3",
  publication decision without publication_decision_sha256
)
allowed_opaque_ids_sha256 = D(
  "history-publication-opaque-ids/v3", sorted typed opaque-ID allowlist
)
publication_sha256 = D("history-publication/v3", publication without publication_sha256)
deletion_receipt.receipt_sha256 = D(
  "history-private-deletion-receipt/v2", receipt without receipt_sha256
)
post_delete_absence_sha256 = D(
  "history-private-absence/v2", sorted post_delete_absent_target_ids
)
```

All embedded descriptor `sha256` values are hashes of independently reopened
external bytes, not hashes of their containing JSON object. Normalized
commitments never replace those byte hashes. Model timestamps must satisfy
`runtime_catalog.captured_at <= requested_at <= captured_at <= resolved_at <
expires_at`; catalog and callable verification expiry may be at most 900
seconds after capture or request respectively.

The deletion receipt's descriptor-safe acquisition proof is a separate receipt
whose hash is `acquisition_receipt_sha256`; embedding the receipt's own byte
descriptor would create another forbidden self-reference. The validator
recomputes all formulas from reopened bytes and derived sets in dependency
order. Equality among producer fields without this recomputation is never
evidence.

## Descriptor-safe input acquisition

Every source, private index member, runtime catalog, trust-root receipt,
provider verification key, verifier implementation, nonce-state snapshot,
nonce-validation receipt, callable-verification receipt, evidence document,
publication document, capability catalog, deletion receipt, and adapter
implementation file is acquired once through the same bounded descriptor
algorithm:

1. Freeze the canonical authorized root, expected effective UID, literal
   normalized relative path, per-file bound, aggregate bound, and cutoff before
   inspecting content. Reject absolute paths, `..`, empty components, and
   normalized-component collisions.
2. Open the root exactly once as a directory file descriptor and retain that FD
   for the complete acquisition. Traverse every intermediate component with
   descriptor-relative `openat`-equivalent operations and
   `O_RDONLY|O_DIRECTORY|O_CLOEXEC|O_NOFOLLOW`; path re-resolution from the
   process working directory is forbidden.
3. Obtain non-following leaf metadata relative to the retained parent FD.
   Require a user-owned regular file,
   link count one, no group/other write bit, and declared per-file and aggregate
   size limits.
4. Open the leaf once, relative to the retained parent FD, with
   `O_RDONLY|O_CLOEXEC|O_NOFOLLOW`. Pre-read `fstat` must match the accepted
   device, inode, regular-file type, UID, mode, link count, size, and nanosecond
   mtime.
5. Stream bounded chunks only from that FD while hashing. Count actual bytes
   read toward both the per-file and aggregate limits. Reject decoding fallback,
   early EOF or short read, growth beyond the accepted size, trailing bytes,
   overflow, and bytes after the inclusive cutoff when a cutoff applies.
6. Before close, repeat `fstat` and require device, inode, file type, UID, mode,
   link count, size, and nanosecond mtime to equal both the accepted facts and
   the pre-read `fstat`. The acquisition receipt binds both fact sets, actual
   bytes read, aggregate bytes after the read, root authority, and open flags.

The resulting `descriptor-file/v2` record includes root authority hash,
relative-path hash, device, inode, size, mode, owner, link count, nanosecond
mtime, capture time, byte hash, and the exact open flags. If a platform cannot
provide descriptor-relative no-follow behavior, stop with
`E_DESCRIPTOR_PLATFORM_UNSAFE`. A path read, pre-open hash, or second read is
not authoritative.

For every closed directory bundle, enumerate once under the same descriptors,
sort normalized relative paths by UTF-8 bytes, and bind the exact recursive
file set and its count. Missing, extra, duplicate, special, linked, unsafe, or
changed members fail before semantic validation.

## Authorized user roots and raw sources

`history-sources/v4` freezes an inclusive pre-discovery cutoff, exact user
authority receipts, and actual user-root selection independently of transcript
metadata. The platform catalog has exactly these source families:

| Platform | Adapter | User root selection | Literal allowlist |
| --- | --- | --- | --- |
| Codex | `codex-history-jsonl` `v2` | host-resolved `CODEX_HOME`, else the authenticated user's canonical home plus `.codex` | `sessions/**/*.jsonl`, `archived_sessions/*.jsonl` |
| Claude Code | `claude-code-history-jsonl` `v2` | host-resolved `CLAUDE_CONFIG_DIR`, else the authenticated user's canonical home plus `.claude` | `projects/**/*.jsonl` |

The authority receipt binds effective user ID, canonical user-home hash,
environment-variable presence and value hash, selected-root hash, selection
basis, platform, cutoff, and capture time. A record's project metadata never
selects a root. Transcript text cannot add a root, path, glob, URI, namespace,
adapter, or remote source.

Each discovered file receives `raw-history-snapshot/v2` descriptor facts and a
raw byte hash. Files appearing during discovery are accepted, excluded exactly
once, or fail the collection; silent skipping is forbidden. The raw manifest
sorts complete source records by source ID and relative-path hash and computes:

```text
raw_source_manifest_sha256 = sha256(
  "raw-source-manifest/v2" || NUL || canonical-json(records)
)
```

## Adapter catalog and implementation binding

The adapter catalog is a descriptor-reopened frozen file, not a producer
constant. Every adapter record embeds the closed envelope catalog and native-ID
field catalog whose canonical commitments it also binds, plus platform,
adapter ID/version, parser and canonicalizer normative hashes,
redaction-policy hash, implementation file descriptor record, implementation
SHA-256, callable entrypoint, and deterministic fixture digest. The validator
reopens each implementation file and recomputes its digest. Any drift is
`E_ADAPTER_IMPLEMENTATION_DRIFT`.

An envelope-catalog entry names its outer envelope type and the complete JSON
pointer sets for semantic fields, root-intent fields, parent fields, namespace
fields, and timestamp fields. A native-ID-catalog entry names the ID type,
complete JSON pointer set, lineage role, and public prefix. Unknown outer
envelopes or uncataloged native-ID locations fail closed.

Both v2 adapters parse strict UTF-8 JSONL with no blank lines, duplicate keys,
unknown outer envelopes, non-integers, non-finite values, heuristic recovery,
content execution, or content-driven path/URI access. They retain native
session/message/parent/project/tool/user/organization/workspace identifiers in
the private native map only.

## Native lineage and root intent

Adapters emit one private native node for every semantic, non-semantic, or
excluded record. Each node binds the private native HMAC linkage and the public
`record_id`, nullable `observation_id`, `node_id`, nullable `parent_id`, nullable
`root_id`, nullable `namespace_id`, nullable `project_family_id`, classification,
classification basis, and record disposition. Classification is one of
`user-root`, `delegated`, `retry`, `continuation`, `test`, `replay`, `synthetic`,
`system`, `duplicate-export`, or `non-semantic`; disposition is exactly one of
`semantic`, `non-semantic`, or `excluded`.

A `user-root` is selected from a platform-native user-authored event with no
native parent after duplicate-export reconciliation. Codex and Claude use
their cataloged native envelope semantics; metadata labels alone cannot create
a root. Native parent edges are authoritative. Artifact edges and heuristic
edges are separately typed, carry confidence and grounding observation IDs,
and never overwrite native parentage.

The ledger owns `native_lineage_closure_sha256`. The validator recomputes every
public linkage from the private native node, then recomputes parent uniqueness,
root closure, descendants,
chronology, cycles, unresolved parents, duplicate exports, namespace aliases,
and project-family membership. Every node belongs to exactly one root closure
or the closed unresolved set. Root, child, unresolved, non-semantic,
duplicate-export, excluded, namespace, and project-family sets and counts
reconcile exactly. The ledger closure sets are `source_ids`, `record_ids`,
`semantic_record_ids`, `excluded_record_ids`, `nonsemantic_record_ids`,
`observation_ids`, `node_ids`, `root_ids`, `child_ids`, `unresolved_ids`,
`duplicate_export_ids`, `nonsemantic_ids`, `excluded_ids`, `namespace_ids`, and
`project_family_ids`; every named count is the length of its corresponding set.

## Per-index unlinkable identity

Before collection, create a new random 32-byte index salt and a user-owned HMAC
key outside git. Both are descriptor-bound private members with mode `0600`;
their parent bundle is mode `0700`. Reuse across indexes is forbidden.

For any private native value:

```text
native_hmac = hmac_sha256(
  identity_key,
  "history-native-id/v2" || NUL || index_salt || NUL ||
  UTF8(platform || ":" || native_type || ":" || native_value)
)
```

For every public type and full native HMAC:

```text
public_digest = hmac_sha256(
  identity_key,
  "history-public-id/v2" || NUL || index_salt || NUL ||
  UTF8(public_type) || NUL || native_hmac
)
public_id = public_prefix || "-" || lowercase_hex(public_digest)
```

`public_type` and `public_prefix` come from the approved native-ID catalog;
synthetic reducer-owned IDs use their schema field name as `public_type` and
the corresponding closed schema prefix. No truncation is allowed. Opaque
public IDs are therefore derived from the full HMAC and a type domain, never
from raw hashes or native values. Observation, record, root, project-family,
namespace, artifact, conflict, state, capability, overlap, and decision IDs
are unique within one index. The index binds salt/key receipt hashes and an
identity-domain version; it never stores the salt, key, native value, or a
reversible native hash in public documents. Recollecting identical history
under another index must yield unlinkable IDs.

## Complete native-ID redaction and semantic ledger

Before semantic text leaves the adapter, the complete native map is frozen.
Its closed type-count table and HMAC-set digest cover session, message, parent,
project, tool, user, organization, workspace, namespace, task, thread, run,
job, artifact, and provider-specific IDs discovered in every accepted or
excluded record. An uncataloged native-ID type is an adapter error, not an
exemption.

Redaction applies the approved credential, URI, absolute-path, email, native-ID,
and high-entropy rules to NFC text. Native values of every length are matched
as literal scalar sequences in descending length/UTF-8 order; there is no UUID,
hex, or opaque-looking exemption. Keys and values are rescanned after
replacement. A residual native value, credential, URI, absolute path, email,
or disallowed control is `E_REDACTION_INCOMPLETE`.

`semantic-observation-ledger/v2` binds each observation to its raw source,
typed private lineage node, root, project family, field, ordinal, canonical
locator, redacted text hash, native-set digest, and semantic commitment. The
validator reopens raw files, reruns the approved adapter and redactor, and
recomputes the complete sorted ledger:

```text
semantic_ledger_sha256 = sha256(
  "semantic-observation-ledger/v2" || NUL || canonical-json(records)
)
```

Self-supplied or packet-recomputed commitments never authorize changed text,
source, record, lineage, locator, or root ownership.

## Active campaign exclusion

Every source contract carries exactly one `active_campaign` disposition.
`not-applicable` requires a descriptor-bound authority receipt proving the
cutoff predates the campaign or the authorized roots cannot contain it.
Otherwise `active-campaign/v4` binds platform, start time, root native HMAC,
alias HMACs, namespace HMACs, identity-key receipt, and one exact exclusion
closure.

The validator requires platform equality, parent/child timestamps not earlier
than their parents, root time not earlier than campaign start, unique native
parentage, unambiguous aliases, no conflicting namespace ownership, no cycles,
and fixed-point descendant closure. Same-namespace records at or after campaign
start are excluded. Post-cutoff records never seed closure. Missing timestamps,
conflicting parents, cycles, alias ambiguity, platform mismatch, chronology
failure, or incomplete closure stops collection.

Every discovered record is included, excluded exactly once with a grounded
reason, or accounted as accepted non-semantic. `source_accounting.source_ids`
is exactly the source array's `source_id` projection; `source_count` equals its
length. Its four aggregate record counts are sums of the corresponding
per-source counts, and `parsed_record_count = semantic_record_count +
nonsemantic_record_count + excluded_record_count`. Raw-manifest,
semantic-ledger, and exclusion-ledger counts equal those same closed
projections. Reason counts and source/root/
namespace sets reconcile with the raw manifest, lineage, semantic ledger,
index, evidence, and publication.

The index lineage is an exact public projection of the ledger accounting: its
source, record, semantic-record, excluded-record, non-semantic-record,
observation, node, root, child, unresolved, excluded, duplicate-export,
non-semantic, namespace, and project-family sets equal the same-named ledger
sets; its counts equal their lengths. `history_index.lineage.counts_sha256`
commits the complete lineage object without that field. The index binding,
history binding, and evidence binding each repeat the ledger's
`native_lineage_closure_sha256`; mismatches stop before reduction.

## History index and exact lifecycle

`history-index/v4` is the closed manifest for one private bundle. Its required
recursive members are `index.json`, `sources.json`, `semantic-ledger.json`,
`exclusion-ledger.json`, `native-map.json`, `identity-salt`,
`identity-key`, `identity-key.receipt.json`, `adapter-catalog.json`, and
`lifecycle.json`.
Every additional private copy is forbidden unless it is declared in the exact
file set with role `declared-private-copy` before validation; each declared copy
becomes an independently identified deletion target.

The lifecycle state machine is:

```text
collecting -> live -> validation-complete -> deletion-pending -> deleted
             live -> expired -> deletion-pending -> deleted
```

Only the shown transitions are legal. `delete-after-validation` must enter
`deletion-pending` immediately after the final successful validation and before
publication. `delete-by` must do so no later than the deadline. Expired,
deletion-pending, or deleted state cannot hydrate, synthesize, validate evidence,
or publish.

The deletion target set exactly equals every ledger, exclusion ledger, native
map, salt, identity key, key receipt, adapter work file, descriptor snapshot containing a
private path, and every declared copy. The live index carries a null deletion
receipt. After deletion, a non-private `history-index/v4` tombstone carries the
pre-delete member commitments and a closed
`history-private-deletion-receipt/v2`; its exact-file-set state is `tombstone`,
every member path is null, and it contains no path, native value, salt, key,
ledger text, or reversible identifier. The receipt binds opaque target
IDs, roles, pre-delete hashes/modes/counts, every state transition, one deletion
attempt per target, the equal post-delete absent-target set, its digest, and a
descriptor record for the receipt itself. Missing targets, an unaccounted copy,
an illegal transition, or a target absent from the proof is
`E_PRIVATE_FILE_SET_MISMATCH`.

## Exact exploration-model authority

The only approved economy display name is exactly `5.6 lunar high`. Before any
model-visible packet is created, the coordinator descriptor-opens a frozen
runtime catalog and a separately captured callable-verification receipt. The
catalog contains every model entry, provider, callable ID, status, supported
settings, and capture time. The receipt binds catalog byte hash, selected entry
ordinal and full entry hash, display name, callable ID, provider, settings hash,
verification protocol, fresh challenge nonce, request/response hashes,
challenge-message commitment, provider authentication MAC, command status,
descriptor-reopened verifier implementation, trusted provider-key entry,
request/capture/expiry times, and receipt
commitment. `model_resolution.authority_validation` is a separately acquired
`callable-authority-validation/v1` receipt. It binds the independently approved
trust-root receipt, actual provider-key and verifier-implementation descriptors,
the external nonce-state descriptor and its before/after hashes, the exact prior
used-nonce and used-receipt sets, validation time, and the 900-second maximum
age. The trusted provider-key catalog is rooted independently of the model
catalog and reduction producer. Each selected trust entry's descriptors must
equal the authority-validation descriptors, but equality alone is not
authority. The validator reopens the trust-root receipt, key, verifier, and
nonce state under the same acquisition rules and verifies the independent
authorization.

Within `authority_validation`, `trust_root_receipt_sha256`,
`provider_key_sha256`, and `verifier_sha256` equal the actual byte hashes in
their corresponding descriptors. `used_nonce_count` and `used_receipt_count`
equal the lengths of their sorted duplicate-free sets. The reopened nonce-state
bytes before validation must parse to exactly those two prior sets and commit as
`nonce_state_before_sha256`. A receipt replay key is the provider-authenticated
pre-authority `callable_verification.response_sha256`, not the challenge-message
or final callable receipt hash; this avoids an authority-validation/challenge
commitment cycle. The atomically
replaced after-state equals those sets union the current challenge nonce and
receipt replay key, commits as `nonce_state_after_sha256`, and its actual byte
hash equals `nonce_state.sha256`. The callable verification's
`authority_validation_receipt_sha256` equals `authority_validation.receipt_sha256`
and is part of the challenge-message commitment.

The validator independently reopens both files, recomputes their descriptor and
byte bindings, requires exactly one catalog entry with the exact display name,
requires it callable under the bound settings, and verifies the receipt against
that entry. Producer-declared display name, alias, family, or callable ID is not
authority. The validator verifies the provider-authenticated HMAC-SHA-256
challenge with the selected independently trusted key, requires a never-used
nonce and provider receipt against the prior state, exact request/response
binding, timestamp ordering, and a maximum 900-second freshness window. The
authority validation's used sets are the descriptor-reopened state before this
call; they must omit both the challenge nonce and receipt replay key. The
after-state hash must commit the atomic append of both values
before the callable receipt becomes usable. A byte-identical replayed receipt is
stale after first use because the currently reopened prior state then contains
both replay keys. Missing, ambiguous,
uncallable, stale, replayed, or unverifiable mapping stops
before disclosure with `E_EXPLORATION_MODEL_UNAVAILABLE`; substitution is
forbidden.

The economy model receives only one bounded redacted source-bound
`capability-packet/v3`. It may classify, summarize, and cluster that packet.
It may not select sources, plan the campaign, widen scope, access another
packet, adjudicate overlap, choose a target skill, decide create/extend/reject,
approve a gate, mutate files, or write final synthesis. The coordinator owns
planning, hydration, cross-packet synthesis, overlap adjudication, and final
decisions. The data policy is exactly
`bounded-redacted-source-bound-packets-only`.

## Capability reduction and catalog-valid decisions

`capability-reduction/v3` binds the live v4 index, exact model resolution,
frozen capability catalog, schedule, packets, attempts, results, hydration,
synthesis, and decisions. Every packet observation is looked up in the live v2
ledger and must equal its source, record, root, project family, locator, text,
and commitment. Unknown or cross-packet evidence is retained as dropped quality
evidence and contributes zero authority.

Retries preserve the immutable packet. Split children form an exact disjoint
partition of their parent. Every terminal packet has exactly one accepted
result. Hydration reopens the same live ledger and exact accepted set. The
primary synthesis input equals the canonical accepted result/receipt set plus
hydration output/receipt.

Each independently rooted `user-root` contributes at most one recurrence credit
per candidate after reducer review. Delegated, retry, continuation, test,
replay, synthetic, system, duplicate-export, non-semantic, excluded, and active
campaign records contribute zero. Independent-root and project-family counts
are separate exact sets.

The candidate-ID set and the reduction decision's `candidate_id` projection are
equal. Every candidate has exactly one
`create`, `extend`, or `reject` decision. Only `extend` has a target, and that
target ID must exist in the descriptor-reopened frozen capability catalog.
Create/reject cannot carry a target. Decision evidence collectively covers the
candidate's accepted hydrated observations. Every reduction decision carries
`decision_sha256`.

Evidence projects each reduction decision by copying `decision_id`,
`candidate_id`, `disposition`, `target_skill_id`, and
`evidence_observation_ids` byte-for-byte and binding the source
`reduction_decision_sha256`. Evidence adds only the exact `claim_ids`,
`capability_ids`, and `overlap_ids` reference closures and its own
`evidence_decision_sha256`. Publication projects that evidence decision by
copying all IDs, disposition, and target, renaming `evidence_observation_ids`
to `observation_ids`, binding `evidence_decision_sha256`, and adding only the
bounded rationale plus `publication_decision_sha256`. No stage may synthesize,
drop, duplicate, retarget, or reorder a decision.

## Closed evidence reconciliation

`history-evidence/v1` is authoritative only after full raw reopening. There is
no authoritative skip-raw flag. A diagnostic command that omits raw reopening
must emit `history-diagnostic/v1`, `authoritative=false`, and
`E_RAW_REOPEN_REQUIRED`; it cannot hydrate, synthesize, validate evidence, or
publish.

Evidence recursively closes and exactly reconciles these closure sets and their counts:
sources, included/excluded/non-semantic records, lineage nodes, roots, children,
unresolved nodes, duplicate exports, namespaces, project families,
observations, claims, artifacts, conflicts,
states, reduction candidates, capabilities, overlaps, and decisions. Each
lineage edge has type, endpoints, occurrence timestamp, confidence, grounding
observation IDs, and state. Every claim/artifact/conflict/state/capability/overlap/decision cites
existing allowed IDs. Recurrence sets equal reducer-reviewed user roots and
project families. Candidate IDs equal the decisions' candidate-ID projection;
decision IDs are independently closed. Extend targets are
catalog-valid. No count may be supplied without its exact sorted ID set.

`counts.sources`, `included_records`, `excluded_records`,
`nonsemantic_records`, and `observations` govern the corresponding
`source_accounting` sets; lineage counts govern their same-named lineage sets;
object counts govern the top-level object arrays. Reference sets inside an
object are checked as typed foreign keys against those closed populations.
`counts.scope_roots` governs `lineage.scope_root_ids`, and `counts.excluded`
governs `lineage.excluded_ids`. Evidence source IDs equal the source-contract
and index source closure; included, excluded, and non-semantic record sets form
an exact duplicate-free partition of the index record set. Observation IDs
equal the semantic ledger observation closure. Publication copies those five
source-accounting sets and their governing counts exactly and carries
`source_accounting_sha256` equal to the validated evidence value.

Lineage mode requires the complete requested lineage scope, roots, edges,
unresolved/excluded accounting, claims, artifacts, conflicts, states, and no
reduction decisions. Capability mode requires the complete candidate,
capability, overlap, recurrence, project-family, and exactly-one decision sets.
Mixed or missing mode outputs fail closed.

## Closed publication and privacy

`history-publication/v3` is derived only from validated evidence and carries the
same exact public sets/counts permitted for its mode. The validator recomputes
its evidence binding, source/count closure, decision projection, and set
projections. It scans every key and value,
including extensions hidden in strings. Publication allows only per-index
opaque IDs, lower-case hashes, bounded paraphrases, normalized public source
IDs, enum states, integers, and the schema's structured locators.

Raw transcript text, raw bytes, private ledger content, native values or HMACs,
salt/key material, absolute paths, URIs, email addresses, credentials, signed
URLs, provider/thread/session/run/job IDs, unrecognized opaque IDs, and unknown
keys are forbidden. UUID/hex appearance grants no exemption. Every opaque ID
must be present in the validated evidence allowlist and typed for its field.

## Breaking migration and diagnostics

No compatibility shim or producer-side conversion exists. Diagnostics are
ordered; the first applicable condition is returned before generic schema
failure.

| Priority | Input condition | Exact diagnostic | Required action |
| --- | --- | --- | --- |
| 1 | `history-sources/v1`, `/v2`, or `/v3` | `E_HISTORY_SOURCES_VERSION_UNSUPPORTED` | recollect under v4 |
| 2 | missing v2 descriptor snapshot | `E_RAW_SNAPSHOT_REBUILD_REQUIRED` | reread authorized raw sources |
| 3 | ledger absent or not v2 | `E_SEMANTIC_LEDGER_REBUILD_REQUIRED` | rerun v2 adapters and redaction |
| 4 | index absent or not v4 | `E_HISTORY_INDEX_REBUILD_REQUIRED` | rebuild the private index |
| 5 | reduction v1/v2 | `E_CAPABILITY_REDUCTION_VERSION_UNSUPPORTED` | rebuild packets/results under v3 |
| 6 | evidence absent or older | `E_HISTORY_EVIDENCE_VERSION_UNSUPPORTED` | regenerate closed v1 evidence |
| 7 | publication v1/v2 | `E_HISTORY_PUBLICATION_VERSION_UNSUPPORTED` | regenerate closed v3 publication |
| 8 | stale/missing exact history binding | `E_HISTORY_BINDING_REQUIRED` | bind the live v4 index |
| 9 | authoritative validation without raw reopening | `E_RAW_REOPEN_REQUIRED` | reopen all raw descriptors |
| 10 | exact economy model unavailable | `E_EXPLORATION_MODEL_UNAVAILABLE` | stop before disclosure |

Old bytes may indicate what to recollect but provide no successor authority.

## Hostile conformance catalog

Gate B-R2 binds 12 positive examples, including an all-excluded active-campaign
ledger with zero semantic observations, 61 protocol-resealed hostile cases
(including a byte-identical receipt under already-used nonce state),
one descriptor-reopened authority ground-truth catalog containing raw Codex and
Claude envelopes plus model/verifier inputs, and twelve executable filesystem
attacks. A mode-0700 synthetic private bundle materializes all ten mandatory
mode-0600 members; it contains only invented fixture data and test-only keys.
The validator recursively reopens that bundle and compares every non-manifest
member's actual size and byte hash to the live index. Every
hostile fixture starts from the positive bundle, mutates the named authoritative
fact, then recomputes every producer-controlled digest, count, receipt, and
outer hash named in its reseal receipt. `expected_diagnostic` is test input, not
proof. The candidate validator invokes the actual ordered diagnostic evaluator
against independently reopened ground truth and external state. Its
`history-diagnostic/v1` execution receipt binds evaluator implementation bytes,
input hash, authority hash, state-before hash, selected priority, and
`actual_diagnostic`; validation compares that returned value to
`expected_diagnostic`. Copying an expectation from a catalog or hard-coded map
does not execute a hostile test. For replay cases, the harness first commits the
nonce and receipt replay key as used, then evaluates the byte-identical receipt
against that state. The candidate validator independently recomputes
normative commitments, materializes every filesystem attack in a temporary
mode-0700 root, and checks the evaluator's returned exact diagnostic. S-013
must reject each fixture from independently reopened ground truth before any
model disclosure.

`selected_priority` is the evaluator-selected predicate priority, never the
fixture ordinal. Priorities 1 through 10 are exactly the ordered migration
table; all other closed diagnostics occupy the catalog-bound namespace after
priority 10. `fixture_ordinal` separately records catalog position. A
multi-fault input binds the first diagnostic actually returned under that
ordering.

The catalog covers: Codex metadata-selected false roots; Claude missing roots;
wrong native parent type; conflicting parents; cycles; chronology inversion;
cross-index deterministic IDs; incomplete native-ID types; surviving Claude
UUID/hex IDs; active-campaign platform/alias/namespace/closure errors; changed
raw bytes; unsafe permissions; size overflow; special files; symlinks; hard
links; descriptor races; changed adapter bytes with resealed producer hashes;
extra/missing private files; illegal lifecycle/deletion transitions; undeleted
copies/salt/key/native maps; substituted model callable IDs; changed runtime
catalog or verification receipt; stale/replayed callable receipts; expired
ledgers; authoritative raw bypass; swapped excerpts,
records, roots, candidates, locators, corpus, or ledger facts; recurrence count
inflation; missing or duplicate decisions; nonexistent extension targets;
incomplete lineage/artifact/conflict/state/capability/overlap sets; and private
identifier/path/URI/credential leakage in publication keys or values.
It also covers every old contract family and a simultaneous version/snapshot
fault proving that ordered migration diagnostics take precedence over generic
schema failure.

## Acceptance matrix

S-013 is complete only when the exact approved bytes remain unchanged and the
following proof is current:

| Surface | Positive proof | Required negative proof |
| --- | --- | --- |
| six schemas | Draft 2020-12 metaschema and closed valid fixtures | unknown fields, old versions, mixed modes |
| source/root selection | both platform user roots and raw manifests recompute | metadata roots, extra roots, unsafe descriptors |
| adapters/lineage | stable Codex and Claude typed roots/edges/families | conflicts, cycles, chronology, drift |
| identity/redaction | two indexes are unlinkable; full native set removed | UUID/hex/native-type leaks and ID reuse |
| active campaign | exact fixed-point exclusion and counts | platform, alias, namespace, parent, cycle, time attacks |
| private lifecycle | exact files, legal transitions, complete deletion | copies, missing targets, unsafe modes, stale use |
| model resolution | reopened catalog plus callable receipt | alias/callable/catalog/receipt substitution |
| reduction | exact packets, attempts, hydration, decisions | cross-packet evidence, recurrence inflation, bad target |
| evidence | exact mode-specific sets/counts/edges | omitted, duplicate, dangling, or inconsistent sets |
| publication | exact projection and allowlisted opaque IDs | leakage in keys/values and unrecognized IDs |
| migration | every older family rejected in priority order | generic schema failure before exact diagnostic |
| raw authority | full reopen supports validation | non-authoritative diagnostics cannot advance |
