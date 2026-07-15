#!/usr/bin/env python3
"""Strict JSON and canonical-byte helpers for history v4.

The history contracts intentionally have no third-party runtime dependency.
This module therefore implements the small, security-relevant subset shared by
the normalizers and validators: duplicate-key rejection, integer-only JSON,
NFC strings, and RFC-8785-compatible canonical bytes for the accepted domain.
"""

from __future__ import annotations

import json
import math
import unicodedata
from pathlib import Path
from typing import Any


class StrictJSONError(ValueError):
    pass


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    normalized_keys: set[str] = set()
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON object key: {key!r}")
        normalized = unicodedata.normalize("NFC", key)
        if normalized in normalized_keys:
            raise StrictJSONError(
                f"normalized JSON object key collision: {normalized!r}"
            )
        normalized_keys.add(normalized)
        result[key] = value
    return result


def loads_strict(value: str) -> object:
    def reject_constant(token: str) -> object:
        raise StrictJSONError(f"non-finite JSON number is not allowed: {token}")

    try:
        result = json.loads(
            value,
            object_pairs_hook=_unique_object,
            parse_constant=reject_constant,
            parse_float=lambda token: (_ for _ in ()).throw(
                StrictJSONError(f"non-integer JSON number is not allowed: {token}")
            ),
        )
        validate_domain(result)
        return result
    except StrictJSONError:
        raise
    except json.JSONDecodeError as exc:
        raise StrictJSONError(str(exc)) from exc


def load_strict(path: Path) -> object:
    """Read one strict UTF-8 JSON value without a decoding fallback."""

    try:
        return loads_strict(path.read_text(encoding="utf-8", errors="strict"))
    except UnicodeDecodeError as exc:
        raise StrictJSONError(f"invalid UTF-8 in {path}: {exc}") from exc


def validate_domain(value: object, path: str = "$") -> None:
    """Enforce the canonical-json/v1 input domain recursively."""

    if value is None or isinstance(value, bool) or isinstance(value, int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise StrictJSONError(f"non-finite number at {path}")
        raise StrictJSONError(f"non-integer JSON number at {path}")
    if isinstance(value, str):
        if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise StrictJSONError(f"unpaired surrogate at {path}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate_domain(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise StrictJSONError(f"non-string object key at {path}")
            validate_domain(key, f"{path}.<key>")
            validate_domain(item, f"{path}.{key}")
        return
    raise StrictJSONError(f"unsupported JSON value {type(value).__name__} at {path}")


def _canonical(value: object) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(
            unicodedata.normalize("NFC", value),
            ensure_ascii=False,
            separators=(",", ":"),
        )
    if isinstance(value, list):
        return "[" + ",".join(_canonical(item) for item in value) + "]"
    if isinstance(value, dict):
        # RFC 8785 sorts property names by their UTF-16 code units.
        normalized: dict[str, object] = {}
        for key, item in value.items():
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized:
                raise StrictJSONError(
                    f"normalized JSON object key collision: {normalized_key!r}"
                )
            normalized[normalized_key] = item
        keys = sorted(normalized, key=lambda item: item.encode("utf-16be"))
        return "{" + ",".join(
            _canonical(key) + ":" + _canonical(normalized[key]) for key in keys
        ) + "}"
    raise StrictJSONError(f"unsupported canonical value: {type(value).__name__}")


def canonical_bytes(value: object) -> bytes:
    validate_domain(value)
    return _canonical(value).encode("utf-8")


def dump_canonical(value: object) -> str:
    return canonical_bytes(value).decode("utf-8")
