# Metal-independent Phosphodiesterase Sourcing - broadened evidence handles

Run: 2026-06-15T18:54:38Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.1.4/4.6.1 metal-independent phosphodiesterases through phosphodiesterase family/name context, hydrolytic phosphodiester/cyclic-nucleotide reaction evidence, and active-/binding-site context where available.
EC / keyword / reaction text are scope-admission only, never predictive; metal-dependent phosphoesterase/nuclease, phosphatase, cyclase/lyase, kinase, transferase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: metal_independent_phosphodiesterase.
- Lanes queried: 5 (<= 80 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 265.
- Target mechanism-corroborated bronze labels: 18 (off-target held 52; disambiguation holds 183; skipped 12).
- **Novelty-admitted labels: 14** (throttled/rejected 4; held@cap 0).
- Combined registry 8272 -> **8286** if merged.

## Floor projection

- `metal_independent_phosphodiesterase`: 0 -> 14 (added 14; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Metal absence counted as evidence: False.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'metal_independent_phosphodiesterase': 150}.

## Novelty gate

- Decisions: {'admit': 14, 'throttle': 4}.
- Reasons: {'closes_hole_fingerprint': 14, 'needed_fingerprint_but_redundant_ortholog': 4}.

## Hold reasons

- {'no_mechanism_corroboration': 183}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
