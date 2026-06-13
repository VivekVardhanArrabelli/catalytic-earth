# Biotin-Dependent Carboxylase Sourcing - broadened evidence handles

Run: 2026-06-13T19:05:10Z

Sources fresh reviewed Swiss-Prot bronze for EC 6.4.1 / 6.3.4 biotin carboxylases
via biotin or biotinyl-Lys context, Rhea ATP/hydrogencarbonate/carboxybiotin
participant evidence, carboxylase family text, and active-/binding-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
kinase, non-biotin ATP ligase, hydrolase, transferase side-EC, non-scope side-EC,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: biotin_dependent_carboxylase.
- Lanes queried: 5 (<= 500 rows each).
- Fetched candidate rows: 139.
- Target mechanism-corroborated bronze labels: 0 (off-target held 0; disambiguation holds 55; skipped 84).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 7190 -> **7190** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| biotin_dependent_carboxylase | biotinyl_lysine_atp_hydrogencarbonate_context | 84 | 0 | 84 | 150 | False | 0 |

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 55}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Biotin carboxylase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Kinase/non-biotin ATP ligase/hydrolase/transferase/side-EC boundary guards: True.
- Per-family cap ceiling: {'biotin_dependent_carboxylase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
