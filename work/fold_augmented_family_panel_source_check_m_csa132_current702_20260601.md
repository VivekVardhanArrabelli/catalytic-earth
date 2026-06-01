# Fold-Augmented Family-Panel Source Check - m_csa:132

Run: 2026-06-01T09:49:59Z

Review-only frozen-local source check for repaired fold-augmented family-panel row m_csa:132.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.

## Row

- Entry: m_csa:132
- Name: alkanal monooxygenase (FMN-linked)
- UniProt: P07740, P07739
- Current label: seed_fingerprint / flavin_monooxygenase
- Benchmark role: secondary_ood_probe::flavin_monooxygenase
- Panel: flavin_monooxygenase_and_flavin_oxygen_transfer

## Fold-Augmented Readout

- Queue rank: 5
- Combined mean geometry+fold: 0.53865
- Threshold margin: 0.0971
- Geometry top1: ser_his_acid_hydrolase
- Nearest predicted-fold fingerprint: flavin_dehydrogenase_reductase
- Selected organic cofactor max: 0.010805

## Repair Evidence

- Predicted-geometry accession: P07740
- Repair policy: best_real_sequence_accession_by_active_site_coverage
- Predicted residues resolved/missing: 5 / 0
- Nearest atlas row: m_csa:120 (flavin_dehydrogenase_reductase); TM=0.6879

## Local Source Evidence

- M-CSA mechanism text describes FMN-peroxo/peroxyflavin oxygen-transfer chemistry, aldehyde oxidation/luminescence, and FMN regeneration; this supports FMO-like oxygen transfer but not a current primary-family import.
- Catalytic residue nodes: 5
- Curated label rationale: Alkanal monooxygenase is FMN-linked oxygenation chemistry, fitting the broad flavin monooxygenase seed fingerprint.

## Decision

- Result: confirm_secondary_fmo_support_after_geometry_repair_no_primary_promotion
- Family promotion ready: False
- Reason: Frozen M-CSA mechanism evidence supports FMN-linked oxygen-transfer chemistry and the repaired P07740 predicted geometry makes the fold-augmented channel score-complete, but current project state keeps FMO secondary/review-only until subtype, hard-negative, duplicate/leakage, coordinate, and expert-admission blockers are resolved.
- Next action: Keep m_csa:132 as secondary FMO support and update the FMO subtype/hard-negative packet/readout; do not promote FMO or edit registries.
