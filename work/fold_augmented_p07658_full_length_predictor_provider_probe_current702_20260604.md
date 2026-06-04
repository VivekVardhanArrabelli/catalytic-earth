# Fold-Augmented P07658 Full-Length Predictor Provider Probe - current702

Run: 2026-06-04T10:18:36Z

Credential-free provider-access probe for full-length sequence predictors after SWISS-MODEL, secondary accession, and public ESMFold checks left P07658 blocked. It uses the exact 715-residue UniProt sequence, stages no coordinates, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_full_length_predictor_provider_probe_blocked_auth_or_access
- Providers probed: 2
- Coordinates returned: 0
- Blockers: ['full_length_predictor_requires_credentials_or_access', 'p07658_predicted_coordinate_not_staged', 'fixed_threshold_audit_not_ready_to_rerun']

## Provider Probes

| provider | endpoint | status | result |
| --- | --- | ---: | --- |
| BioLM ESMFold | https://biolm.ai/api/v3/esmfold/predict/ | 401 | Authentication credentials were not provided. |
| OpenProtein ESMFold | https://api.openprotein.ai/api/v1/fold/models/esmfold | 403 | RBAC: access denied |

## Decision

- Credential-free provider clears P07658 now: False
- Smallest next experiment: Run an approved full-length predictor with available credentials/local runtime, capable of the exact 715-residue P07658 sequence including selenocysteine, then stage the coordinate with provider/model/version/path/checksum provenance.

## Interpretation

- Credential-free full-length provider probing cannot clear P07658: BioLM requires authentication and OpenProtein denies access.
- Provision or choose an approved full-length predictor/runtime, then rerun only the P07658 coordinate staging path with exact sequence provenance.
