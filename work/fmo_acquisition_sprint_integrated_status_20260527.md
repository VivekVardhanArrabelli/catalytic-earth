# FMO Acquisition Sprint Integrated Status - 2026-05-27

Generated: 2026-05-28T02:40:26Z

This is a review-only integration of the current FMO acquisition sprint evidence. It changes no canonical label registries, ontology IDs, fingerprint IDs, thresholds, production scoring, imports, model outputs, representation artifacts, artifact migration state, or artifact storage state.

All requested evidence inputs are present in this rerun:

- `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json` - present
- `artifacts/v3_fmo_source_evidence_scout_702_20260527.json` - present
- `artifacts/v3_fmo_structure_geometry_audit_702_20260527.json` - present
- `artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json` - present
- `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json` - present
- `artifacts/v3_fmo_admission_gate_and_benchmark_impact_702_20260527.json` - present
- `artifacts/v3_wave1_1_diagnostic_benchmark_result_702_20260527.json` - present

No discovered FMO evidence lane remains missing. A few upstream lane artifacts were generated before all sibling lanes landed and may contain local missing-artifact notes; this integrated status uses the current files and hashes above as the controlling lane status.

## Direct Answers

1. Clean FMO support currently stands at **four review-supportable signals**: existing canonical `m_csa:131` and `m_csa:132`, plus local proposed `m_csa:551` and `m_csa:973`. New countable/import-ready FMO rows: **zero**.
2. Rows counted for readiness support: `m_csa:131`, `m_csa:132`, `m_csa:551`, `m_csa:973`. Only `m_csa:131` and `m_csa:132` are existing canonical FMO rows. `m_csa:551` and `m_csa:973` are human-review proposals, not automatic labels.
3. We did **not** reach `n>=6` clean support. The exact gap is **two additional non-duplicate clean FMO rows** that clear source-free materialization/geometry, duplicate/leakage, hard-negative, terminal review, and human/import-gate checks.
4. `m_csa:551` and `m_csa:973` are ready for a **human review/import-review packet only**. They remain blocked from import or canonical relabel by human approval, current `flavin_dehydrogenase_reductase` labels, the `n>=6` gap, hard-negative separation, and row-specific structure/v2 caveats.
5. External source-only candidates to materialize/geometry-check next: start with `uniprot:P12015`, `uniprot:H3JQW0`, and `uniprot:Q93TJ5`, then `uniprot:Q01740`, `uniprot:O15229`, and `uniprot:P23262`. Medium-confidence follow-ups are `uniprot:P11295`, `uniprot:P25535`, and `uniprot:Q6F4M8` after source-strengthening where needed.
6. Hard-negative controls are required across ordinary flavin hydride transfer, flavin oxidase O2 acceptors, flavin/Fe-S relay, flavodiiron NO reductase, radical flavin/Fe-S dehydratase, covalent FAD-adduct chemistry, heme/P450/peroxidase oxygenases, and non-flavin oxygenases/luciferases/metals/pterins/copper.
7. Exact next action: **human review packet** for `m_csa:551` and `m_csa:973`. Run external geometry/materialization as the next acquisition lane after or in parallel. Do not do primary promotion, v2 split, automatic import, or no-go.

## Support Rows

| Row | Current status | Why it supports FMO review | Import state |
| --- | --- | --- | --- |
| `m_csa:131` | Existing canonical FMO | 4-hydroxybenzoate 3-monooxygenase; FAD-dependent aromatic hydroxylase | No change |
| `m_csa:132` | Existing canonical FMO | Alkanal monooxygenase; FMN-linked oxygenation | No change |
| `m_csa:551` | Proposed local candidate | Phenol 2-monooxygenase; NADPH-reduced FAD plus O2 forms C4a-hydroperoxyflavin before phenol hydroxylation | Human review only, not import-ready |
| `m_csa:973` | Proposed local candidate | DszC; FMNH2 plus dioxygen forms C4a-hydroperoxyflavin before sulfur oxygenation | Human review only, not import-ready |

`m_csa:551` structure status: PDB `1FOH`, FAD and phenol/IPH present, geometry supports FMO. Caveats: no NADPH/NADP ligand, no captured C4a-hydroperoxy/peroxide state, and mapped-chain FAD C4X-to-phenol/IPH distance needs structure review because shorter substrate poses occur in other coordinate copies.

`m_csa:973` structure status: PDB `3X0Y`, FMN C4A sits near Tyr96, Ser163, and His391, compatible with an oxygenation pocket. Caveats: no substrate/analog, no NADPH/NADP ligand, no C4a-hydroperoxy/peroxide state, and the v2 audit conflict requires human adjudication.

## External Source-Only Candidates

These rows are source-reviewed acquisition leads only. They do not count toward clean support until materialization/geometry, duplicate/leakage, hard-negative, terminal review, and import gates clear.

