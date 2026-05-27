# Packet 1 / Wave 1 Follow-Through - 2026-05-27

This run closed the remaining Packet 1 / Wave 1 follow-through as additive
review-only artifacts. It did not change production scoring, ontology IDs,
thresholds, imports, model outputs, or fingerprint definitions.

## Locked Reading Order

Use the original Wave 1 card as frozen history, then read the addenda:

1. `artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json`
2. `artifacts/v3_wave1_representation_shootout_result_card_702_20260527_addendum.json`
3. `artifacts/v3_v2_sublabel_audit_702_flavin_hydride_transfer_demotion_20260527.json`
4. `artifacts/v3_packet1_wave1_lockdown_addendum_702_20260527.json`

## Packet 1 Lock-Down

- `m_csa:217` and `m_csa:477` are the TM-pair-verified fold-conflict OOS
  anchors.
- `m_csa:428` is only a partial fold-conflict row with a TIM-barrel
  incidental-primary-hit caveat.
- `m_csa:440` is a near-orphan OOS / router-abstention diagnostic, not a
  fold-conflict row.
- `m_csa:497` is now canonically `out_of_scope` and must be excluded from
  primary flavin and near-orphan primary metrics.

## Flavin Follow-Through

`flavin.dehydrogenase_oxidase_hydride_transfer` is no longer ready for future
eval design without expert review. The addendum demotes it because the bucket
spans clean hydride transfer, semiquinone/electron transfer, covalent FAD
adduct chemistry, flavin radical dehydratase chemistry, and the already fixed
NO reductase case.

`m_csa:750` remains canonically unchanged, but its label state is
review-blocked. The mechanism evidence points to flavin semiquinone radical
dehydration with catalytic Fe-S participation, so it is unsafe as a Wave 1
`top_foldseek_success_learned_failure` canary until review resolves whether it
belongs OOS under v1 or under a future radical flavin/Fe-S dehydratase
fingerprint.

`m_csa:43` still reads as a valid metal-dependent hydrolase Wave 1 canary.

## New Review Queues

- The 210-row `label_factory_review_import` heuristic audit emits a small
  expert-review shortlist without relabeling anything automatically.
- The FMO acquisition packet keeps `m_csa:131` as
  `secondary_ood_probe::flavin_monooxygenase`, identifies two local clean FMO
  review candidates (`m_csa:551`, `m_csa:973`), and records that at least four
  additional clean rows are still required before any primary-promotion
  reconsideration.
