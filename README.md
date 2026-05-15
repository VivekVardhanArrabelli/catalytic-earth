# Catalytic Earth

Catalytic Earth is an open research scaffold for a mechanism-level atlas of enzyme
function. The goal is to make enzyme function searchable by catalytic mechanism,
not only by name, EC number, keyword, or sequence similarity.

## North Star

Build a computable map from protein sequence and structure to chemical function:

```text
protein sequence
+ predicted or experimental structure
+ active-site geometry
+ catalytic residue roles
+ cofactor and metal dependence
+ substrate-pocket constraints
+ reaction bond changes
+ evolutionary context
= mechanism-level function hypothesis
```

This repository has moved past the initial v0 scaffold. The current public state
is a scaffold-level V2 research artifact plus post-V2 active-site geometry,
ligand/cofactor context, substrate-pocket descriptors, curated seed labels,
abstention calibration, cofactor coverage audits, and local performance checks.

## What This Is

- A research program for mechanism-first enzyme discovery.
- A schema for enzyme mechanism fingerprints.
- A registry of public data sources needed for a catalytic knowledge graph.
- A small executable validation and artifact-building pipeline.
- A base for later ingestion, benchmarking, model training, and discovery campaigns.

## What This Is Not

- It is not a wet-lab protocol.
- It is not a claim that computational candidates are validated enzymes.
- It is not a biological design system for harmful functions.
- It is not an EC-number classifier dressed up as mechanistic discovery.

## Current State

The repository currently contains:

1. A bounded catalytic knowledge graph slice linking M-CSA, Rhea, UniProt, PDB,
   and AlphaFold DB references.
2. A mechanism fingerprint registry and benchmark builder with leakage controls.
3. A baseline retrieval system, inconsistency detector, dark-hydrolase mining
   campaign, and candidate dossier writer.
4. PDB mmCIF active-site geometry extraction for catalytic residues.
5. Nearby ligand/cofactor context from non-polymer mmCIF records.
6. Structure-wide ligand inventory for cofactor coverage audits.
7. Substrate-pocket descriptor extraction from nearby protein residues.
8. Curated mechanism labels for 679 entries: all entries in the 475-entry
   source slice plus accepted, factory-gated labels through the 1,000-entry
   candidate queue.
9. Auth-vs-label mmCIF residue-number fallback for cleaner structure mapping.
10. Retrieval evaluation, abstention threshold calibration, hard-negative
    selection, in-scope failure analysis, cofactor coverage analysis,
    label-expansion candidate ranking, geometry slice summaries, and a local
    performance suite.
11. Label-factory automation: explicit bronze/silver/gold label schema,
    mechanism ontology, deterministic promotion/demotion audit, active-learning
    review queue, adversarial negative mining, family-propagation guardrails
    including reaction/substrate mismatch blockers,
    expert-review export/import, review-debt triage, repair guardrail audits,
    ontology-gap and sequence-similarity failure controls, learned-retrieval
    manifest pathing, expert-reviewed ATP/phosphoryl-transfer family expansion,
    batch summary with scaling-quality audit attachment, a scaling gate, a
    versioned declarative counterevidence policy with leakage provenance, and a
    typed label-factory gate input contract.
12. A provenance-bearing selected-PDB override path for review-debt structure
    single points of failure. The first override plan applies holo-preference
    repairs for `m_csa:577` and `m_csa:641`, skips `m_csa:592` as a
    reaction-mismatch policy case, and keeps all rows non-countable.

The 20- through 1,000-entry evaluation slices are clean out-of-scope regression
slices: each has 0 out-of-scope false non-abstentions and 0 hard negatives
under calibrated abstention. The 125-entry slice has 38 in-scope positives, 87
out-of-scope controls, 124/125 evaluable active-site structures, threshold
`0.4115`, and a positive score separation gap of `0.0308`.

The current 1,000-entry countable stress slice has 662 evaluable active-site
structures among 678 evaluated labeled rows, 212 in-scope labels, 466
evaluated out-of-scope controls, 39 structure-mapping issues, 0 hard negatives,
and 0 near misses. Its calibrated threshold is `0.4115`; it retains 208/212
current in-scope positives, abstains on all evaluable out-of-scope controls,
and leaves the same 4 evidence-limited in-scope abstentions (`m_csa:132`,
`m_csa:353`, `m_csa:372`, and `m_csa:430`).
The current actionable in-scope failure count is 0 after separating
selected-structure cofactor gaps from scorer failures. Cofactor policy sweeps
recommend audit-only handling rather than a score penalty because no tested
penalty reduces retained evidence-limited positives without losing retained
positives. Cofactor coverage artifacts explicitly identify retained
evidence-limited positives: `m_csa:41`, `m_csa:108`, `m_csa:160`,
`m_csa:446`, and `m_csa:486`.
`artifacts/v3_selected_pdb_override_plan_700.json` now records a general
selected-structure override plan. The corresponding
`artifacts/v3_geometry_features_1000_selected_pdb_override.json` and downstream
retrieval/evaluation artifacts show `m_csa:577` using holo alternate `1AWB` and
`m_csa:641` using holo alternate `1J7N`, with 0 hard negatives, 0 near misses,
0 out-of-scope false non-abstentions, and 0 actionable in-scope failures. These
override artifacts are repair evidence only; they do not add countable labels.

The 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, 700-, 725-, 750-, 775-,
800-, 825-, 850-, 875-, 900-, 925-, 950-, 975-, and 1,000-entry candidate
queues have been processed through the label factory. `m_csa:494` is
intentionally preserved as a non-countable `needs_expert_review` cobalamin
evidence gap because B12 evidence is structure-wide only. The 675, 700, 725,
750, 775, 800, 825, 850, 875, 900, 925, 950, 975, and 1,000 batches accepted 61 additional clean countable
labels while preserving 0 hard negatives, 0 near misses, 0 out-of-scope false
non-abstentions, and 0 actionable in-scope failures. See
`work/label_queue_500_notes.md`, `work/label_queue_525_notes.md`,
`work/label_queue_550_notes.md`, `work/label_factory_notes.md`,
`work/label_preview_725_notes.md`, `work/label_preview_750_notes.md`,
`work/label_preview_850_notes.md`, `work/label_preview_950_notes.md`,
`work/label_preview_975_notes.md`, `work/label_preview_1000_notes.md`, and
`work/label_preview_1025_notes.md`; the external-source transfer profile is in
`work/external_source_transfer_1025_notes.md`.

