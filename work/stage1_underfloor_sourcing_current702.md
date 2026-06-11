# Stage-1 Hole Sourcing — Cofactor-Defined Holes (non-destructive preview)

Run: 2026-06-11T00:09:09Z

Sources fresh reviewed Swiss-Prot bronze for the cofactor-defined holes via
the existing fetch -> cofactor/EC disambiguation -> novelty-gate pipeline.
EC/name/prose are scope-only (never predictive); tier=bronze; the frozen
current702 benchmark is NOT written. ser_his uses the triad-locator tool.

## Result

- Holes sourced: flavin_monooxygenase, heme_peroxidase_oxidase, flavin_dehydrogenase_reductase.
- Lanes queried: 8 (<= 100 rows each).
- Fetched candidate rows: 602.
- Disambiguated bronze labels: 390 (held 116, skipped 96).
- **Novelty-admitted labels: 286** (throttled/rejected 101).
- Combined registry 2669 -> **2955** if merged.

## Floor projection (100-label floor)

| Fingerprint | combined before | admitted | projected | floor reached | held@cap | over cap |
| --- | --- | --- | --- | --- | --- | --- |
| flavin_monooxygenase | 43 | 73 | 116 | True | 0 | False |
| heme_peroxidase_oxidase | 69 | 50 | 119 | True | 0 | False |
| flavin_dehydrogenase_reductase | 87 | 163 | 250 | True | 3 | False |

## Novelty gate

- Decisions: {'admit': 289, 'reject': 38, 'throttle': 63}.
- Reasons: {'adds_diversity': 186, 'closes_under_floor_fingerprint': 101, 'fingerprint_over_cap_no_new_chemistry': 38, 'needed_fingerprint_but_redundant_ortholog': 9, 'over_cap_but_new_reaction_chemistry': 2, 'redundant_no_novelty_signal': 54}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
