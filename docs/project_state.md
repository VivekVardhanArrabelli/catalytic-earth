# Project State

Last refreshed: 2026-06-14

This file is the durable state summary for agents who do not have chat context.
Treat it as an orientation layer, not as a replacement for the referenced
artifacts.

Read order for a fresh run:

1. `docs/project_state.md`
2. `docs/decision_log.md`
3. `docs/artifact_index.md`
4. `docs/agent_runbook.md`

## North Star

Catalytic Earth is a mechanism-first enzyme atlas scaffold. The objective is a
computable map from sequence, structure, active-site geometry, catalytic roles,
cofactors, substrate-pocket constraints, reaction bond changes, and evolutionary
context to mechanism-level function hypotheses.

The repo is not an EC-number classifier, a wet-lab protocol, or a production
biological design system. Current benchmark claims must be framed as local,
artifact-backed mechanism diagnostics.

## Current Benchmark State

- **NON-HEME IRON 2OG CAPPED; COPPER POST-PREFIX SCOUT NO-YIELD (2026-06-13/14 automation).**
  The latest run continued the documented non-heme 2OG `140:10` slice and kept going through
  bounded windows until the family hit its cap. Applied windows `140:10`, `150:10`, `160:10`,
  `170:10`, `180:10`, and `190:10` added **27** gated source-tier-0 bronze rows and moved
  `non_heme_iron_2og_dioxygenase` **223 -> 250**, exactly at the non-confusable cap **250**.
  The final window had one gate-admitted row held by the cap guard. Do not continue this family
  under current cap policy.

  External bronze is now **6959**; combined label surface is **7661**. External-only split is
  **5735** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
  **5965**, leaving **4035** to 10k by that surface convention. Strict counters remain separate:
  **positive_bronze_count 5948**, **oos_bronze_count 1696**, **silver_ready_count 0**,
  **silver_confirmed_count 17**, **projected_provisional_count 0**.

  Guardrails held: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`; all new rows are bronze, automation-curated,
  `uniprot:*`, `source_tier_0`, and have nested `predictive_evidence []`. EC/name/Rhea/keyword/
  prose/feature handles remain excluded-context admission evidence only and EC is never counted.
  Row audit `artifacts/v3_non_heme_iron_2og_capped_row_guardrail_audit_current702_20260613.json`
  found **0** problems across **250** non-heme 2OG rows. Coverage audit reports **35**
  fingerprints, Gini **0.137**, holes `[]`, under-floor `[]`, next-batch floor deficit **0**, and
  only `metal_dependent_hydrolase` over-cap. Novelty replay over **6959** expansion rows reports
  decisions `{'admit': 6503, 'reject': 47, 'throttle': 409}` and would-not-readmit **456**
  (0.0655).

  Continuation work added fetch-only copper row-window controls to
  `scripts/source_copper_oxidoreductase_family.py` and
  `src/catalytic_earth/copper_oxidoreductase_sourcing.py`. A non-destructive copper
  post-prefix preview (`--max-records-per-lane 320 --record-offset-per-lane 240
  --record-limit-per-lane 40`) fetched **0** rows: current copper lanes have only **153**
  laccase/oxidase rows and **69** amine oxidase rows. `copper_oxidoreductase` remains **140/250**,
  but the current two source selectors are exhausted beyond the already-fetched prefix.

  Next action: do not continue capped non-heme 2OG. Do not replay the current copper lanes; scout
  alternate copper source handles with explicit non-EC mechanism corroborators, or run a clean
  source-supply scout/spec for another under-cap family such as manganese/iron SOD or zinc
  hydratase before any apply.
- **NON-HEME IRON 2OG WINDOWED EXTENSION APPLIED (2026-06-13 automation).**
  After the tier-2 floor run closed all under-floor lanes at their caps, the next useful path was a
  bounded under-cap family/source lane rather than more floor work. This run added fetch-window
  controls to `scripts/source_non_heme_iron_2og_family.py` and
  `src/catalytic_earth/non_heme_iron_2og_sourcing.py`: `--record-offset-per-lane` and
  `--record-limit-per-lane`. These are source-fetch controls only; they do not alter EC scope,
  mechanism corroboration, trust tiers, novelty, caps, or predictive evidence.

  Applied rows: six bounded windows over `non_heme_iron_2og_dioxygenase` applied **51** bronze
  rows: `80:10` (+17), `90:10` (+13), `100:10` (+15), `110:10` (+3), `120:10` (+2), and
  `130:10` (+1). The family moved **172 -> 223** under the non-confusable cap **250**; **27** cap
  slots remain. The final windows were low-yield, so any continuation should first preview
  `140:10` non-destructively.

  External bronze is now **6932**; combined label surface is **7634**. External-only split is
  **5708** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
  **5938**, leaving **4062** to 10k by that surface convention. Strict counters remain separate:
  **positive_bronze_count 5921**, **oos_bronze_count 1696**, **silver_ready_count 0**,
  **silver_confirmed_count 17**, **projected_provisional_count 0**.

  Guardrails held: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; all new rows are bronze,
  automation-curated, `uniprot:*`, `source_tier_0`, and have `predictive_evidence []`.
  EC/name/Rhea/keyword/prose/feature handles remain excluded-context admission evidence only and
  EC is never counted. Row audit
  `artifacts/v3_non_heme_iron_2og_windowed_row_guardrail_audit_current702_20260613.json` found
  **0** problems across **223** non-heme 2OG rows. Coverage audit reports **35** fingerprints,
  Gini **0.135**, holes `[]`, under-floor `[]`, next-batch floor deficit **0**, and only
  `metal_dependent_hydrolase` over-cap. Novelty replay over **6932** expansion rows reports
  decisions `{'admit': 6476, 'reject': 47, 'throttle': 409}` and would-not-readmit **456**
  (0.0658).

  Next action: preview the next non-heme 2OG slice (`--record-offset-per-lane 140
  --record-limit-per-lane 10`) only if a bounded cap-fill is still the best 10k-path use of time;
  otherwise scout a clean new family/source lane. Do not count these bronze rows as silver or
  projected rows.
- **TIER-2 FLOOR EXPANSION CAPPED (2026-06-13 automation).**
  The latest run added an explicit trust-tier parameter to the existing cofactor/EC
  disambiguation path and wired opt-in unreviewed UniProt tier-2 lanes for the three remaining
  under-floor families. Defaults remain `source_tier_0`; unreviewed lanes require
  `--source-tier source_tier_2` and the existing `source_trust_tiers.evaluate_corroboration`
  three-axis gate. EC remains scope-only and non-counted. The run also added source-window controls
  to PfkB and biotin after the first applies so continuation windows could skip already-applied
  source rows without changing admission or leakage behavior.

  Applied rows: `glycoside_hydrolase` **84 -> 150** (+66 across windows `0:40`, `40:40`, and
  `80:40`), `biotin_dependent_carboxylase` **84 -> 150** (+66 across windows `0:40` and `40:40`),
  and `pfkb_ribokinase_family` **46 -> 150** (+104 across windows `0:80` and `80:40`). All three
  former under-floor fingerprints are now exactly at their chemistry-confusable **150** cap.
  External bronze is now **6881**; combined label surface is **7583**. External-only split is
  **5657** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
  **5887**, leaving **4113** to 10k by that surface convention. Strict counters remain separate:
  **positive_bronze_count 5870**,
  **oos_bronze_count 1696**, **silver_ready_count 0**, **silver_confirmed_count 17**,
  **projected_provisional_count 0**.

  Guardrails held: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; all **236** new rows are
  bronze, automation-curated, `uniprot:*`, `source_tier_2`, and have `predictive_evidence []`.
  EC/name/Rhea/keyword/prose/feature handles remain excluded-context admission evidence only and
  EC is never counted. Row audit
  `artifacts/v3_tier2_floor_expansion_row_guardrail_audit_current702_20260613.json` found **0**
  problems. Coverage audit reports **35** fingerprints, Gini **0.1312**, holes `[]`,
  under-floor `[]`, next-batch floor deficit **0**, and only `metal_dependent_hydrolase` over-cap.
  Novelty replay over **6881** expansion rows reports decisions
  `{'admit': 6425, 'reject': 47, 'throttle': 409}` and would-not-readmit **456** (0.0663).

  Next action: floor closure is no longer the urgent lane, and these three families should not
  continue under current cap policy. Scout/spec a clean new family/source lane next. Do not count
  tier-2 bronze rows as silver or projected rows.
- **WINDOWED COA/P450/MOLYBDOPTERIN CAP-FILLS APPLIED (2026-06-13 automation).**
  The latest run added source-window controls to the CoA acyltransferase, cytochrome P450, and
  molybdopterin source runners, then used bounded windows to avoid monolithic live UniProt entry
  fetches. These controls are source-fetch only and do not change admission, trust-tier, novelty,
  caps, or predictive evidence.

  Applied rows: `molybdopterin_oxidoreductase` **207 -> 250** (+43),
  `cytochrome_p450_monooxygenase` **248 -> 250** (+2), and `coa_acyltransferase`
  **188 -> 250** (+62). All three are now exactly at their non-confusable **250/250** cap and
  should not continue under the current cap policy. External bronze is now **6645**; combined label
  surface is **7347**. External-only split is **5421** seed-fingerprint rows and **1224** OOS rows.
  Combined seed-fingerprint label surface is **5651**, leaving **4349** to 10k by that surface
  convention. Strict counters remain separate: **positive_bronze_count 5634**,
  **oos_bronze_count 1696**, **silver_ready_count 0**, **silver_confirmed_count 17**,
  **projected_provisional_count 0**.

  Guardrails held: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; all new rows are bronze,
  automation-curated, `uniprot:*`, and have `predictive_evidence []`; EC/name/Rhea/keyword/prose/
  feature handles remain excluded-context admission evidence only and EC is never counted. Row audit
  `artifacts/v3_windowed_capfills_row_guardrail_audit_current702_20260613.json` found **0**
  problems across **750** rows in the three touched families. Coverage audit reports **35**
  fingerprints, Gini **0.1704**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
  `metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
  **6645** expansion rows reports decisions `{'admit': 6189, 'reject': 47, 'throttle': 409}` and
  would-not-readmit **456** (0.0686).

  A strict-kinase GHMP-like entry/Rhea scout generated **0** labels and should not be wired next:
  the existing GHMP fingerprint is already **150/150** and registry-new supply was sparse. Next
  action: remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase
  **84/100**. Build a genuinely new non-EC mechanism corroborator/source path for those floors, or
  scout/spec a clean new family not already capped.
- **ISOMERASE CAP-FILL APPLIED; GLYCOSIDE ALTERNATE SCOUTS NO-YIELD (2026-06-13 automation).**
  The latest run first pursued the remaining under-floor glycoside path without relaxing
  mechanism-first gates. A base glycoside page-2 continuation over rows **581-660**
  (`scripts/source_glycoside_hydrolase_family.py --query-pages-per-lane 2 --record-offset-per-lane 580 --record-limit-per-lane 80`)
  fetched **80**, mechanism-corroborated/admitted **0**, held **57** no-corroboration rows,
  skipped **23**, and recorded **1** Rhea HTTP 500 (`Q59675`). A new source-fetch-only flag,
  `--only-alternate-name-lanes`, was added so the alternate chitinase/beta-glucanase/glycoside-
  hydrolase name lane can be scouted without refetching the base lane; the first untried
  alternate-only window (`--record-offset-per-lane 40 --record-limit-per-lane 80`) fetched **80**,
  mechanism-corroborated/admitted **0**, and held **80** no-corroboration rows. These artifacts are
  no-apply: `artifacts/v3_glycoside_hydrolase_page2_window580_80_sourcing_preview_current702_20260613.json`
  and
  `artifacts/v3_glycoside_hydrolase_alt_name_only_window40_80_sourcing_preview_current702_20260613.json`.

  Because under-floor source paths remained no-yield and substantial run time remained, the run
  executed the documented smallest under-cap cap-fill:
  `scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --apply`.
  Result: fetched **405**, target mechanism-corroborated **91**, novelty gate admitted **80**
  before the cap guard, applied **8**, held@cap **72**, novelty-throttled/rejected **11**, held
  **61** off-target `nad_p_dehydrogenase` rows, held **90** no-corroboration rows, skipped **163**,
  and had **0** fetch failures on the apply rerun. Frozen current702 stayed byte-unchanged with
  sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.

  External bronze is now **6538**; combined label surface is **7240**;
  `cofactor_independent_isomerase` is **150/150** and should not continue under the current
  chemistry-confusable cap. External-only split is **5314** seed-fingerprint rows and **1224** OOS
  rows. Combined seed-fingerprint label surface is **5544**, leaving **4456** to 10k by that
  surface convention. Strict source-trust counters remain separate:
  **positive_bronze_count 5527**, **oos_bronze_count 1696**, **silver_ready_count 0**,
  **silver_confirmed_count 17**, **projected_provisional_count 0**. Row audit
  `artifacts/v3_cofactor_independent_isomerase_capfill_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **150** isomerase rows. Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_isomerase_capfill_applied.json`
  reports **35** fingerprints, fingerprint Gini **0.1611**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
  `metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
  **6538** expansion rows reports decisions `{'admit': 6082, 'reject': 47, 'throttle': 409}` and
  would-not-readmit **456** (0.0697).

  Next action: remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase
  **84/100**. Do not continue capped isomerase/racemase/GHMP/ThDP-style chemistry-confusable lanes
  without a cap-policy change. Build a genuinely new non-EC mechanism corroborator/source path for
  PfkB/biotin/glycoside, or scout/spec a clean new family not already at cap. Guardrails:
  EC/name/Rhea/keyword/prose/feature handles stay excluded-context admission evidence only, EC is
  never counted, and `predictive_evidence []`.
- **RACEMASE WINDOW400:80 CAP-FILL APPLIED; STRICT KINASE SOURCE-SUPPLY SCOUT WRITTEN (2026-06-13 automation).**
  The latest run applied the bounded non-PLP metal racemase/epimerase continuation from the prior
  handoff after the remaining under-floor source paths were documented no-yield/source-limited.
  Command:
  `scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 400 --record-limit-per-lane 80 --cap-ceiling 150 --apply`.
  Result: fetched **80**, mechanism-corroborated **34**, novelty gate admitted **28** before cap,
  applied **21**, held@cap **7**, novelty-throttled/rejected **6**, held **23** off-target
  `nad_p_dehydrogenase` rows, held **22** no-corroboration rows, skipped **1**, and had **0** fetch
  failures. Frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.

  External bronze is now **6530**; combined label surface is **7232**;
  `metal_racemase_epimerase_non_plp` is **150/150** and should not continue under the current
  chemistry-confusable cap. External-only split is **5306** seed-fingerprint rows and **1224** OOS
  rows. Combined seed-fingerprint label surface is **5536**, leaving **4464** to 10k by that
  surface convention. Strict source-trust counters remain separate:
  **positive_bronze_count 5519**, **oos_bronze_count 1696**, **silver_ready_count 0**,
  **silver_confirmed_count 17**, **projected_provisional_count 0**. Row audit
  `artifacts/v3_metal_racemase_epimerase_non_plp_window400_80_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **150** racemase rows. Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_window400_80_applied.json`
  reports **35** fingerprints, fingerprint Gini **0.1619**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
  `metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
  **6530** expansion rows reports decisions `{'admit': 6074, 'reject': 47, 'throttle': 409}` and
  would-not-readmit **456** (0.0698).

  Continuation work wrote a strict-kinase source-supply scaffold after a bounded entry/Rhea scout
  blocked before artifact write in `fetch_uniprot_entry` TLS handshake. Blocker:
  `artifacts/v3_strict_kinase_subclass_entry_fetch_blocker_after_racemase_cap_current702_20260613.json`.
  Source-supply scout:
  `artifacts/v3_strict_kinase_subclass_source_supply_scout_after_racemase_cap_current702_20260613.json`
  sampled **60** TSV rows with **0** fetch failures and generated **0** labels; it ranks
  `galactokinase_mevalonate_homoserine` first by reviewed supply (**613** total) but the first
  sample window was only **1/20 registry-new**. Next action: do not wire a full kinase fingerprint
  from this scout alone. Run a deeper windowed source scout plus a small entry/Rhea mechanism
  corroborator scout, or return to genuinely new PfkB/biotin/glycoside source paths. Guardrails:
  EC/name/Rhea/keyword/prose/feature handles stay excluded-context admission evidence only, EC is
  never counted, and `predictive_evidence []`.
- **RACEMASE WINDOWED TOP-UP APPLIED; UNDER-FLOOR ALTERNATE SCOUTS NO-YIELD (2026-06-13 automation).**
  The latest run first tried the remaining under-floor path without relaxing mechanism-first gates:
  optional biotin alternate floor-closure lanes fetched **139** reviewed candidates but admitted
  **0** because all registry-new rows lacked non-EC mechanism corroboration; optional glycoside
  alternate-name lanes fetched **80** and admitted **0** for the same reason; zinc hydratase
  under-cap preview fetched **160**, mechanism-corroborated **3**, but novelty-throttled all 3 as
  redundant. No labels from those previews were applied.

  The run then added row-window support to the non-PLP metal racemase/epimerase source runner and
  applied the previously unprocessed rows **321-400** via
  `scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 320 --record-limit-per-lane 80 --cap-ceiling 150 --apply`.
  Result: fetched **80**, mechanism-corroborated **21**, applied **21**, held **49** off-target
  `nad_p_dehydrogenase` rows, held **10** no-corroboration rows, skipped **0**, novelty-throttled
  **0**, held@cap **0**, and had **0** fetch failures. Frozen current702 stayed byte-unchanged
  with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went
  only to `data/registries/external_bronze_labels.json`.

  External bronze is now **6509**; combined label surface is **7211**;
  `metal_racemase_epimerase_non_plp` is **129/150** under cap. Honest counters remain separate:
  **positive_bronze 5515**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
  **projected 0**. External-only bronze split is **5285** seed-fingerprint rows and **1224** OOS
  rows. Remaining positive-bronze gap to 10k is **4485**. Row audit
  `artifacts/v3_metal_racemase_epimerase_non_plp_window_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **129** racemase rows. Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_window320_80_applied.json`
  reports **35** fingerprints, fingerprint Gini **0.1643**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
  `metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_racemase_window320_80_applied.json`
  reports **6509** expansion rows, decisions `{'admit': 6053, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0701). Next action: remaining floors PfkB **46/100**, biotin
  **84/100**, and glycoside hydrolase **84/100** still require genuinely new non-EC
  corroborator/source paths; racemase may continue only as a bounded cap-fill window
  (`--record-offset-per-lane 400 --record-limit-per-lane 80`) with cap 150 inspected first.
- **GLYCOSIDE HYDROLASE FLOOR-WINDOW APPLIED; PAGING SUPPORT ADDED (2026-06-13 automation).**
  The latest run continued the under-floor `glycoside_hydrolase` lane and added row-window/paging
  support to the glycoside source path so durable slices of UniProt search results can be processed
  before expensive entry/Rhea fetches. A monolithic 500-row retry was stopped while blocked in a
  UniProt entry read before artifact write. The productive windowed apply used
  `--max-records-per-lane 500 --record-offset-per-lane 420 --record-limit-per-lane 80`, fetched
  **80**, mechanism-corroborated **14**, applied **12**, held **66** no-corroboration rows,
  skipped **0**, off-target held **0**, novelty-throttled **2**, held@cap **0**, and had **0**
  fetch failures on the apply rerun. Frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.
  External bronze is now **6488**; combined surface is **7190**; `glycoside_hydrolase` is
  **84/150** and still below the 100 floor. Honest counters remain separate:
  **positive_bronze 5494**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
  **projected 0**; remaining positive-bronze gap to 10k is **4506**. External-only bronze split is
  **5264** seed-fingerprint rows and **1224** OOS rows. Row audit
  `artifacts/v3_glycoside_hydrolase_floor500_window_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **84** glycoside hydrolase rows, with active-site/residue-role,
  domain/family, and Rhea axes on every row and no EC axis counted. Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.json`
  reports **35** fingerprints, fingerprint Gini **0.1675**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
  `metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.json`
  reports **6488** expansion rows, decisions `{'admit': 6032, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0703). A second-page preview over rows 501-580
  (`artifacts/v3_glycoside_hydrolase_page2_window500_80_sourcing_preview_current702_20260613.json`)
  fetched **80** but mechanism-corroborated/admitted **0**; do not apply it. Guardrails remain
  active: EC/name/Rhea/keyword/prose/feature handles are excluded-context admission evidence only,
  EC is never counted, and `predictive_evidence []`. Next action: do not repeat the applied
  `420:80` glycoside window or the zero-yield `500:80` page-2 window; build a genuinely new strict
  PfkB/biotin source/corroborator path or an alternate glycoside source lane with non-EC mechanism
  corroboration.
