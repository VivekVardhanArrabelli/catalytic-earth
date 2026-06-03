# Fold-Augmented Fixed-Threshold Combined Rerun Readout - current702

Run: 2026-06-03T00:57:46Z

Fixed-threshold Lever 3 readout over the newly approved source-feature sidecar rows plus the authorized P00889 ortholog surrogate. It applies the frozen 0.44155 combined_mean_geometry_fold threshold and records the P10746 fold-only caveat; it does not tune thresholds or close deployment.

## Status

- fold_augmented_fixed_threshold_combined_rerun_readout_complete_with_caveat
- Fixed threshold: 0.44155
- Combined rows abstained at fixed threshold: 2
- Combined rows retained at fixed threshold: 2
- Fold-only caveat rows: 1

## Combined Rows

| row | accession | geometry top1 | geometry score | fold TM | combined | abstains |
| --- | --- | --- | ---: | ---: | ---: | --- |
| m_csa:78 | P00889 | metal_dependent_hydrolase | 0.3433 | 0.4675 | 0.4054 | True |
| m_csa:531 | P31572 | metal_dependent_hydrolase | 0.3402 | 0.611 | 0.4756 | False |
| uniprot:P78549 | P78549 | flavin_dehydrogenase_reductase | 0.4086 | 0.4411 | 0.42485 | True |
| uniprot:Q3LXA3 | Q3LXA3 | metal_dependent_hydrolase | 0.2938 | 0.6028 | 0.4483 | False |

## Fold-Only Caveat

| row | fold TM | caveat |
| --- | ---: | --- |
| m_csa:204 | 0.5651 | P10746 remains fold-only because no approved non-residue sidecar was created; it is excluded from combined-channel scoring. |

## Guardrails

- P00889 Foldseek/TM was rerun against the existing train atlas.
- No threshold, label, registry, ontology, import, split, model-weight, or heldout-training surface changed.
- Source-feature geometry used approved feature classes, ligand classes, and sequence positions; source ids, target names, EC/Rhea IDs, mechanism text, and feature descriptions were not predictive inputs.

## Next Gate

- Fold the four combined readout rows into the train/cal OOS calibration contract without touching heldout rows, and carry the P10746 fold-only caveat into the deployment-closure audit.
