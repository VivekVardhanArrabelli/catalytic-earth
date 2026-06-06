# Fold-Augmented Lever 3 Retained Pocket-Chemistry Counteraxis Readout - current702

Run: 2026-06-05T08:20:54Z

Lever 3 measured retained pocket-chemistry counteraxis readout. It derives source-free active-site chemistry class counts from frozen pocket residue-code counts, combines them with existing scalar pocket descriptors, selects one threshold rule on train/cal same-family OOS design rows under a zero-calibration-fire guard and an all-train/cal-OOS breadth cap, then applies the rule to retained application rows only after selection. It changes no thresholds, scores no rows, stages no coordinates, and uses no heldout rows for selection or tuning.

## Status

- fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_partial_application
- Pocket-chemistry counteraxis selected now: True
- Ready for partial application now: True
- Application rows used for rule selection: False

## Selection Policy

- Rule family: single_threshold_rule_over_pocket_chemistry_class_counts_or_scalar_descriptors
- Chemistry count features: ['acidic_count', 'aromatic_count', 'basic_count', 'charged_count', 'sulfur_count']
- Descriptor features: ['aromatic_fraction', 'charge_balance', 'hydrophobic_fraction', 'mean_min_distance_to_active_site', 'negative_fraction', 'polar_fraction', 'positive_fraction', 'sulfur_fraction']
- All train/cal OOS breadth cap rows: 8
- Selection objective: maximize design same-family OOS rows fired, then minimize descriptor-covered train/cal OOS rows fired, then deterministic feature/operator/threshold order

## Operating Point

- Calibration retained before/after pocket chemistry: 31/31 of 34
- Train/cal OOS abstained before/after pocket chemistry: 165/165 of 204
- New train/cal OOS abstentions from pocket chemistry: 0
- Production threshold change: False

## Counts

- Calibration descriptor rows: 34/34
- Design same-family descriptor rows: 14/59
- Application rows with pocket descriptors: 11/11
- Rules evaluated / candidates within breadth cap: 310/9
- New retained rows fired after prior counteraxes: 1
- Retained residual rows after pocket chemistry: 1
- Remaining retained rows with any eligible pocket-chemistry rule: 0

## Selected Rule

- Rule: chemistry_count.sulfur_count >= 9.0
- Calibration in-scope fired: 0
- Design same-family rows fired: 2
- All train/cal OOS descriptor rows fired: 2
- Retained application rows fired after selection: ['m_csa:468']

## Application Rows

| row | retained after prior | chemistry fires | new chemistry | feature value | action delta |
| --- | ---: | ---: | ---: | ---: | --- |
| m_csa:25 | False | False | False | 3.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:52 | False | False | False | 3.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:74 | False | False | False | 1.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:84 | False | False | False | 2.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:89 | False | False | False | 6.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:190 | False | False | False | 5.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:229 | False | False | False | 2.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:256 | False | False | False | 4.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:308 | True | False | False | 4.0 | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:468 | True | True | True | 9.0 | abstain_or_route_novel_oos_by_pocket_chemistry |
| m_csa:638 | False | False | False | 3.0 | already_abstain_or_route_novel_oos_by_prior_counteraxis |

## Top Candidate Rules

| rule | design fired | all OOS fired | application fired |
| --- | ---: | ---: | ---: |
| chemistry_count.sulfur_count >= 9.0 | 2 | 2 | 1 |
| descriptor.hydrophobic_fraction <= 0.2093 | 2 | 3 | 0 |
| chemistry_count.acidic_count >= 19.0 | 1 | 1 | 0 |
| chemistry_count.charged_count >= 34.0 | 1 | 1 | 0 |
| chemistry_count.sulfur_count >= 11.0 | 1 | 1 | 0 |
| descriptor.charge_balance >= 0.1818 | 1 | 2 | 0 |
| descriptor.hydrophobic_fraction <= 0.2055 | 1 | 2 | 0 |
| descriptor.positive_fraction >= 0.2727 | 1 | 2 | 0 |
| descriptor.polar_fraction <= 0.1515 | 1 | 4 | 0 |

## Residual Pressure

- Eligible single rules within breadth cap: 9
- Candidate rules hitting remaining retained rows: 0

| rule | design fired | all OOS fired | remaining retained fired |
| --- | ---: | ---: | --- |

## Decision

- Zero residual retained-transfer risk available now: False
- Fixed-threshold scoring closure available now: False
- Unsafe forced mechanism transfer allowed: False
- Apply/change threshold now: False
- Newly abstained retained rows: ['m_csa:468']
- Remaining retained rows after pocket chemistry: ['m_csa:308']
- Next gate: Treat the selected pocket sulfur-count rule as partial fail-closed evidence for newly fired retained rows only. Keep residual retained rows in the evidence queue; do not change threshold 0.44155 or force a mechanism label.

## Guardrails

- Measured readout only. Existing source-free artifacts only; no coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- The pocket-chemistry counteraxis adds 1 retained-row abstention after descriptor, margin, fold-TM, and fold/cofactor pressure counteraxes.
- The selected rule is chemistry_count.sulfur_count >= 9.0; it fires 0 new train/cal OOS rows after prior counteraxes and leaves retained residual rows ['m_csa:308'].
- Current pocket chemistry class-count evidence separates m_csa:468 but not m_csa:308; design or acquire a richer source-free metal/cofactor or ligand-neighborhood axis for that remaining high-confidence lookalike.
