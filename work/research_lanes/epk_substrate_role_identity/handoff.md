# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T11:11:00-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 49.07 minutes (`2026-05-21T15:21:56Z` to
`2026-05-21T16:11:00Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Normal local `HEAD` remains stale
relative to `origin/research/epk-substrate-role-identity`; commit/push should
continue using the remote-tip temporary-index workaround.

## What Was Emitted

This run added one compact source-free coordinate-state feature family:
candidate coordinate-state taxonomy with an in-memory coordinate chemistry
scan. The helper fetches diagnostic structures in memory, writes only reduced
evidence, and does not write raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_coordinate_state_taxonomy_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_coordinate_state_taxonomy.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_gamma_metal_transfer_geometry_probe_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`

The helper reused 204 candidate-pair rows, 7 state-only rows, and 54 PDB-level
conflict rows. It emitted 211 candidate coordinate-state taxonomy rows and
scanned all 54 diagnostic PDBs for compact coordinate chemistry evidence:
terminal-gamma atoms, ADP, and phosphorylated SER/THR/TYR residue
materialization.

No source text, titles, UniProt prose, EC/Rhea, mechanism labels, curated
substrate names, post-hoc source repair, candidate-specific threshold tuning,
production labels, registries, fingerprints, or migration manifests were used
or changed.

## Evidence Summary

Coordinate states after the metal overlay and coordinate chemistry scan:

- `active_gamma=187`
- `metal_absent=18`
- `adp_state=3`
- `ligand_absent=2`
- `ambiguous_coordinate_state=1`

Source-free coordinate chemistry classes:

- `active_gamma_materialized_by_terminal_gamma_atom=205`
- `adp_with_distant_phosphorylated_sty_product_not_materialized=2`
- `adp_without_phosphorylated_sty_product_not_materialized=1`
- `ambiguous_nucleotide_without_terminal_gamma_product_not_materialized=1`
- `ligand_absent_product_not_materialized=2`

The target coordinate states not materialized source-free remain:

- `product_state`
- `substrate_acceptor_analog_state`
- `split_state`
- `unavailable_coordinate_state`

Source-leakage guard:

- 207 rows had no product/analog review-state context.
- 3 product-context rows were not source-free `product_state`:
  `1L0O`, `3QHR`, `3QHW`.
- 1 analog-context row was not source-free `substrate_acceptor_analog_state`:
  `3TM0`.
- The guarded candidate IDs are:
  `1L0O|gamma=none|acceptor=none`,
  `3QHR|gamma=none|acceptor=none`,
  `3QHW|gamma=none|acceptor=none`, and
  `3TM0|gamma=A:ANP300:PG|acceptor=A:SER27:OG`.

The reused conservative conflict projection remains review-only and abstaining:

- TP=14
- FP=0
- TN=8
- FN=0
- Abstained positives=6
- Abstained negatives=26

## Decisive Result

The blocker is not cleared source-free.

The direct coordinate chemistry scan did not independently materialize
`product_state`, `substrate_acceptor_analog_state`, or `split_state` for the
review product/analog hard cases. Promoting those states would require review
context leakage, which remains forbidden.

Hard state cases:

- `1L0O`, `3QHR`, and `3QHW` remain source-free `adp_state` with
  `product_state_evidence` blockers.
- `3TM0` remains source-free `active_gamma` with same-chain
  `topology_ambiguity`; its ligand-analog review context is not a source-free
  substrate-analog coordinate state.

Hard topology cases also persist:

- `9UUR`, `9UUX`, and `9UW4` remain a reciprocal folded-chain topology blocker.
- `3TM0` and `6NOO` remain a same-chain topology ambiguity pair under the
  existing conflict projection.

## Interpretation

Coordinate-state taxonomy is useful review-routing evidence. It makes the state
gap explicit and prevents product/analog review labels from becoming predictive
source-free inputs. It does not assign biological substrate role source-free,
and it does not support production substrate-role identity.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Exact Next Experiment

Do not add scalar rescues. If this lane resumes, require a new source-free
coordinate modality that directly materializes product/analog chemistry without
review-context leakage; otherwise preserve source-reviewed adjudication for
product/ADP, reciprocal folded-chain, and same-chain substrate biology.
