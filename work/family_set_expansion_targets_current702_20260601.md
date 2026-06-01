# Family-Set Expansion Targets - current702

Run: 2026-06-01T02:16:04Z

Targeted family-set expansion proposal to de-risk the current 8-fingerprint bound by increasing no_reliable_structure, near_orphan, confounded-OOS, FMO/flavin-redox boundary, radical/cobalamin/Fe-S, and dark-bin support without padding dense structural neighborhoods.

## Guardrails

- Proposal only. No labels, registries, ontologies, imports, promotions, thresholds, or heldout splits changed.

## Target Families

| Family | Priority bins | Candidate rows | Expected eval impact |
| --- | --- | --- | --- |
| glycyl_radical_or_thiamine_radical_lyase_boundary | cofactor_confounded_oos, near_orphan, dark_bin | m_csa:30, m_csa:31 | adds confounded-OOS controls that reuse known cofactors but should abstain from occupied hydrolase/redox families |
| thiol_disulfide_oxidoreductase_isomerase_boundary | cofactor_confounded_oos, FMO_flavin_redox_boundary | m_csa:191 | tests redox chemistry that can look cofactor-like without matching flavin/heme occupied loci |
| lipoamide_or_sulfur_transfer_redox_boundary | cofactor_confounded_oos, radical_cobalamin_FeS | m_csa:267, m_csa:448 | adds hard OOS controls for known-cofactor leakage and Fe-S/sulfur chemistry |
| flavin_monooxygenase_and_flavin_oxygen_transfer | FMO_flavin_redox_boundary, near_orphan, no_reliable_structure | m_csa:131, m_csa:132, m_csa:551, m_csa:973 | separates flavin oxygen-transfer from flavin dehydrogenase/reductase without promoting FMO prematurely |
| cobalamin_and_radical_rearrangement_panel | radical_cobalamin_FeS, dark_bin, no_reliable_structure | secondary_probe::cobalamin_radical_rearrangement, secondary_probe::radical_sam_enzyme, m_csa:750 | widens the 8-fingerprint bound into radical/cobalamin/Fe-S chemistry where current labels are sparse |
| no_reliable_structure_metal_hydrolase_controls | no_reliable_structure, dark_bin | mh_064, mh_065, mh_066, mh_067, mh_068, mh_072 | increases no_reliable_structure positive and hard-negative support without padding dense structural neighborhoods |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | near_orphan, confounded_OOS, dark_bin | m_csa:10, m_csa:116, mh_073, external_glycoside_panel | adds near-orphan OOS controls that stress hydrolase boundary calls without dense-neighborhood padding |

## Human Validation

- expert mechanism-locus review
- source-backed M-CSA/Swiss-Prot/Rhea provenance
- duplicate and train/test leakage screen
- coordinate or predicted-structure materialization feasibility
- label-factory gate and future frozen split before any countable use
