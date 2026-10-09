Warning: truncated output (original token count: 518559)
... 1025657 bytes omitted ...

# Handoff

<!-- current-research-handoff:start -->
## Current research handoff — Choi benchmark route stopped, 2026-10-09

- **Run/continuity:** automation run
  `automation-6ac8bd9adeb8819096b82a61101ea18a-20261009T160301Z`, shared-control
  epoch 8, from merged main `9e67a1cf620cef98d6b35531089983017468ef98`.
  The previous public-panel survey, PRs #143–#147 and all frozen evidence were
  preserved. Three complementary same-model evidence, reconstruction and
  critical reviews were used; they are not independent expert review.
- **Question:** can Choi et al. version 3 support one fixed 69-case prospective
  comparison of sequence and structure baselines against calibrated
  intended-bond cleavage outcomes?
- **Finding:** no. The primary prose supports 13/69 activity and intended-site
  LC-MS for all 13 reported positives, but the accessible public material does
  not expose a lossless 69-row enzyme/substrate/outcome/model join, expression
  and assay attrition, or a common quantitative measurement/detection bound for
  every negative. The six structures (9YNL, 9YNM, 9YOX, 9YOY, 9YOZ, 9YP0) are a
  positive-enriched validation subset, not same-case inputs for 69 attempts.
  The 13/69 outcome was already public in version 1 on 2025-11-22, so a model
  chosen later is not a prospective test on this cohort. The cognate screen also
  lacks a matched noncognate cross-target matrix and therefore does not measure
  programmable specificity.
- **Decision and limit:** stop this all-in-one benchmark route and do not run a
  sequence or structure model on the top-level summary. This is an evidence and
  access stop, not a claim that the authors lack the data and not counterevidence
  to the reported proteases. Reopen only with a public hashed source bundle that
  resolves all 69 attempts, calibrated negatives and pre-assay same-case inputs;
  a clean specificity claim additionally requires a previously unexposed cohort
  and matched cross-target panel. Exact evidence and the fail-closed schema are
  in `tools/research_lanes/protease_retargeting/choi_v3_benchmark_qualification.json`.
- **Source audit:** official bioRxiv metadata confirms version 3, 2026-09-21 and
  the canonical PDF. Direct PDF/JATS attempts returned HTTP 429; NCBI OA returned
  404 and PMC EFetch withheld full-text XML. Supplementary bytes were not
  recovered. Batch `public_bond_resolved_panel_survey_20261009` is cumulatively
  17 known direct HTTP requests and 185,438 persisted bytes (this run: 10 and
  82,956). Search/connector transport is unexposed; no requester-pays TDM route
  was used.
- **Strongest alternative / next action:** ask the narrower question the public
  data can answer. Audit Huber et al.'s exact-sequence DNA-recording panel once
  for train/test chronology, assayed construct identity and reporter calibration;
  only then preregister a family- or substrate-held-out sequence-specificity
  baseline. Keep it explicitly reporter-level, not bond-localized cleavage or
  de novo design success. Stop if held-out choices used the same measured data,
  exact constructs cannot be reconstructed or normalization is incomparable.
- **Boundaries:** no model, scorer, training, paid compute, provider mutation,
  separately billed API, lab order or outreach. Prime remains disabled; USD 8
  per job and USD 50 per Chicago month are unchanged. Protected registries and
  prior outcomes remain frozen.
<!-- current-research-handoff:end -->

## Historical handoffs — superseded as an execution queue

## Current research handoff — cloud team deployment, 2026-10-09

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
  Revealed-minus-hidden median worst-group RMSDs are −4.655, +8.309, +9.484 and
  +14.937 Å for paired sequence seeds 200–203. Even seed 200 worsens base and
  reactive-backbone medians (+0.227/+0.236 Å). All 40 complex and 40 monomer
  assignments are retained. Four design-seed pairs, not 40 independent complex
  experiments, are the comparison units. Keep the frozen endpoint unchanged.
- **Scientific consequence:** the input omission was verified, but exposing it
  did not repair joint recovery on this scaffold. Native context adds 55 fixed
  sidechain atoms while retaining Zn/water for every polymer residue. All 868
  finite audited retained coordinates per sequence-design output are unchanged.
  Revealed complex fold RMSD medians are 9.166–14.617 Å; isolated donor gains
  can accompany large metal-ligand losses. Do not adopt this switch as an
  established repair or try further water/context seeds to find a favorable one.
- **Reassessment using existing evidence:** retrospective calculation on all 20
  already completed TDPn3 predictions uses its own correctly mapped author AF3
  reference. Median worst-group errors are 0.646/0.797 Å for the 10mer versus
  2.864/2.672 Å for the 12mer, largely water displacement, with close global
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

- Continued on `main`/branch (d14fa1f7+). User: "pursue Option B — the new held-out." Leakage-safe order:
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
  divergent registries" was WRONG — a **shallow-clone artifact**. After `git fetch --unshallow`, the
  real common ancestor is `79dc2d3a` (session base; shared root `93806418`), local `main` (`bed58963`)
  is an ancestor of the branch, and the branch is a strict superset (main 0 commits ahead, branch 148
  ahead). Merged via clean fast-forward: `main == d7a985ed` (origin/main + local main + branch all
  equal). No conflicts, nothing lost.

