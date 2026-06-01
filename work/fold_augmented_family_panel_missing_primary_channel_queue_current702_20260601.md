# Fold-Augmented Family-Panel Missing Primary-Channel Queue - current702

Run: 2026-06-01T09:11:44Z

Review-only materialization queue for family-panel rows that lack either predicted geometry or predicted-structure fold evidence needed by the primary combined channel.

## Status

- missing_primary_channel_queue_ready_review_only
- Missing primary-channel rows: 12
- M-CSA rows: 2
- Secondary-probe rows: 2
- External or placeholder rows: 8
- Score blocker counts: {'predicted_geometry_top1_score_missing': 12, 'predicted_structure_fold_tm_missing': 12}

## Queue

| rank | row | panel | blockers | next action |
| ---: | --- | --- | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | materialize row-level secondary-probe sidecar, accession, geometry, and predicted coordinate before scoring |
| 2 | secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | materialize row-level secondary-probe sidecar, accession, geometry, and predicted coordinate before scoring |
| 3 | m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | repair or materialize predicted active-site geometry, then rerun predicted-fold lookup if the row becomes ok predicted geometry |
| 4 | external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 5 | m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | repair or materialize predicted active-site geometry, then rerun predicted-fold lookup if the row becomes ok predicted geometry |
| 6 | mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 7 | mh_064 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 8 | mh_065 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 9 | mh_066 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 10 | mh_067 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 11 | mh_068 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 12 | mh_072 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |

## Interpretation

- 12 family-panel rows lack the primary geometry+predicted-fold channel.
- Start with current702 M-CSA rows that need predicted-geometry repair, then handle secondary-probe and external placeholder rows through source-backed sidecars.

## Guardrails

- Review-only queue. No labels, registries, ontologies, imports, thresholds, training data, source fetching, or production scoring changed.
