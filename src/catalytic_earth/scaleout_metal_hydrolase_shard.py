from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_ID = "v3_scaleout_metal_hydrolase_shard_current702_20260608"
SCHEMA_VERSION = "v3.scaleout_metal_hydrolase_shard"

DEFAULT_OUT_PATH = Path(
    "artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json"
)
DEFAULT_REPORT_PATH = Path(
    "work/scaleout_metal_hydrolase_shard_current702_20260608.md"
)
DEFAULT_HANDOFF_PATH = Path("work/handoff_metal_hydrolase_shard_20260608.md")

DEFAULT_SOURCE_PATHS = {
    "targeted_expansion_factory_batch": Path(
        "artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json"
    ),
    "targeted_expansion_acquisition_conversion_screens": Path(
        "artifacts/"
        "v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json"
    ),
    "external_metal_hydrolase_tail_panel": Path(
        "artifacts/v3_external_metal_hydrolase_tail_panel_20260528.json"
    ),
    "no_reliable_structure_metal_hydrolase_controls": Path(
        "artifacts/"
        "v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json"
    ),
    "metal_phosphatase_minicampaign_freeze": Path(
        "artifacts/v3_prospective_external_metal_phosphatase_minicampaign_freeze_20260521.json"
    ),
    "metal_phosphatase_minicampaign_decision_packet": Path(
        "artifacts/v3_prospective_external_metal_phosphatase_minicampaign_decision_packet_20260521.json"
    ),
    "metal_phosphatase_minicampaign_baseline_comparison": Path(
        "artifacts/v3_metal_phosphatase_minicampaign_baseline_comparison_20260521.json"
    ),
    "metal_phosphatase_deep_terminal_after_chunked_duplicate": Path(
        "artifacts/"
        "v3_metal_phosphatase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json"
    ),
    "metal_phosphatase_deep_terminal_second_after_q99504_duplicate": Path(
        "artifacts/"
        "v3_metal_phosphatase_deep_terminal_decision_packet_second_after_q99504_duplicate_closure_20260521.json"
    ),
    "metal_phosphatase_deep_terminal_remaining_after_source_free_geometry": Path(
        "artifacts/"
        "v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_source_free_geometry_20260521.json"
    ),
    "metal_phosphatase_second_timeout_targeted_rescue_screen": Path(
        "artifacts/"
        "v3_metal_phosphatase_deep_packet_second_timeout_targeted_rescue_screen_20260521.json"
    ),
    "external_metal_phosphatase_review_ready_specificity_blocker": Path(
        "artifacts/"
        "v3_external_metal_phosphatase_review_ready_phosphate_specificity_blocker_packet_20260522.json"
    ),
}

TERMINAL_STATES = (
    "countable_candidate_preflight_only",
    "review_only_evidence",
    "reject/OOS_preserve_signal",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
)

STATE_PRIORITY = {
    "reject/OOS_preserve_signal": 0,
    "countable_candidate_preflight_only": 1,
    "blocked_family_decision": 2,
    "blocked_locator": 3,
    "blocked_coordinate": 4,
    "review_only_evidence": 5,
}

SUBFAMILY_PRIORITY = {
    "zinc_metalloprotease_zincin": 0,
    "binuclear_metallohydrolase_amidohydrolase": 1,
    "phosphatase_phosphoesterase": 2,
    "nuclease_phosphoesterase": 3,
    "metallo_beta_lactamase_like": 4,
    "sulfatase_fgly_metal_boundary": 5,
    "carbonic_anhydrase_dehydratase_boundary": 6,
    "ntpase_nucleotide_hydrolase_boundary": 7,
    "metal_dependent_nonhydrolytic_negative": 8,
    "no_reliable_structure_metal_hydrolase_controls": 9,
    "metal_hydrolase_general_review_queue": 20,
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


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    for key in (
        "rows",
        "candidate_rows",
        "row_evidence",
        "queue_rows",
        "review_items",
        "results",
        "entries",
    ):
        rows = payload.get(key)
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
        if isinstance(rows, dict):
            return [row for row in rows.values() if isinstance(row, dict)]
    panel = payload.get("panel")
    if isinstance(panel, dict) and isinstance(panel.get("candidate_rows"), list):
        return [{"entry_id": row_id} for row_id in panel["candidate_rows"]]
    return []


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _strip_uniprot(value: Any) -> str:
    text = str(value)
    if text.startswith("uniprot:"):
        return text.split(":", 1)[1]
    return text


def _candidate_id(row: dict[str, Any]) -> str | None:
    for key in ("candidate_id", "row_id", "entry_id", "accession"):
        value = row.get(key)
        if value in (None, ""):
            continue
        text = str(value)
        if key == "accession" and not text.startswith(("m_csa:", "mh_", "uniprot:")):
            return f"uniprot:{text}"
        return text
    return None


def _accession_from_candidate(candidate_id: str) -> str | None:
    if candidate_id.startswith("uniprot:"):
        return candidate_id.split(":", 1)[1]
    if candidate_id.startswith("m_csa:") or candidate_id.startswith("mh_"):
        return candidate_id
    return None


def _sort_key(candidate_id: str) -> tuple[int, str, str]:
    if candidate_id.startswith("m_csa:"):
        suffix = candidate_id.split(":", 1)[1]
        return (0, f"{int(suffix):09d}" if suffix.isdigit() else suffix, candidate_id)
    if candidate_id.startswith("mh_"):
        suffix = candidate_id.split("_", 1)[1]
        return (1, f"{int(suffix):09d}" if suffix.isdigit() else suffix, candidate_id)
    if candidate_id.startswith("uniprot:"):
        return (2, candidate_id.split(":", 1)[1], candidate_id)
    return (3, candidate_id, candidate_id)


def _new_candidate(candidate_id: str) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "accession": _accession_from_candidate(candidate_id),
        "display_names": [],
        "candidate_roles": [],
        "state_votes": [],
        "subfamily_votes": [],
        "confidence_votes": [],
        "active_site_sources": [],
        "coordinate_sources": [],
        "metal_ligand_sources": [],
        "duplicate_screen_sources": [],
        "source_free_preflight_sources": [],
        "next_steps": [],
        "terminal_blockers": [],
        "source_hashes": {},
        "source_contributions": [],
    }