- Continued on branch `claude/continue-last-commit-ytktge` from commit `937b24a6`. User: "merge all
  progress and start work on Gate 1."
- MERGE: `main` and this branch have **no common ancestor** (roots: main 468591fd, branch f60617d6) and
  **divergent `mechanism_fingerprints.json`** (main 2670b1ad vs branch 19d837f1; curated702 identical).
  A merge would be `--allow-unrelated-histories` with whole-tree + registry conflicts. NOT forced — that
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
  `main`; (ii) pick the fork — adopt June 9 coarse router (then Gate 2 gold off-M-CSA + Gate 3
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
  non-M-CSA positives with gold mechanism labels + structures) — a real curation effort. Otherwise the
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
  gold) — a real pipeline, the user's call. Otherwise the fold-channel result stands: generalizes off
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
  metal_dependent_hydrolase 26/34 (0.76), heme_peroxidase_oxidase 17/20 (0.85), plp 6/6 (1.00) — robust,
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
  (both are governance-gated). Built the harness so the eventual run is a one-liner — mirroring how the
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
    GiB floor — wave2 itself recorded downloads disabled below the floor), or (b) promote structured
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
  - External off-M-CSA negative fold-NN median **0.574** ≈ M-CSA OOS **0.566**, far below M-CSA
    in-scope **0.743**; only 2/52 reach the in-scope median.
  - Frontier: fold-NN >= 0.70 leaves just **3/52 (5.8%)** external negatives un-abstained (M-CSA OOS
    4/26 in step), while in-scope retention is 20/35 — external negatives reject together with M-CSA OOS.
  - This is the off-M-CSA OOS-rejection property the cofactor channel lacked; the fold channel (not more
    fingerprint families) is the deployment-abstention lever.
- Caveats recorded in docs: off-M-CSA OOS *rejection* only, not off-M-CSA in-scope *recovery* (needs
  non-M-CSA positives with known mechanism + structure); curated negative panel, not a random sample;
  strict gate lowers in-scope recovery.
- Tests: `tests/test_external_offmcsa_fold_abstention_readout.py` (5) + a CLI parser-defaults case.
  Regenerated docs artifact-reference check -> missing 0.
- Validation: focused unittest (off-M-CSA readout + full test_cli + prior readouts) OK; compileall OK;
  registry `validate` OK (57 FP intact); docs reference check missing 0; `git diff --check` clean.
- Next exact action: close the other half of the deployment question — assemble a **non-M-CSA positive**
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
  9/26 frozen, 30/35 @ 8/26 at the 0.44 dial), proving the 30/35→13/35 drift is the registry growth
  (54→57, v2 metal split) consulted by `predicted_geometry_robustness` — the graph/labels/geometry/
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
    holding 30/35). Residual OOS FPs are high-fold-similar (0.43–0.73); **7 of 8 are
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
  (4756 alignment rows, 61 calibration queries × 132 train in-scope targets). Staged coordinate
  symlinks and the foldseek temp dir are reconstructible and git-ignored; the result TSV is committed.
