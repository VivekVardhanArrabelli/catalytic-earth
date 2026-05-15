# External Source Transfer

The 1,025 preview shows that M-CSA-only tranche growth is no longer the right
path to 10,000 countable labels. The current M-CSA slice exposes 1,003 source
records, while the benchmark target is 10,000 countable labels. External-source
transfer is therefore a new methodology, not a continuation of M-CSA label
import.

## Current State

- Canonical countable labels remain at 679.
- The 1,025 preview passes 21/21 label-factory gates but adds 0 clean countable
  labels.
- All 329 preview review-state rows remain non-countable.
- External UniProtKB/Swiss-Prot artifacts are review-only and create 0
  countable label candidates.
- The first read-only external sample has 30 candidates across six query lanes,
  0 fetch failures, and a clean non-countable guardrail audit.
- The external candidate manifest attaches OOD controls, heuristic-control
  requirements, and exact-reference sequence-cluster controls to those 30
  candidates. Two candidates (`O15527` and `P42126`) overlap existing M-CSA
  reference accessions and are routed to holdout controls, not count growth.
  The lane-balance audit is clean: six lanes have five candidates each, so the
  first external sample has not collapsed to one chemistry.
- The external evidence plan/export requests active-site residue evidence,
  curated mechanism/reaction evidence, structure mapping, OOD assignment,
  sequence holdout checks, heuristic retrieval controls, review decisions, and
  full factory gates for every candidate while carrying the sampled PDB and
  AlphaFold structure references forward. It flags seven candidates with broad
  or incomplete EC context, defers three broad-only candidates for specific
  reaction disambiguation, and exports a review-only active-site evidence queue
  with 25 ready candidates and five deferred candidates.

## Immediate Pilot Direction

The next phase is a small external-source import pilot, not more abstract gate
accumulation. New gates or audits should be added only when they directly
remove one blocker to pilot import readiness.

