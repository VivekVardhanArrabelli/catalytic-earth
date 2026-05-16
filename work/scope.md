# Scope And Calibration

## Current Thesis

Catalytic Earth should build the missing foundation layer between protein
structure and enzyme chemistry: a mechanism-level atlas of catalytic function.

The project should stay honest about impact. Computational predictions are not
validated enzyme discoveries. The real autonomous contribution is narrowing the
search space and producing auditable hypotheses that expert labs can test.

## Time Calibration Rule

Initial estimates must be revised against observed progress.

Track:

- measured wall-clock minutes spent
- estimated/planned minutes only when a real measurement is unavailable
- concrete artifacts produced
- source integrations completed
- graph size and evidence quality
- benchmark quality
- tests passing
- blockers found

Automation cadence:

- run once per hour
- run on `gpt-5.5` with `xhigh` reasoning
- record the real wall-clock start timestamp
- sync from `origin/main` with `git fetch origin` and
  `git pull --ff-only origin main` before editing
- work productively toward project completion until 50 elapsed wall-clock
  minutes
- if the assigned handoff task is completed early or blocked, write a short
  remaining-time plan and implement the highest-value bounded unblocked next
  item instead of handing off early
- begin wrap-up at 50 elapsed wall-clock minutes
- reserve 5 minutes for break/overhead
- review and update README/docs/work files so they reflect the actual end state;
  if no changes are needed, record that docs were checked
- log the hour
- update `work/handoff.md` for the next automation run
- run checks
- commit and push every run
- verify before handoff that no merge is in progress, local `HEAD` equals
  `origin/main`, and `git status -sb` is clean

If a milestone is completed much faster than expected, increase scope or reduce
timeline. If a milestone stalls because the data are messier than expected,
reduce claims before adding complexity.

## Done So Far

V0 initial scaffold is complete:

- public GitHub repository
- research protocol
- mechanism fingerprint schema
- source registry
- seed mechanism registry
- live Rhea sample ingestion
- live M-CSA sample ingestion
- seed catalytic graph linking M-CSA, EC, catalytic residues, and Rhea
- unit tests

V1 graph foundation is complete:

- persistent JSON graph schema
- M-CSA paginated ingestion beyond hand-picked IDs
- Rhea EC reaction mapping beyond toy samples
- UniProt accession linkage
- PDB and AlphaFold DB structure cross-reference nodes
- provenance on graph nodes and edges
- graph summary command and artifact
- normalization and graph construction tests

V2 first research artifact is complete:

- mechanism-level benchmark records
- token-overlap seed fingerprint retrieval baseline
- leakage controls blocking EC numbers, Rhea identifiers, and source entry ids
- graph inconsistency detector
- bounded unreviewed hydrolase mining campaign
- top candidate dossiers with evidence and uncertainty
- reproducible README command sequence
- paper-style V2 report draft

Post-V2 quality work has started:

- PDB mmCIF structure parsing
- active-site residue coordinate extraction
- bounded Foldseek coordinate-readiness staging and partial staged-coordinate
  TM-score signaling for selected accepted-registry structures; this is
  review-only and does not compute a full TM-score split
- pairwise catalytic-residue distance features
- nearby ligand/cofactor context from mmCIF non-polymer atoms
- geometry artifacts for 20-entry regression, 30-entry, 40-entry, 50-entry,
  60-entry, 75-entry, 100-entry, 125-entry, 150-entry, 175-entry, 200-entry,
  225-entry, 250-entry, 275-entry, 300-entry, 325-entry, 350-entry, 375-entry,
  400-entry, 425-entry, 450-entry, 475-entry, 500-entry, 525-entry, 550-entry,
  575-entry, 600-entry, 625-entry, 650-entry, 675-entry, 700-entry, 725-entry,
  750-entry, 775-entry, 800-entry, 825-entry, 850-entry, 875-entry,
  900-entry, 925-entry, 950-entry, 975-entry, and 1000-entry slices
- auth-vs-label mmCIF residue-number fallback for structure mapping
- curated seed mechanism labels for 679 countable entries, with pending
  review-state evidence gaps kept outside the countable registry
- geometry retrieval evaluation against curated labels
- calibrated abstention threshold sweep
- hard-negative controls, in-scope failure analysis, label-expansion candidate
  ranking, and cross-slice geometry summaries
