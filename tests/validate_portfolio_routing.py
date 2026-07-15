#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path("tests/contracts/portfolio-routing-v1.schema.json")
CONTRACT_PATH = Path("tests/portfolio-routing-v1.json")
CASES_PATH = Path("tests/portfolio-routing-cases-v1.json")
PROMPTS_PATH = Path("tests/portfolio-routing-prompts-v1.json")
RUBRICS_PATH = Path("tests/portfolio-routing-rubrics-v1.json")
SOURCE_MAP_PATH = Path("tests/portfolio-routing-source-map-v1.json")
ROLE_FIELDS = (
    "outer_owner",
    "gateways",
    "overlays",
    "evidence_lenses",
    "mechanics",
    "transports",
    "content_owners",
    "fallbacks",
)
ROLE_RELATIONS = (
    "outer",
    "gateway",
    "overlay",
    "evidence-lens",
    "mechanics",
    "transport",
    "content-owner",
    "fallback",
)
EXTERNAL_ROUTE_ORDER = (
    "native-codex",
    "built-in-collaboration",
    "browser-web",
    "stop",
    "skill-creator",
)
OVERLAP_FAMILIES = {
    "audit-brief",
    "audit-front",
    "audit-goal",
    "align-audit-goal",
    "front-align-handoff",
    "agentmail-front-native",
    "brief-map-history",
    "propagate-refactor",
    "skill-authoring",
    "unavailable-private-source",
    "unavailable-public-source",
    "unavailable-routine-collaboration",
    "unavailable-front-approved-change",
}
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


class ContractError(ValueError):
    pass


def strict_json(path: Path) -> Any:
    def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ContractError(f"{path}: duplicate key {key!r}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise ContractError(f"{path}: non-finite number {value}")

    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_pairs,
        parse_constant=reject_constant,
    )


def resolve(root: Path, overlay: Path | None, relative: Path) -> Path:
    if overlay is not None:
        candidate = overlay / relative
        if candidate.exists() or candidate.is_symlink():
            return candidate
    return root / relative


def frontmatter_description(text: str, path: Path) -> str:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ContractError(f"{path}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ContractError(f"{path}: unterminated YAML frontmatter") from error
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict) or not isinstance(data.get("description"), str):
        raise ContractError(f"{path}: description is missing")
    return data["description"]


