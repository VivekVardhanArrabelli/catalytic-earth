# SAM Methyltransferase Sourcing - broadened evidence handles

Run: 2026-06-12T23:23:34Z

Sources fresh reviewed Swiss-Prot bronze for SAM-dependent methyltransferases via
SAM/SAH Rhea participant or Methyltransferase keyword evidence plus EC 2.1.1 scope.
EC / keyword / SAM/SAH participant text are scope-admission only, never predictive;
Fe-S / radical-SAM rows are held off-target.

## Result

- Families sourced: sam_methyltransferase.
- Lanes queried: 3 (<= 120 rows each).
- Fetched candidate rows: 315.
- Target mechanism-corroborated bronze labels: 304 (off-target held 0; disambiguation holds 2; skipped 9).
- **Novelty-admitted labels: 250** (throttled/rejected 40; held@cap 14).
- Combined registry 4042 -> **4292** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sam_methyltransferase | sam_sah_methyl_donor | 0 | 250 | 250 | 250 | True | 14 |

## Novelty gate

- Decisions: {'admit': 264, 'reject': 12, 'throttle': 28}.
- Reasons: {'adds_diversity': 151, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'fingerprint_over_cap_no_new_chemistry': 12, 'over_cap_but_new_reaction_chemistry': 13, 'redundant_no_novelty_signal': 28}.

## Disambiguation holds

- Hold reasons: {'multi_fingerprint_signal_conflict': 2}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- SAM/SAH + keyword handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- No-Fe-S radical-SAM guard: True.
- Per-family cap ceiling: {'sam_methyltransferase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
