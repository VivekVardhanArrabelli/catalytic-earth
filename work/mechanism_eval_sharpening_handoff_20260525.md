# Mechanism Evaluation Sharpening Handoff - 2026-05-25

## Scope

This run produced artifact-only evaluation sharpening for the current 702-label
registry. It did not edit curated labels, fingerprint registries, ontology
registries, production scoring, thresholds, or representation branch outputs.

## Artifacts

- `artifacts/v3_mechanism_prediction_fold_controlled_eval_design_702_20260525.json`
- `artifacts/v3_mechanism_prediction_orphan_eval_design_702_20260525.json`
- `artifacts/v3_mechanism_fingerprint_v2_sublabel_audit_702_20260525.json`

## Fold-Controlled Pilot

The local retained Foldseek TM signal exposes 3 high-TM heldout/train trap rows
across 2 heldout out-of-scope examples. In each row, the retained structural
neighbor belongs to a v1 primary fingerprint and would be an incorrect
fold-neighbor transfer. The retained signal contains 0 primary-vs-primary
cross-fingerprint traps, so all fold-neighborhood claims are provisional.

Current row-level readout:

- Foldseek structural NN proxy: 3/3 follows the fold neighbor incorrectly.
- Sequence-NN: 2/3 abstain correctly for out-of-scope; 1/3 wrong confident
  transfer.
- Active-site geometry baseline: 3/3 abstain correctly for out-of-scope.
- ESM-2 150M, ProtT5, SaProt, 3Di-token NN, and ESM-C: no current702 row-level
  local prediction artifacts found.

## Near-Orphan Pilot

The near-orphan pilot defines rows as heldout v1 primary examples with no
retained same-fingerprint Foldseek train neighbor at TM-score >= 0.70. This
is a retained-signal proxy, not proof that no full structural neighbor exists.

Current row-level readout across 35 near-orphan primary rows:

- Sequence-NN: 25 useful abstentions, 6 correct predictions, 4 wrong confident
  transfers.
- Foldseek structural NN proxy: 35 abstentions because no strong retained
  structural neighbor is available.
- Active-site geometry baseline: 35 correct predictions.
- ESM-2 150M, ProtT5, SaProt, 3Di-token NN, and ESM-C: unavailable locally.

The useful metric here is calibrated abstention versus wrong confident transfer,
not raw accuracy alone.

## V2 Sublabel Audit

The v2 audit covers all 226 v1 primary positive labels with proposal-only
sublabel assignments. It keeps review-only rationale and expert context out of
predictive model features. The audit concludes v1's five primary groups remain
usable as coarse benchmark labels, but are too coarse for the final
representation-learning question without sublabel-stratified analysis.

Ready for future evaluation design after expert approval:

- `ser_his_acid.lipase_esterase_cutinase_like`
- `ser_his_acid.serine_protease_peptidase_like`
- `metal_hydrolase.amidohydrolase_deaminase_like`
- `metal_hydrolase.phosphoesterase_nuclease_or_phosphatase_like`
- `metal_hydrolase.zinc_metalloprotease_or_metallopeptidase_like`
- `plp.lyase_eliminase_synthase`
- `plp.transaminase_aminotransferase`
- `flavin.dehydrogenase_oxidase_hydride_transfer`
- `heme.peroxidase_catalase_like`

Needs expert review before evaluation use:

- underpowered/boundary candidates such as metallo-beta-lactamase-like,
  carbonic anhydrase-like, PLP decarboxylase, PLP radical/cobalamin boundary,
  flavin monooxygenase-like boundary, and heme oxidase/oxygenase-like gap
- all unresolved catch-all sublabels

## Blockers

- CATH/SCOP assignments are unavailable locally; Foldseek TM is the provisional
  fold-neighborhood proxy.
- The retained Foldseek artifact is review-only and not a full accepted
  TM-score split.
- No current702 row-level artifacts are locally available for ESM-2 150M,
  ProtT5, SaProt, 3Di-token NN, or ESM-C.
- V2 sublabels are proposal-only until explicit expert approval.
