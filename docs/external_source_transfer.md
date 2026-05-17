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
- External hard-negative imports now target `label_type=out_of_scope` with
  `fingerprint_id=null` under ontology version `label_factory_v1_8fp`.
  `artifacts/v3_external_out_of_scope_inverse_gate_logic_check_1025.json`
  confirms that the external post-repair path uses the same inverse condition
  as label-factory out-of-scope evidence: all 8 current fingerprint scores must
  stay below the active abstention floor (`0.4115`), with retained
  above-threshold hits treated as false non-abstentions.
- `artifacts/v3_external_sdr_ec_1_1_1_consistency_check_1025.json` records the
  bounded SDR/NAD(P) lane check: 36/36 evaluable SDR-like Swiss-Prot EC 1.1.1.x
  rows were clean abstentions, 0 were SDR false non-abstentions, and 0
  text/annotation leakage rows were used as predictive support.
- The first two-candidate hard-negative import attempt is closed without count
  growth. `O14756` and `Q6NSJ0` both pass the all-8 out-of-scope inverse gate,
  but `artifacts/v3_external_hard_negative_two_candidate_import_attempt_1025.json`
  keeps both blocked by unresolved broader duplicate screening, post-repair
  review acceptance, and full external factory-gate state.
- Because both first candidates failed strict import readiness,
  `artifacts/v3_external_hard_negative_second_tranche_selection_1025.json`
  starts the next review-only tranche with 3 lower-risk candidates (`P33025`,
  `Q13907`, and `P35914`). They are not import-ready or countable; external
  all-30 TM clustering is used only to pick one representative per high-TM
  external cluster.
- `artifacts/v3_external_hard_negative_second_tranche_current_countable_structural_screen_1025.json`
  removes the "not run" status for bounded current-countable structural
  duplicate screening but blocks all three tranche-2 rows: Foldseek completed
  against 672 staged current selected structures, reported 2001/2016 query-
  target pairs, and found high-TM current-countable structural signals for
  `P33025` (`0.7063`), `Q13907` (`0.8686`), and `P35914` (`0.7638`). No
  tranche-2 row is import-ready or countable; UniRef-wide duplicate screening,
  terminal review acceptance, and full factory gates remain unresolved.
- `artifacts/v3_external_hard_negative_second_tranche_terminal_decisions_1025.json`
  records terminal review-only decisions for those three tranche-2 rows:
  all are `rejected_current_countable_structural_duplicate_signal`, with 0
  import-ready rows and 0 countable external labels.
- `artifacts/v3_external_hard_negative_second_tranche_replacement_triage_1025.json`
  triages the remaining current 25-row pool after those terminal rejections and
  admits 0 replacements. The next hard-negative tranche needs new external
  candidate sourcing or new evidence, not another import attempt from the same
  pool.
- `artifacts/v3_external_hard_negative_new_candidate_sourcing_1025.json` begins
  that next sourcing pass without opening an import attempt. It fetches a
  bounded expanded Swiss-Prot surface, excludes the current external pool,
  keeps only lanes already covered by existing counterevidence work, and finds
  8 new rows with explicit UniProt active-site plus catalytic-activity source
  context. They are sourcing candidates only; all still need sequence,
  structural, UniRef-wide duplicate, terminal-review, and factory-gate screens.
- `artifacts/v3_external_hard_negative_new_candidate_backend_sequence_search_1025.json`
  completes the first bounded current-reference sequence screen for those 8
  sourced rows. Seven rows have no near-duplicate signal against the current
  accepted reference FASTA, while `Q04760` is an exact-reference holdout. The
  companion audit is guardrail-clean, but the result remains review-only and
  still does not satisfy structural, UniRef-wide, terminal-review, or factory
  gates.
- `artifacts/v3_external_hard_negative_new_candidate_structural_cluster_index_1025.json`
  stages AlphaFold structures for those 8 sourced rows and completes the
  external all-vs-all Foldseek cache. The cache covers 28/28 unordered pairs,
  forms 7 clusters at `TM >=0.7`, and flags the `P04424`/`P30566` pair at
  `0.8338`.
