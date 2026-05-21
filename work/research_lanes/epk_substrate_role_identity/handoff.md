# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T07:29:20-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 401.87 minutes (`2026-05-21T05:47:28Z` to
`2026-05-21T12:29:20Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Local `HEAD` remains stale relative
to `origin/research/epk-substrate-role-identity`; commit/push work used the
lane temporary-index workaround.

Final sync: pushed materiality artifact commit
`afdba337dc3bf2a369c8954fec4e627d4e8c5609` to
`origin/research/epk-substrate-role-identity`, then pushed handoff-only sync
commit(s) on top. `git fetch --no-write-fetch-head origin` verified the remote
branch could be refreshed without writing `FETCH_HEAD`. Normal `git status`
still reports this linked worktree as behind with lane-file changes because
local `HEAD` remains `8d38053d85cc28b7592267e9420578ca19a98814`.

## What Was Emitted

This run added a candidate-level materiality manifest on top of the existing
source-free candidate evidence and PDB-level conflict decision artifacts. It
does not introduce a scalar rescue threshold, does not use source/review text
as a predictive input, and does not promote any review-only class to production
identity.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_materiality_manifest_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_materiality_manifest.py`

Input artifacts:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`

The helper emitted 211 compact materiality rows:

- 204 reused gamma/acceptor candidate-pair rows.
- 7 reused state-only rows.
- 54 diagnostic PDBs covered through inherited conflict decisions.

Each materiality row keeps source-free evidence separate from
`review_context_for_evaluation_only` and includes:

- candidate ID with PDB, gamma ligand/atom, and acceptor residue/atom,
- first-class coordinate state,
- blocker class,
- candidate materiality class and reason,
- compact distance/topology/reciprocal/exposure/orientation/certainty evidence,
- inherited PDB conflict class and review-only abstention decision.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence Summary

Coordinate states across reused candidate/state rows:

- `active_gamma=205`
- `adp_state=3`
- `ambiguous_coordinate_state=1`
- `ligand_absent=2`

Blocker classes across reused candidate/state rows:

- `topology_ambiguity=109`
- `active_gamma_geometry=72`
- `none=19`
- `substrate_role_identity=4`
- `product_state_evidence=3`
- `ligand_materialization=3`
- `internal_fragment_mimicry=1`

Candidate materiality classes:

- `material_topology_abstention_driver=98`
- `secondary_geometry_within_topology_abstention=42`
- `competing_blocked_candidate_nonfatal=20`
- `material_unblocked_structural_support=19`
- `competing_ambiguous_candidate_nonfatal=11`
- `material_active_gamma_geometry_counterevidence=10`
- `material_substrate_role_abstention_driver=4`
- `material_coordinate_materialization_driver=3`
- `material_state_abstention_driver=3`
- `material_internal_fragment_counterevidence=1`

The inherited review-only abstention routing matrix remains:

- TP=14
- FP=0
- TN=8
- FN=0
- abstained positives=6
- abstained negatives=26

Abstained positive hard cases remain the known review-required classes:

- product/ADP state rows: `3QHR`, `3QHW`, `1L0O`
- reciprocal folded-chain rows: `9UUR`, `9UUX`
- same-chain/autophosphorylation-like row: `3TM0`

Hard-case interpretation:

- `7B56`: internal-fragment mimicry plus active-gamma geometry
  counterevidence; review-only blocked counterevidence.
- `9UUR`, `9UUX`, `9UW4`: shared topology-abstention materiality, so the
  source-free evidence still cannot separate true reciprocal folded-chain
  positives from the decisive topology counterexample.
- `3QHR`, `3QHW`, `1L0O`: material state-abstention rows; terminal-gamma
  transfer geometry is unavailable.
- `3TM0`: same-chain topology-abstention row.
- `1QHA`: active-gamma geometry counterevidence row.

## Interpretation

The new manifest makes row-level evidence materiality explicit, but it does
not clear the source-free substrate-role blocker. It preserves the prior safe
behavior: source-free rows can route review support or hard counterevidence,
but product/ADP, reciprocal folded-chain, same-chain, and folded-role substrate
biology still require abstention or source-reviewed adjudication.

No production readiness claim is allowed. Do not import labels, edit production
fingerprints, calibrate thresholds, or promote candidate materiality classes
into production substrate-role identity.

## Exact Next Experiment

Use `epk_candidate_materiality_manifest_v1_20260521.json` for review routing
and blocker reporting. Stop source-free substrate-role identity probing unless
a genuinely new evidence modality can reduce the topology/state abstention set
without admitting `9UW4`-like counterexamples.
