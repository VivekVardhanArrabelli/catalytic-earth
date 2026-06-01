# Fold-Augmented Family-Panel Source Check - m_csa:267

Run: 2026-06-01T08:48:57Z

Review-only frozen-local source check for the top-ranked non-abstained fold-augmented family-panel row m_csa:267.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.

## Row

- Entry: m_csa:267
- Name: dihydrodipicolinate synthase
- UniProt: P0A6L2
- Current label: out_of_scope / None
- Panel: lipoamide_or_sulfur_transfer_redox_boundary

## Fold-Augmented Readout

- Queue rank: 1
- Combined mean geometry+fold: 0.5679
- Threshold margin: 0.12635
- Geometry top1: heme_peroxidase_oxidase
- Nearest predicted-fold fingerprint: flavin_dehydrogenase_reductase
- Selected organic cofactor max: 0.834847

## Local Source Evidence

- Frozen M-CSA mechanism text describes Lys161 Schiff-base formation with pyruvate, enamine addition to dehydrated (S)-ASA, and cyclization to HTPA; this supports lysine Schiff-base aldol/cyclization chemistry rather than the occupied seed mechanisms used by the current fold-augmented gate.
- Catalytic residue nodes: 6
- Curated label rationale: Dihydrodipicolinate synthase uses lysine Schiff-base aldol condensation and cyclization chemistry rather than PLP-dependent or hydrolase seed chemistry.

## Decision

- Result: keep_as_review_only_oos_boundary_control
- Family promotion ready: False
- Reason: Local source-backed mechanism evidence supports dihydrodipicolinate synthase lysine Schiff-base aldol/cyclization chemistry. The fold-augmented non-abstention is useful as a false-confidence review signal, but it does not support lipoamide/sulfur-transfer, flavin, heme, PLP, hydrolase, or other current seed-family promotion.
- Next action: Continue the source-check queue with m_csa:131; keep m_csa:267 as an OOS boundary control unless a future explicitly authorized Schiff-base aldol/cyclization panel is scoped with expert review.
