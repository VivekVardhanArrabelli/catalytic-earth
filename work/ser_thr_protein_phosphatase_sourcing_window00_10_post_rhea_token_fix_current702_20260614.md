# Ser/Thr Protein Phosphatase Sourcing - broadened evidence handles

Run: 2026-06-14T23:09:00Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.3.16/48 protein phosphatases
through protein-phosphatase family context, dinuclear metal/cofactor evidence,
and Rhea/reviewed phosphoprotein dephosphorylation.
EC / keyword / reaction text are scope-admission only, never predictive;
HAD-like phosphatase, Cys-PTP/DSP/PTEN, small-molecule phosphatase, kinase,
transferase, phosphodiesterase/nuclease, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: ser_thr_protein_phosphatase.
- Lanes queried: 3 (<= 80 rows each).
- Per-lane record window: offset 0, limit 10.
- Fetched candidate rows: 30.
- Target mechanism-corroborated bronze labels: 4 (off-target held 0; disambiguation holds 12; skipped 14).
- **Novelty-admitted labels: 4** (throttled/rejected 0; held@cap 0).
- Combined registry 8010 -> **8014** if merged.

## Floor projection

- `ser_thr_protein_phosphatase`: 0 -> 4 (added 4; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'ser_thr_protein_phosphatase': 150}.

## Novelty gate

- Decisions: {'admit': 4}.
- Reasons: {'closes_hole_fingerprint': 4}.

## Hold reasons

- {'no_mechanism_corroboration': 12}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
