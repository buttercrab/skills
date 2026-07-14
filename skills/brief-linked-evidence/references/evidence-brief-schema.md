# Evidence brief schema

Use UTF-8 JSON with `schema_version` set to `evidence-brief-v1`.

## Root object

Require `schema_version`, `question`, `requested_resources`, `sources`, `answer`, `facts`, `inferences`, `unknowns`, `conflicts`, `context_map`, `actions`, and `decision`.

IDs use lowercase letters, digits, and hyphens, start with a letter, and are globally unique across all collections. Global uniqueness keeps mixed fact/inference decision references unambiguous.

## Requested resources and sources

Every in-scope user input appears once in `requested_resources` with `id`, a redacted or public `input_locator`, and `source_id`. Preserve aliases and redirects as separate requested-resource mappings to the same canonical source when appropriate. Never store embedded credentials, signed query parameters, private access tokens, or secret-bearing URLs.

Each source records:

- `id`;
- `provenance_class`: `requested-resource`, `linked-primary-source`, or `external-corroboration`;
- `kind`: `web-page`, `dashboard`, `slack-thread`, `calendar-event`, `pdf`, `paper`, `github-resource`, or `other`;
- `title` and `resource_locator`;
- `mutability`: `mutable`, `immutable`, or `unknown`;
- `authority`: `primary`, `official`, `secondary`, `community`, or `unknown`;
- `access_scope`: `public`, `private`, `restricted`, or `unknown`;
- `acquisition`;
- `version_context`.

Acquisition status is `acquired`, `blocked`, `failed`, or `not-attempted`. Acquired sources require `method` and a receipt with `provider`, a redacted or opaque `resource_id`, timezone-aware `retrieved_at`, and connector-specific `details`. Details must not contain credentials or private source content. Other statuses require a structured reason.

`version_context` is always an object. It records timezone-aware `observed_at` for acquired sources plus applicable timezone-aware `publication_at` and `updated_at`, and non-empty `version`, `timezone`, and `commit_context` fields. Acquired GitHub resources require at least one of `commit_context`, `version`, or `updated_at`. Use `unknown` for unavailable mutability, authority, or access scope; do not silently omit provenance fields.

## Answer, facts, and inference

`answer.status` is `answered`, `partial`, or `insufficient-evidence`. These predicates apply to the root fact and unknown collections, not merely the IDs selected in `answer`: answered requires facts and no unknowns; partial requires both; insufficient evidence requires unknowns and no facts.

Each fact contains `id`, stable `assertion_key`, finite scalar `value`, atomic `claim`, and one or more citations. Each citation references an acquired source and a structured locator. Locator kinds are `section`, `page`, `line-range`, `message`, `event-field`, `table-cell`, `json-path`, `timestamp`, `anchor`, or `custom`. Pages are positive pages or ordered ranges; line ranges are ordered positive `start-end` ranges; JSON paths begin with `$` and select below the root; table cells use A1 notation; timestamps are timezone-aware ISO timestamps or media timestamps; custom locators use `namespace:value`. Do not use punctuation-only values, `unknown`, `n/a`, or `entire source` as a locator.

Each inference contains `id`, `statement`, non-empty `based_on_fact_ids`, `reasoning`, and `confidence`. Do not attach source citations directly to inferences.

Each unknown contains `id`, `question`, `reason`, `related_source_ids`, and `related_fact_ids`, with at least one valid relation.

## Conflicts and context

Facts with the same `assertion_key` and different scalar values require a conflict record. Each conflict references at least two facts, values, and acquired sources; records `resolved` or `unresolved`; and explains the disagreement. The referenced sources carry authority and version context so both positions remain auditable. Resolved conflicts also provide `resolution` and a finite scalar `resolved_value`.

When more than one source exists, use `context_map` edges between distinct source IDs. Relationship types are `links-to`, `attaches`, `corroborates`, `contradicts`, `updates`, `context-for`, or `same-event`.

## Decisions and actions

An optional decision contains `recommendation`, grounded fact or inference basis IDs, and referenced next-action IDs.

Every action declares its `operation` and redacted or opaque `resource_id`. Action status is `proposed`, `authorized`, `completed`, `failed`, or `cancelled`. Authorized, completed, and failed actions require an authorization record containing:

- structured `source` with `kind` equal to `user-message` or `user-request` and an opaque `resource_id`;
- non-empty `scope`;
- matching `operation` and `resource_id`; and
- timezone-aware `authorized_at`.

Completed actions require a receipt with matching operation and resource ID plus non-empty `provider`, opaque `receipt_id`, and timezone-aware `completed_at`. Completion cannot precede authorization. Proposed actions must not contain a completion receipt. These checks prove only local structural consistency: the action-specific capability must independently verify authority and the provider receipt before mutating or claiming completion.

Run `scripts/validate_evidence_brief.py`. It rejects duplicate JSON keys, non-standard or non-finite numbers, common secret-bearing fields and locators, and internal provenance inconsistencies without contacting external systems. Secret detection is defense in depth, not a substitute for redaction at acquisition time.