def _candidate(
    records: dict[str, dict[str, Any]], candidate_id: str
) -> dict[str, Any]:
    return records.setdefault(candidate_id, _new_candidate(candidate_id))


def _append_unique(values: list[Any], value: Any) -> None:
    if value in (None, "", [], {}):
        return
    if value not in values:
        values.append(value)


def _merge_list(values: list[Any]) -> list[Any]:
    merged: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value in (None, "", [], {}):
            continue
        key = json.dumps(value, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            merged.append(value)
    return merged


def _contribute(
    record: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
    source_row: dict[str, Any],
    contribution_role: str,
) -> None:
    record["source_hashes"][source_key] = source_record["sha256"]
    record["source_contributions"].append(
        {
            "source_key": source_key,
            "path": source_record["path"],
            "source_artifact_sha256": source_record["sha256"],
            "source_row_sha256": _canonical_sha256(source_row),
            "contribution_role": contribution_role,
            "terminal_hint": (
                source_row.get("terminal_state")
                or source_row.get("admission_state")
                or source_row.get("terminal_decision")
                or source_row.get("terminal_decision_after_targeted_probe")
                or source_row.get("candidate_role")
                or source_row.get("score_status")
            ),
        }
    )


def _first_text(row: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return str(value)
    return None


def _contains(text: str, *needles: str) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def _infer_subfamily_from_text(row: dict[str, Any]) -> str:
    text = " ".join(
        str(row.get(key, ""))
        for key in (
            "display_name",
            "protein_name",
            "name",
            "entry_name",
            "rationale",
            "terminal_decision_reason",
        )
    )
    if _contains(text, "carbonic anhydrase", "dehydratase"):
        return "carbonic_anhydrase_dehydratase_boundary"
    if _contains(text, "sulfatase", "sulphatase", "sulfate", "sulphate"):
        return "sulfatase_fgly_metal_boundary"
    if _contains(text, "beta-lactamase", "metallo-beta", "glyoxalase", "lactamase"):
        return "metallo_beta_lactamase_like"
    if _contains(
        text,
        "nuclease",
        "endonuclease",
        "exonuclease",
        "ribonuclease",
        "dnase",
        "rnase",
        "phosphodiesterase",
    ):
        return "nuclease_phosphoesterase"
    if _contains(text, "phosphatase", "phosphoesterase", "nucleotidase"):
        return "phosphatase_phosphoesterase"
    if _contains(
        text,
        "protease",
        "peptidase",
        "carboxypeptidase",
        "aminopeptidase",
        "metalloprote",
        "thermolysin",
        "neprilysin",
        "leishmanolysin",
        "stromelysin",
    ):
        return "zinc_metalloprotease_zincin"
    if _contains(
        text,
        "urease",
        "amidohydrolase",
        "deaminase",
        "hydrolase domain",
        "dihydroorotase",
        "creatininase",
        "prolidase",
        "hydantoinase",
    ):
        return "binuclear_metallohydrolase_amidohydrolase"
    if _contains(text, "atpase", "gtpase", "ntpase", "nucleotide", "helicase"):
        return "ntpase_nucleotide_hydrolase_boundary"
    if _contains(
        text,
        "oxidase",
        "oxygenase",
        "dioxygenase",
        "reductase",
        "dehydrogenase",
        "transferase",
        "lyase",
        "synthase",
        "ligase",
        "peroxidase",
    ):
        return "metal_dependent_nonhydrolytic_negative"
    return "metal_hydrolase_general_review_queue"


def _factory_terminal_state(row: dict[str, Any]) -> str:
    state = str(row.get("admission_state") or "")
    if state == "countable_candidate":
        return "countable_candidate_preflight_only"
    if state in TERMINAL_STATES:
        return state
    if state == "acquisition_needed":
        return "blocked_family_decision"
    return "review_only_evidence"


def _tail_terminal_state(row: dict[str, Any]) -> str:
    role = str(row.get("candidate_role") or "")
    if role in {"oos_hard_negative", "external_hard_negative", "near_family_hard_negative"}:
        return "reject/OOS_preserve_signal"
    if row.get("ready_for_label_import") is True and row.get("countable_label_candidate") is True:
        return "countable_candidate_preflight_only"
    return "review_only_evidence"


def _no_reliable_terminal_state(row: dict[str, Any]) -> str:
    role = str(row.get("evidence_role") or "")
    if "oos" in role.lower() or "control" in role.lower():
        return "reject/OOS_preserve_signal"
    status = str(row.get("predicted_geometry_status") or "")
    if status == "missing":
        return "blocked_coordinate"
    return "review_only_evidence"


def _metal_phosphatase_terminal_state(row: dict[str, Any]) -> str:
    if row.get("countable_label_candidate") is True and row.get("ready_for_label_import") is True:
        return "countable_candidate_preflight_only"
    decision = str(
        row.get("terminal_decision")
        or row.get("terminal_decision_after_targeted_probe")
        or row.get("phosphatase_specific_import_status")
        or ""
    )
    if "duplicate" in decision or "rejection" in decision:
        return "reject/OOS_preserve_signal"
    if "mechanism_match_review_ready" in decision:
        return "blocked_family_decision"
    if "needs_new_extractor" in decision or "blocked_with_exact_missing_evidence" in decision:
        return "blocked_family_decision"
    geometry_status = str(
        row.get("geometry_retrieval_status")
        or row.get("production_score_status")
        or row.get("score_status")
        or row.get("score_status_at_selection")
        or ""
    )
    coordinate_status = str(row.get("coordinate_status") or "")
    if "geometry_missing" in geometry_status or "not_run" in geometry_status:
        return "blocked_coordinate"
    if "not_scored" in geometry_status and "coordinate_sidecar_materialized" not in coordinate_status:
        return "blocked_coordinate"
    if row.get("exact_missing_evidence_to_resolve") or row.get("remaining_import_blockers"):
        return "blocked_family_decision"
    return "review_only_evidence"


def _confidence_from_state(record: dict[str, Any], terminal_state: str) -> str:
    if terminal_state == "reject/OOS_preserve_signal":
        if any(
            "duplicate" in str(screen).lower()
            for screen in record["duplicate_screen_sources"]
        ):
            return "tier_A_duplicate_or_oos_signal"
        return "tier_B_boundary_or_oos_signal"
    if terminal_state == "countable_candidate_preflight_only":
        return "tier_A_source_free_preflight_import_not_performed"
    if record["candidate_id"].startswith("m_csa:"):
        return "tier_A_curated_anchor_review_only"
    if terminal_state in {"blocked_locator", "blocked_coordinate"}:
        return "tier_C_repair_queue"
    if terminal_state == "blocked_family_decision":
        return "tier_B_source_free_preflight_blocked"
    return "tier_B_review_only_candidate"


def _merge_factory_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    if row.get("family_axis") != "metal_hydrolase_subclasses":
        return
    candidate_id = str(row["candidate_id"])
    record = _candidate(records, candidate_id)
    _contribute(record, source_key, source_record, row, "factory_metal_axis_row")
    _append_unique(record["display_names"], row.get("display_name"))
    _append_unique(record["candidate_roles"], row.get("proposed_label_tier"))
    record["state_votes"].append(_factory_terminal_state(row))
    record["subfamily_votes"].append(_infer_subfamily_from_text(row))
    _append_unique(record["next_steps"], row.get("allowed_next_action"))
    mechanical = row.get("mechanical_unblock_requirements") or {}
    _append_unique(record["next_steps"], mechanical.get("allowed_next_action"))
    for blocker in _as_list(mechanical.get("readiness_blockers")):
        _append_unique(record["terminal_blockers"], blocker)
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "status": "factory_active_site_or_locator_evidence",
            **(row.get("active_site_or_locator_evidence") or {}),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            **(row.get("predicted_coordinate_or_provenance_availability") or {}),
        }
    )
    record["metal_ligand_sources"].append(
        {
            "source_key": source_key,
            **(row.get("cofactor_or_metal_evidence") or {}),
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "factory_fold_tm_or_near_neighbor_signal",
            "status": "near_neighbor_signal_present"
            if row.get("fold_tm_or_near_neighbor_signal")
            else "not_available_in_factory_axis",
            "fold_tm_or_near_neighbor_signal": row.get("fold_tm_or_near_neighbor_signal"),
            "geometry_or_reconstruction_status": row.get(
                "geometry_or_reconstruction_status"
            ),
            "source_separation_role": (
                "factory routing/provenance only; no mechanism text or source IDs "
                "used as predictive scoring features"
            ),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "admission_route_basis": row.get("admission_route_basis"),
            "proposed_label_tier": row.get("proposed_label_tier"),
            "rationale": row.get("rationale"),
            "guardrails": {
                "import_or_promotion_performed": False,
                "countable_label_candidate": row.get("admission_state")
                == "countable_candidate",
                "ready_for_label_import": False,
            },
            "row_context_sha256": row.get("row_context_sha256"),
        }
    )


