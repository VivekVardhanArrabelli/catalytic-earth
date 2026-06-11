# Ser/His Hole Sourcing — Cofactorless Triad (non-destructive preview)

Run: 2026-06-11T00:44:33Z

Sources fresh reviewed Swiss-Prot bronze for the cofactorless
`ser_his_acid_hydrolase` hole: serine-hydrolase EC + no cofactor + a coordinate
Ser/Cys/Thr-His-Asp/Glu triad corroborated against the annotated catalytic
ACT_SITE on the AlphaFoldDB v6 predicted structure. EC is scope-only (never
predictive); tier=bronze; the frozen current702 benchmark is NOT written.

## Result

- Lanes queried: 3 (<= 60 rows each).
- Fetched candidate rows: 180; examined 164.
- Coordinates staged (AFDB v6): 159 (unavailable 0).
- **Triad-confirmed labels: 98**.
- **Novelty-admitted labels: 87** (throttled/rejected 11).
- Combined registry 2955 -> **3042** if merged.

## Floor projection (100-label floor)

| Fingerprint | combined before | admitted | projected | floor reached |
| --- | --- | --- | --- | --- |
| ser_his_acid_hydrolase | 42 | 87 | 129 | True |

## Hold reasons

- {'not_a_serine_hydrolase_ec_family': 2, 'registry_or_current702_duplicate': 3, 'triad:no_ser_his_triad': 48, 'triad:ser_his_triad_resolved_uncorroborated': 13}

## Novelty gate

- Decisions: {'admit': 87, 'throttle': 11}.
- Reasons: {'adds_diversity': 29, 'closes_under_floor_fingerprint': 58, 'needed_fingerprint_but_redundant_ortholog': 8, 'redundant_no_novelty_signal': 3}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Cofactorless corroboration is the coordinate triad (not a cofactor); all new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate + hold_reason_counts, then on explicit authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written). Held/throttled rows are the next batch.
