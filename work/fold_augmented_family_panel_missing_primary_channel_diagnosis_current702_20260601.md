# Fold-Augmented Family-Panel Missing Primary-Channel Diagnosis - current702

Run: 2026-06-02T19:15:31Z

Review-only diagnosis for family-panel rows missing the primary combined geometry plus predicted-fold channel. It checks whether frozen current702 geometry and fold scores already exist in upstream artifacts before requesting new runtime work.

## Status

- missing_primary_channel_diagnosis_ready_review_only
- Diagnosed rows: 5
- Rows with predicted geometry evidence: 0
- Rows with train/cal fold score: 0
- Rows with heldout fold score: 0
- Rows with source-backed fold score: 5
- Diagnosis counts: {'source_backed_fold_scored_needs_predicted_geometry': 5}

## Diagnosed Rows

| rank | row | panel | blockers | diagnosis | geometry | fold score | next action |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | predicted_geometry_top1_score_missing | source_backed_fold_scored_needs_predicted_geometry | None:None | family_panel_source_backed_afdb_vs_predicted_atlas:0.4655 | materialize a source-free predicted active-site geometry sidecar for this review-only row before primary-channel readout |
| 2 | external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing | source_backed_fold_scored_needs_predicted_geometry | None:None | family_panel_source_backed_afdb_vs_predicted_atlas:0.6259 | materialize a source-free predicted active-site geometry sidecar for this review-only row before primary-channel readout |
| 3 | mh_064 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | source_backed_fold_scored_needs_predicted_geometry | None:None | family_panel_source_backed_afdb_vs_predicted_atlas:0.9222 | materialize a source-free predicted active-site geometry sidecar for this review-only row before primary-channel readout |
| 4 | mh_065 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | source_backed_fold_scored_needs_predicted_geometry | None:None | family_panel_source_backed_afdb_vs_predicted_atlas:0.9411 | materialize a source-free predicted active-site geometry sidecar for this review-only row before primary-channel readout |
| 5 | mh_072 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | source_backed_fold_scored_needs_predicted_geometry | None:None | family_panel_source_backed_afdb_vs_predicted_atlas:0.5936 | materialize a source-free predicted active-site geometry sidecar for this review-only row before primary-channel readout |

## Interpretation

- All 5 queued rows now have frozen or source-backed fold scores; the remaining primary-channel blocker is source-free predicted active-site geometry.
- m_csa:973 is no longer in the missing primary-channel queue, consistent with the family-panel readout consuming its frozen train/calibration fold score.
- Materialize source-free predicted active-site geometry sidecars for the source-backed fold-scored rows, starting with Q59490, A0A1M6T2I7, and Q6NSJ0.

## Guardrails

- Review-only diagnosis. No labels, registries, ontologies, imports, thresholds, training data, production scoring, source fetching, or Foldseek/TM recomputation changed.