- Added the row-aligned readout builder + CLI:
  `src/catalytic_earth/current57_fold_tm_recompute_readout.py` and
  `build-current57-fold-tm-recompute-readout`. New artifact/report:
  `artifacts/v3_current57_fold_tm_recompute_readout_current702_20260628.json` and
  `work/current57_fold_tm_recompute_readout_current702_20260628.md`. Result
  `current57_fold_tm_recompute_readout_row_aligned`:
  - Recomputed fold-NN coverage **35/35** calibration in-scope and **26/26** OOS (cached overlap was
    **4/35** and **0/26**) — the cofactor/fold alignment blocker is resolved.
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
  `artifacts/v3_external_source_pilot_success_criteria_q6nsj0_replacement_current702_20260616_run22…212152 tokens truncated…d docs to the 59/59 gate state, and rerun the full validation stack
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

- 2026-05-27 `m_csa:497` expert label-state revision: relabeled from
  `seed_fingerprint::flavin_dehydrogenase_reductase` to `out_of_scope` after
  mechanism-locus review concluded the row is flavodiiron nitric oxide
  reduction at a non-heme Fe(II)Fe(II) center, with FMNH2 acting as electron
  donor rather than catalytic flavin hydride-transfer locus. Canonical label
  count remains 702; seed labels are now 231 and out-of-scope labels 471. See
  `artifacts/v3_m_csa497_label_revision_702_20260527.json`,
  `artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json`, and
  `work/m_csa497_label_revision_20260527.md`.

- 2026-05-27 Packet 1 / Wave 1 follow-through lock-down: read the original
  Wave 1 result card through the `m_csa:497` metric-impact artifact, the Wave 1
  result-card addendum, the flavin hydride-transfer sublabel demotion, and
  `artifacts/v3_packet1_wave1_lockdown_addendum_702_20260527.json`. Locked eval
  cells are: `m_csa:217` and `m_csa:477` as TM-pair-verified fold-conflict OOS
  anchors; `m_csa:428` as partial fold-conflict with TIM-barrel
  incidental-primary-hit caveat; `m_csa:440` as near-orphan OOS/router
  abstention diagnostic; and `m_csa:497` excluded from primary flavin and
  near-orphan primary metrics after OOS relabel. `m_csa:750` is review-blocked
  and unsafe for Wave 1 canary use until label state resolves; `m_csa:43`
  remains a valid metal-hydrolase canary. See
  `work/packet1_wave1_followthrough_20260527.md`.

## Automation run catalytic-earth-lever-3-2-forward-push
STARTED_AT_UTC: 2026-06-02T19:02:13Z
STARTED_AT_LOCAL: 2026-06-02 14:02:13 CDT
ENDED_AT_UTC: 2026-06-02T19:43:45Z
ENDED_AT_LOCAL: 2026-06-02 14:43:45 CDT
ELAPSED_MINUTES: 41.5

Wrapped before 55 minutes because the mechanically safe Lever 4 locator-blocker
surface is complete for this run: the remaining rows all require explicit
human/policy/scientific decisions before any locator copy, coordinate fetch,
predicted-geometry scoring, label import, or countability action.

What changed:

- Resolved the highest-priority `mh_067`/`mh_068` split-safe locator-copy class:
  added `v3_family_panel_source_free_locator_copy_decision_mh067_mh068_current702_20260602`,
  copied the approved review-only source-free locators into
  `artifacts/family_panel_source_free_active_site_locators_current702_20260601/`,
  repaired the three `mh_067` candidate positions against the local AFDB model,
  reran locator schema audit, source-free predicted-geometry manifest/retrieval,
  source-check preflight, family-panel readout, source-check queue/completion,
  missing-primary-channel queue/diagnosis, countability preflight, and import
  blocker gate.
- Added review-only source-check packets for `mh_067` and `mh_068`. Both are
  completed source checks with no family promotion, no import readiness, and no
  label/countability change.
- Completed the dedicated `external_glycoside_panel` NAG validator:
  `v3_family_panel_source_free_locator_glycoside_nag_validator_external_glycoside_panel_current702_20260602`
  rejects automatic NAG retargeting because 4/4 NAG sites have near-covalent
  C1-Asn contacts consistent with glycan/N-linked glycosylation context.
- Added `mh_065`/`mh_072` accession-equivalence position audit:
  `v3_family_panel_source_free_locator_accession_equivalence_position_audit_mh065_mh072_current702_20260602`.
  The selected PDBs still map to representative accessions and raw locator
  positions have 0/6 expected residue-code matches in the requested UniProt AFDB
  models, so representative equivalence alone is not sufficient for copy.
- Added `mh_064` alternate-coordinate local-cache preflight:
  `v3_family_panel_source_free_locator_mh064_alternate_coordinate_local_cache_preflight_current702_20260602`.
  It confirms 0/5 alternate CIFs (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, `3SPU`) are
  cached locally and no fetch was attempted.
- Added Q59490 nonlabel-locator feasibility audit:
  `v3_family_panel_source_free_locator_q59490_nonlabel_locator_feasibility_audit_current702_20260602`.
  The selected 1L1L coordinate has water HETATMs only, AFDB Q59490 has no HETATM
  anchor, and the candidate sidecar has 0 residue locators; an alternate source
  row/coordinate or explicit nonlabel strategy remains required.
- Updated `work/family_panel_source_free_locator_blocker_resolution_status_current702_20260601.md`
  and the human decision matrix/import blocker reports so all five unresolved
  rows point to concrete remaining decisions. Import preview remains blocked:
  0/22 rows import-ready, 0 countable labels authorized, and 5 priority rows
  require human/policy decisions.
- Updated CLI/generator logic for the `mh_067`/`mh_068` locator-copy decision and
  refreshed regression coverage for the new blocker artifacts and gate wording.

Guardrails:

- No labels, registries, ontologies, imports, production thresholds, model
  weights, network source fetches, or coordinate downloads changed.
- No heldout training/tuning was performed. New family-panel artifacts are
  review-only and non-countable.

Verification:

- `python -m compileall -q src/catalytic_earth/northstar_next_levers.py src/catalytic_earth/cli.py tests/test_geometry_artifact_regression.py`
- Focused locator/gate regression slice: 21 passed, 122 deselected.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 702 curated labels.
- `python -m json.tool` on the new JSON artifacts.
- `PYTHONPATH=src python -m pytest tests/test_northstar_next_levers.py tests/test_geometry_artifact_regression.py tests/test_cli.py -q`: 364 passed, 81 subtests.
- Full `PYTHONPATH=src python -m pytest -q`: 1235 passed, 100 subtests, one
  existing sklearn/SciPy warning.
- Full `PYTHONPATH=src python -m unittest discover -s tests`: 1190 passed, same
  existing sklearn/SciPy warning.
- `PYTHONPATH=src python -m compileall -q src tests`.
- Current-docs artifact-reference check: 557 checked, 0 missing.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`: 2 passed.
- Repo-wide JSON parse sweep: 3331 JSON files parsed.
- `git diff --check` passed.

