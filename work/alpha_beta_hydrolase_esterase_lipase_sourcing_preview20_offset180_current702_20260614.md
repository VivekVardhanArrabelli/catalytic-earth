# Alpha/Beta Hydrolase Esterase/Lipase Sourcing - broadened evidence handles

Run: 2026-06-14T21:28:23Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.1 esterases/lipases
through alpha/beta hydrolase or esterase/lipase family context,
Ser-His-Asp/Glu catalytic-site evidence, and Rhea/reviewed ester hydrolysis.
EC / keyword / reaction text are scope-admission only, never predictive;
protease/amidase, glycoside/transglycosylase, metal-hydrolase, side-EC,
EC-only, and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: alpha_beta_hydrolase_esterase_lipase.
- Lanes queried: 3 (<= 220 rows each).
- Per-lane record window: offset 180, limit 20.
- Fetched candidate rows: 40.
- Target mechanism-corroborated bronze labels: 9 (off-target held 0; disambiguation holds 31; skipped 0).
- **Novelty-admitted labels: 9** (throttled/rejected 0; held@cap 0).
- Combined registry 7860 -> **7869** if merged.

## Floor projection

- `alpha_beta_hydrolase_esterase_lipase`: 0 -> 9 (added 9; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'alpha_beta_hydrolase_esterase_lipase': 150}.

## Novelty gate

- Decisions: {'admit': 9}.
- Reasons: {'closes_hole_fingerprint': 9}.

## Hold reasons

- {'no_mechanism_corroboration': 18, 'multi_fingerprint_signal_conflict': 13}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
