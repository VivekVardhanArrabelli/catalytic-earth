from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_ID = "v3_targeted_expansion_factory_batch_current702_20260608"
SCHEMA_VERSION = "v3.targeted_expansion_factory_batch"
PRIOR_ARCHITECTURE_DEFAULT_ENTRY_IDS = (
    "m_csa:10",
    "m_csa:30",
    "m_csa:31",
    "m_csa:191",
    "m_csa:448",
    "m_csa:973",
)

ADMISSION_STATES = (
    "countable_candidate",
    "review_only_evidence",
    "reject_preserve_signal",
    "oos_hard_negative",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
    "acquisition_needed",
)

MCSA_AXIS_BY_TOP1 = {
    "metal_dependent_hydrolase": "metal_hydrolase_subclass_expansion",
    "heme_peroxidase_oxidase": "underrepresented_redox_oxygen_transfer",
    "ser_his_acid_hydrolase": "serine_or_cysteine_hydrolase_boundary_controls",
    "flavin_dehydrogenase_reductase": "underrepresented_redox_oxygen_transfer",
    "flavin_monooxygenase": "flavin_oxygen_transfer_boundary",
    "plp_dependent_enzyme": "plp_subclass_expansion",
    "radical_sam_enzyme": "radical_cobalamin_sam_like_probes",
}

EXTERNAL_LANE_AXIS = {
    "external_source:oxidoreductase_long_tail": (
        "underrepresented_redox_oxygen_transfer"
    ),
    "external_source:transferase_phosphoryl": (
        "phosphoryl_transfer_boundary_review_only"
    ),
    "external_source:transferase_methyl": "sam_methyltransferase_transfer_axis",
    "external_source:glycan_chemistry": (
        "glycoside_nucleoside_hydrolase_glycan_transfer"
    ),
    "external_source:isomerase": "near_orphan_isomerase_controls",
    "external_source:lyase": "plp_schiff_base_or_nucleoside_lyase_controls",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": sha256_path(path),
        "bytes": path.stat().st_size,
    }


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object at {path}")
    return payload


def _entry_sort_key(value: str) -> tuple[int, str, str]:
    prefix, _, suffix = value.partition(":")
    if suffix.isdigit():
        return (0, prefix, f"{int(suffix):09d}")
    return (1, prefix, suffix or value)


def _rows(payload: dict[str, Any], key: str = "rows") -> list[dict[str, Any]]:
    return [row for row in payload.get(key, []) if isinstance(row, dict)]


def _sequence_index(sequence_cluster_proxy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("entry_id")): row
        for row in _rows(sequence_cluster_proxy)
        if row.get("entry_id") is not None
    }


def _clean_list(value: Any) -> list[Any]:
    if not isinstance(value, list):
        return []
    return [item for item in value if item not in (None, "")]


def _source_free_policy() -> dict[str, bool]:
    return {
        "mechanism_text_used_for_scoring_or_routing": False,
        "ec_or_rhea_ids_used_for_scoring_or_routing": False,
        "entry_name_or_protein_name_used_for_scoring_or_routing": False,
        "source_ids_used_for_scoring": False,
    }


def _mcsa_family_axis(row: dict[str, Any]) -> str:
    status = str(row.get("status") or "")
    top1 = str(row.get("top1_fingerprint_id") or "")
    cofactor_families = {str(value) for value in _clean_list(row.get("cofactor_families"))}
    cofactor_level = str(row.get("cofactor_evidence_level") or "")
    top1_score = _float_or_none(row.get("top1_score"))
    if status in {"no_structure_positions", "insufficient_resolved_residues"}:
        return "no_reliable_structure_or_locator_gap"
    if top1 == "radical_sam_enzyme" or "cobalamin" in cofactor_families:
        return "radical_cobalamin_sam_like_probes"
    if top1 == "flavin_monooxygenase":
        return "flavin_oxygen_transfer_boundary"
    if "metal_ion" in cofactor_families and top1 == "metal_dependent_hydrolase":
        return "metal_hydrolase_subclass_expansion"
    if cofactor_level == "absent" and top1_score is not None and top1_score < 0.4:
        return "near_orphan_low_geometry_support"
    return MCSA_AXIS_BY_TOP1.get(top1, "near_orphan_low_geometry_support")


