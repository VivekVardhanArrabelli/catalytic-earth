# Fold-Augmented P07658 Prediction Provenance Template - current702

Run: 2026-06-04T12:38:57Z

Provider-fillable provenance template for the P07658 full-length predicted coordinate acceptance preflight. This template stages no coordinate, scores no row, and changes no threshold.

## Status

- fold_augmented_p07658_prediction_provenance_template_ready_unfilled
- Affected row: `m_csa:562` / P07658
- Sequence length: 715
- Selenocysteine positions: 140
- Input sequence SHA-256: `3090cc03d7d9a4015e6607c7008d258d99b15b4dfec5db660eadfea94b8fe9fa`
- Provider-ready FASTA: `work/fold_augmented_p07658_full_length_prediction_input_current702_20260604.fasta`
- Preferred coordinate path: `artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/p07658_full_length_predictor_current702_20260604.cif`

## Required Fill Fields

| field | requirement |
| --- | --- |
| provider | Prediction provider name |
| model_name_or_id | Model name or identifier |
| model_version | Model version |
| run_timestamp_utc | UTC timestamp of the prediction run |
| coordinate_path | Path to the generated mmCIF/PDB coordinate |
| coordinate_sha256 | SHA-256 of the generated coordinate file |
| input_sequence_sha256 | Must match the frozen manifest SHA-256 |
| input_sequence_length | Must equal 715 |
| selenocysteine_handling | Must explicitly document position 140 U handling |
| experimental_pdb_metadata_used_as_deployment_input | Must be false |

## Next Action

Run an approved full-length predictor on the frozen P07658 sequence, fill `artifacts/v3_fold_augmented_p07658_prediction_provenance_template_current702_20260604.json`, save the filled copy as `artifacts/v3_fold_augmented_p07658_prediction_provenance_filled_current702_20260604.json`, then rerun the P07658 acceptance preflight before any staging or fixed-threshold readout.
