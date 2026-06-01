# Fold-Augmented Family-Panel Source Check - m_csa:750

Run: 2026-06-01T08:54:29Z

Review-only frozen-local source check for non-abstained fold-augmented radical/cobalamin panel row m_csa:750.

## Status

- source_check_completed_review_only_no_label_change
- Review-only. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.

## Row

- Entry: m_csa:750
- Name: 4-hydroxybutanoyl-CoA dehydratase
- UniProt: P55792
- Current registry label: out_of_scope / None
- Stale manifest role needing readthrough: primary_supervised_metric::flavin_dehydrogenase_reductase
- Panel: cobalamin_and_radical_rearrangement_panel

## Fold-Augmented Readout

- Queue rank: 3
- Combined mean geometry+fold: 0.55105
- Threshold margin: 0.1095
- Geometry top1: metal_dependent_hydrolase
- Nearest predicted-fold fingerprint: flavin_dehydrogenase_reductase
- Selected organic cofactor max: 0.703989

## Local Source Evidence

- Frozen M-CSA and the existing m_csa750 revision support FAD semiquinone radical plus Fe-S coupled dehydration, including substrate hydrogen abstraction, ketyl radical chemistry, iron coordination of the hydroxy group, water elimination, and final protonation.
- Label revision decision: relabel_out_of_scope
- Mechanism class: radical_flavin_fe_s_dehydratase
- Catalytic residue nodes: 8
- Curated label rationale: 4-hydroxybutanoyl-CoA dehydratase is outside the v1 seed fingerprints: M-CSA mechanism text describes FAD semiquinone radical/Fe-S coupled dehydration rather than ordinary flavin hydride-transfer dehydrogenase-reductase chemistry.

## Decision

- Result: keep_as_oos_boundary_and_future_radical_flavin_fe_s_candidate
- Family promotion ready: False
- Reason: The current registry and dedicated m_csa750 revision already relabel this row out_of_scope. The non-abstained fold readout is expected false-confidence pressure from flavin-like fold/cofactor signals, not evidence for current v1 flavin_dehydrogenase_reductase, FMO, cobalamin, or radical-SAM promotion.
- Next action: Continue the source-check queue with m_csa:551; treat m_csa:750 only as a future radical_flavin_fe_s_dehydratase candidate if a new authorized family panel is scoped.
