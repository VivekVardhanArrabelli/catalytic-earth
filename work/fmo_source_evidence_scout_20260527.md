# FMO Source Evidence Scout

Run time: 2026-05-28T02:37:34Z

Scope: focused source-review only for flavin monooxygenase and oxygenase-boundary candidates. No registry edits, imports, ontology edits, threshold changes, model outputs, or production scoring were performed. Source text was paraphrased and was not used as predictive feature input.

## Local Artifacts

- `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json`: found and inspected. It corroborates `m_csa:551` and `m_csa:973` as clean future FMO candidates, with 22 hard-negative controls, 2 wrong-chemistry blockers, and 1 structure-check boundary row.
- `artifacts/v3_flavin_monooxygenase_acquisition_packet_702_20260527.json`: found `m_csa:551` and `m_csa:973` as clean FMO candidates, with `m_csa:141` and `m_csa:128` as non-clean controls.
- `artifacts/v3_flavin_monooxygenase_acquisition_closure_702_20260527.json`: confirmed four local clean signals total: `m_csa:131`, `m_csa:132`, `m_csa:551`, and `m_csa:973`.
- `artifacts/v1_graph_1025.json` and `artifacts/v2_benchmark_1025.json`: supplied local M-CSA mechanism text/provenance for close review.

## Source Conclusions

| Candidate | Conclusion | Review note |
| --- | --- | --- |
| `m_csa:131` 4-hydroxybenzoate 3-monooxygenase | True FAD/NADPH flavin monooxygenase | Local M-CSA and UniProt support FAD reduction, C4a-peroxy/hydroperoxy FAD, and aromatic hydroxylation. |
| `m_csa:132` alkanal monooxygenase | True FMNH2 oxygenase, boundary | Local M-CSA supports FMN-peroxo/C4a-peroxy chemistry; keep separate from single-component NADPH/FAD FMOs. |
| `m_csa:551` phenol 2-monooxygenase | True FAD/NADPH flavin monooxygenase | Local M-CSA explicitly supports C4a-hydroperoxyflavin phenol hydroxylation; current registry lane remains dehydrogenase/reductase pending expert review. |
| `m_csa:973` DszC | True reduced-FMN sulfur monooxygenase | Local M-CSA and ACS mechanism source support C4aOOH sulfur oxygen transfer; flavin reduction is partner-supplied. |
| `m_csa:141` 4-cresol dehydrogenase | Ordinary flavin dehydrogenase/reductase | Local M-CSA shows substrate hydride transfer to FAD and water-derived oxygen, not C4a-peroxy oxygen transfer. |
| `m_csa:128` firefly luciferase | Other family | Local evidence supports ATP/luciferyl-adenylate oxygenation, not flavin monooxygenase chemistry. |
| `uniprot:P12015` CHMO | True BVMO | UniProt/Rhea plus CHMO literature support FAD/NADPH Baeyer-Villiger oxygen insertion through C4a-peroxyflavin. |
| `uniprot:Q93TJ5` HAPMO | True BVMO | UniProt/Rhea and primary HAPMO sources support FAD/NADPH Baeyer-Villiger oxygenation. |
| `uniprot:P23262` salicylate hydroxylase | True flavoprotein monooxygenase | UniProt/Rhea and NahG mechanism source support FAD/NADH C4a-hydroperoxyflavin oxidative decarboxylation. |
| `uniprot:P11295` IucD | True FAD/NADPH N-hydroxylase, medium confidence | Source support is strong for FAD/NADPH/O2 lysine N6-hydroxylation; add candidate-specific C4a intermediate source if required. |
| `uniprot:Q01740` FMO1 / dimethylaniline monooxygenase | True class B FMO | UniProt/Rhea and FMO oxidative-half-reaction literature support FAD/NADPH C4a-hydroperoxyflavin N/S oxygenation. |
| `uniprot:P06617` tryptophan 2-monooxygenase | Boundary, not clean FMO packet | UniProt supports FMN and O2 but no NAD(P)H reductive activation or explicit C4a oxygen-transfer mechanism in this scout. |
| `uniprot:O15229` KMO | True FAD/NADPH monooxygenase | Prior local external packet plus UniProt/Rhea support KMO as source-admissible, with process gates incomplete. |
| `uniprot:P25535` UbiI | True aromatic FAD/NADPH hydroxylase, medium confidence | Strong FAD/NADPH/O2 hydroxylase support; add explicit C4a source if needed. |
| `uniprot:H3JQW0` OTEMO | True BVMO | UniProt/Rhea and OTEMO/BVMO structural source support Baeyer-Villiger flavin-peroxide chemistry. |
| `uniprot:Q6F4M8` NPCA | True flavin monooxygenase, medium confidence | Strong FAD/nicotinamide/O2 monooxygenase support; add explicit C4a source if needed. |

## Review Packet Readiness

Admissible for label-review evidence packet now: `m_csa:131`, `m_csa:132`, `m_csa:551`, `m_csa:973`, `uniprot:P12015`, `uniprot:Q93TJ5`, `uniprot:P23262`, `uniprot:P11295`, `uniprot:Q01740`, `uniprot:O15229`, `uniprot:P25535`, `uniprot:H3JQW0`, and `uniprot:Q6F4M8`.

Not admissible as clean FMO support in this packet: `m_csa:141`, `m_csa:128`, and `uniprot:P06617`.

External non-M-CSA candidates remain source-reviewed only. They still need source-free structure/geometry checks, duplicate/leakage screening, terminal review, and factory/import gates before any label import.