Label scaling is now gated by the label factory rather than raw queue size. The
current 1,000 factory audit proposes 125 bronze-to-silver promotions, flags
112 abstention/review rows, mines 80 adversarial negative controls from 466
out-of-scope candidates, exports 430 review items from the 1,000 post-batch
review queue, exports all 321 active `expert_label_decision_needed` rows as
review-only no-decision items, generates a non-countable repair-candidate plan
and priority repair guardrail audit for those 321 rows, audits/exports the 92
priority local-evidence gap lanes as review-only items, emits a local-evidence
repair plan, verifies review-only import safety, maps expert-reviewed
ATP/phosphoryl-transfer mismatch lanes to nine concrete fingerprint families,
and passes the 21-check 1,000-slice gate after the accepted-review-debt deferral
audit confirms all 326 accepted-1,000 review-state rows remain non-countable.
The gate also
fails if unlabeled candidate rows are truncated by the queue limit, if
family-guardrail reaction/substrate mismatch lanes lack a dedicated review
export, if expert-label decision rows are not explicitly routed as non-countable
external-review items, or if those rows lack a complete non-countable repair
candidate summary, repair guardrail audit, local-evidence gap audit, and
local-evidence review export; it also requires alternate residue-position
sourcing requests and review-only import-safety audit to remain non-countable,
and requires the
ATP/phosphoryl-transfer family expansion artifact to be guardrail-clean when
attached.
`artifacts/v3_label_batch_acceptance_check_1000.json` records that the latest
canonical accepted batch added 4 labels for counting while 326 review-state
decisions remain pending. `artifacts/v3_accepted_review_debt_deferral_audit_1000.json`
explicitly defers those 326 rows, including the 21 new 1,000-preview review-debt
rows. `artifacts/v3_label_factory_batch_summary.json` aggregates the accepted
batch history and confirms 21/21 accepted batches remain guardrail-clean.
`artifacts/v3_review_debt_summary_1000_preview.json` prioritizes current
evidence-gap rows for the accepted 1,000 state. The 675, 700, 725, 750, 775, 800,
825, 850, 875, 900, 925, 950, 975, and 1,000
scaling-quality audits keep pending evidence gaps outside the
benchmark, classify new debt rows, and attach graph-derived sequence-cluster
proxy artifacts; all report 0 accepted labels with review debt and 0
near-duplicate hits among audited rows. See
`work/label_preview_675_notes.md`, `work/label_preview_700_notes.md`,
`work/label_preview_725_notes.md`, `work/label_preview_750_notes.md`,
`work/label_preview_775_notes.md`, `work/label_preview_850_notes.md`,
`work/label_preview_950_notes.md`, `work/label_preview_975_notes.md`,
`work/label_preview_1000_notes.md`, and
`work/expert_label_decision_review_700_notes.md` for the clean label profiles,
the top evidence gaps, the expert-decision review-only profile, and the
prioritized non-countable repair buckets.

