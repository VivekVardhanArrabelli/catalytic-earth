# Organic Cofactor Resolution current702

Run: 2026-05-30T07:13:54Z
Snapshot: `snapshot/concordance-gate-current702-20260530` at `f393ad25c3959778c7e66a68974bcfee6c93f031`.

## Scope and label policy

- Frozen heldout clean geometry rows: 135/140 (0.964286).
- Cofactor labels are from selected experimental PDB HETATM/local ligand context only: `ligand_context.cofactor_families` plus ligand-code context for row attribution.
- Mechanism fingerprints, downstream expert routing decisions, registries, ontologies, production scoring, global thresholds, imports, and model weights were not edited or used as cofactor-label ground truth.
- M-CSA identifiers are retained as evaluation/reference row IDs only.

## Support

| Class/contrast | Train positives | Heldout positives | Heldout negatives |
| --- | ---: | ---: | ---: |
| flavin | 40 | 11 | 124 |
| heme | 18 | 5 | 130 |
| plp | 24 | 6 | 129 |
| metal_ion | 146 | 29 | 106 |
| tracked_organic_any | 81 | 22 | 113 |
| no_tracked_organic | 466 | 113 | 22 |

Heldout exact local contexts: {"fe_s_cluster": 2, "flavin": 9, "heme": 3, "metal_ion": 25, "multi": 6, "nad": 2, "none": 80, "plp": 6, "sam": 2}.

## Selected channel reliability

| Channel | Selected source | AUC | AP | TP | FP | FN | TN | Coverage | Row-level caveat |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| flavin | trained:esm2_t12_35m | 0.918622 | 0.732961 | 7 | 5 | 4 | 119 | 1.0 | ESM rows not retained; k-mer rows below are nearest row-level diagnostic |
| heme | trained:esm2_t6_8m | 0.866154 | 0.525794 | 3 | 5 | 2 | 125 | 1.0 | ESM rows not retained; k-mer rows below are nearest row-level diagnostic |
| plp | trained:esm2_t6_8m | 0.990956 | 0.876623 | 5 | 3 | 1 | 126 | 1.0 | ESM rows not retained; k-mer rows below are nearest row-level diagnostic |
| metal_ion | borrowed:mionic | 0.781067 | 0.567376 | 21 | 34 | 8 | 72 | 1.0 | threshold row attribution at M-Ionic >=0.95 |

## Retained row-level diagnostics

The selected ESM per-entry score rows are not retained in the frozen snapshot (`t6` JSONL has 0 rows; `t12` JSONL is absent). The table below uses the retained k-mer sidecar as the nearest row-level diagnostic, not as the production cofactor head.

| Row-level source | Class/contrast | AUC | AP | TP | FP | FN | TN | Top FP contexts | Top FN contexts |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| k-mer control | flavin | 0.470674 | 0.082814 | 4 | 55 | 7 | 69 | {"fe_s_no_tracked_organic": 1, "metal_no_tracked_organic": 7, "no_local_cofactor": 38, "other_organic": 4, "tracked_heme": 2, "tracked_plp": 3} | {"tracked_flavin": 7} |
| k-mer control | heme | 0.807692 | 0.16128 | 3 | 33 | 2 | 97 | {"metal_no_tracked_organic": 7, "no_local_cofactor": 21, "other_organic": 2, "tracked_flavin": 2, "tracked_plp": 1} | {"tracked_heme": 2} |
| k-mer control | plp | 0.613695 | 0.088167 | 2 | 43 | 4 | 86 | {"metal_no_tracked_organic": 8, "no_local_cofactor": 26, "other_organic": 3, "tracked_flavin": 6} | {"tracked_plp": 4} |
| k-mer control | tracked_organic_any | 0.543041 | 0.20673 | 7 | 46 | 15 | 67 | {"metal_no_tracked_organic": 10, "no_local_cofactor": 32, "other_organic": 4} | {"tracked_flavin": 8, "tracked_heme": 3, "tracked_plp": 4} |
| M-Ionic | metal_ion @0.95 | 0.781067 | 0.567376 | 21 | 34 | 8 | 72 | {"no_local_cofactor": 29, "other_organic": 1, "tracked_flavin": 2, "tracked_heme": 2} | {"metal_no_tracked_organic": 6, "other_organic": 1, "tracked_heme": 1} |

