"""Live sourcing for the cofactorless `ser_his_acid_hydrolase` hole.

This is the cofactorless analogue of `stage1_hole_sourcing` (which sources the
cofactor-defined Stage-1 fingerprints). `ser_his_acid_hydrolase` is the one seed
fingerprint the cofactor/EC engine structurally cannot reach -- there is no
catalytic cofactor to corroborate -- so its corroborator is the **coordinate
Ser/Cys/Thr-His-Asp/Glu catalytic triad** coinciding with the annotated catalytic
ACT_SITE (the `ser_his_triad_locator` primitive). This module wires the locator's
acquisition contract into a runnable, network-enabled pipeline:

    fetch reviewed serine-hydrolase Swiss-Prot rows (EC 3.4.21/3.4.16/3.1.1,
      ACT_SITE annotated, NO cofactor)                       (build_external_source_ingestion_pilot)
      -> stage the AlphaFoldDB v6 predicted coordinate        (live AFDB; UniProt-numbered)
      -> assess_ser_his_candidate                             (triad geometry corroborated vs ACT_SITE)
      -> evaluate_batch                                       (novelty gate)
      -> cap guard                                            (never push a fingerprint over the ceiling)
      -> non-destructive preview                              (applied_labels ready for apply)
      -> (apply, separate/authorized) apply_external_annotation_anchored_import_to_registry

Why AFDB and not PDB: the triad corroboration requires the coordinate residue
numbers to equal the UniProt ACT_SITE positions. AlphaFoldDB models are 1:1 with
the UniProt sequence (UniProt numbering); experimental PDB chains carry author
numbering that usually differs, so AFDB is the correct staged coordinate.

Guardrails (asserted on the output, identical to the cofactor runner):
- scope decided from reviewed Swiss-Prot/EC annotation ONLY; EC / protein name /
  prose stay in `excluded_context`, never predictive features;
- the corroboration is the **coordinate triad**, not a cofactor (cofactorless);
- `tier=bronze`, `review_status=automation_curated`, uniprot namespace;
- the frozen current702 benchmark is never written (expansion only);
- new labels deduped vs BOTH registries; novelty-gated vs both; cap-guarded;
- without `--apply` the runner writes only an `artifacts/` preview + `work/` report.
"""

from __future__ import annotations

import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .adapters import USER_AGENT, fetch_uniprot_entry, fetch_uniprot_query
from .external_annotation_anchored_import import _build_label
from .external_scaleout_bronze_import import (
    DEFAULT_CURRENT_MANIFEST_PATH,
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
)
from .external_source_ingestion import (
    _read_json,
    _utc_now_iso,
    build_external_source_ingestion_pilot,
)
from .novelty_admission_gate import (
    DEFAULT_CAP_CEILING,
    DEFAULT_PER_CLUSTER_CAP,
    build_diversity_state,
    evaluate_batch,
)
from .ser_his_triad_locator import (
    DEFAULT_TARGET_FLOOR,
    assess_ser_his_candidate,
    is_serine_hydrolase_ec,
)

ARTIFACT_ID = "v3_ser_his_hole_sourcing_preview_current702"
SCHEMA_VERSION = "external_annotation_anchored_import.v1"
FINGERPRINT = "ser_his_acid_hydrolase"

ALPHAFOLD_CIF_URL = "https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v6.cif"

