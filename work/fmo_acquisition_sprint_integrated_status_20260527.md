# FMO Acquisition Sprint Integrated Status - 2026-05-27

This is a review-only integration of the available flavin monooxygenase
acquisition evidence. It does not change canonical label registries, ontology
IDs, fingerprint IDs, thresholds, production scoring, imports, model outputs,
representation artifacts, artifact migration state, or artifact storage state.

Late-arriving `artifacts/v3_fmo_*_20260527.json` outputs were folded in:

- `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json`
- `artifacts/v3_fmo_source_evidence_scout_702_20260527.json`
- `artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json`
- `artifacts/v3_fmo_structure_geometry_audit_702_20260527.json`
- `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json`
- `artifacts/v3_fmo_admission_gate_and_benchmark_impact_702_20260527.json`

No discovered `v3_fmo_*_20260527.json` lane remains missing.

## Direct Answers

- Clean FMO support currently stands at four total review-supportable rows:
  existing canonical `m_csa:131` and `m_csa:132`, plus proposed
  `m_csa:551` and `m_csa:973`.
- Additional clean candidates beyond `m_csa:131` and `m_csa:132`: two
  (`m_csa:551`, `m_csa:973`).
- Target reached for at least four additional clean rows beyond `m_csa:131`
  and `m_csa:132`: no. The sprint is short by two additional clean rows.
- New countable/import-ready FMO rows: zero.
- Source-reviewed external candidates: nine, but they are source-only and not
  counted until source-free geometry, duplicate/leakage, terminal review,
  hard-negative, and import gates clear.
- Exact next decision: assemble a human review/import-review packet for
  `m_csa:551` and `m_csa:973` only. They remain not import-ready and require
  human approval before any registry change. Do not open primary promotion or a
  v2 split yet.

## Clean Rows

| Row | Status | Evidence | Blocker |
| --- | --- | --- | --- |
| `m_csa:131` | Existing canonical FMO | 4-hydroxybenzoate 3-monooxygenase; FAD-dependent aromatic hydroxylase | Keep as secondary/OOD probe outside primary metrics until the family is stronger |
| `m_csa:132` | Existing canonical FMO | Alkanal monooxygenase; FMN-linked oxygenation | Clean but not a named BVMO/cyclohexanone row |
| `m_csa:551` | `proposed_candidate_requires_human_approval` | Phenol 2-monooxygenase; NADPH-reduced FAD plus O2 forms C4a-hydroperoxyflavin before phenol hydroxylation | Currently labeled `flavin_dehydrogenase_reductase`; needs expert approval, target count, and hard-negative separation |
| `m_csa:973` | `proposed_candidate_requires_human_approval` | DszC protein; FMNH2 plus dioxygen forms C4a-hydroperoxyflavin before sulfur oxygenation | Currently labeled `flavin_dehydrogenase_reductase`; v2 audit grouped it under generic flavin hydride/oxidase, so adjudication is required |

Structure/cofactor checks refine the two proposed rows:

- `m_csa:551`: PDB `1FOH`, local and structure cofactor families both
  `flavin`, FAD and phenol/IPH present. Geometry supports FMO, but the selected
  coordinate lacks NADPH/NADP and a C4a-hydroperoxy state, and the mapped-chain
  FAD C4X-to-phenol/IPH distance needs structure review.
- `m_csa:973`: PDB `3X0Y`, local and structure cofactor families both
  `flavin`, FMN C4A is near Tyr96, Ser163, and His391. The structure is
  FMO-compatible but ambiguous because no substrate/analog, NADPH/NADP, or
  C4a-hydroperoxy/peroxide state is present.

## Blocked Or Rejected

- `m_csa:109`: boundary monooxygenase-like signal in the v2 audit, but not
  accepted as clean FMO support in the acquisition closure.
- `m_csa:141`: hydroxylating dehydrogenase with hydride transfer to FAD and
  water-derived oxygen; overlaps flavin reductase/dehydrogenase, not clean FMO.
- `m_csa:128`: ATP/luciferyl-adenylate oxygenation without flavin support.
- `m_csa:133`: P450 heme monooxygenase.
- `m_csa:134`: tetrahydrobiopterin/non-heme iron hydroxylase.
- `m_csa:135`: copper-dependent monooxygenase.
- `m_csa:600`: soluble methane monooxygenase metal chemistry.
- `m_csa:768`: luciferin monooxygenase without clean flavin C4a-peroxy support.
- External frozen candidates `uniprot:O15229`, `uniprot:P25535`,
  `uniprot:H3JQW0`, and `uniprot:Q6F4M8`: the source scout now treats these as
  source-reviewed FMO candidates, but they still lack source-free
  geometry/control/import gates.
