# 700 Label-Factory Notes

## Accepted Countable Labels

The 700-entry gated pass accepted five additional automation-curated bronze
labels for counting:

- `m_csa:686` (`diisopropyl-fluorophosphatase`) as
  `metal_dependent_hydrolase`; retrieval top1 score `0.5817`, local calcium
  evidence, no counterevidence, no review-gap reasons.
- `m_csa:688` (`classical-complement-pathway C3/C5 convertase`) as
  `ser_his_acid_hydrolase`; retrieval top1 score `0.8300`, Ser-His-Asp/Glu
  mechanism text support, no cofactor requirement, no review-gap reasons.
- `m_csa:694` (`6-deoxyerythronolide B hydroxylase`) as
  `heme_peroxidase_oxidase`; retrieval top1 score `0.7112`, local heme
  evidence, no counterevidence, no review-gap reasons.
- `m_csa:697` (`12-oxophytodienoate reductase`) as
  `flavin_dehydrogenase_reductase`; retrieval top1 score `0.6850`, local FMN
  evidence, no counterevidence, no review-gap reasons.
- `m_csa:699` (`cytochrome P450 (BM-3)`) as `heme_peroxidase_oxidase`;
  retrieval top1 score `0.5208`, local heme evidence, no counterevidence, no
  review-gap reasons.

`artifacts/v3_label_batch_acceptance_check_700.json` records these five labels
as accepted for counting and confirms 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, and 0
accepted review-gap labels. The countable registry now has 624 labels.

## Review Debt

The 700 review-state pass leaves 81 `needs_more_evidence` rows outside the
countable benchmark: 61 carried from the 675 state plus 20 new rows. The top
priority rows remain dominated by selected-structure cofactor gaps and
counterevidence:

- `m_csa:494` remains the highest-priority cobalamin/local-cofactor gap.
- New high-priority rows include `m_csa:687`, `m_csa:684`, `m_csa:680`,
  `m_csa:678`, `m_csa:690`, `m_csa:691`, and `m_csa:692`.
- New-debt next actions are 16 `inspect_alternate_structure_or_cofactor_source`,
  2 `expert_review_decision_needed`, 1 `expert_family_boundary_review`, and
  1 `verify_local_cofactor_or_active_site_mapping`.

The 700 scaling-quality audit classifies the new review-debt rows before
promotion: ontology scope pressure, family-propagation boundary, cofactor
family ambiguity, mixed evidence, reaction/substrate mismatch, and active-site
mapping gaps are observed in the deferred rows. Accepted clean labels have 0
review debt and the sequence-cluster proxy has 0 missing assignments and 0
near-duplicate hits among audited rows.

## Next Review Focus

Do not count the 81 review-state rows unless a later evidence pass removes
their gap reasons. The highest-value next repair is an alternate-structure or
cofactor-source inspection for the new 700 debt rows, especially the heme/flavin
absence patterns that are producing below-threshold, counterevidence-heavy
deferrals.
