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
679 countable labels. Review-state registries preserve pending
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

As of the 2026-05-16T05:45:22Z run, do not resume M-CSA strict
Foldseek/TM-score repair. The loop is closed/deferred by
`artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json`, with
`full_tm_score_holdout_claim_permitted=false`, max all-materializable
train/test TM-score `0.9749`, 4,715 target-violating train/test rows,
108 high-TM partition constraints, and 38 sequence-identity partition
constraints. The three recovered index-145 target-shard artifacts are
review-only non-canonical context, not a continuation target.

Next direct work should resume the external structural pilot: classify the 10
selected candidates through broader duplicate screening, representation-control
review, review decisions, and full label-factory readiness. The first
review-only external strict-TM path artifact is
`artifacts/v3_external_structural_tm_holdout_path_1025.json`; it covers the 10
selected pilot rows, requires structure clustering before split assignment, and
keeps 0 countable/import-ready rows. Do not open M-CSA round33, staged index
145 continuation, or more partition repair unless the user explicitly reverses
the override.

## Start-of-Run Confidence Call

Recorded for the 2026-05-16T05:47:16Z run after recovering a stale directory
lock whose recorded PID (`33199`) was no longer alive, confirming the worktree
was clean, syncing clean `origin/main`, and passing startup gates (`426` unit
tests passed and `validate` passed with 679 curated labels):

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

- Curated label registry: 679 bronze automation-curated labels, with 212
  seed-fingerprint positives and 467 out-of-scope labels.
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
current-reference backend search debt for the 28 no-signal rows while broader
UniRef-wide/all-vs-all duplicate screening remains a limitation before import.
The bounded alignment verification
checks 90 top-hit pairs, confirms `O15527` and `P42126` as exact holdouts, and
records 88 no-signal pairs. The import-readiness audit keeps 0 rows ready for
label import and records 10 active-site gaps, 2 exact sequence holdouts, 9
heuristic scope/top1 mismatches, 29 representation-control issues, broader
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
