# NAD(P)-dehydrogenase + Glycosyltransferase Sourcing — broadened evidence handles (non-destructive preview)

Run: 2026-06-17T02:29:38Z

Sources fresh reviewed Swiss-Prot bronze for two families whose defining evidence is
NOT a UniProt cofactor comment, via the broadened mechanism corroborator (cosubstrate /
Rhea participant / functional keyword / active-site) + EC-scope predicate, then the
novelty gate and a per-family cap guard. EC / keyword / cosubstrate are scope-only
(never predictive); tier=bronze; the frozen current702 benchmark is NOT written.

## Result

- Families sourced: nad_p_dehydrogenase.
- Lanes queried: 5 (<= 8 rows each).
- Fetched candidate rows: 40.
- Mechanism-corroborated bronze labels: 21 (held 1, skipped 18).
- **Novelty-admitted labels: 0** (throttled/rejected 4; held@cap 17).
- Combined registry 8728 -> **8728** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nad_p_dehydrogenase | nad_p_cosubstrate | 150 | 0 | 150 | 150 | True | 17 |

## Novelty gate

- Decisions: {'admit': 17, 'throttle': 4}.
- Reasons: {'adds_diversity': 17, 'redundant_no_novelty_signal': 4}.

## Disambiguation holds (mechanism corroboration)

- Hold reasons: {'no_mechanism_corroboration': 1}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Broadened handles (keyword/cosubstrate/binding) scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Per-family cap ceiling: {'nad_p_dehydrogenase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on EXPLICIT authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written; print the frozen sha before/after). Held/throttled rows are the next batch.
