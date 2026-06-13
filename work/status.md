# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Current Automation Run

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T15:10:09Z`
- Started local: `Sat Jun 13 10:10:09 CDT 2026`
- Focus/result: applied the previous handoff's `manganese_iron_superoxide_dismutase` 10k-path lane
  through the full 34fp mechanism-first pipeline, then ran a bounded top-up over the remaining
  reviewed source window. Growth went only to `data/registries/external_bronze_labels.json`;
  frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Registry/counts: external bronze **6238 -> 6404** (+166); combined label surface
  **6940 -> 7106**; `manganese_iron_superoxide_dismutase` **0 -> 166** under cap 250 and above
  floor. Honest counters remain separate: `positive_bronze=5393`, `oos_bronze=1696`,
  `silver_ready=0`, `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k
  **4607**. External-only registry split is **5180** seed-fingerprint bronze and **1224** OOS
  bronze.
- Artifacts: `artifacts/v3_external_hard_negative_next_tranche_preregistration_34fp_1025.json`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_sourcing_preview_current702_20260613.json`,
  `work/manganese_iron_superoxide_dismutase_sourcing_current702_20260613.md`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_topup_sourcing_preview_current702_20260613.json`,
  `work/manganese_iron_superoxide_dismutase_topup_sourcing_current702_20260613.md`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_row_guardrail_audit_current702_20260613.json`,
  `work/manganese_iron_superoxide_dismutase_row_guardrail_audit_current702_20260613.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.json`,
  `work/coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.md`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.json`, and
  `work/novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.md`.
- Guardrails: row audit found **0** problems across **166** SOD rows; all rows have active-site/
  residue-role, cofactor/cosubstrate, and Rhea mechanism axes; EC/name/Rhea/keyword/prose/feature
  handles remain excluded-context admission evidence only; EC is never counted;
  `predictive_evidence []`; boundary SOD/heme/peroxidase/superoxide-reductase/side-EC/multi-signal
  rows were held.
- Validation: focused pytest passed (**301 passed, 14 subtests passed**); `PYTHONPATH=src python -m
  catalytic_earth.cli validate` passed (12 source records, 34 fingerprints, 31 ontology families,
  702 curated labels); JSON parse checks and `git diff --check` passed.
- Next exact action: do not repeat the SOD first-window/top-up previews. Build a genuinely new
  strict source/corroborator path for PfkB **46/100** or biotin **84/100**, or scout/spec the next
  clean fingerprint family through the same gated pipeline.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T14:53:41Z`
- Started local: `Sat Jun 13 09:53:41 CDT 2026`
- Focus/result: no registry write. Continued after user feedback instead of stopping at the bounded
  no-yield previews. Wrote a PfkB/biotin alternate-source scout, then cleared the old
  Mn/Fe-superoxide-dismutase source-poor blocker with a corrected guarded UniProt query and
  row-level mechanism scout. The SOD scout found **252** reviewed guarded rows and an 80-row sample
  with **77** registry-new likely-wireable rows, then wrote a deliberate `label_factory_v1_34fp`
  next-lane spec. Counts remain external bronze **6238**, combined surface **6940**, frozen
  current702 sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- New artifacts: `artifacts/v3_pfkb_biotin_alternate_source_scout_current702_20260613.json`,
  `work/pfkb_biotin_alternate_source_scout_current702_20260613.md`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.json`,
  `work/manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.md`,
  `artifacts/v3_manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.json`, and
  `work/manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.md`.
- Next exact action: wire `manganese_iron_superoxide_dismutase` only through the full 34fp
  fingerprint/ontology/OOS-prereg/tests/non-destructive-preview/apply pipeline with Cu/Zn,
  heme/cytoglobin/peroxidase, superoxide-reductase, side-EC, EC-only, and multi-signal guards.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T14:32:54Z`
- Started local: `Sat Jun 13 09:32:54 CDT 2026`
- Focus/result: cleared the prior live-fetch blocker for bounded previews, but no registry write.
  The runners completed and wrote preview artifacts at small `--max-records-per-lane` values:
  isomerase 5/20, CoA 20, non-heme 2OG 20, molybdopterin 20, zinc 20, copper 20. All yielded
  **0 novelty-admitted labels**, so no `--apply` was justified.
- New artifacts: `artifacts/v3_under_cap_bounded_preview_no_yield_current702_20260613.json` and
  `work/under_cap_bounded_preview_no_yield_current702_20260613.md`, plus the per-lane bounded
  preview/report files listed there.
- Registry/counts unchanged: external bronze **6238**, combined label surface **6940**, frozen
  current702 **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: `positive_bronze=5227`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k **4773**.
- Validation: focused pytest passed (**262 passed, 14 subtests passed**); `validate` passed;
  JSON/JSONL parse passed; `git diff --check` passed.
- Next exact action: do not repeat the same bounded first-window probes. Build a genuinely new
  PfkB/biotin source path with stronger mechanism corroboration, run a deeper under-cap extension
  only with enough closeout time, or start a new-family mechanism/source-supply scout/spec.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T14:08:42Z`
- Started local: `Sat Jun 13 09:08:42 CDT 2026`
- Focus/result: no registry write. The run selected an under-cap approved extension path because
  PfkB (46/100) and biotin (84/100) remain under-floor but their current strict reviewed source
  paths are documented exhausted. CoA extension previews at 500 and 280 rows/lane, then a smaller
  cofactor-independent isomerase cap-fill preview at 120 rows/lane, did not return bounded preview
  artifacts quickly enough for a safe inspect/apply/validate cycle. Blocker artifacts:
  `artifacts/v3_under_cap_extension_live_fetch_blocker_current702_20260613.json` and
  `work/under_cap_extension_live_fetch_blocker_current702_20260613.md`.
- Registry/counts unchanged: external bronze **6238**, combined label surface **6940**, frozen
  current702 **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: `positive_bronze=5227`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k **4773**.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed; JSON/JSONL parse
  passed; `git diff --check` passed. No focused pytest was run because there were no code or
  registry writes.
- Next exact action: retry the smallest cap-fill first:
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`;
  inspect `floor_projection`, `novelty_gate`, held@cap, trust-tier, and leakage fields before any
  `--apply`.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T12:33:42Z`
- Started local: `Sat Jun 13 07:33:42 CDT 2026`
- Focus/result: current handoff left PfkB and biotin as under-floor but source-limited, so this
  run used the existing mechanism-first modules to extend two already approved, non-confusable
  10k-path families with remaining reviewed supply: `cytochrome_p450_monooxygenase` and
  `copper_oxidoreductase`. Growth went only to `data/registries/external_bronze_labels.json`;
  frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- P450 extension command:
  `PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json --report work/cytochrome_p450_extension_sourcing_current702_20260613.md`.
  Result: fetched 337, mechanism-corroborated 189, novelty-admitted/applied 138,
  no-corroboration holds 35, duplicate/current-registry skips 113, novelty-throttled 51,
  held@cap 0; P450 **110 -> 248** under cap 250.
- Copper extension command:
  `PYTHONPATH=src python scripts/source_copper_oxidoreductase_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json --report work/copper_oxidoreductase_extension_sourcing_current702_20260613.md`.
  Result: fetched 222, mechanism-corroborated 81, novelty-admitted/applied 21,
  no-corroboration holds 20, duplicate/current-registry skips 121, novelty-throttled 60,
  held@cap 0; copper **119 -> 140**.
- Registry/counts: external bronze **6079 -> 6238** (+159); combined label surface
  **6781 -> 6940**. Honest counters remain separate: `positive_bronze=5227`,
  `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`; remaining
  positive-bronze gap to 10k is **4773**. External-only registry split is 5014
  seed-fingerprint bronze and 1224 OOS bronze.
- Guardrails: EC/Rhea/name/keyword/prose/feature handles are admission/excluded-context evidence
  only; EC is never counted; `predictive_evidence []`; all added rows are tier bronze /
  automation_curated / `uniprot:*`; dedup/novelty/governor/trust-tier gates ran against frozen
  current702 and existing external bronze; non-confusable per-fingerprint cap 250 was enforced.
  Row audits found 0 problems across 138 P450 rows and 21 copper rows.
- Post-apply audits: `artifacts/v3_coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.md`
  report **6940** combined, **33** fingerprints, fingerprint Gini **0.1633**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **70**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_p450_copper_extensions_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_p450_copper_extensions_applied.md`
  reports **6238** expansion rows, decisions `{'admit': 5782, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0731).
- Validation: focused suite passed
  (`PYTHONPATH=src pytest tests/test_cytochrome_p450_sourcing.py tests/test_copper_oxidoreductase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  -> **304 passed, 14 subtests passed**); `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 33 mechanism fingerprints, 30 ontology families, 702 curated labels);
  JSON/JSONL parse checks passed.
- Next exact action: do not add more P450 (248/250) unless a new reaction/organism gain is
  explicitly justified. Remaining floor work is still PfkB 54 rows and biotin 16 rows, but both
  current reviewed lanes are exhausted under the strict gates; next safest productive work is a
  genuinely new PfkB/biotin source path, or a new fingerprint-family scout/spec if source evidence
  is cleaner than further balanced-lane top-ups.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T11:33:25Z`
- Started local: `Sat Jun 13 06:33:26 CDT 2026`
- Focus/result: strict `pfkb_ribokinase_family` 33fp continuation from the latest handoff and
  scaling docs. Applied a guarded PfkB/ribokinase-family lane through the mechanism-first pipeline
  after tightening the boundary guard so generic `fructokinase` text cannot shadow PfkA. Broad
  EC 2.7 remains blocked and EC must stay scope-only.
- Family/gate setup: added `pfkb_ribokinase_family` fingerprint and mapped it to ontology family
  `pfkb`; bumped `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_33fp`;
  re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`. Counted
  mechanism handles are ATP/ADP phosphoryl-transfer Rhea participant text with PfkB/ribokinase
  substrates, PfkB-family/domain text, ATP/Mg/substrate active-/binding-site evidence,
  cofactor/cosubstrate handles, and structure-compatible evidence. Protein kinase, histidine kinase,
  hydrolase/nuclease, NDK, dNK, ASKHA, GHMP, PfkA, side-EC, and multi-fingerprint rows are held.
- Apply command:
  `PYTHONPATH=src python scripts/source_pfkb_ribokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched 88, mechanism-corroborated 46, applied 46, disambiguation holds 36,
  disambiguation skips 2, off-target held 4 as `askha_sugar_acetate_kinase`, novelty-throttled/
  rejected 0, held@cap 0, duplicate skipped 0; `pfkb_ribokinase_family` **0 -> 46** and remains
  under the 100 floor by 54.
- Registry/counts: external bronze **6033 -> 6079** (+46); combined label surface
  **6735 -> 6781**; frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate per `source_trust_tiers`: `positive_bronze=5085`, `oos_bronze=1696`,
  `silver_ready=0`, `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k is
  **4915**. External-only registry split is 4855 seed-fingerprint bronze and 1224 OOS bronze.
- Guardrails: EC/Rhea/name/keyword/prose/feature handles are admission/excluded-context evidence
  only; EC is never counted; `predictive_evidence []`; every added row is tier bronze /
  automation_curated / `uniprot:*`; dedup/novelty/governor/trust-tier gates ran against frozen
  current702 and existing external bronze; chemistry-confusable cap 150 was enforced. Row guardrail
  audit `artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json` found
  0 problems across 46 PfkB rows and all four mechanism axes present on every row.
- Post-apply audits: `artifacts/v3_coverage_redundancy_audit_current702_20260613_pfkb_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_pfkb_applied.md` report **6781** combined,
  **33** fingerprints, seed positives **5085**, fingerprint Gini **0.162**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **70**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfkb_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_pfkb_applied.md` reports **6079**
  expansion rows, decisions `{'admit': 5623, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.075).
- Floor-extension scout: `artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json`
  / `work/pfkb_ribokinase_family_floor_extension_scout_current702_20260613.md` reran the strict
  reviewed PfkB lane after apply with `--max-records-per-lane 500`; fetched 88 again, found
  **0** new PfkB labels, skipped 48 already-covered rows, held 36 no-corroboration rows, held 4
  off-target ASKHA rows, and left PfkB **46/100**.
- Validation: focused suite passed
  (`PYTHONPATH=src pytest tests/test_pfkb_ribokinase_family_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  -> **294 passed, 14 subtests passed**); `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 33 mechanism fingerprints, 30 ontology families, 702 curated labels);
  JSON/JSONL parse checks and `git diff --check` passed.
- Next exact action: close remaining under-floor positives without broad EC wiring. The reviewed
  strict PfkB lane is exhausted under the current gate, so either return to the biotin 16-row floor
  deficit, design a genuinely new PfkB source/handle path with stronger corroboration, or choose a
  new non-kinase 10k-path family through the same fingerprint/ontology/preregistration/preview/apply
  gates.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T10:31:51Z`
- Started local: `Sat Jun 13 05:31:51 CDT 2026`
- Focus/result: strict `pfka_phosphofructokinase` 32fp continuation from the latest handoff and
  scaling docs. Applied the gated PfkA lane through the existing mechanism-first pipeline, then wrote
  a non-importing PfkB/ribokinase-family next-lane scaffold because the prior scout showed lower
  source quality. Broad EC 2.7 remains blocked and EC must stay scope-only.
- Family/gate setup: added `pfka_phosphofructokinase` fingerprint and mapped it to ontology family
  `pfka`; bumped `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_32fp`;
  re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`. Counted
  mechanism handles are ATP/ADP phosphoryl-transfer Rhea participant text with
  fructose-6-phosphate, PfkA/ATP-dependent 6-phosphofructokinase family text, ATP/Mg/substrate
  active-/binding-site evidence, cofactor/cosubstrate handles, and structure-compatible evidence.
  Protein kinase, histidine kinase, hydrolase/nuclease, NDK, dNK, ASKHA, GHMP, PfkB/ribokinase, and
  multi-fingerprint rows are held.
- Apply command:
  `PYTHONPATH=src python scripts/source_pfka_phosphofructokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched 240, mechanism-corroborated 233, applied 150, disambiguation holds 5,
  disambiguation skips 2, off-target held 0, novelty-throttled/rejected 0, held@cap 83, duplicate
  skipped 0; `pfka_phosphofructokinase` **0 -> 150**.
- Registry/counts: external bronze **5883 -> 6033** (+150); combined label surface
  **6585 -> 6735**; frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: `positive_bronze=5039`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k is **4961**.
- Guardrails: EC/Rhea/name/keyword/prose/feature handles are admission/excluded-context evidence
  only; EC is never counted; `predictive_evidence []`; every added row is tier bronze /
  automation_curated / `uniprot:*`; dedup/novelty/governor/trust-tier gates ran against frozen
  current702 and existing external bronze; chemistry-confusable cap 150 was enforced. Row guardrail
  audit `artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json` found
  0 problems across 150 PfkA rows and all four mechanism axes present on every row.
- Post-apply audits: `artifacts/v3_coverage_redundancy_audit_current702_20260613_pfka_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_pfka_applied.md` report **6735** combined,
  **32** fingerprints, seed positives **5039**, fingerprint Gini **0.1465**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`,
  next-batch floor deficit **16**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfka_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_pfka_applied.md` reports **6033**
  expansion rows, decisions `{'admit': 5577, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0756).
- Validation so far: focused suite passed
  (`PYTHONPATH=src pytest tests/test_pfka_phosphofructokinase_sourcing.py tests/test_deoxynucleoside_kinase_sourcing.py tests/test_nucleoside_diphosphate_kinase_sourcing.py tests/test_askha_sugar_acetate_kinase_sourcing.py tests/test_ghmp_small_molecule_kinase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  -> **312 passed, 14 subtests passed**); `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 32 mechanism fingerprints, 30 ontology families, 702 curated labels).
- Small durable continuation: wrote
  `work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md`, with 0 labels and no
  registry writes. PfkB reviewed supply **85**, sampled **28/40** likely wireable, **0/40** boundary
  signals, and active-/binding-site context **28/40**. Next exact action: tighten/re-scout PfkB
  before any 33fp pipeline, or choose a stronger current scaling-plan family if evidence is cleaner;
  do not broad-wire EC 2.7.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T09:31:37Z`
- Started local: `Sat Jun 13 04:31:37 CDT 2026`
- Focus/result: strict `deoxynucleoside_kinase` 31fp continuation from the latest handoff and
  scaling docs. Applied the gated dNK lane through the existing mechanism-first pipeline, then ran a
  non-destructive PfkA/PfkB source-supply scout as a small durable continuation. Broad EC 2.7 remains
  blocked and EC must stay scope-only.
- Family/gate setup: added `deoxynucleoside_kinase` fingerprint and mapped it to ontology family
  `dnk`; bumped `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_31fp`; re-froze
  OOS preregistration as `artifacts/v3_external_hard_negative_next_tranche_preregistration_31fp_1025.json`.
  Counted mechanism handles are ATP/ADP phosphoryl-transfer Rhea participant text with
  deoxynucleoside substrates, dNK/thymidine/deoxycytidine/deoxyguanosine kinase family text,
  ATP/substrate active-/binding-site evidence, cofactor/cosubstrate handles, and structure-compatible
  evidence. Protein kinase, histidine kinase, hydrolase/nuclease, NDK, ASKHA, GHMP, Pfk, and
  multi-fingerprint rows are held.
- Apply command:
  `PYTHONPATH=src python scripts/source_deoxynucleoside_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched 240, mechanism-corroborated 237, applied 150, disambiguation holds 0,
  off-target held 0, novelty-throttled/rejected 0, held@cap 87, duplicate skipped 0;
  `deoxynucleoside_kinase` **0 -> 150**.