def _merge_tail_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = _candidate_id(row)
    if candidate_id is None:
        return
    record = _candidate(records, candidate_id)
    if row.get("accession") not in (None, ""):
        record["accession"] = str(row["accession"])
    _contribute(record, source_key, source_record, row, "subclass_tail_panel_row")
    _append_unique(record["display_names"], _first_text(row, "name", "protein_name"))
    _append_unique(record["candidate_roles"], row.get("candidate_role"))
    record["state_votes"].append(_tail_terminal_state(row))
    record["subfamily_votes"].append(
        str(row.get("lane") or _infer_subfamily_from_text(row))
    )
    _append_unique(
        record["next_steps"],
        "preserve as review-only subclass evidence; run source-free duplicate, "
        "locator, and label-factory screens before any promotion",
    )
    if _tail_terminal_state(row) == "reject/OOS_preserve_signal":
        _append_unique(
            record["next_steps"],
            "preserve the hard-negative/OOS boundary signal and do not import",
        )
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "status": "tail_panel_subclass_locator_context",
            "geometry_class": row.get("geometry_class"),
            "evidence_summary": row.get("evidence_summary"),
            "expected_router_behavior": row.get("expected_router_behavior"),
            "foldseek_neighbor_expectation": row.get("foldseek_neighbor_expectation"),
            "sequence_neighbor_expectation": row.get("sequence_neighbor_expectation"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "status": "tail_panel_structure_availability",
            **(row.get("structure_availability") or {}),
        }
    )
    record["metal_ligand_sources"].append(
        {
            "source_key": source_key,
            "metal_ligand_state": row.get("metal_ligand_state"),
            "ligand_or_substrate_state": row.get("ligand_or_substrate_state"),
            "observed_ligand_codes": row.get("observed_ligand_codes") or [],
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "tail_panel_expectation_only",
            "status": "duplicate_screen_not_run_in_tail_panel",
            "foldseek_neighbor_expectation": row.get("foldseek_neighbor_expectation"),
            "sequence_neighbor_expectation": row.get("sequence_neighbor_expectation"),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "selection_frozen_before_scoring": row.get("selection_frozen_before_scoring"),
            "predictive_use_allowed": row.get("predictive_use_allowed"),
            "ready_for_label_import": row.get("ready_for_label_import"),
            "current_v1_state": row.get("current_v1_state"),
            "readiness_tier": row.get("readiness_tier"),
            "provenance_tier": row.get("provenance_tier"),
        }
    )


