# Ser/Thr Protein Phosphatase Sourcing - broadened evidence handles

Run: 2026-06-14T23:23:53Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.3.16/48 protein phosphatases
through protein-phosphatase family context, dinuclear metal/cofactor evidence,
and Rhea/reviewed phosphoprotein dephosphorylation.
EC / keyword / reaction text are scope-admission only, never predictive;
HAD-like phosphatase, Cys-PTP/DSP/PTEN, small-molecule phosphatase, kinase,
transferase, phosphodiesterase/nuclease, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: ser_thr_protein_phosphatase.
- Lanes queried: 3 (<= 340 rows each).
- Per-lane record window: offset 220, limit 40.
- Fetched candidate rows: 117.
- Target mechanism-corroborated bronze labels: 61 (off-target held 1; disambiguation holds 33; skipped 22).
- **Novelty-admitted labels: 39** (throttled/rejected 22; held@cap 0).
- Combined registry 8010 -> **8049** if merged.

## Floor projection

- `ser_thr_protein_phosphatase`: 0 -> 39 (added 39; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'ser_thr_protein_phosphatase': 150}.

## Novelty gate

- Decisions: {'admit': 39, 'throttle': 22}.
- Reasons: {'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 13, 'needed_fingerprint_but_redundant_ortholog': 22}.

## Hold reasons

- {'no_mechanism_corroboration': 33}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