The first real sequence-distance holdout evaluation now exists for the accepted
countable registry and both the 1,000 and 1,025 slice contexts:
`artifacts/v3_sequence_distance_holdout_eval_1000.json` and
`artifacts/v3_sequence_distance_holdout_eval_1025.json`. The current artifacts
use MMseqs2 (`18-8cc5c`) with 30% sequence identity and 80% coverage over the
sidecar FASTA
`artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta`, cover
678/678 evaluated labels, cluster 738 sequence records, and hold out 136 rows
by whole sequence clusters. The max observed train/test identity is `0.284`,
so the <=30% target is achieved. Held-out metrics are reported separately from
in-distribution metrics: 44 held-out in-scope rows, 92 held-out out-of-scope
rows, 0 held-out out-of-scope false non-abstentions, and held-out evaluable
top1 accuracy, top3 retained accuracy, and retention all at `1.0000`. The
metadata now includes explicit backend, resolved binary path, cluster-threshold,
target-achievement, and limitation aliases; the deterministic low-neighborhood
proxy fields remain as fallback context.
Full Foldseek/TM-score separation remains uncomputed, but the
coordinate-readiness blocker is now narrower.
`artifacts/v3_foldseek_coordinate_readiness_1000.json`
records the explicit Foldseek binary/version
(`/private/tmp/catalytic-foldseek-env/bin/foldseek`, `10.941cd33`), identifies
678 evaluated accepted-registry rows, finds 676 rows with supported selected
PDB coordinates, flags `m_csa:372` and `m_csa:501` as missing selected
structures, and stages a capped 25-PDB sidecar under
`artifacts/v3_foldseek_coordinates_1000/`. The artifact is review-only,
non-countable, and keeps `tm_score_split_computed=false`.
`artifacts/v3_foldseek_tm_score_signal_1000_staged25.json` then runs a bounded
all-vs-all Foldseek `easy-search` over only that staged sidecar. It records
1,840 pair rows, maps all rows back to the 25 staged structures and entry ids,
finds 532 staged heldout/in-distribution pair rows, and reports max observed
staged train/test TM signal `0.6426` against the `<0.7` target. This is partial
staged-coordinate review evidence only: it adds 0 countable/import-ready rows
and keeps both `tm_score_split_computed=false` and
`full_tm_score_split_computed=false`.
`artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json` expands the
coordinate sidecar to 100 selected PDB structures with 0 fetch failures and 572
supported structures still unstaged behind the deterministic cap. The companion
expanded40 Foldseek signal in
`artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json` is now completed
as a partial staged-coordinate run over the capped selected-coordinate search
directory: 5,699 pair rows, all 5,699 safely mapped rows, 1,633
heldout/in-distribution train/test pairs, max observed train/test TM score
`0.7515`, 0 unmapped raw Foldseek names, and 0 countable/import-ready rows. It
removes the staged25-only proof blocker and the expanded40 raw-name mapping
blocker, but it remains review-only, non-countable, and not import-ready. The
full TM-score split is still false, and the `<0.7` target is not achieved on
this partial signal.
`artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`
stages all currently materializable supported selected coordinates for the
accepted 1,000 context: 672 unique selected PDB mmCIF sidecars, 676
materializable evaluated rows, 0 fetch failures, and 0 supported selected
structures left unstaged. It now explicitly excludes `m_csa:372` and
`m_csa:501` from Foldseek coordinate materialization because both rows have
`geometry_status=no_structure_positions` and no selected structure id in the
current graph/geometry/sequence-holdout evidence. This removes the unstaged selected-coordinate
sidecar blocker. `artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json`
then completes the next bounded Foldseek signal from that all-materializable
sidecar with a 100-coordinate cap and prior staged count 80: 27,542 mapped pair
rows, 7,317 heldout/in-distribution train/test pairs, max observed train/test
TM score `0.7515`, 0 unmapped raw Foldseek names, and 0
countable/import-ready rows. It removes the expanded80 partial-signal ceiling
but remains review-only and non-countable. The `<0.7` target is not achieved on
the computed subset, the cap leaves 572 staged coordinates uncomputed, and no
uncapped full split/signal has completed. The coordinate exclusions must remain
reported before any full TM-score holdout claim.
`artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json` now records
the exact current-split target blocker from that signal: one unique
train/test structure pair, `m_csa:33`/`m_csa:34` (`pdb:1JC5`/`pdb:1MPY`),
drives 48 chain-level rows at or above the `<0.7` threshold, with max pair
TM-score `0.7515`. This keeps the full TM-score holdout claim forbidden and
makes the next generalization task split repair/exclusion review, not just a
larger capped run.
`artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json` now completes
that first split-repair review step without applying it: the observed blocker
has one conservative repair candidate, moving the held-out out-of-scope row
`m_csa:34` to in-distribution before regenerating holdout metrics. The
projected held-out count is 135, held-out in-scope rows remain 44, observed
blocking pairs drop to 0 under the plan, and every field remains
review-only/non-countable. Full TM-score holdout claims remain forbidden until
the repair is applied, sequence-holdout metrics are regenerated, and an
uncapped Foldseek-backed split passes.
`artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json` then
projects the planned move over the existing expanded100 Foldseek rows without
rerunning Foldseek. The projection lowers observed train/test violations from
48 to 0 and the computed-subset max train/test TM-score from `0.7515` to
`0.6993`, but it remains non-claiming because the repair is not applied, the
sequence holdout is not regenerated, and the source signal is still capped.
`artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json`
applies the same move to a candidate copy of the sequence holdout. The repaired
candidate has 135 held-out rows, 44 held-out in-scope rows, 0 held-out
out-of-scope false non-abstentions, and no remaining held-out overlap with the
moved `mmseqs30:m_csa:34` cluster. It does not replace the canonical sequence
holdout. The downstream repaired-coordinate view now exists:
`artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json`
uses that candidate holdout, keeps all 672 currently materialized coordinates
staged, moves `m_csa:34` to in-distribution, and preserves the explicit
coordinate exclusions for `m_csa:372` and `m_csa:501`. The actual repaired
expanded100 Foldseek rerun in
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json`
uses the same 100-coordinate cap and Foldseek `10.941cd33`, maps 27,542 pair
rows, evaluates 6,930 heldout/in-distribution train/test pairs, and records max
train/test TM-score `0.6993`. The companion target audit
`artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json`
finds 0 target-violating pairs. This removes the projection-only blocker for
the computed subset, but remains review-only and non-countable: the canonical
sequence holdout is unchanged, 572 staged coordinates remain outside the capped
signal, two selected rows remain coordinate exclusions, and no full
TM-score-holdout claim is permitted.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`
then completes a staged all-materializable Foldseek signal over all 672
materializable selected coordinates with Foldseek `10.941cd33` and
`--threads 4`. It maps 952,922 pair rows and 274,241 train/test rows, but the
computed subset fails the `<0.7` target with max train/test TM-score `0.9749`
and 4,715 target-violating train/test rows. This removes the previous
all-materializable runtime ambiguity but remains review-only and non-countable:
`m_csa:372` and `m_csa:501` stay coordinate exclusions, the artifact is a
signal rather than a canonical full split, and
`full_tm_score_holdout_claim_permitted=false`.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json`
and
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json`
replace the all-at-once-only runtime path with the first two direct resumable
query chunks: 24 query coordinates searched against all 672 staged
materializable target coordinates with Foldseek `10.941cd33`, `--threads 4`,
and a 900-second bound per chunk. They complete with 28,251 mapped pair rows,
9,142 train/test rows, max train/test TM-score `0.8957`, 11 target-violating
rows across six unique structure pairs in chunk 0, and 59 target-violating rows
across seven unique structure pairs in chunk 1. These artifacts are
review-only, non-countable, not import-ready, and still only chunks 1-2/56.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json`
then attempts chunk 2 with the same command shape and times out at 900 seconds
before pair rows are emitted. The aggregate
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_of_056.json`
records 3 attempted chunks, 2 completed chunks, 24 completed query
coordinates, 28,251 mapped pair rows, 9,142 train/test rows, max train/test
TM-score `0.8957`, 70 target-violating row-level pairs, 13 reported violating
structure pairs, and 54 non-completed chunks. This removes the first
chunk-aggregation ambiguity and the single-run runtime SPOF but adds two
concrete blockers before any full TM-score claim: the completed chunks fail
the `<0.7` target and chunk 2 exceeds the routine 900-second bound.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json`
then retries the same chunk directly with a 1,800-second cap and completes:
12 query coordinates, 12,639 mapped pair rows, 3,216 train/test rows, max
train/test TM-score `0.8427`, and 6 target-violating row-level pairs across 2
reported structure pairs. The completed-retry aggregate
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json`
now records 3/56 completed chunks, 36 completed query coordinates, 40,890
mapped pair rows, 12,358 train/test rows, max train/test TM-score `0.8957`, 76
target-violating row-level pairs, 15 reported violating structure pairs, and
53 non-completed chunks. The query-chunk split-repair plan
`artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json`
classifies the 15 observed blockers into 9 conservative held-out out-of-scope
repair candidates and 6 manual split-redesign blockers involving held-out
in-scope rows (`m_csa:20`, `m_csa:497`, and `m_csa:895`).
`artifacts/v3_sequence_distance_holdout_split_redesign_candidate_1000.json`
tries the corresponding review-only split redesign while preserving those
held-out in-scope rows. It resolves the 15 observed blockers in projection, but
the direct redesigned Foldseek chunk
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_000_of_056.json`
still fails the `<0.7` target: 16,475 mapped rows, 6,909 train/test rows, max
train/test TM-score `0.926`, and 15 target-violating row-level pairs across 4
reported structure pairs. The repair plan
`artifacts/v3_foldseek_tm_score_split_redesign_candidate_query_chunk_repair_plan_1000.json`
identifies the new blocker as held-out in-scope `m_csa:6` against
`m_csa:277`, `m_csa:378`, `m_csa:320`, and `m_csa:108`. These artifacts remain
review-only with 0 countable/import-ready rows.
`artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round2_1000.json`
then moves those four high-TM neighbors into heldout in a second review-only
candidate. The direct round-2 chunk
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_000_of_056.json`
clears chunk 0 with 16,475 mapped rows, 6,939 train/test rows, max train/test
TM-score `0.695`, and 0 target-violating pairs. Its aggregate covers only
1/56 redesigned chunks, so this removes the chunk-0 blocker but not the full
TM-score holdout blocker.
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_001_of_056.json`
then completes chunk 1 and fails the `<0.7` target with 11,776 mapped rows,
4,154 train/test rows, max train/test TM-score `0.8182`, and 12
target-violating row-level pairs across 4 reported structure pairs. The
round-2 repair plan
`artifacts/v3_foldseek_tm_score_split_redesign_candidate_round2_query_chunk_repair_plan_1000.json`
finds no conservative out-of-scope repair candidate and classifies the blocker
as held-out in-scope `m_csa:15`/`m_csa:16` versus train neighbors
`m_csa:258`/`m_csa:157`. The round-3 review-only redesign
`artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round3_1000.json`
moves `m_csa:157` and `m_csa:258` to heldout, preserves 0 sequence-cluster
splits, increases heldout rows to 138, and keeps 0 held-out out-of-scope false
non-abstentions. Its direct chunk aggregate
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_002_of_056.json`
covers chunks 0-2/56 with 36 query coordinates, 40,890 mapped rows, 13,472
train/test rows, max train/test TM-score `0.695`, and 0 target-violating
pairs. This removes the first three query-chunk blockers only; 53 chunks remain
uncomputed. Chunk 3 then times out under the standard 900-second bound before
pair rows are emitted, and
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_003_of_056.json`
keeps that timeout visible while preserving completed-chunk max train/test
TM-score `0.695`. The full split remains blocked by the chunk-3 runtime
blocker, 53 uncomputed chunks, two coordinate exclusions, and candidate-only
split status; no full TM-score holdout claim is permitted.
The active replacement path is now cluster-first rather than blind 56-chunk
continuation. `artifacts/v3_foldseek_tm_score_cluster_first_split_1000.json`
uses the 672 staged materializable structures as the structure index and
turns observed `TM >= 0.7` pairs into 24 partition constraints across 12
constrained clusters, resolving those known constraints in projection with 0
sequence-cluster splits. Verification subchunk 006 first exposed a new
`m_csa:38`/`m_csa:118` blocker at max TM-score `0.7435`; the round-2
cluster-first candidate moves held-out out-of-scope `m_csa:118` to
in-distribution and the same subchunk then passes with max TM-score `0.6509`
and 0 violations. Subchunk 007 under round 2 fails with max TM-score `0.8651`,
16 violating rows, and 9 reported blocking structure pairs. The current
cluster-first handoff artifact,
`artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json`, folds
those blockers back into the split and records 34 high-TM constraints, 14
constrained clusters, 0 projected violations, 0 sequence-cluster splits, and
0 countable/import-ready rows. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json`.
Direct round-3 verification of subchunks 006 and 007 then passes subchunk 006
at max train/test TM-score `0.6509` but exposes one remaining subchunk-007
blocker, `m_csa:45` versus held-out out-of-scope `m_csa:397`, at max
train/test TM-score `0.8043`. Round 4 folds that blocker into 35 high-TM
constraints, moves `m_csa:397` to in-distribution, and clears subchunk 007 at
max train/test TM-score `0.6598`. Round-4 subchunk 008 then exposes
`m_csa:54` versus held-out out-of-scope `m_csa:428` at max TM-score `0.7205`.
The round-5 candidate folds that pair into 36 high-TM constraints, moves
`m_csa:428` to in-distribution, and clears subchunk 008 at max TM-score
`0.6989`. Round-5 subchunk 009 then exposes `m_csa:58` versus held-out
out-of-scope `m_csa:628` at max TM-score `0.879`. The current round-6
cluster-first artifact,
`artifacts/v3_foldseek_tm_score_cluster_first_split_round6_1000.json`, folds
that blocker into 37 high-TM constraints, moves `m_csa:628` to
in-distribution, preserves 0 sequence-cluster splits, and records 0
countable/import-ready rows. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round6.json`,
and the direct round-6 subchunk-009 rerun passes with max train/test TM-score
`0.6699` and 0 target-violating pairs. Round-6 subchunk 010 then times out
under the 900-second bound before emitting pair rows. Splitting that same
window into 3-query microchunks localizes a completed target failure:
microchunk 020 (`m_csa:61`-`m_csa:63`) records 7,488 mapped rows, max
train/test TM-score `0.7116`, and one reported blocking structure pair,
`m_csa:63`/`m_csa:188`. The current round-7 artifact,
`artifacts/v3_foldseek_tm_score_cluster_first_split_round7_1000.json`, folds
that pair into 38 high-TM constraints across 17 constrained clusters,
preserves 0 sequence-cluster splits, and records 0 countable/import-ready rows.
Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round7.json`.
The direct round-7 microchunk-020 rerun times out under the 900-second bound
before emitting pair rows. Single-query isolation resolves that runtime blocker:
indices 60-62 (`m_csa:61`-`m_csa:63`) complete with 7,488 mapped rows, 1,311
train/test rows, max train/test TM-score `0.6967`, and 0 violations, and
indices 63-65 (`m_csa:64`-`m_csa:66`) complete with 2,190 mapped rows, 378
train/test rows, max train/test TM-score `0.5629`, and 0 violations. Staged
index 66 (`m_csa:67`) also passes at max TM-score `0.6535`, but staged index
67 (`m_csa:68`) exposes a `m_csa:68`/`m_csa:750` blocker at max TM-score
`0.7909`; round 8 folds that pair into 39 constraints, 18 constrained
clusters, 0 projected violations, and 0 sequence-cluster splits. Direct
round-8 single-query verification then clears staged indices 68-78, but staged
index 79 exposes held-out out-of-scope `m_csa:80` against in-distribution
`m_csa:408` and `m_csa:569` at max TM-score `0.8726`; round 9 folds those
pairs into 41 constraints, 19 constrained clusters, 0 projected violations, and
0 sequence-cluster splits. The round-9 rerun of staged index 79 plus staged
indices 80-83 passes in aggregate at max TM-score `0.6477` with 0
target-violating pairs. The next round-9 single-query batch clears staged
indices 84-95 with 17,189 mapped rows, 3,257 train/test rows, max train/test
TM-score `0.6579`, and 0 target-violating pairs. The next batch clears staged
indices 96-101 before staged index 102 exposes `m_csa:103`/`pdb:1VAO` versus
held-out `m_csa:115`/`pdb:1W1O` at max TM-score `0.7653`. The cluster-first
builder now unions real sequence-identity clusters before assigning structural
components; round 10 folds that blocker into 42 high-TM constraints plus 38
sequence-identity partition constraints, preserves 0 sequence-cluster splits,
and reruns staged index 102 cleanly at max train/test TM-score `0.6725` with 0
target-violating pairs. Staged index 103 then exposes `m_csa:104` against
`m_csa:686` at max `0.7633`; round 11 folds that in but still exposes
`m_csa:104` against `m_csa:360` and `m_csa:740` at max `0.7317`. Round 12
folds those blockers and clears index 103 at max `0.6669`, then index 104
passes at max `0.4496` before index 105 exposes a larger high-TM blocker
surface at max `0.8862`. Round 13 folds that evidence into 48 high-TM
constraints, 38 sequence-identity partition constraints, 0 projected
violations, and 0 sequence-cluster splits. Round-13 verification clears
indices 105-106, then index 107 exposes `m_csa:108` at max `0.8826`; round 14
folds that surface and reruns index 107 cleanly at max `0.6862`. Index 108
then exposes `m_csa:109` at max `0.7649`; round 15 folds those blockers,
verifies indices 107-109 cleanly at max `0.6996`, and index 110 exposes
`m_csa:111` at max `0.7521`. Round 16 folds that evidence into 66 high-TM
constraints plus 38 sequence-identity partition constraints, with 0 projected
violations, 0 sequence-cluster splits, and readiness staged for the next direct
rerun of index 110. Full TM-score holdout claims remain forbidden until the
remaining round-16 cluster-first coverage passes or is explicitly adjudicated.
Foldseek itself is now available in the isolated temporary environment
`/private/tmp/catalytic-foldseek-env` (`foldseek version` reports
`10.941cd33`). A TM-score split remains blocked until the remaining query
chunks are completed or explicitly adjudicated under the cluster-first round-13
split, coordinate exclusions remain reported, and target checks pass.

