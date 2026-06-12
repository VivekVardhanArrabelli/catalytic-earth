# NAD(P)-dehydrogenase + Glycosyltransferase Sourcing — broadened evidence handles (non-destructive preview)

Run: 2026-06-12T21:56:27Z

Sources fresh reviewed Swiss-Prot bronze for two families whose defining evidence is
NOT a UniProt cofactor comment, via the broadened mechanism corroborator (cosubstrate /
Rhea participant / functional keyword / active-site) + EC-scope predicate, then the
novelty gate and a per-family cap guard. EC / keyword / cosubstrate are scope-only
(never predictive); tier=bronze; the frozen current702 benchmark is NOT written.

## Result

- Families sourced: nad_p_dehydrogenase, glycosyltransferase.
- Lanes queried: 8 (<= 100 rows each).
- Fetched candidate rows: 794.
- Mechanism-corroborated bronze labels: 709 (held 0, skipped 85).
- **Novelty-admitted labels: 373** (throttled/rejected 223; held@cap 113).
- Combined registry 3642 -> **4015** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nad_p_dehydrogenase | nad_p_cosubstrate | 0 | 150 | 150 | 150 | True | 113 |
| glycosyltransferase | sugar_nucleotide_donor | 0 | 223 | 223 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 486, 'reject': 167, 'throttle': 56}.
- Reasons: {'adds_diversity': 274, 'closes_hole_fingerprint': 52, 'closes_under_floor_fingerprint': 148, 'fingerprint_over_cap_no_new_chemistry': 167, 'needed_fingerprint_but_redundant_ortholog': 3, 'over_cap_but_new_reaction_chemistry': 12, 'redundant_no_novelty_signal': 53}.

## Disambiguation holds (mechanism corroboration)

- Hold reasons: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Broadened handles (keyword/cosubstrate/binding) scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Per-family cap ceiling: {'glycosyltransferase': 250, 'nad_p_dehydrogenase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate, then on EXPLICIT authorization append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` (frozen current702 never written; print the frozen sha before/after). Held/throttled rows are the next batch.
