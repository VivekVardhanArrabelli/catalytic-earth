# Stage-1 Hole Sourcing — Cofactor-Defined Holes (non-destructive preview)

Run: 2026-06-14T00:35:42Z

Sources fresh reviewed Swiss-Prot bronze for the cofactor-defined holes via
the existing fetch -> cofactor/EC disambiguation -> novelty-gate pipeline.
EC/name/prose are scope-only (never predictive); tier=bronze; the frozen
current702 benchmark is NOT written. ser_his uses the triad-locator tool.

## Result

- Holes sourced: flavin_monooxygenase, heme_peroxidase_oxidase.
- Lanes queried: 5 (<= 120 rows each).
- Per-lane record window: offset 30, limit 30.
- Fetched candidate rows: 107.
- Disambiguated bronze labels: 21 (held 19, skipped 67).
- **Novelty-admitted labels: 0** (throttled/rejected 20).
- Combined registry 7742 -> **7742** if merged.

## Floor projection (100-label floor)

| Fingerprint | combined before | admitted | projected | floor reached | held@cap | over cap |
| --- | --- | --- | --- | --- | --- | --- |
| flavin_monooxygenase | 116 | 0 | 116 | True | 0 | False |
| heme_peroxidase_oxidase | 119 | 0 | 119 | True | 0 | False |

## Novelty gate

- Decisions: {'admit': 1, 'reject': 1, 'throttle': 19}.
- Reasons: {'adds_diversity': 1, 'fingerprint_over_cap_no_new_chemistry': 1, 'redundant_no_novelty_signal': 19}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