def _merge_no_reliable_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = _candidate_id(row)
    if candidate_id is None:
        return
    record = _candidate(records, candidate_id)
    _contribute(
        record,
        source_key,
        source_record,
        row,
        "no_reliable_structure_metal_hydrolase_control_row",
    )
    _append_unique(record["candidate_roles"], row.get("evidence_role"))
    record["state_votes"].append(_no_reliable_terminal_state(row))
    record["subfamily_votes"].append("no_reliable_structure_metal_hydrolase_controls")
    _append_unique(
        record["next_steps"],
        "repair predicted geometry and source-free locator evidence before any "
        "family-promotion discussion",
    )
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "status": "predicted_geometry_and_fold_channel_control",
            "predicted_geometry_status": row.get("predicted_geometry_status"),
            "predicted_geometry_top1": row.get("predicted_geometry_top1"),
            "evidence_role": row.get("evidence_role"),
        }
    )
    record["coordinate_sources"].append(
        {
            "source_key": source_key,
            "predicted_geometry_status": row.get("predicted_geometry_status"),
            "predicted_geometry_accession_repair": row.get(
                "predicted_geometry_accession_repair"
            ),
            "predicted_structure_fold_channel": row.get("predicted_structure_fold_channel"),
        }
    )
    record["metal_ligand_sources"].append(
        {
            "source_key": source_key,
            "selected_organic_cofactor_scores": row.get(
                "selected_organic_cofactor_scores"
            ),
            "selected_organic_cofactor_max": row.get("selected_organic_cofactor_max"),
        }
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "predicted_structure_fold_channel",
            "status": "fold_channel_boundary_signal",
            "predicted_structure_fold_channel": row.get("predicted_structure_fold_channel"),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "predicted_geometry_score_source": row.get("predicted_geometry_score_source"),
            "predicted_atlas_geometry_variant_scores": row.get(
                "predicted_atlas_geometry_variant_scores"
            ),
            "split_assignment": row.get("split_assignment"),
        }
    )


def _metal_phosphatase_contribution_role(source_key: str) -> str:
    if "freeze" in source_key:
        return "metal_phosphatase_frozen_candidate"
    if "baseline" in source_key:
        return "metal_phosphatase_baseline_or_duplicate_context"
    if "terminal" in source_key:
        return "metal_phosphatase_terminal_decision"
    if "specificity" in source_key:
        return "metal_phosphatase_source_free_specificity_blocker"
    return "metal_phosphatase_evidence"


def _merge_metal_phosphatase_row(
    records: dict[str, dict[str, Any]],
    row: dict[str, Any],
    source_key: str,
    source_record: dict[str, Any],
) -> None:
    candidate_id = _candidate_id(row)
    if candidate_id is None:
        return
    record = _candidate(records, candidate_id)
    _contribute(
        record,
        source_key,
        source_record,
        row,
        _metal_phosphatase_contribution_role(source_key),
    )
    _append_unique(record["display_names"], _first_text(row, "protein_name", "entry_name"))
    _append_unique(record["candidate_roles"], row.get("terminal_decision"))
    _append_unique(record["candidate_roles"], row.get("score_status"))
    terminal_state = _metal_phosphatase_terminal_state(row)
    record["state_votes"].append(terminal_state)
    record["subfamily_votes"].append("phosphatase_phosphoesterase")
    for step in _as_list(row.get("exact_missing_evidence_to_resolve")):
        _append_unique(record["next_steps"], step)
    for blocker in _as_list(row.get("remaining_import_blockers")):
        _append_unique(record["terminal_blockers"], blocker)
    _append_unique(record["terminal_blockers"], row.get("exact_blocker_if_not_terminal"))
    if terminal_state == "blocked_coordinate":
        _append_unique(
            record["next_steps"],
            "materialize source-free geometry and structural duplicate screens for "
            "the frozen phosphatase candidate",
        )
    if terminal_state == "blocked_family_decision":
        _append_unique(
            record["next_steps"],
            "build or preregister source-free phosphate/substrate-pocket evidence, "
            "then rerun review and label-factory gates",
        )
    if terminal_state == "reject/OOS_preserve_signal":
        _append_unique(
            record["next_steps"],
            "preserve the duplicate or insufficient-evidence rejection signal and "
            "do not import without new evidence",
        )
    active_site = row.get("catalytic_residue_metal_phosphate_evidence") or {}
    if not active_site:
        active_site = {
            "active_site_feature_count": row.get("active_site_count"),
            "binding_site_feature_count": row.get("binding_site_count"),
            "metal_binding_feature_count": row.get("metal_binding_site_count"),
        }
    record["active_site_sources"].append(
        {
            "source_key": source_key,
            "status": "metal_phosphatase_active_site_context",
            **active_site,
        }
    )
    coordinate = row.get("structure_pdb_evidence_availability") or {}
    if not coordinate:
        coordinate = {
            "coordinate_path": row.get("coordinate_path"),
            "coordinate_status": row.get("coordinate_status"),
            "pdb_ids_sample": row.get("pdb_ids_sample"),
            "selected_pdb_id": row.get("selected_pdb_id_for_probe")
            or row.get("structure_id"),
            "structure_source": row.get("structure_source"),
        }
    record["coordinate_sources"].append({"source_key": source_key, **coordinate})
    record["metal_ligand_sources"].append(
        {
            "source_key": source_key,
            "metal_binding_site_count": row.get("metal_binding_site_count"),
            "binding_ligand_names_sample": active_site.get("binding_ligand_names_sample"),
            "source_free_phosphate_specificity_scan": row.get(
                "source_free_phosphate_specificity_scan"
            ),
        }
    )
    duplicate_screen = (
        row.get("duplicate_leakage_screen")
        or row.get("foldseek_tm_sidecar")
        or row.get("foldseek_current_countable_sidecar")
        or row.get("nearest_current_countable_hit")
    )
    sequence_screen = (
        row.get("deterministic_sequence_kmer_nearest_neighbor")
        or row.get("review_context")
        or {}
    )
    record["duplicate_screen_sources"].append(
        {
            "source_key": source_key,
            "screen": "metal_phosphatase_duplicate_or_sequence_context",
            "status": row.get("targeted_current_metal_screen_status")
            or row.get("targeted_current_subset_screen_status")
            or row.get("terminal_decision")
            or row.get("terminal_decision_after_targeted_probe")
            or row.get("sequence_baseline_signal")
            or "review_context_only",
            "duplicate_leakage_screen": duplicate_screen,
            "sequence_context": sequence_screen,
            "source_separation_role": (
                "duplicate/leakage and review context only; EC/name/prose fields "
                "are not predictive scoring inputs"
            ),
        }
    )
    record["source_free_preflight_sources"].append(
        {
            "source_key": source_key,
            "terminal_decision": row.get("terminal_decision")
            or row.get("terminal_decision_after_targeted_probe"),
            "current_geometry_retrieval_score_summary": row.get(
                "current_geometry_retrieval_score_summary"
            )
            or row.get("current_geometry_retrieval_triage"),
            "geometry_summary": row.get("geometry_summary"),
            "phosphatase_specific_import_status": row.get(
                "phosphatase_specific_import_status"
            ),
            "ready_for_label_import": row.get("ready_for_label_import"),
            "countable_label_candidate": row.get("countable_label_candidate"),
            "source_separation": row.get("source_separation"),
        }
    )


