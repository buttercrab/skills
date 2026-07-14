#!/usr/bin/env python3
"""Validate a provenance-aware linked evidence brief using only local data."""

from __future__ import annotations

import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn
from urllib.parse import unquote


ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
PLACEHOLDER_LOCATORS = {
    "all",
    "entire document",
    "entire source",
    "n/a",
    "na",
    "unknown",
    "whole document",
    "whole source",
}
SIGNED_URL_RE = re.compile(
    r"(?:https?://[^/\s:@]+:[^@\s]+@|"
    r"(?:[?&#;]|%3[fF]|%26|%23)"
    r"(?:x-amz-signature|x-goog-signature|access[_-]?token|refresh[_-]?token|"
    r"id[_-]?token|client[_-]?secret|password|passwd|auth|credentials?|"
    r"token|sig|signature|api[_-]?key|private[_-]?key|secret[_-]?key)"
    r"(?:=|%3[dD])[^&#;\s]+)",
    re.I,
)
SECRET_RE = re.compile(
    r"(?:bearer\s+[A-Za-z0-9._~+/-]{12,}|"
    r"sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{16,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,})",
    re.I,
)
SENSITIVE_KEYS = {
    "access-token",
    "api-key",
    "apikey",
    "auth",
    "authorization",
    "client-secret",
    "cookie",
    "credential",
    "credentials",
    "id-token",
    "password",
    "passwd",
    "refresh-token",
    "secret",
    "secret-key",
    "set-cookie",
    "sig",
    "signature",
    "token",
    "private-key",
    "x-amz-signature",
    "x-goog-signature",
}
PRIVATE_CONTENT_KEYS = {
    "body",
    "content",
    "document",
    "html",
    "markdown",
    "message",
    "messages",
    "page-content",
    "payload",
    "private-content",
    "raw",
    "source-content",
    "text",
    "transcript",
}
REDACTED_VALUES = {"redacted", "<redacted>", "[redacted]", "***"}


class StrictJSONError(ValueError):
    """Raised when input uses ambiguous or non-standard JSON constructs."""


def reject_constant(value: str) -> NoReturn:
    raise StrictJSONError(f"non-finite number {value!r} is not valid JSON")


def parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise StrictJSONError(f"non-finite number {value!r} is not valid JSON")
    return parsed


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def parse_aware_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def aware_timestamp(value: object) -> bool:
    return parse_aware_timestamp(value) is not None


def normalized_key(value: object) -> str:
    if not isinstance(value, str):
        return ""
    with_word_breaks = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    return re.sub(r"[_\s]+", "-", with_word_breaks.casefold())


def meaningful_locator(value: str) -> bool:
    return bool(re.search(r"[A-Za-z0-9]", value))


def valid_locator(kind: str, value: str) -> bool:
    stripped = value.strip()
    if not stripped or stripped.casefold() in PLACEHOLDER_LOCATORS or not meaningful_locator(stripped):
        return False
    if kind == "page":
        match = re.fullmatch(r"(?:p(?:age)?\s*)?(\d+)(?:\s*-\s*(\d+))?", stripped, re.I)
        return bool(match and int(match.group(1)) > 0 and (match.group(2) is None or int(match.group(2)) >= int(match.group(1))))
    if kind == "line-range":
        match = re.fullmatch(r"L?(\d+)\s*-\s*L?(\d+)", stripped, re.I)
        return bool(match and int(match.group(1)) > 0 and int(match.group(2)) >= int(match.group(1)))
    if kind == "json-path":
        return bool(re.fullmatch(r"\$(?:(?:\.[A-Za-z_][A-Za-z0-9_-]*)|(?:\[(?:\d+|\"[^\"]+\"|'[^']+')\]))+", stripped))
    if kind == "table-cell":
        return bool(re.fullmatch(r"(?:[^!\s]+!)?[A-Z]+[1-9]\d*", stripped, re.I))
    if kind == "timestamp":
        if aware_timestamp(stripped):
            return True
        match = re.fullmatch(r"(?:(\d{1,2}):)?([0-5]?\d):([0-5]\d)(?:\.\d+)?", stripped)
        return bool(match)
    if kind == "custom":
        if not re.fullmatch(r"[a-z][a-z0-9-]{1,31}:.+", stripped):
            return False
        return meaningful_locator(stripped.split(":", 1)[1])
    return True