| Priority | Row | Candidate | Confidence | Current disposition |
| --- | --- | --- | --- | --- |
| 1 | `uniprot:P12015` | cyclohexanone monooxygenase | high | source-only, not counted |
| 2 | `uniprot:H3JQW0` | OTEMO | high | source-only, not counted |
| 3 | `uniprot:Q93TJ5` | 4-hydroxyacetophenone monooxygenase | high | source-only, not counted |
| 4 | `uniprot:Q01740` | FMO1 / dimethylaniline monooxygenase | high | source-only, not counted |
| 5 | `uniprot:O15229` | kynurenine 3-monooxygenase | high | source-only, not counted |
| 6 | `uniprot:P23262` | salicylate hydroxylase / salicylate 1-monooxygenase | high | source-only, not counted |
| 7 | `uniprot:P11295` | L-lysine N6-monooxygenase / IucD | medium | source-only, not counted |
| 8 | `uniprot:P25535` | 2-octaprenylphenol hydroxylase / UbiI | medium | source-only, not counted |
| 9 | `uniprot:Q6F4M8` | 4-nitrophenol / 4-nitrocatechol monooxygenase oxygenase component | medium | source-only, not counted |


Boundary external signal not counted as a clean packet row: `uniprot:P06617` tryptophan 2-monooxygenase, because explicit reductive activation and C4a oxygen-transfer evidence remain insufficient.

## Blocked Or Rejected Rows

- `m_csa:109`: boundary monooxygenase-like signal in the v2 audit; not clean FMO support now.
- `m_csa:141`: hydroxylating dehydrogenase with hydride transfer to FAD and water-derived oxygen; keep as flavin redox control.
- `m_csa:128`: ATP/luciferyl-adenylate oxygenation without flavin support.
- `m_csa:133`: P450 heme monooxygenase.
- `m_csa:134`: tetrahydrobiopterin/non-heme iron hydroxylase.
- `m_csa:135`: copper-dependent monooxygenase.
- `m_csa:600`: soluble methane monooxygenase metal chemistry.
- `m_csa:768`: luciferin monooxygenase without clean flavin C4a-peroxy support.
- `m_csa:977`: flavin halogenase boundary; oxygen activation routes to halogenation rather than substrate oxygen insertion.
- `m_csa:781`: local lysine N6 string false positive; transferase chemistry, not IucD-class hydroxylation.

## Hard-Negative Controls

- `ordinary_flavin_hydride_transfer_dehydrogenase_reductase`: `m_csa:3`, `m_csa:6`, `m_csa:353`, `m_csa:381`, `m_csa:506`, `m_csa:892`, `m_csa:141`
- `flavin_oxidase_o2_acceptor_not_monooxygenase`: `m_csa:109`, `m_csa:110`, `m_csa:113`, `m_csa:354`, `m_csa:822`, `m_csa:852`, `m_csa:895`
- `flavin_fe_s_relay_hcar_like`: `m_csa:990`, `m_csa:108`, `m_csa:114`, `m_csa:142`, `m_csa:294`, `m_csa:800`
- `flavodiiron_no_reductase`: `m_csa:497`
- `radical_flavin_fe_s_dehydratase`: `m_csa:750`
- `covalent_fad_adduct_aps_reductase_like`: `m_csa:123`
- `heme_oxygenases_p450_peroxidases_not_fmo`: `m_csa:133`, `m_csa:699`, `m_csa:795`, `m_csa:601`
- `nonflavin_oxygenases_luciferases_metal_pterin_copper_not_fmo`: `m_csa:128`, `m_csa:129`, `m_csa:130`, `m_csa:134`, `m_csa:135`, `m_csa:600`, `m_csa:768`, `m_csa:977`, `m_csa:781`, `m_csa:930`

These controls protect against false FMO calls from flavin presence alone, NAD(P)H language, oxidase/O2 acceptor wording, monooxygenase names, heme/P450 oxygenation, metal/pterin/copper oxygenation, and source-only family names.

## V2 And Benchmark Impact

The v2 proposal remains evidence-contract material only. Proposed future child ideas such as `flavin.monooxygenase_c4a_peroxy_oxygen_insertion` and `flavin.monooxygenase_two_component_fmnh2_oxygenation` are not registry changes and are not ready for metric use.

Wave 1.1 diagnostic evidence supports review design, not import: geometry supports 17/17 near-orphan rows and rescues 4/4 wrong-Foldseek-transfer rows, while Foldseek makes 4/4 unsafe wrong-transfer calls in that failure slice. Existing learned representation tracks remain limited/underpowered for this decision.

## Decision

Proceed with a human review/import-review packet for `m_csa:551` and `m_csa:973`. Keep both rows as `proposed_candidate_requires_human_approval`, keep all hard negatives separate, and continue external materialization/geometry acquisition to close the two-row support gap before any primary promotion or v2 split.
