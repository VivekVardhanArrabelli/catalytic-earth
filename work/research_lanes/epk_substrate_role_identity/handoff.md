# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T15:15:23-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.48 minutes (`2026-05-21T19:26:54Z` to
`2026-05-21T20:15:23Z`).

Run note: disk free space was 30 GiB, above the 10 GiB stop threshold. Normal
`git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. The local worktree still appears stale
and dirty relative to `origin/research/epk-substrate-role-identity`; use the
remote-tip temporary-index commit/push workaround if normal git metadata
operations remain blocked. Local `HEAD` equality and clean-branch verification
are not possible unless the linked-worktree metadata can be fast-forwarded.

## What Was Emitted

This run added one bounded source-free coordinate modality: acceptor backbone
continuity. The helper fetches model-1 coordinates in memory, emits compact
reduced evidence, and writes no raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_acceptor_backbone_continuity_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/acceptor_backbone_continuity_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json`

The helper reused 211 candidate/state rows, 54 PDB-level conflict rows, and 135
phosphoproduct materialization rows. It scanned 54 diagnostic PDBs in memory and
emitted 220 compact backbone-continuity rows:

- candidate gamma/acceptor pair rows: 204
- state-only rows: 16
- nonterminal phosphoproduct state rows re-emitted: 9
- source-free backbone signature rows: 23
- mixed positive/counterexample backbone signatures: 2

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

Backbone continuity classes:

- `internal_backbone_continuous=206`
- `state_or_candidate_without_acceptor_atom=11`
- `backbone_break_or_missing_atom_context=2`
- `resolved_n_terminal_backbone_boundary=1`

Backbone materiality classes:

- `same_chain_internal_continuous_backbone=162`
- `cross_chain_folded_internal_continuous_backbone=23`
- `reciprocal_folded_internal_continuous_backbone=10`
- `cross_chain_internal_fragment_continuous_backbone=6`
- `adp_state_backbone_context_review_only=5`
- `ligand_absent_no_active_gamma_backbone_context=4`
- `product_state_backbone_context_review_only=4`
- `chain_break_or_missing_backbone_context=2`
- `ambiguous_coordinate_state_no_active_gamma_backbone_context=1`
- `internal_fragment_n_boundary_backbone=1`
- `split_state_backbone_context_review_only=1`
- `state_or_candidate_without_acceptor_atom=1`

Blocker classes:

- `topology_ambiguity=174`
- `none=19`
- `product_state_evidence=9`
- `active_gamma_geometry=7`
- `ligand_materialization=5`
- `substrate_role_identity=4`
- `internal_fragment_mimicry=1`
- `split_state_evidence=1`

The no-promotion conflict projection remains unchanged:

- TP=14
- FP=0
- TN=8
- FN=0
- Abstained positives=6
- Abstained negatives=26

## Decisive Result

The blocker is not cleared source-free.

Acceptor backbone continuity is useful review-routing evidence but does not
adjudicate biological substrate-role identity. The decisive mixed signatures
are:

- `2c6cf40812f1`: same-chain internal continuous backbone, 149 candidates
  across 44 PDBs, with 33 review-positive rows and 116 counterexample rows. It
  includes hard cases `3TM0`, `7B56`, `9UUR`, `9UUX`, and `9UW4`.
- `e705e11d14c1`: reciprocal folded Tyr internal continuous backbone shared by
  `9UUR|gamma=A:ANP501:PG|acceptor=B:TYR204:OH`,
  `9UUX|gamma=A:ANP501:PG|acceptor=B:TYR204:OH`, and counterexample
  `9UW4|gamma=A:ANP501:PG|acceptor=B:TYR204:OH`.

State-specific hard cases remain unchanged:

- `1L0O` remains ADP-only product-state review evidence.
- `3QHR` and `3QHW` materialize product-state phosphoacceptor backbone rows,
  but product chemistry is review-only biological context.
- `4HPU` materializes a split-state phosphoacceptor backbone row, which remains
  counterpressure against promoting product/split chemistry.
- `7B56` is now explicitly represented as an
  `internal_fragment_n_boundary_backbone` row and remains blocked by
  `internal_fragment_mimicry`.

## Interpretation

The useful refinement is narrow: coordinates can show whether an acceptor is an
internal continuous backbone residue, a resolved boundary, or a chain-break
context. That helps review triage for internal-fragment and state-specific rows,
but the internal continuous-backbone signature is broad and mixed across true
substrate candidates and counterexamples.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Verification

- `python -m py_compile` passed for the new helper.
- `python -m json.tool` passed for the new artifact.
- Full lane JSON validation passed for 23 JSON files.
- Full run-log JSONL validation passed; final line has
  `primary_outcome=candidate_evidence_rows_emitted` and
  `measured_minutes=48.48`.
- Required run-record field validation passed.
- `git diff --check` passed.
- No raw `.pdb`, `.cif`, or `.mmcif` files were written in the lane paths.
- No production label registries, mechanism fingerprints, migration manifests,
  or label imports were touched.

## Exact Next Experiment

Stop backbone-continuity probing as a promotion route. Only resume this lane for
a genuinely different source-free modality that can adjudicate ADP/product,
substrate-analog, reciprocal folded-chain, or same-chain biology without
review-context leakage. Otherwise preserve source-reviewed adjudication for
product/ADP, split-state, substrate-analog, reciprocal folded-chain, and
same-chain substrate biology.
