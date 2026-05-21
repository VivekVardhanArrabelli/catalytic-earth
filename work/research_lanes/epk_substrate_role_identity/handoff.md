# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T00:34:34-0500

Primary outcome: `blocker_not_cleared_biology_ambiguity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 49.08 minutes (`2026-05-21T04:45:29Z` to
`2026-05-21T05:34:34Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Local `HEAD` remains stale relative
to `origin/research/epk-substrate-role-identity`; final commit/push work should
use the lane temporary-index workaround.

## What Was Emitted

This run added a compact candidate-conflict decision artifact on top of the
existing candidate evidence table. It did not add a scalar source-free rescue
threshold and did not promote any review-only class to production identity.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_conflict_decision.py`

Input artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`

The helper reused:

- 204 gamma/acceptor candidate-pair rows.
- 7 state-only rows.
- 54 diagnostic PDBs.

It emitted 54 PDB-level candidate-conflict rows with:

- source-free conflict signatures from coordinate states, blockers, and
  candidate role classes,
- state-by-blocker and role-by-blocker matrices,
- nearest candidate, nearest unblocked candidate, and nearest topology
  candidate digests,
- abstention decision classes for topology and state-specific biology,
- hard-case digests for `7B56`, `9UUR`, `9UUX`, `9UW4`, `3QHR`, `3QHW`,
  `1L0O`, `3TM0`, and `1QHA`.

Review labels remain only under `review_context_for_evaluation_only`.
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

Conflict classes across 54 PDB-level rows:

- `topology_conflict_same_chain=26`
- `unblocked_support_low_conflict=7`
- `unblocked_support_with_competing_ambiguous_candidates=7`
- `active_gamma_geometry_conflict=3`
- `coordinate_materialization_conflict=3`
- `state_specific_product_or_adp_conflict=3`
- `topology_conflict_reciprocal_and_same_chain=3`
- `active_gamma_no_near_hydroxyl_conflict=1`
- `internal_fragment_mimicry_conflict=1`

Decision classes:

- `source_free_structural_support_review_only=14`
- `source_free_blocked_counterevidence_review_only=8`
- `abstain_biology_topology_review_required=29`
- `abstain_state_specific_review_required=3`

The review-only abstention routing matrix was:

- TP=14
- FP=0
- TN=8
- FN=0
- abstained positives=6
- abstained negatives=26

Abstained positive hard cases are the known review-required classes:

- product/ADP state rows: `3QHR`, `3QHW`, `1L0O`
- reciprocal folded-chain rows: `9UUR`, `9UUX`
- same-chain/autophosphorylation-like row: `3TM0`

Hard-case interpretation:

- `7B56`: `internal_fragment_mimicry_conflict`, blocked review-only
  counterevidence.
- `9UUR`, `9UUX`, `9UW4`: shared
  `topology_conflict_reciprocal_and_same_chain`, therefore source-free
  abstention.
- `3QHR`, `3QHW`, `1L0O`: `state_specific_product_or_adp_conflict`, therefore
  source-free abstention.
- `3TM0`: `topology_conflict_same_chain`, therefore source-free abstention.
- `1QHA`: `active_gamma_no_near_hydroxyl_conflict`, blocked review-only
  counterevidence.

## Interpretation

The blocker is not cleared source-free. Candidate conflict routing can separate
22 non-abstaining review-only cases without diagnostic false positives or false
negatives, but it must abstain on 32 PDBs. The abstention set includes all
product/ADP positives and the reciprocal/same-chain topology positives, and it
also includes the decisive topology counterexample `9UW4`.

This supports review routing, not production substrate-role identity. Do not
claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or promote the conflict decision classes
into production identity labels.

## Exact Next Experiment

Use `epk_candidate_conflict_decision_v1_20260521.json` for review routing and
blocker reporting. Stop source-free substrate-role identity probing unless a
genuinely new evidence modality can reduce the topology/state abstention set
without admitting `9UW4`-like counterexamples.