- label-factory automation with explicit bronze/silver/gold labels, mechanism
  ontology, promotion/demotion audit, active-learning queue, adversarial
  negative controls, family-propagation guardrails, expert-review
  export/import, and a gate check before counting new label batches
- local artifact performance suite

## V1 Target

V1 should make the knowledge graph real enough for benchmark design.

Completion criteria:

- persistent local graph format with stable node and edge schemas
- Rhea ingestion beyond toy samples
- M-CSA ingestion beyond hand-picked IDs
- UniProt linkage for proteins referenced by M-CSA/Rhea
- structure availability metadata for PDB and AlphaFold DB
- provenance attached to every node and edge
- graph summary metrics generated by command
- tests for normalization and graph construction

## V2 Target

V2 should produce the first serious research artifact, not just infrastructure.

Completion criteria:

- mechanism-level benchmark dataset
- baseline predictor or retrieval system
- leakage controls that prevent trivial EC-number prediction
- misannotation or inconsistency detection prototype
- one bounded dark-enzyme mining campaign
- top candidate dossiers with mechanistic rationale and uncertainty
- reproducible commands from clean checkout
- paper-style report draft

## Current Scope Judgment

Observed speed: v0 scaffold and public repo were completed in one session, so a
one-year estimate for v0-v2 is too conservative.

Observed speed after V2: v1-v2 were feasible in another concentrated work
session because the first V2 is deliberately a computational scaffold, not an
expert-validated enzyme discovery program.

Current expectation:

- v2 scaffold: complete
- immediate priority: falsify generalization before adding more gate machinery.
  The first real MMseqs2 sequence-distance holdout now covers the accepted
  countable registry in both the 1,000 and 1,025 slice contexts. It covers
  678/678 evaluated labels, clusters 738 sequence records at 30% identity and
  80% coverage, holds out 136 rows by whole sequence clusters, records max
  observed train/test identity `0.284`, achieves the <=30% target, preserves
  0 held-out out-of-scope false non-abstentions, and reports held-out evaluable
  top1 accuracy, top3 retained accuracy, and retention of `1.0000`. The current
  artifacts also expose explicit backend, resolved path, cluster-threshold,
  target-achievement, and limitation metadata aliases for review and regression
  gates. M-CSA strict Foldseek/TM-score separation is now closed/deferred rather
  than an active benchmark target. The preserved descriptive evidence is the
  all-materializable readiness/signal pair: 672 materializable selected
  coordinates, explicit coordinate exclusions for `m_csa:372` and `m_csa:501`,
  952,922 mapped Foldseek pair rows, 274,241 train/test rows, max observed
  train/test TM-score `0.9749`, and 4,715 target-violating train/test rows.
  `artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json` records
  `full_tm_score_holdout_claim_permitted=false` and treats strict pairwise
  `TM <0.7` as an unsatisfiable native M-CSA proxy driven by curated fold
  density, not merely leakage. The noncanonical staged, expanded,
  query-chunk, query-single, split-repair, split-redesign, and cluster-first
  round artifacts were removed after that adjudication. Further M-CSA
  round32/index145 or round33 repair is explicitly out of scope unless the
  user reverses the decision; strict TM-diverse holdouts now belong on
  broader external structural data with structure clustering before split
  assignment.
  The first 12-row
  ESM-2 8M representation sample and a 10-row selected-pilot ESM-2 8M
  representation sample are computed and review-only; requested 650M sidecars
  now explicitly record the uncached 650M state, compute
  `facebook/esm2_t30_150M_UR50D` as the largest feasible cached fallback, and
  report 8M-vs-larger `fallback_changed` stability rather than pretending a
  650M control was completed. The selected-pilot representation adjudication
  now turns that stability signal into 3 stable review-only rows, 4
  representation near-duplicate holdouts, and 3 stability-change rows that
  still need review.
