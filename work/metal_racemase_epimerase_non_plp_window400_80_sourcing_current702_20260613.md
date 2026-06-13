# Non-PLP Racemase/Epimerase Sourcing - broadened evidence handles

Run: 2026-06-13T20:04:18Z

Sources fresh reviewed Swiss-Prot bronze for EC 5.1 non-PLP racemase/epimerase enzymes
via racemase/epimerase mechanism text, Rhea isomerization/racemization equations,
active-/binding-site annotations, metal context, or explicit cofactorless context.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
PLP, non-5.1 side-EC, transferase, hydrolase, oxidoreductase, and off-target fingerprint rows
are guarded or held.

## Result

- Families sourced: metal_racemase_epimerase_non_plp.
- Lanes queried: 1 (<= 500 rows each).
- Fetched candidate rows: 80.
- Target mechanism-corroborated bronze labels: 34 (off-target held 23; disambiguation holds 22; skipped 1).
- **Novelty-admitted labels: 21** (throttled/rejected 6; held@cap 7).
- Combined registry 7211 -> **7232** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| metal_racemase_epimerase_non_plp | racemase_epimerase_proton_shift_context | 129 | 21 | 150 | 150 | True | 7 |

## Novelty gate

- Decisions: {'admit': 28, 'throttle': 6}.
- Reasons: {'adds_diversity': 28, 'redundant_no_novelty_signal': 6}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 22}.
- Off-target held counts: {'nad_p_dehydrogenase': 23}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Racemase/epimerase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- PLP and side-EC boundary guards: True.
- Per-family cap ceiling: {'metal_racemase_epimerase_non_plp': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
