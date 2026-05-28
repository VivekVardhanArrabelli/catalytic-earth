# FMO Local Candidate Adjudication - 551 and 973

Status: `complete_review_only_no_imports`. Generated at `2026-05-28T03:49:12Z`.

No canonical labels, registries, ontology files, thresholds, production scoring, model outputs, or imports were changed. This run stopped after the local closure artifact and did not start external acquisition.

## Decision Table

| candidate | mechanism clean | coordinate clean | coordinate fix required | accepted for clean-support readiness | import ready | registry edit allowed |
| --- | --- | --- | --- | --- | --- | --- |
| `m_csa:551` phenol 2-monooxygenase | true | true for productive 1FOH chain C copy | true | true | false | false |
| `m_csa:973` DszC protein | true | false | false | true | false | false |

## `m_csa:551` Phenol 2-Monooxygenase

Decision: mechanism-clean FMO support. NADPH/NADP absence and missing C4a-peroxyflavin are expected structural-state caveats, not disqualifiers.

Coordinate adjudication: the prior mapped chain A has FAD C4X-to-IPH O1 at 7.10 A, so future pocket extraction should not use that copy. The local 1FOH coordinate contains a productive copy on author chain C: FAD label_asym `I` auth_seq_id `801`, IPH label_asym `J` auth_seq_id `802`, FAD C4X-to-IPH O1 distance `4.582 A`. Chain D corroborates the productive pose at `4.649 A`.

Active-site coordinate completeness proxy for chain C is clean from local atom_site evidence: Asp54, Arg281, Tyr289, and Pro364 have all expected non-hydrogen atoms present, occupancy 1.00, no alternate location IDs, and B-factor ranges consistent with resolved coordinates. No density map was inspected, so this is a coordinate-completeness proxy rather than a map-density claim.

Exact caveats:

- Future pocket extraction must use author chain C rather than prior mapped chain A.
- No NADPH/NADP ligand is present; structural-state caveat only.
- No C4a-hydroperoxy/peroxide flavin state is present; structural-state caveat only.
- No relabel, import, registry edit, ontology edit, threshold change, production scoring change, model-output change, or countable FMO promotion is allowed in this closure.

Exact next action: record pdb:1FOH author chain C as the productive copy for future pocket extraction, with chain D as corroborating geometry only. Do not relabel or import.

## `m_csa:973` DszC Protein

Decision: mechanism-clean two-component FMNH2 sulfur monooxygenase support. NADPH/NADP absence is not a blocker because the reductase partner supplies reduced FMNH2.

Coordinate adjudication: keep `coordinate_clean=false`. The selected 3X0Y coordinate lacks substrate/substrate analog and C4a-hydroperoxy/peroxide flavin state, so those remain coordinate-state caveats.

Residue-391 discrepancy: local 3X0Y atom_site evidence resolves auth residue 391 as HIS in every polymer chain A-H, with 10 His391 atoms per chain, full expected non-hydrogen atom coverage, occupancy 1.00, no alternate location IDs, and no CYS at auth_seq_id 391. The acquisition packet text is internally inconsistent because it lists His391 but later says Cys391. With no contrary local primary source, classify this as `structure_resolved_His391_source_text_typo_pending_external_source_check`.

Exact caveats:

- No substrate or substrate analog is present in the selected coordinate.
- No C4a-hydroperoxy/peroxide flavin state is present in the selected coordinate.
- NADPH/NADP absence is not a blocker for DszC because FMNH2 is supplied by a reductase partner.
- Do not count the coordinate as clean until the residue-391 discrepancy is explicitly closed by external primary-source check or retained as a terminal caveat.
- No relabel, import, registry edit, ontology edit, threshold change, production scoring change, model-output change, or countable FMO promotion is allowed in this closure.

Exact next action: carry `m_csa:973` forward as mechanism-clean support in the review packet, retain `coordinate_clean=false`, and defer the external primary-source check or terminal-caveat decision to a later run. Do not relabel or import.

## Output Artifact

Machine-readable closure artifact:

- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
