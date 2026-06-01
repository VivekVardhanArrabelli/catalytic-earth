# Fold-Augmented Family-Panel Source Check - m_csa:131

Run: 2026-06-01T08:51:58Z

Review-only frozen-local source check for non-abstained fold-augmented FMO panel row m_csa:131.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.

## Row

- Entry: m_csa:131
- Name: 4-hydroxybenzoate 3-monooxygenase
- UniProt: P20586
- Current label: seed_fingerprint / flavin_monooxygenase
- Benchmark role: secondary_ood_probe::flavin_monooxygenase
- Panel: flavin_monooxygenase_and_flavin_oxygen_transfer

## Fold-Augmented Readout

- Queue rank: 2
- Combined mean geometry+fold: 0.5516
- Threshold margin: 0.11005
- Geometry top1: metal_dependent_hydrolase
- Nearest predicted-fold fingerprint: flavin_dehydrogenase_reductase
- Selected organic cofactor max: 0.980908

## Local Source Evidence

- Frozen M-CSA mechanism text supports FAD/NADP redox activation, FAD-peroxo formation, aromatic substrate hydroxylation, O-O bond cleavage, and FAD regeneration through proton-relay chemistry; this is direct flavin monooxygenase/oxygen-transfer support.
- Catalytic residue nodes: 5
- Curated label rationale: 4-hydroxybenzoate 3-monooxygenase is an FAD-dependent aromatic hydroxylase matching the flavin monooxygenase seed fingerprint.

## Decision

- Result: confirm_secondary_fmo_probe_support_no_primary_promotion
- Family promotion ready: False
- Reason: Local source-backed mechanism evidence confirms m_csa:131 as a flavin monooxygenase secondary-probe row, but current project state keeps FMO secondary/review-only and blocks primary promotion until subtype, coordinate/materialization, hard-negative, and expert admission gates are completed.
- Next action: Continue the source-check queue with m_csa:750 or run an FMO subtype/hard-negative packet before any primary promotion discussion.
