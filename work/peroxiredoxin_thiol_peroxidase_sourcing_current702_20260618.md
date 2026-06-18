# Peroxiredoxin / Thiol-Peroxidase Sourcing - broadened evidence handles

Run: 2026-06-18T17:30:41Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.11.1 peroxiredoxins / glutathione
peroxidases / thiol peroxidases through a Prx/GPx/thiol-peroxidase family/name OR a
peroxidatic-cysteine/selenocysteine thiol-redox context, plus Rhea/reviewed peroxide
(H2O2 / hydroperoxide) reduction reaction text.
EC / keyword / reaction text are scope-admission only, never predictive;
heme peroxidases/catalases (heme), FAD-dependent NADH peroxidases (flavin),
vanadium/non-heme haloperoxidases, manganese catalases, superoxide dismutases,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: peroxiredoxin_thiol_peroxidase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 331.
- Target mechanism-corroborated bronze labels: 304 (off-target held 0; disambiguation holds 27; skipped 0).
- **Novelty-admitted labels: 150** (throttled/rejected 53; held@cap 101).
- Combined registry 8906 -> **9056** if merged.

## Floor projection

- `peroxiredoxin_thiol_peroxidase`: 0 -> 150 (added 150; cap 150; floor reached: True; held@cap 101).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'peroxiredoxin_thiol_peroxidase': 150}.

## Novelty gate

- Decisions: {'admit': 251, 'reject': 29, 'throttle': 24}.
- Reasons: {'adds_diversity': 151, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'fingerprint_over_cap_no_new_chemistry': 29, 'needed_fingerprint_but_redundant_ortholog': 3, 'redundant_no_novelty_signal': 21}.

## Hold reasons

- {'no_mechanism_corroboration': 27}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
