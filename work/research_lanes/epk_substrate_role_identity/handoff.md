# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T14:18:37-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 52.97 minutes (`2026-05-21T18:25:26Z` to
`2026-05-21T19:18:24Z`).

Run note: disk free space was 29 GiB, above the 10 GiB stop threshold. Normal
`git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Local `HEAD` still appears stale and
dirty relative to `origin/research/epk-substrate-role-identity`; continue using
the remote-tip temporary-index commit/push workaround if normal git metadata
operations remain blocked.

## What Was Emitted

This run added one bounded source-free coordinate modality: reciprocal
active-site competition plus ligand-chain ordinal/auth counterpart context. The
helper fetches model-1 coordinates in memory, emits compact reduced evidence,
and writes no raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_reciprocal_active_site_competition_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/reciprocal_active_site_competition_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json`

The helper reused 211 candidate/state rows, 54 PDB-level conflict rows, and 135
phosphoproduct materialization rows. It scanned 54 diagnostic PDBs in memory and
emitted 220 compact competition rows:

- candidate gamma/acceptor pair rows: 204
- state-only rows: 16
- reciprocal folded candidate rows: 10
- competition signature rows: 58
- mixed competition signature rows: 9
- reciprocal-only signature rows: 8
- mixed reciprocal-only signature rows: 0

No PDB titles, UniProt prose, EC/Rhea, paper/source text, mechanism labels,
curated substrate names, post-hoc source repair, candidate-specific threshold
tuning, production labels, registries, fingerprints, migration manifests, or
raw coordinate dumps were used or changed.

## Evidence Summary

Coordinate states observed:

- `active_gamma=205`
- `adp_state=5`
- `ambiguous_coordinate_state=1`
- `ligand_absent=4`
- `product_state=4`
- `split_state=1`

Reciprocal competition classes:

- `not_reciprocal_folded_candidate=195`
- `no_same_chain_competitor_within_preexisting_6a_shell=2`
- `reciprocal_closer_than_same_chain_competitor=4`
- `reciprocal_same_chain_distance_tie_at_0_001a=1`
- `same_chain_competitor_closer_than_reciprocal=3`
- state/not-applicable rows: 15

Ligand-chain ordinal counterpart classes:

- `counterpart_ser_thr_hydroxyl=153`
- `counterpart_not_sty_hydroxyl=38`
- `counterpart_tyr_hydroxyl=13`
- `counterpart_not_applicable=16`

Blocker classes:

- `topology_ambiguity=174`
- `none=19`
- `product_state_evidence=9`
- `active_gamma_geometry=7`
- `ligand_materialization=5`
- `substrate_role_identity=4`
- `split_state_evidence=1`
- `internal_fragment_mimicry=1`

The no-promotion conflict projection remains unchanged:

- TP=14
- FP=0
- TN=8
- FN=0
- Abstained positives=6
- Abstained negatives=26

## Decisive Result

The blocker is not cleared source-free.

Reciprocal competition is useful review-routing evidence. It separates the hard
reciprocal Tyr rows in this tranche:

- `9UUR|gamma=A:ANP501:PG|acceptor=B:TYR204:OH` and
  `9UUX|gamma=A:ANP501:PG|acceptor=B:TYR204:OH` share a positive-only
  reciprocal competition signature with no same-chain competitor within the
  preexisting 6A shell.
- `9UW4|gamma=A:ANP501:PG|acceptor=B:TYR204:OH` is separated by a same-gamma
  same-chain competitor tie against `A:SER194:OG`.

That split is not a source-free production rule. Promoting the isolated
reciprocal Tyr signature would be a narrow post-hoc distance/order rescue and
would not address product/ADP, same-chain, or analog-state biology. Across the
full competition audit, nine broader signatures still mix positives and
counterexamples, especially same-chain rows. The decisive same-chain mixed
signature `d7bf11628a44` is shared by `3TM0`, `9UUR`, `9UUX`, `9UW4`, and many
counterexamples.

State-specific hard cases remain unchanged:

- `1L0O` remains ADP-only product-state review evidence.
- `3QHR` and `3QHW` remain source-free `product_state` chemistry rows, but
  product chemistry is review-only biological context.
- `4HPU` remains split-state counterpressure against promoting product/split
  chemistry into positive substrate-role calls.
- `7B56` remains blocked by internal-fragment mimicry.

## Interpretation

The useful refinement is narrow: source-free coordinates can show whether a
reciprocal folded acceptor is isolated at its gamma site or tied with same-chain
competition, and can record simple ligand-chain ordinal/auth counterparts. This
reduces review uncertainty for the 9UUR/9UUX/9UW4 trio, but it is not general
biological substrate-role identity.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Verification

- `python -m json.tool` passed for the new artifact.
- Full run-log JSONL validation passed; final line has
  `primary_outcome=candidate_evidence_rows_emitted` and
  `measured_minutes=52.97`.
- Required run-record field validation passed.
- `python -m py_compile` passed for the new helper.
- `git diff --check` passed.
- No raw `.pdb`, `.cif`, or `.mmcif` files were written in the lane paths.
- No production label registries, mechanism fingerprints, migration manifests,
  or label imports were touched.

## Exact Next Experiment

Do not add reciprocal distance/order rescue rules. Only resume this lane for a
genuinely different source-free modality that can adjudicate state-specific or
reciprocal folded-chain biology without review-context leakage. Otherwise
preserve source-reviewed adjudication for product/ADP, split-state,
substrate-analog, reciprocal folded-chain, and same-chain substrate biology.