- external-pilot readiness now has a review-only active-site evidence decision
  artifact for the 10 selected rows. It records 7 explicit active-site source
  rows, 3 binding-context-only rows, 0 countable rows, and 0 import-ready rows.
  A separate success-criteria artifact now makes the pilot completion bar
  explicit: all 10 rows must reach terminal decisions with no unresolved
  process blockers, and at least 1 row must become import-ready under full
  gates unless a zero-pass result is evidence-explained rather than
  process-missing. The first terminal-decision pass now exists for all 10
  selected rows: 4 are rejected as duplicate/near-duplicate representation
  holdouts, 3 are rejected for missing explicit active-site residue evidence,
  and 3 are deferred for human expert adjudication. Those 3 deferred rows are
  now packaged in a review-only human/expert queue with exact unresolved
  evidence, expert questions, and remaining non-human blockers. A follow-on
  confidence audit now conservatively re-checks all 10 terminal decisions and
  normalizes weak hard calls: 4 current decisions remain confident, 3
  representation-only duplicate rejections move to low-confidence
  `needs_review`, and the normalized review queue now carries 6 exact
  questions. The audit now carries the 30-row external all-vs-all sequence
  screen: 0 near-duplicate pairs at 90% identity / 80% coverage, max reported
  external-external identity `0.647`, and UniRef-wide duplicate screening still
  pending. A direct desk-review resolution then checks those six rows against
  local artifacts plus UniProtKB/UniRef90/UniRef50, Rhea, PDB/AlphaFold, and
  InterPro context. Targeted UniRef90/50 mapping finds 0 shared
  candidate/current-reference clusters for the nearest-reference checks, so
  duplicate rejection is not supported; all six rows are instead terminal
  review-only `rejected_representation_conflict` import-safety decisions. The
  resolved pilot surface has 0 `needs_review`, 0 import-ready rows, and 0
  countable external labels. A follow-on repair-lane artifact assigns those
  six representation conflicts to concrete review-only mechanism-control
  lanes: SDR/NAD(P) redox, AKR/NADP redox, DNA Pol X/5'-dRP lyase,
  sugar-phosphate isomerase, Schiff-base lyase/aldolase, and
  glycoside-hydrolase versus metal-hydrolase boundary control. These lanes
  remove generic zero-pass ambiguity but do not add predictive features,
  imports, or countable labels. The first lane implementation now stages a
  review-only SDR/NAD(P) redox sequence-axis control for `O14756`: the source
  row has both a `TGxxxGxG` glycine-rich proxy and a source-active-site
  `YxxxK` proxy, while the conflicting current-reference neighbors lack the
  complete SDR axis. The follow-on import-safety adjudication artifact now
  consumes that non-text control, repairs the O14756 representation-conflict
  blocker, and records post-repair `needs_review`; broader duplicate
  screening, a post-repair review decision, and the full factory gate still
  block import. The next lane now has a bounded `Q6NSJ0` review-only
  glycoside-hydrolase boundary control using source-traced acidic active-site
  residues, active-site spacing, local pocket composition, absent metal/cofactor
  ligand context, and zero metal-hydrolase role-hint support; it is not yet an
  import-safety adjudication. The external structural path now has a
  concrete review-only cluster index for the same 10 selected rows: all 10
  AlphaFold coordinate sidecars are materialized,
  Foldseek completed, nearest-neighbor coverage is 10/10, and the selected
  pilot forms nine `TM >=0.7` clusters with only `O95050`/`P51580` grouped. It
  still has 0 import-ready rows and 0 countable external labels. The broader
  external structural surface now extends to all 30 current candidates:
  `artifacts/v3_external_structural_cluster_index_1025_all30.json` materializes
  30/30 AlphaFold coordinate sidecars, completes nearest-neighbor coverage,
  covers 435/435 unordered nonself all-vs-all Foldseek pairs, and finds 6
  high-TM pairs across 26 pre-split clusters. The review-only
  `artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json`
  assigns 6 test and 24 train candidates, one test row per external lane, with
  max cross-split TM-score `0.6963` and 0 cross-split `TM >=0.7` violations.
  This is structural split evidence only; import/review blockers remain.
- next serious step: keep scaling geometry-aware labels through the factory,
  not by direct bulk curation
- immediate scientific-expansion priority completed: the expert-reviewed
  ATP/phosphoryl-transfer mismatch lane now has durable fingerprint-family
  ontology coverage for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK, PfkA, PfkB, and
  GHMP, wired through guardrails, review exports, active learning, adversarial
  negatives, gates, tests, artifacts, and documentation
- return to factory-gated label scaling toward 10k while preserving quality
  gates; the accepted 1,000 state has 679 countable labels, its 326
  review-state rows have an explicit non-countable deferral audit, and the
  1,025 preview is cleanly non-promotable because it adds 0 countable labels
  while exposing an M-CSA source limit at 1,003 records
