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
`artifacts/v3_external_source_pilot_success_criteria_1025.json` makes the
pilot success definition measurable instead of implicit. Operational success
requires all 10 selected candidates to reach terminal decisions with no
unresolved process blockers. Scientific/import success requires at least 1
candidate to become import-ready under full gates, or a zero-pass result where
every failure is explained by concrete evidence rather than missing process.
`artifacts/v3_external_source_pilot_terminal_decisions_1025.json` now records
the first terminal decision pass for all 10 selected candidates: 4 are rejected
as duplicate/near-duplicate holdouts, 3 are rejected for missing explicit
active-site residue evidence, and 3 are deferred to human expert review because
representation or heuristic evidence remains non-terminal. There are still 0
import-ready rows and 0 countable external labels.
`artifacts/v3_external_source_pilot_human_expert_review_queue_1025.json`
packages those 3 deferred rows (`O14756`, `P34949`, and `Q6NSJ0`) into a
review-only expert queue with the exact unresolved evidence, expert question,
and remaining non-human blockers for each row. It authorizes 0 imports and 0
countable external labels.
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
and review consumers. Full Foldseek/TM-score separation on native M-CSA is now closed/deferred, not an active benchmark target. The preserved descriptive structural evidence is `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json` plus `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`: 672 materializable selected coordinates for 676 materializable evaluated rows, explicit coordinate exclusions for `m_csa:372` and `m_csa:501`, 952,922 mapped Foldseek pair rows, 274,241 train/test rows, max observed train/test TM-score `0.9749`, and 4,715 target-violating train/test rows. `artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json` records `full_tm_score_holdout_claim_permitted=false` and treats strict pairwise `TM <0.7` as an unsatisfiable native M-CSA proxy: M-CSA over-represents common catalytic folds because it is curated for well-characterized catalytic mechanisms, and repeated split-repair/cluster-first rounds added constraints without producing a claimable structural holdout. The noncanonical staged, expanded, query-chunk, query-single, split-repair, split-redesign, and cluster-first round artifacts have been removed and should not be regenerated to force M-CSA below the threshold. The clean MMseqs2 sequence-identity holdout remains valid M-CSA generalization evidence. Future strict TM-diverse holdouts belong on external, fold-diverse structural data with structure clustering before split assignment; `artifacts/v3_external_structural_tm_holdout_path_1025.json` scopes that review-only path for the 10 selected external pilot candidates and authorizes 0 countable/import-ready rows.
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
new packet or dossier artifacts. The M-CSA strict TM-score repair loop is now
adjudicated closed/deferred by
`artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json`: the
all-materializable M-CSA signal observed max train/test TM-score `0.9749`, so
`full_tm_score_holdout_claim_permitted=false` remains correct and further
round32/index145 or round33 repair work should not be resumed. Strict
TM-diverse holdouts should be designed from broader external structural data
with structure clustering before split assignment; the first review-only path
artifact is `artifacts/v3_external_structural_tm_holdout_path_1025.json`,
which covers the 10 selected external pilot rows, requires pre-split structure
clustering, and creates 0 countable/import-ready rows. External packet
decisions still need active-site sources and broader duplicate-screening
evidence beyond the bounded current-reference MMseqs2 search. Do not resume
M-CSA-only count growth or external label import.
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
