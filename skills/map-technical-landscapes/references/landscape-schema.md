# Landscape data contract

Use strict UTF-8 JSON with `schema_version` set to `map-technical-landscapes/v2`. Duplicate object keys and JSON constants such as `NaN` and `Infinity` are invalid.

Version 2 replaces the v1 prose-only stopping rule with measurable fields, adds discovery accounting and candidate relationships, ties gaps to fields and sources, and makes source access and equivalence explicit. V1 artifacts must be migrated before validation; the validator intentionally does not guess these new facts.

Every object accepts only the properties declared below. Every listed property is required, including properties whose value may be `null` or an empty array.

[`landscape-v2.schema.json`](landscape-v2.schema.json) is the machine-readable structural contract. The Python validator adds reference, accounting, identity, provenance, and stopping semantics that JSON Schema cannot express cleanly.

## Root object

Require `schema_version`, `scope`, `field_catalog`, `sources`, `candidates`, `discovery_records`, `identity_decisions`, `candidate_relationships`, `claims`, `taxonomy`, `coverage`, and `summary`.

## Scope and fields

`scope` contains:

- non-empty `question`;
- `unit_of_analysis`: `paper`, `model`, `repository`, `product`, `system`, or `mixed`;
- strict, timezone-aware RFC 3339 `frozen_at` with seconds;
- non-empty, unique `inclusion_rules` and `exclusion_rules`;
- `stopping_rule`, containing non-empty unique `required_query_families` and `required_source_families`, positive integer `minimum_completed_searches`, positive integer `minimum_consecutive_no_new_candidates`, and non-empty `method`.

Each `field_catalog` item has a unique lowercase-hyphen `id`, non-empty `label`, `value_type` (`string`, `number`, `boolean`, or `string-list`), and boolean `required`. The catalog itself is non-empty.

## Sources and claims

Each source has a unique `id`, non-empty `title`, `source_class` (`primary` or `secondary`), structured `locator`, timezone-aware `accessed_at`, `access_status` (`accessible`, `blocked`, or `unavailable`), `version_context` (non-empty string or `null`), and an `equivalence_group` lowercase-hyphen ID. Different locators for mirrors of the same underlying source use the same equivalence group. Duplicate locators are invalid.

Locator forms are:

- `url`: `{ "type": "url", "value": "https://..." }`, with no userinfo credentials or credential-like query/fragment keys such as tokens, passwords, API keys, credentials, or signatures;
- `file`: `{ "type": "file", "value": "/absolute/path" }`;
- `doi`: `{ "type": "doi", "value": "10.<registrant>/<suffix>" }`;
- `commit`: `{ "type": "commit", "repository": "https://...", "rev": "<40-or-64-hex-revision>" }`.

Each claim has a unique `id`, non-empty `candidate_ids`, `field_id` (a catalog ID or `null`), atomic non-empty `statement`, `epistemic_status` (`observed` or `inferred`), non-empty `source_ids`, and `source_strength` (`primary`, `secondary`, or `mixed`). Claims may cite only accessible sources. An inferred claim requires at least two distinct source-equivalence groups. Declared strength matches the cited source-class mix.

## Candidates, discovery accounting, and relationships

Each candidate has a unique `id`, non-empty `name`, unique non-empty `aliases`, `status` (`included` or `excluded`), `exclusion_reason` (non-empty string for excluded candidates, otherwise `null`), `exclusion_claim_ids`, `comparison`, and `technique_ids`. Every alias has a matching identity decision: a unique alias has a merged decision and discovery record, while an alias shared by deliberately separate candidates has an exact kept-separate decision.

Each discovery record has `id`, non-empty `observed_name`, `resolution` (`canonical`, `merged`, or `unresolved`), `candidate_ids`, non-empty `reason`, and non-empty `source_ids`. Canonical and merged records resolve to exactly one candidate; unresolved records resolve to none. Every canonical candidate has exactly one canonical discovery record. A merged record resolves to a declared alias and has one matching merged identity decision.

Each identity decision records `observed_name`, `decision` (`merged` or `kept-separate`), `canonical_candidate_ids`, non-empty `reason`, and non-empty `source_ids`. A normalized observed name has only one decision. A merged alias resolves to exactly one candidate. A kept-separate decision resolves to at least two candidates whose names or aliases include the observed name.

Each candidate relationship has unique `id`, `from_candidate_id`, `to_candidate_id`, `relationship` (`version`, `mirror`, `fork`, or `related`), non-empty `reason`, and non-empty `source_ids`. Endpoints differ; duplicate directed relationship triples are invalid.

Normalize names with Unicode NFKC, whitespace collapse, trim, and case-folding before identity collision and decision checks.

## Comparison cells

Included candidates cover every required field. Each comparison cell contains:

- `status`: `observed`, `inferred`, `unknown`, or `not-applicable`;
- `value`: typed finite value or `null`;
- `claim_ids` and `gap_ids`;
- `note`: string or `null`.

Observed or inferred cells require a typed value and claims matching candidate, field, and epistemic status. Unknown cells require `null`, no claims, a non-empty explanation, and an `unknown-field` gap matching candidate and field. Not-applicable cells require `null`, a non-empty explanation, and a supporting claim matching candidate and field. Excluded candidates require a reason and candidate-matching evidence claim but empty comparison and technique assignments.

## Taxonomy

`taxonomy` contains `techniques` and `unclassified`. Each technique has `id`, non-empty `name`, non-empty `description`, non-empty included `candidate_ids`, and non-empty `claim_ids`. Every assigned candidate is covered by at least one listed claim. Candidate-to-technique references are symmetric. An included candidate with no technique appears once in `taxonomy.unclassified` with a matching `taxonomy-unclassified` gap.

## Coverage and summary

`coverage.searches` is non-empty. Each search records `id`, non-empty `channel`, `query_family`, `source_family`, and `query`, `status` (`completed`, `blocked`, or `failed`), timezone-aware `started_at`, `hit_count`, `new_candidate_ids`, and `note`. Completed searches have a non-negative integer hit count. Blocked or failed searches have `null` hit count, no new candidates, a non-empty note, and a matching coverage gap.

`coverage.gaps` records `id`, `kind`, non-empty `description`, and arrays of referenced `candidate_ids`, `claim_ids`, `source_ids`, `search_ids`, and `field_ids`. Supported kinds are `unknown-field`, `secondary-only-evidence`, `blocked-search`, `failed-search`, `inaccessible-source`, `taxonomy-unclassified`, and `coverage-other`. Kind-specific references must agree with the referenced object.

`coverage.counts` contains `discovered_records`, `canonical_candidates`, `merged_records`, `included`, `excluded`, and `unresolved_records`; every value is derived from discovery records and canonical candidates. The invariant is `discovered_records = canonical_candidates + merged_records + unresolved_records`.

`coverage.stop_assessment` contains boolean `met`, `search_ids`, and a non-empty `note`. It always cites at least one search. When `met` is true, it cites every completed search in chronological order. That full ledger meets the declared minimum, covers all required query and source families, and ends with the declared number of consecutive searches that found no new canonical candidate.

`summary.mode` is `neutral` or `decision`. Neutral mode contains only `mode` and non-empty `neutral_summary`. Decision mode contains only `mode`, non-empty `decision_question`, non-empty `recommendation`, and non-empty grounded `rationale_claim_ids`.

Run `scripts/validate_landscape.py`. It validates structure and internal consistency, not factual source accuracy, claim atomicity, legal conclusions, or real-world exhaustiveness.
