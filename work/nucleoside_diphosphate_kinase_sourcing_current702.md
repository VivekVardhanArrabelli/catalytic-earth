# Nucleoside Diphosphate Kinase Sourcing - broadened evidence handles

Run: 2026-06-13T08:00:26Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.4.6 NDK rows via
Rhea NTP/NDP phosphoryl-transfer text, NDK family text, and active-site/
phosphohistidine/binding-site annotations. EC, keywords, names, UniProt prose,
and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: nucleoside_diphosphate_kinase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 238 (off-target held 0; disambiguation holds 0; skipped 2).
- **Novelty-admitted labels: 150** (throttled/rejected 1; held@cap 87).
- Combined registry 5985 -> **6135** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nucleoside_diphosphate_kinase | phosphohistidine_ntp_ndp_transfer_context | 0 | 150 | 150 | 150 | True | 87 |

## Novelty gate

- Decisions: {'admit': 237, 'throttle': 1}.
- Reasons: {'adds_diversity': 137, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'needed_fingerprint_but_redundant_ortholog': 1}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- NDK handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Protein-kinase/histidine-kinase/hydrolase/NMP-kinase side-EC boundary guards: True.
- Per-family cap ceiling: {'nucleoside_diphosphate_kinase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
