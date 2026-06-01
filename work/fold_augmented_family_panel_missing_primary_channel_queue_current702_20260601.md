# Fold-Augmented Family-Panel Missing Primary-Channel Queue - current702

Run: 2026-06-01T15:02:09Z

Review-only materialization queue for family-panel rows that lack either predicted geometry or predicted-structure fold evidence needed by the primary combined channel.

## Status

- missing_primary_channel_queue_ready_review_only
- Missing primary-channel rows: 7
- M-CSA rows: 0
- Secondary-probe rows: 1
- External or placeholder rows: 6
- Score blocker counts: {'predicted_geometry_top1_score_missing': 7}

## Queue

| rank | row | panel | blockers | next action |
| ---: | --- | --- | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | predicted_geometry_top1_score_missing | materialize row-level secondary-probe sidecar, accession, geometry, and predicted coordinate before scoring |
| 2 | external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | predicted_geometry_top1_score_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 3 | mh_064 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 4 | mh_065 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 5 | mh_067 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 6 | mh_068 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |
| 7 | mh_072 | no_reliable_structure_metal_hydrolase_controls | predicted_geometry_top1_score_missing | create source-backed external row sidecar and coordinate materialization plan before any scoring or family decision |

## Interpretation

- 7 family-panel rows lack the primary geometry+predicted-fold channel.
- No M-CSA rows remain in this queue; continue with the secondary probe row and external placeholder rows that still need approved source-free locator sidecars before predicted-geometry scoring.

## Guardrails

- Review-only queue. No labels, registries, ontologies, imports, thresholds, training data, source fetching, or production scoring changed.