- **GLYCOSIDE HYDROLASE TOP-UP APPLIED; FLOOR STILL OPEN (2026-06-13 automation).**
  The latest run continued the under-floor `glycoside_hydrolase` lane through the existing
  mechanism-first admission pipeline. A 420-row top-up preview/apply fetched **420** reviewed
  EC 3.2.1 candidates, mechanism-corroborated **27**, applied **27**, held **290**
  no-corroboration rows, skipped **103**, held **0** off-target rows, novelty-throttled **0**,
  held@cap **0**, and had **0** fetch failures. Frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.
  External bronze is now **6476**; combined surface is **7178**; `glycoside_hydrolase` is
  **72/150** and still below the 100 floor. Honest counters remain separate:
  **positive_bronze 5482**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
  **projected 0**; remaining positive-bronze gap to 10k is **4518**. External-only bronze split is
  **5252** seed-fingerprint rows and **1224** OOS rows. Row audit
  `artifacts/v3_glycoside_hydrolase_topup_row_guardrail_audit_current702_20260613.json` found
  **0** problems across all **72** glycoside hydrolase rows, with active-site/residue-role,
  domain/family, and Rhea axes on every row and no boundary tokens in mechanism evidence.
  Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_topup_applied.json`
  reports **35** fingerprints, fingerprint Gini **0.1699**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, only
  `metal_dependent_hydrolase` over-cap, and next-batch floor deficit **98**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_topup_applied.json`
  reports **6476** expansion rows, decisions `{'admit': 6020, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0704).
  Guardrails remain active: EC/name/Rhea/keyword/prose/feature handles are excluded-context
  admission evidence only, EC is never counted, and `predictive_evidence []`. A follow-on
  `--max-records-per-lane 650` attempt was rejected by the runner cap of 500; a 500-row preview was
  stopped for closeout before artifact write while in UniProt entry TLS/connect work. Blocker:
  `artifacts/v3_glycoside_hydrolase_floor_topup_live_fetch_blocker_current702_20260613.json`.
  Validation: focused pytest **313 passed + 14 subtests**, `validate` ok (12 source / 35
  fingerprints / 32 ontology families / 702 labels). Next action: retry the 500-row glycoside
  preview early, or add paging/resume support; remaining floors are PfkB **46/100**, glycoside
  hydrolase **72/100**, and biotin **84/100**.
- **GLYCOSIDE HYDROLASE 35FP BRONZE LANE APPLIED (2026-06-13 automation).**
  The preceding run selected a new clean 10k-path family after PfkB/biotin remained source-limited and
  a GHKL histidine-kinase scout found only **1** likely wireable reviewed row. Glycoside hydrolase
  was wired through the full mechanism-first pipeline: `glycoside_hydrolase` fingerprint,
  `glycosidic_bond_hydrolysis` ontology node, `label_factory_v1_35fp`, OOS preregistration re-freeze
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_35fp_1025.json`,
  disambiguation/trust-tier/leakage/coverage tests, non-destructive preview, and explicit `--apply`
  with frozen current702 sha checks. Growth went only to
  `data/registries/external_bronze_labels.json`; frozen current702 remains **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
  The production apply fetched **240** reviewed EC 3.2.1 candidates, mechanism-corroborated **45**,
  applied **45**, held **155** no-corroboration rows, skipped **40**, off-target held **0**,
  novelty-throttled **0**, held@cap **0**, and recorded **1** Rhea timeout fetch failure
  (`P19531`). Glycoside hydrolase moved **0 -> 45** under the chemistry-confusable cap 150 and is
  still below floor.
  External bronze is now **6449**; combined surface is **7151**. Honest counters remain separate:
  **positive_bronze 5438**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
  **projected 0**; remaining positive-bronze gap to 10k is **4562**. External-only bronze split is
  **5225** seed-fingerprint rows and **1224** OOS rows. Row audit
  `artifacts/v3_glycoside_hydrolase_row_guardrail_audit_current702_20260613.json` found **0**
  problems across **45** rows, with active-site/residue-role, domain/family, and Rhea axes on every
  row and no boundary tokens in mechanism evidence. Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_applied.json`
  reports **35** fingerprints, fingerprint Gini **0.1753**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **125**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_applied.json`
  reports **6449** expansion rows, decisions `{'admit': 5993, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0707). Guardrails: EC/name/Rhea/keyword/prose/feature handles are
  excluded-context admission evidence only, EC is never counted, `predictive_evidence []`, and
  glycosyltransferase/transglycosylase/phosphorylase/lyase/side-EC/multi-signal rows are held.
  Validation: focused pytest **313 passed + 14 subtests**, `validate` ok (12 source / 35
  fingerprints / 32 ontology families / 702 labels). Next action: close remaining floors through
  gated top-up/new-source work: glycoside hydrolase **45/100**, PfkB **46/100**, or biotin
  **84/100**.
- **MN/FE SUPEROXIDE DISMUTASE 34FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The previous handoff's `manganese_iron_superoxide_dismutase` lane was wired through the full
  mechanism-first pipeline: fingerprint + `metal_superoxide_dismutation` ontology node,
  `label_factory_v1_34fp`, OOS preregistration re-freeze
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_34fp_1025.json`,
  disambiguation/trust-tier/leakage tests, non-destructive preview, and explicit `--apply` with
  frozen current702 sha checks. Growth went only to `data/registries/external_bronze_labels.json`;
  frozen current702 remains **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
  Initial apply fetched **240**, mechanism-corroborated **181**, applied **164**, held **59**
  no-corroboration rows, novelty-throttled **17**, and moved SOD **0 -> 164**. A bounded top-up
  fetched **252**, skipped **164** already-existing rows, mechanism-corroborated **19**, applied
  **2**, held **69** no-corroboration rows, novelty-throttled **17**, and moved SOD **164 -> 166**
  under the non-confusable cap 250. External bronze is now **6404**; combined surface is **7106**.
  Honest counters remain separate: **positive_bronze 5393**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to
  10k is **4607**. External-only bronze split is **5180** seed-fingerprint rows and **1224** OOS
  rows. Row audit
  `artifacts/v3_manganese_iron_superoxide_dismutase_row_guardrail_audit_current702_20260613.json`
  found **0** problems across **166** rows, with active-site/residue-role, cofactor/cosubstrate,
  and Rhea axes on every row. Post-apply coverage audit
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.json` reports
  **34** fingerprints, fingerprint Gini **0.1608**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **70**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.json` reports
  **6404** expansion rows, decisions `{'admit': 5948, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0712). Guardrails: EC/name/Rhea/keyword/prose/feature handles are
  excluded-context admission evidence only, EC is never counted, `predictive_evidence []`, and
  Cu/Zn SOD/heme/peroxidase/superoxide-reductase/side-EC/multi-signal rows are held. Validation:
  focused pytest **301 passed + 14 subtests**, `validate` ok (12 source / 34 fingerprints /
  31 ontology families / 702 labels). Next action: do not repeat the exhausted SOD previews; build a
  new strict source/corroborator path for PfkB **46/100** or biotin **84/100**, or scout/spec the
  next clean fingerprint family through the same gated pipeline.
- **MN/FE SUPEROXIDE DISMUTASE SOURCE BLOCKER CLEARED; 34FP NEXT-LANE SPEC WRITTEN (2026-06-13 automation).**
  Follow-up to the bounded no-yield previews: a PfkB/biotin alternate-source scout found only limited
  registry-new reviewed supply and boundary-heavy rows, so this run switched to a cleaner new-family
  scout rather than forcing under-floor labels. The earlier breadth-feasibility result had treated
  Mn/Fe SOD as source-poor because a cofactor-comment-only query reached only one reviewed entry.
  A corrected guarded query for reviewed EC 1.15.1.1 Mn/Fe superoxide dismutases now finds **252**
  reviewed rows. In an 80-row mechanism sample, **80/80** rows were registry-new, **80/80** carried
  RHEA:20696/superoxide dismutation reaction context, **80/80** carried Mn/Fe metal context,
  **80/80** carried SOD family text, **77/80** carried active/binding/metal-site evidence, and **0**
  showed the explicit Cu/Zn/heme/side-EC boundary flags. No labels were generated and no registry
  write was performed. Artifacts:
  `artifacts/v3_pfkb_biotin_alternate_source_scout_current702_20260613.json`,
  `work/pfkb_biotin_alternate_source_scout_current702_20260613.md`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.json`,
  `work/manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.md`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.json`, and
  `work/manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.md`. Counts remain
  external bronze **6238**, combined surface **6940**, frozen current702 **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; honest counters remain
  separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**. Next exact action: wire
  `manganese_iron_superoxide_dismutase` as a deliberate `label_factory_v1_34fp` lane only through
  the full pipeline: fingerprint + `metal_superoxide_dismutation` ontology node, OOS prereg
  re-freeze, disambiguation/trust-tier/leakage tests, non-destructive preview, then `--apply` only
  if novelty/dedup/governor/trust-tier gates pass. Required guards: hold Cu/Zn SOD, heme/cytoglobin/
  hemoglobin/peroxidase/nitrite/nitric-oxygen dioxygenase, superoxide reductase, side-EC, EC-only,
  and multi-fingerprint-signal rows.
- **BOUNDED UNDER-CAP PREVIEWS CLEARED FETCH BLOCKER BUT ADMITTED 0 ROWS (2026-06-13 automation).**
  Follow-up to the immediately previous blocked run: bounded live previews now complete and write
  artifacts, so the blocker was not a broken gate. It was the larger sequential UniProt entry/Rhea
  evidence-fetch workload before artifact write. Tested bounded first windows across approved
  under-cap lanes: `cofactor_independent_isomerase` at 5 rows/lane (fetched 14, mechanism 0,
  admitted 0) and 20 rows/lane (fetched 67, mechanism 0, admitted 0), `coa_acyltransferase` 20
  rows/lane (fetched 75, mechanism 0, admitted 0), `non_heme_iron_2og_dioxygenase` 20 rows/lane
  (fetched 66, mechanism 3, admitted 0; all novelty-throttled as redundant), `molybdopterin_
  oxidoreductase` 20 rows/lane (fetched 67, mechanism 2, admitted 0; novelty-throttled), `zinc_
  lyase_hydratase` 20 rows/lane (fetched 20, mechanism 0, admitted 0), and `copper_oxidoreductase`
  20 rows/lane (fetched 40, mechanism 1, admitted 0; novelty-throttled). Aggregate artifact/report:
  `artifacts/v3_under_cap_bounded_preview_no_yield_current702_20260613.json` and
  `work/under_cap_bounded_preview_no_yield_current702_20260613.md`. No `--apply` was run.
  Counts remain external bronze **6238**, combined surface **6940**, frozen current702 **702** with
  sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; honest counters remain
  separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**. Next action: do not repeat the same bounded first-window
  probes; build a new PfkB/biotin source path, run a deeper under-cap extension only with enough
  closeout time, or scout/spec a cleaner new family.
- **UNDER-CAP EXTENSION PREVIEWS BLOCKED BY LIVE FETCH LATENCY (2026-06-13 automation).**
  Latest state still has `pfkb_ribokinase_family` **46/100** and
  `biotin_dependent_carboxylase` **84/100** under floor, with current strict reviewed source paths
  exhausted under mechanism-first gates. This run therefore attempted bounded, already approved
  under-cap extension/cap-fill previews instead of relaxing EC scope rules: CoA/acyl-CoA
  acyltransferase at **188/250** with 500 and 280 rows/lane, then cofactor-independent isomerase at
  **142/150** with 120 rows/lane. All three live preview attempts were terminated after no preview
  artifact was produced quickly enough for a safe inspect/apply/validate cycle; no `--apply` was
  run and no registry rows changed. Blocker artifacts:
  `artifacts/v3_under_cap_extension_live_fetch_blocker_current702_20260613.json` and
  `work/under_cap_extension_live_fetch_blocker_current702_20260613.md`. Counts remain external
  bronze **6238**, combined surface **6940**, frozen current702 **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; honest counters remain
  separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**. Next exact action is to retry the smallest bounded
  cap-fill first:
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`,
  then inspect `floor_projection`, novelty, held@cap, trust-tier, namespace/tier/review-status,
  leakage, and excluded-context fields before any apply. Do not add more P450 without explicit new
  reaction/organism justification because it is **248/250**.
- **P450 + COPPER EXTENSION BRONZE APPLIES COMPLETED (2026-06-13 automation).**
  The latest handoff left `pfkb_ribokinase_family` and `biotin_dependent_carboxylase` under floor,
  but both current reviewed source paths are exhausted under strict gates. This run therefore used
  already approved, non-confusable extension lanes with remaining reviewed supply:
  `cytochrome_p450_monooxygenase` and `copper_oxidoreductase`. P450 extension preview
  `artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json` fetched
  **337**, mechanism-corroborated **189**, applied **138**, held **35** no-corroboration rows,
  skipped **113** already-covered/current-registry rows, novelty-throttled **51**, held **0** at
  cap, and moved P450 **110 -> 248** under cap 250. Copper extension preview
  `artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json` fetched
  **222**, mechanism-corroborated **81**, applied **21**, held **20** no-corroboration rows,
  skipped **121**, novelty-throttled **60**, held **0** at cap, and moved copper **119 -> 140**.
  External bronze **6079 -> 6238**; combined surface **6781 -> 6940**; frozen current702 remains
  702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
  Honest counters remain separate: **positive_bronze 5227**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to
  10k: **4773**. External-only bronze split is 5014 seed-fingerprint rows and 1224 OOS rows. Fresh
  coverage audit:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.json`
  reports **6940** combined, **33** fingerprints, fingerprint Gini **0.1633**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **70**. Novelty replay:
  **6238** expansion rows, decisions `{'admit': 5782, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0731). Row guardrail audits found **0** problems across all
  138 P450 rows and 21 copper rows; all added rows keep `predictive_evidence []`, EC/name/keyword/
  Rhea/prose/feature handles remain excluded-context admission evidence, and EC is never a counted
  corroborator. Validation: focused pytest **304 passed + 14 subtests**, `validate` ok
  (12 source / 33 fingerprints / 30 ontology families / 702 labels). Next action: do not add more
  P450 without explicit new reaction/organism justification because P450 is **248/250**. PfkB
  remains **46/100** and biotin **84/100**; find genuinely new source paths for those strict lanes
  or scout/spec a new family if evidence is cleaner than further balanced-lane top-ups.
- **PFKB/RIBOKINASE-FAMILY 33FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The strict kinase-subclass path continued from the guarded post-PfkA handoff. Added
  `pfkb_ribokinase_family` fingerprint + `pfkb` ontology mapping, bumped the universe to
  `label_factory_v1_33fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`. EC 2.7.1 is
  scope-only; counted mechanism handles are ATP/ADP phosphoryl-transfer Rhea participants with
  PfkB/ribokinase-family acceptors, PfkB-family/domain text, ATP/Mg/substrate active-/binding-site
  evidence, cofactor/cosubstrate handles, and structure-compatible evidence. Protein kinases,
  two-component histidine kinases, hydrolase/nuclease rows, NDK, dNK, ASKHA, GHMP, PfkA,
  cross-subclass/side-EC signals, and multi-fingerprint rows are held; generic `fructokinase` is no
  longer a counted PfkB family token because it shadowed PfkA `6-phosphofructokinase`. Apply fetched
  **88**, mechanism-corroborated **46**, applied **46**, held **36** no-corroboration rows, skipped
  **2**, off-target held **4** as `askha_sugar_acetate_kinase`, held **0** at cap, and throttled
  **0**. External bronze **6033 -> 6079**; combined surface **6735 -> 6781**; frozen current702
  remains 702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
  Honest counters remain separate: **positive_bronze 5085**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to
  10k: **4915**. External-only bronze split is 4855 seed-fingerprint rows and 1224 OOS rows. Fresh
  coverage audit: **6781** combined, **33** fingerprints, fingerprint Gini **0.162**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **70**. Novelty replay:
  **6079** expansion rows, decisions `{'admit': 5623, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.075). Validation: focused pytest **294 passed + 14 subtests**,
  `validate` ok (12 source / 33 fingerprints / 30 ontology families / 702 labels). Row audit
  `artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json` found **0**
  problems across all 46 PfkB rows and all four mechanism axes present on every row. Follow-on
  floor-extension scout
  `artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json` fetched 88
  reviewed rows again with `--max-records-per-lane 500`, found **0** new PfkB labels, skipped **48**
  already-covered rows, held **36** no-corroboration rows, held **4** off-target ASKHA rows, and
  left PfkB **46/100**. All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/
  feature handles remain excluded-context admission evidence and are never predictive. Next action:
  do not broad-wire EC 2.7; close the biotin 16-row deficit, design a genuinely new PfkB
  source/handle path with stronger corroboration, or choose a new 10k-path family through the full
  gated pipeline.
- **PFKA PHOSPHOFRUCTOKINASE 32FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The strict kinase-subclass path continued from the post-dNK scout. Added
  `pfka_phosphofructokinase` fingerprint + existing `pfka` ontology mapping, bumped the universe to
  `label_factory_v1_32fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`. EC 2.7.1 is
  scope-only; counted mechanism handles are ATP/ADP phosphoryl-transfer Rhea participants with
  fructose-6-phosphate, PfkA/ATP-dependent 6-phosphofructokinase family text, ATP/Mg/substrate
  active-/binding-site evidence, cofactor/cosubstrate handles, and structure-compatible evidence.
  Protein kinases, two-component histidine kinases, hydrolase/nuclease rows, NDK, dNK, ASKHA, GHMP,
  PfkB/ribokinase, cross-subclass signals, and multi-fingerprint rows are held. Apply fetched
  **240**, mechanism-corroborated **233**, applied **150**, held **5** no-corroboration rows,
  skipped **2**, held **83** at cap, and held **0** off-target rows. External bronze
  **5883 -> 6033**; combined surface **6585 -> 6735**; frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 5039**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **4961**. Fresh
  coverage audit: **6735** combined, **32** fingerprints, fingerprint Gini **0.1465**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap,
  next-batch floor deficit **16**. Novelty replay: **6033** expansion rows, decisions
  `{'admit': 5577, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0756). Validation:
  focused pytest **312 passed + 14 subtests**, `validate` ok (12 source / 32 fingerprints /
  30 ontology families / 702 labels). Row audit
  `artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json` found **0**
  problems across all 150 PfkA rows and all four mechanism axes present on every row. All added
  rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
  excluded-context admission evidence and are never predictive. The coverage audit now also carries
  the missing `deoxynucleoside_kinase` accounting signature, so seed-positive totals reconcile to
  **5039** across the 32-fingerprint distribution. Follow-on scaffold
  `work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md` is non-importing: PfkB has
  reviewed supply **85** and sampled **28/40** likely wireable, so tighten/re-scout PfkB before any
  33fp path or choose a stronger scaling-plan family if evidence is cleaner. Do not broad-wire
  EC 2.7 or merge kinase subclasses.
- **DEOXYNUCLEOSIDE KINASE 31FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The strict kinase-subclass path continued from the ASKHA/GHMP handoff. Added
  `deoxynucleoside_kinase` fingerprint + existing `dnk` ontology mapping, bumped the universe to
  `label_factory_v1_31fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_31fp_1025.json`. EC 2.7.1 is
  scope-only; counted mechanism handles are ATP/ADP phosphoryl-transfer Rhea participants with
  deoxynucleoside substrates, dNK/thymidine/deoxycytidine/deoxyguanosine kinase family text,
  ATP/substrate active-/binding-site evidence, cofactor/cosubstrate handles, and
  structure-compatible evidence. Protein kinases, two-component histidine kinases,
  hydrolase/nuclease rows, NDK, ASKHA, GHMP, PfkA/PfkB, cross-subclass signals, and
  multi-fingerprint rows are held. Apply fetched **240**, mechanism-corroborated **237**, applied
  **150**, held **87** at cap, and held **0** off-target rows. External bronze **5733 -> 5883**;
  combined surface **6435 -> 6585**; frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 4889**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **5111**. Fresh
  coverage audit: **6585** combined, **31** fingerprints, fingerprint Gini **0.1534**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap,
  next-batch floor deficit **16**. Novelty replay: **5883** expansion rows, decisions
  `{'admit': 5427, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0775). Validation:
  focused pytest **293 passed**, `validate` ok (12 source / 31 fingerprints / 30 ontology families /
  702 labels), JSON/JSONL parse checks, and `git diff --check` passed. Row audit
  `artifacts/v3_deoxynucleoside_kinase_row_guardrail_audit_current702_20260613.json` found **0**
  problems across all 150 dNK rows and all four mechanism axes present on every row. All added rows
  keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
  excluded-context admission evidence and are never predictive. Follow-on scout
  `artifacts/v3_strict_kinase_subclass_source_scout_after_dnk_current702_20260613.json` generated no
  labels and selected strict `pfka_phosphofructokinase` as the next candidate: reviewed supply
  **386**, sampled **40/40** likely wireable, **0/40** boundary signals. Do not broad-wire EC 2.7 or
  merge kinase subclasses; next full lane should be strict PfkA through a 32fp prereg/preview/apply
  pipeline.
- **ASKHA + GHMP 30FP BRONZE EXPANSIONS APPLIED (2026-06-13 automation).**
  The strict kinase-subclass path continued from the post-NDK scout. Added
  `askha_sugar_acetate_kinase` fingerprint + `askha` ontology node (`label_factory_v1_29fp`) and
  `ghmp_small_molecule_kinase` fingerprint + `ghmp` ontology node (`label_factory_v1_30fp`);
  re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_29fp_1025.json` and
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_30fp_1025.json`. EC 2.7.1 is
  scope-only for both lanes; counted mechanism handles are ATP/ADP phosphoryl-transfer Rhea
  participants, ASKHA/GHMP family text, ATP/Mg or substrate active-/binding-site evidence,
  cofactor/cosubstrate handles, and structure-compatible evidence. Protein kinases,
  two-component histidine kinases, hydrolase/nuclease rows, NDK, dNK, Pfk, cross-subclass
  ASKHA/GHMP signals, and multi-fingerprint rows are held. ASKHA apply fetched **240**,
  mechanism-corroborated **227**, applied **150**, held **9** no-corroboration rows, throttled
  **7**, and held **70** at cap. GHMP apply fetched **240**, mechanism-corroborated **228**,
  applied **150**, held **10** no-corroboration rows, throttled **0**, and held **78** at cap.
  External bronze **5433 -> 5733**; combined surface **6135 -> 6435**; frozen current702 remains
  702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest
  counters remain separate: **positive_bronze 4739**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **5261**. Fresh
  coverage audit: **6435** combined, **30** fingerprints, fingerprint Gini **0.1534**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap,
  next-batch floor deficit **16**. Novelty replay: **5733** expansion rows, decisions
  `{'admit': 5277, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0795).
  Validation: focused pytest **280 passed**, `validate` ok (12 source / 30 fingerprints /
  30 ontology families / 702 labels), JSON/JSONL parse checks, and `git diff --check` passed. All
  added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
  excluded-context admission evidence and are never predictive. Next full lane should be strict
  `deoxynucleoside_kinase` via the 31fp pipeline scaffolded in
  `work/deoxynucleoside_kinase_next_lane_spec_current702_20260613.md`; do not broad-wire EC 2.7 or
  merge kinase subclasses.