def _mcsa_admission(row: dict[str, Any]) -> tuple[str, str, str, str]:
    status = str(row.get("status") or "")
    blockers = [str(value) for value in _clean_list(row.get("readiness_blockers"))]
    readiness_score = _int_or_none(row.get("readiness_score"))
    if status == "no_structure_positions":
        return (
            "blocked_coordinate",
            "m_csa_coordinate_positions_missing",
            "materialize or approve a coordinate source before locator scoring",
            "tier_3_blocked_coordinate",
        )
    if (
        status == "insufficient_resolved_residues"
        or "resolved_at_least_three_residues" in blockers
    ):
        return (
            "blocked_locator",
            "m_csa_active_site_locator_incomplete",
            "repair source-free residue locator mapping before family admission",
            "tier_3_blocked_locator",
        )
    if readiness_score is not None and readiness_score >= 5:
        return (
            "review_only_evidence",
            "local_geometry_candidate_ready_for_admission_review",
            "run family-specific source/duplicate/import-preview gates before any countable use",
            "tier_2_geometry_ready_review",
        )
    return (
        "review_only_evidence",
        "local_geometry_candidate_low_support_review_only",
        "preserve as non-counting evidence until a sharper family gate is available",
        "tier_3_review_only_low_support",
    )


def _float_or_none(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _coordinate_status_from_pdb(pdb_id: Any) -> str:
    return "experimental_pdb_selected" if pdb_id else "coordinate_missing"


def _mcsa_candidate_row(
    row: dict[str, Any],
    *,
    sequence_row: dict[str, Any] | None,
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    admission_state, state_basis, next_action, tier = _mcsa_admission(row)
    entry_id = str(row.get("entry_id") or "")
    accessions = (
        _clean_list(sequence_row.get("reference_uniprot_ids"))
        if sequence_row
        else []
    )
    top1_score = _float_or_none(row.get("top1_score"))
    cofactor_families = [str(value) for value in _clean_list(row.get("cofactor_families"))]
    source_hashes = {
        "label_expansion_candidates": source_records["label_expansion_candidates"][
            "sha256"
        ]
    }
    if "sequence_cluster_proxy" in source_records:
        source_hashes["sequence_cluster_proxy"] = source_records[
            "sequence_cluster_proxy"
        ]["sha256"]
    return {
        "candidate_id": entry_id,
        "entry_id": entry_id,
        "source_namespace": "m_csa",
        "accession": str(accessions[0]) if accessions else None,
        "source_accessions": accessions,
        "family_axis": _mcsa_family_axis(row),
        "family_axis_basis": (
            "assigned from source-free geometry top1, cofactor availability, and "
            "coordinate/locator status; mechanism text is retained only by source hash"
        ),
        "proposed_label_tier": tier,
        "provenance_tier": "local_m_csa_geometry_retrieval",
        "admission_state": admission_state,
        "state_basis": state_basis,
        "allowed_next_action": next_action,
        "countable_label_candidate": False,
        "ready_for_label_import": False,
        "human_review_required_for_countable_promotion": True,
        "coordinate_availability": {
            "status": _coordinate_status_from_pdb(row.get("pdb_id")),
            "pdb_id": row.get("pdb_id"),
            "predicted_coordinate_available": None,
            "coordinate_provenance": "M-CSA selected experimental PDB when present",
        },
        "active_site_locator_evidence": {
            "status": row.get("status"),
            "resolved_residue_count": row.get("resolved_residue_count"),
            "has_pairwise_geometry": bool(row.get("has_pairwise_geometry")),
            "has_pocket_context": bool(row.get("has_pocket_context")),
            "readiness_checks": row.get("readiness_checks") or {},
            "readiness_blockers": row.get("readiness_blockers") or [],
        },
        "cofactor_metal_evidence": {
            "cofactor_evidence_level": row.get("cofactor_evidence_level"),
            "cofactor_families": cofactor_families,
        },
        "fold_tm_near_neighbor_signal": {
            "geometry_top1_fingerprint_id": row.get("top1_fingerprint_id"),
            "geometry_top1_score": top1_score,
            "sequence_cluster_id": (
                sequence_row.get("sequence_cluster_id") if sequence_row else None
            ),
            "fold_tm_status": "not_attached_in_this_factory_batch",
        },
        "geometry_reconstruction_status": {
            "status": row.get("status"),
            "readiness_score": row.get("readiness_score"),
            "mechanistic_coherence_score": row.get("mechanistic_coherence_score"),
        },
        "flags": {
            "oos_or_novelty": True,
            "novelty_signal": "not_in_current_label_registry_candidate_artifact",
            "cofactor_confounded": bool(cofactor_families),
            "no_reliable_structure": row.get("status") != "ok",
            "prior_architecture_default_row": entry_id
            in PRIOR_ARCHITECTURE_DEFAULT_ENTRY_IDS,
        },
        "review_context": {
            "entry_name": row.get("entry_name"),
            "mechanism_text_count": row.get("mechanism_text_count"),
        },
        "rationale": (
            "Local M-CSA expansion candidate with geometry/cofactor/locator "
            "evidence preserved for admission routing; no import or countable "
            "promotion is implied."
        ),
        "predictive_feature_policy": _source_free_policy(),
        "source_hashes": source_hashes,
        "source_row_sha256": _canonical_sha256(row),
    }


def _external_family_axis(row: dict[str, Any]) -> str:
    lane_id = str(row.get("lane_id") or "")
    return EXTERNAL_LANE_AXIS.get(lane_id, "external_source_family_decision_needed")


def _external_admission(row: dict[str, Any]) -> tuple[str, str, str, str]:
    blockers = [str(value) for value in _clean_list(row.get("source_evidence_blockers"))]
    sourcing_status = str(row.get("sourcing_status") or "")
    active_site_status = str(row.get("active_site_evidence_status") or "")
    new_to_pool = row.get("new_to_current_external_pool")
    if new_to_pool is False or any("accession_already" in item for item in blockers):
        return (
            "reject_preserve_signal",
            "external_duplicate_or_prior_pool_signal",
            "preserve duplicate/prior-pool signal and do not import",
            "tier_4_reject_preserve_signal",
        )
    if any("terminal_duplicate_rejection" in item for item in blockers):
        return (
            "reject_preserve_signal",
            "prior_terminal_duplicate_rejection",
            "preserve prior terminal duplicate decision and do not import",
            "tier_4_reject_preserve_signal",
        )
    if (
        sourcing_status == "blocked_uncovered_mechanism_lane"
        or any("mechanism_lane_not_covered" in item for item in blockers)
    ):
        return (
            "blocked_family_decision",
            "external_lane_not_covered_by_current_family_policy",
            "decide whether this source lane belongs in the next targeted axis before scoring",
            "tier_3_blocked_family_decision",
        )
    if any("structure_reference_missing" in item for item in blockers):
        return (
            "blocked_coordinate",
            "external_coordinate_reference_missing",
            "acquire AlphaFold/PDB coordinate reference before source-free scoring",
            "tier_3_blocked_coordinate",
        )
    if sourcing_status == "sourced_pending_sequence_structure_distance_screens":
        return (
            "review_only_evidence",
            "external_source_evidence_ready_pending_distance_screens",
            "run duplicate, structural, UniRef, review, and label-factory gates before import",
            "tier_2_external_review_evidence",
        )
    if active_site_status in {
        "binding_or_reaction_context_only",
        "not_sampled_cap_reached",
        "not_sampled_metadata_blocked",
    }:
        return (
            "acquisition_needed",
            f"external_active_site_evidence_{active_site_status}",
            "collect explicit catalytic residue/locator evidence before admission scoring",
            "tier_3_acquisition_needed",
        )
    return (
        "acquisition_needed",
        "external_evidence_sourcing_blocked",
        "complete source, sequence, structure, and review-gate acquisition steps",
        "tier_3_acquisition_needed",
    )


def _external_coordinate_availability(row: dict[str, Any]) -> dict[str, Any]:
    pdb_ids = [str(value) for value in _clean_list(row.get("pdb_ids"))]
    alphafold_ids = [str(value) for value in _clean_list(row.get("alphafold_ids"))]
    if pdb_ids:
        status = "experimental_pdb_references_present"
    elif alphafold_ids:
        status = "predicted_alphafold_reference_present"
    else:
        status = "coordinate_reference_missing"
    return {
        "status": status,
        "pdb_id_count": len(pdb_ids),
        "pdb_id_examples": pdb_ids[:5],
        "alphafold_ids": alphafold_ids[:5],
        "predicted_coordinate_available": bool(alphafold_ids),
        "coordinate_provenance": "UniProt cross-reference fields in source freeze",
    }


def _external_candidate_row(
    row: dict[str, Any],
    *,
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    admission_state, state_basis, next_action, tier = _external_admission(row)
    accession = str(row.get("accession") or "")
    blockers = [str(value) for value in _clean_list(row.get("source_evidence_blockers"))]
    next_required_screens = [
        str(value) for value in _clean_list(row.get("next_required_screens"))
    ]
    return {
        "candidate_id": str(row.get("entry_id") or f"uniprot:{accession}"),
        "entry_id": str(row.get("entry_id") or f"uniprot:{accession}"),
        "source_namespace": "uniprot_swissprot",
        "accession": accession,
        "source_accessions": [accession] if accession else [],
        "family_axis": _external_family_axis(row),
        "family_axis_basis": (
            "assigned from the frozen external sourcing lane for worklist "
            "organization only; lane/name/EC fields are not scoring features"
        ),
        "proposed_label_tier": tier,
        "provenance_tier": "external_swissprot_review_only_freeze",
        "admission_state": admission_state,
        "state_basis": state_basis,
        "allowed_next_action": next_action,
        "countable_label_candidate": False,
        "ready_for_label_import": False,
        "human_review_required_for_countable_promotion": True,
        "coordinate_availability": _external_coordinate_availability(row),
        "active_site_locator_evidence": {
            "active_site_evidence_status": row.get("active_site_evidence_status"),
            "active_site_feature_count": row.get("active_site_feature_count"),
            "binding_site_feature_count": row.get("binding_site_feature_count"),
            "catalytic_activity_count": row.get("catalytic_activity_count"),
            "source_evidence_blockers": blockers,
        },
        "cofactor_metal_evidence": {
            "cofactor_comment_count": row.get("cofactor_comment_count"),
            "cofactor_evidence_level": (
                "source_comment_present"
                if row.get("cofactor_comment_count")
                else "not_attached_or_absent"
            ),
            "cofactor_families": [],
        },
        "fold_tm_near_neighbor_signal": {
            "current_reference_sequence_screen": "not_run_in_freeze",
            "current_countable_structural_screen": "not_run_in_freeze",
            "external_structural_cluster_assignment": "not_run_in_freeze",
            "next_required_screens": next_required_screens,
        },
        "geometry_reconstruction_status": {
            "sourcing_status": row.get("sourcing_status"),
            "score_status": row.get("score_status"),
            "import_ready_candidate": row.get("import_ready_candidate"),
        },
        "flags": {
            "oos_or_novelty": True,
            "novelty_signal": "external_review_only_candidate",
            "cofactor_confounded": bool(row.get("cofactor_comment_count")),
            "no_reliable_structure": not (
                row.get("pdb_ids") or row.get("alphafold_ids")
            ),
            "covered_counterevidence_lane": bool(
                row.get("covered_counterevidence_lane")
            ),
            "new_to_current_external_pool": bool(row.get("new_to_current_external_pool")),
        },
        "review_context": {
            "protein_name": row.get("protein_name"),
            "uniprot_entry_name": row.get("uniprot_entry_name"),
            "uniprot_review_status": row.get("uniprot_review_status"),
        },
        "rationale": (
            "Frozen external-source candidate with accession, source status, "
            "coordinate-reference availability, active-site evidence status, and "
            "required acquisition screens preserved for non-counting admission."
        ),
        "predictive_feature_policy": _source_free_policy(),
        "source_hashes": {
            "external_candidate_freeze": source_records["external_candidate_freeze"][
                "sha256"
            ]
        },
        "source_row_sha256": _canonical_sha256(row),
    }


def _dedupe_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row.get("source_namespace")), str(row.get("candidate_id")))
        deduped[key] = row
    return sorted(
        deduped.values(),
        key=lambda row: (
            str(row.get("source_namespace")),
            _entry_sort_key(str(row.get("candidate_id"))),
        ),
    )


def _state_assignment_audit(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    allowed = set(ADMISSION_STATES)
    seen: set[str] = set()
    violations: list[dict[str, Any]] = []
    for row in candidate_rows:
        candidate_id = str(row.get("candidate_id") or "")
        state = row.get("admission_state")
        row_violations: list[str] = []
        if not candidate_id:
            row_violations.append("missing_candidate_id")
        elif candidate_id in seen:
            row_violations.append("duplicate_candidate_id")
        else:
            seen.add(candidate_id)
        if state not in allowed:
            row_violations.append("unknown_or_missing_admission_state")
        if row.get("countable_label_candidate") is not False:
            row_violations.append("countable_candidate_flag_not_false")
        if row.get("ready_for_label_import") is not False:
            row_violations.append("ready_for_label_import_not_false")
        if row_violations:
            violations.append(
                {
                    "candidate_id": candidate_id or None,
                    "admission_state": state,
                    "violations": row_violations,
                }
            )
    return {
        "passed": not violations,
        "rows_checked": len(candidate_rows),
        "rows_with_exactly_one_state": len(candidate_rows) - len(violations),
        "allowed_states": list(ADMISSION_STATES),
        "violations": violations,
    }


def _factory_guardrail_audit(
    candidate_rows: list[dict[str, Any]],
    *,
    min_target_candidates: int,
    max_target_candidates: int,
) -> dict[str, Any]:
    candidate_ids = {str(row.get("candidate_id")) for row in candidate_rows}
    accession_gaps = [
        row.get("candidate_id")
        for row in candidate_rows
        if not row.get("accession") and not row.get("source_accessions")
    ]
    source_hash_gaps = [
        row.get("candidate_id") for row in candidate_rows if not row.get("source_hashes")
    ]
    family_axis_gaps = [
        row.get("candidate_id") for row in candidate_rows if not row.get("family_axis")
    ]
    policy_violations = []
    for row in candidate_rows:
        policy = row.get("predictive_feature_policy") or {}
        if any(policy.get(key) for key in _source_free_policy()):
            policy_violations.append(row.get("candidate_id"))
    prior_rows_present = sorted(
        set(PRIOR_ARCHITECTURE_DEFAULT_ENTRY_IDS) & candidate_ids,
        key=_entry_sort_key,
    )
    candidate_count = len(candidate_rows)
    violations: list[dict[str, Any]] = []
    if not (min_target_candidates <= candidate_count <= max_target_candidates):
        violations.append(
            {
                "violation": "candidate_count_outside_target_range",
                "candidate_count": candidate_count,
                "min_target_candidates": min_target_candidates,
                "max_target_candidates": max_target_candidates,
            }
        )
    if accession_gaps:
        violations.append(
            {
                "violation": "candidate_rows_missing_accession_or_source_accessions",
                "candidate_ids": accession_gaps,
            }
        )
    if source_hash_gaps:
        violations.append(
            {
                "violation": "candidate_rows_missing_source_hashes",
                "candidate_ids": source_hash_gaps,
            }
        )
    if family_axis_gaps:
        violations.append(
            {
                "violation": "candidate_rows_missing_family_axis",
                "candidate_ids": family_axis_gaps,
            }
        )
    if policy_violations:
        violations.append(
            {
                "violation": "forbidden_predictive_feature_policy_true",
                "candidate_ids": policy_violations,
            }
        )
    if prior_rows_present:
        violations.append(
            {
                "violation": "prior_architecture_default_rows_reintroduced",
                "candidate_ids": prior_rows_present,
            }
        )
    return {
        "passed": not violations,
        "candidate_count": candidate_count,
        "target_range": [min_target_candidates, max_target_candidates],
        "accession_or_source_accessions_complete": not accession_gaps,
        "source_hashes_complete": not source_hash_gaps,
        "family_axis_complete": not family_axis_gaps,
        "forbidden_predictive_feature_policy_clean": not policy_violations,
        "prior_architecture_default_rows_absent": not prior_rows_present,
        "violations": violations,
    }


def _counter_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(key)) for row in rows).items()))


