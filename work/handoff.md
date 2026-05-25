# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval and label-factory quality
automation. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, 475-, 500-, 525-, 550-, 575-,
600-, 625-, 650-, 675-, 700-, 725-, 750-, 775-, 800-, 825-, 850-, 875-,
900-, 925-, 950-, 975-, and 1000-entry
curated slices. The 500-entry and larger
slices are countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
702 countable labels. Review-state registries preserve pending
`needs_expert_review` rows separately so unresolved evidence gaps do not count
as benchmark labels.

## Repository

Local path:

```text
/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth
```

GitHub:

```text
https://github.com/VivekVardhanArrabelli/catalytic-earth
```

## Operating Rules

1. Acquire `.git/catalytic-earth-automation.lock` before work; the tested
   `automation-lock` CLI command can enforce the same atomic lock rules.
2. Sync with `git fetch origin` and `git pull --ff-only origin main`.
3. Read `README.md`, `work/scope.md`, `work/status.md`, and this file.
4. Run `PYTHONPATH=src python -m unittest discover -s tests`.
5. Work productively until 50 elapsed wall-clock minutes, then wrap.
6. During wrap, update stale docs, log measured time, regenerate status,
   commit, push, verify `HEAD == origin/main`, and release the lock only when
   the worktree is clean.

## Current Handoff

### 2026-05-25T12:35Z Sequence-NN Split Blocker Sharpened

This run acquired `.git/catalytic-earth-automation.lock`, fetched
`origin/main`, and confirmed the local branch was already up to date before
edits. Scope stayed limited to the current702 sequence-nearest-neighbor
baseline gate: no labels were imported, no production fingerprints, ontology,
scoring, thresholds, or curated labels were edited, no PLM embeddings were
computed, and no model training was performed.

Updated artifact:

```text
artifacts/v3_sequence_nn_eval_contract_compliance_current702_20260525.json
```

The sequence-NN compliance artifact still blocks before predictions or metrics,
as required by the frozen split contract, because the repaired current702 split
artifact has rows for 698/702 current labels. The blocker is now row-level
explicit under `split_assignment_blocker`: the missing split rows are all
out-of-scope labels with repaired sequence coverage, and the artifact records
their benchmark roles, accessions, sequence SHA-256 values, sequence coverage
statuses, and OOS diagnostic roles.

Exact missing split rows:

```text
m_csa:204       accession=P10746 sequence_sha256=01062407ddcb2c98548de1d956dafa8c5c18aca14ac61c0d36c635e235eb3e73
uniprot:P06744 accession=P06744 sequence_sha256=272fc149643cdf85e7bdf8be908a732f796d89ed1c62fc229e576e042c290983
uniprot:P78549 accession=P78549 sequence_sha256=2c784d6c37a7abb4d87ea1451073f522c6c9f253335f4d71a29fd87aee8fd81f
uniprot:Q3LXA3 accession=Q3LXA3 sequence_sha256=ba204dee5f637838bfca90fe54177d0bd318dd29b1063708638ce74a6fe2ed4e
```

Contract SHA-256 retained by the sequence-NN artifacts:

```text
c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50
```

Underpowered metric cells were not evaluated because the run stopped before
metric reporting. Next action: repair/regenerate the current702 split so all
702 label-manifest rows have a partition, then rerun
`PYTHONPATH=src python -m catalytic_earth.cli build-sequence-nn-baseline` to
permit MMseqs nearest-neighbor predictions and contract-governed metrics.

### 2026-05-25T11:29Z Sequence-NN Baseline Preflight Blocked On Split Coverage

This run acquired `.git/catalytic-earth-automation.lock`, fetched `origin`, and
fast-forward checked `origin/main` at
`9a8dd8b77cf453674796c4a7ce460fd37bdeab0d` before edits. Scope stayed limited
to the current702 sequence-nearest-neighbor baseline gate: no labels were
imported, no production fingerprints, ontology, scoring, thresholds, or curated
labels were edited, no PLM embeddings were computed, and no model training was
performed.

Push note: the first `git push origin main` attempt against the HTTPS remote
failed exactly with `fatal: could not read Username for 'https://github.com':
Device not configured`. The existing deploy-key SSH path was then verified with
`git ls-remote`, and the committed work was pushed successfully to
`git@github.com:VivekVardhanArrabelli/catalytic-earth.git`.

New command:

```text
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-nn-baseline
```

New artifacts:

```text
artifacts/v3_sequence_nn_label_manifest_current702_20260525.json
artifacts/v3_sequence_nn_eval_contract_compliance_current702_20260525.json
```

Contract SHA-256 cited by both sequence-NN artifacts:

```text
c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50
```

Headline result: the label manifest covers all 702 labels and repaired sequence
records, but sequence-NN predictions and metrics were not emitted. The
compliance gate fail-closes because the repaired split artifact has split rows
for 698/702 labels. Missing split assignments are exactly:

```text
m_csa:204
uniprot:P06744
uniprot:P78549
uniprot:Q3LXA3
```

The repaired sequence manifest covers those four rows, so the blocker is split
partition coverage rather than sequence coverage. Underpowered metric cells were
not evaluated because the run stopped before metric reporting. Next action:
repair/regenerate the current702 sequence split so every label-manifest row has
a partition, then rerun `build-sequence-nn-baseline` to allow MMseqs
nearest-neighbor predictions and contract-governed metrics.

### 2026-05-25T11:16Z Mechanism Prediction OOS/Diversity Contract Frozen

This run acquired `.git/catalytic-earth-automation.lock`, fetched `origin`, and
fast-forward checked `origin/main` before edits. Scope stayed limited to the
mechanism-prediction evaluation contract: no labels were imported, no
production fingerprints, ontology, scoring, thresholds, or curated labels were
edited, and no sequence-NN, PLM embedding, model training, or learned
representation benchmark result was run.

New evaluation-contract artifact:

```text
artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json
```

Contract SHA-256 for future benchmark result artifacts:

```text
c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50
```

The artifact freezes the five primary mechanism fingerprints for supervised
metrics and keeps radical SAM, cobalamin radical rearrangement, and flavin
monooxygenase as secondary OOD probe fingerprints with explicit probe roles.
It records SHA-256 digests for the coherence audit, representation baseline
plan, curated label registry, and mechanism fingerprint registry. It also
freezes deterministic OOS tiering rules, train-only MMseqs 30% identity / 80%
coverage diversity reporting, support thresholds, abstention diagnostics,
canary examples, and active-site pooling evidence-budget rules.

Caveat: the full 470-row out-of-scope tier assignment is explicitly not
complete. The contract freezes representative tier assignments and all
secondary probe assignments, then names the next exact task: apply the frozen
rules to all 470 `label_type=out_of_scope` rows and emit
`artifacts/v3_mechanism_prediction_oos_tier_assignments_702.json` with
per-entry tier, trigger, evidence source, and exclusion reason fields before
interpreting model results. Canary expansion remains marked as needed for that
same reason.

Future sequence-NN, PLM, or hybrid benchmark result artifacts must cite the
contract SHA above, stratify OOS abstention by this tier/probe policy, report
primary-fingerprint diversity bins, flag underpowered cells as
`qualitative_only`, and report whole-sequence and active-site-pooled evidence
budgets separately. Macro-F1 alone is not an interpretable win.

Verification passed:

```text
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mechanism_prediction_eval_contract_freezes_oos_diversity_policy
PYTHONPATH=src python -m unittest discover -s tests
git diff --check
jq empty artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json
```

Full unit discovery passed 934 tests. The new artifact is 48,676 bytes, so the
artifact-admission guard was not needed for a large-file check.

Commit `473a690` was created locally, but push to `origin/main` failed with:

```text
fatal: could not read Username for 'https://github.com': Device not configured
```

At handoff, the intended contract-freeze changes are committed locally but not
present on `origin/main` until GitHub HTTPS authentication is restored or the
remote is switched to an authenticated transport.

### 2026-05-25T09:49Z Current702 Sequence Coverage Repaired

This run acquired `.git/catalytic-earth-automation.lock`, fetched `origin`, and
confirmed local `HEAD` matched `origin/main` at
`ad785b59a8087598dd9f66feee8003f7d200258a` before edits. Scope stayed limited
to sequence coverage repair: no labels were imported, no registries,
fingerprints, ontology, scoring, or thresholds changed, and no representation
model benchmark was run.

New sequence repair artifacts:

```text
artifacts/v3_sequence_coverage_repair_current702_20260525.json
artifacts/v3_sequence_manifest_current702_repaired_20260525.json
artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta
artifacts/v3_sequence_distance_holdout_eval_1025_current702_repaired_20260525.json
artifacts/v3_representation_baseline_sequence_coverage_addendum_20260525.json
```

The starting holdout blocker rows were the 20 M-CSA entries named in
`artifacts/v3_representation_baseline_shootout_plan_20260525.json`. All were
resolved from UniProt accession sequences through the existing adapter. Two
multi-accession rows (`m_csa:791`, `m_csa:838`) contribute two sequence records
each, so the supplement records 26 UniProt sequence records across 24 current
labels: the 20 holdout-missing rows plus four non-evaluated current-label
manifest gaps (`m_csa:204`, `uniprot:P06744`, `uniprot:P78549`,
`uniprot:Q3LXA3`). No repair row needed a selected-PDB fallback.

Current coverage summary:

```text
total_current_labels = 702
sequence_covered_labels = 702
missing_sequence_entry_count_after_repair = 0
fallback_count = 2
fallback_entry_ids = m_csa:519, m_csa:588
```

The two fallback rows are pre-existing selected-PDB sequence fallback records
preserved from the historical FASTA, not new fallbacks introduced by this
repair. The repaired sequence-distance holdout evaluates 698 labels, covers
698/698 evaluated rows, holds out 140 rows, has
`sequence_missing_entry_count = 0`, and reports max observed train/test identity
`0.284`; the `<=0.30` sequence-hard target is satisfied.

Recomputed command:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-distance-holdout-eval --slice-id 1025_current702_repaired --retrieval artifacts/v3_geometry_retrieval_1025.json --labels data/registries/curated_mechanism_labels.json --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json --geometry artifacts/v3_geometry_features_1025.json --sequence-fasta artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta --sequence-identity-backend mmseqs --out artifacts/v3_sequence_distance_holdout_eval_1025_current702_repaired_20260525.json
```

Verification passed:

```text
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest discover -s tests
git diff --check
jq empty artifacts/v3_sequence_coverage_repair_current702_20260525.json artifacts/v3_sequence_manifest_current702_repaired_20260525.json artifacts/v3_sequence_distance_holdout_eval_1025_current702_repaired_20260525.json artifacts/v3_representation_baseline_sequence_coverage_addendum_20260525.json
```

Full unit discovery passed 933 tests. A temporary artifact-admission guard run
with fresh inventory/producer-consumer outputs blocked only on four pre-existing
large geometry artifacts:
`artifacts/v3_mcsa_positive_holo_override_20260523_geometry_features_1025.json`,
`artifacts/v3_mcsa_positive_holo_override_20260523_geometry_retrieval_1025.json`,
`artifacts/v3_mcsa_positive_m_csa771_2d0d_20260523_geometry_features_1025.json`,
and
`artifacts/v3_mcsa_positive_m_csa771_2d0d_20260523_geometry_retrieval_1025.json`.
The new sequence artifacts are below the guard's 5 MB large-file threshold.

Next action: do not rerun model benchmarks from this handoff. The sequence
coverage blocker is closed; representation work is now blocked on explicit
authorization to build full current-registry embedding sidecars and then run
the planned benchmark comparisons.

### 2026-05-25T09:08Z Fingerprint V1 Coherence Audit Frozen

This run acquired the automation lock and continued from local `HEAD` and
`origin/main` at `5a2d562`. The required non-destructive fetch attempted against
the configured SSH remote but failed with a public-key error; no merge or
destructive sync was performed. The working baseline still matched the recorded
`origin/main` ref before edits.

New audit-only artifact:

```text
artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json
```

The artifact freezes `mechanism_fingerprint_v1_8fp` for benchmark target
definition without editing `mechanism_fingerprints.json`,
`mechanism_ontology.json`, `curated_mechanism_labels.json`, scoring code, or
thresholds. It audits all eight production fingerprint ids against the current
702-label registry and records SHA-256 digests for the fingerprint and label
registries. Counts are frozen at 232 seed-fingerprint labels and 470
out-of-scope labels.

Primary metric implication: only the five fingerprints with
`coherent_v1` or `coarse_but_acceptable_v1` status are eligible for primary
`mechanism_fingerprint_id` metrics:

```text
ser_his_acid_hydrolase
metal_dependent_hydrolase
plp_dependent_enzyme
flavin_dehydrogenase_reductase
heme_peroxidase_oxidase
```

These cover 226 seed-fingerprint labels. The audit keeps caveats explicit:
metal hydrolase, PLP, flavin redox, and heme redox are coarse v1 buckets and
must be reported with within-fingerprint diversity checks. Radical SAM,
cobalamin radical rearrangement, and flavin monooxygenase are secondary-only
for v1: radical SAM and flavin monooxygenase are singleton/underpowered tails,
and cobalamin radical rearrangement needs a future split because `m_csa:853`
looks like cobalamin adenosyltransferase-like chemistry rather than a radical
rearrangement.

Benchmark rules are now pinned in the audit: out-of-scope/none-of-above is a
secondary abstention target stratified by hard-negative tier where possible;
bootstrap comparisons resample sequence or structure clusters for cluster-based
splits; EC/family prior is a leakage-aware reference only; AFDB/Swiss-Prot
pilots primarily test OOD abstention or embedding-space structure unless real
curated ground truth exists; and a representation win is conjunctive:
mechanism-prediction improvement plus maintained or improved calibrated
abstention on tail and hard-negative cases.

Target A next action remains sequence coverage, not model training. The exact
current blocker is still the 20 missing sequence rows from
`artifacts/v3_representation_baseline_shootout_plan_20260525.json`:

```text
m_csa:577, m_csa:596, m_csa:599, m_csa:623, m_csa:626, m_csa:636,
m_csa:641, m_csa:668, m_csa:706, m_csa:710, m_csa:720, m_csa:771,
m_csa:791, m_csa:812, m_csa:838, m_csa:865, m_csa:892, m_csa:897,
m_csa:917, m_csa:998
```

After supplementing the FASTA/sequence coverage, rerun the sequence holdout
command already recorded under
`artifacts/v3_representation_baseline_shootout_plan_20260525.json`.
Do not train ESM/ProtT5/ESM-C or claim learned superiority before that blocker
is closed.

Verification for this audit passed:

```text
python -m json.tool artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json
PYTHONPATH=src python -m unittest tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mechanism_fingerprint_v1_coherence_audit_freezes_primary_target
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest discover -s tests
git diff --check
PYTHONPATH=src python -m catalytic_earth.cli progress-report --out work/status.md
```

Full unit discovery passed 933 tests.

### 2026-05-25T08:40Z Representation Baseline Shootout V0 And Final Exact40 Holds

This run continued from `origin/main` commit `f7d05c5`, acquired the automation
lock, fast-forward synced, and observed that Targets A/B plus the other
nonclean exact40 buckets were already closed review-only in the latest pushed
state. No labels were imported, no import previews were run, no registry,
ontology, fingerprint, threshold, or production scoring state changed, and the
pre-existing root CIF files were ignored.

New review-only artifacts:

```text
artifacts/v3_learned_retrieval_manifest_1025_current702_full_20260525.json
artifacts/v3_sequence_distance_holdout_eval_1025_current702_20260525.json
artifacts/v3_representation_baseline_shootout_plan_20260525.json
artifacts/v3_mcsa_ai_visual_remaining_manual_expert_holds_index_20260525.json
```

Representation baseline v0 status: the current 702-label registry is now
specified for representation work without a training claim. The full current
learned-retrieval interface covers 698 labels, marks 635 eligible for future
learned-retrieval interfaces, and records four exact missing rows:
`m_csa:204`, `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`. The
shootout plan separates 17 expert-reviewed silver labels as high-trust
evaluation/calibration anchors, 215 automation bronze positives as weak
supervision only, and 470 out-of-scope labels as negative/OOD calibration. The
current 702-label sequence holdout refresh evaluates 698 labels, holds out 140,
retains 0 held-out false non-abstentions for geometry, and records 20 rows with
missing sequence coverage (`m_csa:577`, `m_csa:596`, `m_csa:599`, `m_csa:623`,
`m_csa:626`, `m_csa:636`, `m_csa:641`, `m_csa:668`, `m_csa:706`,
`m_csa:710`, `m_csa:720`, `m_csa:771`, `m_csa:791`, `m_csa:812`,
`m_csa:838`, `m_csa:865`, `m_csa:892`, `m_csa:897`, `m_csa:917`,
`m_csa:998`). The plan compares those heuristic geometry metrics against a
deterministic 3-mer sequence-nearest-neighbor smoke on the current split; the
k-mer smoke gets 0.5441 exact-label accuracy overall, 0.1136 in-scope
exact-label accuracy, and a 0.25 no-threshold out-of-scope false-positive rate.
This is not a model-training result.

The representation plan records existing external k-mer and ESM-2 controls as
external-only sidecars and blocks full ESM/hybrid representation claims until
the 20 missing sequence records and a full current embedding sidecar exist. The
next exact rerun command after supplementing sequence coverage is:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-distance-holdout-eval --slice-id 1025_current702 --retrieval artifacts/v3_geometry_retrieval_1025.json --labels data/registries/curated_mechanism_labels.json --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json --geometry artifacts/v3_geometry_features_1025.json --sequence-fasta artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta --sequence-identity-backend mmseqs --out artifacts/v3_sequence_distance_holdout_eval_1025_current702_20260525.json
```

Remaining exact40 manual/expert residue is now explicit in the holds index:
`m_csa:591`, `m_csa:951`, `m_csa:986`, `m_csa:927`, and `m_csa:886` require
expert biochemical boundary review; `m_csa:650` requires manual visual
target/top1 reconciliation. All six remain non-countable and not import-ready.

Targeted verification passed:

```text
PYTHONPATH=src python -m unittest tests.test_representation_baseline tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_representation_baseline_shootout_plan_is_leakage_guarded tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_remaining_manual_expert_holds_are_explicit
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest discover -s tests
git diff --check
python -m json.tool artifacts/v3_sequence_distance_holdout_eval_1025_current702_20260525.json
python -m json.tool artifacts/v3_representation_baseline_shootout_plan_20260525.json
python -m json.tool artifacts/v3_learned_retrieval_manifest_1025_current702_full_20260525.json
python -m json.tool artifacts/v3_mcsa_ai_visual_remaining_manual_expert_holds_index_20260525.json
```

### 2026-05-25T04:50Z Exact40 AMP/Holo Follow-Up Buckets Closed Review-Only

This run continued from `origin/main` commit `2569007`, acquired the automation
lock, fast-forward synced, and worked only on exact nonclean exact40 buckets.
No labels were imported, no import previews were run, no canonical registry,
ontology, fingerprint, threshold, or scoring state changed, and the
pre-existing root CIF files were ignored.

New review-only artifacts:

```text
artifacts/v3_mcsa_ai_visual_amp_nontransfer_discriminator_eval_20260525.json
artifacts/v3_mcsa_ai_visual_apo_holo_exact5_remediation_20260525.json
artifacts/v3_mcsa_ai_visual_apo_holo_exact5_alternate_structure_scan_20260525.json
artifacts/v3_mcsa_ai_visual_apo_holo_exact5_holo_preference_audit_20260525.json
artifacts/v3_mcsa_ai_visual_apo_holo_exact5_selected_pdb_overrides_20260525.json
artifacts/v3_mcsa_ai_visual_loose_geometry_policy_exact4_20260525.json
artifacts/v3_mcsa_ai_visual_future_family_ontology_backlog_exact5_20260525.json
artifacts/v3_mcsa_ai_visual_true_reject_hard_negative_signal_exact5_20260525.json
```

AMP/nucleotide exact-five decision: 0 import candidates. `m_csa:751`,
`m_csa:833`, `m_csa:780`, and `m_csa:656` route as current-target rejects or
future-family ATPase/helicase/kinase/phosphoryl-transfer evidence; `m_csa:564`
remains terminal review-only because the chemistry is non-transfer-like RNA
phosphodiester cleavage but local/structure metal evidence is absent and the
score stays below threshold. The discriminator artifact explicitly requires
M-CSA catalytic-pocket scope, blocks allosteric/regulatory AMP from catalytic
non-transfer classification, retains aaRS/ligase/ANL/NMNAT/asparagine
synthetase transfer controls, and keeps adenylate kinase, Nudix Ap4A, and
aaRS editing-site AMP as edge/out-of-scope controls.

Apo/holo exact-five decision: the exact remediation filter fed the existing
`scan-review-debt-alternate-structures` CLI. The scan checked all 37 candidate
structures with 0 fetch failures. `m_csa:952`, `m_csa:794`, `m_csa:671`, and
`m_csa:832` have no expected metal in scanned structures. `m_csa:644` has
structure-wide metal hits in alternates (`5CK6`, `5CLK`, `5YNG`) but 0 local
active-site expected-family hits, so the holo-preference audit recommends 0
swaps and the selected-PDB override plan has 0 ready rows.

Additional exact40 buckets handled before wrap:

```text
loose/open/interdomain geometry:
  m_csa:976, m_csa:847, m_csa:642, m_csa:844
wrong-fingerprint/future-family backlog:
  m_csa:793, m_csa:755, m_csa:817, m_csa:597, m_csa:729
true-reject current-target hard-negative signal:
  m_csa:841, m_csa:658, m_csa:827, m_csa:774, m_csa:831
```

All remain non-countable. The loose-geometry artifact blocks import from wide
focus-pair or boundary evidence alone. The future-family backlog records
glycoside hydrolase, transferase/thioester-transfer, cysteine-protease, and
GH18/substrate-assisted routes without ontology or fingerprint edits. The
true-reject artifact preserves those rows as hard negatives for the named
current target only, never as global negatives or future-family positive
seeds.

Rows intentionally left as explicit holds: `m_csa:650` remains manual visual
target/top1 reconciliation; the five expert-biochemistry rows remain expert
holds. Next action: if continuing exact40 cleanup, build only a hold/index
artifact for manual/expert rows or wait for human review; do not import unless
a dedicated preview, label-factory gate, and batch acceptance all pass.

Targeted verification passed:

```text
PYTHONPATH=src python -m unittest tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_amp_nontransfer_discriminator_exact5_review_only tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_apo_holo_exact5_scan_finds_no_local_holo_swaps tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_loose_geometry_policy_exact4_stays_review_only tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_future_family_backlog_exact5_does_not_edit_schema tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_true_reject_hard_negatives_are_current_target_only
```

### 2026-05-25T02:52Z Clean10 Accept7 Imported

The clean-10 M-CSA AI-visual expert decisions were split into seven countable
acceptances and three preserved non-countable signals. The accepted labels are:

```text
m_csa:596, m_csa:626, m_csa:668, m_csa:710, m_csa:720, m_csa:791, m_csa:838
```

Dedicated import-preview artifacts are under:

```text
artifacts/v3_mcsa_ai_visual_clean10_accept7_vivek_20260524_*_import_preview_1025.json
```

The batch acceptance artifact
`artifacts/v3_mcsa_ai_visual_clean10_accept7_vivek_20260524_label_batch_acceptance_check_import_preview_1025.json`
passes with `accepted_for_counting=true`, `accepted_new_label_count=7`, 0
accepted review gaps, 0 hard-negative controls, and 0 accepted
reaction/substrate mismatches. Canonical curated labels moved from 695 to 702,
with all seven new rows as `seed_fingerprint`, `metal_dependent_hydrolase`,
`silver`, `expert_reviewed`, `label_factory_v1_8fp`.

The three non-imported clean-10 rows are deliberately preserved:
`m_csa:954` and `m_csa:955` route to future terpene/isoprenoid carbocation
cyclization family evidence, while `m_csa:661` remains an FGly/sulfatase
sub-family/schema hold. The other 30 exact-40 rows are also preserved in
`artifacts/v3_mcsa_ai_visual_post_clean10_remaining30_signal_20260524.json`
with bucket counts: 5 AMP/nucleotide non-transfer, 5 apo/holo missing cofactor,
4 loose/open/interdomain geometry, 5 expert-biochemistry review, 1 manual
visual review, 5 true reject, and 5 wrong-fingerprint/future-family.

Verification after canonical import:

```text
PYTHONPATH=src python -m catalytic_earth.cli validate
```

passed and validated 702 curated mechanism labels.

### 2026-05-24T21:13Z Clean10 Expert Decisions Recorded

Vivek relayed expert review decisions for the clean-10 M-CSA AI-visual packet.
The decision artifact is:

```text
artifacts/v3_mcsa_ai_visual_clean10_vivek_expert_decision_batch_20260524.json
```

Decision counts: seven `accepted` for the current `metal_dependent_hydrolase`
target (`m_csa:710`, `m_csa:791`, `m_csa:626`, `m_csa:720`, `m_csa:596`,
`m_csa:668`, `m_csa:838`), two `route_future_family` rows (`m_csa:954`,
`m_csa:955`) routed to the existing terpene/isoprenoid carbocation-cyclization
future-family/out-of-scope lane, and one `needs_more_evidence` row
(`m_csa:661`) held for an FGly sulfatase / arylsulfatase sub-family decision.

Pre-commit caveats were checked. `m_csa:838` has `NI` in the selected crystal
structure, but current evidence artifacts classify expected, local, and
structure cofactor families as `metal_ion`, with no counterevidence; the expert
note records Ni as a divalent metal surrogate. `m_csa:954` and `m_csa:955`
match existing out-of-scope terpene carbocation/cyclization precedent in the
registry and artifacts; no production fingerprint or ontology edit was made.

This is a decision-recording artifact only. No labels were imported, no import
preview was run, and no registry, fingerprint, threshold, or scoring state was
changed. Next exact action, if Vivek approves: build dedicated gate/import
preview artifacts for only the seven accepted rows.

### 2026-05-24T18:13Z Run Target Selected: M-CSA Review Workqueue Surface

STARTED_AT for this run: `2026-05-24T18:05:54Z`. Automation memory was checked
first; no memory file existed at run start. Stale lock records for non-live
PIDs were found during the run, and status/process/recent file state was
inspected before replacement. `git fetch origin` and
`git pull --ff-only origin main` completed with the checkout already up to date
at `92f8aa134409993a28a7b6cd69117956d8de1318`. SSH safety was verified:
`origin` is `git@github.com:VivekVardhanArrabelli/catalytic-earth.git`,
`core.sshCommand` points to
`/Users/vivekvardhanarrabelli/.ssh/catalytic_earth_deploy_ed25519`,
`git ls-remote origin HEAD` returned `92f8aa134409993a28a7b6cd69117956d8de1318`,
and `git push --dry-run origin main` returned `Everything up-to-date`.
Startup validation passed before implementation: 917 unit tests and
`PYTHONPATH=src python -m catalytic_earth.cli validate` at 12 source records,
8 mechanism fingerprints, 15 ontology families, and 695 curated mechanism
labels. The only unrelated dirty files remain the pre-existing root-level
untracked CIF files (`6MO.cif`, `IOD.cif`, `NA.cif`, `O.cif`, `UNL.cif`).

Chosen bounded value-add: finish a review-only M-CSA AI-visual support surface
that turns the already-built exact-66, exact-40, clean-10, learning-signal,
rejected-taxonomy, and non-clean strategy artifacts into a practical review
workqueue. This was the highest-value safe target because the science support
artifacts already existed, while Vivek's next bottleneck is operational:
finding the right row, seeing the PyMOL/strategy context, and keeping all
decisions blank until human review. Confidence call: high, because every output
is a deterministic join or projection over immutable review-only artifacts and
does not import labels, run import previews, edit registries/fingerprints,
change scoring, or make biological accept/reject calls.

Completed safe outputs:

```text
artifacts/v3_mcsa_ai_visual_review_support_index_20260524.json
artifacts/v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json
artifacts/v3_mcsa_ai_visual_exact40_review_workqueue_worksheet_20260524.tsv
artifacts/v3_mcsa_ai_visual_exact40_review_worksheet_20260524.tsv
artifacts/v3_mcsa_ai_visual_deferred26_after_exact40_backlog_20260524.json
artifacts/v3_mcsa_ai_visual_deferred26_after_exact40_worksheet_20260524.tsv
artifacts/v3_mcsa_ai_visual_review_surface_readme_20260524.md
tests/test_automation_small_win_artifacts.py
src/catalytic_earth/generalization.py
README.md
docs/label_factory.md
```

Count verification: the fixed AI-visual universe remains exactly 298 rows =
22 accepted review signals, 210 current-target-only rejects, and 66 unresolved
`needs_more_evidence` holds. The support surface preserves exact40=40,
clean10=10, nonclean30=30, deferred26=26, 40 blank exact-40 decisions, 10
clean-row PyMOL script pointers, and 40 existing exact-40 structure paths. The
deferred26 backlog remains outside exact40 and is grouped as 9
apo/holo-local-cofactor deferrals, 13 future-family/schema deferrals, and 4
reject-confirmation deferrals. The exact40 and deferred TSV worksheets keep
all decision/reviewer/date columns blank and include no-import guardrails.

Verification run:

```text
python -m json.tool artifacts/v3_mcsa_ai_visual_review_support_index_20260524.json
python -m json.tool artifacts/v3_mcsa_ai_visual_exact40_review_workqueue_20260524.json
python -m json.tool artifacts/v3_mcsa_ai_visual_deferred26_after_exact40_backlog_20260524.json
PYTHONPATH=src python -m unittest tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_review_support_index_links_current_surface tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_review_surface_readme_points_at_safe_artifacts tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_exact40_workqueue_worksheet_is_blank_review_only tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_deferred26_worksheet_waits_for_exact40 tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_deferred26_backlog_waits_for_exact40 tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_exact40_workqueue_keeps_decisions_blank tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_exact40_review_worksheet_is_blank_tsv
PYTHONPATH=src python -m unittest tests.test_generalization.SequenceDistanceHoldoutTests.test_mmseqs_holdout_clusters_whole_sequence_units
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
python -m compileall -q src tests
git diff --check
git diff -- data/registries data/fingerprints
```

Results: full unit discovery passed with 924 tests; CLI validate reported 12
source records, 8 mechanism fingerprints, 15 ontology families, and 695
curated mechanism labels. The final full-suite rerun initially exposed an
order-dependent MMseqs temp-directory collision; `generalization.py` now uses
unique `/private/tmp` workdirs for MMseqs clustering/search, and the targeted
MMseqs test plus the full 924-test suite pass after that isolation fix. The
protected registry/fingerprint diff was empty. No label import, import preview,
curated label edit, registry/fingerprint edit, production scoring/threshold
change, source artifact mutation, migration, upload/removal, LFS/history
rewrite, or `removal_allowed=true` action occurred. Disk had 24 GiB free at
wrap. The pre-existing root-level untracked CIF files (`6MO.cif`, `IOD.cif`,
`NA.cif`, `O.cif`, `UNL.cif`) remain untouched and outside scope.

Final follow-up before release: `src/catalytic_earth/generalization.py` now
uses unique `/private/tmp` MMseqs working directories via `tempfile.mkdtemp`
instead of deleting/reusing digest-stable paths. This is temp-directory
collision hardening only; it does not change label state, thresholds, scoring
semantics, fingerprints, or ontology semantics. Verification for the follow-up:
`PYTHONPATH=src python -m unittest tests.test_generalization`,
`PYTHONPATH=src python -m catalytic_earth.cli validate`, `git diff --check`,
and `git diff -- data/registries data/fingerprints` all passed.

Next recommended target: do not expand M-CSA review scope while Vivek is away.
If another no-human run is needed, limit it to read-only consistency checks,
documentation links, or leakage-safe learned-representation manifests over this
fixed 298-row surface.

### 2026-05-24T10:06Z Run Target Selected: AI-Visual Learning Signal Manifest

STARTED_AT for this run: `2026-05-24T10:06:00Z`. The automation lock was
acquired, `git fetch origin` and `git pull --ff-only origin main` completed,
and startup validation passed before implementation: 913 unit tests and
`PYTHONPATH=src python -m catalytic_earth.cli validate` at 695 curated labels
and 8 production fingerprints. SSH safety was verified with SSH `origin`, the
deploy-key `core.sshCommand`, `git ls-remote origin HEAD`, and
`git push --dry-run origin main`.

Chosen bounded value-add: build a review-only M-CSA AI-assisted visual learning
signal manifest for the fixed 298-row source universe, separating accepted
positive review signal, current-target hard negatives, unresolved review holds,
future-family routes, and fields forbidden for prediction. This is the highest
safe target from the observed state because the exact-66 triage matrix and
exact-40 human packets already reduce immediate review burden, while the 210
safe rejects and 66 holds are still not packaged as a leakage-aware
representation-learning interface. Confidence call: high that this can be
derived deterministically from the existing 298-row decision artifact plus the
66-row triage matrix without label imports, import previews, registry edits,
fingerprint edits, scoring changes, or source artifact mutation.

Second bounded value-add selected after the manifest completed early:
derive a 210-row rejected-signal taxonomy from the same fixed source universe,
preserving current-target rejection reasons, future-family routes, and likely
reuse lanes for future ontology work. Rationale: the learning manifest protects
against prediction leakage, but Vivek and later agents still need a compact
way to mine the 210 safe rejects without reopening them as global negatives.
Confidence call: high that this is safe because it is a deterministic summary
of existing rejected rows only and does not assign any new accept/reject
decision.

Third bounded value-add selected after the rejected taxonomy completed early:
derive a non-clean exact-40 review strategy for the 30 rows outside the
clean-10 fast path, grouping them by the safest next reviewer workflow
(`structure/PyMOL`, `expert biochemistry`, `future-family/schema`, or
`reject-confirmation review`) without making any row-level decision. Rationale:
the clean-10 packet is already easy to start; the remaining exact-40 rows are
where Vivek will save the most time if the next action is pre-sorted.
Confidence call: high that the strategy can be derived from the existing
exact-40 packet and 66-row triage matrix while keeping all decisions blank.

Fourth bounded value-add selected after the non-clean strategy completed early:
build clean-10 fast-review usability cards that join the clean-first packet,
blank exact-40 template positions, and local PyMOL scripts into one
review-only checklist. Rationale: this directly reduces Vivek's first-pass
review friction without making decisions or changing any scientific state.
Confidence call: high because it is a pure join over existing clean-10 review
artifacts and local script paths already verified by regression tests.

Completed safe outputs:

```text
artifacts/v3_mcsa_ai_visual_learning_signal_manifest_20260524.json
artifacts/v3_mcsa_ai_visual_rejected_signal_taxonomy_20260524.json
artifacts/v3_mcsa_ai_visual_nonclean30_exact40_strategy_20260524.json
artifacts/v3_mcsa_ai_visual_clean10_fast_review_cards_20260524.json
tests/test_automation_small_win_artifacts.py
```

Count verification: the learning manifest covers the fixed 298-row AI-visual
source universe exactly, with 22 `positive_review_signal_review_only` rows,
210 `current_target_hard_negative` rows, and 66 `unresolved_review_hold` rows.
It carries explicit prediction-leakage controls and marks every row
`countable_training_label=false`. The rejected taxonomy covers exactly the 210
safe rejects in source order, keeps all rows scoped as current-target-only hard
negatives, preserves future-family routes, and summarizes route buckets:
56 unrepresented future-family routes, 36 phosphoryl-transfer/kinase routes,
34 oxidoreductase/redox routes, 31 transferase/thioester routes, 19
lyase/dehydratase or Schiff-base routes, 14 glycoside hydrolase routes, 12
isomerase/mutase routes, 3 Cys-His-Asp protease routes, 3 heme/peroxide routes,
and 2 PLP routes. The non-clean exact-40 strategy covers the 30 rows outside
the clean-10 fast path: 10 expert-biochemistry boundary rows, 5 future-family
or schema route rows, 5 reject-confirmation review rows, 5 structure/holo
alternate rows, and 5 structure/PyMOL geometry rows. The clean-10 card packet
has 10 cards, 0 missing structure paths, 0 missing PyMOL scripts, and 10 blank
template decisions.

Verification run:

```text
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_learning_signal_manifest_is_leakage_aware tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_rejected_signal_taxonomy_stays_current_target_only tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_nonclean_exact40_strategy_presorts_without_decisions tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_mcsa_ai_visual_clean10_fast_review_cards_join_local_scripts
python -m compileall -q src tests
python -m json.tool artifacts/v3_mcsa_ai_visual_learning_signal_manifest_20260524.json
python -m json.tool artifacts/v3_mcsa_ai_visual_rejected_signal_taxonomy_20260524.json
python -m json.tool artifacts/v3_mcsa_ai_visual_nonclean30_exact40_strategy_20260524.json
python -m json.tool artifacts/v3_mcsa_ai_visual_clean10_fast_review_cards_20260524.json
git diff --check
```

Results: 917 unit tests passed; targeted M-CSA support-artifact tests passed;
validate reported 12 source records, 8 mechanism fingerprints, 15 ontology
families, and 695 curated mechanism labels. Disk had 24 GiB free at wrap.
`git diff -- data/registries data/fingerprints src/catalytic_earth` was empty.
No label import, import preview, curated label edit, registry/fingerprint edit,
production scoring/threshold change, source artifact mutation, migration,
upload/removal, LFS/history rewrite, or `removal_allowed=true` action occurred.
The only pre-existing dirty entries still outside this run are the root-level
untracked CIF files (`6MO.cif`, `IOD.cif`, `NA.cif`, `O.cif`, `UNL.cif`),
left untouched.

Next recommended target: if Vivek remains away, use these artifacts only to
prepare review ergonomics, not decisions. The next bounded safe add would be a
small README/doc note linking the learning manifest, rejected taxonomy,
non-clean strategy, and clean-10 cards as the current review-support surface,
or a compact cross-artifact consistency test if any later agent adds another
M-CSA support packet.

### 2026-05-24T08:52Z Exact 40 Packet Reverified From origin/main

STARTED_AT for this run: `2026-05-24T08:48:55Z`. The automation lock was
acquired after removing this run's initial stale self-lock record with status
inspection. `git fetch origin` and `git pull --ff-only origin main` completed,
and the checkout was already up to date at
`eadfc50 Record exact40 packet verification handoff`. SSH safety was verified:
`origin` uses `git@github.com:VivekVardhanArrabelli/catalytic-earth.git`,
`core.sshCommand` points to
`/Users/vivekvardhanarrabelli/.ssh/catalytic_earth_deploy_ed25519`,
`git ls-remote origin HEAD` returned `eadfc5091456c16f777613f98e210e6056ae498d`,
and `git push --dry-run origin main` returned `Everything up-to-date`. The only
pre-existing dirty worktree entries remain untracked root-level CIF files
(`6MO.cif`, `IOD.cif`, `NA.cif`, `O.cif`, `UNL.cif`), left untouched.

Required review-only outputs are still present and unchanged in the latest
pushed state:

```text
artifacts/v3_mcsa_ai_visual_exact40_human_review_packet_20260524.json
artifacts/v3_mcsa_ai_visual_clean10_review_first_packet_20260524.json
artifacts/v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json
artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/index.json
artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/open_clean10_pymol.sh
```

Count and contract verification: the requested exact 40 IDs match
`recommended_human_review_plan.unique_recommended_review_ids` in
`artifacts/v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json` exactly
and in order; the exact-40 packet has 40 rows; the clean-first packet has the
10 clean-likely-positive rows; the blank human decision template has 40 rows;
and the PyMOL index has 10 clean-row scripts with zero missing local structure
paths. The exact-40 regression test and a one-off contract check both passed.
All rows remain review-only with explicit allowed reviewer actions and no
default accept decisions.

Verification run:

```text
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m unittest tests.test_automation_small_win_artifacts.AutomationSmallWinArtifactsTest.test_exact40_ai_visual_human_review_packets_are_review_only
one-off exact40 artifact contract check
```

Results: 913 unit tests passed; targeted exact-40 test passed; validate
reported 12 source records, 8 mechanism fingerprints, 15 ontology families,
and 695 curated mechanism labels. No label import, import preview, source
artifact mutation, decision artifact mutation, registry edit, production
fingerprint edit, production scoring change, upload/removal/migration, LFS,
history rewrite, broad structure materialization, or `removal_allowed=true`
action was performed. Confidence call: high that the exact-40 review packet,
clean-10 fast packet, blank decision template, and clean-10 PyMOL index remain
pinned to the completed 66-row triage matrix without altering countable science
state. Next action for Vivek: review the clean-10 packet first, then fill the
exact-40 decision template only with `accepted`, `rejected`,
`needs_more_evidence`, or `route_future_family`.

### 2026-05-24T07:52Z Exact 40 Packet Verified From Latest Pushed State

STARTED_AT for this run: `2026-05-24T07:47:56Z`. The automation lock was
acquired, `origin/main` was fetched and fast-forward checked, and the checkout
was already up to date at `feca197 Build exact40 M-CSA human review packet`.
The only pre-existing dirty worktree entries were untracked root-level CIF files
(`6MO.cif`, `IOD.cif`, `NA.cif`, `O.cif`, `UNL.cif`); they were left untouched.

Required review-only outputs are present in the latest pushed state:

```text
artifacts/v3_mcsa_ai_visual_exact40_human_review_packet_20260524.json
artifacts/v3_mcsa_ai_visual_clean10_review_first_packet_20260524.json
artifacts/v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json
artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/index.json
artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/open_clean10_pymol.sh
```

Count and contract verification: the exact 40 IDs still match
`recommended_human_review_plan.unique_recommended_review_ids` in
`artifacts/v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json` exactly
and in order; the exact-40 packet has 40 rows; the clean-first packet has the
10 clean-likely-positive rows; the blank human decision template has 40 rows;
and the PyMOL index has 10 clean-row scripts with zero missing local structure
paths. All packet rows retain explicit reviewer actions, concise reviewer
questions, and review-only/no-default-accept semantics. No labels were
imported, no import preview was run, no source artifact or decision artifact was
mutated, and no registry, production fingerprint, scoring, upload/removal,
migration, LFS, history, or `removal_allowed=true` action was performed.

Verification run:

```text
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
one-off exact40 artifact contract check
```

Results: 913 unit tests passed; validate reported 12 source records, 8
mechanism fingerprints, 15 ontology families, and 695 curated mechanism
labels. Confidence call: high that the exact-40 review packet, clean-10 fast
packet, blank decision template, and clean-10 PyMOL index are pinned to the
completed 66-row triage matrix and did not alter countable science state. Next
action for Vivek: review the clean-10 packet first, then populate the exact-40
decision template only with `accepted`, `rejected`, `needs_more_evidence`, or
`route_future_family`.

### 2026-05-24T06:56Z Exact 40 Human Review Packet Built

STARTED_AT for this run: `2026-05-24T06:45:50Z`. The exact requested 40 IDs
were verified to match
`recommended_human_review_plan.unique_recommended_review_ids` in
`artifacts/v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json` exactly
and in order. No discrepancy note was needed.

New review-only outputs:

```text
artifacts/v3_mcsa_ai_visual_exact40_human_review_packet_20260524.json
artifacts/v3_mcsa_ai_visual_clean10_review_first_packet_20260524.json
artifacts/v3_mcsa_ai_visual_exact40_human_decision_template_20260524.json
artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/index.json
artifacts/review_pymol/mcsa_ai_visual_exact40_20260524/open_clean10_pymol.sh
```

Counts verified: exact-40 packet has 40 rows; clean-first packet has the 10
clean-likely-positive rows; blank human decision template has 40 rows; the
local PyMOL index has 10 clean-row scripts and zero missing local structure
paths. All rows remain review-only with no default accept decisions, no label
import, no import preview, no registry edit, no production fingerprint edit, no
production scoring change, and no upload/removal/migration action. Canonical
validation remains 695 curated labels and eight production fingerprints.

Verification run:

```text
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
```

Results: 913 unit tests passed; validate reported 12 source records, 8
mechanism fingerprints, 15 ontology families, and 695 curated mechanism
labels.

Confidence call: high that the exact-40 packet is pinned to the completed
66-row triage plan and that it did not mutate source, label, registry,
fingerprint, or scoring state. Medium-high that the clean-10 PyMOL scripts are
usable first-pass reviewer aids because they reuse already-local structure
paths and the prior visual focus pairs; they should still be treated only as
review aids. Next action for Vivek: review the clean-10 packet first, then fill
the blank exact-40 decision template with `accepted`, `rejected`,
`needs_more_evidence`, or `route_future_family`.

### 2026-05-24T05:50Z Exact 66 AI-Visual Review-Hold Triage Matrix Built

The exact pinned M-CSA AI-assisted visual review-hold tranche is now captured in
`artifacts/v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json`.
Source integrity was verified against the reaudited 298-row source: 22
accepted, 210 rejected, and exactly 66 `needs_more_evidence` rows. The matrix
contains exactly those 66 rows in source order. The 22 accepted rows and 210
safe bulk rejects are explicitly excluded, with zero accepted/rejected overlap;
the post-clean9 decision trace and exact-mapping terminal no-go artifacts also
have zero overlap with this target set.

Bucket counts in the 66-row matrix:

```text
clean_likely_positive: 10
apo_or_holo_missing_cofactor: 14
loose_open_or_interdomain_geometry: 4
amp_or_nucleotide_nontransfer_context: 5
wrong_fingerprint_or_future_ontology_family: 18
true_reject: 9
needs_manual_visual_review: 1
needs_expert_biochemistry_review: 5
residue_mapping_issue: 0
coupled_or_missing_schema_family: 0
already_terminal_no_go: 0
already_imported_or_resolved: 0
```

Confidence tiers: 20 high, 40 medium, and 6 low. The recommended human review
plan has an estimated maximum of 40 unique rows: all clean-likely positives
(`m_csa:954`, `m_csa:661`, `m_csa:710`, `m_csa:791`, `m_csa:626`,
`m_csa:720`, `m_csa:596`, `m_csa:668`, `m_csa:838`, `m_csa:955`), all
low-confidence rows (`m_csa:591`, `m_csa:951`, `m_csa:986`, `m_csa:927`,
`m_csa:650`, `m_csa:886`), and 2-5 representative rows per populated blocker
bucket, with the single manual-review row included as its one-row bucket.

No labels were imported, no import previews were run, no registry or production
fingerprint changed, no source review artifact was mutated, and no upload,
removal, migration, LFS tracking, history rewrite, or `removal_allowed=true`
operation occurred. Confidence call: high that the row universe is exact and
the accepted/rejected source rows are excluded; medium-high that the blocker
buckets are useful for batching human review because they are derived from the
reaudited visual decision notes plus enrichment-only review-debt evidence.
Exact next automation target: support or consume human review of the 40-row
recommended subset, then only after explicit human decisions consider dedicated
gate/import-preview work for rows accepted by that review.

### 2026-05-24T00:10Z Human Direction: Exact 66 Review-Hold Triage Before Manual Review

Vivek approved moving the remaining review/on-hold rows into an audited
batching workflow rather than reviewing every row manually. The exact intended
row set is now pinned: the 66 `needs_more_evidence` rows in the reaudited
298-row AI-assisted visual review artifact. Do not rediscover this from broad
review debt and do not substitute the 1025 review-debt universe as the target.

Pinned source artifacts:

```text
artifacts/v3_mcsa_ai_visual_decisions_298_reaudited_bulk_r_safe_20260523.json
artifacts/v3_mcsa_ai_visual_decisions_298_summary_20260523.json
artifacts/v3_mcsa_ai_visual_remaining_66_source_manifest_20260524.json
```

The source manifest records 298 total rows: 22 accepted/positive rows, 210
reaudited safe bulk rejects, and exactly 66 rows with
`decision == "needs_more_evidence"`. The next agent must target only those 66
IDs. The 22 accepted rows and 210 rejected rows may be used only as reference
context; they are not part of the next triage target.

Broad review-debt artifacts may be used only for enrichment/cross-reference:

```text
artifacts/v3_review_debt_summary_1025_preview.json
artifacts/v3_review_evidence_gaps_1025_preview.json
artifacts/v3_review_debt_remediation_1025_preview_all.json
artifacts/v3_mcsa_pymol_exact_mapping_terminal_no_go_23_20260524.json
artifacts/v3_mcsa_positive_post_clean9_decision_trace_22_20260524.json
artifacts/v3_expert_guidance_amp_nontransfer_and_coupled_plp_cobalamin_20260524.json
```

Do **not** manually review all rows and do **not** import labels in this triage
step. Build a compact triage matrix at
`artifacts/v3_mcsa_ai_visual_remaining_66_triage_matrix_20260524.json` with one
row per pinned `needs_more_evidence` candidate and these fields: `entry_id`,
`entry_name`, `structure_id`, `target_fingerprint_id`, `current_decision`,
source artifact, blocker bucket, confidence, evidence_for, evidence_against,
counterevidence, visual evidence, forbidden/review-only evidence, required
human or expert action, expected import potential, sample-review priority,
`would_unblock_if`, and `preserve_for_learning=true`.

Required buckets:

```text
clean_likely_positive
residue_mapping_issue
apo_or_holo_missing_cofactor
loose_open_or_interdomain_geometry
amp_or_nucleotide_nontransfer_context
coupled_or_missing_schema_family
wrong_fingerprint_or_future_ontology_family
true_reject
needs_manual_visual_review
needs_expert_biochemistry_review
already_terminal_no_go
already_imported_or_resolved
```

The purpose is quality control at scale: agents classify all rows, humans
review clean-likely positives, low-confidence rows, and a small representative
sample from each blocker bucket. Preserve all blocked/rejected decision signal
for future learned representations.

### 2026-05-24T00:00Z Expert Guidance: AMP Non-Transfer And Coupled PLP-Cobalamin

Vivek relayed external expert guidance that should be treated as new review
signal, not as a production rule by itself:

```text
artifacts/v3_expert_guidance_amp_nontransfer_and_coupled_plp_cobalamin_20260524.json
```

For `m_csa:784` and `m_csa:904`, the AMP issue should be reframed from
strict "product-state" to **non-transfer AMP context**: AMP can be hydrolytic
substrate-state or product-state and still should suppress
`nucleotide_transfer_ligand_context` when it is in the M-CSA-annotated
catalytic pocket and no transfer-state subrule applies. Required edge cases
before production activation: allosteric/regulatory AMP, ligase
autoadenylated AMP-Lys states with no PPi, adenylate kinase as out-of-scope,
Nudix Ap4A AMP+ATP product geometry, and aaRS editing-site AMP.

For `m_csa:737`, the guidance supports a **coupled PLP-adenosylcobalamin
aminomutase/radical motif** rather than pure PLP, pure cobalamin, or a generic
family. This remains a review-only schema proposal until the label schema can
represent coupled multi-cofactor motifs without collapsing the 3D mechanism
signal.

### 2026-05-24T04:56Z Decision Trace And Exact-Mapping Repair Split

Scientific target worked: preserve the post-clean9 M-CSA decision signal without
changing science, then advance the next bounded review-debt blocker class.
Previous status: the 22-row Vivek M-CSA positive review, 13 post-clean9
accepted/imported rows, and nine terminal current-evidence holds were spread
across multiple artifacts; the remaining PyMOL blocker report also had a
23-row exact focus-pair/distance mapping class with two structure-ID
subblockers. New status: the decision signal is now joined in
`artifacts/v3_mcsa_positive_post_clean9_decision_trace_22_20260524.json`, with
22 unique rows, 13 current imported countable rows, nine terminal blocked rows,
zero rejected rows, and zero new import eligibility from the trace itself.

The exact-mapping review-debt tranche is now terminal for current evidence in
`artifacts/v3_mcsa_pymol_exact_mapping_terminal_no_go_23_20260524.json`.
Rows changed: 23 blocker rows moved from a generic post-materialization blocker
surface into a row-level terminal/no-go packet for the exact CA atom-pair and
distance mapping class. Rows still blocked: all 23; no label import, registry
edit, fingerprint edit, production scoring change, upload/removal, or
`removal_allowed=true` occurred. The current nine M-CSA follow-up holds were
not reopened.

The two structure-ID subblockers were probed against RCSB mmCIF reference
mappings in
`artifacts/v3_mcsa_pymol_structure_id_mapping_repair_probe_m_csa930_946_20260524.json`.
Rows changed: two source-mapping blocker rows were split. `m_csa:946` now has
a review-only repair candidate: `5XD7` maps UniProt `H2IFX0`, resolves all six
requested residues to CA atoms, and gives a longest current CA pair
`m_csa:946:residue:2` to `m_csa:946:residue:6` at 18.663 A. `m_csa:930`
remains blocked because candidate `2PIA` maps UniProt `P33164`, not the
requested `Q9ZFQ5` source residue. Exact next target: build a one-row derived
review-only repair rerun for `m_csa:946` using `5XD7`; keep `m_csa:930`
blocked until Q9ZFQ5-specific structure or explicit residue-position evidence
exists. Confidence call: high that the trace/no-go artifacts preserve decision
signal without changing labels; medium-high that `m_csa:946` is the next
actionable exact-mapping repair row, pending a derived queue rerun.

### 2026-05-24T03:52Z Terminal Decisions: Remaining Nine M-CSA Holds

The remaining nine blocked rows from the Vivek-reviewed M-CSA positive
follow-up were processed by blocker class from the 695-label baseline. No
labels were imported, no import previews were run, no production scoring or
fingerprint registry changed, and canonical labels remain 695 with 8
production fingerprints.

New terminal/current-evidence artifacts:

```text
artifacts/v3_mcsa_positive_loose_cofactor_locality_policy_decision_3_20260524.json
artifacts/v3_mcsa_positive_apo_holo_terminal_no_go_m_csa836_996_20260524.json
artifacts/v3_mcsa_positive_amp_product_terminal_no_go_m_csa784_904_20260524.json
artifacts/v3_mcsa_positive_plp_threshold_terminal_no_go_m_csa777_20260524.json
artifacts/v3_mcsa_positive_schema_decision_m_csa737_coupled_plp_cobalamin_proposal_20260524.json
artifacts/v3_mcsa_positive_remaining_9_terminal_blocker_summary_20260524.json
```

Previous status: `m_csa:611`, `m_csa:657`, `m_csa:1001`, `m_csa:836`,
`m_csa:996`, `m_csa:784`, `m_csa:904`, `m_csa:777`, and `m_csa:737` were
blocked holds requiring new explicit artifacts before any import. New status:
all nine are still blocked, but the current loop is terminal for current
evidence. Rows changed: none in the canonical registry. Rows still blocked:
all nine. The loose/inter-domain/cofactor-locality policy now says these cases
can be countable only with explicit structural evidence that residues, cofactor,
and water/substrate context form one active catalytic unit; the three current
rows do not meet that bar. The apo/holo rows still lack local remapped holo
evidence. The AMP-product rows still lack enough positives plus a tested
production rule. `m_csa:777` remains 0.0008 below the 0.4115 threshold without
new scored PLP evidence. `m_csa:737` now has a review-only coupled
PLP-adenosylcobalamin aminomutase family proposal, not a production fingerprint
or countable multi-target label.

Wrap validation passed: 908-test unit discovery, CLI validate at 695 labels and
8 fingerprints, compileall, artifact-migration dry run with `removal_allowed=0`,
JSON parsing for the new artifacts, and `git diff --check`. Confidence call:
high that the remaining-nine loop should not be repeated from current evidence.
Exact next blocker: none in the specified nine-row M-CSA follow-up; future work
requires new structure evidence, production-rule work, or an explicit
schema/fingerprint task.

### 2026-05-24T03:15Z Canonical Import: Holo Overrides Plus m_csa:771 Landed

The post-clean9 follow-up import is complete and pushed through dedicated
artifacts, not the clean9 path. Canonical labels now validate at 695 with 8
production fingerprints. Imported this run:

```text
m_csa:577, m_csa:641, m_csa:897, m_csa:771
```

The holo override batch used the automation-assisted accept artifact
`artifacts/v3_mcsa_positive_holo_override_accept_decision_3_20260523.json`
plus the dedicated
`artifacts/v3_mcsa_positive_holo_override_accept3_20260523_*_import_preview_1025.json`
gate stack. It passed 21/21 gates and batch acceptance with exactly three new
labels (`691 -> 694`). The `m_csa:771` batch used Vivek's explicit PyMOL
decision in
`artifacts/v3_mcsa_positive_m_csa771_2d0d_vivek_accept_decision_20260523.json`
plus the dedicated
`artifacts/v3_mcsa_positive_m_csa771_2d0d_vivek_20260523_*_import_preview_1025.json`
gate stack. It passed 21/21 gates and batch acceptance with exactly one new
label (`694 -> 695`).

The AMP-product counterevidence rule remains review-only. The expanded stress
panel
`artifacts/v3_mcsa_positive_nucleotide_product_counterevidence_rule_stress_panel_20260524.json`
has 2 product-context exception candidates and 33 retain-counterevidence
transfer controls, but blocks production activation because the positive side
is too small, both exception candidates remain below the abstention floor
without an ungated scoring change, and no production rule/tests/gates were
activated. Confidence call: high that the canonical import state is coherent
and gate-backed; medium-high that `m_csa:784`/`m_csa:904` should remain blocked
until additional product-context positives and tested production code exist.

The compact post-import matrix is
`artifacts/v3_mcsa_positive_remaining_13_decision_matrix_post_import_20260524.json`.
It records four imported rows and nine still-blocked holds. Do not promote
`m_csa:777`, `m_csa:784`, `m_csa:904`, `m_csa:836`, `m_csa:996`, `m_csa:611`,
`m_csa:657`, `m_csa:1001`, or `m_csa:737` without a new explicit blocker-
removal artifact and dedicated gates.

### 2026-05-23T22:05Z Canonical Import: Three Holo Overrides Landed

The gate-clean holo override packet has been applied to the canonical registry:
`m_csa:577`, `m_csa:641`, and `m_csa:897` are now countable
`metal_dependent_hydrolase` labels. Canonical label count is now 694. This is
the expected movement from the accepted holo override preview and uses the
committed gate packet:

```text
artifacts/v3_mcsa_positive_holo_override_accept3_20260523_*_import_preview_1025.json
```

`m_csa:771` is **not** imported yet. Its stacked preview gate is clean from the
694-label baseline, but the canonical registry still lacks `m_csa:771`. Next
agent should import exactly `m_csa:771` from
`artifacts/v3_mcsa_positive_m_csa771_2d0d_vivek_accept_decision_20260523.json`
or the corresponding clean preview packet, then verify the expected movement
`694 -> 695`.

### 2026-05-23T21:55Z Import Previews: Holo Overrides And m_csa:771 Gate-Clean

An overlapping import-preview run produced the dedicated holo override preview
artifact set:

```text
artifacts/v3_mcsa_positive_holo_override_accept3_20260523_*_import_preview_1025.json
```

The preview adds exactly `m_csa:577`, `m_csa:641`, and `m_csa:897` in the
preview registry (`691 -> 694`) as automation-curated bronze
`metal_dependent_hydrolase` labels. The direct safety signals are clean:
accepted new label count 3, no accepted review gaps, no reaction/substrate
mismatches, no hard negatives, no near misses, no out-of-scope false
non-abstentions, and no actionable in-scope failures.

The final generated gate artifacts are clean: `label_factory_gate_check` has no
blockers, and `label_batch_acceptance_check` has `accepted_for_counting=true`,
`factory_gate_ready=true`, `baseline_label_count=691`,
`countable_label_count=694`, and `accepted_new_label_count=3`.

The same overlapping work also emitted a `m_csa:771` import-preview set:

```text
artifacts/v3_mcsa_positive_m_csa771_2d0d_20260523_*_import_preview_1025.json
artifacts/v3_mcsa_positive_m_csa771_2d0d_accept_decision_20260523.json
```

This was generated after the holo preview state was materialized, so it is a
stacked clean preview (`691 -> 694 -> 695`), not a standalone `m_csa:771`
preview from the canonical 691 registry. The authoritative human decision is
`artifacts/v3_mcsa_positive_m_csa771_2d0d_vivek_accept_decision_20260523.json`.
The final generated `m_csa:771` gate artifacts are clean:
`label_factory_gate_check` has no blockers, and `label_batch_acceptance_check`
has `accepted_for_counting=true`, `factory_gate_ready=true`,
`baseline_label_count=694`, `countable_label_count=695`, and
`accepted_new_label_count=1`.

Canonical labels still remain at 691 in this commit. The next canonical movement
should be performed as an explicit import step: first import the gate-clean holo
override packet (`691 -> 694`), then import the gate-clean `m_csa:771` packet
(`694 -> 695`), then regenerate `v3_label_summary.json`, run CLI validate,
targeted regression tests, and full label-factory checks.

### 2026-05-24T02:50Z Agent Output: Holo Overrides Ready For Dedicated Gates

The prior automation left a post-preview accept-decision artifact for the three
holo override rows:

```text
artifacts/v3_mcsa_positive_holo_override_accept_decision_3_20260523.json
```

It is explicitly automation-assisted, not new human expert review. It uses the
prior Vivek hold decisions plus the derived holo evidence from the selected-PDB
override preview. The accepted gate-input rows are `m_csa:577 -> 1AWB`,
`m_csa:641 -> 1J7N`, and `m_csa:897 -> 1H56`; all remain non-imported until a
dedicated countable import preview, full label-factory gate, batch acceptance,
tests, and CLI validate pass. If gates pass, the only allowed canonical movement
from this artifact is `691 -> 694` with exactly those three entries added.

### 2026-05-24T02:46Z Human Decision: m_csa:771 Accepted For Dedicated Gates

Vivek completed the PyMOL check for `m_csa:771` with alternate structure
`2D0D`. The explicit decision artifact is:

```text
artifacts/v3_mcsa_positive_m_csa771_2d0d_vivek_accept_decision_20260523.json
```

The decision is `accept_label` as `ser_his_acid_hydrolase`, reviewer `vivek`.
The evidence is that `2D0D` resolves the selected-PDB Ser103 mutation blocker,
shows catalytic Ser103 mapped to the M-CSA nucleophile, and PyMOL review places
Ser103/His252/Asp224 in a coherent Ser-His-Asp triad: Ser103 OG to His252 NE2
is approximately 2.6-3.1 A and His252 ND1 to Asp224 OD is approximately 3.2 A.
This artifact is a gate input only: it does not import the label, edit the
canonical registry, or authorize import without a dedicated countable import
preview, full label-factory gates, batch acceptance, tests, and CLI validate.

Next automation should consume this decision and run the dedicated `m_csa:771`
gate/import-preview path. If gates pass, the only allowed canonical movement
from this row is `691 -> 692` with exactly `m_csa:771` added.

### 2026-05-23T20:09Z Verification: Requested M-CSA Tranche Already Landed

The 2026-05-23T20:09:07Z automation start found `origin/main` already at the
post-clean9 state described below. The requested mechanical tranche was not
rerun: `artifacts/v3_mcsa_positive_clean9_import_preview_20260523.json`
already records the gated canonical import of exactly `m_csa:599`,
`m_csa:623`, `m_csa:636`, `m_csa:706`, `m_csa:812`, `m_csa:865`,
`m_csa:892`, `m_csa:917`, and `m_csa:998`, and CLI validation confirms
691 curated labels and 8 production fingerprints. The three imported external
out-of-scope labels remain exactly
`uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`; external
seed-fingerprint imports remain 0.

Evidence-based confidence call: confidence is high that no additional
automated label import is authorized from the current repo state. The clean9
import has already passed its gate stack and is canonical; the holo override
preview for `m_csa:577`, `m_csa:641`, and `m_csa:897`, plus the `m_csa:771`
`2D0D` noncanonical review, remain non-imported because they need explicit
post-preview accept decisions and full dedicated gates. The caveat rows
`m_csa:777`, `m_csa:784`, and `m_csa:904` remain held.

### Immediate Next Target: Post-Clean9 M-CSA Holds

The Vivek-reviewed 22-row M-CSA positive follow-up has one gated canonical
import completed. The clean import summary is:

```text
artifacts/v3_mcsa_positive_clean9_import_preview_20260523.json
```

Exactly nine clean rows were imported into
`data/registries/curated_mechanism_labels.json`: `m_csa:599`, `m_csa:623`,
`m_csa:636`, `m_csa:706`, `m_csa:812`, `m_csa:865`, `m_csa:892`,
`m_csa:917`, and `m_csa:998`. The registry moved 682 -> 691 labels, with
221 seed-fingerprint labels and 470 out-of-scope labels. The imported external
out-of-scope labels remain exactly `uniprot:P06744`, `uniprot:P78549`, and
`uniprot:Q3LXA3`; external seed-fingerprint imports remain 0; the production
fingerprint universe remains 8.

The original accepted import-readiness preview remains source evidence only:

```text
artifacts/v3_mcsa_positive_accepted_import_gate_readiness_12_20260523.json
```

It preserves 12 accepted rows and still marks the three accept-with-caveat rows
as blocked: `m_csa:777`, `m_csa:784`, and `m_csa:904`. For `m_csa:777`, do not
use the older 1000-entry score: the current 1025 score is 0.4107, below the
0.4115 abstain threshold. For `m_csa:784` and `m_csa:904`, the new
review-only nucleotide-product stress probe distinguishes AMP product
hydrolysis from true transfer controls, but it is not a production scoring rule
and does not unblock either row.

The hold follow-up artifacts are:

```text
artifacts/v3_mcsa_positive_hold_apo_holo_override_plan_5_20260523.json
artifacts/v3_mcsa_positive_hold_geometry_locality_resolution_3_20260523.json
artifacts/v3_mcsa_positive_residue_mapping_resolution_m_csa_771_20260523.json
artifacts/v3_mcsa_positive_schema_decision_note_m_csa_737_20260523.json
artifacts/v3_post_mcsa_positive_followup_review_only_zero_import_gate_20260523.json
```

The bounded apo scan identifies candidate selected-PDB replacements for
`m_csa:577` (`1AWB`), `m_csa:641` (`1J7N`), and `m_csa:897` (`1H56`), while
`m_csa:836` and `m_csa:996` stay blocked by non-local structure-wide metal
hits. `artifacts/v3_mcsa_positive_holo_override_import_preview_20260523.json`
reruns those three concrete overrides against the post-clean9 691-label
registry and keeps them separate from the clean9 import: all three top1 as
`metal_dependent_hydrolase`, with 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, and 0 actionable in-scope failures, but 0
import-ready candidates until a post-override expert accept decision and
dedicated gates exist.

The geometry packet keeps `m_csa:657` held because Zn is local to beta-subunit
Glu131 but not both scored residues as direct metal ligands; `m_csa:611` and
`m_csa:1001` remain held on conformation/oligomeric role-pair locality.
`artifacts/v3_mcsa_positive_m_csa771_2d0d_noncanonical_review_20260523.json`
confirms `m_csa:771` alternate PDB `2D0D` contains catalytic Ser103 and maps it
to the M-CSA nucleophile role; the paired gate-preview plan keeps it non-imported
until an explicit noncanonical alternate accept decision and full gates rerun.
`m_csa:737` remains a schema decision gap for coupled PLP-cobalamin aminomutase
chemistry; do not create a production fingerprint from it.

Evidence-based confidence call: confidence is high that the clean9 canonical
import is valid because the derived gate stack passes 21/21 label-factory
checks, the batch acceptance artifact is accepted for exactly nine new labels,
hard negatives and near misses are 0, out-of-scope false non-abstentions are 0,
and the registry validates at 691 labels with 8 fingerprints. Confidence is
medium-high that the next M-CSA work should be post-clean9 holds, not external
breadth: the holo overrides and `m_csa:771` are geometry/gate-preview ready but
still need explicit expert accept artifacts before any import. The caveat rows
`m_csa:777`, `m_csa:784`, and `m_csa:904` remain held.

Wrap validation for the 2026-05-23T19:08:15Z run passed: targeted artifact
tests, 899-test full unit discovery, `compileall`, CLI `validate` at 691 labels
and 8 fingerprints, artifact-migration dry run with `removal_allowed=0`, JSON
parsing for new summary artifacts, and `git diff --check`.

### External Queue: Human Review Or No-Breadth Readiness

The external automation queue is now closed for the seven current
mechanism-match review-ready rows. The latest packet is:

```text
artifacts/v3_external_review_ready_automation_terminal_stop_packet_20260522.json
```

It consolidates the heme, metal, and serine review-ready families after
source-free geometry, current-countable duplicate/TM screens, UniRef90/50
current-reference clearance, and the no-import payload gate. All seven rows
remain `mechanism_match_review_ready`, 0 are import-ready, 0 are countable
candidates, no EC/name/prose/source context is counted as predictive, and the
only remaining blocker for that queue is explicit human accept/reject/ambiguous
action. The paired zero-import gate is:

```text
artifacts/v3_external_review_ready_automation_terminal_stop_packet_zero_import_gate_20260522.json
```

The current non-ePK family queue is:

```text
artifacts/v3_non_epk_family_readiness_index_post_external_stop_20260522.json
```

It covers 17 review-only families: 3 external mechanism-match families blocked
only on human action, 6 existing non-ATP family readiness/blocker packets, and
8 closed non-ePK ATP/phosphoryl-transfer packets. It records 0 import-ready
rows, 0 countable candidates, 0 new external rows, and no permission to start a
broad external mini-campaign.

Do not reopen broad external mini-campaign breadth by default. The next
highest-value action is human review on the seven external rows or the 298
PyMOL-ready M-CSA review rows. If human review is unavailable and the main loop
continues M-CSA readiness, the structure-path-only queue is now drained; work
only the 23 exact mapping blockers unless new human decisions arrive.

Evidence-based confidence call: confidence is high that the external queue is
now automation-terminal but not import-ready because the packet records 7/7
source-free geometry-above-floor rows, 7/7 UniRef-clear rows, 0 high-TM
current-countable duplicate hits, 0 import-ready candidates, 0 countable
candidates, no registry/fingerprint edits, no artifact upload/removal, no
`removal_allowed=true`, and a passing focused regression test plus zero-import
gate. Confidence is also high that the PyMOL bridge remains review-only: all
materializable structure-path-only blocker rows were selected from existing
blocker reports before download, 317 selected/review-context mmCIF sidecars
were committed with 0 fetch failures, the final queue has 298/298 verified
focus-atom selections, and the closure zero-import gate passed.
Wrap validation passed with 893 unit tests, CLI validation at 682 labels and 8
fingerprints, artifact migration dry-run/local-file validation at 113 rows with
`removal_allowed=0`, and an admission guard covering all 113 large files.

### Ready Now: 298-Row PyMOL Review Tranche

The PyMOL structure-path readiness queue is drained. The latest materialized
review queue is:

```text
artifacts/v3_mcsa_pymol_expert_review_queue_1025_all_materialized_20260522.json
```

It scans the same 321 M-CSA expert-review rows, materializes 296 selected PDB
mmCIF structures from 12 frozen rank-ordered readiness tranches plus 21 exact
mapping blocker coordinate-context sidecars, and raises `pymol_ready_count`
from 1 to 298. The queue verifies that both focus CA atom selections are
present in the structure file before marking a row ready.
The first 26 ready rows are `m_csa:670`, `m_csa:643`,
`m_csa:756`, `m_csa:757`, `m_csa:760`, `m_csa:696`, `m_csa:654`, `m_csa:663`,
`m_csa:662`, `m_csa:751`, `m_csa:918`, `m_csa:553`, `m_csa:778`,
`m_csa:793`, `m_csa:792`, `m_csa:676`, `m_csa:947`, `m_csa:995`,
`m_csa:972`, `m_csa:980`, `m_csa:974`, `m_csa:910`, `m_csa:842`,
`m_csa:736`, `m_csa:687`, and the prior `m_csa:939`.
The second tranche adds `m_csa:684`, `m_csa:834`, `m_csa:925`, `m_csa:891`,
`m_csa:711`, `m_csa:984`, `m_csa:767`, `m_csa:943`, `m_csa:787`,
`m_csa:785`, `m_csa:764`, `m_csa:726`, `m_csa:680`, `m_csa:591`,
`m_csa:784`, `m_csa:788`, `m_csa:806`, `m_csa:534`, `m_csa:678`,
`m_csa:659`, `m_csa:761`, `m_csa:938`, `m_csa:807`, `m_csa:731`, and
`m_csa:949`.
The third tranche adds `m_csa:748`, `m_csa:952`, `m_csa:794`, `m_csa:673`,
`m_csa:671`, `m_csa:644`, `m_csa:725`, `m_csa:963`, `m_csa:976`,
`m_csa:724`, `m_csa:951`, `m_csa:880`, `m_csa:847`, `m_csa:510`,
`m_csa:741`, `m_csa:962`, `m_csa:967`, `m_csa:843`, `m_csa:961`,
`m_csa:982`, `m_csa:559`, `m_csa:653`, `m_csa:840`, `m_csa:641`, and
`m_csa:960`.
The fourth tranche adds `m_csa:783`, `m_csa:700`, `m_csa:828`, `m_csa:768`,
`m_csa:999`, `m_csa:873`, `m_csa:829`, `m_csa:779`, `m_csa:755`,
`m_csa:781`, `m_csa:817`, `m_csa:693`, `m_csa:564`, `m_csa:875`,
`m_csa:846`, `m_csa:867`, `m_csa:848`, `m_csa:799`, `m_csa:997`,
`m_csa:803`, `m_csa:832`, `m_csa:734`, `m_csa:858`, `m_csa:835`, and
`m_csa:864`. Later tranches drain the remaining structure-path-only rows and
are summarized in
`artifacts/v3_mcsa_pymol_all_materializable_structure_path_closure_20260522.json`.

Run the human review loop with:

```bash
PYTHONPATH=src python -m catalytic_earth.cli launch-mcsa-pymol-review \
  --queue artifacts/v3_mcsa_pymol_expert_review_queue_1025_all_materialized_20260522.json \
  --out artifacts/v3_expert_review_decision_batch_pymol_manual.json \
  --reviewer vivek
```

The generated PyMOL scripts live under:

```text
artifacts/review_pymol/mcsa_1025_all_materialized_20260522/
```

Safety status: this tranche is review-only. It imports 0 labels, creates 0
countable candidates, edits no registries/fingerprints, and passes the
review-only zero-import gate in
`artifacts/v3_post_mcsa_pymol_all_materializable_closure_review_only_zero_import_gate_20260522.json`.
The remaining blocker report now shows 23 blocked rows and 0 next
structure-materialization candidates, with no remaining structure-path
blocker. Exact missing evidence is a focus CA atom pair/distance repair for 23
rows, including 2 rows that also need source graph/PDB mapping repair before
PyMOL staging.

### PyMOL Human-Review Cockpit

As of the 2026-05-22T17:15:38Z main-loop run, the queued M-CSA PyMOL
expert-review cockpit described in
`work/mcsa_pymol_expert_review_cockpit_plan.md` is implemented as review-only
tooling. `src/catalytic_earth/pymol_review.py` adds bounded queue extraction,
`.pml` generation, dry-run/no-launch review-loop support, and decision-batch
validation. The CLI commands are `build-mcsa-pymol-review-queue`,
`launch-mcsa-pymol-review`, and `validate-mcsa-pymol-review`.

`artifacts/v3_mcsa_pymol_expert_review_queue_1025.json` scans 321 existing
expert-label-decision review rows against the current review-gap and geometry
artifacts. It marks only `m_csa:939` PyMOL-ready because that row has a
committed coordinate sidecar, two mapped CA atoms, and an exact measured
geometry distance. The other 320 rows fail closed with explicit missing fields
instead of guessed structures or atom pairs. The generated script lives under
`artifacts/review_pymol/mcsa_1025/`.

`artifacts/v3_expert_review_decision_batch_pymol_manual_dry_run_20260522.json`
and its validation artifact prove the terminal loop can run without PyMOL on
the automation runner. The dry-run decision is `skipped`, and every output row
has `countable_import_ready=false`. Any real expert decision must still be
converted through the existing expert-review import preview and label-factory
gates before it can count.

Evidence-based confidence call: confidence is high that the cockpit is safe
review-only tooling because the queue and dry-run batch record 0 import-ready
and 0 countable rows, the code never writes the curated label registry or
fingerprint registry, tests cover fail-closed missing atom/structure behavior,
and the generated queue exposes missing evidence instead of filling gaps.

The same run added
`artifacts/v3_glycoside_hydrolase_family_readiness_post_pymol_bridge_packet_20260522.json`
as a no-breadth family-readiness fallback from existing glycoside-control
evidence only. It keeps `Q6NSJ0` as the sole positive-like row, still
`needs_review`: the inverse gate is below all eight current fingerprints, but
the source-free glycoside axis-ready count is 0, current-countable structural
duplicate screening and terminal review remain blockers, and import/countable
candidate counts are 0.

The same no-breadth fallback was also applied to sugar-phosphate isomerase in
`artifacts/v3_sugar_phosphate_isomerase_family_readiness_post_pymol_bridge_packet_20260522.json`.
It uses only existing control/readiness artifacts and keeps `P34949` as the
sole positive-like row, still `needs_review`: source-traced basic-site context
exists, but no source-free sugar-phosphate axis is ready, no ESM sidecar is
available, broader duplicate screening and terminal review remain blockers,
and import/countable candidate counts are 0.

Two additional existing-control family packets were closed in the same
review-only style:
`artifacts/v3_schiff_base_lyase_family_readiness_post_pymol_bridge_packet_20260522.json`
and
`artifacts/v3_dna_glycosylase_lyase_family_readiness_post_pymol_bridge_packet_20260522.json`.
They add no external breadth and keep `Q9BXD5` and `P06746` as single
positive-like `needs_review` rows. In both cases the useful evidence is still
source-traced rather than source-free geometry, broader duplicate screening
and terminal review are unresolved, and import/countable candidate counts are
0.

`artifacts/v3_non_epk_family_readiness_index_post_pymol_bridge_20260522.json`
now indexes AKR, glycoside hydrolase, sugar-phosphate isomerase, Schiff-base
lyase, and DNA glycosylase/lyase in one review-only surface. The index records
0 newly frozen external rows, 0 source-free axis-ready family rows, 0
import-ready candidates, 0 countable candidates, and no permission to start
another broad external mini-campaign.

`artifacts/v3_external_review_ready_human_action_checklist_post_pymol_bridge_20260522.json`
also turns the seven already review-ready external mechanism-match rows into a
single human-action checklist. It preserves the same source separation policy,
requires an accept/reject expert action before any label path can continue,
and authorizes 0 imports or countable labels.

The run-level safety gate
`artifacts/v3_post_pymol_review_only_zero_import_gate_20260522.json` validates
the nine new review-only outputs as 9/9 closed: 0 import-ready rows, 0
countable rows, no curated-label or fingerprint registry edits, and no
artifact upload/removal. The corresponding reusable CLI is
`validate-review-only-zero-import-artifacts`.

As of the 2026-05-22T18:17:37Z main-loop run, the automation used that
human-review-only external state to run one bounded non-ePK source-free axis
experiment rather than opening new external breadth.
`src/catalytic_earth/sdr_active_site.py` adds a review-only SDR catalytic-axis
probe that scans coordinate sequences for Tyr-X-X-X-Lys motifs and then
requires Tyr OH/Lys NZ geometry while excluding EC, names, UniProt prose,
source active-site annotations, and curated labels from predictive use.

`artifacts/v3_sdr_source_free_axis_probe_post_pymol_20260522.json` applies the
probe to the already frozen 14-row SDR/AKR/NAD(P) control tranche. Twelve rows
have committed coordinates, five resolve source-free Tyr/Lys geometry, and 0
resolve a full SDR axis because every available structure lacks a local
NAD(P)-like ligand site. The probe also catches the reason motif geometry is
not enough: two resolved motif-only hits are non-SDR controls (`C9JRZ8` and
`m_csa:208`). SDR is therefore converted from a generic source-free-axis gap
to `blocked_with_exact_missing_evidence`: it needs a preregistered NAD(P)
ligand/pocket proxy or holo coordinates, broader duplicate screening, terminal
review, and label-factory gates before any production claim.

The companion benchmark
`artifacts/v3_sdr_source_free_axis_probe_modern_baseline_benchmark_20260522.json`
records EC/keyword routing, deterministic sequence-motif, Foldseek, and ESM
caveats on the same frozen rows. It makes no geometry superiority claim:
Foldseek duplicate screening and ESM/learned sidecars are absent for this SDR
probe. `artifacts/v3_non_epk_family_readiness_index_post_sdr_axis_probe_20260522.json`
adds SDR to the no-breadth family index, and
`artifacts/v3_post_sdr_axis_probe_review_only_zero_import_gate_20260522.json`
validates the five new review-only artifacts as 5/5 zero-import and
zero-countable. The two extra artifacts are
`artifacts/v3_external_review_ready_human_decision_batch_template_post_sdr_20260522.json`
and its validation file; they turn the seven external mechanism-match rows
into a fillable pending decision batch with the allowed terminal vocabulary
while keeping human acceptance separate from label import.

Evidence-based confidence call: confidence is high that SDR remains blocked
for the right reason because the probe is frozen to existing rows, reports 0
NAD(P)-like ligand sites and 0 full SDR-axis-ready rows, and exposes non-SDR
motif-only controls. Confidence is high that no import path opened because the
new packets record 0 import-ready and 0 countable candidates, no registry or
fingerprint edits, no artifact upload/removal, and no `removal_allowed=true`.

As of the 2026-05-22T19:18:23Z main-loop run, the automation kept the same
no-breadth posture and consolidated the SDR/AKR NAD(P)-redox blocker instead
of opening another family or external tranche.
`artifacts/v3_nadp_redox_family_source_free_cofactor_blocker_queue_post_sdr_20260522.json`
records the shared exact blocker: 0 source-free NAD(P) ligand/proxy-ready
rows, SDR motif-only geometry is unsafe because two non-SDR controls also
resolve YxxxK geometry, and AKR remains source-traced rather than source-free.
The follow-on pressure test
`artifacts/v3_sdr_nadp_pocket_proxy_pressure_test_post_blocker_20260522.json`
implements the strict SDR `[ST]GxxxGxG` pocket proxy over the same 14 frozen
rows using only mmCIF coordinates, residue/ligand comp IDs, atom names,
coordinate-derived sequence order, distances, and local contacts. It resolves
`O14756`, filters out the prior loose V-motif heme-control hit, but also
resolves the external SDR control `O75828`; AKR `C9JRZ8` still lacks a
source-free NAD(P)/Tyr-Lys-His axis. EC, names, UniProt/source prose, source
active-site annotations, and curated labels remain excluded from predictive
evidence.
`artifacts/v3_nadp_redox_holo_or_specificity_source_request_queue_post_proxy_20260522.json`
then converts that pressure-test result into three exact review-only evidence
requests: holo/local NAD(P)-like coordinates or a source-free specificity
counteraxis for `O14756`, terminal specificity adjudication for `O75828`, and
a source-free AKR NADP/Tyr-Lys-His coordinate axis for `C9JRZ8`.

`artifacts/v3_non_epk_family_readiness_index_post_nadp_cofactor_blocker_20260522.json`
keeps the six non-ePK family packets review-only and adds that cross-family
cofactor blocker as the next exact no-breadth item. The broad external
mini-campaign item remains `do_not_start_by_default`, while the seven
external mechanism-match rows remain pending human accept/reject/ambiguous
action. `artifacts/v3_post_nadp_cofactor_blocker_review_only_zero_import_gate_20260522.json`
validates the four new/updated artifacts as 4/4 zero-import and
zero-countable.

Evidence-based confidence call: confidence is high that the NAD(P)-redox
families are blocked on the right evidence axis because SDR and AKR now point
to the same missing source-free cofactor ligand/proxy rather than separate
generic `needs_review` buckets, and the strict proxy already shows why pocket
motif evidence alone is not specific enough. Confidence is high that no import
or production path opened because the artifacts record 0 import-ready
candidates, 0 countable candidates, no new external rows, no
registry/fingerprint edits, no artifact upload/removal, and no
`removal_allowed=true`.

As of the 2026-05-22T04:01:49Z main-loop run, the automation closed the
remaining queued redox source-free geometry/structure blockers without adding
external mini-campaign breadth. `src/catalytic_earth/redox_active_site.py`
adds coordinate-only heme/flavin active-site extraction, with focused unit
coverage in `tests/test_redox_active_site.py`. The new extractor uses only
mmCIF atom coordinates, residue/ligand comp ids, atom names, and distances;
EC, protein names, UniProt prose, and curated labels are excluded from
predictive scoring.

`artifacts/v3_external_redox_third_blocker_coordinate_materialization_20260522.json`
materializes the frozen PDB structures `1EB7` for `P14532`, `3W9Z` for
`P33371`, and `4G6G` for `P32340` before outcome scoring. The source-free
geometry artifact
`artifacts/v3_external_redox_third_blocker_source_free_geometry_scores_20260522.json`
resolves all three cofactor active-site packets and top-ranks the intended
current fingerprint lanes above the `0.4115` floor: `P14532` to
`heme_peroxidase_oxidase` at `0.8605`, `P33371` to
`flavin_dehydrogenase_reductase` at `0.8976`, and `P32340` to
`flavin_dehydrogenase_reductase` at `0.8994`.

The targeted current-lane Foldseek/TM screen
`artifacts/v3_external_redox_third_blocker_targeted_current_lane_duplicate_screen_20260522.json`
finds high-TM current-FDR duplicate/leakage signals for `P33371` (`TM 0.7573`)
and `P32340` (`TM 0.7559`), converting both to terminal
`terminal_rejection_duplicate_or_leakage`. `P14532` has no targeted heme hit
above `0.7`, so
`artifacts/v3_heme_peroxidase_p14532_full_current_countable_duplicate_screen_20260522.json`
runs the full 672-target current-countable screen and completes 672/672 pairs
with no high-TM hit; nearest current-countable TM is `0.6413`. The terminal
packet
`artifacts/v3_external_redox_third_blocker_terminal_decision_packet_after_source_free_geometry_and_screens_20260522.json`
therefore marks `P14532` `mechanism_match_review_ready` for review only, with
0 import-ready rows and 0 countable candidates. The companion benchmark records
EC/keyword routing and sequence k-mer routing as baselines, explicitly records
ESM sidecar absence, and makes no superiority claim.

`artifacts/v3_external_deep_remaining_blocker_queue_post_redox_third_closure_20260522.json`
now has 0 source-free geometry/structure blockers. The remaining external deep
blockers are the five earlier mechanism-match review-ready rows blocked on
external seed-fingerprint policy, full label-factory payload gates, and human
label action. The rollup
`artifacts/v3_external_deep_terminal_decision_rollup_post_redox_third_closure_20260522.json`
indexes 82 deep-packet rows: 73 duplicate/leakage terminal rejections, 6
mechanism-match review-ready rows, 3 insufficient-evidence terminal
rejections, 0 exact blockers, 0 import-ready rows, and 0 countable candidates.
The import-readiness check preserves the 682-label registry invariant, 212
`seed_fingerprint`, 470 `out_of_scope`, 8 production fingerprints, and the
only external imports remain `uniprot:P06744`, `uniprot:P78549`, and
`uniprot:Q3LXA3`.

The follow-up no-import payload dry run
`artifacts/v3_external_mechanism_match_review_ready_seed_fingerprint_payload_dry_run_20260522.json`
now packages all six mechanism-match review-ready rows as draft
seed-fingerprint payloads while keeping every row non-countable. It makes the
next import-gate blockers explicit: no external seed-fingerprint counting
policy is preregistered, full label-factory payload gates have not run, no
human label action was requested, and the two metal phosphatase rows still
lack source-free phosphate/substrate specificity for phosphatase-specific
import claims. `artifacts/v3_external_p14532_uniref_current_reference_screen_20260522.json`
now closes the matching UniRef90/50 current-reference overlap screen for
`P14532` with 0 overlaps.

As of the 2026-05-22T07:16:17Z main-loop run, the automation advanced that
same import-gate surface without importing labels or adding external breadth.
`artifacts/v3_external_seed_fingerprint_label_factory_payload_gate_check_20260522.json`
reruns the full label-factory gate against the current 682-label registry for
the external seed-fingerprint payload dry run. It is intentionally no-import
and records an exact blocker rather than hiding it: 20/21 gates pass, but
`applied_label_actions_ready` fails because the current label-factory gate is
still a 1,000-slice/M-CSA applied-label gate and lacks a current-682 external
seed-fingerprint payload adapter/rebaseline.
`artifacts/v3_external_seed_fingerprint_policy_preregistration_and_payload_gate_dry_run_20260522.json`
preregisters a review-only external seed-fingerprint counting policy for the
six existing `mechanism_match_review_ready` rows, keeps source-free geometry
and duplicate evidence separated from review-only EC/name/prose/source
context, confirms all six rows remain above the source-free geometry floor and
UniRef90/50 current-reference-clear, and confirms the external-source transfer
gate is still green at 68/68. Import remains closed with 0 import-ready rows,
0 countable candidates, 0 external seed-fingerprint labels, and unchanged
registry invariants: 682 labels, 212 `seed_fingerprint`, 470 `out_of_scope`,
and external out-of-scope imports exactly `uniprot:P06744`, `uniprot:P78549`,
and `uniprot:Q3LXA3`. The two metal rows (`P0A8Y5` and `P75792`) still retain
the source-free phosphate/substrate specificity blocker before any
phosphatase-specific import claim.
`artifacts/v3_external_metal_phosphatase_review_ready_phosphate_specificity_blocker_packet_20260522.json`
turns that metal blocker into an exact evidence packet: selected/PDB-linked
coordinate scans cover five structures, detect 0 phosphate-like
substrate/product/analog sites near the source-free metal clusters, and keep
both metal rows `blocked_with_exact_missing_evidence` with a concrete next
experiment: find/materialize a coordinate holo or analog structure, or
preregister a source-free phosphate-pocket extractor.

Evidence-based confidence call: confidence is high that no import occurred
because both new artifacts set `ready_for_label_import=false`, record 0
import-ready/countable rows, preserve external imported seed-fingerprint labels
as `[]`, and only add review-only artifacts plus a regression test. Confidence
is high that the next gate blocker is exact because the fresh label-factory
gate artifact records `gate_count=21`, `passed_gate_count=20`, and blockers
exactly `["applied_label_actions_ready"]`; the paired policy artifact names
the required next experiment as a current-682 external seed-fingerprint payload
adapter/rebaseline followed by another no-import gate rerun. Confidence is
high that safety rails were preserved: no registry/fingerprint edits, no
artifact upload/removal/externalization, no Git-LFS/history rewrite, no
threshold change, and no `removal_allowed=true`.

As of the 2026-05-22T08:46:13Z main-loop run, the automation deepened the two
review-ready metal rows without importing labels. The new packet
`artifacts/v3_external_metal_phosphatase_review_ready_phosphate_specificity_blocker_packet_20260522.json`
scans the selected PDB structures plus prefrozen sampled PDB cross-references:
`P75792` scans `1RLM`, `1RLO`, `1RLT`, and `2HF2`; `P0A8Y5` scans `1RKQ`.
The source-free metal-site extractor uses only mmCIF atom coordinates,
residue/ligand comp ids, atom names, and distances. Across five coordinate
structures it finds 0 phosphate-like ligand sites and 0 source-free
phosphate/substrate ligand contexts. Both rows remain
`mechanism_match_review_ready`, but phosphatase-specific import is now
`blocked_with_exact_missing_evidence`: a coordinate holo/analog structure with
phosphate-like substrate/product context, or a preregistered source-free
phosphate-pocket extractor, is required before any external seed-fingerprint
payload gate can count them. The packet carries the same EC/keyword, sequence
k-mer, Foldseek, and ESM sidecar caveats as the prior metal benchmark and makes
no superiority claim.

Evidence-based confidence call: confidence is high that the metal
phosphate/substrate blocker is now exact for the current sampled coordinate
surface because the packet records 5/5 scanned structures, 2 committed
coordinate sidecars, 3 RCSB review fetches with SHA-256 hashes, 0 phosphate-like
site counts, and 0 structures with a phosphate-like ligand. Confidence is high
that no label action occurred because the packet records 0 import-ready rows,
0 countable candidates, 0 external seed-fingerprint imports, and unchanged
registry invariants at 682 labels. Confidence is high that source separation is
preserved because all scan rows set text/name/source predictive usage to false.

As of the 2026-05-22T09:34:39Z main-loop run, the automation deepened the
remaining already frozen serine-hydrolase rows and closed the only new exact
blocker. `artifacts/v3_serine_hydrolase_third_deep_packet_selection_20260522.json`
selects six rows from the 2026-05-21 frozen serine-hydrolase campaign that
were not in the first two serine deep packets and were not exact
current-reference sequence duplicates. The selection is frozen before source-
free geometry or Foldseek outcome scoring, and it adds 0 external rows.
`artifacts/v3_serine_hydrolase_third_deep_packet_source_free_triad_scores_20260522.json`
uses coordinate-only Ser-His-Asp/Glu triad extraction with EC/name/UniProt
prose excluded from predictive evidence. Five rows resolve source-free triads;
`Q9UL19` does not and is terminal
`terminal_rejection_insufficient_evidence`.

The targeted current-Ser-His screen
`artifacts/v3_serine_hydrolase_third_deep_packet_targeted_current_ser_his_screen_20260522.json`
converts four above-floor rows (`P13001`, `A0A0B5LB55`, `F7IX06`, and
`Q09LX1`) to terminal `terminal_rejection_duplicate_or_leakage`. `P15776`
clears the 40-structure targeted Ser-His screen, so
`artifacts/v3_serine_hydrolase_p15776_full_current_countable_duplicate_screen_20260522.json`
runs the full current-countable duplicate/leakage screen across 672 selected
current structures. It completes 1,831 query-target rows, finds 0
`TM >= 0.7` hits, and records nearest max TM `0.626` to `pdb:1EHK`.
The final packet
`artifacts/v3_serine_hydrolase_third_deep_terminal_decision_packet_after_p15776_full_current_screen_20260522.json`
therefore marks `P15776` `mechanism_match_review_ready` for review only.
The post-third-serine rollup
`artifacts/v3_external_deep_terminal_decision_rollup_post_third_serine_full_current_20260522.json`
indexes 88 deep-packet rows: 77 duplicate/leakage terminal rejections, 7
mechanism-match review-ready rows, 4 insufficient-evidence terminal
rejections, 0 exact blockers, 0 import-ready candidates, and 0 countable label
candidates. The companion benchmark records EC/keyword routing, deterministic
sequence/k-mer, Foldseek, and missing ESM sidecar caveats and makes no
superiority claim.

Evidence-based confidence call: confidence is high that the third serine
packet is source-separated because all source-free score rows set
`text_or_label_fields_used_for_score=false` and the packet keeps EC/name/source
context review-only. Confidence is high that `P15776` is review-ready rather
than import-ready because the full-current screen is complete with no
`TM >= 0.7` duplicate signal, while the readiness artifact still records 0
import-ready candidates, 0 countable candidates, no external seed-fingerprint
imports, and unchanged 682-label registry invariants. Confidence is high that
the remaining blocker count is 0 for the indexed deep-packet surface because
the final rollup records `exact_blocker_candidate_count=0`. Final wrap checks
passed 836-test unit discovery, CLI validation with 682 labels and 8
fingerprints, compileall, artifact migration dry-run with `removal_allowed=0`,
new JSON parsing, `git diff --check`, and no registry/fingerprint diffs.

As of the 2026-05-22T10:29:21Z main-loop follow-up, the automation converted
the new `P15776` review-ready row into seven-row no-import import-gate
readiness. `artifacts/v3_external_p15776_uniref_current_reference_screen_20260522.json`
fetches `UniRef90_P15776` and `UniRef50_P15776`, intersects their member
accessions against the 735 current countable reference accessions, and finds 0
overlaps and 0 fetch failures. The evidence role is explicitly duplicate
control only, not positive mechanism evidence. The new readiness packet
`artifacts/v3_external_seed_fingerprint_seven_review_ready_import_gate_readiness_20260522.json`
accounts for all seven `mechanism_match_review_ready` external rows across
heme, metal, and serine-hydrolase lanes. It records 7/7 source-free geometry
above floor, 7/7 UniRef90/50 current-reference clearance, 0 import-ready
candidates, 0 countable candidates, no label or fingerprint edits, and the
unchanged 682-label registry invariant. The current label-factory payload gate
still blocks exactly on `applied_label_actions_ready`; the expanded seven-row
payload gate was not rerun because the current-682 external seed-fingerprint
payload adapter/rebaseline is still missing. The two metal rows still retain
the source-free phosphate/substrate specificity blocker before any
phosphatase-specific import claim.

Evidence-based confidence call: confidence is high that this follow-up only
advanced gate readiness, not imports, because both new artifacts set
`ready_for_label_import=false`, `countable_label_candidate_count=0`, no
external seed-fingerprint labels are present, and at that point the only
label-factory blocker was the preregistered adapter/rebaseline gap. Confidence is high
that the P15776 UniRef screen is source-separated because the artifact records
UniRef as duplicate/leakage evidence only and keeps EC/name/source context out
of predictive mechanism evidence.

As of the 2026-05-22T11:25:41Z main-loop follow-up, the automation closed that
current-682 adapter blocker as a no-import gate rerun. The new adapter artifact
`artifacts/v3_external_seed_fingerprint_applied_labels_1000_currentregistry_payload_adapter.json`
applies the 1,000-slice label-factory audit to the current 682-label registry,
preserving 212 `seed_fingerprint`, 470 `out_of_scope`, and the three imported
external out-of-scope labels while producing a 682-row applied-label artifact.
The rerun gate
`artifacts/v3_external_seed_fingerprint_seven_row_payload_gate_check_1000_currentregistry_adapter.json`
passes 21/21 gates with 0 blockers. The decision artifact
`artifacts/v3_external_seed_fingerprint_seven_row_payload_gate_rerun_no_import_decision_20260522.json`
keeps all seven mechanism-match rows review-only with 0 import-ready and 0
countable candidates. The adapter blocker is resolved for this no-import dry
run, but label import remains closed because human label action was not
requested and `mechanism_match_review_ready` is not itself an import decision.
The metal rows (`P0A8Y5` and `P75792`) still also require source-free
phosphate/substrate specificity. The companion packet
`artifacts/v3_external_seed_fingerprint_nonmetal_human_review_packet_20260522.json`
separates the five non-metal rows (`I2DBY1`, `K7N5M8`, `P14532`, `P39597`, and
`P15776`) as human-review-ready, not import-ready. The benchmark
`artifacts/v3_external_seed_fingerprint_seven_row_post_gate_modern_baseline_benchmark_20260522.json`
records the same seven-row surface against EC/keyword routing, deterministic
sequence/UniRef controls, Foldseek/TM duplicate screens, and absent ESM
sidecars; it explicitly makes no geometry-superiority claim.

Evidence-based confidence call: confidence is high that the adapter blocker is
closed only for a no-import dry run because the rerun gate records
`passed_gate_count=21`, `gate_count=21`, and `blockers=[]`, while the decision
packet still sets `ready_for_label_import=false`,
`import_ready_candidate_count=0`, and `countable_label_candidate_count=0`.
Confidence is high that registry safety rails were preserved because the
adapter and decision artifacts both retain 682 labels, 212 seed fingerprints,
470 out-of-scope labels, external out-of-scope imports exactly
`uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`, and 0 external
seed-fingerprint imports. Confidence is high that source separation remains
intact because all packet rows keep source-free geometry as predictive evidence
and keep EC/name/prose/source context excluded from predictive scoring.
Confidence is high that the benchmark caveats are explicit because it records
`geometry_superiority_claim=false`, `esm_or_learned_embedding_sidecar_available_count=0`,
and 0 import-ready/countable candidates.

As of the 2026-05-22T12:57:22Z main-loop run, the automation continued PLP
deepening on existing frozen rows only. The new selection artifact
`artifacts/v3_plp_aminotransferase_second_deep_packet_selection_20260522.json`
freezes the next seven non-exact-reference PLP aminotransferase rows from the
2026-05-21 mini-campaign (`Q96255`, `Q56YA5`, `P22256`, `Q93ZN9`, `P42588`,
`H8WR05`, and `Q988B8`) after excluding the first seven PLP deep rows and the
two exact current-reference sequence duplicates. It freezes 0 new external
rows and records EC/protein-name/UniProt context as review-only selection
context.

`artifacts/v3_plp_aminotransferase_second_deep_packet_source_free_active_site_geometry_scores_20260522.json`
materializes seven PDB coordinate sidecars and applies the existing
coordinate-only PLP extractor. Four selected coordinates resolve complete
source-free PLP active-site packets and score above the `plp_dependent_enzyme`
floor with 0 text/label fields used; two have a PLP-like site without a
resolved covalent/modified lysine anchor, and one lacks a PLP-like coordinate
site. The targeted current-PLP Foldseek screen
`artifacts/v3_plp_aminotransferase_second_deep_packet_targeted_current_plp_screen_20260522.json`
then finds `TM >= 0.7` current-countable PLP duplicate/leakage signals for all
four source-free-ready rows. The terminal packet
`artifacts/v3_plp_aminotransferase_second_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260522.json`
therefore records four `terminal_rejection_duplicate_or_leakage` rows and
three `terminal_rejection_insufficient_evidence` rows, with 0
mechanism-match review-ready rows, 0 import-ready candidates, and 0 countable
candidates. The companion benchmark records EC/keyword, deterministic
sequence/k-mer, Foldseek/TM, and missing ESM sidecar caveats with no
geometry-superiority claim. The PLP-specific rollup now covers 14 deep rows:
10 duplicate/leakage terminal rejections and 4 insufficient-evidence terminal
rejections.

Evidence-based confidence call: confidence is high that the second PLP packet
is source-separated because the four scored rows use only coordinate-derived
PLP/LLP/PMP/P5P anchor/residue evidence and all rows keep EC/name/source
context out of predictive scoring. Confidence is high that the four
above-floor PLP rows are terminal duplicate/leakage rejections because each has
a targeted current-countable PLP Foldseek `TM >= 0.7` signal. Confidence is
high that the three non-scored rows are terminal insufficient-evidence
decisions for the selected frozen coordinates, not hard negatives or
import-ready rows. Confidence is high that safety rails were preserved: no
label import, registry edit, fingerprint edit, threshold change, artifact
upload/removal, Git-LFS migration, history rewrite, or `removal_allowed=true`
occurred.

As of the 2026-05-22T15:20:31Z main-loop run, the automation closed the
remaining non-exact-reference PLP aminotransferase rows from the frozen
2026-05-21 mini-campaign without adding breadth. The selection artifact
`artifacts/v3_plp_aminotransferase_third_deep_packet_selection_20260522.json`
freezes the last four previously unselected non-exact rows (`Q72LL6`,
`O50131`, `Q8NTR2`, and `P96060`) before source-free geometry or Foldseek
outcome scoring. The coordinate directory
`artifacts/v3_plp_aminotransferase_third_deep_packet_pdb_coordinates_20260522`
materializes the selected PDB structures `2EGY`, `7VNO`, `3PPL`, and `1M32`.

`artifacts/v3_plp_aminotransferase_third_deep_packet_source_free_active_site_geometry_scores_20260522.json`
uses the coordinate-only PLP extractor with EC/name/UniProt/PLP annotation
context excluded from predictive evidence. `Q72LL6` and `O50131` resolve
complete source-free PLP active-site packets and score above the
`plp_dependent_enzyme` floor (`0.9876` and `0.9833`). `Q8NTR2` and `P96060`
have PLP-like context but no resolved covalent/modified lysine anchor packet,
so they are not scored as source-free PLP active sites. The targeted
current-PLP Foldseek screen
`artifacts/v3_plp_aminotransferase_third_deep_packet_targeted_current_plp_screen_20260522.json`
finds current-countable PLP duplicate/leakage signals for the two
source-free-ready rows (`Q72LL6` nearest TM `0.8649`, `O50131` nearest TM
`0.9302`). The terminal packet
`artifacts/v3_plp_aminotransferase_third_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260522.json`
therefore records two `terminal_rejection_duplicate_or_leakage` rows and two
`terminal_rejection_insufficient_evidence` rows. The benchmark
`artifacts/v3_plp_aminotransferase_third_deep_packet_modern_baseline_benchmark_20260522.json`
keeps EC/keyword and sequence baselines review/duplicate context only,
records Foldseek/TM as duplicate/leakage evidence only, records ESM sidecar
absence, and makes no geometry-superiority claim. The rollup
`artifacts/v3_plp_aminotransferase_deep_terminal_decision_rollup_post_third_plp_20260522.json`
now covers all 18 non-exact-reference PLP deep rows: 12 duplicate/leakage
rejections and 6 insufficient-evidence rejections, with 0 import-ready rows and
0 countable candidates.

Evidence-based confidence call: confidence is high that the remaining PLP
frozen rows are now terminal for the selected-coordinate surface because the
third selection artifact covers the only four non-exact rows left after the
first two packets and the two exact current-reference sequence duplicates.
Confidence is high that the two above-floor PLP rows are duplicate/leakage
terminal rejections because both have targeted current-countable PLP Foldseek
signals above `TM >= 0.7`. Confidence is high that the two non-scored rows are
insufficient-evidence terminal decisions rather than hard negatives because
their selected coordinates lack a complete source-free lysine-anchor PLP
packet. Confidence is high that safety rails remain intact: no label import,
registry edit, fingerprint edit, threshold change, artifact upload/removal,
Git-LFS migration, history rewrite, or `removal_allowed=true` occurred.

The companion active queue
`artifacts/v3_external_remaining_blocker_queue_post_third_plp_closure_20260522.json`
prevents the next run from reopening broad sourcing by default. It records 0
remaining source-free geometry/structure blockers, five non-metal
mechanism-match review-ready rows blocked on human review/explicit label
action, and two metal review-ready rows blocked on source-free
phosphate/substrate specificity. It explicitly sets
`start_new_broad_external_minicampaign=false`, preserves 682 labels with 212
seed fingerprints and 470 out-of-scope labels, and keeps external imports at
only `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`.

The no-import human checklist
`artifacts/v3_external_nonmetal_human_review_acceptance_checklist_post_plp_closure_20260522.json`
turns the five non-metal mechanism-match rows into explicit row-level
acceptance criteria. All five already have source-free target-lane geometry
above floor, current-countable duplicate screening, and UniRef current-reference
clearance, but the checklist keeps them non-countable and requires expert
accept/reject/needs-evidence action before any future label path. It preserves
source separation by rejecting EC/name/UniProt prose or source annotations as
predictive evidence.

The metal phosphate-specificity preregistration
`artifacts/v3_metal_phosphatase_phosphate_specificity_extractor_preregistration_20260522.json`
turns the two remaining metal blockers into one exact review-only experiment.
It freezes only `P0A8Y5` and `P75792`, allows only coordinate/ligand/residue
atom data and distances as predictive inputs, and requires a phosphate-like
ligand or preregistered pocket proxy near the existing source-free metal
cluster before phosphatase specificity can advance. It does not run the
extractor, calibrate thresholds, authorize production scoring, or import
labels.

As of the 2026-05-22T16:13:35Z main-loop run, the automation implemented that
preregistered metal phosphate-pocket proxy without opening new external
breadth. `src/catalytic_earth/metal_active_site.py` now exposes
`extract_source_free_metal_phosphatase_pocket_proxy`, which uses only mmCIF atom
coordinates, residue/ligand comp IDs, atom names, chain/residue identifiers,
and distances. It keeps EC labels, names, UniProt prose, source annotations,
curated labels, and post-hoc threshold changes out of predictive evidence.
Focused tests in `tests/test_metal_active_site.py` cover both proxy-resolved and
still-blocked synthetic coordinate cases.

`artifacts/v3_metal_phosphatase_phosphate_pocket_proxy_extractor_test_20260522.json`
runs the extractor on the already selected committed metal-row coordinates
only: `P0A8Y5`/`1RKQ` and `P75792`/`1RLM`. Both rows retain source-free metal
clusters and resolve the preregistered 6.0 Angstrom polar/basic pocket proxy:
`P0A8Y5` has 5 non-metal-ligand pocket contacts with 3 polar/basic contacts,
and `P75792` has 4 non-metal-ligand pocket contacts with 2 polar/basic
contacts. The rows remain `mechanism_match_review_ready` and review-only, with
0 import-ready candidates and 0 countable candidates. The companion benchmark
`artifacts/v3_metal_phosphatase_phosphate_pocket_proxy_modern_baseline_benchmark_20260522.json`
records EC/keyword routing, deterministic sequence-kmer controls, Foldseek/TM
duplicate evidence, and absent ESM sidecars for the same frozen rows, with no
geometry-superiority or production-scoring claim.

`artifacts/v3_external_seed_fingerprint_all_review_ready_human_packet_after_metal_proxy_20260522.json`
then consolidates the five non-metal rows and the two metal rows into one
no-import human-review packet. It records 7/7 source-free geometry-above-floor
rows, 7/7 UniRef current-reference-clear rows, 0 current-countable high-TM
duplicate hits, and 2/2 metal phosphate-pocket proxies resolved. The remaining
blocker class is now explicit human/expert label action for all seven rows; the
packet starts no broad external mini-campaign and authorizes no import,
registry edit, fingerprint edit, threshold calibration, or production score.

Evidence-based confidence call: confidence is high that the immediate metal
phosphate/substrate blocker is now resolved only to review-ready status, not
import readiness, because the new packet records 2/2 pocket proxies detected,
0 import-ready candidates, 0 countable candidates, no registry or fingerprint
edits, and source-context predictive usage count 0. Confidence is high that the
active external no-breadth queue is now human-review-only because the
seven-row packet records 0 source-free geometry/structure blockers and 0 metal
phosphate-specificity blockers. Confidence is moderate on the scientific
strength of the pocket proxy because it is a preregistered coordinate-only
review feature rather than a calibrated production score; any future label path
still needs human/expert action and controls.

The fallback family-readiness packet
`artifacts/v3_akr_family_readiness_post_third_plp_no_breadth_packet_20260522.json`
uses only existing AKR/SDR readiness artifacts plus that no-breadth queue. AKR
stays review-only and production no-go: one source-traced positive-like row
(`C9JRZ8`), 0 source-free AKR axis-ready rows, 0 import-ready candidates, and
0 countable candidates. The exact next experiment, if AKR is reopened, is a
preregistered source-free NADP/Tyr-Lys-His geometry axis with AKR-specific
duplicate screening and SDR/flavin/heme/PLP/out-of-scope counterfamily
controls; it is not started by this packet.

Evidence-based confidence call: confidence is high that the AKR packet is a
bounded readiness fallback rather than a new sourcing campaign because it
freezes 0 new rows, uses only prior artifacts, excludes EC/name/prose/source
annotations from predictive evidence, and keeps `decision_to_start_now=false`.

Evidence-based confidence call: confidence is high that the redox geometry
blockers are closed because all three rows have PDB coordinate sidecars,
source-free cofactor active-site extraction, and target-lane scores above the
floor with text/source fields excluded. Confidence is high that `P33371` and
`P32340` are terminal duplicate/leakage rejections because the targeted
current-FDR screen completed all 98 query-target pairs and both have
`TM >= 0.7` current-FDR hits. Confidence is high that `P14532` is
mechanism-match review-ready, not import-ready, because source-free heme
geometry is above floor and the full current-countable screen completed all
672 pairs with no `TM >= 0.7` hit, while external seed-fingerprint policy and
full label-factory gates are still absent. Confidence is high that no label
import, registry edit, fingerprint edit, threshold change, artifact
upload/removal, Git-LFS migration, history rewrite, or `removal_allowed=true`
occurred. Confidence is high that the payload dry run is non-importing because
all six rows carry `payload_status=draft_review_only_not_imported`, all six
now have UniRef90/50 current-reference no-overlap evidence, import-ready and
countable candidates remain 0, and the registry invariant is unchanged at 682
labels.

As of the 2026-05-22T03:17Z main-loop run, the automation kept the main work
on existing external decisions while doing only a concise ePK lane synthesis.
`artifacts/v3_epk_post_late_decision_synthesis_20260522.json` integrates the
fresh research-lane handoffs and ledgers after the previous late synthesis.
It records `8UYH` as one review-only clean active-state ePK candidate for
policy-harness adjudication, preserves `5UJ7:biological_assembly_1` as the
context-v4-only split counterexample, keeps the 119-row sibling-control surface
as a future scorer-test fixture, and records folded-Tyr reciprocal/product/ADP
and same-chain substrate-role classes as terminal review-only under the
current source-free policy. No ePK production scoring, threshold calibration,
label import, registry edit, fingerprint edit, or artifact migration action is
authorized; the main-loop action remains external terminal-decision deepening
and import-gate readiness.

The same run advanced the existing mechanism-match review-ready external rows
without importing labels. `artifacts/v3_external_mechanism_match_review_ready_uniref_payload_plan_20260522.json`
screens all five review-ready rows from
`artifacts/v3_external_mechanism_match_review_ready_import_blocker_matrix_20260522.json`
against UniRef90/50 cluster members and the 735 current countable reference
accessions. All five (`I2DBY1`, `P75792`, `P0A8Y5`, `P39597`, and `K7N5M8`)
have 0 current-reference cluster overlaps and 0 fetch failures, so the current
UniRef90/50 duplicate-overlap blocker is removed for these rows. They remain
review-only and not import-ready: full label-factory gates have not run, no
external seed-fingerprint counting policy has been preregistered for these
rows, no human label action was requested, and the metal phosphatase rows still
lack source-free phosphate/substrate specificity.

The run also closed the remaining frozen heme-peroxidase rows that could be
decided from existing sequence evidence. `artifacts/v3_heme_peroxidase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522.json`
selects the five previously unselected heme rows from the 2026-05-21 frozen
mini-campaign. Four rows (`P21179`, `P00431`, `P04963`, and `P48534`) are exact
current-reference sequence duplicates and are terminal
`terminal_rejection_duplicate_or_leakage` rows without geometry scoring or
import claims. `P14532` is not an exact sequence duplicate but remains
`needs_new_extractor_or_structure` with one exact blocker: source-free heme
active-site geometry scoring plus current-countable structural duplicate
screening are still missing. The companion benchmark
`artifacts/v3_heme_peroxidase_third_deep_packet_sequence_duplicate_closure_modern_baseline_benchmark_20260522.json`
records that EC/keyword routing is review context only, deterministic sequence
closed four rows, and geometry/Foldseek/ESM sidecars are absent for the
remaining blocker, so no superiority claim is made.

The run then closed the same sequence-duplicate class for the remaining frozen
flavin dehydrogenase/reductase rows. `artifacts/v3_flavin_dehydrogenase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522.json`
selects six previously unselected rows from the existing 2026-05-21 frozen
mini-campaign. Four rows (`P15559`, `P0AEZ1`, `P38489`, and `P42593`) are
exact current-reference sequence duplicates and are terminal
`terminal_rejection_duplicate_or_leakage` rows without geometry scoring or
import claims. `P33371` and `P32340` are not exact sequence duplicates but
remain `needs_new_extractor_or_structure` with one exact blocker: source-free
flavin dehydrogenase active-site geometry scoring plus current-countable
structural duplicate screening are still missing. The companion benchmark
`artifacts/v3_flavin_dehydrogenase_third_deep_packet_sequence_duplicate_closure_modern_baseline_benchmark_20260522.json`
records that EC/keyword routing is review context only, deterministic sequence
closed four rows, and geometry/Foldseek/ESM sidecars are absent for the two
remaining blockers, so no superiority claim is made.

Finally, `artifacts/v3_external_deep_remaining_blocker_queue_20260522.json`
packages the remaining actionable external blockers without adding rows or
opening import. It queues five mechanism-match review-ready rows behind a
review-only label-factory payload dry run and explicit external seed-
fingerprint policy, and queues `P14532`, `P33371`, and `P32340` for the next
coordinate materialization, source-free geometry, and current-countable
structural duplicate screens. The queue is non-countable, review-only, and
explicitly excludes EC/name/source prose from predictive evidence.

Evidence-based confidence call: confidence is high that the UniRef90/50
current-reference overlap screen completed for the five review-ready rows
because 10 candidate clusters fetched successfully and all overlap counts are
0 against the current 735-reference accession set. Confidence is medium that
this materially reduces duplicate/leakage risk because it is a current-
reference cluster screen, not a full future label-factory import decision.
Confidence is high that import remains closed because every row still carries
explicit full-gate and policy blockers and the registry invariants remain 682
labels, 212 `seed_fingerprint`, 470 `out_of_scope`, with external imports
limited to `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`.
Confidence is high that the four heme third-packet duplicate rejections are
terminal for this scope because exact current-reference sequence identity is a
leakage/holdout condition independent of source-free mechanism scoring.
Confidence is high for the same reason that the four FDR third-packet
duplicate rejections are terminal for this scope. Confidence is medium for the
`P33371` and `P32340` blockers because they are exact missing-evidence
statements, not terminal mechanism decisions.
Confidence is high that the blocker queue is a planning artifact only because
it carries 0 import-ready rows, 0 countable candidates, no registry/fingerprint
edits, and no new frozen external breadth.

As of the 2026-05-22T00:57Z main-loop run, the external deepening ladder
continued on already frozen rows only. No new external mini-campaign rows were
frozen. The second flavin dehydrogenase/reductase packet selected seven
previously unselected non-exact-reference rows from the existing 2026-05-21
campaign: `P77258`, `P41407`, `Q8LAH7`, `P0AEN1`, `Q07923`, `P21375`, and
`Q9FUP0`. Coordinates were materialized for all seven, active/binding-site
features mapped for five, and the source-free geometry score artifact used 0
EC/name/label/prose fields. A targeted current
`flavin_dehydrogenase_reductase` Foldseek/TM screen completed all 343
query-target pairs against 49 current FDR structures and found a `TM >= 0.7`
current-FDR structural duplicate signal for every row. The terminal packet
`artifacts/v3_flavin_dehydrogenase_second_deep_terminal_decision_packet_after_targeted_fdr_screen_20260521.json`
therefore converts all seven to `terminal_rejection_duplicate_or_leakage`, with
0 import-ready rows, 0 countable rows, and no duplicate-clear or superiority
claim.

The same run then deepened a second heme-peroxidase packet from already frozen
rows: `P11678`, `P39597`, `P31545`, `Q39034`, `K7N5M8`, `Q47KB1`, and
`P49012`. All seven AlphaFold coordinates were materialized and all seven
mapped active/heme-binding feature sets; source-free geometry top-ranked all
seven to `heme_peroxidase_oxidase` above the `0.4115` floor with 0 text/name
fields used. The targeted current-heme Foldseek/TM screen completed all 140
query-target pairs against 20 current heme structures and converted four rows
(`P11678`, `Q39034`, `Q47KB1`, and `P49012`) to terminal
`terminal_rejection_duplicate_or_leakage`. The follow-up full current-countable
screen
`artifacts/v3_heme_peroxidase_second_deep_packet_full_current_countable_screen_20260521.json`
then closed the exact blocker for the three targeted-clear rows by covering
2016/2016 query-target pairs against 672 unique staged current-countable
structures. `P31545` has a high-TM current-countable hit to `pdb:1IR3`
(`TM 0.7041`) and is a terminal duplicate/leakage rejection. `P39597` and
`K7N5M8` have no `TM >= 0.7` current-countable hit, with nearest TMs `0.6930`
and `0.6747`; the updated terminal packet
`artifacts/v3_heme_peroxidase_second_deep_terminal_decision_packet_after_full_current_screen_20260521.json`
marks them `mechanism_match_review_ready` for review only.
The independent rerun artifact
`artifacts/v3_heme_peroxidase_second_deep_packet_full_current_countable_duplicate_screen_20260521.json`
reproduces the same 3-row status split and keeps the Foldseek/TM evidence
strictly in the duplicate/leakage screen role.

The latest rollup
`artifacts/v3_external_deep_terminal_decision_rollup_post_second_heme_full_current_screen_20260521.json`
now indexes 71 deep-packet rows with 63 duplicate/leakage terminal rejections,
five mechanism-match-review-ready rows, three insufficient-evidence terminal
rejections, 0 exact `needs_new_extractor_or_structure` blockers, 0 import-ready
candidates, and 0 countable label candidates. The post-full-current
import-readiness artifact
`artifacts/v3_external_deep_terminal_import_gate_readiness_check_post_second_heme_full_current_screen_20260521.json`
keeps the label gate closed: registry invariants remain 682 labels, 212
`seed_fingerprint`, 470 `out_of_scope`, and the only imported external labels
remain `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`.
The review-ready import blocker matrix
`artifacts/v3_external_mechanism_match_review_ready_import_blocker_matrix_20260522.json`
then collects the five mechanism-match rows and keeps all five explicitly
blocked from import pending UniRef-wide duplicate evidence and full
label-factory payload gates.

Evidence-based confidence call: confidence is high that the seven second FDR
rows are terminal duplicate/leakage rejections because the targeted current-FDR
screen is complete and every row has a `TM >= 0.7` current-lane hit. Confidence
is high that the four second-heme duplicate rows are terminal rejections for
the same targeted-lane reason. Confidence is high that `P31545` is a terminal
duplicate/leakage rejection because the full current-countable screen found a
`TM >= 0.7` hit. Confidence is medium-high, not import-ready, that `P39597`
and `K7N5M8` are mechanism-match review-ready because source-free heme geometry
is above floor and full current-countable duplicate screening is bounded-clear,
but no UniRef-wide or full label-factory gate evidence has run. Confidence is
high that no label
import, registry edit, fingerprint edit, threshold change, artifact
upload/removal, Git-LFS migration, history rewrite, or `removal_allowed=true`
occurred. Next work should continue another already frozen deep packet or build
import-gate evidence around review-ready rows; do not add broad external row
breadth by default.

As of the 2026-05-21T23:32:51Z main-loop run, the remaining frozen
metal-phosphatase blockers are closed with source-free coordinate evidence and
the next serine-hydrolase ladder item has moved from generic review to terminal
decision packets. The run added the coordinate-only metal-site extractor in
`src/catalytic_earth/metal_active_site.py` and tests in
`tests/test_metal_active_site.py`. It scores the last three rows from the
already frozen metal-phosphatase mini-campaign in
`artifacts/v3_metal_phosphatase_remaining_source_free_geometry_scores_20260521.json`
without EC/name/UniProt prose or labels as predictive input. `P75792` and
`P0A8Y5` resolve Mg/Asp-Ser metal-ligand clusters, top1 to
`metal_dependent_hydrolase` above the `0.4115` floor (`0.6758` and `0.6774`),
and already had bounded current-countable duplicate clearance. The updated
terminal packet
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_source_free_geometry_20260521.json`
therefore marks them `mechanism_match_review_ready` for the broad current
metal-dependent hydrolase lane while explicitly preserving the no-import
caveat that no source-free phosphate/substrate ligand is present. `P77247`
remains `terminal_rejection_duplicate_or_leakage`.

The same run continued to the next ladder item without adding new external
rows. It added `src/catalytic_earth/serine_active_site.py` plus
`tests/test_serine_active_site.py`, selected five rows from the already frozen
serine-hydrolase mini-campaign in
`artifacts/v3_serine_hydrolase_second_deep_packet_selection_20260521.json`,
materialized their PDB coordinates, and wrote
`artifacts/v3_serine_hydrolase_second_deep_packet_source_free_triad_scores_20260521.json`.
Four rows (`P16233`, `Q9FG13`, `P54318`, and `P0ADA1`) resolve coordinate-only
Ser-His-Asp/Glu triads and score above the `ser_his_acid_hydrolase` floor.
The targeted current-serine Foldseek screen
`artifacts/v3_serine_hydrolase_second_deep_packet_targeted_current_ser_his_screen_20260521.json`
then finds `TM >= 0.7` current-countable serine-hydrolase signals for all four,
so
`artifacts/v3_serine_hydrolase_second_deep_terminal_decision_packet_after_targeted_ser_his_screen_20260521.json`
converts them to `terminal_rejection_duplicate_or_leakage`. `Q9NWW9` lacks a
source-free triad in selected `4DPZ` and is
`terminal_rejection_insufficient_evidence`. The latest rollup
`artifacts/v3_external_deep_terminal_decision_rollup_post_second_serine_targeted_screen_20260521.json`
now indexes 57 deep-packet rows with 51 duplicate/leakage rejections, three
mechanism-match-review-ready rows, three insufficient-evidence rejections, 0
`needs_new_extractor_or_structure` rows, 0 import-ready rows, and 0 countable
labels.

The follow-up import-readiness artifact
`artifacts/v3_external_deep_terminal_import_gate_readiness_check_post_second_serine_20260521.json`
keeps the gate closed: registry invariants remain 682 labels, 212
`seed_fingerprint`, 470 `out_of_scope`, the only imported external labels are
still `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`, and no current
deep-packet row has the hard-negative inverse-gate or label-factory payload
required for import.

Evidence-based confidence call: confidence is high that the last two
metal-phosphatase blockers are no longer extractor-missing because their
coordinate-only Mg-ligand clusters score above floor and their bounded
current-countable duplicate screens were already complete with 0 `TM >= 0.7`
hits. Confidence is medium, not high, on phosphate-specific interpretation
because no source-free phosphate/substrate ligand is present, so the packet is
review-ready only for the broad current metal-dependent hydrolase lane and not
label-import-ready. Confidence is high that the four second-selection serine
rows are terminal duplicate/leakage rejections because each has a targeted
current-serine `TM >= 0.7` hit after source-free triad scoring. Confidence is
high that Q9NWW9 is insufficient for the selected coordinate because no
coordinate triad met the preregistered distance cutoffs. Confidence is high
that no label import, registry edit, fingerprint edit, threshold change,
artifact upload/removal, Git-LFS migration, history rewrite, or
`removal_allowed=true` occurred. Next work should continue with bounded
existing-packet flavin/heme work or another exact blocker; do not add broad
external rows by default.

As of the 2026-05-21T22:30:59Z main-loop run, the remaining second
metal-phosphatase blocker is closed for the bounded current-countable selected
structure screen. The run did not freeze new external rows. It continued the
already selected Q99504 row from
`artifacts/v3_metal_phosphatase_deep_packet_second_selection_20260521.json`,
completed non-metal current-countable Foldseek chunks002-007, and wrote
`artifacts/v3_metal_phosphatase_q99504_full_current_countable_duplicate_closure_20260521.json`.
Across the prior metal-lane probe, the targeted rescue-only structures, and
all eight non-metal chunks, Q99504 now has 672/672 bounded current-countable
query-target pairs covered, 0 `TM >= 0.7` duplicate/leakage hits, and nearest
max TM `0.6185` to `pdb:1EHK`.

The updated terminal packet
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_second_after_q99504_duplicate_closure_20260521.json`
therefore changes only Q99504's decision: it is no longer
`needs_new_extractor_or_structure`, but it is also not a mechanism match or
hard-negative import candidate. It is now
`terminal_rejection_insufficient_evidence` because the source-free
metal-hydrolase geometry score remains below the active `0.4115` floor
(`0.3742`), only two active-site residues are resolved, and no source-free
phosphate/substrate-binding feature is present. The companion benchmark
`artifacts/v3_metal_phosphatase_deep_packet_second_after_q99504_duplicate_closure_modern_baseline_benchmark_20260521.json`
keeps EC/keyword routing, deterministic sequence/k-mer, Foldseek, and missing
ESM sidecar caveats separated and makes no superiority claim.
`artifacts/v3_external_deep_terminal_decision_rollup_post_q99504_duplicate_closure_20260521.json`
now indexes 49 deep-packet rows with 49 non-`needs_review` terminal outcomes,
0 import-ready candidates, and 0 countable labels.

The same run also deepened the last three rows from the same frozen
metal-phosphatase campaign without adding new external rows.
`artifacts/v3_metal_phosphatase_deep_packet_remaining_selection_20260521.json`
selects P75792, P77247, and P0A8Y5 after the earlier 14 frozen rows had been
selected. `artifacts/v3_metal_phosphatase_deep_packet_remaining_coordinate_materialization_20260521.json`
materializes three PDB coordinate sidecars, and
`artifacts/v3_metal_phosphatase_deep_packet_remaining_targeted_current_metal_screen_20260521.json`
screens them against the 67 current-countable `metal_dependent_hydrolase`
structures. P77247 has a high-TM targeted current-metal duplicate/leakage
signal to `pdb:1RQL` at max TM `0.8110`, so
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_targeted_metal_screen_20260521.json`
sets it to `terminal_rejection_duplicate_or_leakage`. P75792 and P0A8Y5 remain
`needs_new_extractor_or_structure` with exact blockers: source-free geometry
scoring and full current-countable duplicate screening. The post-remaining
metal rollup
`artifacts/v3_external_deep_terminal_decision_rollup_post_remaining_metal_targeted_screen_20260521.json`
now covers 52 deep-packet rows, with 47 duplicate/leakage rejections, two
insufficient-evidence rejections, one mechanism-match review-ready row, two
exact blockers, 0 import-ready candidates, and 0 countable labels.

The same run then completed the duplicate-screen half of those two exact
blockers. The non-metal Foldseek chunks
`artifacts/v3_metal_phosphatase_remaining_nonmetal_chunk000_probe_20260521.json`
through
`artifacts/v3_metal_phosphatase_remaining_nonmetal_chunk007_probe_20260521.json`
cover 605 non-metal current-countable targets for P75792 and P0A8Y5, with 0
`TM >= 0.7` hits. Combined with the 67-target current-metal screen, the closure
artifact
`artifacts/v3_metal_phosphatase_remaining_full_current_countable_duplicate_closure_20260521.json`
now covers 672/672 bounded current-countable targets per row, 1,344 blocker-row
pairs total, 0 high-TM duplicate/leakage hits, nearest P75792 max TM `0.6855`
to `pdb:2PHK`, and nearest P0A8Y5 max TM `0.6392` to `pdb:1L7N`. This permits
only a bounded current-countable duplicate-clear statement, not UniRef-wide or
external-cluster clearance. The follow-up packet
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_full_current_duplicate_closure_20260521.json`
keeps P75792 and P0A8Y5 at `needs_new_extractor_or_structure` because no
source-free geometry score exists yet; their exact blocker is now
`source_free_geometry_scoring_missing_for_pdb_active_site_features_after_bounded_duplicate_clearance`.
The updated benchmark and rollup
`artifacts/v3_metal_phosphatase_deep_packet_remaining_after_full_current_duplicate_closure_modern_baseline_benchmark_20260521.json`
and
`artifacts/v3_external_deep_terminal_decision_rollup_post_remaining_metal_full_current_duplicate_closure_20260521.json`
make no superiority claim and keep all 52 indexed deep rows review-only with 0
import-ready candidates.

The run added the existing-evidence AKR/NADP readiness recheck
`artifacts/v3_akr_family_readiness_post_q99504_terminal_recheck_20260521.json`.
It preserves the production no-go: C9JRZ8 remains the only source-traced
positive-like AKR row, the 14-row SDR/AKR tranche still has 0 source-free
axis-ready rows, direct local NADP geometry is missing, broader duplicate
screening remains unresolved for positive-like AKR rows, and source
annotations/EC/name/prose are excluded from predictive evidence.

Fresh ePK research-lane handoffs were synthesized once, without copying
production changes, in
`artifacts/v3_epk_late_handoff_only_research_lane_synthesis_20260521.json`.
The conclusion still keeps ePK off the main-loop critical path: Haspin/H3
`4OUC` is source-site-only with no active donor, acid/base proximity is a
review feature rather than a substrate-role rule, `5UJ7` biological assembly 1
remains pinned as the context-v4-only split counterexample, policy v9 now asks
only for a real `metal_absent` review row, and the sibling lane certifies a
119-row review-only control surface for future scorer tests. No production
scoring, label import, threshold change, registry edit, or fingerprint
expansion is authorized.

Evidence-based confidence call: confidence is high that Q99504's previous
duplicate-screen blocker is resolved for the bounded current-countable
selected-structure scope because every one of the 672 staged current targets is
covered with no high-TM hit and 0 raw-name mapping failures in the chunk
artifacts. Confidence is medium-high that the correct terminal decision is
`terminal_rejection_insufficient_evidence`, not mechanism-match review-ready,
because the source-free target-lane score remains below floor and the active
site is under-resolved. Confidence is high that P77247 is a terminal
duplicate/leakage rejection for this review packet because the targeted
current-metal screen completed and found a `TM >= 0.7` current-countable signal;
confidence is high that P75792 and P0A8Y5 no longer have a bounded
current-countable duplicate-screen blocker because all 672 staged current
targets per row are covered with 0 high-TM signals. Confidence is lower only on
their mechanism outcome because source-free geometry scoring is still missing.
Confidence is high that no
label import, registry edit,
fingerprint edit, threshold change, artifact migration, upload/removal,
Git-LFS migration, history rewrite, or `removal_allowed=true` occurred.
Next work should not reopen Q99504 unless a future UniRef-wide/import-gate
cycle is explicitly requested; the two exact metal blockers are now P75792 and
P0A8Y5 source-free geometry scoring from resolved active-site/metal/phosphate
features, or a single preregistered non-ePK source-free family-axis experiment.
Do not resume ePK as the default main-loop task; use the synthesis artifact
only to route isolated research lanes.

As of the 2026-05-21T21:29:56Z main-loop run, the automation deepened the
remaining already frozen metal-phosphatase surface instead of opening another
external mini-campaign. The second selection artifact
`artifacts/v3_metal_phosphatase_deep_packet_second_selection_20260521.json`
freezes seven previously unselected rows from the same 17-row metal-phosphatase
campaign before new geometry or Foldseek scoring, with 0 new external rows
frozen and 0 exact current-reference sequence duplicates.

The run staged seven AlphaFold v6 coordinate sidecars, mapped all seven
UniProt active-site feature sets, and scored the rows against the current
8-fingerprint universe with 0 text/name/label fields used. The bounded
current-countable Foldseek screen
`artifacts/v3_metal_phosphatase_deep_packet_second_current_countable_structural_screen_20260521.json`
completed 5/7 queries against the 672 staged current-countable structures and
found `TM >= 0.7` duplicate/leakage signals for all five completed rows:
`O14595`, `O15194`, `P0AF24`, `Q42546`, and `P0A8Y3`. `Q99504` and `P05186`
timed out and remain exact blockers, not duplicate-clear or mechanism-match
claims.
The bounded timeout rescue
`artifacts/v3_metal_phosphatase_deep_packet_second_timeout_targeted_rescue_screen_20260521.json`
then tested those two timeout rows against the small homologous current subset
`1T7D`, `1RTF`, and `1ALK`. It converted `P05186` to a targeted
current-countable duplicate/leakage rejection and left `Q99504` as the single
exact blocker because no targeted high-TM signal was detected.
The follow-up Q99504 metal-lane probe
`artifacts/v3_metal_phosphatase_q99504_current_metal_target_probe_20260521.json`
then completed all 67 current-countable `metal_dependent_hydrolase` target
structures with 0 high-TM hits (nearest `1L7N`, max TM `0.5324`), narrowing
the remaining blocker to the non-metal current-countable target surface or an
alternate coordinate/target subset.
`artifacts/v3_metal_phosphatase_q99504_current_nonmetal_chunk000_probe_20260521.json`
then completed the first 80 non-metal current-countable targets with 0
high-TM hits (nearest `1B93`, max TM `0.5951`). This further narrows, but does
not clear, Q99504 duplicate risk. Chunk001
`artifacts/v3_metal_phosphatase_q99504_current_nonmetal_chunk001_probe_20260521.json`
also completed 80/80 target pairs with 0 high-TM hits (nearest `1D8D`, max TM
`0.5232`).

The terminal packet
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_second_after_timeout_rescue_20260521.json`
therefore records six `terminal_rejection_duplicate_or_leakage` rows and one
`needs_new_extractor_or_structure` row. The modern-baseline companion
`artifacts/v3_metal_phosphatase_deep_packet_second_after_timeout_rescue_modern_baseline_benchmark_20260521.json`
keeps EC/keyword routing, deterministic 5-mer sequence nearest-neighbor,
geometry triage, Foldseek/TM, and missing ESM sidecar caveats separated and
makes no superiority claim. The new rollup
`artifacts/v3_external_deep_terminal_decision_rollup_post_second_metal_timeout_rescue_20260521.json`
now indexes 49 deep-packet rows across seven packet surfaces: 46
duplicate/leakage rejections, one insufficient-evidence rejection, one
review-only heme mechanism-match row, and one exact current-countable
duplicate-screen blocker. Import-ready count remains 0.

Evidence-based confidence call: confidence is high that the six completed or
target-rescued second-selection metal rows are terminal duplicate/leakage rejections because
each completed an exhaustive exact-TM current-countable screen with at least
one `TM >= 0.7` current-countable signal and 0 raw-name mapping failures, or
the targeted rescue found the same class of current-countable high-TM signal.
Confidence is high that `Q99504` should remain `needs_new_extractor_or_structure`
because the all-current query timed out and the targeted homolog subset
completed without a high-TM hit; the metal-lane subset also completed with 0
high-TM hits, and non-metal chunk000 completed with 0 high-TM hits. Any future
Q99504 closure needs the remaining non-metal all-current subchunks after
chunk001 or a different coordinate/target subset. Otherwise, continue
deepening existing frozen nonterminal surfaces or write a family-readiness
packet.

As of the 2026-05-21T20:27:57Z main-loop run, the frozen PLP
aminotransferase blocker is no longer an extractor-missing surface. The new
source-free extractor module `src/catalytic_earth/plp_active_site.py` maps
PLP/LLP/PMP/P5P-like coordinate sites, covalent or modified lysine anchors,
nearby acid/base residues, and phosphate-binding residues without using EC,
protein names, UniProt prose, PLP annotations, or curated labels as predictive
input. It is regression-tested in `tests/test_plp_active_site.py`.

The PLP deep packet now has three review-only evidence layers. First,
`artifacts/v3_plp_aminotransferase_deep_packet_source_free_active_site_geometry_scores_20260521.json`
materializes the seven selected PDB coordinate sidecars, resolves complete
source-free PLP active-site triplets for six rows, and scores all six to the
current `plp_dependent_enzyme` lane above the `0.4115` floor with top1 PLP and
0 text/label fields used. `Q9NZ45`/`2QD0` has no PLP-like coordinate site and
is not scored. Second,
`artifacts/v3_plp_aminotransferase_deep_packet_targeted_current_plp_screen_20260521.json`
screens the six source-free-ready rows against the 30 current countable PLP
structures with Foldseek exact TM-score; all six have targeted current-PLP
`TM >= 0.7` duplicate/leakage signals (`Q8TD30` 0.8071 to `pdb:1B8G`,
`Q9Y617` 0.9473 to `pdb:1BJO`, `O07566` 0.8675 to `pdb:1B9H`, `P53555`
0.8953 to `pdb:1DTY`, `Q9S7N2` 0.8100 to `pdb:1B8G`, and `P50457` 0.9429 to
`pdb:1D7R`). Targeted Foldseek is import-gate leakage evidence only and does
not establish duplicate-clear.

The terminal packet
`artifacts/v3_plp_aminotransferase_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260521.json`
therefore records six `terminal_rejection_duplicate_or_leakage` rows and one
`terminal_rejection_insufficient_evidence` row (`Q9NZ45`). The companion
benchmark
`artifacts/v3_plp_aminotransferase_deep_packet_post_source_free_anchor_modern_baseline_benchmark_20260521.json`
keeps EC/keyword routing, deterministic 5-mer sequence nearest-neighbor,
Foldseek/TM, and missing ESM sidecar caveats separate and makes no superiority
claim. No label import, registry edit, fingerprint edit, threshold change,
artifact upload/removal, externalization, Git-LFS migration, history rewrite,
or `removal_allowed=true` occurred.

Evidence-based confidence call: confidence is high that the PLP extractor
removed the exact source-free active-site blocker for six frozen rows because
the coordinate-only PLP/LLP anchor triplets score the PLP lane without text
fields and all six then hit current countable PLP structures above the leakage
threshold. Confidence is also high that these are terminal rejection packets,
not mechanism-match evidence, because targeted high-TM current-PLP leakage
supersedes the above-floor PLP geometry signal. `Q9NZ45` is a terminal
insufficient-evidence rejection for the selected frozen PDB, not a clean
hard-negative or wrong-scope import row; any future attempt would need a newly
frozen alternate coordinate source with observed PLP-like active-site evidence.

The same run added the review-only SDR readiness recheck
`artifacts/v3_sdr_family_readiness_post_plp_terminal_review_packet_20260521.json`
using existing artifacts only. It freezes no new external rows and explicitly
keeps SDR at `needs_new_extractor_or_structure`: source-traced O14756
YxxxK/NAD(P) proxy evidence, 36/36 clean SDR abstention context, and the
14-row SDR/AKR/NADP control tranche are useful review context, but there is
still no source-free NAD(P) ligand/proxy geometry axis, no source-free
Ser/Tyr/Lys local catalytic-axis policy, no broader duplicate screen for
positive-like rows, and no terminal external decision packet. The next exact
SDR experiment is preregistered design only, not started now.

For planning continuity, the run also wrote
`artifacts/v3_external_deep_terminal_decision_rollup_post_plp_20260521.json`.
It rolls up the six existing deep-packet lanes without freezing new rows:
42 frozen external rows now have non-`needs_review` terminal outcomes across
metal phosphatase, serine hydrolase, flavin dehydrogenase/reductase, flavin
monooxygenase, heme peroxidase, and PLP. The aggregate is 40
`terminal_rejection_duplicate_or_leakage`, one
`terminal_rejection_insufficient_evidence`, and one
`mechanism_match_review_ready` review-only heme row. Import-ready count remains
0 and the rollup is planning context only. The rollup deliberately derives
aggregate terminal counts from terminal-decision maps, and records the stale
serine summary-counter mismatch it found as a consistency check.
Next main-loop work should continue deepening existing frozen/nonterminal
surfaces or write a concise family-readiness packet, not open another broad
external mini-campaign.

As of the 2026-05-21T19:26:53Z recovery/wrap run, the main loop preserved and
validated the coherent stale-lock dirty work rather than opening another broad
external mini-campaign. The late ePK synthesis artifact
`artifacts/v3_epk_late_lane_decision_synthesis_20260521.json` integrates five
research-lane handoff/ledger digests, pins
`5UJ7:biological_assembly_1` as the current context-v4-only biological-assembly
split residual, and keeps ePK `no_go_review_only`. It explicitly recommends
returning to non-ePK external terminal packets; no ePK scorer, threshold,
registry edit, label import, fingerprint expansion, artifact upload/removal,
or main-loop ePK resumption is authorized.

The same recovered work closes the frozen serine-hydrolase P31614 blocker as a
terminal duplicate/leakage rejection, not as a mechanism match. The new
full-current replacement-coordinate duplicate probe
`artifacts/v3_serine_hydrolase_p31614_full_current_alignment_duplicate_probe_20260521.json`
screens P31614 PDB replacements 4C7L and 4C7W against all 672 current-countable
selected structures and completes 1,344/1,344 query-target pairs. 4C7L finds a
current-countable high-TM signal to `pdb:1IR3` at max pair TM `0.7213`; 4C7W
does not. Because any high-TM current-countable signal is enough for terminal
leakage rejection, the updated packet
`artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_full_current_probe_20260521.json`
sets all seven frozen serine rows to
`terminal_rejection_duplicate_or_leakage`. The active-site triad mapping is
still unresolved and no duplicate-clear, mechanism-match, import, or
superiority claim is made. The companion benchmark
`artifacts/v3_serine_hydrolase_deep_packet_post_p31614_full_current_probe_modern_baseline_benchmark_20260521.json`
keeps EC/keyword, deterministic 5-mer, geometry, atom-site mapping, Foldseek,
and missing ESM sidecar caveats separated.

The recovered PLP aminotransferase follow-up is deliberately a blocker packet.
`artifacts/v3_plp_aminotransferase_deep_packet_selection_20260521.json` freezes
seven non-exact-reference rows from the existing PLP mini-campaign before any
deep outcome scoring. `artifacts/v3_plp_aminotransferase_deep_blocker_packet_after_pdb_cofactor_probe_20260521.json`
fetches the selected PDB coordinates in memory only, observes PLP-like tokens
for six of seven rows, writes no raw coordinate files, scores no production
fingerprint, runs no full-current duplicate screen, and records all seven rows
as `needs_new_extractor_or_structure`. The exact next experiment is a
source-free PLP/LLP/PMP/P5P covalent-anchor and catalytic-residue extractor,
then full current-countable duplicate/leakage screening on the same frozen
selection. The companion benchmark records EC/keyword routing and sequence
diagnostics only, with no superiority claim.

Evidence-based confidence call: confidence is high that the recovered serine
packet is now terminal for duplicate/leakage rejection because the
full-current replacement-coordinate screen completed with a current-countable
TM >= 0.7 signal and pair-cache completeness. Confidence is also high that the
serine result is not mechanism-match or import evidence because the active-site
triad mapping remains unresolved and duplicate-clear is not claimed. Confidence
is medium-high that the PLP packet is the right next blocker artifact rather
than a terminal mechanism decision: it confirms coordinate/PDB availability and
PLP-like token presence, but the project still lacks the source-free covalent
PLP active-site extractor needed before geometry scoring or duplicate-clear
screening. Next main-loop work should implement that PLP extractor or choose
another already frozen nonterminal deep-packet blocker; do not add broad
external row breadth.

As of the 2026-05-21T17:24:23Z automation run, the main loop stayed on the
already frozen FMO deep packet and closed the two remaining nonterminal rows
without adding external candidate breadth. The new chunk-003 follow-up
artifact
`artifacts/v3_flavin_monooxygenase_deep_packet_chunk003_followup_screen_20260521.json`
screens `O94851` and `Q7RTP6` against the next 48 current selected structures
as eight six-target Foldseek subchunks per row. All 16 subchunks complete and
both rows find current-structure `TM >= 0.7` duplicate/leakage signals against
`pdb:1DOC` (`m_csa:131`, `flavin_monooxygenase`): `0.7196` for `O94851` and
`0.7250` for `Q7RTP6`. The supplemental chunk-004 artifact
`artifacts/v3_flavin_monooxygenase_deep_packet_chunk004_followup_screen_20260521.json`
also finds high-TM signals against `pdb:1EHK` before some subchunks time out;
it is corroborating evidence only, not a duplicate-clear claim.

The terminal packet
`artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk004_followup_20260521.json`
now records all seven frozen FMO rows as
`terminal_rejection_duplicate_or_leakage`. `O94851` and `Q7RTP6` no longer
have an exact missing-evidence blocker because a current-structure high-TM
signal is sufficient for terminal leakage rejection; pair-cache completion
remains false and no duplicate-clear claim is made. The benchmark
`artifacts/v3_flavin_monooxygenase_deep_packet_chunk004_followup_modern_baseline_benchmark_20260521.json`
keeps EC/keyword and sequence baselines diagnostic only, records ESM as
unavailable, treats Foldseek/TM only as import-gate duplicate/leakage evidence,
and makes no superiority, import, or production-scoring claim.

The same run also wrote the review-only P31614 active-site blocker artifact
`artifacts/v3_serine_hydrolase_p31614_pdb_active_site_mapping_blocker_20260521.json`.
It keeps the frozen `P31614` row at `needs_new_extractor_or_structure` and
sharpens the exact missing evidence: the replacement PDB coordinates do not
carry a direct `P31614` struct-ref, catalytic position 45 is observed as an
engineered Ser-to-Ala mutant, and source charge-relay positions 342/345 are
absent from the atom-site auth numbering in both 4C7L and 4C7W. The prior
PDB-replacement Foldseek screen still contributes only targeted duplicate
diagnostics against 40 current serine-hydrolase structures; it does not
establish a full-current duplicate-clear claim. The updated terminal packet
`artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_active_site_mapping_20260521.json`
therefore preserves the six serine duplicate/leakage rejections and keeps
`P31614` as a single exact-blocked
`needs_new_extractor_or_structure` row. The companion benchmark
`artifacts/v3_serine_hydrolase_deep_packet_post_p31614_active_site_mapping_modern_baseline_benchmark_20260521.json`
keeps EC/keyword, 5-mer sequence, geometry, atom-site mapping, Foldseek, and
ESM evidence surfaces separated and makes no superiority claim.

Evidence-based confidence call: confidence is high that the FMO terminal
packet is source-separated and review-only, and high that the two formerly
blocked rows now have reproducible current-structure duplicate/leakage
evidence under the same full-current Foldseek/TM convention used by the prior
FMO screens. Confidence is high that this is terminal rejection evidence, not a
mechanism-match or import path. Confidence is medium-high that `P31614` needs
a new coordinate or explicit alignment before it can become review-ready,
because the available PDB replacements do not resolve the source triad. Next
main-loop work should either run that one bounded `P31614` alignment/full-current
duplicate experiment or choose the next already frozen nonterminal external
deep-packet blocker, rather than opening a new broad mini-campaign.

As of the 2026-05-21T15:54:00Z automation run, the main loop integrated the
freshest ePK research-lane outputs only where they changed the no-go decision
surface, then returned to the frozen FMO deep packet. The synthesis artifact
`artifacts/v3_epk_latest_lane_regression_synthesis_20260521.json` keeps ePK
review-only and not production-ready across five lanes: the positive lane emits
0 fresh candidate rows, the false-positive lane preserves
`5UJ7:biological_assembly_1` as the unique context-v4-only split residual while
the 343-row regression gate stays fail-closed, sibling controls keep a
119-row negative scenario matrix, the policy harness rolls 16 rows into eight
entry-level review-only units, and substrate-role graph motifs localize but do
not resolve the `9UUR`/`9UUX`/`9UW4` and `3TM0`/`6NOO` biology ambiguity. No
ePK scorer, threshold, registry edit, label import, fingerprint expansion,
artifact upload/removal, or main-loop ePK task is authorized.

The same run closed the next FMO blocker without adding new broad external row
surface. `artifacts/v3_flavin_monooxygenase_deep_packet_geometry_scores_20260521.json`
scores all seven already frozen FMO deep-packet rows against the eight current
fingerprints using only mapped local cofactor/active-site coordinate evidence.
All seven score successfully with 0 text/name/label fields used; only `H3JQW0`
barely reaches the FMO lane floor (`0.4127` versus `0.4115`), and every row is
top-ranked instead to `flavin_dehydrogenase_reductase`, so no mechanism-match
claim is made from geometry alone.

The full-current follow-up screen
`artifacts/v3_flavin_monooxygenase_deep_packet_full_current_subchunk_screen_20260521.json`
then screens the four previously unresolved FMO rows against the 672 staged
current-countable structures in target subchunks. `H3JQW0` and `Q6F4M8`
complete 672/672 query-target pairs each and have current-countable
`TM >= 0.7` duplicate/leakage signals (`0.7646` and `0.8831` maximum pair TM).
`O94851` and `Q7RTP6` time out on their first current-countable target chunk,
so their pair caches are incomplete and no duplicate-clear claim is permitted.
The terminal packet
`artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_geometry_and_full_current_screen_20260521.json`
now records five `terminal_rejection_duplicate_or_leakage` rows and two
`needs_new_extractor_or_structure` rows. The exact blocker for `O94851` and
`Q7RTP6` is complete full current-countable duplicate/leakage screening after
the subchunk timeout or pair-cache gap. The benchmark
`artifacts/v3_flavin_monooxygenase_deep_packet_post_geometry_full_current_modern_baseline_benchmark_20260521.json`
keeps EC/keyword and sequence baselines diagnostic only, records ESM as
unavailable, records Foldseek/TM as import-gate duplicate/leakage evidence
only, and makes no superiority, import, or production-scoring claim.

`artifacts/v3_flavin_monooxygenase_deep_packet_timeout_chunk000_rescue_probe_20260521.json`
narrows the two remaining FMO blockers by splitting the timed-out first
current-countable target chunk into eight six-target subchunks per candidate.
`O94851` completes seven subchunks and times out only on subchunk 7; `Q7RTP6`
completes five subchunks and times out on subchunks 1, 6, and 7. No completed
subchunk has a `TM >= 0.7` high-TM signal, but neither candidate has a complete
pair cache, so no duplicate-clear or terminal-upgrade claim is allowed.
`artifacts/v3_flavin_monooxygenase_deep_packet_timeout_chunk000_size2_rescue_probe_20260521.json`
then splits the remaining timed subchunks into two-target retries. This closes
the chunk-000 timeout surface for `O94851` with 0 high-TM hits and narrows
`Q7RTP6` to one still-timed two-target retry under parent subchunk 1. `Q7RTP6`
therefore remains blocked by that exact retry plus the unrun remaining
full-current chunks; `O94851` remains blocked by the unrun remaining
full-current chunks.

Evidence-based confidence call: confidence is high that the FMO geometry
scores are source-separated and text-free for the seven frozen rows. Confidence
is high that `H3JQW0` and `Q6F4M8` are terminal duplicate/leakage rejections
under the current-countable structural screen, and high that the three earlier
targeted-FMO rejections remain terminal. Confidence is medium on `O94851` and
`Q7RTP6` because the blocker is now exact but unresolved: one two-target
chunk-000 retry still times out for `Q7RTP6`, and the rest of full-current
screening remains incomplete for both rows. Next main-loop work should either
finish that specific `Q7RTP6` retry and then continue the remaining
current-countable chunks for `O94851`/`Q7RTP6`, or run the bounded `P31614` PDB
active-site mapping plus full-current duplicate-screen probe; do not open new
broad external mini-campaign breadth.

As of the 2026-05-21T14:40:00Z automation run, the main loop closed the
remaining heme-peroxidase deep-packet timeout blocker without opening a new
external mini-campaign. The new subchunk screen
`artifacts/v3_heme_peroxidase_deep_packet_i2dby1_full_current_subchunk_screen_20260521.json`
reruns only the unresolved `I2DBY1` row against all 672 staged current-countable
structures in 14 Foldseek target chunks. All 14 chunks complete, all 672/672
query-target pairs map, the maximum current-countable TM score is `0.5890`,
and 0 hits reach the `TM >= 0.7` duplicate/leakage threshold. This establishes
full-current duplicate clearance for `I2DBY1` only; it does not revise the six
prior high-TM duplicate rejections.

The follow-up terminal packet
`artifacts/v3_heme_peroxidase_deep_terminal_decision_packet_after_i2dby1_subchunk_screen_20260521.json`
therefore updates the frozen heme packet to one
`mechanism_match_review_ready` row (`I2DBY1`) plus six
`terminal_rejection_duplicate_or_leakage` rows. The benchmark
`artifacts/v3_heme_peroxidase_deep_packet_post_i2dby1_subchunk_modern_baseline_benchmark_20260521.json`
keeps EC/keyword and deterministic sequence baselines diagnostic only, records
ESM as unavailable for this packet, and makes no geometry-superiority claim.
No label import, registry edit, fingerprint edit, threshold change, artifact
upload/removal, externalization, Git-LFS migration, or `removal_allowed=true`
occurred.

The same run also advanced the frozen serine-hydrolase blocker without broad
row breadth. The targeted current-fingerprint rescue screen
`artifacts/v3_serine_hydrolase_deep_packet_targeted_current_ser_his_rescue_screen_20260521.json`
screens the six materialized serine rows against the 40 current-countable
`ser_his_acid_hydrolase` structures. All six rows have high-TM
current-countable duplicate/leakage hits, so
`artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_targeted_ser_his_rescue_screen_20260521.json`
converts those six rows to `terminal_rejection_duplicate_or_leakage`. The only
remaining serine `needs_new_extractor_or_structure` row is `P31614`, whose
coordinate sidecar failed to materialize before Foldseek screening. The
companion benchmark
`artifacts/v3_serine_hydrolase_deep_packet_post_targeted_ser_his_rescue_modern_baseline_benchmark_20260521.json`
keeps the targeted rescue as duplicate/leakage rejection evidence only and
continues to make no mechanism-match, duplicate-clear, import, or superiority
claim.
`artifacts/v3_serine_hydrolase_p31614_pdb_replacement_coordinate_screen_20260521.json`
then materializes both frozen PDB cross-references (`4C7L`, `4C7W`) for
`P31614` and runs the same targeted current-serine screen. Both PDB coordinates
complete with 0 high-TM hits, max TM `0.5371`, and no duplicate-clear claim.
The final serine follow-up packet
`artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_pdb_replacement_screen_20260521.json`
therefore keeps `P31614` as the single blocker with an exact missing-evidence
statement: map UniProt active-site residues onto a PDB replacement coordinate
and complete full-current duplicate/leakage screening, or replace `P31614` in a
newly frozen selection.

The run also started the next frozen flavin/heme ladder item without broad
candidate sourcing. `artifacts/v3_flavin_monooxygenase_deep_packet_selection_20260521.json`
freezes seven non-exact-reference rows from the already frozen flavin
monooxygenase mini-campaign before deep geometry/Foldseek scoring, and
`artifacts/v3_flavin_monooxygenase_deep_packet_coordinate_materialization_20260521.json`
materializes all seven AlphaFold sidecars with 0 fetch failures. The targeted
current-fingerprint rescue screen
`artifacts/v3_flavin_monooxygenase_deep_packet_targeted_current_fmo_rescue_screen_20260521.json`
checks only the two current-countable `flavin_monooxygenase` structures and
finds three high-TM duplicate/leakage hits. The terminal packet
`artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_targeted_fmo_rescue_screen_20260521.json`
sets those three rows to `terminal_rejection_duplicate_or_leakage` and leaves
four rows at `needs_new_extractor_or_structure` with the exact blocker:
source-free flavin/cofactor geometry mapping plus full current-countable
duplicate/leakage screening. The benchmark
`artifacts/v3_flavin_monooxygenase_deep_packet_targeted_fmo_modern_baseline_benchmark_20260521.json`
records EC/keyword, deterministic sequence, geometry-not-run, Foldseek, and ESM
caveats with no import or superiority claim.
`artifacts/v3_flavin_monooxygenase_deep_packet_structure_mapping_20260521.json`
then maps flavin/cofactor binding residues onto all seven AlphaFold coordinate
sidecars with status `ok` for every row. The follow-up terminal packet
`artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_structure_mapping_20260521.json`
keeps the same terminal counts but narrows the four non-hit blockers to:
run source-free FMO geometry scoring from mapped flavin/cofactor features and
complete full current-countable duplicate/leakage screening. The benchmark
`artifacts/v3_flavin_monooxygenase_deep_packet_post_structure_mapping_modern_baseline_benchmark_20260521.json`
records mapped-candidate count 7, geometry-scored count 0, ESM unavailable, and
no superiority or import claim.

Evidence-based confidence call: confidence is high that `I2DBY1` now has a
source-separated, reproducible terminal decision packet with active-site/heme
geometry evidence and complete current-countable duplicate/leakage screening.
Confidence is high that this is review-ready only, not import-ready: the row
still requires human/scientific review before any future countable label path,
and the benchmark explicitly permits no superiority claim. Confidence is high
that the six materialized serine rows are terminal duplicate/leakage
rejections; confidence is medium on the remaining serine blocker because it is
now specifically a PDB active-site mapping plus full-current duplicate-screen
problem for `P31614`, not an AlphaFold fetch or targeted-serine Foldseek
problem. Confidence is medium-high that the FMO coordinate-mapping blocker is
closed for all seven selected rows, with the remaining exact blocker shifted to
geometry scoring plus full-current duplicate/leakage screening for the four
non-hit rows. Next main-loop work should run that bounded FMO geometry/full
current-screen step, or if staying on serine, implement a bounded PDB
active-site mapping probe for `P31614`; do not open new broad external row
breadth.

As of the 2026-05-21T13:56:00Z automation run, the main loop integrated fresh
remote ePK research-lane pushes only as decision-changing review context, then
returned to non-ePK deepening. The new concise synthesis
`artifacts/v3_epk_remote_lane_followup_synthesis_20260521.json` keeps ePK
review-only/no-go: positive-evidence surfaces are exhausted with 0 fresh
candidate rows, the false-positive lane preserves `5UJ7:biological_assembly_1`
and extends the regression gate to 318 rows with 0 unsafe non-abstentions, the
policy harness creates a federated adapter scoreboard gate with 0 forbidden
source leakage, and substrate-role identity still has mixed source-free
signature collisions including `9UUR`/`9UUX` versus `9UW4`. No ePK scorer,
threshold, registry edit, label import, fingerprint expansion, artifact
upload/removal, or main-loop ePK task is authorized.

The same run deepened the already frozen heme-peroxidase campaign. The heme
selection artifact
`artifacts/v3_heme_peroxidase_deep_packet_selection_20260521.json` freezes
seven non-exact-reference rows before geometry/Foldseek scoring. All seven
AlphaFold sidecars materialize, all seven active/heme-binding feature sets map
to structure, and
`artifacts/v3_heme_peroxidase_deep_packet_geometry_scores_20260521.json`
top-ranks all seven to `heme_peroxidase_oxidase` above the `0.4115` floor with
0 text/name/label fields used. The all-current Foldseek duplicate screen is
mixed: two rows complete with high-TM current-countable hits, one timed-out row
retains a partial high-TM hit, and a targeted current-heme rescue screen adds
three more high-TM current-countable heme hits without making any duplicate-clear
claim. The terminal packet
`artifacts/v3_heme_peroxidase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
therefore records six `terminal_rejection_duplicate_or_leakage` rows and one
`needs_new_extractor_or_structure` row (`I2DBY1`, exact blocker: complete the
full current-countable structural duplicate/leakage screen). The benchmark
`artifacts/v3_heme_peroxidase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json`
keeps EC/keyword and deterministic sequence baselines diagnostic only, records
ESM as unavailable, and makes no superiority claim.

Evidence-based confidence call: confidence is high that the heme packet is a
source-separated deep decision packet with active-site/heme geometry evidence
and reproducible duplicate/leakage evidence for six terminal rejections.
Confidence is medium on the remaining `I2DBY1` blocker because the targeted
current-heme subset completed without a high-TM hit, but the full
current-countable screen still timed out; no duplicate-clear, mechanism-match,
import, or superiority claim is permitted for that row. Next main-loop work
should either finish that single heme timeout blocker with smaller full-current
target subchunks, or move to another already frozen flavin/heme packet; do not
open new broad external mini-campaign breadth.

As of the 2026-05-21T12:24:00Z automation run, the main loop returned to
non-ePK external decision deepening after a concise fresh-lane ePK synthesis.
`artifacts/v3_epk_fresh_lane_followup_synthesis_20260521.json` integrates the
new positive-evidence, false-positive, sibling-control, policy-harness, and
substrate-role lane state without copying production changes. The synthesis
keeps ePK review-only/no-go: the positive lane adjudicates all 84 candidate
backfill rows with 39 source-supported review-only rows but no upgraded
folded-protein local-metal active-gamma positive; false-positive evidence pins
`5UJ7:biological_assembly_1` as the context-v4-only assembly residual while
expected policy blockers keep unsafe non-abstentions at 0; sibling controls
pin a 119-row future scorer-test contract with 13/13 assertions passing; the
policy bridge gate covers 31 rows with 0 forbidden source leakage and 0 unsafe
control non-abstentions. No ePK scorer, threshold, registry edit, label import,
fingerprint expansion, artifact upload/removal, or main-loop ePK task is
authorized.

The same run then completed the already frozen flavin dehydrogenase/reductase
deep-packet duplicate screen. The new screen artifact
`artifacts/v3_flavin_dehydrogenase_deep_packet_chunked_current_countable_structural_screen_20260521.json`
runs the seven selected flavin rows one query at a time against the 672
current-countable staged structures. Foldseek completed 7/7 query runs, mapped
4,704/4,704 unique query-target structure pairs with 0 raw-name mapping
failures, and found `TM >= 0.7` current-countable duplicate/leakage signals for
all seven rows. The strongest signal is `P42898` against current structure
`1ZP3` at max pair TM `0.9448`.

`artifacts/v3_flavin_dehydrogenase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
therefore converts all seven flavin rows from
`needs_new_extractor_or_structure` to
`terminal_rejection_duplicate_or_leakage`. The post-duplicate benchmark
`artifacts/v3_flavin_dehydrogenase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json`
keeps EC/keyword and deterministic sequence baselines diagnostic only, records
ESM as unavailable, and makes no superiority claim. Evidence-based confidence
call: confidence is high that flavin dehydrogenase now has a reproducible,
source-separated terminal duplicate/leakage packet; confidence is high that no
row from this packet should move toward mechanism-match review or import,
because all seven are current-countable structural leakage signals. The next
main-loop step should either subchunk the serine current-countable target set
to remove the timeout blocker, or continue to another already frozen
flavin/heme packet; do not open new broad mini-campaign breadth.

As of the 2026-05-21T04:47:00Z automation run, the main loop closed the
active metal-phosphatase deep-packet blocker without opening a new external
mini-campaign. The new chunked screen artifact
`artifacts/v3_metal_phosphatase_deep_packet_chunked_current_countable_structural_screen_20260521.json`
reruns the seven already frozen metal-phosphatase deep rows one query at a
time against the 672 current-countable staged structures. Foldseek completed
7/7 query runs, mapped 4,704/4,704 unique query-target structure pairs, had 0
raw-name mapping failures, and found high-TM current-countable structural
duplicate/leakage signals for all seven rows at `TM >= 0.7`.

The follow-up terminal packet
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
therefore converts all seven selected rows from
`needs_new_extractor_or_structure` to the allowed terminal decision
`terminal_rejection_duplicate_or_leakage`. This is a terminal review-only
decision, not a label import or mechanism-match claim: all rows remain
non-countable, import-ready count is 0, no registry/fingerprint artifact was
edited, and Foldseek/TM evidence is explicitly import-gate duplicate/leakage
evidence rather than predictive mechanism evidence. The compact benchmark
`artifacts/v3_metal_phosphatase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json`
keeps EC/keyword and deterministic 5-mer baselines diagnostic only, records
ESM as unavailable for this packet, and makes no superiority claim.

Evidence-based confidence call: confidence is high that the metal phosphatase
deep packet now satisfies the primary one-month visible milestone for a
terminal, reproducible, source-separated external decision with active-site
evidence and duplicate/leakage screening. Confidence is also high that no
metal-phosphatase row should move toward import or mechanism-match review from
this packet, because every row has a current-countable high-TM leakage signal.
The same run attempted the next ladder step for the already frozen serine
selection in
`artifacts/v3_serine_hydrolase_deep_packet_chunked_current_countable_structural_screen_20260521.json`.
That produced a precise blocker rather than a terminal upgrade: the six
materialized serine rows each hit the bounded 120-second Foldseek query
timeout, and `P31614` remains coordinate-missing. The follow-up packet
`artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
therefore keeps all seven rows at `needs_new_extractor_or_structure`. The next
main-loop work should either split serine targets into smaller current-countable
subchunks or move to the already materialized flavin duplicate screen before
any duplicate-clear, mechanism-match, import, or superiority claim is
considered.

As of the 2026-05-21T03:45:00Z automation run, the main loop has produced a
second source-separated external deep packet, this time for the frozen serine
hydrolase mini-campaign. The post-metal ePK lane synthesis
`artifacts/v3_epk_post_metal_research_lane_synthesis_20260521.json` integrates
five sibling research-lane outputs, including the `5UJ7` biological-assembly
residual counterexample, and keeps ePK review-only/no-go with 401 JSON files
and 167 JSONL records validated at 0 parse errors. It authorizes no scorer,
threshold, registry edit, label import, fingerprint expansion, artifact upload,
or main-loop ePK task; the main-loop decision is explicitly to return to the
external decision-deepening ladder.

The serine packet starts from the already frozen
`v3_prospective_external_serine_hydrolase_minicampaign_*_20260521` surface and
selects seven PDB-linked rows before scoring: `P54317`, `Q9BV23`, `P07098`,
`Q99685`, `P04180`, `P31614`, and `E9LVH9`, while excluding exact current
reference duplicate `P94388`. Six AlphaFold coordinate sidecars are
materialized; `P31614` is blocked at coordinate materialization. Six selected
rows map Ser/Asp/His active-site residue sets and score against all eight
current fingerprints with 0 text/name/label fields. Six top-rank the target
`ser_his_acid_hydrolase` lane, one top-ranks `metal_dependent_hydrolase`, and
all target-lane scores remain below the `0.4115` in-scope floor. The duplicate
screen is deliberately not claimed complete: the exact current-countable
structural probe is a blocker artifact with pair-cache completeness false,
screened-candidate count 0, and no duplicate-clear claim.

Evidence-based confidence call: confidence is high that ePK remains out of
main-loop production scope, and high that the serine packet is a real
source-separated small win rather than another broad row list. It is also
blocked from import or mechanism-match review readiness: all seven rows use
the allowed terminal decision `needs_new_extractor_or_structure`. The next
exact experiment is a resumable/chunked current-countable structural
duplicate/leakage screen for the six materialized serine rows plus a PDB or
replacement-coordinate path for `P31614`; no superiority, duplicate-clear,
mechanism-match, or label-import claim is permitted before that evidence.
The next ladder step also has a terminal blocker packet:
`artifacts/v3_flavin_dehydrogenase_deep_packet_selection_20260521.json` freezes
seven nonduplicate flavin dehydrogenase/reductase rows from the existing
20-row campaign. It excludes exact current-reference duplicates `P15559`,
`P0AEZ1`, `P38489`, and `P42593`, uses PDB/catalytic/active-or-binding-site/
flavin context only for selection, and its coordinate materialization companion
stages all seven AlphaFold sidecars. The follow-on structure-mapping artifact
resolves active/cofactor-site coordinates for all seven rows as review-only
mapping evidence. The all-8 geometry score artifact top-ranks six rows to
`flavin_dehydrogenase_reductase`, with four target-lane scores above the
`0.4115` floor, but the terminal packet still uses
`needs_new_extractor_or_structure` for all seven rows because pair-cache
complete current-countable duplicate evidence is absent. The benchmark records
EC/keyword, deterministic 5-mer, geometry, Foldseek, and ESM caveats with no
superiority or import claim.

As of the 2026-05-21T01:18:23Z automation run,
`artifacts/v3_epk_post_overnight_remote_lane_synthesis_20260521.json`
integrates fresh remote ePK research-branch pushes since the overnight
synthesis. It validates 9 JSON artifacts and 3 JSONL ledgers with 0 parse
errors, without copying production changes from the research branches. The
positive-evidence lane adds current-release/source-text negative evidence:
the current-day release surface returned 0 rows, the 2026 canonical backfill
keeps `23FC` as short-segment/PIKK review-only stress, BRAF/MEK alias rows
`6U2G` and `9AXX` are source-relevant but geometry-negative, and Europe PMC
plus targeted-article alias scans found no clean folded-protein transfer-state
positive. The substrate-role lane converts the source-free substrate identity
problem into an explicit review requirement: the conservative gate has 14 true
positives, 34 true negatives, 0 false positives, and 6 false negatives, but it
clears that only by abstaining on product/ADP, reciprocal folded-chain, and
same-chain/autophosphorylation-like contexts. The policy-harness push
materializes the ADP/product-state candidate-repair tripwire already reflected
by the overnight dirty-worktree synthesis; all 10 rows remain review-only
abstentions with 0 expected-decision mismatches.

Evidence-based confidence call: confidence is high that ePK remains
review-only and not production-ready. Fresh remote evidence strengthens the
no-go decision rather than reopening production work: no scorer, threshold,
registry edit, label import, fingerprint expansion, or main-loop ePK task is
authorized. The main loop should continue external mini-campaigns, modern
baseline comparisons, terminal decisions, or non-ePK family packets.

Later dirty sibling-worktree ePK outputs are summarized in
`artifacts/v3_epk_dirty_sibling_followup_synthesis_20260521.json` without
copying production changes. It validates 91 positive-lane JSON files, 48
false-positive JSON files, 53 sibling-control JSON files, 135 policy-harness
JSON files, and 44 total JSONL records with 0 parse errors. The positive lane
keeps `23FC` review-only because publication authority is still absent and the
related ATR-ATRIP article family has no named Chk1/substrate polymer entity.
The false-positive lane finds `5UJ7` biological assembly 1 as an assembly-v4
sufficiency counterexample. Sibling controls show 76/76 weak gamma/product
cases unblock when source-free blockers are disabled, and policy harness keeps
25/25 fresh ADP/product query-context rows as review-only abstentions with 0
mismatches. This reinforces the no-go production decision; any next ePK work is
research-lane-only fixture/guard design, not a main-loop task.

The same run then freezes a fourth 2026-05-21 prospective external
mini-campaign, this time for the current `ser_his_acid_hydrolase` lane. The
freeze artifact
`artifacts/v3_prospective_external_serine_hydrolase_minicampaign_freeze_20260521.json`
locks 19 reviewed UniProtKB/Swiss-Prot EC 3.1.1.* rows before scoring,
requiring catalytic activity, PDB cross-reference, sequence, active-site
annotation, and source evidence for a serine-hydrolase-like nucleophile plus
charge-relay/triad context. Prior external-pool accessions, imported hard
negatives, nuclease/metallo contexts, phospholipase D, and secretory
phospholipase A2 contexts are excluded; selection uses a two-row cap per
primary EC and does not use sequence-neighbor, Foldseek, ESM, geometry, score,
or ePK evidence. The decision packet
`artifacts/v3_prospective_external_serine_hydrolase_minicampaign_decision_packet_20260521.json`
keeps 18 rows as `needs_review` under the existing serine-hydrolase lane and
terminally rejects `P94388` as an exact current-reference sequence duplicate.
The baseline comparison
`artifacts/v3_serine_hydrolase_minicampaign_baseline_comparison_20260521.json`
records EC/keyword routing and deterministic 5-mer duplicate context only; no
geometry, ESM, Foldseek, superiority, mechanism-match, production-score,
threshold, import, registry, or fingerprint claim is opened.
`artifacts/v3_external_minicampaign_modern_baseline_rollup_post_serine_hydrolase_20260521.json`
now covers 78 frozen rows across the PLP, flavin, heme, and serine-hydrolase
mini-campaigns, with 70 `needs_review`, 8 exact current-reference duplicate
terminal rejections, 9 deterministic sequence-neighbor alerts, and 0
geometry-scored external rows. The current register is
`artifacts/v3_main_loop_small_win_register_post_serine_hydrolase_20260521.json`.

The run then adds a fifth prospective external mini-campaign for the current
`metal_dependent_hydrolase` lane. The freeze artifact
`artifacts/v3_prospective_external_metal_phosphatase_minicampaign_freeze_20260521.json`
locks 17 reviewed UniProtKB/Swiss-Prot EC 3.1.3.* phosphatase rows before
scoring, requiring catalytic activity, PDB cross-reference, sequence,
active-site annotation, metal-binding annotation, and phosphatase/
metallophosphoesterase source context. Prior external-pool accessions,
imported hard negatives, and transferase/kinase-like contexts are excluded;
selection again uses a two-row cap per primary EC and no sequence-neighbor,
Foldseek, ESM, geometry, score, or ePK evidence. The decision packet
`artifacts/v3_prospective_external_metal_phosphatase_minicampaign_decision_packet_20260521.json`
keeps all 17 rows as `needs_review` under the existing metal hydrolase lane:
no exact current-reference duplicates, no geometry scoring, and 0 import-ready
rows. The no-claim baseline
`artifacts/v3_metal_phosphatase_minicampaign_baseline_comparison_20260521.json`
keeps EC/keyword and deterministic 5-mer context diagnostic only. The post-
metal rollup
`artifacts/v3_external_minicampaign_modern_baseline_rollup_post_metal_phosphatase_20260521.json`
now covers 95 frozen rows across five 2026-05-21 external mini-campaigns: 87
`needs_review`, 8 exact current-reference duplicate terminal rejections, 9
sequence-neighbor alerts, and 0 geometry-scored external rows. The current
register is
`artifacts/v3_main_loop_small_win_register_post_metal_phosphatase_20260521.json`.

The same run also opens a sixth current-fingerprint external surface for
`flavin_dehydrogenase_reductase`. The freeze artifact
`artifacts/v3_prospective_external_flavin_dehydrogenase_minicampaign_freeze_20260521.json`
locks 20 reviewed UniProtKB/Swiss-Prot oxidoreductase rows from EC 1.5.1.*,
1.6.5.*, or 1.3.1.* before scoring, requiring catalytic activity, PDB
cross-reference, sequence, active-site or binding-site annotation, explicit
FAD/FMN/flavin context, and dehydrogenase/reductase source context. Prior
external-pool accessions, imported hard negatives, and oxygenase/peroxidase/
P450 mixed contexts are excluded. The decision packet
`artifacts/v3_prospective_external_flavin_dehydrogenase_minicampaign_decision_packet_20260521.json`
keeps 16 rows as `needs_review` under the existing flavin redox lane and
terminally rejects four exact current-reference sequence duplicates (`P15559`,
`P0AEZ1`, `P38489`, and `P42593`). The baseline comparison
`artifacts/v3_flavin_dehydrogenase_minicampaign_baseline_comparison_20260521.json`
again records only EC/keyword and deterministic 5-mer context. The post-flavin
dehydrogenase rollup
`artifacts/v3_external_minicampaign_modern_baseline_rollup_post_flavin_dehydrogenase_20260521.json`
now covers 115 frozen rows across six 2026-05-21 external mini-campaigns: 103
`needs_review`, 12 exact current-reference duplicate terminal rejections, 13
sequence-neighbor alerts, and 0 geometry-scored external rows. The current
register is
`artifacts/v3_main_loop_small_win_register_post_flavin_dehydrogenase_20260521.json`.

The cobalamin radical lane was checked next but not forced into an underpowered
campaign. `artifacts/v3_prospective_external_cobalamin_radical_minicampaign_blocker_review_20260521.json`
records the terminal blocker: the reviewed adenosylcobalamin/PDB source query
has only one new row that survives source-context, prior-pool, and cap filters,
below the preregistered 10-row mini-campaign floor. The campaign is therefore
closed before scoring as
`terminal_rejection_insufficient_new_source_surface_for_campaign`, with no
sequence baseline, geometry scoring, terminal-review import gate, registry
edit, label import, or fingerprint change.

The next source-complete current-fingerprint surface is radical SAM.
`artifacts/v3_prospective_external_radical_sam_minicampaign_freeze_20260521.json`
freezes 20 reviewed UniProtKB/Swiss-Prot radical-SAM/PDB rows before scoring,
requiring catalytic activity, sequence, active-site or binding-site annotation,
PDB cross-reference, and radical-SAM or SAM/Fe-S source context. The freeze
excludes imported hard negatives, prior external-pool accessions, and
cobalamin/coenzyme-B12/adenosylcobalamin overlap contexts, uses a two-row cap
per primary EC, and does not use sequence-neighbor, Foldseek, ESM, geometry,
score, or ePK evidence for selection. The decision packet
`artifacts/v3_prospective_external_radical_sam_minicampaign_decision_packet_20260521.json`
keeps all 20 rows as `needs_review` under the current `radical_sam_enzyme`
lane: deterministic 5-mer screening finds 0 exact current-reference matches
and 0 near-neighbor alerts, but source-free external geometry, terminal-review,
and factory/import gates are still absent. The baseline comparison
`artifacts/v3_radical_sam_minicampaign_baseline_comparison_20260521.json`
therefore makes no superiority or mechanism-match claim. The post-radical-SAM
rollup
`artifacts/v3_external_minicampaign_modern_baseline_rollup_post_radical_sam_20260521.json`
now covers 135 frozen rows across seven 2026-05-21 external mini-campaigns:
123 `needs_review`, 12 exact current-reference duplicate terminal rejections,
13 sequence-neighbor alerts, and 0 geometry-scored external rows. The current
register is
`artifacts/v3_main_loop_small_win_register_post_radical_sam_20260521.json`.
No registry edit, label import, production score, threshold, fingerprint
expansion, artifact upload/removal, Git-LFS tracking, history rewrite, or
`removal_allowed=true` occurred.

The all-current-fingerprint benchmark ledger is
`artifacts/v3_current_fingerprint_external_minicampaign_baseline_benchmark_20260521.json`.
It treats the seven scored mini-campaigns plus the cobalamin source-surface
blocker as one review-only modern-baseline comparison. Coverage is now explicit
for all eight production fingerprints: seven lanes have a 10-30 row frozen
external mini-campaign and `cobalamin_radical_rearrangement` has a terminal
insufficient-source-surface blocker. The ledger contains 135 frozen rows, 123
`needs_review` decisions, 12 duplicate terminal rejections, 13 terminal
rejections including the cobalamin blocker, 12 exact current-reference sequence
matches, 13 sequence-neighbor alerts, and 0 geometry-scored external rows. The
EC/keyword, deterministic 5-mer, geometry/retrieval, ESM, and Foldseek sections
all remain diagnostic and no-claim: there are 0 import-ready rows, 0 countable
label candidates, 0 source-free external geometry scores, no superiority
claim, and no production authorization.

The exact next experiment is preregistered but not run in
`artifacts/v3_external_minicampaign_source_free_geometry_preregistration_20260521.json`.
It freezes 14 rows, exactly two `needs_review` rows from each source-complete
mini-campaign, excluding exact current-reference duplicates and deterministic
5-mer near-neighbor alerts. Cobalamin is deliberately excluded until its
source-surface blocker is cleared. The only authorized later bounded operation
is to materialize structure sidecars for those exact accessions, run
current-countable duplicate screens, and only then consider the existing all-8
inverse gate and terminal review. The preregistration itself runs no geometry,
Foldseek, inverse gate, terminal-review import gate, threshold tuning, registry
edit, label import, fingerprint expansion, artifact upload/removal, or ePK
production scoring.

As of the 2026-05-21T02:14:38Z automation run, the main loop started the
metal-phosphatase decision-deepening ladder rather than opening more broad
external rows. `artifacts/v3_metal_phosphatase_deep_packet_selection_20260521.json`
freezes seven rows from the existing 17-row metal-phosphatase mini-campaign
before geometry/Foldseek outcome scoring. The selected rows all have PDB cross
references, active-site and metal-binding source annotations, no exact
current-reference sequence duplicate, and diverse EC 3.1.3.* coverage.
`artifacts/v3_metal_phosphatase_deep_packet_coordinate_materialization_20260521.json`
materializes/reuses seven AlphaFold sidecars, and
`artifacts/v3_metal_phosphatase_deep_packet_structure_mapping_20260521.json`
maps all seven active-site residue sets. The current geometry artifact
`artifacts/v3_metal_phosphatase_deep_packet_geometry_scores_20260521.json`
scores all seven rows against the eight current fingerprints with 0
text/name/label fields used; six rows top1 to `metal_dependent_hydrolase`, one
top1s to `ser_his_acid_hydrolase`, and no target-lane score reaches the
`0.4115` review floor. The attempted exact current-countable Foldseek screen
is captured as a blocker in
`artifacts/v3_metal_phosphatase_deep_packet_current_countable_structural_screen_20260521.json`
and
`artifacts/v3_metal_phosphatase_deep_packet_foldseek_runtime_blocker_20260521.json`:
the 7 x 672 exact screen did not complete with pair-cache evidence, so the
terminal packet
`artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_20260521.json`
sets all seven rows to `needs_new_extractor_or_structure` with the exact
missing evidence named as a completed current-countable structural duplicate
screen. The benchmark
`artifacts/v3_metal_phosphatase_deep_packet_modern_baseline_benchmark_20260521.json`
compares the same frozen rows against EC/keyword routing, deterministic 5-mer,
geometry, Foldseek availability, and ESM availability, and makes no superiority
or import claim.

Evidence-based confidence call: confidence is high that the metal-phosphatase
packet is now a reproducible source-separated blocker rather than another
`needs_review` row list, because candidate selection, coordinate materialization,
geometry scoring, source/context separation, and the missing duplicate-screen
gate are all committed and tested. Confidence is low that any selected row is
ready for mechanism-match or hard-negative import: current geometry remains
below the review floor and the current-countable structural duplicate screen is
the exact unresolved gate. The next main-loop step should be a resumable or
targeted current-countable structural screen for these seven rows before moving
to serine hydrolase.

The normalized terminal-decision ledger is
`artifacts/v3_external_minicampaign_terminal_decision_index_20260521.json`.
It carries 136 review-only decision rows across the seven scored
mini-campaigns plus the cobalamin blocker, normalized to the allowed terminal
decision vocabulary. Counts are 123 `needs_review` and 13
`terminal_rejection`; every row has `ready_for_label_import=false` and
`countable_label_candidate=false`. This is a handoff/regression input only, not
a production benchmark, import request, or scoring authorization.

Wrap validation for the 2026-05-21 small-win main loop passed after minute 48:
774 unit tests, `PYTHONPATH=src python -m catalytic_earth.cli validate`, the
artifact-migration dry-run guard with `removal_allowed=0`, `compileall`, 53
same-day JSON parses, and `git diff --check` all passed. `HEAD` was pushed to
`origin/main` after the radical-SAM, current-fingerprint benchmark,
source-free geometry preregistration, terminal-decision index, and dirty ePK
sibling synthesis commits.

As of the 2026-05-21T00:17:08Z automation run,
`artifacts/v3_epk_overnight_research_lane_synthesis_20260521.json` integrates
the fresh dirty sibling-worktree ePK outputs created after the post-late
synthesis. It validates 11 JSON artifacts, 4 JSONL ledgers, and 4 lane
handoffs with 0 parse errors. The new positive lane evidence adds only
review-only short-segment/peptide stress: `23FC` is an ATR/PIKK Chk1 segment
lead rather than clean canonical folded-protein ePK substrate evidence, while
`1L3R` and `5LIH` remain peptide/pseudosubstrate positives. The false-positive
lane adds bounded high-order v4 overblock stress with 0 lost known positives,
0 non-ORC residual counterexamples, and a fetch-error retry that adds no new
residuals. Sibling controls add a 91-case expected-block oracle with 76 weak
gamma/product proximity cases blocked and 0 expected unblocked weak cases. The
policy harness adds an ADP/product-state/candidate-repair tripwire: 10/10 rows
remain review-only abstentions with 0 expected-decision mismatches.

Evidence-based confidence call: confidence remains high that ePK is still
review-only and not production-ready. The fresh lane outputs improve future
research-lane test fixtures, but they do not justify a scorer, threshold,
registry edit, label import, fingerprint expansion, or main-loop resumption.
The only exact future ePK experiment named by main is isolated research-lane
work:
`epk_source_free_scorer_dry_run_against_oracle_and_tripwires_v1_review_only`.
Do not start that from the main loop.

The same run opens a fresh prospective external PLP aminotransferase
mini-campaign after the ePK integration commit. The freeze artifact
`artifacts/v3_prospective_external_plp_aminotransferase_minicampaign_freeze_20260521.json`
locks 20 reviewed UniProtKB/Swiss-Prot EC 2.6.1.* rows before scoring,
requiring catalytic activity, PDB cross-reference, explicit pyridoxal
5'-phosphate binding/active-site annotation, prior external-pool exclusions,
mixed-EC exclusions, and a two-row cap per primary EC. The decision packet
`artifacts/v3_prospective_external_plp_aminotransferase_minicampaign_decision_packet_20260521.json`
keeps 18 rows as `needs_review` because they route to the current
`plp_dependent_enzyme` fingerprint lane but lack source-free external geometry,
duplicate, terminal-review, and factory/import gates; `P12995` and `P19938`
are terminal rejections as exact current-reference sequence duplicates. The
baseline comparison
`artifacts/v3_plp_aminotransferase_minicampaign_baseline_comparison_20260521.json`
records EC/keyword, deterministic 5-mer, and unrun ESM/Foldseek/geometry
context without a superiority claim. No registry edit, label import,
threshold, production scoring, fingerprint expansion, artifact migration,
upload, removal, Git LFS tracking, or history rewrite was performed.

The run then closes the final non-ePK ATP-family packet slot as terminal
review-only evidence. The preregistration
`artifacts/v3_pfka_vs_neighbor_family_control_tranche_preregistration_20260521.json`
freezes 15 rows before axis decisions: one rejected PfkA boundary row, two
current metal-hydrolase controls, seven neighboring ATP-family controls, and
five PfkA homolog hydroxyl-axis countercontrols. The decision packet
`artifacts/v3_pfka_vs_neighbor_family_control_tranche_axis_decisions_20260521.json`
records one `terminal_rejection`, two hydrolase `mechanism_match` controls,
and 12 `out_of_scope` neighbor/homolog countercontrols, with 0 source-free
PfkA-axis-ready rows and 0 import-ready candidates. The no-claim baseline
`artifacts/v3_pfka_vs_neighbor_family_control_tranche_baseline_comparison_20260521.json`
keeps the three over-floor current-geometry hits diagnostic only and preserves
the homolog hydroxyl distances of 3.221-6.152 Angstrom as counterdiagnostic
context. `artifacts/v3_atp_family_readiness_index_post_pfka_tranche_20260521.json`
now marks all non-ePK ATP-family readiness slots closed review-only no-go; ePK
remains research-lane-only. The current rollup is
`artifacts/v3_main_loop_small_win_register_post_pfka_tranche_20260521.json`.
No registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

The run also freezes a second prospective external mini-campaign, this time
for flavin monooxygenase source rows. The freeze artifact
`artifacts/v3_prospective_external_flavin_monooxygenase_minicampaign_freeze_20260521.json`
locks 20 reviewed UniProtKB/Swiss-Prot EC 1.14.13.* rows before scoring,
requiring catalytic activity, PDB cross-reference, explicit FAD/FMN/flavin
source context, prior-pool exclusions, heme/P450 mixed-context exclusions, and
a two-row cap per primary EC. The decision packet
`artifacts/v3_prospective_external_flavin_monooxygenase_minicampaign_decision_packet_20260521.json`
keeps 19 rows as `needs_review` under the existing `flavin_monooxygenase`
fingerprint lane because external source-free geometry, duplicate-screen
completion, terminal review, and factory/import gates are incomplete; `P15245`
is a terminal rejection as an exact current-reference sequence duplicate. The
baseline comparison
`artifacts/v3_flavin_monooxygenase_minicampaign_baseline_comparison_20260521.json`
records EC/keyword routing, deterministic 5-mer duplicate/neighbor context,
and unrun geometry/ESM/Foldseek sidecars without a superiority claim. No
registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

The final external mini-campaign opened in this run targets the current
`heme_peroxidase_oxidase` lane. The freeze artifact
`artifacts/v3_prospective_external_heme_peroxidase_minicampaign_freeze_20260521.json`
locks 19 reviewed UniProtKB/Swiss-Prot EC 1.11.1.* peroxidase/catalase rows
before scoring, with catalytic activity, PDB cross-reference, explicit
heme/iron source context, prior-pool exclusions, mixed globin/peroxiredoxin/
dual-oxidase exclusions, and a two-row cap per primary EC. The decision packet
`artifacts/v3_prospective_external_heme_peroxidase_minicampaign_decision_packet_20260521.json`
keeps 15 rows as `needs_review` under the existing heme lane and terminally
rejects four exact current-reference sequence duplicates. The baseline
comparison
`artifacts/v3_heme_peroxidase_minicampaign_baseline_comparison_20260521.json`
keeps EC/keyword and deterministic 5-mer context diagnostic only; no geometry,
ESM, Foldseek, superiority, scoring, threshold, import, registry, or
fingerprint claim is opened.

The current modern-baseline rollup
`artifacts/v3_external_minicampaign_modern_baseline_rollup_20260521.json`
aggregates the PLP and flavin external mini-campaigns as a 40-row review-only
benchmark artifact. It records 37 `needs_review` rows and three exact
current-reference duplicate terminal rejections. EC/keyword routing only
assigns current fingerprint-lane context, deterministic sequence-neighbor
checks only supply duplicate/leakage caveats, and geometry/ESM/Foldseek
sidecars remain unrun for these frozen sets. The rollup permits no superiority,
mechanism-match, production-score, or import claim.
After the heme campaign, the post-heme rollup
`artifacts/v3_external_minicampaign_modern_baseline_rollup_post_heme_20260521.json`
extends the same review-only benchmark to all three 2026-05-21 external
mini-campaigns. Across 59 frozen rows it records 52 `needs_review` rows, seven
exact current-reference duplicate terminal rejections, eight deterministic
sequence-neighbor alerts, and 0 geometry-scored external rows. It still permits
no superiority, mechanism-match, production-score, or import claim.

Evidence-based confidence call after wrap validation: confidence is high that
the current small-win loop produced visible review-only decisions without
mutating science baselines. The registry remains 682 labels, the production
fingerprint universe remains 8 fingerprints, the artifact-migration dry-run
keeps `removal_allowed=0`, and the full unit suite plus CLI validation pass.
The next main-loop work should continue prospective external mini-campaigns or
non-ePK family readiness/terminal-decision packets; no current artifact
authorizes production scoring, threshold calibration, label import, registry
edit, or fingerprint expansion.

As of the 2026-05-20T23:16:33Z automation run,
`artifacts/v3_epk_post_late_dirty_lane_synthesis_20260520.json` integrates
the fresh dirty sibling-worktree ePK outputs that appeared after the late-lane
synthesis window. It validates 20 JSON files plus 3 JSONL ledgers with 0 parse
errors. The added evidence changes review context but not the production
decision: positive-evidence lanes add review-only peptide/near-miss positives
and transition-analog false hits (`7PT7`, `1HE1`), the false-positive lane adds
`9I3I` as a topology-clear ORC/MCM non-ePK counterexample, sibling controls
compact the 91-case counteraxis fixture, and the policy harness keeps 8
non-prefrozen GNP/GTP terminal-gamma rows as fail-closed review-only
abstentions. ePK remains review-only, no-go for production activation, and out
of the main-loop default path.

Evidence-based confidence call: confidence is high that the newest ePK lane
evidence still does not justify a scorer, threshold, registry edit, label
import, or fingerprint expansion. The only exact future ePK query is isolated
research-lane work on `epk_v4_overblock_risk_high_order_assemblies_v1_review_only`;
the main loop should continue visible non-ePK small wins.

The same run closes the previously recommended PfkB next step. The frozen
tranche in
`artifacts/v3_pfkb_vs_neighbor_family_control_tranche_preregistration_20260520.json`
locks 11 rows before scoring: two PfkB/ribokinase boundary rows, two current
metal-hydrolase controls, and seven ATP-family neighbor countercontrols. The
decision packet
`artifacts/v3_pfkb_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`
keeps both PfkB boundary rows as `needs_review`, preserves two hydrolase
`mechanism_match` controls, routes seven neighboring ATP-family rows to
`out_of_scope`, and records 0 source-free PfkB-axis-ready rows. The no-claim
baseline comparison records the same all-metal-hydrolase top1 collapse without
claiming superiority. `artifacts/v3_atp_family_readiness_index_post_pfkb_tranche_20260520.json`
now marks five ATP-family tranches closed review-only no-go, keeps ePK
research-lane-only, and recommends a genuinely new prospective external
mini-campaign next; if external sourcing is blocked, the next ATP-family packet
is GHMP. `artifacts/v3_main_loop_small_win_register_post_pfkb_tranche_20260520.json`
rolls up the run. No registry edit, label import, threshold, production
scoring, fingerprint expansion, artifact migration, upload, removal, Git LFS
tracking, or history rewrite was performed.

The run then opens and closes a genuinely new prospective external
sulfotransferase mini-campaign. The freeze artifact
`artifacts/v3_prospective_external_sulfotransferase_minicampaign_freeze_20260520.json`
locks 16 reviewed UniProtKB/Swiss-Prot EC 2.8.2.* rows before scoring, with
catalytic-activity text, active-site annotation, at least one PDB
cross-reference, prior-pool exclusions, mixed-EC exclusions, and a two-row cap
per primary EC number. The decision packet
`artifacts/v3_prospective_external_sulfotransferase_minicampaign_decision_packet_20260520.json`
closes all 16 as review-only terminal rejections by uncovered mechanism lane:
PAPS/sulfuryl-transfer chemistry is outside the current 8 production
fingerprints and outside covered external hard-negative counterevidence lanes,
so 0 rows were scored or import-gated. The matching no-claim baseline
`artifacts/v3_sulfotransferase_minicampaign_baseline_comparison_20260520.json`
keeps EC/keyword and deterministic 5-mer context diagnostic only; the sequence
diagnostic finds one current-reference 5-mer alert but does not change any
terminal decision. `artifacts/v3_main_loop_small_win_register_post_sulfotransferase_20260520.json`
rolls ePK, PfkB, and sulfotransferase into one current small-win register. No
registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

Finally, `artifacts/v3_ghmp_family_readiness_packet_20260520.json` packages
the next ATP-family readiness packet without production scoring. GHMP has one
expert-supported boundary row (`m_csa:654`), 0 countable positive seeds, 0
source-free-axis-ready rows, hydrolase top1 collapse at 0.3581, and a
selected-ligand-state gap because local CDM context is present but a local
ATP/Mg/reactant-state axis is not. `artifacts/v3_atp_family_readiness_index_post_ghmp_packet_20260520.json`
marks GHMP as packet-only no-go and recommends a frozen GHMP-vs-neighbor
ATP-family tranche only as future review-only work. The current rollup is
`artifacts/v3_main_loop_small_win_register_post_ghmp_packet_20260520.json`.
No registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

That exact GHMP tranche is now frozen and closed as review-only terminal
evidence. `artifacts/v3_ghmp_vs_neighbor_family_control_tranche_preregistration_20260520.json`
locks one GHMP boundary row, two current metal-hydrolase controls, and seven
neighboring ATP-family countercontrols before axis decisions. The decision
packet `artifacts/v3_ghmp_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`
keeps `m_csa:654` as `needs_review`, records two hydrolase `mechanism_match`
controls, routes seven neighboring ATP-family rows to `out_of_scope`, and
finds 0 source-free GHMP-axis-ready rows. The no-claim baseline again records
all-metal-hydrolase top1 collapse with 3 rows over the 0.4115 floor. The
post-tranche ATP-family index now marks ASKHA, ATP-grasp, GHKL, dNK, PfkB, and
GHMP closed review-only no-go; NDK and PfkA still only have future packet
slots. The current rollup is
`artifacts/v3_main_loop_small_win_register_post_ghmp_tranche_20260520.json`.
No registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

The main loop then used the remaining cadence window to package NDK readiness
without scoring. `artifacts/v3_ndk_family_readiness_packet_20260520.json`
records one expert-reviewed rejected NDK boundary row (`m_csa:637`), 0
countable positive seeds, 0 source-free-axis-ready rows, hydrolase top1
collapse at 0.4066, and four review-only homolog histidine-axis controls
(`1WKL`, `3Q86`, `9OAN`, `9PFY`) with gamma-to-mapped-histidine distances of
2.899-3.339 Angstrom. Those homologs remain counteraxis evidence, not import or
production-positive evidence, because hydroxyl-axis confusion and
phosphohistidine specificity are unresolved. `artifacts/v3_atp_family_readiness_index_post_ndk_packet_20260520.json`
marks NDK as `readiness_packet_no_go` and recommends only a frozen
NDK-vs-neighbor ATP-family tranche before any scoring. The current rollup is
`artifacts/v3_main_loop_small_win_register_post_ndk_packet_20260520.json`.
No registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

That NDK tranche is also now frozen and closed. The preregistration
`artifacts/v3_ndk_vs_neighbor_family_control_tranche_preregistration_20260520.json`
locks 14 rows before axis decisions: one NDK boundary row, four NDK homolog
histidine-axis controls, two current metal-hydrolase controls, and seven
neighboring ATP-family countercontrols. The decision packet
`artifacts/v3_ndk_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`
terminally rejects the source NDK boundary row, preserves two hydrolase
`mechanism_match` controls, routes 11 homolog/neighbor rows to `out_of_scope`,
and finds 0 source-free NDK-axis-ready rows. The no-claim baseline records all
10 M-CSA rows still top1 route to `metal_dependent_hydrolase`, 3 rows over the
0.4115 floor, and the four homolog histidine-distance measurements as
counterdiagnostic only. The post-tranche ATP-family index now marks ASKHA,
ATP-grasp, GHKL, dNK, PfkB, GHMP, and NDK closed review-only no-go; PfkA is the
only remaining ATP-family packet slot. The current rollup is
`artifacts/v3_main_loop_small_win_register_post_ndk_tranche_20260520.json`.
No registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

The remaining ATP-family packet slot is now also packaged. `artifacts/v3_pfka_family_readiness_packet_20260520.json`
records one expert-reviewed rejected PfkA boundary row (`m_csa:365`), 0
countable positive seeds, 0 source-free-axis-ready rows, hydrolase top1
collapse at 0.3999, five measured PfkA homolog counteraxis rows with
same-chain hydroxyl distances of 3.221-6.152 Angstrom, and five additional
homolog rows that remain mapping-not-ready. The packet is review-only and does
not reuse ePK sibling-control measurements as production-positive or import
evidence. `artifacts/v3_atp_family_readiness_index_post_pfka_packet_20260520.json`
marks PfkA as `readiness_packet_no_go`, leaves no ATP-family packet slots
unstarted, and recommends only a frozen PfkA-vs-neighbor ATP-family tranche
before any scoring. The current rollup is
`artifacts/v3_main_loop_small_win_register_post_pfka_packet_20260520.json`.
No registry edit, label import, threshold, production scoring, fingerprint
expansion, artifact migration, upload, removal, Git LFS tracking, or history
rewrite was performed.

As of the 2026-05-20T22:17:26Z automation run,
`artifacts/v3_epk_late_research_lane_synthesis_20260520.json` integrates the
fresh late ePK research-lane surface without copying production changes. It
validates 27 JSON artifacts plus 3 JSONL ledgers with 0 parse errors,
including remote canonical ePK ligand scouts, a fresh substrate-role
orientation/asymmetry probe, false-positive hunter dirty outputs, the sibling
counteraxis matrix, and the policy harness result. The production decision is
unchanged and stronger: ePK remains review-only, no-go for production
activation, and out of the main-loop critical path. Canonical ePK ligand
scouting reviewed six 50-row pages but found only review-only peptide positives
and folded-complex geometry negatives; substrate-role orientation descriptors
recover `9UUR`/`9UUX` but still admit `9UW4`; false-positive stress finds
ORC/OCCM/MCM ATPase topology-clear counterexamples; sibling controls provide a
91-case review-only fixture; policy remains fail-closed.

Evidence-based confidence call: confidence is high that fresh ePK evidence
does not justify a production scorer, threshold, label import, registry edit,
or fingerprint expansion. If an isolated research lane continues, the exact
next blocker decision is
`epk_substrate_role_blocker_stop_decision_probe_v1_review_only`: classify the
remaining strict-rule false negatives by unavailable ligand state versus
same-chain/autophosphorylation-like topology, then decide whether ePK
substrate-role identity should stop at source-reviewed adjudication rather than
more feature probing. Main-loop work should return to visible non-ePK small
wins after this integration commit.

The same run adds two non-ePK small wins after committing that ePK synthesis.
`artifacts/v3_glycosyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json`
fills the missing deterministic 5-mer nearest-current-reference diagnostic for
the frozen glycosyltransferase mini-campaign: 20/20 rows were checked against
737 current references, one crude near-neighbor alert was found, and the
terminal uncovered-lane rejection is unchanged. The matching baseline artifact
now records that sequence context without making a superiority or import claim.

`artifacts/v3_ghkl_vs_neighbor_family_control_tranche_preregistration_20260520.json`
then freezes the next ATP-family readiness experiment before axis scoring:
two GHKL boundary rows, two current hydrolase controls, two ATP-grasp controls,
one ASKHA, one GHMP, one NDK, and one PfkB countercontrol. The decision packet
`artifacts/v3_ghkl_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`
closes it as review-only terminal evidence: two hydrolase controls remain
`mechanism_match`, six neighboring ATP-family rows are `out_of_scope`, and the
two GHKL boundary rows are `terminal_rejection` because prior expert review
rejected those current label candidates and no source-free GHKL fold/acceptor
axis is ready. `artifacts/v3_atp_family_readiness_index_post_ghkl_20260520.json`
keeps ASKHA, ATP-grasp, and GHKL closed as no-go tranches and recommends a
future dNK packet only as review-only small-win work.
`artifacts/v3_dnk_family_readiness_packet_20260520.json` then packages that
next ATP-family packet without production scoring: `m_csa:588` thymidine
kinase and `m_csa:615` deoxyguanosine kinase remain non-countable
expert-rejected mismatch lanes with current `metal_dependent_hydrolase` top1
collapse, 0 countable positive seeds, 0 source-free-axis-ready rows, no
calibrated threshold, and no external hard-negative re-audit. The packet
records review-only deoxynucleoside 5-prime-hydroxyl transfer context and the
`m_csa:615` DTP gamma-to-hydroxyl measurement, but this does not create a
scorer or import claim.
`artifacts/v3_atp_family_readiness_index_post_dnk_packet_20260520.json` marks
dNK as `readiness_packet_no_go`; the only bounded next dNK step is a frozen
dNK-vs-neighbor-ATP-family control tranche before any scoring.
`artifacts/v3_dnk_vs_neighbor_family_control_tranche_preregistration_20260520.json`
freezes that tranche in the same run: two dNK boundary rows, two current
hydrolase controls, one NDK, one PfkA, one PfkB, one GHMP, one ASKHA, and one
ATP-grasp countercontrol. The decision packet
`artifacts/v3_dnk_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`
closes it as review-only terminal evidence: two hydrolase controls remain
`mechanism_match`, six neighboring ATP-family rows are `out_of_scope`, and the
two dNK boundary rows are `terminal_rejection` because prior expert review
rejected those current label candidates and no source-free dNK fold/substrate
axis is ready. `artifacts/v3_atp_family_readiness_index_post_dnk_tranche_20260520.json`
now keeps ASKHA, ATP-grasp, GHKL, and dNK closed as review-only no-go tranches
and recommends PfkB only as a future review-only packet.
`artifacts/v3_pfkb_family_readiness_packet_20260520.json` packages that PfkB
packet next: `m_csa:663` ribokinase and `m_csa:670`
hydroxymethylpyrimidine kinase remain non-countable PfkB/ribokinase boundary
rows with hydrolase top1 collapse, close cross-family guardrail blockers, 0
countable positive seeds, and 0 source-free-axis-ready rows.
`artifacts/v3_atp_family_readiness_index_post_pfkb_packet_20260520.json` marks
PfkB as `readiness_packet_no_go`; the only bounded PfkB next step is a frozen
PfkB-vs-neighbor-ATP-family tranche before any scoring.
`artifacts/v3_main_loop_small_win_register_post_atp_readiness_20260520.json`
rolls up the run's post-ePK small wins: glycosyltransferase sequence baseline
diagnostic preserves the terminal uncovered-lane rejection, GHKL and dNK are
closed review-only no-go tranches, PfkB is packet-only no-go, and ePK remains
research-lane-only. No registry edit, label
import, threshold, production scoring, fingerprint expansion, artifact
migration, upload, or removal was performed.

As of the 2026-05-20T21:08:55Z automation run,
`artifacts/v3_epk_counterexample_push_synthesis_20260520.json` integrates the
fresh ePK positive-evidence research-lane push that landed after the prior
main-loop synthesis. Eight new lane JSON artifacts validate with 0 parse
errors. The new result changes review context but not the production decision:
no fresh clean folded-protein ePK positive was found, and `7ZDT` is a fresh
source-mapped counterexample where local ATP/Mg-to-Ser geometry occurs in CydDC
ATP-binding/permease heme transporter chains rather than kinase-substrate
phosphorylation. Repeat `7ZDU`/`7ZE5` CydDC and broader ATPase/chaperone
false-positive families reinforce the same blocker.

Evidence-based confidence call: confidence is high that this fresh lane push
keeps ePK review-only and no-go for main-loop production activation. The exact
future ePK experiment, if a separate research lane continues, is a
domain/EC-filtered canonical ePK ligand search with explicit ATPase/chaperone
exclusions. Main-loop work should continue with the frozen ASKHA tranche or a
new prospective external surface, not ePK scorer activation.

The same run closes the frozen ASKHA control tranche in
`artifacts/v3_askha_vs_atp_family_control_tranche_axis_decisions_20260520.json`
and its no-claim baseline companion
`artifacts/v3_askha_vs_atp_family_control_tranche_baseline_comparison_20260520.json`.
The exact 14 preregistered rows remain review-only: four current hydrolase
controls are `mechanism_match`, six ATP-family countercontrols are
`out_of_scope` for ASKHA, three ASKHA boundary rows are `needs_review`, and
`m_csa:651` is a `terminal_rejection` because the prior expert decision rejected
that current label candidate. The source-free ASKHA axis-ready count is 0.
Current 8-fingerprint retrieval is diagnostic only and still routes 12/14 rows
to `metal_dependent_hydrolase`; no baseline superiority, scorer, threshold,
registry edit, or label import is authorized.

`artifacts/v3_atp_grasp_family_readiness_packet_20260520.json` adds the next
non-ePK family-readiness packet after ASKHA. ATP-grasp has two
expert-supported boundary rows (`m_csa:310` and `m_csa:498`), both
non-countable expert-rejected reaction/substrate mismatch lanes with current
`metal_dependent_hydrolase` top1 collapse. The packet records ATP/Mg,
carboxylate/amide acceptor, ATP-grasp fold, hydrolase, and neighboring
ATP-family counteraxis needs, but has 0 countable positive seeds and 0
source-free-axis-ready rows. The next admissible experiment is a frozen
ATP-grasp-vs-neighbor-ATP-family control tranche; no production fingerprint,
threshold, registry edit, or label import is authorized.

`artifacts/v3_atp_grasp_vs_neighbor_family_control_tranche_preregistration_20260520.json`
freezes that exact ATP-grasp next experiment before any new axis scoring. The
12 rows are two ATP-grasp boundary rows, four current hydrolase controls, two
ASKHA controls, two GHMP/PfkB small-molecule kinase controls, and two GHKL/NDK
countercontrols. It is preregistration only: no new geometry, sequence,
Foldseek, inverse-gate, or production-fingerprint scoring was run to select the
rows, and no import or production gate is open.
`artifacts/v3_atp_grasp_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`
then closes the frozen ATP-grasp tranche as review-only terminal evidence:
four current hydrolase controls are `mechanism_match`, six neighboring
ATP-family controls are `out_of_scope`, and both ATP-grasp boundary rows are
`terminal_rejection` because prior expert review rejected those current label
candidates and the source-free ATP-grasp axis is absent. The matching
`artifacts/v3_atp_grasp_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json`
keeps EC/name, geometry retrieval, sequence, ESM, and Foldseek baselines
diagnostic only; no superiority claim or production path is opened.

`artifacts/v3_ghkl_family_readiness_packet_20260520.json` adds a second
ATP-family readiness packet for GHKL/Bergerat kinases. The two
expert-supported rows (`m_csa:327` CheA and `m_csa:603` pyruvate dehydrogenase
kinase) both have local nucleotide/Mg context, but both remain non-countable
expert-rejected mismatch lanes with `metal_dependent_hydrolase` top1 collapse.
The packet records GHKL fold, histidine/protein-acceptor identity, hydrolase,
generic ATP/Mg, and neighboring ATP-family counteraxis blockers. GHKL remains
0 countable positives, 0 source-free-axis-ready rows, and no-go for production
fingerprint expansion.
`artifacts/v3_atp_family_readiness_index_20260520.json` rolls up the
ATP-family queue after ASKHA and ATP-grasp terminal tranches. It keeps all nine
ATP/phosphoryl-transfer families review-only: ASKHA and ATP-grasp are closed
as no-go tranches, GHKL has a packet but no frozen tranche yet, ePK stays
research-lane-only, and NDK/PfkB/GHMP/PfkA/dNK still need packets before any
scoring. The recommended next main-loop ATP-family item is a frozen
GHKL-vs-neighbor-ATP-family control tranche.

The run also opens and closes a genuinely new prospective external
glycosyltransferase mini-campaign. `artifacts/v3_prospective_external_glycosyltransferase_minicampaign_freeze_20260520.json`
freezes 20 reviewed UniProtKB/Swiss-Prot EC 2.4.1.* rows before scoring, with
catalytic-activity text, active-site annotation, at least one PDB
cross-reference, prior-external-pool exclusions, and a two-row cap per primary
EC number. `artifacts/v3_prospective_external_glycosyltransferase_minicampaign_decision_packet_20260520.json`
then closes all 20 as review-only terminal rejections by uncovered mechanism
lane: glycosyltransferase chemistry is outside the current 8 production
fingerprints and covered import-counterevidence lanes, so 0 rows were scored
or import-gated. `artifacts/v3_glycosyltransferase_minicampaign_baseline_comparison_20260520.json`
keeps EC/keyword routing diagnostic only and makes no superiority claim.
`artifacts/v3_glycosyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json`
now adds the deterministic 5-mer nearest-current-reference check for the same
20 frozen rows against 737 current references. It reports one crude
near-neighbor alert, but the terminal decision is unchanged because sequence
neighboring cannot remove the uncovered glycosyltransferase-lane blocker.

As of the 2026-05-20T20:17:20Z automation run,
`artifacts/v3_prospective_external_methyltransferase_minicampaign_freeze_20260520.json`
freezes a genuinely new 20-row Swiss-Prot EC 2.1.1.x methyltransferase surface
before outcome scoring. The freeze required reviewed UniProt rows with
catalytic-activity text, active-site annotation, and at least one PDB
cross-reference, excluded imported external hard negatives and prior external
candidate pools, capped selection at two rows per primary EC number, and did
not use current-fingerprint scores, sequence-neighbor outcomes, Foldseek, ESM,
or ePK evidence for selection.

`artifacts/v3_prospective_external_methyltransferase_minicampaign_decision_packet_20260520.json`
then closes the exact frozen set as 20/20 review-only terminal rejections by
`terminal_rejection_uncovered_mechanism_lane`. The current 8-fingerprint
universe and `0.4115` abstention floor are recorded, but 0 rows were scored
because SAM/one-carbon methyltransferase chemistry is outside the current
production fingerprint universe and outside covered external hard-negative
counterevidence lanes. `artifacts/v3_methyltransferase_minicampaign_baseline_comparison_20260520.json`
adds the no-claim baseline diagnostic: EC/keyword routing detects the
methyltransferase lane, while geometry, deterministic k-mer, ESM, and Foldseek
are intentionally unrun because the terminal pre-scoring lane blocker is
decisive.
`artifacts/v3_methyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json`
adds the deterministic 5-mer nearest-current-reference check for the same 20
frozen rows against 737 current reference sequences. It reports two crude
near-neighbor alerts, but the terminal decision is unchanged because sequence
neighboring cannot remove the uncovered methyltransferase-lane blocker.

Evidence-based confidence call: confidence is high that this is a real
prospective small win rather than a recycled terminal tranche: selection was
documented before decisions, terminal failures were preserved, and import
evidence is separated from review-only UniProt context. Confidence is high that
no label import, registry edit, or production fingerprint expansion is
authorized by this mini-campaign.

The same run adds
`artifacts/v3_askha_family_readiness_packet_20260520.json` as the next
non-ePK family-readiness packet outside the exhausted six-family queue. ASKHA
has four expert-supported boundary rows from the ATP/phosphoryl-transfer family
expansion (`m_csa:592`, `m_csa:643`, `m_csa:651`, and `m_csa:696`), but 0
countable positive seeds and 0 source-free-axis-ready rows. The packet records
ATP/Mg and sugar/carboxylate acceptor evidence needs, hydrolase top1 collapse,
ATP-family counterfamilies, and a frozen ASKHA-vs-ATP-family control tranche
as the next exact review-only experiment. No scoring, threshold, registry edit,
or label import is authorized.

`artifacts/v3_askha_vs_atp_family_control_tranche_preregistration_20260520.json`
now freezes that exact next experiment before any outcome scoring. The tranche
contains 14 review-only rows: four ASKHA boundary rows, four current
production hydrolase controls, and six ATP-family countercontrols spanning
ATP-grasp, GHMP, PfkB, GHKL, and NDK. It is a preregistration only: it opens no
production scoring, label import, registry edit, or fingerprint expansion, and
the next work must compute only the preregistered local axes and duplicate
screens before terminal decisions.

Late in the same run, the policy-harness sibling worktree contained 15 newer
dirty JSON outputs after the latest main ePK synthesis. They were validated in
`artifacts/v3_epk_policy_harness_late_dirty_output_receipt_20260520.json` as a
receipt rather than a new full synthesis: ANP/AMP-PNP surfaces and
cross-ligand sibling-control stresses all stayed review-only, with abstentions
or bounded search-surface exhaustion, 0 expectation mismatches, and no
production claim. This does not change the ePK decision; it only tells the next
main run that a full resynthesis should include these lane outputs if they are
still present or pushed.

`artifacts/v3_epk_fresh_research_lane_push_synthesis_20260520.json` also
integrates fresh remote ePK lane pushes after the latest main synthesis. The
positive-evidence branch adds handoff-only commits for the already synthesized
9IZ0/legacy-ANP-PB work. The newer substrate-role-identity lane is more
decisive: a 54-row reciprocal entity-context probe found that a source-free
folded-Tyr rescue recovers `9UUR`/`9UUX` but also admits `9UW4` as a false
positive. ePK therefore stays no-go and research-lane-only; the exact next
research experiment, if continued outside the main loop, is
`epk_local_burial_solvent_exposure_probe_v1_review_only`.

`artifacts/v3_main_loop_small_win_decision_register_20260520.json` collects the
current run's terminal choices into one review-only register: refreshed ePK
no-go, the late ePK policy-harness receipt, fresh remote ePK lane push
synthesis, methyltransferase terminal rejections, methyltransferase diagnostic
baselines, ASKHA readiness no-promotion, and the ASKHA control-tranche freeze.
It is intended as the next run's decision map, not as evidence for label import
or production scoring.

As of the 2026-05-20T20:12:12Z automation run,
`artifacts/v3_epk_research_lane_synthesis_20260520.json` has been refreshed
from the four sibling ePK research-lane worktrees after a fresh fetch of main.
The main run did not copy production changes or merge lane code. It validated
143 JSON files and 4 JSONL ledgers with 0 parse errors. The refreshed synthesis
adds 36 lane JSON files beyond the prior main synthesis, including the
positive-evidence legacy ANP/PB audit, 2025/2026 phrase follow-ups,
same-author-chain false-positive stress, expanded sibling-control rollups, and
the terminal-gamma geometry lead sibling-control stress.

The ePK decision is unchanged: production activation remains no-go. The
positive lane still has 0 fresh clean folded-protein positives; 9IZ0 joins the
peptide-only review set but has a local-metal caveat, and the legacy ANP/PB
audit supports only review-lane helper handling for 3O7L/4JDI. The
false-positive lane found 7 same-author-chain entity-reuse pressure IDs across 820
rows but 0 current-rule topology-clear counterexamples. The sibling-control
lane now records 64 gamma/metal controls, 47 weak-rule counterexamples, and 15
strict product controls blocked by the source-free substrate-identity
counteraxis. The policy lane completed the terminal-gamma lead/control stress:
six geometry leads plus six matched sibling controls all abstained with 0
expected-decision mismatches and 0 counterexamples.

Evidence-based confidence call: confidence is high that ePK remains review-only
and should not return to the main-loop critical path. Confidence is moderate
that the useful future ePK work is a research-lane-only source-free
substrate-role extractor design, because the latest terminal-gamma stress
proved fail-closed behavior but still did not create an accepted role policy,
threshold, external hard-negative re-audit, registry edit, or label import.

As of the 2026-05-20T19:05:55Z automation run,
`artifacts/v3_epk_research_lane_synthesis_20260520.json` has been refreshed
again from the four ePK sibling research-lane worktrees and origin research
branches before unrelated main-loop work. The main run did not merge lane code
or copy production changes. It validated 107 JSON files and 4 JSONL ledgers
with 0 parse errors across the positive-evidence, false-positive-hunter,
sibling-control, and policy-harness lanes. Several lane worktrees still carry
uncommitted outputs because linked-worktree Git metadata writes are blocked in
their sandboxes; this synthesis treats them as review-only evidence.

The refreshed synthesis keeps ePK out of production. The positive-evidence
lane now adds useful review-only peptide positives (`1O6K`, `1O6L`, `4DG0`,
`3O7L`, and `4JDI`) but still adds 0 fresh clean folded-protein positives.
`2V55` and `3BEG` reject as clean processive folded-substrate evidence because
source-mapped acceptors are distant from ANP gamma or absent from modeled
substrate regions. The false-positive lane found 0 current-rule auth-namespace
counterexamples on the bounded edge-case stress, while preserving namespace
pressure as a future regression concern. The sibling-control lane adds 15
strict product-state controls and blocks all 15 under a review-only
substrate-identity counteraxis, which falsifies weak distance-only rules but
does not create a scorer. The policy harness keeps the fresh ATP terminal-gamma
chemcomp surfaces review-only and abstained/fail-closed.

Evidence-based confidence call: confidence is high that ePK remains no-go for
production activation because the fresh lanes add no ePK score, threshold,
external hard-negative scored re-audit, registry edit, label import, or
fingerprint expansion. Confidence is moderate that the only useful future ePK
follow-up is research-lane-only legacy ANP/PB terminal-atom auditing or a
chemcomp ATP terminal-gamma tranche; neither belongs on the main-loop critical
path until it resolves a preregistered blocker.

As of the same 2026-05-20T19:05:55Z automation run,
`artifacts/v3_source_complete_external_minicampaign_blocker_review_20260520.json`
records that the current source-complete post-P06744 external surface is not a
clean new prospective mini-campaign: all six source-complete rows already have
bounded sequence, current-countable Foldseek, and terminal decision outcomes,
and all six are review-only terminal rejections by current-countable
structural duplicate signal. The artifact therefore closes that reuse path
without import and requires genuinely new external sourcing for the next
prospective campaign.

The fallback small win is
`artifacts/v3_schiff_base_lyase_control_tranche_preregistration_20260520.json`.
It freezes 15 review-only rows before any new tranche scoring: Q9BXD5 as the
single external Schiff-base lyase positive-like row, five current
`heme_peroxidase_oxidase` controls, five current `plp_dependent_enzyme`
controls, two current `ser_his_acid_hydrolase` controls, and two current
`metal_dependent_hydrolase` controls. The artifact documents selection before
outcome scoring, uses existing source/control artifacts only for provenance,
and does not run new geometry axes, thresholds, inverse-gate scores,
production-fingerprint scoring, registry edits, or label imports.
`artifacts/v3_schiff_base_lyase_control_tranche_axis_decisions_20260520.json`
then closes that exact frozen row set with review-only terminal decisions: 14
current controls remain `mechanism_match` rows for their existing context, and
Q9BXD5 stays `needs_review` because its Schiff-base evidence is source-traced
rather than source-free and broader duplicate/factory blockers remain open.
`artifacts/v3_schiff_base_lyase_control_tranche_baseline_comparison_20260520.json`
adds the no-claim baseline diagnostic for the same frozen tranche. EC/name
keyword routing finds Q9BXD5 but also over-admits the PLP current-control
`m_csa:186`; it cannot detect the source-free-axis gap or duplicate/factory
blockers. Q9BXD5 has bounded current-reference sequence no-signal and ESM
sidecar context, but the ESM signal remains a representation holdout and
Foldseek current-countable screening is not available for Q9BXD5 in this
tranche.

Evidence-based confidence call: confidence is high that no prospective
source-complete external mini-campaign can be honestly claimed from the current
post-P06744 surface because the rows are already terminally decided. Confidence
is moderate-to-high that the frozen Schiff-base tranche is the right next
non-ePK experiment because it directly tests the observed Q9BXD5 heme-collapse
failure mode against heme, PLP, and hydrolase controls while keeping all
promotion gates closed. Confidence is high that Schiff-base lyase is still a
no-go production fingerprint because the source-free Schiff-base axis-ready
count is 0.

The same run also stages and closes the next ranked non-ePK fallback tranche
for DNA glycosylase/lyase.
`artifacts/v3_dna_glycosylase_lyase_control_tranche_preregistration_20260520.json`
freezes 11 rows before scoring: P06746 as the single external DNA Pol X/5'-dRP
lyase positive-like row, five current `flavin_dehydrogenase_reductase`
controls, and five current out-of-scope controls.
`artifacts/v3_dna_glycosylase_lyase_control_tranche_axis_decisions_20260520.json`
then records review-only terminal decisions for that exact set: P06746 remains
`needs_review`, five flavin controls remain `mechanism_match`, and five
out-of-scope controls remain `out_of_scope`. The source-free DNA-lyase geometry
axis-ready count is 0, so no production fingerprint, threshold, registry edit,
or label import is authorized.
`artifacts/v3_dna_glycosylase_lyase_control_tranche_baseline_comparison_20260520.json`
adds the no-claim baseline diagnostic: EC/name keyword routing finds only
P06746 and cannot detect source-free geometry or duplicate/factory blockers;
sequence and ESM sidecar evidence is available only for P06746, and no
Foldseek current-countable screen is available for P06746 in this tranche.
`artifacts/v3_mechanism_family_readiness_index_post_tranche_refresh_20260520.json`
rolls up the family queue after these tranche decisions: glycoside hydrolase,
Schiff-base lyase, and DNA glycosylase/lyase are closed as terminal
review-only no-go tranches with 0 source-free-axis-ready families. SDR/AKR and
sugar-phosphate isomerase remain packet-only no-go families; the recommended
next non-ePK queue item is a frozen SDR/AKR/NAD(P) control tranche if no
source-complete external campaign is available.
That recommended queue item is now frozen in
`artifacts/v3_sdr_akr_nadp_control_tranche_preregistration_20260520.json`:
14 rows total, including O14756 SDR, C9JRZ8 AKR, four clean SDR-like EC 1.1.1
abstention controls, four current flavin controls, and four current heme
controls. The artifact is preregistration only and does not run NAD(P) axes,
thresholds, inverse-gate scores, production scoring, registry edits, or label
imports. `artifacts/v3_sdr_akr_nadp_control_tranche_axis_decisions_20260520.json`
now closes those exact frozen rows as review-only terminal evidence: O14756
and C9JRZ8 remain `needs_review`, four external SDR-like abstention controls
are `ambiguous`, and eight current redox controls remain `mechanism_match`.
The source-free SDR/AKR/NAD(P) axis-ready count is 0, so no production
fingerprint expansion, threshold, registry edit, or label import is
authorized. The no-claim companion
`artifacts/v3_sdr_akr_nadp_control_tranche_baseline_comparison_20260520.json`
records that EC/name routing over-admits broad redox controls, bounded
sequence/ESM context is diagnostic only, and Foldseek current-countable
screening was not available for the external positive-like rows in this
tranche.

Updated confidence call: confidence is high that the current non-ePK family
queue has produced terminal small wins rather than production candidates:
glycoside hydrolase, Schiff-base lyase, DNA glycosylase/lyase, and SDR/AKR
all remain review-only no-go surfaces with 0 source-free-axis-ready families.
The sugar-phosphate-isomerase fallback is now frozen in
`artifacts/v3_sugar_phosphate_isomerase_control_tranche_preregistration_20260520.json`:
11 rows total, including P34949 as the positive-like row, four current
`flavin_dehydrogenase_reductase` controls, two current
`flavin_monooxygenase` controls, and four current out-of-scope controls. It is
preregistration only.
`artifacts/v3_sugar_phosphate_isomerase_control_tranche_axis_decisions_20260520.json`
then closes the same frozen rows as review-only terminal evidence: P34949 is
`needs_review`, six current flavin controls remain `mechanism_match`, and four
current controls remain `out_of_scope`. The source-free sugar-phosphate axis
ready count is 0.
`artifacts/v3_sugar_phosphate_isomerase_control_tranche_baseline_comparison_20260520.json`
adds the matching no-claim baseline diagnostic: EC/name routing finds only
P34949 but cannot detect the source-free geometry or duplicate/factory
blockers, and Foldseek current-countable screening is unavailable in this
tranche. The six-family non-ePK small-win queue is now exhausted as terminal
review-only no-go evidence; the next main-loop choice should be genuinely new
external sourcing or a new family packet outside this queue.

As of the 2026-05-20T18:04:27Z automation run,
`artifacts/v3_prospective_external_source_gap_minicampaign_freeze_20260520.json`
freezes a second prospective external mini-campaign before scoring. This
18-row source-gap tranche is deliberately different from the closed
structural-duplicate mini-campaign: it selects six rows with missing
active-site source evidence, six rows with source-specificity or sampling-cap
blockers, and six methyltransferase rows from an uncovered external mechanism
lane. The freeze excludes the closed 12-row mini-campaign and the three
imported external hard negatives. No sequence-neighbor, Foldseek, inverse-gate,
production-fingerprint, EC/keyword outcome, or import-gate scoring was used to
select rows.

`artifacts/v3_prospective_external_source_gap_minicampaign_decision_packet_20260520.json`
closes those 18 rows as terminal review-only rejections before scoring:
6 `terminal_rejection_missing_active_site_source_evidence`, 6
`terminal_rejection_source_specificity_or_sampling_blocker`, and 6
`terminal_rejection_uncovered_mechanism_lane`. The packet explicitly separates
source/import evidence from review-only context, records 0 sequence-screened,
0 Foldseek-screened, and 0 inverse-gate-scored rows, and authorizes 0 label
imports or production fingerprint edits.
`artifacts/v3_source_gap_minicampaign_baseline_comparison_20260520.json`
records the corresponding no-claim baseline diagnostic: EC/keyword lane routing
would admit all 18 rows but detects none of the source blockers, while
geometry, deterministic k-mer, ESM, and Foldseek metrics are intentionally
unscored/unavailable because the rows fail before scoring.

The same run adds two non-ePK family-readiness packets:
`artifacts/v3_schiff_base_lyase_readiness_packet_20260520.json` for Q9BXD5
and `artifacts/v3_dna_glycosylase_lyase_readiness_packet_20260520.json` for
P06746. Both are review-only no-go packets: each has one positive-like row,
no source-free production axis, unresolved duplicate/representation blockers,
and a frozen 10-20 row control-tranche experiment as the next admissible step.
`artifacts/v3_mechanism_family_readiness_index_refresh_20260520.json` folds
those packets into the existing non-ePK index without changing any registry.

Evidence-based confidence call: confidence is high that the new external
source-gap mini-campaign is a real small win because it produces terminal
decisions and prevents source-blocked rows from drifting into scored/import
surfaces. Confidence is high that Schiff-base lyase and DNA
glycosylase/lyase remain no-go production fingerprints because both packets
are single-row, source-traced, and blocked by duplicate/representation
questions. Confidence is moderate that the next useful main-loop experiment is
either a genuinely source-complete external mini-campaign or one frozen
Schiff-base/DNA-lyase control tranche, not ePK production work.

As of the 2026-05-20T17:15:21Z automation run,
`artifacts/v3_glycoside_hydrolase_control_tranche_axis_decisions_20260520.json`
turns the frozen 15-row glycoside hydrolase control tranche into terminal
review-only decisions. Candidate selection remained frozen before outcome
scoring. The packet uses existing preregistered axes and duplicate-screen
evidence only: bounded current-reference sequence search, external all-vs-all
sequence search, external structural clustering, the prior P33025
current-countable structural duplicate screen, active-site/source evidence,
Q6NSJ0 glycoside boundary/import-safety artifacts, and current 1,000-slice
geometry/retrieval context for the 10 production controls.

The terminal decision counts are 10 `mechanism_match` current-control rows, 2
`ambiguous` external rows (`P30176` and `P29372`), 1 `needs_review` boundary row
(`Q6NSJ0`), and 2 `terminal_rejection` rows (`P33025` and `O60568`). All five
external rows have bounded current-reference sequence no-signal and external
all-vs-all structural no-signal, but only P33025 has a prior current-countable
structural duplicate signal and is therefore rejected on that axis. Q6NSJ0
remains useful boundary evidence but not import-ready: source-traced acidic
dyad/glycan-pocket context exists, while source-free axis, broader duplicate
screening, terminal review, and factory gates remain unresolved.

Evidence-based confidence call: confidence is high that the frozen glycoside
tranche produced a visible small win without label import, registry edits, or
fingerprint expansion. Confidence is high that glycoside hydrolase is still a
no-go production fingerprint because the source-free glycoside axis ready count
is 0. Confidence is moderate that future useful work should resolve
source-free acidic-dyad/glycan-pocket axes and current-countable structural
duplicate coverage for unresolved external rows before any import path.

The same run adds
`artifacts/v3_glycoside_hydrolase_control_tranche_baseline_comparison_20260520.json`
as a modern baseline diagnostic for the frozen tranche. It compares the
terminal axis packet with EC/protein-name keyword routing, MMseqs2
current-reference sequence search, a deterministic 5-mer nearest-neighbor
baseline, available ESM-2 sidecars, and the all-30 Foldseek external sidecar.
It makes no superiority claim: 5/5 external rows have sequence no-signal and
external Foldseek no-signal, the deterministic 5-mer baseline has 0
near-neighbor alerts at the diagnostic threshold, and ESM-2 sidecars cover only
2/5 external rows. The Foldseek sidecar is external-external only and does not
replace current-countable structural duplicate screening.

As of the 2026-05-20T17:08:53Z automation run, fresh ePK research-lane
outputs pushed after the prior main synthesis, plus newer dirty sibling
worktree outputs, are integrated in
`artifacts/v3_epk_research_lane_synthesis_20260520.json`. The main run did
not merge lane code or copy production changes. It validated 54 JSON files and
4 JSONL ledgers with 0 parse errors across the positive-evidence,
false-positive-hunter, sibling-control, and policy-harness lanes.

The refreshed synthesis keeps ePK out of production. The positive-evidence
lane reviewed 700 unique RCSB PDB IDs plus 61 Europe PMC/PubMed-style PMIDs
on full-length ATP/phosphorylation-site surfaces and still found 0 fresh clean
folded-protein positives beyond repeat `5HVK` and peptide anchors. The
false-positive lane found no topology-clear cross-chain counterexample on the
bounded ATP-like/Mg and gamma-chain namespace attacks, but preserved namespace
and non-ATP gamma-like pressure cases as review-only attack material. The
sibling-control lane now rolls up 8 families, 452 reviewed rows, 64 gamma/metal
controls, 47 unique weak-rule counterexamples, and 17 product-state branch
controls. The policy harness ran the fresh folded role-identity stress tranche
fail-closed: 25 candidates reviewed, 0 nonconfounded candidates within cutoff,
and 6/6 rows abstained with 0 expected-decision mismatches.

Evidence-based confidence call: confidence is high that ePK remains a no-go
for production activation because the fresh lanes add no score, threshold,
external hard-negative scored re-audit, registry edit, label import, or
fingerprint expansion. Confidence is high that the main loop should continue
with the preregistered glycoside hydrolase control tranche rather than reopen
ePK by default. Confidence is moderate that the only useful future ePK work is
research-lane-only PKA/CFTR site-specific acceptor mapping, with source review
kept after local geometry inspection.

As of the 2026-05-20T16:00:50Z automation run,
`artifacts/v3_glycoside_hydrolase_control_tranche_preregistration_20260520.json`
freezes the next review-only non-ePK family tranche before any new scoring. The
15 frozen rows include five external glycan/glycoside candidates from the
external source manifest (`Q6NSJ0`, `P30176`, `P29372`, `P33025`, and
`O60568`) plus five current `metal_dependent_hydrolase` and five current
`ser_his_acid_hydrolase` controls selected deterministically from registry
order. No geometry, sequence-neighbor, Foldseek, inverse-gate, or production
fingerprint scoring was run to choose these rows. The next step is to compute
only the preregistered review-only local axes and duplicate screens, then emit
terminal decisions without import unless a later explicit gated cycle passes.

As of the 2026-05-20T16:00:50Z automation run,
`artifacts/v3_mechanism_family_readiness_index_20260520.json` compares the
current review-only family packets for SDR, AKR, glycoside hydrolase, and
sugar-phosphate isomerase. All four remain no-go for production scoring,
fingerprint expansion, registry edits, or label import. The index recommends
`glycoside_hydrolase_vs_metal_hydrolase_control_tranche_v1_review_only` as the
next non-ePK family experiment because it most directly tests the observed
metal-hydrolase boundary collapse with acidic-dyad evidence and absent
metal-role context. Any next family experiment must freeze 10-20 rows before
scoring.

As of the 2026-05-20T16:00:50Z automation run, the fourth fallback
mechanism-family readiness packet is staged for sugar-phosphate isomerase in
`artifacts/v3_sugar_phosphate_isomerase_readiness_packet_20260520.json`. It
synthesizes the existing P34949 sugar-phosphate-isomerase scope control, pilot
terminal decisions, active-site evidence decisions, and modern baseline context
into a review-only go/no-go packet. The decision is a no-go for production
fingerprint expansion: P34949 is the only direct positive-like row, Arg295
active-site evidence is source-traced rather than a frozen source-free local
axis, the weak flavin top1 is countered by absent flavin context rather than a
calibrated scorer, and expert review plus broader duplicate screening remain
unresolved.

Evidence-based confidence call: confidence is high that the sugar-phosphate
isomerase packet usefully preserves a terminal review-only scope decision and
not a production fingerprint. Confidence is moderate that the next admissible
experiment is a 10-20 row review-only sugar-phosphate-isomerase versus flavin
control tranche with basic/polar active-site, flavin-context, and substrate
pocket axes frozen before scoring.

As of the 2026-05-20T16:00:50Z automation run, the third fallback
mechanism-family readiness packet is staged for glycoside hydrolase acidic-dyad
chemistry in
`artifacts/v3_glycoside_hydrolase_family_readiness_packet_20260520.json`. It
synthesizes the existing Q6NSJ0 glycoside-hydrolase boundary control, pilot
terminal decisions, active-site evidence decisions, and modern baseline context
into a review-only go/no-go packet. The decision is a no-go for production
fingerprint expansion: Q6NSJ0 is the only direct positive-like row, its
Asp463/Asp520 acidic dyad is source-traced rather than a frozen source-free
role rule, the row remains deferred/rejected from the pilot surface, and the
control has not been integrated into import-safety adjudication or full
factory gates.

Evidence-based confidence call: confidence is high that the glycoside
hydrolase packet is useful boundary evidence against metal-hydrolase collapse
and not a production fingerprint. Confidence is moderate that the next
admissible experiment is a 10-20 row review-only glycoside-hydrolase versus
metal/ser-his-acid hydrolase tranche with acidic-dyad, metal-ligand, and glycan
pocket axes frozen before scoring.

As of the 2026-05-20T16:00:50Z automation run, the second fallback
mechanism-family readiness packet is staged for AKR/NADP redox in
`artifacts/v3_akr_family_readiness_packet_20260520.json`. It synthesizes the
existing C9JRZ8 AKR/NADP repair-control row, AKR import-safety adjudication,
pilot terminal decisions, active-site evidence decisions, SDR sibling context,
and the modern baseline comparison into a review-only go/no-go packet. The
decision is a no-go for production fingerprint expansion: C9JRZ8 is the only
direct positive-like AKR row, its post-repair status is still `needs_review`,
the NADP axis is sequence/source-context rather than direct local ligand
geometry, and broader duplicate screening, terminal acceptance, heuristic
scoring, and full factory gates remain unresolved.

Evidence-based confidence call: confidence is high that the AKR packet is a
useful family-readiness small win and not a production fingerprint, because it
names the positive-like row, counterfamilies, cofactors, active-site evidence,
failure modes, and one next experiment while preserving 0 label imports and 0
registry edits. Confidence is moderate that the next admissible AKR step is a
10-20 row review-only AKR/SDR/flavin/heme control tranche with a frozen
source-free NAD(P) and catalytic-Tyr local-axis design before scoring.

As of the 2026-05-20T16:00:50Z automation run, fresh ePK research-lane
outputs from the four sibling worktrees are integrated as review-only synthesis
in `artifacts/v3_epk_research_lane_synthesis_20260520.json`. The main run did
not merge lane code or copy production changes. It validated 35 JSON/JSONL
lane artifacts across the positive-evidence, false-positive-hunter,
sibling-control, and policy-harness lanes, including local sibling-worktree
outputs that had not yet been pushed from those linked worktrees.

The synthesis keeps ePK out of production. The positive-evidence lane found
review-only peptide/protein-substrate anchors but the later explicit
phosphoacceptor/full-length substrate pass reviewed 177 unique PDB IDs and
found 0 fresh clean folded-protein positives. The false-positive lane found no
topology-clear counterexample on bounded pushed surfaces and newer local
cross-chain stress surfaces, but those surfaces remain bounded review attacks
rather than safety proof. The sibling-control lane found counterexamples for
distance-only and nearest-oxygen rules across ASKHA, dNK, GHKL, GHMP, and an
ATP-grasp follow-up. The policy harness is frozen only as a fail-closed
review-only policy: all diagnostic and synthetic cutoff rows abstain, and no
accepted source-free acceptor/role extractor exists.

Evidence-based confidence call: confidence is high that current ePK production
activation remains a no-go because every lane either preserves a blocker or
adds review-only falsification controls, with no score, threshold, external
hard-negative scored re-audit, registry edit, label import, or fingerprint
expansion. Confidence is moderate that a future exact ePK experiment can be
useful only if it is a fresh post-policy,
`epk_fresh_nonconfounded_folded_substrate_role_identity_stress_v1_review_only`
tranche with source-free features computed before source validation. Confidence
is high that the main automation should continue visible non-ePK small wins
rather than resume ePK as the default task.

As of the 2026-05-20T14:58:48Z automation run, the frozen prospective external
mini-campaign has a terminal review-only outcome in
`artifacts/v3_prospective_external_minicampaign_decision_packet_20260520.json`.
The candidate-freeze artifact selected 12 external review-only candidates
across oxidoreductase, lyase, and isomerase lanes after excluding the prior
external pool, prior new-candidate surfaces, prior terminal duplicate rejects,
the three imported external out-of-scope labels, and the explicit P22830
deferral. Backend MMseqs2 sequence search completed: 11 rows had no current
reference near-duplicate signal and `P07237` was an exact-reference terminal
rejection. This run materialized all 11 missing AlphaFold candidate sidecars in
`artifacts/v3_prospective_external_minicampaign_structural_coordinates_20260520/`
and records their digests in
`artifacts/v3_prospective_external_minicampaign_coordinate_materialization_20260520.json`.
The Foldseek current-countable structural screen then completed 7392/7392
query-target pairs against 672 staged current countable coordinate groups; all
11 sequence-clean rows have high-TM current-countable duplicate signals
(`TM >= 0.7`) and are terminal review-only rejections. The inverse gate remains
configured at the calibrated `0.4115` threshold, but it scored 0 rows because
no candidate survived structural duplicate screening. No external row became
countable or import-ready.

The modern-baseline comparison is in
`artifacts/v3_modern_baseline_comparison_20260520.json`. It compares the
current geometry/retrieval triage against EC/keyword lane routing,
deterministic k-mer nearest-neighbor proxy, cached ESM-2 8M representation, and
the available Foldseek all-30 sidecar. The artifact makes no superiority claim:
geometry abstains on all 12 mapped-control rows at `0.4115` and uses no text or
label fields for scoring, but its review top1s still collapse 9/12 rows to
`metal_dependent_hydrolase` with 9 scope/top1 mismatches. K-mer flags one
representation holdout; ESM-2 flags three; the Foldseek sidecar is useful
structural-diversity context only and does not cover the new prospective
mini-campaign rows. A focused regression test in
`tests/test_automation_small_win_artifacts.py` pins the review-only status,
zero-import outcome, coordinate materialization, completed Foldseek duplicate
screen, 8-fingerprint/threshold metadata, and no-superiority baseline caveat.

As of the 2026-05-20T13:57:21Z automation run, the first fallback
mechanism-family readiness packet is now staged for SDR/NAD(P) redox in
`artifacts/v3_sdr_family_readiness_packet_20260520.json`. It synthesizes the
existing O14756 SDR repair-control row, SDR import-safety adjudication, the
36-row SDR EC 1.1.1 consistency check, AKR/NADP sibling-control artifacts, and
the modern baseline comparison into a review-only go/no-go packet. The decision
is a no-go for production fingerprint expansion: O14756 is the only direct
positive-like SDR row, its post-repair status is still `needs_review`, and the
broader duplicate screen, post-repair terminal review, and full factory gate
remain unresolved. The packet also keeps source-traced active-site overlap,
Rhea/InterPro context, EC labels, protein names, and UniProt prose out of
predictive use until a source-free local axis is preregistered.

Evidence-based confidence call: confidence is high that the current SDR packet
is useful as a family-readiness small win and not a production fingerprint,
because it identifies concrete positives, cofactors, counterfamilies,
active-site evidence, failure modes, and one next experiment while preserving 0
label imports and 0 registry edits. Confidence is moderate that SDR is a
better next non-ePK experiment than another ePK audit, because the existing
O14756/AKR artifacts already define a bounded SDR-vs-AKR control tranche.
Confidence is low that current EC 1.1.1 or representation evidence alone can
support a claim: the 36-row consistency surface is clean abstention context,
not positive SDR calibration.

The same run also adds a sequence-baseline diagnostic for the frozen
mini-campaign in
`artifacts/v3_prospective_external_minicampaign_sequence_baseline_diagnostic_20260520.json`.
It compares the already frozen 12 rows against the bounded MMseqs2
current-reference search and a deterministic 5-mer nearest-neighbor baseline
from the committed FASTA sidecars. After coordinate materialization and
Foldseek rerun, the diagnostic agrees with the terminal surface: 12/12 rows
are terminal rejections, with `P07237` rejected as an exact-reference holdout
and the other 11 rejected by current-countable structural duplicate signal. It
retains one useful baseline caveat: `P31040` remains below the MMseqs2
near-duplicate threshold and has a high deterministic k-mer neighbor signal to
`Q9YHT1`, but its stronger terminal blocker is the completed structural
duplicate screen.

Evidence-based confidence call: confidence is high that the frozen
mini-campaign is now closed as a useful negative result rather than blocked by
missing sidecars, because the pair cache is complete and all sequence-clean
rows have current-countable high-TM duplicate signals. Confidence is high that
no import, registry edit, or inverse-gate claim is authorized from this set.
The next external mini-campaign should use genuinely new preregistered sourcing
or a different frozen surface, not rerun these structurally duplicated rows.

As of the 2026-05-20T12:55:46Z automation run, the completed ePK subagent
packets are integrated as review-only synthesis in
`artifacts/v3_epk_subagent_synthesis_20260520.json`. All four JSON packets
under `artifacts/subagents/` validate. The synthesis keeps ePK out of
production: no ePK score, threshold calibration, real external hard-negative
scored re-audit, registry edit, label import, artifact migration, upload,
removal, Git LFS migration, history rewrite, or `removal_allowed=true`
occurred.

The integrated conclusion is a no-go for current ePK production activation.
Substrate-role/substrate-identity is not freeze-ready; it still depends on
narrow peptide identity, bounded topology/role rules, source-context labels,
and weak residue-position heuristics. The ligand-state policy can be frozen
only as `epk_ligand_state_evidence_policy_v0_20260520` for future
review-only prospective tranches selected after the freeze, not activated for
current scoring. Sibling controls are enough to block distance-only threshold
selection but insufficient for a frozen production policy because ATP-grasp is
thin and ASKHA, dNK, GHKL, and GHMP are under-covered. The external stress
packet is diagnostic only: `4EKK` is the single primary future review-only
probe, while `7ZE5`, `7B56`, `7ZDT`, `2JJ2`, `4HPU`, `9L3U`, and `7T55` are
regression-context counterexamples, not clean held-out performance evidence.

Evidence-based confidence call: confidence is high that ePK should remain
review-only after synthesis because all four independent packets converge on
blocked production gates. Confidence is moderate that a future ligand-state
policy can be useful if it is applied only after a prospective freeze with
source context excluded from predictive features. Confidence is low that more
main-loop ePK audit/control churn will produce the next visible win; the main
loop should pivot to prospective external mini-campaign or modern baseline
comparison after this synthesis commit.

As of the 2026-05-20T11:55:15Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
external hard-negative production score, or `removal_allowed=true` occurred.
SSH deploy-key fetch/pull/ls-remote/dry-run push hygiene passed at startup.
The run first recovered coherent dirty review-only synthesis artifacts from
the previous worktree state in commit `5c9b0ae`, without spawning or delegating
new work.

The interrupted AMP-PNP substrate-mode source-review writes are now recovered.
`artifacts/v3_epk_substrate_mode_next_tranche_source_review_amp_pnp_broad41_80_1025.json`
reviews `1O6K`, `1O6L`, and `4HPU`: `1O6K`/`1O6L` carry the explicit blocker
`pkb_gsk3b_source_context_detected_but_exact_akt1_or_chain_mapping_unresolved`,
while `4HPU` rejects by substrate mode. The regenerated broad81-92 review keeps
`4EKK` as the only source-mapped measurement-ready row. The aggregate
`artifacts/v3_epk_substrate_mode_tranche_recovery_decision_1025.json` records
partial recovery: `4EKK` ready, `1O6K`/`1O6L` unresolved, and `4HPU`/`7ZE5`
rejected, with scoring and registry gates still closed.

Fresh folded protein-substrate stress was negative. The new
`artifacts/v3_epk_substrate_mode_folded_source_stress_*_1025.json` scouts cover
bounded RCSB AMP-PNP, ATP, and ANP protein-substrate query surfaces. The
terminal decision reviews 11 topology hits and finds 0 measurement-ready
positives: `2JJ2`, `4HPU`, `7B56`, and `7ZE5` reject by substrate mode; `1TFW`,
`2DRA`, `2Q66`, `2ZH6`, `9L3M`, and `9L3U` are same-chain topology-confounded;
and current positive repeat `1IR3` remains source-mapping unresolved under the
generic fresh-tranche mapper. This is counterevidence and next-experiment
routing only, not clean held-out performance evidence.

Evidence-based confidence call: confidence is higher that `4EKK` is useful
source-mapped review evidence and that the current broad folded-source query
surface is dominated by counterexamples or topology-confounded rows. Confidence
is lower that the generic fresh-tranche source mapper can recover known
protein-substrate positives without pair-specific source rules, because it
leaves `1IR3` unresolved and keeps `1O6K`/`1O6L` non-ready under exact
AKT1/chain requirements. The next useful experiment is a fresh bounded source
tranche with explicit, pre-frozen source-free substrate-identity features or a
pair-specific source-mapping review kept outside predictive scoring.

As of the 2026-05-20T11:23:08Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
external hard-negative production score, or `removal_allowed=true` occurred.
SSH deploy-key fetch/pull/ls-remote/dry-run push hygiene passed at startup,
and startup checks passed: 674 unit tests plus `catalytic_earth.cli validate`
with 682 labels and 8 production fingerprints.

This run sourced a fresh AMP-PNP substrate-query tranche and added a source
review builder for non-topology-confounded substrate-mode rows.
`artifacts/v3_epk_substrate_mode_next_tranche_candidate_scout_amp_pnp_1025.json`
reviews nine fresh AMP-PNP peptide-substrate candidates and finds one
heteromeric topology hit, `4EKK`. The generic source validator blocks it as
insufficient context, but the new source-mapping review in
`artifacts/v3_epk_substrate_mode_next_tranche_source_review_amp_pnp_1025.json`
maps the candidate acceptor from GSK3B structure Ser7 to UniProt `P49841` Ser9,
matches AKT/PKB phosphosite support, records an AMP-PNP gamma-to-acceptor
distance of 3.228 Angstrom, and marks `4EKK` measurement-ready for review-only
controls. The regenerated pre-count and counteraxis artifacts carry this row
while preserving `precount_gate_status=blocked_review_only` and
`threshold_selection_decision=do_not_select_threshold`.

Follow-on stress stayed fail-closed. The old unified broad-stress path plus the
new tranche treats `4EKK` as a generic source-validation blocker, proving the
source-mapping review is a needed review-only bridge rather than a production
feature. A broader AMP-PNP first-40 scout finds only `7ZE5`; the new source
review rejects it because it is a non-topology transporter hit that fails the
substrate-mode rule. Rows 41-80 and 81-92 were scouted and source-validated
(`1O6K`/`1O6L` accepted in rows 41-80; `4EKK` remains blocked by the generic
validator in rows 81-92), but final source-review writes for those two broader
surfaces hit local `ENOSPC`. Treat those two source-review outputs as recovery
items only; the valid scout/source-validation artifacts are preserved.

Evidence-based confidence call: confidence is higher that `4EKK` is a real
source-mapped positive-like review lead for ePK substrate-mode development, and
higher that `7ZE5` is a useful non-topology counterexample blocked by the
current residue-position heuristic. Confidence remains low that this is
production-admissible because `4EKK` depends on source phosphosite context, the
substrate-mode rule is uncalibrated, and the real external hard-negative scored
re-audit remains closed.

Wrap-up verification passed with 676 unit tests, `tests.test_cli` plus
`tests.test_leakage_closure` (285 tests), `catalytic_earth.cli validate`,
artifact migration dry-run/local-file guard at 108 rows with
`removal_allowed=0`, label invariants at 682 total labels (212 seed
fingerprints, 470 out-of-scope, and the three imported UniProt hard negatives
unchanged), JSON validation for new/regenerated artifacts, and `git diff
--check`. `compileall` was skipped because the workspace disk was at capacity;
tests were run with bytecode writes disabled.

As of the 2026-05-20T09:52:30Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
external hard-negative production score, or `removal_allowed=true` occurred.
SSH deploy-key fetch/pull/ls-remote/dry-run push hygiene passed at startup,
and startup checks passed: 665 unit tests plus `catalytic_earth.cli validate`
with 682 labels and 8 production fingerprints.

This run added a source-free MEK/ERK substrate-mode counteraxis prototype and
made it fail closed. `artifacts/v3_epk_mek_erk_substrate_mode_counteraxis_audit_1025.json`
retains all five current positives (`1IR3`, `5HVK`, `6Z3R`, `9UUR`, and
`9UUX`), carries the topology-ambiguity blocker for `7CAG`, `7ZDU`, `7ZE5`,
and `8BMS`, and blocks the previous residual false hits `2JJ2`, `4HPU`,
`7B56`, and `7ZDT` with a weak residue-position rule: tyrosine acceptors or
N-terminal Ser/Thr/Tyr acceptors. The regenerated pre-count and counteraxis
artifacts include this row, but still keep
`precount_gate_status=blocked_review_only` and
`threshold_selection_decision=do_not_select_threshold`.

The immediate fresh-stress follow-up is also review-only. `artifacts/v3_epk_mek_erk_substrate_mode_fresh_stress_audit_1025.json`
checks the targeted MEK1/ERK1 outside-query tranche: fresh nonrepeat controls
`7M0T`, `7M0W`, and `9UW4` have 0 substrate-mode rule hits, while `9UUR` and
`9UUX` remain repeat current-surface rule hits. However, all three fresh
nonrepeat controls are same-chain topology-confounded, so this is not a clean
generalization pass. `artifacts/v3_epk_mek_erk_substrate_mode_existing_scout_gap_audit_1025.json`
then audits the already materialized ePK scout cache and finds no reusable
non-topology-confounded tranche: the 10 unreviewed topology-hit PDBs outside
the current/fresh surfaces are all same-chain topology-confounded. The
regenerated pre-count and counteraxis artifacts carry that negative queue row
too, with the next action now focused on sourcing a new bounded
non-topology-confounded kinase-substrate tranche.

Evidence-based confidence call: confidence is higher that residue-position
substrate mode is useful counterevidence against the current MEK/ERK false-hit
surface. Confidence remains low that it is production-admissible, because the
rule is weak, the fresh controls are topology-confounded, and the existing
scout cache cannot provide a clean non-topology-confounded stress tranche.

Wrap-up verification passed with 674 unit tests, `tests.test_cli` plus
`tests.test_leakage_closure` (283 tests), `catalytic_earth.cli validate`,
`compileall`, targeted CLI/leakage tests, artifact migration dry-run/local-file
guard at 108 rows with `removal_allowed=0`, label invariants at 682 total
labels (212 seed fingerprints, 470 out-of-scope, and the three imported
UniProt hard negatives unchanged), and `git diff --check`.

As of the 2026-05-20T08:52:03Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
external hard-negative production score, or `removal_allowed=true` occurred.
SSH deploy-key fetch/pull/ls-remote/dry-run push hygiene passed at startup,
and startup checks passed: 656 unit tests plus `catalytic_earth.cli validate`
with 682 labels and 8 production fingerprints.

The residual MEK1/ERK1 broad-role false hits are now closed as review-only
counterexamples but not as production evidence.
`artifacts/v3_epk_mek_erk_residual_false_hit_source_adjudication_1025.json`
source-adjudicates `7CAG` and `8BMS` as transporter-context false hits with 0
unresolved residuals, while explicitly keeping
`source_free_predictive_feature_materialized=false`.
`artifacts/v3_epk_mek_erk_source_free_topology_ambiguity_counteraxis_1025.json`
then replaces that specific source-context blocker with a source-free local
hit-pattern probe: same-chain companion topology blocks `7CAG`, reciprocal
cross-chain topology blocks `8BMS`, and `9UUR`/`9UUX` are retained. The
regenerated pre-count and counteraxis artifacts carry the source-free bounded
counteraxis row, but still keep `precount_gate_status=blocked_review_only` and
`threshold_selection_decision=do_not_select_threshold`.

The important negative result is the broader stress audit.
`artifacts/v3_epk_mek_erk_source_free_topology_broader_stress_audit_1025.json`
applies the same source-free topology-ambiguity rule across the broader
MEK/ERK broad-role hit surface. It retains all five positive controls
(`1IR3`, `5HVK`, `6Z3R`, `9UUR`, `9UUX`) and blocks four false hits (`7CAG`,
`7ZDU`, `7ZE5`, `8BMS`), but fails closed because `2JJ2`, `4HPU`, `7B56`, and
`7ZDT` remain false hits. This narrows the next experiment: the topology rule
is useful bounded counterevidence, but ePK still needs an additional
source-free acceptor or substrate-identity axis before any scorer calibration.

Evidence-based confidence call: confidence is higher that the MEK1/ERK1
residuals were real transporter false hits and that local topology ambiguity is
a useful counteraxis ingredient. Confidence remains low that this axis can
generalize alone, because the broader stress audit leaves four known
nonpositive false hits.

Wrap-up verification passed with 665 unit tests, `tests.test_cli` plus
`tests.test_leakage_closure` (274 tests), `catalytic_earth.cli validate`,
`compileall`, targeted CLI/leakage tests, JSON validation for new and
regenerated ePK artifacts, artifact migration dry-run/local-file guard at 108
rows with `removal_allowed=0`, label invariants at 682 total labels (212 seed
fingerprints, 470 out-of-scope, and the three imported UniProt hard negatives
unchanged), and `git diff --check`.

As of the 2026-05-20T07:50:46Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
external hard-negative production score, or `removal_allowed=true` occurred.
SSH deploy-key fetch/pull/ls-remote/dry-run push hygiene passed at startup,
and startup checks passed: 644 unit tests plus `catalytic_earth.cli validate`
with 682 labels and 8 production fingerprints.

The MEK1/ERK1 role-direction blocker is now source-reviewed in a bounded,
review-only lane. `artifacts/v3_epk_mek_erk_phosphosite_source_review_1025.json`
maps `9UUR` and `9UUX` to ERK1 `P27361` Tyr204, supported by UniProt
phosphotyrosine evidence "by MAP2K1 and MAP2K2", with ANP/ATP gamma distances
4.181 and 3.968 Angstrom. The same-chain `9UW4` MEK active-site topology hit is
rejected as a counterexample. The companion
`artifacts/v3_epk_mek_erk_role_control_rerun_1025.json` admits `9UUR`/`9UUX`
only as source-reviewed broad protein-substrate review rows; it does not create
a source-free scorer, threshold, registry edit, label import, or held-out claim.

The follow-on broad-role stress test is the useful negative result.
`artifacts/v3_epk_mek_erk_broad_role_stress_audit_1025.json` retains both
source-reviewed MEK1/ERK1 positives and the three known positive repeats, but a
naive different-chain/distance broad protein-role rule false-hits eight
nonpositive topology rows: `2JJ2`, `4HPU`, `7B56`, `7CAG`, `7ZDT`, `7ZDU`,
`7ZE5`, and `8BMS`. A concrete review-context counteraxis in
`artifacts/v3_epk_mek_erk_context_counteraxis_stress_audit_1025.json` blocks
the six prior-counterexample repeats but still leaves new residual false hits
`7CAG` and `8BMS`; because that blocker uses review context and is not
source-free, production scoring remains closed. The regenerated pre-count and
counteraxis artifacts now carry both blockers:
`mek_erk_broad_role_stress_audit` and
`mek_erk_context_counteraxis_stress_audit`; pre-count remains
`blocked_review_only`, and counteraxis sufficiency remains
`do_not_select_threshold`.

Evidence-based confidence call: confidence is now higher that MEK1/ERK1 has two
real source-authoritative broad protein-substrate review controls, but also
higher that broad protein-role geometry alone is unsafe. The next useful
experiment is not thresholding; it is to source-adjudicate residual new topology
false hits `7CAG` and `8BMS` or replace review-context blocking with a
source-free acceptor/substrate identity feature before any scorer calibration.

Wrap-up verification passed with 656 unit tests, `catalytic_earth.cli
validate`, `compileall`, targeted CLI/leakage tests, JSON validation for the
new artifacts, artifact migration dry-run/local-file guard at 108 rows with
`removal_allowed=0`, label invariants at 682 total labels (212 seed
fingerprints, 470 out-of-scope, and the three imported UniProt hard negatives
unchanged), and `git diff --check`.

As of the 2026-05-20T06:49:30Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
external hard-negative production score, or `removal_allowed=true` occurred.
SSH deploy-key fetch/pull/ls-remote/dry-run push hygiene passed at startup,
and startup checks passed: 642 unit tests plus `catalytic_earth.cli validate`
with 682 labels and 8 production fingerprints.

This run added a small review-only aggregate builder,
`build-epk-ligand-specific-active-query-extension-audit`, and tightened the
heteromeric source validator so MEK1/ERK1 co-complex rows fail closed under a
specific role-direction/phosphoacceptor-state blocker instead of generic
insufficient context. The targeted regression covers that blocker and the new
aggregate CLI.

The fast-science source expansion result is negative but useful.
`artifacts/v3_epk_ligand_specific_active_query_extension_audit_1025.json`
extends the prior RCSB full-text `protein kinase substrate ANP magnesium`
active-query scout from rows 100-228. It fetches 129 additional structures and
finds 9 heteromeric topology hits: known source-valid repeats `5HVK`/`6Z3R`,
known counterexamples `7B56`/`7M0T`/`7M0W`, and four new blocked hits
(`6BBN`, `9UUR`, `9UUX`, `9UW4`). The new MEK1/ERK1 hits are blocked pending
role-direction and phosphoacceptor-state source review; `6BBN` is a
KIF2A/tubulin motor context with same-author-chain topology risk.

Follow-on bounded routes also fail closed:
`artifacts/v3_epk_mek_erk_targeted_extension_audit_1025.json` covers all 32
`MEK1 ERK1 ANP magnesium` hits and accepts 0 new positives;
`artifacts/v3_epk_substrate_cocomplex_text_extension_audit_1025.json` covers
the six `kinase substrate co-complex ANP magnesium` hits and only repeats
known counterexample `2JJ2`;
`artifacts/v3_epk_amp_pnp_protein_query_extension_audit_1025.json` covers 67
broader AMP-PNP protein-query rows and only repeats known counterexamples
`4HPU`/`7ZE5`; `artifacts/v3_epk_adp_product_query_extension_audit_1025.json`
covers the first 100 ADP/product-state rows with 0 topology hits.
`artifacts/v3_epk_atp_protein_query_extension_audit_1025.json` covers the
first 450 `protein kinase substrate ATP magnesium` rows. It finds known
positive repeat `1IR3`, known counterexamples, and seven new blocked topology
hits (`1TFW`, `2DRA`, `2Q66`, `2ZH6`, `7CAG`, `8BMS`, `9BJI`), all RNA
transferase, AAA+/translocase, or transporter contexts rather than clean
protein-substrate ePK evidence.

The roll-up terminal audit
`artifacts/v3_epk_multi_query_active_site_terminal_audit_1025.json` now covers
784 reviewed query placements and 630 unique structures. It records 27
heteromeric topology hits, 3 known positive repeats (`1IR3`, `5HVK`, `6Z3R`),
8 known counterexample repeats, 11 new blocked topology hits, and 0 accepted
new positives. Its status is
`blocked_review_only_mek_erk_role_direction_and_acceptor_state_unresolved`;
same-author-chain/entity-mapping risk covers 15 hits.

Evidence-based confidence call: confidence is higher that these active-query
routes are not yielding a clean broad protein-substrate ePK positive and that
same-author-chain topology needs to stay a hard counter-axis for broad text
queries. Confidence remains low that MEK1/ERK1 can be admitted without
source-authoritative role direction plus phosphoacceptor state. Next useful
experiment: source-review MEK1/ERK1 with explicit residue/phosphosite evidence
or switch to a curated kinase-substrate complex source; do not threshold ePK
or promote a fingerprint from the current query-derived surface.

Wrap-up verification passed with 644 unit tests, `catalytic_earth.cli
validate`, `compileall`, targeted CLI/leakage tests (253 tests),
JSON validation for the new artifacts, artifact migration dry-run/local-file
guard at 108 rows with `removal_allowed=0`, label invariants at 682 total
labels (212 seed fingerprints, 470 out-of-scope, and the three imported
UniProt hard negatives unchanged), and `git diff --check`.

As of the 2026-05-20T05:48:13Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 638 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

`artifacts/v3_epk_midlength_protein_role_counteraxis_audit_1025.json` is the
new review-only counter-axis audit for the relaxed folded-protein role failure.
It blocks the current `7B56` mid-length acceptor false hit with 0 residual
protein-role false hits, then stress-checks the measured source-valid
heteromeric positives `6Z3R`, `8OXM`, and `8OXO`. All three measured positives
are short peptide-mode acceptor chains, so the counter-axis removes a concrete
false hit but still has 0 broad source-valid protein-role retained positives.
The regenerated pre-count and counteraxis artifacts carry this as
`midlength_counteraxis_lacks_broad_source_valid_positive`; pre-count remains
`blocked_review_only`, and counteraxis sufficiency remains
`do_not_select_threshold`.

The same run executed a ligand-specific active-query source experiment instead
of only recording the blocker. RCSB full-text `protein kinase substrate ANP
magnesium` rows 0-99 were scouted in five review-only tranches:
`artifacts/v3_epk_ligand_specific_active_query_candidate_scout_1025.json`
through `artifacts/v3_epk_ligand_specific_active_query_candidate_scout_round5_1025.json`.
All 100 structures fetched. Ninety-six had no source-free heteromeric
gamma-to-acceptor topology hit; `7ZE5`, `2JJ2`, and `4HPU` are source-context
counterexamples; and `1IR3` is already current peptide-substrate support rather
than new broad protein-substrate evidence. Source-validation reviews for the
hit tranches accepted 0 new candidates, so no distance measurement, scorer,
registry, or label gate opened.

Wrap-up verification for this run passed with 642 unit tests,
`catalytic_earth.cli validate`, `compileall`, JSON parsing for the new/updated
ePK artifacts, label invariants at 682 total labels (212 seed fingerprints and
470 out-of-scope labels, with the three imported UniProt hard negatives still
out-of-scope/null-fingerprint), `git diff --check`, and the artifact migration
dry-run/local-file guard at 108 rows with `removal_allowed=0`.

Evidence-based confidence call: confidence is higher that the mid-length rule
is a useful narrow counter-axis for the `7B56` failure and that the first 100
ligand-specific active-query hits do not contain a new broad protein-substrate
support row. Confidence remains low that the current protein-role surface is
general enough for production, because the only measured source-valid additions
are short peptide-mode and threshold/external scored re-audit gates remain
closed. Next useful experiment: source qualitatively new broad
protein-substrate positives outside the exhausted first-100 active-query
surface, or build an acceptor-identity axis that is not just peptide length.

As of the 2026-05-20T05:04:15Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 632 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.
Wrap-up verification passed with 638 unit tests, `validate`, `compileall`,
JSON parsing, label invariants, `git diff --check`, and the artifact migration
dry-run guard at 108 rows with `removal_allowed=0`.

`artifacts/v3_epk_source_free_protein_substrate_role_discriminator_audit_1025.json`
adds a source-free, review-only protein-substrate role discriminator. It
combines the current protein-substrate acceptor positives `1IR3` and `2PHK`
with the `5HVK` heteromeric topology hit, excludes ligand-analog-only
`m_csa:640`, and records 0 current-control false hits plus 0 imported external
hard-negative non-abstentions. The artifact explicitly keeps
`ready_to_run_epk_scorer=false`, `epk_score_computed=false`,
`external_hard_negative_reaudit_scored=false`, and
`countable_label_candidate_count=0`.

`artifacts/v3_epk_source_free_protein_substrate_role_discriminator_stress_audit_1025.json`
then stress-tests the relaxed folded-protein generalization against the current
source-expansion surface. This is a negative result: `1O6K` and `1O6L` remain
peptide-mode rather than protein-mode evidence, there is no broad source-valid
protein-mode positive, and blocked `7B56` false-hits the relaxed protein-role
logic. The regenerated pre-count and counteraxis artifacts carry this as
review-only blocker evidence; `artifacts/v3_epk_precount_gate_status_1025.json`
remains `blocked_review_only`, and
`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` remains
`do_not_select_threshold`.

To avoid stopping at analysis, the run also opened a fourth bounded
external-source scout that excludes the 31 accessions from the first three
UniProt/PDB-backed source passes:
`artifacts/v3_epk_external_protein_substrate_source_scout_fourth_pass_1025.json`.
It found eight new review-only protein-kinase candidates (`O14730`, `O60229`,
`P78368`, `O43353`, `P08922`, `P09769`, `P0C1S8`, and `P14616`) with no query
or entry-fetch failures. They are only `sourced_pending_structure_mapping_review`
rows, and the follow-on mapping/ligand review closes the pass negatively:
`artifacts/v3_epk_external_source_structure_mapping_review_fourth_pass_1025.json`
maps 37 structures, finds 8 direct-position-ready rows but 0 active-state
mapping-ready rows, and
`artifacts/v3_epk_external_source_lower_priority_ligand_sourcing_review_fourth_pass_1025.json`
finds only metal-without-gamma or non-ATP/remote-ligand contexts. The four-pass
terminal decision covers 100 total structure rows and keeps
measurement-ready count at 0, so no distance measurement, scorer, label import,
or registry change is authorized.

Evidence-based confidence call: confidence is higher that the current
protein-substrate role rule is useful as a narrow control-clean discriminator
for known protein-substrate-like positives, but low that it generalizes beyond
the current support. `7B56` is now explicit counterevidence for relaxed
folded-protein substrate identity. The fourth-pass source scout did not rescue
the lane, so the next useful experiment is a ligand-specific active ATP/ANP
plus metal source query for a true broad protein-substrate ePK positive, or a
stronger source-free acceptor-identity counter-axis before any thresholding or
external scored re-audit.

As of the 2026-05-20T03:45:18Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 624 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

`artifacts/v3_epk_general_substrate_identity_gap_audit_1025.json` tests the
obvious next source-free generalization from the peptide-role rule: accept any
polymer hydroxyl chain lacking local nucleotide/metal context opposite a
larger nucleotide/metal-carrying gamma chain, without the short-peptide limit.
That relaxed rule keeps the two source-valid PKB/GSK3 positives (`1O6K` and
`1O6L`) but false-hits the blocked `7B56` CaMKII/autoinhibitory-peptide
context. The new artifact is therefore a negative review-only result:
`relaxed_polymer_identity_status=fails_closed_relaxed_polymer_rule_has_nonpositive_false_hit`,
`general_substrate_identity_ready_count=0`, no ePK score, no threshold, and no
external scored re-audit.

`artifacts/v3_epk_length_band_substrate_identity_counteraxis_audit_1025.json`
adds one concrete counter-axis to that failed rule: the polymer acceptor must
fall in a short peptide-like band or a large folded-substrate band. This
review-only patch keeps `1O6K`/`1O6L`, blocks the relaxed-rule false hit
`7B56`, and has 0 nonpositive length-band false hits on the current
source-expansion subset. It remains source-expansion scoped and not calibrated
for general ePK substrate identity. The paired
`artifacts/v3_epk_length_band_external_hard_negative_review_1025.json` keeps
the three imported external hard negatives (`uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`) at 0 length-band non-abstentions, but
explicitly records that this is not a real scored re-audit or held-out
performance claim.

`artifacts/v3_epk_precount_gate_status_1025.json` and
`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` now carry that
gap audit plus the length-band counter-axis. The pre-count gate remains
`blocked_review_only`, and the counteraxis decision remains
`do_not_select_threshold`; the new length-band row is useful only as bounded
counterexample repair and names source-expansion-only calibration as the
remaining blocker.

`artifacts/v3_epk_sibling_control_homolog_terminal_review_ndk_1025.json`
closes the current NDK homolog recovery queue for this run. `1WKL`, `3Q86`,
`9OAN`, and `9PFY` are all mapping-ready and measured, with the terminal
status
`terminal_review_only_all_homologs_measured_histidine_axis_blocks_threshold`.
This is negative-control histidine-axis evidence only and does not reopen NDK
mapping unless a new source or gate changes.

Evidence-based confidence call: confidence is higher that a simple
polymer-size/local-ligand relaxation is unsafe for ePK substrate identity
because `7B56` is a concrete broad-stress false hit; confidence is moderate
that an acceptor length-band counter-axis is a useful stress-test repair, but
low that it is general enough for production. Production ePK scoring still
needs a source-free protein-substrate role discriminator or qualitatively new
positive source evidence, followed by calibrated controls and a real external
hard-negative scored re-audit.

As of the 2026-05-20T02:43:53Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 624 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

The preregistered broad-stress lanes were executed rather than left as a paper
plan. The current
`artifacts/v3_epk_unified_prototype_broad_stress_audit_1025.json` now covers
110 exact-query entries plus 299 outside-query reviewed candidates. It finds
13 heteromeric topology hits: the two source-valid PKB/GSK3 positives
(`1O6K` and `1O6L`) plus 11 blocked source-context counterexamples (`2JJ2`,
`4HPU`, `7B56`, `7T55`, `7T56`, `7T57`, `7ZDT`, `7ZDU`, `7ZE5`, `9L3M`, and
`9L3U`). The new round found ATP synthase, CaMKII/autoinhibitory-peptide, and
CydC/CydD transporter contexts, all rejected before any threshold or label
claim.

`artifacts/v3_epk_heteromeric_source_expansion_peptide_role_axis_audit_1025.json`
now carries an explicit source-free counterevidence rule for those outside-query
hits. The two positives still pass the short peptide-role axis, while all 11
blocked candidates have machine-readable counterevidence: 11 non-peptide-like
acceptor chains, 9 acceptor chains with local nucleotide/metal context, 5
same-chain acceptor/gamma contexts, and 5 gamma-chain-not-larger contexts. The
downstream substrate-mode, unified identity, unified scorer, pre-count, and
counteraxis artifacts were regenerated; `blocked_review_only` and
`threshold_selection_decision=do_not_select_threshold` remain unchanged.

Evidence-based confidence call: confidence is higher that the current
source-free peptide-role counterevidence separates the PKB/GSK3 positives from
outside-query topology false positives. Confidence remains low for production
ePK scoring because broad stress is still bounded, thresholds are uncalibrated,
the real external hard-negative scored re-audit is closed, and registry/factory
extension remains out of scope.

As of the 2026-05-20T01:43:22Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 617 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

`artifacts/v3_epk_unified_review_only_scoring_prototype_1025.json` is the new
review-only ePK scorer-development artifact. It uses the unified
substrate-identity rule as a gated local axis, carries the 5HVK gamma distance
forward from nested heteromeric topology evidence, gives full diagnostic signal
to eight positive-like rows (`1IR3`, `1O6K`, `1O6L`, `2PHK`, `5HVK`, `6Z3R`,
`8OXM`, and `8OXO`), excludes ligand-analog-only `3TM0`, blocks 44 current
controls and 20 legacy sibling counter-axis rows, and keeps the three imported
external hard negatives at 0 review-only non-abstentions. It deliberately
reports `prototype_gate_status=fail_closed_review_only`; `epk_score_computed`
and real external hard-negative scored re-audit both remain false.

`artifacts/v3_epk_unified_prototype_broad_stress_audit_1025.json` consolidates
the bounded broad-stress result. The exact 110-entry source query is exhausted,
outside-query scouts reviewed 111 candidates with 0 fetch failures and four
heteromeric topology hits, `1O6K`/`1O6L` are source-valid positives, and
`9L3M`/`9L3U` are source-validation counterexamples. The preregistration
artifact
`artifacts/v3_epk_unified_prototype_next_broad_stress_preregistration_1025.json`
freezes three next broad-stress lanes and carries `9L3M`/`9L3U` as blocked
controls before any threshold calibration. `artifacts/v3_epk_precount_gate_status_1025.json`
and `artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` now include
the unified prototype and broad-stress diagnostic rows while preserving overall
`blocked_review_only` and `threshold_selection_decision=do_not_select_threshold`.

Evidence-based confidence call: confidence is high that the unified
review-only prototype is current-control clean because it retains the eight
positive-like rows, blocks current/sibling controls, and abstains on all three
imported external hard negatives. Confidence remains low for production
scoring because broad-stress evidence is bounded and already contains
source-validation counterexamples, thresholds are uncalibrated, the real
external scored re-audit is closed, and registry/factory extension remains
out of scope.

As of the 2026-05-20T00:42:53Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 616 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

`artifacts/v3_epk_unified_substrate_identity_rule_probe_1025.json` executes the
next review-only substrate-identity experiment. The rule unifies the current
short-peptide and protein-substrate ePK review surfaces by requiring a
hydroxyl acceptor on a polymer substrate chain/entity distinct from the local
nucleotide-associated kinase polymer and without local nucleotide/metal
acceptor-chain context. It hits all eight current positive-like review rows:
five peptide-mode rows (`1O6K`, `1O6L`, `6Z3R`, `8OXM`, and `8OXO`), two
text-free protein-substrate rows (`2PHK` and `1IR3`), and the heteromeric 5HVK
lead. Current peptide/protein/sibling controls have 0 false hits, and the
three imported external hard negatives have 0 feature non-abstentions. The
probe explicitly excludes ligand-analog-only `m_csa:640`.

`artifacts/v3_epk_precount_gate_status_1025.json` now includes the unified
substrate-identity rule gate as a passing diagnostic gate while preserving
overall `blocked_review_only`. `artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json`
now carries the unified rule as a current-control pass but keeps
`threshold_selection_decision=do_not_select_threshold` because the rule is not
frozen as a production scorer, broad stress controls are incomplete, external
hard negatives have not been scored by a real calibrated ePK scorer, and the
registry/factory extension remains closed.

Evidence-based confidence call: confidence is medium-high that the unified
substrate-identity rule is the right next review-only axis because it unifies
peptide and protein-substrate modes while clearing current controls and
imported external hard-negative feature probes. Confidence remains low for
production scoring because threshold calibration, broader control stress, a
real external scored re-audit, and label-factory/registry gates are still
missing.

As of the 2026-05-19T23:41:43Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 610 unit tests plus
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

`artifacts/v3_epk_heteromeric_source_expansion_peptide_role_axis_audit_1025.json`
turns the prior outside-query source-expansion leads into a falsifiable
source-free peptide-role audit. The two accepted PKB/GSK3 AMP-PNP peptide
leads (`1O6K` and `1O6L`) pass the role axis; the two broad peptide ATP
nonpositive controls (`9L3M` and `9L3U`) do not. The audit records 2 source-valid
role hits, 0 source-valid misses, 0 nonpositive false hits, and 0 general
substrate-identity-ready rows. It remains review-only: no ePK score, threshold,
external scored re-audit, registry edit, or label import is allowed.

`artifacts/v3_epk_substrate_mode_gap_audit_1025.json` combines the two
outside-query peptide hits with the three earlier heteromeric peptide-mode hits
(`6Z3R`, `8OXM`, `8OXO`) and the three protein-substrate positive-like controls
from the 5HVK lane. Peptide and protein-substrate modes both pass current
controls, with 0 peptide external-hard-negative non-abstentions and 0 protein
external-hard-negative non-abstentions, but unified source-free substrate
identity is still missing. The artifact status is
`passes_review_only_modes_but_unified_substrate_identity_missing`, so it is a
negative result for scorer readiness rather than promotion evidence.

`artifacts/v3_epk_precount_gate_status_1025.json` now includes both new gates:
the source-expansion peptide-role audit and the substrate-mode gap audit pass as
diagnostic review-only gates. Overall status remains `blocked_review_only`.
`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` now carries a
source-expansion peptide-role decision row and still records
`threshold_selection_decision=do_not_select_threshold`.

Evidence-based confidence call: confidence is high that the source-expansion
peptide role axis separates current PKB/GSK3 peptide positives from the
translocase false-positive source controls, and medium that the combined
peptide/protein-substrate mode audit identifies the right next blocker. Confidence
remains low for production scoring because the project still lacks a unified
source-free substrate-identity rule, threshold calibration, a real external
hard-negative scored re-audit, and label-factory/registry gates.

As of the 2026-05-19T22:40:20Z automation run, the ePK lane remains
review-only but gained one new outside-query source lead. Artifact migration
Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and startup checks passed: 606 unit tests and
`catalytic_earth.cli validate` with 682 labels and 8 production fingerprints.

`artifacts/v3_epk_heteromeric_peptide_broader_stress_audit_1025.json`
confirms the exact RCSB ANP/Mg EC 2.7.11.1 same-query stress surface is
exhausted: 110 entries, 0 unreviewed rows, 3/3 peptide-like positive hits,
0 non-peptide substrate-chain positive hits, and 0 nonaccepted or sibling
peptide-rule false hits. This closes the previous "stress-test current
source" item as a negative result; it does not unblock scoring because the
axis is still a narrow peptide-chain rule.

The same run pivoted outside the exhausted source snapshot. ATP/Mg, ADP/Mg,
and AGS/Mg first-25 novel scouts produced 0 heteromeric topology leads. The
all-11 novel AMP-PNP/Mg scout found `1O6K` and `1O6L`; source validation
accepts both as explicit PKB/GSK3 peptide evidence, and the distance sample
measures nearest gamma-acceptor distances at 3.542-3.566 Angstrom. The AMP-PNP
control rerun remains fail-closed: the new positive-like pair is
source-authority dependent, source-free axis complete count is 0, thresholds
are uncalibrated, and no external scored re-audit exists.

The broad "kinase substrate peptide ATP/Mg" first-25 source expansion scout
found two topology hits (`9L3M` and `9L3U`), but source validation blocked both
as outer mitochondrial transmembrane helix translocase contexts. This is a
useful negative: broad text-query lanes can surface local ATP/gamma geometry
that is not ePK substrate evidence, so every outside-query tranche needs a
source-validation screen before any role-axis or scorer work.

Confidence call: high confidence that safety invariants and migration rails
remain intact; high confidence the exact ANP/Mg same-query source is exhausted
for the current reviewed snapshot; moderate confidence `1O6K`/`1O6L` are useful
review-only PKB/GSK3 source leads because the title/raw CIF context is
explicit. Next best experiment: use these leads to design a source-free
peptide/protein-substrate role axis that can fail against the current sibling
and external hard-negative controls.

As of the 2026-05-19T21:38:11Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved. Startup checks passed: 601 unit tests and `catalytic_earth.cli
validate`.

The NDK homolog mapping queue was already complete at run start:
`artifacts/v3_epk_sibling_control_homolog_mapping_review_ndk_1025.json` has
4/4 measurement-ready structures for `1WKL`, `3Q86`, `9OAN`, and `9PFY`, and
`artifacts/v3_epk_sibling_control_homolog_gamma_distance_sample_ndk_1025.json`
measures all four with nearest histidine distances of 2.899-3.339 Angstrom and
same-chain hydroxyl distances of 3.487-5.240 Angstrom. No NDK repair or
reopening was needed.

`artifacts/v3_epk_heteromeric_peptide_acceptor_identity_probe_1025.json` adds
the requested non-generic local acceptor-identity signal. The rule requires the
candidate hydroxyl to sit on a short peptide-like polymer chain without local
nucleotide/metal ligand context while the gamma-associated polymer chain is
larger. It hits all three retained heteromeric source-valid role candidates
(`6Z3R`, `8OXM`, and `8OXO`), blocks the three nonaccepted heteromeric controls,
and blocks all 11 measured sibling same-chain hydroxyl controls with 0 false
hits. It is deliberately narrow and review-only: source-free ready count is 3,
but it is not a general ePK substrate-identity rule, not a calibrated score,
and not label evidence.

`artifacts/v3_epk_heteromeric_peptide_external_hard_negative_probe_1025.json`
then screens the three imported external hard negatives against that narrow
peptide identity axis using their existing structural sidecars. All three
(`uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`) abstain because the
sidecars have no gamma-nucleotide context; non-abstentions are 0, missing
external rows are 0, and coordinate-unavailable rows are 0. This is still a
diagnostic feature probe, not the real scored external hard-negative re-audit.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with both
new peptide-identity artifacts. Overall status remains `blocked_review_only`.
The new peptide acceptor identity and peptide external-hard-negative gates
pass as diagnostics, but acceptor-threshold calibration, the real external
hard-negative scored re-audit, registry/label-factory extension,
text-free/protein-substrate acceptor production admissibility, source-free
chain topology, the three active-state repair scans, and the gamma negative
control distribution remain failing gates.

`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` was regenerated
against that pre-count state. It now records a peptide-acceptor decision row:
the feature passes current controls and the external feature probe, but stays
not production-admissible because the peptide axis is narrow and does not
replace a general substrate-identity rule. Threshold selection remains
`do_not_select_threshold`.

Evidence-based confidence call: confidence is now medium that short
peptide-like acceptor-chain context is a useful local axis for the current
heteromeric ePK review surface because it clears retained positives,
nonaccepted heteromeric controls, sibling controls, and imported external
hard-negative feature probes. Confidence remains low for production scoring
because the axis is narrow, thresholding is uncalibrated, and no real external
hard-negative scored re-audit or label-factory extension exists.

As of the 2026-05-19T20:36:50Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

`artifacts/v3_epk_heteromeric_broader_counteraxis_control_audit_1025.json`
extends the acceptor-chain nucleotide/metal counter-axis from the six reviewed
heteromeric hits to the full bounded 50-structure heteromeric scout plus
measured sibling controls from NDK, ATP-grasp, PfkA, and PfkB. It keeps the
three source-valid heteromeric leads (`6Z3R`, `8OXM`, and `8OXO`), blocks the
three nonaccepted heteromeric hits (`7M0T`, `7M0W`, and `8ZN6`), and blocks
11/11 measured sibling same-chain hydroxyl hits with 0 sibling residual false
hits. It remains `passes_broader_review_controls_not_scoring_admissible`.

`artifacts/v3_epk_heteromeric_ligand_asymmetry_role_audit_1025.json` then
promotes the counter-axis into an explicit source-free role-direction probe:
gamma-associated ligand-bearing chains can be separated from candidate
acceptor chains on the current retained heteromeric review positives. It
retains 3 source-valid role hits, has 0 nonaccepted role hits and 0 sibling
role-asymmetry false hits, but still marks production scoring blocked because
source-free acceptor identity is absent.

`artifacts/v3_epk_heteromeric_acceptor_identity_gap_audit_1025.json` records
that next blocker as a negative result. The three retained heteromeric role
hits have source-context Ser acceptor candidates, but 0 have a source-free
acceptor-identity feature. The next useful ePK experiment is therefore a
source-free acceptor-identity rule on those retained heteromeric role hits,
with BRAF/MEK nonaccepted hits and sibling-family controls included from the
start. Do not move to threshold calibration, real external hard-negative scored
re-audit, registry extension, or label import until that local identity axis
exists and passes.

`artifacts/v3_epk_heteromeric_acceptor_identity_rule_probe_1025.json` executes
that weakest plausible source-free identity rule by checking generic
Ser/Thr/Tyr hydroxyl residue class after the role-asymmetry and counter-axis
filters. It hits all three retained role candidates; the three nonaccepted
heteromeric hits and 11 sibling same-chain hydroxyl hits are blocked before the
identity rule, leaving 0 residual nonaccepted or sibling identity-rule false
hits on the current controls. It stays review-only and explicitly weak:
generic hydroxyl class is not substrate identity,
`source_free_acceptor_identity_ready_count` remains 0, and no ePK score,
external scored re-audit, registry edit, or label import is allowed.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the
broader counter-axis, ligand-asymmetry role audit, acceptor-identity gap audit,
and generic acceptor-identity rule probe. Overall status remains
`blocked_review_only`; these artifacts remove a bounded role-direction
ambiguity and show the generic identity rule is insufficient, but they do not
satisfy source-free acceptor identity, threshold calibration, external scored
re-audit, registry extension, or label import gates.

Evidence-based confidence call: confidence is higher that local ligand-context
asymmetry is a useful heteromeric ePK role-direction signal, because it clears
the current broader heteromeric/sibling review controls. Confidence remains low
for production scoring because the retained role hits still rely on
source-context acceptor identity plus only a generic hydroxyl-class proxy, and
no calibrated ePK score or real external hard-negative scored re-audit exists.

As of the 2026-05-19T19:34:43Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/ls-remote/dry-run
push hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

`artifacts/v3_epk_heteromeric_source_valid_control_rerun_1025.json` now reruns
the fail-closed ePK review surface with the three measured source-valid
heteromeric leads from the prior run. It carries the existing three current ePK
positive-like rows plus source-valid 5HVK, adds `6Z3R`, `8OXM`, and `8OXO` as
new source-valid heteromeric review positives, and explicitly separates
ambiguous `7M0T`/`7M0W` plus rejected `8ZN6`. The review surface now has seven
positive-like rows, 20 sibling controls with 0 false hits, and three imported
external hard negatives with 0 non-abstentions. It remains
`passes_review_only_controls_but_scorer_blocked`, with no calibrated score,
external scored re-audit, registry edit, or label import.

`artifacts/v3_epk_heteromeric_text_free_axis_gap_audit_1025.json` makes the
next blocker explicit. All four source-authority-dependent positive-like rows
(5HVK plus the three new heteromeric leads) have local geometry axes present,
but 0 have source-free role assignment, 0 have source-free acceptor identity,
and 0 are production-admissible positive rows. This is a blocker inventory only.

`artifacts/v3_epk_heteromeric_source_free_role_rule_probe_1025.json` then tests
the obvious local rule directly: heteromeric entity topology plus gamma-distance
within the 6 Angstrom candidate cutoff. It fails closed because the rule hits
all six reviewed heteromeric candidates, including the three nonaccepted rows
(`7M0T`, `7M0W`, and `8ZN6`). The next useful ePK experiment is therefore a
source-free role-direction disambiguation signal beyond topology plus gamma
distance, not threshold calibration.

`artifacts/v3_epk_heteromeric_acceptor_chain_counteraxis_audit_1025.json` adds
that first local counter-axis. It blocks a topology/gamma hit when the candidate
acceptor chain itself carries nucleotide or metal ligand context. On the
current six reviewed heteromeric candidates it retains the three source-valid
review positives, blocks the three nonaccepted hits (`7M0T`, `7M0W`, `8ZN6`),
loses 0 accepted rows, and leaves 0 residual nonaccepted hits. This is still
review-only: broader heteromeric/sibling controls, threshold calibration, and a
real external hard-negative scored re-audit are not run.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the new
control rerun, text-free gap audit, source-free rule probe, and acceptor-chain
counter-axis. Overall status remains `blocked_review_only`; the new diagnostics
are review-only and do not satisfy production scoring, external hard-negative
scored re-audit, registry extension, or label import.

CLI regression coverage now exercises the four new heteromeric follow-on
commands with local fixture inputs, including the pass/fail transitions from
source-valid control rerun through source-free false-hit probe and
acceptor-chain counter-axis, and the pre-count CLI test now loads the same
four artifact types into the consolidated gate.

Evidence-based confidence call: confidence is higher that heteromeric
protein-substrate geometry can provide useful ePK review controls, because the
expanded surface keeps sibling and imported external hard-negative diagnostics
clean. Confidence remains low for production scoring because topology plus
gamma distance false-hits ambiguous/rejected heteromeric rows, and every
expanded positive-like row still needs broader text-free controls before it can
become a scorer input.

As of the 2026-05-19T17:33:55Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/dry-run push
hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

`artifacts/v3_epk_source_free_chain_topology_role_audit_1025.json` now
stress-tests the local chain-topology replacement with source fields masked.
The rule hits four ligand-specific co-complex probe structures: source-valid
5HVK plus same-accession phosphosite/control-risk structures `3Q4Z`, `4I94`,
and `5XD6`. This deliberately fails closed as
`blocked_review_only_source_free_topology_role_rule_false_hit_risk`; the
`source_free_chain_topology_role_audit` pre-count gate remains failing and no
score, registry edit, label import, or held-out claim is opened.

`artifacts/v3_epk_heteromeric_chain_topology_signal_audit_1025.json` adds the
next counter-axis. It compares each candidate acceptor polymer entity with the
nearest adenylate gamma atom's associated author-chain polymer entity. On the
current hit controls it keeps 5HVK as the sole positive-like heteromeric
signal, abstains on `3Q4Z`, `4I94`, and `5XD6`, and records zero same-accession
false hits. Its full source-free scan across the 60-structure ligand-specific
probe finds only 5HVK as a heteromeric candidate, so the positive-coverage gap
is now explicit rather than an untested assumption. This makes the new
`heteromeric_chain_topology_signal_audit` gate pass as review-only
counterevidence, but the signal is still not production admissible because it
has only one positive-like case and still lacks threshold calibration, a real
external hard-negative scored re-audit, and registry/label factory extensions.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with both
topology audits. Overall status remains `blocked_review_only`; the failing
gate set still includes acceptor threshold calibration, external scored
hard-negative re-audit, registry/label-factory extension, text-free acceptor
feature gap, protein-substrate acceptor candidate audit, source-free topology
role audit, `m_csa:760`, `m_csa:757`, `m_csa:756`, and gamma negative-control
distance distribution.

Evidence-based confidence call: confidence is higher that a purely local
entity-topology counter-axis can remove the specific 5HVK chain-role source
dependency without false-hitting the three current same-accession controls.
Confidence remains low that this can support production scoring: one
positive-like heteromeric case from a 60-structure scan is not enough for
calibration, and the real external hard-negative scored re-audit plus
registry/factory extensions remain absent.

As of the 2026-05-19T16:32:17Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/dry-run push
hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

The queued 5HVK prototype/control rerun is now complete.
`artifacts/v3_epk_ligand_specific_5hvk_prototype_control_rerun_1025.json`
adds source-valid 5HVK to the review-only prototype surface while preserving
the fail-closed controls: four positive-like review rows, 20 sibling controls
still blocked, three imported external hard negatives still abstained, and
`epk_score_computed=false`. This is not a real scored ePK re-audit and makes
no held-out performance claim.

`artifacts/v3_epk_5hvk_protein_substrate_axis_generalization_audit_1025.json`
then records the useful consequence: the protein-substrate-only axis now has
three review-only positive-like rows (`m_csa:35`, `m_csa:246`, and
source-valid 5HVK) without relying on ligand-analog-only `m_csa:640`. That
reduces the ligand-analog dependency for scorer development, but the axis remains
not production-admissible because threshold calibration, a frozen real scorer,
external scored re-audit, registry extension, and label-factory extension are
still missing.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with both
new 5HVK artifacts. The new `ligand_specific_5hvk_prototype_control_rerun`
and `ligand_specific_5hvk_protein_substrate_axis_generalization` gates pass as
diagnostic gates, while the overall status remains `blocked_review_only`.

The run continued into that next diagnostic step.
`artifacts/v3_epk_protein_substrate_scorer_design_freeze_1025.json` freezes a
review-only protein-substrate scorer design and explicitly marks
source-authority axes as invalid for orphan-discovery claims. The matching
`artifacts/v3_epk_protein_substrate_calibration_diagnostic_1025.json` gives a
useful narrow result: three protein-substrate positive-like rows score as
full-axis diagnostics, ligand-analog `m_csa:640` is excluded from calibration
positives, and sibling/external controls stay at zero. It still sets
`epk_score_computed=false`.

`artifacts/v3_epk_source_authority_axis_replacement_gap_audit_1025.json`
captures the remaining production blocker: source-authority acceptor identity
and catalytic context still need local replacements. The first replacement
attempt,
`artifacts/v3_epk_local_chain_topology_acceptor_replacement_rule_1025.json`,
passes current review controls with three positive hits, zero control false
hits, and zero imported external non-abstentions, but it still relies on
source-assigned 5HVK kinase/substrate chain roles.
`artifacts/v3_epk_5hvk_local_polymer_entity_role_audit_1025.json` tests that
blocker directly: local PDB polymer/entity evidence supports a 5HVK co-complex
with disjoint kinase/acceptor chains plus ANP/Mg context, but still cannot
assign kinase versus substrate roles without source authority. The next useful
experiment is a source-free local polymer topology role rule plus broader
chain-topology controls, not registry editing.

Evidence-based confidence call: confidence is higher that a protein-substrate
acceptor axis can be developed without using ligand-analog `m_csa:640` as the
third positive. Confidence remains low that the current evidence can support
production scoring, because the best local replacement rule still uses
source-assigned 5HVK chain roles; the local polymer/entity audit only narrows,
not removes, that dependency. No selected threshold or real external
hard-negative scored re-audit exists.

As of the 2026-05-19T15:31:41Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/dry-run push
hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

The bounded 5HVK source-validity check is now complete.
`artifacts/v3_epk_ligand_specific_5hvk_source_validity_review_1025.json`
accepts 5HVK as source-valid LIMK1/cofilin review evidence: P53667 and P23528
both map through `struct_ref_seq`, the 5HVK title/keywords support the
kinase-substrate co-complex, UniProt P53667 carries ATP-dependent protein
Ser/Thr kinase evidence, UniProt P23528 carries Ser3 phosphoserine evidence,
and P23528 Ser3 OG is 4.236 Angstrom from ANP PG. This produces exactly one
measurement-ready review lead and authorizes rerunning ePK sibling controls and
the imported external hard-negative controls with 5HVK included. It does not
score ePK, select a threshold, import labels, edit registries, or make a
held-out performance claim.

`artifacts/v3_epk_ligand_specific_5hvk_control_rerun_queue_1025.json` turns
that accepted lead into a concrete review-only next-experiment queue. It
records the existing prototype/control surface as 3 current positives, 20
sibling controls, and 3 imported external hard negatives; it marks the 5HVK
candidate-addition, sibling-control rerun, and imported external diagnostic
rerun tasks as ready in review-only mode. It also keeps
`not_a_real_scored_reaudit=true`, `ready_to_run_epk_scorer=false`,
`epk_score_computed=false`, and `countable_label_candidate_count=0`.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the
5HVK source-validity artifact and control-rerun queue. The new
`ligand_specific_5hvk_source_validity_review` and
`ligand_specific_5hvk_control_rerun_queue` gates pass as diagnostic gates, but
the overall pre-count status remains `blocked_review_only`; the failing gates
still include acceptor threshold calibration, external scored re-audit,
registry/label-factory extension, text-free acceptor admissibility,
protein-substrate acceptor coverage, the exhausted `m_csa:760`/`m_csa:757`/
`m_csa:756` source-repair gates, and the negative-control distribution blocker.
The next useful experiment is not another broad source scout: rerun the
review-only prototype/control surface with source-valid 5HVK as a candidate
positive lead using the new queue, while keeping the real scorer and registry
changes closed.

Evidence-based confidence call: confidence is higher that ligand-specific
substrate/co-complex querying can produce source-valid ePK positive leads.
Confidence remains low that the current evidence can support production
scoring, because the scorer has not been rerun with 5HVK, thresholds are still
uncalibrated against controls, and the imported external hard negatives have
not received a real scored re-audit.

As of the 2026-05-19T14:30:37Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/dry-run push
hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

The run closed the pending `Q8IVT5` alternate-co-complex branch as a negative
result. `artifacts/v3_epk_external_source_q8ivt5_alternate_cocomplex_review_1025.json`
maps exact P29678/Q02750 source phospho-acceptor residues where present, but
Ser218/Ser222 stay outside the 6 Angstrom review threshold (best exact-source
distance 9.061 Angstrom), while active-state structures without source-mapped
acceptors remain blocked. `artifacts/v3_epk_external_source_lower_priority_ligand_sourcing_review_1025.json`
also keeps the first-pass mapped-but-ligand-incomplete rows not-ready.

The run then tried two more broad reviewed-UniProt/PDB-backed source passes
instead of repeating audits. `artifacts/v3_epk_external_protein_substrate_source_scout_second_pass_1025.json`
and `artifacts/v3_epk_external_protein_substrate_source_scout_third_pass_1025.json`
source 16 additional non-countable candidates. Their structure-mapping and
ligand-sourcing reviews add 47 reviewed structures, but 0 active-state
measurement-ready positives. `artifacts/v3_epk_external_source_three_pass_terminal_decision_1025.json`
adjudicates the combined broad scout surface: 24 sourced candidates, 63
reviewed structure rows, 5 active-state mapped rows from the original Q8IVT5
surface, 0 source-mapped acceptors, and 0 measurement-ready positives. Do not
repeat the same broad UniProt/PDB-backed ePK source scout without a new query
axis.

The productive new route is ligand-specific active-state sourcing.
`artifacts/v3_epk_ligand_specific_active_state_source_scout_1025.json` queries
RCSB for ANP/Mg EC 2.7.11.1 structures and finds 11 review-only source rows.
`artifacts/v3_epk_ligand_specific_active_state_structure_mapping_review_1025.json`
finds one active-state mapped lead, `P53355`/`1JKK`, but the acceptor audit
finds no acceptor-like hydroxyl within threshold. `artifacts/v3_epk_ligand_specific_p53355_substrate_cocomplex_review_1025.json`
scans 78 P53355 PDB crossrefs and shows active-state kinase structures and
mapped source phospho-acceptor structures are split, so P53355 is not
measurement-ready. `artifacts/v3_epk_ligand_specific_active_state_terminal_decision_1025.json`
keeps that surface blocked.

The most useful next science item is now the bounded substrate/co-complex probe,
not another broad source scout. `artifacts/v3_epk_ligand_specific_substrate_cocomplex_query_probe_1025.json`
screens the first 60 RCSB ANP/Mg EC 2.7.11.1 entries. It finds 42
source-ready structures, 4 within-threshold phosphoacceptor-hit structures,
and one cross-accession review lead: `5HVK`, with source-ready `P53667`
(`LIMK1_HUMAN`) and `P23528` (`COF1_HUMAN`) Ser3 near gamma at 4.236
Angstrom. This is not measurement-ready yet: manual source review must confirm
that the acceptor is valid protein-substrate evidence for the source kinase
and not merely an annotation/co-complex coincidence.
`artifacts/v3_epk_ligand_specific_5hvk_review_priority_1025.json` packages
that single lead for the next source-validity check. Keep scoring, thresholds,
registry edits, label import, and external hard-negative scored re-audit closed
until that review passes and controls are rerun.

Evidence-based confidence call: confidence is higher that a ligand-specific
active-state/substrate co-complex query can produce falsifiable ePK positive
leads. Confidence remains low that the current evidence can support production
scoring, because every reviewed source lane still lacks a validated
source-mapped protein-substrate acceptor under a calibrated scorer.

Verification in this run: startup full unit discovery reported 544 tests
passing; final full unit discovery reported 560 tests passing; `validate`
preserved 682 labels and 8 fingerprints; artifact migration dry-run/local-file
guard passed with 108 rows and `removal_allowed=0`; external label invariants
remained 682 total, 212 seed, 470 out-of-scope, and the three imported
external hard negatives stayed out-of-scope with null fingerprints.

As of the 2026-05-19T13:29:09Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/dry-run push
hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

The run opened the first external ePK positive-source branch after current
M-CSA source repair failed closed. `artifacts/v3_epk_external_protein_substrate_source_scout_1025.json`
uses reviewed PDB-backed UniProt protein-kinase lanes as source-triage context
only. It finds eight non-countable source rows with explicit active-site,
ATP-binding, and protein-phosphotransfer evidence; one additional row is
blocked by missing active-site/ATP-binding source features. The artifact
preserves the three imported external hard negatives as existing labels,
keeps all rows non-countable, and leaves mapping, acceptor evidence,
threshold calibration, external hard-negative re-audit, registry extension,
and label-factory extension blocked.

`artifacts/v3_epk_external_source_structure_mapping_review_1025.json` then
tries direct UniProt-position plus struct-ref-seq mapping for the top sourced
rows. Nine structures now map source positions conservatively. Five `Q8IVT5`
structures, `7JUW`, `7JUX`, `7JUY`, `7JV0`, and `7JV1`, map the source
active-site/ATP-binding positions on a single chain with local ANP/Mg context;
four additional mapped structures lack usable local gamma/metal context. Seven
reviewed structure rows still fail closed because direct position mapping is
missing or ambiguous. The active-state mapped rows are useful source-repair
leads, but none has source-mapped protein-substrate acceptor evidence, so
measurement readiness remains 0 and no score, external held-out claim, registry
edit, or label import is open.

`artifacts/v3_epk_external_source_acceptor_gap_audit_1025.json` checks the
remaining acceptor blocker for those active-state mapped structures. `7JUW`,
`7JUY`, and `7JV0` have a non-catalytic-chain Ser hydroxyl within 6 Angstrom of
ANP PG, while `7JUX` and `7JV1` have no within-threshold non-catalytic-chain
hydroxyl. None of those hydroxyls is source-mapped as the protein-substrate
acceptor, so the lead remains not measurement-ready and fail-closed.

`artifacts/v3_epk_external_source_next_experiment_queue_1025.json` ranks that
negative result into the next bounded experiments. The highest-value follow-up
is source-mapping the three within-threshold unsourced Ser acceptor-like
residues. If that fails, the lane should source an alternate active-state
substrate co-complex for the outside-threshold rows, then only after that
continue the mapped-but-ligand-incomplete accessions. All 16 rows stay
review-only, unscored, non-countable, and blocked from import.

`artifacts/v3_epk_external_source_acceptor_source_mapping_review_1025.json`
executes the top source-mapping experiment and fails closed. All five
active-state `Q8IVT5` candidates map to MEK1 `P29678` Ser194, but the source
phosphoserine evidence is Ser218/Ser222, not Ser194. Those nearby geometry hits
are terminally not source-mapped protein-substrate acceptors, so measurement
readiness remains 0.

Evidence-based confidence call: confidence is higher that external reviewed
kinase source evidence can produce concrete ePK structure-mapping leads.
Confidence remains low that the current lane can support production scoring
because the new active-state `Q8IVT5` leads still lack mapped
protein-substrate acceptors, and the existing threshold/external re-audit
blockers remain unchanged. The next bounded experiment should source alternate
active-state substrate co-complex evidence for `Q8IVT5`, then continue
lower-priority mapped accessions only if that fails.

Verification in this run: startup full unit discovery reported 537 tests
passing; final full unit discovery reported 544 tests passing; `validate`
preserved 682 labels and 8 fingerprints; artifact migration dry-run/local-file
guard passed with 108 rows and `removal_allowed=0`; external label invariants
remained 682 total, 212 seed, 470 out-of-scope, and the three imported
external hard negatives stayed out-of-scope with null fingerprints.

As of the 2026-05-19T12:28:13Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Artifact
migration Phase 1 stayed guard-only and closed; no Phase 2/3 upload, deletion,
externalization, Git LFS change, history rewrite, registry edit, label import,
or `removal_allowed=true` occurred. SSH deploy-key fetch/pull/dry-run push
hygiene passed at startup, and the 682-label / 8-fingerprint baseline was
preserved.

The run converted the analog/product-state policy question into three
fail-closed review-only artifacts. `artifacts/v3_epk_analog_product_state_policy_activation_audit_1025.json`
confirms the preregistered policy cannot activate: seven blockers remain,
including inactive policy status, ligand-analog dependency on `m_csa:640`, 0
production-admissible analog rows, 0 measurement-ready source-repair
candidates, no calibrated ePK score, no real scored external hard-negative
re-audit, and no registry/label-factory extension. `artifacts/v3_epk_analog_product_state_policy_control_reaudit_1025.json`
then tests a narrower inactive active-gamma ligand-analog policy variant. It
covers 3/3 current positives, including ligand-analog-only `m_csa:640`, while
keeping 25 sibling controls at 0 false hits and the three imported external
hard negatives at 0 feature non-abstentions. It still cannot activate because
the policy was not frozen before candidate selection and external hard
negatives were not scored by a real ePK scorer. `artifacts/v3_epk_review_only_external_hard_negative_score_probe_1025.json`
makes the prototype probe explicit: all three imported external hard negatives
have review-only prototype score 0.0 and 0 policy-feature hits, but
`external_hard_negative_reaudit_scored` remains false, so this is not clean
held-out evidence.

The run also closes the specific `5LI1` follow-up clue without reopening broad
`m_csa:756` repair. `artifacts/v3_epk_m_csa756_5li1_residue_evidence_audit_1025.json`
resolves chain-A Lys380/Asp382/Asn383 near ANP/Mg and preserves
structure-level SEP/TPO/PTR-like context. It records a noncanonical `PB` atom,
but no canonical terminal `PG`; the noncanonical atom is policy-inadmissible,
5LI1 residue positions are not source-authoritative, and no protein-substrate
acceptor is mapped. The row remains measurement-not-ready, non-countable, and
review-only.

The 1025 preview/expanded source-triage checks
(`artifacts/v3_epk_protein_substrate_positive_source_triage_1025_preview.json`
and `artifacts/v3_epk_protein_substrate_positive_source_triage_expanded_1025.json`)
did not expose a new protein-substrate ePK source beyond the already-exhausted
`m_csa:760`, `m_csa:757`, and `m_csa:756` candidates. Treat them as negative
queue evidence, not a new label-scaling tranche. The matching expanded terminal
decision (`artifacts/v3_epk_protein_substrate_source_repair_terminal_decision_expanded_1025.json`)
also remains `current_source_candidates_exhausted_review_only` with 0
measurement-ready candidates.

`artifacts/v3_epk_precount_gate_status_1025.json` now consolidates the policy
activation audit, policy control re-audit, score probe, and 5LI1 residue audit
as passed diagnostic review-only gates while keeping the lane blocked. The
remaining failing gates are threshold calibration, real external hard-negative
scored re-audit, registry/label-factory extension, text-free acceptor feature
gap, protein-substrate-only acceptor coverage, the three source-repair scans
for `m_csa:760`/`m_csa:757`/`m_csa:756`, and gamma negative-control distance
distribution. `artifacts/v3_epk_protein_substrate_positive_source_triage_expanded_1025.json`
checks the new-source path with a larger review-only cap and still finds only
the same three exhausted source candidates with 0 measurement-ready rows. The
expanded terminal decision remains closed as a negative result. The
next useful science step is not another repeat of the same source-repair scans;
it should either bring in genuinely new ePK source evidence from outside the
current queue or turn the current review-only probe into a real scored re-audit
only after threshold calibration and policy-freeze requirements are satisfied.

Evidence-based confidence call: confidence is higher that current analog and
5LI1 evidence is useful as design feedback but not admissible for a production
ePK fingerprint. Confidence remains low that the ePK scorer can safely expand
without a new protein-substrate positive or a calibrated, pre-frozen analog
policy because the hard blockers are now explicit and tested.

Verification in this run: full unit discovery reports 537 tests passing;
`validate` preserved 682 labels and 8 fingerprints; artifact migration
local-file guard passed with 108 rows, 0 blockers, and `removal_allowed=0`;
external label invariants stayed at 682 total, 212 seed-fingerprint, 470
out-of-scope, and exactly three imported external out-of-scope labels;
compileall, JSON loading for the new ePK artifacts, and `git diff --check`
passed.

As of the 2026-05-19T11:53:08Z automation run, the ePK lane remains
review-only and blocked from production fingerprint expansion. Startup found a
stale automation lock and coherent dirty work from the previous run; that work
was tested, committed, and pushed first as
`59c7634 Add ePK protein-substrate source repair audits`. SSH deploy-key
fetch/push hygiene passed, full unit discovery passed before recovery commit
with 524 tests, and `validate` preserved the 682-label / 8-fingerprint
baseline. Artifact migration Phase 1 stayed guard-only; no Phase 2/3 upload,
removal, Git LFS change, history rewrite, registry edit, label import, or
`removal_allowed=true` occurred.

The new science work consumed the current protein-substrate source-repair
ladder and failed it closed. `artifacts/v3_epk_m_csa757_active_state_repair_scan_1025.json`
scans the first 25 `m_csa:757` alternates. It finds two active-state leads:
`1CDK` has ANP/Mn context but only through an ambiguous homomeric chain choice,
and `1Q24` has conservative ATP/Mg context plus structure-level SEP/TPO. Neither
maps a protein-substrate acceptor chain, so the scan has 0 measurement-ready
candidates and remains non-countable. `artifacts/v3_epk_m_csa756_active_state_repair_scan_1025.json`
then scans all 15 `m_csa:756` alternates. `5LI1` has structure-level
ANP/Mg/SEP/TPO, while `5LIH` and `9EJM` are ADP/Mg or product-state leads, but
none has conservative active-site remapping plus active-state acceptor geometry.

`artifacts/v3_epk_protein_substrate_source_repair_terminal_decision_1025.json`
closes the current bounded source-repair loop as negative review-only evidence:
`m_csa:760`, `m_csa:757`, and `m_csa:756` have 0 measurement-ready candidates
in aggregate. `artifacts/v3_epk_precount_gate_status_1025.json` now includes
failing `m_csa757_active_state_repair_scan` and
`m_csa756_active_state_repair_scan` gates in addition to the `m_csa:760`
split-state blocker. The next experiment should not repeat those scans without
new evidence; use either a genuinely new protein-substrate ePK source or a
pre-registered ligand-analog/product-state admissibility policy before scorer
calibration.
`artifacts/v3_epk_analog_product_state_policy_preregistration_1025.json` drafts
that policy as inactive review-only scaffolding: homomeric chain choices and
product-state ADP-without-gamma evidence are excluded as predictive support,
and activation requires a frozen rule, sibling-family controls, and a scored
external hard-negative re-audit.

One small follow-on clue is worth preserving but is not yet an artifact:
`5LI1` has ANP/Mg on chain A and local kinase residues near the ligand
(including Asp 382, Asn 383, and Lys 380), while the committed remap remains
non-conservative from selected `1ZRZ` residue positions. If source repair is
reopened, the next bounded experiment should be explicit residue-position
evidence for `5LI1`, not another broad scan of `m_csa:756`.

Evidence-based confidence call: confidence is now higher that the current ePK
source candidates are exhausted rather than merely under-audited. Confidence
remains low that a production ePK scorer can be calibrated from the current
positive set because the only clean protein-substrate acceptor feature still
misses `m_csa:640`, and every current source-repair pivot lacks a measurable
combined ATP/Mg plus mapped protein-substrate acceptor geometry.

Final verification in this run: targeted CLI/leakage tests for the
`m_csa:757`, `m_csa:756`, terminal-decision, analog-policy, and pre-count
status paths passed; full unit discovery reports 529 tests passing; `validate`
preserved 682 labels and 8 fingerprints; the artifact migration local-file
guard passed with 108 rows and `removal_allowed=0`; compileall, JSON
validation, external-label invariant inspection, and `git diff --check` passed.

As of the 2026-05-19T03:58:32Z automation run, the ePK lane remains
review-only and scientifically blocked from production fingerprint expansion.
Startup protocol passed: the repo lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key fetch/push hygiene
passed, the 516-test unit discovery passed, and `validate` preserved the 682
label / 8 fingerprint baseline. Artifact migration Phase 1 stayed guard-only;
no Phase 2/3 upload, deletion, Git LFS change, history rewrite, registry edit,
or label import was performed.

The run tightened the ePK acceptor story with three new review-only artifacts.
`artifacts/v3_epk_protein_substrate_acceptor_candidate_audit_1025.json` strips
ligand-analog rescue from the chain/ligand acceptor feature. It keeps 2/3
current positives, blocks all 25 negative-control rows with 0 false hits, and
abstains on all three imported external hard negatives, but misses
`m_csa:640`; this makes the positive-coverage blocker explicit.
`artifacts/v3_epk_ligand_analog_policy_blocker_decision_1025.json` records the
policy decision that ligand-analog acceptor evidence is not
production-admissible for `m_csa:640` without a future pre-registered analog
policy and scored external re-audit.

The source-repair path also advanced and failed closed. `artifacts/v3_epk_protein_substrate_positive_source_triage_1025.json`
identifies three additional non-countable ePK-family source rows:
`m_csa:756`, `m_csa:757`, and `m_csa:760`, with `m_csa:760` first because its
selected structure has ADP/Mg product-state context. `artifacts/v3_epk_m_csa760_atp_state_repair_scan_1025.json`
then scans the known `m_csa:760` alternate structures: `1TID` and `1TIL` have
ATP/Mg catalytic context, while `1TH8` and `1THN` have protein-substrate
product-state context, but no single structure combines ATP/Mg with the
protein-substrate acceptor. The row is split-state blocked with 0
measurement-ready candidates.

A bounded follow-on inventory screen should guide the next run but is not a
label, score, or held-out claim: among the first 25 `m_csa:757` candidate
structures, `1CDK` has ANP/Mn/TPO and `1Q24` has ATP/Mg/SEP/TPO context; among
the 15 `m_csa:756` candidates, `5LI1` has ANP/Mg/SEP/TPO, `5LIH` has ADP/Mn,
and `9EJM` has ADP/Mg. `m_csa:757` is the next best bounded source-repair
target because it has protein-substrate review context plus ATP/Mg alternate
leads.

`artifacts/v3_epk_precount_gate_status_1025.json` now includes the
`m_csa760_atp_state_repair_scan` gate. The lane remains
`blocked_review_only`; failing gates are acceptor threshold calibration,
external hard-negative scored re-audit, registry/label-factory extension,
text-free acceptor production admissibility, protein-substrate positive
coverage, `m_csa:760` split-state repair, and gamma negative-control
distribution readiness.

Evidence-based confidence call: confidence increased that the current
protein-substrate acceptor axis is scientifically useful because it has 0
control false hits and 0 external hard-negative non-abstentions, but confidence
is low that current positives are enough for production ePK scoring. Both
`m_csa:640` and `m_csa:760` now fail for evidence-policy reasons rather than
implementation gaps. The next bounded science step should pivot to another
protein-substrate ePK source (`m_csa:757`, then `m_csa:756`) or pre-register a
strict analog/product-state policy before any score, registry change, label
import, or external hard-negative performance claim.

Verification so far in this run: targeted CLI/leakage tests for the new
builders passed, and full unit discovery now reports 524 tests passing.

As of the 2026-05-19T02:57:27Z automation run, the direct automation protocol
passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed
through `git ls-remote` and `git push --dry-run`, startup unit discovery
passed, and `validate` passed. Phase 1 artifact migration stayed guard-only
and closed; no Phase 2/3 upload, removal, Git LFS change, history rewrite,
registry edit, or label import was performed.

The ePK lane now has a stronger review-only acceptor disambiguation
experiment. The new CLI builder
`build-epk-chain-ligand-acceptor-disambiguation-audit` generated
`artifacts/v3_epk_chain_ligand_acceptor_disambiguation_audit_1025.json`. It
keeps all three current ePK positives as feature hits, adds same-chain and
acceptor-like ligand-analog context, and produces 0 false hits across 25
negative-control rows: the current 20 NDK/PfkB/PfkA/ATP-grasp sibling controls
plus 5 older measured control rows. The three imported external hard negatives
remain abstentions. The feature passes current review controls but remains
`feature_admissible_for_production_scoring=false`.

`build-epk-chain-ligand-external-hard-negative-feature-screen` generated
`artifacts/v3_epk_chain_ligand_external_hard_negative_feature_screen_1025.json`.
It records 3/3 imported external hard negatives as abstentions and 0
non-abstentions under the chain/ligand feature, while keeping
`external_hard_negative_reaudit_scored=false` and clean held-out performance
claims closed.

The run also closed an older pre-count bookkeeping gap without changing the
underlying template artifacts. `build-epk-family-specific-mapping-template-validation-review`
generated
`artifacts/v3_epk_family_specific_mapping_template_validation_review_1025.json`,
which validates the PfkB, PfkA, and ATP-grasp family-specific templates by
downstream mapping and distance evidence only. This lets
`artifacts/v3_epk_precount_gate_status_1025.json` pass the
`family_specific_homolog_mapping_template`,
`chain_ligand_acceptor_disambiguation_audit`, and
`chain_ligand_external_hard_negative_feature_screen` gates. The pre-count lane
still remains `blocked_review_only` with five failing gates:
`acceptor_threshold_calibrated`, `external_hard_negative_scored_reaudit`,
`registry_and_label_factory_extension`,
`text_free_acceptor_feature_gap_audit`, and
`gamma_negative_control_distance_distribution`.

`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` was regenerated
against the updated pre-count status. It now records the chain/ligand feature
as passing current review controls with 0 sibling-control false hits and 0
external hard-negative feature non-abstentions, plus the three validated
family-template IDs. The threshold decision remains `do_not_select_threshold`;
no ePK score, external hard-negative scored re-audit, registry edit, or label
import exists.

Evidence-based confidence call: this run improved the ePK scorer-design
surface but did not create countable ePK evidence. Chain/ligand context is a
promising review-only counteraxis because it removes the 11 false hits from the
nearest-oxygen feature on current controls, but it still needs calibration and
generalization before production scoring. The next bounded science step should
turn that feature into a stricter text-free production candidate or add a
second counterevidence axis for the remaining negative-control distribution
blocker. Do not edit `mechanism_fingerprints.json`, import ePK labels, score
external hard negatives as clean held-out performance, or reopen artifact
migration Phase 2.

Verification passed with the 516-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, `jq empty` over updated ePK JSON,
targeted CLI/leakage tests for the new builders and updated artifacts, and
`git diff --check`.

As of the 2026-05-19T01:55:31Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed
through `git ls-remote` and `git push --dry-run`, startup unit discovery passed,
and `validate` passed. Phase 1 artifact migration stayed guard-only and closed;
no Phase 2/3 upload, removal, Git LFS change, history rewrite, registry edit,
or label import was performed.

The ePK lane now has `m_csa:640` alternate-state geometry reviewed without
turning it into production evidence. The new CLI builder
`build-epk-m-csa640-alternate-gamma-geometry-review` produced
`artifacts/v3_epk_m_csa640_alternate_gamma_geometry_review_1025.json` from the
existing ATP-state evidence and gamma-threshold control plan. It confirms
`3TM0` maps all four catalytic residues, treats B31 as a review-only
substrate-OH analog, measures ANP PG-to-B31 O14 at 3.558 Angstrom, and keeps
`production_scoring_admissible=false`, `epk_score_computed=false`, and all
registry/import flags false.

`artifacts/v3_epk_review_only_scoring_prototype_1025.json` was regenerated with
that alternate review attached. It still fails closed, but the decision surface
changed: all three current ePK rows are now positive-like review-only axis
hits under the uncalibrated 6-Angstrom candidate cutoff, while the four NDK
phosphohistidine controls, 16 PfkB/PfkA/ATP-grasp family-specific controls,
and three imported external hard negatives remain blocked or abstained.
`artifacts/v3_epk_precount_gate_status_1025.json` now passes the
`gamma_geometry_measured_for_all_prototype_rows` and
`m_csa640_alternate_gamma_geometry_reviewed` review-only gates, but the lane
remains `blocked_review_only` because acceptor-threshold calibration,
negative-control distribution readiness, text-free acceptor feature
admissibility, external hard-negative scored re-audit, and
registry/label-factory extension still fail.

The run then added the first explicit substrate-acceptor counteraxis prototype.
`build-epk-substrate-acceptor-counteraxis-prototype` generated
`artifacts/v3_epk_substrate_acceptor_counteraxis_prototype_1025.json`, marking
the three current ePK rows as positive-like review-only acceptor-axis hits,
blocking all 20 NDK/family-specific ATP-family controls, and abstaining on all
three imported external hard negatives. It records the weak axis directly:
source-supported acceptor identity is still review context, not a text-free
production scoring feature.
`artifacts/v3_epk_external_hard_negative_counteraxis_review_1025.json`
separately confirms the three imported external hard negatives remain
review-only abstentions under that counteraxis and explicitly forbids clean
held-out performance claims.

The run also tested the next weak axis as a negative result.
`build-epk-text-free-acceptor-feature-gap-audit` generated
`artifacts/v3_epk_text_free_acceptor_feature_gap_audit_1025.json`, which audits
the text-free nearest-gamma-to-oxygen feature at the same 6-Angstrom candidate
cutoff. It hits all three current ePK positives, but false-hits 11 of 20
NDK/PfkB/PfkA/ATP-grasp sibling controls, leaving the feature
`blocked_review_only`. This is the next concrete blocker: a production scorer
needs a text-free disambiguation signal beyond nearest oxygen distance, such
as chain/substrate context or ligand-class constraints.

Evidence-based confidence call: ePK is now a sharper review-only prototype,
not a countable positive fingerprint. The immediate geometry gap for
`m_csa:640` is closed for diagnostics, and the concrete counteraxis blocks
current sibling-family controls, but the simplest text-free acceptor feature
now fails with 11 sibling-control false hits. Production readiness is still
blocked by acceptor disambiguation, uncalibrated thresholds, and no real
external hard-negative scored re-audit. The next bounded science step should
add a stronger text-free acceptor disambiguation signal, then rerun the same
review-only counteraxis surface. Do not edit `mechanism_fingerprints.json`,
import ePK labels, treat external rows as clean held-out performance, or reopen
artifact migration Phase 2.

Verification passed with the final 510-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, `jq empty` on the updated ePK artifacts,
and targeted CLI/leakage tests for the new builders.

As of the 2026-05-19T00:55:27Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed
through `git ls-remote` and `git push --dry-run`, startup unit discovery passed,
and `validate` passed. Phase 1 artifact migration stayed guard-only and closed;
no Phase 2/3 upload, removal, Git LFS change, history rewrite, registry edit,
or label import was performed.

The ePK lane now has family-specific homolog counterevidence for all three
previously missing sibling families. The new review-only mapper
`build-epk-family-specific-homolog-mapping-review` consumes the seeded
family templates and uses role-compatible local residue evidence rather than
exact residue-position transfer. It produced
`artifacts/v3_epk_family_specific_homolog_mapping_review_pfkb_1025.json`,
`artifacts/v3_epk_family_specific_homolog_mapping_review_pfka_1025.json`, and
`artifacts/v3_epk_family_specific_homolog_mapping_review_atp_grasp_1025.json`.
Together they mark 16/32 homolog controls measurement-ready: 9/10 PfkB,
5/10 PfkA, and 2/12 ATP-grasp. The remaining 16 rows are terminally blocked
for this pass by unresolved acid/base mapping.

The paired distance sampler
`build-epk-family-specific-homolog-gamma-distance-sample` generated
`artifacts/v3_epk_family_specific_homolog_gamma_distance_sample_pfkb_1025.json`,
`artifacts/v3_epk_family_specific_homolog_gamma_distance_sample_pfka_1025.json`,
and
`artifacts/v3_epk_family_specific_homolog_gamma_distance_sample_atp_grasp_1025.json`.
The nearest PG-to-family-acid/base distances span 3.611-5.596 Angstrom, so all
16 measured PfkB/PfkA/ATP-grasp sibling controls hit the 6-Angstrom candidate
scenario. This is explicit negative evidence against distance-only ePK
thresholding, not a calibrated threshold or score.

`artifacts/v3_epk_review_only_scoring_prototype_1025.json` was regenerated
with those family-specific controls attached. It now contains 26 rows:
two uncalibrated positive-like ePK rows, one positive abstention, four NDK
phosphohistidine counter-axis blocks, 16 family-specific sibling-control
blocks, and three imported external hard-negative abstentions for
`uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`. The new
`artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` makes the
fail-closed result machine-readable: threshold selection remains
`do_not_select_threshold`, `epk_score_computed=false`,
`external_hard_negative_reaudit_scored=false`, and all registry/import flags
remain false.

`artifacts/v3_epk_precount_gate_status_1025.json` remains
`blocked_review_only`. The new `family_specific_homolog_mapping_from_template`
gate passes because all three template families now have measured
family-specific homolog controls, but the template-readiness gate itself still
fails, and so do acceptor-threshold calibration, full gamma geometry,
negative-control distribution readiness, external hard-negative scored
re-audit, and registry/label-factory extension.

Evidence-based confidence call: the ePK lane now has a stronger falsification
surface and a concrete scorer-design constraint, not a countable positive
fingerprint. A 6-Angstrom distance-only rule would collide with 16
non-ePK sibling controls and four NDK phosphohistidine controls. The next
bounded science step should add a substrate-acceptor/family-disambiguation
counteraxis or complete the missing `m_csa:640` gamma geometry by reviewing
the `3TM0` ANP/B31 alternate-state residue mapping and ligand-analog
admissibility before any real ePK score. Do not edit
`mechanism_fingerprints.json`, import ePK labels, score external hard negatives
as clean held-out performance, or reopen artifact migration Phase 2.

Verification passed with the final 502-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, `jq empty` on the updated ePK artifacts,
and `git diff --check`.

As of the 2026-05-18T23:53:56Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed,
startup unit discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. It added
`artifacts/v3_epk_sibling_control_homolog_gamma_distance_sample_ndk_1025.json`
plus the CLI builder
`build-epk-sibling-control-homolog-gamma-distance-sample`. This consumes the
NDK homolog mapping review and measures all four mapped structures (`1WKL`,
`3Q86`, `9OAN`, and `9PFY`) as phosphohistidine counter-axis controls. The
nearest PG-to-mapped-His distances are 2.899-3.339 Angstrom. This is useful
counterevidence against gamma-distance-only ePK thresholding, but it is not a
hydroxyl-acceptor calibration threshold, production ePK score, external
hard-negative re-audit, registry edit, or label import.

The run also opened bounded source-only queues for the remaining missing
sibling families:
`artifacts/v3_epk_sibling_control_homolog_source_plan_pfkb_1025.json` finds
9/10 PfkB candidates with gamma-capable nucleotide plus metal context,
`artifacts/v3_epk_sibling_control_homolog_source_plan_pfka_1025.json` finds
5/10 PfkA candidates, and
`artifacts/v3_epk_sibling_control_homolog_source_plan_atp_grasp_1025.json`
finds 2/12 ATP-grasp candidates. Those source-plan rows start as
mapping-pending, measurement-not-ready, non-countable, and review-only.

The same run continued into the first mapping audit for those queues:
`artifacts/v3_epk_sibling_control_homolog_mapping_review_pfkb_1025.json`,
`artifacts/v3_epk_sibling_control_homolog_mapping_review_pfka_1025.json`, and
`artifacts/v3_epk_sibling_control_homolog_mapping_review_atp_grasp_1025.json`.
All three fail closed under the current histidine-centric homolog mapper.
PfkB has 4 nucleotide-site mapped candidates but 0 catalytic-histidine mapped
candidates, PfkA has 5 and 0, and ATP-grasp has 0 and 0. None are
measurement-ready. This is a useful negative result: the remaining sibling
families need family-specific catalytic-residue templates before distance
measurement, not another blind gamma-distance pass.

`artifacts/v3_epk_family_specific_mapping_template_review_pfkb_1025.json`,
`artifacts/v3_epk_family_specific_mapping_template_review_pfka_1025.json`, and
`artifacts/v3_epk_family_specific_mapping_template_review_atp_grasp_1025.json`
seed the first family-specific templates from existing source-family geometry
evidence. Together they record 35 residue-role seeds across five M-CSA source
entries, but keep `family_specific_mapping_ready=false`, forbid exact
residue-position transfer to homolog candidates, and do not measure distances
or change any scorer.

`artifacts/v3_epk_review_only_scoring_prototype_1025.json` is the first
fail-closed ePK prototype evaluation surface. It records two uncalibrated
positive-like rows (`m_csa:35` and `m_csa:246`), one positive abstention
(`m_csa:640`), four NDK phosphohistidine counter-axis blocks, and three
imported external hard-negative abstentions for `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`. The artifact deliberately keeps
`epk_score_computed=false`, `threshold_calibrated=false`, and
`ready_to_expand_positive_fingerprint_universe=false`.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the
NDK homolog measurement attached. The lane remains `blocked_review_only`:
local axes, measured-row acceptor identity review, threshold/control planning,
non-ready-row exclusion, sibling alternate-control measurement, and NDK
homolog counter-axis measurement plus the PfkB/PfkA/ATP-grasp source templates
are explicit, but negative-control distribution readiness, acceptor-threshold
calibration, complete gamma geometry, family-specific homolog mapping from the
seeded templates, external hard-negative scored re-audit, and
registry/label-factory extension still fail closed.

Evidence-based confidence call: ePK now has a better falsification surface, not
a countable fingerprint. The next bounded ePK action should implement the
PfkB family-specific homolog mapper from the seeded source template because
PfkB has 9 gamma-plus-metal candidates and partial nucleotide-site mapping,
then re-run mapping before any measurement. PfkA is second; ATP-grasp still
needs better gamma-capable/source diversity as well as a mapper. Do not add
the ePK registry fingerprint, import ePK labels, score external hard negatives
as clean held-out performance, or reopen migration Phase 2.

Verification passed with the final 498-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, `jq empty` on the new ePK JSON artifacts,
and `git diff --check`.

As of the 2026-05-18T22:53:24Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed,
startup unit discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. It added
`artifacts/v3_epk_sibling_control_homolog_mapping_review_ndk_1025.json` plus
the CLI builder `build-epk-sibling-control-homolog-mapping-review`. This
consumes the NDK homolog-source plan and maps all four sourced NDK structures
(`1WKL`, `3Q86`, `9OAN`, and `9PFY`) to catalytic histidine plus local
nucleotide-site residue context. The mapping review sets
`measurement_ready_homolog_structure_count=4` for a future bounded
negative-control measurement pass, but it measures no calibration distance,
selects no threshold, computes no ePK score, runs no external hard-negative
re-audit, and changes no registry or label.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the NDK
homolog mapping review attached. The lane remains `blocked_review_only`: NDK
mapping is no longer the immediate blocker, but the pre-count gate still fails
negative-control distribution readiness, acceptor-threshold calibration,
complete gamma geometry, external hard-negative scored re-audit, and
registry/label-factory extension.

Evidence-based confidence call: ePK threshold selection is now blocked by the
next measurement/calibration step rather than NDK mapping. The highest-value
next bounded ePK action is to measure the mapped NDK homolog controls in a
review-only pass and then re-run the calibration sufficiency status; in
parallel only as needed, source metal-supported gamma-capable controls for
ATP-grasp, PfkA, and PfkB. Do not add the ePK registry fingerprint, import ePK
labels, score external hard negatives, or reopen migration Phase 2.

Verification passed with the final 490-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T21:52:26Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed,
startup unit discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. It added
`artifacts/v3_epk_sibling_control_homolog_source_plan_ndk_1025.json` plus the
CLI builder `build-epk-sibling-control-homolog-source-plan`. This consumes the
post-repair sibling-control source decision and opens the first one-family
homolog-source pass for NDK. The bounded RCSB shortlist contains four
gamma-capable, Mg-supported NDK structures (`1WKL`, `3Q86`, `9OAN`, and
`9PFY`), all kept `review_only` with
`measurement_ready_homolog_structure_count=0` because catalytic-residue mapping
is still pending. No distance was measured, no threshold was selected, no ePK
score or external hard-negative re-audit was run, and no registry or label was
changed.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the NDK
homolog-source plan attached. The lane remains `blocked_review_only`: NDK now
has source candidates for a future mapping pass, but the pre-count gate still
records 0 homolog structures ready for negative-control measurement, and
negative-control distribution readiness, acceptor-threshold calibration,
complete gamma geometry, external hard-negative scored re-audit, and
registry/label-factory extension still fail closed.

Evidence-based confidence call: ePK threshold selection is blocked in a more
diagnostic way. The direct graph-linked sibling-control repair surface remains
exhausted, and the first NDK homolog source shortlist is promising only as
source material, not calibration evidence. The next bounded ePK step should map
NDK catalytic histidine/nucleotide-site residues onto those four candidates
before any distance measurement; if mapping fails, move to PfkB
metal-supported homolog sourcing. Do not add the ePK registry fingerprint,
import ePK labels, score external hard negatives, or reopen migration Phase 2.

Verification passed with the final 488-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T20:50:54Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and
`git pull --ff-only origin main` were clean, SSH deploy-key push hygiene passed,
startup unit discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. It completed the direct graph-linked
one-family repair review for the remaining missing sibling ATP-family controls:
`artifacts/v3_epk_sibling_control_repair_review_atp_grasp_1025.json`,
`artifacts/v3_epk_sibling_control_repair_review_ndk_1025.json`, and
`artifacts/v3_epk_sibling_control_repair_review_pfka_1025.json`. ATP-grasp
has no candidate structures for `m_csa:310` and only no-target-ligand `8FBZ`
for `m_csa:498`; NDK `m_csa:637` has only product/partial `1DEL`
`AMP`/`DGP`/`MG` context; and PfkA `m_csa:365` has only no-target-ligand
`2PFK` context. Together with the existing PfkB review, all four missing
families have 0 measurement-ready repaired structures.

The run also added
`artifacts/v3_epk_missing_sibling_control_post_repair_source_decision_1025.json`
and the CLI builder
`build-epk-missing-sibling-control-post-repair-source-decision`. This artifact
routes all six missing sibling-control rows (`m_csa:310`, `m_csa:365`,
`m_csa:498`, `m_csa:637`, `m_csa:663`, and `m_csa:670`) to external or homolog
gamma-capable source search because direct graph-linked repair is exhausted.
It fetches no new candidates, measures no distances, selects no threshold,
scores no ePK rows, runs no external hard-negative re-audit, and changes no
registries.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with all four
sibling-control repair reviews attached. The lane remains
`blocked_review_only`: the aggregate repair-review fields now record
`negative_control_repair_review_family_ids=["atp_grasp","ndk","pfka","pfkb"]`,
0 total measurement-ready repaired structures, and unresolved rows
`m_csa:310`/`m_csa:365`/`m_csa:498`/`m_csa:637`/`m_csa:663`/`m_csa:670`, while
negative-control distribution readiness, acceptor-threshold calibration,
complete gamma geometry, external hard-negative scored re-audit, and
registry/label-factory extension still fail closed.

Evidence-based confidence call: ePK threshold selection is now blocked by a
clearer result, not an unreviewed direct-structure gap. The current direct
graph-linked sibling-control repair surface is exhausted and yields no
measurement-ready structures, so the next bounded ePK step should source
external or homolog gamma-capable controls for one family at a time, with NDK
ATP-state sourcing or PfkB metal-supported gamma-capable sourcing still the
highest-value choices. Do not add the ePK registry fingerprint, import ePK
labels, score external hard negatives, or reopen migration Phase 2.

Verification passed with the final 486-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T19:50:41Z automation run, the normal direct automation
protocol passed: the lock was acquired after replacing a stale dead-PID lock,
`git fetch` and `git pull --ff-only origin main` were clean, SSH deploy-key
push hygiene passed, startup unit discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. It added
`artifacts/v3_epk_sibling_control_repair_review_1025.json` plus the CLI
builder `build-epk-sibling-control-repair-review`. This consumes the missing
sibling-control source request and sibling alternate-structure plan for one
family, PfkB. The review confirms that ribokinase `m_csa:663` has complete
catalytic-residue mapping in gamma-capable `1GQT`/`ACP`, but the fetched CIF
has no metal ligand context. `m_csa:670` still has no gamma-capable
graph-linked alternate. The PfkB lane therefore remains `blocked_review_only`
with 0 measurement-ready repaired structures; no distance is measured, no
threshold is calibrated, no ePK score is computed, and no external
hard-negative re-audit is run.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the
PfkB repair-review artifact attached. The lane remains `blocked_review_only`:
the status now records `negative_control_repair_review_family_id=pfkb`,
`negative_control_repair_review_status=blocked_review_only`, and unresolved
PfkB rows `m_csa:663`/`m_csa:670`, while negative-control distribution
readiness, acceptor-threshold calibration, complete gamma geometry, external
hard-negative scored re-audit, and registry/label-factory extension still fail
closed.

Evidence-based confidence call: ePK scorer development is narrowed but still
not closer to countability. PfkB mapping ambiguity is resolved for `m_csa:663`,
but the missing metal context means PfkB still cannot be measured as a sibling
negative control. The active fingerprint universe remains 8; curated labels
remain 682 with 212 `seed_fingerprint` and 470 `out_of_scope` labels; external
imported labels remain exactly `uniprot:P06744`, `uniprot:P78549`, and
`uniprot:Q3LXA3`; external imported seed-fingerprint labels remain 0. The next
bounded ePK step should source a metal-supported PfkB gamma-capable control or
move to another missing sibling family, preferably NDK ATP-state sourcing or
ATP-grasp/PfkA gamma-capable sourcing. Do not add the ePK registry
fingerprint, import ePK labels, score external hard negatives, or reopen
migration Phase 2.

Verification passed with the final 482-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T18:48:23Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and `git pull --ff-only
origin main` were clean, SSH deploy-key push hygiene passed, startup unit
discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. It added
`artifacts/v3_epk_missing_sibling_control_source_request_1025.json` plus the
CLI builder `build-epk-missing-sibling-control-source-request`. This consumes
the negative-control calibration sufficiency decision, selected-structure
negative-control distribution, and sibling alternate-structure plan, then turns
the remaining ATP-grasp, NDK, PfkA, and PfkB coverage gaps into explicit
source/repair requests. The packet has 6 review-only rows: ATP-grasp
`m_csa:310` needs graph-linked or external structure evidence, ATP-grasp
`m_csa:498` and PfkA `m_csa:365` need additional gamma-capable source
evidence, NDK `m_csa:637` needs an ATP-state/gamma-capable alternate, and
PfkB `m_csa:663`/`m_csa:670` need metal/context or catalytic-residue mapping
repair plus additional source evidence. It measures no distances, selects no
threshold, scores no ePK rows, runs no external hard-negative re-audit, and
changes no registries.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the new
source-request packet attached. The lane remains `blocked_review_only`:
negative-control source requests are now explicit and
`negative_control_source_request_open=true`, while negative-control
distribution readiness, acceptor-threshold calibration, complete gamma
geometry, external hard-negative scored re-audit, and registry/label-factory
extension still fail closed.

Evidence-based confidence call: ePK scorer development is more actionable but
not closer to countability. The current blocker is now specific source/repair
work for ATP-grasp, NDK, PfkA, and PfkB sibling controls, plus the already
observed sibling-control collisions at candidate thresholds. There is still no
ePK scorer, calibrated threshold, positive-universe expansion, external
hard-negative ePK re-audit, registry edit, or label import. The active
fingerprint universe remains 8; curated labels remain 682 with 212
`seed_fingerprint` and 470 `out_of_scope` labels; external imported labels
remain exactly `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`;
external imported seed-fingerprint labels remain 0. The next bounded ePK step
should use the source-request packet to repair or source one missing sibling
family at a time, starting with PfkB mapping/metal-context repair or NDK
ATP-state sourcing. Do not add the ePK registry fingerprint, import ePK
labels, score external hard negatives, or reopen migration Phase 2.

Verification passed with the final 480-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T17:46:25Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and `git pull --ff-only
origin main` were clean, SSH deploy-key push hygiene passed, startup unit
discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any external
hard-negative label. It added
`artifacts/v3_epk_sibling_negative_control_alternate_gamma_distance_sample_1025.json`
plus the CLI builder
`build-epk-sibling-negative-control-alternate-gamma-distance-sample`. This
consumes the sibling alternate-control plan and measures only the three
gamma-plus-metal mapped candidates from that plan. All three are measured as
review-only counterevidence: ASKHA `m_csa:592`/`3FGU` has nearest ANP
PG-to-Thr hydroxyl distance 4.175 Angstrom, GHKL `m_csa:603`/`3CRL` has
nearest ANP PG-to-Ser hydroxyl distance 7.910 Angstrom, and ASKHA
`m_csa:696`/`1QHA` has nearest ANP PG-to-Thr hydroxyl distance 9.920 Angstrom.
No threshold is selected, no ePK score is computed, no external hard-negative
re-audit is run, and no registry is changed.

The run then added
`artifacts/v3_epk_negative_control_calibration_sufficiency_decision_1025.json`
plus `build-epk-negative-control-calibration-sufficiency-decision`. It combines
the two selected-structure sibling controls with the three alternate-control
measurements. The combined surface has 5 measured controls across 4 of 8
sibling ATP-family controls, leaves ATP-grasp, NDK, PfkA, and PfkB unmeasured,
and records `threshold_calibration_decision=do_not_select_threshold`. The
candidate 6-Angstrom scenario already collides with `m_csa:592` and
`m_csa:615`, while the 8-Angstrom scenario collides with `m_csa:592`,
`m_csa:603`, `m_csa:615`, and `m_csa:654`.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with both
new artifacts attached. The lane remains `blocked_review_only`: local-axis
prototyping, measured-row acceptor identity review, gamma-threshold control
planning, non-ready-row exclusion, sibling alternate-control measurement, and
negative-control sufficiency review are explicit, but negative-control
distribution readiness, acceptor-threshold calibration, complete gamma
geometry, external hard-negative scored re-audit, and registry/label-factory
extension still fail closed.

Evidence-based confidence call: ePK scorer-development now has a measured
negative-control warning surface rather than only a to-measure alternate list.
The conclusion is stricter, not looser: gamma-distance-only threshold selection
is unsafe and under-covered. There is still no ePK scorer, calibrated
threshold, positive-universe expansion, external hard-negative ePK re-audit,
registry edit, or label import. The active fingerprint universe remains 8;
curated labels remain 682 with 212 `seed_fingerprint` and 470 `out_of_scope`
labels; external imported labels remain exactly `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`; external imported seed-fingerprint
labels remain 0. The next bounded ePK step should source or measure missing
ATP-grasp, NDK, PfkA, and PfkB sibling controls, or design a non-distance-only
control axis before any threshold selection. Do not add the ePK registry
fingerprint, import ePK labels, score external hard negatives, or reopen
migration Phase 2.

Verification passed with the final 479-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T16:45:55Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and `git pull --ff-only
origin main` were clean, SSH deploy-key push hygiene passed, startup unit
discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label. First, it added
`artifacts/v3_epk_nonready_ligand_exclusion_decision_1025.json` plus the CLI
builder `build-epk-nonready-ligand-exclusion-decision`. This consumes the
non-ready ligand repair and alternate-structure artifacts and makes the current
calibration decision explicit: `m_csa:282` and `m_csa:662` stay excluded from
ePK threshold calibration because the alternate review found 3 gamma-capable
alternates but 0 alternates with gamma-capable nucleotide, metal context, and
complete catalytic-residue mapping. `m_csa:282` keeps its selected-structure
ATP/Mg signal classified as nonlocal, and `m_csa:662` remains metal-context
missing in its ANP alternates. The updated pre-count gate now passes only the
non-ready-row repaired-or-excluded gate; no local evidence audit, scorer,
threshold, registry, or label import is opened.

The run then added
`artifacts/v3_epk_sibling_negative_control_alternate_structure_plan_1025.json`
plus `build-epk-sibling-negative-control-alternate-structure-plan`. It expands
the sibling ATP-phosphoryl-transfer negative-control surface beyond selected
structures by screening 38 graph-linked alternate PDB structures for the 13
unmeasured non-ePK sibling controls under an 8-structure-per-entry cap. The
screen finds 7 gamma-capable alternate structures and 3 review-only
gamma-plus-metal mapped candidates for a future distance-measurement pass:
`m_csa:592`, `m_csa:603`, and `m_csa:696`. This is not a distance
distribution, threshold calibration, or ePK score; the selected-structure dNK
negative-control hit at 3.232 Angstrom remains the active warning against
gamma-distance-only thresholds.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with both
new artifacts attached. The lane remains `blocked_review_only`: local-axis
prototyping, measured-row acceptor identity review, gamma-threshold control
planning, and non-ready-row exclusion pass, but negative-control distribution
readiness, acceptor-threshold calibration, complete gamma geometry, external
hard-negative scored re-audit, and registry/label-factory extension still fail
closed.

Evidence-based confidence call: ePK scorer-development is cleaner because the
two non-ready rows can no longer silently influence threshold selection, and
the sibling-family control surface now has three concrete alternate structures
to measure next. There is still no ePK scorer, calibrated threshold,
positive-universe expansion, external hard-negative ePK re-audit, registry
edit, or label import. The active fingerprint universe remains 8; curated
labels remain 682 with 212 `seed_fingerprint` and 470 `out_of_scope` labels;
external imported labels remain exactly `uniprot:P06744`, `uniprot:P78549`,
and `uniprot:Q3LXA3`; external imported seed-fingerprint labels remain 0. The
next bounded ePK step should measure review-only gamma-to-hydroxyl distances
for the three mapped sibling alternate-control candidates, then decide whether
the negative-control distribution is still too sparse for threshold selection.
Do not add the ePK registry fingerprint, import ePK labels, score external hard
negatives, or reopen migration Phase 2.

Verification passed with the final 475-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T14:43:23Z automation run, the normal direct automation
protocol passed: the lock was acquired, `git fetch` and `git pull --ff-only
origin main` were clean, SSH deploy-key push hygiene passed, startup unit
discovery passed, `validate` passed, and
`validate-artifact-migration --dry-run --check-local-files` again reported 108
rows, 0 blockers, and `removal_allowed=0`. Phase 1 artifact migration remained
guard-only and closed.

The scientific work continued the review-only ePK lane by adding
`artifacts/v3_epk_negative_control_gamma_distance_distribution_1025.json` plus
the CLI builder `build-epk-negative-control-gamma-distance-distribution`. It
screens the 15 non-ePK sibling ATP-phosphoryl-transfer boundary rows from the
family-expansion artifact against selected-structure gamma-to-hydroxyl geometry.
Only two controls are currently measured: dNK `m_csa:615` has nearest DTP
PG-to-Ser hydroxyl distance 3.232 Angstrom, and GHMP `m_csa:654` has nearest
ANP PG-to-Ser hydroxyl distance 6.184 Angstrom. The close `m_csa:615` hit
falls under the 4-, 6-, and 8-Angstrom candidate scenarios, so gamma-distance
geometry alone is counterevidence, not an ePK threshold. The distribution is
started but `negative_control_distance_distribution_ready=false`.

The run also added
`artifacts/v3_epk_nonready_ligand_alternate_structure_plan_1025.json` plus
`build-epk-nonready-ligand-alternate-structure-plan`. It screens the two
non-ready ePK rows, `m_csa:282` and `m_csa:662`, across graph-linked PDB
structures. `m_csa:282` has one alternate gamma-capable structure (`4H3Q`) but
lacks metal context and catalytic-residue mapping; `m_csa:662` has two
alternate gamma-capable structures (`3X03` and `6K4H`) but no metal-supported
complete repair. The artifact records 3 alternate gamma-capable structures, 0
alternate gamma+metal+mapped structures, and keeps
`nonready_rows_repaired_or_excluded=false`.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the new
negative-control artifact attached. The lane remains `blocked_review_only`:
local-axis prototyping, measured-row acceptor identity review, and
gamma-threshold control planning pass, but negative-control distribution
readiness, acceptor-threshold calibration, complete gamma geometry,
non-ready-row repair, external hard-negative scored re-audit, and registry/
label-factory extension all fail closed.

Evidence-based confidence call: ePK now has a stronger pre-score control
surface, and the first sibling-family negative control shows why a simple
gamma-distance cutoff would be unsafe. There is still no ePK scorer, calibrated
threshold, positive-universe expansion, external hard-negative ePK re-audit,
registry edit, or label import. The active fingerprint universe remains 8;
curated labels remain 682 with 212 `seed_fingerprint` and 470 `out_of_scope`
labels; external imported labels remain exactly `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`; external imported seed-fingerprint
labels remain 0. The next bounded ePK step should expand sibling-family
negative-control coverage, review the `4H3Q`/`3X03`/`6K4H` alternate-structure
repair gaps, or keep `m_csa:282`/`m_csa:662` explicitly excluded before any
threshold selection. Do not add the ePK registry fingerprint, import ePK
labels, or score external hard negatives until the full pre-count gate path is
implemented.

Verification passed with the final 471-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T13:54:41Z automation run, a stale automation lock from an
interrupted ePK run was recovered after confirming the prior PID was not alive
and the dirty worktree was coherent. `git fetch`, `git pull --ff-only origin
main`, SSH deploy-key hygiene, unit discovery, `validate`, and
`validate-artifact-migration --dry-run --check-local-files` all passed before
continuing. Phase 1 artifact migration was again checked only as a guard and
remains closed/non-blocking: the manifest still reports 108 rows, 0 blockers,
and `removal_allowed=0`.

The recovered scientific work added the review-only
`artifacts/v3_epk_acceptor_identity_review_1025.json` and
`artifacts/v3_epk_atp_state_evidence_plan_1025.json` builders. The former
confirms the two measured ePK gamma-to-acceptor rows are source-supported
review candidates (`m_csa:35` Ser hydroxyl and `m_csa:246` Tyr hydroxyl on
non-catalytic substrate chains). The latter narrows the `m_csa:640` product-
state blocker to graph-linked ATP-state analog evidence: `1J7U` and `3TM0`
carry ANP/Mg context and map all four catalytic sequence-position residues,
while `3TM0` also carries acceptor-like `B31` with nearest ANP PG-to-B31 oxygen
distance 3.558 Angstrom. Both artifacts are review-only and do not compute an
ePK score.

This run then added
`artifacts/v3_epk_gamma_threshold_control_plan_1025.json` plus the CLI builder
`build-epk-gamma-threshold-control-plan`. It combines the two selected-
structure positive-like distances (`m_csa:35` 3.610 Angstrom and `m_csa:246`
5.082 Angstrom) with the alternate `m_csa:640` `3TM0` ANP/B31 distance (3.558
Angstrom). The 4-Angstrom candidate threshold misses `m_csa:246`; 6 and
8 Angstrom cover the review geometry, but every scenario is marked
`not_selectable_without_negative_controls`. Required controls remain external
hard-negative expanded-ontology re-audit, sibling ATP-phosphoryl-transfer
family controls, repaired/excluded `m_csa:282` and `m_csa:662`, and an explicit
alternate-structure policy for `m_csa:640`.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with the
threshold-control plan attached. The lane remains `blocked_review_only`:
local-axis prototyping, measured-row acceptor identity review, and gamma-
threshold control planning pass, while acceptor-threshold calibration,
complete gamma geometry, non-ready row repair, external hard-negative scored
re-audit, and registry/label-factory extension still fail closed.

Evidence-based confidence call: ePK has a cleaner pre-score review surface, but
there is still no ePK scorer, calibrated threshold, positive-universe
expansion, external hard-negative ePK re-audit, registry edit, or label import.
The active fingerprint universe remains 8; curated labels remain 682 with 212
`seed_fingerprint` and 470 `out_of_scope` labels; external imported labels
remain exactly `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`;
external imported seed-fingerprint labels remain 0. The next bounded ePK step
should collect negative-control gamma-distance distributions or repair/exclude
`m_csa:282` and `m_csa:662` before any threshold selection. Verification
passed with the final 467-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T08:16:50Z automation run, Phase 1 artifact migration was
checked only as a guard and remains closed/non-blocking:
`validate-artifact-migration --dry-run --check-local-files` still reports 108
rows, 0 blockers, and `removal_allowed=0`. The scientific work continued the
review-only ePK positive-fingerprint path without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any external
hard-negative label.

The run added `artifacts/v3_epk_acceptor_identity_review_1025.json` plus the
CLI builder `build-epk-acceptor-identity-review`. It consumes the review-only
gamma-geometry measurement sample and the current 1,000-slice graph to review
whether the measured hydroxyl atoms match source-supported substrate-acceptor
identity. Both gamma-measured rows pass that review context: `m_csa:35` maps
nearest ATP PG to a non-catalytic-chain Ser hydroxyl consistent with protein
substrate hydroxyl context, and `m_csa:246` maps nearest ANP PG to a
non-catalytic-chain Tyr hydroxyl consistent with tyrosine substrate context.
`m_csa:640` remains source-supported but unmeasured because the selected
structure is local ADP/product-state rather than ATP/gamma-capable.

The run then added `artifacts/v3_epk_atp_state_evidence_plan_1025.json` plus
the CLI builder `build-epk-atp-state-evidence-plan`. It screens the
graph-linked PDB structures for `m_csa:640` and finds eight candidate
structures. Two alternates (`1J7U` and `3TM0`) have gamma-capable ANP/Mg
context and map all four catalytic sequence-position residues. `3TM0` also
carries the acceptor-like aminoglycoside ligand code `B31`; the current
selected `1L8T` retains ADP/Mg plus KAN context. The same artifact measures
nearest ANP PG-to-B31 oxygen distance at 3.558 Angstrom in `3TM0`, still
review-only. This narrows the next action to threshold/control design before
any scorer work.

`artifacts/v3_epk_precount_gate_status_1025.json` was regenerated with that
acceptor-identity review and the ATP-state evidence plan attached. The
measured-row acceptor identity gate now passes, but the overall lane remains
`blocked_review_only`: acceptor-threshold calibration, complete gamma geometry
across all prototype rows, non-ready-row repair, external hard-negative scored
re-audit, and registry/label-factory extension still fail closed. Mechanism
text is explicitly review context only and is not an ePK scoring feature.

Evidence-based confidence call: this removes the measured-row acceptor identity
ambiguity for `m_csa:35` and `m_csa:246`, but it is still not an ePK scorer or
positive fingerprint expansion. The active fingerprint universe remains 8;
curated labels remain 682 with 212 `seed_fingerprint` and 470 `out_of_scope`
labels; external imported labels remain exactly `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`; external imported seed-fingerprint
labels remain 0. The next bounded ePK step should design threshold/control
criteria for the measured `m_csa:640` alternate geometry, calibrate
acceptor/gamma thresholds only after appropriate negative controls exist, or
act on the `m_csa:282`/`m_csa:662` ligand-repair lanes. Do not add the ePK
registry fingerprint, import ePK labels, or score external hard negatives until
the full pre-count gate path is implemented.
Verification passed with the final 465-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T07:14:59Z automation run, Phase 1 artifact migration was
checked only as a guard and remains closed/non-blocking:
`validate-artifact-migration --dry-run --check-local-files` still reports 108
rows, 0 blockers, and `removal_allowed=0`. The scientific work continued the
review-only ePK positive-fingerprint path without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any external
hard-negative label.

The run added `artifacts/v3_epk_text_free_local_axis_prototype_1025.json` plus
the CLI builder `build-epk-text-free-local-axis-prototype`. The artifact
materializes binary local feature axes only for the three rows already marked
ready by the local-evidence audit: `m_csa:35`, `m_csa:246`, and `m_csa:640`.
Each row has local adenine-nucleotide, metal-ligand, and catalytic acid/base
axes from geometry evidence. `m_csa:282` and `m_csa:662` remain excluded from
the prototype because their local ligand axes are not ready. The artifact keeps
entry names as traceability only and explicitly excludes names, EC/Rhea IDs,
UniProt prose, M-CSA text, curated label strings, and expert rationales from
predictive use.

The run also added
`artifacts/v3_epk_acceptor_geometry_axis_gap_plan_1025.json` plus the CLI
builder `build-epk-acceptor-geometry-axis-gap-plan`. This stays review-only and
uses current geometry features to expose candidate acceptor context for the
same three prototype rows: hydroxyl-residue pocket context for all three rows
and near acceptor-like `KAN` ligand context for `m_csa:640`. `m_csa:282` and
`m_csa:662` remain excluded until their local ligand axes are repaired. The
artifact does not verify acceptor identity, threshold the acceptor axis, measure
gamma-phosphate-to-acceptor geometry, compute an ePK score, or score external
hard negatives under ePK.

Finally, `artifacts/v3_epk_nonready_ligand_repair_plan_1025.json` plus
`build-epk-nonready-ligand-repair-plan` now make the two excluded-row repair
lanes explicit. `m_csa:282` has ATP and Mg only as nonlocal structure-level
ligands in selected structure `1S9I`, so it needs local ligand-distance,
residue-mapping, or selected-structure repair. `m_csa:662` has no
selected-structure ligand axis in `1BO1`, so it needs alternate ligand evidence
or alternate-structure sourcing before it can join any ePK scorer prototype.

`artifacts/v3_epk_acceptor_axis_threshold_design_1025.json` plus
`build-epk-acceptor-axis-threshold-design` records candidate acceptor-axis
cutoffs of 4, 6, and 8 Angstrom. The 6 Angstrom candidate is the smallest one
that covers the three current prototype rows by hydroxyl-residue context, but
it is explicitly not selected or calibrated and cannot be used as an ePK
threshold until gamma-phosphate-to-acceptor geometry and external re-audit
controls exist.

`artifacts/v3_epk_gamma_geometry_feasibility_plan_1025.json` plus
`build-epk-gamma-geometry-feasibility-plan` closes the run by separating
atom-level reaction-center feasibility from scoring. `m_csa:35` and
`m_csa:246` have local ATP/ANP plus acceptor context and are ready for a future
gamma-phosphate atom-geometry measurement. `m_csa:640` has local ADP plus
acceptor context, so it needs ATP-state or analog evidence before gamma
geometry can support scoring.

The run then added `artifacts/v3_epk_gamma_geometry_measurement_sample_1025.json`
plus `build-epk-gamma-geometry-measurement-sample`, using RCSB mmCIF atom
coordinates for `2PHK` and `1IR3`. It measures review-only nearest
PG-to-candidate-hydroxyl distances of 3.610 Angstrom for `m_csa:35` and
5.082 Angstrom for `m_csa:246`; `m_csa:640` remains skipped because the
selected structure is local ADP/product-state rather than ATP/gamma-capable.
These distances are not accepted substrate identities, thresholds, ePK scores,
external-hard-negative re-audit evidence, or label gates.

`artifacts/v3_epk_precount_gate_status_1025.json` plus
`build-epk-precount-gate-status` consolidates the current lane as
`blocked_review_only`. The local-axis prototype gate passes, while acceptor
threshold calibration, complete gamma geometry across all prototype rows,
non-ready-row repair, external hard-negative scored re-audit, and registry/
label-factory extension all fail closed.

Evidence-based confidence call: this is a useful scorer-development surface,
but still not an ePK scorer or positive fingerprint expansion. The active
fingerprint universe remains 8; curated labels remain 682 with 212
`seed_fingerprint` and 470 `out_of_scope` labels; external imported labels
remain exactly `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`;
external imported seed-fingerprint labels remain 0. Acceptor geometry,
gamma-phosphoryl-transfer reaction-center geometry, ePK threshold calibration,
external hard-negative scored re-audit, terminal review, label-factory gate
extension, and registry edits remain blockers before any countable ePK work.
The next bounded ePK step, if chosen, should verify whether the measured
hydroxyl atoms are true substrate acceptors, source ATP-state evidence for
`m_csa:640`, or act on the two explicit ligand-repair lanes; do not add the ePK
registry fingerprint, import ePK labels, or score external hard negatives until
the full pre-count gate path is implemented.
Verification passed with the final 461-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T06:13:08Z automation run, Phase 1 artifact migration was
checked only as a guard and remains closed/non-blocking:
`validate-artifact-migration --dry-run --check-local-files` still reports 108
rows, 0 blockers, and `removal_allowed=0`. The scientific work stayed on the
post-infra ePK positive-fingerprint path without editing
`mechanism_fingerprints.json`, `curated_mechanism_labels.json`, or any
external hard-negative label.

The run added `artifacts/v3_epk_draft_fingerprint_spec_1025.json`, a
review-only draft fingerprint specification for
`epk_atp_gamma_phosphoryl_transfer`. It freezes the intended local predictive
axes (ATP/Mg2+ positioning, ATP gamma-phosphoryl-transfer reaction center,
hydroxyl-acceptor scope, acid/base activation, and neighboring ATP-family
counterevidence), explicitly excludes protein names, EC/Rhea identifiers,
UniProt prose, M-CSA mechanism text, curator rationales, and label strings from
predictive use, and keeps the pre-count gate state blocked. The artifact keeps
the positive fingerprint universe at 8, imports 0 labels, scores 0 external hard
negatives, and leaves all three imported external hard negatives only as
review-only re-audit rows.

The same run added `artifacts/v3_epk_local_evidence_audit_1025.json`, which
profiles those five ePK boundary rows against the current 1,000-slice geometry
artifact. Three rows (`m_csa:35`, `m_csa:246`, and `m_csa:640`) have local
nucleotide, metal, and acid/base axes ready for a future text-free axis
prototype. `m_csa:282` has ATP/Mg structure-level signal but not a local active
site ligand axis, and `m_csa:662` lacks a local ligand axis. The audit computes
no ePK score, keeps `ready_to_run_epk_scorer=false`, and leaves acceptor
geometry, threshold calibration, external hard-negative re-audit, terminal
review, and label-factory gates as blockers before any countable ePK work.

Evidence-based confidence call: the ePK lane is now better specified and has a
first local-evidence readiness profile, but it is still not a positive
fingerprint expansion. The active fingerprint universe remains 8; curated
labels remain 682 with 212 `seed_fingerprint` and 470 `out_of_scope` labels;
external imported labels remain exactly `uniprot:P06744`, `uniprot:P78549`, and
`uniprot:Q3LXA3`; external imported seed-fingerprint labels remain 0. The next
bounded ePK step, if chosen, should prototype a text-free local ePK feature axis
only on the three ready rows, or repair the `m_csa:282`/`m_csa:662`
ligand/structure gaps. Do not import ePK labels, add the ePK registry
fingerprint, or reuse external hard negatives under ePK until scorer,
threshold, re-audit, terminal-review, and label-factory gates pass.
Verification passed with the final 447-test unit suite, `validate`,
`validate-artifact-migration --dry-run --check-local-files`, `compileall`,
external label invariant inspection, and `git diff --check`.

As of the 2026-05-18T05:10:47Z automation run, Phase 1 artifact migration was
checked only as a guard and remains closed/non-blocking: `validate`, the 439
unit-test suite, and `validate-artifact-migration --dry-run
--check-local-files` all passed with the 682-label, 8-fingerprint baseline.
The run then moved to bounded science work and created
`artifacts/v3_epk_positive_fingerprint_readiness_packet_1025.json`.

The new ePK packet packages the five expert-supported ePK/ePK-like
ATP/phosphoryl-transfer boundary rows (`m_csa:35`, `m_csa:246`, `m_csa:282`,
`m_csa:640`, and `m_csa:662`) as review-only evidence for a future positive
fingerprint. It records ATP gamma-phosphoryl-transfer reaction-center evidence,
hydroxyl-acceptor scope, ATP/Mg2+ context, hydrolase-top1 counterevidence, and
neighboring ATP-family controls. Evidence-based confidence call: the ePK lane
is ready for draft fingerprint specification work, but not for registry
expansion, countable seed labels, or external hard-negative evaluation claims.
The active positive fingerprint universe remains 8, curated labels remain 682,
external imported out-of-scope labels remain exactly `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`, and the ePK packet explicitly blocks
count growth on external-hard-negative re-audit plus future scoring and
label-factory gates.

The same run also added
`artifacts/v3_epk_external_hard_negative_reaudit_plan_1025.json`, a review-only
checklist for `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`. It
confirms all three external label contracts and evidence-separation fields are
intact, but keeps their ePK status `planned_not_scored`; no ePK score,
threshold, terminal decision, or label change was produced.

Next automation should continue from this ePK readiness surface only if it can
stay review-only or explicitly implement the missing pre-count gates. Do not
add the ePK fingerprint to `mechanism_fingerprints.json`, import ePK labels, or
use external hard negatives under a widened ontology until an ePK scorer,
inverse-gate threshold policy, external hard-negative re-audit, terminal-review
rerun, and label-factory gate plan are implemented and pass. If the next run
does not take ePK forward, choose another bounded external-source
mechanism-readiness task rather than artifact migration.

As of the 2026-05-18T04:03:36Z automation run, Phase 1 is complete and
stopped at the Phase 2 approval checkpoint. The execution manifest was
refreshed against latest pulled `main` commit
`072ce84b57e8c86c23b61b6ebe2d2c6a4c63c94f` and still covers 108 large
noncanonical rows with 0 migration-ready rows, 0 remote SHA-256 verifications,
0 restore-test passes, and 0 removal authorizations. Producer status is now
68 `known`, 40 `unavailable_with_reason`, and 0 `unknown_blocking`. The final
24 geometry-feature rows from slices 275 through 850 were closed as
`unavailable_with_reason` rather than known: Git history and the committed
progress log identify the label-batch/artifact commits, but the exact
per-row adjacent-slice `--reuse-existing` plus PDB/mmCIF cache closure is not
reconstructable from committed state. Each row preserves committed path, size,
SHA-256, Git target URI, source inputs, producer command pattern, downstream
consumers, and migration blockers.

Phase 2 readiness checklist for human approval: choose the external storage
target, select the approved row subset, upload only after approval, record
non-Git `target_uri` values, independently verify remote SHA-256, run restore
subset tests from the uploaded targets, keep `removal_allowed=false`, and rerun
the full source-only plus restored-artifact validation suite. Phase 2 is not
authorized by the current automation prompt, and Phase 3 Git removal is also
not authorized.

Evidence-based confidence call: this was a no-science-recompute Phase 1
provenance-manifest closure and readiness-report pass. No artifact upload,
deletion, Git LFS migration, externalization, label/import artifact edit,
scientific-artifact recompute, or history rewrite was performed. Verification
passed with startup 439-test unit discovery, startup CLI `validate`, targeted
artifact/transfer/source-only tests, final 439-test unit discovery,
source-only compile/import/CLI-help/validate smokes,
`validate-artifact-migration --dry-run`, `validate-artifact-migration
--dry-run --check-local-files`, restore smoke dry-run, transfer-scope public
contract import, and external label invariant inspection. Early exit exception:
the measured elapsed time was 9.383 minutes because all remaining safe Phase 1
steps are complete and the next action is an approval-gated Phase 2 storage
decision.

As of the 2026-05-18T03:03:01Z automation run, Phase 1 remains
instrumentation-only and continued Step 6 on the geometry-feature provenance
gaps. The execution manifest was refreshed against latest pulled `main` commit
`330180448ddbd407d2b4ccea9c7603ae2fa7b3d5` and still covers 108 large
noncanonical rows with 0 migration-ready rows, 0 remote SHA-256 verifications,
0 restore-test passes, and 0 removal authorizations. Producer status is now
68 `known`, 16 `unavailable_with_reason`, and 24 `unknown_blocking`. The new
unavailable rows are `artifacts/v3_geometry_features_875.json`,
`artifacts/v3_geometry_features_900.json`,
`artifacts/v3_geometry_features_925.json`,
`artifacts/v3_geometry_features_950.json`, and
`artifacts/v3_geometry_features_975.json`; their exact historical
adjacent-slice `--reuse-existing` plus PDB/mmCIF cache closure is not
reconstructable from committed state, but each row preserves committed path,
size, SHA-256, Git target URI, source inputs, producer command pattern,
downstream consumers, and migration blockers. The remaining
`unknown_blocking_count` is 24, all geometry feature artifacts from slices
275 through 850 with adjacent-slice provenance gaps.
Evidence-based confidence call: this was a no-science-recompute Phase 1
provenance-manifest pass. No artifact upload, deletion, Git LFS migration,
externalization, label/import artifact edit, scientific-artifact recompute, or
history rewrite was performed. Verification passed with startup and final
439-test unit discovery, targeted artifact/transfer/source-only tests,
source-only compile/import/CLI-help/validate smokes, CLI `validate`,
`validate-artifact-migration --dry-run --check-local-files`, restore smoke
dry-run, external label invariant inspection, and `git diff --check`. The next
automation run should stay in Phase 1 Step 6 on the 24 remaining
geometry-feature provenance gaps; do not start Phase 2 uploads without
explicit human authorization.

As of the 2026-05-18T02:00:59Z automation run, Phase 1 remains
instrumentation-only. The run first verified Step 1 through Step 5 readiness,
then made a narrow Step 2/Step 3 safety hardening pass and one Step 6
provenance batch. The migration validator now rejects downstream-consumer
accounting drift, and regression coverage explicitly blocks unsafe removal
contract drift plus restore overwrite of an existing mismatched file without
`--force`. The execution manifest was refreshed against latest pulled `main`
commit `cd8e72c34b5bc180b40c949263c64c028ef7ed06` and still covers 108 large
noncanonical rows with 0 migration-ready rows, 0 remote SHA-256 verifications,
0 restore-test passes, and 0 removal authorizations. Producer status is now
68 `known`, 11 `unavailable_with_reason`, and 29 `unknown_blocking`. The new
unavailable rows are `artifacts/v3_geometry_features_1000.json` and
`artifacts/v3_geometry_features_1025.json`; their exact historical
adjacent-slice `--reuse-existing` plus PDB/mmCIF cache closure is not
reconstructable from committed state, but each row preserves committed path,
size, SHA-256, Git target URI, source inputs, producer command pattern,
downstream consumers, and migration blockers. The remaining
`unknown_blocking_count` is 29, all geometry feature artifacts from slices
275 through 975 with adjacent-slice provenance gaps.
Evidence-based confidence call: this was a no-science-recompute Phase 1
manifest/validator/restore/provenance pass. No artifact upload, deletion, Git
LFS migration, externalization, label/import artifact edit, scientific-artifact
recompute, or history rewrite was performed. Verification passed with targeted
artifact/transfer/source-only tests, full 439-test unit discovery, CLI
`validate`, `validate-artifact-migration --dry-run`, restore smoke dry-run,
external label invariant inspection, and `git diff --check`. The next
automation run should stay in Phase 1 Step 6 on the 29 remaining
geometry-feature provenance gaps; do not start Phase 2 uploads without
explicit human authorization.

As of the 2026-05-17T23:56:35Z automation run, Phase 1 remains
instrumentation-only and closed one conservative producer-provenance family.
The execution manifest was refreshed against latest pulled `main` commit
`0bf97dc45e98b03ba15139eda98e44c4f6608131` and still covers 108 large
noncanonical rows with 0 migration-ready rows, 0 remote SHA-256 verifications,
0 restore-test passes, and 0 removal authorizations. The 9 Foldseek coordinate
sidecars now use `producer_status=unavailable_with_reason`: their historical
fetch/restage session is not reconstructable from committed state, but each
row preserves the committed path, size, SHA-256, Git target URI, source inputs,
producer command pattern, downstream consumers, and migration blockers. The
remaining `unknown_blocking_count` is 31, all geometry feature artifacts with
adjacent-slice `--reuse-existing` provenance gaps. A validator hardening test
now also blocks non-Git/externalized storage rows that lack `target_uri`, even
if no removal is authorized yet.
Evidence-based confidence call: this was a no-science-recompute Phase 1
manifest/validator provenance pass. No artifact upload, deletion, Git LFS
migration, externalization, label/import artifact edit, scientific-artifact
recompute, or history rewrite was performed. Verification passed with targeted
artifact/transfer/source-only tests, source-only compile, `transfer_scope`
import, CLI help, CLI `validate`, full 437-test unit suite,
`validate-artifact-migration --dry-run --check-local-files`, restore smoke
dry-run, and `git diff --check`. The next automation run should stay in Phase
1 and continue Step 6 on the 31 geometry-feature provenance gaps; do not start
Phase 2 uploads without explicit human authorization.

As of the 2026-05-17T22:57:18Z automation run, Phase 1 remains
instrumentation-only and has a provenance-readability hardening slice. The
execution manifest was refreshed against latest pulled `main` commit
`6a29655d595314d33558947531e21391b66046e0` and still covers 108 large
noncanonical rows with 0 migration-ready rows, 0 remote SHA-256 verifications,
0 restore-test passes, and 0 removal authorizations. Execution rows now carry
the producer command list, source inputs, parameter assumptions, and explicit
`producer_provenance_recovery_steps`; the validator requires known producers to
retain commands and `unknown_blocking` rows to retain recovery steps. The 40
blocked rows remain 31 geometry feature artifacts and 9 Foldseek coordinate
sidecars, all with source status `partially_inferred`, and all still
`removal_allowed=false`. The storage inventory/policy/admission guard were
refreshed after the execution manifest changed; inventory now covers 2,580
artifact files and 2.5563 GiB with 108 large files, 0 policy blockers, and 0
deletion authorization.
Verification passed with targeted artifact/transfer tests, source-only compile,
`transfer_scope` import, CLI help, CLI `validate`, full 436-test unit suite,
`validate-artifact-migration --dry-run --check-local-files`, restore smoke
dry-run, and `git diff --check`.
Evidence-based confidence call: this was a no-science-recompute Phase 1
instrumentation hardening pass. No artifact upload, deletion, Git LFS
migration, externalization, label/import artifact edit, scientific-artifact
recompute, or history rewrite was performed. The next automation run should
stay in Phase 1 and either keep tightening provenance for the 40
`unknown_blocking` rows or add more negative validator tests; do not start
Phase 2 uploads without explicit human authorization.

As of the 2026-05-17T21:46:03Z automation run, Phase 1 remains
instrumentation-only and has one additional fail-closed validator hardening
slice. The `validate-artifact-migration` path now rejects any
`storage_class=git` execution row whose `target_uri` is not an explicit
`git:<source_path>@<commit>` identity matching both the row `source_path` and
the manifest's recorded `current_main_commit`, and it blocks
`migration_ready=true` on Git-retained rows or `unknown_blocking` producer
provenance. The committed execution
manifest was refreshed against latest pulled `main` commit
`75d82f0ad0edc1e84501ebe4d9cbc9389f4bbb27`; it still has 108 rows, 0
migration-ready rows, 0 remote SHA-256 verifications, and 0 removal
authorizations. The 40 `unknown_blocking` rows remain blocked, but their
per-row `producer_status_reason` now distinguishes the 31 geometry
adjacent-slice `--reuse-existing` provenance gaps from the 9 Foldseek
coordinate sidecar refetch/restage hash-closure gaps. Regression coverage now
validates the committed execution manifest itself plus a negative path for Git
target path/commit drift. The `artifact_pointer.v1` validator now rejects empty
restore contracts, invalid size/hash/storage metadata, and non-SHA-256 restore
verification before any future pointer replacement can pass tests. The
source-only contract test also covers `validate-artifact-migration --dry-run`,
and the sparse-checkout docs now include the small execution manifest without
restoring large artifact payloads. Verification passed with 436 unit tests,
targeted artifact/transfer/source-only tests, source compile/import/CLI
help/validate, migration validation with local file checks, restore smoke
dry-run, and `git diff --check`.
Evidence-based confidence call: this was a no-science-recompute Phase 1
instrumentation hardening pass. No artifact upload, deletion, Git LFS
migration, externalization, scientific-artifact recompute, label/import
artifact edit, or history rewrite was performed. The next automation run should
stay in Phase 1 and continue with provenance tightening for the 40
`unknown_blocking` producer rows unless a human explicitly authorizes Phase 2
uploads.

As of the 2026-05-17T21:12:59Z automation run, Phase 1 remains
instrumentation-only and has been hardened without artifact upload or removal.
The `validate-artifact-migration` CLI now rejects stale current-main baseline
metadata and stale row-derived execution counts before any future removal gate
can pass. The execution manifest was refreshed against latest pulled
`origin/main` commit `0a68c40335b4af8f00aeafc281e72b4fc6e81cae`, so current
`git:<source_path>@<commit_sha>` target URIs point at that main baseline while
still reporting `migration_ready_count=0`, `remote_sha256_verified_count=0`,
`restore_test_passed=false`, and `removal_allowed_count=0`. Its
`unknown_blocking_summary` records the current 40 blocked producer rows as 31
regenerable geometry feature artifacts and 9 Foldseek coordinate sidecars; this
is diagnostic only and does not make any row migration-ready. Each execution row
now also records the source producer command status and a producer-status reason
so `partially_inferred` provenance remains visible after fail-closed mapping to
`unknown_blocking`. Evidence-based confidence call: this is a
no-science-recompute Phase 1 hardening slice; label
registries, import-decision artifacts, retrieval outputs, sequence-distance
metrics, and hard-negative decision artifacts were not edited. The next
automation run should continue Phase 1 only by tightening/documenting the 40
`unknown_blocking` producer rows, unless a human explicitly authorizes Phase 2
uploads.

As of the 2026-05-17T19:28:16Z automation run, Phase 1 of no-loss artifact
migration instrumentation is implemented and pushed forward from current
`main`; no Phase 2 upload or Phase 3 artifact removal has been performed.
`artifacts/v3_artifact_migration_execution_1025.json` is the execution manifest
for `artifact_migration_execution.v1`, derived from the existing readiness plan
and producer/consumer manifest. It targets
`baseline=current_main_three_external_hard_negatives`, `slice_id=1025`, and
`canonical_countable_label_count=682`; the external imported out-of-scope labels
remain exactly `uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`, with
0 imported external seed-fingerprint labels and ontology version
`label_factory_v1_8fp`.

The execution manifest covers 108 large noncanonical rows. Producer status is
68 `known` and 40 `unknown_blocking` after mapping historical
`partially_inferred` provenance to fail-closed blocking status. Every current
row is explicitly `storage_class=git` with a `git:<source_path>@<commit_sha>`
target URI. Status counts remain fail-closed:
`migration_ready_count=0`, `remote_sha256_verified_count=0`,
`removal_allowed_count=0`, and all stored `removal_allowed` values are derived
by the validator. The new `validate-artifact-migration` CLI accepts this Phase
1 draft because every row is explicitly blocked from removal; it rejects
malformed hashes, unsafe producer/storage states, canonical removal, missing
restore/summary/target information, missing remote hash verification, missing
restore tests, unaccounted downstream consumers, and any stored removal value
that disagrees with the derived gate.
The storage inventory/policy chain was refreshed after adding the execution
manifest: inventory now covers 2,580 artifact files and still has 108 large
files, 0 policy blockers, and 0 deletion authorizations.

Restore support is now fail-closed through `restore-artifacts`. It supports
`--dry-run`, `--path`, `--subset smoke`, local/file targets for tests, Git
targets for current in-repo rows, hash verification before writing, quarantine
on hash mismatch, and no overwrite of an existing mismatched file without
`--force`. Pointer records are defined as `artifact_pointer.v1`; Phase 1 only
adds the format and tests and does not replace any artifact with a pointer.
Source-only reproducibility tests now cover `compileall`, importing
`catalytic_earth.transfer_scope`, CLI help, CLI `validate`, and a public
contract import for the transfer-scope symbols previously involved in a clean
checkout failure.

Evidence-based confidence call: artifact migration instrumentation is coherent
for Phase 1 and does not alter label registries, import-decision artifacts,
retrieval outputs, sequence-distance metrics, or other scientific artifacts.
The next automation run should not upload, remove, migrate to LFS, or rewrite
history without an explicit Phase 2/Phase 3 human authorization. If continuing
within Phase 1 only, the highest-value follow-up is tightening or documenting
the 40 `unknown_blocking` producer rows, while keeping `removal_allowed=false`.

As of the 2026-05-17T18:06:14Z automation run, artifact infrastructure has a
durable no-loss planning layer but no migration has been performed.
`artifacts/v3_artifact_storage_inventory_1025.json` now covers 2,579 artifact
files and 2.556 GiB of artifact payload, with 108 files above the 5 MiB
large-file threshold. `artifacts/v3_artifact_storage_policy_check_1025.json`
passes with 0 blockers and 0 deletion authorizations.
`artifacts/v3_artifact_producer_consumer_manifest_1025.json` covers all 108
large noncanonical rows: 99 `regenerable_intermediate` and 9 `raw_cache` rows,
with 68 `known` producer command statuses and 40 `partially_inferred` statuses.
`artifacts/v3_artifact_migration_readiness_plan_1025.json` ranks those rows as
8 `candidate_git_lfs_later`, 91 `candidate_release_asset_later`, and 9
`candidate_object_storage_later`, while keeping `migration_ready_now_count=0`
and authorizing no deletion, external upload, or history rewrite.
`artifacts/v3_artifact_admission_guard_1025.json` passes because all current
large noncanonical rows have manifest coverage; future large noncanonical rows
must be canonical evidence or get a producer/consumer manifest row before they
are acceptable. `docs/artifact_storage.md` now documents the source-only sparse
checkout path and the need to export the deploy-key `GIT_SSH_COMMAND` for the
whole session, including lazy blob fetches. Evidence-based confidence call: the
repo still carries the full artifact payload, but the next storage step is now
a human-reviewed migration decision or more provenance tightening for the 40
partially inferred rows, not artifact deletion or LFS/object-storage migration
by automation.

As of this manual infrastructure pass, artifact migration is being started
without deleting or externalizing any files. `docs/artifact_storage.md` defines
the no-information-loss rule: no artifact may leave Git unless a committed
manifest preserves path, size, SHA-256, category, producer/provenance,
downstream consumers, replacement storage location when applicable, and the
scientific conclusion in a canonical summary. The new inventory tooling writes
`artifacts/v3_artifact_storage_inventory_1025.json`, covering 2,574 artifact
files and 2.55 GiB of artifact payload at creation time. It classifies 102 files
as `canonical_evidence`, 358 as `regenerable_intermediate`, 760 as `raw_cache`,
and 1,354 as `compact_artifact`; 108 files are above the 5 MiB threshold. The
policy check in `artifacts/v3_artifact_storage_policy_check_1025.json` passes
with 0 blockers and 0 deletion authorizations. Evidence-based confidence call:
the repo still carries the bulky artifacts, but future agents now have a
non-lossy manifest/policy gate before any storage migration. Next infra work
should identify producer commands and downstream consumers for the largest
regenerable/cache artifacts before moving anything to LFS, release assets, or
object storage.

As of the 2026-05-17T17:01:40Z run, leakage-risk closure is now the active
handoff state. The original 10 selected external pilot candidates and repaired
lanes (`O14756`, `Q6NSJ0`, `P34949`, `Q9BXD5`, `C9JRZ8`, `P06746`, `P55263`,
`O60568`, `O95050`, and `P51580`) are recorded as development/review evidence
only in `artifacts/v3_external_pilot_repair_leakage_closure_1025.json`; they
must not be used as clean held-out performance proof after candidate-specific
repair. The next external hard-negative tranche is frozen before candidate
selection in
`artifacts/v3_external_hard_negative_next_tranche_preregistration_1025.json`
with the 8-fingerprint universe, `label_factory_v1_8fp`, threshold policy
`external_hard_negative_threshold_policy_v1_2026_05_17`, floor `0.4115`,
all-current-fingerprints-below-floor inverse gate, duplicate controls,
external-only structural-neighborhood rules, admissible source evidence,
excluded context, and success/failure criteria. Import gates can now be run
with `--require-pre-registration` to block next-tranche imports that do not
reference the frozen artifact/version.

Threshold provenance is documented in
`artifacts/v3_external_hard_negative_threshold_policy_1025.json`; candidate- or
tranche-specific threshold tuning is disallowed. Existing external hard
negatives (`uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3`) now carry
separated `predictive_evidence`, `import_gate_evidence`, `review_only_context`,
and `excluded_context` fields, and
`artifacts/v3_external_hard_negative_ontology_reaudit_policy_1025.json` requires
re-audit whenever the positive fingerprint universe expands, especially before
ePK, SDR, AKR, glycoside-hydrolase, isomerase, or lyase fingerprints. Evidence
based confidence call: the registry remains at 682 labels and the current
leakage controls are coherent; the next milestone should be infrastructure and
artifact strategy before ePK expansion or broad scale-up, not more M-CSA
strict-TM repair or repaired-pilot performance claims.

As of the 2026-05-17T15:41:11Z run, the project did not reopen the superseded
O14756/Q6NSJ0 import attempt. Instead, it opened a bounded post-P06744
review-only sourcing surface and ran the first sequence duplicate screens.
`artifacts/v3_external_hard_negative_post_p06744_sourcing_1025.json` excludes
the prior fresh, next-candidate, broader-structural, and P22830 deferral
surfaces, then selects six non-countable covered-lane rows: `P23921`, `P26439`,
`P09104`, `P13929`, `Q15084`, and `Q96JJ7`. The current-reference MMseqs2
screen and external all-vs-all sequence screen both report 6/6 no-signal rows
with guardrail-clean audits. The structural follow-up materializes all six
AlphaFold sidecars, completes the 15/15 external all-vs-all Foldseek cache, and
screens all six rows against current countable structures. Every row has a
high-TM current-countable duplicate signal, so
`artifacts/v3_external_hard_negative_post_p06744_terminal_decisions_1025.json`
records six terminal review-only duplicate rejections with 0 import-ready rows
and 0 countable candidates. Evidence-based confidence call: this surface is
closed by structural duplicate evidence; next work needs fresh sourcing rather
than retrying these six rows. Verification passed with 409 unit tests,
`validate` over 682 curated labels, `compileall`, and `git diff --check`.

As of the 2026-05-17T14:38:38Z verification run, the latest pushed repository
state supersedes the older O14756/Q6NSJ0 import-attempt prompt. The two-candidate
attempt is already terminally closed, `P06744`, `P78549`, and `Q3LXA3` are the
only external countable hard negatives, and the canonical registry remains at
682 labels: 212 seed-fingerprint positives and 470 out-of-scope labels.
Evidence-based confidence call: the current state is coherent and should not
reopen O14756/Q6NSJ0, P22830, the broader duplicate-signal rejects, the six
original pilot repair lanes, or M-CSA strict TM repair without explicit new
evidence. Startup verification passed with 405 unit tests and `validate` over
682 curated labels. `docs/label_factory.md` was corrected to match the current
682-label state.

As of the 2026-05-17T13:37:34Z run, `P06744` is imported as the third external
out-of-scope hard-negative label. Evidence-based confidence call: the import is
defensible under the current 8-fingerprint ontology because terminal review,
bounded duplicate controls, targeted and current-reference UniRef90/50 checks,
current-countable Foldseek screening, all-8 inverse-gate scoring, the baseline
label-factory gate, and the external-transfer gate all pass. The canonical
registry now has 682 labels: 679 accepted M-CSA labels, 212 seed-fingerprint
positives, and 470 out-of-scope labels including `uniprot:P06744`,
`uniprot:P78549`, and `uniprot:Q3LXA3`.

New artifacts:
`artifacts/v3_external_hard_negative_broader_structural_terminal_review_decisions_1025.json`
records `P06744` as `accepted_out_of_scope_pending_factory_gate`, and
`artifacts/v3_external_hard_negative_broader_structural_factory_import_gate_1025.json`
selects exactly `P06744` under a single-import cap while allowing the two prior
external labels only as lineage. Post-import regression expectations were
updated to 682 total labels and 470 out-of-scope labels. Next direct work should
avoid reopening the five broader-surface duplicate-signal rejects and should
source or screen a fresh structurally lower-risk external hard-negative surface
only if another explicit import cycle is requested.

As of the 2026-05-17T01:23:28Z run, the first external hard-negative import
attempt is closed without count growth. Evidence-based confidence call: the
external out-of-scope inverse gate is now explicit and test-covered for the
current 8-fingerprint ontology, but neither O14756 nor Q6NSJ0 is defensible as
an import-ready hard negative because duplicate, post-repair review, and full
factory gates still block them.

`MechanismLabel` now carries `ontology_version_at_decision`, with existing
registry labels migrated to `label_factory_v1_8fp`. External terminal and
post-repair decision artifacts now carry `target_label_type=out_of_scope`,
`target_fingerprint_id=null`, and the same ontology version so future ontology
expansion cannot retroactively change this hard-negative decision surface.
`artifacts/v3_external_out_of_scope_inverse_gate_logic_check_1025.json` records
Step 1A as passed: curated out-of-scope labels still reject non-null
fingerprints and above-threshold retained hits, and the O14756/Q6NSJ0 external
post-repair paths require all 8 current fingerprint scores below the active
`0.4115` floor. `artifacts/v3_external_sdr_ec_1_1_1_consistency_check_1025.json`
records Step 1B as passed on the bounded SDR check: 36/36 evaluable SDR-like
Swiss-Prot EC 1.1.1.x rows were clean abstentions, with 0 SDR false
non-abstentions and 0 predictive text/annotation leakage rows.

`artifacts/v3_external_hard_negative_two_candidate_import_attempt_1025.json`
then tried exactly the requested two candidates. O14756 passes the inverse gate
with top1 `heme_peroxidase_oxidase` score `0.3039`; Q6NSJ0 passes with top1
`metal_dependent_hydrolase` score `0.3552`. Both rows remain
`import_blocked`, `import_ready_candidate=false`, and non-countable because
broader duplicate screening, terminal post-repair review acceptance, and the
full external factory gate are unresolved. Do not try P34949, Q9BXD5, C9JRZ8,
P06746, or any third original pilot candidate in this cycle.

Because both first candidates failed strict readiness,
`artifacts/v3_external_hard_negative_second_tranche_selection_1025.json` starts
the next review-only hard-negative tranche with P33025, Q13907, and P35914 as
lower-risk candidates. P60174 is explicitly excluded for high
current-reference identity (`0.899`), and Q9BXS1 is excluded because Q13907
already represents the same external `TM >= 0.7` cluster. These tranche-2 rows
are not import-ready and not countable. The 2026-05-17T02:23:59Z run then
added
`artifacts/v3_external_hard_negative_second_tranche_current_countable_structural_screen_1025.json`,
which runs Foldseek over those 3 external rows against 672 staged current
selected structures. Foldseek completed, but only 2001/2016 query-target pairs
were reported and all three admitted rows have high-TM current-countable
structural signals: P33025 to `m_csa:735` at `0.7063`, Q13907 to `m_csa:190`
at `0.8686`, and P35914 to `m_csa:328` at `0.7638`. Evidence-based confidence
call: tranche-2 import readiness is now lower, not higher.
`artifacts/v3_external_hard_negative_second_tranche_terminal_decisions_1025.json`
records all three admitted rows as terminal review-only
`rejected_current_countable_structural_duplicate_signal` outcomes with 0
import-ready rows and 0 countable labels.
`artifacts/v3_external_hard_negative_second_tranche_replacement_triage_1025.json`
then triages the current 25-row pool and admits 0 replacements. Next direct
work has now moved to fresh external sourcing rather than reconsidering this
pool; do not retry P33025/Q13907/P35914 or reopen
O14756/Q6NSJ0/P34949/Q9BXD5/C9JRZ8/P06746 repair lanes in this cycle without
new expert evidence. The 2026-05-17T03:25:01Z run added
`artifacts/v3_external_hard_negative_new_candidate_sourcing_1025.json`, a
review-only expanded Swiss-Prot sourcing pass. It excludes the current external
pool, keeps only covered mechanism lanes, and finds 8 new rows with explicit
UniProt active-site and catalytic-activity context: `O75828`, `O95154`,
`O95479`, `P04424`, `Q8N0X4`, `P30566`, `Q04760`, and `Q13087`. Evidence-based
confidence call: this removes the immediate "no new candidates" sourcing
blocker, but it does not create an import-ready tranche. Every sourced row
still needs duplicate/review/factory evidence before any import attempt. The
same run also added
`artifacts/v3_external_hard_negative_new_candidate_backend_sequence_search_1025.json`
and its audit for those 8 rows. The MMseqs2 current-reference screen is
complete and guardrail-clean: 7 rows have no near-duplicate signal, while
`Q04760` is an exact-reference holdout to `m_csa:32`; do not carry `Q04760`
into an import attempt.
`artifacts/v3_external_hard_negative_new_candidate_structural_cluster_index_1025.json`
already covers the external all-vs-all side for the 8 sourced rows: all 8
AlphaFold coordinate sidecars are staged, 28/28 unordered Foldseek pairs are
covered, and only `P04424`/`P30566` cluster at `TM >=0.7` (`0.8338`).
`artifacts/v3_external_hard_negative_new_candidate_current_countable_structural_screen_1025.json`
now screens the 7 sequence no-signal rows against 672 current countable
selected structures. The 2026-05-17T04:26:35Z run fixed the Foldseek
multi-model target alias mapper (`pdb_1MEK_MODEL_37_A` now maps back to
`pdb_1MEK`) and reran the screen. The pair cache is now complete at 4704/4704
unique query-target pairs, and all 7 sequence-clean rows have high-TM
current-countable duplicate signals. `Q13087` is no longer a viable no-signal
candidate: its completed-cache nearest current-countable hit is selected
structure `1MEK` at `TM=0.9039`. The new
`artifacts/v3_external_hard_negative_new_candidate_terminal_decisions_1025.json`
artifact records all 7 rows as terminal review-only
`rejected_current_countable_structural_duplicate_signal` outcomes, with 0
import-ready rows and 0 countable labels. Evidence-based confidence call: the
fresh sourced tranche is closed by current-countable structural duplicate
signals, not by an unresolved process blocker. The 2026-05-17T05:28:04Z run
then opened the next replacement sourcing surface without retrying those rows.
`artifacts/v3_external_hard_negative_next_candidate_sourcing_1025.json`
excludes the original 30-row pool, the second-tranche duplicate rejects, and
all 8 prior fresh sourced rows, then admits 8 replacement covered-lane
Swiss-Prot rows with explicit UniProt active-site plus catalytic-activity
context: `P00338`, `P04406`, `P14060`, `Q9GZT4`, `P22830`, `Q8TB92`,
`P78549`, and `Q3LXA3`. The bounded current-reference MMseqs2 screen
`artifacts/v3_external_hard_negative_next_candidate_backend_sequence_search_1025.json`
and audit record 8/8 no-signal rows, 0 exact-reference holdouts, 0
near-duplicate rows, and 0 import-ready/countable rows. The same run also
staged the replacement structural surface:
`artifacts/v3_external_hard_negative_next_candidate_structural_cluster_index_1025.json`
materializes 8/8 AlphaFold sidecars, covers 28/28 external all-vs-all Foldseek
pairs, and finds 0 high-TM external pairs.
`artifacts/v3_external_hard_negative_next_candidate_current_countable_structural_screen_1025.json`
then completes the current-countable Foldseek screen over 5376/5376
query-target pairs. Five rows have high-TM current-countable duplicate signals
(`P00338`, `P04406`, `P14060`, `Q8TB92`, and `Q9GZT4`), while `P22830`,
`P78549`, and `Q3LXA3` have no current-countable structural duplicate signal at
`TM >=0.7`. `artifacts/v3_external_hard_negative_next_candidate_terminal_decisions_1025.json`
records 5 review-only duplicate-signal rejections and 3 review-only deferrals
that initially remain blocked by UniRef-wide duplicate screening, terminal
review, and full factory gates. Evidence-based confidence call: the immediate
no-new-candidates blocker is removed and this surface has 3 structurally
non-duplicate follow-up rows, but none is import-ready or countable yet.
The 2026-05-17T06:29:04Z run then added
`artifacts/v3_external_hard_negative_next_candidate_all_vs_all_sequence_search_1025.json`
and
`artifacts/v3_external_hard_negative_next_candidate_all_vs_all_sequence_search_audit_1025.json`.
The bounded external all-vs-all sequence screen covers the same 8 replacement
rows, completes with 8/8 no-signal rows, finds 0 exact/near-duplicate external
sequence pairs, and remains guardrail-clean while preserving the UniRef-wide
blocker. The new
`artifacts/v3_external_hard_negative_next_candidate_duplicate_evidence_review_1025.json`
narrows the surviving surface to `P22830`, `P78549`, and `Q3LXA3`: all 3 are
`bounded_duplicate_controls_clear_uniref_pending`, meaning bounded
current-reference sequence, external all-vs-all sequence, external structural,
and current-countable structural controls are clear. Evidence-based confidence
call: these 3 rows are now better duplicate-screened than the previous
replacement surface, but at this stage none is import-ready because UniRef-wide
duplicate screening, terminal review acceptance, and full factory gates still
block all 3. The same run also added
`artifacts/v3_external_hard_negative_next_candidate_terminal_review_queue_1025.json`,
which packages those 3 rows into review-only terminal review packets with
explicit allowed outcomes and remaining non-human blockers; it accepts/imports
0 rows. The follow-on
`artifacts/v3_external_hard_negative_next_candidate_targeted_uniref_check_1025.json`
queries UniRef90/50 handles for each queued candidate and its nearest current
structural-reference accession. `P22830` vs `P00518`, `P78549` vs `P00750`,
and `Q3LXA3` vs `P06213` have 0 shared UniRef90/50 clusters and 0 fetch
failures. The 2026-05-17T07:29:36Z run then added
`artifacts/v3_external_hard_negative_next_candidate_uniref_current_reference_screen_1025.json`,
which fetches each candidate's UniRef90 and UniRef50 cluster members and
intersects them with all 735 current countable reference accessions. `P22830`,
`P78549`, and `Q3LXA3` all have 0 current-reference cluster overlaps, with 6/6
candidate UniRef clusters fetched successfully. Evidence-based confidence call:
the surviving next-candidate surface no longer has a current-reference UniRef
cluster duplicate blocker. The 2026-05-17T08:31:07Z run then added
`artifacts/v3_external_hard_negative_next_candidate_inverse_gate_scores_1025.json`,
which maps the UniProt active-site features for those 3 rows onto their staged
AlphaFold sidecars and verifies complete 8/8 current-fingerprint coverage below
the `0.4115` out-of-scope floor: `P22830` top1 `metal_dependent_hydrolase`
`0.3686`, `P78549` top1 `flavin_dehydrogenase_reductase` `0.1150`, and
`Q3LXA3` top1 `metal_dependent_hydrolase` `0.2929`. The companion
`artifacts/v3_external_hard_negative_next_candidate_terminal_review_decisions_1025.json`
records all 3 as review-only
`accepted_out_of_scope_pending_factory_gate` decisions. Evidence-based
confidence call: terminal review acceptance is resolved for this surface. The
same run then added
`artifacts/v3_external_hard_negative_next_candidate_factory_import_gate_1025.json`.
All 3 rows pass the candidate factory gate; the single-import cap selects
`P78549` because its maximum current-fingerprint score is lowest (`0.1150`).
The accepted review item imports `uniprot:P78549` as an external
`out_of_scope` hard-negative label with `fingerprint_id=null` and
`ontology_version_at_decision=label_factory_v1_8fp`, bringing the canonical
registry to 680 countable labels. `P22830` and `Q3LXA3` remain unimported under
`single_import_cap_not_selected_this_run`. The post-import litmus regression
now pins 680 total labels, 468 out-of-scope labels, 212 seed-fingerprint
labels, no overlap between in-scope and out-of-scope entry ids, unchanged
1,000-slice in-scope retention (`0.9858`), held-out sequence identity
`<=0.284`, 43/43 retained held-out positives correct, and 0 held-out
out-of-scope false non-abstentions. The 2026-05-17T09:32:49Z run then added
`artifacts/v3_external_hard_negative_next_candidate_followup_cycle_decision_1025.json`.
Evidence-based confidence call: the post-import litmus remains green, `P22830`
and `Q3LXA3` are both eligible only for a later explicit single-import cycle,
and `Q3LXA3` is the recommended next review target because its maximum
current-fingerprint score is lower (`0.2929` versus `0.3686`). No second
external label was imported in this run. Next work should either open that
explicit Q3LXA3 single-import cycle under the same gates and cap, or switch to
a broader external structural surface; do not retry the 5 duplicate-signal
rows without new evidence.

The 2026-05-17T10:34:03Z run opened that explicit later single-import cycle.
`artifacts/v3_external_hard_negative_q3lxa3_single_import_cycle_gate_1025.json`
allows the prior `uniprot:P78549` import only as lineage and selects exactly
`Q3LXA3`. The row passes terminal review, bounded duplicate evidence, UniRef
current-reference screening, complete 8/8 out-of-scope inverse-gate scoring
below `0.4115`, the baseline label-factory gate, and the external transfer
gate. The accepted review item imports `uniprot:Q3LXA3` as an external
`out_of_scope` hard-negative label with `fingerprint_id=null` and
`ontology_version_at_decision=label_factory_v1_8fp`, bringing the canonical
registry to 681 countable labels: 212 seed fingerprints and 469 out-of-scope
labels. `artifacts/v3_external_hard_negative_q3lxa3_post_import_followup_cycle_decision_1025.json`
records the post-Q3LXA3 litmus as green and leaves `P22830` as the only
remaining factory-pass row eligible for a future explicit cycle. Evidence-based
confidence call: the second external import is defensible under the current
8-fingerprint ontology, but further count growth should not be automatic;
`P22830` has a much narrower margin to the `0.4115` floor (`0.3686`) and should
either receive its own explicit cycle or be deferred in favor of broader
external structural sourcing.

The 2026-05-17T11:35:39Z run made that explicit go/no-go decision without
changing registry counts. A temporary later-cycle gate probe selected P22830,
confirming that the formal terminal-review, duplicate, UniRef current-reference,
inverse-gate, label-factory, and external-transfer checks would pass for an
explicit import cycle. `artifacts/v3_external_hard_negative_p22830_cycle_deferral_1025.json`
nevertheless defers the row before import because its maximum current-fingerprint
score is `0.3686`, only `0.0429` below the active `0.4115` out-of-scope floor,
after two external hard-negative imports are already countable. Evidence-based
confidence call: preserving the 681-label registry and switching to broader
external structural sourcing is the safer next step than taking automatic third
count growth from the last remaining factory-pass row. `docs/label_factory.md`
was checked and still needs no content change for this decision-only slice.
As a remaining-time probe, the run also reran the existing next-candidate
sourcing command with the two prior sourced surfaces merged as an exclusion set
in `/private/tmp`. It found eight review-only source-evidence rows
(`P14550`, `P15428`, `P23921`, `P26439`, `P28330`, `P30838`, `P31040`, and
`P36959`), but all eight came from `external_source:oxidoreductase_long_tail`.
That raw probe artifact was not committed because its lineage pointed to a
temporary merged-prior file. Next direct work should add a durable
multi-prior/lane-balanced broader structural sourcing path, or explicitly
decide that an oxidoreductase-only surface is acceptable before running
sequence and structural duplicate screens.

The 2026-05-17T12:37:08Z run added that durable path without opening any import
attempt. `artifacts/v3_external_hard_negative_broader_structural_sourcing_1025.json`
merges the original 30-row pool, second-tranche terminal rejects, both prior
fresh sourced surfaces, both prior terminal-decision artifacts, and the explicit
P22830 deferral into one reproducible exclusion surface. It then applies a
two-per-lane cap and selects six review-only source-evidence rows across three
covered lanes: `P14550` and `P15428` from oxidoreductase_long_tail, `Q969S2`
and `Q96FI4` from lyase, and `P06744` and `Q9BV20` from isomerase. Evidence-based
confidence call: the previous one-lane probe is no longer the active sourcing
blocker.

The same run then advanced the six rows through the first bounded duplicate
screens. `artifacts/v3_external_hard_negative_broader_structural_backend_sequence_search_1025.json`
records 6/6 no-signal rows against the current countable reference FASTA.
`artifacts/v3_external_hard_negative_broader_structural_all_vs_all_sequence_search_1025.json`
finds 0 exact/near-duplicate sequence pairs within the six-row broader surface.
`artifacts/v3_external_hard_negative_broader_structural_cluster_index_1025.json`
materializes all six AlphaFold sidecars, covers 15/15 external all-vs-all
Foldseek pairs, and finds 0 high-TM external pairs. The current-countable
screen
`artifacts/v3_external_hard_negative_broader_structural_current_countable_structural_screen_1025.json`
completes 4,032/4,032 query-target pairs: five rows have high-TM
current-countable structural duplicate signals, and only `P06744` has no
current-countable structural duplicate signal. `artifacts/v3_external_hard_negative_broader_structural_terminal_decisions_1025.json`
therefore rejects `P14550`, `P15428`, `Q969S2`, `Q96FI4`, and `Q9BV20` as
review-only duplicate-signal rows and defers `P06744` behind UniRef-wide
duplicate screening, terminal review acceptance, inverse-gate/factory evidence,
and the full import gate. Follow-on `P06744` artifacts record clear bounded
duplicate evidence, a targeted UniRef90/50 nearest-reference no-shared-cluster
result, a UniRef90/50 current-reference screen with 0 current-reference
overlaps, and an all-8 out-of-scope inverse-gate pass with top1
`metal_dependent_hydrolase` score `0.3066`. Evidence-based confidence call: the
broader surface had one surviving no-current-structural-signal row, and its
duplicate/inverse-gate blockers were narrowed before the later terminal
review/factory import completed for `P06744`; do not retry the five
duplicate-signal rows without new evidence.

Run verification for the current handoff: started `2026-05-17T12:37:08Z` and
wrapped at `2026-05-17T13:25:07Z`. Startup checks passed with 400 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 404 unit tests, `validate` over 681 curated labels, `compileall`,
and `git diff --check`. README, `docs/external_source_transfer.md`,
`docs/label_factory.md`, work scope, handoff, status, progress log, and
external transfer notes were checked or updated. No registry import was made.

Run verification for the current handoff: started `2026-05-17T10:34:03Z` and
wrapped at `2026-05-17T10:49:59Z`. Startup checks passed with 395 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 399 unit tests, `validate` over 681 curated labels, `compileall`,
`git diff --check`, JSON parse checks for the new Q3LXA3 artifacts and
registry summary, and the external transfer gate at 68/68. README,
`docs/external_source_transfer.md`, `docs/label_factory.md`, work scope,
handoff, status, progress log, and external transfer notes were checked or
updated.

Run verification for the current handoff: started `2026-05-17T09:32:49Z` and
wrapped at `2026-05-17T09:41:38Z`. Startup checks passed with 393 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 395 unit tests, `validate`, `compileall`, `git diff --check`, JSON
parse check for the follow-up artifact, and the external transfer gate at
68/68. README, `docs/external_source_transfer.md`, `docs/label_factory.md`,
work scope, handoff, status, progress log, and external transfer notes were
checked or updated; no registry import was made.

Run verification for the current handoff: started `2026-05-17T08:31:07Z` and
wrapped at `2026-05-17T09:08:30Z`. Startup checks passed with 388 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 393 unit tests, `validate` over 680 curated labels, `compileall`,
`git diff --check`, JSON parse checks for the new inverse-gate/terminal/factory
artifacts and imported registry, and the already-rerun external transfer gate at
68/68. README, `docs/external_source_transfer.md`, `docs/label_factory.md`,
work scope, handoff, status, progress log, and external transfer notes were
updated to reflect the first external hard-negative import.

Run verification for the previous handoff: started `2026-05-17T07:29:36Z` and
wrapped at `2026-05-17T07:42:26Z`. Startup checks passed with 386 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 388 unit tests, `validate`, `compileall`, `git diff --check`, JSON
parse checks for the new UniRef current-reference screen, the focused scaling
artifact regression, and the external transfer gate still at 68/68. README,
`docs/external_source_transfer.md`, work scope, handoff, status inputs, and
external transfer notes were updated; `docs/label_factory.md` was checked and
did not need content changes for this duplicate-screen slice.

Run verification for the current handoff: started `2026-05-17T06:29:04Z` and
wrapped at `2026-05-17T06:47:24Z`. Startup checks passed with 383 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 386 unit tests, `validate`, `compileall`, `git diff --check`, JSON
parse checks for the new all-vs-all sequence, duplicate-evidence,
terminal-review-queue, and targeted-UniRef artifacts, plus focused artifact
regressions. README, `docs/external_source_transfer.md`, work scope, handoff,
status inputs, and external transfer notes were updated; `docs/label_factory.md`
was checked and did not need content changes for this duplicate-screen/review
slice.

Run verification for the current handoff: started `2026-05-17T05:28:04Z` and
wrapped at `2026-05-17T06:09:30Z`. Startup checks passed with 382 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 383 unit tests, `validate`, `compileall`, `git diff --check`, JSON
parse checks for the new sourcing/sequence/structural/terminal artifacts, and
the external transfer gate still at 68/68. README,
`docs/external_source_transfer.md`, `docs/label_factory.md`, work scope,
handoff, status inputs, and external transfer notes were checked; label-factory
docs required no content change for this replacement-sourcing slice.

Run verification for the current handoff: started `2026-05-17T03:25:01Z`.
Startup checks passed with 378 unit tests and `PYTHONPATH=src python -m
catalytic_earth.cli validate`. Final checks passed with 380 unit tests,
`validate`, `compileall`, `git diff --check`, JSON parse checks for the new
sourcing/sequence/structural artifacts, coordinate digest rechecks after CIF
whitespace normalization, focused artifact regressions, and the external
transfer gate still at 68/68. README, `docs/external_source_transfer.md`, work
scope/handoff/status inputs, and external transfer notes were updated;
`docs/label_factory.md` was checked and did not need content changes for this
sourcing/duplicate-screen slice.

Run verification for the current handoff: started `2026-05-17T02:23:59Z` and
wrapped at `2026-05-17T02:50:16Z`. Startup checks passed with 376 unit tests
and `PYTHONPATH=src python -m catalytic_earth.cli validate`; final checks
passed with 378 unit tests, `validate`, `compileall`, `git diff --check`, JSON
parse checks for the new hard-negative artifacts, and the external transfer
gate remaining at 68/68. README, label-factory docs, external-transfer docs,
scope, handoff, and repair/transfer notes were checked; label-factory docs
required no content change for this structural duplicate-screen slice.

As of the 2026-05-16T01:55:26-05:00 run, do not resume M-CSA strict
Foldseek/TM-score repair. The loop is closed/deferred by
`artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json`, with
`full_tm_score_holdout_claim_permitted=false`, max all-materializable
train/test TM-score `0.9749`, 4,715 target-violating train/test rows,
108 high-TM partition constraints, and 38 sequence-identity partition
constraints. Noncanonical staged, expanded, query-chunk, query-single,
target-shard, split-repair, split-redesign, and cluster-first round artifacts
were removed after their summary was captured; they are not continuation
targets.

The external pilot terminal-decision pass now exists in
`artifacts/v3_external_source_pilot_terminal_decisions_1025.json`. It covers
the 10 selected candidates with exactly one terminal status each: 4
`rejected_duplicate_or_near_duplicate`, 3
`rejected_active_site_evidence_missing`, and 3
`deferred_requires_human_expert`, with 0 import-ready rows and 0 countable
external labels. The 3 deferred rows are now routed by
`artifacts/v3_external_source_pilot_human_expert_review_queue_1025.json`:
`O14756`, `P34949`, and `Q6NSJ0` each have a review-only expert question,
automation limitation, and remaining non-human blockers. The terminal-decision
confidence audit now exists in
`artifacts/v3_external_source_pilot_decision_confidence_audit_1025.json`: it
checks all 10 selected rows against active-site, duplicate/near-duplicate,
representation, heuristic, review, structure, transfer-gate, and factory-gate
evidence, keeps 4 current decisions confident, marks 3 current hard
representation-only duplicate rejections low-confidence, and keeps 3 rows in
needs-review status. The normalized companion
`artifacts/v3_external_source_pilot_decisions_review_normalized_1025.json`
records 6 `needs_review`, 3 `rejected_active_site_evidence_missing`, and 1
`rejected_duplicate_or_near_duplicate` decision; the normalized queue
`artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_1025.json`
routes all 6 needs-review rows (`O14756`, `P06746`, `C9JRZ8`, `P34949`,
`Q9BXD5`, and `Q6NSJ0`) with exact unresolved questions. All three audit and
normalization artifacts are review-only, with 0 import-ready rows and 0
countable external labels. The 2026-05-16T15:04:24Z run then added
`artifacts/v3_external_source_pilot_needs_review_resolution_1025.json`,
`artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json`, and
`artifacts/v3_external_source_pilot_human_expert_review_queue_resolved_1025.json`.
That desk review checked local active-site, reaction, sequence, representation,
heuristic, and structural artifacts plus UniProtKB/UniRef90/UniRef50 source
context. Targeted UniRef90/50 mapping found 0 shared candidate/current-reference
clusters for the nearest-reference checks, so duplicate rejection is not
supported, but all 6 rows are terminal review-only
`rejected_representation_conflict` import-safety decisions because current
representation or heuristic controls conflict with source-supported chemistry.
The resolved decision surface has 0 `needs_review`, 0 import-ready rows, and 0
countable external labels.
`artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json` now
turns those six review-only representation conflicts into named
representation/heuristic repair lanes: SDR/NAD(P) redox, AKR/NADP redox, DNA
Pol X/5'-dRP lyase, sugar-phosphate isomerase, Schiff-base lyase/aldolase, and
glycoside-hydrolase versus metal-hydrolase boundary control. These lanes
remove the generic zero-pass repair ambiguity but are not predictive features,
import-ready decisions, or countable labels.
`artifacts/v3_external_source_pilot_sdr_redox_repair_control_1025.json` now
implements the first bounded repair-lane control for `O14756`. It stages only
sequence-derived SDR/NAD(P) evidence: a `TGxxxGxG` glycine-rich proxy plus a
source-active-site-overlapping `YxxxK` proxy, then contrasts that complete SDR
axis against the conflicting current-reference neighbors. Those neighbors lack
the complete SDR axis. The follow-on
`artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_1025.json`
now consumes that non-text control in the import-safety path. It repairs the
O14756 representation-conflict blocker and records the post-repair normalized
status as `needs_review`, but it still creates 0 import-ready rows and 0
countable external labels because broader duplicate screening, a post-repair
review decision, and the full factory gate remain unresolved.
`artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json`
now opens the next repair lane for `Q6NSJ0` as review-only control evidence.
It stages source-traced acidic active-site residues, active-site spacing, local
pocket composition, absent local metal/cofactor ligand context, and zero
metal-hydrolase role-hint support as a non-text boundary control. The follow-on
`artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_1025.json`
now consumes that control in the import-safety path. It repairs the Q6NSJ0
representation/heuristic boundary blocker and records the post-repair
normalized status as `needs_review`, but it still creates 0 import-ready rows
and 0 countable external labels because broader duplicate screening, a
post-repair review decision, and the full factory gate remain unresolved.
`artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_control_1025.json`
now opens the next P34949 repair lane as review-only scope-control evidence.
It uses the source-traced active-site Arg, local pocket composition, absent
flavin/cofactor context, zero flavin role-hint support, and weak top1 score
with local `absent_flavin_context` counterevidence to separate
mannose-6-phosphate isomerase scope from the weak flavin-redox heuristic top1.
The follow-on
`artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_import_safety_adjudication_1025.json`
now consumes that control in the import-safety path. It repairs the P34949 weak
flavin/scope representation blocker and records the post-repair normalized
status as `needs_review`, but it still creates 0 import-ready rows and 0
countable external labels because broader duplicate screening, a post-repair
review decision, and the full factory gate remain unresolved.
`artifacts/v3_external_source_pilot_schiff_base_lyase_control_1025.json` now
opens the next Q9BXD5 repair lane as review-only scope-control evidence. It
uses source-traced Tyr/Lys active-site residues, a Schiff-base Lys, local
pocket composition, absent heme/cofactor context, zero heme/electron-transfer
role-hint support, and weak top1 score with local `absent_heme_context`
counterevidence to separate N-acetylneuraminate lyase scope from the weak
heme-peroxidase heuristic top1. The follow-on
`artifacts/v3_external_source_pilot_schiff_base_lyase_import_safety_adjudication_1025.json`
now consumes that control in the import-safety path. It repairs the Q9BXD5 weak
heme/scope blocker and records the post-repair normalized status as
`needs_review`, but it still creates 0 import-ready rows and 0 countable
external labels because the representation near-duplicate holdout, broader
duplicate screening, a post-repair review decision, and the full factory gate
remain unresolved.
The external structural pilot path has now moved from path definition to a concrete
review-only structure cache in
`artifacts/v3_external_structural_cluster_index_1025.json`: all 10 selected
AlphaFold coordinate sidecars are materialized, Foldseek completed, the nearest
neighbor cache covers 10/10 candidates, and pre-split clustering at `TM >=0.7`
finds one high-TM pair (`O95050`/`P51580`) across nine clusters. This is not a
train/test split and keeps 0 countable/import-ready rows. The broader external
structural surface now exists in
`artifacts/v3_external_structural_tm_holdout_path_1025_all30.json` and
`artifacts/v3_external_structural_cluster_index_1025_all30.json`: all 30
current external candidates have AlphaFold sidecars, Foldseek nearest-neighbor
coverage is 30/30, the all-vs-all Foldseek cache now covers 435/435 unordered
nonself pairs, and the pre-split cache finds 6 high-TM pairs across 26
clusters. `artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json`
now removes the split-assignment blocker with a review-only cluster-preserving
split: 6 test and 24 train candidates, one test candidate from each external
lane, 144/144 cross-split pairs checked, max cross-split TM-score `0.6963`,
and 0 cross-split pairs at `TM >=0.7`. This is not an import-ready benchmark
claim; every external row remains non-countable. The 2026-05-16T13:02:29Z
audit-verification run reran the confidence, normalization, and normalized
queue builders idempotently and found no defensible local-evidence-only
resolution for the 6 normalized `needs_review` rows. The 2026-05-16T09:03:56-05:00
run then added `artifacts/v3_external_source_all_vs_all_sequence_search_1025.json`
and `artifacts/v3_external_source_all_vs_all_sequence_search_audit_1025.json`:
MMseqs2 searched all 30 external candidates against each other, found 0
near-duplicate pairs at 90% identity / 80% coverage, recorded max reported
external-external identity `0.647`, and kept 0 import-ready/countable rows. The
confidence audit now carries this external all-vs-all no-signal evidence for
the selected pilot rows. The later needs-review resolution, mechanism repair
lane, SDR control, SDR import-safety adjudication, Q6NSJ0 boundary
adjudication, P34949 sugar-phosphate isomerase control, P34949 import-safety
adjudication, Q9BXD5 Schiff-base lyase control, and Q9BXD5 import-safety
adjudication artifacts supersede the 6-row normalized queue for pilot-decision
work; do not re-open those rows without new evidence. The 2026-05-16T17:49:33-05:00
run then added `artifacts/v3_external_source_pilot_akr_nadp_repair_control_1025.json`
and
`artifacts/v3_external_source_pilot_akr_nadp_import_safety_adjudication_1025.json`.
The C9JRZ8 control uses only non-text sequence/local evidence: a `VGLG`
cofactor-binding proxy, source-traced active-site Tyr, local H/K context, and
current-reference contrast rows lacking the complete AKR/NADP axis. The
import-safety adjudication repairs the C9JRZ8 representation near-duplicate
conflict and records post-repair `needs_review`, but import remains blocked by
`heuristic_control_not_scored`, broader duplicate screening, post-repair review
decision, and full factory gates. Next direct work should complete remaining
duplicate/review/factory blockers for repaired external rows if a defensible
full path exists. The 2026-05-16T23:51:02Z run then added
`artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_1025.json`
and
`artifacts/v3_external_source_pilot_dna_pol_x_lyase_import_safety_adjudication_1025.json`.
The P06746 control uses only non-text sequence/local evidence:
source-active-site Lys-72, local basic/acidic sequence context, and
current-reference contrast rows lacking the complete DNA Pol X/5'-dRP lyase
axis. The import-safety adjudication repairs the P06746 representation
near-duplicate conflict and records post-repair `needs_review`, but import
remains blocked by `heuristic_control_not_scored`, broader duplicate screening,
post-repair review decision, and full factory gates. Do not broaden dashboards
or generic gates before resolving a specific import blocker.
Do not open M-CSA round33, staged index 145 continuation, or more partition repair
unless the user explicitly reverses the override.

GitHub credential hygiene has been moved off the unstable HTTPS path. Local
`main` is aligned with `origin/main` after pushing the P06746 DNA Pol X/5'-dRP
lyase repair lane. The root cause was that scheduled shells could see the
`gh auth git-credential` helper but could not read a valid `gh` token or any
HTTPS credential noninteractively, so `git credential fill`, `git push
--dry-run origin main`, and `git push origin main` all failed with
`fatal: could not read Username for 'https://github.com': Device not
configured`. Recovery created a repo-scoped read-write GitHub deploy key
(`~/.ssh/catalytic_earth_deploy_ed25519`), added it to
`VivekVardhanArrabelli/catalytic-earth`, changed `origin` to
`git@github.com:VivekVardhanArrabelli/catalytic-earth.git`, and set the
worktree-local `core.sshCommand` to use that key with `BatchMode=yes`. Future
agents should push over SSH and should not return to HTTPS/`gh auth` repair
unless the deploy key is explicitly removed.

## Start-of-Run Confidence Call

Recorded for the 2026-05-17T02:23:59Z run after acquiring the automation lock,
syncing clean `origin/main`, verifying the SSH deploy-key push path, and
passing startup gates (`376` unit tests and `validate` with 679 curated
labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, no M-CSA strict-TM repair path was reopened, and the
  work stayed on external fold-diverse hard-negative blockers.
- External-source repair/import: Yes for bounded duplicate-screen evidence, no
  for import or countable labels. The tranche-2 current-countable structural
  screen finds high-TM current selected-structure signals for P33025, Q13907,
  and P35914; the terminal decision artifact rejects all three as review-only
  duplicate-risk outcomes, leaving 0 import-ready rows and 0 countable external
  labels.
- Scientific generalization work: Yes, but review-only. The new Foldseek screen
  compares three external candidates to 672 staged current selected structures;
  it is duplicate-risk evidence, not a new benchmark split or validated enzyme
  function claim.
- SPOF hardening work: Yes. A direct CLI/function/test path now records the
  current-countable structural duplicate screen that the previous handoff
  identified as a blocker for second-tranche import readiness.

Recorded for the 2026-05-16T23:51:02Z run after acquiring the automation lock,
syncing clean `origin/main`, verifying that `gh auth status` remains invalid
and the scheduled shell cannot fill GitHub credentials noninteractively,
passing startup gates (`370` unit tests passed and `validate` passed with 679
curated labels), passing focused external-pilot artifact tests (`106` tests),
and preserving the current safe local commit after push failed with the HTTPS
username/device error:

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for the final current review-only
  import-safety adjudication lane, no for import or countable labels. The
  P06746 DNA Pol X/5'-dRP lyase control consumes source-active-site Lys-72,
  local basic/acidic sequence context, current-reference contrast rows lacking
  the complete axis, and bounded sequence no-signal status. It repairs the
  representation near-duplicate conflict and records post-repair
  `needs_review`, but the row still requires heuristic scoring, broader
  duplicate screening, a post-repair review decision, and full factory gates
  before any import claim.
- Scientific generalization work: No new benchmark or split claim. The all-30
  external structural split remains review-only with max cross-split TM about
  `0.6963`; strict TM-diverse claims remain on external fold-diverse surfaces
  only.
- SPOF hardening work: Yes. New CLI paths, artifacts, and regression tests make
  the P06746 DNA Pol X/5'-dRP lyase post-repair import-safety decision path
  executable while preserving review-only/countable-label separation.

Recorded for the 2026-05-16T17:49:33-05:00 run after acquiring a stale-lock
recovery lock, syncing with `origin/main`, verifying the GitHub credential
helper is installed but the `gh` token is invalid, passing startup gates (`368`
unit tests passed and `validate` passed with 679 curated labels), and passing
focused AKR artifact tests plus final full tests (`370` unit tests and
`validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for one additional review-only
  import-safety adjudication lane, no for import or countable labels. The
  C9JRZ8 AKR/NADP control consumes a sequence-derived `VGLG` cofactor-binding
  proxy, source-traced active-site Tyr, local H/K context, current-reference
  contrast rows lacking the complete AKR/NADP axis, and bounded sequence
  no-signal status. It repairs the representation near-duplicate conflict and
  records post-repair `needs_review`, but the row still requires heuristic
  scoring, broader duplicate screening, a post-repair review decision, and full
  factory gates before any import claim.
- Scientific generalization work: No new benchmark or split claim. The all-30
  external structural split remains review-only with max cross-split TM about
  `0.6963`; strict TM-diverse claims remain on external fold-diverse surfaces
  only.
- SPOF hardening work: Yes. New CLI paths, artifacts, and regression tests make
  the C9JRZ8 AKR/NADP post-repair import-safety decision path executable while
  preserving review-only/countable-label separation. `docs/label_factory.md`
  was checked and did not need a content change.

Recorded for the 2026-05-16T21:47:33Z run after acquiring the automation lock,
syncing clean `origin/main`, passing startup gates (`365` unit tests passed and
`validate` passed with 679 curated labels), and passing wrap checks (`368` unit
tests, `validate`, `compileall`, and `git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for two review-only import-safety
  adjudication paths and one additional lane control, no for import or
  countable labels. The P34949 non-text rule consumes a source-traced active-site
  Arg, local pocket composition, absent flavin/cofactor context, zero flavin
  role-hint support, weak top1 score with `absent_flavin_context`, and bounded
  sequence no-signal status; it repairs the weak flavin/scope blocker and
  records post-repair `needs_review`. The Q9BXD5 rule consumes source-traced
  Tyr/Lys active-site residues, a Schiff-base Lys, absent heme/cofactor context,
  zero heme/electron-transfer role-hint support, weak heme top1 score with
  `absent_heme_context`, local pocket context, and bounded sequence no-signal
  status; it repairs the weak heme/scope blocker while preserving the
  representation near-duplicate holdout as an import blocker. Both rows still
  require broader duplicate screening, post-repair review decisions, and full
  factory gates before any import claim.
- Scientific generalization work: No new benchmark or split claim. The all-30
  external structural split remains review-only with max cross-split TM about
  `0.6963`; strict TM-diverse claims remain on external fold-diverse surfaces
  only.
- SPOF hardening work: Yes. New CLI paths, artifacts, and regression tests make
  the P34949 and Q9BXD5 post-repair import-safety decision paths executable
  while preserving review-only/countable-label separation. `docs/label_factory.md`
  was checked and did not need a content change.

Recorded for the 2026-05-16T20:47:11Z run after acquiring the automation
lock, syncing clean `origin/main`, passing startup gates (`363` unit tests
passed and `validate` passed with 679 curated labels), and passing wrap checks
(`365` unit tests, `validate`, `compileall`, and `git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for one real Q6NSJ0 import-safety
  adjudication path and one next-lane P34949 control, no for import or
  countable labels. The glycoside-hydrolase boundary rule consumes only
  source-traced acidic active-site residues, local pocket/ligand context,
  role-hint absence, and bounded sequence-search status; it repairs Q6NSJ0's
  representation/heuristic blocker and records post-repair `needs_review`.
  The sugar-phosphate isomerase control stages the source-traced active-site
  Arg, local pocket composition, absent flavin/cofactor context, zero flavin
  role-hint support, and weak top1 score with local `absent_flavin_context`
  counterevidence for P34949.
- Scientific generalization work: No new benchmark or split claim. The all-30
  external structural split remains review-only with max cross-split TM about
  `0.6963`; strict TM-diverse claims remain on external fold-diverse surfaces
  only.
- SPOF hardening work: Yes. Two new CLI paths, artifacts, and regression tests
  make the Q6NSJ0 post-repair import-safety decision path executable and stage
  the next sugar-phosphate isomerase lane while preserving review-only/countable
  label separation.

Recorded for the 2026-05-16T19:45:17Z run after acquiring the automation
lock, syncing clean `origin/main`, passing startup gates (`361` unit tests
passed and `validate` passed with 679 curated labels), and passing wrap checks
(`363` unit tests, `validate`, `compileall`, and `git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for one real O14756 import-safety
  adjudication path and one next-lane control, no for import or countable
  labels. The SDR/NAD(P) rule consumes only sequence/active-site/reference
  axis evidence, repairs O14756's representation-conflict blocker, and records
  post-repair `needs_review`; broader duplicate screening, a post-repair
  review decision, and the full factory gate still block import. The `Q6NSJ0`
  glycoside-hydrolase boundary lane now has a review-only non-text control
  from acidic active-site residues, local pocket composition, absent
  metal/cofactor ligand context, and zero metal-hydrolase role-hint support.
- Scientific generalization work: No new benchmark or split claim. The all-30
  external structural split remains review-only with max cross-split TM about
  `0.6963`; strict TM-diverse claims remain on external fold-diverse surfaces
  only.
- SPOF hardening work: Yes. Two new CLI paths, artifacts, and regression tests
  make the first post-repair import-safety decision path executable while
  preserving review-only/countable-label separation.

Recorded for the 2026-05-16T12:06:39-05:00 run after acquiring the automation
lock, syncing clean `origin/main`, passing startup gates (`360` unit tests
passed and `validate` passed with 679 curated labels), and confirming the six
normalized external `needs_review` rows were already resolved on the latest
pushed state; wrap checks also passed (`361` unit tests, `validate`,
`compileall`, and `git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for one bounded review-only repair
  control, no for import or countable labels. This run stages the SDR/NAD(P)
  redox lane for `O14756` as a sequence-derived contrast control using a
  `TGxxxGxG` glycine-rich proxy plus a source-active-site-overlapping `YxxxK`
  proxy. The conflicting current-reference neighbors lack the complete SDR
  axis, so the lane is ready for future review-only scorer repair; the selected
  pilot still has 0 `needs_review`, 0 import-ready rows, and 0 countable
  external labels.
- Scientific generalization work: No new benchmark or split claim. The all-30
  external structural split remains review-only with max cross-split TM about
  `0.6963`; this run advances representation/heuristic control repair rather
  than broadening structure.
- SPOF hardening work: Yes. The new control artifact, CLI path, and regression
  coverage make the first repair lane executable while preserving review-only
  import-safety invariants. The substantive repair-control commit has since
  reached `origin/main`; only a later handoff/status correction remains local
  because the current shell still cannot complete HTTPS Git push.

Recorded for the 2026-05-16T16:04:57Z run after acquiring the automation lock,
syncing clean `origin/main`, passing startup gates (`359` unit tests passed and
`validate` passed with 679 curated labels), confirming the six normalized
external `needs_review` rows were already resolved on the latest pushed state,
and passing wrap checks (`360` unit tests, `validate`, `compileall`, and
`git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for representation/heuristic repair
  scoping, no for import or countable labels. This run added
  `artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json`, which
  assigns the six resolved representation conflicts to six named review-only
  repair lanes: SDR/NAD(P) redox, AKR/NADP redox, DNA Pol X/5'-dRP lyase,
  sugar-phosphate isomerase, Schiff-base lyase/aldolase, and
  glycoside-hydrolase versus metal-hydrolase boundary control. The selected
  pilot still has 0 `needs_review`, 0 import-ready rows, and 0 countable
  external labels.
- Scientific generalization work: No new benchmark or split claim. The
  all-30 external structural split remains review-only with max cross-split TM
  about `0.6963`; this run prepared the next representation/heuristic repair
  target rather than broadening structure.
- SPOF hardening work: Yes. The new CLI, artifact, and regression coverage make
  the zero-pass repair lanes explicit while preserving review-only/import-safety
  invariants. `docs/label_factory.md` was checked and needed no content change.

Recorded for the 2026-05-16T15:04:24Z run after acquiring the automation lock,
syncing clean `origin/main`, passing startup gates (`358` unit tests passed and
`validate` passed with 679 curated labels), desk-reviewing the 6 normalized
external `needs_review` rows, and passing wrap checks (`359` unit tests,
`validate`, `compileall`, and `git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and no
  M-CSA strict-TM round, query, split-repair, or partition-repair work was
  resumed.
- External-source repair/import: Yes for pilot review reduction, no for import
  or countable labels. This run added a needs-review resolution artifact, a
  resolved decision artifact, and an empty resolved review queue. Targeted
  UniRef90/50 mapping found 0 shared candidate/current-reference clusters for
  the nearest-reference checks, so duplicate rejection was not supported; all
  six formerly `needs_review` rows were closed as review-only
  `rejected_representation_conflict` import-safety decisions. The resolved
  pilot surface has 0 `needs_review`, 0 import-ready rows, and 0 countable
  external labels.
- Scientific generalization work: No new benchmark or split claim. The current
  all-30 external structural split remains review-only; the new work explains a
  zero-pass selected-pilot outcome rather than broadening the structural
  surface.
- SPOF hardening work: Yes. Regression coverage now checks the resolved
  six-row artifact, resolved decision counts, zero queued expert rows, and the
  invariant that no resolved external row is countable or import-ready.

Recorded for the 2026-05-16T09:03:56-05:00 run after recovering this run's
self-created short-lived shell-PID lock, reacquiring a live lock, syncing clean
`origin/main`, passing startup gates (`357` unit tests passed and `validate`
passed with 679 curated labels), and confirming the candidate-by-candidate
confidence audit already existed before external expansion:

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and no M-CSA strict-TM round, query, split-repair, or partition-repair work
  was resumed.
- External-source repair/import: Yes for duplicate-confidence repair, no for
  import or countable labels. This run added a real review-only external
  candidate all-vs-all MMseqs2 sequence screen covering 30/30 external rows,
  with 0 near-duplicate pairs at 90% identity / 80% coverage and max reported
  external-external identity `0.647`; the pilot audit/normalized decisions now
  carry that evidence while preserving 6 `needs_review`, 0 import-ready rows,
  and 0 countable external labels.
- Scientific generalization work: No new benchmark/import claim. The existing
  review-only all-30 structural split remains the structural generalization
  artifact; the new all-vs-all sequence screen narrows duplicate uncertainty
  only inside the current external candidate sample.
- SPOF hardening work: Yes. The backend current-reference sequence-search
  artifact no longer overclaims UniRef/all-vs-all completion, the external
  all-vs-all sequence screen has a dedicated builder/audit and regression
  coverage, and the transfer-gate command documentation now includes the
  pilot active-site decision input needed for the 68/68 gate.

Recorded for the 2026-05-16T13:02:29Z run after confirming no fresh automation
lock was active, syncing clean `origin/main`, passing startup gates (`357` unit
tests passed and `validate` passed with 679 curated labels), rerunning the
external pilot confidence/normalization builders idempotently, checking the
latest README/docs/work guidance, and passing wrap checks (`357` unit tests,
`validate`, `compileall`, and `git diff --check`):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and no M-CSA strict-TM round, query, split-repair, or partition-repair work
  was resumed.
- External-source repair/import: Yes for audit verification and guidance
  repair, no for import or countable labels. The requested candidate-by-candidate
  audit already existed on `origin/main`; this run reran the three audit and
  normalization CLIs with no artifact diff, verified the normalized 6-row
  `needs_review` surface, and found no safe local-evidence-only decision update.
- Scientific generalization work: No new benchmark or split claim. The
  existing review-only all-30 external structural split remains the current
  generalization artifact, with import still blocked by review/duplicate/factory
  evidence.
- SPOF hardening work: Yes. The handoff and external-transfer docs now point
  next agents at the normalized 6-row review blocker rather than the older
  3-row deferred-only queue; no new gates or artifacts were added.

Recorded for the 2026-05-16T07:01:54-05:00 run after confirming no fresh
automation lock was active, syncing clean `origin/main`, passing startup gates
(`356` unit tests passed and `validate` passed with 679 curated labels), and
passing wrap checks (`357` unit tests passed and `validate` passed with 679
curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and no M-CSA strict-TM round, query, split-repair, or partition-repair work
  was resumed.
- External-source repair/import: Yes for selected-pilot confidence repair and
  no for import or countable labels. This run added a candidate-by-candidate
  decision-confidence audit, normalized 3 weak representation-only duplicate
  rejections to `needs_review`, preserved 3 active-site-missing rejections and
  1 stable representation-near-duplicate rejection, routed all 6
  needs-review rows, and kept 0 import-ready rows / 0 countable external
  labels.
- Scientific generalization work: No new benchmark or split claim. The
  existing external all-30 review-only structural split remains the current
  generalization artifact; this run focused on evidence confidence for pilot
  decisions before any import expansion.
- SPOF hardening work: Yes. The pilot terminal-decision surface now has a
  reproducible CLI audit, normalized decision artifact, normalized review
  queue, and regression coverage so representation-only duplicate rejections
  cannot silently remain overconfident. README, `docs/external_source_transfer.md`,
  `work/handoff.md`, and `work/scope.md` were updated; `docs/label_factory.md`
  was checked and needed no change.

Recorded for the 2026-05-16T11:01:29Z run after recovering this run's
short-lived stale shell-PID lock, confirming the git tree was clean, syncing
clean `origin/main`, passing startup gates (`354` unit tests passed and
`validate` passed with 679 curated labels), completing the external all-30
structural pair cache, and assigning a review-only cluster-preserving split:

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and no M-CSA strict-TM round, query, split-repair, or partition-repair work
  was resumed.
- External-source repair/import: Yes for external structural repair, no for
  import or countable labels. This run changed the all-30 external structural
  cluster index from an incomplete 313/435 pair cache to a complete 435/435
  unordered nonself pair cache and added a review-only split plan with 6 test
  and 24 train candidates, 0 cross-split `TM >=0.7` violations, 0 import-ready
  rows, and 0 countable external labels.
- Scientific generalization work: Yes. Strict structural-diversity work is now
  on the external Swiss-Prot/AFDB surface, with cluster-preserving split
  assignment and max cross-split TM-score `0.6963`; this is still review-only
  because pilot rows are not import-ready benchmark labels.
- SPOF hardening work: Yes. The Foldseek command now forces exhaustive exact
  TM-align reporting with `-e inf` and high `--max-seqs`, regression tests
  guard complete all-vs-all pair coverage and the review-only split plan, and
  M-CSA strict-TM repair remains closed.

Recorded for the 2026-05-16T09:59:24Z run after syncing clean `origin/main`,
passing startup gates (`352` unit tests passed and `validate` passed with
679 curated labels), passing wrap checks (`354` unit tests passed, `validate`
passed with 679 curated labels, `compileall` passed, and `git diff --check`
passed), and expanding the external structural surface:

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and no M-CSA strict-TM round, query, split-repair, or partition-repair work
  was resumed.
- External-source repair/import: Yes for external structural-surface repair,
  no for import or countable labels. This run added the all-30 external
  structural path and cluster index with 30/30 AlphaFold sidecars, 0 fetch
  failures, 30/30 Foldseek nearest-neighbor coverage, 6 high-TM pairs, 26
  pre-split clusters, 0 import-ready rows, and 0 countable external labels.
- Scientific generalization work: Yes for moving strict structural-diversity
  work onto the broader external Swiss-Prot/AFDB surface, not for a full split
  claim. Strict TM-diverse split assignment remains blocked because Foldseek
  emitted an incomplete all-vs-all pair cache.
- SPOF hardening work: Yes. A dedicated path builder, all-30 artifact
  regression, coordinate digests, and lineage metadata now keep the external
  structural surface reproducible while preserving the M-CSA strict-TM closure.

Recorded for the 2026-05-16T08:59:00Z run after syncing clean `origin/main`,
passing startup gates (`350` unit tests passed and `validate` passed with
679 curated labels), and passing wrap checks (`352` unit tests passed,
`validate` passed with 679 curated labels, `compileall` passed, and
`git diff --check` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and no M-CSA strict-TM round, query, split-repair, or partition-repair work
  was resumed.
- External-source repair/import: Yes for selected-pilot structure-index
  readiness, no for import or countable labels. This run added
  `artifacts/v3_external_structural_cluster_index_1025.json` plus 10
  AlphaFold coordinate sidecars, with 0 fetch failures, 10/10 nearest-neighbor
  cache coverage, 1 high-TM pair, and 0 import-ready rows.
- Scientific generalization work: Yes for external structural diversity
  groundwork, not for a full split claim. Foldseek completed on the 10 selected
  external pilot structures, clustering them into nine `TM >=0.7` components;
  full strict-TM split assignment remains blocked until a broader external
  fold-diverse candidate surface is available.
- SPOF hardening work: Yes. A dedicated CLI builder and regression coverage now
  materialize external coordinate sidecars with digests, validate 1,025
  lineage, keep the artifact review-only/non-countable, and keep M-CSA
  strict-TM repair closed.

Recorded for the 2026-05-16T07:57:24Z run after syncing clean `origin/main`,
passing startup gates (`349` unit tests passed and `validate` passed with
679 curated labels), and passing wrap checks (`350` unit tests passed and
`validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and M-CSA strict TM-score repair remains closed/deferred with
  `full_tm_score_holdout_claim_permitted=false`.
- External-source repair/import: Yes for deferred-pilot review routing, no for
  import or countable labels. This run added
  `artifacts/v3_external_source_pilot_human_expert_review_queue_1025.json`,
  routing `O14756`, `P34949`, and `Q6NSJ0` to review-only human/expert
  questions with exact unresolved evidence and remaining non-human blockers.
- Scientific generalization work: No new structural split claim or M-CSA TM
  work. The external structural pilot path remains the next fold-diverse
  generalization route after expert decision routing.
- SPOF hardening work: Yes. A dedicated CLI builder and regression coverage now
  keep deferred selected-pilot rows review-only, non-countable, and explicitly
  blocked on expert review, broader duplicate screening, and full factory gates.

Recorded for the 2026-05-16T01:55:26-05:00 run after syncing clean
`origin/main` and passing startup gates (`428` unit tests passed and
`validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. M-CSA-only tranche growth remains stopped.
- External-source repair/import: No for import and no new countable external
  labels. This run cleaned the M-CSA strict-TM implementation loop and recorded
  terminal decisions for the 10 selected external pilot rows: 4
  duplicate/near-duplicate rejections, 3 active-site-evidence-missing
  rejections, and 3 human-expert deferrals.
- Scientific generalization work: Yes for cleanup/adjudication, not for a new
  M-CSA strict-TM claim. Noncanonical round/chunk artifacts were removed after
  retaining the all-materializable max-TM evidence and final adjudication with
  `full_tm_score_holdout_claim_permitted=false`.
- SPOF hardening work: Yes. Tests now retain generic Foldseek tooling coverage
  while removing M-CSA round-repair pinned artifact tests, and a guardrail
  prevents current guidance from making M-CSA strict-TM round repair the main
  priority again.

Recorded for the 2026-05-16T05:47:16Z run after recovering a stale directory
lock whose recorded PID (`33199`) was no longer alive, confirming the worktree
was clean, syncing clean `origin/main`, passing startup gates (`426` unit
tests passed and `validate` passed with 679 curated labels), and passing wrap
checks (`428` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not reopen an M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  labels. Latest pushed state already redirects the next direct work to the
  external structural pilot; the selected external pilot still has 10
  review-only candidates, 0 terminal decisions, 0 import-ready rows, 3
  unresolved active-site-source rows, 10 broader duplicate-screening blockers,
  3 unresolved representation-control rows, and 10 full-gate blockers.
- Scientific generalization work: No new M-CSA strict TM-score claim or repair
  artifact was landed. The current repo state has already adjudicated the
  native M-CSA strict pairwise-TM repair loop as review-only/non-canonical
  context with `full_tm_score_holdout_claim_permitted=false`; do not resume
  round33 or staged index 145 continuation unless the user explicitly reverses
  that state.
- SPOF hardening work: No new scientific SPOF hardening was landed in this
  bounded run. Operationally, the stale lock was recovered only after the
  recorded PID was dead and the git tree was clean; README, label-factory docs,
  external-transfer docs, scope, status, and handoff state were checked against
  latest `origin/main`.

Recorded for the 2026-05-16T05:45:22Z run after syncing clean `origin/main`,
passing startup gates (`426` unit tests passed and `validate` passed with
679 curated labels), and final gates (`429` unit tests passed and `validate`
passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records.
- External-source repair/import: No for import and no new countable external
  labels. The selected external pilot still has 10 review-only candidates,
  0 terminal decisions, 0 import-ready rows, 3 unresolved active-site-source
  rows, 10 broader duplicate-screening blockers, 3 unresolved
  representation-control rows, and 10 full-gate blockers.
- Scientific generalization work: Yes for adjudication, not repair. The
  all-materializable M-CSA Foldseek signal observed max train/test TM-score
  `0.9749`; round32 accumulated 108 high-TM constraints plus 38 sequence
  constraints; index 145 timed out under the standard single-query path. This
  is now treated as an unsatisfiable M-CSA proxy rather than unfinished
  engineering work.
- SPOF hardening work: Yes. Preserved three coherent target-shard artifacts as
  non-canonical review-only context, added durable adjudication/regression
  coverage that keeps
  `full_tm_score_holdout_claim_permitted=false`, and added a review-only
  external structural TM-holdout path artifact for the 10 selected pilot rows.

Recorded for the 2026-05-15T22:00:14Z run after syncing clean `origin/main`
and passing startup gates (`426` unit tests passed and `validate` passed with
679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 30 index 142 cleared at max `0.6204`, index 143 exposed `m_csa:144`
  at max `0.872`, round 31 folded that surface but still failed index 143 at
  max `0.8001`, and round 32 folded the second surface before clearing
  indices 143-144 at max `0.5745`. Index 145 timed out at 900 seconds before
  Foldseek pair rows were emitted.
- SPOF hardening work: Yes. The run converted the new high-TM train/test
  blockers into cluster-first partition constraints, bringing the active split
  to 108 high-TM constraints plus 38 sequence-identity constraints with 0
  projected violations, 0 sequence-cluster splits, and 0 held-out out-of-scope
  false non-abstentions. `m_csa:372` and `m_csa:501` remain coordinate
  exclusions, most query coverage remains unverified under the cluster-first
  split, index 145 is a runtime blocker, and
  `full_tm_score_holdout_claim_permitted=false`.
- Next start: retry or adjudicate staged index 145 under
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round32.json`.

Recorded for the 2026-05-15T15:59:13-05:00 run after syncing clean
`origin/main` and passing startup gates (`424` unit tests passed and
`validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 28 index 131 exposed `m_csa:132` versus `m_csa:532` at max TM-score
  `0.8385`; round 29 folded that blocker and cleared indices 131-139 before
  index 140 exposed `m_csa:141` versus `m_csa:903` at max `0.7337`; round 30
  folded that blocker and cleared indices 140-141 at max `0.6873`.
- SPOF hardening work: Yes. The run converted the new high-TM train/test
  blockers into cluster-first partition constraints, bringing the active split
  to 102 high-TM constraints plus 38 sequence-identity constraints with 0
  projected violations, 0 sequence-cluster splits, and 0 held-out out-of-scope
  false non-abstentions. `m_csa:372` and `m_csa:501` remain coordinate
  exclusions, most query coverage remains unverified under the cluster-first
  split, and `full_tm_score_holdout_claim_permitted=false`.
- Next start: continue single-query verification from staged index 142 under
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round30.json`.

Recorded for the 2026-05-15T19:58:30Z run after repairing a self-created stale
exec-shell PID lock into the expected live sentinel directory lock, syncing
clean `origin/main`, and passing startup gates (`421` unit tests passed and
`validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 24 index 123 exposed `m_csa:124` at max TM-score `0.9676`; round 25
  folded those blockers but exposed a second `m_csa:124` surface at max
  `0.8735`; round 26 folded that surface and cleared indices 123-126 at max
  `0.6981` before index 127 exposed `m_csa:128` versus `m_csa:198` at max
  `0.8035`; round 27 folded that pair and cleared indices 127-129 at max
  `0.6868` before index 130 exposed `m_csa:131` versus
  `m_csa:281`/`m_csa:555` at max `0.7574`; round 28 folded those blockers and
  cleared index 130 at max `0.6775`.
- SPOF hardening work: Yes. The run converted the new high-TM train/test
  blockers into cluster-first partition constraints, bringing the active split
  to 100 high-TM constraints plus 38 sequence-identity constraints with 0
  projected violations, 0 sequence-cluster splits, and 0 held-out out-of-scope
  false non-abstentions. `m_csa:372` and `m_csa:501` remain coordinate
  exclusions, most query coverage remains unverified under the cluster-first
  split, and `full_tm_score_holdout_claim_permitted=false`.
- Next start: continue single-query verification from staged index 131 under
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round28.json`.

Recorded for the 2026-05-15T18:56:51Z run after lock recovery/repair and
clean startup gates (`418` unit tests passed and `validate` passed with 679
curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 22 index 119 exposes `m_csa:120` at max TM-score `0.7556`; round 23
  folds those blockers but its index-119 rerun still exposes `m_csa:120` at
  max `0.711`; round 24 folds the second blocker surface and clears staged
  indices 119-122 in aggregate at max train/test TM-score `0.6961`.
- SPOF hardening work: Yes. The run converted the new high-TM train/test
  blockers into cluster-first partition constraints, bringing the active split
  to 93 high-TM constraints plus 38 sequence-identity constraints with 0
  projected violations, 0 sequence-cluster splits, and 0 held-out out-of-scope
  false non-abstentions. `m_csa:372` and `m_csa:501` remain coordinate
  exclusions, most query coverage remains unverified under the cluster-first
  split, and `full_tm_score_holdout_claim_permitted=false`.
- Next start: continue single-query verification from staged index 123 under
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round24.json`.

Recorded for the 2026-05-15T17:54:36Z run after clean startup gates
(`415` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 19 clears staged indices 112-113 before index 114 exposes `m_csa:115`
  versus `m_csa:822` at max TM-score `0.7338`; round 20 folds that pair and
  clears index 114 before index 115 exposes a broader `m_csa:116` surface at
  max `0.9749`; round 21 folds that surface but exposes `m_csa:116` versus
  held-out `m_csa:67` at max `0.9032`; round 22 folds that pair and clears
  indices 115-118 at max `0.6939`.
- SPOF hardening work: Yes. The run converted each new high-TM train/test
  blocker into cluster-first partition constraints, bringing the active split
  to 82 high-TM constraints plus 38 sequence-identity constraints with 0
  projected violations and 0 sequence-cluster splits. `m_csa:372` and
  `m_csa:501` remain coordinate exclusions, most query coverage remains
  unverified under the cluster-first split, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T11:53:48-05:00 run after clean startup gates
(`412` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 16 reruns staged index 110 and exposes `m_csa:111` versus `m_csa:852`
  at max TM-score `0.7708`; round 17 folds that pair, clears index 110 at max
  `0.6823`, clears index 111 at max `0.564`, then index 112 exposes
  `m_csa:113` versus held-out `m_csa:131` at max `0.7063`. Round 18 folds
  that pair but exposes a broader `m_csa:113` surface against `m_csa:942`,
  `m_csa:978`, and related in-distribution neighbors at max `0.9087`. Round
  19 folds that evidence into 72 high-TM constraints plus 38 sequence-identity
  partition constraints, with 0 projected violations and 0 sequence-cluster
  splits.
- SPOF hardening work: Yes. The run converted each observed high-TM train/test
  blocker into a cluster-first partition constraint and stopped forward
  coverage when index 112 exposed unresolved blocker evidence. `m_csa:372` and
  `m_csa:501` remain coordinate exclusions, most query coverage remains
  unverified under the cluster-first split, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T15:52:42Z run after clean startup gates
(`409` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round 13 clears staged indices 105-106 before index 107 exposes `m_csa:108`
  at max TM-score `0.8826`; round 14 folds that blocker and clears index 107
  at max `0.6862`. Index 108 exposes `m_csa:109` at max `0.7649`; round 15
  folds that blocker and clears indices 107-109 at max `0.6996`. Index 110
  exposes `m_csa:111` at max `0.7521`; round 16 folds it into 66 high-TM
  constraints with 0 projected violations and 0 sequence-cluster splits.
- SPOF hardening work: Yes. The run kept using cluster-first, one-query
  verification and constraint-cache repair rather than blind 56-chunk grinding.
  `m_csa:372` and `m_csa:501` remain coordinate exclusions, most query coverage
  remains unverified under the cluster-first split, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T14:52:02Z run after clean startup gates
(`401` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round-9 single-query verification clears staged indices 96-101 before index
  102 exposes `m_csa:103`/`pdb:1VAO` versus held-out `m_csa:115`/`pdb:1W1O`
  at max TM-score `0.7653`. Round 10 folds that blocker into 42 high-TM
  constraints plus 38 sequence-identity partition constraints, preserves 0
  sequence-cluster splits, and reruns staged index 102 cleanly at max
  train/test TM-score `0.6725`. Rounds 11 and 12 fold the next staged-index
  103 blockers, with round 12 clearing index 103 at max `0.6669`; index 104
  passes at max `0.4496`; index 105 exposes a larger blocker at max `0.8862`,
  and round 13 folds it into 48 high-TM constraints with 0 sequence-cluster
  splits.
- SPOF hardening work: Yes. The cluster-first builder now unions real
  sequence-identity clusters before structural component assignment, preventing
  a repaired structure split from introducing sequence-cluster leakage. The
  all-materializable staged-coordinate Foldseek signal also completed and
  removes the prior runtime ambiguity, but it fails the `<0.7` target at max
  `0.9749`; `m_csa:372` and `m_csa:501` remain coordinate exclusions and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T13:50:06Z run after clean startup gates
(`400` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification, but not for a full split claim. Round-9
  single-query verification now clears staged indices 84-95 with 17,189 mapped
  rows, 3,257 train/test rows, max train/test TM-score `0.6579`, and 0
  target-violating pairs.
- SPOF hardening work: Yes. The run converted more of the remaining
  cluster-first proof surface into resumable one-query Foldseek evidence
  instead of returning to blind all-vs-all or 56-chunk grinding. `m_csa:372`
  and `m_csa:501` remain coordinate exclusions, most query coverage remains
  unverified under the cluster-first round-9 split, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T12:48:12Z run after clean startup gates
(`396` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round-8 single-query verification cleared staged indices 68-78 before staged
  index 79 exposed held-out out-of-scope `m_csa:80` versus in-distribution
  `m_csa:408`/`m_csa:569` at max TM-score `0.8726`. Round 9 folds those pairs
  into 41 high-TM constraints, 19 constrained clusters, 0 projected
  violations, and 0 sequence-cluster splits; the direct round-9 rerun of index
  79 plus indices 80-83 passes at max TM-score `0.6477`.
- SPOF hardening work: Yes. The run converted a new high-TM train/test blocker
  into a cluster-first partition constraint and verified the repaired bounded
  query window instead of continuing blind chunks. `m_csa:372` and `m_csa:501`
  remain coordinate exclusions, most query coverage remains unverified under
  the cluster-first round-9 split, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T08:05:27Z run after clean startup gates
(`391` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification, but not for a full split claim. The timed-out
  round-7 microchunk-020 window was isolated into one-query Foldseek checks:
  indices 60-62 (`m_csa:61`-`m_csa:63`) pass in aggregate at max TM-score
  `0.6967`, and indices 63-65 (`m_csa:64`-`m_csa:66`) pass in aggregate at
  max TM-score `0.5629`, both with 0 target-violating pairs. Staged index 66
  (`m_csa:67`) also passes at max TM-score `0.6535`; staged index 67
  (`m_csa:68`) exposes a new `m_csa:68`/`m_csa:750` blocker at max TM-score
  `0.7909`, and round 8 folds that pair into 39 constraints with 0 projected
  violations.
- SPOF hardening work: Yes. The run converted the round-7 microchunk-020
  runtime blocker into six completed one-query evidence artifacts plus two
  aggregate summaries, then stopped on the next high-TM blocker and converted
  it into a round-8 cluster-first partition constraint. `m_csa:372` and
  `m_csa:501` remain coordinate exclusions, most query coverage remains
  unverified under the cluster-first round-8 split, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T07:04:30Z run after clean startup gates
(`387` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round-6 subchunk 010 timed out under the 900-second bound before pair rows
  were emitted. A 3-query split of that same window completed microchunk 020,
  found a `m_csa:63`/`m_csa:188` blocker at max TM-score `0.7116`, and round 7
  folded that pair into 38 high-TM constraints. The direct round-7
  microchunk-020 rerun timed out, so the repair remains unverified.
- SPOF hardening work: Yes. The run converted the subchunk-010 runtime blocker
  into a smaller completed evidence unit, turned the newly observed high-TM
  pair into a partition constraint, regenerated round-7 coordinate readiness,
  and pinned the new timeout/failure artifacts in tests. `m_csa:372` and
  `m_csa:501` remain coordinate exclusions, the `m_csa:61`-`m_csa:63` window
  needs single-query isolation under round 7, the `m_csa:64`-`m_csa:66` half
  is still unrun, all outputs remain review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T06:03:46Z run after clean startup gates
(`387` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not change external pilot evidence decisions; the
  selected external pilot remains review-only with 0 import-ready rows and 0
  countable candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  Round-4 subchunk 008 exposed a `m_csa:54`/`m_csa:428` blocker at max
  TM-score `0.7205`; round 5 folded it into 36 high-TM constraints and the
  direct round-5 rerun passed at max TM-score `0.6989`. Round-5 subchunk 009
  exposed a `m_csa:58`/`m_csa:628` blocker at max TM-score `0.879`; round 6
  folded it into 37 high-TM constraints and the direct round-6 rerun passed at
  max TM-score `0.6699`.
- SPOF hardening work: Yes. The run continued the cluster-first replacement
  path instead of blind 56-chunk grinding, converted two newly observed
  high-TM pairs into partition constraints, regenerated round-5 and round-6
  coordinate-readiness artifacts, and reran each failing bounded verification
  unit. `m_csa:372` and `m_csa:501` remain coordinate exclusions, most query
  coverage remains unverified under the cluster-first round-6 split, all
  outputs remain review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T05:02:16Z run after clean startup gates
(`383` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not change external pilot evidence decisions; the
  selected external pilot remains review-only with 0 import-ready rows and 0
  countable candidates.
- Scientific generalization work: Yes for direct Foldseek/TM-score
  cluster-first verification and split repair, but not for a full split claim.
  This run directly reran round-3 cluster-first subchunks 006 and 007. Subchunk
  006 passed with max train/test TM-score `0.6509`; subchunk 007 exposed one
  remaining `m_csa:45`/`m_csa:397` blocker at max TM-score `0.8043`. The
  round-4 cluster-first candidate folds that blocker into 35 high-TM
  constraints, moves held-out out-of-scope `m_csa:397` to in-distribution,
  preserves 0 sequence-cluster splits and 0 held-out out-of-scope false
  non-abstentions, and its direct subchunk-007 rerun passes with max train/test
  TM-score `0.6598`.
- SPOF hardening work: Yes. The run prevents blind chunk grinding by converting
  the new observed high-TM pair into a cluster-first partition constraint,
  regenerating round-4 coordinate readiness, and rerunning the failing bounded
  verification unit. `m_csa:372` and `m_csa:501` remain coordinate exclusions,
  most query coverage remains unverified under the cluster-first round-4 split,
  all outputs remain review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T04:00:46Z run after clean startup gates
(`378` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. This run did not modify external pilot decisions; the selected
  external pilot remains review-only with 0 import-ready rows and 0 countable
  candidates.
- Scientific generalization work: Yes for Foldseek/TM-score cluster-first
  split design and bounded verification, but not for a full split claim. This
  run added cluster-first split candidates through round 3, round-specific
  readiness artifacts, and query subchunk verification artifacts. The current
  round-3 cluster-first candidate has 34 high-TM constraints, 14 constrained
  clusters, 0 projected known constraint violations, 0 sequence-cluster splits,
  and 0 held-out out-of-scope false non-abstentions. Round-2 subchunk 006
  passes after moving held-out out-of-scope `m_csa:118` to in-distribution,
  but round-2 subchunk 007 fails with max train/test TM-score `0.8651`, 16
  violating rows, and 9 reported blocking structure pairs; those blockers are
  folded into the current round-3 candidate.
- SPOF hardening work: Yes. The run replaces blind 56-chunk continuation with
  a cluster-first partition-constraint cache over the 672 staged
  materializable structures, demonstrates a smaller 6-query verification
  route for the old chunk-3 timeout region, and converts the latest failure
  into concrete round-3 split constraints. `m_csa:372` and `m_csa:501` remain
  coordinate exclusions, most query coverage remains unverified under the
  cluster-first round-3 split, all outputs remain review-only/non-countable,
  and `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T21:59:56-05:00 run after clean startup gates
(`374` unit tests passed and `validate` passed with 679 curated labels; final
wrap-up gates passed `378` unit tests and `validate` after the new artifacts
were pinned):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected external pilot remains review-only with 0
  import-ready rows and 0 countable candidates; this run did not change pilot
  terminal decisions or import readiness.
- Scientific generalization work: Yes for Foldseek/TM-score split-redesign
  evidence, but not for a full split claim. This run added
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_002_of_056.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_003_of_056.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_002_of_056.json`,
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_003_of_056.json`.
  Round-3 chunk 2 completed directly under the 900-second bound with 12,639
  mapped rows, 2,385 train/test rows, max train/test TM-score `0.584`, and 0
  target-violating pairs. The chunks 0-2 aggregate covers 36 query
  coordinates, 40,890 mapped rows, 13,472 train/test rows, max train/test
  TM-score `0.695`, and 0 target-violating pairs. Chunk 3 timed out under the
  standard 900-second bound before emitting pair rows; the chunks 0-3 aggregate
  keeps that timeout visible while preserving completed-chunk max `0.695`.
- SPOF hardening work: Yes. The run removes the round-3 chunk-2 runtime and
  target-status ambiguity, and converts chunk 3 into a concrete runtime
  blocker without claiming full separation. `m_csa:372` and `m_csa:501`
  remain coordinate exclusions, chunks 3-55 remain uncomputed under the
  round-3 redesigned split until chunk 3 is retried or split, all outputs
  remain review-only and non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T01:57:51Z run after clean startup gates
(`370` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000
  with 679 canonical labels, the 1,025 preview adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. Do not open another M-CSA-only tranche without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected external pilot remains review-only with 0
  import-ready rows and 0 countable candidates; this run did not change pilot
  review decisions or import readiness.
- Scientific generalization work: Yes for Foldseek/TM-score split-redesign
  evidence, but not for a full split claim. This run added
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_001_of_056.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_aggregate_000_001_of_056.json`,
  `artifacts/v3_foldseek_tm_score_split_redesign_candidate_round2_query_chunk_repair_plan_1000.json`,
  `artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round3_1000.json`,
  `artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate_round3.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_000_of_056.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_001_of_056.json`,
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_001_of_056.json`.
  Round-2 chunk 1 exposed a new target failure with max train/test TM-score
  `0.8182`; the round-3 redesign moved `m_csa:157` and `m_csa:258` to
  heldout and direct chunks 0-1 clear with max train/test TM-score `0.695` and
  0 target-violating pairs.
- SPOF hardening work: Yes. The run avoids a false full-holdout claim by
  preserving the failed round-2 chunk-1 artifact and repair plan, then
  directly validates the round-3 candidate over both completed query chunks.
  `m_csa:372` and `m_csa:501` remain coordinate exclusions, 54 query chunks
  remain uncomputed under the round-3 redesigned split, all outputs remain
  review-only/non-countable, and `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-15T00:56:30Z run after clean startup gates
(`362` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  Do not open another M-CSA-only tranche without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected external pilot remains review-only with 0
  import-ready rows and 0 countable candidates; this run did not change the
  pilot success criteria or external review decisions.
- Scientific generalization work: Yes for Foldseek/TM-score split-redesign
  evidence, but not for a full split claim. This run added
  `artifacts/v3_sequence_distance_holdout_split_redesign_candidate_1000.json`,
  `artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_000_of_056.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_aggregate_000_of_056.json`,
  `artifacts/v3_foldseek_tm_score_split_redesign_candidate_query_chunk_repair_plan_1000.json`,
  `artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round2_1000.json`,
  `artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate_round2.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_000_of_056.json`,
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_aggregate_000_of_056.json`.
  The redesign candidate resolves the 15 previously observed completed-chunk
  blockers in projection, but the direct redesigned chunk 0 fails with max
  train/test TM-score `0.926`. The round-2 redesign then moves `m_csa:277`,
  `m_csa:378`, `m_csa:320`, and `m_csa:108` to heldout and clears chunk 0
  directly with max train/test TM-score `0.695` and 0 target-violating pairs.
- SPOF hardening work: Yes. The run removes the projection-only ambiguity for
  the first split redesign by rerunning Foldseek directly, then removes the
  resulting chunk-0 blocker with a second direct redesign check. `m_csa:372`
  and `m_csa:501` remain coordinate exclusions, 55 query chunks remain
  uncomputed under the round-2 redesigned split, all outputs remain
  review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T18:55:52-05:00 run after clean startup gates
(`359` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  Do not open another M-CSA-only tranche without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected external pilot still has 0 import-ready rows and 0
  countable candidates. Pilot success criteria exist, but active-site,
  broader duplicate-screening, representation/review, and full label-factory
  blockers remain review-only.
- Scientific generalization work: Yes for Foldseek/TM-score query-chunk
  runtime repair and target-failure adjudication, but not for a full split
  claim. This run added
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json`,
  and
  `artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json`.
  Chunk 2 completes under a 1,800-second cap, but the completed chunks still
  fail the `<0.7` target.
- SPOF hardening work: Yes. The split-repair planner now computes holdout
  counts from row partitions when consuming candidate holdout artifacts and
  reports unique held-out in-scope blockers instead of double-counting repeated
  pairs. The completed-retry aggregate records 3/56 completed chunks, 36
  completed query coordinates, 40,890 mapped pair rows, 12,358 train/test rows,
  max train/test TM-score `0.8957`, 76 target-violating row-level pairs, 15
  reported target-violating structure pairs, and 53 non-completed chunks. The
  query-chunk split-repair plan classifies those blockers into 9 conservative
  held-out out-of-scope repair candidates and 6 manual split-redesign blockers
  involving held-out in-scope rows (`m_csa:20`, `m_csa:497`, and `m_csa:895`).
  `m_csa:372` and `m_csa:501` remain coordinate exclusions, all outputs remain
  review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T22:54:46Z run after clean startup gates
(`356` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  Do not open another M-CSA-only tranche without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected external pilot still has 0 import-ready rows and 0
  countable candidates. Pilot criteria exist, but active-site, broader
  duplicate-screening, representation/review, and full gate blockers remain
  review-only.
- Scientific generalization work: Yes for Foldseek/TM-score chunk aggregation
  and direct runtime evidence, but not for a full split claim. This run added
  `aggregate-foldseek-tm-score-query-chunks`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json`,
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_of_056.json`.
  Chunk 2 used the repaired candidate readiness artifact, Foldseek
  `10.941cd33`, 12 query coordinates against all 672 staged materializable
  targets, `--threads 4`, and a 900-second runtime bound, but timed out before
  pair rows were emitted.
- SPOF hardening work: Yes. The aggregate removes the first query-chunk
  aggregation ambiguity: chunks 0-2 now show 3 attempted chunks, 2 completed
  chunks, 24 completed query coordinates, 28,251 mapped pair rows, 9,142
  train/test rows, max train/test TM-score `0.8957`, 70 target-violating
  row-level pairs, 13 reported violating structure pairs, and 54 non-completed
  chunks. It also prevents false success: the completed chunks fail `<0.7`,
  chunk 2 exceeds the routine runtime bound, `m_csa:372` and `m_csa:501`
  remain coordinate exclusions, all outputs remain review-only/non-countable,
  and `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T21:53:47Z run after clean startup gates
(`354` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  No M-CSA-only tranche should be opened without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected external pilot success criteria already exist, but
  pilot rows remain review-only with 0 import-ready rows and 0 countable
  candidates until active-site, duplicate-screening, representation, review,
  and full label-factory blockers are terminally resolved.
- Scientific generalization work: Yes for direct Foldseek/TM-score query-chunk
  evidence, but not for a full split claim. This run added
  `build-foldseek-tm-score-query-chunk-signal` and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json`
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json`.
  The direct commands used the repaired candidate readiness artifact, Foldseek
  `10.941cd33`, 12 query coordinates per chunk against all 672 staged
  materializable target coordinates, `--threads 4`, and a 900-second runtime
  bound. The chunks completed with 28,251 mapped pair rows, 9,142 train/test
  rows, max train/test TM-score `0.8957`, and 70 total target-violating
  row-level pairs. Chunk 0 reports six unique target-violating structure pairs;
  chunk 1 reports seven.
- SPOF hardening work: Yes. The new query-chunk path removes the
  all-at-once-only Foldseek runtime SPOF and creates a resumable route for the
  remaining 54 chunks. It also prevents false success: the current repaired
  split now has new exact target-failure evidence outside the expanded100 cap,
  chunk aggregation is incomplete, `m_csa:372` and `m_csa:501` remain
  coordinate exclusions, all outputs remain review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T20:53:13Z run after clean startup gates
(`349` unit tests passed and `validate` passed with 679 curated labels):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  No M-CSA-only tranche should be opened without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected pilot still has 10 rows, 0 terminal decisions, 0
  import-ready rows, 0 countable candidates, 3 active-site-source blockers, 10
  broader duplicate-screening blockers, 3 representation-control
  stability-change blockers, and 10 full-gate blockers.
- Scientific generalization work: Yes for direct Foldseek/TM-score full-run
  feasibility evidence, but not for a full split claim. This run added the
  compact all-materializable Foldseek summary path and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`.
  The direct command used all 672 staged materializable coordinates, Foldseek
  `10.941cd33`, `--threads 4`, and a 1,500-second runtime bound, but timed out
  before Foldseek emitted a result TSV. It therefore records 0 pair rows, no
  max train/test TM-score, and no target pass.
- SPOF hardening work: Yes. The new compact summary path removes the
  repository-bloat SPOF for future full Foldseek runs and the timeout artifact
  turns the uncapped all-materializable blocker into concrete runtime evidence.
  False-claim safety remains intact: the canonical holdout is unchanged,
  `m_csa:372` and `m_csa:501` remain coordinate exclusions, all outputs remain
  review-only/non-countable, and `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T19:52:23Z run after clean startup gates
(`346` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  No M-CSA-only tranche should be opened without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected pilot still has 10 rows, 0 terminal decisions, 0
  import-ready rows, 0 countable candidates, 3 active-site-source blockers, 10
  broader duplicate-screening blockers, 3 representation-control
  stability-change blockers, and 10 full-gate blockers.
- Scientific generalization work: Yes for direct Foldseek/TM-score split
  repair follow-through, but not for a full split claim. This run added
  `artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json`,
  and
  `artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json`.
  The actual repaired expanded100 Foldseek rerun uses the candidate holdout
  where `m_csa:34` is in-distribution, maps 27,542 pair rows, evaluates 6,930
  heldout/in-distribution train/test pairs, and records max train/test TM-score
  `0.6993` with 0 target-violating pairs in the companion audit.
- SPOF hardening work: Yes. The new artifacts remove the projection-only
  ambiguity for the computed repaired subset while preserving false-claim
  safety: the canonical holdout is unchanged, the source signal is still capped
  at 100/672 staged coordinates, `m_csa:372` and `m_csa:501` remain explicit
  coordinate exclusions, all rows remain review-only/non-countable, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T18:51:29Z run after clean startup gates
(`340` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  No M-CSA-only tranche should be opened without new source-scale evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The selected pilot still has 10 rows, 0 terminal decisions, 0
  import-ready rows, 0 countable candidates, 3 active-site-source blockers, 10
  broader duplicate-screening blockers, 3 representation-control
  stability-change blockers, and 10 full-gate blockers.
- Scientific generalization work: Yes, for direct Foldseek/TM-score split
  repair planning, but not for a full split. This run added
  `artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json`, which consumes
  the target-failure audit and sequence holdout. The observed blocking pair
  `m_csa:33`/`m_csa:34` has one conservative review-only repair candidate:
  move held-out out-of-scope `m_csa:34` to in-distribution before regenerating
  sequence-holdout metrics. The projected held-out count is 135, all 44
  held-out in-scope rows remain held out, and observed blocking pairs in the
  supplied signal project to 0 after repair. The companion projection artifact
  `artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json` applies
  that move only in memory over the expanded100 Foldseek rows: source
  train/test violations drop from 48 to 0 and max train/test TM-score drops
  from `0.7515` to `0.6993`. The candidate repaired sequence holdout
  `artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json`
  applies the move to a copy: 135 held-out rows, 44 held-out in-scope rows, 0
  held-out out-of-scope false non-abstentions, and no remaining held-out
  overlap with the moved `mmseqs30:m_csa:34` cluster.
- SPOF hardening work: Yes. The new plan prevents the exact Foldseek target
  violation from staying as an aggregate blocker while preserving false-claim
  safety: the repaired holdout is a candidate copy only, downstream artifacts
  are not rebuilt from it, the source Foldseek signal remains partial, the
  uncapped Foldseek split remains uncomputed, and
  `full_tm_score_holdout_claim_permitted=false`.

Recorded for the 2026-05-14T17:50:46Z run after clean startup gates
(`336` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview adds 0 clean countable labels, and
  the source-scale audit remains capped at 1,003 observed M-CSA source records.
  No M-CSA-only tranche should be opened without new source-scale evidence.
- External-source repair/import: Yes for review-only representation repair; no
  for import and no new countable external candidates. This run added
  `artifacts/v3_external_source_pilot_representation_adjudication_1025.json`
  and refreshed `artifacts/v3_external_source_pilot_success_criteria_1025.json`.
  The pilot still has 10 selected rows, 0 terminal decisions, 0 import-ready
  rows, 0 countable candidates, 3 active-site-source blockers, 10 broader
  duplicate-screening blockers, and 10 full-gate blockers, but the generic
  representation-control surface is now 3 stable review-only rows, 4
  representation near-duplicate holdouts, and 3 unresolved stability-change
  review rows.
- Scientific generalization work: Yes, for direct Foldseek/TM-score target
  failure evidence but not for a full split. This run added
  `artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json`, which shows
  the current sequence-holdout split already violates the `<0.7` target via
  one unique train/test structure pair, `m_csa:33`/`m_csa:34`
  (`pdb:1JC5`/`pdb:1MPY`), max pair TM-score `0.7515`, across 48 chain-level
  violating rows. The full TM-score holdout claim remains false.
- SPOF hardening work: Yes. The new Foldseek audit turns the aggregate
  expanded100 max TM-score into exact blocking-pair evidence, so extending the
  capped run alone cannot be mistaken for a pass path. The selected-pilot
  representation adjudication also removes stale generic representation-process
  ambiguity while preserving review-only/non-countable safeguards and the 650M
  cache-miss blocker.

Recorded for the 2026-05-14T16:50:02Z run after clean startup gates
(`335` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview still adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. No M-CSA-only tranche should be opened without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The pilot success artifact still reports 10 selected rows, 0
  terminal decisions, 0 import-ready rows, 0 countable candidates, 3
  active-site-source blockers, 10 broader-duplicate-screening blockers, 9
  representation-control blockers, and 10 full-gate blockers.
- Scientific generalization work: Yes, for direct Foldseek/TM-score blocker
  narrowing but not for a full split. This run completed
  `artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json` from the
  all-materializable sidecar using Foldseek `10.941cd33`: 100 staged
  coordinates, 27,542 mapped pair rows, 7,317 heldout/in-distribution
  train/test pairs, max observed train/test TM score `0.7515`, 0 unmapped raw
  names, and 0 countable/import-ready rows. The `<0.7` target is still not
  achieved, 572 staged coordinates remain uncomputed, and
  `full_tm_score_holdout_claim_permitted` stays false.
- SPOF hardening work: Yes. The new expanded100 artifact and regression
  coverage make the latest Foldseek evidence durable while preserving
  false-full-claim blockers: cap-applied coverage is partial, two
  selected-structure coordinate exclusions remain (`m_csa:372`, `m_csa:501`),
  and the builder still emits a signal rather than a tested full TM-score
  split.

Recorded for the 2026-05-14T15:48:54Z run after clean startup gates
(`334` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview still adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. No M-CSA-only tranche should be opened without new source-scale
  evidence.
- External-source repair/import: No for import and no new countable external
  candidates. The current pilot success artifact still reports 10 selected
  rows, 0 terminal decisions, 0 import-ready rows, 0 countable candidates, 3
  active-site-source blockers, 10 broader-duplicate-screening blockers, 9
  representation-control blockers, and 10 full-gate blockers.
- Scientific generalization work: Yes, for direct Foldseek/TM-score blocker
  narrowing but not for a full split. This run completed
  `artifacts/v3_foldseek_tm_score_signal_1000_expanded80.json` from the
  all-materializable sidecar using Foldseek `10.941cd33`: 80 staged
  coordinates, 18,591 mapped pair rows, 5,666 heldout/in-distribution train/test
  pairs, max observed train/test TM score `0.7515`, 0 unmapped raw names, and 0
  countable/import-ready rows. The `<0.7` target is still not achieved, 592
  staged coordinates remain uncomputed, and `full_tm_score_holdout_claim_permitted`
  stays false.
- SPOF hardening work: Yes. The new expanded80 artifact and regression coverage
  make the latest Foldseek evidence durable while preserving false-full-claim
  blockers: cap-applied coverage is partial, two selected-structure coordinate
  exclusions remain (`m_csa:372`, `m_csa:501`), and the builder still emits a
  signal rather than a tested full TM-score split.

Recorded for the 2026-05-14T14:46:52Z run after clean startup gates
(`332` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The accepted countable slice remains 1,000 with
  679 canonical labels, the 1,025 preview still adds 0 clean countable labels,
  and the source-scale audit remains capped at 1,003 observed M-CSA source
  records. No new M-CSA tranche should be opened without a source-scale audit
  showing new usable M-CSA records.
- External-source repair/import: Yes for repair evidence and pilot readiness
  definition; no for import. This run added
  `artifacts/v3_external_source_pilot_success_criteria_1025.json`, which makes
  pilot success measurable across candidate count, terminal decisions,
  active-site source resolution, broader duplicate screening, representation
  adjudication, review decisions, full label-factory gates, import-ready rows,
  and countable-label candidates. Current status is `needs_more_work`: 10
  selected rows, 0 terminal decisions, 0 import-ready rows, 0 countable
  candidates, 7 explicit active-site rows, 3 binding-context-only active-site
  rows, broader duplicate screening and full label-factory gates unresolved for
  all 10, and representation-control blockers on 9 rows.
- Scientific generalization work: Yes, for Foldseek blocker clarification but
  not for a new full split. The real MMseqs2 sequence-distance holdouts remain
  the accepted sequence evidence. The all-materializable Foldseek readiness
  artifact now explicitly excludes `m_csa:372` and `m_csa:501` from coordinate
  materialization because both have `geometry_status=no_structure_positions`
  and `selected_structure_id=null` in current evidence. Foldseek/TM-score
  remains partial: expanded60 still has max train/test TM score `0.7515`,
  misses the `<0.7` target, leaves 612 staged coordinates uncomputed, and
  cannot claim a full TM-score holdout.
- SPOF hardening work: Yes. The external pilot no longer treats evidence
  packet completion as an implicit success condition; the success criteria now
  explicitly distinguish operational success, scientific/import success,
  needs-more-work states, process-missing failures, and evidence-explained
  zero-pass outcomes while keeping all outputs review-only and non-countable.
  The Foldseek readiness path also no longer leaves the two unmaterializable
  selected-structure rows ambiguous: they are explicit coordinate exclusions
  with evidence.

Recorded for the 2026-05-14T13:45:19Z run after clean startup gates
(`331` unit tests passed and `validate` passed):

- M-CSA-only count growth: No. The 1,025 preview still adds 0 accepted clean
  labels, source-scale is capped at 1,003 observed M-CSA records, and current
  hard-negative, false-non-abstention, near-miss, and actionable-failure checks
  remain clean but do not create more M-CSA source headroom.
- External-source repair/import: No for import; yes only for review-only repair
  evidence. Backend current-reference MMseqs2 search debt is cleared for the
  28 no-signal external rows, but 2 exact sequence holdouts, 3 selected-pilot
  binding-context-only active-site rows, broader duplicate screening,
  representation-review debt, expert-review no-decision artifacts, and full
  factory gates still block every external row from import.
- Scientific generalization work: Yes. The accepted-registry 1,000 and 1,025
  MMseqs2 holdouts are real backend evidence: `/opt/homebrew/bin/mmseqs`
  version `18-8cc5c`, 738 sequence records, 678/678 evaluated rows with
  sequence coverage, 30% identity and 80% coverage clustering, 136 held-out
  rows by whole clusters, max observed train/test identity `0.284`, target
  <=30% achieved, and 0 held-out out-of-scope false non-abstentions. This run
  hardened the artifacts with explicit backend, resolved path,
  cluster-threshold, target-achievement, and limitation metadata aliases.
  Foldseek remains absent from default `PATH`; the prior temp-env Foldseek
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`
  remains the documented path. This run added a bounded expanded60 Foldseek
  signal from the all-materializable coordinate sidecar: 60 staged coordinates,
  12,329 mapped pair rows, 3,716 heldout/in-distribution train/test pairs, max
  train/test TM score `0.7515`, and 0 countable/import-ready rows. The partial
  signal removes the expanded40 ceiling, but the `<0.7` target is not achieved
  on the computed subset and full Foldseek/TM-score split remains blocked by
  `m_csa:372`, `m_csa:501`, the 612 capped-out staged coordinates, and the
  unrun full split builder.
- SPOF hardening work: Yes. Sequence holdout metadata is now less brittle for
  downstream gates and reviewers while preserving the proxy fallback path and
  pinned regression coverage. Existing external artifact lineage,
  review-only audits, and Foldseek false-full-claim blockers remain in force.

## Recent Project Progress

- Added `aggregate-foldseek-tm-score-query-chunks` plus
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_of_056.json`.
  The aggregate consumes chunks 0-2, keeps the timed-out chunk 2 visible, and
  records 3 attempted chunks, 2 completed chunks, 24 completed query
  coordinates, 28,251 mapped pair rows, 9,142 train/test rows, max train/test
  TM-score `0.8957`, 70 target-violating row-level pairs, 13 reported
  violating structure pairs, and 54 non-completed chunks. It is review-only,
  non-countable, not import-ready, and keeps
  `full_tm_score_holdout_claim_permitted=false`.
- Added
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json`.
  Chunk 2 uses the same all-target query-chunk command shape as chunks 0-1
  but times out after 900 seconds before pair rows are emitted. This is a
  concrete runtime blocker for that query range, not a failed validation gate
  and not a full TM-score signal.
- Added `build-foldseek-tm-score-query-chunk-signal`, a resumable Foldseek
  query-chunk command that searches a deterministic query slice against all
  staged materializable target coordinates and keeps compact summary evidence.
  The first direct chunk artifacts,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json`,
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json`,
  use the repaired candidate readiness artifact, 24 total query coordinates,
  all 672 staged targets, Foldseek `10.941cd33`, `--threads 4`, and a
  900-second timeout per chunk. They completed with 28,251 mapped pair rows,
  9,142 train/test rows, max train/test TM-score `0.8957`, and 70 total
  target-violating row-level pairs. This removes the all-at-once-only runtime
  SPOF, but full query aggregation is incomplete and both chunks now prove the
  repaired split still fails the `<0.7` target beyond the expanded100 cap.
- Added `build-foldseek-tm-score-all-materializable-signal`, a compact
  all-materializable Foldseek summary command that records command/version,
  coordinate coverage, coordinate exclusions, mapped-pair counts, target status,
  top train/test pairs, and blocking pairs without committing every Foldseek
  pair row. The first direct run wrote
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`
  from the repaired candidate readiness artifact. The latest staged signal now
  covers all 672 staged materializable coordinates with Foldseek `10.941cd33`
  and `--threads 4`, maps 952,922 pair rows and 274,241 train/test rows, and
  fails the `<0.7` target at max train/test TM-score `0.9749` with 4,715
  target-violating train/test rows. It keeps `m_csa:372`/`m_csa:501` as the
  coordinate exclusions and preserves 0 countable/import-ready rows with
  `full_tm_score_holdout_claim_permitted=false`.
- Added
  `artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json`,
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json`,
  and
  `artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json`.
  The coordinate-readiness artifact consumes the candidate sequence holdout and
  moves `m_csa:34` to in-distribution while keeping 672 materialized
  coordinates and the two coordinate exclusions. The actual Foldseek rerun uses
  the same 100-coordinate cap as expanded100 under the repaired partition:
  27,542 mapped pair rows, 6,930 train/test rows, max train/test TM-score
  `0.6993`, and 0 target-violating pairs. This removes the projection-only
  blocker for the computed subset, but the canonical holdout is unchanged and a
  full all-materializable split remains uncomputed.
- Added `artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json` plus CLI
  and regression coverage. The plan consumes the target-failure audit and
  sequence holdout, names `m_csa:34` as the only held-out row that must move to
  repair the observed `m_csa:33`/`m_csa:34` TM-score split violation, and
  records that the move preserves all 44 held-out in-scope rows while reducing
  projected held-out count from 136 to 135. It keeps the repair unapplied,
  review-only, non-countable, and not import-ready; the full all-materializable
  Foldseek split remains uncomputed and no full holdout claim is permitted.
- Added `artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json`.
  This projection applies the proposed `m_csa:34` move only to existing
  expanded100 Foldseek pair rows, reducing source train/test violations from 48
  to 0 and projected max train/test TM-score from `0.7515` to `0.6993`.
  Because the sequence holdout and downstream metrics are not regenerated and
  572 staged coordinates remain uncomputed, the projection remains review-only
  and non-claiming.
- Added `artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json`.
  This candidate applies the repair to a copy of the sequence holdout, moves
  `m_csa:34` from held-out to in-distribution, preserves all 44 held-out
  in-scope rows, keeps held-out out-of-scope false non-abstentions at 0, and
  records no remaining held-out overlap with the moved MMseqs2 cluster. It is
  not canonical and downstream artifacts have not been rebuilt from it.
- Added `artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json` plus
  CLI and regression coverage. The audit consumes the expanded100 Foldseek
  signal and identifies the exact current-split target blocker: one unique
  train/test structure pair, `m_csa:33`/`m_csa:34` (`pdb:1JC5`/`pdb:1MPY`),
  reaches max pair TM-score `0.7515` across 48 chain-level violating rows.
  This keeps `full_tm_score_holdout_claim_permitted=false` and changes the next
  Foldseek work from "keep increasing capped coverage" to split
  repair/exclusion review plus any later full-signal confirmation.
- Added
  `artifacts/v3_external_source_pilot_representation_adjudication_1025.json`
  and refreshed
  `artifacts/v3_external_source_pilot_success_criteria_1025.json`. The
  selected-pilot representation surface is now concrete: 3 stable review-only
  controls, 4 representation near-duplicate holdouts, and 3 stability-change
  rows requiring representation review. The success artifact remains
  `needs_more_work` with 0 terminal decisions, 0 import-ready rows, and 0
  countable candidates; broader duplicate screening and full label-factory
  gates still block all 10 selected rows.
- Completed a direct bounded expanded100 Foldseek/TM-score signal from
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`.
  The command used `/private/tmp/catalytic-foldseek-env/bin/foldseek` version
  `10.941cd33`, `--max-staged-coordinates 100`, and
  `--prior-staged-coordinate-count 80`. The new
  `artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json` records 27,542
  mapped pair rows, 838 heldout pair rows, 7,317 heldout/in-distribution
  train/test rows, 19,387 in-distribution pair rows, max observed train/test TM
  score `0.7515`, 0 unmapped raw Foldseek names, and explicit 0
  countable/import-ready rows. It removes the expanded80 partial-signal ceiling
  only. It remains review-only/non-countable because the `<0.7` target fails on
  the computed subset, the cap leaves 572 staged coordinates uncomputed, and
  `tm_score_split_computed=false` plus `full_tm_score_split_computed=false`
  remain true.
- Completed a direct bounded expanded80 Foldseek/TM-score signal from
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`.
  The command used `/private/tmp/catalytic-foldseek-env/bin/foldseek` version
  `10.941cd33`, `--max-staged-coordinates 80`, and
  `--prior-staged-coordinate-count 60`; runtime was 1,232 seconds. The new
  `artifacts/v3_foldseek_tm_score_signal_1000_expanded80.json` records 18,591
  mapped pair rows, 827 heldout pair rows, 5,666 heldout/in-distribution
  train/test rows, 12,098 in-distribution pair rows, max observed train/test TM
  score `0.7515`, 0 unmapped raw Foldseek names, and explicit 0
  countable/import-ready rows. It removes the expanded60 partial-signal ceiling
  only. It remains review-only/non-countable because the `<0.7` target fails on
  the computed subset, the cap leaves 592 staged coordinates uncomputed, and
  `tm_score_split_computed=false` plus `full_tm_score_split_computed=false`
  remain true.
- Added explicit external pilot success criteria in
  `artifacts/v3_external_source_pilot_success_criteria_1025.json` plus CLI,
  regression coverage, and docs. The artifact keeps all rows review-only and
  records `pilot_status=needs_more_work`: 10 selected candidates, 0 terminal
  decisions, 0 import-ready rows, 0 countable candidates, 7 explicit
  active-site-source rows, 3 binding-context-only rows, broader duplicate
  screening and full label-factory gates unresolved for all 10, and 9
  representation-control unresolved rows. This removes the external-pilot
  "evidence assembled equals success" ambiguity without authorizing import.
- Hardened the all-materializable Foldseek coordinate-readiness artifact with
  explicit coordinate exclusions for `m_csa:372` and `m_csa:501`. Both rows
  have `geometry_status=no_structure_positions`, `selected_structure_id=null`,
  and `selected_structure_key=missing_selected_structure` in current evidence,
  so they are excluded from Foldseek coordinate materialization rather than
  left as ambiguous missing structures. The artifact still stages 672
  supported selected PDB coordinates with 0 fetch failures, keeps 0
  countable/import-ready rows, and does not permit a full TM-score holdout
  claim.
- Hardened the accepted-registry sequence-distance holdout backend metadata for
  the 1,000 and 1,025 contexts. The regenerated artifacts keep the same
  MMseqs2 result (`18-8cc5c`, 738 sequence records, 136 held-out rows, max
  train/test identity `0.284`, target <=30% achieved, 0 held-out out-of-scope
  false non-abstentions) and now expose explicit `backend`,
  `backend_resolved_path`, `cluster_threshold`, `target_identity_achieved`,
  `target_max_train_test_identity`, and `limitations` fields. Regression tests
  pin both the real MMseqs2 path and the proxy fallback metadata. Tool check
  found `mmseqs`, `blastp`, `makeblastdb`, and `diamond` on `PATH`; `foldseek`
  was not on `PATH`, so the documented temp-env Foldseek path remains required.
- No-code delegated Foldseek attempt at 2026-05-14T11:42:35Z. The parent
  automation acquired the lock, synced `origin/main`, verified `mmseqs`,
  `blastp`, `makeblastdb`, and `diamond` on PATH plus Foldseek
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`,
  ran 331 unit tests and validation cleanly, and instructed a worker to build
  `artifacts/v3_foldseek_tm_score_signal_1000_all_materializable.json` from
  the all-materializable coordinate sidecar. The worker did not return within
  the wrap-up window and was shut down; the parent worktree stayed clean and no
  implementation or artifact changes were integrated. The next agent should
  retry the delegated all-materializable Foldseek/TM-score signal or a bounded
  larger-than-40 cap, keeping the two missing selected-structure blockers
  (`m_csa:372`, `m_csa:501`) and all review-only/non-countable claims intact.
- Completed a bounded expanded60 Foldseek/TM-score signal from
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`.
  The command used `/private/tmp/catalytic-foldseek-env/bin/foldseek` version
  `10.941cd33`, `--max-staged-coordinates 60`, and
  `--prior-staged-coordinate-count 40`; runtime was 777.55 seconds. The new
  `artifacts/v3_foldseek_tm_score_signal_1000_expanded60.json` records 12,329
  mapped pair rows, 457 heldout pair rows, 3,716 heldout/in-distribution
  train/test rows, 8,156 in-distribution pair rows, max observed train/test TM
  score `0.7515`, 0 unmapped raw Foldseek names, and explicit 0
  countable/import-ready rows. It removes the expanded40 partial-signal
  ceiling only. It remains review-only/non-countable because the `<0.7` target
  fails on the computed subset, the cap leaves 612 staged coordinates
  uncomputed, and `tm_score_split_computed=false` plus
  `full_tm_score_split_computed=false` remain true.
- Staged all currently materializable selected Foldseek coordinates for the
  accepted 1,000 context in
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`:
  672 unique selected PDB mmCIF sidecars, 676 materializable evaluated rows,
  0 fetch failures, and 0 supported selected structures left unstaged. This
  removes the unstaged selected-coordinate sidecar blocker while keeping
  `tm_score_split_computed=false` and `full_tm_score_split_computed=false`.
  Full TM-score split work remains blocked by `m_csa:372`, `m_csa:501`, and the
  unrun all-materializable Foldseek split builder.
- Added
  `artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json`
  plus CLI and transfer-gate wiring. The artifact classifies the 10 selected
  external pilot rows as review-only evidence decisions: 7 rows have explicit
  active-site source evidence, 3 rows remain binding-context-only, 0 rows are
  countable, and 0 rows are import-ready. The external transfer gate now checks
  the artifact as part of the typed input contract and passes 68/68 checks.
- Hardened the 650M representation-readiness path without claiming a real 650M
  run. The mapped-control and selected-pilot 650M sidecars now record the 650M
  cache miss, requested dimension `1280`, computed fallback backend
  `esm2_t30_150m_ur50d`, actual dimension `640`, and
  `requested_650m_or_larger_representation_backend_not_computed`. The stability
  sidecars report `fallback_changed` while all rows remain review-only and
  non-countable: mapped controls have 3 nearest-reference changes and 4
  heuristic-disagreement-status changes, while selected pilot rows have 4
  nearest-reference changes and 3 heuristic-disagreement-status changes.
- Expanded Foldseek coordinate readiness from 25 to 100 staged selected PDB
  coordinates in `artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json`
  with 0 fetch failures. The bounded expanded40 Foldseek signal in
  `artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json` now completes as
  partial staged-coordinate review evidence: 5,699 pair rows, all 5,699 safely
  mapped rows, 1,633 heldout/in-distribution train/test pairs, max train/test
  TM score `0.7515`, 0 unmapped raw Foldseek names, and 0
  countable/import-ready rows. It removes the staged25-only proof blocker and
  the expanded40 raw-name mapping blocker, but stays non-countable/not
  import-ready because full TM-score split remains false and the partial signal
  does not achieve the `<0.7` target. The CLI now accepts
  `--max-staged-coordinates` plus `--prior-staged-coordinate-count`, capped
  runs use a dedicated selected-coordinate search directory, and the artifact
  explicitly blocks full holdout claims while coverage remains partial.
- Added a bounded Foldseek coordinate-readiness path for the accepted 1,000
  context. `build-foldseek-coordinate-readiness` records explicit Foldseek
  provenance, selected-structure materialization readiness, missing selected
  structures, fetch failures, and review-only/non-countable status without
  computing or claiming a TM-score split. The current artifact stages 25
  selected PDB mmCIF files, identifies 676 materializable evaluated rows and
  missing selected structures for `m_csa:372` and `m_csa:501`, and keeps
  `tm_score_split_computed=false`.
- Added `artifacts/v3_foldseek_tm_score_signal_1000_staged25.json`, a partial
  review-only Foldseek `easy-search` signal over only the 25 staged coordinate
  files. It records 1,840 mapped pair rows, 532 staged heldout/in-distribution
  pair rows, max staged train/test TM score `0.6426` against the `<0.7`
  target, 0 countable/import-ready rows, and keeps
  `full_tm_score_split_computed=false`.
- Refreshed the downstream selected-pilot chain after the 1,025 backend
  sequence-search update. `v3_external_source_pilot_candidate_priority_1025`,
  review-decision export, evidence packet, pilot representation plan/sample,
  evidence dossiers, and the transfer gate now agree with the blocker matrix:
  the same 10 selected rows remain review-only/non-countable, all 10 carry
  backend no-near-duplicate status in the pilot packet/dossiers, stale
  complete-near-duplicate blockers are absent from selected no-signal rows, and
  the transfer gate still passes 67/67.
- Recovered a stale automation lock with a dirty worktree and finalized the
  coherent in-progress label-factory scaling work rather than starting a
  conflicting tranche.
- Accepted gated 625-, 650-, 675-, and 700-entry label-factory batches. The
  675 batch added only `m_csa:666`; the 700 batch added `m_csa:686`,
  `m_csa:688`, `m_csa:694`, `m_csa:697`, and `m_csa:699`.
- Tightened provisional review rules so Ser-His mechanism text paired with a
  metal-dependent top hit stays `needs_expert_review` unless explicit metal
  catalysis evidence is present.
- Added an active-learning gate requiring all unlabeled candidate rows to be
  retained even when the ranked queue is capped.
- Added `artifacts/v3_label_factory_batch_summary.json` to aggregate accepted
  batches, review debt, gate status, and active-queue retention.
- Added `artifacts/v3_review_debt_summary_650.json` to rank 53 evidence-gap
  rows for the next review pass.
- Added preview triage artifacts
  `artifacts/v3_review_evidence_gaps_675_preview.json` and
  `artifacts/v3_review_debt_summary_675_preview.json` so the 675 promotion
  decision can inspect evidence gaps first.
- Added `artifacts/v3_label_factory_preview_summary_675.json` to summarize the
  unpromoted preview's acceptance, pending-review, gate, and queue-retention
  metrics.
- Added `artifacts/v3_label_preview_promotion_readiness_675.json`; it is
  mechanically ready but recommends review before promotion because preview
  review debt increased, and it carries new-debt entry ids and next-action
  counts for audit. The gate requires preview summary counts to match
  acceptance and explicit unlabeled-candidate retention.
- After the preview-readiness gate was in place, used the remaining productive
  work window to expose carried/new debt entry ids and next-action counts in
  durable artifacts and regression tests.
- Added `work/label_preview_675_notes.md` with the accepted-label profile and
  top evidence gaps to inspect before promotion.
- Added `artifacts/v3_label_scaling_quality_audit_675_preview.json` and a
  batch-acceptance review-gap gate. The 675 preview now defers
  below-threshold evidence-limited negatives instead of counting them.
- Added graph-derived exact-UniProt sequence-cluster proxy artifacts for 675
  and 700 and attached them to scaling-quality audits; both report 0 missing
  assignments and 0 near-duplicate hits among audited rows.
- Extended geometry slice summaries, regression tests, and performance timing
  through the 700-entry countable slice.
- Added `work/label_preview_700_notes.md` with the accepted-label profile and
  highest-priority 700 review-debt rows.
- Remaining-time plan executed before wrap-up: after the 700 gate accepted five
  clean labels but review debt rose to 81 rows, stopped tranche growth and
  focused on sequence-cluster audit coverage, review-debt notes, regression
  tests, and documentation.
- Added `analyze-review-debt-remediation` and
  `scan-review-debt-alternate-structures` so accepted-700 review debt is
  repairable without counting new labels. The focused 20-row remediation
  artifact, full 81-row remediation artifact, and 152-PDB alternate-structure
  scan now keep structure-wide cofactor hits separate from local active-site
  support.
- Remaining-time plan for the 700 review-debt repair run: after the remediation
  commands and target regression tests passed before the productive-work
  boundary, rerun the deterministic remediation, scaling-quality audit, batch
  summary, validation, and full test suite; use any remaining time to check
  docs for stale current-state claims rather than opening another tranche.
- Remaining-time plan executed for the remap run: after conservative
  alternate-PDB residue remapping worked on the focused 700 scan, used the
  remaining productive window to run a complete all-debt bounded scan, add a
  review-only remap lead summary command, regenerate artifacts, and verify
  targeted tests instead of reopening label count growth.
- Remaining-time plan for the expert-decision run: after the dedicated
  expert-label decision export passed, use the remaining productive window to
  harden countable-import refusal, add repair-candidate ranking, make the gate
  and scaling audit require the repair-candidate summary, refresh artifact
  regression coverage, and document the next non-countable repair subset
  instead of reopening 725+ label growth.
- Remaining-time plan executed for this recovery run: after the local-evidence
  gap audit was coherent and tests passed, added a dedicated local-evidence
  review export, no-decision batch, repair plan, factory/scaling-quality gates,
  and countable-import refusal before updating docs. Count growth stayed
  stopped at 624 labels.
- This run reduced review-only local-evidence debt without count growth:
  the 4 reaction/substrate repair lanes (`m_csa:592`, `m_csa:643`,
  `m_csa:654`, `m_csa:662`) are closed as reviewed out-of-scope repair-only
  rows, the 3 explicit alternate-residue lanes (`m_csa:567`, `m_csa:578`,
  `m_csa:667`) now have concrete sourcing requests across 34 alternate PDB
  structures, and the review-only import-safety audit confirms the mismatch,
  expert-decision, and local-evidence decision batches add 0 countable labels.
- Implemented the expert-reviewed ATP/phosphoryl-transfer fingerprint-family
  expansion for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP.
  The expansion is wired through ontology records, reaction/substrate mismatch
  review export mapping, family-propagation blockers, active-learning priority,
  adversarial negatives, gate checks, scaling-quality audit, regression tests,
  and documentation while keeping every mapped row non-countable.
- Accepted the gated 725-entry label-factory batch. The batch added
  `m_csa:705`, `m_csa:709`, `m_csa:714`, `m_csa:716`, `m_csa:723`, and
  `m_csa:727` as clean countable labels, raising the canonical registry to 630
  labels while leaving 100 review-state rows non-countable.
- Added accepted-725 review-only repair artifacts: expert-label decision export
  for 95 rows, 25-row local-evidence gap audit/export/repair plan, 8 explicit
  alternate residue-position requests, review-only import-safety audit, focused
  alternate-structure scan, remap-local audit for `m_csa:712`, ontology-gap
  audit, learned-retrieval manifest, sequence-similarity failure-set audit, and
  scaling-quality audit.
- Added `artifacts/v3_accepted_review_debt_deferral_audit_725.json`, which
  explicitly defers all 100 accepted-725 review-state rows with 0 countable
  candidates and upgrades the 725 gate to 21/21 checks.
- Accepted the gated 750-entry label-factory batch. The batch added
  `m_csa:728`, `m_csa:733`, `m_csa:735`, `m_csa:739`, `m_csa:740`,
  `m_csa:742`, and `m_csa:750` as clean countable labels, raising the
  canonical registry to 637 labels while leaving 118 review-state rows
  non-countable.
- Added `artifacts/v3_accepted_review_debt_deferral_audit_750.json`, which
  explicitly defers all 118 accepted-750 review-state rows with 0 countable
  candidates and upgrades the post-batch 750 gate to 20/20 checks.
- Accepted the gated 775-entry label-factory batch. The batch added
  `m_csa:754`, `m_csa:758`, `m_csa:759`, `m_csa:762`, and `m_csa:776` as
  clean countable labels, raising the canonical registry to 642 labels while
  leaving 138 review-state rows non-countable.
- Tightened the provisional Ser-His hydrolase path so `m_csa:771`-style
  Ser-His text with counterevidence remains `needs_more_evidence` and is
  classified as a text-leakage risk rather than counted.
- Accepted the gated 800-, 825-, and 850-entry label-factory batches. The
  batches added ten clean countable labels total, raising the canonical
  registry to 652 labels while leaving 203 review-state rows non-countable.
- Added geometry-feature row reuse through `build-geometry-features
  --reuse-existing` so bounded tranches can reuse unchanged geometry rows
  instead of rebuilding every prior entry.
- Tightened provisional metal-hydrolase promotion so `m_csa:836`-style
  role-inferred metal-hydrolase candidates without local ligand support remain
  `needs_more_evidence` rather than counted.
- Accepted the gated 875-, 900-, 925-, and 950-entry label-factory batches.
  The batches added 21 clean countable labels total, raising the canonical
  registry to 673 labels while leaving 282 review-state rows non-countable.
- Added `expert_review_decision_needed` as an explicit scaling-quality issue
  class so PLP-supported rows such as `m_csa:865` are classified as
  non-countable external-review debt rather than blocking promotion as
  unclassified review debt.
- Accepted the gated 975- and 1,000-entry label-factory batches, raising the
  canonical registry to 679 countable labels while leaving 326 review-state
  rows non-countable.
- Opened the bounded 1,025 preview. The preview gate passes 21/21 checks, but
  acceptance is false because it adds 0 clean countable labels and review debt
  rises to 329 rows. The source-scale audit records 1,003 observed M-CSA source
  records and shifts next work toward external-source transfer.
- Added external-source transfer scaffolding for the post-M-CSA path:
  source-limit audit, transfer manifest, query manifest, OOD calibration plan,
  30-row UniProtKB/Swiss-Prot read-only candidate sample, guardrail audit,
  artifact regression tests, and unit tests. All external candidates are
  non-countable.
- Hardened the external-source transfer path with a review-only candidate
  manifest, candidate-manifest audit, lane-balance audit, evidence plan,
  evidence request export, external review-only import-safety audit, 11/11
  transfer gate, bounded Rhea reaction-context sample, and reaction-context
  guardrail audit. The canonical registry remains at 679 labels; 0 external
  labels are countable.
- Added broad/incomplete EC routing and a review-only active-site evidence
  queue for the external path: seven candidates require broad-EC attention,
  three broad-only rows are deferred before active-site mapping, 25 candidates
  are queued for active-site evidence, and 0 external labels are countable.
- Advanced the external path from evidence queue to bounded review-only
  controls: sampled UniProtKB active-site features for all 25 ready external
  rows, found 15 active-site-feature-supported candidates and 10 feature gaps,
  queued 12 candidates for heuristic-control prototyping, mapped all 12
  heuristic-ready controls onto current AlphaFold CIF structures, ran the
  current geometry heuristic, and recorded a metal-hydrolase top1 collapse plus
  9 scope/top1 mismatches in
  `artifacts/v3_external_source_failure_mode_audit_1025.json`. The external
  transfer gate now passes 33/33 review-only checks and still adds 0 countable
  labels.
- Expanded external-source controls from the 4-control heuristic sample to all
  12 heuristic-ready AlphaFold controls, added review-only control-repair,
  representation-control, binding-context, full reaction-context, and
  sequence-holdout artifacts, and raised the external transfer gate to 33/33.
  External candidates still add 0 countable labels and are not import-ready.
- Added external-source repair controls for the prior repair pass: feature-proxy
  representation comparison, broad-EC disambiguation, active-site gap source
  requests, and a sequence-neighborhood plan. The external transfer gate now
  passes 38/38 review-only checks while keeping every external row non-countable.
- Added bounded sequence-neighborhood screening and candidate-level import
  readiness auditing. That intermediate external transfer gate passed 41/41
  review-only checks while keeping every external row non-countable and
  import-blocked.
- Added bounded sequence-alignment verification for the sequence-neighborhood
  top hits plus an active-site sourcing queue for the 10 external active-site
  gaps. That checkpoint raised the external transfer gate to 45/45 review-only
  checks while keeping every external row non-countable and import-blocked.
- Added source-review exports for active-site sourcing and complete sequence
  search, a representation-backend plan, and an integrated external blocker
  matrix. The external transfer gate now passes 53/53 review-only checks while
  keeping every external row non-countable and import-blocked.
- Added active-site sourcing resolution and representation backend samples for
  the external 1,025 transfer path. The active-site resolution re-checks all 10
  gap rows against UniProt feature evidence, finds 0 explicit active-site
  residue sources, and keeps 7 binding-plus-reaction rows and 3 reaction-only
  rows non-countable. The deterministic sequence k-mer baseline covers all 12
  planned representation controls and flags `P60174` as a representation
  near-duplicate holdout; the canonical ESM-2 sample covers all 12 controls,
  flags 3 representation near-duplicate holdouts, and keeps the external
  transfer gate at 59/59 review-only checks with 0 import-ready labels.
- Added sequence/fold-distance holdout evaluation for the accepted countable
  registry in both the 1,000 and 1,025 slice contexts. No Foldseek, MMseqs2,
  BLAST, or DIAMOND executable was available locally, so
  `artifacts/v3_sequence_distance_holdout_eval_1000.json` and
  `artifacts/v3_sequence_distance_holdout_eval_1025.json` explicitly label the
  split as a deterministic proxy using exact UniProt reference clusters,
  selected-structure identifiers, and active-site geometry buckets. The
  held-out partition has 136 rows, 135/136 rows passing the strict
  low-neighborhood proxy, 0 out-of-scope false non-abstentions, held-out
  evaluable in-scope top1 accuracy and retention of `0.9767`, and
  top1/top3 accuracy among retained held-out evaluable rows of `1.0000`.
- Added the first bounded learned representation backend sample for external
  pilot readiness. `artifacts/v3_external_source_representation_backend_sample_1025.json`
  computes 12 ESM-2 (`facebook/esm2_t6_8M_UR50D`) candidate-control rows with
  320-dimensional embeddings, keeps all rows review-only and non-countable,
  flags 3 representation-near-duplicate holdouts, and emits 12
  learned-vs-heuristic disagreement rows. The existing 12-row deterministic
  k-mer sample remains the baseline/proxy control, and heuristic geometry
  retrieval remains attached as the required baseline.
- Hardened external transfer artifact graph consistency for the 1,025 pilot
  path. `check-external-source-transfer-gates` now validates artifact-path
  lineage across all 61 supplied external artifacts, records the clean
  1,025 lineage under
  `artifacts/v3_external_source_transfer_gate_check_1025.json`, and fails fast
  on mixed-slice paths or payload-declared slice contradictions before a gate
  artifact can silently pass.
- Added `artifacts/v3_external_source_pilot_evidence_dossiers_1025.json` as a
  review-only per-candidate evidence dossier for the 10 selected external
  pilot rows. It records active-site feature support, active-site sourcing
  status, Rhea reaction context, sequence alignment checks, structure mapping,
  heuristic control results, representation controls, and remaining blockers
  without making any row countable or import-ready.
- Added a pilot-specific representation backend path for the selected external
  worklist. `artifacts/v3_external_source_pilot_representation_backend_plan_1025.json`
  covers all 10 selected rows, and
  `artifacts/v3_external_source_pilot_representation_backend_sample_1025.json`
  computes review-only ESM-2 embeddings for all 10, flags `P55263` as a
  representation near-duplicate holdout, refreshes the pilot dossiers so every
  selected row has representation evidence, and keeps every external row
  non-countable and not import-ready.
- Added the real sequence-distance holdout backend for the accepted registry.
  `build-sequence-distance-holdout-eval` now accepts a FASTA and runs MMseqs2
  clustering at 30% identity and 80% coverage while retaining the deterministic
  proxy path as fallback context. The refreshed 1,000 and 1,025 holdout
  artifacts cover 678/678 evaluated labels, cluster 738 sequence records, hold
  out 136 rows by whole sequence clusters, record max train/test identity
  `0.284`, achieve the <=30% target, and keep held-out out-of-scope false
  non-abstentions at 0. Foldseek/TM-score separation remains absent, but
  `build-foldseek-coordinate-readiness` now records Foldseek provenance and
  bounded coordinate staging readiness.
- Added `artifacts/v3_foldseek_coordinate_readiness_1000.json` plus the
  bounded sidecar directory `artifacts/v3_foldseek_coordinates_1000/`. The
  artifact is review-only/non-countable, records explicit Foldseek
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`,
  identifies 678 evaluated rows, 676 rows with supported selected PDB
  coordinates, missing selected structures for `m_csa:372` and `m_csa:501`,
  and stages 25 selected PDB mmCIF files while keeping
  `tm_score_split_computed=false`.
  `artifacts/v3_foldseek_tm_score_signal_1000_staged25.json` then computes a
  partial staged-coordinate Foldseek TM signal over those 25 files only: 1,840
  mapped pair rows, 532 staged heldout/in-distribution pair rows, max staged
  train/test TM score `0.6426`, 0 countable/import-ready rows, and
  `full_tm_score_split_computed=false`.
- Added `work/foldseek_readiness_notes.md`. Foldseek is installable in the
  isolated temporary Conda environment `/private/tmp/catalytic-foldseek-env`
  and reports version `10.941cd33`. TM-score splitting remains blocked on
  materializing the remaining selected PDB/AlphaFold coordinates and adding
  the Foldseek split builder.
- Hardened mechanism-text counterevidence into explicit categories:
  structure/local-evidence counterevidence remains predictive safety evidence,
  while mechanism-text counterevidence is review context only and not valid for
  orphan discovery safety claims. The accepted-1,000 ablation artifact records
  157 changed rows, 156 review-debt rows, 20 top1 route changes, and 0
  structure/local guardrail losses.
- Extended the representation backend path to larger ESM-2 identifiers and
  added 650M sidecar/stability artifacts for mapped controls and selected pilot
  rows. The current 650M run is feasibility evidence only:
  `facebook/esm2_t33_650M_UR50D` was not cached locally, so sidecars record
  `model_unavailable_locally`, expected dimension `1280`, embedding failures,
  elapsed time, and 8M-vs-650M stability status without replacing the computed
  8M baseline.
- Added a real external-pilot backend sequence search for the 30-row
  UniProtKB/Swiss-Prot sample. `artifacts/v3_external_source_backend_sequence_search_1025.json`
  uses local MMseqs2 `18-8cc5c`, compares 30 external sequences against 735
  current accepted-reference accessions represented by 737 sequence records,
  preserves exact-reference holdouts `O15527` and `P42126`, records 28
  no-near-duplicate-signal rows and 0 backend failures, and keeps every row
  review-only, non-countable, and not import-ready.
- Wired the backend sequence-search artifact into external import-readiness,
  blocker-matrix, and transfer-gate artifacts. The complete-search blocker is
  removed only for backend no-signal rows; import readiness still reports 0
  import-ready rows, 2 sequence holdout/search rows, active-site gaps,
  representation-control issues, no expert decisions, and full factory-gate
  blockers. The external transfer gate now passes 67/67 review-only checks.

## Current Metrics

- Curated label registry: 682 bronze automation-curated labels, with 212
  seed-fingerprint positives and 470 out-of-scope labels. The external
  out-of-scope members are `uniprot:P06744`, `uniprot:P78549`, and
  `uniprot:Q3LXA3`.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 500-entry countable slice: threshold `0.4115`, 490/498 evaluated labeled
  rows evaluable, 127/131 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and `m_csa:494` preserved as non-countable.
- 525-entry countable slice: threshold `0.4115`, 514/522 evaluated labeled
  rows evaluable, 135/139 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 550-entry countable slice: threshold `0.4115`, 535/545 evaluated labeled
  rows evaluable, 140/144 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 575-entry countable slice: threshold `0.4115`, 552/562 evaluated labeled
  rows evaluable, 142/146 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 600-entry countable slice: threshold `0.4115`, 568/578 evaluated labeled
  rows evaluable, 143/147 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 625-entry countable slice: threshold `0.4115`, 584/598 evaluated labeled
  rows evaluable, 144/148 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 25 ready label candidates before the accepted
  batch decisions.
- 650-entry countable slice: threshold `0.4115`, 601/617 evaluated labeled
  rows evaluable, 147/151 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 31 ready label candidates before the accepted
  batch decisions.
- 675-entry countable slice: threshold `0.4115`, 601/618 evaluated labeled
  rows evaluable, 148/152 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 49 ready label candidates after accepting
  `m_csa:666`.
- 700-entry countable slice: threshold `0.4115`, 607/623 evaluated labeled
  rows evaluable, 153/157 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 64 ready label candidates after accepting the five
  clean 700 labels.
- 725-entry countable slice: threshold `0.4115`, 613/629 evaluated labeled
  rows evaluable, 159/163 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 85 ready label candidates before accepting six
  clean 725 labels.
- 750-entry countable slice: threshold `0.4115`, 620/636 evaluated labeled
  rows evaluable, 166/170 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 95 ready label candidates after accepting seven
  clean 750 labels.
- 775-entry countable slice: threshold `0.4115`, 625/641 evaluated labeled
  rows evaluable, 171/175 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 113 ready label candidates after accepting five
  clean 775 labels.
- 800-entry countable slice: threshold `0.4115`, 629/645 evaluated labeled
  rows evaluable, 175/179 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, and 4 evidence-limited
  in-scope abstentions after accepting four clean 800 labels.
- 825-entry countable slice: threshold `0.4115`, 632/648 evaluated labeled
  rows evaluable, 178/182 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, and 4 evidence-limited
  in-scope abstentions after accepting three clean 825 labels.
- 850-entry countable slice: threshold `0.4115`, 635/651 evaluated labeled
  rows evaluable, 181/185 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 97 bronze-to-silver promotion candidates after
  accepting three clean 850 labels.
- 950-entry countable slice: threshold `0.4115`, 656/672 evaluated labeled
  rows evaluable, 202/206 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 111 bronze-to-silver promotion candidates after
  accepting six clean 950 labels.
- Evidence-limited abstentions remain `m_csa:132`, `m_csa:353`, `m_csa:372`,
  and `m_csa:430`.
- Retained evidence-limited positives remain `m_csa:41`, `m_csa:108`,
  `m_csa:160`, `m_csa:446`, and `m_csa:486`; the smallest retained
  evidence-limited margin is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is still `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Label factory at 950: 111 bronze-to-silver promotions proposed, 389 active
  learning review rows queued, 100 adversarial negatives mined, 277 active
  expert-label decision rows routed through a review-only export, complete
  repair-candidate summary, priority repair guardrail audit, complete 84-row
  local-evidence gap audit/export, repair plan, review-only import-safety
  audit, ATP/phosphoryl-transfer family expansion, and 21/21 gate checks
  passing.
- Label batch summary: 19/19 accepted batches, 0 blockers, 0 hard negatives,
  0 near misses, 0 false non-abstentions, 0 actionable in-scope failures, and
  all active queues retained their unlabeled candidates.
- Latest accepted batch acceptance: 6 additional labels accepted for counting,
  282 review-state decisions pending, 673 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- Accepted-950 deferral audit: all 282 review-state rows explicitly remain
  non-countable, with 84 priority local-evidence rows audited/exported, 32
  explicit alternate residue-position requests, 19 new 950-preview review-debt
  rows classified and deferred, and 0 accepted-label overlap.
- Accepted-1000 current state: 679 countable labels, 326 review-state rows
  explicitly deferred, 21/21 gate checks passing, 0 hard negatives, 0 near
  misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures,
  and `m_csa:986` kept non-countable as a low-score local-heme boundary row.
- 1,025 preview state: 21/21 preview gate checks passing but 0 accepted new
  labels, so the preview is not promoted. Review debt rises to 329 rows with
  new rows `m_csa:1003`, `m_csa:1004`, and `m_csa:1005`; all remain
  non-countable. Source scaling is now the bottleneck: the graph exposes 1,003
  M-CSA records, and external-source transfer artifacts now provide a
  review-only UniProtKB/Swiss-Prot path with 30 non-countable sample candidates.
- Sequence/fold-distance holdout state: `artifacts/v3_sequence_distance_holdout_eval_1000.json`
  and `artifacts/v3_sequence_distance_holdout_eval_1025.json` evaluate the
  accepted countable registry under real MMseqs2 sequence clustering plus the
  retained proxy fields. Both contexts evaluate 678 labeled retrieval rows,
  cover all 678 with sequence evidence, cluster 738 sequence records at 30%
  identity and 80% coverage, and hold out 136 rows by whole sequence clusters.
  Max observed train/test identity is `0.284`, so the <=30% target is achieved.
  Held-out metrics are 44 in-scope rows, 43 evaluable in-scope rows, 92
  out-of-scope rows, 0 held-out out-of-scope false non-abstentions, and
  held-out evaluable top1 accuracy, top3 retained accuracy, and retention of
  `1.0000`. Foldseek/TM-score clustering is still not computed.
- External backend sequence-search state:
  `artifacts/v3_external_source_backend_sequence_search_1025.json` is real
  MMseqs2 evidence for the existing 30-row UniProtKB/Swiss-Prot sample. It
  uses the accepted-reference FASTA-derived sidecar plus fetched external
  sequences, covers 30/30 external rows and 735 current reference accessions,
  preserves 2 exact-reference holdouts, records 28 no-signal rows, 0
  near-duplicate rows, 0 failures, and removes the bounded current-reference
  complete-search blocker only for the 28 no-signal rows. It does not run
  UniRef-wide search or Foldseek/TM-score, and no external row is countable or
  import-ready.
- Learned representation state: `artifacts/v3_external_source_representation_backend_sample_1025.json`
  computes a 12-row ESM-2 sample for external mapped controls with
  `embedding_backend_available=true`, vector dimension `320`, 0 embedding
  failures, 3 representation-near-duplicate holdouts, 12 learned-vs-heuristic
  disagreement rows, and 0 countable/import-ready rows. The audit
  `artifacts/v3_external_source_representation_backend_sample_audit_1025.json`
  is guardrail-clean. This is pilot-priority evidence only; sequence search,
  active-site sourcing, review decisions, and full factory gates remain
  required before any import.
- Pilot representation state:
  `artifacts/v3_external_source_pilot_representation_backend_sample_1025.json`
  computes ESM-2 embeddings for all 10 selected pilot candidates, has vector
  dimension `320`, 0 embedding failures, 9 complete learned-representation
  rows, 1 representation-near-duplicate holdout (`P55263` to reference
  `Q9TVW2` at cosine `0.9731`), 30 reference pairs, and 0 countable/import-ready
  rows. The refreshed pilot dossiers now attach representation rows to all 10
  selected candidates, keep 3 explicit-active-site evidence blockers, and keep
  every selected candidate blocked before import.
- 650M representation state:
  `artifacts/v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_1025.json`
  and
  `artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json`
  attempt `facebook/esm2_t33_650M_UR50D` in local-only mode after a bounded
  150M feasibility run. The 650M model is still not cached, and the environment
  had only about 3.2 GiB free for a 2.61 GB remote weight file with CPU-only
  inference, so the sidecars use the cached `facebook/esm2_t30_150M_UR50D`
  backend as the largest feasible actual model. Mapped controls now have 12
  review-only 640-dimensional rows, 0 embedding failures, 7 representation
  near-duplicate holdouts, and 12 learned-vs-heuristic disagreements; selected
  pilot rows now have 10 review-only rows, 0 embedding failures, 4
  representation near-duplicate holdouts, and 10 learned-vs-heuristic
  disagreements. Their paired 8M-vs-larger stability audits report
  `fallback_changed`, remain review-only, and keep 0 countable or import-ready
  rows.
- 725 post-batch review surface: all 95 unlabeled candidates are retained in a
  207-row active-learning queue; 95 expert-label decision rows are exported as
  review-only no-decision items; 25 priority local-evidence lanes are audited
  and exported with 0 countable candidates; 8 alternate residue-position
  requests are explicit; 24 reaction/substrate mismatch lanes remain
  non-countable; the scaling-quality audit classifies all 24 new review-debt
  rows and leaves 0 unclassified.
- 725 discovery controls: the mechanism ontology gap audit records 121
  review-only scope-pressure rows, the learned-retrieval manifest stages 568
  eligible rows with the heuristic baseline as control, and the
  sequence-similarity failure-set audit keeps 2 duplicate clusters as
  non-countable controls.
- Historical accepted-700 repair context remains below because the 725 repair
  artifacts build on those same review-only lanes.
- 700 post-batch active-learning queue: all 76 unlabeled candidates are
  retained; no unlabeled rows are omitted by the queue limit. The queue now
  includes `reaction_substrate_mismatch_value` and ranks 18 kinase or ATP
  phosphoryl-transfer rows with hydrolase top hits for expert review.
- 700 expert-label decision review export: all 76 active-queue
  `expert_label_decision_needed` rows are exported as `no_decision`, 0 are
  countable candidates, 56 carried review-debt rows and 20 new review-debt rows
  are linked, and the 7 reaction/substrate mismatch lanes are already covered by
  the dedicated mismatch export. Risk flags include 50 cofactor-family
  ambiguity rows, 29 counterevidence-boundary rows, 14 active-site
  mapping/structure-gap rows, 9 text-leakage/nonlocal-evidence risks, 7
  reaction/substrate mismatches, 7 substrate-class boundaries, 6 sibling
  mechanism confusions, and 2 Ser-His/metal-boundary rows.
- 700 expert-label repair candidates:
  `artifacts/v3_expert_label_decision_repair_candidates_700.json` ranks 30
  review-only repair candidates and buckets all 76 rows as 14 active-site
  mapping/structure-gap repairs, 7 text-leakage/nonlocal-evidence guardrails,
  30 cofactor-evidence repairs, 1 Ser-His/metal-boundary review, 1 sibling
  mechanism-boundary review, and 23 external expert-label decisions.
- 700 expert-label repair guardrail audit: 21 priority repair rows remain
  non-countable, including 14 active-site mapping/structure-gap rows and 9
  text-leakage/nonlocal-evidence rows. Three conservative-remap local expected
  family evidence leads (`m_csa:577`, `m_csa:592`, and `m_csa:641`) remain
  review-only, with 0 countable label candidates.
- 700 mechanism ontology gap audit: 115 non-countable scope-pressure rows
  expose transferase phosphoryl, lyase, isomerase, oxidoreductase long-tail,
  methyl-transfer, and glycan chemistry pressure without creating a new
  ontology family from keyword evidence alone.
- 700 learned retrieval manifest: 562 eligible labeled entries are staged for a
  future learned-representation path, with 160 emitted rows and the current
  heuristic geometry retrieval preserved as the required control.
- 700 sequence-similarity failure-set audit: 2 exact-reference duplicate
  clusters are kept as non-countable controls before any family propagation or
  learned-retrieval split.
- Review debt summary: 81 evidence-gap rows, all `needs_more_evidence`, with
  61 carried rows and 20 new rows. New-debt next actions are 16 alternate
  structure/cofactor-source inspections, 2 expert-review decisions, 1 family
  boundary review, and 1 local cofactor/active-site mapping check.
- 700 scaling-quality audit: 20 new review-debt rows classified, 0 accepted
  labels with review debt, 0 hard negatives, 0 near misses, 0 near-duplicate
  hits, observed ontology scope pressure, family-propagation boundary,
  cofactor ambiguity, reaction/substrate mismatch, active-site mapping gaps,
  active-learning queue concentration, and alternate-structure hits lacking
  local support.
- 700 remediation plan: all 20 new debt rows have gap detail, graph context,
  selected geometry context, and a repair bucket. Buckets are 12
  alternate-PDB ligand scans, 3 external cofactor-source reviews, 1 active-site
  mapping repair, 1 local mapping/structure-selection review, 1 family-boundary
  review, and 2 expert label decisions.
- 700 full debt remediation plan: all 81 review-debt rows are mapped. Buckets
  are 37 alternate-PDB ligand scans, 9 local mapping/structure-selection
  reviews, 9 external cofactor-source reviews, 7 family-boundary reviews,
  16 expert label decisions, and 3 active-site mapping repairs. Sixty-nine
  rows have alternate PDBs but 0 alternate-PDB M-CSA residue-position support.
- 700 focused alternate-structure scan: 13 structure-scan rows, 152 candidate
  PDB structures, 0 fetch failures, 63 alternate-PDB structures with
  conservative remapped active-site positions, 3 structure-wide
  expected-family hit rows (`m_csa:679`, `m_csa:696`, `m_csa:698`), and 0
  local active-site expected-family hit rows. These hits remain review-only
  evidence.
- 700 all-debt bounded alternate-structure scan: 46 scan-candidate review-debt
  rows, all 739 candidate PDB structures scanned, 0 fetch failures, 362
  alternate-PDB structures with conservative remapped active-site positions,
  19 expected-family hit rows, and 3 review-only local expected-family hit
  rows from remaps (`m_csa:577`, `m_csa:592`, `m_csa:641`). The remap lead
  summary records 44 review-only leads and 0 countable label candidates.
- 700 remap-local audit: `m_csa:577` and `m_csa:641` require expert
  family-boundary review, `m_csa:592` requires expert reaction/substrate review,
  all three require strict remap guardrails, and there are 0 structure-selection
  candidates after reaction mismatch triage.
- 700 reaction/substrate mismatch audit: 18 active-queue hydrolase-top1 rows
  with kinase or ATP phosphoryl-transfer text are routed to expert
  reaction/substrate review; 0 are countable.
- 700 family-propagation guardrails now block 24 reported rows with
  `reaction_substrate_mismatch` before propagation or countable promotion;
  14 of those rows are retained by a priority override beyond `max_rows`.
- 700 reaction/substrate mismatch review export: all 24 family-guardrail lanes
  are exported together, split into 17 current out-of-scope labels and 7
  unlabeled pending-review rows. The export records 0 labeled seed mismatches,
  and now supplies the expert-reviewed pressure surface for the ePK, ASKHA,
  ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP ontology expansion. The
  expansion artifact maps 20 supported lanes across all nine families, records
  4 non-target hints and 0 unsupported family mappings, and keeps
  `countable_label_candidate_count=0`. Its current review-only decision batch
  routes the 7 unlabeled rows to reviewed out-of-scope repair decisions,
  rejects 17 current controls, and adds 0 countable labels.
- Structure mapping: 19 total mapping issues at 700.
- Local performance was regenerated on 700 artifacts in `artifacts/perf_report.json`.

## Current Confidence Call

Label-quality confidence call for the 2026-05-14T02:32:17Z run:

- M-CSA-only count growth: no. The canonical registry remains 679 countable
  bronze labels, the 1,025 preview still adds 0 clean countable labels, and the
  source-scale audit still exposes only 1,003 M-CSA source records.
- External-source repair/import: yes for bounded repair/readiness evidence, no
  for countable import. External rows remain review-only and non-countable; the
  new real sequence holdout and representation sidecars remove readiness
  blockers, but active-site source decisions, complete sequence search, review
  decisions, and full label-factory gates still block import.
- Scientific generalization work: yes. MMseqs2 sequence clustering now provides
  a real <=30% sequence-identity holdout for the accepted registry with max
  train/test identity `0.284`, 0 held-out out-of-scope false non-abstentions,
  and pinned held-out/in-distribution metrics. Foldseek/TM-score separation is
  still open, but the coordinate blocker is narrowed by a review-only readiness
  artifact that stages 25 selected PDB mmCIF files and records the remaining
  missing/unstaged coordinate surface.
- SPOF hardening work: yes, but only for named blockers. This run split
  mechanism-text counterevidence into structure/local versus review-context
  categories, added the text-removal ablation, and recorded 0 structure/local
  guardrail losses; the 650M representation path is implemented but blocked by
  uncached local model weights.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock status
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --out artifacts/v3_label_expansion_candidates_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_family_propagation_guardrails_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --labels artifacts/v3_countable_labels_batch_675.json --out artifacts/v3_family_propagation_guardrails_700_preview_batch.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --baseline-review-debt artifacts/v3_review_debt_summary_675.json --max-rows 45 --out artifacts/v3_review_debt_summary_700.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation --review-debt artifacts/v3_review_debt_summary_700.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --graph artifacts/v1_graph_700.json --geometry artifacts/v3_geometry_features_700.json --debt-status new --out artifacts/v3_review_debt_remediation_700.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-review-debt-remediation --review-debt artifacts/v3_review_debt_summary_700.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --graph artifacts/v1_graph_700.json --geometry artifacts/v3_geometry_features_700.json --debt-status all --out artifacts/v3_review_debt_remediation_700_all.json
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures --remediation artifacts/v3_review_debt_remediation_700.json --max-entries 13 --max-structures-per-entry 60 --out artifacts/v3_review_debt_alternate_structure_scan_700.json
PYTHONPATH=src python -m catalytic_earth.cli scan-review-debt-alternate-structures --remediation artifacts/v3_review_debt_remediation_700_all.json --max-entries 46 --max-structures-per-entry 80 --out artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt-remap-leads --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json --remediation artifacts/v3_review_debt_remediation_700_all.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --out artifacts/v3_review_debt_remap_leads_700_all_bounded.json
PYTHONPATH=src python -m catalytic_earth.cli audit-review-debt-remap-local-leads --remap-leads artifacts/v3_review_debt_remap_leads_700_all_bounded.json --remediation artifacts/v3_review_debt_remediation_700_all.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --out artifacts/v3_review_debt_remap_local_lead_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-reaction-substrate-mismatches --review-evidence-gaps artifacts/v3_review_evidence_gaps_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --out artifacts/v3_reaction_substrate_mismatch_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-reaction-substrate-mismatch-review-export --reaction-substrate-mismatch-audit artifacts/v3_reaction_substrate_mismatch_audit_700.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_reaction_substrate_mismatch_review_export_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch --review artifacts/v3_reaction_substrate_mismatch_review_export_700.json --batch-id 700_reaction_substrate_mismatch_review --reviewer automation_label_factory --out artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-expert-label-decision-repair-guardrails --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json --remap-local-lead-audit artifacts/v3_review_debt_remap_local_lead_audit_700.json --out artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-expert-label-decision-local-evidence-gaps --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json --out artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-expert-label-decision-local-evidence-review-export --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_expert_label_decision_local_evidence_review_export_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch --review artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --batch-id 700_expert_label_decision_local_evidence_review --reviewer automation_label_factory --out artifacts/v3_expert_label_decision_local_evidence_decision_batch_700.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-expert-label-decision-local-evidence-repair-plan --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --out artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json
PYTHONPATH=src python -m catalytic_earth.cli resolve-expert-label-decision-local-evidence-repair-lanes --expert-label-decision-local-evidence-repair-plan artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json --reaction-substrate-mismatch-decision-batch artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json --out artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-explicit-alternate-residue-position-requests --expert-label-decision-local-evidence-repair-plan artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json --review-debt-remediation artifacts/v3_review_debt_remediation_700_all.json --graph artifacts/v1_graph_700.json --out artifacts/v3_explicit_alternate_residue_position_requests_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-review-only-import-safety --labels data/registries/curated_mechanism_labels.json --review artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json --review artifacts/v3_expert_label_decision_decision_batch_700.json --review artifacts/v3_expert_label_decision_local_evidence_decision_batch_700.json --out artifacts/v3_review_only_import_safety_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_700.json --applied-label-factory artifacts/v3_label_factory_applied_labels_700.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_700.json --expert-review-export artifacts/v3_expert_review_export_700_post_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700.json --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --expert-label-decision-local-evidence-repair-resolution artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json --explicit-alternate-residue-position-requests artifacts/v3_explicit_alternate_residue_position_requests_700.json --review-only-import-safety-audit artifacts/v3_review_only_import_safety_audit_700.json --atp-phosphoryl-transfer-family-expansion artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json --out artifacts/v3_label_factory_gate_check_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-mechanism-ontology-gaps --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700_all.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --max-rows 80 --out artifacts/v3_mechanism_ontology_gap_audit_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-learned-retrieval-manifest --geometry artifacts/v3_geometry_features_700.json --retrieval artifacts/v3_geometry_retrieval_700.json --labels data/registries/curated_mechanism_labels.json --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_700.json --max-rows 160 --out artifacts/v3_learned_retrieval_manifest_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-sequence-similarity-failure-sets --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json --labels data/registries/curated_mechanism_labels.json --active-learning-queue artifacts/v3_active_learning_review_queue_700.json --out artifacts/v3_sequence_similarity_failure_sets_700.json
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-cluster-proxy --graph artifacts/v1_graph_700.json --out artifacts/v3_sequence_cluster_proxy_700.json
PYTHONPATH=src python -m catalytic_earth.cli audit-label-scaling-quality --batch-id 700_preview --acceptance artifacts/v3_label_batch_acceptance_check_700_preview.json --readiness artifacts/v3_label_preview_promotion_readiness_700.json --review-debt artifacts/v3_review_debt_summary_700_preview.json --review-evidence-gaps artifacts/v3_review_evidence_gaps_700_preview.json --active-learning-queue artifacts/v3_active_learning_review_queue_700_preview_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_700_preview_batch.json --hard-negatives artifacts/v3_hard_negative_controls_700_preview_batch.json --decision-batch artifacts/v3_expert_review_decision_batch_700_preview.json --structure-mapping artifacts/v3_structure_mapping_issues_700.json --expert-review-export artifacts/v3_expert_review_export_700_preview_post_batch.json --sequence-clusters artifacts/v3_sequence_cluster_proxy_700.json --alternate-structure-scan artifacts/v3_review_debt_alternate_structure_scan_700.json --remap-local-lead-audit artifacts/v3_review_debt_remap_local_lead_audit_700.json --reaction-substrate-mismatch-audit artifacts/v3_reaction_substrate_mismatch_audit_700.json --reaction-substrate-mismatch-review-export artifacts/v3_reaction_substrate_mismatch_review_export_700.json --expert-label-decision-review-export artifacts/v3_expert_label_decision_review_export_700.json --expert-label-decision-repair-candidates artifacts/v3_expert_label_decision_repair_candidates_700.json --expert-label-decision-repair-guardrail-audit artifacts/v3_expert_label_decision_repair_guardrail_audit_700.json --expert-label-decision-local-evidence-gap-audit artifacts/v3_expert_label_decision_local_evidence_gap_audit_700.json --expert-label-decision-local-evidence-review-export artifacts/v3_expert_label_decision_local_evidence_review_export_700.json --expert-label-decision-local-evidence-repair-resolution artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json --explicit-alternate-residue-position-requests artifacts/v3_explicit_alternate_residue_position_requests_700.json --review-only-import-safety-audit artifacts/v3_review_only_import_safety_audit_700.json --atp-phosphoryl-transfer-family-expansion artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json --out artifacts/v3_label_scaling_quality_audit_700_preview.json
```

## Next Agent Start Here

User-approved priority override: do not keep adding gates upon gates. Every new
artifact, audit, or gate must directly remove one named SPOF, generalization, or
external-pilot blocker; otherwise do not build it.

Latest run was direct only, with no subagents or delegation. Do not open another
M-CSA-only tranche. Do not claim full TM-score holdout.

The active Foldseek path is now cluster-first, not blind chunk continuation.
This run added `build-foldseek-tm-score-cluster-first-split` and pinned
cluster-first artifacts:
`artifacts/v3_foldseek_tm_score_cluster_first_split_1000.json`,
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split.json`,
`artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_query_subchunk_006_of_112.json`,
`artifacts/v3_foldseek_tm_score_cluster_first_split_round2_1000.json`,
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round2.json`,
`artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_006_of_112.json`,
`artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_007_of_112.json`,
`artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_aggregate_006_007_of_112.json`,
`artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json`, and
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json`.

The first cluster-first candidate uses the 672 staged materializable structures
as the structure index and folds existing `TM >= 0.7` evidence into 24
partition constraints across 12 constrained clusters. It projects 0 known
constraint violations and preserves 0 sequence-cluster splits. A first
6-query verification subchunk (`006/112`) then exposed a new blocker:
`m_csa:38` against held-out out-of-scope `m_csa:118`, max train/test
TM-score `0.7435`. Round 2 moves `m_csa:118` to in-distribution and the same
subchunk passes with 14,207 mapped rows, 2,358 train/test rows, max TM-score
`0.6509`, and 0 target-violating pairs.

The paired round-2 subchunk `007/112` completed with 9,094 mapped rows, 5,449
train/test rows, max train/test TM-score `0.8651`, and 16 target-violating rows
across 9 reported structure pairs. The current handoff split is
`artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json`: it folds
those blockers into 34 high-TM constraints across 14 constrained clusters,
projects 0 known constraint violations, preserves 0 sequence-cluster splits,
moves 12 entries to heldout and 12 held-out out-of-scope entries to
in-distribution, keeps held-out out-of-scope false non-abstentions at 0, and
keeps all rows review-only/non-countable.

The previous run then reran subchunks `006/112` and `007/112` from the round-3
readiness. Subchunk 006 passed again with 14,207 mapped rows, 2,356
train/test rows, max TM-score `0.6509`, and 0 target-violating pairs.
Subchunk 007 still failed with 9,094 mapped rows, 4,976 train/test rows, max
TM-score `0.8043`, and one reported blocker: `m_csa:45` against held-out
out-of-scope `m_csa:397`. Round 4 folded that blocker into 35 high-TM
constraints, moved `m_csa:397` to in-distribution, and the direct round-4
subchunk `007/112` rerun passed with 9,094 mapped rows, 4,975 train/test rows,
max TM-score `0.6598`, and 0 target-violating pairs.

This run continued from round 4. Direct round-4 subchunk `008/112` completed
with 8,641 mapped rows, 1,540 train/test rows, max TM-score `0.7205`, and one
reported blocker: `m_csa:54` against held-out out-of-scope `m_csa:428`.
`artifacts/v3_foldseek_tm_score_cluster_first_split_round5_1000.json` folds
that blocker into 36 high-TM constraints across 15 constrained clusters, moves
`m_csa:428` to in-distribution, preserves 0 sequence-cluster splits, keeps
held-out out-of-scope false non-abstentions at 0, and keeps all rows
review-only/non-countable. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round5.json`.
The direct round-5 rerun of subchunk `008/112` passes with 8,641 mapped rows,
1,532 train/test rows, max TM-score `0.6989`, and 0 target-violating pairs.

Direct round-5 subchunk `009/112` then completed with 15,531 mapped rows,
2,955 train/test rows, max TM-score `0.879`, and one reported blocker:
`m_csa:58` against held-out out-of-scope `m_csa:628`. The current handoff
split was then
`artifacts/v3_foldseek_tm_score_cluster_first_split_round6_1000.json`: it
folds that blocker into 37 high-TM constraints across 16 constrained clusters,
moves `m_csa:628` to in-distribution, preserves 0 sequence-cluster splits,
keeps held-out out-of-scope false non-abstentions at 0, and keeps all rows
review-only/non-countable. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round6.json`.
The direct round-6 rerun of subchunk `009/112` passes with 15,531 mapped rows,
2,939 train/test rows, max TM-score `0.6699`, and 0 target-violating pairs.

This run continued from round 6. Direct subchunk `010/112` timed out under the
900-second bound before emitting pair rows. A 3-query split of the same window
completed microchunk `020/224` (`m_csa:61`-`m_csa:63`) with 7,488 mapped rows,
1,319 train/test rows, max TM-score `0.7116`, and one reported blocker:
in-distribution `m_csa:63`/`pdb:1CB7` against held-out out-of-scope
`m_csa:188`/`pdb:1XEL`. The current handoff split is now
`artifacts/v3_foldseek_tm_score_cluster_first_split_round7_1000.json`: it
folds that blocker into 38 high-TM constraints across 17 constrained clusters,
moves `m_csa:188` to in-distribution, preserves 0 sequence-cluster splits,
keeps held-out out-of-scope false non-abstentions at 0, and keeps all rows
review-only/non-countable. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round7.json`.
The direct round-7 rerun of microchunk `020/224` timed out under the
900-second bound before emitting pair rows. This run isolated that timeout
with single-query checks under the same round-7 readiness. Staged indices 60,
61, and 62 (`m_csa:61`-`m_csa:63`) all complete and aggregate to 7,488 mapped
rows, 1,311 train/test rows, max TM-score `0.6967`, and 0 target-violating
pairs. Staged indices 63, 64, and 65 (`m_csa:64`-`m_csa:66`) also complete and
aggregate to 2,190 mapped rows, 378 train/test rows, max TM-score `0.5629`,
and 0 target-violating pairs. Staged index 66 (`m_csa:67`) completes with 687
mapped rows, 593 train/test rows, max TM-score `0.6535`, and 0 target-violating
pairs. Staged index 67 (`m_csa:68`) then exposes one blocker:
in-distribution `m_csa:68`/`pdb:1IVH` against held-out `m_csa:750`/
`pdb:1U8V`, max TM-score `0.7909`.

Round-8 single-query verification then clears staged indices 68-78
(`m_csa:69`-`m_csa:79`) before staged index 79 exposes a new blocker:
held-out out-of-scope `m_csa:80`/`pdb:1C3C` against in-distribution
`m_csa:408`/`pdb:1AUW` and `m_csa:569`/`pdb:1FUQ`, max TM-score `0.8726`.

The current handoff split is now
`artifacts/v3_foldseek_tm_score_cluster_first_split_round16_1000.json`: it
folds the latest staged-index-110 blocker surface into 66 high-TM constraints
across 21 constrained clusters and also applies 38 real sequence-identity
partition constraints before assignment. This preserves 0 sequence-cluster
splits, keeps held-out out-of-scope false non-abstentions at 0, and keeps all
rows review-only/non-countable. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round16.json`.
The direct round-9 rerun of staged index 79 plus staged indices 80-83 passes
in aggregate with 4,434 mapped rows, 763 train/test rows, max TM-score
`0.6477`, and 0 target-violating pairs. Continuing round-9 single-query
verification clears staged indices 84-95 with 17,189 mapped rows, 3,257
train/test rows, max train/test TM-score `0.6579`, and 0 target-violating
pairs. The next round-9 batch clears indices 96-101 before index 102 exposes
`m_csa:103`/`pdb:1VAO` versus held-out `m_csa:115`/`pdb:1W1O` at max TM-score
`0.7653`. The direct round-10 rerun of staged index 102 passes at max
train/test TM-score `0.6725` with 0 target-violating pairs. Staged index 103
then exposes `m_csa:104`/`pdb:1C9U` versus held-out `m_csa:686`/`pdb:1E1A`
at max `0.7633`; round 11 folds that pair but exposes `m_csa:104` versus
`m_csa:360`/`m_csa:740` at max `0.7317`; round 12 folds those pairs and
clears staged index 103 at max `0.6669`. Staged index 104 then passes at max
`0.4496`, and staged index 105 exposes a larger high-TM blocker surface at
max `0.8862` with 72 violating rows. Round 13 folds those constraints and
clears indices 105-106 before index 107 exposes `m_csa:108` at max `0.8826`.
Round 14 folds that surface and reruns index 107 cleanly at max `0.6862`.
Index 108 then exposes `m_csa:109` at max `0.7649`; round 15 folds those
blockers and verifies indices 107-109 cleanly at max `0.6996`. Index 110 then
exposes `m_csa:111` against `m_csa:364`, `m_csa:550`, `m_csa:236`, and
`m_csa:270` at max `0.7521`. Round 16 folds that blocker, but its direct
index-110 rerun still exposes `m_csa:111` against `m_csa:852` at max `0.7708`.
Round 17 folds that pair and verifies index 110 cleanly at max `0.6823`;
index 111 also passes at max `0.564`. Index 112 then exposes `m_csa:113`
against held-out `m_csa:131` at max `0.7063`; round 18 folds that pair but
its rerun exposes a larger `m_csa:113` blocker surface against `m_csa:942`,
`m_csa:978`, and related in-distribution neighbors at max `0.9087`. Round 19
folds that evidence and clears indices 112-113 before index 114 exposes
`m_csa:115` versus `m_csa:822` at max `0.7338`. Round 20 folds that pair and
clears index 114, but index 115 exposes a broader `m_csa:116` surface at max
`0.9749`; round 21 folds that surface but exposes `m_csa:116` versus held-out
`m_csa:67` at max `0.9032`. Round 22 folds that pair into 82 high-TM
constraints plus 38 sequence-identity partition constraints, with 0 projected
violations and 0 sequence-cluster splits, then clears indices 115-118 at max
`0.6939` with 0 target-violating pairs.

Next Foldseek work should continue from round-22 readiness at staged query
index 119 using the same one-query verification pattern, or a larger bounded
chunk only if the runtime risk is acceptable. Stop on any `TM >= 0.7`
train/test blocker and fold it into a new cluster-first round before
continuing.
`m_csa:372` and `m_csa:501` remain coordinate exclusions, most query coverage
remains unverified, and `full_tm_score_holdout_claim_permitted=false` remains
required.

External pilot import remains blocked. The selected-pilot representation
adjudication now gives concrete review-only statuses: 3 stable representation
controls, 4 near-duplicate holdouts, and 3 stability-change rows needing
review. The refreshed pilot success criteria still reports 0 terminal
decisions, 0 import-ready rows, 0 countable candidates, 3 active-site-source
blockers, 10 broader duplicate-screening blockers, 3 unresolved
representation-control blockers, and 10 full-gate blockers. Next useful pilot
work is broader duplicate screening or review decisions only after the blocker
evidence is sufficient; keep all outputs non-countable unless full import
conditions pass.

Label-quality confidence call for the 2026-05-14T00:28:43Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF/artifact-lineage hardening. Evidence at run start: 298 unit tests
passed, `validate` passed with 679 curated labels, the 1,025 preview remained
non-promotable with 0 clean countable labels, current artifacts already
contained the proxy sequence/fold-distance holdout plus the canonical and
selected-pilot ESM-2 representation samples, and `foldseek`, `mmseqs`,
`blastp`, and `diamond` were absent on PATH. The code-confirmed failure was the
missing lineage check on the high-fan-in scaling-quality audit.

Latest run continued artifact-graph consistency and selected-PDB SPOF hardening
instead of adding gate count or opening another M-CSA tranche. Code inspection
found that `build-geometry-features` could accept a selected-PDB override plan
whose ready rows were outside the selected graph slice, whose residue node ids
did not belong to the selected graph, or whose `current_selected_pdb_id` no
longer matched selected graph evidence. That path now fails before geometry
write, and negative regressions cover out-of-slice override rows and unknown
override residue node ids. The run also found that several external pilot
builders joined high-fan-in artifacts before the transfer gate could reject
mixed source slices. `audit-external-source-import-readiness`,
`build-external-source-transfer-blocker-matrix`,
`build-external-source-pilot-evidence-packet`, and
`build-external-source-pilot-evidence-dossiers` now share a fail-fast external
artifact-lineage loader, record checked lineage in `metadata.artifact_lineage`,
and have CLI negative regressions for mixed 1,000/1,025 inputs. Refreshed
external artifacts keep the 1,025 transfer gate at 66/66, with 0 countable
external rows and 0 import-ready rows.

Label-quality confidence call for the 2026-05-14T01:30:08Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF/artifact-lineage hardening. Evidence at run start: 300 unit tests
passed, `validate` passed with 679 curated labels, the 1,025 preview remained
non-promotable with 0 clean countable labels, current artifacts already
contained the proxy sequence/fold-distance holdout plus canonical and
selected-pilot ESM-2 representation samples, and `foldseek`, `mmseqs`,
`blastp`, and `diamond` were absent on PATH. The code-confirmed failures were
silent selected-PDB override mismatch handling and missing build-time lineage
checks on the import-readiness, blocker-matrix, pilot-packet, and
pilot-dossier builders.

Previous run targeted the external-pilot representation-control SPOF rather than
adding gate count. Code and artifact evidence showed that the selected pilot
dossiers still depended on the 12-row mapped-control representation sample and
therefore had representation rows for only 4 of the 10 selected pilot
candidates; the other 6 carried stale representation-backend blockers before
review could proceed. The fix adds
`build-external-source-pilot-representation-backend-plan`, builds the
review-only pilot plan and ESM-2 sample, refreshes pilot dossiers to attach
representation evidence to all 10 selected rows, and adds the pilot
representation sample to typed candidate-lineage validation. The refreshed
external transfer gate now passes 66/66 with 0 blockers, records
`external_pilot_representation_sample_candidate_count=10`, validates 33
candidate-lineage artifacts, and validates 63 clean 1,025 artifact-path inputs.
All external rows remain review-only, non-countable, and not import-ready;
`P55263` is explicitly held out as a representation near-duplicate control.

Label-quality confidence call for the 2026-05-13T23:26:40Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, yes for bounded scientific generalization/control
work through the pilot-specific leakage-safe ESM-2 sample, and yes for
SPOF/external-pilot hardening. Evidence at run start: 296 unit tests and
`validate` passed, the 1,025 preview remained non-promotable with 0 clean
countable labels, current artifacts already contained the proxy sequence/fold
holdout and 12-row canonical ESM-2 sample, no Foldseek/MMseqs2/BLAST/DIAMOND
backend was available on PATH, and the selected pilot dossier artifact exposed
missing representation rows for 6 selected candidates.

Current SPOF status after the 2026-05-13T22:25:38Z run: counterevidence
maintainability is handled at the code level. `geometry_retrieval.py` uses a
versioned declarative `COUNTEREVIDENCE_POLICY` with typed shared inputs,
rule-level provenance, backwards-compatible reason/detail fields, and explicit
mechanism-text leakage flags. `check_label_factory_gates` accepts the typed
`LabelFactoryGateInputs.v1` contract, the CLI loads gate artifacts through a
table-driven map, and non-exempt label-factory gate inputs now get slice-lineage
validation plus payload-declared slice/batch checks. The current 1,000 gate
artifact also records payload methods and short payload digests, and a negative
regression test rejects a renamed or stale artifact whose payload slice metadata
contradicts the path lineage. Text-leakage protection is now enforced in both
the geometry scorer and the external representation sample: geometry retrieval
excludes mechanism text, entry names, labels, EC/Rhea identifiers, source ids,
and target labels from positive scoring, and uses a text-free local
PLP ligand-anchor feature for PLP-supported positives. Representation samples
use sequence embeddings and length coverage as predictive sources; heuristic
fingerprint ids, matched M-CSA reference ids, and source scope signals carry
explicit review/holdout leakage flags. The representation audit fails if
EC/Rhea ids, mechanism text, labels, fingerprint ids, or source-target
identifiers appear as predictive feature sources. Artifact consistency
hardening exists in the external blocker matrix audit, which rejects
candidate-manifest lineage mismatches, and in the external transfer gate, which
validates candidate accessions across high-fan-in external artifacts,
artifact-path slice lineage across supplied external artifacts, and pilot
review-only/no-decision semantics through the typed
`ExternalSourceTransferGateInputs.v1` contract and shared candidate-lineage
artifact registry before passing the 65/65 review-only gate. The gate CLI fails
fast on mixed 1,000/1,025 paths, payload-declared slice contradictions, or
pilot artifacts that stop being non-countable review work products. The
sequence-holdout audit is now part of the row-level candidate-lineage registry,
so a stale or mismatched holdout audit cannot silently satisfy the gate by
matching only high-level candidate counts.

Latest run targeted the artifact-graph consistency SPOF rather than adding gate
count. The code evidence showed that `sequence_holdout_audit` was accepted by
`ExternalSourceTransferGateInputs.v1` and checked by its own gate, but it was
not included in `EXTERNAL_TRANSFER_CANDIDATE_LINEAGE_FIELDS`. The fix adds it
to shared candidate-lineage validation, adds a negative regression with a
mismatched holdout accession, and refreshes
`artifacts/v3_external_source_transfer_gate_check_1025.json`; the gate still
passes 65/65, now with `sequence_holdout_audit` listed among 32 checked
candidate-lineage artifacts and a clean 62-artifact path lineage. This removes
one silent-failure surface without changing countable labels or import
readiness.

Label-quality confidence call for the 2026-05-13T22:25:38Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF/artifact-lineage hardening. Evidence at run start: 296 unit tests
and `validate` passed, the 1,025 preview remained non-promotable, current
artifacts already contained the proxy sequence/fold-distance holdout and
12-row ESM-2 representation sample, Foldseek/MMseqs2/BLAST/DIAMOND were absent
on PATH, and the code inspection found the sequence-holdout audit lineage gap
inside the external transfer gate contract.

Previous run targeted the external-pilot sequence SPOF rather than adding generic
gate count. The new
`artifacts/v3_external_source_sequence_reference_screen_audit_1025.json` checks
whether the bounded current countable-reference screen can clear the
current-reference near-duplicate blocker. The initial audit exposed two
inactive demerged UniProt references (`P03176` and `Q05489`) among the expected
735 current countable reference accessions; the fetch path now resolves those
conservatively to all listed replacements (`P0DTH5`/`Q9QNF7` and
`P0DUB8`/`P0DUB9`) instead of silently dropping them. The audit now records
complete current-reference coverage, 28 current-reference top-hit no-signal
rows, and two exact-reference holdouts. The sequence-search export replaces
`complete_near_duplicate_reference_search_not_completed` with
`complete_uniref_or_all_vs_all_near_duplicate_search_required` for the 28
non-holdout rows, keeps 0 countable/import-ready external rows, and the
external transfer gate now checks the reference-screen audit directly and
passes 65/65. The gate also rejects a stale sequence-search export that claims
a different current-reference completion count than the audit rows support.

Label-quality confidence call for the 2026-05-13T21:24:10Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF/external-pilot hardening. Evidence at run start: 292 unit tests and
`validate` passed, the 1,025 preview remained non-promotable, current artifacts
already contained the proxy sequence/fold-distance holdout and 12-row ESM-2
representation sample, and the new reference-screen audit showed that missing
the initial reference-screen audit exposed inactive demerged current-reference
accessions that had to be resolved before external pilot sequence clearance.

Previous run removed the code-confirmed text-leakage SPOF rather than adding
generic gates or labels. The prior PLP mechanism-text score boost in
`geometry_retrieval.py` was removed, a local PLP ligand-anchor score based on
proximal PLP/LLP/PMP/P5P ligand context was added, retrieval metadata now
declares excluded leakage-prone fields, and regression tests verify that PLP
mechanism text no longer changes the score. Refreshed 1,000/1,025 retrieval,
holdout, label-factory, selected-PDB override, and external heuristic-control
artifacts preserve 0 hard negatives, 0 near misses, 0 out-of-scope false
non-abstentions, 0 actionable in-scope failures, and 0 countable/import-ready
external rows. `artifacts/v3_label_factory_gate_check_1000.json` still passes
21/21; after the current reference-screen gate integration,
`artifacts/v3_external_source_transfer_gate_check_1025.json` passes 65/65.
Final verification after regenerated artifacts: 292 unit tests,
`validate`, `compileall`, `git diff --check`, and JSON artifact parsing passed.

Label-quality confidence call for the 2026-05-13T20:23:44Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF hardening. Evidence at run start: 290 unit tests passed,
`validate` passed with 679 curated labels, the 1,025 preview remained
non-promotable and review-only, the latest artifacts already contained the
proxy sequence/fold-distance holdout and the 12-row ESM-2 representation sample,
and the code inspection found a positive PLP mechanism-text scoring path that
was not compatible with orphan-enzyme discovery claims.

An earlier SPOF run removed the selected-PDB single-point blocker in bounded
form. The new
`build-selected-pdb-overrides` command produces
`artifacts/v3_selected_pdb_override_plan_700.json` from the holo-preference
audit and remediation plan. The plan applies `m_csa:577` -> `1AWB` and
`m_csa:641` -> `1J7N` with explicit remapped residue positions, keeps
`m_csa:592` skipped because its glucokinase reaction/substrate mismatch still
requires review, and records 0 countable label candidates. The downstream
1,000-context selected-PDB override geometry/retrieval/evaluation artifacts
preserve 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions,
and 0 actionable in-scope failures.

This run also converted the external blocker matrix into a bounded pilot
priority artifact instead of another generic gate. The new
`artifacts/v3_external_source_pilot_candidate_priority_1025.json` selects 10
review-only candidates across the external lanes, caps lane selection at 2,
defers 5 exact-holdout or near-duplicate rows, records
`external_pilot_candidate_ranking` as the blocker removed, and keeps every row
non-countable and not import-ready. Its leakage provenance records that
mechanism text, EC/Rhea identifiers, source labels, and target labels are not
priority-scoring evidence. The companion
`artifacts/v3_external_source_pilot_review_decision_export_1025.json` exports
those 10 rows as no-decision review packets with 0 completed decisions.
This run then added
`artifacts/v3_external_source_pilot_evidence_packet_1025.json`, which
consolidates 79 source targets for those selected rows: all 10 sequence-search
packets plus 3 active-site sourcing packets. It is guardrail-clean, has 0
missing required source packets, and keeps every row review-only, non-countable,
and not import-ready.
This run then added
`artifacts/v3_external_source_pilot_evidence_dossiers_1025.json`, which
assembles the same selected 10 into per-candidate review dossiers. Seven have
explicit UniProt active-site feature support, all 10 have Rhea reaction
context, four have representation-sample rows, and all 10 still carry import
blockers. The dossier artifact removes only the pilot evidence-assembly
blocker; it does not authorize external import. Dossier assembly now also adds
local evidence-completeness blockers, so selected rows missing explicit
active-site evidence (`O60568`, `O95050`, and `P51580` in the current pilot)
stay blocked even if an upstream blocker matrix goes stale.

Latest run added a direct external-pilot SPOF safeguard rather than another
count-growth gate. `check_external_source_transfer_gates` now has four
pilot-specific checks: priority rows must remain leakage-safe and review-only,
pilot review-decision exports must stay no-decision with 0 completed decisions,
pilot evidence packets must stay guardrail-clean review packets with source
targets, and pilot dossiers must remain non-countable evidence summaries. The
same code path now adds local dossier blockers for missing explicit active-site
evidence, missing specific reaction context, and near-duplicate sequence
alerts. The pilot gate logic lives in a focused helper rather than another
large branch cascade inside the external transfer gate. A negative regression
test fails a completed pilot decision, and the regenerated
`artifacts/v3_external_source_transfer_gate_check_1025.json` records 65/65
passing checks with 10 selected pilot candidates, 0 completed pilot decisions,
79 source targets, and 10 dossier rows that still carry import blockers. The
dossier metadata now records 3 local explicit-active-site evidence blockers and
0 missing-specific-reaction blockers for the current selected pilot rows.

Label-quality confidence call for the 2026-05-13T18:23:11Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF hardening.
Evidence at run start: 287 unit tests passed, `validate` passed with 679
curated labels, the latest docs and artifacts already contained the proxy
sequence/fold-distance holdout plus the 12-row ESM-2 representation sample, and
the current 1,025 state remained review-only with 0 countable/import-ready
external rows. During the run, `foldseek`, `mmseqs`, `blastp`, and `diamond`
were absent on PATH, so real sequence/fold separation remained blocked. The
run therefore hardened the external pilot review-decision SPOF and kept M-CSA
count growth and external import stopped.

Remaining-time plan executed in the same run: after the review-decision gate
safeguard passed, use the remaining bounded window to make the pilot dossier
path less dependent on stale upstream blockers. That added local active-site,
reaction-context, and sequence-alert blockers, summarized those blockers in
dossier metadata, centralized the pilot import review-requirement list, and
made the gate require selected pilot rows to be eligible and blocker-free.

Next ordered worklist:

1. Treat external transfer artifact-path lineage as handled for the current
   1,025 gate and the current import-readiness, blocker-matrix, pilot-packet,
   and pilot-dossier builders: row-level candidate lineage, path-inferred
   slice lineage, and payload-declared slice contradictions now fail before the
   gate or high-fan-in builder can silently pass, and pilot priority/review/
   evidence/dossier artifacts now fail if they stop being review-only/no-
   decision work products. Continue artifact graph consistency only where new
   code evidence shows another high-fan-in audit can mix source slice, graph id,
   label batch, or artifact lineage without a negative regression.
2. Sequence-distance holdout evaluation is implemented with a real MMseqs2
   backend and pinned by regression tests. Treat the sequence-identity split as
   real for the accepted countable registry: 678/678 evaluated labels are
   covered, 738 sequence records are clustered at 30% identity and 80%
   coverage, and max observed train/test identity is `0.284`. The retained
   proxy fields are fallback context only. Foldseek is available in the
   temporary Conda env `/private/tmp/catalytic-foldseek-env`. The new
  Foldseek coordinate-readiness artifact stages 25 selected PDB mmCIF
  files and records 676 materializable rows plus two missing selected
  structures. A partial staged-coordinate TM signal exists for those 25 files,
  but full TM-score separation remains missing until the remaining coordinates
  are staged and a structural backend is wired in.
3. Use the learned representation backend path, pilot priority artifact,
   no-decision review export, pilot evidence packet, pilot-specific
   representation sample, and pilot evidence dossiers for reviewer work. The
   canonical 12-row mapped-control ESM-2 8M sample and the 10-row selected-pilot
   ESM-2 8M sample are both computed and review-only. The 650M sidecars are
   implemented but currently unavailable because the model is not cached
   locally; do not treat them as computed embeddings until the model can be
   loaded. The next work is to fill evidence decisions from the per-candidate
   dossier/source-target rows while preserving heuristic geometry retrieval as
   the baseline.
4. Reviewer policy and schema typing are lower priority unless code evidence
   exposes new ambiguity in countable vs review-only imports or high-fan-in
   artifact schemas.
5. Keep ePK and transition-state signature work lower priority until the SPOF
   and external-pilot blockers above are either fixed or explicitly blocked.

Concrete user direction for the next runs: stop adding abstract gates unless
they directly unblock the first external-source import pilot. The 1,025
checkpoint already proved the key strategic point: M-CSA-only count growth is
source-limited, while external-source import is not yet ready. The next
valuable work is not a larger gate count; it is a small, evidence-backed
external pilot.

Immediate target: advance the 10 selected candidates in
`artifacts/v3_external_source_pilot_candidate_priority_1025.json` from the
30-row UniProtKB/Swiss-Prot sample. Keep every external row review-only until
active-site, reaction, sequence, representation, review, and full label-factory
gates pass. Do not open another M-CSA-only tranche such as 1,050 as normal
progress.

Priority blockers to remove:

1. Source explicit catalytic or active-site residue evidence for the 10
   active-site-feature gap rows using
   `artifacts/v3_external_source_active_site_sourcing_export_1025.json`.
   Binding context and Rhea context are useful, but they do not replace
   catalytic active-site evidence.
2. Complete real near-duplicate or UniRef-style sequence searches for the 28
   rows in `artifacts/v3_external_source_sequence_search_export_1025.json`.
   Exact-reference overlaps and high-similarity rows stay holdout controls, not
   labels.
3. Use the computed ESM-2 representation sample, the pilot-priority artifact,
   and the consolidated pilot evidence packet to prepare representation repair
   or reviewer decisions for the 10 selected candidates. Preserve heuristic
   geometry retrieval as the required control baseline.
4. Advance the 10 selected pilot candidates toward explicit active-site
   evidence, specific reaction evidence, clean sequence holdout status, clean
   structure mapping, non-collapsed heuristic/representation behavior, and no
   broad-EC ambiguity.
5. Fill the no-decision review packets only after evidence is assembled. Keep
   decisions review-only first. Attempt countable import only for candidates
   that pass active-site, reaction, sequence, representation, review, and full
   factory gates.

Definition of done for this pivot: 5-10 named external candidates have
per-row evidence dossiers covering active-site residues, reaction/mechanism
evidence, structure mapping, sequence holdout/near-duplicate status, heuristic
retrieval control, representation control, and remaining blockers. If no
candidate is import-ready, the output should be a ranked blocker list for the
pilot, not more generic audit machinery.

Start from the accepted 1,000 state plus the non-promoted 1,025 preview. The
canonical registry remains at 679 countable labels; the latest accepted labels
are still `m_csa:978`, `m_csa:988`, `m_csa:990`, and `m_csa:994`.

The bounded 1,025 preview remains open but not promotable. The preview gate
passes 21/21 checks, but
`artifacts/v3_label_batch_acceptance_check_1025_preview.json` is not accepted
for counting because it adds 0 clean countable labels. Review debt rises from
326 to 329 rows, with new rows `m_csa:1003`, `m_csa:1004`, and `m_csa:1005`,
all explicitly deferred by
`artifacts/v3_accepted_review_debt_deferral_audit_1025_preview.json`.

The 1,025 run exposed a source-scale bottleneck rather than a label-quality
failure. `artifacts/v3_source_scale_limit_audit_1025.json` records 1,003
observed M-CSA source records for the requested 1,025 tranche and recommends
stopping M-CSA-only count growth. The external-source transfer path is now
gated for review-only evidence collection rather than count growth:
`artifacts/v3_external_source_transfer_manifest_1025.json`,
`artifacts/v3_external_source_query_manifest_1025.json`,
`artifacts/v3_external_ood_calibration_plan_1025.json`,
`artifacts/v3_external_source_candidate_sample_1025.json`,
`artifacts/v3_external_source_candidate_sample_audit_1025.json`,
`artifacts/v3_external_source_candidate_manifest_1025.json`,
`artifacts/v3_external_source_candidate_manifest_audit_1025.json`,
`artifacts/v3_external_source_lane_balance_audit_1025.json`,
`artifacts/v3_external_source_evidence_plan_1025.json`,
`artifacts/v3_external_source_evidence_request_export_1025.json`,
`artifacts/v3_external_source_active_site_evidence_queue_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_audit_1025.json`,
`artifacts/v3_external_source_failure_mode_audit_1025.json`,
`artifacts/v3_external_source_control_repair_plan_1025.json`,
`artifacts/v3_external_source_control_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_audit_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_active_site_gap_source_requests_1025.json`,
`artifacts/v3_external_source_sequence_holdout_audit_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_plan_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json`,
`artifacts/v3_external_source_sequence_search_export_1025.json`,
`artifacts/v3_external_source_sequence_search_export_audit_1025.json`,
`artifacts/v3_external_source_backend_sequence_search_1025.json`,
`artifacts/v3_external_source_backend_sequence_search_audit_1025.json`,
`artifacts/v3_external_source_import_readiness_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_audit_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json`,
`artifacts/v3_external_source_review_only_import_safety_audit_1025.json`, and
`artifacts/v3_external_source_transfer_gate_check_1025.json` keep
`countable_label_candidate_count=0` and pass a 67/67 review-only transfer gate.
The candidate manifest has 30 UniProtKB/Swiss-Prot rows across six balanced
query lanes; `O15527` and `P42126` are exact-reference overlaps and are routed
to sequence-holdout controls. The evidence plan flags seven broad/incomplete EC
contexts; the active-site queue exports 25 ready evidence rows and defers five
rows, including two exact-reference holdouts and three broad-EC disambiguation
cases.

External active-site and control work is broader now. The UniProtKB feature
sample covers all 25 active-site-ready rows: 15 have active-site features, 10
remain active-site-feature gaps, and all sampled rows remain non-countable. The
heuristic-control queue marks 12 candidates ready for control prototyping and
defers 13 rows. The expanded structure-mapping sample maps all 12
heuristic-ready controls onto current AlphaFold model CIFs, resolves all
requested active-site positions, and then runs the existing geometry retrieval
heuristic as a control. The heuristic is not label-ready: top1 predictions are
9 `metal_dependent_hydrolase`, 2 `heme_peroxidase_oxidase`, and 1
`flavin_dehydrogenase_reductase`, with 9 scope/top1 mismatches. The
failure-mode audit records active-site feature gaps, broad-EC disambiguation
needs, top1 fingerprint collapse, metal-hydrolase collapse, and scope/top1
mismatch as review-only failures to repair before any external label decision.
The active-site feature-gap rows are `O60568`, `P29372`, `P27144`, `A2RUC4`,
`P51580`, `O95050`, `Q9HBK9`, `A5PLL7`, `P32189`, and `Q32P41`.

The new control-repair artifacts turn the current weaknesses into concrete
non-countable repair work. `artifacts/v3_external_source_control_repair_plan_1025.json`
has 25 repair rows: 10 active-site feature gaps, 3 broad-EC disambiguation
rows, and 12 heuristic-control repair rows. The representation control manifest
exposes all 12 mapped controls as future representation rows with embeddings
explicitly not computed and no training labels. The representation comparison
adds feature-proxy controls for all 12 mapped rows, flags 7 metal-hydrolase
collapse rows, preserves 2 glycan-boundary rows, and keeps every row
non-countable. The binding-context repair plan splits the 10 active-site
feature gaps into 7 rows ready for binding-context mapping and 3 rows still
missing binding context; the mapping sample maps 7/7 ready rows with 0 fetch
failures. Binding positions remain repair context only, not catalytic
active-site evidence. The active-site gap source-request artifact now covers
all 10 gaps as review-only sourcing tasks, and the active-site sourcing queue
prioritizes those gaps into 7 mapped-binding-context rows and 3 primary-source
rows.

`artifacts/v3_external_source_reaction_evidence_sample_1025.json` now queries
Rhea for all 30 external candidates. It records 64 reaction-context rows with 0
fetch failures and remains non-countable. Its companion audit
`artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json` is
guardrail-clean but flags 16 broad-EC context rows across `1.1.1.-`,
`1.11.1.-`, `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and `4.2.99.-`;
those rows are not specific mechanism evidence. The sequence-holdout audit
keeps `O15527` and `P42126` as exact-reference holdouts and marks the remaining
28 candidates as near-duplicate-search cases before any future import decision.
The broad-EC disambiguation audit finds specific reaction context for all 3
broad-only repair rows, and the sequence-neighborhood plan converts the
sequence surface into 2 exact-holdout rows and 28 near-duplicate search
requests. The sequence-neighborhood sample fetches all 30 external sequences
and all 735 current countable M-CSA reference accessions after resolving
inactive demerged references, finds 0 high-similarity alerts in the bounded
unaligned screen, and the real MMseqs2 backend sequence-search artifact compares
all 30 external rows against 735 current reference accessions / 737 sequence
records. That backend search records 28 no-signal rows, 2 exact-reference
holdouts, 0 near-duplicate rows, and 0 failures, clearing bounded
current-reference backend search debt for the 28 no-signal rows. The external
all-vs-all sequence screen now clears the current 30-row candidate-candidate
duplicate screen with 0 near-duplicate pairs, while UniRef-wide duplicate
screening remains a limitation before import.
The bounded alignment verification
checks 90 top-hit pairs, confirms `O15527` and `P42126` as exact holdouts, and
records 88 no-signal pairs. The import-readiness audit keeps 0 rows ready for
label import and records 10 active-site gaps, 2 exact sequence holdouts, 9
heuristic scope/top1 mismatches, 29 representation-control issues, UniRef-wide
duplicate-screening limitations, and 2 alignment-confirmed sequence holdouts.
The sequence-search export converts all 30 rows into no-decision sequence
controls; the backend search carries the 28 current-reference no-signal rows
and 2 sequence-holdout tasks.
The active-site sourcing export carries 72 source targets for the 10 active-site
gaps with 0 completed decisions. The active-site sourcing resolution re-checks
those 10 gaps against UniProt feature evidence, records 0 explicit active-site
residue sources, and keeps the 7 binding-plus-reaction rows plus 3 reaction-only
rows non-countable. The representation-backend plan covers 12 mapped controls,
keeps embeddings absent, and requires heuristic-baseline contrast for 9 rows.
The deterministic k-mer representation backend sample computes review-only
sequence controls for all 12 planned rows, flags one representation
near-duplicate holdout (`P60174` against `m_csa:324`/`P00940`), and does not
replace the canonical ESM-2 learned representation sample, which now provides
the current review-only learned control. The
transfer blocker matrix joins all 30 candidates into
prioritized review-only next actions: 7 primary literature/PDB active-site
source reviews for rows where the UniProt re-check found no explicit active-site
positions, 3 primary active-site source tasks, 18 near-duplicate sequence
searches, and 2 sequence holdouts. Its audit now records 10 active-site
resolution rows, 12 representation sample rows, and one representation
near-duplicate alert. Its dominant next-action fraction is 0.6000 and dominant
lane fraction is 0.1667, so the queue has not collapsed to one action or one
chemistry lane.

Label-quality confidence call for the 2026-05-13T10:12:41Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
work. Evidence at run start: `validate` and 259 unit tests passed, the 1,025
preview gate remains clean but non-promotable with 0 accepted new labels, the
external transfer gate passes 45/45 review-only checks, hard negatives remain
0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
the import-readiness audit keeps 0 external rows import-ready, and active-site,
sequence-neighborhood, heuristic, and representation blockers remain
unresolved. The operational decision is to reduce external-source readiness
uncertainty while keeping every external candidate non-countable.

Remaining-time plan for the 2026-05-13T10:12:41Z run: after adding
active-site sourcing export, complete sequence-search export,
representation-backend planning, the external transfer blocker matrix, and the
53/53 transfer gate, use the remaining productive window for guardrail
hardening, artifact regression tests, full validation, JSON/countable-label
scans, CLI help checks, and documentation freshness. Do not open an external
label decision or import path until source evidence, complete sequence search,
real representation controls, review decisions, and the full label-factory gate
pass.

Wrap-up note for the 2026-05-13T10:12:41Z run: productive work continued to the
50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T11:03:46Z`;
documentation was checked and updated across README, docs, and work notes. The
run added active-site sourcing export, sequence-search export,
representation-backend planning, an integrated transfer blocker matrix,
review-only status hardening for the new export audits, and a 53/53
external-source transfer gate. Final verification passed:
`PYTHONPATH=src python -m unittest discover -s tests` with 265 tests,
`PYTHONPATH=src python -m catalytic_earth.cli validate`, `compileall`,
`git diff --check`, JSON/countable-label guardrail scans, and CLI help checks.
External rows remain 0 countable and not import-ready.

Label-quality confidence call for the 2026-05-13T11:14:12Z run: yes for
external-source repair and scientific-expansion controls, no for external label
import or M-CSA-only count growth. Evidence at run start: `validate` and 265
unit tests passed, the 1,025 preview remained non-promotable with 0 accepted
new labels, the external transfer gate passed 53/53 review-only checks, hard
negatives remained 0, near misses remained 0, out-of-scope false
non-abstentions remained 0, actionable in-scope failures remained 0,
review-only import growth remained 0, and the import-readiness audit kept 0
external rows import-ready. The operational decision was to reduce external
active-site and representation uncertainty while keeping every external
candidate non-countable.

Label-quality confidence call for the 2026-05-13T13:16:40Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
work, no for external-source import, and yes for scientific generalization
work. Evidence at run start: `validate` and 268 unit tests passed, the 1,025
preview still added 0 clean countable labels, source-scale audit remained
limited to 1,003 observed M-CSA records, hard negatives remained 0, near misses
remained 0, out-of-scope false non-abstentions remained 0, actionable in-scope
failures remained 0, review-only import growth remained 0, the external
transfer gate remained review-only at 59/59 checks with 0 import-ready rows,
active-site source evidence remained unresolved for 10 external rows, complete
near-duplicate search remained unresolved for 28 rows, and real representation
controls remained absent. The run therefore implemented the user-requested
sequence/fold-distance holdout first. The new holdout artifacts preserve 0
held-out out-of-scope false non-abstentions and surface a small held-out versus
in-distribution accuracy gap (`0.9767` vs `0.9881` evaluable in-scope top1),
but explicitly do not claim real <=30% sequence-identity or <0.7 TM-score
separation because no local Foldseek/MMseqs2/BLAST/DIAMOND executable was
available.

Wrap-up for the 2026-05-13T13:16:40Z run: implemented the proxy
sequence/fold-distance holdout artifacts for the 1,000 and 1,025 contexts,
promoted the canonical 12-row external representation sample to ESM-2
(`facebook/esm2_t6_8M_UR50D`), preserved the k-mer sample as an explicit
baseline artifact, and kept all external rows review-only/non-countable. The
transfer gate remains 60/60 and `ready_for_label_import=false`; the learned
sample has 0 embedding failures, 3 representation near-duplicate holdouts, and
12 learned-vs-heuristic disagreements. The later selected-PDB override run
implemented the holo-PDB swap action path for `m_csa:577` and `m_csa:641`
without count growth. Final verification before logging: 276 unit tests passed,
`validate` passed, `compileall` passed, `git diff --check` passed, JSON
artifact parse passed, and the 1,000-slice label-factory gate smoke wrote
lineage metadata with `slice_id=1000`.

Label-quality confidence call for the 2026-05-13T10:19:12-05:00 run: no for
additional M-CSA-only count growth, yes for bounded external-source pilot
readiness repair, no for external-source import, no for new scientific
generalization artifacts, and yes for SPOF hardening.
Evidence at run start: 276 unit tests passed, `validate` passed, the accepted
M-CSA count stayed at 679 labels, the 1,025 preview still added 0 clean
countable labels, source-scale audit still limited M-CSA exposure to 1,003
observed source records, hard negatives remained 0, near misses remained 0,
out-of-scope false non-abstentions remained 0, and actionable in-scope failures
remained 0. The run therefore targeted the selected-PDB SPOF: the new override
plan applies holo-preference repairs for `m_csa:577` and `m_csa:641`, skips
`m_csa:592`, keeps 0 countable label candidates, and its 1,000-context
downstream selected-PDB override evaluation preserves 0 hard negatives, 0 near
misses, 0 out-of-scope false non-abstentions, and 0 actionable in-scope
failures. The same run extended external transfer artifact-lineage hardening:
`check_external_source_transfer_gates` now validates candidate accessions across
high-fan-in external artifacts and the gate artifact passes 60/60 with
`metadata.artifact_lineage.guardrail_clean=true`, including the pilot priority
review-decision export, and pilot evidence-packet artifacts. The pilot-priority
artifact selects 10 review-only candidates, defers 5 holdout or near-duplicate
rows, and keeps all selected rows non-countable and not import-ready. The
review-decision export artifact creates 10 no-decision packets with 0 completed
decisions.

Wrap-up verification for the same run: 283 unit tests passed, `validate`
passed with 679 curated labels, `compileall` passed, `git diff --check` passed,
JSON artifact parsing passed for the selected-PDB, pilot-priority, pilot review
export, and external transfer gate artifacts, and CLI smoke coverage now pins
the new pilot priority and review-decision export commands. The later
2026-05-13T11:20:13-05:00 run added the pilot evidence-packet command and
included that artifact in external transfer candidate-lineage validation.

Label-quality confidence call for the 2026-05-13T11:20:13-05:00 run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF hardening.
Evidence at run start: 283 unit tests passed, `validate` passed with 679
curated labels, the 1,025 preview still added 0 clean countable labels, the
source-scale audit still limited exposed M-CSA records to 1,003, the proxy
sequence/fold holdout and 12-row ESM-2 representation sample already existed,
and the selected-PDB override path was already applied for `m_csa:577` and
`m_csa:641`. The code evidence for the active SPOF was that label-factory
gate lineage validation still trusted path-inferred slice ids whenever payload
lineage was absent or contradicted the filename. This run hardened that path:
`cmd_check_label_factory_gates` now loads gate artifacts before lineage
validation, rejects payload-declared slice/batch metadata that conflicts with
path lineage, records payload methods and short digests in
`metadata.artifact_lineage`, and pins the failure with a negative CLI
regression test. The same run added a review-only pilot evidence packet for
the 10 selected external candidates, consolidating 79 source targets with 0
missing sequence packets and 0 missing required active-site packets while
keeping `ready_for_label_import=false`.

Label-quality confidence call for the 2026-05-13T17:21:43Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair, no
for external-source import, no for new scientific generalization artifacts, and
yes for SPOF hardening. Evidence at run start: 285 unit tests passed,
`validate` passed with 679 curated labels, the 1,025 preview still added 0
clean countable labels, the source-scale audit still limited exposed M-CSA
records to 1,003, proxy sequence/fold holdout and ESM-2 representation samples
already existed, and no Foldseek, MMseqs2, BLAST, or DIAMOND executable was
available on PATH. The active code evidence was an artifact-graph consistency
gap: the external transfer gate checked row accessions but did not fail fast on
mixed source-slice artifact paths. This run added
`validate_external_transfer_artifact_path_lineage`, wired it into the gate CLI
with fail-fast behavior, regenerated
`artifacts/v3_external_source_transfer_gate_check_1025.json` with clean
`artifact_path_lineage.slice_id=1025` across 61 inputs, and pinned a negative
mixed-slice regression test. Remaining time went to the first external pilot
evidence-dossier artifact, which joins current active-site, reaction, sequence,
structure, heuristic, representation, and blocker evidence for the 10 selected
candidates while keeping all rows review-only. No countable labels or
import-ready external rows were created.

Label-quality confidence call for the 2026-05-13T14:17:40Z run: no for
additional M-CSA-only count growth, no for external-source import, no for new
external candidate repair, no for new scientific generalization artifacts, and
yes for SPOF hardening. Evidence at run start: `validate` and 273 unit tests
passed, the accepted M-CSA count stayed at 679 labels, the 1,025 preview still
added 0 clean countable labels, source-scale audit still limited M-CSA exposure
to 1,003 observed source records, hard negatives remained 0, near misses
remained 0, out-of-scope false non-abstentions remained 0, actionable in-scope
failures remained 0, and the latest external transfer gate remained review-only
with 0 import-ready rows. The run therefore targeted the first named SPOF:
counterevidence maintainability. It replaced the geometry-retrieval
counterevidence branch cascade with typed declarative rules and gave the
label-factory gate a typed input contract plus table-driven CLI artifact
loading plus non-exempt slice-lineage validation. It then advanced the next
SPOFs in bounded form: representation samples now declare sequence-only
predictive features and mark heuristic fingerprint ids, matched M-CSA ids, and
scope signals as review/holdout context; the external blocker-matrix audit now
rejects candidate-manifest lineage mismatches.

Remaining-time plan for the 2026-05-13T14:17:40Z run: after counterevidence
policy refactoring and label-factory gate input hardening passed focused tests
and a 1,000-slice gate smoke, use the remaining productive window for
documentation, full tests/validation, and wrap-up rather than opening count
growth or another generic transfer gate. The next unblocked SPOF is text-leakage
mitigation across learned representation artifacts and external pilot ranking,
followed by artifact graph consistency checks.

Remaining-time plan for the 2026-05-13T11:14:12Z run: after the active-site
sourcing resolution and deterministic representation sample were in place, use
the remaining productive window to make the blocker matrix consume those packets
directly, add gate/audit checks that reject stale blocker matrices, refresh
artifacts and docs to the 59/59 gate state, and rerun the full validation stack
before wrap-up. Do not open external label decisions or import rows during this
run.

New failure modes checked in the 2026-05-13T11:14:12Z run: the deterministic
representation sample surfaced one representation-level near-duplicate holdout
(`P60174` nearest `P00940`/`m_csa:324`) that was not promoted, and the blocker
matrix path had a stale-integration risk where resolution/sample artifacts could
exist without row-level blocker evidence. The transfer gate now has explicit
matrix-integration checks for active-site resolution and representation sample
rows, and the matrix audit rejects advertised integration counts that are absent
from rows.

Wrap-up note for the 2026-05-13T11:14:12Z run:
`ENDED_AT=2026-05-13T12:04:24Z`; measured productive-plus-wrap elapsed time was
about 50.2 minutes. Documentation was checked and updated across README, docs,
and work notes; no stale current-state claims are intentionally left outside
historical progress entries/status that will be regenerated from the log. Final
verification before wrap-up passed: full unit tests with 268 tests, validate,
compileall, `git diff --check`, JSON artifact parse checks,
countable/import-ready guardrail scans for the new artifacts, and CLI help
checks for the new commands. External rows remain 0 countable and not
import-ready; the gate is 59/59 review-only checks.

Label-quality confidence call for the 2026-05-13T09:10:54Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
work. Evidence at run start: `validate` and 256 unit tests passed, the 1,025
preview gate remains clean but non-promotable with 0 accepted new labels, the
external transfer gate passed 41/41 review-only checks before this run's new
sequence-alignment and active-site-sourcing gates, hard negatives remain
0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
the import-readiness audit keeps 0 external rows import-ready, and active-site,
sequence-neighborhood, heuristic, and representation blockers remain unresolved.
The operational decision is to reduce external-source readiness uncertainty
while keeping every external candidate non-countable.

Remaining-time plan for the 2026-05-13T09:10:54Z run: after adding bounded
sequence-alignment verification, active-site sourcing queue artifacts, and the
45/45 external transfer gate, use the remaining productive window for artifact
regression tests, full validation, JSON/countable-label guardrail scans, and
documentation freshness. Do not open an external label decision or import path
until active-site sourcing, complete sequence-neighborhood controls, real
representation controls, review decisions, and full label-factory gates pass.

Wrap-up note for the 2026-05-13T09:10:54Z run: productive work continued to the
50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T10:03:45Z`;
documentation was checked and updated across README, docs, and work notes. Final
verification passed with 259 unit tests, `validate`, `compileall`,
`git diff --check`, JSON artifact parsing, CLI help checks for the new commands,
external countable/import-ready guardrail scans, and a 45/45 external transfer
gate.

Label-quality confidence call for the 2026-05-13T03:08:55-05:00 run: no for
additional M-CSA-only count growth, yes for bounded external-source control
repair. Evidence at run start: `validate` and 252 unit tests passed, the 1,025
preview gate remains clean but non-promotable with 0 accepted new labels, the
prior external transfer gate passed 38/38 review-only checks, hard negatives
remain 0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
and the source-scale audit records only 1,003 observed M-CSA records for the
requested 1,025 tranche. The operational decision was to reduce external
sequence/readiness uncertainty while keeping every external candidate
non-countable.

Remaining-time plan for the 2026-05-13T03:08:55-05:00 run: after the bounded
sequence-neighborhood screen and import-readiness audit passed targeted tests,
keep work scoped to artifact regression coverage, docs, validation, and final
gate verification. Do not import external labels until explicit active-site
sourcing, complete sequence-neighborhood controls, real representation
controls, review decisions, and full label-factory gates pass.

Wrap-up note for the 2026-05-13T03:08:55-05:00 run: productive work continued
to the 50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T03:59:49-05:00`;
documentation was checked and updated across README, docs, and work notes.
Final verification passed with 256 unit tests, `validate`, `compileall`,
`git diff --check`, JSON artifact parse checks, CLI help checks, and external
artifact import/countable guardrail checks.

Label-quality confidence call for the 2026-05-13T07:08:09Z run: no for
additional M-CSA-only count growth, yes for bounded external-source repair
controls. Evidence at run start: `validate` and 247 unit tests passed, the
1,025 preview gate remains clean but non-promotable with 0 accepted new labels,
the prior external transfer gate passed 33/33 review-only checks, hard
negatives remain 0, near misses remain 0, out-of-scope false non-abstentions
remain 0, actionable in-scope failures remain 0, review-only import growth
remains 0, the ATP/phosphoryl-transfer family expansion remains guardrail-clean,
and the source-scale audit records only 1,003 observed M-CSA records for the
requested 1,025 tranche. The operational decision is to repair external-source
control readiness while keeping every external candidate non-countable.

Remaining-time plan for the 2026-05-13T07:08:09Z run: after adding
representation-control comparison, broad-EC disambiguation, active-site gap
source requests, sequence-neighborhood controls, and updated external transfer
gates, use the remaining productive window for focused regression tests, full
validation, JSON artifact checks, and documentation/status updates. Do not
import external labels until explicit sequence, active-site, representation,
decision, and label-factory gates pass.

Wrap-up note for the 2026-05-13T07:08:09Z run: productive work continued past
the 50-minute boundary before wrap-up. `ENDED_AT=2026-05-13T08:00:14Z`;
documentation was checked and updated across README, docs, and work notes.
Final verification passed with 252 unit tests, `validate`, `compileall`,
`git diff --check`, CLI help checks for the new commands, and JSON artifact
countable-label checks.

Label-quality confidence call for the 2026-05-13T06:06:38Z run: no for
additional M-CSA-only count growth, yes for bounded external-source control
repair. Evidence at run start: `validate` and 239 unit tests passed, the 1,025
preview gate passes 21/21 checks, the prior external transfer gate passes 22/22
review-only checks, hard negatives remain 0, near misses remain 0,
out-of-scope false non-abstentions remain 0, actionable in-scope failures
remain 0, review-only import growth remains 0, the 1,025 acceptance artifact
adds 0 clean countable labels, and the source-scale audit records only 1,003
observed M-CSA records for the requested 1,025 tranche. The existing external
control artifacts exposed active-site feature gaps, broad-EC rows, and a
metal-hydrolase/top1 collapse, so this run repaired guardrails instead of
opening label growth. This is an operational workflow decision, not a claim of
biological truth.

Remaining-time plan for the 2026-05-13T06:06:38Z run: after expanding
structure mapping to all 12 heuristic-ready controls, adding repair,
representation, binding-context, reaction, and sequence-holdout artifacts, use
the remaining productive window for regression tests, docs, and final gate
validation. Do not import external labels until a separate reviewed decision
artifact passes full label-factory gates.

Label-quality confidence call for the 2026-05-13T03:03:14Z run: yes, current
quality gates are good enough to spend this run on a bounded 1,025 preview.
Evidence at run start: `validate` and 206 unit tests passed, the accepted-1,000
gate passes 21/21 checks with 0 blockers, the accepted-1,000 review-debt
deferral audit keeps all 326 review-state rows non-countable with 0 accepted
overlap and 0 countable candidates, hard negatives remain 0, near misses remain
0, out-of-scope false non-abstentions remain 0, actionable in-scope failures
remain 0, review-only import growth remains 0, 321 expert-label decision rows
remain review-only, the 92 priority local-evidence gap rows remain
non-countable, and the ATP/phosphoryl-transfer family expansion remains
guardrail-clean with 0 countable label candidates. This is an operational
workflow decision, not a claim of biological truth.

Label-quality confidence call at handoff after the 2026-05-13T03:03:14Z run:
no for additional M-CSA-only count growth, yes for bounded external-source
transfer scaffolding.
Evidence: the 1,025 factory gate passes 21/21 checks, hard negatives remain 0,
near misses remain 0, out-of-scope false non-abstentions remain 0, actionable
in-scope failures remain 0, accepted review-gap labels remain 0, and
review-only import growth remains 0. However, the 1,025 acceptance artifact has
0 accepted new labels and the source-scale audit shows the M-CSA-only path does
not have enough source records for the next tranche. This is an operational
workflow decision, not a claim of biological truth.

Label-quality confidence call for the 2026-05-13T04:04:36Z run: no for
additional M-CSA-only count growth, yes for bounded external-source transfer
scaffolding. Evidence at run start: `validate` and 217 unit tests passed, the
1,025 preview gate passes 21/21 checks, hard negatives remain 0, near misses
remain 0, out-of-scope false non-abstentions remain 0, actionable in-scope
failures remain 0, accepted review-gap labels remain 0, review-only import
growth remains 0, the 1,025 acceptance artifact adds 0 clean countable labels,
and the source-scale audit records only 1,003 observed M-CSA records for the
requested 1,025 tranche. This run should advance external-source transfer
guardrails while keeping all external candidates non-countable.

Label-quality confidence call for the 2026-05-13T05:05:40Z run: no for
additional M-CSA-only count growth, yes for bounded external-source evidence
and control work. Evidence at run start: `validate` and 230 unit tests passed,
the 1,025 preview gate passes 21/21 checks, hard negatives remain 0, near
misses remain 0, out-of-scope false non-abstentions remain 0, actionable
in-scope failures remain 0, review-only import growth remains 0, the 1,025
acceptance artifact adds 0 clean countable labels, and the source-scale audit
records only 1,003 observed M-CSA records for the requested 1,025 tranche. This
run should keep external rows review-only while converting evidence gaps into
explicit control artifacts.

Remaining-time plan for the 2026-05-13T05:05:40Z run: after all 25 ready
external rows had active-site evidence sampled and the first 4 mapped controls
showed a metal-hydrolase top1 collapse, use remaining productive time to attach
failure-mode tests, update durable docs, and avoid any external label decision
until ontology/representation controls can separate those lanes.

Remaining-time plan for the 2026-05-13T04:04:36Z run: after the external
candidate manifest, evidence plan, evidence request export, import-safety
audit, and 11/11 external-transfer gate are implemented, use the remaining
productive window to harden documentation, artifact regression coverage, and
review-only external-source guardrails rather than opening another M-CSA-only
tranche.

Remaining-time plan for the 2026-05-13T03:03:14Z run: after the 1,025 preview
proved clean but non-promotable, use the remaining productive window to harden
the external-source transfer path. Completed: source-scale audit, transfer
manifest, query manifest, OOD calibration plan, bounded read-only UniProtKB/
Swiss-Prot sample, sample guardrail audit, regression tests, and documentation.

Label-quality confidence call for the 2026-05-13T01:00:39Z run: yes, current
quality gates are good enough to spend this run on a bounded 975 preview.
Evidence at run start: `validate` and 205 unit tests passed, the accepted-950
gate passes 21/21 checks with 0 blockers, the accepted-950 review-debt
deferral audit keeps all 282 review-state rows non-countable with 0 accepted
overlap, hard negatives remain 0, near misses remain 0, out-of-scope false
non-abstentions remain 0, actionable in-scope failures remain 0, review-only
import growth remains 0, 277 expert-label decision rows remain review-only,
the 84 priority local-evidence gap rows remain non-countable, and the
ATP/phosphoryl-transfer family expansion remains guardrail-clean with 0
countable label candidates. This is an operational workflow decision, not a
claim of biological truth.

Remaining-time plan for the 2026-05-13T01:00:39Z run: after the 975 gate
accepted two clean labels and the post-975 gate stayed clean, the run opened,
repaired, and accepted the bounded 1,000-entry preview. The review-debt
deferral, queue-retention, hard-negative, false-non-abstention,
actionable-failure, and family-boundary gates are clean.

Label-quality confidence call for the 2026-05-12T23:58:38Z run: yes, current
quality gates are good enough to spend this run on bounded 875 scaling.
Evidence at run start: `validate` and 205 unit tests passed, the accepted-850
gate passes 20/20 checks, the accepted-850 review-debt deferral audit keeps
all 203 review-state rows non-countable with 0 accepted-label overlap, hard
negatives remain 0, near misses remain 0, out-of-scope false non-abstentions
remain 0, actionable in-scope failures remain 0, review-only import growth
remains 0, and the ATP/phosphoryl-transfer family expansion remains
guardrail-clean with 0 countable label candidates. This is an operational
workflow decision, not a claim of biological truth.

Label-quality confidence call for the 2026-05-12T20:55:05Z run: yes, current
quality gates are good enough to spend this run on bounded 775 scaling.
Evidence at run start: `validate` and 200 unit tests passed, the accepted-750
gate passes 20/20 checks, the accepted-750 review-debt deferral audit keeps 118
review-state rows non-countable, hard negatives remain 0, near misses remain 0,
out-of-scope false non-abstentions remain 0, actionable in-scope failures
remain 0, review-only import growth remains 0, and the ATP/phosphoryl-transfer
family expansion remains guardrail-clean with 0 countable label candidates.
This is an operational workflow decision, not a claim of biological truth.

Label-quality confidence call for the 2026-05-12T19:54:22Z run: yes, current
quality gates were good enough to explicitly defer the 750 review-debt surface
and promote the seven clean 750 labels. Evidence: baseline `validate` and 200
unit tests passed at run start, the post-batch 750 gate passes 20/20 checks,
hard negatives remain 0, near misses remain 0, out-of-scope false
non-abstentions remain 0, actionable in-scope failures remain 0, accepted
labels with review debt remain 0, review-only import growth remains 0, and the
ATP/phosphoryl-transfer family expansion remains guardrail-clean with 0
countable label candidates. This is an operational workflow decision, not a
claim of biological truth.

Start with:
`artifacts/v3_label_batch_acceptance_check_1025_preview.json`,
`artifacts/v3_label_factory_gate_check_1025_preview.json`,
`artifacts/v3_label_scaling_quality_audit_1025_preview.json`,
`artifacts/v3_review_debt_summary_1025_preview.json`,
`artifacts/v3_accepted_review_debt_deferral_audit_1025_preview.json`,
`artifacts/v3_source_scale_limit_audit_1025.json`,
`artifacts/v3_external_source_transfer_manifest_1025.json`,
`artifacts/v3_external_source_query_manifest_1025.json`,
`artifacts/v3_external_ood_calibration_plan_1025.json`,
`artifacts/v3_external_source_candidate_sample_1025.json`,
`artifacts/v3_external_source_candidate_sample_audit_1025.json`,
`artifacts/v3_external_source_candidate_manifest_1025.json`,
`artifacts/v3_external_source_candidate_manifest_audit_1025.json`,
`artifacts/v3_external_source_lane_balance_audit_1025.json`,
`artifacts/v3_external_source_evidence_plan_1025.json`,
`artifacts/v3_external_source_evidence_request_export_1025.json`,
`artifacts/v3_external_source_active_site_evidence_queue_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_1025.json`,
`artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_1025.json`,
`artifacts/v3_external_source_heuristic_control_queue_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_1025.json`,
`artifacts/v3_external_source_structure_mapping_plan_audit_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_1025.json`,
`artifacts/v3_external_source_structure_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_1025.json`,
`artifacts/v3_external_source_heuristic_control_scores_audit_1025.json`,
`artifacts/v3_external_source_failure_mode_audit_1025.json`,
`artifacts/v3_external_source_control_repair_plan_1025.json`,
`artifacts/v3_external_source_control_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_1025.json`,
`artifacts/v3_external_source_representation_control_manifest_audit_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_1025.json`,
`artifacts/v3_external_source_representation_control_comparison_audit_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_1025.json`,
`artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_1025.json`,
`artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json`,
`artifacts/v3_external_source_active_site_gap_source_requests_1025.json`,
`artifacts/v3_external_source_sequence_holdout_audit_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_plan_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_1025.json`,
`artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_1025.json`,
`artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json`,
`artifacts/v3_external_source_sequence_search_export_1025.json`,
`artifacts/v3_external_source_sequence_search_export_audit_1025.json`,
`artifacts/v3_external_source_import_readiness_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`,
`artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_1025.json`,
`artifacts/v3_external_source_representation_backend_plan_audit_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_1025.json`,
`artifacts/v3_external_source_representation_backend_sample_audit_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_1025.json`,
`artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json`,
`artifacts/v3_external_source_review_only_import_safety_audit_1025.json`,
`artifacts/v3_external_source_transfer_gate_check_1025.json`,
`artifacts/v3_external_source_reaction_evidence_sample_1025.json`,
`artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json`,
`artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json`, and
`work/label_preview_1025_notes.md`. For the compact external-transfer profile,
also read `work/external_source_transfer_1025_notes.md`.

Highest-value options:

1. Do not promote the 1,025 preview; it has 0 accepted labels and exists as a
   source-limit audit point.
2. Continue review-only external-source evidence collection from
   `artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`:
   the first UniProt feature re-check found 0 explicit active-site residue
   sources, so the next active-site step is primary literature/PDB source
   review for the 7 binding-plus-reaction context rows and primary active-site
   source discovery for the 3 reaction-only rows without counting any row.
3. Treat the Rhea reaction-context sample as context only, especially the 16
   broad-EC context rows; do not treat Rhea rows as active-site evidence.
4. Treat `artifacts/v3_external_source_backend_sequence_search_1025.json` as
   the bounded current-reference sequence-search result: it clears that backend
   search blocker for the 28 no-signal rows, while broader UniRef-wide or
   all-vs-all duplicate screening remains a limitation before import.
5. Use the 12-row ESM-2 representation sample in
   `artifacts/v3_external_source_representation_backend_sample_1025.json` and
   its learned-vs-heuristic disagreements to prioritize pilot review, while
   keeping heuristic retrieval, sequence-search controls, and
   `artifacts/v3_external_source_kmer_representation_backend_sample_1025.json`
   as required baselines.
6. Use `artifacts/v3_external_source_transfer_blocker_matrix_1025.json` as the
   candidate-level blocker map: 10 active-site source rows with resolution
   statuses carried forward, 28 backend no-signal sequence rows, 2 sequence
   holdouts, 12 representation-backend plans, 12 representation sample rows, 3
   representation near-duplicate holdouts in the ESM-2 sample, 1 representation
   near-duplicate holdout in the k-mer baseline, and 0 completed import
   decisions. The 67/67 transfer gate now fails stale matrices that omit
   active-site resolution, backend sequence-search, or representation sample
   integration, and also fails high-fan-in external artifacts with unexpected
   candidate accessions, missing full-coverage manifest rows, or candidate-count
   drift.
7. Keep every external UniProtKB/Swiss-Prot candidate non-countable until a
   separate decision artifact passes the full label-factory gate.
8. Preserve the nine-family ATP/phosphoryl-transfer layer as boundary evidence;
   do not collapse these families into generic hydrolase or metal-hydrolase
   labels.

Label-quality confidence call for the 2026-05-12T16:56:09-05:00 run: yes,
current quality gates are good enough to open a bounded 800 preview. Evidence
at run start: `validate` and 202 unit tests passed, the accepted-775 gate
passes 20/20 checks, the accepted-775 review-debt deferral audit keeps all 138
review-state rows non-countable with 0 accepted-label overlap, hard negatives
remain 0, near misses remain 0, out-of-scope false non-abstentions remain 0,
actionable in-scope failures remain 0, review-only import growth remains 0,
and the ATP/phosphoryl-transfer family expansion remains guardrail-clean with
0 countable label candidates. This is an operational workflow decision, not a
claim of biological truth.

Remaining-time plan for the 2026-05-12T16:56:09-05:00 run: after accepting
the clean 800 batch, use the remaining productive window to remove a scaling
bottleneck exposed by the run by adding geometry-artifact row reuse, verify it
against the real 800 graph, then open the next bounded tranche only if the
post-800 gate remains clean and the wrap-up window is still protected.

Keep `m_csa:650` and `m_csa:771` in review unless explicit local mechanism
evidence resolves their counterevidence; they are regression cases for
mechanism text that should not override family-boundary or triad-coherence
conflicts.

Remaining-time plan executed for the 2026-05-12T20:55:05Z run: after the 775
gate was clean and the registry had 642 labels, do not open 800 in the final
productive minutes. Instead, preserve the 775 evidence by adding
`work/label_preview_775_notes.md`, refreshing current-state docs, generating
`artifacts/perf_report_775.json`, and checking stale status/handoff claims
before measured wrap-up.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
- Bronze/silver/gold tiers are evidence-management tiers, not wet-lab
  validation status.
- Geometry retrieval is heuristic, not learned.
- Ligand/cofactor evidence uses nearby and structure-wide mmCIF ligand atoms
  plus inferred roles; it does not model occupancy, alternate conformers,
  biological assembly, or substrate state.
- `m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430` are currently best
  treated as evidence-limited abstentions because selected structures lack
  expected local or structure-wide cofactor evidence.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.

## Run Timing

- STARTED_AT: 2026-05-15T15:59:13-05:00
- ENDED_AT: 2026-05-15T16:34:59-05:00
- Measured elapsed time: 35.767 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly continued round-28 Foldseek cluster-first verification from staged
  index 131. Index 131 exposed `m_csa:132` versus `m_csa:532` at max TM-score
  `0.8385`; round 29 folded that blocker into 101 high-TM constraints plus 38
  sequence-identity constraints.
- Round 29 cleared index 131 at max `0.6904` and cleared indices 132-139
  before index 140 exposed `m_csa:141` versus `m_csa:903` at max `0.7337`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round30_1000.json`
  and
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round30.json`.
  Round 30 has 102 high-TM constraints, 38 sequence-identity partition
  constraints, 0 projected violations, 0 sequence-cluster splits, 0 held-out
  out-of-scope false non-abstentions, 0 countable labels, and 0 import-ready
  rows. Its direct verification clears indices 140-141 at max train/test
  TM-score `0.6873`. Next direct Foldseek work should continue staged index
  142 under round-30 readiness.
- Full TM-score holdout remains forbidden: round-30 coverage is still partial,
  the split remains review-only/candidate-only, and `m_csa:372`/`m_csa:501`
  remain coordinate exclusions.

### 2026-05-15T22:00:14Z run

- Directly continued Foldseek cluster-first verification from round-30 staged
  index 142. Index 142 passed at max train/test TM-score `0.6204`. Index 143
  exposed `m_csa:144`/`pdb:1G8K` against train neighbors at max `0.872` with
  88 violating train/test rows.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round31_1000.json`
  and
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round31.json`.
  Round 31 raised the split to 106 high-TM constraints, but the index-143
  rerun still failed at max `0.8001` with 12 violating rows.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round32_1000.json`
  and
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round32.json`.
  Round 32 has 108 high-TM constraints, 38 sequence-identity constraints,
  0 projected violations, 0 sequence-cluster splits, 0 held-out out-of-scope
  false non-abstentions, 0 countable labels, and 0 import-ready rows.
- Direct round-32 verification clears index 143 at max `0.5745` and index 144
  at max `0.4664`. Index 145 (`m_csa:146`/`pdb:4V4E`) timed out after 900
  seconds before pair rows were emitted. The aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round32_query_single_aggregate_143_145_of_672.json`
  records 2 completed query coordinates, 4,346 pair rows, 961 train/test rows,
  max train/test TM-score `0.5745`, 0 target-violating pairs, and one timeout
  artifact.
- Full TM-score holdout remains forbidden: round-32 coverage is still partial,
  index 145 is unresolved, the split remains review-only/candidate-only, and
  `m_csa:372`/`m_csa:501` remain coordinate exclusions. Next direct Foldseek
  work should retry or explicitly adjudicate staged index 145 under round-32
  readiness before advancing to index 146.
- Final verification passed: 426 unit tests, `validate`, `compileall`,
  `git diff --check`, and JSON parsing for 20 new Foldseek artifacts.

- STARTED_AT: 2026-05-15T19:58:30Z
- ENDED_AT: 2026-05-15T20:30:22Z
- Measured elapsed time: 31.867 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. Repaired a
  self-created stale exec-shell PID lock into a live sentinel lock before
  syncing. No M-CSA-only count growth and no external import.
- Directly continued round-24 Foldseek cluster-first verification from staged
  index 123. Index 123 exposed `m_csa:124` blockers at max TM-score `0.9676`;
  round 25 folded those blockers but its index-123 rerun exposed a second
  `m_csa:124` surface at max `0.8735`.
- Round 26 folded that surface into 97 high-TM constraints plus 38
  sequence-identity constraints and cleared indices 123-126 at max train/test
  TM-score `0.6981`. Index 127 then exposed `m_csa:128` versus `m_csa:198` at
  max `0.8035`.
- Round 27 folded that pair, cleared indices 127-129 at max `0.6868`, then
  index 130 exposed `m_csa:131` versus `m_csa:281`/`m_csa:555` at max
  `0.7574`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round28_1000.json`
  and
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round28.json`.
  Round 28 has 100 high-TM constraints, 38 sequence-identity partition
  constraints, 0 projected violations, 0 sequence-cluster splits, 0 held-out
  out-of-scope false non-abstentions, 0 countable labels, and 0 import-ready
  rows. Its direct index-130 rerun passes at max train/test TM-score `0.6775`.
  Next direct Foldseek work should continue staged index 131 under round-28
  readiness.
- Full TM-score holdout remains forbidden: round-28 coverage is still partial,
  the split remains review-only/candidate-only, and `m_csa:372`/`m_csa:501`
  remain coordinate exclusions.
- Final verification passed: 424 unit tests, `validate`, `compileall`,
  `git diff --check`, and JSON parsing for 23 new Foldseek artifacts.

- STARTED_AT: 2026-05-15T14:52:02Z
- ENDED_AT: 2026-05-15T15:31:50Z
- Measured elapsed time: 39.800 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Hardened cluster-first split assignment so real sequence-identity clusters
  are unioned before structural component assignment. This fixed the
  staged-index-102 repair path without introducing sequence-cluster splits.
- Directly ran round-9 single-query checks from staged indices 96-102. Indices
  96-101 passed; index 102 exposed `m_csa:103`/`pdb:1VAO` versus held-out
  `m_csa:115`/`pdb:1W1O` at max TM-score `0.7653`.
- Built and verified cluster-first rounds 10-12 for the subsequent blockers.
  Round 12 clears staged index 103 at max TM-score `0.6669`; staged index 104
  passes at max `0.4496`; staged index 105 exposes a larger high-TM blocker
  surface at max `0.8862`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round13_1000.json`
  and
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round13.json`.
  Round 13 has 48 high-TM constraints, 38 sequence-identity partition
  constraints, 0 projected violations, 0 sequence-cluster splits, 0 countable
  labels, and 0 import-ready rows. Next direct Foldseek work should rerun
  staged index 105 under round-13 readiness.
- The all-materializable staged-coordinate Foldseek signal now completes over
  all 672 materializable selected coordinates and maps 952,922 pair rows, but
  it fails the `<0.7` target at max train/test TM-score `0.9749`; it remains
  review-only/non-countable and non-claiming.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m unittest discover -s tests`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m compileall src tests`, and JSON parsing for 28
  new/updated Foldseek artifacts.

- STARTED_AT: 2026-05-15T13:50:06Z
- ENDED_AT: 2026-05-15T14:30:32Z
- Measured elapsed time: 40.433 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly ran round-9 single-query checks from
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round9.json`.
  Staged indices 84-95 all completed with 17,189 mapped rows, 3,257
  train/test rows, max train/test TM-score `0.6579`, and 0 target-violating
  pairs.
- Added
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_084_of_672.json`
  through
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_095_of_672.json`
  plus
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_aggregate_084_095_of_672.json`.
  The aggregate remains review-only/non-countable and keeps
  `full_tm_score_holdout_claim_permitted=false`.
- Next direct Foldseek work should start at staged index 96 under round-9
  readiness. Stop on any `TM >= 0.7` train/test blocker and fold it into a
  new cluster-first round before continuing.
- Final verification passed: the new aggregate pin test, `git diff --check`,
  `PYTHONPATH=src python -m unittest discover -s tests`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m compileall src tests`.

- STARTED_AT: 2026-05-15T12:48:12Z
- ENDED_AT: 2026-05-15T13:31:56Z
- Measured elapsed time: 43.733 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly ran round-8 single-query checks from
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round8.json`.
  Staged indices 68-78 passed before staged index 79 exposed held-out
  out-of-scope `m_csa:80` versus in-distribution `m_csa:408` and `m_csa:569`
  at max TM-score `0.8726`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round9_1000.json`
  and `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round9.json`.
  Round 9 has 41 high-TM constraints, 19 constrained clusters, 0 projected
  violations, 0 sequence-cluster splits, and moves the `m_csa:80` high-TM
  neighborhood to in-distribution while keeping 0 countable labels and 0
  import-ready rows.
- Direct round-9 verification reran staged index 79 and continued through
  staged index 83. The aggregate covers 5 query coordinates, 4,434 mapped rows,
  763 train/test rows, max TM-score `0.6477`, and 0 target-violating pairs.
  Next direct Foldseek work should start at staged index 84 under round-9
  readiness.
- Final verification passed: JSON parsing for 21 new Foldseek artifacts, 4
  focused artifact tests, `git diff --check`, `PYTHONPATH=src python -m
  unittest discover -s tests` with 400 tests, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m compileall src
  tests`.

- STARTED_AT: 2026-05-15T08:05:27Z
- ENDED_AT: 2026-05-15T08:45:41Z
- Measured elapsed time: 40.233 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly isolated the timed-out round-7 microchunk `020/224` with one-query
  checks from
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round7.json`.
  Staged indices 60-62 (`m_csa:61`-`m_csa:63`) pass in aggregate at max
  TM-score `0.6967`; staged indices 63-65 (`m_csa:64`-`m_csa:66`) pass in
  aggregate at max TM-score `0.5629`; staged index 66 (`m_csa:67`) passes at
  max TM-score `0.6535`.
- Staged index 67 (`m_csa:68`) exposes a new `m_csa:68`/`m_csa:750` blocker at
  max TM-score `0.7909`. Round 8 folds that pair into
  `artifacts/v3_foldseek_tm_score_cluster_first_split_round8_1000.json` with
  39 high-TM constraints, 18 constrained clusters, 0 projected violations, 0
  sequence-cluster splits, 0 countable labels, and 0 import-ready rows. Its
  readiness artifact is
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round8.json`.
- `src/catalytic_earth/generalization.py` now ingests prior cluster-first
  `partition_constraints` as pair-cache evidence so incremental rounds can
  reuse the cluster cache rather than reconstructing every source artifact.
- Final verification passed: JSON parsing for 13 new Foldseek artifacts, 6
  focused artifact/cache tests, `git diff --check`, `PYTHONPATH=src python -m
  unittest discover -s tests` with 396 tests, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m compileall -q
  src tests`.

- STARTED_AT: 2026-05-15T07:04:30Z
- ENDED_AT: 2026-05-15T07:58:04Z
- Measured elapsed time: 53.567 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly ran cluster-first round-6 subchunk `010/112` from
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round6.json`.
  It timed out under the 900-second bound before pair rows were emitted,
  leaving full TM-score holdout claims forbidden.
- Split that same query window into 3-query microchunks. Round-6 microchunk
  `020/224` completed with 7,488 mapped rows, 1,319 train/test rows, max
  TM-score `0.7116`, and one blocker: in-distribution `m_csa:63` versus
  held-out out-of-scope `m_csa:188`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round7_1000.json`
  and `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round7.json`.
  Round 7 has 38 high-TM constraints, 17 constrained clusters, 0 projected
  known violations, 0 sequence-cluster splits, 0 held-out out-of-scope false
  non-abstentions, and moves `m_csa:188` to in-distribution. Its direct
  microchunk-020 rerun timed out under the 900-second bound, so the repair is
  not verified.
- Continue from round-7 readiness by isolating microchunk `020/224` with
  single-query checks for staged query indices 60, 61, and 62. Only then
  proceed to the unrun `m_csa:64`-`m_csa:66` half of original subchunk 010.
- Final verification passed: `git diff --check`, JSON parsing for the 5 new
  Foldseek artifacts, the 4 focused artifact-pin tests, `PYTHONPATH=src python
  -m unittest discover -s tests` with 391 tests, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m compileall -q
  src tests`.

- STARTED_AT: 2026-05-15T06:03:46Z
- ENDED_AT: 2026-05-15T06:48:58Z
- Measured elapsed time: 45.200 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly ran cluster-first round-4 subchunk 008 from
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round4.json`.
  It completed with 8,641 mapped rows, 1,540 train/test rows, max TM-score
  `0.7205`, and one blocker: `m_csa:54` versus held-out out-of-scope
  `m_csa:428`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round5_1000.json`
  and `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round5.json`.
  Round 5 has 36 high-TM constraints, 15 constrained clusters, 0 projected
  violations, 0 sequence-cluster splits, 0 held-out out-of-scope false
  non-abstentions, and moves `m_csa:428` to in-distribution. Its direct
  subchunk-008 rerun passes with 8,641 mapped rows, 1,532 train/test rows, max
  TM-score `0.6989`, and 0 target-violating pairs.
- Directly ran round-5 subchunk 009. It completed with 15,531 mapped rows,
  2,955 train/test rows, max TM-score `0.879`, and one blocker: `m_csa:58`
  versus held-out out-of-scope `m_csa:628`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round6_1000.json`
  and `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round6.json`.
  Round 6 has 37 high-TM constraints, 16 constrained clusters, 0 projected
  violations, 0 sequence-cluster splits, 0 held-out out-of-scope false
  non-abstentions, and moves `m_csa:628` to in-distribution. Its direct
  subchunk-009 rerun passes with 15,531 mapped rows, 2,939 train/test rows,
  max TM-score `0.6699`, and 0 target-violating pairs. Continue from round-6
  subchunk `010/112`; stop and fold in any new high-TM blocker before
  continuing broad coverage.
- Final verification passed: `git diff --check`, JSON parsing for the 10 new
  Foldseek artifacts, `PYTHONPATH=src python -m unittest discover -s tests`
  with 387 tests, `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  and `PYTHONPATH=src python -m compileall -q src tests`.

- STARTED_AT: 2026-05-15T05:02:16Z
- ENDED_AT: 2026-05-15T05:48:11Z
- Measured elapsed time: 45.917 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and regenerated work/status.md before
  commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Directly reran cluster-first round-3 subchunks 006 and 007 from
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json`.
  Subchunk 006 passed with 14,207 mapped rows, 2,356 train/test rows, max
  TM-score `0.6509`, and 0 target-violating pairs. Subchunk 007 failed with
  9,094 mapped rows, 4,976 train/test rows, max TM-score `0.8043`, and one
  blocker, `m_csa:45` versus held-out out-of-scope `m_csa:397`.
- Added `artifacts/v3_foldseek_tm_score_cluster_first_split_round4_1000.json`
  and `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round4.json`.
  Round 4 has 35 high-TM constraints, 14 constrained clusters, 0 projected
  violations, 0 sequence-cluster splits, 0 held-out out-of-scope false
  non-abstentions, and moves `m_csa:397` to in-distribution.
- The direct round-4 subchunk-007 rerun passes with 9,094 mapped rows, 4,975
  train/test rows, max TM-score `0.6598`, and 0 target-violating pairs.
  Continue with bounded verification from the round-4 readiness, starting with
  the next unverified subchunk `008/112`. Stop and fold in any new high-TM
  blocker before continuing broad coverage.
- Final verification passed: `git diff --check`, JSON parsing for the 6 new
  Foldseek artifacts, `PYTHONPATH=src python -m unittest discover -s tests`
  with 387 tests, `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m compileall -q src tests`.

- STARTED_AT: 2026-05-15T04:00:46Z
- ENDED_AT: 2026-05-15T04:56:08Z
- Measured elapsed time: 55.367 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/foldseek_readiness_notes.md,
  work/handoff.md, work/scope.md, and work/status.md before commit.
- Normal locked direct run with no subagents or delegation. No M-CSA-only count
  growth and no external import.
- Implemented `build-foldseek-tm-score-cluster-first-split`, a review-only
  cluster-first candidate builder that turns observed `TM >= 0.7` Foldseek
  evidence into structural partition constraints before verification chunks
  run.
- The current handoff split is
  `artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json`: 34
  high-TM constraints, 14 constrained clusters, 0 projected known
  train/test violations, 0 sequence-cluster splits, and 0 countable/import-ready
  rows. Its readiness artifact is
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json`.
- Verification evidence: round-2 subchunk 006 passes with 14,207 mapped rows,
  2,358 train/test rows, max TM-score `0.6509`, and 0 target-violating pairs.
  Round-2 subchunk 007 fails with 9,094 mapped rows, 5,449 train/test rows,
  max TM-score `0.8651`, and 16 target-violating rows across 9 reported
  structure pairs; those blockers are folded into the round-3 split. Next
  verification should rerun subchunk 007 from the round-3 readiness and stop
  on any new target violation.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 383 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing for
  the 10 new Foldseek artifacts.

- STARTED_AT: 2026-05-14T03:33:18Z
- ENDED_AT: 2026-05-14T04:23:26Z
- Measured elapsed time: 50.133 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, docs/label_factory.md, work/scope.md,
  work/handoff.md, and work/status.md before commit.
- Normal locked delegated run per user instruction. No M-CSA-only count growth
  and no external import. The run added a real MMseqs2 backend external sequence
  search for the 30-row UniProtKB/Swiss-Prot sample, wired it into
  import-readiness, the blocker matrix, transfer gate, selected-pilot priority,
  pilot packets, representation plan/sample, and pilot dossiers.
- The backend search uses MMseqs2 `18-8cc5c`, covers 30 external rows against
  735 current reference accessions / 737 sequence records, keeps exact holdouts
  `O15527` and `P42126`, records 28 current-reference no-signal rows, 0
  near-duplicate rows, 0 failures, 0 countable rows, and 0 import-ready rows.
  The selected pilot rows no longer carry stale complete-near-duplicate-search
  blockers for backend no-signal evidence; broader UniRef/all-vs-all duplicate
  screening remains a limitation before import.
- Final verification passed: `PYTHONPATH=src python -m unittest discover -s
  tests` with 313 tests, `PYTHONPATH=src python -m catalytic_earth.cli
  validate`, `PYTHONPATH=src python -m compileall -q src tests`, `git diff
  --check`, and JSON parsing across 1706 artifact files. The external transfer
  gate passes 67/67 review-only checks.

- STARTED_AT: 2026-05-13T23:26:40Z
- ENDED_AT: 2026-05-13T23:51:56Z
- Measured elapsed time: 25.267 minutes
- Documentation checked and updated across README,
  docs/external_source_transfer.md, work/scope.md, work/handoff.md,
  work/status.md inputs, and work/external_source_transfer_1025_notes.md before
  status regeneration.
- Normal locked SPOF-hardening run kept M-CSA-only growth stopped and did not
  import external labels. The code-confirmed blocker was selected-pilot
  representation coverage: pilot dossiers had representation rows for only 4
  of the 10 selected candidates because they depended on the 12-row mapped
  control sample.
- The run added a pilot-specific representation backend plan/sample for all 10
  selected pilot candidates, refreshed the pilot dossiers, added the pilot
  representation sample to candidate-lineage validation, and added a focused
  gate requiring selected-pilot representation sample coverage. The transfer
  gate now passes 66/66 and keeps all external rows review-only,
  non-countable, and not import-ready; `P55263` is a representation
  near-duplicate holdout.
- Remaining-time plan executed in the same run: after the pilot sample covered
  all selected rows, harden the artifact graph by adding a negative regression
  for stale pilot representation sample rows and a direct 66th gate check for
  selected-pilot representation coverage.
- Final verification passed: `PYTHONPATH=src python -m unittest discover -s
  tests` with 298 tests, `PYTHONPATH=src python -m catalytic_earth.cli
  validate`, `PYTHONPATH=src python -m compileall -q src tests`,
  `git diff --check`, and JSON artifact parsing with `jq empty`.

- STARTED_AT: 2026-05-13T22:25:38Z
- ENDED_AT: 2026-05-13T22:33:55Z
- Measured elapsed time: 8.283 minutes
- Documentation checked and updated across README, docs/external_source_transfer.md,
  work/scope.md, work/handoff.md, and
  work/external_source_transfer_1025_notes.md before status regeneration.
- Normal locked SPOF-hardening run kept M-CSA-only growth stopped and did not
  import external labels. Counterevidence maintainability, text leakage,
  sequence/fold proxy holdout, learned representation sample, and selected-PDB
  override evidence were already present, so the bounded unblocked item was the
  artifact-graph consistency gap in the external transfer gate.
- The external gate's shared candidate-lineage registry now includes
  `sequence_holdout_audit`; a negative regression shows a mismatched holdout
  accession fails the lineage gate, and
  `artifacts/v3_external_source_transfer_gate_check_1025.json` still passes
  65/65 with 0 countable/import-ready external rows.
- Final verification passed: `PYTHONPATH=src python -m unittest discover -s
  tests` with 296 tests, `PYTHONPATH=src python -m catalytic_earth.cli
  validate`, `PYTHONPATH=src python -m compileall -q src tests`,
  `git diff --check`, and changed JSON artifact parsing.

- STARTED_AT: 2026-05-13T06:06:38Z
- ENDED_AT: 2026-05-13T06:57:46Z
- Measured elapsed time: 51.133 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/external_source_transfer.md, docs/v2_strengthening_report.md,
  work/scope.md, work/handoff.md, work/label_factory_notes.md,
  work/label_preview_1025_notes.md, work/external_source_transfer_1025_notes.md,
  and work/external_source_control_repair_1025_notes.md before status
  regeneration.
- Normal locked run kept external UniProtKB/Swiss-Prot candidates review-only
  and repaired the post-M-CSA transfer controls without importing labels.
- Expanded structure mapping and heuristic scoring from 4 to all 12
  heuristic-ready external controls, added control-repair, representation,
  binding-context, full reaction-context, and sequence-holdout artifacts, and
  kept every external row non-countable.
- The external transfer gate now passes 33/33 checks for review-only evidence
  collection; the repair plan records 25 non-countable repair rows, the
  representation manifest exposes 12 mapped controls, the binding-context
  sample maps 7/7 rows as context only, and the sequence audit keeps two exact
  reference overlaps as holdouts.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 247 tests,
  targeted external-transfer/scaling tests, JSON artifact parsing, external
  import/countable violation scan, and `python -m compileall -q src tests`.

- STARTED_AT: 2026-05-13T04:04:36Z
- ENDED_AT: 2026-05-13T04:55:29Z
- Measured elapsed time: 50.883 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/external_source_transfer.md, docs/ingestion_plan.md,
  docs/research_program.md, docs/safety_scope.md, docs/v2_report.md,
  docs/v2_strengthening_report.md, work/scope.md, work/handoff.md,
  work/label_factory_notes.md, work/label_preview_1025_notes.md, and
  work/external_source_transfer_1025_notes.md before status regeneration.
- Normal locked run from the non-promoted 1,025 preview kept M-CSA-only growth
  stopped and hardened external-source transfer without importing labels.
- Added review-only external candidate manifest, manifest audit, lane-balance
  audit, evidence plan/export, active-site evidence queue, import-safety audit,
  11/11 transfer gate, Rhea reaction-context sample, and reaction-context audit.
  All external artifacts keep `countable_label_candidate_count=0`.
- The evidence plan flags seven broad/incomplete EC candidates; the active-site
  evidence queue exports 25 ready review-only candidates and defers five rows
  (two exact-reference holdouts and three broad-EC disambiguation cases).
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 230 tests,
  targeted external-transfer tests, and `python -m compileall -q src tests`.

- STARTED_AT: 2026-05-13T03:03:14Z
- ENDED_AT: 2026-05-13T03:54:50Z
- Measured elapsed time: 51.600 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md,
  docs/research_program.md, docs/ingestion_plan.md, docs/safety_scope.md,
  docs/external_source_transfer.md, work/scope.md, work/handoff.md,
  work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_1025_notes.md before status regeneration.
- Normal locked run from the accepted 1000 state first made an evidence-based
  confidence call, opened the bounded 1025 preview, and stopped promotion when
  the acceptance artifact added 0 clean countable labels.
- The 1025 preview gate passes 21/21 checks and records 0 hard negatives, 0
  near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope
  failures, 0 accepted review-gap labels, and 0 review-only import count
  growth. All 329 preview review-state rows remain non-countable.
- Source-scale audit now records 1,003 observed M-CSA source records for the
  requested 1,025 tranche, so M-CSA-only scaling is the active bottleneck. The
  run added review-only external-source transfer, query, OOD calibration,
  30-row UniProtKB/Swiss-Prot candidate sample, and sample guardrail artifacts
  with 0 countable external candidates.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 217 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing across
  1627 artifact/registry files.

- STARTED_AT: 2026-05-13T01:00:39Z
- ENDED_AT: 2026-05-13T02:01:02Z
- Measured elapsed time: 60.383 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md,
  work/label_preview_975_notes.md, and work/label_preview_1000_notes.md before
  status regeneration.
- Normal locked run from the accepted 950 state first made an evidence-based
  confidence call, accepted the bounded 975 batch, then opened, repaired, and
  accepted the bounded 1000 batch.
- The 1000 gate passes 21/21 checks and records 0 hard negatives, 0 near
  misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope
  failures, 0 accepted review-gap labels, 0 accepted reaction/substrate
  mismatch labels, and 0 review-only import count growth.
- The canonical registry now has 679 labels. All 326 accepted-1000 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_1000.json`, including the
  21 new 1000-preview review-debt rows. `m_csa:986` is explicitly deferred as
  local-heme low-score boundary evidence rather than counted out-of-scope.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 206 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing across
  artifact/registry files.

- STARTED_AT: 2026-05-12T23:58:38Z
- ENDED_AT: 2026-05-13T00:50:24Z
- Measured elapsed time: 51.767 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_950_notes.md before status regeneration.
- Normal locked run from the accepted 850 state first made an evidence-based
  confidence call, then accepted the bounded 875, 900, 925, and 950 batches.
- The 950 gate passes 21/21 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 673 labels. All 282 accepted-950 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_950.json`, including the
  19 new 950-preview review-debt rows. `m_csa:865` is explicitly classified as
  `expert_review_decision_needed` rather than unclassified review debt.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 205 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and JSON parsing across
  1432 artifact/registry files.

- STARTED_AT: 2026-05-12T16:56:09-05:00
- ENDED_AT: 2026-05-12T17:58:13-05:00
- Measured elapsed time: 62.067 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_850_notes.md before status regeneration.
- Normal locked run from the accepted 775 state first made an evidence-based
  confidence call, then accepted the bounded 800, 825, and 850 batches.
- The 850 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 652 labels. All 203 accepted-850 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_850.json`, including the
  22 new 850-preview review-debt rows. `m_csa:836` is explicitly deferred as
  role-inferred metal-hydrolase evidence without local ligand support rather
  than counted.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 205 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and `jq empty` across
  JSON artifacts.

- STARTED_AT: 2026-05-12T20:55:05Z
- ENDED_AT: 2026-05-12T21:45:56Z
- Measured elapsed time: 50.850 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/performance.md,
  docs/v2_strengthening_report.md, docs/v2_report.md, work/scope.md,
  work/handoff.md, work/status.md inputs, work/label_factory_notes.md, and
  work/label_preview_775_notes.md before status regeneration.
- Normal locked run from the accepted 750 state first made an evidence-based
  confidence call, then opened, repaired, and accepted the bounded 775 batch.
- The 775 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 642 labels. All 138 accepted-775 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_775.json`, including the
  20 new 775-preview review-debt rows. `m_csa:771` is explicitly deferred as
  counterevidence/text-leakage risk rather than counted.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 202 tests,
  `PYTHONPATH=src python -m compileall -q src tests`, and `jq empty` across
  JSON artifacts.

- STARTED_AT: 2026-05-12T19:54:22Z
- ENDED_AT: 2026-05-12T20:14:16Z
- Measured elapsed time: 79.900 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  docs/geometry_features.md, docs/v2_strengthening_report.md, work/scope.md,
  work/handoff.md, work/label_factory_notes.md, and
  work/label_preview_750_notes.md before status regeneration.
- Normal locked run from the accepted 725 state first made an evidence-based
  confidence call, then explicitly deferred the 750 preview review-debt surface
  and promoted the seven clean 750 candidates into the canonical registry.
- The 750 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- The canonical registry now has 637 labels. All 118 accepted-750 review-state
  rows remain non-countable under
  `artifacts/v3_accepted_review_debt_deferral_audit_750.json`, including the
  18 new 750-preview review-debt rows.
- Final verification passed: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 200 tests, and
  `PYTHONPATH=src python -m compileall -q src tests`.

- STARTED_AT: 2026-05-12T17:51:49Z
- ENDED_AT: 2026-05-12T18:51:39Z
- Measured elapsed time: 59.833 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  work/scope.md, work/handoff.md, work/status.md inputs, and
  work/label_preview_750_notes.md before status regeneration.
- Normal locked run from the accepted 725 state first made an evidence-based
  confidence call, then added an accepted-725 review-debt deferral audit with
  100 non-countable rows and upgraded the 725 gate to 21/21 checks.
- Remaining-time plan executed before wrap-up: after the 725 deferral audit was
  clean, opened a bounded 750 preview. The 750 preview generated graph,
  geometry, retrieval, label-factory, review export, acceptance, scaling-quality,
  ontology-gap, learned-retrieval, and sequence-similarity artifacts. It found
  7 mechanically clean candidates and a 19/19 preview gate, but promotion is
  deferred because 18 new review-debt rows require repair or explicit deferral.
- Final verification passed: `git diff --check`, `jq empty` over regenerated
  JSON artifacts, `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 200 tests, and
  `PYTHONPATH=src python -m compileall -q src tests`.

- STARTED_AT: 2026-05-12T11:51:27-05:00
- ENDED_AT: 2026-05-12T12:47:20-05:00
- Measured elapsed time: 55.883 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  work/scope.md, work/handoff.md, work/status.md inputs, and
  work/label_preview_725_notes.md before status regeneration.
- Normal locked run from the accepted 700 state first made an evidence-based
  confidence call, then accepted the bounded 725 label-factory batch with 6
  clean countable labels and 100 review-state rows kept outside the benchmark.
- The 725 gate passes 20/20 checks and records 0 hard negatives, 0 near misses,
  0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0
  accepted review-gap labels, 0 accepted reaction/substrate mismatch labels,
  and 0 review-only import count growth.
- Remaining-time plan executed before wrap-up: after accepting 725, added
  review-only repair controls for 95 expert-label decision rows, 25
  local-evidence lanes, 8 alternate residue-position requests, a focused
  alternate-structure scan, strict remap-local audit for `m_csa:712`,
  ontology-gap audit, learned-retrieval manifest, sequence-similarity failure
  controls, regression tests, and documentation. Next run should repair or
  explicitly defer the accepted-725 review-debt surface before blind 750
  scaling.

- STARTED_AT: 2026-05-12T15:50:29Z
- ENDED_AT: 2026-05-12T16:41:18Z
- Measured elapsed time: 50.817 minutes
- Documentation checked and updated across README, docs/label_factory.md,
  work/scope.md, work/handoff.md, work/label_preview_700_notes.md,
  work/expert_label_decision_local_evidence_gap_700_notes.md,
  work/atp_phosphoryl_transfer_family_expansion_700_notes.md, and status
  inputs before status regeneration.
- Normal locked run from the accepted 700 state did not grow the countable
  registry. It implemented the expert-reviewed ATP/phosphoryl-transfer family
  expansion for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and GHMP as
  ontology/family-boundary evidence.
- The expansion artifact maps 20 supported reaction/substrate mismatch lanes
  across all nine target families, records 4 non-target expert hints and 0
  unsupported mappings, and keeps `countable_label_candidate_count=0`.
- The 700 gate now passes 21/21 checks and requires complete mismatch-lane
  export, complete expert-label decision export, complete expert-label
  repair-candidate coverage, complete repair-guardrail coverage, complete
  local-evidence gap audit/export, local-evidence repair resolution, explicit
  alternate residue-position requests, review-only import-safety evidence, and
  ATP/phosphoryl-transfer family expansion evidence with 0 countable candidates.
  The scaling-quality audit and batch summary also carry those gates.
- Final verification passed: `git diff --check`, `jq empty` over regenerated
  JSON artifacts, `PYTHONPATH=src python -m catalytic_earth.cli validate`,
  `PYTHONPATH=src python -m unittest discover -s tests` with 198 tests, and
  `PYTHONPATH=src python -m compileall -q src tests`.

- 2026-05-21 ePK pause/no-go synthesis: `docs/epk_heuristic_geometry_no_go_20260521.md`
  and `artifacts/v3_epk_heuristic_geometry_no_go_decision_20260521.json`
  record the research-director decision that heuristic geometry-only ePK
  production activation is a no-go. Current ePK agents should be paused rather
  than allowed to keep building review-only machinery. Future ePK work should
  restart only for a learned-context pilot, a clean active-state candidate
  search, a terminal candidate-class decision, or a wet-lab/expert-adjudication
  bridge. No labels, fingerprints, thresholds, production scorers, imports, or
  migration state changed.