def _load_sources(
    source_paths: dict[str, Path],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, str]]:
    payloads: dict[str, Any] = {}
    source_records: dict[str, dict[str, Any]] = {}
    missing: dict[str, str] = {}
    for source_key, path in source_paths.items():
        if not path.exists():
            missing[source_key] = str(path)
            continue
        payloads[source_key] = _read_json(path)
        source_records[source_key] = _source_record(path)
    return payloads, source_records, missing


def _merge_source_rows(
    payloads: dict[str, Any], source_records: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for source_key, payload in payloads.items():
        rows = _rows_from_payload(payload)
        if source_key == "targeted_expansion_factory_batch":
            for row in rows:
                _merge_factory_row(records, row, source_key, source_records[source_key])
        elif source_key == "external_metal_hydrolase_tail_panel":
            for row in rows:
                _merge_tail_row(records, row, source_key, source_records[source_key])
        elif source_key == "no_reliable_structure_metal_hydrolase_controls":
            for row in rows:
                _merge_no_reliable_row(
                    records, row, source_key, source_records[source_key]
                )
        elif source_key == "targeted_expansion_acquisition_conversion_screens":
            for row in rows:
                if row.get("family_axis") != "metal_hydrolase_subclasses":
                    continue
                _merge_metal_phosphatase_row(
                    records, row, source_key, source_records[source_key]
                )
        elif source_key.startswith("metal_phosphatase") or source_key.startswith(
            "external_metal_phosphatase"
        ):
            for row in rows:
                _merge_metal_phosphatase_row(
                    records, row, source_key, source_records[source_key]
                )
    return records


def _choose_subfamily(record: dict[str, Any]) -> str:
    lanes = _merge_list(record["subfamily_votes"])
    if not lanes:
        return "metal_hydrolase_general_review_queue"
    return sorted(lanes, key=lambda lane: (SUBFAMILY_PRIORITY.get(str(lane), 99), str(lane)))[
        0
    ]


def _choose_terminal_state(record: dict[str, Any]) -> str:
    states = [state for state in record["state_votes"] if state in TERMINAL_STATES]
    if not states:
        return "review_only_evidence"
    return sorted(states, key=lambda state: STATE_PRIORITY[state])[0]


def _extract_status_counts(sources: list[dict[str, Any]], *keys: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for source in sources:
        for key in keys:
            for value in _as_list(source.get(key)):
                if value not in (None, "", [], {}):
                    counts[str(value)] += 1
    return dict(sorted(counts.items()))


def _coordinate_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    paths: list[str] = []
    pdb_ids: list[str] = []
    alphafold_ids: list[str] = []
    statuses: list[str] = []
    selected: list[str] = []
    for source in sources:
        for key in ("coordinate_path", "alphafold_coordinate_path"):
            for value in _as_list(source.get(key)):
                if value:
                    paths.append(str(value))
        for key in ("pdb_ids", "pdb_ids_sample"):
            for value in _as_list(source.get(key)):
                if value:
                    pdb_ids.append(str(value))
        for value in _as_list(source.get("alphafold_ids")):
            if value:
                alphafold_ids.append(str(value))
        for key in (
            "coordinate_status",
            "status",
            "predicted_geometry_status",
            "structure_source",
        ):
            value = source.get(key)
            if value not in (None, "", [], {}):
                statuses.append(str(value))
        for key in ("selected_structure", "selected_structure_id", "selected_pdb_id"):
            value = source.get(key)
            if value not in (None, "", [], {}):
                selected.append(str(value))
    return {
        "coordinate_paths": sorted(set(paths)),
        "pdb_ids": sorted(set(pdb_ids)),
        "alphafold_ids": sorted(set(alphafold_ids)),
        "selected_structures": sorted(set(selected)),
        "status_counts": dict(Counter(statuses)),
        "coordinate_or_provenance_available": bool(paths or pdb_ids or alphafold_ids or selected),
        "source_specific": sources,
    }


def _active_site_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    numeric_keys = (
        "active_site_feature_count",
        "binding_site_feature_count",
        "resolved_residue_count",
        "metal_binding_feature_count",
        "metal_binding_feature_count_from_freeze",
    )
    maxima: dict[str, int] = {}
    blockers: list[str] = []
    gap_classes: list[str] = []
    for source in sources:
        for key in numeric_keys:
            value = source.get(key)
            if isinstance(value, int):
                maxima[key] = max(maxima.get(key, 0), value)
        for value in _as_list(source.get("readiness_blockers")):
            blockers.append(str(value))
        for value in _as_list(source.get("local_evidence_gap_classes")):
            gap_classes.append(str(value))
    return {
        **maxima,
        "status_counts": _extract_status_counts(
            sources,
            "status",
            "active_site_evidence_status",
            "predicted_geometry_status",
            "geometry_class",
        ),
        "readiness_blockers": sorted(set(blockers)),
        "local_evidence_gap_classes": sorted(set(gap_classes)),
        "source_specific": sources,
    }


def _metal_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    ligand_codes: list[str] = []
    cofactor_families: list[str] = []
    ligand_names: list[str] = []
    states: list[str] = []
    for source in sources:
        for key in ("observed_ligand_codes", "cofactor_families"):
            for value in _as_list(source.get(key)):
                if key == "observed_ligand_codes":
                    ligand_codes.append(str(value))
                else:
                    cofactor_families.append(str(value))
        for value in _as_list(source.get("binding_ligand_names_sample")):
            ligand_names.append(str(value))
        for key in (
            "metal_ligand_state",
            "ligand_or_substrate_state",
            "cofactor_evidence_level",
        ):
            value = source.get(key)
            if value not in (None, "", [], {}):
                states.append(str(value))
    return {
        "observed_ligand_codes": sorted(set(ligand_codes)),
        "binding_ligand_names_sample": sorted(set(ligand_names)),
        "cofactor_families": sorted(set(cofactor_families)),
        "state_summaries": sorted(set(states)),
        "source_specific": sources,
    }


def _duplicate_summary(sources: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: list[str] = []
    screens: list[str] = []
    nearest_hits: list[Any] = []
    for source in sources:
        for key in ("status", "screen"):
            value = source.get(key)
            if value not in (None, "", [], {}):
                if key == "status":
                    statuses.append(str(value))
                else:
                    screens.append(str(value))
        duplicate = source.get("duplicate_leakage_screen")
        if isinstance(duplicate, dict):
            nearest = duplicate.get("nearest_current_metal_hit") or duplicate.get(
                "nearest_current_countable_hit"
            )
            if nearest:
                nearest_hits.append(nearest)
        nearest = source.get("nearest_current_countable_hit")
        if nearest:
            nearest_hits.append(nearest)
    return {
        "status_counts": dict(Counter(statuses)),
        "screen_types": sorted(set(screens)),
        "nearest_current_hits_sample": nearest_hits[:5],
        "source_specific": sources,
    }


def _default_next_step(terminal_state: str) -> str:
    return {
        "countable_candidate_preflight_only": (
            "hold for Vivek/main-thread controlled-promotion decision; do not "
            "import automatically"
        ),
        "review_only_evidence": (
            "preserve as review-only family evidence until explicit promotion "
            "gates pass"
        ),
        "reject/OOS_preserve_signal": (
            "preserve the non-counting rejection/OOS/duplicate signal and do not "
            "import without new evidence"
        ),
        "blocked_locator": (
            "repair source-free residue mapping or active-site locator evidence"
        ),
        "blocked_coordinate": (
            "materialize or approve a valid coordinate/provenance source before "
            "source-free scoring"
        ),
        "blocked_family_decision": (
            "resolve the source-free subclass decision or extractor blocker, then "
            "rerun pre-promotion gates"
        ),
    }[terminal_state]


def _machine_steps_for_terminal(
    terminal_state: str, next_steps: list[Any]
) -> list[str]:
    cleaned = [str(step) for step in _merge_list(next_steps) if str(step)]
    needles = {
        "countable_candidate_preflight_only": (
            "hold",
            "controlled-promotion",
            "do not import",
        ),
        "review_only_evidence": ("review-only", "promotion gates", "preserve"),
        "reject/OOS_preserve_signal": (
            "preserve the duplicate",
            "oos",
            "hard-negative",
            "rejection",
            "do not import",
            "preserve as non-counting",
        ),
        "blocked_locator": ("locator", "residue mapping", "active-site"),
        "blocked_coordinate": ("coordinate", "geometry", "materialize", "structure"),
        "blocked_family_decision": (
            "phosphate",
            "substrate",
            "extractor",
            "family",
            "label-factory",
            "subclass",
        ),
    }[terminal_state]
    preferred: list[str] = []
    for step in cleaned:
        lowered = step.lower()
        if any(needle in lowered for needle in needles):
            preferred.append(step)
    if not preferred:
        preferred.append(_default_next_step(terminal_state))
    ordered = preferred + cleaned + [_default_next_step(terminal_state)]
    deduped: list[str] = []
    seen: set[str] = set()
    for step in ordered:
        if step not in seen:
            seen.add(step)
            deduped.append(step)
    return deduped


def _finalize_record(record: dict[str, Any]) -> dict[str, Any]:
    terminal_state = _choose_terminal_state(record)
    subfamily = _choose_subfamily(record)
    next_steps = _machine_steps_for_terminal(terminal_state, record["next_steps"])
    candidate_roles = _merge_list(record["candidate_roles"])
    display_name = record["display_names"][0] if record["display_names"] else None
    row = {
        "candidate_id": record["candidate_id"],
        "accession": record["accession"],
        "display_name": display_name,
        "proposed_family_lane": "metal_hydrolase_subclasses",
        "proposed_subfamily_lane": subfamily,
        "terminal_state": terminal_state,
        "candidate_roles": candidate_roles,
        "confidence_tier": _confidence_from_state(record, terminal_state),
        "active_site_or_locator_evidence": _active_site_summary(
            record["active_site_sources"]
        ),
        "coordinate_or_provenance_status": _coordinate_summary(
            record["coordinate_sources"]
        ),
        "ligand_cofactor_metal_evidence": _metal_summary(
            record["metal_ligand_sources"]
        ),
        "duplicate_screens": _duplicate_summary(record["duplicate_screen_sources"]),
        "source_free_preflight": {
            "status": "source_free_preflight_or_review_context_available"
            if record["source_free_preflight_sources"]
            else "source_free_preflight_not_available",
            "guardrail": (
                "candidate/evidence lane only; no imports, promotions, registry "
                "edits, threshold changes, heldout training, or tuning"
            ),
            "source_specific": record["source_free_preflight_sources"],
        },
        "source_hashes": dict(sorted(record["source_hashes"].items())),
        "source_contributions": record["source_contributions"],
        "terminal_blockers": sorted(set(str(value) for value in record["terminal_blockers"])),
        "machine_actionable_next_step": next_steps[0],
        "machine_actionable_next_steps": next_steps,
    }
    row["row_context_sha256"] = _canonical_sha256(
        {
            "candidate_id": row["candidate_id"],
            "terminal_state": row["terminal_state"],
            "proposed_subfamily_lane": row["proposed_subfamily_lane"],
            "source_contributions": row["source_contributions"],
        }
    )
    return row


def _validate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [row["candidate_id"] for row in rows]
    duplicate_ids = sorted(
        candidate_id for candidate_id, count in Counter(ids).items() if count > 1
    )
    invalid_states = sorted(
        {
            row.get("terminal_state")
            for row in rows
            if row.get("terminal_state") not in TERMINAL_STATES
        }
    )
    missing_required = []
    required_keys = {
        "candidate_id",
        "proposed_family_lane",
        "proposed_subfamily_lane",
        "terminal_state",
        "active_site_or_locator_evidence",
        "coordinate_or_provenance_status",
        "ligand_cofactor_metal_evidence",
        "duplicate_screens",
        "source_hashes",
        "confidence_tier",
        "machine_actionable_next_step",
    }
    for row in rows:
        missing = sorted(required_keys - set(row))
        if missing:
            missing_required.append(
                {"candidate_id": row.get("candidate_id"), "missing_keys": missing}
            )
    return {
        "candidate_ids_unique": not duplicate_ids,
        "duplicate_candidate_ids": duplicate_ids,
        "terminal_states_allowed": not invalid_states,
        "invalid_terminal_states": invalid_states,
        "required_row_fields_present": not missing_required,
        "rows_missing_required_fields": missing_required[:20],
        "source_hashes_present_for_all_rows": all(row.get("source_hashes") for row in rows),
    }


def build_scaleout_metal_hydrolase_shard(
    *,
    source_paths: dict[str, Path] | None = None,
    created_utc: str | None = None,
    started_at_utc: str | None = None,
    started_at_local: str | None = None,
) -> dict[str, Any]:
    paths = source_paths or DEFAULT_SOURCE_PATHS
    payloads, source_records, missing_sources = _load_sources(paths)
    records = _merge_source_rows(payloads, source_records)
    rows = [_finalize_record(records[candidate_id]) for candidate_id in sorted(records, key=_sort_key)]
    terminal_counts = Counter(row["terminal_state"] for row in rows)
    subfamily_counts = Counter(row["proposed_subfamily_lane"] for row in rows)
    confidence_counts = Counter(row["confidence_tier"] for row in rows)
    role_counts = Counter(
        role for row in rows for role in row.get("candidate_roles", [])
    )
    validation = _validate_rows(rows)
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc or _utc_now_iso(),
        "automation_id": "ce-expansion-shard-metal-hydrolase",
        "started_at_utc": started_at_utc,
        "started_at_local": started_at_local,
        "status": "candidate_evidence_lane_ready",
        "scope": {
            "current_countable_label_count": 702,
            "family_lane": "metal_hydrolase_subclasses",
            "source_policy": "source-free candidate/evidence lane; source IDs and text may appear only as provenance/rationale",
            "output_policy": "no registry, ontology, import, split, threshold, model, heldout-training, or tuning edits",
        },
        "candidate_count": len(rows),
        "terminal_state_counts": dict(sorted(terminal_counts.items())),
        "subfamily_lane_counts": dict(sorted(subfamily_counts.items())),
        "confidence_tier_counts": dict(sorted(confidence_counts.items())),
        "candidate_role_counts": dict(sorted(role_counts.items())),
        "source_artifacts": source_records,
        "missing_optional_source_artifacts": missing_sources,
        "source_row_counts": {
            key: len(_rows_from_payload(payload)) for key, payload in payloads.items()
        },
        "guardrails": {
            "candidate_evidence_lane_only": True,
            "registry_edits_performed": False,
            "ontology_edits_performed": False,
            "imports_or_promotions_performed": False,
            "production_thresholds_changed": False,
            "train_test_splits_changed": False,
            "model_weights_changed": False,
            "heldout_training_or_tuning_performed": False,
            "mechanism_text_or_source_ids_used_as_predictive_scoring_features": False,
            "oos_reject_signal_preserved": terminal_counts["reject/OOS_preserve_signal"]
            > 0,
        },
        "validation_checks": validation,
        "rows": rows,
    }


def render_scaleout_metal_hydrolase_report(artifact: dict[str, Any]) -> str:
    lines = [
        "# Metal Hydrolase Scale-Out Shard",
        "",
        f"- Artifact: `{artifact['artifact_id']}`",
        f"- Created UTC: `{artifact['created_utc']}`",
        f"- Candidate rows: `{artifact['candidate_count']}`",
        f"- Status: `{artifact['status']}`",
        f"- Family lane: `{artifact['scope']['family_lane']}`",
        "",
        "## Terminal States",
        "",
    ]
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Subfamily Lanes", ""])
    for lane, count in artifact["subfamily_lane_counts"].items():
        lines.append(f"- `{lane}`: {count}")
    lines.extend(["", "## Confidence Tiers", ""])
    for tier, count in artifact["confidence_tier_counts"].items():
        lines.append(f"- `{tier}`: {count}")
    lines.extend(["", "## Source Artifacts", ""])
    for key, record in artifact["source_artifacts"].items():
        lines.append(
            f"- `{key}`: `{record['path']}` sha256 `{record['sha256']}`"
        )
    if artifact["missing_optional_source_artifacts"]:
        lines.extend(["", "## Missing Optional Sources", ""])
        for key, path in artifact["missing_optional_source_artifacts"].items():
            lines.append(f"- `{key}`: `{path}`")
    lines.extend(["", "## Review Queues", ""])
    for state in TERMINAL_STATES:
        examples = [
            row
            for row in artifact["rows"]
            if row["terminal_state"] == state
        ][:12]
        if not examples:
            continue
        lines.append(f"### `{state}`")
        lines.append("")
        for row in examples:
            lines.append(
                "- "
                f"`{row['candidate_id']}` "
                f"`{row['proposed_subfamily_lane']}` "
                f"`{row['confidence_tier']}` - "
                f"{row['machine_actionable_next_step']}"
            )
        lines.append("")
    lines.extend(
        [
            "## Guardrails",
            "",
            "- No registry, ontology, import, train/test split, threshold, model, or heldout-training/tuning edits were performed.",
            "- Mechanism text, source IDs, EC/Rhea-like context, target names, and source labels are preserved only as provenance/rationale, not predictive scoring features.",
            "- OOS, hard-negative, duplicate, locator, coordinate, and family-decision blockers remain non-counting signals.",
            "",
            "## Validation",
            "",
        ]
    )
    for key, value in artifact["validation_checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def render_handoff(
    artifact: dict[str, Any],
    *,
    started_at_utc: str | None,
    started_at_local: str | None,
    elapsed_minutes: float | None = None,
) -> str:
    lines = [
        "# Metal Hydrolase Shard Handoff",
        "",
        f"- Automation ID: `ce-expansion-shard-metal-hydrolase`",
        f"- STARTED_AT_UTC: `{started_at_utc or artifact.get('started_at_utc')}`",
        f"- STARTED_AT_LOCAL: `{started_at_local or artifact.get('started_at_local')}`",
        f"- ENDED_AT_UTC: `{_utc_now_iso()}`",
    ]
    if elapsed_minutes is not None:
        lines.append(f"- ELAPSED_MINUTES: `{elapsed_minutes:.3f}`")
    lines.extend(
        [
            "- Lock: `/tmp/ce_scaleout_metal_hydrolase_shard.lock`",
            "- Status: durable lane artifact/report generated; candidate/evidence lane only.",
            "",
            "## Outputs",
            "",
            f"- JSON: `{DEFAULT_OUT_PATH}`",
            f"- Report: `{DEFAULT_REPORT_PATH}`",
            f"- Handoff: `{DEFAULT_HANDOFF_PATH}`",
            "",
            "## Counts",
            "",
            f"- Candidate rows: `{artifact['candidate_count']}`",
        ]
    )
    for state, count in artifact["terminal_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Next Action", ""])
    lines.append(
        "Main merger lane should review the metal hydrolase shard by subfamily "
        "and terminal state, then choose which source-free preflight, locator, "
        "coordinate, or family-decision queues to advance. Do not import from "
        "this shard directly."
    )
    return "\n".join(lines) + "\n"


def write_scaleout_metal_hydrolase_shard(
    *,
    out_path: Path = DEFAULT_OUT_PATH,
    report_path: Path = DEFAULT_REPORT_PATH,
    handoff_path: Path = DEFAULT_HANDOFF_PATH,
    source_paths: dict[str, Path] | None = None,
    created_utc: str | None = None,
    started_at_utc: str | None = None,
    started_at_local: str | None = None,
    elapsed_minutes: float | None = None,
) -> dict[str, Any]:
    artifact = build_scaleout_metal_hydrolase_shard(
        source_paths=source_paths,
        created_utc=created_utc,
        started_at_utc=started_at_utc,
        started_at_local=started_at_local,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    handoff_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    report_path.write_text(render_scaleout_metal_hydrolase_report(artifact))
    handoff_path.write_text(
        render_handoff(
            artifact,
            started_at_utc=started_at_utc,
            started_at_local=started_at_local,
            elapsed_minutes=elapsed_minutes,
        )
    )
    return artifact


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="build the current702 metal hydrolase scale-out shard"
    )
    parser.add_argument("--out", default=str(DEFAULT_OUT_PATH))
    parser.add_argument("--report", default=str(DEFAULT_REPORT_PATH))
    parser.add_argument("--handoff", default=str(DEFAULT_HANDOFF_PATH))
    parser.add_argument("--created-utc")
    parser.add_argument("--started-at-utc")
    parser.add_argument("--started-at-local")
    parser.add_argument("--elapsed-minutes", type=float)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    artifact = write_scaleout_metal_hydrolase_shard(
        out_path=Path(args.out),
        report_path=Path(args.report),
        handoff_path=Path(args.handoff),
        created_utc=args.created_utc,
        started_at_utc=args.started_at_utc,
        started_at_local=args.started_at_local,
        elapsed_minutes=args.elapsed_minutes,
    )
    print(f"wrote {args.out} ({artifact['candidate_count']} candidates)")
    print(f"wrote {args.report}")
    print(f"wrote {args.handoff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
