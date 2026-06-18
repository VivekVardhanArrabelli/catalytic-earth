# Aminoacyl-tRNA-Synthetase Sourcing - broadened evidence handles

Run: 2026-06-18T18:57:12Z

Sources fresh reviewed Swiss-Prot bronze for EC 6.1.1 aminoacyl-tRNA
synthetases through an X--tRNA-ligase / aminoacyl-tRNA-synthetase family/name plus
a Rhea/reviewed aminoacylation reaction (ATP + amino acid + tRNA -> aminoacyl-tRNA
+ AMP + diphosphate).
EC / keyword / reaction text are scope-admission only, never predictive;
tRNA-modifying methyltransferases, pseudouridine synthases, CCA-adding
nucleotidyltransferases, amidotransferases,
side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: aminoacyl_trna_synthetase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 331.
- Target mechanism-corroborated bronze labels: 271 (off-target held 0; disambiguation holds 50; skipped 10).
- **Novelty-admitted labels: 150** (throttled/rejected 20; held@cap 101).
- Combined registry 9327 -> **9477** if merged.

## Floor projection

- `aminoacyl_trna_synthetase`: 0 -> 150 (added 150; cap 150; floor reached: True; held@cap 101).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'aminoacyl_trna_synthetase': 150}.

## Novelty gate

- Decisions: {'admit': 251, 'reject': 10, 'throttle': 10}.
- Reasons: {'adds_diversity': 151, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'fingerprint_over_cap_no_new_chemistry': 10, 'redundant_no_novelty_signal': 10}.

## Hold reasons

- {'no_mechanism_corroboration': 50}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
