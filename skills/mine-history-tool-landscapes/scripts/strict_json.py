#!/usr/bin/env python3
"""Strict JSON decoding shared by the history indexer and validator."""

from __future__ import annotations

import json


class StrictJSONError(ValueError):
    pass


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def loads_strict(value: str) -> object:
    try:
        return json.loads(value, object_pairs_hook=_unique_object)
    except StrictJSONError:
        raise
    except json.JSONDecodeError as exc:
        raise StrictJSONError(str(exc)) from exc