class Validator:
    def __init__(self, data: object):
        self.data = data
        self.errors: list[tuple[str, str, str]] = []

    def err(self, path: str, code: str, message: str) -> None:
        self.errors.append((path, code, message))

    def collection(self, key: str) -> tuple[list[dict], dict[str, dict]]:
        value = self.data.get(key) if isinstance(self.data, dict) else None
        if not isinstance(value, list):
            self.err(f"/{key}", "E012", "must be an array")
            return [], {}
        indexed: dict[str, dict] = {}
        clean: list[dict] = []
        for i, item in enumerate(value):
            p = f"/{key}/{i}"
            if not isinstance(item, dict):
                self.err(p, "E012", "must be an object")
                continue
            ident = item.get("id")
            if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
                self.err(f"{p}/id", "E014", "invalid lowercase-hyphen ID")
            elif ident in indexed:
                self.err(f"{p}/id", "E015", f"duplicate ID {ident!r}")
            else:
                indexed[ident] = item
            clean.append(item)
        return clean, indexed

    def refs(self, values: object, allowed: set[str], path: str, *, nonempty: bool = False) -> list[str]:
        if not isinstance(values, list):
            self.err(path, "E012", "must be an array")
            return []
        if nonempty and not values:
            self.err(path, "E010", "must not be empty")
        seen: set[str] = set()
        valid: list[str] = []
        for i, value in enumerate(values):
            if not isinstance(value, str):
                self.err(f"{path}/{i}", "E020", f"dangling reference {value!r}")
                continue
            if value in seen:
                self.err(f"{path}/{i}", "E033", f"duplicate reference {value!r}")
            seen.add(value)
            if value not in allowed:
                self.err(f"{path}/{i}", "E020", f"dangling reference {value!r}")
            else:
                valid.append(value)
        return valid

    def validate(self) -> list[tuple[str, str, str]]:
        if not isinstance(self.data, dict):
            self.err("/", "E012", "root must be an object")
            return self.errors
        required = {"schema_version", "question", "requested_resources", "sources", "answer", "facts", "inferences", "unknowns", "conflicts", "context_map", "actions", "decision"}
        for key in sorted(required - set(self.data)):
            self.err("/", "E010", f"missing field {key}")
        for key in sorted(set(self.data) - required):
            self.err(f"/{key}", "E011", "unknown top-level field")
        if self.data.get("schema_version") != "evidence-brief-v1":
            self.err("/schema_version", "E013", "must equal evidence-brief-v1")
        if not isinstance(self.data.get("question"), str) or not self.data.get("question", "").strip():
            self.err("/question", "E010", "question must be non-empty")

        def scan_secrets(value: object, path: str, *, in_receipt_details: bool = False) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    child_path = f"{path}/{key}"
                    child_in_details = in_receipt_details or child_path.endswith("/acquisition/receipt/details")
                    normalized = normalized_key(key)
                    if (normalized in SENSITIVE_KEYS and isinstance(child, str)
                            and child.strip().casefold() not in REDACTED_VALUES):
                        self.err(child_path, "E034", "secret-bearing field must be removed or explicitly redacted")
                    if child_in_details and normalized in PRIVATE_CONTENT_KEYS:
                        self.err(child_path, "E034", "receipt details must contain metadata, not source content")
                    scan_secrets(child, child_path, in_receipt_details=child_in_details)
            elif isinstance(value, list):
                for i, child in enumerate(value):
                    scan_secrets(child, f"{path}/{i}", in_receipt_details=in_receipt_details)
            elif isinstance(value, str):
                decoded = value
                for _ in range(2):
                    decoded = unquote(decoded)
                if SIGNED_URL_RE.search(decoded) or SECRET_RE.search(decoded):
                    self.err(path, "E034", "secret-bearing or signed locator/content is forbidden")
        scan_secrets(self.data, "")

        requested, requested_by_id = self.collection("requested_resources")
        sources, source_by_id = self.collection("sources")
        facts, fact_by_id = self.collection("facts")
        inferences, inference_by_id = self.collection("inferences")
        unknowns, unknown_by_id = self.collection("unknowns")
        conflicts, conflict_by_id = self.collection("conflicts")
        actions, action_by_id = self.collection("actions")

        collections = {
            "requested_resources": requested_by_id,
            "sources": source_by_id,
            "facts": fact_by_id,
            "inferences": inference_by_id,
            "unknowns": unknown_by_id,
            "conflicts": conflict_by_id,
            "actions": action_by_id,
        }
        owner_by_id: dict[str, str] = {}
        for collection_name, indexed in collections.items():
            for ident in indexed:
                previous = owner_by_id.get(ident)
                if previous is not None:
                    self.err(
                        f"/{collection_name}/{ident}",
                        "E015",
                        f"ID {ident!r} is already used in {previous}",
                    )
                else:
                    owner_by_id[ident] = collection_name

        if not requested:
            self.err("/requested_resources", "E010", "at least one requested resource is required")
        requested_sources: list[str] = []
        for i, item in enumerate(requested):
            p = f"/requested_resources/{i}"
            source_id = item.get("source_id")
            if not isinstance(source_id, str) or source_id not in source_by_id:
                self.err(f"{p}/source_id", "E020", f"unknown source {source_id!r}")
            else:
                requested_sources.append(source_id)
                if source_by_id[source_id].get("provenance_class") != "requested-resource":
                    self.err(f"{p}/source_id", "E021", "source is not a requested-resource")
            if not isinstance(item.get("input_locator"), str) or not item.get("input_locator", "").strip():
                self.err(f"{p}/input_locator", "E010", "input locator is required")
        expected_requested = {s["id"] for s in sources if s.get("provenance_class") == "requested-resource" and isinstance(s.get("id"), str)}
        if set(requested_sources) != expected_requested:
            self.err("/requested_resources", "E021", "every requested-resource source must have one or more input mappings")

        acquired: set[str] = set()
        for i, source in enumerate(sources):
            p = f"/sources/{i}"
            source_id = source.get("id")
            for key in ("title", "resource_locator"):
                if not isinstance(source.get(key), str) or not source.get(key, "").strip():
                    self.err(f"{p}/{key}", "E010", f"{key} must be non-empty")
            if source.get("provenance_class") not in {"requested-resource", "linked-primary-source", "external-corroboration"}:
                self.err(f"{p}/provenance_class", "E013", "invalid provenance class")
            if source.get("kind") not in {"web-page", "dashboard", "slack-thread", "calendar-event", "pdf", "paper", "github-resource", "other"}:
                self.err(f"{p}/kind", "E013", "invalid source kind")
            if source.get("mutability") not in {"mutable", "immutable", "unknown"}:
                self.err(f"{p}/mutability", "E013", "mutability must be mutable, immutable, or unknown")
            if source.get("authority") not in {"primary", "official", "secondary", "community", "unknown"}:
                self.err(f"{p}/authority", "E013", "invalid source authority")
            if source.get("access_scope") not in {"public", "private", "restricted", "unknown"}:
                self.err(f"{p}/access_scope", "E013", "invalid source access scope")
            version = source.get("version_context")
            if not isinstance(version, dict):
                self.err(f"{p}/version_context", "E012", "version_context must be an object")
                version = {}
            for timestamp_key in ("publication_at", "updated_at"):
                if timestamp_key in version and not aware_timestamp(version.get(timestamp_key)):
                    self.err(f"{p}/version_context/{timestamp_key}", "E016", "must be a timezone-aware timestamp")
            for text_key in ("version", "timezone", "commit_context"):
                if text_key in version and (not isinstance(version.get(text_key), str) or not version.get(text_key, "").strip()):
                    self.err(f"{p}/version_context/{text_key}", "E010", "must be a non-empty string")
            acquisition = source.get("acquisition")
            if not isinstance(acquisition, dict):
                self.err(f"{p}/acquisition", "E012", "must be an object")
                continue
            status = acquisition.get("status")
            if status == "acquired":
                if isinstance(source_id, str) and source_id in source_by_id:
                    acquired.add(source_id)
                receipt = acquisition.get("receipt")
                if not isinstance(acquisition.get("method"), str) or not acquisition.get("method", "").strip() or not isinstance(receipt, dict):
                    self.err(f"{p}/acquisition", "E031", "acquired source requires method and receipt")
                elif any(not isinstance(receipt.get(k), str) or not receipt.get(k, "").strip() for k in ("provider", "resource_id")) or not aware_timestamp(receipt.get("retrieved_at")) or not isinstance(receipt.get("details"), dict):
                    self.err(f"{p}/acquisition/receipt", "E031", "receipt requires provider, resource_id, and timezone-aware retrieved_at")
                if not aware_timestamp(version.get("observed_at")):
                    self.err(f"{p}/version_context/observed_at", "E016", "acquired source needs timezone-aware observed_at")
                if source.get("kind") == "github-resource" and not any(
                        isinstance(version.get(k), str) and version.get(k, "").strip()
                        for k in ("commit_context", "version", "updated_at")):
                    self.err(
                        f"{p}/version_context",
                        "E016",
                        "acquired github-resource needs commit_context, version, or updated_at",
                    )
            elif status in {"blocked", "failed", "not-attempted"}:
                reason = acquisition.get("reason")
                if (not isinstance(reason, dict)
                        or not isinstance(reason.get("code"), str)
                        or not reason.get("code", "").strip()
                        or not isinstance(reason.get("detail"), str)
                        or not reason.get("detail", "").strip()):
                    self.err(f"{p}/acquisition/reason", "E030", "non-acquired source requires reason code and detail")
            else:
                self.err(f"{p}/acquisition/status", "E013", "invalid acquisition status")

        fact_sources: dict[str, set[str]] = {}
        by_assertion: dict[str, list[str]] = {}
        for i, fact in enumerate(facts):
            p = f"/facts/{i}"
            if not isinstance(fact.get("claim"), str) or not fact.get("claim", "").strip():
                self.err(f"{p}/claim", "E010", "fact claim must be non-empty")
            key = fact.get("assertion_key")
            if not isinstance(key, str) or not key.strip():
                self.err(f"{p}/assertion_key", "E010", "assertion_key is required")
            elif isinstance(fact.get("id"), str) and fact.get("id") in fact_by_id:
                by_assertion.setdefault(key, []).append(fact["id"])
            if "value" not in fact:
                self.err(f"{p}/value", "E010", "fact value field is required")
            elif isinstance(fact.get("value"), (dict, list)):
                self.err(f"{p}/value", "E012", "fact value must be a JSON scalar")
            elif isinstance(fact.get("value"), float) and not math.isfinite(fact["value"]):
                self.err(f"{p}/value", "E012", "fact value must be finite")
            citations = fact.get("citations")
            if not isinstance(citations, list) or not citations:
                self.err(f"{p}/citations", "E010", "fact needs at least one citation")
                continue
            fact_id = fact.get("id")
            if isinstance(fact_id, str) and fact_id in fact_by_id:
                fact_sources[fact_id] = set()
            for j, citation in enumerate(citations):
                cp = f"{p}/citations/{j}"
                if not isinstance(citation, dict):
                    self.err(cp, "E012", "citation must be an object")
                    continue
                source_id = citation.get("source_id")
                if not isinstance(source_id, str) or source_id not in source_by_id:
                    self.err(f"{cp}/source_id", "E020", f"unknown source {source_id!r}")
                elif source_id not in acquired:
                    self.err(f"{cp}/source_id", "E022", f"source {source_id!r} is not acquired")
                elif isinstance(fact_id, str) and fact_id in fact_sources:
                    fact_sources[fact_id].add(source_id)
                locator = citation.get("locator")
                allowed_kinds = {"section", "page", "line-range", "message", "event-field", "table-cell", "json-path", "timestamp", "anchor", "custom"}
                if (not isinstance(locator, dict)
                        or locator.get("kind") not in allowed_kinds
                        or not isinstance(locator.get("value"), str)
                        or not valid_locator(locator.get("kind"), locator.get("value"))):
                    self.err(f"{cp}/locator", "E023", "citation needs a specific structured locator")

        for i, inference in enumerate(inferences):
            for key in ("statement", "reasoning"):
                if not isinstance(inference.get(key), str) or not inference.get(key, "").strip():
                    self.err(f"/inferences/{i}/{key}", "E010", f"{key} must be non-empty")
            if inference.get("confidence") not in {"high", "medium", "low"}:
                self.err(f"/inferences/{i}/confidence", "E013", "confidence must be high, medium, or low")
            refs = self.refs(inference.get("based_on_fact_ids"), set(fact_by_id), f"/inferences/{i}/based_on_fact_ids", nonempty=True)
            if not refs:
                self.err(f"/inferences/{i}", "E024", "inference lacks valid fact basis")
            if "citations" in inference:
                self.err(f"/inferences/{i}/citations", "E011", "inferences must not cite sources directly")

        for i, unknown in enumerate(unknowns):
            for key in ("question", "reason"):
                if not isinstance(unknown.get(key), str) or not unknown.get(key, "").strip():
                    self.err(f"/unknowns/{i}/{key}", "E010", f"{key} must be non-empty")
            srefs = self.refs(unknown.get("related_source_ids", []), set(source_by_id), f"/unknowns/{i}/related_source_ids")
            frefs = self.refs(unknown.get("related_fact_ids", []), set(fact_by_id), f"/unknowns/{i}/related_fact_ids")
            if not srefs and not frefs:
                self.err(f"/unknowns/{i}", "E010", "unknown needs a related source or fact")

        covered_conflicts: set[frozenset[str]] = set()
        for i, conflict in enumerate(conflicts):
            p = f"/conflicts/{i}"
            if not isinstance(conflict.get("explanation"), str) or not conflict.get("explanation", "").strip():
                self.err(f"{p}/explanation", "E010", "conflict explanation must be non-empty")
            fids = self.refs(conflict.get("fact_ids"), set(fact_by_id), f"{p}/fact_ids", nonempty=True)
            values = {json.dumps(fact_by_id[f].get("value"), sort_keys=True) for f in fids}
            keys = {fact_by_id[f].get("assertion_key") for f in fids}
            source_ids = set().union(*(fact_sources.get(f, set()) for f in fids))
            if len(fids) < 2 or len(values) < 2 or len(keys) != 1 or len(source_ids) < 2:
                self.err(p, "E025", "conflict needs two differing facts for one assertion from two sources")
            else:
                covered_conflicts.add(frozenset(fids))
            status = conflict.get("status")
            if status not in {"resolved", "unresolved"}:
                self.err(f"{p}/status", "E013", "invalid conflict status")
            if status == "resolved" and (not isinstance(conflict.get("resolution"), str) or not conflict.get("resolution", "").strip() or "resolved_value" not in conflict):
                self.err(p, "E032", "resolved conflict needs resolution and resolved_value")
            elif status == "resolved":
                resolved_value = conflict.get("resolved_value")
                if isinstance(resolved_value, (dict, list)) or (isinstance(resolved_value, float) and not math.isfinite(resolved_value)):
                    self.err(f"{p}/resolved_value", "E012", "resolved_value must be a finite JSON scalar")
        for assertion, fids in by_assertion.items():
            values = {json.dumps(fact_by_id[f].get("value"), sort_keys=True) for f in fids if f in fact_by_id}
            if len(values) > 1 and not any(set(fids).issubset(group) for group in covered_conflicts):
                self.err("/conflicts", "E025", f"differing values for {assertion!r} lack a conflict")

        context = self.data.get("context_map")
        if not isinstance(context, list):
            self.err("/context_map", "E012", "must be an array")
        elif len(sources) > 1 and not context:
            self.err("/context_map", "E026", "multiple sources require a context map")
        else:
            for i, edge in enumerate(context):
                p = f"/context_map/{i}"
                if not isinstance(edge, dict):
                    self.err(p, "E012", "must be an object")
                    continue
                left, right = edge.get("from_source_id"), edge.get("to_source_id")
                if (not isinstance(left, str)
                        or not isinstance(right, str)
                        or left not in source_by_id
                        or right not in source_by_id
                        or left == right):
                    self.err(p, "E020", "context edge needs two distinct valid sources")
                if edge.get("relationship") not in {"links-to", "attaches", "corroborates", "contradicts", "updates", "context-for", "same-event"}:
                    self.err(f"{p}/relationship", "E013", "invalid relationship")

        answer = self.data.get("answer")
        if not isinstance(answer, dict):
            self.err("/answer", "E012", "must be an object")
        else:
            fids = self.refs(answer.get("fact_ids"), set(fact_by_id), "/answer/fact_ids")
            uids = self.refs(answer.get("unknown_ids"), set(unknown_by_id), "/answer/unknown_ids")
            status = answer.get("status")
            has_facts = bool(fact_by_id)
            has_unknowns = bool(unknown_by_id)
            valid = ((status == "answered" and bool(fids) and has_facts and not has_unknowns and not uids) or
                     (status == "partial" and bool(fids) and bool(uids) and has_facts and has_unknowns) or
                     (status == "insufficient-evidence" and not fids and bool(uids) and not has_facts and has_unknowns))
            if not valid:
                self.err("/answer", "E027", "answer support is inconsistent with status")

        for i, action in enumerate(actions):
            p = f"/actions/{i}"
            status = action.get("status")
            for key in ("operation", "resource_id"):
                if not isinstance(action.get(key), str) or not action.get(key, "").strip():
                    self.err(f"{p}/{key}", "E010", f"action {key} must be non-empty")
            if status not in {"proposed", "authorized", "completed", "failed", "cancelled"}:
                self.err(f"{p}/status", "E013", "invalid action status")
            authorization_time: datetime | None = None
            if status in {"authorized", "completed", "failed"}:
                authorization = action.get("authorization")
                source = authorization.get("source") if isinstance(authorization, dict) else None
                if (not isinstance(authorization, dict)
                        or not isinstance(source, dict)
                        or source.get("kind") not in {"user-message", "user-request"}
                        or not isinstance(source.get("resource_id"), str)
                        or not source.get("resource_id", "").strip()
                        or any(not isinstance(authorization.get(k), str) or not authorization.get(k, "").strip() for k in ("scope", "operation", "resource_id"))
                        or not aware_timestamp(authorization.get("authorized_at"))):
                    self.err(f"{p}/authorization", "E029", "action requires scoped authorization with source, operation, and timestamp")
                elif authorization.get("operation") != action.get("operation") or authorization.get("resource_id") != action.get("resource_id"):
                    self.err(f"{p}/authorization", "E029", "authorization operation and resource must match the action")
                else:
                    authorization_time = parse_aware_timestamp(authorization.get("authorized_at"))
            if status == "completed":
                receipt = action.get("receipt")
                if not isinstance(receipt, dict) or any(not isinstance(receipt.get(k), str) or not receipt.get(k, "").strip() for k in ("provider", "receipt_id", "operation", "resource_id")) or not aware_timestamp(receipt.get("completed_at")):
                    self.err(f"{p}/receipt", "E028", "completed action requires a valid receipt")
                elif receipt.get("operation") != action.get("operation") or receipt.get("resource_id") != action.get("resource_id"):
                    self.err(f"{p}/receipt", "E028", "receipt operation and resource must match the action")
                elif authorization_time is not None:
                    completion_time = parse_aware_timestamp(receipt.get("completed_at"))
                    if completion_time is not None and completion_time < authorization_time:
                        self.err(f"{p}/receipt/completed_at", "E028", "completion cannot precede authorization")
            if status == "proposed" and action.get("receipt") is not None:
                self.err(f"{p}/receipt", "E013", "proposed action must not have a receipt")

        decision = self.data.get("decision")
        if decision is not None:
            if not isinstance(decision, dict) or not isinstance(decision.get("recommendation"), str) or not decision.get("recommendation", "").strip():
                self.err("/decision", "E012", "decision must contain a recommendation")
            else:
                basis = decision.get("basis_ids")
                self.refs(basis, set(fact_by_id) | set(inference_by_id), "/decision/basis_ids", nonempty=True)
                self.refs(decision.get("next_action_ids", []), set(action_by_id), "/decision/next_action_ids")

        return sorted(self.errors)


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] in {"-h", "--help"}:
        print("usage: validate_evidence_brief.py PATH/evidence-brief.json")
        print("Validate an evidence-brief-v1 artifact without contacting external systems.")
        return 0
    if len(argv) != 2:
        print("usage: validate_evidence_brief.py PATH/evidence-brief.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(
            Path(argv[1]).read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
            parse_float=parse_finite_float,
        )
    except OSError as exc:
        print(f"unreadable: {exc}", file=sys.stderr)
        return 2
    except (UnicodeError, json.JSONDecodeError, StrictJSONError, RecursionError) as exc:
        print(f"E001 /: invalid JSON: {exc}", file=sys.stderr)
        return 1
    try:
        errors = Validator(data).validate()
    except RecursionError as exc:
        print(f"E001 /: invalid JSON nesting: {exc}", file=sys.stderr)
        return 1
    if errors:
        for path, code, message in errors:
            print(f"{code} {path}: {message}", file=sys.stderr)
        print(f"INVALID {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"VALID evidence-brief-v1 {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
