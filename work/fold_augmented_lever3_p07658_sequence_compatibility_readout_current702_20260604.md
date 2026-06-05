# Fold-Augmented Lever 3 P07658 Sequence Compatibility Readout - current702

Run: 2026-06-05T01:25:07Z

Lever 3 measured P07658 sequence-compatibility readout. It checks the frozen full-length sequence contract, classifies allowed versus rejected U140 handling policies, and composes the credential/local route and local inventory evidence without generating coordinates, scoring rows, or changing threshold 0.44155.

## Status

- fold_augmented_lever3_p07658_sequence_compatibility_readout_no_compatible_route
- Sequence contract valid: True
- Current evidence sufficient for deployment closure: False
- Fixed-threshold audit ready to rerun now: False

## Sequence Contract

- Expected length: 715
- Expected SHA-256: 3090cc03d7d9a4015e6607c7008d258d99b15b4dfec5db660eadfea94b8fe9fa
- Dispatch FASTA SHA-256: 3090cc03d7d9a4015e6607c7008d258d99b15b4dfec5db660eadfea94b8fe9fa
- Expected U positions: [140]
- Dispatch U positions: [140]
- Dispatch FASTA matches manifest: True

## Operating Point Context

- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204

## Sequence Policies

| policy | acceptable closure input | available now | reason |
| --- | ---: | ---: | --- |
| submit_exact_full_length_u_preserved_sequence | True | False | The manifest and dispatch FASTA preserve the exact 715-aa P07658 sequence with U140; closure still needs a route that returns a coordinate and filled provenance. |
| provider_internal_u140_handling_documented | True | False | A provider may internally normalize or model selenocysteine only if the submitted input hash still matches the frozen manifest and provenance documents U140 handling. |
| submit_u140_mutated_sequence | False | False | Submitting a mutated sequence would fail the frozen input sequence-hash and U140-position acceptance checks. |
| truncate_or_split_715aa_sequence | False | False | Truncation or fragment stitching would no longer measure the full-length deployment row and is rejected by the sequence length/hash contract. |
| use_experimental_pdb_or_pdb_provider_mapping | False | False | Experimental PDB shortcuts and provider=PDB repository rows are explicitly disallowed deployment inputs for this gate. |
| deterministic_missing_coordinate_abstention | False | True | Fail-closed abstention is operationally safe when no predicted coordinate exists, but it cannot prove fold/chemistry confounded separation or authorize the fixed-threshold rerun. |

## Route Evidence

- Routes attempted: 6
- Exact-sequence submitted routes: 5
- Sequence modified or truncated routes: 0
- Credential/auth denial routes: 3
- Provider routes with credentials: 0
- Local predictor modules present: 0
- Local coordinate candidates: 0
- Local filled provenance candidates: 0

## Acceptance Gate Matrix

- Required gates passed: 3/7
- Required gate failures: ['credentialed_or_local_exact_prediction_route_available', 'preferred_full_length_coordinate_present', 'filled_prediction_provenance_present', 'local_inventory_ready_for_acceptance_preflight']
- All-or-abstain action now: abstain_or_route_novel_oos_until_coordinate_provenance_exists

| gate | passed | action if failed | evidence |
| --- | ---: | --- | --- |
| train_cal_operating_point_context_available | True | abstain_or_route_novel_oos | A train/cal-selected operating point must be available before any fixed-threshold rerun can be interpreted. |
| p07658_sequence_contract_preserved | True | abstain_or_route_novel_oos | The submitted FASTA must match the frozen 715-aa P07658 input hash and U140 position. |
| provider_dispatch_packet_ready | True | abstain_or_route_novel_oos | The provider-neutral dispatch packet must have all required operator inputs before a coordinate run is requested. |
| credentialed_or_local_exact_prediction_route_available | False | abstain_or_route_novel_oos | At least one credentialed provider route or local predictor must accept the exact full-length sequence. |
| preferred_full_length_coordinate_present | False | abstain_or_route_novel_oos | The returned full-length coordinate must exist at the preferred staging path before row scoring. |
| filled_prediction_provenance_present | False | abstain_or_route_novel_oos | Provider/model/version/path/checksum/input-sequence/U140 provenance must be filled before acceptance. |
| local_inventory_ready_for_acceptance_preflight | False | abstain_or_route_novel_oos | Coordinate and provenance files must both be present before the P07658 acceptance preflight is rerun. |

## Decision

- Missing-coordinate abstention safe but not closure: True
- Sequence mutation or truncation allowed now: False
- Exact missing evidence needed: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Do not mutate or truncate U140 and do not use experimental PDB shortcuts. Run exactly one credentialed/local full-length prediction route, fill provenance, and rerun acceptance preflight.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, or secret values changed.
- Critical violations: 0

## Interpretation

- The frozen P07658 sequence contract is valid, but no compatible exact full-length prediction route is available now.
- The manifest and dispatch FASTA preserve the 715-aa sequence with U140, 0 credentialed/local routes are available, 0 local coordinate/provenance candidates are present, and mutation, truncation, split prediction, or experimental-PDB shortcuts remain rejected. The all-or-abstain gate fails until an exact route, coordinate, and filled provenance are present.
- Provision exactly one full-length predictor route; if the provider internally handles U140, record that handling in provenance while keeping the submitted sequence hash fixed.
