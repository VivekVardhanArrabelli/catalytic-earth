# Predicted-Structure Fold Channel Contract Audit - current702

Run: 2026-06-01T07:38:02Z

Strict contract audit for the existing AlphaFoldDB-predicted Foldseek/TM channel: verify that the scored all-heldout and priority cofactor-confounded rows match frozen current702 inputs.

## Status

- fold_channel_contract_passed_current702
- Heldout ok rows: 126
- All-heldout nearest hits: 126
- Priority confounded rows: 6
- Priority nearest hits: 6
- Critical violation counts: {'status_violations': 0, 'count_mismatches': 0, 'duplicate_all_heldout_hit_ids': 0, 'duplicate_priority_hit_ids': 0, 'missing_all_heldout_hit_ids': 0, 'extra_all_heldout_hit_ids': 0, 'missing_priority_hit_ids': 0, 'extra_priority_hit_ids': 0, 'missing_fold_signal_row_score_ids': 0, 'extra_fold_signal_row_score_ids': 0, 'score_range_violations': 0, 'source_mismatches': 0, 'guardrail_mismatches': 0, 'unexpected_blockers': 0, 'command_violations': 0, 'missing_result_files': 0}

## Foldseek Result Files

- all_heldout_vs_atlas: exists=True, lines=11297, hits=126
- priority_cofactor_confounded_oos_vs_atlas: exists=True, lines=402, hits=6

## Contract

- Expected fold-channel status: computed_all_heldout_foldseek_scores
- Allowed computed blockers: predicted_coordinate_files_missing_for_all_heldout_scope, predicted_coordinate_files_missing_for_priority_scope
- This audit validates the scored artifact without changing labels, registries, thresholds, or imports.

## Interpretation

- The real predicted-structure fold channel satisfies the strict current702 scoring contract: all ok heldout rows and all six priority cofactor-confounded OOS rows have parsed nearest-atlas Foldseek/TM hits, with only persistent coordinate-file provenance listed as an allowed blocker.
- Use this as the validation layer for downstream fold-augmented gate work; persistent CIF provenance remains optional research infrastructure, not a scoring blocker.
