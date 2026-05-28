# Full TM Structural Signal - current702 / Wave 1.1 - 2026-05-28

Read-only structural-neighborhood signal. No labels, registries, ontologies, thresholds, production scoring, imports, model outputs, training artifacts, or source data were changed.

## What was reused

- Current702 coordinate readiness: 702 rows; 696 materialized/reused coordinate rows; 6 missing or unsupported.
- Existing Wave 1 row export: 140 heldout diagnostic rows with Foldseek top1, sequence-NN proxy, and router fields.
- Targeted Packet 1 exact TM chunks: 4 query rows, 2971 heldout-vs-train pair rows retained, 68 rows at TM/Foldseek proxy >= 0.70.
- Raw targeted chunk TSVs found: 4 / 4.

## Compute decision

- The old all-materializable raw TSV referenced by `v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json` is no longer present, so the 952,922 mapped rows could not be reprocessed.
- A staged heldout-vs-train local Foldseek workdir existed with 134 query structures and 538 train targets, but the exact-TM run in that workdir had already run for roughly 90 minutes without convertible output. A duplicate command was stopped; no completed broad rerun is claimed. A second fast heldout-vs-train process plus later smoke-sized structural-search processes appeared later and were also stopped without using them for evidence.
- Disk was restored and kept above the 10 GiB floor by deleting stale `/private/tmp` model-cache directories only; the Foldseek binary and small targeted query raw TSVs were preserved.

## Signal counts

- Near-orphan flagged rows: 35.
- Fold-conflict flagged rows: 15.
- OOS router-control rows: 9.
- Label-contested / do-not-anchor rows: 5.

## Targeted TM rows

| row | status | retained train-test pairs | TM>=0.70 rows | max TM | high-TM neighbor labels |
| --- | --- | ---: | ---: | ---: | --- |
| `m_csa:217` | verified_fold_conflict_anchor | 719 | 14 | 0.7761 | out_of_scope:2, ser_his_acid_hydrolase:12 |
| `m_csa:428` | caveated_partial_fold_conflict_not_clean_anchor | 709 | 46 | 0.7670 | flavin_dehydrogenase_reductase:2, out_of_scope:44 |
| `m_csa:440` | targeted_tm_supports_near_orphan_not_fold_conflict | 1365 | 0 | 0.6455 | none |
| `m_csa:477` | verified_fold_conflict_anchor | 178 | 8 | 0.7723 | ser_his_acid_hydrolase:8 |

## Metric-anchor holds

- Label/child-cell contested holds that should not anchor metrics now: `m_csa:403`, `m_csa:497`, `m_csa:723`, `m_csa:750`, `m_csa:994`.
- `m_csa:428` has targeted TM evidence but remains caveated; keep it out of clean fold-conflict anchor counts.
- `m_csa:217` and `m_csa:477` remain Packet 1 verified fold-conflict reference anchors; `m_csa:440` remains an OOS router-control / near-orphan row, not a fold-conflict anchor.

## Outputs

- `artifacts/v3_full_tm_structural_signal_702_20260528.json`: 702 row summaries plus targeted top-k exact-TM evidence.
- This report: `work/full_tm_structural_signal_20260528.md`.

## Non-claims

- Full 692-query all-vs-all current702 TM evidence remains incomplete; this artifact does not claim a canonical full TM-score holdout.
- The old all-materializable raw TSV was not present, so its 952922 mapped rows could not be reprocessed beyond the retained 200-row artifact.
- Only four Packet 1 rows have completed exact targeted TM top-k evidence; other Wave 1 rows retain top1 Foldseek proxy evidence from the existing audit.
- Sequence identity is reported only where existing exports already contain it; otherwise the deterministic 3-mer Jaccard proxy is surfaced.
- Rows marked label_contested_do_not_anchor_metrics are review-only holds and should not anchor metrics until a separate expert/frozen-contract decision.