- **BIOTIN FLOOR-CLOSURE + STRICT NDK 28FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  A Rhea-first biotin floor-closure scout kept the ATP + hydrogencarbonate/CO2/carboxylation gate
  intact and found only **3** additional safe rows; `biotin_dependent_carboxylase` is now **84/100**
  and remains under floor by **16**. The fallback narrow kinase-subclass path then split strict
  `nucleoside_diphosphate_kinase` from broad EC 2.7 after a clean scout (714 reviewed rows, 80/80
  sampled wireable, 0 sampled side-EC boundaries). Added the `nucleoside_diphosphate_kinase`
  fingerprint + `phosphohistidine_ntp_transfer` ontology family, bumped the universe to
  `label_factory_v1_28fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_28fp_1025.json`. EC 2.7.4.6 is
  scope-only; counted handles are Rhea NTP/NDP phosphoryl-transfer participants, NDK family text,
  active-site phosphohistidine/catalytic-His or binding-site evidence, and structure. Protein
  kinases, two-component histidine kinases, hydrolase/nuclease rows, adenylate/guanylate/NMP kinase
  side ECs, and multi-fingerprint rows are held. NDK apply fetched **240**, mechanism-corroborated
  **238**, applied **150** at the chemistry-confusable cap, held@cap **87**, throttled **1**, and
  held **0** off-target rows. External bronze **5280 -> 5433**; combined surface **5982 -> 6135**;
  frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 4439**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **5561**. Fresh
  coverage audit: **6135** combined, **28** fingerprints, fingerprint Gini **0.1608**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap,
  next-batch floor deficit **16**. Novelty replay: **5433** expansion rows, decisions
  `{'admit': 4977, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0839). Validation:
  focused pytest **230 passed + 14 subtests**, `validate` ok (12 source / 28 fingerprints /
  30 ontology families / 702 labels), JSON/JSONL parse checks, and `git diff --check` passed.
  Follow-on scout
  `artifacts/v3_strict_kinase_subclass_source_scout_after_ndk_current702_20260613.json` generated
  no labels but sampled strict kinase splits: deoxynucleoside kinase **278 reviewed / 39-of-40
  likely wireable / 1 boundary**, GHMP small-molecule kinase **613 / 37-of-40 / 0**, and ASKHA
  sugar/acetate kinase **667 / 39-of-40 / 0**. Next full lane should be strict
  `askha_sugar_acetate_kinase` through the usual fingerprint/ontology -> 29fp OOS prereg ->
  disambiguation tests -> preview -> gated apply path. Do not broad-wire EC 2.7, merge kinase
  subclasses, or count EC as mechanism evidence.
- **BIOTIN-DEPENDENT CARBOXYLASE 27FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  Latest handoff blocked broad EC 2.7 kinase and recommended a guarded biotin-carboxylase lane if
  mechanism-first handles were clean. Added `biotin_dependent_carboxylase` fingerprint +
  `biotin_carboxyl_transfer` ontology family, bumped the universe to `label_factory_v1_27fp`, and
  re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_27fp_1025.json`. EC 6.4.1 /
  6.3.4 is scope-only; counted handles require biotin/biotinyl-Lys evidence plus ATP/
  hydrogencarbonate/carboxybiotin reaction context, carboxylase family text, or active-/binding-site
  evidence. A guardrail correction removed **12** EC 6.3.4.15 biotin-protein ligase rows that lacked
  carboxylation chemistry, leaving **81** valid bronze rows. External bronze **5199 -> 5280**;
  combined surface **5901 -> 5982**; frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 4269**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **5731**. Fresh
  post-biotin coverage audit: **5982** combined, **27** fingerprints, fingerprint Gini **0.1655**,
  holes `[]`, under-floor `['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase`
  over-cap, next-batch floor deficit **19**. Novelty replay: **5280** expansion rows, decisions
  `{'admit': 4824, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0864). Validation:
  focused pytest **391 passed + 14 subtests**, `validate` ok (12 source / 27 fingerprints /
  29 ontology families / 702 labels), JSON/JSONL parse checks, and `git diff --check` passed.
  Follow-on: try a non-destructive biotin floor-closure scout that keeps ATP + hydrogencarbonate/
  CO2/carboxybiotin chemistry mandatory; if reviewed supply cannot close the 19-row deficit, return
  to a narrow kinase-subclass scout. Do not broad-wire EC 2.7 or admit biotin-protein ligases.
- **ZINC LYASE/HYDRATASE 26FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  Latest handoff recommended guarded `zinc_lyase_hydratase` after the ThDP apply. Added the
  `zinc_lyase_hydratase` fingerprint + `zinc_hydro_lyase` ontology family, bumped the universe to
  `label_factory_v1_26fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_26fp_1025.json`. EC 4.2.1 is
  scope-only; counted handles come from Zn cofactor/site evidence, Rhea hydration/dehydration/
  carbonic reaction text, Lyase/hydratase family text, or active-/binding-/metal-site evidence. PLP,
  ThDP, hydrolase/transferase/aldolase/isomerase side rows, non-4.2.1 side ECs, and multi-signal
  rows are held. Live apply
  `PYTHONPATH=src python scripts/source_zinc_lyase_hydratase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`
  fetched **240**, mechanism-corroborated **116**, admitted/applied **113**, held **57** off-target
  rows (`nad_p_dehydrogenase` 47, `metallophosphomonoesterase` 6,
  `metallo_amidohydrolase_deaminase` 4), held **10** no-corroboration rows, throttled **3**, and
  skipped **0** duplicates. External bronze **5086 -> 5199**; combined surface **5788 -> 5901**;
  frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 4188**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **5812**. Fresh
  post-zinc coverage audit: **5901** combined, fingerprint Gini **0.1559**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Novelty replay: **5199**
  expansion rows, decisions `{'admit': 4743, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0877). Validation: focused pytest **387 passed + 14 subtests**,
  `validate` ok (12 source / 26 fingerprints / 28 ontology families / 702 labels), JSON parse
  checks, and `git diff --check` passed. Follow-on: do not broad-wire EC 2.7 kinase; next scout
  should split a narrow kinase subclass or test a guarded biotin-carboxylase handle.
- **THIAMINE DIPHOSPHATE 25FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The broad EC 2.7 kinase lane remains blocked by subclass mixing, so this run selected the next
  clean fallback from the post-class-II scout: `thiamine_diphosphate_enzyme`. Mechanism scout
  `artifacts/v3_thiamine_diphosphate_mechanism_handle_scout_current702_20260613.json` examined
  **80** reviewed entries with **0** fetch failures and found ThDP context **80/80**, Rhea
  cross-reference **80/80**, Mg context **77/80**, active/binding-site context **73/80**, Rhea
  carbonyl/decarboxylation/transfer text **62/80**, and likely wireable rows **65/80**; flavin,
  side-EC, and kinase/hydrolase boundary signals forced explicit guards. Added
  `thiamine_diphosphate_enzyme` fingerprint + `thiamine_diphosphate_ylide` ontology family, bumped
  the universe to `label_factory_v1_25fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_25fp_1025.json`. EC
  2.2.1/4.1.1/1.2.4 is scope-only; counted handles come from ThDP/Mg cofactor or binding context,
  Rhea decarboxylation/carbonyl-transfer/ThDP participant evidence, ThDP-family keyword/domain text,
  or active-/binding-site evidence. PLP, molybdopterin/flavin/heme, kinase/phosphotransferase,
  hydrolase, side-EC, and multi-signal rows are held. Live apply
  `PYTHONPATH=src python scripts/source_thiamine_diphosphate_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`
  fetched **240**, mechanism-corroborated **181**, admitted/applied **150**, held **14** off-target
  `coa_acyltransferase` rows, held **37** no-corroboration rows, and skipped **0** duplicates.
  External bronze **4936 -> 5086**; combined surface **5638 -> 5788**; frozen current702 remains
  702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
  Honest counters remain separate: **positive_bronze 4075**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to
  10k: **5925**. Fresh post-ThDP coverage audit: **5788** combined, fingerprint Gini **0.1541**,
  holes `[]`, only `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Novelty
  replay: **5086** expansion rows, decisions `{'admit': 4630, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0897). Validation: focused pytest **80 passed**, leakage prereg/import
  subset **5 passed, 181 deselected**, and `validate` ok (12 source / 25 fingerprints / 27 ontology
  families / 702 labels). Follow-on: zinc lyase/hydratase mechanism scout
  `artifacts/v3_zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.json` found a viable
  but guarded next lane (50/80 likely wireable; 30/80 side-EC/boundary rows). Next concrete action:
  wire `zinc_lyase_hydratase` as a guarded 26fp lane only if tests/OOS prereg/preview gates pass.
- **ATP AMIDE LIGASE + CLASS-II METAL ALDOLASE 24FP BRONZE EXPANSIONS APPLIED (2026-06-13 automation).**
  The latest handoff state superseded the prompt's older P450 direction: P450/2OG/CoA/isomerase/
  molybdopterin/copper/racemase were already applied, so this run applied the next handoff lane
  `atp_amide_ligase`, then used a post-ATP source-supply scout to select
  `class_ii_metal_aldolase`. ATP wiring added the `atp_amide_ligase` fingerprint, attached the
  lane to the existing `atp_grasp` ontology context, bumped the universe to `label_factory_v1_23fp`,
  re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_23fp_1025.json`, and applied
  **150** bronze rows from reviewed Swiss-Prot. Guardrails: EC 6.3 is scope-only; counted handles
  come from ATP/ADP/phosphate/Mg, Ligase/ATP-grasp keyword/domain, Rhea amide/C-N/acyl-phosphate
  chemistry, or active-/binding-site evidence; biotin/carboxylase, kinase/phosphotransferase,
  hydrolase/transferase side rows, and multi-signal rows are held. The class-II scout
  `artifacts/v3_class_ii_metal_aldolase_mechanism_handle_scout_current702_20260613.json` examined
  80 entries with 0 fetch failures and supported a guarded 24fp lane: `class_ii_metal_aldolase`
  fingerprint + `carbon_carbon_lyase` ontology family, EC 4.1.2/4.1.3 scope-only, metal/Lyase/
  aldolase/C-C/Rhea/active-site corroborators, PLP/ThDP/Schiff-class-I/hydrolase/transferase/
  oxidoreductase/side-EC/multi-signal guards, and OOS preregistration re-frozen as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_24fp_1025.json`. Live apply
  `PYTHONPATH=src python scripts/source_atp_amide_ligase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`
  fetched **240**, mechanism-corroborated **171**, admitted/applied **150**, and held **8**
  off-target rows. Live apply
  `PYTHONPATH=src python scripts/source_class_ii_metal_aldolase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`
  fetched **240**, mechanism-corroborated **182**, admitted/applied **150**, and held **7**
  off-target rows. Net registry state: external bronze **4636 -> 4936**, combined label surface
  **5338 -> 5638**, frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 3925**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **6075**. Fresh
  post-class-II coverage audit: **5638** combined, fingerprint Gini **0.1581**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Novelty replay: **4936**
  expansion rows, decisions `{'admit': 4480, 'reject': 47, 'throttle': 409}`, would-not-readmit
  **456** (0.0924). Validation: focused pytest **156 passed**, leakage prereg/import-gate subset
  **14 passed, 171 deselected**, import/transfer-scope tests **133 passed**, and `validate` ok
  (12 source / 24 fingerprints / 26 ontology families / 702 labels). Follow-on: source-supply scout
  ranked `atp_phosphotransferase_kinase` first, but the kinase mechanism scout showed broad EC 2.7 is
  not clean enough (75/80 multi-subclass boundary rows; only 4 likely wireable). Next concrete action
  is to split a narrow kinase subclass or select the next cleaner lane, with ThDP enzyme the best
  fallback candidate.
- **COPPER + NON-PLP RACEMASE/EPIMERASE 22FP BRONZE EXPANSIONS APPLIED (2026-06-13 automation).**
  The latest handoff state superseded the prompt's older P450 direction: P450/2OG/CoA/isomerase/
  molybdopterin were already applied, so this run applied the next handoff lane
  `copper_oxidoreductase`, then used a post-copper source-supply scout to select
  `metal_racemase_epimerase_non_plp`. Copper wiring added the `copper_oxidoreductase` fingerprint +
  `copper_redox` ontology family, bumped the universe to `label_factory_v1_21fp`, re-froze OOS
  preregistration as `artifacts/v3_external_hard_negative_next_tranche_preregistration_21fp_1025.json`,
  and applied **119** bronze rows from reviewed Swiss-Prot. Post-copper scout
  `artifacts/v3_next_lane_source_supply_scout_after_copper_current702_20260613.json` recommended
  `metal_racemase_epimerase_non_plp`; mechanism scout
  `artifacts/v3_metal_racemase_epimerase_mechanism_handle_scout_current702_20260613.json` examined
  80 entries with 0 fetch failures and found strong non-EC handles (Isomerase keyword 80/80, Rhea
  80/80, isomerization text 80/80, racemase/epimerase text 78/80, active/binding-site context
  59/80 and 70/80) plus PLP/side-EC boundary signals. The lane was wired as a deliberate 22fp
  universe change: `metal_racemase_epimerase_non_plp` fingerprint +
  `stereochemical_isomerization` ontology family, EC 5.1 scope-only rule, racemase/epimerase/
  mutarotase text, Rhea isomerization/racemization, Isomerase keyword/domain, active-/binding-site,
  metal, or cofactorless mechanism corroboration, PLP and side-EC guards, and OOS preregistration
  re-frozen as `artifacts/v3_external_hard_negative_next_tranche_preregistration_22fp_1025.json`.
  Live apply
  `PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 320 --cap-ceiling 150 --apply`
  fetched **320** rows, mechanism-corroborated **108**, admitted/applied **108**, held **133**
  off-target `nad_p_dehydrogenase` rows, held **48** no-corroboration rows, skipped **31**, and
  reached the floor at **108/150**. Net registry state after both applies: external bronze
  **4409 -> 4636**, combined surface **5111 -> 5338**, frozen current702 remains 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: **positive_bronze 3625**, **oos_bronze 1696**, **silver_ready 0**,
  **silver_confirmed 17**, **projected 0**; remaining positive-bronze gap to 10k: **6375**. Fresh
  post-racemase coverage audit: **5338** combined, fingerprint Gini **0.1665**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Novelty replay: **4636**
  expansion rows, decisions `{'admit': 4180, 'reject': 47, 'throttle': 409}`, would-not-readmit
  **456** (0.0984). Validation: focused pytest **399 passed, 14 subtests passed**; `validate` ok
  (12 source / 22 fingerprints / 25 ontology families / 702 labels); JSON parse and diff checks ok.
  Next concrete action: mechanism-handle scout **`atp_amide_ligase`** (EC 6.3, confusable cap 150)
  before any 23fp wiring; use ATP/Mg/acyl-phosphate/amide-ligase Rhea or Ligase/ATP-grasp
  keyword/domain plus active-/binding-site evidence as counted corroborators, EC scope-only, and
  guard kinases/biotin carboxylases/ATP transferases/hydrolase side rows.
- **MOLYBDOPTERIN OXIDOREDUCTASE 20FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The post-isomerase recommended lane was scouted, wired, re-frozen, previewed, and applied as a
  deliberate 20-fingerprint universe change. Mechanism-handle scout:
  `artifacts/v3_molybdopterin_oxidoreductase_mechanism_handle_scout_current702_20260613.json`
  examined 80 reviewed UniProt entries with **0 fetch failures**; handles were Mo-cofactor
  **80/80**, Rhea cross-reference **78/80**, Mo feature/ligand context **65/80**, redox reaction
  text **49/80**, and oxo-transfer reaction text **71/80**, with heme/flavin/peroxidase boundary
  signals recorded as guards. New family/gate surface: `molybdopterin_oxidoreductase` fingerprint +
  `molybdopterin_redox` ontology node,
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = label_factory_v1_20fp`, OOS preregistration
  re-frozen as `artifacts/v3_external_hard_negative_next_tranche_preregistration_20fp_1025.json`,
  EC 1.* oxidoreductase scope-only rule with molybdopterin/Mo-cofactor, Rhea redox/oxo-transfer,
  Molybdenum keyword/domain, Mo-pterin feature/ligand, and active-/binding-/metal-site mechanism
  corroboration; hydrolase, non-oxidoreductase side-EC, peroxide/peroxidase, biosynthesis, and
  multi-fingerprint-signal rows stay held. Live apply:
  `PYTHONPATH=src python scripts/source_molybdopterin_oxidoreductase_family.py --max-records-per-lane 80 --apply`
  fetched **255** rows -> target mechanism-corroborated **210** -> gate-admitted before cap **207**
  -> appended **207** bronze rows; `molybdopterin_oxidoreductase` **0 -> 207** (cap 250; floor
  reached); **0 held at cap**, **3 novelty-throttled**, **41 disambiguation holds**
  (`no_mechanism_corroboration`), **0 off-target matches held**, **4 skipped**, duplicate skipped at
  apply **0**. External bronze **4202 -> 4409**; combined surface **4904 -> 5111**; frozen current702
  stayed 702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`
  before/after apply. Honest counters remain separate after apply: **positive_bronze 3398**,
  **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Fresh coverage
  audit: **5111** combined, fingerprint Gini **0.1613**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Novelty replay: **4409**
  expansion rows, decisions `{'admit': 3953, 'reject': 47, 'throttle': 409}`, would-not-readmit
  **456** (0.1034). Spot-check over all 207 Mo rows found **0** leakage/trust-tier problems; axes:
  cofactor/cosubstrate 207, active-site/residue-role 206, domain/family 206, Rhea participant 206.
  Validation: focused pytest **111 passed**, selected leakage prereg/import-gate pytest
  **10 passed, 171 deselected**, JSON parse checks ok, and `validate` ok
  (12 source / 20 fingerprints / 23 ontology families / 702 labels). Next concrete action:
  use the copper mechanism-handle scout
  (`artifacts/v3_copper_oxidoreductase_mechanism_handle_scout_current702_20260613.json`) as design
  input for possible 21fp wiring. It examined 80 entries with 0 fetch failures and found Rhea
  78/80, redox text 77/80, copper feature/ligand context 31/80, and explicit copper cofactor
  comments 20/80, plus small heme/side-EC/glycosyltransferase boundary signals. Keep EC scope-only
  and design explicit heme/flavin/molybdopterin/hydrolase/glycosyltransferase guards before any
  copper preview/apply.
- **COFACTOR-INDEPENDENT ISOMERASE 19FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  In the same productive block as the CoA lane below, the post-CoA recommended lane was wired as a
  deliberate 19-fingerprint universe change and applied through the canonical external bronze writer.
  New family/gate surface: `cofactor_independent_isomerase` fingerprint + `isomerization` ontology
  node, `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = label_factory_v1_19fp`, OOS preregistration
  re-frozen as `artifacts/v3_external_hard_negative_next_tranche_preregistration_19fp_1025.json`,
  EC 5.3 scope-only rule with Rhea isomerization equation text, Isomerase keyword/domain, and
  active-/binding-site/base mechanism corroboration, plus non-5.3 side-EC guards. Live apply:
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 80 --apply`
  fetched **266** rows -> target mechanism-corroborated **147** -> gate-admitted before cap **142** ->
  appended **142** bronze rows; `cofactor_independent_isomerase` **0 -> 142** (chemistry-confusable
  cap 150; floor reached); **0 held at cap**, **5 novelty-throttled**, **70 disambiguation holds**
  (`no_mechanism_corroboration`), **28 off-target matches held** (`nad_p_dehydrogenase`), **21
  skipped**, duplicate skipped at apply **0**. Net registry result after the CoA + isomerase block:
  external bronze **3872 -> 4202** (+330); combined surface **4574 -> 4904**; frozen current702
  stayed 702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`
  before/after both applies. Honest counters remain separate after apply: **positive_bronze 3191**,
  **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Fresh coverage
  audit: **4904** combined, fingerprint Gini **0.1613**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Novelty replay: **4202**
  expansion rows, decisions `{'admit': 3746, 'reject': 47, 'throttle': 409}`, would-not-readmit
  **456** (0.1085). Validation: targeted pytest **95 passed**, selected leakage prereg/import-gate
  pytest **8 passed**, selected transfer-scope pytest **1 passed**, and `validate` ok
  (12 source / 19 fingerprints / 22 ontology families / 702 labels). Artifacts/reports:
  `artifacts/v3_cofactor_independent_isomerase_sourcing_preview_current702.json`,
  `work/cofactor_independent_isomerase_sourcing_current702.md`,
  `work/cofactor_independent_isomerase_apply_current702_20260613.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_isomerase_applied.json`,
  `work/coverage_redundancy_audit_current702_20260613_isomerase_applied.md`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_isomerase_applied.json`,
  `work/novelty_admission_gate_audit_current702_20260613_isomerase_applied.md`. Follow-on scout:
  `artifacts/v3_next_lane_source_supply_scout_after_isomerase_current702_20260613.json` recommends
  **molybdopterin oxidoreductase** next over copper (460 reviewed rows and 33 distinct full ECs in a
  200-row sample vs 222/12). Both are reaction-poor, so the next safe action is a mechanism-handle
  scout plus subclass/boundary guard design before any preview/apply.
- **CoA ACYLTRANSFERASE 18FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  The post-2OG next lane was wired as a deliberate 18-fingerprint universe change and applied through
  the canonical external bronze writer. New family/gate surface: `coa_acyltransferase` fingerprint +
  `acyl_transfer` ontology node, `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION =
  label_factory_v1_18fp`, OOS preregistration re-frozen as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_18fp_1025.json`, EC 2.3.1
  scope-only rule with CoA/acyl-CoA Rhea participant, CoA/acyl-CoA feature text, Acyltransferase
  keyword/domain, and active-/binding-site mechanism corroboration, plus hydrolase side-EC guards.
  Live apply:
  `PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 80 --apply`
  fetched **218** rows -> target mechanism-corroborated **204** -> gate-admitted before cap **188** ->
  appended **188** bronze rows; `coa_acyltransferase` **0 -> 188** (cap 250; floor reached);
  **0 held at cap**, **16 novelty-throttled**, **11 disambiguation holds**
  (`no_mechanism_corroboration`), **1 off-target match held** (`metallo_amidohydrolase_deaminase`),
  **2 skipped**, fetch failures **0**, duplicate skipped at apply **0**. Net registry result:
  external bronze **3872 -> 4060** (+188); combined surface **4574 -> 4762**; frozen current702
  stayed 702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`
  before/after apply. Honest counters remain separate after apply: **positive_bronze 3049**,
  **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Fresh coverage
  audit: **4762** combined, fingerprint Gini **0.1652**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Validation: focused pytest
  over sourcing/disambiguation/leakage/coverage/novelty passed, and `validate` ok
  (12 source / 18 fingerprints / 21 ontology families / 702 labels). Artifacts/reports:
  `artifacts/v3_coa_acyltransferase_sourcing_preview_current702.json`,
  `work/coa_acyltransferase_sourcing_current702.md`,
  `work/coa_acyltransferase_apply_current702_20260613.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_coa_applied.json`,
  `work/coverage_redundancy_audit_current702_20260613_coa_applied.md`. Follow-on scouts recommend
  **cofactor-independent isomerase** next (5273 reviewed rows, 51 distinct full ECs in a 200-row
  sample, no reaction-poor warning). Mechanism-handle scout over 80 entries found catalytic activity
  context **80/80**, Rhea cross-reference **62/80**, active-or-binding-site context **65/80**, and
  fetch failures **0**; it also surfaced multi-EC boundary rows requiring explicit off-target guards.
- **NON-HEME IRON 2OG 17FP BRONZE EXPANSION APPLIED (2026-06-13 automation).**
  After the P450 lane below completed early in the same productive block, the documented next lane
  was wired as a deliberate 17-fingerprint universe change and applied through the canonical
  external bronze writer. New family/gate surface: `non_heme_iron_2og_dioxygenase` fingerprint +
  `non_heme_iron_oxygenation` ontology node,
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = label_factory_v1_17fp`, OOS preregistration
  re-frozen as `artifacts/v3_external_hard_negative_next_tranche_preregistration_17fp_1025.json`,
  EC 1.14.11 scope-only rule with Fe(II), 2-oxoglutarate/succinate/CO2 Rhea participant,
  Dioxygenase keyword/domain, and active/binding-site mechanism corroboration, plus heme/flavin/
  peroxide guards. Live apply:
  `PYTHONPATH=src python scripts/source_non_heme_iron_2og_family.py --max-records-per-lane 80 --apply`
  fetched **212** rows -> target mechanism-corroborated **198** -> gate-admitted before cap
  **172** -> appended **172** bronze rows; `non_heme_iron_2og_dioxygenase` **0 -> 172** (cap 250;
  floor reached); **0 held at cap**, **26 novelty-throttled**, **12 disambiguation holds**
  (`multi_fingerprint_signal_conflict` 5, `no_mechanism_corroboration` 7), **2 skipped**, fetch
  failures **0**. Net registry result across the P450 + 2OG run: external bronze **3590 -> 3872**
  (+282); combined surface **4292 -> 4574**; frozen current702 stayed 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after both applies.
  Honest counters remain separate after apply: **positive_bronze 2861**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Guardrails verified: EC scope-only
  and never counted; 2OG/keyword/Rhea/active-site handles admission/excluded-context only;
  `predictive_evidence []`; all added labels are `tier=bronze`, `review_status=automation_curated`,
  `uniprot:*`; dedup vs both registries; caps held. Fresh coverage audit: **4574** combined,
  fingerprint Gini **0.1657**, holes `[]`, only `metal_dependent_hydrolase` over-cap, next-batch
  floor deficit **0**. Validation so far: targeted pytest **275 passed, 14 subtests** over
  P450/2OG/NAD/SAM sourcing, disambiguation/import, trust-tier, leakage-prereg, coverage, novelty,
  and fingerprints. Artifacts/reports:
  `artifacts/v3_non_heme_iron_2og_sourcing_preview_current702.json`,
  `work/non_heme_iron_2og_sourcing_current702.md`,
  `work/non_heme_iron_2og_apply_current702_20260612.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260612_2og_applied.json`,
  `work/coverage_redundancy_audit_current702_20260612_2og_applied.md`.
  Follow-on current source-supply scout recommends **CoA acyltransferase** next (7728 reviewed rows,
  82 distinct full EC labels in a 200-row sample, no reaction-poor warning), via
  `artifacts/v3_next_lane_source_supply_scout_after_p450_2og_current702_20260613.json`. A lane-design
  scout adds that the Acyltransferase keyword lane has **7728** rows while UniProt
  `cc_cofactor:coa` alone has only **23**, with **108** distinct EC labels in a 500-row sample; use
  keyword/domain plus CoA/acyl-CoA Rhea participant or active-site evidence as admission handles, not
  `cc_cofactor:coa` alone. A mechanism-handle scout over 80 reviewed entries found Rhea present
  **80/80**, CoA/acyl-CoA reaction text **72/80**, active/binding-site context **56/80**, and fetch
  failures **0**; it also surfaced multi-EC boundary rows, so the next runner needs explicit
  multi-fingerprint-signal holds.
