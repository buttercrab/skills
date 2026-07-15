#!/usr/bin/env python3
"""Render every declared portfolio-routing projection from its canonical contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = Path("tests/portfolio-routing-v1.json")
CASES = Path("tests/portfolio-routing-cases-v1.json")
PROMPTS = Path("tests/portfolio-routing-prompts-v1.json")
RUBRICS = Path("tests/portfolio-routing-rubrics-v1.json")
DESCRIPTION = re.compile(r"(?m)^description:.*$")
ROUTING_BLOCK_BEGIN = "<!-- BEGIN GENERATED PORTFOLIO ROUTING v1 -->"
ROUTING_BLOCK_END = "<!-- END GENERATED PORTFOLIO ROUTING v1 -->"
ROUTING_BLOCK_FIELDS = (
    "skill",
    "routing_role",
    "portfolio_position",
    "positive_request_classes",
    "triggers",
    "exclusions",
    "state_owner",
    "precedence",
    "legal_compositions",
    "fallbacks",
    "forbidden_actions",
)


class SyncError(ValueError):
    pass


def strict_json(path: Path) -> dict:
    def reject_pairs(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise SyncError(f"{path}: duplicate key {key!r}")
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_pairs,
        parse_constant=lambda item: (_ for _ in ()).throw(
            SyncError(f"{path}: non-finite number {item}")
        ),
    )
    if not isinstance(value, dict):
        raise SyncError(f"{path}: expected object")
    return value


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def row_digest(row: dict) -> str:
    encoded = json.dumps(
        row,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def render_agent(row: dict) -> bytes:
    agent = row["package_projection"]["agent"]
    lines = [
        f"# portfolio-routing-v1-row-sha256: {row_digest(row)}",
        "interface:",
        f"  display_name: {json.dumps(agent['display_name'], ensure_ascii=False)}",
        f"  short_description: {json.dumps(agent['short_description'], ensure_ascii=False)}",
        f"  default_prompt: {json.dumps(agent['default_prompt'], ensure_ascii=False)}",
    ]
    implicit = agent["allow_implicit_invocation"]
    if implicit is not None:
        lines.extend(
            [
                "policy:",
                f"  allow_implicit_invocation: {'true' if implicit else 'false'}",
            ]
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_routing_block(row: dict) -> str:
    projection = {field: row[field] for field in ROUTING_BLOCK_FIELDS}
    lines = [
        ROUTING_BLOCK_BEGIN,
        "## Portfolio routing contract (generated)",
        "",
        "This block is generated from `tests/portfolio-routing-v1.json`; do not edit it by hand.",
        "",
    ]
    for field, value in projection.items():
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        lines.append(f"- `{field}`: {encoded}")
    lines.append(ROUTING_BLOCK_END)
    return "\n".join(lines)


def render_skill(path: Path, row: dict) -> bytes:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.find("\n---\n", 4) < 0:
        raise SyncError(f"{path}: invalid frontmatter")
    frontmatter_end = text.find("\n---\n", 4)
    prefix = text[:frontmatter_end]
    if len(DESCRIPTION.findall(prefix)) != 1:
        raise SyncError(f"{path}: expected one frontmatter description")
    rendered = DESCRIPTION.sub(
        f"description: {row['package_projection']['frontmatter_description']}",
        prefix,
    ) + text[frontmatter_end:]
    block = render_routing_block(row)
    begin_count = rendered.count(ROUTING_BLOCK_BEGIN)
    end_count = rendered.count(ROUTING_BLOCK_END)
    if begin_count == end_count == 0:
        rendered = rendered.rstrip() + "\n\n" + block + "\n"
    elif begin_count == end_count == 1:
        begin = rendered.index(ROUTING_BLOCK_BEGIN)
        end = rendered.index(ROUTING_BLOCK_END, begin) + len(ROUTING_BLOCK_END)
        rendered = rendered[:begin] + block + rendered[end:]
    else:
        raise SyncError(
            f"{path}: expected zero or one complete generated routing block, "
            f"got {begin_count} begin and {end_count} end markers"
        )
    return rendered.encode("utf-8")


def projections(root: Path) -> dict[Path, bytes]:
    contract = strict_json(root / CONTRACT)
    cases = contract["routing_cases"]
    rubric = contract["routing_rubrics"]
    outputs: dict[Path, bytes] = {
        CASES: json_bytes(
            {
                "schema_version": "portfolio-routing-cases/v1",
                "canonical_contract": CONTRACT.as_posix(),
                "visibility": "evaluator-only",
                "cases": cases,
            }
        ),
        PROMPTS: json_bytes(
            {
                "schema_version": "portfolio-routing-prompts/v1",
                "canonical_contract": CONTRACT.as_posix(),
                "visibility": "trial-input",
                "cases": [
                    {key: case[key] for key in ("id", "kind", "family", "prompt")}
                    for case in cases
                ],
            }
        ),
        RUBRICS: json_bytes(
            {
                "schema_version": "portfolio-routing-rubrics/v1",
                "canonical_contract": CONTRACT.as_posix(),
                "expected_answer_catalog": CASES.as_posix(),
                "visibility": "evaluator-only",
                **rubric,
            }
        ),
    }
    for row in contract["rows"]:
        skill = row["skill"]
        skill_path = Path("skills") / skill / "SKILL.md"
        agent_path = Path("skills") / skill / "agents" / "openai.yaml"
        outputs[skill_path] = render_skill(root / skill_path, row)
        outputs[agent_path] = render_agent(row)
    return outputs


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    temporary = path.parent / f".{path.name}.tmp.{os.getpid()}.{uuid.uuid4()}"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        os.chmod(path, mode)
        directory = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if a projection differs")
    mode.add_argument("--write", action="store_true", help="atomically update projections")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    changed = []
    for relative, expected in projections(root).items():
        path = root / relative
        actual = path.read_bytes() if path.is_file() else None
        if actual == expected:
            continue
        changed.append(relative.as_posix())
        if args.write:
            atomic_write(path, expected)
    if changed and not args.write:
        for path in changed:
            print(f"routing projection differs: {path}", file=sys.stderr)
        return 1
    action = "updated" if args.write else "verified"
    print(f"portfolio routing projections {action}: {len(changed)} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