- New source-reviewed external candidates `uniprot:P12015`, `uniprot:Q93TJ5`,
  `uniprot:P23262`, `uniprot:P11295`, and `uniprot:Q01740`: preserve for a
  future evidence packet, but do not count them as supportable clean rows yet.
- `uniprot:P06617`: boundary tryptophan 2-monooxygenase source signal; not a
  clean FMO packet row in this run.

Named-family lanes moved from absent to source-reviewed-but-not-gated for
BVMO/cyclohexanone monooxygenase, HAPMO, IucD-class lysine N6 hydroxylase,
salicylate 1-monooxygenase, and FMO1/dimethylaniline-like chemistry.
Tryptophan 2-monooxygenase remains boundary/not clean for this packet.

## Hard Negatives To Keep Separate

Keep the following controls separate from FMO and from generic
`flavin_dehydrogenase_reductase` collapse:

- `m_csa:141`, `m_csa:128`, `m_csa:133`, `m_csa:134`, `m_csa:135`,
  `m_csa:600`, and `m_csa:768` for non-FMO oxygenase boundary chemistry.
- `m_csa:497` and `m_csa:750` as primary flavin readthrough-excluded
  boundary/OOS controls.
- Candidate scout controls: `m_csa:977`, `m_csa:781`, `m_csa:130`,
  `m_csa:930`, `m_csa:699`, `m_csa:935`, `m_csa:109`, `m_csa:809`,
  `m_csa:978`, `m_csa:129`, `m_csa:34`, `m_csa:37`, `m_csa:547`,
  `m_csa:583`, `m_csa:672`, `m_csa:743`, `m_csa:795`, and `m_csa:936`.
- Counteraxis groups: ordinary flavin hydride transfer (`m_csa:3`,
  `m_csa:6`, `m_csa:353`, `m_csa:381`, `m_csa:506`, `m_csa:892`),
  flavin oxidase O2 acceptors (`m_csa:109`, `m_csa:110`, `m_csa:113`,
  `m_csa:354`, `m_csa:822`, `m_csa:852`, `m_csa:895`), flavin/Fe-S relay
  (`m_csa:990`, `m_csa:108`, `m_csa:114`, `m_csa:142`, `m_csa:294`,
  `m_csa:800`), `m_csa:497`, `m_csa:750`, covalent FAD-adduct `m_csa:123`,
  heme oxygenases/P450/peroxidases (`m_csa:133`, `m_csa:699`, `m_csa:795`,
  `m_csa:601`), and non-flavin oxygenase/luciferase/metal/pterin/copper rows
  (`m_csa:128`, `m_csa:129`, `m_csa:130`, `m_csa:134`, `m_csa:135`,
  `m_csa:600`, `m_csa:768`).
- `flavin.dehydrogenase_oxidase_hydride_transfer` as a demoted mixed-chemistry
  v2 child label. It must be split before any metric use and must not absorb
  FMO rows.

## V2 And Benchmark Impact

Packet 3 leaves the FMO boundary as a future acquisition target, not a pilot or
canonical child label. The late v2 proposal is useful as an evidence contract,
not a registry change. It proposes future child candidates
`flavin.monooxygenase_c4a_peroxy_oxygen_insertion` and
`flavin.monooxygenase_two_component_fmnh2_oxygenation`, but keeps
`flavin_monooxygenase` as a secondary OOD probe until at least `n>=6` clean
positives, hard-negative controls, duplicate/leakage review, and expert
approval are available.

Required future evidence fields are flavin cofactor, oxygen activation
intermediate, substrate oxygen insertion, reductive activation context,
active-site residues, structural-state caveats, and source
independence/leakage separation.

Wave 1.1 benchmark evidence is useful only for review design: geometry rescues
17/17 near-orphan rows and 4/4 wrong-Foldseek-transfer rows, while Foldseek
makes 4/4 unsafe wrong-transfer calls in that failure slice. No countable
metric or import decision follows from this diagnostic benchmark.

The finalized admission-gate artifact is complete and review-only:
`m_csa:551` and `m_csa:973` are ready for a human review packet, zero rows are
import-ready, registry edits are not allowed, and primary promotion is not
ready.

## Next Decision

Assemble the human review/import-review packet for `m_csa:551` and
`m_csa:973`, both marked `proposed_candidate_requires_human_approval`.
Continue acquisition in parallel: source-reviewed external candidates need
source-free structure/geometry, duplicate/leakage, terminal review, and
import-gate checks before they can count toward the remaining two clean rows.
