# Fold-Augmented Lever 3 Descriptor Generalization Counteraxis Readout - current702

Run: 2026-06-05T05:12:02Z

Lever 3 measured descriptor-generalization counteraxis readout. It selects a source-free pocket descriptor/count rule on train/cal same-family OOS design rows while explicitly excluding the retained descriptor-present application rows, then applies the selected rule to those excluded rows. It changes no thresholds, scores no new rows, stages no coordinates, and uses no heldout rows for selection or threshold tuning.

## Status

- fold_augmented_lever3_descriptor_generalization_counteraxis_readout_partial_application
- Descriptor counteraxis selected now: True
- Ready for partial application now: True
- Application rows used for rule selection: False

## Counts

- Calibration descriptor rows: 34/34
- Design same-family descriptor rows: 14/59
- Application rows fired after selection: 1/2
- Retained residual rows before/after descriptor counteraxis: 11/10

## Selected Rule

- Rule: residue_count.LEU <= 1.0
- Calibration in-scope fired: 0
- Design same-family rows fired: 3
- All train/cal OOS descriptor rows fired: 7

## Application Rows

| row | action delta | selected rule fires | used for selection |
| --- | --- | --- | --- |
| m_csa:25 | abstain_or_route_novel_oos | True | False |
| m_csa:52 | retain_at_fixed_operating_point_not_scoring_closure | False | False |

## Top Candidate Rules

| rule | design fired | all OOS fired | application fired |
| --- | ---: | ---: | ---: |
| residue_count.LEU <= 1.0 | 3 | 7 | 1 |
| descriptor.hydrophobic_fraction <= 0.2093 | 2 | 3 | 0 |
| residue_count.THR <= 0.0 | 2 | 10 | 0 |
| residue_count.ASN >= 8.0 | 1 | 1 | 0 |
| residue_count.ASP >= 11.0 | 1 | 1 | 0 |
| residue_count.CYS >= 7.0 | 1 | 1 | 0 |
| residue_count.GLN >= 8.0 | 1 | 1 | 0 |
| residue_count.LEU >= 15.0 | 1 | 1 | 0 |
| residue_count.MET >= 7.0 | 1 | 1 | 0 |
| descriptor.charge_balance >= 0.1818 | 1 | 2 | 0 |

## Decision

- Zero residual retained-transfer risk available now: False
- Fixed-threshold scoring closure available now: False
- Unsafe forced mechanism transfer allowed: False
- Apply/change threshold now: False
- Remaining evidence: ['source-free pocket descriptor acquisition for retained same-family rows still missing descriptors', 'a train/cal-selected source-free descriptor or chemistry counteraxis that fires m_csa:52 while preserving calibration in-scope retention']
- Next gate: Apply the descriptor counteraxis only as partial abstention evidence for fired retained rows; keep m_csa:52 and the descriptor-missing retained rows fail-open to the evidence queue, not scoring closure.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- The descriptor counteraxis abstains 1/2 descriptor-present retained residual rows after train/cal-only selection.
- The selected rule is residue_count.LEU <= 1.0; retained residual rows fall from 11 to 10, but zero residual risk is not closed.
- Treat this as partial fail-closed evidence and continue with source-free descriptor acquisition for the missing rows plus a separate m_csa:52 counteraxis search.
