# Fold-Augmented Lever 3 Descriptor-Present Counteraxis Preflight - current702

Run: 2026-06-05T04:13:54Z

Lever 3 measured preflight for descriptor-present retained same-family residual rows. It freezes the source-free pocket descriptor fields that can be used as input to a future train/cal-only counteraxis design, but it does not select a counteraxis, tune a threshold, score rows, stage coordinates, or use these retained rows as calibration evidence.

## Status

- fold_augmented_lever3_descriptor_present_counteraxis_preflight_ready_input_frozen
- Descriptor input values frozen: True
- Counteraxis selected now: False
- Counteraxis ready for deployment now: False

## Counts

- Descriptor-present retained rows requested/found/missing: 2/2/0
- Descriptor fields: 8
- Residue-code count fields: 20
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204

## Allowed Feature Contract

- Descriptor fields: ['aromatic_fraction', 'charge_balance', 'hydrophobic_fraction', 'mean_min_distance_to_active_site', 'negative_fraction', 'polar_fraction', 'positive_fraction', 'sulfur_fraction']
- Residue-code fields: ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
- Forbidden fields: ['mechanism_text_count', 'mechanism_text_snippets', 'true_fingerprint_id', 'top1_fingerprint_id', 'entry_name', 'experimental_pdb_id', 'pdb_id']
- Retained rows may select/tune rule: False

## Descriptor-Present Rows

| row | top1 score | nearby residues | descriptor keys | countable now |
| --- | ---: | ---: | --- | --- |
| m_csa:25 | 0.3778 | 55 | aromatic_fraction, charge_balance, hydrophobic_fraction, mean_min_distance_to_active_site, negative_fraction, polar_fraction, positive_fraction, sulfur_fraction | False |
| m_csa:52 | 0.5977 | 59 | aromatic_fraction, charge_balance, hydrophobic_fraction, mean_min_distance_to_active_site, negative_fraction, polar_fraction, positive_fraction, sulfur_fraction | False |

## Decision

- Score or force mechanism label for retained rows now: False
- Apply/change threshold now: False
- Next gate: Use these frozen descriptor fields only as a candidate input contract. Select any pocket/chemistry counteraxis on a train/cal-only surface, then rerun the retained-risk readout; do not tune on m_csa:25 or m_csa:52.

## Guardrails

- Measured preflight only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- 2/2 descriptor-present retained residual rows have frozen source-free pocket values.
- The candidate input contract exposes 8 numeric descriptor fields and 20 residue-count fields, but no counteraxis is selected now.
- Design any same-family pocket counteraxis on train/cal-only evidence, then apply it through a new measured readout without changing threshold 0.44155.