- **CYTOCHROME P450 16FP BRONZE EXPANSION APPLIED (2026-06-12/13 automation).**
  The documented post-SAM scaling lane was wired as a deliberate 16-fingerprint universe change and
  applied through the canonical external bronze writer, not the frozen benchmark. New family/gate
  surface: `cytochrome_p450_monooxygenase` fingerprint + `heme_monooxygenation` ontology node,
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = label_factory_v1_16fp`, OOS preregistration
  re-frozen as `artifacts/v3_external_hard_negative_next_tranche_preregistration_16fp_1025.json`,
  EC 1.14 scope-only rule with heme plus O2/Rhea participant, P450/monooxygenase keyword/domain, or
  heme-thiolate/active-site evidence as mechanism corroboration, explicit non-peroxidase guard, and
  off-target fingerprint matches held by the runner. Live apply:
  `PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 80 --apply`
  fetched **142** rows -> target mechanism-corroborated **128** -> gate-admitted before cap **110** ->
  appended **110** bronze rows; `cytochrome_p450_monooxygenase` **0 -> 110** (cap 250; floor
  reached); **0 held at cap**, **18 throttled/rejected**, **14 disambiguation holds**, fetch failures
  **0**. Net registry result: external bronze **3590 -> 3700** (+110); combined surface **4292 ->
  4402**; frozen current702 stayed 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply. Honest
  counters remain separate after apply: **positive_bronze 2689**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Guardrails verified: EC scope-only
  and never counted; P450/O2/heme handles admission/excluded context only; `predictive_evidence []`;
  all added labels are `tier=bronze`, `review_status=automation_curated`, `uniprot:*`; dedup vs both
  registries; caps held. Fresh coverage audit: fingerprint Gini **0.1657**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Validation: targeted pytest
  **264 passed, 14 subtests** over P450/NAD/SAM sourcing, disambiguation/import, trust-tier,
  leakage-prereg, coverage, novelty, and fingerprints; `validate` ok
  (12 source / 16 fingerprints / 19 ontology families / 702 labels). Artifacts/reports:
  `artifacts/v3_cytochrome_p450_sourcing_preview_current702.json`,
  `work/cytochrome_p450_sourcing_current702.md`,
  `work/cytochrome_p450_apply_current702_20260612.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260612_p450_applied.json`,
  `work/coverage_redundancy_audit_current702_20260612_p450_applied.md`.
  Next scaling action: wire **non-heme iron 2OG dioxygenase** as a deliberate 17-fingerprint universe
  change. A focused scout already confirmed the lane has **870** reviewed rows on the EC 1.14.11 +
  iron/dioxygenase handle and **36** distinct specific ECs in a 200-row sample
  (`artifacts/v3_non_heme_iron_2og_next_lane_scout_current702_20260612.json`).
- **SAM METHYLTRANSFERASE 15FP BRONZE EXPANSION APPLIED (2026-06-12 automation).**
  The documented post-NAD/glyco scaling lane was wired as a deliberate 15-fingerprint universe
  change and applied through the canonical external bronze writer, not the frozen benchmark. New
  family/gate surface: `sam_methyltransferase` fingerprint + `methyl_transfer` ontology node,
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = label_factory_v1_15fp`, OOS preregistration
  re-frozen as `artifacts/v3_external_hard_negative_next_tranche_preregistration_15fp_1025.json`,
  EC 2.1.1 scope-only rule with SAM/SAH Rhea participant or Methyltransferase keyword mechanism
  corroboration, explicit no-Fe-S/radical-SAM guard, and off-target fingerprint matches held by
  the runner. Live apply:
  `PYTHONPATH=src python scripts/source_sam_methyltransferase_family.py --max-records-per-lane 120 --apply`
  fetched **315** rows -> target mechanism-corroborated **304** -> gate-admitted before cap **264** ->
  appended **250** bronze rows; `sam_methyltransferase` **0 -> 250** (cap 250; floor reached);
  **14 held at cap**, **28 throttled**, **12 rejected over-cap/no-new-chemistry**,
  **2 multi-fingerprint-signal rows held**, **9 skipped**, fetch failures **0**. Net registry result:
  external bronze **3340 -> 3590** (+250); combined surface **4042 -> 4292**; frozen current702 stayed
  702 with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after
  apply. Honest counters remain separate after apply: **positive_bronze 2579**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Guardrails verified: EC scope-only
  and never counted; SAM/SAH/keyword handles admission/excluded context only; `predictive_evidence []`;
  all added labels are `tier=bronze`, `review_status=automation_curated`, `uniprot:*`; dedup vs both
  registries; caps held. Fresh coverage audit: fingerprint Gini **0.1657**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Validation: targeted pytest
  **82 passed** over SAM/NAD sourcing, disambiguation/import, trust-tier, leakage-prereg, coverage,
  novelty, fingerprints, and CLI readiness tests; `validate` ok
  (12 source / 15 fingerprints / 18 ontology families / 702 labels); `git diff --check` and JSON
  parse checks clean. Artifacts/reports:
  `artifacts/v3_sam_methyltransferase_sourcing_preview_current702.json`,
  `work/sam_methyltransferase_sourcing_current702.md`,
  `work/sam_methyltransferase_apply_current702_20260612.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260612_sam_methyl_applied.json`,
  `work/coverage_redundancy_audit_current702_20260612_sam_methyl_applied.md`.
  Next scaling action: wire **cytochrome P450 monooxygenase** as a deliberate 16-fingerprint universe
  change (spec + ontology + heme/thiolate + oxygenase/Rhea or P450 keyword/domain mechanism handles +
  non-peroxidase guard + tests + OOS prereg re-freeze) before preview/apply.
- **NAD(P)-DEHYDROGENASE + GLYCOSYLTRANSFERASE BRONZE EXPANSION APPLIED (2026-06-12 automation).**
  The prior broadened-handle preview was rerun with deeper lanes and applied through the canonical
  external bronze writer, not the frozen benchmark. Main floor run (`--max-records-per-lane 100`):
  fetched **794** rows -> mechanism-corroborated **709** -> gate-admitted-before-cap **486** ->
  applied **373** rows (**nad_p_dehydrogenase 150**, **glycosyltransferase 223**); no fetch failures.
  NAD(P) is now at its chemistry-confusable **150 cap** with **113 held at cap**. Follow-on glyco
  cap-fill (`--families glycosyltransferase --max-records-per-lane 150`): fetched **445** ->
  mechanism-corroborated **157** -> applied **27** more glyco rows, with **10 held at cap**, taking
  glycosyltransferase **223 -> 250**. Net registry result: external bronze **2940 -> 3340** (+400);
  combined surface **3642 -> 4042**; frozen current702 stayed 702 with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after both applies.
  Honest counters remain separate after apply: **positive_bronze 2329**, **oos_bronze 1696**,
  **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Guardrails verified: EC scope-only
  and never counted; broadened handles are admission/excluded context only; `predictive_evidence []`;
  all added labels are `tier=bronze`, `review_status=automation_curated`, `uniprot:*`; dedup vs both
  registries; caps held. Fresh coverage audit: fingerprint Gini **0.1578**, holes `[]`, only
  `metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. Validation: targeted pytest
  **231 passed, 14 subtests**, `validate` ok
  (12 source / 14 fingerprints / 17 ontology families / 702 labels), `git diff --check` clean.
  Artifacts/reports: `artifacts/v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702.json`,
  `artifacts/v3_glycosyltransferase_cap_fill_preview_current702.json`,
  `work/nad_glycosyltransferase_subfamily_sourcing_current702.md`,
  `work/glycosyltransferase_cap_fill_current702.md`,
  `work/nad_glyco_floor_expansion_apply_current702_20260612.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260612_nad_glyco_applied.json`,
  `work/coverage_redundancy_audit_current702_20260612_nad_glyco_applied.md`.
  Next scaling action: wire **SAM methyltransferase** as a deliberate 15-fingerprint universe change
  (spec + ontology + EC 2.1.1/SAM-SAH or Methyltransferase keyword corroborator + no-Fe-S guard +
  tests + OOS prereg re-freeze) before preview/apply.
- **BROADENED EVIDENCE HANDLES WIRED INTO THE ADMISSION ENGINE (2026-06-12) — nad_p_dehydrogenase
  + glycosyltransferase admitted via mechanism corroborators, not cofactor comments; PREVIEW only.**
  The evidence-handle scout proved the recovery (NAD(P) EC 1.1.1: `cc_cofactor` 7 → `keyword:NAD/NADP`
  7700); this wires that fix into the gate. `external_cofactor_ec_disambiguation` was generalized
  from a cofactor-only corroborator to a per-family MECHANISM corroborator (`mechanism_corroborator_axes`)
  reading, in addition to cofactor: cosubstrate / Rhea reaction participant, functional keyword
  (UniProt `keywords`, now extracted in `adapters` + carried on the ingestion row), and
  binding-/active-site presence. "Exactly one rule fires": the EC-prefix predicate is the SCOPE
  selector, a mechanism axis CONFIRMS membership, and admission requires
  `source_trust_tiers.evaluate_corroboration(source_tier_0, …)` to admit (≥1 counted MECHANISM axis);
  **EC is `ec_scope_hint`, NEVER counted** (EC alone can never admit). Broadened handles are
  SCOPE/ADMISSION evidence → `evidence.source_trust_tier`/`excluded_context`, never predictive
  (`predictive_evidence []`; leakage wall unchanged). Two families added end-to-end: fingerprint
  specs (`mechanism_fingerprints.json`, deploy-missing context = NAD(P) cosubstrate / sugar-nucleotide
  donor), ontology nodes (`nicotinamide_redox`, `glycosyl_transfer`), disambiguation rules
  (nad_p EC 1.1.1, glyco EC 2.4), capped EC-subclass lane queries + `DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT`,
  governor signatures, OFFLINE tests, and a runner
  (`nad_glycosyltransferase_subfamily_sourcing.py` / `scripts/source_nad_glycosyltransferase_families.py`,
  modeled on the Stage-2 runner; per-family cap 150 confusable / 250 else). **Live preview (real
  UniProt, 25/lane, non-destructive):** fetched **149** → mechanism-corroborated **128** →
  novelty-admitted **127** → cap-guarded **127** → projected **nad_p_dehydrogenase 0→93** (cap 150),
  **glycosyltransferase 0→34** (cap 250); combined 3642 → **3769 if merged**; 2 lane search timeouts,
  neither family hit the 100-floor at 25/lane (re-run higher to reach floor). Universe 12 → **14**:
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` → `label_factory_v1_14fp`, OOS prereg re-frozen
  (`…preregistration_14fp_1025.json`, supersedes 12fp), historical `_8fp` label stamp unchanged; the
  OOS inverse gate now reports `incomplete_current_fingerprint_coverage` until the new fingerprints
  gain atlas (Stage-3-style; OOS tranche stays blocked until then). Frozen current702 byte-unchanged
  (`sha256:5eec9bef…`); expansion stays 2940; **no `--apply`, no registry write**. `validate` ok
  (14 fp / 17 ontology families / 702 labels); full suite green except the 6 known env-backend
  failures; `git diff --check` clean. **STOP before --apply — preview reported for authorization.**
  See decision_log 2026-06-12 "BROADENED EVIDENCE HANDLES WIRED INTO THE ADMISSION ENGINE";
  `artifacts/v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702.json`,
  `work/nad_glycosyltransferase_subfamily_sourcing_current702.md`.
- **EVIDENCE-HANDLE EXPANSION + SOURCE TRUST-TIER POLICY (2026-06-12) — fix within-Swiss-Prot
  handles first, then expand sources honestly; counters stay separate.** User direction: the
  breadth scout's shortfall is partly a HANDLE problem (fix before leaving Swiss-Prot) and partly a
  real supply gap (expand sources via trust tiers); do NOT redefine 10k to paper over a positive
  gap. Two non-destructive, offline-tested modules; no registry/label written; frozen current702
  untouched (`sha256:5eec9bef…`). (1) `evidence_handle_expansion.py` measures, per family, how much
  reviewed supply each within-Swiss-Prot corroborator handle recovers (cc_cofactor vs keyword vs
  binding-site vs active-site; EC is scope, not a corroborator). Decision-grade (live UniProt):
  **NAD(P) dehydrogenases EC 1.1.1 — `cc_cofactor:nad/nadp` reaches 7 of 7804; `keyword:NAD/NADP`
  reaches 7700** (NAD is a cosubstrate keyword, not a cofactor comment). Across 6 families the
  broader handles recover ~64k raw reviewed entries the cofactor handle misses (RAW/overlapping, not
  additive) and **~741 additional reachable POSITIVE bronze** after cap+novelty discount (the bounded
  figure); the big pools must be split by EC-subclass into capped lanes. These winning handles are
  what to wire into the import gate per family before sourcing beyond Swiss-Prot. (2)
  `source_trust_tiers.py` encodes the durable policy: trust tiers 0–4 (only 0–2 bronze-eligible,
  escalating N-of-M corroboration 1/2/3; tiers 3–4 are hypotheses, never countable bronze), 6 counted
  MECHANISM corroborator axes + `evaluate_corroboration`, and the SEPARATE honest counters
  (`positive_bronze`/`oos_bronze`/`silver_ready`/`silver_confirmed`/`projected`) that must never be
  merged. **EC is `ec_scope_hint` — non-counted (scope / fetch / stratification + excluded_context
  only); EC alone can never satisfy N-of-M** (the counted reaction axis is
  `rhea_reaction_or_participant_pattern`, mechanism, not EC). Ledger at that point:
  **positive_bronze 1929, oos_bronze 1696, silver_confirmed 17** (1929
  bronze + 17 silver = 1946 positives). Trust tiers ADD a gate; governor + novelty gate stay
  mandatory. `validate` ok (702/12/15); full suite green except the 6 known env-backend failures.
  See decision_log 2026-06-12 "EVIDENCE-HANDLE EXPANSION + SOURCE TRUST-TIER POLICY";
  `artifacts/v3_evidence_handle_expansion_current702.json`,
  `artifacts/v3_source_trust_tier_policy_current702.json`,
  `work/evidence_handle_expansion_current702.md`.
