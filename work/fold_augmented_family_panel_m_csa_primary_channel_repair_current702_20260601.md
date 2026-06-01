# Fold-Augmented Family-Panel M-CSA Primary-Channel Repair - current702

Run: 2026-06-01T09:44:14Z

Review-only primary-channel repair for family-panel M-CSA rows diagnosed as missing predicted geometry. It applies frozen current702 accession-repair policies, then parses Foldseek/TM scores against the predicted in-distribution atlas.

## Status

- m_csa_primary_channel_repair_scored_review_only
- Target rows: 2
- Predicted-geometry ok rows: 2
- Foldseek hits: 2
- Primary-channel score-complete rows: 2
- Repair policy counts: {'best_real_sequence_accession_by_active_site_coverage': 1, 'manifest_accession_compatible_residue_subset': 1}
- Research-gate status counts if readout is refreshed: {'nonabstained_at_research_threshold': 2}

## Row Scores

| row | repair policy | accession | geometry top1 | geometry score | nearest atlas | atlas fingerprint | TM | combined | fixed gate |
| --- | --- | --- | --- | ---: | --- | --- | ---: | ---: | --- |
| m_csa:116 | manifest_accession_compatible_residue_subset | Q2RSB2 | metal_dependent_hydrolase | 0.3734 | m_csa:727 | metal_dependent_hydrolase | 0.5417 | 0.45755 | nonabstained_at_research_threshold |
| m_csa:132 | best_real_sequence_accession_by_active_site_coverage | P07740 | ser_his_acid_hydrolase | 0.3894 | m_csa:120 | flavin_dehydrogenase_reductase | 0.6879 | 0.53865 | nonabstained_at_research_threshold |

## Interpretation

- 2/2 M-CSA missing-channel rows now have repaired predicted geometry plus nearest-atlas Foldseek/TM scores.
- Refresh the family-panel evidence packets and fold-augmented family-panel readout so these repaired rows leave the missing primary-channel queue; keep all decisions review-only.

## Guardrails

- Review-only repair. No labels, registries, ontologies, imports, thresholds, training data, model weights, or production scoring changed.
- AlphaFoldDB coordinates were transient runtime inputs; raw coordinate files are not committed.