- higher-impact work now depends on quality, not more scaffolding
- geometry-aware features are now available for 20-, 30-, 40-, 50-, 60-, 75-,
  100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-, 300-, 325-, 350-, 375-,
  400-, 425-, 450-, 475-, 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, 700-,
  725-, 750-, 775-, 800-, 825-, 850-, 875-, 900-, 925-, 950-, 975-, and
  1000-entry slices; all 100 regression geometry entries are evaluable, the
  1000-entry countable slice has 662/678 labeled rows evaluable and 999 geometry entries with 960
  pairwise geometry
  records
- curated labels now cover 679 entries, with 212 local active-site
  seed-fingerprint positives in the 1000-entry geometry evaluation and 467 total
  out-of-scope labels; every label has explicit tier, review status,
  confidence, evidence score, and evidence provenance fields
- the 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, 700-, 725-, 750-, 775-,
  800-, 825-, 850-, 875-, 900-, 925-, 950-, 975-, and 1000-entry queues have been processed
  through the label factory; accepted batches added 204 labels beyond the
  475-entry source slice and left 326 review-state decisions pending after the
  1000 batch
- label scaling is now gated by the factory: the current 1000 audit proposes 125
  bronze-to-silver promotions, flags 112 abstention/review rows, mines 80
  adversarial negative controls, exports 430 expert-review items from the
  current ranked review cutoff plus all unlabeled candidates from the 1000
  review queue, exports all 321 active `expert_label_decision_needed` rows as
  review-only no-decision items, generates a complete non-countable repair
  candidate summary and repair guardrail audit for those rows, audits and
  exports the 92 priority local-evidence gap lanes as review-only items, emits
  a local-evidence repair plan, verifies review-only import safety, attaches
  the ATP/phosphoryl-transfer family expansion gate, attaches the accepted-1000
  review-debt deferral audit, and passes the 21-check label-factory gate. The
  active-learning queue now includes reaction/substrate
  mismatch and ATP-family boundary ranking terms, and the 1000
  family-propagation guardrail blocks 30 reported rows on the same mismatch
  signal. The dedicated mismatch review export carries all 30 lanes and feeds
  the expert-reviewed ATP/phosphoryl-transfer family expansion. The expansion
  artifact maps supported lanes across all nine target families and keeps
  `countable_label_candidate_count=0`. The review-only import-safety audit
  prevents the reviewed mismatch, expert-decision, and local-evidence decision
  artifacts from adding countable labels. The expert-label decision export
  records 0 countable candidates, and the repair/local-evidence artifacts keep
  all priority lanes non-countable
- counterevidence maintainability is no longer the top single-point blocker:
  the geometry scorer now uses a versioned declarative policy with typed shared
  inputs, rule-level provenance, and explicit mechanism-text leakage flags. The
  label-factory gate has a typed `LabelFactoryGateInputs.v1` contract and a
  table-driven CLI artifact loader so future gate inputs do not keep growing as
  one-off branches. The gate CLI now validates non-exempt artifact slice
  lineage plus payload-declared slice/batch metadata, fails on contradictions,
  and writes lineage metadata, payload methods, and payload digests into the
  gate artifact.
- text-leakage mitigation is now enforced in the geometry scorer as well as the
  representation sample: mechanism text, entry names, labels, EC/Rhea ids,
  source ids, and target labels are excluded from positive retrieval scoring.
  The PLP mechanism-text boost has been replaced by a text-free local
  PLP ligand-anchor feature, with regression tests and refreshed 1,000/1,025
  retrieval, holdout, label-factory, and external heuristic-control artifacts
  preserving 0 hard negatives, 0 near misses, 0 out-of-scope false
  non-abstentions, and 0 countable external labels. Counterevidence artifacts
  now separate structure/local evidence from mechanism-text review context, and
  the 1,000-slice mechanism-text ablation records 157 changed rows, 156
  review-debt rows, 20 top1 route changes, and 0 structure/local guardrail
  losses.