- `artifacts/v3_external_hard_negative_new_candidate_current_countable_structural_screen_1025.json`
  now screens the 7 sequence no-signal rows against current countable selected
  structures. Foldseek completed with a fully mapped 4704/4704 pair cache after
  multi-model current target aliases were normalized. All 7 rows have high-TM
  current-countable duplicate signals; `Q13087` maps to current selected
  structure `1MEK` at `TM=0.9039`, so it is no longer a no-signal candidate.
- `artifacts/v3_external_hard_negative_new_candidate_terminal_decisions_1025.json`
  records all 7 sequence-clean fresh candidates as terminal review-only
  `rejected_current_countable_structural_duplicate_signal` outcomes with 0
  import-ready rows and 0 countable candidates. This closes the fresh sourced
  tranche without authorizing import.
- `artifacts/v3_external_hard_negative_next_candidate_sourcing_1025.json`
  starts the next review-only hard-negative sourcing surface. It excludes the
  original 30-row pool, the second-tranche rejects, and all 8 prior fresh
  sourced rows, then admits 8 replacement covered-lane Swiss-Prot rows with
  explicit UniProt active-site plus catalytic-activity source context.
- `artifacts/v3_external_hard_negative_next_candidate_backend_sequence_search_1025.json`
  completes the bounded current-reference MMseqs2 screen for those 8
  replacements. All 8 have no current-reference near-duplicate signal, with 0
  exact-reference holdouts and a guardrail-clean audit. They remain
  review-only.
- `artifacts/v3_external_hard_negative_next_candidate_structural_cluster_index_1025.json`
  stages all 8 replacement AlphaFold coordinate sidecars and completes the
  external all-vs-all Foldseek cache. The cache covers 28/28 unordered pairs,
  forms 8 clusters at `TM >=0.7`, and finds 0 high-TM external pairs.
- `artifacts/v3_external_hard_negative_next_candidate_current_countable_structural_screen_1025.json`
  screens those 8 sequence-clean rows against current countable selected
  structures. Foldseek completes 5376/5376 unique query-target pairs: 5 rows
  have high-TM current-countable duplicate signals, and 3 rows (`P22830`,
  `P78549`, `Q3LXA3`) have no current-countable structural duplicate signal.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_decisions_1025.json`
  records 5 review-only duplicate-signal rejections and 3 review-only
  deferrals that still require UniRef-wide duplicate screening, terminal
  review, and full factory gates. No replacement row is import-ready or
  countable.
- `artifacts/v3_external_hard_negative_next_candidate_all_vs_all_sequence_search_1025.json`
  and its audit complete the bounded external all-vs-all sequence screen for
  those 8 replacements. All 8 rows have no external sequence near-duplicate
  signal, and the audit remains guardrail-clean while explicitly preserving
  the UniRef-wide duplicate-screening blocker.
- `artifacts/v3_external_hard_negative_next_candidate_duplicate_evidence_review_1025.json`
  summarizes the 3 deferred rows (`P22830`, `P78549`, `Q3LXA3`): bounded
  current-reference sequence, external all-vs-all sequence, external
  structural, and current-countable structural controls are clear, but
  UniRef-wide duplicate screening, terminal review acceptance, and full factory
  gates still block import. No replacement row is import-ready or countable.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_review_queue_1025.json`
  packages those 3 bounded-clear rows into review-only terminal review packets
  with explicit allowed outcomes and remaining non-human blockers. It removes
  only the review-packet scaffolding gap; 0 rows are accepted, import-ready, or
  countable.
