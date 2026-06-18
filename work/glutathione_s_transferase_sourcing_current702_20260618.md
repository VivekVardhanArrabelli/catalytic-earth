# Glutathione-S-Transferase Sourcing - broadened evidence handles

Run: 2026-06-18T18:44:27Z

Sources fresh reviewed Swiss-Prot bronze for EC 2.5.1.18 glutathione
S-transferases through a glutathione-transferase family/name plus a Rhea/reviewed
reaction conjugating glutathione to an electrophile (-> an S-substituted
glutathione).
EC / keyword / reaction text are scope-admission only, never predictive;
glutathione peroxidase (EC 1.11.1), glutathione reductase (EC 1.8.1.7),
glutathione synthetase, glutaredoxin, gamma-glutamyltransferase,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: glutathione_s_transferase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 323.
- Target mechanism-corroborated bronze labels: 267 (off-target held 1; disambiguation holds 55; skipped 0).
- **Novelty-admitted labels: 141** (throttled/rejected 126; held@cap 0).
- Combined registry 9186 -> **9327** if merged.

## Floor projection

- `glutathione_s_transferase`: 0 -> 141 (added 141; cap 250; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'glutathione_s_transferase': 250}.

## Novelty gate

- Decisions: {'admit': 141, 'throttle': 126}.
- Reasons: {'adds_diversity': 41, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 91, 'redundant_no_novelty_signal': 35}.

## Hold reasons

- {'no_mechanism_corroboration': 55}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