- **STAGE-3 PREREQS DONE (2026-06-11) — OOS hard-negative pre-registration re-frozen to the 12fp
  universe + a clean (decoupled) ontology version bump; the next OOS import is unblocked.** Two
  deferred Stage-2 follow-ups, both REQUIRED before any new OOS import; neither writes a label or
  touches the frozen 702 (`sha256:5eec9bef…` unchanged; registries unchanged). (1) New governance
  artifact `v3_external_hard_negative_next_tranche_preregistration_12fp_1025.json` re-freezes the
  tranche pre-registration against the LIVE 12-fingerprint universe (`ontology_version_at_decision`
  = `label_factory_v1_12fp`, generated from `load_fingerprints()` so the universe matches the gate);
  the 8fp artifact is kept as the superseded historical record. (2) The ontology version bump is
  DECOUPLED, not a global rename: `DEFAULT_ONTOLOGY_VERSION_AT_DECISION` STAYS `label_factory_v1_8fp`
  (the historical stamp on every existing label + spent/threshold contracts + 60+ transfer_scope
  artifacts — renaming would rewrite history and risk the frozen-702 hash), and a NEW
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = "label_factory_v1_12fp"` is what the OOS prereg
  gate now requires. Candidate-row ontology checks correctly stay `_8fp` (registry stamp, a different
  concept from the inverse-gate universe). Tests updated intentionally (accept-test loads the real
  12fp artifact; new frozen-for-12 test; stale-8fp test now asserts both universe + ontology blockers);
  historical `_8fp` assertions untouched. `validate` ok (702/12/15); full suite green except the 6
  known env-backend failures. See decision_log 2026-06-11 "STAGE-3 PREREQS".
- **BREADTH FEASIBILITY SCOUT (2026-06-11) — real numbers say 10k diverse POSITIVE bronze is NOT
  reachable from reviewed Swiss-Prot alone; the target should be re-scoped.** Before sourcing more
  bronze, replaced the scaling-plan cap-math *estimate* with REAL reviewed-Swiss-Prot supply +
  reaction-diversity numbers. New non-destructive recon (`breadth_feasibility_scout.py` /
  `scripts/scout_breadth_feasibility.py`, offline-tested with injected fetchers) probed 18 curated
  candidate families beyond the current 12 (non-hydrolase first) via the cheap `x-total-results`
  header count + an EC-only reaction-diversity sample; it writes NO registry and creates NO labels.
  **Verdict (live UniProt): `ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone`.**
  Current combined positive bronze 1946 (12 fingerprints); beyond those **15/18 candidate families
  are clean** (distinct + floor-reachable + non-redundant), 0 redundant — breadth genuinely exists —
  but the clean families' capped, novelty-discounted supply projects to only **~4737** positive
  bronze (**gap 5263 to 10k**), and the honest discounts cut deeper: **9/15 clean families are
  reaction-poor** (ortholog padding → diversity-discounted new bronze ~1936) and **8/18 have a weak
  cofactor handle** (<25% of the EC ceiling). The decision-grade weak-handle case: NAD(P)
  dehydrogenases (EC 1.1.1, ~7804 reviewed) capture only **7** under `cc_cofactor:nad/nadp` (NAD(P)
  is a cosubstrate, not a UniProt COFACTOR comment) — the largest oxidoreductase pool is unreachable
  by the current cofactor-anchored gate without a **sequence-motif/EC-only handle**. **Re-scope
  implication:** reviewed Swiss-Prot yields low thousands of diverse POSITIVE bronze, not 10k; 10k
  needs to be defined as positives + diverse novelty-gated OOS + bronze→silver depth, or admit
  sources beyond reviewed Swiss-Prot. Cleanest first non-hydrolase families to source:
  `non_heme_iron_2og_dioxygenase`, `cytochrome_p450_monooxygenase`, `copper_oxidoreductase`,
  `molybdopterin_oxidoreductase`, `glycosyltransferase`, `coa_acyltransferase`,
  `cofactor_independent_isomerase`. `validate` ok; full suite green except the 6 known env-backend
  failures; frozen current702 untouched (`sha256:5eec9bef…`). See decision_log 2026-06-11 "BREADTH
  FEASIBILITY SCOUT"; `artifacts/v3_breadth_feasibility_scout_current702.json`,
  `work/breadth_feasibility_scout_current702.md`.
- **TRACK 1 (context depth) 1c DONE (2026-06-11) — leakage-safe row-specific BOND-CHANGE feature
  makes the metal sub-families predictively separable.** The Stage-2 honest finding was that the
  leakage-safe *chemistry* representation could NOT separate the four metal sub-families (they share
  the divalent-metal cofactor + water-activator residue roles; repr-loop LOO collapsed to ~0.49
  metal-only / ~0.68 overall) because they differ only by the reaction-center BOND hydrolysed — not
  yet a feature. 1c adds that feature: `mechanism_representation_loop` now derives a row-specific
  bond-change vector (`bc_phosphomonoester`, `bc_phosphodiester`, `bc_peptide_cn`, `bc_amide_cn`)
  from the **Rhea reaction equation's substrate→product chemistry** — NOT the fingerprint's declared
  bond_change (that would leak the label), NOT EC, NOT name/prose. It fires only for HYDROLYSIS
  (water on the substrate side), which keeps non-hydrolase (lyase/transferase) chemistries — e.g.
  cobalamin ammonia-lyases — out of the bond space. **Measured honestly (LOO self-consistency):
  overall 0.679 → 0.751; the four v2 sub-families jump to metallopeptidase 0.95,
  metallophosphoesterase_nuclease 0.93, metallophosphomonoesterase 0.89,
  metallo_amidohydrolase_deaminase 0.75 (v2-only ≈ 0.88, from ~indistinct); non-metal separability
  PRESERVED exactly at 0.854** (the water constraint excludes the non-metal lyases that would
  otherwise pollute). The coarse v1 umbrella `metal_dependent_hydrolase` now (correctly) scatters to
  its sub-families → its own self-consistency drops to ~0 — that is the split working, not a
  regression. Bond-change is weighted co-equal with cofactor (1.0; not tuned to the metric).
  Honest limitation: metallopeptidases largely lack a small-molecule Rhea reaction (110/150 have
  none — their substrate is a generic protein), so their separation is partly "metal hydrolase with
  no hydrolysis-reaction bond-change" by elimination; phosphomono/diester/amide are cleanly
  reaction-driven. This is the discriminator for ALL future fine splits, not just metal. Diagnostic
  only — the representation organises/triages the expansion's self-supply; it is NEVER a benchmark
  scorer and the frozen 702 is never read. `validate` ok; full suite green except the 6 known
  env-backend failures. See decision_log 2026-06-11 "TRACK 1 — 1c";
  `artifacts/v3_mechanism_representation_loop_current702_20260610.json`.
- **TRACK 1 (context depth) 1b DONE (2026-06-11) — AlphaFoldDB v6 coordinate provenance staged for
  expansion labels (0%/6% → 98.3%).** With the sequence backfilled (1a), the next missing context is
  STRUCTURE — the predicted coordinate unlocks geometry / active-site context and the bronze→silver
  promotion path for all families. A new reusable module
  (`src/catalytic_earth/label_structure_backfill.py` / `scripts/backfill_label_structures.py`)
  derives the AFDB v6 handle from each label's accession (`AF-{acc}-F1-model_v6.cif`), fetches the
  predicted CIF, hashes it, and records `evidence.structure_provenance.afdb_v6_coordinate`
  (structure_handle, model_url, model_version, **coordinate_sha256**, coordinate_bytes,
  atom_record_count, retrieved_utc, status). Live AFDB: **2890/2940 staged (98.3%); 50 unavailable**
  (AFDB excludes some very long sequences — recorded honestly as `afdb_v6_unavailable`, not
  fabricated). Coordinates are **regeneratable from the handle**, so the large CIFs are NEVER
  committed: each is staged to a temp dir, hashed, and discarded (only hash + handle stored); a
  resumable cache lives under the git-ignored `data/cache/`. The provenance is **additive** — the
  existing `coordinate_status` / `coordinate_path` (incl. the ser_his triad-confirmed status) are
  preserved. Row counts UNCHANGED (combined 3642 / expansion 2940 / seed_labels 1716 pins hold); the
  only registry diff is the new nested key; frozen current702 byte-unchanged (`sha256:5eec9bef…`)
  before and after. Structure is review-only mechanism context (a bronze→silver signal), NEVER a
  predictive feature; the leakage wall is unchanged. `validate` ok; full suite green except the 6
  known env-backend failures. See decision_log 2026-06-11 "TRACK 1 — 1b";
  `artifacts/v3_label_structure_backfill_preview_current702.json`,
  `work/label_structure_backfill_current702.md`.
- **TRACK 1 (context depth) 1a DONE (2026-06-11) — deploy-input SEQUENCE backfilled onto every
  expansion label (0% → 100%).** The North Star maps a raw SEQUENCE → mechanism, but the expansion
  atlas stored only the UniProt handle + length — the one input a deployed model predicts FROM was
  absent for all 2940 expansion labels (the frozen-702 sequences live in a separate manifest). A new
  reusable module (`src/catalytic_earth/label_sequence_backfill.py` /
  `scripts/backfill_label_sequences.py`) fetches the reviewed UniProt sequence by accession (TSV
  `fields=accession,sequence,length,reviewed`, batched 25, reusing the `adapters` primitives) and
  records it under **`evidence.sequence_provenance`** (sequence, sha256, length, source_accession,
  source=`reviewed_uniprot`, retrieval provenance, retrieved_utc). Live UniProt: **2940/2940
  backfilled (100% coverage, 0 fetch-missing, 0 length-conflicts)**; seed 1716/1716 and OOS
  1224/1224 both carry the sequence. The sequence is the legitimate DEPLOY INPUT (it is NOT
  EC/name/prose) — stored as DATA under `sequence_provenance`, **never** in `predictive_evidence`
  (stays `[]`) or `excluded_context`; the leakage wall is unchanged and the OOS leakage validator
  accepts it (round-trip through `MechanismLabel.from_dict().to_dict()` verified for all 2940 rows).
  Row counts are **UNCHANGED** (a block added in place; combined 3642 / expansion 2940 / seed_labels
  1716 pins all hold); the only diff is the new key, re-serialized with the same compact
  `_dump_registry` serializer (`git diff --check` clean). Frozen current702 byte-unchanged
  (`sha256:5eec9bef…`) before and after. Sequence wired at SOURCE time too:
  `external_annotation_anchored_import._build_label` now populates `sequence_provenance` from the
  canonical ingestion-pilot row (`external_source_ingestion._candidate_row` carries `sequence` +
  `sequence_sha256`), so future sourced labels get it natively. `validate` ok (702/12/15); full
  suite green except the 6 known env-backend failures. See decision_log 2026-06-11 "TRACK 1 — 1a";
  `artifacts/v3_label_sequence_backfill_preview_current702.json`,
  `work/label_sequence_backfill_current702.md`. **Next (Track 1):** 1b stage AlphaFoldDB v6
  coordinates (`evidence.structure_provenance`, hash+handle, no committed CIFs) and 1c the
  leakage-safe row-specific BOND-CHANGE feature from Rhea (the discriminator that makes the metal
  sub-families predictively separable).
- **STAGE 2 STARTED (2026-06-11) — `metal_dependent_hydrolase` split into four v2 sub-families (+600 bronze).**
  The coarse over-cap umbrella was split (by reaction-center bond change, not metal alone)
  into `metallopeptidase` (peptide C-N), `metallophosphoesterase_nuclease` (phosphodiester
  P-O), `metallophosphomonoesterase` (phosphomonoester P-O), and
  `metallo_amidohydrolase_deaminase` (non-peptide amide/amidine C-N). Each got a fingerprint
  spec (`mechanism_fingerprints.json`, with a declared **deploy-missing context = metal**),
  an ontology node (`mechanism_ontology.json` hydrolysis family), a metal+EC disambiguation
  rule, lane maps, and a governor signature. A new runner
  (`stage2_hydrolase_subfamily_sourcing.py` / `scripts/source_stage2_hydrolase_subfamilies.py`)
  sourced each to the floor via the Stage-1 chain (fetch → metal/EC disambiguation → novelty
  gate → cap guard). Live UniProt: 1530 rows → 1167 disambiguated → **600 admitted** (150
  per sub-family, `--cap-ceiling 150`) → expansion **2340 → 2940**, combined **3042 → 3642**;
  frozen 702 untouched (`sha256:5eec9bef…`). Governor: holes `[]`; fingerprint Gini
  **0.1917 → 0.1518** (most balanced yet); seed positives **1346 → 1946**; positive:OOS
  **0.79 → 1.15**; the coarse umbrella stays the lone over-cap (308, **no new labels added**).
  Cap=150 (not 250) on purpose: filling chemistry-confusable sub-families to the ceiling
  manufactures redundancy (a 250-cap dry run put metallopeptidase at 7.14 labels/distinct-rxn,
  worse than the 2.96 parent). **Honest finding:** the leakage-safe *chemistry* representation
  CANNOT yet separate the four metal sub-families (repr-loop LOO self-consistency 0.90 → 0.68,
  the drop entirely within the metal super-family; non-metal stays 0.85) — they differ by
  reaction-center bond change, which needs the **deferred row-specific bond-change feature**
  (using the fingerprint's own bond-change would leak the label). Expanding the positive
  universe 8 → 12 correctly invalidates the 8fp OOS hard-negative pre-registration (must be
  re-frozen for 12fp before the next OOS import — Stage 3). The ontology version key stays
  `label_factory_v1_8fp` (a deferred clean bump). **Cap math, plainly:** +600 from one split;
  10k still needs sustained family breadth (incl. non-hydrolase chemistries — hydrolysis now
  holds 6 of 12 fingerprints). See decision_log 2026-06-11 "STAGE 2 STARTED";
  `artifacts/v3_stage2_hydrolase_subfamily_sourcing_preview_current702.json`.
- **STAGE 1 COMPLETE (2026-06-11) — every hole closed; no fingerprint below the floor.**
  The last open hole, the cofactorless `ser_his_acid_hydrolase`, was sourced **42 → 129**
  by a new dedicated runner (`scripts/source_ser_his_hole.py` / module
  `ser_his_hole_sourcing.py`): fetch serine-hydrolase rows (EC 3.4.21/3.4.16/3.1.1, **no
  cofactor**) → stage the **AlphaFoldDB v6** predicted coordinate → confirm the
  Ser-His-Asp catalytic triad coincides (≥2 overlap) with the annotated ACT_SITE →
  novelty gate → apply (+87 bronze; expansion **2340**; combined **3042**; frozen 702
  untouched). The corroborator is the coordinate **triad**, not a cofactor — and the
  triad is present in the **apo** predicted structure (UniProt-numbered), which is why
  ser_his is apo-confirmable. Governor now: **`holes: []`**, **all 8 fingerprints
  at/above the 100-floor** (7 BALANCED + the intentional `metal_dependent_hydrolase`
  over-cap 308), fingerprint Gini **0.1917** (was 0.51), next-batch floor deficit **0**,
  seed positives **1346**. Required AFDB egress (open here alongside UniProt), so the loop
  is runnable, not just a contract. See decision_log 2026-06-11 "ser_his Hole CLOSED";
  `artifacts/v3_ser_his_hole_sourcing_preview_current702.json`. **Next is Stage 2**
  (expand the family set — the real 10k lever; the metal over-cap v2 split is the on-ramp).
- **Stage-1 cofactor-defined sourcing COMPLETE (2026-06-11) — 7 of 8 fingerprints now BALANCED.**
  After the two holes (below), the three under-floor cofactor fingerprints were sourced
  to the 100-floor by the same runner (now generalized to all five cofactor-defined
  Stage-1 fingerprints): `flavin_monooxygenase` **43 → 116**, `heme_peroxidase_oxidase`
  **69 → 119**, `flavin_dehydrogenase_reductase` **87 → 250** (+286 bronze; expansion
  **1967 → 2253**; combined **2669 → 2955**; frozen 702 untouched). Governor: fingerprint
  Gini **0.3408 → 0.2608** (originally 0.51); seed positives 973 → 1259; the only HOLE
  is `ser_his_acid_hydrolase` (42) and the only OVER_CAP is `metal_dependent_hydrolase`
  (308, untouched). Load-bearing fix: the runner now enforces a hard per-fingerprint
  **cap guard** (`cap_ceiling=250`) — the novelty gate had pushed `flavin_dehydrogenase_reductase`
  to 253 (over cap) because it admits diverse rows greedily and permits
  `over_cap_but_new_reaction_chemistry`; the guard trims each fingerprint's admitted set
  so combined never exceeds the cap (surplus held, not imported), landing flavin_DR at
  exactly 250. flavin_DR is highly diverse (~0.5 labels/reaction), so filling it toward
  cap is honest supply and balance improved. See decision_log 2026-06-11 "Stage-1
  Under-Floor Closure"; `artifacts/v3_stage1_underfloor_sourcing_preview_current702.json`.
- **Stage-1 hole sourcing applied (2026-06-10) — two cofactor-defined holes closed to floor.**
  Ran `docs/stage1_hole_sourcing_runbook.md` with live UniProt egress. 548 reviewed
  Swiss-Prot rows across 10 narrow EC/cofactor lanes (0 fetch failures) → 259
  disambiguated bronze (277 held for no cofactor+EC corroboration, 12 dup-screened) →
  257 novelty-admitted, appended to the SEPARATE expansion registry
  `data/registries/external_bronze_labels.json` (**1710 → 1967**; combined
  **2412 → 2669**). Frozen current702 benchmark byte-unchanged (702 labels,
  `sha256:5eec9bef…`). Per-fingerprint combined (frozen + expansion):
  `radical_sam_enzyme` **10 → 133** (expansion 9 → 132) and
  `cobalamin_radical_rearrangement` **10 → 144** (expansion 7 → 141) — both **HOLE
  closed, 100-floor reached**. The governor now lists holes as
  `['ser_his_acid_hydrolase']` only (was [ser_his, radical_sam, cobalamin]);
  fingerprint Gini **0.51 → 0.3408**. A load-bearing fix went in: the cobalamin
  matcher in `external_cofactor_ec_disambiguation.cofactor_evidence` missed UniProt's
  inline-oxidation-state cofactor names (`adenosylcob(III)alamin`, `cob(II)alamin`),
  so it now also matches the `cob(i/ii/iii)alamin` stems (scope-only read; leakage
  wall unchanged). `ser_his_acid_hydrolase` stays a hole at 42: its triad-locator scan
  is coordinate-confirmation-only / network-free by design, the local candidate pool is
  drained (0 confirmed recoveries), and closing it needs the live fetch +
  coordinate-staging + triad-confirm loop the acquisition contract describes (not yet
  wired into `build-ser-his-triad-locator-scan`). See decision_log 2026-06-10
  "Stage-1 Hole Sourcing"; `artifacts/v3_stage1_hole_sourcing_preview_current702.json`,
  `work/stage1_hole_sourcing_current702.md`.
- **Current headline result (2026-06-06) — cofactor reconstruction:** the predicted-geometry
  drop is recovered by reconstructing the deploy-missing cofactor from sequence. Predicted-apo
  **23/45 → 37/45** primary (confirmed heldout one-shot, now SPENT; OOS/sec FP 12.3% → 25.9%).
  Full detail in *Trusted Results* below, the decision_log "HELDOUT ONE-SHOT SPENT" entry, and
  `docs/MAP.md`. **Vocabulary note (so this is searchable):** *cofactor reconstruction* =
  *cofactor recovery* = the *sequence→cofactor-presence channel* (`cofactor_presence_calibration.py`)
  fused into the router; the generalized form is "reconstruct the deploy-missing active-site
  context from sequence" (`docs/predicted_geometry_robustness_pipeline_runbook.md`).
- Current label surface: 702 curated labels in the current sequence-NN manifest,
  with 562 in-distribution rows and 140 heldout rows.
- Current targeted expansion surface (2026-06-08): the first reusable targeted
  expansion factory batch has 816 non-importing candidates across 8 family axes
  with exact-one-state admission routing. Counts: 0 countable candidates, 391
  review-only evidence rows, 205 reject/OOS-preserve rows, 90 locator blockers,
  44 coordinate blockers, 86 acquisition-needed rows, and 0 family-decision
  blockers. It also carries the six architecture-default family-admission rows
  without reopening human review. Use
  `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json` and
  `work/targeted_expansion_factory_batch_current702_20260608.md`.
- Current acquisition conversion screen (2026-06-08): the 86
  acquisition-needed targeted-expansion rows have a durable non-importing
  conversion artifact. Terminal states: 27 reject/OOS-preserve rows, 7 locator
  blockers, 50 family-decision blockers, 1 review-only row, 1
  countable-candidate preflight-only row, and 0 coordinate blockers. The
  preflight-only row is not an import. Use
  `artifacts/v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json`
  and
  `work/targeted_expansion_acquisition_conversion_screens_current702_20260608.md`.
- Current scale-out merged acceptance surface (2026-06-08): seven shard
  artifacts were consolidated into a non-importing merger/QA surface with 4,820
  source rows deduplicated to 2,463 canonical candidate keys. Canonical states:
  1,940 reject/OOS-preserve, 280 review-only, 85 blocked-locator, 24
  blocked-coordinate, 134 blocked-family-decision, and 0 new
  countable-candidate preflight rows after current-registry overlap. The four
  source preflight-only rows collapse to three canonical groups
  (`uniprot:P78549`, `m_csa:127`, and `m_csa:281`) blocked from import preview
  by current702 overlap and/or conservative reject/OOS resolution. Use
  `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`
  and `work/scaleout_merged_acceptance_surface_current702_20260608.md`. The
  repair overlay remains durable:
  `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`
  records hash-matched coordinates for the 7 acquisition-conversion
  locator-blocked rows, recommends `uniprot:Q9BXS1` as future
  reject/OOS-preserve, and keeps `uniprot:P60174` first for review-gated
  locator copy. No locator sidecar, import preview artifact, registry edit,
  threshold/model/split edit, or heldout training/tuning was performed.
- Current countable-label unblocker matrix (2026-06-08): the non-reject
  canonical scale-out rows were classified into concrete import-preview or
  blocker actions. Target rows reconcile to 523 candidates: 280 review-only,
  134 family-decision, 85 locator, and 24 coordinate. Automated gates produced
  0 import-preview candidates because no row has both
  `ready_for_label_import=True` and `countable_label_candidate=True`; 37 rows
  are exact current-registry overlaps and 17 carry positive duplicate-screen
  signals. The matrix resolved 102 family-decision rows to existing no-import
  family defaults, moved 21 coordinate blockers with local coordinate files into
  locator repair, left 2 true coordinate repairs, and kept 36 rows as
  true-expert-only. Use
  `artifacts/v3_countable_label_unblocker_matrix_current702_20260608.json` and
  `work/countable_label_unblocker_matrix_current702_20260608.md`; no import
  preview artifact was written.
- Current external-source ingestion pilot (2026-06-08): the first rerunnable
  reviewed Swiss-Prot/UniProt + AFDB/PDB + Rhea/EC ingestion lane samples 28
  non-M-CSA external candidates across seven scale-out family lanes. Terminal
  states: 16 `external_countable_preflight_candidate`, 7
  `locator_ready_candidate`, 4 `coordinate_ready_pending_locator`, and 1
  `blocked_duplicate_or_current_registry_conflict` (`uniprot:P23721`). A
  preview-only import artifact was produced for the 16 preflight rows, but no
  production registry/import/ontology/model/threshold/split edit was made. Use
  `artifacts/v3_external_source_ingestion_pilot_current702_20260608.json`,
  `artifacts/v3_external_source_ingestion_import_preview_current702_20260608.json`,
  and `work/external_source_ingestion_pilot_current702_20260608.md`.
- Current external admission validation (2026-06-08): the 16 external
  import-preview rows reconcile exactly to the pilot and pass reviewed
  Swiss-Prot, source-hash/provenance, exact residue locator, PDB/AFDB handle,
  Rhea/specific EC, lane-assignment, and recomputed exact current702
  accession/sequence duplicate gates. They are admission-ready as a
  materialization queue, not direct production imports: 6 are
  `admission_ready_pending_locator_materialization` with local coordinates
  already matched, and 10 are
  `admission_ready_pending_coordinate_materialization`. No direct
  `admission_ready_external_label_candidate` rows exist until local coordinates
  and approved source-free locator sidecars are materialized and the validation
  reruns. Use
  `artifacts/v3_external_source_admission_validation_16_current702_20260608.json`,
  `artifacts/v3_external_source_admission_ready_preview_current702_20260608.json`,
  and `work/external_source_admission_validation_16_current702_20260608.md`.
- Current external bulk ingestion scout (2026-06-08): the pilot ingestion
  pattern now scales to 693 reviewed Swiss-Prot/UniProt candidates across the
  seven family lanes, with structured residue/cofactor evidence where present,
  AFDB/PDB coordinate provenance, Rhea/EC provenance, current702 duplicate
  status, and external-pilot duplicate status. Terminal states: 354
  `provisional_external_countable_preflight_candidate`, 194
  `locator_ready_candidate`, 97 `coordinate_ready_pending_locator`, 39
  `blocked_duplicate_or_current_registry_conflict`, 4
  `locator_repair_candidate`, 3 `coordinate_repair_candidate`, and 2
  `hard_blocked_with_next_action`. The provisional preview artifact has 354
  rows, all still blocked from production import until
  `ce-external-admission-16-validation` or its scaled successor validates the
  gates; no production registry/import/ontology/model/threshold/split edit was
  made. Use
  `artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json`,
  `artifacts/v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json`,
  and `work/external_bulk_ingestion_scout_current702_20260608.md`.
- Current redox/cofactor-confounded external shard (2026-06-09): the targeted
  reviewed Swiss-Prot scaleout covers redox oxygen/sulfur, heme
  peroxidase/oxidase-like, flavin monooxygenase versus dehydrogenase/reductase
  boundaries, Fe-S/flavin combined systems, sulfur oxidoreductases,
  oxygenases, dehydrogenases, and cofactor-confounded OOS negatives. It
  dedupes against current702 plus local prior external/scaleout artifacts and
  completed external-admission branch artifacts. Counts: 2,681 candidate rows,
  2,512 unique non-duplicate rows, 743 `import_ready_preview`, 214
  `locator_ready_candidate`, 103 `coordinate_ready_pending_locator`, 21
  `locator_repair_candidate`, 18 `coordinate_repair_candidate`, 119
  `reject/OOS_preserve_signal`, 169 duplicate/current/prior conflicts, and
  1,294 hard blockers, mostly UniProt entry materialization timeouts preserved
  as explicit source-retrieval blockers. Use
  `artifacts/v3_external_scaleout_shard_redox_cofactor_confounded_current702_20260609.json`,
  `artifacts/v3_external_scaleout_shard_redox_cofactor_confounded_import_ready_preview_current702_20260609.json`,
  and
  `work/external_scaleout_shard_redox_cofactor_confounded_current702_20260609.md`.
  No production registry/import/ontology/model/threshold/split edit was made;
  import-ready preview rows still require current-countable structural
  duplicate screening, label-factory review, and explicit registry-change
  authorization.
- Current v1 primary mechanism targets: `ser_his_acid_hydrolase`,
  `metal_dependent_hydrolase`, `plp_dependent_enzyme`,
  `flavin_dehydrogenase_reductase`, and `heme_peroxidase_oxidase`.
- Secondary OOD probe fingerprints: `radical_sam_enzyme`,
  `cobalamin_radical_rearrangement`, and `flavin_monooxygenase`.
- The 2026-05-25 sequence manifest predates the later canonical `m_csa:497` and
  `m_csa:750` OOS revisions. Use the Wave 1 readthrough masks when reading
  Wave 1 artifacts that still carry those rows as primary flavin labels.
- Current Wave 1.2 standardized heldout readout:
  - canonical mask: 45 primary rows, 92 pure OOS rows, 3 secondary-probe rows;
  - Wave 1 readthrough mask after excluding `m_csa:497` and `m_csa:750` from
    primary metrics: 43 primary rows and 97 nonprimary/OOS rows.

When a report predates 2026-05-27 row-level revisions, do not copy its primary
flavin counts directly. Check the decision log and the row-level revision
artifacts first.

## Trusted Results

### 2026-06-09 session update — cofactor-fusion precision side measured (step-4)

- **The precision side of the cofactor-fusion router is now measured on a reusable,
  leakage-safe train/cal OOS surface** (previously unmeasured — the recovery harness had
  no OOS rows). Scoring the in-distribution OOS rows through the FROZEN router: raw fusion
  lifts in-scope recall (apo 17/35 -> 30/35 cal) at an OOS-FP cost (train FP 0.402 ->
  0.480); the recalibrated-threshold dial (0.44) and the suppression dial both cut FP back,
  but on the out-of-sample calibration surface **the threshold dial dominates** — 0.44
  keeps recall 30/35 and reaches OOS FP 8/26, while suppression reaches the same 8/26 only
  by dropping recall to 23/35. Lever-2 electron-flow (+0.04, different surface) is the
  complementary precision lever. Research diagnostic only: no production threshold change,
  no heldout read; deployable-point selection stays separately authorized.
  (`artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json`,
  `work/cofactor_fusion_operating_point_train_cal_oos_current702_20260609.md`,
  decision_log 2026-06-09 "Step-4 Precision Side Measured".)

### 2026-06-06 session update — predicted-geometry recovery confirmed (read newest-first)

- **Predicted-geometry recovery now works and is confirmed on the spent heldout
  one-shot.** Applying the FROZEN leakage-safe cofactor-presence channel via raw cofactor
  fusion at the existing 0.4115 threshold moved predicted-apo primary from **23/45 to
  37/45** (+14 recovered), at a precision cost of OOS/secondary FP **12.3% -> 25.9%**.
  The one-shot is **spent**; do not re-run or tune any threshold/policy against it.
  (`artifacts/v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json`;
  decision_log 2026-06-04 "HELDOUT ONE-SHOT SPENT".)
- **The leakage-safe methodology validated itself:** the in-distribution recovery harness
  predicted the result before the read — out-of-sample calibration recovery 70.6% ->
  heldout 63.6%; projected ~38/45 landed at 37/45.
  (`src/catalytic_earth/predicted_geometry_recovery.py`,
  `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json`.)
- **Leakage-safe cofactor-presence channel** (heads fit on train, thresholds + backend
  selected on calibration, heldout never read for fit/threshold): metal/flavin/PLP/heme
  one-vs-rest heads, optional cofactor-binding sequence-motif features.
  (`src/catalytic_earth/cofactor_presence_calibration.py`,
  `artifacts/v3_cofactor_presence_calibration_current702_20260604.json` [+ `_motif_`].)
- **Problem-2 diagnosis (the foundation under the above):** the 45->23 drop is
  **cofactor-loss-dominated** (22/22 lost primaries are cofactor-apo loss), the predicted
  backbone is faithful (restoration probe recovers **22/22**; realistic graft **19/22**;
  3 distorted-backbone rows are the ESMFold2 apo secondary-lever boundary). Generalized to
  a reusable pipeline — diagnose missing context -> bound ceiling -> reconstruct from
  sequence -> fuse + abstain — see `docs/predicted_geometry_robustness_pipeline_runbook.md`.
  (`artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json`,
  `v3_cofactor_restoration_recovery_probe_current702_20260604.json`,
  `v3_cofactor_graft_fidelity_probe_current702_20260604.json`,
  `v3_esmfold2_predicted_geometry_robustness_experiment_contract_current702_20260603.json`.)
- **Lever-2 electron-flow is a complementary precision lever (research-grade):** a direct
  source-free electron-flow OR overlay raises OOS abstain-recall **0.467 -> 0.507 (+0.04)**
  at **primary retention 1.0** (PQQ `m_csa:104`, NAD-family `m_csa:464`, Fe-S `m_csa:119`);
  not deployable until a protected-import authorization + approved-sidecar rerun. It offsets
  the cofactor channel's precision cost (cofactor adds recall, electron-flow adds OOS
  abstention). (`src/catalytic_earth/lever2_mechanism_incremental_readout.py`,
  `artifacts/v3_lever2_source_free_electron_flow_current_split_operating_point_readout_current702_20260606.json`;
  decision_log 2026-06-06 "Lever 2 Electron-Flow…".)

### Pre-2026-06-06 trusted results

- Geometry re-export removed the prior join confound. The current Wave 1.2 audit
  joins 140/140 standardized heldout rows, recovers the five rows missed by the
  older preview geometry eval (`m_csa:577`, `m_csa:599`, `m_csa:710`,
  `m_csa:892`, and `m_csa:897`), and reports 45/45 canonical primary accuracy
  with 0/92 pure-OOS false positives under the existing 0.4115 geometry
  abstention threshold.
- Hand-scored active-site geometry remains the current first router. The
  geometry-feature logistic probe is useful but weaker on the audit: 66.7%
  canonical primary accuracy and 4.2% OOS/secondary false-positive rate.
- The clean experimental-coordinate geometry result is not deployment-ready by
  itself. The AlphaFoldDB predicted-geometry audit drops the hand router from
  45/45 to 23/45 primary heldout correct, with 17 primary abstentions, 5 wrong
  non-abstained primary calls, and a 12.3% OOS/secondary false-positive rate.
  This makes robustness to predicted active-site geometry degradation a learned
  model job description, not a raw clean-M-CSA accuracy contest.
- A real AlphaFoldDB-predicted structure Foldseek channel is now scored for all
  126 heldout rows with ok predicted geometry against the predicted
  in-distribution atlas. The standalone nearest-atlas TM signal separates
  in-scope from all OOS at AUC 0.814301; a no-fit mean of predicted geometry
  confidence and fold TM reaches AUC 0.907622 overall and 0.911348 on the six
  cofactor-confounded OOS rows. These are diagnostics, not production thresholds.
- The scored predicted-structure fold channel now has a strict contract audit.
  It confirms 126/126 ok heldout rows and 6/6 priority cofactor-confounded OOS
  rows have parsed nearest-atlas Foldseek/TM hits, with zero critical contract
  violations. The AFDB-v6 coordinate bundle is now persisted locally, so the
  coordinate-provenance gate is no longer a reproducibility blocker.
- The fold-channel coordinate-provenance audit now reports all 299 expected
  AFDB-v6 coordinate paths observed across 293 deduplicated accessions. The
  all-heldout and priority TSVs remain present and parseable, and the contract
  audit still has zero critical violations.
- A reproduction manifest now ties that fold channel together for future reruns:
  it records exact AFDB-v6 coordinate requests, scored TSV hashes, Foldseek
  commands, contract/provenance audit hashes, and no remaining byte-level
  reproduction blockers. No Foldseek/TM score was recomputed.
- A carryover-resolution audit now makes stale fold-channel prompts explicit:
  the requested fold-channel artifact/report are present and score-complete,
  126/126 heldout rows and 6/6 priority cofactor-confounded rows remain scored,
  and no Foldseek/TM rerun is needed unless the contract audit fails.
- The fold-augmented gate now has a leakage-safe thresholding contract. A
  deterministic in-distribution train/cal split selected the
  `combined_mean_geometry_fold` threshold `0.44155` at >=90% calibration
  in-scope retention. Heldout final readout at that fixed threshold retains
  45/47 in-scope rows, abstains on 44/79 OOS rows, and abstains on 5/6
  cofactor-confounded OOS rows. This is a research contract, not a production
  threshold.
- A CLI-generated confounded deployment-closure audit now ties that contract to
  the predicted-structure-vs-atlas fold channel. It confirms 6/6 priority
  cofactor-confounded rows have nearest-atlas Foldseek/TM hits and the fixed
  operating point abstains on 5/6, but production closure remains blocked by
  five train/cal OOS surface gaps.
- A companion fold-augmented novelty-variant diagnostic now records the existing
  predicted-geometry plus predicted-fold combinations without rerunning
  Foldseek/TM. The best existing-channel variant is still
  `mean_top1_raw_and_tm`, with all-OOS AUC `0.907622` and confounded-OOS AUC
  `0.911348`; this confirms the rank signal but does not select a threshold.
- A companion fold-augmented novelty operating-grid readout now enumerates
  0.95/0.90/0.85/0.80 in-scope-retention diagnostics over those existing
  variant rows. The best frozen variant artifact signal abstains on 72.15% of
  OOS rows and 5/6 cofactor-confounded OOS rows at >=90% in-scope retention; the
  best 0.90 grid row uses `mean_top1_atlas_percentile_and_tm` and abstains on
  77.22% of OOS rows. This remains a heldout review-only diagnostic.
- A geometry-only predicted-atlas operating-grid readout now enumerates the
  post-hoc retention/OOS-abstention tradeoff for all 10 frozen geometry novelty
  signals. The best geometry-only signal remains
  `negative_nearest_class_centroid_robust_distance`; at >=90% in-scope retention
  it abstains on only 22.78% of OOS and 2/6 cofactor-confounded OOS rows, so it
  remains diagnostic input rather than a standalone deployment gate.
- A matched-retention delta audit now compares that frozen geometry-only grid
  to the fold-augmented grid. Fold augmentation improves OOS and
  cofactor-confounded abstention at all four shared retention targets; at 90%
  in-scope retention, OOS abstention rises by `0.5444` and confounded-OOS
  abstention rises by `0.5`. This is still review-only and selects no threshold.
- A train/cal OOS-negative calibration surface now exists for the fold-augmented
  gate. The hash-selected 76-row surface has 71 score-complete rows with
  predicted geometry, selected organic cofactor scores, and exact Foldseek/TM
  nearest-train scores. The OOS-calibrated research contract keeps the primary
  `combined_mean_geometry_fold` threshold at `0.44155`; at that threshold it
  abstains on 28/71 calibration OOS negatives while preserving the heldout final
  readout above. The six accession-compatible active-site mapping blockers have
  been cleared; the surface remains partial because `m_csa:78` lacks an AFDB
  coordinate, `m_csa:204` and `m_csa:531` need source-geometry repair, and two
  UniProt-only rows need active-site sidecars.
- The partial train/cal OOS-negative surface is now explicitly sufficient for
  the bounded fold-augmented research contract with blocker disclosure, because
  71/76 rows are score-complete, the OOS-calibrated contract consumes exactly
  those 71 rows, no accession-compatible mapping blockers remain, and the
  primary threshold did not move. It is not sufficient for production-like
  threshold claims until the remaining five blockers are cleared.
- The remaining five train/cal OOS score-surface blockers were inspected from
  frozen inputs. None can be safely cleared without new source-backed
  active-site evidence, an alternate predicted coordinate, or an explicitly
  authorized experimental-coordinate-only policy.
- Those same five Lever 3 fold-channel deployment blockers now have
  blocker-specific review gates plus a decision-application record. Three
  coordinate-available rows (`m_csa:531`, `uniprot:P78549`, and
  `uniprot:Q3LXA3`) now have an approved source-feature sidecar surface
  materialized for rerun input, with 3 rows and 18 source-feature support
  records. `m_csa:78`/P23007 has P00889 authorized as an ortholog surrogate and
  the AFDB coordinate has been fetched and hashed. The fixed-threshold combined
  readout has now been run over the four newly combined-score rows:
  `m_csa:78` and `uniprot:P78549` abstain at threshold `0.44155`, while
  `m_csa:531` and `uniprot:Q3LXA3` are retained. The calibration-impact audit
  expands the train/cal OOS combined-score surface from 71/76 to 75/76 rows and
  raises fixed-threshold OOS abstentions from 28 to 30.
  The expanded train/cal OOS surface is now materialized as a first-class
  threshold-selection input, and the regenerated OOS-calibrated research
  contract keeps the primary threshold unchanged at `0.44155`, with 30/75
  calibration OOS rows abstained and the same heldout final readout
  (45/47 in-scope retained; 5/6 cofactor-confounded OOS abstained).
  `m_csa:204`/P10746 is explicitly kept fold-only with the
  no-non-residue-sidecar policy caveat. The post-rerun closure-status gate
  reduces the prior five production blockers to this single caveat. The
  regenerated confounded readiness gate still keeps threshold `0.44155`,
  remains research-ready for the 5/6 confounded abstention result, and stays
  deployment-blocked until P10746 is resolved by policy acceptance or an
  approved non-residue sidecar.
- Two confounded-proxy train/cal scoring tranches have now been materialized
  and joined back to the deployable predicted-structure-vs-train-atlas surface.
  The first 50-row tranche fetched 48/50 AFDB-v6 query CIFs and produced
  47/50 full-channel rows. The second 66-row structural tranche fetched 64/66
  query CIFs, ran Foldseek against the train atlas, and produced 64/66
  full-channel rows; `P00806` and `P04531` have no AFDB-v6 prediction. The
  composed
  `v3_fold_augmented_confounded_proxy_extended_train_cal_oos_surface_current702_20260603`
  gives 186/192 train/cal OOS full-channel rows. At the fixed threshold
  `0.44155`, the proxy audit abstains on 63/186 calibration OOS rows overall,
  but 0/4 high-cofactor proxy rows and only 10/55 strict same-family structural
  proxy rows. The current candidate pool still has 170 unscored ready
  train/cal OOS rows, but 0 high-cofactor-axis and 0 structural-axis rows under
  the current proxy gate, so the next scoring-tranche plan selects 0 rows and
  the input manifest fails closed on `scoring_tranche_plan_empty`. The
  background-axis blocker confirms all 170 remaining rows are background-only
  under the current proxy axes, and the scout finds 0 mechanically ready
  replacement axes without a pre-registered train/cal-only proxy-axis contract.
- The first pre-registered source-free replacement proxy axis is now
  materialized and scored. The `active_site_residue_count_10_plus` contract
  selects six train/cal-only rows (`m_csa:89`, `m_csa:90`, `m_csa:143`,
  `m_csa:253`, `m_csa:466`, and `m_csa:501`). All six have AFDB-v6 query
  coordinates, nearest-train Foldseek/TM hits, predicted-geometry scores, and
  combined fold/geometry/cofactor channel scores. `m_csa:501` was admitted only
  through the new opt-in predicted-only sequence-position repair policy, which
  uses reference sequence positions when experimental structure positions are
  absent. Composing the new tranche gives a partial 192/198 train/cal OOS
  full-channel surface with six remaining prior/base blockers. At unchanged
  threshold `0.44155`, the new proxy axis abstains 1/6 rows (`m_csa:466`) and
  retains 5/6, so it is a measured tranche readout, not a deployable
  operating-point closure. Do not rerun the global fixed-threshold proxy audit
  from this partial surface; clear the prior/base full-channel and
  policy/calibration blockers or pre-register another train/cal-only proxy axis
  before any new operating-point claim.
- A non-overlapping follow-up source-free proxy axis has now been materialized
  and scored. The `organic_score_0_30_to_below_high_axis_threshold` contract
  excludes the already scored overlap row `m_csa:89` and selects four
  train/cal-only rows (`m_csa:60`, `m_csa:75`, `m_csa:214`, and `m_csa:288`).
  All four have AFDB-v6 query coordinates, nearest-train Foldseek/TM hits,
  predicted-geometry scores, selected cofactor scores, and combined
  fold/geometry/cofactor channel scores. At unchanged threshold `0.44155`,
  only `m_csa:288` abstains. Composing the follow-up tranche gives a partial
  196/202 train/cal OOS full-channel surface with six inherited prior/base
  blockers. The post-follow-up background scout reports 160 remaining
  background-only rows, 0 active-site-count candidates, 0 organic-score
  candidates, and 8 unsupported-geometry rows that require data-quality repair
  rather than scoring. A repair-only queue now lists those 8 rows with
  accessions and required coordinate/locus gates; 0/8 expected AFDB-v6
  coordinate files are local and 0 are ready to score. This remains a measured
  tranche readout rather than a deployable operating-point closure.
- The post-P10746/Q43088 Lever 3 residual surface is now narrowed to exact
  current-evidence blockers. P10746's prior human keep-fold-only caveat has
  been reconciled, but deployment closure is still blocked. Four rows
  (`m_csa:416`/P07071, `m_csa:562`/P07658, `m_csa:586`/P00806, and
  `m_csa:637`/P04531) still lack approved deployment-valid predicted
  coordinates after AFDB v1-v6 exhaustion; local experimental CIF shortcuts
  exist for P07658/P00806/P04531 but are explicitly deployment-invalid, and a
  repo-wide sanity scan across 1,636 local CIFs found no other local CIF
  accession hit. Q43088 has a local AFDB-v6 predicted structure and one Tyr287
  role-graph anchor; a review-only nearest-neighbor scout now lists 12
  candidate locator positions, but 0 additional locators are approved and two
  are still required before any rescore. The fixed threshold remains `0.44155`
  and must not be rerun or retuned until those five surface-completeness rows
  clear. Confounded-safe calibration is also still blocked: the high-cofactor
  proxy needs 16 new fixed-threshold abstained train/cal rows and the
  same-family structural proxy needs 170.
- A downstream fold-augmented research readout now applies the fixed
  OOS-calibrated `combined_mean_geometry_fold` threshold to the seven
  review-only family expansion packets. After the repaired M-CSA primary-channel
  pass and the source-free predicted-geometry retrieval for three approved
  locator rows, it finds 15/22 primary score-complete rows, with 9
  non-abstained review-priority rows (`mh_066`, `m_csa:267`, `m_csa:131`,
  `m_csa:750`, `m_csa:551`, `m_csa:132`, `mh_073`,
  `secondary_probe::radical_sam_enzyme`, and `m_csa:116`), 6 abstained rows,
  and 7 geometry/fold-missing rows. `m_csa:973` is score-complete via its
  frozen train/calibration fold score and abstains at the fixed threshold. This
  is a triage signal only, not a family promotion or threshold change.
- The rank-1 family-panel source check for `m_csa:267` is complete from frozen
  local artifacts and keeps the row as a review-only OOS boundary control:
  local M-CSA graph evidence supports dihydrodipicolinate synthase lysine
  Schiff-base aldol/cyclization chemistry rather than any current seed-family
  promotion.
- The rank-2 family-panel source check for `m_csa:131` confirms source-backed
  flavin monooxygenase/oxygen-transfer support for the existing secondary-probe
  row, but does not authorize primary FMO promotion while subtype,
  coordinate/materialization, hard-negative, and expert-admission blockers
  remain active.
- The rank-3 family-panel source check for `m_csa:750` reads through the current
  registry and existing label-revision artifact, keeping it as OOS/boundary
  evidence and a future radical flavin/Fe-S dehydratase candidate, not a
  current v1 flavin, FMO, cobalamin, or radical-SAM promotion.
- The rank-4 family-panel source check for `m_csa:551` confirms mechanism-clean
  future FMO support, but the prior local adjudication explicitly blocks import
  and registry edits.
- The repaired M-CSA primary-channel pass cleared the remaining M-CSA
  missing-channel rows without label, threshold, split, import, registry, or
  production-scorer changes. `m_csa:132` uses real-sequence accession `P07740`
  and nearest-atlas TM `0.6879`; `m_csa:116` uses the accession-compatible
  `Q2RSB2` residue subset and nearest-atlas TM `0.5417`. Both are
  non-abstained under the fixed research gate and have frozen-local
  source-check packets: `m_csa:132` remains secondary FMO support only, and
  `m_csa:116` remains an OOS transhydrogenase/hydride-transfer control.
- The family-panel primary-channel gaps are queued separately. The original
  10 secondary/external rows all have source-backed predicted-fold scores; after
  approved source-free locator scoring for three rows, 7 still lack
  source-free predicted active-site geometry top1 scores. There are no
  remaining M-CSA rows in the missing primary-channel queue.
- The 10-row missing queue now has a review-only source-backed materialization
  plan and a scored P0/P1 materialization. It selects Q59490 for the cobalamin
  secondary probe, A0A1M6T2I7 for the radical-SAM secondary probe, Q6NSJ0 for
  the glycoside placeholder, and seven prior-resolved metal-hydrolase/boundary
  representatives. All 10 sidecars record PDB and AFDB-v6 coordinate hashes and
  real Foldseek/TM hits against the frozen predicted atlas, with nearest TM
  scores from `0.4655` to `1.004`. These rows remain review-only and are not
  primary-channel score-complete until source-free predicted geometry is
  materialized.
- The source-free predicted-geometry sidecar manifest now narrows that blocker:
  10/10 queued rows have AFDB-v6 CIF hashes and source-backed Foldseek/TM
  scores, 3/10 have approved source-free active-site locator sidecars, and
  7/10 remain blocked on approved locators. The
  companion locator schema requires at least two source-free sequence-position
  residue locators and forbids source prose, entry names, EC/Rhea identifiers,
  labels, benchmark roles, and panel IDs as predictive geometry features. The
  schema audit currently reports 3/10 locator sidecars present and passing,
  with `locator_sidecar_missing` as the remaining critical violation class. A
  materialization plan names the exact locator sidecar paths and rerun commands;
  eight rows start from structure-local ligand geometry candidates, while
  `mh_067` and `mh_068` require split-safe train/cal-template checks due to
  same-accession current702 geometry matches. A template-only bundle stages all
  10 locator sidecar shells outside the audited locator directory; none are
  scoring-ready until validated source-free residue locators are added and the
  schema audit is rerun.
- A review-only source-free locator candidate audit now stages coordinate-only
  contact candidates outside the audited locator directory. Eight of the 10
  rows have at least two selected-structure ligand/metal contact candidates;
  Q59490 and C7C422 remain blocked by no non-water/non-metal ligand candidate
  in the selected PDB coordinate. Six candidate rows have all candidate
  positions prevalidated against matching `_struct_ref_seq` UniProt mapping;
  Q79MP6 and P0A6P9 still need position validation. All 10 candidates remain
  not ready for predicted-geometry scoring until manual review,
  forbidden-feature review, and any split-safe template checks pass.
- A companion candidate-integrity audit checks those 10 staged sidecar files
  against the candidate audit payload and review-only guardrails. All 10 pass
  file/payload/guardrail integrity checks, remain outside the audited locator
  directory, and still have 0 scoring-ready rows.
- A companion source-free locator review queue ranks those candidates: three
  rows (`mh_066`, `mh_073`, and `secondary_probe::radical_sam_enzyme`) are
  priority-1 for manual forbidden-feature review; Q6NSJ0 needs ligand
  specificity review, P00918/P15289 need split-safe template checks,
  Q79MP6/P0A6P9 need position validation, and Q59490/C7C422 need a new
  source-free locator path or alternate coordinate.
- The manual locator review packet now combines candidate sidecar SHA-256s,
  integrity status, priority classes, and per-row review checklists. It is the
  exact next human-review artifact; no row is copy-ready or scoring-ready.
- A priority-1 locator review preflight dry-ran schema compatibility,
  guardrail cleanliness, and coordinate-contact plausibility for `mh_066`,
  `mh_073`, and `secondary_probe::radical_sam_enzyme`. All three passed the
  automation preflight, with `mh_073` carrying a minimum-two-locator warning.
  Human approval has since moved these three sidecars into the audited locator
  directory and made them scoring-ready.
- A blocked-row rescue manifest now inspects the two no-ligand locator rows.
  Both selected coordinates contain only water HETATMs. `mh_064` has five
  frozen source alternate PDB IDs (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, and `3SPU`)
  staged as exact fetch commands pending manual approval; Q59490 has no frozen
  alternate beyond `1L1L` and needs a new nonlabel locator strategy or an
  explicitly authorized alternate source row.
- A review-only FMO subtype/hard-negative packet keeps `m_csa:131` and repaired
  `m_csa:132` as secondary-probe support, `m_csa:551` and `m_csa:973` as future
  support only, and `m_csa:750` as radical flavin/Fe-S boundary negative. No
  FMO row is import-ready or registry-edit-ready.
- The high-value glycyl-radical/thiamine panel now has a no-template
  feature-refresh guardrail. Its two rows (`m_csa:30` and `m_csa:31`) are
  score-complete and abstained at the fixed research threshold, but both are
  heldout OOS/final-only controls, absent from the P0 train/cal readiness
  audit, and absent from the train/cal feature contract. They may be
  source-checked as review-only heldout evidence, but must not feed the
  no-template train/cal feature refresh.
- A source-free predicted-geometry retrieval now scores the three approved
  locator rows (`secondary_probe::radical_sam_enzyme`, `mh_073`, and `mh_066`)
  against the existing geometry fingerprint surface using only approved residue
  locators and local AFDB-v6 CIFs. All three rows resolve at least two predicted
  residues and are retained by the existing `combined_mean_geometry_fold`
  research threshold when joined to their source-backed fold scores. This is
  review-only evidence; seven family-panel rows remain blocked on approved
  source-free locators and no labels, imports, thresholds, splits, or
  production scorers changed.
- The family-panel evidence packets now consume the approved source-free
  retrieval where applicable: `secondary_probe::radical_sam_enzyme`, `mh_066`,
  and `mh_073` are geometry-ok in their packet rows. The packet coverage audit
  now reports 15/22 family-panel rows with predicted geometry and 21 rows with
  predicted-fold hits while preserving all review-only guardrails.
- The highest-value glycyl-radical/thiamine-radical boundary panel now has a
  readiness packet. Both rows (`m_csa:30` and `m_csa:31`) are score-complete
  and abstain under the fixed fold-augmented research threshold, so they are
  ready only as review-only OOS boundary controls. Both still lack
  source-backed row-specific bond-change evidence and expert mechanism-locus
  validation before any family-expansion discussion.
- A companion source-check preflight now packages the three newly non-abstained
  source-free geometry rows for local review. It holds `mh_066`, `mh_073`, and
  `secondary_probe::radical_sam_enzyme` as review-only pending source checks,
  with `mh_066` showing geometry/fold agreement and the other two requiring
  mechanism-locus and duplicate/leakage review before any family decision.
- The first source-free geometry source check is complete for `mh_066`. Frozen
  local evidence supports an IMP-1 zinc metallo-beta-lactamase hydrolase
  context and both source-free geometry plus predicted-fold channels agree on
  `metal_dependent_hydrolase`, but the row remains an external non-countable
  review-only expansion candidate. It is not import-ready because row-specific
  bond-change/residue-role evidence, duplicate/split review, and expert
  admission are still unresolved.
- The second source-free geometry source check is complete for `mh_073`. Frozen
  local evidence supports an H-Ras Mg/GTPase nucleotide locus, while source-free
  geometry and predicted-fold channels disagree. The nearest fold hit is a
  current702 GTPase-like `metal_dependent_hydrolase` seed, so the row is kept
  as a review-only Mg/nucleotide boundary hard negative rather than promotion
  support.
- The third source-free geometry source check is complete for
  `secondary_probe::radical_sam_enzyme`. Frozen local evidence supports a TigE
  radical-SAM/Fe-S locus, but source-free geometry calls
  `metal_dependent_hydrolase` and the nearest predicted-fold hit is a
  `plp_dependent_enzyme` seed. The row remains secondary review-only evidence,
  not import-ready family promotion support.
- A remaining source-free locator blocker action queue initially classified
  seven family-panel rows after the three source checks. Two rows,
  `mh_067`/`mh_068`, have since passed copy approval, source-free geometry
  scoring, and source checks as review-only/no-promotion rows. The remaining
  five blocker rows are `mh_065`, `mh_072`, `external_glycoside_panel`,
  `mh_064`, and `secondary_probe::cobalamin_radical_rearrangement` (Q59490).
- The `mh_065`/`mh_072` UniProt position-validation attempt is complete and
  keeps both rows blocked. Their candidate contacts are coordinate-local, but
  frozen selected PDB mappings point to `Q932P5` for `1DDK` and `P08324` for
  `1E9I`, not the source accessions `Q79MP6` and `P0A6P9`. Do not copy these
  locator sidecars or score source-free predicted geometry. A local-cache
  matching-coordinate scout found 0 non-AFDB replacement coordinates;
  same-accession AFDB files exist but already failed residue-transfer with 0/6
  expected residue-code matches. The human decision is to leave both rows
  blocked; unblock only with matching frozen coordinates or a real expert
  alignment/remap that resolves the residue-code mismatch.
- The `external_glycoside_panel` ligand-specificity path remains blocked.
  The selected acetate (`ACT`) locator from unliganded MYORG `7QQF` was
  rejected, NAG contacts remain glycan/glycosylation-context evidence, and a
  local-cache substrate-coordinate scout found 0 same-accession substrate-like
  candidates. The block decision now explicitly rejects copying acetate,
  NAG/glycan, or raw glycan/buffer retargeting. Do not copy or score this row
  until a dedicated substrate-complex coordinate or expert-approved non-glycan
  locator exists.
- The final no-ligand locator blocker packet isolates two policy decisions:
  `mh_064` needs explicit approval before fetching five frozen alternate PDBs
  (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, `3SPU`), and Q59490 needs a nonlabel
  locator strategy or approved alternate source row. A local-cache Q59490
  alternate-source scout found 0 eligible alternate rows. The Q59490 block
  decision now leaves the row blocked rather than fabricating residue locators
  from panel identity or source prose. The `mh_064` block decision now leaves
  the row blocked rather than fetching unapproved alternate coordinates.
  Automation did not fetch coordinates, copy sidecars, or score predicted
  geometry for either blocker.
- A refreshed source-free locator blocker status plus human-decision matrix now
  consolidates the five remaining blocker rows into four decision classes.
  Automation discovery is complete, 0/5 are automation-clearable, 0 are
  import-preview-ready, and `mh_065`/`mh_072` have now been explicitly left
  blocked rather than remapped; `external_glycoside_panel` is now explicitly
  left blocked rather than acetate/NAG-retargeted; Q59490 is now explicitly
  left blocked rather than nonlabel-fabricated or alternate-source-substituted.
  `mh_064` is now explicitly left blocked rather than fetch-authorized. No
  locator-policy decision remains automation-clearable; all remaining unblock
  paths require external approval/evidence before any copy, fetch, scoring,
  import, or label action. The consolidated locator-policy closure status
  records 5/5 blocked locator rows, 0 automation-clearable locator decisions,
  0 rows approved for copy/scoring, 0 import-preview-ready rows, and 0 countable
  label candidates.
- The family-panel import-preview blocker gate has been refreshed against that
  enriched matrix. It still reports 0/22 import-preview-ready rows, 0 countable
  label candidates, 11 completed source checks that remain review-only/no
  promotion, 6 expert family-admission blockers, and 5 source-free
  locator/primary-channel blockers.
- A refreshed current-run artifact integrity audit indexes 28 JSON artifacts
  and 28 matching work reports from this run, including the P0 train/cal
  feature sidecar, coverage-gap audit, and calibration review packet. All
  parse/presence checks passed, and the validation summary records full pytest,
  unittest discovery, compileall, `validate`, repo-wide JSON/JSONL parse,
  current-docs reference check, and diff-check success.
- Learned-representation results are diagnostic, not decision-grade. ESM-2
  logistic is the strongest local learned comparator in the Wave 1.2 table but
  does not displace geometry. ESM-C logistic versus ESM-C cosine shows decoder
  choice is a real confound.
- Mechanism-feature embedding readiness now includes a normalized row-level
  active-site residue-role graph sidecar for 656 current702 rows. This closes
  the role-vocabulary sidecar gap only; directed electron/proton-transfer edges
  and row-specific bond-change mapping remain future feature work. A separate
  reaction-center template sidecar row-aligns fingerprint-level chemical
  operations and bond-change descriptors for 232 rows, but it is not
  row-specific reaction evidence.
- A no-fit row-specific bond-change schema now makes that remaining feature gap
  explicit: 232 rows require source-backed row-specific bond-change evidence,
  with allowed event types, required sidecar fields, forbidden predictive keys,
  and a materialization queue staged before any embedding pilot can consume the
  feature. No source evidence was materialized and no model was fit.
- A companion feature-contract gap audit confirms that the staged
  row-specific bond-change schema has not entered the current no-fit
  mechanism-feature contract: 524 train/cal feature rows contain 0 bond-change
  feature rows, 0 heldout rows, and the strict feature-contract audit still has
  0 critical violations.
- The row-specific bond-change gap now has a no-fit materialization priority
  manifest. It partitions the 232 evidence-required rows into 171 P0 train/cal
  feature-contract gap rows, 13 P1 in-distribution rows needing upstream
  feature-bundle repair, and 48 P2 heldout final-only rows, plus a balanced
  15-row P0 pilot seed queue. It materializes no source evidence and mutates no
  feature contract.
- A no-fit P0 source-graph readiness audit now checks that balanced 15-row
  pilot seed against the frozen M-CSA graph. All 15 rows have entry nodes,
  mechanism-text edges, catalytic-residue edges, and EC mappings; 11/15 have
  local EC-to-Rhea mappings; 0/15 expose structured row-specific bond-change
  event edges. Manual/source-backed extraction remains required before any
  feature-contract refresh.
- A companion P0 extraction work package turns that readiness result into 15
  manual extraction templates with nine required source-backed fields, exact
  event/mapping acceptance criteria, and per-row Rhea lookup flags. It still
  materializes no source evidence and authorizes no feature-contract or model
  use.
- A strict audit now validates that P0 extraction work package as
  template-only: all 15 rows have the expected nine fields, 0 rows contain
  non-null extracted values, 0 rows are contract/model consumable, and the audit
  reports 0 critical violations.
- A companion TSV worksheet now gives the next run a manual filling surface for
  those same 15 P0 rows. All source-evidence cells are blank by construction;
  four rows are flagged for Rhea lookup, and the worksheet must be audited after
  any source-backed values are filled.
- A source-evidence sidecar schema now stages the future filled sidecar contract
  for that worksheet: 12 required row fields, six event fields, four mapping
  fields, forbidden predictive fields, and strict evidence/leakage checks. It
  is schema-only and still materializes 0 source values.
- The P0 worksheet now has a draft source-evidence sidecar derived from frozen
  local M-CSA graph evidence. All 15 rows have source spans and draft
  bond-change events. After the bounded official Rhea lookup resolution, 12/15
  have Rhea equations and 3/15 remain Rhea-missing. `m_csa:5`, `m_csa:11`,
  and `m_csa:169` now carry reviewer-approved M-CSA-only provenance from
  Vivek Vardhan Arrabelli, so 3/15 rows are feature-contract-consumable only
  through train/cal split filtering. The remaining 12 rows stay draft.
- A companion manual-review queue ranks those 15 draft rows without changing
  review state. It now separates the three approved M-CSA-only rows from the
  12 remaining draft rows: five high-complexity multi-event rows including
  Rhea-resolved `m_csa:124`, then seven standard draft reviews. It authorizes
  no full feature-contract refresh, model use, label change, or threshold
  change.
- A bounded official Rhea lookup resolution queried the four staged EC/accession
  rows. Exact EC queries returned no Rhea records, but accession `P00396`
  resolves `m_csa:124` to `RHEA:11436` with Rhea EC `7.1.1.9`, reflecting an
  EC reclassification away from the worksheet `ec:1.9.3.1`. The remaining Rhea
  lookup manifest is now empty because the three unresolved official Rhea rows
  are reviewer-resolved as M-CSA-only source evidence, not Rhea-resolved.
- A bounded official-source audit rechecked those three remaining rows against
  Rhea EC queries with and without the `ec:` prefix, Rhea accession queries, and
  current UniProtKB catalytic-activity records. Rhea still returns 0 records;
  UniProt confirms matching EC activity for all three accessions but provides
  no Rhea cross-references. These rows are not automation-resolvable from
  official Rhea/UniProt alone; the sidecar now records the human decision to
  approve M-CSA-only source evidence for all three with reviewer provenance.
- A companion reviewer decision matrix now makes that human gate explicit for
  `m_csa:11`, `m_csa:169`, and `m_csa:5`. Each row has three allowed decision
  options: approve M-CSA-only source evidence with reviewer provenance,
  reject/rewrite draft events, or hold for an authorized alternate reaction
  source. The matrix now records 3 reviewer IDs, 3 copy-ready approved
  decisions, and 3 feature-contract-consumable rows.
- A strict consumption audit confirms that the Rhea lookup resolution is used
  only as review evidence: `m_csa:124` carries `RHEA:11436` in the sidecar,
  the three Rhea-absent rows are reviewer-approved M-CSA-only evidence, and
  there are 0 unresolved lookup rows, 3 feature-contract-consumable rows, and
  0 model-training-eligible rows.
- A P0 feature-readiness audit now makes the no-template embedding blocker
  exact. All 15 rows are structurally ready as source-evidence rows,
  with 10 rows carrying bond-change events, 6 carrying proton-transfer events,
  and 9 carrying electron-transfer events. Three rows are approved and
  consumable for split-filtered train/cal materialization, but the feature
  contract contains no row-specific bond/proton/electron fields and the full
  15-row refresh remains blocked until the remaining 12 draft rows are reviewed.
- A companion P0 refresh-blocker audit now packages that into the automation
  decision: full no-template feature-contract refresh is not allowed from the
  P0 sidecar, but partial train/cal feature materialization is allowed for only
  the 3 approved rows. The load-bearing guardrail is that M-CSA-derived
  row-specific bond-change features must remain train/cal-only; heldout M-CSA
  rows must not be used for training or threshold tuning.
- The partial train/cal feature sidecar for those approved P0 rows is now
  materialized. It copies only label-stripped row-specific event features for
  `m_csa:5`, `m_csa:11`, and `m_csa:169`; all three are assigned to the train
  split, 12 draft rows are excluded, 0 heldout rows are present, and no model or
  threshold is fit. The materialized approved event surface carries three
  `bond_broken`, two `bond_formed`, two `electron_transfer`, and two
  `proton_transfer` events, but it is not enough to rerun the no-template
  centroid or residual methods because it has no calibration rows. A strict
  guardrail audit passes with 0 critical violations and confirms the predictive
  payload is numeric/boolean event features only.
- A companion P0 train/cal coverage-gap audit makes the next review gate
  exact: the remaining draft P0 queue has 8 train rows and 4 calibration rows.
  The no-template rerun is blocked by absent approved calibration coverage. The
  next manual review rows are `m_csa:186`, `m_csa:147`, `m_csa:6`, and
  `m_csa:133`; `m_csa:186` and `m_csa:147` also add the currently
  unmaterialized `bond_order_changed` event type. A manual calibration review
  packet now carries those four rows and 16 event-review records without
  recording approvals or changing the feature contract.
- The mechanism-feature role-graph and reaction-center sidecars now pass a
  strict schema and row-alignment audit over all 702 current rows with zero
  critical violations. This validates the current sidecars as schema-safe
  train/cal-only embedding inputs, not as new mechanistic supervision.
- The mechanism-feature cofactor-locus gap now has a stricter review-only schema
  and materialization queue for `metal_ion_locus`, `cobalamin_locus`,
  `radical_sam_locus`, and `iron_sulfur_locus`. It uses existing geometry
  ligand context only: 176 current702 rows have proximal metal context, 4 have
  cobalamin, 8 have SAM, and 17 have Fe-S cluster context.
- The review-only `metal_ion_locus` sidecar is now materialized for all 702
  current rows from existing geometry ligand context. It marks 175 rows with
  proximal metal context, 85 with structure-wide-only metal context, 422 with no
  metal context, and 20 with unsupported/missing geometry. It is not label or
  predictive evidence until a future train/cal-only embedding pilot consumes it
  under split filtering. Its strict schema audit passes with zero critical
  violations.
- The review-only `cobalamin_locus` sidecar is also materialized and audited. It
  marks 4 rows with proximal cobalamin context, 678 with no cobalamin context,
  and 20 unsupported/missing-geometry rows; there are no structure-wide-only B12
  rows in the current geometry source.
- The review-only `radical_sam_locus` and `iron_sulfur_locus` sidecars are now
  materialized and audited from the same existing ligand context. The
  radical-SAM sidecar marks 8 proximal SAM-context rows and 2
  structure-wide-only rows; the Fe-S sidecar marks 17 proximal Fe-S-context rows
  and 11 structure-wide-only rows. Both carry explicit SAM/Fe-S copresence
  status, keep predictive/import flags false for all 702 rows, and pass schema
  audits with zero critical violations.
- A completion audit now confirms that all four schema-named cofactor-locus
  sidecar classes are materialized for 702 rows and schema-passing with zero
  critical violations.
- A no-fit mechanism-feature embedding train/cal input manifest now enumerates
  the current sidecar surface without fitting weights or evaluating heldout
  rows. It keeps all 140 heldout rows excluded, marks 562 in-distribution
  candidate rows, and finds 524 rows with the minimal role-graph plus organic
  and inorganic cofactor-locus feature bundle.
- A deterministic train/cal split manifest now partitions those 524 ready
  mechanism-feature rows into 418 train rows and 106 calibration rows across six
  strata. Heldout remains excluded, 38 train/cal candidates remain blocked by
  role-graph readiness, and no model weights or thresholds are fit.
- A no-fit mechanism-feature embedding feature contract now strips labels from
  the ready train/cal feature-row surface. It exposes 524 feature rows with 418
  train and 106 calibration assignments, records allowed feature groups
  (role-graph, reaction-template, organic cofactor, and inorganic cofactor
  loci), excludes heldout rows, and keeps model fitting explicitly blocked until
  authorized.
- A strict audit now validates that feature contract against train/cal row
  alignment, forbidden label/outcome field exclusion, no-heldout discipline, and
  no-model-fit guardrails. It passes for 524/524 rows with zero critical
  violations; model fitting remains blocked until explicitly authorized.
- A train/cal-only mechanism-feature embedding pilot now consumes the audited
  feature contract directly. It fits standardized nearest-primary centroids on
  the 418 assigned train rows and selects a >=90% primary-retention threshold
  on the 106 calibration rows. The full contract reaches calibration AUC
  `0.948491` and 100% OOS abstention at 91.43% primary retention, but the
  no-reaction-template ablation drops to AUC `0.549698` and 14.08% OOS
  abstention at the same retention target. Treat this as a real implementation
  result and a clear signal that the next mechanism-feature work must close
  row-specific bond-change/proton/electron-flow features and then materialize
  the same allowed feature surface for heldout once-only readout; do not trust
  the full-contract score as production evidence.
- That heldout readout is now materialized once. Existing sidecars provide the
  same allowed feature surface for 132/140 heldout rows; 8 remain blocked by
  accession-compatible role-graph gaps. The full-contract variant reaches
  heldout AUC `0.8812` and abstains on 100% of ready OOS rows at the
  calibration-selected threshold, but retains only 75% of ready primary rows.
  The no-reaction-template ablation is near chance on heldout (AUC `0.488591`,
  9.52% OOS abstention at 85.42% primary retention). This confirms the real
  next lever is row-specific mechanism-feature materialization, not another
  template-level classifier.
- The out-of-span residual is the surviving deployable signal from this lever and
  is now confirmed. Built on a separate closed-form information-preserving metric
  line (an independent Lever 2 build), the unsupervised out-of-atlas-span residual
  survives a PCA cutoff-robustness sweep and a held-out-from-design confirmatory
  split with a label-permutation null (p=0.0005). Unlike the template-dependent
  centroid scores it is sequence-only and deployment-valid.
- That confirmed residual is integrated into the per-channel rule gate as a third
  lift channel, adding a +0.076 confounded-safe OOS-abstain lift at the >=85%
  in-scope retention floor. The residual threshold remains research-grade pending a
  deployable calibration.
- 2026-06-02: the two independent Lever 2 builds are integrated into one result
  (see `docs/decision_log.md` 2026-06-02). The consolidated negative — a learned or
  standardized embedding over the CURRENT feature surface does not deployably beat
  geometry — is robust precisely because both builds reach it independently. The
  confirmed gate-integrated residual is the live deployable signal; the centroid
  line's train/cal/heldout discipline (418 train / 106 calibration / once-only
  heldout) becomes the calibration standard the residual must meet; and its
  bond-change/proton/electron feature-materialization track (Rhea provenance) is the
  kept forward path to the genuinely-new mechanism feature. No code or artifacts from
  either build were removed.
- Later 2026-06-02 Lever 2 artifacts materialize the approved row-specific
  bond/proton/electron surface into a 43-row train/cal OOS-augmented feature
  surface and freeze a calibration-only no-template pair contract. The stronger
  pair (`event_residue_role:proton_transfer|electrostatic_stabiliser` plus
  `residue_code_count:his=3`) reaches calibration OOS abstention 0.857143 at
  the residual threshold 3.21469422, with heldout still unread. Deployment is
  blocked by the missing source-free proton-transfer event-axis linker and
  current702 heldout locator surface. A His-count-only fallback avoids the
  event axis but drops calibration OOS abstention to 0.642857 and requires
  explicit acceptance before any heldout read.
- 2026-06-03 Lever 2 outcome (see `docs/decision_log.md`): the 53 priority-1
  source-free heldout locators were reviewed (approve 53, reject `m_csa:723`,
  `m_csa:599`) and materialized into the audited locator dir. The source-free
  proton-transfer/electrostatic-stabiliser event axis was then drafted by a
  deterministic label-blind rubric and reviewed, but **not signed off**: only
  14/53 rows can evidence the pair source-free (cofactor-anchored locators miss
  the substrate-proximal catalytic machinery for metal/heme sites). A train/cal
  source-free token re-selection (heldout never read) then showed **no
  source-free-replicable token clears a useful bar** — multivariate LOO-CV AUC
  0.538, and the His-count fallback's signal was role-dependent (source-free,
  `HIS>=3` fires only on OOS rows). Decision: **defer Lever 2**; do not spend the
  one-shot heldout read on any Lever 2 token. The 53 approved locators are banked
  as a split-protected asset; the source-free discriminative value lives in the
  geometry/fold channel (AUC 0.81-0.91).
- 2026-06-03 ESMFold2 robustness experiment staged (see `docs/decision_log.md`):
  ESMFold2 was verified real (Biohub / A. Rives, 2026-05-27, MIT/open weights).
  Problem 2 (robustness to predicted vs experimental active-site geometry) is now
  staged as a no-fit, leakage-safe contract plus a runnable `esmfold2`
  coordinate-supplier backend in `predicted_geometry_robustness.py`. The contract
  enumerates the exact prediction work list (184 in-distribution+fingerprint
  atlas rows, 140 heldout rows, 323 unique accessions), fixes the
  train/cal-selects-thresholds / heldout-final-only discipline, records the
  AlphaFoldDB-v6 baseline to beat (hand router 23/45 primary, 12.3% OOS FP;
  fold/TM AUC 0.814; geometry+fold mean AUC 0.908), and plans six comparison
  metrics including pLDDT-gated abstention vs the fixed 0.44155 fold-augmented
  gate. No ESMFold2 inference was run, no weights downloaded, no threshold
  changed, no heldout row read. The apo caveat is kept front and center: ESMFold2
  improves the protein side-chain part and supplies pLDDT, but cannot supply
  cofactor geometry, so expect only partial help. Run via
  `build-esmfold2-robustness-experiment-contract` and the three predicted-geometry
  commands with `--backend esmfold2 --esmfold2-staged-dir <DIR>`.
- 2026-06-03 predicted-geometry failure decomposition (see `docs/decision_log.md`,
  backend-agnostic, no fit): the AlphaFoldDB-v6 45/45 -> 23/45 primary drop is
  **cofactor-loss-dominated**. Of 22 lost primary rows, **22/22 are
  `cofactor_apo_loss`** (cofactor/metal proximal experimentally, absent in the apo
  prediction; all residues resolved) and **0 are fold/side-chain-limited**. So an
  apo folder (ESMFold2) has a primary-recovery upper bound of 0 here and is
  demoted to a secondary role: OOS false-positive reduction (10 FPs: 7
  cofactor-apo-loss + 3 fold) and pLDDT-gated abstention. The real Problem-2 lever
  is **cofactor-awareness** (place/dock the cofactor, or a sequence
  cofactor-presence channel). Control: 13/23 correct primaries also had an
  experimental cofactor, so apo geometry can suffice for some rows. Re-run the
  decomposition on a future ESMFold2 audit to confirm the pattern.
- 2026-06-04 cofactor restoration recovery probe (see `docs/decision_log.md`,
  counterfactual, no fit, frozen threshold/fingerprints): restoring the
  experimental cofactor onto the predicted apo backbone recovers **22/22
  cofactor_apo_loss lost primary rows** (100%; readthrough 20/20), with per-row
  score lifts 0.08–0.41 and every row flipping to the correct fingerprint. The apo
  control rescore reproduces the audit exactly
  (`apo_control_rescore_matches_audit: true`). This confirms the predicted backbone
  is faithful and the missing cofactor is the entire loss, so cofactor-restoration
  is the Problem-2 lever with a perfect-information ceiling of all 22. It is an
  upper bound (perfect placement); real docking is imperfect.
- 2026-06-04 cofactor graft fidelity probe (see `docs/decision_log.md`,
  coordinate-free, no fit): a realistic rigid graft (judged by whether the
  predicted active-site internal pairwise-distance distortion stays within each
  cofactor's proximity margin) recovers **19/22** vs the 22/22 upper bound. 20/22
  predicted active sites are faithful (internal RMSD <= 1.5 A; most 0.12–0.6 A).
  The 3 non-realistic rows (`m_csa:213` RMSD 18.6 A, `m_csa:854` RMSD 8.2 A, and
  `m_csa:714` failing the proximity margin) are where the predicted backbone is
  distorted — exactly the boundary where the ESMFold2 secondary lever (better
  predicted geometry) would help. numpy is unavailable here, so the true
  atom-level graft (superpose catalytic residues, transplant cofactor atoms,
  re-score) is the documented next escalation; predicted heldout CIFs are already
  staged under
  `artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/queries_all_heldout/`.
- A no-fit mechanism-feature train/cal guardrail audit now pins the same
  surface across the input manifest, split manifest, and feature contract: 524
  feature rows exactly match 524 split rows, 140 heldout rows remain excluded,
  and label identity fields are not features. This still does not authorize
  model fitting or heldout evaluation.
- ProtT5 and SaProt have only NN/cosine-style local standardized exports today.
  Matched logistic-head reruns are blocked until raw local sidecars or weights
  exist; do not download large models for this by default.
- FMO remains secondary-only. Local FMO rows and external candidates are useful
  review/acquisition evidence, but no canonical primary promotion, registry
  change, threshold change, production scorer change, or import is authorized.

## Expansion And Generalization Constraints

- **LOMO (Leave-One-Mechanism-Out) open-set eval already ran and is a recorded NEGATIVE
  baseline — it MOTIVATES targeted expansion; it is NOT a pending gate.** Result: no exact
  open-set recovery (sources: merged lever-2 readouts,
  `docs/session_decision_record_20260530.md`, the merged
  `automation/lomo-frozen-snapshot-current702-20260530` infra, and
  `work/lomo_frozen_snapshot_transfer_current702_20260530.md`). **Do NOT rerun LOMO as a
  prerequisite for expansion.** The one durable hygiene action: **preserve/record the frozen
  pre-expansion snapshot/tag now** — expansion adds rows, and once it does a clean
  pre-expansion baseline can no longer be reconstructed. If a future generalization
  re-baseline is ever wanted, run it against that frozen snapshot and keep expansion
  row-adds out of the eval split — optional hygiene, not a blocker on targeted expansion.

## Concluded And Archived Tracks

- **ePK (eukaryotic protein kinase) family expansion = NO-GO** for heuristic geometry
  (`docs/epk_heuristic_geometry_no_go_20260521.md`). The 5 research tracks
  (`false-positive-hunter`, `policy-harness`, `positive-evidence`, `sibling-controls`,
  `substrate-role-identity`) are **archived as recoverable tags** `archive/epk-*` (NOT
  merged — their conclusions are captured; their code stays out of main). Detailed
  learnings live in the tags under `artifacts/research_lanes/epk_*` (candidate-conflict,
  false-negative state-topology, source-free adjudication requirement, terminal blocker
  classes). Restore with `git checkout archive/epk-<track>` only if revisited.
- **Branch consolidation complete (2026-06-06):** every research track is unified into
  `main` (PRs #4 cofactor, #5 youthful Problem-2, #6 lever-2 electron-flow + trailing
  commits; earlier representation-shootout / LOMO-snapshot / organic-cofactor / Lever-2
  PRs already in main). Only the 5 `archive/epk-*` tags remain unmerged. `main` is the
  single source of truth; `work/handoff.md` is an auto-generated ledger (this file +
  `docs/session_decision_record_*` are the durable human handoff).

## Active Blockers

- **Precision operating point for cofactor fusion — precision side now MEASURED
  leakage-safe (2026-06-09).** The confirmed 23 -> 37/45 recovery came with OOS/sec FP
  rising 12.3% -> 25.9%, but that was the spent heldout read. The precision side now has a
  reusable leakage-safe train/cal OOS surface
  (`artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json`,
  CLI `build-cofactor-fusion-operating-point`). On the out-of-sample calibration surface
  the **recalibrated-threshold dial dominates the suppression dial**: threshold 0.44 keeps
  recall 30/35 while dropping OOS FP 9/26 -> 8/26, whereas the suppression dial reaches the
  same 8/26 only by sacrificing 7 in-scope primaries (recall 23/35). Prefer the
  recalibrated threshold; layer the complementary Lever-2 electron-flow OOS lift (+0.04 at
  primary retention 1.0, a different surface). Still open: choosing a *deployable* point is
  a separately authorized decision (thin 26-row cal OOS set; partial coordinate coverage)
  and must not be tuned against the spent heldout one-shot.
- Fair ProtT5/SaProt logistic-head comparison needs local raw embedding or
  structure-token sidecars and an ESM-2-style train/cal-only head. Existing
  local exports are not equivalent decoders.
- Sequence-to-deployment geometry is blocked by predicted-structure active-site
  degradation: AlphaFoldDB has no proximal ligands and perturbs the hand
  geometry evidence enough to introduce primary wrong calls and OOS false
  positives. ESMFold is not locally available without staging runtime/weights.
  The ESMFold2 experiment (Problem 2) is now staged as a no-fit contract with a
  runnable `esmfold2` coordinate-supplier backend, but stays blocked here on
  staged coordinates: `torch`/`esm`/`foldseek` are absent and every
  predicted-structure host (Hugging Face, ESM Atlas, AlphaFold EBI) returns
  network 403. Run it where ESMFold2 coordinates can be staged.
- FMO primary promotion is blocked by missing or unsuitable exact coordinate
  materialization for key external subtype rows, subtype/child-stratum
  definition work, PHBH-leaning gate behavior, hard-negative separation, and
  expert review.
- `m_csa:497` and `m_csa:750` must not be used as primary flavin support in old
  Wave 1 cells. They are OOS/boundary negatives under the current registry.
- Review surfaces are not labels. AI-visual review packets, PyMOL queues, FMO
  scouts, and external packets are review-only until a dedicated import preview,
  label-factory gate, and batch acceptance authorize counting.
- Disk must stay above 10 GiB free. Avoid large downloads and broad artifact
  regeneration unless the task explicitly asks for them.

## Next Gates

0. Problem 2 (recommended): the failure decomposition + cofactor-restoration probe
   settled the lever. The 45/45 -> 23/45 drop is cofactor-loss-dominated (22/22
   lost primaries are `cofactor_apo_loss`), and restoring the cofactor onto the
   predicted apo backbone recovers **22/22** (the backbone is faithful), so the
   **primary lever is cofactor-awareness**, not a better apo folder, with a ceiling
   of all 22 (realistic 19/22 by the coordinate-free graft fidelity probe; the 3
   distorted-backbone rows are abstention cases and the ESMFold2 boundary).
   The solution architecture is generalized (see the 2026-06-04 "Problem 2 Solution
   Architecture" decision-log entry): diagnose the deploy-missing context ->
   bound the ceiling -> reconstruct the context from sequence -> fuse + abstain.
   Steps 1-2 are built and class/backend-agnostic. **Step 3 is now DONE and confirmed
   (2026-06-06):** the leakage-safe train/cal **sequence -> cofactor-presence channel**
   (`src/catalytic_earth/cofactor_presence_calibration.py`, supervised by STRUCTURAL
   ligand context only) was fused into the router where the experimental `ligand_context`
   plugs in, and the heldout one-shot moved predicted-apo primary **23/45 -> 37/45** (+14;
   OOS/sec FP 12.3% -> 25.9%); the in-distribution recovery harness predicted it
   out-of-sample (70.6% -> heldout 63.6%). **The heldout one-shot is SPENT — do not re-run
   or tune against it.** **Step 4 operating-point selection now has its PRECISION side
   measured leakage-safe (2026-06-09, `build-cofactor-fusion-operating-point`):** on the
   out-of-sample calibration surface the recalibrated-abstention-threshold dial DOMINATES
   the sequence-supported suppression dial (threshold 0.44 keeps recall 30/35 and drops OOS
   FP to 8/26; suppression reaches 8/26 only by losing 7 in-scope primaries). Default to the
   recalibrated threshold and layer the complementary **Lever-2 electron-flow** OOS lift
   (+0.04 abstain at primary retention 1.0, different surface). What remains is selecting a
   *deployable* point — a separately authorized decision (thin 26-row cal OOS set, partial
   coordinate coverage), decided on a leakage-safe OOS surface, NOT by peeking at the spent
   one-shot. NOTE: LOMO already ran as a NEGATIVE baseline that motivates targeted
   expansion (do NOT rerun it); just preserve the frozen pre-expansion snapshot/tag (see
   "Expansion And Generalization Constraints" below). Default deploy path is the feature-channel
   (A); structure-restoration with a CANONICAL/template cofactor (B) is held in
   reserve. The experimental-cofactor atom-level graft is demoted to an optional
   oracle (sharpen the ceiling integer / one-time-validate the cheap proxy); it is
   NOT on the critical path and needs numpy (absent here) or a pure superposition.
   The ESMFold2 coordinate-swap experiment stays
   staged as a no-fit contract
   (`artifacts/v3_esmfold2_predicted_geometry_robustness_experiment_contract_current702_20260603.json`)
   with a runnable `esmfold2` backend, but is now scoped to its secondary value
   only: OOS false-positive reduction and pLDDT-gated abstention. To run it in an
   env with ESMFold2 access + `foldseek`: predict the 323 accessions, stage as
   mmCIF keyed by accession, run `build-predicted-geometry-robustness-audit`,
   `build-predicted-geometry-in-distribution-atlas-retrieval`, and
   `build-predicted-geometry-distillation-audit` with `--backend esmfold2
   --esmfold2-staged-dir <DIR>`, then re-run
   `build-predicted-geometry-failure-decomposition` on the ESMFold2 audit to
   confirm the pattern. Thresholds on train/cal; heldout once.
1. Targeted expansion factory/conversion screen (active expansion track): use
   `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json` as
   the source batch and
   `artifacts/v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json`
   as the conversion-screen result. The exact next action is human review of
   the conversion result, especially the single
   `countable_candidate_preflight_only` row and the 50 family-decision blockers.
   Do not start a larger promotion/import batch until Vivek or the main thread
   explicitly asks after reviewing this result.
2. Use the fold-augmented research gate with the disclosed 71/76 train/cal
   OOS-negative surface when running downstream diagnostics; clear the remaining
   five source-geometry/coordinate/sidecar blockers before any stronger
   threshold or production-like claim.
3. For family-panel review, the six non-abstained fold-augmented rows are
   source-checked and remain review-only. `m_csa:973` reuses its frozen
   train/calibration fold score, is score-complete, and abstains under the fixed
   research threshold. The 10-row source-backed coordinate/Foldseek pass is
   done, and five approved locator rows now have source-free predicted-geometry
   inputs visible to the source-free surface. `mh_067`/`mh_068` passed the
   split-safe check, were approved/copied into the audited locator directory,
   and are source-checked as review-only/no-promotion. The import-preview gate
   still reports 0/22 import-ready rows: `mh_065`/`mh_072` are explicitly left
   blocked until matching coordinates or a residue-code-resolving expert remap
   exist; the remaining open priority locator decisions are
   `external_glycoside_panel` (ligand-specificity validator or substrate
   coordinate), `mh_064` (alternate-coordinate fetch policy), and Q59490 /
   `secondary_probe::cobalamin_radical_rearrangement` (nonlabel locator
   strategy or alternate source). No label/import/family promotion is
   authorized.
4. If representation work resumes, produce row-aligned local sidecars first,
   start from
   `artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`,
   then
   `artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`.
   The row-specific train/cal feature rerun is now complete through the
   calibration-only pair contract. Next choose the deployable application path:
   preferred path is filling
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_current702_20260602.json`
   after approved current702 heldout locator sidecars exist; fallback path is
   explicitly accepting the lower-recall His-count-only contract in
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_current702_20260602.json`.
   The current approval packet
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_current702_20260603.json`
   normalizes the 55 priority-1 locator rewrites into pending approve/reject
   records with candidate and planned-payload hashes; it records 49 clean rows,
   6 warning rows, and 0 approvals.
   The current locator rewrite materialization gate
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_current702_20260603.json`
   is fail-closed: 55 preflight-passed rows have 0 explicit approvals and 0
   copied locator sidecars, so preflight alone is not enough to build the
   heldout application surface.
   The composed pre-threshold readiness gate
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_current702_20260603.json`
   keeps the frozen residual threshold unapplied until approved locators,
   event-axis linkers, and the heldout-safe source-free application surface all
   exist.
   In both cases, do not apply any frozen residual threshold or read heldout
   until the chosen source-free application surface is complete and guardrail
   audited.
