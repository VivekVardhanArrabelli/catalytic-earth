# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T10:09:47-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.35 minutes (`2026-05-21T14:21:26Z` to
`2026-05-21T15:09:47Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Normal local `HEAD` remains stale
relative to `origin/research/epk-substrate-role-identity`; commit/push should
use the remote-tip temporary-index workaround.

## What Was Emitted

This run added one compact, non-scalar source-free feature family: gamma-site
and PDB candidate graph motifs. It reuses the existing candidate evidence table
plus the metal/transfer-geometry overlay and emits graph rows only; it does not
fetch coordinates or write raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_graph_motif_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_graph_motif_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_gamma_metal_transfer_geometry_probe_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`

The helper reused 204 candidate-pair rows, 7 state-only rows, and 54 diagnostic
PDB conflict rows. It emitted:

- 98 gamma-site graph motif rows.
- 7 state-materialization graph rows.
- 54 PDB graph motif rows.
- 37 gamma-site graph motif groups.
- 4 state-materialization graph groups.
- 42 PDB graph motif groups.

No source text, titles, UniProt prose, EC/Rhea, mechanism labels, curated
substrate names, post-hoc source repair, candidate-specific threshold tuning,
production labels, registries, fingerprints, or migration manifests were used
or changed.

## Evidence Summary

Coordinate states after the metal overlay:

- `active_gamma=187`
- `metal_absent=18`
- `adp_state=3`
- `ligand_absent=2`
- `ambiguous_coordinate_state=1`

Blocker class counts after graph-row projection:

- `topology_ambiguity=103`
- `active_gamma_geometry=79`
- `none=18`
- `substrate_role_identity=4`
- `ligand_materialization=3`
- `product_state_evidence=3`
- `internal_fragment_mimicry=1`

Graph collision summary:

- 3 mixed positive/counterexample gamma-site graph motif groups covering 13
  PDBs.
- Mixed gamma-site motif blockers are `active_gamma_geometry=1` and
  `topology_ambiguity=2`.
- 2 mixed positive/counterexample PDB graph motif groups covering 5 PDBs.

The reused conservative conflict projection remains review-only and abstaining:

- TP=14
- FP=0
- TN=8
- FN=0
- Abstained positives=6
- Abstained negatives=26

## Decisive Result

The graph motif audit does not clear substrate-role identity source-free.

The reciprocal Tyr hard trio remains inseparable by graph motif:

- PDB graph signature `7deae36bdf7b`: `9UUR`, `9UUX`, `9UW4`
  - review-only labels: 2 positives, 1 counterexample
- Gamma-site graph signature `26659cc98a93`: `9UUR`, `9UUX`, `9UW4`
  - review-only labels: 2 positives, 1 counterexample

The same-chain topology shape also remains unsafe:

- PDB graph signature `7d3244390445`: `3TM0`, `6NOO`
  - review-only labels: 1 positive, 1 counterexample
- Gamma-site graph signature `dc7e7db20443`: `2JJ2`, `3TM0`, `5C1O`,
  `6NOO`, `7T55`, `8W2J`, `9L3M`, `9L3U`, `9NBW`
  - review-only labels: 1 positive, 31 counterexample candidate rows

The graph motif feature reduces uncertainty by localizing ambiguity to
candidate graph structures, but it does not assign biological substrate role.
Mixed topology and metal-absent reciprocal motifs remain review blockers.

## Interpretation

The blocker is not cleared source-free. Candidate graph motifs are useful
review-routing evidence and make coordinate states first-class after metal
overlay, but graph topology still collides between positives and counterexamples.
Product/ADP rows remain state-specific review-only evidence, reciprocal
folded-chain Tyr rows remain biology ambiguity, and same-chain graph motifs
remain unsafe because they admit counterexamples.

This is review-routing/blocker evidence only. It is not a production
substrate-role identity rule and does not support ePK production readiness.

## Exact Next Experiment

Do not run another scalar source-free rescue on this tranche. If this lane
resumes, require a genuinely new source-free evidence modality beyond candidate
graph topology, metal materialization, coordinate certainty, exposure,
orientation, and sequence context. Otherwise preserve the source-reviewed
adjudication requirement for topology and product-state substrate biology.