The bounded 1,025 preview has been opened but not promoted. Its factory gate
passes 21/21 checks, but the batch acceptance artifact records 0 accepted new
labels, 329 review-state rows, and a `do_not_promote` scaling recommendation.
`artifacts/v3_source_scale_limit_audit_1025.json` also shows that the M-CSA
slice currently exposes 1,003 source records rather than 1,025, so M-CSA-only
growth cannot reach the 10,000-label target. The new external-source transfer
artifacts scope a UniProtKB/Swiss-Prot path with query lanes, OOD calibration,
sequence-similarity controls, a 30-row read-only candidate sample, an external
candidate manifest, evidence plan/export, review-only import-safety audit,
active-site feature sampling, structure-mapping and heuristic-control
prototypes, failure-mode audit, control-repair artifacts, representation-control
comparison, broad-EC disambiguation, active-site gap source requests,
sequence-neighborhood controls, sequence-alignment verification,
sequence-search export, import-readiness audit, active-site sourcing queue/export,
active-site sourcing resolution, representation-backend plan/sample, a
candidate blocker matrix, a 10-row external pilot candidate priority worklist,
a consolidated pilot evidence packet, 10 per-candidate pilot evidence
dossiers, a 10-row pilot-specific ESM-2 representation sample, and a 68/68
external transfer gate with backend sequence-search, current-reference sequence
screen, candidate, artifact-path, and pilot review-only decision validation. The
evidence plan
flags seven broad or incomplete EC contexts,
defers three broad-only candidates for reaction disambiguation, and exports a
review-only active-site evidence queue with 25 ready candidates. The active-site
feature pass finds 15 feature-supported candidates and 10 active-site-feature
gaps; the expanded structure-mapping sample maps all 12 heuristic-ready
AlphaFold controls, but the heuristic control still collapses 9/12 to
`metal_dependent_hydrolase` top1 and records 9 scope/top1 mismatches, so the
failure-mode audit keeps this as a review-only retrieval-control issue. The
control-repair plan converts the current weaknesses into 25 non-countable
repair rows, the representation manifest exposes 12 mapped controls for future
learned or structure-language comparison, the feature-proxy comparison flags
7 metal-hydrolase collapse rows and 2 glycan-boundary rows, the broad-EC audit
finds specific reaction context for all 3 broad-only repair rows, and the
binding-context path maps 7/7 active-site-gap rows as repair context only. The
active-site sourcing resolution re-checks all 10 active-site-gap rows against
UniProt feature evidence, finds 0 explicit active-site residue sources, and
keeps them non-countable. The computed ESM-2 representation backend sample
covers all 12 planned controls, flags three representation-level
near-duplicate holdouts, and remains review-only; the deterministic k-mer
sample is preserved separately as a labeled proxy baseline. The
active-site gap source-request artifact covers all 10 gaps, and the
sequence-neighborhood plan keeps 2 exact-reference overlaps as holdouts while
scoping duplicate-screening controls for the other 28 candidates. The bounded
sequence screen fetches all 30 external sequences plus all 735 current
countable M-CSA reference accessions after resolving inactive demerged UniProt
references `P03176` and `Q05489` to their replacement accessions. The
current-reference screen audit now clears the current-reference near-duplicate
blocker: 28 rows have top-hit alignments with no near-duplicate signal and two
exact-reference rows stay holdouts. `artifacts/v3_external_source_backend_sequence_search_1025.json`
then runs a real MMseqs2 18-8cc5c bounded backend search over the 30 external
rows against 735 current reference accessions / 737 sequence records. It
preserves exact holdouts `O15527` and `P42126`, records 28 no-signal rows, 0
near-duplicate rows, and 0 failures, and keeps every row review-only,
non-countable, and not import-ready. This removes the bounded current-reference
backend sequence-search debt for the 28 no-signal rows; broader UniRef-wide or
all-vs-all duplicate screening remains required before any import. The bounded
sequence-alignment verification checks 90 top-hit pairs, confirms the two
exact-reference holdouts, and keeps every row non-countable. The
import-readiness audit keeps 0 rows import-ready while summarizing 10
active-site gaps, 2 exact sequence holdouts, 9 heuristic scope/top1
mismatches, 29 representation-control issues, and the remaining broader
duplicate-screening limitation, while the active-site sourcing queue
prioritizes the 10 active-site gaps into 7 mapped-binding-context rows and 3
primary-source rows. The active-site sourcing export carries 72 source targets,
the sequence-search export plus backend search keep all 30 rows in no-decision
review-only sequence controls, the
representation-backend plan covers 12 controls without computing embeddings, and
the blocker matrix joins all 30 external rows into a non-countable worklist
with the active-site resolution and representation sample statuses carried
forward: 7 literature/PDB active-site reviews, 3 primary active-site source
tasks, 9 real representation-backend selections, 6 representation-control
attachments, 3 representation-near-duplicate holdouts, and 2 sequence holdouts.
`artifacts/v3_external_source_pilot_candidate_priority_1025.json` then selects
10 review-only pilot candidates across six external lanes, defers 5 exact
holdout or near-duplicate rows, and keeps every selected row non-countable and
not import-ready. Its leakage policy records that mechanism text, EC/Rhea ids,
source labels, and target labels are excluded from priority scoring.
`artifacts/v3_external_source_pilot_review_decision_export_1025.json` exports
those 10 rows as no-decision review packets with 0 completed decisions, so it
removes the packet-scaffolding blocker without authorizing import.
`artifacts/v3_external_source_pilot_evidence_packet_1025.json` consolidates
79 source targets for the same 10 rows, including all 10 sequence-search
packets and 3 active-site sourcing packets, while carrying backend
no-near-duplicate status for all 10 selected rows and keeping every row
review-only and non-countable.
`artifacts/v3_external_source_pilot_evidence_dossiers_1025.json` assembles
the selected 10 rows into review-only per-candidate dossiers: 7 currently have
explicit UniProt active-site feature support, all 10 have Rhea reaction
context, all 10 now have pilot-specific ESM-2 representation rows, and all 10
still carry import blockers. The pilot representation sample flags `P55263` as
a representation near-duplicate holdout and keeps every row review-only. The
dossier assembly now adds local evidence-completeness blockers itself; the 3
selected rows without explicit active-site evidence are flagged, and no
selected row is missing specific reaction context. Backend no-signal rows no
longer inherit the stale complete-near-duplicate sequence blockers in the
pilot packet or dossiers.
`artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json`
now classifies those 10 selected rows into review-only active-site evidence
decision states. It records 7 rows with explicit active-site source evidence
and 3 rows with binding context only, removes the pilot source-status ambiguity
blocker, and keeps all 10 rows non-countable and not import-ready because
broader duplicate screening, representation controls, review decisions, and the
full label-factory gate remain unresolved.
`artifacts/v3_external_source_pilot_representation_adjudication_1025.json`
then consumes the 8M-vs-largest-feasible ESM-2 stability audit for the selected
pilot rows. It keeps every row review-only and non-countable while splitting
the former generic representation-control surface into 3 stable review-only
controls, 4 representation near-duplicate holdouts, and 3 stability-change rows
that need representation review. The requested 650M backend remains unavailable
locally, so this is a largest-feasible 150M fallback adjudication, not a 650M
completion claim.
`artifacts/v3_external_source_pilot_success_criteria_1025.json` now makes the
pilot success definition measurable instead of implicit. Operational success
requires all 10 selected candidates to reach terminal decisions with no
unresolved process blockers. Scientific/import success requires at least 1
candidate to become import-ready under full gates, or a zero-pass result where
every failure is explained by concrete evidence rather than missing process.
The current status is `needs_more_work`: 0 terminal decisions, 0 import-ready
rows, 7 explicit active-site rows, 3 binding-context-only active-site rows, all
10 still needing broader duplicate screening and full label-factory gates, 3
remaining unresolved representation-control rows after adjudication, and 0
countable label candidates.
Two sample candidates overlap existing M-CSA reference accessions and are
routed to sequence-holdout controls; the lane-balance audit confirms six evenly
represented query lanes. All
external rows remain non-countable; the gate authorizes evidence collection
only, not label import. Its lineage metadata now records a clean 1,025 slice
across the current checked external artifacts, includes the sequence-holdout
audit, pilot active-site evidence decisions, and pilot representation sample in
row-level candidate-lineage validation, and
fails fast on mixed-slice artifact paths or payload-declared slice
contradictions. The import-readiness audit, transfer blocker matrix, pilot
evidence packet, and pilot evidence dossiers now run the same artifact-path
lineage check at build time and record the clean 1,025 lineage in their own
metadata, so stale mixed-slice pilot work fails before downstream gates. The full Rhea reaction-context
pass covers all 30 external candidates with 64 reaction records, flags 16
broad-EC context rows, and remains review-only. See
`docs/external_source_transfer.md` for the guarded command sequence.
`artifacts/v3_sequence_distance_holdout_eval_1000.json` and
`artifacts/v3_sequence_distance_holdout_eval_1025.json` now report real
MMseqs2 sequence-identity holdout metrics for the accepted countable registry
while preserving the older low-neighborhood proxy fields as fallback context.
Both contexts use the sidecar FASTA
`artifacts/v3_sequence_distance_holdout_eval_uniprot_1000_1025.fasta`,
cover 678/678 evaluated labels, cluster 738 sequence records at 30% identity
and 80% coverage, hold out 136 rows by whole sequence clusters, and record a
max observed train/test identity of `0.284`. The target <=30% sequence-identity
split is achieved, with 0 held-out out-of-scope false non-abstentions; held-out
evaluable in-scope top1 accuracy, top3 retained accuracy, and retention are all
`1.0000`. The artifacts now also expose explicit backend, resolved path,
cluster-threshold, target-achievement, and limitation metadata aliases for gate
and review consumers. Full Foldseek/TM-score separation remains uncomputed.
`artifacts/v3_foldseek_coordinate_readiness_1000.json` narrows that blocker by
recording the explicit Foldseek binary/version
(`/private/tmp/catalytic-foldseek-env/bin/foldseek`, `10.941cd33`), the 678
evaluated accepted-registry rows, 676 rows with supported selected PDB
coordinates, two explicit coordinate exclusions for rows with no selected
structure in the current evidence (`m_csa:372`, `m_csa:501`), and a capped
25-PDB coordinate sidecar in
`artifacts/v3_foldseek_coordinates_1000/`. It is review-only/non-countable and
keeps `tm_score_split_computed=false`. The paired
`artifacts/v3_foldseek_tm_score_signal_1000_staged25.json` adds a bounded
all-vs-all Foldseek `easy-search` signal over only those 25 staged coordinates:
1,840 pair rows, 25 mapped staged entries, 532 staged heldout/in-distribution
pair rows, and max observed staged train/test TM signal `0.6426` against the
`<0.7` target. It is review-only, has 0 countable/import-ready rows, and keeps
`full_tm_score_split_computed=false`. The expanded coordinate-readiness sidecar
`artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json` now stages
100 selected PDB coordinates with 0 fetch failures, and the companion
`artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json` now records a
completed review-only partial Foldseek run over a capped 40-coordinate subset:
5,699 pair rows, all 5,699 safely mapped rows, 1,633
heldout/in-distribution train/test pairs, max observed train/test TM score
`0.7515`, and 0 unmapped raw Foldseek names, with 0 countable/import-ready
rows. This removes the staged25-only proof blocker and the expanded40 raw-name
mapping blocker, but it is still partial, non-countable, and not import-ready.
`artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`
then stages all currently materializable supported selected coordinates:
672 unique selected PDB mmCIF sidecars for 676 materializable evaluated rows,
with 0 fetch failures, 0 supported selected structures left unstaged, and
explicit coordinate-exclusion evidence for `m_csa:372` and `m_csa:501`
(`geometry_status=no_structure_positions`, `selected_structure_id=null`). This
removes the unstaged selected-coordinate sidecar blocker and makes the
unmaterializable rows explicit. The companion capped Foldseek signals now
extend through `artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json`:
100 staged coordinates, 27,542 mapped pair rows, 7,317
heldout/in-distribution train/test pairs, max observed train/test TM score
`0.7515`, 0 unmapped raw Foldseek names, and 0 countable/import-ready rows.
This removes the expanded80 partial-signal ceiling, but it is still
review-only, capped, and not import-ready. The `<0.7` target is not achieved
on the computed 100-coordinate subset, 572 staged coordinates remain
uncomputed, `tm_score_split_computed=false` and
`full_tm_score_split_computed=false` remain true, and the full TM-score split
still requires an uncapped Foldseek-backed split/signal over the full
materialized set with the coordinate exclusions reported.
`artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json` now makes the
target failure actionable rather than just aggregate metadata: the current
sequence-holdout split already has one unique blocking train/test structure
pair, `m_csa:33`/`m_csa:34` (`pdb:1JC5`/`pdb:1MPY`), with max pair TM-score
`0.7515` across 48 chain-level violating rows. A full holdout claim remains
forbidden unless the split is repaired or the exclusion policy is explicitly
reviewed; extending the capped signal alone cannot make the current split pass
the `<0.7` target.
`artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json` now converts that
observed blocker into a concrete, review-only split-repair candidate: move the
held-out out-of-scope row `m_csa:34` into the in-distribution side before
regenerating sequence-holdout metrics. The projected held-out count would move
from 136 to 135 while preserving all 44 held-out in-scope rows, but the repair
is not applied yet; full TM-score holdout claims remain forbidden until the
sequence holdout, downstream metrics, and an uncapped Foldseek-backed split are
regenerated and pass.
`artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json` applies the
same proposed move only as an in-memory projection over the existing expanded100
Foldseek rows: source train/test violations drop from 48 to 0 and projected
max train/test TM-score is `0.6993`, just under the `<0.7` target. This is
still review-only and non-countable because the real sequence split has not
been regenerated and 572 staged coordinates remain outside the capped signal.
`artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json`
applies the same move to a candidate copy of the sequence holdout: `m_csa:34`
moves from held-out to in-distribution, held-out count becomes 135, held-out
in-scope count stays 44, held-out out-of-scope false non-abstentions stay 0,
and the moved MMseqs2 cluster does not overlap remaining held-out clusters.
`artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json`
then rebuilds the Foldseek coordinate-readiness view from that candidate split
while reusing the all-materializable coordinate sidecar: 672 coordinates remain
staged, `m_csa:34` is now in-distribution, and `m_csa:372`/`m_csa:501` remain
explicit coordinate exclusions. The companion actual Foldseek rerun
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json`
uses the same 100-coordinate cap as expanded100 under the candidate partition:
27,542 mapped pair rows, 6,930 heldout/in-distribution train/test rows, max
observed train/test TM-score `0.6993`, and 0 target-violating pairs in
`artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json`.
This removes the projection-only ambiguity for the computed subset, but the
candidate does not replace the canonical holdout or authorize a full
TM-score-holdout claim: 572 staged coordinates remain uncomputed, the signal is
capped, two selected rows remain excluded from coordinate materialization, and
all three artifacts keep 0 countable/import-ready rows.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`
now records a completed all-materializable staged-coordinate Foldseek signal
over all 672 materializable selected coordinates with Foldseek `10.941cd33` and
`--threads 4`. It maps 952,922 pair rows and 274,241 train/test rows, but the
computed subset fails the `<0.7` target at max train/test TM-score `0.9749`
with 4,715 target-violating train/test rows. This removes the prior
all-materializable runtime ambiguity but does not authorize a full
TM-score-holdout claim: `m_csa:372` and `m_csa:501` remain coordinate
exclusions, the artifact is a review-only signal rather than a canonical split,
and `full_tm_score_holdout_claim_permitted=false` remains correct.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json`
and
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json`
then run the first two resumable all-materializable query chunks directly.
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json`
attempts the next chunk with the same repaired candidate readiness artifact,
Foldseek `10.941cd33`, 12 query coordinates against all 672 staged
materializable target coordinates, `--threads 4`, and a 900-second bound, but
times out before emitting pair rows. A direct longer-cap retry,
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json`,
uses the same chunk and completes under a 1,800-second bound with 12,639
mapped pair rows, 3,216 train/test rows, max train/test TM-score `0.8427`, and
6 target-violating row-level pairs across 2 reported structure pairs. The
completed-retry aggregate
`artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json`
records 3/56 completed chunks, 36 completed query coordinates, 40,890 mapped
pair rows, 12,358 train/test rows, max train/test TM-score `0.8957`, 76
target-violating row-level pairs, 15 reported target-violating structure
pairs, and 53 non-completed chunks. The query-chunk split-repair plan
`artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json`
classifies those 15 observed blockers: 9 have conservative held-out
out-of-scope move candidates, while 6 require manual split redesign because
they touch held-out in-scope rows (`m_csa:20`, `m_csa:497`, and `m_csa:895`).
This removes the chunk-2 runtime ambiguity and narrows the target-failure
surface, but the repaired candidate split still fails `<0.7`, the query
aggregation is incomplete, all rows remain review-only/non-countable/not
import-ready, and `full_tm_score_holdout_claim_permitted=false` remains
correct.
`artifacts/v3_sequence_distance_holdout_split_redesign_candidate_1000.json`
then applies a review-only split redesign over those observed blockers: the 9
held-out out-of-scope repair candidates move to in-distribution, and the 6
high-TM train neighbors of held-out in-scope blockers move to heldout. The
candidate projects 0 observed completed-chunk blockers, keeps sequence-cluster
partition splits at 0, and keeps held-out out-of-scope false non-abstentions
at 0. The direct Foldseek check
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_000_of_056.json`
invalidates that projection as a full fix: chunk 0 completes with 16,475
mapped pair rows, 6,909 train/test rows, max train/test TM-score `0.926`, and
15 target-violating row-level pairs across 4 reported structure pairs. The
follow-up plan
`artifacts/v3_foldseek_tm_score_split_redesign_candidate_query_chunk_repair_plan_1000.json`
narrows the new blocker to held-out in-scope `m_csa:6` versus
`m_csa:277`, `m_csa:378`, `m_csa:320`, and `m_csa:108`. This is review-only
evidence; it creates 0 countable/import-ready rows and keeps
`full_tm_score_holdout_claim_permitted=false`.
A second redesign candidate,
`artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round2_1000.json`,
moves those four high-TM neighbors to heldout as well. The direct round-2
Foldseek chunk
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_000_of_056.json`
clears chunk 0 with max train/test TM-score `0.695` and 0 target-violating
pairs, and the single-chunk aggregate records 1/56 completed redesigned chunks.
Chunk 1 under the round-2 split then exposes a new concrete blocker:
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_001_of_056.json`
completes with 11,776 mapped rows, 4,154 train/test rows, max train/test
TM-score `0.8182`, and 12 target-violating row-level pairs across 4 reported
structure pairs. The repair plan
`artifacts/v3_foldseek_tm_score_split_redesign_candidate_round2_query_chunk_repair_plan_1000.json`
classifies those blockers as held-out in-scope `m_csa:15` and `m_csa:16`
against train neighbors `m_csa:258` and `m_csa:157`, with 0 conservative
out-of-scope repair candidates. The round-3 candidate
`artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round3_1000.json`
moves `m_csa:157` and `m_csa:258` to heldout, keeps sequence-cluster splits at
0, and keeps every row review-only/non-countable. Direct round-3 Foldseek
chunks 0, 1, and 2 clear the target: the aggregate
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_002_of_056.json`
covers 36 query coordinates, 40,890 mapped rows, 13,472 train/test rows, max
train/test TM-score `0.695`, and 0 target-violating pairs. This removes the
first three query-chunk blockers only. A direct chunk 3 attempt,
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_003_of_056.json`,
times out under the standard 900-second bound before pair rows are emitted, and
the aggregate
`artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_003_of_056.json`
keeps that timeout visible while preserving the completed-chunk max
train/test TM-score `0.695`. The 53 chunks from 3-55 remain uncomputed until
chunk 3 is retried or split into a smaller query slice, the two coordinate
exclusions still stand, and full-holdout claims remain forbidden.
A cluster-first Foldseek split path now replaces blind chunk iteration as the
active design. `artifacts/v3_foldseek_tm_score_cluster_first_split_1000.json`
reuses the 672 materialized selected-coordinate index and turns the previously
observed `TM >= 0.7` pairs into 24 partition constraints across 12 constrained
clusters, resolving all observed constraints in projection with 0 sequence
identity cluster splits. A first 6-query verification subchunk then exposed a
new high-TM blocker, `m_csa:38` versus `m_csa:118`, with max train/test
TM-score `0.7435`; the round-2 cluster-first candidate moves held-out
out-of-scope `m_csa:118` to in-distribution and the same subchunk passes with
max train/test TM-score `0.6509` and 0 violations. The paired subchunk 007
then fails with max train/test TM-score `0.8651`, 16 violating rows, and 9
reported structure-pair blockers. Those blockers are folded into
`artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json`, which
now records 34 high-TM constraints, 14 constrained clusters, 0 projected
constraint violations, 0 sequence-cluster splits, and a companion readiness
artifact at
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json`.
Direct round-3 verification reruns subchunks 006 and 007 from that readiness.
Subchunk 006 passes with max train/test TM-score `0.6509`, but subchunk 007
exposes one remaining high-TM blocker, `m_csa:45` versus `m_csa:397`, at max
train/test TM-score `0.8043`. The round-4 cluster-first candidate folds that
blocker into 35 high-TM constraints, moves held-out out-of-scope `m_csa:397`
to in-distribution, and its direct subchunk 007 rerun passes with max
train/test TM-score `0.6598`. Round-4 subchunk 008 then exposes a new
`m_csa:54`/`m_csa:428` blocker at max TM-score `0.7205`; round 5 moves
held-out out-of-scope `m_csa:428` to in-distribution, raises the constraint
count to 36, and clears subchunk 008 at max TM-score `0.6989`. Round-5
subchunk 009 then exposes `m_csa:58`/`m_csa:628` at max TM-score `0.879`;
round 6 moves held-out out-of-scope `m_csa:628` to in-distribution, records
37 high-TM constraints with 0 sequence-cluster splits, and clears subchunk 009
at max TM-score `0.6699`. Direct round-6 subchunk 010 times out under the
900-second bound before pair rows are emitted, so the same query window was
split into 3-query microchunks. Round-6 microchunk 020 completes with 7,488
mapped rows and exposes a new `m_csa:63`/`m_csa:188` blocker at max TM-score
`0.7116`. Round 7 folds that pair into 38 high-TM constraints, 17 constrained
clusters, 0 projected known violations, and 0 sequence-cluster splits, but its
direct microchunk-020 rerun times out under the same 900-second bound before
pair rows are emitted. The timed-out round-7 window has now been verified with
single-query chunks: staged indices 60-62 (`m_csa:61`-`m_csa:63`) aggregate to
7,488 mapped rows, 1,311 train/test rows, max train/test TM-score `0.6967`,
and 0 violations, while staged indices 63-65 (`m_csa:64`-`m_csa:66`) aggregate
to 2,190 mapped rows, 378 train/test rows, max train/test TM-score `0.5629`,
and 0 violations. Continuing one-query checks then clears staged index 66
(`m_csa:67`) at max TM-score `0.6535`, but staged index 67 (`m_csa:68`) exposes
a new `m_csa:68`/`m_csa:750` blocker at max TM-score `0.7909`. Round 8 folds
that pair into 39 high-TM constraints, 18 constrained clusters, 0 projected
known violations, and 0 sequence-cluster splits, with readiness at
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round8.json`.
Direct round-8 single-query verification then clears staged indices 68-78, but
staged index 79 exposes held-out out-of-scope `m_csa:80` against
in-distribution `m_csa:408` and `m_csa:569` at max TM-score `0.8726`. Round 9
folds those pairs into 41 high-TM constraints across 19 constrained clusters,
moves the `m_csa:80` high-TM neighborhood to in-distribution, preserves 0
sequence-cluster splits and 0 held-out out-of-scope false non-abstentions, and
keeps readiness at
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round9.json`.
The direct round-9 rerun of staged index 79 plus staged indices 80-83 passes
in aggregate at max TM-score `0.6477` with 0 target-violating pairs. Continuing
round-9 single-query verification clears staged indices 84-95 with 17,189
mapped rows, 3,257 train/test rows, max train/test TM-score `0.6579`, and 0
target-violating pairs. Continuing from index 96 clears staged indices 96-101
before staged index 102 exposes `m_csa:103`/`pdb:1VAO` versus held-out
`m_csa:115`/`pdb:1W1O` at max TM-score `0.7653`. The cluster-first builder
now preserves real sequence-identity components as partition constraints.
Round 10 folds the new blocker into 42 high-TM constraints plus 38
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
indices 105-106, then index 107 exposes `m_csa:108` against a broad held-out
neighborhood at max `0.8826`; round 14 folds that surface into 60 high-TM
constraints and reruns index 107 cleanly at max `0.6862`. Index 108 then
exposes `m_csa:109` versus `m_csa:800`/`m_csa:267` at max `0.7649`; round 15
folds those blockers, backfills indices 107-109 cleanly at max `0.6996`, and
index 110 exposes `m_csa:111` versus `m_csa:364`, `m_csa:550`, `m_csa:236`,
and `m_csa:270` at max `0.7521`. Round 16 folds that evidence into 66 high-TM
constraints plus 38 sequence-identity partition constraints, but the direct
round-16 rerun of index 110 still exposes `m_csa:111` versus `m_csa:852` at
max `0.7708`. Round 17 folds that pair, clears index 110 at max `0.6823`,
clears index 111 at max `0.564`, then index 112 exposes `m_csa:113` versus
held-out `m_csa:131` at max `0.7063`. Round 18 folds that pair, but the
round-18 rerun of index 112 exposes a larger `m_csa:113` blocker surface
against `m_csa:942`/`m_csa:978` and related in-distribution neighbors at max
`0.9087`. Round 19 folds that evidence into 72 high-TM constraints and clears
indices 112-113 before index 114 exposes `m_csa:115` versus `m_csa:822` at max
`0.7338`. Round 20 folds that pair and clears index 114, but index 115 exposes
a broader `m_csa:116` surface at max `0.9749`; round 21 folds that surface but
still exposes `m_csa:116` versus held-out `m_csa:67` at max `0.9032`. Round 22
folds the remaining pair into 82 high-TM constraints plus 38 sequence-identity
partition constraints, preserves 0 projected violations and 0 sequence-cluster
splits, and clears indices 115-118 in aggregate at max train/test TM-score
`0.6939` with 0 target-violating pairs. Its readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round22.json`.
Continuing from staged index 119 exposes `m_csa:120` blockers at max `0.7556`;
round 23 folds those blockers but the rerun still exposes a second
`m_csa:120` surface at max `0.711`. Round 24 folds that second surface into
93 high-TM constraints plus 38 sequence-identity partition constraints, with 0
projected violations and 0 sequence-cluster splits. Direct round-24
verification clears staged indices 119-122 in aggregate at max train/test
TM-score `0.6961`, with 0 target-violating pairs. Index 123 then exposes
`m_csa:124` blockers in two successive surfaces; rounds 25 and 26 fold those
into 97 high-TM constraints and round 26 clears indices 123-126 at max
`0.6981`. Index 127 exposes `m_csa:128` versus `m_csa:198`; round 27 folds
that pair and clears indices 127-129 at max `0.6868`. Index 130 exposes
`m_csa:131` versus `m_csa:281`/`m_csa:555`; round 28 folds those blockers into
100 high-TM constraints plus 38 sequence-identity constraints, preserves 0
projected violations and 0 sequence-cluster splits, and clears index 130 at
max `0.6775`. Index 131 then exposes `m_csa:132` versus `m_csa:532` at max
`0.8385`; round 29 folds that blocker into 101 high-TM constraints and clears
indices 131-139 before index 140 exposes `m_csa:141` versus `m_csa:903` at
max `0.7337`. Round 30 folds that blocker into 102 high-TM constraints plus
38 sequence-identity constraints, preserves 0 projected violations and 0
sequence-cluster splits, and clears indices 140-141 at max `0.6873`. The
next direct pass clears index 142 at max `0.6204`, then index 143 exposes a
larger `m_csa:144` surface at max `0.872`. Round 31 folds that surface into
106 high-TM constraints, but the rerun still exposes a second index-143
surface at max `0.8001`. Round 32 folds that second surface into 108 high-TM
constraints plus 38 sequence-identity constraints, preserves 0 projected
violations and 0 sequence-cluster splits, and clears indices 143-144 at max
`0.5745`. The active readiness artifact is
`artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round32.json`.
Index 145 (`m_csa:146`/`pdb:4V4E`) is now the direct runtime blocker: exact
Foldseek single-query verification timed out at 900 seconds before pair rows
were emitted.
These artifacts remain review-only and non-countable; no full TM-score holdout
claim is permitted until index 145 and the remaining query coverage pass or are
explicitly adjudicated.
`artifacts/v3_external_source_representation_backend_sample_1025.json`
also computes the first bounded learned representation sample for all 12 mapped
external pilot controls using `facebook/esm2_t6_8M_UR50D`. The sample records
320-dimensional embeddings, keeps all rows review-only and non-countable,
flags three representation-near-duplicate holdouts, and emits 12
learned-vs-heuristic disagreement rows while preserving geometry retrieval as
the required baseline. Its predictive feature policy is sequence-only:
heuristic fingerprint ids, matched M-CSA reference ids, and source scope signals
are carried with leakage flags as review or holdout context, not as discovery
evidence. The geometry retrieval scorer now follows the same text-leakage
boundary: mechanism text, entry names, labels, EC/Rhea identifiers, and source
ids are excluded from positive scoring. The former PLP mechanism-text boost was
replaced with a text-free local PLP ligand-anchor feature derived from proximal
PLP/LLP/PMP/P5P ligand context, and the refreshed 1,000/1,025 retrieval,
holdout, label-factory, and external heuristic-control artifacts preserve 0 hard
negatives, 0 near misses, 0 out-of-scope false non-abstentions, and 0 countable
external labels.
ESM-2 650M support is implemented as a review-only sidecar path for mapped
controls and selected pilot rows. The current environment still could not
compute `facebook/esm2_t33_650M_UR50D`: the 650M weights are not cached, the
remote weight file is about 2.61 GB, only about 3.2 GiB remained free after the
150M cache, and no MPS backend was available. The sidecars now record the
requested 650M backend as unavailable, fall back to the cached
`facebook/esm2_t30_150M_UR50D` backend for computed review-only rows, record
actual dimension `640` versus requested dimension `1280`, and mark
`requested_650m_or_larger_representation_backend_not_computed`. The 8M-vs-larger
stability audits now report `fallback_changed` for both mapped controls and
selected pilot rows, which is a real representation-control signal rather than a
replacement for a future full 650M control. The selected-pilot adjudication now
uses that signal to reduce the pilot representation surface from 9 generic
blockers to 3 unresolved stability-change rows plus 4 concrete
near-duplicate-holdout rows and 3 stable review-only controls.
`artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json`
prioritizes the current 21 local-evidence repair lanes as 4 reaction/substrate
expert-review lanes, 3 explicit alternate-residue-position sourcing lanes,
3 active-site mapping or structure-selection lanes, and 11 family-boundary
review lanes. `artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json`
closes the 4 reaction/substrate lanes as reviewed out-of-scope repair debt
without adding countable labels; `artifacts/v3_explicit_alternate_residue_position_requests_700.json`
turns the 3 alternate-residue lanes into sourceable evidence requests across
34 alternate PDB structures; and
`artifacts/v3_review_only_import_safety_audit_700.json` confirms the
review-only decision artifacts add 0 countable labels.
The accepted-700 non-countable repair artifacts remain as historical
discovery-facing controls:
`artifacts/v3_mechanism_ontology_gap_audit_700.json` records 115 ontology
scope-pressure rows without creating new families,
`artifacts/v3_learned_retrieval_manifest_700.json` defines a future learned
representation interface with 562 eligible rows and heuristic retrieval as the
control, and `artifacts/v3_sequence_similarity_failure_sets_700.json` keeps the
2 exact-reference duplicate clusters as sequence-similarity failure controls.
The 700 review-debt repair pass now adds structure-aware remediation artifacts:
`artifacts/v3_review_debt_remediation_700.json`,
`artifacts/v3_review_debt_remediation_700_all.json`, and
`artifacts/v3_review_debt_alternate_structure_scan_700.json`. The focused
accepted-700 scan checks 152 candidate PDB structures for the 13 new-debt
structure-scan rows, conservatively remaps selected active-site residue
positions onto 63 alternate-PDB structures, finds 3 structure-wide
cofactor-family hits, and keeps them non-countable because 0 have local
active-site support. The all-debt bounded scan
`artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json`
covers all 46 scan-candidate review-debt rows and all 739 candidate PDB
structures, remaps 362 alternate-PDB structures, and finds review-only local
expected-family hits for `m_csa:577`, `m_csa:592`, and `m_csa:641`.
`artifacts/v3_review_debt_remap_local_lead_audit_700.json` routes
`m_csa:577` and `m_csa:641` to expert family-boundary review and `m_csa:592`
to expert reaction/substrate review, while keeping all three under a strict
non-countable remap guardrail. `artifacts/v3_reaction_substrate_mismatch_audit_700.json`
flags 18 active-queue hydrolase-top1 rows with kinase or ATP phosphoryl-transfer
text for expert reaction/substrate review. The 700 family-propagation guardrail
retains all 24 hydrolase-top1 reaction/substrate mismatch blockers, split
between 17 labeled propagation blocks and 7 unlabeled pending-review blocks.
The accepted-725 repair preview adds a focused scan for 12 new review-debt
rows, covering 140 structures with 0 fetch failures. It finds structure-wide
expected-family hits for `m_csa:712`, `m_csa:718`, and `m_csa:724`; only
`m_csa:712` has local support from a conservative remap, so it is routed to
strict expert family-boundary review and remains non-countable. The 725
ontology-gap audit records 121 review-only scope-pressure rows, the learned
retrieval manifest exposes 568 eligible rows for future representation work,
and the sequence-similarity failure-set audit keeps 2 duplicate clusters as
non-countable propagation controls.
`artifacts/v3_reaction_substrate_mismatch_review_export_700.json` now carries
all 24 lanes together.
`artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json` implements the
expert-reviewed ontology expansion for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK,
PfkA, PfkB, and GHMP. It maps 20 expert-supported mismatch lanes to those
families, records 4 non-target hints for future work, and keeps
`countable_label_candidate_count=0`. The reviewed decision batch remains
review-only while routing the 7 unlabeled rows to reviewed out-of-scope repair
decisions and rejecting 17 controls. Countable import refuses
review-only artifacts even when they carry reviewed repair decisions, so these
lanes cannot enter the benchmark.

The 875, 900, 925, 950, 975, and 1,000 batches accepted 27 clean
automation-curated bronze labels after the accepted 850 state. The latest
1,000 batch accepted `m_csa:978`, `m_csa:988`, `m_csa:990`, and `m_csa:994`;
the 21 new 1,000-preview
review-debt rows remain explicitly non-countable under
`artifacts/v3_accepted_review_debt_deferral_audit_1000.json`. The bounded
1,025 preview is open but not promoted; the real MMseqs2 <=30% sequence
holdout, the 12-row mapped-control ESM-2 8M representation sample, the
10-row selected-pilot ESM-2 8M representation sample, and 650M local-only
feasibility sidecars are now in place. The
first SPOF hardening pass also refactored counterevidence and gate inputs. The
label-factory gate and countable batch-acceptance CLI now record validated
artifact lineage and fail on non-exempt slice mismatches, including
payload-declared slice or batch metadata that contradicts path lineage, while
recording payload methods and digests.
The label scaling-quality audit now applies the same fail-fast lineage check
before promotion-risk classification and records the validated slice lineage in
its artifact metadata.
The external transfer gate now also exposes a typed
`ExternalSourceTransferGateInputs.v1` contract and a shared candidate-lineage
artifact registry so the high-fan-in pilot gate does not keep accreting
one-off lineage branches; the CLI gate command builds that contract from its
artifact map instead of passing another long keyword cascade into the gate, and
the contract rejects non-object artifact payloads at the gate boundary.
The external pilot ranking, no-decision review export, evidence-packet,
pilot-specific representation, and dossier artifacts are now built; the
high-fan-in pilot builders also fail fast on mixed-slice lineage before writing
new packet or dossier artifacts. The next bounded Foldseek item is retrying
round-3 chunk 3 with a longer runtime or smaller query slice, stopping for
adjudication if a target-violating pair appears. External packet decisions
still need active-site sources and broader duplicate-screening evidence beyond
the bounded current-reference MMseqs2 search. Do not resume M-CSA-only count
growth or external label import.
See
`docs/label_factory.md`.

## Quickstart

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m catalytic_earth.cli validate

python -m catalytic_earth.cli build-ledger --out artifacts/source_ledger.json
python -m catalytic_earth.cli fingerprint-demo --out artifacts/mechanism_demo.json
python -m catalytic_earth.cli fetch-rhea-sample --limit 10 --out artifacts/rhea_sample.json
python -m catalytic_earth.cli fetch-mcsa-sample --ids 1,2,3 --out artifacts/mcsa_sample.json
python -m catalytic_earth.cli build-seed-graph --mcsa-ids 1,2,3 --out artifacts/seed_graph.json

python -m catalytic_earth.cli build-v1-graph --max-mcsa 50 --page-size 50 --out artifacts/v1_graph.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph.json --out artifacts/v1_graph_summary.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph.json --out artifacts/v2_benchmark.json
python -m catalytic_earth.cli run-baseline --benchmark artifacts/v2_benchmark.json --out artifacts/v2_baseline.json
python -m catalytic_earth.cli detect-inconsistencies --graph artifacts/v1_graph.json --out artifacts/v2_inconsistencies.json
python -m catalytic_earth.cli mine-dark-hydrolases --limit 100 --out artifacts/v2_dark_hydrolase_candidates.json
python -m catalytic_earth.cli write-dossiers --candidates artifacts/v2_dark_hydrolase_candidates.json --out-dir artifacts/v2_dossiers --top 10
python -m catalytic_earth.cli write-v2-report --out docs/v2_report.md

python -m catalytic_earth.cli label-summary --out artifacts/v3_label_summary.json

python -m catalytic_earth.cli build-v1-graph --max-mcsa 500 --page-size 100 --out artifacts/v1_graph_500.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph_500.json --out artifacts/v1_graph_summary_500.json
python -m catalytic_earth.cli build-sequence-cluster-proxy --graph artifacts/v1_graph_500.json --out artifacts/v3_sequence_cluster_proxy_500.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph_500.json --out artifacts/v2_benchmark_500.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_500.json --max-entries 500 --out artifacts/v3_geometry_features_500.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_500.json --out artifacts/v3_geometry_retrieval_500.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_abstention_calibration_500.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_geometry_label_eval_500.json
python -m catalytic_earth.cli analyze-geometry-failures --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_geometry_failure_analysis_500.json
python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_in_scope_failure_analysis_500.json
python -m catalytic_earth.cli analyze-cofactor-coverage --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_coverage_500.json
python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_policy_500.json
python -m catalytic_earth.cli analyze-seed-family-performance --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_seed_family_performance_500.json
python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_geometry_score_margins_500.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_hard_negative_controls_500.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_label_expansion_candidates_500.json
python -m catalytic_earth.cli build-adversarial-negatives --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_adversarial_negative_controls_500.json
python -m catalytic_earth.cli build-label-factory-audit --retrieval artifacts/v3_geometry_retrieval_500.json --hard-negatives artifacts/v3_hard_negative_controls_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_500.json --abstain-threshold 0.4115 --out artifacts/v3_label_factory_audit_500.json
python -m catalytic_earth.cli apply-label-factory-actions --label-factory-audit artifacts/v3_label_factory_audit_500.json --out artifacts/v3_label_factory_applied_labels_500.json
python -m catalytic_earth.cli build-active-learning-queue --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --label-factory-audit artifacts/v3_label_factory_audit_500.json --abstain-threshold 0.4115 --max-rows 150 --out artifacts/v3_active_learning_review_queue_500.json
python -m catalytic_earth.cli export-label-review --queue artifacts/v3_active_learning_review_queue_500.json --out artifacts/v3_expert_review_export_500.json
python -m catalytic_earth.cli import-label-review --review artifacts/v3_expert_review_export_500.json --out artifacts/v3_expert_review_import_preview_500.json
python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_family_propagation_guardrails_500.json
python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_500.json --applied-label-factory artifacts/v3_label_factory_applied_labels_500.json --active-learning-queue artifacts/v3_active_learning_review_queue_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_500.json --expert-review-export artifacts/v3_expert_review_export_500.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_500.json --out artifacts/v3_label_factory_gate_check_500.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_500.json --out artifacts/v3_structure_mapping_issues_500.json
python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
python -m catalytic_earth.cli perf-suite --graph artifacts/v1_graph_500.json --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --iterations 5 --out artifacts/perf_report.json

python -m catalytic_earth.cli log-work --stage post-v2 --task "example work entry" --minutes 1
python -m catalytic_earth.cli progress-report --out work/status.md
python -m unittest discover -s tests
```

