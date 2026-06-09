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

ONTOLOGY_VERSION = "label_factory_v1_8fp"

# Annotation-derived family lane -> primary mechanism fingerprint.
LANE_PRIMARY_FINGERPRINT: dict[str, str] = {
    "metal hydrolase": "metal_dependent_hydrolase",
    "metal hydrolase amidase/peptidase boundary": "metal_dependent_hydrolase",
    "metal hydrolase Mg/Mn controls": "metal_dependent_hydrolase",
    "metal hydrolase amino/carboxypeptidase": "metal_dependent_hydrolase",
    "PLP children": "plp_dependent_enzyme",
    "PLP lyase/eliminase": "plp_dependent_enzyme",
    "flavin redox boundary": "flavin_dehydrogenase_reductase",
}
COFACTOR_FOR_FINGERPRINT: dict[str, str] = {
    "metal_dependent_hydrolase": "metal",
    "plp_dependent_enzyme": "plp",
    "flavin_dehydrogenase_reductase": "flavin",
    "heme_peroxidase_oxidase": "heme",
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
    return json.loads(Path(path).read_text(encoding="utf-8"))


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

    return {
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
            "provenance": {
                "accession": accession,
                "ec_numbers": ec,
                "cofactor_names": cofactor_names,
                "rhea_record_count": (row.get("rhea_ec_provenance") or {}).get(
                    "rhea_record_count"
                ),
                "source_evidence_codes": row.get("source_evidence_codes"),
                "structure_handle": handle,
                "coordinate_status": row.get("coordinate_status"),
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
            "authorization, merge `applied_labels` into "
            "`data/registries/curated_mechanism_labels.json`, refresh the label "
            "summary, and assign the new uniprot rows to the in_distribution split "
            "(never heldout). Held/skipped rows are the next batch: rerun the "
            "current702 duplicate screen for skipped rows and disambiguate the "
            "cofactor-confounded redox and secondary-probe radical-SAM/cobalamin "
            "lanes."
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