Exact next action:

Do not rerun locator discovery. Start with the top remaining decision class:
for `mh_065`/`mh_072`, provide matching frozen coordinates or explicitly approve
alignment/remapped locators before any raw representative-coordinate copy. Then
rerun locator schema/scoring only if approved. The other remaining decisions are
`external_glycoside_panel` substrate-complex or expert-approved non-glycan
locator, `mh_064` alternate-coordinate fetch approval/rejection, and Q59490
alternate source or explicit nonlabel locator strategy.

## Automation run: catalytic-earth-lever-3-2-forward-push 2026-06-04

STARTED_AT_UTC: 2026-06-04T13:02:32Z
STARTED_AT_LOCAL: 2026-06-04T08:02:32-0500
ENDED_AT_UTC: 2026-06-04T13:52:40Z
ENDED_AT_LOCAL: 2026-06-04T08:52:40-0500 CDT
ELAPSED_MINUTES: 50.1

Scope: Lever 3 only. Starting from the current exact next action above: resolve
or precisely block the remaining confounded-safe locator/novelty gate evidence
decisions without changing labels, registries, ontologies, imports, production
thresholds, model weights, or heldout splits.

What changed:

- Added a P07658 prediction dispatch packet:
  `artifacts/v3_fold_augmented_p07658_prediction_dispatch_packet_current702_20260604.json`
  and
  `work/fold_augmented_p07658_prediction_dispatch_packet_current702_20260604.md`.
  The packet composes the frozen 715-aa FASTA, provenance template, public and
  local provider probes, and acceptance preflight. It is ready for an external
  approved provider run but blocked now: 0/6 provider routes return a coordinate,
  0 candidate coordinate files exist, 0 candidate provenance files exist, and
  7 acceptance checks still fail. No coordinate was staged or scored.
- Added high-cofactor train/cal OOS acquisition dispatch:
  `artifacts/v3_fold_augmented_confounded_proxy_high_cofactor_acquisition_dispatch_packet_current702_20260604.json`
  and report. It freezes 16 unfilled intake slots with acceptance checks for
  non-heldout train/cal OOS role, source-free high-cofactor membership,
  deployment-valid predicted coordinate/provenance, no experimental-PDB shortcut,
  and unchanged threshold `0.44155`. The 16 existing near misses remain
  non-countable and no candidate row is registered or scored.
- Added same-family structural train/cal OOS acquisition dispatch:
  `artifacts/v3_fold_augmented_confounded_proxy_same_family_structural_acquisition_dispatch_packet_current702_20260604.json`
  and report. It freezes 170 unfilled intake slots with the same deployment and
  guardrail checks. The 80 background structural rows remain non-countable and
  no candidate row is registered or scored.
- Added combined dispatch readiness summary:
  `artifacts/v3_fold_augmented_lever3_dispatch_readiness_summary_current702_20260604.json`
  and report. Final counts: 3/3 dispatch packets ready for external action but
  blocked; 186 train/cal OOS intake slots required; 0 slots filled; 0 slots
  ready to score; 0 guardrail violations; fixed-threshold audit not ready.
- Regenerated the Lever 3 blocker-packet guardrail audit, minimum next-experiment
  queue, and queue/template guardrail audit. The final blocker audit checks 7
  artifacts with 0 violations; the final queue/template audit checks 9 artifacts
  with 0 violations.
- Added builder tests, CLI registrations, current-artifact regressions, and a
  source-artifact checksum regression so stale source hashes in the new dispatch
  packets are caught.

Guardrails:

- Worked only on Lever 3.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, or threshold values changed.
- No heldout M-CSA rows were used for training or threshold tuning.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or
  experimental PDB metadata were used as predictive features.
- No row was registered, scored, imported, promoted, or used for a fixed-threshold
  audit rerun.
- No coordinate was staged, downloaded, or imported. Experimental/public PDB
  evidence remains blocker evidence only.

Verification:

- Focused builder slice:
  `PYTHONPATH=src python -m pytest tests/test_northstar_next_levers.py -k 'dispatch_readiness_summary or acquisition_dispatch or p07658_prediction_dispatch' -q`:
  4 passed, 177 deselected.
- Focused artifact regression after final regeneration:
  `PYTHONPATH=src python -m pytest tests/test_geometry_artifact_regression.py -k 'dispatch_readiness_summary or queue_and_template_guardrail or acquisition_dispatch or p07658_prediction_dispatch or dispatch_source_artifact_hashes' -q`:
  6 passed, 228 deselected, 4 subtests passed.
- Full touched-test slice:
  `PYTHONPATH=src python -m pytest tests/test_northstar_next_levers.py tests/test_geometry_artifact_regression.py tests/test_cli.py -q`:
  534 passed, 169 subtests passed.
