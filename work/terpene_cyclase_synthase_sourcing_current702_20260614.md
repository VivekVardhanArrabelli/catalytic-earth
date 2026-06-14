# Terpene Cyclase/Synthase Sourcing - broadened evidence handles

Run: 2026-06-14T01:52:41Z

Sources fresh reviewed Swiss-Prot bronze for EC 4.2.3 terpene cyclases/synthases
via terpene/cyclase family context, Mg/Mn or diphosphate evidence, and Rhea
diphosphate-release/cyclization context where available. EC / keyword / reaction
text are scope-admission only, never predictive; prenyltransferase, hydratase,
side-EC, EC-only, and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: terpene_cyclase_synthase.
- Lanes queried: 2 (<= 160 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 208.
- Target mechanism-corroborated bronze labels: 114 (off-target held 1; disambiguation holds 65; skipped 28).
- **Novelty-admitted labels: 112** (throttled/rejected 2; held@cap 0).
- Combined registry 7742 -> **7854** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| terpene_cyclase_synthase | metal_prenyl_diphosphate_and_carbocation_intermediate | 0 | 112 | 112 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 112, 'throttle': 2}.
- Reasons: {'adds_diversity': 12, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 2}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 65}.
- Off-target held counts: {'cytochrome_p450_monooxygenase': 1}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Terpene handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Boundary guards: True.
- Per-family cap ceiling: {'terpene_cyclase_synthase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
