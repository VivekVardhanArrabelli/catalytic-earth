"""Scale-out drain of the annotation-anchored bronze import (Wave 2 continuation).

This driver pulls the *already-materialized* import-ready candidate pools through
the SAME conservative annotation-anchored engine that produced the first 186
expansion labels (``external_annotation_anchored_import``). It adds no new
sourcing and no env-blocked dependencies -- it only drains rows that were held
back earlier:

1. The 324 rows the first Wave 2 batch *skipped* solely because their current702
   accession/sequence duplicate screen had not been promoted to the top-level
   field the engine reads. Their screen is re-run here (accession overlap
   re-checked against BOTH registries + current702; sequence-sha overlap
   re-verified against current702 where the row carries the precomputed digest;
   the upstream current702 sequence screen must independently read clear).
2. Four other import-ready shard pools (metal/phosphoryl/glycoside,
   redox-cofactor-confounded, plp/radical/cobalamin, near-orphan diversity).

Scope is decided ONLY from reviewed Swiss-Prot/EC/Rhea/cofactor annotation, the
same field-standard bronze basis adopted on 2026-06-09. The leakage discipline is
unchanged and absolute: EC, protein name, and prose stay in ``excluded_context``
and are NEVER predictive features; the benchmark scorer never sees them.

Conservative policy (quality over count), identical in spirit to the engine:
- Positive (``seed_fingerprint``) ONLY when an annotation-derived primary lane
  maps to one of the eight fingerprints AND the matching cofactor class
  (metal/PLP/flavin) is annotated. The shard vocabulary adds specific PLP
  catalytic lanes (aminotransferase, decarboxylase, racemase/epimerase, sulfur
  lyase boundary) on top of the engine's lanes; their PLP corroboration is the
  reviewed ``cofactor_family_flags.plp_evidence_present`` annotation evidence.
- ``out_of_scope`` for lanes clearly outside the eight fingerprints (phosphoryl
  transfer/phosphatase, kinase, glycoside/nucleoside, terpene synthase/lyase,
  isomerase/racemase, transferase tail, C-C lyase/decarboxylase,
  dehydratase/hydratase lyase).
- HOLD genuinely ambiguous lanes -- do not guess. The entire
  ``redox_cofactor_confounded`` pool is held (cofactor-confounded redox), and the
  secondary-probe radical-SAM / cobalamin lanes are held. These are the rows the
  optional cofactor/EC disambiguation task is meant to make countable later.

Output is NON-DESTRUCTIVE: a preview artifact in the engine's preview schema
(``applied_labels`` ready for the existing
``apply-external-annotation-anchored-import`` writer, which appends to the
SEPARATE ``external_bronze_labels.json`` expansion registry and never touches the
frozen current702 benchmark).
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .external_annotation_anchored_import import (
    COFACTOR_FOR_FINGERPRINT,
    HOLD_LANES,
    LANE_PRIMARY_FINGERPRINT,
    OUT_OF_SCOPE_LANES,
    _build_label,
    _load_json,
    _preview_rows,
    _utc_now_iso,
    cofactor_classes,
)

DEFAULT_CURRENT_MANIFEST_PATH = Path(
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# Specific PLP catalytic lanes the shard vocabulary introduces, all corroborated
# as plp_dependent_enzyme. "PLP broad cofactor context" is deliberately NOT here:
# a non-specific cofactor-context lane is not a confident primary mechanism call.
SCALEOUT_PRIMARY_LANES: dict[str, str] = {
    **LANE_PRIMARY_FINGERPRINT,
    "PLP aminotransferase": "plp_dependent_enzyme",
    "PLP decarboxylase": "plp_dependent_enzyme",
    "PLP racemase/epimerase": "plp_dependent_enzyme",
    "PLP sulfur lyase boundary": "plp_dependent_enzyme",
}

# Near-orphan / phosphoryl / glycoside lanes clearly outside the eight
# fingerprints (added on top of the engine's OUT_OF_SCOPE_LANES).
SCALEOUT_OUT_OF_SCOPE_LANES: frozenset[str] = OUT_OF_SCOPE_LANES | frozenset(
    {
        "terpene synthase/lyase",
        "isomerase/racemase/epimerase",
        "transferase tail outside current fingerprints",
        "carbon-carbon lyase/decarboxylase",
        "dehydratase/hydratase lyase",
    }
)

# Pools held in their entirety: cofactor-confounded redox must not be guessed.
COFACTOR_CONFOUNDED_HOLD_POOLS: frozenset[str] = frozenset(
    {"redox_cofactor_confounded"}
)

# Standard ChEBI for pyridoxal 5'-phosphate; used only if a PLP row carries no
# explicit PLP ligand cross-reference among its residue locators.
_PLP_CHEBI_FALLBACK = "CHEBI:597326"
_PLP_NAME = "pyridoxal 5'-phosphate"

# The materialized import-ready pools this driver drains. ``schema`` selects the
# normalization path; ``pool`` is the per-row provenance / policy key.
SCALEOUT_POOLS: tuple[dict[str, str], ...] = (
    {
        "pool": "wave2_skipped_duplicate_screen_rerun",
        "schema": "wave2",
        "path": (
            "artifacts/"
            "v3_external_materialization_wave2_import_ready_preview_current702_20260609.json"
        ),
        "only_unscreened": "true",
    },
    {
        "pool": "metal_phosphoryl_glycoside",
        "schema": "shard",
        "path": (
            "artifacts/v3_external_scaleout_shard_metal_phosphoryl_glycoside"
            "_import_ready_preview_current702_20260609.json"
        ),
    },
    {
        "pool": "redox_cofactor_confounded",
        "schema": "shard",
        "path": (
            "artifacts/v3_external_scaleout_shard_redox_cofactor_confounded"
            "_import_ready_preview_current702_20260609.json"
        ),
    },
    {
        "pool": "plp_radical_cobalamin",
        "schema": "shard",
        "path": (
            "artifacts/v3_external_scaleout_shard_plp_radical_cobalamin"
            "_import_ready_preview_current702_20260609.json"
        ),
    },
    {
        "pool": "near_orphan_diversity",
        "schema": "shard",
        "path": (
            "artifacts/v3_external_scaleout_shard_near_orphan_diversity"
            "_import_ready_preview_current702_20260609.json"
        ),
    },
)


def _clean_accession(value: Any) -> str:
    text = str(value or "").strip()
    return text.split(":", 1)[1] if text.startswith("uniprot:") else text


def build_current702_reference_index(
    *,
    current_manifest_payload: dict[str, Any],
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
) -> dict[str, set[str]]:
    """Accession and sequence-SHA reference sets for the duplicate screen.

    Accessions are drawn from the frozen current702 manifest (entry accessions,
    sequence ids, real-sequence accessions, and per-record accessions) AND from
    both label registries, so the re-run screen dedups against BOTH registries.
    Sequence SHAs come from the current702 manifest rows/records.
    """
    current_accessions: set[str] = set()
    current_sequence_shas: set[str] = set()
    for row in current_manifest_payload.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        for value in (row.get("accession"), row.get("sequence_id")):
            cleaned = _clean_accession(value)
            if cleaned:
                current_accessions.add(cleaned)
        for value in row.get("real_sequence_accessions", []) or []:
            cleaned = _clean_accession(value)
            if cleaned:
                current_accessions.add(cleaned)
        if row.get("sequence_sha256"):
            current_sequence_shas.add(str(row["sequence_sha256"]))
        for record in row.get("sequence_records", []) or []:
            if not isinstance(record, dict):
                continue
            cleaned = _clean_accession(record.get("accession"))
            if cleaned:
                current_accessions.add(cleaned)
            if record.get("sequence_sha256"):
                current_sequence_shas.add(str(record["sequence_sha256"]))

    registry_accessions: set[str] = set()
    for label in list(frozen_benchmark_payload) + list(expansion_payload):
        if not isinstance(label, dict):
            continue
        entry_id = str(label.get("entry_id") or "")
        if entry_id.startswith("uniprot:"):
            registry_accessions.add(_clean_accession(entry_id))

    return {
        "current_accessions": current_accessions,
        "current_sequence_shas": current_sequence_shas,
        "registry_accessions": registry_accessions,
    }


def _upstream_current702_status(row: dict[str, Any]) -> str | None:
    """Upstream current702 screen verdict recorded by the materialization pipeline."""
    detail = row.get("duplicate_status")
    if isinstance(detail, dict) and detail.get("current_registry_conflict_status"):
        return str(detail["current_registry_conflict_status"])
    summary = row.get("duplicate_status_summary")
    if isinstance(summary, dict) and summary.get("current702_status"):
        return str(summary["current702_status"])
    return None


def _row_sequence_sha(row: dict[str, Any]) -> str | None:
    detail = row.get("duplicate_status")
    if isinstance(detail, dict) and detail.get("exact_sequence_sha256"):
        return str(detail["exact_sequence_sha256"])
    return None


def rerun_current702_duplicate_screen(
    row: dict[str, Any], *, index: dict[str, set[str]]
) -> dict[str, Any]:
    """Re-run the current702 accession/sequence duplicate screen for one row.

    Independent re-verification (does not blindly trust the stale top-level
    field): accession overlap is re-checked against the current702 reference
    accessions AND both label registries; sequence-SHA overlap is re-checked
    against the current702 sequence-SHA set when the row carries the precomputed
    digest; and the upstream current702 sequence screen must read clear. A row
    clears only when none of these flags a conflict.
    """
    accession = _clean_accession(row.get("accession"))
    accession_conflict = accession in index["current_accessions"] or (
        accession in index["registry_accessions"]
    )
    sequence_sha = _row_sequence_sha(row)
    sequence_conflict = bool(sequence_sha) and sequence_sha in index[
        "current_sequence_shas"
    ]
    upstream = _upstream_current702_status(row)
    upstream_clear = upstream == "no_exact_current702_accession_or_sequence_sha_overlap"

    if accession_conflict:
        status = "exact_current702_or_expansion_accession_overlap"
    elif sequence_conflict:
        status = "exact_current702_sequence_sha_overlap"
    elif not upstream_clear:
        status = "upstream_current702_screen_not_confirmed"
    else:
        status = "no_exact_current702_accession_or_sequence_sha_overlap"
    return {
        "duplicate_current_registry_conflict_status": status,
        "screen_detail": {
            "accession": accession,
            "accession_conflict": accession_conflict,
            "sequence_sha256": sequence_sha,
            "sequence_conflict": sequence_conflict,
            "upstream_current702_status": upstream,
        },
    }


def _synthesize_plp_cofactor_provenance(row: dict[str, Any]) -> list[dict[str, Any]]:
    """Make annotation-derived PLP corroboration visible to the engine.

    The plp/radical/cobalamin shard records PLP dependence in
    ``cofactor_family_flags.plp_evidence_present`` rather than the
    ``cofactor_provenance`` list the engine reads. When that flag is set we
    surface a single PLP cofactor record (with the row's own PLP ligand ChEBI if
    present among its residue locators), tagged so the provenance stays honest.
    """
    flags = row.get("cofactor_family_flags") or {}
    if not flags.get("plp_evidence_present"):
        return []
    chebi = _PLP_CHEBI_FALLBACK
    for locator in row.get("residue_locators") or []:
        if not isinstance(locator, dict):
            continue
        name = str(locator.get("ligand_name") or "").lower()
        ligand_id = locator.get("ligand_id")
        if "pyridoxal" in name and ligand_id:
            chebi = str(ligand_id)
            break
    return [
        {
            "name": _PLP_NAME,
            "cross_reference": {"id": chebi},
            "evidence_codes": [],
            "provenance": "derived_from_reviewed_cofactor_family_flags_plp_evidence",
        }
    ]


def _normalize_row(
    row: dict[str, Any], *, schema: str, index: dict[str, set[str]]
) -> dict[str, Any]:
    """Project a pool row onto the engine's expected input schema."""
    normalized = dict(row)
    screen = rerun_current702_duplicate_screen(row, index=index)
    normalized["duplicate_current_registry_conflict_status"] = screen[
        "duplicate_current_registry_conflict_status"
    ]
    normalized["_scaleout_screen_detail"] = screen["screen_detail"]
    if schema == "shard" and not normalized.get("cofactor_provenance"):
        synthesized = _synthesize_plp_cofactor_provenance(row)
        if synthesized:
            normalized["cofactor_provenance"] = synthesized
    return normalized


