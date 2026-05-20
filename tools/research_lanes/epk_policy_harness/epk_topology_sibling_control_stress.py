#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from epk_fresh_surface_scan import LANE_ID, build_tranche_row, ligand_slug


DEFAULT_GEOMETRY_LEADS = ("9UQ0", "9VLN", "22VT", "9VLW", "9O4E", "10TZ")
SOURCE_FREE_MATCHING_FEATURES = (
    "ligand_code_from_structure",
    "terminal_gamma_atom_name",
    "local_metal_context_review_only",
    "best_any_ser_thr_tyr_gamma_distance_angstrom",
    "best_cross_auth_chain_distance_angstrom",
    "nearest_gamma_metal_distance_angstrom",
    "nonconfounded_inter_auth_chain_within_cutoff",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def relative_path_string(path: str | Path | None, root: Path) -> str:
    if path is None:
        return ""
    value = Path(path)
    try:
        return str(value.relative_to(root))
    except ValueError:
        return str(value)


def numeric(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def distance_delta(a: Any, b: Any, *, missing_penalty: float) -> float:
    left = numeric(a)
    right = numeric(b)
    if left is None or right is None:
        return missing_penalty
    return abs(left - right)


def row_ligand_code(row: dict[str, Any], *, fallback: str) -> str:
    return str(
        row.get("gamma_ligand_code")
        or row.get("_surface_ligand_code")
        or fallback
    ).upper()


def load_surface_rows(surface_paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in surface_paths:
        surface = load_json(path)
        metadata = surface.get("metadata", {})
        artifact_id = str(metadata.get("artifact_id") or path.stem)
        ligand_code = str(metadata.get("ligand_code") or "").upper()
        for row in surface.get("rows", []):
            if not isinstance(row, dict):
                continue
            copied = dict(row)
            copied["_surface_artifact"] = str(path)
            copied["_surface_artifact_id"] = artifact_id
            copied["_surface_ligand_code"] = ligand_code
            rows.append(copied)
    return rows


def source_surface_contexts(surface_paths: list[Path], root: Path) -> list[dict[str, Any]]:
    contexts: list[dict[str, Any]] = []
    for path in surface_paths:
        surface = load_json(path)
        metadata = surface.get("metadata", {})
        contexts.append(
            {
                "artifact": (
                    str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
                ),
                "query": metadata.get("query"),
                "query_mode": metadata.get("query_mode"),
                "ligand_code": metadata.get("ligand_code"),
                "chem_comp_id": metadata.get("chem_comp_id"),
                "review_only": True,
            }
        )
    return contexts


def candidate_control_rows(rows: list[dict[str, Any]], lead_ids: set[str]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []
    for row in rows:
        pdb_id = str(row.get("pdb_id") or "").upper()
        if pdb_id in lead_ids:
            continue
        if row.get("fetch_status") != "fetched":
            continue
        if row.get("terminal_gamma_atom_detected") is not True:
            continue
        if row.get("nonconfounded_inter_auth_chain_within_cutoff") is True:
            continue
        controls.append(row)
    return controls


def control_score(lead: dict[str, Any], control: dict[str, Any], *, cutoff: float) -> tuple[float, str]:
    score = 0.0
    if row_ligand_code(lead, fallback="") != row_ligand_code(control, fallback=""):
        score += 20.0
    if bool(lead.get("local_metal_context_review_only")) != bool(
        control.get("local_metal_context_review_only")
    ):
        score += 100.0
    score += distance_delta(
        lead.get("nearest_gamma_metal_distance_angstrom"),
        control.get("nearest_gamma_metal_distance_angstrom"),
        missing_penalty=25.0,
    )
    score += 0.5 * distance_delta(
        lead.get("best_any_ser_thr_tyr_gamma_distance_angstrom"),
        control.get("best_any_ser_thr_tyr_gamma_distance_angstrom"),
        missing_penalty=10.0,
    )
    control_cross = numeric(control.get("best_cross_auth_chain_distance_angstrom"))
    if control_cross is None:
        score += 5.0
    else:
        score += 0.2 * abs(control_cross - cutoff)
    return (round(score, 6), str(control.get("pdb_id") or ""))


def match_controls(
    leads: list[dict[str, Any]], controls: list[dict[str, Any]], *, cutoff: float
) -> list[dict[str, Any]]:
    unused_controls = {str(control["pdb_id"]).upper(): control for control in controls}
    pairs: list[dict[str, Any]] = []
    for lead in sorted(
        leads,
        key=lambda row: (
            numeric(row.get("best_cross_auth_chain_distance_angstrom")) or 9999.0,
            str(row.get("pdb_id") or ""),
        ),
    ):
        if not unused_controls:
            raise ValueError("not enough terminal-gamma control rows to match every lead")
        ranked = sorted(
            unused_controls.values(),
            key=lambda control: control_score(lead, control, cutoff=cutoff),
        )
        control = ranked[0]
        del unused_controls[str(control["pdb_id"]).upper()]
        pairs.append(
            {
                "pair_id": f"pair_{lead['pdb_id']}_{control['pdb_id']}",
                "lead_pdb_id": lead["pdb_id"],
                "control_pdb_id": control["pdb_id"],
                "pairing_score": control_score(lead, control, cutoff=cutoff)[0],
                "pairing_status": "frozen_before_harness_evaluation",
                "pairing_feature_basis": list(SOURCE_FREE_MATCHING_FEATURES),
                "lead": lead,
                "control": control,
            }
        )
    return pairs


def enrich_pair_row(
    row: dict[str, Any],
    *,
    pair: dict[str, Any],
    pair_role: str,
    ligand_code: str,
) -> dict[str, Any]:
    tranche_row = build_tranche_row(row, ligand_code=ligand_code)
    slug = ligand_slug(ligand_code)
    tranche_row["sibling_pair_id"] = pair["pair_id"]
    tranche_row["sibling_pair_role"] = pair_role
    tranche_row["sibling_matching_features"] = list(SOURCE_FREE_MATCHING_FEATURES)
    tranche_row["sibling_pairing_score"] = pair["pairing_score"]
    tranche_row["sibling_control_match_status"] = pair["pairing_status"]
    if pair_role == "sibling_control":
        tranche_row["row_role"] = f"fresh_{slug}_sibling_topology_control_review_only"
        tranche_row["sibling_counterfamily_context"] = True
        tranche_row["post_score_review_status"] = (
            f"fresh_{slug}_sibling_control_review_only_no_source_free_role_policy"
        )
        tranche_row["expected_frozen_policy_decision"] = (
            "review_only_abstain_sibling_control_context"
        )
    else:
        tranche_row["sibling_counterfamily_context"] = False
        tranche_row["expected_frozen_policy_decision"] = (
            "review_only_abstain_missing_source_free_acceptor_role"
        )
    return tranche_row


def build_artifacts(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.root).resolve()
    surface_paths = [Path(path).resolve() for path in args.surface]
    missing = [str(path) for path in surface_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing surface artifacts: {missing}")

    rows = load_surface_rows(surface_paths)
    if args.auto_leads:
        lead_ids = {
            str(row.get("pdb_id") or "").upper()
            for row in rows
            if row.get("fetch_status") == "fetched"
            and row.get("terminal_gamma_atom_detected") is True
            and row.get("nonconfounded_inter_auth_chain_within_cutoff") is True
        }
    else:
        lead_ids = {pdb_id.upper() for pdb_id in args.lead_ids}
    if not lead_ids:
        raise ValueError("no terminal-gamma geometry leads available for sibling stress")
    leads_by_id = {str(row.get("pdb_id") or "").upper(): row for row in rows}
    missing_leads = sorted(lead_ids - set(leads_by_id))
    if missing_leads:
        raise ValueError(f"lead ids absent from supplied surfaces: {missing_leads}")
    leads = [leads_by_id[pdb_id] for pdb_id in sorted(lead_ids)]
    not_geometry_leads = [
        str(row.get("pdb_id"))
        for row in leads
        if row.get("nonconfounded_inter_auth_chain_within_cutoff") is not True
    ]
    if not_geometry_leads:
        raise ValueError(f"lead ids are not cross-chain geometry leads: {not_geometry_leads}")

    if args.max_pairs is not None:
        leads = sorted(
            leads,
            key=lambda row: (
                numeric(row.get("best_cross_auth_chain_distance_angstrom")) or 9999.0,
                str(row.get("pdb_id") or ""),
            ),
        )[: args.max_pairs]
        lead_ids = {str(row.get("pdb_id") or "").upper() for row in leads}

    controls = candidate_control_rows(rows, lead_ids)
    pairs = match_controls(leads, controls, cutoff=args.cutoff)

    timestamp_slug = args.timestamp.replace("-", "").replace(":", "").replace("Z", "Z")
    prefix = f"{args.artifact_prefix}_{timestamp_slug}"
    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    stress_path = artifact_dir / f"{prefix}.json"
    tranche_path = artifact_dir / f"{prefix}_tranche.json"

    pair_summaries = [
        {
            "pair_id": pair["pair_id"],
            "lead_pdb_id": pair["lead_pdb_id"],
            "control_pdb_id": pair["control_pdb_id"],
            "pairing_score": pair["pairing_score"],
            "pairing_status": pair["pairing_status"],
            "pairing_feature_basis": pair["pairing_feature_basis"],
            "lead_ligand_code_from_structure": row_ligand_code(
                pair["lead"], fallback=args.ligand_code
            ),
            "control_ligand_code_from_structure": row_ligand_code(
                pair["control"], fallback=args.ligand_code
            ),
            "lead_surface_artifact": relative_path_string(
                pair["lead"].get("_surface_artifact"), root
            ),
            "control_surface_artifact": relative_path_string(
                pair["control"].get("_surface_artifact"), root
            ),
            "lead_best_cross_auth_chain_distance_angstrom": pair["lead"].get(
                "best_cross_auth_chain_distance_angstrom"
            ),
            "control_best_cross_auth_chain_distance_angstrom": pair["control"].get(
                "best_cross_auth_chain_distance_angstrom"
            ),
            "lead_nearest_gamma_metal_distance_angstrom": pair["lead"].get(
                "nearest_gamma_metal_distance_angstrom"
            ),
            "control_nearest_gamma_metal_distance_angstrom": pair["control"].get(
                "nearest_gamma_metal_distance_angstrom"
            ),
        }
        for pair in pairs
    ]
    stress_artifact = {
        "metadata": {
            "artifact_id": prefix,
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "query_id": args.query_id,
            "candidate_ids_frozen_before_local_feature_review": True,
            "lead_control_pairing_frozen_before_evaluation": True,
            "pairing_uses_source_free_local_features_only": True,
            "sibling_control_context_review_only": True,
            "source_free_matching_features": list(SOURCE_FREE_MATCHING_FEATURES),
            "lead_count": len(leads),
            "matched_pair_count": len(pairs),
            "candidate_distance_cutoff_angstrom": args.cutoff,
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "source_surface_artifacts": [
                str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
                for path in surface_paths
            ],
            "source_surface_query_contexts_review_only": source_surface_contexts(
                surface_paths, root
            ),
            "ligand_codes_observed": sorted(
                {
                    row_ligand_code(row, fallback=args.ligand_code)
                    for row in leads + controls
                    if row_ligand_code(row, fallback=args.ligand_code)
                }
            ),
        },
        "pairs": pair_summaries,
    }
    write_json(stress_path, stress_artifact)

    tranche_rows: list[dict[str, Any]] = []
    for pair in pairs:
        tranche_rows.append(
            enrich_pair_row(
                pair["lead"],
                pair=pair,
                pair_role="geometry_lead",
                ligand_code=row_ligand_code(pair["lead"], fallback=args.ligand_code),
            )
        )
        tranche_rows.append(
            enrich_pair_row(
                pair["control"],
                pair=pair,
                pair_role="sibling_control",
                ligand_code=row_ligand_code(pair["control"], fallback=args.ligand_code),
            )
        )

    tranche = {
        "metadata": {
            "tranche_id": f"{prefix}_tranche",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "clean_held_out_performance_evidence": False,
            "row_count": len(tranche_rows),
            "terminal_gamma_required_for_tranche": True,
            "terminal_gamma_atom_name_required": "PG",
            "terminal_gamma_candidate_count_reviewed": len(tranche_rows),
            "search_surface_exhausted": False,
            "search_surface_candidate_count_reviewed": len(rows),
            "nonconfounded_candidate_count_within_cutoff": len(leads),
            "description": (
                "Review-only sibling-control stress over terminal-gamma geometry "
                "leads and matched topology controls. Pairing used only compact "
                "source-free local features from frozen surface artifacts."
            ),
            "source_artifacts": [
                "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json",
                str(stress_path.relative_to(root)),
                *[
                    str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
                    for path in surface_paths
                ],
            ],
            "source_surface_query_contexts_review_only": source_surface_contexts(
                surface_paths, root
            ),
            "query_context_review_only_contract": {
                "source_queries_review_only": True,
                "query_text_not_matching_feature": True,
                "coordinate_ligand_code_required": True,
            },
            "source_validation_phase_contract": {
                "candidate_ids_frozen_before_local_feature_review": True,
                "source_free_local_features_computed_before_source_validation": True,
                "source_validation_applied_after_local_features": True,
                "source_validation_review_only": True,
                "review_only_source_validation_fields": [
                    "source_validation_status",
                    "source_validation_phase",
                    "post_score_review_status",
                ],
            },
            "topology_review_contract": {
                "topology_status_required": True,
                "cross_chain_geometry_review_only_without_preaccepted_role_policy": True,
                "role_policy_status": "none_accepted_in_policy_v0",
            },
            "sibling_control_contract": {
                "lead_control_pairing_frozen_before_evaluation": True,
                "pairing_uses_source_free_local_features_only": True,
                "sibling_control_context_review_only": True,
                "lead_and_control_expected_abstention": True,
                "matched_pair_count": len(pairs),
                "source_free_matching_features": list(SOURCE_FREE_MATCHING_FEATURES),
                "role_policy_status": "none_accepted_in_policy_v0",
            },
            "ligand_codes_observed": sorted(
                {
                    row.get("ligand_code_from_structure")
                    for row in tranche_rows
                    if row.get("ligand_code_from_structure")
                }
            ),
        },
        "rows": tranche_rows,
    }
    write_json(tranche_path, tranche)
    return stress_path, tranche_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a compact source-free sibling-control stress tranche."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--surface", action="append", required=True)
    parser.add_argument("--lead-id", dest="lead_ids", action="append")
    parser.add_argument("--auto-leads", action="store_true")
    parser.add_argument("--ligand-code", default="ATP")
    parser.add_argument("--cutoff", type=float, default=6.0)
    parser.add_argument("--max-pairs", type=int)
    parser.add_argument(
        "--artifact-prefix",
        default="epk_terminal_gamma_geometry_lead_sibling_control_stress",
    )
    parser.add_argument(
        "--query-id",
        default="epk_terminal_gamma_geometry_lead_source_free_role_sibling_control_stress_v1_review_only",
    )
    parser.add_argument("--timestamp", default=utc_now())
    args = parser.parse_args(argv)
    args.lead_ids = tuple(args.lead_ids or DEFAULT_GEOMETRY_LEADS)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.cutoff <= 0:
        raise ValueError("--cutoff must be positive")
    if args.max_pairs is not None and args.max_pairs <= 0:
        raise ValueError("--max-pairs must be positive")
    stress_path, tranche_path = build_artifacts(args)
    print(stress_path)
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
