# Protein Kinase Sourcing - broadened evidence handles

Run: 2026-06-17T02:32:36Z

Sources fresh reviewed Swiss-Prot bronze for EC 2.7.10/2.7.11 Ser/Thr/Tyr
protein kinases via protein-kinase family context, ATP/Mg evidence, Rhea
protein phosphorylation context, and active-/binding-site evidence where available.
EC / keyword / reaction text are scope-admission only, never predictive; histidine
kinases, small-molecule kinases, ATP ligases, hydrolases, side-EC, EC-only,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: protein_kinase_ser_thr_tyr.
- Lanes queried: 1 (<= 10 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 10.
- Target mechanism-corroborated bronze labels: 1 (off-target held 0; disambiguation holds 0; skipped 9).
- **Novelty-admitted labels: 0** (throttled/rejected 1; held@cap 0).
- Combined registry 8728 -> **8728** if merged.

## Floor projection

- `protein_kinase_ser_thr_tyr`: 100 -> 100 (added 0; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Per-family caps: {'protein_kinase_ser_thr_tyr': 150}.

## Novelty gate

- Decisions: {'throttle': 1}.
- Reasons: {'redundant_no_novelty_signal': 1}.

## Hold reasons

- {}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
