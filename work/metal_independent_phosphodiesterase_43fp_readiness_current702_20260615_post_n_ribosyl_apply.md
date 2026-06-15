# Metal-independent Phosphodiesterase 43fp Readiness

Created: 2026-06-15 after the N-ribosyl hydrolase cursor batch apply.

## Current State

- Latest factory:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_n_ribosyl_apply.json`.
- Current positive universe: `label_factory_v1_42fp`.
- Next required universe if this lane is implemented: `label_factory_v1_43fp`.
- Current counted surface: external rows 7570, combined labels 8272, no coverage holes, no
  under-floor fingerprints.
- Factory result: no existing lane has >=150 cap room; `metal_independent_phosphodiesterase` is the
  next high-yield blocked lane with projected clean admits 150.
- Bounded post-apply source-wall scout:
  `artifacts/v3_metal_independent_phosphodiesterase_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`.
  It fetched 68 reviewed rows across broad EC/family-handle windows, had 0 fetch failures, but only
  1 target mechanism-corroborated / novelty-admitted preview label. This is source-wall evidence
  only and is not apply-ready; the 43fp runner should use better lane splits/source handles rather
  than relying on the broad first windows alone.
- Source-handle count scout:
  `artifacts/v3_metal_independent_phosphodiesterase_source_handle_count_scout_current702_20260615_post_n_ribosyl_apply.json`.
  Promising reviewed counts for the future runner: `ec_3_1_4_catalytic_cyclic_amp_gmp` = 121,
  `phosphodiesterase_hydrolase_non_metal_keyword` = 224, and `ec_3_1_4_act_or_binding_site` = 718.
  Narrow name-only cyclic nucleotide PDE lanes are small (39-40). The `ec_4_6_1` cyclase probe is
  high-count (1389) but likely boundary-heavy and should not be the first apply lane without a
  stricter hydrolysis source wall preview.
- Targeted source-wall scout:
  `artifacts/v3_metal_independent_phosphodiesterase_targeted_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`.
  It fetched 157 rows from the cyclic AMP/GMP catalytic-activity and non-metal hydrolase handle
  lanes, with 0 fetch failures, but only 13 target mechanism-corroborated labels and 11
  novelty-admitted preview labels. These handles are better than broad EC windows but still far
  below a 150-row batch. The 43fp runner should add more specific source paths or lane splits before
  attempting an apply-sized preview.

## Mechanism Contract

- EC 3.1.4 / 4.6.1 are scope/fetch context only and must remain excluded/review-only context.
- Counted non-EC corroborators:
  - phosphodiesterase or cyclic-nucleotide phosphodiesterase family/name handle;
  - hydrolytic phosphodiester or cyclic-nucleotide P-O cleavage reaction evidence;
  - active-site acid/base or substrate-binding residue evidence where available.
- Holds:
  - metal-dependent phosphodiesterase/nuclease rows;
  - phosphomonoesterase and protein phosphatase rows;
  - phospholipase C / cyclase / lyase rows without hydrolytic phosphodiester cleavage;
  - kinase or transferase side rows;
  - EC-only rows and unresolved multi-fingerprint conflicts.
- Metal presence is a boundary/filter. Metal absence is not counted as evidence.

## Required Build Sequence

1. Add fingerprint `metal_independent_phosphodiesterase` and an ontology node for
   metal-independent hydrolytic phosphodiester/cyclic-nucleotide P-O cleavage.
2. Bump the live positive universe to `label_factory_v1_43fp`.
3. Add the `43fp` hard-negative preregistration constant/path and refresh/freeze the OOS
   preregistration before candidate selection.
4. Implement the reviewed-UniProt source runner with bounded windows and timeout-safe fetching.
5. Run non-destructive preview, row guardrail audit, novelty/governor/dedup/cap replay,
   source-contract/leakage validation, and full tests.
6. Apply only through an explicit command that prints frozen current702 sha before and after.

Do not apply from the existing preview-only source wall or from the design-only preregistration.
