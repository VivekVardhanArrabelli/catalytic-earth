#!/usr/bin/env python3
"""Guarded non-peptide phosphosite candidate-row search.

This lane-local wrapper targets source-rich wording for folded or full-length
protein substrates with mapped phosphoacceptor context, while reusing the
candidate-level row emitter from guarded_phrase_candidate_rows.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import guarded_phrase_candidate_rows as guarded


SURFACE_SET_NAME = "nonpeptide_phosphosite_source_terms"

NONPEPTIDE_PHOSPHOSITE_SURFACES = [
    guarded.GuardedSurface(
        "full_length_substrate_phosphorylation_site_amp_pnp_gamma",
        "full-length substrate phosphorylation site AMP-PNP",
        "gamma",
        100,
        0,
        "Targets source wording that explicitly joins full-length substrate, site mapping, and AMP-PNP.",
    ),
    guarded.GuardedSurface(
        "full_length_substrate_phosphorylation_site_atpgammas_gamma",
        "full-length substrate phosphorylation site ATPgammaS",
        "gamma",
        100,
        0,
        "Targets ATPgammaS full-length substrate site wording under exact active-gamma filters.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_full_length_substrate_phosphoacceptor_amp_pnp_gamma",
        "protein kinase full-length substrate phosphoacceptor AMP-PNP",
        "gamma",
        100,
        0,
        "Targets explicit phosphoacceptor wording for non-peptide substrate complexes.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_full_length_substrate_phosphoacceptor_atpgammas_gamma",
        "protein kinase full-length substrate phosphoacceptor ATPgammaS",
        "gamma",
        100,
        0,
        "Targets explicit ATPgammaS phosphoacceptor wording for full-length substrates.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_protein_substrate_phosphorylation_site_amp_pnp_gamma",
        "protein kinase protein substrate phosphorylation site AMP-PNP",
        "gamma",
        100,
        0,
        "Targets folded-protein substrate phosphorylation-site wording with AMP-PNP.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_protein_substrate_phosphorylation_site_atpgammas_gamma",
        "protein kinase protein substrate phosphorylation site ATPgammaS",
        "gamma",
        100,
        0,
        "Targets folded-protein substrate phosphorylation-site wording with ATPgammaS.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_nonpeptide_substrate_amp_pnp_magnesium_gamma",
        "protein kinase non-peptide substrate AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets explicit non-peptide substrate wording with local-metal active-gamma context.",
    ),
    guarded.GuardedSurface(
        "kinase_substrate_protein_phosphoacceptor_atpgammas_gamma",
        "kinase substrate protein phosphoacceptor ATPgammaS",
        "gamma",
        100,
        0,
        "Targets broad source wording for protein phosphoacceptor plus ATPgammaS.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_folded_substrate_amp_pnp_magnesium_gamma",
        "protein kinase folded substrate AMP-PNP magnesium",
        "gamma",
        100,
        0,
        "Targets articles that describe folded-substrate states directly.",
    ),
    guarded.GuardedSurface(
        "protein_kinase_full_length_substrate_adp_metal_fluoride_transition",
        "protein kinase full-length substrate ADP metal fluoride",
        "transition",
        100,
        0,
        "Targets transition-analog wording for full-length substrates.",
    ),
    guarded.GuardedSurface(
        "kinase_protein_substrate_transition_state_adp_metal_fluoride_transition",
        "kinase protein substrate transition state ADP metal fluoride",
        "transition",
        100,
        0,
        "Targets transition-state source wording for folded-protein substrates.",
    ),
    guarded.GuardedSurface(
        "tyrosine_kinase_protein_substrate_phosphoacceptor_amp_pnp_gamma",
        "tyrosine kinase protein substrate phosphoacceptor AMP-PNP",
        "gamma",
        100,
        0,
        "Targets tyrosine-kinase folded-protein substrate phosphoacceptor wording.",
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
        NONPEPTIDE_PHOSPHOSITE_SURFACES,
        max_unique_pdb_ids,
        max_cif_bytes,
        row_timeout_seconds,
        sleep_seconds,
        include_prior_seen,
        ignore_prior_pdb_ids,
    )
    artifact["metadata"]["method"] = "nonpeptide_phosphosite_candidate_rows"
    artifact["metadata"]["source_surface_intent"] = (
        "Source-rich non-peptide/full-length substrate phosphoacceptor wording "
        "under exact canonical ePK ligand/metal filters."
    )
    artifact["source_review_summary"]["recommendation"] = (
        "Source-adjudicate any fresh rows as review-only evidence. If none are fresh, "
        "treat this non-peptide phosphosite wording surface as exhausted until a new "
        "RCSB release or publication metadata appears."
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
    parser.add_argument("--max-unique-pdb-ids", type=int, default=80)
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
