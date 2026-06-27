# Flavin-Disulfide-Reductase Sourcing - broadened evidence handles

Run: 2026-06-27T18:50:23Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.8.1 flavin-dependent disulfide
reductases (the class-I pyridine nucleotide-disulfide oxidoreductases:
glutathione / thioredoxin / trypanothione / lipoamide / CoA-disulfide reductases)
through an FAD cofactor plus a Rhea/reviewed NAD(P)H:disulfide reduction reaction and
a disulfide-reductase family/name or active-site handle. EC / keyword / reaction text
are scope-admission only, never predictive; sulfite reductase, non-flavin thiol-redox
enzymes, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: flavin_disulfide_reductase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 389.
- Target mechanism-corroborated bronze labels: 168 (off-target held 87; disambiguation holds 77; skipped 57).
- **Novelty-admitted labels: 150** (throttled/rejected 7; held@cap 11).
- Combined registry 9777 -> **9927** if merged.

## Floor projection

- `flavin_disulfide_reductase`: 0 -> 150 (added 150; cap 150; floor reached: True; held@cap 11).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'flavin_disulfide_reductase': 150}.

## Novelty gate

- Decisions: {'admit': 161, 'throttle': 7}.
- Reasons: {'adds_diversity': 61, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 7}.

## Hold reasons

- {'no_mechanism_corroboration': 77}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