- artifact-lineage hardening has started: the external transfer blocker matrix
  audit now compares row accessions and candidate-manifest source method against
  the candidate manifest and fails on stale or mismatched matrix inputs. The
  countable label-batch acceptance CLI now validates countable/review-state
  label, evaluation, hard-negative, in-scope failure, factory-gate, and
  review-gap lineage before deciding whether a batch can count. The
  label scaling-quality audit now validates non-exempt preview input lineage
  before risk classification and records the checked slice lineage in
  `metadata.artifact_lineage`, so acceptance, review-debt, active-learning,
  hard-negative, repair, and deferral artifacts cannot silently mix source
  slices.
  The external transfer gate now also validates candidate lineage across high-fan-in
  external artifacts through `ExternalSourceTransferGateInputs.v1` and a
  shared candidate-lineage artifact registry. The CLI command now builds that
  typed contract from the artifact map before calling the gate, then fails on
  non-object artifact payloads, unexpected accessions, missing full-coverage
  manifest rows, per-artifact candidate-count drift, stale sequence-holdout
  audit rows, or pilot artifacts that stop being review-only/no-decision work
  products.
  The external import-readiness audit, transfer blocker matrix, pilot evidence
  packet, and pilot evidence dossier builders now share the same fail-fast
  artifact-path lineage loader and record checked 1,025 lineage under
  `metadata.artifact_lineage`, so pilot work cannot silently mix source slices
  before the gate runs.
- selected-PDB single-point mitigation now has a general override path with
  provenance. `artifacts/v3_selected_pdb_override_plan_700.json` applies the
  holo-preference action path for `m_csa:577` and `m_csa:641`, keeps
  `m_csa:592` skipped because its glucokinase reaction/substrate mismatch still
  needs review, and records 0 countable label candidates. The 1,000-context
  selected-PDB override geometry/retrieval/evaluation artifacts preserve 0 hard
  negatives, 0 near misses, 0 out-of-scope false non-abstentions, and 0
  actionable in-scope failures. Ready override rows now fail before geometry
  write if their entries, residue node ids, or current selected PDB provenance
  do not match the selected graph slice.
- external pilot prioritization now has a review-only 10-row worklist:
  `artifacts/v3_external_source_pilot_candidate_priority_1025.json` selects
  lane-balanced candidates from the 30-row external blocker matrix, defers exact
  holdout and near-duplicate rows, and keeps 0 countable or import-ready rows.
  `artifacts/v3_external_source_pilot_review_decision_export_1025.json` exports
  those rows as no-decision review packets with 0 completed decisions.
  `artifacts/v3_external_source_pilot_evidence_packet_1025.json` consolidates
  79 review-only source targets for the same candidates, including all 10
  sequence-search packets, all 10 backend no-signal statuses, and 3 active-site
  sourcing packets. The pilot-specific
  representation sample now computes ESM-2 embeddings for all 10 selected
  candidates, flags `P55263` as a representation near-duplicate holdout, and
  keeps every selected row non-countable and not import-ready.
- external sequence controls now repair a current-reference coverage gap instead
  of silently treating the bounded screen as complete. The screen now covers all
  735 expected current countable M-CSA reference accessions because
  `artifacts/v3_external_source_sequence_reference_screen_audit_1025.json`
  resolves inactive demerged UniProt references `P03176` and `Q05489` to their
  replacement accessions. `artifacts/v3_external_source_backend_sequence_search_1025.json`
  now uses MMseqs2 18-8cc5c to compare 30 external rows against 735 current
  reference accessions / 737 sequence records. It preserves exact holdouts
  `O15527` and `P42126`, records 28 no-signal rows, 0 near-duplicate rows, and
  0 failures, and keeps every row review-only, non-countable, and not
  import-ready. The bounded current-reference backend search debt is cleared
  for the 28 no-signal rows; the external all-vs-all sequence screen covers
  the current 30-row sample with 0 near-duplicate pairs; UniRef-wide duplicate
  screening remains active. The refreshed pilot packet and dossiers consume
  this backend status so selected no-signal rows no longer retain stale
  complete-near-duplicate sequence blockers.
- review-debt triage now ranks 326 evidence-gap rows from the 1000 review pass,
  with 326 `needs_more_evidence` decisions, 305 carried rows, 21 new rows, and
  explicit non-countable deferral coverage for every row
- strengthened geometry scoring reaches top1/top3/retained accuracy of 1.0 on
  the 38 in-scope positives in the 125-entry slice at the current zero-false
  threshold
- ligand/cofactor context is now parsed from nearby mmCIF non-polymer atoms and
  used in retrieval scoring; structure-wide ligand inventory is also recorded
  for cofactor coverage audits
