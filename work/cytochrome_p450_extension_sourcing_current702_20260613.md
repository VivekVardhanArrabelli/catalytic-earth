# Cytochrome P450 Sourcing - broadened evidence handles

Run: 2026-06-13T12:36:14Z

Sources fresh reviewed Swiss-Prot bronze for cytochrome P450 monooxygenases via
heme plus P450/monooxygenase keyword, heme-thiolate binding, or O2/Rhea participant
evidence with EC 1.14 scope. EC / keyword / O2 participant text are
scope-admission only, never predictive; peroxide/peroxidase rows are held out.

## Result

- Families sourced: cytochrome_p450_monooxygenase.
- Lanes queried: 4 (<= 240 rows each).
- Fetched candidate rows: 337.
- Target mechanism-corroborated bronze labels: 189 (off-target held 0; disambiguation holds 35; skipped 113).
- **Novelty-admitted labels: 138** (throttled/rejected 51; held@cap 0).
- Combined registry 6781 -> **6919** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cytochrome_p450_monooxygenase | heme_thiolate_oxygen_cosubstrate | 110 | 138 | 248 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 138, 'throttle': 51}.
- Reasons: {'adds_diversity': 138, 'redundant_no_novelty_signal': 51}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 35}.
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
