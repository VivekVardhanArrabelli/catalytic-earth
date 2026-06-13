# Non-PLP Racemase/Epimerase Sourcing - broadened evidence handles

Run: 2026-06-13T03:35:13Z

Sources fresh reviewed Swiss-Prot bronze for EC 5.1 non-PLP racemase/epimerase enzymes
via racemase/epimerase mechanism text, Rhea isomerization/racemization equations,
active-/binding-site annotations, metal context, or explicit cofactorless context.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
PLP, non-5.1 side-EC, transferase, hydrolase, oxidoreductase, and off-target fingerprint rows
are guarded or held.

## Result

- Families sourced: metal_racemase_epimerase_non_plp.
- Lanes queried: 1 (<= 320 rows each).
- Fetched candidate rows: 320.
- Target mechanism-corroborated bronze labels: 108 (off-target held 133; disambiguation holds 48; skipped 31).
- **Novelty-admitted labels: 108** (throttled/rejected 0; held@cap 0).
- Combined registry 5230 -> **5338** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| metal_racemase_epimerase_non_plp | racemase_epimerase_proton_shift_context | 0 | 108 | 108 | 150 | True | 0 |

## Novelty gate

- Decisions: {'admit': 108}.
- Reasons: {'adds_diversity': 8, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 48}.
- Off-target held counts: {'nad_p_dehydrogenase': 133}.

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
