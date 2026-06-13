# Thiamine Diphosphate Sourcing - broadened evidence handles

Run: 2026-06-13T05:13:32Z

Sources fresh reviewed Swiss-Prot bronze for ThDP-dependent enzymes via ThDP/Mg
cofactor or binding context, Rhea decarboxylation/carbonyl-transfer/ThDP participant
evidence, ThDP-family text, and active-/binding-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
PLP, molybdopterin/flavin/heme, kinase/phosphotransferase, hydrolase, side-EC,
and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: thiamine_diphosphate_enzyme.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 181 (off-target held 14; disambiguation holds 37; skipped 8).
- **Novelty-admitted labels: 150** (throttled/rejected 13; held@cap 18).
- Combined registry 5638 -> **5788** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| thiamine_diphosphate_enzyme | thdp_mg_ylide_carbonyl_substrate_context | 0 | 150 | 150 | 150 | True | 18 |

## Novelty gate

- Decisions: {'admit': 168, 'throttle': 13}.
- Reasons: {'adds_diversity': 68, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 13}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 37}.
- Off-target held counts: {'coa_acyltransferase': 14}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- ThDP handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- PLP/Mo/flavin/heme/kinase/hydrolase/side-EC boundary guards: True.
- Per-family cap ceiling: {'thiamine_diphosphate_enzyme': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
