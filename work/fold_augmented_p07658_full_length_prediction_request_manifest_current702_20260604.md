# Fold-Augmented P07658 Full-Length Prediction Request Manifest - current702

Run: 2026-06-04T12:19:23Z

Exact input/acceptance manifest for the remaining P07658 Lever 3 full-length predicted-coordinate blocker. It stages no coordinate, scores no row, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_full_length_prediction_request_manifest_ready_blocker_not_cleared
- Entry: m_csa:562 / P07658
- Sequence length: 715
- Selenocysteine count: 1
- Sequence SHA-256: 3090cc03d7d9a4015e6607c7008d258d99b15b4dfec5db660eadfea94b8fe9fa
- Coordinates staged now: 0
- Fixed-threshold audit ready to rerun now: False
- Blockers: ['p07658_full_length_predicted_coordinate_not_returned_or_staged', 'provider_model_version_path_checksum_provenance_missing_until_coordinate_exists', 'fixed_threshold_audit_not_ready_to_rerun']

## FASTA

```fasta
>m_csa:562|P07658|full_length_715aa|selenocysteine_U_preserved|lever3_prediction_request
MKKVVTVCPYCASGCKINLVVDNGKIVRAEAAQGKTNQGTLCLKGYYGWDFINDTQILTP
RLKTPMIRRQRGGKLEPVSWDEALNYVAERLSAIKEKYGPDAIQTTGSSRGTGNETNYVM
QKFARAVIGTNNVDCCARVUHGPSVAGLHQSVGNGAMSNAINEIDNTDLVFVFGYNPADS
HPIVANHVINAKRNGAKIIVCDPRKIETARIADMHIALKNGSNIALLNAMGHVIIEENLY
DKAFVASRTEGFEEYRKIVEGYTPESVEDITGVSASEIRQAARMYAQAKSAAILWGMGVT
QFYQGVETVRSLTSLAMLTGNLGKPHAGVNPVRGQNNVQGACDMGALPDTYPGYQYVKDP
ANREKFAKAWGVESLPAHTGYRISELPHRAAHGEVRAAYIMGEDPLQTDAELSAVRKAFE
DLELVIVQDIFMTKTASAADVILPSTSWGEHEGVFTAADRGFQRFFKAVEPKWDLKTDWQ
IISEIATRMGYPMHYNNTQEIWDELRHLCPDFYGATYEKMGELGFIQWPCRDTSDADQGT
SYLFKEKFDTPNGLAQFFTCDWVAPIDKLTDEYPMVLSTVREVGHYSCRSMTGNCAALAA
LADEPGYAQINTEDAKRLGIEDEALVWVHSRKGKIITRAQVSDRPNKGAIYMTYQWWIGA
CNELVTENLSPITKTPEYKYCAVRVEPIADQRAAEQYVIDEYNKLKTRLREAALA
```

## Acceptance Checks

- coordinate_file_exists: required=True
- coordinate_sha256_recorded: required=True
- provider_model_version_recorded: required=True
- input_sequence_sha256_matches_manifest: required=True
- sequence_length_is_715: required=True
- selenocysteine_handling_documented: required=True
- experimental_pdb_metadata_not_used_as_deployment_input: required=True
- row_not_scored_until_coordinate_staged: required=True

## Decision

- Prediction request ready now: True
- Coordinate blocker cleared now: False
- Next gate: After a coordinate exists, run acceptance checks against this manifest; only then score P07658 at unchanged threshold 0.44155 with the already staged Q43088 sidecar.

## Interpretation

- P07658 remains blocked, but the exact full-length predictor input and acceptance checks are now frozen for the smallest next experiment.
- Run a full-length predictor/provider using this sequence, then stage the returned coordinate with provenance and rerun only the fixed-threshold row-scoring readiness checks.
