# Handoff

<!-- current-research-handoff:start -->
## Current research handoff â€” Huber benchmark narrowed, 2026-10-09

- **Run/continuity:** automation run
  `automation-6ac8bd9adeb8819096b82a61101ea18a-20261009T163745Z`, shared-control
  epoch 9, from merged main `dc8947d9e2029a2dc5ab1d181d8ddb2487422218`.
  PRs #143â€“#148, the Choi stop and all frozen evidence were preserved. Three
  complementary same-model source/data/critical reviews were used; they are not
  independent expert review.
- **Question:** can Huber et al.'s public exact-sequence DNA-recording panel
  support the inherited family- or substrate-held-out sequence-specificity
  benchmark with comparable quantitative negatives?
- **Finding:** no for that proposed split. The author ML task contains one
  TEVp-I scaffold, six mutable protease positions and 20 ENLYFQX substrates.
  The model receives only the six protease residues and emits 20
  substrate-specific heads, so family holdout is impossible and substrate
  holdout is not the released task. The fixed 1,000-variant test is randomly
  selected from 1,625 fully measured AB variants with at least 100 reads per
  substrate; the paper's design analysis explicitly emulates search on these
  already measured outcomes. This is an exposed, coverage-selected retrospective
  test, not a new prospective cohort.
- **Endpoint and identity:** the released code supplies the constant full parent
  sequence and mutation-block mapping, and the raw campaign reproduces the
  1,625-row complete cohort and seed-42 test identity. The recorder provides
  continuous fraction-flipped AUC4h, reads and within-screen quantitative
  negatives. It subtracts screen-specific inactive controls, sets values inside
  their 95% interval to zero and retains a small C151A binding contribution.
  Raw AUC is not a common cleavage scale across screens, and reporter activation
  does not localize the peptide bond. Selected post-screen FRET checks cannot
  calibrate the full panel. The primary Methods report hysteretic thresholds
  p1=0.01/p2=0.1, while archived code/config use 0.01/0.05; any later work must
  freeze and disclose a sensitivity analysis rather than silently choose one.
- **Decision:** do not repeat the spent random split or preregister it as family
  or substrate generalization. The only supported scope is retrospective
  within-scaffold reporter-activity prediction; it cannot show intended-bond
  cleavage, rate, de novo design, new-scaffold transfer or Problem 8 success.
  Exact hashes, reconstruction counts and boundaries are in
  `tools/research_lanes/protease_retargeting/huber_reporter_benchmark_qualification.json`.
- **Next consequential action:** qualify and preregister the separate, single-
  campaign TEVp-0 single-mutant by 134 single-mutant-substrate matrix for
  two-axis blocked folds. Compare a row-plus-column additive baseline with
  Hamming/biochemical interaction and Atlas representations. Continue only if
  exact construct/control provenance survives and interaction information beats
  the additive baseline on every frozen fold; otherwise stop. Any result remains
  retrospective reporter generalization.
- **Acquisition incident:** the two source-repository clones materialized known
  pack files totaling 96,056,357 bytes before size inspection, exceeding the
  new batch's default 30 MiB cap. Further acquisition for
  `huber_reporter_audit_20261009` is stopped. The 864 MB processed and 37 MB raw
  release assets were not downloaded; the checked-in raw archive was sufficient.
  This breach is recorded rather than used to reset the allowance.
- **Boundaries:** no model, scorer, training, paid compute, provider mutation,
  separately billed API, lab order or outreach. Prime remains disabled; USD 8
  per job and USD 50 per Chicago month are unchanged. Protected registries and
  prior outcomes remain frozen.
<!-- current-research-handoff:end -->

## Historical handoffs â€” superseded as an execution queue

## Current research handoff â€” cloud team deployment, 2026-10-09

- **Standing execution authorization:** the owner requests hourly research in
  Codex Cloud, independent of the laptop, using only Codex/ChatGPT allowance.
  Prime Intellect may cost at most **USD 8 per logical job and USD 50 per
  America/Chicago calendar month**, including retries, failures and overhead.
  This supersedes the completed rental's narrower authorization for future
  justified jobs, but does not establish operational readiness. Follow
  [the cloud team instructions](../docs/CLOUD_RESEARCH.md). No separately billed
  agent API, lab orders or outreach are authorized.
- **Deployment checkpoint:** private `catalytic-earth` Codex Cloud environment
  prepared on 2026-10-09; CPU build and 872 core tests (3 skipped) passed.
  GitHub API reports repository write permission; public research domains and
  Prime's unauthenticated HTTPS endpoint are reachable. The setup chat is
  `01a11ffa-26ca-7641-8f06-492c6773f001` on host `durable`. The environment is
  published. The schedulable cloud Work controller is
  `6ac8b6f5-a864-83ea-8ee0-e81d7dc82f8d` (backend
  `01a1200a-b70b-73df-8012-3235ce7a6030`, host `durable`). It verified cloud
  Python/Git, public source access and GitHub connector writes, then completed
  the live shared-control start/heartbeat/checkpoint/complete cycle, ending idle
  at `6caab4e5c797017fc166cb72c19dd9f20ccc80a8`. Separate cloud checkouts saw the
  same record; all nine helper tests passed there. This Work chat cannot attach
  the published environment and has no shell push credential; use the tested
  connector path. PR #141 contains the deployment changes. No hourly cloud
  schedule is activated at this checkpoint; activation requires its passing CI,
  merge and a real scheduled-run check. All old local schedules stay
  paused. No Prime cloud secret or tested unattended paid lifecycle exists yet;
  paid launches remain disabled. The shared control helper is coordination and
  budget infrastructure, not a provider adapter or scientific result.

- **Direction:** the owner clarified on 2026-10-09 that Problem 8 is the primary
  target: design proteases on demand that cut a chosen protein sequence
  specifically and efficiently. Develop the full computable Atlas through the
  mechanisms, constraints and evidence needed for that research. Choose the
  strongest available approach; proving Atlas's added value is not a prerequisite
  for progress toward protease capability. No working protease or Atlas design
  advantage is claimed. Both finite design comparisons and the earlier
  substrate-window comparison remain closed without rescue sampling.
- **Completed question:** does fixed enzyme/substrate sidechain geometry during
  LigandMPNN sequence design improve joint recovery on the retained
  water-fixed-seed-3 scaffold? All eight distinct sequences and 80 unconditioned
  RF3 predictions completed. No new backbone was generated.
  [Result and complete evidence](../tools/research_lanes/protease_retargeting/sidechain_context/results_20261002/README.md).
- **Primary result:** no consistent joint reference-recovery advantage.
  Revealed-minus-hidden median worst-group RMSDs are âˆ’4.655, +8.309, +9.484 and
  +14.937 Ã… for paired sequence seeds 200â€“203. Even seed 200 worsens base and
  reactive-backbone medians (+0.227/+0.236 Ã…). All 40 complex and 40 monomer
  assignments are retained. Four design-seed pairs, not 40 independent complex
  experiments, are the comparison units. Keep the frozen endpoint unchanged.
- **Scientific consequence:** the input omission was verified, but exposing it
  did not repair joint recovery on this scaffold. Native context adds 55 fixed
  sidechain atoms while retaining Zn/water for every polymer residue. All 868
  finite audited retained coordinates per sequence-design output are unchanged.
  Revealed complex fold RMSD medians are 9.166â€“14.617 Ã…; isolated donor gains
  can accompany large metal-ligand losses. Do not adopt this switch as an
  established repair or try further water/context seeds to find a favorable one.
- **Reassessment using existing evidence:** retrospective calculation on all 20
  already completed TDPn3 predictions uses its own correctly mapped author AF3
  reference. Median worst-group errors are 0.646/0.797 Ã… for the 10mer versus
  2.864/2.672 Ã… for the 12mer, largely water displacement, with close global
  fold recovery. Published activity therefore coexists with imperfect predicted
  water geometry. This positive-only context is not an activity discriminator,
  a new prediction experiment or a cross-scaffold ranking. Original source
  assays and isolated peptide prediction contexts remain distinct.
- **Next consequential action:** establish an exact sequence- and assay-matched
  inactive control retaining the catalytic identities/atoms scored here, using
  primary construct/assay evidence within the remaining source budget. Stop if
  a comparable pair cannot be established. TDPn3's general-base knockout lacks
  an exact retained substitution; do not invent E147A. Even a confirmed E147A
  removes scored Glu atoms, making a missing-group penalty tautological; such
  a control needs a separately justified common endpoint. The unnormalized
  113-design screen cannot automatically supply matched inactive labels.
  No suitable negative is established, so activity discrimination using this
  readout is not currently executable. Bound this control search to the question
  it can unlock. If unavailable, close that evaluation route and choose another
  justified experiment toward the same Problem 8 capability; this is not a
  prerequisite for all protease research or Atlas development. The positive-only
  reanalysis is complete; do not repeat it or relabel it validation. Any new
  compute requires a justified new question and the standing execution limits
  and readiness checks above; the completed rental is closed.
- **Evidence boundaries:** one post hoc selected imposed hybrid scaffold, four
  new sequence seeds; combined enzyme/substrate context, not Tyr-only causality.
  Public LigandMPNN differs from author EnhancedMPNN. RF3 cached MACE features
  were absent in both arms; common fallback does not establish equivalent
  quality. Per-input native RNG reset is not atom-matched noise or bitwise GPU
  identity. No rate, barrier, specificity, physical fold or measured function.
- **Compute:** current user continuation authorized the bounded follow-up.
  A100 offers vanished before creation; one RTX6000Ada at $0.75/hour was frozen
  before sampling under the same two-hour/$5 ceiling. Pod
  `39a95f4dd24448cd923ac3ef2ec9ca34` was provider-confirmed TERMINATED at
  20:07:41 UTC after verified retrieval; estimated $0.20, final charge unavailable.
  No paid instance remains from this run. No wet work, outreach or order.
- **Verification and ownership:** 431 archived file hashes and all 80 assigned
  CIF hashes verified. Local recomputation matches all 1,548 numeric readouts
  within 2.85e-14. Separate Astra/max workers check raw-coordinate arithmetic,
  native identities/context/RNG and mechanistic interpretation. Same-model
  checks are not independent expert review. Seven unrelated demo paths and
  protected registries are preserved; deployment status is recorded above.
- **Completed experiment/publication:** started 2026-10-02 at 19:29:38 UTC; base
  `837afd8faff28455bc94dfa1cc6ee606e6dbbb54`; branch
  `codex/protease-sidechain-context`; local receipt
  `.git/catalytic-earth-runs/20261002T192938Z-protease-sidechain-context/`.
  Scientific freeze `dddd4e8c`; hardware amendment `14119cfd`, both before sampling.
  PR #139 merged as `400aaccb`; all four CI checks passed and the run lock was
  released. No second queue or replacement samples were created.
- **Direction update:** owner-requested priority alignment only, starting from
  `400aaccba948dfa684e4fb6b205c075a7b16cd47` on
  `codex/problem8-primary-target`. No new scientific result, model execution,
  source acquisition or paid compute. Current publication state is in Git and
  `.git/catalytic-earth-runs/20261009T090124Z-problem8-direction/`.
- **Acquisition:** no new author-source acquisition. Named source batch remains
  30,250,296 of 31,457,280 bytes and 92 of 100 requests. Official runtime/packages
  and 3,049,418,389 checkpoint bytes were separately authorized for this rental;
  do not reset the named source budget or treat unmetered package traffic as an
  exact receipt. Earlier acquisition receipts remain unchanged.


## Session run - Option B started: M-CSA held-out EXHAUSTED; new untouched off-M-CSA bronze held-out FROZEN before any router fix (2026-06-28)

- Continued on `main`/branch (d14fa1f7+). User: "pursue Option B â€” the new held-out." Leakage-safe order:
  freeze the validation vehicle before any model change.
- FINDING: M-CSA held-out is spent. Designated partition 140; one-shot spent 126; only **14 untouched
  (1 in-scope, 13 OOS), no structures**. (All 126 spent rows were inside the partition -> original claim
  clean.) So a repaired fine-57 router cannot be validated on a fresh M-CSA held-out.
- NEW HELD-OUT: `src/catalytic_earth/option_b_heldout_preregistration.py`,
  `build-option-b-heldout-preregistration` ->
  `artifacts/v3_option_b_heldout_preregistration_current702_20260628.json` /
  `work/option_b_heldout_preregistration_current702_20260628.md`, status
  `preregistered_not_yet_run_pending_router_fix`. Drawn from untouched off-M-CSA bronze: **22**
  high-confidence atlas-family non-M-CSA positives (**13 non-metal, 9 metal**), disjoint from train/cal,
  M-CSA, and the 162 used in recovery dev. Content-hash `7ffa38d8...` (deterministic). Pre-committed bar
  (first principles, before scoring): recovery >= **0.70** AND non-metal->metal misroute <= **0.20**.
  The metal/non-metal split directly tests the Gate-1 failure mode.
- Caveats (honest): n=22 (focused probe, not precise), bronze (concordance not gold), off-M-CSA,
  structures to materialise. A deployment-grade Option-B validation needs gold-curated rows.
- Tests: `tests/test_option_b_heldout_preregistration.py` (5) + CLI parser case.
- Validation: focused unittest OK; compileall OK; registry `validate` OK (57 FP); reference check regen
  below; `git diff --check` clean; no held-out scored; no data/ change.
- Next exact action (Option B continuation): (1) implement the fine-57 router repair on train/cal only
  (constrain metal v2-subclasses to require metal-cofactor support; re-verify calibration -> ~30/35);
  (2) freeze the repaired-router rule; (3) materialise structures for the 22 frozen accessions (verify
  sha 7ffa38d8 first) and run the one-shot vs the bar. Do not re-run the spent M-CSA held-out; do not
  grow fingerprint families.

## Session run - Gate 1 router reconciliation (fine-57 drift = genuine misrouting, adopt June 9 coarse router); branch merged to main via clean fast-forward (2026-06-28)

- MERGE CORRECTION: an earlier claim in this run that branch and `main` were "unrelated histories with
  divergent registries" was WRONG â€” a **shallow-clone artifact**. After `git fetch --unshallow`, the
  real common ancestor is `79dc2d3a` (session base; shared root `93806418`), local `main` (`bed58963`)
  is an ancestor of the branch, and the branch is a strict superset (main 0 commits ahead, branch 148
  ahead). Merged via clean fast-forward: `main == d7a985ed` (origin/main + local main + branch all
  equal). No conflicts, nothing lost.

- Continued on branch `claude/continue-last-commit-ytktge` from commit `937b24a6`. User: "merge all
  progress and start work on Gate 1."
- MERGE: `main` and this branch have **no common ancestor** (roots: main 468591fd, branch f60617d6) and
  **divergent `mechanism_fingerprints.json`** (main 2670b1ad vs branch 19d837f1; curated702 identical).
  A merge would be `--allow-unrelated-histories` with whole-tree + registry conflicts. NOT forced â€” that
  reconciliation is the user's call. All progress is already pushed to the branch (line of record).
- GATE 1: added `src/catalytic_earth/router_reconciliation_diagnostic.py` +
  `build-router-reconciliation-diagnostic`. Artifact/report:
  `artifacts/v3_router_reconciliation_diagnostic_current702_20260628.json` /
  `work/router_reconciliation_diagnostic_current702_20260628.md`. Status
  `fine_router_drift_includes_genuine_misrouting_not_just_relabeling`:
  - Calibration in-scope (35) @ 0.4115: exact 13; documented v2-split relabeling -> **26/35**; June 9
    ref **30/35**. NOT reconcilable by relabeling (gap 4).
  - **8 genuine misroutes; 7 are non-metal (flavin/heme/PLP) enzymes over-claimed by fine-57 metal
    v2-subclass fingerprints** in the fused geometry router. Coarse June 9 has no metal subclasses ->
    no misroute -> 30/35.
  - Fork resolved on evidence: **Option A (June 9 coarse router)** = deployable validated baseline now
    (held-out PASS 35/47, 15/79 OOS FP), coarse granularity. **Option B (repair fine-57)** = real router
    fix (constrain metal subclasses) + NEW pre-registration + NEW held-out; only if fine metal-subclass
    calls are needed. Recommendation: A now, B as scoped follow-up.
- Calibration-only; spent held-out untouched; no registry/ontology/label/threshold/model change.
- Tests: `tests/test_router_reconciliation_diagnostic.py` (5) + CLI parser case.
- Validation: focused unittest OK; compileall OK; registry `validate` OK (57 FP); reference check regen
  below; `git diff --check` clean.
- Next exact action (Gate 1 close-out, needs user): (i) decide the merge/registry reconciliation for
  `main`; (ii) pick the fork â€” adopt June 9 coarse router (then Gate 2 gold off-M-CSA + Gate 3
  productionize), or invest in Option B fine-router repair (constrain metal subclasses; new held-out).
  Do not re-run the spent held-out one-shot; do not grow fingerprint families.

## Session run - DEPLOYMENT CLAIM (M-CSA): locked held-out one-shot executed once and PASSED (35/47 recovery, 15/79 OOS FP); no main-repo registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `00031510`. User: "continue
  till we make a deployment claim", no shortcuts. The honest endpoint = execute the locked held-out
  one-shot. Done. No main-repo registry/label/threshold/model mutation (registry validated intact at
  57 FP after).
- Added executor `src/catalytic_earth/heldout_oneshot_eval.py` + `run-heldout-oneshot-eval`, and a
  minimal additive `split_assignment` param on `build_cofactor_fusion_operating_point` (default
  unchanged) so held-out rows are scored via the exact calibration-replay router. Committed infra
  first (no results).
- Executed in an isolated worktree, registry pinned to `d567ee0d`:
  - VALIDATION first: calibration at threshold 0.44 reproduced the known dial exactly (30/35 @ 8 FP).
  - ONE-SHOT: executor verified the frozen set sha256 (`45632519...`, 47 in-scope + 79 OOS, full
    coverage) and scored via the pinned June 9 router at 0.44.
  - Result PASS: recovery **35/47 (0.745)** >= 0.70; OOS-FP **15/79 (0.190)** <= 0.40. Artifacts
    `artifacts/v3_heldout_oneshot_eval_result_current702_20260628.json` /
    `work/heldout_oneshot_eval_result_current702_20260628.md`.
  - Worktree removed; main registry confirmed clean.
- Folded the PASS into the consolidated readiness summary (now reads
  `deployment_claim_made_mcsa_heldout_passed_offmcsa_generalizes`).
- THE HELD-OUT ONE-SHOT IS NOW SPENT. Do not re-run it. Any future router/threshold change needs a NEW
  pre-registration and (ideally) a different held-out set.
- Scope honesty: the validated claim is M-CSA. Off-M-CSA the fold channel generalizes on both halves
  (recovery 132/156 bronze, rejection). Still open: a SwissProt-wide GOLD off-M-CSA claim (bronze labels
  are automation-curated, not gold) and broadening beyond cofactor families (data-blocked).
- Tests: `tests/test_heldout_oneshot_eval.py` (4, sha-guard + verdict), readiness PASS-path test added.
- Validation: focused unittest OK; compileall OK; registry `validate` OK (57 FP); reference check
  pending regen below; `git diff --check` clean; main `data/` untouched.
- Next exact action: if a broader claim is wanted, build a GOLD off-M-CSA recovery set (curated
  non-M-CSA positives with gold mechanism labels + structures) â€” a real curation effort. Otherwise the
  M-CSA deployment claim stands and the fold channel is the documented off-M-CSA lever. Do not grow
  fingerprint families; do not re-run the spent held-out one-shot.

## Session run - (b) deployment-readiness synthesis + (a) atlas-broadening feasibility (blocked); no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `88d61126`. User asked for "b
  then a". No registry/label/threshold/model mutation; no download; no heldout read.
- (b) Consolidated deployment-readiness summary (verifiable aggregate; reads source values + sha256,
  computes nothing new): `src/catalytic_earth/fold_channel_deployment_readiness.py`,
  `build-fold-channel-deployment-readiness` ->
  `artifacts/v3_fold_channel_deployment_readiness_summary_current702_20260628.json` /
  `work/fold_channel_deployment_readiness_summary_current702_20260628.md`. Status
  `fold_channel_generalizes_off_mcsa_both_halves_deployment_claim_still_gated`. Validated: off-M-CSA
  recovery 132/156 (0.846, all 4 cofactor families); off-M-CSA rejection (external 0.574 ~ M-CSA OOS
  0.566 << in-scope 0.743); June 9 dial 30/35 @ 8 FP. Not validated: no gold off-M-CSA; held-out
  one-shot locked/unspent (M-CSA-only); cofactor-family scope; calibration figures are development.
  (committed `2a639bc4`)
- (a) Attempted to broaden the atlas beyond the 5 cofactor families. Audit:
  `src/catalytic_earth/atlas_broadening_feasibility.py`, `build-atlas-broadening-feasibility` ->
  `artifacts/v3_atlas_broadening_feasibility_current702_20260628.json` /
  `work/atlas_broadening_feasibility_current702_20260628.md`. Status
  `blocked_atlas_broadening_no_fine_multifamily_mcsa_label_source`: fine (57-family) M-CSA truth labels
  exist only on the cofactor operating-point surface (5 families, 133 structures); label manifest has 0
  fine-fingerprint rows; curated registry is coarse-8 (incompatible); bronze is non-M-CSA. **52/57
  families unreachable for now.** Unblock = derive fine multi-family M-CSA truth labels
  (router/operating-point over the full in-distribution set) + structures (router-derived, not gold).
- Tests: `tests/test_fold_channel_deployment_readiness.py` (5), `tests/test_atlas_broadening_feasibility.py`
  (4), + CLI parser cases. Docs artifact-reference check -> missing 0.
- Validation: focused unittest OK; compileall OK; registry `validate` OK (57 FP intact); reference check
  missing 0; `git diff --check` clean; `data/` untouched.
- Next exact action: broadening (a) needs a fine multi-family M-CSA labelling effort (router-derived, not
  gold) â€” a real pipeline, the user's call. Otherwise the fold-channel result stands: generalizes off
  M-CSA on both halves for the cofactor families; remaining deployment gates are gold off-M-CSA eval and
  the locked held-out one-shot. Do not grow fingerprint families.

## Session run - off-M-CSA in-scope RECOVERY confirmed: fold-NN recovers 132/156 (84.6%) of non-M-CSA bronze positives across all 4 families; no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `6666474f`. User authorized the
  bounded download. No registry/label/threshold/model mutation; no heldout read.
- Executed the signed-off plan: downloaded **156/162** AlphaFold CIFs (6 are AFDB 404). Correction:
  AFDB URL is **v6** not v4 (v4 -> 404); fixed `AFDB_URL_TEMPLATE` + the unit test to v6 and regenerated
  the manifest (accession-list sha unchanged `1887478a...`). Staged CIFs (~70 MB) git-ignored; result
  TSV (872K, 12874 rows) committed.
- foldseek easy-search the 156 positives vs the M-CSA train atlas (same flags as the calibration
  recompute), built the positive map
  (`artifacts/v3_offmcsa_recovery_bronze_positive_map_current702_20260628.json`), and ran the recovery
  harness -> `artifacts/v3_fold_nn_mechanism_recovery_offmcsa_bronze_current702_20260628.json` /
  `work/fold_nn_mechanism_recovery_offmcsa_bronze_current702_20260628.md`.
- Result: recovery **132/156 (0.846)**, full coverage; per family flavin 83/96 (0.86),
  metal_dependent_hydrolase 26/34 (0.76), heme_peroxidase_oxidase 17/20 (0.85), plp 6/6 (1.00) â€” robust,
  not a flavin composition artifact. On par with the 28/35 (0.80) M-CSA baseline. Curve: fold-NN >= 0.74
  -> 93/95 (0.98) precision at 0.60 recovery.
- Significance: with the earlier abstention result, the fold channel now generalizes off M-CSA on BOTH
  halves (recovers off-distribution positives AND rejects off-distribution negatives). Strongest
  evidence the structural-retrieval lever is real, not an M-CSA artifact.
- Caveats: bronze labels are automation-curated (non-circular for fold since admission used
  sequence/cofactor, not structure, but not gold truth); scoped to the 4 cofactor atlas families; 6 AFDB
  404s.
- Tooling fix applied: download manifest module + test now use AFDB v6.
- Validation: focused unittest (manifest + recovery + full test_cli) 251 OK; compileall OK; registry
  `validate` OK (57 FP intact); docs reference check missing 0; `git diff --check` clean; disk 25 GiB
  free.
- Next exact action: optionally broaden the M-CSA atlas beyond the 5 cofactor families for a wider
  off-M-CSA recovery sweep; or write the consolidated deployment-readiness summary (fold channel: both
  halves generalize off M-CSA) and decide whether the held-out one-shot is still worth spending (still
  M-CSA-only). Do not grow fingerprint families.

## Session run - off-M-CSA recovery download manifest built (162 trusted bronze positives, ~97 MB); sign-off plan, NO fetch; no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `862a13e9`. User chose the
  off-M-CSA recovery line via the bounded-download path (preferred over spending the M-CSA-only
  held-out one-shot, which stays locked). Per plan, built the download manifest for sign-off BEFORE
  fetching anything. No download, no `data/` mutation.
- Located the expansion positives: `data/registries/external_bronze_labels.json` is a shard index ->
  `external_bronze_labels.shards/part-0000{0..4}.json` (9299 rows; schema entry_id `uniprot:ACC`,
  fingerprint_id, confidence, label_type, review_status). Present locally (~69 MB).
- Module + CLI: `src/catalytic_earth/offmcsa_recovery_download_manifest.py`,
  `build-offmcsa-recovery-download-manifest`. Artifact/report:
  `artifacts/v3_offmcsa_recovery_download_manifest_current702_20260628.json` /
  `work/offmcsa_recovery_download_manifest_current702_20260628.md`. Status
  `download_manifest_ready_awaiting_authorization`.
- Selection (frozen): high-confidence, in-scope (not out_of_scope), fingerprint in an M-CSA atlas
  family, non-M-CSA accession, not already structured -> **162** AlphaFold CIFs (~97 MB) across 4
  families (flavin_dehydrogenase_reductase 102, metal_dependent_hydrolase 34, heme_peroxidase_oxidase
  20, plp_dependent_enzyme 6). Accession-list sha256 `1887478a...`. URL pattern
  `https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_v4.cif`. Note: the M-CSA train atlas covers only
  5 cofactor families, so recovery is scoped to those (matches the 28/35 baseline's atlas).
- Non-circular: bronze admission used sequence/cofactor, not structure; bronze labels are evaluation
  targets only.
- Tests: `tests/test_offmcsa_recovery_download_manifest.py` (4) + a CLI parser-defaults case.
  Regenerated docs artifact-reference check -> missing 0.
- Validation: focused unittest (download manifest + full test_cli) OK; compileall OK; registry
  `validate` OK (57 FP intact); docs reference check missing 0; `git diff --check` clean; disk 25 GiB
  free (above the 10 GiB floor).
- Next exact action: on the user's sign-off of this manifest, fetch the 162 CIFs (skip-if-exists, stop
  below 10 GiB), foldseek vs the M-CSA train atlas, build the off-M-CSA positive map, and run
  build-fold-nn-mechanism-recovery-readout --positives <map> --foldseek-tsv <tsv> --surface-label
  offmcsa_bronze_high_confidence; compare to the 28/35 (0.80) M-CSA baseline and the abstention
  frontier. Held-out one-shot remains locked. Do not grow fingerprint families.

## Session run - held-out one-shot test PRE-REGISTERED (frozen rule + content-hashed 126-row set + pre-committed bar); scores no held-out data; no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `eea36c59`. Prompted by the
  user's leakage question ("are we training on test / using test to modify / cheating?"). Verified the
  honest answer: this session trained nothing, scored no held-out rows (every artifact
  `heldout_rows_scored: False`), and mutated no `data/` files (session diff touches only
  artifacts/docs/src/tests/work). The real caveat is calibration *reuse*: the same 35+26 calibration
  rows were inspected repeatedly, so all session operating points are optimistic development figures,
  not validated. This run locks the one unbiased test before running it.
- Module + CLI: `src/catalytic_earth/heldout_oneshot_preregistration.py`,
  `build-heldout-oneshot-preregistration`. Artifact/report:
  `artifacts/v3_heldout_oneshot_preregistration_current702_20260628.json` /
  `work/heldout_oneshot_preregistration_current702_20260628.md`. Status `preregistered_not_yet_run`.
  Locked: June 9 router @ 0.44 dial (registry pin `d567ee0d`); the 126-row held-out set (47 in-scope +
  79 OOS), enumerated + content-hashed `sha256 45632519...` (deterministic); pre-committed PASS bar
  recovery >= 0.70 AND OOS-FP rate <= 0.40 (calibration 0.857/0.308 minus ~2 SE); one-shot guardrail.
  Held-out labels used only to size/freeze the set, never as features; bar derived from calibration
  only.
- Execution (separately authorized one-shot, NOT done here): isolated worktree, pin registry to
  `d567ee0d`, build a held-out split manifest of exactly the 126 frozen entry_ids (verify sha256), run
  the cofactor_fusion_operating_point router over the held-out coordinate dirs at threshold 0.44, count
  recovery + OOS FP, compare to the bar, emit PASS/FAIL verbatim, stop. The execution path (scoring the
  held-out split) is not implemented yet and must match the frozen sha when built.
- Tests: `tests/test_heldout_oneshot_preregistration.py` (4) + a CLI parser-defaults case. Regenerated
  docs artifact-reference check -> missing 0.
- Validation: focused unittest (prereg + full test_cli) OK; compileall OK; registry `validate` OK
  (57 FP intact); docs reference check missing 0; `git diff --check` clean.
- Next exact action: decide whether to spend the held-out one-shot (it only certifies M-CSA, per the
  earlier note) by authorizing the frozen execution; and/or proceed with the still-pending off-M-CSA
  recovery decision (download trusted positives, or promote wave2 candidates via import gates). Do not
  grow fingerprint families.

## Session run - fold-NN mechanism recovery harness built + M-CSA baseline (28/35; 96% precision at fold>=0.65); ready to run off-M-CSA once a labelled positive set exists; no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `3f94b35b` (recovery
  feasibility). The off-M-CSA recovery run is gated on a user decision (download trusted-positive
  structures, or promote structured wave2 candidates through the import gates) that was NOT taken here
  (both are governance-gated). Built the harness so the eventual run is a one-liner â€” mirroring how the
  recompute manifest/command preceded foldseek availability.
- Module + CLI: `src/catalytic_earth/fold_nn_mechanism_recovery_readout.py`,
  `build-fold-nn-mechanism-recovery-readout`. Surface-agnostic: takes positives (accession + true
  fingerprint), their foldseek scores vs the M-CSA train atlas, and the atlas accession->fingerprint
  map (from the recompute manifest); reports fold-NN nearest-neighbour mechanism recovery + a
  recovery/abstention threshold curve.
- M-CSA in-distribution baseline (real run, existing recompute TSV):
  `artifacts/v3_fold_nn_mechanism_recovery_mcsa_baseline_current702_20260628.json` /
  `work/fold_nn_mechanism_recovery_mcsa_baseline_current702_20260628.md`. Recovery **28/35 (0.80)** no
  abstention (reproduces the recompute readout's match); confidence-gated precision-on-retained
  fold>=0.65 **24/25 (0.96)** @ 0.69 recovery, fold>=0.74 **17/18 (0.94)** @ 0.49 recovery. This is the
  reference the off-M-CSA recovery will be compared against.
- To run off-M-CSA later:
  `build-fold-nn-mechanism-recovery-readout --positives <nonmcsa_positive_map.json>
  --foldseek-tsv <nonmcsa_vs_mcsa_train_atlas.tsv> --surface-label offmcsa_<source>`.
- Tests: `tests/test_fold_nn_mechanism_recovery_readout.py` (4) + a CLI parser-defaults case.
  Regenerated docs artifact-reference check -> missing 0.
- Validation: focused unittest (recovery harness + full test_cli) OK; compileall OK; registry
  `validate` OK (57 FP intact); docs reference check missing 0; `git diff --check` clean.
- Decision still pending from the user (unchanged): authorize a bounded AlphaFold download for trusted
  bronze positives, OR authorize promoting structured wave2 candidates through the import/label-factory
  gates. Either unblocks the off-M-CSA recovery run; the harness and baseline are ready. Do not grow
  fingerprint families.

## Session run - off-M-CSA in-scope RECOVERY scoped and data-blocked (non-M-CSA structures exist but none carry trusted labels); read-only, no download, no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `8b6566dc` (off-M-CSA
  abstention). Read-only feasibility; no download, no registry/label/threshold/model change, no heldout.
- Scoped the recovery half of the off-M-CSA fold test. Audit builder + CLI:
  `src/catalytic_earth/offmcsa_recovery_feasibility.py`, `build-offmcsa-recovery-feasibility`.
  Artifact/report: `artifacts/v3_offmcsa_recovery_feasibility_current702_20260628.json` /
  `work/offmcsa_recovery_feasibility_current702_20260628.md`. Status
  `blocked_offmcsa_recovery_no_local_labeled_nonmcsa_positive_structures`:
  - 42 structured surfaces; **248** distinct non-M-CSA structured accessions locally (mostly wave2
    import candidates), but **0** production-label-ready (wave2: 0 ready, 600 in review; rest are
    external negatives/controls). Trusted bronze positives have labels but no local structures.
  - Unblock: (a) materialize AlphaFold CIFs for trusted bronze positives (download; needs auth + >=10
    GiB floor â€” wave2 itself recorded downloads disabled below the floor), or (b) promote structured
    wave2 candidates through import/label-factory gates (no new download).
- Bug fixed in passing: a too-strict accession regex `[A-NR-Z0-9]` dropped accessions containing
  O/P/Q (undercounted non-M-CSA structures as 11); corrected to `[A-Z][A-Z0-9]{5,9}` -> 248. Tests
  cover the classifier.
- Tests: `tests/test_offmcsa_recovery_feasibility.py` (4) + a CLI parser-defaults case. Regenerated
  docs artifact-reference check -> missing 0.
- Validation: focused unittest (feasibility + full test_cli) OK; compileall OK; registry `validate` OK
  (57 FP intact); docs reference check missing 0; `git diff --check` clean.
- Decision needed from the user: the off-M-CSA recovery half cannot be measured without trusted-labelled
  non-M-CSA structures. Either authorize a bounded AlphaFold download for a sample of trusted bronze
  positives, or authorize promoting a sample of structured wave2 candidates through the import gates.
  Until then, the off-M-CSA *abstention* result stands as the deployment-relevant finding; the *recovery*
  half is open and data-gated. Do not grow fingerprint families.

## Session run - fold-NN abstention signal GENERALIZES off M-CSA (external non-M-CSA negatives track M-CSA OOS, not in-scope); no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `ffb970df` (June 9 replay).
  Trigger: heldout is M-CSA-only (699/702), so an M-CSA heldout read can't probe the deployment
  distribution. No registry/ontology/label/threshold/heldout/model/fingerprint mutation.
- Tested whether the fold-NN abstention separation survives off M-CSA: **52 external non-M-CSA hard
  negatives** (6 overlapping current702 accessions excluded) fold-scored with `foldseek easy-search`
  against the **same M-CSA train in-scope atlas** (132 targets). Staging symlinks git-ignored; result
  TSV committed:
  `artifacts/v3_external_offmcsa_fold_abstention_current702_20260628_results/external_negatives_vs_mcsa_train_atlas.tsv`
  (4117 rows).
- Added readout builder + CLI:
  `src/catalytic_earth/external_offmcsa_fold_abstention_readout.py`,
  `build-external-offmcsa-fold-abstention-readout`. Artifact/report:
  `artifacts/v3_external_offmcsa_fold_abstention_readout_current702_20260628.json` /
  `work/external_offmcsa_fold_abstention_readout_current702_20260628.md`. Status
  `fold_nn_abstention_signal_generalizes_off_mcsa`:
  - External off-M-CSA negative fold-NN median **0.574** â‰ˆ M-CSA OOS **0.566**, far below M-CSA
    in-scope **0.743**; only 2/52 reach the in-scope median.
  - Frontier: fold-NN >= 0.70 leaves just **3/52 (5.8%)** external negatives un-abstained (M-CSA OOS
    4/26 in step), while in-scope retention is 20/35 â€” external negatives reject together with M-CSA OOS.
  - This is the off-M-CSA OOS-rejection property the cofactor channel lacked; the fold channel (not more
    fingerprint families) is the deployment-abstention lever.
- Caveats recorded in docs: off-M-CSA OOS *rejection* only, not off-M-CSA in-scope *recovery* (needs
  non-M-CSA positives with known mechanism + structure); curated negative panel, not a random sample;
  strict gate lowers in-scope recovery.
- Tests: `tests/test_external_offmcsa_fold_abstention_readout.py` (5) + a CLI parser-defaults case.
  Regenerated docs artifact-reference check -> missing 0.
- Validation: focused unittest (off-M-CSA readout + full test_cli + prior readouts) OK; compileall OK;
  registry `validate` OK (57 FP intact); docs reference check missing 0; `git diff --check` clean.
- Next exact action: close the other half of the deployment question â€” assemble a **non-M-CSA positive**
  surface (proteins with known mechanism class AND AlphaFold structure, off M-CSA) and measure off-M-CSA
  in-scope *recovery* via the same fold-NN-to-M-CSA-atlas retrieval, so recovery and abstention are both
  characterized off-distribution. Do not grow fingerprint families; the lever is the fold channel.

## Session run - June 9 router replay reproduces the bar (30/35 @ 8 FP); fold-NN gate gives NO Pareto improvement (precision/recall dial only); isolated registry pin, no main-repo registry mutation (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from commit `0079855d` (current-57
  cofactor+fold fusion preregistration). No main-repo registry/ontology/label/threshold/heldout/
  model-weight/fingerprint mutation. Main-repo registry validated intact at 57 fingerprints.
- Reproduced the trusted June 9 router surface **with per-row detail**: pinned the fingerprint registry
  to commit `d567ee0d` (June 9, 8-family state) inside an **isolated git worktree** and ran the current
  `build-cofactor-fusion-operating-point`. This exactly reproduces June 9 (calibration fused 30/35 @
  9/26 frozen, 30/35 @ 8/26 at the 0.44 dial), proving the 30/35â†’13/35 drift is the registry growth
  (54â†’57, v2 metal split) consulted by `predicted_geometry_robustness` â€” the graph/labels/geometry/
  channel artifacts are byte-identical to June 9. The worktree was removed afterward; the main repo's
  registry was never changed.
- Committed the per-row June 9 surface as
  `artifacts/v3_june9_router_pinned_rowdetail_operating_point_current702_20260628.json` (distinct
  artifact_id + `pin_provenance` recording the pin commit and isolation method).
- Added the readout builder + CLI:
  `src/catalytic_earth/june9_router_fold_fusion_readout.py` and
  `build-june9-router-fold-fusion-readout`. Artifact/report:
  `artifacts/v3_june9_router_fold_fusion_readout_current702_20260628.json` /
  `work/june9_router_fold_fusion_readout_current702_20260628.md`. Status
  `june9_router_fold_gate_no_pareto_improvement_precision_recall_tradeoff_only`:
  - June 9 exact recovery ceiling **30/35**; dial point **30/35 @ 8/26 OOS FP** is the top operating
    point.
  - Fold-NN OOS-rejection gate gives **no Pareto improvement** at top recovery (cannot beat 8/26 while
    holding 30/35). Residual OOS FPs are high-fold-similar (0.43â€“0.73); **7 of 8 are
    `metal_dependent_hydrolase`** (the drift family).
  - Fold gate is a precision/recall dial only: 28/35 @ 6/26, 23/35 @ 1/26, 18/35 @ 0/26.
- Correction to prior read recorded in docs: the fold channel's +3 recovery was specific to the drifted
  current-57 router; on the healthy June 9 router the cofactor channel already separates the OOS rows.
- Tests: `tests/test_june9_router_fold_fusion_readout.py` (4) + a CLI parser-defaults case. Regenerated
  docs artifact-reference check -> missing 0.
- Validation: focused unittest (June 9 readout + fusion + full test_cli) OK; compileall OK; registry
  `validate` OK (57 FP intact); docs reference check missing 0; `git diff --check` clean.
- Next exact action: pick the deployment operating point on the June 9 router (default: dial 30/35 @
  8/26; or a narrower near-zero-OOS-FP fold-dial regime) and spend the **single heldout-final read** to
  confirm it, since both the train/cal recovery and precision are now characterized. Do not grow
  fingerprint families to chase recovery; the current-57 drift is a taxonomy-version artifact, not a
  supply gap. Separately, consider whether the production router should be pinned to the June 9
  fingerprint resolution for the cofactor-precision surface.

## Session run - current-57 cofactor+fold fusion preregistered and fail-closed; fold gate +3 recovery at OOS-FP ceiling; router 26/35 ceiling blocks the bar; no registry apply (2026-06-28)

- Continued on branch `claude/continue-last-commit-ytktge` from the prior commit
  (`a177f460`, current-57 Fold/TM recompute readout). No registry, ontology, label, split, threshold,
  heldout, model-weight, or fingerprint-family mutation. Frozen current702 SHA unchanged.
- Added the preregistered current-57 cofactor + fold-NN fusion rule:
  `src/catalytic_earth/current57_cofactor_fold_fusion_preregistration.py` and
  `build-current57-cofactor-fold-fusion-preregistration`. Rule
  `retained := fused.top1_score >= cofactor_threshold AND fold_nn_alntmscore >= fold_threshold`,
  correctness under the legacy-v1 metal-umbrella projection, fold-NN as an OOS-rejection/abstention
  gate; both thresholds swept on calibration only (out-of-sample for the cofactor channel, never
  heldout).
- New artifact/report:
  `artifacts/v3_current57_cofactor_fold_fusion_preregistration_current702_20260628.json` and
  `work/current57_cofactor_fold_fusion_preregistration_current702_20260628.md`. Status
  `blocked_current57_cofactor_fold_fusion_not_deployable`:
  - Trusted June 9 done bar: recovery >= **30/35**, OOS FP <= **8/26** (0.44 dial).
  - Fold-NN marginal value: cofactor-only best under OOS-FP ceiling **20/35 @ FP 6**; fusion best
    **23/35 @ FP 8** (+3 recovery); max-precision regime **20/35 @ FP 5**.
  - Fail-closed because the binding constraint is recovery: current-57 compatible-recovery ceiling is
    **26/35** (exact 13/35), below the 30/35 bar; eligible calibration points **0**.
- Durable docs: `docs/project_state.md` and `docs/decision_log.md` updated with the fail-closed fusion
  and the recovery-ceiling diagnosis. Regenerated docs artifact-reference check -> missing 0.
- Tests: `tests/test_current57_cofactor_fold_fusion_preregistration.py` (4) and a CLI parser-defaults
  case in `tests/test_cli.py`.
- Validation: focused unittest (new fusion + readout + full test_cli) OK; compileall OK; registry
  `validate` OK (57 FP / 54 families / 702 labels); docs reference check missing 0; `git diff --check`
  clean.
- Next exact action: pin/replay the intended June 9 router/fingerprint surface so in-scope recovery
  clears the trusted bar, then re-apply this fold-NN OOS-rejection gate and promote a single
  calibration operating point to one heldout-final evaluation. The current-57 router recovery ceiling
  (26/35), not OOS FP, is now the documented blocker; growing fingerprint families will not move it.

## Session run - current-57 Fold/TM recomputed; row alignment resolved; fold-NN separates in-scope from OOS; no registry apply (2026-06-28)

- Continued from `origin/main` last commit `79dc2d3a` ("Block current57 cached fold fusion") on branch
  `claude/continue-last-commit-ytktge`. No registry, ontology, label, split, threshold, heldout,
  model-weight, or fingerprint-family mutation was made. Frozen current702 SHA unchanged.
- Installed `foldseek` (commit `718d42176d2f67d36a60866fedfb881f8d5a7ebf`, linux-avx2, user-authorized)
  and materialized the `v3_current57_fold_tm_recompute_input_manifest_current702_20260628` staging plan
  via symlinks (calibration cofactor queries + train in-scope fold atlas; heldout dirs excluded by
  construction). Ran the manifest's recorded `foldseek easy-search` command, producing
  `artifacts/v3_current57_fold_tm_recompute_current702_20260628_results/calibration_vs_current57_train_atlas.tsv`
  (4756 alignment rows, 61 calibration queries Ã— 132 train in-scope targets). Staged coordinate
  symlinks and the foldseek temp dir are reconstructible and git-ignored; the result TSV is committed.
- Added the row-aligned readout builder + CLI:
  `src/catalytic_earth/current57_fold_tm_recompute_readout.py` and
  `build-current57-fold-tm-recompute-readout`. New artifact/report:
  `artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json` and
  `work/current57_fold_tm_recompute_readout_current702_20260628.md`. Result
  `current57_fold_tm_recompute_readout_row_aligned`:
  - Recomputed fold-NN coverage **35/35** calibration in-scope and **26/26** OOS (cached overlap was
    **4/35** and **0/26**) â€” the cofactor/fold alignment blocker is resolved.
  - Fold-NN abstention separation: in-scope best-alntmscore median **0.743** vs OOS **0.566** (gap
    **0.177**); in-scope fold nearest neighbor recovers the true fingerprint in **28/35 (0.80)**.
  - Heldout-excluded, calibration-vs-train only; no threshold selected, no supervised model trained,
    no heldout row read or scored.
- Durable docs updated: `docs/project_state.md` (new headline) and `docs/decision_log.md` (new dated
  entry) record the resolved alignment and the fold-NN separation. Regenerated
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260628.json` -> missing 0.
- Tests: `tests/test_current57_fold_tm_recompute_readout.py` (5 tests) and a CLI parser-defaults case
  in `tests/test_cli.py`.
- Validation:
  - `PYTHONPATH=src python -m unittest tests.test_current57_fold_tm_recompute_readout tests.test_cli` -> OK (241 tests).
  - `PYTHONPATH=src python -m compileall -q src tests` -> OK.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` -> 57 fingerprints, 54 ontology families, 702 labels.
  - Docs artifact-reference check -> missing 0.
  - `git diff --check` clean.
- Next exact action: preregister a current-57 cofactor+fold fusion rule that uses this now-aligned fold
  surface as the OOS-rejection/abstention channel, and test on train/cal whether it clears the trusted
  June 9 in-scope-recovery / OOS-FP bar before any heldout read. The current-57 cofactor precision
  contract (OOS FP 26/26) still governs deployment; this readout alone does not authorize fusion.

## Session run - current-57 cofactor/fold alignment blocked; recompute manifest ready; no registry apply (2026-06-28, Codex automation)

- Started at `2026-06-28T03:32:44Z` from current `origin/main`
  `b94d0e25e01cb4cc1680a15f2b9fc6992ff77a6b`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry, ontology,
  label, split, threshold, heldout, model-weight, or fingerprint-family mutation was made. Elapsed
  runtime at closeout was **23.1 min** (31.9 min remaining of the 55 min budget).
- Added the heldout-excluded current-57 cofactor/fold row-alignment audit:
  `src/catalytic_earth/current57_cofactor_fold_alignment_audit.py` and
  `build-current57-cofactor-fold-alignment-audit`. It checks whether the current-57 cofactor
  train/cal precision rows can be joined to the cached fold/TM row-level contracts before any cached
  atlas-engine fusion claim.
- New alignment artifact/report:
  `artifacts/v3_current57_cofactor_fold_alignment_audit_current702_20260628.json` and
  `work/current57_cofactor_fold_alignment_audit_current702_20260628.md`. Result:
  `blocked_cached_fold_surface_not_row_aligned_with_current57_cofactor_surface`. Calibration in-scope
  overlap is only **4/35** and calibration OOS overlap is **0/26** against the required 0.9 overlap
  fractions; the overlap-only fixed fold gate is non-interpretable because no current-57 OOS row has a
  cached fold score.
- Integrated the alignment blocker into
  `src/catalytic_earth/predicted_geometry_atlas_engine_preregistration.py` and regenerated
  `artifacts/v3_predicted_geometry_atlas_engine_preregistration_current702_20260628.json` /
  `work/predicted_geometry_atlas_engine_preregistration_current702_20260628.md`. Status is now
  `preregistered_cached_surface_blocked_current57_precision_contract_fold_alignment_new_foldseek_backend_blocked`;
  cached atlas-engine fusion is explicitly not runnable.
- Added a no-score current-57 Fold/TM recompute input manifest and CLI:
  `src/catalytic_earth/current57_fold_tm_recompute_manifest.py` and
  `build-current57-fold-tm-recompute-manifest`. New artifact/report:
  `artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json` and
  `work/current57_fold_tm_recompute_input_manifest_current702_20260628.md`. It maps the exact current-57
  calibration queries (**61/61**) and train in-scope fold targets (**133/133**) to train/cal-safe
  staged AlphaFold CIFs and records the future `foldseek easy-search` command. It did not materialize
  staging directories and did not compute new Fold/TM scores.
- Durable docs updated: `docs/project_state.md` and `docs/decision_log.md` now record the row-alignment
  blocker and the concrete recompute manifest. `docs/MAP.md` was not changed because the compass is
  unchanged: breadth remains stopped and the predicted-geometry recovery line is the priority.
- Validation passed:
  - `PYTHONPATH=src pytest -q tests/test_current57_fold_tm_recompute_manifest.py tests/test_current57_cofactor_fold_alignment_audit.py tests/test_predicted_geometry_atlas_engine_preregistration.py tests/test_cli.py -k 'current57_fold_tm_recompute or current57_cofactor_fold_alignment or predicted_geometry_atlas_engine_preregistration or current57_cofactor_precision_contract'`
    -> 13 passed, 232 deselected.
  - Earlier focused recovery/preregistration suite after the alignment audit:
    `PYTHONPATH=src pytest -q tests/test_current57_cofactor_fold_alignment_audit.py tests/test_cofactor_precision_contract.py tests/test_predicted_geometry_atlas_engine_preregistration.py tests/test_cofactor_fusion_operating_point.py tests/test_predicted_geometry_recovery.py tests/test_cofactor_presence_calibration.py tests/test_cofactor_channel_probe.py tests/test_geometry_retrieval.py tests/test_cli.py -k 'current57_cofactor_fold_alignment or cofactor_precision_contract or predicted_geometry_atlas_engine_preregistration or cofactor_fusion_operating_point or predicted_geometry_recovery or cofactor_presence_calibration or cofactor_channel_probe or geometry_retrieval'`
    -> 94 passed, 232 deselected, 2 subtests.
  - `PYTHONPATH=src python -m compileall -q src tests` passed.
  - Final full `PYTHONPATH=src pytest -q` -> 2536 passed, 1 warning, 244 subtests in 182.63s.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` -> validated 12 sources, 57 fingerprints,
    54 ontology families, 702 curated labels.
  - `PYTHONPATH=src python -m catalytic_earth.cli build-current-docs-artifact-reference-check --out artifacts/v3_current_docs_artifact_reference_check_current702_20260628.json --report work/current_docs_artifact_reference_check_current702_20260628.md`
    -> missing 0.
  - JSON/JSONL parse passed: 10725 JSON files and 8338 JSONL records across 27 JSONL files.
  - `git diff --check` passed.
  - Frozen current702 SHA after work:
    `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Next exact action: install/expose `foldseek`, materialize the
  `v3_current57_fold_tm_recompute_input_manifest_current702_20260628` staging plan, run its recorded
  calibration-vs-train easy-search command, then build a current-57 fold/TM score readout before any
  cached atlas-engine fusion or heldout read. Alternative: pin/replay the intended June 9 router and
  fold row surface.

## Session run - current-57 cofactor precision contract fail-closed; atlas prereg updated; no registry apply (2026-06-28, Codex automation)

- Started at `2026-06-28T02:31:07Z` from current `origin/main`
  `60b17cdf2635843f3fc62beb71ad5e7ed26915e9`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry, ontology,
  label, threshold, heldout split, or model-weight mutation was made. Elapsed runtime at closeout was
  **20.4 min** (34.6 min remaining of the 55 min budget).
- Added the heldout-excluded current-57 cofactor precision contract builder and CLI:
  `src/catalytic_earth/cofactor_precision_contract.py` and
  `build-current57-cofactor-precision-contract`. It reads the current-57 train/cal cofactor
  diagnostic plus the trusted June 9 precision artifact, applies only the documented legacy-v1
  metal-hydrolase compatibility projection, and fail-closes if no threshold matches the trusted
  recovery/OOS bar.
- New contract artifact/report:
  `artifacts/v3_current57_cofactor_precision_contract_current702_20260628.json` and
  `work/current57_cofactor_precision_contract_current702_20260628.md`. Result:
  `blocked_current57_cofactor_precision_contract_not_deployable`. Exact current-57 calibration fused
  readout remains **13/35, 26/26 OOS FP**; v1 metal-compatible recovery rises to **26/35**, proving a
  large taxonomy-version component, but OOS remains **26/26**. The best point under the trusted June 9
  OOS FP ceiling is threshold **0.733** with only **20/35** recovery and **8/26** OOS FP, below the
  preregistered **30/35** recovery bar.
- Integrated that contract into
  `src/catalytic_earth/predicted_geometry_atlas_engine_preregistration.py` and the
  `build-predicted-geometry-atlas-engine-preregistration` CLI. Regenerated
  `artifacts/v3_predicted_geometry_atlas_engine_preregistration_current702_20260628.json` and
  `work/predicted_geometry_atlas_engine_preregistration_current702_20260628.md`; status is now
  `preregistered_cached_surface_blocked_current57_precision_contract_new_foldseek_backend_blocked`.
  Cached atlas-engine fusion remains blocked even though existing scored fold/TM surfaces are reusable.
- Durable docs updated: `docs/project_state.md` and `docs/decision_log.md` now record the fail-closed
  current-57 contract and the updated preregistration status. `docs/MAP.md` was not changed because
  the compass is unchanged: predicted-geometry recovery is still the priority and broad family growth
  remains stopped unless explicitly reauthorized.
- Validation passed:
  - `PYTHONPATH=src pytest -q tests/test_cofactor_precision_contract.py tests/test_predicted_geometry_atlas_engine_preregistration.py tests/test_cofactor_fusion_operating_point.py tests/test_cli.py -k 'cofactor_precision_contract or predicted_geometry_atlas_engine_preregistration or current57_cofactor_precision_contract'`
    -> 8 passed, 242 deselected.
  - Focused recovery/precision suite:
    `PYTHONPATH=src pytest -q tests/test_cofactor_precision_contract.py tests/test_cofactor_fusion_operating_point.py tests/test_predicted_geometry_atlas_engine_preregistration.py tests/test_predicted_geometry_recovery.py tests/test_cofactor_presence_calibration.py tests/test_cofactor_channel_probe.py tests/test_geometry_retrieval.py`
    -> 89 passed, 2 subtests.
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` -> validated 12 sources, 57 fingerprints,
    54 ontology families, 702 curated labels.
  - Full `PYTHONPATH=src pytest -q` was run twice after the main changes; final run -> 2528 passed,
    1 warning, 244 subtests in 183.09s.
  - `PYTHONPATH=src python -m compileall -q src tests` passed.
  - `PYTHONPATH=src python -m catalytic_earth.cli build-current-docs-artifact-reference-check --out artifacts/v3_current_docs_artifact_reference_check_current702_20260628.json --report work/current_docs_artifact_reference_check_current702_20260628.md`
    -> missing 0.
  - JSON/JSONL parse passed: 10723 JSON files and 8336 JSONL records across 27 JSONL files.
  - `git diff --check` passed.
  - Frozen current702 SHA after work:
    `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Next exact action: do not run atlas-engine fusion or spend heldout on the current-57 cofactor
  surface. Either pin/replay the intended June 9 router/fingerprint surface for cofactor precision,
  or build a new preregistered current-57 precision channel/fusion rule that clears a train/cal
  recovery/OOS done bar. Install/expose `foldseek` before any new Foldseek/TM scoring.

## Session run - predicted-geometry atlas prereg blocked by current-57 router drift; no registry apply (2026-06-28, Codex automation)

- Started at `2026-06-28T01:30:17Z` from current `origin/main`
  `ae6b313fed4d0c2f7e8952520c5251676a626b21`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry, ontology,
  label, threshold, or model-weight mutation was made. Elapsed runtime at closeout was **18.7 min**
  (36.3 min remaining of the 55 min budget).
- Added a full-env/preregistration builder and CLI:
  `src/catalytic_earth/predicted_geometry_atlas_engine_preregistration.py` and
  `build-predicted-geometry-atlas-engine-preregistration`. It hashes the cofactor/fold source
  artifacts, records local backend status, and fixes the heldout-excluded train/cal atlas-engine
  contract before any fusion/heldout read.
- Environment result: numpy, torch, sklearn, pandas, mmseqs, and diamond are present; `esm`, BioPython,
  biotite, jackhmmer/hmmscan, and `foldseek` are missing. Existing scored fold/TM surfaces are
  reusable; new Foldseek/TM scoring is blocked until `foldseek` is installed/exposed.
- Preregistration artifact:
  `artifacts/v3_predicted_geometry_atlas_engine_preregistration_current702_20260628.json`; report:
  `work/predicted_geometry_atlas_engine_preregistration_current702_20260628.md`. Status:
  `preregistered_cached_surface_blocked_current57_router_drift_new_foldseek_backend_blocked`.
  Guardrails: no heldout rows scored/read, no production threshold change, no model refit, no
  registry/ontology/fingerprint-family growth, no EC/name/prose/fingerprint predictive features.
- Added row-level train/cal diagnostics to `cofactor_fusion_operating_point.py` so future precision
  artifacts can expose per-row in-scope/OOS flags alongside aggregate operating points. Regression
  coverage added in `tests/test_cofactor_fusion_operating_point.py`.
- Ran the cofactor-fusion operating-point command against the current repo after the 57-family scaling
  era and preserved the result under a new diagnostic path:
  `artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260628_current57_rerun.json`;
  report:
  `work/cofactor_fusion_operating_point_train_cal_oos_current702_20260628_current57_rerun.md`. The
  trusted June 9 artifact path was restored unchanged. Current-57 calibration fused readout is
  **13/35 in-scope, 26/26 OOS FP**, versus the trusted June 9 contract's **30/35, 9/26**. Treat this
  as a router/fingerprint-surface drift diagnostic, not a replacement threshold candidate.
- Durable docs updated: `docs/project_state.md` and `docs/decision_log.md` now record the blocker.
  Next gate: before atlas-engine fusion or any heldout read, either freeze/replay the intended June 9
  router/fingerprint surface for cofactor precision, or preregister a new current-57 train/cal
  cofactor precision rule. Install/expose `foldseek` before any new Foldseek/TM scoring.
- Validation passed:
  - `PYTHONPATH=src python -m catalytic_earth.cli validate` -> validated 12 sources, 57 fingerprints,
    54 ontology families, 702 curated labels.
  - Focused recovery/precision tests:
    `PYTHONPATH=src pytest -q tests/test_cofactor_fusion_operating_point.py tests/test_predicted_geometry_atlas_engine_preregistration.py tests/test_predicted_geometry_recovery.py tests/test_cofactor_presence_calibration.py tests/test_cofactor_channel_probe.py tests/test_geometry_retrieval.py`
    -> 86 passed, 2 subtests.
  - Full `PYTHONPATH=src pytest -q` -> 2524 passed, 1 warning, 244 subtests in 183.44s.
  - `PYTHONPATH=src python -m compileall -q src tests` passed.
  - `PYTHONPATH=src python -m catalytic_earth.cli build-current-docs-artifact-reference-check --out artifacts/v3_current_docs_artifact_reference_check_current702_20260628.json --report work/current_docs_artifact_reference_check_current702_20260628.md`
    -> missing 0.
  - JSON/JSONL parse passed: 4581 JSON files and 715 progress JSONL records.
  - `git diff --check` passed.
  - Frozen current702 SHA after work:
    `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Next exact action: resolve the current-router precision surface before fusion. Prefer a small
  train/cal-only experiment that either pins the June 9 eight-family/v1 router surface as the intended
  cofactor precision contract or preregisters a new current-57 cofactor threshold/selection rule.
  Do not spend heldout or claim deployment closure from the old 0.44 cofactor threshold while this
  drift diagnostic is unresolved.

## Session run - source-transfer chain refreshed; all-vs-all duplicate screen clean; no registry apply (2026-06-17, Codex automation run0310)

- Started at `2026-06-17T03:09:49Z` from current `origin/main`
  `8359eb6e5ef26a454494e6edb12195084b22ef56`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry apply or
  label write was attempted.
- Baseline safety was green before work: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed, and the baseline focused critical pytest suite passed **525 passed, 14 subtests**.
  Final validation passed; final focused critical/source-transfer/biotin/NAD pytest passed
  **536 passed, 14 subtests**; final full `PYTHONPATH=src pytest -q` passed **2404 passed,
  1 warning, 244 subtests**. Final compileall, JSON/JSONL parse, hard-limit scan, frozen SHA
  check, docs-reference check, and `git diff --check` are rerun after this closeout edit.
- Coverage remained unchanged at **8728** combined labels = **702** frozen + **8026** expansion.
  Pre-lane audits
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run0310_pre_lane.json` and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0310_pre_lane.json` show
  holes **0**, floor deficit **0**, over-cap only `metal_dependent_hydrolase`, and novelty replay
  **7565** admit / **414** throttle / **47** reject.
- Refreshed scale-wall planning before lane work:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0310_pre_lane.json` still
  has **0** ready existing lanes >=150 and top projected clean admits **77**;
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run0310_pre_lane.json` still shows
  four handle-blocked families and **741** reachable positive-bronze uplift if handles are
  repaired; `artifacts/v3_breadth_feasibility_scout_current702_20260616_run0310_pre_lane.json`
  still projects **9673** reviewed-Swiss-Prot clean positives, gap **327** to 10k; and
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run0310.json` still recommends
  external source-transfer/source-handle strategy over M-CSA-only tranche growth.
- Bounded reviewed biotin broad-handle preview
  `artifacts/v3_biotin_dependent_carboxylase_reviewed_broad_handle_preview_current702_20260616_run0310.json`
  fetched **139** rows, found **47** mechanism-corroborated bronze rows and **41**
  novelty-admitted preview rows, projecting **8728 -> 8769** if merged. Its row guardrail audit
  `artifacts/v3_biotin_dependent_carboxylase_reviewed_broad_handle_preview_row_guardrail_audit_current702_20260616_run0310.json`
  passed with **41** rows and **0** problems. The family floor was already reached and the preview
  was below autonomous high-yield criteria, so no apply was attempted. The offset-250 follow-up
  `artifacts/v3_biotin_dependent_carboxylase_reviewed_broad_handle_preview_offset250_current702_20260616_run0310.json`
  fetched **0** rows, confirming this reviewed window is exhausted for this handle.
- Rebuilt the full current external source-transfer review chain from transfer/query/candidate
  manifests through evidence queues, active-site sourcing, reaction context, representation
  backend plan/sample, sequence screens, import readiness, blocker matrix, pilot evidence packets,
  pilot terminal decisions, normalized decisions, and human-expert queue. The refreshed import
  readiness audit
  `artifacts/v3_external_source_import_readiness_audit_current702_20260616_run0310.json` holds all
  **47** rows review-only with **0** import-ready/countable rows: **21** blocked by active-site
  sourcing, **14** by heuristic control, **9** by representation control, **2** by sequence
  holdout, and **1** by review/factory gate.
- Transfer blocker matrix
  `artifacts/v3_external_source_transfer_blocker_matrix_current702_20260616_run0310.json` remains
  fail-closed with **47** review-only rows and **0** countable candidates. Prioritized next-action
  counts are **15** `select_and_run_real_representation_backend`, **12**
  `curate_primary_literature_or_pdb_active_site_sources`, **9**
  `find_primary_active_site_or_residue_role_source`, **9**
  `compute_or_attach_real_representation_control`, and **2**
  `keep_sequence_holdout_out_of_import_batch`.
- Pilot replay artifacts remain non-importing:
  `artifacts/v3_external_source_pilot_success_criteria_current702_20260616_run0310.json` has
  **12** candidates with **0** import-ready/countable rows and blockers for active-site source
  unresolved (**6**), broader duplicate screening unresolved (**12**), full label-factory gate not
  passed (**12**), representation control unresolved (**12**), and review decision not terminal
  (**12**). Terminal decisions
  `artifacts/v3_external_source_pilot_terminal_decisions_current702_20260616_run0310.json` are
  **6** `deferred_requires_human_expert` and **6** `rejected_active_site_evidence_missing`; the
  normalized expert queue
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_current702_20260616_run0310.json`
  carries **6** queued rows and **0** import-ready/countable rows.
- The current bounded sequence reference screen
  `artifacts/v3_external_source_sequence_reference_screen_audit_current702_20260616_run0310.json`
  remains fail-closed because **30** candidate top-hit alignments are incomplete, **15** aligned
  with no alert, and **2** preexisting sequence holdouts were retained. To advance the broader
  duplicate gate, added run0310 all-vs-all external sequence screen
  `artifacts/v3_external_source_all_vs_all_sequence_search_current702_20260616_run0310.json` using
  real `mmseqs2_easy_search`: **47/47** rows had no external near-duplicate signal, **0** exact or
  near-duplicate rows, max external-vs-external identity **0.874**, and **0**
  import-ready/countable rows. Its audit
  `artifacts/v3_external_source_all_vs_all_sequence_search_audit_current702_20260616_run0310.json`
  passed clean. This removes only the external-candidate all-vs-all duplicate-screen blocker;
  UniRef-wide duplicate screening remains not run.
- The terminal review/factory gap replay could not be rebuilt for run0310 because the CLI exposes
  `build-external-source-pilot-mechanism-repair-lanes` and
  `build-external-source-pilot-review-resolution-gap-audit`, but no current CLI producer for the
  required `needs_review_resolution` artifact. No synthetic review-resolution artifact was created.
- Storage safety was refreshed for run0310:
  `artifacts/v3_artifact_storage_inventory_current702_20260616_run0310.json`,
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run0310.json`,
  `artifacts/v3_artifact_producer_consumer_manifest_current702_20260616_run0310.json`,
  `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run0310.json`,
  `artifacts/v3_artifact_migration_execution_current702_20260616_run0310.json`, and
  `artifacts/v3_artifact_admission_guard_current702_20260616_run0310.json`. No
  `data/registries` or `artifacts` file exceeded **90 MB**, migration dry-run validation passed
  with **0** rows and **0** blockers, and **0** deletions/removals were authorized. Repo policy
  remains fail-closed on **4** large unclassified artifacts at the **50 MB** policy threshold.
- A final bounded NAD/glycosyltransferase live scout was attempted with `--max-records-per-lane 80`
  and `--fetch-timeout-seconds 20`, but it did not complete before closeout and was interrupted
  while waiting on a slow UniProt entry fetch. It produced no completed preview artifact, did not
  write label files, and did not modify registries.
- Next exact action: do not import the biotin preview, the six terminal-deferred source-transfer
  rows, or any run0310 review-only transfer row. Either add/expose a current
  `needs_review_resolution` producer so mechanism-repair lanes and review-resolution gap replay
  can run on run0310, or resolve the remaining import blockers directly: primary active-site
  sources for **21** rows, real representation backend/control for **15** rows, UniRef-wide
  duplicate screen, terminal review decisions, and full label-factory/novelty/governor/
  row-guardrail gates.

## Session run - terminal replay deferred; source-handle scale wall refreshed; no registry apply (2026-06-17, Codex automation run0210)

- Started at `2026-06-17T02:08:10Z` from current `origin/main`
  `a11ee18680aaa74c1959798434dcb5b4a29dcb30`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry apply or
  label write was attempted.
- Baseline safety was green before work: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed, and the baseline focused critical pytest suite passed **448 passed, 160 subtests**.
  Final affected/source-transfer pytest passed **428 passed, 160 subtests**; final full
  `PYTHONPATH=src pytest -q` passed **2404 passed, 1 warning, 244 subtests**. Final compileall,
  docs-reference check (**missing: 0**), hard-limit scan, JSON/JSONL parse, frozen SHA check, and
  `git diff --check` passed or are rerun after this closeout edit.
- Final coverage remained unchanged at **8728** combined labels = **702** frozen + **8026**
  expansion. Final no-apply audits
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run0210_final_noapply.json` and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0210_final_noapply.json`
  show holes **0**, floor deficit **0**, over-cap only `metal_dependent_hydrolase`, and novelty
  replay **7565** admit / **414** throttle / **47** reject.
- Added `build-external-source-pilot-terminal-review-factory-replay-audit`, wired its CLI command,
  and covered it in transfer/CLI tests. The audit consumes recorded terminal decisions for the
  run0009 five-row replay queue but is deliberately non-authorizing: it never creates terminal
  acceptances, import-ready rows, countable rows, or labels.
- Terminal replay artifact
  `artifacts/v3_external_source_pilot_terminal_review_factory_replay_audit_current702_20260616_run0210.json`
  consumed **5/5** recorded terminal decisions for Q6NSJ0, C9JRZ8, O14756, P06746, and Q8N0X4.
  All **5** are `deferred_requires_human_expert`, so terminal accepted **0**, factory pass **0**,
  import-ready **0**, and countable label candidates **0**. Zero-import validation
  `artifacts/v3_external_source_pilot_terminal_review_factory_replay_audit_zero_import_current702_20260616_run0210.json`
  passed **1/1 valid**.
- Added bounded fetch support to `scripts/source_nad_glycosyltransferase_families.py` and its
  sourcing writer so future UniProt/Rhea calls can time out into preview `fetch_failures` instead
  of hanging an automation run. Regression coverage in
  `tests/test_nad_glycosyltransferase_subfamily_sourcing.py` remains green.
- Refreshed source-wall planning:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0210_post_terminal_replay.json`
  still has **0** ready existing lanes >=150 and top projected clean admits **77**;
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run0210_post_terminal_replay.json`
  shows four handle-blocked families and **741** bounded reachable-bronze headroom if handles are
  repaired; `artifacts/v3_breadth_feasibility_scout_current702_20260616_run0210_post_terminal_replay.json`
  still projects **9673** reviewed-Swiss-Prot clean positives, gap **327** to 10k; and
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run0210.json` still recommends
  external source-transfer/source-handle strategy over M-CSA-only tranche growth.
- Current-state no-apply probes:
  `artifacts/v3_glycosyltransferase_handle_cap_probe_current702_20260616_run0210.json` fetched
  **15** rows, found **0** mechanism-corroborated/admitted labels, and passed row guardrails with
  **0** rows; `artifacts/v3_nad_p_dehydrogenase_handle_cap_probe_current702_20260616_run0210.json`
  fetched **40** rows, found **21** mechanism-corroborated labels, but all **17**
  novelty-admitted-before-cap rows were held at the **150** family cap; row guardrails passed with
  **0** rows; `artifacts/v3_biotin_dependent_carboxylase_floor_handle_probe_current702_20260616_run0210.json`
  fetched **14** rows and found **8** novelty-admitted labels, but the family was already at floor
  and this subthreshold fragment was not an autonomous apply candidate; row guardrails passed with
  **8** rows and **0** problems.
- Additional capped-lane probes:
  `artifacts/v3_terpene_cyclase_synthase_cap_probe_current702_20260616_run0210.json` fetched
  **49** rows and admitted **0**; `artifacts/v3_protein_kinase_cap_probe_current702_20260616_run0210.json`
  fetched **10** rows and admitted **0**; and
  `artifacts/v3_short_chain_dehydrogenase_reductase_cap_probe_current702_20260616_run0210.json`
  fetched **26** rows and admitted **0**. All companion row-guardrail audits passed with **0**
  problem rows.
- Early closeout reason: after the terminal replay and five current-state source probes, the
  remaining safe scaling choices were concretely blocked by no holes/floor deficits, no ready
  lane projected at >=150 clean admits, terminal decisions deferred to human/expert review, and
  current probes that were capped, already-at-floor, or zero-yield. Applying tiny fragments would
  violate the current scale-wall policy.
- Next exact action: do not import the five terminal-deferred rows, the biotin fragment, or any
  cap-probe rows. The next productive run should either resolve the human/expert terminal review
  blocker for Q6NSJ0/C9JRZ8/O14756/P06746/Q8N0X4, or formalize a higher-yield external
  source-transfer/source-handle lane beyond reviewed Swiss-Prot with duplicate screening,
  active-site/source resolution, full label-factory, novelty, governor, and row-guardrail gates.

## Session run - P55263 PfkB import-safety keep-held; no registry apply (2026-06-17, Codex automation run0009)

- Started at `2026-06-17T01:07:32Z` from current `origin/main`
  `e9e80382644583cfb885806af4e0479509cd8955`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry apply or label
  write was attempted.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed, and
  baseline focused critical pytest passed **728 passed, 174 subtests**. Focused transfer/CLI/
  review-only/leakage/registry/novelty/coverage pytest passed **616 passed, 174 subtests**.
  Focused transfer/CLI/review-only pytest passed **380 passed, 160 subtests**. Final full
  `PYTHONPATH=src pytest -q` passed **2402 passed, 1 warning, 244 subtests**. Final compileall,
  docs-reference check (**missing: 0**), hard-limit scan, frozen SHA check, and `git diff --check`
  passed; final JSON/JSONL parse is rerun after this handoff edit.
- Coverage remained unchanged at **8728** combined labels = **702** frozen + **8026** expansion,
  with no holes, floor deficit **0**, novelty replay **7565** admit / **414** throttle / **47**
  reject, **0** ready existing lanes >=150, top projected clean admits **77**, and reviewed
  Swiss-Prot clean-positive projection **9673** with gap **327** to 10k.
- Added a review-only P55263 PfkB keep-held path:
  `build-external-source-pilot-pfkb-source-free-control-decision`,
  `build-external-source-pilot-pfkb-import-safety-adjudication`, and gap-audit consumption of
  `--pfkb-import-safety-adjudication`. Regression coverage verifies the replay removes only the
  stale `family_import_safety_adjudication_missing` blocker and does not create terminal acceptance,
  countable labels, or import-ready rows.
- New PfkB artifacts:
  `artifacts/v3_external_source_pilot_p55263_pfkb_source_free_control_decision_current702_20260616_run0009.json`
  records `source_free_pfkb_control_not_implemented_keep_held` with `predictive_evidence: []`;
  `artifacts/v3_external_source_pilot_p55263_pfkb_import_safety_adjudication_current702_20260616_run0009.json`
  records `pfkb_source_free_control_explicit_keep_held`; and
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_p55263_pfkb_keepheld_replay_current702_20260616_run0009.json`
  now has **5** `review_decision_and_factory_gate_blocked_after_control_repair`, **1**
  `family_control_unresolved_after_adjudication`, and **1**
  `manual_source_mechanism_keep_held_after_import_safety`. Import-ready/countable rows remain **0**.
- Zero-import validation
  `artifacts/v3_external_source_pilot_pfkb_keepheld_review_only_zero_import_audit_current702_20260616_run0009.json`
  passed **3/3 valid**. This required adding explicit zero-import metadata flags to the new
  review-only artifacts and gap-audit metadata.
- Added the terminal-review/factory replay queue
  `artifacts/v3_external_source_pilot_terminal_review_factory_replay_queue_current702_20260616_run0009.json`
  for the **5** control-repaired rows (Q6NSJ0, C9JRZ8, O14756, P06746, Q8N0X4). It records no
  terminal decisions, keeps full factory status `not_run`, and has **0** import-ready/countable
  rows. Its zero-import audit
  `artifacts/v3_external_source_pilot_terminal_review_factory_replay_queue_zero_import_audit_current702_20260616_run0009.json`
  passed **1/1 valid**.
- Bounded source-tier-2 PfkB source-handle scout
  `artifacts/v3_pfkb_ribokinase_family_tier2_source_handle_scout_current702_20260616_run0009.json`
  fetched **80** unreviewed site-annotated rows and found **7** mechanism-corroborated bronze labels
  but only **2** novelty-admitted rows, projecting **8728 -> 8730** if merged. The PfkB family was
  already above floor (**128 -> 130** projected), so this is strategy evidence only and not an
  autonomous apply candidate. Row guardrail audit
  `artifacts/v3_pfkb_ribokinase_family_tier2_source_handle_scout_row_guardrail_audit_current702_20260616_run0009.json`
  passed with **2** rows and **0** problems.
- Bounded source-tier-2 biotin-dependent carboxylase scout
  `artifacts/v3_biotin_dependent_carboxylase_tier2_source_handle_scout_current702_20260616_run0009.json`
  fetched **80** unreviewed site-annotated rows and found **16** mechanism-corroborated bronze
  labels and **9** novelty-admitted rows, projecting **8728 -> 8737** if merged. The family floor
  was already reached (**100 -> 109** projected), so this is also strategy evidence only and not an
  autonomous apply candidate. Row guardrail audit
  `artifacts/v3_biotin_dependent_carboxylase_tier2_source_handle_scout_row_guardrail_audit_current702_20260616_run0009.json`
  passed with **9** rows and **0** problems.
- Bounded source-tier-2 metal-independent phosphodiesterase scout
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_source_handle_scout_current702_20260616_run0009.json`
  fetched **315** unreviewed rows, found **0** mechanism-corroborated target bronze labels, held
  **66** off-target rows, and projected **8728 -> 8728** if merged. Row guardrail audit
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_source_handle_scout_row_guardrail_audit_current702_20260616_run0009.json`
  passed with **0** rows and **0** problems. This supports the current scale-wall finding that
  low-yield tier-2 windows are not enough without a higher-yield source-transfer/source-handle
  unlock.
- Storage hygiene remains fail-closed: run0009 storage artifacts record **46** large-unclassified/
  admission blockers, **116** producer-consumer/readiness/execution rows, **0** migration-ready
  files, **0** deletion-authorized files, and **0** removal-allowed files. Migration dry-run
  validation passed with **116** rows and **0** blockers.
- New planning artifacts:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run0009_pre_lane.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run0009_post_noapply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0009_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0009_post_noapply.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0009_pre_lane.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run0009_pre_lane.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run0009_pre_lane.json`, and
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run0009.json`.
- Next exact action: do not import P55263 or tier-2 PfkB scout rows. Consume the five-row
  terminal-review/factory replay queue with explicit review decisions and full factory/novelty/
  governor/row-guardrail gates, implement a real tested source-free PfkB/ribokinase control, or
  open a higher-yield source-transfer/source-handle lane that passes duplicate, active-site,
  factory, novelty, governor, row-guardrail, and lane-authorization gates.

## Session run - Q6NSJ0 boundary repaired; P55263 design packeted; no registry apply (2026-06-17, Codex automation)

- Started at `2026-06-17T00:08:09Z` from current `origin/main`
  `69f1785647469dd6eac671bbb72aef2b0a3dd59d`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry apply or
  label write was attempted.
- Baseline safety was green before work: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed, and the baseline focused critical suite passed **786 passed, 174 subtests**. Final
  focused critical suite passed **788 passed, 174 subtests**; final transfer/CLI module suite
  passed **371 passed, 160 subtests**; final full `PYTHONPATH=src pytest -q` passed
  **2396 passed, 1 warning, 244 subtests**. Final compileall, docs-reference check
  (**0 missing / 2147 checked / 14 ignored**), JSON/JSONL parse (**22** run0008 JSON artifacts and
  **688** progress records), hard-limit scan, frozen SHA check, and `git diff --check` passed.
- Coverage remains unchanged at **8728** combined labels = **702** frozen + **8026** expansion, with
  no holes, floor deficit **0**, novelty replay **7565** admit / **414** throttle / **47** reject,
  **0** ready existing lanes >=150, top projected clean admits **77**, and reviewed-Swiss-Prot
  clean-positive projection **9673** with gap **327** to 10k. This run continued source-transfer
  gate repair instead of padding low-yield reviewed-Swiss-Prot lanes.
- Repaired the Q6NSJ0 glycoside boundary-control interpretation in code. Raw role-hint matches are
  now retained separately from evidence-bearing metal/ligand/hydroxide role matches with non-empty
  matched residue codes. Regression coverage in `tests/test_transfer_scope.py` verifies a raw
  role-hint match with empty `matched_codes` does not block Q6NSJ0-style glycoside readiness.
- Regenerated Q6NSJ0 boundary control:
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_q6nsj0_replacement_current702_20260616_run0008.json`.
  It now has **1** `review_only_glycoside_hydrolase_boundary_ready` row, source-traced acidic dyad
  **463/520**, absent metal-ligand context, raw role-hint count **1**, and evidence-bearing metal
  role-hint count **0**. It remains review-only, non-countable, and non-import-authorizing.
- Regenerated Q6NSJ0 glycoside import-safety:
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_q6nsj0_replacement_current702_20260616_run0008.json`.
  Q6NSJ0 is now `glycoside_boundary_representation_conflict_repaired`, but still blocked by
  explicit review decision, full label-factory gate, inverse/out-of-scope checks, and source-free
  predictive gate work.
- Merged Q6NSJ0 with historical P33025 glycoside adjudication:
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_merged_q6nsj0_p33025_current702_20260616_run0008.json`.
  The merged replay has **1** repaired and **1** unrepaired glycoside row; P33025 remains
  `glycoside_boundary_representation_conflict_not_repaired`. Import-ready/countable rows remain
  **0**.
- Replayed the source-transfer review gap:
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_p55263_with_glyco_repair_replay_current702_20260616_run0008.json`.
  It holds **7** rows with **0** import-ready and **0** countable candidates: **5**
  `review_decision_and_factory_gate_blocked_after_control_repair`, **1**
  `family_control_unresolved_after_adjudication`, and **1**
  `manual_source_mechanism_control_design_review_only`.
  The review-only safety audit
  `artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_q6nsj0_p55263_with_glyco_repair_replay_current702_20260616_run0008.json`
  passed **safe=True**, **0** unsafe artifacts, and **0** new countable labels.
- Added `build-external-source-pilot-manual-source-mechanism-control-design` and transfer/CLI tests.
  The command is deliberately non-authorizing: it can name a candidate control route for manual
  source-mechanism rows, but keeps EC, names, UniProt prose, source handles, and Rhea text in
  excluded/review context and leaves `predictive_evidence: []`.
- Extended `build-external-source-pilot-review-resolution-gap-audit` with an optional
  `--manual-source-mechanism-control-design` input so non-authorizing manual designs are preserved
  in the gap replay as blocker context. This changes P55263's gap status to
  `manual_source_mechanism_control_design_review_only`; it does not make the row countable or
  import-ready.
- Built the P55263 design packet:
  `artifacts/v3_external_source_pilot_p55263_mechanism_control_design_current702_20260616_run0008.json`,
  plus safety audit
  `artifacts/v3_external_source_pilot_p55263_mechanism_control_design_import_safety_current702_20260616_run0008.json`.
  The packet maps the adenosine kinase / RHEA:20824 context to candidate
  `pfkb_ribokinase_family`, but keeps **0** import-ready/countable rows and blockers for manual
  source-mechanism review, representation instability, family import-safety adjudication, terminal
  review decision, and full label-factory gate.
- Added a durable P55263 PfkB feasibility audit:
  `artifacts/v3_external_source_pilot_p55263_pfkb_control_feasibility_audit_current702_20260616_run0008.json`.
  It records that existing PfkB support is source/review context and the source-free ATP/Mg and
  acceptor-pocket control is still not implemented, so P55263 remains held.
- Storage hygiene remains non-blocking for registry safety: no `data/registries` or `artifacts`
  file exceeds **90 MB**. Run0008 storage artifacts
  `artifacts/v3_artifact_storage_inventory_current702_20260616_run0008.json`,
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run0008.json`,
  `artifacts/v3_artifact_producer_consumer_manifest_current702_20260616_run0008.json`,
  `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run0008.json`, and
  `artifacts/v3_artifact_migration_execution_manifest_current702_20260616_run0008.json` record
  **45** large-unclassified policy blockers, **116** manifest rows, **0** migration-ready files,
  and **0** deletion/removal-authorized files. Migration dry run validated with **116** rows and
  `removal_allowed=0`.
- Next exact action: use Q6NSJ0's repaired boundary and P55263's control-design packet only as
  review planning evidence. Do not apply/import from run0008 artifacts. The next scaling unlock is
  explicit terminal review/factory replay for the five control-repaired rows, an implemented
  source-free PfkB/ribokinase-family control plus P55263 import-safety adjudication, or a new
  source-handle/source-transfer lane that passes duplicate, active-site, factory, novelty,
  governor, and row-guardrail gates.

## Session run - Q6NSJ0/P55263 source-transfer replay held; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `490eb6856a77478b730a7642589f867c18b6ff84`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before/after stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No registry apply or label
  write was attempted.
- Baseline/final safety stayed green: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed; focused transfer/CLI suite passed **367 passed, 160 subtests**; final full
  `PYTHONPATH=src pytest -q` passed **2392 passed, 1 warning, 244 subtests**. Final compileall,
  docs-reference check, JSON/JSONL parse, hard-limit scan, and `git diff --check` are rerun below
  before commit.
- Coverage remains unchanged at **8728** combined labels = **702** frozen + **8026** expansion, with
  no holes, floor deficit **0**, novelty replay **7565** admit / **414** throttle / **47** reject,
  **0** ready existing lanes >=150, and top projected clean admits **77**. This run continued
  source-transfer repair rather than reviewed-Swiss-Prot padding.
- Completed the run2205 next action for Q6NSJ0. Current-slice artifacts
  `artifacts/v3_external_source_pilot_needs_review_resolution_q6nsj0_replacement_current702_20260616_run2306.json`,
  `artifacts/v3_external_source_pilot_decisions_review_resolved_q6nsj0_replacement_current702_20260616_run2306.json`,
  and
  `artifacts/v3_external_source_pilot_mechanism_repair_lanes_q6nsj0_replacement_current702_20260616_run2306.json`
  route Q6NSJ0 to `split_glycoside_hydrolase_from_metal_hydrolase_control`.
- Q6NSJ0 still cannot import. Its boundary control
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_q6nsj0_replacement_current702_20260616_run2306.json`
  has active-site dyad **463/520** and no metal-ligand context, but remains incomplete because the
  current full40 heuristic top1 role fraction is **0.3333** with only one role hint. The merged
  glycoside adjudication
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_merged_q6nsj0_p33025_current702_20260616_run2306.json`
  keeps Q6NSJ0 and P33025 at `glycoside_boundary_representation_conflict_not_repaired`.
- Fixed glycoside import-safety duplicate-status handling so later UniRef/current-reference
  no-overlap status overrides stale active-site `broader_duplicate_screening_required` blockers.
  Added regression coverage in `tests/test_transfer_scope.py`.
- Routed P55263 into an explicit manual source-mechanism review packet instead of a generic missing
  lane:
  `artifacts/v3_external_source_pilot_manual_source_mechanism_review_packet_p55263_with_stability_current702_20260616_run2306.json`.
  P55263 has active-site residue **317**, Rhea **RHEA:20824**, and UniRef/current-reference
  no-overlap, but lacks current heuristic scoring. Matched stability audit
  `artifacts/v3_external_source_pilot_representation_backend_stability_p55263_matched_current702_20260616_run2306.json`
  adds a P55263 row and shows nearest-reference instability (Q9TVW2 -> P03958), so the packet adds
  `representation_control_instability_review_required`. The new CLI
  `build-external-source-pilot-manual-source-mechanism-review-packet` is non-authorizing and
  preserves `ready_for_label_import: false`.
- Final merged gap audit
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_p55263_with_merged_glyco_import_safety_current702_20260616_run2306.json`
  holds **7** rows with **0** import-ready and **0** countable candidates: **4**
  `review_decision_and_factory_gate_blocked_after_control_repair`, **2**
  `family_control_unresolved_after_adjudication`, and **1**
  `manual_source_mechanism_review_required`. Consolidated review-only import safety
  `artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_q6nsj0_p55263_with_stability_packet_current702_20260616_run2306.json`
  passed **safe=True**, **0** unsafe artifacts, **0** new countable labels.
- Follow-up glycoside replacement scouts after treating Q6NSJ0 as failed,
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_replacement_scout_after_q6nsj0_current702_20260616_run2306.json`
  and
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_replacement_scout_after_q6nsj0_live_current702_20260616_run2306.json`,
  selected **no** replacement candidate: all six remaining glycan rows are
  `replacement_scope_mismatch_or_low_priority`, with **0** import-ready and **0** countable rows.
  Do not keep cycling this handle without new source evidence or a new source-free control design.
- Storage hygiene: docs-reference check
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run2306.json` has **0**
  missing references across **2110** checked references. Hard-limit scan found no
  `data/registries` or `artifacts` file over **90 MB**. Storage inventory/policy artifacts
  `artifacts/v3_artifact_storage_inventory_current702_20260616_run2306.json` and
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run2306.json` remain blocked by
  **44** large-unclassified artifacts, with **0** deletions authorized. The producer/consumer
  manifest and readiness plan
  `artifacts/v3_artifact_producer_consumer_manifest_current702_20260616_run2306.json` and
  `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run2306.json` have **116**
  rows, **0** migration-ready files, and **0** deletion-authorized files. The dry-run execution
  manifest `artifacts/v3_artifact_migration_execution_manifest_current702_20260616_run2306.json`
  validated with **116** rows and `removal_allowed=0`; this is not a registry-size hard blocker.
- Next exact action: repair or replace the glycoside boundary control with source-free
  representation/heuristic evidence for Q6NSJ0/P33025, or manually resolve P55263's
  mechanism-control family. Do not apply/import until explicit review decisions, duplicate checks,
  family controls, full label-factory gates, novelty, governor, and row guardrails all pass.

## Session run - Q6NSJ0 replacement packet routed; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `e399887446677b2c47c0b72564d634842d357b4d`,
  acquired `.git/catalytic-earth-automation.lock`, and confirmed frozen current702 sha before and
  after work stayed `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. No label
  registry apply was attempted.
- Baseline/final safety stayed green: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed; focused registry/source/leakage/novelty/import/transfer/CLI tests passed **607 passed,
  174 subtests**; final full `PYTHONPATH=src pytest -q` passed **2389 passed, 1 warning, 244
  subtests**. `compileall`, JSON parsing, hard-limit scan, and `git diff --check` passed.
- Fresh planning/post-noapply state:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run2205_pre_lane.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run2205_post_noapply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run2205_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run2205_post_noapply.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run2205_pre_lane.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run2205_pre_lane.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run2205_pre_lane.json`, and
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run2205.json`. Coverage remains
  **8728** combined = **702** frozen + **8026** expansion, no holes, floor deficit **0**, novelty
  replay **7565** admit / **414** throttle / **47** reject, top ready lane **77**, reviewed
  Swiss-Prot projection **9673**, gap **327** to 10k.
- Added review-only Q6NSJ0 replacement scouting and pinned pilot selection support. Key artifacts:
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_replacement_scout_current702_20260616_run2205.json`
  selected Q6NSJ0 as the P33025 replacement candidate, and
  `artifacts/v3_external_source_pilot_candidate_priority_q6nsj0_replacement_current702_20260616_run2205.json`
  selected **13** pilot rows with Q6NSJ0 pinned. Pinned rows now flow into review export/evidence
  packets without becoming import-ready or countable.
- Advanced Q6NSJ0 through the review-only source-transfer packet:
  `artifacts/v3_external_source_active_site_evidence_sample_q6nsj0_window_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_evidence_dossiers_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_active_site_evidence_decisions_q6nsj0_replacement_current702_20260616_run2205.json`,
  and `artifacts/v3_external_source_pilot_uniref_current_reference_screen_q6nsj0_replacement_current702_20260616_run2205.json`.
  Q6NSJ0 has explicit active-site positions **463** and **520**, Rhea **RHEA:21112**, bounded
  sequence no-signal, and no UniRef90/50 current-reference overlap.
- Built exact current-slice representation/decision routing artifacts:
  `artifacts/v3_external_source_pilot_representation_backend_plan_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_representation_backend_sample_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_representation_backend_stability_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_representation_adjudication_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_success_criteria_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_terminal_decisions_q6nsj0_replacement_current702_20260616_run2205.json`,
  `artifacts/v3_external_source_pilot_decision_confidence_audit_q6nsj0_replacement_current702_20260616_run2205.json`,
  and normalized review artifacts. Terminal status remains **7** `deferred_requires_human_expert`,
  **6** `rejected_active_site_evidence_missing`, **0** import-ready, **0** countable.
- The expert queue
  `artifacts/v3_external_source_pilot_human_expert_review_queue_q6nsj0_replacement_current702_20260616_run2205.json`
  has **7** queued rows. After duplicate-screen replay, its only non-human blocker is
  `full_label_factory_gate_not_run`. The gap audit
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_replacement_current702_20260616_run2205.json`
  still holds **7** rows for missing family import-safety adjudication / review / factory gates.
- Storage/doc hygiene: docs reference check
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run2205.json` has **0**
  missing references. Storage inventory/policy/manifest/readiness artifacts record **14963** files,
  **43** large-unclassified policy blockers, **0** deletion authorized, and **0** migration-ready
  rows; no `data/registries` or `artifacts` file exceeds **90 MB**.
- Next exact action: build a current-slice `needs_review_resolution` and repair-lane mapping for
  Q6NSJ0, then run `build-external-source-pilot-glycoside-hydrolase-import-safety-adjudication`
  against the replacement packet. Only after that, rerun success criteria, terminal/confidence
  normalization, label-factory, novelty, governor, and row-guardrail gates before any import.

## Session run - source-transfer review gap mapped; acyl-CoA control adjudicated; no registry apply (2026-06-16, Codex automation)

- Recovered the stale run2004 worktree first, validated it, and committed it as
  `2654643e9ef3024d08835a9de2994cdf4fd337a3`. Then acquired a fresh
  `.git/catalytic-earth-automation.lock`, confirmed `git pull --ff-only origin main` was current
  from `origin/main` `c99f07bd44a63daac5c20cc4d75349d05147cc3c`, and recorded frozen current702
  SHA `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before work.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed and
  the focused registry/source/leakage/novelty/import/CLI suite passed **581 passed, 174 subtests**.
  After the first code changes, the focused transfer/CLI module suite passed **355 passed, 160
  subtests**, the final critical suite passed **715 passed, 174 subtests**, and a pre-acyl full
  pytest rerun passed **2380 passed, 1 warning, 244 subtests**. Post-acyl focused tests passed
  **3 passed**; final closeout validation is rerun below before commit.
- Fresh planning artifacts:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run2105_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run2105_pre_lane.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run2105_pre_lane.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run2105_pre_lane.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run2105_pre_lane.json`, and
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run2105.json`. Coverage remains
  **8728** combined = **702** frozen + **8026** expansion, with **0** holes, floor deficit **0**,
  Gini **0.1779**, novelty replay **7565** admit / **414** throttle / **47** reject, **0** ready
  existing lanes >=150, top projected clean admits **77**, evidence-handle reachable uplift **741**,
  reviewed-Swiss-Prot clean-positive projection **9673**, and gap **327** to 10k.
- Added `build-external-source-pilot-review-resolution-gap-audit` and CLI coverage. The initial
  run2105 gap audit
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_t12_allvsall_uniref_current702_20260616_run2105.json`
  maps the five held source-transfer review rows with **0** import-ready and **0** countable label
  candidates: three rows remain blocked by review-decision plus factory gates after control repair,
  Q8N0X4 is missing family import-safety adjudication, and P33025 still has an unresolved glycoside
  boundary control.
- Re-routed Q8N0X4 from manual review to
  `add_acyl_coa_lyase_thioesterase_scope_control` and added
  `build-external-source-pilot-acyl-coa-lyase-thioesterase-control`. The staged control artifact
  `artifacts/v3_external_source_pilot_acyl_coa_lyase_thioesterase_control_t12_allvsall_uniref_current702_20260616_run2105.json`
  records source-traced active-site residue **D320** with sequence window
  `GKGAFTFQGSMIDMPLLKQAQNTVT` plus Rhea context. It is review-only, non-countable, and not
  import-authorizing.
- Added
  `build-external-source-pilot-acyl-coa-lyase-thioesterase-import-safety-adjudication`. The real
  Q8N0X4 adjudication
  `artifacts/v3_external_source_pilot_acyl_coa_lyase_thioesterase_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2105.json`
  marks `acyl_coa_lyase_thioesterase_scope_control_repaired` while preserving explicit review,
  representation/heuristic, and full label-factory blockers. The with-acyl gap replay
  `artifacts/v3_external_source_pilot_review_resolution_gap_audit_t12_allvsall_uniref_with_acyl_import_safety_current702_20260616_run2105.json`
  still has **5** held rows, **0** import-ready, and **0** countable candidates: **4**
  `review_decision_and_factory_gate_blocked_after_control_repair` and **1**
  `family_control_unresolved_after_adjudication`.
- Refreshed mechanism repair lanes:
  `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_uniref_current702_20260616_run2105_enriched.json`.
  Lane counts are one each for AKR/NADP, SDR/NAD(P), DNA Pol X lyase, acyl-CoA
  lyase/thioesterase scope control, and glycoside hydrolase / metal hydrolase boundary.
- Review-only import-safety audit
  `artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_with_acyl_current702_20260616_run2105.json`
  is safe with **0** unsafe artifacts and **0** new countable labels across the repaired replay. No
  registry apply was attempted; post-noapply coverage and novelty artifacts
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run2105_post_noapply.json` and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run2105_post_noapply.json`
  confirm unchanged coverage/novelty state.
- Durable-doc and storage hygiene:
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run2105.json` passed with
  **0** missing references across **2080** checked references, with **14** ignored references.
  `find data/registries artifacts -type f -size +90M -print` found no files.
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run2105.json` is blocked by
  **43** large-unclassified artifacts, with **0** deletions authorized and **14932** source files
  inventoried. This is a storage-classification blocker, not a registry/shard hard-limit breach.
- Closure note:
  `work/external_source_transfer_pilot_review_resolution_gap_current702_20260616_run2105.md`.
  Next concrete action: record explicit review decisions for the four control-repaired rows and
  rerun duplicate/factory gates only after those decisions exist; separately repair or replace the
  P33025 glycoside-boundary control. Keep all five source-transfer rows out of import/apply unless
  review decision, duplicate, label-factory, novelty, governor, and row-guardrail gates pass
  explicitly.

## Session run - source-transfer review/factory replay refreshed; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `c99f07bd44a63daac5c20cc4d75349d05147cc3c`,
  acquired `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main`
  was already up to date. Frozen current702 sha before work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed; the
  focused registry/source/leakage/novelty/import/CLI/transfer suite passed **697 passed, 174
  subtests**. After the CLI fix, focused parser/transfer tests passed **3 passed** and **12 passed,
  117 deselected**, and the broader focused suite passed **600 passed, 174 subtests**. `compileall`
  passed.
- Fresh planning artifacts:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run2004_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run2004_pre_lane.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run2004_pre_lane.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run2004_pre_lane.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run2004_pre_lane.json`, and
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run2004.json`. Coverage remains
  **8728** combined = **702** frozen + **8026** expansion, with **0** holes, floor deficit **0**,
  Gini **0.1779**, novelty replay **7565** admit / **414** throttle / **47** reject, **0** ready
  existing lanes >=150, top projected clean admits **77**, evidence-handle reachable uplift **741**,
  reviewed-Swiss-Prot clean-positive projection **9673**, and gap **327** to 10k.
- Advanced the run1904 next action through the review/factory replay path:
  `artifacts/v3_external_source_pilot_review_decision_export_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_evidence_packet_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_evidence_dossiers_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_active_site_evidence_decisions_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_success_criteria_t12_allvsall_uniref_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_terminal_decisions_t12_allvsall_uniref_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_t12_allvsall_uniref_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_uniref_current702_20260616_run2004.json`,
  `artifacts/v3_external_source_pilot_decisions_review_normalized_t12_allvsall_uniref_current702_20260616_run2004.json`, and
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run2004.json`.
- Success criteria remains `needs_more_work`: **12** rows still have no terminal review decision and
  no full label-factory gate, **7** have duplicate-screening unresolved, **6** have active-site
  source unresolved, **2** have representation-control unresolved, and **0** rows are import-ready
  or countable. Normalized review routing still queues **5** rows: C9JRZ8, O14756, P06746, Q8N0X4,
  and P33025. Their shared non-human blockers are `external_review_decision_artifact_not_built` and
  `full_label_factory_gate_not_run`.
- Review-only guardrails stayed safe:
  `artifacts/v3_external_source_pilot_review_only_import_safety_t12_allvsall_uniref_current702_20260616_run2004.json`
  passed. Mechanism repair controls and import-safety adjudications were refreshed:
  AKR, SDR, and DNA Pol X representation conflicts remain repaired review-only; the glycoside
  boundary remains unrepaired; all four adjudications report **0** import-ready and **0** countable
  rows. Closure note:
  `work/external_source_transfer_pilot_review_factory_closure_current702_20260616_run2004.md`.
- A direct `check-label-factory-gates` attempt was intentionally not bypassed after lineage
  validation rejected mixing slice `20260616` review-only source-transfer audit input with required
  slice `500` label-factory baseline inputs. No label-factory pass was claimed.
- Code hardening: `build-external-source-pilot-terminal-decisions` no longer defaults optional
  structural TM context to stale `artifacts/v3_external_structural_tm_holdout_path_1025.json`; the
  default is now `None`, with parser regression coverage in `tests/test_cli.py`. A `/tmp`
  no-struct replay verified the fixed default.
- Storage/source posture: hard-limit scan found no `data/registries` or `artifacts` files over
  **90 MB**. `artifacts/v3_artifact_storage_policy_check_current702_20260616_run2004.json` remains
  blocked with **41** policy blockers, **0** deletion-authorized rows, and **0** migration-ready
  rows in `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run2004.json`.
- Next exact action: build or obtain a source-supported expert review decision artifact for the
  five queued `needs_review` rows, then rerun success criteria and full label-factory gates with
  same-slice baseline inputs. Do not import/apply from run2004 artifacts.

## Session run - source-transfer UniRef duplicate screen cleared; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `dcebefa0a15a1e589834a391b1279c3b0b741340`,
  acquired `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main`
  was already up to date. Frozen current702 sha before and after work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed.
- Baseline and final safety were green: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed; baseline critical registry/leakage/novelty/import suite passed **587 passed, 174
  subtests**; focused new UniRef/current-reference regression suite passed **6 passed, 126
  deselected**; full CLI/transfer-scope module suite passed **349 passed, 160 subtests**; final
  critical suite passed **592 passed, 174 subtests**; full `PYTHONPATH=src pytest -q` passed
  **2374 passed, 1 warning, 244 subtests**. `compileall`, generated run1904 JSON parsing, progress
  JSONL parsing, and `git diff --check` passed.
- Fresh planning/post-state artifacts:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1904_pre_lane.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1904_post_noapply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1904_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1904_post_noapply.json`, and
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1904_pre_lane.json`.
  Coverage remains **8728** combined = **702** frozen + **8026** expansion, with **0** holes, floor
  deficit **0**, Gini **0.1779**, novelty replay **7565** admit / **414** throttle / **47** reject,
  **0** ready existing lanes >=150, and top projected clean admits **77**.
- Refreshed non-destructive source scouts:
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run1904_pre_lane.json` and
  `work/evidence_handle_expansion_current702_20260616_run1904_pre_lane.md` still show **6**
  families probed, **4** unlocked by better handles, source-supply uplift **63967**, and reachable
  positive-bronze uplift **741**. `artifacts/v3_breadth_feasibility_scout_current702_20260616_run1904_pre_lane.json`
  and `work/breadth_feasibility_scout_current702_20260616_run1904_pre_lane.md` still show **18**
  families probed, **14** clean, estimated new clean bronze **2641**, projected positive bronze
  **9673**, and gap to 10k positive bronze **327**; verdict remains
  `ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone`.
- Added a review-only source-transfer UniRef/current-reference duplicate screen:
  `build-external-source-pilot-uniref-current-reference-screen`. It reuses the existing
  UniRef/current-reference intersection machinery for source pilot rows, records UniRef90/50
  cluster context against current countable reference accessions, and cannot make rows countable or
  import-ready. Confidence and success-criteria replay now accept optional
  `--external-uniref-current-reference-screen` context.
- Live screen artifact
  `artifacts/v3_external_source_pilot_uniref_current_reference_screen_t12_allvsall_current702_20260616_run1904.json`
  processed the **5** normalized run1804 review rows, fetched **13** UniRef clusters, found **5**
  no-current-reference-overlap rows, and had **0** fetch failures or overlap holdouts.
- Refreshed the t12 all-vs-all source-transfer packet with UniRef/current-reference context:
  `artifacts/v3_external_source_pilot_success_criteria_t12_allvsall_uniref_current702_20260616_run1904.json`,
  `artifacts/v3_external_source_pilot_terminal_decisions_t12_allvsall_uniref_current702_20260616_run1904.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_t12_allvsall_uniref_current702_20260616_run1904.json`,
  `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_uniref_current702_20260616_run1904.json`,
  `artifacts/v3_external_source_pilot_decisions_review_normalized_t12_allvsall_uniref_current702_20260616_run1904.json`,
  and
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run1904.json`.
  Success criteria still reports `needs_more_work`: **5** rows now have
  `current_reference_external_all_vs_all_uniref_no_signal`, **7** rows still require broader
  duplicate screening, full label-factory gate is not run for **12**, terminal review decision is
  not accepted for **12**, active-site source remains unresolved for **6**, and representation
  control remains unresolved for **2**.
- Terminal/confidence routing remains non-countable: terminal statuses are **6**
  `rejected_active_site_evidence_missing`, **2** `rejected_duplicate_or_near_duplicate`, and **4**
  `deferred_requires_human_expert`. Confidence replay recommends **5** `needs_review`, **6**
  active-site rejections, and **1** duplicate/near-duplicate rejection. Normalized review queue has
  **5** rows and only non-human blockers `external_review_decision_artifact_not_built` and
  `full_label_factory_gate_not_run`.
- Refreshed repair controls and import-safety adjudications with suffix
  `t12_allvsall_uniref_current702_20260616_run1904`. AKR, SDR, and DNA Pol X conflicts remain
  repaired review-only; the glycoside boundary remains unrepaired. All adjudications report **0**
  import-ready and **0** countable rows.
- Closure note:
  `work/external_source_transfer_pilot_uniref_current_reference_closure_current702_20260616_run1904.md`.
  Review-queue routing note:
  `work/external_source_transfer_pilot_uniref_review_queue_current702_20260616_run1904.md`.
  Next concrete action: run the external source pilot review/factory path for the **5** queued
  `needs_review` rows in
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run1904.json`,
  then rerun repair controls, import-safety adjudication, success criteria, and label-factory/
  novelty/governor gates. Do not import/apply from run1904 artifacts.
- Durable-doc and storage hygiene:
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run1904.json` passed with
  **0** missing references across **2036** checked references. `find data/registries artifacts -type
  f -size +90M -print` found no files. Storage artifacts
  `artifacts/v3_artifact_storage_inventory_current702_20260616_run1904.json`,
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run1904.json`,
  `artifacts/v3_artifact_producer_consumer_manifest_current702_20260616_run1904.json`, and
  `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run1904.json` record
  **40** large-unclassified policy blockers, **0** deletions authorized, and **0** migrations ready
  now. Source scale audit
  `artifacts/v3_source_scale_limit_audit_current702_20260616_run1904.json` still recommends
  `stop_m_csa_only_tranche_growth_and_scope_external_source_transfer`.
- Remaining duplicate-screen residue was inspected before closeout: the **7** rows still marked
  `broader_duplicate_screening_required` are not the highest-yield next action because **6** also
  lack explicit active-site source resolution and **1** is already a representation near-duplicate
  holdout. Prioritize the five queued review rows instead of padding those lower-yield blockers.

## Session run - source-transfer repair lanes enriched; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `32deaca7e00715c5ed9bcb9141783b5efd163bc0`,
  acquired `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main`
  was already up to date. Frozen current702 sha before and after work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed.
- Baseline and final safety were green: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed; focused CLI/source-transfer regression suite passed **16 passed, 111 deselected**;
  critical registry/leakage/novelty/import suite passed **258 passed, 14 subtests**; full
  `PYTHONPATH=src pytest -q` passed **2369 passed, 1 warning, 244 subtests**. `git diff --check`,
  generated JSON parsing, and progress JSONL parsing passed.
- Fresh planning/post-state artifacts:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1804_pre_lane.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1804_post_noapply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1804_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1804_post_noapply.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1804_pre_lane.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run1804_pre_lane.json`, and
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run1804_pre_lane.json`. Coverage
  remains **8728** combined = **702** frozen + **8026** expansion, with **0** holes, floor deficit
  **0**, Gini **0.1779**, novelty replay **7565** admit / **414** throttle / **47** reject, **0**
  ready existing lanes >=150, and top projected clean admits **77**.
- Added source-context enrichment for
  `build-external-source-pilot-mechanism-repair-lanes`: the command now accepts optional
  `--source-context-decisions`, merges by accession as review-only context, and supports flattened
  terminal/active-site rows. Regression coverage is in `tests/test_transfer_scope.py` and
  `tests/test_cli.py`.
- Ran real MMseqs2 all-vs-all sequence screening across the current 47 external candidates:
  `artifacts/v3_external_source_all_vs_all_sequence_search_current702_20260616_run1804.json`,
  TSV
  `artifacts/v3_external_source_all_vs_all_sequence_search_current702_20260616_run1804.tsv`, and
  audit
  `artifacts/v3_external_source_all_vs_all_sequence_search_audit_current702_20260616_run1804.json`.
  The screen covered **47/47**, found **0** exact/near duplicate pairs, and remains review-only;
  it does not remove `uniref_wide_duplicate_screen_not_run`.
- Refreshed the selected t12 pilot packet using all-vs-all context:
  `artifacts/v3_external_source_pilot_success_criteria_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_terminal_decisions_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_decisions_review_normalized_t12_allvsall_current702_20260616_run1804.json`,
  and
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_current702_20260616_run1804.json`.
  Status is still `needs_more_work`: **6** active-site-evidence rejections, **2**
  duplicate/near-duplicate rejections, **4** direct human/expert deferrals, and **5** normalized
  review rows after confidence replay.
- Enriched mechanism repair lanes at
  `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_current702_20260616_run1804_enriched.json`.
  Lane routing: C9JRZ8 -> AKR/NADP contrast, O14756 -> SDR/NAD(P) contrast, P06746 -> DNA Pol
  X/5'-dRP lyase contrast, Q8N0X4 -> manual mechanism review, P33025 -> glycoside hydrolase /
  metal hydrolase boundary.
- Built repair controls and import-safety adjudications:
  `artifacts/v3_external_source_pilot_akr_nadp_repair_control_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_sdr_redox_repair_control_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_t12_allvsall_current702_20260616_run1804.json`,
  `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_t12_allvsall_current702_20260616_run1804.json`,
  plus the four matching `*_import_safety_adjudication_t12_allvsall_current702_20260616_run1804.json`
  artifacts. AKR, SDR, and DNA representation conflicts are repaired review-only; glycoside boundary
  remains unrepaired. All adjudications report **0** import-ready and **0** countable rows.
- Closure note:
  `work/external_source_transfer_pilot_repair_closure_current702_20260616_run1804.md`.
  Next concrete action: run the approved broader UniRef/current-reference duplicate screen for the
  **5** normalized `needs_review` rows, then rerun confidence, normalization, repair controls, and
  import-safety adjudication. Do not import/apply from run1804 artifacts.
- Durable-doc and storage hygiene:
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run1804.json` passed with
  **0** missing references across **2021** checked references. Registry file-size scan found no
  `data/registries` files over **45 MB**; run1804 artifacts are small. The artifact storage
  inventory/policy/plan
  `artifacts/v3_artifact_storage_inventory_current702_20260616_run1804.json`,
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run1804.json`,
  `artifacts/v3_artifact_producer_consumer_manifest_current702_20260616_run1804.json`, and
  `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run1804.json` record the
  same **4** pre-existing large unclassified artifacts, **0** deletions authorized, and **0**
  migrations ready now.
- Source scale limit audit
  `artifacts/v3_source_scale_limits_current702_20260616_run1804.json` still recommends
  `stop_m_csa_only_tranche_growth_and_scope_external_source_transfer`.

## Session run - learned source-transfer representation gate cleared; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `46e8112cf5cfa43c58419318180e3dd5316b3bc2`,
  acquired `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main`
  was already up to date. Frozen current702 sha before work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed and
  the focused registry/source/leakage/novelty/import suite passed **251 passed**.
- Fresh run1704 planning artifacts:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1704_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1704_pre_lane.json`, and
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1704_pre_lane.json`.
  Coverage remains **8728** combined labels = **702** frozen + **8026** expansion, with **no
  holes**, floor deficit **0**, Gini **0.1779**, novelty replay **7565** admit / **414** throttle /
  **47** reject, **0** ready existing lanes >=150, and top projected clean admits **77**.
- Implemented a narrow CLI fix in `src/catalytic_earth/cli.py`: optional structural/all-vs-all
  context for `audit-external-source-pilot-decision-confidence` now defaults to `None` and is loaded
  only when explicitly provided. This prevents stale 1025 structural artifacts from being silently
  mixed into current-slice confidence audits. Regression coverage:
  `tests/test_cli.py::CliTests::test_external_source_pilot_decision_confidence_optional_context_defaults`.
- Built learned representation samples for the 12-row run1604 pilot with current run1704 outputs.
  The ESM2 t6/8M and t12/35M samples both audited clean:
  `artifacts/v3_external_source_pilot_representation_backend_sample_esm2_t6_8m_current702_20260616_run1704.json`,
  `artifacts/v3_external_source_pilot_representation_backend_sample_esm2_t12_35m_current702_20260616_run1704.json`,
  and their audit artifacts. The selected t12 adjudication
  `artifacts/v3_external_source_pilot_representation_adjudication_t12_current702_20260616_run1704.json`
  reduced representation unresolved rows from **12** to **2**, with **8** review-only adjudicated
  rows and **2** near-duplicate holds.
- Tested a stronger ESM2 t30/150M follow-up:
  `artifacts/v3_external_source_pilot_representation_backend_sample_esm2_t30_150m_current702_20260616_run1704.json`,
  audit
  `artifacts/v3_external_source_pilot_representation_backend_sample_esm2_t30_150m_audit_current702_20260616_run1704.json`,
  stability audit
  `artifacts/v3_external_source_pilot_representation_backend_esm2_t12_vs_t30_stability_audit_current702_20260616_run1704.json`,
  and adjudication
  `artifacts/v3_external_source_pilot_representation_adjudication_t30_current702_20260616_run1704.json`.
  It did not improve unresolved representation count (**2**) and increased near-duplicate holds
  (**5**), so t12 remains the selected routing state.
- Consolidated gate check with the selected t12 pilot sample
  `artifacts/v3_external_source_transfer_gate_check_pilot_esm2_t12_current702_20260616_run1704.json`
  passes **66/66** gates with **0** blockers. It still reports **0** countable/import-ready rows and
  `ready_for_label_import: false`.
- Refreshed downstream review-only routing:
  `artifacts/v3_external_source_pilot_success_criteria_t12_current702_20260616_run1704.json`,
  `artifacts/v3_external_source_pilot_terminal_decisions_t12_current702_20260616_run1704.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_t12_current702_20260616_run1704.json`,
  `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_current702_20260616_run1704.json`,
  `artifacts/v3_external_source_pilot_decisions_review_normalized_t12_current702_20260616_run1704.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_current702_20260616_run1704.json`,
  and `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_current702_20260616_run1704.json`.
  Terminal state remains non-countable: **6** rejected for missing active-site evidence, **2**
  rejected duplicate/near-duplicate, and **4** deferred to human/expert review. Normalized queue has
  **5** review rows; repair lanes are all `manual_source_mechanism_review_required`.
- Validation so far: registry validate passed; focused CLI/transfer-scope regression set passed
  **15 passed**; full `PYTHONPATH=src pytest -q` passed **2367 passed, 1 warning, 244 subtests**.
- Early closeout reason: no holes/floor deficits exist, no current high-yield lane projects >=150,
  coordinate materialization remains blocked by disk below the **10 GiB** coordinate-download floor,
  the **197** controlled-ready import-review rows still require explicit batch/label-factory/
  registry authorization, and the source-transfer pilot now needs manual source/mechanism review
  plus duplicate/factory gates before any import.
- Next concrete action: inspect the **5** rows in
  `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_current702_20260616_run1704.json`
  and resolve source-supported mechanism context manually; do not import/apply from the run1704
  source-transfer artifacts.

## Session run - external source-transfer pilot queue advanced; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `41a7102177fc9c4500454b8cf84e4bd41c167865`,
  acquired `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main`
  was already up to date. Frozen current702 sha before and after work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed and
  the focused registry/source/leakage/novelty/import suite passed **273 passed, 14 subtests**.
- Lane choice: there were no holes/floor deficits and no ready existing lanes >=150, so the run
  continued the approved high-yield source-transfer route using the current 47-row external
  source-transfer candidate manifest.
- Added an opt-in full-manifest sequence-control mode:
  `build-external-source-sequence-neighborhood-plan --include-manifest-rows`. The default
  holdout-audit-driven behavior remains unchanged; the new mode emits non-countable review-only
  sequence-control rows for manifest accessions missing from the holdout audit so blocker matrices
  can demand complete candidate coverage. Code/tests touched:
  `src/catalytic_earth/transfer_scope.py`, `src/catalytic_earth/cli.py`, and
  `tests/test_transfer_scope.py`.
- Fixed a current-slice structural lineage bug: `build-external-structural-tm-holdout-path` now
  prefers the validated artifact-lineage `slice_id` and source artifact paths over stale manifest
  metadata/default 1025 paths. This kept
  `artifacts/v3_external_structural_tm_holdout_path_current702_20260616_run1604.json` internally
  consistent on slice `20260616` and unblocked terminal-decision lineage validation.
- Built current-slice source-transfer artifacts with suffix `current702_20260616_run1604`, including
  candidate manifest, evidence plan/export, full40 active-site evidence, heuristic/structure
  controls, reaction evidence, representation controls, active-site sourcing, current sequence
  holdout audit, and full47 sequence-control artifacts. There are **105** run1604 artifacts; none are
  over **45 MB** and JSON/JSONL parsing is clean.
- Repaired the blocker-matrix input width with current full47 sequence artifacts:
  `artifacts/v3_external_source_sequence_holdout_audit_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_sequence_neighborhood_plan_full47_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_sequence_neighborhood_sample_full47_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_sequence_alignment_verification_full47_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_sequence_search_export_full47_current702_20260616_run1604.json`,
  and audits. The full47 matrix
  `artifacts/v3_external_source_transfer_blocker_matrix_full47_current702_20260616_run1604.json`
  audits clean at
  `artifacts/v3_external_source_transfer_blocker_matrix_full47_audit_current702_20260616_run1604.json`.
- Matrix result: **47** rows, **0** countable/import-ready rows, review-only. Main blockers are
  **21** explicit active-site source gaps, **14** heuristic scope mismatches, **12** representation
  backend-not-selected rows, **2** exact sequence holdouts, and **1** representation near-duplicate
  holdout.
- Built a 12-row lane-balanced pilot queue:
  `artifacts/v3_external_source_pilot_candidate_priority_current702_20260616_run1604.json`.
  Selected accessions: `C9JRZ8`, `O14756`, `P55263`, `P06746`, `Q8N0X4`, `A2RUC4`, `P00568`,
  `P27144`, `O95050`, `P51580`, `Q32P41`, and `P33025`.
- Built pilot review artifacts:
  `artifacts/v3_external_source_pilot_evidence_packet_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_review_decision_export_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_evidence_dossiers_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_active_site_evidence_decisions_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_representation_backend_plan_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_representation_backend_sample_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_review_only_import_safety_audit_current702_20260616_run1604.json`,
  `artifacts/v3_external_structural_tm_holdout_path_current702_20260616_run1604.json`, and
  `artifacts/v3_external_source_pilot_success_criteria_current702_20260616_run1604.json`.
- Pilot state: active-site evidence decisions show **6** explicit active-site-source-present rows,
  **6** binding-context-only rows, **0** accepted decisions, and **0** import-ready rows. Success
  criteria is `needs_more_work`: **12** duplicate-screening/factory/review-decision blockers,
  **11** representation-control blockers, and **6** active-site-source unresolved blockers.
- Consolidated gate check
  `artifacts/v3_external_source_transfer_gate_check_current702_20260616_run1604.json` passes
  **65/66** gates. The sole remaining gate blocker is
  `external_pilot_representation_sample_review_only`; the current pilot sample is the local
  deterministic sequence-kmer control and does not satisfy the learned-representation sample plus
  stability/adjudication requirement. A bounded local-only ESM2 t6/8M attempt
  `artifacts/v3_external_source_pilot_representation_backend_sample_esm2_t6_8m_current702_20260616_run1604.json`
  was audited clean but has `embedding_backend_available: false` and **12** pilot rows with
  `embedding_backend_unavailable`; the model weights are not cached locally and no download was
  allowed. Follow-up artifacts
  `artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_stability_audit_current702_20260616_run1604.json`
  and `artifacts/v3_external_source_pilot_representation_adjudication_current702_20260616_run1604.json`
  record `comparison_backend_unavailable` and **12** unresolved representation rows.
- Built terminal and review-routing artifacts after the structural lineage fix:
  `artifacts/v3_external_source_pilot_terminal_decisions_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_human_expert_review_queue_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_decision_confidence_audit_current702_20260616_run1604.json`,
  `artifacts/v3_external_source_pilot_decisions_review_normalized_current702_20260616_run1604.json`,
  and
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_current702_20260616_run1604.json`.
  Terminal state is **12** non-countable outcomes: **6** `rejected_active_site_evidence_missing`
  and **6** `deferred_requires_human_expert`. The normalized human/expert queue contains **6**
  rows and all artifacts report **0** import-ready/countable rows.
- Validation: final `PYTHONPATH=src python -m catalytic_earth.cli validate` passed; focused suite
  `PYTHONPATH=src pytest tests/test_transfer_scope.py tests/test_registry_io.py tests/test_source_trust_tiers.py tests/test_leakage_closure.py tests/test_novelty_admission_gate.py tests/test_external_source_admission_validation.py tests/test_external_import_review_preflight.py tests/test_bronze_preview_row_guardrails.py -q`
  passed **366 passed, 14 subtests**; full `PYTHONPATH=src pytest -q` passed **2365 passed,
  1 warning, 244 subtests**. Current-docs artifact reference check
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run1604.json` passed with
  **0** missing references.
- Next concrete action: build a current learned pilot-representation backend sample and a matching
  stability/adjudication artifact for the 12 selected pilot rows, rerun the transfer gate/confidence
  audit, and complete review/factory/duplicate gates before considering any external-registry-only
  import. Do not import/apply any labels from run1604 artifacts.

## Session run - external import closure packet refreshed; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `a611246f724128feee11857b62058a6bb64a9e5e`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main` was
  already up to date. Frozen current702 sha before and after work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed and
  the focused source/leakage/novelty/import path suite passed **293 passed, 14 subtests**.
- Fresh planning refreshes:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1503_pre_gate.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1503_pre_gate.json`, and
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1503_pre_gate.json`.
  Coverage remains **8728** combined labels = **702** frozen + **8026** expansion, with **no
  holes**, floor deficit **0**, Gini **0.1779**, and only `metal_dependent_hydrolase` over cap.
  Novelty replay remains **7565** admit / **414** throttle / **47** reject. Factory has **0**
  ready existing lanes >=150 and top projected clean admits **77**.
- Advanced the 197-row controlled-review-ready queue through the current closure packet:
  `artifacts/v3_external_import_review_preflight_size120_current702_20260616_run1503.json`,
  `artifacts/v3_external_import_review_ready_preview_size120_current702_20260616_run1503.json`,
  `artifacts/v3_external_import_review_repair_queue_size120_current702_20260616_run1503.json`,
  `artifacts/v3_external_batch_import_approval_packet_size120_current702_20260616_run1503.json`,
  and `artifacts/v3_targeted_expansion_defense_ledger_size120_current702_20260616_run1503.json`.
  The packet validates **833** review-surface rows: **197** `controlled_import_review_ready`
  and **636** blocked rows (**473** coordinate blockers, **121** locator blockers, **13**
  current702 duplicates, **27** external duplicates, **2** hard blockers). It is still
  review-only: `ready_for_production_label_import` is false and production import is not
  authorized.
- Fixed stale defense-ledger wording in
  `src/catalytic_earth/external_import_review_preflight.py`: scoped queue ledgers now derive the
  Wave 2 surface sentence from current `preview_rows`, `repair_surface_rows`, and
  `review_surface_rows`, and filter stale dynamic count claims from previous ledgers. Regression
  coverage is in `tests/test_external_import_review_preflight.py`.
- Focused closure tests passed:
  `PYTHONPATH=src pytest tests/test_external_import_review_preflight.py tests/test_cli.py::CliTests::test_external_import_review_preflight_parser_defaults tests/test_cli.py::CliTests::test_external_import_closure_packet_parser_defaults -q`
  -> **4 passed**.
- Final validation passed: full pytest completed with **2364 passed, 1 warning, 244 subtests**,
  JSON/JSONL parse passed, registry and run1503 artifact file-size scans found no files over
  **45 MB**, and `git diff --check` passed.
- Safety notes: data/registry shard sizes are under **45 MB**; current run artifacts are under
  **45 MB**. Disk free remains about **8 GiB**, below the **10 GiB** coordinate-download floor.
- Artifact storage policy check
  `artifacts/v3_artifact_storage_policy_check_current702_20260616_run1503.json` is blocked by
  **4** pre-existing large unclassified 2026-06-09/10 artifacts. Follow-up readiness plan
  `artifacts/v3_artifact_migration_readiness_plan_current702_20260616_run1503.json` authorizes
  **0** migrations/deletions, so do not clean these up ad hoc.
- Bounded non-import follow-up:
  `work/external_import_repair_queue_priorities_size120_current702_20260616_run1503.md` ranks the
  **636** blocked rows. Highest-yield repairs are PLP children coordinate blockers (**106**),
  phosphoryl transfer coordinate blockers (**105**), redox oxygen/sulfur coordinate blockers
  (**76**), radical-SAM/cobalamin coordinate blockers (**73**), and near-orphan locator blockers
  (**70**).
- Durable-doc reference check
  `artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run1503.json` passes with
  **0** missing references after replacing two inherited `work/...md` placeholders with the
  concrete reaction-saturation trim report path.
- Next concrete action: do **not** import from the run1503 closure artifacts. Obtain explicit
  controlled batch approval plus label-factory and registry-change authorization for the **197**
  ready rows, or continue non-import repair by restoring disk free above **10 GiB** and rerunning
  materialization for the **636** blocked rows.

## Session run - external source-handle queue validated; no registry apply (2026-06-16, Codex automation)

- Started from current `origin/main` at `0efc3a328cfb6f011c6e4bdbd628ee4f187809ae`, acquired
  `.git/catalytic-earth-automation.lock`, and confirmed `git pull --ff-only origin main` was
  already up to date. Frozen current702 sha before work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed and frozen current702 remained unchanged.
- Baseline safety was green before work: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed, and the focused source/leakage/novelty/import path suite passed **308 passed,
  14 subtests**.
- Current planning refreshes:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1403_pre_lane.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1403_pre_lane.json`, and
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1403_pre_lane.json`.
  Coverage remains **8728** combined labels = **702** frozen + **8026** expansion, with **no
  holes**, floor deficit **0**, Gini **0.1779**, and only `metal_dependent_hydrolase` over cap.
  Novelty replay remains **7565** admit / **414** throttle / **47** reject. Factory has **0**
  ready existing lanes >=150 and top projected clean admits **77**.
- Fixed a real admission-path mismatch: the external bulk scout emits
  `provisional_external_countable_preflight_candidate`, while
  `ce-external-admission-16-validation` previously accepted only
  `external_countable_preflight_candidate`. Updated
  `src/catalytic_earth/external_source_admission_validation.py` to accept both source preflight
  states, kept the production/import wall intact, and added regression coverage in
  `tests/test_external_source_admission_validation.py`. The report text now uses the expected
  preview count rather than hard-coded "16" wording.
- Revalidated the prior post-PDE size-5 external bulk scout:
  `artifacts/v3_external_source_admission_validation_10_current702_20260616_run1403_post_pde_bulk_size5.json`
  and ready preview
  `artifacts/v3_external_source_admission_ready_preview_10_current702_20260616_run1403_post_pde_bulk_size5.json`.
  Result: **10/10** admission-ready materialization queue rows, **7** pending coordinate
  materialization, **3** pending locator materialization, **0** direct external label candidates.
- Built the bounded high-yield source-handle expansion:
  `artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1403_size120.json` with report
  `work/external_bulk_ingestion_scout_current702_20260616_run1403_size120.md`. It fetched **833**
  reviewed UniProt candidate rows and produced **431** provisional import-preview rows with **0**
  fetch failures and **0** production edits. Terminal state summary: **431**
  `provisional_external_countable_preflight_candidate`, **236** `locator_ready_candidate`,
  **117** `coordinate_ready_pending_locator`, **40** duplicate/current conflicts, **3**
  coordinate-repair, **4** locator-repair, and **2** hard blockers.
- Validated the size-120 preview through the repaired admission gate:
  `artifacts/v3_external_source_admission_validation_431_current702_20260616_run1403_bulk_size120.json`
  and ready preview
  `artifacts/v3_external_source_admission_ready_preview_431_current702_20260616_run1403_bulk_size120.json`.
  Result: **431/431** validation passed, **402** `admission_ready_pending_coordinate_materialization`,
  **29** `admission_ready_pending_locator_materialization`, **0** direct external label candidates,
  and **0** production import authorization. Largest lanes in the admission queue are PLP children
  **108**, phosphoryl transfer **108**, redox oxygen/sulfur **72**, radical-SAM/cobalamin **67**,
  glycoside/nucleoside **56**, metal hydrolase **19**, and near-orphan/no-reliable-structure **1**.
- A probe of `build-external-source-structure-mapping-plan` was blocked because its default
  `artifacts/v3_external_source_active_site_evidence_sample.json` input is absent; no artifact was
  written.
- Scoped Wave 2 materialization was run directly against the size-120 scout and its 431-row ready
  preview, with coordinate downloads disabled and no default older sources merged:
  `artifacts/v3_external_materialization_wave2_size120_current702_20260616_run1403.json`,
  `artifacts/v3_external_materialization_wave2_size120_import_ready_preview_current702_20260616_run1403.json`,
  `artifacts/v3_external_materialization_wave2_size120_repair_queue_current702_20260616_run1403.json`,
  and locator sidecar directory
  `artifacts/external_materialization_wave2_size120_source_free_locators_current702_20260616_run1403/`.
  It consumed **833** source rows plus **431** admission-ready preview rows, wrote **667**
  source-free locator sidecars, reused local coordinates for **204** rows, promoted **197** rows
  to preview-only `import_ready_preview_materialized_coordinate_locator`, and left **636** rows in
  repair/continuation. Coordinate downloads performed: **0**. Validation passed, and production
  guardrails report no registry/import/model/threshold/ontology edits. Disk free at the end was
  **8.573 GiB**, below the 10 GiB coordinate-download floor.
- Controlled import-review preflight was run against the scoped Wave 2 outputs:
  `artifacts/v3_external_import_review_preflight_size120_current702_20260616_run1403.json`,
  `artifacts/v3_external_import_review_ready_preview_size120_current702_20260616_run1403.json`,
  and `artifacts/v3_external_import_review_repair_queue_size120_current702_20260616_run1403.json`.
  It passed validation with **197** `controlled_import_review_ready` rows and **636**
  repair/not-ready rows. Repair split: **473** coordinate blockers, **121** locator blockers,
  **13** current702 duplicates, **27** external duplicates, and **2** hard blockers. The ready
  preview is still preview-only; `ready_for_production_label_import` is false and production
  guardrails report no registry/import edits.
- Retained only the final size-120 scout/validation artifacts plus the size-5 revalidation to keep
  the commit lean; intermediate size-10/30/60 exploratory artifacts were deleted before commit.
- Next concrete action: run label-factory/novelty/governor/row-guardrail/leakage gates on the
  **197** controlled-review-ready rows and require explicit production authorization before any
  external-registry-only apply. Separately, restore disk free space above **10 GiB** and continue
  coordinate materialization for the **636** repair rows.

## Session run - PDE tier-2 floor batch applied; no positive holes remain (2026-06-16, Codex automation)

- Started from current `origin/main` at `ebc1aad2ff356deaf1c3ab9a5d542a2d77d35245`, acquired the
  automation lock, and confirmed `git pull --ff-only origin main` was already up to date. Frozen
  current702 sha before and after apply was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Baseline validation was green before work: registry validator passed and the focused source,
  leakage, novelty, registry, and scaleout/import suite passed **351 passed, 14 subtests**.
- Current governor refresh before lane work showed `metal_independent_phosphodiesterase` as the
  lone hole at **0/100**, floor deficit **100**, `metal_dependent_hydrolase` over cap, and novelty
  replay **7465** admit / **414** throttle / **47** reject.
- Stable GDPD/cyclic source-tier-2 local slicing produced floor-closing supply. Component previews:
  prior offset-0 scout
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_size30_current702_20260616_run1235.json`
  admitted **28**, and local-slice offsets **30/60/90**
  (`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset30_size30_current702_20260616_run1302.json`,
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset60_size30_current702_20260616_run1302.json`,
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset90_size30_current702_20260616_run1302.json`)
  admitted **30** rows each.
- Combined preview
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_current702_20260616_run1302.json`
  deduped to **118** candidate labels, admitted **116**, and throttled **2**. Preview governor
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_governor_current702_20260616_run1302.json`
  found 116 rows exceeded the reaction-aware cap for one concrete reaction.
- Reaction-cap-trimmed preview
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_reaction_cap_trimmed_preview_current702_20260616_run1302.json`
  held **16** surplus rows and kept exactly **100**. Row audit
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_reaction_cap_trimmed_row_guardrail_audit_current702_20260616_run1302.json`
  audited all **100** rows with **0** problems.
- Explicit apply appended the PDE batch to the external registry only. A registry audit found the
  16 reaction-cap-held accessions present after the first write; correction artifact
  `artifacts/v3_metal_independent_phosphodiesterase_reaction_cap_surplus_registry_correction_current702_20260616_run1302.json`
  removed exactly those surplus rows. Final external rows: **8026**. Final PDE rows: **100**.
- Post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1302_post_pde_apply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1302_post_pde_apply.json`,
  and `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1302_post_pde_apply.json`.
  Coverage reports **8728** combined labels, **no holes**, floor deficit **0**, Gini **0.1779**,
  and only `metal_dependent_hydrolase` over cap. Novelty replay reports **7565** admit /
  **414** throttle / **47** reject across **8026** expansion rows. Factory still has **0** ready
  existing lanes >=150 and top projected clean admits **77**.
- Post-PDE breadth scout
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run1302_post_pde_apply.json`
  probed **18** reviewed Swiss-Prot families, found **14** clean families, estimated **2641** new
  clean positive bronze, projected positive bronze **9673**, and left a **327** gap to 10k; verdict
  remains reviewed Swiss-Prot alone is not enough. A bounded size-5 external bulk ingestion scout
  `artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1302_post_pde_apply_size5.json`
  found **35** candidates and **10** provisional import-preview rows, with import preview
  `artifacts/v3_external_bulk_ingestion_import_preview_current702_20260616_run1302_post_pde_apply_size5.json`;
  this is strategy input only and must pass `ce-external-admission-16-validation` before any
  countable import.
  Strategy artifact `artifacts/v3_post_pde_source_tier_strategy_current702_20260616_run1302.json`
  records the next exact action: build a beyond-reviewed source-tier or source-handle expansion
  pilot for clean non-hydrolase families, then pass the same preview/audit/novelty/cap/test gates
  before any external-registry-only apply.
- Final validation passed: registry validator passed, focused safety suite passed
  **383 passed, 14 subtests**, full pytest passed **2363 passed, 1 warning, 244 subtests**,
  JSON/JSONL parse passed, registry file-size scan found no file over **45 MB**, and
  `git diff --check` passed. Frozen current702 stayed unchanged.
- Next concrete action: do **not** pad PDE, SBL, APH, N-ribosyl, or any balanced/reaction-saturated
  lane. Use the post-PDE factory/governor state to design the next high-yield source-tier or
  source-handle expansion, then run non-destructive preview, row guardrail audit, novelty/governor
  replay, leakage/source-contract tests, and explicit apply only if a meaningful clean batch passes.

## Session run - PDE Hydrolase and tier-2 scouts blocked below gate (2026-06-16, Codex automation)

- Started from current `origin/main` at `cd04a5fcaac9c97aa3050736878f78128e172bf5`, recovered a
  dead automation lock PID, reacquired `.git/catalytic-earth-automation.lock`, and confirmed
  `git pull --ff-only origin main` was already up to date. Frozen current702 sha before work was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no registry apply was
  performed and frozen current702 remained unchanged.
- Preserved the inherited mechanism-first PDE hydrolase work and made it reproducible by adding
  `metal_independent_pde_ec_3_1_4_hydrolase_non_metal`,
  `metal_independent_pde_ec_3_1_4_actsite_catalytic_non_metal`, and stricter tier-2 GDPD/cyclic
  source splits to
  `src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py` plus the offline guarded
  lane test in `tests/test_metal_independent_phosphodiesterase_sourcing.py`. EC 3.1.4 and
  all name/keyword/active-site handles are scope/fetch only; counted corroboration remains non-EC
  mechanism evidence and `predictive_evidence` stays `[]`.
- Added reusable preview row guardrails in
  `src/catalytic_earth/bronze_preview_row_guardrails.py`,
  `scripts/audit_bronze_preview_row_guardrails.py`, and
  `tests/test_bronze_preview_row_guardrails.py`. The audit checks UniProt namespace, bronze tier,
  `automation_curated`, expected fingerprint/source tier, empty predictive evidence, required
  excluded context, non-EC source-trust axes, and current702 duplicate-screen evidence before any
  apply.
- The inherited hydrolase preview
  `artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_preview_window0_120_current702_20260616_run0114.json`
  fetched **120** reviewed rows, found **17** target PDE labels, admitted **17**, held **22**
  off-target rows, and held **69** rows for missing mechanism corroboration. Row audit
  `artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_row_guardrail_audit_current702_20260616_run0114.json`
  found **0** problem rows. Apply remains **unauthorized** because this would move PDE only
  **0 -> 17**, leaving the 100-row floor open.
- Small tier-2 sample
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_preview_size20_current702_20260616_run1209.json`
  fetched **40** unreviewed rows across the two strict PDE tier-2 lanes, produced **0** target
  admissions, held **6** off-target `sam_methyltransferase` rows, and held **34** rows for missing
  or insufficient mechanism/trust-tier corroboration. This confirms the tier-2 path needs a sharper
  source wall before any larger fetch/apply attempt.
- Added and tested a second reviewed source split,
  `metal_independent_pde_ec_3_1_4_actsite_catalytic_non_metal`, after a count scout found 119
  reviewed non-metal EC 3.1.4 rows with ACT_SITE and catalytic-activity annotations. The bounded
  preview
  `artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_preview_size40_current702_20260616_run1218.json`
  fetched **40** rows, admitted only **2** target PDE labels, held **4** off-target rows, and held
  **23** rows for missing mechanism corroboration. Row audit
  `artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_row_guardrail_audit_current702_20260616_run1218.json`
  found **0** problems. Source strategy:
  `artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_source_strategy_current702_20260616_run1218.json`.
  Apply remains unauthorized.
- A sharper strict tier-2 GDPD/cyclic split was then previewed without registry writes:
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_size30_current702_20260616_run1235.json`
  fetched **60** unreviewed rows, admitted **28** target PDE labels, held **32** rows for missing
  mechanism corroboration, and held **0** off-target rows. Row audit
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_row_guardrail_audit_current702_20260616_run1235.json`
  checked all **28** source-tier-2 rows with **0** problems. This is still **no-apply**: current
  external PDE remains **0**, and the preview would only move PDE to **28/100**.
- A larger GDPD/cyclic size-120 preview was attempted after the clean 28-row scout, but the process
  terminated with SIGTERM before writing an artifact. Treat that as no evidence and rerun it only
  with a stable paginated/cursor setup before any floor-closing apply decision.
- A post-push lockless 13:02 orphan worker was stopped before it could keep writing uncontrolled
  outputs. It left a completed non-destructive GDPD/cyclic offset preview:
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_offset30_size60_current702_20260616_run1302.json`
  with report
  `work/metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_offset30_size60_current702_20260616_run1302.md`.
  The preview fetched **120** source-tier-2 rows, admitted **58** target PDE labels, held **62**
  rows for missing mechanism corroboration, and had **0** off-target rows. Row audit
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_offset30_row_guardrail_audit_current702_20260616_run1302.json`
  checked all **58** rows with **0** problems. This is still **no-apply** because PDE would remain
  **58/100**, below the floor. The same lockless sequence also left
  `artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_offset90_size30_current702_20260616_run1302.json`,
  which admitted **28** rows with **0** row-guardrail problems but reported non-independent offset
  metadata; treat it as duplicate/subfloor evidence, not apply authority. A later local-slice
  sequence completed three separate previews at offsets **30/60/90**, each admitting **30** rows
  with **0** row-guardrail problems. These are still **no-apply** diagnostics because they came
  from the lockless orphan sequence and no deduped aggregate floor-closing artifact was produced;
  even the naive slice sum is only **90/100**.
- Latest non-destructive post-tier2 audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run1209_post_tier2_scout.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1209_post_tier2_scout.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1209_post_tier2_scout.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run1209_post_tier2_scout.json`.
  They keep the current state at **8628** combined labels, **6932** combined seed surface, Gini
  **0.1948**, `metal_independent_phosphodiesterase` as the lone hole at **0/100**, novelty replay
  **7465** admit / **414** throttle / **47** reject, and **0** ready existing lanes >=150.
- Added sharp reviewed-handle count scout
  `artifacts/v3_metal_independent_phosphodiesterase_sharp_handle_count_scout_current702_20260616_run1207.json`.
  It confirms the broad EC 3.1.4 + Hydrolase baseline has **490** raw reviewed rows but has already
  previewed to only **17** admitted labels; the best sharper non-baseline handle
  `actsite_catalytic_non_metal` has only **119** raw reviewed rows before disambiguation/novelty.
  Do not spend another run retrying these reviewed windows for apply.
- Live cursor/offset PDE fetch attempts from interrupted automation runs were found still running
  and targeting overlapping artifacts; they were terminated to prevent duplicate or
  non-reproducible source writes. One stale worker appended the unauthorized **17-row** hydrolase
  preview to the external registry; that append was detected, restored back to the SBL baseline
  (**7926** external rows), and stale `post_pde_apply` artifacts were pruned. Frozen current702
  remained unchanged throughout.
- Final validation for this no-apply run: `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed with **12** source records, **46** fingerprints, **43** ontology families, and **702**
  curated labels; focused critical tests passed **267 passed, 14 subtests**; final full suite passed
  **2363 passed, 1 warning, 244 subtests**; `compileall`, JSON/JSONL parse, registry file-size
  scan, frozen SHA check, and `git diff --check` passed. Frozen current702 SHA after closeout was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; external rows remained
  **7926** with **0** external PDE rows.
- Next concrete action: do **not** apply the 17-row hydrolase, 2-row ACT_SITE, or 28-row
  GDPD/cyclic previews, and do not retry the same broad reviewed EC/name/PLD/hydrolase/ACT_SITE
  windows. The most plausible next PDE move is a stable paginated GDPD/cyclic tier-2 window or a
  genuinely sharper source wall that can actually close the 100 floor, followed by row guardrail
  audit, novelty/governor/dedup/cap replay, leakage/source-contract tests, and explicit apply only
  if the batch gate is met.

## Session run - SBL 46fp tier-2 floor batch applied; PDE remains lone hole (2026-06-16, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main` at
  `a4c86f131f0bbbfae38b3c7e309942009aa49311`, acquired the automation lock, and pulled
  fast-forward before work. Frozen current702 sha before apply was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; after apply it was the
  same. No frozen current702 rows were written.
- Built `serine_beta_lactamase` as the guarded 46th positive fingerprint lane: fingerprint,
  ontology family `serine_acyl_enzyme_beta_lactam_hydrolysis`, deploy-missing context,
  disambiguation/source-trust rule, source runner
  `src/catalytic_earth/serine_beta_lactamase_sourcing.py`, script
  `scripts/source_serine_beta_lactamase_family.py`, high-yield factory wiring, focused tests, and
  46fp hard-negative preregistration
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_46fp_1025.json`.
- Mechanism discipline stayed intact. EC 3.5.2.6, SBL names, UniProt prose, reaction text, active
  site handles, and query handles are scope/admission excluded context only. Counted axes are
  non-EC family/domain, beta-lactam hydrolysis reaction/participant, and Ser/Lys/Glu active-site
  context. Metallo/zinc beta-lactamases, PBPs/DD-peptidases, beta-lactam synthases, generic
  amidohydrolases, side-EC, EC-only, and multi-fingerprint rows are held; `predictive_evidence`
  remains `[]`.
- Live SBL tier-2 preview
  `artifacts/v3_serine_beta_lactamase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260616_run0014.json`
  fetched **240** rows, produced **115** target mechanism-corroborated labels, admitted **106**
  novelty-safe labels, held **0** off-target fingerprint matches, and held **9** by novelty/cap
  replay. Row audit
  `artifacts/v3_serine_beta_lactamase_tier2_row_guardrail_audit_current702_20260616_run0014.json`
  audited all **106** rows with **0** problems.
- Explicit reuse-preview apply appended **106** SBL bronze rows to the sharded external registry,
  skipped **0** duplicates, changed external rows **7820 -> 7926**, and changed combined label
  surface **8522 -> 8628**. The registry manifest remains GitHub-safe with shards about
  **18 MB / 18 MB / 18 MB / 8.4 MB**.
- Honest counters after apply: external rows **7926** = external seed **6702** + external OOS
  **1224**, with external silver **30**. Combined label surface **8628**; combined seed surface
  **6932**; positive_bronze **6885**; OOS bronze **1696**; silver_confirmed **47**; projected
  **0**.
- Post-apply refreshes:
  `artifacts/v3_coverage_redundancy_audit_current702_20260616_run0014_post_sbl_apply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0014_post_sbl_apply.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0014_post_sbl_apply.json`,
  `artifacts/v3_mechanism_representation_loop_current702_20260616_run0014_post_sbl_apply.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run0014_post_sbl_apply.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run0014_post_sbl_apply.json`, and
  `artifacts/v3_post_sbl_source_strategy_current702_20260616_run0014.json`. Coverage reports
  **8628** combined labels, Gini **0.1948**, lone hole `metal_independent_phosphodiesterase`, and
  over-cap `metal_dependent_hydrolase`. Novelty replay reports **7465** admit / **414** throttle /
  **47** reject across **7926** expansion rows. Factory reports **0** ready existing lanes >=150;
  top projected clean admits are **77**. Breadth feasibility reports reviewed Swiss-Prot clean-only
  positives project to **9573**, leaving a **427** gap to 10k before further diversity discounts.
- Added source-free `bc_beta_lactam_hydrolysis` to the representation loop so SBL rows do not
  collapse into generic ester/Ser-His hydrolase chemistry. Post-apply representation loop reports
  **6702** seed labels, LOO self-consistency **0.7635**, SBL self-consistency **1.0**, **3211**
  promotion candidates, and **1585** review outliers; no registry rows were written by the audit.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12** source
  records, **46** fingerprints, **43** ontology families, and **702** curated labels. Focused
  baseline safety suite passed **363 passed**. Focused SBL/leakage/import suite passed
  **156 passed** after apply. Stale-invariant targeted rerun passed **5 passed**. Final full suite
  passed **2357 passed, 1 warning, 244 subtests passed in 169.66s**. `compileall`, JSON/JSONL
  parsing, registry file-size scan, frozen-SHA check, and `git diff --check` passed before doc
  closeout.
- Closeout snapshot: **2026-06-16T00:53:00Z**, elapsed **39.2** minutes, remaining **15.8**
  minutes. Closed before minute 50 because a second safe same-run scaling item was concretely
  blocked: SBL is floor-closed and reaction-saturated, PDE remains the only true hole but all
  existing PDE reviewed/PLD/tier-2 handles are documented below gate or boundary-heavy, the
  high-yield factory reports **0** ready existing lanes >=150, and evidence-handle/breadth scouts
  are strategy inputs rather than apply authority.
- Next concrete action: do **not** source more SBL without a new reaction-diversity split, and do
  not retry broad PDE EC/name handles, the 7-row PLD preview, or terpene window170. The remaining
  safe bronze-scaleout path is a sharper `metal_independent_phosphodiesterase` source wall that
  can plausibly close the 100 floor; if PDE remains blocked, move to a source-tier expansion beyond
  reviewed Swiss-Prot through count scout, preregistration if needed, non-destructive preview, row
  audit, novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit apply
  only if gates pass.

## Session run - PDE PLD scout valid but subfloor; serine beta-lactamase plan staged (2026-06-15, Codex automation)

- Started from current `origin/main` at `a4c86f131f0bbbfae38b3c7e309942009aa49311`, acquired the automation lock, and pulled fast-forward before work. Frozen current702 sha before/after the no-apply run stayed `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no frozen current702 rows and no external registry rows were written.
- Baseline safety was green: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12** source records, **45** fingerprints, **42** ontology families, and **702** curated labels. Focused baseline source/admission/novelty/import/PDE tests passed **128 passed**.
- Refreshed planning state in `artifacts/v3_coverage_redundancy_audit_current702_20260615_run2314_pre_lane.json`, `artifacts/v3_novelty_admission_gate_audit_current702_20260615_run2314_pre_lane.json`, and `artifacts/v3_high_yield_family_lane_factory_current702_20260615_run2314_pre_lane.json`: combined labels **8522**, fingerprint Gini **0.1944**, `metal_independent_phosphodiesterase` remains the lone hole, novelty replay **7359** admit / **414** throttle / **47** reject, and **0** existing lanes project >=150 clean admits.
- Added a narrow PLD source-wall extension for `metal_independent_phosphodiesterase`: `phospholipase D` family text plus explicit PLD hydrolytic reaction participants (`phosphocholine`, phosphoethanolamide/glycosylinositol, and glycero-3-phosphate). EC/name/reaction handles stay excluded context and `predictive_evidence` remains `[]`; phospholipase C remains a hold. Focused tests cover PLD admit and PLC hold.
- PLD preview `artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_preview_current702_20260615_run2314.json` fetched **22** reviewed rows, produced **7** target mechanism-corroborated labels, held **4** off-target metallophosphoesterase/nuclease rows, and admitted **7** novelty-safe labels. Row guardrail audit `artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_row_guardrail_audit_current702_20260615_run2314.json` found **0** problems, but this is far below the 100 PDE floor, so no apply was authorized.
- Added timeout-safe live fetching to `scripts/source_terpene_cyclase_synthase_family.py` and fetcher pass-through in `src/catalytic_earth/terpene_cyclase_synthase_sourcing.py`. Terpene cap-close window `artifacts/v3_terpene_cyclase_synthase_capclose_window170_preview_current702_20260615_run2314.json` fetched **138** rows, found **7** target labels, and admitted **0** novelty-safe rows. Do not retry window170 for apply.
- Evidence/source strategy artifacts: `artifacts/v3_metal_independent_phosphodiesterase_source_strategy_current702_20260615_run2314.json`, `artifacts/v3_evidence_handle_expansion_current702_20260615_run2314.json`, `artifacts/v3_serine_beta_lactamase_source_tier_scout_current702_20260615_run2314.json`, and `artifacts/v3_serine_beta_lactamase_build_plan_current702_20260615_run2314.json`. The serine beta-lactamase scout found reviewed supply subscale (**147** exact/name, **132** active-site), but strict unreviewed tier-2 active-site/reaction supply is large (**1854**) for a future guarded lane if PDE remains blocked.
- Honest counters are unchanged from SDR: external rows **7820** = external seed **6596** + external OOS **1224**, external silver **30**; combined label surface **8522**; combined seed surface **6826**; positive bronze **6779**; OOS bronze **1696**; silver_confirmed **47**; projected **0**.
- Final validation: focused post-change suite passed **136 passed in 1.93s**. Full suite passed **2348 passed, 1 warning, 244 subtests passed in 175.77s**. `compileall`, JSON/JSONL parsing, doc/progress reference tests (**5 passed**), registry file-size scan, frozen-SHA check, and `git diff --check` passed.
- Closed before minute 50 because all safe mutation paths were concretely blocked: PDE PLD is only **7** admits, terpene window170 has **0** admits, balanced/capped families are not eligible for padding, and serine beta-lactamase requires new fingerprint/OOS/source-runner implementation before any preview/apply authority.
- Next concrete action: do not apply the PLD preview, do not retry broad PDE EC/name handles or terpene window170. Either build a sharper mechanism-bearing PDE split capable of closing the 100 floor, or if PDE remains blocked implement `serine_beta_lactamase` from the build plan through fingerprint/ontology/OOS/source-runner tests, non-destructive preview, row audit, novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit apply only if gates pass.

## Session run - SDR 45fp bronze floor batch applied; PDE remains lone hole (2026-06-15, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main` at
  `5e7c1006e7f4a0438bc3bc4943eedd78acded89f`, acquired the automation lock, and pulled
  fast-forward before work. Frozen current702 sha before apply was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; after apply it was the
  same. No frozen current702 rows were written.
- Built `short_chain_dehydrogenase_reductase` as the guarded 45th positive fingerprint lane:
  fingerprint, ontology family `sdr_nicotinamide_hydride_transfer`, deploy-missing context,
  disambiguation/source-trust rule, source runner
  `src/catalytic_earth/short_chain_dehydrogenase_reductase_sourcing.py`, script
  `scripts/source_short_chain_dehydrogenase_reductase_family.py`, high-yield factory wiring,
  focused tests, and 45fp hard-negative preregistration
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_45fp_1025.json`.
- Mechanism discipline stayed intact. EC 1.1.1, SDR names, UniProt prose, and source handles are
  scope/admission excluded context only. Counted axes are non-EC SDR family/domain, NAD(P)
  cosubstrate, Rhea redox reaction/participant, and active/binding-site context when available.
  AKR/MDR/ALDH/flavin/metal redox boundary rows are held, and `predictive_evidence` remains `[]`.
- Live sourcing tried smaller windows first (10, 60, 120, 150, and three-lane 60 previews). The
  apply-sized artifact is
  `artifacts/v3_short_chain_dehydrogenase_reductase_sourcing_preview_named220_current702_20260615_run2213.json`:
  **220** fetched rows, **103** target mechanism-corroborated labels, **100** novelty-admitted
  labels, **0** off-target holds, and `short_chain_dehydrogenase_reductase` **0 -> 100** (cap
  150; floor reached). Row audit
  `artifacts/v3_short_chain_dehydrogenase_reductase_row_guardrail_audit_current702_20260615_run2213.json`
  audited all **100** rows with **0** problems.
- Explicit reuse-preview apply appended **100** SDR bronze rows to the sharded external registry,
  skipped **0** duplicates, changed external rows **7720 -> 7820**, and changed combined label
  surface **8422 -> 8522**. Shard safety remains green: manifest about **4 KB**, shards about
  **17 MB / 17 MB / 17 MB / 7.4 MB**, curated current702 about **500 KB**.
- Honest counters after apply: external rows **7820** = external seed **6596** + external OOS
  **1224**, with external silver **30**. Combined label surface **8522**; combined seed surface
  **6826**; positive bronze **6779**; OOS bronze **1696**; silver_confirmed **47**; projected
  **0**.
- Post-apply planning refreshes:
  `artifacts/v3_coverage_redundancy_audit_current702_20260615_run2213_post_sdr_apply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260615_run2213_post_sdr_apply.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_run2213_post_sdr_apply.json`,
  `artifacts/v3_mechanism_representation_loop_current702_20260615_run2213_post_sdr_apply.json`,
  `artifacts/v3_bronze_silver_promotion_preview_current702_20260615_run2213_post_sdr_apply.json`,
  and `artifacts/v3_family_set_expansion_targets_current702_20260615_run2213_post_sdr_apply.json`.
  Coverage reports **8522** combined labels, Gini **0.1944**, lone hole
  `metal_independent_phosphodiesterase`, and over-cap `metal_dependent_hydrolase`. Novelty replay
  reports **7359** admit / **414** throttle / **47** reject across **7820** expansion rows. Factory
  reports **0** ready existing lanes >=150; top projected clean admits are **77** under current
  handles. Representation loop reports LOO self-consistency **0.7576**; SDR self-consistency is
  **0.95**, and generic NAD(P) dehydrogenase now has a documented source-free chemistry ceiling
  against SDR.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12** source
  records, **45** fingerprints, **42** ontology families, and **702** curated labels. Focused SDR /
  leakage / import suites passed **106 passed**. Targeted stale-invariant rerun passed **6 passed**.
  Final full suite passed **2346 passed, 1 warning, 244 subtests passed in 166.99s**. `compileall`,
  JSON/JSONL parsing, file-size scan, frozen-SHA check, and `git diff --check` were clean before
  doc closeout.
- Next concrete action: do **not** source more SDR, APH, or the same PDE EC/name windows. The only
  current hole is `metal_independent_phosphodiesterase`; build a materially sharper
  mechanism-bearing PDE source wall beyond EC/name counts, or pivot to a new high-yield
  family/source-tier strategy. Any mutation must go through OOS preregistration if the fingerprint
  universe changes, non-destructive preview, row audit, novelty/governor/dedup/cap replay,
  leakage/source-contract validation, and explicit apply only if the clean batch gate is met.

## Session run - APH tier-2 bronze batch applied; PDE remains lone hole (2026-06-15, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main` at
  `f60617d6a1492cdf264689cdf3216bd428425250`, acquired the automation lock, and pulled
  fast-forward before work. Frozen current702 sha before apply was
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; after apply it was the
  same. No frozen current702 rows were written.
- Implemented guarded APH unreviewed tier-2 source-handle support in
  `src/catalytic_earth/aminoglycoside_phosphotransferase_sourcing.py` and
  `scripts/source_aminoglycoside_phosphotransferase_family.py`. The new path is fail-closed:
  unreviewed tier-2 lanes require `source_tier_2`, at least three independent non-EC mechanism
  axes, EC scope only, and empty `predictive_evidence`.
- APH tier-2 non-destructive preview
  `artifacts/v3_aminoglycoside_phosphotransferase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260615.json`
  fetched **240** rows, found **239** target labels, admitted **150** novelty-safe rows, held
  **19** by novelty replay, and held **70** more at cap. Row audit
  `artifacts/v3_aminoglycoside_phosphotransferase_tier2_row_guardrail_audit_current702_20260615.json`
  audited all **150** rows with **0** problems.
- Explicit reuse-preview apply appended **150** APH bronze rows to the sharded external registry,
  skipped **0** duplicates, changed external rows **7570 -> 7720**, and changed combined label
  surface **8272 -> 8422**. Shard safety remains green: manifest about **1.2 KB**, shards about
  **17 MB / 17 MB / 17 MB / 6.7 MB**, curated current702 about **496 KB**.
- Honest counters after apply: external rows **7720** = external seed **6496** + external OOS
  **1224**, with external silver **30**. Combined label surface **8422**; combined seed surface
  **6726**; positive bronze **6679**; OOS bronze **1696**; silver_confirmed **47**; projected
  **0**.
- Post-apply planning refreshes:
  `artifacts/v3_coverage_redundancy_audit_current702_20260615_post_aph_tier2_apply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_aph_tier2_apply.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_aph_tier2_apply.json`,
  `artifacts/v3_family_set_expansion_targets_current702_20260615_post_aph_tier2_apply.json`,
  `artifacts/v3_bronze_silver_promotion_preview_current702_20260615_post_aph_tier2_apply.json`,
  and `artifacts/v3_mechanism_representation_loop_current702_20260615_post_aph_tier2_apply.json`.
  Coverage reports **8422** combined labels, Gini **0.1944**, lone hole
  `metal_independent_phosphodiesterase`, and over-cap `metal_dependent_hydrolase`. Novelty replay
  reports **7259** admit / **414** throttle / **47** reject across **7720** expansion rows. Factory
  reports **0** ready existing lanes >=150; top projected clean admits are
  `short_chain_dehydrogenase_reductase` at **84** and PDE at **34** under current handles.
- Added post-APH PDE source strategy:
  `artifacts/v3_metal_independent_phosphodiesterase_post_aph_source_strategy_current702_20260615.json`
  and `work/metal_independent_phosphodiesterase_post_aph_source_strategy_current702_20260615.md`.
  The strategy records that the existing PDE previews remain blocked: **14** reviewed admits,
  **0** alternate reviewed admits, and **0** tier-2 admits with **186** off-target plus **197**
  trust-tier-insufficient holds. Do not pad or apply those previews.
- Added a PDE exact-EC distribution scout:
  `artifacts/v3_metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.json`
  and `work/metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.md`.
  Broad reviewed EC 3.1.4 has **1086** rows and **490** after the current non-metal filter, but the
  exact cyclic-nucleotide splits are all subscale after filtering: 3.1.4.17 **6**, 3.1.4.35 **7**,
  3.1.4.53 **2**, 3.1.4.52 **18**, 3.1.4.37 **15**, and 3.1.4.58 **12**. The broader windows are
  boundary-heavy, so the next PDE attempt needs a new mechanism-bearing source wall beyond EC/name
  counts.
- Added fallback source-handle scout:
  `artifacts/v3_evidence_handle_expansion_current702_20260615_post_aph_apply.json` and
  `work/evidence_handle_expansion_current702_20260615_post_aph_apply.md`. It probed **6** families,
  found **4** handle-blocked families unlocked by better reviewed handles, and estimates **741**
  capped reachable positive-bronze uplift. This is source-wall headroom only: NAD(P)/oxidoreductase
  pools overlap and must be split into family-specific capped lanes, not sourced as one broad
  bucket.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed before the APH apply.
  Post-change focused critical suite passed **97 passed**; final full suite passed **2337 passed,
  1 warning, 244 subtests passed in 169.68s**. `compileall`, JSON/JSONL parsing, file-size scan,
  and `git diff --check` were clean before doc closeout; final doc-closeout validation is recorded
  in `work/status.md`.
- Closeout snapshot: **2026-06-15T21:46:55Z**, elapsed **33.6** minutes, remaining **21.4**
  minutes. Closed before minute 50 because APH closed at cap and all remaining same-run mutation
  paths are concretely blocked: reviewed PDE **14** admits, alternate reviewed PDE **0**, tier-2
  PDE **0**, exact cyclic PDE splits at most **18** after the non-metal filter, and no ready
  existing lane >=150. The next useful work is a new source-wall/OOS design, not a safe same-run
  apply.
- Next concrete action: do not source more APH, and do not retry the same PDE EC/name windows.
  Build a new mechanism-bearing PDE source wall beyond EC/name counts, or pivot to a split
  high-yield source-tier/family strategy such as SDR/AKR or serine beta-lactamase. Any mutation
  must go through OOS preregistration if the fingerprint universe changes, non-destructive preview,
  row audit, novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit
  apply only if the clean batch gate is met.

## Session run - APH 44fp infrastructure built; corrected source wall subscale, no registry mutation (2026-06-15, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main` at
  `eccb5125746353377b5d4d00a2a4aca38d7c6f08`, acquired the automation lock, and verified registry
  file-size safety: external bronze remains a manifest plus shards about **17 MB / 17 MB / 17 MB /
  5.9 MB**, below the GitHub-safe threshold. Frozen current702 stayed untouched; no external
  bronze rows were applied.
- Built `aminoglycoside_phosphotransferase` as the guarded 44th positive fingerprint lane
  infrastructure: fingerprint, ontology family `aminoglycoside_phosphoryl_transfer`, deploy-missing
  context, coverage/governor signature, disambiguation rule, source runner
  `src/catalytic_earth/aminoglycoside_phosphotransferase_sourcing.py`, script
  `scripts/source_aminoglycoside_phosphotransferase_family.py`, high-yield factory wiring, tests,
  and 44fp hard-negative preregistration
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_44fp_1025.json`.
- Corrected an important source-wall assumption before any apply: live UniProt inspection showed EC
  `2.7.1.130` and `2.7.1.192` are lipid-A and PTS MurNAc kinases, not aminoglycoside
  phosphotransferases. The APH rule/source scope is now restricted to reviewed APH ECs
  `2.7.1.95`, `2.7.1.72`, `2.7.1.87`, `2.7.1.119`, and `2.7.1.163`, with APH family/name plus
  active/binding-site, ATP/Mg, or aminoglycoside phosphorylation mechanism evidence. EC remains
  scope-only and never a counted corroborator.
- Live corrected preview was clean but subscale:
  `artifacts/v3_aminoglycoside_phosphotransferase_sourcing_preview_corrected_active_binding_bounded50_current702_20260615.json`
  / `work/aminoglycoside_phosphotransferase_sourcing_corrected_active_binding_bounded50_current702_20260615.md`
  fetched **18** reviewed rows, produced **17** target mechanism-corroborated labels, and admitted
  **17** novelty-safe rows with **0** off-target holds and **0** disambiguation holds. No apply was
  performed because this is far below the >=150 clean-admit batch gate.
- Planning refreshes after 44fp infrastructure:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_aph_44fp_infra.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260615_post_aph_44fp_infra.json`, and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_aph_44fp_infra.json`.
  Coverage reports **8272** combined labels, fingerprint Gini **0.2156**, holes
  `aminoglycoside_phosphotransferase` and `metal_independent_phosphodiesterase`, and only
  `metal_dependent_hydrolase` over cap. Novelty replay remains **7109** admit / **414** throttle /
  **47** reject across **7570** expansion rows. The factory now reports **0** ready existing lanes
  >=150; top projected clean admits under current handles is `short_chain_dehydrogenase_reductase`
  at **84**.
- Honest counters are unchanged from the N-ribosyl apply: external rows **7570** = external seed
  **6346** + external OOS **1224**, with external silver **30**. Combined label surface **8272**;
  combined seed surface **6576**; positive bronze **6529**; OOS bronze **1696**;
  silver_confirmed **47**; projected **0**.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12** source
  records, **44** fingerprints, **41** ontology families, and **702** curated labels. Final focused
  critical suite passed **433 passed, 14 subtests passed in 2.94s**. APH/factory/leakage focused
  rerun passed **302 passed, 14 subtests passed** after correcting the EC surface. Registry size
  scan passed: manifest **4 KB**, shards **17M / 17M / 17M / 5.9M**, curated **500K**.
- Closeout snapshot: **2026-06-15T20:55:19Z**, elapsed about **75.0** minutes, remaining **-20.0**
  minutes. The overrun was caused by a full-window UniProt preview attempt that was interrupted
  while waiting on slow entry fetches, followed by the necessary EC correction.
- Next concrete action: do **not** apply the 17-row APH preview. Current reviewed Swiss-Prot APH
  supply is too small for the >=150 gate after the corrected source wall. Pivot to higher-yield
  mechanism-first source strategy: build a source wall for `short_chain_dehydrogenase_reductase` /
  `aldo_keto_reductase` or another family/source tier that can plausibly clear >=150, refresh OOS
  preregistration if the fingerprint universe changes, preview non-destructively, audit rows,
  replay novelty/governor/dedup/cap gates, validate leakage/source contracts, then apply only if
  the batch gate is met.

## Session run - Metal-independent PDE 43fp infrastructure built; source handles subscale, no registry mutation (2026-06-15, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main` at `45be297288793783d0b8083d19d4323d628d9a71`, acquired the automation lock, and verified registry file-size safety: the external registry remains a sharded manifest plus shards about **17 MB / 17 MB / 17 MB / 5.9 MB**, below the GitHub-safe threshold. Frozen current702 stayed byte-unchanged at sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Built `metal_independent_phosphodiesterase` as the guarded 43rd positive fingerprint lane infrastructure, with no external bronze apply: new fingerprint `metal_independent_phosphodiesterase`, ontology family `metal_independent_phosphodiester_hydrolysis`, source runner `src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py`, script `scripts/source_metal_independent_phosphodiesterase_family.py`, deploy context, coverage/governor signature, high-yield-factory wiring, focused tests, tier-2 lane support, and the 43fp hard-negative preregistration `artifacts/v3_external_hard_negative_next_tranche_preregistration_43fp_1025.json`. The current positive universe is now `label_factory_v1_43fp` with **43** fingerprints and **40** ontology families.
- Mechanism discipline was preserved. EC 3.1.4 / 4.6.1, protein-name, keyword, and source/query handles are scope/admission context only. Metal absence is a boundary filter, not evidence. Tier-2 unreviewed rows require `source_tier_2` and the stricter independent mechanism-axis gate. `predictive_evidence` remains `[]` for generated rows, and no frozen current702 labels were written.
- Reviewed UniProt PDE preview was clean but subscale: `artifacts/v3_metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.json` / `work/metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.md` fetched **265** rows, produced **18** target mechanism-corroborated labels, admitted only **14** novelty-safe rows, held **52** off-target rows, and left **183** `no_mechanism_corroboration` holds. No apply was performed.
- Additional source-handle probes did not unlock the lane. Alternate reviewed handles fetched **130** rows with **0** target / **0** admitted labels (`artifacts/v3_metal_independent_phosphodiesterase_alternate_handle_preview_current702_20260615.json`). Tier-2 PDE count scouts were large, but the live tier-2 preview fetched **400** rows with **0** target labels, **0** admits, **186** off-target holds, and **197** `trust_tier_corroboration_insufficient` holds (`artifacts/v3_metal_independent_phosphodiesterase_tier2_sourcing_preview_cursor_pages2_size100_current702_20260615.json`). Do not pad or apply the 14-row reviewed preview.
- Planning refreshes after 43fp infrastructure: `artifacts/v3_coverage_redundancy_audit_current702_20260615_post_pde_43fp_infra.json`, `artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_pde_43fp_infra.json`, `artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_pde_43fp_infra.json`, and `work/metal_independent_phosphodiesterase_43fp_source_strategy_current702_20260615.md`. Coverage reports **8272** combined labels, fingerprint Gini **0.1974**, `metal_independent_phosphodiesterase` as the lone hole/under-floor fingerprint, and only `metal_dependent_hydrolase` over cap. Novelty replay reports **7109** admit / **414** throttle / **47** reject across **7570** expansion rows. The high-yield factory now reports **0** ready existing lanes >=150 and no high-yield blocked lanes; top projected clean admits under current handles is `short_chain_dehydrogenase_reductase` at **84**.
- Honest counters are unchanged from the prior N-ribosyl apply: external rows **7570** = external seed **6346** + external OOS **1224**, with external silver **30**. Combined label surface **8272**; combined seed surface **6576**; positive bronze **6529**; OOS bronze **1696**; silver_confirmed **47**; projected **0**.
- Validation: preflight `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12** source records, **42** fingerprints, **39** ontology families, and **702** curated labels. Post-change validate passed with **12** source records, **43** fingerprints, **40** ontology families, and **702** curated labels. Focused affected suite passed **350 passed in 3.15s**. The first full-suite attempt found two stale universe pins; after updating them for 43fp, the exact failed tests passed **2 passed in 0.38s** and the final full suite passed **2326 passed, 1 warning in 165.71s**. `tests/test_progress.py tests/test_doc_reference_check.py` passed **5 passed**. `git diff --check`, JSON parsing of progress/new artifacts, registry file-size scan, frozen SHA check, and live-preregistration consistency check all passed.
- Closeout snapshot: **2026-06-15T19:29:22Z**, elapsed **50.3** minutes, remaining **4.7** minutes.
- Next concrete action: stop retrying the same PDE UniProt handles for mass growth. Either design a materially sharper PDE source split, or pivot to a higher-yield source-handle/source-tier strategy such as SDR/AKR with a family-specific mechanism-first source wall, fresh OOS preregistration if the fingerprint universe changes, non-destructive preview, row guardrail audit, novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit apply only if the batch gate is met.

## Session run - N-ribosyl hydrolase cursor batch applied; next lane reset to metal-independent PDE (2026-06-15, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main`, acquired the automation lock, and
  verified registry file-size safety after apply: the external registry remains a sharded manifest
  plus shards about **17 MB / 17 MB / 17 MB / 5.9 MB**, below the GitHub-safe threshold. Frozen
  current702 stayed byte-unchanged at sha
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Implemented the missing reliable UniProt source path for `n_ribosyl_hydrolase`: added
  Link-header cursor pagination in `src/catalytic_earth/adapters.py`, added
  `--use-query-cursor-pagination` / `--query-pages-per-lane` to
  `scripts/source_n_ribosyl_hydrolase_family.py`, and fixed the process timeout wrapper so large
  child-process payloads are read before join instead of falsely timing out.
- Applied an N-ribosyl bronze batch through the gated path. Cursor preview
  `artifacts/v3_n_ribosyl_hydrolase_sourcing_preview_cursor_synonym_pages5_size40_current702_20260615.json`
  fetched **200** reviewed rows, found **181** target mechanism-corroborated labels, admitted
  **150** novelty-safe rows, and held **31** at cap. Row audit
  `artifacts/v3_n_ribosyl_hydrolase_row_guardrail_audit_current702_20260615_cursor_synonym_pages5_size40.json`
  audited all **150** admitted rows with **0** problem rows. Explicit reuse-preview apply appended
  **150** rows, skipped **0** duplicates, changed external registry **7420 -> 7570**, and changed
  combined label surface **8122 -> 8272**.
- Mechanism discipline stayed intact. EC 3.2.2 remains scope/fetch context only; nucleosidase
  synonyms remain scope/admission-only excluded context; `predictive_evidence` remains `[]`.
  Counted source-tier axes for the applied rows are non-EC domain/family plus Rhea
  reaction/participant evidence.
- After fetching, `origin/main` had advanced to `cd8f2da7` with the representation-separability
  restore, so the work was rebased before commit. The post-rebase full suite initially found a
  real representation failure: N-ribosyl Rhea equations produced D-ribose/ribose-5-phosphate plus
  nucleobase, but the source-free reaction-center feature space had no N-glycosidic class, pulling
  some rows into the zero-feature hydrolase bucket. Added `bc_n_glycosidic_hydrolysis`, derived
  only from Rhea substrate/product strings. Real-registry representation self-consistency is now
  **0.7598**; `n_ribosyl_hydrolase` **0.9933**; carbohydrate `glycoside_hydrolase` **0.8133**.
- Honest counters are now: external rows **7570** = external seed **6346** + external OOS
  **1224**, with external silver **30**. Combined label surface **8272**; combined seed surface
  **6576**; positive bronze **6529**; OOS bronze **1696**; silver_confirmed **47**; projected
  **0**.
- Post-apply planning refreshes:
  `artifacts/v3_coverage_redundancy_audit_current702_20260615_post_n_ribosyl_apply.json`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_n_ribosyl_apply.json`, and
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_n_ribosyl_apply.json`.
  Coverage reports **8272** combined labels, fingerprint Gini **0.1783**, no holes/under-floor
  fingerprints, and only `metal_dependent_hydrolase` over cap. Novelty replay reports **7109**
  admit / **414** throttle / **47** reject across **7570** external rows. The factory reports
  **0** ready existing lanes >=150; next lane is `metal_independent_phosphodiesterase` with
  projected clean admits **150**.
- Added next-lane readiness note
  `work/metal_independent_phosphodiesterase_43fp_readiness_current702_20260615_post_n_ribosyl_apply.md`.
  Also wrote bounded source-wall scout
  `artifacts/v3_metal_independent_phosphodiesterase_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`
  / `work/metal_independent_phosphodiesterase_source_wall_scout_current702_20260615_post_n_ribosyl_apply.md`:
  **68** fetched rows, **1** target mechanism-corroborated/novelty-admitted preview label, **0**
  fetch failures. Treat this as a warning that the 43fp runner needs better lane splits/source
  handles than the broad first windows. Count scout
  `artifacts/v3_metal_independent_phosphodiesterase_source_handle_count_scout_current702_20260615_post_n_ribosyl_apply.json`
  found better candidate handles for the future runner:
  `ec_3_1_4_catalytic_cyclic_amp_gmp` (**121**), `phosphodiesterase_hydrolase_non_metal_keyword`
  (**224**), and `ec_3_1_4_act_or_binding_site` (**718**). `ec_4_6_1` has high count (**1389**)
  but looks cyclase-boundary-heavy. Targeted source-wall scout
  `artifacts/v3_metal_independent_phosphodiesterase_targeted_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`
  fetched **157** rows from the two better handles but still produced only **13** target /
  **11** novelty-admitted preview labels, with **0** fetch failures. Cursor source-wall scout
  `artifacts/v3_metal_independent_phosphodiesterase_cursor_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`
  / `work/metal_independent_phosphodiesterase_cursor_source_wall_scout_current702_20260615_post_n_ribosyl_apply.md`
  fetched **244** cursor-paged rows from active/binding-site, hydrolase non-metal, and
  cyclic-nucleotide name handles, but still produced only **18** target / **14** novelty-admitted
  preview labels. Do not apply from the preview-only source wall. The next
  mutation must be the full 43fp path: fingerprint + ontology node, 43fp OOS preregistration before
  candidate selection, runner with sharper source handles, preview, row audit,
  novelty/governor/dedup/cap replay, tests, and explicit apply.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12** source
  records, **42** fingerprints, **39** ontology families, and **702** curated labels. Focused
  affected suites passed, including representation/leakage **235 passed, 14 subtests passed**.
  Final post-rebase full suite passed **2315 passed, 1 warning, 244 subtests passed in 167.24s**.
  `git diff --check`, JSON parsing, progress-log parsing, and registry file-size scan were clean.
- Next concrete action: build `metal_independent_phosphodiesterase` as the 43rd fingerprint through
  the full gated path, but improve source splits beyond the tested broad/targeted/cursor handles
  before expecting an apply-sized preview. Do not continue N-ribosyl as a growth lane now that it is
  capped at 150.

## Session run - N-ribosyl hydrolase 42fp infrastructure built; aggregate blocked below batch gate (2026-06-15, Codex automation)

- Hard blockers stayed clear. Started from current `origin/main`, acquired the automation lock, and
  verified registry file-size safety: external bronze remains a sharded manifest plus shards about
  **17 MB / 17 MB / 17 MB / 4.9 MB**, below the GitHub-safe threshold. Frozen current702 remains
  byte-unchanged at sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
  No external bronze labels were applied and no frozen current702 rows were written.
- Built `n_ribosyl_hydrolase` as the first 42nd positive fingerprint lane through the guarded
  path: new fingerprint `n_ribosyl_hydrolase`, ontology family `n_glycosidic_bond_hydrolysis`,
  reviewed-UniProt source runner `src/catalytic_earth/n_ribosyl_hydrolase_sourcing.py`, script
  `scripts/source_n_ribosyl_hydrolase_family.py`, focused tests, high-yield-factory wiring, deploy
  context, governor/coverage signatures, and the 42fp hard-negative preregistration
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_42fp_1025.json`. The current
  positive universe is now `label_factory_v1_42fp`.
- Mechanism discipline was preserved. EC 3.2.2 stays scope/fetch context only. Counted
  corroboration for `n_ribosyl_hydrolase` requires mechanism-bearing non-EC evidence such as
  N-ribosyl/nucleosidase family/name context plus N-glycosidic hydrolysis Rhea/reaction participant
  evidence. Added synonym handles (`nucleosidase`, `uridine nucleosidase`, `purine nucleosidase`,
  `N-ribohydrolase`, `nucleoside N-ribohydrolase`) as scope/admission handles only; they stay in
  excluded/review-only context and `predictive_evidence` remains `[]`.
- Non-destructive live previews show the lane is useful but not apply-ready. Initial source windows
  were low yield; synonym-expanded windows reached **61** unique novelty-safe
  `n_ribosyl_hydrolase` labels after aggregate dedup/novelty/cap replay. Row guardrails found
  **0** problem rows, but the aggregate is below the **150** clean-admit batch gate. The
  apply-candidate-named files were corrected in place to status
  `non_destructive_aggregate_blocked_below_150_no_apply` /
  `row_guardrails_pass_but_batch_gate_blocks_apply`; do not apply them.
- Key artifacts:
  `artifacts/v3_n_ribosyl_hydrolase_source_handle_scout_current702_20260615.json`,
  `artifacts/v3_n_ribosyl_hydrolase_sourcing_preview_aggregate_synonyms_current702_20260615.json`,
  `artifacts/v3_n_ribosyl_hydrolase_row_guardrail_audit_current702_20260615_synonym_aggregate.json`,
  `work/n_ribosyl_hydrolase_synonym_aggregate_blocker_current702_20260615.md`,
  `artifacts/v3_n_ribosyl_hydrolase_sourcing_preview_aggregate_current702_20260615_apply_candidate.json`,
  `artifacts/v3_n_ribosyl_hydrolase_row_guardrail_audit_current702_20260615_apply_candidate.json`,
  `work/n_ribosyl_hydrolase_apply_candidate_current702_20260615.md`, and
  `work/n_ribosyl_hydrolase_next_source_strategy_current702_20260615.md`. Offset-paged UniProt
  synonym windows produced a raw mechanism-corroborated window sum of **166**, but overlapped the
  earlier accession set and left only **61** unique labels; treat reliable cursor pagination or a
  stronger source path as the next source-handle task.
- Planning/coverage refresh after the 42fp infrastructure:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_n_ribosyl_infra.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260615_post_n_ribosyl_infra.json`, and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_n_ribosyl_infra.json`.
  Coverage reports **8122** combined labels, fingerprint Gini **0.2005**, `n_ribosyl_hydrolase`
  as the lone under-floor/hole, and `metal_dependent_hydrolase` over cap. Novelty replay remains
  **6959** admit / **414** throttle / **47** reject across **7420** external rows.
- Honest counters are unchanged from the prior Ser/Thr apply: external rows **7420** = external
  seed **6196** + external OOS **1224**, with external silver **30**. Combined label surface
  **8122**; combined seed surface **6426**; positive bronze **6379**; OOS bronze **1696**;
  silver_confirmed **47**; projected **0**.
- Validation so far: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with **12**
  source records, **42** mechanism fingerprints, **39** ontology families, and **702** curated
  labels. Focused affected suite passed: **14 passed** across N-ribosyl sourcing, source-wall
  boundary controls, 42fp/41fp OOS preregistration checks, factory import gate, and newest
  governor signatures. Final full-suite/JSON/diff/file-size results are recorded in
  `work/status.md` at closeout.
- Next concrete action: do **not** apply the 61-row aggregate. First implement reliable UniProt
  cursor pagination or another reviewed mechanism-bearing source path for N-ribosyl hydrolase, then
  rebuild a non-destructive aggregate and apply only if >=150 clean unique rows pass novelty,
  governor, dedup, cap, source-contract, leakage, and row guardrail gates. If N-ribosyl source
  supply is exhausted, pivot to `metal_independent_phosphodiesterase` as the next new-fingerprint
  lane with a fresh fingerprint-universe preregistration.

## Session run - Discovery-compass source walls ready; registry unchanged (2026-06-15, Codex automation)

- Hard blockers stayed clear. Fetched/rebased onto current `origin/main` at start, acquired the
  automation lock, and verified registry file-size safety: external bronze remains a sharded
  manifest plus shards about **17 MB / 17 MB / 17 MB / 4.9 MB**, below the GitHub-safe threshold.
  `PYTHONPATH=src python -m catalytic_earth.cli validate` passed at preflight with **12** source
  records, **41** fingerprints, **38** ontology families, and **702** curated labels. No labels,
  fingerprints, ontology nodes, or registries were written; frozen current702 remains sha
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Implemented preview-only source-wall rules for the two top discovery-compass high-yield lanes:
  `n_ribosyl_hydrolase` and `metal_independent_phosphodiesterase` in
  `src/catalytic_earth/external_cofactor_ec_disambiguation.py`. EC 3.2.2 / 3.1.4 / 4.6.1 remain
  scope/fetch context only and never count as corroborators. N-ribosyl rows require non-EC family
  text plus N-glycosidic hydrolysis reaction evidence and hold O-glycosidase, phosphorylase,
  kinase, transferase, EC-only, and multi-signal rows. Metal-independent phosphodiesterase rows
  require non-EC phosphodiesterase family text plus hydrolytic phosphodiester/cyclic-nucleotide
  reaction evidence; metal presence is a hold/filter, not metal absence counted as evidence.
- Refreshed the high-yield lane factory:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260615_discovery_compass.json` and
  `work/high_yield_family_lane_factory_current702_20260615_discovery_compass.md`. It ranks **14**
  candidates, has **0** ready existing lanes >=150, and now marks the top two lanes as
  `blocked_new_fingerprint_oos_prereg_and_runner_required` with
  `source_wall_rule_status=implemented_preview_only`: `n_ribosyl_hydrolase` (**1991** reviewed
  non-EC-corroborated supply, projected **150**) and `metal_independent_phosphodiesterase`
  (**1129** supply, projected **150**).
- Added/updated design-only preregistrations:
  `artifacts/v3_n_ribosyl_hydrolase_lane_preregistration_current702_20260615_discovery_compass.json`
  and
  `artifacts/v3_metal_independent_phosphodiesterase_lane_preregistration_current702_20260615_discovery_compass.json`.
  Both explicitly prohibit registry mutation from the artifact and require fingerprint + ontology,
  OOS preregistration for the then-current fingerprint universe, source runner, bounded preview,
  row guardrail audit, novelty/governor/dedup/cap replay, tests, and explicit apply before labels
  can be admitted. `n_ribosyl_hydrolase` is the active first 42fp path; the phosphodiesterase
  lane must use the next-fingerprint universe if it follows N-ribosyl.
- Added next-lane build plan
  `work/n_ribosyl_hydrolase_42fp_build_plan_current702_20260615.md` with the exact source-wall
  contract, initial reviewed-UniProt lane queries, required 42fp OOS gate, and no-apply conditions.
  Added follow-on build plan
  `work/metal_independent_phosphodiesterase_nextfp_build_plan_current702_20260615.md` with the
  metal-boundary rule and no-apply conditions for the second 150-row candidate.
- Updated durable docs: `docs/project_state.md`, `docs/scaling_plan_to_10k.md`,
  `docs/decision_log.md`, `docs/discovery_and_de_novo_strategy.md`, and `docs/artifact_index.md`.
  The active next scaleout action is now `n_ribosyl_hydrolase` through the full gated 42fp path,
  not a low-yield SDR topup and not a direct apply from the source wall.
- Rebased over upstream commit `37b47be6`, which added
  `work/next_instance_representation_separability_fix_spec.md`. Treat that spec as an active
  constraint before more ester-hydrolase, phosphatase, or NAD-redox-subtype sourcing. It does not
  by itself block the planned N-ribosyl hydrolase lane, but it should stop follow-on
  phosphatase/ester/NAD scaleout until the representation fix is landed.
- Closeout validation: post-rebase focused source-wall/factory/leakage/trust-tier suite
  **298 passed, 14 subtests passed in 0.35s**; full suite before the docs/spec-only rebase
  **2298 passed, 1 warning, 244 subtests passed in 165.46s**; CLI validate passed with **12**
  source records, **41** fingerprints, **38** ontology families, and **702** curated labels; JSON
  artifact/progress-log parse, registry file-size scan, and `git diff --check` passed. Closeout
  snapshot: **2026-06-15T15:28:21Z**, elapsed **50.0** minutes, remaining **5.0** minutes.
  Commit/push target is direct `origin/main`; after clean synced push, release the active lock with
  `PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock --repo-root "$PWD" release --require-clean --require-no-merge --require-synced`.
- Next concrete action: build `n_ribosyl_hydrolase` as the first 42fp lane: add fingerprint and
  ontology node, refresh hard-negative OOS preregistration, implement the reviewed-UniProt source
  runner, run non-destructive preview + row guardrail audit, then apply only if novelty, governor,
  dedup, cap, source-contract, and leakage gates pass.

## Session run - Representation separability restore landed (2026-06-15)

- Implemented `work/next_instance_representation_separability_fix_spec.md` in
  `src/catalytic_earth/mechanism_representation_loop.py` + `tests/test_mechanism_representation_loop.py`.
  Representation code only â€” NO registry write; frozen current702 stayed byte-unchanged and
  `python -m catalytic_earth.cli validate` reports 702 / 41 fp.
- Added four leakage-safe reaction-center classes, each derived ONLY from the Rhea
  substrate->product equation (never EC/name/prose/fingerprint/fold):
  - `bc_ester_hydrolysis` (BOND_CHANGE_CLASSES) â€” ester/lipase C-O hydrolysis -> alcohol +
    fatty acid/carboxylate; excludes NAD(P) aldehyde-DH, `[protein]` substrates, and free-phosphate
    products. Tokenizes RHS on Rhea's ` + ` separator (`\s\+\s`) so charged ions stay intact.
  - `bc_glycoside_hydrolysis` (BOND_CHANGE_CLASSES) â€” O-/N-glycoside hydrolysis -> free sugar +
    aglycone; also gives `glycoside_hydrolase` its defining feature so it stops spuriously firing
    `bc_carbon_carbon_lyase`.
  - `bc_aldehyde_oxidation` (NONHYDROLYTIC_BOND_CLASSES) â€” water-consuming NAD redox
    (aldehyde + NAD(+) + H2O -> carboxylate + NADH), separating aldehyde-DH from generic NAD redox.
  - reused `acc_protein` on protein dephosphorylation (no new dim) â€” distinguishes
    `ser_thr_protein_phosphatase` from small-molecule `metallophosphomonoesterase`.
- Measured on the live sharded registry (6196 seed labels): overall leave-one-out
  self-consistency **0.713 -> 0.7542** (matches the measure-first prototype exactly). Per family:
  `alpha_beta_hydrolase_esterase_lipase` 0.20 -> 0.68, `glycoside_hydrolase` 0.50 -> 0.81,
  `nad_p_dehydrogenase` 0.55 -> 0.96 (aldehyde-DH stays ~0.99), `ser_thr_protein_phosphatase`
  0.00 -> 0.875. Minor accepted: `had_like_phosphatase` ~0.95 (>0.9), `metallophosphomonoesterase`
  0.24 (<0.4, a separate metal-phosphatase-cluster follow-up).
- Re-baselined the relaxed real-registry test assertions UP to the validated reality
  (LOO > 0.74; nad_p > 0.9; aldehyde-DH >= 0.95; +floors for alpha_beta > 0.6, glycoside > 0.8,
  ser_thr > 0.8). Added classifier unit tests (positive + negative) for each new class.
- DOCUMENTED principled ceiling (NOT hacked back): `ser_his_acid_hydrolase` 0.91 -> 0.67 â€” both
  alpha/beta-hydrolases and Ser-His acid hydrolases are Ser-His-Asp serine esterases, so
  `bc_ester_hydrolysis` correctly fires for both; the residual split is FOLD-level. Test asserts
  > 0.6 with the rationale in a comment.
- Closed governor coverage gap: registered `ser_thr_protein_phosphatase` (one of 41/42 missing)
  in `coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES` (EC 3.1.3.16/48, scope-only).
- Full offline suite: same known baseline failures as clean tree (env-only: mmseqs / esm2 /
  toy sequence-head backends), no NEW regressions; `git diff --check` clean.

## Session run - Ser/Thr protein phosphatase bronze batch applied (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start; registry safety
  remains green after apply. `data/registries/external_bronze_labels.json` is still a small
  sharded manifest, shard files are about **17 MB / 17 MB / 17 MB / 4.9 MB**, and frozen current702
  stayed sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Fixed the Ser/Thr source-wall representation gap that held valid curated reactions. The rule now
  recognizes Rhea/UniProt protein-substrate forms such as
  `O-phospho-L-seryl-[protein] + H2O = L-seryl-[protein] + phosphate` and the threonyl analog as
  reaction-participant evidence. EC remains scope-only and is still not a counted corroborator.
- Replayed contiguous bounded Ser/Thr windows after the fix:
  `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window00_10_post_rhea_token_fix_current702_20260614.json`
  through
  `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_window220_260_post_rhea_token_fix_current702_20260614.json`.
  Aggregate artifact
  `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_aggregate_current702_20260614_post_rhea_token_fix.json`
  combined **743** fetched candidate rows, **170** unique mechanism-corroborated Ser/Thr
  candidates, **58** novelty-throttled/rejected rows, **2** off-target metallophosphomonoesterase
  holds, and **112** novelty-safe admitted rows. Row guardrail audit
  `artifacts/v3_ser_thr_protein_phosphatase_row_guardrail_audit_current702_20260614_post_rhea_token_fix.json`
  audited all **112** labels with **0** problems.
- Applied the aggregate with frozen SHA checks: external registry **7308 -> 7420**; combined label
  surface **8010 -> 8122**. Honest counters now: external rows **7420** = external seed **6196**
  + external OOS **1224**, with external silver **30**. Combined seed surface **6426**; combined
  OOS **1696**; positive bronze **6379**; silver_confirmed **47**; projected **0**.
- Post-apply refreshes: coverage audit reports **8122** combined labels, no holes, fingerprint Gini
  **0.1807**, and only `metal_dependent_hydrolase` over cap. Novelty replay reports **6959**
  admit / **414** throttle / **47** reject across **7420** external rows. High-yield factory now
  reports **0** ready existing lanes >=150; top projected clean admits is **84** for
  `short_chain_dehydrogenase_reductase`, captured as design-only preregistration
  `artifacts/v3_short_chain_dehydrogenase_reductase_lane_preregistration_current702_20260614_post_ser_thr_apply.json`.
  Evidence-handle scout
  `artifacts/v3_evidence_handle_expansion_current702_20260614_post_ser_thr_apply.json` reports
  **4/6** handle-blocked families unlocked and reachable positive-bronze uplift **741**. Breadth
  feasibility scout
  `artifacts/v3_breadth_feasibility_scout_current702_20260614_post_ser_thr_apply.json` projects
  reviewed Swiss-Prot clean-only positive bronze to **9067**, leaving a **933** positive gap; it
  concludes 10k diverse positive bronze is **not** reachable from reviewed Swiss-Prot alone.
- Quality refresh: bronze->silver preview reports **202** silver-ready pending geometry rows,
  **1742** chemistry-disagree holds, and **1779** low-cohesion holds. Ser/Thr contributes **112**
  chemistry-disagree holds under the current source-free representation and **0** low-cohesion
  holds. Silver geometry audit/run preview found **108** runnable rows, **0** passes, **108** holds,
  and **94** blocked before geometry. Full residue-mapping preview
  `artifacts/v3_silver_pdb_residue_mapping_current702_20260614_post_ser_thr_apply_full_preview.json`
  mapped **0** rows; blockers are **82** missing mmCIF alignment tables, **4** no exact residues,
  and **116** no residue positions mapped. Holo-coordinate reuse preview verified all **202**
  silver-ready rows already have local holo coordinates. Targeted Ser/Thr PDB-ID preview queried
  **99** missing-PDB accessions and found **0** new UniProt xrefs; broader limit-150 PDB preview
  also backfilled **0** rows. **13/112** Ser/Thr rows already had PDB IDs.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (**12** source
  records, **41** fingerprints, **38** ontology families, **702** curated labels); focused affected
  suite **324 passed, 14 subtests passed**; final full suite **2293 passed, 1 warning, 244 subtests
  passed in 165.28s**; registry file-size scan, JSON parse, and diff checks are part of closeout.
- Next concrete action: do not continue Ser/Thr as a mass-growth lane without improved novelty
  handles; only **38** cap room remains and the last window was mostly novelty-throttled. Improve
  source handles or external sources for a >=150 lane; SDR is the current design-only top candidate
  at **84** projected clean admits. In parallel, continue silver residue mapping/geometry
  representation work for the 202 pending silver-ready rows.

## Session run - Ser/Thr protein phosphatase runner built; live sourcing blocked (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start; the external
  registry remained sharded and GitHub-safe. No external bronze rows were applied and frozen
  current702 stayed sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Implemented the guarded `ser_thr_protein_phosphatase` lane as the 41st positive fingerprint:
  `src/catalytic_earth/ser_thr_protein_phosphatase_sourcing.py`,
  `scripts/source_ser_thr_protein_phosphatase_family.py`, new fingerprint
  `ser_thr_protein_phosphatase`, ontology family
  `dinuclear_metal_phosphoprotein_dephosphorylation`, disambiguation/source-wall rules, focused
  tests, and OOS preregistration
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_41fp_1025.json`.
  EC 3.1.3.16/48 is scope only; counted corroboration requires protein-phosphatase family/name,
  dinuclear metal/cofactor/binding-site context, and phosphoprotein dephosphorylation reaction
  evidence. HAD-like phosphatase, Cys-PTP/DSP/PTEN, small-molecule phosphatase, kinase,
  transferase, phosphodiesterase/nuclease, side-EC, EC-only, and multi-fingerprint rows stay held.
  `predictive_evidence` remains empty.
- Live sourcing did **not** apply rows. Full, 20-row, 5-row, and 1-row previews stalled in UniProt
  REST reads and were interrupted before writing preview artifacts. A new timeout option was added
  to the Ser/Thr runner. Timeout-bounded windows
  `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_timeout_window00_current702_20260614.json`
  through
  `artifacts/v3_ser_thr_protein_phosphatase_sourcing_preview_timeout_window12_14_current702_20260614.json`
  completed non-destructively: **11** windows covering offsets 0-14, **13** fetched candidate rows,
  **0** target mechanism-corroborated rows, **13** `no_mechanism_corroboration` holds, **0**
  novelty-admitted rows, and **26** fetch failures. Durable blocker:
  `work/ser_thr_protein_phosphatase_live_sourcing_blocker_current702_20260614.md`.
- Refreshed planning/quality artifacts without registry mutation:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_ser_thr_runner.json`
  now reports **1** ready existing lane (`ser_thr_protein_phosphatase`) with projected clean admits
  **150** and no blocked high-yield lanes. Coverage remains **8010** combined labels, fingerprint
  Gini **0.1807**, no holes/under-floor fingerprints, and only `metal_dependent_hydrolase` over cap.
  Novelty replay remains **6847** admit / **414** throttle / **47** reject across **7308** external
  rows.
- Quality refresh: bronze->silver preview reports **202** silver-ready pending geometry rows,
  **1630** chemistry-disagree holds, and **1779** low-cohesion holds. Silver geometry audit reports
  **108** runnable / **94** blocked rows, and the non-destructive geometry confirmation run scored
  **108** ready rows with **0** passes and **108** holds. Chemistry-disagree and cohesion summaries
  were written as review-only artifacts; no demotions, threshold relaxations, or silver flips.
- Validation so far: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (**12** source
  records, **41** fingerprints, **38** ontology families, **702** curated labels); focused
  Ser/Thr/disambiguation/leakage/factory/critical registry suite **305 passed, 14 subtests
  passed**; full suite initially found two stale 41fp count/list pins, both patched and direct
  rerun **2 passed**. Final full-suite result is recorded in `work/status.md`.
- Next concrete action: rerun the Ser/Thr protein phosphatase preview with stable UniProt REST
  access, preferably using `--fetch-timeout-seconds` and bounded windows; aggregate only completed
  previews, run a row guardrail audit, and apply only if the mechanism-first gates pass. If UniProt
  remains unstable, implement a repo-supported batch entry fetch/cache path before sourcing.

## Session run - Alpha/beta hydrolase esterase/lipase bronze lane applied (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start; the external
  registry remained sharded and GitHub-safe after apply. `data/registries/external_bronze_labels.json`
  is still a small manifest, shard files are about **17 MB / 17 MB / 17 MB / 4.1 MB**, and frozen
  current702 stayed sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Implemented and applied the guarded `alpha_beta_hydrolase_esterase_lipase` lane:
  `src/catalytic_earth/alpha_beta_hydrolase_esterase_lipase_sourcing.py`,
  `scripts/source_alpha_beta_hydrolase_esterase_lipase_family.py`,
  `tests/test_alpha_beta_hydrolase_esterase_lipase_sourcing.py`, new fingerprint
  `alpha_beta_hydrolase_esterase_lipase`, ontology family
  `ser_his_acid_ester_hydrolysis`, and the `label_factory_v1_40fp` OOS preregistration artifact
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_40fp_1025.json`.
  EC 3.1.1 is scope only; counted corroboration requires non-EC family/domain text,
  Ser-His-Asp/Glu active-site context, and Rhea ester-hydrolysis evidence. Protein names, EC,
  source prose, and target lane handles stay excluded/review-only context; `predictive_evidence`
  stays empty.
- Bounded sourcing used twenty 20-record windows from the reviewed UniProt lane and aggregated only
  novelty-safe rows. The aggregate preview
  `artifacts/v3_alpha_beta_hydrolase_esterase_lipase_sourcing_preview_aggregate_current702_20260614.json`
  combined **795** fetched rows, found **161** unique target mechanism-corroborated rows, capped
  **150** admitted rows, cap-trimmed **1**, and throttled **10**. Aggregate row guardrail
  `artifacts/v3_alpha_beta_hydrolase_esterase_lipase_row_guardrail_audit_current702_20260614_aggregate.json`
  audited all **150** rows with **0** problems.
- Apply result: external rows **7158 -> 7308**; combined label surface **7860 -> 8010**. Honest
  counters now: external rows **7308** = external seed **6084** + external OOS **1224**, with
  external silver-confirmed **30**. Combined seed surface **6314**; combined OOS **1696**;
  positive bronze **6267**; OOS bronze **1696**; combined silver_confirmed **47**; projected **0**.
- Post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_post_alpha_beta_apply.json`
  reports **8010** combined labels, no holes/under-floor fingerprints, fingerprint Gini **0.1807**,
  and only `metal_dependent_hydrolase` over cap. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_post_alpha_beta_apply.json`
  reports **7308** expansion rows with decisions **6847** admit / **414** throttle / **47** reject.
  High-yield factory
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_alpha_beta_apply.json`
  finds no existing lane with >=150 cap room and selects `ser_thr_protein_phosphatase` as the next
  new-fingerprint runner to build.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (**12** source
  records, **40** fingerprints, **37** ontology families, **702** curated labels); focused
  count-sensitive suite **27 passed**; alpha/beta/disambiguation/ontology/leakage suite
  **281 passed**; critical registry/import/admission suite **48 passed**. Full-suite result is
  recorded in `work/status.md` after closeout validation.
- Next concrete action: build `ser_thr_protein_phosphatase` as a new guarded fingerprint/source
  runner: ontology node, mechanism disambiguation rule, 41fp OOS preregistration, row guardrail
  audit, preview, tests, then apply only if the mechanism-first gates and batch size hold. Continue
  silver geometry/PDB/chemistry-disagree quality lanes in parallel, but alpha/beta is now capped.

## Session run - ALDH bronze lane applied and 39fp OOS preregistration refreshed (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start; the external
  registry remained sharded and GitHub-safe after the apply. `data/registries/external_bronze_labels.json`
  is still a small manifest, shard files remain below the 45 MB safety scan threshold, and frozen
  current702 stayed sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Implemented and applied the guarded `aldehyde_dehydrogenase` lane:
  `src/catalytic_earth/aldehyde_dehydrogenase_sourcing.py`,
  `scripts/source_aldehyde_dehydrogenase_family.py`, `tests/test_aldehyde_dehydrogenase_sourcing.py`,
  new fingerprint `aldehyde_dehydrogenase`, ontology node
  `cys_thiohemiacetal_aldehyde_oxidation`, and the `label_factory_v1_39fp` OOS preregistration
  artifact `artifacts/v3_external_hard_negative_next_tranche_preregistration_39fp_1025.json`.
  EC 1.2.1 is scope only; counted corroboration requires non-EC mechanism axes such as ALDH
  family/domain, NAD(P) cosubstrate or binding-site context, Rhea aldehyde oxidation context, and
  catalytic Cys/Glu active-site evidence where available. `predictive_evidence` stays empty.
- Live preview/apply:
  `artifacts/v3_aldehyde_dehydrogenase_sourcing_preview_current702_20260614.json` /
  `work/aldehyde_dehydrogenase_sourcing_current702_20260614.md` fetched **264** rows, found
  **250** target mechanism-corroborated rows, admitted the capped **150** through dedup/novelty/cap
  gates, and held **3** off-target fingerprint matches. The frozen SHA was printed before and after
  apply and remained unchanged.
- Row guardrail audit:
  `artifacts/v3_aldehyde_dehydrogenase_row_guardrail_audit_current702_20260614.json` audited all
  **150** applied rows with **0** problems. All rows are UniProt namespace, tier `bronze`,
  `automation_curated`, source tier 0, novelty-admitted, and have `predictive_evidence: []`; all
  rows carry cofactor/cosubstrate, domain/family, and Rhea participant axes, and **148/150** also
  carry active-site/residue-role evidence.
- Apply result: external rows **7008 -> 7158**; combined label surface **7710 -> 7860**. Honest
  counters now: external rows **7158** = external seed **5934** + external OOS **1224**, with
  external silver-confirmed **30**. Combined seed surface **6164**; combined OOS **1696**;
  combined silver_confirmed **47**; projected **0**.
- Post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_post_aldehyde_dehydrogenase_apply.json`
  reports **7860** combined labels, no holes/under-floor fingerprints, fingerprint Gini **0.1835**,
  and only `metal_dependent_hydrolase` over cap. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_post_aldehyde_dehydrogenase_apply.json`
  reports **7158** expansion rows with decisions **6702** admit / **409** throttle / **47** reject.
  The high-yield factory now reports no existing lane with >=150 cap room and points to
  `alpha_beta_hydrolase_esterase_lipase` as the next new-fingerprint lane; design-only
  preregistration is
  `artifacts/v3_alpha_beta_hydrolase_esterase_lipase_lane_preregistration_current702_20260614_post_aldehyde_dehydrogenase_apply.json`.
- Bounded PDB quality lane: the full PDB-ID backfill preview was interrupted after a UniProt
  response hang and wrote no artifact. An ALDH-only preview
  `artifacts/v3_label_pdb_id_backfill_preview_aldehyde_dehydrogenase_current702_20260614.json`
  examined the **150** new ALDH rows: **27** already had PDB IDs, **123** UniProt accessions were
  queried, and **0** additional PDB xrefs were backfilled.
- Representation note: ALDH is internally coherent under the current source-free representation
  (**1.0** self-consistency), but it exposes a real NAD(P)-redox boundary: generic
  `nad_p_dehydrogenase` rows now split **82** to themselves and **68** to ALDH. Keep this as a
  leakage-safe feature/geometry design gap, not a reason to relax admission, cohesion, or silver
  thresholds.
- Validation: focused affected suite **107 passed**; exact full-suite failures after stale-pin
  refresh **8 passed**; final full suite **2272 passed, 1 warning, 244 subtests passed**;
  `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (**12** source records,
  **39** fingerprints, **36** ontology families, **702** curated labels); JSON parse checks and
  registry file-size scan passed.
- Next concrete action: build the `alpha_beta_hydrolase_esterase_lipase` runner from the
  preregistration artifact above, including fingerprint, ontology node, disambiguation rule, OOS
  preregistration/row guardrail tests, and preview before any apply. In parallel, continue explicit
  residue mapping for blocked silver-ready rows and address the ALDH/NAD(P) representation gap only
  with leakage-tested local chemistry/geometry features.

## Session run - HAD-like phosphatase source lane applied (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start; the external
  registry remains sharded and GitHub-safe after the apply. `data/registries/external_bronze_labels.json`
  is still a small manifest, shard max is ~18 MB, and no file under `data/registries/` exceeds
  the 45 MB safety scan threshold. Frozen current702 stayed sha
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Implemented the guarded HAD-like phosphatase lane:
  `src/catalytic_earth/had_like_phosphatase_sourcing.py`,
  `scripts/source_had_like_phosphatase_family.py`, `tests/test_had_like_phosphatase_sourcing.py`,
  new fingerprint `had_like_phosphatase`, ontology node
  `had_aspartyl_phosphoenzyme_hydrolysis`, and the `label_factory_v1_38fp` hard-negative
  preregistration artifact
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_38fp_1025.json`.
  EC 3.1.3 is scope only; counted corroboration requires mechanism axes such as HAD family/domain,
  Mg/Asp phosphoenzyme context, active/binding-site evidence, or Rhea phosphomonoester hydrolysis.
  `predictive_evidence` stays empty for the new rows.
- Live preview/apply:
  `artifacts/v3_had_like_phosphatase_sourcing_preview_current702_20260614.json` /
  `work/had_like_phosphatase_sourcing_current702_20260614.md` fetched **354** rows, found
  **147** target mechanism-corroborated bronze rows, admitted **146** through dedup/novelty/cap
  gates, and held **143** off-target metallophosphomonoesterase matches plus **8** disambiguation
  holds. The broader 500-record probe
  `artifacts/v3_had_like_phosphatase_broad500_sourcing_preview_current702_20260614.json` saturated
  at **145** admits, so the applied **146** is the current high-yield floor-scale result rather
  than a tiny top-up.
- Row guardrail audit:
  `artifacts/v3_had_like_phosphatase_row_guardrail_audit_current702_20260614.json` audited all
  **146** applied rows with **0** problems. All entry IDs are UniProt namespace; all rows are
  tier `bronze` and `automation_curated`; `predictive_evidence` is empty; mechanism axes counted
  were active-site/residue role **146**, cofactor/cosubstrate **146**, domain/family **146**, and
  Rhea participant/reaction **143**.
- Apply command appended **146** bronze rows to the external registry and preserved all frozen
  current702 bytes: external rows **6862 -> 7008**, combined label surface **7564 -> 7710**.
  Honest counters now: external rows **7008** = external positive bronze **5754** + external OOS
  bronze **1224** + external silver-confirmed **30**. Combined seed surface **6014**; combined
  positive bronze **5967**; combined OOS bronze **1696**; silver_confirmed **47**; projected **0**.
- Post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_post_had_like_apply.json` reports
  **7710** combined labels, no holes or under-floor fingerprints, fingerprint Gini **0.1891**, and
  only `metal_dependent_hydrolase` over cap. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_post_had_like_apply.json` reports
  **7008** expansion rows with decisions **6552** admit / **409** throttle / **47** reject. The
  refreshed high-yield factory
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_had_like_apply.json`
  finds no existing lane with >=150 cap room and selects `aldehyde_dehydrogenase` as the next
  new-family runner to build. Captured the design-only next-lane contract in
  `artifacts/v3_aldehyde_dehydrogenase_lane_preregistration_current702_20260614_post_had_apply.json`
  (3160 reviewed EC-scope rows, 3153 non-EC corroborated supply estimate, 150 projected clean
  admits; holds molybdopterin/flavin/generic NAD(P) aldehyde oxidoreductase confounds).
- Test/doc cleanup from the live count change: refreshed stale real-registry pins from
  6862/7564/37fp to 7008/7710/38fp with documented count rationale. The representation loop now
  records a real leakage-safe representation ceiling: HAD-like phosphatase is self-consistent
  (**0.9726**), but generic `metallophosphomonoesterase` rows often confuse into HAD under
  source-free reaction/cofactor/site features. This is a representation gap, not a reason to lower
  admission or silver thresholds.
- Validation: focused HAD/registry/leakage/source suite **326 passed**; targeted stale-pin suite
  **26 passed**; full suite **2262 passed, 1 warning in 162.56s**; `PYTHONPATH=src python -m
  catalytic_earth.cli validate` passed (**12** source records, **38** fingerprints, **35** ontology
  families, **702** curated labels); JSON parse checks passed for new artifacts; `git diff --check`
  passed; registry file-size scan passed.
- Next concrete action: build the `aldehyde_dehydrogenase` fingerprint/ontology/source runner from
  the preregistration contract above, then run a preview plus row guardrail audit before any apply.
  In parallel, continue explicit residue mapping for the **106** blocked silver-ready rows and
  treat the **124** runnable silver holds as geometry representation gaps.

## Session run - Silver geometry confirmation apply (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start; registry safety
  remains green after the tier flips: `data/registries/external_bronze_labels.json` is still a
  small sharded manifest and shard files remain below the 45 MB scan threshold (largest ~17 MB).
- Added and applied the separate silver geometry-confirmation lane:
  `src/catalytic_earth/silver_geometry_confirmation_run.py`,
  `scripts/run_silver_geometry_confirmation.py`, and
  `tests/test_silver_geometry_confirmation_run.py`. The lane consumes only rows that pass the
  existing silver runnability audit (sha-matched holo coordinate + explicit PDB residue mapping),
  builds local geometry features from those mmCIF files, runs the existing geometry retrieval and
  label-factory promotion rule, and writes only the external registry on explicit `--apply`.
  UniProt binding-site/prose roles, EC, Rhea, names, and source text are not scoring features.
- Real apply artifact:
  `artifacts/v3_silver_geometry_confirmation_run_current702_20260614_apply.json` /
  `work/silver_geometry_confirmation_run_current702_20260614_apply.md`. Input **260**
  silver-ready rows included **154** runnable rows; **152** local geometry rows were OK; **30**
  passed geometry confirmation and were flipped from bronze to silver; **124** runnable rows were
  held by the geometry/label-factory gate. Passing families: flavin dehydrogenase/reductase **12**,
  metallo-amidohydrolase/deaminase **17**, PLP-dependent enzyme **1**.
- Fixed the bronze->silver preview to exclude already silver-confirmed rows from the pending queue
  while retaining them in seed centroids/counts. Post-apply artifacts now report the pending state
  honestly: `artifacts/v3_silver_geometry_confirmation_audit_current702_20260614_post_geometry_apply.json`
  found **230** pending silver-ready rows = **124** still runnable + **106** blocked; and
  `artifacts/v3_silver_geometry_confirmation_run_current702_20260614_post_apply_pending.json`
  found **0** additional pass rows among the 124 remaining runnable holds.
- Honest counters after apply: external registry **6862** rows = external positive bronze **5608**
  + external OOS bronze **1224** + external silver-confirmed **30**. Combined label surface remains
  **7564**; combined seed surface remains **5868**; combined positive bronze **5821**; combined OOS
  bronze **1696**; combined silver_confirmed **47**; projected **0**. Frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Additional bounded quality/scaling artifacts from the same run:
  `artifacts/v3_label_pdb_id_backfill_preview_current702_20260614_post_silver_apply_remaining.json`
  closed the remaining PDB-ID preview surface (**4842** queried, **0** backfilled, **0** deferred);
  `artifacts/v3_bronze_silver_promotion_preview_current702_20260614_post_silver_apply.json`
  refreshed pending queues (**230** silver-ready, **1344** chemistry-disagree,
  **1759** low-cohesion); and
  `artifacts/v3_cohesion_threshold_calibration_current702_20260614_post_silver_apply.json`
  kept the global threshold unchanged while identifying **232** near-threshold low-cohesion holds
  for review-only calibration design.
- Refreshed planning/scout artifacts:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_silver_apply.json`,
  `artifacts/v3_evidence_handle_expansion_current702_20260614_post_silver_apply.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260614_post_silver_apply.json`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_post_silver_apply.json`, and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_post_silver_apply.json`.
  The high-yield factory still selects `had_like_phosphatase` as the next new-family lane; the
  design-only preregistration is
  `artifacts/v3_had_like_phosphatase_lane_preregistration_current702_20260614_post_silver_apply.json`.
  Fresh downstream eval design is documented at `docs/fresh_leakage_safe_downstream_eval_design.md`.
  Rhea/metal annotation backfill remains mutation-blocked until a row-level preview/apply writer
  exists; see `work/rhea_metal_annotation_backfill_blocker_current702_20260614_post_silver_apply.md`.
- Validation: focused critical/silver/source suite **302 passed, 23 subtests passed**; full suite
  **2252 passed, 1 warning, 244 subtests passed in 161.34s**; `python -m catalytic_earth.cli
  validate` passed; JSON parse checks passed for generated artifacts/registries; `git diff
  --check` passed; registry/coordinate file-size scan found no unsafe changed registry files.
- Next concrete action: build the `had_like_phosphatase` ontology/fingerprint/source runner from
  the preregistered guardrails, while continuing explicit PDB residue mapping for the **106** blocked
  pending silver-ready rows. Treat the **124** runnable-held rows as geometry
  representation/calibration gaps rather than silver.

## Session run - Silver coordinate materialization and explicit PDB residue mappings (2026-06-14, Codex automation)

- Hard blockers stayed clear. Local `main` matched fetched `origin/main` at start. The external
  registry remains sharded and GitHub-safe: `data/registries/external_bronze_labels.json` is a
  ~1.2 KB manifest, shard max is still ~17 MB, and no new registry/coordinate file exceeds 45 MB.
  New holo coordinate files under `artifacts/v3_silver_holo_coordinates_current702/` total ~243 MB
  with each file below the GitHub per-file safety threshold.
- Added sha-aware silver geometry runnability checks:
  `src/catalytic_earth/silver_geometry_confirmation.py` now requires any local coordinate file to
  match the `holo_pdb_confirmation.coordinate_sha256`; mismatched local PDB files no longer count
  as runnable geometry material.
- Added two bounded provenance lanes:
  `src/catalytic_earth/silver_holo_coordinate_materialization.py` /
  `scripts/materialize_silver_holo_coordinates.py` materialize only sha-verified local holo PDB
  mmCIFs for silver-ready rows, and
  `src/catalytic_earth/silver_pdb_residue_mapping.py` /
  `scripts/map_silver_pdb_residues.py` maps exact UniProt active-site positions to explicit PDB
  chain/residue positions only through mmCIF `_struct_ref_seq` +
  `_pdbx_poly_seq_scheme` alignment tables. Both write only external registry provenance on
  explicit `--apply`; frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; no tier changes; no
  predictive evidence changes.
- Applied silver materialization in bounded chunks. Reused 3 already-tracked sha-matching PDB files,
  then fetched/materialized bounded RCSB batches through the `fetch257` artifact. Verified local
  holo-coordinate rows moved **0/3 usable -> 260** (counting only files whose sha matches the
  recorded holo confirmation).
  `holo_confirmed` remains **260**; PDB-bearing rows remain **2020**.
- Applied explicit PDB residue mapping after each coordinate batch. Final mapping artifact
  `artifacts/v3_silver_pdb_residue_mapping_current702_20260614_post_fetch257_apply.json` mapped
  **40** newly updated rows and **380** exact residues in its final pass; current registry has
  **162** rows with
  `pdb_residue_mapping_provenance.status =
  pdb_residue_mapping_from_mmcif_struct_ref_seq`.
- Final silver audit:
  `artifacts/v3_silver_geometry_confirmation_audit_current702_20260614_post_fetch257_mapping.json`
  / `work/silver_geometry_confirmation_audit_current702_20260614_post_fetch257_mapping.md` found
  **154/260** rows ready for the separate geometry-confirmation run, **106** still blocked, and
  **0** silver flips. Remaining blockers: `missing_explicit_pdb_residue_mapping` **98** and
  `insufficient_exact_active_site_residues` **20**; the local-holo-coordinate blocker is cleared
  for the current 260-row silver-ready queue.
- Honest counters stayed separate: external registry **6862** rows = positive bronze **5638** +
  OOS bronze **1224**; all external rows still bronze; combined label surface **7564**; combined
  seed surface **5868**; silver_ready queue **260**; ready-for-geometry subset **154**;
  silver_confirmed tier count **17**; projected provisional **0**.
- Validation from this run: focused critical suite **291 passed, 14 subtests passed**; full suite
  **2248 passed, 1 warning, 244 subtests passed in 161.34s**. Final `validate`, JSON parse, and
  `git diff --check` results are recorded in `work/progress_log.jsonl`.
- Next concrete action: run or implement the separate geometry-confirmation gate for the **154**
  runnable rows and only promote rows that pass. In parallel, continue bounded holo-coordinate
  materialization + explicit mmCIF/SIFTS residue mapping for the remaining silver-ready queue.
  Once silver quality work is bounded, resume the high-yield new-family lane
  (`had_like_phosphatase` remains the top factory recommendation) without relaxing mechanism-first
  admission.

## Session run - Silver geometry blocker audit, PDB-ID scaleout, eval design (2026-06-14, Codex automation)

- Hard blockers rechecked and stayed clear. The external registry remains sharded and GitHub-safe:
  `data/registries/external_bronze_labels.json` is a ~1.2 KB manifest and the four shard files are
  still all below 18 MB after this run. The only >45 MB files are the same pre-existing artifacts
  from earlier work, not changed registry files.
- Added the missing non-destructive silver geometry confirmation audit:
  `src/catalytic_earth/silver_geometry_confirmation.py`,
  `scripts/audit_silver_geometry_confirmation.py`, and
  `tests/test_silver_geometry_confirmation.py`. It consumes the bronze->silver preview queue and
  requires recorded holo PDB confirmation, a local holo coordinate file, and explicit PDB
  chain/residue mappings before any row is considered runnable for the separate geometry gate.
  It deliberately does not run/fake geometry scoring and does not flip tiers.
- Live result:
  `artifacts/v3_silver_geometry_confirmation_audit_current702_20260614.json` /
  `work/silver_geometry_confirmation_audit_current702_20260614.md` found **260/260** silver-ready
  rows blocked before geometry confirmation, **0** runnable rows, and **0** silver flips.
  Blockers: `missing_explicit_pdb_residue_mapping` **260**, `missing_local_holo_coordinate_file`
  **259**, and `insufficient_exact_active_site_residues` **20**. This is the current silver
  blocker; UniProt sequence positions must not be treated as PDB residue mappings.
- Continued bounded UniProt PDB-ID backfill through the existing sharded writer. Applied chunks:
  `--limit 500` backfilled **187**, `--limit 1000` backfilled **332**, `--limit 2000` backfilled
  **203**, and a final `--limit 3000` probe backfilled **0** (no-yield; stopped). External rows
  with PDB IDs moved **1298 -> 2020** (+722 this run after the previous run's first chunk);
  row count stayed **6862**, frozen current702 sha stayed
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`, and
  `predictive_evidence` stayed unchanged. Holo confirmation was attempted on a bounded 150-row
  RCSB batch after the second chunk, but RCSB TLS/network stalls forced a clean interrupt before
  any registry apply; silver-ready remains **260**.
- Refreshed non-mutating planning artifacts:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_pdb_backfill.json`
  (top next lane: `had_like_phosphatase`, projected clean admits 150; no existing lane >=150),
  `artifacts/v3_breadth_feasibility_scout_current702_20260614_post_pdb_backfill.json`
  (reviewed Swiss-Prot alone projects **8509** positive bronze, gap **1491**),
  `artifacts/v3_evidence_handle_expansion_current702_20260614_post_pdb_backfill.json`
  (4/6 handle-blocked families unlocked; reachable positive-bronze uplift **741**), and
  `artifacts/v3_external_surface_eval_split_design_current702_20260614_post_pdb_backfill.json`
  (design only; no benchmark run).
- Current honest counters: external registry **6862** rows = positive bronze **5638** + OOS bronze
  **1224**; combined label surface **7564**; combined seed surface **5868**; remaining seed gap
  **4132**; PDB-bearing external rows **2020**; holo-confirmed rows **260**; silver-ready pending
  geometry **260**; silver_confirmed tier count still **17**; projected provisional **0**.
- Validation from this run: focused critical tests **233 passed, 14 subtests passed in 54.90s**;
  full suite **2241 passed, 1 warning, 244 subtests passed in 162.80s**; `python -m
  catalytic_earth.cli validate` passed; `git diff --check` passed. Final validation was rerun after
  the registry backfill/docs closeout as recorded in `work/progress_log.jsonl`.
- Next concrete action: do **not** flip any silver tiers until local holo PDB coordinates and
  explicit PDB chain/residue mappings exist for silver-ready rows. Build a SIFTS/PDB residue-mapping
  materialization lane for the 260 silver-ready rows, then rerun the silver geometry audit and only
  run/apply the geometry gate for rows that become runnable. For bronze growth, build the
  `had_like_phosphatase` fingerprint/source runner with mechanism-first disambiguation and OOS
  preregistration, or use the evidence-handle scout to widen non-EC admission handles without
  making them predictive features.
- Early-closeout rationale relative to the 55-minute automation window: remaining safe work is no
  longer a bounded apply/preview. Silver is blocked on SIFTS/PDB residue mapping + local holo
  coordinate materialization; the RCSB holo apply path hit TLS/network stalls and was interrupted
  before any write; large PDB-ID chunks reached a no-yield/no-xref wall; chemistry-disagree/cohesion
  lanes have no standalone fresh runner beyond the existing post-shard artifact; and the next
  high-yield bronze lane (`had_like_phosphatase`) requires a new fingerprint, OOS preregistration,
  mechanism disambiguation rule, row guardrail audit, and runner. Starting those in closeout would
  create unfinished shared-registry/fingerprint work.

## Session run - Registry sharding, full-suite recovery, PDB backfill lane (2026-06-14, Codex automation)

- Hard blocker cleared: `data/registries/external_bronze_labels.json` was ~54 MB and unsafe for
  continued GitHub growth. Added transparent sharded-registry support
  (`src/catalytic_earth/registry_io.py`) and rewired registry loaders/writers across import,
  validation, promotion, coverage, representation, trim, and backfill paths. The external registry
  is now a 1,203-byte manifest plus four shards (`part-00000..00003`, max 17,996,716 bytes),
  preserving all 6,862 labels and loader behavior.
- Full test suite checked as requested. Initial full run had 5 stale/expanded-universe failures
  (ATP/PfkA off-target accounting, EPK positive fingerprint count, geometry ablation top-k after
  37fp expansion, SDR inverse-gate missing-fingerprint list). Updated the assertions with measured
  rationale. Final post-backfill validation: focused changed-state tests **39 passed**; full suite
  **2238 passed, 1 warning, 244 subtests passed in 163.10s**; `python -m catalytic_earth.cli
  validate` OK; `git diff --check` OK.
- Bounded PDB-ID backfill lane added and applied: new
  `src/catalytic_earth/label_pdb_id_backfill.py`, `scripts/backfill_label_pdb_ids.py`, and
  `tests/test_label_pdb_id_backfill.py`. It copies curated UniProt `xref_pdb` IDs only into
  external `evidence.structure_provenance.pdb_ids`, records provenance, preserves row count/order,
  leaves `predictive_evidence` unchanged, refuses to target frozen current702, and writes through
  the sharded registry writer. Applied with `--limit 120`: queried 120 missing-PDB rows,
  backfilled **19**, already had PDB **1279**, without xref **101**, deferred **5463**; frozen
  current702 sha `5eec9bef...` identical before/after.
- Silver lane advanced but not overclaimed: post-PDB-backfill holo preview checked 50 rows and found
  **0** new holo confirmations; already confirmed remains **260** and silver remains
  `silver_ready_pending_geometry_run` only. No annotation-only silver flips; no tiers changed.
- New artifacts/reports:
  `artifacts/v3_bronze_silver_promotion_preview_current702_20260614_post_registry_shard.json`,
  `artifacts/v3_mechanism_representation_loop_current702_20260614_post_registry_shard.json`,
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_registry_shard.json`,
  `artifacts/v3_chemistry_disagree_triage_current702_20260614_post_registry_shard.json`,
  `artifacts/v3_pdb_id_backfill_scout_current702_20260614_post_registry_shard.json`,
  `artifacts/v3_label_pdb_id_backfill_preview_current702_20260614_post_registry_shard.json`,
  `artifacts/v3_holo_structure_promotion_preview_current702_20260614_post_pdb_backfill.json`,
  `artifacts/v3_breadth_feasibility_scout_current702_20260614_post_registry_shard.json`,
  and
  `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_current702_20260614_post_registry_shard.json`
  with matching `work/*.md` reports.
- Current honest counters: external registry **6862** rows = positive bronze **5638** + OOS bronze
  **1224**; combined label surface **7564**; combined seed surface **5868**; remaining seed gap
  **4132**; PDB-bearing external rows **1298**; holo-confirmed rows **260**; silver_confirmed
  tier count still **17**. Four pre-existing artifact blobs remain >45 MB, but no changed/new file
  exceeds 45 MB.
- Next concrete action: continue the PDB-ID backfill in bounded `--limit` chunks, then rerun holo
  confirmation. In parallel, implement the high-yield new-family runner recommended by the factory
  (`had_like_phosphatase`/aldehyde dehydrogenase only with mechanism-first disambiguation), and keep
  geometry-confirmation/tier flips separate from annotation-only evidence.

## Session run - First silver-ready rows via holo experimental-PDB confirmation (2026-06-14, Claude Code automation)

- MILESTONE: `silver_ready` 0 -> 109 for the first time. Diagnosis (measured, not guessed):
  the gate scores silver only on TRUE holo (annotated cofactor present in coordinates), but
  the registry's only staged coordinates are AlphaFoldDB predictions = inherently apo, so
  silver was stuck at 0. Of 5638 seed rows, 371 chemistry-corroborated, cofactor-defined rows
  carry experimental pdb_ids; a sample fetch confirmed 5/6 holo.
- Built `holo_structure_promotion` + `scripts/promote_holo_structures.py`: for each
  chemistry-corroborated row (the gate's own nearest-centroid + cohesion test) with
  experimental pdb_ids + an annotated cofactor, fetch the PDB mmCIF, test whether the cofactor
  HETATM is present (same test the gate uses), and record a sha-pinned
  structure_provenance.holo_pdb_confirmation. structure_confirmability honours that as holo.
  mmCIF regeneratable from the PDB id, NEVER committed (AFDB-backfill discipline). Candidate
  selection chemistry-only; structure stays review-only, never predictive.
- Applied in two passes (bounded `--per-fingerprint-cap 8`, then the full corroborated pool):
  260 holo confirmed across 24 fingerprints (~70-80% hit-rate; 111 candidates apo-only). Gate:
  silver_ready_pending_geometry_run 0->260; blocked_pending_structure 2534->2275; blocked_apo
  1->0; review 1344 / hold 1759 unchanged. HONEST: blocked_pending_structure (2275) still
  dominates (the ~5300 rows with no experimental PDB are not inflated), and silver_ready is
  *_pending_geometry_run -- the actual geometry-confirmation run is a SEPARATE authorized step.
  Label counts/tiers UNCHANGED (apply added only provenance; all bronze): expansion 6862,
  combined 7564, positive_bronze 5851, silver_confirmed 17; counters stay SEPARATE. New-label
  sourcing PAUSED during this work (same-file write conflict + 51 MB GitHub soft limit);
  resume only on a clean registry after this commits.
- Artifacts: `..._holo_structure_promotion_preview_current702.json`,
  `..._post_holo_confirmation.json` (+ work reports). New module + script + 8 offline unit
  tests; the honest_about_apo real-registry test re-baselined honestly (silver_ready > 0 from
  recorded holo, blocked_pending_structure dominant, geometry never faked).
- Guards: frozen sha (`5eec9befâ€¦`) printed identical before/after the apply; frozen NEVER
  written; mmCIFs never committed; validate ok (702 / 37 fp); `git diff --check` clean;
  leakage wall intact. data/cache/holo_pdb_hetatm_cache.json (git-ignored) makes re-runs
  resumable.
- Next: scale holo confirmation across the rest of the 371-row corroborated pool (rerun the
  script with a higher/zero per-fingerprint-cap; the cache makes it resumable), then run the
  SEPARATE authorized geometry-confirmation on the silver_ready queue to actually flip tiers
  to silver. RCSB egress confirmed reachable in this environment.

## Session run - C-C lyase / aldol separation (2026-06-14, Claude Code automation)

- Measure-first follow-on to the kinase separation. Both named frontiers were measured and
  found to be ceilings, NOT hacked: (A) fold-defined kinases = principled
  reaction-chemistry-overlap ceiling; (B) apo->holo silver promotion = data ceiling -- of
  5638 seed rows only 104 carry a coordinate file (103 apo, 1 holo) and 5534 have an
  unresolved `coordinate_path`, so the geometry gate genuinely abstains (no holo coordinates
  stageable offline; heldout one-shot already spent). silver_ready stays 0 honestly.
- The genuine, leakage-safe, non-fold gap: `class_ii_metal_aldolase` sat at leave-one-out
  0.013 despite 100% of its rows carrying a Rhea reaction. Root cause: class II metal
  aldolases carry only the shared divalent-metal cofactor + a C-C bond cleavage, and the
  feature space had NO C-C-cleavage class, so they collapsed into the generic metal cluster.
- Fix (Rhea-equation only): added `bc_carbon_carbon_lyase` -- fires when one organic substrate
  cleaves into two organic fragments (or the reverse), no water, no NTP anhydride. New
  `_organic_fragments` helper splits on Rhea ` + ` (keeps `NH4(+)`/`H(+)` intact) and drops
  inorganic leaving groups, so decarboxylation/dehydratase/deamination do NOT trip it (this
  also fixed an earlier-draft cobalamin regression caused by `+`-split shredding `NH4(+)`).
  Dims 35 -> 36.
- Result (LOO): overall 0.719 -> 0.755 expansion-only (frozen+exp 0.699 -> 0.7335).
  class_ii_metal_aldolase 0.013 -> 0.813; bonus metallophosphoesterase_nuclease 0.120->0.380,
  non_heme_iron_2og 0.872->0.972, coa 0.948->0.984, ThDP 0.733->0.787; cobalamin unchanged
  0.825 (no regression; worst -0.020). Promotion gate review_chemistry_disagrees 1572 -> 1344.
- Other low families left as documented ceilings (not hacked): metallopeptidase /
  metallophosphoesterase_nuclease dominated by `(no reaction)` rows (data ceiling);
  metal_racemase vs cofactor_independent_isomerase differ only by an under-annotated metal.
- Artifacts: `..._cc_lyase_aldolase_separation.json`, `..._post_cc_lyase_separation.json`
  (+ `work/*.md` reports). New classifier unit tests (positive + negative) and a
  class_ii_metal_aldolase separability lock. No registry written; frozen byte-unchanged
  (sha `5eec9befâ€¦`); validate ok (702 / 37 fp); `git diff --check` clean; leakage wall intact.
- Next (still open): both frontiers remain the documented ceilings. The next genuine
  representation lever would require new DATA, not features: holo coordinates for the silver
  gate, or Rhea reactions / metal annotations for the no-reaction metallopeptidase/nuclease
  and racemase rows. A sequence/structure (fold) axis for the fold kinases must stay strictly
  out of the predictive label basis if ever attempted.

## Session run - Kinase acceptor-specificity + ATP-ligation separation (2026-06-14, Claude Code automation)

- Follow-on to the cosubstrate/bond-change extension: separated the ATP-driven sub-cluster.
  Root bug: `bc_phosphoryl_transfer` only fired for protein kinase; other ATP->ADP kinases
  fired only generic divalent_metal and separated on residue noise, so pfkb/ghmp/
  atp_amide_ligase collapsed.
- Fix (leakage-safe, Rhea-equation only): corrected `bc_phosphoryl_transfer` (fires for any
  ATP->ADP transfer to an organic acceptor); added `bc_atp_dependent_ligation` (ATP->ADP+Pi
  or ATP->AMP+PPi, splits the ligase atp_amide_ligase out); added phospho-ACCEPTOR classes
  `acc_protein`/`acc_nucleoside`/`acc_sugar` (fire only inside a phosphoryl-transfer eqn).
  Dims 31 -> 35.
- Result (leave-one-out): overall 0.645 -> 0.699 (frozen+exp; 0.66 -> 0.719 expansion-only).
  atp_amide_ligase 0.05 -> 0.87; pfka/ndp/deoxynucleoside -> 1.0. Promotion gate
  review_chemistry_disagrees 1883 -> 1572. Cumulative this turn: 0.36 -> 0.699 (+94%).
- PRINCIPLED CEILING: pfkb_ribokinase_family + ghmp_small_molecule_kinase stay ~0 -- they are
  FOLD-defined families whose reaction chemistry overlaps the sugar kinases. Reaction-equation
  features cannot separate fold-defined families; that needs a sequence/structure axis, not
  this leakage-safe reaction representation. Documented, accepted, not hacked around.
- Artifacts: `..._kinase_acceptor_separation.json`, `..._post_kinase_separation.json`. New
  classifier unit tests; separability test extended. No registry written; frozen unchanged.
- Next (still open): the kinase-fold separation belongs to a sequence/structure axis; and
  silver_ready is still gated on HOLO structure (Problem-2 apo->holo cofactor reconstruction).

## Session run - Mechanism-representation separability extension (2026-06-14, Claude Code automation)

- Attacked the root North Star bottleneck for de novo grounding: bronze->silver promotion
  was blocked because the chemistry-feature representation predated the ontology expansion
  and could not SEPARATE the new families. Leave-one-out diagnosis: overall self-consistency
  **0.36**, 12 of 37 families at exactly **0.0** -- every family defined by a cosubstrate/
  donor (NAD(P), CoA, sugar-nucleotide, prenyl-PP) or a non-hydrolytic bond change collapsed
  (the feature space had only cofactor classes + 4 hydrolysis bond classes).
- Fix: extended `mechanism_representation_loop.featurize` with leakage-safe **cosubstrate
  classes** + **non-hydrolytic bond-change classes** (`classify_reaction_nonhydrolytic`,
  `cosubstrate_classes`), derived ONLY from the Rhea substrate->product equation (never
  EC/name/prose/fingerprint). COFACTOR_CLASSES kept as the vector prefix (cofactor-presence
  helpers untouched); dims 16 -> 31.
- Result: overall LOO self-consistency **0.36 -> 0.645** (+78%). nad_p_dehydrogenase 0->0.95,
  coa_acyltransferase 0->0.95, protein_kinase 0->0.97, terpene 0->0.92, biotin 0->1.0,
  non_heme_iron_2og 0->0.87, sam 0.60->0.96. Promotion gate `review_chemistry_disagrees`
  **3558 -> 1883** (halved); those rows moved to honest `blocked_pending_structure`.
  silver_ready stays 0 -- needs HOLO coordinates (registry is overwhelmingly apo, the
  documented Problem-2 frontier, now correctly the NEXT gate). Remaining low separability:
  coarse `metal_dependent_hydrolase` umbrella + the ATP kinase sub-families (differ only by
  acceptor -- a finer unsolved sub-problem).
- Artifacts: `artifacts/v3_mechanism_representation_loop_current702_20260614_cosubstrate_bondchange_extension.json`,
  `artifacts/v3_bronze_silver_promotion_preview_current702_20260614_post_representation_extension.json`.
- Tests: new class-by-class unit tests in `tests/test_mechanism_representation_loop.py`; the
  dormant 12-family separability test re-baselined honestly to the 37-family reality (leakage
  guardrails kept, count 1716->5638, thresholds to measured numbers); bronze_silver stale pin
  refreshed. No registry written; frozen byte-unchanged; leakage wall intact.
- Next (the hard frontier): silver_ready is gated on HOLO structure. The kinase sub-family
  separation (acceptor-specificity) and the apo->holo cofactor reconstruction (Problem 2) are
  the two remaining levers for actual silver promotion / de novo grounding.

## Session run - Near-saturated trim APPLIED (2026-06-14, Claude Code automation, authorized)

- Took the optional backward follow-up: trimmed the 3 families over the rate-8
  reaction-aware cap but below the labels/rxn>10 default ratio
  (`cobalamin_radical_rearrangement`, `pfkb_ribokinase_family`, `radical_sam_enzyme`).
  `scripts/trim_reaction_saturation.py --saturation-ratio-threshold 9.0` (9.0 < lowest
  ratio 9.26 -> captures exactly those 3, the only families over the reaction-aware cap).
  Previewed, then APPLIED on explicit user authorization; frozen sha `5eec9befâ€¦` identical
  before/after.
- Result: **72** rows demoted, expansion **6934 -> 6862**, combined **7636 -> 7564**,
  positive_bronze **5923 -> 5851** (oos_bronze unchanged 1696; counters SEPARATE). Per
  family: cobalamin 141->120 (15 rxn, cap 120), pfkb 150->128 (16 rxn, cap 128),
  radical_sam 213->184 (23 rxn, cap 184); all to labels/rxn 8.0. Reaction diversity fully
  preserved (15/15, 16/16, 23/23); organisms 106/106, 124/124, 184/191.
- Post-apply governor
  (`artifacts/v3_coverage_redundancy_audit_current702_20260614_near_saturated_trim_applied.json`):
  combined 7564, Gini 0.1891, holes [], under-floor [], over-cap
  ['metal_dependent_hydrolase'], reaction_saturated [] -- NO family over its reaction-aware
  cap now. Novelty replay (`...near_saturated_trim_applied.json`): 6862 rows, admit 6406 /
  reject 47 / throttle 409, would-not-readmit 456.
- Guards: frozen NEVER written; validate ok (702 / 37 fp); `git diff --check` clean.
  Refreshed the 2 real-registry count pins to 6862/7564 (coverage, novelty). Demoted rows
  are bronze, never frozen. Atlas is now 7564 labels (5851 positive bronze).

## Session run - Reaction-aware caps WIRED into the live sourcing path (2026-06-14, Claude Code automation)

- The prior turn built the reaction-aware cap + per-reaction gate but left them un-wired
  into the forward runners. This turn wires them in so the climb is mechanism-diverse BY
  CONSTRUCTION, and closes the governor coverage gap. Engine/governor/script wiring only --
  NO registry written: combined stays **7636** (702 frozen + 6934 expansion), **37**
  fingerprints, frozen current702 byte-unchanged sha256 `5eec9befâ€¦`, counters unchanged
  (positive_bronze 5923, oos_bronze 1696, silver_confirmed 17, SEPARATE).
- Shared cap guard: `stage1_hole_sourcing._reaction_aware_cap_guard` +
  `_distinct_reactions_by_fingerprint`, now used by all three runners (stage1 holes,
  stage2 hydrolase sub-families, NAD/glycosyltransferase). Opt-in `reaction_aware_caps`
  (default `False` = flat ceiling, byte-stable) makes the per-family cap
  `clamp(rate*distinct_reactions, floor, base_cap)` (base_cap = flat cap_ceiling or NAD's
  per-family 150/250). Single-reaction family -> floor 100 (preserved, not dropped);
  reaction-rich family -> base ceiling. distinct_reactions counted over
  frozen+expansion+this-run's-admits so new reactions earn headroom. floor_projection now
  carries `effective_cap`/`distinct_reactions`/`projected_over_effective_cap`.
- Runners thread the gate's `per_reaction_cap` (default `None`) into `evaluate_batch` so
  no single Rhea reaction accumulates endless orthologs at admission (enforced at/above
  floor only). The three forward scripts expose `--reaction-aware-caps/--no-...` (default
  ON in the live path), `--reaction-cap-rate` (8), `--per-reaction-cap` (12, negative
  disables). Library defaults stay off; live path defaults on.
- Governor coverage gap closed: added `terpene_cyclase_synthase` (EC 4.2.3) and
  `protein_kinase_ser_thr_tyr` (EC 2.7.10/2.7.11) to `FINGERPRINT_SOURCING_SIGNATURES`
  (35 -> 37). Coverage-accounting metadata only; EC stays scope-only, never predictive.
- New tests: `tests/test_reaction_aware_cap_wiring.py` (cap-guard helper, distinct-reaction
  counting, batch per_reaction_cap), runner propagation/back-compat in
  `tests/test_stage2_hydrolase_subfamily_sourcing.py`, governor coverage of the 2 newest
  fingerprints in `tests/test_coverage_redundancy_audit.py`.
- Guards: frozen NEVER written; `validate` ok (12 source / 37 fp / 34 ontology / 702
  labels); `git diff --check` clean; full offline suite = the known 12 pre-existing
  failures + 1 numpy collection error, no NEW regressions. The optional backward trim of
  the 3 near-saturated families (`cobalamin_radical_rearrangement`,
  `pfkb_ribokinase_family`, `radical_sam_enzyme`) was NOT taken -- no authorization to
  demote more. To address: `scripts/trim_reaction_saturation.py
  --saturation-ratio-threshold <lower>` (preview first; `--apply` only on authorization,
  prints frozen sha before/after).
- Next: run the forward scripts with live UniProt egress (reaction-aware caps now ON by
  default) to fill holes/under-floor families diversely; consider the optional near-
  saturated trim above.

## Session run - Reaction-aware caps + reaction-saturation trim APPLIED (2026-06-14, Claude Code automation)

- Pivoted from volume growth to diversity-quality. Built forward prevention + backward
  cleanup, previewed, then APPLIED the trim on authorization. Rebased onto the
  protein-kinase 37fp lane on main first. Post-apply state: external bronze **6934** (was
  7363), combined **7636** (was 8065), **37** fingerprints; frozen current702
  byte-unchanged sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`
  (printed identical before/after the rewrite); counters separate (positive_bronze 5923
  (was 6352), oos_bronze 1696, silver_ready 0, silver_confirmed 17, projected 0).
- Engine (forward): `coverage_redundancy_audit.reaction_aware_cap` =
  `clamp(rate*distinct_reactions, floor, ceiling)` (rate 8 / floor 100 / ceiling 250);
  governor now flags `reaction_saturated` families (11 at rate 8, surplus 451) and
  recommends TRIM (flagged: governor signature list is 35 families and omits the 2
  newest fingerprints; the trim is data-driven over all 37). `novelty_admission_gate`
  gained opt-in `per_reaction_cap` (default `None` = old behavior; `DiversityState`
  tracks per-reaction occupancy per scope), enforced only at/above floor so holes still
  reach the floor.
- Deliverable: new `src/catalytic_earth/reaction_saturation_trim.py`,
  `scripts/trim_reaction_saturation.py`, CLI `build-reaction-saturation-trim`,
  `tests/test_reaction_saturation_trim.py`. Trim
  `artifacts/v3_reaction_saturation_trim_preview_current702_20260614.json` /
  `work/reaction_saturation_trim_preview_current702_20260614.md`: 9 reaction-saturated
  families trimmed (labels/rxn>10 AND over cap), **429** demoted, expansion 7363->6934,
  combined 8065->7636, positive_bronze 6352->5923 (oos unchanged). Per family SOD
  166->100, pfka 150->100, ghmp 150->100, deoxynucleoside 150->100, zinc 113->100,
  biotin 150->100, askha 150->100, ndp 150->100, protein_kinase_ser_thr_tyr 150->100.
  Reaction diversity preserved in all 9. Gini 0.1352->0.1872 (rises by design;
  labels/rxn is the real metric and drops to the cap). Near-saturated held: cobalamin,
  pfkb, radical_sam. `select_diverse_keep` keeps >=1 row per distinct reaction then
  maximizes organism/length/cluster spread via the near-dup proxy (mmseqs noted as
  stronger offline dedup). Applied via `apply_reaction_saturation_trim_to_registry`
  (non-destructive expansion-registry rewrite; dropped only the 429 demoted ids,
  re-validated every kept label through MechanismLabel.from_dict).
- Post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_reaction_trim_applied.json`
  (combined 7636, Gini 0.1872, holes [], under-floor [], over-cap
  ['metal_dependent_hydrolase'], floor deficit 0) and
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_reaction_trim_applied.json`
  (6934 rows; admit 6478 / reject 47 / throttle 409; would-not-readmit 456).
- Guards: frozen NEVER written (sha identical before/after); `validate` ok (12 source /
  37 fp / 34 ontology / 702 labels); `git diff --check` clean; frozen byte-unchanged.
  Refreshed the 2 count pins to post-trim values (coverage 7636/6934, novelty 6934);
  left flagged the pre-existing failures (epk, atp_amide_ligase, pfka_sourcing,
  bronze_silver_promotion, cofactor_channel/calibration, generalization pin,
  geometry_retrieval, mechanism_representation_loop, sequence_cofactor_channel,
  transfer_scope SDR, numpy collection error).
- Next: add the 2 newest fingerprints to the governor signature list, and wire the
  reaction-aware cap + per-reaction cap into the live runners (stage2/nad_glyco/stage1).
  Optionally tune `--reaction-cap-rate` / `--saturation-ratio-threshold` to also trim the
  3 near-saturated families. Atlas is now 7636 labels (5923 positive bronze).

## Session run - Protein kinase 37fp high-yield lane applied (2026-06-14, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run did not replay terpene
  cap-room top-ups because terpene had only **77** remaining slots. It refreshed the family-lane
  factory after terpene, marked prior SDR/AKR no-import/source-free blockers, then built the
  highest immediately wireable >=150 lane: `protein_kinase_ser_thr_tyr`.
- Registry/universe wiring: added `protein_kinase_ser_thr_tyr` to
  `data/registries/mechanism_fingerprints.json`, added ontology family
  `protein_substrate_phosphoryl_transfer`, bumped
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_37fp`, added deploy-missing
  context wiring, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_37fp_1025.json`. Frozen
  current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Source/admission infrastructure: added
  `src/catalytic_earth/protein_kinase_sourcing.py`,
  `scripts/source_protein_kinase_family.py`, and
  `tests/test_protein_kinase_sourcing.py`. The shared disambiguation rule admits reviewed
  Ser/Thr/Tyr protein kinase candidates only when non-EC protein-kinase family text plus ATP/Mg
  cosubstrate context and Rhea protein-phosphoryl-transfer or active/binding-site evidence are
  present. Histidine kinases, small-molecule kinases, ATP ligases, hydrolases, side-EC rows,
  EC-only rows, and multi-fingerprint rows stay held. EC remains scope-only and never counts as a
  mechanism axis.
- Preview/apply:
  - Initial one-lane preview
    `artifacts/v3_protein_kinase_sourcing_preview_current702_20260614.json` fetched **190**,
    mechanism-corroborated **81**, novelty-admitted **72**, and was not applied because it missed
    the >=150 batch gate. Guardrail audit
    `artifacts/v3_protein_kinase_row_guardrail_audit_current702_20260614.json` found **0**
    problems across all **72** preview rows.
  - Intermediate preview
    `artifacts/v3_protein_kinase_sourcing_preview420_current702_20260614.json` /
    `work/protein_kinase_sourcing_preview420_current702_20260614.md` fetched **420**,
    mechanism-corroborated **198**, and novelty-admitted **145**; it also stayed below the batch
    gate and was not applied.
  - Enlarged preview
    `artifacts/v3_protein_kinase_sourcing_preview470_current702_20260614.json` /
    `work/protein_kinase_sourcing_preview470_current702_20260614.md` fetched **470**,
    mechanism-corroborated **248**, held **0** off-target rows, novelty-admitted **150**, and held
    **0** at cap. Row audit
    `artifacts/v3_protein_kinase_preview470_row_guardrail_audit_current702_20260614.json` found
    **0** problems across all **150** preview labels. The audited preview was applied exactly with
    `--apply --reuse-preview`.
- Net registry change: external bronze **7213 -> 7363** (+150); combined label surface
  **7915 -> 8065**; `protein_kinase_ser_thr_tyr` **0 -> 150**, exactly at its chemistry-confusable
  cap **150**. Growth went only to `data/registries/external_bronze_labels.json`.
- Guardrails verified: all added rows are `tier=bronze`, `review_status=automation_curated`,
  `uniprot:*`, `source_tier_0`, and have `predictive_evidence []`. EC/name/keyword/Rhea/ATP/Mg/
  active-site/binding-site handles are excluded-context admission evidence only. Independent
  mechanism axes in the audited rows: `cofactor_or_cosubstrate=150`,
  `domain_or_family_profile=150`, `rhea_reaction_or_participant_pattern=150`,
  `active_site_motif_or_residue_role=141`.
- Post-apply counts: external bronze **7363**; combined label surface **8065**. External-only split
  is **6139** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
  **6369**, leaving **3631** to the 10k seed-surface target. Honest counters remain separate:
  `positive_bronze_count=6352`, `oos_bronze_count=1696`, `silver_ready_count=0`,
  `silver_confirmed_count=17`, `projected_provisional_count=0`.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_protein_kinase_applied.json` /
  `work/coverage_redundancy_audit_current702_20260614_protein_kinase_applied.md`: **8065**
  combined, **7363** expansion, fingerprint Gini **0.1385**, holes `[]`, under-floor `[]`,
  next-batch floor deficit **0**, over-cap `['metal_dependent_hydrolase']`. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_protein_kinase_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260614_protein_kinase_applied.md`: **7363**
  expansion rows, decisions `{'admit': 6907, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0619).
- Factory artifact after wiring:
  `artifacts/v3_high_yield_family_lane_factory_37fp_current702_20260614.json` /
  `work/high_yield_family_lane_factory_37fp_current702_20260614.md` ranked **12** families before
  the apply. It correctly surfaced `protein_kinase_ser_thr_tyr` as the only immediately ready
  existing >=150 lane. That lane is now capped at **150/150**, so the next run should treat the
  artifact as pre-apply context and either rerun the factory or build the next blocked high-yield
  family.
- Validation passed:
  `PYTHONPATH=src pytest tests/test_protein_kinase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_high_yield_family_lane_factory.py tests/test_fingerprints.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_source_only_contract.py tests/test_coverage_redundancy_audit.py tests/test_novelty_admission_gate.py -q`
  -> **302 passed, 14 subtests passed**. `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 37 fingerprints, 34 ontology families, 702 curated labels). JSON parse
  checks for touched registries/artifacts passed. `git diff --check` passed.
- Next exact action: do **not** continue protein kinase under the current cap policy. Rerun the
  high-yield factory against the 37fp applied state, then wire the next high-yield new family. The
  best immediate candidates are `aldehyde_dehydrogenase` or `alpha_beta_hydrolase_esterase_lipase`
  for cleaner boundaries, or `had_like_phosphatase` only with a hard boundary against the existing
  over-cap `metal_dependent_hydrolase` and other phosphatase/hydrolase rows. Keep SDR/AKR blocked
  unless a source-free, non-EC mechanism rule can separate them from capped NAD(P) dehydrogenase,
  MDR/flavin/metal redox, and each other.

## Session run - Terpene cyclase/synthase 36fp high-yield lane applied (2026-06-14, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run followed the latest
  high-yield factory result rather than replaying capped/tiny lanes. It built the top ranked new
  family lane, `terpene_cyclase_synthase`, through fingerprint, ontology, OOS preregistration,
  mechanism-first rule, source runner, preview, row audit, apply, and validation.
- Registry/universe wiring: added `terpene_cyclase_synthase` to
  `data/registries/mechanism_fingerprints.json`, added ontology family
  `terpene_carbocation_cyclization`, bumped
  `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_36fp`, and re-froze OOS
  preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_36fp_1025.json`.
- Source/admission infrastructure: added
  `src/catalytic_earth/terpene_cyclase_synthase_sourcing.py`,
  `scripts/source_terpene_cyclase_synthase_family.py`, and
  `tests/test_terpene_cyclase_synthase_sourcing.py`. The shared
  `external_cofactor_ec_disambiguation` rule now admits reviewed EC 4.2.3 rows only when non-EC
  terpene/cyclase family context plus Mg/Mn or diphosphate context and Rhea/site evidence are
  present. Prenyltransferase chain-extension, generic hydratase/lyase, side-EC, EC-only, and
  multi-fingerprint rows stay held. EC remains scope-only and never counts as a mechanism axis.
- Preview/apply:
  - Narrow preview
    `artifacts/v3_terpene_cyclase_synthase_sourcing_preview_current702_20260614.json` fetched
    **208**, mechanism-corroborated **114**, novelty-admitted **112**; below the >=150 batch gate,
    so it was not applied.
  - Broadened source preview
    `artifacts/v3_terpene_cyclase_synthase_broad250_sourcing_preview_current702_20260614.json` /
    `work/terpene_cyclase_synthase_broad250_sourcing_current702_20260614.md` fetched **416**,
    mechanism-corroborated **188**, held **48** off-target rows
    (`nad_p_dehydrogenase=47`, `cytochrome_p450_monooxygenase=1`), held **134**
    no-corroboration rows, novelty-admitted **173**, and held **0** at cap. Row audit
    `artifacts/v3_terpene_cyclase_synthase_broad250_row_guardrail_audit_current702_20260614.json`
    found **0** problems across all **173** preview labels.
  - Applied the audited broad250 preview exactly. External bronze **7040 -> 7213** (+173);
    combined label surface **7742 -> 7915**; `terpene_cyclase_synthase` **0 -> 173** under clean
    cap **250**. Frozen current702 stayed byte-unchanged with sha256
    `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Guardrails verified: all added rows are `tier=bronze`, `review_status=automation_curated`,
  `uniprot:*`, `source_tier_0`, and have `predictive_evidence []`. EC/name/prose/keyword/Rhea/
  metal/diphosphate handles are excluded-context admission evidence only; EC is never a counted
  corroborator. Growth went only to `data/registries/external_bronze_labels.json`.
- Post-apply counts: external bronze **7213**; combined label surface **7915**. External-only split
  is **5989** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
  **6219**, leaving **3781** to the 10k seed-surface target. Honest counters remain separate:
  `positive_bronze_count=6202`, `oos_bronze_count=1696`, `silver_ready_count=0`,
  `silver_confirmed_count=17`, `projected_provisional_count=0`.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_terpene_broad250_applied.json` /
  `work/coverage_redundancy_audit_current702_20260614_terpene_broad250_applied.md`: **7915**
  combined, **7213** expansion, fingerprint Gini **0.1385**, holes `[]`, under-floor `[]`,
  next-batch floor deficit **0**, over-cap `['metal_dependent_hydrolase']`. Novelty replay
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_terpene_broad250_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260614_terpene_broad250_applied.md`: **7213**
  expansion rows, decisions `{'admit': 6757, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0632).
- Validation passed:
  `PYTHONPATH=src pytest tests/test_terpene_cyclase_synthase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_leakage_closure.py tests/test_source_only_contract.py tests/test_fingerprints.py tests/test_ontology.py -q`
  -> **278 passed, 14 subtests passed**. `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 36 fingerprints, 33 ontology families, 702 curated labels). JSON parse
  checks for touched registries/artifacts passed. `git diff --check` passed.
- Next exact action: do **not** continue terpene as a high-yield run lane under current objective;
  cap room is now only **77**, below the >=150 batch gate. Use the factory ranking to build the
  next new-family lane, preferably `short_chain_dehydrogenase_reductase` only after an SDR-specific
  rule separates it from the capped coarse `nad_p_dehydrogenase` fingerprint and AKR/MDR/flavin/
  metal redox boundaries. If SDR is judged too confusable for an immediate apply, wire
  `aldehyde_dehydrogenase` or `had_like_phosphatase` through the same 36fp->37fp OOS prereg,
  rule, source runner, preview, row audit, and apply gates.

## Session run - High-yield family scout + lane factory built; no safe >=150 apply in current universe (2026-06-14, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. Current docs showed the recent
  failure mode clearly: non-heme 2OG, CoA, P450, molybdopterin, PfkB, biotin, glycoside,
  isomerase/racemase/kinase subfamilies, SAM MTase, glycosyltransferase, and several hydrolase
  splits are capped; existing copper/SOD/zinc/FMO/heme selectors are exhausted or below the
  150-row batch threshold. This run therefore did not spend time on tiny top-ups.
- Non-destructive high-yield supply scout:
  `artifacts/v3_high_yield_family_supply_scout_current702_20260614.json` /
  `work/high_yield_family_supply_scout_current702_20260614.md` refreshed reviewed UniProt supply
  across **18** broad candidate families. It found **14** clean/floor-reachable candidates under
  old cap math, estimated **2641** capped clean bronze (**1504** diversity-discounted), and still
  projected only **8687** positive bronze from reviewed Swiss-Prot alone, leaving **1313** to 10k
  even before newer per-family caps/current-count limits are applied. This is recon only: no labels
  or registries were written.
- New reusable infrastructure: added `src/catalytic_earth/high_yield_family_lane_factory.py`,
  `scripts/build_high_yield_family_lane_factory.py`, and
  `tests/test_high_yield_family_lane_factory.py`. The factory lets future lanes declare scope
  query, non-EC corroborator query, required mechanism axes, disambiguation holds, cap class,
  source tier, rationale, row-guardrail requirement, and preview/apply command templates. It ranks
  candidate families against live reviewed supply plus current registry cap room while preserving
  the leakage wall: EC is scope-only, non-EC handles are source/admission-only, and no
  `predictive_evidence` is created.
- Factory scout artifact:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260614.json` /
  `work/high_yield_family_lane_factory_current702_20260614.md` ranked **12** candidate families.
  Result: **0** existing lanes are ready for a >=150-row preview/apply. **8** high-yield lanes are
  blocked only because they require a new fingerprint / ontology node / OOS preregistration /
  disambiguation rule before any registry mutation. Top ranked lane:
  `terpene_cyclase_synthase` with reviewed scope supply **2335**, non-EC corroborator-reachable
  supply **2315**, estimated corroboration rate **0.991**, clean non-confusable cap **250**, and
  projected clean admits **250**. Next ranked high-yield blocked lanes are
  `short_chain_dehydrogenase_reductase`, `aldo_keto_reductase`, `had_like_phosphatase`,
  `protein_kinase_ser_thr_tyr`, `aldehyde_dehydrogenase`,
  `alpha_beta_hydrolase_esterase_lipase`, and `ser_thr_protein_phosphatase`.
- No registry apply was attempted. The factory evidence says a >=150 batch is not available under
  the current fingerprint universe; applying top-ups would violate the run objective. Frozen
  current702 remained byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; external bronze remains
  **7040**; combined label surface remains **7742**; combined seed-fingerprint surface remains
  **6046**, leaving **3954** to the 10k seed-surface target. External-only split remains **5816**
  seed rows and **1224** OOS rows. Honest counters remain separate:
  `positive_bronze_count=6029`, `oos_bronze_count=1696`, `silver_ready_count=0`,
  `silver_confirmed_count=17`, `projected_provisional_count=0`.
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_high_yield_family_lane_factory.py tests/test_breadth_feasibility_scout.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **213 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON
  parse checks for the new artifacts and both registries passed. `git diff --check` passed.
- Next exact action: build `terpene_cyclase_synthase` as the first high-yield new-family lane:
  add fingerprint + ontology node, preregister the OOS/fingerprint-universe change, add a
  mechanism-first disambiguation rule requiring non-EC terpene/cyclase + Mg/Mn/diphosphate/Rhea
  corroborators, hold prenyltransferase/lyase/multi-signal rows, add a source runner and row
  guardrail audit, run a non-destructive preview, then apply only if dedup, novelty, cap,
  trust-tier, leakage, and frozen-sha gates pass.

## Session run - Stage-1 radical-SAM post-prefix top-up applied; FMO/heme scouts no-yield (2026-06-14, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. Latest repo state said
  `non_heme_iron_2og_dioxygenase` was capped, current copper selectors were exhausted, and SOD/zinc
  under-cap lanes had concrete no-yield/exhaustion evidence. This run therefore used the existing
  Stage-1 cofactor mechanism-first pipeline for remaining non-confusable cofactor surface rather
  than replaying capped or exhausted family lanes.
- Implementation: added fetch-only window controls to `src/catalytic_earth/stage1_hole_sourcing.py`
  and `scripts/stage1_source_holes.py`: `--record-offset-per-lane` and
  `--record-limit-per-lane`. These controls are applied before entry/Rhea fetch and do not change
  EC scope, disambiguation, trust-tier evaluation, novelty, caps, or predictive evidence. The
  Stage-1 CLI `--apply` path now prints/verifies frozen current702 sha256 before and after append.
- Applied gated source-tier-0 bronze rows:
  - `artifacts/v3_stage1_radical_cobalamin_window100_40_sourcing_preview_current702_20260614.json`
    / `work/stage1_radical_cobalamin_window100_40_sourcing_current702_20260614.md` used
    `--holes radical_sam_enzyme cobalamin_radical_rearrangement --max-records-per-lane 180
    --record-offset-per-lane 100 --record-limit-per-lane 40`.
  - Fetched **160**, disambiguated **82**, applied **81** `radical_sam_enzyme` rows, held **78**
    no-corroboration rows, skipped **0**, and cap-held **1** off-target `coa_acyltransferase` row.
    `cobalamin_radical_rearrangement` stayed **144**. `radical_sam_enzyme` moved **133 -> 214**
    combined, still under the non-confusable cap **250**.
- Continuation scouts:
  - `artifacts/v3_stage1_flavin_heme_window0_30_sourcing_preview_current702_20260614.json` /
    `work/stage1_flavin_heme_window0_30_sourcing_current702_20260614.md`: fetched **125**,
    disambiguated **12**, final novelty-admitted **0**.
  - `artifacts/v3_stage1_flavin_heme_window30_30_sourcing_preview_current702_20260614.json` /
    `work/stage1_flavin_heme_window30_30_sourcing_current702_20260614.md`: fetched **107**,
    disambiguated **21**, final novelty-admitted **0**.
  Do not apply those FMO/heme windows; they are redundant/cap-held under current gates.
- Net registry change: external bronze **6959 -> 7040** (+81); combined label surface
  **7661 -> 7742**. External-only split is **5816** seed-fingerprint rows and **1224** OOS rows.
  Combined seed-fingerprint surface is **6046**, leaving **3954** to 10k by that surface
  convention. Honest counters remain separate: `positive_bronze_count=6029`,
  `oos_bronze_count=1696`, `silver_ready_count=0`, `silver_confirmed_count=17`,
  `projected_provisional_count=0`.
- Guardrails verified: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`; all **81** added rows are `tier=bronze`,
  `review_status=automation_curated`, `uniprot:*`, `source_tier_0`, and have
  `predictive_evidence []`. EC/name/prose/Rhea/cofactor/feature handles remain excluded-context
  admission evidence only, and EC is never counted. Row audit
  `artifacts/v3_stage1_radical_sam_window100_40_row_guardrail_audit_current702_20260614.json` /
  `work/stage1_radical_sam_window100_40_row_guardrail_audit_current702_20260614.md` found **0**
  problems across the **81** newly applied rows.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.json`
  / `work/coverage_redundancy_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.md`:
  **7742** combined, **7040** expansion, seed positives **6046**, fingerprint Gini **0.1385**,
  holes `[]`, under-floor `[]`, next-batch floor deficit **0**, over-cap
  `['metal_dependent_hydrolase']`. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.md`:
  **7040** expansion rows, decisions `{'admit': 6584, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0648).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_stage1_hole_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **316 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON parse
  checks for touched registry/artifacts and `git diff --check` passed.
- Next exact action: do not replay non-heme 2OG, current copper selectors, SOD full-query, zinc
  prefix, or the two FMO/heme windows above. The next bounded 10k-path action can continue Stage-1
  `radical_sam_enzyme` carefully with `--record-offset-per-lane 140 --record-limit-per-lane 40`
  only while cap room remains (radical-SAM is **214/250**), or run a clean source-supply scout/spec
  for another under-cap family with explicit non-EC mechanism corroborators. Any continuation must
  inspect preview gates before apply and hold off-target/multi-signal rows.

## Session run - Non-heme iron 2OG capped; copper post-prefix scout no-yield (2026-06-13/14, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run followed the latest
  handoff exactly: `non_heme_iron_2og_dioxygenase` was **223/250** with a concrete next
  `140:10` preview. The lane still had reviewed, mechanism-first source yield, so the run
  continued bounded windows until the family hit its non-confusable cap.
- Applied gated bronze rows through the existing mechanism-first non-heme 2OG path:
  - `140:10`: fetched **10**, mechanism **7**, applied **6**, throttled **1**, skipped **3**.
  - `150:10`: fetched **10**, mechanism **6**, applied **5**, throttled **1**, skipped **4**.
  - `160:10`: fetched **10**, mechanism **6**, applied **5**, throttled **1**, skipped **4**.
  - `170:10`: fetched **10**, mechanism **6**, applied **3**, throttled **3**, skipped **4**.
  - `180:10`: fetched **10**, mechanism **6**, applied **4**, held **1** no-corroboration row,
    throttled **2**, skipped **3**.
  - `190:10`: fetched **10**, mechanism **6**, gate-admitted **5**, applied **4**, held@cap
    **1**, held **3** no-corroboration rows, skipped **1**.
  Net movement: `non_heme_iron_2og_dioxygenase` **223 -> 250** (+27), exactly at cap. Do not
  continue this lane under current cap policy.
- Net registry change: external bronze **6932 -> 6959** (+27); combined label surface
  **7634 -> 7661**. External-only split is **5735** seed-fingerprint rows and **1224** OOS rows.
  Combined seed-fingerprint surface is **5965**, leaving **4035** to 10k by that surface
  convention. Honest counters remain separate: `positive_bronze_count=5948`,
  `oos_bronze_count=1696`, `silver_ready_count=0`, `silver_confirmed_count=17`,
  `projected_provisional_count=0`.
- Guardrails verified: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`; all added rows are `tier=bronze`,
  `review_status=automation_curated`, `uniprot:*`, `source_tier_0`, and have nested
  `predictive_evidence []`. EC/name/Rhea/keyword/prose/feature handles remain excluded-context
  admission evidence only, and EC is never a counted corroborator. Row audit
  `artifacts/v3_non_heme_iron_2og_capped_row_guardrail_audit_current702_20260613.json` /
  `work/non_heme_iron_2og_capped_row_guardrail_audit_current702_20260613.md` found **0** problems
  across all **250** non-heme 2OG rows.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_non_heme_2og_capped_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_non_heme_2og_capped_applied.md`:
  **7661** combined, **6959** expansion, seed positives **5965**, fingerprint Gini **0.137**,
  holes `[]`, under-floor `[]`, next-batch floor deficit **0**, over-cap
  `['metal_dependent_hydrolase']`. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_non_heme_2og_capped_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_non_heme_2og_capped_applied.md`:
  **6959** expansion rows, decisions `{'admit': 6503, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0655).
- Continuation work: added fetch-only source-window controls to
  `scripts/source_copper_oxidoreductase_family.py` and
  `src/catalytic_earth/copper_oxidoreductase_sourcing.py`, with an offline test proving the slice
  is applied before entry/Rhea fetch. This does not change copper admission, trust-tier, novelty,
  cap, or leakage behavior. A non-destructive copper post-prefix preview
  `artifacts/v3_copper_oxidoreductase_postprefix_window240_40_sourcing_preview_current702_20260613.json`
  / `work/copper_oxidoreductase_postprefix_window240_40_sourcing_current702_20260613.md` used
  `--max-records-per-lane 320 --record-offset-per-lane 240 --record-limit-per-lane 40` and found
  **0** fetched rows: current copper lanes have only **153** laccase/oxidase rows and **69** amine
  oxidase rows. `copper_oxidoreductase` remains **140/250**, but the existing source selectors are
  exhausted beyond the already-fetched prefix.
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_non_heme_iron_2og_sourcing.py tests/test_copper_oxidoreductase_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **323 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON parse
  checks for touched registries/artifacts and `git diff --check` passed.
- Next exact action: do **not** continue non-heme 2OG under current cap policy. For copper, do not
  repeat the current two source lanes; they are source-exhausted after 153 + 69 reviewed rows. The
  next 10k-path action should be a clean new family/source scout or a copper alternate-source scout
  only if it specifies non-EC mechanism corroborators up front. Candidate under-cap families with
  existing fingerprints include `copper_oxidoreductase` **140/250**,
  `manganese_iron_superoxide_dismutase` **166/250**, and `zinc_lyase_hydratase` **113/150**, but
  each needs fresh source handles or a source-supply scout rather than replaying exhausted lanes.

## Session run - Non-heme iron 2OG windowed bronze extension applied (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. The latest state docs said all
  former floor lanes were closed and capped, so this run chose a bounded under-cap 10k-path lane
  with existing mechanism-first admission: `non_heme_iron_2og_dioxygenase` was **172/250** with
  reviewed supply and a prior first-window no-yield duplicate probe. To avoid refetching the
  applied prefix, this run added source-window controls to the non-heme 2OG runner:
  `--record-offset-per-lane` and `--record-limit-per-lane`. These are fetch-only controls and do
  not change disambiguation, trust-tier evaluation, novelty, caps, or leakage behavior.
- Applied gated bronze rows:
  - window `80:10`: fetched **20**, mechanism **18**, novelty-applied **17**, throttled **1**,
    skipped **2**.
  - window `90:10`: fetched **20**, mechanism **13**, novelty-applied **13**, skipped **7**.
  - window `100:10`: fetched **18**, mechanism **15**, novelty-applied **15**, skipped **3**.
  - window `110:10`: fetched **10**, mechanism **3**, novelty-applied **3**, skipped **7**.
  - window `120:10`: fetched **10**, mechanism **2**, novelty-applied **2**, skipped **8**.
  - window `130:10`: fetched **10**, mechanism **1**, novelty-applied **1**, skipped **9**.
  Net family movement: `non_heme_iron_2og_dioxygenase` **172 -> 223** (+51), still below the
  non-confusable cap **250** with **27** cap room. Yield tapered after offset 100, so the next
  bounded continuation should inspect `--record-offset-per-lane 140 --record-limit-per-lane 10`
  before applying.
- Net registry change: external bronze **6881 -> 6932** (+51); combined label surface
  **7583 -> 7634**. External-only split is **5708** seed-fingerprint rows and **1224** OOS rows.
  Combined seed-fingerprint surface is **5938**, leaving **4062** to 10k by that surface
  convention. Strict counters remain separate: `positive_bronze_count=5921`,
  `oos_bronze_count=1696`, `silver_ready_count=0`, `silver_confirmed_count=17`,
  `projected_provisional_count=0`.
- Guardrails verified: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`; all added rows are `tier=bronze`,
  `review_status=automation_curated`, `entry_id` namespace `uniprot:*`, `source_tier_0`, and have
  `predictive_evidence []`. EC/name/Rhea/keyword/prose/feature handles remain excluded-context
  admission evidence only; EC is never counted as a mechanism corroborator. Row audit
  `artifacts/v3_non_heme_iron_2og_windowed_row_guardrail_audit_current702_20260613.json` /
  `work/non_heme_iron_2og_windowed_row_guardrail_audit_current702_20260613.md` found **0**
  problems across all **223** non-heme 2OG rows.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_non_heme_2og_windowed_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_non_heme_2og_windowed_applied.md`:
  **7634** combined, **6932** expansion, fingerprint Gini **0.135**, holes `[]`, under-floor `[]`,
  next-batch floor deficit **0**, over-cap `['metal_dependent_hydrolase']`. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_non_heme_2og_windowed_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_non_heme_2og_windowed_applied.md`:
  **6932** expansion rows, decisions `{'admit': 6476, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0658).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_non_heme_iron_2og_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **314 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON parse
  checks for touched registry/artifacts and `git diff --check` passed.
- Next exact action: if continuing this lane, run a non-destructive preview for
  `scripts/source_non_heme_iron_2og_family.py --max-records-per-lane 180 --record-offset-per-lane 140 --record-limit-per-lane 10 --cap-ceiling 250`
  with fresh artifact/report names, inspect novelty/trust-tier/cap/leakage fields, and apply only
  if it admits clean rows. If yield is zero or redundant, switch to a clean new family/source scout
  rather than broad cap padding. Keep EC scope-only and keep `predictive_evidence []`.

## Session run - Tier-2 floor expansion capped (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run followed the latest
  state docs: CoA/P450/molybdopterin and other cap-fill lanes were already capped or paused, while
  PfkB, biotin carboxylase, and glycoside hydrolase were still under the 100-label floor under
  reviewed tier-0 source paths.
- Implementation: added an explicit source-trust tier parameter to the cofactor/EC disambiguation
  path, preserving default `source_tier_0` behavior while allowing selected callers to pass
  `source_tier_2`. Tier 2 uses the existing `source_trust_tiers.evaluate_corroboration` policy and
  therefore requires **3 independent counted mechanism axes**; EC remains a non-counted scope hint.
  Added source-fetch-only unreviewed tier-2 lanes to the existing glycoside hydrolase, biotin
  carboxylase, and PfkB/ribokinase runners. These lanes require explicit
  `--source-tier source_tier_2`; attempting to run them as tier 0 fails closed. After the first
  three applies, added `--record-offset-per-lane` and `--record-limit-per-lane` controls to PfkB
  and biotin so bounded continuation windows can skip already-applied source rows without changing
  admission, trust-tier, novelty, caps, or leakage rules.
- Applied gated tier-2 rows:
  - Glycoside tier2 `window0:40`: fetched **40**, mechanism **30**, novelty-applied **23**.
  - Biotin tier2 `window0:40`: fetched **40**, mechanism **39**, novelty-applied **39**.
  - PfkB tier2 `window0:80`: fetched **80**, mechanism **80**, novelty-applied **79**.
  - Glycoside tier2 `window40:40`: fetched **40**, mechanism **40**, novelty-applied **34**.
  - Glycoside tier2 `window80:40`: fetched **40**, mechanism **26**, novelty-applied **9**.
  - Biotin tier2 `window40:40`: fetched **40**, mechanism **40**, novelty-applied **27**.
  - PfkB tier2 `window80:40`: fetched **40**, mechanism **40**, novelty-applied **25**.
  Net family movement: `glycoside_hydrolase` **84 -> 150** (+66),
  `biotin_dependent_carboxylase` **84 -> 150** (+66), and
  `pfkb_ribokinase_family` **46 -> 150** (+104). All three former floors are now closed and exactly
  at their chemistry-confusable cap **150**; do not continue them under current cap policy.
- Net registry change: external bronze **6645 -> 6881** (+236); combined label surface
  **7347 -> 7583**. External-only split is **5657** seed-fingerprint rows and **1224** OOS rows.
  Combined seed-fingerprint label surface is **5887**, leaving **4113** to 10k by that surface
  convention. Strict source-trust counters remain separate: `positive_bronze_count=5870`,
  `oos_bronze_count=1696`, `silver_ready_count=0`, `silver_confirmed_count=17`,
  `projected_provisional_count=0`.
- Guardrails verified: frozen current702 stayed byte-unchanged with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`; all **236** added rows are `tier=bronze`,
  `review_status=automation_curated`, `entry_id` namespace `uniprot:*`, `source_tier_2`, and have
  `predictive_evidence []`. EC/name/Rhea/keyword/prose/feature handles remain excluded-context
  admission evidence only; EC is never counted as a mechanism corroborator. Row audit
  `artifacts/v3_tier2_floor_expansion_row_guardrail_audit_current702_20260613.json` found **0**
  problems.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_tier2_floor_expansion_capped_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_tier2_floor_expansion_capped_applied.md`:
  **7583** combined, **6881** expansion, fingerprint Gini **0.1312**, holes `[]`, under-floor
  `[]`, next-batch floor deficit **0**, over-cap `['metal_dependent_hydrolase']`. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_tier2_floor_expansion_capped_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_tier2_floor_expansion_capped_applied.md`:
  **6881** expansion rows, decisions `{'admit': 6425, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0663).
- Validation: targeted pytest passed
  (`PYTHONPATH=src pytest tests/test_pfkb_ribokinase_family_sourcing.py tests/test_biotin_dependent_carboxylase_sourcing.py tests/test_glycoside_hydrolase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_source_ingestion.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **337 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON parse
  checks for touched registry/artifacts and `git diff --check` passed.
- Next exact action: do **not** treat tier-2 rows as silver or projected rows; they are bronze only
  because they satisfy the stricter three-axis gate. The former floor lanes are now capped, not just
  floor-closed. The next 10k-path action should be a clean new family/source lane scout or spec,
  with OOS preregistration if the fingerprint universe changes. Keep EC scope-only, keep
  `predictive_evidence []`, and keep honest counters separate.

## Session run - Windowed CoA/P450/Molybdopterin cap-fills applied (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main` after reading automation memory
  and current state docs. This run followed the latest guidance: remaining PfkB/biotin/glycoside
  floors remain source-limited/no-yield under current non-EC mechanism gates, so work moved to
  bounded, existing-family 10k-path cap-fills with explicit source windows.
- Implementation: exposed existing `build_external_source_ingestion_pilot` row-window controls on
  three family runners:
  `scripts/source_molybdopterin_oxidoreductase_family.py`,
  `scripts/source_cytochrome_p450_family.py`, and
  `scripts/source_coa_acyltransferase_family.py`, with offline tests confirming the row slice is
  applied before entry/Rhea fetch. This is source-fetch control only; it does not change
  disambiguation, trust-tier evaluation, novelty, caps, or predictive evidence.
- A monolithic P450 cap-fill probe
  `scripts/source_cytochrome_p450_family.py --max-records-per-lane 500 --cap-ceiling 250`
  was interrupted before artifact write while inside UniProt entry TLS/connect work. Blocker:
  `artifacts/v3_cytochrome_p450_capfill_live_fetch_blocker_current702_20260613.json` /
  `work/cytochrome_p450_capfill_live_fetch_blocker_current702_20260613.md`. No registry write.
- A bounded strict-kinase GHMP-like entry/Rhea mechanism scout was written after the latest
  handoff's source-supply scout. Artifact/report:
  `artifacts/v3_strict_kinase_ghmp_like_entry_mechanism_scout_current702_20260613.json` /
  `work/strict_kinase_ghmp_like_entry_mechanism_scout_current702_20260613.md`. It sampled **120**
  search rows for `galactokinase_mevalonate_homoserine`, found **5** registry-new rows, fetched
  **5/5** entries, and generated **0** labels. It should **not** be wired next: the existing
  `ghmp_small_molecule_kinase` fingerprint is already **150/150**, active-/binding-site handles
  were absent in the fetched registry-new sample, and a split would need a new chemistry boundary
  plus OOS preregistration.
- Applied windowed molybdopterin cap-fill:
  - `--record-offset-per-lane 80 --record-limit-per-lane 8`: fetched **24**, mechanism **21**,
    admitted/applied **20**, throttled **1**, held@cap **0**, skipped **1**.
  - `--record-offset-per-lane 88 --record-limit-per-lane 8`: fetched **24**, mechanism **20**,
    admitted/applied **19**, throttled **1**, held@cap **0**, skipped **4**.
  - `--record-offset-per-lane 96 --record-limit-per-lane 8`: fetched **19**, mechanism **11**,
    gate-admitted **5**, applied **4**, held@cap **1**, throttled/rejected **6**, skipped **8**.
  `molybdopterin_oxidoreductase` moved **207 -> 250**, exactly at the 250 cap.
- Applied windowed P450 cap-fill:
  - `--record-offset-per-lane 240 --record-limit-per-lane 8`: fetched **24**, mechanism **14**,
    gate-admitted **6**, applied **2**, held@cap **4**, throttled/rejected **8**, held
    **1** no-corroboration row, skipped **9**.
  `cytochrome_p450_monooxygenase` moved **248 -> 250**, exactly at the 250 cap.
- Applied windowed CoA cap-fill:
  - `--record-offset-per-lane 80 --record-limit-per-lane 8`: fetched **24**, mechanism **15**,
    applied **11**, throttled/rejected **4**, skipped **9**.
  - `--record-offset-per-lane 88 --record-limit-per-lane 8`: fetched **24**, mechanism **15**,
    applied **13**, held **2** no-corroboration rows, throttled/rejected **2**, skipped **7**.
  - `--record-offset-per-lane 96 --record-limit-per-lane 8`: fetched **24**, mechanism **18**,
    applied **14**, throttled/rejected **4**, skipped **6**.
  - `--record-offset-per-lane 104 --record-limit-per-lane 8`: fetched **24**, mechanism **19**,
    applied **17**, held **1** multi-fingerprint-signal row and **1** no-corroboration row,
    throttled/rejected **2**, skipped **3**.
  - `--record-offset-per-lane 112 --record-limit-per-lane 8`: fetched **24**, mechanism **23**,
    gate-admitted **12**, applied **7**, held@cap **5**, throttled/rejected **11**, skipped **1**.
  `coa_acyltransferase` moved **188 -> 250**, exactly at the 250 cap.
- Net registry change: external bronze **6538 -> 6645** (+107); combined label surface
  **7240 -> 7347**. Added rows by family: molybdopterin **+43**, P450 **+2**, CoA **+62**.
  External-only split is **5421** seed-fingerprint rows and **1224** OOS rows. Combined
  seed-fingerprint label surface is **5651**, leaving **4349** to 10k by that surface convention.
  Strict source-trust counters remain separate: `positive_bronze_count=5634`,
  `oos_bronze_count=1696`, `silver_ready_count=0`, `silver_confirmed_count=17`,
  `projected_provisional_count=0`.
- Guardrails verified: frozen current702 stayed byte-unchanged before/after every apply with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`; all added rows are `tier=bronze`,
  `review_status=automation_curated`, `entry_id` namespace `uniprot:*`; EC/name/Rhea/keyword/prose/
  feature handles remain excluded-context admission evidence only; EC is never a counted
  corroborator; `predictive_evidence []`. Row audit
  `artifacts/v3_windowed_capfills_row_guardrail_audit_current702_20260613.json` found **0**
  problems across all **750** rows in the three touched capped families.
- Fresh audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_windowed_capfills_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_windowed_capfills_applied.md`: **7347**
  combined, **6645** expansion, fingerprint Gini **0.1704**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **86**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_windowed_capfills_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_windowed_capfills_applied.md`: **6645**
  expansion rows, decisions `{'admit': 6189, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0686).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_coa_acyltransferase_sourcing.py tests/test_cytochrome_p450_sourcing.py tests/test_molybdopterin_oxidoreductase_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **329 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels).
  JSON parse checks and `git diff --check` passed.
- Next exact action: do **not** continue CoA, P450, or molybdopterin under the current cap policy;
  all are now **250/250**. Remaining floors are still PfkB **46/100**, biotin **84/100**, and
  glycoside hydrolase **84/100**. The best next 10k-path action is a genuinely new non-EC
  mechanism-corroborator/source path for those floors, or a clean new-family scout/spec not already
  capped. Avoid GHMP-like strict-kinase continuation unless a real new chemistry split and OOS
  preregistration are justified.

## Session run - Isomerase cap-fill applied; glycoside alternate scouts no-yield (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main` after reading automation memory
  and the current state docs. This run first followed the latest under-floor guidance:
  `glycoside_hydrolase` was still **84/100**, while PfkB and biotin source paths remained
  source-limited/no-yield.
- Status: **APPLIED a gated cofactor-independent isomerase cap-fill to the separate external
  registry after under-floor glycoside continuations admitted 0 rows.** Frozen current702 stayed
  byte-unchanged before/after apply with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.
- Glycoside under-floor work before apply:
  - Added an alternate-only source selector for the existing alternate-name glycoside lane:
    `--only-alternate-name-lanes`. This is a source-fetch selector only; it does not change
    admission, counted corroborator axes, novelty, caps, or predictive evidence.
  - Base glycoside page-2 continuation
    `artifacts/v3_glycoside_hydrolase_page2_window580_80_sourcing_preview_current702_20260613.json`
    fetched **80**, mechanism-corroborated **0**, admitted **0**, held **57** no-corroboration
    rows, skipped **23**, and recorded **1** Rhea HTTP 500 (`Q59675`). Do not apply.
  - Alternate-only name lane
    `artifacts/v3_glycoside_hydrolase_alt_name_only_window40_80_sourcing_preview_current702_20260613.json`
    fetched **80**, mechanism-corroborated **0**, admitted **0**, held **80** no-corroboration
    rows, skipped **0**, and had **0** fetch failures. Do not apply.
- Apply command:
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md --apply`.
  Result: fetched **405**, target mechanism-corroborated **91**, novelty gate admitted **80**
  before the cap guard, applied **8**, held@cap **72**, novelty-throttled/rejected **11**, held
  **61** off-target `nad_p_dehydrogenase` rows, held **90** no-corroboration rows, skipped **163**,
  and had **0** fetch failures on the apply rerun. `cofactor_independent_isomerase` moved
  **142 -> 150**, exactly at the chemistry-confusable cap 150; do not continue this cap-fill lane
  unless the cap policy changes.
- Counts after apply: external bronze **6530 -> 6538** (+8); combined label surface
  **7232 -> 7240**. External-only bronze split is **5314** seed-fingerprint rows and **1224** OOS
  rows. Combined seed-fingerprint label surface is **5544**, leaving **4456** to a 10k
  seed-fingerprint surface. Strict source-trust counter ledger remains separate:
  `positive_bronze_count=5527`, `oos_bronze_count=1696`, `silver_ready_count=0`,
  `silver_confirmed_count=17`, `projected_provisional_count=0`.
- Guardrails verified: all 8 added rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/name/Rhea/keyword/prose/feature handles remain admission/
  excluded-context evidence only; EC is never a counted corroborator; `predictive_evidence []`.
  Row audit
  `artifacts/v3_cofactor_independent_isomerase_capfill_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **150** cofactor-independent isomerase rows.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_isomerase_capfill_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_isomerase_capfill_applied.md`;
  **7240** combined, **35** fingerprints, seed positives **5544**, fingerprint Gini **0.1611**,
  holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **86**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_isomerase_capfill_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_isomerase_capfill_applied.md`;
  **6538** expansion rows, decisions `{'admit': 6082, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0697).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_cofactor_independent_isomerase_sourcing.py tests/test_glycoside_hydrolase_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
  -> **322 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels).
  JSON/JSONL parse checks and `git diff --check` passed.
- Next exact action: remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside
  hydrolase **84/100**. Isomerase, racemase, GHMP, ThDP, and other chemistry-confusable 150-cap
  families at cap should stay paused. The next productive work is a genuinely new non-EC
  mechanism-corroborator/source path for PfkB/biotin/glycoside, or a scout/spec for a clean new
  family not already at cap. Keep EC scope-only and keep `predictive_evidence []`.

## Session run - Racemase cap reached; strict kinase scout scaffolded (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main` after reading automation memory
  and current state docs. This run followed the latest handoff: remaining PfkB/biotin/glycoside
  floor paths are still source-limited/no-yield, so the bounded non-PLP metal racemase/epimerase
  cap-fill continuation was inspected first.
- Status: **APPLIED the gated non-PLP metal racemase/epimerase window400:80 cap-fill to the
  separate external registry.** Frozen current702 stayed byte-unchanged before/after apply with
  sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.
- Apply command:
  `PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 400 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_metal_racemase_epimerase_non_plp_window400_80_sourcing_preview_current702_20260613.json --report work/metal_racemase_epimerase_non_plp_window400_80_sourcing_current702_20260613.md --apply`.
  Result: fetched **80**, mechanism-corroborated **34**, novelty gate admitted **28** before cap,
  applied **21**, held@cap **7**, novelty-throttled/rejected **6**, held **23** off-target
  `nad_p_dehydrogenase` rows, held **22** no-corroboration rows, skipped **1**, fetch failures
  **0**. `metal_racemase_epimerase_non_plp` moved **129 -> 150**, exactly at the chemistry-
  confusable cap 150; do not continue this cap-fill lane unless the cap policy changes.
- Counts after apply: external bronze **6509 -> 6530** (+21); combined label surface
  **7211 -> 7232**. External-only bronze split is **5306** seed-fingerprint rows and **1224** OOS
  rows. Combined seed-fingerprint label surface is **5536**, leaving **4464** to a 10k
  seed-fingerprint surface. Strict source-trust counter ledger remains separate:
  `positive_bronze_count=5519`, `oos_bronze_count=1696`, `silver_ready_count=0`,
  `silver_confirmed_count=17`, `projected_provisional_count=0`.
- Guardrails verified: all 21 added rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/name/Rhea/keyword/prose/feature handles remain admission/
  excluded-context evidence only; EC is never a counted corroborator; `predictive_evidence []`.
  Row audit
  `artifacts/v3_metal_racemase_epimerase_non_plp_window400_80_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **150** racemase/epimerase rows.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_window400_80_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_racemase_window400_80_applied.md`;
  **7232** combined, **35** fingerprints, fingerprint Gini **0.1619**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **86**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_racemase_window400_80_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_racemase_window400_80_applied.md`;
  **6530** expansion rows, decisions `{'admit': 6074, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0698).
- Continuation work: a bounded strict-kinase subclass entry/Rhea scout over
  hexokinase/glucokinase, glycerol kinase, and galactokinase/mevalonate/homoserine was interrupted
  before artifact write while `fetch_uniprot_entry` was blocked in TLS handshake. Blocker artifact:
  `artifacts/v3_strict_kinase_subclass_entry_fetch_blocker_after_racemase_cap_current702_20260613.json`
  / `work/strict_kinase_subclass_entry_fetch_blocker_after_racemase_cap_current702_20260613.md`.
  A cheaper source-supply TSV scout completed:
  `artifacts/v3_strict_kinase_subclass_source_supply_scout_after_racemase_cap_current702_20260613.json`
  / `work/strict_kinase_subclass_source_supply_scout_after_racemase_cap_current702_20260613.md`.
  It sampled **60** rows with **0** fetch failures and generated **0** labels. It ranked
  `galactokinase_mevalonate_homoserine` first by reviewed supply (**613** total) but its first
  20-row TSV window was only **1/20 registry-new**; `glycerol_kinase` was **443** total and **0/20
  registry-new**; `hexokinase_glucokinase` was **223** total and **3/20 registry-new**. This is
  source-supply only; do **not** wire a full fingerprint from it without a smaller/deeper
  entry/Rhea mechanism corroborator scout.
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_metal_racemase_epimerase_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py tests/test_fingerprints.py -q`
  -> **314 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels).
- Next exact action: remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside
  hydrolase **84/100**. Racemase is capped at **150/150**. Build a genuinely new non-EC
  corroborator/source path for those floors, or run a deeper windowed strict-kinase TSV scout plus
  a **small** entry/Rhea mechanism scout for `galactokinase_mevalonate_homoserine` before any
  fingerprint/ontology/OOS-prereg work. Keep EC scope-only and keep `predictive_evidence []`.

## Session run - Racemase windowed top-up applied; floor scouts no-yield (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run first followed the
  latest handoff's under-floor instruction: build genuinely new strict PfkB/biotin or alternate
  glycoside source/corroborator paths before using cap-fill lanes.
- Status: **APPLIED a gated non-PLP metal racemase/epimerase windowed top-up to the separate
  external registry after under-floor source paths produced no admissible rows.** Frozen current702
  stayed byte-unchanged before/after apply with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.
- Source-path work before the apply:
  - Added optional biotin alternate floor-closure lanes
    (`--include-alternate-floor-closure-lanes`) using Rhea/raw-EC source selectors from the prior
    PfkB/biotin scout. Preview
    `artifacts/v3_biotin_dependent_carboxylase_alt_floor_closure_sourcing_preview_current702_20260613.json`
    fetched **139**, mechanism-corroborated **0**, admitted **0**, held **55** no-corroboration
    rows, skipped **84**, and had **0** fetch failures. Do not apply.
  - Added optional glycoside alternate-name lanes (`--include-alternate-name-lanes`) using existing
    chitinase/beta-glucanase/glycoside-hydrolase family-text handles without changing admission
    rules. Bounded preview
    `artifacts/v3_glycoside_hydrolase_alt_name_window40_sourcing_preview_current702_20260613.json`
    fetched **80**, mechanism-corroborated **0**, admitted **0**, held **55** no-corroboration rows,
    skipped **25**, and had **1** Rhea HTTP 500 fetch failure (`Q9LIR6`). Do not apply.
  - Zinc hydratase under-cap preview
    `artifacts/v3_zinc_lyase_hydratase_under_cap_sourcing_preview_current702_20260613.json`
    fetched **160**, mechanism-corroborated **3**, admitted **0** after novelty throttled all 3 as
    redundant, held **55** off-target rows, held **8** no-corroboration rows, and skipped **94**.
    Do not apply.
- Implementation change: added row-window support to
  `scripts/source_metal_racemase_epimerase_family.py` /
  `src/catalytic_earth/metal_racemase_epimerase_sourcing.py` as
  `--record-offset-per-lane` and `--record-limit-per-lane`, mirroring the glycoside windowing
  pattern. The monolithic racemase 500-row top-up was interrupted before artifact write while in
  live UniProt entry TLS/connect work; blocker/resolution artifact:
  `artifacts/v3_metal_racemase_epimerase_topup_live_fetch_blocker_current702_20260613.json`.
- Apply command:
  `PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 320 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_metal_racemase_epimerase_non_plp_window320_80_sourcing_preview_current702_20260613.json --report work/metal_racemase_epimerase_non_plp_window320_80_sourcing_current702_20260613.md --apply`.
  Result: fetched **80**, mechanism-corroborated **21**, applied **21**, held **49** off-target
  `nad_p_dehydrogenase` rows, held **10** no-corroboration rows, skipped **0**, novelty-throttled
  **0**, held@cap **0**, fetch failures **0**. `metal_racemase_epimerase_non_plp` moved
  **108 -> 129** under the chemistry-confusable cap 150.
- Counts after apply: external bronze **6488 -> 6509** (+21); combined label surface
  **7190 -> 7211**. Honest counters remain separate: `positive_bronze=5515`,
  `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`.
  External-only bronze split is **5285** seed-fingerprint rows and **1224** OOS rows. Remaining
  positive-bronze gap to 10k: **4485**. Remaining floors are still PfkB **46/100**, biotin
  **84/100**, and glycoside hydrolase **84/100**.
- Guardrails verified: all 21 added rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/name/Rhea/keyword/prose/feature handles remain admission/
  excluded-context evidence only; EC is never a counted corroborator; `predictive_evidence []`.
  Row audit
  `artifacts/v3_metal_racemase_epimerase_non_plp_window_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **129** racemase/epimerase rows.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_window320_80_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_racemase_window320_80_applied.md`;
  **7211** combined, **35** fingerprints, fingerprint Gini **0.1643**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **86**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_racemase_window320_80_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_racemase_window320_80_applied.md`;
  **6509** expansion rows, decisions `{'admit': 6053, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0701).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_metal_racemase_epimerase_sourcing.py tests/test_glycoside_hydrolase_sourcing.py tests/test_biotin_dependent_carboxylase_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_coverage_redundancy_audit.py tests/test_leakage_closure.py tests/test_source_only_contract.py tests/test_fingerprints.py -q`
  -> **322 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels).
- Next exact action: remaining under-floor lanes need a genuinely new non-EC mechanism corroborator
  source path; the new biotin and glycoside alternate source lanes should not be applied unless a
  later window changes the mechanism-corroboration result. The racemase window can safely continue
  with `--record-offset-per-lane 400 --record-limit-per-lane 80` only if cap 150 and novelty gates
  are inspected first; current racemase is **129/150** with at most 21 rows of cap room.

## Session run - Glycoside hydrolase floor-window applied; paging support added (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run followed the latest
  handoff's under-floor `glycoside_hydrolase` continuation.
- Status: **APPLIED a gated glycoside hydrolase floor-window top-up to the separate external
  registry.** Frozen current702 stayed byte-unchanged before/after apply with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
  `data/registries/external_bronze_labels.json`.
- Implementation change: added row-window support to the shared external ingestion pilot and
  exposed it on `scripts/source_glycoside_hydrolase_family.py` as
  `--record-offset-per-lane`, `--record-limit-per-lane`, and `--query-pages-per-lane`. This lets a
  family process a durable slice of UniProt search results before expensive entry/Rhea fetches,
  without changing admission or predictive-feature rules.
- Apply command:
  `PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 500 --record-offset-per-lane 420 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_floor500_window420_80_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_floor500_window420_80_sourcing_current702_20260613.md --apply`.
  Result: fetched **80**, mechanism-corroborated **14**, applied **12**, held **66**
  no-corroboration rows, skipped **0**, off-target held **0**, novelty-throttled **2**, held@cap
  **0**, fetch failures **0** on the apply rerun. Glycoside hydrolase moved **72 -> 84** under the
  chemistry-confusable cap 150 and remains below the 100 floor.
- Counts after apply: external bronze **6476 -> 6488** (+12); combined label surface
  **7178 -> 7190**. Honest counters remain separate: `positive_bronze=5494`,
  `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`.
  External-only bronze split is **5264** seed-fingerprint rows and **1224** OOS rows. Remaining
  positive-bronze gap to 10k: **4506**.
- Guardrails verified: all 12 added rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/protein-name/Rhea/keyword/prose/feature handles remain
  admission/excluded-context evidence only; EC is never a counted corroborator;
  `predictive_evidence []`. Row audit
  `artifacts/v3_glycoside_hydrolase_floor500_window_row_guardrail_audit_current702_20260613.json`
  found **0** problems across all **84** glycoside hydrolase rows; every row has active-site/
  residue-role, domain/family, and Rhea reaction/participant axes, with no EC axis counted.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.md`;
  **7190** combined, **35** fingerprints, fingerprint Gini **0.1675**, holes `[]`, under-floor
  `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **86**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.md`;
  **6488** expansion rows, decisions `{'admit': 6032, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0703).
- Continuation attempt: page-2 non-destructive preview
  `PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 500 --query-pages-per-lane 2 --record-offset-per-lane 500 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_page2_window500_80_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_page2_window500_80_sourcing_current702_20260613.md`
  fetched **80**, mechanism-corroborated **0**, admitted **0**, held **36** no-corroboration rows,
  skipped **44**, fetch failures **0**. Do not apply that artifact.
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_glycoside_hydrolase_sourcing.py tests/test_external_source_ingestion.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_source_only_contract.py tests/test_fingerprints.py -q`
  -> **317 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON/JSONL
  parse checks and `git diff --check` passed.
- Next exact action: do not repeat the applied `420:80` glycoside window or the zero-yield
  `500:80` page-2 window. Remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside
  hydrolase **84/100**. PfkB and biotin current strict reviewed source paths are documented
  exhausted; the next safe work is a genuinely new strict source/corroborator path for PfkB/biotin
  or an alternate glycoside source lane with non-EC mechanism corroboration. Keep EC scope-only and
  keep `predictive_evidence []`.

## Session run - Glycoside hydrolase top-up applied; floor still open (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run followed the latest
  handoff's under-floor `glycoside_hydrolase` continuation rather than switching families.
- Status: **APPLIED a gated glycoside hydrolase top-up to the separate external registry.** Frozen
  current702 stayed byte-unchanged before/after apply with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Growth went only to
  `data/registries/external_bronze_labels.json`.
- Apply command:
  `PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 420 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_topup_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_topup_sourcing_current702_20260613.md --apply`.
  Result: fetched **420**, mechanism-corroborated **27**, applied **27**, disambiguation holds
  **290**, skipped **103**, off-target held **0**, novelty-throttled **0**, held@cap **0**, fetch
  failures **0**. Glycoside hydrolase moved **45 -> 72** under the chemistry-confusable cap 150 and
  remains below the 100 floor.
- Counts after apply: external bronze **6449 -> 6476** (+27); combined label surface
  **7151 -> 7178**. Honest counters stay separate: `positive_bronze=5482`,
  `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`.
  External-only bronze split is **5252** seed-fingerprint rows and **1224** OOS rows. Remaining
  positive-bronze gap to 10k: **4518**.
- Guardrails verified: all 27 top-up rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/protein-name/Rhea/keyword/prose/feature handles remain
  admission/excluded-context evidence only; EC is never a counted corroborator;
  `predictive_evidence []`; row audit
  `artifacts/v3_glycoside_hydrolase_topup_row_guardrail_audit_current702_20260613.json` found
  **0** problems across all **72** glycoside hydrolase rows; every row has active-site/residue-role,
  domain/family, and Rhea reaction/participant axes, with no boundary tokens in mechanism evidence.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_topup_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_topup_applied.md`;
  **7178** combined, **35** fingerprints, fingerprint Gini **0.1699**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **98**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_topup_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_topup_applied.md`;
  **6476** expansion rows, decisions `{'admit': 6020, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0704).
- Continuation attempt: `--max-records-per-lane 650` is invalid because the ingestion runner caps
  values at 500. A follow-on 500-row preview was stopped for closeout after no artifact was written;
  traceback showed it in `fetch_uniprot_entry` TLS/connect work. Blocker artifact:
  `artifacts/v3_glycoside_hydrolase_floor_topup_live_fetch_blocker_current702_20260613.json` /
  `work/glycoside_hydrolase_floor_topup_live_fetch_blocker_current702_20260613.md`.
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_glycoside_hydrolase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_external_annotation_anchored_import.py tests/test_fingerprints.py tests/test_source_only_contract.py -q`
  -> **313 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON/JSONL
  parse checks and `git diff --check` passed.
- Next exact action: retry the glycoside hydrolase 500-row floor top-up preview early in a run, or
  add paging/resume support before deeper windows. Remaining floors are PfkB **46/100**, glycoside
  hydrolase **72/100**, and biotin **84/100**. Do not count EC as evidence, do not loosen
  glycosyltransferase/transglycosylase/phosphorylase/lyase/side-EC/multi-signal holds, and keep
  `predictive_evidence []`.

## Session run - Glycoside hydrolase 35fp bronze lane applied (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run chose a new clean
  10k-path family after the handoff's remaining PfkB/biotin strict reviewed paths were still
  source-limited and a GHKL histidine-kinase scout found only **1** likely wireable reviewed row.
- Source scouting: `artifacts/v3_ghkl_histidine_kinase_mechanism_handle_scout_current702_20260613.json`
  / `work/ghkl_histidine_kinase_mechanism_handle_scout_current702_20260613.md` showed GHKL was not
  a productive immediate apply lane. `artifacts/v3_glycoside_hydrolase_mechanism_handle_scout_current702_20260613.json`
  / `work/glycoside_hydrolase_mechanism_handle_scout_current702_20260613.md` sampled **240**
  reviewed EC 3.2.1 rows with **194** registry-new and **178** likely wireable by non-EC mechanism
  handles, so glycoside hydrolase was routed through the full pipeline.
- Status: **APPLIED a gated glycoside hydrolase bronze expansion to the separate external registry.**
  Added `glycoside_hydrolase` fingerprint, ontology node `glycosidic_bond_hydrolysis`, deploy-missing
  context `glycosidic_substrate_ordered_water_hydrolysis_context`, coverage source signature,
  source module/script, disambiguation/trust-tier/leakage/coverage tests, and OOS preregistration
  re-freeze `artifacts/v3_external_hard_negative_next_tranche_preregistration_35fp_1025.json`.
  Frozen current702 stayed byte-unchanged before/after apply with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Apply command:
  `PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 240 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_sourcing_current702_20260613.md --apply`.
  Result: fetched **240**, mechanism-corroborated **45**, applied **45**, disambiguation holds
  **155**, skipped **40**, off-target held **0**, novelty-throttled **0**, held@cap **0**,
  fetch failures **1** (`P19531` Rhea timeout). Glycoside hydrolase moved **0 -> 45** under the
  chemistry-confusable cap 150 and remains below the 100 floor.
- Counts after apply: external bronze **6404 -> 6449** (+45); combined label surface
  **7106 -> 7151**. Honest counters stay separate: `positive_bronze=5438`,
  `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`.
  External-only bronze split is **5225** seed-fingerprint rows and **1224** OOS rows. Remaining
  positive-bronze gap to 10k: **4562**.
- Guardrails verified: all 45 added rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/protein-name/Rhea/keyword/prose/feature handles remain
  admission/excluded-context evidence only; EC is never a counted corroborator;
  `predictive_evidence []`; glycosyltransferase, transglycosylase, phosphorylase, lyase, side-EC,
  EC-only, and multi-fingerprint rows are held. Row audit
  `artifacts/v3_glycoside_hydrolase_row_guardrail_audit_current702_20260613.json` found **0**
  problems across **45** rows; every row has active-site/residue-role, domain/family, and
  Rhea reaction/participant axes, with no boundary tokens in mechanism evidence.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_applied.md`; **7151**
  combined, **35** fingerprints, fingerprint Gini **0.1753**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **125**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_applied.md`; **6449**
  expansion rows, decisions `{'admit': 5993, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0707).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_glycoside_hydrolase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_external_annotation_anchored_import.py tests/test_fingerprints.py tests/test_source_only_contract.py -q`
  -> **313 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels).
- Next exact action: close the remaining floors without relaxing the leakage wall. First try a
  deeper strict glycoside hydrolase continuation/top-up to reach 100 only if the same gates hold;
  otherwise return to PfkB **46/100** and biotin **84/100** with genuinely new source/corroborator
  paths. Do not count EC as evidence, and do not repeat the weak GHKL scout as a production lane.

## Session run - Mn/Fe SOD 34fp bronze expansion applied (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run followed the latest
  handoff's `manganese_iron_superoxide_dismutase` lane through the full gated 34fp pipeline.
- Status: **APPLIED a gated Mn/Fe superoxide dismutase bronze expansion to the separate external
  registry.** Frozen current702 stayed byte-unchanged before/after both applies with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. External bronze
  **6238 -> 6404** (+166); combined label surface **6940 -> 7106**.
- Family/gate setup: added `manganese_iron_superoxide_dismutase` fingerprint, added ontology node
  `metal_superoxide_dismutation`, bumped the positive fingerprint universe to
  `label_factory_v1_34fp`, and re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_34fp_1025.json`.
- Initial SOD apply:
  `PYTHONPATH=src python scripts/source_manganese_iron_superoxide_dismutase_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_manganese_iron_superoxide_dismutase_sourcing_preview_current702_20260613.json --report work/manganese_iron_superoxide_dismutase_sourcing_current702_20260613.md --apply`.
  Result: fetched **240**, mechanism-corroborated **181**, applied **164**, held **59**
  no-corroboration rows, skipped **0**, off-target held **0**, novelty-throttled **17**,
  held@cap **0**; SOD **0 -> 164**.
- Bounded top-up apply:
  `PYTHONPATH=src python scripts/source_manganese_iron_superoxide_dismutase_family.py --max-records-per-lane 320 --cap-ceiling 250 --out artifacts/v3_manganese_iron_superoxide_dismutase_topup_sourcing_preview_current702_20260613.json --report work/manganese_iron_superoxide_dismutase_topup_sourcing_current702_20260613.md --apply`.
  Result: fetched **252**, skipped **164** already-existing rows, mechanism-corroborated **19**,
  applied **2**, held **69** no-corroboration rows, off-target held **0**, novelty-throttled
  **17**, held@cap **0**; SOD **164 -> 166** under cap 250 and above floor.
- Guardrails verified: all added rows are `tier=bronze`, `review_status=automation_curated`,
  `entry_id` namespace `uniprot:*`; dedup + novelty gates ran against frozen current702 and the
  external bronze registry; EC/protein-name/Rhea/keyword/prose/feature handles remain
  admission/excluded-context evidence only; EC is never a counted corroborator;
  `predictive_evidence []`; Cu/Zn SOD, heme/peroxidase/cytoglobin/hemoglobin, nitrite/nitric-oxygen
  dioxygenase, superoxide-reductase, side-EC, EC-only, and multi-fingerprint rows were held.
  Row audit `artifacts/v3_manganese_iron_superoxide_dismutase_row_guardrail_audit_current702_20260613.json`
  found **0** problems across **166** rows, with active-site/residue-role, cofactor/cosubstrate,
  and Rhea reaction/participant axes present on every row.
- Honest counters remain separate: `positive_bronze=5393`, `oos_bronze=1696`,
  `silver_ready=0`, `silver_confirmed=17`, `projected=0`. External-only bronze split is
  **5180** seed-fingerprint rows and **1224** OOS rows. Remaining positive-bronze gap to 10k:
  **4607**.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.md`; **7106** combined,
  **34** fingerprints, fingerprint Gini **0.1608**, holes `[]`, under-floor
  `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **70**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.md`; **6404**
  expansion rows, decisions `{'admit': 5948, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0712).
- Validation: focused pytest passed
  (`PYTHONPATH=src pytest tests/test_manganese_iron_superoxide_dismutase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py tests/test_external_annotation_anchored_import.py tests/test_source_only_contract.py -q`
  -> **301 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 34 fingerprints, 31 ontology families, 702 curated labels). JSON parse
  checks and `git diff --check` passed.
- Next exact action: do not repeat the SOD first-window or top-up previews; the guarded reviewed
  source is now largely exhausted at **166/250** with only redundant or no-corroboration rows left
  in this query. The remaining floor deficit is still PfkB **46/100** and biotin **84/100**; build a
  genuinely new strict source/corroborator path for those lanes, or scout/spec the next clean
  fingerprint family through fingerprint/ontology/OOS-prereg/preview/apply gates.

## Session run - Mn/Fe SOD source blocker cleared; 34fp next-lane spec written (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This run continued after user
  feedback that the previous bounded no-yield run should not have stopped at the first 0-row result.
- Status: **NO REGISTRY WRITE; USEFUL 10K-PATH LANE ADVANCED.** No `--apply` was run and no labels
  were generated. Counts remain external bronze **6238**, combined label surface **6940**, frozen
  current702 **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: `positive_bronze=5227`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`; remaining positive-bronze gap to 10k **4773**.
- PfkB/biotin alternate-source scout:
  `artifacts/v3_pfkb_biotin_alternate_source_scout_current702_20260613.json` and
  `work/pfkb_biotin_alternate_source_scout_current702_20260613.md`. Result: source counts found
  some registry-new reviewed accessions but no clean immediate apply path. Samples include boundary
  cases such as non-biotin subunits, biotin-protein ligases, acetone carboxylase subunits, and
  bifunctional thiamine/HMP kinase rows. Do not admit those rows directly; EC/name/Rhea remain
  scope/admission context only.
- Mn/Fe SOD source/mechanism scout:
  `artifacts/v3_manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.json`
  and `work/manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.md`.
  The prior breadth-feasibility result had undercounted this lane by requiring a UniProt COFACTOR
  comment. A guarded reviewed query now finds **252** Mn/Fe SOD rows. In an 80-row sample:
  **80/80** registry-new, **80/80** RHEA:20696/superoxide dismutation reaction context,
  **80/80** Mn/Fe metal context, **80/80** SOD family text, **77/80** active/binding/metal-site
  evidence, **0** explicit Cu/Zn/heme/side-EC boundary flags, **0** fetch failures.
- Next-lane spec:
  `artifacts/v3_manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.json` and
  `work/manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.md`. It proposes
  `manganese_iron_superoxide_dismutase` as a deliberate `label_factory_v1_34fp` lane with ontology
  node `metal_superoxide_dismutation`, cap 250, deploy-missing context
  `mn_fe_superoxide_redox_dismutation_context`, and counted mechanism axes from Rhea/reaction
  superoxide dismutation, Mn/Fe metal or metal-site evidence, active/binding/metal-site evidence,
  and SOD family/domain text.
- Guardrails preserved: EC/name/Rhea/text handles are scope/admission evidence only and remain
  excluded from predictive features; EC is never a counted corroborator; no `predictive_evidence`
  changes; frozen current702 was not written.
- Required next action: wire the SOD lane only through the full pipeline: add fingerprint and
  ontology node, bump to `label_factory_v1_34fp`, re-freeze OOS preregistration, add
  disambiguation/trust-tier/leakage/source tests, run a non-destructive preview, and apply only if
  novelty/dedup/governor/cap/trust-tier gates pass. Required guards: hold Cu/Zn SOD,
  heme/cytoglobin/hemoglobin/peroxidase/nitrite/nitric-oxygen dioxygenase, superoxide reductase,
  side-EC, EC-only, and multi-fingerprint-signal rows.

## Session run - bounded under-cap previews cleared blocker but admitted 0 rows (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. This resumed the prior blocked
  run after user feedback that the live-fetch blocker should have been isolated rather than treated
  as a final stop.
- Status: **BLOCKER CLEARED FOR BOUNDED PREVIEWS, NO REGISTRY WRITE.** The sourcing runners do
  complete and write preview artifacts at small `--max-records-per-lane` values. The prior
  no-artifact behavior came from larger sequential UniProt entry/Rhea evidence-fetch workloads
  before artifact write, not from a broken gate. No `--apply` was run because all bounded previews
  yielded **0 novelty-admitted labels**.
- Bounded preview results:
  - `cofactor_independent_isomerase` micro 5 rows/lane:
    `artifacts/v3_cofactor_independent_isomerase_micro_capfill_sourcing_preview_current702_20260613.json`;
    fetched **14**, mechanism-corroborated **0**, novelty-admitted **0**.
  - `cofactor_independent_isomerase` 20 rows/lane:
    `artifacts/v3_cofactor_independent_isomerase_bounded_capfill_sourcing_preview_current702_20260613.json`;
    fetched **67**, mechanism-corroborated **0**, novelty-admitted **0**.
  - `coa_acyltransferase` 20 rows/lane:
    `artifacts/v3_coa_acyltransferase_bounded_extension_sourcing_preview_current702_20260613.json`;
    fetched **75**, mechanism-corroborated **0**, novelty-admitted **0**.
  - `non_heme_iron_2og_dioxygenase` 20 rows/lane:
    `artifacts/v3_non_heme_iron_2og_bounded_extension_sourcing_preview_current702_20260613.json`;
    fetched **66**, mechanism-corroborated **3**, novelty-admitted **0**; all 3 throttled as
    `redundant_no_novelty_signal`.
  - `molybdopterin_oxidoreductase` 20 rows/lane:
    `artifacts/v3_molybdopterin_oxidoreductase_bounded_extension_sourcing_preview_current702_20260613.json`;
    fetched **67**, mechanism-corroborated **2**, novelty-admitted **0**; both throttled as
    `redundant_no_novelty_signal`.
  - `zinc_lyase_hydratase` 20 rows/lane:
    `artifacts/v3_zinc_lyase_hydratase_bounded_extension_sourcing_preview_current702_20260613.json`;
    fetched **20**, mechanism-corroborated **0**, novelty-admitted **0**.
  - `copper_oxidoreductase` 20 rows/lane:
    `artifacts/v3_copper_oxidoreductase_bounded_extension_sourcing_preview_current702_20260613.json`;
    fetched **40**, mechanism-corroborated **1**, novelty-admitted **0**; throttled as
    `redundant_no_novelty_signal`.
- Aggregate artifact/report:
  `artifacts/v3_under_cap_bounded_preview_no_yield_current702_20260613.json` and
  `work/under_cap_bounded_preview_no_yield_current702_20260613.md`.
- Counts unchanged: external bronze **6238** (5014 seed-fingerprint bronze + 1224 OOS bronze);
  combined label surface **6940**; frozen current702 **702** with sha256
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters remain
  separate: `positive_bronze=5227`, `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`,
  `projected=0`; remaining positive-bronze gap to 10k **4773**.
- Guardrails preserved: no labels applied; EC/name/keyword/Rhea/prose/feature handles remain
  excluded-context admission evidence only; EC is never a counted mechanism corroborator;
  `predictive_evidence` was not changed; frozen current702 was not written.
- Validation: focused pytest passed
  (`tests/test_cofactor_independent_isomerase_sourcing.py tests/test_coa_acyltransferase_sourcing.py tests/test_non_heme_iron_2og_sourcing.py tests/test_molybdopterin_oxidoreductase_sourcing.py tests/test_zinc_lyase_hydratase_sourcing.py tests/test_copper_oxidoreductase_sourcing.py tests/test_leakage_closure.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  -> **262 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 33 fingerprints, 30 ontology families, 702 curated labels).
  JSON/JSONL parse checks and `git diff --check` passed.
- Next exact action: do **not** repeat these same bounded first-window probes. The next useful
  action is a genuinely new PfkB/biotin source path with stronger mechanism corroboration, a deeper
  under-cap extension only when enough time remains for preview completion + validation + push, or a
  new-family mechanism/source-supply scout/spec if evidence is cleaner.

## Session run - under-cap extension previews blocked by live fetch latency (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. Latest state left
  `pfkb_ribokinase_family` (46/100) and `biotin_dependent_carboxylase` (84/100) under floor, but
  both current strict reviewed source paths are exhausted under mechanism-first gates. This run
  therefore attempted bounded, already approved under-cap extension/cap-fill previews rather than
  relaxing EC or forcing source-limited under-floor lanes.
- Status: **BLOCKED with no registry write.** No preview produced inspectable gate output before the
  live fetch/evidence extraction attempts were terminated, so no `--apply` was run. Frozen
  current702 stayed byte-unchanged
  (`sha256:5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`).
- Attempted commands:
  `PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 500 --cap-ceiling 250 --out artifacts/v3_coa_acyltransferase_extension_sourcing_preview_current702_20260613.json --report work/coa_acyltransferase_extension_sourcing_current702_20260613.md`
  (terminated after no preview artifact),
  `PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 280 --cap-ceiling 250 --out artifacts/v3_coa_acyltransferase_extension_sourcing_preview_current702_20260613.json --report work/coa_acyltransferase_extension_sourcing_current702_20260613.md`
  (terminated after no preview artifact), and
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`
  (terminated after no preview artifact).
- Counts unchanged: external bronze **6238** (5014 seed-fingerprint bronze + 1224 OOS bronze);
  combined label surface **6940**; honest counters remain separate:
  `positive_bronze=5227`, `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`,
  `projected=0`; remaining positive-bronze gap to 10k **4773**.
- Current under-cap approved lanes worth a bounded retry: `cofactor_independent_isomerase` 142/150,
  `coa_acyltransferase` 188/250, `non_heme_iron_2og_dioxygenase` 172/250,
  `molybdopterin_oxidoreductase` 207/250, and `copper_oxidoreductase` 140/250. Do not add more
  P450 without explicit new reaction/organism justification because it is 248/250. Do not broad-wire
  EC 2.7 or admit EC-only rows.
- Guardrails preserved: no labels generated/applied; no `predictive_evidence` changes; EC/name/
  keyword/Rhea/prose/feature handles remain excluded-context admission evidence only; EC is never a
  counted mechanism corroborator; frozen current702 was not written.
- New blocker artifacts:
  `artifacts/v3_under_cap_extension_live_fetch_blocker_current702_20260613.json` and
  `work/under_cap_extension_live_fetch_blocker_current702_20260613.md`.
- Validation: `PYTHONPATH=src python -m catalytic_earth.cli validate` passed (12 source records,
  33 mechanism fingerprints, 30 ontology families, 702 curated labels). JSON/JSONL parse checks
  passed; `git diff --check` passed. No focused pytest was run because this run changed docs and a
  blocker artifact only, with no code or registry writes.
- Next exact action: retry the smallest cap-fill first:
  `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`.
  If it produces preview rows, inspect `floor_projection`, `novelty_gate`, held@cap, trust-tier,
  namespace/tier/review-status, `predictive_evidence`, and excluded-context fields before running
  the same command with `--apply`.

## Session run - P450 + copper extension bronze applies (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`. The latest handoff left
  `pfkb_ribokinase_family` and `biotin_dependent_carboxylase` under floor, but both current
  reviewed source paths are exhausted under strict mechanism-first gates. This run therefore used
  already approved, non-confusable extension lanes with remaining reviewed supply:
  `cytochrome_p450_monooxygenase` and `copper_oxidoreductase`.
- Status: **APPLIED two gated external bronze extensions to the separate external registry.**
  Frozen current702 stayed byte-unchanged
  (`sha256:5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`) before/after both
  applies. External bronze **6079 -> 6238** (+159); combined label surface **6781 -> 6940**.
- P450 extension: non-destructive preview
  `PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json --report work/cytochrome_p450_extension_sourcing_current702_20260613.md`.
  Result: fetched **337**, target mechanism-corroborated **189**, applied **138**,
  no-corroboration holds **35**, duplicate/current-registry skips **113**, novelty-throttled
  **51**, held@cap **0**, off-target held **0**; `cytochrome_p450_monooxygenase`
  **110 -> 248** under the non-confusable cap 250.
- Copper extension: non-destructive preview
  `PYTHONPATH=src python scripts/source_copper_oxidoreductase_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json --report work/copper_oxidoreductase_extension_sourcing_current702_20260613.md`.
  Result: fetched **222**, target mechanism-corroborated **81**, applied **21**,
  no-corroboration holds **20**, duplicate/current-registry skips **121**, novelty-throttled
  **60**, held@cap **0**, off-target held **0**; `copper_oxidoreductase` **119 -> 140**.
- Guardrails verified: EC/Rhea/name/keyword/prose/feature handles are scope/admission evidence only
  and remain in `excluded_context`; EC is never a counted corroborator; `predictive_evidence []`;
  every added row is `tier=bronze`, `review_status=automation_curated`, `uniprot:*`; dedup ran
  against frozen current702 and external bronze; cap 250 was enforced for both non-confusable
  lanes. Row audits found **0** problems across all **138** P450 rows and **21** copper rows; all
  rows have cofactor/cosubstrate, domain/family, active-site/residue-role, and Rhea participant
  axes.
- Honest counters after apply: `positive_bronze=5227`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`. Do not merge them. External-only bronze split is 5014
  seed-fingerprint rows and 1224 OOS rows. Remaining positive-bronze gap to 10k: **4773**.
- Fresh post-apply audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.json`
  / `work/coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.md`;
  **6940** combined, **33** fingerprints, seed positives **5227**, fingerprint Gini **0.1633**,
  holes `[]`, under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **70**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_p450_copper_extensions_applied.json`
  / `work/novelty_admission_gate_audit_current702_20260613_p450_copper_extensions_applied.md`;
  **6238** expansion rows, decisions `{'admit': 5782, 'reject': 47, 'throttle': 409}`,
  would-not-readmit **456** (0.0731).
- Validation:
  `PYTHONPATH=src pytest tests/test_cytochrome_p450_sourcing.py tests/test_copper_oxidoreductase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  passed (**304 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 33 mechanism fingerprints, 30 ontology families, 702 curated labels).
  JSON/JSONL parse checks passed.
- Key new artifacts/files this run:
  `artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json`,
  `work/cytochrome_p450_extension_sourcing_current702_20260613.md`,
  `artifacts/v3_cytochrome_p450_extension_row_guardrail_audit_current702_20260613.json`,
  `work/cytochrome_p450_extension_row_guardrail_audit_current702_20260613.md`,
  `artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json`,
  `work/copper_oxidoreductase_extension_sourcing_current702_20260613.md`,
  `artifacts/v3_copper_oxidoreductase_extension_row_guardrail_audit_current702_20260613.json`,
  `work/copper_oxidoreductase_extension_row_guardrail_audit_current702_20260613.md`,
  final coverage/novelty audits named `p450_copper_extensions_applied`, and
  `data/registries/external_bronze_labels.json`.
- Next exact action: do **not** add more P450 unless a new reaction/organism gain is explicitly
  justified, because it is now **248/250**. PfkB remains **46/100** and biotin remains **84/100**,
  but their current reviewed strict lanes are exhausted; the next safest productive work is a
  genuinely new PfkB/biotin source path with stronger corroboration, or a new fingerprint-family
  source-supply scout/spec if evidence is cleaner than further balanced-lane top-ups.

## Session run - PfkB ribokinase-family 33fp bronze expansion applied (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` on current `origin/main`
  (`eff1342cabe960e05ec9c38f1558705ec3b794b9` before local edits). The latest handoff left
  `pfkb_ribokinase_family` as a guarded candidate after the PfkA apply; this run tightened the
  PfkB/PfkA boundary and applied the strict PfkB lane through the full mechanism-first pipeline.
- Status: **APPLIED a gated `pfkb_ribokinase_family` bronze expansion to the separate external
  bronze registry.** Frozen current702 stayed byte-unchanged
  (`sha256:5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`) before/after apply.
  External bronze **6033 -> 6079** (+46); combined label surface **6735 -> 6781**.
- Family/gate setup: added `pfkb_ribokinase_family` fingerprint and mapped it to ontology family
  `pfkb`; bumped `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_33fp`;
  re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`. EC 2.7.1 is
  scope-only. Counted mechanism corroboration comes from ATP/ADP phosphoryl-transfer Rhea
  participant context with PfkB-family acceptors (ribose, adenosine, inosine,
  1-phosphofructose/fructose-1-phosphate, hydroxymethylpyrimidine), PfkB/ribokinase-family text,
  ATP/Mg/substrate active- or binding-site evidence, cofactor/cosubstrate handles, and
  structure-compatible evidence. Protein kinases, two-component histidine kinases,
  hydrolase/nuclease rows, NDK, dNK, ASKHA, GHMP, PfkA, side-EC, and multi-fingerprint rows are
  held. A boundary bug was fixed by removing generic `fructokinase` as a counted PfkB family token
  because it matched inside `6-phosphofructokinase` and shadowed PfkA.
- Apply command:
  `PYTHONPATH=src python scripts/source_pfkb_ribokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched **88**, target mechanism-corroborated **46**, applied **46**,
  no-corroboration holds **36**, disambiguation skips **2**, off-target held **4** as
  `askha_sugar_acetate_kinase`, novelty-throttled/rejected **0**, held@cap **0**, duplicate
  skipped **0**; `pfkb_ribokinase_family` **0 -> 46** (chemistry-confusable cap 150; still
  under the 100 floor by 54).
- Guardrails verified: EC/Rhea/name/keyword/prose/feature handles are scope/admission evidence only
  and remain in `excluded_context`; EC is never a counted corroborator; `predictive_evidence []`;
  every added row is `tier=bronze`, `review_status=automation_curated`, `uniprot:*`; dedup ran
  against frozen current702 and external bronze; per-fingerprint cap 150 was enforced. Row audit
  `artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json` found **0**
  problems across all **46** PfkB rows; all four independent mechanism axes are present on every
  row: active-site/residue role, cofactor/cosubstrate, domain/family profile, and Rhea
  reaction/participant pattern.
- Honest counters after apply, per the combined-registry counter policy in `source_trust_tiers`:
  `positive_bronze=5085`, `oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`,
  `projected=0`. Do not merge them. External-only bronze split is 4855 seed-fingerprint rows and
  1224 OOS rows. Remaining positive-bronze gap to 10k: **4915**.
- Fresh post-PfkB audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_pfkb_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_pfkb_applied.md`; **6781** combined,
  **33** fingerprints, seed positives **5085**, fingerprint Gini **0.162**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
  `['metal_dependent_hydrolase']`, next-batch floor deficit **70**. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfkb_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_pfkb_applied.md`; **6079** expansion rows,
  decisions `{'admit': 5623, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.075).
- Durable follow-on scout:
  `artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json` /
  `work/pfkb_ribokinase_family_floor_extension_scout_current702_20260613.md` reran the strict
  reviewed PfkB lane after apply with `--max-records-per-lane 500`. It fetched **88** rows again,
  found **0** new target PfkB labels, skipped **48** already-covered rows, held **36** rows for
  `no_mechanism_corroboration`, held **4** off-target ASKHA rows, and left
  `pfkb_ribokinase_family` at **46/100**.
- Validation:
  `PYTHONPATH=src pytest tests/test_pfkb_ribokinase_family_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  passed (**294 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 33 mechanism fingerprints, 30 ontology families, 702 curated labels).
- Key new artifacts/files this run:
  `src/catalytic_earth/pfkb_ribokinase_family_sourcing.py`,
  `scripts/source_pfkb_ribokinase_family.py`,
  `tests/test_pfkb_ribokinase_family_sourcing.py`,
  `artifacts/v3_pfkb_ribokinase_family_sourcing_preview_current702.json`,
  `work/pfkb_ribokinase_family_sourcing_current702.md`,
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`,
  `artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json`,
  `work/pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.md`,
  `artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json`,
  `work/pfkb_ribokinase_family_floor_extension_scout_current702_20260613.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_pfkb_applied.json`,
  `work/coverage_redundancy_audit_current702_20260613_pfkb_applied.md`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfkb_applied.json`,
  `work/novelty_admission_gate_audit_current702_20260613_pfkb_applied.md`, and
  `data/registries/external_bronze_labels.json`.
- Next exact action: do **not** broad-wire EC 2.7 or merge kinase subclasses. PfkB is now a real
  33fp lane but remains under floor by 54, and the strict reviewed PfkB lane is exhausted under the
  current gate. Either return to the biotin floor deficit (16 rows), design a genuinely new PfkB
  source/handle path with stronger corroboration, or pick a new non-kinase 10k-path family through
  the full fingerprint/ontology/preregistration/preview/apply pipeline.

## Session run - PfkA 32fp bronze expansion applied (2026-06-13, Codex automation)

- Automation ID: `ce-nad-glyco-floor-expansion`; lock acquired at
  `.git/catalytic-earth-automation.lock` after reading the current handoff/project-state/scaling
  context. The latest handoff selected strict `pfka_phosphofructokinase` from the post-dNK Pfk
  scout; this run followed that lane through the full mechanism-first pipeline.
- Status: **APPLIED a gated `pfka_phosphofructokinase` bronze expansion to the separate external
  bronze registry.** Frozen current702 stayed byte-unchanged
  (`sha256:5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`) before/after apply.
  External bronze **5883 -> 6033** (+150); combined label surface **6585 -> 6735**.
- Family/gate setup: added `pfka_phosphofructokinase` fingerprint and mapped it to the existing
  ontology family `pfka`; bumped `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to
  `label_factory_v1_32fp`; re-froze OOS preregistration as
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`. EC 2.7.1 is
  scope-only. Counted mechanism corroboration comes from ATP/ADP phosphoryl-transfer Rhea
  participant context with fructose-6-phosphate, PfkA/ATP-dependent 6-phosphofructokinase family
  text, ATP/Mg/substrate active- or binding-site evidence, cofactor/cosubstrate handles, and
  structure-compatible evidence. Protein kinases, two-component histidine kinases,
  hydrolase/nuclease rows, NDK, dNK, ASKHA, GHMP, PfkB/ribokinase, and multi-fingerprint rows are
  held. The PfkA/ASKHA boundary was tightened so the synonym `phosphohexokinase` does not falsely
  trip the broad ASKHA `hexokinase` guard.
- Apply command:
  `PYTHONPATH=src python scripts/source_pfka_phosphofructokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
  Result: fetched **240**, target mechanism-corroborated **233**, applied **150**,
  no-corroboration holds **5**, disambiguation skips **2**, novelty-throttled/rejected **0**,
  held@cap **83**, off-target held **0**, duplicate skipped **0**; `pfka_phosphofructokinase`
  **0 -> 150** (chemistry-confusable cap 150; floor reached).
- Guardrails verified: EC/Rhea/name/keyword/prose/feature handles are scope/admission evidence only
  and remain in `excluded_context`; EC is never a counted corroborator; `predictive_evidence []`;
  every added row is `tier=bronze`, `review_status=automation_curated`, `uniprot:*`; dedup ran
  against frozen current702 and external bronze; per-fingerprint cap 150 was enforced. Row audit
  `artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json` found **0**
  problems across all **150** PfkA rows; all four independent mechanism axes are present on every
  row: active-site/residue role, cofactor/cosubstrate, domain/family profile, and Rhea
  reaction/participant pattern.
- Honest counters after apply: `positive_bronze=5039`, `oos_bronze=1696`, `silver_ready=0`,
  `silver_confirmed=17`, `projected=0`. Do not merge them. Remaining positive-bronze gap to 10k:
  **4961**.
- Fresh post-PfkA audits:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_pfka_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_pfka_applied.md`; **6735** combined,
  **32** fingerprints, seed positives **5039**, fingerprint Gini **0.1465**, holes `[]`,
  under-floor `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`,
  next-batch floor deficit **16**. The coverage accounting signature for the previously applied
  `deoxynucleoside_kinase` was added so the fingerprint distribution now reconciles with the label
  totals. Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfka_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_pfka_applied.md`; **6033** expansion rows,
  decisions `{'admit': 5577, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0756).
- Validation:
  `PYTHONPATH=src pytest tests/test_pfka_phosphofructokinase_sourcing.py tests/test_deoxynucleoside_kinase_sourcing.py tests/test_nucleoside_diphosphate_kinase_sourcing.py tests/test_askha_sugar_acetate_kinase_sourcing.py tests/test_ghmp_small_molecule_kinase_sourcing.py tests/test_external_cofactor_ec_disambiguation.py tests/test_external_annotation_anchored_import.py tests/test_ontology.py tests/test_leakage_closure.py tests/test_coverage_redundancy_audit.py tests/test_source_trust_tiers.py tests/test_novelty_admission_gate.py -q`
  passed (**312 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed (12 source records, 32 mechanism fingerprints, 30 ontology families, 702 curated labels).
- Small durable continuation: wrote
  `work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md` using the prior non-destructive
  PfkB scout. PfkB is **not** yet an apply lane: reviewed supply **85**, sampled **28/40** likely
  wireable, **0/40** boundary signals, and active-/binding-site context only **28/40**. Next work
  should first improve/re-run the source-supply scout or choose a stronger current scaling-plan
  family if evidence is cleaner.
- Key new artifacts/files this run:
  `src/catalytic_earth/pfka_phosphofructokinase_sourcing.py`,
  `scripts/source_pfka_phosphofructokinase_family.py`,
  `tests/test_pfka_phosphofructokinase_sourcing.py`,
  `artifacts/v3_pfka_phosphofructokinase_sourcing_preview_current702.json`,
  `work/pfka_phosphofructokinase_sourcing_current702.md`,
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`,
  `artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json`,
  `work/pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_pfka_applied.json`,
  `work/coverage_redundancy_audit_current702_20260613_pfka_applied.md`,
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfka_applied.json`,
  `work/novelty_admission_gate_audit_current702_20260613_pfka_applied.md`, and
  `work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md`.
- Next exact action: do **not** broad-wire EC 2.7 or merge kinase subclasses. Either tighten and
  re-scout `pfkb_ribokinase_family` before any 33fp wiring, or select a stronger current
  scaling-plan family if the evidence supply is cleaner. Any next family still needs fingerprint/
  ontology spec if new, OOS prereg re-freeze, mechanism corroborator rules, non-destructive preview,
×½{ëÍÊ×¬¢h­µç[˜\šX[[œÜXÝ[Û‹[™Ú]Y™ˆKXÚXÚØ‚‚\ÈÙˆHŒ‹LKLNŒMŽLˆ]]ÛX][Ûˆ[‹\ÙHH\Y˜XÝZYÜ˜][ÛˆØ\Â˜ÚXÚÙYÛ›H\ÈHÝX\™[™™[XZ[œÈÛÜÙYÛ›Û‹X›ØÚÚ[™Î‚˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\ØÝ[™\ÜÈLœ›ÝÜË›ØÚÙ\œË[™™[[Ý˜[Ø[ÝÙYLˆHØÚY[YšXÈÛÜšÈÛÛ[YYBœ™]šY]Ë[Û›HTÈÜÚ]]™KYš[™Ù\œš[]Ú]Ý]Y][™Â˜YXÚ[š\ÛWÙš[™Ù\œš[ËšœÛÛ˜Ý\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛ˜Üˆ[žH^\›˜[š\™[™YØ]]™HX™[‚‚•H[ˆYY\Y˜XÝËÝŒ×Ù\×ØXØÙ\Ü—ÚY[]WÜ™]šY]×ÌLKšœÛÛ˜\ÈBÓHZ[\ˆZ[Y\ËXXØÙ\Ü‹ZY[]K\™]šY]Øˆ]ÛÛœÝ[Y\ÈH™]šY]Ë[Û›B™Ø[[XKYÙ[ÛY]žHYX\Ý\™[Y[Ø[\H[™HÝ\œ™[K\ÛXÙHÜ˜\È™]šY]ÂÚ]\ˆHYX\Ý\™YY›Þ[]Û\ÈX]ÚÛÝ\˜ÙK\Ý\ÜYÝXœÝ˜]KXXØÙ\Ü‚šY[]Kˆ›ÝØ[[XK[YX\Ý\™Y›ÝÜÈ\ÜÈ]™]šY]ÈÛÛ^ˆWØÜØNŒÍXX\Â›™X\™\ÝUÈÈH›Û‹XØ][]XËXÚZ[ˆÙ\ˆY›Þ[ÛÛœÚ\Ý[Ú]›ÝZ[‚œÝXœÝ˜]HY›Þ[ÛÛ^[™WØÜØNŒ˜X\È™X\™\ÝS”ÈÈB››Û‹XØ][]XËXÚZ[ˆ\ˆY›Þ[ÛÛœÚ\Ý[Ú]\›ÜÚ[™HÝXœÝ˜]HÛÛ^‚˜WØÜØN™[XZ[œÈÛÝ\˜ÙK\Ý\ÜY][›YX\Ý\™Y™XØ]\ÙHHÙ[XÝYœÝXÝ\™H\ÈØØ[QÜ›ÙXÝ\Ý]H˜]\ˆ[ˆUÙØ[[XKXØ\X›K‚‚•H[ˆ[ˆYY\Y˜XÝËÝŒ×Ù\×Ø]ÜÝ]WÙ]šY[˜ÙWÜ[—ÌLKšœÛÛ˜\ÂHÓHZ[\ˆZ[Y\ËX]\Ý]KY]šY[˜ÙK\[˜ˆ]ØÜ™Y[œÈB™Ü˜\[[šÙYˆÝXÝ\™\È›ÜˆWØÜØN[™š[™ÈZYÚØ[™Y]BœÝXÝ\™\ËˆÛÈ[\›˜]\È
RÕX[™ÕL
H]™HØ[[XKXØ\X›HS”ÓYÂ˜ÛÛ^[™X\[›Ý\ˆØ][]XÈÙ\]Y[˜ÙK\ÜÚ][Ûˆ™\ÚYY\ËˆÕL[ÛÂ˜Ø\œšY\ÈHXØÙ\Ü‹[ZÙH[Z[›ÙÛXÛÜÚYHYØ[™ÛÙHŒÌXÈHÝ\œ™[œÙ[XÝYS™]Z[œÈQÓYÈ\ÈÐSˆÛÛ^ˆHØ[YH\Y˜XÝYX\Ý\™\Â›™X\™\ÝS”Ë]ËPŒÌHÞYÙ[ˆ\Ý[˜ÙH]ËMN[™ÜÝ›ÛH[ˆÕLÝ[œ™]šY]Ë[Û›Kˆ\È˜\œ›ÝÜÈH™^XÝ[ÛˆÈ™\ÚÛØÛÛ›Û\ÚYÛˆ™Y›Ü™B˜[žHØÛÜ™\ˆÛÜšË‚‚˜\Y˜XÝËÝŒ×Ù\×Ü™XÛÝ[ÙØ]WÜÝ]\×ÌLKšœÛÛ˜Ø\È™YÙ[™\˜]YÚ]]˜XØÙ\Ü‹ZY[]H™]šY]È[™HU\Ý]H]šY[˜ÙH[ˆ]XÚYˆB›YX\Ý\™Y\›ÝÈXØÙ\ÜˆY[]HØ]H›ÝÈ\ÜÙ\Ë]HÝ™\˜[[™H™[XZ[œÂ˜›ØÚÙYÜ™]šY]×ÛÛ›XˆXØÙ\Ü‹]™\ÚÛØ[Xœ˜][Û‹ÛÛ\]HØ[[XHÙ[ÛY]žB˜XÜ›ÜÜÈ[›ÝÝ\H›ÝÜË›Û‹\™XYK\›ÝÈ™\Z\‹^\›˜[\™[™YØ]]™HØÛÜ™Yœ™KX]Y][™™YÚ\ÝžKÛX™[Y˜XÝÜžH^[œÚ[ÛˆÝ[˜Z[ÛÜÙYˆYXÚ[š\ÛB^\È^XÚ]H™]šY]ÈÛÛ^Û›H[™\È›Ý[ˆTÈØÛÜš[™È™X]\™K‚‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\È™[[Ý™\ÈHYX\Ý\™Y\›ÝÈXØÙ\ÜˆY[]B˜[XšYÝZ]H›ÜˆWØÜØNŒÍX[™WØÜØNŒ˜]]\ÈÝ[›Ý[ˆTÈØÛÜ™\ˆÜ‚œÜÚ]]™Hš[™Ù\œš[^[œÚ[Û‹ˆHXÝ]™Hš[™Ù\œš[[š]™\œÙH™[XZ[œÈÂ˜Ý\˜]YX™[È™[XZ[ˆŽˆÚ]ŒLˆÙYYÙš[™Ù\œš[[™ÌÝ]ÛÙ—ÜØÛÜX›X™[ÎÈ^\›˜[[\ÜYX™[È™[XZ[ˆ^XÝH[š\›Ý”Í˜[š\›Ý”ÎMX[™[š\›Ý”LÓLØÈ^\›˜[[\ÜYÙYYYš[™Ù\œš[›X™[È™[XZ[ˆˆH™^›Ý[™YTÈÝ\ÚÝ[\ÚYÛˆ™\ÚÛØÛÛ›Û˜Üš]\šXH›ÜˆHYX\Ý\™YWØÜØN[\›˜]HÙ[ÛY]žKØ[Xœ˜]B˜XØÙ\Ü‹ÙØ[[XH™\ÚÛÈÛ›HY\ˆ\›ÜšX]H™YØ]]™HÛÛ›ÛÈ^\ÝÜ‚˜XÝÛˆHWØÜØNŒŽ˜ØWØÜØNŒ˜YØ[™\™\Z\ˆ[™\ËˆÈ›ÝYHTÂœ™YÚ\ÝžHš[™Ù\œš[[\ÜTÈX™[ËÜˆØÛÜ™H^\›˜[\™™YØ]]™\È[[H[™KXÛÝ[Ø]H]\È[\[Y[Y‚•™\šYšXØ][Ûˆ\ÜÙYÚ]Hš[˜[K]\Ý[š]ÝZ]K˜[Y]X˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\ØÛÛ\[X[™^\›˜[X™[[˜\šX[[œÜXÝ[Û‹[™Ú]Y™ˆKXÚXÚØ‚‚\ÈÙˆHŒ‹LKLNÎŒMNVˆ]]ÛX][Ûˆ[‹\ÙHH\Y˜XÝZYÜ˜][ÛˆØ\Â˜ÚXÚÙYÛ›H\ÈHÝX\™[™™[XZ[œÈÛÜÙYÛ›Û‹X›ØÚÚ[™Î‚˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\ØÝ[™\ÜÈLœ›ÝÜË›ØÚÙ\œË[™™[[Ý˜[Ø[ÝÙYLˆHØÚY[YšXÈÛÜšÈÛÛ[YYBœ™]šY]Ë[Û›HTÈÜÚ]]™KYš[™Ù\œš[]Ú]Ý]Y][™Â˜YXÚ[š\ÛWÙš[™Ù\œš[ËšœÛÛ˜Ý\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛ˜Üˆ[žH^\›˜[š\™[™YØ]]™HX™[‚‚•H[ˆYY\Y˜XÝËÝŒ×Ù\×Ý^Ùœ™YWÛØØ[Ø^\×Ü›ÝÝ\WÌLKšœÛÛ˜\ÂHÓHZ[\ˆZ[Y\Ë]^Yœ™YK[ØØ[X^\Ë\›ÝÝ\XˆH\Y˜XÝ›X]\šX[^™\Èš[˜\žHØØ[™X]\™H^\ÈÛ›H›ÜˆH™YH›ÝÜÈ[™XYHX\šÙYœ™XYHžHHØØ[Y]šY[˜ÙH]Y]ˆWØÜØNŒÍXWØÜØNŒ˜[™WØÜØN‚‘XXÚ›ÝÈ\ÈØØ[Y[š[™K[XÛ[ÝYKY][[YØ[™[™Ø][]XÈXÚYØ˜\ÙB˜^\Èœ›ÛHÙ[ÛY]žH]šY[˜ÙKˆWØÜØNŒŽ˜[™WØÜØNŒ˜™[XZ[ˆ^ÛYYœ›ÛBH›ÝÝ\H™XØ]\ÙHZ\ˆØØ[YØ[™^\È\™H›Ý™XYKˆH\Y˜XÝÙY\Â™[žH˜[Y\È\È˜XÙXXš[]HÛ›H[™^XÚ]H^ÛY\È˜[Y\ËPËÔšXHQË•[šT›Ý›ÜÙKKPÔÐH^Ý\˜]YX™[Ýš[™ÜË[™^\˜][Û˜[\Èœ›ÛBœ™YXÝ]™H\ÙK‚‚•H[ˆ[ÛÈYY˜\Y˜XÝËÝŒ×Ù\×ØXØÙ\Ü—ÙÙ[ÛY]žWØ^\×ÙØ\Ü[—ÌLKšœÛÛ˜\ÈHÓB˜Z[\ˆZ[Y\ËXXØÙ\Ü‹YÙ[ÛY]žKX^\ËYØ\\[˜ˆ\ÈÝ^\È™]šY]Ë[Û›H[™\Ù\ÈÝ\œ™[Ù[ÛY]žH™X]\™\ÈÈ^ÜÙHØ[™Y]HXØÙ\ÜˆÛÛ^›ÜˆBœØ[YH™YH›ÝÝ\H›ÝÜÎˆY›Þ[\™\ÚYYHØÚÙ]ÛÛ^›Üˆ[™YH›ÝÜÂ˜[™™X\ˆXØÙ\Ü‹[ZÙHÐS˜YØ[™ÛÛ^›ÜˆWØÜØNˆWØÜØNŒŽ˜[™˜WØÜØNŒ˜™[XZ[ˆ^ÛYY[[Z\ˆØØ[YØ[™^\È\™H™\Z\™YˆB˜\Y˜XÝÙ\È›Ý™\šYžHXØÙ\ÜˆY[]K™\ÚÛHXØÙ\Üˆ^\ËYX\Ý\™B™Ø[[XK\ÜÜ]K]ËXXØÙ\ÜˆÙ[ÛY]žKÛÛ\]H[ˆTÈØÛÜ™KÜˆØÛÜ™H^\›˜[š\™™YØ]]™\È[™\ˆTË‚‚‘š[˜[K\Y˜XÝËÝŒ×Ù\×Û›Ûœ™XYWÛYØ[™Ü™\Z\—Ü[—ÌLKšœÛÛ˜\Â˜Z[Y\Ë[›Ûœ™XYK[YØ[™\™\Z\‹\[˜›ÝÈXZÙHHÛÈ^ÛYY\›ÝÈ™\Z\‚›[™\È^XÚ]ˆWØÜØNŒŽ˜\ÈU[™YÈÛ›H\È›Û›ØØ[ÝXÝ\™K[]™[›YØ[™È[ˆÙ[XÝYÝXÝ\™HTÎRXÛÈ]™YYÈØØ[YØ[™Y\Ý[˜ÙKœ™\ÚYYK[X\[™ËÜˆÙ[XÝY\ÝXÝ\™H™\Z\‹ˆWØÜØNŒ˜\È›ÂœÙ[XÝY\ÝXÝ\™HYØ[™^\È[ˆP“ÌXÛÈ]™YYÈ[\›˜]HYØ[™]šY[˜ÙB›Üˆ[\›˜]K\ÝXÝ\™HÛÝ\˜Ú[™È™Y›Ü™H]Ø[ˆ›Ú[ˆ[žHTÈØÛÜ™\ˆ›ÝÝ\K‚‚˜\Y˜XÝËÝŒ×Ù\×ØXØÙ\Ü—Ø^\×Ý™\ÚÛÙ\ÚYÛ—ÌLKšœÛÛ˜\Â˜Z[Y\ËXXØÙ\Ü‹X^\Ë]™\ÚÛY\ÚYÛ˜™XÛÜ™ÈØ[™Y]HXØÙ\Ü‹X^\Â˜Ý]Ù™œÈÙˆ‹[™[™ÜÝ›ÛKˆHˆ[™ÜÝ›ÛHØ[™Y]H\ÈHÛX[\ÝÛ™B]ÛÝ™\œÈH™YHÝ\œ™[›ÝÝ\H›ÝÜÈžHY›Þ[\™\ÚYYHÛÛ^]š]\È^XÚ]H›ÝÙ[XÝYÜˆØ[Xœ˜]Y[™Ø[››Ý™H\ÙY\È[ˆTÂ™\ÚÛ[[Ø[[XK\ÜÜ]K]ËXXØÙ\ÜˆÙ[ÛY]žH[™^\›˜[™KX]Y]˜ÛÛ›ÛÈ^\Ý‚‚˜\Y˜XÝËÝŒ×Ù\×ÙØ[[XWÙÙ[ÛY]žWÙ™X\ÚXš[]WÜ[—ÌLKšœÛÛ˜\Â˜Z[Y\ËYØ[[XKYÙ[ÛY]žKY™X\ÚXš[]K\[˜ÛÜÙ\ÈH[ˆžHÙ\\˜][™Â˜]ÛK[]™[™XXÝ[Û‹XÙ[\ˆ™X\ÚXš[]Hœ›ÛHØÛÜš[™ËˆWØÜØNŒÍX[™˜WØÜØNŒ˜]™HØØ[UÐS”\ÈXØÙ\ÜˆÛÛ^[™\™H™XYH›ÜˆH]\™B™Ø[[XK\ÜÜ]H]ÛKYÙ[ÛY]žHYX\Ý\™[Y[ˆWØÜØN\ÈØØ[Q\Â˜XØÙ\ÜˆÛÛ^ÛÈ]™YYÈU\Ý]HÜˆ[˜[ÙÈ]šY[˜ÙH™Y›Ü™HØ[[XB™Ù[ÛY]žHØ[ˆÝ\ÜØÛÜš[™Ë‚‚•H[ˆ[ˆYY\Y˜XÝËÝŒ×Ù\×ÙØ[[XWÙÙ[ÛY]žWÛYX\Ý\™[Y[ÜØ[\WÌLKšœÛÛ˜œ\ÈZ[Y\ËYØ[[XKYÙ[ÛY]žK[YX\Ý\™[Y[\Ø[\X\Ú[™ÈÔÐˆ[PÒQˆ]ÛB˜ÛÛÜ™[˜]\È›Üˆ”Ø[™RTŒØˆ]YX\Ý\™\È™]šY]Ë[Û›H™X\™\Ý”Ë]ËXØ[™Y]KZY›Þ[\Ý[˜Ù\ÈÙˆËŒL[™ÜÝ›ÛH›ÜˆWØÜØNŒÍX[™KŒˆ[™ÜÝ›ÛH›ÜˆWØÜØNŒ˜ÈWØÜØN™[XZ[œÈÚÚ\Y™XØ]\ÙHBœÙ[XÝYÝXÝ\™H\ÈØØ[QÜ›ÙXÝ\Ý]H˜]\ˆ[ˆUÙØ[[XKXØ\X›K‚•\ÙH\Ý[˜Ù\È\™H›ÝXØÙ\YÝXœÝ˜]HY[]Y\Ë™\ÚÛËTÈØÛÜ™\Ë™^\›˜[Z\™[™YØ]]™H™KX]Y]]šY[˜ÙKÜˆX™[Ø]\Ë‚‚˜\Y˜XÝËÝŒ×Ù\×Ü™XÛÝ[ÙØ]WÜÝ]\×ÌLKšœÛÛ˜\Â˜Z[Y\Ë\™XÛÝ[YØ]K\Ý]\ØÛÛœÛÛY]\ÈHÝ\œ™[[™H\Â˜›ØÚÙYÜ™]šY]×ÛÛ›XˆHØØ[X^\È›ÝÝ\HØ]H\ÜÙ\ËÚ[HXØÙ\Ü‚™\ÚÛØ[Xœ˜][Û‹ÛÛ\]HØ[[XHÙ[ÛY]žHXÜ›ÜÜÈ[›ÝÝ\H›ÝÜË››Û‹\™XYK\›ÝÈ™\Z\‹^\›˜[\™[™YØ]]™HØÛÜ™Y™KX]Y][™™YÚ\ÝžKÂ›X™[Y˜XÝÜžH^[œÚ[Ûˆ[˜Z[ÛÜÙY‚‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\È\ÈH\ÙY[ØÛÜ™\‹Y]™[ÜY[Ý\™˜XÙK˜]Ý[›Ý[ˆTÈØÛÜ™\ˆÜˆÜÚ]]™Hš[™Ù\œš[^[œÚ[Û‹ˆHXÝ]™B™š[™Ù\œš[[š]™\œÙH™[XZ[œÈÈÝ\˜]YX™[È™[XZ[ˆŽˆÚ]ŒL‚˜ÙYYÙš[™Ù\œš[[™ÌÝ]ÛÙ—ÜØÛÜXX™[ÎÈ^\›˜[[\ÜYX™[Âœ™[XZ[ˆ^XÝH[š\›Ý”Í[š\›Ý”ÎMX[™[š\›Ý”LÓLØÂ™^\›˜[[\ÜYÙYYYš[™Ù\œš[X™[È™[XZ[ˆˆXØÙ\ÜˆÙ[ÛY]žK™Ø[[XK\ÜÜÜž[]˜[œÙ™\ˆ™XXÝ[Û‹XÙ[\ˆÙ[ÛY]žKTÈ™\ÚÛØ[Xœ˜][Û‹™^\›˜[\™[™YØ]]™HØÛÜ™Y™KX]Y]\›Z[˜[™]šY]ËX™[Y˜XÝÜžHØ]B™^[œÚ[Û‹[™™YÚ\ÝžHY]È™[XZ[ˆ›ØÚÙ\œÈ™Y›Ü™H[žHÛÝ[X›HTÈÛÜšË‚•H™^›Ý[™YTÈÝ\YˆÚÜÙ[‹ÚÝ[™\šYžHÚ]\ˆHYX\Ý\™YšY›Þ[]Û\È\™HYHÝXœÝ˜]HXØÙ\ÜœËÛÝ\˜ÙHU\Ý]H]šY[˜ÙH›Ü‚˜WØÜØNÜˆXÝÛˆHÛÈ^XÚ]YØ[™\™\Z\ˆ[™\ÎÈÈ›ÝYHTÂœ™YÚ\ÝžHš[™Ù\œš[[\ÜTÈX™[ËÜˆØÛÜ™H^\›˜[\™™YØ]]™\È[[H[™KXÛÝ[Ø]H]\È[\[Y[Y‚•™\šYšXØ][Ûˆ\ÜÙYÚ]Hš[˜[ŒK]\Ý[š]ÝZ]K˜[Y]X˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\ØÛÛ\[X[™^\›˜[X™[[˜\šX[[œÜXÝ[Û‹[™Ú]Y™ˆKXÚXÚØ‚‚\ÈÙˆHŒ‹LKLNŽŒLÎŒˆ]]ÛX][Ûˆ[‹\ÙHH\Y˜XÝZYÜ˜][ÛˆØ\Â˜ÚXÚÙYÛ›H\ÈHÝX\™[™™[XZ[œÈÛÜÙYÛ›Û‹X›ØÚÚ[™Î‚˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\ØÝ[™\ÜÈLœ›ÝÜË›ØÚÙ\œË[™™[[Ý˜[Ø[ÝÙYLˆHØÚY[YšXÈÛÜšÈÝ^YYÛˆBœÜÝZ[™œ˜HTÈÜÚ]]™KYš[™Ù\œš[]Ú]Ý]Y][™Â˜YXÚ[š\ÛWÙš[™Ù\œš[ËšœÛÛ˜Ý\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛ˜Üˆ[žB™^\›˜[\™[™YØ]]™HX™[‚‚•H[ˆYY\Y˜XÝËÝŒ×Ù\×Ù˜YÙš[™Ù\œš[ÜÜX×ÌLKšœÛÛ˜Bœ™]šY]Ë[Û›H˜Yš[™Ù\œš[ÜXÚYšXØ][Ûˆ›Ü‚˜\×Ø]ÙØ[[XWÜÜÜÜž[Ý˜[œÙ™\˜ˆ]œ™Y^™\ÈH[[™YØØ[™YXÝ]™B˜^\È
UÓYÌŠÈÜÚ][Ûš[™ËUØ[[XK\ÜÜÜž[]˜[œÙ™\ˆ™XXÝ[ÛˆÙ[\‹šY›Þ[XXØÙ\ÜˆØÛÜKXÚYØ˜\ÙHXÝ]˜][Û‹[™™ZYÚ›Üš[™ÈUY˜[Z[B˜ÛÝ[\™]šY[˜ÙJK^XÚ]H^ÛY\È›ÝZ[ˆ˜[Y\ËPËÔšXHY[YšY\œË•[šT›Ý›ÜÙKKPÔÐHYXÚ[š\ÛH^Ý\˜]Üˆ˜][Û˜[\Ë[™X™[Ýš[™ÜÈœ›ÛBœ™YXÝ]™H\ÙK[™ÙY\ÈH™KXÛÝ[Ø]HÝ]H›ØÚÙYˆH\Y˜XÝÙY\ÂHÜÚ]]™Hš[™Ù\œš[[š]™\œÙH][\ÜÈX™[ËØÛÜ™\È^\›˜[\™›™YØ]]™\Ë[™X]™\È[™YH[\ÜY^\›˜[\™™YØ]]™\ÈÛ›H\Âœ™]šY]Ë[Û›H™KX]Y]›ÝÜË‚‚•HØ[YH[ˆYY\Y˜XÝËÝŒ×Ù\×ÛØØ[Ù]šY[˜ÙWØ]Y]ÌLKšœÛÛ˜ÚXÚœ›Ùš[\ÈÜÙHš]™HTÈ›Ý[™\žH›ÝÜÈYØZ[œÝHÝ\œ™[K\ÛXÙHÙ[ÛY]žB˜\Y˜XÝˆ™YH›ÝÜÈ
WØÜØNŒÍXWØÜØNŒ˜[™WØÜØN
H]™HØØ[›XÛ[ÝYKY][[™XÚYØ˜\ÙH^\È™XYH›ÜˆH]\™H^Yœ™YH^\Âœ›ÝÝ\KˆWØÜØNŒŽ˜\ÈUÓYÈÝXÝ\™K[]™[ÚYÛ˜[]›ÝHØØ[XÝ]™BœÚ]HYØ[™^\Ë[™WØÜØNŒ˜XÚÜÈHØØ[YØ[™^\ËˆH]Y]ÛÛ\]\Â››ÈTÈØÛÜ™KÙY\È™XYWÝ×Ü[—Ù\×ÜØÛÜ™\Y˜[ÙX[™X]™\ÈXØÙ\Ü‚™Ù[ÛY]žK™\ÚÛØ[Xœ˜][Û‹^\›˜[\™[™YØ]]™H™KX]Y]\›Z[˜[œ™]šY]Ë[™X™[Y˜XÝÜžHØ]\È\È›ØÚÙ\œÈ™Y›Ü™H[žHÛÝ[X›HTÈÛÜšË‚‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆHTÈ[™H\È›ÝÈ™]\ˆÜXÚYšYY[™\ÈB™š\œÝØØ[Y]šY[˜ÙH™XY[™\ÜÈ›Ùš[K]]\ÈÝ[›ÝHÜÚ]]™B™š[™Ù\œš[^[œÚ[Û‹ˆHXÝ]™Hš[™Ù\œš[[š]™\œÙH™[XZ[œÈÈÝ\˜]Y›X™[È™[XZ[ˆŽˆÚ]ŒLˆÙYYÙš[™Ù\œš[[™ÌÝ]ÛÙ—ÜØÛÜXX™[ÎÂ™^\›˜[[\ÜYX™[È™[XZ[ˆ^XÝH[š\›Ý”Í[š\›Ý”ÎMX[™˜[š\›Ý”LÓLØÈ^\›˜[[\ÜYÙYYYš[™Ù\œš[X™[È™[XZ[ˆˆH™^˜›Ý[™YTÈÝ\YˆÚÜÙ[‹ÚÝ[›ÝÝ\HH^Yœ™YHØØ[TÈ™X]\™H^\Â›Û›HÛˆH™YH™XYH›ÝÜËÜˆ™\Z\ˆHWØÜØNŒŽ˜ØWØÜØNŒ˜›YØ[™ÜÝXÝ\™HØ\ËˆÈ›Ý[\ÜTÈX™[ËYHTÈ™YÚ\ÝžB™š[™Ù\œš[Üˆ™]\ÙH^\›˜[\™™YØ]]™\È[™\ˆTÈ[[ØÛÜ™\‹™\ÚÛ™KX]Y]\›Z[˜[\™]šY]Ë[™X™[Y˜XÝÜžHØ]\È\ÜË‚•™\šYšXØ][Ûˆ\ÜÙYÚ]Hš[˜[Ë]\Ý[š]ÝZ]K˜[Y]X˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\ØÛÛ\[X[™^\›˜[X™[[˜\šX[[œÜXÝ[Û‹[™Ú]Y™ˆKXÚXÚØ‚‚\ÈÙˆHŒ‹LKLNNŒLÖˆ]]ÛX][Ûˆ[‹\ÙHH\Y˜XÝZYÜ˜][ÛˆØ\Â˜ÚXÚÙYÛ›H\ÈHÝX\™[™™[XZ[œÈÛÜÙYÛ›Û‹X›ØÚÚ[™Îˆ˜[Y]XHÎB[š]]\ÝÝZ]K[™˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[‚‹KXÚXÚË[ØØ[Yš[\Ø[\ÜÙYÚ]HŽ‹[X™[Yš[™Ù\œš[˜\Ù[[™K‚•H[ˆ[ˆ[Ý™YÈ›Ý[™YØÚY[˜ÙHÛÜšÈ[™Ü™X]Y˜\Y˜XÝËÝŒ×Ù\×ÜÜÚ]]™WÙš[™Ù\œš[Ü™XY[™\Ü×ÜXÚÙ]ÌLKšœÛÛ˜‚‚•H™]ÈTÈXÚÙ]XÚØYÙ\ÈHš]™H^\\Ý\ÜYTËÙTË[ZÙBUÜÜÜÜž[]˜[œÙ™\ˆ›Ý[™\žH›ÝÜÈ
WØÜØNŒÍXWØÜØNŒ˜WØÜØNŒŽ˜˜WØÜØN[™WØÜØNŒ˜
H\È™]šY]Ë[Û›H]šY[˜ÙH›ÜˆH]\™HÜÚ]]™B™š[™Ù\œš[ˆ]™XÛÜ™ÈUØ[[XK\ÜÜÜž[]˜[œÙ™\ˆ™XXÝ[Û‹XÙ[\ˆ]šY[˜ÙKšY›Þ[XXØÙ\ÜˆØÛÜKUÓYÌŠÈÛÛ^Y›Û\ÙK]ÜHÛÝ[\™]šY[˜ÙK[™›™ZYÚ›Üš[™ÈUY˜[Z[HÛÛ›ÛËˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆHTÈ[™Bš\È™XYH›Üˆ˜Yš[™Ù\œš[ÜXÚYšXØ][ÛˆÛÜšË]›Ý›Üˆ™YÚ\ÝžB™^[œÚ[Û‹ÛÝ[X›HÙYYX™[ËÜˆ^\›˜[\™[™YØ]]™H]˜[X][ÛˆÛZ[\Ë‚•HXÝ]™HÜÚ]]™Hš[™Ù\œš[[š]™\œÙH™[XZ[œÈÝ\˜]YX™[È™[XZ[ˆŽ‹™^\›˜[[\ÜYÝ][Ù‹\ØÛÜHX™[È™[XZ[ˆ^XÝH[š\›Ý”Í˜[š\›Ý”ÎMX[™[š\›Ý”LÓLØ[™HTÈXÚÙ]^XÚ]H›ØÚÜÂ˜ÛÝ[Ü›ÝÝÛˆ^\›˜[Z\™[™YØ]]™H™KX]Y]\È]\™HØÛÜš[™È[™›X™[Y˜XÝÜžHØ]\Ë‚‚•HØ[YH[ˆ[ÛÈYY˜\Y˜XÝËÝŒ×Ù\×Ù^\›˜[Ú\™Û™YØ]]™WÜ™X]Y]Ü[—ÌLKšœÛÛ˜H™]šY]Ë[Û›B˜ÚXÚÛ\Ý›Üˆ[š\›Ý”Í[š\›Ý”ÎMX[™[š\›Ý”LÓLØˆ]˜ÛÛ™š\›\È[™YH^\›˜[X™[ÛÛ˜XÝÈ[™]šY[˜ÙK\Ù\\˜][ÛˆšY[È\™Bš[XÝ]ÙY\ÈZ\ˆTÈÝ]\È[›™YÛ›ÝÜØÛÜ™YÈ›ÈTÈØÛÜ™K™\ÚÛ\›Z[˜[XÚ\Ú[Û‹ÜˆX™[Ú[™ÙHØ\È›ÙXÙY‚‚“™^]]ÛX][ÛˆÚÝ[ÛÛ[YHœ›ÛH\ÈTÈ™XY[™\ÜÈÝ\™˜XÙHÛ›HYˆ]Ø[‚œÝ^H™]šY]Ë[Û›HÜˆ^XÚ]H[\[Y[HZ\ÜÚ[™È™KXÛÝ[Ø]\ËˆÈ›Ý˜YHTÈš[™Ù\œš[ÈYXÚ[š\ÛWÙš[™Ù\œš[ËšœÛÛ˜[\ÜTÈX™[ËÜ‚\ÙH^\›˜[\™™YØ]]™\È[™\ˆHÚY[™YÛÛÙÞH[[[ˆTÈØÛÜ™\‹š[™\œÙKYØ]H™\ÚÛÛXÞK^\›˜[\™[™YØ]]™H™KX]Y]\›Z[˜[\™]šY]Âœ™\[‹[™X™[Y˜XÝÜžHØ]H[ˆ\™H[\[Y[Y[™\ÜËˆYˆH™^[‚™Ù\È›ÝZÙHTÈ›ÜØ\™ÚÛÜÙH[›Ý\ˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙB›YXÚ[š\ÛK\™XY[™\ÜÈ\ÚÈ˜]\ˆ[ˆ\Y˜XÝZYÜ˜][Û‹‚‚\ÈÙˆHŒ‹LKLNŒÎŒÍ–ˆ]]ÛX][Ûˆ[‹\ÙHH\ÈÛÛ\]H[™œÝÜY]H\ÙHˆ\›Ý˜[ÚXÚÜÚ[ˆH^XÝ][ÛˆX[šY™\ÝØ\Âœ™Yœ™\ÚYYØZ[œÝ]\Ý[YXZ[˜ÛÛ[Z]˜Ì˜ÙNMÙNÎ˜ÌŒØŒX™X™L™˜Í˜MÍŒØÎM˜[™Ý[ÛÝ™\œÈL\™ÙB››Û˜Ø[›ÛšXØ[›ÝÜÈÚ]ZYÜ˜][Û‹\™XYH›ÝÜË™[[ÝHÒKLMˆ™\šYšXØ][ÛœËŒ™\ÝÜ™K]\Ý\ÜÙ\Ë[™™[[Ý˜[]]Üš^˜][ÛœËˆ›ÙXÙ\ˆÝ]\È\È›ÝÂŽÛ›ÝÛ˜[˜]˜Z[X›WÝÚ]Ü™X\ÛÛ˜[™[šÛ›ÝÛ—Ø›ØÚÚ[™ØˆHš[˜[ŒÙ[ÛY]žKY™X]\™H›ÝÜÈœ›ÛHÛXÙ\ÈÍH›ÝYÚLÙ\™HÛÜÙY\Â˜[˜]˜Z[X›WÝÚ]Ü™X\ÛÛ˜˜]\ˆ[ˆÛ›ÝÛŽˆÚ]\ÝÜžH[™HÛÛ[Z]Yœ›ÙÜ™\ÜÈÙÈY[YžHHX™[X˜]ÚØ\Y˜XÝÛÛ[Z]Ë]H^XÝœ\‹\›ÝÈY˜XÙ[\ÛXÙHK\™]\ÙKY^\Ý[™Ø\È‹Û[PÒQˆØXÚHÛÜÝ\™H\È›Ýœ™XÛÛœÝXÝX›Hœ›ÛHÛÛ[Z]YÝ]KˆXXÚ›ÝÈ™\Ù\™\ÈÛÛ[Z]Y]Ú^™K”ÒKLM‹Ú]\™Ù]T’KÛÝ\˜ÙH[œ]Ë›ÙXÙ\ˆÛÛ[X[™]\›‹ÝÛœÝ™X[B˜ÛÛœÝ[Y\œË[™ZYÜ˜][Ûˆ›ØÚÙ\œË‚‚”\ÙHˆ™XY[™\ÜÈÚXÚÛ\Ý›Üˆ[X[ˆ\›Ý˜[ˆÚÛÜÙHH^\›˜[ÝÜ˜YÙB\™Ù]Ù[XÝH\›Ý™Y›ÝÈÝXœÙ]\ØYÛ›HY\ˆ\›Ý˜[™XÛÜ™››Û‹QÚ]\™Ù]Ý\šX˜[Y\Ë[™\[™[H™\šYžH™[[ÝHÒKLM‹[ˆ™\ÝÜ™BœÝXœÙ]\ÝÈœ›ÛHH\ØYY\™Ù]ËÙY\™[[Ý˜[Ø[ÝÙYY˜[ÙX[™™\[‚H[ÛÝ\˜ÙK[Û›H\È™\ÝÜ™YX\Y˜XÝ˜[Y][ÛˆÝZ]Kˆ\ÙHˆ\È›Ý˜]]Üš^™YžHHÝ\œ™[]]ÛX][Ûˆ›Û\[™\ÙHÈÚ]™[[Ý˜[\È[ÛÂ››Ý]]Üš^™Y‚‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈØ\ÈH›Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHBœ›Ý™[˜[˜ÙK[X[šY™\ÝÛÜÝ\™H[™™XY[™\ÜË\™\Ü\ÜËˆ›È\Y˜XÝ\ØY™[][Û‹Ú]”ÈZYÜ˜][Û‹^\›˜[^˜][Û‹X™[Ú[\Ü\Y˜XÝY]œØÚY[YšXËX\Y˜XÝ™XÛÛ\]KÜˆ\ÝÜžH™]Üš]HØ\È\™›Ü›YYˆ™\šYšXØ][Û‚œ\ÜÙYÚ]Ý\\ÎK]\Ý[š]\ØÛÝ™\žKÝ\\ÓH˜[Y]X\™Ù]Y˜\Y˜XÝÝ˜[œÙ™\‹ÜÛÝ\˜ÙK[Û›H\ÝËš[˜[ÎK]\Ý[š]\ØÛÝ™\žKœÛÝ\˜ÙK[Û›HÛÛ\[KÚ[\ÜÐÓKZ[Ý˜[Y]HÛ[ÚÙ\Ë˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[˜˜[Y]KX\Y˜XÝ[ZYÜ˜][Û‚‹KYžK\[ˆKXÚXÚË[ØØ[Yš[\Ø™\ÝÜ™HÛ[ÚÙHžK\[‹˜[œÙ™\‹\ØÛÜHX›XÂ˜ÛÛ˜XÝ[\Ü[™^\›˜[X™[[˜\šX[[œÜXÝ[Û‹ˆX\›H^]^Ù\[ÛŽ‚HYX\Ý\™Y[\ÙY[YHØ\ÈKŒÎÈZ[]\È™XØ]\ÙH[™[XZ[š[™ÈØY™H\ÙHBœÝ\È\™HÛÛ\]H[™H™^XÝ[Ûˆ\È[ˆ\›Ý˜[YØ]Y\ÙHˆÝÜ˜YÙB™XÚ\Ú[Û‹‚‚\ÈÙˆHŒ‹LKLNÎŒÎŒVˆ]]ÛX][Ûˆ[‹\ÙHH™[XZ[œÂš[œÝ[Y[][Û‹[Û›H[™ÛÛ[YYÝ\ˆÛˆHÙ[ÛY]žKY™X]\™H›Ý™[˜[˜ÙB™Ø\ËˆH^XÝ][ÛˆX[šY™\ÝØ\È™Yœ™\ÚYYØZ[œÝ]\Ý[YXZ[˜ÛÛ[Z]˜ÌÌN™Ù˜ØÙXNXÍÍŒØYL™˜MØŒÙX[™Ý[ÛÝ™\œÈL\™ÙB››Û˜Ø[›ÛšXØ[›ÝÜÈÚ]ZYÜ˜][Û‹\™XYH›ÝÜË™[[ÝHÒKLMˆ™\šYšXØ][ÛœËŒ™\ÝÜ™K]\Ý\ÜÙ\Ë[™™[[Ý˜[]]Üš^˜][ÛœËˆ›ÙXÙ\ˆÝ]\È\È›ÝÂŽÛ›ÝÛ˜Mˆ[˜]˜Z[X›WÝÚ]Ü™X\ÛÛ˜[™[šÛ›ÝÛ—Ø›ØÚÚ[™ØˆH™]Â[˜]˜Z[X›H›ÝÜÈ\™H\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÎÍKšœÛÛ˜˜\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÎLšœÛÛ˜˜\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÎLKšœÛÛ˜˜\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÎMLšœÛÛ˜[™˜\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÎMÍKšœÛÛ˜ÈZ\ˆ^XÝ\ÝÜšXØ[˜Y˜XÙ[\ÛXÙHK\™]\ÙKY^\Ý[™Ø\È‹Û[PÒQˆØXÚHÛÜÝ\™H\È›Ýœ™XÛÛœÝXÝX›Hœ›ÛHÛÛ[Z]YÝ]K]XXÚ›ÝÈ™\Ù\™\ÈÛÛ[Z]Y]œÚ^™KÒKLM‹Ú]\™Ù]T’KÛÝ\˜ÙH[œ]Ë›ÙXÙ\ˆÛÛ[X[™]\›‹™ÝÛœÝ™X[HÛÛœÝ[Y\œË[™ZYÜ˜][Ûˆ›ØÚÙ\œËˆH™[XZ[š[™Â˜[šÛ›ÝÛ—Ø›ØÚÚ[™×ØÛÝ[\È[Ù[ÛY]žH™X]\™H\Y˜XÝÈœ›ÛHÛXÙ\ÂŒÍH›ÝYÚLÚ]Y˜XÙ[\ÛXÙH›Ý™[˜[˜ÙHØ\Ë‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈØ\ÈH›Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHBœ›Ý™[˜[˜ÙK[X[šY™\Ý\ÜËˆ›È\Y˜XÝ\ØY[][Û‹Ú]”ÈZYÜ˜][Û‹™^\›˜[^˜][Û‹X™[Ú[\Ü\Y˜XÝY]ØÚY[YšXËX\Y˜XÝ™XÛÛ\]KÜ‚š\ÝÜžH™]Üš]HØ\È\™›Ü›YYˆ™\šYšXØ][Ûˆ\ÜÙYÚ]Ý\\[™š[˜[ÎK]\Ý[š]\ØÛÝ™\žK\™Ù]Y\Y˜XÝÝ˜[œÙ™\‹ÜÛÝ\˜ÙK[Û›H\ÝËœÛÝ\˜ÙK[Û›HÛÛ\[KÚ[\ÜÐÓKZ[Ý˜[Y]HÛ[ÚÙ\ËÓH˜[Y]X˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\Ø™\ÝÜ™HÛ[ÚÙB™žK\[‹^\›˜[X™[[˜\šX[[œÜXÝ[Û‹[™Ú]Y™ˆKXÚXÚØˆH™^˜]]ÛX][Ûˆ[ˆÚÝ[Ý^H[ˆ\ÙHHÝ\ˆÛˆH™[XZ[š[™Â™Ù[ÛY]žKY™X]\™H›Ý™[˜[˜ÙHØ\ÎÈÈ›ÝÝ\\ÙHˆ\ØYÈÚ]Ý]™^XÚ][X[ˆ]]Üš^˜][Û‹‚‚\ÈÙˆHŒ‹LKLNŽŒNVˆ]]ÛX][Ûˆ[‹\ÙHH™[XZ[œÂš[œÝ[Y[][Û‹[Û›KˆH[ˆš\œÝ™\šYšYYÝ\H›ÝYÚÝ\H™XY[™\ÜË[ˆXYHH˜\œ›ÝÈÝ\‹ÔÝ\ÈØY™]H\™[š[™È\ÜÈ[™Û™HÝ\‚œ›Ý™[˜[˜ÙH˜]ÚˆHZYÜ˜][Ûˆ˜[Y]Üˆ›ÝÈ™Z™XÝÈÝÛœÝ™X[KXÛÛœÝ[Y\‚˜XØÛÝ[[™ÈšY[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙH^XÚ]H›ØÚÜÈ[œØY™H™[[Ý˜[˜ÛÛ˜XÝšY\È™\ÝÜ™HÝ™\Üš]HÙˆ[ˆ^\Ý[™ÈZ\ÛX]ÚYš[HÚ]Ý]˜KY›Ü˜ÙXˆH^XÝ][ÛˆX[šY™\ÝØ\È™Yœ™\ÚYYØZ[œÝ]\Ý[YXZ[˜˜ÛÛ[Z]ÙMÌ˜ÌÍX˜ÌNÎMLŒØÍÌŽYÙY˜[™Ý[ÛÝ™\œÈL\™ÙB››Û˜Ø[›ÛšXØ[›ÝÜÈÚ]ZYÜ˜][Û‹\™XYH›ÝÜË™[[ÝHÒKLMˆ™\šYšXØ][ÛœËŒ™\ÝÜ™K]\Ý\ÜÙ\Ë[™™[[Ý˜[]]Üš^˜][ÛœËˆ›ÙXÙ\ˆÝ]\È\È›ÝÂŽÛ›ÝÛ˜LH[˜]˜Z[X›WÝÚ]Ü™X\ÛÛ˜[™ŽH[šÛ›ÝÛ—Ø›ØÚÚ[™ØˆH™]Â[˜]˜Z[X›H›ÝÜÈ\™H\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÌLšœÛÛ˜[™˜\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÌLKšœÛÛ˜ÈZ\ˆ^XÝ\ÝÜšXØ[˜Y˜XÙ[\ÛXÙHK\™]\ÙKY^\Ý[™Ø\È‹Û[PÒQˆØXÚHÛÜÝ\™H\È›Ýœ™XÛÛœÝXÝX›Hœ›ÛHÛÛ[Z]YÝ]K]XXÚ›ÝÈ™\Ù\™\ÈÛÛ[Z]Y]œÚ^™KÒKLM‹Ú]\™Ù]T’KÛÝ\˜ÙH[œ]Ë›ÙXÙ\ˆÛÛ[X[™]\›‹™ÝÛœÝ™X[HÛÛœÝ[Y\œË[™ZYÜ˜][Ûˆ›ØÚÙ\œËˆH™[XZ[š[™Â˜[šÛ›ÝÛ—Ø›ØÚÚ[™×ØÛÝ[\ÈŽK[Ù[ÛY]žH™X]\™H\Y˜XÝÈœ›ÛHÛXÙ\ÂŒÍH›ÝYÚMÍHÚ]Y˜XÙ[\ÛXÙH›Ý™[˜[˜ÙHØ\Ë‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈØ\ÈH›Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHB›X[šY™\ÝÝ˜[Y]Ü‹Ü™\ÝÜ™KÜ›Ý™[˜[˜ÙH\ÜËˆ›È\Y˜XÝ\ØY[][Û‹Ú]“”ÈZYÜ˜][Û‹^\›˜[^˜][Û‹X™[Ú[\Ü\Y˜XÝY]ØÚY[YšXËX\Y˜XÝœ™XÛÛ\]KÜˆ\ÝÜžH™]Üš]HØ\È\™›Ü›YYˆ™\šYšXØ][Ûˆ\ÜÙYÚ]\™Ù]Y˜\Y˜XÝÝ˜[œÙ™\‹ÜÛÝ\˜ÙK[Û›H\ÝË[ÎK]\Ý[š]\ØÛÝ™\žKÓB˜˜[Y]X˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[˜™\ÝÜ™HÛ[ÚÙHžK\[‹™^\›˜[X™[[˜\šX[[œÜXÝ[Û‹[™Ú]Y™ˆKXÚXÚØˆH™^˜]]ÛX][Ûˆ[ˆÚÝ[Ý^H[ˆ\ÙHHÝ\ˆÛˆHŽH™[XZ[š[™Â™Ù[ÛY]žKY™X]\™H›Ý™[˜[˜ÙHØ\ÎÈÈ›ÝÝ\\ÙHˆ\ØYÈÚ]Ý]™^XÚ][X[ˆ]]Üš^˜][Û‹‚‚\ÈÙˆHŒ‹LKLMÕŒÎMŽŒÍVˆ]]ÛX][Ûˆ[‹\ÙHH™[XZ[œÂš[œÝ[Y[][Û‹[Û›H[™ÛÜÙYÛ™HÛÛœÙ\˜]]™H›ÙXÙ\‹\›Ý™[˜[˜ÙH˜[Z[K‚•H^XÝ][ÛˆX[šY™\ÝØ\È™Yœ™\ÚYYØZ[œÝ]\Ý[YXZ[˜ÛÛ[Z]˜™ŽMÙÍYNNŒØ˜LMLLÎYYNNMÍŒLÌX[™Ý[ÛÝ™\œÈL\™ÙB››Û˜Ø[›ÛšXØ[›ÝÜÈÚ]ZYÜ˜][Û‹\™XYH›ÝÜË™[[ÝHÒKLMˆ™\šYšXØ][ÛœËŒ™\ÝÜ™K]\Ý\ÜÙ\Ë[™™[[Ý˜[]]Üš^˜][ÛœËˆHH›ÛÙYZÈÛÛÜ™[˜]BœÚYXØ\œÈ›ÝÈ\ÙH›ÙXÙ\—ÜÝ]\Ï][˜]˜Z[X›WÝÚ]Ü™X\ÛÛ˜ˆZ\ˆ\ÝÜšXØ[™™]ÚÜ™\ÝYÙHÙ\ÜÚ[Ûˆ\È›Ý™XÛÛœÝXÝX›Hœ›ÛHÛÛ[Z]YÝ]K]XXÚœ›ÝÈ™\Ù\™\ÈHÛÛ[Z]Y]Ú^™KÒKLM‹Ú]\™Ù]T’KÛÝ\˜ÙH[œ]Ëœ›ÙXÙ\ˆÛÛ[X[™]\›‹ÝÛœÝ™X[HÛÛœÝ[Y\œË[™ZYÜ˜][Ûˆ›ØÚÙ\œËˆBœ™[XZ[š[™È[šÛ›ÝÛ—Ø›ØÚÚ[™×ØÛÝ[\ÈÌK[Ù[ÛY]žH™X]\™H\Y˜XÝÈÚ]˜Y˜XÙ[\ÛXÙHK\™]\ÙKY^\Ý[™Ø›Ý™[˜[˜ÙHØ\ËˆH˜[Y]Üˆ\™[š[™È\Ý››ÝÈ[ÛÈ›ØÚÜÈ›Û‹QÚ]Ù^\›˜[^™YÝÜ˜YÙH›ÝÜÈ]XÚÈ\™Ù]Ý\šX]™[‚šYˆ›È™[[Ý˜[\È]]Üš^™YY]‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈØ\ÈH›Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHB›X[šY™\ÝÝ˜[Y]Üˆ›Ý™[˜[˜ÙH\ÜËˆ›È\Y˜XÝ\ØY[][Û‹Ú]”Â›ZYÜ˜][Û‹^\›˜[^˜][Û‹X™[Ú[\Ü\Y˜XÝY]ØÚY[YšXËX\Y˜XÝœ™XÛÛ\]KÜˆ\ÝÜžH™]Üš]HØ\È\™›Ü›YYˆ™\šYšXØ][Ûˆ\ÜÙYÚ]\™Ù]Y˜\Y˜XÝÝ˜[œÙ™\‹ÜÛÝ\˜ÙK[Û›H\ÝËÛÝ\˜ÙK[Û›HÛÛ\[K˜[œÙ™\—ÜØÛÜXš[\ÜÓH[ÓH˜[Y]X[ÍË]\Ý[š]ÝZ]K˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\Ø™\ÝÜ™HÛ[ÚÙB™žK\[‹[™Ú]Y™ˆKXÚXÚØˆH™^]]ÛX][Ûˆ[ˆÚÝ[Ý^H[ˆ\ÙBŒH[™ÛÛ[YHÝ\ˆÛˆHÌHÙ[ÛY]žKY™X]\™H›Ý™[˜[˜ÙHØ\ÎÈÈ›ÝÝ\”\ÙHˆ\ØYÈÚ]Ý]^XÚ][X[ˆ]]Üš^˜][Û‹‚‚\ÈÙˆHŒ‹LKLMÕŒŽMÎŒNˆ]]ÛX][Ûˆ[‹\ÙHH™[XZ[œÂš[œÝ[Y[][Û‹[Û›H[™\ÈH›Ý™[˜[˜ÙK\™XYXš[]H\™[š[™ÈÛXÙKˆB™^XÝ][ÛˆX[šY™\ÝØ\È™Yœ™\ÚYYØZ[œÝ]\Ý[YXZ[˜ÛÛ[Z]˜˜LŽMMYNMLÌMÌÍMNMÍLÌYLŒLÎLXŒ™L[™Ý[ÛÝ™\œÈL\™ÙB››Û˜Ø[›ÛšXØ[›ÝÜÈÚ]ZYÜ˜][Û‹\™XYH›ÝÜË™[[ÝHÒKLMˆ™\šYšXØ][ÛœËŒ™\ÝÜ™K]\Ý\ÜÙ\Ë[™™[[Ý˜[]]Üš^˜][ÛœËˆ^XÝ][Ûˆ›ÝÜÈ›ÝÈØ\œžBH›ÙXÙ\ˆÛÛ[X[™\ÝÛÝ\˜ÙH[œ]Ë\˜[Y]\ˆ\ÜÝ[\[ÛœË[™^XÚ]˜›ÙXÙ\—Ü›Ý™[˜[˜ÙWÜ™XÛÝ™\žWÜÝ\ØÈH˜[Y]Üˆ™\]Z\™\ÈÛ›ÝÛˆ›ÙXÙ\œÈÂœ™]Z[ˆÛÛ[X[™È[™[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÝÜÈÈ™]Z[ˆ™XÛÝ™\žHÝ\ËˆH˜›ØÚÙY›ÝÜÈ™[XZ[ˆÌHÙ[ÛY]žH™X]\™H\Y˜XÝÈ[™H›ÛÙYZÈÛÛÜ™[˜]BœÚYXØ\œË[Ú]ÛÝ\˜ÙHÝ]\È\X[WÚ[™™\œ™Y[™[Ý[˜™[[Ý˜[Ø[ÝÙYY˜[ÙXˆHÝÜ˜YÙH[™[ÜžKÜÛXÞKØYZ\ÜÚ[ÛˆÝX\™Ù\™Bœ™Yœ™\ÚYY\ˆH^XÝ][ÛˆX[šY™\ÝÚ[™ÙYÈ[™[ÜžH›ÝÈÛÝ™\œÈ‹N˜\Y˜XÝš[\È[™‹MMŒÈÚPˆÚ]L\™ÙHš[\ËÛXÞH›ØÚÙ\œË[™™[][Ûˆ]]Üš^˜][Û‹‚•™\šYšXØ][Ûˆ\ÜÙYÚ]\™Ù]Y\Y˜XÝÝ˜[œÙ™\ˆ\ÝËÛÝ\˜ÙK[Û›HÛÛ\[K˜˜[œÙ™\—ÜØÛÜX[\ÜÓH[ÓH˜[Y]X[Í‹]\Ý[š]ÝZ]K˜˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[ˆKXÚXÚË[ØØ[Yš[\Ø™\ÝÜ™HÛ[ÚÙB™žK\[‹[™Ú]Y™ˆKXÚXÚØ‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈØ\ÈH›Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHBš[œÝ[Y[][Ûˆ\™[š[™È\ÜËˆ›È\Y˜XÝ\ØY[][Û‹Ú]”Â›ZYÜ˜][Û‹^\›˜[^˜][Û‹X™[Ú[\Ü\Y˜XÝY]ØÚY[YšXËX\Y˜XÝœ™XÛÛ\]KÜˆ\ÝÜžH™]Üš]HØ\È\™›Ü›YYˆH™^]]ÛX][Ûˆ[ˆÚÝ[œÝ^H[ˆ\ÙHH[™Z]\ˆÙY\YÚ[š[™È›Ý™[˜[˜ÙH›ÜˆH˜[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÝÜÈÜˆY[Ü™H™YØ]]™H˜[Y]Üˆ\ÝÎÈÈ›ÝÝ\”\ÙHˆ\ØYÈÚ]Ý]^XÚ][X[ˆ]]Üš^˜][Û‹‚‚\ÈÙˆHŒ‹LKLMÕŒNŽŒÖˆ]]ÛX][Ûˆ[‹\ÙHH™[XZ[œÂš[œÝ[Y[][Û‹[Û›H[™\ÈÛ™HY][Û˜[˜Z[XÛÜÙY˜[Y]Üˆ\™[š[™ÂœÛXÙKˆH˜[Y]KX\Y˜XÝ[ZYÜ˜][Û˜]›ÝÈ™Z™XÝÈ[žB˜ÝÜ˜YÙWØÛ\ÜÏYÚ]^XÝ][Ûˆ›ÝÈÚÜÙH\™Ù]Ý\šX\È›Ý[ˆ^XÚ]˜Ú]ÛÝ\˜ÙWÜ]ÛÛ[Z]˜Y[]HX]Ú[™È›ÝH›ÝÈÛÝ\˜ÙWÜ][™HX[šY™\Ý	ÜÈ™XÛÜ™YÝ\œ™[ÛXZ[—ØÛÛ[Z][™]›ØÚÜÂ˜ZYÜ˜][Û—Ü™XYO]YXÛˆÚ]\™]Z[™Y›ÝÜÈÜˆ[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÙXÙ\‚œ›Ý™[˜[˜ÙKˆHÛÛ[Z]Y^XÝ][Û‚›X[šY™\ÝØ\È™Yœ™\ÚYYØZ[œÝ]\Ý[YXZ[˜ÛÛ[Z]˜ÍY™ŒYYÌYNLYX™MXØ˜ÎLÎY˜˜ŒØÈ]Ý[\ÈL›ÝÜË›ZYÜ˜][Û‹\™XYH›ÝÜË™[[ÝHÒKLMˆ™\šYšXØ][ÛœË[™™[[Ý˜[˜]]Üš^˜][ÛœËˆH[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÝÜÈ™[XZ[ˆ›ØÚÙY]Z\‚œ\‹\›ÝÈ›ÙXÙ\—ÜÝ]\×Ü™X\ÛÛ˜›ÝÈ\Ý[™ÝZ\Ú\ÈHÌHÙ[ÛY]žB˜Y˜XÙ[\ÛXÙHK\™]\ÙKY^\Ý[™Ø›Ý™[˜[˜ÙHØ\Èœ›ÛHHH›ÛÙYZÂ˜ÛÛÜ™[˜]HÚYXØ\ˆ™Y™]ÚÜ™\ÝYÙH\ÚXÛÜÝ\™HØ\Ëˆ™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙH›ÝÂ˜[Y]\ÈHÛÛ[Z]Y^XÝ][ÛˆX[šY™\Ý]Ù[ˆ\ÈH™YØ]]™H]›ÜˆÚ]\™Ù]]ØÛÛ[Z]šYˆH\Y˜XÝÜÚ[\‹ŒX˜[Y]Üˆ›ÝÈ™Z™XÝÈ[\Bœ™\ÝÜ™HÛÛ˜XÝË[˜[YÚ^™KÚ\ÚÜÝÜ˜YÙHY]Y]K[™›Û‹TÒKLMˆ™\ÝÜ™B™\šYšXØ][Ûˆ™Y›Ü™H[žH]\™HÚ[\ˆ™\XÙ[Y[Ø[ˆ\ÜÈ\ÝËˆBœÛÝ\˜ÙK[Û›HÛÛ˜XÝ\Ý[ÛÈÛÝ™\œÈ˜[Y]KX\Y˜XÝ[ZYÜ˜][ÛˆKYžK\[˜˜[™HÜ\œÙKXÚXÚÛÝ]ØÜÈ›ÝÈ[˜ÛYHHÛX[^XÝ][ÛˆX[šY™\ÝÚ]Ý]œ™\ÝÜš[™È\™ÙH\Y˜XÝ^[ØYËˆ™\šYšXØ][Ûˆ\ÜÙYÚ]Íˆ[š]\ÝË\™Ù]Y\Y˜XÝÝ˜[œÙ™\‹ÜÛÝ\˜ÙK[Û›H\ÝËÛÝ\˜ÙHÛÛ\[KÚ[\ÜÐÓBš[Ý˜[Y]KZYÜ˜][Ûˆ˜[Y][ÛˆÚ]ØØ[š[HÚXÚÜË™\ÝÜ™HÛ[ÚÙB™žK\[‹[™Ú]Y™ˆKXÚXÚØ‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈØ\ÈH›Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHBš[œÝ[Y[][Ûˆ\™[š[™È\ÜËˆ›È\Y˜XÝ\ØY[][Û‹Ú]”Â›ZYÜ˜][Û‹^\›˜[^˜][Û‹ØÚY[YšXËX\Y˜XÝ™XÛÛ\]KX™[Ú[\Ü˜\Y˜XÝY]Üˆ\ÝÜžH™]Üš]HØ\È\™›Ü›YYˆH™^]]ÛX][Ûˆ[ˆÚÝ[œÝ^H[ˆ\ÙHH[™ÛÛ[YHÚ]›Ý™[˜[˜ÙHYÚ[š[™È›ÜˆH˜[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÙXÙ\ˆ›ÝÜÈ[›\ÜÈH[X[ˆ^XÚ]H]]Üš^™\È\ÙH‚\ØYË‚‚\ÈÙˆHŒ‹LKLMÕŒNŒLŽNVˆ]]ÛX][Ûˆ[‹\ÙHH™[XZ[œÂš[œÝ[Y[][Û‹[Û›H[™\È™Y[ˆ\™[™YÚ]Ý]\Y˜XÝ\ØYÜˆ™[[Ý˜[‚•H˜[Y]KX\Y˜XÝ[ZYÜ˜][Û˜ÓH›ÝÈ™Z™XÝÈÝ[HÝ\œ™[[XZ[ˆ˜\Ù[[™B›Y]Y]H[™Ý[H›ÝËY\š]™Y^XÝ][ÛˆÛÝ[È™Y›Ü™H[žH]\™H™[[Ý˜[Ø]B˜Ø[ˆ\ÜËˆH^XÝ][ÛˆX[šY™\ÝØ\È™Yœ™\ÚYYØZ[œÝ]\Ý[Y˜ÜšYÚ[‹ÛXZ[˜ÛÛ[Z]MŽÍÌÍXYŽŒYXY˜ÌŽYMÌ˜˜Í™NXØYXÛÈÝ\œ™[˜Ú]ÛÝ\˜ÙWÜ]ÛÛ[Z]ÜÚO˜\™Ù]T’\ÈÚ[]]XZ[ˆ˜\Ù[[™HÚ[BœÝ[™\Ü[™ÈZYÜ˜][Û—Ü™XYWØÛÝ[L™[[ÝWÜÚLM—Ý™\šYšYYØÛÝ[L˜™\ÝÜ™WÝ\ÝÜ\ÜÙYY˜[ÙX[™™[[Ý˜[Ø[ÝÙYØÛÝ[Lˆ]Â˜[šÛ›ÝÛ—Ø›ØÚÚ[™×ÜÝ[[X\žX™XÛÜ™ÈHÝ\œ™[›ØÚÙY›ÙXÙ\ˆ›ÝÜÈ\ÈÌBœ™YÙ[™\˜X›HÙ[ÛY]žH™X]\™H\Y˜XÝÈ[™H›ÛÙYZÈÛÛÜ™[˜]HÚYXØ\œÎÈ\Âš\ÈXYÛ›ÜÝXÈÛ›H[™Ù\È›ÝXZÙH[žH›ÝÈZYÜ˜][Û‹\™XYKˆXXÚ^XÝ][Ûˆ›ÝÂ››ÝÈ[ÛÈ™XÛÜ™ÈHÛÝ\˜ÙH›ÙXÙ\ˆÛÛ[X[™Ý]\È[™H›ÙXÙ\‹\Ý]\È™X\ÛÛ‚œÛÈ\X[WÚ[™™\œ™Y›Ý™[˜[˜ÙH™[XZ[œÈš\ÚX›HY\ˆ˜Z[XÛÜÙYX\[™ÈÂ˜[šÛ›ÝÛ—Ø›ØÚÚ[™Øˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\È\ÈB››Ë\ØÚY[˜ÙK\™XÛÛ\]H\ÙHH\™[š[™ÈÛXÙNÈX™[œ™YÚ\ÝšY\Ë[\ÜYXÚ\Ú[Ûˆ\Y˜XÝË™]šY]˜[Ý]]ËÙ\]Y[˜ÙKY\Ý[˜ÙB›Y]šXÜË[™\™[™YØ]]™HXÚ\Ú[Ûˆ\Y˜XÝÈÙ\™H›ÝY]YˆH™^˜]]ÛX][Ûˆ[ˆÚÝ[ÛÛ[YH\ÙHHÛ›HžHYÚ[š[™ËÙØÝ[Y[[™ÈH˜[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÙXÙ\ˆ›ÝÜË[›\ÜÈH[X[ˆ^XÚ]H]]Üš^™\È\ÙH‚\ØYË‚‚\ÈÙˆHŒ‹LKLMÕNNŒŽŒM–ˆ]]ÛX][Ûˆ[‹\ÙHHÙˆ›Ë[ÜÜÈ\Y˜XÝ›ZYÜ˜][Ûˆ[œÝ[Y[][Ûˆ\È[\[Y[Y[™\ÚY›ÜØ\™œ›ÛHÝ\œ™[˜XZ[˜È›È\ÙHˆ\ØYÜˆ\ÙHÈ\Y˜XÝ™[[Ý˜[\È™Y[ˆ\™›Ü›YY‚˜\Y˜XÝËÝŒ×Ø\Y˜XÝÛZYÜ˜][Û—Ù^XÝ][Û—ÌLKšœÛÛ˜\ÈH^XÝ][ÛˆX[šY™\Ý™›Üˆ\Y˜XÝÛZYÜ˜][Û—Ù^XÝ][Û‹ŒX\š]™Yœ›ÛHH^\Ý[™È™XY[™\ÜÈ[‚˜[™›ÙXÙ\‹ØÛÛœÝ[Y\ˆX[šY™\Ýˆ]\™Ù]Â˜˜\Ù[[™OXÝ\œ™[ÛXZ[—Ý™YWÙ^\›˜[Ú\™Û™YØ]]™\ØÛXÙWÚYLLX[™˜Ø[›ÛšXØ[ØÛÝ[X›WÛX™[ØÛÝ[MŽ˜ÈH^\›˜[[\ÜYÝ][Ù‹\ØÛÜHX™[Âœ™[XZ[ˆ^XÝH[š\›Ý”Í[š\›Ý”ÎMX[™[š\›Ý”LÓLØÚ]Œ[\ÜY^\›˜[ÙYYYš[™Ù\œš[X™[È[™ÛÛÙÞH™\œÚ[Û‚˜X™[Ù˜XÝÜžWÝŒWÎœ‚‚•H^XÝ][ÛˆX[šY™\ÝÛÝ™\œÈL\™ÙH›Û˜Ø[›ÛšXØ[›ÝÜËˆ›ÙXÙ\ˆÝ]\È\ÂŽÛ›ÝÛ˜[™[šÛ›ÝÛ—Ø›ØÚÚ[™ØY\ˆX\[™È\ÝÜšXØ[˜\X[WÚ[™™\œ™Y›Ý™[˜[˜ÙHÈ˜Z[XÛÜÙY›ØÚÚ[™ÈÝ]\Ëˆ]™\žHÝ\œ™[œ›ÝÈ\È^XÚ]HÝÜ˜YÙWØÛ\ÜÏYÚ]Ú]HÚ]ÛÝ\˜ÙWÜ]ÛÛ[Z]ÜÚO˜\™Ù]T’KˆÝ]\ÈÛÝ[È™[XZ[ˆ˜Z[XÛÜÙY‚˜ZYÜ˜][Û—Ü™XYWØÛÝ[L™[[ÝWÜÚLM—Ý™\šYšYYØÛÝ[L˜™[[Ý˜[Ø[ÝÙYØÛÝ[L[™[ÝÜ™Y™[[Ý˜[Ø[ÝÙY˜[Y\È\™H\š]™Y˜žHH˜[Y]Ü‹ˆH™]È˜[Y]KX\Y˜XÝ[ZYÜ˜][Û˜ÓHXØÙ\È\È\ÙBŒH˜Y™XØ]\ÙH]™\žH›ÝÈ\È^XÚ]H›ØÚÙYœ›ÛH™[[Ý˜[È]™Z™XÝÂ›X[›Ü›YY\Ú\Ë[œØY™H›ÙXÙ\‹ÜÝÜ˜YÙHÝ]\ËØ[›ÛšXØ[™[[Ý˜[Z\ÜÚ[™Âœ™\ÝÜ™KÜÝ[[X\žKÝ\™Ù][™›Ü›X][Û‹Z\ÜÚ[™È™[[ÝH\Ú™\šYšXØ][Û‹Z\ÜÚ[™Âœ™\ÝÜ™H\ÝË[˜XØÛÝ[YÝÛœÝ™X[HÛÛœÝ[Y\œË[™[žHÝÜ™Y™[[Ý˜[˜[YB]\ØYÜ™Y\ÈÚ]H\š]™YØ]K‚•HÝÜ˜YÙH[™[ÜžKÜÛXÞHÚZ[ˆØ\È™Yœ™\ÚYY\ˆY[™ÈH^XÝ][Û‚›X[šY™\Ýˆ[™[ÜžH›ÝÈÛÝ™\œÈ‹N\Y˜XÝš[\È[™Ý[\ÈL\™ÙB™š[\ËÛXÞH›ØÚÙ\œË[™[][Ûˆ]]Üš^˜][ÛœË‚‚”™\ÝÜ™HÝ\Ü\È›ÝÈ˜Z[XÛÜÙY›ÝYÚ™\ÝÜ™KX\Y˜XÝØˆ]Ý\ÜÂ˜KYžK\[˜K\]K\ÝXœÙ]Û[ÚÙXØØ[Ùš[H\™Ù]È›Üˆ\ÝËÚ]\™Ù]È›ÜˆÝ\œ™[[‹\™\È›ÝÜË\Ú™\šYšXØ][Ûˆ™Y›Ü™HÜš][™Ë]X\˜[[™B›Ûˆ\ÚZ\ÛX]Ú[™›ÈÝ™\Üš]HÙˆ[ˆ^\Ý[™ÈZ\ÛX]ÚYš[HÚ]Ý]˜KY›Ü˜ÙXˆÚ[\ˆ™XÛÜ™È\™HYš[™Y\È\Y˜XÝÜÚ[\‹ŒXÈ\ÙHHÛ›B˜YÈH›Ü›X][™\ÝÈ[™Ù\È›Ý™\XÙH[žH\Y˜XÝÚ]HÚ[\‹‚”ÛÝ\˜ÙK[Û›H™\›ÙXÚXš[]H\ÝÈ›ÝÈÛÝ™\ˆÛÛ\[X[[\Ü[™Â˜Ø][]X×ÙX\˜[œÙ™\—ÜØÛÜXÓH[ÓH˜[Y]X[™HX›XÂ˜ÛÛ˜XÝ[\Ü›ÜˆH˜[œÙ™\‹\ØÛÜHÞ[X›ÛÈ™]š[Ý\ÛH[›Û™Y[ˆHÛX[‚˜ÚXÚÛÝ]˜Z[\™K‚‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\Y˜XÝZYÜ˜][Ûˆ[œÝ[Y[][Ûˆ\ÈÛÚ\™[™›Üˆ\ÙHH[™Ù\È›Ý[\ˆX™[™YÚ\ÝšY\Ë[\ÜYXÚ\Ú[Ûˆ\Y˜XÝËœ™]šY]˜[Ý]]ËÙ\]Y[˜ÙKY\Ý[˜ÙHY]šXÜËÜˆÝ\ˆØÚY[YšXÈ\Y˜XÝË‚•H™^]]ÛX][Ûˆ[ˆÚÝ[›Ý\ØY™[[Ý™KZYÜ˜]HÈ”ËÜˆ™]Üš]Bš\ÝÜžHÚ]Ý][ˆ^XÚ]\ÙH‹Ô\ÙHÈ[X[ˆ]]Üš^˜][Û‹ˆYˆÛÛ[Z[™ÂÚ][ˆ\ÙHHÛ›KHYÚ\Ý]˜[YH›ÛÝË]\\ÈYÚ[š[™ÈÜˆØÝ[Y[[™ÂH[šÛ›ÝÛ—Ø›ØÚÚ[™Ø›ÙXÙ\ˆ›ÝÜËÚ[HÙY\[™È™[[Ý˜[Ø[ÝÙYY˜[ÙX‚‚\ÈÙˆHŒ‹LKLMÕNŒŽŒMˆ]]ÛX][Ûˆ[‹\Y˜XÝ[™œ˜\ÝXÝ\™H\ÈB™\˜X›H›Ë[ÜÜÈ[›š[™È^Y\ˆ]›ÈZYÜ˜][Ûˆ\È™Y[ˆ\™›Ü›YY‚˜\Y˜XÝËÝŒ×Ø\Y˜XÝÜÝÜ˜YÙWÚ[™[ÜžWÌLKšœÛÛ˜›ÝÈÛÝ™\œÈ‹MÎH\Y˜XÝ™š[\È[™‹MMˆÚPˆÙˆ\Y˜XÝ^[ØYÚ]Lš[\ÈX›Ý™HHHZP‚›\™ÙKYš[H™\ÚÛˆ\Y˜XÝËÝŒ×Ø\Y˜XÝÜÝÜ˜YÙWÜÛXÞWØÚXÚ×ÌLKšœÛÛ˜œ\ÜÙ\ÈÚ]›ØÚÙ\œÈ[™[][Ûˆ]]Üš^˜][ÛœË‚˜\Y˜XÝËÝŒ×Ø\Y˜XÝÜ›ÙXÙ\—ØÛÛœÝ[Y\—ÛX[šY™\ÝÌLKšœÛÛ˜ÛÝ™\œÈ[L›\™ÙH›Û˜Ø[›ÛšXØ[›ÝÜÎˆNH™YÙ[™\˜X›WÚ[\›YYX]X[™H˜]×ØØXÚX›ÝÜËÚ]ŽÛ›ÝÛ˜›ÙXÙ\ˆÛÛ[X[™Ý]\Ù\È[™\X[WÚ[™™\œ™YÝ]\Ù\Ë‚˜\Y˜XÝËÝŒ×Ø\Y˜XÝÛZYÜ˜][Û—Ü™XY[™\Ü×Ü[—ÌLKšœÛÛ˜˜[šÜÈÜÙH›ÝÜÈ\ÂŽØ[™Y]WÙÚ]Ûœ×Û]\˜LHØ[™Y]WÜ™[X\ÙWØ\ÜÙ]Û]\˜[™B˜Ø[™Y]WÛØš™XÝÜÝÜ˜YÙWÛ]\˜Ú[HÙY\[™ÈZYÜ˜][Û—Ü™XYWÛ›Ý×ØÛÝ[L˜[™]]Üš^š[™È›È[][Û‹^\›˜[\ØYÜˆ\ÝÜžH™]Üš]K‚˜\Y˜XÝËÝŒ×Ø\Y˜XÝØYZ\ÜÚ[Û—ÙÝX\™ÌLKšœÛÛ˜\ÜÙ\È™XØ]\ÙH[Ý\œ™[›\™ÙH›Û˜Ø[›ÛšXØ[›ÝÜÈ]™HX[šY™\ÝÛÝ™\˜YÙNÈ]\™H\™ÙH›Û˜Ø[›ÛšXØ[›ÝÜÂ›]\Ý™HØ[›ÛšXØ[]šY[˜ÙHÜˆÙ]H›ÙXÙ\‹ØÛÛœÝ[Y\ˆX[šY™\Ý›ÝÈ™Y›Ü™H^B˜\™HXØÙ\X›KˆØÜËØ\Y˜XÝÜÝÜ˜YÙK›Y›ÝÈØÝ[Y[ÈHÛÝ\˜ÙK[Û›HÜ\œÙB˜ÚXÚÛÝ]][™H™YYÈ^ÜH\ÞKZÙ^HÒUÔÔÒÐÓÓSPS‘›ÜˆBÚÛHÙ\ÜÚ[Û‹[˜ÛY[™È^žH›Øˆ™]Ú\Ëˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆBœ™\ÈÝ[Ø\œšY\ÈH[\Y˜XÝ^[ØY]H™^ÝÜ˜YÙHÝ\\È›ÝÂ˜H[X[‹\™]šY]ÙYZYÜ˜][ÛˆXÚ\Ú[ÛˆÜˆ[Ü™H›Ý™[˜[˜ÙHYÚ[š[™È›ÜˆHœ\X[H[™™\œ™Y›ÝÜË›Ý\Y˜XÝ[][ÛˆÜˆ”ËÛØš™XÝ\ÝÜ˜YÙHZYÜ˜][Û‚˜žH]]ÛX][Û‹‚‚\ÈÙˆ\ÈX[X[[™œ˜\ÝXÝ\™H\ÜË\Y˜XÝZYÜ˜][Ûˆ\È™Z[™ÈÝ\YÚ]Ý][][™ÈÜˆ^\›˜[^š[™È[žHš[\ËˆØÜËØ\Y˜XÝÜÝÜ˜YÙK›YYš[™\ÂH›ËZ[™›Ü›X][Û‹[ÜÜÈ[Nˆ›È\Y˜XÝX^HX]™HÚ][›\ÜÈHÛÛ[Z]Y›X[šY™\Ý™\Ù\™\È]Ú^™KÒKLM‹Ø]YÛÜžK›ÙXÙ\‹Ü›Ý™[˜[˜ÙK™ÝÛœÝ™X[HÛÛœÝ[Y\œË™\XÙ[Y[ÝÜ˜YÙHØØ][ÛˆÚ[ˆ\XØX›K[™BœØÚY[YšXÈÛÛ˜Û\Ú[Ûˆ[ˆHØ[›ÛšXØ[Ý[[X\žKˆH™]È[™[ÜžHÛÛ[™ÈÜš]\Â˜\Y˜XÝËÝŒ×Ø\Y˜XÝÜÝÜ˜YÙWÚ[™[ÜžWÌLKšœÛÛ˜ÛÝ™\š[™È‹MÍ\Y˜XÝ™š[\È[™‹MHÚPˆÙˆ\Y˜XÝ^[ØY]Ü™X][Ûˆ[YKˆ]Û\ÜÚYšY\ÈLˆš[\Â˜\ÈØ[›ÛšXØ[Ù]šY[˜ÙXÍN\È™YÙ[™\˜X›WÚ[\›YYX]XÍŒ\È˜]×ØØXÚX˜[™KÍM\ÈÛÛ\XÝØ\Y˜XÝÈLš[\È\™HX›Ý™HHHZPˆ™\ÚÛˆBœÛXÞHÚXÚÈ[ˆ\Y˜XÝËÝŒ×Ø\Y˜XÝÜÝÜ˜YÙWÜÛXÞWØÚXÚ×ÌLKšœÛÛ˜\ÜÙ\ÂÚ]›ØÚÙ\œÈ[™[][Ûˆ]]Üš^˜][ÛœËˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[‚H™\ÈÝ[Ø\œšY\ÈH[ÞH\Y˜XÝË]]\™HYÙ[È›ÝÈ]™HB››Û‹[ÜÜÞHX[šY™\ÝÜÛXÞHØ]H™Y›Ü™H[žHÝÜ˜YÙHZYÜ˜][Û‹ˆ™^[™œ˜HÛÜšÂœÚÝ[Y[YžH›ÙXÙ\ˆÛÛ[X[™È[™ÝÛœÝ™X[HÛÛœÝ[Y\œÈ›ÜˆH\™Ù\Ýœ™YÙ[™\˜X›KØØXÚH\Y˜XÝÈ™Y›Ü™H[Ýš[™È[ž][™ÈÈ”Ë™[X\ÙH\ÜÙ]ËÜ‚›Øš™XÝÝÜ˜YÙK‚‚\ÈÙˆHŒ‹LKLMÕMÎŒNˆ[‹XZØYÙK\š\ÚÈÛÜÝ\™H\È›ÝÈHXÝ]™Bš[™Ù™ˆÝ]KˆHÜšYÚ[˜[LÙ[XÝY^\›˜[[ÝØ[™Y]\È[™™\Z\™Y›[™\È
ÌMÍM˜M“”ÒŒÍMXNP–XÎR”–ŽÍ˜MLŒØ˜ÍŒMŽÎMLL[™LMN
H\™H™XÛÜ™Y\È]™[ÜY[Ü™]šY]È]šY[˜ÙB›Û›H[ˆ\Y˜XÝËÝŒ×Ù^\›˜[Ü[ÝÜ™\Z\—ÛXZØYÙWØÛÜÝ\™WÌLKšœÛÛ˜È^B›]\Ý›Ý™H\ÙY\ÈÛX[ˆ[[Ý]\™›Ü›X[˜ÙH›ÛÙˆY\ˆØ[™Y]K\ÜXÚYšXÂœ™\Z\‹ˆH™^^\›˜[\™[™YØ]]™H˜[˜ÚH\Èœ›Þ™[ˆ™Y›Ü™HØ[™Y]BœÙ[XÝ[Ûˆ[‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^Ý˜[˜ÚWÜ™\™YÚ\Ý˜][Û—ÌLKšœÛÛ˜Ú]HYš[™Ù\œš[[š]™\œÙKX™[Ù˜XÝÜžWÝŒWÎœ™\ÚÛÛXÞB˜^\›˜[Ú\™Û™YØ]]™WÝ™\ÚÛÜÛXÞWÝŒWÌŒ—ÌWÌMØ›ÛÜˆLMX˜[XÝ\œ™[Yš[™Ù\œš[ËX™[ÝËY›ÛÜˆ[™\œÙHØ]K\XØ]HÛÛ›ÛË™^\›˜[[Û›HÝXÝ\˜[[™ZYÚ›ÜšÛÙ[\ËYZ\ÜÚX›HÛÝ\˜ÙH]šY[˜ÙK™^ÛYYÛÛ^[™ÝXØÙ\ÜËÙ˜Z[\™HÜš]\šXKˆ[\ÜØ]\ÈØ[ˆ›ÝÈ™H[‚Ú]K\™\]Z\™K\™K\™YÚ\Ý˜][Û˜È›ØÚÈ™^]˜[˜ÚH[\ÜÈ]È›Ýœ™Y™\™[˜ÙHHœ›Þ™[ˆ\Y˜XÝÝ™\œÚ[Û‹‚‚•™\ÚÛ›Ý™[˜[˜ÙH\ÈØÝ[Y[Y[‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÝ™\ÚÛÜÛXÞWÌLKšœÛÛ˜ÈØ[™Y]KHÜ‚˜[˜ÚK\ÜXÚYšXÈ™\ÚÛ[š[™È\È\Ø[ÝÙYˆ^\Ý[™È^\›˜[\™›™YØ]]™\È
[š\›Ý”Í[š\›Ý”ÎMX[™[š\›Ý”LÓLØ
H›ÝÈØ\œžBœÙ\\˜]Y™YXÝ]™WÙ]šY[˜ÙX[\ÜÙØ]WÙ]šY[˜ÙX™]šY]×ÛÛ›WØÛÛ^˜[™^ÛYYØÛÛ^šY[Ë[™˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛÛÛÙÞWÜ™X]Y]ÜÛXÞWÌLKšœÛÛ˜™\]Z\™\Âœ™KX]Y]Ú[™]™\ˆHÜÚ]]™Hš[™Ù\œš[[š]™\œÙH^[™Ë\ÜXÚX[H™Y›Ü™B™TËÑ‹RÔ‹ÛXÛÜÚYKZY›Û\ÙK\ÛÛY\˜\ÙKÜˆX\ÙHš[™Ù\œš[Ëˆ]šY[˜ÙB˜˜\ÙYÛÛ™šY[˜ÙHØ[ˆH™YÚ\ÝžH™[XZ[œÈ]ŽˆX™[È[™HÝ\œ™[›XZØYÙHÛÛ›ÛÈ\™HÛÚ\™[ÈH™^Z[\ÝÛ™HÚÝ[™H[™œ˜\ÝXÝ\™H[™˜\Y˜XÝÝ˜]YÞH™Y›Ü™HTÈ^[œÚ[ÛˆÜˆœ›ØYØØ[K]\›Ý[Ü™HKPÔÐBœÝšXÝUH™\Z\ˆÜˆ™\Z\™Y\[Ý\™›Ü›X[˜ÙHÛZ[\Ë‚‚\ÈÙˆHŒ‹LKLMÕMNNŒLVˆ[‹H›Ú™XÝY›Ý™[Ü[ˆHÝ\\œÙYY“ÌMÍM‹ÔM“”ÒŒ[\Ü][\ˆ[œÝXY]Ü[™YH›Ý[™YÜÝTÍœ™]šY]Ë[Û›HÛÝ\˜Ú[™ÈÝ\™˜XÙH[™˜[ˆHš\œÝÙ\]Y[˜ÙH\XØ]HØÜ™Y[œË‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜÜÝÜÍÜÛÝ\˜Ú[™×ÌLKšœÛÛ˜^ÛY\ÂHš[Üˆœ™\Ú™^XØ[™Y]Kœ›ØY\‹\ÝXÝ\˜[[™ŒŽÌY™\œ˜[œÝ\™˜XÙ\Ë[ˆÙ[XÝÈÚ^›Û‹XÛÝ[X›HÛÝ™\™Y[[™H›ÝÜÎˆŒÎLŒXÎX˜LLLÎLŽXLML[™NM’’ØˆHÝ\œ™[\™Y™\™[˜ÙHS\Ù\\Ì‚œØÜ™Y[ˆ[™^\›˜[[]œËX[Ù\]Y[˜ÙHØÜ™Y[ˆ›Ý™\Ü‹Íˆ›Ë\ÚYÛ˜[›ÝÜÂÚ]ÝX\™˜Z[XÛX[ˆ]Y]ËˆHÝXÝ\˜[›ÛÝË]\X]\šX[^™\È[Ú^[Q›ÛÚYXØ\œËÛÛ\]\ÈHMKÌMH^\›˜[[]œËX[›ÛÙYZÈØXÚK[™œØÜ™Y[œÈ[Ú^›ÝÜÈYØZ[œÝÝ\œ™[ÛÝ[X›HÝXÝ\™\Ëˆ]™\žH›ÝÈ\ÈBšYÚUHÝ\œ™[XÛÝ[X›H\XØ]HÚYÛ˜[ÛÂ˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜÜÝÜÍÝ\›Z[˜[ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜œ™XÛÜ™ÈÚ^\›Z[˜[™]šY]Ë[Û›H\XØ]H™Z™XÝ[ÛœÈÚ][\Ü\™XYH›ÝÜÂ˜[™ÛÝ[X›HØ[™Y]\Ëˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆ\ÈÝ\™˜XÙH\Â˜ÛÜÙYžHÝXÝ\˜[\XØ]H]šY[˜ÙNÈ™^ÛÜšÈ™YYÈœ™\ÚÛÝ\˜Ú[™È˜]\‚[ˆ™]žZ[™È\ÙHÚ^›ÝÜËˆ™\šYšXØ][Ûˆ\ÜÙYÚ]H[š]\ÝË˜˜[Y]XÝ™\ˆŽˆÝ\˜]YX™[ËÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ‚‚\ÈÙˆHŒ‹LKLMÕMŒÎŒÎˆ™\šYšXØ][Ûˆ[‹H]\Ý\ÚY™\ÜÚ]ÜžBœÝ]HÝ\\œÙY\ÈHÛ\ˆÌMÍM‹ÔM“”ÒŒ[\ÜX][\›Û\ˆHÛËXØ[™Y]B˜][\\È[™XYH\›Z[˜[HÛÜÙYÍÎMX[™LÓLØ\™HB›Û›H^\›˜[ÛÝ[X›H\™™YØ]]™\Ë[™HØ[›ÛšXØ[™YÚ\ÝžH™[XZ[œÈ]ŽˆX™[ÎˆŒLˆÙYYYš[™Ù\œš[ÜÚ]]™\È[™ÌÝ][Ù‹\ØÛÜHX™[Ë‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆHÝ\œ™[Ý]H\ÈÛÚ\™[[™ÚÝ[›Ýœ™[Ü[ˆÌMÍM‹ÔM“”ÒŒŒŽÌHœ›ØY\ˆ\XØ]K\ÚYÛ˜[™Z™XÝËHÚ^›ÜšYÚ[˜[[Ý™\Z\ˆ[™\ËÜˆKPÔÐHÝšXÝH™\Z\ˆÚ]Ý]^XÚ]™]Â™]šY[˜ÙKˆÝ\\™\šYšXØ][Ûˆ\ÜÙYÚ]H[š]\ÝÈ[™˜[Y]XÝ™\‚ŽˆÝ\˜]YX™[ËˆØÜËÛX™[Ù˜XÝÜžK›YØ\ÈÛÜœ™XÝYÈX]ÚHÝ\œ™[Ž‹[X™[Ý]K‚‚\ÈÙˆHŒ‹LKLMÕLÎŒÍÎŒÍˆ[‹Í\È[\ÜY\ÈH\™^\›˜[›Ý][Ù‹\ØÛÜH\™[™YØ]]™HX™[ˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆH[\Ü\Â™Y™[œÚX›H[™\ˆHÝ\œ™[Yš[™Ù\œš[ÛÛÙÞH™XØ]\ÙH\›Z[˜[™]šY]Ë˜›Ý[™Y\XØ]HÛÛ›ÛË\™Ù]Y[™Ý\œ™[\™Y™\™[˜ÙH[šT™YŽLÍLÚXÚÜË˜Ý\œ™[XÛÝ[X›H›ÛÙYZÈØÜ™Y[š[™Ë[N[™\œÙKYØ]HØÛÜš[™ËH˜\Ù[[™B›X™[Y˜XÝÜžHØ]K[™H^\›˜[]˜[œÙ™\ˆØ]H[\ÜËˆHØ[›ÛšXØ[œ™YÚ\ÝžH›ÝÈ\ÈŽˆX™[ÎˆÎHXØÙ\YKPÔÐHX™[ËŒLˆÙYYYš[™Ù\œš[œÜÚ]]™\Ë[™ÌÝ][Ù‹\ØÛÜHX™[È[˜ÛY[™È[š\›Ý”Í˜[š\›Ý”ÎMX[™[š\›Ý”LÓLØ‚‚“™]È\Y˜XÝÎ‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[Ý\›Z[˜[Ü™]šY]×ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜œ™XÛÜ™ÈÍ\ÈXØÙ\YÛÝ]ÛÙ—ÜØÛÜWÜ[™[™×Ù˜XÝÜžWÙØ]X[™˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[Ù˜XÝÜžWÚ[\ÜÙØ]WÌLKšœÛÛ˜œÙ[XÝÈ^XÝHÍ[™\ˆHÚ[™ÛKZ[\ÜØ\Ú[H[ÝÚ[™ÈHÛÈš[Ü‚™^\›˜[X™[ÈÛ›H\È[™XYÙKˆÜÝZ[\Ü™YÜ™\ÜÚ[Ûˆ^XÝ][ÛœÈÙ\™B\]YÈŽˆÝ[X™[È[™ÌÝ][Ù‹\ØÛÜHX™[Ëˆ™^\™XÝÛÜšÈÚÝ[˜]›ÚY™[Ü[š[™ÈHš]™Hœ›ØY\‹\Ý\™˜XÙH\XØ]K\ÚYÛ˜[™Z™XÝÈ[™ÚÝ[œÛÝ\˜ÙHÜˆØÜ™Y[ˆHœ™\ÚÝXÝ\˜[HÝÙ\‹\š\ÚÈ^\›˜[\™[™YØ]]™HÝ\™˜XÙB›Û›HYˆ[›Ý\ˆ^XÚ][\ÜÞXÛH\È™\]Y\ÝY‚‚\ÈÙˆHŒ‹LKLMÕNŒŒÎŒŽˆ[‹Hš\œÝ^\›˜[\™[™YØ]]™H[\Ü˜][\\ÈÛÜÙYÚ]Ý]ÛÝ[Ü›ÝÝˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆB™^\›˜[Ý][Ù‹\ØÛÜH[™\œÙHØ]H\È›ÝÈ^XÚ][™\ÝXÛÝ™\™Y›ÜˆB˜Ý\œ™[Yš[™Ù\œš[ÛÛÙÞK]™Z]\ˆÌMÍMˆ›ÜˆM“”ÒŒ\ÈY™[œÚX›H\Â˜[ˆ[\Ü\™XYH\™™YØ]]™H™XØ]\ÙH\XØ]KÜÝ\™\Z\ˆ™]šY]Ë[™[™˜XÝÜžHØ]\ÈÝ[›ØÚÈ[K‚‚˜YXÚ[š\ÛSX™[›ÝÈØ\œšY\ÈÛÛÙÞWÝ™\œÚ[Û—Ø]ÙXÚ\Ú[Û˜Ú]^\Ý[™Âœ™YÚ\ÝžHX™[ÈZYÜ˜]YÈX™[Ù˜XÝÜžWÝŒWÎœˆ^\›˜[\›Z[˜[[™œÜÝ\™\Z\ˆXÚ\Ú[Ûˆ\Y˜XÝÈ›ÝÈØ\œžH\™Ù]ÛX™[Ý\O[Ý]ÛÙ—ÜØÛÜX˜\™Ù]Ùš[™Ù\œš[ÚY[[[™HØ[YHÛÛÙÞH™\œÚ[ÛˆÛÈ]\™HÛÛÙÞB™^[œÚ[ÛˆØ[››Ý™]›ØXÝ]™[HÚ[™ÙH\È\™[™YØ]]™HXÚ\Ú[ÛˆÝ\™˜XÙK‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÛÝ]ÛÙ—ÜØÛÜWÚ[™\œÙWÙØ]WÛÙÚX×ØÚXÚ×ÌLKšœÛÛ˜™XÛÜ™Â”Ý\PH\È\ÜÙYˆÝ\˜]YÝ][Ù‹\ØÛÜHX™[ÈÝ[™Z™XÝ›Û‹[[™š[™Ù\œš[È[™X›Ý™K]™\ÚÛ™]Z[™Y]Ë[™HÌMÍM‹ÔM“”ÒŒ^\›˜[œÜÝ\™\Z\ˆ]È™\]Z\™H[Ý\œ™[š[™Ù\œš[ØÛÜ™\È™[ÝÈHXÝ]™B˜LMX›ÛÜ‹ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÙ—ÙX×ÌWÌWÌWØÛÛœÚ\Ý[˜ÞWØÚXÚ×ÌLKšœÛÛ˜œ™XÛÜ™ÈÝ\Pˆ\È\ÜÙYÛˆH›Ý[™YÑˆÚXÚÎˆÍ‹ÌÍˆ]˜[XX›HÑ‹[ZÙB”ÝÚ\ÜËT›ÝPÈKŒKŒKž›ÝÜÈÙ\™HÛX[ˆXœÝ[[ÛœËÚ]Ñˆ˜[ÙB››Û‹XXœÝ[[ÛœÈ[™™YXÝ]™H^Ø[››Ý][ÛˆXZØYÙH›ÝÜË‚‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÝÛ×ØØ[™Y]WÚ[\ÜØ][\ÌLKšœÛÛ˜[ˆšYY^XÝHH™\]Y\ÝYÛÈØ[™Y]\ËˆÌMÍMˆ\ÜÙ\ÈH[™\œÙHØ]BÚ]ÜH[YWÜ\›ÞY\ÙWÛÞY\ÙXØÛÜ™HŒÌÎXÈM“”ÒŒ\ÜÙ\ÈÚ]ÜB˜Y][Ù\[™[ÚY›Û\ÙXØÛÜ™HŒÍML˜ˆ›Ý›ÝÜÈ™[XZ[‚˜[\ÜØ›ØÚÙY[\ÜÜ™XYWØØ[™Y]OY˜[ÙX[™›Û‹XÛÝ[X›H™XØ]\ÙB˜œ›ØY\ˆ\XØ]HØÜ™Y[š[™Ë\›Z[˜[ÜÝ\™\Z\ˆ™]šY]ÈXØÙ\[˜ÙK[™B™[^\›˜[˜XÝÜžHØ]H\™H[œ™\ÛÛ™YˆÈ›ÝžHÍMKNP–KÎR”–Ž”Í‹Üˆ[žH\™ÜšYÚ[˜[[ÝØ[™Y]H[ˆ\ÈÞXÛK‚‚™XØ]\ÙH›Ýš\œÝØ[™Y]\È˜Z[YÝšXÝ™XY[™\ÜË˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜÙXÛÛ™Ý˜[˜ÚWÜÙ[XÝ[Û—ÌLKšœÛÛ˜Ý\ÂH™^™]šY]Ë[Û›H\™[™YØ]]™H˜[˜ÚHÚ]ÌÌKLLÎLË[™ÍNLM\Â›ÝÙ\‹\š\ÚÈØ[™Y]\ËˆŒMÍ\È^XÚ]H^ÛYY›ÜˆYÚ˜Ý\œ™[\™Y™\™[˜ÙHY[]H
ŽNX
K[™NP–ÌH\È^ÛYY™XØ]\ÙHLLÎLÂ˜[™XYH™\™\Ù[ÈHØ[YH^\›˜[HHØÛ\Ý\‹ˆ\ÙH˜[˜ÚKLˆ›ÝÜÂ˜\™H›Ý[\Ü\™XYH[™›ÝÛÝ[X›KˆHŒ‹LKLMÕŽŒŒÎNVˆ[ˆ[‚˜YY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜÙXÛÛ™Ý˜[˜ÚWØÝ\œ™[ØÛÝ[X›WÜÝXÝ\˜[ÜØÜ™Y[—ÌLKšœÛÛ˜ÚXÚ[œÈ›ÛÙYZÈÝ™\ˆÜÙHÈ^\›˜[›ÝÜÈYØZ[œÝÌˆÝYÙYÝ\œ™[œÙ[XÝYÝXÝ\™\Ëˆ›ÛÙYZÈÛÛ\]Y]Û›HŒKÌŒMˆ]Y\žK]\™Ù]Z\œÂÙ\™H™\ÜY[™[™YHYZ]Y›ÝÜÈ]™HYÚUHÝ\œ™[XÛÝ[X›BœÝXÝ\˜[ÚYÛ˜[ÎˆÌÌHÈWØÜØNÌÍX]ÌŒØLLÎLÈÈWØÜØNŒNL˜]ŽŽ˜[™ÍNLMÈWØÜØNŒÌŽ]ÍŒÎˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙB˜Ø[ˆ˜[˜ÚKLˆ[\Ü™XY[™\ÜÈ\È›ÝÈÝÙ\‹›ÝYÚ\‹‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜÙXÛÛ™Ý˜[˜ÚWÝ\›Z[˜[ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜œ™XÛÜ™È[™YHYZ]Y›ÝÜÈ\È\›Z[˜[™]šY]Ë[Û›B˜™Z™XÝYØÝ\œ™[ØÛÝ[X›WÜÝXÝ\˜[Ù\XØ]WÜÚYÛ˜[Ý]ÛÛY\ÈÚ]š[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›HX™[Ë‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜÙXÛÛ™Ý˜[˜ÚWÜ™\XÙ[Y[ÝšXYÙWÌLKšœÛÛ˜[ˆšXYÙ\ÈHÝ\œ™[K\›ÝÈÛÛ[™YZ]È™\XÙ[Y[Ëˆ™^\™XÝÛÜšÈ\È›ÝÈ[Ý™YÈœ™\Ú^\›˜[ÛÝ\˜Ú[™È˜]\ˆ[ˆ™XÛÛœÚY\š[™È\ÂœÛÛÈÈ›Ý™]žHÌÌKÔLLÎLËÔÍNLMÜˆ™[Ü[‚“ÌMÍM‹ÔM“”ÒŒÔÍMKÔNP–KÐÎR”–ŽÔÍˆ™\Z\ˆ[™\È[ˆ\ÈÞXÛHÚ]Ý]›™]È^\]šY[˜ÙKˆHŒ‹LKLMÕÎŒNŒVˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™]×ØØ[™Y]WÜÛÝ\˜Ú[™×ÌLKšœÛÛ˜Bœ™]šY]Ë[Û›H^[™YÝÚ\ÜËT›ÝÛÝ\˜Ú[™È\ÜËˆ]^ÛY\ÈHÝ\œ™[^\›˜[œÛÛÙY\ÈÛ›HÛÝ™\™YYXÚ[š\ÛH[™\Ë[™š[™È™]È›ÝÜÈÚ]^XÚ]•[šT›ÝXÝ]™K\Ú]H[™Ø][]XËXXÝ]š]HÛÛ^ˆÍÍNŽÎMLMM˜ÎMMÎXNŒÌM˜LÍŒ[™LLÌØˆ]šY[˜ÙKX˜\ÙY˜ÛÛ™šY[˜ÙHØ[ˆ\È™[[Ý™\ÈH[[YYX]H››È™]ÈØ[™Y]\ÈˆÛÝ\˜Ú[™Â˜›ØÚÙ\‹]]Ù\È›ÝÜ™X]H[ˆ[\Ü\™XYH˜[˜ÚKˆ]™\žHÛÝ\˜ÙY›ÝÂœÝ[™YYÈ\XØ]KÜ™]šY]ËÙ˜XÝÜžH]šY[˜ÙH™Y›Ü™H[žH[\Ü][\ˆBœØ[YH[ˆ[ÛÈYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™]×ØØ[™Y]WØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜˜[™]È]Y]›ÜˆÜÙH›ÝÜËˆHS\Ù\\ÌˆÝ\œ™[\™Y™\™[˜ÙHØÜ™Y[ˆ\Â˜ÛÛ\]H[™ÝX\™˜Z[XÛX[ŽˆÈ›ÝÜÈ]™H›È™X\‹Y\XØ]HÚYÛ˜[Ú[B˜LÍŒ\È[ˆ^XÝ\™Y™\™[˜ÙHÛÝ]ÈWØÜØNŒÌ˜ÈÈ›ÝØ\œžHLÍŒš[È[ˆ[\Ü][\‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™]×ØØ[™Y]WÜÝXÝ\˜[ØÛ\Ý\—Ú[™^ÌLKšœÛÛ˜˜[™XYHÛÝ™\œÈH^\›˜[[]œËX[ÚYH›ÜˆHÛÝ\˜ÙY›ÝÜÎˆ[[Q›ÛÛÛÜ™[˜]HÚYXØ\œÈ\™HÝYÙYŽÌŽ[›Ü™\™Y›ÛÙYZÈZ\œÈ\™B˜ÛÝ™\™Y[™Û›HØÌM˜Û\Ý\ˆ]HLØ
ŽÌÎ
K‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™]×ØØ[™Y]WØÝ\œ™[ØÛÝ[X›WÜÝXÝ\˜[ÜØÜ™Y[—ÌLKšœÛÛ˜››ÝÈØÜ™Y[œÈHÈÙ\]Y[˜ÙH›Ë\ÚYÛ˜[›ÝÜÈYØZ[œÝÌˆÝ\œ™[ÛÝ[X›BœÙ[XÝYÝXÝ\™\ËˆHŒ‹LKLMÕŒŽŒÍVˆ[ˆš^YH›ÛÙYZÂ›][K[[Ù[\™Ù][X\ÈX\\ˆ
—ÌSQR×ÓSÑSÌÍ×ÐX›ÝÈX\È˜XÚÈÂ˜—ÌSQRØ
H[™™\˜[ˆHØÜ™Y[‹ˆHZ\ˆØXÚH\È›ÝÈÛÛ\]H]ÌÍÌ[š\]YH]Y\žK]\™Ù]Z\œË[™[ÈÙ\]Y[˜ÙKXÛX[ˆ›ÝÜÈ]™HYÚUB˜Ý\œ™[XÛÝ[X›H\XØ]HÚYÛ˜[ËˆLLÌØ\È›ÈÛ™Ù\ˆHšXX›H›Ë\ÚYÛ˜[˜Ø[™Y]Nˆ]ÈÛÛ\]YXØXÚH™X\™\ÝÝ\œ™[XÛÝ[X›H]\ÈÙ[XÝYœÝXÝ\™HSQRØ]OLŽLÎXˆH™]Â˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™]×ØØ[™Y]WÝ\›Z[˜[ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜˜\Y˜XÝ™XÛÜ™È[È›ÝÜÈ\È\›Z[˜[™]šY]Ë[Û›B˜™Z™XÝYØÝ\œ™[ØÛÝ[X›WÜÝXÝ\˜[Ù\XØ]WÜÚYÛ˜[Ý]ÛÛY\ËÚ]š[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›HX™[Ëˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆB™œ™\ÚÛÝ\˜ÙY˜[˜ÚH\ÈÛÜÙYžHÝ\œ™[XÛÝ[X›HÝXÝ\˜[\XØ]BœÚYÛ˜[Ë›ÝžH[ˆ[œ™\ÛÛ™Y›ØÙ\ÜÈ›ØÚÙ\‹ˆHŒ‹LKLMÕNŒŽŒˆ[‚[ˆÜ[™YH™^™\XÙ[Y[ÛÝ\˜Ú[™ÈÝ\™˜XÙHÚ]Ý]™]žZ[™ÈÜÙH›ÝÜË‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÜÛÝ\˜Ú[™×ÌLKšœÛÛ˜™^ÛY\ÈHÜšYÚ[˜[Ì\›ÝÈÛÛHÙXÛÛ™]˜[˜ÚH\XØ]H™Z™XÝË[™˜[š[Üˆœ™\ÚÛÝ\˜ÙY›ÝÜË[ˆYZ]È™\XÙ[Y[ÛÝ™\™Y[[™B”ÝÚ\ÜËT›Ý›ÝÜÈÚ]^XÚ][šT›ÝXÝ]™K\Ú]H\ÈØ][]XËXXÝ]š]B˜ÛÛ^ˆÌÎ˜MŒNQÖ•ŒŽÌNŽL˜˜ÎMX[™LÓLØˆH›Ý[™YÝ\œ™[\™Y™\™[˜ÙHS\Ù\\ÌˆØÜ™Y[‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜˜[™]Y]™XÛÜ™Î›Ë\ÚYÛ˜[›ÝÜË^XÝ\™Y™\™[˜ÙHÛÝ]Ë›™X\‹Y\XØ]H›ÝÜË[™[\Ü\™XYKØÛÝ[X›H›ÝÜËˆHØ[YH[ˆ[ÛÂœÝYÙYH™\XÙ[Y[ÝXÝ\˜[Ý\™˜XÙN‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÜÝXÝ\˜[ØÛ\Ý\—Ú[™^ÌLKšœÛÛ˜›X]\šX[^™\ÈÎ[Q›ÛÚYXØ\œËÛÝ™\œÈŽÌŽ^\›˜[[]œËX[›ÛÙYZÂœZ\œË[™š[™ÈYÚUH^\›˜[Z\œË‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WØÝ\œ™[ØÛÝ[X›WÜÝXÝ\˜[ÜØÜ™Y[—ÌLKšœÛÛ˜[ˆÛÛ\]\ÈHÝ\œ™[XÛÝ[X›H›ÛÙYZÈØÜ™Y[ˆÝ™\ˆLÍÍ‹ÍLÍÍ‚œ]Y\žK]\™Ù]Z\œËˆš]™H›ÝÜÈ]™HYÚUHÝ\œ™[XÛÝ[X›H\XØ]HÚYÛ˜[ÂŠÌÎ˜MŒNŽL˜[™NQÖ•
KÚ[HŒŽÌ˜ÎMX[™LÓLØ]™H›ÈÝ\œ™[XÛÝ[X›HÝXÝ\˜[\XØ]HÚYÛ˜[]˜HLØˆ\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÝ\›Z[˜[ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜œ™XÛÜ™ÈH™]šY]Ë[Û›H\XØ]K\ÚYÛ˜[™Z™XÝ[ÛœÈ[™È™]šY]Ë[Û›HY™\œ˜[Â][š]X[H™[XZ[ˆ›ØÚÙYžH[šT™Y‹]ÚYH\XØ]HØÜ™Y[š[™Ë\›Z[˜[œ™]šY]Ë[™[˜XÝÜžHØ]\Ëˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆH[[YYX]B››Ë[™]ËXØ[™Y]\È›ØÚÙ\ˆ\È™[[Ý™Y[™\ÈÝ\™˜XÙH\ÈÈÝXÝ\˜[B››Û‹Y\XØ]H›ÛÝË]\›ÝÜË]›Û™H\È[\Ü\™XYHÜˆÛÝ[X›HY]‚•HŒ‹LKLMÕŽŒŽNŒˆ[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WØ[Ýœ×Ø[ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜˜[™˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WØ[Ýœ×Ø[ÜÙ\]Y[˜ÙWÜÙX\˜ÚØ]Y]ÌLKšœÛÛ˜‚•H›Ý[™Y^\›˜[[]œËX[Ù\]Y[˜ÙHØÜ™Y[ˆÛÝ™\œÈHØ[YH™\XÙ[Y[œ›ÝÜËÛÛ\]\ÈÚ]Î›Ë\ÚYÛ˜[›ÝÜËš[™È^XÝÛ™X\‹Y\XØ]H^\›˜[œÙ\]Y[˜ÙHZ\œË[™™[XZ[œÈÝX\™˜Z[XÛX[ˆÚ[H™\Ù\š[™ÈH[šT™Y‹]ÚYB˜›ØÚÙ\‹ˆH™]Â˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÙ\XØ]WÙ]šY[˜ÙWÜ™]šY]×ÌLKšœÛÛ˜›˜\œ›ÝÜÈHÝ\š]š[™ÈÝ\™˜XÙHÈŒŽÌÎMX[™LÓLØˆ[È\™B˜›Ý[™YÙ\XØ]WØÛÛ›Û×ØÛX\—Ý[š\™Y—Ü[™[™ØYX[š[™È›Ý[™Y˜Ý\œ™[\™Y™\™[˜ÙHÙ\]Y[˜ÙK^\›˜[[]œËX[Ù\]Y[˜ÙK^\›˜[ÝXÝ\˜[˜[™Ý\œ™[XÛÝ[X›HÝXÝ\˜[ÛÛ›ÛÈ\™HÛX\‹ˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙB˜Ø[ˆ\ÙHÈ›ÝÜÈ\™H›ÝÈ™]\ˆ\XØ]K\ØÜ™Y[™Y[ˆH™]š[Ý\Âœ™\XÙ[Y[Ý\™˜XÙK]]\ÈÝYÙH›Û™H\È[\Ü\™XYH™XØ]\ÙH[šT™Y‹]ÚYB™\XØ]HØÜ™Y[š[™Ë\›Z[˜[™]šY]ÈXØÙ\[˜ÙK[™[˜XÝÜžHØ]\ÈÝ[˜›ØÚÈ[ËˆHØ[YH[ˆ[ÛÈYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÝ\›Z[˜[Ü™]šY]×Ü]Y]YWÌLKšœÛÛ˜ÚXÚXÚØYÙ\ÈÜÙHÈ›ÝÜÈ[È™]šY]Ë[Û›H\›Z[˜[™]šY]ÈXÚÙ]ÈÚ]™^XÚ][ÝÙYÝ]ÛÛY\È[™™[XZ[š[™È›Û‹Z[X[ˆ›ØÚÙ\œÎÈ]XØÙ\ËÚ[\ÜÂŒ›ÝÜËˆH›ÛÝË[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÝ\™Ù]YÝ[š\™Y—ØÚXÚ×ÌLKšœÛÛ˜œ]Y\šY\È[šT™YŽLÍL[™\È›ÜˆXXÚ]Y]YYØ[™Y]H[™]È™X\™\ÝÝ\œ™[œÝXÝ\˜[\™Y™\™[˜ÙHXØÙ\ÜÚ[Û‹ˆŒŽÌœÈLNÎMXœÈÍL˜[™LÓLØœÈŒŒLØ]™HÚ\™Y[šT™YŽLÍLÛ\Ý\œÈ[™™]Ú™˜Z[\™\ËˆHŒ‹LKLMÕÎŒŽNŒÍ–ˆ[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÝ[š\™Y—ØÝ\œ™[Ü™Y™\™[˜ÙWÜØÜ™Y[—ÌLKšœÛÛ˜ÚXÚ™]Ú\ÈXXÚØ[™Y]IÜÈ[šT™YŽL[™[šT™YLÛ\Ý\ˆY[X™\œÈ[™š[\œÙXÝÈ[HÚ][ÌÍHÝ\œ™[ÛÝ[X›H™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœËˆŒŽÌ˜ÎMX[™LÓLØ[]™HÝ\œ™[\™Y™\™[˜ÙHÛ\Ý\ˆÝ™\›\ËÚ]‹Í‚˜Ø[™Y]H[šT™YˆÛ\Ý\œÈ™]ÚYÝXØÙ\ÜÙ[Kˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[‚HÝ\š]š[™È™^XØ[™Y]HÝ\™˜XÙH›ÈÛ™Ù\ˆ\ÈHÝ\œ™[\™Y™\™[˜ÙH[šT™Y‚˜Û\Ý\ˆ\XØ]H›ØÚÙ\‹ˆHŒ‹LKLMÕŒÌNŒÖˆ[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÚ[™\œÙWÙØ]WÜØÛÜ™\×ÌLKšœÛÛ˜ÚXÚX\ÈH[šT›ÝXÝ]™K\Ú]H™X]\™\È›ÜˆÜÙHÈ›ÝÜÈÛÈZ\ˆÝYÙY[Q›ÛÚYXØ\œÈ[™™\šYšY\ÈÛÛ\]HÎÝ\œ™[Yš[™Ù\œš[ÛÝ™\˜YÙH™[ÝÂHLMXÝ][Ù‹\ØÛÜH›ÛÜŽˆŒŽÌÜHY][Ù\[™[ÚY›Û\ÙX˜ŒÍŽ˜ÎMXÜH›]š[—ÙZY›ÙÙ[˜\ÙWÜ™YXÝ\ÙXŒLML[™˜LÓLØÜHY][Ù\[™[ÚY›Û\ÙXŒŽLŽXˆHÛÛ\[š[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÝ\›Z[˜[Ü™]šY]×ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜œ™XÛÜ™È[È\È™]šY]Ë[Û›B˜XØÙ\YÛÝ]ÛÙ—ÜØÛÜWÜ[™[™×Ù˜XÝÜžWÙØ]XXÚ\Ú[ÛœËˆ]šY[˜ÙKX˜\ÙY˜ÛÛ™šY[˜ÙHØ[ˆ\›Z[˜[™]šY]ÈXØÙ\[˜ÙH\È™\ÛÛ™Y›Üˆ\ÈÝ\™˜XÙKˆBœØ[YH[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÙ˜XÝÜžWÚ[\ÜÙØ]WÌLKšœÛÛ˜‚[È›ÝÜÈ\ÜÈHØ[™Y]H˜XÝÜžHØ]NÈHÚ[™ÛKZ[\ÜØ\Ù[XÝÂ˜ÎMX™XØ]\ÙH]ÈX^[][HÝ\œ™[Yš[™Ù\œš[ØÛÜ™H\ÈÝÙ\Ý
ŒLML
K‚•HXØÙ\Y™]šY]È][H[\ÜÈ[š\›Ý”ÎMX\È[ˆ^\›˜[˜Ý]ÛÙ—ÜØÛÜX\™[™YØ]]™HX™[Ú]š[™Ù\œš[ÚY[[[™˜ÛÛÙÞWÝ™\œÚ[Û—Ø]ÙXÚ\Ú[Û[X™[Ù˜XÝÜžWÝŒWÎœœš[™Ú[™ÈHØ[›ÛšXØ[œ™YÚ\ÝžHÈŽÛÝ[X›HX™[ËˆŒŽÌ[™LÓLØ™[XZ[ˆ[š[\ÜY[™\‚˜Ú[™ÛWÚ[\ÜØØ\Û›ÝÜÙ[XÝYÝ\×Ü[˜ˆHÜÝZ[\Ü]]\È™YÜ™\ÜÚ[Û‚››ÝÈ[œÈŽÝ[X™[ËŽÝ][Ù‹\ØÛÜHX™[ËŒLˆÙYYYš[™Ù\œš[›X™[Ë›ÈÝ™\›\™]ÙY[ˆ[‹\ØÛÜH[™Ý][Ù‹\ØÛÜH[žHYË[˜Ú[™ÙYŒK\ÛXÙH[‹\ØÛÜH™][[Ûˆ
ŽNN
K[[Ý]Ù\]Y[˜ÙHY[]B˜LŒŽËÍÈ™]Z[™Y[[Ý]ÜÚ]]™\ÈÛÜœ™XÝ[™[[Ý]›Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËˆHŒ‹LKLMÕNŒÌŽVˆ[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÛ™^ØØ[™Y]WÙ›ÛÝÝ\ØÞXÛWÙXÚ\Ú[Û—ÌLKšœÛÛ˜‚‘]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆHÜÝZ[\Ü]]\È™[XZ[œÈÜ™Y[‹ŒŽÌ˜[™LÓLØ\™H›Ý[YÚX›HÛ›H›ÜˆH]\ˆ^XÚ]Ú[™ÛKZ[\ÜÞXÛK˜[™LÓLØ\ÈH™XÛÛ[Y[™Y™^™]šY]È\™Ù]™XØ]\ÙH]ÈX^[][B˜Ý\œ™[Yš[™Ù\œš[ØÛÜ™H\ÈÝÙ\ˆ
ŒŽLŽX™\œÝ\ÈŒÍŽ˜
Kˆ›ÈÙXÛÛ™™^\›˜[X™[Ø\È[\ÜY[ˆ\È[‹ˆ™^ÛÜšÈÚÝ[Z]\ˆÜ[ˆ]™^XÚ]LÓLÈÚ[™ÛKZ[\ÜÞXÛH[™\ˆHØ[YHØ]\È[™Ø\ÜˆÝÚ]ÚÂ˜Hœ›ØY\ˆ^\›˜[ÝXÝ\˜[Ý\™˜XÙNÈÈ›Ý™]žHHH\XØ]K\ÚYÛ˜[œ›ÝÜÈÚ]Ý]™]È]šY[˜ÙK‚‚•HŒ‹LKLMÕLŒÍŒÖˆ[ˆÜ[™Y]^XÚ]]\ˆÚ[™ÛKZ[\ÜÞXÛK‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜLÛL×ÜÚ[™ÛWÚ[\ÜØÞXÛWÙØ]WÌLKšœÛÛ˜˜[ÝÜÈHš[Üˆ[š\›Ý”ÎMX[\ÜÛ›H\È[™XYÙH[™Ù[XÝÈ^XÝB˜LÓLØˆH›ÝÈ\ÜÙ\È\›Z[˜[™]šY]Ë›Ý[™Y\XØ]H]šY[˜ÙK[šT™Y‚˜Ý\œ™[\™Y™\™[˜ÙHØÜ™Y[š[™ËÛÛ\]HÎÝ][Ù‹\ØÛÜH[™\œÙKYØ]HØÛÜš[™Â˜™[ÝÈLMXH˜\Ù[[™HX™[Y˜XÝÜžHØ]K[™H^\›˜[˜[œÙ™\‚™Ø]KˆHXØÙ\Y™]šY]È][H[\ÜÈ[š\›Ý”LÓLØ\È[ˆ^\›˜[˜Ý]ÛÙ—ÜØÛÜX\™[™YØ]]™HX™[Ú]š[™Ù\œš[ÚY[[[™˜ÛÛÙÞWÝ™\œÚ[Û—Ø]ÙXÚ\Ú[Û[X™[Ù˜XÝÜžWÝŒWÎœœš[™Ú[™ÈHØ[›ÛšXØ[œ™YÚ\ÝžHÈŽHÛÝ[X›HX™[ÎˆŒLˆÙYYš[™Ù\œš[È[™ŽHÝ][Ù‹\ØÛÜB›X™[Ëˆ\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜLÛL×ÜÜÝÚ[\ÜÙ›ÛÝÝ\ØÞXÛWÙXÚ\Ú[Û—ÌLKšœÛÛ˜œ™XÛÜ™ÈHÜÝTLÓLÈ]]\È\ÈÜ™Y[ˆ[™X]™\ÈŒŽÌ\ÈHÛ›Bœ™[XZ[š[™È˜XÝÜžK\\ÜÈ›ÝÈ[YÚX›H›ÜˆH]\™H^XÚ]ÞXÛKˆ]šY[˜ÙKX˜\ÙY˜ÛÛ™šY[˜ÙHØ[ˆHÙXÛÛ™^\›˜[[\Ü\ÈY™[œÚX›H[™\ˆHÝ\œ™[ŽYš[™Ù\œš[ÛÛÙÞK]\\ˆÛÝ[Ü›ÝÝÚÝ[›Ý™H]]ÛX]XÎÂ˜ŒŽÌ\ÈH]XÚ˜\œ›ÝÙ\ˆX\™Ú[ˆÈHLMX›ÛÜˆ
ŒÍŽ˜
H[™ÚÝ[™Z]\ˆ™XÙZ]™H]ÈÝÛˆ^XÚ]ÞXÛHÜˆ™HY™\œ™Y[ˆ˜]›ÜˆÙˆœ›ØY\‚™^\›˜[ÝXÝ\˜[ÛÝ\˜Ú[™Ë‚‚•HŒ‹LKLMÕLNŒÍNŒÎVˆ[ˆXYH]^XÚ]ÛËÛ›ËYÛÈXÚ\Ú[ÛˆÚ]Ý]˜Ú[™Ú[™È™YÚ\ÝžHÛÝ[ËˆH[\Ü˜\žH]\‹XÞXÛHØ]H›Ø™HÙ[XÝYŒŽÌ˜ÛÛ™š\›Z[™È]H›Ü›X[\›Z[˜[\™]šY]Ë\XØ]K[šT™YˆÝ\œ™[\™Y™\™[˜ÙKš[™\œÙKYØ]KX™[Y˜XÝÜžK[™^\›˜[]˜[œÙ™\ˆÚXÚÜÈÛÝ[\ÜÈ›Üˆ[‚™^XÚ][\ÜÞXÛKˆ\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WÜŒŽÌØÞXÛWÙY™\œ˜[ÌLKšœÛÛ˜›™]™\[\ÜÈY™\œÈH›ÝÈ™Y›Ü™H[\Ü™XØ]\ÙH]ÈX^[][HÝ\œ™[Yš[™Ù\œš[œØÛÜ™H\ÈŒÍŽ˜Û›HŒŽX™[ÝÈHXÝ]™HLMXÝ][Ù‹\ØÛÜH›ÛÜ‹˜Y\ˆÛÈ^\›˜[\™[™YØ]]™H[\ÜÈ\™H[™XYHÛÝ[X›Kˆ]šY[˜ÙKX˜\ÙY˜ÛÛ™šY[˜ÙHØ[ˆ™\Ù\š[™ÈHŽK[X™[™YÚ\ÝžH[™ÝÚ]Ú[™ÈÈœ›ØY\‚™^\›˜[ÝXÝ\˜[ÛÝ\˜Ú[™È\ÈHØY™\ˆ™^Ý\[ˆZÚ[™È]]ÛX]XÈ\™˜ÛÝ[Ü›ÝÝœ›ÛHH\Ý™[XZ[š[™È˜XÝÜžK\\ÜÈ›ÝËˆØÜËÛX™[Ù˜XÝÜžK›YØ\ÈÚXÚÙY[™Ý[™YYÈ›ÈÛÛ[Ú[™ÙH›Üˆ\ÈXÚ\Ú[Û‹[Û›HÛXÙK‚\ÈH™[XZ[š[™Ë][YH›Ø™KH[ˆ[ÛÈ™\˜[ˆH^\Ý[™È™^XØ[™Y]BœÛÝ\˜Ú[™ÈÛÛ[X[™Ú]HÛÈš[ÜˆÛÝ\˜ÙYÝ\™˜XÙ\ÈY\™ÙY\È[ˆ^Û\Ú[ÛˆÙ]š[ˆÜš]˜]KÝ\ˆ]›Ý[™ZYÚ™]šY]Ë[Û›HÛÝ\˜ÙKY]šY[˜ÙH›ÝÜÂŠMMLMMŽŒÎLŒXÎXŽÌÌÌÎÌL[™˜ÍŽMNX
K][ZYÚØ[YHœ›ÛH^\›˜[ÜÛÝ\˜ÙN›ÞYÜ™YXÝ\ÙWÛÛ™×ÝZ[‚•]˜]È›Ø™H\Y˜XÝØ\È›ÝÛÛ[Z]Y™XØ]\ÙH]È[™XYÙHÚ[YÈB[\Ü˜\žHY\™ÙY\š[Üˆš[Kˆ™^\™XÝÛÜšÈÚÝ[YH\˜X›B›][K\š[Ü‹Û[™KX˜[[˜ÙYœ›ØY\ˆÝXÝ\˜[ÛÝ\˜Ú[™È]Üˆ^XÚ]B™XÚYH][ˆÞYÜ™YXÝ\ÙK[Û›HÝ\™˜XÙH\ÈXØÙ\X›H™Y›Ü™H[›š[™ÂœÙ\]Y[˜ÙH[™ÝXÝ\˜[\XØ]HØÜ™Y[œË‚‚•HŒ‹LKLMÕLŽŒÍÎŒˆ[ˆYY]\˜X›H]Ú]Ý]Ü[š[™È[žH[\Ü˜][\ˆ\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[ÜÛÝ\˜Ú[™×ÌLKšœÛÛ˜›Y\™Ù\ÈHÜšYÚ[˜[Ì\›ÝÈÛÛÙXÛÛ™]˜[˜ÚH\›Z[˜[™Z™XÝË›Ýš[Ü‚™œ™\ÚÛÝ\˜ÙYÝ\™˜XÙ\Ë›Ýš[Üˆ\›Z[˜[YXÚ\Ú[Ûˆ\Y˜XÝË[™H^XÚ]”ŒŽÌY™\œ˜[[ÈÛ™H™\›ÙXÚX›H^Û\Ú[ÛˆÝ\™˜XÙKˆ][ˆ\Y\ÈBÛË\\‹[[™HØ\[™Ù[XÝÈÚ^™]šY]Ë[Û›HÛÝ\˜ÙKY]šY[˜ÙH›ÝÜÈXÜ›ÜÜÈ™YB˜ÛÝ™\™Y[™\ÎˆMML[™MMŽœ›ÛHÞYÜ™YXÝ\ÙWÛÛ™×ÝZ[NMŽTÌ˜˜[™NM‘’Mœ›ÛHX\ÙK[™Í[™NP•ŒŒœ›ÛH\ÛÛY\˜\ÙKˆ]šY[˜ÙKX˜\ÙY˜ÛÛ™šY[˜ÙHØ[ˆH™]š[Ý\ÈÛ™K[[™H›Ø™H\È›ÈÛ™Ù\ˆHXÝ]™HÛÝ\˜Ú[™Â˜›ØÚÙ\‹‚‚•HØ[YH[ˆ[ˆY˜[˜ÙYHÚ^›ÝÜÈ›ÝYÚHš\œÝ›Ý[™Y\XØ]BœØÜ™Y[œËˆ\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[Ø˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜œ™XÛÜ™È‹Íˆ›Ë\ÚYÛ˜[›ÝÜÈYØZ[œÝHÝ\œ™[ÛÝ[X›H™Y™\™[˜ÙHTÕK‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[Ø[Ýœ×Ø[ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜™š[™È^XÝÛ™X\‹Y\XØ]HÙ\]Y[˜ÙHZ\œÈÚ][ˆHÚ^\›ÝÈœ›ØY\ˆÝ\™˜XÙK‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[ØÛ\Ý\—Ú[™^ÌLKšœÛÛ˜›X]\šX[^™\È[Ú^[Q›ÛÚYXØ\œËÛÝ™\œÈMKÌMH^\›˜[[]œËX[‘›ÛÙYZÈZ\œË[™š[™ÈYÚUH^\›˜[Z\œËˆHÝ\œ™[XÛÝ[X›BœØÜ™Y[‚˜\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[ØÝ\œ™[ØÛÝ[X›WÜÝXÝ\˜[ÜØÜ™Y[—ÌLKšœÛÛ˜˜ÛÛ\]\ÈÌ‹ÍÌˆ]Y\žK]\™Ù]Z\œÎˆš]™H›ÝÜÈ]™HYÚUB˜Ý\œ™[XÛÝ[X›HÝXÝ\˜[\XØ]HÚYÛ˜[Ë[™Û›HÍ\È›Â˜Ý\œ™[XÛÝ[X›HÝXÝ\˜[\XØ]HÚYÛ˜[ˆ\Y˜XÝËÝŒ×Ù^\›˜[Ú\™Û™YØ]]™WØœ›ØY\—ÜÝXÝ\˜[Ý\›Z[˜[ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜\™Y›Ü™H™Z™XÝÈMMLMMŽNMŽTÌ˜NM‘’M[™NP•ŒŒ\Âœ™]šY]Ë[Û›H\XØ]K\ÚYÛ˜[›ÝÜÈ[™Y™\œÈÍ™Z[™[šT™Y‹]ÚYB™\XØ]HØÜ™Y[š[™Ë\›Z[˜[™]šY]ÈXØÙ\[˜ÙK[™\œÙKYØ]KÙ˜XÝÜžH]šY[˜ÙK˜[™H[[\ÜØ]Kˆ›ÛÝË[ÛˆÍ\Y˜XÝÈ™XÛÜ™ÛX\ˆ›Ý[™Y™\XØ]H]šY[˜ÙKH\™Ù]Y[šT™YŽLÍL™X\™\Ý\™Y™\™[˜ÙH›Ë\Ú\™YXÛ\Ý\‚œ™\Ý[H[šT™YŽLÍLÝ\œ™[\™Y™\™[˜ÙHØÜ™Y[ˆÚ]Ý\œ™[\™Y™\™[˜ÙB›Ý™\›\Ë[™[ˆ[NÝ][Ù‹\ØÛÜH[™\œÙKYØ]H\ÜÈÚ]ÜB˜Y][Ù\[™[ÚY›Û\ÙXØÛÜ™HŒÌ˜ˆ]šY[˜ÙKX˜\ÙYÛÛ™šY[˜ÙHØ[ˆB˜œ›ØY\ˆÝ\™˜XÙHYÛ™HÝ\š]š[™È›ËXÝ\œ™[\ÝXÝ\˜[\ÚYÛ˜[›ÝË[™]Â™\XØ]KÚ[™\œÙKYØ]H›ØÚÙ\œÈÙ\™H˜\œ›ÝÙY™Y›Ü™HH]\ˆ\›Z[˜[œ™]šY]ËÙ˜XÝÜžH[\ÜÛÛ\]Y›ÜˆÍÈÈ›Ý™]žHHš]™B™\XØ]K\ÚYÛ˜[›ÝÜÈÚ]Ý]™]È]šY[˜ÙK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕLŽŒÍÎŒ˜[™Ü˜\Y]Œ‹LKLMÕLÎŒNŒÖ˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ][š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ][š]\ÝË˜[Y]XÝ™\ˆŽHÝ\˜]YX™[ËÛÛ\[X[˜[™Ú]Y™ˆKXÚXÚØˆ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›Y˜ØÜËÛX™[Ù˜XÝÜžK›YÛÜšÈØÛÜK[™Ù™‹Ý]\Ë›ÙÜ™\ÜÈÙË[™™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™HÚXÚÙYÜˆ\]Yˆ›È™YÚ\ÝžH[\ÜØ\ÈXYK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕLŒÍŒÖ˜[™Ü˜\Y]Œ‹LKLMÕLNNV˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]ÎMH[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]ÎNH[š]\ÝË˜[Y]XÝ™\ˆŽHÝ\˜]YX™[ËÛÛ\[X[˜Ú]Y™ˆKXÚXÚØ”ÓÓˆ\œÙHÚXÚÜÈ›ÜˆH™]ÈLÓLÈ\Y˜XÝÈ[™œ™YÚ\ÝžHÝ[[X\žK[™H^\›˜[˜[œÙ™\ˆØ]H]ŽÍŽˆ‘PQQK˜ØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÛX™[Ù˜XÝÜžK›YÛÜšÈØÛÜKš[™Ù™‹Ý]\Ë›ÙÜ™\ÜÈÙË[™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™HÚXÚÙYÜ‚\]Y‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕNŒÌŽV˜[™Ü˜\Y]Œ‹LKLMÕNNŒÎ˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]ÎLÈ[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]ÎMH[š]\ÝË˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓ‚œ\œÙHÚXÚÈ›ÜˆH›ÛÝË]\\Y˜XÝ[™H^\›˜[˜[œÙ™\ˆØ]H]ŽÍŽˆ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÛX™[Ù˜XÝÜžK›YÛÜšÈØÛÜK[™Ù™‹Ý]\Ë›ÙÜ™\ÜÈÙË[™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™B˜ÚXÚÙYÜˆ\]YÈ›È™YÚ\ÝžH[\ÜØ\ÈXYK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕŒÌNŒÖ˜[™Ü˜\Y]Œ‹LKLMÕNŒŒÌ˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]Î[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]ÎLÈ[š]\ÝË˜[Y]XÝ™\ˆŽÝ\˜]YX™[ËÛÛ\[X[˜Ú]Y™ˆKXÚXÚØ”ÓÓˆ\œÙHÚXÚÜÈ›ÜˆH™]È[™\œÙKYØ]KÝ\›Z[˜[Ù˜XÝÜžB˜\Y˜XÝÈ[™[\ÜY™YÚ\ÝžK[™H[™XYK\™\[ˆ^\›˜[˜[œÙ™\ˆØ]H]ŽÍŽˆ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÛX™[Ù˜XÝÜžK›YÛÜšÈØÛÜK[™Ù™‹Ý]\Ë›ÙÜ™\ÜÈÙË[™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™B\]YÈ™Y›XÝHš\œÝ^\›˜[\™[™YØ]]™H[\Ü‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆH™]š[Ý\È[™Ù™ŽˆÝ\YŒ‹LKLMÕÎŒŽNŒÍ–˜[™Ü˜\Y]Œ‹LKLMÕÎŽŒ–˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]Îˆ[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]Î[š]\ÝË˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓ‚œ\œÙHÚXÚÜÈ›ÜˆH™]È[šT™YˆÝ\œ™[\™Y™\™[˜ÙHØÜ™Y[‹H›ØÝ\ÙYØØ[[™Â˜\Y˜XÝ™YÜ™\ÜÚ[Û‹[™H^\›˜[˜[œÙ™\ˆØ]HÝ[]ŽÍŽˆ‘PQQK˜ØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšÈØÛÜK[™Ù™‹Ý]\È[œ]Ë[™™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™H\]YÈØÜËÛX™[Ù˜XÝÜžK›YØ\ÈÚXÚÙY[™™Y›Ý™YYÛÛ[Ú[™Ù\È›Üˆ\È\XØ]K\ØÜ™Y[ˆÛXÙK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕŽŒŽNŒ˜[™Ü˜\Y]Œ‹LKLMÕŽÎŒ˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]ÎÈ[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]Îˆ[š]\ÝË˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓ‚œ\œÙHÚXÚÜÈ›ÜˆH™]È[]œËX[Ù\]Y[˜ÙK\XØ]KY]šY[˜ÙK\›Z[˜[\™]šY]Ë\]Y]YK[™\™Ù]YU[šT™Yˆ\Y˜XÝË\È›ØÝ\ÙY\Y˜XÝœ™YÜ™\ÜÚ[ÛœËˆ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšÈØÛÜK[™Ù™‹œÝ]\È[œ]Ë[™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™H\]YÈØÜËÛX™[Ù˜XÝÜžK›YØ\ÈÚXÚÙY[™Y›Ý™YYÛÛ[Ú[™Ù\È›Üˆ\È\XØ]K\ØÜ™Y[‹Ü™]šY]ÂœÛXÙK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕNŒŽŒ˜[™Ü˜\Y]Œ‹LKLMÕŽŒNŒÌ˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]Îˆ[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]ÎÈ[š]\ÝË˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓ‚œ\œÙHÚXÚÜÈ›ÜˆH™]ÈÛÝ\˜Ú[™ËÜÙ\]Y[˜ÙKÜÝXÝ\˜[Ý\›Z[˜[\Y˜XÝË[™H^\›˜[˜[œÙ™\ˆØ]HÝ[]ŽÍŽˆ‘PQQK˜ØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÛX™[Ù˜XÝÜžK›YÛÜšÈØÛÜKš[™Ù™‹Ý]\È[œ]Ë[™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™HÚXÚÙYÈX™[Y˜XÝÜžB™ØÜÈ™\]Z\™Y›ÈÛÛ[Ú[™ÙH›Üˆ\È™\XÙ[Y[\ÛÝ\˜Ú[™ÈÛXÙK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕÎŒNŒV˜‚”Ý\\ÚXÚÜÈ\ÜÙYÚ]ÍÎ[š]\ÝÈ[™UÓ”U\Ü˜È]Ûˆ[B˜Ø][]X×ÙX\˜ÛH˜[Y]Xˆš[˜[ÚXÚÜÈ\ÜÙYÚ]Î[š]\ÝË˜˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓˆ\œÙHÚXÚÜÈ›ÜˆH™]ÂœÛÝ\˜Ú[™ËÜÙ\]Y[˜ÙKÜÝXÝ\˜[\Y˜XÝËÛÛÜ™[˜]HYÙ\Ý™XÚXÚÜÈY\ˆÒQ‚Ú]\ÜXÙH›Ü›X[^˜][Û‹›ØÝ\ÙY\Y˜XÝ™YÜ™\ÜÚ[ÛœË[™H^\›˜[˜[œÙ™\ˆØ]HÝ[]ŽÍŽˆ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšÂœØÛÜKÚ[™Ù™‹ÜÝ]\È[œ]Ë[™^\›˜[˜[œÙ™\ˆ›Ý\ÈÙ\™H\]YÂ˜ØÜËÛX™[Ù˜XÝÜžK›YØ\ÈÚXÚÙY[™Y›Ý™YYÛÛ[Ú[™Ù\È›Üˆ\ÂœÛÝ\˜Ú[™ËÙ\XØ]K\ØÜ™Y[ˆÛXÙK‚‚”[ˆ™\šYšXØ][Ûˆ›ÜˆHÝ\œ™[[™Ù™ŽˆÝ\YŒ‹LKLMÕŽŒŒÎNV˜[™Ü˜\Y]Œ‹LKLMÕŽLŒM–˜ˆÝ\\ÚXÚÜÈ\ÜÙYÚ]ÍÍˆ[š]\ÝÂ˜[™UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÈš[˜[ÚXÚÜÂœ\ÜÙYÚ]ÍÎ[š]\ÝË˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓ‚œ\œÙHÚXÚÜÈ›ÜˆH™]È\™[™YØ]]™H\Y˜XÝË[™H^\›˜[˜[œÙ™\‚™Ø]H™[XZ[š[™È]ŽÍŽˆ‘PQQKX™[Y˜XÝÜžHØÜË^\›˜[]˜[œÙ™\ˆØÜËœØÛÜK[™Ù™‹[™™\Z\‹Ý˜[œÙ™\ˆ›Ý\ÈÙ\™HÚXÚÙYÈX™[Y˜XÝÜžHØÜÂœ™\]Z\™Y›ÈÛÛ[Ú[™ÙH›Üˆ\ÈÝXÝ\˜[\XØ]K\ØÜ™Y[ˆÛXÙK‚‚\ÈÙˆHŒ‹LKLM•NMNŒ‹LNŒ[‹È›Ý™\Ý[YHKPÔÐHÝšXÝ‘›ÛÙYZËÕK\ØÛÜ™H™\Z\‹ˆHÛÜ\ÈÛÜÙYÙY™\œ™YžB˜\Y˜XÝËÝŒ×ÛXÜØWÝWÚÛÝ]Ù™X\ÚXš[]WØYYXØ][Û—ÌLšœÛÛ˜Ú]˜[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙXX^[[X]\šX[^˜X›B˜Z[‹Ý\ÝK\ØÛÜ™HŽMÍXÌMH\™Ù]]š[Û][™È˜Z[‹Ý\Ý›ÝÜËŒLYÚUH\][ÛˆÛÛœÝ˜Z[Ë[™ÎÙ\]Y[˜ÙKZY[]H\][Û‚˜ÛÛœÝ˜Z[Ëˆ›Û˜Ø[›ÛšXØ[ÝYÙY^[™Y]Y\žKXÚ[šË]Y\žK\Ú[™ÛK\™Ù]\Ú\™Ü]\™\Z\‹Ü]\™Y\ÚYÛ‹[™Û\Ý\‹Yš\œÝ›Ý[™\Y˜XÝÂÙ\™H™[[Ý™YY\ˆZ\ˆÝ[[X\žHØ\ÈØ\\™YÈ^H\™H›ÝÛÛ[X][Û‚\™Ù]Ë‚‚•H^\›˜[[Ý\›Z[˜[YXÚ\Ú[Ûˆ\ÜÈ›ÝÈ^\ÝÈ[‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÝ\›Z[˜[ÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜ˆ]ÛÝ™\œÂHLÙ[XÝYØ[™Y]\ÈÚ]^XÝHÛ™H\›Z[˜[Ý]\ÈXXÚˆ˜™Z™XÝYÙ\XØ]WÛÜ—Û™X\—Ù\XØ]XÂ˜™Z™XÝYØXÝ]™WÜÚ]WÙ]šY[˜ÙWÛZ\ÜÚ[™Ø[™Â˜Y™\œ™YÜ™\]Z\™\×Ú[X[—Ù^\Ú][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›B™^\›˜[X™[ËˆHÈY™\œ™Y›ÝÜÈ\™H›ÝÈ›Ý]YžB˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÚ[X[—Ù^\Ü™]šY]×Ü]Y]YWÌLKšœÛÛ˜‚˜ÌMÍM˜ÍMX[™M“”ÒŒXXÚ]™HH™]šY]Ë[Û›H^\]Y\Ý[Û‹˜]]ÛX][Ûˆ[Z]][Û‹[™™[XZ[š[™È›Û‹Z[X[ˆ›ØÚÙ\œËˆH\›Z[˜[YXÚ\Ú[Û‚˜ÛÛ™šY[˜ÙH]Y]›ÝÈ^\ÝÈ[‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙXÚ\Ú[Û—ØÛÛ™šY[˜ÙWØ]Y]ÌLKšœÛÛ˜ˆ]˜ÚXÚÜÈ[LÙ[XÝY›ÝÜÈYØZ[œÝXÝ]™K\Ú]K\XØ]KÛ™X\‹Y\XØ]Kœ™\™\Ù[][Û‹]\š\ÝXË™]šY]ËÝXÝ\™K˜[œÙ™\‹YØ]K[™˜XÝÜžKYØ]B™]šY[˜ÙKÙY\ÈÝ\œ™[XÚ\Ú[ÛœÈÛÛ™šY[X\šÜÈÈÝ\œ™[\™œ™\™\Ù[][Û‹[Û›H\XØ]H™Z™XÝ[ÛœÈÝËXÛÛ™šY[˜ÙK[™ÙY\ÈÈ›ÝÜÈ[‚›™YYË\™]šY]ÈÝ]\ËˆH›Ü›X[^™YÛÛ\[š[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙXÚ\Ú[Ûœ×Ü™]šY]×Û›Ü›X[^™YÌLKšœÛÛ˜œ™XÛÜ™Èˆ™YY×Ü™]šY]ØÈ™Z™XÝYØXÝ]™WÜÚ]WÙ]šY[˜ÙWÛZ\ÜÚ[™Ø[™B˜™Z™XÝYÙ\XØ]WÛÜ—Û™X\—Ù\XØ]XXÚ\Ú[ÛŽÈH›Ü›X[^™Y]Y]YB˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÚ[X[—Ù^\Ü™]šY]×Ü]Y]YWÛ›Ü›X[^™YÌLKšœÛÛ˜œ›Ý]\È[ˆ™YYË\™]šY]È›ÝÜÈ
ÌMÍM˜Í˜ÎR”–ŽÍMX˜NP–X[™M“”ÒŒ
HÚ]^XÝ[œ™\ÛÛ™Y]Y\Ý[ÛœËˆ[™YH]Y][™››Ü›X[^˜][Ûˆ\Y˜XÝÈ\™H™]šY]Ë[Û›KÚ][\Ü\™XYH›ÝÜÈ[™˜ÛÝ[X›H^\›˜[X™[ËˆHŒ‹LKLM•MNŒŒˆ[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÛ™YY×Ü™]šY]×Ü™\ÛÛ][Û—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙXÚ\Ú[Ûœ×Ü™]šY]×Ü™\ÛÛ™YÌLKšœÛÛ˜[™˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÚ[X[—Ù^\Ü™]šY]×Ü]Y]YWÜ™\ÛÛ™YÌLKšœÛÛ˜‚•]\ÚÈ™]šY]ÈÚXÚÙYØØ[XÝ]™K\Ú]K™XXÝ[Û‹Ù\]Y[˜ÙK™\™\Ù[][Û‹š]\š\ÝXË[™ÝXÝ\˜[\Y˜XÝÈ\È[šT›ÝÐ‹Õ[šT™YŽLÕ[šT™YLÛÝ\˜ÙB˜ÛÛ^ˆ\™Ù]Y[šT™YŽLÍLX\[™È›Ý[™Ú\™YØ[™Y]KØÝ\œ™[\™Y™\™[˜ÙB˜Û\Ý\œÈ›ÜˆH™X\™\Ý\™Y™\™[˜ÙHÚXÚÜËÛÈ\XØ]H™Z™XÝ[Ûˆ\È›ÝœÝ\ÜY][ˆ›ÝÜÈ\™H\›Z[˜[™]šY]Ë[Û›B˜™Z™XÝYÜ™\™\Ù[][Û—ØÛÛ™›XÝ[\Ü\ØY™]HXÚ\Ú[ÛœÈ™XØ]\ÙHÝ\œ™[œ™\™\Ù[][ÛˆÜˆ]\š\ÝXÈÛÛ›ÛÈÛÛ™›XÝÚ]ÛÝ\˜ÙK\Ý\ÜYÚ[Z\ÝžK‚•H™\ÛÛ™YXÚ\Ú[ÛˆÝ\™˜XÙH\È™YY×Ü™]šY]Ø[\Ü\™XYH›ÝÜË[™˜ÛÝ[X›H^\›˜[X™[Ë‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÛYXÚ[š\ÛWÜ™\Z\—Û[™\×ÌLKšœÛÛ˜›ÝÂ\›œÈÜÙHÚ^™]šY]Ë[Û›H™\™\Ù[][ÛˆÛÛ™›XÝÈ[È˜[YYœ™\™\Ù[][Û‹Ú]\š\ÝXÈ™\Z\ˆ[™\ÎˆÑ‹ÓQ

H™YÞRÔ‹ÓQ™YÞB”ÛÍIËY”X\ÙKÝYØ\‹\ÜÜ]H\ÛÛY\˜\ÙKØÚY™‹X˜\ÙHX\ÙKØ[Û\ÙK[™™ÛXÛÜÚYKZY›Û\ÙH™\œÝ\ÈY][ZY›Û\ÙH›Ý[™\žHÛÛ›Ûˆ\ÙH[™\Âœ™[[Ý™HHÙ[™\šXÈ™\›Ë\\ÜÈ™\Z\ˆ[XšYÝZ]H]\™H›Ý™YXÝ]™H™X]\™\Ëš[\Ü\™XYHXÚ\Ú[ÛœËÜˆÛÝ[X›HX™[Ë‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÙ—Ü™YÞÜ™\Z\—ØÛÛ›ÛÌLKšœÛÛ˜›ÝÂš[\[Y[ÈHš\œÝ›Ý[™Y™\Z\‹[[™HÛÛ›Û›ÜˆÌMÍM˜ˆ]ÝYÙ\ÈÛ›BœÙ\]Y[˜ÙKY\š]™YÑ‹ÓQ

H]šY[˜ÙNˆHÞÞØÛXÚ[™K\šXÚ›ÞH\ÈBœÛÝ\˜ÙKXXÝ]™K\Ú]K[Ý™\›\[™È^Ø›ÞK[ˆÛÛ˜\ÝÈ]ÛÛ\]HÑ‚˜^\ÈYØZ[œÝHÛÛ™›XÝ[™ÈÝ\œ™[\™Y™\™[˜ÙH™ZYÚ›ÜœËˆÜÙH™ZYÚ›ÜœÈXÚÂHÛÛ\]HÑˆ^\ËˆH›ÛÝË[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÙ—Ü™YÞÚ[\ÜÜØY™]WØYYXØ][Û—ÌLKšœÛÛ˜››ÝÈÛÛœÝ[Y\È]›Û‹]^ÛÛ›Û[ˆH[\Ü\ØY™]H]ˆ]™\Z\œÈB“ÌMÍMˆ™\™\Ù[][Û‹XÛÛ™›XÝ›ØÚÙ\ˆ[™™XÛÜ™ÈHÜÝ\™\Z\ˆ›Ü›X[^™YœÝ]\È\È™YY×Ü™]šY]Ø]]Ý[Ü™X]\È[\Ü\™XYH›ÝÜÈ[™˜ÛÝ[X›H^\›˜[X™[È™XØ]\ÙHœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËHÜÝ\™\Z\‚œ™]šY]ÈXÚ\Ú[Û‹[™H[˜XÝÜžHØ]H™[XZ[ˆ[œ™\ÛÛ™Y‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙÛXÛÜÚYWÚY›Û\ÙWØ›Ý[™\žWØÛÛ›ÛÌLKšœÛÛ˜››ÝÈÜ[œÈH™^™\Z\ˆ[™H›ÜˆM“”ÒŒ\È™]šY]Ë[Û›HÛÛ›Û]šY[˜ÙK‚’]ÝYÙ\ÈÛÝ\˜ÙK]˜XÙYXÚYXÈXÝ]™K\Ú]H™\ÚYY\ËXÝ]™K\Ú]HÜXÚ[™ËØØ[œØÚÙ]ÛÛ\ÜÚ][Û‹XœÙ[ØØ[Y][ØÛÙ˜XÝÜˆYØ[™ÛÛ^[™™\›Â›Y][ZY›Û\ÙH›ÛKZ[Ý\Ü\ÈH›Û‹]^›Ý[™\žHÛÛ›ÛˆH›ÛÝË[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙÛXÛÜÚYWÚY›Û\ÙWÚ[\ÜÜØY™]WØYYXØ][Û—ÌLKšœÛÛ˜››ÝÈÛÛœÝ[Y\È]ÛÛ›Û[ˆH[\Ü\ØY™]H]ˆ]™\Z\œÈHM“”ÒŒœ™\™\Ù[][Û‹Ú]\š\ÝXÈ›Ý[™\žH›ØÚÙ\ˆ[™™XÛÜ™ÈHÜÝ\™\Z\‚››Ü›X[^™YÝ]\È\È™YY×Ü™]šY]Ø]]Ý[Ü™X]\È[\Ü\™XYH›ÝÜÂ˜[™ÛÝ[X›H^\›˜[X™[È™XØ]\ÙHœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËBœÜÝ\™\Z\ˆ™]šY]ÈXÚ\Ú[Û‹[™H[˜XÝÜžHØ]H™[XZ[ˆ[œ™\ÛÛ™Y‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÝYØ\—ÜÜÜ]WÚ\ÛÛY\˜\ÙWØÛÛ›ÛÌLKšœÛÛ˜››ÝÈÜ[œÈH™^ÍMH™\Z\ˆ[™H\È™]šY]Ë[Û›HØÛÜKXÛÛ›Û]šY[˜ÙK‚’]\Ù\ÈHÛÝ\˜ÙK]˜XÙYXÝ]™K\Ú]H\™ËØØ[ØÚÙ]ÛÛ\ÜÚ][Û‹XœÙ[™›]š[‹ØÛÙ˜XÝÜˆÛÛ^™\›È›]š[ˆ›ÛKZ[Ý\Ü[™ÙXZÈÜHØÛÜ™BÚ]ØØ[XœÙ[Ù›]š[—ØÛÛ^ÛÝ[\™]šY[˜ÙHÈÙ\\˜]B›X[››ÜÙKM‹\ÜÜ]H\ÛÛY\˜\ÙHØÛÜHœ›ÛHHÙXZÈ›]š[‹\™YÞ]\š\ÝXÈÜK‚•H›ÛÝË[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÝYØ\—ÜÜÜ]WÚ\ÛÛY\˜\ÙWÚ[\ÜÜØY™]WØYYXØ][Û—ÌLKšœÛÛ˜››ÝÈÛÛœÝ[Y\È]ÛÛ›Û[ˆH[\Ü\ØY™]H]ˆ]™\Z\œÈHÍMHÙXZÂ™›]š[‹ÜØÛÜH™\™\Ù[][Ûˆ›ØÚÙ\ˆ[™™XÛÜ™ÈHÜÝ\™\Z\ˆ›Ü›X[^™YœÝ]\È\È™YY×Ü™]šY]Ø]]Ý[Ü™X]\È[\Ü\™XYH›ÝÜÈ[™˜ÛÝ[X›H^\›˜[X™[È™XØ]\ÙHœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËHÜÝ\™\Z\‚œ™]šY]ÈXÚ\Ú[Û‹[™H[˜XÝÜžHØ]H™[XZ[ˆ[œ™\ÛÛ™Y‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜØÚY™—Ø˜\ÙWÛX\ÙWØÛÛ›ÛÌLKšœÛÛ˜›ÝÂ›Ü[œÈH™^NP–H™\Z\ˆ[™H\È™]šY]Ë[Û›HØÛÜKXÛÛ›Û]šY[˜ÙKˆ]\Ù\ÈÛÝ\˜ÙK]˜XÙY\‹Ó\ÈXÝ]™K\Ú]H™\ÚYY\ËHØÚY™‹X˜\ÙH\ËØØ[œØÚÙ]ÛÛ\ÜÚ][Û‹XœÙ[[YKØÛÙ˜XÝÜˆÛÛ^™\›È[YKÙ[XÝ›Û‹]˜[œÙ™\‚œ›ÛKZ[Ý\Ü[™ÙXZÈÜHØÛÜ™HÚ]ØØ[XœÙ[Ú[YWØÛÛ^˜ÛÝ[\™]šY[˜ÙHÈÙ\\˜]H‹XXÙ][™]\˜[Z[˜]HX\ÙHØÛÜHœ›ÛHHÙXZÂš[YK\\›ÞY\ÙH]\š\ÝXÈÜKˆH›ÛÝË[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜØÚY™—Ø˜\ÙWÛX\ÙWÚ[\ÜÜØY™]WØYYXØ][Û—ÌLKšœÛÛ˜››ÝÈÛÛœÝ[Y\È]ÛÛ›Û[ˆH[\Ü\ØY™]H]ˆ]™\Z\œÈHNP–HÙXZÂš[YKÜØÛÜH›ØÚÙ\ˆ[™™XÛÜ™ÈHÜÝ\™\Z\ˆ›Ü›X[^™YÝ]\È\Â˜™YY×Ü™]šY]Ø]]Ý[Ü™X]\È[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›B™^\›˜[X™[È™XØ]\ÙHH™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]œ›ØY\‚™\XØ]HØÜ™Y[š[™ËHÜÝ\™\Z\ˆ™]šY]ÈXÚ\Ú[Û‹[™H[˜XÝÜžHØ]Bœ™[XZ[ˆ[œ™\ÛÛ™Y‚•H^\›˜[ÝXÝ\˜[[Ý]\È›ÝÈ[Ý™Yœ›ÛH]Yš[š][ÛˆÈHÛÛ˜Ü™]Bœ™]šY]Ë[Û›HÝXÝ\™HØXÚH[‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÝXÝ\˜[ØÛ\Ý\—Ú[™^ÌLKšœÛÛ˜ˆ[LÙ[XÝY[Q›ÛÛÛÜ™[˜]HÚYXØ\œÈ\™HX]\šX[^™Y›ÛÙYZÈÛÛ\]YH™X\™\Ý›™ZYÚ›ÜˆØXÚHÛÝ™\œÈLÌLØ[™Y]\Ë[™™K\Ü]Û\Ý\š[™È]HLØ™š[™ÈÛ™HYÚUHZ\ˆ
ÎMLLØLMN
HXÜ›ÜÜÈš[™HÛ\Ý\œËˆ\È\È›ÝB˜Z[‹Ý\ÝÜ][™ÙY\ÈÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆHœ›ØY\ˆ^\›˜[œÝXÝ\˜[Ý\™˜XÙH›ÝÈ^\ÝÈ[‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÝXÝ\˜[ÝWÚÛÝ]Ü]ÌLWØ[ÌšœÛÛ˜[™˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÝXÝ\˜[ØÛ\Ý\—Ú[™^ÌLWØ[ÌšœÛÛ˜ˆ[Ì˜Ý\œ™[^\›˜[Ø[™Y]\È]™H[Q›ÛÚYXØ\œË›ÛÙYZÈ™X\™\Ý[™ZYÚ›Ü‚˜ÛÝ™\˜YÙH\ÈÌÌÌH[]œËX[›ÛÙYZÈØXÚH›ÝÈÛÝ™\œÈÍKÍÍH[›Ü™\™Y››ÛœÙ[ˆZ\œË[™H™K\Ü]ØXÚHš[™ÈˆYÚUHZ\œÈXÜ›ÜÜÈ‚˜Û\Ý\œËˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÝXÝ\˜[ÝWÙ]™\œÙWÜÜ]Ü[—ÌLWØ[ÌšœÛÛ˜››ÝÈ™[[Ý™\ÈHÜ]X\ÜÚYÛ›Y[›ØÚÙ\ˆÚ]H™]šY]Ë[Û›HÛ\Ý\‹\™\Ù\š[™ÂœÜ]ˆˆ\Ý[™˜Z[ˆØ[™Y]\ËÛ™H\ÝØ[™Y]Hœ›ÛHXXÚ^\›˜[›[™KMÌMÜ›ÜÜË\Ü]Z\œÈÚXÚÙYX^Ü›ÜÜË\Ü]K\ØÛÜ™HŽMŒØ˜[™Ü›ÜÜË\Ü]Z\œÈ]HLØˆ\È\È›Ý[ˆ[\Ü\™XYH™[˜ÚX\šÂ˜ÛZ[NÈ]™\žH^\›˜[›ÝÈ™[XZ[œÈ›Û‹XÛÝ[X›KˆHŒ‹LKLM•LÎŒŽŒŽV‚˜]Y]]™\šYšXØ][Ûˆ[ˆ™\˜[ˆHÛÛ™šY[˜ÙK›Ü›X[^˜][Û‹[™›Ü›X[^™Yœ]Y]YHZ[\œÈY[\Ý[H[™›Ý[™›ÈY™[œÚX›HØØ[Y]šY[˜ÙK[Û›Bœ™\ÛÛ][Ûˆ›ÜˆHˆ›Ü›X[^™Y™YY×Ü™]šY]Ø›ÝÜËˆHŒ‹LKLM•NŒÎM‹LNŒœ[ˆ[ˆYY\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ[Ýœ×Ø[ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜˜[™\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ[Ýœ×Ø[ÜÙ\]Y[˜ÙWÜÙX\˜ÚØ]Y]ÌLKšœÛÛ˜‚“S\Ù\\ÌˆÙX\˜ÚY[Ì^\›˜[Ø[™Y]\ÈYØZ[œÝXXÚÝ\‹›Ý[™›™X\‹Y\XØ]HZ\œÈ]L	HY[]HÈ	HÛÝ™\˜YÙK™XÛÜ™YX^™\ÜY™^\›˜[Y^\›˜[Y[]HØ[™Ù\[\Ü\™XYKØÛÝ[X›H›ÝÜËˆB˜ÛÛ™šY[˜ÙH]Y]›ÝÈØ\œšY\È\È^\›˜[[]œËX[›Ë\ÚYÛ˜[]šY[˜ÙH›Ü‚HÙ[XÝY[Ý›ÝÜËˆH]\ˆ™YYË\™]šY]È™\ÛÛ][Û‹YXÚ[š\ÛH™\Z\‚›[™KÑˆÛÛ›ÛÑˆ[\Ü\ØY™]HYYXØ][Û‹M“”ÒŒ›Ý[™\žB˜YYXØ][Û‹ÍMHÝYØ\‹\ÜÜ]H\ÛÛY\˜\ÙHÛÛ›ÛÍMH[\Ü\ØY™]B˜YYXØ][Û‹NP–HØÚY™‹X˜\ÙHX\ÙHÛÛ›Û[™NP–H[\Ü\ØY™]B˜YYXØ][Ûˆ\Y˜XÝÈÝ\\œÙYHH‹\›ÝÈ›Ü›X[^™Y]Y]YH›Üˆ[ÝYXÚ\Ú[Û‚ÛÜšÎÈÈ›Ý™K[Ü[ˆÜÙH›ÝÜÈÚ]Ý]™]È]šY[˜ÙKˆHŒ‹LKLM•MÎNŒÌËLNŒœ[ˆ[ˆYY\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝØZÜ—Û˜YÜ™\Z\—ØÛÛ›ÛÌLKšœÛÛ˜˜[™˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝØZÜ—Û˜YÚ[\ÜÜØY™]WØYYXØ][Û—ÌLKšœÛÛ˜‚•HÎR”–ŽÛÛ›Û\Ù\ÈÛ›H›Û‹]^Ù\]Y[˜ÙKÛØØ[]šY[˜ÙNˆH‘ÓØ˜ÛÙ˜XÝÜ‹Xš[™[™È›ÞKÛÝ\˜ÙK]˜XÙYXÝ]™K\Ú]H\‹ØØ[ÒÈÛÛ^[™˜Ý\œ™[\™Y™\™[˜ÙHÛÛ˜\Ý›ÝÜÈXÚÚ[™ÈHÛÛ\]HRÔ‹ÓQ^\ËˆBš[\Ü\ØY™]HYYXØ][Ûˆ™\Z\œÈHÎR”–Ž™\™\Ù[][Ûˆ™X\‹Y\XØ]B˜ÛÛ™›XÝ[™™XÛÜ™ÈÜÝ\™\Z\ˆ™YY×Ü™]šY]Ø][\Ü™[XZ[œÈ›ØÚÙYžB˜]\š\ÝX×ØÛÛ›ÛÛ›ÝÜØÛÜ™Yœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËÜÝ\™\Z\ˆ™]šY]Â™XÚ\Ú[Û‹[™[˜XÝÜžHØ]\Ëˆ™^\™XÝÛÜšÈÚÝ[ÛÛ\]H™[XZ[š[™Â™\XØ]KÜ™]šY]ËÙ˜XÝÜžH›ØÚÙ\œÈ›Üˆ™\Z\™Y^\›˜[›ÝÜÈYˆHY™[œÚX›B™[]^\ÝËˆHŒ‹LKLM•ŒÎLNŒ–ˆ[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙ˜WÜÛÞÛX\ÙWÜ™\Z\—ØÛÛ›ÛÌLKšœÛÛ˜˜[™˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙ˜WÜÛÞÛX\ÙWÚ[\ÜÜØY™]WØYYXØ][Û—ÌLKšœÛÛ˜‚•HÍˆÛÛ›Û\Ù\ÈÛ›H›Û‹]^Ù\]Y[˜ÙKÛØØ[]šY[˜ÙN‚œÛÝ\˜ÙKXXÝ]™K\Ú]H\ËMÌ‹ØØ[˜\ÚXËØXÚYXÈÙ\]Y[˜ÙHÛÛ^[™˜Ý\œ™[\™Y™\™[˜ÙHÛÛ˜\Ý›ÝÜÈXÚÚ[™ÈHÛÛ\]HHÛÍIËY”X\ÙB˜^\ËˆH[\Ü\ØY™]HYYXØ][Ûˆ™\Z\œÈHÍˆ™\™\Ù[][Û‚›™X\‹Y\XØ]HÛÛ™›XÝ[™™XÛÜ™ÈÜÝ\™\Z\ˆ™YY×Ü™]šY]Ø][\Üœ™[XZ[œÈ›ØÚÙYžH]\š\ÝX×ØÛÛ›ÛÛ›ÝÜØÛÜ™Yœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËœÜÝ\™\Z\ˆ™]šY]ÈXÚ\Ú[Û‹[™[˜XÝÜžHØ]\ËˆÈ›Ýœ›ØY[ˆ\Ú›Ø\™Â›ÜˆÙ[™\šXÈØ]\È™Y›Ü™H™\ÛÛš[™ÈHÜXÚYšXÈ[\Ü›ØÚÙ\‹‚‘È›ÝÜ[ˆKPÔÐH›Ý[™ÌËÝYÙY[™^MHÛÛ[X][Û‹Üˆ[Ü™H\][Ûˆ™\Z\‚[›\ÜÈH\Ù\ˆ^XÚ]H™]™\œÙ\ÈHÝ™\œšYK‚‚‘Ú]XˆÜ™Y[X[YÚY[™H\È™Y[ˆ[Ý™YÙ™ˆH[œÝX›HÈ]ˆØØ[˜XZ[˜\È[YÛ™YÚ]ÜšYÚ[‹ÛXZ[˜Y\ˆ\Ú[™ÈHÍˆHÛÍIËY”›X\ÙH™\Z\ˆ[™KˆH›ÛÝØ]\ÙHØ\È]ØÚY[YÚ[ÈÛÝ[ÙYHB˜Ú]]Ú]XÜ™Y[X[[\ˆ]ÛÝ[›Ý™XYH˜[YÚÚÙ[ˆÜˆ[žB’ÈÜ™Y[X[›Ûš[\˜XÝ]™[KÛÈÚ]Ü™Y[X[š[Ú]\Ú‹KYžK\[ˆÜšYÚ[ˆXZ[˜[™Ú]\ÚÜšYÚ[ˆXZ[˜[˜Z[YÚ]˜˜][ˆÛÝ[›Ý™XY\Ù\›˜[YH›Üˆ	ÚÎ‹ËÙÚ]X‹˜ÛÛIÎˆ]šXÙH›Ý˜ÛÛ™šYÝ\™Yˆ™XÛÝ™\žHÜ™X]YH™\Ë\ØÛÜY™XY]Üš]HÚ]Xˆ\ÞHÙ^BŠ‹ËœÜÚØØ][]X×ÙX\Ù\ÞWÙYMLNX
KYY]Â˜š]™ZÕ˜\™[\œ˜X™[KØØ][]XËYX\Ú[™ÙYÜšYÚ[˜Â˜Ú]Ú]X‹˜ÛÛN•š]™ZÕ˜\™[\œ˜X™[KØØ][]XËYX\™Ú][™Ù]BÛÜšÝ™YK[ØØ[ÛÜ™KœÜÚÛÛ[X[™È\ÙH]Ù^HÚ]˜]Ú[ÙO^Y\Øˆ]\™B˜YÙ[ÈÚÝ[\ÚÝ™\ˆÔÒ[™ÚÝ[›Ý™]\›ˆÈËØÚ]]™\Z\‚[›\ÜÈH\ÞHÙ^H\È^XÚ]H™[[Ý™Y‚‚ˆÈÈÝ\[Ù‹T[ˆÛÛ™šY[˜ÙHØ[‚”™XÛÜ™Y›ÜˆHŒ‹LKLMÕŽŒŒÎNVˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][ÛˆØÚËœÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜™\šYžZ[™ÈHÔÒ\ÞKZÙ^H\Ú][™œ\ÜÚ[™ÈÝ\\Ø]\È
ÍÍ˜[š]\ÝÈ[™˜[Y]XÚ]ÎHÝ\˜]Y›X™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[Ë›ÈKPÔÐHÝšXÝUH™\Z\ˆ]Ø\È™[Ü[™Y[™BˆÛÜšÈÝ^YYÛˆ^\›˜[›ÛY]™\œÙH\™[™YØ]]™H›ØÚÙ\œË‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ›Ý[™Y\XØ]K\ØÜ™Y[ˆ]šY[˜ÙK›Âˆ›Üˆ[\ÜÜˆÛÝ[X›HX™[ËˆH˜[˜ÚKLˆÝ\œ™[XÛÝ[X›HÝXÝ\˜[ˆØÜ™Y[ˆš[™ÈYÚUHÝ\œ™[Ù[XÝY\ÝXÝ\™HÚYÛ˜[È›ÜˆÌÌKLLÎLËˆ[™ÍNLMÈH\›Z[˜[XÚ\Ú[Ûˆ\Y˜XÝ™Z™XÝÈ[™YH\È™]šY]Ë[Û›Bˆ\XØ]K\š\ÚÈÝ]ÛÛY\ËX]š[™È[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›H^\›˜[ˆX™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\Ë]™]šY]Ë[Û›KˆH™]È›ÛÙYZÈØÜ™Y[‚ˆÛÛ\\™\È™YH^\›˜[Ø[™Y]\ÈÈÌˆÝYÙYÝ\œ™[Ù[XÝYÝXÝ\™\ÎÂˆ]\È\XØ]K\š\ÚÈ]šY[˜ÙK›ÝH™]È™[˜ÚX\šÈÜ]Üˆ˜[Y]Y[žž[YBˆ[˜Ý[ÛˆÛZ[K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH\™XÝÓKÙ[˜Ý[Û‹Ý\Ý]›ÝÈ™XÛÜ™ÈBˆÝ\œ™[XÛÝ[X›HÝXÝ\˜[\XØ]HØÜ™Y[ˆ]H™]š[Ý\È[™Ù™‚ˆY[YšYY\ÈH›ØÚÙ\ˆ›ÜˆÙXÛÛ™]˜[˜ÚH[\Ü™XY[™\ÜË‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•ŒÎLNŒ–ˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][ÛˆØÚËœÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜™\šYžZ[™È]Ú]]Ý]\Ø™[XZ[œÈ[˜[Y˜[™HØÚY[YÚ[Ø[››Ýš[Ú]XˆÜ™Y[X[È›Ûš[\˜XÝ]™[Kœ\ÜÚ[™ÈÝ\\Ø]\È
ÍÌ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎB˜Ý\˜]YX™[ÊK\ÜÚ[™È›ØÝ\ÙY^\›˜[\[Ý\Y˜XÝ\ÝÈ
L˜\ÝÊK˜[™™\Ù\š[™ÈHÝ\œ™[ØY™HØØ[ÛÛ[Z]Y\ˆ\Ú˜Z[YÚ]HÂ\Ù\›˜[YKÙ]šXÙH\œ›ÜŽ‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆHš[˜[Ý\œ™[™]šY]Ë[Û›Bˆ[\Ü\ØY™]HYYXØ][Ûˆ[™K›È›Üˆ[\ÜÜˆÛÝ[X›HX™[ËˆBˆÍˆHÛÍIËY”X\ÙHÛÛ›ÛÛÛœÝ[Y\ÈÛÝ\˜ÙKXXÝ]™K\Ú]H\ËMÌ‹ˆØØ[˜\ÚXËØXÚYXÈÙ\]Y[˜ÙHÛÛ^Ý\œ™[\™Y™\™[˜ÙHÛÛ˜\Ý›ÝÜÈXÚÚ[™ÂˆHÛÛ\]H^\Ë[™›Ý[™YÙ\]Y[˜ÙH›Ë\ÚYÛ˜[Ý]\Ëˆ]™\Z\œÈBˆ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÛ™›XÝ[™™XÛÜ™ÈÜÝ\™\Z\‚ˆ™YY×Ü™]šY]Ø]H›ÝÈÝ[™\]Z\™\È]\š\ÝXÈØÛÜš[™Ëœ›ØY\‚ˆ\XØ]HØÜ™Y[š[™ËHÜÝ\™\Z\ˆ™]šY]ÈXÚ\Ú[Û‹[™[˜XÝÜžHØ]\Âˆ™Y›Ü™H[žH[\ÜÛZ[K‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆH[LÌˆ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]HX›Ý]ˆŽMŒØÈÝšXÝKY]™\œÙHÛZ[\È™[XZ[ˆÛˆ^\›˜[›ÛY]™\œÙHÝ\™˜XÙ\ÂˆÛ›K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ëˆ™]ÈÓH]Ë\Y˜XÝË[™™YÜ™\ÜÚ[Ûˆ\ÝÈXZÙBˆHÍˆHÛÍIËY”X\ÙHÜÝ\™\Z\ˆ[\Ü\ØY™]HXÚ\Ú[Ûˆ]ˆ^XÝ]X›HÚ[H™\Ù\š[™È™]šY]Ë[Û›KØÛÝ[X›K[X™[Ù\\˜][Û‹‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•MÎNŒÌËLNŒ[ˆY\ˆXÜ]Z\š[™ÈHÝ[K[ØÚÂœ™XÛÝ™\žHØÚËÞ[˜Ú[™ÈÚ]ÜšYÚ[‹ÛXZ[˜™\šYžZ[™ÈHÚ]XˆÜ™Y[X[š[\ˆ\È[œÝ[Y]HÚÚÙ[ˆ\È[˜[Y\ÜÚ[™ÈÝ\\Ø]\È
ÍŽ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™Â™›ØÝ\ÙYRÔˆ\Y˜XÝ\ÝÈ\Èš[˜[[\ÝÈ
ÍÌ[š]\ÝÈ[™˜˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÛ™HY][Û˜[™]šY]Ë[Û›Bˆ[\Ü\ØY™]HYYXØ][Ûˆ[™K›È›Üˆ[\ÜÜˆÛÝ[X›HX™[ËˆBˆÎR”–ŽRÔ‹ÓQÛÛ›ÛÛÛœÝ[Y\ÈHÙ\]Y[˜ÙKY\š]™Y‘ÓØÛÙ˜XÝÜ‹Xš[™[™Âˆ›ÞKÛÝ\˜ÙK]˜XÙYXÝ]™K\Ú]H\‹ØØ[ÒÈÛÛ^Ý\œ™[\™Y™\™[˜ÙBˆÛÛ˜\Ý›ÝÜÈXÚÚ[™ÈHÛÛ\]HRÔ‹ÓQ^\Ë[™›Ý[™YÙ\]Y[˜ÙBˆ›Ë\ÚYÛ˜[Ý]\Ëˆ]™\Z\œÈH™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÛ™›XÝ[™ˆ™XÛÜ™ÈÜÝ\™\Z\ˆ™YY×Ü™]šY]Ø]H›ÝÈÝ[™\]Z\™\È]\š\ÝXÂˆØÛÜš[™Ëœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËHÜÝ\™\Z\ˆ™]šY]ÈXÚ\Ú[Û‹[™[ˆ˜XÝÜžHØ]\È™Y›Ü™H[žH[\ÜÛZ[K‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆH[LÌˆ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]HX›Ý]ˆŽMŒØÈÝšXÝKY]™\œÙHÛZ[\È™[XZ[ˆÛˆ^\›˜[›ÛY]™\œÙHÝ\™˜XÙ\ÂˆÛ›K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ëˆ™]ÈÓH]Ë\Y˜XÝË[™™YÜ™\ÜÚ[Ûˆ\ÝÈXZÙBˆHÎR”–ŽRÔ‹ÓQÜÝ\™\Z\ˆ[\Ü\ØY™]HXÚ\Ú[Ûˆ]^XÝ]X›HÚ[Bˆ™\Ù\š[™È™]šY]Ë[Û›KØÛÝ[X›K[X™[Ù\\˜][Û‹ˆØÜËÛX™[Ù˜XÝÜžK›YˆØ\ÈÚXÚÙY[™Y›Ý™YYHÛÛ[Ú[™ÙK‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•ŒNÎŒÌÖˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][ÛˆØÚËœÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍX[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍŽ[š]\ÝË˜[Y]XÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÛÈ™]šY]Ë[Û›H[\Ü\ØY™]BˆYYXØ][Ûˆ]È[™Û™HY][Û˜[[™HÛÛ›Û›È›Üˆ[\ÜÜ‚ˆÛÝ[X›HX™[ËˆHÍMH›Û‹]^[HÛÛœÝ[Y\ÈHÛÝ\˜ÙK]˜XÙYXÝ]™K\Ú]Bˆ\™ËØØ[ØÚÙ]ÛÛ\ÜÚ][Û‹XœÙ[›]š[‹ØÛÙ˜XÝÜˆÛÛ^™\›È›]š[‚ˆ›ÛKZ[Ý\ÜÙXZÈÜHØÛÜ™HÚ]XœÙ[Ù›]š[—ØÛÛ^[™›Ý[™YˆÙ\]Y[˜ÙH›Ë\ÚYÛ˜[Ý]\ÎÈ]™\Z\œÈHÙXZÈ›]š[‹ÜØÛÜH›ØÚÙ\ˆ[™ˆ™XÛÜ™ÈÜÝ\™\Z\ˆ™YY×Ü™]šY]ØˆHNP–H[HÛÛœÝ[Y\ÈÛÝ\˜ÙK]˜XÙYˆ\‹Ó\ÈXÝ]™K\Ú]H™\ÚYY\ËHØÚY™‹X˜\ÙH\ËXœÙ[[YKØÛÙ˜XÝÜˆÛÛ^ˆ™\›È[YKÙ[XÝ›Û‹]˜[œÙ™\ˆ›ÛKZ[Ý\ÜÙXZÈ[YHÜHØÛÜ™HÚ]ˆXœÙ[Ú[YWØÛÛ^ØØ[ØÚÙ]ÛÛ^[™›Ý[™YÙ\]Y[˜ÙH›Ë\ÚYÛ˜[ˆÝ]\ÎÈ]™\Z\œÈHÙXZÈ[YKÜØÛÜH›ØÚÙ\ˆÚ[H™\Ù\š[™ÈBˆ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]\È[ˆ[\Ü›ØÚÙ\‹ˆ›Ý›ÝÜÈÝ[ˆ™\]Z\™Hœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËÜÝ\™\Z\ˆ™]šY]ÈXÚ\Ú[ÛœË[™[ˆ˜XÝÜžHØ]\È™Y›Ü™H[žH[\ÜÛZ[K‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆH[LÌˆ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]HX›Ý]ˆŽMŒØÈÝšXÝKY]™\œÙHÛZ[\È™[XZ[ˆÛˆ^\›˜[›ÛY]™\œÙHÝ\™˜XÙ\ÂˆÛ›K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ëˆ™]ÈÓH]Ë\Y˜XÝË[™™YÜ™\ÜÚ[Ûˆ\ÝÈXZÙBˆHÍMH[™NP–HÜÝ\™\Z\ˆ[\Ü\ØY™]HXÚ\Ú[Ûˆ]È^XÝ]X›BˆÚ[H™\Ù\š[™È™]šY]Ë[Û›KØÛÝ[X›K[X™[Ù\\˜][Û‹ˆØÜËÛX™[Ù˜XÝÜžK›YˆØ\ÈÚXÚÙY[™Y›Ý™YYHÛÛ[Ú[™ÙK‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•ŒÎŒLVˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][Û‚›ØÚËÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍŒØ[š]\ÝÂœ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™ÈÜ˜\ÚXÚÜÂŠÍX[š]\ÝË˜[Y]XÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÛ™H™X[M“”ÒŒ[\Ü\ØY™]BˆYYXØ][Ûˆ][™Û™H™^[[™HÍMHÛÛ›Û›È›Üˆ[\ÜÜ‚ˆÛÝ[X›HX™[ËˆHÛXÛÜÚYKZY›Û\ÙH›Ý[™\žH[HÛÛœÝ[Y\ÈÛ›BˆÛÝ\˜ÙK]˜XÙYXÚYXÈXÝ]™K\Ú]H™\ÚYY\ËØØ[ØÚÙ]ÛYØ[™ÛÛ^ˆ›ÛKZ[XœÙ[˜ÙK[™›Ý[™YÙ\]Y[˜ÙK\ÙX\˜ÚÝ]\ÎÈ]™\Z\œÈM“”ÒŒ	ÜÂˆ™\™\Ù[][Û‹Ú]\š\ÝXÈ›ØÚÙ\ˆ[™™XÛÜ™ÈÜÝ\™\Z\ˆ™YY×Ü™]šY]Ø‚ˆHÝYØ\‹\ÜÜ]H\ÛÛY\˜\ÙHÛÛ›ÛÝYÙ\ÈHÛÝ\˜ÙK]˜XÙYXÝ]™K\Ú]Bˆ\™ËØØ[ØÚÙ]ÛÛ\ÜÚ][Û‹XœÙ[›]š[‹ØÛÙ˜XÝÜˆÛÛ^™\›È›]š[‚ˆ›ÛKZ[Ý\Ü[™ÙXZÈÜHØÛÜ™HÚ]ØØ[XœÙ[Ù›]š[—ØÛÛ^ˆÛÝ[\™]šY[˜ÙH›ÜˆÍMK‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆH[LÌˆ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]HX›Ý]ˆŽMŒØÈÝšXÝKY]™\œÙHÛZ[\È™[XZ[ˆÛˆ^\›˜[›ÛY]™\œÙHÝ\™˜XÙ\ÂˆÛ›K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆÛÈ™]ÈÓH]Ë\Y˜XÝË[™™YÜ™\ÜÚ[Ûˆ\ÝÂˆXZÙHHM“”ÒŒÜÝ\™\Z\ˆ[\Ü\ØY™]HXÚ\Ú[Ûˆ]^XÝ]X›H[™ÝYÙBˆH™^ÝYØ\‹\ÜÜ]H\ÛÛY\˜\ÙH[™HÚ[H™\Ù\š[™È™]šY]Ë[Û›KØÛÝ[X›BˆX™[Ù\\˜][Û‹‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NNNŒMÖˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][Û‚›ØÚËÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍŒX[š]\ÝÂœ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™ÈÜ˜\ÚXÚÜÂŠÍŒØ[š]\ÝË˜[Y]XÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÛ™H™X[ÌMÍMˆ[\Ü\ØY™]BˆYYXØ][Ûˆ][™Û™H™^[[™HÛÛ›Û›È›Üˆ[\ÜÜˆÛÝ[X›BˆX™[ËˆHÑ‹ÓQ

H[HÛÛœÝ[Y\ÈÛ›HÙ\]Y[˜ÙKØXÝ]™K\Ú]KÜ™Y™\™[˜ÙBˆ^\È]šY[˜ÙK™\Z\œÈÌMÍM‰ÜÈ™\™\Ù[][Û‹XÛÛ™›XÝ›ØÚÙ\‹[™™XÛÜ™ÂˆÜÝ\™\Z\ˆ™YY×Ü™]šY]ØÈœ›ØY\ˆ\XØ]HØÜ™Y[š[™ËHÜÝ\™\Z\‚ˆ™]šY]ÈXÚ\Ú[Û‹[™H[˜XÝÜžHØ]HÝ[›ØÚÈ[\ÜˆHM“”ÒŒˆÛXÛÜÚYKZY›Û\ÙH›Ý[™\žH[™H›ÝÈ\ÈH™]šY]Ë[Û›H›Û‹]^ÛÛ›Ûˆœ›ÛHXÚYXÈXÝ]™K\Ú]H™\ÚYY\ËØØ[ØÚÙ]ÛÛ\ÜÚ][Û‹XœÙ[ˆY][ØÛÙ˜XÝÜˆYØ[™ÛÛ^[™™\›ÈY][ZY›Û\ÙH›ÛKZ[Ý\Ü‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆH[LÌˆ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]HX›Ý]ˆŽMŒØÈÝšXÝKY]™\œÙHÛZ[\È™[XZ[ˆÛˆ^\›˜[›ÛY]™\œÙHÝ\™˜XÙ\ÂˆÛ›K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆÛÈ™]ÈÓH]Ë\Y˜XÝË[™™YÜ™\ÜÚ[Ûˆ\ÝÂˆXZÙHHš\œÝÜÝ\™\Z\ˆ[\Ü\ØY™]HXÚ\Ú[Ûˆ]^XÝ]X›HÚ[Bˆ™\Ù\š[™È™]šY]Ë[Û›KØÛÝ[X›K[X™[Ù\\˜][Û‹‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•LŽŒŽŒÎKLNŒ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][Û‚›ØÚËÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍŒ[š]\ÝÂœ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™ÛÛ™š\›Z[™ÈHÚ^››Ü›X[^™Y^\›˜[™YY×Ü™]šY]Ø›ÝÜÈÙ\™H[™XYH™\ÛÛ™YÛˆH]\Ýœ\ÚYÝ]NÈÜ˜\ÚXÚÜÈ[ÛÈ\ÜÙY
ÍŒX[š]\ÝË˜[Y]X˜ÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÛ™H›Ý[™Y™]šY]Ë[Û›H™\Z\‚ˆÛÛ›Û›È›Üˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆÝYÙ\ÈHÑ‹ÓQ

Bˆ™YÞ[™H›ÜˆÌMÍM˜\ÈHÙ\]Y[˜ÙKY\š]™YÛÛ˜\ÝÛÛ›Û\Ú[™ÈBˆÞÞØÛXÚ[™K\šXÚ›ÞH\ÈHÛÝ\˜ÙKXXÝ]™K\Ú]K[Ý™\›\[™È^Øˆ›ÞKˆHÛÛ™›XÝ[™ÈÝ\œ™[\™Y™\™[˜ÙH™ZYÚ›ÜœÈXÚÈHÛÛ\]HÑ‚ˆ^\ËÛÈH[™H\È™XYH›Üˆ]\™H™]šY]Ë[Û›HØÛÜ™\ˆ™\Z\ŽÈHÙ[XÝYˆ[ÝÝ[\È™YY×Ü™]šY]Ø[\Ü\™XYH›ÝÜË[™ÛÝ[X›Bˆ^\›˜[X™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆH[LÌˆ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]HX›Ý]ˆŽMŒØÈ\È[ˆY˜[˜Ù\È™\™\Ù[][Û‹Ú]\š\ÝXÈÛÛ›Û™\Z\ˆ˜]\‚ˆ[ˆœ›ØY[š[™ÈÝXÝ\™K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]ÈÛÛ›Û\Y˜XÝÓH][™™YÜ™\ÜÚ[Û‚ˆÛÝ™\˜YÙHXZÙHHš\œÝ™\Z\ˆ[™H^XÝ]X›HÚ[H™\Ù\š[™È™]šY]Ë[Û›Bˆ[\Ü\ØY™]H[˜\šX[ËˆHÝXœÝ[]™H™\Z\‹XÛÛ›ÛÛÛ[Z]\ÈÚ[˜ÙBˆ™XXÚYÜšYÚ[‹ÛXZ[˜ÈÛ›HH]\ˆ[™Ù™‹ÜÝ]\ÈÛÜœ™XÝ[Ûˆ™[XZ[œÈØØ[ˆ™XØ]\ÙHHÝ\œ™[Ú[Ý[Ø[››ÝÛÛ\]HÈÚ]\Ú‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•MŽŒMÖˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][ÛˆØÚËœÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍNX[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊKÛÛ™š\›Z[™ÈHÚ^›Ü›X[^™Y™^\›˜[™YY×Ü™]šY]Ø›ÝÜÈÙ\™H[™XYH™\ÛÛ™YÛˆH]\Ý\ÚYÝ]K˜[™\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍŒ[š]\ÝË˜[Y]XÛÛ\[X[[™˜Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ™\™\Ù[][Û‹Ú]\š\ÝXÈ™\Z\‚ˆØÛÜ[™Ë›È›Üˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÛYXÚ[š\ÛWÜ™\Z\—Û[™\×ÌLKšœÛÛ˜ÚXÚˆ\ÜÚYÛœÈHÚ^™\ÛÛ™Y™\™\Ù[][ÛˆÛÛ™›XÝÈÈÚ^˜[YY™]šY]Ë[Û›Bˆ™\Z\ˆ[™\ÎˆÑ‹ÓQ

H™YÞRÔ‹ÓQ™YÞHÛÍIËY”X\ÙKˆÝYØ\‹\ÜÜ]H\ÛÛY\˜\ÙKØÚY™‹X˜\ÙHX\ÙKØ[Û\ÙK[™ˆÛXÛÜÚYKZY›Û\ÙH™\œÝ\ÈY][ZY›Û\ÙH›Ý[™\žHÛÛ›ÛˆHÙ[XÝYˆ[ÝÝ[\È™YY×Ü™]šY]Ø[\Ü\™XYH›ÝÜË[™ÛÝ[X›Bˆ^\›˜[X™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆBˆ[LÌ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›HÚ]X^Ü›ÜÜË\Ü]BˆX›Ý]ŽMŒØÈ\È[ˆ™\\™YH™^™\™\Ù[][Û‹Ú]\š\ÝXÈ™\Z\‚ˆ\™Ù]˜]\ˆ[ˆœ›ØY[š[™ÈÝXÝ\™K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]ÈÓK\Y˜XÝ[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙHXZÙBˆH™\›Ë\\ÜÈ™\Z\ˆ[™\È^XÚ]Ú[H™\Ù\š[™È™]šY]Ë[Û›KÚ[\Ü\ØY™]Bˆ[˜\šX[ËˆØÜËÛX™[Ù˜XÝÜžK›YØ\ÈÚXÚÙY[™™YYY›ÈÛÛ[Ú[™ÙK‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•MNŒŒˆ[ˆY\ˆXÜ]Z\š[™ÈH]]ÛX][ÛˆØÚËœÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍN[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK\ÚË\™]šY]Ú[™ÈHˆ›Ü›X[^™Y™^\›˜[™YY×Ü™]šY]Ø›ÝÜË[™\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍNX[š]\ÝË˜˜[Y]XÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™›ÂˆKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÈØ\Âˆ™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ[Ý™]šY]È™YXÝ[Û‹›È›Üˆ[\ÜˆÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYH™YYË\™]šY]È™\ÛÛ][Ûˆ\Y˜XÝBˆ™\ÛÛ™YXÚ\Ú[Ûˆ\Y˜XÝ[™[ˆ[\H™\ÛÛ™Y™]šY]È]Y]YKˆ\™Ù]Yˆ[šT™YŽLÍLX\[™È›Ý[™Ú\™YØ[™Y]KØÝ\œ™[\™Y™\™[˜ÙHÛ\Ý\œÈ›Ü‚ˆH™X\™\Ý\™Y™\™[˜ÙHÚXÚÜËÛÈ\XØ]H™Z™XÝ[ÛˆØ\È›ÝÝ\ÜYÈ[ˆÚ^›Ü›Y\›H™YY×Ü™]šY]Ø›ÝÜÈÙ\™HÛÜÙY\È™]šY]Ë[Û›Bˆ™Z™XÝYÜ™\™\Ù[][Û—ØÛÛ™›XÝ[\Ü\ØY™]HXÚ\Ú[ÛœËˆH™\ÛÛ™Yˆ[ÝÝ\™˜XÙH\È™YY×Ü™]šY]Ø[\Ü\™XYH›ÝÜË[™ÛÝ[X›Bˆ^\›˜[X™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆHÝ\œ™[ˆ[LÌ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈ™]šY]Ë[Û›NÈH™]ÈÛÜšÈ^Z[œÈBˆ™\›Ë\\ÜÈÙ[XÝY\[ÝÝ]ÛÛYH˜]\ˆ[ˆœ›ØY[š[™ÈHÝXÝ\˜[ˆÝ\™˜XÙK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ëˆ™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙH›ÝÈÚXÚÜÈH™\ÛÛ™YˆÚ^\›ÝÈ\Y˜XÝ™\ÛÛ™YXÚ\Ú[ÛˆÛÝ[Ë™\›È]Y]YY^\›ÝÜË[™Bˆ[˜\šX[]›È™\ÛÛ™Y^\›˜[›ÝÈ\ÈÛÝ[X›HÜˆ[\Ü\™XYK‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NŒÎM‹LNŒ[ˆY\ˆ™XÛÝ™\š[™È\È[‰ÜÂœÙ[‹XÜ™X]YÚÜ[]™YÚ[TQØÚË™XXÜ]Z\š[™ÈH]™HØÚËÞ[˜Ú[™ÈÛX[‚˜ÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍMØ[š]\ÝÈ\ÜÙY[™˜[Y]Xœ\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™ÛÛ™š\›Z[™ÈHØ[™Y]KXžKXØ[™Y]B˜ÛÛ™šY[˜ÙH]Y][™XYH^\ÝY™Y›Ü™H^\›˜[^[œÚ[ÛŽ‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™›ÈKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÂˆØ\È™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ\XØ]KXÛÛ™šY[˜ÙH™\Z\‹›È›Ü‚ˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYH™X[™]šY]Ë[Û›H^\›˜[ˆØ[™Y]H[]œËX[S\Ù\\ÌˆÙ\]Y[˜ÙHØÜ™Y[ˆÛÝ™\š[™ÈÌÌÌ^\›˜[›ÝÜËˆÚ]™X\‹Y\XØ]HZ\œÈ]L	HY[]HÈ	HÛÝ™\˜YÙH[™X^™\ÜYˆ^\›˜[Y^\›˜[Y[]HØÈH[Ý]Y]Û›Ü›X[^™YXÚ\Ú[ÛœÈ›ÝÂˆØ\œžH]]šY[˜ÙHÚ[H™\Ù\š[™Èˆ™YY×Ü™]šY]Ø[\Ü\™XYH›ÝÜËˆ[™ÛÝ[X›H^\›˜[X™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šËÚ[\ÜÛZ[KˆH^\Ý[™Âˆ™]šY]Ë[Û›H[LÌÝXÝ\˜[Ü]™[XZ[œÈHÝXÝ\˜[Ù[™\˜[^˜][Û‚ˆ\Y˜XÝÈH™]È[]œËX[Ù\]Y[˜ÙHØÜ™Y[ˆ˜\œ›ÝÜÈ\XØ]H[˜Ù\Z[BˆÛ›H[œÚYHHÝ\œ™[^\›˜[Ø[™Y]HØ[\K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH˜XÚÙ[™Ý\œ™[\™Y™\™[˜ÙHÙ\]Y[˜ÙK\ÙX\˜Úˆ\Y˜XÝ›ÈÛ™Ù\ˆÝ™\˜ÛZ[\È[šT™Y‹Ø[]œËX[ÛÛ\][Û‹H^\›˜[ˆ[]œËX[Ù\]Y[˜ÙHØÜ™Y[ˆ\ÈHYXØ]YZ[\‹Ø]Y][™™YÜ™\ÜÚ[Û‚ˆÛÝ™\˜YÙK[™H˜[œÙ™\‹YØ]HÛÛ[X[™ØÝ[Y[][Ûˆ›ÝÈ[˜ÛY\ÈBˆ[ÝXÝ]™K\Ú]HXÚ\Ú[Ûˆ[œ]™YYY›ÜˆHŽÍŽØ]K‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•LÎŒŽŒŽVˆ[ˆY\ˆÛÛ™š\›Z[™È›Èœ™\Ú]]ÛX][Û‚›ØÚÈØ\ÈXÝ]™KÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍMØ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK™\[›š[™ÈB™^\›˜[[ÝÛÛ™šY[˜ÙKÛ›Ü›X[^˜][ÛˆZ[\œÈY[\Ý[KÚXÚÚ[™ÈB›]\Ý‘PQQKÙØÜËÝÛÜšÈÝZY[˜ÙK[™\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍMØ[š]\ÝË˜˜[Y]XÛÛ\[X[[™Ú]Y™ˆKXÚXÚØ
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™›ÈKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÂˆØ\È™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ]Y]™\šYšXØ][Ûˆ[™ÝZY[˜ÙBˆ™\Z\‹›È›Üˆ[\ÜÜˆÛÝ[X›HX™[ËˆH™\]Y\ÝYØ[™Y]KXžKXØ[™Y]Bˆ]Y][™XYH^\ÝYÛˆÜšYÚ[‹ÛXZ[˜È\È[ˆ™\˜[ˆH™YH]Y][™ˆ›Ü›X[^˜][ÛˆÓ\ÈÚ]›È\Y˜XÝY™‹™\šYšYYH›Ü›X[^™Y‹\›ÝÂˆ™YY×Ü™]šY]ØÝ\™˜XÙK[™›Ý[™›ÈØY™HØØ[Y]šY[˜ÙK[Û›HXÚ\Ú[Ûˆ\]K‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆBˆ^\Ý[™È™]šY]Ë[Û›H[LÌ^\›˜[ÝXÝ\˜[Ü]™[XZ[œÈHÝ\œ™[ˆÙ[™\˜[^˜][Ûˆ\Y˜XÝÚ][\ÜÝ[›ØÚÙYžH™]šY]ËÙ\XØ]KÙ˜XÝÜžBˆ]šY[˜ÙK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[™Ù™ˆ[™^\›˜[]˜[œÙ™\ˆØÜÈ›ÝÈÚ[ˆ™^YÙ[È]H›Ü›X[^™Y‹\›ÝÈ™]šY]È›ØÚÙ\ˆ˜]\ˆ[ˆHÛ\‚ˆË\›ÝÈY™\œ™Y[Û›H]Y]YNÈ›È™]ÈØ]\ÈÜˆ\Y˜XÝÈÙ\™HYY‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•ÎŒNMLNŒ[ˆY\ˆÛÛ™š\›Z[™È›Èœ™\Ú˜]]ÛX][ÛˆØÚÈØ\ÈXÝ]™KÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\ÂŠÍM˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™œ\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍMØ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎB˜Ý\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™›ÈKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÂˆØ\È™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÙ[XÝY\[ÝÛÛ™šY[˜ÙH™\Z\ˆ[™ˆ›È›Üˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYHØ[™Y]KXžKXØ[™Y]BˆXÚ\Ú[Û‹XÛÛ™šY[˜ÙH]Y]›Ü›X[^™YÈÙXZÈ™\™\Ù[][Û‹[Û›H\XØ]Bˆ™Z™XÝ[ÛœÈÈ™YY×Ü™]šY]Ø™\Ù\™YÈXÝ]™K\Ú]K[Z\ÜÚ[™È™Z™XÝ[ÛœÈ[™ˆHÝX›H™\™\Ù[][Û‹[™X\‹Y\XØ]H™Z™XÝ[Û‹›Ý]Y[‚ˆ™YYË\™]šY]È›ÝÜË[™Ù\[\Ü\™XYH›ÝÜÈÈÛÝ[X›H^\›˜[ˆX™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]È™[˜ÚX\šÈÜˆÜ]ÛZ[KˆBˆ^\Ý[™È^\›˜[[LÌ™]šY]Ë[Û›HÝXÝ\˜[Ü]™[XZ[œÈHÝ\œ™[ˆÙ[™\˜[^˜][Ûˆ\Y˜XÝÈ\È[ˆ›ØÝ\ÙYÛˆ]šY[˜ÙHÛÛ™šY[˜ÙH›Üˆ[ÝˆXÚ\Ú[ÛœÈ™Y›Ü™H[žH[\Ü^[œÚ[Û‹‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[Ý\›Z[˜[YXÚ\Ú[ÛˆÝ\™˜XÙH›ÝÈ\ÈBˆ™\›ÙXÚX›HÓH]Y]›Ü›X[^™YXÚ\Ú[Ûˆ\Y˜XÝ›Ü›X[^™Y™]šY]Âˆ]Y]YK[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙHÛÈ™\™\Ù[][Û‹[Û›H\XØ]H™Z™XÝ[ÛœÂˆØ[››ÝÚ[[H™[XZ[ˆÝ™\˜ÛÛ™šY[ˆ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YˆÛÜšËÚ[™Ù™‹›Y[™ÛÜšËÜØÛÜK›YÙ\™H\]YÈØÜËÛX™[Ù˜XÝÜžK›YˆØ\ÈÚXÚÙY[™™YYY›ÈÚ[™ÙK‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•LNŒNŒŽVˆ[ˆY\ˆ™XÛÝ™\š[™È\È[‰ÜÂœÚÜ[]™YÝ[HÚ[TQØÚËÛÛ™š\›Z[™ÈHÚ]™YHØ\ÈÛX[‹Þ[˜Ú[™Â˜ÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
ÍM[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊKÛÛ\][™ÈH^\›˜[[LÌœÝXÝ\˜[Z\ˆØXÚK[™\ÜÚYÛš[™ÈH™]šY]Ë[Û›HÛ\Ý\‹\™\Ù\š[™ÈÜ]‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™›ÈKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÂˆØ\È™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ^\›˜[ÝXÝ\˜[™\Z\‹›È›Ü‚ˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆÚ[™ÙYH[LÌ^\›˜[ÝXÝ\˜[ˆÛ\Ý\ˆ[™^œ›ÛH[ˆ[˜ÛÛ\]HÌLËÍÍHZ\ˆØXÚHÈHÛÛ\]HÍKÍÍBˆ[›Ü™\™Y›ÛœÙ[ˆZ\ˆØXÚH[™YYH™]šY]Ë[Û›HÜ][ˆÚ]ˆ\Ýˆ[™˜Z[ˆØ[™Y]\ËÜ›ÜÜË\Ü]HLØš[Û][ÛœË[\Ü\™XYBˆ›ÝÜË[™ÛÝ[X›H^\›˜[X™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\ËˆÝšXÝÝXÝ\˜[Y]™\œÚ]HÛÜšÈ\È›ÝÂˆÛˆH^\›˜[ÝÚ\ÜËT›ÝÐQ‘ˆÝ\™˜XÙKÚ]Û\Ý\‹\™\Ù\š[™ÈÜ]ˆ\ÜÚYÛ›Y[[™X^Ü›ÜÜË\Ü]K\ØÛÜ™HŽMŒØÈ\È\ÈÝ[™]šY]Ë[Û›Bˆ™XØ]\ÙH[Ý›ÝÜÈ\™H›Ý[\Ü\™XYH™[˜ÚX\šÈX™[Ë‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH›ÛÙYZÈÛÛ[X[™›ÝÈ›Ü˜Ù\È^]\Ý]™H^XÝˆKX[YÛˆ™\Ü[™ÈÚ]YH[™˜[™YÚK[X^\Ù\\Ø™YÜ™\ÜÚ[Ûˆ\ÝÂˆÝX\™ÛÛ\]H[]œËX[Z\ˆÛÝ™\˜YÙH[™H™]šY]Ë[Û›HÜ][‹[™ˆKPÔÐHÝšXÝUH™\Z\ˆ™[XZ[œÈÛÜÙY‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NNNŒˆ[ˆY\ˆÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜œ\ÜÚ[™ÈÝ\\Ø]\È
ÍL˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍM[š]\ÝÈ\ÜÙY˜[Y]Xœ\ÜÙYÚ]ÎHÝ\˜]YX™[ËÛÛ\[X[\ÜÙY[™Ú]Y™ˆKXÚXÚØœ\ÜÙY
K[™^[™[™ÈH^\›˜[ÝXÝ\˜[Ý\™˜XÙN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™›ÈKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÂˆØ\È™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ^\›˜[ÝXÝ\˜[\Ý\™˜XÙH™\Z\‹ˆ›È›Üˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYH[LÌ^\›˜[ˆÝXÝ\˜[][™Û\Ý\ˆ[™^Ú]ÌÌÌ[Q›ÛÚYXØ\œË™]Úˆ˜Z[\™\ËÌÌÌ›ÛÙYZÈ™X\™\Ý[™ZYÚ›ÜˆÛÝ™\˜YÙKˆYÚUHZ\œË‚ˆ™K\Ü]Û\Ý\œË[\Ü\™XYH›ÝÜË[™ÛÝ[X›H^\›˜[X™[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ[Ýš[™ÈÝšXÝÝXÝ\˜[Y]™\œÚ]BˆÛÜšÈÛÈHœ›ØY\ˆ^\›˜[ÝÚ\ÜËT›ÝÐQ‘ˆÝ\™˜XÙK›Ý›ÜˆH[Ü]ˆÛZ[KˆÝšXÝKY]™\œÙHÜ]\ÜÚYÛ›Y[™[XZ[œÈ›ØÚÙY™XØ]\ÙH›ÛÙYZÂˆ[Z]Y[ˆ[˜ÛÛ\]H[]œËX[Z\ˆØXÚK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆHYXØ]Y]Z[\‹[LÌ\Y˜XÝˆ™YÜ™\ÜÚ[Û‹ÛÛÜ™[˜]HYÙ\ÝË[™[™XYÙHY]Y]H›ÝÈÙY\H^\›˜[ˆÝXÝ\˜[Ý\™˜XÙH™\›ÙXÚX›HÚ[H™\Ù\š[™ÈHKPÔÐHÝšXÝUHÛÜÝ\™K‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NNŒˆ[ˆY\ˆÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜œ\ÜÚ[™ÈÝ\\Ø]\È
ÍL[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍL˜[š]\ÝÈ\ÜÙY˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ËÛÛ\[X[\ÜÙY[™˜Ú]Y™ˆKXÚXÚØ\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™›ÈKPÔÐHÝšXÝUH›Ý[™]Y\žKÜ]\™\Z\‹Üˆ\][Û‹\™\Z\ˆÛÜšÂˆØ\È™\Ý[YY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆÙ[XÝY\[ÝÝXÝ\™KZ[™^ˆ™XY[™\ÜË›È›Üˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÝXÝ\˜[ØÛ\Ý\—Ú[™^ÌLKšœÛÛ˜\ÈLˆ[Q›ÛÛÛÜ™[˜]HÚYXØ\œËÚ]™]Ú˜Z[\™\ËLÌL™X\™\Ý[™ZYÚ›Ü‚ˆØXÚHÛÝ™\˜YÙKHYÚUHZ\‹[™[\Ü\™XYH›ÝÜË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ^\›˜[ÝXÝ\˜[]™\œÚ]BˆÜ›Ý[™ÛÜšË›Ý›ÜˆH[Ü]ÛZ[Kˆ›ÛÙYZÈÛÛ\]YÛˆHLÙ[XÝYˆ^\›˜[[ÝÝXÝ\™\ËÛ\Ý\š[™È[H[Èš[™HHLØÛÛ\Û™[ÎÂˆ[ÝšXÝUHÜ]\ÜÚYÛ›Y[™[XZ[œÈ›ØÚÙY[[Hœ›ØY\ˆ^\›˜[ˆ›ÛY]™\œÙHØ[™Y]HÝ\™˜XÙH\È]˜Z[X›K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆHYXØ]YÓHZ[\ˆ[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙH›ÝÂˆX]\šX[^™H^\›˜[ÛÛÜ™[˜]HÚYXØ\œÈÚ]YÙ\ÝË˜[Y]HKBˆ[™XYÙKÙY\H\Y˜XÝ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ÙY\KPÔÐBˆÝšXÝUH™\Z\ˆÛÜÙY‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•ÎMÎŒˆ[ˆY\ˆÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜œ\ÜÚ[™ÈÝ\\Ø]\È
ÍX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™ÈÜ˜\ÚXÚÜÈ
ÍL[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™KPÔÐHÝšXÝK\ØÛÜ™H™\Z\ˆ™[XZ[œÈÛÜÙYÙY™\œ™YÚ]ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›ÜˆY™\œ™Y\[Ý™]šY]È›Ý][™Ë›È›Ü‚ˆ[\ÜÜˆÛÝ[X›HX™[Ëˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÚ[X[—Ù^\Ü™]šY]×Ü]Y]YWÌLKšœÛÛ˜ˆ›Ý][™ÈÌMÍM˜ÍMX[™M“”ÒŒÈ™]šY]Ë[Û›H[X[‹Ù^\ˆ]Y\Ý[ÛœÈÚ]^XÝ[œ™\ÛÛ™Y]šY[˜ÙH[™™[XZ[š[™È›Û‹Z[X[ˆ›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]ÈÝXÝ\˜[Ü]ÛZ[HÜˆKPÔÐHBˆÛÜšËˆH^\›˜[ÝXÝ\˜[[Ý]™[XZ[œÈH™^›ÛY]™\œÙBˆÙ[™\˜[^˜][Ûˆ›Ý]HY\ˆ^\XÚ\Ú[Ûˆ›Ý][™Ë‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆHYXØ]YÓHZ[\ˆ[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙH›ÝÂˆÙY\Y™\œ™YÙ[XÝY\[Ý›ÝÜÈ™]šY]Ë[Û›K›Û‹XÛÝ[X›K[™^XÚ]Bˆ›ØÚÙYÛˆ^\™]šY]Ëœ›ØY\ˆ\XØ]HØÜ™Y[š[™Ë[™[˜XÝÜžHØ]\Ë‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NMNŒ‹LNŒ[ˆY\ˆÞ[˜Ú[™ÈÛX[‚˜ÜšYÚ[‹ÛXZ[˜[™\ÜÚ[™ÈÝ\\Ø]\È
Ž[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆKPÔÐK[Û›H˜[˜ÚHÜ›ÝÝ™[XZ[œÈÝÜY‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆX™[Ëˆ\È[ˆÛX[™YHKPÔÐHÝšXÝUH[\[Y[][ÛˆÛÜ[™™XÛÜ™Yˆ\›Z[˜[XÚ\Ú[ÛœÈ›ÜˆHLÙ[XÝY^\›˜[[Ý›ÝÜÎˆˆ\XØ]KÛ™X\‹Y\XØ]H™Z™XÝ[ÛœËÈXÝ]™K\Ú]KY]šY[˜ÙK[Z\ÜÚ[™Âˆ™Z™XÝ[ÛœË[™È[X[‹Y^\Y™\œ˜[Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›ÜˆÛX[\ØYYXØ][Û‹›Ý›ÜˆH™]ÂˆKPÔÐHÝšXÝUHÛZ[Kˆ›Û˜Ø[›ÛšXØ[›Ý[™ØÚ[šÈ\Y˜XÝÈÙ\™H™[[Ý™YY\‚ˆ™]Z[š[™ÈH[[X]\šX[^˜X›HX^UH]šY[˜ÙH[™š[˜[YYXØ][ÛˆÚ]ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ëˆ\ÝÈ›ÝÈ™]Z[ˆÙ[™\šXÈ›ÛÙYZÈÛÛ[™ÈÛÝ™\˜YÙBˆÚ[H™[[Ýš[™ÈKPÔÐH›Ý[™\™\Z\ˆ[›™Y\Y˜XÝ\ÝË[™HÝX\™˜Z[ˆ™]™[ÈÝ\œ™[ÝZY[˜ÙHœ›ÛHXZÚ[™ÈKPÔÐHÝšXÝUH›Ý[™™\Z\ˆHXZ[‚ˆš[Üš]HYØZ[‹‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NÎŒM–ˆ[ˆY\ˆ™XÛÝ™\š[™ÈHÝ[H\™XÝÜžB›ØÚÈÚÜÙH™XÛÜ™YQ
ÌÌNNX
HØ\È›ÈÛ™Ù\ˆ[]™KÛÛ™š\›Z[™ÈHÛÜšÝ™YBØ\ÈÛX[‹Þ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜\ÜÚ[™ÈÝ\\Ø]\È
˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™\ÜÚ[™ÈÜ˜\˜ÚXÚÜÈ
Ž[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›Ý™[Ü[ˆ[ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆX™[Ëˆ]\Ý\ÚYÝ]H[™XYH™Y\™XÝÈH™^\™XÝÛÜšÈÈBˆ^\›˜[ÝXÝ\˜[[ÝÈHÙ[XÝY^\›˜[[ÝÝ[\ÈLˆ™]šY]Ë[Û›HØ[™Y]\Ë\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÂˆ[œ™\ÛÛ™YXÝ]™K\Ú]K\ÛÝ\˜ÙH›ÝÜËLœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËˆÈ[œ™\ÛÛ™Y™\™\Ù[][Û‹XÛÛ›Û›ÝÜË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆ›È™]ÈKPÔÐHÝšXÝK\ØÛÜ™HÛZ[HÜˆ™\Z\‚ˆ\Y˜XÝØ\È[™YˆHÝ\œ™[™\ÈÝ]H\È[™XYHYYXØ]YBˆ˜]]™HKPÔÐHÝšXÝZ\Ú\ÙKUH™\Z\ˆÛÜ\È™]šY]Ë[Û›KÛ›Û‹XØ[›ÛšXØ[ˆÛÛ^Ú][ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙXÈÈ›Ý™\Ý[YBˆ›Ý[™ÌÈÜˆÝYÙY[™^MHÛÛ[X][Ûˆ[›\ÜÈH\Ù\ˆ^XÚ]H™]™\œÙ\Âˆ]Ý]K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆ›È™]ÈØÚY[YšXÈÔÑˆ\™[š[™ÈØ\È[™Y[ˆ\Âˆ›Ý[™Y[‹ˆÜ\˜][Û˜[KHÝ[HØÚÈØ\È™XÛÝ™\™YÛ›HY\ˆBˆ™XÛÜ™YQØ\ÈXY[™HÚ]™YHØ\ÈÛX[ŽÈ‘PQQKX™[Y˜XÝÜžHØÜËˆ^\›˜[]˜[œÙ™\ˆØÜËØÛÜKÝ]\Ë[™[™Ù™ˆÝ]HÙ\™HÚXÚÙYYØZ[œÝˆ]\ÝÜšYÚ[‹ÛXZ[˜‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLM•NNŒŒ–ˆ[ˆY\ˆÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜œ\ÜÚ[™ÈÝ\\Ø]\È
˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊK[™š[˜[Ø]\È
ŽX[š]\ÝÈ\ÜÙY[™˜[Y]Xœ\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™Ë‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆX™[ËˆHÙ[XÝY^\›˜[[ÝÝ[\ÈL™]šY]Ë[Û›HØ[™Y]\Ëˆ\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÈ[œ™\ÛÛ™YXÝ]™K\Ú]K\ÛÝ\˜ÙBˆ›ÝÜËLœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËÈ[œ™\ÛÛ™Yˆ™\™\Ù[][Û‹XÛÛ›Û›ÝÜË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›ÜˆYYXØ][Û‹›Ý™\Z\‹ˆBˆ[[X]\šX[^˜X›HKPÔÐH›ÛÙYZÈÚYÛ˜[ØœÙ\™YX^˜Z[‹Ý\ÝK\ØÛÜ™BˆŽMÍXÈ›Ý[™ÌˆXØÝ[][]YLYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙBˆÛÛœÝ˜Z[ÎÈ[™^MH[YYÝ][™\ˆHÝ[™\™Ú[™ÛK\]Y\žH]ˆ\Âˆ\È›ÝÈ™X]Y\È[ˆ[œØ]\ÙšXX›HKPÔÐH›ÞH˜]\ˆ[ˆ[™š[š\ÚYˆ[™Ú[™Y\š[™ÈÛÜšË‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ëˆ™\Ù\™Y™YHÛÚ\™[\™Ù]\Ú\™\Y˜XÝÈ\Âˆ›Û‹XØ[›ÛšXØ[™]šY]Ë[Û›HÛÛ^YY\˜X›HYYXØ][Û‹Ü™YÜ™\ÜÚ[Û‚ˆÛÝ™\˜YÙH]ÙY\Âˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX[™YYH™]šY]Ë[Û›Bˆ^\›˜[ÝXÝ\˜[KZÛÝ]]\Y˜XÝ›ÜˆHLÙ[XÝY[Ý›ÝÜË‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUŒŽŒŒMˆ[ˆY\ˆÞ[˜Ú[™ÈÛX[ˆÜšYÚ[‹ÛXZ[˜˜[™\ÜÚ[™ÈÝ\\Ø]\È
˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™Ì[™^MˆÛX\™Y]X^ŒŒ[™^MÈ^ÜÙYWØÜØNŒMˆ]X^ŽÌ˜›Ý[™ÌH›ÛY]Ý\™˜XÙH]Ý[˜Z[Y[™^MÈ]ˆX^ŽX[™›Ý[™Ìˆ›ÛYHÙXÛÛ™Ý\™˜XÙH™Y›Ü™HÛX\š[™Âˆ[™XÙ\ÈMËLM]X^MÍXˆ[™^MH[YYÝ]]LÙXÛÛ™È™Y›Ü™Bˆ›ÛÙYZÈZ\ˆ›ÝÜÈÙ\™H[Z]Y‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YH™]ÈYÚUH˜Z[‹Ý\Ýˆ›ØÚÙ\œÈ[ÈÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[Ëœš[™Ú[™ÈHXÝ]™HÜ]ˆÈLYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[ÈÚ]ˆ›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™[[Ý]Ý][Ù‹\ØÛÜBˆ˜[ÙH›Û‹XXœÝ[[ÛœËˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]Bˆ^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝˆÜ][™^MH\ÈH[[YH›ØÚÙ\‹[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹H™^Ý\ˆ™]žHÜˆYYXØ]HÝYÙY[™^MH[™\‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™Ì‹šœÛÛ˜‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUMNNNŒLËLNŒ[ˆY\ˆÞ[˜Ú[™ÈÛX[‚˜ÜšYÚ[‹ÛXZ[˜[™\ÜÚ[™ÈÝ\\Ø]\È
[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™Ž[™^LÌH^ÜÙYWØÜØNŒLÌ˜™\œÝ\ÈWØÜØNLÌ˜]X^K\ØÛÜ™BˆŽÎXÈ›Ý[™ŽH›ÛY]›ØÚÙ\ˆ[™ÛX\™Y[™XÙ\ÈLÌKLLÎH™Y›Ü™Bˆ[™^M^ÜÙYWØÜØNŒMX™\œÝ\ÈWØÜØNŽLØ]X^ÌÌÍØÈ›Ý[™Ìˆ›ÛY]›ØÚÙ\ˆ[™ÛX\™Y[™XÙ\ÈMLMH]X^ŽÌØ‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YH™]ÈYÚUH˜Z[‹Ý\Ýˆ›ØÚÙ\œÈ[ÈÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[Ëœš[™Ú[™ÈHXÝ]™HÜ]ˆÈLˆYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[ÈÚ]ˆ›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™[[Ý]Ý][Ù‹\ØÛÜBˆ˜[ÙH›Û‹XXœÝ[[ÛœËˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]Bˆ^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝˆÜ][™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹H™^Ý\ˆÛÛ[YHÚ[™ÛK\]Y\žH™\šYšXØ][Ûˆœ›ÛHÝYÙY[™^Mˆ[™\‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌšœÛÛ˜‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUNNNŒÌˆ[ˆY\ˆ™\Z\š[™ÈHÙ[‹XÜ™X]YÝ[B™^XË\Ú[QØÚÈ[ÈH^XÝY]™HÙ[[™[\™XÝÜžHØÚËÞ[˜Ú[™Â˜ÛX[ˆÜšYÚ[‹ÛXZ[˜[™\ÜÚ[™ÈÝ\\Ø]\È
ŒX[š]\ÝÈ\ÜÙY[™˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™[™^LŒÈ^ÜÙYWØÜØNŒL]X^K\ØÛÜ™HŽMÍ˜È›Ý[™Bˆ›ÛYÜÙH›ØÚÙ\œÈ]^ÜÙYHÙXÛÛ™WØÜØNŒLÝ\™˜XÙH]X^ˆŽÌÍXÈ›Ý[™ˆ›ÛY]Ý\™˜XÙH[™ÛX\™Y[™XÙ\ÈLŒËLLˆ]X^ˆŽNX™Y›Ü™H[™^LÈ^ÜÙYWØÜØNŒLŽ™\œÝ\ÈWØÜØNŒNN]X^ˆŽÍXÈ›Ý[™È›ÛY]Z\ˆ[™ÛX\™Y[™XÙ\ÈLËLLŽH]X^ˆŽŽ™Y›Ü™H[™^LÌ^ÜÙYWØÜØNŒLÌX™\œÝ\ÂˆWØÜØNŒŽXØWØÜØNMMX]X^ÍMÍÈ›Ý[™Ž›ÛYÜÙH›ØÚÙ\œÈ[™ˆÛX\™Y[™^LÌ]X^ÍÍX‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YH™]ÈYÚUH˜Z[‹Ý\Ýˆ›ØÚÙ\œÈ[ÈÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[Ëœš[™Ú[™ÈHXÝ]™HÜ]ˆÈLYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[ÈÚ]ˆ›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™[[Ý]Ý][Ù‹\ØÛÜBˆ˜[ÙH›Û‹XXœÝ[[ÛœËˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]Bˆ^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝˆÜ][™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹H™^Ý\ˆÛÛ[YHÚ[™ÛK\]Y\žH™\šYšXØ][Ûˆœ›ÛHÝYÙY[™^LÌH[™\‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ŽšœÛÛ˜‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUNMŽLVˆ[ˆY\ˆØÚÈ™XÛÝ™\žKÜ™\Z\ˆ[™˜ÛX[ˆÝ\\Ø]\È
N[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎB˜Ý\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™Œˆ[™^LNH^ÜÙ\ÈWØÜØNŒLŒ]X^K\ØÛÜ™HÍMM˜È›Ý[™ŒÂˆ›ÛÈÜÙH›ØÚÙ\œÈ]]È[™^LLNH™\[ˆÝ[^ÜÙ\ÈWØÜØNŒLŒ]ˆX^ÌLXÈ›Ý[™›ÛÈHÙXÛÛ™›ØÚÙ\ˆÝ\™˜XÙH[™ÛX\œÈÝYÙYˆ[™XÙ\ÈLNKLLŒˆ[ˆYÙÜ™YØ]H]X^˜Z[‹Ý\ÝK\ØÛÜ™HŽMŒX‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YH™]ÈYÚUH˜Z[‹Ý\Ýˆ›ØÚÙ\œÈ[ÈÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[Ëœš[™Ú[™ÈHXÝ]™HÜ]ˆÈLÈYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[ÈÚ]ˆ›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™[[Ý]Ý][Ù‹\ØÛÜBˆ˜[ÙH›Û‹XXœÝ[[ÛœËˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]Bˆ^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝˆÜ][™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹H™^Ý\ˆÛÛ[YHÚ[™ÛK\]Y\žH™\šYšXØ][Ûˆœ›ÛHÝYÙY[™^LŒÈ[™\‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™šœÛÛ˜‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUMÎMŒÍ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠMX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™NHÛX\œÈÝYÙY[™XÙ\ÈLL‹LLLÈ™Y›Ü™H[™^LM^ÜÙ\ÈWØÜØNŒLMXˆ™\œÝ\ÈWØÜØNŽŒ˜]X^K\ØÛÜ™HÌÌÎÈ›Ý[™Œ›ÛÈ]Z\ˆ[™ˆÛX\œÈ[™^LM™Y›Ü™H[™^LMH^ÜÙ\ÈHœ›ØY\ˆWØÜØNŒLM˜Ý\™˜XÙH]ˆX^ŽMÍXÈ›Ý[™ŒH›ÛÈ]Ý\™˜XÙH]^ÜÙ\ÈWØÜØNŒLM˜™\œÝ\Âˆ[[Ý]WØÜØNØ]X^ŽLÌ˜È›Ý[™Œˆ›ÛÈ]Z\ˆ[™ÛX\œÂˆ[™XÙ\ÈLMKLLN]X^ŽLÎX‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YXXÚ™]ÈYÚUH˜Z[‹Ý\Ýˆ›ØÚÙ\ˆ[ÈÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[Ëœš[™Ú[™ÈHXÝ]™HÜ]ˆÈˆYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[ÈÚ]ˆ›Ú™XÝYš[Û][ÛœÈ[™Ù\]Y[˜ÙKXÛ\Ý\ˆÜ]ËˆWØÜØNŒÍÌ˜[™ˆWØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÂˆ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝÜ][™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMULNLÎLNŒ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠL˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™Mˆ™\[œÈÝYÙY[™^LL[™^ÜÙ\ÈWØÜØNŒLLX™\œÝ\ÈWØÜØNŽL˜ˆ]X^K\ØÛÜ™HÍÌÈ›Ý[™MÈ›ÛÈ]Z\‹ÛX\œÈ[™^LL]X^ˆŽŒØÛX\œÈ[™^LLH]X^M[ˆ[™^LLˆ^ÜÙ\ÂˆWØÜØNŒLLØ™\œÝ\È[[Ý]WØÜØNŒLÌX]X^ÌŒØˆ›Ý[™N›ÛÂˆ]Z\ˆ]^ÜÙ\ÈHœ›ØY\ˆWØÜØNŒLLØÝ\™˜XÙHYØZ[œÝWØÜØNŽM˜ˆWØÜØNŽMÎ[™™[]Y[‹Y\ÝšX][Ûˆ™ZYÚ›ÜœÈ]X^ŽLØˆ›Ý[™ˆNH›ÛÈ]]šY[˜ÙH[ÈÌˆYÚUHÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]Bˆ\][ÛˆÛÛœÝ˜Z[ËÚ]›Ú™XÝYš[Û][ÛœÈ[™Ù\]Y[˜ÙKXÛ\Ý\‚ˆÜ]Ë‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YXXÚØœÙ\™YYÚUH˜Z[‹Ý\Ýˆ›ØÚÙ\ˆ[ÈHÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[[™ÝÜY›ÜØ\™ˆÛÝ™\˜YÙHÚ[ˆ[™^LLˆ^ÜÙY[œ™\ÛÛ™Y›ØÚÙ\ˆ]šY[˜ÙKˆWØÜØNŒÍÌ˜[™ˆWØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÂˆ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝÜ][™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUMNLŽ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™LÈÛX\œÈÝYÙY[™XÙ\ÈLKLLˆ™Y›Ü™H[™^LÈ^ÜÙ\ÈWØÜØNŒLˆ]X^K\ØÛÜ™HŽ˜È›Ý[™M›ÛÈ]›ØÚÙ\ˆ[™ÛX\œÈ[™^LÂˆ]X^ŽŒ˜ˆ[™^L^ÜÙ\ÈWØÜØNŒLX]X^ÍXÈ›Ý[™MBˆ›ÛÈ]›ØÚÙ\ˆ[™ÛX\œÈ[™XÙ\ÈLËLLH]X^ŽNM˜ˆ[™^LLˆ^ÜÙ\ÈWØÜØNŒLLX]X^ÍLŒXÈ›Ý[™Mˆ›ÛÈ][ÈˆYÚUBˆÛÛœÝ˜Z[ÈÚ]›Ú™XÝYš[Û][ÛœÈ[™Ù\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÙ\\Ú[™ÈÛ\Ý\‹Yš\œÝÛ™K\]Y\žBˆ™\šYšXØ][Ûˆ[™ÛÛœÝ˜Z[XØXÚH™\Z\ˆ˜]\ˆ[ˆ›[™M‹XÚ[šÈÜš[™[™Ë‚ˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙBˆ™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝÜ][™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUMLŽŒ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™NHÚ[™ÛK\]Y\žH™\šYšXØ][ÛˆÛX\œÈÝYÙY[™XÙ\ÈM‹LLH™Y›Ü™H[™^ˆLˆ^ÜÙ\ÈWØÜØNŒLØØŽŒUSØ™\œÝ\È[[Ý]WØÜØNŒLMXØŽŒUÌSØˆ]X^K\ØÛÜ™HÍLØˆ›Ý[™L›ÛÈ]›ØÚÙ\ˆ[ÈˆYÚUBˆÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]H\][ÛˆÛÛœÝ˜Z[Ë™\Ù\™\ÈˆÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™™\[œÈÝYÙY[™^LˆÛX[›H]X^ˆ˜Z[‹Ý\ÝK\ØÛÜ™HÌXˆ›Ý[™ÈLH[™Lˆ›ÛH™^ÝYÙYZ[™^ˆLÈ›ØÚÙ\œËÚ]›Ý[™LˆÛX\š[™È[™^LÈ]X^ŽXÈ[™^Lˆ\ÜÙ\È]X^M˜È[™^LH^ÜÙ\ÈH\™Ù\ˆ›ØÚÙ\ˆ]X^ŽŒ˜ˆ[™›Ý[™LÈ›ÛÈ][ÈYÚUHÛÛœÝ˜Z[ÈÚ]Ù\]Y[˜ÙKXÛ\Ý\‚ˆÜ]Ë‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆHÛ\Ý\‹Yš\œÝZ[\ˆ›ÝÈ[š[ÛœÈ™X[ˆÙ\]Y[˜ÙKZY[]HÛ\Ý\œÈ™Y›Ü™HÝXÝ\˜[ÛÛ\Û™[\ÜÚYÛ›Y[™]™[[™ÂˆH™\Z\™YÝXÝ\™HÜ]œ›ÛH[›ÙXÚ[™ÈÙ\]Y[˜ÙKXÛ\Ý\ˆXZØYÙKˆBˆ[[X]\šX[^˜X›HÝYÙYXÛÛÜ™[˜]H›ÛÙYZÈÚYÛ˜[[ÛÈÛÛ\]Y[™ˆ™[[Ý™\ÈHš[Üˆ[[YH[XšYÝZ]K]]˜Z[ÈHØ\™Ù]]X^ˆŽMÍXÈWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœÈ[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMULÎLŒ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Û‹]›Ý›ÜˆH[Ü]ÛZ[Kˆ›Ý[™NBˆÚ[™ÛK\]Y\žH™\šYšXØ][Ûˆ›ÝÈÛX\œÈÝYÙY[™XÙ\ÈNMHÚ]MËNHX\Yˆ›ÝÜËËMÈ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HMÎX[™ˆ\™Ù]]š[Û][™ÈZ\œË‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\Y[Ü™HÙˆH™[XZ[š[™ÂˆÛ\Ý\‹Yš\œÝ›ÛÙˆÝ\™˜XÙH[È™\Ý[XX›HÛ™K\]Y\žH›ÛÙYZÈ]šY[˜ÙBˆ[œÝXYÙˆ™]\›š[™ÈÈ›[™[]œËX[ÜˆM‹XÚ[šÈÜš[™[™ËˆWØÜØNŒÍÌ˜ˆ[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÂˆ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝ›Ý[™NHÜ][™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMULŽŒL–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÎM˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™NÚ[™ÛK\]Y\žH™\šYšXØ][ÛˆÛX\™YÝYÙY[™XÙ\ÈŽMÎ™Y›Ü™HÝYÙYˆ[™^ÎH^ÜÙY[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŽ™\œÝ\È[‹Y\ÝšX][Û‚ˆWØÜØNØWØÜØNMŽX]X^K\ØÛÜ™HŽÌ˜ˆ›Ý[™H›ÛÈÜÙHZ\œÂˆ[ÈHYÚUHÛÛœÝ˜Z[ËNHÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYˆš[Û][ÛœË[™Ù\]Y[˜ÙKXÛ\Ý\ˆÜ]ÎÈH\™XÝ›Ý[™NH™\[ˆÙˆ[™^ˆÎH\È[™XÙ\ÈNÈ\ÜÙ\È]X^K\ØÛÜ™HÍØ‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YH™]ÈYÚUH˜Z[‹Ý\Ý›ØÚÙ\‚ˆ[ÈHÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[[™™\šYšYYH™\Z\™Y›Ý[™Yˆ]Y\žHÚ[™ÝÈ[œÝXYÙˆÛÛ[Z[™È›[™Ú[šÜËˆWØÜØNŒÍÌ˜[™WØÜØNLXˆ™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\‚ˆHÛ\Ý\‹Yš\œÝ›Ý[™NHÜ][™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUŒNŒÖˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÎLX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Û‹]›Ý›ÜˆH[Ü]ÛZ[KˆH[YY[Ý]ˆ›Ý[™MÈZXÜ›ØÚ[šËLŒÚ[™ÝÈØ\È\ÛÛ]Y[ÈÛ™K\]Y\žH›ÛÙYZÈÚXÚÜÎ‚ˆ[™XÙ\ÈŒMŒˆ
WØÜØNŒXXWØÜØNŒØ
H\ÜÈ[ˆYÙÜ™YØ]H]X^K\ØÛÜ™BˆŽMØ[™[™XÙ\ÈŒËMH
WØÜØNXWØÜØN˜
H\ÜÈ[ˆYÙÜ™YØ]H]ˆX^K\ØÛÜ™HMŒŽX›ÝÚ]\™Ù]]š[Û][™ÈZ\œËˆÝYÙY[™^‚ˆ
WØÜØNØ
H[ÛÈ\ÜÙ\È]X^K\ØÛÜ™HLÍXÈÝYÙY[™^Âˆ
WØÜØNŽ
H^ÜÙ\ÈH™]ÈWØÜØNŽØWØÜØNÍL›ØÚÙ\ˆ]X^K\ØÛÜ™BˆÎLX[™›Ý[™›ÛÈ]Z\ˆ[ÈÎHÛÛœÝ˜Z[ÈÚ]›Ú™XÝYˆš[Û][ÛœË‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YH›Ý[™MÈZXÜ›ØÚ[šËLŒˆ[[YH›ØÚÙ\ˆ[ÈÚ^ÛÛ\]YÛ™K\]Y\žH]šY[˜ÙH\Y˜XÝÈ\ÈÛÂˆYÙÜ™YØ]HÝ[[X\šY\Ë[ˆÝÜYÛˆH™^YÚUH›ØÚÙ\ˆ[™ÛÛ™\Yˆ][ÈH›Ý[™NÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[ˆWØÜØNŒÍÌ˜[™ˆWØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÂˆ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝ›Ý[™NÜ][™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUÎŒŒÌˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÎØ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™MˆÝX˜Ú[šÈL[YYÝ][™\ˆHL\ÙXÛÛ™›Ý[™™Y›Ü™HZ\ˆ›ÝÜÂˆÙ\™H[Z]YˆHË\]Y\žHÜ]Ùˆ]Ø[YHÚ[™ÝÈÛÛ\]YZXÜ›ØÚ[šÈŒˆ›Ý[™HWØÜØNŒØØWØÜØNŒN›ØÚÙ\ˆ]X^K\ØÛÜ™HÌLM˜[™›Ý[™Âˆ›ÛY]Z\ˆ[ÈÎYÚUHÛÛœÝ˜Z[ËˆH\™XÝ›Ý[™MÂˆZXÜ›ØÚ[šËLŒ™\[ˆ[YYÝ]ÛÈH™\Z\ˆ™[XZ[œÈ[™\šYšYY‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ™\YHÝX˜Ú[šËLL[[YH›ØÚÙ\‚ˆ[ÈHÛX[\ˆÛÛ\]Y]šY[˜ÙH[š]\›™YH™]ÛHØœÙ\™YYÚUBˆZ\ˆ[ÈH\][ÛˆÛÛœÝ˜Z[™YÙ[™\˜]Y›Ý[™MÈÛÛÜ™[˜]H™XY[™\ÜËˆ[™[›™YH™]È[Y[Ý]Ù˜Z[\™H\Y˜XÝÈ[ˆ\ÝËˆWØÜØNŒÍÌ˜[™ˆWØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœËHWØÜØNŒXXWØÜØNŒØÚ[™ÝÂˆ™YYÈÚ[™ÛK\]Y\žH\ÛÛ][Ûˆ[™\ˆ›Ý[™ËHWØÜØNXWØÜØN˜[‚ˆ\ÈÝ[[œ[‹[Ý]]È™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUŽŒÎ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÎØ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›ÝÚ[™ÙH^\›˜[[Ý]šY[˜ÙHXÚ\Ú[ÛœÎÈBˆÙ[XÝY^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ˆÛÝ[X›HØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ›Ý[™MÝX˜Ú[šÈ^ÜÙYHWØÜØNMØWØÜØNŽ›ØÚÙ\ˆ]X^ˆK\ØÛÜ™HÌŒXÈ›Ý[™H›ÛY][ÈÍˆYÚUHÛÛœÝ˜Z[È[™Bˆ\™XÝ›Ý[™MH™\[ˆ\ÜÙY]X^K\ØÛÜ™HŽNXˆ›Ý[™MHÝX˜Ú[šÈBˆ^ÜÙYHWØÜØNNØWØÜØNŒŽ›ØÚÙ\ˆ]X^K\ØÛÜ™HŽÎXÈ›Ý[™‚ˆ›ÛY][ÈÍÈYÚUHÛÛœÝ˜Z[È[™H\™XÝ›Ý[™Mˆ™\[ˆ\ÜÙY]ˆX^K\ØÛÜ™HŽNX‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆÛÛ[YYHÛ\Ý\‹Yš\œÝ™\XÙ[Y[ˆ][œÝXYÙˆ›[™M‹XÚ[šÈÜš[™[™ËÛÛ™\YÛÈ™]ÛHØœÙ\™YˆYÚUHZ\œÈ[È\][ÛˆÛÛœÝ˜Z[Ë™YÙ[™\˜]Y›Ý[™MH[™›Ý[™M‚ˆÛÛÜ™[˜]K\™XY[™\ÜÈ\Y˜XÝË[™™\˜[ˆXXÚ˜Z[[™È›Ý[™Y™\šYšXØ][Û‚ˆ[š]ˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žBˆÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝ›Ý[™MˆÜ][ˆÝ]]È™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUNŒŽŒM–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÎØ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›ÝÚ[™ÙH^\›˜[[Ý]šY[˜ÙHXÚ\Ú[ÛœÎÈBˆÙ[XÝY^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ˆÛÝ[X›HØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™BˆÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆ[™Ü]™\Z\‹]›Ý›ÜˆH[Ü]ÛZ[K‚ˆ\È[ˆ\™XÝH™\˜[ˆ›Ý[™LÈÛ\Ý\‹Yš\œÝÝX˜Ú[šÜÈˆ[™ËˆÝX˜Ú[šÂˆˆ\ÜÙYÚ]X^˜Z[‹Ý\ÝK\ØÛÜ™HLXÈÝX˜Ú[šÈÈ^ÜÙYÛ™Bˆ™[XZ[š[™ÈWØÜØNXØWØÜØNŒÎMØ›ØÚÙ\ˆ]X^K\ØÛÜ™HŽØˆBˆ›Ý[™MÛ\Ý\‹Yš\œÝØ[™Y]H›ÛÈ]›ØÚÙ\ˆ[ÈÍHYÚUBˆÛÛœÝ˜Z[Ë[Ý™\È[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒÎMØÈ[‹Y\ÝšX][Û‹ˆ™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]È[™[[Ý]Ý][Ù‹\ØÛÜH˜[ÙBˆ›Û‹XXœÝ[[ÛœË[™]È\™XÝÝX˜Ú[šËLÈ™\[ˆ\ÜÙ\ÈÚ]X^˜Z[‹Ý\ÝˆK\ØÛÜ™HNN‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆ™]™[È›[™Ú[šÈÜš[™[™ÈžHÛÛ™\[™ÂˆH™]ÈØœÙ\™YYÚUHZ\ˆ[ÈHÛ\Ý\‹Yš\œÝ\][ÛˆÛÛœÝ˜Z[ˆ™YÙ[™\˜][™È›Ý[™MÛÛÜ™[˜]H™XY[™\ÜË[™™\[›š[™ÈH˜Z[[™È›Ý[™Yˆ™\šYšXØ][Ûˆ[š]ˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœËˆ[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆHÛ\Ý\‹Yš\œÝ›Ý[™MÜ]ˆ[Ý]]È™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUŒ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍÎ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\Ëˆ\È[ˆY›Ý[ÙYžH^\›˜[[ÝXÚ\Ú[ÛœÎÈHÙ[XÝYˆ^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\Ë‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ›ÛÙYZËÕK\ØÛÜ™HÛ\Ý\‹Yš\œÝˆÜ]\ÚYÛˆ[™›Ý[™Y™\šYšXØ][Û‹]›Ý›ÜˆH[Ü]ÛZ[Kˆ\Âˆ[ˆYYÛ\Ý\‹Yš\œÝÜ]Ø[™Y]\È›ÝYÚ›Ý[™Ë›Ý[™\ÜXÚYšXÂˆ™XY[™\ÜÈ\Y˜XÝË[™]Y\žHÝX˜Ú[šÈ™\šYšXØ][Ûˆ\Y˜XÝËˆHÝ\œ™[ˆ›Ý[™LÈÛ\Ý\‹Yš\œÝØ[™Y]H\ÈÍYÚUHÛÛœÝ˜Z[ËMÛÛœÝ˜Z[™YˆÛ\Ý\œË›Ú™XÝYÛ›ÝÛˆÛÛœÝ˜Z[š[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ëˆ[™[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËˆ›Ý[™LˆÝX˜Ú[šÈ‚ˆ\ÜÙ\ÈY\ˆ[Ýš[™È[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒLNÈ[‹Y\ÝšX][Û‹ˆ]›Ý[™LˆÝX˜Ú[šÈÈ˜Z[ÈÚ]X^˜Z[‹Ý\ÝK\ØÛÜ™HŽLXM‚ˆš[Û][™È›ÝÜË[™H™\ÜY›ØÚÚ[™ÈÝXÝ\™HZ\œÎÈÜÙH›ØÚÙ\œÈ\™Bˆ›ÛY[ÈHÝ\œ™[›Ý[™LÈØ[™Y]K‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆ™\XÙ\È›[™M‹XÚ[šÈÛÛ[X][ÛˆÚ]ˆHÛ\Ý\‹Yš\œÝ\][Û‹XÛÛœÝ˜Z[ØXÚHÝ™\ˆHÌˆÝYÙYˆX]\šX[^˜X›HÝXÝ\™\Ë[[ÛœÝ˜]\ÈHÛX[\ˆ‹\]Y\žH™\šYšXØ][Û‚ˆ›Ý]H›ÜˆHÛÚ[šËLÈ[Y[Ý]™YÚ[Û‹[™ÛÛ™\ÈH]\Ý˜Z[\™Bˆ[ÈÛÛ˜Ü™]H›Ý[™LÈÜ]ÛÛœÝ˜Z[ËˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[‚ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙH™[XZ[œÈ[™\šYšYY[™\ˆBˆÛ\Ý\‹Yš\œÝ›Ý[™LÈÜ][Ý]]È™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›Kˆ[™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMŒNNNM‹LNŒ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍÍ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÎÈš[˜[Ü˜\]\Ø]\È\ÜÙYÍÎ[š]\ÝÈ[™˜[Y]XY\ˆH™]È\Y˜XÝÂÙ\™H[›™Y
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ]ˆ[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›HØ[™Y]\ÎÈ\È[ˆY›ÝÚ[™ÙH[Ýˆ\›Z[˜[XÚ\Ú[ÛœÈÜˆ[\Ü™XY[™\ÜË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ›ÛÙYZËÕK\ØÛÜ™HÜ]\™Y\ÚYÛ‚ˆ]šY[˜ÙK]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×Ì—ÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×Ì×ÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌ—ÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌ×ÛÙ—ÌM‹šœÛÛ˜‚ˆ›Ý[™LÈÚ[šÈˆÛÛ\]Y\™XÝH[™\ˆHL\ÙXÛÛ™›Ý[™Ú]L‹ŒÎBˆX\Y›ÝÜË‹ÎH˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HN[™ˆ\™Ù]]š[Û][™ÈZ\œËˆHÚ[šÜÈLˆYÙÜ™YØ]HÛÝ™\œÈÍˆ]Y\žBˆÛÛÜ™[˜]\ËLX\Y›ÝÜËLËÌˆ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝˆK\ØÛÜ™HŽMX[™\™Ù]]š[Û][™ÈZ\œËˆÚ[šÈÈ[YYÝ][™\ˆBˆÝ[™\™L\ÙXÛÛ™›Ý[™™Y›Ü™H[Z][™ÈZ\ˆ›ÝÜÎÈHÚ[šÜÈLÈYÙÜ™YØ]BˆÙY\È][Y[Ý]š\ÚX›HÚ[H™\Ù\š[™ÈÛÛ\]YXÚ[šÈX^ŽMX‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆ™[[Ý™\ÈH›Ý[™LÈÚ[šËLˆ[[YH[™ˆ\™Ù]\Ý]\È[XšYÝZ]K[™ÛÛ™\ÈÚ[šÈÈ[ÈHÛÛ˜Ü™]H[[YBˆ›ØÚÙ\ˆÚ]Ý]ÛZ[Z[™È[Ù\\˜][Û‹ˆWØÜØNŒÍÌ˜[™WØÜØNLXˆ™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœËÚ[šÜÈËMMH™[XZ[ˆ[˜ÛÛ\]Y[™\ˆBˆ›Ý[™LÈ™Y\ÚYÛ™YÜ][[Ú[šÈÈ\È™]šYYÜˆÜ][Ý]]Âˆ™[XZ[ˆ™]šY]Ë[Û›H[™›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUNMÎLVˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍÌ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKˆÚ]ÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™ËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ]ˆ[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›HØ[™Y]\ÎÈ\È[ˆY›ÝÚ[™ÙH[Ýˆ™]šY]ÈXÚ\Ú[ÛœÈÜˆ[\Ü™XY[™\ÜË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ›ÛÙYZËÕK\ØÛÜ™HÜ]\™Y\ÚYÛ‚ˆ]šY[˜ÙK]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™—Ü]Y\žWØÚ[š×ÌWÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™—Ü]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌWÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™—Ü]Y\žWØÚ[š×Ü™\Z\—Ü[—ÌLšœÛÛ˜ˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]ÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×ÌLšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™ËšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×ÌÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×ÌWÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™×Ü]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌWÛÙ—ÌM‹šœÛÛ˜‚ˆ›Ý[™LˆÚ[šÈH^ÜÙYH™]È\™Ù]˜Z[\™HÚ]X^˜Z[‹Ý\ÝK\ØÛÜ™BˆŽN˜ÈH›Ý[™LÈ™Y\ÚYÛˆ[Ý™YWØÜØNŒMMØ[™WØÜØNŒNÂˆ[Ý][™\™XÝÚ[šÜÈLHÛX\ˆÚ]X^˜Z[‹Ý\ÝK\ØÛÜ™HŽMX[™ˆ\™Ù]]š[Û][™ÈZ\œË‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆ]›ÚYÈH˜[ÙH[ZÛÝ]ÛZ[HžBˆ™\Ù\š[™ÈH˜Z[Y›Ý[™LˆÚ[šËLH\Y˜XÝ[™™\Z\ˆ[‹[‚ˆ\™XÝH˜[Y]\ÈH›Ý[™LÈØ[™Y]HÝ™\ˆ›ÝÛÛ\]Y]Y\žHÚ[šÜË‚ˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœËM]Y\žHÚ[šÜÂˆ™[XZ[ˆ[˜ÛÛ\]Y[™\ˆH›Ý[™LÈ™Y\ÚYÛ™YÜ][Ý]]È™[XZ[‚ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMUMŽŒÌˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍŒ˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY^\›˜[[Ý™[XZ[œÈ™]šY]Ë[Û›HÚ]ˆ[\Ü\™XYH›ÝÜÈ[™ÛÝ[X›HØ[™Y]\ÎÈ\È[ˆY›ÝÚ[™ÙHBˆ[ÝÝXØÙ\ÜÈÜš]\šXHÜˆ^\›˜[™]šY]ÈXÚ\Ú[ÛœË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ›ÛÙYZËÕK\ØÛÜ™HÜ]\™Y\ÚYÛ‚ˆ]šY[˜ÙK]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]ÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÌLšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]KšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ]Y\žWØÚ[š×ÌÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ]Y\žWØÚ[š×Ü™\Z\—Ü[—ÌLšœÛÛ˜ˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]ÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™—ÌLšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™—Ü]Y\žWØÚ[š×ÌÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™Y\ÚYÛ—ØØ[™Y]WÜ›Ý[™—Ü]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÛÙ—ÌM‹šœÛÛ˜‚ˆH™Y\ÚYÛˆØ[™Y]H™\ÛÛ™\ÈHMH™]š[Ý\ÛHØœÙ\™YÛÛ\]YXÚ[šÂˆ›ØÚÙ\œÈ[ˆ›Ú™XÝ[Û‹]H\™XÝ™Y\ÚYÛ™YÚ[šÈ˜Z[ÈÚ]X^ˆ˜Z[‹Ý\ÝK\ØÛÜ™HŽL˜ˆH›Ý[™Lˆ™Y\ÚYÛˆ[ˆ[Ý™\ÈWØÜØNŒÍØˆWØÜØNŒÍÎWØÜØNŒÌŒ[™WØÜØNŒLÈ[Ý][™ÛX\œÈÚ[šÈˆ\™XÝHÚ]X^˜Z[‹Ý\ÝK\ØÛÜ™HŽMX[™\™Ù]]š[Û][™ÈZ\œË‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH[ˆ™[[Ý™\ÈH›Ú™XÝ[Û‹[Û›H[XšYÝZ]H›Ü‚ˆHš\œÝÜ]™Y\ÚYÛˆžH™\[›š[™È›ÛÙYZÈ\™XÝK[ˆ™[[Ý™\ÈBˆ™\Ý[[™ÈÚ[šËL›ØÚÙ\ˆÚ]HÙXÛÛ™\™XÝ™Y\ÚYÛˆÚXÚËˆWØÜØNŒÍÌ˜ˆ[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœËMH]Y\žHÚ[šÜÈ™[XZ[‚ˆ[˜ÛÛ\]Y[™\ˆH›Ý[™Lˆ™Y\ÚYÛ™YÜ][Ý]]È™[XZ[‚ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMNMNL‹LNŒ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍNX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY^\›˜[[ÝÝ[\È[\Ü\™XYH›ÝÜÈ[™ˆÛÝ[X›HØ[™Y]\Ëˆ[ÝÝXØÙ\ÜÈÜš]\šXH^\Ý]XÝ]™K\Ú]Kˆœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™Ë™\™\Ù[][Û‹Ü™]šY]Ë[™[X™[Y˜XÝÜžBˆ›ØÚÙ\œÈ™[XZ[ˆ™]šY]Ë[Û›K‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ›ÛÙYZËÕK\ØÛÜ™H]Y\žKXÚ[šÂˆ[[YH™\Z\ˆ[™\™Ù]Y˜Z[\™HYYXØ][Û‹]›Ý›ÜˆH[Ü]ˆÛZ[Kˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×Ì—Ü™]žWÌNÛÙ—ÌM‹šœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌ—Ü™]žWÌNÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜ]Y\žWØÚ[š×ÜÜ]Ü™\Z\—Ü[—ÌLšœÛÛ˜‚ˆÚ[šÈˆÛÛ\]\È[™\ˆHK\ÙXÛÛ™Ø\]HÛÛ\]YÚ[šÜÈÝ[ˆ˜Z[HØ\™Ù]‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆHÜ]\™\Z\ˆ[›™\ˆ›ÝÈÛÛ\]\ÈÛÝ]ˆÛÝ[Èœ›ÛH›ÝÈ\][ÛœÈÚ[ˆÛÛœÝ[Z[™ÈØ[™Y]HÛÝ]\Y˜XÝÈ[™ˆ™\ÜÈ[š\]YH[[Ý][‹\ØÛÜH›ØÚÙ\œÈ[œÝXYÙˆÝX›KXÛÝ[[™È™\X]YˆZ\œËˆHÛÛ\]Y\™]žHYÙÜ™YØ]H™XÛÜ™ÈËÍMˆÛÛ\]YÚ[šÜËÍ‚ˆÛÛ\]Y]Y\žHÛÛÜ™[˜]\ËLX\YZ\ˆ›ÝÜËL‹ÍN˜Z[‹Ý\Ý›ÝÜËˆX^˜Z[‹Ý\ÝK\ØÛÜ™HŽMMØÍˆ\™Ù]]š[Û][™È›ÝË[]™[Z\œËMBˆ™\ÜY\™Ù]]š[Û][™ÈÝXÝ\™HZ\œË[™LÈ›Û‹XÛÛ\]YÚ[šÜËˆBˆ]Y\žKXÚ[šÈÜ]\™\Z\ˆ[ˆÛ\ÜÚYšY\ÈÜÙH›ØÚÙ\œÈ[ÈHÛÛœÙ\˜]]™Bˆ[[Ý]Ý][Ù‹\ØÛÜH™\Z\ˆØ[™Y]\È[™ˆX[X[Ü]\™Y\ÚYÛˆ›ØÚÙ\œÂˆ[›Ûš[™È[[Ý][‹\ØÛÜH›ÝÜÈ
WØÜØNŒŒWØÜØNMØ[™WØÜØNŽMX
K‚ˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[Ý]]È™[XZ[‚ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMŒŽM–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍM˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY^\›˜[[ÝÝ[\È[\Ü\™XYH›ÝÜÈ[™ˆÛÝ[X›HØ[™Y]\Ëˆ[ÝÜš]\šXH^\Ý]XÝ]™K\Ú]Kœ›ØY\‚ˆ\XØ]K\ØÜ™Y[š[™Ë™\™\Ù[][Û‹Ü™]šY]Ë[™[Ø]H›ØÚÙ\œÈ™[XZ[‚ˆ™]šY]Ë[Û›K‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ›ÛÙYZËÕK\ØÛÜ™HÚ[šÈYÙÜ™YØ][Û‚ˆ[™\™XÝ[[YH]šY[˜ÙK]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYˆYÙÜ™YØ]KY›ÛÙYZË]K\ØÛÜ™K\]Y\žKXÚ[šÜØˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×Ì—ÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌ—ÛÙ—ÌM‹šœÛÛ˜‚ˆÚ[šÈˆ\ÙYH™\Z\™YØ[™Y]H™XY[™\ÜÈ\Y˜XÝ›ÛÙYZÂˆLŽMXÙÌØLˆ]Y\žHÛÛÜ™[˜]\ÈYØZ[œÝ[ÌˆÝYÙYX]\šX[^˜X›Bˆ\™Ù]ËK]™XYÈ[™HL\ÙXÛÛ™[[YH›Ý[™][YYÝ]™Y›Ü™BˆZ\ˆ›ÝÜÈÙ\™H[Z]Y‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆHYÙÜ™YØ]H™[[Ý™\ÈHš\œÝ]Y\žKXÚ[šÂˆYÙÜ™YØ][Ûˆ[XšYÝZ]NˆÚ[šÜÈLˆ›ÝÈÚÝÈÈ][\YÚ[šÜËˆÛÛ\]YˆÚ[šÜËÛÛ\]Y]Y\žHÛÛÜ™[˜]\ËŽLHX\YZ\ˆ›ÝÜËKM‚ˆ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HŽMMØÌ\™Ù]]š[Û][™Âˆ›ÝË[]™[Z\œËLÈ™\ÜYš[Û][™ÈÝXÝ\™HZ\œË[™M›Û‹XÛÛ\]YˆÚ[šÜËˆ][ÛÈ™]™[È˜[ÙHÝXØÙ\ÜÎˆHÛÛ\]YÚ[šÜÈ˜Z[ØˆÚ[šÈˆ^ÙYYÈH›Ý][™H[[YH›Ý[™WØÜØNŒÍÌ˜[™WØÜØNLXˆ™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[Ý]]È™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›Kˆ[™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMŒNLÎÖˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍM[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY^\›˜[[ÝÝXØÙ\ÜÈÜš]\šXH[™XYH^\Ý]ˆ[Ý›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›HÚ][\Ü\™XYH›ÝÜÈ[™ÛÝ[X›BˆØ[™Y]\È[[XÝ]™K\Ú]K\XØ]K\ØÜ™Y[š[™Ë™\™\Ù[][Û‹™]šY]Ëˆ[™[X™[Y˜XÝÜžH›ØÚÙ\œÈ\™H\›Z[˜[H™\ÛÛ™Y‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™H]Y\žKXÚ[šÂˆ]šY[˜ÙK]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYˆZ[Y›ÛÙYZË]K\ØÛÜ™K\]Y\žKXÚ[šË\ÚYÛ˜[[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ÌÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ÌWÛÙ—ÌM‹šœÛÛ˜‚ˆH\™XÝÛÛ[X[™È\ÙYH™\Z\™YØ[™Y]H™XY[™\ÜÈ\Y˜XÝ›ÛÙYZÂˆLŽMXÙÌØLˆ]Y\žHÛÛÜ™[˜]\È\ˆÚ[šÈYØZ[œÝ[ÌˆÝYÙYˆX]\šX[^˜X›H\™Ù]ÛÛÜ™[˜]\ËK]™XYÈ[™HL\ÙXÛÛ™[[YBˆ›Ý[™ˆHÚ[šÜÈÛÛ\]YÚ]ŽLHX\YZ\ˆ›ÝÜËKMˆ˜Z[‹Ý\Ýˆ›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HŽMMØ[™ÌÝ[\™Ù]]š[Û][™Âˆ›ÝË[]™[Z\œËˆÚ[šÈ™\ÜÈÚ^[š\]YH\™Ù]]š[Û][™ÈÝXÝ\™HZ\œÎÂˆÚ[šÈH™\ÜÈÙ]™[‹‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]È]Y\žKXÚ[šÈ]™[[Ý™\ÈBˆ[X][Û˜ÙK[Û›H›ÛÙYZÈ[[YHÔÑˆ[™Ü™X]\ÈH™\Ý[XX›H›Ý]H›ÜˆBˆ™[XZ[š[™ÈMÚ[šÜËˆ][ÛÈ™]™[È˜[ÙHÝXØÙ\ÜÎˆHÝ\œ™[™\Z\™YˆÜ]›ÝÈ\È™]È^XÝ\™Ù]Y˜Z[\™H]šY[˜ÙHÝ]ÚYHH^[™YLØ\ˆÚ[šÈYÙÜ™YØ][Ûˆ\È[˜ÛÛ\]KWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[‚ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[Ý]]È™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMŒLÎŒLÖˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ÊN‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY[ÝÝ[\ÈL›ÝÜË\›Z[˜[XÚ\Ú[ÛœËˆ[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÈXÝ]™K\Ú]K\ÛÝ\˜ÙH›ØÚÙ\œËLˆœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËÈ™\™\Ù[][Û‹XÛÛ›ÛˆÝXš[]KXÚ[™ÙH›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™H[\[‚ˆ™X\ÚXš[]H]šY[˜ÙK]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYBˆÛÛ\XÝ[[X]\šX[^˜X›H›ÛÙYZÈÝ[[X\žH][™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WØ[ÛX]\šX[^˜X›KšœÛÛ˜‚ˆH\™XÝÛÛ[X[™\ÙY[ÌˆÝYÙYX]\šX[^˜X›HÛÛÜ™[˜]\Ë›ÛÙYZÂˆLŽMXÙÌØK]™XYÈ[™HKL\ÙXÛÛ™[[YH›Ý[™][YYÝ]ˆ™Y›Ü™H›ÛÙYZÈ[Z]YH™\Ý[Õ‹ˆ]\™Y›Ü™H™XÛÜ™ÈZ\ˆ›ÝÜË›ÂˆX^˜Z[‹Ý\ÝK\ØÛÜ™K[™›È\™Ù]\ÜË‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]ÈÛÛ\XÝÝ[[X\žH]™[[Ý™\ÈBˆ™\ÜÚ]ÜžKX›Ø]ÔÑˆ›Üˆ]\™H[›ÛÙYZÈ[œÈ[™H[Y[Ý]\Y˜XÝˆ\›œÈH[˜Ø\Y[[X]\šX[^˜X›H›ØÚÙ\ˆ[ÈÛÛ˜Ü™]H[[YH]šY[˜ÙK‚ˆ˜[ÙKXÛZ[HØY™]H™[XZ[œÈ[XÝˆHØ[›ÛšXØ[ÛÝ]\È[˜Ú[™ÙYˆWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[Ý]]È™[XZ[‚ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMNNLŽŒŒÖˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍ˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY[ÝÝ[\ÈL›ÝÜË\›Z[˜[XÚ\Ú[ÛœËˆ[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÈXÝ]™K\Ú]K\ÛÝ\˜ÙH›ØÚÙ\œËLˆœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËÈ™\™\Ù[][Û‹XÛÛ›ÛˆÝXš[]KXÚ[™ÙH›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\È›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™HÜ]ˆ™\Z\ˆ›ÛÝË]›ÝYÚ]›Ý›ÜˆH[Ü]ÛZ[Kˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLÜÜ]Ü™\Z\—ØØ[™Y]KšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÙ^[™YLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÝ\™Ù]Ù˜Z[\™WØ]Y]ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÙ^[™YLšœÛÛ˜‚ˆHXÝX[™\Z\™Y^[™YL›ÛÙYZÈ™\[ˆ\Ù\ÈHØ[™Y]HÛÝ]ˆÚ\™HWØÜØNŒÍ\È[‹Y\ÝšX][Û‹X\ÈËMˆZ\ˆ›ÝÜË]˜[X]\È‹LÌˆ[Ý]Ú[‹Y\ÝšX][Ûˆ˜Z[‹Ý\ÝZ\œË[™™XÛÜ™ÈX^˜Z[‹Ý\ÝK\ØÛÜ™BˆŽNLØÚ]\™Ù]]š[Û][™ÈZ\œÈ[ˆHÛÛ\[š[Ûˆ]Y]‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]È\Y˜XÝÈ™[[Ý™HH›Ú™XÝ[Û‹[Û›Bˆ[XšYÝZ]H›ÜˆHÛÛ\]Y™\Z\™YÝXœÙ]Ú[H™\Ù\š[™È˜[ÙKXÛZ[BˆØY™]NˆHØ[›ÛšXØ[ÛÝ]\È[˜Ú[™ÙYHÛÝ\˜ÙHÚYÛ˜[\ÈÝ[Ø\Yˆ]LÍÌˆÝYÙYÛÛÜ™[˜]\ËWØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆ^XÚ]ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMNLNŒŽVˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÍ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÙ[XÝY[ÝÝ[\ÈL›ÝÜË\›Z[˜[XÚ\Ú[ÛœËˆ[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÈXÝ]™K\Ú]K\ÛÝ\˜ÙH›ØÚÙ\œËLˆœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËÈ™\™\Ù[][Û‹XÛÛ›ÛˆÝXš[]KXÚ[™ÙH›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\Ë›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™HÜ]ˆ™\Z\ˆ[›š[™Ë]›Ý›ÜˆH[Ü]ˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÜ]Ü™\Z\—Ü[—ÌLšœÛÛ˜ÚXÚÛÛœÝ[Y\ÂˆH\™Ù]Y˜Z[\™H]Y][™Ù\]Y[˜ÙHÛÝ]ˆHØœÙ\™Y›ØÚÚ[™ÈZ\‚ˆWØÜØNŒÌØØWØÜØNŒÍ\ÈÛ™HÛÛœÙ\˜]]™H™]šY]Ë[Û›H™\Z\ˆØ[™Y]N‚ˆ[Ý™H[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒÍÈ[‹Y\ÝšX][Ûˆ™Y›Ü™H™YÙ[™\˜][™ÂˆÙ\]Y[˜ÙKZÛÝ]Y]šXÜËˆH›Ú™XÝY[[Ý]ÛÝ[\ÈLÍK[ˆ[[Ý][‹\ØÛÜH›ÝÜÈ™[XZ[ˆ[Ý][™ØœÙ\™Y›ØÚÚ[™ÈZ\œÈ[ˆBˆÝ\YYÚYÛ˜[›Ú™XÝÈY\ˆ™\Z\‹ˆHÛÛ\[š[Ûˆ›Ú™XÝ[Ûˆ\Y˜XÝˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÜ]Ü™\Z\—Ü›Ú™XÝ[Û—ÌLšœÛÛ˜\Y\Âˆ][Ý™HÛ›H[ˆY[[ÜžHÝ™\ˆH^[™YL›ÛÙYZÈ›ÝÜÎˆÛÝ\˜ÙBˆ˜Z[‹Ý\Ýš[Û][ÛœÈ›Üœ›ÛHÈ[™X^˜Z[‹Ý\ÝK\ØÛÜ™H›ÜÂˆœ›ÛHÍLMXÈŽNLØˆHØ[™Y]H™\Z\™YÙ\]Y[˜ÙHÛÝ]ˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]ÜÜ]Ü™\Z\—ØØ[™Y]WÌLšœÛÛ˜ˆ\Y\ÈH[Ý™HÈHÛÜNˆLÍH[[Ý]›ÝÜË[[Ý][‹\ØÛÜH›ÝÜËˆ[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœË[™›È™[XZ[š[™È[[Ý]ˆÝ™\›\Ú]H[Ý™Y[\Ù\\ÌÌ›WØÜØNŒÍÛ\Ý\‹‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]È[ˆ™]™[ÈH^XÝ›ÛÙYZÈ\™Ù]ˆš[Û][Ûˆœ›ÛHÝ^Z[™È\È[ˆYÙÜ™YØ]H›ØÚÙ\ˆÚ[H™\Ù\š[™È˜[ÙKXÛZ[BˆØY™]NˆH™\Z\™YÛÝ]\ÈHØ[™Y]HÛÜHÛ›KÝÛœÝ™X[H\Y˜XÝÂˆ\™H›Ý™XZ[œ›ÛH]HÛÝ\˜ÙH›ÛÙYZÈÚYÛ˜[™[XZ[œÈ\X[Bˆ[˜Ø\Y›ÛÙYZÈÜ]™[XZ[œÈ[˜ÛÛ\]Y[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMMÎL–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÌÍ˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈYÈÛX[ˆÛÝ[X›HX™[Ë[™ˆHÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚ˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[H]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ™]šY]Ë[Û›H™\™\Ù[][Ûˆ™\Z\ŽÈ›Âˆ›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[Ø[™Y]\Ëˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™\™\Ù[][Û—ØYYXØ][Û—ÌLKšœÛÛ˜ˆ[™™Yœ™\ÚY\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÝXØÙ\Ü×ØÜš]\šXWÌLKšœÛÛ˜‚ˆH[ÝÝ[\ÈLÙ[XÝY›ÝÜË\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYBˆ›ÝÜËÛÝ[X›HØ[™Y]\ËÈXÝ]™K\Ú]K\ÛÝ\˜ÙH›ØÚÙ\œËLœ›ØY\‚ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œË]HÙ[™\šXÂˆ™\™\Ù[][Û‹XÛÛ›ÛÝ\™˜XÙH\È›ÝÈÈÝX›H™]šY]Ë[Û›H›ÝÜËˆ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]Ë[™È[œ™\ÛÛ™YÝXš[]KXÚ[™ÙBˆ™]šY]È›ÝÜË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\Ë›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™H\™Ù]ˆ˜Z[\™H]šY[˜ÙH]›Ý›ÜˆH[Ü]ˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÝ\™Ù]Ù˜Z[\™WØ]Y]ÌLšœÛÛ˜ÚXÚÚÝÜÂˆHÝ\œ™[Ù\]Y[˜ÙKZÛÝ]Ü][™XYHš[Û]\ÈHØ\™Ù]šXBˆÛ™H[š\]YH˜Z[‹Ý\ÝÝXÝ\™HZ\‹WØÜØNŒÌØØWØÜØNŒÍˆ
ŽŒRÍXØŽŒSTX
KX^Z\ˆK\ØÛÜ™HÍLMXXÜ›ÜÜÈÚZ[‹[]™[ˆš[Û][™È›ÝÜËˆH[K\ØÛÜ™HÛÝ]ÛZ[H™[XZ[œÈ˜[ÙK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]È›ÛÙYZÈ]Y]\›œÈHYÙÜ™YØ]Bˆ^[™YLX^K\ØÛÜ™H[È^XÝ›ØÚÚ[™Ë\Z\ˆ]šY[˜ÙKÛÈ^[™[™ÈBˆØ\Y[ˆ[Û™HØ[››Ý™HZ\ÝZÙ[ˆ›ÜˆH\ÜÈ]ˆHÙ[XÝY\[Ýˆ™\™\Ù[][ÛˆYYXØ][Ûˆ[ÛÈ™[[Ý™\ÈÝ[HÙ[™\šXÈ™\™\Ù[][Û‹\›ØÙ\ÜÂˆ[XšYÝZ]HÚ[H™\Ù\š[™È™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›HØY™YÝX\™È[™HLBˆØXÚK[Z\ÜÈ›ØÚÙ\‹‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMMŽLŒ–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÌÍX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈÝ[YÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™Ëˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆH[ÝÝXØÙ\ÜÈ\Y˜XÝÝ[™\ÜÈLÙ[XÝY›ÝÜËˆ\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÂˆXÝ]™K\Ú]K\ÛÝ\˜ÙH›ØÚÙ\œËLœ›ØY\‹Y\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËBˆ™\™\Ù[][Û‹XÛÛ›Û›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\Ë›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™H›ØÚÙ\‚ˆ˜\œ›ÝÚ[™È]›Ý›ÜˆH[Ü]ˆ\È[ˆÛÛ\]Yˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÙ^[™YLšœÛÛ˜œ›ÛHBˆ[[X]\šX[^˜X›HÚYXØ\ˆ\Ú[™È›ÛÙYZÈLŽMXÙÌØˆLÝYÙYˆÛÛÜ™[˜]\ËËMˆX\YZ\ˆ›ÝÜËËÌMÈ[Ý]Ú[‹Y\ÝšX][Û‚ˆ˜Z[‹Ý\ÝZ\œËX^ØœÙ\™Y˜Z[‹Ý\ÝHØÛÜ™HÍLMX[›X\Y˜]Âˆ˜[Y\Ë[™ÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆHØ\™Ù]\ÈÝ[›ÝˆXÚY]™YMÌˆÝYÙYÛÛÜ™[˜]\È™[XZ[ˆ[˜ÛÛ\]Y[™ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YÝ^\È˜[ÙK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]È^[™YL\Y˜XÝ[™™YÜ™\ÜÚ[Û‚ˆÛÝ™\˜YÙHXZÙHH]\Ý›ÛÙYZÈ]šY[˜ÙH\˜X›HÚ[H™\Ù\š[™Âˆ˜[ÙKY[XÛZ[H›ØÚÙ\œÎˆØ\X\YYÛÝ™\˜YÙH\È\X[ÛÂˆÙ[XÝY\ÝXÝ\™HÛÛÜ™[˜]H^Û\Ú[ÛœÈ™[XZ[ˆ
WØÜØNŒÍÌ˜WØÜØNLX
Kˆ[™HZ[\ˆÝ[[Z]ÈHÚYÛ˜[˜]\ˆ[ˆH\ÝY[K\ØÛÜ™BˆÜ]‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMMNMˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÌÍ[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈÝ[YÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™Ëˆ›ÈKPÔÐK[Û›H˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]™]ÈÛÝ\˜ÙK\ØØ[Bˆ]šY[˜ÙK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\Ü[™›È™]ÈÛÝ[X›H^\›˜[ˆØ[™Y]\ËˆHÝ\œ™[[ÝÝXØÙ\ÜÈ\Y˜XÝÝ[™\ÜÈLÙ[XÝYˆ›ÝÜË\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÂˆXÝ]™K\Ú]K\ÛÝ\˜ÙH›ØÚÙ\œËLœ›ØY\‹Y\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËBˆ™\™\Ù[][Û‹XÛÛ›Û›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\Ë›Üˆ\™XÝ›ÛÙYZËÕK\ØÛÜ™H›ØÚÙ\‚ˆ˜\œ›ÝÚ[™È]›Ý›ÜˆH[Ü]ˆ\È[ˆÛÛ\]Yˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÙ^[™YšœÛÛ˜œ›ÛHBˆ[[X]\šX[^˜X›HÚYXØ\ˆ\Ú[™È›ÛÙYZÈLŽMXÙÌØˆÝYÙYˆÛÛÜ™[˜]\ËNNLHX\YZ\ˆ›ÝÜËKˆ[Ý]Ú[‹Y\ÝšX][Ûˆ˜Z[‹Ý\ÝˆZ\œËX^ØœÙ\™Y˜Z[‹Ý\ÝHØÛÜ™HÍLMX[›X\Y˜]È˜[Y\Ë[™ˆÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆHØ\™Ù]\ÈÝ[›ÝXÚY]™YNL‚ˆÝYÙYÛÛÜ™[˜]\È™[XZ[ˆ[˜ÛÛ\]Y[™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YˆÝ^\È˜[ÙK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH™]È^[™Y\Y˜XÝ[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙBˆXZÙHH]\Ý›ÛÙYZÈ]šY[˜ÙH\˜X›HÚ[H™\Ù\š[™È˜[ÙKY[XÛZ[Bˆ›ØÚÙ\œÎˆØ\X\YYÛÝ™\˜YÙH\È\X[ÛÈÙ[XÝY\ÝXÝ\™HÛÛÜ™[˜]Bˆ^Û\Ú[ÛœÈ™[XZ[ˆ
WØÜØNŒÍÌ˜WØÜØNLX
K[™HZ[\ˆÝ[[Z]ÈBˆÚYÛ˜[˜]\ˆ[ˆH\ÝY[K\ØÛÜ™HÜ]‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMMŽL–ˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÌÌ˜[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHXØÙ\YÛÝ[X›HÛXÙH™[XZ[œÈKÚ]ˆÎHØ[›ÛšXØ[X™[ËHKH™]šY]ÈÝ[YÈÛX[ˆÛÝ[X›HX™[Ëˆ[™HÛÝ\˜ÙK\ØØ[H]Y]™[XZ[œÈØ\Y]KÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™Ëˆ›È™]ÈKPÔÐH˜[˜ÚHÚÝ[™HÜ[™YÚ]Ý]HÛÝ\˜ÙK\ØØ[H]Y]ˆÚÝÚ[™È™]È\ØX›HKPÔÐH™XÛÜ™Ë‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ™\Z\ˆ]šY[˜ÙH[™[Ý™XY[™\ÜÂˆYš[š][ÛŽÈ›È›Üˆ[\Üˆ\È[ˆYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÝXØÙ\Ü×ØÜš]\šXWÌLKšœÛÛ˜ÚXÚXZÙ\Âˆ[ÝÝXØÙ\ÜÈYX\Ý\˜X›HXÜ›ÜÜÈØ[™Y]HÛÝ[\›Z[˜[XÚ\Ú[ÛœËˆXÝ]™K\Ú]HÛÝ\˜ÙH™\ÛÛ][Û‹œ›ØY\ˆ\XØ]HØÜ™Y[š[™Ë™\™\Ù[][Û‚ˆYYXØ][Û‹™]šY]ÈXÚ\Ú[ÛœË[X™[Y˜XÝÜžHØ]\Ë[\Ü\™XYH›ÝÜËˆ[™ÛÝ[X›K[X™[Ø[™Y]\ËˆÝ\œ™[Ý]\È\È™YY×Û[Ü™WÝÛÜšØˆLˆÙ[XÝY›ÝÜË\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÛÝ[X›BˆØ[™Y]\ËÈ^XÚ]XÝ]™K\Ú]H›ÝÜËÈš[™[™ËXÛÛ^[Û›HXÝ]™K\Ú]Bˆ›ÝÜËœ›ØY\ˆ\XØ]HØÜ™Y[š[™È[™[X™[Y˜XÝÜžHØ]\È[œ™\ÛÛ™Y›Ü‚ˆ[L[™™\™\Ù[][Û‹XÛÛ›Û›ØÚÙ\œÈÛˆH›ÝÜË‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\Ë›Üˆ›ÛÙYZÈ›ØÚÙ\ˆÛ\šYšXØ][Ûˆ]ˆ›Ý›ÜˆH™]È[Ü]ˆH™X[S\Ù\\ÌˆÙ\]Y[˜ÙKY\Ý[˜ÙHÛÝ]È™[XZ[‚ˆHXØÙ\YÙ\]Y[˜ÙH]šY[˜ÙKˆH[[X]\šX[^˜X›H›ÛÙYZÈ™XY[™\ÜÂˆ\Y˜XÝ›ÝÈ^XÚ]H^ÛY\ÈWØÜØNŒÍÌ˜[™WØÜØNLXœ›ÛHÛÛÜ™[˜]BˆX]\šX[^˜][Ûˆ™XØ]\ÙH›Ý]™HÙ[ÛY]žWÜÝ]\Ï[›×ÜÝXÝ\™WÜÜÚ][ÛœØˆ[™Ù[XÝYÜÝXÝ\™WÚY[[[ˆÝ\œ™[]šY[˜ÙKˆ›ÛÙYZËÕK\ØÛÜ™Bˆ™[XZ[œÈ\X[ˆ^[™YŒÝ[\ÈX^˜Z[‹Ý\ÝHØÛÜ™HÍLMXˆZ\ÜÙ\ÈHØ\™Ù]X]™\ÈŒLˆÝYÙYÛÛÜ™[˜]\È[˜ÛÛ\]Y[™ˆØ[››ÝÛZ[HH[K\ØÛÜ™HÛÝ]‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆH^\›˜[[Ý›ÈÛ™Ù\ˆ™X]È]šY[˜ÙBˆXÚÙ]ÛÛ\][Ûˆ\È[ˆ[\XÚ]ÝXØÙ\ÜÈÛÛ™][ÛŽÈHÝXØÙ\ÜÈÜš]\šXH›ÝÂˆ^XÚ]H\Ý[™ÝZ\ÚÜ\˜][Û˜[ÝXØÙ\ÜËØÚY[YšXËÚ[\ÜÝXØÙ\ÜËˆ™YYË[[Ü™K]ÛÜšÈÝ]\Ë›ØÙ\ÜË[Z\ÜÚ[™È˜Z[\™\Ë[™]šY[˜ÙKY^Z[™Yˆ™\›Ë\\ÜÈÝ]ÛÛY\ÈÚ[HÙY\[™È[Ý]]È™]šY]Ë[Û›H[™›Û‹XÛÝ[X›K‚ˆH›ÛÙYZÈ™XY[™\ÜÈ][ÛÈ›ÈÛ™Ù\ˆX]™\ÈHÛÈ[›X]\šX[^˜X›BˆÙ[XÝY\ÝXÝ\™H›ÝÜÈ[XšYÝ[Ý\Îˆ^H\™H^XÚ]ÛÛÜ™[˜]H^Û\Ú[ÛœÂˆÚ]]šY[˜ÙK‚‚”™XÛÜ™Y›ÜˆHŒ‹LKLMLÎNŒNVˆ[ˆY\ˆÛX[ˆÝ\\Ø]\ÂŠÌÌX[š]\ÝÈ\ÜÙY[™˜[Y]X\ÜÙY
N‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHKH™]šY]ÈÝ[YÈXØÙ\YÛX[‚ˆX™[ËÛÝ\˜ÙK\ØØ[H\ÈØ\Y]KÈØœÙ\™YKPÔÐH™XÛÜ™Ë[™Ý\œ™[ˆ\™[™YØ]]™K˜[ÙK[›Û‹XXœÝ[[Û‹™X\‹[Z\ÜË[™XÝ[Û˜X›KY˜Z[\™HÚXÚÜÂˆ™[XZ[ˆÛX[ˆ]È›ÝÜ™X]H[Ü™HKPÔÐHÛÝ\˜ÙHXY›ÛÛK‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\Üˆ›È›Üˆ[\ÜÈY\ÈÛ›H›Üˆ™]šY]Ë[Û›H™\Z\‚ˆ]šY[˜ÙKˆ˜XÚÙ[™Ý\œ™[\™Y™\™[˜ÙHS\Ù\\ÌˆÙX\˜ÚX\ÈÛX\™Y›ÜˆBˆŽ›Ë\ÚYÛ˜[^\›˜[›ÝÜË]ˆ^XÝÙ\]Y[˜ÙHÛÝ]ËÈÙ[XÝY\[Ýˆš[™[™ËXÛÛ^[Û›HXÝ]™K\Ú]H›ÝÜËœ›ØY\ˆ\XØ]HØÜ™Y[š[™Ëˆ™\™\Ù[][Û‹\™]šY]ÈX^\\™]šY]È›ËYXÚ\Ú[Ûˆ\Y˜XÝË[™[ˆ˜XÝÜžHØ]\ÈÝ[›ØÚÈ]™\žH^\›˜[›ÝÈœ›ÛH[\Ü‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\ËˆHXØÙ\Y\™YÚ\ÝžHK[™KBˆS\Ù\\ÌˆÛÝ]È\™H™X[˜XÚÙ[™]šY[˜ÙNˆÛÜÚÛYXœ™]ËØš[‹Û[\Ù\\Øˆ™\œÚ[ÛˆNNØÍXØÌÎÙ\]Y[˜ÙH™XÛÜ™ËÎÍÎ]˜[X]Y›ÝÜÈÚ]ˆÙ\]Y[˜ÙHÛÝ™\˜YÙKÌ	HY[]H[™	HÛÝ™\˜YÙHÛ\Ý\š[™ËLÍˆ[[Ý]ˆ›ÝÜÈžHÚÛHÛ\Ý\œËX^ØœÙ\™Y˜Z[‹Ý\ÝY[]HŒŽ\™Ù]ˆLÌ	HXÚY]™Y[™[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËˆ\È[‚ˆ\™[™YH\Y˜XÝÈÚ]^XÚ]˜XÚÙ[™™\ÛÛ™Y]ˆÛ\Ý\‹]™\ÚÛ\™Ù]XXÚY]™[Y[[™[Z]][ÛˆY]Y]H[X\Ù\Ë‚ˆ›ÛÙYZÈ™[XZ[œÈXœÙ[œ›ÛHY˜][UÈHš[Üˆ[\Y[ˆ›ÛÙYZÂˆÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[‹Øš[‹Ù›ÛÙYZØ™\œÚ[ÛˆLŽMXÙÌØˆ™[XZ[œÈHØÝ[Y[Y]ˆ\È[ˆYYH›Ý[™Y^[™YŒ›ÛÙYZÂˆÚYÛ˜[œ›ÛHH[[X]\šX[^˜X›HÛÛÜ™[˜]HÚYXØ\ŽˆŒÝYÙYÛÛÜ™[˜]\ËˆL‹ÌŽHX\YZ\ˆ›ÝÜËËÌMˆ[Ý]Ú[‹Y\ÝšX][Ûˆ˜Z[‹Ý\ÝZ\œËX^ˆ˜Z[‹Ý\ÝHØÛÜ™HÍLMX[™ÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆH\X[ˆÚYÛ˜[™[[Ý™\ÈH^[™YÙZ[[™Ë]HØ\™Ù]\È›ÝXÚY]™YˆÛˆHÛÛ\]YÝXœÙ][™[›ÛÙYZËÕK\ØÛÜ™HÜ]™[XZ[œÈ›ØÚÙYžBˆWØÜØNŒÍÌ˜WØÜØNLXHŒLˆØ\Y[Ý]ÝYÙYÛÛÜ™[˜]\Ë[™Bˆ[œ[ˆ[Ü]Z[\‹‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\ËˆÙ\]Y[˜ÙHÛÝ]Y]Y]H\È›ÝÈ\ÜÈœš]H›Ü‚ˆÝÛœÝ™X[HØ]\È[™™]šY]Ù\œÈÚ[H™\Ù\š[™ÈH›ÞH˜[˜XÚÈ][™ˆ[›™Y™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙKˆ^\Ý[™È^\›˜[\Y˜XÝ[™XYÙKˆ™]šY]Ë[Û›H]Y]Ë[™›ÛÙYZÈ˜[ÙKY[XÛZ[H›ØÚÙ\œÈ™[XZ[ˆ[ˆ›Ü˜ÙK‚‚ˆÈÈ™XÙ[›Ú™XÝ›ÙÜ™\ÜÂ‚‹HYYYÙÜ™YØ]KY›ÛÙYZË]K\ØÛÜ™K\]Y\žKXÚ[šÜØ\Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ØYÙÜ™YØ]WÌÌ—ÛÙ—ÌM‹šœÛÛ˜‚ˆHYÙÜ™YØ]HÛÛœÝ[Y\ÈÚ[šÜÈL‹ÙY\ÈH[YY[Ý]Ú[šÈˆš\ÚX›K[™ˆ™XÛÜ™ÈÈ][\YÚ[šÜËˆÛÛ\]YÚ[šÜËÛÛ\]Y]Y\žBˆÛÛÜ™[˜]\ËŽLHX\YZ\ˆ›ÝÜËKMˆ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝˆK\ØÛÜ™HŽMMØÌ\™Ù]]š[Û][™È›ÝË[]™[Z\œËLÈ™\ÜYˆš[Û][™ÈÝXÝ\™HZ\œË[™M›Û‹XÛÛ\]YÚ[šÜËˆ]\È™]šY]Ë[Û›Kˆ›Û‹XÛÝ[X›K›Ý[\Ü\™XYK[™ÙY\Âˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹HYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×Ì—ÛÙ—ÌM‹šœÛÛ˜‚ˆÚ[šÈˆ\Ù\ÈHØ[YH[]\™Ù]]Y\žKXÚ[šÈÛÛ[X[™Ú\H\ÈÚ[šÜÈLBˆ][Y\ÈÝ]Y\ˆLÙXÛÛ™È™Y›Ü™HZ\ˆ›ÝÜÈ\™H[Z]Yˆ\È\ÈBˆÛÛ˜Ü™]H[[YH›ØÚÙ\ˆ›Üˆ]]Y\žH˜[™ÙK›ÝH˜Z[Y˜[Y][ÛˆØ]Bˆ[™›ÝH[K\ØÛÜ™HÚYÛ˜[‚‹HYYZ[Y›ÛÙYZË]K\ØÛÜ™K\]Y\žKXÚ[šË\ÚYÛ˜[H™\Ý[XX›H›ÛÙYZÂˆ]Y\žKXÚ[šÈÛÛ[X[™]ÙX\˜Ú\ÈH]\›Z[š\ÝXÈ]Y\žHÛXÙHYØZ[œÝ[ˆÝYÙYX]\šX[^˜X›H\™Ù]ÛÛÜ™[˜]\È[™ÙY\ÈÛÛ\XÝÝ[[X\žH]šY[˜ÙK‚ˆHš\œÝ\™XÝÚ[šÈ\Y˜XÝËˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ÌÛÙ—ÌM‹šœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÜ]Y\žWØÚ[š×ÌWÛÙ—ÌM‹šœÛÛ˜ˆ\ÙHH™\Z\™YØ[™Y]H™XY[™\ÜÈ\Y˜XÝÝ[]Y\žHÛÛÜ™[˜]\Ëˆ[ÌˆÝYÙY\™Ù]Ë›ÛÙYZÈLŽMXÙÌØK]™XYÈ[™BˆL\ÙXÛÛ™[Y[Ý]\ˆÚ[šËˆ^HÛÛ\]YÚ]ŽLHX\YZ\ˆ›ÝÜËˆKMˆ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HŽMMØ[™ÌÝ[ˆ\™Ù]]š[Û][™È›ÝË[]™[Z\œËˆ\È™[[Ý™\ÈH[X][Û˜ÙK[Û›H[[YBˆÔÑ‹][]Y\žHYÙÜ™YØ][Ûˆ\È[˜ÛÛ\]H[™›ÝÚ[šÜÈ›ÝÈ›Ý™HBˆ™\Z\™YÜ]Ý[˜Z[ÈHØ\™Ù]™^[Û™H^[™YLØ\‚‹HYYZ[Y›ÛÙYZË]K\ØÛÜ™KX[[X]\šX[^˜X›K\ÚYÛ˜[HÛÛ\XÝˆ[[X]\šX[^˜X›H›ÛÙYZÈÝ[[X\žHÛÛ[X[™]™XÛÜ™ÈÛÛ[X[™Ý™\œÚ[Û‹ˆÛÛÜ™[˜]HÛÝ™\˜YÙKÛÛÜ™[˜]H^Û\Ú[ÛœËX\Y\Z\ˆÛÝ[Ë\™Ù]Ý]\ËˆÜ˜Z[‹Ý\ÝZ\œË[™›ØÚÚ[™ÈZ\œÈÚ]Ý]ÛÛ[Z][™È]™\žH›ÛÙYZÂˆZ\ˆ›ÝËˆHš\œÝ\™XÝ[ˆÜ›ÝBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WØ[ÛX]\šX[^˜X›KšœÛÛ˜ˆœ›ÛHH™\Z\™YØ[™Y]H™XY[™\ÜÈ\Y˜XÝˆH]\ÝÝYÙYÚYÛ˜[›ÝÂˆÛÝ™\œÈ[ÌˆÝYÙYX]\šX[^˜X›HÛÛÜ™[˜]\ÈÚ]›ÛÙYZÈLŽMXÙÌØˆ[™K]™XYÈX\ÈML‹LŒˆZ\ˆ›ÝÜÈ[™ÍH˜Z[‹Ý\Ý›ÝÜË[™ˆ˜Z[ÈHØ\™Ù]]X^˜Z[‹Ý\ÝK\ØÛÜ™HŽMÍXÚ]ÌMBˆ\™Ù]]š[Û][™È˜Z[‹Ý\Ý›ÝÜËˆ]ÙY\ÈWØÜØNŒÍÌ˜ØWØÜØNLX\ÈBˆÛÛÜ™[˜]H^Û\Ú[ÛœÈ[™™\Ù\™\ÈÛÝ[X›KÚ[\Ü\™XYH›ÝÜÈÚ]ˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹HYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLÜÜ]Ü™\Z\—ØØ[™Y]KšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÙ^[™YLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÝ\™Ù]Ù˜Z[\™WØ]Y]ÌLÜÜ]Ü™\Z\—ØØ[™Y]WÙ^[™YLšœÛÛ˜‚ˆHÛÛÜ™[˜]K\™XY[™\ÜÈ\Y˜XÝÛÛœÝ[Y\ÈHØ[™Y]HÙ\]Y[˜ÙHÛÝ][™ˆ[Ý™\ÈWØÜØNŒÍÈ[‹Y\ÝšX][ÛˆÚ[HÙY\[™ÈÌˆX]\šX[^™YˆÛÛÜ™[˜]\È[™HÛÈÛÛÜ™[˜]H^Û\Ú[ÛœËˆHXÝX[›ÛÙYZÈ™\[ˆ\Ù\ÂˆHØ[YHLXÛÛÜ™[˜]HØ\\È^[™YL[™\ˆH™\Z\™Y\][ÛŽ‚ˆËMˆX\YZ\ˆ›ÝÜË‹LÌ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™BˆŽNLØ[™\™Ù]]š[Û][™ÈZ\œËˆ\È™[[Ý™\ÈH›Ú™XÝ[Û‹[Û›Bˆ›ØÚÙ\ˆ›ÜˆHÛÛ\]YÝXœÙ]]HØ[›ÛšXØ[ÛÝ]\È[˜Ú[™ÙY[™Bˆ[[[X]\šX[^˜X›HÜ]™[XZ[œÈ[˜ÛÛ\]Y‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÜ]Ü™\Z\—Ü[—ÌLšœÛÛ˜\ÈÓBˆ[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙKˆH[ˆÛÛœÝ[Y\ÈH\™Ù]Y˜Z[\™H]Y][™ˆÙ\]Y[˜ÙHÛÝ]˜[Y\ÈWØÜØNŒÍ\ÈHÛ›H[[Ý]›ÝÈ]]\Ý[Ý™HÂˆ™\Z\ˆHØœÙ\™YWØÜØNŒÌØØWØÜØNŒÍK\ØÛÜ™HÜ]š[Û][Û‹[™ˆ™XÛÜ™È]H[Ý™H™\Ù\™\È[[[Ý][‹\ØÛÜH›ÝÜÈÚ[H™YXÚ[™Âˆ›Ú™XÝY[[Ý]ÛÝ[œ›ÛHLÍˆÈLÍKˆ]ÙY\ÈH™\Z\ˆ[˜\YYˆ™]šY]Ë[Û›K›Û‹XÛÝ[X›K[™›Ý[\Ü\™XYNÈH[[[X]\šX[^˜X›Bˆ›ÛÙYZÈÜ]™[XZ[œÈ[˜ÛÛ\]Y[™›È[ÛÝ]ÛZ[H\È\›Z]Y‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÜ]Ü™\Z\—Ü›Ú™XÝ[Û—ÌLšœÛÛ˜‚ˆ\È›Ú™XÝ[Ûˆ\Y\ÈH›ÜÜÙYWØÜØNŒÍ[Ý™HÛ›HÈ^\Ý[™Âˆ^[™YL›ÛÙYZÈZ\ˆ›ÝÜË™YXÚ[™ÈÛÝ\˜ÙH˜Z[‹Ý\Ýš[Û][ÛœÈœ›ÛHˆÈ[™›Ú™XÝYX^˜Z[‹Ý\ÝK\ØÛÜ™Hœ›ÛHÍLMXÈŽNLØ‚ˆ™XØ]\ÙHHÙ\]Y[˜ÙHÛÝ][™ÝÛœÝ™X[HY]šXÜÈ\™H›Ý™YÙ[™\˜]Y[™ˆMÌˆÝYÙYÛÛÜ™[˜]\È™[XZ[ˆ[˜ÛÛ\]YH›Ú™XÝ[Ûˆ™[XZ[œÈ™]šY]Ë[Û›Bˆ[™›Û‹XÛZ[Z[™Ë‚‹HYY\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]ÜÜ]Ü™\Z\—ØØ[™Y]WÌLšœÛÛ˜‚ˆ\ÈØ[™Y]H\Y\ÈH™\Z\ˆÈHÛÜHÙˆHÙ\]Y[˜ÙHÛÝ][Ý™\ÂˆWØÜØNŒÍœ›ÛH[[Ý]È[‹Y\ÝšX][Û‹™\Ù\™\È[[[Ý]ˆ[‹\ØÛÜH›ÝÜËÙY\È[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ][™ˆ™XÛÜ™È›È™[XZ[š[™È[[Ý]Ý™\›\Ú]H[Ý™YS\Ù\\ÌˆÛ\Ý\‹ˆ]\Âˆ›ÝØ[›ÛšXØ[[™ÝÛœÝ™X[H\Y˜XÝÈ]™H›Ý™Y[ˆ™XZ[œ›ÛH]‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÝ\™Ù]Ù˜Z[\™WØ]Y]ÌLšœÛÛ˜\ÂˆÓH[™™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙKˆH]Y]ÛÛœÝ[Y\ÈH^[™YL›ÛÙYZÂˆÚYÛ˜[[™Y[YšY\ÈH^XÝÝ\œ™[\Ü]\™Ù]›ØÚÙ\ŽˆÛ™H[š\]YBˆ˜Z[‹Ý\ÝÝXÝ\™HZ\‹WØÜØNŒÌØØWØÜØNŒÍ
ŽŒRÍXØŽŒSTX
Kˆ™XXÚ\ÈX^Z\ˆK\ØÛÜ™HÍLMXXÜ›ÜÜÈÚZ[‹[]™[š[Û][™È›ÝÜË‚ˆ\ÈÙY\È[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX[™Ú[™Ù\ÈH™^ˆ›ÛÙYZÈÛÜšÈœ›ÛHšÙY\[˜Ü™X\Ú[™ÈØ\YÛÝ™\˜YÙHˆÈÜ]ˆ™\Z\‹Ù^Û\Ú[Ûˆ™]šY]È\È[žH]\ˆ[\ÚYÛ˜[ÛÛ™š\›X][Û‹‚‹HYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™\™\Ù[][Û—ØYYXØ][Û—ÌLKšœÛÛ˜ˆ[™™Yœ™\ÚYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÝXØÙ\Ü×ØÜš]\šXWÌLKšœÛÛ˜ˆBˆÙ[XÝY\[Ý™\™\Ù[][ÛˆÝ\™˜XÙH\È›ÝÈÛÛ˜Ü™]NˆÈÝX›H™]šY]Ë[Û›BˆÛÛ›ÛË™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]Ë[™ÈÝXš[]KXÚ[™ÙBˆ›ÝÜÈ™\]Z\š[™È™\™\Ù[][Ûˆ™]šY]ËˆHÝXØÙ\ÜÈ\Y˜XÝ™[XZ[œÂˆ™YY×Û[Ü™WÝÛÜšØÚ]\›Z[˜[XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜË[™ˆÛÝ[X›HØ[™Y]\ÎÈœ›ØY\ˆ\XØ]HØÜ™Y[š[™È[™[X™[Y˜XÝÜžBˆØ]\ÈÝ[›ØÚÈ[LÙ[XÝY›ÝÜË‚‹HÛÛ\]YH\™XÝ›Ý[™Y^[™YL›ÛÙYZËÕK\ØÛÜ™HÚYÛ˜[œ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØ[ÛX]\šX[^˜X›KšœÛÛ˜‚ˆHÛÛ[X[™\ÙYÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[‹Øš[‹Ù›ÛÙYZØ™\œÚ[Û‚ˆLŽMXÙÌØK[X^\ÝYÙYXÛÛÜ™[˜]\ÈL[™ˆK\š[Ü‹\ÝYÙYXÛÛÜ™[˜]KXÛÝ[ˆH™]Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÙ^[™YLšœÛÛ˜™XÛÜ™ÈËM‚ˆX\YZ\ˆ›ÝÜËÎ[Ý]Z\ˆ›ÝÜËËÌMÈ[Ý]Ú[‹Y\ÝšX][Û‚ˆ˜Z[‹Ý\Ý›ÝÜËNKÎÈ[‹Y\ÝšX][ÛˆZ\ˆ›ÝÜËX^ØœÙ\™Y˜Z[‹Ý\ÝBˆØÛÜ™HÍLMX[›X\Y˜]È›ÛÙYZÈ˜[Y\Ë[™^XÚ]ˆÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆ]™[[Ý™\ÈH^[™Y\X[\ÚYÛ˜[ÙZ[[™ÂˆÛ›Kˆ]™[XZ[œÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›H™XØ]\ÙHHØ\™Ù]˜Z[ÈÛ‚ˆHÛÛ\]YÝXœÙ]HØ\X]™\ÈMÌˆÝYÙYÛÛÜ™[˜]\È[˜ÛÛ\]Y[™ˆWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX\È[ÝWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙXˆ™[XZ[ˆYK‚‹HÛÛ\]YH\™XÝ›Ý[™Y^[™Y›ÛÙYZËÕK\ØÛÜ™HÚYÛ˜[œ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØ[ÛX]\šX[^˜X›KšœÛÛ˜‚ˆHÛÛ[X[™\ÙYÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[‹Øš[‹Ù›ÛÙYZØ™\œÚ[Û‚ˆLŽMXÙÌØK[X^\ÝYÙYXÛÛÜ™[˜]\È[™ˆK\š[Ü‹\ÝYÙYXÛÛÜ™[˜]KXÛÝ[ŒÈ[[YHØ\ÈKŒÌˆÙXÛÛ™ËˆH™]Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÙ^[™YšœÛÛ˜™XÛÜ™ÈNNLBˆX\YZ\ˆ›ÝÜËÈ[Ý]Z\ˆ›ÝÜËKˆ[Ý]Ú[‹Y\ÝšX][Û‚ˆ˜Z[‹Ý\Ý›ÝÜËL‹N[‹Y\ÝšX][ÛˆZ\ˆ›ÝÜËX^ØœÙ\™Y˜Z[‹Ý\ÝBˆØÛÜ™HÍLMX[›X\Y˜]È›ÛÙYZÈ˜[Y\Ë[™^XÚ]ˆÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆ]™[[Ý™\ÈH^[™YŒ\X[\ÚYÛ˜[ÙZ[[™ÂˆÛ›Kˆ]™[XZ[œÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›H™XØ]\ÙHHØ\™Ù]˜Z[ÈÛ‚ˆHÛÛ\]YÝXœÙ]HØ\X]™\ÈNLˆÝYÙYÛÛÜ™[˜]\È[˜ÛÛ\]Y[™ˆWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX\È[ÝWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙXˆ™[XZ[ˆYK‚‹HYY^XÚ]^\›˜[[ÝÝXØÙ\ÜÈÜš]\šXH[‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜÝXØÙ\Ü×ØÜš]\šXWÌLKšœÛÛ˜\ÈÓKˆ™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙK[™ØÜËˆH\Y˜XÝÙY\È[›ÝÜÈ™]šY]Ë[Û›H[™ˆ™XÛÜ™È[ÝÜÝ]\Ï[™YY×Û[Ü™WÝÛÜšØˆLÙ[XÝYØ[™Y]\Ë\›Z[˜[ˆXÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÈ^XÚ]ˆXÝ]™K\Ú]K\ÛÝ\˜ÙH›ÝÜËÈš[™[™ËXÛÛ^[Û›H›ÝÜËœ›ØY\ˆ\XØ]BˆØÜ™Y[š[™È[™[X™[Y˜XÝÜžHØ]\È[œ™\ÛÛ™Y›Üˆ[L[™Bˆ™\™\Ù[][Û‹XÛÛ›Û[œ™\ÛÛ™Y›ÝÜËˆ\È™[[Ý™\ÈH^\›˜[\[Ýˆ™]šY[˜ÙH\ÜÙ[X›Y\]X[ÈÝXØÙ\ÜÈˆ[XšYÝZ]HÚ]Ý]]]Üš^š[™È[\Ü‚‹H\™[™YH[[X]\šX[^˜X›H›ÛÙYZÈÛÛÜ™[˜]K\™XY[™\ÜÈ\Y˜XÝÚ]ˆ^XÚ]ÛÛÜ™[˜]H^Û\Ú[ÛœÈ›ÜˆWØÜØNŒÍÌ˜[™WØÜØNLXˆ›Ý›ÝÜÂˆ]™HÙ[ÛY]žWÜÝ]\Ï[›×ÜÝXÝ\™WÜÜÚ][ÛœØÙ[XÝYÜÝXÝ\™WÚY[[ˆ[™Ù[XÝYÜÝXÝ\™WÚÙ^O[Z\ÜÚ[™×ÜÙ[XÝYÜÝXÝ\™X[ˆÝ\œ™[]šY[˜ÙKˆÛÈ^H\™H^ÛYYœ›ÛH›ÛÙYZÈÛÛÜ™[˜]HX]\šX[^˜][Ûˆ˜]\ˆ[‚ˆY\È[XšYÝ[Ý\ÈZ\ÜÚ[™ÈÝXÝ\™\ËˆH\Y˜XÝÝ[ÝYÙ\ÈÌ‚ˆÝ\ÜYÙ[XÝYˆÛÛÜ™[˜]\ÈÚ]™]Ú˜Z[\™\ËÙY\ÈˆÛÝ[X›KÚ[\Ü\™XYH›ÝÜË[™Ù\È›Ý\›Z]H[K\ØÛÜ™HÛÝ]ˆÛZ[K‚‹H\™[™YHXØÙ\Y\™YÚ\ÝžHÙ\]Y[˜ÙKY\Ý[˜ÙHÛÝ]˜XÚÙ[™Y]Y]H›Ü‚ˆHK[™KHÛÛ^ËˆH™YÙ[™\˜]Y\Y˜XÝÈÙY\HØ[YBˆS\Ù\\Ìˆ™\Ý[
NNØÍXØÌÎÙ\]Y[˜ÙH™XÛÜ™ËLÍˆ[[Ý]›ÝÜËX^ˆ˜Z[‹Ý\ÝY[]HŒŽ\™Ù]LÌ	HXÚY]™Y[[Ý]Ý][Ù‹\ØÛÜBˆ˜[ÙH›Û‹XXœÝ[[ÛœÊH[™›ÝÈ^ÜÙH^XÚ]˜XÚÙ[™ˆ˜XÚÙ[™Ü™\ÛÛ™YÜ]Û\Ý\—Ý™\ÚÛ\™Ù]ÚY[]WØXÚY]™Yˆ\™Ù]ÛX^Ý˜Z[—Ý\ÝÚY[]X[™[Z]][ÛœØšY[Ëˆ™YÜ™\ÜÚ[Ûˆ\ÝÂˆ[ˆ›ÝH™X[S\Ù\\Ìˆ][™H›ÞH˜[˜XÚÈY]Y]KˆÛÛÚXÚÂˆ›Ý[™[\Ù\\Ø›\ÝXZÙX›\Ý˜[™X[[Û™ÛˆUÈ›ÛÙYZØˆØ\È›ÝÛˆUÛÈHØÝ[Y[Y[\Y[ˆ›ÛÙYZÈ]™[XZ[œÈ™\]Z\™Y‚‹H›ËXÛÙH[YØ]Y›ÛÙYZÈ][\]Œ‹LKLMLNŽŒÍV‹ˆH\™[ˆ]]ÛX][ÛˆXÜ]Z\™YHØÚËÞ[˜ÙYÜšYÚ[‹ÛXZ[˜™\šYšYY[\Ù\\Øˆ›\ÝXZÙX›\Ý˜[™X[[Û™ÛˆU\È›ÛÙYZÂˆÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[‹Øš[‹Ù›ÛÙYZØ™\œÚ[ÛˆLŽMXÙÌØˆ˜[ˆÌÌH[š]\ÝÈ[™˜[Y][ÛˆÛX[›K[™[œÝXÝYHÛÜšÙ\ˆÈZ[ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØ[ÛX]\šX[^˜X›KšœÛÛ˜œ›ÛBˆH[[X]\šX[^˜X›HÛÛÜ™[˜]HÚYXØ\‹ˆHÛÜšÙ\ˆY›Ý™]\›ˆÚ][‚ˆHÜ˜\]\Ú[™ÝÈ[™Ø\ÈÚ]ÝÛŽÈH\™[ÛÜšÝ™YHÝ^YYÛX[ˆ[™›Âˆ[\[Y[][ÛˆÜˆ\Y˜XÝÚ[™Ù\ÈÙ\™H[YÜ˜]YˆH™^YÙ[ÚÝ[ˆ™]žHH[YØ]Y[[X]\šX[^˜X›H›ÛÙYZËÕK\ØÛÜ™HÚYÛ˜[ÜˆH›Ý[™Yˆ\™Ù\‹][‹MØ\ÙY\[™ÈHÛÈZ\ÜÚ[™ÈÙ[XÝY\ÝXÝ\™H›ØÚÙ\œÂˆ
WØÜØNŒÍÌ˜WØÜØNLX
H[™[™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›HÛZ[\È[XÝ‚‹HÛÛ\]YH›Ý[™Y^[™YŒ›ÛÙYZËÕK\ØÛÜ™HÚYÛ˜[œ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØ[ÛX]\šX[^˜X›KšœÛÛ˜‚ˆHÛÛ[X[™\ÙYÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[‹Øš[‹Ù›ÛÙYZØ™\œÚ[Û‚ˆLŽMXÙÌØK[X^\ÝYÙYXÛÛÜ™[˜]\ÈŒ[™ˆK\š[Ü‹\ÝYÙYXÛÛÜ™[˜]KXÛÝ[È[[YHØ\ÈÍÍËMHÙXÛÛ™ËˆH™]Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÙ^[™YŒšœÛÛ˜™XÛÜ™ÈL‹ÌŽBˆX\YZ\ˆ›ÝÜËMÈ[Ý]Z\ˆ›ÝÜËËÌMˆ[Ý]Ú[‹Y\ÝšX][Û‚ˆ˜Z[‹Ý\Ý›ÝÜËMMˆ[‹Y\ÝšX][ÛˆZ\ˆ›ÝÜËX^ØœÙ\™Y˜Z[‹Ý\ÝBˆØÛÜ™HÍLMX[›X\Y˜]È›ÛÙYZÈ˜[Y\Ë[™^XÚ]ˆÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆ]™[[Ý™\ÈH^[™Y\X[\ÚYÛ˜[ˆÙZ[[™ÈÛ›Kˆ]™[XZ[œÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›H™XØ]\ÙHHØ\™Ù]ˆ˜Z[ÈÛˆHÛÛ\]YÝXœÙ]HØ\X]™\ÈŒLˆÝYÙYÛÛÜ™[˜]\Âˆ[˜ÛÛ\]Y[™WÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX\Âˆ[ÝWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX™[XZ[ˆYK‚‹HÝYÙY[Ý\œ™[HX]\šX[^˜X›HÙ[XÝY›ÛÙYZÈÛÛÜ™[˜]\È›ÜˆBˆXØÙ\YKÛÛ^[‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØ[ÛX]\šX[^˜X›KšœÛÛ˜‚ˆÌˆ[š\]YHÙ[XÝYˆ[PÒQˆÚYXØ\œËÍˆX]\šX[^˜X›H]˜[X]Y›ÝÜËˆ™]Ú˜Z[\™\Ë[™Ý\ÜYÙ[XÝYÝXÝ\™\ÈY[œÝYÙYˆ\Âˆ™[[Ý™\ÈH[œÝYÙYÙ[XÝYXÛÛÜ™[˜]HÚYXØ\ˆ›ØÚÙ\ˆÚ[HÙY\[™ÂˆWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX[™[ÝWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX‚ˆ[K\ØÛÜ™HÜ]ÛÜšÈ™[XZ[œÈ›ØÚÙYžHWØÜØNŒÍÌ˜WØÜØNLX[™Bˆ[œ[ˆ[[X]\šX[^˜X›H›ÛÙYZÈÜ]Z[\‹‚‹HYYˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝØXÝ]™WÜÚ]WÙ]šY[˜ÙWÙXÚ\Ú[Ûœ×ÌLKšœÛÛ˜ˆ\ÈÓH[™˜[œÙ™\‹YØ]HÚ\š[™ËˆH\Y˜XÝÛ\ÜÚYšY\ÈHLÙ[XÝYˆ^\›˜[[Ý›ÝÜÈ\È™]šY]Ë[Û›H]šY[˜ÙHXÚ\Ú[ÛœÎˆÈ›ÝÜÈ]™H^XÚ]ˆXÝ]™K\Ú]HÛÝ\˜ÙH]šY[˜ÙKÈ›ÝÜÈ™[XZ[ˆš[™[™ËXÛÛ^[Û›K›ÝÜÈ\™BˆÛÝ[X›K[™›ÝÜÈ\™H[\Ü\™XYKˆH^\›˜[˜[œÙ™\ˆØ]H›ÝÈÚXÚÜÂˆH\Y˜XÝ\È\ÙˆH\Y[œ]ÛÛ˜XÝ[™\ÜÙ\ÈŽÍŽÚXÚÜË‚‹H\™[™YHLH™\™\Ù[][Û‹\™XY[™\ÜÈ]Ú]Ý]ÛZ[Z[™ÈH™X[LBˆ[‹ˆHX\YXÛÛ›Û[™Ù[XÝY\[ÝLHÚYXØ\œÈ›ÝÈ™XÛÜ™HLBˆØXÚHZ\ÜË™\]Y\ÝY[Y[œÚ[ÛˆLŽÛÛ\]Y˜[˜XÚÈ˜XÚÙ[™ˆ\ÛL—ÝÌÌMLWÝ\LXÝX[[Y[œÚ[Ûˆ[™ˆ™\]Y\ÝYÍLWÛÜ—Û\™Ù\—Ü™\™\Ù[][Û—Ø˜XÚÙ[™Û›ÝØÛÛ\]YˆHÝXš[]BˆÚYXØ\œÈ™\Ü˜[˜XÚ×ØÚ[™ÙYÚ[H[›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›H[™ˆ›Û‹XÛÝ[X›NˆX\YÛÛ›ÛÈ]™HÈ™X\™\Ý\™Y™\™[˜ÙHÚ[™Ù\È[™ˆ]\š\ÝXËY\ØYÜ™Y[Y[\Ý]\ÈÚ[™Ù\ËÚ[HÙ[XÝY[Ý›ÝÜÈ]™Hˆ™X\™\Ý\™Y™\™[˜ÙHÚ[™Ù\È[™È]\š\ÝXËY\ØYÜ™Y[Y[\Ý]\ÈÚ[™Ù\Ë‚‹H^[™Y›ÛÙYZÈÛÛÜ™[˜]H™XY[™\ÜÈœ›ÛHHÈLÝYÙYÙ[XÝY‚ˆÛÛÜ™[˜]\È[ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLÙ^[™YLšœÛÛ˜ˆÚ]™]Ú˜Z[\™\ËˆH›Ý[™Y^[™Y›ÛÙYZÈÚYÛ˜[[‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÙ^[™YšœÛÛ˜›ÝÈÛÛ\]\È\Âˆ\X[ÝYÙYXÛÛÜ™[˜]H™]šY]È]šY[˜ÙNˆKŽNHZ\ˆ›ÝÜË[KŽNHØY™[BˆX\Y›ÝÜËKŒÌÈ[Ý]Ú[‹Y\ÝšX][Ûˆ˜Z[‹Ý\ÝZ\œËX^˜Z[‹Ý\ÝˆHØÛÜ™HÍLMX[›X\Y˜]È›ÛÙYZÈ˜[Y\Ë[™ˆÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆ]™[[Ý™\ÈHÝYÙYK[Û›H›ÛÙˆ›ØÚÙ\ˆ[™ˆH^[™Y˜]Ë[˜[YHX\[™È›ØÚÙ\‹]Ý^\È›Û‹XÛÝ[X›KÛ›Ýˆ[\Ü\™XYH™XØ]\ÙH[K\ØÛÜ™HÜ]™[XZ[œÈ˜[ÙH[™H\X[ÚYÛ˜[ˆÙ\È›ÝXÚY]™HHØ\™Ù]ˆHÓH›ÝÈXØÙ\ÂˆK[X^\ÝYÙYXÛÛÜ™[˜]\Ø\ÈK\š[Ü‹\ÝYÙYXÛÛÜ™[˜]KXÛÝ[Ø\Yˆ[œÈ\ÙHHYXØ]YÙ[XÝYXÛÛÜ™[˜]HÙX\˜Ú\™XÝÜžK[™H\Y˜XÝˆ^XÚ]H›ØÚÜÈ[ÛÝ]ÛZ[\ÈÚ[HÛÝ™\˜YÙH™[XZ[œÈ\X[‚‹HYYH›Ý[™Y›ÛÙYZÈÛÛÜ™[˜]K\™XY[™\ÜÈ]›ÜˆHXØÙ\YKˆÛÛ^ˆZ[Y›ÛÙYZËXÛÛÜ™[˜]K\™XY[™\ÜØ™XÛÜ™È^XÚ]›ÛÙYZÂˆ›Ý™[˜[˜ÙKÙ[XÝY\ÝXÝ\™HX]\šX[^˜][Ûˆ™XY[™\ÜËZ\ÜÚ[™ÈÙ[XÝYˆÝXÝ\™\Ë™]Ú˜Z[\™\Ë[™™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›HÝ]\ÈÚ]Ý]ˆÛÛ\][™ÈÜˆÛZ[Z[™ÈHK\ØÛÜ™HÜ]ˆHÝ\œ™[\Y˜XÝÝYÙ\ÈBˆÙ[XÝYˆ[PÒQˆš[\ËY[YšY\ÈÍˆX]\šX[^˜X›H]˜[X]Y›ÝÜÈ[™ˆZ\ÜÚ[™ÈÙ[XÝYÝXÝ\™\È›ÜˆWØÜØNŒÍÌ˜[™WØÜØNLX[™ÙY\ÂˆWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÝYÙYKšœÛÛ˜H\X[ˆ™]šY]Ë[Û›H›ÛÙYZÈX\ÞK\ÙX\˜ÚÚYÛ˜[Ý™\ˆÛ›HHHÝYÙYÛÛÜ™[˜]Bˆš[\Ëˆ]™XÛÜ™ÈKX\YZ\ˆ›ÝÜËLÌˆÝYÙY[Ý]Ú[‹Y\ÝšX][Û‚ˆZ\ˆ›ÝÜËX^ÝYÙY˜Z[‹Ý\ÝHØÛÜ™H˜YØZ[œÝHØˆ\™Ù]ÛÝ[X›KÚ[\Ü\™XYH›ÝÜË[™ÙY\Âˆ[ÝWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX‚‹H™Yœ™\ÚYHÝÛœÝ™X[HÙ[XÝY\[ÝÚZ[ˆY\ˆHKH˜XÚÙ[™ˆÙ\]Y[˜ÙK\ÙX\˜Ú\]KˆŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝØØ[™Y]WÜš[Üš]WÌLXˆ™]šY]ËYXÚ\Ú[Ûˆ^Ü]šY[˜ÙHXÚÙ][Ý™\™\Ù[][Ûˆ[‹ÜØ[\Kˆ]šY[˜ÙHÜÜÚY\œË[™H˜[œÙ™\ˆØ]H›ÝÈYÜ™YHÚ]H›ØÚÙ\ˆX]š^‚ˆHØ[YHLÙ[XÝY›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K[LØ\œžBˆ˜XÚÙ[™›Ë[™X\‹Y\XØ]HÝ]\È[ˆH[ÝXÚÙ]ÙÜÜÚY\œËÝ[BˆÛÛ\]K[™X\‹Y\XØ]H›ØÚÙ\œÈ\™HXœÙ[œ›ÛHÙ[XÝY›Ë\ÚYÛ˜[›ÝÜË[™ˆH˜[œÙ™\ˆØ]HÝ[\ÜÙ\ÈËÍË‚‹H™XÛÝ™\™YHÝ[H]]ÛX][ÛˆØÚÈÚ]H\HÛÜšÝ™YH[™š[˜[^™YBˆÛÚ\™[[‹\›ÙÜ™\ÜÈX™[Y˜XÝÜžHØØ[[™ÈÛÜšÈ˜]\ˆ[ˆÝ\[™ÈBˆÛÛ™›XÝ[™È˜[˜ÚK‚‹HXØÙ\YØ]YŒKKLKÍKK[™ÌY[žHX™[Y˜XÝÜžH˜]Ú\ËˆBˆÍH˜]ÚYYÛ›HWØÜØN˜ÈHÌ˜]ÚYYWØÜØNŽ˜ˆWØÜØNŽWØÜØNŽMWØÜØNŽMØ[™WØÜØNŽNX‚‹HYÚ[™Y›Ýš\Ú[Û˜[™]šY]È[\ÈÛÈÙ\‹R\ÈYXÚ[š\ÛH^Z\™YÚ]BˆY][Y\[™[Ü]Ý^\È™YY×Ù^\Ü™]šY]Ø[›\ÜÈ^XÚ]Y][ˆØ][\Ú\È]šY[˜ÙH\È™\Ù[‚‹HYY[ˆXÝ]™K[X\›š[™ÈØ]H™\]Z\š[™È[[›X™[YØ[™Y]H›ÝÜÈÈ™Bˆ™]Z[™Y]™[ˆÚ[ˆH˜[šÙY]Y]YH\ÈØ\Y‚‹HYY\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWØ˜]ÚÜÝ[[X\žKšœÛÛ˜ÈYÙÜ™YØ]HXØÙ\Yˆ˜]Ú\Ë™]šY]ÈXØ]HÝ]\Ë[™XÝ]™K\]Y]YH™][[Û‹‚‹HYY\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍLšœÛÛ˜È˜[šÈLÈ]šY[˜ÙKYØ\ˆ›ÝÜÈ›ÜˆH™^™]šY]È\ÜË‚‹HYY™]šY]ÈšXYÙH\Y˜XÝÂˆ\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÍWÜ™]šY]ËšœÛÛ˜[™ˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍÍWÜ™]šY]ËšœÛÛ˜ÛÈHÍH›Û[Ý[Û‚ˆXÚ\Ú[ÛˆØ[ˆ[œÜXÝ]šY[˜ÙHØ\Èš\œÝ‚‹HYY\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWÜ™]šY]×ÜÝ[[X\žWÍÍKšœÛÛ˜ÈÝ[[X\š^™HBˆ[œ›Û[ÝY™]šY]ÉÜÈXØÙ\[˜ÙK[™[™Ë\™]šY]ËØ]K[™]Y]YK\™][[Û‚ˆY]šXÜË‚‹HYY\Y˜XÝËÝŒ×ÛX™[Ü™]šY]×Ü›Û[Ý[Û—Ü™XY[™\Ü×ÍÍKšœÛÛ˜È]\ÂˆYXÚ[šXØ[H™XYH]™XÛÛ[Y[™È™]šY]È™Y›Ü™H›Û[Ý[Ûˆ™XØ]\ÙH™]šY]Âˆ™]šY]ÈX[˜Ü™X\ÙY[™]Ø\œšY\È™]ËYX[žHYÈ[™™^XXÝ[Û‚ˆÛÝ[È›Üˆ]Y]ˆHØ]H™\]Z\™\È™]šY]ÈÝ[[X\žHÛÝ[ÈÈX]ÚˆXØÙ\[˜ÙH[™^XÚ][›X™[YXØ[™Y]H™][[Û‹‚‹HY\ˆH™]šY]Ë\™XY[™\ÜÈØ]HØ\È[ˆXÙK\ÙYH™[XZ[š[™È›ÙXÝ]™BˆÛÜšÈÚ[™ÝÈÈ^ÜÙHØ\œšYYÛ™]ÈX[žHYÈ[™™^XXÝ[ÛˆÛÝ[È[‚ˆ\˜X›H\Y˜XÝÈ[™™YÜ™\ÜÚ[Ûˆ\ÝË‚‹HYYÛÜšËÛX™[Ü™]šY]×ÍÍWÛ›Ý\Ë›YÚ]HXØÙ\Y[X™[›Ùš[H[™ˆÜ]šY[˜ÙHØ\ÈÈ[œÜXÝ™Y›Ü™H›Û[Ý[Û‹‚‹HYY\Y˜XÝËÝŒ×ÛX™[ÜØØ[[™×Ü]X[]WØ]Y]ÍÍWÜ™]šY]ËšœÛÛ˜[™Bˆ˜]ÚXXØÙ\[˜ÙH™]šY]ËYØ\Ø]KˆHÍH™]šY]È›ÝÈY™\œÂˆ™[ÝË]™\ÚÛ]šY[˜ÙK[[Z]Y™YØ]]™\È[œÝXYÙˆÛÝ[[™È[K‚‹HYYÜ˜\Y\š]™Y^XÝU[šT›ÝÙ\]Y[˜ÙKXÛ\Ý\ˆ›ÞH\Y˜XÝÈ›ÜˆÍBˆ[™Ì[™]XÚY[HÈØØ[[™Ë\]X[]H]Y]ÎÈ›Ý™\ÜZ\ÜÚ[™Âˆ\ÜÚYÛ›Y[È[™™X\‹Y\XØ]H]È[[Û™È]Y]Y›ÝÜË‚‹H^[™YÙ[ÛY]žHÛXÙHÝ[[X\šY\Ë™YÜ™\ÜÚ[Ûˆ\ÝË[™\™›Ü›X[˜ÙH[Z[™Âˆ›ÝYÚHÌY[žHÛÝ[X›HÛXÙK‚‹HYYÛÜšËÛX™[Ü™]šY]×ÍÌÛ›Ý\Ë›YÚ]HXØÙ\Y[X™[›Ùš[H[™ˆYÚ\Ý\š[Üš]HÌ™]šY]ËYX›ÝÜË‚‹H™[XZ[š[™Ë][YH[ˆ^XÝ]Y™Y›Ü™HÜ˜\]\ˆY\ˆHÌØ]HXØÙ\Yš]™BˆÛX[ˆX™[È]™]šY]ÈX›ÜÙHÈH›ÝÜËÝÜY˜[˜ÚHÜ›ÝÝ[™ˆ›ØÝ\ÙYÛˆÙ\]Y[˜ÙKXÛ\Ý\ˆ]Y]ÛÝ™\˜YÙK™]šY]ËYX›Ý\Ë™YÜ™\ÜÚ[Û‚ˆ\ÝË[™ØÝ[Y[][Û‹‚‹HYY[˜[^™K\™]šY]ËYX\™[YYX][Û˜[™ˆØØ[‹\™]šY]ËYXX[\›˜]K\ÝXÝ\™\ØÛÈXØÙ\YMÌ™]šY]ÈX\Âˆ™\Z\˜X›HÚ]Ý]ÛÝ[[™È™]ÈX™[ËˆH›ØÝ\ÙYŒ\›ÝÈ™[YYX][Û‚ˆ\Y˜XÝ[K\›ÝÈ™[YYX][Ûˆ\Y˜XÝ[™ML‹Tˆ[\›˜]K\ÝXÝ\™BˆØØ[ˆ›ÝÈÙY\ÝXÝ\™K]ÚYHÛÙ˜XÝÜˆ]ÈÙ\\˜]Hœ›ÛHØØ[XÝ]™K\Ú]BˆÝ\Ü‚‹H™[XZ[š[™Ë][YH[ˆ›ÜˆHÌ™]šY]ËYX™\Z\ˆ[ŽˆY\ˆH™[YYX][Û‚ˆÛÛ[X[™È[™\™Ù]™YÜ™\ÜÚ[Ûˆ\ÝÈ\ÜÙY™Y›Ü™HH›ÙXÝ]™K]ÛÜšÂˆ›Ý[™\žK™\[ˆH]\›Z[š\ÝXÈ™[YYX][Û‹ØØ[[™Ë\]X[]H]Y]˜]ÚˆÝ[[X\žK˜[Y][Û‹[™[\ÝÝZ]NÈ\ÙH[žH™[XZ[š[™È[YHÈÚXÚÂˆØÜÈ›ÜˆÝ[HÝ\œ™[\Ý]HÛZ[\È˜]\ˆ[ˆÜ[š[™È[›Ý\ˆ˜[˜ÚK‚‹H™[XZ[š[™Ë][YH[ˆ^XÝ]Y›ÜˆH™[X\[ŽˆY\ˆÛÛœÙ\˜]]™Bˆ[\›˜]KTˆ™\ÚYYH™[X\[™ÈÛÜšÙYÛˆH›ØÝ\ÙYÌØØ[‹\ÙYBˆ™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈÈ[ˆHÛÛ\]H[YX›Ý[™YØØ[‹YBˆ™]šY]Ë[Û›H™[X\XYÝ[[X\žHÛÛ[X[™™YÙ[™\˜]H\Y˜XÝË[™™\šYžBˆ\™Ù]Y\ÝÈ[œÝXYÙˆ™[Ü[š[™ÈX™[ÛÝ[Ü›ÝÝ‚‹H™[XZ[š[™Ë][YH[ˆ›ÜˆH^\YXÚ\Ú[Ûˆ[ŽˆY\ˆHYXØ]Yˆ^\[X™[XÚ\Ú[Ûˆ^Ü\ÜÙY\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈÂˆ\™[ˆÛÝ[X›KZ[\Ü™Y\Ø[Y™\Z\‹XØ[™Y]H˜[šÚ[™ËXZÙHHØ]Bˆ[™ØØ[[™È]Y]™\]Z\™HH™\Z\‹XØ[™Y]HÝ[[X\žK™Yœ™\Ú\Y˜XÝˆ™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙK[™ØÝ[Y[H™^›Û‹XÛÝ[X›H™\Z\ˆÝXœÙ]ˆ[œÝXYÙˆ™[Ü[š[™ÈÌJÈX™[Ü›ÝÝ‚‹H™[XZ[š[™Ë][YH[ˆ^XÝ]Y›Üˆ\È™XÛÝ™\žH[ŽˆY\ˆHØØ[Y]šY[˜ÙBˆØ\]Y]Ø\ÈÛÚ\™[[™\ÝÈ\ÜÙYYYHYXØ]YØØ[Y]šY[˜ÙBˆ™]šY]È^Ü›ËYXÚ\Ú[Ûˆ˜]Ú™\Z\ˆ[‹˜XÝÜžKÜØØ[[™Ë\]X[]HØ]\Ëˆ[™ÛÝ[X›KZ[\Ü™Y\Ø[™Y›Ü™H\][™ÈØÜËˆÛÝ[Ü›ÝÝÝ^YYˆÝÜY]ŒX™[Ë‚‹H\È[ˆ™YXÙY™]šY]Ë[Û›HØØ[Y]šY[˜ÙHXÚ]Ý]ÛÝ[Ü›ÝÝ‚ˆH™XXÝ[Û‹ÜÝXœÝ˜]H™\Z\ˆ[™\È
WØÜØNNL˜WØÜØNØˆWØÜØNMWØÜØNŒ˜
H\™HÛÜÙY\È™]šY]ÙYÝ][Ù‹\ØÛÜH™\Z\‹[Û›Bˆ›ÝÜËHÈ^XÚ][\›˜]K\™\ÚYYH[™\È
WØÜØNMØWØÜØNMÎˆWØÜØNØ
H›ÝÈ]™HÛÛ˜Ü™]HÛÝ\˜Ú[™È™\]Y\ÝÈXÜ›ÜÜÈÍ[\›˜]H‚ˆÝXÝ\™\Ë[™H™]šY]Ë[Û›H[\Ü\ØY™]H]Y]ÛÛ™š\›\ÈHZ\ÛX]Úˆ^\YXÚ\Ú[Û‹[™ØØ[Y]šY[˜ÙHXÚ\Ú[Ûˆ˜]Ú\ÈYÛÝ[X›HX™[Ë‚‹H[\[Y[YH^\\™]šY]ÙYUÜÜÜÜž[]˜[œÙ™\ˆš[™Ù\œš[Y˜[Z[Bˆ^[œÚ[Ûˆ›ÜˆTËTÒÒKUYÜ˜\ÜÒÓ’Ë‘ËšÐKšÐ‹[™ÒT‚ˆH^[œÚ[Ûˆ\ÈÚ\™Y›ÝYÚÛÛÙÞH™XÛÜ™Ë™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Úˆ™]šY]È^ÜX\[™Ë˜[Z[K\›ÜYØ][Ûˆ›ØÚÙ\œËXÝ]™K[X\›š[™Èš[Üš]KˆY™\œØ\šX[™YØ]]™\ËØ]HÚXÚÜËØØ[[™Ë\]X[]H]Y]™YÜ™\ÜÚ[Ûˆ\ÝËˆ[™ØÝ[Y[][ÛˆÚ[HÙY\[™È]™\žHX\Y›ÝÈ›Û‹XÛÝ[X›K‚‹HXØÙ\YHØ]YÌKY[žHX™[Y˜XÝÜžH˜]ÚˆH˜]ÚYYˆWØÜØNÌXWØÜØNÌXWØÜØNÌMWØÜØNÌM˜WØÜØNÌŒØ[™ˆWØÜØNÌØ\ÈÛX[ˆÛÝ[X›HX™[Ë˜Z\Ú[™ÈHØ[›ÛšXØ[™YÚ\ÝžHÈŒÌˆX™[ÈÚ[HX]š[™ÈL™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›K‚‹HYYXØÙ\YMÌH™]šY]Ë[Û›H™\Z\ˆ\Y˜XÝÎˆ^\[X™[XÚ\Ú[Ûˆ^Üˆ›ÜˆMH›ÝÜËK\›ÝÈØØ[Y]šY[˜ÙHØ\]Y]Ù^ÜÜ™\Z\ˆ[‹^XÚ]ˆ[\›˜]H™\ÚYYK\ÜÚ][Ûˆ™\]Y\ÝË™]šY]Ë[Û›H[\Ü\ØY™]H]Y]›ØÝ\ÙYˆ[\›˜]K\ÝXÝ\™HØØ[‹™[X\[ØØ[]Y]›ÜˆWØÜØNÌL˜ÛÛÙÞKYØ\ˆ]Y]X\›™Y\™]šY]˜[X[šY™\ÝÙ\]Y[˜ÙK\Ú[Z[\š]H˜Z[\™K\Ù]]Y][™ˆØØ[[™Ë\]X[]H]Y]‚‹HYY\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÍÌKšœÛÛ˜ÚXÚˆ^XÚ]HY™\œÈ[LXØÙ\YMÌH™]šY]Ë\Ý]H›ÝÜÈÚ]ÛÝ[X›BˆØ[™Y]\È[™\Ü˜Y\ÈHÌHØ]HÈŒKÌŒHÚXÚÜË‚‹HXØÙ\YHØ]YÍLY[žHX™[Y˜XÝÜžH˜]ÚˆH˜]ÚYYˆWØÜØNÌŽWØÜØNÌÌØWØÜØNÌÍXWØÜØNÌÎXWØÜØNÍˆWØÜØNÍ˜[™WØÜØNÍL\ÈÛX[ˆÛÝ[X›HX™[Ë˜Z\Ú[™ÈBˆØ[›ÛšXØ[™YÚ\ÝžHÈŒÍÈX™[ÈÚ[HX]š[™ÈLN™]šY]Ë\Ý]H›ÝÜÂˆ›Û‹XÛÝ[X›K‚‹HYY\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÍÍLšœÛÛ˜ÚXÚˆ^XÚ]HY™\œÈ[LNXØÙ\YMÍL™]šY]Ë\Ý]H›ÝÜÈÚ]ÛÝ[X›BˆØ[™Y]\È[™\Ü˜Y\ÈHÜÝX˜]ÚÍLØ]HÈŒÌŒÚXÚÜË‚‹HXØÙ\YHØ]YÍÍKY[žHX™[Y˜XÝÜžH˜]ÚˆH˜]ÚYYˆWØÜØNÍMWØÜØNÍNWØÜØNÍNXWØÜØNÍŒ˜[™WØÜØNÍÍ˜\ÂˆÛX[ˆÛÝ[X›HX™[Ë˜Z\Ú[™ÈHØ[›ÛšXØ[™YÚ\ÝžHÈˆX™[ÈÚ[BˆX]š[™ÈLÎ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›K‚‹HYÚ[™YH›Ýš\Ú[Û˜[Ù\‹R\ÈY›Û\ÙH]ÛÈWØÜØNÍÌX\Ý[BˆÙ\‹R\È^Ú]ÛÝ[\™]šY[˜ÙH™[XZ[œÈ™YY×Û[Ü™WÙ]šY[˜ÙX[™\ÂˆÛ\ÜÚYšYY\ÈH^[XZØYÙHš\ÚÈ˜]\ˆ[ˆÛÝ[Y‚‹HXØÙ\YHØ]YKKK[™LY[žHX™[Y˜XÝÜžH˜]Ú\ËˆBˆ˜]Ú\ÈYY[ˆÛX[ˆÛÝ[X›HX™[ÈÝ[˜Z\Ú[™ÈHØ[›ÛšXØ[ˆ™YÚ\ÝžHÈLˆX™[ÈÚ[HX]š[™ÈŒÈ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›K‚‹HYYÙ[ÛY]žKY™X]\™H›ÝÈ™]\ÙH›ÝYÚZ[YÙ[ÛY]žKY™X]\™\ÂˆK\™]\ÙKY^\Ý[™ØÛÈ›Ý[™Y˜[˜Ú\ÈØ[ˆ™]\ÙH[˜Ú[™ÙYÙ[ÛY]žH›ÝÜÂˆ[œÝXYÙˆ™XZ[[™È]™\žHš[Üˆ[žK‚‹HYÚ[™Y›Ýš\Ú[Û˜[Y][ZY›Û\ÙH›Û[Ý[ÛˆÛÈWØÜØNŽÍ˜\Ý[Bˆ›ÛKZ[™™\œ™YY][ZY›Û\ÙHØ[™Y]\ÈÚ]Ý]ØØ[YØ[™Ý\Ü™[XZ[‚ˆ™YY×Û[Ü™WÙ]šY[˜ÙX˜]\ˆ[ˆÛÝ[Y‚‹HXØÙ\YHØ]YÍKKLKLKK[™MLY[žHX™[Y˜XÝÜžH˜]Ú\Ë‚ˆH˜]Ú\ÈYYŒHÛX[ˆÛÝ[X›HX™[ÈÝ[˜Z\Ú[™ÈHØ[›ÛšXØ[ˆ™YÚ\ÝžHÈÌÈX™[ÈÚ[HX]š[™ÈŽˆ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›K‚‹HYY^\Ü™]šY]×ÙXÚ\Ú[Û—Û™YYY\È[ˆ^XÚ]ØØ[[™Ë\]X[]H\ÜÝYBˆÛ\ÜÈÛÈ\Ý\ÜY›ÝÜÈÝXÚ\ÈWØÜØNŽX\™HÛ\ÜÚYšYY\Âˆ›Û‹XÛÝ[X›H^\›˜[\™]šY]ÈX˜]\ˆ[ˆ›ØÚÚ[™È›Û[Ý[Ûˆ\Âˆ[˜Û\ÜÚYšYY™]šY]ÈX‚‹HXØÙ\YHØ]YMÍKH[™KY[žHX™[Y˜XÝÜžH˜]Ú\Ë˜Z\Ú[™ÈBˆØ[›ÛšXØ[™YÚ\ÝžHÈÎHÛÝ[X›HX™[ÈÚ[HX]š[™ÈÌˆ™]šY]Ë\Ý]Bˆ›ÝÜÈ›Û‹XÛÝ[X›K‚‹HÜ[™YH›Ý[™YKH™]šY]ËˆH™]šY]ÈØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜË]ˆXØÙ\[˜ÙH\È˜[ÙH™XØ]\ÙH]YÈÛX[ˆÛÝ[X›HX™[È[™™]šY]ÈXˆš\Ù\ÈÈÌŽH›ÝÜËˆHÛÝ\˜ÙK\ØØ[H]Y]™XÛÜ™ÈKÈØœÙ\™YKPÔÐHÛÝ\˜ÙBˆ™XÛÜ™È[™ÚYÈ™^ÛÜšÈÝØ\™^\›˜[\ÛÝ\˜ÙH˜[œÙ™\‹‚‹HYY^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆØØY™›Û[™È›ÜˆHÜÝSKPÔÐH]‚ˆÛÝ\˜ÙK[[Z]]Y]˜[œÙ™\ˆX[šY™\Ý]Y\žHX[šY™\ÝÓÑØ[Xœ˜][Ûˆ[‹ˆÌ\›ÝÈ[šT›ÝÐ‹ÔÝÚ\ÜËT›Ý™XY[Û›HØ[™Y]HØ[\KÝX\™˜Z[]Y]ˆ\Y˜XÝ™YÜ™\ÜÚ[Ûˆ\ÝË[™[š]\ÝËˆ[^\›˜[Ø[™Y]\È\™Bˆ›Û‹XÛÝ[X›K‚‹H\™[™YH^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆ]Ú]H™]šY]Ë[Û›HØ[™Y]BˆX[šY™\ÝØ[™Y]K[X[šY™\Ý]Y][™KX˜[[˜ÙH]Y]]šY[˜ÙH[‹ˆ]šY[˜ÙH™\]Y\Ý^Ü^\›˜[™]šY]Ë[Û›H[\Ü\ØY™]H]Y]LKÌLBˆ˜[œÙ™\ˆØ]K›Ý[™YšXH™XXÝ[Û‹XÛÛ^Ø[\K[™™XXÝ[Û‹XÛÛ^ˆÝX\™˜Z[]Y]ˆHØ[›ÛšXØ[™YÚ\ÝžH™[XZ[œÈ]ÎHX™[ÎÈ^\›˜[ˆX™[È\™HÛÝ[X›K‚‹HYYœ›ØYÚ[˜ÛÛ\]HPÈ›Ý][™È[™H™]šY]Ë[Û›HXÝ]™K\Ú]H]šY[˜ÙBˆ]Y]YH›ÜˆH^\›˜[]ˆÙ]™[ˆØ[™Y]\È™\]Z\™Hœ›ØYQPÈ][[Û‹ˆ™YHœ›ØY[Û›H›ÝÜÈ\™HY™\œ™Y™Y›Ü™HXÝ]™K\Ú]HX\[™ËHØ[™Y]\Âˆ\™H]Y]YY›ÜˆXÝ]™K\Ú]H]šY[˜ÙK[™^\›˜[X™[È\™HÛÝ[X›K‚‹HY˜[˜ÙYH^\›˜[]œ›ÛH]šY[˜ÙH]Y]YHÈ›Ý[™Y™]šY]Ë[Û›BˆÛÛ›ÛÎˆØ[\Y[šT›ÝÐˆXÝ]™K\Ú]H™X]\™\È›Üˆ[H™XYH^\›˜[ˆ›ÝÜË›Ý[™MHXÝ]™K\Ú]KY™X]\™K\Ý\ÜYØ[™Y]\È[™L™X]\™HØ\Ëˆ]Y]YYLˆØ[™Y]\È›Üˆ]\š\ÝXËXÛÛ›Û›ÝÝ\[™ËX\Y[L‚ˆ]\š\ÝXË\™XYHÛÛ›ÛÈÛÈÝ\œ™[[Q›ÛÒQˆÝXÝ\™\Ë˜[ˆBˆÝ\œ™[Ù[ÛY]žH]\š\ÝXË[™™XÛÜ™YHY][ZY›Û\ÙHÜHÛÛ\ÙH\ÂˆHØÛÜKÝÜHZ\ÛX]Ú\È[‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ˜Z[\™WÛ[ÙWØ]Y]ÌLKšœÛÛ˜ˆH^\›˜[ˆ˜[œÙ™\ˆØ]H›ÝÈ\ÜÙ\ÈÌËÌÌÈ™]šY]Ë[Û›HÚXÚÜÈ[™Ý[YÈÛÝ[X›BˆX™[Ë‚‹H^[™Y^\›˜[\ÛÝ\˜ÙHÛÛ›ÛÈœ›ÛHHXÛÛ›Û]\š\ÝXÈØ[\HÈ[ˆLˆ]\š\ÝXË\™XYH[Q›ÛÛÛ›ÛËYY™]šY]Ë[Û›HÛÛ›Û\™\Z\‹ˆ™\™\Ù[][Û‹XÛÛ›Ûš[™[™ËXÛÛ^[™XXÝ[Û‹XÛÛ^[™ˆÙ\]Y[˜ÙKZÛÝ]\Y˜XÝË[™˜Z\ÙYH^\›˜[˜[œÙ™\ˆØ]HÈÌËÌÌË‚ˆ^\›˜[Ø[™Y]\ÈÝ[YÛÝ[X›HX™[È[™\™H›Ý[\Ü\™XYK‚‹HYY^\›˜[\ÛÝ\˜ÙH™\Z\ˆÛÛ›ÛÈ›ÜˆHš[Üˆ™\Z\ˆ\ÜÎˆ™X]\™K\›ÞBˆ™\™\Ù[][ÛˆÛÛ\\š\ÛÛ‹œ›ØYQPÈ\Ø[XšYÝX][Û‹XÝ]™K\Ú]HØ\ÛÝ\˜ÙBˆ™\]Y\ÝË[™HÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙ[‹ˆH^\›˜[˜[œÙ™\ˆØ]H›ÝÂˆ\ÜÙ\ÈÎÌÎ™]šY]Ë[Û›HÚXÚÜÈÚ[HÙY\[™È]™\žH^\›˜[›ÝÈ›Û‹XÛÝ[X›K‚‹HYY›Ý[™YÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙØÜ™Y[š[™È[™Ø[™Y]K[]™[[\Üˆ™XY[™\ÜÈ]Y][™Ëˆ][\›YYX]H^\›˜[˜[œÙ™\ˆØ]H\ÜÙYKÍBˆ™]šY]Ë[Û›HÚXÚÜÈÚ[HÙY\[™È]™\žH^\›˜[›ÝÈ›Û‹XÛÝ[X›H[™ˆ[\ÜX›ØÚÙY‚‹HYY›Ý[™YÙ\]Y[˜ÙKX[YÛ›Y[™\šYšXØ][Ûˆ›ÜˆHÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙˆÜ]È\È[ˆXÝ]™K\Ú]HÛÝ\˜Ú[™È]Y]YH›ÜˆHL^\›˜[XÝ]™K\Ú]BˆØ\Ëˆ]ÚXÚÜÚ[˜Z\ÙYH^\›˜[˜[œÙ™\ˆØ]HÈKÍH™]šY]Ë[Û›BˆÚXÚÜÈÚ[HÙY\[™È]™\žH^\›˜[›ÝÈ›Û‹XÛÝ[X›H[™[\ÜX›ØÚÙY‚‹HYYÛÝ\˜ÙK\™]šY]È^ÜÈ›ÜˆXÝ]™K\Ú]HÛÝ\˜Ú[™È[™ÛÛ\]HÙ\]Y[˜ÙBˆÙX\˜ÚH™\™\Ù[][Û‹X˜XÚÙ[™[‹[™[ˆ[YÜ˜]Y^\›˜[›ØÚÙ\‚ˆX]š^ˆH^\›˜[˜[œÙ™\ˆØ]H›ÝÈ\ÜÙ\ÈLËÍLÈ™]šY]Ë[Û›HÚXÚÜÈÚ[BˆÙY\[™È]™\žH^\›˜[›ÝÈ›Û‹XÛÝ[X›H[™[\ÜX›ØÚÙY‚‹HYYXÝ]™K\Ú]HÛÝ\˜Ú[™È™\ÛÛ][Ûˆ[™™\™\Ù[][Ûˆ˜XÚÙ[™Ø[\\È›Ü‚ˆH^\›˜[KH˜[œÙ™\ˆ]ˆHXÝ]™K\Ú]H™\ÛÛ][Ûˆ™KXÚXÚÜÈ[LˆØ\›ÝÜÈYØZ[œÝ[šT›Ý™X]\™H]šY[˜ÙKš[™È^XÚ]XÝ]™K\Ú]Bˆ™\ÚYYHÛÝ\˜Ù\Ë[™ÙY\ÈÈš[™[™Ë\\Ë\™XXÝ[Ûˆ›ÝÜÈ[™È™XXÝ[Û‹[Û›Bˆ›ÝÜÈ›Û‹XÛÝ[X›KˆH]\›Z[š\ÝXÈÙ\]Y[˜ÙHË[Y\ˆ˜\Ù[[™HÛÝ™\œÈ[L‚ˆ[›™Y™\™\Ù[][ÛˆÛÛ›ÛÈ[™›YÜÈŒMÍ\ÈH™\™\Ù[][Û‚ˆ™X\‹Y\XØ]HÛÝ]ÈHØ[›ÛšXØ[TÓKLˆØ[\HÛÝ™\œÈ[LˆÛÛ›ÛËˆ›YÜÈÈ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]Ë[™ÙY\ÈH^\›˜[ˆ˜[œÙ™\ˆØ]H]NKÍNH™]šY]Ë[Û›HÚXÚÜÈÚ][\Ü\™XYHX™[Ë‚‹HYYÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]]˜[X][Ûˆ›ÜˆHXØÙ\YÛÝ[X›Bˆ™YÚ\ÝžH[ˆ›ÝHK[™KHÛXÙHÛÛ^Ëˆ›È›ÛÙYZËS\Ù\\Ì‹ˆ“TÕÜˆPSSÓ‘^XÝ]X›HØ\È]˜Z[X›HØØ[KÛÂˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]Ù]˜[ÌLšœÛÛ˜[™ˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]Ù]˜[ÌLKšœÛÛ˜^XÚ]HX™[BˆÜ]\ÈH]\›Z[š\ÝXÈ›ÞH\Ú[™È^XÝ[šT›Ý™Y™\™[˜ÙHÛ\Ý\œËˆÙ[XÝY\ÝXÝ\™HY[YšY\œË[™XÝ]™K\Ú]HÙ[ÛY]žHXÚÙ]ËˆBˆ[[Ý]\][Ûˆ\ÈLÍˆ›ÝÜËLÍKÌLÍˆ›ÝÜÈ\ÜÚ[™ÈHÝšXÝˆÝË[™ZYÚ›ÜšÛÙ›ÞKÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœË[[Ý]ˆ]˜[XX›H[‹\ØÛÜHÜHXØÝ\˜XÞH[™™][[ÛˆÙˆŽMÍØ[™ˆÜKÝÜÈXØÝ\˜XÞH[[Û™È™]Z[™Y[[Ý]]˜[XX›H›ÝÜÈÙˆKŒ‚‹HYYHš\œÝ›Ý[™YX\›™Y™\™\Ù[][Ûˆ˜XÚÙ[™Ø[\H›Üˆ^\›˜[ˆ[Ý™XY[™\ÜËˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜ˆÛÛ\]\ÈLˆTÓKLˆ
˜XÙX›ÛÚËÙ\ÛL—Ý—ÎWÕTL
HØ[™Y]KXÛÛ›Û›ÝÜÈÚ]ˆÌŒY[Y[œÚ[Û˜[[X™Y[™ÜËÙY\È[›ÝÜÈ™]šY]Ë[Û›H[™›Û‹XÛÝ[X›Kˆ›YÜÈÈ™\™\Ù[][Û‹[™X\‹Y\XØ]HÛÝ]Ë[™[Z]ÈL‚ˆX\›™Y]œËZ]\š\ÝXÈ\ØYÜ™Y[Y[›ÝÜËˆH^\Ý[™ÈL‹\›ÝÈ]\›Z[š\ÝXÂˆË[Y\ˆØ[\H™[XZ[œÈH˜\Ù[[™KÜ›ÞHÛÛ›Û[™]\š\ÝXÈÙ[ÛY]žBˆ™]šY]˜[™[XZ[œÈ]XÚY\ÈH™\]Z\™Y˜\Ù[[™K‚‹H\™[™Y^\›˜[˜[œÙ™\ˆ\Y˜XÝÜ˜\ÛÛœÚ\Ý[˜ÞH›ÜˆHKH[Ýˆ]ˆÚXÚËY^\›˜[\ÛÝ\˜ÙK]˜[œÙ™\‹YØ]\Ø›ÝÈ˜[Y]\È\Y˜XÝ\]ˆ[™XYÙHXÜ›ÜÜÈ[ŒHÝ\YY^\›˜[\Y˜XÝË™XÛÜ™ÈHÛX[‚ˆKH[™XYÙH[™\‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜[™˜Z[È˜\ÝˆÛˆZ^Y\ÛXÙH]ÈÜˆ^[ØYYXÛ\™YÛXÙHÛÛ˜YXÝ[ÛœÈ™Y›Ü™HHØ]Bˆ\Y˜XÝØ[ˆÚ[[H\ÜË‚‹HYY\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙ]šY[˜ÙWÙÜÜÚY\œ×ÌLKšœÛÛ˜\ÈBˆ™]šY]Ë[Û›H\‹XØ[™Y]H]šY[˜ÙHÜÜÚY\ˆ›ÜˆHLÙ[XÝY^\›˜[ˆ[Ý›ÝÜËˆ]™XÛÜ™ÈXÝ]™K\Ú]H™X]\™HÝ\ÜXÝ]™K\Ú]HÛÝ\˜Ú[™ÂˆÝ]\ËšXH™XXÝ[ÛˆÛÛ^Ù\]Y[˜ÙH[YÛ›Y[ÚXÚÜËÝXÝ\™HX\[™Ëˆ]\š\ÝXÈÛÛ›Û™\Ý[Ë™\™\Ù[][ÛˆÛÛ›ÛË[™™[XZ[š[™È›ØÚÙ\œÂˆÚ]Ý]XZÚ[™È[žH›ÝÈÛÝ[X›HÜˆ[\Ü\™XYK‚‹HYYH[Ý\ÜXÚYšXÈ™\™\Ù[][Ûˆ˜XÚÙ[™]›ÜˆHÙ[XÝY^\›˜[ˆÛÜšÛ\Ýˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—ÌLKšœÛÛ˜ˆÛÝ™\œÈ[LÙ[XÝY›ÝÜË[™ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜ˆÛÛ\]\È™]šY]Ë[Û›HTÓKLˆ[X™Y[™ÜÈ›Üˆ[L›YÜÈMLŒØ\ÈBˆ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]™Yœ™\Ú\ÈH[ÝÜÜÚY\œÈÛÈ]™\žBˆÙ[XÝY›ÝÈ\È™\™\Ù[][Ûˆ]šY[˜ÙK[™ÙY\È]™\žH^\›˜[›ÝÂˆ›Û‹XÛÝ[X›H[™›Ý[\Ü\™XYK‚‹HYYH™X[Ù\]Y[˜ÙKY\Ý[˜ÙHÛÝ]˜XÚÙ[™›ÜˆHXØÙ\Y™YÚ\ÝžK‚ˆZ[\Ù\]Y[˜ÙKY\Ý[˜ÙKZÛÝ]Y]˜[›ÝÈXØÙ\ÈHTÕH[™[œÈS\Ù\\Ì‚ˆÛ\Ý\š[™È]Ì	HY[]H[™	HÛÝ™\˜YÙHÚ[H™]Z[š[™ÈH]\›Z[š\ÝXÂˆ›ÞH]\È˜[˜XÚÈÛÛ^ˆH™Yœ™\ÚYK[™KHÛÝ]ˆ\Y˜XÝÈÛÝ™\ˆÎÍÎ]˜[X]YX™[ËÛ\Ý\ˆÌÎÙ\]Y[˜ÙH™XÛÜ™ËÛˆÝ]LÍˆ›ÝÜÈžHÚÛHÙ\]Y[˜ÙHÛ\Ý\œË™XÛÜ™X^˜Z[‹Ý\ÝY[]BˆŒŽXÚY]™HHLÌ	H\™Ù][™ÙY\[[Ý]Ý][Ù‹\ØÛÜH˜[ÙBˆ›Û‹XXœÝ[[ÛœÈ]ˆ›ÛÙYZËÕK\ØÛÜ™HÙ\\˜][Ûˆ™[XZ[œÈXœÙ[]ˆZ[Y›ÛÙYZËXÛÛÜ™[˜]K\™XY[™\ÜØ›ÝÈ™XÛÜ™È›ÛÙYZÈ›Ý™[˜[˜ÙH[™ˆ›Ý[™YÛÛÜ™[˜]HÝYÚ[™È™XY[™\ÜË‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLšœÛÛ˜\ÈBˆ›Ý[™YÚYXØ\ˆ\™XÝÜžH\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]\×ÌLØˆBˆ\Y˜XÝ\È™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K™XÛÜ™È^XÚ]›ÛÙYZÂˆÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[‹Øš[‹Ù›ÛÙYZØ™\œÚ[ÛˆLŽMXÙÌØˆY[YšY\ÈÎ]˜[X]Y›ÝÜËÍˆ›ÝÜÈÚ]Ý\ÜYÙ[XÝY‚ˆÛÛÜ™[˜]\ËZ\ÜÚ[™ÈÙ[XÝYÝXÝ\™\È›ÜˆWØÜØNŒÍÌ˜[™WØÜØNLXˆ[™ÝYÙ\ÈHÙ[XÝYˆ[PÒQˆš[\ÈÚ[HÙY\[™ÂˆWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX‚ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLÜÝYÙYKšœÛÛ˜[ˆÛÛ\]\ÈBˆ\X[ÝYÙYXÛÛÜ™[˜]H›ÛÙYZÈHÚYÛ˜[Ý™\ˆÜÙHHš[\ÈÛ›NˆKˆX\YZ\ˆ›ÝÜËLÌˆÝYÙY[Ý]Ú[‹Y\ÝšX][ÛˆZ\ˆ›ÝÜËX^ÝYÙYˆ˜Z[‹Ý\ÝHØÛÜ™H˜ÛÝ[X›KÚ[\Ü\™XYH›ÝÜË[™ˆ[ÝWÜØÛÜ™WÜÜ]ØÛÛ\]YY˜[ÙX‚‹HYYÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›Yˆ›ÛÙYZÈ\È[œÝ[X›H[ˆBˆ\ÛÛ]Y[\Ü˜\žHÛÛ™H[š\›Û›Y[Üš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[˜ˆ[™™\ÜÈ™\œÚ[ÛˆLŽMXÙÌØˆK\ØÛÜ™HÜ][™È™[XZ[œÈ›ØÚÙYÛ‚ˆX]\šX[^š[™ÈH™[XZ[š[™ÈÙ[XÝY‹Ð[Q›ÛÛÛÜ™[˜]\È[™Y[™ÂˆH›ÛÙYZÈÜ]Z[\‹‚‹H\™[™YYXÚ[š\ÛK]^ÛÝ[\™]šY[˜ÙH[È^XÚ]Ø]YÛÜšY\Î‚ˆÝXÝ\™KÛØØ[Y]šY[˜ÙHÛÝ[\™]šY[˜ÙH™[XZ[œÈ™YXÝ]™HØY™]H]šY[˜ÙKˆÚ[HYXÚ[š\ÛK]^ÛÝ[\™]šY[˜ÙH\È™]šY]ÈÛÛ^Û›H[™›Ý˜[Y›Ü‚ˆÜœ[ˆ\ØÛÝ™\žHØY™]HÛZ[\ËˆHXØÙ\YLKX›][Ûˆ\Y˜XÝ™XÛÜ™ÂˆMMÈÚ[™ÙY›ÝÜËMMˆ™]šY]ËYX›ÝÜËŒÜH›Ý]HÚ[™Ù\Ë[™ˆÝXÝ\™KÛØØ[ÝX\™˜Z[ÜÜÙ\Ë‚‹H^[™YH™\™\Ù[][Ûˆ˜XÚÙ[™]È\™Ù\ˆTÓKLˆY[YšY\œÈ[™ˆYYLHÚYXØ\‹ÜÝXš[]H\Y˜XÝÈ›ÜˆX\YÛÛ›ÛÈ[™Ù[XÝY[Ýˆ›ÝÜËˆHÝ\œ™[LH[ˆ\È™X\ÚXš[]H]šY[˜ÙHÛ›N‚ˆ˜XÙX›ÛÚËÙ\ÛL—ÝÌ×ÍLWÕTLØ\È›ÝØXÚYØØ[KÛÈÚYXØ\œÈ™XÛÜ™ˆ[Ù[Ý[˜]˜Z[X›WÛØØ[X^XÝY[Y[œÚ[ÛˆLŽ[X™Y[™È˜Z[\™\Ëˆ[\ÙY[YK[™K]œËMLHÝXš[]HÝ]\ÈÚ]Ý]™\XÚ[™ÈHÛÛ\]YˆH˜\Ù[[™K‚‹HYYH™X[^\›˜[\[Ý˜XÚÙ[™Ù\]Y[˜ÙHÙX\˜Ú›ÜˆHÌ\›ÝÂˆ[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[\Kˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜ˆ\Ù\ÈØØ[S\Ù\\ÌˆNNØÍXØÛÛ\\™\ÈÌ^\›˜[Ù\]Y[˜Ù\ÈYØZ[œÝÌÍBˆÝ\œ™[XØÙ\Y\™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœÈ™\™\Ù[YžHÌÍÈÙ\]Y[˜ÙH™XÛÜ™Ëˆ™\Ù\™\È^XÝ\™Y™\™[˜ÙHÛÝ]ÈÌMMLØ[™ŒL˜™XÛÜ™ÈŽˆ›Ë[™X\‹Y\XØ]K\ÚYÛ˜[›ÝÜÈ[™˜XÚÙ[™˜Z[\™\Ë[™ÙY\È]™\žH›ÝÂˆ™]šY]Ë[Û›K›Û‹XÛÝ[X›K[™›Ý[\Ü\™XYK‚‹HÚ\™YH˜XÚÙ[™Ù\]Y[˜ÙK\ÙX\˜Ú\Y˜XÝ[È^\›˜[[\Ü\™XY[™\ÜËˆ›ØÚÙ\‹[X]š^[™˜[œÙ™\‹YØ]H\Y˜XÝËˆHÛÛ\]K\ÙX\˜Ú›ØÚÙ\ˆ\Âˆ™[[Ý™YÛ›H›Üˆ˜XÚÙ[™›Ë\ÚYÛ˜[›ÝÜÎÈ[\Ü™XY[™\ÜÈÝ[™\ÜÈˆ[\Ü\™XYH›ÝÜËˆÙ\]Y[˜ÙHÛÝ]ÜÙX\˜Ú›ÝÜËXÝ]™K\Ú]HØ\Ëˆ™\™\Ù[][Û‹XÛÛ›Û\ÜÝY\Ë›È^\XÚ\Ú[ÛœË[™[˜XÝÜžKYØ]Bˆ›ØÚÙ\œËˆH^\›˜[˜[œÙ™\ˆØ]H›ÝÈ\ÜÙ\ÈËÍÈ™]šY]Ë[Û›HÚXÚÜË‚‚ˆÈÈÝ\œ™[Y]šXÜÂ‚‹HÝ\˜]YX™[™YÚ\ÝžNˆŽˆœ›Ûž™H]]ÛX][Û‹XÝ\˜]YX™[ËÚ]ŒL‚ˆÙYYYš[™Ù\œš[ÜÚ]]™\È[™ÌÝ][Ù‹\ØÛÜHX™[ËˆH^\›˜[ˆÝ][Ù‹\ØÛÜHY[X™\œÈ\™H[š\›Ý”Í[š\›Ý”ÎMX[™ˆ[š\›Ý”LÓLØ‚‹HŒY[žHÛXÙNˆ™\ÚÛLŒÌŒ]˜[XX›KËÍÈ[‹\ØÛÜHÜÚ]]™\Âˆ™]Z[™Y˜[ÙH›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë‚‹HLKY[žHÛXÙNˆ™\ÚÛLMXLÌLH]˜[XX›KÎÌÎ[‹\ØÛÜBˆÜÚ]]™\È™]Z[™Y˜[ÙH›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËˆØÛÜ™HØ\ŒÌ‚‹HLY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXLÍN]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KLËÌLÌH[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™WØÜØNM™\Ù\™Y\È›Û‹XÛÝ[X›K‚‹HLKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXLMÍLŒˆ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KLÍKÌLÎH[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™™XYHX™[Ø[™Y]\Ë‚‹HMLY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXLÍKÍMH]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMÌM[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™™XYHX™[Ø[™Y]\Ë‚‹HMÍKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXML‹ÍMŒˆ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KM‹ÌMˆ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™™XYHX™[Ø[™Y]\Ë‚‹HŒY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXMŽÍMÎ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMËÌMÈ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™™XYHX™[Ø[™Y]\Ë‚‹HŒKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXNÍNN]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMÌM[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™H™XYHX™[Ø[™Y]\È™Y›Ü™HHXØÙ\Yˆ˜]ÚXÚ\Ú[ÛœË‚‹HLY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒKÍŒMÈ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMËÌMLH[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™ÌH™XYHX™[Ø[™Y]\È™Y›Ü™HHXØÙ\Yˆ˜]ÚXÚ\Ú[ÛœË‚‹HÍKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒKÍŒN]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMÌMLˆ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™H™XYHX™[Ø[™Y]\ÈY\ˆXØÙ\[™ÂˆWØÜØN˜‚‹HÌY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒËÍŒŒÈ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMLËÌMMÈ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™™XYHX™[Ø[™Y]\ÈY\ˆXØÙ\[™ÈHš]™BˆÛX[ˆÌX™[Ë‚‹HÌKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒLËÍŒŽH]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMNKÌMŒÈ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™H™XYHX™[Ø[™Y]\È™Y›Ü™HXØÙ\[™ÈÚ^ˆÛX[ˆÌHX™[Ë‚‹HÍLY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒŒÍŒÍˆ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KM‹ÌMÌ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™MH™XYHX™[Ø[™Y]\ÈY\ˆXØÙ\[™ÈÙ]™[‚ˆÛX[ˆÍLX™[Ë‚‹HÍÍKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒKÍH]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMÌKÌMÍH[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™LLÈ™XYHX™[Ø[™Y]\ÈY\ˆXØÙ\[™Èš]™BˆÛX[ˆÍÍHX™[Ë‚‹HY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒŽKÍH]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMÍKÌMÎH[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë[™]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœÈY\ˆXØÙ\[™È›Ý\ˆÛX[ˆX™[Ë‚‹HKY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒÌ‹Í]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KMÎÌNˆ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë[™]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœÈY\ˆXØÙ\[™È™YHÛX[ˆHX™[Ë‚‹HLY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXŒÍKÍLH]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KNKÌNH[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™MÈœ›Ûž™K]Ë\Ú[™\ˆ›Û[Ý[ÛˆØ[™Y]\ÈY\‚ˆXØÙ\[™È™YHÛX[ˆLX™[Ë‚‹HMLY[žHÛÝ[X›HÛXÙNˆ™\ÚÛLMXM‹ÍÌˆ]˜[X]YX™[Yˆ›ÝÜÈ]˜[XX›KŒ‹ÌŒˆ[‹\ØÛÜHÜÚ]]™\È™]Z[™Y˜[ÙBˆ›Û‹XXœÝ[[ÛœË\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë]šY[˜ÙK[[Z]Yˆ[‹\ØÛÜHXœÝ[[ÛœË[™LLHœ›Ûž™K]Ë\Ú[™\ˆ›Û[Ý[ÛˆØ[™Y]\ÈY\‚ˆXØÙ\[™ÈÚ^ÛX[ˆMLX™[Ë‚‹H]šY[˜ÙK[[Z]YXœÝ[[ÛœÈ™[XZ[ˆWØÜØNŒLÌ˜WØÜØNŒÍLØWØÜØNŒÍÌ˜ˆ[™WØÜØNÌ‚‹H™]Z[™Y]šY[˜ÙK[[Z]YÜÚ]]™\È™[XZ[ˆWØÜØNXWØÜØNŒLˆWØÜØNŒMŒWØÜØN˜[™WØÜØN˜ÈHÛX[\Ý™]Z[™Yˆ]šY[˜ÙK[[Z]YX\™Ú[ˆ\ÈŒLØ‚‹HÛÙ˜XÝÜˆÛXÞH™XÛÛ[Y[™][ÛˆXÜ›ÜÜÈ[ÛXÙ\È\Âˆ]Y]ÛÛ›WÛÜ—ÜÙ\\˜]WÜÝ˜][XÈ›È\ÝYÜÝZØÈÛÙ˜XÝÜˆ[˜[H™YXÙ\Âˆ]šY[˜ÙK[[Z]Y™]Z[™YÜÚ]]™\ÈÚ]Ý]ÜÚ[™È™]Z[™YÜÚ]]™\Ë‚‹HHÛÜÙ\Ý™[ÝËY›ÛÜˆÝ][Ù‹\ØÛÜHÛÛ›Û\ÈÝ[WØÜØNXBˆY][Y\[™[Y›Û\ÙH]ŒLÌX™[ÝÈHÛÜœ™XÝ\ÜÚ]]™H›ÛÜ‹‚‹HX™[˜XÝÜžH]MLˆLLHœ›Ûž™K]Ë\Ú[™\ˆ›Û[Ý[ÛœÈ›ÜÜÙYÎHXÝ]™BˆX\›š[™È™]šY]È›ÝÜÈ]Y]YYLY™\œØ\šX[™YØ]]™\ÈZ[™YÍÈXÝ]™Bˆ^\[X™[XÚ\Ú[Ûˆ›ÝÜÈ›Ý]Y›ÝYÚH™]šY]Ë[Û›H^ÜÛÛ\]Bˆ™\Z\‹XØ[™Y]HÝ[[X\žKš[Üš]H™\Z\ˆÝX\™˜Z[]Y]ÛÛ\]H\›ÝÂˆØØ[Y]šY[˜ÙHØ\]Y]Ù^Ü™\Z\ˆ[‹™]šY]Ë[Û›H[\Ü\ØY™]Bˆ]Y]UÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Û‹[™ŒKÌŒHØ]HÚXÚÜÂˆ\ÜÚ[™Ë‚‹HX™[˜]ÚÝ[[X\žNˆNKÌNHXØÙ\Y˜]Ú\Ë›ØÚÙ\œË\™™YØ]]™\Ëˆ™X\ˆZ\ÜÙ\Ë˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Ë[™ˆ[XÝ]™H]Y]Y\È™]Z[™YZ\ˆ[›X™[YØ[™Y]\Ë‚‹H]\ÝXØÙ\Y˜]ÚXØÙ\[˜ÙNˆˆY][Û˜[X™[ÈXØÙ\Y›ÜˆÛÝ[[™ËˆŽˆ™]šY]Ë\Ý]HXÚ\Ú[ÛœÈ[™[™ËÌÈÛÝ[X›HX™[Ë\™™YØ]]™\Ëˆ™X\ˆZ\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœË[™XÝ[Û˜X›Bˆ[‹\ØÛÜH˜Z[\™\Ë‚‹HXØÙ\YNMLY™\œ˜[]Y]ˆ[Žˆ™]šY]Ë\Ý]H›ÝÜÈ^XÚ]H™[XZ[‚ˆ›Û‹XÛÝ[X›KÚ]š[Üš]HØØ[Y]šY[˜ÙH›ÝÜÈ]Y]YÙ^ÜYÌ‚ˆ^XÚ][\›˜]H™\ÚYYK\ÜÚ][Ûˆ™\]Y\ÝËNH™]ÈML\™]šY]È™]šY]ËYXˆ›ÝÜÈÛ\ÜÚYšYY[™Y™\œ™Y[™XØÙ\Y[X™[Ý™\›\‚‹HXØÙ\YLLÝ\œ™[Ý]NˆÎHÛÝ[X›HX™[ËÌˆ™]šY]Ë\Ý]H›ÝÜÂˆ^XÚ]HY™\œ™YŒKÌŒHØ]HÚXÚÜÈ\ÜÚ[™Ë\™™YØ]]™\Ë™X\‚ˆZ\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Ëˆ[™WØÜØNŽN˜Ù\›Û‹XÛÝ[X›H\ÈHÝË\ØÛÜ™HØØ[Z[YH›Ý[™\žH›ÝË‚‹HKH™]šY]ÈÝ]NˆŒKÌŒH™]šY]ÈØ]HÚXÚÜÈ\ÜÚ[™È]XØÙ\Y™]ÂˆX™[ËÛÈH™]šY]È\È›Ý›Û[ÝYˆ™]šY]ÈXš\Ù\ÈÈÌŽH›ÝÜÈÚ]ˆ™]È›ÝÜÈWØÜØNŒLØWØÜØNŒL[™WØÜØNŒLXÈ[™[XZ[‚ˆ›Û‹XÛÝ[X›KˆÛÝ\˜ÙHØØ[[™È\È›ÝÈH›Ý[™XÚÎˆHÜ˜\^ÜÙ\ÈKÂˆKPÔÐH™XÛÜ™Ë[™^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆ\Y˜XÝÈ›ÝÈ›ÝšYHBˆ™]šY]Ë[Û›H[šT›ÝÐ‹ÔÝÚ\ÜËT›Ý]Ú]Ì›Û‹XÛÝ[X›HØ[\HØ[™Y]\Ë‚‹HÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]Ý]Nˆ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]Ù]˜[ÌLšœÛÛ˜ˆ[™\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÙ\Ý[˜ÙWÚÛÝ]Ù]˜[ÌLKšœÛÛ˜]˜[X]HBˆXØÙ\YÛÝ[X›H™YÚ\ÝžH[™\ˆ™X[S\Ù\\ÌˆÙ\]Y[˜ÙHÛ\Ý\š[™È\ÈBˆ™]Z[™Y›ÞHšY[Ëˆ›ÝÛÛ^È]˜[X]HÎX™[Y™]šY]˜[›ÝÜËˆÛÝ™\ˆ[ÎÚ]Ù\]Y[˜ÙH]šY[˜ÙKÛ\Ý\ˆÌÎÙ\]Y[˜ÙH™XÛÜ™È]Ì	BˆY[]H[™	HÛÝ™\˜YÙK[™ÛÝ]LÍˆ›ÝÜÈžHÚÛHÙ\]Y[˜ÙHÛ\Ý\œË‚ˆX^ØœÙ\™Y˜Z[‹Ý\ÝY[]H\ÈŒŽÛÈHLÌ	H\™Ù]\ÈXÚY]™Y‚ˆ[[Ý]Y]šXÜÈ\™H[‹\ØÛÜH›ÝÜËÈ]˜[XX›H[‹\ØÛÜH›ÝÜËL‚ˆÝ][Ù‹\ØÛÜH›ÝÜË[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœË[™ˆ[[Ý]]˜[XX›HÜHXØÝ\˜XÞKÜÈ™]Z[™YXØÝ\˜XÞK[™™][[ÛˆÙ‚ˆKŒˆ›ÛÙYZËÕK\ØÛÜ™HÛ\Ý\š[™È\ÈÝ[›ÝÛÛ\]Y‚‹H^\›˜[˜XÚÙ[™Ù\]Y[˜ÙK\ÙX\˜ÚÝ]N‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜\È™X[ˆS\Ù\\Ìˆ]šY[˜ÙH›ÜˆH^\Ý[™ÈÌ\›ÝÈ[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[\Kˆ]ˆ\Ù\ÈHXØÙ\Y\™Y™\™[˜ÙHTÕKY\š]™YÚYXØ\ˆ\È™]ÚY^\›˜[ˆÙ\]Y[˜Ù\ËÛÝ™\œÈÌÌÌ^\›˜[›ÝÜÈ[™ÌÍHÝ\œ™[™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœËˆ™\Ù\™\Èˆ^XÝ\™Y™\™[˜ÙHÛÝ]Ë™XÛÜ™ÈŽ›Ë\ÚYÛ˜[›ÝÜËˆ™X\‹Y\XØ]H›ÝÜË˜Z[\™\Ë[™™[[Ý™\ÈH›Ý[™YÝ\œ™[\™Y™\™[˜ÙBˆÛÛ\]K\ÙX\˜Ú›ØÚÙ\ˆÛ›H›ÜˆHŽ›Ë\ÚYÛ˜[›ÝÜËˆ]Ù\È›Ý[‚ˆ[šT™Y‹]ÚYHÙX\˜ÚÜˆ›ÛÙYZËÕK\ØÛÜ™K[™›È^\›˜[›ÝÈ\ÈÛÝ[X›HÜ‚ˆ[\Ü\™XYK‚‹HX\›™Y™\™\Ù[][ÛˆÝ]Nˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜ˆÛÛ\]\ÈHL‹\›ÝÈTÓKLˆØ[\H›Üˆ^\›˜[X\YÛÛ›ÛÈÚ]ˆ[X™Y[™×Ø˜XÚÙ[™Ø]˜Z[X›O]YX™XÝÜˆ[Y[œÚ[ÛˆÌŒ[X™Y[™Âˆ˜Z[\™\ËÈ™\™\Ù[][Û‹[™X\‹Y\XØ]HÛÝ]ËLˆX\›™Y]œËZ]\š\ÝXÂˆ\ØYÜ™Y[Y[›ÝÜË[™ÛÝ[X›KÚ[\Ü\™XYH›ÝÜËˆH]Y]ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WØ]Y]ÌLKšœÛÛ˜ˆ\ÈÝX\™˜Z[XÛX[‹ˆ\È\È[Ý\š[Üš]H]šY[˜ÙHÛ›NÈÙ\]Y[˜ÙHÙX\˜ÚˆXÝ]™K\Ú]HÛÝ\˜Ú[™Ë™]šY]ÈXÚ\Ú[ÛœË[™[˜XÝÜžHØ]\È™[XZ[‚ˆ™\]Z\™Y™Y›Ü™H[žH[\Ü‚‹H[Ý™\™\Ù[][ÛˆÝ]N‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜ˆÛÛ\]\ÈTÓKLˆ[X™Y[™ÜÈ›Üˆ[LÙ[XÝY[ÝØ[™Y]\Ë\È™XÝÜ‚ˆ[Y[œÚ[ÛˆÌŒ[X™Y[™È˜Z[\™\ËHÛÛ\]HX\›™Y\™\™\Ù[][Û‚ˆ›ÝÜËH™\™\Ù[][Û‹[™X\‹Y\XØ]HÛÝ]
MLŒØÈ™Y™\™[˜ÙBˆNU•Ì˜]ÛÜÚ[™HŽMÌÌX
KÌ™Y™\™[˜ÙHZ\œË[™ÛÝ[X›KÚ[\Ü\™XYBˆ›ÝÜËˆH™Yœ™\ÚY[ÝÜÜÚY\œÈ›ÝÈ]XÚ™\™\Ù[][Ûˆ›ÝÜÈÈ[LˆÙ[XÝYØ[™Y]\ËÙY\È^XÚ]XXÝ]™K\Ú]H]šY[˜ÙH›ØÚÙ\œË[™ÙY\ˆ]™\žHÙ[XÝYØ[™Y]H›ØÚÙY™Y›Ü™H[\Ü‚‹HLH™\™\Ù[][ÛˆÝ]N‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ù\ÛL—ÝÌ×ÍLWÝ\LÜØ[\WÌLKšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ù\ÛL—ÝÌ×ÍLWÝ\LÜØ[\WÌLKšœÛÛ˜ˆ][\˜XÙX›ÛÚËÙ\ÛL—ÝÌ×ÍLWÕTL[ˆØØ[[Û›H[ÙHY\ˆH›Ý[™YˆMLH™X\ÚXš[]H[‹ˆHLH[Ù[\ÈÝ[›ÝØXÚY[™H[š\›Û›Y[ˆYÛ›HX›Ý]ËŒˆÚPˆœ™YH›ÜˆH‹ŒHÐˆ™[[ÝHÙZYÚš[HÚ]ÔK[Û›Bˆ[™™\™[˜ÙKÛÈHÚYXØ\œÈ\ÙHHØXÚY˜XÙX›ÛÚËÙ\ÛL—ÝÌÌMLWÕTLˆ˜XÚÙ[™\ÈH\™Ù\Ý™X\ÚX›HXÝX[[Ù[ˆX\YÛÛ›ÛÈ›ÝÈ]™HL‚ˆ™]šY]Ë[Û›HY[Y[œÚ[Û˜[›ÝÜË[X™Y[™È˜Z[\™\ËÈ™\™\Ù[][Û‚ˆ™X\‹Y\XØ]HÛÝ]Ë[™LˆX\›™Y]œËZ]\š\ÝXÈ\ØYÜ™Y[Y[ÎÈÙ[XÝYˆ[Ý›ÝÜÈ›ÝÈ]™HL™]šY]Ë[Û›H›ÝÜË[X™Y[™È˜Z[\™\Ëˆ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]Ë[™LX\›™Y]œËZ]\š\ÝXÂˆ\ØYÜ™Y[Y[ËˆZ\ˆZ\™YK]œË[\™Ù\ˆÝXš[]H]Y]È™\Üˆ˜[˜XÚ×ØÚ[™ÙY™[XZ[ˆ™]šY]Ë[Û›K[™ÙY\ÛÝ[X›HÜˆ[\Ü\™XYBˆ›ÝÜË‚‹HÌHÜÝX˜]Ú™]šY]ÈÝ\™˜XÙNˆ[MH[›X™[YØ[™Y]\È\™H™]Z[™Y[ˆBˆŒË\›ÝÈXÝ]™K[X\›š[™È]Y]YNÈMH^\[X™[XÚ\Ú[Ûˆ›ÝÜÈ\™H^ÜY\Âˆ™]šY]Ë[Û›H›ËYXÚ\Ú[Ûˆ][\ÎÈHš[Üš]HØØ[Y]šY[˜ÙH[™\È\™H]Y]Yˆ[™^ÜYÚ]ÛÝ[X›HØ[™Y]\ÎÈ[\›˜]H™\ÚYYK\ÜÚ][Û‚ˆ™\]Y\ÝÈ\™H^XÚ]È™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Ú[™\È™[XZ[‚ˆ›Û‹XÛÝ[X›NÈHØØ[[™Ë\]X[]H]Y]Û\ÜÚYšY\È[™]È™]šY]ËYXˆ›ÝÜÈ[™X]™\È[˜Û\ÜÚYšYY‚‹HÌH\ØÛÝ™\žHÛÛ›ÛÎˆHYXÚ[š\ÛHÛÛÙÞHØ\]Y]™XÛÜ™ÈLŒBˆ™]šY]Ë[Û›HØÛÜK\™\ÜÝ\™H›ÝÜËHX\›™Y\™]šY]˜[X[šY™\ÝÝYÙ\ÈMŽˆ[YÚX›H›ÝÜÈÚ]H]\š\ÝXÈ˜\Ù[[™H\ÈÛÛ›Û[™BˆÙ\]Y[˜ÙK\Ú[Z[\š]H˜Z[\™K\Ù]]Y]ÙY\Èˆ\XØ]HÛ\Ý\œÈ\Âˆ›Û‹XÛÝ[X›HÛÛ›ÛË‚‹H\ÝÜšXØ[XØÙ\YMÌ™\Z\ˆÛÛ^™[XZ[œÈ™[ÝÈ™XØ]\ÙHHÌH™\Z\‚ˆ\Y˜XÝÈZ[ÛˆÜÙHØ[YH™]šY]Ë[Û›H[™\Ë‚‹HÌÜÝX˜]ÚXÝ]™K[X\›š[™È]Y]YNˆ[Íˆ[›X™[YØ[™Y]\È\™Bˆ™]Z[™YÈ›È[›X™[Y›ÝÜÈ\™HÛZ]YžHH]Y]YH[Z]ˆH]Y]YH›ÝÂˆ[˜ÛY\È™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÝ˜[YX[™˜[šÜÈNÚ[˜\ÙHÜˆUˆÜÜÜž[]˜[œÙ™\ˆ›ÝÜÈÚ]Y›Û\ÙHÜ]È›Üˆ^\™]šY]Ë‚‹HÌ^\[X™[XÚ\Ú[Ûˆ™]šY]È^Üˆ[ÍˆXÝ]™K\]Y]YBˆ^\ÛX™[ÙXÚ\Ú[Û—Û™YYY›ÝÜÈ\™H^ÜY\È›×ÙXÚ\Ú[Û˜\™BˆÛÝ[X›HØ[™Y]\ËMˆØ\œšYY™]šY]ËYX›ÝÜÈ[™Œ™]È™]šY]ËYX›ÝÜÂˆ\™H[šÙY[™HÈ™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Ú[™\È\™H[™XYHÛÝ™\™YžBˆHYXØ]YZ\ÛX]Ú^Üˆš\ÚÈ›YÜÈ[˜ÛYHLÛÙ˜XÝÜ‹Y˜[Z[Bˆ[XšYÝZ]H›ÝÜËŽHÛÝ[\™]šY[˜ÙKX›Ý[™\žH›ÝÜËMXÝ]™K\Ú]BˆX\[™ËÜÝXÝ\™KYØ\›ÝÜËH^[XZØYÙKÛ›Û›ØØ[Y]šY[˜ÙHš\ÚÜËÂˆ™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Ú\ËÈÝXœÝ˜]KXÛ\ÜÈ›Ý[™\šY\ËˆÚX›[™ÂˆYXÚ[š\ÛHÛÛ™\Ú[ÛœË[™ˆÙ\‹R\ËÛY][X›Ý[™\žH›ÝÜË‚‹HÌ^\[X™[™\Z\ˆØ[™Y]\Î‚ˆ\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ØØ[™Y]\×ÍÌšœÛÛ˜˜[šÜÈÌˆ™]šY]Ë[Û›H™\Z\ˆØ[™Y]\È[™XÚÙ]È[Íˆ›ÝÜÈ\ÈMXÝ]™K\Ú]BˆX\[™ËÜÝXÝ\™KYØ\™\Z\œËÈ^[XZØYÙKÛ›Û›ØØ[Y]šY[˜ÙHÝX\™˜Z[ËˆÌÛÙ˜XÝÜ‹Y]šY[˜ÙH™\Z\œËHÙ\‹R\ËÛY][X›Ý[™\žH™]šY]ËHÚX›[™ÂˆYXÚ[š\ÛKX›Ý[™\žH™]šY]Ë[™ŒÈ^\›˜[^\[X™[XÚ\Ú[ÛœË‚‹HÌ^\[X™[™\Z\ˆÝX\™˜Z[]Y]ˆŒHš[Üš]H™\Z\ˆ›ÝÜÈ™[XZ[‚ˆ›Û‹XÛÝ[X›K[˜ÛY[™ÈMXÝ]™K\Ú]HX\[™ËÜÝXÝ\™KYØ\›ÝÜÈ[™Bˆ^[XZØYÙKÛ›Û›ØØ[Y]šY[˜ÙH›ÝÜËˆ™YHÛÛœÙ\˜]]™K\™[X\ØØ[^XÝYˆ˜[Z[H]šY[˜ÙHXYÈ
WØÜØNMÍØWØÜØNNL˜[™WØÜØNX
H™[XZ[‚ˆ™]šY]Ë[Û›KÚ]ÛÝ[X›HX™[Ø[™Y]\Ë‚‹HÌYXÚ[š\ÛHÛÛÙÞHØ\]Y]ˆLMH›Û‹XÛÝ[X›HØÛÜK\™\ÜÝ\™H›ÝÜÂˆ^ÜÙH˜[œÙ™\˜\ÙHÜÜÜž[X\ÙK\ÛÛY\˜\ÙKÞYÜ™YXÝ\ÙHÛ™Ë]Z[ˆY][]˜[œÙ™\‹[™ÛXØ[ˆÚ[Z\ÝžH™\ÜÝ\™HÚ]Ý]Ü™X][™ÈH™]ÂˆÛÛÙÞH˜[Z[Hœ›ÛHÙ^]ÛÜ™]šY[˜ÙH[Û™K‚‹HÌX\›™Y™]šY]˜[X[šY™\ÝˆMŒˆ[YÚX›HX™[Y[šY\È\™HÝYÙY›ÜˆBˆ]\™HX\›™Y\™\™\Ù[][Ûˆ]Ú]MŒ[Z]Y›ÝÜÈ[™HÝ\œ™[ˆ]\š\ÝXÈÙ[ÛY]žH™]šY]˜[™\Ù\™Y\ÈH™\]Z\™YÛÛ›Û‚‹HÌÙ\]Y[˜ÙK\Ú[Z[\š]H˜Z[\™K\Ù]]Y]ˆˆ^XÝ\™Y™\™[˜ÙH\XØ]BˆÛ\Ý\œÈ\™HÙ\\È›Û‹XÛÝ[X›HÛÛ›ÛÈ™Y›Ü™H[žH˜[Z[H›ÜYØ][ÛˆÜ‚ˆX\›™Y\™]šY]˜[Ü]‚‹H™]šY]ÈXÝ[[X\žNˆH]šY[˜ÙKYØ\›ÝÜË[™YY×Û[Ü™WÙ]šY[˜ÙXÚ]ˆŒHØ\œšYY›ÝÜÈ[™Œ™]È›ÝÜËˆ™]ËYX™^XÝ[ÛœÈ\™HMˆ[\›˜]BˆÝXÝ\™KØÛÙ˜XÝÜ‹\ÛÝ\˜ÙH[œÜXÝ[ÛœËˆ^\\™]šY]ÈXÚ\Ú[ÛœËH˜[Z[Bˆ›Ý[™\žH™]šY]Ë[™HØØ[ÛÙ˜XÝÜ‹ØXÝ]™K\Ú]HX\[™ÈÚXÚË‚‹HÌØØ[[™Ë\]X[]H]Y]ˆŒ™]È™]šY]ËYX›ÝÜÈÛ\ÜÚYšYYXØÙ\YˆX™[ÈÚ]™]šY]ÈX\™™YØ]]™\Ë™X\ˆZ\ÜÙ\Ë™X\‹Y\XØ]Bˆ]ËØœÙ\™YÛÛÙÞHØÛÜH™\ÜÝ\™K˜[Z[K\›ÜYØ][Ûˆ›Ý[™\žKˆÛÙ˜XÝÜˆ[XšYÝZ]K™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚXÝ]™K\Ú]HX\[™ÈØ\ËˆXÝ]™K[X\›š[™È]Y]YHÛÛ˜Ù[˜][Û‹[™[\›˜]K\ÝXÝ\™H]ÈXÚÚ[™ÂˆØØ[Ý\Ü‚‹HÌ™[YYX][Ûˆ[Žˆ[Œ™]ÈX›ÝÜÈ]™HØ\]Z[Ü˜\ÛÛ^ˆÙ[XÝYÙ[ÛY]žHÛÛ^[™H™\Z\ˆXÚÙ]ˆXÚÙ]È\™HL‚ˆ[\›˜]KTˆYØ[™ØØ[œËÈ^\›˜[ÛÙ˜XÝÜ‹\ÛÝ\˜ÙH™]šY]ÜËHXÝ]™K\Ú]BˆX\[™È™\Z\‹HØØ[X\[™ËÜÝXÝ\™K\Ù[XÝ[Ûˆ™]šY]ËH˜[Z[KX›Ý[™\žBˆ™]šY]Ë[™ˆ^\X™[XÚ\Ú[ÛœË‚‹HÌ[X™[YYX][Ûˆ[Žˆ[H™]šY]ËYX›ÝÜÈ\™HX\YˆXÚÙ]Âˆ\™HÍÈ[\›˜]KTˆYØ[™ØØ[œËHØØ[X\[™ËÜÝXÝ\™K\Ù[XÝ[Û‚ˆ™]šY]ÜËH^\›˜[ÛÙ˜XÝÜ‹\ÛÝ\˜ÙH™]šY]ÜËÈ˜[Z[KX›Ý[™\žH™]šY]ÜËˆMˆ^\X™[XÚ\Ú[ÛœË[™ÈXÝ]™K\Ú]HX\[™È™\Z\œËˆÚ^K[š[™Bˆ›ÝÜÈ]™H[\›˜]HœÈ][\›˜]KTˆKPÔÐH™\ÚYYK\ÜÚ][ÛˆÝ\Ü‚‹HÌ›ØÝ\ÙY[\›˜]K\ÝXÝ\™HØØ[ŽˆLÈÝXÝ\™K\ØØ[ˆ›ÝÜËMLˆØ[™Y]BˆˆÝXÝ\™\Ë™]Ú˜Z[\™\ËŒÈ[\›˜]KTˆÝXÝ\™\ÈÚ]ˆÛÛœÙ\˜]]™H™[X\YXÝ]™K\Ú]HÜÚ][ÛœËÈÝXÝ\™K]ÚYBˆ^XÝYY˜[Z[H]›ÝÜÈ
WØÜØNÎXWØÜØNŽM˜WØÜØNŽN
K[™ˆØØ[XÝ]™K\Ú]H^XÝYY˜[Z[H]›ÝÜËˆ\ÙH]È™[XZ[ˆ™]šY]Ë[Û›Bˆ]šY[˜ÙK‚‹HÌ[YX›Ý[™Y[\›˜]K\ÝXÝ\™HØØ[ŽˆˆØØ[‹XØ[™Y]H™]šY]ËYXˆ›ÝÜË[ÌÎHØ[™Y]HˆÝXÝ\™\ÈØØ[›™Y™]Ú˜Z[\™\ËÍŒ‚ˆ[\›˜]KTˆÝXÝ\™\ÈÚ]ÛÛœÙ\˜]]™H™[X\YXÝ]™K\Ú]HÜÚ][ÛœËˆNH^XÝYY˜[Z[H]›ÝÜË[™È™]šY]Ë[Û›HØØ[^XÝYY˜[Z[H]ˆ›ÝÜÈœ›ÛH™[X\È
WØÜØNMÍØWØÜØNNL˜WØÜØNX
KˆH™[X\XYˆÝ[[X\žH™XÛÜ™È™]šY]Ë[Û›HXYÈ[™ÛÝ[X›HX™[Ø[™Y]\Ë‚‹HÌ™[X\[ØØ[]Y]ˆWØÜØNMÍØ[™WØÜØNX™\]Z\™H^\ˆ˜[Z[KX›Ý[™\žH™]šY]ËWØÜØNNL˜™\]Z\™\È^\™XXÝ[Û‹ÜÝXœÝ˜]H™]šY]Ëˆ[™YH™\]Z\™HÝšXÝ™[X\ÝX\™˜Z[Ë[™\™H\™HÝXÝ\™K\Ù[XÝ[Û‚ˆØ[™Y]\ÈY\ˆ™XXÝ[ÛˆZ\ÛX]ÚšXYÙK‚‹HÌ™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Ú]Y]ˆNXÝ]™K\]Y]YHY›Û\ÙK]ÜH›ÝÜÂˆÚ]Ú[˜\ÙHÜˆUÜÜÜž[]˜[œÙ™\ˆ^\™H›Ý]YÈ^\ˆ™XXÝ[Û‹ÜÝXœÝ˜]H™]šY]ÎÈ\™HÛÝ[X›K‚‹HÌ˜[Z[K\›ÜYØ][ÛˆÝX\™˜Z[È›ÝÈ›ØÚÈ™\ÜY›ÝÜÈÚ]ˆ™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]Ú™Y›Ü™H›ÜYØ][ÛˆÜˆÛÝ[X›H›Û[Ý[ÛŽÂˆMÙˆÜÙH›ÝÜÈ\™H™]Z[™YžHHš[Üš]HÝ™\œšYH™^[Û™X^Ü›ÝÜØ‚‹HÌ™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Ú™]šY]È^Üˆ[˜[Z[KYÝX\™˜Z[[™\Âˆ\™H^ÜYÙÙ]\‹Ü][ÈMÈÝ\œ™[Ý][Ù‹\ØÛÜHX™[È[™Âˆ[›X™[Y[™[™Ë\™]šY]È›ÝÜËˆH^Ü™XÛÜ™ÈX™[YÙYYZ\ÛX]Ú\Ëˆ[™›ÝÈÝ\Y\ÈH^\\™]šY]ÙY™\ÜÝ\™HÝ\™˜XÙH›ÜˆHTËTÒÒKˆUYÜ˜\ÜÒÓ’Ë‘ËšÐKšÐ‹[™ÒTÛÛÙÞH^[œÚ[Û‹ˆBˆ^[œÚ[Ûˆ\Y˜XÝX\ÈŒÝ\ÜY[™\ÈXÜ›ÜÜÈ[š[™H˜[Z[Y\Ë™XÛÜ™Âˆ›Û‹]\™Ù][È[™[œÝ\ÜY˜[Z[HX\[™ÜË[™ÙY\ÂˆÛÝ[X›WÛX™[ØØ[™Y]WØÛÝ[Lˆ]ÈÝ\œ™[™]šY]Ë[Û›HXÚ\Ú[Ûˆ˜]Úˆ›Ý]\ÈHÈ[›X™[Y›ÝÜÈÈ™]šY]ÙYÝ][Ù‹\ØÛÜH™\Z\ˆXÚ\Ú[ÛœËˆ™Z™XÝÈMÈÝ\œ™[ÛÛ›ÛË[™YÈÛÝ[X›HX™[Ë‚‹HÝXÝ\™HX\[™ÎˆNHÝ[X\[™È\ÜÝY\È]Ì‚‹HØØ[\™›Ü›X[˜ÙHØ\È™YÙ[™\˜]YÛˆÌ\Y˜XÝÈ[ˆ\Y˜XÝËÜ\™—Ü™\ÜšœÛÛ˜‚‚ˆÈÈÝ\œ™[ÛÛ™šY[˜ÙHØ[‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLMŽŒÌŽŒMÖˆ[Ž‚‚‹HKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ›ËˆHØ[›ÛšXØ[™YÚ\ÝžH™[XZ[œÈÎHÛÝ[X›Bˆœ›Ûž™HX™[ËHKH™]šY]ÈÝ[YÈÛX[ˆÛÝ[X›HX™[Ë[™BˆÛÝ\˜ÙK\ØØ[H]Y]Ý[^ÜÙ\ÈÛ›HKÈKPÔÐHÛÝ\˜ÙH™XÛÜ™Ë‚‹H^\›˜[\ÛÝ\˜ÙH™\Z\‹Ú[\ÜˆY\È›Üˆ›Ý[™Y™\Z\‹Ü™XY[™\ÜÈ]šY[˜ÙK›Âˆ›ÜˆÛÝ[X›H[\Üˆ^\›˜[›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›H[™›Û‹XÛÝ[X›NÈBˆ™]È™X[Ù\]Y[˜ÙHÛÝ][™™\™\Ù[][ÛˆÚYXØ\œÈ™[[Ý™H™XY[™\ÜÂˆ›ØÚÙ\œË]XÝ]™K\Ú]HÛÝ\˜ÙHXÚ\Ú[ÛœËÛÛ\]HÙ\]Y[˜ÙHÙX\˜Ú™]šY]ÂˆXÚ\Ú[ÛœË[™[X™[Y˜XÝÜžHØ]\ÈÝ[›ØÚÈ[\Ü‚‹HØÚY[YšXÈÙ[™\˜[^˜][ÛˆÛÜšÎˆY\ËˆS\Ù\\ÌˆÙ\]Y[˜ÙHÛ\Ý\š[™È›ÝÈ›ÝšY\ÂˆH™X[LÌ	HÙ\]Y[˜ÙKZY[]HÛÝ]›ÜˆHXØÙ\Y™YÚ\ÝžHÚ]X^ˆ˜Z[‹Ý\ÝY[]HŒŽ[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËˆ[™[›™Y[[Ý]Ú[‹Y\ÝšX][ÛˆY]šXÜËˆ›ÛÙYZËÕK\ØÛÜ™HÙ\\˜][Ûˆ\ÂˆÝ[Ü[‹]HÛÛÜ™[˜]H›ØÚÙ\ˆ\È˜\œ›ÝÙYžHH™]šY]Ë[Û›H™XY[™\ÜÂˆ\Y˜XÝ]ÝYÙ\ÈHÙ[XÝYˆ[PÒQˆš[\È[™™XÛÜ™ÈH™[XZ[š[™ÂˆZ\ÜÚ[™ËÝ[œÝYÙYÛÛÜ™[˜]HÝ\™˜XÙK‚‹HÔÑˆ\™[š[™ÈÛÜšÎˆY\Ë]Û›H›Üˆ˜[YY›ØÚÙ\œËˆ\È[ˆÜ]ˆYXÚ[š\ÛK]^ÛÝ[\™]šY[˜ÙH[ÈÝXÝ\™KÛØØ[™\œÝ\È™]šY]ËXÛÛ^ˆØ]YÛÜšY\ËYYH^\™[[Ý˜[X›][Û‹[™™XÛÜ™YÝXÝ\™KÛØØ[ˆÝX\™˜Z[ÜÜÙ\ÎÈHLH™\™\Ù[][Ûˆ]\È[\[Y[Y]›ØÚÙYžBˆ[˜ØXÚYØØ[[Ù[ÙZYÚË‚‚ˆÈÈÝ\ÛÛ[X[™Â‚˜˜\Ú™Ú]™]ÚÜšYÚ[‚™Ú][KY™‹[Û›HÜšYÚ[ˆXZ[‚™Ú]Ý]\È\Ø‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]]ÛX][Û‹[ØÚÈK[ØÚËY\ˆ™Ú]ØØ][]XËYX\X]]ÛX][Û‹›ØÚÈÝ]\Â”UÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝÂ”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]B”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHÝ[[X\š^™KYÙ[ÛY]žK\ÛXÙ\ÈKX\Y˜XÝY\ˆ\Y˜XÝÈK[Ý]\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÜÛXÙWÜÝ[[X\žKšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[[X™[Y^[œÚ[Û‹XØ[™Y]\ÈKYÙ[ÛY]žH\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÍÌšœÛÛˆK\™]šY]˜[\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÜ™]šY]˜[ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×ÛX™[Ù^[œÚ[Û—ØØ[™Y]\×ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[Y˜[Z[K\›ÜYØ][Û‹YÝX\™˜Z[ÈKYÙ[ÛY]žH\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÍÌšœÛÛˆK\™]šY]˜[\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÜ™]šY]˜[ÍÌšœÛÛˆK[X™[È]KÜ™YÚ\ÝšY\ËØÝ\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù˜[Z[WÜ›ÜYØ][Û—ÙÝX\™˜Z[×ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[Y˜[Z[K\›ÜYØ][Û‹YÝX\™˜Z[ÈKYÙ[ÛY]žH\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÍÌšœÛÛˆK\™]šY]˜[\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÜ™]šY]˜[ÍÌšœÛÛˆK[X™[È\Y˜XÝËÝŒ×ØÛÝ[X›WÛX™[×Ø˜]ÚÍÍKšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù˜[Z[WÜ›ÜYØ][Û—ÙÝX\™˜Z[×ÍÌÜ™]šY]×Ø˜]ÚšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHÝ[[X\š^™K\™]šY]ËYXK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌšœÛÛˆKXXÝ]™K[X\›š[™Ë\]Y]YH\Y˜XÝËÝŒ×ØXÝ]™WÛX\›š[™×Ü™]šY]×Ü]Y]YWÍÌšœÛÛˆKX˜\Ù[[™K\™]šY]ËYX\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍÍKšœÛÛˆK[X^\›ÝÜÈHK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH[˜[^™K\™]šY]ËYX\™[YYX][ÛˆK\™]šY]ËYX\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍÌšœÛÛˆK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌšœÛÛˆKYÜ˜\\Y˜XÝËÝŒWÙÜ˜\ÍÌšœÛÛˆKYÙ[ÛY]žH\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÍÌšœÛÛˆKYX\Ý]\È™]ÈK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH[˜[^™K\™]šY]ËYX\™[YYX][ÛˆK\™]šY]ËYX\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍÌšœÛÛˆK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌšœÛÛˆKYÜ˜\\Y˜XÝËÝŒWÙÜ˜\ÍÌšœÛÛˆKYÙ[ÛY]žH\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÍÌšœÛÛˆKYX\Ý]\È[K[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌØ[šœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHØØ[‹\™]šY]ËYXX[\›˜]K\ÝXÝ\™\ÈK\™[YYX][Ûˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌšœÛÛˆK[X^Y[šY\ÈLÈK[X^\ÝXÝ\™\Ë\\‹Y[žHŒK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXØ[\›˜]WÜÝXÝ\™WÜØØ[—ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHØØ[‹\™]šY]ËYXX[\›˜]K\ÝXÝ\™\ÈK\™[YYX][Ûˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌØ[šœÛÛˆK[X^Y[šY\ÈˆK[X^\ÝXÝ\™\Ë\\‹Y[žHK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXØ[\›˜]WÜÝXÝ\™WÜØØ[—ÍÌØ[Ø›Ý[™YšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHÝ[[X\š^™K\™]šY]ËYX\™[X\[XYÈKX[\›˜]K\ÝXÝ\™K\ØØ[ˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXØ[\›˜]WÜÝXÝ\™WÜØØ[—ÍÌØ[Ø›Ý[™YšœÛÛˆK\™[YYX][Ûˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌØ[šœÛÛˆK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[X\ÛXY×ÍÌØ[Ø›Ý[™YšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y]\™]šY]ËYX\™[X\[ØØ[[XYÈK\™[X\[XYÈ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[X\ÛXY×ÍÌØ[Ø›Ý[™YšœÛÛˆK\™[YYX][Ûˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌØ[šœÛÛˆK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[X\ÛØØ[ÛXYØ]Y]ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y]\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]Ú\ÈK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌšœÛÛˆKXXÝ]™K[X\›š[™Ë\]Y]YH\Y˜XÝËÝŒ×ØXÝ]™WÛX\›š[™×Ü™]šY]×Ü]Y]YWÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚØ]Y]ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]Ú\™]šY]ËY^ÜK\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]ÚX]Y]\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚØ]Y]ÍÌšœÛÛˆKY˜[Z[K\›ÜYØ][Û‹YÝX\™˜Z[È\Y˜XÝËÝŒ×Ù˜[Z[WÜ›ÜYØ][Û—ÙÝX\™˜Z[×ÍÌšœÛÛˆK[X™[È]KÜ™YÚ\ÝšY\ËØÝ\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÜ™]šY]×Ù^ÜÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[\™]šY]ËYXÚ\Ú[Û‹X˜]ÚK\™]šY]È\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÜ™]šY]×Ù^ÜÍÌšœÛÛˆKX˜]ÚZYÌÜ™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÜ™]šY]ÈK\™]šY]Ù\ˆ]]ÛX][Û—ÛX™[Ù˜XÝÜžHK[Ý]\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÙXÚ\Ú[Û—Ø˜]ÚÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y]Y^\[X™[YXÚ\Ú[Û‹\™\Z\‹YÝX\™˜Z[ÈKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹XØ[™Y]\È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ØØ[™Y]\×ÍÌØ[šœÛÛˆK\™[X\[ØØ[[XYX]Y]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[X\ÛØØ[ÛXYØ]Y]ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ÙÝX\™˜Z[Ø]Y]ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y]Y^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\ÈKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹YÝX\™˜Z[X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ÙÝX\™˜Z[Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹XØ[™Y]\È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ØØ[™Y]\×ÍÌØ[šœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[Y^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™]šY]ËY^ÜKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛˆK[X™[È]KÜ™YÚ\ÝšY\ËØÝ\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]×Ù^ÜÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[\™]šY]ËYXÚ\Ú[Û‹X˜]ÚK\™]šY]È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]×Ù^ÜÍÌšœÛÛˆKX˜]ÚZYÌÙ^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]ÈK\™]šY]Ù\ˆ]]ÛX][Û—ÛX™[Ù˜XÝÜžHK[Ý]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙXÚ\Ú[Û—Ø˜]ÚÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHÝ[[X\š^™KY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™\Z\‹\[ˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]×Ù^ÜÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™\Z\—Ü[—ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH™\ÛÛ™KY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™\Z\‹[[™\ÈKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™\Z\‹\[ˆ\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™\Z\—Ü[—ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]×Ù^ÜÍÌšœÛÛˆK\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]Ú\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÜ™]šY]×Ù^ÜÍÌšœÛÛˆK\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]ÚYXÚ\Ú[Û‹X˜]Ú\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÙXÚ\Ú[Û—Ø˜]ÚÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™\Z\—Ü™\ÛÛ][Û—ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[Y^XÚ]X[\›˜]K\™\ÚYYK\ÜÚ][Û‹\™\]Y\ÝÈKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™\Z\‹\[ˆ\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™\Z\—Ü[—ÍÌšœÛÛˆK\™]šY]ËYX\™[YYX][Ûˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[YYX][Û—ÍÌØ[šœÛÛˆKYÜ˜\\Y˜XÝËÝŒWÙÜ˜\ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ù^XÚ]Ø[\›˜]WÜ™\ÚYYWÜÜÚ][Û—Ü™\]Y\Ý×ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y]\™]šY]Ë[Û›KZ[\Ü\ØY™]HK[X™[È]KÜ™YÚ\ÝšY\ËØÝ\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛˆK\™]šY]È\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÙXÚ\Ú[Û—Ø˜]ÚÍÌšœÛÛˆK\™]šY]È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÙXÚ\Ú[Û—Ø˜]ÚÍÌšœÛÛˆK\™]šY]È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙXÚ\Ú[Û—Ø˜]ÚÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×Ü™]šY]×ÛÛ›WÚ[\ÜÜØY™]WØ]Y]ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHÚXÚË[X™[Y˜XÝÜžKYØ]\ÈK[X™[Y˜XÝÜžKX]Y]\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWØ]Y]ÍÌšœÛÛˆKX\YY[X™[Y˜XÝÜžH\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWØ\YYÛX™[×ÍÌšœÛÛˆKXXÝ]™K[X\›š[™Ë\]Y]YH\Y˜XÝËÝŒ×ØXÝ]™WÛX\›š[™×Ü™]šY]×Ü]Y]YWÍÌšœÛÛˆKXY™\œØ\šX[[™YØ]]™\È\Y˜XÝËÝŒ×ØY™\œØ\šX[Û™YØ]]™WØÛÛ›Û×ÍÌšœÛÛˆKY^\\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\Ü™]šY]×Ù^ÜÍÌÜÜÝØ˜]ÚšœÛÛˆKY˜[Z[K\›ÜYØ][Û‹YÝX\™˜Z[È\Y˜XÝËÝŒ×Ù˜[Z[WÜ›ÜYØ][Û—ÙÝX\™˜Z[×ÍÌšœÛÛˆK\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]Ú\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÜ™]šY]×Ù^ÜÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™]šY]×Ù^ÜÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹XØ[™Y]\È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ØØ[™Y]\×ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹YÝX\™˜Z[X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ÙÝX\™˜Z[Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]×Ù^ÜÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™\Z\‹\™\ÛÛ][Ûˆ\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™\Z\—Ü™\ÛÛ][Û—ÍÌšœÛÛˆKY^XÚ]X[\›˜]K\™\ÚYYK\ÜÚ][Û‹\™\]Y\ÝÈ\Y˜XÝËÝŒ×Ù^XÚ]Ø[\›˜]WÜ™\ÚYYWÜÜÚ][Û—Ü™\]Y\Ý×ÍÌšœÛÛˆK\™]šY]Ë[Û›KZ[\Ü\ØY™]KX]Y]\Y˜XÝËÝŒ×Ü™]šY]×ÛÛ›WÚ[\ÜÜØY™]WØ]Y]ÍÌšœÛÛˆKX]\ÜÜÜž[]˜[œÙ™\‹Y˜[Z[KY^[œÚ[Ûˆ\Y˜XÝËÝŒ×Ø]ÜÜÜÜž[Ý˜[œÙ™\—Ù˜[Z[WÙ^[œÚ[Û—ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWÙØ]WØÚXÚ×ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y][YXÚ[š\ÛK[ÛÛÙÞKYØ\ÈKXXÝ]™K[X\›š[™Ë\]Y]YH\Y˜XÝËÝŒ×ØXÝ]™WÛX\›š[™×Ü™]šY]×Ü]Y]YWÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹XØ[™Y]\È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ØØ[™Y]\×ÍÌØ[šœÛÛˆKY˜[Z[K\›ÜYØ][Û‹YÝX\™˜Z[È\Y˜XÝËÝŒ×Ù˜[Z[WÜ›ÜYØ][Û—ÙÝX\™˜Z[×ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛˆK[X^\›ÝÜÈK[Ý]\Y˜XÝËÝŒ×ÛYXÚ[š\ÛWÛÛÛÙÞWÙØ\Ø]Y]ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[[X\›™Y\™]šY]˜[[X[šY™\ÝKYÙ[ÛY]žH\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÙ™X]\™\×ÍÌšœÛÛˆK\™]šY]˜[\Y˜XÝËÝŒ×ÙÙ[ÛY]žWÜ™]šY]˜[ÍÌšœÛÛˆK[X™[È]KÜ™YÚ\ÝšY\ËØÝ\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛˆK[ÛÛÙÞKYØ\X]Y]\Y˜XÝËÝŒ×ÛYXÚ[š\ÛWÛÛÛÙÞWÙØ\Ø]Y]ÍÌšœÛÛˆK[X^\›ÝÜÈMŒK[Ý]\Y˜XÝËÝŒ×ÛX\›™YÜ™]šY]˜[ÛX[šY™\ÝÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y]\Ù\]Y[˜ÙK\Ú[Z[\š]KY˜Z[\™K\Ù]ÈK\Ù\]Y[˜ÙKXÛ\Ý\œÈ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWØÛ\Ý\—Ü›ÞWÍÌšœÛÛˆK[X™[È]KÜ™YÚ\ÝšY\ËØÝ\˜]YÛYXÚ[š\ÛWÛX™[ËšœÛÛˆKXXÝ]™K[X\›š[™Ë\]Y]YH\Y˜XÝËÝŒ×ØXÝ]™WÛX\›š[™×Ü™]šY]×Ü]Y]YWÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWÜÚ[Z[\š]WÙ˜Z[\™WÜÙ]×ÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHZ[\Ù\]Y[˜ÙKXÛ\Ý\‹\›ÞHKYÜ˜\\Y˜XÝËÝŒWÙÜ˜\ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWØÛ\Ý\—Ü›ÞWÍÌšœÛÛ‚”UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH]Y][X™[\ØØ[[™Ë\]X[]HKX˜]ÚZYÌÜ™]šY]ÈKXXØÙ\[˜ÙH\Y˜XÝËÝŒ×ÛX™[Ø˜]ÚØXØÙ\[˜ÙWØÚXÚ×ÍÌÜ™]šY]ËšœÛÛˆK\™XY[™\ÜÈ\Y˜XÝËÝŒ×ÛX™[Ü™]šY]×Ü›Û[Ý[Û—Ü™XY[™\Ü×ÍÌšœÛÛˆK\™]šY]ËYX\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÍÌÜ™]šY]ËšœÛÛˆK\™]šY]ËY]šY[˜ÙKYØ\È\Y˜XÝËÝŒ×Ü™]šY]×Ù]šY[˜ÙWÙØ\×ÍÌÜ™]šY]ËšœÛÛˆKXXÝ]™K[X\›š[™Ë\]Y]YH\Y˜XÝËÝŒ×ØXÝ]™WÛX\›š[™×Ü™]šY]×Ü]Y]YWÍÌÜ™]šY]×Ø˜]ÚšœÛÛˆKY˜[Z[K\›ÜYØ][Û‹YÝX\™˜Z[È\Y˜XÝËÝŒ×Ù˜[Z[WÜ›ÜYØ][Û—ÙÝX\™˜Z[×ÍÌÜ™]šY]×Ø˜]ÚšœÛÛˆKZ\™[™YØ]]™\È\Y˜XÝËÝŒ×Ú\™Û™YØ]]™WØÛÛ›Û×ÍÌÜ™]šY]×Ø˜]ÚšœÛÛˆKYXÚ\Ú[Û‹X˜]Ú\Y˜XÝËÝŒ×Ù^\Ü™]šY]×ÙXÚ\Ú[Û—Ø˜]ÚÍÌÜ™]šY]ËšœÛÛˆK\ÝXÝ\™K[X\[™È\Y˜XÝËÝŒ×ÜÝXÝ\™WÛX\[™×Ú\ÜÝY\×ÍÌšœÛÛˆKY^\\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\Ü™]šY]×Ù^ÜÍÌÜ™]šY]×ÜÜÝØ˜]ÚšœÛÛˆK\Ù\]Y[˜ÙKXÛ\Ý\œÈ\Y˜XÝËÝŒ×ÜÙ\]Y[˜ÙWØÛ\Ý\—Ü›ÞWÍÌšœÛÛˆKX[\›˜]K\ÝXÝ\™K\ØØ[ˆ\Y˜XÝËÝŒ×Ü™]šY]×ÙXØ[\›˜]WÜÝXÝ\™WÜØØ[—ÍÌšœÛÛˆK\™[X\[ØØ[[XYX]Y]\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜ™[X\ÛØØ[ÛXYØ]Y]ÍÌšœÛÛˆK\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]ÚX]Y]\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚØ]Y]ÍÌšœÛÛˆK\™XXÝ[Û‹\ÝXœÝ˜]K[Z\ÛX]Ú\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ü™XXÝ[Û—ÜÝXœÝ˜]WÛZ\ÛX]ÚÜ™]šY]×Ù^ÜÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™]šY]×Ù^ÜÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹XØ[™Y]\È\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ØØ[™Y]\×ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹\™\Z\‹YÝX\™˜Z[X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—Ü™\Z\—ÙÝX\™˜Z[Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙKYØ\X]Y]\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\Ø]Y]ÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™]šY]ËY^Ü\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™]šY]×Ù^ÜÍÌšœÛÛˆKY^\[X™[YXÚ\Ú[Û‹[ØØ[Y]šY[˜ÙK\™\Z\‹\™\ÛÛ][Ûˆ\Y˜XÝËÝŒ×Ù^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÜ™\Z\—Ü™\ÛÛ][Û—ÍÌšœÛÛˆKY^XÚ]X[\›˜]K\™\ÚYYK\ÜÚ][Û‹\™\]Y\ÝÈ\Y˜XÝËÝŒ×Ù^XÚ]Ø[\›˜]WÜ™\ÚYYWÜÜÚ][Û—Ü™\]Y\Ý×ÍÌšœÛÛˆK\™]šY]Ë[Û›KZ[\Ü\ØY™]KX]Y]\Y˜XÝËÝŒ×Ü™]šY]×ÛÛ›WÚ[\ÜÜØY™]WØ]Y]ÍÌšœÛÛˆKX]\ÜÜÜž[]˜[œÙ™\‹Y˜[Z[KY^[œÚ[Ûˆ\Y˜XÝËÝŒ×Ø]ÜÜÜÜž[Ý˜[œÙ™\—Ù˜[Z[WÙ^[œÚ[Û—ÍÌšœÛÛˆK[Ý]\Y˜XÝËÝŒ×ÛX™[ÜØØ[[™×Ü]X[]WØ]Y]ÍÌÜ™]šY]ËšœÛÛ‚˜‚ˆÈÈ™^YÙ[Ý\\™B‚•\Ù\‹X\›Ý™Yš[Üš]HÝ™\œšYNˆÈ›ÝÙY\Y[™ÈØ]\È\ÛˆØ]\Ëˆ]™\žH™]Â˜\Y˜XÝ]Y]ÜˆØ]H]\Ý\™XÝH™[[Ý™HÛ™H˜[YYÔÑ‹Ù[™\˜[^˜][Û‹Ü‚™^\›˜[\[Ý›ØÚÙ\ŽÈÝ\Ú\ÙHÈ›ÝZ[]‚‚“]\Ý[ˆØ\È\™XÝÛ›KÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆÈ›ÝÜ[ˆ[›Ý\‚“KPÔÐK[Û›H˜[˜ÚKˆÈ›ÝÛZ[H[K\ØÛÜ™HÛÝ]‚‚•HXÝ]™H›ÛÙYZÈ]\È›ÝÈÛ\Ý\‹Yš\œÝ›Ý›[™Ú[šÈÛÛ[X][Û‹‚•\È[ˆYYZ[Y›ÛÙYZË]K\ØÛÜ™KXÛ\Ý\‹Yš\œÝ\Ü][™[›™Y˜Û\Ý\‹Yš\œÝ\Y˜XÝÎ‚˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]ÌLšœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]šœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü]Y\žWÜÝX˜Ú[š×Ì—ÛÙ—ÌLL‹šœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™—ÌLšœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™‹šœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™—Ü]Y\žWÜÝX˜Ú[š×Ì—ÛÙ—ÌLL‹šœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™—Ü]Y\žWÜÝX˜Ú[š×Ì×ÛÙ—ÌLL‹šœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™—Ü]Y\žWÜÝX˜Ú[š×ØYÙÜ™YØ]WÌ—Ì×ÛÙ—ÌLL‹šœÛÛ˜˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™×ÌLšœÛÛ˜[™˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ËšœÛÛ˜‚‚•Hš\œÝÛ\Ý\‹Yš\œÝØ[™Y]H\Ù\ÈHÌˆÝYÙYX]\šX[^˜X›HÝXÝ\™\Â˜\ÈHÝXÝ\™H[™^[™›ÛÈ^\Ý[™ÈHHØ]šY[˜ÙH[Èœ\][ÛˆÛÛœÝ˜Z[ÈXÜ›ÜÜÈLˆÛÛœÝ˜Z[™YÛ\Ý\œËˆ]›Ú™XÝÈÛ›ÝÛ‚˜ÛÛœÝ˜Z[š[Û][ÛœÈ[™™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]ËˆHš\œÝ‹\]Y\žH™\šYšXØ][ÛˆÝX˜Ú[šÈ
‹ÌLL˜
H[ˆ^ÜÙYH™]È›ØÚÙ\Ž‚˜WØÜØNŒÎYØZ[œÝ[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒLNX^˜Z[‹Ý\Ý•K\ØÛÜ™HÍÍXˆ›Ý[™ˆ[Ý™\ÈWØÜØNŒLNÈ[‹Y\ÝšX][Ûˆ[™HØ[YBœÝX˜Ú[šÈ\ÜÙ\ÈÚ]MŒÈX\Y›ÝÜË‹ÍN˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™B˜LX[™\™Ù]]š[Û][™ÈZ\œË‚‚•HZ\™Y›Ý[™LˆÝX˜Ú[šÈËÌLL˜ÛÛ\]YÚ]KMX\Y›ÝÜËKB˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HŽLX[™Mˆ\™Ù]]š[Û][™È›ÝÜÂ˜XÜ›ÜÜÈH™\ÜYÝXÝ\™HZ\œËˆHÝ\œ™[[™Ù™ˆÜ]\Â˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™×ÌLšœÛÛ˜ˆ]›ÛÂÜÙH›ØÚÙ\œÈ[ÈÍYÚUHÛÛœÝ˜Z[ÈXÜ›ÜÜÈMÛÛœÝ˜Z[™YÛ\Ý\œËœ›Ú™XÝÈÛ›ÝÛˆÛÛœÝ˜Z[š[Û][ÛœË™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë›[Ý™\ÈLˆ[šY\ÈÈ[Ý][™Lˆ[[Ý]Ý][Ù‹\ØÛÜH[šY\ÈÂš[‹Y\ÝšX][Û‹ÙY\È[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ][™šÙY\È[›ÝÜÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›K‚‚•H™]š[Ý\È[ˆ[ˆ™\˜[ˆÝX˜Ú[šÜÈ‹ÌLL˜[™ËÌLL˜œ›ÛHH›Ý[™LÂœ™XY[™\ÜËˆÝX˜Ú[šÈˆ\ÜÙYYØZ[ˆÚ]MŒÈX\Y›ÝÜË‹ÍM‚˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HLX[™\™Ù]]š[Û][™ÈZ\œË‚”ÝX˜Ú[šÈÈÝ[˜Z[YÚ]KMX\Y›ÝÜËMÍˆ˜Z[‹Ý\Ý›ÝÜËX^•K\ØÛÜ™HŽØ[™Û™H™\ÜY›ØÚÙ\ŽˆWØÜØNXYØZ[œÝ[[Ý]›Ý][Ù‹\ØÛÜHWØÜØNŒÎMØˆ›Ý[™›ÛY]›ØÚÙ\ˆ[ÈÍHYÚUB˜ÛÛœÝ˜Z[Ë[Ý™YWØÜØNŒÎMØÈ[‹Y\ÝšX][Û‹[™H\™XÝ›Ý[™MœÝX˜Ú[šÈËÌLL˜™\[ˆ\ÜÙYÚ]KMX\Y›ÝÜËMÍH˜Z[‹Ý\Ý›ÝÜË›X^K\ØÛÜ™HNN[™\™Ù]]š[Û][™ÈZ\œË‚‚•\È[ˆÛÛ[YYœ›ÛH›Ý[™ˆ\™XÝ›Ý[™MÝX˜Ú[šÈÌLL˜ÛÛ\]YÚ]HX\Y›ÝÜËKM˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HÌŒX[™Û™Bœ™\ÜY›ØÚÙ\ŽˆWØÜØNMYØZ[œÝ[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŽ‚˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™WÌLšœÛÛ˜›ÛÂ]›ØÚÙ\ˆ[ÈÍˆYÚUHÛÛœÝ˜Z[ÈXÜ›ÜÜÈMHÛÛœÝ˜Z[™YÛ\Ý\œË[Ý™\Â˜WØÜØNŽÈ[‹Y\ÝšX][Û‹™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]ËÙY\Âš[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ][™ÙY\È[›ÝÜÂœ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›Kˆ]È™XY[™\ÜÈ\Y˜XÝ\Â˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™KšœÛÛ˜‚•H\™XÝ›Ý[™MH™\[ˆÙˆÝX˜Ú[šÈÌLL˜\ÜÙ\ÈÚ]HX\Y›ÝÜËŒKLÌˆ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HŽNX[™\™Ù]]š[Û][™ÈZ\œË‚‚‘\™XÝ›Ý[™MHÝX˜Ú[šÈKÌLL˜[ˆÛÛ\]YÚ]MKLÌHX\Y›ÝÜËŒ‹MMH˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HŽÎX[™Û™H™\ÜY›ØÚÙ\Ž‚˜WØÜØNNYØZ[œÝ[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒŽˆHÝ\œ™[[™Ù™‚œÜ]Ø\È[‚˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™—ÌLšœÛÛ˜ˆ]™›ÛÈ]›ØÚÙ\ˆ[ÈÍÈYÚUHÛÛœÝ˜Z[ÈXÜ›ÜÜÈMˆÛÛœÝ˜Z[™YÛ\Ý\œË›[Ý™\ÈWØÜØNŒŽÈ[‹Y\ÝšX][Û‹™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]ËšÙY\È[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ][™ÙY\È[›ÝÜÂœ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›Kˆ]È™XY[™\ÜÈ\Y˜XÝ\Â˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™‹šœÛÛ˜‚•H\™XÝ›Ý[™Mˆ™\[ˆÙˆÝX˜Ú[šÈKÌLL˜\ÜÙ\ÈÚ]MKLÌHX\Y›ÝÜËŒ‹LÎH˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HŽNX[™\™Ù]]š[Û][™ÈZ\œË‚‚•\È[ˆÛÛ[YYœ›ÛH›Ý[™‹ˆ\™XÝÝX˜Ú[šÈLÌLL˜[YYÝ][™\ˆBŽL\ÙXÛÛ™›Ý[™™Y›Ü™H[Z][™ÈZ\ˆ›ÝÜËˆHË\]Y\žHÜ]ÙˆHØ[YHÚ[™ÝÂ˜ÛÛ\]YZXÜ›ØÚ[šÈŒÌŒ
WØÜØNŒXXWØÜØNŒØ
HÚ]ËX\Y›ÝÜËŒKÌNH˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HÌLM˜[™Û™H™\ÜY›ØÚÙ\Ž‚š[‹Y\ÝšX][ÛˆWØÜØNŒØØŽŒPÐØYØZ[œÝ[[Ý]Ý][Ù‹\ØÛÜB˜WØÜØNŒNØŽŒVSˆHÝ\œ™[[™Ù™ˆÜ]\È›ÝÂ˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™×ÌLšœÛÛ˜ˆ]™›ÛÈ]›ØÚÙ\ˆ[ÈÎYÚUHÛÛœÝ˜Z[ÈXÜ›ÜÜÈMÈÛÛœÝ˜Z[™YÛ\Ý\œË›[Ý™\ÈWØÜØNŒNÈ[‹Y\ÝšX][Û‹™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]ËšÙY\È[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ][™ÙY\È[›ÝÜÂœ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›Kˆ]È™XY[™\ÜÈ\Y˜XÝ\Â˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ËšœÛÛ˜‚•H\™XÝ›Ý[™MÈ™\[ˆÙˆZXÜ›ØÚ[šÈŒÌŒ[YYÝ][™\ˆBŽL\ÙXÛÛ™›Ý[™™Y›Ü™H[Z][™ÈZ\ˆ›ÝÜËˆ\È[ˆ\ÛÛ]Y][Y[Ý]Ú]Ú[™ÛK\]Y\žHÚXÚÜÈ[™\ˆHØ[YH›Ý[™MÈ™XY[™\ÜËˆÝYÙY[™XÙ\ÈŒŒK[™Œˆ
WØÜØNŒXXWØÜØNŒØ
H[ÛÛ\]H[™YÙÜ™YØ]HÈËX\Yœ›ÝÜËKÌLH˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HŽMØ[™\™Ù]]š[Û][™ÂœZ\œËˆÝYÙY[™XÙ\ÈŒË[™H
WØÜØNXWØÜØN˜
H[ÛÈÛÛ\]H[™˜YÙÜ™YØ]HÈ‹NLX\Y›ÝÜËÍÎ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HMŒŽX˜[™\™Ù]]š[Û][™ÈZ\œËˆÝYÙY[™^ˆ
WØÜØNØ
HÛÛ\]\ÈÚ]ŽÂ›X\Y›ÝÜËNLÈ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HLÍX[™\™Ù]]š[Û][™ÂœZ\œËˆÝYÙY[™^È
WØÜØNŽ
H[ˆ^ÜÙ\ÈÛ™H›ØÚÙ\Ž‚š[‹Y\ÝšX][ÛˆWØÜØNŽØŽŒRU’YØZ[œÝ[[Ý]WØÜØNÍLÂ˜ŽŒUN˜X^K\ØÛÜ™HÎLX‚‚”›Ý[™NÚ[™ÛK\]Y\žH™\šYšXØ][Ûˆ[ˆÛX\œÈÝYÙY[™XÙ\ÈŽMÎŠWØÜØNŽXXWØÜØNÎX
H™Y›Ü™HÝYÙY[™^ÎH^ÜÙ\ÈH™]È›ØÚÙ\Ž‚š[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŽØŽŒPÌÐØYØZ[œÝ[‹Y\ÝšX][Û‚˜WØÜØNØŽŒPUUØ[™WØÜØNMŽXØŽŒQ•TXX^K\ØÛÜ™HŽÌ˜‚‚•HÝ\œ™[[™Ù™ˆÜ]\È›ÝÂ˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™M—ÌLšœÛÛ˜ˆ]™›ÛÈH]\ÝÝYÙYZ[™^LLL›ØÚÙ\ˆÝ\™˜XÙH[ÈˆYÚUHÛÛœÝ˜Z[Â˜XÜ›ÜÜÈŒHÛÛœÝ˜Z[™YÛ\Ý\œÈ[™[ÛÈ\Y\ÈÎ™X[Ù\]Y[˜ÙKZY[]Bœ\][ÛˆÛÛœÝ˜Z[È™Y›Ü™H\ÜÚYÛ›Y[ˆ\È™\Ù\™\ÈÙ\]Y[˜ÙKXÛ\Ý\‚œÜ]ËÙY\È[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ][™ÙY\È[œ›ÝÜÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›Kˆ]È™XY[™\ÜÈ\Y˜XÝ\Â˜\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™M‹šœÛÛ˜‚•H\™XÝ›Ý[™NH™\[ˆÙˆÝYÙY[™^ÎH\ÈÝYÙY[™XÙ\ÈNÈ\ÜÙ\Âš[ˆYÙÜ™YØ]HÚ]ÍX\Y›ÝÜËÍŒÈ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™B˜ÍØ[™\™Ù]]š[Û][™ÈZ\œËˆÛÛ[Z[™È›Ý[™NHÚ[™ÛK\]Y\žB™\šYšXØ][ÛˆÛX\œÈÝYÙY[™XÙ\ÈNMHÚ]MËNHX\Y›ÝÜËËMÂ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HMÎX[™\™Ù]]š[Û][™ÂœZ\œËˆH™^›Ý[™NH˜]ÚÛX\œÈ[™XÙ\ÈM‹LLH™Y›Ü™H[™^Lˆ^ÜÙ\Â˜WØÜØNŒLØØŽŒUSØ™\œÝ\È[[Ý]WØÜØNŒLMXØŽŒUÌSØ]X^K\ØÛÜ™B˜ÍLØˆH\™XÝ›Ý[™LL™\[ˆÙˆÝYÙY[™^Lˆ\ÜÙ\È]X^˜Z[‹Ý\ÝK\ØÛÜ™HÌXÚ]\™Ù]]š[Û][™ÈZ\œËˆÝYÙY[™^LÂ[ˆ^ÜÙ\ÈWØÜØNŒLØŽŒPÎUX™\œÝ\È[[Ý]WØÜØNŽ˜ØŽŒQLPX˜]X^ÍŒÌØÈ›Ý[™LH›ÛÈ]Z\ˆ]^ÜÙ\ÈWØÜØNŒL™\œÝ\Â˜WØÜØNŒÍŒØWØÜØNÍ]X^ÌÌMØÈ›Ý[™Lˆ›ÛÈÜÙHZ\œÈ[™˜ÛX\œÈÝYÙY[™^LÈ]X^ŽXˆÝYÙY[™^L[ˆ\ÜÙ\È]X^˜M˜[™ÝYÙY[™^LH^ÜÙ\ÈH\™Ù\ˆYÚUH›ØÚÙ\ˆÝ\™˜XÙH]›X^ŽŒ˜Ú]Ìˆš[Û][™È›ÝÜËˆ›Ý[™LÈ›ÛÈÜÙHÛÛœÝ˜Z[È[™˜ÛX\œÈ[™XÙ\ÈLKLLˆ™Y›Ü™H[™^LÈ^ÜÙ\ÈWØÜØNŒL]X^Ž˜‚”›Ý[™M›ÛÈ]Ý\™˜XÙH[™™\[œÈ[™^LÈÛX[›H]X^ŽŒ˜‚’[™^L[ˆ^ÜÙ\ÈWØÜØNŒLX]X^ÍXÈ›Ý[™MH›ÛÈÜÙB˜›ØÚÙ\œÈ[™™\šYšY\È[™XÙ\ÈLËLLHÛX[›H]X^ŽNM˜ˆ[™^LL[‚™^ÜÙ\ÈWØÜØNŒLLXYØZ[œÝWØÜØNŒÍWØÜØNMLWØÜØNŒŒÍ˜[™˜WØÜØNŒÌ]X^ÍLŒXˆ›Ý[™Mˆ›ÛÈ]›ØÚÙ\‹]]È\™XÝš[™^LLL™\[ˆÝ[^ÜÙ\ÈWØÜØNŒLLXYØZ[œÝWØÜØNŽL˜]X^ÍÌ‚”›Ý[™MÈ›ÛÈ]Z\ˆ[™™\šYšY\È[™^LLÛX[›H]X^ŽŒØÂš[™^LLH[ÛÈ\ÜÙ\È]X^Mˆ[™^LLˆ[ˆ^ÜÙ\ÈWØÜØNŒLLØ˜YØZ[œÝ[[Ý]WØÜØNŒLÌX]X^ÌŒØÈ›Ý[™N›ÛÈ]Z\ˆ]š]È™\[ˆ^ÜÙ\ÈH\™Ù\ˆWØÜØNŒLLØ›ØÚÙ\ˆÝ\™˜XÙHYØZ[œÝWØÜØNŽM˜˜WØÜØNŽMÎ[™™[]Y[‹Y\ÝšX][Ûˆ™ZYÚ›ÜœÈ]X^ŽLØˆ›Ý[™NB™›ÛÈ]]šY[˜ÙH[™ÛX\œÈ[™XÙ\ÈLL‹LLLÈ™Y›Ü™H[™^LM^ÜÙ\Â˜WØÜØNŒLMX™\œÝ\ÈWØÜØNŽŒ˜]X^ÌÌÎˆ›Ý[™Œ›ÛÈ]Z\ˆ[™˜ÛX\œÈ[™^LM][™^LMH^ÜÙ\ÈHœ›ØY\ˆWØÜØNŒLM˜Ý\™˜XÙH]X^˜ŽMÍXÈ›Ý[™ŒH›ÛÈ]Ý\™˜XÙH]^ÜÙ\ÈWØÜØNŒLM˜™\œÝ\È[[Ý]˜WØÜØNØ]X^ŽLÌ˜ˆ›Ý[™Œˆ›ÛÈ]Z\ˆ[ÈˆYÚUB˜ÛÛœÝ˜Z[È\ÈÎÙ\]Y[˜ÙKZY[]H\][ÛˆÛÛœÝ˜Z[ËÚ]›Ú™XÝYš[Û][ÛœÈ[™Ù\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[ˆÛX\œÈ[™XÙ\ÈLMKLLN]X^˜ŽLÎXÚ]\™Ù]]š[Û][™ÈZ\œË‚‚“™^›ÛÙYZÈÛÜšÈÚÝ[ÛÛ[YHœ›ÛH›Ý[™LŒˆ™XY[™\ÜÈ]ÝYÙY]Y\žBš[™^LNH\Ú[™ÈHØ[YHÛ™K\]Y\žH™\šYšXØ][Ûˆ]\›‹ÜˆH\™Ù\ˆ›Ý[™Y˜Ú[šÈÛ›HYˆH[[YHš\ÚÈ\ÈXØÙ\X›KˆÝÜÛˆ[žHHHØ˜Z[‹Ý\Ý›ØÚÙ\ˆ[™›Û][ÈH™]ÈÛ\Ý\‹Yš\œÝ›Ý[™™Y›Ü™B˜ÛÛ[Z[™Ë‚˜WØÜØNŒÍÌ˜[™WØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË[ÜÝ]Y\žHÛÝ™\˜YÙBœ™[XZ[œÈ[™\šYšYY[™[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX™[XZ[œÂœ™\]Z\™Y‚‚‘^\›˜[[Ý[\Ü™[XZ[œÈ›ØÚÙYˆHÙ[XÝY\[Ý™\™\Ù[][Û‚˜YYXØ][Ûˆ›ÝÈÚ]™\ÈÛÛ˜Ü™]H™]šY]Ë[Û›HÝ]\Ù\ÎˆÈÝX›H™\™\Ù[][Û‚˜ÛÛ›ÛË™X\‹Y\XØ]HÛÝ]Ë[™ÈÝXš[]KXÚ[™ÙH›ÝÜÈ™YY[™Âœ™]šY]ËˆH™Yœ™\ÚY[ÝÝXØÙ\ÜÈÜš]\šXHÝ[™\ÜÈ\›Z[˜[™XÚ\Ú[ÛœË[\Ü\™XYH›ÝÜËÛÝ[X›HØ[™Y]\ËÈXÝ]™K\Ú]K\ÛÝ\˜ÙB˜›ØÚÙ\œËLœ›ØY\ˆ\XØ]K\ØÜ™Y[š[™È›ØÚÙ\œËÈ[œ™\ÛÛ™Yœ™\™\Ù[][Û‹XÛÛ›Û›ØÚÙ\œË[™L[YØ]H›ØÚÙ\œËˆ™^\ÙY[[ÝÛÜšÈ\Èœ›ØY\ˆ\XØ]HØÜ™Y[š[™ÈÜˆ™]šY]ÈXÚ\Ú[ÛœÈÛ›HY\ˆH›ØÚÙ\‚™]šY[˜ÙH\ÈÝY™šXÚY[ÈÙY\[Ý]]È›Û‹XÛÝ[X›H[›\ÜÈ[[\Ü˜ÛÛ™][ÛœÈ\ÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLMŒŽÖˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑ‹Ø\Y˜XÝ[[™XYÙH\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆŽN[š]\ÝÂœ\ÜÙY˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ËHKH™]šY]È™[XZ[™Y››Û‹\›Û[ÝX›HÚ]ÛX[ˆÛÝ[X›HX™[ËÝ\œ™[\Y˜XÝÈ[™XYB˜ÛÛZ[™YH›ÞHÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]\ÈHØ[›ÛšXØ[[™œÙ[XÝY\[ÝTÓKLˆ™\™\Ù[][ÛˆØ[\\Ë[™›ÛÙYZØ[\Ù\\Ø˜›\Ý[™X[[Û™Ù\™HXœÙ[ÛˆUˆHÛÙKXÛÛ™š\›YY˜Z[\™HØ\ÈB›Z\ÜÚ[™È[™XYÙHÚXÚÈÛˆHYÚY˜[‹Z[ˆØØ[[™Ë\]X[]H]Y]‚‚“]\Ý[ˆÛÛ[YY\Y˜XÝYÜ˜\ÛÛœÚ\Ý[˜ÞH[™Ù[XÝYTˆÔÑˆ\™[š[™Âš[œÝXYÙˆY[™ÈØ]HÛÝ[ÜˆÜ[š[™È[›Ý\ˆKPÔÐH˜[˜ÚKˆÛÙH[œÜXÝ[Û‚™›Ý[™]Z[YÙ[ÛY]žKY™X]\™\ØÛÝ[XØÙ\HÙ[XÝYTˆÝ™\œšYH[‚ÚÜÙH™XYH›ÝÜÈÙ\™HÝ]ÚYHHÙ[XÝYÜ˜\ÛXÙKÚÜÙH™\ÚYYH›ÙHYÂ™Y›Ý™[Û™ÈÈHÙ[XÝYÜ˜\ÜˆÚÜÙHÝ\œ™[ÜÙ[XÝYÜ—ÚY›Â›Û™Ù\ˆX]ÚYÙ[XÝYÜ˜\]šY[˜ÙKˆ]]›ÝÈ˜Z[È™Y›Ü™HÙ[ÛY]žBÜš]K[™™YØ]]™H™YÜ™\ÜÚ[ÛœÈÛÝ™\ˆÝ][Ù‹\ÛXÙHÝ™\œšYH›ÝÜÈ[™[šÛ›ÝÛ‚›Ý™\œšYH™\ÚYYH›ÙHYËˆH[ˆ[ÛÈ›Ý[™]Ù]™\˜[^\›˜[[Ý˜Z[\œÈ›Ú[™YYÚY˜[‹Z[ˆ\Y˜XÝÈ™Y›Ü™HH˜[œÙ™\ˆØ]HÛÝ[™Z™XÝ›Z^YÛÝ\˜ÙHÛXÙ\Ëˆ]Y]Y^\›˜[\ÛÝ\˜ÙKZ[\Ü\™XY[™\ÜØ˜Z[Y^\›˜[\ÛÝ\˜ÙK]˜[œÙ™\‹X›ØÚÙ\‹[X]š^˜Z[Y^\›˜[\ÛÝ\˜ÙK\[ÝY]šY[˜ÙK\XÚÙ][™˜Z[Y^\›˜[\ÛÝ\˜ÙK\[ÝY]šY[˜ÙKYÜÜÚY\œØ›ÝÈÚ\™HH˜Z[Y˜\Ý^\›˜[˜\Y˜XÝ[[™XYÙHØY\‹™XÛÜ™ÚXÚÙY[™XYÙH[ˆY]Y]K˜\Y˜XÝÛ[™XYÙX˜[™]™HÓH™YØ]]™H™YÜ™\ÜÚ[ÛœÈ›ÜˆZ^YKÌKH[œ]Ëˆ™Yœ™\ÚY™^\›˜[\Y˜XÝÈÙY\HKH˜[œÙ™\ˆØ]H]‹Í‹Ú]ÛÝ[X›B™^\›˜[›ÝÜÈ[™[\Ü\™XYH›ÝÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLMNŒÌŒˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑ‹Ø\Y˜XÝ[[™XYÙH\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆÌ[š]\ÝÂœ\ÜÙY˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ËHKH™]šY]È™[XZ[™Y››Û‹\›Û[ÝX›HÚ]ÛX[ˆÛÝ[X›HX™[ËÝ\œ™[\Y˜XÝÈ[™XYB˜ÛÛZ[™YH›ÞHÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]\ÈØ[›ÛšXØ[[™œÙ[XÝY\[ÝTÓKLˆ™\™\Ù[][ÛˆØ[\\Ë[™›ÛÙYZØ[\Ù\\Ø˜›\Ý[™X[[Û™Ù\™HXœÙ[ÛˆUˆHÛÙKXÛÛ™š\›YY˜Z[\™\ÈÙ\™BœÚ[[Ù[XÝYTˆÝ™\œšYHZ\ÛX]Ú[™[™È[™Z\ÜÚ[™ÈZ[][YH[™XYÙB˜ÚXÚÜÈÛˆH[\Ü\™XY[™\ÜË›ØÚÙ\‹[X]š^[Ý\XÚÙ][™œ[ÝYÜÜÚY\ˆZ[\œË‚‚”™]š[Ý\È[ˆ\™Ù]YH^\›˜[\[Ý™\™\Ù[][Û‹XÛÛ›ÛÔÑˆ˜]\ˆ[‚˜Y[™ÈØ]HÛÝ[ˆÛÙH[™\Y˜XÝ]šY[˜ÙHÚÝÙY]HÙ[XÝY[Ý™ÜÜÚY\œÈÝ[\[™YÛˆHL‹\›ÝÈX\YXÛÛ›Û™\™\Ù[][ÛˆØ[\H[™\™Y›Ü™HY™\™\Ù[][Ûˆ›ÝÜÈ›ÜˆÛ›HÙˆHLÙ[XÝY[Ý˜Ø[™Y]\ÎÈHÝ\ˆˆØ\œšYYÝ[H™\™\Ù[][Û‹X˜XÚÙ[™›ØÚÙ\œÈ™Y›Ü™Bœ™]šY]ÈÛÝ[›ØÙYYˆHš^YÂ˜Z[Y^\›˜[\ÛÝ\˜ÙK\[Ý\™\™\Ù[][Û‹X˜XÚÙ[™\[˜Z[ÈBœ™]šY]Ë[Û›H[Ý[ˆ[™TÓKLˆØ[\K™Yœ™\Ú\È[ÝÜÜÚY\œÈÈ]XÚœ™\™\Ù[][Ûˆ]šY[˜ÙHÈ[LÙ[XÝY›ÝÜË[™YÈH[Ýœ™\™\Ù[][ÛˆØ[\HÈ\YØ[™Y]K[[™XYÙH˜[Y][Û‹ˆH™Yœ™\ÚY™^\›˜[˜[œÙ™\ˆØ]H›ÝÈ\ÜÙ\È‹ÍˆÚ]›ØÚÙ\œË™XÛÜ™Â˜^\›˜[Ü[ÝÜ™\™\Ù[][Û—ÜØ[\WØØ[™Y]WØÛÝ[LL˜[Y]\ÈÌÂ˜Ø[™Y]K[[™XYÙH\Y˜XÝË[™˜[Y]\ÈŒÈÛX[ˆKH\Y˜XÝ\][œ]Ë‚[^\›˜[›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›K›Û‹XÛÝ[X›K[™›Ý[\Ü\™XYNÂ˜MLŒØ\È^XÚ]H[Ý]\ÈH™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÛ›Û‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕŒÎŒŽˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\ÜY\È›Üˆ›Ý[™YØÚY[YšXÈÙ[™\˜[^˜][Û‹ØÛÛ›ÛÛÜšÈ›ÝYÚH[Ý\ÜXÚYšXÈXZØYÙK\ØY™HTÓKLˆØ[\K[™Y\È›Ü‚”ÔÑ‹Ù^\›˜[\[Ý\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆŽMˆ[š]\ÝÈ[™˜˜[Y]X\ÜÙYHKH™]šY]È™[XZ[™Y›Û‹\›Û[ÝX›HÚ]ÛX[‚˜ÛÝ[X›HX™[ËÝ\œ™[\Y˜XÝÈ[™XYHÛÛZ[™YH›ÞHÙ\]Y[˜ÙKÙ›ÛšÛÝ][™L‹\›ÝÈØ[›ÛšXØ[TÓKLˆØ[\K›È›ÛÙYZËÓS\Ù\\Ì‹Ð“TÕÑPSSÓ‘˜˜XÚÙ[™Ø\È]˜Z[X›HÛˆU[™HÙ[XÝY[ÝÜÜÚY\ˆ\Y˜XÝ^ÜÙY›Z\ÜÚ[™È™\™\Ù[][Ûˆ›ÝÜÈ›ÜˆˆÙ[XÝYØ[™Y]\Ë‚‚Ý\œ™[ÔÑˆÝ]\ÈY\ˆHŒ‹LKLLÕŒŽŒNŒÎˆ[ŽˆÛÝ[\™]šY[˜ÙB›XZ[Z[˜Xš[]H\È[™Y]HÛÙH]™[ˆÙ[ÛY]žWÜ™]šY]˜[œX\Ù\ÈB™\œÚ[Û™YXÛ\˜]]™HÓÕS•T‘U’QSÑWÔÓPÖXÚ]\YÚ\™Y[œ]Ëœ[K[]™[›Ý™[˜[˜ÙK˜XÚÝØ\™ËXÛÛ\]X›H™X\ÛÛ‹Ù]Z[šY[Ë[™^XÚ]›YXÚ[š\ÛK]^XZØYÙH›YÜËˆÚXÚ×ÛX™[Ù˜XÝÜžWÙØ]\ØXØÙ\ÈH\Y˜X™[˜XÝÜžQØ]R[œ]ËŒXÛÛ˜XÝHÓHØYÈØ]H\Y˜XÝÈ›ÝYÚBX›KYš]™[ˆX\[™›Û‹Y^[\X™[Y˜XÝÜžHØ]H[œ]È›ÝÈÙ]ÛXÙK[[™XYÙB˜[Y][Ûˆ\È^[ØYYXÛ\™YÛXÙKØ˜]ÚÚXÚÜËˆHÝ\œ™[KØ]B˜\Y˜XÝ[ÛÈ™XÛÜ™È^[ØYY]ÙÈ[™ÚÜ^[ØYYÙ\ÝË[™H™YØ]]™Bœ™YÜ™\ÜÚ[Ûˆ\Ý™Z™XÝÈH™[˜[YYÜˆÝ[H\Y˜XÝÚÜÙH^[ØYÛXÙHY]Y]B˜ÛÛ˜YXÝÈH][™XYÙKˆ^[XZØYÙH›ÝXÝ[Ûˆ\È›ÝÈ[™›Ü˜ÙY[ˆ›ÝHÙ[ÛY]žHØÛÜ™\ˆ[™H^\›˜[™\™\Ù[][ÛˆØ[\NˆÙ[ÛY]žH™]šY]˜[™^ÛY\ÈYXÚ[š\ÛH^[žH˜[Y\ËX™[ËPËÔšXHY[YšY\œËÛÝ\˜ÙHYË˜[™\™Ù]X™[Èœ›ÛHÜÚ]]™HØÛÜš[™Ë[™\Ù\ÈH^Yœ™YHØØ[”YØ[™X[˜ÚÜˆ™X]\™H›Üˆ\Ý\ÜYÜÚ]]™\Ëˆ™\™\Ù[][ÛˆØ[\\Â\ÙHÙ\]Y[˜ÙH[X™Y[™ÜÈ[™[™ÝÛÝ™\˜YÙH\È™YXÝ]™HÛÝ\˜Ù\ÎÈ]\š\ÝXÂ™š[™Ù\œš[YËX]ÚYKPÔÐH™Y™\™[˜ÙHYË[™ÛÝ\˜ÙHØÛÜHÚYÛ˜[ÈØ\œžB™^XÚ]™]šY]ËÚÛÝ]XZØYÙH›YÜËˆH™\™\Ù[][Ûˆ]Y]˜Z[ÈY‚‘PËÔšXHYËYXÚ[š\ÛH^X™[Ëš[™Ù\œš[YËÜˆÛÝ\˜ÙK]\™Ù]šY[YšY\œÈ\X\ˆ\È™YXÝ]™H™X]\™HÛÝ\˜Ù\Ëˆ\Y˜XÝÛÛœÚ\Ý[˜ÞBš\™[š[™È^\ÝÈ[ˆH^\›˜[›ØÚÙ\ˆX]š^]Y]ÚXÚ™Z™XÝÂ˜Ø[™Y]K[X[šY™\Ý[™XYÙHZ\ÛX]Ú\Ë[™[ˆH^\›˜[˜[œÙ™\ˆØ]KÚXÚ˜[Y]\ÈØ[™Y]HXØÙ\ÜÚ[ÛœÈXÜ›ÜÜÈYÚY˜[‹Z[ˆ^\›˜[\Y˜XÝË˜\Y˜XÝ\]ÛXÙH[™XYÙHXÜ›ÜÜÈÝ\YY^\›˜[\Y˜XÝË[™[Ýœ™]šY]Ë[Û›KÛ›ËYXÚ\Ú[ÛˆÙ[X[XÜÈ›ÝYÚH\Y˜^\›˜[ÛÝ\˜ÙU˜[œÙ™\‘Ø]R[œ]ËŒXÛÛ˜XÝ[™Ú\™YØ[™Y]K[[™XYÙB˜\Y˜XÝ™YÚ\ÝžH™Y›Ü™H\ÜÚ[™ÈHKÍH™]šY]Ë[Û›HØ]KˆHØ]HÓH˜Z[Â™˜\ÝÛˆZ^YKÌKH]Ë^[ØYYXÛ\™YÛXÙHÛÛ˜YXÝ[ÛœËÜ‚œ[Ý\Y˜XÝÈ]ÝÜ™Z[™È›Û‹XÛÝ[X›H™]šY]ÈÛÜšÈ›ÙXÝËˆBœÙ\]Y[˜ÙKZÛÝ]]Y]\È›ÝÈ\ÙˆH›ÝË[]™[Ø[™Y]K[[™XYÙH™YÚ\ÝžKœÛÈHÝ[HÜˆZ\ÛX]ÚYÛÝ]]Y]Ø[››ÝÚ[[HØ]\ÙžHHØ]HžB›X]Ú[™ÈÛ›HYÚ[]™[Ø[™Y]HÛÝ[Ë‚‚“]\Ý[ˆ\™Ù]YH\Y˜XÝYÜ˜\ÛÛœÚ\Ý[˜ÞHÔÑˆ˜]\ˆ[ˆY[™ÈØ]B˜ÛÝ[ˆHÛÙH]šY[˜ÙHÚÝÙY]Ù\]Y[˜ÙWÚÛÝ]Ø]Y]Ø\ÈXØÙ\YžB˜^\›˜[ÛÝ\˜ÙU˜[œÙ™\‘Ø]R[œ]ËŒX[™ÚXÚÙYžH]ÈÝÛˆØ]K]]Ø\Â››Ý[˜ÛYY[ˆVT“SÕS”Ñ‘T—ÐÐS‘QUWÓS‘PQÑWÑ’QSØˆHš^YÈ]ÈÚ\™YØ[™Y]K[[™XYÙH˜[Y][Û‹YÈH™YØ]]™H™YÜ™\ÜÚ[ÛˆÚ]B›Z\ÛX]ÚYÛÝ]XØÙ\ÜÚ[Û‹[™™Yœ™\Ú\Â˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜ÈHØ]HÝ[œ\ÜÙ\ÈKÍK›ÝÈÚ]Ù\]Y[˜ÙWÚÛÝ]Ø]Y]\ÝY[[Û™ÈÌˆÚXÚÙY˜Ø[™Y]K[[™XYÙH\Y˜XÝÈ[™HÛX[ˆŒ‹X\Y˜XÝ][™XYÙKˆ\È™[[Ý™\Â›Û™HÚ[[Y˜Z[\™HÝ\™˜XÙHÚ]Ý]Ú[™Ú[™ÈÛÝ[X›HX™[ÈÜˆ[\Üœ™XY[™\ÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕŒŽŒNŒÎˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑ‹Ø\Y˜XÝ[[™XYÙH\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆŽMˆ[š]\ÝÂ˜[™˜[Y]X\ÜÙYHKH™]šY]È™[XZ[™Y›Û‹\›Û[ÝX›KÝ\œ™[˜\Y˜XÝÈ[™XYHÛÛZ[™YH›ÞHÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ][™ŒL‹\›ÝÈTÓKLˆ™\™\Ù[][ÛˆØ[\K›ÛÙYZËÓS\Ù\\Ì‹Ð“TÕÑPSSÓ‘Ù\™HXœÙ[›ÛˆU[™HÛÙH[œÜXÝ[Ûˆ›Ý[™HÙ\]Y[˜ÙKZÛÝ]]Y][™XYÙHØ\š[œÚYHH^\›˜[˜[œÙ™\ˆØ]HÛÛ˜XÝ‚‚”™]š[Ý\È[ˆ\™Ù]YH^\›˜[\[ÝÙ\]Y[˜ÙHÔÑˆ˜]\ˆ[ˆY[™ÈÙ[™\šXÂ™Ø]HÛÝ[ˆH™]Â˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÜ™Y™\™[˜ÙWÜØÜ™Y[—Ø]Y]ÌLKšœÛÛ˜ÚXÚÜÂÚ]\ˆH›Ý[™YÝ\œ™[ÛÝ[X›K\™Y™\™[˜ÙHØÜ™Y[ˆØ[ˆÛX\ˆB˜Ý\œ™[\™Y™\™[˜ÙH™X\‹Y\XØ]H›ØÚÙ\‹ˆH[š]X[]Y]^ÜÙYÛÂš[˜XÝ]™H[Y\™ÙY[šT›Ý™Y™\™[˜Ù\È
ÌMÍ˜[™LMX
H[[Û™ÈH^XÝYÌÍHÝ\œ™[ÛÝ[X›H™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœÎÈH™]Ú]›ÝÈ™\ÛÛ™\ÈÜÙB˜ÛÛœÙ\˜]]™[HÈ[\ÝY™\XÙ[Y[È
XØNTS‘Ø[™˜PŽØPŽX
H[œÝXYÙˆÚ[[H›Ü[™È[KˆH]Y]›ÝÈ™XÛÜ™Â˜ÛÛ\]HÝ\œ™[\™Y™\™[˜ÙHÛÝ™\˜YÙKŽÝ\œ™[\™Y™\™[˜ÙHÜZ]›Ë\ÚYÛ˜[œ›ÝÜË[™ÛÈ^XÝ\™Y™\™[˜ÙHÛÝ]ËˆHÙ\]Y[˜ÙK\ÙX\˜Ú^Ü™\XÙ\Â˜ÛÛ\]WÛ™X\—Ù\XØ]WÜ™Y™\™[˜ÙWÜÙX\˜ÚÛ›ÝØÛÛ\]YÚ]˜ÛÛ\]WÝ[š\™Y—ÛÜ—Ø[Ýœ×Ø[Û™X\—Ù\XØ]WÜÙX\˜ÚÜ™\]Z\™Y›ÜˆHŽ››Û‹ZÛÝ]›ÝÜËÙY\ÈÛÝ[X›KÚ[\Ü\™XYH^\›˜[›ÝÜË[™B™^\›˜[˜[œÙ™\ˆØ]H›ÝÈÚXÚÜÈH™Y™\™[˜ÙK\ØÜ™Y[ˆ]Y]\™XÝH[™œ\ÜÙ\ÈKÍKˆHØ]H[ÛÈ™Z™XÝÈHÝ[HÙ\]Y[˜ÙK\ÙX\˜Ú^Ü]ÛZ[\Â˜HY™™\™[Ý\œ™[\™Y™\™[˜ÙHÛÛ\][ÛˆÛÝ[[ˆH]Y]›ÝÜÈÝ\Ü‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕŒNŒŒLˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑ‹Ù^\›˜[\[Ý\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆŽLˆ[š]\ÝÈ[™˜˜[Y]X\ÜÙYHKH™]šY]È™[XZ[™Y›Û‹\›Û[ÝX›KÝ\œ™[\Y˜XÝÂ˜[™XYHÛÛZ[™YH›ÞHÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ][™L‹\›ÝÈTÓKL‚œ™\™\Ù[][ÛˆØ[\K[™H™]È™Y™\™[˜ÙK\ØÜ™Y[ˆ]Y]ÚÝÙY]Z\ÜÚ[™ÂH[š]X[™Y™\™[˜ÙK\ØÜ™Y[ˆ]Y]^ÜÙY[˜XÝ]™H[Y\™ÙYÝ\œ™[\™Y™\™[˜ÙB˜XØÙ\ÜÚ[ÛœÈ]YÈ™H™\ÛÛ™Y™Y›Ü™H^\›˜[[ÝÙ\]Y[˜ÙHÛX\˜[˜ÙK‚‚”™]š[Ý\È[ˆ™[[Ý™YHÛÙKXÛÛ™š\›YY^[XZØYÙHÔÑˆ˜]\ˆ[ˆY[™Â™Ù[™\šXÈØ]\ÈÜˆX™[ËˆHš[ÜˆYXÚ[š\ÛK]^ØÛÜ™H›ÛÜÝ[‚˜Ù[ÛY]žWÜ™]šY]˜[œXØ\È™[[Ý™YHØØ[YØ[™X[˜ÚÜˆØÛÜ™H˜\ÙYÛ‚œ›Þ[X[ÓÔTÔTYØ[™ÛÛ^Ø\ÈYY™]šY]˜[Y]Y]H›ÝÂ™XÛ\™\È^ÛYYXZØYÙK\›Û™HšY[Ë[™™YÜ™\ÜÚ[Ûˆ\ÝÈ™\šYžH]›YXÚ[š\ÛH^›ÈÛ™Ù\ˆÚ[™Ù\ÈHØÛÜ™Kˆ™Yœ™\ÚYKÌKH™]šY]˜[šÛÝ]X™[Y˜XÝÜžKÙ[XÝYTˆÝ™\œšYK[™^\›˜[]\š\ÝXËXÛÛ›Û˜\Y˜XÝÈ™\Ù\™H\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙB››Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Ë[™ÛÝ[X›KÚ[\Ü\™XYB™^\›˜[›ÝÜËˆ\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWÙØ]WØÚXÚ×ÌLšœÛÛ˜Ý[\ÜÙ\ÂŒŒKÌŒNÈY\ˆHÝ\œ™[™Y™\™[˜ÙK\ØÜ™Y[ˆØ]H[YÜ˜][Û‹˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜\ÜÙ\ÈKÍK‚‘š[˜[™\šYšXØ][ÛˆY\ˆ™YÙ[™\˜]Y\Y˜XÝÎˆŽLˆ[š]\ÝË˜˜[Y]XÛÛ\[X[Ú]Y™ˆKXÚXÚØ[™”ÓÓˆ\Y˜XÝ\œÚ[™È\ÜÙY‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕŒŒŒÎˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑˆ\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆŽL[š]\ÝÈ\ÜÙY˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ËHKH™]šY]È™[XZ[™Y››Û‹\›Û[ÝX›H[™™]šY]Ë[Û›KH]\Ý\Y˜XÝÈ[™XYHÛÛZ[™YBœ›ÞHÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ][™HL‹\›ÝÈTÓKLˆ™\™\Ù[][ÛˆØ[\K˜[™HÛÙH[œÜXÝ[Ûˆ›Ý[™HÜÚ]]™HYXÚ[š\ÛK]^ØÛÜš[™È]]Ø\È›ÝÛÛ\]X›HÚ]Üœ[‹Y[žž[YH\ØÛÝ™\žHÛZ[\Ë‚‚[ˆX\›Y\ˆÔÑˆ[ˆ™[[Ý™YHÙ[XÝYTˆÚ[™ÛK\Ú[›ØÚÙ\ˆ[ˆ›Ý[™Y™›Ü›KˆH™]Â˜Z[\Ù[XÝY\‹[Ý™\œšY\ØÛÛ[X[™›ÙXÙ\Â˜\Y˜XÝËÝŒ×ÜÙ[XÝYÜ—ÛÝ™\œšYWÜ[—ÍÌšœÛÛ˜œ›ÛHHÛË\™Y™\™[˜ÙB˜]Y][™™[YYX][Ûˆ[‹ˆH[ˆ\Y\ÈWØÜØNMÍØOˆPUÐ˜[™˜WØÜØNXOˆRÓ˜Ú]^XÚ]™[X\Y™\ÚYYHÜÚ][ÛœËÙY\Â˜WØÜØNNL˜ÚÚ\Y™XØ]\ÙH]ÈÛXÛÚÚ[˜\ÙH™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚÝ[œ™\]Z\™\È™]šY]Ë[™™XÛÜ™ÈÛÝ[X›HX™[Ø[™Y]\ËˆHÝÛœÝ™X[BŒKXÛÛ^Ù[XÝYTˆÝ™\œšYHÙ[ÛY]žKÜ™]šY]˜[Ù]˜[X][Ûˆ\Y˜XÝÂœ™\Ù\™H\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœË˜[™XÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Ë‚‚•\È[ˆ[ÛÈÛÛ™\YH^\›˜[›ØÚÙ\ˆX]š^[ÈH›Ý[™Y[Ýœš[Üš]H\Y˜XÝ[œÝXYÙˆ[›Ý\ˆÙ[™\šXÈØ]KˆH™]Â˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝØØ[™Y]WÜš[Üš]WÌLKšœÛÛ˜Ù[XÝÈLœ™]šY]Ë[Û›HØ[™Y]\ÈXÜ›ÜÜÈH^\›˜[[™\ËØ\È[™HÙ[XÝ[Ûˆ]‹™Y™\œÈH^XÝZÛÝ]Üˆ™X\‹Y\XØ]H›ÝÜË™XÛÜ™Â˜^\›˜[Ü[ÝØØ[™Y]WÜ˜[šÚ[™Ø\ÈH›ØÚÙ\ˆ™[[Ý™Y[™ÙY\È]™\žH›ÝÂ››Û‹XÛÝ[X›H[™›Ý[\Ü\™XYKˆ]ÈXZØYÙH›Ý™[˜[˜ÙH™XÛÜ™È]›YXÚ[š\ÛH^PËÔšXHY[YšY\œËÛÝ\˜ÙHX™[Ë[™\™Ù]X™[È\™H›Ýœš[Üš]K\ØÛÜš[™È]šY[˜ÙKˆHÛÛ\[š[Û‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÜ™]šY]×ÙXÚ\Ú[Û—Ù^ÜÌLKšœÛÛ˜^ÜÂÜÙHL›ÝÜÈ\È›ËYXÚ\Ú[Ûˆ™]šY]ÈXÚÙ]ÈÚ]ÛÛ\]YXÚ\Ú[ÛœË‚•\È[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙ]šY[˜ÙWÜXÚÙ]ÌLKšœÛÛ˜ÚXÚ˜ÛÛœÛÛY]\ÈÎHÛÝ\˜ÙH\™Ù]È›ÜˆÜÙHÙ[XÝY›ÝÜÎˆ[LÙ\]Y[˜ÙK\ÙX\˜ÚœXÚÙ]È\ÈÈXÝ]™K\Ú]HÛÝ\˜Ú[™ÈXÚÙ]Ëˆ]\ÈÝX\™˜Z[XÛX[‹\È›Z\ÜÚ[™È™\]Z\™YÛÝ\˜ÙHXÚÙ]Ë[™ÙY\È]™\žH›ÝÈ™]šY]Ë[Û›K›Û‹XÛÝ[X›K˜[™›Ý[\Ü\™XYK‚•\È[ˆ[ˆYY˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝÙ]šY[˜ÙWÙÜÜÚY\œ×ÌLKšœÛÛ˜ÚXÚ˜\ÜÙ[X›\ÈHØ[YHÙ[XÝYL[È\‹XØ[™Y]H™]šY]ÈÜÜÚY\œËˆÙ]™[ˆ]™B™^XÚ][šT›ÝXÝ]™K\Ú]H™X]\™HÝ\Ü[L]™HšXH™XXÝ[Û‚˜ÛÛ^›Ý\ˆ]™H™\™\Ù[][Û‹\Ø[\H›ÝÜË[™[LÝ[Ø\œžH[\Ü˜›ØÚÙ\œËˆHÜÜÚY\ˆ\Y˜XÝ™[[Ý™\ÈÛ›HH[Ý]šY[˜ÙKX\ÜÙ[X›B˜›ØÚÙ\ŽÈ]Ù\È›Ý]]Üš^™H^\›˜[[\ÜˆÜÜÚY\ˆ\ÜÙ[X›H›ÝÈ[ÛÈYÂ›ØØ[]šY[˜ÙKXÛÛ\][™\ÜÈ›ØÚÙ\œËÛÈÙ[XÝY›ÝÜÈZ\ÜÚ[™È^XÚ]˜XÝ]™K\Ú]H]šY[˜ÙH
ÍŒMŽÎMLL[™LMN[ˆHÝ\œ™[[Ý
BœÝ^H›ØÚÙY]™[ˆYˆ[ˆ\Ý™X[H›ØÚÙ\ˆX]š^ÛÙ\ÈÝ[K‚‚“]\Ý[ˆYYH\™XÝ^\›˜[\[ÝÔÑˆØY™YÝX\™˜]\ˆ[ˆ[›Ý\‚˜ÛÝ[YÜ›ÝÝØ]KˆÚXÚ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]\Ø›ÝÈ\È›Ý\‚œ[Ý\ÜXÚYšXÈÚXÚÜÎˆš[Üš]H›ÝÜÈ]\Ý™[XZ[ˆXZØYÙK\ØY™H[™™]šY]Ë[Û›Kœ[Ý™]šY]ËYXÚ\Ú[Ûˆ^ÜÈ]\ÝÝ^H›ËYXÚ\Ú[ÛˆÚ]ÛÛ\]YXÚ\Ú[ÛœËœ[Ý]šY[˜ÙHXÚÙ]È]\ÝÝ^HÝX\™˜Z[XÛX[ˆ™]šY]ÈXÚÙ]ÈÚ]ÛÝ\˜ÙB\™Ù]Ë[™[ÝÜÜÚY\œÈ]\Ý™[XZ[ˆ›Û‹XÛÝ[X›H]šY[˜ÙHÝ[[X\šY\ËˆBœØ[YHÛÙH]›ÝÈYÈØØ[ÜÜÚY\ˆ›ØÚÙ\œÈ›ÜˆZ\ÜÚ[™È^XÚ]XÝ]™K\Ú]B™]šY[˜ÙKZ\ÜÚ[™ÈÜXÚYšXÈ™XXÝ[ÛˆÛÛ^[™™X\‹Y\XØ]HÙ\]Y[˜ÙB˜[\ËˆH[ÝØ]HÙÚXÈ]™\È[ˆH›ØÝ\ÙY[\ˆ˜]\ˆ[ˆ[›Ý\‚›\™ÙHœ˜[˜ÚØ\ØØYH[œÚYHH^\›˜[˜[œÙ™\ˆØ]KˆH™YØ]]™H™YÜ™\ÜÚ[Û‚\Ý˜Z[ÈHÛÛ\]Y[ÝXÚ\Ú[Û‹[™H™YÙ[™\˜]Y˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜™XÛÜ™ÈKÍBœ\ÜÚ[™ÈÚXÚÜÈÚ]LÙ[XÝY[ÝØ[™Y]\ËÛÛ\]Y[ÝXÚ\Ú[ÛœËÎHÛÝ\˜ÙH\™Ù]Ë[™LÜÜÚY\ˆ›ÝÜÈ]Ý[Ø\œžH[\Ü›ØÚÙ\œËˆB™ÜÜÚY\ˆY]Y]H›ÝÈ™XÛÜ™ÈÈØØ[^XÚ]XXÝ]™K\Ú]H]šY[˜ÙH›ØÚÙ\œÈ[™ŒZ\ÜÚ[™Ë\ÜXÚYšXË\™XXÝ[Ûˆ›ØÚÙ\œÈ›ÜˆHÝ\œ™[Ù[XÝY[Ý›ÝÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕNŒŒÎŒLVˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑˆ\™[š[™Ë‚‘]šY[˜ÙH][ˆÝ\ˆŽÈ[š]\ÝÈ\ÜÙY˜[Y]X\ÜÙYÚ]ÎB˜Ý\˜]YX™[ËH]\ÝØÜÈ[™\Y˜XÝÈ[™XYHÛÛZ[™YH›ÞBœÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]\ÈHL‹\›ÝÈTÓKLˆ™\™\Ù[][ÛˆØ[\K[™HÝ\œ™[KHÝ]H™[XZ[™Y™]šY]Ë[Û›HÚ]ÛÝ[X›KÚ[\Ü\™XYB™^\›˜[›ÝÜËˆ\š[™ÈH[‹›ÛÙYZØ[\Ù\\Ø›\Ý[™X[[Û™Ù\™HXœÙ[ÛˆUÛÈ™X[Ù\]Y[˜ÙKÙ›ÛÙ\\˜][Ûˆ™[XZ[™Y›ØÚÙYˆBœ[ˆ\™Y›Ü™H\™[™YH^\›˜[[Ý™]šY]ËYXÚ\Ú[ÛˆÔÑˆ[™Ù\KPÔÐB˜ÛÝ[Ü›ÝÝ[™^\›˜[[\ÜÝÜY‚‚”™[XZ[š[™Ë][YH[ˆ^XÝ]Y[ˆHØ[YH[ŽˆY\ˆH™]šY]ËYXÚ\Ú[ÛˆØ]BœØY™YÝX\™\ÜÙY\ÙHH™[XZ[š[™È›Ý[™YÚ[™ÝÈÈXZÙHH[ÝÜÜÚY\‚œ]\ÜÈ\[™[ÛˆÝ[H\Ý™X[H›ØÚÙ\œËˆ]YYØØ[XÝ]™K\Ú]Kœ™XXÝ[Û‹XÛÛ^[™Ù\]Y[˜ÙKX[\›ØÚÙ\œËÝ[[X\š^™YÜÙH›ØÚÙ\œÈ[‚™ÜÜÚY\ˆY]Y]KÙ[˜[^™YH[Ý[\Ü™]šY]Ë\™\]Z\™[Y[\Ý[™›XYHHØ]H™\]Z\™HÙ[XÝY[Ý›ÝÜÈÈ™H[YÚX›H[™›ØÚÙ\‹Yœ™YK‚‚“™^Ü™\™YÛÜšÛ\Ý‚‚ŒKˆ™X]^\›˜[˜[œÙ™\ˆ\Y˜XÝ\][™XYÙH\È[™Y›ÜˆHÝ\œ™[ˆKHØ]H[™HÝ\œ™[[\Ü\™XY[™\ÜË›ØÚÙ\‹[X]š^[Ý\XÚÙ]ˆ[™[ÝYÜÜÚY\ˆZ[\œÎˆ›ÝË[]™[Ø[™Y]H[™XYÙK]Z[™™\œ™YˆÛXÙH[™XYÙK[™^[ØYYXÛ\™YÛXÙHÛÛ˜YXÝ[ÛœÈ›ÝÈ˜Z[™Y›Ü™HBˆØ]HÜˆYÚY˜[‹Z[ˆZ[\ˆØ[ˆÚ[[H\ÜË[™[Ýš[Üš]KÜ™]šY]ËÂˆ]šY[˜ÙKÙÜÜÚY\ˆ\Y˜XÝÈ›ÝÈ˜Z[Yˆ^HÝÜ™Z[™È™]šY]Ë[Û›KÛ›ËBˆXÚ\Ú[ÛˆÛÜšÈ›ÙXÝËˆÛÛ[YH\Y˜XÝÜ˜\ÛÛœÚ\Ý[˜ÞHÛ›HÚ\™H™]ÂˆÛÙH]šY[˜ÙHÚÝÜÈ[›Ý\ˆYÚY˜[‹Z[ˆ]Y]Ø[ˆZ^ÛÝ\˜ÙHÛXÙKÜ˜\YˆX™[˜]ÚÜˆ\Y˜XÝ[™XYÙHÚ]Ý]H™YØ]]™H™YÜ™\ÜÚ[Û‹‚Œ‹ˆÙ\]Y[˜ÙKY\Ý[˜ÙHÛÝ]]˜[X][Ûˆ\È[\[Y[YÚ]H™X[S\Ù\\Ì‚ˆ˜XÚÙ[™[™[›™YžH™YÜ™\ÜÚ[Ûˆ\ÝËˆ™X]HÙ\]Y[˜ÙKZY[]HÜ]\Âˆ™X[›ÜˆHXØÙ\YÛÝ[X›H™YÚ\ÝžNˆÎÍÎ]˜[X]YX™[È\™BˆÛÝ™\™YÌÎÙ\]Y[˜ÙH™XÛÜ™È\™HÛ\Ý\™Y]Ì	HY[]H[™	BˆÛÝ™\˜YÙK[™X^ØœÙ\™Y˜Z[‹Ý\ÝY[]H\ÈŒŽˆH™]Z[™Yˆ›ÞHšY[È\™H˜[˜XÚÈÛÛ^Û›Kˆ›ÛÙYZÈ\È]˜Z[X›H[ˆBˆ[\Ü˜\žHÛÛ™H[ˆÜš]˜]KÝ\ØØ][]XËY›ÛÙYZËY[˜ˆH™]Âˆ›ÛÙYZÈÛÛÜ™[˜]K\™XY[™\ÜÈ\Y˜XÝÝYÙ\ÈHÙ[XÝYˆ[PÒQ‚ˆš[\È[™™XÛÜ™ÈÍˆX]\šX[^˜X›H›ÝÜÈ\ÈÛÈZ\ÜÚ[™ÈÙ[XÝYˆÝXÝ\™\ËˆH\X[ÝYÙYXÛÛÜ™[˜]HHÚYÛ˜[^\ÝÈ›ÜˆÜÙHHš[\Ëˆ][K\ØÛÜ™HÙ\\˜][Ûˆ™[XZ[œÈZ\ÜÚ[™È[[H™[XZ[š[™ÈÛÛÜ™[˜]\Âˆ\™HÝYÙY[™HÝXÝ\˜[˜XÚÙ[™\ÈÚ\™Y[‹‚ŒËˆ\ÙHHX\›™Y™\™\Ù[][Ûˆ˜XÚÙ[™][Ýš[Üš]H\Y˜XÝˆ›ËYXÚ\Ú[Ûˆ™]šY]È^Ü[Ý]šY[˜ÙHXÚÙ][Ý\ÜXÚYšXÂˆ™\™\Ù[][ÛˆØ[\K[™[Ý]šY[˜ÙHÜÜÚY\œÈ›Üˆ™]šY]Ù\ˆÛÜšËˆBˆØ[›ÛšXØ[L‹\›ÝÈX\YXÛÛ›ÛTÓKLˆHØ[\H[™HL\›ÝÈÙ[XÝY\[ÝˆTÓKLˆHØ[\H\™H›ÝÛÛ\]Y[™™]šY]Ë[Û›KˆHLHÚYXØ\œÈ\™Bˆ[\[Y[Y]Ý\œ™[H[˜]˜Z[X›H™XØ]\ÙHH[Ù[\È›ÝØXÚYˆØØ[NÈÈ›Ý™X][H\ÈÛÛ\]Y[X™Y[™ÜÈ[[H[Ù[Ø[ˆ™BˆØYYˆH™^ÛÜšÈ\ÈÈš[]šY[˜ÙHXÚ\Ú[ÛœÈœ›ÛHH\‹XØ[™Y]BˆÜÜÚY\‹ÜÛÝ\˜ÙK]\™Ù]›ÝÜÈÚ[H™\Ù\š[™È]\š\ÝXÈÙ[ÛY]žH™]šY]˜[\ÂˆH˜\Ù[[™K‚ˆ™]šY]Ù\ˆÛXÞH[™ØÚ[XH\[™È\™HÝÙ\ˆš[Üš]H[›\ÜÈÛÙH]šY[˜ÙBˆ^ÜÙ\È™]È[XšYÝZ]H[ˆÛÝ[X›HœÈ™]šY]Ë[Û›H[\ÜÈÜˆYÚY˜[‹Z[‚ˆ\Y˜XÝØÚ[X\Ë‚KˆÙY\TÈ[™˜[œÚ][Û‹\Ý]HÚYÛ˜]\™HÛÜšÈÝÙ\ˆš[Üš]H[[HÔÑ‚ˆ[™^\›˜[\[Ý›ØÚÙ\œÈX›Ý™H\™HZ]\ˆš^YÜˆ^XÚ]H›ØÚÙY‚‚ÛÛ˜Ü™]H\Ù\ˆ\™XÝ[Ûˆ›ÜˆH™^[œÎˆÝÜY[™ÈXœÝ˜XÝØ]\È[›\ÜÂ^H\™XÝH[˜›ØÚÈHš\œÝ^\›˜[\ÛÝ\˜ÙH[\Ü[ÝˆHKB˜ÚXÚÜÚ[[™XYH›Ý™YHÙ^HÝ˜]YÚXÈÚ[ˆKPÔÐK[Û›HÛÝ[Ü›ÝÝ\ÂœÛÝ\˜ÙK[[Z]YÚ[H^\›˜[\ÛÝ\˜ÙH[\Ü\È›ÝY]™XYKˆH™^˜[XX›HÛÜšÈ\È›ÝH\™Ù\ˆØ]HÛÝ[È]\ÈHÛX[]šY[˜ÙKX˜XÚÙY™^\›˜[[Ý‚‚’[[YYX]H\™Ù]ˆY˜[˜ÙHHLÙ[XÝYØ[™Y]\È[‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ[ÝØØ[™Y]WÜš[Üš]WÌLKšœÛÛ˜œ›ÛHBŒÌ\›ÝÈ[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[\KˆÙY\]™\žH^\›˜[›ÝÈ™]šY]Ë[Û›H[[˜XÝ]™K\Ú]K™XXÝ[Û‹Ù\]Y[˜ÙK™\™\Ù[][Û‹™]šY]Ë[™[X™[Y˜XÝÜžB™Ø]\È\ÜËˆÈ›ÝÜ[ˆ[›Ý\ˆKPÔÐK[Û›H˜[˜ÚHÝXÚ\ÈKL\È›Ü›X[œ›ÙÜ™\ÜË‚‚”š[Üš]H›ØÚÙ\œÈÈ™[[Ý™N‚‚ŒKˆÛÝ\˜ÙH^XÚ]Ø][]XÈÜˆXÝ]™K\Ú]H™\ÚYYH]šY[˜ÙH›ÜˆHLˆXÝ]™K\Ú]KY™X]\™HØ\›ÝÜÈ\Ú[™Âˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ù^ÜÌLKšœÛÛ˜‚ˆš[™[™ÈÛÛ^[™šXHÛÛ^\™H\ÙY[]^HÈ›Ý™\XÙBˆØ][]XÈXÝ]™K\Ú]H]šY[˜ÙK‚Œ‹ˆÛÛ\]H™X[™X\‹Y\XØ]HÜˆ[šT™Y‹\Ý[HÙ\]Y[˜ÙHÙX\˜Ú\È›ÜˆHŽˆ›ÝÜÈ[ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÜÙX\˜ÚÙ^ÜÌLKšœÛÛ˜‚ˆ^XÝ\™Y™\™[˜ÙHÝ™\›\È[™YÚ\Ú[Z[\š]H›ÝÜÈÝ^HÛÝ]ÛÛ›ÛË›ÝˆX™[Ë‚ŒËˆ\ÙHHÛÛ\]YTÓKLˆ™\™\Ù[][ÛˆØ[\KH[Ý\š[Üš]H\Y˜XÝˆ[™HÛÛœÛÛY]Y[Ý]šY[˜ÙHXÚÙ]È™\\™H™\™\Ù[][Ûˆ™\Z\‚ˆÜˆ™]šY]Ù\ˆXÚ\Ú[ÛœÈ›ÜˆHLÙ[XÝYØ[™Y]\Ëˆ™\Ù\™H]\š\ÝXÂˆÙ[ÛY]žH™]šY]˜[\ÈH™\]Z\™YÛÛ›Û˜\Ù[[™K‚ˆY˜[˜ÙHHLÙ[XÝY[ÝØ[™Y]\ÈÝØ\™^XÚ]XÝ]™K\Ú]Bˆ]šY[˜ÙKÜXÚYšXÈ™XXÝ[Ûˆ]šY[˜ÙKÛX[ˆÙ\]Y[˜ÙHÛÝ]Ý]\ËÛX[‚ˆÝXÝ\™HX\[™Ë›Û‹XÛÛ\ÙY]\š\ÝXËÜ™\™\Ù[][Ûˆ™Z]š[Ü‹[™›Âˆœ›ØYQPÈ[XšYÝZ]K‚Kˆš[H›ËYXÚ\Ú[Ûˆ™]šY]ÈXÚÙ]ÈÛ›HY\ˆ]šY[˜ÙH\È\ÜÙ[X›YˆÙY\ˆXÚ\Ú[ÛœÈ™]šY]Ë[Û›Hš\œÝˆ][\ÛÝ[X›H[\ÜÛ›H›ÜˆØ[™Y]\Âˆ]\ÜÈXÝ]™K\Ú]K™XXÝ[Û‹Ù\]Y[˜ÙK™\™\Ù[][Û‹™]šY]Ë[™[ˆ˜XÝÜžHØ]\Ë‚‚‘Yš[š][ÛˆÙˆÛ™H›Üˆ\È]›ÝˆKLL˜[YY^\›˜[Ø[™Y]\È]™Bœ\‹\›ÝÈ]šY[˜ÙHÜÜÚY\œÈÛÝ™\š[™ÈXÝ]™K\Ú]H™\ÚYY\Ë™XXÝ[Û‹ÛYXÚ[š\ÛB™]šY[˜ÙKÝXÝ\™HX\[™ËÙ\]Y[˜ÙHÛÝ]Û™X\‹Y\XØ]HÝ]\Ë]\š\ÝXÂœ™]šY]˜[ÛÛ›Û™\™\Ù[][ÛˆÛÛ›Û[™™[XZ[š[™È›ØÚÙ\œËˆYˆ›Â˜Ø[™Y]H\È[\Ü\™XYKHÝ]]ÚÝ[™HH˜[šÙY›ØÚÙ\ˆ\Ý›ÜˆBœ[Ý›Ý[Ü™HÙ[™\šXÈ]Y]XXÚ[™\žK‚‚”Ý\œ›ÛHHXØÙ\YKÝ]H\ÈH›Û‹\›Û[ÝYKH™]šY]ËˆB˜Ø[›ÛšXØ[™YÚ\ÝžH™[XZ[œÈ]ÎHÛÝ[X›HX™[ÎÈH]\ÝXØÙ\YX™[Â˜\™HÝ[WØÜØNŽMÎWØÜØNŽNWØÜØNŽNL[™WØÜØNŽNM‚‚•H›Ý[™YKH™]šY]È™[XZ[œÈÜ[ˆ]›Ý›Û[ÝX›KˆH™]šY]ÈØ]Bœ\ÜÙ\ÈŒKÌŒHÚXÚÜË]˜\Y˜XÝËÝŒ×ÛX™[Ø˜]ÚØXØÙ\[˜ÙWØÚXÚ×ÌLWÜ™]šY]ËšœÛÛ˜\È›ÝXØÙ\Y™›ÜˆÛÝ[[™È™XØ]\ÙH]YÈÛX[ˆÛÝ[X›HX™[Ëˆ™]šY]ÈXš\Ù\Èœ›ÛBŒÌˆÈÌŽH›ÝÜËÚ]™]È›ÝÜÈWØÜØNŒLØWØÜØNŒL[™WØÜØNŒLX˜[^XÚ]HY™\œ™YžB˜\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÌLWÜ™]šY]ËšœÛÛ˜‚‚•HKH[ˆ^ÜÙYHÛÝ\˜ÙK\ØØ[H›Ý[™XÚÈ˜]\ˆ[ˆHX™[\]X[]B™˜Z[\™Kˆ\Y˜XÝËÝŒ×ÜÛÝ\˜ÙWÜØØ[WÛ[Z]Ø]Y]ÌLKšœÛÛ˜™XÛÜ™ÈKÂ›ØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™È›ÜˆH™\]Y\ÝYKH˜[˜ÚH[™™XÛÛ[Y[™ÂœÝÜ[™ÈKPÔÐK[Û›HÛÝ[Ü›ÝÝˆH^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆ]\È›ÝÂ™Ø]Y›Üˆ™]šY]Ë[Û›H]šY[˜ÙHÛÛXÝ[Ûˆ˜]\ˆ[ˆÛÝ[Ü›ÝÝ‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ]Y\žWÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÛÛÙØØ[Xœ˜][Û—Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÛX[šY™\ÝØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÛ[™WØ˜[[˜ÙWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ]šY[˜ÙWÜ[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ]šY[˜ÙWÜ™\]Y\ÝÙ^ÜÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙ]šY[˜ÙWÜ]Y]YWÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙ]šY[˜ÙWÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙ]šY[˜ÙWÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜ]Y]YWÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜ]Y]YWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×ÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×ÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜØÛÜ™\×ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜØÛÜ™\×Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ˜Z[\™WÛ[ÙWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØÛÛ›ÛÜ™\Z\—Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØÛÛ›ÛÜ™\Z\—Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛÛX[šY™\ÝØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛØÛÛ\\š\ÛÛ—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛØÛÛ\\š\ÛÛ—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^Ü™\Z\—Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^Ü™\Z\—Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^ÛX\[™×ÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^ÛX\[™×ÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙØ\ÜÛÝ\˜ÙWÜ™\]Y\Ý×ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÚÛÝ]Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÛ™ZYÚ›ÜšÛÙÜ[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÛ™ZYÚ›ÜšÛÙÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÛ™ZYÚ›ÜšÛÙÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWØ[YÛ›Y[Ý™\šYšXØ][Û—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWØ[YÛ›Y[Ý™\šYšXØ][Û—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÜÙX\˜ÚÙ^ÜÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÜÙX\˜ÚÙ^ÜØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ[\ÜÜ™XY[™\Ü×Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü]Y]YWÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü]Y]YWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ù^ÜÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ù^ÜØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü™\ÛÛ][Û—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü™\ÛÛ][Û—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—Ø›ØÚÙ\—ÛX]š^ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—Ø›ØÚÙ\—ÛX]š^Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™]šY]×ÛÛ›WÚ[\ÜÜØY™]WØ]Y]ÌLKšœÛÛ˜[™˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜ÙY\˜ÛÝ[X›WÛX™[ØØ[™Y]WØÛÝ[L[™\ÜÈHËÍÈ™]šY]Ë[Û›H˜[œÙ™\ˆØ]K‚•HØ[™Y]HX[šY™\Ý\ÈÌ[šT›ÝÐ‹ÔÝÚ\ÜËT›Ý›ÝÜÈXÜ›ÜÜÈÚ^˜[[˜ÙYœ]Y\žH[™\ÎÈÌMMLØ[™ŒL˜\™H^XÝ\™Y™\™[˜ÙHÝ™\›\È[™\™H›Ý]YÈÙ\]Y[˜ÙKZÛÝ]ÛÛ›ÛËˆH]šY[˜ÙH[ˆ›YÜÈÙ]™[ˆœ›ØYÚ[˜ÛÛ\]HPÂ˜ÛÛ^ÎÈHXÝ]™K\Ú]H]Y]YH^ÜÈH™XYH]šY[˜ÙH›ÝÜÈ[™Y™\œÈš]™Bœ›ÝÜË[˜ÛY[™ÈÛÈ^XÝ\™Y™\™[˜ÙHÛÝ]È[™™YHœ›ØYQPÈ\Ø[XšYÝX][Û‚˜Ø\Ù\Ë‚‚‘^\›˜[XÝ]™K\Ú]H[™ÛÛ›ÛÛÜšÈ\Èœ›ØY\ˆ›ÝËˆH[šT›ÝÐˆ™X]\™BœØ[\HÛÝ™\œÈ[HXÝ]™K\Ú]K\™XYH›ÝÜÎˆMH]™HXÝ]™K\Ú]H™X]\™\ËLœ™[XZ[ˆXÝ]™K\Ú]KY™X]\™HØ\Ë[™[Ø[\Y›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›KˆBš]\š\ÝXËXÛÛ›Û]Y]YHX\šÜÈLˆØ[™Y]\È™XYH›ÜˆÛÛ›Û›ÝÝ\[™È[™™Y™\œÈLÈ›ÝÜËˆH^[™YÝXÝ\™K[X\[™ÈØ[\HX\È[L‚š]\š\ÝXË\™XYHÛÛ›ÛÈÛÈÝ\œ™[[Q›Û[Ù[ÒQœË™\ÛÛ™\È[œ™\]Y\ÝYXÝ]™K\Ú]HÜÚ][ÛœË[™[ˆ[œÈH^\Ý[™ÈÙ[ÛY]žH™]šY]˜[š]\š\ÝXÈ\ÈHÛÛ›ÛˆH]\š\ÝXÈ\È›ÝX™[\™XYNˆÜH™YXÝ[ÛœÈ\™BŽHY][Ù\[™[ÚY›Û\ÙXˆ[YWÜ\›ÞY\ÙWÛÞY\ÙX[™B˜›]š[—ÙZY›ÙÙ[˜\ÙWÜ™YXÝ\ÙXÚ]HØÛÜKÝÜHZ\ÛX]Ú\ËˆB™˜Z[\™K[[ÙH]Y]™XÛÜ™ÈXÝ]™K\Ú]H™X]\™HØ\Ëœ›ØYQPÈ\Ø[XšYÝX][Û‚›™YYËÜHš[™Ù\œš[ÛÛ\ÙKY][ZY›Û\ÙHÛÛ\ÙK[™ØÛÜKÝÜB›Z\ÛX]Ú\È™]šY]Ë[Û›H˜Z[\™\ÈÈ™\Z\ˆ™Y›Ü™H[žH^\›˜[X™[XÚ\Ú[Û‹‚•HXÝ]™K\Ú]H™X]\™KYØ\›ÝÜÈ\™HÍŒMŽŽLÍÌ˜ÌML”•PÍ˜LMNÎMLLNR’ÎXMTØÌŒNX[™LÌ”X‚‚•H™]ÈÛÛ›Û\™\Z\ˆ\Y˜XÝÈ\›ˆHÝ\œ™[ÙXZÛ™\ÜÙ\È[ÈÛÛ˜Ü™]B››Û‹XÛÝ[X›H™\Z\ˆÛÜšËˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØÛÛ›ÛÜ™\Z\—Ü[—ÌLKšœÛÛ˜š\ÈH™\Z\ˆ›ÝÜÎˆLXÝ]™K\Ú]H™X]\™HØ\ËÈœ›ØYQPÈ\Ø[XšYÝX][Û‚œ›ÝÜË[™Lˆ]\š\ÝXËXÛÛ›Û™\Z\ˆ›ÝÜËˆH™\™\Ù[][ÛˆÛÛ›ÛX[šY™\Ý™^ÜÙ\È[LˆX\YÛÛ›ÛÈ\È]\™H™\™\Ù[][Ûˆ›ÝÜÈÚ][X™Y[™ÜÂ™^XÚ]H›ÝÛÛ\]Y[™›È˜Z[š[™ÈX™[ËˆH™\™\Ù[][ÛˆÛÛ\\š\ÛÛ‚˜YÈ™X]\™K\›ÞHÛÛ›ÛÈ›Üˆ[LˆX\Y›ÝÜË›YÜÈÈY][ZY›Û\ÙB˜ÛÛ\ÙH›ÝÜË™\Ù\™\ÈˆÛXØ[‹X›Ý[™\žH›ÝÜË[™ÙY\È]™\žH›ÝÂ››Û‹XÛÝ[X›KˆHš[™[™ËXÛÛ^™\Z\ˆ[ˆÜ]ÈHLXÝ]™K\Ú]B™™X]\™HØ\È[ÈÈ›ÝÜÈ™XYH›Üˆš[™[™ËXÛÛ^X\[™È[™È›ÝÜÈÝ[›Z\ÜÚ[™Èš[™[™ÈÛÛ^ÈHX\[™ÈØ[\HX\ÈËÍÈ™XYH›ÝÜÈÚ]™]Ú™˜Z[\™\Ëˆš[™[™ÈÜÚ][ÛœÈ™[XZ[ˆ™\Z\ˆÛÛ^Û›K›ÝØ][]XÂ˜XÝ]™K\Ú]H]šY[˜ÙKˆHXÝ]™K\Ú]HØ\ÛÝ\˜ÙK\™\]Y\Ý\Y˜XÝ›ÝÈÛÝ™\œÂ˜[LØ\È\È™]šY]Ë[Û›HÛÝ\˜Ú[™È\ÚÜË[™HXÝ]™K\Ú]HÛÝ\˜Ú[™È]Y]YBœš[Üš]^™\ÈÜÙHØ\È[ÈÈX\YXš[™[™ËXÛÛ^›ÝÜÈ[™Èš[X\žK\ÛÝ\˜ÙBœ›ÝÜË‚‚˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™XXÝ[Û—Ù]šY[˜ÙWÜØ[\WÌLKšœÛÛ˜›ÝÈ]Y\šY\Â”šXH›Üˆ[Ì^\›˜[Ø[™Y]\Ëˆ]™XÛÜ™È™XXÝ[Û‹XÛÛ^›ÝÜÈÚ]™™]Ú˜Z[\™\È[™™[XZ[œÈ›Û‹XÛÝ[X›Kˆ]ÈÛÛ\[š[Ûˆ]Y]˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™XXÝ[Û—Ù]šY[˜ÙWÜØ[\WØ]Y]ÌLKšœÛÛ˜\Â™ÝX\™˜Z[XÛX[ˆ]›YÜÈMˆœ›ØYQPÈÛÛ^›ÝÜÈXÜ›ÜÜÈKŒKŒK‹X˜KŒLKŒK‹XKŽ‹K‹X‹ŒKŒK‹X‹ËŒK‹XËŒ‹Œ‹‹X[™Œ‹ŽNK‹XÂÜÙH›ÝÜÈ\™H›ÝÜXÚYšXÈYXÚ[š\ÛH]šY[˜ÙKˆHÙ\]Y[˜ÙKZÛÝ]]Y]šÙY\ÈÌMMLØ[™ŒL˜\È^XÝ\™Y™\™[˜ÙHÛÝ]È[™X\šÜÈH™[XZ[š[™ÂŒŽØ[™Y]\È\È™X\‹Y\XØ]K\ÙX\˜ÚØ\Ù\È™Y›Ü™H[žH]\™H[\ÜXÚ\Ú[Û‹‚•Hœ›ØYQPÈ\Ø[XšYÝX][Ûˆ]Y]š[™ÈÜXÚYšXÈ™XXÝ[ÛˆÛÛ^›Üˆ[Â˜œ›ØY[Û›H™\Z\ˆ›ÝÜË[™HÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙ[ˆÛÛ™\ÈBœÙ\]Y[˜ÙHÝ\™˜XÙH[Èˆ^XÝZÛÝ]›ÝÜÈ[™Ž™X\‹Y\XØ]HÙX\˜Úœ™\]Y\ÝËˆHÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙØ[\H™]Ú\È[Ì^\›˜[Ù\]Y[˜Ù\Â˜[™[ÌÍHÝ\œ™[ÛÝ[X›HKPÔÐH™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœÈY\ˆ™\ÛÛš[™Âš[˜XÝ]™H[Y\™ÙY™Y™\™[˜Ù\Ëš[™ÈYÚ\Ú[Z[\š]H[\È[ˆH›Ý[™Y[˜[YÛ™YØÜ™Y[‹[™H™X[S\Ù\\Ìˆ˜XÚÙ[™Ù\]Y[˜ÙK\ÙX\˜Ú\Y˜XÝÛÛ\\™\Â˜[Ì^\›˜[›ÝÜÈYØZ[œÝÌÍHÝ\œ™[™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœÈÈÌÍÈÙ\]Y[˜ÙBœ™XÛÜ™Ëˆ]˜XÚÙ[™ÙX\˜Ú™XÛÜ™ÈŽ›Ë\ÚYÛ˜[›ÝÜËˆ^XÝ\™Y™\™[˜ÙBšÛÝ]Ë™X\‹Y\XØ]H›ÝÜË[™˜Z[\™\ËÛX\š[™È›Ý[™Y˜Ý\œ™[\™Y™\™[˜ÙH˜XÚÙ[™ÙX\˜ÚX›ÜˆHŽ›Ë\ÚYÛ˜[›ÝÜËˆH^\›˜[˜[]œËX[Ù\]Y[˜ÙHØÜ™Y[ˆ›ÝÈÛX\œÈHÝ\œ™[Ì\›ÝÈØ[™Y]KXØ[™Y]B™\XØ]HØÜ™Y[ˆÚ]™X\‹Y\XØ]HZ\œËÚ[H[šT™Y‹]ÚYH\XØ]BœØÜ™Y[š[™È™[XZ[œÈH[Z]][Ûˆ™Y›Ü™H[\Ü‚•H›Ý[™Y[YÛ›Y[™\šYšXØ][Û‚˜ÚXÚÜÈLÜZ]Z\œËÛÛ™š\›\ÈÌMMLØ[™ŒL˜\È^XÝÛÝ]Ë[™œ™XÛÜ™È›Ë\ÚYÛ˜[Z\œËˆH[\Ü\™XY[™\ÜÈ]Y]ÙY\È›ÝÜÈ™XYH›Ü‚›X™[[\Ü[™™XÛÜ™ÈLXÝ]™K\Ú]HØ\Ëˆ^XÝÙ\]Y[˜ÙHÛÝ]ËBš]\š\ÝXÈØÛÜKÝÜHZ\ÛX]Ú\ËŽH™\™\Ù[][Û‹XÛÛ›Û\ÜÝY\Ë[šT™Y‹]ÚYB™\XØ]K\ØÜ™Y[š[™È[Z]][ÛœË[™ˆ[YÛ›Y[XÛÛ™š\›YYÙ\]Y[˜ÙHÛÝ]Ë‚•HÙ\]Y[˜ÙK\ÙX\˜Ú^ÜÛÛ™\È[Ì›ÝÜÈ[È›ËYXÚ\Ú[ÛˆÙ\]Y[˜ÙB˜ÛÛ›ÛÎÈH˜XÚÙ[™ÙX\˜ÚØ\œšY\ÈHŽÝ\œ™[\™Y™\™[˜ÙH›Ë\ÚYÛ˜[›ÝÜÂ˜[™ˆÙ\]Y[˜ÙKZÛÝ]\ÚÜË‚•HXÝ]™K\Ú]HÛÝ\˜Ú[™È^ÜØ\œšY\ÈÌˆÛÝ\˜ÙH\™Ù]È›ÜˆHLXÝ]™K\Ú]B™Ø\ÈÚ]ÛÛ\]YXÚ\Ú[ÛœËˆHXÝ]™K\Ú]HÛÝ\˜Ú[™È™\ÛÛ][Ûˆ™KXÚXÚÜÂÜÙHLØ\ÈYØZ[œÝ[šT›Ý™X]\™H]šY[˜ÙK™XÛÜ™È^XÚ]XÝ]™K\Ú]Bœ™\ÚYYHÛÝ\˜Ù\Ë[™ÙY\ÈHÈš[™[™Ë\\Ë\™XXÝ[Ûˆ›ÝÜÈ\ÈÈ™XXÝ[Û‹[Û›Bœ›ÝÜÈ›Û‹XÛÝ[X›KˆH™\™\Ù[][Û‹X˜XÚÙ[™[ˆÛÝ™\œÈLˆX\YÛÛ›ÛËšÙY\È[X™Y[™ÜÈXœÙ[[™™\]Z\™\È]\š\ÝXËX˜\Ù[[™HÛÛ˜\Ý›ÜˆH›ÝÜË‚•H]\›Z[š\ÝXÈË[Y\ˆ™\™\Ù[][Ûˆ˜XÚÙ[™Ø[\HÛÛ\]\È™]šY]Ë[Û›BœÙ\]Y[˜ÙHÛÛ›ÛÈ›Üˆ[Lˆ[›™Y›ÝÜË›YÜÈÛ™H™\™\Ù[][Û‚›™X\‹Y\XØ]HÛÝ]
ŒMÍYØZ[œÝWØÜØNŒÌØM
K[™Ù\È›Ýœ™\XÙHHØ[›ÛšXØ[TÓKLˆX\›™Y™\™\Ù[][ÛˆØ[\KÚXÚ›ÝÈ›ÝšY\ÂHÝ\œ™[™]šY]Ë[Û›HX\›™YÛÛ›ÛˆB˜[œÙ™\ˆ›ØÚÙ\ˆX]š^›Ú[œÈ[ÌØ[™Y]\È[Âœš[Üš]^™Y™]šY]Ë[Û›H™^XÝ[ÛœÎˆÈš[X\žH]\˜]\™KÔˆXÝ]™K\Ú]BœÛÝ\˜ÙH™]šY]ÜÈ›Üˆ›ÝÜÈÚ\™HH[šT›Ý™KXÚXÚÈ›Ý[™›È^XÚ]XÝ]™K\Ú]BœÜÚ][ÛœËÈš[X\žHXÝ]™K\Ú]HÛÝ\˜ÙH\ÚÜËN™X\‹Y\XØ]HÙ\]Y[˜ÙBœÙX\˜Ú\Ë[™ˆÙ\]Y[˜ÙHÛÝ]Ëˆ]È]Y]›ÝÈ™XÛÜ™ÈLXÝ]™K\Ú]Bœ™\ÛÛ][Ûˆ›ÝÜËLˆ™\™\Ù[][ÛˆØ[\H›ÝÜË[™Û™H™\™\Ù[][Û‚›™X\‹Y\XØ]H[\ˆ]ÈÛZ[˜[™^XXÝ[Ûˆœ˜XÝ[Ûˆ\ÈŒ[™ÛZ[˜[›[™Hœ˜XÝ[Ûˆ\ÈŒMËÛÈH]Y]YH\È›ÝÛÛ\ÙYÈÛ™HXÝ[ÛˆÜˆÛ™B˜Ú[Z\ÝžH[™K‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕLŒLŽVˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‚ÛÜšËˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™NH[š]\ÝÈ\ÜÙYHKBœ™]šY]ÈØ]H™[XZ[œÈÛX[ˆ]›Û‹\›Û[ÝX›HÚ]XØÙ\Y™]ÈX™[ËB™^\›˜[˜[œÙ™\ˆØ]H\ÜÙ\ÈKÍH™]šY]Ë[Û›HÚXÚÜË\™™YØ]]™\È™[XZ[‚Œ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆ˜XÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈH[\Ü\™XY[™\ÜÈ]Y]ÙY\È^\›˜[›ÝÜÈ[\Ü\™XYK[™XÝ]™K\Ú]KœÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙ]\š\ÝXË[™™\™\Ù[][Ûˆ›ØÚÙ\œÈ™[XZ[‚[œ™\ÛÛ™YˆHÜ\˜][Û˜[XÚ\Ú[Ûˆ\ÈÈ™YXÙH^\›˜[\ÛÝ\˜ÙH™XY[™\ÜÂ[˜Ù\Z[HÚ[HÙY\[™È]™\žH^\›˜[Ø[™Y]H›Û‹XÛÝ[X›K‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕLŒLŽVˆ[ŽˆY\ˆY[™Â˜XÝ]™K\Ú]HÛÝ\˜Ú[™È^ÜÛÛ\]HÙ\]Y[˜ÙK\ÙX\˜Ú^Üœ™\™\Ù[][Û‹X˜XÚÙ[™[›š[™ËH^\›˜[˜[œÙ™\ˆ›ØÚÙ\ˆX]š^[™BLËÍLÈ˜[œÙ™\ˆØ]K\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈ›ÜˆÝX\™˜Z[š\™[š[™Ë\Y˜XÝ™YÜ™\ÜÚ[Ûˆ\ÝË[˜[Y][Û‹”ÓÓ‹ØÛÝ[X›K[X™[œØØ[œËÓH[ÚXÚÜË[™ØÝ[Y[][Ûˆœ™\Ú™\ÜËˆÈ›ÝÜ[ˆ[ˆ^\›˜[›X™[XÚ\Ú[ÛˆÜˆ[\Ü][[ÛÝ\˜ÙH]šY[˜ÙKÛÛ\]HÙ\]Y[˜ÙHÙX\˜Úœ™X[™\™\Ù[][ÛˆÛÛ›ÛË™]šY]ÈXÚ\Ú[ÛœË[™H[X™[Y˜XÝÜžHØ]Bœ\ÜË‚‚•Ü˜\]\›ÝH›ÜˆHŒ‹LKLLÕLŒLŽVˆ[Žˆ›ÙXÝ]™HÛÜšÈÛÛ[YYÈBL[Z[]H›Ý[™\žH™Y›Ü™HÜ˜\]\ˆS‘QÐULŒ‹LKLLÕLNŒÎ–˜Â™ØÝ[Y[][ÛˆØ\ÈÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜË[™ÛÜšÈ›Ý\ËˆBœ[ˆYYXÝ]™K\Ú]HÛÝ\˜Ú[™È^ÜÙ\]Y[˜ÙK\ÙX\˜Ú^Üœ™\™\Ù[][Û‹X˜XÚÙ[™[›š[™Ë[ˆ[YÜ˜]Y˜[œÙ™\ˆ›ØÚÙ\ˆX]š^œ™]šY]Ë[Û›HÝ]\È\™[š[™È›ÜˆH™]È^Ü]Y]Ë[™HLËÍLÂ™^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆØ]Kˆš[˜[™\šYšXØ][Ûˆ\ÜÙY‚˜UÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]H\ÝË˜UÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XÛÛ\[X[˜Ú]Y™ˆKXÚXÚØ”ÓÓ‹ØÛÝ[X›K[X™[ÝX\™˜Z[ØØ[œË[™ÓH[ÚXÚÜË‚‘^\›˜[›ÝÜÈ™[XZ[ˆÛÝ[X›H[™›Ý[\Ü\™XYK‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕLNŒMŒL–ˆ[ŽˆY\È›Ü‚™^\›˜[\ÛÝ\˜ÙH™\Z\ˆ[™ØÚY[YšXËY^[œÚ[ÛˆÛÛ›ÛË›È›Üˆ^\›˜[X™[š[\ÜÜˆKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™B[š]\ÝÈ\ÜÙYHKH™]šY]È™[XZ[™Y›Û‹\›Û[ÝX›HÚ]XØÙ\Y›™]ÈX™[ËH^\›˜[˜[œÙ™\ˆØ]H\ÜÙYLËÍLÈ™]šY]Ë[Û›HÚXÚÜË\™›™YØ]]™\È™[XZ[™Y™X\ˆZ\ÜÙ\È™[XZ[™YÝ][Ù‹\ØÛÜH˜[ÙB››Û‹XXœÝ[[ÛœÈ™[XZ[™YXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[™Yœ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[™Y[™H[\Ü\™XY[™\ÜÈ]Y]Ù\™^\›˜[›ÝÜÈ[\Ü\™XYKˆHÜ\˜][Û˜[XÚ\Ú[ÛˆØ\ÈÈ™YXÙH^\›˜[˜XÝ]™K\Ú]H[™™\™\Ù[][Ûˆ[˜Ù\Z[HÚ[HÙY\[™È]™\žH^\›˜[˜Ø[™Y]H›Û‹XÛÝ[X›K‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕLÎŒMŽˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‚ÛÜšË›È›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü[™Y\È›ÜˆØÚY[YšXÈÙ[™\˜[^˜][Û‚ÛÜšËˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™Ž[š]\ÝÈ\ÜÙYHKBœ™]šY]ÈÝ[YYÛX[ˆÛÝ[X›HX™[ËÛÝ\˜ÙK\ØØ[H]Y]™[XZ[™Y›[Z]YÈKÈØœÙ\™YKPÔÐH™XÛÜ™Ë\™™YØ]]™\È™[XZ[™Y™X\ˆZ\ÜÙ\Âœ™[XZ[™YÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[™YXÝ[Û˜X›H[‹\ØÛÜB™˜Z[\™\È™[XZ[™Y™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[™YH^\›˜[˜[œÙ™\ˆØ]H™[XZ[™Y™]šY]Ë[Û›H]NKÍNHÚXÚÜÈÚ][\Ü\™XYH›ÝÜË˜XÝ]™K\Ú]HÛÝ\˜ÙH]šY[˜ÙH™[XZ[™Y[œ™\ÛÛ™Y›ÜˆL^\›˜[›ÝÜËÛÛ\]B›™X\‹Y\XØ]HÙX\˜Ú™[XZ[™Y[œ™\ÛÛ™Y›ÜˆŽ›ÝÜË[™™X[™\™\Ù[][Û‚˜ÛÛ›ÛÈ™[XZ[™YXœÙ[ˆH[ˆ\™Y›Ü™H[\[Y[YH\Ù\‹\™\]Y\ÝYœÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]š\œÝˆH™]ÈÛÝ]\Y˜XÝÈ™\Ù\™Hš[[Ý]Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ[™Ý\™˜XÙHHÛX[[[Ý]™\œÝ\Âš[‹Y\ÝšX][ÛˆXØÝ\˜XÞHØ\
ŽMÍØœÈŽNX]˜[XX›H[‹\ØÛÜHÜJK˜]^XÚ]HÈ›ÝÛZ[H™X[LÌ	HÙ\]Y[˜ÙKZY[]HÜˆÈK\ØÛÜ™BœÙ\\˜][Ûˆ™XØ]\ÙH›ÈØØ[›ÛÙYZËÓS\Ù\\Ì‹Ð“TÕÑPSSÓ‘^XÝ]X›HØ\Â˜]˜Z[X›K‚‚•Ü˜\]\›ÜˆHŒ‹LKLLÕLÎŒMŽˆ[Žˆ[\[Y[YH›ÞBœÙ\]Y[˜ÙKÙ›ÛY\Ý[˜ÙHÛÝ]\Y˜XÝÈ›ÜˆHK[™KHÛÛ^Ëœ›Û[ÝYHØ[›ÛšXØ[L‹\›ÝÈ^\›˜[™\™\Ù[][ÛˆØ[\HÈTÓKL‚Š˜XÙX›ÛÚËÙ\ÛL—Ý—ÎWÕTL
K™\Ù\™YHË[Y\ˆØ[\H\È[ˆ^XÚ]˜˜\Ù[[™H\Y˜XÝ[™Ù\[^\›˜[›ÝÜÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›KˆB˜[œÙ™\ˆØ]H™[XZ[œÈŒÍŒ[™™XYWÙ›Ü—ÛX™[Ú[\ÜY˜[ÙXÈHX\›™YœØ[\H\È[X™Y[™È˜Z[\™\ËÈ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]Ë[™ŒLˆX\›™Y]œËZ]\š\ÝXÈ\ØYÜ™Y[Y[ËˆH]\ˆÙ[XÝYTˆÝ™\œšYH[‚š[\[Y[YHÛËTˆÝØ\XÝ[Ûˆ]›ÜˆWØÜØNMÍØ[™WØÜØNXÚ]Ý]ÛÝ[Ü›ÝÝˆš[˜[™\šYšXØ][Ûˆ™Y›Ü™HÙÙÚ[™ÎˆÍˆ[š]\ÝÈ\ÜÙY˜˜[Y]X\ÜÙYÛÛ\[X[\ÜÙYÚ]Y™ˆKXÚXÚØ\ÜÙY”ÓÓ‚˜\Y˜XÝ\œÙH\ÜÙY[™HK\ÛXÙHX™[Y˜XÝÜžHØ]HÛ[ÚÙHÜ›ÝB›[™XYÙHY]Y]HÚ]ÛXÙWÚYLL‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕLŒNNŒL‹LNŒ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH[Ýœ™XY[™\ÜÈ™\Z\‹›È›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÂ™Ù[™\˜[^˜][Ûˆ\Y˜XÝË[™Y\È›ÜˆÔÑˆ\™[š[™Ë‚‘]šY[˜ÙH][ˆÝ\ˆÍˆ[š]\ÝÈ\ÜÙY˜[Y]X\ÜÙYHXØÙ\Y“KPÔÐHÛÝ[Ý^YY]ÎHX™[ËHKH™]šY]ÈÝ[YYÛX[‚˜ÛÝ[X›HX™[ËÛÝ\˜ÙK\ØØ[H]Y]Ý[[Z]YKPÔÐH^ÜÝ\™HÈKÂ›ØœÙ\™YÛÝ\˜ÙH™XÛÜ™Ë\™™YØ]]™\È™[XZ[™Y™X\ˆZ\ÜÙ\È™[XZ[™Y›Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[™Y[™XÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Âœ™[XZ[™YˆH[ˆ\™Y›Ü™H\™Ù]YHÙ[XÝYTˆÔÑŽˆH™]ÈÝ™\œšYBœ[ˆ\Y\ÈÛË\™Y™\™[˜ÙH™\Z\œÈ›ÜˆWØÜØNMÍØ[™WØÜØNXÚÚ\Â˜WØÜØNNL˜ÙY\ÈÛÝ[X›HX™[Ø[™Y]\Ë[™]ÈKXÛÛ^™ÝÛœÝ™X[HÙ[XÝYTˆÝ™\œšYH]˜[X][Ûˆ™\Ù\™\È\™™YØ]]™\Ë™X\‚›Z\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœË[™XÝ[Û˜X›H[‹\ØÛÜB™˜Z[\™\ËˆHØ[YH[ˆ^[™Y^\›˜[˜[œÙ™\ˆ\Y˜XÝ[[™XYÙH\™[š[™Î‚˜ÚXÚ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]\Ø›ÝÈ˜[Y]\ÈØ[™Y]HXØÙ\ÜÚ[ÛœÈXÜ›ÜÜÂšYÚY˜[‹Z[ˆ^\›˜[\Y˜XÝÈ[™HØ]H\Y˜XÝ\ÜÙ\ÈŒÍŒÚ]˜Y]Y]K˜\Y˜XÝÛ[™XYÙK™ÝX\™˜Z[ØÛX[]YX[˜ÛY[™ÈH[Ýš[Üš]Bœ™]šY]ËYXÚ\Ú[Ûˆ^Ü[™[Ý]šY[˜ÙK\XÚÙ]\Y˜XÝËˆH[Ý\š[Üš]B˜\Y˜XÝÙ[XÝÈL™]šY]Ë[Û›HØ[™Y]\ËY™\œÈHÛÝ]Üˆ™X\‹Y\XØ]Bœ›ÝÜË[™ÙY\È[Ù[XÝY›ÝÜÈ›Û‹XÛÝ[X›H[™›Ý[\Ü\™XYKˆBœ™]šY]ËYXÚ\Ú[Ûˆ^Ü\Y˜XÝÜ™X]\ÈL›ËYXÚ\Ú[ÛˆXÚÙ]ÈÚ]ÛÛ\]Y™XÚ\Ú[ÛœË‚‚•Ü˜\]\™\šYšXØ][Ûˆ›ÜˆHØ[YH[ŽˆŽÈ[š]\ÝÈ\ÜÙY˜[Y]Xœ\ÜÙYÚ]ÎHÝ\˜]YX™[ËÛÛ\[X[\ÜÙYÚ]Y™ˆKXÚXÚØ\ÜÙY’”ÓÓˆ\Y˜XÝ\œÚ[™È\ÜÙY›ÜˆHÙ[XÝYT‹[Ý\š[Üš]K[Ý™]šY]Â™^Ü[™^\›˜[˜[œÙ™\ˆØ]H\Y˜XÝË[™ÓHÛ[ÚÙHÛÝ™\˜YÙH›ÝÈ[œÂH™]È[Ýš[Üš]H[™™]šY]ËYXÚ\Ú[Ûˆ^ÜÛÛ[X[™ËˆH]\‚ŒŒ‹LKLLÕLNŒŒŒLËLNŒ[ˆYYH[Ý]šY[˜ÙK\XÚÙ]ÛÛ[X[™[™š[˜ÛYY]\Y˜XÝ[ˆ^\›˜[˜[œÙ™\ˆØ[™Y]K[[™XYÙH˜[Y][Û‹‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕLNŒŒŒLËLNŒ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑˆ\™[š[™Ë‚‘]šY[˜ÙH][ˆÝ\ˆŽÈ[š]\ÝÈ\ÜÙY˜[Y]X\ÜÙYÚ]ÎB˜Ý\˜]YX™[ËHKH™]šY]ÈÝ[YYÛX[ˆÛÝ[X›HX™[ËBœÛÝ\˜ÙK\ØØ[H]Y]Ý[[Z]Y^ÜÙYKPÔÐH™XÛÜ™ÈÈKËH›ÞBœÙ\]Y[˜ÙKÙ›ÛÛÝ][™L‹\›ÝÈTÓKLˆ™\™\Ù[][ÛˆØ[\H[™XYH^\ÝY˜[™HÙ[XÝYTˆÝ™\œšYH]Ø\È[™XYH\YY›ÜˆWØÜØNMÍØ[™˜WØÜØNXˆHÛÙH]šY[˜ÙH›ÜˆHXÝ]™HÔÑˆØ\È]X™[Y˜XÝÜžB™Ø]H[™XYÙH˜[Y][ÛˆÝ[\ÝY]Z[™™\œ™YÛXÙHYÈÚ[™]™\ˆ^[ØY›[™XYÙHØ\ÈXœÙ[ÜˆÛÛ˜YXÝYHš[[˜[YKˆ\È[ˆ\™[™Y]]‚˜ÛYØÚXÚ×ÛX™[Ù˜XÝÜžWÙØ]\Ø›ÝÈØYÈØ]H\Y˜XÝÈ™Y›Ü™H[™XYÙB˜[Y][Û‹™Z™XÝÈ^[ØYYXÛ\™YÛXÙKØ˜]ÚY]Y]H]ÛÛ™›XÝÈÚ]œ][™XYÙK™XÛÜ™È^[ØYY]ÙÈ[™ÚÜYÙ\ÝÈ[‚˜Y]Y]K˜\Y˜XÝÛ[™XYÙX[™[œÈH˜Z[\™HÚ]H™YØ]]™HÓBœ™YÜ™\ÜÚ[Ûˆ\ÝˆHØ[YH[ˆYYH™]šY]Ë[Û›H[Ý]šY[˜ÙHXÚÙ]›Ü‚HLÙ[XÝY^\›˜[Ø[™Y]\ËÛÛœÛÛY][™ÈÎHÛÝ\˜ÙH\™Ù]ÈÚ]›Z\ÜÚ[™ÈÙ\]Y[˜ÙHXÚÙ]È[™Z\ÜÚ[™È™\]Z\™YXÝ]™K\Ú]HXÚÙ]ÈÚ[BšÙY\[™È™XYWÙ›Ü—ÛX™[Ú[\ÜY˜[ÙX‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕMÎŒŒNÖˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‹›Â™›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑˆ\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆŽH[š]\ÝÈ\ÜÙY˜˜[Y]X\ÜÙYÚ]ÎHÝ\˜]YX™[ËHKH™]šY]ÈÝ[YY˜ÛX[ˆÛÝ[X›HX™[ËHÛÝ\˜ÙK\ØØ[H]Y]Ý[[Z]Y^ÜÙYKPÔÐBœ™XÛÜ™ÈÈKË›ÞHÙ\]Y[˜ÙKÙ›ÛÛÝ][™TÓKLˆ™\™\Ù[][ÛˆØ[\\Â˜[™XYH^\ÝY[™›È›ÛÙYZËS\Ù\\Ì‹“TÕÜˆPSSÓ‘^XÝ]X›HØ\Â˜]˜Z[X›HÛˆUˆHXÝ]™HÛÙH]šY[˜ÙHØ\È[ˆ\Y˜XÝYÜ˜\ÛÛœÚ\Ý[˜ÞB™Ø\ˆH^\›˜[˜[œÙ™\ˆØ]HÚXÚÙY›ÝÈXØÙ\ÜÚ[ÛœÈ]Y›Ý˜Z[˜\ÝÛ‚›Z^YÛÝ\˜ÙK\ÛXÙH\Y˜XÝ]Ëˆ\È[ˆYY˜˜[Y]WÙ^\›˜[Ý˜[œÙ™\—Ø\Y˜XÝÜ]Û[™XYÙXÚ\™Y][ÈHØ]HÓBÚ]˜Z[Y˜\Ý™Z]š[Ü‹™YÙ[™\˜]Y˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜Ú]ÛX[‚˜\Y˜XÝÜ]Û[™XYÙKœÛXÙWÚYLLXXÜ›ÜÜÈŒH[œ]Ë[™[›™YH™YØ]]™B›Z^Y\ÛXÙH™YÜ™\ÜÚ[Ûˆ\Ýˆ™[XZ[š[™È[YHÙ[ÈHš\œÝ^\›˜[[Ý™]šY[˜ÙKYÜÜÚY\ˆ\Y˜XÝÚXÚ›Ú[œÈÝ\œ™[XÝ]™K\Ú]K™XXÝ[Û‹Ù\]Y[˜ÙKœÝXÝ\™K]\š\ÝXË™\™\Ù[][Û‹[™›ØÚÙ\ˆ]šY[˜ÙH›ÜˆHLÙ[XÝY˜Ø[™Y]\ÈÚ[HÙY\[™È[›ÝÜÈ™]šY]Ë[Û›Kˆ›ÈÛÝ[X›HX™[ÈÜ‚š[\Ü\™XYH^\›˜[›ÝÜÈÙ\™HÜ™X]Y‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕMŒMÎˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝ›È›Üˆ^\›˜[\ÛÝ\˜ÙH[\Ü›È›Üˆ™]Â™^\›˜[Ø[™Y]H™\Z\‹›È›Üˆ™]ÈØÚY[YšXÈÙ[™\˜[^˜][Ûˆ\Y˜XÝË[™žY\È›ÜˆÔÑˆ\™[š[™Ëˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™ÌÈ[š]\ÝÂœ\ÜÙYHXØÙ\YKPÔÐHÛÝ[Ý^YY]ÎHX™[ËHKH™]šY]ÈÝ[˜YYÛX[ˆÛÝ[X›HX™[ËÛÝ\˜ÙK\ØØ[H]Y]Ý[[Z]YKPÔÐH^ÜÝ\™BÈKÈØœÙ\™YÛÝ\˜ÙH™XÛÜ™Ë\™™YØ]]™\È™[XZ[™Y™X\ˆZ\ÜÙ\Âœ™[XZ[™YÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[™YXÝ[Û˜X›H[‹\ØÛÜB™˜Z[\™\È™[XZ[™Y[™H]\Ý^\›˜[˜[œÙ™\ˆØ]H™[XZ[™Y™]šY]Ë[Û›BÚ][\Ü\™XYH›ÝÜËˆH[ˆ\™Y›Ü™H\™Ù]YHš\œÝ˜[YYÔÑŽ‚˜ÛÝ[\™]šY[˜ÙHXZ[Z[˜Xš[]Kˆ]™\XÙYHÙ[ÛY]žK\™]šY]˜[˜ÛÝ[\™]šY[˜ÙHœ˜[˜ÚØ\ØØYHÚ]\YXÛ\˜]]™H[\È[™Ø]™HB›X™[Y˜XÝÜžHØ]HH\Y[œ]ÛÛ˜XÝ\ÈX›KYš]™[ˆÓH\Y˜XÝ›ØY[™È\È›Û‹Y^[\ÛXÙK[[™XYÙH˜[Y][Û‹ˆ][ˆY˜[˜ÙYH™^”ÔÑœÈ[ˆ›Ý[™Y›Ü›Nˆ™\™\Ù[][ÛˆØ[\\È›ÝÈXÛ\™HÙ\]Y[˜ÙK[Û›Bœ™YXÝ]™H™X]\™\È[™X\šÈ]\š\ÝXÈš[™Ù\œš[YËX]ÚYKPÔÐHYË[™œØÛÜHÚYÛ˜[È\È™]šY]ËÚÛÝ]ÛÛ^ÈH^\›˜[›ØÚÙ\‹[X]š^]Y]›ÝÂœ™Z™XÝÈØ[™Y]K[X[šY™\Ý[™XYÙHZ\ÛX]Ú\Ë‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕMŒMÎˆ[ŽˆY\ˆÛÝ[\™]šY[˜ÙBœÛXÞH™Y˜XÝÜš[™È[™X™[Y˜XÝÜžHØ]H[œ]\™[š[™È\ÜÙY›ØÝ\ÙY\ÝÂ˜[™HK\ÛXÙHØ]HÛ[ÚÙK\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈ›Ü‚™ØÝ[Y[][Û‹[\ÝËÝ˜[Y][Û‹[™Ü˜\]\˜]\ˆ[ˆÜ[š[™ÈÛÝ[™Ü›ÝÝÜˆ[›Ý\ˆÙ[™\šXÈ˜[œÙ™\ˆØ]KˆH™^[˜›ØÚÙYÔÑˆ\È^[XZØYÙB›Z]YØ][ÛˆXÜ›ÜÜÈX\›™Y™\™\Ù[][Ûˆ\Y˜XÝÈ[™^\›˜[[Ý˜[šÚ[™Ë™›ÛÝÙYžH\Y˜XÝÜ˜\ÛÛœÚ\Ý[˜ÞHÚXÚÜË‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕLNŒMŒL–ˆ[ŽˆY\ˆHXÝ]™K\Ú]BœÛÝ\˜Ú[™È™\ÛÛ][Ûˆ[™]\›Z[š\ÝXÈ™\™\Ù[][ÛˆØ[\HÙ\™H[ˆXÙK\ÙBH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈÈXZÙHH›ØÚÙ\ˆX]š^ÛÛœÝ[YHÜÙHXÚÙ]Â™\™XÝKYØ]KØ]Y]ÚXÚÜÈ]™Z™XÝÝ[H›ØÚÙ\ˆX]šXÙ\Ë™Yœ™\Ú˜\Y˜XÝÈ[™ØÜÈÈHNKÍNHØ]HÝ]K[™™\[ˆH[˜[Y][ÛˆÝXÚÂ˜™Y›Ü™HÜ˜\]\ˆÈ›ÝÜ[ˆ^\›˜[X™[XÚ\Ú[ÛœÈÜˆ[\Ü›ÝÜÈ\š[™È\Âœ[‹‚‚“™]È˜Z[\™H[Ù\ÈÚXÚÙY[ˆHŒ‹LKLLÕLNŒMŒL–ˆ[ŽˆH]\›Z[š\ÝXÂœ™\™\Ù[][ÛˆØ[\HÝ\™˜XÙYÛ™H™\™\Ù[][Û‹[]™[™X\‹Y\XØ]HÛÝ]ŠŒMÍ™X\™\ÝMØWØÜØNŒÌ
H]Ø\È›Ý›Û[ÝY[™H›ØÚÙ\‚›X]š^]YHÝ[KZ[YÜ˜][Ûˆš\ÚÈÚ\™H™\ÛÛ][Û‹ÜØ[\H\Y˜XÝÈÛÝ[™^\ÝÚ]Ý]›ÝË[]™[›ØÚÙ\ˆ]šY[˜ÙKˆH˜[œÙ™\ˆØ]H›ÝÈ\È^XÚ]›X]š^Z[YÜ˜][ÛˆÚXÚÜÈ›ÜˆXÝ]™K\Ú]H™\ÛÛ][Ûˆ[™™\™\Ù[][ÛˆØ[\Bœ›ÝÜË[™HX]š^]Y]™Z™XÝÈY™\\ÙY[YÜ˜][ÛˆÛÝ[È]\™HXœÙ[™œ›ÛH›ÝÜË‚‚•Ü˜\]\›ÝH›ÜˆHŒ‹LKLLÕLNŒMŒL–ˆ[Ž‚˜S‘QÐULŒ‹LKLLÕLŽŒŒ˜ÈYX\Ý\™Y›ÙXÝ]™K\\Ë]Ü˜\[\ÙY[YHØ\Â˜X›Ý]LŒˆZ[]\ËˆØÝ[Y[][ÛˆØ\ÈÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜË˜[™ÛÜšÈ›Ý\ÎÈ›ÈÝ[HÝ\œ™[\Ý]HÛZ[\È\™H[[[Û˜[HYÝ]ÚYBš\ÝÜšXØ[›ÙÜ™\ÜÈ[šY\ËÜÝ]\È]Ú[™H™YÙ[™\˜]Yœ›ÛHHÙËˆš[˜[™\šYšXØ][Ûˆ™Y›Ü™HÜ˜\]\\ÜÙYˆ[[š]\ÝÈÚ]Ž\ÝË˜[Y]K˜ÛÛ\[X[Ú]Y™ˆKXÚXÚØ”ÓÓˆ\Y˜XÝ\œÙHÚXÚÜË˜ÛÝ[X›KÚ[\Ü\™XYHÝX\™˜Z[ØØ[œÈ›ÜˆH™]È\Y˜XÝË[™ÓH[˜ÚXÚÜÈ›ÜˆH™]ÈÛÛ[X[™Ëˆ^\›˜[›ÝÜÈ™[XZ[ˆÛÝ[X›H[™›Ýš[\Ü\™XYNÈHØ]H\ÈNKÍNH™]šY]Ë[Û›HÚXÚÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕNŒLMˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‚ÛÜšËˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™Mˆ[š]\ÝÈ\ÜÙYHKBœ™]šY]ÈØ]H™[XZ[œÈÛX[ˆ]›Û‹\›Û[ÝX›HÚ]XØÙ\Y™]ÈX™[ËB™^\›˜[˜[œÙ™\ˆØ]H\ÜÙYKÍH™]šY]Ë[Û›HÚXÚÜÈ™Y›Ü™H\È[‰ÜÈ™]ÂœÙ\]Y[˜ÙKX[YÛ›Y[[™XÝ]™K\Ú]K\ÛÝ\˜Ú[™ÈØ]\Ë\™™YØ]]™\È™[XZ[‚Œ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆ˜XÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈH[\Ü\™XY[™\ÜÈ]Y]ÙY\È^\›˜[›ÝÜÈ[\Ü\™XYK[™XÝ]™K\Ú]KœÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙ]\š\ÝXË[™™\™\Ù[][Ûˆ›ØÚÙ\œÈ™[XZ[ˆ[œ™\ÛÛ™Y‚•HÜ\˜][Û˜[XÚ\Ú[Ûˆ\ÈÈ™YXÙH^\›˜[\ÛÝ\˜ÙH™XY[™\ÜÈ[˜Ù\Z[BÚ[HÙY\[™È]™\žH^\›˜[Ø[™Y]H›Û‹XÛÝ[X›K‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕNŒLMˆ[ŽˆY\ˆY[™È›Ý[™YœÙ\]Y[˜ÙKX[YÛ›Y[™\šYšXØ][Û‹XÝ]™K\Ú]HÛÝ\˜Ú[™È]Y]YH\Y˜XÝË[™BKÍH^\›˜[˜[œÙ™\ˆØ]K\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈ›Üˆ\Y˜XÝœ™YÜ™\ÜÚ[Ûˆ\ÝË[˜[Y][Û‹”ÓÓ‹ØÛÝ[X›K[X™[ÝX\™˜Z[ØØ[œË[™™ØÝ[Y[][Ûˆœ™\Ú™\ÜËˆÈ›ÝÜ[ˆ[ˆ^\›˜[X™[XÚ\Ú[ÛˆÜˆ[\Ü][[XÝ]™K\Ú]HÛÝ\˜Ú[™ËÛÛ\]HÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙÛÛ›ÛË™X[œ™\™\Ù[][ÛˆÛÛ›ÛË™]šY]ÈXÚ\Ú[ÛœË[™[X™[Y˜XÝÜžHØ]\È\ÜË‚‚•Ü˜\]\›ÝH›ÜˆHŒ‹LKLLÕNŒLMˆ[Žˆ›ÙXÝ]™HÛÜšÈÛÛ[YYÈBL[Z[]H›Ý[™\žH™Y›Ü™HÜ˜\]\ˆS‘QÐULŒ‹LKLLÕLŒÎV˜Â™ØÝ[Y[][ÛˆØ\ÈÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜË[™ÛÜšÈ›Ý\Ëˆš[˜[™\šYšXØ][Ûˆ\ÜÙYÚ]NH[š]\ÝË˜[Y]XÛÛ\[X[˜Ú]Y™ˆKXÚXÚØ”ÓÓˆ\Y˜XÝ\œÚ[™ËÓH[ÚXÚÜÈ›ÜˆH™]ÈÛÛ[X[™Ë™^\›˜[ÛÝ[X›KÚ[\Ü\™XYHÝX\™˜Z[ØØ[œË[™HKÍH^\›˜[˜[œÙ™\‚™Ø]K‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕÎŒMKLNŒ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙHÛÛ›Ûœ™\Z\‹ˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™Lˆ[š]\ÝÈ\ÜÙYHKBœ™]šY]ÈØ]H™[XZ[œÈÛX[ˆ]›Û‹\›Û[ÝX›HÚ]XØÙ\Y™]ÈX™[ËBœš[Üˆ^\›˜[˜[œÙ™\ˆØ]H\ÜÙYÎÌÎ™]šY]Ë[Û›HÚXÚÜË\™™YØ]]™\Âœ™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆ˜XÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈ˜[™HÛÝ\˜ÙK\ØØ[H]Y]™XÛÜ™ÈÛ›HKÈØœÙ\™YKPÔÐH™XÛÜ™È›ÜˆBœ™\]Y\ÝYKH˜[˜ÚKˆHÜ\˜][Û˜[XÚ\Ú[ÛˆØ\ÈÈ™YXÙH^\›˜[œÙ\]Y[˜ÙKÜ™XY[™\ÜÈ[˜Ù\Z[HÚ[HÙY\[™È]™\žH^\›˜[Ø[™Y]B››Û‹XÛÝ[X›K‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕÎŒMKLNŒ[ŽˆY\ˆH›Ý[™YœÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙØÜ™Y[ˆ[™[\Ü\™XY[™\ÜÈ]Y]\ÜÙY\™Ù]Y\ÝËšÙY\ÛÜšÈØÛÜYÈ\Y˜XÝ™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙKØÜË˜[Y][Û‹[™š[˜[™Ø]H™\šYšXØ][Û‹ˆÈ›Ý[\Ü^\›˜[X™[È[[^XÚ]XÝ]™K\Ú]BœÛÝ\˜Ú[™ËÛÛ\]HÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙÛÛ›ÛË™X[™\™\Ù[][Û‚˜ÛÛ›ÛË™]šY]ÈXÚ\Ú[ÛœË[™[X™[Y˜XÝÜžHØ]\È\ÜË‚‚•Ü˜\]\›ÝH›ÜˆHŒ‹LKLLÕÎŒMKLNŒ[Žˆ›ÙXÝ]™HÛÜšÈÛÛ[YYÈHL[Z[]H›Ý[™\žH™Y›Ü™HÜ˜\]\ˆS‘QÐULŒ‹LKLLÕÎNNKLNŒÂ™ØÝ[Y[][ÛˆØ\ÈÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜË[™ÛÜšÈ›Ý\Ë‚‘š[˜[™\šYšXØ][Ûˆ\ÜÙYÚ]Mˆ[š]\ÝË˜[Y]XÛÛ\[X[˜Ú]Y™ˆKXÚXÚØ”ÓÓˆ\Y˜XÝ\œÙHÚXÚÜËÓH[ÚXÚÜË[™^\›˜[˜\Y˜XÝ[\ÜØÛÝ[X›HÝX\™˜Z[ÚXÚÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕÎŒŒVˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH™\Z\‚˜ÛÛ›ÛËˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™È[š]\ÝÈ\ÜÙYBŒKH™]šY]ÈØ]H™[XZ[œÈÛX[ˆ]›Û‹\›Û[ÝX›HÚ]XØÙ\Y™]ÈX™[ËHš[Üˆ^\›˜[˜[œÙ™\ˆØ]H\ÜÙYÌËÌÌÈ™]šY]Ë[Û›HÚXÚÜË\™›™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÂœ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝœ™[XZ[œÈHUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ™[XZ[œÈÝX\™˜Z[XÛX[‹˜[™HÛÝ\˜ÙK\ØØ[H]Y]™XÛÜ™ÈÛ›HKÈØœÙ\™YKPÔÐH™XÛÜ™È›ÜˆBœ™\]Y\ÝYKH˜[˜ÚKˆHÜ\˜][Û˜[XÚ\Ú[Ûˆ\ÈÈ™\Z\ˆ^\›˜[\ÛÝ\˜ÙB˜ÛÛ›Û™XY[™\ÜÈÚ[HÙY\[™È]™\žH^\›˜[Ø[™Y]H›Û‹XÛÝ[X›K‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕÎŒŒVˆ[ŽˆY\ˆY[™Âœ™\™\Ù[][Û‹XÛÛ›ÛÛÛ\\š\ÛÛ‹œ›ØYQPÈ\Ø[XšYÝX][Û‹XÝ]™K\Ú]HØ\œÛÝ\˜ÙH™\]Y\ÝËÙ\]Y[˜ÙK[™ZYÚ›ÜšÛÙÛÛ›ÛË[™\]Y^\›˜[˜[œÙ™\‚™Ø]\Ë\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈ›Üˆ›ØÝ\ÙY™YÜ™\ÜÚ[Ûˆ\ÝË[˜[Y][Û‹”ÓÓˆ\Y˜XÝÚXÚÜË[™ØÝ[Y[][Û‹ÜÝ]\È\]\ËˆÈ›Ýš[\Ü^\›˜[X™[È[[^XÚ]Ù\]Y[˜ÙKXÝ]™K\Ú]K™\™\Ù[][Û‹™XÚ\Ú[Û‹[™X™[Y˜XÝÜžHØ]\È\ÜË‚‚•Ü˜\]\›ÝH›ÜˆHŒ‹LKLLÕÎŒŒVˆ[Žˆ›ÙXÝ]™HÛÜšÈÛÛ[YY\ÝHL[Z[]H›Ý[™\žH™Y›Ü™HÜ˜\]\ˆS‘QÐULŒ‹LKLLÕŒŒM˜Â™ØÝ[Y[][ÛˆØ\ÈÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜË[™ÛÜšÈ›Ý\Ë‚‘š[˜[™\šYšXØ][Ûˆ\ÜÙYÚ]Lˆ[š]\ÝË˜[Y]XÛÛ\[X[˜Ú]Y™ˆKXÚXÚØÓH[ÚXÚÜÈ›ÜˆH™]ÈÛÛ[X[™Ë[™”ÓÓˆ\Y˜XÝ˜ÛÝ[X›K[X™[ÚXÚÜË‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕŽŒŽŒÎˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙHÛÛ›Ûœ™\Z\‹ˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™ŒÎH[š]\ÝÈ\ÜÙYHKBœ™]šY]ÈØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜËHš[Üˆ^\›˜[˜[œÙ™\ˆØ]H\ÜÙ\ÈŒ‹ÌŒ‚œ™]šY]Ë[Û›HÚXÚÜË\™™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆ›Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Âœ™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈHKHXØÙ\[˜ÙH\Y˜XÝ˜YÈÛX[ˆÛÝ[X›HX™[Ë[™HÛÝ\˜ÙK\ØØ[H]Y]™XÛÜ™ÈÛ›HKÂ›ØœÙ\™YKPÔÐH™XÛÜ™È›ÜˆH™\]Y\ÝYKH˜[˜ÚKˆH^\Ý[™È^\›˜[˜ÛÛ›Û\Y˜XÝÈ^ÜÙYXÝ]™K\Ú]H™X]\™HØ\Ëœ›ØYQPÈ›ÝÜË[™B›Y][ZY›Û\ÙKÝÜHÛÛ\ÙKÛÈ\È[ˆ™\Z\™YÝX\™˜Z[È[œÝXYÙ‚›Ü[š[™ÈX™[Ü›ÝÝˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝHÛZ[HÙ‚˜š[ÛÙÚXØ[]‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕŽŒŽŒÎˆ[ŽˆY\ˆ^[™[™ÂœÝXÝ\™HX\[™ÈÈ[Lˆ]\š\ÝXË\™XYHÛÛ›ÛËY[™È™\Z\‹œ™\™\Ù[][Û‹š[™[™ËXÛÛ^™XXÝ[Û‹[™Ù\]Y[˜ÙKZÛÝ]\Y˜XÝË\ÙBH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈ›Üˆ™YÜ™\ÜÚ[Ûˆ\ÝËØÜË[™š[˜[Ø]B˜[Y][Û‹ˆÈ›Ý[\Ü^\›˜[X™[È[[HÙ\\˜]H™]šY]ÙYXÚ\Ú[Û‚˜\Y˜XÝ\ÜÙ\È[X™[Y˜XÝÜžHØ]\Ë‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕÎŒÎŒMˆ[ŽˆY\ËÝ\œ™[œ]X[]HØ]\È\™HÛÛÙ[›ÝYÚÈÜ[™\È[ˆÛˆH›Ý[™YKH™]šY]Ë‚‘]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™Œˆ[š]\ÝÈ\ÜÙYHXØÙ\YLK™Ø]H\ÜÙ\ÈŒKÌŒHÚXÚÜÈÚ]›ØÚÙ\œËHXØÙ\YLK™]šY]ËYX™Y™\œ˜[]Y]ÙY\È[Ìˆ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›HÚ]XØÙ\Y›Ý™\›\[™ÛÝ[X›HØ[™Y]\Ë\™™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[‚ŒÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Âœ™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈÌŒH^\[X™[XÚ\Ú[Ûˆ›ÝÜÂœ™[XZ[ˆ™]šY]Ë[Û›KHLˆš[Üš]HØØ[Y]šY[˜ÙHØ\›ÝÜÈ™[XZ[‚››Û‹XÛÝ[X›K[™HUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ™[XZ[œÂ™ÝX\™˜Z[XÛX[ˆÚ]ÛÝ[X›HX™[Ø[™Y]\Ëˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝHÛZ[HÙˆš[ÛÙÚXØ[]‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[][™Ù™ˆY\ˆHŒ‹LKLLÕÎŒÎŒMˆ[Ž‚››È›ÜˆY][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙB˜[œÙ™\ˆØØY™›Û[™Ë‚‘]šY[˜ÙNˆHKH˜XÝÜžHØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜË\™™YØ]]™\È™[XZ[ˆ›™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›Bš[‹\ØÛÜH˜Z[\™\È™[XZ[ˆXØÙ\Y™]šY]ËYØ\X™[È™[XZ[ˆ[™œ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈˆÝÙ]™\‹HKHXØÙ\[˜ÙH\Y˜XÝ\ÂŒXØÙ\Y™]ÈX™[È[™HÛÝ\˜ÙK\ØØ[H]Y]ÚÝÜÈHKPÔÐK[Û›H]Ù\Â››Ý]™H[›ÝYÚÛÝ\˜ÙH™XÛÜ™È›ÜˆH™^˜[˜ÚKˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝHÛZ[HÙˆš[ÛÙÚXØ[]‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕŒŒÍ–ˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH˜[œÙ™\‚œØØY™›Û[™Ëˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™ŒMÈ[š]\ÝÈ\ÜÙYBŒKH™]šY]ÈØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜË\™™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\Âœ™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜB™˜Z[\™\È™[XZ[ˆXØÙ\Y™]šY]ËYØ\X™[È™[XZ[ˆ™]šY]Ë[Û›H[\Ü™Ü›ÝÝ™[XZ[œÈHKHXØÙ\[˜ÙH\Y˜XÝYÈÛX[ˆÛÝ[X›HX™[Ë˜[™HÛÝ\˜ÙK\ØØ[H]Y]™XÛÜ™ÈÛ›HKÈØœÙ\™YKPÔÐH™XÛÜ™È›ÜˆBœ™\]Y\ÝYKH˜[˜ÚKˆ\È[ˆÚÝ[Y˜[˜ÙH^\›˜[\ÛÝ\˜ÙH˜[œÙ™\‚™ÝX\™˜Z[ÈÚ[HÙY\[™È[^\›˜[Ø[™Y]\È›Û‹XÛÝ[X›K‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕNŒNˆ[Žˆ›È›Ü‚˜Y][Û˜[KPÔÐK[Û›HÛÝ[Ü›ÝÝY\È›Üˆ›Ý[™Y^\›˜[\ÛÝ\˜ÙH]šY[˜ÙB˜[™ÛÛ›ÛÛÜšËˆ]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™ŒÌ[š]\ÝÈ\ÜÙYHKH™]šY]ÈØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜË\™™YØ]]™\È™[XZ[ˆ™X\‚›Z\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›Bš[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈHKB˜XØÙ\[˜ÙH\Y˜XÝYÈÛX[ˆÛÝ[X›HX™[Ë[™HÛÝ\˜ÙK\ØØ[H]Y]œ™XÛÜ™ÈÛ›HKÈØœÙ\™YKPÔÐH™XÛÜ™È›ÜˆH™\]Y\ÝYKH˜[˜ÚKˆ\Âœ[ˆÚÝ[ÙY\^\›˜[›ÝÜÈ™]šY]Ë[Û›HÚ[HÛÛ™\[™È]šY[˜ÙHØ\È[Â™^XÚ]ÛÛ›Û\Y˜XÝË‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕNŒNˆ[ŽˆY\ˆ[H™XYB™^\›˜[›ÝÜÈYXÝ]™K\Ú]H]šY[˜ÙHØ[\Y[™Hš\œÝX\YÛÛ›ÛÂœÚÝÙYHY][ZY›Û\ÙHÜHÛÛ\ÙK\ÙH™[XZ[š[™È›ÙXÝ]™H[YHÈ]XÚ™˜Z[\™K[[ÙH\ÝË\]H\˜X›HØÜË[™]›ÚY[žH^\›˜[X™[XÚ\Ú[Û‚[[ÛÛÙÞKÜ™\™\Ù[][ÛˆÛÛ›ÛÈØ[ˆÙ\\˜]HÜÙH[™\Ë‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕŒŒÍ–ˆ[ŽˆY\ˆH^\›˜[˜Ø[™Y]HX[šY™\Ý]šY[˜ÙH[‹]šY[˜ÙH™\]Y\Ý^Ü[\Ü\ØY™]B˜]Y][™LKÌLH^\›˜[]˜[œÙ™\ˆØ]H\™H[\[Y[Y\ÙHH™[XZ[š[™Âœ›ÙXÝ]™HÚ[™ÝÈÈ\™[ˆØÝ[Y[][Û‹\Y˜XÝ™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙK[™œ™]šY]Ë[Û›H^\›˜[\ÛÝ\˜ÙHÝX\™˜Z[È˜]\ˆ[ˆÜ[š[™È[›Ý\ˆKPÔÐK[Û›B˜[˜ÚK‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕÎŒÎŒMˆ[ŽˆY\ˆHKH™]šY]Âœ›Ý™YÛX[ˆ]›Û‹\›Û[ÝX›K\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈÈ\™[‚H^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆ]ˆÛÛ\]YˆÛÝ\˜ÙK\ØØ[H]Y]˜[œÙ™\‚›X[šY™\Ý]Y\žHX[šY™\ÝÓÑØ[Xœ˜][Ûˆ[‹›Ý[™Y™XY[Û›H[šT›ÝÐ‹Â”ÝÚ\ÜËT›ÝØ[\KØ[\HÝX\™˜Z[]Y]™YÜ™\ÜÚ[Ûˆ\ÝË[™ØÝ[Y[][Û‹‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLLÕNŒŒÎVˆ[ŽˆY\ËÝ\œ™[œ]X[]HØ]\È\™HÛÛÙ[›ÝYÚÈÜ[™\È[ˆÛˆH›Ý[™YMÍH™]šY]Ë‚‘]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™ŒH[š]\ÝÈ\ÜÙYHXØÙ\YNML™Ø]H\ÜÙ\ÈŒKÌŒHÚXÚÜÈÚ]›ØÚÙ\œËHXØÙ\YNML™]šY]ËYX™Y™\œ˜[]Y]ÙY\È[Žˆ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›HÚ]XØÙ\Y›Ý™\›\\™™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙB››Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›Bš[\ÜÜ›ÝÝ™[XZ[œÈÍÈ^\[X™[XÚ\Ú[Ûˆ›ÝÜÈ™[XZ[ˆ™]šY]Ë[Û›KHš[Üš]HØØ[Y]šY[˜ÙHØ\›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›K[™BUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ™[XZ[œÈÝX\™˜Z[XÛX[ˆÚ]˜ÛÝ[X›HX™[Ø[™Y]\Ëˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝB˜ÛZ[HÙˆš[ÛÙÚXØ[]‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLLÕNŒŒÎVˆ[ŽˆY\ˆHMÍHØ]B˜XØÙ\YÛÈÛX[ˆX™[È[™HÜÝNMÍHØ]HÝ^YYÛX[‹H[ˆÜ[™Yœ™\Z\™Y[™XØÙ\YH›Ý[™YKY[žH™]šY]ËˆH™]šY]ËYX™Y™\œ˜[]Y]YK\™][[Û‹\™[™YØ]]™K˜[ÙK[›Û‹XXœÝ[[Û‹˜XÝ[Û˜X›KY˜Z[\™K[™˜[Z[KX›Ý[™\žHØ]\È\™HÛX[‹‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLL•ŒÎNŒÎˆ[ŽˆY\ËÝ\œ™[œ]X[]HØ]\È\™HÛÛÙ[›ÝYÚÈÜ[™\È[ˆÛˆ›Ý[™YÍHØØ[[™Ë‚‘]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™ŒH[š]\ÝÈ\ÜÙYHXØÙ\YNL™Ø]H\ÜÙ\ÈŒÌŒÚXÚÜËHXØÙ\YNL™]šY]ËYXY™\œ˜[]Y]ÙY\Â˜[ŒÈ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›HÚ]XØÙ\Y[X™[Ý™\›\\™›™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÂœ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝœ™[XZ[œÈ[™HUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ™[XZ[œÂ™ÝX\™˜Z[XÛX[ˆÚ]ÛÝ[X›HX™[Ø[™Y]\Ëˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝHÛZ[HÙˆš[ÛÙÚXØ[]‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLL•ŒMNŒVˆ[ŽˆY\ËÝ\œ™[œ]X[]HØ]\È\™HÛÛÙ[›ÝYÚÈÜ[™\È[ˆÛˆ›Ý[™YÍÍHØØ[[™Ë‚‘]šY[˜ÙH][ˆÝ\ˆ˜[Y]X[™Œ[š]\ÝÈ\ÜÙYHXØÙ\YMÍL™Ø]H\ÜÙ\ÈŒÌŒÚXÚÜËHXØÙ\YMÍL™]šY]ËYXY™\œ˜[]Y]ÙY\ÈLNœ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›K\™™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆ›Ý][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\Âœ™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈ[™HUÜÜÜÜž[]˜[œÙ™\‚™˜[Z[H^[œÚ[Ûˆ™[XZ[œÈÝX\™˜Z[XÛX[ˆÚ]ÛÝ[X›HX™[Ø[™Y]\Ë‚•\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝHÛZ[HÙˆš[ÛÙÚXØ[]‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLL•NNMŒŒ–ˆ[ŽˆY\ËÝ\œ™[œ]X[]HØ]\ÈÙ\™HÛÛÙ[›ÝYÚÈ^XÚ]HY™\ˆHÍL™]šY]ËYXÝ\™˜XÙB˜[™›Û[ÝHHÙ]™[ˆÛX[ˆÍLX™[Ëˆ]šY[˜ÙNˆ˜\Ù[[™H˜[Y]X[™Œ[š]\ÝÈ\ÜÙY][ˆÝ\HÜÝX˜]ÚÍLØ]H\ÜÙ\ÈŒÌŒÚXÚÜËš\™™YØ]]™\È™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙB››Û‹XXœÝ[[ÛœÈ™[XZ[ˆXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆXØÙ\Y›X™[ÈÚ]™]šY]ÈX™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈ[™BUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ™[XZ[œÈÝX\™˜Z[XÛX[ˆÚ]˜ÛÝ[X›HX™[Ø[™Y]\Ëˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝB˜ÛZ[HÙˆš[ÛÙÚXØ[]‚‚”Ý\Ú]‚˜\Y˜XÝËÝŒ×ÛX™[Ø˜]ÚØXØÙ\[˜ÙWØÚXÚ×ÌLWÜ™]šY]ËšœÛÛ˜˜\Y˜XÝËÝŒ×ÛX™[Ù˜XÝÜžWÙØ]WØÚXÚ×ÌLWÜ™]šY]ËšœÛÛ˜˜\Y˜XÝËÝŒ×ÛX™[ÜØØ[[™×Ü]X[]WØ]Y]ÌLWÜ™]šY]ËšœÛÛ˜˜\Y˜XÝËÝŒ×Ü™]šY]×ÙXÜÝ[[X\žWÌLWÜ™]šY]ËšœÛÛ˜˜\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÌLWÜ™]šY]ËšœÛÛ˜˜\Y˜XÝËÝŒ×ÜÛÝ\˜ÙWÜØØ[WÛ[Z]Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ]Y\žWÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÛÛÙØØ[Xœ˜][Û—Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØØ[™Y]WÛX[šY™\ÝØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÛ[™WØ˜[[˜ÙWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ]šY[˜ÙWÜ[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ]šY[˜ÙWÜ™\]Y\ÝÙ^ÜÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙ]šY[˜ÙWÜ]Y]YWÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙ]šY[˜ÙWÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙ]šY[˜ÙWÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜ]Y]YWÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜ]Y]YWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×ÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÝXÝ\™WÛX\[™×ÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜØÛÜ™\×ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ]\š\ÝX×ØÛÛ›ÛÜØÛÜ™\×Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÙ˜Z[\™WÛ[ÙWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØÛÛ›ÛÜ™\Z\—Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØÛÛ›ÛÜ™\Z\—Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛÛX[šY™\ÝÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛÛX[šY™\ÝØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛØÛÛ\\š\ÛÛ—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—ØÛÛ›ÛØÛÛ\\š\ÛÛ—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^Ü™\Z\—Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^Ü™\Z\—Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^ÛX\[™×ÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØš[™[™×ØÛÛ^ÛX\[™×ÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÙØ\ÜÛÝ\˜ÙWÜ™\]Y\Ý×ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÚÛÝ]Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÛ™ZYÚ›ÜšÛÙÜ[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÛ™ZYÚ›ÜšÛÙÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÛ™ZYÚ›ÜšÛÙÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWØ[YÛ›Y[Ý™\šYšXØ][Û—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWØ[YÛ›Y[Ý™\šYšXØ][Û—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÜÙX\˜ÚÙ^ÜÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜÙ\]Y[˜ÙWÜÙX\˜ÚÙ^ÜØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ[\ÜÜ™XY[™\Ü×Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü]Y]YWÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü]Y]YWØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ù^ÜÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ù^ÜØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü™\ÛÛ][Û—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü™\ÛÛ][Û—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™Ü[—Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—Ø›ØÚÙ\—ÛX]š^ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—Ø›ØÚÙ\—ÛX]š^Ø]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™]šY]×ÛÛ›WÚ[\ÜÜØY™]WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™XXÝ[Û—Ù]šY[˜ÙWÜØ[\WÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™XXÝ[Û—Ù]šY[˜ÙWÜØ[\WØ]Y]ÌLKšœÛÛ˜˜\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØœ›ØYÙX×Ù\Ø[XšYÝX][Û—Ø]Y]ÌLKšœÛÛ˜[™˜ÛÜšËÛX™[Ü™]šY]×ÌLWÛ›Ý\Ë›Yˆ›ÜˆHÛÛ\XÝ^\›˜[]˜[œÙ™\ˆ›Ùš[K˜[ÛÈ™XYÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÌLWÛ›Ý\Ë›Y‚‚’YÚ\Ý]˜[YHÜ[ÛœÎ‚‚ŒKˆÈ›Ý›Û[ÝHHKH™]šY]ÎÈ]\ÈXØÙ\YX™[È[™^\ÝÈ\ÈBˆÛÝ\˜ÙK[[Z]]Y]Ú[‚Œ‹ˆÛÛ[YH™]šY]Ë[Û›H^\›˜[\ÛÝ\˜ÙH]šY[˜ÙHÛÛXÝ[Ûˆœ›ÛBˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØXÝ]™WÜÚ]WÜÛÝ\˜Ú[™×Ü™\ÛÛ][Û—ÌLKšœÛÛ˜‚ˆHš\œÝ[šT›Ý™X]\™H™KXÚXÚÈ›Ý[™^XÚ]XÝ]™K\Ú]H™\ÚYYBˆÛÝ\˜Ù\ËÛÈH™^XÝ]™K\Ú]HÝ\\Èš[X\žH]\˜]\™KÔˆÛÝ\˜ÙBˆ™]šY]È›ÜˆHÈš[™[™Ë\\Ë\™XXÝ[ÛˆÛÛ^›ÝÜÈ[™š[X\žHXÝ]™K\Ú]BˆÛÝ\˜ÙH\ØÛÝ™\žH›ÜˆHÈ™XXÝ[Û‹[Û›H›ÝÜÈÚ]Ý]ÛÝ[[™È[žH›ÝË‚ŒËˆ™X]HšXH™XXÝ[Û‹XÛÛ^Ø[\H\ÈÛÛ^Û›K\ÜXÚX[HHM‚ˆœ›ØYQPÈÛÛ^›ÝÜÎÈÈ›Ý™X]šXH›ÝÜÈ\ÈXÝ]™K\Ú]H]šY[˜ÙK‚ˆ™X]\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØ˜XÚÙ[™ÜÙ\]Y[˜ÙWÜÙX\˜ÚÌLKšœÛÛ˜\ÂˆH›Ý[™YÝ\œ™[\™Y™\™[˜ÙHÙ\]Y[˜ÙK\ÙX\˜Ú™\Ý[ˆ]ÛX\œÈ]˜XÚÙ[™ˆÙX\˜Ú›ØÚÙ\ˆ›ÜˆHŽ›Ë\ÚYÛ˜[›ÝÜËÚ[Hœ›ØY\ˆ[šT™Y‹]ÚYHÜ‚ˆ[]œËX[\XØ]HØÜ™Y[š[™È™[XZ[œÈH[Z]][Ûˆ™Y›Ü™H[\Ü‚Kˆ\ÙHHL‹\›ÝÈTÓKLˆ™\™\Ù[][ÛˆØ[\H[‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÜ™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜[™ˆ]ÈX\›™Y]œËZ]\š\ÝXÈ\ØYÜ™Y[Y[ÈÈš[Üš]^™H[Ý™]šY]ËÚ[BˆÙY\[™È]\š\ÝXÈ™]šY]˜[Ù\]Y[˜ÙK\ÙX\˜ÚÛÛ›ÛË[™ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚÛY\—Ü™\™\Ù[][Û—Ø˜XÚÙ[™ÜØ[\WÌLKšœÛÛ˜ˆ\È™\]Z\™Y˜\Ù[[™\Ë‚‹ˆ\ÙH\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—Ø›ØÚÙ\—ÛX]š^ÌLKšœÛÛ˜\ÈBˆØ[™Y]K[]™[›ØÚÙ\ˆX\ˆLXÝ]™K\Ú]HÛÝ\˜ÙH›ÝÜÈÚ]™\ÛÛ][Û‚ˆÝ]\Ù\ÈØ\œšYY›ÜØ\™Ž˜XÚÙ[™›Ë\ÚYÛ˜[Ù\]Y[˜ÙH›ÝÜËˆÙ\]Y[˜ÙBˆÛÝ]ËLˆ™\™\Ù[][Û‹X˜XÚÙ[™[œËLˆ™\™\Ù[][ÛˆØ[\H›ÝÜËÂˆ™\™\Ù[][Ûˆ™X\‹Y\XØ]HÛÝ]È[ˆHTÓKLˆØ[\KH™\™\Ù[][Û‚ˆ™X\‹Y\XØ]HÛÝ][ˆHË[Y\ˆ˜\Ù[[™K[™ÛÛ\]Y[\ÜˆXÚ\Ú[ÛœËˆHËÍÈ˜[œÙ™\ˆØ]H›ÝÈ˜Z[ÈÝ[HX]šXÙ\È]ÛZ]ˆXÝ]™K\Ú]H™\ÛÛ][Û‹˜XÚÙ[™Ù\]Y[˜ÙK\ÙX\˜ÚÜˆ™\™\Ù[][ÛˆØ[\Bˆ[YÜ˜][Û‹[™[ÛÈ˜Z[ÈYÚY˜[‹Z[ˆ^\›˜[\Y˜XÝÈÚ][™^XÝYˆØ[™Y]HXØÙ\ÜÚ[ÛœËZ\ÜÚ[™È[XÛÝ™\˜YÙHX[šY™\Ý›ÝÜËÜˆØ[™Y]KXÛÝ[ˆšY‚ËˆÙY\]™\žH^\›˜[[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[™Y]H›Û‹XÛÝ[X›H[[BˆÙ\\˜]HXÚ\Ú[Ûˆ\Y˜XÝ\ÜÙ\ÈH[X™[Y˜XÝÜžHØ]K‚Žˆ™\Ù\™HHš[™KY˜[Z[HUÜÜÜÜž[]˜[œÙ™\ˆ^Y\ˆ\È›Ý[™\žH]šY[˜ÙNÂˆÈ›ÝÛÛ\ÙH\ÙH˜[Z[Y\È[ÈÙ[™\šXÈY›Û\ÙHÜˆY][ZY›Û\ÙBˆX™[Ë‚‚“X™[\]X[]HÛÛ™šY[˜ÙHØ[›ÜˆHŒ‹LKLL•MŽMŽŒKLNŒ[ŽˆY\Ë˜Ý\œ™[]X[]HØ]\È\™HÛÛÙ[›ÝYÚÈÜ[ˆH›Ý[™Y™]šY]Ëˆ]šY[˜ÙB˜][ˆÝ\ˆ˜[Y]X[™Œˆ[š]\ÝÈ\ÜÙYHXØÙ\YMÍÍHØ]Bœ\ÜÙ\ÈŒÌŒÚXÚÜËHXØÙ\YMÍÍH™]šY]ËYXY™\œ˜[]Y]ÙY\È[LÎœ™]šY]Ë\Ý]H›ÝÜÈ›Û‹XÛÝ[X›HÚ]XØÙ\Y[X™[Ý™\›\\™™YØ]]™\Âœ™[XZ[ˆ™X\ˆZ\ÜÙ\È™[XZ[ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœÈ™[XZ[ˆ˜XÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\È™[XZ[ˆ™]šY]Ë[Û›H[\ÜÜ›ÝÝ™[XZ[œÈ˜[™HUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ™[XZ[œÈÝX\™˜Z[XÛX[ˆÚ]ŒÛÝ[X›HX™[Ø[™Y]\Ëˆ\È\È[ˆÜ\˜][Û˜[ÛÜšÙ›ÝÈXÚ\Ú[Û‹›ÝB˜ÛZ[HÙˆš[ÛÙÚXØ[]‚‚”™[XZ[š[™Ë][YH[ˆ›ÜˆHŒ‹LKLL•MŽMŽŒKLNŒ[ŽˆY\ˆXØÙ\[™ÂHÛX[ˆ˜]Ú\ÙHH™[XZ[š[™È›ÙXÝ]™HÚ[™ÝÈÈ™[[Ý™HHØØ[[™Â˜›Ý[™XÚÈ^ÜÙYžHH[ˆžHY[™ÈÙ[ÛY]žKX\Y˜XÝ›ÝÈ™]\ÙK™\šYžH]˜YØZ[œÝH™X[Ü˜\[ˆÜ[ˆH™^›Ý[™Y˜[˜ÚHÛ›HYˆBœÜÝNØ]H™[XZ[œÈÛX[ˆ[™HÜ˜\]\Ú[™ÝÈ\ÈÝ[›ÝXÝY‚‚’ÙY\WØÜØNL[™WØÜØNÍÌX[ˆ™]šY]È[›\ÜÈ^XÚ]ØØ[YXÚ[š\ÛB™]šY[˜ÙH™\ÛÛ™\ÈZ\ˆÛÝ[\™]šY[˜ÙNÈ^H\™H™YÜ™\ÜÚ[ÛˆØ\Ù\È›Ü‚›YXÚ[š\ÛH^]ÚÝ[›ÝÝ™\œšYH˜[Z[KX›Ý[™\žHÜˆšXYXÛÚ\™[˜ÙB˜ÛÛ™›XÝË‚‚”™[XZ[š[™Ë][YH[ˆ^XÝ]Y›ÜˆHŒ‹LKLL•ŒMNŒVˆ[ŽˆY\ˆHÍÍB™Ø]HØ\ÈÛX[ˆ[™H™YÚ\ÝžHYˆX™[ËÈ›ÝÜ[ˆ[ˆHš[˜[œ›ÙXÝ]™HZ[]\Ëˆ[œÝXY™\Ù\™HHÍÍH]šY[˜ÙHžHY[™Â˜ÛÜšËÛX™[Ü™]šY]×ÍÍÍWÛ›Ý\Ë›Y™Yœ™\Ú[™ÈÝ\œ™[\Ý]HØÜËÙ[™\˜][™Â˜\Y˜XÝËÜ\™—Ü™\ÜÍÍÍKšœÛÛ˜[™ÚXÚÚ[™ÈÝ[HÝ]\ËÚ[™Ù™ˆÛZ[\Â˜™Y›Ü™HYX\Ý\™YÜ˜\]\‚‚’Û›ÝÛˆ›ØÚÙ\œÎ‚‚‹HX™[È\™H›Ýš\Ú[Û˜[[™›Ý^\\™]šY]ÙYÈÈ›ÝÛZ[H˜[Y]Y[žž[YBˆ[˜Ý[Û‹‚‹Hœ›Ûž™KÜÚ[™\‹ÙÛÛY\œÈ\™H]šY[˜ÙK[X[˜YÙ[Y[Y\œË›ÝÙ][X‚ˆ˜[Y][ÛˆÝ]\Ë‚‹HÙ[ÛY]žH™]šY]˜[\È]\š\ÝXË›ÝX\›™Y‚‹HYØ[™ØÛÙ˜XÝÜˆ]šY[˜ÙH\Ù\È™X\˜žH[™ÝXÝ\™K]ÚYH[PÒQˆYØ[™]Û\Âˆ\È[™™\œ™Y›Û\ÎÈ]Ù\È›Ý[Ù[ØØÝ\[˜ÞK[\›˜]HÛÛ™›Ü›Y\œËˆš[ÛÙÚXØ[\ÜÙ[X›KÜˆÝXœÝ˜]HÝ]K‚‹HWØÜØNŒLÌ˜WØÜØNŒÍLØWØÜØNŒÍÌ˜[™WØÜØNÌ\™HÝ\œ™[H™\Ýˆ™X]Y\È]šY[˜ÙK[[Z]YXœÝ[[ÛœÈ™XØ]\ÙHÙ[XÝYÝXÝ\™\ÈXÚÂˆ^XÝYØØ[ÜˆÝXÝ\™K]ÚYHÛÙ˜XÝÜˆ]šY[˜ÙK‚‹H[Y]X˜\ÙHØØ[Xš[]H\È›Ý™Y[ˆYX\Ý\™YÈ\™‹\ÝZ]X\ÈØØ[ˆ\Y˜XÝ[Z[™ÈÛ›K‚‚ˆÈÈ[ˆ[Z[™Â‚‹HÕT•QÐUˆŒ‹LKLMUMNNNŒLËLNŒ‹HS‘QÐUˆŒ‹LKLMUMŽŒÍNKLNŒ‹HYX\Ý\™Y[\ÙY[YNˆÍKÍÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝHÛÛ[YY›Ý[™LŽ›ÛÙYZÈÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆœ›ÛHÝYÙYˆ[™^LÌKˆ[™^LÌH^ÜÙYWØÜØNŒLÌ˜™\œÝ\ÈWØÜØNLÌ˜]X^K\ØÛÜ™BˆŽÎXÈ›Ý[™ŽH›ÛY]›ØÚÙ\ˆ[ÈLHYÚUHÛÛœÝ˜Z[È\ÈÎˆÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[Ë‚‹H›Ý[™ŽHÛX\™Y[™^LÌH]X^ŽL[™ÛX\™Y[™XÙ\ÈLÌ‹LLÎBˆ™Y›Ü™H[™^M^ÜÙYWØÜØNŒMX™\œÝ\ÈWØÜØNŽLØ]X^ÌÌÍØ‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌÌLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌšœÛÛ˜‚ˆ›Ý[™Ì\ÈLˆYÚUHÛÛœÝ˜Z[ËÎÙ\]Y[˜ÙKZY[]H\][Û‚ˆÛÛœÝ˜Z[Ë›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËÛÝ[X›HX™[Ë[™[\Ü\™XYBˆ›ÝÜËˆ]È\™XÝ™\šYšXØ][ÛˆÛX\œÈ[™XÙ\ÈMLMH]X^˜Z[‹Ý\ÝˆK\ØÛÜ™HŽÌØˆ™^\™XÝ›ÛÙYZÈÛÜšÈÚÝ[ÛÛ[YHÝYÙY[™^ˆMˆ[™\ˆ›Ý[™LÌ™XY[™\ÜË‚‹H[K\ØÛÜ™HÛÝ]™[XZ[œÈ›Ü˜šY[Žˆ›Ý[™LÌÛÝ™\˜YÙH\ÈÝ[\X[ˆHÜ]™[XZ[œÈ™]šY]Ë[Û›KØØ[™Y]K[Û›K[™WØÜØNŒÍÌ˜ØWØÜØNLXˆ™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË‚‚ˆÈÈÈŒ‹LKLMUŒŽŒŒMˆ[‚‚‹H\™XÝHÛÛ[YY›ÛÙYZÈÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆœ›ÛH›Ý[™LÌÝYÙYˆ[™^M‹ˆ[™^Mˆ\ÜÙY]X^˜Z[‹Ý\ÝK\ØÛÜ™HŒŒˆ[™^MÂˆ^ÜÙYWØÜØNŒMØŽŒQÎØYØZ[œÝ˜Z[ˆ™ZYÚ›ÜœÈ]X^ŽÌ˜Ú]ˆš[Û][™È˜Z[‹Ý\Ý›ÝÜË‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌWÌLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌKšœÛÛ˜‚ˆ›Ý[™ÌH˜Z\ÙYHÜ]ÈLˆYÚUHÛÛœÝ˜Z[Ë]H[™^LMÂˆ™\[ˆÝ[˜Z[Y]X^ŽXÚ]Lˆš[Û][™È›ÝÜË‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™Ì—ÌLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™Ì‹šœÛÛ˜‚ˆ›Ý[™Ìˆ\ÈLYÚUHÛÛœÝ˜Z[ËÎÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[Ëˆ›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]Ý][Ù‹\ØÛÜBˆ˜[ÙH›Û‹XXœÝ[[ÛœËÛÝ[X›HX™[Ë[™[\Ü\™XYH›ÝÜË‚‹H\™XÝ›Ý[™LÌˆ™\šYšXØ][ÛˆÛX\œÈ[™^MÈ]X^MÍX[™[™^Mˆ]X^ˆ[™^MH
WØÜØNŒM˜ØŽX
H[YYÝ]Y\ˆLˆÙXÛÛ™È™Y›Ü™HZ\ˆ›ÝÜÈÙ\™H[Z]YˆHYÙÜ™YØ]Bˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™Ì—Ü]Y\žWÜÚ[™ÛWØYÙÜ™YØ]WÌM×ÌMWÛÙ—ÍÌ‹šœÛÛ˜ˆ™XÛÜ™ÈˆÛÛ\]Y]Y\žHÛÛÜ™[˜]\ËÍˆZ\ˆ›ÝÜËMŒH˜Z[‹Ý\Ý›ÝÜËˆX^˜Z[‹Ý\ÝK\ØÛÜ™HMÍX\™Ù]]š[Û][™ÈZ\œË[™Û™H[Y[Ý]ˆ\Y˜XÝ‚‹H[K\ØÛÜ™HÛÝ]™[XZ[œÈ›Ü˜šY[Žˆ›Ý[™LÌˆÛÝ™\˜YÙH\ÈÝ[\X[ˆ[™^MH\È[œ™\ÛÛ™YHÜ]™[XZ[œÈ™]šY]Ë[Û›KØØ[™Y]K[Û›K[™ˆWØÜØNŒÍÌ˜ØWØÜØNLX™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœËˆ™^\™XÝ›ÛÙYZÂˆÛÜšÈÚÝ[™]žHÜˆ^XÚ]HYYXØ]HÝYÙY[™^MH[™\ˆ›Ý[™LÌ‚ˆ™XY[™\ÜÈ™Y›Ü™HY˜[˜Ú[™ÈÈ[™^M‹‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆˆ[š]\ÝË˜[Y]XÛÛ\[X[ˆÚ]Y™ˆKXÚXÚØ[™”ÓÓˆ\œÚ[™È›ÜˆŒ™]È›ÛÙYZÈ\Y˜XÝË‚‚‹HÕT•QÐUˆŒ‹LKLMUNNNŒÌ‚‹HS‘QÐUˆŒ‹LKLMUŒŒÌŒŒ–‚‹HYX\Ý\™Y[\ÙY[YNˆÌKŽÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ™\Z\™YBˆÙ[‹XÜ™X]YÝ[H^XË\Ú[QØÚÈ[ÈH]™HÙ[[™[ØÚÈ™Y›Ü™BˆÞ[˜Ú[™Ëˆ›ÈKPÔÐK[Û›HÛÝ[Ü›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝHÛÛ[YY›Ý[™L›ÛÙYZÈÛ\Ý\‹Yš\œÝ™\šYšXØ][Ûˆœ›ÛHÝYÙYˆ[™^LŒËˆ[™^LŒÈ^ÜÙYWØÜØNŒL›ØÚÙ\œÈ]X^K\ØÛÜ™HŽMÍ˜Âˆ›Ý[™H›ÛYÜÙH›ØÚÙ\œÈ]]È[™^LLŒÈ™\[ˆ^ÜÙYHÙXÛÛ™ˆWØÜØNŒLÝ\™˜XÙH]X^ŽÌÍX‚‹H›Ý[™ˆ›ÛY]Ý\™˜XÙH[ÈMÈYÚUHÛÛœÝ˜Z[È\ÈÎˆÙ\]Y[˜ÙKZY[]HÛÛœÝ˜Z[È[™ÛX\™Y[™XÙ\ÈLŒËLLˆ]X^˜Z[‹Ý\ÝˆK\ØÛÜ™HŽNXˆ[™^LÈ[ˆ^ÜÙYWØÜØNŒLŽ™\œÝ\ÈWØÜØNŒNN]ˆX^ŽÍX‚‹H›Ý[™È›ÛY]Z\‹ÛX\™Y[™XÙ\ÈLËLLŽH]X^ŽŽ[‚ˆ[™^LÌ^ÜÙYWØÜØNŒLÌX™\œÝ\ÈWØÜØNŒŽXØWØÜØNMMX]X^ˆÍMÍ‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ŽÌLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ŽšœÛÛ˜‚ˆ›Ý[™Ž\ÈLYÚUHÛÛœÝ˜Z[ËÎÙ\]Y[˜ÙKZY[]H\][Û‚ˆÛÛœÝ˜Z[Ë›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]ˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËÛÝ[X›HX™[Ë[™[\Ü\™XYBˆ›ÝÜËˆ]È\™XÝ[™^LLÌ™\[ˆ\ÜÙ\È]X^˜Z[‹Ý\ÝK\ØÛÜ™HÍÍX‚ˆ™^\™XÝ›ÛÙYZÈÛÜšÈÚÝ[ÛÛ[YHÝYÙY[™^LÌH[™\ˆ›Ý[™LŽˆ™XY[™\ÜË‚‹H[K\ØÛÜ™HÛÝ]™[XZ[œÈ›Ü˜šY[Žˆ›Ý[™LŽÛÝ™\˜YÙH\ÈÝ[\X[ˆHÜ]™[XZ[œÈ™]šY]Ë[Û›KØØ[™Y]K[Û›K[™WØÜØNŒÍÌ˜ØWØÜØNLXˆ™[XZ[ˆÛÛÜ™[˜]H^Û\Ú[ÛœË‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆ[š]\ÝË˜[Y]XÛÛ\[X[ˆÚ]Y™ˆKXÚXÚØ[™”ÓÓˆ\œÚ[™È›ÜˆŒÈ™]È›ÛÙYZÈ\Y˜XÝË‚‚‹HÕT•QÐUˆŒ‹LKLMUMLŽŒ–‚‹HS‘QÐUˆŒ‹LKLMUMNŒÌNL‚‹HYX\Ý\™Y[\ÙY[YNˆÎKŽZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™[™YÛ\Ý\‹Yš\œÝÜ]\ÜÚYÛ›Y[ÛÈ™X[Ù\]Y[˜ÙKZY[]HÛ\Ý\œÂˆ\™H[š[Û™Y™Y›Ü™HÝXÝ\˜[ÛÛ\Û™[\ÜÚYÛ›Y[ˆ\Èš^YBˆÝYÙYZ[™^LLˆ™\Z\ˆ]Ú]Ý][›ÙXÚ[™ÈÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë‚‹H\™XÝH˜[ˆ›Ý[™NHÚ[™ÛK\]Y\žHÚXÚÜÈœ›ÛHÝYÙY[™XÙ\ÈM‹LL‹ˆ[™XÙ\ÂˆM‹LLH\ÜÙYÈ[™^Lˆ^ÜÙYWØÜØNŒLØØŽŒUSØ™\œÝ\È[[Ý]ˆWØÜØNŒLMXØŽŒUÌSØ]X^K\ØÛÜ™HÍLØ‚‹HZ[[™™\šYšYYÛ\Ý\‹Yš\œÝ›Ý[™ÈLLLˆ›ÜˆHÝXœÙ\]Y[›ØÚÙ\œË‚ˆ›Ý[™LˆÛX\œÈÝYÙY[™^LÈ]X^K\ØÛÜ™HŽXÈÝYÙY[™^Lˆ\ÜÙ\È]X^M˜ÈÝYÙY[™^LH^ÜÙ\ÈH\™Ù\ˆYÚUH›ØÚÙ\‚ˆÝ\™˜XÙH]X^ŽŒ˜‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™L×ÌLšœÛÛ˜ˆ[™ˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™LËšœÛÛ˜‚ˆ›Ý[™LÈ\ÈYÚUHÛÛœÝ˜Z[ËÎÙ\]Y[˜ÙKZY[]H\][Û‚ˆÛÛœÝ˜Z[Ë›Ú™XÝYš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]ËÛÝ[X›BˆX™[Ë[™[\Ü\™XYH›ÝÜËˆ™^\™XÝ›ÛÙYZÈÛÜšÈÚÝ[™\[‚ˆÝYÙY[™^LH[™\ˆ›Ý[™LLÈ™XY[™\ÜË‚‹HH[[X]\šX[^˜X›HÝYÙYXÛÛÜ™[˜]H›ÛÙYZÈÚYÛ˜[›ÝÈÛÛ\]\ÈÝ™\‚ˆ[ÌˆX]\šX[^˜X›HÙ[XÝYÛÛÜ™[˜]\È[™X\ÈML‹LŒˆZ\ˆ›ÝÜË]ˆ]˜Z[ÈHØ\™Ù]]X^˜Z[‹Ý\ÝK\ØÛÜ™HŽMÍXÈ]™[XZ[œÂˆ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›H[™›Û‹XÛZ[Z[™Ë‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[Ü˜È\ÝØ[™”ÓÓˆ\œÚ[™È›ÜˆŽˆ™]ËÝ\]Y›ÛÙYZÈ\Y˜XÝË‚‚‹HÕT•QÐUˆŒ‹LKLMULÎLŒ–‚‹HS‘QÐUˆŒ‹LKLMUMŒÌŒÌ–‚‹HYX\Ý\™Y[\ÙY[YNˆÌÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝH˜[ˆ›Ý[™NHÚ[™ÛK\]Y\žHÚXÚÜÈœ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™KšœÛÛ˜‚ˆÝYÙY[™XÙ\ÈNMH[ÛÛ\]YÚ]MËNHX\Y›ÝÜËËMÂˆ˜Z[‹Ý\Ý›ÝÜËX^˜Z[‹Ý\ÝK\ØÛÜ™HMÎX[™\™Ù]]š[Û][™ÂˆZ\œË‚‹HYYˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™WÜ]Y\žWÜÚ[™ÛWÌÛÙ—ÍÌ‹šœÛÛ˜ˆ›ÝYÚˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™WÜ]Y\žWÜÚ[™ÛWÌMWÛÙ—ÍÌ‹šœÛÛ˜ˆ\Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WÜÚYÛ˜[ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™WÜ]Y\žWÜÚ[™ÛWØYÙÜ™YØ]WÌÌMWÛÙ—ÍÌ‹šœÛÛ˜‚ˆHYÙÜ™YØ]H™[XZ[œÈ™]šY]Ë[Û›KÛ›Û‹XÛÝ[X›H[™ÙY\Âˆ[ÝWÜØÛÜ™WÚÛÝ]ØÛZ[WÜ\›Z]YY˜[ÙX‚‹H™^\™XÝ›ÛÙYZÈÛÜšÈÚÝ[Ý\]ÝYÙY[™^Mˆ[™\ˆ›Ý[™NBˆ™XY[™\ÜËˆÝÜÛˆ[žHHHØ˜Z[‹Ý\Ý›ØÚÙ\ˆ[™›Û][ÈBˆ™]ÈÛ\Ý\‹Yš\œÝ›Ý[™™Y›Ü™HÛÛ[Z[™Ë‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆH™]ÈYÙÜ™YØ]H[ˆ\ÝÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]X[™ˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[Ü˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLMULŽŒL–‚‹HS‘QÐUˆŒ‹LKLMULÎŒÌNM–‚‹HYX\Ý\™Y[\ÙY[YNˆËÌÌÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝH˜[ˆ›Ý[™NÚ[™ÛK\]Y\žHÚXÚÜÈœ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™šœÛÛ˜‚ˆÝYÙY[™XÙ\ÈŽMÎ\ÜÙY™Y›Ü™HÝYÙY[™^ÎH^ÜÙY[[Ý]ˆÝ][Ù‹\ØÛÜHWØÜØNŽ™\œÝ\È[‹Y\ÝšX][ÛˆWØÜØN[™WØÜØNMŽXˆ]X^K\ØÛÜ™HŽÌ˜‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™WÌLšœÛÛ˜ˆ[™\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™KšœÛÛ˜‚ˆ›Ý[™H\ÈHYÚUHÛÛœÝ˜Z[ËNHÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYˆš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™[Ý™\ÈHWØÜØNŽYÚUBˆ™ZYÚ›ÜšÛÙÈ[‹Y\ÝšX][ÛˆÚ[HÙY\[™ÈÛÝ[X›HX™[È[™ˆ[\Ü\™XYH›ÝÜË‚‹H\™XÝ›Ý[™NH™\šYšXØ][Ûˆ™\˜[ˆÝYÙY[™^ÎH[™ÛÛ[YY›ÝYÚˆÝYÙY[™^ËˆHYÙÜ™YØ]HÛÝ™\œÈH]Y\žHÛÛÜ™[˜]\ËÍX\Y›ÝÜËˆÍŒÈ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HÍØ[™\™Ù]]š[Û][™ÈZ\œË‚ˆ™^\™XÝ›ÛÙYZÈÛÜšÈÚÝ[Ý\]ÝYÙY[™^[™\ˆ›Ý[™NBˆ™XY[™\ÜË‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆ”ÓÓˆ\œÚ[™È›ÜˆŒH™]È›ÛÙYZÈ\Y˜XÝËˆ›ØÝ\ÙY\Y˜XÝ\ÝËÚ]Y™ˆKXÚXÚØUÓ”U\Ü˜È]Ûˆ[Bˆ[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]\ÝËUÓ”U\Ü˜È]Ûˆ[BˆØ][]X×ÙX\˜ÛH˜[Y]X[™UÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[Ü˜Âˆ\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLMUŒNŒÖ‚‹HS‘QÐUˆŒ‹LKLMUNV‚‹HYX\Ý\™Y[\ÙY[YNˆŒŒÌÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝH\ÛÛ]YH[YY[Ý]›Ý[™MÈZXÜ›ØÚ[šÈŒÌŒÚ]Û™K\]Y\žBˆÚXÚÜÈœ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ËšœÛÛ˜‚ˆÝYÙY[™XÙ\ÈŒMŒˆ
WØÜØNŒXXWØÜØNŒØ
H\ÜÈ[ˆYÙÜ™YØ]H]X^ˆK\ØÛÜ™HŽMØÈÝYÙY[™XÙ\ÈŒËMH
WØÜØNXWØÜØN˜
H\ÜÈ[‚ˆYÙÜ™YØ]H]X^K\ØÛÜ™HMŒŽXÈÝYÙY[™^ˆ
WØÜØNØ
H\ÜÙ\È]ˆX^K\ØÛÜ™HLÍX‚‹HÝYÙY[™^È
WØÜØNŽ
H^ÜÙ\ÈH™]ÈWØÜØNŽØWØÜØNÍL›ØÚÙ\ˆ]ˆX^K\ØÛÜ™HÎLXˆ›Ý[™›ÛÈ]Z\ˆ[Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌLšœÛÛ˜Ú]ˆÎHYÚUHÛÛœÝ˜Z[ËNÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYš[Û][ÛœËˆÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]ËÛÝ[X›HX™[Ë[™[\Ü\™XYH›ÝÜËˆ]Âˆ™XY[™\ÜÈ\Y˜XÝ\Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™šœÛÛ˜‚‹HÜ˜ËØØ][]X×ÙX\ÙÙ[™\˜[^˜][Û‹œX›ÝÈ[™Ù\ÝÈš[ÜˆÛ\Ý\‹Yš\œÝˆ\][Û—ØÛÛœÝ˜Z[Ø\ÈZ\‹XØXÚH]šY[˜ÙHÛÈ[˜Ü™[Y[[›Ý[™ÈØ[‚ˆ™]\ÙHHÛ\Ý\ˆØXÚH˜]\ˆ[ˆ™XÛÛœÝXÝ[™È]™\žHÛÝ\˜ÙH\Y˜XÝ‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆ”ÓÓˆ\œÚ[™È›ÜˆLÈ™]È›ÛÙYZÈ\Y˜XÝË‚ˆ›ØÝ\ÙY\Y˜XÝØØXÚH\ÝËÚ]Y™ˆKXÚXÚØUÓ”U\Ü˜È]Ûˆ[Bˆ[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ÎMˆ\ÝËUÓ”U\Ü˜È]Ûˆ[BˆØ][]X×ÙX\˜ÛH˜[Y]X[™UÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\BˆÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLMUÎŒŒÌ‚‹HS‘QÐUˆŒ‹LKLMUÎNŒ‚‹HYX\Ý\™Y[\ÙY[YNˆLËMÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝH˜[ˆÛ\Ý\‹Yš\œÝ›Ý[™MˆÝX˜Ú[šÈLÌLL˜œ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™‹šœÛÛ˜‚ˆ][YYÝ][™\ˆHL\ÙXÛÛ™›Ý[™™Y›Ü™HZ\ˆ›ÝÜÈÙ\™H[Z]YˆX]š[™È[K\ØÛÜ™HÛÝ]ÛZ[\È›Ü˜šY[‹‚‹HÜ]]Ø[YH]Y\žHÚ[™ÝÈ[ÈË\]Y\žHZXÜ›ØÚ[šÜËˆ›Ý[™MˆZXÜ›ØÚ[šÂˆŒÌŒÛÛ\]YÚ]ËX\Y›ÝÜËKÌNH˜Z[‹Ý\Ý›ÝÜËX^ˆK\ØÛÜ™HÌLM˜[™Û™H›ØÚÙ\Žˆ[‹Y\ÝšX][ÛˆWØÜØNŒØ™\œÝ\Âˆ[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒN‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™×ÌLšœÛÛ˜ˆ[™\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ËšœÛÛ˜‚ˆ›Ý[™È\ÈÎYÚUHÛÛœÝ˜Z[ËMÈÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYˆÛ›ÝÛˆš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]Ý][Ù‹\ØÛÜH˜[ÙBˆ›Û‹XXœÝ[[ÛœË[™[Ý™\ÈWØÜØNŒNÈ[‹Y\ÝšX][Û‹ˆ]È\™XÝˆZXÜ›ØÚ[šËLŒ™\[ˆ[YYÝ][™\ˆHL\ÙXÛÛ™›Ý[™ÛÈH™\Z\ˆ\Âˆ›Ý™\šYšYY‚‹HÛÛ[YHœ›ÛH›Ý[™MÈ™XY[™\ÜÈžH\ÛÛ][™ÈZXÜ›ØÚ[šÈŒÌŒÚ]ˆÚ[™ÛK\]Y\žHÚXÚÜÈ›ÜˆÝYÙY]Y\žH[™XÙ\ÈŒŒK[™Œ‹ˆÛ›H[‚ˆ›ØÙYYÈH[œ[ˆWØÜØNXWØÜØN˜[ˆÙˆÜšYÚ[˜[ÝX˜Ú[šÈL‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØ”ÓÓˆ\œÚ[™È›ÜˆHH™]Âˆ›ÛÙYZÈ\Y˜XÝËH›ØÝ\ÙY\Y˜XÝ\[ˆ\ÝËUÓ”U\Ü˜È]Û‚ˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ÎLH\ÝËUÓ”U\Ü˜È]Ûˆ[BˆØ][]X×ÙX\˜ÛH˜[Y]X[™UÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\BˆÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLMUŽŒÎ–‚‹HS‘QÐUˆŒ‹LKLMUŽN‚‹HYX\Ý\™Y[\ÙY[YNˆKŒŒZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝH˜[ˆÛ\Ý\‹Yš\œÝ›Ý[™MÝX˜Ú[šÈœ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™šœÛÛ˜‚ˆ]ÛÛ\]YÚ]HX\Y›ÝÜËKM˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™BˆÌŒX[™Û™H›ØÚÙ\ŽˆWØÜØNM™\œÝ\È[[Ý]Ý][Ù‹\ØÛÜBˆWØÜØNŽ‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™WÌLšœÛÛ˜ˆ[™\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™KšœÛÛ˜‚ˆ›Ý[™H\ÈÍˆYÚUHÛÛœÝ˜Z[ËMHÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYˆš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]Ý][Ù‹\ØÛÜH˜[ÙBˆ›Û‹XXœÝ[[ÛœË[™[Ý™\ÈWØÜØNŽÈ[‹Y\ÝšX][Û‹ˆ]È\™XÝˆÝX˜Ú[šËL™\[ˆ\ÜÙ\ÈÚ]HX\Y›ÝÜËKLÌˆ˜Z[‹Ý\Ý›ÝÜËX^ˆK\ØÛÜ™HŽNX[™\™Ù]]š[Û][™ÈZ\œË‚‹H\™XÝH˜[ˆ›Ý[™MHÝX˜Ú[šÈKˆ]ÛÛ\]YÚ]MKLÌHX\Y›ÝÜËˆ‹MMH˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HŽÎX[™Û™H›ØÚÙ\ŽˆWØÜØNNˆ™\œÝ\È[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒŽ‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™—ÌLšœÛÛ˜ˆ[™\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™‹šœÛÛ˜‚ˆ›Ý[™ˆ\ÈÍÈYÚUHÛÛœÝ˜Z[ËMˆÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYˆš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]Ý][Ù‹\ØÛÜH˜[ÙBˆ›Û‹XXœÝ[[ÛœË[™[Ý™\ÈWØÜØNŒŽÈ[‹Y\ÝšX][Û‹ˆ]È\™XÝˆÝX˜Ú[šËLH™\[ˆ\ÜÙ\ÈÚ]MKLÌHX\Y›ÝÜË‹LÎH˜Z[‹Ý\Ý›ÝÜËˆX^K\ØÛÜ™HŽNX[™\™Ù]]š[Û][™ÈZ\œËˆÛÛ[YHœ›ÛH›Ý[™M‚ˆÝX˜Ú[šÈLÌLL˜ÈÝÜ[™›Û[ˆ[žH™]ÈYÚUH›ØÚÙ\ˆ™Y›Ü™BˆÛÛ[Z[™Èœ›ØYÛÝ™\˜YÙK‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØ”ÓÓˆ\œÚ[™È›ÜˆHL™]Âˆ›ÛÙYZÈ\Y˜XÝËUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆÚ]ÎÈ\ÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]Xˆ[™UÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLMUNŒŽŒM–‚‹HS‘QÐUˆŒ‹LKLMUNŒLV‚‹HYX\Ý\™Y[\ÙY[YNˆKŽLMÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™™YÙ[™\˜]YÛÜšËÜÝ]\Ë›Y™Y›Ü™BˆÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H\™XÝH™\˜[ˆÛ\Ý\‹Yš\œÝ›Ý[™LÈÝX˜Ú[šÜÈˆ[™Èœ›ÛBˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ËšœÛÛ˜‚ˆÝX˜Ú[šÈˆ\ÜÙYÚ]MŒÈX\Y›ÝÜË‹ÍMˆ˜Z[‹Ý\Ý›ÝÜËX^ˆK\ØÛÜ™HLX[™\™Ù]]š[Û][™ÈZ\œËˆÝX˜Ú[šÈÈ˜Z[YÚ]ˆKMX\Y›ÝÜËMÍˆ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HŽØ[™Û™Bˆ›ØÚÙ\‹WØÜØNX™\œÝ\È[[Ý]Ý][Ù‹\ØÛÜHWØÜØNŒÎMØ‚‹HYY\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ÌLšœÛÛ˜ˆ[™\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™šœÛÛ˜‚ˆ›Ý[™\ÈÍHYÚUHÛÛœÝ˜Z[ËMÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYˆš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[[Ý]Ý][Ù‹\ØÛÜH˜[ÙBˆ›Û‹XXœÝ[[ÛœË[™[Ý™\ÈWØÜØNŒÎMØÈ[‹Y\ÝšX][Û‹‚‹HH\™XÝ›Ý[™MÝX˜Ú[šËLÈ™\[ˆ\ÜÙ\ÈÚ]KMX\Y›ÝÜËMÍBˆ˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HNN[™\™Ù]]š[Û][™ÈZ\œË‚ˆÛÛ[YHÚ]›Ý[™Y™\šYšXØ][Ûˆœ›ÛHH›Ý[™M™XY[™\ÜËÝ\[™ÈÚ]ˆH™^[™\šYšYYÝX˜Ú[šÈÌLL˜ˆÝÜ[™›Û[ˆ[žH™]ÈYÚUBˆ›ØÚÙ\ˆ™Y›Ü™HÛÛ[Z[™Èœ›ØYÛÝ™\˜YÙK‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØ”ÓÓˆ\œÚ[™È›ÜˆHˆ™]Âˆ›ÛÙYZÈ\Y˜XÝËUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆÚ]ÎÈ\ÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]X[™ˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLMUŒ–‚‹HS‘QÐUˆŒ‹LKLMUMŽŒ‚‹HYX\Ý\™Y[\ÙY[YNˆMKŒÍÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÙ›ÛÙYZ×Ü™XY[™\Ü×Û›Ý\Ë›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜØÛÜK›Y[™ÛÜšËÜÝ]\Ë›Y™Y›Ü™HÛÛ[Z]‚‹H›Ü›X[ØÚÙY\™XÝ[ˆÚ]›ÈÝX˜YÙ[ÈÜˆ[YØ][Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[ˆÜ›ÝÝ[™›È^\›˜[[\Ü‚‹H[\[Y[YZ[Y›ÛÙYZË]K\ØÛÜ™KXÛ\Ý\‹Yš\œÝ\Ü]H™]šY]Ë[Û›BˆÛ\Ý\‹Yš\œÝØ[™Y]HZ[\ˆ]\›œÈØœÙ\™YHHØ›ÛÙYZÂˆ]šY[˜ÙH[ÈÝXÝ\˜[\][ÛˆÛÛœÝ˜Z[È™Y›Ü™H™\šYšXØ][ÛˆÚ[šÜÂˆ[‹‚‹HHÝ\œ™[[™Ù™ˆÜ]\Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ÝWÜØÛÜ™WØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™×ÌLšœÛÛ˜ˆÍˆYÚUHÛÛœÝ˜Z[ËMÛÛœÝ˜Z[™YÛ\Ý\œË›Ú™XÝYÛ›ÝÛ‚ˆ˜Z[‹Ý\Ýš[Û][ÛœËÙ\]Y[˜ÙKXÛ\Ý\ˆÜ]Ë[™ÛÝ[X›KÚ[\Ü\™XYBˆ›ÝÜËˆ]È™XY[™\ÜÈ\Y˜XÝ\Âˆ\Y˜XÝËÝŒ×Ù›ÛÙYZ×ØÛÛÜ™[˜]WÜ™XY[™\Ü×ÌLØÛ\Ý\—Ùš\œÝÜÜ]Ü›Ý[™ËšœÛÛ˜‚‹H™\šYšXØ][Ûˆ]šY[˜ÙNˆ›Ý[™LˆÝX˜Ú[šÈˆ\ÜÙ\ÈÚ]MŒÈX\Y›ÝÜËˆ‹ÍN˜Z[‹Ý\Ý›ÝÜËX^K\ØÛÜ™HLX[™\™Ù]]š[Û][™ÈZ\œË‚ˆ›Ý[™LˆÝX˜Ú[šÈÈ˜Z[ÈÚ]KMX\Y›ÝÜËKH˜Z[‹Ý\Ý›ÝÜËˆX^K\ØÛÜ™HŽLX[™Mˆ\™Ù]]š[Û][™È›ÝÜÈXÜ›ÜÜÈH™\ÜYˆÝXÝ\™HZ\œÎÈÜÙH›ØÚÙ\œÈ\™H›ÛY[ÈH›Ý[™LÈÜ]ˆ™^ˆ™\šYšXØ][ÛˆÚÝ[™\[ˆÝX˜Ú[šÈÈœ›ÛHH›Ý[™LÈ™XY[™\ÜÈ[™ÝÜˆÛˆ[žH™]È\™Ù]š[Û][Û‹‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ÎÈ\ÝËˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ[™”ÓÓˆ\œÚ[™È›Ü‚ˆHL™]È›ÛÙYZÈ\Y˜XÝË‚‚‹HÕT•QÐUˆŒ‹LKLMÎŒÌÎŒN‚‹HS‘QÐUˆŒ‹LKLMŒŒÎŒ–‚‹HYX\Ý\™Y[\ÙY[YNˆLŒLÌÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÛX™[Ù˜XÝÜžK›YÛÜšËÜØÛÜK›YˆÛÜšËÚ[™Ù™‹›Y[™ÛÜšËÜÝ]\Ë›Y™Y›Ü™HÛÛ[Z]‚‹H›Ü›X[ØÚÙY[YØ]Y[ˆ\ˆ\Ù\ˆ[œÝXÝ[Û‹ˆ›ÈKPÔÐK[Û›HÛÝ[Ü›ÝÝˆ[™›È^\›˜[[\ÜˆH[ˆYYH™X[S\Ù\\Ìˆ˜XÚÙ[™^\›˜[Ù\]Y[˜ÙBˆÙX\˜Ú›ÜˆHÌ\›ÝÈ[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[\KÚ\™Y][Âˆ[\Ü\™XY[™\ÜËH›ØÚÙ\ˆX]š^˜[œÙ™\ˆØ]KÙ[XÝY\[Ýš[Üš]Kˆ[ÝXÚÙ]Ë™\™\Ù[][Ûˆ[‹ÜØ[\K[™[ÝÜÜÚY\œË‚‹HH˜XÚÙ[™ÙX\˜Ú\Ù\ÈS\Ù\\ÌˆNNØÍXØÛÝ™\œÈÌ^\›˜[›ÝÜÈYØZ[œÝˆÌÍHÝ\œ™[™Y™\™[˜ÙHXØÙ\ÜÚ[ÛœÈÈÌÍÈÙ\]Y[˜ÙH™XÛÜ™ËÙY\È^XÝÛÝ]ÂˆÌMMLØ[™ŒL˜™XÛÜ™ÈŽÝ\œ™[\™Y™\™[˜ÙH›Ë\ÚYÛ˜[›ÝÜËˆ™X\‹Y\XØ]H›ÝÜË˜Z[\™\ËÛÝ[X›H›ÝÜË[™[\Ü\™XYH›ÝÜË‚ˆHÙ[XÝY[Ý›ÝÜÈ›ÈÛ™Ù\ˆØ\œžHÝ[HÛÛ\]K[™X\‹Y\XØ]K\ÙX\˜Úˆ›ØÚÙ\œÈ›Üˆ˜XÚÙ[™›Ë\ÚYÛ˜[]šY[˜ÙNÈœ›ØY\ˆ[šT™Y‹Ø[]œËX[\XØ]BˆØÜ™Y[š[™È™[XZ[œÈH[Z]][Ûˆ™Y›Ü™H[\Ü‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\Âˆ\ÝØÚ]ÌLÈ\ÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛBˆ˜[Y]XUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØÚ]Y™‚ˆKXÚXÚØ[™”ÓÓˆ\œÚ[™ÈXÜ›ÜÜÈMÌˆ\Y˜XÝš[\ËˆH^\›˜[˜[œÙ™\‚ˆØ]H\ÜÙ\ÈËÍÈ™]šY]Ë[Û›HÚXÚÜË‚‚‹HÕT•QÐUˆŒ‹LKLLÕŒÎŒŽ‚‹HS‘QÐUˆŒ‹LKLLÕŒÎLNM–‚‹HYX\Ý\™Y[\ÙY[YNˆKŒÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YˆÛÜšËÜÝ]\Ë›Y[œ]Ë[™ÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÌLWÛ›Ý\Ë›Y™Y›Ü™BˆÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙYÔÑ‹Z\™[š[™È[ˆÙ\KPÔÐK[Û›HÜ›ÝÝÝÜY[™Y›Ýˆ[\Ü^\›˜[X™[ËˆHÛÙKXÛÛ™š\›YY›ØÚÙ\ˆØ\ÈÙ[XÝY\[Ýˆ™\™\Ù[][ÛˆÛÝ™\˜YÙNˆ[ÝÜÜÚY\œÈY™\™\Ù[][Ûˆ›ÝÜÈ›ÜˆÛ›HˆÙˆHLÙ[XÝYØ[™Y]\È™XØ]\ÙH^H\[™YÛˆHL‹\›ÝÈX\YˆÛÛ›ÛØ[\K‚‹HH[ˆYYH[Ý\ÜXÚYšXÈ™\™\Ù[][Ûˆ˜XÚÙ[™[‹ÜØ[\H›Üˆ[LˆÙ[XÝY[ÝØ[™Y]\Ë™Yœ™\ÚYH[ÝÜÜÚY\œËYYH[Ýˆ™\™\Ù[][ÛˆØ[\HÈØ[™Y]K[[™XYÙH˜[Y][Û‹[™YYH›ØÝ\ÙYˆØ]H™\]Z\š[™ÈÙ[XÝY\[Ý™\™\Ù[][ÛˆØ[\HÛÝ™\˜YÙKˆH˜[œÙ™\‚ˆØ]H›ÝÈ\ÜÙ\È‹Íˆ[™ÙY\È[^\›˜[›ÝÜÈ™]šY]Ë[Û›Kˆ›Û‹XÛÝ[X›K[™›Ý[\Ü\™XYNÈMLŒØ\ÈH™\™\Ù[][Û‚ˆ™X\‹Y\XØ]HÛÝ]‚‹H™[XZ[š[™Ë][YH[ˆ^XÝ]Y[ˆHØ[YH[ŽˆY\ˆH[ÝØ[\HÛÝ™\™Yˆ[Ù[XÝY›ÝÜË\™[ˆH\Y˜XÝÜ˜\žHY[™ÈH™YØ]]™H™YÜ™\ÜÚ[Û‚ˆ›ÜˆÝ[H[Ý™\™\Ù[][ÛˆØ[\H›ÝÜÈ[™H\™XÝØ]HÚXÚÈ›Ü‚ˆÙ[XÝY\[Ý™\™\Ù[][ÛˆÛÝ™\˜YÙK‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\Âˆ\ÝØÚ]ŽN\ÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛBˆ˜[Y]XUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØˆÚ]Y™ˆKXÚXÚØ[™”ÓÓˆ\Y˜XÝ\œÚ[™ÈÚ]œH[\X‚‚‹HÕT•QÐUˆŒ‹LKLLÕŒŽŒNŒÎ‚‹HS‘QÐUˆŒ‹LKLLÕŒŽŒÌÎMV‚‹HYX\Ý\™Y[\ÙY[YNˆŒŽÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YˆÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›Y[™ˆÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÌLWÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙYÔÑ‹Z\™[š[™È[ˆÙ\KPÔÐK[Û›HÜ›ÝÝÝÜY[™Y›Ýˆ[\Ü^\›˜[X™[ËˆÛÝ[\™]šY[˜ÙHXZ[Z[˜Xš[]K^XZØYÙKˆÙ\]Y[˜ÙKÙ›Û›ÞHÛÝ]X\›™Y™\™\Ù[][ÛˆØ[\K[™Ù[XÝYT‚ˆÝ™\œšYH]šY[˜ÙHÙ\™H[™XYH™\Ù[ÛÈH›Ý[™Y[˜›ØÚÙY][HØ\ÈBˆ\Y˜XÝYÜ˜\ÛÛœÚ\Ý[˜ÞHØ\[ˆH^\›˜[˜[œÙ™\ˆØ]K‚‹HH^\›˜[Ø]IÜÈÚ\™YØ[™Y]K[[™XYÙH™YÚ\ÝžH›ÝÈ[˜ÛY\ÂˆÙ\]Y[˜ÙWÚÛÝ]Ø]Y]ÈH™YØ]]™H™YÜ™\ÜÚ[ÛˆÚÝÜÈHZ\ÛX]ÚYÛÝ]ˆXØÙ\ÜÚ[Ûˆ˜Z[ÈH[™XYÙHØ]K[™ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÙØ]WØÚXÚ×ÌLKšœÛÛ˜Ý[\ÜÙ\ÂˆKÍHÚ]ÛÝ[X›KÚ[\Ü\™XYH^\›˜[›ÝÜË‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\Âˆ\ÝØÚ]ŽMˆ\ÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛBˆ˜[Y]XUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØˆÚ]Y™ˆKXÚXÚØ[™Ú[™ÙY”ÓÓˆ\Y˜XÝ\œÚ[™Ë‚‚‹HÕT•QÐUˆŒ‹LKLLÕŽŒŽŒÎ‚‹HS‘QÐUˆŒ‹LKLLÕŽMÎ–‚‹HYX\Ý\™Y[\ÙY[YNˆLKŒLÌÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YˆÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›YˆÛÜšËÛX™[Ü™]šY]×ÌLWÛ›Ý\Ë›YÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÌLWÛ›Ý\Ë›Yˆ[™ÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWØÛÛ›ÛÜ™\Z\—ÌLWÛ›Ý\Ë›Y™Y›Ü™HÝ]\Âˆ™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆÙ\^\›˜[[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[™Y]\È™]šY]Ë[Û›Bˆ[™™\Z\™YHÜÝSKPÔÐH˜[œÙ™\ˆÛÛ›ÛÈÚ]Ý][\Ü[™ÈX™[Ë‚‹H^[™YÝXÝ\™HX\[™È[™]\š\ÝXÈØÛÜš[™Èœ›ÛHÈ[L‚ˆ]\š\ÝXË\™XYH^\›˜[ÛÛ›ÛËYYÛÛ›Û\™\Z\‹™\™\Ù[][Û‹ˆš[™[™ËXÛÛ^[™XXÝ[Û‹XÛÛ^[™Ù\]Y[˜ÙKZÛÝ]\Y˜XÝË[™ˆÙ\]™\žH^\›˜[›ÝÈ›Û‹XÛÝ[X›K‚‹HH^\›˜[˜[œÙ™\ˆØ]H›ÝÈ\ÜÙ\ÈÌËÌÌÈÚXÚÜÈ›Üˆ™]šY]Ë[Û›H]šY[˜ÙBˆÛÛXÝ[ÛŽÈH™\Z\ˆ[ˆ™XÛÜ™ÈH›Û‹XÛÝ[X›H™\Z\ˆ›ÝÜËBˆ™\™\Ù[][ÛˆX[šY™\Ý^ÜÙ\ÈLˆX\YÛÛ›ÛËHš[™[™ËXÛÛ^ˆØ[\HX\ÈËÍÈ›ÝÜÈ\ÈÛÛ^Û›K[™HÙ\]Y[˜ÙH]Y]ÙY\ÈÛÈ^XÝˆ™Y™\™[˜ÙHÝ™\›\È\ÈÛÝ]Ë‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]È\ÝËˆ\™Ù]Y^\›˜[]˜[œÙ™\‹ÜØØ[[™È\ÝË”ÓÓˆ\Y˜XÝ\œÚ[™Ë^\›˜[ˆ[\ÜØÛÝ[X›Hš[Û][ÛˆØØ[‹[™]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLLÕŒŒÍ–‚‹HS‘QÐUˆŒ‹LKLLÕMNŒŽV‚‹HYX\Ý\™Y[\ÙY[YNˆLŽÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YØÜËÚ[™Ù\Ý[Û—Ü[‹›YˆØÜËÜ™\ÙX\˜ÚÜ›ÙÜ˜[K›YØÜËÜØY™]WÜØÛÜK›YØÜËÝŒ—Ü™\Ü›YˆØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YˆÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›YÛÜšËÛX™[Ü™]šY]×ÌLWÛ›Ý\Ë›Y[™ˆÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\—ÌLWÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHH›Û‹\›Û[ÝYKH™]šY]ÈÙ\KPÔÐK[Û›HÜ›ÝÝˆÝÜY[™\™[™Y^\›˜[\ÛÝ\˜ÙH˜[œÙ™\ˆÚ]Ý][\Ü[™ÈX™[Ë‚‹HYY™]šY]Ë[Û›H^\›˜[Ø[™Y]HX[šY™\ÝX[šY™\Ý]Y][™KX˜[[˜ÙBˆ]Y]]šY[˜ÙH[‹Ù^ÜXÝ]™K\Ú]H]šY[˜ÙH]Y]YK[\Ü\ØY™]H]Y]ˆLKÌLH˜[œÙ™\ˆØ]KšXH™XXÝ[Û‹XÛÛ^Ø[\K[™™XXÝ[Û‹XÛÛ^]Y]‚ˆ[^\›˜[\Y˜XÝÈÙY\ÛÝ[X›WÛX™[ØØ[™Y]WØÛÝ[L‚‹HH]šY[˜ÙH[ˆ›YÜÈÙ]™[ˆœ›ØYÚ[˜ÛÛ\]HPÈØ[™Y]\ÎÈHXÝ]™K\Ú]Bˆ]šY[˜ÙH]Y]YH^ÜÈH™XYH™]šY]Ë[Û›HØ[™Y]\È[™Y™\œÈš]™H›ÝÜÂˆ
ÛÈ^XÝ\™Y™\™[˜ÙHÛÝ]È[™™YHœ›ØYQPÈ\Ø[XšYÝX][ÛˆØ\Ù\ÊK‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ŒÌ\ÝËˆ\™Ù]Y^\›˜[]˜[œÙ™\ˆ\ÝË[™]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLLÕÎŒÎŒM‚‹HS‘QÐUˆŒ‹LKLLÕÎML‚‹HYX\Ý\™Y[\ÙY[YNˆLKŒZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙÙ[ÛY]žWÙ™X]\™\Ë›YØÜËÜ\™›Ü›X[˜ÙK›YˆØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YØÜËÝŒ—Ü™\Ü›YˆØÜËÜ™\ÙX\˜ÚÜ›ÙÜ˜[K›YØÜËÚ[™Ù\Ý[Û—Ü[‹›YØÜËÜØY™]WÜØÛÜK›YˆØÜËÙ^\›˜[ÜÛÝ\˜ÙWÝ˜[œÙ™\‹›YÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YˆÛÜšËÜÝ]\Ë›Y[œ]ËÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›Y[™ˆÛÜšËÛX™[Ü™]šY]×ÌLWÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YLÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[Ü[™YH›Ý[™YLH™]šY]Ë[™ÝÜY›Û[Ý[ÛˆÚ[‚ˆHXØÙ\[˜ÙH\Y˜XÝYYÛX[ˆÛÝ[X›HX™[Ë‚‹HHLH™]šY]ÈØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ëˆ™X\ˆZ\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜBˆ˜Z[\™\ËXØÙ\Y™]šY]ËYØ\X™[Ë[™™]šY]Ë[Û›H[\ÜÛÝ[ˆÜ›ÝÝˆ[ÌŽH™]šY]È™]šY]Ë\Ý]H›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›K‚‹HÛÝ\˜ÙK\ØØ[H]Y]›ÝÈ™XÛÜ™ÈKÈØœÙ\™YKPÔÐHÛÝ\˜ÙH™XÛÜ™È›ÜˆBˆ™\]Y\ÝYKH˜[˜ÚKÛÈKPÔÐK[Û›HØØ[[™È\ÈHXÝ]™H›Ý[™XÚËˆBˆ[ˆYY™]šY]Ë[Û›H^\›˜[\ÛÝ\˜ÙH˜[œÙ™\‹]Y\žKÓÑØ[Xœ˜][Û‹ˆÌ\›ÝÈ[šT›ÝÐ‹ÔÝÚ\ÜËT›ÝØ[™Y]HØ[\K[™Ø[\HÝX\™˜Z[\Y˜XÝÂˆÚ]ÛÝ[X›H^\›˜[Ø[™Y]\Ë‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ŒMÈ\ÝËˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ[™”ÓÓˆ\œÚ[™ÈXÜ›ÜÜÂˆMŒÈ\Y˜XÝÜ™YÚ\ÝžHš[\Ë‚‚‹HÕT•QÐUˆŒ‹LKLLÕNŒŒÎV‚‹HS‘QÐUˆŒ‹LKLLÕŽŒNŒ–‚‹HYX\Ý\™Y[\ÙY[YNˆŒŒÎÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙÙ[ÛY]žWÙ™X]\™\Ë›YØÜËÜ\™›Ü›X[˜ÙK›YˆØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YØÜËÝŒ—Ü™\Ü›YÛÜšËÜØÛÜK›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜÝ]\Ë›Y[œ]ËÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›YˆÛÜšËÛX™[Ü™]šY]×ÎMÍWÛ›Ý\Ë›Y[™ÛÜšËÛX™[Ü™]šY]×ÌLÛ›Ý\Ë›Y™Y›Ü™BˆÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YMLÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[XØÙ\YH›Ý[™YMÍH˜]Ú[ˆÜ[™Y™\Z\™Y[™ˆXØÙ\YH›Ý[™YL˜]Ú‚‹HHLØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ë™X\‚ˆZ\ÜÙ\ËÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜBˆ˜Z[\™\ËXØÙ\Y™]šY]ËYØ\X™[ËXØÙ\Y™XXÝ[Û‹ÜÝXœÝ˜]BˆZ\ÛX]ÚX™[Ë[™™]šY]Ë[Û›H[\ÜÛÝ[Ü›ÝÝ‚‹HHØ[›ÛšXØ[™YÚ\ÝžH›ÝÈ\ÈÎHX™[Ëˆ[ÌˆXØÙ\YLL™]šY]Ë\Ý]Bˆ›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›H[™\‚ˆ\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÌLšœÛÛ˜[˜ÛY[™ÈBˆŒH™]ÈL\™]šY]È™]šY]ËYX›ÝÜËˆWØÜØNŽN˜\È^XÚ]HY™\œ™Y\ÂˆØØ[Z[YHÝË\ØÛÜ™H›Ý[™\žH]šY[˜ÙH˜]\ˆ[ˆÛÝ[YÝ][Ù‹\ØÛÜK‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]Œˆ\ÝËˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ[™”ÓÓˆ\œÚ[™ÈXÜ›ÜÜÂˆ\Y˜XÝÜ™YÚ\ÝžHš[\Ë‚‚‹HÕT•QÐUˆŒ‹LKLL•ŒÎNŒÎ‚‹HS‘QÐUˆŒ‹LKLLÕLŒ‚‹HYX\Ý\™Y[\ÙY[YNˆLKÍÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙÙ[ÛY]žWÙ™X]\™\Ë›YØÜËÜ\™›Ü›X[˜ÙK›YˆØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YØÜËÝŒ—Ü™\Ü›YÛÜšËÜØÛÜK›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜÝ]\Ë›Y[œ]ËÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›Y[™ˆÛÜšËÛX™[Ü™]šY]×ÎMLÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YLÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[[ˆXØÙ\YH›Ý[™YÍKLLK[™ML˜]Ú\Ë‚‹HHMLØ]H\ÜÙ\ÈŒKÌŒHÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\ËˆXØÙ\Y™]šY]ËYØ\X™[ËXØÙ\Y™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚX™[Ëˆ[™™]šY]Ë[Û›H[\ÜÛÝ[Ü›ÝÝ‚‹HHØ[›ÛšXØ[™YÚ\ÝžH›ÝÈ\ÈÌÈX™[Ëˆ[ŽˆXØÙ\YNML™]šY]Ë\Ý]Bˆ›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›H[™\‚ˆ\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÎMLšœÛÛ˜[˜ÛY[™ÈBˆNH™]ÈML\™]šY]È™]šY]ËYX›ÝÜËˆWØÜØNŽX\È^XÚ]HÛ\ÜÚYšYY\Âˆ^\Ü™]šY]×ÙXÚ\Ú[Û—Û™YYY˜]\ˆ[ˆ[˜Û\ÜÚYšYY™]šY]ÈX‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ŒH\ÝËˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ[™”ÓÓˆ\œÚ[™ÈXÜ›ÜÜÂˆMÌˆ\Y˜XÝÜ™YÚ\ÝžHš[\Ë‚‚‹HÕT•QÐUˆŒ‹LKLL•MŽMŽŒKLNŒ‹HS‘QÐUˆŒ‹LKLL•MÎNŒLËLNŒ‹HYX\Ý\™Y[\ÙY[YNˆŒ‹ŒÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙÙ[ÛY]žWÙ™X]\™\Ë›YØÜËÜ\™›Ü›X[˜ÙK›YˆØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YØÜËÝŒ—Ü™\Ü›YÛÜšËÜØÛÜK›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜÝ]\Ë›Y[œ]ËÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›Y[™ˆÛÜšËÛX™[Ü™]šY]×ÎLÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YÍÍHÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[[ˆXØÙ\YH›Ý[™YK[™L˜]Ú\Ë‚‹HHLØ]H\ÜÙ\ÈŒÌŒÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\ËˆXØÙ\Y™]šY]ËYØ\X™[ËXØÙ\Y™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚX™[Ëˆ[™™]šY]Ë[Û›H[\ÜÛÝ[Ü›ÝÝ‚‹HHØ[›ÛšXØ[™YÚ\ÝžH›ÝÈ\ÈLˆX™[Ëˆ[ŒÈXØÙ\YNL™]šY]Ë\Ý]Bˆ›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›H[™\‚ˆ\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÎLšœÛÛ˜[˜ÛY[™ÈBˆŒˆ™]ÈL\™]šY]È™]šY]ËYX›ÝÜËˆWØÜØNŽÍ˜\È^XÚ]HY™\œ™Y\Âˆ›ÛKZ[™™\œ™YY][ZY›Û\ÙH]šY[˜ÙHÚ]Ý]ØØ[YØ[™Ý\Ü˜]\‚ˆ[ˆÛÝ[Y‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]ŒH\ÝËˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ[™œH[\XXÜ›ÜÜÂˆ”ÓÓˆ\Y˜XÝË‚‚‹HÕT•QÐUˆŒ‹LKLL•ŒMNŒV‚‹HS‘QÐUˆŒ‹LKLL•ŒNNM–‚‹HYX\Ý\™Y[\ÙY[YNˆLŽLZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙÙ[ÛY]žWÙ™X]\™\Ë›YØÜËÜ\™›Ü›X[˜ÙK›YˆØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YØÜËÝŒ—Ü™\Ü›YÛÜšËÜØÛÜK›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÜÝ]\Ë›Y[œ]ËÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›Y[™ˆÛÜšËÛX™[Ü™]šY]×ÍÍÍWÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YÍLÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[[ˆÜ[™Y™\Z\™Y[™XØÙ\YH›Ý[™YÍÍH˜]Ú‚‹HHÍÍHØ]H\ÜÙ\ÈŒÌŒÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\ËˆXØÙ\Y™]šY]ËYØ\X™[ËXØÙ\Y™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚX™[Ëˆ[™™]šY]Ë[Û›H[\ÜÛÝ[Ü›ÝÝ‚‹HHØ[›ÛšXØ[™YÚ\ÝžH›ÝÈ\ÈˆX™[Ëˆ[LÎXØÙ\YMÍÍH™]šY]Ë\Ý]Bˆ›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›H[™\‚ˆ\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÍÍÍKšœÛÛ˜[˜ÛY[™ÈBˆŒ™]ÈÍÍK\™]šY]È™]šY]ËYX›ÝÜËˆWØÜØNÍÌX\È^XÚ]HY™\œ™Y\ÂˆÛÝ[\™]šY[˜ÙKÝ^[XZØYÙHš\ÚÈ˜]\ˆ[ˆÛÝ[Y‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]Œˆ\ÝËˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ[™œH[\XXÜ›ÜÜÂˆ”ÓÓˆ\Y˜XÝË‚‚‹HÕT•QÐUˆŒ‹LKLL•NNMŒŒ–‚‹HS‘QÐUˆŒ‹LKLL•ŒŒMŒM–‚‹HYX\Ý\™Y[\ÙY[YNˆÎKŽLZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆØÜËÙÙ[ÛY]žWÙ™X]\™\Ë›YØÜËÝŒ—ÜÝ™[™Ý[š[™×Ü™\Ü›YÛÜšËÜØÛÜK›YˆÛÜšËÚ[™Ù™‹›YÛÜšËÛX™[Ù˜XÝÜžWÛ›Ý\Ë›Y[™ˆÛÜšËÛX™[Ü™]šY]×ÍÍLÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YÌHÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[[ˆ^XÚ]HY™\œ™YHÍL™]šY]È™]šY]ËYXÝ\™˜XÙBˆ[™›Û[ÝYHÙ]™[ˆÛX[ˆÍLØ[™Y]\È[ÈHØ[›ÛšXØ[™YÚ\ÝžK‚‹HHÍLØ]H\ÜÙ\ÈŒÌŒÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\ËˆXØÙ\Y™]šY]ËYØ\X™[ËXØÙ\Y™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚX™[Ëˆ[™™]šY]Ë[Û›H[\ÜÛÝ[Ü›ÝÝ‚‹HHØ[›ÛšXØ[™YÚ\ÝžH›ÝÈ\ÈŒÍÈX™[Ëˆ[LNXØÙ\YMÍL™]šY]Ë\Ý]Bˆ›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›H[™\‚ˆ\Y˜XÝËÝŒ×ØXØÙ\YÜ™]šY]×ÙXÙY™\œ˜[Ø]Y]ÍÍLšœÛÛ˜[˜ÛY[™ÈBˆN™]ÈÍL\™]šY]È™]šY]ËYX›ÝÜË‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]Œ\ÝË[™ˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLL•MÎLNV‚‹HS‘QÐUˆŒ‹LKLL•NLNŒÎV‚‹HYX\Ý\™Y[\ÙY[YNˆNKŽÌÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YÛÜšËÜÝ]\Ë›Y[œ]Ë[™ˆÛÜšËÛX™[Ü™]šY]×ÍÍLÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YÌHÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[[ˆYY[ˆXØÙ\YMÌH™]šY]ËYXY™\œ˜[]Y]Ú]ˆL›Û‹XÛÝ[X›H›ÝÜÈ[™\Ü˜YYHÌHØ]HÈŒKÌŒHÚXÚÜË‚‹H™[XZ[š[™Ë][YH[ˆ^XÝ]Y™Y›Ü™HÜ˜\]\ˆY\ˆHÌHY™\œ˜[]Y]Ø\ÂˆÛX[‹Ü[™YH›Ý[™YÍL™]šY]ËˆHÍL™]šY]ÈÙ[™\˜]YÜ˜\ˆÙ[ÛY]žK™]šY]˜[X™[Y˜XÝÜžK™]šY]È^ÜXØÙ\[˜ÙKØØ[[™Ë\]X[]KˆÛÛÙÞKYØ\X\›™Y\™]šY]˜[[™Ù\]Y[˜ÙK\Ú[Z[\š]H\Y˜XÝËˆ]›Ý[™ˆÈYXÚ[šXØ[HÛX[ˆØ[™Y]\È[™HNKÌNH™]šY]ÈØ]K]›Û[Ý[Ûˆ\ÂˆY™\œ™Y™XØ]\ÙHN™]È™]šY]ËYX›ÝÜÈ™\]Z\™H™\Z\ˆÜˆ^XÚ]Y™\œ˜[‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØœH[\XÝ™\ˆ™YÙ[™\˜]Yˆ”ÓÓˆ\Y˜XÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]Œ\ÝË[™ˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HÕT•QÐUˆŒ‹LKLL•LNLNŒËLNŒ‹HS‘QÐUˆŒ‹LKLL•LŽÎŒŒLNŒ‹HYX\Ý\™Y[\ÙY[YNˆMKŽÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YÛÜšËÜÝ]\Ë›Y[œ]Ë[™ˆÛÜšËÛX™[Ü™]šY]×ÍÌWÛ›Ý\Ë›Y™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YÌÝ]Hš\œÝXYH[ˆ]šY[˜ÙKX˜\ÙYˆÛÛ™šY[˜ÙHØ[[ˆXØÙ\YH›Ý[™YÌHX™[Y˜XÝÜžH˜]ÚÚ]‚ˆÛX[ˆÛÝ[X›HX™[È[™L™]šY]Ë\Ý]H›ÝÜÈÙ\Ý]ÚYHH™[˜ÚX\šË‚‹HHÌHØ]H\ÜÙ\ÈŒÌŒÚXÚÜÈ[™™XÛÜ™È\™™YØ]]™\Ë™X\ˆZ\ÜÙ\ËˆÝ][Ù‹\ØÛÜH˜[ÙH›Û‹XXœÝ[[ÛœËXÝ[Û˜X›H[‹\ØÛÜH˜Z[\™\ËˆXØÙ\Y™]šY]ËYØ\X™[ËXØÙ\Y™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]ÚX™[Ëˆ[™™]šY]Ë[Û›H[\ÜÛÝ[Ü›ÝÝ‚‹H™[XZ[š[™Ë][YH[ˆ^XÝ]Y™Y›Ü™HÜ˜\]\ˆY\ˆXØÙ\[™ÈÌKYYˆ™]šY]Ë[Û›H™\Z\ˆÛÛ›ÛÈ›ÜˆMH^\[X™[XÚ\Ú[Ûˆ›ÝÜËBˆØØ[Y]šY[˜ÙH[™\Ë[\›˜]H™\ÚYYK\ÜÚ][Ûˆ™\]Y\ÝËH›ØÝ\ÙYˆ[\›˜]K\ÝXÝ\™HØØ[‹ÝšXÝ™[X\[ØØ[]Y]›ÜˆWØÜØNÌL˜ˆÛÛÙÞKYØ\]Y]X\›™Y\™]šY]˜[X[šY™\ÝÙ\]Y[˜ÙK\Ú[Z[\š]H˜Z[\™BˆÛÛ›ÛË™YÜ™\ÜÚ[Ûˆ\ÝË[™ØÝ[Y[][Û‹ˆ™^[ˆÚÝ[™\Z\ˆÜ‚ˆ^XÚ]HY™\ˆHXØÙ\YMÌH™]šY]ËYXÝ\™˜XÙH™Y›Ü™H›[™ÍLˆØØ[[™Ë‚‚‹HÕT•QÐUˆŒ‹LKLL•MNLŒŽV‚‹HS‘QÐUˆŒ‹LKLL•MŽNŒN‚‹HYX\Ý\™Y[\ÙY[YNˆLŽMÈZ[]\Â‹HØÝ[Y[][ÛˆÚXÚÙY[™\]YXÜ›ÜÜÈ‘PQQKØÜËÛX™[Ù˜XÝÜžK›YˆÛÜšËÜØÛÜK›YÛÜšËÚ[™Ù™‹›YÛÜšËÛX™[Ü™]šY]×ÍÌÛ›Ý\Ë›YˆÛÜšËÙ^\ÛX™[ÙXÚ\Ú[Û—ÛØØ[Ù]šY[˜ÙWÙØ\ÍÌÛ›Ý\Ë›YˆÛÜšËØ]ÜÜÜÜž[Ý˜[œÙ™\—Ù˜[Z[WÙ^[œÚ[Û—ÍÌÛ›Ý\Ë›Y[™Ý]\Âˆ[œ]È™Y›Ü™HÝ]\È™YÙ[™\˜][Û‹‚‹H›Ü›X[ØÚÙY[ˆœ›ÛHHXØÙ\YÌÝ]HY›ÝÜ›ÝÈHÛÝ[X›Bˆ™YÚ\ÝžKˆ][\[Y[YH^\\™]šY]ÙYUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[Bˆ^[œÚ[Ûˆ›ÜˆTËTÒÒKUYÜ˜\ÜÒÓ’Ë‘ËšÐKšÐ‹[™ÒT\ÂˆÛÛÙÞKÙ˜[Z[KX›Ý[™\žH]šY[˜ÙK‚‹HH^[œÚ[Ûˆ\Y˜XÝX\ÈŒÝ\ÜY™XXÝ[Û‹ÜÝXœÝ˜]HZ\ÛX]Ú[™\ÂˆXÜ›ÜÜÈ[š[™H\™Ù]˜[Z[Y\Ë™XÛÜ™È›Û‹]\™Ù]^\[È[™ˆ[œÝ\ÜYX\[™ÜË[™ÙY\ÈÛÝ[X›WÛX™[ØØ[™Y]WØÛÝ[L‚‹HHÌØ]H›ÝÈ\ÜÙ\ÈŒKÌŒHÚXÚÜÈ[™™\]Z\™\ÈÛÛ\]HZ\ÛX]Ú[[™Bˆ^ÜÛÛ\]H^\[X™[XÚ\Ú[Ûˆ^ÜÛÛ\]H^\[X™[ˆ™\Z\‹XØ[™Y]HÛÝ™\˜YÙKÛÛ\]H™\Z\‹YÝX\™˜Z[ÛÝ™\˜YÙKÛÛ\]BˆØØ[Y]šY[˜ÙHØ\]Y]Ù^ÜØØ[Y]šY[˜ÙH™\Z\ˆ™\ÛÛ][Û‹^XÚ]ˆ[\›˜]H™\ÚYYK\ÜÚ][Ûˆ™\]Y\ÝË™]šY]Ë[Û›H[\Ü\ØY™]H]šY[˜ÙK[™ˆUÜÜÜÜž[]˜[œÙ™\ˆ˜[Z[H^[œÚ[Ûˆ]šY[˜ÙHÚ]ÛÝ[X›HØ[™Y]\Ë‚ˆHØØ[[™Ë\]X[]H]Y][™˜]ÚÝ[[X\žH[ÛÈØ\œžHÜÙHØ]\Ë‚‹Hš[˜[™\šYšXØ][Ûˆ\ÜÙYˆÚ]Y™ˆKXÚXÚØœH[\XÝ™\ˆ™YÙ[™\˜]Yˆ”ÓÓˆ\Y˜XÝËUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØÚ]NN\ÝË[™ˆUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‚‹HŒ‹LKLŒHTÈ]\ÙKÛ›ËYÛÈÞ[\Ú\ÎˆØÜËÙ\×Ú]\š\ÝX×ÙÙ[ÛY]žWÛ›×ÙÛ×ÌŒŒLŒK›Yˆ[™\Y˜XÝËÝŒ×Ù\×Ú]\š\ÝX×ÙÙ[ÛY]žWÛ›×ÙÛ×ÙXÚ\Ú[Û—ÌŒŒLŒKšœÛÛ˜ˆ™XÛÜ™H™\ÙX\˜ÚY\™XÝÜˆXÚ\Ú[Ûˆ]]\š\ÝXÈÙ[ÛY]žK[Û›HTÂˆ›ÙXÝ[ÛˆXÝ]˜][Ûˆ\ÈH›ËYÛËˆÝ\œ™[TÈYÙ[ÈÚÝ[™H]\ÙY˜]\‚ˆ[ˆ[ÝÙYÈÙY\Z[[™È™]šY]Ë[Û›HXXÚ[™\žKˆ]\™HTÈÛÜšÈÚÝ[ˆ™\Ý\Û›H›ÜˆHX\›™YXÛÛ^[ÝHÛX[ˆXÝ]™K\Ý]HØ[™Y]BˆÙX\˜ÚH\›Z[˜[Ø[™Y]KXÛ\ÜÈXÚ\Ú[Û‹ÜˆHÙ][X‹Ù^\XYYXØ][Û‚ˆœšYÙKˆ›ÈX™[Ëš[™Ù\œš[Ë™\ÚÛË›ÙXÝ[ÛˆØÛÜ™\œË[\ÜËÜ‚ˆZYÜ˜][ÛˆÝ]HÚ[™ÙY‚‚‹HŒ‹LKLÈWØÜØNMØ^\X™[\Ý]H™]š\Ú[ÛŽˆ™[X™[Yœ›ÛBˆÙYYÙš[™Ù\œš[Ž™›]š[—ÙZY›ÙÙ[˜\ÙWÜ™YXÝ\ÙXÈÝ]ÛÙ—ÜØÛÜXY\‚ˆYXÚ[š\ÛK[ØÝ\È™]šY]ÈÛÛ˜ÛYYH›ÝÈ\È›]›ÙZ\›Ûˆš]šXÈÞYBˆ™YXÝ[Ûˆ]H›Û‹Z[YH™JRJQ™JRJHÙ[\‹Ú]“S’ˆXÝ[™È\È[XÝ›Û‚ˆÛ›Üˆ˜]\ˆ[ˆØ][]XÈ›]š[ˆYšYK]˜[œÙ™\ˆØÝ\ËˆØ[›ÛšXØ[X™[ˆÛÝ[™[XZ[œÈÌŽÈÙYYX™[È\™H›ÝÈŒÌH[™Ý][Ù‹\ØÛÜHX™[ÈÌKˆÙYBˆ\Y˜XÝËÝŒ×ÛWØÜØMM×ÛX™[Ü™]š\Ú[Û—ÍÌ—ÌŒŒLËšœÛÛ˜ˆ\Y˜XÝËÝŒ×ÛWØÜØMM×ÝØ]™LWÛY]šX×Ú[\XÝÍÌ—ÌŒŒLËšœÛÛ˜[™ˆÛÜšËÛWØÜØMM×ÛX™[Ü™]š\Ú[Û—ÌŒŒLË›Y‚‚‹HŒ‹LKLÈXÚÙ]HÈØ]™HH›ÛÝË]›ÝYÚØÚËYÝÛŽˆ™XYHÜšYÚ[˜[ˆØ]™HH™\Ý[Ø\™›ÝYÚHWØÜØNMØY]šXËZ[\XÝ\Y˜XÝHØ]™HBˆ™\Ý[XØ\™Y[™[KH›]š[ˆYšYK]˜[œÙ™\ˆÝX›X™[[[Ý[Û‹[™ˆ\Y˜XÝËÝŒ×ÜXÚÙ]WÝØ]™LWÛØÚÙÝÛ—ØY[™[WÍÌ—ÌŒŒLËšœÛÛ˜ˆØÚÙY]˜[ˆÙ[È\™NˆWØÜØNŒŒMØ[™WØÜØNÍØ\ÈK\Z\‹]™\šYšYY›ÛXÛÛ™›XÝÓÔÂˆ[˜ÚÜœÎÈWØÜØNŽ\È\X[›ÛXÛÛ™›XÝÚ]SKX˜\œ™[ˆ[˜ÚY[[\š[X\žKZ]Ø]™X]ÈWØÜØN\È™X\‹[Üœ[ˆÓÔËÜ›Ý]\‚ˆXœÝ[[ÛˆXYÛ›ÜÝXÎÈ[™WØÜØNMØ^ÛYYœ›ÛHš[X\žH›]š[ˆ[™ˆ™X\‹[Üœ[ˆš[X\žHY]šXÜÈY\ˆÓÔÈ™[X™[ˆWØÜØNÍL\È™]šY]ËX›ØÚÙYˆ[™[œØY™H›ÜˆØ]™HHØ[˜\žH\ÙH[[X™[Ý]H™\ÛÛ™\ÎÈWØÜØNØˆ™[XZ[œÈH˜[YY][ZY›Û\ÙHØ[˜\žKˆÙYBˆÛÜšËÜXÚÙ]WÝØ]™LWÙ›ÛÝÝ›ÝYÚÌŒŒLË›Y‚‚ˆÈÈ]]ÛX][Ûˆ[ˆØ][]XËYX\[]™\‹LËL‹Y›ÜØ\™\\Ú”ÕT•QÐUÕUÎˆŒ‹L‹L•NNŒŽŒLÖ‚”ÕT•QÐUÓÐÐSˆŒ‹L‹LˆMŒŽŒLÈÑ‘S‘QÐUÕUÎˆŒ‹L‹L•NNÎV‚‘S‘QÐUÓÐÐSˆŒ‹L‹LˆMÎHÑ‘STÑQÓRS•UTÎˆKB‚•Ü˜\Y™Y›Ü™HMHZ[]\È™XØ]\ÙHHYXÚ[šXØ[HØY™H]™\ˆØØ]Ü‹X›ØÚÙ\‚œÝ\™˜XÙH\ÈÛÛ\]H›Üˆ\È[ŽˆH™[XZ[š[™È›ÝÜÈ[™\]Z\™H^XÚ]š[X[‹ÜÛXÞKÜØÚY[YšXÈXÚ\Ú[ÛœÈ™Y›Ü™H[žHØØ]ÜˆÛÜKÛÛÜ™[˜]H™]Úœ™YXÝYYÙ[ÛY]žHØÛÜš[™ËX™[[\ÜÜˆÛÝ[Xš[]HXÝ[Û‹‚‚•Ú]Ú[™ÙY‚‚‹H™\ÛÛ™YHYÚ\Ý\š[Üš]HZÌØØZÌŽÜ]\ØY™HØØ]Ü‹XÛÜHÛ\ÜÎ‚ˆYYŒ×Ù˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWÛØØ]Ü—ØÛÜWÙXÚ\Ú[Û—ÛZ×ÛZŽØÝ\œ™[Ì—ÌŒŒŒ˜ˆÛÜYYH\›Ý™Y™]šY]Ë[Û›HÛÝ\˜ÙKYœ™YHØØ]ÜœÈ[Âˆ\Y˜XÝËÙ˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWØXÝ]™WÜÚ]WÛØØ]Üœ×ØÝ\œ™[Ì—ÌŒŒŒKØˆ™\Z\™YH™YHZÌØØ[™Y]HÜÚ][ÛœÈYØZ[œÝHØØ[Q‘ˆ[Ù[ˆ™\˜[ˆØØ]ÜˆØÚ[XH]Y]ÛÝ\˜ÙKYœ™YH™YXÝYYÙ[ÛY]žHX[šY™\ÝÜ™]šY]˜[ˆÛÝ\˜ÙKXÚXÚÈ™Y›YÚ˜[Z[K\[™[™XYÝ]ÛÝ\˜ÙKXÚXÚÈ]Y]YKØÛÛ\][Û‹ˆZ\ÜÚ[™Ë\š[X\žKXÚ[›™[]Y]YKÙXYÛ›ÜÚ\ËÛÝ[Xš[]H™Y›YÚ[™[\Üˆ›ØÚÙ\ˆØ]K‚‹HYY™]šY]Ë[Û›HÛÝ\˜ÙKXÚXÚÈXÚÙ]È›ÜˆZÌØ[™ZÌŽˆ›Ý\™BˆÛÛ\]YÛÝ\˜ÙHÚXÚÜÈÚ]›È˜[Z[H›Û[Ý[Û‹›È[\Ü™XY[™\ÜË[™›ÂˆX™[ØÛÝ[Xš[]HÚ[™ÙK‚‹HÛÛ\]YHYXØ]Y^\›˜[ÙÛXÛÜÚYWÜ[™[QÈ˜[Y]ÜŽ‚ˆŒ×Ù˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWÛØØ]Ü—ÙÛXÛÜÚYWÛ˜Y×Ý˜[Y]Ü—Ù^\›˜[ÙÛXÛÜÚYWÜ[™[ØÝ\œ™[Ì—ÌŒŒŒ˜ˆ™Z™XÝÈ]]ÛX]XÈQÈ™]\™Ù][™È™XØ]\ÙHÍQÈÚ]\È]™H™X\‹XÛÝ˜[[ˆÌKP\ÛˆÛÛXÝÈÛÛœÚ\Ý[Ú]ÛXØ[‹Ó‹[[šÙYÛXÛÜÞ[][ÛˆÛÛ^‚‹HYYZÌXØZÌÌ˜XØÙ\ÜÚ[Û‹Y\]Z]˜[[˜ÙHÜÚ][Ûˆ]Y]‚ˆŒ×Ù˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWÛØØ]Ü—ØXØÙ\ÜÚ[Û—Ù\]Z]˜[[˜ÙWÜÜÚ][Û—Ø]Y]ÛZWÛZÌ—ØÝ\œ™[Ì—ÌŒŒŒ˜‚ˆHÙ[XÝYœÈÝ[X\È™\™\Ù[]]™HXØÙ\ÜÚ[ÛœÈ[™˜]ÈØØ]Ü‚ˆÜÚ][ÛœÈ]™HÍˆ^XÝY™\ÚYYKXÛÙHX]Ú\È[ˆH™\]Y\ÝY[šT›ÝQ‘‚ˆ[Ù[ËÛÈ™\™\Ù[]]™H\]Z]˜[[˜ÙH[Û™H\È›ÝÝY™šXÚY[›ÜˆÛÜK‚‹HYYZÌ[\›˜]KXÛÛÜ™[˜]HØØ[XØXÚH™Y›YÚ‚ˆŒ×Ù˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWÛØØ]Ü—ÛZØ[\›˜]WØÛÛÜ™[˜]WÛØØ[ØØXÚWÜ™Y›YÚØÝ\œ™[Ì—ÌŒŒŒ˜‚ˆ]ÛÛ™š\›\ÈÍH[\›˜]HÒQœÈ
Ô’Ò˜Ô’ÒØÔÐ“ÔÑ”ÔÔX
H\™BˆØXÚYØØ[H[™›È™]ÚØ\È][\Y‚‹HYYMNML›Û›X™[[ØØ]Üˆ™X\ÚXš[]H]Y]‚ˆŒ×Ù˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWÛØØ]Ü—ÜMNMLÛ›Û›X™[ÛØØ]Ü—Ù™X\ÚXš[]WØ]Y]ØÝ\œ™[Ì—ÌŒŒŒ˜‚ˆHÙ[XÝYSSÛÛÜ™[˜]H\ÈØ]\ˆUU\ÈÛ›KQ‘ˆMNML\È›ÈUUBˆ[˜ÚÜ‹[™HØ[™Y]HÚYXØ\ˆ\È™\ÚYYHØØ]ÜœÎÈ[ˆ[\›˜]HÛÝ\˜ÙBˆ›ÝËØÛÛÜ™[˜]HÜˆ^XÚ]›Û›X™[Ý˜]YÞH™[XZ[œÈ™\]Z\™Y‚‹H\]YÛÜšËÙ˜[Z[WÜ[™[ÜÛÝ\˜ÙWÙœ™YWÛØØ]Ü—Ø›ØÚÙ\—Ü™\ÛÛ][Û—ÜÝ]\×ØÝ\œ™[Ì—ÌŒŒŒK›Yˆ[™H[X[ˆXÚ\Ú[ÛˆX]š^Ú[\Ü›ØÚÙ\ˆ™\ÜÈÛÈ[š]™H[œ™\ÛÛ™Yˆ›ÝÜÈÚ[ÈÛÛ˜Ü™]H™[XZ[š[™ÈXÚ\Ú[ÛœËˆ[\Ü™]šY]È™[XZ[œÈ›ØÚÙY‚ˆÌŒˆ›ÝÜÈ[\Ü\™XYKÛÝ[X›HX™[È]]Üš^™Y[™Hš[Üš]H›ÝÜÂˆ™\]Z\™H[X[‹ÜÛXÞHXÚ\Ú[ÛœË‚‹H\]YÓKÙÙ[™\˜]ÜˆÙÚXÈ›ÜˆHZÌØØZÌŽØØ]Ü‹XÛÜHXÚ\Ú[Ûˆ[™ˆ™Yœ™\ÚY™YÜ™\ÜÚ[ÛˆÛÝ™\˜YÙH›ÜˆH™]È›ØÚÙ\ˆ\Y˜XÝÈ[™Ø]HÛÜ™[™Ë‚‚‘ÝX\™˜Z[Î‚‚‹H›ÈX™[Ë™YÚ\ÝšY\ËÛÛÙÚY\Ë[\ÜË›ÙXÝ[Ûˆ™\ÚÛË[Ù[ˆÙZYÚË™]ÛÜšÈÛÝ\˜ÙH™]Ú\ËÜˆÛÛÜ™[˜]HÝÛ›ØYÈÚ[™ÙY‚‹H›È[Ý]˜Z[š[™ËÝ[š[™ÈØ\È\™›Ü›YYˆ™]È˜[Z[K\[™[\Y˜XÝÈ\™Bˆ™]šY]Ë[Û›H[™›Û‹XÛÝ[X›K‚‚•™\šYšXØ][ÛŽ‚‚‹H]Ûˆ[HÛÛ\[X[\HÜ˜ËØØ][]X×ÙX\Û›ÜÝ\—Û™^Û]™\œËœHÜ˜ËØØ][]X×ÙX\ØÛKœH\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œX‹H›ØÝ\ÙYØØ]Ü‹ÙØ]H™YÜ™\ÜÚ[ÛˆÛXÙNˆŒH\ÜÙYLŒˆ\Ù[XÝY‚‹HUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆÌˆÝ\˜]YX™[Ë‚‹H]Ûˆ[HœÛÛ‹ÛÛÛˆH™]È”ÓÓˆ\Y˜XÝË‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÛ›ÜÝ\—Û™^Û]™\œËœH\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œH\ÝËÝ\ÝØÛKœH\XˆÍ\ÜÙYHÝX\ÝË‚‹H[UÓ”U\Ü˜È]Ûˆ[H]\Ý\XˆLŒÍH\ÜÙYLÝX\ÝËÛ™Bˆ^\Ý[™ÈÚÛX\›‹ÔØÚTHØ\›š[™Ë‚‹H[UÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆLNL\ÜÙYØ[YBˆ^\Ý[™ÈÚÛX\›‹ÔØÚTHØ\›š[™Ë‚‹HUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‹HÝ\œ™[YØÜÈ\Y˜XÝ\™Y™\™[˜ÙHÚXÚÎˆMMÈÚXÚÙYZ\ÜÚ[™Ë‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÙØ×Ü™Y™\™[˜ÙWØÚXÚËœH\Xˆˆ\ÜÙY‚‹H™\Ë]ÚYH”ÓÓˆ\œÙHÝÙY\ˆÌÌÌH”ÓÓˆš[\È\œÙY‚‹HÚ]Y™ˆKXÚXÚØ\ÜÙY‚‚‘^XÝ™^XÝ[ÛŽ‚‚‘È›Ý™\[ˆØØ]Üˆ\ØÛÝ™\žKˆÝ\Ú]HÜ™[XZ[š[™ÈXÚ\Ú[ÛˆÛ\ÜÎ‚™›ÜˆZÌXØZÌÌ˜›ÝšYHX]Ú[™Èœ›Þ™[ˆÛÛÜ™[˜]\ÈÜˆ^XÚ]H\›Ý™B˜[YÛ›Y[Ü™[X\YØØ]ÜœÈ™Y›Ü™H[žH˜]È™\™\Ù[]]™KXÛÛÜ™[˜]HÛÜKˆ[‚œ™\[ˆØØ]ÜˆØÚ[XKÜØÛÜš[™ÈÛ›HYˆ\›Ý™YˆHÝ\ˆ™[XZ[š[™ÈXÚ\Ú[ÛœÈ\™B˜^\›˜[ÙÛXÛÜÚYWÜ[™[ÝXœÝ˜]KXÛÛ\^Üˆ^\X\›Ý™Y›Û‹YÛXØ[‚›ØØ]Ü‹ZÌ[\›˜]KXÛÛÜ™[˜]H™]Ú\›Ý˜[Ü™Z™XÝ[Û‹[™MNML˜[\›˜]HÛÝ\˜ÙHÜˆ^XÚ]›Û›X™[ØØ]ÜˆÝ˜]YÞK‚‚ˆÈÈ]]ÛX][Ûˆ[ŽˆØ][]XËYX\[]™\‹LËL‹Y›ÜØ\™\\ÚŒ‹L‹L‚”ÕT•QÐUÕUÎˆŒ‹L‹LLÎŒŽŒÌ–‚”ÕT•QÐUÓÐÐSˆŒ‹L‹LŒŽŒÌ‹LL‘S‘QÐUÕUÎˆŒ‹L‹LLÎLŽ‚‘S‘QÐUÓÐÐSˆŒ‹L‹LLŽLLÑ‘STÑQÓRS•UTÎˆLŒB‚”ØÛÜNˆ]™\ˆÈÛ›KˆÝ\[™Èœ›ÛHHÝ\œ™[^XÝ™^XÝ[ÛˆX›Ý™Nˆ™\ÛÛ™B›Üˆ™XÚ\Ù[H›ØÚÈH™[XZ[š[™ÈÛÛ™›Ý[™Y\ØY™HØØ]Ü‹Û›Ý™[HØ]H]šY[˜ÙB™XÚ\Ú[ÛœÈÚ]Ý]Ú[™Ú[™ÈX™[Ë™YÚ\ÝšY\ËÛÛÙÚY\Ë[\ÜË›ÙXÝ[Û‚™\ÚÛË[Ù[ÙZYÚËÜˆ[Ý]Ü]Ë‚‚•Ú]Ú[™ÙY‚‚‹HYYHÍN™YXÝ[Ûˆ\Ü]ÚXÚÙ]‚ˆ\Y˜XÝËÝŒ×Ù›ÛØ]YÛY[YÜÍNÜ™YXÝ[Û—Ù\Ü]ÚÜXÚÙ]ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆ[™ˆÛÜšËÙ›ÛØ]YÛY[YÜÍNÜ™YXÝ[Û—Ù\Ü]ÚÜXÚÙ]ØÝ\œ™[Ì—ÌŒŒŒ›Y‚ˆHXÚÙ]ÛÛ\ÜÙ\ÈHœ›Þ™[ˆÌMKXXHTÕK›Ý™[˜[˜ÙH[\]KX›XÈ[™ˆØØ[›ÝšY\ˆ›Ø™\Ë[™XØÙ\[˜ÙH™Y›YÚˆ]\È™XYH›Üˆ[ˆ^\›˜[ˆ\›Ý™Y›ÝšY\ˆ[ˆ]›ØÚÙY›ÝÎˆÍˆ›ÝšY\ˆ›Ý]\È™]\›ˆHÛÛÜ™[˜]KˆØ[™Y]HÛÛÜ™[˜]Hš[\È^\ÝØ[™Y]H›Ý™[˜[˜ÙHš[\È^\Ý[™ˆÈXØÙ\[˜ÙHÚXÚÜÈÝ[˜Z[ˆ›ÈÛÛÜ™[˜]HØ\ÈÝYÙYÜˆØÛÜ™Y‚‹HYYYÚXÛÙ˜XÝÜˆ˜Z[‹ØØ[ÓÔÈXÜ]Z\Ú][Ûˆ\Ü]Ú‚ˆ\Y˜XÝËÝŒ×Ù›ÛØ]YÛY[YØÛÛ™›Ý[™YÜ›ÞWÚYÚØÛÙ˜XÝÜ—ØXÜ]Z\Ú][Û—Ù\Ü]ÚÜXÚÙ]ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆ[™™\Üˆ]œ™Y^™\ÈMˆ[™š[Y[ZÙHÛÝÈÚ]XØÙ\[˜ÙHÚXÚÜÈ›Ü‚ˆ›Û‹Z[Ý]˜Z[‹ØØ[ÓÔÈ›ÛKÛÝ\˜ÙKYœ™YHYÚXÛÙ˜XÝÜˆY[X™\œÚ\ˆ\Þ[Y[]˜[Y™YXÝYÛÛÜ™[˜]KÜ›Ý™[˜[˜ÙK›È^\š[Y[[TˆÚÜÝ]ˆ[™[˜Ú[™ÙY™\ÚÛMMXˆHMˆ^\Ý[™È™X\ˆZ\ÜÙ\È™[XZ[‚ˆ›Û‹XÛÝ[X›H[™›ÈØ[™Y]H›ÝÈ\È™YÚ\Ý\™YÜˆØÛÜ™Y‚‹HYYØ[YKY˜[Z[HÝXÝ\˜[˜Z[‹ØØ[ÓÔÈXÜ]Z\Ú][Ûˆ\Ü]Ú‚ˆ\Y˜XÝËÝŒ×Ù›ÛØ]YÛY[YØÛÛ™›Ý[™YÜ›ÞWÜØ[YWÙ˜[Z[WÜÝXÝ\˜[ØXÜ]Z\Ú][Û—Ù\Ü]ÚÜXÚÙ]ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆ[™™\Üˆ]œ™Y^™\ÈMÌ[™š[Y[ZÙHÛÝÈÚ]HØ[YH\Þ[Y[[™ˆÝX\™˜Z[ÚXÚÜËˆH˜XÚÙÜ›Ý[™ÝXÝ\˜[›ÝÜÈ™[XZ[ˆ›Û‹XÛÝ[X›H[™ˆ›ÈØ[™Y]H›ÝÈ\È™YÚ\Ý\™YÜˆØÛÜ™Y‚‹HYYÛÛXš[™Y\Ü]Ú™XY[™\ÜÈÝ[[X\žN‚ˆ\Y˜XÝËÝŒ×Ù›ÛØ]YÛY[YÛ]™\Œ×Ù\Ü]ÚÜ™XY[™\Ü×ÜÝ[[X\žWØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆ[™™\Üˆš[˜[ÛÝ[ÎˆËÌÈ\Ü]ÚXÚÙ]È™XYH›Üˆ^\›˜[XÝ[Ûˆ]ˆ›ØÚÙYÈNˆ˜Z[‹ØØ[ÓÔÈ[ZÙHÛÝÈ™\]Z\™YÈÛÝÈš[YÈÛÝÂˆ™XYHÈØÛÜ™NÈÝX\™˜Z[š[Û][ÛœÎÈš^Y]™\ÚÛ]Y]›Ý™XYK‚‹H™YÙ[™\˜]YH]™\ˆÈ›ØÚÙ\‹\XÚÙ]ÝX\™˜Z[]Y]Z[š[][H™^Y^\š[Y[ˆ]Y]YK[™]Y]YKÝ[\]HÝX\™˜Z[]Y]ˆHš[˜[›ØÚÙ\ˆ]Y]ÚXÚÜÈÂˆ\Y˜XÝÈÚ]š[Û][ÛœÎÈHš[˜[]Y]YKÝ[\]H]Y]ÚXÚÜÈH\Y˜XÝÂˆÚ]š[Û][ÛœË‚‹HYYZ[\ˆ\ÝËÓH™YÚ\Ý˜][ÛœËÝ\œ™[X\Y˜XÝ™YÜ™\ÜÚ[ÛœË[™BˆÛÝ\˜ÙKX\Y˜XÝÚXÚÜÝ[H™YÜ™\ÜÚ[ÛˆÛÈÝ[HÛÝ\˜ÙH\Ú\È[ˆH™]È\Ü]ÚˆXÚÙ]È\™HØ]YÚ‚‚‘ÝX\™˜Z[Î‚‚‹HÛÜšÙYÛ›HÛˆ]™\ˆË‚‹H›ÈX™[Ë™YÚ\ÝšY\ËÛÛÙÚY\Ë[\ÜË›ÙXÝ[Ûˆ™\ÚÛË[Ý]ˆÜ]Ë[Ù[ÙZYÚËÜˆ™\ÚÛ˜[Y\ÈÚ[™ÙY‚‹H›È[Ý]KPÔÐH›ÝÜÈÙ\™H\ÙY›Üˆ˜Z[š[™ÈÜˆ™\ÚÛ[š[™Ë‚‹H›ÈYXÚ[š\ÛH^PËÔšXHQËX™[ËÛÝ\˜ÙHQË\™Ù]˜[Y\ËÜ‚ˆ^\š[Y[[ˆY]Y]HÙ\™H\ÙY\È™YXÝ]™H™X]\™\Ë‚‹H›È›ÝÈØ\È™YÚ\Ý\™YØÛÜ™Y[\ÜY›Û[ÝYÜˆ\ÙY›ÜˆHš^Y]™\ÚÛˆ]Y]™\[‹‚‹H›ÈÛÛÜ™[˜]HØ\ÈÝYÙYÝÛ›ØYYÜˆ[\ÜYˆ^\š[Y[[ÜX›XÈ‚ˆ]šY[˜ÙH™[XZ[œÈ›ØÚÙ\ˆ]šY[˜ÙHÛ›K‚‚•™\šYšXØ][ÛŽ‚‚‹H›ØÝ\ÙYZ[\ˆÛXÙN‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÛ›ÜÝ\—Û™^Û]™\œËœHZÈ	Ù\Ü]ÚÜ™XY[™\Ü×ÜÝ[[X\žHÜˆXÜ]Z\Ú][Û—Ù\Ü]ÚÜˆÍNÜ™YXÝ[Û—Ù\Ü]Ú	È\X‚ˆ\ÜÙYMÍÈ\Ù[XÝY‚‹H›ØÝ\ÙY\Y˜XÝ™YÜ™\ÜÚ[ÛˆY\ˆš[˜[™YÙ[™\˜][ÛŽ‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œHZÈ	Ù\Ü]ÚÜ™XY[™\Ü×ÜÝ[[X\žHÜˆ]Y]YWØ[™Ý[\]WÙÝX\™˜Z[ÜˆXÜ]Z\Ú][Û—Ù\Ü]ÚÜˆÍNÜ™YXÝ[Û—Ù\Ü]ÚÜˆ\Ü]ÚÜÛÝ\˜ÙWØ\Y˜XÝÚ\Ú\ÉÈ\X‚ˆˆ\ÜÙYŒŽ\Ù[XÝYÝX\ÝÈ\ÜÙY‚‹H[ÝXÚY]\ÝÛXÙN‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÛ›ÜÝ\—Û™^Û]™\œËœH\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œH\ÝËÝ\ÝØÛKœH\X‚ˆLÍ\ÜÙYMŽHÝX\ÝÈ\ÜÙY‚‹Hš[˜[[]\Ý‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\XˆMˆ\ÜÙYNÝX\ÝÈ\ÜÙYÚ]ˆH^\Ý[™ÈÚÛX\›‹ÔØÚTH\™XØ][ÛˆØ\›š[™Ë‚‹Hš[˜[[[š]\Ý\ØÛÝ™\žN‚ˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆLÍŒH\ÝÈ\ÜÙYÚ]ˆHØ[YH^\Ý[™ÈÚÛX\›‹ÔØÚTH\™XØ][ÛˆØ\›š[™Ë‚‹HUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆLˆÛÝ\˜ÙH™XÛÜ™ËˆYXÚ[š\ÛHš[™Ù\œš[ËMHÛÛÙÞH˜[Z[Y\ËÌˆX™[Ë‚‹HUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÜ›ÙÜ™\ÜËœH\XˆÈ\ÜÙY‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÙØ×Ü™Y™\™[˜ÙWØÚXÚËœH\Xˆˆ\ÜÙY‚‹HÛÝ\˜ÙKX\Y˜XÝ\ÚÝÙY\Ý™\ˆH™]È\Ü]ÚØ]Y]\Y˜XÝÎ‚ˆNÛÝ\˜ÙH\Ú\ÈÚXÚÙYÝ[K‚‹H™\Ë]ÚYH”ÓÓˆ\œÙNˆÍLŽH”ÓÓˆš[\ÈÚXÚÙY‚‹HÚ]Y™ˆKXÚXÚØ‚‹H\ÚÈÝX\™˜Z[ˆŒÚPˆ]˜Z[X›K‚‚ÛÛ[Z]Ü\ÚÝ]\Î‚‚‹H[™Ù™‹ÜÝ]\ËÛY[[ÜžH\™H™Z[™È\]YY\ˆ˜[Y][Û‹ˆÛÛ[Z]\ÚˆPQOHÜšYÚ[‹ÛXZ[˜™\šYšXØ][Û‹[™ØÚÈ™[X\ÙH\™HH™[XZ[š[™ÂˆYXÚ[šXØ[Ü˜\Ý\ÈY\ˆ\È[™Ù™ˆY]‚‚‘^XÝ™^XÝ[ÛŽ‚‚‘È›Ý™\[ˆÜˆ™][™H™\ÚÛMMXY]ˆH™^]™\ˆÈXÝ[Ûˆ\Î‚‚ŒKˆ[‹Ü›Ýš\Ú[Ûˆ^XÝHÛ™H\›Ý™Y[[[™Ý™YXÝÜ‹Ü›ÝšY\ˆ\Ú[™ÂˆÛÜšËÙ›ÛØ]YÛY[YÜÍNÙ[Û[™ÝÜ™YXÝ[Û—Ú[œ]ØÝ\œ™[Ì—ÌŒŒŒ™˜\ÝX‚Œ‹ˆÜš]HH™]\›™YÛÛÜ™[˜]HÈH™Y™\œ™YÍNÛÛÜ™[˜]H][™ˆš[ˆ\Y˜XÝËÝŒ×Ù›ÛØ]YÛY[YÜÍNÜ™YXÝ[Û—Ü›Ý™[˜[˜ÙWÙš[YØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆÚ]›ÝšY\‹Û[Ù[Ý™\œÚ[Û‹Ü]ØÚXÚÜÝ[KÙ\]Y[˜ÙHÒKÛ[™ÝK\ÜÚ][Û‚ˆM[™[™Ë[™^XÚ]›ËY^\š[Y[[\ÚÜÝ]]šY[˜ÙK‚ŒËˆ™\[‚ˆZ[Y›ÛX]YÛY[Y\ÍN\™YXÝ[Û‹XXØÙ\[˜ÙK\™Y›YÚÚ]BˆØ[™Y]HÛÛÜ™[˜]H[™š[Y›Ý™[˜[˜ÙKˆÝYÙH[™ØÛÜ™HÍNÛ›HY‚ˆ]™\žHXØÙ\[˜ÙHÚXÚÈ\ÜÙ\Ë‚ˆY\ˆÍN\ÜÙ\Ëš[HMˆÛÝ\˜ÙKYœ™YHYÚXÛÙ˜XÝÜˆ˜Z[‹ØØ[ÓÔÂˆ[ZÙHÛÝÎÈ[ˆ[™HH\™Ù\ˆMÌ\›ÝÈØ[YKY˜[Z[HÝXÝ\˜[[ZÙK‚ˆØÛÜ™HÛ›HXØÙ\Y›ÝÜÈ][˜Ú[™ÙY™\ÚÛMMX[™Û›HY\‚ˆ[ZÙHÚXÚÜÈ\ÜË‚‚ˆÈÈ]]ÛX][Û‹Ú[™Ù™ˆ\]Nˆ˜[Z[HYZ\ÜÚ[Ûˆ\[™[˜ÞH™YXÝ[ÛˆŒ‹L‹L‚”ØÛÜNˆ™YXÙHš]™ZÈ\[™[˜ÞH[ˆH\™Ù]Y˜[Z[K[X™[^[œÚ[Ûˆ]Ú]Ý][\Ü[™ÈX™[ËÚ[™Ú[™È™YÚ\ÝšY\ËÛÛÛÙÚY\ËÜˆ›Û[Ý[™È[žH›ÝÂÈÛÝ[X›HÝ]\Ë‚‚•Ú]Ú[™ÙY‚‚‹HYY˜[Z[WØYZ\ÜÚ[Û—Ø\˜Ú]XÝ\™WÙY˜][ÝŒX›ÜÜØ[ÈÈH˜[Z[BˆX™[YZ\ÜÚ[Ûˆ\[[™Kˆ[™[™È˜[Z[KYXÚ\Ú[Ûˆ›ÝÜÈ›ÝÈÙ][‚ˆ\˜Ú]XÝ\™KY\š]™Y›Û‹XÛÝ[[™ÈY˜][Ú[ˆH^\Ý[™ÈÚ[›™[ÈÝ\Üˆ™Z™XÝÓÓÔÈ™\Ù\˜][ÛˆÜˆ™]šY]Ë[Û›H™\Ù\˜][Û‹‚‹H™YÙ[™\˜]Y‚ˆ\Y˜XÝËÝŒ×Ù˜[Z[WÛX™[ØYZ\ÜÚ[Û—Ü\[[™WØÝ\œ™[Ì—ÌŒŒŒËšœÛÛ˜ˆ\Y˜XÝËÝŒ×Ù˜[Z[WÛX™[ØYZ\ÜÚ[Û—Ù^\ÙXÚ\Ú[Û—Ý[\]WØÝ\œ™[Ì—ÌŒŒŒËšœÛÛ˜ˆ[™ÛÜšËÙ˜[Z[WÛX™[ØYZ\ÜÚ[Û—Ü\[[™WØÝ\œ™[Ì—ÌŒŒŒË›Y‚‹HÝ\œ™[™\Ý[›ÜˆHˆ™]š[Ý\ÛH[X[‹X›ØÚÙY˜[Z[KYXÚ\Ú[Ûˆ›ÝÜÎ‚ˆ‹Íˆ]™H\˜Ú]XÝ\™HY˜][›Û‹XÛÝ[[™È›ÜÜØ[È[™ˆ[X[—Ù˜[Z[WÙXÚ\Ú[Û—Ü›ÝÜ×ØY\—Ø\˜Ú]XÝ\™WÙY˜][ÈH‚‹H›ÜÜÙYY˜][Î‚ˆWØÜØNŒLWØÜØNŒÌWØÜØNŒÌX[™WØÜØNŒNLXO‚ˆ™Z™XÝÙ˜[Z[WÜ[™[Ú[\ÜØØ[™Y]XÂˆWØÜØN[™WØÜØNŽMÌØO‚ˆÙY\Ù˜[Z[WÜ[™[Ü™]šY]×ÛÛ›WÜ™\]Z\™WÛ[Ü™WÙ]šY[˜ÙX‚‹HÛÝ[X›KÚ[\ÜØY™]H\È[˜Ú[™ÙYˆ\˜Ú]XÝ\™HY˜][ÈX^H›Ý]H›ÝÜÂˆ]Ø^Hœ›ÛH[\ÜÜˆÙY\[H™]šY]Ë[Û›K]X^H›ÝXØÙ\H˜[Z[K\[™[ˆ[\ÜØ[™Y]K›Û[ÝHHÛÝ[X›HX™[[\ˆÜ]ËÜˆÚ[™ÙBˆ™\ÚÛÈÚ]Ý][X[ˆ™]šY]Ë‚‚’ÝÈYÙ[ÈÚÝ[™XY\Î‚‚‹HÈ›Ý\ÚÈš]™ZÈÈYYXØ]H\ÙHˆ›ÝÜÈ\ÝÈ™\Ù\™H›Û‹XÛÝ[[™ÂˆÚYÛ˜[ˆ\ÙHH\˜Ú]XÝ\™H›ÜÜØ[^Y\ˆ[›\ÜÈHÛØ[\ÈÈÝ™\œšYHBˆ›ÝÈ[ÈÛÝ[X›H›Û[Ý[Û‹‚‹HH™[XZ[š[™È˜[Z[K\[™[ÛÜšÈ\ÈØØ]Ü‹ØÛÛÜ™[˜]HXÜ]Z\Ú][Ûˆ[™YBˆÛÝ[X›H˜[Z[H^[œÚ[Û‹›Ý™\X]Y›ØÚÙ\‹\XÚÙ]›ÜÙHÛˆ\ÙHØ[YBˆÚ^›ÝÜË‚‚•™\šYšXØ][ÛŽ‚‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÙ˜[Z[WÛX™[ØYZ\ÜÚ[Û‹œH\X‚ˆ\ÜÙYHÝX\ÝÈ\ÜÙY‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝØÛKœH\X‚ˆŒˆ\ÜÙYMŒÝX\ÝÈ\ÜÙY‚‹HUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆLˆÛÝ\˜ÙH™XÛÜ™ËˆYXÚ[š\ÛHš[™Ù\œš[ËMHÛÛÙÞH˜[Z[Y\ËÌˆX™[Ë‚‹H”ÓÓˆ\œÙH›ÜˆH™YÙ[™\˜]Y˜[Z[KXYZ\ÜÚ[Ûˆ\Y˜XÝÈ\ÜÙY‚‹HÚ]Y™ˆKXÚXÚØ\ÜÙY‚‚ˆÈÈ]]ÛX][Û‹Ú[™Ù™ˆ\]Nˆ\˜Ú]XÝ\™HY˜][ÈX]\šX[^™YŒ‹L‹L‚”ØÛÜNˆÛÛ™\\˜Ú]XÝ\™K\›ÜÜÙY›Û‹XÛÝ[[™È˜[Z[KXYZ\ÜÚ[ÛˆY˜][È[ÂH^\Ý[™È™]šY]ÙYYXÚ\Ú[Ûˆ\XØ][Ûˆ]ÛÈYÙ[ÈÝÜ™X][™ÈBœØ[YHÚ^›ÝÜÈ\È]™H[X[ˆ›ØÚÙ\œË‚‚•Ú]Ú[™ÙY‚‚‹HYYÓN‚ˆUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛHX]\šX[^™KY˜[Z[K[X™[XYZ\ÜÚ[Û‹X\˜Ú]XÝ\™KYY˜][Ø‚‹HYY\Y˜XÝ‚ˆ\Y˜XÝËÝŒ×Ù˜[Z[WÛX™[ØYZ\ÜÚ[Û—Ø\˜Ú]XÝ\™WÙY˜][ÙXÚ\Ú[Ûœ×ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆ[™™\Ü‚ˆÛÜšËÙ˜[Z[WÛX™[ØYZ\ÜÚ[Û—Ø\˜Ú]XÝ\™WÙY˜][ÙXÚ\Ú[Ûœ×ØÝ\œ™[Ì—ÌŒŒŒ›Y‚‹HX]\šX[^™Yˆ›Û‹XÛÝ[[™ÈXÚ\Ú[ÛœÈœ›ÛBˆ˜[Z[WØYZ\ÜÚ[Û—Ø\˜Ú]XÝ\™WÙY˜][ÝŒX‚ˆ™Z™XÝÙ˜[Z[WÜ[™[Ú[\ÜØØ[™Y]X[™ˆˆÙY\Ù˜[Z[WÜ[™[Ü™]šY]×ÛÛ›WÜ™\]Z\™WÛ[Ü™WÙ]šY[˜ÙX‚‹H\YYHX]\šX[^™YXÚ\Ú[ÛœÈ›ÝYÚH^\Ý[™È^\YXÚ\Ú[Û‚ˆ\XØ][ÛŽ‚ˆ\Y˜XÝËÝŒ×Ù›ÛØ]YÛY[YÙ˜[Z[WÜ[™[Ù^\Ú[\ÜÙXÚ\Ú[Û—Ø\XØ][Û—ØÝ\œ™[Ì—ÌŒŒŒËšœÛÛ˜‚‹H™YÙ[™\˜]YHXØÙ\Y[\Ü™]šY]ËX™[Y˜XÝÜžH™XY[™\ÜË[™˜[Z[BˆYZ\ÜÚ[Ûˆ\[[™Kˆš[˜[YZ\ÜÚ[Û‹\Ý]HÛÝ[È›ÝÈ]™Bˆ›ØÚÙYÙ˜[Z[WÙXÚ\Ú[ÛˆH™Z™XÝÜ™\Ù\™WÜÚYÛ˜[H[™ˆ™]šY]×ÛÛ›WÙ]šY[˜ÙHH˜‚‚‘ÝX\™˜Z[Î‚‚‹H›ÈXØÙ\Ú[\ÜØÛÝ[X›H›Û[Ý[ÛˆXÚ\Ú[ÛœÈÙ\™HX]\šX[^™Y‚‹H›ÈX™[Ë™YÚ\ÝšY\ËÛÛÙÚY\Ë[\ÜË›ÙXÝ[Ûˆ™\ÚÛË[Ý]ˆÜ]ËÜˆ[Ù[ÙZYÚÈÚ[™ÙY‚‹HHX]\šX[^™\ˆ™Y\Ù\È\˜Ú]XÝ\™HY˜][È]›ÜÜÙBˆ^XÚ]ØXØÙ\Ù˜[Z[WÜ[™[Ú[\ÜØØ[™Y]X‚‚Ý\œ™[™^XÝ[ÛŽ‚‚‹HH˜[Z[KYXÚ\Ú[Ûˆ›ØÚÙ\ˆ\ÈÛX\™YˆÈ›Ý\ÚÈš]™ZÈÈ™]šY]ÂˆWØÜØNŒLWØÜØNŒÌWØÜØNŒÌXWØÜØNŒNLXWØÜØNÜ‚ˆWØÜØNŽMÌØYØZ[ˆ[›\ÜÈHÛØ[\ÈÈÝ™\œšYH[H[ÈÛÝ[X›Bˆ›Û[Ý[Û‹‚‹HH™[XZ[š[™ÈÝ\œ™[Y˜[Z[H›ØÚÙ\œÈ\™HÛÛ˜Ü™]HØØ]Ü‹ØÛÛÜ™[˜]Bˆ›ØÚÙ\œÎˆZÌXZÌÌ˜^\›˜[ÙÛXÛÜÚYWÜ[™[ZÌ[™ˆÙXÛÛ™\žWÜ›Ø™NŽ˜ÛØ˜[[Z[—Ü˜YXØ[Ü™X\œ˜[™Ù[Y[‚‚ˆÈÈ]]ÛX][Ûˆ[Žˆ\™Ù]Y^[œÚ[Ûˆ˜XÝÜžH
Œ‹L‹LŒŽVŠB‹HÕT•QÐUÕUÎˆŒ‹L‹LŒŽV‚‹HÕT•QÐUÓÐÐSˆÝ[ˆ[ˆÈŒÎŒŽHÑŒ‚‹HS‘QÐUÕUÎˆŒ‹L‹LMÎŒŒ‚‹HS‘QÐUÓÐÐSˆÝ[ˆ[ˆÈŒÎMÎŒŒÑŒ‚‹HSTÑQÓRS•UTÎˆLNÂ‹H]]ÛX][ÛˆQˆØ][]XËYX\Y˜[Z[K[X™[XYZ\ÜÚ[Û‹\\[[™B‹HÝ]\ÎˆÜ˜\ÛÛ\]NÈÛÛ[Z]Ü\ÚÜÞ[˜ËÛØÚË\™[X\ÙH\™HH™[XZ[š[™ÂˆYXÚ[šXØ[Ý\ÈY\ˆ\È[™Ù™ˆY]‚‚”ØÛÜN‚‚‹HZ[Hš\œÝ™]\ØX›H\™Ù]Y^[œÚ[Ûˆ˜XÝÜžHÝ]]›Üˆ]™\œÙH]\ÂˆÜ›ÝÝœ›ÛHÝ\œ™[ØØ[Ù]HÛÝ\˜Ù\ËˆH˜]Ú]˜[X]\ÈÌÈ›Û‹Z[\Ü[™ÂˆØ[™Y]\ÈXÜ›ÜÜÈLˆ\™Ù]Y˜[Z[H^\Èœ›ÛHÌKPÔÐH^[œÚ[Ûˆ›ÝÜÈ\ÂˆÍÎH[šT›ÝÔÝÚ\ÜËT›Ý^\›˜[Yœ™Y^™H›ÝÜË‚‹H^ÛYYH[™XYHX]\šX[^™Y\˜Ú]XÝ\™KYY˜][›ÝÜÂˆWØÜØNŒLWØÜØNŒÌWØÜØNŒÌXWØÜØNŒNLXWØÜØN[™ˆWØÜØNŽMÌØ‚‹HYYHXXÚ[™K\™XYX›Hš\œÝXXÝ[ÛˆØÜ™Y[ˆ[œ]›ÜˆHLˆ^\›˜[ˆ™]šY]Ë[Û›H›ÝÜÈ]ÚÝ[[\ˆÛÝ\˜ÙKYœ™YH\XØ]KÝXÝ\˜[[šT™Y‹ˆ™]šY]Ë[™X™[Y˜XÝÜžHØ]\È™^‚‚\Y˜XÝËÜ™\ÜÈ›ÙXÙY‚‚‹H\Y˜XÝËÝŒ×Ý\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžWØ˜]ÚØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜ˆ
Œ×Ý\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžWØ˜]ÚØÝ\œ™[Ì—ÌŒŒŒ
NˆÌÈØ[™Y]\ËˆLˆ˜[Z[H^\Ë^XÝ[Û™K\Ý]H]Y]ÛÝ\˜ÙH\Ú\ËYZ\ÜÚ[ÛˆÝ]\Ëˆš\œÝXXÝ[ÛˆØÜ™Y[ˆ[œ][™ÛÝ[X›KÚ[\Ü\™XYH›ÝÜË‚‹HÛÜšËÝ\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžWØ˜]ÚØÝ\œ™[Ì—ÌŒŒŒ›YˆX\šÙÝÛ‚ˆ™\ÜÚ]YZ\ÜÚ[ÛˆÛÝ[Ë˜[Z[H^\ËÛÛÜ™[˜]HÝ]\Ë›ÜÜÙYY\œËˆÛÝ\˜ÙH\Ú\ËXÝ[Ûˆ˜[˜Ú\Ëš\œÝXXÝ[Ûˆ™]šY]Ë›ØÚÙ\œË[™™^ˆ˜]Ú™XÛÛ[Y[™][ÛœË‚‚’Ù^HÛÝ[Î‚‚‹HYZ\ÜÚ[ÛˆÝ]\ÎˆŒˆ™]šY]×ÛÛ›WÙ]šY[˜ÙXMÎXÜ]Z\Ú][Û—Û™YYYˆLÌ›ØÚÙYÙ˜[Z[WÙXÚ\Ú[Û˜Ìˆ›ØÚÙYÛØØ]Ü˜Nˆ™Z™XÝÜ™\Ù\™WÜÚYÛ˜[È›ØÚÙYØÛÛÜ™[˜]XˆÛÝ[X›WØØ[™Y]X[™ÛÜ×Ú\™Û™YØ]]™X‚‹HÛÝ\˜ÙH˜[Y\ÜXÙ\ÎˆÌWØÜØXÍÎH[š\›ÝÜÝÚ\ÜÜ›Ý‚‹HÛÛÜ™[˜]HÝ]\Ù\ÎˆÌŒˆ^\š[Y[[Ü—ÜÙ[XÝYˆ^\š[Y[[Ü—Ü™Y™\™[˜Ù\×Ü™\Ù[LÌˆ™YXÝYØ[Y›ÛÜ™Y™\™[˜ÙWÜ™\Ù[ˆÛÛÜ™[˜]WÛZ\ÜÚ[™Ø[™BˆÛÛÜ™[˜]WÜ™Y™\™[˜ÙWÛZ\ÜÚ[™Ø‚‹Hš\œÝXXÝ[ÛˆØÜ™Y[ˆ[œ]ˆLˆ™]šY]×ÛÛ›WÙ]šY[˜ÙX^\›˜[›ÝÜÎ‚ˆ[š\›Ý”ÌŒÍØ[š\›Ý”M“[š\›Ý”MMÍˆ[š\›Ý”Ž[š\›Ý”ŽÌÌ[š\›Ý”ÌLXˆ[š\›Ý”ÌÎ[š\›Ý”ÌL[š\›Ý”ÍŽMNXˆ[š\›Ý”MN[š\›Ý”NUX[™[š\›Ý”NP–‘L˜‚‚ÛÙH]ÈÚ[™ÙY‚‚‹HYYÜ˜ËØØ][]X×ÙX\Ý\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžKœX‚‹HYYÓHÚ\š[™È[ˆÜ˜ËØØ][]X×ÙX\ØÛKœX‚ˆZ[]\™Ù]YY^[œÚ[Û‹Y˜XÝÜžKX˜]Ú‚‹HYY\ÝËÝ\ÝÝ\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžKœX‚‹HYYÓH\œÙ\ˆÛÝ™\˜YÙH[ˆ\ÝËÝ\ÝØÛKœX‚‹H\]YHÝ\œ™[˜[Z[K\[™[XÚ\Ú[Ûˆ™YÜ™\ÜÚ[Ûˆ[‚ˆ\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œXÈX]ÚH[™XYBˆX]\šX[^™Y\˜Ú]XÝ\™KYY˜][XÚ\Ú[ÛœÈ›ÝÈÛˆXZ[‹‚‹H\]Y\˜X›HØÜÈ™XØ]\ÙHH[ˆÜ™X]YH\˜X›HÛÝ\˜ÙK[Ù‹]]Ý]]‚ˆØÜËÜ›Ú™XÝÜÝ]K›Y[™ØÜËØ\Y˜XÝÚ[™^›Yˆ›ÈXÚ\Ú[Û‹[ÙÈ\]BˆØ\È™YYY™XØ]\ÙH\È[ˆY›Ý™XÛÜ™H™]È\˜X›H\˜Ú]XÝ\™KÜÛXÞBˆXÚ\Ú[Û‹‚‚‘ÝX\™˜Z[Î‚‚‹H›È›ÙXÝ[ÛˆX™[™YÚ\ÝšY\ËÛÛÙÚY\Ë[\ÜË˜Z[‹Ý\ÝÜ]Ëˆ[Ù[ÙZYÚË›ÙXÝ[Ûˆ™\ÚÛËÜˆ™\ÚÛ˜[Y\ÈÙ\™HÚ[™ÙY‚‹H›ÈX™[ÈÙ\™H›Û[ÝYÚ[\ÜY[™]™\žHØ[™Y]H›ÝÈ\ÂˆÛÝ[X›WÛX™[ØØ[™Y]HH˜[ÙX[™™XYWÙ›Ü—ÛX™[Ú[\ÜH˜[ÙX‚‹H›È[Ý]KPÔÐH›ÝÈØ\È\ÙY›Üˆ˜Z[š[™ÈÜˆ™\ÚÛ[š[™Ë‚‹HYXÚ[š\ÛH^Ûš\]ËPËÔšXH›ÝÈšY[ËX™[Ë\™Ù]˜[Y\Ë[™ÛÝ\˜ÙBˆQÈÙ\™H›Ý\ÙY\ÈØÛÜš[™ËÛ[Ù[™X]\™\ËˆPËÔšXH›ÝÈšY[È[™YXÚ[š\ÛBˆÛš\]È\™H›ÝÛÜYY[ÈØ[™Y]K\›ÝÈ]šY[˜ÙHšY[Ë‚‹HH˜YXØ[ØÛØ˜[[Z[ˆ˜[Z[K\[™[\Y˜XÝÈÙ\™H[œÜXÝY]›Ý›ÛYˆ[È\È˜]Ú™XØ]\ÙHH]˜Z[X›H›ÝÜÈ\™H[ÜÝH[Ý]Ü‚ˆÙXÛÛ™\žK\›Ø™H™]šY]ÈX]\šX[˜]\ˆ[ˆÛÝ[X›H]\ËYÜ›ÝÝ[œ]‚‚•™\šYšXØ][ÛŽ‚‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÝ\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžKœH\ÝËÝ\ÝØÛKœNŽÛU\ÝÎŽ\ÝÝ\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžWÜ\œÙ\—ÙY˜][È\X‚ˆ\ÜÙY‚‹HUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝØÛKœH\ÝËÝ\ÝÝ\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžKœH\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œNŽ‘Ù[ÛY]žP\Y˜XÝ™YÜ™\ÜÚ[Û•\ÝÎŽ\ÝÙ›ÛØ]YÛY[YÙ˜[Z[WÜ[™[Ù^\Ú[\ÜÙXÚ\Ú[Û—Ø\XØ][Û—ØÝ\œ™[ØÛÝ[È\X‚ˆŒLH\ÜÙYMŒÝX\ÝÈ\ÜÙY‚‹H\™Ù\ˆÝXÚYÛXÙBˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝØÛKœH\ÝËÝ\ÝÝ\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžKœH\ÝËÝ\ÝÙÙ[ÛY]žWØ\Y˜XÝÜ™YÜ™\ÜÚ[Û‹œH\X‚ˆLÍÈ\ÜÙYŒMˆÝX\ÝÈ\ÜÙY‚‹Hš[˜[[]\Ý‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\XˆMÌˆ\ÜÙYÝX\ÝÈ\ÜÙYÚ]ˆH^\Ý[™ÈÚÛX\›‹ÔØÚTH\™XØ][ÛˆØ\›š[™Ë‚‹Hš[˜[[š]\Ý\ØÛÝ™\žN‚ˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆMMÈ\ÝÈ\ÜÙYÚ]ˆHØ[YH^\Ý[™ÈÚÛX\›‹ÔØÚTH\™XØ][ÛˆØ\›š[™Ë‚‹HUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]XˆLˆÛÝ\˜ÙH™XÛÜ™ËˆYXÚ[š\ÛHš[™Ù\œš[ËMHÛÛÙÞH˜[Z[Y\ËÌˆÝ\˜]YX™[Ë‚‹HUÓ”U\Ü˜È]Ûˆ[HÛÛ\[X[\HÜ˜È\ÝØ‚‹H]Ûˆ[HœÛÛ‹ÛÛ\Y˜XÝËÝŒ×Ý\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžWØ˜]ÚØÝ\œ™[Ì—ÌŒŒŒšœÛÛˆ‹Ù]‹Û[‚‹H]\›Z[š\ÝXÈÓH™\[ˆÚ]KXÜ™X]Y]]ÈŒ‹L‹LŒŽV˜™\›ÙXÙYˆ›ÝH”ÓÓˆ\Y˜XÝ[™X\šÙÝÛˆ™\Üž]KY›Ü‹Xž]K‚‹H™\Ë]ÚYH”ÓÓˆ\œÙNˆÍš[\ÈÚXÚÙY\œÙH\œ›ÜœË‚‹H™\Ë]ÚYH”ÓÓ“\œÙNˆÈš[\È[™ÎNMH[™\ÈÚXÚÙY\œÙH\œ›ÜœË‚‹H™\Ë]ÚYHÔÕ‹ÕÕˆØØ[ŽˆŽHš[\È[™ÍÈ›ÝÜÈØØ[›™Y\œÙH\œ›ÜœË‚‹H\™Ù]YÙ[™\˜]Y\›ÝÈ]šY[˜ÙH]Y]ˆÌÈ›ÝÜÈÚXÚÙY›Ü˜šY[ˆ]šY[˜ÙBˆšY[^[ØYÈ[™[\ÜØÛÝ[X›H›YÈš[Û][ÛœË‚‹H\™Ù]YÛÝ\˜ÙKZ\Ú]Y]ˆ[È™XÛÜ™Y˜XÝÜžHÛÝ\˜ÙH\Ú\ÈX]ÚY‚‹HÚ]Y™ˆKXÚXÚØ‚‹H\ÚÈÝX\™˜Z[ˆMÈÚPˆ]˜Z[X›K‚‹H›Û‹YØ][™È^Ü˜]ÜžH™\Ë]ÚYHÛÝ\˜ÙWØ\Y˜XÝØ\ÚÝÙY\Ø\È][\Yˆ]\È›ÝH˜[YÝ\œ™[Ø]H™XØ]\ÙHÛ\ˆ\˜Ú]™Y\Y˜XÝÈ™Y™\™[˜ÙBˆZ\ÜÚ[™È^\›˜[ÛÜšÝ™Y\È[™Ý[H\ÝÜšXØ[ÛÝ\˜Ù\Ë‚‚ÛÛ[Z]Ü\ÚÜÞ[˜ËÛØÚÈÝ]\Î‚‚‹HÛÛ[Z]\Úˆ[™[™È[[HÜÝZ[™Ù™ˆÛÛ[Z]\ÈÜ™X]YÈš[˜[\ÚYˆPQÚ[™H™\ÜY[ˆH]]ÛX][ÛˆY[[ÜžH[™š[˜[™\ÜÛœÙH™XØ]\ÙHBˆÛÛ[Z]Ø[››ÝÛÛZ[ˆ]ÈÝÛˆš[˜[\Ú‚‹H\ÚÜÞ[˜ÈÝ]\Îˆ[™[™ÎÈÚ[\ÚÈÜšYÚ[‹ÛXZ[˜[™™\šYžBˆPQOHÜšYÚ[‹ÛXZ[˜‚‹HØÚÈ™[X\ÙHÝ]\Îˆ[™[™ÎÈÚ[™[X\ÙHHØ[›ÛšXØ[™\È]]ÛX][ÛˆØÚÂˆY\ˆÛX[‹ÜÞ[˜ÙY™\šYšXØ][Û‹‚‚‘^XÝ™^XÝ[ÛŽ‚‚”[ˆHš\œÝXXÝ[ÛˆØÜ™Y[ˆ[œ]œ›ÛB˜\Y˜XÝËÝŒ×Ý\™Ù]YÙ^[œÚ[Û—Ù˜XÝÜžWØ˜]ÚØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜‚œÛÝ\˜ÙKYœ™YHÝ\œ™[\™Y™\™[˜ÙH\XØ]HÙX\˜ÚÝ\œ™[XÛÝ[X›HÝXÝ\˜[œØÜ™Y[‹^\›˜[[]œËX[ÝXÝ\˜[Û\Ý\ˆ\ÜÚYÛ›Y[[šT™Y‹]ÚYH\XØ]BœØÜ™Y[š[™Ë\›Z[˜[™]šY]ÈXÚ\Ú[Û‹[™[X™[Y˜XÝÜžHØ]H›ÜˆHL‚™^\›˜[™]šY]×ÛÛ›WÙ]šY[˜ÙX›ÝÜËˆÛ›HY\ˆÜÙHØ]\È\ÜÈÚÝ[[žH›ÝÂ˜\›ØXÚHÛÝ[X›K\›Û[Ý[Ûˆ›Ý[™\žK‚‚ˆÈÈÑH^\›˜[YZ\ÜÚ[ÛˆMˆ˜[Y][Ûˆ[‚‹HÕT•QÐUÕUÎˆŒ‹L‹LŒÎŒÎŒŒ‚‹HÕT•QÐUÓÐÐSˆŒ‹L‹LNŒÎŒŒLL‹HØÚÎˆÛÜšËÛØÚÜËØÙWÙ^\›˜[ØYZ\ÜÚ[Û—ÌM‹›ØÚØ‹HS‘QÐUÕUÎˆŒ‹L‹LŒÎLNŒŒ–‚‹HS‘QÐUÓÐÐSˆŒ‹L‹LNLNŒŒ‹LL‹HSTÑQÓRS•UTÎˆLËŒÌÂ‹H]]ÛX][ÛˆQˆÙKY^\›˜[XYZ\ÜÚ[Û‹LM‹]˜[Y][Û˜‚ˆÈÈÈ™\Ý[‚‹HZ[H™\[›˜X›HYZ\ÜÚ[Ûˆ˜[Y][ÛˆØ]H›ÜˆHMˆ›ÝÜÈ[‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û—Ú[\ÜÜ™]šY]×ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜‚‹HÝ]]\Y˜XÝ‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û—ÌM—ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜‚‹HYZ\ÜÚ[Û‹\™XYH™]šY]Î‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ü™XYWÜ™]šY]×ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜‚‹H[X[ˆ™\Ü‚ˆÛÜšËÙ^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û—ÌM—ØÝ\œ™[Ì—ÌŒŒŒ›Y‚‹H™\[›˜X›HÛÙKÝ\ÝÎ‚ˆÜ˜ËØØ][]X×ÙX\Ù^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û‹œXˆÓHÛÛ[X[™Z[Y^\›˜[\ÛÝ\˜ÙKXYZ\ÜÚ[Û‹]˜[Y][Û‹LM˜[™ˆ\ÝËÝ\ÝÙ^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û‹œX‚‚ˆÈÈÈXÚ\Ú[ÛˆÝ[[X\žB‚‹H[Mˆ[\Ü\™]šY]È›ÝÜÈ™XÛÛ˜Ú[H^XÝHÈ[Ý›ÝÜÈ[‚ˆ^\›˜[ØÛÝ[X›WÜ™Y›YÚØØ[™Y]XÝ]K‚‹H[Mˆ\ÜÈ™]šY]ÙYÝÚ\ÜËT›ÝÛÝ\˜ÙKZ\ÚÜ›Ý™[˜[˜ÙK^XÝ™\ÚYYBˆØØ]Ü‹‹ÐQ‘ˆ[™KšXKÜÜXÚYšXÈPË[™KX\ÜÚYÛ›Y[[™™XÛÛ\]Yˆ^XÝÝ\œ™[ÌˆXØÙ\ÜÚ[Û‹ÜÙ\]Y[˜ÙH\XØ]HØ]\Ë‚‹H\›Z[˜[Ý]\ÎˆLˆYZ\ÜÚ[Û—Ü™XYWÜ[™[™×ØÛÛÜ™[˜]WÛX]\šX[^˜][Û˜‚ˆYZ\ÜÚ[Û—Ü™XYWÜ[™[™×ÛØØ]Ü—ÛX]\šX[^˜][Û˜ˆYZ\ÜÚ[Û—Ü™XYWÙ^\›˜[ÛX™[ØØ[™Y]X‚‹H˜[Z[KÛ[™HÛÝ[Îˆ™YÞÞYÙ[‹ÜÝ[\ˆ[™[™ÈÛÛÜ™[˜]NÈÚ[™[ˆÂˆ[™[™ÈØØ]ÜŽÈÛXÛÜÚYKÛXÛ[ÜÚYHH[™[™ÈÛÛÜ™[˜]H[™H[™[™ÂˆØØ]ÜŽÈÜÜÜž[˜[œÙ™\ˆˆ[™[™ÈÛÛÜ™[˜]H[™ˆ[™[™ÈØØ]ÜŽÂˆ˜YXØ[TÐSKØÛØ˜[[Z[ˆÈ[™[™ÈÛÛÜ™[˜]K‚‹H›È›ÝÈØ\È›Ý]YÈ[X[ˆ™]šY]ËˆH™[XZ[š[™ÈÛÜšÈ\ÈYXÚ[šXØ[‚ˆX]\šX[^™KÚ\ÚØØ[ÛÛÜ™[˜]\È›ÜˆHLÛÛÜ™[˜]K\[™[™È›ÝÜË[‚ˆX]\šX[^™H\›Ý™YÛÝ\˜ÙKYœ™YHØØ]ÜˆÚYXØ\œÈ›Üˆ[Mˆ[™™\[ˆ\Âˆ˜[Y][Û‹‚‹H›ÈX™[ÈÙ\™H[\ÜY[™›È›ÙXÝ[Ûˆ™YÚ\ÝžKÚ[\ÜÛÛÛÙÞKÛ[Ù[Âˆ™\ÚÛÜÜ]Ý\™˜XÙHØ\ÈY]Y‚‚ˆÈÈÈ˜[Y][Û‚‚‹H]Ûˆ[HœÛÛ‹ÛÛ\ÜÙY›ÜˆH[Ý[\Ü\™]šY]ËYZ\ÜÚ[Û‚ˆ˜[Y][Û‹[™YZ\ÜÚ[Û‹\™XYH™]šY]È”ÓÓˆ\Y˜XÝË‚‹H›ØÝ\ÙY]\Ý‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÙ^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û‹œH\ÝËÝ\ÝÙ^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û‹œH\ÝËÝ\ÝØÛKœNŽÛU\ÝÎŽ\ÝÙ^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û—Ü[ÝÜ\œÙ\—ÙY˜][È\ÝËÝ\ÝØÛKœNŽÛU\ÝÎŽ\ÝÙ^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û—Ü\œÙ\—ÙY˜][È\X‚ˆ\ÜÙY‚‹H[[š]\Ý‚ˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆKÍˆ\ÝÈ\ÜÙY‚‹HUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]Xˆ\ÜÙYÚ]Ì‚ˆÝ\˜]YYXÚ[š\ÛHX™[Ë‚‹HÝ\œ™[ØÜÈ\Y˜XÝ\™Y™\™[˜ÙHÚXÚÈ\ÜÙYÚ]Z\ÜÚ[™È™Y™\™[˜Ù\ÎÈBˆ[\Ü˜\žHÚXÚÈÝ]]Ø\È›ÝÙ\™XØ]\ÙH]\È›ÝH\˜X›HÝ]]›Ü‚ˆ\È[‹‚‹HÚ]Y™ˆKXÚXÚØˆ\ÜÙY‚‹H›ÙXÝ[Û‹YY]ÝX\™˜Z[ØØ[ŽˆÚ[™ÙY]È\™H[Z]YÈØÜË[™Ù™‹ˆ˜[Y][ÛˆÛÙKÝ\ÝË[™H™]È˜[Y][Û‹Ü™\Ü\Y˜XÝÎÈ›È›ÙXÝ[Û‚ˆ™YÚ\ÝžK[\ÜÛÛÙÞK[Ù[™\ÚÛÜˆÜ]]Ú[™ÙY‚‹H\ÚÈÝX\™˜Z[ˆˆZ˜™\ÜYNÚPˆœ™YK‚‚ˆÈÈÈ^XÝ™^XÝ[Û‚‚”Ý\Ú]HÚ^YZ\ÜÚ[Û—Ü™XYWÜ[™[™×ÛØØ]Ü—ÛX]\šX[^˜][Û˜›ÝÜÂ˜™XØ]\ÙHZ\ˆÛÛÜ™[˜]\È\™H[™XYHØØ[H\Ú[X]ÚY‚˜[š\›Ý”NVMŒMØ[š\›Ý”NX[š\›Ý”NMŒMX[š\›Ý”Œ˜˜[š\›Ý”NMŽQÍ˜[™[š\›Ý”ÌŒNXˆX]\šX[^™H\›Ý™YÛÝ\˜ÙKYœ™YB›ØØ]ÜˆÚYXØ\œÈœ›ÛHH™]šY]ÙY^XÝ™\ÚYYHØØ]ÜœË[ˆ™\[‚˜Z[Y^\›˜[\ÛÝ\˜ÙKXYZ\ÜÚ[Û‹]˜[Y][Û‹LM˜ˆ›ÜˆHÝ\ˆL›ÝÜËš\œÝ›X]\šX[^™HÜˆ\Ú[X]ÚH™Y™\™[˜ÙY‹ÐQ‘ˆÛÛÜ™[˜]\Ë‚‚ˆÈÈÑH^\›˜[[È[™Ù\Ý[ÛˆØÛÝ]‹HÕT•QÐUÕUÎˆŒ‹L‹LŒÎŒÎNÖ‚‹HÕT•QÐUÓÐÐSˆŒ‹L‹LNŒÎNËLL‹HØÚÎˆÛÜšËÛØÚÜËØÙWÙ^\›˜[Ø[×Ú[™Ù\Ý[Û‹›ØÚØ‹HS‘QÐUÕUÎˆŒ‹L‹LUŒŽ–‚‹HS‘QÐUÓÐÐSˆŒ‹L‹LNNŒŽ‹LL‹HSTÑQÓRS•UTÎˆŒ‹ŽNÂ‹H]]ÛX][ÛˆQˆÙKY^\›˜[X[ËZ[™Ù\Ý[Û‹\ØÛÝ]‚ˆÈÈÈ™\Ý[‚‹HZ[H™\[›˜X›H[ÈØÛÝ]Ý™\ˆ™]šY]ÙYÝÚ\ÜËT›ÝÕ[šT›ÝY]Y]KˆÝXÝ\™Y™\ÚYYKØÛÙ˜XÝÜˆ]šY[˜ÙKQ‘‹ÔˆÛÛÜ™[˜]H›Ý™[˜[˜ÙK[™ˆšXKÑPÈ›Ý™[˜[˜ÙK‚‹HÝ]]\Y˜XÝ‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[Ø[×Ú[™Ù\Ý[Û—ÜØÛÝ]ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜‚‹H›Ýš\Ú[Û˜[[\Ü\™]šY]È\Y˜XÝ‚ˆ\Y˜XÝËÝŒ×Ù^\›˜[Ø[×Ú[™Ù\Ý[Û—Ü›Ýš\Ú[Û˜[Ú[\ÜÜ™]šY]×ØÝ\œ™[Ì—ÌŒŒŒšœÛÛ˜‚‹H[X[ˆ™\Ü‚ˆÛÜšËÙ^\›˜[Ø[×Ú[™Ù\Ý[Û—ÜØÛÝ]ØÝ\œ™[Ì—ÌŒŒŒ›Y‚‹H™\[›˜X›HÛÙKÝ\ÝÎ‚ˆÜ˜ËØØ][]X×ÙX\Ù^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û‹œXÓHÛÛ[X[™ˆZ[Y^\›˜[X[ËZ[™Ù\Ý[Û‹\ØÛÝ]\ÝËÝ\ÝÙ^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û‹œXˆ[™\ÝËÝ\ÝØÛKœX‚‚ˆÈÈÈXÚ\Ú[ÛˆÝ[[X\žB‚‹HØ[™Y]H›ÝÜÎˆŽLÈXÜ›ÜÜÈHÙ]™[ˆ™\]Y\ÝY[™\Ë‚‹H›Ýš\Ú[Û˜[™]šY]È›ÝÜÎˆÍM[^XÚ]H›Ýš\Ú[Û˜[[[ˆÙKY^\›˜[XYZ\ÜÚ[Û‹LM‹]˜[Y][Û˜ÜˆHØØ[YÝXØÙ\ÜÛÜˆ˜[Y]\ÈBˆØ]\Ë‚‹H\›Z[˜[Ý]\ÎˆÍMˆ›Ýš\Ú[Û˜[Ù^\›˜[ØÛÝ[X›WÜ™Y›YÚØØ[™Y]XNMˆØØ]Ü—Ü™XYWØØ[™Y]XMÈÛÛÜ™[˜]WÜ™XYWÜ[™[™×ÛØØ]Ü˜ÎBˆ›ØÚÙYÙ\XØ]WÛÜ—ØÝ\œ™[Ü™YÚ\ÝžWØÛÛ™›XÝˆØØ]Ü—Ü™\Z\—ØØ[™Y]XÈÛÛÜ™[˜]WÜ™\Z\—ØØ[™Y]X[™‚ˆ\™Ø›ØÚÙYÝÚ]Û™^ØXÝ[Û˜‚‹H˜[Z[KÛ[™HÛÝ™\˜YÙNˆY][Y›Û\ÙK™YÞÞYÙ[‹ÜÝ[\‹Ú[™[‹ˆÛXÛÜÚYKÛXÛ[ÜÚYKÜÜÜž[˜[œÙ™\‹˜YXØ[TÐSKØÛØ˜[[Z[‹[™ˆ™X\‹[Üœ[‹Û›Ë\™[XX›K\ÝXÝ\™K‚‹HÛÝ\˜ÙH™]šY]˜[˜Z[\™\Îˆˆ[šT›ÝÚ[™ÛK\]Y\žH[Z]\È™XÛÜ™Y\ÈLÂˆ\È[ˆ™\]Y\ÝYL™XÛÜ™È\ˆ[™K\ÙY›ÈYÚ[˜][Û‹\ØX›YˆPËX˜\ÙYšXH˜[˜XÚÈ›Üˆ[[YK[™\™›Ü›YY›ÈÛÛÜ™[˜]HÝÛ›ØYË‚‹H\XØ]H[™[™È[˜ÛY\È›ÝÝ\œ™[ÌˆXØÙ\ÜÚ[Û‹ÜÙ\]Y[˜ÙHÝ]\È[™ˆ^XÝ^\›˜[\[ÝXØÙ\ÜÚ[Û‹ÜÙ\]Y[˜ÙHÝ]\Ëˆ[ÝÝ™\›\È\™H›ØÚÙY\Âˆ\XØ]KØÝ\œ™[\™YÚ\ÝžHÛÛ™›XÝË‚‹H›ÈX™[ÈÙ\™H[\ÜY[™›È›ÙXÝ[Ûˆ™YÚ\ÝžKÚ[\ÜÛÛÛÙÞKÛ[Ù[Âˆ™\ÚÛÜÜ]Ý\™˜XÙHØ\ÈY]Y‚‚ˆÈÈÈ˜[Y][Û‚‚‹H]Ûˆ[HœÛÛ‹ÛÛ\ÜÙY›Üˆ›Ý[È”ÓÓˆ\Y˜XÝË‚‹H™\]Z\™Y\›ÝËYšY[[˜\šX[ÚXÚÈ\ÜÙYˆ]™\žH›ÝÈ\È›Ý™[˜[˜ÙKˆ\›Z[˜[Ý]K\XØ]HÝ]\Ë]šY[˜ÙH˜\Ú\Ë›ØÚÙ\ˆ˜\Ú\ËÛÝ\˜ÙBˆ]Y\žKÚ\ÚÝ[Y\Ý[\[™™^XÝ[Û‹‚‹H›ØÝ\ÙY]\Ý‚ˆUÓ”U\Ü˜È]Ûˆ[H]\Ý\ÝËÝ\ÝÙ^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û‹œH\ÝËÝ\ÝÙ^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û‹œH\ÝËÝ\ÝØÛKœNŽÛU\ÝÎŽ\ÝÙ^\›˜[ÜÛÝ\˜ÙWÚ[™Ù\Ý[Û—Ü[ÝÜ\œÙ\—ÙY˜][È\ÝËÝ\ÝØÛKœNŽÛU\ÝÎŽ\ÝÙ^\›˜[ÜÛÝ\˜ÙWØYZ\ÜÚ[Û—Ý˜[Y][Û—Ü\œÙ\—ÙY˜][È\ÝËÝ\ÝØÛKœNŽÛU\ÝÎŽ\ÝÙ^\›˜[Ø[×Ú[™Ù\Ý[Û—ÜØÛÝ]Ü\œÙ\—ÙY˜][È\X‚ˆˆ\ÜÙY‚‹H[[š]\Ý‚ˆUÓ”U\Ü˜È]Ûˆ[H[š]\Ý\ØÛÝ™\ˆ\È\ÝØˆKÎ\ÝÈ\ÜÙY‚‹HUÓ”U\Ü˜È]Ûˆ[HØ][]X×ÙX\˜ÛH˜[Y]Xˆ\ÜÙYÚ]Ì‚ˆÝ\˜]YYXÚ[š\ÛHX™[Ë‚‹HÝ\œ™[ØÜÈ\Y˜XÝ\™Y™\™[˜ÙHÚXÚÈ\ÜÙYÚ]Z\ÜÚ[™È™Y™\™[˜Ù\ÎÈBˆ[\Ü˜\žHÚXÚÈÝ]]Ø\È›ÝÙ\™XØ]\ÙH]\È›Ý\˜X›H›Üˆ\È[‹‚‹HÚ]Y™ˆKXÚXÚØˆ\ÜÙY‚‹H›ÙXÝ[Û‹YY]ÝX\™˜Z[ØØ[ŽˆÚ[™ÙY]È\™H[Z]YÈØÜË[™Ù™‹ˆ[™Ù\Ý[ÛˆÛÙKÝ\ÝË[™H™]ÈØÛÝ]Ü™\Ü\Y˜XÝÎÈ›È›ÙXÝ[Û‚ˆ™YÚ\ÝžK[\ÜÛÛÙÞK[Ù[™\ÚÛÜˆÜ]]Ú[™ÙY‚‹H\ÚÈÝX\™˜Z[ˆˆZ˜™\ÜYNÚPˆœ™YK‚‚ˆÈÈÈ^XÝ™^XÝ[Û‚‚”[ˆHØØ[YYZ\ÜÚ[Û‹]˜[Y][Ûˆ[™HÝ™\ˆHÛX[™\™\Ù[]]™HÛXÙHœ›ÛBHÍM›Ýš\Ú[Û˜[™]šY]È›ÝÜÈ™Y›Ü™H[žH›ÙXÝ[Ûˆ[\Ü\ØÝ\ÜÚ[Û‹ˆÝ\Ú]›ÝÜÈ]]™H^\š[Y[[ˆ›Ý™[˜[˜ÙH[™^XÝ™]šY]ÙYØØ]ÜœË[ˆ^[™Û›HY\ˆÛÛÜ™[˜]HX]\šX[^˜][Û‹ØØ]ÜˆÚYXØ\œËÝXÝ\˜[™\XØ]HØÜ™Y[š[™ËX™[Y˜XÝÜžHØ]\Ë[™^XÚ]›ÙXÝ[Ûˆ]]Üš^˜][Û‚˜[\ÜË‚