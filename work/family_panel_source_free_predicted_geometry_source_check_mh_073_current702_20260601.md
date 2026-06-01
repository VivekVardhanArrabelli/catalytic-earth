# Family Panel Source-Free Predicted-Geometry Source Check - mh_073

Run: 2026-06-01T15:52:25Z

Review-only frozen-local source check for source-free predicted-geometry family-panel row mh_073.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, source fetching, or production scoring changed.

## Row

- Entry: mh_073
- Name: GTPase HRas
- Source accession: uniprot:P01112
- Panel: near_orphan_glycoside_or_nucleoside_hydrolase_controls
- Current state: external_no_decision_review_only

## Fold-Augmented Readout

- Queue rank: 7
- Combined mean geometry+fold: 0.48775
- Threshold margin: 0.0462
- Geometry top1: ser_his_acid_hydrolase (0.1733)
- Nearest predicted-fold fingerprint: metal_dependent_hydrolase (TM 0.8022)
- Geometry/fold agreement: False

## Local Frozen Evidence

- External panel context predeclares HRas as a hard negative for Mg/nucleotide leakage, not a countable family lead.
- Local 121P coordinate metadata maps to UniProt P01112, contains Mg plus a guanylate ester analog, and centers the site on Mg/GTPase chemistry rather than beta-lactam or glycoside hydrolase chemistry.
- The approved source-free locator has the minimum two UniProt-validated Mg-contact locators: SER17 and THR35.
- Current702 has no exact P01112 accession match, but the nearest predicted-fold atlas row is m_csa:535, a current702 GTPase-like seed labeled metal_dependent_hydrolase.
- The source-free geometry top1 is weak ser_his_acid_hydrolase while the fold hit is metal_dependent_hydrolase, so the non-abstention is a boundary false-confidence signal.

## Decision

- Result: keep_as_review_only_gtpase_boundary_hard_negative
- Family promotion ready: False
- Reason: Frozen local evidence supports an H-Ras Mg/GTPase nucleotide locus, the external panel predeclares mh_073 as a hard negative against Mg/nucleotide leakage, and source-free geometry disagrees with the metal-dependent fold hit. The non-abstention is a useful false-confidence/boundary signal, not support for near-orphan hydrolase or metal-hydrolase promotion.
- Next action: Continue the source-free source-check queue with secondary_probe::radical_sam_enzyme; keep mh_073 review-only unless a future explicitly authorized GTPase-boundary policy revisits current702 metal_dependent_hydrolase scope.