- Final full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1406 passed, 188 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Final full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1361 tests passed, with
  the same existing sklearn/SciPy deprecation warning.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, 702 labels.
- `PYTHONPATH=src python -m compileall -q src tests`.
- `PYTHONPATH=src python -m pytest tests/test_progress.py -q`: 3 passed.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`: 2 passed.
- Source-artifact hash sweep over the new dispatch/audit artifacts:
  18 source hashes checked, 0 stale.
- Repo-wide JSON parse: 3529 JSON files checked.
- `git diff --check`.
- Disk guardrail: 20 GiB available.

Commit/push status:

- Handoff/status/memory are being updated after validation. Commit, push,
  `HEAD == origin/main` verification, and lock release are the remaining
  mechanical wrap steps after this handoff edit.

Exact next action:

Do not rerun or retune threshold `0.44155` yet. The next Lever 3 action is:

1. Run/provision exactly one approved full-length predictor/provider using
   `work/fold_augmented_p07658_full_length_prediction_input_current702_20260604.fasta`.
2. Write the returned coordinate to the preferred P07658 coordinate path and
   fill
   `artifacts/v3_fold_augmented_p07658_prediction_provenance_filled_current702_20260604.json`
   with provider/model/version/path/checksum, sequence SHA/length, U-position
   140 handling, and explicit no-experimental-shortcut evidence.
3. Rerun
   `build-fold-augmented-p07658-prediction-acceptance-preflight` with the
   candidate coordinate and filled provenance. Stage and score P07658 only if
   every acceptance check passes.
4. After P07658 passes, fill the 16 source-free high-cofactor train/cal OOS
   intake slots; then handle the larger 170-row same-family structural intake.
   Score only accepted rows at unchanged threshold `0.44155` and only after
   intake checks pass.

## Automation/handoff update: family admission dependency reduction 2026-06-08

Scope: Reduce Vivek dependency in the targeted family-label expansion path
without importing labels, changing registries/ontologies, or promoting any row
to countable status.

What changed:

- Added `family_admission_architecture_default_v1` proposals to the family
  label admission pipeline. Pending family-decision rows now get an
  architecture-derived non-counting default when the existing channels support
  reject/OOS preservation or review-only preservation.
- Regenerated:
  `artifacts/v3_family_label_admission_pipeline_current702_20260607.json`,
  `artifacts/v3_family_label_admission_expert_decision_template_current702_20260607.json`,
  and `work/family_label_admission_pipeline_current702_20260607.md`.
- Current result for the 6 previously human-blocked family-decision rows:
  6/6 have architecture default non-counting proposals and
  `human_family_decision_rows_after_architecture_defaults = 0`.
- Proposed defaults:
  `m_csa:10`, `m_csa:30`, `m_csa:31`, and `m_csa:191` ->
  `reject_family_panel_import_candidate`;
  `m_csa:448` and `m_csa:973` ->
  `keep_family_panel_review_only_require_more_evidence`.
- Countable/import safety is unchanged: architecture defaults may route rows
  away from import or keep them review-only, but may not accept a family-panel
  import candidate, promote a countable label, alter splits, or change
  thresholds without human review.

How agents should read this:

- Do not ask Vivek to adjudicate these 6 rows just to preserve non-counting
  signal. Use the architecture proposal layer unless the goal is to override a
  row into countable promotion.
- The remaining family-panel work is locator/coordinate acquisition and true
  countable family expansion, not repeated blocker-packet prose on these same
  six rows.

Verification:

- `PYTHONPATH=src python -m pytest tests/test_family_label_admission.py -q`:
  4 passed, 9 subtests passed.
- `PYTHONPATH=src python -m pytest tests/test_cli.py -q`:
  206 passed, 160 subtests passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, 702 labels.
- JSON parse for the regenerated family-admission artifacts passed.
- `git diff --check` passed.

## Automation/handoff update: architecture defaults materialized 2026-06-08

Scope: Convert architecture-proposed non-counting family-admission defaults into
the existing reviewed-decision application path, so agents stop treating the
same six rows as live human blockers.

What changed:

- Added CLI:
  `PYTHONPATH=src python -m catalytic_earth.cli materialize-family-label-admission-architecture-defaults`.
- Added artifact:
  `artifacts/v3_family_label_admission_architecture_default_decisions_current702_20260608.json`
  and report:
  `work/family_label_admission_architecture_default_decisions_current702_20260608.md`.
- Materialized 6 non-counting decisions from
  `family_admission_architecture_default_v1`:
  4 `reject_family_panel_import_candidate` and
  2 `keep_family_panel_review_only_require_more_evidence`.
- Applied the materialized decisions through the existing expert-decision
  application:
  `artifacts/v3_fold_augmented_family_panel_expert_import_decision_application_current702_20260603.json`.
- Regenerated the accepted import preview, label-factory readiness, and family
  admission pipeline. Final admission-state counts now have
  `blocked_family_decision = 0`, `reject_preserve_signal = 4`, and
  `review_only_evidence = 2`.

Guardrails:

- No accept/import/countable promotion decisions were materialized.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, or model weights changed.
- The materializer refuses architecture defaults that propose
  `explicit_accept_family_panel_import_candidate`.

Current next action:

- The family-decision blocker is cleared. Do not ask Vivek to review
  `m_csa:10`, `m_csa:30`, `m_csa:31`, `m_csa:191`, `m_csa:448`, or
  `m_csa:973` again unless the goal is to override them into countable
  promotion.
- The remaining current-family blockers are concrete locator/coordinate
  blockers: `mh_065`, `mh_072`, `external_glycoside_panel`, `mh_064`, and
  `secondary_probe::cobalamin_radical_rearrangement`.

## Automation Run: targeted expansion factory (2026-06-08T04:06:45Z)
- STARTED_AT_UTC: 2026-06-08T04:06:45Z
- STARTED_AT_LOCAL: Sun Jun  7 23:06:45 CDT 2026
- ENDED_AT_UTC: 2026-06-08T04:57:20Z
- ENDED_AT_LOCAL: Sun Jun  7 23:57:20 CDT 2026
- ELAPSED_MINUTES: 50.583
- Automation ID: catalytic-earth-family-label-admission-pipeline
- Status: wrap complete; commit/push/sync/lock-release are the remaining
  mechanical steps after this handoff edit.

Scope:

- Built the first reusable targeted expansion factory output for diverse atlas
  growth from current local/data sources. The batch evaluates 703 non-importing
  candidates across 12 targeted family axes from 324 M-CSA expansion rows plus
  379 UniProt/Swiss-Prot external-freeze rows.
- Excluded the already materialized architecture-default rows
  `m_csa:10`, `m_csa:30`, `m_csa:31`, `m_csa:191`, `m_csa:448`, and
  `m_csa:973`.
- Added a machine-readable first-action screen input for the 12 external
  review-only rows that should enter source-free duplicate, structural, UniRef,
  review, and label-factory gates next.

Artifacts/reports produced:

- `artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json`
  (`v3_targeted_expansion_factory_batch_current702_20260608`): 703 candidates,
  12 family axes, exact-one-state audit, source hashes, admission states,
  first-action screen input, and 0 countable/import-ready rows.
- `work/targeted_expansion_factory_batch_current702_20260608.md`: markdown
  report with admission counts, family axes, coordinate status, proposed tiers,
  source hashes, action tranches, first-action preview, blockers, and next
  batch recommendations.

Key counts:

- Admission states: 262 `review_only_evidence`, 178 `acquisition_needed`,
  130 `blocked_family_decision`, 72 `blocked_locator`, 58
  `reject_preserve_signal`, 3 `blocked_coordinate`, 0
  `countable_candidate`, and 0 `oos_hard_negative`.
- Source namespaces: 324 `m_csa`, 379 `uniprot_swissprot`.
- Coordinate statuses: 322 `experimental_pdb_selected`, 248
  `experimental_pdb_references_present`, 130
  `predicted_alphafold_reference_present`, 2 `coordinate_missing`, and 1
  `coordinate_reference_missing`.
- First-action screen input: 12 `review_only_evidence` external rows:
  `uniprot:P07237`, `uniprot:P0A6L4`, `uniprot:P14174`,
  `uniprot:P28240`, `uniprot:P28330`, `uniprot:P30101`,
  `uniprot:P30838`, `uniprot:P31040`, `uniprot:P36959`,
  `uniprot:P54098`, `uniprot:Q8TAT5`, and `uniprot:Q9BZE2`.

Code paths changed:

- Added `src/catalytic_earth/targeted_expansion_factory.py`.
- Added CLI wiring in `src/catalytic_earth/cli.py`:
  `build-targeted-expansion-factory-batch`.
- Added `tests/test_targeted_expansion_factory.py`.
- Added CLI parser coverage in `tests/test_cli.py`.
- Updated the current family-panel decision regression in
  `tests/test_geometry_artifact_regression.py` to match the already
  materialized architecture-default decisions now on main.
- Updated durable docs because the run created a durable source-of-truth output:
  `docs/project_state.md` and `docs/artifact_index.md`. No decision-log update
  was needed because this run did not record a new durable architecture/policy
  decision.

Guardrails:

- No production label registries, ontologies, imports, train/test splits,
  model weights, production thresholds, or threshold values were changed.
- No labels were promoted/imported, and every candidate row has
  `countable_label_candidate = false` and `ready_for_label_import = false`.
- No heldout M-CSA row was used for training or threshold tuning.
- Mechanism text snippets, EC/Rhea row fields, labels, target names, and source
  IDs were not used as scoring/model features. EC/Rhea row fields and mechanism
  snippets are not copied into candidate-row evidence fields.
- The radical/cobalamin family-panel artifacts were inspected but not folded
  into this batch because the available rows are mostly heldout or
  secondary-probe review material rather than countable atlas-growth input.

Verification:

- `PYTHONPATH=src python -m pytest tests/test_targeted_expansion_factory.py tests/test_cli.py::CliTests::test_targeted_expansion_factory_parser_defaults -q`:
  4 passed.
- `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_targeted_expansion_factory.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_fold_augmented_family_panel_expert_import_decision_application_current_counts -q`:
  211 passed, 160 subtests passed.
- Larger touched slice
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_targeted_expansion_factory.py tests/test_geometry_artifact_regression.py -q`:
  537 passed, 216 subtests passed.
