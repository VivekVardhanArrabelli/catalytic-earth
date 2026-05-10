from __future__ import annotations

from collections import Counter
from typing import Any

from .labels import COUNTABLE_REVIEW_STATUSES, MechanismLabel
from .ontology import fingerprint_family


def build_learned_retrieval_manifest(
    geometry: dict[str, Any],
    retrieval: dict[str, Any],
    labels: list[MechanismLabel],
    *,
    ontology_gap_audit: dict[str, Any] | None = None,
    max_rows: int = 0,
) -> dict[str, Any]:
    """Build a representation-learning interface while preserving heuristic controls."""
    labels_by_entry = {label.entry_id: label for label in labels}
    retrieval_by_entry = {
        str(row.get("entry_id")): row
        for row in retrieval.get("results", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }
    ontology_gap_by_entry = {
        str(row.get("entry_id")): row
        for row in (ontology_gap_audit or {}).get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }

    rows: list[dict[str, Any]] = []
    for geometry_row in geometry.get("entries", []):
        if not isinstance(geometry_row, dict) or not isinstance(
            geometry_row.get("entry_id"), str
        ):
            continue
        entry_id = str(geometry_row["entry_id"])
        label = labels_by_entry.get(entry_id)
        if label is None:
            continue
        retrieval_row = retrieval_by_entry.get(entry_id, {})
        top_fingerprints = retrieval_row.get("top_fingerprints", [])
        if not isinstance(top_fingerprints, list):
            top_fingerprints = []
        top1 = top_fingerprints[0] if top_fingerprints else {}
        if not isinstance(top1, dict):
            top1 = {}
        residue_codes = [
            str(residue.get("code", "")).upper()
            for residue in geometry_row.get("residues", [])
            if isinstance(residue, dict) and residue.get("code")
        ]
        ligand_context = geometry_row.get("ligand_context", {})
        if not isinstance(ligand_context, dict):
            ligand_context = {}
        pocket_context = geometry_row.get("pocket_context", {})
        if not isinstance(pocket_context, dict):
            pocket_context = {}
        pocket_descriptors = pocket_context.get("descriptors", {})
        if not isinstance(pocket_descriptors, dict):
            pocket_descriptors = {}
        ontology_gap = ontology_gap_by_entry.get(entry_id, {})
        eligible = (
            geometry_row.get("status") == "ok"
            and label.review_status in COUNTABLE_REVIEW_STATUSES
            and int(geometry_row.get("resolved_residue_count", 0) or 0) >= 3
        )
        rows.append(
            {
                "entry_id": entry_id,
                "entry_name": geometry_row.get("entry_name"),
                "label_type": label.label_type,
                "fingerprint_id": label.fingerprint_id,
                "ontology_family": fingerprint_family(label.fingerprint_id)
                if label.fingerprint_id
                else None,
                "review_status": label.review_status,
                "tier": label.tier,
                "eligible_for_learned_retrieval": eligible,
                "eligibility_blockers": _learned_manifest_blockers(
                    geometry_row,
                    label,
                ),
                "heuristic_baseline_control": {
                    "top1_fingerprint_id": top1.get("fingerprint_id"),
                    "top1_score": top1.get("score"),
                    "retrieval_status": retrieval_row.get("status"),
                },
                "feature_summary": {
                    "pdb_id": geometry_row.get("pdb_id"),
                    "resolved_residue_count": geometry_row.get(
                        "resolved_residue_count"
                    ),
                    "residue_codes": residue_codes,
                    "pairwise_distance_count": len(
                        geometry_row.get("pairwise_distances_angstrom", [])
                    ),
                    "local_cofactor_families": ligand_context.get(
                        "cofactor_families", []
                    ),
                    "structure_cofactor_families": ligand_context.get(
                        "structure_cofactor_families", []
                    ),
                    "pocket_descriptor_names": sorted(pocket_descriptors),
                },
                "ontology_gap_scope_signals": ontology_gap.get("scope_signals", []),
                "embedding_status": "not_computed_interface_only",
                "countable_training_label": eligible,
            }
        )

    rows = sorted(
        rows,
        key=lambda row: (
            0 if row["eligible_for_learned_retrieval"] else 1,
            str(row["label_type"]),
            str(row["entry_id"]),
        ),
    )
    emitted_rows = rows if max_rows <= 0 else rows[:max_rows]
    eligible_rows = [row for row in rows if row["eligible_for_learned_retrieval"]]
    label_type_counts = Counter(str(row["label_type"]) for row in rows)
    family_counts = Counter(
        str(row["ontology_family"])
        for row in eligible_rows
        if row.get("ontology_family")
    )
    return {
        "metadata": {
            "method": "learned_retrieval_manifest",
            "source_geometry_method": geometry.get("metadata", {}).get("artifact"),
            "source_retrieval_method": retrieval.get("metadata", {}).get("method"),
            "labeled_entry_count": len(rows),
            "eligible_entry_count": len(eligible_rows),
            "ineligible_entry_count": len(rows) - len(eligible_rows),
            "emitted_row_count": len(emitted_rows),
            "omitted_by_max_rows": max(0, len(rows) - len(emitted_rows)),
            "max_rows": max_rows,
            "label_type_counts": dict(sorted(label_type_counts.items())),
            "eligible_ontology_family_counts": dict(sorted(family_counts.items())),
            "embedding_status": "not_computed_interface_only",
            "control_rule": (
                "learned retrieval candidates must be compared against the "
                "current heuristic geometry retrieval baseline"
            ),
            "training_label_rule": (
                "only countable automation_curated or expert_reviewed labels with "
                "resolved local geometry are eligible; review-only rows are excluded"
            ),
        },
        "rows": emitted_rows,
    }


def _learned_manifest_blockers(
    geometry_row: dict[str, Any],
    label: MechanismLabel,
) -> list[str]:
    blockers: list[str] = []
    if geometry_row.get("status") != "ok":
        blockers.append("geometry_status_not_ok")
    if int(geometry_row.get("resolved_residue_count", 0) or 0) < 3:
        blockers.append("fewer_than_three_resolved_residues")
    if label.review_status not in COUNTABLE_REVIEW_STATUSES:
        blockers.append("label_not_countable_review_status")
    return blockers
