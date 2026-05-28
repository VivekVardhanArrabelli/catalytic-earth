# Bronze Label Mismatch and Full TM Audit - 2026-05-28

Review-only cross-cutting audit before further benchmark decisions. No labels, registries, ontologies, imports, thresholds, production scoring, or model outputs were changed.

## Label-Factory Heuristic Shortlist

- Population: 210 bronze rows with `label_factory_review_import` provenance.
- Heuristic shortlist: 11 rows; already-resolved label-quality blockers: m_csa:497, m_csa:750.
- Interpretation: cheap red-flag scan only, not a 210-row manual review.

| Row | Current family | Rule | Signals | Prior disposition | Action |
| --- | --- | --- | --- | --- | --- |
| `m_csa:486` | `metal_dependent_hydrolase` | `metal_sulfatase_or_nucleotide_boundary` | nucleotide hydrolase | `open_shortlist` | review note only |
| `m_csa:506` | `flavin_dehydrogenase_reductase` | `flavin_metal_radical_conflict` | semiquinone | `keep_current_label` | review note only |
| `m_csa:535` | `metal_dependent_hydrolase` | `metal_sulfatase_or_nucleotide_boundary` | nucleotide hydrolase | `open_shortlist` | review note only |
| `m_csa:714` | `heme_peroxidase_oxidase` | `heme_nonheme_or_mixed_metal_oxidase_signal` | copper, terminal oxidase | `move_to_secondary_or_future_family_blocker` | pull/quarantine before model claims |
| `m_csa:735` | `heme_peroxidase_oxidase` | `heme_nonheme_or_mixed_metal_oxidase_signal` | copper, terminal oxidase | `move_to_secondary_or_future_family_blocker` | pull/quarantine before model claims |
| `m_csa:854` | `plp_dependent_enzyme` | `plp_b12_or_radical_boundary` | Fe-S | `open_shortlist` | review note only |
| `m_csa:855` | `plp_dependent_enzyme` | `plp_b12_or_radical_boundary` | Fe-S | `keep_current_label` | review note only |
| `m_csa:862` | `flavin_dehydrogenase_reductase` | `flavin_metal_radical_conflict` | semiquinone | `keep_current_label` | review note only |
| `m_csa:935` | `heme_peroxidase_oxidase` | `heme_nonheme_or_mixed_metal_oxidase_signal` | pterin | `open_shortlist` | review note only |
| `m_csa:978` | `flavin_dehydrogenase_reductase` | `flavin_metal_radical_conflict` | radical | `keep_current_label` | review note only |
| `m_csa:994` | `metal_dependent_hydrolase` | `metal_sulfatase_or_nucleotide_boundary` | nucleotide hydrolase | `open_shortlist` | pull/quarantine before model claims |

Resolved rows already pulled or requiring stale-slice pull-through: `m_csa:497` and `m_csa:750`.

## Heldout-vs-Train TM Signal

- Parsed local retained-hit chunks for 134/134 heldout queries against 538 train structures.
- Missing query chunk: none; missing rows are explicit in JSON.
- Retained unique heldout/train pairs: 32608/72092; exhaustive pair ceiling closed: `false`.
- Max retained heldout/train TM score: 0.9826; threshold remains `<0.7` and no split/claim threshold changed.
- Classification counts: `{"dense_same_family_structural_neighborhood": 46, "fold_conflict_structural_neighborhood": 7, "mixed_high_tm_structural_neighborhood": 25, "near_orphan_no_retained_tm_ge_0_70_hit": 56}`.
- Review-use counts: `{"dense_same_family_transfer_candidate": 46, "fold_conflict_candidate": 4, "mixed_neighborhood_review_candidate": 12, "near_orphan_candidate_from_retained_hits": 56, "oos_fold_conflict_hard_negative_candidate": 16}`.

Top fold-conflict or mixed-neighborhood examples retained in the JSON:

| Row | Family | Max TM | High-TM neighbors | Review use | Nearest target |
| --- | --- | ---: | ---: | --- | --- |
| `m_csa:714` | `heme_peroxidase_oxidase` | 0.972 | 4 | `mixed_neighborhood_review_candidate` | m_csa:124 |
| `m_csa:220` | `out_of_scope` | 0.9307 | 10 | `oos_fold_conflict_hard_negative_candidate` | m_csa:298 |
| `m_csa:346` | `out_of_scope` | 0.9306 | 12 | `oos_fold_conflict_hard_negative_candidate` | m_csa:70 |
| `m_csa:628` | `out_of_scope` | 0.9127 | 9 | `oos_fold_conflict_hard_negative_candidate` | m_csa:533 |
| `m_csa:333` | `out_of_scope` | 0.9073 | 5 | `oos_fold_conflict_hard_negative_candidate` | m_csa:280 |
| `m_csa:188` | `out_of_scope` | 0.9029 | 9 | `oos_fold_conflict_hard_negative_candidate` | m_csa:557 |
| `m_csa:144` | `out_of_scope` | 0.8809 | 5 | `oos_fold_conflict_hard_negative_candidate` | m_csa:562 |
| `m_csa:606` | `out_of_scope` | 0.873 | 9 | `oos_fold_conflict_hard_negative_candidate` | m_csa:470 |
| `m_csa:431` | `ser_his_acid_hydrolase` | 0.8557 | 4 | `mixed_neighborhood_review_candidate` | m_csa:631 |
| `m_csa:497` | `out_of_scope` | 0.848 | 7 | `oos_fold_conflict_hard_negative_candidate` | m_csa:16 |
| `m_csa:723` | `ser_his_acid_hydrolase` | 0.8425 | 2 | `fold_conflict_candidate` | m_csa:380 |
| `m_csa:255` | `out_of_scope` | 0.8318 | 8 | `oos_fold_conflict_hard_negative_candidate` | m_csa:237 |
| `m_csa:686` | `metal_dependent_hydrolase` | 0.8245 | 7 | `mixed_neighborhood_review_candidate` | m_csa:360 |
| `m_csa:424` | `plp_dependent_enzyme` | 0.8202 | 15 | `mixed_neighborhood_review_candidate` | m_csa:855 |
| `m_csa:453` | `ser_his_acid_hydrolase` | 0.8155 | 12 | `mixed_neighborhood_review_candidate` | m_csa:518 |

Near-orphan/no-retained-high-TM examples retained in the JSON:

| Row | Family | Max TM | Review use |
| --- | --- | ---: | --- |
| `m_csa:9` | `out_of_scope` | 0.6311 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:10` | `out_of_scope` | 0.6061 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:14` | `out_of_scope` | 0.6057 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:31` | `out_of_scope` | 0.5127 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:43` | `metal_dependent_hydrolase` | 0.6062 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:44` | `metal_dependent_hydrolase` | 0.6171 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:46` | `out_of_scope` | 0.6917 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:56` | `out_of_scope` | 0.5041 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:67` | `out_of_scope` | 0.6783 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:71` | `out_of_scope` | 0.584 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:79` | `out_of_scope` | 0.6475 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:86` | `out_of_scope` | 0.5721 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:97` | `metal_dependent_hydrolase` | 0.5508 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:121` | `out_of_scope` | 0.6509 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:125` | `out_of_scope` | 0.4894 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:129` | `out_of_scope` | 0.5574 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:163` | `metal_dependent_hydrolase` | 0.5994 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:171` | `metal_dependent_hydrolase` | 0.6657 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:180` | `metal_dependent_hydrolase` | 0.5027 | `near_orphan_candidate_from_retained_hits` |
| `m_csa:185` | `out_of_scope` | 0.4748 | `near_orphan_candidate_from_retained_hits` |

## Pull / Quarantine Policy

Rows that must be pulled or kept out of clean canaries/test slices before model claims:

| Row | Class | Reason |
| --- | --- | --- |
| `m_csa:403` | `must_pull_from_metric_anchor_slices` | prior full-TM signal marked label_contested_do_not_anchor_metrics; keep out of canary/test claims until reviewed |
| `m_csa:497` | `must_pull_or_keep_pulled` | already-resolved label-quality blocker from provisional label_factory_review_import population |
| `m_csa:714` | `quarantine_from_clean_canaries` | future-family/subfamily boundary blocker; do not use as a clean seed-fingerprint canary until policy exists |
| `m_csa:723` | `must_pull_from_metric_anchor_slices` | prior full-TM signal marked label_contested_do_not_anchor_metrics; keep out of canary/test claims until reviewed |
| `m_csa:735` | `quarantine_from_clean_canaries` | future-family/subfamily boundary blocker; do not use as a clean seed-fingerprint canary until policy exists |
| `m_csa:750` | `must_pull_or_keep_pulled` | already-resolved label-quality blocker from provisional label_factory_review_import population |
| `m_csa:994` | `must_pull_from_metric_anchor_slices` | prior full-TM signal marked label_contested_do_not_anchor_metrics; keep out of canary/test claims until reviewed |

Do not treat the TM signal as a benchmark win claim. It is structural-neighborhood review evidence for fold-conflict and near-orphan classification only, with exhaustive all-pair closure still blocked by retained-hit coverage rather than complete 134x538 pair-row retention.

## Verification

```text
python -m json.tool artifacts/v3_bronze_label_mismatch_and_full_tm_audit_702_20260528.json
PYTHONPATH=src python -m catalytic_earth.cli validate
git diff --check
```
