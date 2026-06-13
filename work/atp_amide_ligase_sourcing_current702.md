# ATP Amide Ligase Sourcing - broadened evidence handles

Run: 2026-06-13T04:14:38Z

Sources fresh reviewed Swiss-Prot bronze for non-biotin EC 6.3 ATP-dependent amide
ligases via ATP/ADP/phosphate or Mg context, Ligase/ATP-grasp text, Rhea C-N/amide
ligation evidence, and active-/binding-site annotations.
EC, keywords, names, UniProt prose, and Rhea text are scope-admission only and never predictive;
biotin carboxylases, kinases/phosphotransferases, transferase/hydrolase side rows,
side-EC rows, and off-target fingerprint rows are guarded or held.

## Result

- Families sourced: atp_amide_ligase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 171 (off-target held 8; disambiguation holds 50; skipped 11).
- **Novelty-admitted labels: 150** (throttled/rejected 5; held@cap 16).
- Combined registry 5338 -> **5488** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atp_amide_ligase | atp_mg_acyl_phosphate_amide_ligation_context | 0 | 150 | 150 | 150 | True | 16 |

## Novelty gate

- Decisions: {'admit': 166, 'throttle': 5}.
- Reasons: {'adds_diversity': 66, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 2, 'redundant_no_novelty_signal': 3}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 50}.
- Off-target held counts: {'coa_acyltransferase': 3, 'flavin_dehydrogenase_reductase': 1, 'metallo_amidohydrolase_deaminase': 2, 'sam_methyltransferase': 2}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- ATP ligase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Biotin/kinase/transferase/hydrolase/side-EC boundary guards: True.
- Per-family cap ceiling: {'atp_amide_ligase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
