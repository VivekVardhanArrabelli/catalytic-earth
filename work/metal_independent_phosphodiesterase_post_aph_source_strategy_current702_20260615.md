# Metal-independent Phosphodiesterase Post-APH Source Strategy

Run: 2026-06-15 automation `ce-nad-glyco-floor-expansion`

## Summary

After the APH tier-2 apply, `metal_independent_phosphodiesterase` is the only remaining
hole/under-floor fingerprint. It is still not apply-ready. The previously tested reviewed and
tier-2 UniProt handles are useful source-wall evidence but should not be retried as mass-growth
lanes without a materially sharper source split.

## Current state

- Combined label surface: 8422.
- Combined seed surface: 6726.
- External registry rows: 7720.
- Current positive universe: `label_factory_v1_44fp`.
- Coverage hole/under-floor fingerprint: `metal_independent_phosphodiesterase`.
- Ready existing lanes with >=150 projected clean admits: 0.
- Top factory projection: `short_chain_dehydrogenase_reductase` at 84 clean admits; PDE at 34 under
  current handles.

## Evidence already tested

Post-APH exact-EC distribution scout:

- Artifact:
  `artifacts/v3_metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.json`
- Report:
  `work/metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.md`
- Broad reviewed EC 3.1.4 count: 1086.
- Broad reviewed EC 3.1.4 after the current non-metal filter: 490.
- Exact cyclic-nucleotide candidate splits after the non-metal filter are all subscale:
  EC 3.1.4.17 = 6, EC 3.1.4.35 = 7, EC 3.1.4.53 = 2, EC 3.1.4.52 = 18,
  EC 3.1.4.37 = 15, EC 3.1.4.58 = 12.
- Interpretation: exact EC splits are too small for a 150-row batch, while broad EC/name windows
  are boundary-heavy and already failed preview gates.

Reviewed PDE preview:

- Artifact:
  `artifacts/v3_metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.json`
- Fetched rows: 265.
- Target mechanism-corroborated labels: 18.
- Novelty-admitted labels: 14.
- Interpretation: clean but far below the 150-row apply gate.

Alternate reviewed handles:

- Artifact:
  `artifacts/v3_metal_independent_phosphodiesterase_alternate_handle_preview_current702_20260615.json`
- Fetched rows: 130.
- Target labels: 0.
- Novelty-admitted labels: 0.
- Interpretation: not useful for mutation.

Tier-2 PDE handles:

- Artifact:
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_sourcing_preview_cursor_pages2_size100_current702_20260615.json`
- Fetched rows: 400.
- Target labels: 0.
- Novelty-admitted labels: 0.
- Off-target holds: 186.
- Trust-tier-insufficient holds: 197.
- Interpretation: the current tier-2 PDE handles are not source-wall safe for apply.

## Guardrail interpretation

- EC 3.1.4 / 4.6.1 remains scope/fetch context only.
- Metal absence is a boundary filter, not counted evidence.
- `predictive_evidence` must remain empty for annotation-sourced bronze.
- Tier-2 PDE still requires three independent non-EC mechanism axes.
- No existing PDE preview should be applied or padded.

## Next exact action

Do not retry the same PDE EC/name source handles as a mass-growth path. The exact-EC scout shows
the cyclic-nucleotide subfamilies are too small after the non-metal filter, while broad EC/name
windows are boundary-heavy. Either design a new mechanism-bearing PDE source wall beyond EC/name
counts, or pivot to a different high-yield family/source-tier strategy such as SDR/AKR or serine
beta-lactamase only after adding the family-specific source wall, OOS preregistration if the
fingerprint universe changes, non-destructive preview, row guardrail audit,
novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit apply.