def classify_scaleout_row(row: dict[str, Any], *, pool: str) -> dict[str, Any]:
    """Conservative scope decision over the extended scale-out lane vocabulary."""
    dup_status = str(row.get("duplicate_current_registry_conflict_status") or "")
    if not dup_status.startswith("no_exact"):
        return {"decision": "skip", "reason": "current702_duplicate_screen_not_confirmed"}

    if pool in COFACTOR_CONFOUNDED_HOLD_POOLS:
        return {
            "decision": "hold",
            "reason": "cofactor_confounded_redox_pool_held_for_disambiguation",
            "lane": row.get("target_family_lane"),
        }

    lane = row.get("target_family_lane")
    cofactors = cofactor_classes(row)

    if lane in SCALEOUT_PRIMARY_LANES:
        fingerprint = SCALEOUT_PRIMARY_LANES[lane]
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
    if lane in SCALEOUT_OUT_OF_SCOPE_LANES:
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


def _tag_scaleout_provenance(
    label: dict[str, Any], *, pool: str, source_artifact: str
) -> None:
    """Record the scale-out pool/source on the engine-built label (provenance only)."""
    evidence = label["evidence"]
    evidence["sources"] = ["external_scaleout_bronze_import"]
    evidence.setdefault("source_provenance", {})["scaleout_pool"] = pool
    evidence["source_provenance"]["scaleout_source_artifact"] = source_artifact
    evidence.setdefault("notes", []).append(
        f"scale-out drain batch: pool={pool}; source={source_artifact}; same "
        "conservative annotation-anchored policy as the Wave 2 engine"
    )