def _admission_state_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(str(row.get("admission_state")) for row in rows)
    return {state: counter.get(state, 0) for state in ADMISSION_STATES}


def _nested_counter(rows: list[dict[str, Any]], path: tuple[str, ...]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        value: Any = row
        for key in path:
            value = value.get(key) if isinstance(value, dict) else None
        counter[str(value)] += 1
    return dict(sorted(counter.items()))


def _acquisition_plan(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    acquisition_rows = [
        row for row in candidate_rows if row.get("admission_state") == "acquisition_needed"
    ]
    blocked_family_rows = [
        row
        for row in candidate_rows
        if row.get("admission_state") == "blocked_family_decision"
    ]
    blocked_locator_rows = [
        row for row in candidate_rows if row.get("admission_state") == "blocked_locator"
    ]
    blocked_coordinate_rows = [
        row for row in candidate_rows if row.get("admission_state") == "blocked_coordinate"
    ]
    action_counts = Counter(str(row.get("allowed_next_action")) for row in candidate_rows)
    return {
        "status": "ready",
        "counts": {
            "acquisition_needed_rows": len(acquisition_rows),
            "blocked_family_decision_rows": len(blocked_family_rows),
            "blocked_locator_rows": len(blocked_locator_rows),
            "blocked_coordinate_rows": len(blocked_coordinate_rows),
        },
        "next_mechanical_steps": [
            {
                "rank": 1,
                "action": (
                    "Run source-free duplicate and structural distance screens "
                    "for the external review-only rows."
                ),
                "unblocks": (
                    "external rows with explicit active-site evidence can move "
                    "from review_only_evidence to a countable review boundary."
                ),
            },
            {
                "rank": 2,
                "action": (
                    "Collect explicit catalytic residue or locator sources for "
                    "acquisition_needed external rows."
                ),
                "unblocks": (
                    "active-site locator evidence and later geometry/reconstruction "
                    "scoring."
                ),
            },
            {
                "rank": 3,
                "action": (
                    "Materialize or repair coordinate/locator mappings for "
                    "blocked M-CSA rows."
                ),
                "unblocks": "local geometry candidates can enter normal admission review.",
            },
            {
                "rank": 4,
                "action": (
                    "Decide whether uncovered external lanes become targeted axes "
                    "or stay preserved OOS signal."
                ),
                "unblocks": (
                    "family-axis routing for blocked_family_decision rows without "
                    "row-by-row review."
                ),
            },
        ],
        "allowed_next_action_counts": dict(sorted(action_counts.items())),
    }


def _candidate_ref(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": row.get("candidate_id"),
        "entry_id": row.get("entry_id"),
        "accession": row.get("accession"),
        "family_axis": row.get("family_axis"),
        "provenance_tier": row.get("provenance_tier"),
        "source_namespace": row.get("source_namespace"),
    }


def _first_action_screen_row(row: dict[str, Any]) -> dict[str, Any]:
    locator = row.get("active_site_locator_evidence") or {}
    coordinate = row.get("coordinate_availability") or {}
    fold_signal = row.get("fold_tm_near_neighbor_signal") or {}
    return {
        "candidate_id": row.get("candidate_id"),
        "entry_id": row.get("entry_id"),
        "accession": row.get("accession"),
        "source_accessions": row.get("source_accessions"),
        "source_namespace": row.get("source_namespace"),
        "family_axis": row.get("family_axis"),
        "proposed_label_tier": row.get("proposed_label_tier"),
        "admission_state": row.get("admission_state"),
        "required_action": row.get("allowed_next_action"),
        "coordinate_status": coordinate.get("status"),
        "active_site_evidence_status": (
            locator.get("active_site_evidence_status") or locator.get("status")
        ),
        "next_required_screens": fold_signal.get("next_required_screens") or [],
        "source_hashes": row.get("source_hashes"),
        "source_row_sha256": row.get("source_row_sha256"),
    }


def _first_action_screen_input(
    candidate_rows: list[dict[str, Any]],
    action_tranches: list[dict[str, Any]],
) -> dict[str, Any]:
    if not action_tranches:
        return {
            "status": "empty",
            "tranche_rank": None,
            "required_action": None,
            "candidate_count": 0,
            "rows": [],
        }
    first_tranche = action_tranches[0]
    rows = [
        row
        for row in candidate_rows
        if row.get("admission_state") == first_tranche["admission_state"]
        and row.get("allowed_next_action") == first_tranche["allowed_next_action"]
    ]
    rows = sorted(
        rows,
        key=lambda row: (
            str(row.get("source_namespace")),
            _entry_sort_key(str(row.get("candidate_id"))),
        ),
    )
    return {
        "status": "ready" if rows else "empty",
        "tranche_rank": first_tranche["rank"],
        "admission_state": first_tranche["admission_state"],
        "required_action": first_tranche["allowed_next_action"],
        "candidate_count": len(rows),
        "rows": [_first_action_screen_row(row) for row in rows],
    }


def _tranche_priority(state: str, action: str) -> int:
    if state == "review_only_evidence" and (
        "structural" in action or "UniRef" in action or "distance" in action
    ):
        return 10
    if state == "review_only_evidence":
        return 20
    if state == "acquisition_needed":
        return 30
    if state == "blocked_locator":
        return 40
    if state == "blocked_coordinate":
        return 50
    if state == "blocked_family_decision":
        return 60
    if state == "reject_preserve_signal":
        return 90
    return 80


def _action_tranches(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in candidate_rows:
        grouped[
            (
                str(row.get("admission_state")),
                str(row.get("allowed_next_action")),
            )
        ].append(row)

    tranches: list[dict[str, Any]] = []
    for (state, action), rows in grouped.items():
        rows = sorted(
            rows,
            key=lambda row: (
                str(row.get("source_namespace")),
                _entry_sort_key(str(row.get("candidate_id"))),
            ),
        )
        priority = _tranche_priority(state, action)
        tranches.append(
            {
                "priority": priority,
                "admission_state": state,
                "allowed_next_action": action,
                "candidate_count": len(rows),
                "family_axis_counts": _counter_by(rows, "family_axis"),
                "source_namespace_counts": _counter_by(rows, "source_namespace"),
                "candidate_refs_preview": [_candidate_ref(row) for row in rows[:25]],
                "preview_limit": 25,
                "full_rows_are_in_candidate_rows": True,
            }
        )
    tranches = sorted(
        tranches,
        key=lambda tranche: (
            int(tranche["priority"]),
            -int(tranche["candidate_count"]),
            str(tranche["allowed_next_action"]),
        ),
    )
    for rank, tranche in enumerate(tranches, start=1):
        tranche["rank"] = rank
    return tranches


def build_targeted_expansion_factory_batch(
    *,
    label_expansion_candidates: dict[str, Any],
    external_candidate_freeze: dict[str, Any],
    sequence_cluster_proxy: dict[str, Any] | None = None,
    source_records: dict[str, dict[str, Any]] | None = None,
    artifact_id: str = ARTIFACT_ID,
    created_utc: str | None = None,
    min_target_candidates: int = 500,
    max_target_candidates: int = 1000,
) -> dict[str, Any]:
    source_records = source_records or {
        "label_expansion_candidates": {"path": "<in-memory>", "sha256": "unknown"},
        "external_candidate_freeze": {"path": "<in-memory>", "sha256": "unknown"},
    }
    sequence_rows = _sequence_index(sequence_cluster_proxy or {})
    candidate_rows: list[dict[str, Any]] = []
    for row in _rows(label_expansion_candidates):
        entry_id = str(row.get("entry_id") or "")
        if entry_id in PRIOR_ARCHITECTURE_DEFAULT_ENTRY_IDS:
            continue
        candidate_rows.append(
            _mcsa_candidate_row(
                row,
                sequence_row=sequence_rows.get(entry_id),
                source_records=source_records,
            )
        )
    for row in _rows(external_candidate_freeze):
        candidate_rows.append(
            _external_candidate_row(row, source_records=source_records)
        )

    candidate_rows = _dedupe_candidates(candidate_rows)
    state_audit = _state_assignment_audit(candidate_rows)
    guardrail_audit = _factory_guardrail_audit(
        candidate_rows,
        min_target_candidates=min_target_candidates,
        max_target_candidates=max_target_candidates,
    )
    state_counts = _admission_state_counts(candidate_rows)
    family_axis_counts = _counter_by(candidate_rows, "family_axis")
    source_counts = _counter_by(candidate_rows, "source_namespace")
    tier_counts = _counter_by(candidate_rows, "proposed_label_tier")
    provenance_counts = _counter_by(candidate_rows, "provenance_tier")
    coordinate_counts = _nested_counter(candidate_rows, ("coordinate_availability", "status"))
    action_tranches = _action_tranches(candidate_rows)
    candidate_count = len(candidate_rows)
    below_min = max(0, min_target_candidates - candidate_count)
    above_max = max(0, candidate_count - max_target_candidates)

    return {
        "artifact_id": artifact_id,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc or _utc_now_iso(),
        "status": (
            "targeted_expansion_factory_batch_ready"
            if not below_min and not above_max
            else "targeted_expansion_factory_batch_ready_with_volume_gap"
        ),
        "scope": (
            "Reusable targeted expansion factory batch for diverse atlas growth. "
            "Rows preserve evidence and admission state only; no label import, "
            "registry edit, split edit, threshold edit, or countable promotion is "
            "performed."
        ),
        "target_policy": {
            "min_target_candidates": min_target_candidates,
            "max_target_candidates": max_target_candidates,
            "candidate_volume_gap_to_min": below_min,
            "candidate_volume_over_max": above_max,
            "human_review_required_only_for_countable_promotion": True,
            "prior_architecture_default_rows_excluded": list(
                PRIOR_ARCHITECTURE_DEFAULT_ENTRY_IDS
            ),
        },
        "guardrails": {
            "label_registry_edited": False,
            "ontology_registry_edited": False,
            "imports_or_promotions_performed": False,
            "train_test_splits_changed": False,
            "production_thresholds_changed": False,
            "model_weights_changed": False,
            "heldout_mcsa_rows_used_for_training_or_tuning": False,
            "mechanism_text_ec_rhea_names_or_source_ids_used_as_predictive_features": False,
        },
        "source_artifacts": source_records,
        "counts": {
            "candidate_rows_evaluated": candidate_count,
            "family_axes_evaluated": len(family_axis_counts),
            "admission_state_counts": state_counts,
            "family_axis_counts": family_axis_counts,
            "source_namespace_counts": source_counts,
            "proposed_label_tier_counts": tier_counts,
            "provenance_tier_counts": provenance_counts,
            "coordinate_status_counts": coordinate_counts,
            "countable_candidate_rows": state_counts.get("countable_candidate", 0),
            "ready_for_label_import_rows": 0,
        },
        "state_assignment_audit": state_audit,
        "factory_guardrail_audit": guardrail_audit,
        "action_tranches": action_tranches,
        "first_action_screen_input": _first_action_screen_input(
            candidate_rows,
            action_tranches,
        ),
        "candidate_rows": candidate_rows,
        "acquisition_plan": _acquisition_plan(candidate_rows),
        "recommendation": {
            "first_batch_status": (
                "target_volume_met"
                if candidate_count >= min_target_candidates
                else "largest_defensible_local_batch_below_target"
            ),
            "first_batch_candidate_count": candidate_count,
            "next_batch": (
                "Prioritize external rows with explicit active-site evidence for "
                "sequence/structure duplicate screens, then convert the largest "
                "acquisition_needed external bins through catalytic-residue source "
                "collection."
            ),
        },
    }


def _markdown_report(batch: dict[str, Any]) -> str:
    counts = batch["counts"]
    lines = [
        "# Targeted Expansion Factory Batch - current702",
        "",
        f"- Artifact: `{batch['artifact_id']}`",
        f"- Status: `{batch['status']}`",
        f"- Target volume: {batch['recommendation']['first_batch_status']}",
        f"- Candidate rows: {counts['candidate_rows_evaluated']}",
        f"- Family axes: {counts['family_axes_evaluated']}",
        (
            f"- Countable/import-ready rows: {counts['countable_candidate_rows']} / "
            f"{counts['ready_for_label_import_rows']}"
        ),
        "",
        "## Admission Counts",
        "",
    ]
    for state, count in counts["admission_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Family Axes", ""])
    for axis, count in counts["family_axis_counts"].items():
        lines.append(f"- `{axis}`: {count}")
    lines.extend(["", "## Coordinate Status", ""])
    for status, count in counts["coordinate_status_counts"].items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Proposed Tiers", ""])
    for tier, count in counts["proposed_label_tier_counts"].items():
        lines.append(f"- `{tier}`: {count}")
    lines.extend(["", "## Source Surfaces", ""])
    for source, count in counts["source_namespace_counts"].items():
        lines.append(f"- `{source}`: {count}")
    lines.extend(["", "## Source Hashes", ""])
    for source, record in batch["source_artifacts"].items():
        lines.append(
            f"- `{source}`: `{record['sha256']}` from `{record['path']}`"
        )
    plan = batch["acquisition_plan"]
    audit = batch["factory_guardrail_audit"]
    lines.extend(
        [
            "",
            "## Factory Audit",
            "",
            f"- Passed: {audit['passed']}",
            (
                "- Accession/source-accession coverage complete: "
                f"{audit['accession_or_source_accessions_complete']}"
            ),
            f"- Source hashes complete: {audit['source_hashes_complete']}",
            f"- Family axes complete: {audit['family_axis_complete']}",
            (
                "- Forbidden predictive feature policy clean: "
                f"{audit['forbidden_predictive_feature_policy_clean']}"
            ),
            (
                "- Prior architecture-default rows absent: "
                f"{audit['prior_architecture_default_rows_absent']}"
            ),
            "",
            "## Action Tranches",
            "",
        ]
    )
    for tranche in batch["action_tranches"][:8]:
        lines.append(
            (
                f"{tranche['rank']}. `{tranche['admission_state']}` - "
                f"{tranche['candidate_count']} rows - "
                f"{tranche['allowed_next_action']}"
            )
        )
    if batch["action_tranches"]:
        first_input = batch["first_action_screen_input"]
        lines.extend(
            [
                "",
                "## First Action Preview",
                "",
                (
                    f"- Tranche {first_input['tranche_rank']}: "
                    f"`{first_input['admission_state']}` / "
                    f"{first_input['candidate_count']} rows"
                ),
                f"- Action: {first_input['required_action']}",
            ]
        )
        for ref in first_input["rows"]:
            lines.append(
                (
                    f"- `{ref['candidate_id']}` / `{ref['accession']}` / "
                    f"`{ref['family_axis']}`"
                )
            )
    lines.extend(
        [
            "",
            "## Blockers And Next Batch",
            "",
            f"- Acquisition-needed rows: {plan['counts']['acquisition_needed_rows']}",
            (
                "- Blocked family-decision rows: "
                f"{plan['counts']['blocked_family_decision_rows']}"
            ),
            f"- Blocked locator rows: {plan['counts']['blocked_locator_rows']}",
            f"- Blocked coordinate rows: {plan['counts']['blocked_coordinate_rows']}",
            "",
            "## Mechanical Next Steps",
            "",
        ]
    )
    for item in plan["next_mechanical_steps"]:
        lines.append(f"{item['rank']}. {item['action']}")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            (
                "- No labels, registries, ontologies, imports, splits, thresholds, "
                "or model weights were changed."
            ),
            (
                "- Mechanism text, EC/Rhea IDs, names, labels, target names, and "
                "source IDs are preserved only as provenance/review context and "
                "are not scoring inputs."
            ),
            "- Human review is required only to cross a countable-promotion boundary.",
            "",
        ]
    )
    return "\n".join(lines)