- `artifacts/v3_external_hard_negative_next_candidate_targeted_uniref_check_1025.json`
  performs a targeted UniRef90/50 check against each deferred row's nearest
  current structural-reference accession. `P22830` vs `P00518`, `P78549` vs
  `P00750`, and `Q3LXA3` vs `P06213` all have no shared UniRef90/50 cluster.
  This reduces nearest-reference duplicate concern but does not replace the
  required UniRef-wide duplicate screen.

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
M-CSA strict Foldseek/TM-score separation is now closed/deferred rather than an active target. The preserved descriptive structural evidence is `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json` plus `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`: 672 materializable selected coordinates, explicit coordinate exclusions for `m_csa:372` and `m_csa:501`, 952,922 mapped Foldseek pair rows, 274,241 train/test rows, max train/test TM-score `0.9749`, and 4,715 target-violating train/test rows. `artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json` records `full_tm_score_holdout_claim_permitted=false` and states that strict pairwise `TM <0.7` is not a native M-CSA holdout target without destructive split repair. The noncanonical staged, expanded, query-chunk, query-single, split-repair, split-redesign, and cluster-first round artifacts were removed after their aggregate lesson was captured. Do not resume round32/index145, round33, or any further M-CSA partition repair unless the user explicitly reverses that decision. Future strict TM-diverse holdouts belong on broader external structural data such as Swiss-Prot/UniProt/AFDB candidates, with structure clustering before split assignment. The first review-only path artifact, `artifacts/v3_external_structural_tm_holdout_path_1025.json`, covers the 10 selected pilot candidates, confirms all 10 have AlphaFold DB structure ids and 7 have PDB references, and defines the required structure-index, nearest-neighbor, and cluster caches without authorizing import. `artifacts/v3_external_structural_cluster_index_1025.json` now materializes all 10 selected AlphaFold coordinate sidecars, completes a Foldseek nearest-neighbor cache, and clusters the pilot at `TM >=0.7` before any split assignment; only `O95050`/`P51580` cluster together, and 0 rows become countable or import-ready. The broader review-only structural surface now uses `artifacts/v3_external_structural_tm_holdout_path_1025_all30.json`, `artifacts/v3_external_structural_cluster_index_1025_all30.json`, and `artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json`: all 30 current external candidates have AlphaFold sidecars, the Foldseek all-vs-all cache covers 435/435 unordered nonself pairs, 6 high-TM pairs form 26 pre-split clusters, and the review-only split assigns 6 test / 24 train candidates with max cross-split TM-score `0.6963` and 0 cross-split `TM >=0.7` pairs. No external row becomes countable or import-ready.

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
  the 28 no-signal rows and the external candidate all-vs-all MMseqs2 screen
  as complete for the current 30-row sample, while still requiring UniRef-wide
  duplicate screening before import;
- advance the 10 selected pilot-priority candidates with explicit active-site
  evidence, specific reaction evidence, clean sequence holdout status, clean
  structure mapping, non-collapsed retrieval/representation behavior, and no
  broad-EC ambiguity;
- treat the 6 formerly normalized `needs_review` rows (`O14756`, `P06746`,
  `C9JRZ8`, `P34949`, `Q9BXD5`, and `Q6NSJ0`) as resolved for this pilot pass:
  `artifacts/v3_external_source_pilot_needs_review_resolution_1025.json`
  records targeted UniRef90/50 no-shared-cluster checks plus source-mechanism
  review, and
  `artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json`
  closes them as review-only `rejected_representation_conflict` outcomes.
  Next external work should therefore focus on representation/heuristic repair
  policy or a broader external fold-diverse structural surface, not re-opening
  those six rows without new evidence.
- `artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json`
  now classifies the 10 selected pilot rows as review-only active-site evidence
  decisions: 7 have explicit active-site source evidence, 3 have binding
  context only, 0 are countable, and 0 are import-ready. This removes the
  pilot source-status ambiguity blocker, but every selected row still requires
  UniRef-wide duplicate screening, representation-control review, a completed
  review decision, and the full label-factory gate before import.
- `artifacts/v3_external_source_pilot_success_criteria_1025.json` defines the
  pilot success bar rather than treating evidence assembly as completion.
  Operational success means all 10 selected rows reach terminal decisions with
  no unresolved process blockers. Scientific/import success means at least 1
  row becomes import-ready under full gates, or a zero-pass outcome where every
  failure is evidence-explained rather than process-missing.
- `artifacts/v3_external_source_pilot_terminal_decisions_1025.json` records the
  first terminal pass for the 10 selected pilot candidates: 4
  representation-near-duplicate holdouts are rejected as
  `rejected_duplicate_or_near_duplicate`, 3 binding-context-only rows are
  rejected as `rejected_active_site_evidence_missing`, and 3 rows with explicit
  active-site evidence are `deferred_requires_human_expert` for representation
  stability or heuristic-scope adjudication. The pass has 0 import-ready rows,
  0 countable label candidates, and no external label import authorization.
