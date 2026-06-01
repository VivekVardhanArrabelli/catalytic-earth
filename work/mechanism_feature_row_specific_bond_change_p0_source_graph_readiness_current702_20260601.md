# Mechanism Feature Row-Specific Bond-Change P0 Source-Graph Readiness - current702

Run: 2026-06-01T18:33:09Z

No-fit source-graph readiness audit for the balanced P0 row-specific bond-change pilot seed queue. It checks frozen local graph context only and does not extract mechanism text, materialize bond-change events, mutate the feature contract, or fit a model.

## Status

- p0_source_graph_context_ready_bond_events_not_structured
- Balanced P0 seed rows: 15
- M-CSA entry nodes present: 15
- Mechanism text present rows: 15
- Catalytic residue edge rows: 15
- Rhea mapping present rows: 11
- Structured bond-change ready rows: 0
- Manual extraction required rows: 15
- Blocker counts: {'rhea_reaction_mapping_missing': 4, 'structured_bond_change_events_missing': 15}

## Row Readiness

- m_csa:5 (ser_his_acid_hydrolase): source_context_present_structured_bond_events_missing; residues=5, mechanism_text=1, rhea=0, blockers=rhea_reaction_mapping_missing, structured_bond_change_events_missing
- m_csa:6 (flavin_dehydrogenase_reductase): source_context_present_structured_bond_events_missing; residues=7, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:11 (metal_dependent_hydrolase): source_context_present_structured_bond_events_missing; residues=11, mechanism_text=1, rhea=0, blockers=rhea_reaction_mapping_missing, structured_bond_change_events_missing
- m_csa:15 (metal_dependent_hydrolase): source_context_present_structured_bond_events_missing; residues=8, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:16 (metal_dependent_hydrolase): source_context_present_structured_bond_events_missing; residues=5, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:37 (heme_peroxidase_oxidase): source_context_present_structured_bond_events_missing; residues=7, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:66 (plp_dependent_enzyme): source_context_present_structured_bond_events_missing; residues=4, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:68 (flavin_dehydrogenase_reductase): source_context_present_structured_bond_events_missing; residues=4, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:94 (ser_his_acid_hydrolase): source_context_present_structured_bond_events_missing; residues=5, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:102 (flavin_dehydrogenase_reductase): source_context_present_structured_bond_events_missing; residues=3, mechanism_text=2, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:124 (heme_peroxidase_oxidase): source_context_present_structured_bond_events_missing; residues=14, mechanism_text=1, rhea=0, blockers=rhea_reaction_mapping_missing, structured_bond_change_events_missing
- m_csa:133 (heme_peroxidase_oxidase): source_context_present_structured_bond_events_missing; residues=6, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing
- m_csa:147 (plp_dependent_enzyme): source_context_present_structured_bond_events_missing; residues=6, mechanism_text=1, rhea=3, blockers=structured_bond_change_events_missing
- m_csa:169 (ser_his_acid_hydrolase): source_context_present_structured_bond_events_missing; residues=5, mechanism_text=1, rhea=0, blockers=rhea_reaction_mapping_missing, structured_bond_change_events_missing
- m_csa:186 (plp_dependent_enzyme): source_context_present_structured_bond_events_missing; residues=3, mechanism_text=1, rhea=1, blockers=structured_bond_change_events_missing

## Interpretation

- The balanced P0 seed rows have local M-CSA graph context, mechanism-text links, and catalytic-residue edges, but the frozen graph does not expose structured row-specific bond-change event edges. Rhea reaction mappings are present for the subset with local EC-to-Rhea coverage.
- Use this readiness audit to drive manual/source-backed extraction of row-specific reaction participant mappings and bond-change events; do not add the feature to the train/cal contract until a source-backed sidecar and strict audit exist.
