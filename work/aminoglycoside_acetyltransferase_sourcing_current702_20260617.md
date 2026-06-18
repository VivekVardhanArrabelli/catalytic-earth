# Aminoglycoside Acetyltransferase Sourcing - broadened evidence handles

Run: 2026-06-18T01:44:39Z

Sources fresh reviewed Swiss-Prot bronze for EC 2.3.1 aminoglycoside
acetyltransferases (AAC; GNAT fold) through AAC family/name context, acetyl-CoA
cosubstrate or binding context, and Rhea/reviewed N-acetyl-transfer text.
EC / keyword / reaction text are scope-admission only, never predictive;
generic CoA acyltransferases, aminoglycoside phosphotransferase (APH) and
nucleotidyltransferase (ANT), metal/flavin, side-EC, EC-only, and off-target
rows are guarded.

## Result

- Families sourced: aminoglycoside_acetyltransferase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 46.
- Target mechanism-corroborated bronze labels: 32 (off-target held 5; disambiguation holds 8; skipped 1).
- **Novelty-admitted labels: 32** (throttled/rejected 0; held@cap 0).
- Combined registry 8870 -> **8902** if merged.

## Floor projection

- `aminoglycoside_acetyltransferase`: 0 -> 32 (added 32; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'aminoglycoside_acetyltransferase': 150}.

## Novelty gate

- Decisions: {'admit': 32}.
- Reasons: {'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 6}.

## Hold reasons

- {'no_mechanism_corroboration': 8}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
