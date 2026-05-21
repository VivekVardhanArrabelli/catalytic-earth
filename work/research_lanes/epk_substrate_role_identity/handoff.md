# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T23:32:34-0500

Primary outcome: `blocker_not_cleared_biology_ambiguity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.23 minutes (`2026-05-21T03:43:58Z` to
`2026-05-21T04:32:12Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Local `HEAD` remains stale relative
to `origin/research/epk-substrate-role-identity`; final commits should keep
using the lane temporary-index workaround.

Final sync: pushed blocker-audit commit
`bd7e225950550b7521a0576f5180d78dc787677c` to
`origin/research/epk-substrate-role-identity`. Final verification used
`git fetch --no-write-fetch-head origin` and
`git rev-parse origin/research/epk-substrate-role-identity`; local `HEAD`
remains `8d38053d85cc28b7592267e9420578ca19a98814`, so normal `git status`
still reports this linked worktree as behind with lane-file changes.

## What Was Emitted

This run added a compact blocker audit on top of the existing candidate
evidence table. It did not add another scalar source-free substrate identity
proxy.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_blocker_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_blocker_audit.py`

Input artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`

The helper reused:

- 204 gamma/acceptor candidate-pair rows.
- 7 state-only rows.
- 54 diagnostic PDBs.

It emitted 54 PDB-level triage rows with:

- coordinate-state counts,
- blocker-class counts,
- source-free state x blocker matrices,
- unblocked-candidate sanity flags,
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

PDB-level triage buckets:

- `topology_review_required=29`
- `unblocked_structural_candidate_present=14`
- `active_gamma_geometry_blocked=3`
- `coordinate_materialization_review=3`
- `state_specific_product_or_adp_review=3`
- `active_gamma_no_near_hydroxyl_review=1`
- `internal_fragment_mimicry_blocked=1`

The PDB-level unblocked-candidate sanity flag was:

- TP=14
- FP=0
- TN=34
- FN=6

False negatives are the known review-required classes:

- product/ADP state rows: `3QHR`, `3QHW`, `1L0O`
- reciprocal folded-chain rows: `9UUR`, `9UUX`
- same-chain/autophosphorylation-like row: `3TM0`

Hard-case interpretation:

- `7B56`: `internal_fragment_mimicry_blocked`
- `9UUR`, `9UUX`, `9UW4`: `topology_review_required`
- `3QHR`, `3QHW`, `1L0O`: `state_specific_product_or_adp_review`
- `3TM0`: `topology_review_required`
- `1QHA`: `active_gamma_no_near_hydroxyl_review`

## Interpretation

The blocker is not cleared source-free. Candidate evidence is now useful for
review routing, but structure-only evidence still cannot assign biological
substrate role for product/ADP, reciprocal folded-chain, or same-chain/
autophosphorylation-like cases without source-reviewed adjudication.

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or promote the unblocked-candidate sanity
flag into a production identity rule.

## Exact Next Experiment

Use `epk_candidate_blocker_audit_v1_20260521.json` for review triage and
blocker reporting. Stop source-free scalar probing unless a genuinely new
evidence modality becomes available. Preserve product/ADP, reciprocal
folded-chain, and same-chain/autophosphorylation-like cases as source-reviewed
adjudication requirements.