## Confidence bins

### k-mer flavin

| Score bin | Rows | Positives | Observed positive rate | Mean score |
| --- | ---: | ---: | ---: | ---: |
| [0.00,0.10) | 0 | 0 | None | None |
| [0.10,0.25) | 0 | 0 | None | None |
| [0.25,0.50) | 76 | 7 | 0.092105 | 0.497598 |
| [0.50,0.75) | 59 | 4 | 0.067797 | 0.501895 |
| [0.75,0.90) | 0 | 0 | None | None |
| [0.90,1.00] | 0 | 0 | None | None |

### k-mer heme

| Score bin | Rows | Positives | Observed positive rate | Mean score |
| --- | ---: | ---: | ---: | ---: |
| [0.00,0.10) | 0 | 0 | None | None |
| [0.10,0.25) | 0 | 0 | None | None |
| [0.25,0.50) | 99 | 2 | 0.020202 | 0.494244 |
| [0.50,0.75) | 36 | 3 | 0.083333 | 0.503058 |
| [0.75,0.90) | 0 | 0 | None | None |
| [0.90,1.00] | 0 | 0 | None | None |

### k-mer plp

| Score bin | Rows | Positives | Observed positive rate | Mean score |
| --- | ---: | ---: | ---: | ---: |
| [0.00,0.10) | 0 | 0 | None | None |
| [0.10,0.25) | 0 | 0 | None | None |
| [0.25,0.50) | 90 | 4 | 0.044444 | 0.496395 |
| [0.50,0.75) | 45 | 2 | 0.044444 | 0.502216 |
| [0.75,0.90) | 0 | 0 | None | None |
| [0.90,1.00] | 0 | 0 | None | None |

### k-mer tracked_organic_any

| Score bin | Rows | Positives | Observed positive rate | Mean score |
| --- | ---: | ---: | ---: | ---: |
| [0.00,0.10) | 0 | 0 | None | None |
| [0.10,0.25) | 0 | 0 | None | None |
| [0.25,0.50) | 82 | 15 | 0.182927 | 0.498138 |
| [0.50,0.75) | 53 | 7 | 0.132075 | 0.502216 |
| [0.75,0.90) | 0 | 0 | None | None |
| [0.90,1.00] | 0 | 0 | None | None |

### M-Ionic metal_ion

| Score bin | Rows | Positives | Observed positive rate | Mean score |
| --- | ---: | ---: | ---: | ---: |
| [0.00,0.10) | 0 | 0 | None | None |
| [0.10,0.25) | 3 | 0 | 0.0 | 0.20398 |
| [0.25,0.50) | 13 | 0 | 0.0 | 0.418954 |
| [0.50,0.75) | 24 | 2 | 0.083333 | 0.657886 |
| [0.75,0.90) | 20 | 2 | 0.1 | 0.840498 |
| [0.90,1.00] | 75 | 25 | 0.333333 | 0.967557 |

## False positive / false negative examples

### flavin nearest row-level rows

| Error | Entry | Score | Local families | Ligands | Context |
| --- | --- | ---: | --- | --- | --- |
| FP | m_csa:121 | 0.505677 | ['heme'] | ['HEM', 'MO', 'MTE'] | tracked_heme |
| FP | m_csa:79 | 0.505201 | [] | ['DMD'] | no_local_cofactor |
| FP | m_csa:453 | 0.504653 | [] | [] | no_local_cofactor |
| FP | m_csa:431 | 0.503776 | [] | [] | no_local_cofactor |
| FP | m_csa:254 | 0.503592 | [] | ['R46'] | no_local_cofactor |
| FP | m_csa:419 | 0.503519 | ['plp'] | ['PLP'] | tracked_plp |
| FP | m_csa:346 | 0.50345 | [] | ['CAA'] | no_local_cofactor |
| FP | m_csa:313 | 0.503344 | [] | ['NRI'] | no_local_cofactor |
| FN | m_csa:211 | 0.497138 | ['flavin'] | ['FMN'] | tracked_flavin |
| FN | m_csa:892 | 0.497308 | ['flavin'] | ['FMN', 'ORO'] | tracked_flavin |
| FN | m_csa:551 | 0.497675 | ['flavin'] | ['FAD', 'IPH'] | tracked_flavin |
| FN | m_csa:3 | 0.497678 | ['flavin'] | ['FAD'] | tracked_flavin |
| FN | m_csa:990 | 0.497706 | ['fe_s_cluster', 'flavin'] | ['FAD', 'SF4'] | tracked_flavin |
| FN | m_csa:497 | 0.498739 | ['flavin'] | ['FEO', 'FMN', 'OXY'] | tracked_flavin |
| FN | m_csa:750 | 0.498836 | ['fe_s_cluster', 'flavin'] | ['FAD', 'SF4'] | tracked_flavin |

