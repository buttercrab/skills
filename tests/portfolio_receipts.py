#!/usr/bin/env python3
"""Canonical manifests and strict portfolio gate/trial/evaluation receipts."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import uuid


MANIFEST_VERSION = "portfolio-source-manifest/v1"
AMBIENT_PROFILE_VERSION = "portfolio-ambient-watch-profile/v1"
REQUIRED_AMBIENT_CATEGORIES = {
    "python",
    "go",
    "cargo",
    "postgresql",
    "installer",
    "shell-config",
    "network-policy",
}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
COMMON_FIELDS = {
    "receipt_type",
    "schema_version",
    "receipt_id",
    "packet_id",
    "packet_revision",
    "protected_digest",
    "repository_root",
    "manifest_algorithm_version",
    "timestamp",
}
GATE_BASE_FIELDS = COMMON_FIELDS | {
    "gate_id",
    "profile",
    "artifact_manifest_digest",
    "approver_evidence",
    "scope",
}
TRIAL_FIELDS = COMMON_FIELDS | {
    "trial_component_id",
    "trial_component_digest",
    "source_digest",
    "package_manifest_digest",
    "routing_case_digest",
    "prompt_digest",
    "output_schema_digest",
    "isolation_digest",
    "runner_digest",
    "runner_schema_version",
    "command_policy_digest",
    "retry_policy_digest",
    "status_policy_digest",
    "tool_policy_digest",
    "data_policy_digest",
    "network_policy_digest",
    "mutation_policy_digest",
    "model",
    "reasoning_effort",
    "trial_id",
    "case_id",
    "run_ordinal",
    "local_run_id",
    "provider_thread_id",
    "fresh_session_marker",
    "attempt_number",
    "automatic_retry",
    "run_manifest_digest",
    "event_stream_digest",
    "raw_batch_output_hash",
    "raw_output_hash",
    "pre_state_digest",
    "post_state_digest",
}
EVALUATION_FIELDS = COMMON_FIELDS | {
    "evaluation_component_id",
    "evaluation_component_digest",
    "trial_receipt_id",
    "trial_receipt_hash",
    "evaluator_id",
    "case_id",
    "run_ordinal",
    "source_digest",
    "prompt_digest",
    "output_schema_digest",
    "isolation_digest",
    "runner_digest",
    "runner_schema_version",
    "command_policy_digest",
    "retry_policy_digest",
    "status_policy_digest",
    "tool_policy_digest",
    "data_policy_digest",
    "network_policy_digest",
    "mutation_policy_digest",
    "model",
    "reasoning_effort",
    "local_run_id",
    "provider_thread_id",
    "fresh_session_marker",
    "attempt_number",
    "automatic_retry",
    "run_manifest_digest",
    "event_stream_digest",
    "raw_batch_output_hash",
    "raw_output_hash",
    "pre_state_digest",
    "post_state_digest",
    "rubric_keys",
    "rubric_digest",
    "dispositions",
}

RUN_HASH_FIELDS = {
    "prompt_digest",
    "output_schema_digest",
    "isolation_digest",
    "runner_digest",
    "command_policy_digest",
    "retry_policy_digest",
    "status_policy_digest",
    "tool_policy_digest",
    "data_policy_digest",
    "network_policy_digest",
    "mutation_policy_digest",
    "run_manifest_digest",
    "event_stream_digest",
    "raw_batch_output_hash",
    "raw_output_hash",
    "pre_state_digest",
    "post_state_digest",
}
RUN_TEXT_FIELDS = {"runner_schema_version", "model", "reasoning_effort", "case_id"}
RUN_UUID_FIELDS = {"local_run_id", "provider_thread_id", "fresh_session_marker"}
TRIAL_INPUT_FIELDS = {
    "source_digest",
    "package_manifest_digest",
    "routing_case_digest",
    *RUN_HASH_FIELDS,
    *RUN_TEXT_FIELDS,
    *RUN_UUID_FIELDS,
    "run_ordinal",
    "attempt_number",
    "automatic_retry",
}
EVALUATION_INPUT_FIELDS = {
    "source_digest",
    *RUN_HASH_FIELDS,
    *RUN_TEXT_FIELDS,
    *RUN_UUID_FIELDS,
    "run_ordinal",
    "attempt_number",
    "automatic_retry",
    "rubric_digest",
    "rubric_keys",
}


class ContractError(ValueError):
    pass


def _reject_constant(value: str) -> None:
    raise ContractError(f"non-finite JSON number is forbidden: {value}")


def _pairs(items: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in items:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_load(path: Path) -> dict:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("JSON root must be an object")
    return value


def canonical_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"value is not canonical JSON: {exc}") from exc


def digest_value(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _relative_path(value: str) -> str:
    if "\x00" in value:
        raise ContractError("path contains NUL")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ContractError(f"path must be normalized repository-relative POSIX text: {value!r}")
    normalized = path.as_posix()
    if normalized != value:
        raise ContractError(f"path is not normalized: {value!r}")
    return normalized


def _root(value: str | Path) -> Path:
    raw = Path(value).expanduser().absolute()
    if raw.is_symlink():
        raise ContractError(f"repository root must not be a symlink: {raw}")
    try:
        root = raw.resolve(strict=True)
    except OSError as exc:
        raise ContractError(f"repository root is unavailable: {raw}") from exc
    if not root.is_dir():
        raise ContractError(f"repository root is not a directory: {root}")
    return root


def _reject_symlink_parents(root: Path, relative: str) -> Path:
    current = root
    parts = PurePosixPath(relative).parts
    for part in parts[:-1]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(info.st_mode):
            raise ContractError(f"intermediate path is a symlink: {current}")
        if not stat.S_ISDIR(info.st_mode):
            raise ContractError(f"intermediate path is not a directory: {current}")
    return root.joinpath(*parts)


def manifest_entry(root: Path, relative: str) -> dict:
    relative = _relative_path(relative)
    path = _reject_symlink_parents(root, relative)
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"path": relative, "type": "absent"}
    mode = f"{stat.S_IMODE(info.st_mode):04o}"
    if stat.S_ISREG(info.st_mode):
        return {
            "path": relative,
            "type": "regular",
            "mode": mode,
            "sha256": digest_file(path),
            "size": info.st_size,
            "nlink": info.st_nlink,
        }
    if stat.S_ISLNK(info.st_mode):
        target = os.fsencode(os.readlink(path))
        return {
            "path": relative,
            "type": "symlink",
            "mode": mode,
            "sha256": hashlib.sha256(target).hexdigest(),
            "size": len(target),
        }
    raise ContractError(f"manifest inputs must be regular files, symlinks, or absent: {relative}")


def build_manifest(root_value: str | Path, paths: list[str]) -> dict:
    root = _root(root_value)
    normalized = [_relative_path(item) for item in paths]
    if not normalized or len(normalized) != len(set(normalized)):
        raise ContractError("manifest paths must be nonempty and unique")
    entries = [manifest_entry(root, item) for item in sorted(normalized, key=lambda item: item.encode("utf-8"))]
    return {
        "schema_version": MANIFEST_VERSION,
        "repository_root": str(root),
        "entries": entries,
    }


def tree_manifest(path_value: str | Path, excluded_names: set[str] | None = None) -> dict:
    path = Path(path_value).expanduser().absolute()
    excluded = excluded_names or set()
    if not path.exists() and not path.is_symlink():
        return {"root": str(path), "type": "absent", "entries": []}
    if path.is_symlink():
        target = os.fsencode(os.readlink(path))
        return {
            "root": str(path),
            "type": "symlink",
            "entries": [{"path": ".", "type": "symlink", "sha256": hashlib.sha256(target).hexdigest()}],
        }
    if path.is_file():
        info = path.lstat()
        return {
            "root": str(path),
            "type": "regular",
            "entries": [
                {
                    "path": ".",
                    "type": "regular",
                    "mode": f"{stat.S_IMODE(info.st_mode):04o}",
                    "sha256": digest_file(path),
                    "size": info.st_size,
                }
            ],
        }
    if not path.is_dir():
        raise ContractError(f"snapshot root must be a file, symlink, directory, or absent: {path}")
    entries: list[dict] = []
    for current, directories, files in os.walk(path, topdown=True, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(
            [name for name in directories if name not in excluded],
            key=lambda item: os.fsencode(item),
        )
        names = sorted(directories + files, key=lambda item: os.fsencode(item))
        for name in names:
            child = current_path / name
            relative = child.relative_to(path).as_posix()
            info = child.lstat()
            mode = f"{stat.S_IMODE(info.st_mode):04o}"
            if stat.S_ISLNK(info.st_mode):
                target = os.fsencode(os.readlink(child))
                entries.append(
                    {
                        "path": relative,
                        "type": "symlink",
                        "mode": mode,
                        "sha256": hashlib.sha256(target).hexdigest(),
                    }
                )
            elif stat.S_ISREG(info.st_mode):
                entries.append(
                    {
                        "path": relative,
                        "type": "regular",
                        "mode": mode,
                        "sha256": digest_file(child),
                        "size": info.st_size,
                    }
                )
            elif stat.S_ISDIR(info.st_mode):
                entries.append({"path": relative, "type": "directory", "mode": mode})
            else:
                entries.append({"path": relative, "type": "special", "mode": mode})
    return {"root": str(path), "type": "directory", "entries": entries}


def state_snapshot(repo: str | Path, watches: list[str]) -> dict:
    repository = tree_manifest(repo, excluded_names={".git", ".planning"})
    watched = [tree_manifest(path) for path in watches]
    return {
        "schema_version": "portfolio-state-snapshot/v1",
        "repository": {"root": repository["root"], "digest": digest_value(repository)},
        "watched": [
            {"root": item["root"], "digest": digest_value(item)}
            for item in watched
        ],
    }


def resolve_ambient_watch_profile(
    profile_path: Path,
    *,
    repo: str | Path,
    host_home: str | Path,
    host_tmpdir: str | Path,
) -> list[str]:
    profile = strict_load(profile_path)
    _exact_keys(profile, {"schema_version", "required_categories", "entries"})
    if profile["schema_version"] != AMBIENT_PROFILE_VERSION:
        raise ContractError("unsupported ambient watch profile")
    categories = profile["required_categories"]
    if not isinstance(categories, list) or set(categories) != REQUIRED_AMBIENT_CATEGORIES or len(categories) != len(set(categories)):
        raise ContractError("ambient watch profile must name every required category exactly once")
    entries = profile["entries"]
    if not isinstance(entries, list) or not entries:
        raise ContractError("ambient watch profile entries must be nonempty")
    bases = {
        "repo": Path(repo).expanduser().absolute(),
        "home": Path(host_home).expanduser().absolute(),
        "tmp": Path(host_tmpdir).expanduser().absolute(),
    }
    observed_categories: set[str] = set()
    resolved: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ContractError("ambient watch entry must be an object")
        _exact_keys(entry, {"category", "base", "path"})
        category = entry["category"]
        base = entry["base"]
        value = entry["path"]
        if category not in REQUIRED_AMBIENT_CATEGORIES:
            raise ContractError(f"unknown ambient watch category: {category}")
        if base not in {"repo", "home", "tmp", "absolute"}:
            raise ContractError(f"unknown ambient watch base: {base}")
        if not isinstance(value, str) or not value or "\x00" in value or "\n" in value or "\r" in value:
            raise ContractError("ambient watch path must be nonempty single-line text")
        path = Path(value)
        if base == "absolute":
            if not path.is_absolute():
                raise ContractError("absolute ambient watch path must be absolute")
            target = path
        else:
            if path.is_absolute() or any(part in {"", ".", ".."} for part in PurePosixPath(value).parts):
                raise ContractError("relative ambient watch path must be normalized and traversal-free")
            target = bases[base].joinpath(*PurePosixPath(value).parts)
        observed_categories.add(category)
        resolved.append(str(target.absolute()))
    if observed_categories != REQUIRED_AMBIENT_CATEGORIES:
        raise ContractError("ambient watch entries do not cover every required category")
    if len(resolved) != len(set(resolved)):
        raise ContractError("ambient watch paths must resolve uniquely")
    return resolved


def _exact_keys(value: dict, expected: set[str]) -> None:
    actual = set(value)
    if actual != expected:
        raise ContractError(
            f"closed object fields differ; missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
        )


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{field} must be nonempty text")
    return value


def _hash(value: object, field: str) -> str:
    text = _text(value, field)
    if not HASH_RE.fullmatch(text):
        raise ContractError(f"{field} must be lowercase SHA-256")
    return text


def _uuid(value: object, field: str) -> str:
    text = _text(value, field)
    try:
        parsed = str(uuid.UUID(text))
    except ValueError as exc:
        raise ContractError(f"{field} must be a UUID") from exc
    if parsed != text:
        raise ContractError(f"{field} must use canonical lowercase UUID text")
    return text


def _timestamp(value: object) -> str:
    text = _text(value, "timestamp")
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("timestamp must be RFC3339") from exc
    if parsed.tzinfo is None:
        raise ContractError("timestamp needs a timezone")
    return text


def _common(value: dict, receipt_type: str) -> None:
    if value.get("receipt_type") != receipt_type:
        raise ContractError(f"receipt_type must be {receipt_type}")
    if value.get("schema_version") != 1 or isinstance(value.get("schema_version"), bool):
        raise ContractError("schema_version must be integer 1")
    _uuid(value.get("receipt_id"), "receipt_id")
    _uuid(value.get("packet_id"), "packet_id")
    revision = value.get("packet_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise ContractError("packet_revision must be a positive integer")
    _hash(value.get("protected_digest"), "protected_digest")
    root = Path(_text(value.get("repository_root"), "repository_root"))
    if not root.is_absolute() or ".." in root.parts:
        raise ContractError("repository_root must be absolute normalized text")
    if value.get("manifest_algorithm_version") != MANIFEST_VERSION:
        raise ContractError(f"manifest_algorithm_version must be {MANIFEST_VERSION}")
    _timestamp(value.get("timestamp"))


def _component(value: object, field: str) -> dict:
    if not isinstance(value, dict):
        raise ContractError(f"{field} must be an object")
    _exact_keys(value, {"id", "digest"})
    _uuid(value.get("id"), f"{field}.id")
    _hash(value.get("digest"), f"{field}.digest")
    return value


def validate_gate(value: dict) -> None:
    gate = value.get("gate_id")
    if gate == "A":
        optional = {key for key in ("authorized_delta_digest", "expected_postimage_digest") if key in value}
        if len(optional) != 1:
            raise ContractError("Gate A requires exactly one delta or expected-postimage digest")
        _exact_keys(value, GATE_BASE_FIELDS | optional)
        if value.get("profile") != "authorized-delta":
            raise ContractError("Gate A profile must be authorized-delta")
        _hash(value[next(iter(optional))], next(iter(optional)))
    elif gate == "B":
        _exact_keys(value, GATE_BASE_FIELDS)
        if value.get("profile") != "immutable-specification":
            raise ContractError("Gate B profile must be immutable-specification")
    elif gate == "C":
        _exact_keys(value, GATE_BASE_FIELDS | {"trial_component", "evaluation_component"})
        if value.get("profile") != "immutable-evaluation-snapshot":
            raise ContractError("Gate C profile must be immutable-evaluation-snapshot")
        trial = _component(value.get("trial_component"), "trial_component")
        evaluation = _component(value.get("evaluation_component"), "evaluation_component")
        if trial["id"] == evaluation["id"]:
            raise ContractError("Gate C component IDs must be distinct")
    else:
        raise ContractError("gate_id must be A, B, or C")
    _common(value, "gate-approval/v1")
    _hash(value.get("artifact_manifest_digest"), "artifact_manifest_digest")
    _text(value.get("approver_evidence"), "approver_evidence")
    scope = value.get("scope")
    if not isinstance(scope, list) or not scope or len(scope) != len(set(scope)):
        raise ContractError("scope must be a nonempty unique list")
    for item in scope:
        _text(item, "scope item")


def _run_binding(value: dict) -> None:
    for field in sorted(RUN_HASH_FIELDS):
        _hash(value.get(field), field)
    for field in sorted(RUN_TEXT_FIELDS):
        _text(value.get(field), field)
    identities = [_uuid(value.get(field), field) for field in sorted(RUN_UUID_FIELDS)]
    if len(identities) != len(set(identities)):
        raise ContractError("local run, provider thread, and fresh-session identities must be distinct")
    ordinal = value.get("run_ordinal")
    if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal not in {1, 2, 3}:
        raise ContractError("run_ordinal must be integer 1, 2, or 3")
    if value.get("attempt_number") != 1 or isinstance(value.get("attempt_number"), bool):
        raise ContractError("attempt_number must be integer 1")
    if value.get("automatic_retry") is not False:
        raise ContractError("automatic_retry must be false")
    if value.get("pre_state_digest") != value.get("post_state_digest"):
        raise ContractError("run mutated bound source state")


def validate_trial(value: dict, gate: dict | None = None) -> None:
    _exact_keys(value, TRIAL_FIELDS)
    _common(value, "trial-receipt/v1")
    for field in ("trial_component_id", "trial_id"):
        _uuid(value.get(field), field)
    for field in ("trial_component_digest", "source_digest", "package_manifest_digest", "routing_case_digest"):
        _hash(value.get(field), field)
    _run_binding(value)
    if value["trial_id"] in {value[field] for field in RUN_UUID_FIELDS}:
        raise ContractError("trial identity collides with run/session identity")
    if gate is not None:
        validate_gate(gate)
        if gate["gate_id"] != "C":
            raise ContractError("trial receipt requires a Gate C approval")
        component = gate["trial_component"]
        if value["trial_component_id"] != component["id"] or value["trial_component_digest"] != component["digest"]:
            raise ContractError("trial receipt does not match the approved trial component")
        _same_packet(value, gate)


def validate_evaluation(value: dict, trial: dict | None = None, gate: dict | None = None) -> None:
    _exact_keys(value, EVALUATION_FIELDS)
    _common(value, "evaluation-receipt/v1")
    for field in ("evaluation_component_id", "trial_receipt_id", "evaluator_id"):
        _uuid(value.get(field), field)
    for field in ("evaluation_component_digest", "trial_receipt_hash", "source_digest", "rubric_digest"):
        _hash(value.get(field), field)
    _run_binding(value)
    if value["evaluator_id"] in {value[field] for field in RUN_UUID_FIELDS}:
        raise ContractError("evaluator identity collides with run/session identity")
    dispositions = value.get("dispositions")
    if not isinstance(dispositions, list) or not dispositions:
        raise ContractError("dispositions must be a nonempty list")
    keys: list[str] = []
    for index, item in enumerate(dispositions):
        if not isinstance(item, dict):
            raise ContractError(f"dispositions[{index}] must be an object")
        _exact_keys(item, {"rubric_key", "verdict", "evidence"})
        keys.append(_text(item.get("rubric_key"), "rubric_key"))
        if item.get("verdict") not in {"pass", "fail"}:
            raise ContractError("verdict must be pass or fail")
        _text(item.get("evidence"), "evidence")
    if len(keys) != len(set(keys)):
        raise ContractError("rubric keys must be unique")
    rubric_keys = value.get("rubric_keys")
    if (
        not isinstance(rubric_keys, list)
        or not rubric_keys
        or len(rubric_keys) != len(set(rubric_keys))
        or any(not isinstance(item, str) or not item for item in rubric_keys)
    ):
        raise ContractError("rubric_keys must be a nonempty unique text list")
    if rubric_keys != keys:
        raise ContractError("rubric_keys must exactly match disposition order")
    if trial is not None:
        validate_trial(trial)
        if value["trial_receipt_id"] != trial["receipt_id"]:
            raise ContractError("evaluation references the wrong trial receipt")
        if value["trial_receipt_hash"] != digest_value(trial):
            raise ContractError("evaluation trial_receipt_hash is stale or altered")
        if value["evaluator_id"] == trial["trial_id"]:
            raise ContractError("evaluator identity must differ from trial identity")
        if value["case_id"] != trial["case_id"] or value["run_ordinal"] != trial["run_ordinal"]:
            raise ContractError("evaluation is cross-wired to the wrong trial case or run")
        for field in RUN_UUID_FIELDS:
            if value[field] == trial[field]:
                raise ContractError(f"evaluation reuses trial {field}")
        _same_packet(value, trial)
    if gate is not None:
        validate_gate(gate)
        if gate["gate_id"] != "C":
            raise ContractError("evaluation receipt requires a Gate C approval")
        if trial is not None:
            validate_trial(trial, gate=gate)
        component = gate["evaluation_component"]
        if value["evaluation_component_id"] != component["id"] or value["evaluation_component_digest"] != component["digest"]:
            raise ContractError("evaluation receipt does not match the approved evaluation component")
        _same_packet(value, gate)


def validate_trial_inputs(value: dict, expected: dict) -> None:
    """Bind a trial receipt to the immutable inputs and captured raw output."""
    _exact_keys(expected, TRIAL_INPUT_FIELDS)
    mismatched = [field for field in sorted(TRIAL_INPUT_FIELDS) if value.get(field) != expected.get(field)]
    if mismatched:
        raise ContractError(f"trial input binding mismatch: {mismatched}")


def validate_evaluation_inputs(value: dict, expected: dict) -> None:
    """Bind an evaluation receipt to the approved evaluator-only policy."""
    _exact_keys(expected, EVALUATION_INPUT_FIELDS)
    mismatched = [field for field in sorted(EVALUATION_INPUT_FIELDS) if value.get(field) != expected.get(field)]
    if mismatched:
        raise ContractError(f"evaluation input binding mismatch: {mismatched}")


def validate_receipt_batch(
    trials: list[dict],
    evaluations: list[dict],
    *,
    gate: dict,
) -> None:
    """Prove three fresh trial runs and three fresh evaluator runs without replay or cross-wiring."""
    trial_by_receipt: dict[str, dict] = {}
    trial_ids: set[str] = set()
    all_receipt_ids: set[str] = set()
    trial_runs: dict[int, dict] = {}
    trial_cases: dict[int, set[str]] = {}
    run_binding_fields = {
        "source_digest",
        "local_run_id",
        "provider_thread_id",
        "fresh_session_marker",
        "run_manifest_digest",
        "event_stream_digest",
        "raw_batch_output_hash",
        "prompt_digest",
        "output_schema_digest",
        "runner_digest",
        "runner_schema_version",
        "command_policy_digest",
        "retry_policy_digest",
        "status_policy_digest",
        "tool_policy_digest",
        "data_policy_digest",
        "network_policy_digest",
        "mutation_policy_digest",
        "model",
        "reasoning_effort",
        "pre_state_digest",
        "post_state_digest",
    }
    for trial in trials:
        validate_trial(trial, gate=gate)
        receipt_id = trial["receipt_id"]
        if receipt_id in all_receipt_ids or trial["trial_id"] in trial_ids:
            raise ContractError("reused trial receipt or trial identity")
        all_receipt_ids.add(receipt_id)
        trial_ids.add(trial["trial_id"])
        trial_by_receipt[receipt_id] = trial
        ordinal = trial["run_ordinal"]
        binding = {field: trial[field] for field in run_binding_fields}
        previous = trial_runs.setdefault(ordinal, binding)
        if previous != binding:
            raise ContractError(f"trial run {ordinal} has inconsistent run binding")
        cases = trial_cases.setdefault(ordinal, set())
        if trial["case_id"] in cases:
            raise ContractError(f"trial run {ordinal} repeats a case")
        cases.add(trial["case_id"])

    if set(trial_runs) != {1, 2, 3} or len({item["local_run_id"] for item in trial_runs.values()}) != 3:
        raise ContractError("exactly three distinct trial runs are required")
    if len({item["provider_thread_id"] for item in trial_runs.values()}) != 3:
        raise ContractError("trial provider thread identities must be distinct")
    if len({item["fresh_session_marker"] for item in trial_runs.values()}) != 3:
        raise ContractError("trial fresh-session markers must be distinct")
    if not trial_cases or any(cases != trial_cases[1] for cases in trial_cases.values()):
        raise ContractError("all trial runs must cover the same unique case set")

    evaluator_ids: set[str] = set()
    evaluated_trials: set[str] = set()
    evaluation_runs: dict[int, dict] = {}
    evaluation_cases: dict[int, set[str]] = {}
    for evaluation in evaluations:
        receipt_id = evaluation["receipt_id"]
        if receipt_id in all_receipt_ids:
            raise ContractError("reused receipt identity")
        all_receipt_ids.add(receipt_id)
        trial_id = evaluation["trial_receipt_id"]
        trial = trial_by_receipt.get(trial_id)
        if trial is None:
            raise ContractError("evaluation references an unknown trial receipt")
        evaluator_id = evaluation["evaluator_id"]
        if evaluator_id in evaluator_ids or evaluator_id in trial_ids:
            raise ContractError("reused or colliding evaluator identity")
        if trial_id in evaluated_trials:
            raise ContractError("trial receipt has multiple evaluations")
        evaluator_ids.add(evaluator_id)
        evaluated_trials.add(trial_id)
        validate_evaluation(evaluation, trial=trial, gate=gate)
        ordinal = evaluation["run_ordinal"]
        binding = {field: evaluation[field] for field in run_binding_fields}
        previous = evaluation_runs.setdefault(ordinal, binding)
        if previous != binding:
            raise ContractError(f"evaluation run {ordinal} has inconsistent run binding")
        cases = evaluation_cases.setdefault(ordinal, set())
        if evaluation["case_id"] in cases:
            raise ContractError(f"evaluation run {ordinal} repeats a case")
        cases.add(evaluation["case_id"])

    if evaluated_trials != set(trial_by_receipt):
        raise ContractError("every trial receipt must have exactly one evaluation")
    if set(evaluation_runs) != {1, 2, 3} or len({item["local_run_id"] for item in evaluation_runs.values()}) != 3:
        raise ContractError("exactly three distinct evaluator runs are required")
    if len({item["provider_thread_id"] for item in evaluation_runs.values()}) != 3:
        raise ContractError("evaluator provider thread identities must be distinct")
    if len({item["fresh_session_marker"] for item in evaluation_runs.values()}) != 3:
        raise ContractError("evaluator fresh-session markers must be distinct")
    if any(evaluation_cases.get(ordinal) != trial_cases[ordinal] for ordinal in (1, 2, 3)):
        raise ContractError("evaluator runs must cover their paired trial case sets")
    all_run_values = [*trial_runs.values(), *evaluation_runs.values()]
    for field in ("local_run_id", "provider_thread_id", "fresh_session_marker"):
        if len({item[field] for item in all_run_values}) != 6:
            raise ContractError(f"trial/evaluator {field} values must be globally distinct")


def aggregate_routing_evaluations(records: list[dict]) -> dict:
    """Apply per-case gates plus the cross-case systematic-failure rule."""
    required = {"case_id", "family", "kind", "trial_id", "dispositions"}
    case_trials: dict[str, list[dict]] = {}
    failures: dict[str, dict[str, set[str]]] = {}
    seen_trials: set[str] = set()
    for record in records:
        _exact_keys(record, required)
        case_id = _text(record.get("case_id"), "case_id")
        family = _text(record.get("family"), "family")
        kind = record.get("kind")
        if kind not in {"critical", "ordinary"}:
            raise ContractError("aggregate kind must be critical or ordinary")
        trial_id = _uuid(record.get("trial_id"), "trial_id")
        if trial_id in seen_trials:
            raise ContractError("aggregate reuses a trial identity")
        seen_trials.add(trial_id)
        dispositions = record.get("dispositions")
        if not isinstance(dispositions, list) or not dispositions:
            raise ContractError("aggregate dispositions must be nonempty")
        keys: set[str] = set()
        for item in dispositions:
            if not isinstance(item, dict):
                raise ContractError("aggregate disposition must be an object")
            _exact_keys(item, {"rubric_key", "verdict"})
            key = _text(item.get("rubric_key"), "rubric_key")
            if key in keys or item.get("verdict") not in {"pass", "fail"}:
                raise ContractError("aggregate dispositions must have unique keys and pass/fail verdicts")
            keys.add(key)
            if item["verdict"] == "fail" and kind == "ordinary":
                bucket = failures.setdefault(key, {"cases": set(), "families": set()})
                bucket["cases"].add(case_id)
                bucket["families"].add(family)
        case_trials.setdefault(case_id, []).append(record)

    case_results: list[dict] = []
    for case_id, trials in sorted(case_trials.items()):
        if len(trials) != 3:
            raise ContractError(f"case {case_id} requires exactly three trials")
        kind = trials[0]["kind"]
        if any(item["kind"] != kind or item["family"] != trials[0]["family"] for item in trials):
            raise ContractError(f"case {case_id} has inconsistent kind or family")
        passes = sum(all(item["verdict"] == "pass" for item in trial["dispositions"]) for trial in trials)
        required_passes = 3 if kind == "critical" else 2
        case_results.append({
            "case_id": case_id,
            "kind": kind,
            "passes": passes,
            "required": required_passes,
            "verdict": "pass" if passes >= required_passes else "fail",
        })

    systematic = [
        key
        for key, bucket in sorted(failures.items())
        if len(bucket["cases"]) >= 3 and len(bucket["families"]) >= 2
    ]
    passed = not systematic and all(item["verdict"] == "pass" for item in case_results)
    return {
        "schema_version": "portfolio-routing-aggregate/v1",
        "verdict": "pass" if passed else "fail",
        "case_results": case_results,
        "systematic_failure_keys": systematic,
    }


def _same_packet(left: dict, right: dict) -> None:
    fields = ("packet_id", "packet_revision", "protected_digest", "repository_root")
    mismatched = [field for field in fields if left.get(field) != right.get(field)]
    if mismatched:
        raise ContractError(f"packet identity mismatch: {mismatched}")


def validate_receipt(value: dict, trial: dict | None = None, gate: dict | None = None) -> None:
    receipt_type = value.get("receipt_type")
    if receipt_type == "gate-approval/v1":
        if trial is not None or gate is not None:
            raise ContractError("gate approval does not consume another receipt")
        validate_gate(value)
    elif receipt_type == "trial-receipt/v1":
        if trial is not None:
            raise ContractError("trial receipt cannot consume another trial")
        validate_trial(value, gate=gate)
    elif receipt_type == "evaluation-receipt/v1":
        validate_evaluation(value, trial=trial, gate=gate)
    else:
        raise ContractError("unknown receipt_type")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    manifest_parser = subparsers.add_parser("manifest")
    manifest_parser.add_argument("--root", required=True)
    manifest_parser.add_argument("path", nargs="+")
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("receipt")
    validate_parser.add_argument("--trial")
    validate_parser.add_argument("--gate")
    validate_parser.add_argument("--inputs")
    hash_parser = subparsers.add_parser("hash")
    hash_parser.add_argument("json_file")
    state_parser = subparsers.add_parser("state")
    state_parser.add_argument("--repo", required=True)
    state_parser.add_argument("--watch", action="append", default=[])
    watch_parser = subparsers.add_parser("watch-paths")
    watch_parser.add_argument("--repo", required=True)
    watch_parser.add_argument("--profile", required=True)
    watch_parser.add_argument("--host-home", required=True)
    watch_parser.add_argument("--host-tmpdir", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "manifest":
            manifest = build_manifest(args.root, args.path)
            output = {"digest": digest_value(manifest), "manifest": manifest}
        elif args.command == "hash":
            value = strict_load(Path(args.json_file))
            output = {"digest": digest_value(value)}
        elif args.command == "state":
            output = state_snapshot(args.repo, args.watch)
        elif args.command == "watch-paths":
            paths = resolve_ambient_watch_profile(
                Path(args.profile),
                repo=args.repo,
                host_home=args.host_home,
                host_tmpdir=args.host_tmpdir,
            )
            for path in paths:
                print(path)
            return 0
        else:
            value = strict_load(Path(args.receipt))
            trial = strict_load(Path(args.trial)) if args.trial else None
            gate = strict_load(Path(args.gate)) if args.gate else None
            validate_receipt(value, trial=trial, gate=gate)
            if args.inputs:
                inputs = strict_load(Path(args.inputs))
                if value["receipt_type"] == "trial-receipt/v1":
                    validate_trial_inputs(value, inputs)
                elif value["receipt_type"] == "evaluation-receipt/v1":
                    validate_evaluation_inputs(value, inputs)
                else:
                    raise ContractError("gate approvals do not consume input bindings")
            output = {"digest": digest_value(value), "receipt_type": value["receipt_type"], "valid": True}
    except ContractError as exc:
        print(json.dumps({"error": str(exc), "valid": False}, sort_keys=True), file=sys.stderr)
        return 3
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