def schema_errors(schema: dict[str, Any], document: Any, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{label}: schema error at {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def render_routing_block(row: dict[str, Any]) -> str:
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


def validate(root: Path, overlay: Path | None = None) -> list[str]:
    errors: list[str] = []
    schema_file = resolve(root, overlay, SCHEMA_PATH)
    contract_file = resolve(root, overlay, CONTRACT_PATH)
    cases_file = resolve(root, overlay, CASES_PATH)
    prompts_file = resolve(root, overlay, PROMPTS_PATH)
    rubrics_file = resolve(root, overlay, RUBRICS_PATH)
    source_map_file = resolve(root, overlay, SOURCE_MAP_PATH)

    schema = strict_json(schema_file)
    Draft202012Validator.check_schema(schema)
    contract = strict_json(contract_file)
    cases = strict_json(cases_file)
    prompts = strict_json(prompts_file)
    rubrics = strict_json(rubrics_file)
    source_map = strict_json(source_map_file)
    for label, document in (
        ("contract", contract),
        ("cases", cases),
        ("prompts", prompts),
        ("rubrics", rubrics),
        ("source-map", source_map),
    ):
        errors.extend(schema_errors(schema, document, label))

    if errors:
        return errors

    skills = contract["portfolio_skills"]
    rows = contract["rows"]
    row_names = [row["skill"] for row in rows]
    if row_names != skills:
        errors.append("contract: row order and membership must exactly equal portfolio_skills")
    if len(set(row_names)) != len(row_names):
        errors.append("contract: duplicate skill row")

    role_taxonomy = contract["role_taxonomy"]
    if [item["field"] for item in role_taxonomy] != list(ROLE_FIELDS):
        errors.append("contract: role taxonomy field order differs from the closed role grammar")
    if [item["relation"] for item in role_taxonomy] != list(ROLE_RELATIONS):
        errors.append("contract: role taxonomy relation order differs from the closed role grammar")
    role_by_field = {item["field"]: item for item in role_taxonomy}
    relation_to_field = {item["relation"]: item["field"] for item in role_taxonomy}

    external_routes = contract["external_routes"]
    external_names = [item["route"] for item in external_routes]
    if external_names != list(EXTERNAL_ROUTE_ORDER):
        errors.append("contract: external route order and membership differ")
    if len(set(external_names)) != len(external_names):
        errors.append("contract: duplicate external route")
    known_routes = set(skills) | set(external_names)
    allowed_by_field = {
        field: set(role_by_field[field]["allowed_routes"])
        for field in ROLE_FIELDS
    }
    for field, allowed in allowed_by_field.items():
        unknown = sorted(allowed - known_routes)
        if unknown:
            errors.append(f"contract: role {field} names unknown routes {unknown}")
    cataloged_by_role = set().union(*allowed_by_field.values())
    missing_role = sorted(known_routes - cataloged_by_role)
    if missing_role:
        errors.append(f"contract: routes have no allowed role {missing_role}")

    composition_edges: dict[str, set[tuple[str, str]]] = {
        route: set() for route in known_routes
    }

    def add_compositions(source: str, compositions: list[dict[str, str]]) -> None:
        for composition in compositions:
            target = composition["route"]
            relation = composition["relation"]
            if target not in known_routes:
                errors.append(f"contract: {source} names unavailable composition route {target!r}")
                continue
            field = relation_to_field.get(relation)
            if field is None or field == "outer_owner":
                errors.append(f"contract: {source} names invalid target relation {relation!r}")
                continue
            if target not in allowed_by_field[field]:
                errors.append(
                    f"contract: {source} composes {target!r} as {relation!r}, "
                    f"but {target!r} is not allowed in {field}"
                )
                continue
            edge = (target, relation)
            if edge in composition_edges[source]:
                errors.append(f"contract: {source} duplicates composition edge {edge}")
            composition_edges[source].add(edge)

    for external in external_routes:
        add_compositions(external["route"], external["legal_compositions"])

    case_families: dict[str, set[str]] = {}
    for row in rows:
        name = row["skill"]
        family = row["case_family"]
        case_families[family] = set()
        skill_path = Path("skills") / name / "SKILL.md"
        agent_path = Path("skills") / name / "agents" / "openai.yaml"
        skill_file = resolve(root, overlay, skill_path)
        agent_file = resolve(root, overlay, agent_path)
        if not skill_file.is_file():
            errors.append(f"{skill_path}: missing")
            continue
        if not agent_file.is_file():
            errors.append(f"{agent_path}: missing")
            continue

        skill_text = skill_file.read_text(encoding="utf-8")
        actual_description = frontmatter_description(skill_text, skill_file)
        expected_description = row["package_projection"]["frontmatter_description"]
        if actual_description != expected_description:
            errors.append(f"{skill_path}: frontmatter description diverges from canonical projection")

        begin_count = skill_text.count(ROUTING_BLOCK_BEGIN)
        end_count = skill_text.count(ROUTING_BLOCK_END)
        expected_block = render_routing_block(row)
        if begin_count != 1 or end_count != 1:
            errors.append(
                f"{skill_path}: expected exactly one complete generated routing block; "
                f"got {begin_count} begin and {end_count} end markers"
            )
        else:
            begin = skill_text.index(ROUTING_BLOCK_BEGIN)
            end = skill_text.index(ROUTING_BLOCK_END, begin) + len(ROUTING_BLOCK_END)
            if skill_text[begin:end] != expected_block:
                errors.append(
                    f"{skill_path}: generated routing block is stale or hand-edited"
                )

        agent_text = agent_file.read_text(encoding="utf-8")
        agent_data = yaml.safe_load(agent_text)
        interface = agent_data.get("interface", {}) if isinstance(agent_data, dict) else {}
        policy = agent_data.get("policy", {}) if isinstance(agent_data, dict) else {}
        actual_agent = {
            "display_name": interface.get("display_name"),
            "short_description": interface.get("short_description"),
            "default_prompt": interface.get("default_prompt"),
            "allow_implicit_invocation": policy.get("allow_implicit_invocation"),
        }
        if actual_agent != row["package_projection"]["agent"]:
            errors.append(f"{agent_path}: interface or implicit policy diverges from canonical projection")
        row_digest = hashlib.sha256(
            json.dumps(
                row,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        marker = f"# portfolio-routing-v1-row-sha256: {row_digest}"
        if marker not in agent_text.splitlines():
            errors.append(f"{agent_path}: full canonical routing row digest diverges")

        for phrase in row["body_assertions"]["required"]:
            if phrase not in skill_text:
                errors.append(f"{skill_path}: missing canonical body assertion {phrase!r}")
        for phrase in row["body_assertions"]["forbidden"]:
            if phrase in skill_text:
                errors.append(f"{skill_path}: contains forbidden routing assertion {phrase!r}")

        add_compositions(name, row["legal_compositions"])
        for fallback in row["fallbacks"]:
            if fallback["route"] not in known_routes:
                errors.append(f"contract: {name} names unavailable fallback route {fallback['route']!r}")

    expected_cases = {
        "schema_version": "portfolio-routing-cases/v1",
        "canonical_contract": contract["canonical_owner"],
        "visibility": "evaluator-only",
        "cases": contract["routing_cases"],
    }
    if cases != expected_cases:
        errors.append("cases: catalog differs from the exact canonical routing_cases projection")
    expected_prompts = {
        "schema_version": "portfolio-routing-prompts/v1",
        "canonical_contract": contract["canonical_owner"],
        "visibility": "trial-input",
        "cases": [
            {field: case[field] for field in ("id", "kind", "family", "prompt")}
            for case in contract["routing_cases"]
        ],
    }
    if prompts != expected_prompts:
        errors.append("prompts: catalog differs from the exact raw canonical case projection")
    expected_rubrics = {
        "schema_version": "portfolio-routing-rubrics/v1",
        "canonical_contract": contract["canonical_owner"],
        "expected_answer_catalog": CASES_PATH.as_posix(),
        "visibility": "evaluator-only",
        **contract["routing_rubrics"],
    }
    if rubrics != expected_rubrics:
        errors.append("rubrics: policy differs from the exact canonical routing_rubrics projection")

    catalog_ids: set[str] = set()
    overlap_seen: set[str] = set()
    for case in cases["cases"]:
        case_id = case["id"]
        if case_id in catalog_ids:
            errors.append(f"cases: duplicate id {case_id!r}")
        catalog_ids.add(case_id)
        family = case["family"]
        if case["kind"] in {"positive", "negative"}:
            if family not in case_families:
                errors.append(f"cases: uncataloged family {family!r}")
            else:
                case_families[family].add(case["kind"])
        else:
            overlap_seen.add(family)
        expected = case["expected"]
        selected_by_field = {
            "outer_owner": [expected["outer_owner"]],
            **{field: expected[field] for field in ROLE_FIELDS if field != "outer_owner"},
        }
        referenced_list = [
            (field, route)
            for field in ROLE_FIELDS
            for route in selected_by_field[field]
        ]
        referenced = {route for _, route in referenced_list}
        unknown = sorted(referenced - known_routes)
        if unknown:
            errors.append(f"cases: {case_id} names unknown routes {unknown}")
        for field, route in referenced_list:
            if route in known_routes and route not in allowed_by_field[field]:
                errors.append(f"cases: {case_id} route {route!r} is not allowed in {field}")
        duplicates = sorted(
            route for route in referenced
            if sum(1 for _, candidate in referenced_list if candidate == route) > 1
        )
        if duplicates:
            errors.append(f"cases: {case_id} duplicates routes across roles {duplicates}")

        selected = {route for route in referenced if route in known_routes}
        reached = {expected["outer_owner"]} if expected["outer_owner"] in selected else set()
        progress = True
        while progress:
            progress = False
            for source in tuple(reached):
                for target, relation in composition_edges.get(source, set()):
                    field = relation_to_field[relation]
                    if target in selected_by_field[field] and target not in reached:
                        reached.add(target)
                        progress = True
        unreachable = sorted(selected - reached)
        if unreachable:
            errors.append(
                f"cases: {case_id} routes are not reachable through directional legal compositions {unreachable}"
            )

    prompt_ids: set[str] = set()
    evaluator_by_id = {case["id"]: case for case in cases["cases"]}
    for prompt_case in prompts["cases"]:
        case_id = prompt_case["id"]
        if case_id in prompt_ids:
            errors.append(f"prompts: duplicate id {case_id!r}")
        prompt_ids.add(case_id)
        evaluator_case = evaluator_by_id.get(case_id)
        if evaluator_case is None:
            errors.append(f"prompts: unknown evaluator case {case_id!r}")
            continue
        projected = {
            field: evaluator_case[field]
            for field in ("id", "kind", "family", "prompt")
        }
        if prompt_case != projected:
            errors.append(f"prompts: {case_id} differs from the evaluator case raw projection")
    if prompt_ids != catalog_ids:
        errors.append("prompts: case IDs must exactly match evaluator case IDs")

    rubric_keys = [item["key"] for item in rubrics["rubric_catalog"]]
    known_rubrics = set(rubric_keys)
    if len(known_rubrics) != len(rubric_keys):
        errors.append("rubrics: duplicate rubric key")
    unknown_defaults = set(rubrics["default_rubric_keys"]) - known_rubrics
    if unknown_defaults:
        errors.append(f"rubrics: default policy names unknown keys {sorted(unknown_defaults)}")
    override_ids: set[str] = set()
    unknown_critical = set(rubrics["critical_case_ids"]) - catalog_ids
    if unknown_critical:
        errors.append(f"rubrics: critical policy names unknown cases {sorted(unknown_critical)}")
    for override in rubrics["case_overrides"]:
        case_id = override["case_id"]
        if case_id in override_ids:
            errors.append(f"rubrics: duplicate override for {case_id!r}")
        override_ids.add(case_id)
        if case_id not in catalog_ids:
            errors.append(f"rubrics: override names unknown case {case_id!r}")
        unknown_keys = set(override["add"]) - known_rubrics
        if unknown_keys:
            errors.append(f"rubrics: {case_id} names unknown keys {sorted(unknown_keys)}")

    for family, kinds in sorted(case_families.items()):
        if kinds != {"positive", "negative"}:
            errors.append(f"cases: family {family!r} requires exactly positive and negative coverage")
    if overlap_seen != OVERLAP_FAMILIES:
        errors.append(
            f"cases: overlap families differ; expected {sorted(OVERLAP_FAMILIES)}, got {sorted(overlap_seen)}"
        )

    if source_map["canonical_owner"] != contract["canonical_owner"]:
        errors.append("source-map: canonical owner differs from contract")
    if source_map["editable_truths"] != [contract["canonical_owner"]]:
        errors.append("source-map: routing contract must be the only editable truth")

    readme = resolve(root, overlay, Path("README.md")).read_text(encoding="utf-8")
    required_readme = [
        "## Canonical portfolio routing",
        "`tests/portfolio-routing-v1.json` is the only editable source of portfolio routing truth.",
        "Package descriptions, agent metadata, generated routing contract blocks, and evaluator-only cases are validated projections.",
        "`tests/portfolio-routing-prompts-v1.json` is the only catalog copied into an isolated trial root",
        "Expected routes and rubrics remain evaluator-only",
        "`scripts/sync_portfolio_routing.py --check` verifies every generated routing projection",
    ]
    for phrase in required_readme:
        if phrase not in readme:
            errors.append(f"README.md: missing routing ownership statement {phrase!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical portfolio routing and package parity.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--overlay", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    overlay = args.overlay.resolve() if args.overlay else None
    errors = validate(root, overlay)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("portfolio routing valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
