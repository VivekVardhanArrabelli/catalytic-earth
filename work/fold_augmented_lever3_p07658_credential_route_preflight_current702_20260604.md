# Fold-Augmented Lever 3 P07658 Credential-Route Preflight - current702

Run: 2026-06-05T00:11:42Z

Lever 3 measured preflight for the next exact P07658 prediction experiment. It checks whether this runtime has a credentialed provider route or local full-length predictor module available, records only env-var presence, and generates no coordinates.

## Status

- fold_augmented_lever3_p07658_credential_route_preflight_no_route
- Operating-point readout available: True
- Credentialed/local exact route available now: False
- Ready to run exact P07658 prediction now: False

## Operating Context

- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204
- P07658 coordinate gap cleared now: False

## Provider Routes

| route | credential present | env vars checked |
| --- | ---: | --- |
| huggingface_router_esmfold | False | HF_TOKEN, HUGGINGFACEHUB_API_TOKEN, HUGGING_FACE_HUB_TOKEN |
| nvidia_nim_esmfold | False | NVIDIA_API_KEY, NVIDIA_NIM_API_KEY |
| biolm_esmfold | False | BIOLM_API_KEY, BIOLM_TOKEN |

## Local Runtime

| module | predictor candidate | available |
| --- | ---: | ---: |
| esm | True | False |
| openfold | True | False |
| chai_lab | True | False |
| boltz | True | False |
| alphafold | True | False |
| colabfold | True | False |
| torch | False | True |

## Counts

- Credential env vars present: 0/7
- Provider routes with credentials: 0/3
- Local predictor modules present: 0/6
- Torch available: 1
- Disk free GiB: 13.39
- Disk guardrail above 10 GiB: True

## Decision

- Fixed-threshold audit ready to rerun now: False
- Remaining missing evidence: ['one credentialed provider route or one local full-length predictor runtime', 'accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun', 'credentialed or local exact full-length P07658 predicted coordinate with provider/model/version/path/checksum and U140 provenance']
- Smallest next experiment: Provision exactly one credentialed provider route (HF_TOKEN, NVIDIA_API_KEY, or BIOLM_API_KEY) or install one local predictor runtime that can handle the frozen 715-aa P07658 sequence with U140 provenance.
- Next gate: Provision a credentialed/local route before more no-credential retries.

## Guardrails

- Env-var presence only; no secret values, coordinates, row scores, labels, thresholds, imports, heldout tuning, or experimental-PDB shortcuts changed.

## Interpretation

- This runtime has no credentialed/local exact P07658 prediction route.
- 0/3 credentialed provider routes and 0/6 local predictor modules are available now.
- Provision a single credentialed/provider or local predictor route before attempting P07658 again; do not truncate or mutate U140.