5. For FMO, revise the review/silver evidence gate into subtype panels, finish
   coordinate/materialization blockers, and keep candidate rows review-only.
6. For label growth, require explicit expert decision, no-import safety checks
   where applicable, label-factory gate pass, batch acceptance, and registry
   summary refresh before any countable import. The current scale-out merged
   acceptance surface is review/control input only; it preserves shard signal
   and repair overlays but does not authorize label import or registry
   mutation.
7. **STAGE 1 COMPLETE (2026-06-10/11) — Stage 2 + held-pool triage are next.** All
   eight fingerprints are at/above the 100-floor; the governor's hole list is empty
   (`holes: []`); fingerprint Gini 0.51→0.1917; combined 2412→3042 (frozen 702 untouched).
   Sourced via `scripts/stage1_source_holes.py --apply` (the five cofactor-defined
   fingerprints) and `scripts/source_ser_his_hole.py --apply` (the cofactorless ser_his
   triad route): `radical_sam_enzyme` 10→133, `cobalamin_radical_rearrangement` 10→144,
   `flavin_monooxygenase` 43→116, `heme_peroxidase_oxidase` 69→119,
   `flavin_dehydrogenase_reductase` 87→250, `ser_his_acid_hydrolase` 42→129. The
   **remaining** work: (a) **Stage 2 — the real 10k lever:** 8 fingerprints × 250 cap ≈
   2,000 positives max, so 10k requires expanding the family set; the lone over-cap
   `metal_dependent_hydrolase` (308) is the on-ramp (split the coarse
   proteases/nucleases/phosphatases/deaminases bucket into v2 sub-families: fingerprint
   spec + ontology node + disambiguation rule + missing-context type, then source); and
   (b) triage the existing held pools the 2026-06-09 pending-candidate inventory describes
   (~730 disambiguation-held + 275 review-ready) through the governor/novelty gate.
   Decision-log entries 2026-06-11 "ser_his Hole CLOSED", "Stage-1 Under-Floor Closure",
   2026-06-10 "Stage-1 Hole Sourcing … Closed To Floor".

