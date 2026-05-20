# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T12:03:32-0500

Primary outcome: `blocker_not_cleared_biology_ambiguity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

## What Was Tested

Built a 22-row review-only diagnostic tranche in
`artifacts/research_lanes/epk_substrate_role_identity/epk_substrate_role_identity_tranche_20260520.json`.
All rows materialized from RCSB PDB files in memory; no raw coordinate files
were written.

Rows included requested review-only positives:
`5HVK`, `6Z3R`, `9UUR`, `9UUX`, `1QMZ`, `3QHR`, `3QHW`, `3X2U`, `3X2V`,
`3X2W`, and `4IAC`.

Rows included requested counterexamples/pressure controls:
`2JJ2`, `7ZE5`, `7B56`, `9UW4`, `3R5F`, `5C1O`, `6U1D`, `6U1E`, `5TT6`,
`6NOO`, and `9NBW`.

Predictive inputs were limited to structure-derived features: ligand state,
terminal gamma-equivalent availability, nearest hydroxyl geometry, nearest
nonpolymer oxygen, chain topology, own-chain nucleotide/metal context, polymer
chain/entity counts, chain length, residue ordinal, Tyr/N-terminal-STY mode,
local atom count, and co-materialization. PDB title, UniProt prose, EC/Rhea,
paper/source text, mechanism labels, curated substrate names, post-hoc source
repair, and candidate-specific threshold tuning were explicitly forbidden.

## Evidence

Rule evaluation is in
`artifacts/research_lanes/epk_substrate_role_identity/epk_substrate_role_identity_rule_eval_20260520.json`.

Strict source-free rule:
`strict_cross_chain_terminal_or_peptide_no_acceptor_ligand_v1`

Confusion matrix: TP=7, FP=1, TN=10, FN=4.

It retained `5HVK`, `6Z3R`, `1QMZ`, `3X2U`, `3X2V`, `3X2W`, and `4IAC`, and
blocked most ATPase/ATP-grasp/transporter controls. It still false-hit `7B56`
because a midlength folded/polymer chain with N-terminal Ser and no own-chain
nucleotide/metal context looks source-free-compatible with a true folded
substrate. It missed `9UUR`/`9UUX` by topology or acceptor-context ambiguity
and missed `3QHR`/`3QHW` because only ADP/product-state ligand atoms were
present.

Permissive nearest-hydroxyl rule:
`permissive_nearest_hydroxyl_6a_v1`

Confusion matrix: TP=9, FP=11, TN=0, FN=2.

It recovered most active-gamma positives but every counterexample with a
nearby Ser/Thr/Tyr hydroxyl became a false hit. This directly confirms that
distance-only or nearest-hydroxyl evidence is not a substrate-role identity
rule.

## Blocker Classification

The blocker is not cleared. The primary failure is biological role ambiguity,
not a missing implementation detail. ATP-dependent sibling families, ATPases,
transporters, kinase-kinase arrangements, product-state structures, and folded
protein substrate complexes can all co-materialize gamma-proximal hydroxyls.
Local topology, residue class, N-terminal position, chain length, and own-chain
ligand context are useful pressure features but do not uniquely identify the
true kinase substrate phosphoacceptor.

Comparable project blockers have not been cleared by structure-only
nearest-atom rules. Prior usable ePK progress required source-reviewed hybrid
evidence as evaluation/support context, while keeping that evidence out of
predictive features.

## Exact Next Experiment

Run
`epk_fresh_nonconfounded_folded_nterminal_substrate_vs_midlength_mimic_stress_v1_review_only`.

Freeze 20-30 PDB IDs before feature extraction: fresh non-overlap folded or
midlength kinase-substrate co-complex candidates with active gamma-capable
ligands, plus matched `7B56`-like midlength N-terminal-STY mimics, ATP-grasp
controls, ATPase/transporter controls, and ADP/product-state positives. Compute
the same source-free features before source validation. Test a prespecified
variant that removes midlength N-terminal-STY acceptance unless an additional
source-free folded-substrate role asymmetry feature is found. Success requires
retaining true folded N-terminal substrate positives while rejecting `7B56`-like
midlength mimics and all sibling controls, with no threshold tuning or registry
edits.