- Registry/counts: external bronze **5733 -> 5883** (+150); combined label surface
  **6435 -> 6585**; frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: `positive_bronze=4889`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k is **5111**.
- Guardrails: EC/Rhea/name/keyword/prose/feature handles are admission/excluded-context evidence
  only; EC is never counted; `predictive_evidence []`; every added row is tier bronze /
  automation_curated / `uniprot:*`; dedup/novelty/governor/trust-tier gates ran against frozen
  current702 and existing external bronze; chemistry-confusable cap 150 was enforced. Row guardrail
  audit `artifacts/v3_deoxynucleoside_kinase_row_guardrail_audit_current702_20260613.json` found
  0 problems across 150 dNK rows and all four mechanism axes present on every row.
- Post-apply audits: `artifacts/v3_coverage_redundancy_audit_current702_20260613_dnk_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_dnk_applied.md` report **6585** combined,
  **31** fingerprints, fingerprint Gini **0.1534**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, next-batch floor
  deficit **16**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_dnk_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_dnk_applied.md` reports **5883**
  expansion rows, decisions `{'admit': 5427, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0775).
- Validation: focused suite passed
  (`PYTHONPATH=src pytest tests/test_deoxynucleoside_kinase_sourcing.py tests/test_nucleoside_diphosphate_kinase_sourcing.py tests/test_askha_sugar_acetate_kinase_sourcing.py tests/test_ghmp_small_molecule_kinase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py`
  -> **293 passed**); `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (12 source
  records, 31 mechanism fingerprints, 30 ontology families, 702 curated labels); JSON/JSONL parse
  checks and `git diff --check` passed.
- Small durable continuation: wrote
  `artifacts/v3_strict_kinase_subclass_source_scout_after_dnk_current702_20260613.json` /
  `work/strict_kinase_subclass_source_scout_after_dnk_current702_20260613.md`, with 0 labels and no
  registry writes. PfkA reviewed supply **386**, sampled **40/40** likely wireable, **0/40** boundary
  signals; PfkB reviewed supply **85**, sampled **28/40** likely wireable, **0/40** boundary signals.
  Next exact action: full strict `pfka_phosphofructokinase` 32fp pipeline, not broad EC 2.7.
- Closeout budget check: at final ledger write, elapsed **31.1** minutes from `STARTED_AT`
  with **23.9** minutes remaining in the expected 55-minute work block. Decision:
  `closeout_after_dnk_apply_and_pfk_scout`; reason: dNK apply/audits/validation and PfkA/PfkB scout
  are complete, while full PfkA wiring/preregistration/preview/apply is too large to start safely
  while preserving docs/tests/push/lock-release closeout.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T08:29:42Z`
- Started local: `Sat Jun 13 03:29:42 CDT 2026`
- Focus/result: strict kinase-subclass continuation from the latest handoff. Applied two gated
  chemistry-confusable bronze lanes through the existing mechanism-first pipeline:
  `askha_sugar_acetate_kinase` (29fp) and `ghmp_small_molecule_kinase` (30fp). Growth went only to
  `data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- ASKHA setup/apply: added `askha_sugar_acetate_kinase` fingerprint + `askha` ontology node,
  bumped the universe to `label_factory_v1_29fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_29fp_1025.json`. Command:
  `PYTHONPATH=src python scripts/source_askha_sugar_acetate_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched 240, target mechanism-corroborated 227, applied 150, held 9
  no-corroboration rows, novelty-throttled 7, held@cap 70, duplicate skipped 0,
  `askha_sugar_acetate_kinase` 0 -> 150.
- GHMP setup/apply: added `ghmp_small_molecule_kinase` fingerprint + `ghmp` ontology node, bumped
  the universe to `label_factory_v1_30fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_30fp_1025.json`. Command:
  `PYTHONPATH=src python scripts/source_ghmp_small_molecule_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched 240, target mechanism-corroborated 228, applied 150, held 10
  no-corroboration rows, novelty-throttled 0, held@cap 78, duplicate skipped 0,
  `ghmp_small_molecule_kinase` 0 -> 150.
- Registry/counts: external bronze **5433 -> 5733** (+300); combined label surface
  **6135 -> 6435**. Honest counters remain separate: `positive_bronze=4739`,
  `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`; remaining
  positive-bronze gap to 10k is **5261**.
- Guardrails: EC 2.7.1 is scope-only and never counted. Counted corroboration came from ATP/ADP
  phosphoryl-transfer Rhea participant text, ASKHA/GHMP family text, active-/binding-site evidence,
  cofactor/cosubstrate handles, and structure-compatible handles. EC/name/keyword/Rhea/prose/
  feature handles remain `excluded_context`; `predictive_evidence []`; all rows are bronze /
  automation_curated / `uniprot:*`; dedup/novelty/governor/trust-tier gates ran against frozen
  current702 and existing external bronze; chemistry-confusable cap 150 was enforced for both lanes.
- Post-apply audits: `artifacts/v3_coverage_redundancy_audit_current702_20260613_ghmp_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_ghmp_applied.md` report **6435** combined,
  **30** fingerprints, fingerprint Gini **0.1534**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, next-batch floor
  deficit **16**. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_ghmp_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_ghmp_applied.md` reports **5733**
  expansion rows, decisions `{'admit': 5277, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0795).
- Validation: focused suite passed
  (`PYTHONPATH=src pytest tests/test_askha_sugar_acetate_kinase_sourcing.py tests/test_ghmp_small_molecule_kinase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py` -> **280 passed**);
  `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (12 source records,
  30 mechanism fingerprints, 30 ontology families, 702 curated labels); JSON/JSONL parse and
  `git diff --check` passed.
- Small durable continuation: wrote
  `work/deoxynucleoside_kinase_next_lane_spec_current702_20260613.md` with the next strict kinase
  split design. dNK reviewed supply from the prior scout is 278, sampled 39/40 likely wireable with
  1/40 boundary signal. Next exact action: full `deoxynucleoside_kinase` 31fp pipeline
  (fingerprint/ontology -> OOS prereg re-freeze -> disambiguation guards/tests -> preview -> gated
  apply), not broad EC 2.7.
- Closeout budget check: at `2026-06-13T09:03:06Z`, elapsed **33.4** minutes from `STARTED_AT`
  with **21.6** minutes remaining in the expected 55-minute work block. Decision:
  `closeout_after_two_applies_and_small_durable_continuation`; reason: ASKHA and GHMP applies,
  post-apply audits, focused validation, and the dNK scaffold were complete, while the next safe
  action is a full 31fp dNK wiring/preregistration/preview/apply cycle too large to start safely
  while preserving required docs/tests/push/lock-release closeout.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T07:30:33Z`
- Started local: `Sat Jun 13 02:30:36 CDT 2026`
- Focus: biotin floor-closure scout/apply followed by the fallback narrow kinase-subclass lane from
  the latest handoff. Broad EC 2.7 kinase stayed blocked; strict `nucleoside_diphosphate_kinase`
  was split out as a guarded 28fp lane.
- Result: applied +3 corrected external bronze rows for `biotin_dependent_carboxylase` and +150
  rows for `nucleoside_diphosphate_kinase`; external bronze **5280 -> 5433**; combined surface
  **5982 -> 6135**; frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Family/gate setup: added optional Rhea-first biotin floor-closure lane; added
  `nucleoside_diphosphate_kinase` fingerprint + `phosphohistidine_ntp_transfer` ontology family
  (`label_factory_v1_28fp`); re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_28fp_1025.json`.
- Biotin floor-closure command:
  `PYTHONPATH=src python scripts/source_biotin_dependent_carboxylase_family.py --include-floor-closure-lanes --max-records-per-lane 500 --cap-ceiling 150 --out artifacts/v3_biotin_dependent_carboxylase_floor_closure_scout_current702_20260613.json --report work/biotin_dependent_carboxylase_floor_closure_scout_current702_20260613.md --apply`.
  Result: fetched 126, Rhea-first lane found 105 reviewed rows already inside the candidate universe,
  admitted/applied 3 new pyruvate-carboxylase subunit A rows, held 42 no-corroboration rows, skipped
  81 duplicates; `biotin_dependent_carboxylase` **81 -> 84**, still under floor by 16.
- NDK apply command:
  `PYTHONPATH=src python scripts/source_nucleoside_diphosphate_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched 240, mechanism-corroborated 238, gate-admitted 237, novelty-throttled 1,
  held@cap 87, off-target held 0, duplicate skipped 0, applied 150; `nucleoside_diphosphate_kinase`
  **0 -> 150** (chemistry-confusable cap 150; floor reached).
- Guardrails: EC remains scope-only and never counted; Rhea/name/keyword/feature handles are
  admission/excluded-context only; `predictive_evidence []`; every added row is tier bronze /
  automation_curated / uniprot namespace; dedup ran against frozen current702 and external bronze;
  NDK side-EC guards hold protein kinases, two-component histidine kinases, hydrolase/nuclease rows,
  NMP kinases, and multi-fingerprint signals.
- Coverage audit: 6135 combined labels; 28 fingerprints; fingerprint Gini 0.1608; holes `[]`;
  under-floor `['biotin_dependent_carboxylase']`; over-cap `['metal_dependent_hydrolase']`;
  next-batch floor deficit 16. Novelty replay: 5433 expansion rows, decisions
  `{'admit': 4977, 'reject': 47, 'throttle': 409}`, would-not-readmit 456 (0.0839).
- Honest counters: `positive_bronze=4439`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap 5561.
- Validation: focused pytest `230 passed, 14 subtests passed`; `validate` passed (12 source records,
  28 mechanism fingerprints, 30 ontology families, 702 curated labels); row guardrail audits found
  0 problems across all 84 biotin and all 150 NDK rows; JSON/JSONL parse checks and
  `git diff --check` passed.
- Continuation scout after NDK:
  `artifacts/v3_strict_kinase_subclass_source_scout_after_ndk_current702_20260613.json` /
  `work/strict_kinase_subclass_source_scout_after_ndk_current702_20260613.md` sampled strict
  kinase splits without generating labels. Reviewed supply / likely wireable sample: deoxynucleoside
  kinase 278 / 39-of-40 with 1 boundary signal; GHMP small-molecule kinase 613 / 37-of-40 with 0
  boundary signals; ASKHA sugar/acetate kinase 667 / 39-of-40 with 0 boundary signals.
- Closeout budget check: after the NDK apply, validation, direct push, and the follow-on scout,
  elapsed time was about 45 minutes from `STARTED_AT`; with roughly 10 minutes left in the expected
  55-minute block, closeout started because the next safe step is full ASKHA wiring/29fp prereg/
  preview/apply, which is too large to begin safely in the remaining window.
- Follow-on: biotin remains below floor but reviewed Rhea-first source supply is exhausted under the
  current gate. Next highest-impact lane is strict `askha_sugar_acetate_kinase`; do not broad-wire
  EC 2.7, merge kinase subclasses, or count EC as mechanism evidence. Required next sequence:
  fingerprint/ontology spec -> 29fp OOS prereg re-freeze -> disambiguation guards/tests ->
  non-destructive preview -> gated apply only if novelty/governor/dedup/trust-tier gates pass.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T06:28:39Z`
- Started local: `Sat Jun 13 01:28:39 CDT 2026`
- Focus: guarded `biotin_dependent_carboxylase` 27fp setup/apply from the latest handoff after the
  zinc lyase/hydratase apply. Broad EC 2.7 kinase remains blocked by subclass mixing.
- Result: applied +81 corrected external bronze rows for `biotin_dependent_carboxylase`; external
  bronze 5199 -> 5280; combined surface 5901 -> 5982; frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Family/gate setup: added `biotin_dependent_carboxylase` fingerprint +
  `biotin_carboxyl_transfer` ontology family (`label_factory_v1_27fp`); re-froze OOS
  preregistration as `artifacts/v3_external_hard_negative_next_tranche_preregistration_27fp_1025.json`.
- Apply command:
  `PYTHONPATH=src python scripts/source_biotin_dependent_carboxylase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Corrected result after removing 12 EC 6.3.4.15 biotin-protein ligase boundary rows: fetched 126,
  mechanism-corroborated/admitted/applied 81, disambiguation holds 44, off-target held 0,
  novelty-throttled/rejected 0, held at cap 0, duplicate skipped 1.
- Guardrails: EC 6.4.1 / 6.3.4 scope-only and never counted; ATP + hydrogencarbonate/CO2/
  carboxybiotin chemistry is mandatory; `predictive_evidence []`; tier bronze /
  automation_curated / uniprot namespace; dedup vs both registries; multi-fingerprint-signal and
  biotin-protein ligase rows held; chemistry-confusable cap 150 enforced.
- Coverage audit: 5982 combined labels; 27 fingerprints; fingerprint Gini 0.1655; holes `[]`;
  under-floor `['biotin_dependent_carboxylase']`; over-cap `['metal_dependent_hydrolase']`;
  next-batch floor deficit 19. Novelty replay: 5280 expansion rows, decisions
  `{'admit': 4824, 'reject': 47, 'throttle': 409}`, would-not-readmit 456 (0.0864).
- Honest counters: `positive_bronze=4269`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap 5731.
- Validation: focused pytest `391 passed, 14 subtests passed`; `validate` passed (12 source records,
  27 mechanism fingerprints, 29 ontology families, 702 curated labels); JSON/JSONL parse checks and
  `git diff --check` passed.
- Follow-on: run a non-destructive biotin floor-closure source scout for the remaining 19 rows
  without relaxing the ATP/hydrogencarbonate/carboxybiotin chemistry requirement; if reviewed supply
  cannot safely close the deficit, return to a narrow kinase-subclass scout.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T05:53:52Z`
- Started local: `Sat Jun 13 00:53:52 CDT 2026`
- Focus: guarded `zinc_lyase_hydratase` 26fp wiring/apply from the latest handoff after the ThDP
  apply. Older P450/2OG/CoA/copper/ATP/class-II/ThDP lanes were already applied.
- Result: applied +113 external bronze rows for `zinc_lyase_hydratase`; external bronze
  5086 -> 5199; combined surface 5788 -> 5901; frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Family/gate setup: added `zinc_lyase_hydratase` fingerprint + `zinc_hydro_lyase` ontology family
  (`label_factory_v1_26fp`); re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_26fp_1025.json`.
- Apply command:
  `PYTHONPATH=src python scripts/source_zinc_lyase_hydratase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Fetched 240, mechanism-corroborated 116, admitted/applied 113, held 57 off-target rows
  (`nad_p_dehydrogenase` 47, `metallophosphomonoesterase` 6,
  `metallo_amidohydrolase_deaminase` 4), held 10 no-corroboration rows, novelty-throttled 3,
  duplicate skipped 0.
- Guardrails: EC 4.2.1 scope-only and never counted; zinc/Rhea/Lyase/hydratase/active-site handles
  are admission/excluded-context only; `predictive_evidence []`; tier bronze / automation_curated /
  uniprot namespace; dedup vs both registries; multi-fingerprint-signal/off-target rows held;
  chemistry-confusable cap 150 enforced.
- Coverage audit: 5901 combined labels; fingerprint Gini 0.1559; holes `[]`; over-cap
  `['metal_dependent_hydrolase']`; next-batch floor deficit 0. Novelty replay: 5199 expansion rows,
  decisions `{'admit': 4743, 'reject': 47, 'throttle': 409}`, would-not-readmit 456 (0.0877).
- Honest counters: `positive_bronze=4188`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap 5812.
- Follow-on: do not broad-wire EC 2.7 kinase; latest scout had 75/80 multi-subclass boundary rows
  and only 4 clean rows. Next useful action is a focused scout that either splits a narrow kinase
  subclass with clean non-EC handles or designs a guarded biotin-carboxylase handle around
  biotinyl-Lys/Rhea ATP-hydrogencarbonate/carboxybiotin evidence.
- Validation: focused pytest `387 passed, 14 subtests passed`; `validate` passed (12 source records,
  26 mechanism fingerprints, 28 ontology families, 702 curated labels); JSON parse checks and
  `git diff --check` passed during closeout.

## Previous Automation Snapshot

- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T03:58:23Z`
- Started local: `Fri Jun 12 22:58:23 CDT 2026`
- Focus: `atp_amide_ligase` from the latest handoff, then the post-ATP 10k-path lane selected by
  current evidence (`class_ii_metal_aldolase`). The older prompt's P450 direction was already
  complete in prior runs.
- Result: applied +150 external bronze rows for `atp_amide_ligase` and +150 for
  `class_ii_metal_aldolase`; external bronze 4636 -> 4936; combined surface 5338 -> 5638; frozen
  current702 sha stayed `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Family/gate setup: added `atp_amide_ligase` fingerprint (`label_factory_v1_23fp`) and
  `class_ii_metal_aldolase` fingerprint + `carbon_carbon_lyase` ontology family
  (`label_factory_v1_24fp`); re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_23fp_1025.json` and
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_24fp_1025.json`.
- Apply commands:
  `PYTHONPATH=src python scripts/source_atp_amide_ligase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`
  and
  `PYTHONPATH=src python scripts/source_class_ii_metal_aldolase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  ATP fetched 240, mechanism-corroborated 171, admitted/applied 150, held 8 off-target rows,
  duplicate skipped 0. Class-II fetched 240, mechanism-corroborated 182, admitted/applied 150, held
  7 off-target rows, duplicate skipped 0.
- Guardrails: EC scope-only and never counted; broadened handles are admission/excluded-context only;
  `predictive_evidence []`; tier bronze / automation_curated / uniprot namespace; dedup vs both
  registries; multi-fingerprint-signal/off-target rows held; chemistry-confusable cap 150 enforced
  for both new families.
- Coverage audit: 5638 combined labels; fingerprint Gini 0.1581; holes `[]`; over-cap
  `['metal_dependent_hydrolase']`; next-batch floor deficit 0. Novelty replay: 4936 expansion rows,
  decisions `{'admit': 4480, 'reject': 47, 'throttle': 409}`, would-not-readmit 456 (0.0924).
- Honest counters: `positive_bronze=3925`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap 6075.
- Follow-on: post-class-II source scout ranked `atp_phosphotransferase_kinase` first, but its
  mechanism scout found 75/80 multi-subclass boundary rows and only 4 likely clean rows. Do not
  broad-wire EC 2.7; split a narrow kinase subclass or use the next cleaner lane, with ThDP enzyme
  the best fallback candidate.
- Validation: focused pytest `156 passed`; leakage prereg/import-gate subset `14 passed, 171
  deselected`; import/transfer-scope tests `133 passed`; `validate` passed (12 source records, 24
  mechanism fingerprints, 26 ontology families, 702 curated labels); JSON/JSONL parse and
  `git diff --check` passed during closeout.

## Previous Automation Snapshot


- Automation ID: `ce-nad-glyco-floor-expansion`
- Started UTC: `2026-06-13T00:58:14Z`
- Started local: `Fri Jun 12 19:58:14 CDT 2026`
- Focus: CoA acyltransferase and cofactor-independent isomerase as the next 10k scaling lanes after
  the completed P450 and non-heme iron 2OG applies.
- Result: applied +188 external bronze rows for `coa_acyltransferase` and +142 for
  `cofactor_independent_isomerase`; external bronze 3872 -> 4202; combined surface 4574 -> 4904;
  frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Family/gate setup: added `coa_acyltransferase` fingerprint + `acyl_transfer` ontology node
  (`label_factory_v1_18fp`) and `cofactor_independent_isomerase` fingerprint + `isomerization`
  ontology node (`label_factory_v1_19fp`); re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_18fp_1025.json` and
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_19fp_1025.json`.
- Apply commands:
  `PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 80 --apply`
  and
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 80 --apply`.
  CoA fetched 218, mechanism-corroborated 204, admitted/applied 188, throttled 16, held 11
  no-corroboration rows, held 1 off-target match, held at cap 0, duplicate skipped 0. Isomerase
  fetched 266, mechanism-corroborated 147, admitted/applied 142, throttled 5, held 70
  no-corroboration rows, held 28 off-target NAD(P) matches, held at cap 0, duplicate skipped 0.
- Guardrails: EC scope-only and never counted; broadened handles are admission/excluded-context
  only; `predictive_evidence []`; tier bronze / automation_curated / uniprot namespace; dedup vs both
  registries; multi-fingerprint-signal/off-target rows held; cap 250 for CoA and chemistry-confusable
  cap 150 for isomerase enforced.
- Coverage audit: 4904 combined labels; fingerprint Gini 0.1613; holes `[]`; over-cap
  `['metal_dependent_hydrolase']`; next-batch floor deficit 0. Novelty replay: 4202 expansion rows,
  decisions `{'admit': 3746, 'reject': 47, 'throttle': 409}`, would-not-readmit 456 (0.1085).
- Honest counters: `positive_bronze=3191`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap 6809.
- Follow-on: non-destructive post-isomerase scout recommends `molybdopterin_oxidoreductase` next
  over `copper_oxidoreductase` (460 reviewed rows and 33 distinct full EC labels in 200 sampled
  rows vs 222/12). Both are reaction-poor, so the next runner should start with a mechanism-handle
  scout and boundary guard design before any preview/apply.
- Validation: targeted pytest `95 passed`, selected leakage prereg/import-gate pytest `8 passed`,
  selected transfer-scope pytest `1 passed`, and `validate` passed (12 source records, 19 mechanism
  fingerprints, 22 ontology families, 702 curated labels). JSON/JSONL parse and `git diff --check`
  passed during closeout.

## Time

