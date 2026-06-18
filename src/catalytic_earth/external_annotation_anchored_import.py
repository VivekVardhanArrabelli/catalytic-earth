"""Annotation-anchored bronze external label import (Wave 2, non-destructive).

Reaching 10k labels requires external transfer, but the project's de-facto bar --
"a label's scope must be confirmed by local active-site geometry" -- cannot be met
on the available AlphaFold **apo** coordinates: the geometry inverse-gate abstains
on 100% of external rows because the cofactor is missing (the same predicted-apo
degradation characterized by the step-4 work). That conflated two separable things:

1. Predictive leakage discipline -- the benchmark SCORER must never see EC, protein
   names, or prose. This stays absolute.
2. Label evidence basis -- what is allowed to DECIDE a label's scope. The field
   standard (and what this module adopts as a bronze source) is reviewed
   Swiss-Prot/EC/Rhea/cofactor annotation.

This module assigns scope from reviewed annotation only, keeps EC/name/prose in
`excluded_context` (never predictive), tiers every row `bronze`, and records
geometry/structure confirmation as a deferred bronze->silver promotion signal.

Conservative policy (quality-preserving):
- Positive (seed_fingerprint) ONLY when the annotation-derived family lane maps to
  a primary fingerprint AND a corroborating cofactor class is annotated (metal/PLP/
  flavin). No cofactor corroboration -> hold.
- out_of_scope for lanes clearly outside the eight fingerprints (phosphoryl
  transfer, glycoside/nucleoside, near-orphan, lyase/isomerase).
- Hold genuinely ambiguous lanes (cofactor-confounded redox; secondary-probe
  radical-SAM/cobalamin) for explicit review.
- Require a confirmed current702 accession/sequence duplicate screen (kept gate).

Output is NON-DESTRUCTIVE: an applied-registry preview artifact (new label records
in registry schema) plus an acceptance/diversity audit. It never writes
`data/registries/curated_mechanism_labels.json`; merging is a separate, explicitly
authorized step.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .registry_io import dump_registry, load_json, write_registry_payload

ONTOLOGY_VERSION = "label_factory_v1_8fp"

# Annotation-derived family lane -> primary mechanism fingerprint.
LANE_PRIMARY_FINGERPRINT: dict[str, str] = {
    "metal hydrolase": "metal_dependent_hydrolase",
    "metal hydrolase amidase/peptidase boundary": "metal_dependent_hydrolase",
    "metal hydrolase Mg/Mn controls": "metal_dependent_hydrolase",
    "metal hydrolase amino/carboxypeptidase": "metal_dependent_hydrolase",
    # Stage-2 metal_dependent_hydrolase v2 sub-families (cofactor still = metal; the
    # bond-change distinction is enforced by the EC-class disambiguation rules).
    "metallopeptidase": "metallopeptidase",
    "metallophosphoesterase/nuclease": "metallophosphoesterase_nuclease",
    "metallophosphomonoesterase": "metallophosphomonoesterase",
    "metallo amidohydrolase/deaminase": "metallo_amidohydrolase_deaminase",
    "PLP children": "plp_dependent_enzyme",
    "PLP lyase/eliminase": "plp_dependent_enzyme",
    "flavin redox boundary": "flavin_dehydrogenase_reductase",
}
COFACTOR_FOR_FINGERPRINT: dict[str, str] = {
    "metal_dependent_hydrolase": "metal",
    "metallopeptidase": "metal",
    "metallophosphoesterase_nuclease": "metal",
    "metallophosphomonoesterase": "metal",
    "metallo_amidohydrolase_deaminase": "metal",
    "plp_dependent_enzyme": "plp",
    "flavin_dehydrogenase_reductase": "flavin",
    "heme_peroxidase_oxidase": "heme",
}
# Analog of COFACTOR_FOR_FINGERPRINT for the broadened-handle families whose defining
# admission evidence is NOT a UniProt cofactor comment but a dissociable COSUBSTRATE / donor
# (2026-06-12). This is the per-family "deploy-missing active-site context" the apo predicted
# structure lacks (Stage-2 checklist item 3) -- recorded as SCOPE/admission metadata only,
# never a predictive feature. These families are admitted via the broadened mechanism
# corroborator in `external_cofactor_ec_disambiguation`, not via `classify_row`.
DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT: dict[str, str] = {
    "nad_p_dehydrogenase": "nad_p_cosubstrate",
    "glycosyltransferase": "sugar_nucleotide_donor",
    "glycoside_hydrolase": "glycosidic_substrate_ordered_water_hydrolysis_context",
    "sam_methyltransferase": "sam_sah_methyl_donor",
    "cytochrome_p450_monooxygenase": "heme_thiolate_oxygen_cosubstrate",
    "non_heme_iron_2og_dioxygenase": "fe_ii_2og_o2_cosubstrate",
    "coa_acyltransferase": "coa_acyl_coa_donor",
    "cofactor_independent_isomerase": "active_site_base_isomerization_context",
    "molybdopterin_oxidoreductase": "molybdopterin_metal_center_redox_context",
    "copper_oxidoreductase": "copper_redox_metal_center_context",
    "metal_racemase_epimerase_non_plp": "racemase_epimerase_proton_shift_context",
    "atp_amide_ligase": "atp_mg_acyl_phosphate_amide_ligation_context",
    "class_ii_metal_aldolase": "metal_stabilized_aldol_c_c_bond_context",
    "thiamine_diphosphate_enzyme": "thdp_mg_ylide_carbonyl_substrate_context",
    "zinc_lyase_hydratase": "zinc_water_elimination_addition_context",
    "biotin_dependent_carboxylase": "biotinyl_lysine_atp_hydrogencarbonate_context",
    "nucleoside_diphosphate_kinase": "phosphohistidine_ntp_ndp_transfer_context",
    "askha_sugar_acetate_kinase": "atp_mg_sugar_or_acetate_phosphoryl_transfer_context",
    "ghmp_small_molecule_kinase": "atp_mg_ghmp_small_molecule_phosphoryl_transfer_context",
    "deoxynucleoside_kinase": "atp_mg_deoxynucleoside_5_prime_phosphoryl_transfer_context",
    "pfka_phosphofructokinase": "atp_mg_fructose_6_phosphate_phosphoryl_transfer_context",
    "pfkb_ribokinase_family": "atp_mg_pfkb_ribokinase_family_phosphoryl_transfer_context",
    "manganese_iron_superoxide_dismutase": "mn_fe_superoxide_redox_dismutation_context",
    "terpene_cyclase_synthase": "metal_prenyl_diphosphate_and_carbocation_intermediate",
    "protein_kinase_ser_thr_tyr": "atp_mg_protein_substrate_phosphoryl_transfer_context",
    "had_like_phosphatase": "mg_aspartyl_phosphoenzyme_phosphomonoester_hydrolysis_context",
    "ser_thr_protein_phosphatase": "dinuclear_metal_phosphoprotein_dephosphorylation_context",
    "aldehyde_dehydrogenase": "nad_p_cys_glu_thiohemiacetal_hydride_transfer_context",
    "short_chain_dehydrogenase_reductase": "nad_p_sdr_ser_tyr_lys_hydride_transfer_context",
    "aldo_keto_reductase": "nadp_akr_tyr_lys_his_asp_tim_barrel_hydride_transfer_context",
    "aminoglycoside_acetyltransferase": "acetyl_coa_aminoglycoside_gnat_n_acetyl_transfer_context",
    "metallo_beta_lactamase": "dizinc_metallo_beta_lactamase_ring_hydrolysis_context",
    "alpha_beta_hydrolase_esterase_lipase": "ser_his_acid_ester_hydrolysis_context",
    "n_ribosyl_hydrolase": "n_glycosidic_bond_hydrolysis_context",
    "metal_independent_phosphodiesterase": "metal_independent_phosphodiester_hydrolysis_context",
    "aminoglycoside_phosphotransferase": "atp_mg_aminoglycoside_phosphoryl_transfer_context",
    "serine_beta_lactamase": "ser_lys_glu_beta_lactam_acyl_enzyme_hydrolysis_context",
}
OUT_OF_SCOPE_LANES: frozenset[str] = frozenset(
    {
        "phosphoryl transfer",
        "phosphoryl transfer/phosphatase",
        "glycoside/nucleoside",
        "glycoside hydrolase",
        "near-orphan/no-reliable-structure",
        "adjacent high-yield lyase/isomerase",
        "nucleotide phosphoryl-transfer boundary",
        "kinase/phosphotransferase",
    }
)
# Genuinely ambiguous lanes held for explicit review, never blind-imported.
HOLD_LANES: frozenset[str] = frozenset(
    {
        "redox oxygen/sulfur",
        "radical-SAM/cobalamin",
        "Fe-S/flavin combined systems",
    }
)

EXCLUDED_PREDICTIVE_CONTEXT = [
    "protein_name",
    "ec_label",
    "uniprot_prose",
    "source_annotation",
    "curated_mechanism_text",
    "target_family_lane",
]
EXPERIMENTAL_EVIDENCE_CODE = "ECO:0000269"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> Any:
    return load_json(Path(path))


def _preview_rows(preview: Any) -> list[dict[str, Any]]:
    if isinstance(preview, list):
        return [r for r in preview if isinstance(r, dict)]
    for value in preview.values():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            return value
    return []


def cofactor_classes(row: dict[str, Any]) -> set[str]:
    """Cofactor classes annotated for the row (metal/plp/flavin/heme), name-based."""
    classes: set[str] = set()
    for cof in row.get("cofactor_provenance") or []:
        name = str(cof.get("name") or "").lower()
        if any(
            metal in name
            for metal in (
                "zn",
                "zinc",
                "mn",
                "manganese",
                "mg",
                "magnesium",
                "fe",
                "iron",
                "ni",
                "nickel",
                "cobalt",
                "co(2",
                "cu",
                "copper",
                "ca(2",
                "calcium",
                "cadmium",
                "metal",
            )
        ):
            classes.add("metal")
        if "pyridoxal" in name or name.strip() == "plp":
            classes.add("plp")
        if any(flavin in name for flavin in ("fad", "flavin", "fmn", "riboflavin")):
            classes.add("flavin")
        if "heme" in name or "haem" in name:
            classes.add("heme")
        if "molybdopterin" in name or "molybdenum cofactor" in name or "moco" in name:
            classes.add("molybdopterin")
    return classes


def classify_row(row: dict[str, Any]) -> dict[str, Any]:
    """Conservative annotation-anchored scope decision for one candidate row."""
    dup_status = str(row.get("duplicate_current_registry_conflict_status") or "")
    if not dup_status.startswith("no_exact"):
        return {"decision": "skip", "reason": "current702_duplicate_screen_not_confirmed"}

    lane = row.get("target_family_lane")
    cofactors = cofactor_classes(row)

    if lane in LANE_PRIMARY_FINGERPRINT:
        fingerprint = LANE_PRIMARY_FINGERPRINT[lane]
        needed = COFACTOR_FOR_FINGERPRINT[fingerprint]
        if needed in cofactors:
            return {
                "decision": "import",
                "label_type": "seed_fingerprint",
                "fingerprint_id": fingerprint,
                "reason": f"annotation_lane_{lane!r}_with_{needed}_cofactor_corroboration",
                "cofactor_classes": sorted(cofactors),
            }
        return {
            "decision": "hold",
            "reason": "primary_lane_without_cofactor_corroboration",
            "lane": lane,
            "cofactor_classes": sorted(cofactors),
        }
    if lane in OUT_OF_SCOPE_LANES:
        return {
            "decision": "import",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "reason": f"annotation_lane_{lane!r}_outside_eight_fingerprints",
            "cofactor_classes": sorted(cofactors),
        }
    if lane in HOLD_LANES:
        return {"decision": "hold", "reason": "ambiguous_lane_review_required", "lane": lane}
    return {"decision": "hold", "reason": "unmapped_lane", "lane": str(lane)}


def _confidence_and_score(
    row: dict[str, Any], decision: dict[str, Any]
) -> tuple[str, float]:
    codes = set(row.get("source_evidence_codes") or [])
    experimental = EXPERIMENTAL_EVIDENCE_CODE in codes
    has_cofactor = bool(decision.get("cofactor_classes"))
    ec = (row.get("rhea_ec_provenance") or {}).get("ec_numbers") or []
    specific_ec = any("-" not in str(e) for e in ec)
    rhea = ((row.get("rhea_ec_provenance") or {}).get("rhea_record_count") or 0) > 0

    score = 0.50
    if experimental:
        score += 0.15
    if has_cofactor:
        score += 0.10
    if specific_ec:
        score += 0.05
    if rhea:
        score += 0.05
    score = round(min(score, 0.85), 4)
    confidence = "high" if (experimental and has_cofactor) else "medium"
    return confidence, score


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    """Structured, review-only mechanism evidence a future model can learn from.

    Reaction chemistry (Rhea), catalytic/binding residues, and cofactor dependence
    are the North Star evidence axes. They are provenance/supervision context, NOT
    predictive features (see ``excluded_context``).
    """
    rhea = row.get("rhea_ec_provenance") or {}
    reactions = [
        {
            "rhea_id": rec.get("rhea_id"),
            "reaction": rec.get("reaction"),
            "ec_number": rec.get("ec_number"),
            "evidence_codes": rec.get("evidence_codes"),
            "source": rec.get("source"),
        }
        for rec in (rhea.get("rhea_records") or [])
        if isinstance(rec, dict)
    ]
    cofactors = [
        {
            "name": c.get("name"),
            "chebi_id": (c.get("cross_reference") or {}).get("id"),
            "evidence_codes": c.get("evidence_codes"),
        }
        for c in (row.get("cofactor_provenance") or [])
        if isinstance(c, dict)
    ]
    residues = [
        {
            "position": loc.get("position"),
            "feature_code": loc.get("feature_code"),
            "feature_type": loc.get("feature_type"),
            "ligand_id": loc.get("ligand_id"),
            "ligand_name": loc.get("ligand_name"),
            "evidence_codes": loc.get("evidence_codes"),
            "exact": loc.get("exact"),
        }
        for loc in (row.get("residue_locators") or [])
        if isinstance(loc, dict)
    ]
    return {
        "reaction_equations": reactions,
        "ec_numbers": rhea.get("ec_numbers") or [],
        "cofactors": cofactors,
        "active_site_residues": residues,
        "active_site_residue_count": len(residues),
        "catalytic_residue_count": sum(
            1 for r in residues if r.get("feature_code") == "ACT_SITE"
        ),
        "binding_residue_count": sum(
            1 for r in residues if r.get("feature_code") == "BINDING"
        ),
    }


def _build_label(row: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    accession = str(row.get("accession"))
    fingerprint = decision.get("fingerprint_id")
    label_type = decision["label_type"]
    confidence, score = _confidence_and_score(row, decision)
    ec = (row.get("rhea_ec_provenance") or {}).get("ec_numbers") or []
    cofactor_names = [
        c.get("name") for c in (row.get("cofactor_provenance") or []) if c.get("name")
    ]
    handle = row.get("afdb_or_pdb_identifier") or (row.get("pdb_ids") or [None])[0]

    scope_phrase = (
        f"in-scope {fingerprint}" if label_type == "seed_fingerprint" else "out_of_scope"
    )
    rationale = (
        f"{accession} imported as annotation-anchored bronze {scope_phrase}: reviewed "
        f"Swiss-Prot EC {ec or 'n/a'}"
        + (
            f" with {', '.join(sorted(decision.get('cofactor_classes', [])))} cofactor "
            "corroboration"
            if decision.get("cofactor_classes")
            else ""
        )
        + "; current702 accession/sequence duplicate screen clear; structure/geometry "
        "confirmation deferred as a bronze->silver promotion signal. EC, protein name, "
        "and prose are excluded from predictive features."
    )

    notes = [
        "annotation-anchored bronze: scope decided from reviewed Swiss-Prot/EC/Rhea/"
        "cofactor annotation, not local geometry",
        "structure/cofactor-fused geometry confirmation is a deferred bronze->silver "
        "promotion signal, not an entry gate",
    ]
    if label_type == "out_of_scope":
        notes.append(
            "out_of_scope is scoped to ontology_version_at_decision and must be "
            "re-audited on positive fingerprint expansion"
        )

    label = {
        "confidence": confidence,
        "entry_id": f"uniprot:{accession}",
        "evidence": {
            "cofactor_evidence_level": "annotated" if cofactor_names else None,
            "conflicts": [],
            "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
            "excluded_context": list(EXCLUDED_PREDICTIVE_CONTEXT),
            "import_gate_evidence": [
                "reviewed_swissprot_entry",
                "current702_accession_sequence_duplicate_screen_clear",
                "annotation_anchored_scope_assignment",
                "bronze_tier_annotation_basis",
            ],
            "migration": "label_factory_v1_default",
            "notes": notes,
            "pending_promotion_audits": [
                "geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure",
                "foldseek_structural_near_duplicate_screen",
            ],
            "predictive_evidence": [],
            "mechanism_evidence": _mechanism_evidence(row),
            "structure_provenance": {
                "structure_handle": handle,
                "coordinate_status": row.get("coordinate_status"),
                "coordinate_path": row.get("coordinate_path"),
                "alphafold_ids": row.get("alphafold_ids"),
                "pdb_ids": row.get("pdb_ids"),
            },
            "source_provenance": {
                "accession": accession,
                "organism": row.get("organism"),
                "sequence_length": row.get("sequence_length"),
                "protein_name": row.get("protein_name"),
                "reviewed_status": row.get("reviewed_status"),
                "source_evidence_codes": row.get("source_evidence_codes"),
                "source_hashes": row.get("source_hashes"),
                "target_family_lane": row.get("target_family_lane"),
                "import_decision_reason": decision.get("reason"),
            },
            "retrieval_score": None,
            "review_only_context": [
                "accession_identity",
                "protein_name",
                "ec_label",
                "uniprot_prose",
                "source_annotation",
                "target_family_lane",
            ],
            "sources": ["external_annotation_anchored_import_wave2"],
        },
        "evidence_score": score,
        "fingerprint_id": fingerprint,
        "label_type": label_type,
        "ontology_version_at_decision": ONTOLOGY_VERSION,
        "rationale": rationale,
        "review_status": "automation_curated",
        "tier": "bronze",
    }

    # Wire the deploy-input sequence at SOURCE time: the canonical ingestion-pilot row
    # carries the raw sequence, which is the legitimate model INPUT (not EC/name/prose),
    # so future sourced labels get evidence.sequence_provenance natively. It is stored
    # DATA -- never a predictive feature -- so the leakage wall is unchanged.
    sequence = row.get("sequence")
    if isinstance(sequence, str) and sequence:
        from .label_sequence_backfill import sequence_provenance_block

        label["evidence"]["sequence_provenance"] = sequence_provenance_block(
            sequence=sequence,
            accession=accession,
            retrieved_utc=(row.get("source_provenance") or {}).get("query_timestamp_utc")
            or _utc_now_iso(),
            retrieval={
                "endpoint": "https://rest.uniprot.org/uniprotkb/search",
                "fields": "accession,sequence,length,reviewed",
                "format": "tsv",
                "source_query_sha256": (row.get("source_hashes") or {}).get(
                    "source_query_sha256"
                ),
                "reviewed_status": row.get("reviewed_status"),
            },
            stored_length=row.get("sequence_length"),
        )

    return label


def build_external_annotation_anchored_import(
    *,
    preview: Any,
    registry: list[dict[str, Any]],
) -> dict[str, Any]:
    rows = _preview_rows(preview)
    existing_entry_ids = {str(r.get("entry_id")) for r in registry}

    new_labels: list[dict[str, Any]] = []
    holds: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []
    seen_accessions: set[str] = set()

    decision_counts: Counter[str] = Counter()
    label_type_counts: Counter[str] = Counter()
    fingerprint_counts: Counter[str] = Counter()
    lane_scope: dict[str, Counter[str]] = {}
    confidence_counts: Counter[str] = Counter()
    hold_reasons: Counter[str] = Counter()

    for row in rows:
        decision = classify_row(row)
        decision_counts[decision["decision"]] += 1
        accession = str(row.get("accession"))
        entry_id = f"uniprot:{accession}"

        if decision["decision"] == "skip":
            skips.append({"accession": accession, "reason": decision["reason"]})
            continue
        if decision["decision"] == "hold":
            hold_reasons[decision["reason"]] += 1
            holds.append(
                {
                    "accession": accession,
                    "lane": decision.get("lane"),
                    "reason": decision["reason"],
                }
            )
            continue

        # import: final guards -- not already in registry, not duplicated in batch.
        if entry_id in existing_entry_ids or accession in seen_accessions:
            skips.append({"accession": accession, "reason": "duplicate_entry_id_in_registry_or_batch"})
            decision_counts["skip"] += 1
            continue
        seen_accessions.add(accession)

        label = _build_label(row, decision)
        new_labels.append(label)
        label_type_counts[label["label_type"]] += 1
        if label["fingerprint_id"]:
            fingerprint_counts[label["fingerprint_id"]] += 1
        confidence_counts[label["confidence"]] += 1
        lane = str(row.get("target_family_lane"))
        lane_scope.setdefault(lane, Counter())[label["label_type"]] += 1

    current_total = len(registry)
    imported = len(new_labels)

    return {
        "artifact_id": (
            "v3_external_annotation_anchored_import_preview_wave2_current702_20260609"
        ),
        "schema_version": "external_annotation_anchored_import.v1",
        "created_utc": _utc_now_iso(),
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_or_prose": False,
            "ec_name_prose_excluded_context_on_every_label": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "new_labels_join_in_distribution_split_never_heldout": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
        },
        "counts": {
            "preview_rows": len(rows),
            "decision_counts": dict(decision_counts),
            "importable_new_labels": imported,
            "label_type_counts": dict(label_type_counts),
            "fingerprint_counts": dict(sorted(fingerprint_counts.items())),
            "confidence_counts": dict(confidence_counts),
            "hold_count": len(holds),
            "hold_reason_counts": dict(hold_reasons),
            "skip_count": len(skips),
            "current_registry_labels": current_total,
            "projected_registry_labels_if_merged": current_total + imported,
        },
        "diversity_by_lane": {
            lane: dict(counter) for lane, counter in sorted(lane_scope.items())
        },
        "next_action": (
            "Review per-lane diversity and the scope assignment. On explicit "
            "authorization, append `applied_labels` to the SEPARATE expansion "
            "registry `data/registries/external_bronze_labels.json` (the frozen "
            "current702 benchmark registry is never written). The combined total "
            "is frozen-benchmark + expansion. Held/skipped rows are the next batch: "
            "rerun the current702 duplicate screen for skipped rows and "
            "disambiguate the cofactor-confounded redox and secondary-probe "
            "radical-SAM/cobalamin lanes."
        ),
        "applied_labels": new_labels,
        "holds_sample": holds[:50],
        "skips_sample": skips[:50],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Annotation-Anchored Bronze External Import — Wave 2 (non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Reviewed Swiss-Prot/EC/Rhea/cofactor annotation as a bronze label source.",
        "EC, protein names, and prose are excluded from predictive features (the",
        "benchmark scorer never sees them); structure/geometry confirmation is a",
        "deferred bronze->silver promotion signal. The curated registry is NOT",
        "written by this run.",
        "",
        "## Result",
        "",
        f"- Preview rows considered: {c['preview_rows']}.",
        f"- **Importable bronze labels this batch: {c['importable_new_labels']}** "
        f"-> registry {c['current_registry_labels']} -> "
        f"**{c['projected_registry_labels_if_merged']}** if merged.",
        f"- Label types: {c['label_type_counts']}.",
        f"- Positive fingerprints: {c['fingerprint_counts']}.",
        f"- Confidence: {c['confidence_counts']}.",
        f"- Held for review: {c['hold_count']} ({c['hold_reason_counts']}).",
        f"- Skipped: {c['skip_count']} (mostly current702 duplicate screen not yet "
        "confirmed — the next batch).",
        "",
        "## Diversity by lane (label_type split)",
        "",
        "| Lane | imported scope split |",
        "| --- | --- |",
    ]
    for lane, counter in audit["diversity_by_lane"].items():
        lines.append(f"| {lane} | {counter} |")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Curated registry written: "
            f"{audit['guardrails']['curated_registry_written']}.",
            "- EC/name/prose used as predictive features: "
            f"{audit['guardrails']['predictive_features_use_ec_name_or_prose']}.",
            "- All new labels bronze / automation_curated; uniprot namespace; "
            "heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def apply_external_annotation_anchored_import_to_registry(
    *,
    preview_path: Path,
    expansion_registry_path: Path,
    frozen_benchmark_registry_path: Path,
) -> dict[str, Any]:
    """Append the preview's bronze labels to the SEPARATE expansion registry.

    The frozen current702 benchmark registry
    (`data/registries/curated_mechanism_labels.json`) is never written: its label
    count, coherence-audit baseline, and eval-contract hash are deliberately
    pinned. Expansion bronze labels live in their own registry so the benchmark
    stays clean while the total label count grows toward 10k. New labels are
    deduped against BOTH registries and validated through the label schema before
    being written.
    """
    from .labels import MechanismLabel  # local import avoids a module cycle

    preview_artifact = _load_json(preview_path)
    frozen = _load_json(frozen_benchmark_registry_path)
    expansion_path = Path(expansion_registry_path)
    existing_expansion = (
        _load_json(expansion_path) if expansion_path.exists() else []
    )

    known_ids = {str(r.get("entry_id")) for r in frozen}
    known_ids |= {str(r.get("entry_id")) for r in existing_expansion}

    appended: list[dict[str, Any]] = []
    duplicate_skipped = 0
    for label in preview_artifact.get("applied_labels", []):
        entry_id = str(label.get("entry_id"))
        if entry_id in known_ids:
            duplicate_skipped += 1
            continue
        known_ids.add(entry_id)
        # Validate through the canonical label schema (annotation-anchored aware).
        MechanismLabel.from_dict(label)
        appended.append(label)

    new_expansion = list(existing_expansion) + appended
    write_result = write_registry_payload(expansion_path, new_expansion)

    return {
        "frozen_benchmark_labels": len(frozen),
        "frozen_benchmark_registry_written": False,
        "expansion_registry_before": len(existing_expansion),
        "appended": len(appended),
        "duplicate_skipped": duplicate_skipped,
        "expansion_registry_after": len(new_expansion),
        "combined_total_labels": len(frozen) + len(new_expansion),
        "appended_label_type_counts": dict(
            Counter(label.get("label_type") for label in appended)
        ),
        "appended_fingerprint_counts": dict(
            Counter(
                label.get("fingerprint_id")
                for label in appended
                if label.get("fingerprint_id")
            )
        ),
        "all_appended_bronze": all(label.get("tier") == "bronze" for label in appended),
        "expansion_registry_path": str(expansion_path),
        "expansion_registry_storage": write_result,
    }


def _dump_registry(registry: list[dict[str, Any]]) -> str:
    """Serialize the registry in its canonical one-label-per-line compact format."""
    return dump_registry(registry)


def write_external_annotation_anchored_import(
    *,
    preview_path: Path,
    registry_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_external_annotation_anchored_import(
        preview=_load_json(preview_path),
        registry=_load_json(registry_path),
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