Build toward a 5-10 candidate pilot from the existing 30-row UniProtKB/Swiss-Prot
sample. Keep every external row review-only until active-site, reaction,
sequence, representation, review, and full label-factory gates pass.

Priority blockers:

- use the 12-row ESM-2 learned-vs-heuristic disagreement sample and the
  review-only pilot priority artifact to drive pilot review decisions and
  representation repair;
- source explicit catalytic or active-site residue evidence for the 10
  active-site-feature gap rows;
- treat the bounded current-reference MMseqs2 sequence search as complete for
  the 28 no-signal rows, while still requiring broader UniRef-wide/all-vs-all
  duplicate screening before import;
- advance the 10 selected pilot-priority candidates with explicit active-site
  evidence, specific reaction evidence, clean sequence holdout status, clean
  structure mapping, non-collapsed retrieval/representation behavior, and no
  broad-EC ambiguity;
- fill the no-decision review packets for those pilot candidates only after
  evidence assembly, and before any countable import attempt.
- `artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json`
  now classifies the 10 selected pilot rows as review-only active-site evidence
  decisions: 7 have explicit active-site source evidence, 3 have binding
  context only, 0 are countable, and 0 are import-ready. This removes the
  pilot source-status ambiguity blocker, but every selected row still requires
  broader duplicate screening, representation-control review, a completed
  review decision, and the full label-factory gate before import.
