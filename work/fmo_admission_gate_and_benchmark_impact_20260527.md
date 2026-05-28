# FMO Admission Gate and Benchmark Impact - 2026-05-27

Status: `complete_review_only_no_imports`.

All requested FMO inputs are present. This run made no imports, registry edits, ontology edits, threshold changes, model-training changes, or production-scoring changes.

## Gate Decision

`m_csa:551` and `m_csa:973` are ready for a human review packet. They are not import-ready, not canonical-label changes, and both remain `requires_human_approval_before_registry_edit`.

| candidate | review packet | blocked reason | clean support impact | benchmark impact | controls |
| --- | --- | --- | --- | --- | --- |
| `m_csa:551` phenol 2-monooxygenase | ready | none for packet creation; caveats remain for expert review | yes; together they raise clean support from 2 to 4 if approved | no Wave 1.1 change; future v2 remains secondary/pilot-only below n>=6 | 8 counteraxis groups required |
| `m_csa:973` DszC protein | ready | none for packet creation; caveats remain for expert review | yes; together they raise clean support from 2 to 4 if approved | no Wave 1.1 change; future v2 remains secondary/pilot-only below n>=6 | 8 counteraxis groups required |

Important packet caveats:

- `m_csa:551`: source evidence is high-confidence and geometry supports FMO, but the selected structure lacks NADPH/NADP and a C4a-peroxy state; mapped-chain FAD C4X to phenol/IPH distance needs visual review.
- `m_csa:973`: source evidence is high-confidence, but geometry is ambiguous because the selected FMN-bound structure lacks substrate/analog, NADPH/NADP, and a C4a-peroxy state.

## Not Ready For Full Gate

Source-only external candidates are not ready for the full admission packet: `uniprot:P12015`, `uniprot:Q93TJ5`, `uniprot:P23262`, `uniprot:P11295`, `uniprot:Q01740`, `uniprot:O15229`, `uniprot:P25535`, `uniprot:H3JQW0`, `uniprot:Q6F4M8`.

They are source-admissible acquisition leads, but still need source-free geometry, duplicate/leakage screening, terminal review, and factory/import gates before any countable support or registry action.

Control and rejected rows remain hard negatives or boundaries. The candidate scout found 22 hard-negative controls, 2 blocked wrong-chemistry rows, and 1 structure-check boundary row; these do not increase clean FMO support.

## Benchmark Impact

- Immediate Wave 1.1 impact: none. No metric, threshold, label, model, or production scoring changed.
- If `m_csa:551` and `m_csa:973` are later approved, clean FMO support rises from the two canonical rows (`m_csa:131`, `m_csa:132`) to four rows.
- Four rows remain below the proposed `n>=6` floor for primary reconsideration, so FMO remains secondary OOD/acquisition-target or later pilot-only.
- The hard-negative counteraxis is now available and should travel with the packet: ordinary flavin hydride transfer, flavin oxidase, Fe-S relay, flavodiiron NO reductase, radical flavin/Fe-S dehydratase, covalent FAD-adduct chemistry, heme oxygenase/P450/peroxidase, and non-flavin oxygenase/luciferase/metal controls.

## Guardrails

- No canonical label changes were made.
- No imports were run.
- No ontology edits, thresholds, model training, production scoring, registry edits, or countable metrics were created.
- Proposed candidates remain `requires_human_approval_before_registry_edit`.