# Serine/cysteine-hydrolase EC families whose catalysis runs through a
# Ser/Cys/Thr-His-acid triad. Each lane is a NARROW EC subquery that requires an
# annotated ACT_SITE and excludes any annotated cofactor at the source (so we only
# fetch genuinely cofactorless candidates -- the triad locator's sourcing rule). EC
# is used for SCOPE ASSIGNMENT only (excluded_context; never predictive).
SER_HIS_LANE_QUERIES: tuple[dict[str, str], ...] = (
    {
        "lane_id": "ser_his_ec_3_4_21",
        "target_family_lane": "serine/cysteine hydrolase",
        "query": (
            "(reviewed:true) AND (ec:3.4.21.*) AND (ft_act_site:*) "
            "AND NOT (cc_cofactor:*)"
        ),
    },
    {
        "lane_id": "ser_his_ec_3_4_16",
        "target_family_lane": "serine/cysteine hydrolase",
        "query": (
            "(reviewed:true) AND (ec:3.4.16.*) AND (ft_act_site:*) "
            "AND NOT (cc_cofactor:*)"
        ),
    },
    {
        "lane_id": "ser_his_ec_3_1_1",
        "target_family_lane": "esterase/lipase triad",
        "query": (
            "(reviewed:true) AND (ec:3.1.1.*) AND (ft_act_site:*) "
            "AND NOT (cc_cofactor:*)"
        ),
    },
)


def afdb_v6_cif_fetcher(accession: str) -> str | None:
    """Fetch the AlphaFoldDB v6 predicted CIF for an accession (None on 404)."""
    url = ALPHAFOLD_CIF_URL.format(accession=accession)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - public AFDB
            return response.read().decode("utf-8")
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    except (URLError, OSError):
        return None


def _ser_his_combined_count(
    frozen: list[dict[str, Any]], expansion: list[dict[str, Any]]
) -> int:
    return sum(
        1
        for label in list(frozen) + list(expansion)
        if label.get("fingerprint_id") == FINGERPRINT
        and label.get("label_type") == "seed_fingerprint"
    )


def _ser_his_decision() -> dict[str, Any]:
    return {
        "label_type": "seed_fingerprint",
        "fingerprint_id": FINGERPRINT,
        "reason": (
            "ser_his_triad_locator: serine-hydrolase-family EC + no annotated cofactor "
            "+ coordinate Ser/Cys/Thr-His-Asp/Glu triad annotation-corroborated against "
            "the catalytic ACT_SITE; EC used for scope assignment only (never predictive)"
        ),
    }


