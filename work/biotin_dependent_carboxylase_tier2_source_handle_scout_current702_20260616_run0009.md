# Biotin-Dependent Carboxylase Sourcing - broadened evidence handles

Run: 2026-06-17T01:46:56Z

Sources fresh reviewed Swiss-Prot bronze for EC 6.4.1 / 6.3.4 biotin carboxylases
via biotin or biotinyl-Lys context, Rhea ATP/hydrogencarbonate/carboxybiotin
participant evidence, carboxylase family text, and active-/binding-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
kinase, non-biotin ATP ligase, hydrolase, transferase side-EC, non-scope side-EC,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: biotin_dependent_carboxylase.
- Lanes queried: 1 (<= 160 rows each).
- Per-lane record window: offset 0, limit 80.
- Source trust tier: source_tier_2.
- Unreviewed tier-2 lanes enabled: False (only: True).
- Fetched candidate rows: 80.
- Target mechanism-corroborated bronze labels: 16 (off-target held 0; disambiguation holds 1; skipped 63).
- **Novelty-admitted labels: 9** (throttled/rejected 7; held@cap 0).
- Combined registry 8728 -> **8737** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| biotin_dependent_carboxylase | biotinyl_lysine_atp_hydrogencarbonate_context | 100 | 9 | 109 | 150 | True | 0 |

## Novelty gate

- Decisions: {'admit': 9, 'throttle': 7}.
- Reasons: {'adds_diversity': 9, 'redundant_no_novelty_signal': 7}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 1}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Biotin carboxylase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Source trust tier: source_tier_2; tier-2 three-axis gate: True.
- Kinase/non-biotin ATP ligase/hydrolase/transferase/side-EC boundary guards: True.
- Per-family cap ceiling: {'biotin_dependent_carboxylase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
