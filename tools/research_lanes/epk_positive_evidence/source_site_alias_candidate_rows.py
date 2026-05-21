#!/usr/bin/env python3
"""Guarded source-site alias candidate-row search.

This helper targets named folded-substrate phosphorylation-site aliases that
are easy to miss with generic source wording. It reuses the guarded candidate
row emitter and skips prior lane PDB IDs by default.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import guarded_phrase_candidate_rows as guarded


SURFACE_SET_NAME = "source_site_alias_terms"

SOURCE_SITE_ALIAS_SURFACES = [
    guarded.GuardedSurface(
        "braf_mek_ser218_ser222_amp_pnp_gamma",
        "BRAF MEK Ser218 Ser222 AMP-PNP",
        "gamma",
        100,
        0,
        "Targets RAF/MEK folded substrate site aliases with AMP-PNP.",
    ),
    guarded.GuardedSurface(
        "braf_mek_ser218_ser222_atpgammas_gamma",
        "BRAF MEK Ser218 Ser222 ATPgammaS",
        "gamma",
        100,
        0,
        "Targets RAF/MEK folded substrate site aliases with ATPgammaS.",
    ),
    guarded.GuardedSurface(
        "craf_mek_ser218_ser222_atpgammas_gamma",
        "CRAF MEK Ser218 Ser222 ATPgammaS",
        "gamma",
        100,
        0,
        "Targets recent CRAF/MEK ATPgammaS source wording.",
    ),
    guarded.GuardedSurface(
        "mek_erk_thr202_tyr204_amp_pnp_gamma",
        "MEK ERK Thr202 Tyr204 AMP-PNP",
        "gamma",
        100,
        0,
        "Targets MEK/ERK activation-loop acceptor aliases with AMP-PNP.",
    ),
    guarded.GuardedSurface(
        "mek_erk_thr202_tyr204_atpgammas_gamma",
        "MEK ERK Thr202 Tyr204 ATPgammaS",
        "gamma",
        100,
        0,
        "Targets MEK/ERK activation-loop acceptor aliases with ATPgammaS.",
    ),
    guarded.GuardedSurface(
        "pink1_ubiquitin_ser65_amp_pnp_gamma",
        "PINK1 ubiquitin Ser65 AMP-PNP",
        "gamma",
        100,
        0,
        "Targets PINK1/ubiquitin folded substrate Ser65 source aliases.",
    ),
    guarded.GuardedSurface(
        "pink1_ubiquitin_ser65_atpgammas_gamma",
        "PINK1 ubiquitin Ser65 ATPgammaS",
        "gamma",
        100,
        0,
        "Targets PINK1/ubiquitin folded substrate Ser65 ATPgammaS aliases.",
    ),
    guarded.GuardedSurface(
        "limk1_cofilin_ser3_amp_pnp_gamma",
        "LIMK1 cofilin Ser3 AMP-PNP",
        "gamma",
        100,
        0,
        "Targets LIMK1/cofilin full-length substrate Ser3 source aliases.",
    ),
    guarded.GuardedSurface(
        "cdk7_cdk2_thr160_amp_pnp_gamma",
        "CDK7 CDK2 Thr160 AMP-PNP",
        "gamma",
        100,
        0,
        "Targets CAK/CDK activation-loop substrate site aliases.",
    ),
    guarded.GuardedSurface(
        "mtorc2_akt_ser473_atpgammas_gamma",
        "mTORC2 Akt Ser473 ATPgammaS",
        "gamma",
        100,
        0,
        "Targets mTORC2/Akt hydrophobic-motif source aliases.",
    ),
    guarded.GuardedSurface(
        "raf_mek_adp_metal_fluoride_transition",
        "RAF MEK ADP metal fluoride",
        "transition",
        100,
        0,
        "Targets RAF/MEK transition-analog wording.",
    ),
    guarded.GuardedSurface(
        "erk_rsk_adp_metal_fluoride_transition",
        "ERK RSK ADP metal fluoride",
        "transition",
        100,
        0,
        "Targets MAPK/RSK transition-analog wording.",
    ),
    guarded.GuardedSurface(
        "camkii_glun2b_ser1303_atp_magnesium_gamma",
        "CaMKII GluN2B Ser1303 ATP magnesium",
        "gamma",
        100,
        0,
        "Targets CaMKII/GluN2B site aliases while prior PDBs remain skipped.",
    ),
]


def build_artifact(
    out: Path,
    artifacts_dir: Path,
    max_unique_pdb_ids: int,
    max_cif_bytes: int,
    row_timeout_seconds: int,
    sleep_seconds: float,
    include_prior_seen: bool,
    ignore_prior_pdb_ids: list[str],
) -> dict[str, Any]:
    artifact = guarded.build_artifact(
        out,
        artifacts_dir,
        SURFACE_SET_NAME,
        SOURCE_SITE_ALIAS_SURFACES,
        max_unique_pdb_ids,
        max_cif_bytes,
        row_timeout_seconds,
        sleep_seconds,
        include_prior_seen,
        ignore_prior_pdb_ids,
    )
    artifact["metadata"]["method"] = "source_site_alias_candidate_rows"
    artifact["metadata"]["source_surface_intent"] = (
        "Named folded-substrate phosphosite aliases under exact canonical ePK "
        "ligand/metal filters, with prior lane PDB IDs skipped by default."
    )
    artifact["source_review_summary"]["recommendation"] = (
        "Source-adjudicate any fresh rows as review-only evidence. If none are fresh, "
        "keep these named site-alias surfaces exhausted until new PDB IDs appear."
    )
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=Path("artifacts/research_lanes/epk_positive_evidence"),
    )
    parser.add_argument("--max-unique-pdb-ids", type=int, default=60)
    parser.add_argument("--max-cif-bytes", type=int, default=25_000_000)
    parser.add_argument("--row-timeout-seconds", type=int, default=45)
    parser.add_argument("--sleep-seconds", type=float, default=0.03)
    parser.add_argument("--include-prior-seen", action="store_true")
    parser.add_argument("--ignore-prior-pdb-id", action="append", default=[])
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(
        args.out,
        args.artifacts_dir,
        args.max_unique_pdb_ids,
        args.max_cif_bytes,
        args.row_timeout_seconds,
        args.sleep_seconds,
        args.include_prior_seen,
        args.ignore_prior_pdb_id,
    )
    print(
        json.dumps(
            {
                "out": str(args.out),
                "unique_pdb_ids_reviewed": artifact["metadata"]["unique_pdb_ids_reviewed"],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
                "candidate_evidence_rows_emitted": artifact["metadata"][
                    "candidate_evidence_rows_emitted"
                ],
                "fresh_candidate_evidence_rows_emitted": artifact["metadata"][
                    "fresh_candidate_evidence_rows_emitted"
                ],
                "coordinate_state_counts": artifact["metadata"]["coordinate_state_counts"],
                "skipped_prior_seen_pdb_id_count": artifact["metadata"][
                    "skipped_prior_seen_pdb_id_count"
                ],
                "primary_outcome": artifact["source_review_summary"]["primary_outcome"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