- Final full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1702 passed, 244 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Final unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1657 tests passed, with
  the same existing sklearn/SciPy deprecation warning.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, 702 curated labels.
- `PYTHONPATH=src python -m compileall -q src tests`.
- `python -m json.tool artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json >/dev/null`.
- Deterministic CLI rerun with `--created-utc 2026-06-08T04:06:45Z` reproduced
  both the JSON artifact and markdown report byte-for-byte.
- Repo-wide JSON parse: 3644 files checked, 0 parse errors.
- Repo-wide JSONL parse: 27 files and 7995 lines checked, 0 parse errors.
- Repo-wide CSV/TSV scan: 29 files and 34083 rows scanned, 0 parse errors.
- Targeted generated-row evidence audit: 703 rows checked, 0 forbidden evidence
  field payloads and 0 import/countable flag violations.
- Targeted source-hash audit: all 3 recorded factory source hashes matched.
- `git diff --check`.
- Disk guardrail: 17 GiB available.
- Non-gating exploratory repo-wide `source_artifacts` hash sweep was attempted
  but is not a valid current gate because older archived artifacts reference
  missing external worktrees and stale historical sources.

Commit/push/sync/lock status:

- Commit hash: pending until the post-handoff commit is created; final pushed
  HEAD will be reported in the automation memory and final response because a
  commit cannot contain its own final hash.
