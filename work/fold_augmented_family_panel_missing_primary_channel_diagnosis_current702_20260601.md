# Fold-Augmented Family-Panel Missing Primary-Channel Diagnosis - current702

Run: 2026-06-01T09:55:09Z

Review-only diagnosis for family-panel rows missing the primary combined geometry plus predicted-fold channel. It checks whether frozen current702 geometry and fold scores already exist in upstream artifacts before requesting new runtime work.

## Status

- missing_primary_channel_diagnosis_ready_review_only
- Diagnosed rows: 10
- Rows with predicted geometry evidence: 0
- Rows with train/cal fold score: 0
- Rows with heldout fold score: 0
- Diagnosis counts: {'needs_source_backed_row_sidecar_and_coordinate_materialization': 10}

## Diagnosed Rows

| rank | row | panel | blockers | diagnosis | geometry | fold score | next action |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 2 | secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 3 | external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 4 | mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 5 | mh_064 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 6 | mh_065 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 7 | mh_066 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 8 | mh_067 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 9 | mh_068 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |
| 10 | mh_072 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing, predicted_structure_fold_tm_missing | needs_source_backed_row_sidecar_and_coordinate_materialization | None:None | None:None | create a source-backed row sidecar with accession and coordinate materialization scope before geometry or fold scoring |

## Interpretation

- 0 queued rows already have a frozen fold score upstream; the rest need geometry, sidecar, or fold-lookup materialization.
- m_csa:973 is no longer in the missing primary-channel queue, consistent with the family-panel readout consuming its frozen train/calibration fold score.
- Work the remaining missing rows by first repairing current702 M-CSA predicted geometry, then materializing source-backed sidecars for secondary and external rows.

## Guardrails

- Review-only diagnosis. No labels, registries, ontologies, imports, thresholds, training data, production scoring, source fetching, or Foldseek/TM recomputation changed.