- `artifacts/v3_external_source_pilot_success_criteria_1025.json` defines the
  pilot success bar rather than treating evidence assembly as completion.
  Operational success means all 10 selected rows reach terminal decisions with
  no unresolved process blockers. Scientific/import success means at least 1
  row becomes import-ready under full gates, or a zero-pass outcome where every
  failure is evidence-explained rather than process-missing. The current status
  is `needs_more_work`: 0 terminal decisions, 0 import-ready rows, 0 countable
  candidates, 3 unresolved active-site-source rows, 10 broader-duplicate
  screening blockers, 3 unresolved representation-control stability-change
  rows after selected-pilot adjudication, and 10 full-gate blockers.
- `artifacts/v3_external_source_pilot_representation_adjudication_1025.json`
  consumes the selected-pilot 8M-vs-largest-feasible ESM-2 stability audit and
  keeps all 10 rows review-only: 3 are stable review-only representation
  controls, 4 are representation near-duplicate holdouts, and 3 require review
  because nearest-reference evidence changed under the 150M fallback. The
  requested 650M backend remains not cached, so this removes generic
  representation-process ambiguity without claiming 650M completion or import
  readiness.
- The active-site evidence pass now samples all 25 ready candidates from
  UniProtKB feature records. It finds active-site features for 15 candidates,
  leaves 10 candidates as active-site-feature gaps, and keeps all rows
  non-countable. A heuristic-control queue then identifies 12 candidates ready
  for structure mapping and defers 13 rows, including 3 broad-EC rows.
- The structure-mapping sample now covers all 12 heuristic-ready external
  candidates on current AlphaFold model CIFs, resolves all requested active-site
  positions, and runs the current geometry-retrieval heuristic as a control.
  That heuristic now carries a text-free scoring policy: mechanism text, source
  labels, EC/Rhea identifiers, and target labels are review context only, while
  the PLP-specific positive signal comes from local ligand-anchor evidence.
  The control is intentionally not a label decision: 9/12 scored candidates
  rank `metal_dependent_hydrolase` top1, 2 rank `heme_peroxidase_oxidase`, and
  1 ranks `flavin_dehydrogenase_reductase`. The failure-mode audit records
  active-site feature gaps, broad-EC disambiguation needs, top1 fingerprint
  collapse, metal-hydrolase collapse, and 9 scope/top1 mismatches as review-only
  blockers to label import.
- The external control repair plan converts the current failures into 25
  non-countable repair rows: 10 active-site feature gaps, 3 broad-EC
  disambiguation rows, and 12 heuristic-control repair rows. The representation
  control manifest exposes all 12 mapped controls for future learned or
  structure-language scoring while keeping `embedding_status` as
  `not_computed_interface_only`. The feature-proxy representation comparison
  keeps embeddings uncomputed, flags 7 metal-hydrolase collapse rows, records
  2 glycan-boundary cases, and leaves every row non-countable.
- The binding-context repair path splits the 10 active-site feature gaps into
  7 rows with binding context ready to map and 3 rows without binding context.
  The binding-context mapping sample maps 7/7 ready rows with 0 fetch failures,
  but binding positions remain repair context only and do not replace
  catalytic active-site evidence. The active-site gap source-request artifact
  turns all 10 gaps into explicit review-only sourcing tasks; 7 have mapped
  binding context and 3 need curated residue sources.
