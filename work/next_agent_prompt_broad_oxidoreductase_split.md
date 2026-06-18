# Next-agent task: add a HIGH-SUPPLY oxidoreductase fingerprint family

You are continuing the Catalytic Earth scaling work. The goal is to grow the **combined**
mechanism-label count toward 10k by adding a NEW, coherent, **high-supply** mechanism fingerprint
family and sourcing its first reviewed-Swiss-Prot bronze tranche — following the exact, proven
"add-a-family" recipe below. **Do not touch the frozen `current702` benchmark.**

## Current state (read these first)

- `docs/project_state.md`, `docs/decision_log.md`, `docs/scaling_plan_to_10k.md` (top entries are the
  most recent).
- Combined labels: **8906** = 702 frozen + 8204 expansion bronze. **49** live fingerprints.
- Frozen `current702` registry sha must stay `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`
  (every apply asserts this; never write `data/registries/curated_mechanism_labels.json`).
- Three families were just added this way — **study one end-to-end as your template**:
  `git show bc218056` (metallo_beta_lactamase), `git show 4b169cda` (aminoglycoside_acetyltransferase),
  `git show 51a0223b` (aldo_keto_reductase).

## Why this task (not another narrow family)

Narrow families are nearly exhausted: metallo_beta_lactamase yielded only **4** novel reviewed rows.
The remaining ~1094 gap to 10k needs families with **hundreds** of novel reviewed entries. Broad
oxidoreductase (EC 1.x) pools are the supply; the evidence-handle-expansion recon
(`artifacts/v3_evidence_handle_expansion_current702_20260616_run0310_pre_lane.json`) says to **split
them by EC-subclass into capped, coherent lanes** — not source one giant bucket.

## Step 0 — pick the family (measure supply, confirm coherence)

