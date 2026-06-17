# NAD(P)-dehydrogenase + Glycosyltransferase Sourcing — broadened evidence handles (non-destructive preview)

Run: 2026-06-17T02:21:33Z

Sources fresh reviewed Swiss-Prot bronze for two families whose defining evidence is
NOT a UniProt cofactor comment, via the broadened mechanism corroborator (cosubstrate /
Rhea participant / functional keyword / active-site) + EC-scope predicate, then the
novelty gate and a per-family cap guard. EC / keyword / cosubstrate are scope-only
(never predictive); tier=bronze; the frozen current702 benchmark is NOT written.

## Result

- Families sourced: glycosyltransferase.
- Lanes queried: 3 (<= 5 rows each).
- Fetched candidate rows: 15.
- Mechanism-corroborated bronze labels: 0 (held 1, skipped 14).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 8728 -> **8728** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| glycosyltransferase | sugar_nucleotide_donor | 250 | 0 | 250 | 250 | True | 0 |

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Disambiguation holds (mechanism corroboration)

- Hold reasons: {'multi_fingerprint_signal_conflict': 1}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Broadened handles (keyword/cosubstrate/binding) scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Per-family cap ceiling: {'glycosyltransferase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on EXPLICIT authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written; print the frozen sha before/after). Held/throttled rows are the next batch.
