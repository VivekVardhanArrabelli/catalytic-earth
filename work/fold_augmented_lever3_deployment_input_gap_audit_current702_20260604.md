# Fold-Augmented Lever 3 Deployment Input Gap Audit - current702

Run: 2026-06-05T00:11:42Z

Lever 3 measured deployment-input gap audit. It separates the accepted operating-point evidence from the remaining P07658 predicted-coordinate input gates, uses only existing source-free readouts and preflights, and does not score rows or create coordinates.

## Status

- fold_augmented_lever3_deployment_input_gap_audit_ready_p07658_inputs_only
- Operating point usable for hard-confounded train/cal routing: True
- Deployment input gap isolated to P07658: True
- Fixed-threshold audit ready to rerun now: False

## Operating Point

- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204
- Hard-confounded residuals closed: True

## P07658 Input Gates

| gate | satisfied | evidence |
| --- | ---: | --- |
| lever3_operating_point_counteraxis_contracts | True | 31/34 calibration in-scope retained and 105/204 train/cal OOS abstained. |
| p07658_dispatch_inputs | True | 4/4 dispatch inputs present. |
| p07658_exact_prediction_route | False | 0/3 credentialed provider routes, 0/6 local predictor modules, and 0 routes returning coordinates now. |
| p07658_candidate_coordinate_file | False | Candidate coordinate exists: False. |
| p07658_candidate_prediction_provenance | False | Candidate provenance exists: False. |
| p07658_acceptance_preflight | False | 1/8 acceptance checks passed. |

## Counts

- Input gates satisfied: 2/6
- Acceptance checks passed: 1/8
- Credentialed provider routes: 0/3
- Local predictor modules present: 0/6
- Provider routes returning coordinates now: 0

## Decision

- Route-equivalent no-credential retries should stop: True
- Missing input gates: ['p07658_exact_prediction_route', 'p07658_candidate_coordinate_file', 'p07658_candidate_prediction_provenance', 'p07658_acceptance_preflight']
- Exact missing evidence needed: ['one credentialed provider route or one local full-length predictor runtime', 'exact full-length P07658 predicted coordinate file', 'provider/model/version/path/checksum, sequence-hash, and U140 provenance', 'P07658 acceptance preflight with all required checks passing']
- Smallest next experiment: Provision exactly one credentialed provider route (HF_TOKEN, NVIDIA_API_KEY, or BIOLM_API_KEY) or install one local predictor runtime that can handle the frozen 715-aa P07658 sequence with U140 provenance.
- Next gate: Provision one credentialed/local exact P07658 route, write coordinate/provenance, and rerun acceptance preflight.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, or secret values changed.
- Critical violations: 0

## Interpretation

- Lever 3 operating-point evidence is deployment-valid for hard-confounded train/cal routing; full closure is isolated to P07658 input provenance.
- 2/6 deployment input gates are satisfied; 1/8 P07658 acceptance checks pass.
- P07658 lacks an available exact prediction route, returned coordinate file, filled provenance, and passing acceptance preflight.
- Stop no-credential route-equivalent retries and perform the single credentialed/local P07658 prediction experiment named by the dispatch packet.