1. Pick a coherent EC 1.x subclass with a single clean catalytic mechanism that is NOT already a
   fingerprint (run `validate` to list the 49; avoid overlap with: `nad_p_dehydrogenase`,
   `short_chain_dehydrogenase_reductase`, `aldo_keto_reductase`, `aldehyde_dehydrogenase`,
   `flavin_dehydrogenase_reductase`, `flavin_monooxygenase`, `cytochrome_p450_monooxygenase`,
   `heme_peroxidase_oxidase`, `copper_oxidoreductase`, `molybdopterin_oxidoreductase`,
   `non_heme_iron_2og_dioxygenase`, `manganese_iron_superoxide_dismutase`).
   Good candidates to evaluate (verify, don't assume): thioredoxin/glutathione-disulfide
   oxidoreductases (EC 1.8.1.*), peroxiredoxin/glutathione peroxidase (EC 1.11.1.*, distinct from the
   heme peroxidase fingerprint), FAD/FMN flavoprotein subclasses not covered by the existing flavin
   fingerprints, or a clean EC 1.5.* / 1.6.* / 1.17.* subclass.
2. Measure reachable supply with `catalytic_earth.adapters.fetch_uniprot_query_count` (and/or run the
   high-yield lane factory: `PYTHONPATH=src python scripts/build_high_yield_family_lane_factory.py`).
   Require a corroborator query that returns **>= ~150 reviewed** entries so the lane fills its cap.
3. Define the disambiguation **discriminator** up front: which existing fingerprint(s) is it
   reaction-confusable with, and what non-leakage signal separates them (cofactor identity, a specific
   reaction-center bond change, a family/name handle)? EC is SCOPE ONLY, never a predictive feature.

## Step 1 — the add-a-family recipe (mirror `git show bc218056` exactly)

1. **Fingerprint record** → append to `data/registries/mechanism_fingerprints.json` (write with
   `json.dumps(d, indent=2)+"\n"`). Required keys: `id, name, enzyme_space, active_site_signature`
   (list of `{role, residue, constraints}`), `cofactors, reaction_center` (`{bond_changes,
   chemical_operation}`), `substrate_constraints, evidence_features, counterevidence_features,
   uncertainty_axes, seed_examples, deploy_missing_active_site_context`.
2. **Ontology family** → insert into `data/registries/mechanism_ontology.json` `families`
   (`{id, name, parent_id, fingerprint_ids, v2_split_note, family_boundary_guardrails}`); put it under
   a sensible parent (e.g. `nicotinamide_redox`, `hydrolysis`, or a new mechanism child).
3. **Deploy-missing context** → add an entry to `DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT` in
   `src/catalytic_earth/external_annotation_anchored_import.py`.
4. **Disambiguation engine** `src/catalytic_earth/external_cofactor_ec_disambiguation.py`:
   - add token lists (family-text / reaction / boundary), an EC constant, and the evidence signals
     (`<fp>_family_text`, `<fp>_<cofactor>_context`, `<fp>_reaction`, `<fp>_boundary_signal`,
     `non_<fp>_scope_side_ec`);
   - register those signals in the evidence dict;
   - add the `DISAMBIGUATION_RULES` entry;
   - **CRITICAL**: add `and not c["<fp>_family_text"]` (or the right exclusion) to every existing rule
     it would otherwise collide with — exactly how `nad_p_dehydrogenase` excludes AKR,
     `coa_acyltransferase` excludes AAC, and `metallo_amidohydrolase_deaminase` excludes the
     beta-lactam MBL rows. Confirm "exactly one rule fires" for the new positive and that confusable
     neighbors still classify correctly;
   - add `<fp>_family_text` to the `domain_or_family_profile` axis list (~line 2900);
   - add a cofactor-provenance branch in `_synthesize_cofactor_provenance`.
5. **Sourcing module** `src/catalytic_earth/<fp>_sourcing.py` — copy
   `src/catalytic_earth/aldo_keto_reductase_sourcing.py`; change `FAMILY`, the scope query, the 3 lane
   queries, and the descriptive strings/guardrail keys.
6. **Runner** `scripts/source_<fp>_family.py` — copy `scripts/source_aldo_keto_reductase_family.py`;
   change the imports, defaults, and egress-probe query.
7. **Tests**: `tests/test_<fp>_sourcing.py` (copy `tests/test_aldo_keto_reductase_sourcing.py` with
   family-specific fake rows + boundary controls); add positive/negative cases to
   `tests/test_external_cofactor_ec_disambiguation.py`.

## Step 2 — leakage re-registration (universe 49 -> 50)

1. Create `artifacts/v3_external_hard_negative_next_tranche_preregistration_50fp_1025.json` from the
   49fp one: set `fingerprint_universe` to the live sorted ids, `ontology_version_at_decision` =
   `label_factory_v1_50fp`, `supersedes` = the 49fp filename, `supersedes_ontology_version` =
   `label_factory_v1_49fp`, a `re_freeze_reason`, and a fresh `created_at`.
2. Bump `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` in `src/catalytic_earth/labels.py` to
   `label_factory_v1_50fp`.
3. Add `EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_50FP_ARTIFACT` in
   `src/catalytic_earth/transfer_scope.py`.
4. In `tests/test_leakage_closure.py`: add a `test_50fp_..._is_frozen_for_live_universe`, change the
   49fp test to `test_49fp_..._now_superseded_by_50fp`, and point the import-gate happy-path test at
   the 50fp artifact.

## Step 3 — wire the lane factory, then source + apply

1. In `src/catalytic_earth/high_yield_family_lane_factory.py`, set the family `_spec`'s
   `existing_fingerprint_id`, `current_runner`, `oos_preregistration_required=False`,
   `source_wall_rule_status="implemented_new_fingerprint_runner"`.
2. `PYTHONPATH=src python scripts/source_<fp>_family.py --apply --fetch-timeout-seconds 30 \
   --max-records-per-lane 300 --out artifacts/v3_<fp>_sourcing_preview_current702_<date>.json \
   --report work/<fp>_sourcing_current702_<date>.md`.
   Verify the printed frozen sha is unchanged before AND after apply.

## Step 4 — audits, baselines, full suite, commit

1. `build-coverage-redundancy-audit` and `build-novelty-admission-gate-audit` → confirm holes `[]`,
   floor deficit 0, over-cap unchanged (only `metal_dependent_hydrolase`).
2. Update the registry-count baselines to the new combined / expansion / seed_labels:
   `tests/test_coverage_redundancy_audit.py`, `tests/test_novelty_admission_gate.py`,
   `tests/test_mechanism_representation_loop.py`, `tests/test_bronze_silver_promotion_preview.py`,
   `tests/test_cli.py` (`current_positive_fingerprint_count` = 50), and the sorted
   `missing_current_fingerprint_ids` list in `tests/test_transfer_scope.py`
   (`test_external_pilot_sdr_redox_import_safety_repairs_representation_only`) — add the new id
   alphabetically.
3. **Representation-loop confusability** (`tests/test_mechanism_representation_loop.py::
   test_build_on_real_registry_is_leakage_safe`): if the new family shares a reaction-center class
   with an existing one and has enough rows, the existing family's per-fingerprint self-consistency
   can collapse and overall LOO can drop. FIRST compute the actual values, then document the collapse
   honestly (it is the cost of confusable families — do NOT add fold/name leakage), adjusting the
   per-family assertion and, if needed, the overall-LOO floor (currently `> 0.70`) with a comment.
4. `PYTHONPATH=src python -m catalytic_earth.cli validate` and `git diff --check`.
5. Full suite: `PYTHONPATH=src python -m unittest discover -s tests`. **Known PRE-EXISTING env
   failures (6, NOT regressions):** the web container has no numpy/torch/esm2/mmseqs, so
   `test_active_site_supervised_smoke`, `test_low_calibration_support_is_flagged`,
   `test_builds_clean_label_set_and_dense_head_predictions`,
   `test_builds_presence_label_balance_and_kmer_probe`, `test_builds_train_cal_only_channel`, and
   `test_current_1000_holdout_artifact_is_pinned` fail. Anything else is yours to fix.
6. Write an apply-summary artifact + progress-log entry + top-of-file updates to
   `docs/decision_log.md`, `docs/project_state.md`, `docs/scaling_plan_to_10k.md` (mirror the existing
   2026-06-17 entries). Commit on branch `claude/festive-albattani-60le4t` and
   `git push -u origin claude/festive-albattani-60le4t`. Do NOT open a PR unless asked.

## Hard rules

- Never edit `data/registries/curated_mechanism_labels.json` (frozen 702), production scoring,
  thresholds, or imports beyond the expansion-bronze append the runner performs.
- EC / protein name / UniProt prose / source annotation / curated mechanism text / target family lane
  are `excluded_context` — never predictive features. Each appended label must keep
  `predictive_evidence: []` and carry >= 1 real mechanism axis.
- Caps: 150 (chemistry-confusable) / 250 (clean). Never push a family over cap.