For bounded tranche scaling after an accepted geometry slice, reuse unchanged
geometry rows instead of rebuilding every prior entry:

```bash
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_975.json --max-entries 975 --reuse-existing artifacts/v3_geometry_features_950.json --out artifacts/v3_geometry_features_975.json
```

The commands currently operate on curated seed registries in `data/registries/`.
The first source-specific adapters fetch small Rhea and M-CSA samples and build
a seed graph linking M-CSA entries, EC numbers, catalytic residues, and Rhea
reactions.

The v1 graph command expands this into a persistent graph slice linking M-CSA,
Rhea, UniProt, PDB, and AlphaFold DB cross-references.

Automation runs use the tested `automation-lock` CLI wrapper to acquire the
local run lock and to release it only after clean-tree, no-merge, and
`HEAD == origin/main` checks pass.

## Repository Layout

```text
data/registries/        Seed source and mechanism registries
docs/                   Research protocol and design notes
src/catalytic_earth/    Validation and artifact-building code
tests/                  Unit tests for graph, retrieval, labels, and structure code
artifacts/              Generated local outputs
work/                   Time ledger, scope calibration, and handoff state
```

## Roadmap And Timeline Calibration

The original "one year to v2" framing was too conservative for scaffold
construction. In practice, v0-v2 plus several post-V2 quality upgrades were
implemented quickly because they are bounded computational artifacts, not
expert-validated enzyme discoveries.

