# FMO External Hard-Negative Duplicate Gate - 2026-05-28

Review-only gate for the current external FMO acquisition candidates. No labels, registries, ontology files, thresholds, production scoring, model outputs, or imports were changed.

## Inputs

- `artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
- `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json`
- `artifacts/v3_packet3_v2_sublabel_decision_closure_702_20260527.json`
- Supporting context: `artifacts/v3_fmo_source_evidence_scout_702_20260527.json` and prior FMO deep-packet terminal decisions for `H3JQW0` and `O15229`.
- Current UniProt REST lookup for `P12015,H3JQW0,Q93TJ5,Q01740,O15229,P23262` at `2026-05-28T04:10:21Z`.

## Decision Table

| Priority | Candidate | Mechanism signal | Current-row duplicate/family overlap | Main failure mode | Disposition |
| --- | --- | --- | --- | --- | --- |
| 1 | `uniprot:P12015` CHMO | FAD/NADPH BVMO; cyclohexanone to epsilon-caprolactone; FAD-4a-OOH/peroxyflavin support | Not duplicate of `m_csa:131`, `132`, `551`, or `973`; adds missing BVMO cyclic-ketone lactonization | Geometry/model sees only FAD/NADPH fold and absorbs into generic flavin redox | `hard_negative_gate_pass` |
| 2 | `uniprot:H3JQW0` OTEMO | FAD/NADPH BVMO lactonization of OT-CoA | Source chemistry is true FMO, but prior full-current screen marked terminal duplicate/leakage; same broad BVMO lane as CHMO/HAPMO | Prior source-free geometry top-ranked `flavin_dehydrogenase_reductase`; high-TM leakage to current OOS `m_csa:246` | `duplicate_hold` |
| 3 | `uniprot:Q93TJ5` HAPMO | FAD/NADPH aromatic-ketone BVMO; ester-forming oxygen insertion | Not duplicate of current rows; same broad external BVMO axis as CHMO but distinct HAPMO named family | Geometry/model may collapse ester-forming BVMO into generic FAD/NADPH oxidoreductase | `hard_negative_gate_pass` |
| 4 | `uniprot:Q01740` human FMO1 | Class B FAD/NADPH FMO; N/S oxygenation | Partial oxygenation-class overlap with `m_csa:973`, but not duplicate: single-chain class B FMO vs two-component FMNH2 DszC | No reviewed PDB in current lookup; generic FAD/NADPH motifs can dominate without N/S oxygenation product evidence | `hard_negative_gate_pass` |
| 5 | `uniprot:O15229` KMO | FAD/NADPH kynurenine hydroxylation | Prior targeted current-FMO screen found high-TM duplicate/leakage to canonical `m_csa:131` (`pdb:1DOC`, max pair TM 0.8122) | Prior geometry top-ranked `flavin_dehydrogenase_reductase` and kept FMO lane below floor | `duplicate_hold` |
| 6 | `uniprot:P23262` salicylate 1-monooxygenase | FAD/NADH salicylate oxidative decarboxylation to catechol | Clean but same-family aromatic hydroxylase support already covered by `m_csa:131` and `m_csa:551` | NADH/FAD aromatic hydroxylase may look like ordinary flavin redox or oxidase unless C4a-hydroperoxyflavin/product evidence is required | `duplicate_hold` |

## Hard-Negative Separation

All six candidates have source support for flavin-dependent oxygen insertion and are not rejected as non-FMO chemistry. None should be treated as oxidase-only, Fe-S/flavin relay, flavodiiron NO reductase, radical flavin/Fe-S dehydratase, covalent FAD adduct chemistry, heme/P450/peroxidase, pterin/non-heme iron/copper oxygenase, ATP/luciferase oxygenation, or name-only monooxygenase.

The holds are therefore duplicate/leakage holds, not chemistry rejections:

- `H3JQW0`: true BVMO source chemistry, but prior terminal duplicate/leakage evidence blocks use as a new row.
- `O15229`: true FMO source chemistry, but prior high-TM duplicate/leakage to `m_csa:131` blocks use as a new row.
- `P23262`: true FMO source chemistry, but same-family aromatic hydroxylase support already represented by current rows.

## Bottom Line

`P12015`, `Q93TJ5`, and `Q01740` are the only candidates that pass this hard-negative duplicate gate as genuinely new future review leads. They remain source-only and not import-ready. `H3JQW0`, `O15229`, and `P23262` should not be counted as new evidence rows in this gate.
