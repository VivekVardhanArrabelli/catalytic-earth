# Stage-1 Hole Sourcing — Cofactor-Defined Holes (non-destructive preview)

Run: 2026-06-14T00:33:51Z

Sources fresh reviewed Swiss-Prot bronze for the cofactor-defined holes via
the existing fetch -> cofactor/EC disambiguation -> novelty-gate pipeline.
EC/name/prose are scope-only (never predictive); tier=bronze; the frozen
current702 benchmark is NOT written. ser_his uses the triad-locator tool.

## Result

- Holes sourced: flavin_monooxygenase, heme_peroxidase_oxidase.
- Lanes queried: 5 (<= 120 rows each).
- Per-lane record window: offset 0, limit 30.
- Fetched candidate rows: 125.
- Disambiguated bronze labels: 12 (held 39, skipped 74).
- **Novelty-admitted labels: 0** (throttled/rejected 10).
- Combined registry 7742 -> **7742** if merged.

## Floor projection (100-label floor)

| Fingerprint | combined before | admitted | projected | floor reached | held@cap | over cap |
| --- | --- | --- | --- | --- | --- | --- |
| flavin_monooxygenase | 116 | 0 | 116 | True | 0 | False |
| heme_peroxidase_oxidase | 119 | 0 | 119 | True | 0 | False |

## Novelty gate

- Decisions: {'admit': 2, 'reject': 6, 'throttle': 4}.
- Reasons: {'adds_diversity': 1, 'fingerprint_over_cap_no_new_chemistry': 6, 'over_cap_but_new_reaction_chemistry': 1, 'redundant_no_novelty_signal': 4}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
