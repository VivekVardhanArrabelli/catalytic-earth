# Family Panel Source-Free Predicted-Geometry Source Check - mh_066

Run: 2026-06-01T15:48:19Z

Review-only frozen-local source check for source-free predicted-geometry family-panel row mh_066.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, source fetching, or production scoring changed.

## Row

- Entry: mh_066
- Name: Metallo-beta-lactamase IMP-1
- Source accession: uniprot:P52699
- Panel: no_reliable_structure_metal_hydrolase_controls
- Current state: external_no_decision_review_only

## Fold-Augmented Readout

- Queue rank: 1
- Combined mean geometry+fold: 0.66335
- Threshold margin: 0.2218
- Geometry top1: metal_dependent_hydrolase (0.3822)
- Nearest predicted-fold fingerprint: metal_dependent_hydrolase (TM 0.9445)
- Geometry/fold agreement: True

## Local Frozen Evidence

- External panel context identifies IMP-1 as a tier-B external metallo-beta-lactamase lead with zinc beta-lactam hydrolysis context, but explicitly keeps it non-countable and review-only.
- Local 1DD6 coordinate metadata maps to UniProt P52699, carries EC 3.5.2.6, contains zinc entities, and describes an IMP-1 metallo-beta-lactamase hydrolase structure.
- The approved source-free locator has three UniProt-validated Zn-contact locators: ASP99, CYS176, and HIS215.
- Current702 has no exact P52699 accession match, but the nearest predicted-fold atlas row is m_csa:15, an occupied metal_dependent_hydrolase B1 beta-lactamase seed.
- No row-specific M-CSA-like bond-change or residue-role graph sidecar has been extracted for this external row.

## Decision

- Result: hold_as_review_only_metal_hydrolase_expansion_candidate
- Family promotion ready: False
- Reason: Frozen local evidence is consistent with IMP-1 zinc metallo-beta-lactamase hydrolase context and the source-free geometry/fold channels agree on metal_dependent_hydrolase, but mh_066 is an external non-countable row with no extracted row-specific bond-change/residue-role sidecar and no authorized duplicate, split, or expert admission gate.
- Next action: Continue the source-free source-check queue with mh_073, then secondary_probe::radical_sam_enzyme; keep mh_066 review-only until a future explicitly authorized import/admission packet resolves bond-change, duplicate, split, and expert-review blockers.
