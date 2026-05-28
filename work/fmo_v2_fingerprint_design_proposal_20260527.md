# FMO V2 Fingerprint Design Proposal - 2026-05-27

This is proposal-only. No ontology, registry, label import, threshold, scoring, or training change was made.

## Recommendation

Keep `flavin_monooxygenase` as a secondary OOD probe and future acquisition target for now. Do not absorb it into `flavin_dehydrogenase_reductase`, and do not promote it to primary metrics until the evidence gate reaches at least `n>=6` clean, non-duplicate rows plus hard-negative controls.

Proposed future IDs:

- Family: `flavin_monooxygenase`
- Child candidate: `flavin.monooxygenase_c4a_peroxy_oxygen_insertion`
- Optional later split: `flavin.monooxygenase_two_component_fmnh2_oxygenation`

The child framing is useful if FMO stays under the broad flavin family during v2 work. The primary-family path should reopen only after count and negative-control gates are met.

## Evidence Contract

Future countable review should require these fields before any metric use:

- `flavin_cofactor`: FAD/FADH2 or FMN/FMNH2 must be in the oxygenating active-site chemistry, not only in a remote reductase partner.
- `oxygen_activation_intermediate`: source evidence for C4a-hydroperoxyflavin, C4a-peroxyflavin, or equivalent reduced-flavin plus O2 oxygenating intermediate.
- `substrate_oxygen_insertion`: the row must record substrate, product, and O2-derived oxygen insertion such as hydroxylation, N-oxygenation, S-oxygenation, or Baeyer-Villiger insertion.
- `reductive_activation_context`: NADPH/NADH, partner reductase, or pre-reduced flavin context should be recorded when relevant; reductase activity alone is not FMO evidence.
- `active_site_residues`: record residue IDs and roles when known, but do not use a motif-only rule because FMO subclasses are not residue-identical.
- `structural_state_caveats`: flag holo/apo state, flavin-bound state, substrate/product/analog state, mobile flavin conformations, missing residues, and two-component partner state.
- `source_independence_and_leakage`: mechanism curation sources must be separated from model features, and future benchmark rows need duplicate/leakage review.

## Current Context

The 2026-05-27 closure has two canonical `flavin_monooxygenase` rows: `m_csa:131` and `m_csa:132`. It also identifies two clean future candidates currently labelled under `flavin_dehydrogenase_reductase`: `m_csa:551` phenol 2-monooxygenase and `m_csa:973` DszC protein.

Those four rows are useful context, not a metric set. Even if `m_csa:551` and `m_csa:973` are later expert-accepted, the support would be four clean rows, still short of the proposed `n>=6` floor and still missing hard-negative separation.

After the initial inventory, FMO status/blocker artifacts appeared at `artifacts/v3_fmo_acquisition_sprint_integrated_status_702_20260527.json` and `artifacts/v3_fmo_admission_gate_and_benchmark_impact_702_20260527.json`. They support the same design conclusion: four review-supportable FMO signals, zero import-ready rows, and missing named-family lanes. They are context only for this proposal.

A later geometry artifact appeared at `artifacts/v3_fmo_structure_geometry_audit_702_20260527.json`. It adds review-only structural caveats: `m_csa:551` has FAD plus phenol/IPH context but no NADPH or peroxyflavin state and needs visual pose review; `m_csa:973` has an FMN active-site residue cluster but no substrate/analog or peroxyflavin state; `m_csa:141` is structurally flavin/heme redox; `m_csa:128` has no flavin ligand.

## Exclusion Rules

Exclude ordinary flavin dehydrogenases, reductases, and oxidases when the chemistry is hydride transfer to flavin, terminal O2 reoxidation, peroxide formation, or water-derived oxygen without substrate oxygen insertion. `m_csa:141` is the local control example.

Exclude flavin/Fe-S electron-relay systems, radical flavin or flavin/Fe-S enzymes, radical dehydratases, heme oxygenases and P450s, pterin/metal/copper/diiron oxygenases, and non-flavin luciferase or ATP-adenylate oxygenations. Also exclude name-only monooxygenase or hydroxylase hits.

## Benchmark Policy

Allowed now:

- Secondary OOD probe
- Canary for over-absorption into generic flavin reductase
- Proposal-only evidence contract

Not allowed now:

- Primary supervised metric
- Production scoring
- Threshold tuning
- Label import
- Canonical child registry entry

After `n>=6` clean positives and explicit hard-negative review, a pilot-only child evaluation can be designed with expert approval. Future primary promotion should wait for clean positives, hard negatives, duplicate/leakage review, and expert sign-off.

## Acquisition Priorities

1. Expert-review `m_csa:551` for FAD/NADPH/O2, C4a-hydroperoxyflavin, phenol hydroxylation, and structural state.
2. Expert-review `m_csa:973` for FMNH2/O2, C4a-hydroperoxyflavin, sulfur oxygenation, two-component reductase context, and the residue-391 source discrepancy.
3. Source cyclohexanone monooxygenase or other BVMO rows with explicit flavin-peroxy Baeyer-Villiger insertion.
4. Source HAPMO and related aromatic ketone monooxygenases.
5. Source IucD-class lysine N6 hydroxylase or other clean flavin N-hydroxylases.
6. Source FMO1/FMO3/FMO5 or dimethylaniline-like N/S oxygenation rows with structure support.
7. Source salicylate 1-monooxygenase, tryptophan 2-monooxygenase, and related aromatic hydroxylases only with explicit flavin C4a-peroxy evidence.
8. Revisit prior external candidates KMO, UBII, OTEMO, and nitrophenol/nitrocatechol monooxygenase only after source-free geometry, duplicate/leakage, terminal review, and import gates.
9. Build the hard-negative control packet across ordinary flavin hydride transfer, Fe-S electron relay, radical flavin/Fe-S, heme oxygenase/P450, non-flavin oxygenase, and name-only monooxygenase cases.

## Source Artifacts

- `artifacts/v3_packet3_v2_sublabel_decision_closure_702_20260527.json`
- `artifacts/v3_flavin_monooxygenase_acquisition_closure_702_20260527.json`
- `artifacts/v3_flavin_monooxygenase_acquisition_packet_702_20260527.json`