def build_scaleout_bronze_import(
    *,
    pools: list[dict[str, Any]],
    registry: list[dict[str, Any]],
    index: dict[str, set[str]],
) -> dict[str, Any]:
    """Drain every pool through the conservative engine into one preview artifact."""
    existing_entry_ids = {str(label.get("entry_id")) for label in registry}
    seen_accessions: set[str] = set()

    new_labels: list[dict[str, Any]] = []
    holds: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []

    decision_counts: Counter[str] = Counter()
    label_type_counts: Counter[str] = Counter()
    fingerprint_counts: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()
    hold_reasons: Counter[str] = Counter()
    lane_scope: dict[str, Counter[str]] = {}
    per_pool: dict[str, Counter[str]] = {}

    total_rows = 0
    for spec in pools:
        pool = str(spec["pool"])
        schema = str(spec["schema"])
        source_artifact = Path(str(spec["path"])).stem
        rows = spec["rows"]
        per_pool.setdefault(pool, Counter())
        for raw in rows:
            total_rows += 1
            row = _normalize_row(raw, schema=schema, index=index)
            decision = classify_scaleout_row(row, pool=pool)
            decision_counts[decision["decision"]] += 1
            per_pool[pool][decision["decision"]] += 1
            accession = _clean_accession(row.get("accession"))
            entry_id = f"uniprot:{accession}"

            if decision["decision"] == "skip":
                skips.append({"accession": accession, "pool": pool, "reason": decision["reason"]})
                continue
            if decision["decision"] == "hold":
                hold_reasons[decision["reason"]] += 1
                holds.append(
                    {
                        "accession": accession,
                        "pool": pool,
                        "lane": decision.get("lane"),
                        "reason": decision["reason"],
                    }
                )
                continue

            if entry_id in existing_entry_ids or accession in seen_accessions:
                skips.append(
                    {
                        "accession": accession,
                        "pool": pool,
                        "reason": "duplicate_entry_id_in_registry_or_batch",
                    }
                )
                decision_counts["skip"] += 1
                per_pool[pool]["skip_duplicate"] += 1
                continue
            seen_accessions.add(accession)

            label = _build_label(row, decision)
            _tag_scaleout_provenance(label, pool=pool, source_artifact=source_artifact)
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
            "v3_external_scaleout_bronze_import_preview_current702_20260609"
        ),
        "schema_version": "external_annotation_anchored_import.v1",
        "created_utc": _utc_now_iso(),
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "drain_basis": (
            "scale-out of the Wave 2 annotation-anchored engine over already-"
            "materialized import-ready pools (no new sourcing); the 324 skipped "
            "Wave 2 rows had their current702 duplicate screen re-run and "
            "promoted, the four shard pools were classified by the same "
            "conservative policy"
        ),
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
            "current702_duplicate_screen_rerun_against_both_registries": True,
            "cofactor_confounded_redox_pool_held": True,
            "secondary_probe_radical_sam_cobalamin_held": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
        },
        "counts": {
            "preview_rows": total_rows,
            "decision_counts": dict(decision_counts),
            "per_pool_decision_counts": {
                pool: dict(counter) for pool, counter in sorted(per_pool.items())
            },
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
            "On explicit authorization, append `applied_labels` to the SEPARATE "
            "expansion registry `data/registries/external_bronze_labels.json` via "
            "`apply-external-annotation-anchored-import` (the frozen current702 "
            "benchmark registry is never written; labels dedup against BOTH "
            "registries and validate through the label schema). The held "
            "cofactor-confounded redox and secondary-probe radical-SAM/cobalamin "
            "lanes await the cofactor/EC disambiguation task."
        ),
        "applied_labels": new_labels,
        "holds_sample": holds[:50],
        "skips_sample": skips[:50],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Scale-Out Annotation-Anchored Bronze Import — drain batch (non-destructive)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Drains the already-materialized import-ready pools through the same",
        "conservative annotation-anchored engine. No new sourcing. EC/name/prose",
        "stay in excluded_context (never predictive); structure/geometry",
        "confirmation is a deferred bronze->silver promotion signal. The curated",
        "current702 benchmark registry is NOT written by this run.",
        "",
        "## Result",
        "",
        f"- Pool rows considered: {c['preview_rows']}.",
        f"- **Importable bronze labels this batch: {c['importable_new_labels']}** "
        f"-> expansion registry {c['current_registry_labels']} -> "
        f"**{c['projected_registry_labels_if_merged']}** if merged.",
        f"- Label types: {c['label_type_counts']}.",
        f"- Positive fingerprints: {c['fingerprint_counts']}.",
        f"- Confidence: {c['confidence_counts']}.",
        f"- Held for review: {c['hold_count']} ({c['hold_reason_counts']}).",
        f"- Skipped: {c['skip_count']}.",
        "",
        "## Per-pool decisions",
        "",
        "| Pool | decisions |",
        "| --- | --- |",
    ]
    for pool, counter in c["per_pool_decision_counts"].items():
        lines.append(f"| {pool} | {counter} |")
    lines.extend(
        [
            "",
            "## Diversity by lane (label_type split)",
            "",
            "| Lane | imported scope split |",
            "| --- | --- |",
        ]
    )
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
            "- current702 duplicate screen re-run against BOTH registries: "
            f"{audit['guardrails']['current702_duplicate_screen_rerun_against_both_registries']}.",
            "- Cofactor-confounded redox pool held: "
            f"{audit['guardrails']['cofactor_confounded_redox_pool_held']}.",
            "- All new labels bronze / automation_curated; uniprot namespace; "
            "heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def load_scaleout_pools(
    specs: tuple[dict[str, str], ...] = SCALEOUT_POOLS,
) -> list[dict[str, Any]]:
    """Load each pool's rows. The wave2 pool keeps only its unscreened rows."""
    loaded: list[dict[str, Any]] = []
    for spec in specs:
        payload = _load_json(Path(spec["path"]))
        rows = _preview_rows(payload)
        if spec.get("only_unscreened") == "true":
            rows = [
                row
                for row in rows
                if not str(
                    row.get("duplicate_current_registry_conflict_status") or ""
                ).startswith("no_exact")
            ]
        loaded.append({**spec, "rows": rows})
    return loaded


def write_scaleout_bronze_import(
    *,
    out_path: Path,
    report_path: Path | None = None,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    specs: tuple[dict[str, str], ...] = SCALEOUT_POOLS,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    index = build_current702_reference_index(
        current_manifest_payload=_load_json(current_manifest_path),
        frozen_benchmark_payload=frozen,
        expansion_payload=expansion,
    )
    audit = build_scaleout_bronze_import(
        pools=load_scaleout_pools(specs),
        registry=expansion,
        index=index,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
