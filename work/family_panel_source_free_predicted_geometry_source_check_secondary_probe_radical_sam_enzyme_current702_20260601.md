# Family Panel Source-Free Predicted-Geometry Source Check - secondary_probe::radical_sam_enzyme

Run: 2026-06-01T15:55:38Z

Review-only frozen-local source check for source-free predicted-geometry family-panel row secondary_probe::radical_sam_enzyme.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, source fetching, or production scoring changed.

## Row

- Entry: secondary_probe::radical_sam_enzyme
- Source accession: uniprot:A0A1M6T2I7
- Panel: cobalamin_and_radical_rearrangement_panel
- Current state: secondary_probe_review_only_not_import_ready

## Fold-Augmented Readout

- Queue rank: 8
- Combined mean geometry+fold: 0.48335
- Threshold margin: 0.0418
- Geometry top1: metal_dependent_hydrolase (0.2628)
- Nearest predicted-fold fingerprint: plp_dependent_enzyme (TM 0.7039)
- Geometry/fold agreement: False

## Local Frozen Evidence

- The prospective radical-SAM freeze selected A0A1M6T2I7 as rank 1 before outcome scoring, with catalytic activity, PDB cross-reference, and radical-SAM/Fe-S/SAM source context.
- Local 8VPO coordinate metadata maps to A0A1M6T2I7, describes TigE, carries radical SAM and Fe-S keywords, and contains two SF4 iron-sulfur clusters.
- The approved source-free locator has four UniProt-validated SF4-contact cysteine locators: CYS414, CYS417, CYS423, and CYS446.
- Current702 has no exact A0A1M6T2I7 accession match and only one radical-SAM secondary probe row; the nearest predicted-fold atlas row is m_csa:358, a PLP-dependent seed.
- The source-free geometry top1 is metal_dependent_hydrolase while the fold hit is plp_dependent_enzyme, so the retained score is a confounded chemistry signal rather than current-family promotion evidence.

## Decision

- Result: confirm_radical_sam_locus_review_only_no_family_promotion
- Family promotion ready: False
- Reason: Frozen local evidence supports a radical-SAM/Fe-S TigE locus, but the source-free geometry and predicted-fold channels disagree and the nearest fold hit is PLP-dependent. Without a row-specific bond-change/residue-role sidecar, duplicate/split review, and expert admission, this remains secondary review-only radical-SAM panel evidence rather than current-family promotion support.
- Next action: After the three source-free source checks, return to clearing the seven remaining approved-locator blockers or build a stricter radical-SAM/cobalamin mechanism-locus sidecar before any family expansion decision.
