from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


DISTANCE_BINS_ANGSTROM = [0.0, 3.0, 4.5, 6.0, 8.0, 12.0, 16.0, 24.0, 40.0]

FORBIDDEN_PREDICTIVE_KEY_FRAGMENTS = [
    "ec_label",
    "ec_number",
    "entry",
    "expert",
    "fingerprint",
    "label",
    "mechanism",
    "name",
    "note",
    "pdb",
    "rationale",
    "review",
    "rhea",
    "source",
    "uniprot",
]


def build_active_site_encoder_cache(
    *,
    readiness_matrix: dict[str, Any],
    geometry_features: dict[str, Any],
    include_rows: list[str] | None = None,
    max_rows: int | None = None,
) -> dict[str, Any]:
    """Build a small label-blind active-site feature cache from local artifacts."""
    readiness_rows = [
        row
        for row in readiness_matrix.get("rows", [])
        if isinstance(row, dict)
        and row.get("allowed_use") == "label_blind_feature_extraction_smoke_ready"
        and not row.get("quarantined_before_model_claims")
    ]
    if include_rows:
        include_set = set(include_rows)
        available = {str(row.get("candidate_id")) for row in readiness_rows}
        missing = sorted(include_set - available)
        if missing:
            raise ValueError(
                "include rows are not label-blind smoke-ready: " + ", ".join(missing)
            )
        readiness_rows = [
            row for row in readiness_rows if str(row.get("candidate_id")) in include_set
        ]
    if max_rows is not None:
        readiness_rows = readiness_rows[:max_rows]

    geometry_by_entry = {
        str(entry.get("entry_id")): entry
        for entry in geometry_features.get("entries", [])
        if isinstance(entry, dict) and entry.get("entry_id")
    }

    records = []
    skipped_rows = []
    for row in readiness_rows:
        entry_id = str(row["candidate_id"])
        geometry_entry = geometry_by_entry.get(entry_id)
        if not geometry_entry:
            skipped_rows.append({"entry_id": entry_id, "reason": "geometry_entry_missing"})
            continue
        if geometry_entry.get("status") != "ok":
            skipped_rows.append(
                {
                    "entry_id": entry_id,
                    "reason": "geometry_entry_not_ok",
                    "status": geometry_entry.get("status"),
                }
            )
            continue
        records.append(_cache_record(row, geometry_entry))

    forbidden_hits = sorted(
        {
            hit
            for record in records
            for hit in _forbidden_predictive_key_hits(record["predictive_features"])
        }
    )
    summary = {
        "artifact_id": "v3_active_site_encoder_cache_smoke_20260528",
        "schema_version": "active_site_encoder_cache.v1",
        "created_utc": _utc_now_iso(),
        "review_only": True,
        "label_blind": True,
        "training_executed": False,
        "label_registry_changed": False,
        "fingerprint_registry_changed": False,
        "production_scoring_changed": False,
        "thresholds_changed": False,
        "requested_row_count": len(readiness_rows),
        "emitted_row_count": len(records),
        "skipped_rows": skipped_rows,
        "predictive_feature_forbidden_key_hits": forbidden_hits,
        "forbidden_inputs_used": [],
        "predictive_feature_contract": {
            "row_identifiers_in_metadata_only": True,
            "target_labels_in_predictive_features": False,
            "source_ids_in_predictive_features": False,
            "mechanism_text_in_predictive_features": False,
            "entry_names_in_predictive_features": False,
            "expert_notes_in_predictive_features": False,
        },
    }
    if forbidden_hits:
        summary["forbidden_inputs_used"] = forbidden_hits
    return {"records": records, "summary": summary}