- Push/sync status: pending; will push to `origin/main` and verify
  `HEAD == origin/main`.
- Lock release status: pending; will release the canonical repo automation lock
  after clean/synced verification.

Exact next action:

Run the first-action screen input from
`artifacts/v3_targeted_expansion_factory_batch_current702_20260608.json`:
source-free current-reference duplicate search, current-countable structural
screen, external all-vs-all structural cluster assignment, UniRef-wide duplicate
screening, terminal review decision, and full label-factory gate for the 12
external `review_only_evidence` rows. Only after those gates pass should any row
approach a countable-promotion boundary.

## CE External Admission 16 Validation Run
- STARTED_AT_UTC: 2026-06-08T23:38:20Z
- STARTED_AT_LOCAL: 2026-06-08T18:38:20-0500
- Lock: `work/locks/ce_external_admission_16.lock`
- ENDED_AT_UTC: 2026-06-08T23:51:22Z
- ENDED_AT_LOCAL: 2026-06-08T18:51:22-0500
- ELAPSED_MINUTES: 13.033
- Automation ID: `ce-external-admission-16-validation`

### Result

- Built a rerunnable admission validation gate for the 16 rows in
  `artifacts/v3_external_source_ingestion_import_preview_current702_20260608.json`.
- Output artifact:
  `artifacts/v3_external_source_admission_validation_16_current702_20260608.json`.
- Admission-ready preview:
  `artifacts/v3_external_source_admission_ready_preview_current702_20260608.json`.
- Human report:
  `work/external_source_admission_validation_16_current702_20260608.md`.
- Rerunnable code/tests:
  `src/catalytic_earth/external_source_admission_validation.py`,
  CLI command `build-external-source-admission-validation-16`, and
  `tests/test_external_source_admission_validation.py`.

### Decision Summary

- All 16 import-preview rows reconcile exactly to pilot rows in
  `external_countable_preflight_candidate` state.
- All 16 pass reviewed Swiss-Prot, source-hash/provenance, exact residue
  locator, PDB/AFDB handle, Rhea/specific EC, lane-assignment, and recomputed
  exact current702 accession/sequence duplicate gates.
- Terminal states: 10
  `admission_ready_pending_coordinate_materialization`, 6
  `admission_ready_pending_locator_materialization`, 0
  `admission_ready_external_label_candidate`.
- Family/lane counts: redox oxygen/sulfur 4 pending coordinate; PLP children 3
  pending locator; glycoside/nucleoside 1 pending coordinate and 1 pending
  locator; phosphoryl transfer 2 pending coordinate and 2 pending locator;
  radical-SAM/cobalamin 3 pending coordinate.
- No row was routed to human review. The remaining work is mechanical:
  materialize/hash local coordinates for the 10 coordinate-pending rows, then
  materialize approved source-free locator sidecars for all 16 and rerun this
  validation.
- No labels were imported and no production registry/import/ontology/model/
  threshold/split surface was edited.

### Validation

- `python -m json.tool` passed for the pilot, import-preview, admission
  validation, and admission-ready preview JSON artifacts.
- Focused pytest:
  `PYTHONPATH=src python -m pytest tests/test_external_source_admission_validation.py tests/test_external_source_ingestion.py tests/test_cli.py::CliTests::test_external_source_ingestion_pilot_parser_defaults tests/test_cli.py::CliTests::test_external_source_admission_validation_parser_defaults -q`:
  4 passed.