- `artifacts/v3_external_source_pilot_human_expert_review_queue_1025.json`
  routes the 3 deferred rows (`O14756`, `P34949`, and `Q6NSJ0`) into a
  review-only human/expert queue with the exact unresolved evidence, expert
  question, and remaining non-human blockers. It removes only the deferred-row
  routing blocker; UniRef-wide duplicate screening and full label-factory gates
  still block import.
- `artifacts/v3_external_source_pilot_decision_confidence_audit_1025.json`
  audits every selected terminal decision against active-site evidence,
  duplicate/near-duplicate evidence, representation controls, heuristic
  controls, review decisions, structure controls, and factory-gate state. It
  records 4 confident current decisions, 3 low-confidence current hard
  duplicate rejections, and 3 existing needs-review rows. It now carries the
  external all-vs-all screen evidence showing 0 selected-row external
  near-duplicate hits while preserving the remaining UniRef-wide blocker.
- `artifacts/v3_external_source_pilot_decisions_review_normalized_1025.json`
  normalizes the post-audit decision surface to the accepted vocabulary:
  6 `needs_review`, 3 `rejected_active_site_evidence_missing`, 1
  `rejected_duplicate_or_near_duplicate`, 0 import-ready, and 0 countable rows.
  `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_1025.json`
  routes all 6 `needs_review` rows (`O14756`, `P06746`, `C9JRZ8`, `P34949`,
  `Q9BXD5`, and `Q6NSJ0`) with exact unresolved questions. This removes the
  immediate pilot-decision confidence blocker without adding import authority.
- `artifacts/v3_external_source_pilot_needs_review_resolution_1025.json`
  actively resolves those 6 rows by desk review. Local active-site, reaction,
  sequence, representation, heuristic, and structural artifacts were checked
  with UniProtKB/UniRef90/UniRef50 source context; targeted UniRef90/50 mapping
  found 0 shared candidate/current-reference clusters for the nearest-reference
  checks, so duplicate rejection is not supported. All 6 rows are nevertheless
  terminal review-only `rejected_representation_conflict` import-safety
  decisions because source-supported mechanisms conflict with current
  representation or heuristic controls. The resolved decisions and queue
  artifacts leave 0 `needs_review`, 0 import-ready rows, and 0 countable
  external labels.
- `artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json`
  converts those 6 review-only representation conflicts into concrete
  mechanism repair lanes without changing any decision: SDR/NAD(P) redox,
  AKR/NADP redox, DNA Pol X/5'-dRP lyase, sugar-phosphate isomerase,
  Schiff-base lyase/aldolase, and glycoside-hydrolase versus
  metal-hydrolase boundary control. This removes the generic zero-pass
  repair-lane ambiguity; the lanes are not predictive features, import-ready
  rows, or countable labels.
- `artifacts/v3_external_source_pilot_sdr_redox_repair_control_1025.json`
  implements the first bounded repair-lane control for the SDR/NAD(P) row
  `O14756`. It stages only sequence-derived control evidence: a `TGxxxGxG`
  glycine-rich NAD(P)-binding proxy plus a source-active-site-overlapping
  `YxxxK` proxy, and contrasts that signal against the conflicting
  current-reference neighbors, which lack the complete SDR axis. This removes
  the "no implemented repair-lane control" blocker for one lane.
