"""Run the silver geometry-confirmation gate on materialized silver-ready rows.

The preceding silver audit only answers whether a row is runnable. This module
uses those runnable rows to build local geometry features from sha-matched holo
PDB coordinates and explicit PDB residue mappings, then reuses the existing
geometry retrieval + label-factory promotion rule. It writes only the external
registry on an explicit apply.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .bronze_silver_promotion_preview import DEFAULT_EXPANSION_REGISTRY_PATH
from .geometry_retrieval import run_geometry_retrieval
from .labels import MechanismLabel, build_label_factory_audit
from .mechanism_representation_loop import (
    DEFAULT_FROZEN_BENCHMARK_PATH,
    DEFAULT_PROMOTION_COHESION,
)
from .registry_io import load_json, write_registry_payload
from .silver_geometry_confirmation import build_silver_geometry_confirmation_audit
from .structure import (
    atom_position,
    ligand_context_from_atoms,
    pairwise_distances,
    parse_atom_site_loop,
    pocket_context_from_atoms,
    residue_centroid,
    select_residue_atoms,
)

ARTIFACT_ID = "v3_silver_geometry_confirmation_run_current702"
SCHEMA_VERSION = "silver_geometry_confirmation_run.v1"
DEFAULT_OUT = Path("artifacts/v3_silver_geometry_confirmation_run_current702.json")
DEFAULT_REPORT = Path("work/silver_geometry_confirmation_run_current702.md")
DEFAULT_GEOMETRY_ABSTAIN_THRESHOLD = 0.4115
GEOMETRY_CONFIRMATION_SOURCE = "silver_geometry_confirmation_run"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _entry_id_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = entry_id.partition(":")
    try:
        numeric = int(suffix)
    except ValueError:
        numeric = 0
    return (prefix, numeric, entry_id)


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("structure_provenance") or {}


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("mechanism_evidence") or {}


def _holo_confirmation(row: dict[str, Any]) -> dict[str, Any]:
    confirmation = _structure_provenance(row).get("holo_pdb_confirmation") or {}
    return confirmation if isinstance(confirmation, dict) else {}


def _coordinate_path(row: dict[str, Any]) -> Path | None:
    raw = _structure_provenance(row).get("coordinate_path")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.exists() else None


def _active_site_residues(row: dict[str, Any]) -> list[dict[str, Any]]:
    residues = _mechanism_evidence(row).get("active_site_residues") or []
    return [residue for residue in residues if isinstance(residue, dict)]


def _mapped_structure_positions(row: dict[str, Any], *, pdb_id: str) -> list[dict[str, Any]]:
    positions: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for residue in _active_site_residues(row):
        if residue.get("exact") is not True:
            continue
        for position in residue.get("structure_positions") or []:
            if not isinstance(position, dict):
                continue
            if str(position.get("pdb_id") or "").upper() != pdb_id:
                continue
            key = (
                pdb_id,
                str(position.get("chain_name") or ""),
                str(position.get("resid") or ""),
                str(position.get("code") or "").upper(),
            )
            if key in seen:
                continue
            seen.add(key)
            positions.append(position)
    return positions


def _empty_ligand_context() -> dict[str, Any]:
    return {
        "distance_cutoff_angstrom": 6.0,
        "proximal_ligands": [],
        "ligand_codes": [],
        "cofactor_families": [],
        "structure_ligands": [],
        "structure_ligand_codes": [],
        "structure_cofactor_families": [],
    }


def _empty_pocket_context() -> dict[str, Any]:
    return {
        "distance_cutoff_angstrom": 8.0,
        "nearby_residue_count": 0,
        "nearby_residue_sites": [],
        "residue_code_counts": {},
        "descriptors": {
            "hydrophobic_fraction": 0.0,
            "polar_fraction": 0.0,
            "positive_fraction": 0.0,
            "negative_fraction": 0.0,
            "aromatic_fraction": 0.0,
            "sulfur_fraction": 0.0,
            "charge_balance": 0.0,
            "mean_min_distance_to_active_site": 0.0,
        },
    }


def _geometry_feature_for_row(row: dict[str, Any], runnability_row: dict[str, Any]) -> dict[str, Any]:
    entry_id = str(row.get("entry_id") or "")
    confirmation = _holo_confirmation(row)
    pdb_id = str(confirmation.get("pdb_id") or "").upper()
    coordinate = _coordinate_path(row)
    base = {
        "entry_id": entry_id,
        "entry_name": None,
        "pdb_id": pdb_id or None,
        "mechanism_text_count": 0,
        "mechanism_text_snippets": [],
        "coordinate_path": str(coordinate) if coordinate else None,
        "coordinate_sha256": runnability_row.get("local_coordinate_sha256"),
        "holo_confirmation_coordinate_sha256": runnability_row.get(
            "holo_confirmation_coordinate_sha256"
        ),
        "source_annotation_roles_used_for_score": False,
        "residue_roles_source": "not_used_for_scoring",
    }
    if coordinate is None:
        return {
            **base,
            "status": "missing_local_holo_coordinate_file",
            "residue_count": 0,
            "resolved_residue_count": 0,
            "missing_positions": 0,
            "residues": [],
            "pairwise_distances_angstrom": [],
            "ligand_context": _empty_ligand_context(),
            "pocket_context": _empty_pocket_context(),
        }
    expected_sha = confirmation.get("coordinate_sha256")
    actual_sha = _sha256_path(coordinate)
    if expected_sha and actual_sha != expected_sha:
        return {
            **base,
            "coordinate_sha256": actual_sha,
            "status": "local_coordinate_sha_mismatch_holo_confirmation",
            "residue_count": 0,
            "resolved_residue_count": 0,
            "missing_positions": 0,
            "residues": [],
            "pairwise_distances_angstrom": [],
            "ligand_context": _empty_ligand_context(),
            "pocket_context": _empty_pocket_context(),
        }

    positions = _mapped_structure_positions(row, pdb_id=pdb_id)
    try:
        atoms = parse_atom_site_loop(coordinate.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return {
            **base,
            "coordinate_sha256": actual_sha,
            "status": "structure_parse_failed",
            "error": str(exc),
            "residue_count": len(positions),
            "resolved_residue_count": 0,
            "missing_positions": len(positions),
            "residues": [],
            "pairwise_distances_angstrom": [],
            "ligand_context": _empty_ligand_context(),
            "pocket_context": _empty_pocket_context(),
        }

    resolved: list[dict[str, Any]] = []
    missing_positions: list[dict[str, Any]] = []
    for position in positions:
        residue_atoms = select_residue_atoms(
            atoms,
            chain_name=position.get("chain_name"),
            resid=position.get("resid"),
            code=position.get("code"),
        )
        residue_record = {
            "residue_node_id": (
                f"{entry_id}:{pdb_id}:{position.get('chain_name')}:{position.get('resid')}"
            ),
            "code": str(position.get("code") or "").upper(),
            "chain_name": position.get("chain_name"),
            "resid": str(position.get("resid") or ""),
            # UniProt active-site roles/binding-site prose are admission context, not
            # predictive geometry features for this confirmation run.
            "roles": [],
            "mapping_source": position.get("mapping_source"),
            "uniprot_position": position.get("uniprot_position"),
        }
        if not residue_atoms:
            missing_positions.append(residue_record)
            continue
        residue_record.update(
            {
                "atom_count": len(residue_atoms),
                "centroid": residue_centroid(residue_atoms),
                "ca": atom_position(residue_atoms, "CA"),
            }
        )
        resolved.append(residue_record)

    distances = pairwise_distances(resolved)
    status = "ok" if len(resolved) >= 2 and distances else "insufficient_resolved_residues"
    return {
        **base,
        "coordinate_sha256": actual_sha,
        "status": status,
        "residue_count": len(positions),
        "resolved_residue_count": len(resolved),
        "missing_positions": len(missing_positions),
        "missing_position_details": missing_positions,
        "residues": resolved,
        "pairwise_distances_angstrom": distances,
        "ligand_context": ligand_context_from_atoms(atoms, resolved),
        "pocket_context": pocket_context_from_atoms(atoms, resolved),
    }


def _feature_summary(feature: dict[str, Any]) -> dict[str, Any]:
    ligand_context = feature.get("ligand_context") or {}
    return {
        "status": feature.get("status"),
        "pdb_id": feature.get("pdb_id"),
        "coordinate_path": feature.get("coordinate_path"),
        "coordinate_sha256": feature.get("coordinate_sha256"),
        "holo_confirmation_coordinate_sha256": feature.get(
            "holo_confirmation_coordinate_sha256"
        ),
        "resolved_residue_count": feature.get("resolved_residue_count"),
        "missing_positions": feature.get("missing_positions"),
        "pairwise_distance_count": len(feature.get("pairwise_distances_angstrom") or []),
        "proximal_ligand_codes": ligand_context.get("ligand_codes", []),
        "proximal_cofactor_families": ligand_context.get("cofactor_families", []),
        "structure_ligand_codes": ligand_context.get("structure_ligand_codes", []),
        "structure_cofactor_families": ligand_context.get("structure_cofactor_families", []),
        "source_annotation_roles_used_for_score": feature.get(
            "source_annotation_roles_used_for_score"
        ),
    }


def _top_hit(result: dict[str, Any], fingerprint_id: str | None) -> tuple[int | None, dict[str, Any] | None]:
    for rank, hit in enumerate(result.get("top_fingerprints") or [], start=1):
        if hit.get("fingerprint_id") == fingerprint_id:
            return rank, hit
    return None, None


def _confirmation_rows(
    *,
    runnability_rows: list[dict[str, Any]],
    geometry_features: list[dict[str, Any]],
    retrieval: dict[str, Any],
    label_factory_audit: dict[str, Any],
) -> list[dict[str, Any]]:
    features_by_entry = {feature["entry_id"]: feature for feature in geometry_features}
    retrieval_by_entry = {row.get("entry_id"): row for row in retrieval.get("results", [])}
    factory_by_entry = {
        row.get("entry_id"): row for row in label_factory_audit.get("rows", [])
    }
    rows: list[dict[str, Any]] = []
    for runnable in sorted(runnability_rows, key=lambda row: _entry_id_sort_key(str(row["entry_id"]))):
        entry_id = str(runnable["entry_id"])
        feature = features_by_entry.get(entry_id, {})
        result = retrieval_by_entry.get(entry_id, {})
        factory = factory_by_entry.get(entry_id, {})
        top = result.get("top_fingerprints") or []
        top1 = top[0] if top else {}
        target_rank, target_hit = _top_hit(result, runnable.get("fingerprint_id"))
        action = str(factory.get("recommended_action") or "not_evaluated")
        decision = (
            "pass_geometry_confirmation"
            if action == "promote_to_silver" and feature.get("status") == "ok"
            else "hold_geometry_confirmation"
        )
        blockers: list[str] = []
        if feature.get("status") != "ok":
            blockers.append(f"geometry_feature_status:{feature.get('status')}")
        if action != "promote_to_silver":
            blockers.append(f"label_factory_action:{action}")
        for conflict in factory.get("evidence_conflicts") or []:
            blockers.append(f"label_factory_conflict:{conflict}")
        rows.append(
            {
                "entry_id": entry_id,
                "fingerprint_id": runnable.get("fingerprint_id"),
                "current_tier": runnable.get("tier"),
                "decision": decision,
                "blockers": blockers,
                "proposed_tier": "silver" if decision == "pass_geometry_confirmation" else runnable.get("tier"),
                "tier_changed": False,
                "geometry_status": feature.get("status"),
                "geometry_evidence": _feature_summary(feature),
                "holo_evidence": {
                    "holo_pdb_id": runnable.get("holo_pdb_id"),
                    "cofactor_comp_ids_present": runnable.get("cofactor_comp_ids_present", []),
                    "coordinate_sha256_matches_holo_confirmation": runnable.get(
                        "coordinate_sha256_matches_holo_confirmation"
                    ),
                    "explicit_structure_position_count": runnable.get(
                        "explicit_structure_position_count"
                    ),
                    "exact_active_site_residue_count": runnable.get(
                        "exact_active_site_residue_count"
                    ),
                },
                "retrieval": {
                    "top1_fingerprint_id": top1.get("fingerprint_id"),
                    "top1_score": top1.get("score"),
                    "target_rank": target_rank,
                    "target_score": target_hit.get("score") if target_hit else None,
                    "target_cofactor_evidence_level": (
                        target_hit.get("cofactor_evidence_level") if target_hit else None
                    ),
                    "top_fingerprints": top[:5],
                },
                "label_factory": {
                    "recommended_action": action,
                    "proposed_tier": factory.get("proposed_tier"),
                    "factory_evidence_score": factory.get("factory_evidence_score"),
                    "evidence_conflicts": factory.get("evidence_conflicts", []),
                    "cofactor_coverage_status": factory.get("cofactor_coverage_status"),
                    "expected_cofactor_families": factory.get("expected_cofactor_families", []),
                },
            }
        )
    return rows


def build_silver_geometry_confirmation_run(
    expansion_payload: list[dict[str, Any]],
    *,
    created_utc: str | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    min_exact_residues: int = 2,
    abstain_threshold: float = DEFAULT_GEOMETRY_ABSTAIN_THRESHOLD,
) -> dict[str, Any]:
    """Build a non-destructive silver geometry-confirmation run artifact."""
    created = created_utc or _utc_now_iso()
    runnability = build_silver_geometry_confirmation_audit(
        expansion_payload,
        created_utc=created,
        cohesion_threshold=cohesion_threshold,
        min_exact_residues=min_exact_residues,
    )
    rows_by_entry = {
        row.get("entry_id"): row
        for row in expansion_payload
        if isinstance(row, dict) and row.get("entry_id")
    }
    runnable_rows = [
        row
        for row in runnability.get("rows", [])
        if row.get("decision") == "ready_for_geometry_confirmation_run"
        and row.get("entry_id") in rows_by_entry
    ]
    geometry_features = [
        _geometry_feature_for_row(rows_by_entry[row["entry_id"]], row)
        for row in sorted(runnable_rows, key=lambda item: _entry_id_sort_key(str(item["entry_id"])))
    ]
    retrieval = run_geometry_retrieval({"entries": geometry_features}) if geometry_features else {
        "metadata": {
            "method": "geometry_aware_seed_fingerprint_retrieval",
            "entry_count": 0,
            "text_or_label_fields_used_for_score": False,
        },
        "results": [],
    }
    labels = [MechanismLabel.from_dict(rows_by_entry[row["entry_id"]]) for row in runnable_rows]
    label_factory_audit = build_label_factory_audit(
        retrieval,
        labels,
        abstain_threshold=abstain_threshold,
    )
    rows = _confirmation_rows(
        runnability_rows=runnable_rows,
        geometry_features=geometry_features,
        retrieval=retrieval,
        label_factory_audit=label_factory_audit,
    )
    decision_counts = Counter(row["decision"] for row in rows)
    by_fingerprint: dict[str, Counter[str]] = {}
    for row in rows:
        by_fingerprint.setdefault(str(row.get("fingerprint_id") or "__missing__"), Counter())[
            str(row["decision"])
        ] += 1
    geometry_status_counts = Counter(str(row.get("geometry_status")) for row in rows)
    source_roles_used = any(
        feature.get("source_annotation_roles_used_for_score") is not False
        for feature in geometry_features
    )
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "Run the separate silver geometry-confirmation gate on rows that already "
            "passed silver-ready chemistry/holo materialization and explicit PDB "
            "residue-mapping gates."
        ),
        "policy": {
            "silver_ready_source": "bronze_silver_promotion_preview",
            "runnability_gate": "silver_geometry_confirmation_audit",
            "geometry_retrieval_gate": "geometry_aware_seed_fingerprint_retrieval",
            "promotion_gate": "label_factory_promotion_demotion_audit",
            "cohesion_threshold": cohesion_threshold,
            "min_exact_active_site_residues": min_exact_residues,
            "geometry_abstain_threshold": abstain_threshold,
            "pass_rule": (
                "ready_for_geometry_confirmation_run AND local geometry status ok AND "
                "label_factory recommended_action == promote_to_silver"
            ),
            "source_annotation_roles_used_for_score": False,
            "uniprot_binding_site_prose_used_for_score": False,
            "ec_rhea_name_or_source_prose_used_for_score": False,
            "registry_apply_requires_explicit_apply": True,
        },
        "guardrails": {
            "registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "tier_changed": False,
            "geometry_confirmation_run_or_faked": False,
            "annotation_only_silver_promotion": False,
            "predictive_evidence_changed": False,
            "source_annotation_roles_used_for_score": source_roles_used,
            "text_or_label_fields_used_for_score": False,
        },
        "counts": {
            "expansion_rows": len(expansion_payload),
            "silver_ready_input_rows": runnability["counts"]["silver_ready_input_rows"],
            "ready_for_geometry_confirmation_run": len(runnable_rows),
            "blocked_before_geometry_confirmation": runnability["counts"][
                "blocked_before_geometry_confirmation"
            ],
            "geometry_rows_scored": len(geometry_features),
            "geometry_rows_ok": int(geometry_status_counts.get("ok", 0)),
            "pass_geometry_confirmation": int(
                decision_counts.get("pass_geometry_confirmation", 0)
            ),
            "hold_geometry_confirmation": int(
                decision_counts.get("hold_geometry_confirmation", 0)
            ),
            "silver_flip_candidates": int(
                decision_counts.get("pass_geometry_confirmation", 0)
            ),
            "silver_flips_applied": 0,
        },
        "runnability_blocker_counts": runnability.get("blocker_counts", {}),
        "geometry_status_counts": dict(sorted(geometry_status_counts.items())),
        "label_factory_metadata": label_factory_audit.get("metadata", {}),
        "decision_counts": dict(sorted(decision_counts.items())),
        "decision_counts_by_fingerprint": {
            fp: dict(sorted(counter.items())) for fp, counter in sorted(by_fingerprint.items())
        },
        "silver_ready_input_entry_ids": sorted(
            (row["entry_id"] for row in runnability.get("rows", [])),
            key=_entry_id_sort_key,
        ),
        "ready_entry_ids": sorted((row["entry_id"] for row in runnable_rows), key=_entry_id_sort_key),
        "pass_entry_ids": sorted(
            (row["entry_id"] for row in rows if row["decision"] == "pass_geometry_confirmation"),
            key=_entry_id_sort_key,
        ),
        "hold_entry_ids": sorted(
            (row["entry_id"] for row in rows if row["decision"] == "hold_geometry_confirmation"),
            key=_entry_id_sort_key,
        ),
        "retrieval_metadata": retrieval.get("metadata", {}),
        "rows": rows,
    }


def summarize_confirmation_run(audit: dict[str, Any]) -> dict[str, Any]:
    return dict(audit)


def _honest_counters(
    *,
    frozen_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
) -> dict[str, int]:
    combined = [*frozen_payload, *expansion_payload]
    return {
        "external_rows": len(expansion_payload),
        "positive_bronze": sum(
            1
            for row in combined
            if row.get("label_type") == "seed_fingerprint" and row.get("tier") == "bronze"
        ),
        "oos_bronze": sum(
            1
            for row in combined
            if row.get("label_type") == "out_of_scope" and row.get("tier") == "bronze"
        ),
        "silver_ready": sum(1 for row in combined if row.get("tier") == "silver_ready"),
        "silver_confirmed": sum(
            1 for row in combined if row.get("tier") in {"silver", "silver_confirmed"}
        ),
        "projected": sum(
            1
            for row in combined
            if row.get("tier") in {"projected", "provisional", "hypothesis"}
        ),
        "combined_label_surface": len(combined),
        "combined_seed_surface": sum(
            1 for row in combined if row.get("label_type") == "seed_fingerprint"
        ),
    }


def _append_unique(values: list[Any], value: str) -> list[Any]:
    out = list(values) if isinstance(values, list) else []
    if value not in out:
        out.append(value)
    return out


def _updated_registry_with_silver_flips(
    expansion_payload: list[dict[str, Any]],
    audit: dict[str, Any],
    *,
    created_utc: str,
) -> list[dict[str, Any]]:
    rows_by_entry = {row["entry_id"]: row for row in audit.get("rows", [])}
    pass_ids = {
        row["entry_id"]
        for row in audit.get("rows", [])
        if row.get("decision") == "pass_geometry_confirmation"
    }
    updated: list[dict[str, Any]] = []
    for row in expansion_payload:
        entry_id = row.get("entry_id")
        if entry_id not in pass_ids:
            updated.append(json.loads(json.dumps(row)))
            continue
        audit_row = rows_by_entry[str(entry_id)]
        record = json.loads(json.dumps(row))
        record["tier"] = "silver"
        record["evidence_score"] = max(
            float(record.get("evidence_score", 0.0) or 0.0),
            float(audit_row.get("label_factory", {}).get("factory_evidence_score", 0.0) or 0.0),
        )
        evidence = record.setdefault("evidence", {})
        evidence["sources"] = _append_unique(evidence.get("sources", []), GEOMETRY_CONFIRMATION_SOURCE)
        evidence["notes"] = _append_unique(
            evidence.get("notes", []),
            "silver tier earned by local holo geometry confirmation; annotation-only promotion is not used",
        )
        pending = evidence.get("pending_promotion_audits")
        if isinstance(pending, list):
            evidence["pending_promotion_audits"] = [
                item
                for item in pending
                if item
                != "geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure"
            ]
        structure = evidence.setdefault("structure_provenance", {})
        structure["silver_geometry_confirmation"] = {
            "status": "silver_geometry_confirmed_local_holo_pdb",
            "artifact_id": ARTIFACT_ID,
            "schema_version": SCHEMA_VERSION,
            "confirmed_utc": created_utc,
            "pdb_id": audit_row["geometry_evidence"]["pdb_id"],
            "coordinate_path": audit_row["geometry_evidence"]["coordinate_path"],
            "coordinate_sha256": audit_row["geometry_evidence"]["coordinate_sha256"],
            "holo_confirmation_coordinate_sha256": audit_row["geometry_evidence"][
                "holo_confirmation_coordinate_sha256"
            ],
            "resolved_residue_count": audit_row["geometry_evidence"][
                "resolved_residue_count"
            ],
            "explicit_structure_position_count": audit_row["holo_evidence"][
                "explicit_structure_position_count"
            ],
            "top1_fingerprint_id": audit_row["retrieval"]["top1_fingerprint_id"],
            "top1_score": audit_row["retrieval"]["top1_score"],
            "target_fingerprint_id": audit_row["fingerprint_id"],
            "target_score": audit_row["retrieval"]["target_score"],
            "factory_evidence_score": audit_row["label_factory"][
                "factory_evidence_score"
            ],
            "cofactor_coverage_status": audit_row["label_factory"][
                "cofactor_coverage_status"
            ],
            "source_annotation_roles_used_for_score": False,
            "ec_rhea_name_or_source_prose_used_for_score": False,
            "predictive_evidence_changed": False,
        }
        updated.append(record)
    return updated


def _mark_applied_rows(audit: dict[str, Any]) -> None:
    for row in audit.get("rows", []):
        if row.get("decision") == "pass_geometry_confirmation":
            row["tier_changed"] = True
            row["applied_tier"] = "silver"


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Silver Geometry Confirmation Run",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Runs the separate geometry-confirmation gate for silver-ready rows that",
        "already have sha-matched holo coordinates and explicit PDB residue mappings.",
        "",
        "## Result",
        "",
        f"- Silver-ready input rows: {c['silver_ready_input_rows']}.",
        f"- Ready/runnable rows scored: {c['ready_for_geometry_confirmation_run']}.",
        f"- Geometry rows OK: {c['geometry_rows_ok']}.",
        f"- Passed geometry confirmation: {c['pass_geometry_confirmation']}.",
        f"- Held by geometry confirmation: {c['hold_geometry_confirmation']}.",
        f"- Silver flips applied: {c['silver_flips_applied']}.",
        "",
        "## Guardrails",
        "",
        f"- Registry written: {audit['guardrails']['registry_written']}.",
        f"- Frozen current702 preserved: {audit['guardrails']['frozen_current702_benchmark_preserved']}.",
        f"- Source annotation roles used for score: {audit['guardrails']['source_annotation_roles_used_for_score']}.",
        f"- Text/name/label fields used for score: {audit['guardrails']['text_or_label_fields_used_for_score']}.",
        "",
        "## Decisions By Fingerprint",
        "",
        "| fingerprint | pass | hold |",
        "| --- | ---: | ---: |",
    ]
    for fp, counts in audit.get("decision_counts_by_fingerprint", {}).items():
        lines.append(
            f"| {fp} | {counts.get('pass_geometry_confirmation', 0)} | "
            f"{counts.get('hold_geometry_confirmation', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "- Continue explicit residue mapping for blocked silver-ready rows and treat",
            "  held geometry rows as calibration/representation gaps unless new local",
            "  structure evidence changes the gate result.",
            "",
        ]
    )
    return "\n".join(lines)


def write_silver_geometry_confirmation_run(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    min_exact_residues: int = 2,
    abstain_threshold: float = DEFAULT_GEOMETRY_ABSTAIN_THRESHOLD,
    apply: bool = False,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError("refusing to write silver flips into the frozen current702 benchmark")

    frozen_sha_before = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )
    expansion_payload = load_json(expansion_path)
    frozen_payload = load_json(frozen_path)
    if not isinstance(expansion_payload, list):
        raise ValueError(f"{expansion_path} must contain a registry list")
    if not isinstance(frozen_payload, list):
        raise ValueError(f"{frozen_path} must contain a registry list")
    created = _utc_now_iso()
    audit = build_silver_geometry_confirmation_run(
        expansion_payload,
        created_utc=created,
        cohesion_threshold=cohesion_threshold,
        min_exact_residues=min_exact_residues,
        abstain_threshold=abstain_threshold,
    )
    audit["frozen_sha256_before"] = frozen_sha_before
    audit["frozen_benchmark_registry_written"] = False
    audit["expansion_registry_written"] = False
    audit["honest_counters_before"] = _honest_counters(
        frozen_payload=frozen_payload,
        expansion_payload=expansion_payload,
    )
    if apply:
        updated = _updated_registry_with_silver_flips(
            expansion_payload,
            audit,
            created_utc=created,
        )
        if len(updated) != len(expansion_payload):
            raise ValueError(
                "row-count guard tripped: updated registry length "
                f"{len(updated)} != input {len(expansion_payload)}"
            )
        before_predictive = {
            row.get("entry_id"): (row.get("evidence") or {}).get("predictive_evidence")
            for row in expansion_payload
        }
        for label in updated:
            MechanismLabel.from_dict(label)
        after_predictive = {
            row.get("entry_id"): (row.get("evidence") or {}).get("predictive_evidence")
            for row in updated
        }
        if before_predictive != after_predictive:
            raise ValueError("predictive_evidence changed during silver geometry apply")
        write_result = write_registry_payload(expansion_path, updated)
        _mark_applied_rows(audit)
        audit["guardrails"]["registry_written"] = True
        audit["guardrails"]["tier_changed"] = bool(audit["pass_entry_ids"])
        audit["counts"]["silver_flips_applied"] = len(audit["pass_entry_ids"])
        audit["expansion_registry_written"] = True
        audit["expansion_registry_path"] = str(expansion_path)
        audit["expansion_registry_storage"] = write_result
        audit["honest_counters_after"] = _honest_counters(
            frozen_payload=frozen_payload,
            expansion_payload=updated,
        )
        audit["silver_confirmed_delta"] = (
            audit["honest_counters_after"]["silver_confirmed"]
            - audit["honest_counters_before"]["silver_confirmed"]
        )
    else:
        audit["honest_counters_after"] = audit["honest_counters_before"]
        audit["silver_confirmed_delta"] = 0

    audit["frozen_sha256_after"] = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )
    audit["frozen_benchmark_byte_unchanged"] = (
        audit["frozen_sha256_before"] == audit["frozen_sha256_after"]
    )
    audit["guardrails"]["frozen_current702_benchmark_preserved"] = audit[
        "frozen_benchmark_byte_unchanged"
    ]

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summarize_confirmation_run(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