- Entries: 408
- Measured elapsed time: 11681.4 minutes (194.69 hours)
- Estimated/planned time: 405 minutes (6.75 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- automation-lever-3: 23.5 measured minutes (0.39 hours)
- external-transfer-spof-hardening: 246.7 measured minutes (4.11 hours)
- infrastructure: 106.2 measured minutes (1.77 hours)
- leakage-risk closure: 11.8 measured minutes (0.20 hours)
- northstar-lever-2: 167.5 measured minutes (2.79 hours)
- northstar-lever-2-3: 55.6 measured minutes (0.93 hours)
- northstar-lever3: 1249.5 measured minutes (20.83 hours)
- ops: 130.6 measured minutes (2.18 hours)
- post-infra-science: 1804.7 measured minutes (30.08 hours)
- post-mcsa-spof-hardening: 1764.6 measured minutes (29.41 hours)
- post-v2: 3125.4 measured minutes (52.09 hours)
- sequence-nn-baseline: 46.8 measured minutes (0.78 hours)
- targeted-expansion: 213.5 measured minutes (3.56 hours)
- v3: 2734.9 measured minutes (45.58 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 180 estimated minutes (3.00 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 3947
- Evidence references logged: 3310

## Recent Entries

### 2026-06-08T05:12:17.067792+00:00 - v3

- Task: targeted expansion factory batch current702
- Time mode: measured
- Measured minutes: 50.833
- Started: 2026-06-08T04:21:01Z
- Ended: 2026-06-08T05:11:51Z
- Artifacts: artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json, work/targeted_expansion_factory_batch_current702_20260608.md
- Evidence: pytest 1703 passed, unittest 1658 passed, validate 702 labels, docs refs missing 0, row/source hash mismatches 0
- Commit: `pending_final_wrap_commit`
- Notes: Integrated over origin/main targeted factory; upgraded batch to 816 non-importing candidates across 8 axes with six architecture-default rows carried over.

### 2026-06-08T13:53:00.862088+00:00 - targeted-expansion

- Task: Acquisition-needed conversion screens for first targeted expansion batch
- Time mode: measured
- Measured minutes: 50.633
- Started: 2026-06-08T13:01:52Z
- Ended: 2026-06-08T13:52:30Z
- Artifacts: artifacts/v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json, work/targeted_expansion_acquisition_conversion_screens_current702_20260608.md
- Evidence: PYTHONPATH=src python -m pytest -q:1708 passed, PYTHONPATH=src python -m unittest discover -s tests:1663 tests OK, PYTHONPATH=src python -m catalytic_earth.cli validate:702 labels
- Notes: Routed 86 acquisition-needed rows: 27 reject/OOS, 7 locator blockers, 50 family-decision blockers, 1 review-only, 1 preflight-only.

### 2026-06-08T14:19:32.103369+00:00 - targeted-expansion

- Task: Acquisition conversion screen self-stop reconciliation
- Time mode: measured
- Measured minutes: 50.45
- Started: 2026-06-08T13:23:13Z
- Ended: 2026-06-08T14:13:40Z
- Artifacts: artifacts/v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json, work/targeted_expansion_acquisition_conversion_screens_current702_20260608.md, work/handoff.md, work/status.md
- Evidence: origin/main already contained durable 86-row conversion screen at fcee1b76, local duplicate conversion work stashed instead of pushed, focused canonical conversion tests passed, validate passed for 702 curated labels, JSON parse and git diff check passed, disk free 11049096 KiB
- Notes: Paused automation after detecting the pushed conversion screen; exact next action remains human review of the conversion report before any controlled promotion discussion.

### 2026-06-09T03:49:20.085384+00:00 - targeted-expansion

- Task: Targeted expansion defense ledger current702
- Time mode: measured
- Measured minutes: 21.117
- Started: 2026-06-09T03:36:09Z
- Ended: 2026-06-09T03:57:16Z
- Artifacts: artifacts/v3_targeted_expansion_defense_ledger_current702_20260609.json, work/targeted_expansion_defense_ledger_current702_20260609.md, work/handoff.md, work/status.md
- Evidence: ledger JSON parse passed, custom source path and count reconciliation passed including Wave 2, rebased over origin/main 4190c5a2, unittest discovery 1681 passed after rebase, validate passed with 702 curated labels, docs artifact reference check missing 0, git diff check passed, production edit guardrail scan clean, pushed ledger commit 91e13a31 and verified HEAD equals origin/main
- Commit: `91e13a3198a366759f7b73a22356a80fd22781e9`
- Notes: Built review-ready ledger tying current702 targeted scaleout choices to prior cofactor geometry fold locator near-orphan OOS and external Swiss-Prot AFDB Rhea lessons; external 333-row import-ready preview remains preview-only.

### 2026-06-09T03:50:15.392215+00:00 - targeted-expansion

- Task: External import-ready review preflight
- Time mode: measured
- Measured minutes: 15.483
- Started: 2026-06-09T03:34:46Z
- Ended: 2026-06-09T03:50:15Z
- Artifacts: artifacts/v3_external_import_review_preflight_current702_20260609.json, artifacts/v3_external_import_review_ready_preview_current702_20260609.json, artifacts/v3_external_import_review_repair_queue_current702_20260609.json, work/external_import_review_preflight_current702_20260609.md, work/handoff.md, work/status.md
- Evidence: 333 preview rows classified, 317 controlled-review ready rows, 15 external duplicate conflicts, 1 family policy review row, 0 current702 exact duplicate conflicts, 0 locator blockers, 0 coordinate blockers, 0 exact coordinate current702 overlaps, JSON parse and count reconciliation passed, focused tests passed, unittest discovery 1683 passed, validate passed with 702 labels, docs artifact-reference missing 0, git diff check passed
- Notes: Foldseek/TM structural duplicate screen was not recomputed because Foldseek is unavailable and disk free is about 1.4 GiB; exact coordinate/structure-id overlap screen was clean.

### 2026-06-09T05:25:43.402284+00:00 - targeted-expansion

- Task: External materialization Wave 2 current702 scaleout merge
- Time mode: measured
- Measured minutes: 14.75
- Started: 2026-06-09T05:10:41Z
- Ended: 2026-06-09T05:25:26Z
- Artifacts: artifacts/v3_external_materialization_wave2_current702_20260609.json, artifacts/v3_external_materialization_wave2_import_ready_preview_current702_20260609.json, artifacts/v3_external_materialization_wave2_repair_queue_current702_20260609.json, artifacts/external_materialization_wave2_source_free_locators_current702_20260609, work/external_materialization_wave2_current702_20260609.md, work/handoff.md, work/status.md
- Evidence: 5132 source surface rows consumed, 4795 unique candidates merged, 318 controlled import-ready preview rows, 4477 repair queue rows, 1970 new locator sidecars and 309 reused locator sidecars, 0 coordinate downloads because disk below 10 GiB, focused tests passed, unittest discovery 1690 passed, validate passed, docs artifact-reference missing 0, diff check and production edit guardrail passed
- Commit: `pending_final_wrap_commit`
- Notes: Consumed landed redox/cofactor and PLP/radical/cobalamin previews plus supplemental 20260608 scaleout shards; disk remained below floor so shard-preview rows with locators stay in coordinate continuation.

### 2026-06-09T05:54:43.128126+00:00 - targeted-expansion

- Task: Near-orphan diversity external scaleout shard current702
- Time mode: measured
- Measured minutes: 41.117
- Started: 2026-06-09T05:12:53Z
- Ended: 2026-06-09T05:54:00Z
- Artifacts: artifacts/v3_external_scaleout_shard_near_orphan_diversity_current702_20260609.json, artifacts/v3_external_scaleout_shard_near_orphan_diversity_import_ready_preview_current702_20260609.json, work/external_scaleout_shard_near_orphan_diversity_current702_20260609.md, work/handoff.md, work/status.md
- Evidence: 3022 candidate rows and 2821 unique non-duplicate rows, 142 import-ready preview rows and 7 provisional rows, 13 diversity bins with 637 near-orphan rows and 204 no-structure rows, 1306 OOS fold cofactor hard-negative rows, JSON parse count provenance and no-structure reconciliation passed, focused shard tests passed, unittest discovery 1691 passed, validate passed with 702 labels, docs artifact-reference missing 0, git diff check passed, production edit guardrail scan clean
- Commit: `pending_final_wrap_commit`
- Notes: Default 4500-cap live pass was stopped after about 16 minutes to preserve wrap budget; final lane-balanced pass used 220 records per lane with 24 workers and 5-second entry timeouts.

### 2026-06-09T13:24:24.360224+00:00 - targeted-expansion

- Task: External materialization Wave 2 current702 scaleout merge
- Time mode: measured
- Measured minutes: 19.983
- Started: 2026-06-09T13:03:15Z
- Ended: 2026-06-09T13:23:14Z
- Artifacts: artifacts/v3_external_materialization_wave2_current702_20260609.json, artifacts/v3_external_materialization_wave2_import_ready_preview_current702_20260609.json, artifacts/v3_external_materialization_wave2_repair_queue_current702_20260609.json, artifacts/external_materialization_wave2_source_free_locators_current702_20260609, artifacts/external_materialization_wave2_coordinates_current702_20260609, work/external_materialization_wave2_current702_20260609.md, work/handoff.md, work/status.md
- Evidence: 18235 source surface rows consumed, 12495 unique candidates merged, 600 import-ready preview rows, 248 Wave 2 coordinate files present, 5213 locator sidecars parsed, 11895 repair queue rows, focused tests passed, unittest discovery 1697 passed, validate passed, docs artifact-reference missing 0, diff check passed, production edit guardrail clean
- Notes: Consumed broad Wave 2 bulk metal/phosphoryl/glycoside near-orphan/diversity redox/cofactor and PLP/radical/cobalamin outputs; bounded coordinate materialization promoted 282 rows while preserving disk above 10 GiB.

## Expectation Updates

- 2026-05-09T13:40:20.355854+00:00: v0 completed in one active session, so the previous one-year v0-v2 timeline is too conservative and must be recalibrated from logged progress
- 2026-05-09T13:40:25.768544+00:00: Use observed artifact-per-hour rate to revise v1 and v2 estimates after each material chunk.
- 2026-05-09T13:54:30.954964+00:00: V1 completed much faster than the earlier days-to-weeks estimate because paginated M-CSA and UniProt TSV APIs were straightforward.
- 2026-05-09T13:54:31.022704+00:00: The completed V2 is a scaffold-level research artifact, not the final high-impact enzyme atlas; time estimates must distinguish scaffold completion from scientific validation.
- 2026-05-09T14:01:49.012481+00:00: Geometry extraction was implementable quickly for PDB-linked M-CSA entries; the harder next step is label quality and retrieval evaluation.
- 2026-05-09T14:03:45.516905+00:00: Next quality bottleneck is curated mechanism labels and evaluation, not baseline implementation.
- 2026-05-09T14:10:40.717863+00:00: The next bottleneck is improving ranking and abstention, not adding labels machinery.
- 2026-05-09T14:13:21.398170+00:00: Progress will now be measured per hourly block rather than per ad hoc milestone.
- 2026-05-09T14:18:10.779278+00:00: Continuity is now treated as a required output of each 55-minute work block.
- 2026-05-09T14:25:33.013901+00:00: The time overestimate came from confusing scaffold implementation with scientifically robust validation; current progress is fast but still small-label and artifact-scale.
- 2026-05-09T15:20:27.676203+00:00: Ligand/cofactor context integration from mmCIF was quick; next quality bottleneck shifts to substrate-pocket descriptors and larger curated labels.
- 2026-05-09T15:22:39.241656+00:00: README now states that scaffold work moved faster than first estimated; impact depends on scaling labels, harder benchmarks, expert review, and validation.
- 2026-05-09T15:30:17.008476+00:00: Substrate-pocket descriptors integrated quickly; next bottleneck is targeted failure analysis and label expansion rather than more feature plumbing.
- 2026-05-09T15:42:05.002091+00:00: Future runs should consume the full 55-minute wall-clock block by rolling into the next highest-value bounded task when assigned work finishes early.
- 2026-05-09T16:02:34.920556+00:00: Current out-of-scope errors are threshold-margin cases; next gain likely comes from abstention policy refinement and harder negatives.
- 2026-05-09T16:03:37.698226+00:00: Automation model selection is now treated as an operating invariant, not an implicit app default.
- 2026-05-09T16:14:49.435851+00:00: Automation runs now distinguish productive work time from wrap-up time; normal runs should spend at least 50 measured minutes advancing the project.
- 2026-05-09T17:07:37.625326+00:00: Next priority is hard-negative scorer separation and structure mapping repair, not more scaffold work
- 2026-05-09T18:08:06.495922+00:00: remaining bottleneck is separating two ligand-supported metal-like controls without losing retained positives
- 2026-05-09T19:35:11+00:00: The 100-entry slice is clean, but full 125-entry labeling exposes hard redox and metal-like controls; robustness now depends on hard-negative separation and seed-family splits.
- 2026-05-09T19:52:34.146667+00:00: The main 125-entry bottleneck is no longer hidden heme-absent overlap; remaining controls concentrate in metal-like and Ser-His-like groups.
- 2026-05-09T20:12:10.878697+00:00: End-of-run quality now includes documentation freshness, not only code artifacts and git cleanliness.
- 2026-05-09T21:11:49.565784+00:00: Hard-negative separation is clean through the 150-entry slice; next quality bottleneck is evidence-limited in-scope positives with missing local cofactor context.
- 2026-05-09T22:17:13.285127+00:00: The main 150-entry bottleneck is retained positives without selected-structure cofactor evidence, not hard-negative separation
- 2026-05-09T23:20:32.069816+00:00: The 175-entry bottleneck is now near-miss metal-hydrolase controls and fragile evidence-limited retained positives, not hard-negative separation.
- 2026-05-10T00:22:01.303388+00:00: The 225-entry bottleneck is now the selected-structure cofactor gap for m_csa:132 or the next label expansion, not hard-negative separation.
- 2026-05-10T01:18:40.670377+00:00: Next bottleneck is expanding beyond 275 labels or resolving m_csa:132 selected-structure cofactor absence.
- 2026-05-10T02:23:20.695520+00:00: The benchmark can expand in 25-entry curation tranches while preserving guardrails; the next bottleneck is 400-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T03:26:17.876722+00:00: The benchmark can continue expanding in curated 25-entry tranches, but the next bottleneck is 475-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T04:23:35.521223+00:00: The benchmark can keep expanding in 25-entry curation tranches; next bottleneck is 500-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T05:25:09.634817+00:00: Next bottleneck is importing decisions from the 500 queue through the label factory rather than expanding labels directly.
- 2026-05-10T06:26:21.995107+00:00: The active bottleneck is cobalamin local cofactor evidence for m_csa:494 and preserving countable/review-state separation.
- 2026-05-10T07:28:17.575433+00:00: The active bottleneck moved from the 500 cobalamin deferral to preserving review-state labels while opening a 575-entry tranche.
- 2026-05-10T08:36:59.402518+00:00: The active bottleneck is reviewing the accepted 625 preview before promoting it to canonical labels.
- 2026-05-10T13:59:54.901465+00:00: The active bottleneck is reviewing the accepted 675 preview before promoting it to canonical labels.
- 2026-05-10T14:37:36.208242+00:00: The active bottleneck is auditing the 24 new 675-preview review-debt rows before promotion.
- 2026-05-10T15:39:13.368774+00:00: The active bottleneck is deciding whether to promote m_csa:666 alone or resolve the 61 pending 675-preview review-state rows first.
- 2026-05-10T16:41:45.028412+00:00: Stop further tranche growth at 624 countable labels until 81 review-state rows are triaged or stronger evidence is added.
- 2026-05-10T17:43:34.382296+00:00: Count growth remains stopped at 624 countable labels until accepted-700 review debt has local evidence or explicit expert resolution.
- 2026-05-10T18:46:18.139775+00:00: Next bottleneck is auditing m_csa:577 m_csa:592 and m_csa:641 remap-local leads against counterevidence before any further gated scaling.
- 2026-05-10T19:48:49.955298+00:00: Next bottleneck is deciding whether kinase/phosphoryl-transfer mismatch rows need an ontology-family rule or expert reaction/substrate export before more count growth.
- 2026-05-10T20:50:01.204415+00:00: Next bottleneck shifts from detecting reaction/substrate mismatch lanes to reducing review-only debt without expert-authority count growth.
- 2026-05-10T22:51:19.534178+00:00: Next bottleneck is reducing expert-label decision review-only debt with evidence repair, not opening 725+ count growth.
- 2026-05-10T23:56:45.965586+00:00: Next run should reduce expert-label repair debt or harden local-evidence checks before opening any 725+ tranche.
- 2026-05-11T03:12:54.274263+00:00: Next bottleneck is resolving one local-evidence repair lane from the 21-row plan before count growth.
- 2026-05-12T15:04:26.275853+00:00: After prioritized scientific expansion is implemented and guardrail-clean, agents should resume factory-gated label expansion while preserving label quality and import-safety controls.
- 2026-05-12T16:42:24.970333+00:00: Keep ATP families as boundary evidence; stop scaling if next gate exposes quality drift.
- 2026-05-12T17:48:03.708741+00:00: Next run should repair or explicitly defer the accepted-725 review-debt surface before blind 750 scaling.
- 2026-05-12T18:52:33.655337+00:00: Next run should repair or explicitly defer the 18 new 750-preview review-debt rows before promoting seven clean candidates.
- 2026-05-12T20:14:45.382801+00:00: 750 review debt can be explicitly deferred without weakening countable-label gates; resume bounded scaling toward 1,000 labels.
- 2026-05-12T21:46:07.698000+00:00: Countable registry is 642 labels; the label factory remains below the 1000-label milestone and should continue bounded batches with quality repair on any gate failure.
- 2026-05-12T22:58:26.440004+00:00: Countable registry is 652 labels; next bounded work is an 875 preview while post-850 gate stays clean.
- 2026-05-13T00:50:52.831198+00:00: Countable registry is 673 labels; next bounded work is a 975 preview while post-950 gate stays clean.
- 2026-05-13T02:01:21.378176+00:00: Low-score local heme boundary rows now defer instead of becoming countable out-of-scope negatives.
- 2026-05-13T03:55:19.973294+00:00: The 1,025 preview is guardrail-clean but non-promotable; 10k progress now depends on external-source transfer rather than another M-CSA-only tranche.
- 2026-05-13T04:55:52.608228+00:00: Next bounded work should use the active-site evidence queue for external candidates while keeping all external rows non-countable.
- 2026-05-13T05:57:24.579339+00:00: External transfer remains review-only; repair active-site feature gaps and heuristic metal-hydrolase collapse before any label import.
- 2026-05-13T06:58:30.872167+00:00: External transfer remains non-countable; next bounded work should source active-site evidence for 10 gaps, disambiguate 3 broad-EC rows, and prototype representation controls for 12 mapped controls.
- 2026-05-13T12:55:17.737175+00:00: The next useful milestone is pilot import readiness for named external candidates, not a higher external-transfer gate count.
- 2026-05-13T13:02:54.457092+00:00: The next run should implement holdout/generalization evaluation first; external pilot work resumes after that signal or in parallel only when directly unblocking import readiness.
- 2026-05-13T17:47:33.256358+00:00: External pilot now has per-candidate review dossiers; next work should fill decisions and missing evidence, not add generic gates.
- 2026-05-13T18:44:44.009443+00:00: External pilot import remains blocked; next work should fill real active-site and sequence evidence decisions rather than expanding gate count.
- 2026-05-13T19:39:20.606270+00:00: External pilot import remains blocked; high-fan-in gate maintenance is reduced, but active-site source decisions and complete near-duplicate search remain the next blockers.
- 2026-05-13T20:51:07.000000+00:00: Geometry retrieval predictive evidence is now explicitly text-free; PLP positive signal uses local ligand-anchor context
- 2026-05-13T22:04:23.805937+00:00: M-CSA-only growth remains stopped; next external-pilot work should fill real sequence-search and active-site decisions rather than add generic gates.
- 2026-05-13T22:34:16.818554+00:00: External transfer remains non-countable; complete UniRef/all-vs-all sequence search and active-site evidence decisions still block import.
- 2026-05-13T23:52:26.926762+00:00: external pilot can proceed to review decisions only after active-site sources and complete sequence search; no external import is ready
- 2026-05-14T00:43:19.772463+00:00: Artifact graph consistency still matters at count-decision boundaries; next work should fill external pilot evidence decisions rather than add generic gates.
- 2026-05-14T03:08:19.594666+00:00: External pilot remains review-only; next highest-value work is coordinate staging for TM-score only if it directly unblocks pilot import readiness, plus active-site source decisions and complete near-duplicate search.
- 2026-05-14T04:23:49.348241+00:00: Next useful external-pilot work is active-site source decisions and representation repair for selected rows; M-CSA-only count growth remains stopped.
- 2026-05-14T05:08:05.672183+00:00: Full TM-score split remains blocked until remaining selected coordinates are staged and a Foldseek-backed split builder is added; partial staged25 TM signal is review-only evidence.
- 2026-05-14T05:12:09.497043+00:00: Foldseek artifacts now have regression coverage; full TM-score split remains blocked until the remaining selected coordinates and split builder are implemented.
- 2026-05-14T09:28:41.519786+00:00: Expanded40 Foldseek raw-name mapping is no longer a blocker, but the partial staged-coordinate TM signal still fails the <0.7 target and full TM-score split remains blocked on full coordinate coverage plus a split builder.
- 2026-05-14T10:16:36.145071+00:00: Requested 650M representation remains blocked by local cache/disk/CPU limits; largest feasible cached ESM-2 150M now gives a real review-only control signal while Foldseek remains partial and fails the <0.7 target.
- 2026-05-14T11:07:34.295381+00:00: Next work should run a full Foldseek/TM-score split only after resolving missing selected structures and should advance pilot rows through broader duplicate screening, representation review, and review decisions without countable import.
- 2026-05-14T12:34:37.036864+00:00: Next agent should retry the all-materializable Foldseek TM-score signal as delegated backend work or emit a bounded larger-than-40 completed signal without false full-holdout claims.
- 2026-05-14T12:50:26.982940+00:00: Sequence-distance holdout is real backend evidence; next generalization blocker remains full Foldseek/TM-score split and external import blockers.
- 2026-05-14T14:10:21.275491+00:00: Expanded60 removes the expanded40 partial-signal ceiling, but full TM-score split remains blocked by two missing selected structures, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T15:07:52.876846+00:00: External pilot now has measurable success criteria and remains needs_more_work; Foldseek selected-structure blocker is narrowed to explicit coordinate exclusions plus the unrun full TM-score split.
- 2026-05-14T16:15:30.855586+00:00: Expanded80 removes the expanded60 partial-signal ceiling, but full TM-score split remains blocked by two coordinate exclusions, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T17:29:09.455993+00:00: Expanded100 removes the expanded80 partial-signal ceiling, but full TM-score split remains blocked by two coordinate exclusions, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T19:04:21.441130+00:00: Next Foldseek work should apply/regenerate the repaired split and rerun downstream metrics before any full TM-score claim
- 2026-05-14T19:08:48.002960+00:00: Next Foldseek work should rebuild downstream evaluation from the candidate split and run an uncapped all-materializable Foldseek signal when feasible
- 2026-05-14T20:34:07.608397+00:00: Repaired expanded100 removes the projection-only computed-subset blocker, but full TM-score split remains blocked by the cap, two coordinate exclusions, and the uncomputed all-materializable signal
- 2026-05-14T21:29:26.788448+00:00: Uncapped all-materializable Foldseek exact TM-score search exceeds the normal automation window; next work needs a longer run budget or chunk/resume support, not another routine capped increment
- 2026-05-14T22:36:14.676450+00:00: Resumable Foldseek query chunks remove the all-at-once-only runtime SPOF but show the repaired candidate split still fails the <0.7 TM-score target beyond the expanded100 cap
- 2026-05-14T23:22:21.551765+00:00: Foldseek query chunk aggregation is now durable; next work should adjudicate target-violating chunk blockers or change the chunk-2 runtime/slice strategy before routine chunk continuation
- 2026-05-15T00:19:07.369532+00:00: Full TM-score holdout remains blocked by target-violating completed chunks, held-out in-scope split blockers, incomplete query coverage, and two coordinate exclusions
- 2026-05-15T01:39:52.871051+00:00: Round-2 split redesign clears Foldseek chunk 0 only; next work should continue chunk 1 under the round-2 candidate and stop on any new target violation
- 2026-05-15T02:47:11.394945+00:00: Round-3 split redesign clears Foldseek chunks 0-1 only; next work should continue chunk 2 and stop on any new target violation
- 2026-05-15T03:40:39.370706+00:00: Round-3 Foldseek chunks 0-2 clear the completed-chunk target, but chunk 3 is now the runtime blocker; retry or split chunk 3 before continuing coverage
- 2026-05-15T04:56:18.692987+00:00: Cluster-first Foldseek split design replaces blind 56-chunk continuation; next work should verify bounded subchunks from the round-3 cluster-first readiness and fold in any new high-TM blockers before continuing.
- 2026-05-15T05:48:11.759711+00:00: Cluster-first round4 clears the latest failing verification unit; continue bounded round4 subchunks and fold in any new high-TM blockers before claiming full TM-score holdout.
- 2026-05-15T06:49:36.549572+00:00: Cluster-first round6 clears subchunk 009; next work should continue bounded round6 verification from subchunk 010 and fold in any new high-TM blocker before broad coverage claims
- 2026-05-15T08:46:02.937530+00:00: Round-8 cluster-first split folds in the new m_csa:68/m_csa:750 blocker; next work should continue single-query verification from staged index 68 under round-8 readiness.
- 2026-05-15T13:32:19.332566+00:00: Round-9 cluster-first split folds in the m_csa:80 high-TM blocker; next work should continue single-query verification from staged index 84 under round-9 readiness.
- 2026-05-15T14:31:01.833373+00:00: Round-9 cluster-first verification now clears staged indices 79-95; next work should continue from staged index 96 and stop on any TM>=0.7 blocker
- 2026-05-15T16:41:11.445104+00:00: Full TM-score holdout remains blocked by incomplete round-16 verification coverage and two coordinate exclusions.
- 2026-05-15T17:34:47.871028+00:00: Round-19 cluster-first split is the active Foldseek handoff; next work should verify staged index 112 under round-19 readiness.
- 2026-05-15T19:16:47.231347+00:00: Full TM-score holdout remains blocked by incomplete round-24 verification coverage and two coordinate exclusions.
- 2026-05-15T22:46:27.435996+00:00: Full TM-score holdout remains blocked by round32 index 145 timeout, incomplete query coverage, candidate-only split status, and two coordinate exclusions.
- 2026-05-16T06:10:48.154425+00:00: Next useful work is external pilot blockers or external structure index/nearest-neighbor cache, not more M-CSA strict-TM repair.
- 2026-05-16T07:15:23.155977+00:00: Next work should route the 3 deferred external pilot rows to human/expert review or start external structural clustering; do not resume M-CSA round repair.
- 2026-05-16T08:06:00.835318+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or start external structural clustering; do not resume M-CSA round repair.
- 2026-05-16T09:14:46.363953+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or expand the broader external structural candidate surface before any strict TM-diverse split assignment.
- 2026-05-16T10:14:24.266801+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or complete/cache the missing all-30 external structural pairs before strict TM-diverse split assignment.
- 2026-05-16T11:15:09.904197+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or broaden external structural candidates beyond the current review-only 30-row split before import claims.
- 2026-05-16T12:15:25.647551+00:00: Next external pilot work should resolve the six needs_review rows or broaden external structural candidates; do not treat representation-only duplicate signals as hard rejections unless evidence is stable.
- 2026-05-16T13:07:13+00:00: Next external pilot work should resolve the six needs_review rows or broaden external structural candidates; no local-evidence-only decision update was defensible.
- 2026-05-16T14:26:15.956789+00:00: External candidate all-vs-all duplicate screen is now complete for the current 30-row sample; UniRef-wide screening plus review decisions still block import.
- 2026-05-16T15:22:11.987493+00:00: Selected-pilot needs_review is no longer the active blocker; next external work should repair representation or heuristic controls or broaden the external structural surface.
- 2026-05-16T20:03:03.218017+00:00: Next direct work should integrate the Q6NSJ0 glycoside-hydrolase boundary control into import-safety adjudication or complete O14756 duplicate review and full factory gate path before import.
- 2026-05-16T21:00:19.989175+00:00: Next direct work should integrate the P34949 sugar-phosphate isomerase control into import-safety adjudication or complete duplicate/review/factory blockers for repaired O14756 and Q6NSJ0.
- 2026-05-16T21:04:56.234887+00:00: Next run should reacquire the lock, verify local-ahead state, and push the remaining handoff/status correction after GitHub credentials are usable.
- 2026-05-16T22:05:28.138975+00:00: Next direct work should complete duplicate/review/factory blockers for repaired external rows or continue C9JRZ8 AKR/NADP repair without broadening generic gates.
- 2026-05-16T23:03:05.000429+00:00: Next direct work should complete duplicate/review/factory blockers for repaired external rows or implement the remaining P06746 DNA Pol X/5'-dRP lyase repair lane without broadening generic gates.
- 2026-05-17T02:10:05.048551+00:00: External out-of-scope import requires all-8 inverse gate plus duplicate review and factory gates; O14756 and Q6NSJ0 are blocked despite inverse-gate pass.
- 2026-05-17T04:14:25+00:00: Fresh external sourcing and the first current-countable structural screen are complete; Q13087 is the only sequence-clean row without a high-TM current-countable signal, but pair-cache completion, UniRef-wide screening, terminal review, and factory gates still block import.
- 2026-05-17T05:01:18.923988+00:00: Fresh sourced hard-negative tranche is closed by current-countable structural duplicate signals; next work needs new external candidate sourcing or genuinely new evidence.
- 2026-05-17T07:42:26.961418+00:00: Next-candidate UniRef current-reference duplicate blocker is removed for P22830 P78549 Q3LXA3; terminal review and full factory gates are now the active blockers.
- 2026-05-17T09:08:30+00:00: First external out-of-scope hard-negative import succeeded for P78549; next work should decide whether P22830 or Q3LXA3 should enter a later single-import cycle after litmus remains green.
- 2026-05-17T09:41:38.959359+00:00: Post-import litmus remains green after P78549; Q3LXA3 is the next review-only candidate if a later explicit single-import cycle is opened.
- 2026-05-17T10:50:16.595786+00:00: Second external out-of-scope hard-negative import succeeded for Q3LXA3; P22830 remains review-only and should require its own explicit cycle or broader sourcing decision.
- 2026-05-17T13:25:17.879225+00:00: Broader external sourcing now has one surviving no-current-structural-signal row, P06744; terminal review and full factory/import gates are the active blockers.
- 2026-05-17T13:49:27.020292+00:00: P06744 is now a countable external out-of-scope hard negative; next work should not retry broader duplicate-signal rejects without new evidence.
- 2026-05-17T17:13:28.332690+00:00: candidate-specific pilot repairs are development evidence only; next external tranche requires frozen preregistration
- 2026-05-18T04:13:16.733717+00:00: Phase 1 artifact-migration instrumentation is complete; next action is human approval for Phase 2 upload target and subset.
- 2026-05-18T07:51:37.415598+00:00: ePK now has review-only local axes, acceptor threshold hypotheses, gamma-distance samples, and a blocked pre-count gate; positive-universe expansion still requires true acceptor identity, ATP-state repair, threshold calibration, external re-audit, and label-factory extension.
- 2026-05-18T13:55:35.875542+00:00: ePK threshold selection is now blocked on negative-control distance distributions and non-ready row repair rather than threshold design itself.
- 2026-05-18T15:03:10.233611+00:00: ePK threshold selection is now blocked by observed sibling-family gamma-distance overlap plus incomplete non-ready row repair.
- 2026-05-18T17:05:01.231831+00:00: ePK threshold selection is now blocked by negative-control calibration and complete gamma geometry rather than non-ready-row ambiguity.
- 2026-05-18T18:01:10.526233+00:00: ePK threshold selection remains blocked after measured sibling alternate controls; next work needs missing ATP-grasp NDK PfkA and PfkB controls or a non-distance-only axis.
- 2026-05-18T19:01:23.160128+00:00: ePK threshold selection now has explicit ATP-grasp NDK PfkA and PfkB source requests; next work should repair or source one missing sibling family at a time before any score or threshold.
- 2026-05-18T20:03:10.553576+00:00: ePK PfkB mapping ambiguity is narrowed but threshold selection remains blocked because PfkB still lacks a metal-supported gamma-capable sibling control.
- 2026-05-18T21:12:49.756080+00:00: ePK direct graph-linked sibling-control repair is exhausted for ATP-grasp NDK PfkA and PfkB; threshold selection now needs external or homolog gamma-capable controls rather than another direct repair review.
- 2026-05-18T22:05:23.696999+00:00: ePK NDK now has homolog gamma-metal source candidates but threshold selection remains blocked until catalytic-residue mapping succeeds.
- 2026-05-18T23:06:35.869912+00:00: ePK NDK mapping is no longer the active blocker; next work should measure mapped NDK homolog controls review-only before threshold selection.
- 2026-05-19T00:13:47.867615+00:00: ePK gamma distance alone remains unsafe; NDK histidine counter-axis evidence and fail-closed external-negative abstentions make family-specific mapping for PfkB PfkA and ATP-grasp the next bounded step before any scorer or threshold claim.
- 2026-05-19T00:38:30.189051+00:00: ePK remaining sibling controls now need family-specific homolog mappers from seeded source templates before any distance measurement or threshold claim.
- 2026-05-19T01:44:03.576487+00:00: ePK distance-only thresholding is now explicitly falsified by 16 family-specific sibling controls plus NDK phosphohistidine controls; next useful work needs a substrate-acceptor or family-disambiguation rule or the 3TM0 ANP/B31 m_csa:640 gamma-geometry review before any score.
- 2026-05-19T02:44:02.632801+00:00: ePK has a sharper fail-closed review-only counteraxis, but the simplest text-free acceptor feature is blocked by sibling-control false hits; next work should add chain/substrate or ligand-class disambiguation before any score or external scored re-audit.
- 2026-05-19T03:46:56.310139+00:00: ePK chain/ligand context is promising review-only disambiguation, but production scoring remains blocked by calibration, text-free feature admissibility, negative-control distribution readiness, and scored external hard-negative re-audit.
- 2026-05-19T12:03:38.595849+00:00: Current bounded ePK source-repair candidates are exhausted as review-only negatives; next useful work needs new mapped protein-substrate evidence or an inactive policy draft promoted only after sibling and external hard-negative re-audits.
- 2026-05-19T13:17:33.402946+00:00: ePK analog/product-state and 5LI1 evidence are now explicit fail-closed review-only blockers; source triage still has no new protein-substrate candidate, so production expansion needs genuinely new source evidence or a pre-frozen calibrated policy path.
- 2026-05-19T14:18:17.427495+00:00: External reviewed kinase source evidence can produce mapped active-state Q8IVT5 structures, but current acceptor-like geometry is not source-mapped; production ePK expansion remains blocked until an exact source-mapped protein-substrate acceptor and calibrated scorer controls exist.
- 2026-05-19T15:19:23.015183+00:00: Ligand-specific substrate/co-complex querying can produce concrete review leads; next work should manually validate 5HVK source evidence before any measurement or scoring.
- 2026-05-19T16:05:05.942310+00:00: 5HVK is now source-valid review evidence, but ePK production scoring remains blocked until the queued prototype/control rerun, threshold calibration, and real external hard-negative scored re-audit exist.
- 2026-05-19T17:07:27.421941+00:00: 5HVK reduces the ligand-analog dependency for ePK scorer development, but production scoring remains blocked by source-authority chain-role dependence, threshold calibration, broader controls, and real external hard-negative scored re-audit.
- 2026-05-19T18:22:33.619263+00:00: Source-free local topology alone false-hits same-accession phosphosite controls, but a heteromeric author-chain polymer entity counter-axis separates current hits; production remains blocked by one-positive coverage, threshold calibration, real external hard-negative scored re-audit, and registry/factory extension.
- 2026-05-19T19:16:16.071899+00:00: ePK heteromeric topology now has measured source-valid review leads beyond 5HVK, but scorer threshold external re-audit and registry gates remain closed.
- 2026-05-19T20:23:20.534717+00:00: ePK heteromeric topology now has a review-only local counteraxis that clears the current six-row review surface, but production scoring still needs broader controls thresholds and a real external scored re-audit.
- 2026-05-19T21:26:22.348537+00:00: ePK heteromeric role direction is stronger after broader counteraxis and ligand-asymmetry controls, but generic hydroxyl residue identity is too weak for production; next work needs a non-generic local acceptor-identity signal before thresholding or external scored re-audit.
- 2026-05-19T22:26:42.259225+00:00: A short peptide-like acceptor-chain rule is useful current-control evidence for heteromeric ePK review, but it is narrow; production scoring still needs general substrate identity, threshold calibration, real external scored re-audit, and registry/factory extension.
- 2026-05-19T23:28:59.207385+00:00: The exact ANP/Mg source is exhausted and outside-query sourcing can find PKB/GSK3 peptide review leads but the decision surface still needs a source-free substrate-role or general acceptor-identity axis before any scorer or label gate.
- 2026-05-20T00:30:20.032873+00:00: ePK peptide-mode coverage now includes outside-query PKB/GSK3 leads but production scoring remains blocked by missing unified source-free substrate identity threshold calibration real external scored re-audit and registry gates.
- 2026-05-20T02:33:19.307966+00:00: ePK unified review-only prototype is current-control clean, but broad-stress counterexamples 9L3M/9L3U and uncalibrated thresholds keep production scoring closed; next work should execute the preregistered broad-stress tranche before threshold or real external scored re-audit.
- 2026-05-20T03:33:14.995937+00:00: ePK broad-stress execution found more source-context counterexamples but the peptide-role counterevidence rule blocks them without changing production gates; next work should seek a more general source-free substrate identity axis or a qualitatively new positive source before threshold work.
- 2026-05-20T04:34:07.290642+00:00: A relaxed polymer identity rule is unsafe because 7B56 false-hits; a length-band counteraxis repairs that bounded source-expansion false hit but remains too scoped for production, so ePK still needs broader substrate-identity stress or new positive source evidence before thresholding.
- 2026-05-20T05:33:51.904993+00:00: ePK protein-role evidence is current-control clean but not general: 7B56 blocks relaxed folded-protein generalization and the fourth external source pass adds no measurement-ready positives.
- 2026-05-20T06:36:57.763104+00:00: The mid-length rule repairs the current 7B56 failure but has no broad source-valid protein-substrate positive; the first 100 ligand-specific active-query hits add counterexamples but no new positive source, so ePK thresholding and production fingerprint expansion remain closed.
- 2026-05-20T07:35:18.172497+00:00: Broad active-query routes now look negative for clean ePK protein-substrate sourcing; next progress needs MEK ERK source-authority review or a curated kinase-substrate source rather than thresholding current query hits.
- 2026-05-20T08:39:33.652171+00:00: MEK ERK now provides two source-authoritative review controls but broad protein-role geometry is unsafe; source-free substrate identity or source adjudication for 7CAG and 8BMS is the next blocker before scorer calibration.
- 2026-05-20T09:40:52.064773+00:00: MEK ERK residual false hits are now closed in a bounded source-free topology probe, but broader stress leaves four false hits; the next useful ePK work needs an additional source-free acceptor or substrate-identity axis before thresholding.
- 2026-05-20T11:24:52.078372+00:00: 4EKK is useful source-mapped ePK review evidence, but production remains blocked by source-context dependence, uncalibrated substrate-mode logic, external scored re-audit, and local disk capacity before broader source-review recovery.
- 2026-05-20T12:19:46.938589+00:00: Folded protein-substrate sourcing is still negative under the current source-free substrate-mode surface; next work needs a fresh bounded tranche with stronger source-free substrate identity or pair-specific source mapping kept outside predictive scoring.
- 2026-05-20T13:17:20.692201+00:00: Next external mini-campaign blocker is restoring or configuring Foldseek before current-countable structural screen and inverse-gate scoring can produce import decisions
- 2026-05-20T14:14:08.715044+00:00: Next mini-campaign work should materialize the 11 candidate coordinate sidecars before rerunning Foldseek; next SDR work should freeze a 10-20 row SDR/AKR control tranche before scoring.
- 2026-05-20T15:32:22.885905+00:00: Next external mini-campaign work needs genuinely new preregistered sourcing or a different frozen surface; do not rerun this structurally duplicated set for import.
- 2026-05-20T16:07:10.750132+00:00: Current ePK evidence still does not remove production blockers; the only exact future ePK experiment is deferred review-only fresh substrate-role stress.
- 2026-05-20T16:21:03.279937+00:00: Next best non-ePK family work is scoring only the preregistered glycoside hydrolase versus metal/ser-his hydrolase review-only tranche; no family is production-ready.
- 2026-05-20T17:10:02.023049+00:00: Fresh ePK research-lane output reinforces the no-go production decision; main-loop work should continue the preregistered glycoside hydrolase control tranche.
- 2026-05-20T17:16:23.980051+00:00: Glycoside hydrolase control tranche is closed as a review-only small win; future work needs source-free acidic-dyad/glycan-pocket axes and broader duplicate coverage before any import path.
- 2026-05-20T17:19:03.090362+00:00: Glycoside baseline comparison is diagnostic only; Foldseek external no-signal does not replace current-countable structural duplicate screening.
- 2026-05-20T17:20:38.990082+00:00: Small-win run is ready to commit and push with ePK still review-only and glycoside hydrolase still no-go for production.
- 2026-05-20T18:22:16.234314+00:00: Next main-loop work should use source-complete external rows or freeze one Schiff-base/DNA-lyase control tranche before scoring; ePK remains research-lane-only.
- 2026-05-20T19:12:53.814979+00:00: Commit the ePK integration, then return the main loop to source-complete external rows or a frozen non-ePK control tranche.
- 2026-05-20T19:49:09.571418+00:00: The previous fallback queue no longer has an unscored family tranche; all six families are terminal review-only no-go surfaces.
- 2026-05-20T19:49:17.503329+00:00: Small-win tranche run is ready to commit and push; next work should avoid reopening the closed six-family queue unless new evidence appears.
- 2026-05-20T20:13:02.164962+00:00: Commit this ePK integration, then return the main loop to genuinely new external sourcing or a new non-ePK family packet.
- 2026-05-20T20:55:03.996810+00:00: Next main loop can score the frozen ASKHA tranche axes or start another genuinely new prospective external surface; ePK remains research-lane-only.
- 2026-05-20T22:19:09.281826+00:00: Fresh late ePK evidence strengthens the no-go decision; commit this integration, then return the main loop to non-ePK visible small wins.
- 2026-05-20T22:44:16.389654+00:00: ePK remains review-only no-go; GHKL/dNK closed review-only; PfkB packet-only no-go.
- 2026-05-20T23:59:52.878029+00:00: Main loop has closed NDK as review-only no-go and packaged PfkA; next bounded ATP-family step is a frozen PfkA-vs-neighbor tranche before any scoring, or a genuinely new external mini-campaign.
- 2026-05-21T00:18:48.662111+00:00: Commit ePK synthesis integration before returning to non-ePK small-win ladder.
- 2026-05-21T00:27:03.666400+00:00: Next bounded work can close PfkA-vs-neighbor tranche or stop for wrap if cadence is reached.
- 2026-05-21T00:35:13.353330+00:00: continue external or non-ATP-family small wins; do not promote PfkA
- 2026-05-21T00:41:53.519062+00:00: future movement needs source-free geometry duplicate screens terminal review and factory/import gates
- 2026-05-21T00:44:11.610704+00:00: simple EC and sequence baselines provide routing and duplicate caveats only
- 2026-05-21T00:49:00.721874+00:00: future movement needs source-free geometry duplicate screens terminal review and factory/import gates
- 2026-05-21T00:51:14.465122+00:00: 20260521 external campaign baselines are routing and duplicate diagnostics only
- 2026-05-21T00:58:14.196100+00:00: external mini-campaign wins are terminal review-only evidence until source-free geometry duplicate screens terminal review and factory/import gates exist
- 2026-05-21T01:19:56.798534+00:00: Commit ePK remote synthesis before returning to external mini-campaign small wins.
- 2026-05-21T01:27:27.260565+00:00: future movement needs source-free geometry duplicate screens terminal review and factory/import gates
- 2026-05-21T01:31:38.491051+00:00: future movement needs source-free geometry duplicate screens terminal review and factory/import gates
- 2026-05-21T01:35:50.770123+00:00: future movement needs source-free geometry duplicate screens terminal review and factory/import gates
- 2026-05-21T01:41:08.373902+00:00: use a different external sourcing route or wait for new cobalamin source rows; do not score one-row campaign
- 2026-05-21T01:47:47.464485+00:00: radical SAM external mini-campaign remains review-only and not import-ready
- 2026-05-21T01:50:11.872301+00:00: current-fingerprint external benchmark is review-only and cannot support superiority import or production scoring claims
- 2026-05-21T01:55:41.795664+00:00: external small-win rows remain review-only until source-free geometry duplicate screens terminal review and factory/import gates pass
- 2026-05-21T02:00:27.449389+00:00: ePK remains review-only no-go; next exact ePK work belongs only in isolated research lanes
- 2026-05-21T02:02:02.049578+00:00: next main-loop work should run the 14-row source-free geometry sidecar and duplicate-screen experiment or continue non-ePK small wins
- 2026-05-21T02:49:40.198593+00:00: No superiority or import claim is made until the duplicate/leakage screen completes; geometry top1 routed six of seven rows to metal_dependent_hydrolase but remained below the in-scope floor.
- 2026-05-21T02:52:33.159296+00:00: next main-loop work should complete a resumable/chunked current-countable structural duplicate screen before any import or superiority claim
- 2026-05-21T04:01:42.976219+00:00: Geometry adds signal for flavin but no import or mechanism-match claim is allowed until pair-cache-complete duplicate screening exists.
- 2026-05-21T14:06:11.129182+00:00: Next exact heme work is smaller full-current subchunk duplicate screening for I2DBY1 before any duplicate-clear or mechanism-match claim.
- 2026-05-21T15:03:50.814880+00:00: Next main-loop work should run bounded FMO geometry scoring and full current-countable duplicate/leakage screening for the four non-hit rows, or the bounded P31614 PDB active-site mapping probe; do not open a new broad mini-campaign.
- 2026-05-21T16:08:32.602022+00:00: Next FMO work is one Q7RTP6 two-target retry plus remaining full-current chunks for O94851 and Q7RTP6; no broad mini-campaign or duplicate-clear claim.
- 2026-05-21T17:08:18.443673+00:00: Next exact FMO work is chunks003-013 for O94851 and Q7RTP6, using smaller subchunks when a 48-target chunk times out.
- 2026-05-21T17:09:52.130652+00:00: Next exact work remains chunks003-013 for O94851 and Q7RTP6 before any duplicate-clear or wrong-scope terminal claim.
- 2026-05-21T18:12:47.873454+00:00: Next work should run one bounded P31614 coordinate/alignment plus full-current duplicate experiment or choose another frozen nonterminal external deep-packet blocker; do not open a broad mini-campaign.
- 2026-05-21T19:37:19.047962+00:00: Next main-loop win should implement the PLP source-free covalent cofactor extractor or choose another frozen nonterminal deep-packet blocker before adding broad external rows.
- 2026-05-21T21:16:37.365926+00:00: Do not open a seventh broad external mini-campaign; continue terminal deepening or exact family-readiness experiments.
- 2026-05-21T23:19:22.103465+00:00: Next metal work should build source-free geometry scoring for P75792/P0A8Y5 or move to a bounded non-ePK family-axis experiment
- 2026-05-22T00:21:07.387970+00:00: Continue bounded external terminal-decision deepening and import-gate readiness checks before any new broad mini-campaign.
- 2026-05-22T01:48:29+00:00: Next main-loop work should close the three second-heme full current-countable duplicate-screen blockers or deepen another existing frozen packet before adding broad rows.
- 2026-05-22T02:11:28+00:00: Next main-loop work should deepen another existing frozen packet or build import-gate evidence around review-ready rows without adding broad rows.
- 2026-05-22T02:17:12+00:00: Next main-loop work should deepen another existing frozen packet or choose one review-ready row for explicit UniRef-wide and label-factory payload work.
- 2026-05-22T03:34:56.636211+00:00: Next main-loop work should materialize coordinates then run source-free geometry and current-countable structural duplicate screens for P14532 plus P33371/P32340, or run a no-import label-factory payload dry run for the five review-ready rows only after explicit policy preregistration.
- 2026-05-22T05:15:55.239970+00:00: Next main-loop work should not add broad rows; build a no-import seed-fingerprint payload/policy dry run for the six review-ready rows or deepen another existing frozen packet.
- 2026-05-22T05:23:06.284991+00:00: Next run should preregister external seed-fingerprint counting policy before any full label-factory payload gate dry run or continue frozen-row deepening.
- 2026-05-22T05:25:41.522048+00:00: Next exact import-gate step is preregistering an external seed-fingerprint counting policy and running a full no-import label-factory payload gate dry run for the six review-ready rows.
- 2026-05-22T08:48:17.767316+00:00: Next exact work is a current-682 external seed-fingerprint payload adapter/rebaseline and no-import gate rerun; metal rows still need source-free phosphate/substrate specificity.
- 2026-05-22T08:49:45.493927+00:00: Next exact work is a current-682 external seed-fingerprint payload adapter/rebaseline or a source-free phosphate-pocket extractor/holo-structure search before any metal import claim.
- 2026-05-22T08:51:15.302701+00:00: Metal mechanism-match rows need a holo/analog phosphate-like coordinate structure or preregistered phosphate-pocket extractor before phosphatase-specific seed import claims.
- 2026-05-22T10:20:02.906647+00:00: Next useful work is no-import import-gate readiness for the seven review-ready rows or a bounded full-current/UniRef screen for any remaining review-ready row outside the six-row payload dry run.
- 2026-05-22T10:31:38.361386+00:00: Next exact work is the current-682 external seed-fingerprint payload adapter and no-import label-factory gate rerun for all seven review-ready rows.
- 2026-05-22T11:35:58.020005+00:00: Next exact decision is human/expert review for the five non-metal review-ready seed candidates; metal rows still need phosphate/substrate specificity evidence before phosphatase-specific import claims.
- 2026-05-22T13:05:41.322034+00:00: Continue terminal deepening or exact family-readiness packets; remaining PLP breadth should only use already frozen rows.
- 2026-05-22T13:08:53.551713+00:00: Second PLP packet is ready for review; continue existing frozen-row deepening next.
- 2026-05-22T15:49:13.822899+00:00: PLP non-exact frozen rows are terminal; AKR remains review-only no-go.
- 2026-05-22T18:05:27.783477+00:00: Next action is human accept/reject review or a bounded source-free axis experiment, not label import
- 2026-05-22T18:35:34.824679+00:00: Next action is human accept/reject review or a future preregistered NAD(P) pocket/holo-structure experiment; do not import labels
- 2026-05-22T19:42:57.546947+00:00: Next no-breadth work should wait for human action on seven mechanism-match rows or resolve NADP holo/specificity evidence for O14756 O75828 C9JRZ8.
- 2026-05-22T20:37:21.159775+00:00: If human review is unavailable, continue only bounded PyMOL structure materialization from the remaining blocker report.
- 2026-05-22T21:32:20.016660+00:00: The no-breadth queue is now human-review blocked rather than source-free geometry or duplicate-screen blocked.
- 2026-05-23T18:03:35.801938+00:00: Next external-deepening work should resume with metal phosphatase only if new human action or source-free coordinate evidence is available; otherwise the queue is human/evidence blocked.
- 2026-05-23T19:56:43.019061+00:00: Do not return to broad external breadth until post-clean9 M-CSA hold decisions are either accepted through gates or explicitly deferred.
- 2026-05-23T20:13:13.233624+00:00: Next M-CSA automation needs explicit post-preview accept decisions for held override or m_csa771 rows before more gated imports.
- 2026-05-24T03:55:03.938943+00:00: Do not repeat the nine-row M-CSA blocker loop without new evidence, production-rule work, or an explicit schema/fingerprint task.
- 2026-05-24T04:58:59.872641+00:00: Next run should build a one-row derived review-only repair rerun for m_csa:946 using 5XD7 and keep m_csa:930 blocked until Q9ZFQ5 evidence exists.
- 2026-05-24T05:54:43.004965+00:00: Next automation should support human review of the 40-row subset before any later dedicated gate or import-preview work.
- 2026-05-24T18:47:30.176583+00:00: Next substantive step is human review of clean10 then exact40; while Vivek is away only maintain consistency or docs around the fixed 298-row support surface.
- 2026-05-24T18:49:21.274042+00:00: Do not make M-CSA review decisions while Vivek is away; next safe work should only maintain review-support consistency or documentation until human review happens.
- 2026-05-24T18:53:06.309748+00:00: Next no-human run should only maintain review-support consistency or leakage-safe manifests; human review starts with clean10.
- 2026-05-25T09:13:01Z: Next benchmark work should resolve the 20 missing sequence rows before any representation training or learned-superiority claim.
- 2026-05-25T11:17:39.450858+00:00: Future sequence-NN or PLM benchmark results must cite the contract SHA and include OOS tier plus diversity reports before interpretation.
- 2026-05-25T12:36:38Z: Repair or regenerate the current702 split before any sequence-NN prediction or metric artifact is allowed.
- 2026-05-25T13:37:58.445786+00:00: Repair or regenerate the current702 split before sequence-NN predictions or metrics; restore GitHub push authentication before local ahead commits can land.
- 2026-05-25T14:36:49.637815+00:00: Next run should repair/regenerate split coverage before MMseqs nearest-neighbor prediction.
- 2026-05-25T15:10:30.958833+00:00: Next work should inspect or compare the deterministic sequence baseline as a control rather than repairing split coverage.
- 2026-05-27T10:15:26Z: Next Packet 1/Wave 1 work should be expert review for m_csa:750 plus FMO acquisition; do not treat hydride sublabel as ready. Push requires GitHub credential repair.
- 2026-05-27T13:12:54.482909+00:00: Wave 1 Packet 1 TM-pair claims are no longer capped by the prior 200-row retention limit; full 692-query all-vs-all remains unclaimed.
- 2026-06-03T09:54:04.655478+00:00: Next run should start by applying explicit source-packet decisions if available; otherwise no mechanical gate is open.
- 2026-06-03T10:52:23.444858+00:00: Next run should edit only source decision packets if reviewed decisions are available then rerun the source intake preflight before application or materialization gates.
- 2026-06-03T11:23:19.905443+00:00: Next run should edit source decision packets only if reviewed decisions are available, then rerun source intake and the decision-application contract audit before any matching gate.
- 2026-06-03T14:51:20.045307+00:00: Lever 3 now has an executable 50-row train/cal scoring input manifest; next step is materializing query CIFs and scoring without heldout threshold tuning.
- 2026-06-03T15:57:39.461549+00:00: Lever 3 proxy calibration is now mechanically exhausted under the current proxy axes; remaining progress needs source decisions, policy decisions, or a new proxy/evidence axis rather than another automatic scoring tranche.
- 2026-06-03T17:56:13.579427+00:00: Next Lever 3 progress should clear prior/base full-channel and policy/calibration blockers, or pre-register a no-duplicate follow-up train/cal-only proxy axis before scoring.
- 2026-06-03T19:56:36.530027+00:00: clear six remaining combined-score blockers before fixed-threshold confounded proxy audit
- 2026-06-03T23:39:07+00:00: Next Lever 2 work should clear locator coverage for the 87 missing heldout rows or write an explicit partial-surface policy before any frozen residual threshold read.
- 2026-06-04T00:37:12.914214+00:00: Next run should decide deterministic missing-locator abstention versus complete source-free locator coverage before any frozen residual threshold read.
- 2026-06-04T01:43:55.363807+00:00: Next Lever 2 work should not rerun heldout; start with train/cal-safe feature repair for feature-complete primary abstentions, then recover primary source-free locator coverage.
- 2026-06-04T12:50:52.667257+00:00: Next Lever 3 action is to run/provision the exact P07658 full-length predicted coordinate using the FASTA/template, rerun acceptance preflight, then acquire 16 source-free high-cofactor train/cal OOS rows before the 170-row same-family structural surface.
- 2026-06-04T13:53:10.947379+00:00: Next Lever 3 action is to fill the P07658 coordinate and provenance dispatch first then high-cofactor slots then same-family structural slots before any fixed-threshold rerun.
- 2026-06-04T14:25:57.944431+00:00: Lever 3 now has a measured current operating-point readout but deployment closure still needs P07658 accepted full-length predicted-coordinate provenance plus 16 high-cofactor and 170 same-family structural train/cal OOS acquisition rows.
- 2026-06-04T15:52:38.463795+00:00: Current source-free evidence supports measured diagnostics but not deployment closure; strict high-cofactor and same-family acquisitions remain required
- 2026-06-04T16:54:35.141959+00:00: Current evidence is measured but insufficient; next action is exact P07658 full-length prediction/provenance, then 16 strict high-cofactor rows, then 170 strict same-family structural rows
- 2026-06-04T17:54:27.719250+00:00: Current train/cal-selected source-free channels are measured but insufficient for Lever 3 closure; next progress needs accepted P07658 full-length predicted-coordinate provenance plus strict high-cofactor acquisition.
- 2026-06-04T18:22:07.166395+00:00: Current fixed source-free channels cannot close Lever 3 at 90pct retention or at any retention; next progress needs accepted P07658 coordinate provenance plus strict high-cofactor acquisition.
- 2026-06-04T20:51:00.471108+00:00: Current source-free numeric evidence now supports a measured operating-point closure scout for high-cofactor plus same-family shortfall at 31/34 calibration retention, but deployment closure still needs an accepted bandpass counteraxis contract and full-length P07658 predicted-coordinate provenance.
- 2026-06-04T21:37:20.235148+00:00: Lever 3 counteraxis evidence is now contract-ready at the train/cal operating point; remaining deployment closure requires only accepted exact full-length P07658 predicted-coordinate provenance before any fixed-threshold rerun.
- 2026-06-04T22:26:32.470910+00:00: Counteraxis contracts remain ready but no no-credential exact route clears P07658; next progress requires credentialed BioLM or NVIDIA NIM-style route or local predictor that emits full-length coordinate provenance with U140 documented.
- 2026-06-04T23:22:40.005804+00:00: Lever 3 now has a deployment-valid train-cal operating-point readout for hard-confounded residual routing but production closure remains blocked until exactly one credentialed or local full-length P07658 predictor route emits coordinate and U140 provenance.
- 2026-06-05T00:25:15.243472+00:00: Lever 3 operating-point evidence remains deployment-valid for hard-confounded train-cal routing while the only unsatisfied evidence family is exact full-length P07658 predicted-coordinate provenance and no local coordinate candidate is already present.
- 2026-06-05T01:33:57.855493+00:00: Lever 3 operating-point evidence remains deployment-valid for train-cal hard-confounded routing but P07658 closure must fail closed until one exact full-length credentialed or local predictor route returns coordinate plus filled provenance.
- 2026-06-05T02:27:05.027678+00:00: Lever 3 current evidence is enough for fail-closed safe abstention routing on the remaining P07658 gap but not enough for fixed-threshold scoring closure until exact full-length coordinate provenance exists.
- 2026-06-05T03:33:38.753039+00:00: Lever 3 now has a deployment-valid row-action readout that applies accepted counteraxes and fail-closed P07658 abstention; fixed-threshold scoring closure still needs exact full-length P07658 coordinate provenance and zero-residual-risk closure would need source-free counteraxis evidence for 11 retained same-family rows.

## Scope Adjustments

- 2026-05-09T13:40:25.768544+00:00: Project management is now repository state, not chat state; future scope changes must be recorded in the ledger.
- 2026-05-09T13:54:30.954964+00:00: V1 criteria are satisfied by a bounded 50-entry graph slice; broader scale is now an expansion problem, not a schema blocker.
- 2026-05-09T13:54:31.022704+00:00: V2 scaffold criteria are satisfied; next work should increase scientific quality rather than add more dashboard-like surface area.
- 2026-05-09T14:01:49.012481+00:00: Post-V2 quality work now targets geometry-aware retrieval rather than more text-only scaffolding.
- 2026-05-09T14:03:45.516905+00:00: Geometry now affects retrieval scores through residue signature matching and catalytic-cluster compactness.
- 2026-05-09T14:10:40.717863+00:00: Curated labels are now explicit for the 20-entry geometry slice; retrieval quality is measurable and currently weak at top1.
- 2026-05-09T14:13:21.398170+00:00: Each automation run is now an hourly carry-forward block: 55 minutes work, 5 minutes break/overhead, commit and push every run.
- 2026-05-09T14:18:10.779278+00:00: Every automation run must now leave explicit next-agent start instructions before committing and pushing.
- 2026-05-09T14:25:33.013901+00:00: V2 is stronger: retrieval has cofactor-aware scoring, calibrated abstention, and local performance measurement; full scalability and ligand parsing remain future work.
- 2026-05-09T15:20:27.676203+00:00: Post-V2 quality scope now includes ligand-supported cofactor evidence in retrieval; substrate-pocket descriptors become the next bounded upgrade.
- 2026-05-09T15:22:39.241656+00:00: Next automation should continue from substrate-pocket descriptors and harder negative controls, not from v0-v2 scaffold planning.
- 2026-05-09T15:30:17.008476+00:00: Post-V2 retrieval now includes pocket-aware scoring; next bounded iteration should tune abstention and false-positive control using failure categories.
- 2026-05-09T15:42:05.002091+00:00: Automation handoff now requires origin/main sync verification before the next agent starts.
- 2026-05-09T16:02:34.920556+00:00: Failure analysis is now explicit and reproducible; next bounded step is threshold-policy tuning with guardrails.
- 2026-05-09T16:03:37.698226+00:00: Catalytic Earth automation documentation now forbids downgrading below gpt-5.5 with xhigh reasoning.
- 2026-05-09T16:14:49.435851+00:00: If assigned work finishes or blocks early, agents must switch to the highest-value bounded unblocked task until the 50-minute work boundary.
- 2026-05-09T17:07:37.625326+00:00: 40-entry slice now has 36 labels, 26 evaluable structures, and explicit hard-negative plus structure-mapping blockers
- 2026-05-09T18:08:06.495922+00:00: expanded geometry slice to 60 fully labeled entries with 63 labels
- 2026-05-09T19:35:11+00:00: Expanded the audited geometry slice to 125 fully labeled entries; next scope is reducing 125-entry hard negatives without regressing the clean 20-100 slices.
- 2026-05-09T19:52:34.146667+00:00: 125-entry hard-negative controls are now grouped and anchored to correctly ranked positives; next scorer work should target the largest grouped control clusters.
- 2026-05-09T20:12:10.878697+00:00: Every automation wrap-up must update stale README/docs/work files or explicitly record that documentation was checked and unchanged.
- 2026-05-09T21:11:49.565784+00:00: Post-V2 geometry scope now tracks 150 labeled entries with cross-slice summary artifacts and in-scope failure analysis.
- 2026-05-09T22:17:13.285127+00:00: 150-entry geometry scope now separates local active-site positives from enzyme-level labels and tracks cofactor coverage explicitly
- 2026-05-09T23:20:32.069816+00:00: Post-V2 geometry scope now tracks 175 fully labeled entries with cofactor policy and seed-family audits.
- 2026-05-10T00:22:01.303388+00:00: Post-V2 geometry scope now tracks a fully labeled 225-entry source slice with 12 cross-slice summaries and clean hard-negative guardrails.
- 2026-05-10T01:18:40.670377+00:00: Post-V2 geometry scope now tracks a fully labeled 275-entry source slice.
- 2026-05-10T02:23:20.695520+00:00: Post-V2 geometry scope now tracks a fully labeled 375-entry source slice and a generated 400-entry candidate queue.
- 2026-05-10T03:26:17.876722+00:00: Post-V2 geometry scope now tracks a fully labeled 450-entry source slice and a generated 475-entry candidate queue.
- 2026-05-10T04:23:35.521223+00:00: Post-V2 geometry scope now tracks a fully labeled 475-entry source slice and a generated 500-entry candidate queue.
- 2026-05-10T05:25:09.634817+00:00: Label scaling is now factory-gated; new labels must pass promotion, demotion, adversarial-negative, active-learning, expert-review, family-propagation, validation, and test checks before counting.
- 2026-05-10T06:26:21.995107+00:00: 500-slice label scaling now has countable batch import and acceptance checks; next scope is resolving m_csa:494, not opening a 525-label tranche.
- 2026-05-10T07:28:17.575433+00:00: Label-factory scaling can continue from the 550 review-state registry; next tranche should use 546 as the countable baseline.
- 2026-05-10T08:36:59.402518+00:00: Post-V2 geometry scope now tracks accepted 600-entry countable labels and a generated 625-entry preview batch.
- 2026-05-10T13:59:54.901465+00:00: Post-V2 geometry scope now tracks accepted 650-entry countable labels and a generated 675 preview batch.
- 2026-05-10T14:37:36.208242+00:00: Post-V2 label-factory scope now separates preview mechanical acceptance from promotion readiness with carried/new review-debt metadata.
- 2026-05-10T15:39:13.368774+00:00: Post-V2 label-factory scope now blocks accepted review-gap labels, attaches scaling-quality audits to preview summaries, and records the missing sequence-cluster artifact before promotion.
- 2026-05-10T16:41:45.028412+00:00: 700-entry slice is guardrail-clean for clean labels; next bounded work is review-debt repair, not blind expansion.
- 2026-05-10T17:43:34.382296+00:00: Review-debt repair now separates alternate-structure cofactor leads from local active-site evidence before any further gated scaling.
- 2026-05-10T18:46:18.139775+00:00: Alternate-PDB residue remapping now produces review-only local evidence leads but does not reopen count growth.
- 2026-05-10T19:48:49.955298+00:00: 700 scaling remains stopped at 624 countable labels until reaction/substrate mismatch lanes are resolved by ontology rule or expert review.
- 2026-05-10T20:50:01.204415+00:00: 700 scaling remains stopped at 624 countable labels; reaction/substrate mismatch lanes now require complete expert-review export before more count growth.
- 2026-05-10T22:51:19.534178+00:00: 700 scaling remains at 624 countable labels; active expert-label decision lanes now require complete non-countable review export and repair-candidate coverage before any further gated growth.
- 2026-05-10T23:56:45.965586+00:00: 700 scaling remains at 624 countable labels; this run added repair guardrails and discovery-facing controls instead of count growth because review debt remains the limiting gate.
- 2026-05-11T03:12:54.274263+00:00: 700 factory gate now requires local-evidence gap audit and review-only export before count growth.
- 2026-05-12T15:04:26.275853+00:00: Expert-reviewed ATP/phosphoryl-transfer mismatch lanes now drive aggressive fingerprint-family ontology expansion for ePK ASKHA ATP-grasp GHKL dNK NDK PfkA PfkB and GHMP before returning to 10k gated label scaling.
- 2026-05-12T16:42:24.970333+00:00: Nine-family ATP/phosphoryl-transfer expansion is complete; next bounded work can resume factory-gated scaling toward 725.
- 2026-05-12T17:48:03.708741+00:00: Accepted 725 as the latest gated countable slice: 630 countable labels and 100 review-state rows kept non-countable.
- 2026-05-12T18:52:33.655337+00:00: Accepted-725 review debt is explicitly deferred; 750 preview is open but not canonical.
- 2026-05-12T20:14:45.382801+00:00: Accepted 750 as latest gated countable slice; next bounded work is a 775 preview only while the 750 post-batch gate stays clean.
- 2026-05-12T21:46:07.698000+00:00: Accepted 775 as latest gated countable slice; next bounded work is an 800 preview only while the 775 post-batch gate stays clean.
- 2026-05-12T22:58:26.440004+00:00: Accepted 850 as latest gated countable slice; geometry row reuse added for tranche scaling.
- 2026-05-13T00:50:52.831198+00:00: Accepted 950 as latest gated countable slice; review-debt deferral remains mandatory before 1,000-label milestone.
- 2026-05-13T02:01:21.378176+00:00: Accepted 1000 as latest gated countable slice; next bounded tranche is 1025 only while post-1000 gates stay clean.
- 2026-05-13T03:55:19.973294+00:00: M-CSA-only scaling is source-limited at 1,003 observed records; next work should build external-source transfer with all imported candidates non-countable until full factory gates pass.
- 2026-05-13T04:55:52.608228+00:00: M-CSA-only scaling remains stopped at 1,003 observed source records; external-source transfer is review-only evidence collection until active-site evidence OOD sequence holdouts heuristic controls decisions and factory gates pass.
- 2026-05-13T05:57:24.579339+00:00: M-CSA-only count growth remains stopped at 1,003 observed records; post-M-CSA scaling now depends on active-site-supported external controls plus representation or ontology repairs.
- 2026-05-13T06:58:30.872167+00:00: M-CSA-only count growth remains stopped at 1,003 observed records; post-M-CSA scaling still depends on review-only external-source repair and representation controls before label import.
- 2026-05-13T08:00:59.297672+00:00: Post-M-CSA scaling remains review-only; next import readiness depends on active-site sourcing, near-duplicate sequence search, and real representation controls before any external label decision.
- 2026-05-13T09:00:39.138608+00:00: External transfer remains non-countable; next import readiness depends on active-site sourcing, complete near-duplicate sequence search, and real representation controls before any external decision.
- 2026-05-13T10:03:45+00:00: External transfer remains non-countable; next import readiness depends on sourcing explicit active-site evidence, completing near-duplicate sequence search, and replacing feature-proxy representation controls before any external decision.
- 2026-05-13T11:04:16.318492+00:00: External transfer remains non-countable; next import readiness depends on sourcing explicit active-site evidence, completing near-duplicate sequence search, and running real representation controls before any external decision.
- 2026-05-13T12:05:19.086868+00:00: External transfer remains non-countable; next import readiness depends on primary literature/PDB active-site source review, complete near-duplicate sequence search, and replacing deterministic k-mer controls with real learned or structure-language representation controls before any external decision.
- 2026-05-13T12:55:17.737175+00:00: Post-M-CSA work now prioritizes a 5-10 candidate external-source pilot over additional abstract transfer gates or M-CSA-only tranche growth.
- 2026-05-13T13:02:54.457092+00:00: Agent work is now instruction-only redirected toward sequence/fold-distance holdout evaluation before external import or further abstract gates.
- 2026-05-13T14:08:28.620965+00:00: External transfer remains non-countable; next pilot readiness work should use the holdout metrics and learned-vs-heuristic disagreements to rank candidates before active-site source review, complete sequence search, selected-PDB override repairs, and full factory gates.
- 2026-05-13T16:04:03.062604+00:00: External pilot now has leakage-provenance ranking and no-decision review packets; next work should fill active-site and sequence evidence for selected candidates, not increase M-CSA-only count.
- 2026-05-13T16:37:11.331979+00:00: External pilot packets now have consolidated review-only source targets; next work should fill evidence decisions, not increase M-CSA count.
- 2026-05-13T17:47:33.256358+00:00: External transfer gate now fails fast on mixed-slice artifact paths across supplied gate artifacts.
- 2026-05-13T18:44:44.009443+00:00: External pilot review-decision path now fails if selected rows are ineligible, pilot decisions are completed prematurely, required review prerequisites are missing, or pilot dossier evidence blockers are stale.
- 2026-05-13T19:39:20.606270+00:00: External transfer gate input typing and CLI loading are now contract-based; next pilot work should fill real active-site and sequence evidence, not add generic gate count.
- 2026-05-13T20:51:07.000000+00:00: No M-CSA-only growth or external import; SPOF text-leakage hardening only
- 2026-05-13T22:04:23.805937+00:00: External transfer remains non-countable; current-reference sequence screen blocker is cleared, but complete UniRef/all-vs-all near-duplicate search and active-site evidence still block import.
- 2026-05-13T22:34:16.818554+00:00: Artifact-lineage SPOF hardening now includes the external sequence-holdout audit in row-level candidate lineage checks.
- 2026-05-13T23:52:26.926762+00:00: selected-pilot representation coverage is now a direct review-only gate input rather than stale mapped-control evidence
- 2026-05-14T00:43:19.772463+00:00: Label batch acceptance and scaling-quality audits now fail fast on mixed slice lineage before count/import decisions.
- 2026-05-14T01:50:53.503582+00:00: High-fan-in external pilot builders now fail fast on mixed-slice lineage before artifact write; selected-PDB ready overrides must match graph slice provenance.
- 2026-05-14T03:08:19.594666+00:00: Real sequence-distance holdout replaces proxy-only generalization signal; Foldseek/TM-score split now depends on coordinate materialization rather than tool availability alone.
- 2026-05-14T04:23:49.348241+00:00: External pilot sequence-search work now uses real MMseqs2 current-reference backend evidence before review decisions; import remains blocked by active-site, representation, broader duplicate-screening, review, and factory gates.
- 2026-05-14T11:07:34.295381+00:00: Unstaged selected-coordinate sidecar blocker is removed, but full TM-score split remains blocked by two missing selected structures and the unrun Foldseek split builder; selected-pilot active-site source status is classified but import remains blocked.
- 2026-05-14T12:34:37.036864+00:00: No project scope change; full TM-score split remains blocked by two missing selected structures and the unrun all-materializable Foldseek signal.
- 2026-05-14T14:10:21.275491+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded60 as a full holdout split.
- 2026-05-14T15:07:52.876846+00:00: Do not count external pilot evidence as success until terminal decisions and import criteria pass; report m_csa:372 and m_csa:501 as coordinate exclusions before any full TM-score holdout claim.
- 2026-05-14T16:15:30.855586+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded80 as a full holdout split.
- 2026-05-14T17:29:09.455993+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded100 as a full holdout split.
- 2026-05-14T19:04:21.441130+00:00: Foldseek target failure now has a concrete unapplied repair candidate and computed-subset projection; full holdout still requires regenerated sequence metrics and uncapped Foldseek split
- 2026-05-14T19:08:48.002960+00:00: Foldseek split repair now has an unapplied candidate sequence holdout copy; canonical holdout and downstream artifacts still need regeneration before any claim
- 2026-05-14T20:34:07.608397+00:00: Foldseek split repair now has an actual repaired expanded100 signal under the candidate holdout; canonical holdout remains unchanged and no full holdout claim is permitted.
- 2026-05-14T22:36:14.676450+00:00: Full TM-score holdout remains blocked by incomplete chunk aggregation new target-violating pairs and two coordinate exclusions
- 2026-05-14T23:22:21.551765+00:00: Full TM-score holdout remains blocked by target-violating completed chunks a timed-out chunk-2 range incomplete query coverage and two coordinate exclusions
- 2026-05-15T04:56:18.692987+00:00: Foldseek/TM-score work now uses observed high-TM structural clusters as partition constraints before verification chunks.
- 2026-05-15T15:32:34.144335+00:00: Cluster-first Foldseek verification now preserves real sequence-identity components before structural assignment; next work should rerun staged index 105 under round-13 readiness.
- 2026-05-15T16:41:11.445104+00:00: Round-16 cluster-first split is the active Foldseek handoff; next work should verify staged index 110 under round-16 readiness.
- 2026-05-15T18:36:22.139127+00:00: Round-22 cluster-first split is the active Foldseek handoff; next work should continue from staged index 119 under round-22 readiness.
- 2026-05-15T19:16:47.231347+00:00: Round-24 cluster-first split is the active Foldseek handoff; next work should continue single-query verification from staged index 123 under round-24 readiness.
- 2026-05-16T06:10:48.154425+00:00: Do not resume M-CSA round33 or staged-index-145 partition repair as normal progress; strict TM-diverse holdouts now move to external fold-diverse structural data before split assignment.
- 2026-05-16T06:25:28.404682+00:00: No scope change; latest pushed repo state supersedes stale prompt Foldseek continuation and keeps external structural pilot as next direct work
- 2026-05-16T07:15:23.155977+00:00: M-CSA strict pairwise TM <0.7 is closed/deferred for the curated M-CSA surface; strict TM-diverse holdouts move to external fold-diverse structural data.
- 2026-05-16T08:06:00.835318+00:00: Deferred external pilot rows are now routed to human/expert review packets; external import remains blocked by expert decisions broader duplicate screening and full factory gates.
- 2026-05-16T09:14:46.363953+00:00: Selected-pilot external structural clustering is now a review-only cache, not a train/test split or import authorization.
- 2026-05-16T10:14:24.266801+00:00: External fold-diverse structural work now starts from the all-30 UniProtKB/Swiss-Prot candidate surface rather than only the selected 10-row pilot; strict split claims remain blocked until pair-cache and review/import blockers are resolved.
- 2026-05-16T11:15:09.904197+00:00: External structural TM-diverse split assignment is now available only as review-only all-30 Swiss-Prot/AFDB evidence; import and benchmark claims remain blocked by terminal review decisions and broader duplicate/factory gates.
- 2026-05-16T21:00:19.989175+00:00: Q6NSJ0 boundary repair is now an import-safety adjudication; P34949 sugar-phosphate isomerase is the next staged review-only control, not an import.
- 2026-05-16T22:05:28.138975+00:00: P34949 and Q9BXD5 now have review-only import-safety adjudications; Q9BXD5 still preserves the representation near-duplicate holdout as an import blocker.
- 2026-05-17T02:10:05.048551+00:00: First external hard-negative import attempt is closed without count growth; next external work starts tranche-2 review-only candidates P33025 Q13907 P35914.
- 2026-05-17T04:14:25+00:00: Next hard-negative work should complete the missing current-countable pair cache for Q13087/sequence-clean rows, then continue UniRef-wide duplicate and terminal review gates before any import attempt.
- 2026-05-17T17:13:28.332690+00:00: leakage-risk closure complete; next milestone is infrastructure/artifact strategy before ePK or broad scale-up
- 2026-05-18T05:26:10.455344+00:00: ePK is ready for draft fingerprint specification but not positive-universe expansion; external hard negatives require scored ePK re-audit before any future counting claim.
- 2026-05-18T06:29:09.711385+00:00: ePK now has a review-only draft spec and local evidence audit but remains blocked from positive-universe expansion until scorer threshold external re-audit terminal review and factory gates pass.
- 2026-05-20T13:17:20.692201+00:00: ePK remains review-only; main loop pivoted to external mini-campaign and baseline comparison small wins
- 2026-05-20T14:14:08.715044+00:00: Main loop now has a non-ePK SDR readiness packet and a mini-campaign sequence baseline; Foldseek binary is restored but candidate coordinate sidecars are the active external-screen blocker.
- 2026-05-20T15:32:22.885905+00:00: Frozen prospective mini-campaign is now closed as terminal review-only duplicate evidence rather than blocked by missing coordinate sidecars.
- 2026-05-20T16:07:10.750132+00:00: Fresh ePK research-lane outputs are synthesized as review-only evidence; main loop should continue non-ePK small wins instead of ePK default work.
- 2026-05-20T16:21:03.279937+00:00: Main loop has concrete non-ePK family-readiness small wins and a frozen glycoside hydrolase control tranche for the next review-only experiment.
- 2026-05-20T17:10:02.023049+00:00: ePK lane synthesis now includes later pushed and dirty sibling-worktree evidence without copying production changes; PKA/CFTR mapping is research-lane-only if reopened.
- 2026-05-20T17:16:23.980051+00:00: Glycoside hydrolase remains no-go for production fingerprint expansion; Q6NSJ0 is needs-review boundary evidence, not a label import candidate.
- 2026-05-20T17:19:03.090362+00:00: Modern baseline comparison now exists for the glycoside tranche without authorizing production scoring or import.
- 2026-05-20T18:22:16.234314+00:00: Main loop added a source-gap terminal mini-campaign plus two non-ePK readiness packets; no registry import or production fingerprint path opened.
- 2026-05-20T19:12:53.814979+00:00: Fresh ePK lane output adds review-only peptide positives and product-state controls but preserves the no-go production decision.
- 2026-05-20T19:49:09.571418+00:00: Six-family non-ePK small-win queue is now closed as review-only no-go evidence; next main loop should source a genuinely new external mini-campaign or choose a new family packet.
- 2026-05-20T20:13:02.164962+00:00: ePK synthesis now includes terminal-gamma lead/control stress and same-author-chain pressure while preserving no-go production scope.
- 2026-05-20T20:55:03.996810+00:00: Main loop closed a new prospective external methyltransferase terminal-failure win, added ASKHA readiness plus a frozen ASKHA-vs-ATP-family tranche, and kept new ePK lane evidence research-only.
- 2026-05-20T22:19:09.281826+00:00: ePK late-lane synthesis is integrated as review-only evidence with no production scorer threshold label import registry edit or fingerprint expansion.
- 2026-05-20T22:44:16.389654+00:00: Main loop stayed off ePK audit churn and advanced non-ePK visible small wins.
- 2026-05-21T00:18:48.662111+00:00: ePK remains review-only no-go and out of main-loop production scope; future scorer dry-run belongs only in isolated research lane.
- 2026-05-21T00:27:03.666400+00:00: External PLP mini-campaign is review-only; current PLP lane presence is not a mechanism-match or import claim without source-free geometry and factory gates.
- 2026-05-21T00:35:13.353330+00:00: all non-ePK ATP-family readiness slots closed review-only no-go
- 2026-05-21T00:41:53.519062+00:00: flavin monooxygenase external mini-campaign remains review-only and not import-ready
- 2026-05-21T00:44:11.610704+00:00: modern baseline rollup is review-only and not a production/import benchmark
- 2026-05-21T00:49:00.721874+00:00: heme peroxidase external mini-campaign remains review-only and not import-ready
- 2026-05-21T00:51:14.465122+00:00: post-heme baseline rollup remains review-only with no superiority or import claim
- 2026-05-21T00:58:14.196100+00:00: no registry import fingerprint edit production scoring threshold or artifact migration upload/removal
- 2026-05-21T01:19:56.798534+00:00: ePK remains review-only no-go and out of main-loop production scope after fresh remote branch synthesis.
- 2026-05-21T01:27:27.260565+00:00: serine hydrolase external mini-campaign remains review-only and not import-ready
- 2026-05-21T01:31:38.491051+00:00: metal phosphatase external mini-campaign remains review-only and not import-ready
- 2026-05-21T01:35:50.770123+00:00: flavin dehydrogenase external mini-campaign remains review-only and not import-ready
- 2026-05-21T01:41:08.373902+00:00: cobalamin radical external surface is terminal review-only blocker evidence, not a scored mini-campaign
- 2026-05-21T01:47:47.464485+00:00: all current production fingerprint lanes now have either a review-only external mini-campaign or a terminal source-surface blocker
- 2026-05-21T01:50:11.872301+00:00: modern baseline comparison is now explicit across the current fingerprint external surfaces
- 2026-05-21T01:55:41.795664+00:00: next exact external experiment is source-free sidecar materialization and duplicate screening for 14 frozen rows only
- 2026-05-21T02:00:27.449389+00:00: fresh dirty sibling ePK outputs reinforce no-go production scope and do not resume ePK main-loop work
- 2026-05-21T02:02:02.049578+00:00: wrapped after minute 48 with external small-win artifacts pushed and ePK kept review-only
- 2026-05-21T02:49:40.198593+00:00: External deepening now has a source-separated metal-phosphatase blocker packet; next exact step is a resumable or chunked current-countable structural duplicate screen for the selected 7 rows.
- 2026-05-21T02:52:33.159296+00:00: wrap validation keeps the metal-phosphatase blocker packet review-only and ready for the next duplicate-screen experiment
- 2026-05-21T04:01:42.976219+00:00: External deepening now has serine and flavin source-separated terminal blocker packets after the metal packet; next work is current-countable structural duplicate screening not row breadth.
- 2026-05-21T12:24:08.992494+00:00: Flavin dehydrogenase deep packet is now terminal duplicate/leakage evidence; ePK remains review-only no-go and main loop should not open new broad external breadth.
- 2026-05-21T14:06:11.129182+00:00: External deepening produced a mostly terminal heme packet without new broad row breadth; ePK remains review-only no-go.
- 2026-05-21T15:03:50.814880+00:00: Existing frozen external rows were converted to terminal decisions or exact blockers without new broad row breadth; FMO mapping narrowed the next blocker to source-free geometry scoring plus full-current duplicate screening.
- 2026-05-21T16:08:32.602022+00:00: External deepening stayed on frozen FMO rows: two more rows reached terminal duplicate/leakage rejection and the two unresolved rows now have exact subchunk-level blockers.
- 2026-05-21T17:08:18.443673+00:00: FMO duplicate-screen blocker is narrowed from chunk000/chunk001 uncertainty to chunks003-013 only; no new external breadth or import path was opened.
- 2026-05-21T18:12:47.873454+00:00: Existing frozen rows were deepened into terminal duplicate/leakage decisions or exact active-site blockers without adding broad external breadth.
- 2026-05-21T19:37:19.047962+00:00: Recovered stale-lock work converts the final serine blocker to terminal duplicate/leakage rejection and records PLP as an exact extractor blocker without registry import or artifact migration.
- 2026-05-21T21:16:37.365926+00:00: PLP blocker converted to terminal review-only duplicate/leakage packet; SDR remains review-only blocked on source-free NAD(P) and catalytic-axis geometry.
- 2026-05-21T23:19:22.103465+00:00: No new external rows; deepened existing frozen metal-phosphatase decisions and synthesized ePK handoffs once without returning ePK to main-loop default
- 2026-05-22T00:21:07.387970+00:00: Closed existing frozen metal and serine blockers without adding broad external rows or opening imports.
- 2026-05-22T01:48:29+00:00: Recovered dirty work continues existing frozen external deepening with no new external row freeze.
- 2026-05-22T02:11:28+00:00: Added a supplemental duplicate-screen rerun artifact instead of replacing the canonical terminal packet from the pushed closure commit.
- 2026-05-22T02:17:12+00:00: Added an import-blocker matrix rather than opening new external breadth.
- 2026-05-22T03:34:56.636211+00:00: Added import-gate evidence, sequence-duplicate terminal closures, and a non-countable blocker queue from existing frozen rows only.
- 2026-05-22T05:15:55.239970+00:00: Closed all queued source-free geometry/structure blockers; remaining external deep blockers are import-gate policy/payload only.
- 2026-05-22T05:23:06.284991+00:00: Converted remaining import-gate blocker surface into a no-import dry run without opening label import.
- 2026-05-22T05:25:41.522048+00:00: Import-gate readiness advanced without import: UniRef duplicate evidence is now clear for all six review-ready rows, but seed-fingerprint import remains policy/gate blocked.
- 2026-05-22T08:48:17.767316+00:00: Advanced import-gate readiness for existing review-ready rows without adding external breadth or importing labels.
- 2026-05-22T08:49:45.493927+00:00: Import-gate readiness advanced without import: seed-fingerprint policy dry run has an exact current-682 adapter blocker and metal phosphatase rows have exact phosphate-specific missing evidence.
- 2026-05-22T08:51:15.302701+00:00: Converted the metal-row phosphate/substrate specificity blocker into an exact source-free evidence packet.
- 2026-05-22T10:20:02.906647+00:00: Closed the remaining frozen serine-hydrolase rows without adding external breadth; P15776 is review-ready but not import-ready.
- 2026-05-22T10:31:38.361386+00:00: Advanced seven-row review-ready import-gate readiness without adding external breadth or importing labels.
- 2026-05-22T11:35:58.020005+00:00: Closed the current-682 seed-payload adapter blocker without importing labels or adding external breadth.
- 2026-05-22T13:05:41.322034+00:00: Second PLP packet deepens existing frozen rows only; no seed-fingerprint import path opened.
- 2026-05-22T13:08:53.551713+00:00: Final wrap only; no additional external rows or label changes.
- 2026-05-22T15:49:13.822899+00:00: No new broad external rows; remaining external queue is human review plus metal phosphate specificity.
- 2026-05-22T16:29:06.133933+00:00: External no-breadth queue is now human-review-only; no new external mini-campaign should start before human action or a new bounded control experiment.
- 2026-05-22T18:05:27.783477+00:00: No new broad external rows; PyMOL review cockpit and non-ePK family readiness remain review-only
- 2026-05-22T18:35:34.824679+00:00: No new broad external rows; SDR blocker is exact and external queue is human-review-ready only
- 2026-05-22T19:42:57.546947+00:00: NADP redox family fallback is now blocked on holo/local NADP evidence or source-free specificity controls, not another broad row freeze.
- 2026-05-22T20:37:21.159775+00:00: M-CSA PyMOL readiness now has 51 human-review-ready rows; next useful step is human decisions before more machinery.
- 2026-05-22T21:32:20.016660+00:00: External review-ready rows should not trigger more automated breadth by default; next action is human review or bounded no-breadth readiness only.
- 2026-05-22T23:08:25.796026+00:00: Final wrap only; no label import registry edit artifact removal or new external breadth.
- 2026-05-23T18:03:35.801938+00:00: Closed the M-CSA 22-row positive follow-up as review-only import-readiness/blocker evidence without mutating canonical registries.
- 2026-05-23T19:56:43.019061+00:00: M-CSA clean9 is imported; next M-CSA work is explicit accept decisions for held override and m_csa771 previews before any more imports.
- 2026-05-23T20:13:13.233624+00:00: No new M-CSA import work was opened because the requested tranche is already canonical and remaining rows are human-decision blocked.
- 2026-05-24T03:55:03.938943+00:00: Closed the current-evidence loop for the nine remaining Vivek-reviewed M-CSA follow-up blockers without importing labels.
- 2026-05-24T04:58:59.872641+00:00: Decision-trace signal is now reusable and the exact-mapping blocker class has a one-row actionable repair target without reopening the terminal nine holds.
- 2026-05-24T05:54:43.004965+00:00: Built only the exact pinned 66-row needs_more_evidence matrix and kept broad 1025 review debt enrichment-only.
- 2026-05-24T18:47:30.176583+00:00: Added review-only navigation and worksheets without label import import previews registry edits fingerprint edits scoring changes or source artifact mutation.
- 2026-05-24T18:53:06.309748+00:00: Review-support surface is now a navigation layer only; no M-CSA decisions or imports were opened while Vivek is away.
- 2026-05-24T18:53:19.546556+00:00: Hardened only temporary MMseqs workdir handling to avoid concurrent digest-path collisions; no scoring threshold ontology label or fingerprint semantics changed.
- 2026-05-25T09:13:01Z: Target 0 completed as a frozen caveat artifact; Target A remains blocked on exact sequence coverage rows.
- 2026-05-25T14:36:49.637815+00:00: Sequence-NN remains fail-closed until the repaired current702 split covers all 702 labels; no PLM or learned baseline work was started.
- 2026-05-25T15:10:30.958833+00:00: Current702 sequence-NN is unblocked and reported with deterministic amino-acid-only baseline artifacts; PLM and learned representation work remain outside this prompt.
- 2026-05-26T04:27:02.589694+00:00: Wave 1 representation results are now framed as diagnostic structural-neighborhood evidence, not a bigger-model leaderboard.
- 2026-05-27T10:15:26Z: Packet 1 and Wave 1 are now read through additive review-only addenda rather than stale readiness/canary advertising.
- 2026-05-27T13:12:54.482909+00:00: Closed evaluation-design evidence only with review-only Foldseek chunk artifacts and no registry scoring threshold import model or representation changes.
- 2026-06-03T09:54:04.655478+00:00: Active Lever 2/3/4 remains review-gated; derived templates are patch aids only and not source-of-truth decisions.
- 2026-06-03T10:52:23.444858+00:00: Active Lever 2/3/4 now has a hash-preserving source-decision intake preflight between review packets and application gates.
- 2026-06-03T11:23:19.905443+00:00: Active Lever 2/3/4 application gates now require explicit reviewed statuses and approval booleans before follow-on materialization/application gates can open.
- 2026-06-03T16:23:45.947867+00:00: Lever 3 automatic scoring is exhausted under current proxy axes; a reviewed source decision or pre-registered new train/cal-only proxy-axis contract is required before more scoring.
- 2026-06-03T17:56:13.579427+00:00: Lever 3 active-site-count proxy axis is fully scored but not closure-sufficient; do not rerun the global fixed-threshold proxy audit from the partial/base-blocked surface.
- 2026-06-03T19:56:36.530027+00:00: train/cal-only Lever 3 protein-only fold topology residual after AFDB locus repair exhausted
- 2026-06-03T23:39:07+00:00: Event-axis signoff is no longer the Lever 2 blocker; locator coverage and heldout-safe application-surface policy are now the remaining Lever 2 blockers.
- 2026-06-04T00:37:12.914214+00:00: Lever 2 partial source-free surface is review-ready but fail-closed until explicit operating-contract decision.
- 2026-06-04T01:43:55.363807+00:00: Lever 2 partial source-free surface is no longer a pending read; it is a read-once nondeployable result.
- 2026-06-04T15:52:38.463795+00:00: Lever 3 only; no labels, registries, ontologies, heldout splits, imports, or threshold changes
- 2026-06-04T16:54:35.141959+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds or threshold tuning changed
- 2026-06-04T17:54:27.719250+00:00: Lever 3 only; no threshold changes, heldout tuning, row scoring, coordinate staging, labels, registries, ontologies, imports, or source decisions changed.
- 2026-06-04T18:22:07.166395+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging or source decisions changed
- 2026-06-04T20:51:00.471108+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting or source decisions changed
- 2026-06-04T21:37:20.235148+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting or source decisions changed.
- 2026-06-04T22:26:32.470910+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting or experimental PDB deployment shortcuts changed.
- 2026-06-04T23:22:40.005804+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions secret values or experimental PDB deployment shortcuts changed.
- 2026-06-05T00:25:15.243472+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions secret values or experimental PDB deployment shortcuts changed.
- 2026-06-05T01:33:57.855493+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions secret values or experimental PDB deployment shortcuts changed.
- 2026-06-05T02:27:05.027678+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions secret values or experimental PDB deployment shortcuts changed.
- 2026-06-05T03:33:38.753039+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions secret values or experimental PDB deployment shortcuts changed.
- 2026-06-05T05:24:07.185327+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions secret values provider calls or experimental-PDB deployment shortcuts changed.
- 2026-06-05T06:24:37.090381+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T07:54:22.667696+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T08:53:14.250032+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T09:52:04.608209+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T10:52:49.778990+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T11:52:16.895985+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T12:29:58.962873+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T13:51:57.851542+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T14:36:17.881700+00:00: Lever 3 only; no labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting source decisions provider calls secret values or experimental-PDB deployment shortcuts changed.
- 2026-06-05T15:08:04.783030+00:00: Lever 3 finalization only; no current-family counteraxis hunting labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting provider calls or source decisions changed.
- 2026-06-05T16:06:56.986922+00:00: Lever 3 finalization verification only; no current-family counteraxis hunting labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting provider calls or source decisions changed.
- 2026-06-05T17:06:58.568415+00:00: Lever 3 finalization verification only; no current-family counteraxis hunting labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting provider calls or source decisions changed.
- 2026-06-05T19:06:13.363198+00:00: Lever 3 finalization verification only; no current-family counteraxis hunting labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting provider calls source decisions or P07658 no-credential retries changed.
- 2026-06-05T20:05:21.984184+00:00: Lever 3 finalization verification only; no current-family counteraxis hunting labels registries ontologies imports heldout splits production thresholds threshold tuning row scoring coordinate staging model fitting provider calls source decisions or P07658 no-credential retries changed.
- 2026-06-08T13:53:00.862088+00:00: Converted uncertainty to non-importing terminal states; no promotion/import batch started.
- 2026-06-08T14:19:32.103369+00:00: Self-stop reconciliation only; no duplicate artifact, label import, registry edit, ontology edit, split edit, model change, threshold change, or promotion batch started.
- 2026-06-09T03:49:20.085384+00:00: Defense-ledger artifact and report only; no registry import ontology split threshold model weight production locator sidecar or heldout tuning edit.
- 2026-06-09T03:50:15.392215+00:00: Preview-only import-review preflight; no production registry import ontology split threshold model weight coordinate download or label import changed.
- 2026-06-09T05:25:43.402284+00:00: Preview and repair artifacts only; no production registry import ontology split threshold model weight coordinate download or label import changed.
- 2026-06-09T05:54:43.128126+00:00: Read-only external scaleout shard only; no production registry import ontology split threshold model weight coordinate download or label import changed.
- 2026-06-09T13:24:24.360224+00:00: Preview and repair artifacts plus review-only coordinate and locator sidecars only; no production registry import ontology split threshold model weight or label import changed.

## Automation run - ce-nad-glyco-floor-expansion (2026-06-12T23:09:11Z)
- STARTED_AT: `2026-06-12T23:09:11Z`
- STARTED_LOCAL: `Fri Jun 12 18:09:11 CDT 2026`
- Status: starting; handoff and automation memory read; acquiring automation lock next.

- 2026-06-12T23:27:14Z: SAM methyltransferase apply completed; appended 250 bronze; external bronze 3340 -> 3590; combined 4042 -> 4292; frozen current702 sha unchanged. Running post-apply validation/audit next.

- 2026-06-12T23:34:16Z: Validation complete: targeted pytest 82 passed; validate passed (12 source records, 15 fingerprints, 18 ontology families, 702 labels); git diff --check and JSON parse checks clean; SAM guardrail spot check passed. Elapsed seconds: 1505.

## Automation run start - 2026-06-13T01:57:51Z

- STARTED_AT: `2026-06-13T01:57:51Z`
- STARTED_LOCAL: `Fri Jun 12 20:57:51 CDT 2026`
- Automation ID: `ce-nad-glyco-floor-expansion`
- Initial lane from latest handoff: `molybdopterin_oxidoreductase` mechanism-handle scout before any 20fp wiring/apply.

- Lock acquired: `.git/catalytic-earth-automation.lock` at `2026-06-13T01:58:17Z`; proceeding with origin sync and molybdopterin scout.

- Molybdopterin apply succeeded at `2026-06-13T02:21:10Z`: external bronze `4202 -> 4409` (+207), combined `4904 -> 5111`; frozen current702 sha unchanged `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

- Validation complete at `2026-06-13T02:26:52Z`: focused pytest `111 passed`; leakage prereg/import-gate `10 passed, 171 deselected`; validate passed (12 source, 20 fingerprints, 23 ontology families, 702 labels); JSON parse checks passed.

- Copper mechanism-handle scout completed at `2026-06-13T02:29:20Z`: 80 entries, 0 fetch failures, Rhea 78/80, redox text 77/80, copper feature/ligand 31/80, explicit copper cofactor 20/80; no registry/ontology change.

- Closeout integrity checks passed at `2026-06-13T02:35:47Z`: targeted pytest `111 passed`; leakage prereg/import-gate `10 passed, 171 deselected`; CLI validate passed; JSON parse checks passed; `git diff --check` passed. Ready for fetch, commit, push, and release-lock after the required productive block window.

- Additional import/transfer-scope coverage passed at `2026-06-13T02:37:23Z`: `PYTHONPATH=src pytest tests/test_external_annotation_anchored_import.py tests/test_transfer_scope.py -q` -> `133 passed` after updating the stale 20fp inverse-gate fixture expectation for `molybdopterin_oxidoreductase`.

## Automation run start - ce-nad-glyco-floor-expansion

- STARTED_AT: `2026-06-13T03:58:23Z`
- STARTED_LOCAL: `Fri Jun 12 22:58:23 CDT 2026`
- Initial lane: latest handoff supersedes older P450 prompt; proceeding with ATP amide ligase scout unless gates redirect.

## Automation run 2026-06-13T04:59:16Z

- Automation ID: ce-nad-glyco-floor-expansion
- STARTED_AT: `2026-06-13T04:59:16Z`
- STARTED_LOCAL: `Fri Jun 12 23:59:16 CDT 2026`
- Status: lock acquisition in progress.

## Automation run 2026-06-13T05:53:52Z

- Automation ID: ce-nad-glyco-floor-expansion
- STARTED_AT: `2026-06-13T05:53:52Z`
- STARTED_LOCAL: `Sat Jun 13 00:53:52 CDT 2026`
- Initial lane: latest handoff directs guarded `zinc_lyase_hydratase` 26fp setup/apply if mechanism-first gates pass.
- Status: lock acquisition in progress.

## Automation run 2026-06-13T10:31:51Z

- Automation ID: ce-nad-glyco-floor-expansion
- STARTED_AT: `2026-06-13T10:31:51Z`
- STARTED_LOCAL: `Sat Jun 13 05:31:51 CDT 2026`
- Initial lane: latest handoff directs strict `pfka_phosphofructokinase` 32fp setup/apply if mechanism-first gates pass.
- Status: lock acquisition in progress.
