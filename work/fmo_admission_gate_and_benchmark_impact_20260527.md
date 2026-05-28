# FMO Admission Gate and Benchmark Impact - 2026-05-27

Status: `complete_review_only_no_imports`. Refreshed at `2026-05-28T02:46:25Z` using the candidate scout, source scout, geometry audit, hard-negative counteraxis, v2 design proposal, and Wave 1.1 benchmark artifact.

No imports, canonical label changes, ontology edits, thresholds, model training, production scoring, registry edits, or countable metric changes were made.

## Gate Decision

`m_csa:551` and `m_csa:973` are ready for a human review packet. There is no remaining blocker for packet creation. Both remain blocked for any registry edit until human approval, duplicate/leakage review, and final review clear.

| candidate | candidate scope | review packet | blocked reason | source-free geometry status | duplicate/leakage status | benchmark impact if later approved |
| --- | --- | --- | --- | --- | --- | --- |
| `m_csa:551` phenol 2-monooxygenase | local_m_csa | ready | none for packet creation | FAD plus phenol/IPH support; lacks NADPH/NADP and C4a-peroxy state; mapped-chain pose needs visual review | not complete before registry edit | would raise clean support only to 4 with `m_csa:973`, still below `n>=6`; no Wave 1.1 change |
| `m_csa:973` DszC protein | local_m_csa | ready | none for packet creation | FMN active-site cluster is compatible but ambiguous; lacks substrate/analog, NADPH/NADP, and C4a-peroxy state | not complete before registry edit | would raise clean support only to 4 with `m_csa:551`, still below `n>=6`; no Wave 1.1 change |

Required hard-negative controls for any later positive use: `ordinary_flavin_hydride_transfer_dehydrogenase_reductase`, `flavin_oxidase_o2_acceptor_not_monooxygenase`, `flavin_fe_s_relay_hcar_like`, `flavodiiron_no_reductase_m_csa497`, `radical_flavin_fe_s_dehydratase_m_csa750`, `covalent_fad_adduct_aps_reductase_like`, `heme_oxygenases_p450_peroxidases_not_fmo`, `nonflavin_oxygenases_luciferases_metal_pterin_copper_not_fmo`.

## External Source-Only Candidates

These candidates are source-admissible, but not structure/import-ready. They remain `external_source_only` and `requires_human_approval_before_registry_edit`.

| candidate | enzyme | source confidence | current status | missing gates |
| --- | --- | --- | --- | --- |
| `uniprot:P12015` | cyclohexanone monooxygenase | high | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:Q93TJ5` | 4-hydroxyacetophenone monooxygenase | high | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:P23262` | salicylate hydroxylase / salicylate 1-monooxygenase | high | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:P11295` | L-lysine N6-monooxygenase / IucD | medium | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:Q01740` | flavin-containing monooxygenase 1 / dimethylaniline monooxygenase | high | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:O15229` | kynurenine 3-monooxygenase | high | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:P25535` | 2-octaprenylphenol hydroxylase / UbiI | medium | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:H3JQW0` | 2-oxo-Delta(3)-4,5,5-trimethylcyclopentenylacetyl-CoA monooxygenase / OTEMO | high | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |
| `uniprot:Q6F4M8` | 4-nitrophenol 4-monooxygenase / 4-nitrocatechol 2-monooxygenase oxygenase component | medium | source-admissible only | source-free geometry/materialization, duplicate/leakage, terminal review, and import gates |

`uniprot:P11295`, `uniprot:P25535`, and `uniprot:Q6F4M8` also need stronger candidate-specific C4a-intermediate citations if the human review standard requires intermediate-level evidence.

## Clean Support Count

We do not have `n>=6` clean support now.

Counted clean rows now:

- `m_csa:131` 4-hydroxybenzoate 3-monooxygenase
- `m_csa:132` alkanal monooxygenase (FMN-linked)

Rows ready for human review but not counted yet:

- `m_csa:551` phenol 2-monooxygenase
- `m_csa:973` DszC protein

If both local candidates are later expert-approved, clean support becomes 4. The remaining gap is at least two additional non-duplicate clean FMO positives, plus source-free geometry/materialization, duplicate/leakage screening, terminal human review, import-gate closure, and hard-negative separation.

## Boundary And Control Status

The candidate scout nonclean rows remain non-countable: 22 hard-negative controls, 3 blocked wrong-chemistry rows, and 10 needs-structure-check rows. The needs-structure-check set includes the nine source-only external candidates listed above plus `m_csa:930`; these are useful as acquisition leads or controls, not as clean FMO support.

Source rejected or boundary packets remain blocked: `m_csa:141`, `m_csa:128`, and `uniprot:P06617`. `uniprot:P06617` needs candidate-specific C4a-peroxyflavin or oxygen-transfer mechanism evidence before it could support the FMO lane.

## Benchmark Impact

Immediate Wave 1.1 impact is none. No metrics, thresholds, labels, models, or production scoring changed.

Even after later approval of `m_csa:551` and `m_csa:973`, FMO remains secondary OOD/acquisition-target or later pilot-only because support would be 4, below the proposed `n>=6` floor. External source-only rows can help close that gap only after source-free geometry, duplicate/leakage, terminal review, import gates, and human approval.

## Next Action

Next action should be a human review packet for the local M-CSA candidates first: `m_csa:551` and `m_csa:973`, carrying the geometry caveats and hard-negative counteraxis. After that, run external geometry/materialization work for the strongest source-only candidates to close the remaining `n>=6` gap. Broad acquisition is lower priority because there are already source-admissible external leads waiting on structure/import gates.