- `artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_1025.json`
  now integrates that control into the O14756 import-safety decision path. The
  non-text rule treats the complete candidate SDR axis, source-active-site
  `YxxxK` overlap, absent complete SDR axes among current-reference neighbors,
  and bounded sequence-search no-signal status as enough to repair the
  representation-conflict blocker. O14756 still remains review-only and
  post-repair `needs_review`, with 0 import-ready/countable rows, because
  broader duplicate screening, a post-repair review decision, and the full
  factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json`
  starts the next repair lane for `Q6NSJ0` as review-only non-text control
  evidence. It uses source-traced acidic active-site residues, active-site
  spacing, local pocket composition, absent local metal/cofactor ligand
  context, and zero metal-hydrolase role-hint support to separate the
  glycoside-hydrolase boundary from the broad metal-hydrolase heuristic
  collapse.
- `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_1025.json`
  now integrates the Q6NSJ0 boundary control into the import-safety path. The
  non-text rule treats the acidic active-site pair, active-site spacing, absent
  local metal/cofactor context, zero metal-hydrolase role-hint support, and
  bounded sequence-search no-signal status as enough to repair the
  glycoside-hydrolase versus metal-hydrolase representation/heuristic conflict.
  Q6NSJ0 still remains review-only and post-repair `needs_review`, with 0
  import-ready/countable rows, because broader duplicate screening, a
  post-repair review decision, and the full factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_control_1025.json`
  starts the P34949 sugar-phosphate isomerase lane as review-only non-text
  scope-control evidence. It uses the source-traced active-site Arg, local
  pocket composition, absent flavin/cofactor ligand context, zero flavin
  role-hint support, and weak top1 score with local `absent_flavin_context`
  counterevidence to separate mannose-6-phosphate isomerase scope from the
  weak flavin-redox heuristic top1.
- `artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_import_safety_adjudication_1025.json`
  now integrates the P34949 scope control into the import-safety path. The
  non-text rule treats the source-traced active-site Arg, local pocket
  composition, absent flavin/cofactor context, zero flavin role-hint support,
  weak top1 score with `absent_flavin_context` counterevidence, and bounded
  sequence-search no-signal status as enough to repair the weak flavin/scope
  representation conflict. P34949 still remains review-only and post-repair
  `needs_review`, with 0 import-ready/countable rows, because broader duplicate
  screening, a post-repair review decision, and the full factory gate are still
  unresolved.
- `artifacts/v3_external_source_pilot_schiff_base_lyase_control_1025.json`
  starts the Q9BXD5 Schiff-base lyase/aldolase lane as review-only non-text
  scope-control evidence. It uses source-traced Tyr/Lys active-site residues,
  a Schiff-base Lys, active-site spacing, local pocket composition, absent
  heme/cofactor ligand context, zero heme/electron-transfer role-hint support,
  and weak heme top1 score with local `absent_heme_context` counterevidence to
  separate N-acetylneuraminate lyase scope from the weak heme-peroxidase
  heuristic top1.
