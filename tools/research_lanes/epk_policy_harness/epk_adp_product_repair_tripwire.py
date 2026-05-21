#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LANE_ID = "epk_policy_harness"
DEFAULT_PREFIX = "epk_adp_product_state_candidate_repair_tripwire"
DEFAULT_QUERY_ID = (
    "epk_adp_product_state_and_candidate_repair_tripwire_contract_v1_review_only"
)

REVIEW_ONLY_CONTEXTS = [
    "ADP",
    "PRODUCT_STATE",
    "SUBSTRATE_ACCEPTOR_ANALOG",
    "SPLIT_STATE",
    "CANDIDATE_SPECIFIC_SOURCE_REPAIR",
]

SOURCE_ARTIFACTS = {
    "policy": "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json",
    "diagnostic_tranche": (
        "artifacts/research_lanes/epk_policy_harness/"
        "epk_policy_diagnostic_tranche_20260520.json"
    ),
    "adp_scout_round1": "artifacts/v3_epk_adp_product_query_candidate_scout_1025.json",
    "adp_scout_round2": (
        "artifacts/v3_epk_adp_product_query_candidate_scout_round2_1025.json"
    ),
    "analog_control_reaudit": (
        "artifacts/v3_epk_analog_product_state_policy_control_reaudit_1025.json"
    ),
    "source_repair_terminal": (
        "artifacts/v3_epk_protein_substrate_source_repair_terminal_decision_1025.json"
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def timestamp_slug(timestamp: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "", timestamp)


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


def rel(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def source_payloads(root: Path) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for key, relative_path in SOURCE_ARTIFACTS.items():
        path = root / relative_path
        if not path.exists():
            raise ValueError(f"missing source artifact {relative_path}")
        payloads[key] = load_json(path)
    return payloads


def first_scout_row(payload: dict[str, Any]) -> dict[str, Any]:
    for row in payload.get("rows", []):
        if row.get("review_only") is True and str(row.get("pdb_id") or "").strip():
            return row
    raise ValueError("ADP scout source has no compact review-only rows")


def row_by_pdb(payload: dict[str, Any], pdb_id: str) -> dict[str, Any]:
    for row in payload.get("rows", []):
        if str(row.get("pdb_id") or "").upper() == pdb_id.upper():
            return row
    raise ValueError(f"source artifact has no row for PDB {pdb_id}")


def row_by_entry(payload: dict[str, Any], entry_id: str) -> dict[str, Any]:
    for row in payload.get("rows", []):
        if str(row.get("entry_id") or "").lower() == entry_id.lower():
            return row
    raise ValueError(f"source artifact has no row for entry {entry_id}")


def base_tripwire_row(row_id: str, source_artifact: str) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "source_artifact": source_artifact,
        "row_role": "adp_product_repair_tripwire_review_only",
        "clean_held_out_performance_evidence": False,
        "development_or_regression_context": True,
        "product_state_context": False,
        "substrate_acceptor_analog_context": False,
        "split_state_context": False,
        "candidate_specific_source_repair": False,
        "candidate_specific_source_repair_used_for_predictive_feature": False,
        "source_review_used_for_predictive_feature": False,
        "source_validation_used_for_predictive_feature": False,
        "source_query_used_for_predictive_feature": False,
        "source_text_used_for_predictive_feature": False,
        "structure_title_used_for_predictive_feature": False,
        "post_hoc_ligand_alias_expansion": False,
        "post_hoc_threshold_selection": False,
        "cross_pdb_split_state_fusion": False,
        "homomeric_chain_choice_as_substrate_mapping": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "threshold_calibrated": False,
        "ready_for_production_scoring": False,
        "ready_for_label_import": False,
        "local_geometry_like_fields_present": False,
        "terminal_gamma_equivalent_geometry": False,
        "terminal_gamma_atom_name": None,
        "nearest_gamma_acceptor_distance_angstrom": None,
        "local_metal_context": False,
        "catalytic_site_locality": False,
        "source_free_acceptor_role_features": False,
        "source_free_acceptor_role_policy_id": None,
        "same_structure_co_materialization": False,
        "tripwire_predictive_status": "review_only_blocked",
        "expected_frozen_policy_decision": "review_only_abstain_tripwire",
    }


def adp_query_row(
    source_row: dict[str, Any],
    *,
    source_artifact: str,
    source_query: str,
) -> dict[str, Any]:
    pdb_id = str(source_row["pdb_id"]).upper()
    row = base_tripwire_row(
        f"pdb:{pdb_id}:adp_product_query_tripwire",
        source_artifact,
    )
    row.update(
        {
            "pdb_id": pdb_id,
            "row_role": "adp_product_query_surface_tripwire_review_only",
            "ligand_code_from_structure": "ADP",
            "ligand_context": "ADP",
            "product_state_context": True,
            "tripwire_review_only_contexts": ["ADP", "PRODUCT_STATE"],
            "source_query": source_query,
            "source_validation_status": source_row.get("source_validation_status"),
            "post_score_review_status": source_row.get("candidate_status"),
            "expected_frozen_policy_decision": (
                "review_only_abstain_adp_product_state_tripwire"
            ),
        }
    )
    return row


def diagnostic_adp_row(source_row: dict[str, Any], *, source_artifact: str) -> dict[str, Any]:
    row = base_tripwire_row("pdb:1TH8:adp_product_geometry_tripwire", source_artifact)
    row.update(
        {
            "pdb_id": "1TH8",
            "ligand_code_from_structure": "ADP",
            "ligand_context": "ADP",
            "product_state_context": True,
            "tripwire_review_only_contexts": ["ADP", "PRODUCT_STATE"],
            "local_geometry_like_fields_present": True,
            "terminal_gamma_equivalent_geometry": bool(
                source_row.get("terminal_gamma_equivalent_geometry")
            ),
            "terminal_gamma_atom_name": source_row.get("terminal_gamma_atom_name"),
            "nearest_gamma_acceptor_distance_angstrom": source_row.get(
                "nearest_gamma_acceptor_distance_angstrom"
            ),
            "local_metal_context": bool(source_row.get("local_metal_context")),
            "catalytic_site_locality": bool(source_row.get("catalytic_site_locality")),
            "source_free_acceptor_role_features": bool(
                source_row.get("source_free_acceptor_role_features")
            ),
            "same_structure_co_materialization": bool(
                source_row.get("same_structure_co_materialization")
            ),
            "post_score_review_status": "adp_product_state_prior_diagnostic_blocker",
            "expected_frozen_policy_decision": (
                "review_only_abstain_adp_product_state_tripwire"
            ),
        }
    )
    return row


def analog_row(source_row: dict[str, Any], *, source_artifact: str) -> dict[str, Any]:
    distance = source_row.get("nearest_gamma_to_candidate_acceptor_distance_angstrom")
    row = base_tripwire_row("pdb:3TM0:substrate_acceptor_analog_tripwire", source_artifact)
    row.update(
        {
            "pdb_id": "3TM0",
            "ligand_code_from_structure": "ANP",
            "ligand_context": "SUBSTRATE_ACCEPTOR_ANALOG",
            "substrate_acceptor_analog_context": True,
            "tripwire_review_only_contexts": ["SUBSTRATE_ACCEPTOR_ANALOG"],
            "local_geometry_like_fields_present": True,
            "terminal_gamma_equivalent_geometry": bool(
                source_row.get("active_gamma_geometry")
            ),
            "terminal_gamma_atom_name": "PG",
            "nearest_gamma_acceptor_distance_angstrom": distance,
            "local_metal_context": True,
            "catalytic_site_locality": True,
            "source_free_acceptor_role_features": True,
            "source_free_acceptor_role_policy_id": (
                "source_feature_review_only_not_preaccepted"
            ),
            "same_structure_co_materialization": True,
            "post_score_review_status": source_row.get("policy_reaudit_decision"),
            "expected_frozen_policy_decision": (
                "review_only_abstain_substrate_acceptor_analog_tripwire"
            ),
        }
    )
    return row


def repair_row(source_row: dict[str, Any], *, source_artifact: str) -> dict[str, Any]:
    entry_id = str(source_row["entry_id"])
    active_count = int(source_row.get("active_state_or_atp_metal_candidate_count") or 0)
    mapped_count = int(source_row.get("mapped_or_context_acceptor_candidate_count") or 0)
    is_split_state = "split" in str(source_row.get("decision") or "").lower()
    row = base_tripwire_row(
        f"{entry_id}:candidate_specific_source_repair_tripwire",
        source_artifact,
    )
    contexts = ["CANDIDATE_SPECIFIC_SOURCE_REPAIR"]
    if is_split_state:
        contexts.append("SPLIT_STATE")
    row.update(
        {
            "pdb_id": None,
            "entry_id": entry_id,
            "ligand_code_from_structure": "ATP",
            "ligand_context": "POST_HOC_REPAIR",
            "candidate_specific_source_repair": True,
            "split_state_context": is_split_state,
            "tripwire_review_only_contexts": contexts,
            "local_geometry_like_fields_present": active_count > 0 or mapped_count > 0,
            "terminal_gamma_equivalent_geometry": active_count > 0,
            "terminal_gamma_atom_name": "PG" if active_count > 0 else None,
            "local_metal_context": active_count > 0,
            "catalytic_site_locality": active_count > 0,
            "source_free_acceptor_role_features": mapped_count > 0,
            "source_free_acceptor_role_policy_id": (
                "candidate_repair_context_review_only_not_preaccepted"
                if mapped_count > 0
                else None
            ),
            "same_structure_co_materialization": False,
            "source_validation_status": source_row.get("repair_status"),
            "post_score_review_status": source_row.get("decision"),
            "expected_frozen_policy_decision": (
                "review_only_abstain_candidate_specific_source_repair_tripwire"
            ),
        }
    )
    return row


def counterfactual_local_feature_row(
    source: dict[str, Any],
    *,
    row_id: str,
    contexts: list[str],
    ligand_code: str,
    source_artifact: str,
) -> dict[str, Any]:
    row = base_tripwire_row(row_id, source_artifact)
    row.update(
        {
            "pdb_id": source.get("pdb_id"),
            "entry_id": source.get("entry_id"),
            "row_role": "counterfactual_local_feature_tripwire_review_only",
            "ligand_code_from_structure": ligand_code,
            "tripwire_review_only_contexts": contexts,
            "local_geometry_like_fields_present": True,
            "terminal_gamma_equivalent_geometry": True,
            "terminal_gamma_atom_name": "PG",
            "nearest_gamma_acceptor_distance_angstrom": 3.0,
            "local_metal_context": True,
            "catalytic_site_locality": True,
            "source_free_acceptor_role_features": True,
            "source_free_acceptor_role_policy_id": (
                "counterfactual_tripwire_not_preaccepted"
            ),
            "same_structure_co_materialization": True,
            "post_score_review_status": (
                "counterfactual_local_features_review_only_tripwire"
            ),
            "counterfactual_local_features_injected_for_tripwire_only": True,
            "expected_frozen_policy_decision": (
                "review_only_abstain_counterfactual_tripwire_context"
            ),
        }
    )
    if "ADP" in contexts:
        row["ligand_context"] = "ADP"
    if "PRODUCT_STATE" in contexts:
        row["product_state_context"] = True
    if "SUBSTRATE_ACCEPTOR_ANALOG" in contexts:
        row["ligand_context"] = "SUBSTRATE_ACCEPTOR_ANALOG"
        row["substrate_acceptor_analog_context"] = True
    if "SPLIT_STATE" in contexts:
        row["split_state_context"] = True
        row["same_structure_co_materialization"] = False
    if "CANDIDATE_SPECIFIC_SOURCE_REPAIR" in contexts:
        row["ligand_context"] = "POST_HOC_REPAIR"
        row["candidate_specific_source_repair"] = True
    return row


def build_artifacts(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.root).resolve()
    payloads = source_payloads(root)
    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    prefix = f"{args.artifact_prefix}_{timestamp_slug(args.timestamp)}"
    artifact_path = artifact_dir / f"{prefix}.json"
    tranche_path = artifact_dir / f"{prefix}_tranche.json"

    scout_one = first_scout_row(payloads["adp_scout_round1"])
    scout_two = first_scout_row(payloads["adp_scout_round2"])
    diagnostic_adp = row_by_pdb(payloads["diagnostic_tranche"], "1TH8")
    analog = row_by_pdb(payloads["analog_control_reaudit"], "3TM0")
    repair_rows = [
        row_by_entry(payloads["source_repair_terminal"], "m_csa:756"),
        row_by_entry(payloads["source_repair_terminal"], "m_csa:757"),
        row_by_entry(payloads["source_repair_terminal"], "m_csa:760"),
    ]

    source_rows = [
        adp_query_row(
            scout_one,
            source_artifact=SOURCE_ARTIFACTS["adp_scout_round1"],
            source_query=str(
                payloads["adp_scout_round1"].get("metadata", {}).get("source_query")
                or ""
            ),
        ),
        adp_query_row(
            scout_two,
            source_artifact=SOURCE_ARTIFACTS["adp_scout_round2"],
            source_query=str(
                payloads["adp_scout_round2"].get("metadata", {}).get("source_query")
                or ""
            ),
        ),
        diagnostic_adp_row(
            diagnostic_adp,
            source_artifact=SOURCE_ARTIFACTS["diagnostic_tranche"],
        ),
        analog_row(analog, source_artifact=SOURCE_ARTIFACTS["analog_control_reaudit"]),
    ]
    source_rows.extend(
        repair_row(row, source_artifact=SOURCE_ARTIFACTS["source_repair_terminal"])
        for row in repair_rows
    )
    source_rows.extend(
        [
            counterfactual_local_feature_row(
                {"pdb_id": scout_one.get("pdb_id")},
                row_id="pdb:13PK:adp_product_all_local_features_tripwire",
                contexts=["ADP", "PRODUCT_STATE"],
                ligand_code="ADP",
                source_artifact=SOURCE_ARTIFACTS["adp_scout_round1"],
            ),
            counterfactual_local_feature_row(
                {"entry_id": "m_csa:757"},
                row_id="m_csa:757:candidate_repair_all_local_features_tripwire",
                contexts=["CANDIDATE_SPECIFIC_SOURCE_REPAIR"],
                ligand_code="ATP",
                source_artifact=SOURCE_ARTIFACTS["source_repair_terminal"],
            ),
            counterfactual_local_feature_row(
                {"entry_id": "m_csa:760"},
                row_id="m_csa:760:candidate_repair_all_local_features_tripwire",
                contexts=[
                    "CANDIDATE_SPECIFIC_SOURCE_REPAIR",
                    "SPLIT_STATE",
                ],
                ligand_code="ATP",
                source_artifact=SOURCE_ARTIFACTS["source_repair_terminal"],
            ),
        ]
    )

    geometry_like_count = sum(
        1 for row in source_rows if row.get("local_geometry_like_fields_present") is True
    )
    source_queries = [
        str(payloads["adp_scout_round1"].get("metadata", {}).get("source_query") or ""),
        str(payloads["adp_scout_round2"].get("metadata", {}).get("source_query") or ""),
    ]
    source_contexts = [
        {
            "artifact": SOURCE_ARTIFACTS[key],
            "query": query,
            "query_mode": "full_text",
            "query_ligand_synonyms_review_only": ["ADP"],
            "coordinate_ligand_codes_observed": ["ADP"],
            "review_only": True,
        }
        for key, query in (
            ("adp_scout_round1", source_queries[0]),
            ("adp_scout_round2", source_queries[1]),
        )
        if query
    ]

    metadata = {
        "artifact_id": prefix,
        "created_at": args.timestamp,
        "lane_id": LANE_ID,
        "review_only": True,
        "query_id": args.query_id,
        "policy_version": "epk_review_only_policy_harness_v0_20260520",
        "source_artifacts": list(SOURCE_ARTIFACTS.values()),
        "source_surface_query_contexts_review_only": source_contexts,
        "candidate_contexts_frozen_before_tripwire_evaluation": True,
        "geometry_like_tripwire_row_count": geometry_like_count,
        "raw_coordinate_dump_written": False,
        "production_claim_allowed": False,
        "labels_or_fingerprints_changed": False,
        "epk_score_computed": False,
        "threshold_calibrated": False,
        "ready_for_label_import": False,
        "ready_for_production_scoring": False,
        "review_only_contexts": REVIEW_ONLY_CONTEXTS,
    }
    artifact = {
        "metadata": metadata,
        "rows": [
            {
                "row_id": row["row_id"],
                "source_artifact": row["source_artifact"],
                "pdb_id": row.get("pdb_id"),
                "entry_id": row.get("entry_id"),
                "tripwire_review_only_contexts": row.get(
                    "tripwire_review_only_contexts", []
                ),
                "local_geometry_like_fields_present": row.get(
                    "local_geometry_like_fields_present"
                ),
                "post_score_review_status": row.get("post_score_review_status"),
                "source_validation_status": row.get("source_validation_status"),
                "raw_coordinate_dump_written": False,
            }
            for row in source_rows
        ],
    }
    write_json(artifact_path, artifact)

    tranche = {
        "metadata": {
            "tranche_id": f"{prefix}_tranche",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "clean_held_out_performance_evidence": False,
            "row_count": len(source_rows),
            "search_surface_exhausted": False,
            "search_surface_candidate_count_reviewed": len(source_rows),
            "nonconfounded_candidate_count_within_cutoff": 0,
            "description": (
                "Review-only ADP/product-state, substrate/acceptor analog, split-state, "
                "and candidate-specific source-repair tripwire tranche. Prior "
                "development rows may stress the frozen policy but cannot support "
                "held-out performance or production scoring claims."
            ),
            "source_artifacts": [SOURCE_ARTIFACTS["policy"], rel(artifact_path, root)],
            "source_surface_query_contexts_review_only": source_contexts,
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
            },
            "adp_product_repair_tripwire_contract": {
                "candidate_contexts_frozen_before_tripwire_evaluation": True,
                "adp_product_state_rows_review_only": True,
                "substrate_acceptor_analog_rows_review_only": True,
                "candidate_specific_repairs_review_only": True,
                "local_geometry_like_fields_cannot_override_review_only_context": True,
                "candidate_specific_source_repairs_forbidden_as_predictive_features": True,
                "future_policy_activation_requires_fresh_preregistered_policy": True,
                "future_policy_activation_allowed": False,
                "geometry_like_tripwire_row_count": geometry_like_count,
                "review_only_contexts": REVIEW_ONLY_CONTEXTS,
            },
        },
        "rows": source_rows,
    }
    write_json(tranche_path, tranche)
    return artifact_path, tranche_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a compact review-only ADP/product-state and candidate-repair "
            "tripwire tranche from prior ePK review artifacts."
        )
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--artifact-prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--query-id", default=DEFAULT_QUERY_ID)
    parser.add_argument("--timestamp", default=utc_now())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    artifact_path, tranche_path = build_artifacts(args)
    print(artifact_path)
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