- substrate-pocket descriptors are now included in retrieval scoring; next
  bottleneck is margin robustness plus larger and cleaner curated labels
- adaptive abstention thresholds now use observed score boundaries; the
  20-entry regression slice has a zero-false threshold that retains all 7
  in-scope positives
- all countable slices from 20 through 1000 currently have 0 hard negatives,
  0 near misses, and 0 out-of-scope false non-abstentions at the current
  calibrated thresholds
- the 725-entry countable slice retains 159/163 in-scope positives, has 4
  evidence-limited in-scope abstentions, and has a 0.0131 correct-positive
  separation gap; the actionable in-scope failure count is 0 after separating
  selected-structure cofactor gaps from scorer failures
- the 20-, 30-, 40-, 50-, 60-, 75-, and 100-entry structure-mapping issue
  reports currently have 0 non-OK mappings after auth/label residue-number
  fallback; the 125-entry report has 1 labeled out-of-scope
  insufficient-residue issue, the 150- and 175-entry reports each have 2, the
  200-, 225-, 250-, 275-, and 300-entry reports each have 3, and the 325-,
  350-, 375-, 400-, 425-, 450-, 475-, 500-, 525-, 550-, 575-, 600-, 625-,
  650-, 675-, 700-, and 725-entry reports have 4, 5, 7, 7, 7, 7, 7, 8, 8, 10,
  11, 11, 15, 17, 17, 19, and 21 respectively; later accepted reports rise to
  23 at 750, 27 at 775, 28 at 800, 29 at 825, 30 at 850, 31 at 875, 33 at
  900, 34 at 925, 38 at 950 and 975, and 39 at 1000
