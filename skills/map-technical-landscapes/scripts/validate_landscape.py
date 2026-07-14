#!/usr/bin/env python3
"""Validate a map-technical-landscapes v2 JSON artifact without external access."""

from __future__ import annotations

import json
import math
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlparse


ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
DOI_RE = re.compile(r"^10\.\d{4,9}/[^\s]+$")
REV_RE = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
SECRET_URL_KEY_RE = re.compile(r"(?:api[-_]?key|token|secret|passw(?:or)?d|credential|signature|authorization)", re.IGNORECASE)
TOP_KEYS = {
    "schema_version",
    "scope",
    "field_catalog",
    "sources",
    "candidates",
    "discovery_records",
    "identity_decisions",
    "candidate_relationships",
    "claims",
    "taxonomy",
    "coverage",
    "summary",
}


def timestamp(value: object) -> bool:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).split()).casefold()


def enum_value(value: object, allowed: set[str]) -> bool:
    return isinstance(value, str) and value in allowed


def identity_values(candidate: dict) -> list[str]:
    values: list[str] = []
    if isinstance(candidate.get("name"), str):
        values.append(candidate["name"])
    aliases = candidate.get("aliases")
    if isinstance(aliases, list):
        values.extend(alias for alias in aliases if isinstance(alias, str))
    return values


def alias_values(candidate: dict) -> list[str]:
    aliases = candidate.get("aliases")
    return [alias for alias in aliases if isinstance(alias, str)] if isinstance(aliases, list) else []


def contains_ref(item: dict, key: str, value: str) -> bool:
    values = item.get(key)
    return isinstance(values, list) and value in values


def ref_values(item: dict, key: str) -> list[str]:
    values = item.get(key)
    return [value for value in values if isinstance(value, str)] if isinstance(values, list) else []


def url_has_secret_parameter(parsed) -> bool:
    pairs = list(parse_qsl(parsed.query, keep_blank_values=True))
    if "=" in parsed.fragment:
        pairs.extend(parse_qsl(parsed.fragment, keep_blank_values=True))
    return any(SECRET_URL_KEY_RE.search(key) for key, _ in pairs)


def parsed_public_url(value: object):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = urlparse(value)
        _ = parsed.port
        hostname = parsed.hostname
    except ValueError:
        return None
    if (
        parsed.scheme not in {"http", "https"}
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or url_has_secret_parameter(parsed)
    ):
        return None
    return parsed


def canonical_url(parsed) -> tuple[object, ...]:
    port = parsed.port
    if (parsed.scheme == "http" and port == 80) or (parsed.scheme == "https" and port == 443):
        port = None
    return (
        parsed.scheme.lower(),
        parsed.hostname.casefold(),
        port,
        parsed.path or "/",
        parsed.query,
    )


