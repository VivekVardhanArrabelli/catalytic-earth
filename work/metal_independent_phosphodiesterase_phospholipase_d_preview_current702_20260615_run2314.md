# Metal-independent Phosphodiesterase Sourcing - broadened evidence handles

Run: 2026-06-15T23:20:58Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.4/4.6.1 metal-independent phosphodiesterases through phosphodiesterase family/name context, hydrolytic phosphodiester/cyclic-nucleotide reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive; metal-dependent phosphoesterase/nuclease, phosphatase, cyclase/lyase, kinase, transferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: metal_independent_phosphodiesterase.
- Lanes queried: 1 (<= 80 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 22.
- Target mechanism-corroborated bronze labels: 7 (off-target held 4; disambiguation holds 11; skipped 0).
- **Novelty-admitted labels: 7** (throttled/rejected 0; held@cap 0).
- Combined registry 8522 -> **8529** if merged.

## Floor projection

- `metal_independent_phosphodiesterase`: 0 -> 7 (added 7; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Metal absence counted as evidence: False.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'metal_independent_phosphodiesterase': 150}.

## Novelty gate

- Decisions: {'admit': 7}.
- Reasons: {'closes_hole_fingerprint': 7}.

## Hold reasons

- {'no_mechanism_corroboration': 11}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
