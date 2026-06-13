# Cytochrome P450 Sourcing - broadened evidence handles

Run: 2026-06-13T00:09:19Z

Sources fresh reviewed Swiss-Prot bronze for cytochrome P450 monooxygenases via
heme plus P450/monooxygenase keyword, heme-thiolate binding, or O2/Rhea participant
evidence with EC 1.14 scope. EC / keyword / O2 participant text are
scope-admission only, never predictive; peroxide/peroxidase rows are held out.

## Result

- Families sourced: cytochrome_p450_monooxygenase.
- Lanes queried: 4 (<= 80 rows each).
- Fetched candidate rows: 142.
- Target mechanism-corroborated bronze labels: 128 (off-target held 0; disambiguation holds 14; skipped 0).
- **Novelty-admitted labels: 110** (throttled/rejected 18; held@cap 0).
- Combined registry 4292 -> **4402** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cytochrome_p450_monooxygenase | heme_thiolate_oxygen_cosubstrate | 0 | 110 | 110 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 110, 'throttle': 18}.
- Reasons: {'adds_diversity': 10, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 17, 'redundant_no_novelty_signal': 1}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 14}.
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