## Maintenance Notes

- Keep this file short enough to scan. Put detailed historical reasoning in the
  decision log or the specific artifact report.
- Refresh this file only when the current gate, trusted result set, blockers, or
  source-of-truth order changes.
- If a run only validates existing outputs, update automation memory rather than
  inflating this file.

## Primary References

2026-06-08 targeted expansion factory:

- `src/catalytic_earth/targeted_expansion_factory.py`
- `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json`
- `work/targeted_expansion_factory_batch_current702_20260608.md`
- `src/catalytic_earth/targeted_expansion_acquisition_conversion.py`
- `artifacts/v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json`
- `work/targeted_expansion_acquisition_conversion_screens_current702_20260608.md`
- `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`
- `work/scaleout_merged_acceptance_surface_current702_20260608.md`
- `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`
- `work/scaleout_locator_coordinate_repair_current702_20260608.md`

2026-06-06 session (cofactor recovery, electron-flow, consolidation):

- `src/catalytic_earth/cofactor_presence_calibration.py` + `artifacts/v3_cofactor_presence_calibration_current702_20260604.json`
- `src/catalytic_earth/predicted_geometry_recovery.py` + `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json`
- `artifacts/v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json`
- `artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json`
- `artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json`
- `artifacts/v3_cofactor_graft_fidelity_probe_current702_20260604.json`
- `artifacts/v3_esmfold2_predicted_geometry_robustness_experiment_contract_current702_20260603.json`
- `src/catalytic_earth/lever2_mechanism_incremental_readout.py` + `artifacts/v3_lever2_source_free_electron_flow_current_split_operating_point_readout_current702_20260606.json`
- `docs/predicted_geometry_robustness_pipeline_runbook.md`, `docs/MAP.md`, `docs/session_decision_record_20260606.md`

