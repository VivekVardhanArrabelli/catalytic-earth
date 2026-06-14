# Alpha/Beta Hydrolase Esterase/Lipase Sourcing - broadened evidence handles

Run: 2026-06-14T21:30:20Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.1 esterases/lipases
through alpha/beta hydrolase or esterase/lipase family context,
Ser-His-Asp/Glu catalytic-site evidence, and Rhea/reviewed ester hydrolysis.
EC / keyword / reaction text are scope-admission only, never predictive;
protease/amidase, glycoside/transglycosylase, metal-hydrolase, side-EC,
EC-only, and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: alpha_beta_hydrolase_esterase_lipase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 260, limit 20.
- Fetched candidate rows: 40.
- Target mechanism-corroborated bronze labels: 19 (off-target held 0; disambiguation holds 20; skipped 1).
- **Novelty-admitted labels: 19** (throttled/rejected 0; held@cap 0).
- Combined registry 7860 -> **7879** if merged.

## Floor projection

- `alpha_beta_hydrolase_esterase_lipase`: 0 -> 19 (added 19; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'alpha_beta_hydrolase_esterase_lipase': 150}.

## Novelty gate

- Decisions: {'admit': 19}.
- Reasons: {'closes_hole_fingerprint': 19}.

## Hold reasons

- {'no_mechanism_corroboration': 20}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