- The reaction-context pass now queries Rhea for all 30 external candidates,
  finds 64 reaction records with 0 fetch failures, and keeps every row
  `reaction_context_only` and non-countable because the Rhea rows have not been
  converted into a reviewed decision artifact or full label-factory gate. Its
  guardrail audit is clean and flags 16 broad-EC context rows across
  `1.1.1.-`, `1.11.1.-`, `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and
  `4.2.99.-`. The broad-EC disambiguation audit finds specific reaction
  context for all 3 broad-only repair rows while keeping them review-only.
- The sequence-holdout audit keeps `O15527` and `P42126` as exact M-CSA
  reference-overlap holdouts and scopes duplicate-screening controls for the
  remaining 28 candidates. The sequence-neighborhood plan converts those into
  2 exact-holdout rows and 28 sequence-search control rows. The bounded
  sequence-neighborhood screen fetches all 30 external sequences and all 735
  current countable M-CSA reference accessions after resolving inactive
  demerged UniProt references `P03176` and `Q05489` to their replacement
  accessions. The current-reference screen audit now clears the
  current-reference near-duplicate blocker: 28 rows have top-hit alignments
  with no near-duplicate signal and the two exact-reference rows remain
  holdouts. `artifacts/v3_external_source_backend_sequence_search_1025.json`
  upgrades that bounded screen to a real MMseqs2 18-8cc5c backend search over
  the 30 external rows against 735 current reference accessions / 737 sequence
  records. It preserves exact holdouts `O15527` and `P42126`, records 28
  no-signal rows, 0 near-duplicate rows, and 0 failures, and keeps every row
  review-only, non-countable, and not import-ready. This removes the bounded
  current-reference backend sequence-search debt for the 28 no-signal rows,
  but broader UniRef-wide/all-vs-all duplicate screening remains mandatory
  before import. The bounded top-hit alignment verification checks 90
  sequence-neighborhood pairs, confirms the two exact-reference holdouts by
  alignment, and finds 88 no-signal top-hit pairs.
- The import-readiness audit aggregates the current blockers by candidate: 10
  active-site gaps, 2 exact sequence holdouts, 9 heuristic scope/top1
  mismatches, 29 representation-control issues, and the remaining broader
  duplicate-screening limitation. It keeps 0 rows import-ready. The active-site
  sourcing queue turns the 10 active-site gaps into 7 mapped-binding-context
  sourcing rows and 3 primary-source rows, and the active-site sourcing export
  packages 72 source targets without decisions. The active-site sourcing
  resolution re-checks all 10 active-site-gap rows against UniProt feature
  evidence, finds 0 explicit active-site residue sources, and leaves the rows
  non-countable. The sequence-search export plus backend search keep all 30
  candidates in no-decision sequence controls: 28 bounded current-reference
  no-signal rows, 2 exact sequence holdouts, and broader duplicate screening
  still pending.
  The representation-backend plan covers 12 mapped controls without computing
  embeddings. `artifacts/v3_external_source_kmer_representation_backend_sample_1025.json`
  preserves the deterministic k-mer baseline/proxy, while the canonical
  `artifacts/v3_external_source_representation_backend_sample_1025.json`
  computes the 12-row ESM-2 sample. The transfer blocker matrix joins all 30
  candidates into a review-only next-action worklist and carries the
  resolution/sample row evidence directly: 7 rows move to literature/PDB
  active-site review, 3 remain primary active-site source tasks, 9 require
  select/run real representation-backend actions, 6 require compute/attach
  representation-control actions, 3 stay representation-near-duplicate holdouts, and 2 stay
  sequence holdouts. Its dominant next-action fraction is 0.3000 and dominant
  lane fraction is 0.1667, so the queue has not collapsed to one action or
  chemistry lane. The external transfer gate now directly checks the
  current-reference sequence screen audit and backend sequence-search artifact.
  It passes 68/68 review-only checks, including selected-pilot representation
  sample coverage and active-site evidence decisions, and remains not ready for
  label import.
- The learned representation backend path now has a computed 12-row ESM-2
  sample in `artifacts/v3_external_source_representation_backend_sample_1025.json`
  plus a clean review-only audit. It uses `facebook/esm2_t6_8M_UR50D`,
  records 320-dimensional embeddings, keeps all rows non-countable and not
  import-ready, flags 3 representation-near-duplicate holdouts, and emits 12
  learned-vs-heuristic disagreement rows for active-learning priority. The
  sample now declares `sequence_embedding_cosine` and `sequence_length_coverage`
  as the only predictive representation feature sources. Heuristic fingerprint
  ids, matched M-CSA reference ids, and source scope signals are carried with
  explicit leakage flags as review or holdout context only. The audit now also
  fails if EC/Rhea identifiers, mechanism text, source labels, fingerprint ids,
  or source-target identifiers appear as predictive feature sources. The
  heuristic geometry retrieval remains the required baseline control.
- The representation backend now supports larger ESM-2 model identifiers,
  including `facebook/esm2_t33_650M_UR50D`, without replacing the computed 8M
  baseline. The current 650M sidecar artifacts for mapped controls and pilot
  rows were run in local-only mode and record `model_unavailable_locally`
  because the 650M weights were not cached. They still provide explicit
  expected dimension `1280`, elapsed time, embedding failures, and 8M-vs-650M
  stability audits as review-only feasibility evidence.
- The transfer blocker matrix audit now performs a row-level candidate-manifest
  lineage check. A matrix built from a stale or mismatched manifest fails with
  `external_transfer_blocker_matrix_candidate_lineage_mismatch` instead of
  passing because high-level candidate counts happen to match. The matrix
  builder now also validates artifact-path and payload slice lineage across the
  candidate manifest, import-readiness audit, active-site sourcing export and
  resolution, sequence-search export, and representation backend plan/sample
  before writing a matrix, and records
  `artifact_graph_consistency_for_external_blocker_matrix` in metadata.
- The external transfer gate now performs its own candidate-lineage and
  artifact-path lineage checks across high-fan-in external artifacts through
  `ExternalSourceTransferGateInputs.v1` plus a shared candidate-lineage
  artifact registry. The CLI command builds that typed contract from its
  artifact map before calling the gate, avoiding another one-off keyword
  cascade, and the contract rejects non-object artifact payloads before gate
  checks run. Evidence plans, review exports, sequence
  controls, active-site sourcing packets, representation samples, and blocker
  matrices fail the gate if they carry accessions outside the candidate manifest
  or claim full 30-row coverage while silently dropping manifest rows. The
  current lineage check also includes the sequence-holdout audit, pilot-priority,
  no-decision pilot review export, pilot evidence-packet, and pilot
  evidence-dossier artifacts, and fails fast if supplied artifact paths mix
  source slices such as 1,000 and 1,025. It also fails if those pilot artifacts
  stop being review-only, non-countable, no-decision work products.
  The import-readiness audit, pilot evidence-packet builder, and pilot dossier
  builder now use the same artifact-path lineage validator before writing their
  artifacts and record the checked lineage under `metadata.artifact_lineage`.
- `artifacts/v3_external_source_pilot_candidate_priority_1025.json` ranks the
  30 external candidates for a bounded review pilot. It selects 10
  non-countable candidates across the external lanes, defers 5 exact-holdout or
  near-duplicate rows, and records `external_pilot_candidate_ranking` as the
  blocker removed. Its leakage policy explicitly excludes mechanism text,
  EC/Rhea ids, source labels, and target labels from priority scoring. The
  worklist is review context only: selected rows still require active-site
  evidence, reaction/mechanism review, complete
  near-duplicate sequence search, leakage-safe representation controls, review
  decisions, and full label-factory gates before any import attempt.
- `artifacts/v3_external_source_pilot_review_decision_export_1025.json` exports
  those 10 selected rows as no-decision review packets. It records 0 completed
  decisions, 0 countable candidates, and `ready_for_label_import=false`; the
  artifact removes only the review-packet scaffolding blocker.
- `artifacts/v3_external_source_pilot_evidence_packet_1025.json` consolidates
  sequence-search and active-site source targets for the same 10 selected rows.
  It records 79 source targets, all 10 sequence-search packets, 3 active-site
  sourcing packets, 10 backend sequence-search packets with no-near-duplicate
  status, 0 missing required source packets, and `guardrail_clean=true`; it
  removes only the source-packet consolidation blocker and does not authorize
  import. Its metadata now also records clean 1,025 artifact lineage for the
  pilot priority list, active-site sourcing export, sequence-search export, and
  backend sequence-search artifact.
- `artifacts/v3_external_source_pilot_representation_backend_plan_1025.json`
  and `artifacts/v3_external_source_pilot_representation_backend_sample_1025.json`
  extend leakage-safe sequence representation controls to all 10 selected pilot
  rows. The ESM-2 sample computes 320-dimensional embeddings, keeps every row
  review-only and non-countable, and flags `P55263` as a representation
  near-duplicate holdout.
- `artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json`
  and its audit/stability sidecars attempt the 650M upgrade for those same
  selected pilot rows in local-only mode after a bounded 150M feasibility run.
  The 650M weights are not cached, and the current machine had only about 3.2
  GiB free for a 2.61 GB remote 650M weight file with CPU-only inference, so the
  sidecars record the 650M cache miss, use cached
  `facebook/esm2_t30_150M_UR50D` as the largest feasible fallback, and mark
  `requested_650m_or_larger_representation_backend_not_computed`; they remain
  review-only feasibility/control evidence and do not replace a real 650M
  control.
- `artifacts/v3_external_source_pilot_evidence_dossiers_1025.json` assembles
  the same 10 selected rows into per-candidate review dossiers. It records 7
  candidates with explicit UniProt active-site feature support, all 10 with
  Rhea reaction context, all 10 with pilot representation-sample rows, and 10
  with remaining blockers; it is review-only and does not authorize import.
  Dossier assembly now adds local blockers for missing explicit active-site evidence,
  missing specific reaction context, and near-duplicate sequence alerts instead
  of relying only on upstream blocker lists. The current selected pilot has 3
  local explicit-active-site evidence blockers and 0 missing-specific-reaction
  blockers. The dossier sequence summaries carry the backend no-signal status
  for all 10 selected rows and no longer retain stale complete-near-duplicate
  blockers for those rows. Its metadata records clean 1,025 lineage across the
  packet, active-site, reaction, sequence, representation, heuristic, structure,
  blocker-matrix, and import-readiness inputs.
- `artifacts/v3_external_source_pilot_success_criteria_1025.json` converts the
  selected-pilot work into measurable review-only criteria. It records 10
  selected candidates, 0 terminal review decisions, 0 import-ready rows, 0
  countable label candidates, the explicit active-site split of 7 resolved and
  3 unresolved rows, broader duplicate screening still required for all 10,
  representation-control adjudication still unresolved for 9 rows, and full
  label-factory gates not run for all 10. Its current `pilot_status` is
  `needs_more_work`.

## Artifacts

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-source-scale-limits \
  --graph artifacts/v1_graph_1025.json \
  --prior-graph artifacts/v1_graph_1000.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --review-debt artifacts/v3_review_debt_summary_1025_preview.json \
  --label-expansion-candidates artifacts/v3_label_expansion_candidates_1025.json \
  --target-source-entries 1025 \
  --public-target-countable-labels 10000 \
  --out artifacts/v3_source_scale_limit_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-transfer-manifest \
  --source-scale-audit artifacts/v3_source_scale_limit_audit_1025.json \
  --learned-retrieval-manifest artifacts/v3_learned_retrieval_manifest_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_1025.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_1025_preview_batch.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_source_transfer_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-sequence-distance-holdout-eval \
  --slice-id 1000 \
  --retrieval artifacts/v3_geometry_retrieval_1000.json \
  --labels artifacts/v3_countable_labels_batch_1000.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1000.json \
  --geometry artifacts/v3_geometry_features_1000.json \
  --abstain-threshold 0.4115 \
  --sequence-fasta artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta \
  --sequence-identity-backend mmseqs \
  --sequence-identity-threshold 0.30 \
  --sequence-identity-coverage 0.80 \
  --out artifacts/v3_sequence_distance_holdout_eval_1000.json

PYTHONPATH=src python -m catalytic_earth.cli build-sequence-distance-holdout-eval \
  --slice-id 1025 \
  --retrieval artifacts/v3_geometry_retrieval_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --geometry artifacts/v3_geometry_features_1025.json \
  --abstain-threshold 0.4115 \
  --sequence-fasta artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta \
  --sequence-identity-backend mmseqs \
  --sequence-identity-threshold 0.30 \
  --sequence-identity-coverage 0.80 \
  --out artifacts/v3_sequence_distance_holdout_eval_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-query-manifest \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_1025.json \
  --max-lanes 8 \
  --out artifacts/v3_external_source_query_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-ood-calibration-plan \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_ood_calibration_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-candidate-sample \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --max-records-per-lane 5 \
  --out artifacts/v3_external_source_candidate_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-candidate-sample \
  --candidate-sample artifacts/v3_external_source_candidate_sample_1025.json \
  --out artifacts/v3_external_source_candidate_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-candidate-manifest \
  --candidate-sample artifacts/v3_external_source_candidate_sample_1025.json \
  --ood-calibration-plan artifacts/v3_external_ood_calibration_plan_1025.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --out artifacts/v3_external_source_candidate_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-candidate-manifest \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --out artifacts/v3_external_source_candidate_manifest_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-lane-balance \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --min-lanes 3 \
  --max-dominant-lane-fraction 0.6 \
  --out artifacts/v3_external_source_lane_balance_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-evidence-plan \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --candidate-manifest-audit artifacts/v3_external_source_candidate_manifest_audit_1025.json \
  --out artifacts/v3_external_source_evidence_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-evidence-request-export \
  --evidence-plan artifacts/v3_external_source_evidence_plan_1025.json \
  --max-rows 50 \
  --out artifacts/v3_external_source_evidence_request_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-evidence-queue \
  --evidence-plan artifacts/v3_external_source_evidence_plan_1025.json \
  --max-rows 50 \
  --out artifacts/v3_external_source_active_site_evidence_queue_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-evidence-sample \
  --active-site-evidence-queue artifacts/v3_external_source_active_site_evidence_queue_1025.json \
  --max-candidates 25 \
  --out artifacts/v3_external_source_active_site_evidence_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-evidence-sample \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --out artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-heuristic-control-queue \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --max-rows 25 \
  --out artifacts/v3_external_source_heuristic_control_queue_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-heuristic-control-queue \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --out artifacts/v3_external_source_heuristic_control_queue_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-structure-mapping-plan \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --max-rows 25 \
  --out artifacts/v3_external_source_structure_mapping_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-structure-mapping-plan \
  --structure-mapping-plan artifacts/v3_external_source_structure_mapping_plan_1025.json \
  --out artifacts/v3_external_source_structure_mapping_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-structure-mapping-sample \
  --structure-mapping-plan artifacts/v3_external_source_structure_mapping_plan_1025.json \
  --max-candidates 12 \
  --out artifacts/v3_external_source_structure_mapping_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-structure-mapping-sample \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --out artifacts/v3_external_source_structure_mapping_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-heuristic-control-scores \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --top-k 5 \
  --out artifacts/v3_external_source_heuristic_control_scores_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-heuristic-control-scores \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --out artifacts/v3_external_source_heuristic_control_scores_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-failure-modes \
  --active-site-evidence-sample-audit artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --heuristic-control-scores-audit artifacts/v3_external_source_heuristic_control_scores_audit_1025.json \
  --structure-mapping-sample-audit artifacts/v3_external_source_structure_mapping_sample_audit_1025.json \
  --out artifacts/v3_external_source_failure_mode_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-control-repair-plan \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --heuristic-control-scores-audit artifacts/v3_external_source_heuristic_control_scores_audit_1025.json \
  --external-failure-mode-audit artifacts/v3_external_source_failure_mode_audit_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_control_repair_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-control-repair-plan \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --external-failure-mode-audit artifacts/v3_external_source_failure_mode_audit_1025.json \
  --out artifacts/v3_external_source_control_repair_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-control-manifest \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_representation_control_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-control-manifest \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --out artifacts/v3_external_source_representation_control_manifest_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-binding-context-repair-plan \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_binding_context_repair_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-binding-context-repair-plan \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --out artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-binding-context-mapping-sample \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --max-candidates 7 \
  --out artifacts/v3_external_source_binding_context_mapping_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-binding-context-mapping-sample \
  --binding-context-mapping-sample artifacts/v3_external_source_binding_context_mapping_sample_1025.json \
  --out artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-gap-source-requests \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --binding-context-mapping-sample artifacts/v3_external_source_binding_context_mapping_sample_1025.json \
  --out artifacts/v3_external_source_active_site_gap_source_requests_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-holdouts \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --max-rows 100 \
  --out artifacts/v3_external_source_sequence_holdout_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-neighborhood-plan \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --sequence-holdout-audit artifacts/v3_external_source_sequence_holdout_audit_1025.json \
  --out artifacts/v3_external_source_sequence_neighborhood_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-neighborhood-sample \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --max-external-rows 30 \
  --max-reference-sequences 1000 \
  --top-k 3 \
  --out artifacts/v3_external_source_sequence_neighborhood_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-neighborhood-sample \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --out artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-alignment-verification \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --top-k 3 \
  --max-pairs 120 \
  --out artifacts/v3_external_source_sequence_alignment_verification_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-alignment-verification \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --out artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-reference-screen \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_source_sequence_reference_screen_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-sequence-search-export \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --sequence-reference-screen-audit artifacts/v3_external_source_sequence_reference_screen_audit_1025.json \
  --out artifacts/v3_external_source_sequence_search_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-sequence-search-export \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --out artifacts/v3_external_source_sequence_search_export_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-backend-sequence-search \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --sequence-clusters artifacts/v3_sequence_cluster_proxy_1025.json \
  --labels data/registries/curated_mechanism_labels.json \
  --reference-fasta artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta \
  --external-fasta-out artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --reference-fasta-out artifacts/v3_external_source_backend_sequence_search_reference_1025.fasta \
  --result-tsv-out artifacts/v3_external_source_backend_sequence_search_1025.tsv \
  --backend auto \
  --out artifacts/v3_external_source_backend_sequence_search_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-backend-sequence-search \
  --backend-sequence-search artifacts/v3_external_source_backend_sequence_search_1025.json \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --out artifacts/v3_external_source_backend_sequence_search_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-reaction-evidence-sample \
  --evidence-request-export artifacts/v3_external_source_evidence_request_export_1025.json \
  --max-candidates 30 \
  --max-reactions-per-ec 2 \
  --out artifacts/v3_external_source_reaction_evidence_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-reaction-evidence-sample \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-control-comparison \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_representation_control_comparison_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-control-comparison \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --out artifacts/v3_external_source_representation_control_comparison_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-plan \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --out artifacts/v3_external_source_representation_backend_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-plan \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --out artifacts/v3_external_source_representation_backend_plan_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --out artifacts/v3_external_source_kmer_representation_backend_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample \
  --representation-backend-sample artifacts/v3_external_source_kmer_representation_backend_sample_1025.json \
  --out artifacts/v3_external_source_kmer_representation_backend_sample_audit_1025.json

HF_HOME=/private/tmp/catalytic-earth-hf \
PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --max-rows 12 \
  --top-k 3 \
  --embedding-backend esm2_t6_8m_ur50d \
  --model-name facebook/esm2_t6_8M_UR50D \
  --out artifacts/v3_external_source_representation_backend_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --out artifacts/v3_external_source_representation_backend_sample_audit_1025.json

# The current 650M sidecar is generated after caching the largest feasible
# smaller ESM-2 tier (`facebook/esm2_t30_150M_UR50D`) in
# `/private/tmp/catalytic-earth-hf-cache`. It records 650M as requested and 150M
# as the actual computed fallback; do not read it as a completed 650M control.
PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --max-rows 12 \
  --top-k 3 \
  --embedding-backend esm2_t33_650m_ur50d \
  --model-name facebook/esm2_t33_650M_UR50D \
  --local-files-only \
  --out artifacts/v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --out artifacts/v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-stability \
  --baseline-representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --comparison-representation-backend-sample artifacts/v3_external_source_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --out artifacts/v3_external_source_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-broad-ec-disambiguation \
  --control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-import-readiness \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --backend-sequence-search artifacts/v3_external_source_backend_sequence_search_1025.json \
  --out artifacts/v3_external_source_import_readiness_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-sourcing-queue \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_queue_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-sourcing-queue \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-sourcing-export \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-sourcing-export \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-active-site-sourcing-resolution \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_resolution_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-active-site-sourcing-resolution \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --out artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-transfer-blocker-matrix \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --backend-sequence-search artifacts/v3_external_source_backend_sequence_search_1025.json \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --out artifacts/v3_external_source_transfer_blocker_matrix_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-transfer-blocker-matrix \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --out artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-candidate-priority \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --max-candidates 10 \
  --max-per-lane 2 \
  --out artifacts/v3_external_source_pilot_candidate_priority_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-review-decision-export \
  --pilot-candidate-priority artifacts/v3_external_source_pilot_candidate_priority_1025.json \
  --max-rows 10 \
  --out artifacts/v3_external_source_pilot_review_decision_export_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-evidence-packet \
  --pilot-candidate-priority artifacts/v3_external_source_pilot_candidate_priority_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --backend-sequence-search artifacts/v3_external_source_backend_sequence_search_1025.json \
  --max-rows 10 \
  --out artifacts/v3_external_source_pilot_evidence_packet_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-representation-backend-plan \
  --pilot-candidate-priority artifacts/v3_external_source_pilot_candidate_priority_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --max-rows 10 \
  --out artifacts/v3_external_source_pilot_representation_backend_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-plan \
  --representation-backend-plan artifacts/v3_external_source_pilot_representation_backend_plan_1025.json \
  --out artifacts/v3_external_source_pilot_representation_backend_plan_audit_1025.json

HF_HOME=/private/tmp/catalytic-earth-hf-cache \
PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample \
  --representation-backend-plan artifacts/v3_external_source_pilot_representation_backend_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --max-rows 10 \
  --top-k 3 \
  --embedding-backend esm2_t6_8m_ur50d \
  --out artifacts/v3_external_source_pilot_representation_backend_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample \
  --representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --out artifacts/v3_external_source_pilot_representation_backend_sample_audit_1025.json

# Same requested-650M/actual-150M sidecar pattern for selected pilot rows.
PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample \
  --representation-backend-plan artifacts/v3_external_source_pilot_representation_backend_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --max-rows 10 \
  --top-k 3 \
  --embedding-backend esm2_t33_650m_ur50d \
  --model-name facebook/esm2_t33_650M_UR50D \
  --local-files-only \
  --out artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample \
  --representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --out artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-stability \
  --baseline-representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --comparison-representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --out artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-evidence-dossiers \
  --pilot-evidence-packet artifacts/v3_external_source_pilot_evidence_packet_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --out artifacts/v3_external_source_pilot_evidence_dossiers_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-active-site-evidence-decisions \
  --pilot-evidence-dossiers artifacts/v3_external_source_pilot_evidence_dossiers_1025.json \
  --pilot-evidence-packet artifacts/v3_external_source_pilot_evidence_packet_1025.json \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --backend-sequence-search artifacts/v3_external_source_backend_sequence_search_1025.json \
  --pilot-representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --max-rows 10 \
  --out artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-success-criteria \
  --pilot-candidate-priority artifacts/v3_external_source_pilot_candidate_priority_1025.json \
  --pilot-review-decision-export artifacts/v3_external_source_pilot_review_decision_export_1025.json \
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --external-transfer-gate artifacts/v3_external_source_transfer_gate_check_1025.json \
  --min-import-ready-rows 1 \
  --max-rows 10 \
  --out artifacts/v3_external_source_pilot_success_criteria_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-review-only-import-safety \
  --labels data/registries/curated_mechanism_labels.json \
  --review artifacts/v3_external_source_evidence_request_export_1025.json \
  --out artifacts/v3_external_source_review_only_import_safety_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli check-external-source-transfer-gates \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --ood-calibration-plan artifacts/v3_external_ood_calibration_plan_1025.json \
  --candidate-sample-audit artifacts/v3_external_source_candidate_sample_audit_1025.json \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --candidate-manifest-audit artifacts/v3_external_source_candidate_manifest_audit_1025.json \
  --lane-balance-audit artifacts/v3_external_source_lane_balance_audit_1025.json \
  --evidence-plan artifacts/v3_external_source_evidence_plan_1025.json \
  --evidence-request-export artifacts/v3_external_source_evidence_request_export_1025.json \
  --review-only-import-safety-audit artifacts/v3_external_source_review_only_import_safety_audit_1025.json \
  --active-site-evidence-queue artifacts/v3_external_source_active_site_evidence_queue_1025.json \
  --active-site-evidence-sample artifacts/v3_external_source_active_site_evidence_sample_1025.json \
  --active-site-evidence-sample-audit artifacts/v3_external_source_active_site_evidence_sample_audit_1025.json \
  --heuristic-control-queue artifacts/v3_external_source_heuristic_control_queue_1025.json \
  --heuristic-control-queue-audit artifacts/v3_external_source_heuristic_control_queue_audit_1025.json \
  --structure-mapping-plan artifacts/v3_external_source_structure_mapping_plan_1025.json \
  --structure-mapping-plan-audit artifacts/v3_external_source_structure_mapping_plan_audit_1025.json \
  --structure-mapping-sample artifacts/v3_external_source_structure_mapping_sample_1025.json \
  --structure-mapping-sample-audit artifacts/v3_external_source_structure_mapping_sample_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --heuristic-control-scores-audit artifacts/v3_external_source_heuristic_control_scores_audit_1025.json \
  --external-failure-mode-audit artifacts/v3_external_source_failure_mode_audit_1025.json \
  --external-control-repair-plan artifacts/v3_external_source_control_repair_plan_1025.json \
  --external-control-repair-plan-audit artifacts/v3_external_source_control_repair_plan_audit_1025.json \
  --reaction-evidence-sample artifacts/v3_external_source_reaction_evidence_sample_1025.json \
  --reaction-evidence-sample-audit artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json \
  --representation-control-manifest artifacts/v3_external_source_representation_control_manifest_1025.json \
  --representation-control-manifest-audit artifacts/v3_external_source_representation_control_manifest_audit_1025.json \
  --representation-control-comparison artifacts/v3_external_source_representation_control_comparison_1025.json \
  --representation-control-comparison-audit artifacts/v3_external_source_representation_control_comparison_audit_1025.json \
  --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json \
  --representation-backend-plan-audit artifacts/v3_external_source_representation_backend_plan_audit_1025.json \
  --representation-backend-sample artifacts/v3_external_source_representation_backend_sample_1025.json \
  --representation-backend-sample-audit artifacts/v3_external_source_representation_backend_sample_audit_1025.json \
  --broad-ec-disambiguation-audit artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json \
  --active-site-gap-source-requests artifacts/v3_external_source_active_site_gap_source_requests_1025.json \
  --sequence-neighborhood-plan artifacts/v3_external_source_sequence_neighborhood_plan_1025.json \
  --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json \
  --sequence-neighborhood-sample-audit artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json \
  --sequence-alignment-verification artifacts/v3_external_source_sequence_alignment_verification_1025.json \
  --sequence-alignment-verification-audit artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json \
  --sequence-reference-screen-audit artifacts/v3_external_source_sequence_reference_screen_audit_1025.json \
  --sequence-search-export artifacts/v3_external_source_sequence_search_export_1025.json \
  --sequence-search-export-audit artifacts/v3_external_source_sequence_search_export_audit_1025.json \
  --sequence-backend-search artifacts/v3_external_source_backend_sequence_search_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --active-site-sourcing-queue artifacts/v3_external_source_active_site_sourcing_queue_1025.json \
  --active-site-sourcing-queue-audit artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json \
  --active-site-sourcing-export artifacts/v3_external_source_active_site_sourcing_export_1025.json \
  --active-site-sourcing-export-audit artifacts/v3_external_source_active_site_sourcing_export_audit_1025.json \
  --active-site-sourcing-resolution artifacts/v3_external_source_active_site_sourcing_resolution_1025.json \
  --active-site-sourcing-resolution-audit artifacts/v3_external_source_active_site_sourcing_resolution_audit_1025.json \
  --transfer-blocker-matrix artifacts/v3_external_source_transfer_blocker_matrix_1025.json \
  --transfer-blocker-matrix-audit artifacts/v3_external_source_transfer_blocker_matrix_audit_1025.json \
  --pilot-candidate-priority artifacts/v3_external_source_pilot_candidate_priority_1025.json \
  --pilot-review-decision-export artifacts/v3_external_source_pilot_review_decision_export_1025.json \
  --pilot-evidence-packet artifacts/v3_external_source_pilot_evidence_packet_1025.json \
  --pilot-evidence-dossiers artifacts/v3_external_source_pilot_evidence_dossiers_1025.json \
  --pilot-representation-backend-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --binding-context-repair-plan artifacts/v3_external_source_binding_context_repair_plan_1025.json \
  --binding-context-repair-plan-audit artifacts/v3_external_source_binding_context_repair_plan_audit_1025.json \
  --binding-context-mapping-sample artifacts/v3_external_source_binding_context_mapping_sample_1025.json \
  --binding-context-mapping-sample-audit artifacts/v3_external_source_binding_context_mapping_sample_audit_1025.json \
  --sequence-holdout-audit artifacts/v3_external_source_sequence_holdout_audit_1025.json \
  --out artifacts/v3_external_source_transfer_gate_check_1025.json
```

## Guardrails

External-source artifacts are not label registries. They must remain
non-countable until a future run builds explicit external candidate evidence
and then passes OOD calibration, sequence-similarity failure controls, review
exports, decision artifacts, heuristic control comparison, and the full
label-factory gate. The current gate only authorizes review-only evidence
collection.

The transfer gate now checks both row-level candidate lineage and artifact-path
lineage. Current 1,025 artifacts share a clean path-inferred slice across 63
supplied artifacts, and the CLI fails fast if a future gate invocation mixes
1,000 and 1,025 artifacts or if payload-declared slice metadata contradicts the
artifact path. Candidate-lineage validation now includes the sequence-holdout
audit and pilot representation sample, so stale holdout or pilot
representation rows cannot silently satisfy the gate by matching only
high-level candidate counts. The high-fan-in import-readiness, blocker-matrix,
pilot-packet, and pilot-dossier builders now fail before artifact write on the
same mixed-slice condition instead of relying only on the later transfer gate.

Do not import external candidates directly into
`data/registries/curated_mechanism_labels.json`. The first safe external-source
milestone is a review-only candidate manifest and evidence-request export that
can fail cleanly without changing the benchmark label count.