Current timeline judgment:

1. Done: public repo, graph slice, mechanism fingerprints, V2 benchmark,
   retrieval baseline, inconsistency detection, dark-enzyme candidate dossiers,
   active-site geometry, ligand/cofactor context, labels, calibration, and
   performance checks.
2. Current automation blocks: keep using the label factory for every new
   tranche. The 1,000 slice is accepted only for its clean countable labels; 326
   review-state rows remain outside the benchmark and now have an explicit
   non-countable deferral audit. Each batch must pass
   promotion/demotion, adversarial-negative, active-learning, expert-review
   export/import, family-propagation, ATP/phosphoryl-transfer family-boundary,
   validation, and test gates before labels count toward the benchmark.
3. Next serious milestone: move beyond M-CSA-only tranche growth. The 1,025
   preview is cleanly non-promotable with 0 accepted labels, and the source
   audit shows only 1,003 M-CSA records are available in the current slice.
   External-source transfer must stay review-only until active-site evidence,
   OOD calibration, sequence-similarity failure controls, heuristic retrieval
   controls, and the full label-factory gate pass.
4. Long-term impact path: expert-reviewed mechanism labels, learned
   geometry-aware retrieval, source-scale ingestion, and candidate dossiers that
   are credible enough for external labs to prioritize.

So the near-term scope is not "build a dashboard for a year." It is to keep
turning fast scaffold progress into increasingly hard, falsifiable mechanism
benchmarks. Real-world impact still requires expert review and wet-lab
validation outside this repository.