def build_ser_his_hole_sourcing(
    *,
    max_records_per_lane: int = 60,
    current_manifest_payload: dict[str, Any],
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    staging_dir: Path,
    created_utc: str | None = None,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    confirm_margin: int = 40,
    lane_queries: tuple[dict[str, str], ...] = SER_HIS_LANE_QUERIES,
    query_fetcher: Callable[[str, int], dict[str, Any]] = fetch_uniprot_query,
    entry_fetcher: Callable[[str], dict[str, Any]] = fetch_uniprot_entry,
    cif_fetcher: Callable[[str], str | None] = afdb_v6_cif_fetcher,
) -> dict[str, Any]:
    """Source the cofactorless ser_his hole; return a non-destructive preview."""
    created = created_utc or _utc_now_iso()
    staging_dir = Path(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 1. Fetch reviewed serine-hydrolase candidate rows (EC from the search row, so
    #    no Rhea network is needed; the entry fetch supplies ACT_SITE + cofactor).
    pilot = build_external_source_ingestion_pilot(
        current_manifest_payload=current_manifest_payload,
        label_registry_payload=list(frozen_benchmark_payload) + list(expansion_payload),
        created_utc=created,
        max_records_per_lane=max_records_per_lane,
        lane_queries=lane_queries,
        query_fetcher=query_fetcher,
        entry_fetcher=entry_fetcher,
        fetch_rhea_fallback=False,
    )

    existing_entry_ids = {
        str(label.get("entry_id"))
        for label in list(frozen_benchmark_payload) + list(expansion_payload)
    }
    combined_before = _ser_his_combined_count(frozen_benchmark_payload, expansion_payload)
    deficit = max(target_floor - combined_before, 0)
    # Stage coordinates only until we have enough confirmed candidates to clear the
    # floor after novelty throttling -- bounds the AFDB fetch volume.
    confirm_budget = min(
        max(cap_ceiling - combined_before, 0), deficit + max(confirm_margin, 0)
    )

    assigned_labels: list[dict[str, Any]] = []
    hold_reasons: Counter[str] = Counter()
    coordinate_failures: list[dict[str, Any]] = []
    seen_accessions: set[str] = set()
    coordinates_staged = 0
    examined = 0

    for candidate in pilot["rows"]:
        if len(assigned_labels) >= confirm_budget:
            break
        examined += 1
        accession = str(candidate.get("accession") or "")
        entry_id = f"uniprot:{accession}"
        ec_numbers = (candidate.get("rhea_ec_provenance") or {}).get("ec_numbers") or []

        # Cheap gates first (no network): serine-hydrolase EC, cofactorless, novel.
        if not is_serine_hydrolase_ec([str(e) for e in ec_numbers]):
            hold_reasons["not_a_serine_hydrolase_ec_family"] += 1
            continue
        if candidate.get("cofactor_provenance"):
            hold_reasons["catalytic_cofactor_annotated"] += 1
            continue
        screen = candidate.get("duplicate_current_registry_conflict") or {}
        if screen.get("duplicate_or_current_registry_conflict"):
            hold_reasons["registry_or_current702_duplicate"] += 1
            continue
        if entry_id in existing_entry_ids or accession in seen_accessions:
            hold_reasons["registry_or_current702_duplicate"] += 1
            continue

        # Stage the AFDB v6 predicted coordinate (UniProt-numbered) for triad confirm.
        cif_text = cif_fetcher(accession)
        if cif_text is None:
            hold_reasons["no_afdb_predicted_coordinate"] += 1
            coordinate_failures.append({"accession": accession, "reason": "afdb_v6_unavailable"})
            continue
        coord_path = staging_dir / f"AF-{accession}-F1-model_v6.cif"
        coord_path.write_text(cif_text, encoding="utf-8")
        coordinates_staged += 1

        staged = dict(candidate)
        staged["coordinate_path"] = str(coord_path)
        label = _build_label(staged, _ser_his_decision())
        assessment = assess_ser_his_candidate(label)
        if assessment["decision"] != "assign_ser_his":
            hold_reasons[f"triad:{assessment['reason']}"] += 1
            continue

        # Confirmed. Record the corroboration; keep the committed label free of the
        # transient staged path (the coordinate is AFDB-v6 regeneratable).
        confirmation = assessment["triad_confirmation"]
        evidence = label["evidence"]
        evidence["sources"] = ["ser_his_triad_locator_hole_sourcing"]
        evidence["cofactor_evidence_level"] = "cofactorless_triad"
        evidence.setdefault("import_gate_evidence", []).append(
            "coordinate_ser_his_acid_triad_annotation_corroborated"
        )
        evidence.setdefault("notes", []).append(
            "cofactorless ser_his_acid_hydrolase: the corroboration is the coordinate "
            "Ser/Cys/Thr-His-Asp/Glu catalytic triad coinciding (>=2 overlap) with the "
            "annotated catalytic ACT_SITE residues, not a cofactor; EC is scope-only "
            "(never a predictive feature). Triad confirmed on the AlphaFoldDB v6 "
            "predicted (apo) structure, which is UniProt-numbered."
        )
        structure = evidence["structure_provenance"]
        structure["structure_handle"] = f"AF-{accession}-F1"
        structure["coordinate_status"] = "afdb_v6_predicted_coordinate_triad_confirmed"
        structure["coordinate_path"] = None
        structure["coordinate_source"] = ALPHAFOLD_CIF_URL.format(accession=accession)
        structure["alphafold_ids"] = [accession]
        structure["ser_his_triad_confirmation"] = {
            "triad_residue_ids": confirmation["triad_residue_ids"],
            "annotated_act_site_overlap": confirmation["annotated_act_site_overlap"],
            "annotated_act_site_overlap_count": confirmation["annotated_act_site_overlap_count"],
            "status": confirmation["status"],
        }
        assigned_labels.append(label)
        seen_accessions.add(accession)

    # 2. Novelty gate (state seeded from BOTH registries so orthologs are throttled).
    state = build_diversity_state(frozen_benchmark_payload, expansion_payload)
    gate = evaluate_batch(
        assigned_labels,
        state,
        per_cluster_cap=per_cluster_cap,
        target_floor=target_floor,
    )
    admit_ids = set(gate["admit_entry_ids"])
    gate_admitted = [l for l in assigned_labels if l.get("entry_id") in admit_ids]
    throttled = [l for l in assigned_labels if l.get("entry_id") not in admit_ids]

    # 3. Cap guard -- never push ser_his over the cap (a no-op while it is a hole,
    #    kept for parity with the cofactor runner).
    admitted: list[dict[str, Any]] = []
    cap_trimmed = 0
    for label in gate_admitted:
        if combined_before + len(admitted) >= cap_ceiling:
            cap_trimmed += 1
            continue
        admitted.append(label)

    projected = combined_before + len(admitted)
    floor_projection = {
        FINGERPRINT: {
            "combined_before": combined_before,
            "admitted_this_run": len(admitted),
            "projected_combined": projected,
            "deficit_to_floor_before": deficit,
            "deficit_to_floor_after": max(target_floor - projected, 0),
            "floor_reached": projected >= target_floor,
            "cap_ceiling": cap_ceiling,
            "held_at_cap_this_run": cap_trimmed,
            "projected_over_cap": projected > cap_ceiling,
        }
    }

    combined_total = len(frozen_benchmark_payload) + len(expansion_payload)
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_annotation_plus_source_free_triad_geometry",
        "stage": "scaling_plan_to_10k:stage_1_close_the_holes:ser_his_cofactorless",
        "fingerprint": FINGERPRINT,
        "corroboration": (
            "coordinate Ser/Cys/Thr-His-Asp/Glu catalytic triad annotation-corroborated "
            "against the catalytic ACT_SITE on the AlphaFoldDB v6 predicted structure"
        ),
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "cofactorless_corroboration_is_coordinate_triad_not_cofactor": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "novelty_gated_against_both_registries": True,
            "per_fingerprint_cap_ceiling_enforced": cap_ceiling,
            "no_fingerprint_pushed_over_cap": not floor_projection[FINGERPRINT][
                "projected_over_cap"
            ],
            "triad_confirmation_uses_only_coordinates_no_text": True,
        },
        "floor_projection": floor_projection,
        "counts": {
            "lanes_queried": len(lane_queries),
            "max_records_per_lane": max_records_per_lane,
            "fetched_candidate_rows": pilot["candidate_count"],
            "examined_rows": examined,
            "coordinates_staged": coordinates_staged,
            "triad_confirmed_labels": len(assigned_labels),
            "novelty_admitted_labels": len(admitted),
            "novelty_throttled_or_rejected": len(throttled),
            "held_at_cap_ceiling": cap_trimmed,
            "hold_reason_counts": dict(sorted(hold_reasons.items())),
            "coordinate_failure_count": len(coordinate_failures),
            "current_combined_labels": combined_total,
            "projected_combined_labels_if_merged": combined_total + len(admitted),
        },
        "novelty_gate": {
            "decision_counts": gate["decision_counts"],
            "reason_counts": gate["reason_counts"],
        },
        "lane_summaries": pilot["lane_summaries"],
        "fetch_failures": pilot["fetch_failures"],
        "fetch_failure_count": pilot["fetch_failure_count"],
        "coordinate_failures": coordinate_failures[:50],
        "next_action": (
            "Review floor_projection + novelty_gate + hold_reason_counts, then on "
            "explicit authorization append `applied_labels` to "
            "data/registries/external_bronze_labels.json via "
            "`apply-external-annotation-anchored-import` (frozen current702 never "
            "written). Held/throttled rows are the next batch."
        ),
        "applied_labels": admitted,
        "throttled_or_rejected_sample": [
            {"entry_id": l.get("entry_id"), "fingerprint_id": l.get("fingerprint_id")}
            for l in throttled[:50]
        ],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    proj = audit["floor_projection"][FINGERPRINT]
    lines = [
        "# Ser/His Hole Sourcing — Cofactorless Triad (non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Sources fresh reviewed Swiss-Prot bronze for the cofactorless",
        "`ser_his_acid_hydrolase` hole: serine-hydrolase EC + no cofactor + a coordinate",
        "Ser/Cys/Thr-His-Asp/Glu triad corroborated against the annotated catalytic",
        "ACT_SITE on the AlphaFoldDB v6 predicted structure. EC is scope-only (never",
        "predictive); tier=bronze; the frozen current702 benchmark is NOT written.",
        "",
        "## Result",
        "",
        f"- Lanes queried: {c['lanes_queried']} (<= {c['max_records_per_lane']} rows each).",
        f"- Fetched candidate rows: {c['fetched_candidate_rows']}; examined {c['examined_rows']}.",
        f"- Coordinates staged (AFDB v6): {c['coordinates_staged']} "
        f"(unavailable {c['coordinate_failure_count']}).",
        f"- **Triad-confirmed labels: {c['triad_confirmed_labels']}**.",
        f"- **Novelty-admitted labels: {c['novelty_admitted_labels']}** "
        f"(throttled/rejected {c['novelty_throttled_or_rejected']}).",
        f"- Combined registry {c['current_combined_labels']} -> "
        f"**{c['projected_combined_labels_if_merged']}** if merged.",
        "",
        "## Floor projection (100-label floor)",
        "",
        "| Fingerprint | combined before | admitted | projected | floor reached |",
        "| --- | --- | --- | --- | --- |",
        f"| {FINGERPRINT} | {proj['combined_before']} | {proj['admitted_this_run']} | "
        f"{proj['projected_combined']} | {proj['floor_reached']} |",
        "",
        "## Hold reasons",
        "",
        f"- {c['hold_reason_counts']}",
        "",
        "## Novelty gate",
        "",
        f"- Decisions: {audit['novelty_gate']['decision_counts']}.",
        f"- Reasons: {audit['novelty_gate']['reason_counts']}.",
        "",
        "## Guardrails",
        "",
        "- Curated registry written: "
        f"{audit['guardrails']['curated_registry_written']}.",
        "- EC scope-only / never predictive: "
        f"{audit['guardrails']['ec_used_for_scope_assignment_only_never_predictive']}.",
        "- Cofactorless corroboration is the coordinate triad (not a cofactor); all new "
        "labels bronze / automation_curated; novelty-gated vs both registries; heldout "
        "benchmark unchanged.",
        "",
        "## Next action",
        "",
        f"- {audit['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_ser_his_hole_sourcing(
    *,
    out_path: Path,
    report_path: Path | None = None,
    max_records_per_lane: int = 60,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    staging_dir: Path | None = None,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    per_cluster_cap: int = DEFAULT_PER_CLUSTER_CAP,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    confirm_margin: int = 40,
) -> dict[str, Any]:
    """Build the preview and write it (non-destructive: no registry is touched)."""
    expansion_path = Path(expansion_registry_path)
    if staging_dir is None:
        staging_dir = Path(tempfile.gettempdir()) / "ser_his_staged_coordinates"
    audit = build_ser_his_hole_sourcing(
        max_records_per_lane=max_records_per_lane,
        current_manifest_payload=_read_json(Path(current_manifest_path)),
        frozen_benchmark_payload=_read_json(Path(frozen_benchmark_path)),
        expansion_payload=_read_json(expansion_path) if expansion_path.exists() else [],
        staging_dir=Path(staging_dir),
        target_floor=target_floor,
        per_cluster_cap=per_cluster_cap,
        cap_ceiling=cap_ceiling,
        confirm_margin=confirm_margin,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
