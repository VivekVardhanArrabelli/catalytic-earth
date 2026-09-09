#!/usr/bin/env python3
"""Reproduce a source-bound assembly projection and its reviewed interpretation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_assembly_context import project_assembly  # noqa: E402
from catalytic_earth.canonical_hash import canonical_file_sha256  # noqa: E402

DEFAULT_PACKET = ROOT / "data/atlas/assembly_context/6ha3"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def _bound_source(binding: dict, root: Path) -> Path:
    relative = binding.get("path")
    _require(isinstance(relative, str) and bool(relative), "source path is absent")
    posix, windows = PurePosixPath(relative), PureWindowsPath(relative)
    _require(
        not posix.is_absolute() and not windows.drive and not windows.is_absolute()
        and "\\" not in relative and ".." not in posix.parts
        and relative == posix.as_posix(),
        "source path must be repository-relative",
    )
    path = (root / relative).resolve()
    _require(root.resolve() in path.parents and path.is_file(), "bound source is missing")
    _require(canonical_file_sha256(path) == binding.get("sha256"), "bound source hash differs")
    return path


def build(packet: Path = DEFAULT_PACKET, root: Path = ROOT) -> dict:
    spec = _json(packet / "spec.json")
    _require(spec.get("schema_version") == "catalytic-earth.assembly-context-spec.v1", "spec schema differs")
    source = _bound_source(spec["coordinate_source"], root)
    bindings = spec["retained_context_bindings"]
    _require(len(bindings) == 2, "retained context binding count differs")
    contexts = {binding["binding_role"]: _json(_bound_source(binding, root)) for binding in bindings}
    _require(set(contexts) == {"study_projection", "source_inventory"}, "retained context roles differ")
    _validate_context(spec, contexts["study_projection"], contexts["source_inventory"])
    geometry = project_assembly(source.read_text(encoding="utf-8"), spec["assembly_spec"])
    return {
        "schema_version": "catalytic-earth.reviewed-assembly-context.v1",
        "packet_id": spec["packet_id"],
        "coordinate_source": spec["coordinate_source"],
        "geometry": geometry,
        "source_reviewed_context": spec["source_reviewed_context"],
        "claim_scope": "selected assembly atoms with a source-scoped omission warning",
        "independent_validation": False,
        "complete_active_site": False,
        "geometry_to_function_causation": False,
    }


def _validate_context(spec: dict, study: dict, inventory: dict) -> None:
    """Check evidence joins; source correctness still requires the pinned review."""
    context = spec["source_reviewed_context"]
    subject = context["structure_subject"]
    deposited = study["arrangement"]
    _require(
        subject["pdb_id"] == spec["assembly_spec"]["pdb_id"] == deposited["pdb_id"]
        and subject["reported_variant"] == deposited["protein"]["deposited_mutation"],
        "study structure/variant identity differs",
    )
    _require(
        all(spec["coordinate_source"][key] == deposited["coordinate_source"][key] for key in ("path", "sha256")),
        "study coordinate binding differs",
    )
    selections = spec["assembly_spec"]["selections"]
    by_id = {row["selection_id"]: row for row in selections}
    _require(len(by_id) == len(selections), "selection IDs repeat")
    relation, role = context["relation"], context["source_role"]
    site_id = relation["structure_selection_id"]
    _require(site_id in by_id and role["selection_id"] == site_id, "source role/selection binding differs")
    site_binding = subject["site_selection_binding"]
    _require(
        site_binding.get("selection_id") == site_id
        and all(by_id[site_id].get(key) == value for key, value in site_binding.items())
        and set(site_binding) == {"selection_id", "operator_ids", "model_id", "label_asym_id", "auth_seq_id", "label_comp_id", "atom_names"},
        "source role/copy binding differs",
    )
    panel = context["functional_panel"]
    _require(panel["study_doi"] == study["study"]["doi"] == inventory["study"]["doi"], "study DOI differs")
    _require(relation["functional_observation_id"] == panel["observation_id"], "functional observation binding differs")
    variants = [row["reported_variant"] for row in panel["variant_results"]]
    _require(len(variants) == len(set(variants)) and variants.count(relation["compared_variant"]) == 1, "compared variant is absent or ambiguous")
    _require(
        relation["same_variant_as_structure"] is (relation["compared_variant"] == subject["reported_variant"]),
        "structure/assay variant equivalence differs",
    )
    _require(relation["selective_partner_only_intervention"] is False, "unsupported selective-copy intervention")
    _require(panel["numeric_detection_floor"] is None and panel["numeric_intermediate_fraction"] is None, "unsupported quantitative nondetection")
    turnover = context["separate_turnover_observation"]
    _require(
        turnover["observation_id"] != panel["observation_id"] and turnover["endpoint"] != panel["endpoint"]
        and relation["compared_variant"] in turnover["k_cat_per_s"],
        "separate turnover endpoint binding differs",
    )
    _require(context["kinetic_reporter_limit"]["reported_variant"] == relation["compared_variant"], "reporter variant binding differs")
    sources = {row["artifact_id"]: row for row in inventory["sources"]}
    cited_ids = [row["artifact_id"] for row in context["sources"]]
    _require(bool(cited_ids) and len(cited_ids) == len(set(cited_ids)), "cited source IDs are absent or repeat")
    for evidence in (role, panel, turnover, context["kinetic_reporter_limit"]):
        ids = evidence["source_artifact_ids"]
        _require(bool(ids) and len(ids) == len(set(ids)) and set(ids) <= set(cited_ids), "evidence source binding differs")
    for cited in context["sources"]:
        source = sources.get(cited["artifact_id"], {})
        _require(
            all(cited[key] == source.get(key) for key in ("artifact_id", "sha256", "bytes", "source_url", "redistributed"))
            and cited["inherited_inspection_depth"] == source.get("inspection_depth"),
            "cited source/inventory binding differs",
        )


def check(packet: Path = DEFAULT_PACKET, root: Path = ROOT) -> dict:
    result = build(packet, root)
    _require(_json(packet / "projection.json") == result, "assembly projection is stale")
    review = _json(packet / "review.json")
    _require(review.get("schema_version") == "catalytic-earth.assembly-context-review.v1", "assembly review schema differs")
    pins = {name: canonical_file_sha256(packet / name) for name in ("spec.json", "projection.json", "acquisition_appendix.json")}
    _require(review.get("reviewed_sha256") == pins, "assembly review pins are stale")
    _require(review.get("decision") == "accept_source_scoped_omission_warning", "assembly review decision differs")
    acquisition = _json(packet / "acquisition_appendix.json")
    _require(acquisition.get("schema_version") == "catalytic-earth.source-acquisition-appendix.v1", "acquisition appendix schema differs")
    inherited = _json(_bound_source(acquisition["inherited_receipts"], root))
    attempts = acquisition["additional_attempts"]
    _require(
        all(type(row.get("bytes_read")) is int and row["bytes_read"] >= 0 for row in attempts),
        "additional acquisition byte counts are invalid",
    )
    count = inherited["aggregate"]["direct_capture_request_count"] + len(attempts)
    size = inherited["aggregate"]["direct_capture_response_bytes"] + sum(row["bytes_read"] for row in attempts)
    _require(acquisition["cumulative_direct_capture_requests"] == count, "cumulative request count differs")
    _require(acquisition["cumulative_direct_capture_bytes"] == size, "cumulative byte count differs")
    _require(count <= 100 and size <= 31457280, "cumulative source budget exceeded")
    _require(all(row["batch_id"] == acquisition["batch_id"] for row in attempts), "source batch identity differs")
    spec = _json(packet / "spec.json")
    inventory_binding = next(row for row in spec["retained_context_bindings"] if row["binding_role"] == "source_inventory")
    inventory = _json(_bound_source(inventory_binding, root))
    _require(acquisition["batch_id"] == inventory["batch_id"], "inherited source batch differs")
    start = inherited["aggregate"]["direct_capture_request_count"] + 1
    _require([row["request_index"] for row in attempts] == list(range(start, start + len(attempts))), "cumulative request indices differ")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--query", action="store_true")
    args = parser.parse_args()
    if args.check or args.query:
        result = check(args.packet)
        if args.query:
            print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
        else:
            print(f"Assembly context and source-review pins are current: {result['packet_id']}")
    else:
        result = build(args.packet)
        (args.packet / "projection.json").write_text(
            json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
        )
        print("Wrote assembly projection; source review is required before --check succeeds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
