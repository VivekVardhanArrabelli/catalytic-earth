# FMO Hard-Negative Counteraxis - 2026-05-27

Review-only artifact:
`artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json`.

No registry, ontology, fingerprint, import, threshold, model-output,
model-training, or production-scoring change was made.

## Inputs inspected

- `artifacts/v3_packet3_v2_sublabel_decision_closure_702_20260527.json`
- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_flavin_fe_s_population_expert_disposition_702_20260527.json`
- `artifacts/v3_wave1_1_diagnostic_benchmark_result_702_20260527.json`
- `artifacts/v3_flavin_monooxygenase_acquisition_closure_702_20260527.json`
- current `data/registries/curated_mechanism_labels.json`
- entry names from `artifacts/v1_graph_1025.json`

## Current axis state

- Current labels: `702`.
- Current canonical FMO rows: `m_csa:131`, `m_csa:132`.
- Current canonical `flavin_dehydrogenase_reductase` rows: `48`.
- Current OOS rows: `472`.
- `m_csa:497` and `m_csa:750` are already relabeled to OOS and excluded from
  primary flavin metrics.
- `m_csa:551` and `m_csa:973` are clean secondary/future FMO candidates, not
  hard negatives; the acquisition closure still blocks primary FMO promotion
  until n>=6 and hard-negative separation are met.

## Counteraxis groups

| Control group | Representatives | Why not FMO | Expected behavior | Regression gate |
| --- | --- | --- | --- | --- |
| ordinary flavin hydride-transfer dehydrogenase/reductase | `m_csa:3`, `m_csa:6`, `m_csa:353`, `m_csa:381`, `m_csa:506`, `m_csa:892` | Flavin transfers hydride/electrons between substrate and redox partners; no flavin peroxy oxygen insertion. | route_other_family | FMO requires explicit C4a-(hydro)peroxyflavin plus substrate oxygen insertion. |
| flavin oxidase O2 acceptor, not monooxygenase | `m_csa:109`, `m_csa:110`, `m_csa:113`, `m_csa:354`, `m_csa:822`, `m_csa:852`, `m_csa:895` | O2/peroxide is acceptor or peroxide partner, not oxygen donor inserted by flavin. | route_other_family | Oxygen or oxidase naming alone must not satisfy FMO. |
| flavin + Fe-S relay / HCAR-like | `m_csa:990`, `m_csa:108`, `m_csa:114`, `m_csa:142`, `m_csa:294`, `m_csa:800` | Fe-S relays electrons and FAD performs reduction/coupled chemistry, not peroxy oxygenation. | route_other_family | Carry `cofactor_complexity=fe_s_plus_flavin`; require peroxy oxygenation before FMO. |
| flavodiiron NO reductase | `m_csa:497` | Non-heme di-iron NO reduction; FMNH2 is electron donor, not oxygenating flavin locus. | reject | Any FMO call on `m_csa:497` is a hard regression. |
| radical flavin/Fe-S dehydratase | `m_csa:750` | FAD semiquinone plus Fe-S radical dehydration, not monooxygenation. | reject | Any FMO call on `m_csa:750` is a hard regression. |
| covalent FAD-adduct APS reductase-like | `m_csa:123` | Covalent FAD-substrate adduct and sulfur-oxygen bond chemistry, not O2-derived oxygen insertion. | route_other_family | Route as flavin boundary or abstain in child-label settings; never FMO. |
| heme oxygenase/P450/peroxidase | `m_csa:133`, `m_csa:699`, `m_csa:795`, `m_csa:601` | Oxygen activation locus is heme/peroxidase chemistry, not flavin. | route_other_family | Heme evidence routes away from FMO even when named monooxygenase/oxygenase. |
| non-flavin oxygenase/luciferase/metal/pterin/copper | `m_csa:128`, `m_csa:129`, `m_csa:130`, `m_csa:134`, `m_csa:135`, `m_csa:600`, `m_csa:768` | O2 use is supported, but oxygen activation is ATP/luciferin, metal, pterin/non-heme iron, copper, or other non-flavin chemistry. | reject | Non-flavin oxygenases reject as FMO unless direct C4a-peroxy flavin evidence exists. |

## Policy summary

The FMO gate should be keyed to mechanism, not vocabulary or cofactors. FAD/FMN,
NAD(P)H, O2, Fe-S, substrate oxidation, or oxygenase naming are shared features
and must not be sufficient. Clean FMO needs flavin-dependent O2 activation to a
C4a-(hydro)peroxyflavin or equivalent flavin peroxy oxygenating intermediate
followed by substrate oxygen insertion/oxygenation.

The review preserves these controls as regression signal only. It does not
import labels, promote FMO, split v2 child labels, tune thresholds, train models,
or create a countable metric.