Earlier primary references:

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `artifacts/v3_predicted_structure_fold_channel_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_channel_coordinate_provenance_audit_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.json`
- `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json`
- `artifacts/v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json`
- `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json`
- `artifacts/v3_fold_augmented_confounded_deployment_closure_audit_current702_20260601.json`
- `artifacts/v3_fold_augmented_source_feature_active_site_sidecar_review_gate_current702_20260602.json`
- `artifacts/v3_fold_augmented_p23007_alternate_accession_policy_gate_current702_20260602.json`
- `artifacts/v3_fold_augmented_non_residue_interaction_sidecar_policy_preflight_current702_20260602.json`
- `artifacts/v3_fold_augmented_p10746_source_feature_refresh_audit_current702_20260603.json`
- `artifacts/v3_fold_augmented_blocker_human_decision_application_current702_20260603.json`
- `artifacts/v3_fold_augmented_approved_source_feature_active_site_sidecar_materialization_current702_20260603.json`
- `artifacts/v3_fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current702_20260603.json`
- `artifacts/v3_fold_augmented_fixed_threshold_rerun_readiness_current702_20260603.json`
- `artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_readout_current702_20260603.json`
- `artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current702_20260603.json`
- `artifacts/v3_fold_augmented_expanded_train_cal_oos_negative_surface_scores_current702_20260603.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.json`
- `artifacts/v3_fold_augmented_post_rerun_deployment_closure_status_current702_20260603.json`
- `artifacts/v3_fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.json`
- `artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_packet_current702_20260603.json`
- `artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_application_current702_20260603.json`
- `artifacts/v3_fold_augmented_post_decision_deployment_closure_status_current702_20260603.json`
- `artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_current702_20260603.json`
- `artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scoring_input_manifest_current702_20260603.json`
- `artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current702_20260603.json`
- `artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_extended_train_cal_oos_surface_current702_20260603.json`
- `artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_current702_20260603.json`
- `artifacts/v3_active_lever_mechanical_actionability_audit_current702_20260603.json`
- `artifacts/v3_esmfold2_predicted_geometry_robustness_experiment_contract_current702_20260603.json`
- `artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json`
- `artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json`
- `artifacts/v3_cofactor_graft_fidelity_probe_current702_20260604.json`
- `artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_schema_current702_20260601.json`
- `artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json`
- `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_feature_contract_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`
- `artifacts/v3_mechanism_feature_residual_robustness_current702_20260601.json`
- `artifacts/v3_mechanism_residual_gate_integration_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_feature_contract_gap_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.tsv`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_calibration_review_packet_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_research_readout_current702_20260601.json`
- `artifacts/v3_family_panel_high_value_glycyl_radical_readiness_packet_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa267_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa131_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa750_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa551_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa132_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa116_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json`
- `artifacts/v3_family_panel_source_backed_sidecar_materialization_plan_current702_20260601.json`
- `artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_retrieval_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_completion_reconciliation_current702_20260602.json`
- `artifacts/v3_fold_augmented_family_panel_countability_gate_preflight_current702_20260602.json`
- `artifacts/v3_fold_augmented_family_panel_import_preview_blocker_gate_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_mh065_mh072_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_glycoside_substrate_coordinate_scout_external_glycoside_panel_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_q59490_alternate_source_cache_scout_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_q59490_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_mh064_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_policy_closure_status_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_human_decision_matrix_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_schema_audit_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_template_bundle_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_review_queue_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.json`
- `artifacts/v3_fmo_subtype_hard_negative_packet_current702_20260601.json`
- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
