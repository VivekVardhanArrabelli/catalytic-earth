# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T17:20:11-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 49.78 minutes (`2026-05-21T21:30:24Z` to
`2026-05-21T22:20:11Z`).

Run note: disk free space was 29 GiB, above the 10 GiB stop threshold. Normal
`git fetch origin` failed at run start because the sandbox could not write the
linked-worktree `FETCH_HEAD`:

`/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git/worktrees/catalytic-earth-epk-substrate-role-identity/FETCH_HEAD`

`git pull --ff-only origin research/epk-substrate-role-identity` failed on the
same metadata path. The run continued from the current on-disk lane state, which
already contained the remote lane artifacts. Local `HEAD` remains stale relative
to `origin/research/epk-substrate-role-identity`; normal local clean and
HEAD-equals-origin verification remain blocked until linked-worktree metadata
can be fast-forwarded. Use the remote-tip temporary-index commit/push workaround
if normal metadata writes remain blocked.

## What Was Emitted

This run added one bounded source-free coordinate modality: protein Asp/Glu
carboxylate proximity around candidate acceptor atoms, with active-gamma context
tracked separately. The helper fetches model-1 coordinates in memory, emits
compact reduced evidence, and writes no raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_acid_base_proximity_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/acid_base_proximity_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json`

The helper reused 211 candidate/state rows, 54 PDB-level conflict rows, and 135
phosphoproduct materialization rows. It scanned 54 diagnostic PDBs in memory and
emitted 220 compact acid/base proximity rows:

- candidate gamma/acceptor pair rows: 204
- state-only rows: 16
- nonterminal phosphoproduct state rows re-emitted: 9
- product/split rows with acceptor atom context: 5
- active/candidate rows with gamma-context carboxylates: 70
- source-free acid/base signature rows: 68
- mixed positive/counterexample acid/base signatures: 8

No PDB titles, UniProt prose, EC/Rhea, paper/source text, mechanism labels,
curated substrate names, post-hoc source repair, candidate-specific threshold
tuning, production labels, registries, fingerprints, migration manifests, or raw
coordinate dumps were used or changed.

## Evidence Summary

Coordinate states observed:

- `active_gamma=205`
- `adp_state=5`
- `ambiguous_coordinate_state=1`
- `ligand_absent=4`
- `product_state=4`
- `split_state=1`

Acid/base proximity classes:

- `no_near_acceptor_carboxylate=85`
- `acceptor_carboxylate_proximal_with_gamma_context=40`
- `acceptor_carboxylate_contact_with_gamma_context=30`
- `acceptor_carboxylate_contact_without_gamma_context=29`
- `acceptor_carboxylate_proximal_without_gamma_context=25`
- acceptor absent/not resolved state rows: `active_gamma=1`, `adp_state=5`,
  `ambiguous_coordinate_state=1`, `ligand_absent=4`

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

Carboxylate proximity is useful review-routing evidence because it marks whether
candidate acceptors have nearby protein Asp/Glu oxygens and whether those
oxygens are also within a fixed 6.0 A active-gamma shell. It still does not
adjudicate biological substrate-role identity without review context. The
signature audit found 8 mixed positive/counterexample acid/base signatures.

Hard-case observations:

- `9UUR` and `9UUX` reciprocal Tyr candidates have gamma-coupled carboxylate
  contacts, but `9UW4` counterexample candidates do too.
- `3QHR` and `3QHW` product-state acceptors are emitted as product-state review
  evidence without active-gamma context.
- `4HPU` split-state acceptor has carboxylate proximity evidence, but remains
  split-state counterpressure.
- `7B56` internal-fragment pressure remains handled by terminal/internal-fragment
  counterevidence, not acid/base proximity.

## Interpretation

The useful refinement is narrow: acid/base proximity materializes a compact
candidate-level review feature for acceptor geometry. Mixed signature collisions
show it is not substrate-role identity. Promoting a carboxylate signature would
either be a post-hoc rescue or would admit known counterexample pressure.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Verification

- `python -m py_compile` passed for the new helper.
- `python -m json.tool` passed for the new artifact.
- Full lane JSON validation passed for 25 JSON files.
- Full run-log JSONL validation passed for 26 records; final line has
  `primary_outcome=candidate_evidence_rows_emitted` and
  `measured_minutes=49.78`.
- Required run-record field validation passed.
- `git diff --check` passed.
- No raw `.pdb`, `.cif`, or `.mmcif` files were written in the lane paths.
- No production label registries, mechanism fingerprints, migration manifests,
  or label imports were touched.

## Exact Next Experiment

Stop acid/base carboxylate proximity probing as a promotion route. Only resume
this lane for a genuinely different source-free modality that can adjudicate
ADP/product, substrate-analog, reciprocal folded-chain, or same-chain biology
without review-context leakage. Otherwise preserve source-reviewed adjudication
for product/ADP, split-state, substrate-analog, reciprocal folded-chain, and
same-chain substrate biology.
