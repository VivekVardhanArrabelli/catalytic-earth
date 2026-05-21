# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T16:17:13-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.77 minutes (`2026-05-21T20:28:27Z` to
`2026-05-21T21:17:13Z`).

Run note: disk free space was 29 GiB, above the 10 GiB stop threshold. Normal
`git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. A direct `git merge --ff-only
origin/research/epk-substrate-role-identity` then failed on linked-worktree
`ORIG_HEAD.lock` permissions. Preserve outputs and use the remote-tip
temporary-index commit/push workaround if normal metadata writes remain blocked.
Remote-tip temporary-index pushes succeeded during wrap. Local `HEAD` remains
stale at `8d38053d85cc28b7592267e9420578ca19a98814` while
`origin/research/epk-substrate-role-identity` advanced; normal local clean and
HEAD-equals-origin verification remain blocked until the linked-worktree
metadata can be fast-forwarded.

## What Was Emitted

This run added one bounded source-free coordinate modality: ordered solvent
bridging around gamma/acceptor pairs. The helper fetches model-1 coordinates in
memory, emits compact reduced evidence, and writes no raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_ordered_solvent_bridge_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/ordered_solvent_bridge_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json`

The helper reused 211 candidate/state rows, 54 PDB-level conflict rows, and 135
phosphoproduct materialization rows. It scanned 54 diagnostic PDBs in memory and
emitted 220 compact ordered-solvent rows:

- candidate gamma/acceptor pair rows: 204
- state-only rows: 16
- nonterminal phosphoproduct state rows re-emitted: 9
- source-free ordered-solvent signature rows: 63
- mixed positive/counterexample solvent signatures: 7
- ordered gamma/acceptor water-bridge candidate rows: 8

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

Ordered-solvent bridge classes:

- `no_ordered_water_within_3p5a=144`
- `acceptor_solvated_only=21`
- `separate_ordered_waters_near_gamma_and_acceptor=19`
- `gamma_solvated_only=12`
- `ordered_water_bridge_between_gamma_and_acceptor=8`
- `gamma_or_acceptor_atom_not_resolved=1`
- state-not-applicable rows: `adp_state=5`, `ambiguous_coordinate_state=1`,
  `ligand_absent=4`, `product_state=4`, `split_state=1`

Blocker classes:

- `topology_ambiguity=109`
- `active_gamma_geometry=71`
- `none=19`
- `product_state_evidence=9`
- `ligand_materialization=6`
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

Ordered solvent is useful review-routing evidence because it distinguishes
water bridge, separate solvation, acceptor-only solvation, gamma-only solvation,
and no ordered-water contact around candidate pairs. It still does not
adjudicate biological substrate-role identity without review context. The
signature audit found 7 mixed positive/counterexample ordered-solvent
signatures.

State-specific hard cases remain unchanged:

- `1L0O`, `3QHR`, and `3QHW` remain ADP/product-state review evidence.
- `4HPU` remains split-state review counterpressure.
- `3TM0`, `9UUR`, and `9UUX` remain positive abstentions.
- `7B56` and `9UW4` remain decisive counterexample pressure.

## Interpretation

The useful refinement is narrow: ordered solvent materialization can tell a
reviewer whether water is present between or around a gamma/acceptor pair.
Mixed signature collisions show it is not substrate-role identity. Promoting a
solvent signature would either be a post-hoc rescue or would admit known
counterexample pressure.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Verification

- `python -m py_compile` passed for the new helper.
- `python -m json.tool` passed for the new artifact.
- Full lane JSON validation passed for 24 JSON files.
- Full run-log JSONL validation passed for 25 records; final line has
  `primary_outcome=candidate_evidence_rows_emitted` and
  `measured_minutes=48.77`.
- Required run-record field validation passed.
- `git diff --check` passed.
- No raw `.pdb`, `.cif`, or `.mmcif` files were written in the lane paths.
- No production label registries, mechanism fingerprints, migration manifests,
  or label imports were touched.
- Remote-tip temporary-index pushes succeeded; local worktree status still
  appears dirty because local `HEAD` is stale and cannot be fast-forwarded by
  normal linked-worktree metadata operations.

## Exact Next Experiment

Stop ordered-solvent bridge probing as a promotion route. Only resume this lane
for a genuinely different source-free modality that can adjudicate ADP/product,
substrate-analog, reciprocal folded-chain, or same-chain biology without
review-context leakage. Otherwise preserve source-reviewed adjudication for
product/ADP, split-state, substrate-analog, reciprocal folded-chain, and
same-chain substrate biology.
