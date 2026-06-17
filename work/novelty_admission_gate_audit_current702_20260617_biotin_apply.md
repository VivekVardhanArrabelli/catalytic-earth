# Novelty / Saturation Admission Gate

Run: 2026-06-17T19:17:50Z

An online, non-destructive filter that sits AFTER the exact accession/sequence-SHA screen and admits incoming candidates only when they add diversity -- closing the near-duplicate / lane-saturation gap the governor measured. Writes no registry; emits no labels.

## Policy

- Cluster key: (fingerprint_or_scope, full_ec, organism, sequence_length_bin).
- Per-cluster cap 3; floor 100; cap ceiling 250; hole threshold 25.
- post exact-dedup gate: hole/under-floor admit unless redundant ortholog; over-cap reject unless new reaction; balanced/OOS admit only on novelty, throttle saturated clusters.

## Retrospective self-audit (existing expansion replayed through the gate)

- Expansion rows: 8067.
- Decisions: {'admit': 7606, 'reject': 47, 'throttle': 414}.
- Would NOT re-admit (redundant under policy): 461 (0.0571).
- Reasons: {'adds_diversity': 3241, 'closes_hole_fingerprint': 1066, 'closes_under_floor_fingerprint': 3289, 'fingerprint_over_cap_no_new_chemistry': 47, 'needed_fingerprint_but_redundant_ortholog': 15, 'over_cap_but_new_reaction_chemistry': 10, 'redundant_no_novelty_signal': 399}.
- Non-admit concentration by scope: {'out_of_scope': 373, 'metal_dependent_hydrolase': 71, 'heme_peroxidase_oxidase': 10, 'alpha_beta_hydrolase_esterase_lipase': 5, 'plp_dependent_enzyme': 2}.

## Usage

- feed an engine preview's applied_labels through evaluate_batch against build_diversity_state(frozen, expansion); apply only the ADMIT set via apply-external-annotation-anchored-import.

## Guardrails

- Frozen benchmark written: False.
- Labels emitted: 0.
- The gate is advisory; the authorized apply step is what writes.
