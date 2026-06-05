# Fold-Augmented Lever 3 Retained Pairwise Descriptor Counteraxis Readout - current702

Run: 2026-06-05T06:18:16Z

Lever 3 measured retained pairwise descriptor counteraxis readout. It pre-registers a source-free residue-count OR-rule family, selects within train/cal same-family OOS design rows under a zero-calibration-fire guard and an all-train/cal-OOS breadth cap, then applies the selected rule to retained descriptor rows only after selection. It changes no thresholds, scores no new rows, stages no coordinates, and uses no heldout rows.

## Status

- fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_partial_application
- Pairwise descriptor counteraxis selected now: True
- Ready for partial application now: True
- Application rows used for rule selection: False

## Selection Policy

- Rule family: pairwise_or_of_residue_code_count_threshold_rules
- All train/cal OOS breadth cap rows: 8
- Selection objective: maximize design same-family OOS rows fired, then minimize all train/cal OOS descriptor rows fired, then deterministic rule id

## Counts

- Calibration descriptor rows: 34/34
- Design same-family descriptor rows: 14/59
- Atom/pair rules checked: 11/66
- Candidate pair rules within breadth cap: 53
- New retained rows fired after prior rule: 1
- Retained residual rows before/after pairwise counteraxis: 10/9
- Greedy follow-up new application rows after selected pairwise rule: 0
- Remaining retained rows with any eligible capped pair rule: 0
- Full frozen feature-family rules within breadth cap / remaining hits: 117/0

## Selected Rule

- Rule: residue_count.ASN >= 8.0 OR residue_count.LEU <= 1.0
- Calibration in-scope fired: 0
- Design same-family rows fired: 4
- All train/cal OOS descriptor rows fired: 8
- Retained application rows fired after selection: ['m_csa:25', 'm_csa:84']

## Application Rows

| row | source | prior fires | pairwise fires | new abstention | action delta |
| --- | --- | ---: | ---: | ---: | --- |
| m_csa:25 | descriptor_present_preflight | True | True | False | already_abstain_or_route_novel_oos_by_prior_descriptor_rule |
| m_csa:52 | descriptor_present_preflight | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:74 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:84 | retained_descriptor_rescue | False | True | True | abstain_or_route_novel_oos |
| m_csa:89 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:190 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:229 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:256 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:308 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:468 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:638 | retained_descriptor_rescue | False | False | False | retain_at_fixed_operating_point_not_scoring_closure |

## Top Candidate Pair Rules

| rule | design fired | all OOS fired | application fired |
| --- | ---: | ---: | ---: |
| residue_count.ASN >= 8.0 OR residue_count.LEU <= 1.0 | 4 | 8 | 2 |
| residue_count.ASP >= 11.0 OR residue_count.LEU <= 1.0 | 4 | 8 | 1 |
| residue_count.CYS >= 7.0 OR residue_count.LEU <= 1.0 | 4 | 8 | 1 |
| residue_count.LEU <= 1.0 OR residue_count.LEU >= 15.0 | 4 | 8 | 1 |
| residue_count.LEU <= 1.0 OR residue_count.MET >= 7.0 | 4 | 8 | 1 |
| residue_count.GLN >= 8.0 OR residue_count.LEU <= 1.0 | 3 | 7 | 1 |
| residue_count.LEU <= 0.0 OR residue_count.LEU <= 1.0 | 3 | 7 | 1 |
| residue_count.LEU <= 1.0 OR residue_count.LEU <= 1.0 | 3 | 7 | 1 |
| residue_count.ASN >= 8.0 OR residue_count.CYS >= 7.0 | 2 | 2 | 1 |
| residue_count.ASN >= 8.0 OR residue_count.GLN >= 8.0 | 2 | 2 | 1 |

## Retained-Blind Greedy Follow-Up

| rank | rule | new design fired | all OOS fired | new application fired |
| ---: | --- | ---: | ---: | --- |
| 1 | residue_count.ASN >= 8.0 OR residue_count.LEU <= 1.0 | 4 | 8 | ['m_csa:84'] |
| 2 | residue_count.CYS >= 7.0 OR residue_count.LEU >= 15.0 | 2 | 2 | [] |
| 3 | residue_count.SER >= 9.0 OR residue_count.SER >= 9.0 | 1 | 4 | [] |

## Full Feature-Family Residual Pressure

- Eligible capped pair rules: 117

| rule | design fired | all OOS fired | remaining retained fired |
| --- | ---: | ---: | --- |

## Decision

- Zero residual retained-transfer risk available now: False
- Fixed-threshold scoring closure available now: False
- Unsafe forced mechanism transfer allowed: False
- Apply/change threshold now: False
- Remaining retained rows: ['m_csa:52', 'm_csa:74', 'm_csa:89', 'm_csa:190', 'm_csa:229', 'm_csa:256', 'm_csa:308', 'm_csa:468', 'm_csa:638']
- Next gate: Treat the selected pairwise residue-count rule as partial fail-closed evidence for newly fired retained rows only. Continue designing train/cal-only counteraxes for the remaining retained descriptor rows; do not change threshold 0.44155 or force a mechanism label.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- The pairwise residue-count counteraxis adds 1 new retained-row abstention after train/cal-only selection.
- The selected rule is residue_count.ASN >= 8.0 OR residue_count.LEU <= 1.0; retained residual rows fall from 10 to 9 after the prior descriptor rule.
- Keep the remaining retained descriptor rows in the evidence queue and search for another source-free counteraxis selected only on train/cal evidence.
