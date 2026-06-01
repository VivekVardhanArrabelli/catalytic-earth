# Fold-Augmented Family-Panel Source Check - m_csa:116

Run: 2026-06-01T09:49:59Z

Review-only frozen-local source check for repaired fold-augmented family-panel row m_csa:116.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.

## Row

- Entry: m_csa:116
- Name: NAD(P)+ transhydrogenase (AB-specific)
- UniProt: Q2RSB2, Q2RSB4
- Current label: out_of_scope / None
- Benchmark role: oos_tier::unknown_oos
- Panel: near_orphan_glycoside_or_nucleoside_hydrolase_controls

## Fold-Augmented Readout

- Queue rank: 6
- Combined mean geometry+fold: 0.45755
- Threshold margin: 0.016
- Geometry top1: metal_dependent_hydrolase
- Nearest predicted-fold fingerprint: metal_dependent_hydrolase
- Selected organic cofactor max: 0.050535

## Repair Evidence

- Predicted-geometry accession: Q2RSB2
- Repair policy: manifest_accession_compatible_residue_subset
- Predicted residues resolved/missing: 5 / 0
- Nearest atlas row: m_csa:727 (metal_dependent_hydrolase); TM=0.5417

## Local Source Evidence

- M-CSA mechanism text describes NADH/NADP+ alignment, C4 hydride transfer between nicotinamide rings, and proton-translocation-linked conformational change, outside current seed fingerprints.
- Catalytic residue nodes: 6
- Curated label rationale: NAD(P)+ transhydrogenase performs nicotinamide hydride transfer coupled to proton translocation outside the current seed fingerprints.

## Decision

- Result: keep_as_review_only_oos_transhydrogenase_control
- Family promotion ready: False
- Reason: Frozen M-CSA mechanism evidence describes NAD(P)+ transhydrogenase hydride transfer coupled to proton translocation. The repaired fold-augmented non-abstention is a boundary false-confidence signal against occupied hydrolase/metal-like atlas neighborhoods, not support for a current seed-family promotion.
- Next action: Keep m_csa:116 as an OOS near-orphan/transhydrogenase control; prioritize source-backed sidecars for the remaining non-M-CSA missing-channel rows.
