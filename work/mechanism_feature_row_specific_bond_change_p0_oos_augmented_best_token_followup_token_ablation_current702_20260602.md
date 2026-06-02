# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Token Ablation - current702

Run: 2026-06-02T12:28:23Z

Calibration-only follow-up single-token ablation over the remaining retained OOS rows after the best-token residual contract. Each candidate token is added on top of the frozen best-token train/cal surface, guardrail-audited, and scored without reading heldout.

## Status

- p0_oos_augmented_best_token_followup_token_ablation_ready
- Remaining retained OOS rows: 8
- Candidate tokens scored: 309
- Tokens beating best-token residual contract: 54
- Baseline best-token OOS abstain recall: 0.714286
- Baseline best-token residual AUC: 0.776786
- Critical violations: 0

## Top Follow-Up Token Ablations

| token | OOS abstain recall | residual AUC | recall delta | AUC delta |
| --- | ---: | ---: | ---: | ---: |
| residue_code_count:his=3 | 0.857143 | 0.875 | 0.142857 | 0.098214 |
| residue_role_count:metal_ligand=3 | 0.857143 | 0.857143 | 0.142857 | 0.080357 |
| residue_code_count:glu=2 | 0.821429 | 0.830357 | 0.107143 | 0.053571 |
| residue_role_present:electrostatic_stabiliser | 0.821429 | 0.821429 | 0.107143 | 0.044643 |
| event_participant_arity:proton_transfer|before_3|after_3|delta_0 | 0.785714 | 0.883929 | 0.071428 | 0.107143 |
| event_residue_role_count:electron_transfer|metal_ligand=1 | 0.785714 | 0.883929 | 0.071428 | 0.107143 |
| residue_code_count:gln=1 | 0.785714 | 0.883929 | 0.071428 | 0.107143 |
| residue_code_count:his=2 | 0.785714 | 0.883929 | 0.071428 | 0.107143 |
| residue_code_count:tyr=1 | 0.785714 | 0.839286 | 0.071428 | 0.0625 |
| event_residue_code_count:proton_transfer|his=1 | 0.785714 | 0.830357 | 0.071428 | 0.053571 |
| participant_role_count:catalytic_residue=5 | 0.785714 | 0.830357 | 0.071428 | 0.053571 |
| residue_code_count:asn=1 | 0.785714 | 0.830357 | 0.071428 | 0.053571 |
| event_residue_role:proton_transfer|metal_ligand | 0.785714 | 0.821429 | 0.071428 | 0.044643 |
| event_residue_role_count:proton_transfer|metal_ligand=1 | 0.785714 | 0.821429 | 0.071428 | 0.044643 |
| residue_role_present:proton_acceptor | 0.785714 | 0.821429 | 0.071428 | 0.044643 |
| residue_role_present:proton_donor | 0.785714 | 0.821429 | 0.071428 | 0.044643 |
| event_residue_code_count:proton_transfer|asp=1 | 0.785714 | 0.803571 | 0.071428 | 0.026785 |
| residue_code_count:asp=2 | 0.785714 | 0.803571 | 0.071428 | 0.026785 |
| participant_role_count:substrate=3 | 0.75 | 0.883929 | 0.035714 | 0.107143 |
| residue_role_present:hydrogen_bond_acceptor | 0.75 | 0.875 | 0.035714 | 0.098214 |

## Decision

- Follow-up token replaces best-token contract: True
- Best follow-up token: residue_code_count:his=3
- Best follow-up OOS abstain recall: 0.857143
- Best follow-up residual AUC: 0.875
- Keep best-token residual threshold: False
- Next gate: Materialize the best follow-up token pair through a durable train/cal sidecar and explicit calibration contract before any heldout read.

## Interpretation

- At least one follow-up token beats the best-token calibration residual operating point.
- Use an explicit follow-up calibration contract gate before any heldout read.