- next bottleneck is external-source transfer, not another M-CSA-only tranche.
  The 1,025 preview gate passes 21/21, but batch acceptance is false because 0
  new labels are cleanly countable and review debt rises to 329 rows. The source
  audit records 1,003 observed M-CSA source records against the requested 1,025
  tranche, so the 10,000-label target requires a separate UniProtKB/Swiss-Prot
  style transfer method with OOD calibration, sequence-similarity controls,
  external evidence collection, and heuristic-control comparison. The first
  30-row external sample now has a review-only candidate manifest, evidence
  plan/export, import-safety audit, active-site feature sampling, structure
  mapping, heuristic-control scoring, failure-mode audit, control-repair
  artifacts, representation-control comparison, broad-EC disambiguation,
  active-site gap source requests, sequence-neighborhood controls, bounded
  sequence-neighborhood screening, bounded sequence-alignment verification,
  sequence-search export, backend current-reference and all-vs-all sequence
  searches, import-readiness audit, active-site sourcing
  queue/export/resolution, representation-backend plan/sample, transfer blocker
  matrix, active-site pilot decisions, pilot success criteria, and a 68/68
  transfer gate with direct current-reference sequence-screen and backend
  sequence-search checks;
  2 exact-reference overlaps are routed to holdout controls, the
  lane-balance audit confirms six evenly represented query lanes, a
  full Rhea reaction-context sample collects 64 review-only reaction records
  across all 30 external candidates while flagging 16 broad-EC context rows,
  the evidence plan flags
  7 broad/incomplete EC candidates, the active-site evidence queue exports 25
  ready review-only candidates while deferring 5 rows, the active-site feature
  pass finds 15 feature-supported rows and 10 gaps, the expanded AlphaFold
  mapping sample resolves all 12 heuristic-ready controls, the heuristic
  control collapses 9/12 controls to metal hydrolase top1 with 9 scope/top1
  mismatches, the repair plan creates 25 non-countable repair rows, the
  representation-control comparison flags 7 metal-hydrolase collapse rows and
  2 glycan-boundary rows, the broad-EC audit finds specific reaction context for
  all 3 broad-only repair rows, the active-site gap source-request artifact
  covers all 10 active-site gaps, the sequence-neighborhood plan scopes
  sequence-search controls for 28 rows, the bounded sequence screen checks all 30
  external sequences against 735 current countable M-CSA reference accessions
  with 0 high-similarity alerts after resolving inactive demerged references
  `P03176` and `Q05489`, bounded alignment verification checks 90 top-hit pairs and
  confirms the two exact-reference holdouts, the backend sequence-search
  artifact uses MMseqs2 18-8cc5c over 30 external rows against 735 current
  reference accessions / 737 sequence records, preserves exact holdouts
  `O15527` and `P42126`, records 28 no-signal rows, 0 near-duplicate rows, and
  0 failures, and removes the bounded current-reference backend search debt for
  the 28 no-signal rows; the external all-vs-all sequence screen covers 30/30
  rows with 0 near-duplicate pairs while UniRef-wide duplicate screening remains
  blocked, the
  import-readiness audit records 0
  import-ready rows plus 10 active-site gaps, 9 heuristic scope/top1
  mismatches, 29 representation-control issues, 2 exact sequence holdouts, and
  UniRef-wide duplicate-screening limitations, the active-site sourcing queue
  prioritizes 7 mapped-binding-context rows and 3 primary-source rows, the
  active-site sourcing export carries 72 source targets, the sequence-search
  export plus backend search keeps all 30 rows review-only, non-countable, and
  not import-ready,
  the active-site sourcing resolution finds 0 explicit active-site residue
  sources across the 10 gap rows, the representation-backend plan covers 12
  controls without embeddings, the deterministic k-mer baseline covers all 12
  controls and flags one representation near-duplicate holdout, the canonical
  ESM-2 sample covers all 12 controls, flags three representation
  near-duplicate holdouts, emits 12 learned-vs-heuristic disagreements, and
  now marks heuristic fingerprint ids, matched M-CSA reference ids, and scope
  signals as review or holdout context rather than predictive evidence, the
  transfer blocker matrix keeps all 30 candidates non-countable with explicit
  next actions and now prioritizes 7 literature/PDB active-site reviews,
  3 primary active-site source tasks, 9 select/run real representation-backend
  actions, 6 compute/attach representation-control actions,
  3 representation-near-duplicate holdouts, and 2 sequence holdouts, the
  pilot-priority artifact selects 10
  non-countable candidates and defers 5 holdout or near-duplicate rows, the
  pilot review-decision export keeps 10 selected rows as no-decision packets,
  the pilot evidence packet consolidates 79 source targets for review, the
  pilot-specific ESM-2 sample covers all 10 selected candidates with 9 complete
  learned-representation rows and 1 representation near-duplicate holdout, the
  pilot dossiers now carry representation rows for all 10 selected candidates
  while preserving 3 explicit-active-site blockers, and 0 external labels are
  countable.
  The accepted 1000 clean labels are `m_csa:978`, `m_csa:988`, `m_csa:990`,
  and `m_csa:994`; the other 326 accepted-1000 review-state rows remain
  outside the benchmark and now have an explicit deferral audit. `m_csa:986` is
  the current scaling-quality regression row for local heme support below the
  abstention floor that should stay non-countable.
  The 725 scaling-quality audit observes
  ontology scope pressure, family-propagation boundaries, cofactor ambiguity,
  reaction/substrate mismatches, active-site mapping gaps, and active-learning
  queue concentration in deferred rows, while the sequence-cluster proxy reports
  0 missing assignments and 0 near-duplicate hits among audited rows. The
  725 remediation artifacts expose all 100 review-debt rows, all 24 new rows,
  a focused 140-structure alternate-PDB scan for 12 new rows, and a strict
  remap-local audit that routes `m_csa:712` to expert family-boundary review.
  The reaction mismatch audit flags 18 active-queue hydrolase-top1 rows with
  kinase or ATP phosphoryl-transfer text, while the dedicated mismatch export
  covers all 24 family-guardrail lanes and all remain non-countable. The
  ATP/phosphoryl transfer expansion remains ready and non-countable. The
  mechanism ontology gap audit records 121 review-only scope-pressure rows, the
  learned-retrieval manifest exposes 568 eligible rows for future
  representation work with heuristic controls, and the sequence-similarity
  failure-set audit keeps the 2 exact-reference duplicate clusters as
  non-countable propagation controls. The
  alternate path is
  resolving
  review-state/evidence-limited rows
  (`m_csa:494`, `m_csa:510`, `m_csa:529`, `m_csa:534`, `m_csa:650`,
  `m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430`), while ensuring
  evidence-limited retained positives (`m_csa:41`, `m_csa:108`, `m_csa:160`,
  `m_csa:446`, and `m_csa:486`) remain audit-visible and preserving the
  zero-hard-negative guardrail
- local performance is now measured for current artifacts; full-source
  scalability remains unmeasured

This estimate must keep being revised from the progress log, not from vibes.
