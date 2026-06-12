# NAD(P)-dehydrogenase + Glycosyltransferase Sourcing — broadened evidence handles (non-destructive preview)

Run: 2026-06-12T22:11:44Z

Sources fresh reviewed Swiss-Prot bronze for two families whose defining evidence is
NOT a UniProt cofactor comment, via the broadened mechanism corroborator (cosubstrate /
Rhea participant / functional keyword / active-site) + EC-scope predicate, then the
novelty gate and a per-family cap guard. EC / keyword / cosubstrate are scope-only
(never predictive); tier=bronze; the frozen current702 benchmark is NOT written.

## Result

- Families sourced: glycosyltransferase.
- Lanes queried: 3 (<= 150 rows each).
- Fetched candidate rows: 445.
- Mechanism-corroborated bronze labels: 157 (held 0, skipped 288).
- **Novelty-admitted labels: 27** (throttled/rejected 120; held@cap 10).
- Combined registry 4015 -> **4042** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| glycosyltransferase | sugar_nucleotide_donor | 223 | 27 | 250 | 250 | True | 10 |

## Novelty gate

- Decisions: {'admit': 37, 'reject': 100, 'throttle': 20}.
- Reasons: {'adds_diversity': 28, 'fingerprint_over_cap_no_new_chemistry': 100, 'over_cap_but_new_reaction_chemistry': 9, 'redundant_no_novelty_signal': 20}.

## Disambiguation holds (mechanism corroboration)

- Hold reasons: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Broadened handles (keyword/cosubstrate/binding) scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Per-family cap ceiling: {'glycosyltransferase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on EXPLICIT authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written; print the frozen sha before/after). Held/throttled rows are the next batch.