class Validator:
    def __init__(self, data: object):
        self.data = data
        self.errors: list[dict[str, str]] = []

    def err(self, path: str, code: str, message: str) -> None:
        self.errors.append({"path": path, "code": code, "message": message})

    def exact(self, item: object, path: str, required: set[str]) -> dict:
        if not isinstance(item, dict):
            self.err(path, "wrong-type", "must be an object")
            return {}
        for key in sorted(required - set(item)):
            self.err(f"{path}/{key}", "missing-field", "required property is missing")
        for key in sorted(set(item) - required):
            self.err(f"{path}/{key}", "unknown-field", "property is not declared by schema v2")
        return item

    def unique_ids(self, items: object, path: str, *, nonempty: bool = False) -> dict[str, dict]:
        result: dict[str, dict] = {}
        if not isinstance(items, list):
            self.err(path, "wrong-type", "must be an array")
            return result
        if nonempty and not items:
            self.err(path, "empty", "must not be empty")
        for index, item in enumerate(items):
            item_path = f"{path}/{index}"
            if not isinstance(item, dict):
                self.err(item_path, "wrong-type", "must be an object")
                continue
            ident = item.get("id")
            if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
                self.err(f"{item_path}/id", "invalid-id", "must be a lowercase hyphen identifier")
                continue
            if ident in result:
                self.err(f"{item_path}/id", "duplicate-id", f"duplicate id {ident!r}")
            else:
                result[ident] = item
        return result

    def refs(self, values: object, allowed: set[str], path: str, *, nonempty: bool = False) -> list[str]:
        if not isinstance(values, list):
            self.err(path, "wrong-type", "must be an array")
            return []
        if nonempty and not values:
            self.err(path, "empty", "must not be empty")
        string_values = [value for value in values if isinstance(value, str)]
        if len(string_values) != len(set(string_values)):
            self.err(path, "duplicate-reference", "contains duplicate references")
        for index, value in enumerate(values):
            if not isinstance(value, str) or value not in allowed:
                self.err(f"{path}/{index}", "dangling-reference", f"unknown reference {value!r}")
        return [value for value in string_values if value in allowed]

    def nonempty_text(self, value: object, path: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            self.err(path, "empty", "must be a non-empty string")
            return False
        return True

    def string_list(
        self,
        values: object,
        path: str,
        *,
        min_items: int = 0,
        normalized_unique: bool = False,
    ) -> list[str]:
        if not isinstance(values, list):
            self.err(path, "wrong-type", "must be an array")
            return []
        valid = [value for value in values if isinstance(value, str) and value.strip()]
        if len(valid) != len(values):
            self.err(path, "invalid-list", "must contain only non-empty strings")
        if len(values) < min_items:
            self.err(path, "too-short", f"must contain at least {min_items} items")
        keys = [normalize(value) if normalized_unique else value for value in valid]
        if len(keys) != len(set(keys)):
            self.err(path, "duplicate-value", "must contain unique values")
        return valid

    def validate(self) -> list[dict[str, str]]:
        root = self.exact(self.data, "", TOP_KEYS)
        if not root:
            return self.errors
        if root.get("schema_version") != "map-technical-landscapes/v2":
            self.err("/schema_version", "invalid-value", "must equal map-technical-landscapes/v2")

        scope = self.exact(
            root.get("scope"),
            "/scope",
            {"question", "unit_of_analysis", "frozen_at", "inclusion_rules", "exclusion_rules", "stopping_rule"},
        )
        self.nonempty_text(scope.get("question"), "/scope/question")
        if not enum_value(scope.get("unit_of_analysis"), {"paper", "model", "repository", "product", "system", "mixed"}):
            self.err("/scope/unit_of_analysis", "invalid-value", "invalid unit")
        if not timestamp(scope.get("frozen_at")):
            self.err("/scope/frozen_at", "invalid-timestamp", "must be strict timezone-aware RFC 3339 with seconds")
        self.string_list(scope.get("inclusion_rules"), "/scope/inclusion_rules", min_items=1)
        self.string_list(scope.get("exclusion_rules"), "/scope/exclusion_rules", min_items=1)
        stop_rule = self.exact(
            scope.get("stopping_rule"),
            "/scope/stopping_rule",
            {
                "method",
                "required_query_families",
                "required_source_families",
                "minimum_completed_searches",
                "minimum_consecutive_no_new_candidates",
            },
        )
        self.nonempty_text(stop_rule.get("method"), "/scope/stopping_rule/method")
        required_query_families = self.string_list(
            stop_rule.get("required_query_families"),
            "/scope/stopping_rule/required_query_families",
            min_items=2,
            normalized_unique=True,
        )
        required_source_families = self.string_list(
            stop_rule.get("required_source_families"),
            "/scope/stopping_rule/required_source_families",
            min_items=2,
            normalized_unique=True,
        )
        for key in ("minimum_completed_searches", "minimum_consecutive_no_new_candidates"):
            value = stop_rule.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                self.err(f"/scope/stopping_rule/{key}", "invalid-count", "must be a positive integer")

        fields = self.unique_ids(root.get("field_catalog"), "/field_catalog", nonempty=True)
        for ident, field in fields.items():
            path = f"/field_catalog/{ident}"
            self.exact(field, path, {"id", "label", "value_type", "required"})
            self.nonempty_text(field.get("label"), f"{path}/label")
            if not enum_value(field.get("value_type"), {"string", "number", "boolean", "string-list"}):
                self.err(f"{path}/value_type", "invalid-value", "invalid value_type")
            if not isinstance(field.get("required"), bool):
                self.err(f"{path}/required", "wrong-type", "must be boolean")

        sources = self.unique_ids(root.get("sources"), "/sources", nonempty=True)
        seen_locators: dict[tuple[object, ...], str] = {}
        for ident, source in sources.items():
            path = f"/sources/{ident}"
            self.exact(
                source,
                path,
                {"id", "title", "source_class", "locator", "accessed_at", "access_status", "version_context", "equivalence_group"},
            )
            self.nonempty_text(source.get("title"), f"{path}/title")
            if not enum_value(source.get("source_class"), {"primary", "secondary"}):
                self.err(f"{path}/source_class", "invalid-value", "must be primary or secondary")
            if not timestamp(source.get("accessed_at")):
                self.err(f"{path}/accessed_at", "invalid-timestamp", "must be strict timezone-aware RFC 3339 with seconds")
            if not enum_value(source.get("access_status"), {"accessible", "blocked", "unavailable"}):
                self.err(f"{path}/access_status", "invalid-value", "invalid access status")
            version_context = source.get("version_context")
            if version_context is not None and (not isinstance(version_context, str) or not version_context.strip()):
                self.err(f"{path}/version_context", "invalid-value", "must be null or a non-empty string")
            if not isinstance(source.get("equivalence_group"), str) or not ID_RE.fullmatch(source.get("equivalence_group", "")):
                self.err(f"{path}/equivalence_group", "invalid-id", "must be a lowercase hyphen identifier")

            locator = source.get("locator")
            locator_path = f"{path}/locator"
            canonical: tuple[object, ...] | None = None
            if not isinstance(locator, dict):
                self.err(locator_path, "wrong-type", "must be an object")
            else:
                kind = locator.get("type")
                if enum_value(kind, {"url", "file", "doi"}):
                    self.exact(locator, locator_path, {"type", "value"})
                    value = locator.get("value")
                    if kind == "url":
                        parsed = parsed_public_url(value)
                        if parsed is None:
                            self.err(f"{locator_path}/value", "invalid-locator", "URL must be public http(s) without credentials or secret parameters")
                        else:
                            canonical = ("url", *canonical_url(parsed))
                    elif kind == "file":
                        if not isinstance(value, str) or not Path(value).is_absolute():
                            self.err(f"{locator_path}/value", "invalid-locator", "file locator must be absolute")
                        else:
                            canonical = ("file", os.path.normpath(value))
                    else:
                        if not isinstance(value, str) or not DOI_RE.fullmatch(value):
                            self.err(f"{locator_path}/value", "invalid-locator", "invalid DOI")
                        else:
                            canonical = ("doi", value.casefold())
                elif kind == "commit":
                    self.exact(locator, locator_path, {"type", "repository", "rev"})
                    parsed = parsed_public_url(locator.get("repository"))
                    if parsed is None:
                        self.err(f"{locator_path}/repository", "invalid-locator", "repository must be public http(s) without userinfo credentials")
                    if not isinstance(locator.get("rev"), str) or not REV_RE.fullmatch(locator.get("rev", "")):
                        self.err(f"{locator_path}/rev", "invalid-locator", "revision must be 40 or 64 hexadecimal characters")
                    if parsed is not None and isinstance(locator.get("rev"), str) and REV_RE.fullmatch(locator["rev"]):
                        canonical = ("commit", *canonical_url(parsed), locator["rev"].casefold())
                else:
                    self.err(f"{locator_path}/type", "invalid-locator", "type must be url, file, doi, or commit")
            if canonical is not None:
                if canonical in seen_locators:
                    self.err(locator_path, "duplicate-locator", f"duplicates source {seen_locators[canonical]}")
                else:
                    seen_locators[canonical] = ident

        candidates = self.unique_ids(root.get("candidates"), "/candidates")
        claims = self.unique_ids(root.get("claims"), "/claims")
        discovery_records = self.unique_ids(root.get("discovery_records"), "/discovery_records")
        relationships = self.unique_ids(root.get("candidate_relationships"), "/candidate_relationships")
        coverage_raw = root.get("coverage") if isinstance(root.get("coverage"), dict) else {}
        gaps = self.unique_ids(coverage_raw.get("gaps", []), "/coverage/gaps")
        taxonomy_raw = root.get("taxonomy") if isinstance(root.get("taxonomy"), dict) else {}
        techniques = self.unique_ids(taxonomy_raw.get("techniques", []), "/taxonomy/techniques")
        searches = self.unique_ids(coverage_raw.get("searches", []), "/coverage/searches", nonempty=True)

        for ident, claim in claims.items():
            path = f"/claims/{ident}"
            self.exact(claim, path, {"id", "candidate_ids", "field_id", "statement", "epistemic_status", "source_ids", "source_strength"})
            self.nonempty_text(claim.get("statement"), f"{path}/statement")
            self.refs(claim.get("candidate_ids"), set(candidates), f"{path}/candidate_ids", nonempty=True)
            source_ids = self.refs(claim.get("source_ids"), set(sources), f"{path}/source_ids", nonempty=True)
            state = claim.get("epistemic_status")
            if not enum_value(state, {"observed", "inferred"}):
                self.err(f"{path}/epistemic_status", "invalid-value", "must be observed or inferred")
            inaccessible = [source_id for source_id in source_ids if sources[source_id].get("access_status") != "accessible"]
            if inaccessible:
                self.err(f"{path}/source_ids", "inaccessible-evidence", f"claims may not cite inaccessible sources: {inaccessible}")
            groups = {value for source_id in source_ids if isinstance((value := sources[source_id].get("equivalence_group")), str)}
            if state == "inferred" and len(groups) < 2:
                self.err(f"{path}/source_ids", "insufficient-independent-evidence", "inference requires two source-equivalence groups")
            classes = {value for source_id in source_ids if isinstance((value := sources[source_id].get("source_class")), str)}
            actual_strength = "mixed" if len(classes) > 1 else (next(iter(classes)) if classes else None)
            if claim.get("source_strength") != actual_strength:
                self.err(f"{path}/source_strength", "strength-mismatch", f"must be {actual_strength!r}")
            field_id = claim.get("field_id")
            if field_id is not None and field_id not in fields:
                self.err(f"{path}/field_id", "dangling-reference", "unknown field")

        name_owners: dict[str, set[str]] = {}
        alias_owners: dict[str, set[str]] = {}
        for ident, candidate in candidates.items():
            path = f"/candidates/{ident}"
            self.exact(
                candidate,
                path,
                {"id", "name", "aliases", "status", "exclusion_reason", "exclusion_claim_ids", "comparison", "technique_ids"},
            )
            self.nonempty_text(candidate.get("name"), f"{path}/name")
            aliases = self.string_list(candidate.get("aliases"), f"{path}/aliases", normalized_unique=True)
            identities = [candidate.get("name"), *aliases]
            normalized_identities = [normalize(value) for value in identities if isinstance(value, str) and value.strip()]
            if len(normalized_identities) != len(set(normalized_identities)):
                self.err(f"{path}/aliases", "identity-collision", "name and aliases must be distinct after normalization")
            for value in identities:
                if isinstance(value, str) and value.strip():
                    name_owners.setdefault(normalize(value), set()).add(ident)
            for alias in aliases:
                alias_owners.setdefault(normalize(alias), set()).add(ident)
            status = candidate.get("status")
            if not enum_value(status, {"included", "excluded"}):
                self.err(f"{path}/status", "invalid-value", "must be included or excluded")
            comparison = candidate.get("comparison")
            technique_ids = self.refs(candidate.get("technique_ids"), set(techniques), f"{path}/technique_ids")
            exclusion_ids = self.refs(candidate.get("exclusion_claim_ids"), set(claims), f"{path}/exclusion_claim_ids")
            if status == "excluded":
                self.nonempty_text(candidate.get("exclusion_reason"), f"{path}/exclusion_reason")
                if not exclusion_ids:
                    self.err(f"{path}/exclusion_claim_ids", "empty", "excluded candidate needs evidence")
                for claim_id in exclusion_ids:
                    if not contains_ref(claims[claim_id], "candidate_ids", ident):
                        self.err(f"{path}/exclusion_claim_ids", "claim-candidate-mismatch", f"claim {claim_id} does not reference candidate")
                if comparison != {} or technique_ids:
                    self.err(path, "excluded-has-comparison", "excluded candidate must have empty comparison and techniques")
                continue
            if candidate.get("exclusion_reason") is not None or exclusion_ids:
                self.err(path, "included-has-exclusion", "included candidate must use null reason and no exclusion claims")
            if not isinstance(comparison, dict):
                self.err(f"{path}/comparison", "wrong-type", "must be an object")
                comparison = {}
            for field_id, field in fields.items():
                if field.get("required") and field_id not in comparison:
                    self.err(f"{path}/comparison", "missing-field", f"missing required field {field_id}")
            for field_id, cell in comparison.items():
                cell_path = f"{path}/comparison/{field_id}"
                if field_id not in fields:
                    self.err(cell_path, "unknown-field", "field not declared in catalog")
                    continue
                cell = self.exact(cell, cell_path, {"status", "value", "claim_ids", "gap_ids", "note"})
                state = cell.get("status")
                value = cell.get("value")
                claim_ids = self.refs(cell.get("claim_ids"), set(claims), f"{cell_path}/claim_ids")
                gap_ids = self.refs(cell.get("gap_ids"), set(gaps), f"{cell_path}/gap_ids")
                note = cell.get("note")
                if note is not None and not isinstance(note, str):
                    self.err(f"{cell_path}/note", "wrong-type", "must be a string or null")
                if enum_value(state, {"observed", "inferred"}):
                    expected = fields[field_id].get("value_type")
                    type_ok = (
                        (expected == "string" and isinstance(value, str) and bool(value.strip()))
                        or (expected == "number" and isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value))
                        or (expected == "boolean" and isinstance(value, bool))
                        or (
                            expected == "string-list"
                            and isinstance(value, list)
                            and bool(value)
                            and all(isinstance(item, str) and item.strip() for item in value)
                            and len(value) == len(set(value))
                        )
                    )
                    if not type_ok or not claim_ids:
                        self.err(cell_path, "ungrounded-cell", "observed/inferred cell needs a typed finite value and claim")
                    for claim_id in claim_ids:
                        claim = claims[claim_id]
                        if not contains_ref(claim, "candidate_ids", ident) or claim.get("field_id") != field_id or claim.get("epistemic_status") != state:
                            self.err(cell_path, "claim-cell-mismatch", f"claim {claim_id} does not match candidate, field, and status")
                elif state == "unknown":
                    matching_gaps = [
                        gap_id
                        for gap_id in gap_ids
                        if gaps[gap_id].get("kind") == "unknown-field"
                        and contains_ref(gaps[gap_id], "candidate_ids", ident)
                        and contains_ref(gaps[gap_id], "field_ids", field_id)
                    ]
                    if value is not None or claim_ids or not matching_gaps or not isinstance(note, str) or not note.strip():
                        self.err(cell_path, "invalid-unknown", "unknown needs null, no claims, a matching unknown-field gap, and note")
                elif state == "not-applicable":
                    matching_claims = [
                        claim_id
                        for claim_id in claim_ids
                        if contains_ref(claims[claim_id], "candidate_ids", ident) and claims[claim_id].get("field_id") == field_id
                    ]
                    if value is not None or not matching_claims or not isinstance(note, str) or not note.strip():
                        self.err(cell_path, "invalid-not-applicable", "not-applicable needs null, matching field claim, and note")
                else:
                    self.err(f"{cell_path}/status", "invalid-value", "invalid cell status")

        decisions_raw = root.get("identity_decisions")
        if not isinstance(decisions_raw, list):
            self.err("/identity_decisions", "wrong-type", "must be an array")
            decisions_raw = []
        decision_by_name: dict[str, dict] = {}
        for index, decision in enumerate(decisions_raw):
            path = f"/identity_decisions/{index}"
            decision = self.exact(decision, path, {"observed_name", "decision", "canonical_candidate_ids", "reason", "source_ids"})
            observed = decision.get("observed_name")
            self.nonempty_text(observed, f"{path}/observed_name")
            self.nonempty_text(decision.get("reason"), f"{path}/reason")
            candidate_ids = self.refs(decision.get("canonical_candidate_ids"), set(candidates), f"{path}/canonical_candidate_ids", nonempty=True)
            self.refs(decision.get("source_ids"), set(sources), f"{path}/source_ids", nonempty=True)
            key = normalize(observed) if isinstance(observed, str) and observed.strip() else ""
            if key:
                if key in decision_by_name:
                    self.err(path, "contradictory-identity-decision", "normalized observed name already has a decision")
                else:
                    decision_by_name[key] = decision
            kind = decision.get("decision")
            if kind == "merged":
                if len(candidate_ids) != 1:
                    self.err(f"{path}/canonical_candidate_ids", "invalid-merge", "merged decision must resolve to one candidate")
                elif key not in {normalize(alias) for alias in alias_values(candidates[candidate_ids[0]])}:
                    self.err(path, "invalid-merge", "merged observed_name must be a declared alias")
            elif kind == "kept-separate":
                if len(candidate_ids) < 2:
                    self.err(f"{path}/canonical_candidate_ids", "invalid-split", "kept-separate needs at least two candidates")
                elif any(key not in {normalize(value) for value in identity_values(candidates[cid])} for cid in candidate_ids):
                    self.err(path, "invalid-split", "observed_name must identify every kept-separate candidate")
            else:
                self.err(f"{path}/decision", "invalid-value", "must be merged or kept-separate")

        for key, owners in name_owners.items():
            if len(owners) < 2:
                continue
            decision = decision_by_name.get(key)
            linked = set(decision.get("canonical_candidate_ids", [])) if decision and decision.get("decision") == "kept-separate" else set()
            if owners != linked:
                self.err("/candidates", "identity-collision", f"identity {key!r} collides across {sorted(owners)} without exact kept-separate decision")

        canonical_record_counts = {candidate_id: 0 for candidate_id in candidates}
        merged_record_names: set[tuple[str, str]] = set()
        for ident, record in discovery_records.items():
            path = f"/discovery_records/{ident}"
            self.exact(record, path, {"id", "observed_name", "resolution", "candidate_ids", "reason", "source_ids"})
            observed = record.get("observed_name")
            self.nonempty_text(observed, f"{path}/observed_name")
            self.nonempty_text(record.get("reason"), f"{path}/reason")
            candidate_ids = self.refs(record.get("candidate_ids"), set(candidates), f"{path}/candidate_ids")
            self.refs(record.get("source_ids"), set(sources), f"{path}/source_ids", nonempty=True)
            resolution = record.get("resolution")
            key = normalize(observed) if isinstance(observed, str) and observed.strip() else ""
            if resolution == "canonical":
                if len(candidate_ids) != 1:
                    self.err(f"{path}/candidate_ids", "invalid-resolution", "canonical record resolves to exactly one candidate")
                else:
                    canonical_record_counts[candidate_ids[0]] += 1
                    candidate_name = candidates[candidate_ids[0]].get("name")
                    if not isinstance(candidate_name, str) or key != normalize(candidate_name):
                        self.err(path, "identity-mismatch", "canonical observed_name must match candidate name")
            elif resolution == "merged":
                if len(candidate_ids) != 1:
                    self.err(f"{path}/candidate_ids", "invalid-resolution", "merged record resolves to exactly one candidate")
                else:
                    candidate_id = candidate_ids[0]
                    merged_record_names.add((key, candidate_id))
                    decision = decision_by_name.get(key)
                    candidate_aliases = alias_values(candidates[candidate_id])
                    if key not in {normalize(alias) for alias in candidate_aliases} or not decision or decision.get("decision") != "merged" or decision.get("canonical_candidate_ids") != [candidate_id]:
                        self.err(path, "identity-mismatch", "merged record needs matching alias and merged identity decision")
            elif resolution == "unresolved":
                if candidate_ids:
                    self.err(f"{path}/candidate_ids", "invalid-resolution", "unresolved record must not resolve to a candidate")
            else:
                self.err(f"{path}/resolution", "invalid-value", "must be canonical, merged, or unresolved")
        for candidate_id, count in canonical_record_counts.items():
            if count != 1:
                self.err("/discovery_records", "accounting-mismatch", f"candidate {candidate_id} needs exactly one canonical discovery record, found {count}")
        for key, decision in decision_by_name.items():
            if decision.get("decision") == "merged":
                candidate_id = decision.get("canonical_candidate_ids", [None])[0] if decision.get("canonical_candidate_ids") else None
                if (key, candidate_id) not in merged_record_names:
                    self.err("/discovery_records", "missing-merged-record", f"merged decision {key!r} lacks a discovery record")
        for key, owners in alias_owners.items():
            decision = decision_by_name.get(key)
            if len(owners) == 1:
                owner = next(iter(owners))
                if not decision or decision.get("decision") != "merged" or decision.get("canonical_candidate_ids") != [owner] or (key, owner) not in merged_record_names:
                    self.err("/identity_decisions", "missing-alias-decision", f"alias {key!r} needs matching merged decision and discovery record")
            elif not decision or decision.get("decision") != "kept-separate" or set(decision.get("canonical_candidate_ids", [])) != owners:
                self.err("/identity_decisions", "missing-alias-decision", f"shared alias {key!r} needs exact kept-separate decision")

        relationship_keys: set[tuple[str, str, str]] = set()
        for ident, relationship in relationships.items():
            path = f"/candidate_relationships/{ident}"
            self.exact(relationship, path, {"id", "from_candidate_id", "to_candidate_id", "relationship", "reason", "source_ids"})
            from_id = relationship.get("from_candidate_id")
            to_id = relationship.get("to_candidate_id")
            self.refs([from_id], set(candidates), f"{path}/from_candidate_id", nonempty=True)
            self.refs([to_id], set(candidates), f"{path}/to_candidate_id", nonempty=True)
            kind = relationship.get("relationship")
            if not enum_value(kind, {"version", "mirror", "fork", "related"}):
                self.err(f"{path}/relationship", "invalid-value", "invalid relationship")
            self.nonempty_text(relationship.get("reason"), f"{path}/reason")
            self.refs(relationship.get("source_ids"), set(sources), f"{path}/source_ids", nonempty=True)
            if from_id == to_id and from_id in candidates:
                self.err(path, "self-relationship", "relationship endpoints must differ")
            key = (from_id, to_id, kind)
            if all(isinstance(value, str) for value in key):
                if key in relationship_keys:
                    self.err(path, "duplicate-relationship", "duplicate directed relationship")
                relationship_keys.add(key)

        taxonomy = self.exact(root.get("taxonomy"), "/taxonomy", {"techniques", "unclassified"})
        for ident, technique in techniques.items():
            path = f"/taxonomy/techniques/{ident}"
            self.exact(technique, path, {"id", "name", "description", "candidate_ids", "claim_ids"})
            self.nonempty_text(technique.get("name"), f"{path}/name")
            self.nonempty_text(technique.get("description"), f"{path}/description")
            candidate_ids = self.refs(technique.get("candidate_ids"), set(candidates), f"{path}/candidate_ids", nonempty=True)
            claim_ids = self.refs(technique.get("claim_ids"), set(claims), f"{path}/claim_ids", nonempty=True)
            for candidate_id in candidate_ids:
                candidate_technique_ids = candidates[candidate_id].get("technique_ids")
                if candidates[candidate_id].get("status") != "included" or not isinstance(candidate_technique_ids, list) or ident not in candidate_technique_ids:
                    self.err(path, "taxonomy-mismatch", f"candidate {candidate_id} does not symmetrically reference technique")
                if not any(contains_ref(claims[claim_id], "candidate_ids", candidate_id) for claim_id in claim_ids):
                    self.err(f"{path}/claim_ids", "taxonomy-claim-mismatch", f"no taxonomy claim covers candidate {candidate_id}")
        for candidate_id, candidate in candidates.items():
            if candidate.get("status") == "included":
                raw_technique_ids = candidate.get("technique_ids")
                for technique_id in raw_technique_ids if isinstance(raw_technique_ids, list) else []:
                    if technique_id in techniques and not contains_ref(techniques[technique_id], "candidate_ids", candidate_id):
                        self.err(f"/candidates/{candidate_id}/technique_ids", "taxonomy-mismatch", f"technique {technique_id} does not reference candidate")

        unclassified = taxonomy.get("unclassified") if isinstance(taxonomy, dict) else None
        if not isinstance(unclassified, list):
            self.err("/taxonomy/unclassified", "wrong-type", "must be an array")
            unclassified = []
        unclassified_ids: set[str] = set()
        for index, item in enumerate(unclassified):
            path = f"/taxonomy/unclassified/{index}"
            item = self.exact(item, path, {"candidate_id", "gap_id"})
            candidate_id = item.get("candidate_id")
            gap_id = item.get("gap_id")
            if candidate_id not in candidates or candidates[candidate_id].get("status") != "included":
                self.err(f"{path}/candidate_id", "dangling-reference", "must reference an included candidate")
            elif candidate_id in unclassified_ids:
                self.err(f"{path}/candidate_id", "duplicate-reference", "candidate appears twice")
            else:
                unclassified_ids.add(candidate_id)
            if gap_id not in gaps or gaps[gap_id].get("kind") != "taxonomy-unclassified" or not contains_ref(gaps[gap_id], "candidate_ids", candidate_id):
                self.err(f"{path}/gap_id", "invalid-gap", "must reference a matching taxonomy-unclassified gap")
        for candidate_id, candidate in candidates.items():
            if candidate.get("status") != "included":
                continue
            if candidate.get("technique_ids") and candidate_id in unclassified_ids:
                self.err("/taxonomy/unclassified", "taxonomy-mismatch", f"classified candidate {candidate_id} is also unclassified")
            if not candidate.get("technique_ids") and candidate_id not in unclassified_ids:
                self.err("/taxonomy/unclassified", "missing-unclassified", f"candidate {candidate_id} has no technique and is not unclassified")

        coverage = self.exact(root.get("coverage"), "/coverage", {"searches", "counts", "gaps", "stop_assessment"})
        for ident, search in searches.items():
            path = f"/coverage/searches/{ident}"
            self.exact(search, path, {"id", "channel", "query_family", "source_family", "query", "status", "started_at", "hit_count", "new_candidate_ids", "note"})
            for key in ("channel", "query_family", "source_family", "query"):
                self.nonempty_text(search.get(key), f"{path}/{key}")
            if not timestamp(search.get("started_at")):
                self.err(f"{path}/started_at", "invalid-timestamp", "must be strict timezone-aware RFC 3339 with seconds")
            new_candidate_ids = self.refs(search.get("new_candidate_ids"), set(candidates), f"{path}/new_candidate_ids")
            status = search.get("status")
            hit_count = search.get("hit_count")
            note = search.get("note")
            if note is not None and not isinstance(note, str):
                self.err(f"{path}/note", "wrong-type", "must be a string or null")
            if status == "completed":
                if not isinstance(hit_count, int) or isinstance(hit_count, bool) or hit_count < 0:
                    self.err(f"{path}/hit_count", "invalid-count", "completed search needs non-negative integer hit_count")
                elif hit_count < len(new_candidate_ids):
                    self.err(f"{path}/hit_count", "accounting-mismatch", "hit_count cannot be smaller than new candidate count")
            elif enum_value(status, {"blocked", "failed"}):
                if hit_count is not None or new_candidate_ids or not isinstance(note, str) or not note.strip():
                    self.err(path, "invalid-search", "blocked/failed search needs null count, no new candidates, and note")
            else:
                self.err(f"{path}/status", "invalid-value", "invalid search status")

        allowed_gap_kinds = {
            "unknown-field",
            "secondary-only-evidence",
            "blocked-search",
            "failed-search",
            "inaccessible-source",
            "taxonomy-unclassified",
            "coverage-other",
        }
        for ident, gap in gaps.items():
            path = f"/coverage/gaps/{ident}"
            self.exact(gap, path, {"id", "kind", "description", "candidate_ids", "claim_ids", "source_ids", "search_ids", "field_ids"})
            kind = gap.get("kind")
            if not enum_value(kind, allowed_gap_kinds):
                self.err(f"{path}/kind", "invalid-value", "invalid gap kind")
            self.nonempty_text(gap.get("description"), f"{path}/description")
            candidate_ids = self.refs(gap.get("candidate_ids"), set(candidates), f"{path}/candidate_ids")
            claim_ids = self.refs(gap.get("claim_ids"), set(claims), f"{path}/claim_ids")
            source_ids = self.refs(gap.get("source_ids"), set(sources), f"{path}/source_ids")
            search_ids = self.refs(gap.get("search_ids"), set(searches), f"{path}/search_ids")
            field_ids = self.refs(gap.get("field_ids"), set(fields), f"{path}/field_ids")
            if not any((candidate_ids, claim_ids, source_ids, search_ids, field_ids)):
                self.err(path, "ungrounded-gap", "gap must reference at least one object")
            if kind == "unknown-field" and (not candidate_ids or not field_ids):
                self.err(path, "invalid-gap", "unknown-field gap needs candidate and field references")
            if kind == "unknown-field" and any((claim_ids, source_ids, search_ids)):
                self.err(path, "gap-reference-mismatch", "unknown-field gap may reference only candidates and fields")
            if kind == "blocked-search" and (not search_ids or any(searches[sid].get("status") != "blocked" for sid in search_ids)):
                self.err(path, "invalid-gap", "blocked-search gap must reference blocked searches")
            if kind == "blocked-search" and any((candidate_ids, claim_ids, source_ids, field_ids)):
                self.err(path, "gap-reference-mismatch", "blocked-search gap may reference only searches")
            if kind == "failed-search" and (not search_ids or any(searches[sid].get("status") != "failed" for sid in search_ids)):
                self.err(path, "invalid-gap", "failed-search gap must reference failed searches")
            if kind == "failed-search" and any((candidate_ids, claim_ids, source_ids, field_ids)):
                self.err(path, "gap-reference-mismatch", "failed-search gap may reference only searches")
            if kind == "inaccessible-source" and (not source_ids or any(sources[sid].get("access_status") == "accessible" for sid in source_ids)):
                self.err(path, "invalid-gap", "inaccessible-source gap must reference blocked or unavailable sources")
            if kind == "inaccessible-source" and any((candidate_ids, claim_ids, search_ids, field_ids)):
                self.err(path, "gap-reference-mismatch", "inaccessible-source gap may reference only sources")
            if kind == "taxonomy-unclassified" and not candidate_ids:
                self.err(path, "invalid-gap", "taxonomy-unclassified gap needs a candidate")
            if kind == "taxonomy-unclassified" and any((claim_ids, source_ids, search_ids, field_ids)):
                self.err(path, "gap-reference-mismatch", "taxonomy-unclassified gap may reference only candidates")
            if kind == "secondary-only-evidence" and (not claim_ids or any(claims[cid].get("source_strength") != "secondary" for cid in claim_ids)):
                self.err(path, "invalid-gap", "secondary-only-evidence gap must reference secondary claims")
            if kind == "secondary-only-evidence" and claim_ids:
                claim_candidates = {candidate_id for claim_id in claim_ids for candidate_id in ref_values(claims[claim_id], "candidate_ids")}
                claim_fields = {claims[claim_id].get("field_id") for claim_id in claim_ids if isinstance(claims[claim_id].get("field_id"), str)}
                claim_sources = {source_id for claim_id in claim_ids for source_id in ref_values(claims[claim_id], "source_ids")}
                if not set(candidate_ids).issubset(claim_candidates) or not set(field_ids).issubset(claim_fields) or not set(source_ids).issubset(claim_sources) or search_ids:
                    self.err(path, "gap-reference-mismatch", "secondary-only-evidence references must agree with its claims")

        for search_id, search in searches.items():
            search_status = search.get("status")
            expected_kind = {"blocked": "blocked-search", "failed": "failed-search"}.get(search_status) if isinstance(search_status, str) else None
            if expected_kind and not any(gap.get("kind") == expected_kind and contains_ref(gap, "search_ids", search_id) for gap in gaps.values()):
                self.err(f"/coverage/searches/{search_id}", "missing-gap", f"{search.get('status')} search needs {expected_kind} gap")
        for source_id, source in sources.items():
            if source.get("access_status") != "accessible" and not any(gap.get("kind") == "inaccessible-source" and contains_ref(gap, "source_ids", source_id) for gap in gaps.values()):
                self.err(f"/sources/{source_id}", "missing-gap", "inaccessible source needs inaccessible-source gap")

        actual_counts = {
            "discovered_records": len(discovery_records),
            "canonical_candidates": len(candidates),
            "merged_records": sum(record.get("resolution") == "merged" for record in discovery_records.values()),
            "included": sum(candidate.get("status") == "included" for candidate in candidates.values()),
            "excluded": sum(candidate.get("status") == "excluded" for candidate in candidates.values()),
            "unresolved_records": sum(record.get("resolution") == "unresolved" for record in discovery_records.values()),
        }
        counts = self.exact(
            coverage.get("counts") if isinstance(coverage, dict) else None,
            "/coverage/counts",
            {"discovered_records", "canonical_candidates", "merged_records", "included", "excluded", "unresolved_records"},
        )
        for key in ("discovered_records", "canonical_candidates", "merged_records", "included", "excluded", "unresolved_records"):
            value = counts.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                self.err(f"/coverage/counts/{key}", "invalid-count", "must be a non-negative integer, not boolean")
        if counts != actual_counts:
            self.err("/coverage/counts", "accounting-mismatch", f"must equal {actual_counts}")
        if actual_counts["discovered_records"] != actual_counts["canonical_candidates"] + actual_counts["merged_records"] + actual_counts["unresolved_records"]:
            self.err("/coverage/counts", "accounting-invariant", "discovered must equal canonical + merged + unresolved")

        stop = self.exact(coverage.get("stop_assessment") if isinstance(coverage, dict) else None, "/coverage/stop_assessment", {"met", "search_ids", "note"})
        if not isinstance(stop.get("met"), bool):
            self.err("/coverage/stop_assessment/met", "wrong-type", "must be boolean")
        self.nonempty_text(stop.get("note"), "/coverage/stop_assessment/note")
        stop_search_ids = self.refs(stop.get("search_ids"), set(searches), "/coverage/stop_assessment/search_ids", nonempty=True)
        if stop.get("met") is True:
            supporting = [searches[search_id] for search_id in stop_search_ids]
            if any(search.get("status") != "completed" for search in supporting):
                self.err("/coverage/stop_assessment/search_ids", "invalid-stop-evidence", "met assessment may cite only completed searches")
            supporting_times = [search.get("started_at") for search in supporting]
            if all(timestamp(value) for value in supporting_times):
                parsed_supporting_times = [datetime.fromisoformat(value.replace("Z", "+00:00")) for value in supporting_times]
                if parsed_supporting_times != sorted(parsed_supporting_times):
                    self.err("/coverage/stop_assessment/search_ids", "unordered-stop-evidence", "supporting searches must be chronological")
            completed_searches = sorted(
                [search for search in searches.values() if search.get("status") == "completed" and timestamp(search.get("started_at"))],
                key=lambda search: datetime.fromisoformat(search["started_at"].replace("Z", "+00:00")),
            )
            if completed_searches:
                expected_stop_ids = [search["id"] for search in completed_searches]
                if stop_search_ids != expected_stop_ids:
                    self.err("/coverage/stop_assessment/search_ids", "incomplete-stop-evidence", "met assessment must cite every completed search in chronological order")
                latest_completed = completed_searches[-1]
                if not supporting or supporting[-1].get("id") != latest_completed.get("id"):
                    self.err("/coverage/stop_assessment/search_ids", "stale-stop-evidence", "supporting sequence must end with the latest completed search")
            minimum_completed = stop_rule.get("minimum_completed_searches")
            if isinstance(minimum_completed, int) and not isinstance(minimum_completed, bool) and len(completed_searches) < minimum_completed:
                self.err("/coverage/stop_assessment/search_ids", "insufficient-stop-evidence", "fewer supporting searches than declared minimum")
            query_families = {normalize(search.get("query_family", "")) for search in completed_searches if isinstance(search.get("query_family"), str)}
            source_families = {normalize(search.get("source_family", "")) for search in completed_searches if isinstance(search.get("source_family"), str)}
            if not {normalize(value) for value in required_query_families}.issubset(query_families):
                self.err("/coverage/stop_assessment/search_ids", "missing-query-family", "supporting searches do not cover required query families")
            if not {normalize(value) for value in required_source_families}.issubset(source_families):
                self.err("/coverage/stop_assessment/search_ids", "missing-source-family", "supporting searches do not cover required source families")
            consecutive = stop_rule.get("minimum_consecutive_no_new_candidates")
            if isinstance(consecutive, int) and not isinstance(consecutive, bool):
                trailing = completed_searches[-consecutive:]
                if len(trailing) < consecutive or any(search.get("status") != "completed" or search.get("new_candidate_ids") for search in trailing):
                    self.err("/coverage/stop_assessment/search_ids", "no-saturation", "supporting sequence does not end with required no-new-candidate searches")

        summary = root.get("summary")
        if not isinstance(summary, dict):
            self.err("/summary", "wrong-type", "must be an object")
        elif summary.get("mode") == "neutral":
            self.exact(summary, "/summary", {"mode", "neutral_summary"})
            self.nonempty_text(summary.get("neutral_summary"), "/summary/neutral_summary")
        elif summary.get("mode") == "decision":
            self.exact(summary, "/summary", {"mode", "decision_question", "recommendation", "rationale_claim_ids"})
            self.nonempty_text(summary.get("decision_question"), "/summary/decision_question")
            self.nonempty_text(summary.get("recommendation"), "/summary/recommendation")
            self.refs(summary.get("rationale_claim_ids"), set(claims), "/summary/rationale_claim_ids", nonempty=True)
        else:
            self.exact(summary, "/summary", {"mode", "neutral_summary", "decision_question", "recommendation", "rationale_claim_ids"})
            self.err("/summary/mode", "invalid-value", "must be neutral or decision")

        return sorted(self.errors, key=lambda error: (error["path"], error["code"], error["message"]))


class DuplicateKeyError(ValueError):
    pass


def strict_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def reject_json_constant(value: str):
    raise ValueError(f"invalid JSON constant {value}")


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] in {"-h", "--help"}:
        print("usage: validate_landscape.py PATH/landscape.json")
        print("Validate a map-technical-landscapes/v2 artifact without contacting external systems.")
        return 0
    if len(argv) != 2:
        print(json.dumps({"valid": False, "errors": [{"path": "/", "code": "usage", "message": "usage: validate_landscape.py LANDSCAPE.json"}]}, sort_keys=True))
        return 2
    try:
        data = json.loads(
            Path(argv[1]).read_text(encoding="utf-8"),
            object_pairs_hook=strict_object_pairs,
            parse_constant=reject_json_constant,
        )
    except DuplicateKeyError as exc:
        print(json.dumps({"valid": False, "errors": [{"path": "/", "code": "duplicate-key", "message": str(exc)}]}, sort_keys=True))
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [{"path": "/", "code": "parse-error", "message": str(exc)}]}, sort_keys=True))
        return 2
    errors = Validator(data).validate()
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
