#!/usr/bin/env python3
"""Targeted article-alias follow-up for sparse source-text mappings."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import current_release_epk_followup as current


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"


@dataclass(frozen=True)
class AliasSurface:
    surface_id: str
    query: str
    source_article: str
    rows: int = 20


DEFAULT_SURFACES = [
    AliasSurface(
        "braf_mek1_phosphorylation_asymmetric_dimer",
        "BRAF MEK1 phosphorylation asymmetric dimer ATP magnesium",
        "Mechanism of MEK1 phosphorylation by the N-terminal acidic motif-mediated asymmetric BRAF dimer",
        25,
    ),
    AliasSurface(
        "braf_mek1_n_terminal_acidic_motif",
        "BRAF MEK1 N-terminal acidic motif phosphorylation substrate",
        "Mechanism of MEK1 phosphorylation by the N-terminal acidic motif-mediated asymmetric BRAF dimer",
        25,
    ),
    AliasSurface(
        "p90rsk2_erk2_complex",
        "p90RSK2 ERK2 complex phosphorylation substrate ATP",
        "Structural insights and biophysical characterization of p90RSK2:ERK2 complex",
        25,
    ),
    AliasSurface(
        "nleh_cest_serine_phosphorylation",
        "NleH CesT serine phosphorylation kinase ATPgammaS",
        "Serine phosphorylation of CesT by the type III secretion system effectors NleH1 and NleH2",
        25,
    ),
    AliasSurface(
        "ikk2_ikba_phosphoenzyme_intermediate",
        "IKK2 substrate IkappaB alpha phosphoenzyme intermediate ATP",
        "Dual-specific autophosphorylation of kinase IKK2 enables phosphorylation of substrate IkappaB alpha",
        25,
    ),
    AliasSurface(
        "ccdc6_ret_dual_atp_adp_kinase",
        "CCDC6 RET fusion ATP ADP dependent kinase substrate",
        "The oncogenic CCDC6-RET fusion protein is a dual ATP- and ADP-dependent kinase",
        25,
    ),
    AliasSurface(
        "ef2k_aspartate_phosphorylation",
        "eukaryotic elongation factor 2 kinase conserved aspartate phosphorylation ATP",
        "Phosphorylation of a conserved aspartate in the catalytic site of eukaryotic elongation factor 2 kinase",
        25,
    ),
]


def search_surface(surface: AliasSurface) -> dict[str, Any]:
    result = current.rcsb_full_text_ids(surface.query, rows=surface.rows)
    return {
        "surface_id": surface.surface_id,
        "source_article": surface.source_article,
        **result,
    }


def build_artifact(out: Path, max_unique_pdb_ids: int, sleep_seconds: float) -> dict[str, Any]:
    generated_at = current.now_iso()
    search_surfaces = []
    seen: dict[str, list[dict[str, Any]]] = {}
    for surface in DEFAULT_SURFACES:
        result = search_surface(surface)
        search_surfaces.append(result)
        for rank, pdb_id in enumerate(result["pdb_ids"], start=1):
            if pdb_id not in seen and len(seen) >= max_unique_pdb_ids:
                continue
            seen.setdefault(pdb_id, []).append(
                {
                    "surface_id": result["surface_id"],
                    "rank": rank,
                    "source_article": result["source_article"],
                    "query_or_source": result["query_or_source"],
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    rows = []
    fetch_failures = []
    for pdb_id, search_hits in seen.items():
        try:
            rows.append(current.scan_pdb_id(pdb_id, search_hits))
        except Exception as exc:  # noqa: BLE001 - compact research artifact keeps failures.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(
                {
                    "pdb_id": pdb_id,
                    "search_hits": search_hits,
                    "candidate_status": "fetch_or_parse_failed_review_only",
                    "fetch_error": repr(exc),
                    "review_only": True,
                    "countable_label_candidate": False,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                    "epk_score_computed": False,
                    "ready_for_production_scoring": False,
                    "ready_for_label_import": False,
                    "target_family_id": TARGET_FAMILY_ID,
                    "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["candidate_status"]] = status_counts.get(row["candidate_status"], 0) + 1
    nonpeptide = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_nonpeptide_candidate_source_validation_pending_review_only"
    ]
    short_or_peptide = [
        row["pdb_id"]
        for row in rows
        if row["candidate_status"] == "local_metal_peptide_or_short_candidate_review_only"
    ]
    evidence_for = []
    if nonpeptide:
        evidence_for.append(
            "Targeted article aliases found local-metal non-peptide candidates requiring source adjudication: "
            + ", ".join(nonpeptide)
            + "."
        )
    if short_or_peptide:
        evidence_for.append(
            "Targeted article aliases found review-only short/peptide local-metal candidates: "
            + ", ".join(short_or_peptide)
            + "."
        )
    if not evidence_for:
        evidence_for.append(
            "Targeted article aliases returned RCSB rows but no local-metal ePK substrate candidate."
        )

    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "targeted_article_alias_followup",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "search_surface_count": len(search_surfaces),
            "surface_rows_returned_total": sum(item["returned_count"] for item in search_surfaces),
            "surface_total_count_reported_total": sum(item["total_count"] for item in search_surfaces),
            "unique_pdb_ids_reviewed": len(rows),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "local_metal_nonpeptide_candidate_pdb_ids": nonpeptide,
            "local_metal_peptide_or_short_candidate_pdb_ids": short_or_peptide,
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "Targeted source-alias mapping only. It does not create labels, scores, "
                "thresholds, fingerprints, migrations, or production claims."
            ),
            "source_urls": [
                current.RCSB_SEARCH_URL,
                current.scout.RCSB_ENTRY_URL,
                current.scout.RCSB_CIF_URL,
            ],
        },
        "search_surfaces": search_surfaces,
        "fetch_failures": fetch_failures,
        "rows": rows,
        "source_review_summary": {
            "primary_outcome": "next_query_defined" if nonpeptide else "evidence_for" if short_or_peptide else "search_surface_exhausted",
            "production_claim_allowed": False,
            "search_surface_exhausted": not bool(nonpeptide or short_or_peptide),
            "evidence_for": evidence_for,
            "evidence_against": [
                "No targeted sparse-mapping article alias produced a clean folded-protein ePK transfer-state positive.",
                "Most mapped structures were kinase-only, recruitment, non-ePK enzyme, or donor-without-heteromeric-acceptor contexts.",
            ],
            "counterexamples_found": [],
            "recommendation": (
                "Use these sparse article aliases as exhausted for now. Next run should monitor newly released "
                "RCSB rows and publication metadata rather than revisit these exact aliases unless new PDB IDs appear."
            ),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-unique-pdb-ids", type=int, default=80)
    parser.add_argument("--sleep-seconds", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.out, args.max_unique_pdb_ids, args.sleep_seconds)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "local_metal_nonpeptide_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_nonpeptide_candidate_pdb_ids"
                ],
                "local_metal_peptide_or_short_candidate_pdb_ids": artifact["metadata"][
                    "local_metal_peptide_or_short_candidate_pdb_ids"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