### heme nearest row-level rows

| Error | Entry | Score | Local families | Ligands | Context |
| --- | --- | ---: | --- | --- | --- |
| FP | m_csa:46 | 0.509034 | ['sam'] | ['SAM'] | other_organic |
| FP | m_csa:627 | 0.508387 | [] | [] | no_local_cofactor |
| FP | m_csa:321 | 0.506836 | ['metal_ion'] | ['ZN'] | metal_no_tracked_organic |
| FP | m_csa:31 | 0.506397 | [] | ['DHF', 'TMP'] | no_local_cofactor |
| FP | m_csa:71 | 0.505961 | [] | [] | no_local_cofactor |
| FP | m_csa:185 | 0.504807 | [] | ['PED'] | no_local_cofactor |
| FP | m_csa:313 | 0.504608 | [] | ['NRI'] | no_local_cofactor |
| FP | m_csa:129 | 0.503839 | [] | ['AKG', 'FE2', 'TAU'] | no_local_cofactor |
| FN | m_csa:709 | 0.496403 | ['heme'] | ['HEM'] | tracked_heme |
| FN | m_csa:250 | 0.499119 | ['heme', 'metal_ion'] | ['HEM', 'MN'] | tracked_heme |

### plp nearest row-level rows

| Error | Entry | Score | Local families | Ligands | Context |
| --- | --- | ---: | --- | --- | --- |
| FP | m_csa:388 | 0.507466 | [] | ['ASP'] | no_local_cofactor |
| FP | m_csa:79 | 0.507425 | [] | ['DMD'] | no_local_cofactor |
| FP | m_csa:402 | 0.506308 | [] | ['PO4'] | no_local_cofactor |
| FP | m_csa:97 | 0.505586 | ['metal_ion'] | ['DHZ', 'ZN'] | metal_no_tracked_organic |
| FP | m_csa:617 | 0.504387 | [] | [] | no_local_cofactor |
| FP | m_csa:313 | 0.504111 | [] | ['NRI'] | no_local_cofactor |
| FP | m_csa:606 | 0.504084 | [] | [] | no_local_cofactor |
| FP | m_csa:369 | 0.50396 | [] | ['PO4'] | no_local_cofactor |
| FN | m_csa:418 | 0.49568 | ['plp'] | ['PLP'] | tracked_plp |
| FN | m_csa:854 | 0.497236 | ['plp'] | ['ACT', 'PLP'] | tracked_plp |
| FN | m_csa:545 | 0.49937 | ['plp'] | ['PLP'] | tracked_plp |
| FN | m_csa:424 | 0.499646 | ['plp'] | ['PLP'] | tracked_plp |

## Concordance gating resolution

- `flavin`: conditional_not_broad. conditional_target_rescue_only.
- `heme`: discounted_except_local_role_or_preregistered_target_rescue. discount_broad_gating.
- `plp`: diagnostic_only_until_retained_row_level_high_confidence_evidence_exists. strong_rank_signal_but_discount_for_gate.
- `metal_ion`: trusted only when combined with existing route/geometry constraints. strict_threshold_contrast_only.
- `no_tracked_organic`: safe_as_suppression_context_not_as_biological_absence_claim. contrast_not_ground_truth_absence.

No routing policy or threshold was rewired. The output stops at artifact/report diagnostics.

## Required outputs

- JSON: `artifacts/v3_organic_cofactor_resolution_current702_20260530.json`
- Report: `work/organic_cofactor_resolution_current702_20260530.md`
