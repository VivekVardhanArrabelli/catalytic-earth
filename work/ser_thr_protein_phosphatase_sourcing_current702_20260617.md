# Ser/Thr Protein Phosphatase Sourcing - broadened evidence handles

Run: 2026-06-17T20:10:23Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.3.16/48 protein phosphatases
through protein-phosphatase family context, dinuclear metal/cofactor evidence,
and Rhea/reviewed phosphoprotein dephosphorylation.
EC / keyword / reaction text are scope-admission only, never predictive;
HAD-like phosphatase, Cys-PTP/DSP/PTEN, small-molecule phosphatase, kinase,
transferase, phosphodiesterase/nuclease, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: ser_thr_protein_phosphatase.
- Lanes queried: 3 (<= 250 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 456.
- Target mechanism-corroborated bronze labels: 85 (off-target held 1; disambiguation holds 177; skipped 193).
- **Novelty-admitted labels: 0** (throttled/rejected 85; held@cap 0).
- Combined registry 8817 -> **8817** if merged.

## Floor projection

- `ser_thr_protein_phosphatase`: 112 -> 112 (added 0; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'ser_thr_protein_phosphatase': 150}.

## Novelty gate

- Decisions: {'throttle': 85}.
- Reasons: {'redundant_no_novelty_signal': 85}.

## Hold reasons

- {'no_mechanism_corroboration': 177}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
