# Cytochrome P450 Sourcing - broadened evidence handles

Run: 2026-06-13T22:19:38Z

Sources fresh reviewed Swiss-Prot bronze for cytochrome P450 monooxygenases via
heme plus P450/monooxygenase keyword, heme-thiolate binding, or O2/Rhea participant
evidence with EC 1.14 scope. EC / keyword / O2 participant text are
scope-admission only, never predictive; peroxide/peroxidase rows are held out.

## Result

- Families sourced: cytochrome_p450_monooxygenase.
- Lanes queried: 4 (<= 500 rows each).
- Fetched candidate rows: 24.
- Target mechanism-corroborated bronze labels: 14 (off-target held 0; disambiguation holds 1; skipped 9).
- **Novelty-admitted labels: 2** (throttled/rejected 8; held@cap 4).
- Combined registry 7283 -> **7285** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cytochrome_p450_monooxygenase | heme_thiolate_oxygen_cosubstrate | 248 | 2 | 250 | 250 | True | 4 |

## Novelty gate

- Decisions: {'admit': 6, 'reject': 8}.
- Reasons: {'adds_diversity': 3, 'fingerprint_over_cap_no_new_chemistry': 8, 'over_cap_but_new_reaction_chemistry': 3}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 1}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- P450/O2/heme handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Non-peroxidase guard: True.
- Per-family cap ceiling: {'cytochrome_p450_monooxygenase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