def write_active_site_encoder_cache(
    *,
    readiness_matrix_path: Path,
    geometry_features_path: Path,
    out_path: Path,
    summary_path: Path,
    report_path: Path | None = None,
    include_rows: list[str] | None = None,
    max_rows: int | None = None,
) -> dict[str, Any]:
    with readiness_matrix_path.open("r", encoding="utf-8") as handle:
        readiness_matrix = json.load(handle)
    with geometry_features_path.open("r", encoding="utf-8") as handle:
        geometry_features = json.load(handle)
    cache = build_active_site_encoder_cache(
        readiness_matrix=readiness_matrix,
        geometry_features=geometry_features,
        include_rows=include_rows,
        max_rows=max_rows,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for record in cache["records"]:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(cache["summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_markdown_report(cache["summary"]), encoding="utf-8")
    return cache["summary"]


def _cache_record(readiness_row: dict[str, Any], geometry_entry: dict[str, Any]) -> dict[str, Any]:
    residues = [
        residue
        for residue in geometry_entry.get("residues", [])
        if isinstance(residue, dict)
    ]
    node_id_to_index = {
        str(residue.get("residue_node_id")): index
        for index, residue in enumerate(residues)
        if residue.get("residue_node_id")
    }
    center = _coordinate_center(residues)
    nodes = [_node_features(index, residue, center) for index, residue in enumerate(residues)]
    edges = [
        _edge_features(edge, node_id_to_index)
        for edge in geometry_entry.get("pairwise_distances_angstrom", [])
        if isinstance(edge, dict)
    ]
    edges = [edge for edge in edges if edge is not None]

    ligand_context = geometry_entry.get("ligand_context", {}) or {}
    pocket_context = geometry_entry.get("pocket_context", {}) or {}
    predictive_features = {
        "schema_version": "active_site_predictive_features.v1",
        "active_site_residue_count": int(geometry_entry.get("residue_count") or 0),
        "resolved_residue_count": int(geometry_entry.get("resolved_residue_count") or 0),
        "role_annotated_residue_count": int(
            readiness_row.get("role_annotated_residue_count") or 0
        ),
        "missing_position_count": int(geometry_entry.get("missing_positions") or 0),
        "pairwise_edge_count": len(edges),
        "pocket_descriptor_available": bool(readiness_row.get("pocket_descriptor_available")),
        "local_cofactor_family_available": bool(
            readiness_row.get("local_cofactor_family_available")
        ),
        "structure_cofactor_family_available": bool(
            readiness_row.get("structure_cofactor_family_available")
        ),
        "coordinate_availability": _coordinate_availability(readiness_row),
        "residue_type_counts": dict(
            sorted(Counter(_residue_code(residue) for residue in residues).items())
        ),
        "role_counts": _role_counts(residues),
        "distance_summary": _distance_summary(edges),
        "distance_bin_counts": _distance_bin_counts(edges),
        "pocket_descriptors": _pocket_descriptors(pocket_context),
        "cofactor_family_presence": sorted(
            str(family)
            for family in ligand_context.get("cofactor_families", [])
            if family
        ),
        "structure_cofactor_family_presence": sorted(
            str(family)
            for family in ligand_context.get("structure_cofactor_families", [])
            if family
        ),
        "proximal_ligand_summary": _proximal_ligand_summary(ligand_context),
        "nodes": nodes,
        "edges": edges,
    }
    return {
        "schema_version": "active_site_encoder_cache_row.v1",
        "metadata": {
            "entry_id": readiness_row.get("candidate_id"),
            "split_assignment": readiness_row.get("split_assignment"),
            "source_group": readiness_row.get("source_group"),
            "selected_structure": readiness_row.get("selected_structure"),
            "coordinate_path": readiness_row.get("coordinate_path"),
            "current_fingerprint_id": readiness_row.get("current_fingerprint_id"),
            "allowed_use": readiness_row.get("allowed_use"),
        },
        "predictive_features": predictive_features,
        "feature_masks": {
            "ca_present_count": sum(1 for node in nodes if node["ca_present"]),
            "centroid_present_count": sum(1 for node in nodes if node["centroid_present"]),
            "edge_count": len(edges),
            "has_pocket_descriptors": bool(predictive_features["pocket_descriptors"]),
            "has_local_cofactor_family": bool(
                predictive_features["cofactor_family_presence"]
            ),
        },
        "forbidden_inputs_used": [],
    }


def _node_features(index: int, residue: dict[str, Any], center: dict[str, float]) -> dict[str, Any]:
    ca = residue.get("ca") if isinstance(residue.get("ca"), dict) else None
    centroid = (
        residue.get("centroid") if isinstance(residue.get("centroid"), dict) else None
    )
    coordinate = ca or centroid
    return {
        "node_index": index,
        "residue_type": _residue_code(residue),
        "roles": sorted(str(role) for role in residue.get("roles", []) if role),
        "atom_count_clipped": min(int(residue.get("atom_count") or 0), 40),
        "relative_active_site_index_bucket": _index_bucket(index),
        "ca_present": ca is not None,
        "centroid_present": centroid is not None,
        "relative_coordinate": _relative_coordinate(coordinate, center),
    }


def _edge_features(
    edge: dict[str, Any], node_id_to_index: dict[str, int]
) -> dict[str, Any] | None:
    left = node_id_to_index.get(str(edge.get("left")))
    right = node_id_to_index.get(str(edge.get("right")))
    if left is None or right is None:
        return None
    distance = max(0.0, min(float(edge.get("distance") or 0.0), 40.0))
    return {
        "left_node_index": left,
        "right_node_index": right,
        "distance_angstrom_clipped_0_40": round(distance, 3),
        "distance_bin": _distance_bin(distance),
        "coordinate_type": str(edge.get("coordinate_type") or "unknown"),
    }


def _coordinate_center(residues: list[dict[str, Any]]) -> dict[str, float]:
    coordinates = []
    for residue in residues:
        coordinate = residue.get("ca") or residue.get("centroid")
        if isinstance(coordinate, dict):
            coordinates.append(coordinate)
    if not coordinates:
        return {"x": 0.0, "y": 0.0, "z": 0.0}
    return {
        axis: mean(float(coordinate.get(axis) or 0.0) for coordinate in coordinates)
        for axis in ("x", "y", "z")
    }


def _relative_coordinate(
    coordinate: dict[str, Any] | None, center: dict[str, float]
) -> dict[str, float] | None:
    if coordinate is None:
        return None
    return {
        axis: round(float(coordinate.get(axis) or 0.0) - center[axis], 4)
        for axis in ("x", "y", "z")
    }


def _residue_code(residue: dict[str, Any]) -> str:
    return str(residue.get("code") or "UNK").upper()


def _index_bucket(index: int) -> str:
    if index < 5:
        return "0_4"
    if index < 10:
        return "5_9"
    if index < 20:
        return "10_19"
    return "20_plus"


def _role_counts(residues: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for residue in residues:
        counts.update(str(role) for role in residue.get("roles", []) if role)
    return dict(sorted(counts.items()))


def _distance_summary(edges: list[dict[str, Any]]) -> dict[str, float | int | None]:
    distances = [float(edge["distance_angstrom_clipped_0_40"]) for edge in edges]
    if not distances:
        return {"count": 0, "min": None, "mean": None, "max": None}
    return {
        "count": len(distances),
        "min": round(min(distances), 3),
        "mean": round(mean(distances), 3),
        "max": round(max(distances), 3),
    }


def _distance_bin_counts(edges: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(edge["distance_bin"]) for edge in edges)
    return dict(sorted(counts.items()))


def _distance_bin(distance: float) -> str:
    for low, high in zip(DISTANCE_BINS_ANGSTROM, DISTANCE_BINS_ANGSTROM[1:]):
        if low <= distance < high:
            return f"{_fmt_bin(low)}_{_fmt_bin(high)}"
    return "40_plus"


def _fmt_bin(value: float) -> str:
    text = str(value).replace(".", "_")
    return text[:-2] if text.endswith("_0") else text


def _pocket_descriptors(pocket_context: dict[str, Any]) -> dict[str, float]:
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        return {}
    allowed = [
        "hydrophobic_fraction",
        "polar_fraction",
        "positive_fraction",
        "negative_fraction",
        "charge_balance",
        "aromatic_fraction",
        "sulfur_fraction",
        "mean_min_distance_to_active_site",
    ]
    return {
        key: round(float(descriptors[key]), 4)
        for key in allowed
        if descriptors.get(key) is not None
    }


def _proximal_ligand_summary(ligand_context: dict[str, Any]) -> dict[str, float | int | None]:
    ligands = [
        ligand
        for ligand in ligand_context.get("proximal_ligands", [])
        if isinstance(ligand, dict)
    ]
    distances = [
        float(ligand["min_distance_to_active_site"])
        for ligand in ligands
        if ligand.get("min_distance_to_active_site") is not None
    ]
    return {
        "proximal_ligand_count": len(ligands),
        "min_any_ligand_distance_angstrom": (
            round(min(distances), 3) if distances else None
        ),
        "mean_any_ligand_distance_angstrom": (
            round(mean(distances), 3) if distances else None
        ),
    }


def _coordinate_availability(readiness_row: dict[str, Any]) -> dict[str, bool]:
    status = str(readiness_row.get("coordinate_status") or "")
    return {
        "local_coordinate_available": status in {"already_materialized", "materialized"},
        "selected_structure_supported": bool(readiness_row.get("selected_structure")),
    }


def _forbidden_predictive_key_hits(payload: Any, prefix: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_path = f"{prefix}.{key}" if prefix else str(key)
            lowered = str(key).lower()
            for fragment in FORBIDDEN_PREDICTIVE_KEY_FRAGMENTS:
                if fragment in lowered:
                    hits.append(key_path)
                    break
            hits.extend(_forbidden_predictive_key_hits(value, key_path))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            hits.extend(_forbidden_predictive_key_hits(value, f"{prefix}[{index}]"))
    return hits


def _markdown_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Active-site encoder cache smoke",
            "",
            f"- Emitted rows: {summary['emitted_row_count']}",
            f"- Requested rows: {summary['requested_row_count']}",
            f"- Skipped rows: {len(summary['skipped_rows'])}",
            f"- Forbidden predictive key hits: {len(summary['predictive_feature_forbidden_key_hits'])}",
            f"- Training executed: {summary['training_executed']}",
            f"- Label registry changed: {summary['label_registry_changed']}",
            "",
        ]
    )


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
