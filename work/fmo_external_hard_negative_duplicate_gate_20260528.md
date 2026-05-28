# FMO External Hard-Negative Duplicate Gate - 2026-05-28

Run time: 2026-05-28T04:12:00Z

Review-only gate for six external FMO acquisition candidates. No labels, registries, ontology files, thresholds, production scoring, model outputs, imports, or model-training artifacts were changed.

## Bottom Line

Three source-only candidates pass this hard-negative/duplicate screen as non-import-ready external leads:

- `uniprot:P12015` CHMO
- `uniprot:Q93TJ5` HAPMO
- `uniprot:Q01740` human FMO1

Three candidates are held:

- `uniprot:H3JQW0` OTEMO: `duplicate_hold`, preserving the prior terminal duplicate/leakage rejection.
- `uniprot:O15229` KMO: `duplicate_hold`, preserving the prior high-TM duplicate/leakage signal against canonical `m_csa:131`.
- `uniprot:P23262` salicylate 1-monooxygenase: `duplicate_hold`, because it is same-family aromatic hydroxylase support already covered by `m_csa:131` and proposed `m_csa:551`.

None are countable or import-ready from this gate.

## Controlling Context

Current canonical FMO rows are `m_csa:131` 4-hydroxybenzoate 3-monooxygenase and `m_csa:132` alkanal monooxygenase. Proposed review-only FMO support rows are `m_csa:551` phenol 2-monooxygenase and `m_csa:973` DszC protein.

The positive axis remains strict: reduced FAD/FMN plus O2 must form C4a-(hydro)peroxyflavin or equivalent flavin-peroxy oxygenating chemistry, followed by substrate oxygen insertion or oxygenation. Flavin presence, NAD(P)H, O2 use, oxidase names, hydroxylase names, or monooxygenase names are not enough.

## Candidate Decisions

| Priority | Candidate | New evidence row? | Duplicate/family overlap | Hard-negative separation | Disposition |
| --- | --- | --- | --- | --- | --- |
| 1 | `uniprot:P12015` CHMO | Yes, if later gates clear | New BVMO/lactone oxygen-insertion axis; same broad BVMO class as HAPMO/OTEMO only | Passes: FAD/NADPH BVMO oxygen insertion, not ordinary flavin redox or oxidase-only chemistry | `hard_negative_gate_pass` |
| 2 | `uniprot:H3JQW0` OTEMO | No for this gate | Same BVMO lane as CHMO/HAPMO; prior current-countable duplicate/leakage terminal rejection | Mechanism separates from hard negatives, but duplicate/leakage controls dominate | `duplicate_hold` |
| 3 | `uniprot:Q93TJ5` HAPMO | Yes, if later gates clear | Distinct HAPMO/aryl-ketone BVMO row, but not a separate diversity axis from BVMO alone | Passes: FAD/NADPH peroxyflavin ester-forming oxygen insertion | `hard_negative_gate_pass` |
| 4 | `uniprot:Q01740` human FMO1 | Yes, if later gates clear | New class B FMO N/S oxygenation lane; only partial reaction-type overlap with DszC sulfur oxygenation | Passes: FAD/NADPH C4a-hydroperoxyflavin N/S oxygenation, not P450/heme or generic flavin redox | `hard_negative_gate_pass` |
| 5 | `uniprot:O15229` KMO | No for this gate | Prior high-TM duplicate/leakage against `m_csa:131`; same broad aromatic hydroxylase lane | Mechanism separates from hard negatives, but duplicate/leakage controls dominate | `duplicate_hold` |
| 6 | `uniprot:P23262` salicylate 1-monooxygenase | No for this gate | Same-family aromatic hydroxylase support already represented by `m_csa:131` and `m_csa:551` | Mechanism separates from hard negatives, but family overlap makes it corroborative rather than new | `duplicate_hold` |

## Model Failure Modes To Preserve

- CHMO/HAPMO/OTEMO can be over-absorbed into `flavin_dehydrogenase_reductase` if a scorer keys on FAD/NADPH geometry and misses Baeyer-Villiger oxygen insertion.
- FMO1 can collapse into generic flavin redox if the model sees FAD/NADPH but not the C4a-hydroperoxyflavin N/S oxygenation contract.
- KMO already shows the failure mode: prior geometry scored top1 as `flavin_dehydrogenase_reductase` and found high-TM duplicate/leakage against `m_csa:131`.
- Salicylate 1-monooxygenase can be mistaken for generic FAD/NADH redox or counted as new when it mostly duplicates the existing aromatic hydroxylase lane.

## Hard-Negative Separation

All three pass candidates separate from:

- ordinary flavin hydride-transfer dehydrogenases/reductases
- flavin oxidases where O2 is only terminal acceptor
- Fe-S/flavin relays
- flavodiiron NO reductase
- radical flavin/Fe-S dehydratase
- covalent FAD-adduct chemistry
- heme/P450/peroxidases
- pterin, non-heme iron, copper, or other non-flavin oxygenases
- luciferase/ATP-dependent oxygenations
- name-only monooxygenase hits

The held candidates are held for duplicate/family overlap, not because they are rejected as non-FMO chemistry.

## Source Artifacts

- `artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
- `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json`
- `artifacts/v3_packet3_v2_sublabel_decision_closure_702_20260527.json`
- `artifacts/v3_fmo_source_evidence_scout_702_20260527.json`
- `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk002_rescue_20260521.json`

## Verification Targets

- JSON parse: `artifacts/v3_fmo_external_hard_negative_duplicate_gate_702_20260528.json`
- CLI validation: `PYTHONPATH=src python -m catalytic_earth.cli validate`
- Whitespace: `git diff --check`