def write_targeted_expansion_factory_batch(
    *,
    label_expansion_candidates_path: Path,
    external_candidate_freeze_path: Path,
    sequence_cluster_proxy_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    artifact_id: str = ARTIFACT_ID,
    created_utc: str | None = None,
    min_target_candidates: int = 500,
    max_target_candidates: int = 1000,
) -> dict[str, Any]:
    label_expansion_candidates = _read_json_object(label_expansion_candidates_path)
    external_candidate_freeze = _read_json_object(external_candidate_freeze_path)
    sequence_cluster_proxy = _read_json_object(sequence_cluster_proxy_path)
    source_records = {
        "label_expansion_candidates": _source_record(label_expansion_candidates_path),
        "external_candidate_freeze": _source_record(external_candidate_freeze_path),
        "sequence_cluster_proxy": _source_record(sequence_cluster_proxy_path),
    }
    batch = build_targeted_expansion_factory_batch(
        label_expansion_candidates=label_expansion_candidates,
        external_candidate_freeze=external_candidate_freeze,
        sequence_cluster_proxy=sequence_cluster_proxy,
        source_records=source_records,
        artifact_id=artifact_id,
        created_utc=created_utc,
        min_target_candidates=min_target_candidates,
        max_target_candidates=max_target_candidates,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(batch, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_markdown_report(batch) + "\n", encoding="utf-8")
    return batch
