# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Expanded Token Ablation - current702

Run: 2026-06-02T11:26:28Z

Calibration-only single-token ablation for retained-OOS candidate feature tokens. Each token is added as one sanitized boolean feature to the coarse train/cal sidecar, guardrail-audited, and scored with the existing no-template centroid/residual method; heldout remains unread.

## Status

- p0_oos_augmented_expanded_token_ablation_ready
- Candidate tokens scored: 80
- Tokens beating coarse residual contract: 33
- Coarse residual OOS abstain recall: 0.5
- Coarse residual AUC: 0.669643
- Critical violations: 0

## Top Token Ablations

| token | OOS abstain recall | residual AUC | recall delta | AUC delta |
| --- | ---: | ---: | ---: | ---: |
| event_residue_role:proton_transfer|electrostatic_stabiliser | 0.714286 | 0.776786 | 0.214286 | 0.107143 |
| residue_code_count:his=3 | 0.642857 | 0.758929 | 0.142857 | 0.089286 |
| residue_role_present:proton_acceptor | 0.642857 | 0.741071 | 0.142857 | 0.071428 |
| residue_role_present:proton_donor | 0.642857 | 0.741071 | 0.142857 | 0.071428 |
| participant_role_count:catalytic_residue=5 | 0.642857 | 0.732143 | 0.142857 | 0.0625 |
| residue_role_count:metal_ligand=3 | 0.642857 | 0.732143 | 0.142857 | 0.0625 |
| residue_role_count:hydrogen_bond_donor=2 | 0.607143 | 0.696429 | 0.107143 | 0.026786 |
| residue_role_present:electrostatic_stabiliser | 0.607143 | 0.696429 | 0.107143 | 0.026786 |
| event_type_present:proton_transfer | 0.607143 | 0.6875 | 0.107143 | 0.017857 |
| residue_role_present:hydrogen_bond_acceptor | 0.571429 | 0.794643 | 0.071429 | 0.125 |
| residue_code_count:his=2 | 0.571429 | 0.776786 | 0.071429 | 0.107143 |
| event_mapped_residue_bucket:proton_transfer|five_plus | 0.571429 | 0.723214 | 0.071429 | 0.053571 |
| event_residue_role:proton_transfer|hydrogen_bond_acceptor | 0.571429 | 0.705357 | 0.071429 | 0.035714 |
| event_residue_role:proton_transfer|hydrogen_bond_donor | 0.571429 | 0.705357 | 0.071429 | 0.035714 |
| event_participant_arity:proton_transfer|before_1|after_1|delta_0 | 0.571429 | 0.6875 | 0.071429 | 0.017857 |
| participant_role_count:product=1 | 0.571429 | 0.669643 | 0.071429 | 0.0 |
| participant_role_count:substrate=3 | 0.535714 | 0.8125 | 0.035714 | 0.142857 |
| residue_role_count:covalently_attached=1 | 0.535714 | 0.75 | 0.035714 | 0.080357 |
| event_residue_code:proton_transfer|his | 0.535714 | 0.741071 | 0.035714 | 0.071428 |
| residue_role_present:hydrogen_bond_donor | 0.535714 | 0.741071 | 0.035714 | 0.071428 |

## Decision

- Single-token expansion replaces frozen residual contract: True
- Best token: event_residue_role:proton_transfer|electrostatic_stabiliser
- Best token residual OOS abstain recall: 0.714286
- Best token residual AUC: 0.776786
- Keep existing residual threshold: False
- Next gate: Materialize the best beating token as a durable train/cal sidecar and write an explicit calibration contract before any heldout read.

## Interpretation

- At least one retained-OOS token beats the coarse residual operating point on calibration OOS abstention while preserving or improving residual AUC.
- Promote only the top token through a durable calibration contract gate; do not read heldout yet.