- `artifacts/v3_external_source_pilot_schiff_base_lyase_import_safety_adjudication_1025.json`
  now integrates the Q9BXD5 scope control into the import-safety path. The
  non-text rule repairs the weak heme/scope conflict but deliberately leaves
  the representation near-duplicate holdout unresolved. Q9BXD5 remains
  review-only and post-repair `needs_review`, with 0 import-ready/countable
  rows, because representation holdout review, broader duplicate screening, a
  post-repair review decision, and the full factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_akr_nadp_repair_control_1025.json`
  starts the C9JRZ8 AKR/NADP lane as review-only non-text control evidence.
  It uses a sequence-derived `VGLG` cofactor-binding proxy, source-traced
  active-site Tyr, local H/K context, and current-reference contrast rows that
  lack the complete AKR/NADP axis.
- `artifacts/v3_external_source_pilot_akr_nadp_import_safety_adjudication_1025.json`
  now integrates the C9JRZ8 control into the import-safety path. The non-text
  rule repairs the representation near-duplicate conflict, but deliberately
  leaves heuristic scoring, broader duplicate screening, post-repair review,
  and the full factory gate unresolved. C9JRZ8 remains review-only and
  post-repair `needs_review`, with 0 import-ready/countable rows.
- `artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_1025.json`
  starts the P06746 DNA Pol X/5'-dRP lyase lane as review-only non-text
  control evidence. It uses the source-active-site Lys-72 residue, local
  basic/acidic sequence context, and current-reference contrast rows that lack
  the complete DNA Pol X/5'-dRP lyase axis.
- `artifacts/v3_external_source_pilot_dna_pol_x_lyase_import_safety_adjudication_1025.json`
  now integrates the P06746 control into the import-safety path. The non-text
  rule repairs the representation near-duplicate conflict, but deliberately
  leaves heuristic scoring, broader duplicate screening, post-repair review,
  and the full factory gate unresolved. P06746 remains review-only and
  post-repair `needs_review`, with 0 import-ready/countable rows.
- `artifacts/v3_external_structural_cluster_index_1025.json` removes the
  selected-pilot structure-index blocker by staging all 10 AlphaFold coordinate
  sidecars, recording SHA-256 digests, running Foldseek, and caching
  nearest-neighbor clusters before any split assignment. It finds 9 clusters at
  `TM >=0.7`, with only `O95050` and `P51580` grouped; this is review-only
  structural evidence and not a split, import, or label-count artifact.
- `artifacts/v3_external_structural_tm_holdout_path_1025_all30.json` and
  `artifacts/v3_external_structural_cluster_index_1025_all30.json` expand the
  external fold-diverse structural surface beyond the 10 selected pilot rows:
  30/30 AlphaFold coordinate sidecars are materialized with 0 fetch failures,
  Foldseek nearest-neighbor coverage is complete for all 30 rows, the
  all-vs-all pair cache covers 435/435 unordered nonself pairs, and the
  pre-split surface has 6 high-TM pairs across 26 clusters.
- `artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json`
  assigns a review-only, cluster-preserving external structural split after the
  complete all-vs-all cache: 6 test and 24 train candidates, one test row per
  external lane, 144/144 cross-split pairs checked, max cross-split TM-score
  `0.6963`, and 0 cross-split `TM >=0.7` violations. This removes the
  split-assignment blocker but still authorizes 0 imports and 0 countable
  external labels.
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
  current-reference backend sequence-search debt for the 28 no-signal rows.
  `artifacts/v3_external_source_all_vs_all_sequence_search_1025.json` runs
  the same MMseqs2 backend all-vs-all across the 30 external candidates,
  covers 30/30 sequences, finds 0 near-duplicate pairs, records max reported
  external-external identity `0.647`, and keeps all rows review-only. UniRef-wide
  duplicate screening remains mandatory before import. The bounded top-hit
  alignment verification checks 90
  sequence-neighborhood pairs, confirms the two exact-reference holdouts by
  alignment, and finds 88 no-signal top-hit pairs.
- The import-readiness audit aggregates the current blockers by candidate: 10
  active-site gaps, 2 exact sequence holdouts, 9 heuristic scope/top1
  mismatches, 29 representation-control issues, and the remaining UniRef-wide
  duplicate-screening limitation. It keeps 0 rows import-ready. The active-site
  sourcing queue turns the 10 active-site gaps into 7 mapped-binding-context
  sourcing rows and 3 primary-source rows, and the active-site sourcing export
  packages 72 source targets without decisions. The active-site sourcing
  resolution re-checks all 10 active-site-gap rows against UniProt feature
  evidence, finds 0 explicit active-site residue sources, and leaves the rows
  non-countable. The sequence-search export plus backend search keep all 30
  candidates in no-decision sequence controls: 28 bounded current-reference
  no-signal rows, 2 exact sequence holdouts, external all-vs-all no-signal
  rows, and UniRef-wide duplicate screening still pending.
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
  3 unresolved rows, UniRef-wide duplicate screening still required for all 10,
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

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-all-vs-all-sequence-search \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --external-fasta artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --result-tsv-out artifacts/v3_external_source_all_vs_all_sequence_search_1025.tsv \
  --backend auto \
  --out artifacts/v3_external_source_all_vs_all_sequence_search_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-all-vs-all-sequence-search \
  --all-vs-all-sequence-search artifacts/v3_external_source_all_vs_all_sequence_search_1025.json \
  --candidate-manifest artifacts/v3_external_source_candidate_manifest_1025.json \
  --out artifacts/v3_external_source_all_vs_all_sequence_search_audit_1025.json

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

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-sdr-redox-repair-control \
  --repair-lanes artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json \
  --needs-review-resolution artifacts/v3_external_source_pilot_needs_review_resolution_1025.json \
  --pilot-representation-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --pilot-larger-representation-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --pilot-representation-stability-audit artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --external-sequence-fasta artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --reference-sequence-fasta artifacts/v3_external_source_backend_sequence_search_reference_1025.fasta \
  --curated-labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_external_source_pilot_sdr_redox_repair_control_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-sdr-redox-import-safety-adjudication \
  --sdr-redox-repair-control artifacts/v3_external_source_pilot_sdr_redox_repair_control_1025.json \
  --resolved-pilot-decisions artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json \
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --pilot-success-criteria artifacts/v3_external_source_pilot_success_criteria_1025.json \
  --out artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-glycoside-hydrolase-boundary-control \
  --repair-lanes artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json \
  --needs-review-resolution artifacts/v3_external_source_pilot_needs_review_resolution_1025.json \
  --pilot-representation-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --pilot-larger-representation-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --pilot-representation-stability-audit artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --external-sequence-fasta artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --out artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-glycoside-hydrolase-import-safety-adjudication \
  --glycoside-hydrolase-boundary-control artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json \
  --resolved-pilot-decisions artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json \
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --pilot-success-criteria artifacts/v3_external_source_pilot_success_criteria_1025.json \
  --out artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-sugar-phosphate-isomerase-control \
  --repair-lanes artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json \
  --needs-review-resolution artifacts/v3_external_source_pilot_needs_review_resolution_1025.json \
  --pilot-representation-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --pilot-larger-representation-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --pilot-representation-stability-audit artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --external-sequence-fasta artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --out artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_control_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-sugar-phosphate-isomerase-import-safety-adjudication \
  --sugar-phosphate-isomerase-control artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_control_1025.json \
  --resolved-pilot-decisions artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json \
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --pilot-success-criteria artifacts/v3_external_source_pilot_success_criteria_1025.json \
  --out artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_import_safety_adjudication_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-schiff-base-lyase-control \
  --repair-lanes artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json \
  --needs-review-resolution artifacts/v3_external_source_pilot_needs_review_resolution_1025.json \
  --pilot-representation-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --pilot-larger-representation-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --pilot-representation-stability-audit artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --external-sequence-fasta artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --out artifacts/v3_external_source_pilot_schiff_base_lyase_control_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-schiff-base-lyase-import-safety-adjudication \
  --schiff-base-lyase-control artifacts/v3_external_source_pilot_schiff_base_lyase_control_1025.json \
  --resolved-pilot-decisions artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json \
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --pilot-success-criteria artifacts/v3_external_source_pilot_success_criteria_1025.json \
  --out artifacts/v3_external_source_pilot_schiff_base_lyase_import_safety_adjudication_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-dna-pol-x-lyase-repair-control \
  --repair-lanes artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json \
  --needs-review-resolution artifacts/v3_external_source_pilot_needs_review_resolution_1025.json \
  --pilot-representation-sample artifacts/v3_external_source_pilot_representation_backend_sample_1025.json \
  --pilot-larger-representation-sample artifacts/v3_external_source_pilot_representation_backend_esm2_t33_650m_ur50d_sample_1025.json \
  --pilot-representation-stability-audit artifacts/v3_external_source_pilot_representation_backend_esm2_t6_8m_vs_t33_650m_stability_audit_1025.json \
  --heuristic-control-scores artifacts/v3_external_source_heuristic_control_scores_1025.json \
  --external-sequence-fasta artifacts/v3_external_source_backend_sequence_search_external_1025.fasta \
  --reference-sequence-fasta artifacts/v3_external_source_backend_sequence_search_reference_1025.fasta \
  --curated-labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-pilot-dna-pol-x-lyase-import-safety-adjudication \
  --dna-pol-x-lyase-repair-control artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_1025.json \
  --resolved-pilot-decisions artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json \
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
  --external-import-readiness-audit artifacts/v3_external_source_import_readiness_audit_1025.json \
  --pilot-success-criteria artifacts/v3_external_source_pilot_success_criteria_1025.json \
  --out artifacts/v3_external_source_pilot_dna_pol_x_lyase_import_safety_adjudication_1025.json

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
  --pilot-active-site-evidence-decisions artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json \
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

For the current 8-fingerprint ontology, the only allowed external hard-negative
import target is `out_of_scope` with a null fingerprint id and
`ontology_version_at_decision=label_factory_v1_8fp`. A candidate must have a
complete all-8 inverse score check below the active abstention floor, clean
duplicate evidence, a terminal post-repair review acceptance, and full
label-factory gates before any registry import. A source-supported mechanism
description or repaired representation conflict alone is never import-ready.