- Full unittest:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1,676 tests passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: passed with 702
  curated mechanism labels.
- Current docs artifact-reference check passed with 0 missing references; the
  temporary check output was not kept because it is not a durable output for
  this run.
- `git diff --check`: passed.
- Production-edit guardrail scan: changed paths are limited to docs, handoff,
  validation code/tests, and the new validation/report artifacts; no production
  registry, import, ontology, model, threshold, or split path changed.
- Disk guardrail: `df -h .` reported 18 GiB free.

### Exact Next Action

Start with the six `admission_ready_pending_locator_materialization` rows
because their coordinates are already locally hash-matched:
`uniprot:Q9Y617`, `uniprot:P04181`, `uniprot:Q96255`, `uniprot:P04062`,
`uniprot:Q969G6`, and `uniprot:P32189`. Materialize approved source-free
locator sidecars from the reviewed exact residue locators, then rerun
`build-external-source-admission-validation-16`. For the other 10 rows, first
materialize or hash-match the referenced PDB/AFDB coordinates.

## CE External Bulk Ingestion Scout
- STARTED_AT_UTC: 2026-06-08T23:39:47Z
- STARTED_AT_LOCAL: 2026-06-08T18:39:47-0500
- Lock: `work/locks/ce_external_bulk_ingestion.lock`
- ENDED_AT_UTC: 2026-06-09T00:02:46Z
- ENDED_AT_LOCAL: 2026-06-08T19:02:46-0500
- ELAPSED_MINUTES: 22.983
- Automation ID: `ce-external-bulk-ingestion-scout`

### Result

- Built a rerunnable bulk scout over reviewed Swiss-Prot/UniProt metadata,
  structured residue/cofactor evidence, AFDB/PDB coordinate provenance, and
  Rhea/EC provenance.
- Output artifact:
  `artifacts/v3_external_bulk_ingestion_scout_current702_20260608.json`.
- Provisional import-preview artifact:
  `artifacts/v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json`.
- Human report:
  `work/external_bulk_ingestion_scout_current702_20260608.md`.
- Rerunnable code/tests:
  `src/catalytic_earth/external_source_ingestion.py`, CLI command
  `build-external-bulk-ingestion-scout`, `tests/test_external_source_ingestion.py`,
  and `tests/test_cli.py`.

### Decision Summary

- Candidate rows: 693 across the seven requested lanes.
- Provisional preview rows: 354, all explicitly provisional until
  `ce-external-admission-16-validation` or a scaled successor validates the
  gates.
- Terminal states: 354
  `provisional_external_countable_preflight_candidate`, 194
  `locator_ready_candidate`, 97 `coordinate_ready_pending_locator`, 39
  `blocked_duplicate_or_current_registry_conflict`, 4
  `locator_repair_candidate`, 3 `coordinate_repair_candidate`, and 2
  `hard_blocked_with_next_action`.
- Family/lane coverage: metal hydrolase, redox oxygen/sulfur, PLP children,
  glycoside/nucleoside, phosphoryl transfer, radical-SAM/cobalamin, and
  near-orphan/no-reliable-structure.
- Source retrieval failures: 0. UniProt single-query limit is recorded as 500;
  this run requested 100 records per lane, used no pagination, disabled
  EC-based Rhea fallback for runtime, and performed no coordinate downloads.
- Duplicate handling includes both current702 accession/sequence status and
  exact external-pilot accession/sequence status. Pilot overlaps are blocked as
  duplicate/current-registry conflicts.
- No labels were imported and no production registry/import/ontology/model/
  threshold/split surface was edited.

### Validation

- `python -m json.tool` passed for both bulk JSON artifacts.
- Required-row-field invariant check passed: every row has provenance,
  terminal state, duplicate status, evidence basis, blocker basis, source
  query/hash/timestamp, and next action.
- Focused pytest:
  `PYTHONPATH=src python -m pytest tests/test_external_source_ingestion.py tests/test_external_source_admission_validation.py tests/test_cli.py::CliTests::test_external_source_ingestion_pilot_parser_defaults tests/test_cli.py::CliTests::test_external_source_admission_validation_parser_defaults tests/test_cli.py::CliTests::test_external_bulk_ingestion_scout_parser_defaults -q`:
  6 passed.
- Full unittest:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1,678 tests passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: passed with 702
  curated mechanism labels.
- Current docs artifact-reference check passed with 0 missing references; the
  temporary check output was not kept because it is not durable for this run.
- `git diff --check`: passed.
- Production-edit guardrail scan: changed paths are limited to docs, handoff,
  ingestion code/tests, and the new scout/report artifacts; no production
  registry, import, ontology, model, threshold, or split path changed.
- Disk guardrail: `df -h .` reported 18 GiB free.

### Exact Next Action

Run a scaled admission-validation lane over a small representative slice from
the 354 provisional preview rows before any production import discussion. Start
with rows that have experimental PDB provenance and exact reviewed locators,
then expand only after coordinate materialization, locator sidecars, structural
duplicate screening, label-factory gates, and explicit production authorization
all pass.
