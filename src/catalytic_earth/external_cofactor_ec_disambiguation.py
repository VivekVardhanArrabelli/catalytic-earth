"""Cofactor/EC disambiguation for the held redox and radical-SAM/cobalamin lanes.

The scale-out drain HELD two families of rows -- do not guess:
- the entire ``redox_cofactor_confounded`` pool (cofactor-confounded redox), and
- the secondary-probe radical-SAM / cobalamin lanes.

This module makes a high-precision subset of them *countable* by corroborating
the annotated cofactor identity against the reviewed reaction/EC class. Scope is
still decided ONLY from reviewed Swiss-Prot/EC/Rhea/cofactor annotation -- the
same field-standard bronze basis -- and EC stays in ``excluded_context``, never a
predictive feature (the benchmark scorer never sees it). Using EC + cofactor to
*decide a label's scope* is exactly what the annotation-anchored basis permits;
the leakage wall (EC/name/prose are never predictive) is unchanged.

A row is disambiguated to a fingerprint only when an annotated cofactor AND a
uniquely matching reaction class agree, and no *other* fingerprint's rule also
fires (multi-signal rows stay held). Each rule below is the textbook cofactor +
EC-class signature of one of the eight fingerprints:

- ``heme_peroxidase_oxidase``  : heme cofactor + EC 1.11.1 (peroxidase).
- ``flavin_monooxygenase``     : flavin (FAD/FMN), no heme + EC 1.14.13/1.14.14
                                 (NAD(P)H- or reduced-flavin-dependent, one O
                                 inserted).
- ``flavin_dehydrogenase_reductase`` : flavin, no heme + EC 1.3 (CH-CH donor),
                                 1.6 (on NAD(P)H), or 1.8.1 (disulfide reductase)
                                 -- hydride/electron transfer, no oxygen insertion.
- ``radical_sam_enzyme``       : CX3CX2C radical-SAM motif, or [4Fe-4S] + SAM
                                 both annotated.
- ``cobalamin_radical_rearrangement`` : adenosylcobalamin/B12 + a mutase /
                                 eliminase EC (5.4.99, 5.4.3, 4.2.1.28/30,
                                 4.3.1.7).

Output is NON-DESTRUCTIVE: a preview artifact in the engine's preview schema
(``applied_labels`` ready for ``apply-external-annotation-anchored-import``, which
appends to the SEPARATE ``external_bronze_labels.json`` expansion registry and
never touches the frozen current702 benchmark).
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from .external_annotation_anchored_import import (
    _build_label,
    _load_json,
    _preview_rows,
    _utc_now_iso,
    cofactor_classes,
)
from .external_scaleout_bronze_import import (
    DEFAULT_CURRENT_MANIFEST_PATH,
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
    _clean_accession,
    build_current702_reference_index,
    rerun_current702_duplicate_screen,
)

# ChEBI ids used only to record a synthesized cofactor on rows that carry their
# cofactor evidence as family flags + residue ligands rather than a cofactor list.
_FE4S4_CHEBI = "CHEBI:49883"
_SAM_CHEBI = "CHEBI:59789"
_ADOCBL_CHEBI = "CHEBI:18408"

# The held pools this module re-examines (all classified "hold" by the scale-out
# drain). ``schema`` selects normalization; ``lanes`` (when present) restricts a
# shard to its secondary-probe lanes.
DISAMBIGUATION_POOLS: tuple[dict[str, Any], ...] = (
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
        "lanes": (
            "B12 adenosylcobalamin enzymes",
            "B12/cobalamin broad enzymes",
            "cobalamin radical rearrangement",
            "coupled PLP adenosylcobalamin aminomutase",
            "radical SAM named families",
            "radical SAM iron-sulfur",
            "SAM-dependent radical-like boundary",
        ),
    },
    {
        "pool": "wave2_held_redox_radical",
        "schema": "wave2",
        "path": (
            "artifacts/"
            "v3_external_materialization_wave2_import_ready_preview_current702_20260609.json"
        ),
        "lanes": ("redox oxygen/sulfur", "radical-SAM/cobalamin"),
        "only_unscreened": True,
    },
)


def _ec_numbers(row: dict[str, Any]) -> list[str]:
    return [
        str(e)
        for e in (row.get("rhea_ec_provenance") or {}).get("ec_numbers") or []
    ]


def _ec_has_prefix(row: dict[str, Any], prefixes: tuple[str, ...]) -> bool:
    return any(ec.startswith(p) for ec in _ec_numbers(row) for p in prefixes)


def _ligand_names(row: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for locator in row.get("residue_locators") or []:
        if isinstance(locator, dict) and locator.get("ligand_name"):
            names.append(str(locator["ligand_name"]).lower())
    return names


def cofactor_evidence(row: dict[str, Any]) -> dict[str, bool]:
    """Annotated cofactor evidence, fused across the row's evidence channels.

    Reads cofactor names, the shard ``cofactor_family_flags``, and the active-site
    residue ligand names so a row's cofactor identity is detected however the
    materialization pipeline recorded it.
    """
    names = [
        str(c.get("name") or "").lower()
        for c in (row.get("cofactor_provenance") or [])
    ] + _ligand_names(row)
    flags = row.get("cofactor_family_flags") or {}

    def any_name(*keys: str) -> bool:
        return any(any(k in n for k in keys) for n in names)

    return {
        # Catalytic divalent metal (Zn/Mn/Mg/Fe/Ni/Co/Cu/Ca/Cd). UniProt spells the
        # oxidation state inline ("Zn(2+)", "Co(2+)"), so match the element stems.
        # "cob(...)alamin" is matched by the cobalamin key below, not here ("cob" !=
        # "cobalt"), so B12 enzymes do not read as bare metal.
        "metal": any_name(
            "zn",
            "zinc",
            "mn",
            "manganese",
            "mg",
            "magnesium",
            "fe(",
            "fe2",
            "fe3",
            "iron",
            "ni(",
            "nickel",
            "cobalt",
            "co(2",
            "cu",
            "copper",
            "ca(2",
            "calcium",
            "cadmium",
            "divalent metal",
        ),
        "heme": any_name("heme", "haem"),
        "flavin": any_name("fad", "fmn", "flavin"),
        "fe_s": any_name("fe-s", "4fe-4s", "2fe-2s", "3fe-4s", "iron-sulfur")
        or bool(flags.get("sf4_or_fe_s_evidence_present")),
        "sam": any_name("s-adenosyl-l-methionine", "adenosylmethionine", "adomet")
        or bool(flags.get("sam_or_adomet_evidence_present")),
        "cx3cx2c_motif": bool(flags.get("cx3cx2c_motif_evidence_present")),
        # UniProt records B12 cofactors with the cobalt oxidation state spelled
        # inline -- "adenosylcob(III)alamin", "cob(II)alamin", "methylcob(III)alamin"
        # -- so the bare substring "cobalamin" never matches the canonical names.
        # Match the cob(I/II/III)alamin stems too (scope-only annotation read).
        "cobalamin": any_name(
            "cobalamin",
            "adenosylcobalamin",
            "b12",
            "cobamamide",
            "cob(i)alamin",
            "cob(ii)alamin",
            "cob(iii)alamin",
        )
        or bool(flags.get("cobalamin_or_b12_evidence_present")),
    }


# EC-prefix signatures for the metal_dependent_hydrolase v2 sub-families (Stage 2).
# Mutually exclusive prefixes + an annotated catalytic metal keep "exactly one rule
# fires"; the metal requirement excludes Ser/Cys peptidases (3.4.21/22/23), Cys-based
# protein-tyrosine phosphatases (3.1.3.48 carry no catalytic metal), and serine
# amidases. EC is used for SCOPE only and stays in excluded_context (never predictive).
_METALLOPEPTIDASE_EC = ("3.4.24", "3.4.17", "3.4.11")
_METALLOPHOSPHOESTERASE_NUCLEASE_EC = (
    "3.1.4",
    "3.1.11",
    "3.1.12",
    "3.1.13",
    "3.1.14",
    "3.1.15",
    "3.1.16",
    "3.1.21",
    "3.1.22",
    "3.1.23",
    "3.1.24",
    "3.1.25",
    "3.1.26",
    "3.1.27",
    "3.1.30",
    "3.1.31",
)
_METALLOPHOSPHOMONOESTERASE_EC = ("3.1.3",)
_METALLO_AMIDOHYDROLASE_DEAMINASE_EC = ("3.5.2", "3.5.4", "3.5.1")


# Each rule: fingerprint id -> predicate over (cofactor_evidence, row).
DISAMBIGUATION_RULES: tuple[tuple[str, Callable[[dict[str, bool], dict[str, Any]], bool]], ...] = (
    (
        "heme_peroxidase_oxidase",
        lambda c, row: c["heme"] and _ec_has_prefix(row, ("1.11.1",)),
    ),
    (
        "metallopeptidase",
        lambda c, row: c["metal"] and _ec_has_prefix(row, _METALLOPEPTIDASE_EC),
    ),
    (
        "metallophosphoesterase_nuclease",
        lambda c, row: c["metal"]
        and _ec_has_prefix(row, _METALLOPHOSPHOESTERASE_NUCLEASE_EC),
    ),
    (
        "metallophosphomonoesterase",
        lambda c, row: c["metal"] and _ec_has_prefix(row, _METALLOPHOSPHOMONOESTERASE_EC),
    ),
    (
        "metallo_amidohydrolase_deaminase",
        lambda c, row: c["metal"]
        and _ec_has_prefix(row, _METALLO_AMIDOHYDROLASE_DEAMINASE_EC),
    ),
    (
        "flavin_monooxygenase",
        lambda c, row: c["flavin"]
        and not c["heme"]
        and _ec_has_prefix(row, ("1.14.13", "1.14.14")),
    ),
    (
        "flavin_dehydrogenase_reductase",
        lambda c, row: c["flavin"]
        and not c["heme"]
        and _ec_has_prefix(row, ("1.3.", "1.6.", "1.8.1")),
    ),
    (
        "radical_sam_enzyme",
        lambda c, row: c["cx3cx2c_motif"] or (c["fe_s"] and c["sam"]),
    ),
    (
        "cobalamin_radical_rearrangement",
        lambda c, row: c["cobalamin"]
        and _ec_has_prefix(row, ("5.4.99", "5.4.3", "4.2.1.28", "4.2.1.30", "4.3.1.7")),
    ),
)


def disambiguate_row(row: dict[str, Any]) -> dict[str, Any]:
    """Assign a fingerprint only when exactly one rule fires (else stay held)."""
    evidence = cofactor_evidence(row)
    matched = [fp for fp, rule in DISAMBIGUATION_RULES if rule(evidence, row)]
    distinct = sorted(set(matched))
    if not distinct:
        return {"decision": "hold", "reason": "no_cofactor_ec_corroboration"}
    if len(distinct) > 1:
        return {
            "decision": "hold",
            "reason": "multi_fingerprint_signal_conflict",
            "candidates": distinct,
        }
    return {"decision": "import", "fingerprint_id": distinct[0], "cofactor_evidence": evidence}


def _synthesize_cofactor_provenance(
    row: dict[str, Any], fingerprint: str, evidence: dict[str, bool]
) -> list[dict[str, Any]]:
    """Surface a synthesized cofactor record when the row carries none.

    Honest provenance: the cofactor was read from reviewed family-flag / residue
    ligand evidence; each record is tagged with that derivation.
    """
    existing = row.get("cofactor_provenance") or []
    if existing:
        return list(existing)
    tag = "derived_from_reviewed_cofactor_family_flags_and_residue_ligands"
    records: list[dict[str, Any]] = []
    if fingerprint == "radical_sam_enzyme":
        records = [
            {"name": "[4Fe-4S] cluster", "cross_reference": {"id": _FE4S4_CHEBI}},
            {"name": "S-adenosyl-L-methionine", "cross_reference": {"id": _SAM_CHEBI}},
        ]
    elif fingerprint == "cobalamin_radical_rearrangement":
        records = [{"name": "adenosylcobalamin", "cross_reference": {"id": _ADOCBL_CHEBI}}]
    elif evidence.get("heme"):
        records = [{"name": "heme", "cross_reference": {"id": None}}]
    elif evidence.get("flavin"):
        records = [{"name": "FAD", "cross_reference": {"id": None}}]
    elif evidence.get("metal"):
        records = [{"name": "catalytic divalent metal", "cross_reference": {"id": None}}]
    for record in records:
        record["evidence_codes"] = []
        record["provenance"] = tag
    return records


def _normalize_row(
    row: dict[str, Any], *, fingerprint: str, evidence: dict[str, bool], index
) -> dict[str, Any]:
    normalized = dict(row)
    screen = rerun_current702_duplicate_screen(row, index=index)
    normalized["duplicate_current_registry_conflict_status"] = screen[
        "duplicate_current_registry_conflict_status"
    ]
    normalized["cofactor_provenance"] = _synthesize_cofactor_provenance(
        row, fingerprint, evidence
    )
    return normalized


def _build_decision(
    row: dict[str, Any], fingerprint: str
) -> dict[str, Any]:
    classes = sorted(cofactor_classes(row))
    ec = _ec_numbers(row)
    return {
        "decision": "import",
        "label_type": "seed_fingerprint",
        "fingerprint_id": fingerprint,
        "reason": (
            f"cofactor_ec_disambiguation_to_{fingerprint}_"
            f"from_annotated_cofactor_and_ec_class_{ec or 'n/a'}"
        ),
        "cofactor_classes": classes,
    }


def build_cofactor_ec_disambiguation(
    *,
    pools: list[dict[str, Any]],
    registry: list[dict[str, Any]],
    index,
) -> dict[str, Any]:
    existing_entry_ids = {str(label.get("entry_id")) for label in registry}
    seen_accessions: set[str] = set()

    new_labels: list[dict[str, Any]] = []
    holds: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []

    decision_counts: Counter[str] = Counter()
    fingerprint_counts: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()
    hold_reasons: Counter[str] = Counter()
    per_pool: dict[str, Counter[str]] = {}
    lane_scope: dict[str, Counter[str]] = {}

    total_rows = 0
    for spec in pools:
        pool = str(spec["pool"])
        source_artifact = Path(str(spec["path"])).stem
        per_pool.setdefault(pool, Counter())
        for raw in spec["rows"]:
            total_rows += 1
            verdict = disambiguate_row(raw)
            if verdict["decision"] == "hold":
                decision_counts["hold"] += 1
                per_pool[pool]["hold"] += 1
                hold_reasons[verdict["reason"]] += 1
                holds.append(
                    {
                        "accession": _clean_accession(raw.get("accession")),
                        "pool": pool,
                        "lane": raw.get("target_family_lane"),
                        "reason": verdict["reason"],
                        "candidates": verdict.get("candidates"),
                    }
                )
                continue

            fingerprint = verdict["fingerprint_id"]
            row = _normalize_row(
                raw, fingerprint=fingerprint, evidence=verdict["cofactor_evidence"], index=index
            )
            if not str(
                row.get("duplicate_current_registry_conflict_status") or ""
            ).startswith("no_exact"):
                decision_counts["skip"] += 1
                per_pool[pool]["skip_screen"] += 1
                skips.append(
                    {
                        "accession": _clean_accession(raw.get("accession")),
                        "pool": pool,
                        "reason": "current702_duplicate_screen_not_confirmed",
                    }
                )
                continue

            accession = _clean_accession(row.get("accession"))
            entry_id = f"uniprot:{accession}"
            if entry_id in existing_entry_ids or accession in seen_accessions:
                decision_counts["skip"] += 1
                per_pool[pool]["skip_duplicate"] += 1
                skips.append(
                    {
                        "accession": accession,
                        "pool": pool,
                        "reason": "duplicate_entry_id_in_registry_or_batch",
                    }
                )
                continue
            seen_accessions.add(accession)

            decision = _build_decision(row, fingerprint)
            label = _build_label(row, decision)
            evidence = label["evidence"]
            evidence["sources"] = ["external_cofactor_ec_disambiguation"]
            evidence.setdefault("source_provenance", {})["disambiguation_pool"] = pool
            evidence["source_provenance"]["disambiguation_source_artifact"] = source_artifact
            evidence.setdefault("import_gate_evidence", []).append(
                "cofactor_ec_disambiguation_unique_fingerprint_match"
            )
            evidence.setdefault("notes", []).append(
                "cofactor/EC disambiguation of a previously-held "
                f"cofactor-confounded/secondary-probe row: {pool}; EC class used "
                "for scope assignment only (review-only; never a predictive feature)"
            )
            new_labels.append(label)
            decision_counts["import"] += 1
            per_pool[pool]["import"] += 1
            fingerprint_counts[fingerprint] += 1
            confidence_counts[label["confidence"]] += 1
            lane = str(raw.get("target_family_lane"))
            lane_scope.setdefault(lane, Counter())[fingerprint] += 1

    current_total = len(registry)
    imported = len(new_labels)
    return {
        "artifact_id": (
            "v3_external_cofactor_ec_disambiguation_preview_current702_20260609"
        ),
        "schema_version": "external_annotation_anchored_import.v1",
        "created_utc": _utc_now_iso(),
        "status": "non_destructive_preview_pending_explicit_registry_merge_authorization",
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "disambiguation_basis": (
            "previously-held cofactor-confounded redox and secondary-probe "
            "radical-SAM/cobalamin rows made countable by corroborating the "
            "annotated cofactor identity against the reviewed reaction/EC class; "
            "only unique single-fingerprint matches are imported, multi-signal "
            "rows stay held; EC is used for scope assignment only and remains a "
            "review-only, non-predictive feature"
        ),
        "guardrails": {
            "curated_registry_written": False,
            "frozen_current702_benchmark_preserved": True,
            "expansion_labels_written_to_separate_registry_not_benchmark": True,
            "predictive_features_use_ec_name_or_prose": False,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "ec_name_prose_excluded_context_on_every_label": True,
            "all_new_labels_tier": "bronze",
            "all_new_labels_review_status": "automation_curated",
            "external_entry_id_namespace": "uniprot",
            "heldout_benchmark_unchanged": True,
            "current702_accession_sequence_duplicate_screen_required": True,
            "multi_fingerprint_signal_rows_held": True,
            "structure_geometry_confirmation_is_deferred_promotion_signal": True,
        },
        "counts": {
            "examined_rows": total_rows,
            "decision_counts": dict(decision_counts),
            "per_pool_decision_counts": {
                pool: dict(counter) for pool, counter in sorted(per_pool.items())
            },
            "importable_new_labels": imported,
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
            "`apply-external-annotation-anchored-import`. Rows still held "
            "(no/ambiguous cofactor-EC corroboration) remain a review queue."
        ),
        "applied_labels": new_labels,
        "holds_sample": holds[:50],
        "skips_sample": skips[:50],
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Cofactor/EC Disambiguation Of Held Redox + Radical-SAM/Cobalamin Lanes",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Makes a high-precision subset of the previously-HELD cofactor-confounded",
        "redox and secondary-probe radical-SAM/cobalamin rows countable, by",
        "corroborating the annotated cofactor against the reviewed reaction/EC",
        "class. Only unique single-fingerprint matches are imported; multi-signal",
        "rows stay held. EC is used for scope assignment only and is never a",
        "predictive feature. The frozen current702 benchmark is NOT written.",
        "",
        "## Result",
        "",
        f"- Held rows examined: {c['examined_rows']}.",
        f"- **Disambiguated bronze labels: {c['importable_new_labels']}** "
        f"-> expansion registry {c['current_registry_labels']} -> "
        f"**{c['projected_registry_labels_if_merged']}** if merged.",
        f"- Fingerprints recovered: {c['fingerprint_counts']}.",
        f"- Confidence: {c['confidence_counts']}.",
        f"- Still held: {c['hold_count']} ({c['hold_reason_counts']}).",
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
            "## Diversity by lane (recovered fingerprint)",
            "",
            "| Lane | recovered |",
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
            "- EC used for scope assignment only, never predictive: "
            f"{audit['guardrails']['ec_used_for_scope_assignment_only_never_predictive']}.",
            "- Multi-fingerprint-signal rows held: "
            f"{audit['guardrails']['multi_fingerprint_signal_rows_held']}.",
            "- All new labels bronze / automation_curated; uniprot namespace; "
            "heldout benchmark unchanged.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def load_disambiguation_pools(
    specs: tuple[dict[str, Any], ...] = DISAMBIGUATION_POOLS,
) -> list[dict[str, Any]]:
    loaded: list[dict[str, Any]] = []
    for spec in specs:
        rows = _preview_rows(_load_json(Path(spec["path"])))
        if spec.get("only_unscreened"):
            rows = [
                row
                for row in rows
                if not str(
                    row.get("duplicate_current_registry_conflict_status") or ""
                ).startswith("no_exact")
            ]
        lanes = spec.get("lanes")
        if lanes:
            allowed = set(lanes)
            rows = [row for row in rows if row.get("target_family_lane") in allowed]
        loaded.append({**spec, "rows": rows})
    return loaded


def write_cofactor_ec_disambiguation(
    *,
    out_path: Path,
    report_path: Path | None = None,
    current_manifest_path: Path = DEFAULT_CURRENT_MANIFEST_PATH,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    specs: tuple[dict[str, Any], ...] = DISAMBIGUATION_POOLS,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    index = build_current702_reference_index(
        current_manifest_payload=_load_json(current_manifest_path),
        frozen_benchmark_payload=frozen,
        expansion_payload=expansion,
    )
    audit = build_cofactor_ec_disambiguation(
        pools=load_disambiguation_pools(specs),
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
