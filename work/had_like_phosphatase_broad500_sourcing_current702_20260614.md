# HAD-like Phosphatase Sourcing - broadened evidence handles

Run: 2026-06-14T19:19:31Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.3 HAD-like
phosphatases through HAD/haloacid-dehalogenase family context, Asp/Mg
site evidence, and Rhea/reviewed phosphomonoester hydrolysis where
available. EC / keyword / reaction text are scope-admission only, never
predictive; protein phosphatases, metal phosphomonoesterases without HAD
signal, phosphodiesterases/nucleases, kinases, side-EC, EC-only, and
off-target fingerprint rows are guarded or held.

## Result

- Families sourced: had_like_phosphatase.
- Lanes queried: 3 (<= 500 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 613.
- Target mechanism-corroborated bronze labels: 147 (off-target held 207; disambiguation holds 203; skipped 56).
- **Novelty-admitted labels: 145** (throttled/rejected 2; held@cap 0).
- Combined registry 7564 -> **7709** if merged.

## Floor projection

- `had_like_phosphatase`: 0 -> 145 (added 145; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'had_like_phosphatase': 150}.

## Novelty gate

- Decisions: {'admit': 145, 'throttle': 2}.
- Reasons: {'adds_diversity': 45, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 2}.

## Hold reasons

- {'no_mechanism_corroboration': 7, 'multi_fingerprint_signal_conflict': 196}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
