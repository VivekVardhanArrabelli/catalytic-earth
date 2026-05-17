# External Source Transfer 1025 Notes

The M-CSA 1,025 preview is not promotable and should stay a source-limit audit
point: it adds 0 M-CSA countable labels. External-source transfer is now the
active path for post-M-CSA scaling work. The first three countable external
hard-negative imports are `uniprot:P06744`, `uniprot:P78549`, and
`uniprot:Q3LXA3`, bringing the canonical registry to 682 labels.

Current external artifacts:

- `artifacts/v3_external_source_candidate_manifest_1025.json` carries 30
  UniProtKB/Swiss-Prot candidates across six lanes with 0 countable candidates.
- `artifacts/v3_external_source_lane_balance_audit_1025.json` is clean: each
  lane contributes five candidates and the dominant-lane fraction is `0.1667`.
- `artifacts/v3_external_source_candidate_manifest_audit_1025.json` is clean and
  confirms 0 rows are marked ready for label import.
- `artifacts/v3_external_source_evidence_plan_1025.json` requests active-site
  residue positions, curated reaction or mechanism evidence, structure mapping,
  heuristic geometry controls, OOD assignment, sequence holdouts, review
  decisions, and full label-factory gates before import. It flags seven broad
  or incomplete EC-context candidates and routes three broad-only candidates to
  reaction disambiguation before active-site mapping.
- `artifacts/v3_external_source_evidence_request_export_1025.json` exports 30
  no-decision review items and is marked `external_source_review_only`.
- `artifacts/v3_external_source_active_site_evidence_queue_1025.json` prioritizes
  25 review-only candidates for active-site evidence collection and defers five
  rows: two exact-reference holdouts and three broad-EC disambiguation cases.
- `artifacts/v3_external_source_active_site_evidence_sample_1025.json` samples
  all 25 ready rows from UniProtKB features: 15 have active-site features, 10
  are active-site-feature gaps, all 25 have catalytic-activity comments, and 0
  rows are countable or import-ready. The current active-site feature-gap
  accessions are `O60568`, `P29372`, `P27144`, `A2RUC4`, `P51580`, `O95050`,
  `Q9HBK9`, `A5PLL7`, `P32189`, and `Q32P41`.
- `artifacts/v3_external_source_heuristic_control_queue_1025.json` marks 12
  candidates ready for heuristic-control prototyping and defers 13 rows: 10
  active-site-feature gaps and 3 broad-EC disambiguation cases.
- `artifacts/v3_external_source_structure_mapping_plan_1025.json` carries 12
  candidates into structure mapping and keeps 13 deferred.
  `artifacts/v3_external_source_structure_mapping_sample_1025.json` maps all
  12 heuristic-ready candidates onto current AlphaFold CIFs with 0 fetch
  failures and 0 countable labels.
- `artifacts/v3_external_source_heuristic_control_scores_1025.json` runs the
  current geometry-retrieval heuristic on those 12 mapped controls. The top1
  predictions are 9 `metal_dependent_hydrolase`, 2
  `heme_peroxidase_oxidase`, and 1 `flavin_dehydrogenase_reductase`, so
  `artifacts/v3_external_source_failure_mode_audit_1025.json` records top1
  fingerprint collapse, metal-hydrolase collapse, and scope/top1 mismatch as
  review-only failure modes before any external decision artifact can count.
  The audit now records 9 scope/top1 mismatches; glycan-chemistry hydrolase
  controls are tracked separately from non-hydrolase transferase, isomerase,
  lyase, and oxidoreductase mismatch lanes.
- `artifacts/v3_external_source_control_repair_plan_1025.json` turns those
  weaknesses into 25 non-countable repair rows: 10 active-site feature gaps, 3
  broad-EC disambiguation rows, and 12 heuristic-control repair rows.
- `artifacts/v3_external_source_representation_control_manifest_1025.json`
  exposes all 12 mapped controls as future representation rows. Embeddings are
  explicitly not computed, and no row is a training label.
- `artifacts/v3_external_source_representation_control_comparison_1025.json`
  compares feature-proxy controls against the heuristic baseline without
  computing embeddings. It flags 7 metal-hydrolase collapse rows, keeps 2
  glycan-boundary rows as review-only, and creates 0 countable labels.
- `artifacts/v3_external_source_binding_context_repair_plan_1025.json` splits
  the 10 active-site-feature gaps into 7 rows ready for binding-context mapping
  and 3 rows still missing binding context.
- `artifacts/v3_external_source_binding_context_mapping_sample_1025.json` maps
  7/7 binding-context repair rows with 0 fetch failures. These mapped binding
  positions remain repair context only; they are not catalytic active-site
  evidence.
- `artifacts/v3_external_source_active_site_gap_source_requests_1025.json`
  converts all 10 active-site-feature gaps into sourcing requests: 7 have
  mapped binding context and 3 need curated residue sources.
- `artifacts/v3_external_source_review_only_import_safety_audit_1025.json`
  confirms countable import adds 0 labels from that export.
- `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json` runs a
  bounded sequence screen against all 735 current countable M-CSA reference
  accessions after resolving inactive demerged references to replacement
  accessions. It fetches all 30 external sequences, records 0 high-similarity
  alerts under the current unaligned screen, retains the 2 exact-reference
  holdouts, and keeps broader near-duplicate search as a
  mandatory future control.
- `artifacts/v3_external_source_sequence_alignment_verification_1025.json`
  verifies the top 90 sequence-neighborhood pairs with bounded global
  edit-identity checks. It confirms `O15527` and `P42126` as alignment-level
  exact holdouts, records 88 no-signal pairs, and keeps complete search
  mandatory.
- `artifacts/v3_external_source_sequence_reference_screen_audit_1025.json`
  checks whether the current countable-reference sequence screen is complete
  before using it to relax pilot sequence blockers. It now clears the
  current-reference blocker by resolving inactive demerged UniProt references
  `P03176` -> `P0DTH5`/`Q9QNF7` and `Q05489` -> `P0DUB8`/`P0DUB9`, giving
  sequence coverage for all 735 expected current countable reference
  accessions. The artifact is review-only, records 28 current-reference top-hit
  no-signal rows plus the two exact holdouts. The companion
  `artifacts/v3_external_source_all_vs_all_sequence_search_1025.json` covers
  all 30 external candidates with MMseqs2 all-vs-all search, finds 0
  near-duplicate pairs at 90% identity / 80% coverage, and records max
  reported external-external identity `0.647`; UniRef-wide near-duplicate
  search remains mandatory.
- `artifacts/v3_external_source_import_readiness_audit_1025.json` aggregates
  candidate-level blockers: 10 active-site gaps, 2 sequence holdouts,
  remaining UniRef-wide duplicate screening, 9 heuristic scope/top1 mismatches,
  and 29 representation-control issues. It marks 0 rows ready for label import.
- `artifacts/v3_external_source_active_site_sourcing_queue_1025.json` converts
  the 10 active-site gaps into a prioritized non-countable sourcing queue: 7
  mapped-binding-context rows and 3 primary active-site source rows.
- `artifacts/v3_external_source_active_site_sourcing_export_1025.json` packages
  those 10 active-site sourcing tasks with 72 source targets and 0 completed
  decisions.
- `artifacts/v3_external_source_sequence_search_export_1025.json` keeps all 30
  external candidates in no-decision sequence controls: 28 duplicate-search
  controls and 2 sequence holdouts. The prior
  `complete_near_duplicate_reference_search_not_completed` blocker is replaced
  by the bounded current-reference backend screen plus the external all-vs-all
  screen; UniRef-wide search remains the unresolved sequence blocker for the
  28 non-holdout rows.
- `artifacts/v3_external_source_representation_backend_plan_1025.json` covers 12
  mapped representation controls without computing embeddings.
- `artifacts/v3_external_source_kmer_representation_backend_sample_1025.json`
  preserves the deterministic sequence k-mer baseline for those 12 rows and
  flags 1 representation near-duplicate holdout without making any row
  countable.
- `artifacts/v3_external_source_representation_backend_sample_1025.json`
  computes the canonical 12-row ESM-2 representation sample, flags 3
  representation near-duplicate holdouts, and emits learned-vs-heuristic
  disagreements without making any row countable.
- `artifacts/v3_external_source_pilot_representation_backend_plan_1025.json`
  extends the representation backend plan to the 10 selected pilot rows.
  `artifacts/v3_external_source_pilot_representation_backend_sample_1025.json`
  computes ESM-2 embeddings for all 10, flags `P55263` as a representation
  near-duplicate holdout, and keeps every row review-only and non-countable.
  `artifacts/v3_external_source_pilot_representation_adjudication_1025.json`
  now joins that 8M baseline to the largest-feasible ESM-2 stability audit:
  3 pilot rows are stable review-only representation controls, 4 are
  representation near-duplicate holdouts, and 3 need review because the nearest
  reference changed under the 150M fallback. The requested 650M backend remains
  not cached and is not claimed as computed.
- `artifacts/v3_external_source_active_site_sourcing_resolution_1025.json`
  re-checks the 10 active-site-gap rows against UniProt feature evidence,
  records 0 explicit active-site residue sources, and leaves all rows
  non-countable.
- `artifacts/v3_external_source_transfer_blocker_matrix_1025.json` joins all 30
  candidates into a review-only blocker matrix with prioritized next actions.
  The matrix now consumes active-site resolution and representation sample
  packets directly, so the current gate rejects stale matrices that omit those
  row-level blockers.
- `artifacts/v3_external_source_pilot_candidate_priority_1025.json` converts
  that blocker matrix into a bounded review pilot worklist. It selects 10
  candidates (`O14756`, `P06746`, `C9JRZ8`, `P55263`, `P34949`, `Q9BXD5`,
  `Q6NSJ0`, `O60568`, `O95050`, and `P51580`), caps lanes at 2 selected rows,
  defers 5 exact-holdout or near-duplicate rows, and keeps all selected rows
  non-countable and not import-ready. Its leakage policy excludes mechanism
  text, EC/Rhea ids, source labels, and target labels from priority scoring.
- `artifacts/v3_external_source_pilot_review_decision_export_1025.json` exports
  the selected 10 as no-decision review packets with 0 completed decisions.
  It is packet scaffolding only; active-site evidence, sequence search,
  representation controls, reviewed decisions, and full gates still block
  import.
- `artifacts/v3_external_source_pilot_evidence_packet_1025.json` joins source
  targets for the same selected 10. It carries 79 review-only targets, all 10
  sequence-search packets, 3 active-site sourcing packets, and no missing
  required source packets; it is source-packet consolidation only.
- `artifacts/v3_external_source_pilot_evidence_dossiers_1025.json` turns the
  selected 10 into per-candidate review dossiers. Seven have explicit UniProt
  active-site feature support, all 10 have Rhea reaction context, all 10 have
  pilot representation-sample rows, and all 10 still carry import blockers. The
  artifact is review-only and creates 0 countable candidates. The latest
  assembly also adds local evidence-completeness blockers, including explicit
  active-site-evidence blockers for `O60568`, `O95050`, and `P51580`.
- `artifacts/v3_external_source_pilot_active_site_evidence_decisions_1025.json`
  classifies the selected 10 into 7 explicit active-site-source rows and 3
  binding-context-only rows, while keeping every row review-only and
  non-countable.
- `artifacts/v3_external_source_pilot_success_criteria_1025.json` now defines
  measurable pilot success. It requires all 10 selected rows to reach terminal
  decisions with no unresolved process blockers, and requires at least 1
  import-ready row under full gates or a zero-pass result whose failures are
  evidence-explained rather than process-missing.
- `artifacts/v3_external_source_pilot_terminal_decisions_1025.json` now gives
  all 10 selected rows a terminal status: 4 rejected duplicate/near-duplicate
  holdouts, 3 rejected active-site-evidence-missing rows, and 3 rows deferred
  to human expert review. The 3 deferred rows are routed by
  `artifacts/v3_external_source_pilot_human_expert_review_queue_1025.json`;
  UniRef-wide duplicate screening and full factory gates still block import.
- `artifacts/v3_external_source_pilot_needs_review_resolution_1025.json`
  supersedes the normalized 6-row needs-review queue for pilot-decision work.
  The desk review checks local evidence plus UniProtKB/UniRef90/UniRef50,
  Rhea, PDB/AlphaFold, and InterPro context. Targeted UniRef90/50 mapping
  finds 0 shared candidate/current-reference clusters for the nearest-reference
  checks, so duplicate rejection is not supported; all 6 rows are instead
  resolved as terminal review-only `rejected_representation_conflict`
  import-safety decisions. The resolved decision and queue artifacts leave 0
  `needs_review`, 0 import-ready rows, and 0 countable external labels.
- `artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json`
  removes the generic zero-pass repair-lane ambiguity for those 6 resolved
  representation conflicts. It assigns one review-only lane each for
  SDR/NAD(P) redox, AKR/NADP redox, DNA Pol X/5'-dRP lyase,
  sugar-phosphate isomerase, Schiff-base lyase/aldolase, and
  glycoside-hydrolase versus metal-hydrolase boundary repair. These are
  next-code/worklist lanes only; they are not predictive features, import-ready
  decisions, or countable labels.
- `artifacts/v3_external_source_pilot_sdr_redox_repair_control_1025.json`
  implements the first bounded lane control without changing decisions. For
  `O14756`, it stages sequence-derived SDR/NAD(P) control evidence using a
  `TGxxxGxG` glycine-rich proxy and a source-active-site-overlapping `YxxxK`
  proxy, then contrasts that complete SDR axis against the conflicting
  current-reference neighbors. The current-reference neighbors do not carry the
  complete SDR axis, so this removes the unimplemented-control blocker for that
  lane while keeping 0 import-ready and 0 countable rows.
- `artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_1025.json`
  turns the staged O14756 SDR/NAD(P) control into a real import-safety
  adjudication. The non-text sequence rule repairs the prior
  `rejected_representation_conflict` blocker and records post-repair
  `needs_review`, but it keeps the row non-countable and not import-ready
  because broader duplicate screening, a post-repair review decision, and the
  full factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json`
  opens the next lane for `Q6NSJ0`. It stages review-only, non-text boundary
  evidence from source-traced acidic active-site residues, active-site spacing,
  local pocket composition, absent metal/cofactor ligand context, and zero
  metal-hydrolase role-hint support.
- `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_1025.json`
  turns that Q6NSJ0 boundary control into a review-only import-safety
  adjudication. It repairs the prior glycoside-hydrolase versus
  metal-hydrolase representation/heuristic conflict and records post-repair
  `needs_review`, but it keeps the row non-countable and not import-ready
  because broader duplicate screening, a post-repair review decision, and the
  full factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_control_1025.json`
  opens the next lane for `P34949`. It stages review-only, non-text
  scope-control evidence from the source-traced active-site Arg, local pocket
  composition, absent flavin/cofactor context, zero flavin role-hint support,
  and weak top1 score with local `absent_flavin_context` counterevidence.
- `artifacts/v3_external_source_pilot_sugar_phosphate_isomerase_import_safety_adjudication_1025.json`
  turns that P34949 scope control into a review-only import-safety
  adjudication. It repairs the prior weak flavin/scope representation conflict
  and records post-repair `needs_review`, but it keeps the row non-countable
  and not import-ready because broader duplicate screening, a post-repair
  review decision, and the full factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_schiff_base_lyase_control_1025.json`
  opens the next lane for `Q9BXD5`. It stages review-only, non-text
  scope-control evidence from source-traced Tyr/Lys active-site residues, a
  Schiff-base Lys, active-site spacing, local pocket composition, absent
  heme/cofactor context, zero heme/electron-transfer role-hint support, and
  weak heme top1 score with local `absent_heme_context` counterevidence.
- `artifacts/v3_external_source_pilot_schiff_base_lyase_import_safety_adjudication_1025.json`
  turns that Q9BXD5 scope control into a review-only import-safety
  adjudication. It repairs the prior weak heme/scope conflict and records
  post-repair `needs_review`, but it keeps the row non-countable and not
  import-ready because the representation near-duplicate holdout, broader
  duplicate screening, a post-repair review decision, and the full factory gate
  are still unresolved.
- `artifacts/v3_external_source_pilot_akr_nadp_repair_control_1025.json`
  opens the next lane for `C9JRZ8`. It stages review-only, non-text
  AKR/NADP-axis evidence from a sequence-derived `VGLG` cofactor-binding proxy,
  source-traced active-site Tyr, local H/K context, and current-reference
  contrast rows that lack the complete AKR/NADP axis.
- `artifacts/v3_external_source_pilot_akr_nadp_import_safety_adjudication_1025.json`
  turns that C9JRZ8 control into a review-only import-safety adjudication. It
  repairs the prior representation near-duplicate conflict and records
  post-repair `needs_review`, but it keeps the row non-countable and not
  import-ready because heuristic scoring, broader duplicate screening, a
  post-repair review decision, and the full factory gate are still unresolved.
- `artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_1025.json`
  opens the final current repair lane for `P06746`. It stages review-only,
  non-text DNA Pol X/5'-dRP lyase axis evidence from source-active-site
  Lys-72, local basic/acidic sequence context, and current-reference contrast
  rows that lack the complete axis.
- `artifacts/v3_external_source_pilot_dna_pol_x_lyase_import_safety_adjudication_1025.json`
  turns that P06746 control into a review-only import-safety adjudication. It
  repairs the prior representation near-duplicate conflict and records
  post-repair `needs_review`, but it keeps the row non-countable and not
  import-ready because heuristic scoring, broader duplicate screening, a
  post-repair review decision, and the full factory gate are still unresolved.
- `artifacts/v3_external_out_of_scope_inverse_gate_logic_check_1025.json`
  records the current external hard-negative import target explicitly:
  `label_type=out_of_scope`, `fingerprint_id=null`, and
  `ontology_version_at_decision=label_factory_v1_8fp`. The gate requires all
  8 current fingerprint scores below `0.4115`; above-threshold retained hits
  remain false non-abstentions.
- `artifacts/v3_external_sdr_ec_1_1_1_consistency_check_1025.json` supports the
  O14756 attempt with a bounded SDR/NAD(P) consistency check: 36/36 evaluable
  SDR-like Swiss-Prot EC 1.1.1.x rows are clean abstentions, with 0 SDR false
  non-abstentions and 0 predictive leakage rows.
- `artifacts/v3_external_hard_negative_two_candidate_import_attempt_1025.json`
  attempts exactly O14756 and Q6NSJ0. Both pass the all-8 inverse gate, but
  both remain non-countable because broader duplicate screening, post-repair
  review acceptance, and full external factory gates are unresolved.
- `artifacts/v3_external_hard_negative_second_tranche_selection_1025.json`
  starts the next review-only hard-negative selection with P33025, Q13907, and
  P35914. P60174 is excluded by high current-reference identity; Q9BXS1 is
  excluded because Q13907 already represents the same external `TM >=0.7`
  cluster.
- `artifacts/v3_external_hard_negative_second_tranche_current_countable_structural_screen_1025.json`
  runs the admitted tranche-2 rows against the staged current selected
  structures with Foldseek. It completes with 2001/2016 query-target pairs and
  finds high-TM current-countable structural signals for all three admitted
  rows: P33025 to `m_csa:735` at `0.7063`, Q13907 to `m_csa:190` at `0.8686`,
  and P35914 to `m_csa:328` at `0.7638`. The screen is review-only and blocks
  import; 0 rows are countable or import-ready.
- `artifacts/v3_external_hard_negative_second_tranche_terminal_decisions_1025.json`
  converts those signals into terminal review-only decisions. P33025, Q13907,
  and P35914 are all `rejected_current_countable_structural_duplicate_signal`
  outcomes, with 0 import-ready rows and 0 countable labels.
- `artifacts/v3_external_hard_negative_second_tranche_replacement_triage_1025.json`
  triages the existing 25-row external pool after the terminal duplicate
  rejections. It admits 0 replacements: the remaining rows are blocked by the
  current-cycle hard stop, missing active-site/scoring/structure evidence,
  uncovered mechanism lanes, high current-reference identity, same-cluster
  status, or possible existing-fingerprint context.
- `artifacts/v3_external_hard_negative_new_candidate_sourcing_1025.json` starts
  a fresh review-only sourcing surface after that pool exhaustion. It fetches
  up to 12 Swiss-Prot rows per query lane, excludes the existing current
  external pool, keeps only already covered counterevidence lanes, checks
  bounded UniProt active-site/catalytic-activity context, and identifies 8
  sourcing candidates: O75828, O95154, O95479, P04424, Q8N0X4, P30566, Q04760,
  and Q13087. These rows are not a new import tranche yet; they still need
  current-reference sequence search, current-countable structural screening,
  external structural clustering, UniRef-wide duplicate screening, terminal
  review, and the full factory gate.
- `artifacts/v3_external_hard_negative_new_candidate_backend_sequence_search_1025.json`
  screens the 8 sourced rows against the current accepted reference FASTA with
  MMseqs2. The backend succeeds with 8/8 external sequences and 737 current
  reference sequence records: 7 rows have no near-duplicate signal, and Q04760
  is an exact-reference holdout to `m_csa:32`. The audit artifact is clean, but
  these rows remain review-only; structural duplicate screening and UniRef-wide
  duplicate screening still block import.
- `artifacts/v3_external_hard_negative_new_candidate_structural_cluster_index_1025.json`
  stages all 8 sourced AlphaFold structures and completes the external
  all-vs-all structural cache. It covers 28/28 unordered nonself Foldseek
  pairs, forms 7 clusters at `TM >=0.7`, and flags only the P04424/P30566 pair
  as high-TM (`0.8338`). This removes the external-cluster context blocker for
  this sourced surface, not the current-countable structural duplicate blocker.
- `artifacts/v3_external_hard_negative_new_candidate_current_countable_structural_screen_1025.json`
  screens the 7 sequence no-signal sourced rows against 672 current countable
  selected structures. Foldseek completed with 4704/4704 unique query-target
  pairs after multi-model current target names were normalized. All 7
  sequence-clean rows have high-TM current-countable duplicate signals; Q13087
  is no longer a no-signal row because it maps to current selected structure
  1MEK at `TM=0.9039`.
- `artifacts/v3_external_hard_negative_new_candidate_terminal_decisions_1025.json`
  records all 7 sequence-clean fresh candidates as terminal review-only
  `rejected_current_countable_structural_duplicate_signal` outcomes. The fresh
  sourced tranche has 0 import-ready rows and 0 countable candidates.
- `artifacts/v3_external_hard_negative_next_candidate_sourcing_1025.json` starts
  the next replacement sourcing surface after excluding the original 30-row
  pool, the second-tranche duplicate rejects, and all 8 prior fresh sourced
  rows. It admits 8 covered-lane Swiss-Prot rows with explicit UniProt
  active-site plus catalytic-activity context: P00338, P04406, P14060, Q9GZT4,
  P22830, Q8TB92, P78549, and Q3LXA3. These are review-only sourcing rows, not
  an import tranche.
- `artifacts/v3_external_hard_negative_next_candidate_backend_sequence_search_1025.json`
  screens those 8 replacement rows against the current accepted reference FASTA
  with MMseqs2. The backend succeeds with 8/8 no-signal rows, 0 exact-reference
  holdouts, and 0 near-duplicate rows; the companion audit is guardrail-clean.
- `artifacts/v3_external_hard_negative_next_candidate_structural_cluster_index_1025.json`
  stages all 8 replacement AlphaFold coordinate sidecars and completes the
  external all-vs-all structural cache. It covers 28/28 unordered nonself
  Foldseek pairs, forms 8 clusters at `TM >=0.7`, and finds 0 high-TM external
  pairs.
- `artifacts/v3_external_hard_negative_next_candidate_current_countable_structural_screen_1025.json`
  screens the 8 sequence-clean replacement rows against 672 current countable
  selected structures. Foldseek completes 5376/5376 unique query-target pairs:
  5 rows have high-TM current-countable duplicate signals, while P22830,
  P78549, and Q3LXA3 have no current-countable structural duplicate signal.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_decisions_1025.json`
  records terminal review-only outcomes for the replacement surface: 5
  `rejected_current_countable_structural_duplicate_signal` rows and 3
  `deferred_requires_review_and_factory_gate_after_structural_screen` rows.
  The deferred rows initially require UniRef-wide duplicate screening, terminal
  review, and full factory gates; 0 rows are import-ready or countable.
- `artifacts/v3_external_hard_negative_next_candidate_all_vs_all_sequence_search_1025.json`
  runs the bounded external all-vs-all sequence screen for the 8 replacement
  rows using the next-candidate external FASTA. MMseqs2 completes the screen
  with 8/8 no-signal rows, 0 exact/near-duplicate external sequence pairs, and
  a guardrail-clean audit in
  `artifacts/v3_external_hard_negative_next_candidate_all_vs_all_sequence_search_audit_1025.json`.
- `artifacts/v3_external_hard_negative_next_candidate_duplicate_evidence_review_1025.json`
  records the bounded duplicate-evidence status for the 3 deferred rows
  (`P22830`, `P78549`, and `Q3LXA3`). All 3 are
  `bounded_duplicate_controls_clear_uniref_pending`: current-reference
  sequence, external all-vs-all sequence, external structural, and
  current-countable structural controls are clear. UniRef-wide duplicate
  screening, terminal review acceptance, and full factory gates still block all
  3 rows, so 0 rows are import-ready or countable.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_review_queue_1025.json`
  routes those 3 bounded-clear rows into review-only terminal review packets.
  The queue records allowed outcomes, the remaining UniRef-wide and factory
  blockers, and 0 accepted/import-ready/countable rows.
- `artifacts/v3_external_hard_negative_next_candidate_targeted_uniref_check_1025.json`
  queries UniRef for the 3 terminal-review-queued candidates and their nearest
  current structural-reference accessions. `P22830`/`P00518`,
  `P78549`/`P00750`, and `Q3LXA3`/`P06213` share 0 UniRef90/50 clusters, with
  0 fetch failures. This is nearest-reference evidence only; at this stage the
  artifact explicitly preserves the full UniRef-wide duplicate-screening
  blocker.
- `artifacts/v3_external_hard_negative_next_candidate_uniref_current_reference_screen_1025.json`
  fetches each queued candidate's UniRef90 and UniRef50 cluster members and
  intersects them with all 735 current countable reference accessions. P22830,
  P78549, and Q3LXA3 all have 0 current-reference cluster overlaps across 6/6
  fetched candidate clusters.
- `artifacts/v3_external_hard_negative_next_candidate_inverse_gate_scores_1025.json`
  scores those same 3 rows against the current 8-fingerprint ontology using
  UniProt active-site features mapped onto staged AlphaFold sidecars. All 3
  pass the out-of-scope inverse gate at threshold 0.4115: P22830 top1
  metal_dependent_hydrolase 0.3686, P78549 top1
  flavin_dehydrogenase_reductase 0.1150, and Q3LXA3 top1
  metal_dependent_hydrolase 0.2929.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_review_decisions_1025.json`
  records P22830, P78549, and Q3LXA3 as review-only
  accepted_out_of_scope_pending_factory_gate terminal decisions. The remaining
  blocker is the full factory gate; 0 rows are import-ready or countable.
- `artifacts/v3_external_hard_negative_next_candidate_factory_import_gate_1025.json`
  runs that full gate. P22830, P78549, and Q3LXA3 all pass; the single-import
  cap selects P78549 because its maximum current-fingerprint score is lowest
  (`0.1150`). `uniprot:P78549` is now the first countable external
  out-of-scope hard-negative label. P22830 and Q3LXA3 remain unimported under
  `single_import_cap_not_selected_this_run`.
- `artifacts/v3_external_hard_negative_next_candidate_followup_cycle_decision_1025.json`
  keeps the next step review-only. The post-import litmus remains green; P22830
  and Q3LXA3 are eligible for a later explicit single-import cycle, with Q3LXA3
  recommended first because its maximum current-fingerprint score is lower
  (`0.2929` versus `0.3686`).
- `artifacts/v3_external_hard_negative_q3lxa3_single_import_cycle_gate_1025.json`
  opens that explicit later cycle and imports exactly `uniprot:Q3LXA3` after
  terminal review, duplicate evidence, UniRef current-reference screening,
  all-8 inverse-gate scoring, the baseline label-factory gate, and the external
  transfer gate all pass.
- `artifacts/v3_external_hard_negative_q3lxa3_post_import_followup_cycle_decision_1025.json`
  keeps the post-Q3LXA3 litmus green and leaves P22830 review-only for any
  future explicit cycle.
- `artifacts/v3_external_hard_negative_p22830_cycle_deferral_1025.json` records
  the explicit go/no-go decision for the last remaining factory-pass row. A
  temporary later-cycle probe would select P22830, but the row is deferred
  before import because its `0.0429` margin below the active `0.4115`
  out-of-scope floor is inside the conservative deferral band after two
  successful external imports. P22830 remains review-only and non-countable.
- The post-import litmus regression now pins two external count movements:
  681 total labels, 469 out-of-scope labels, 212 seed-fingerprint labels, no
  entry-id overlap between those groups, unchanged 1,000-slice retained
  in-scope behavior, max held-out train/test identity `0.284`, 43/43 retained
  held-out positives correct, and 0 held-out out-of-scope false
  non-abstentions.
- `artifacts/v3_external_structural_cluster_index_1025.json` stages all 10
  selected AlphaFold coordinate sidecars and completes Foldseek
  nearest-neighbor clustering before any split assignment. It finds nine
  clusters at `TM >=0.7`, with only `O95050` and `P51580` grouped, and remains
  review-only with 0 import-ready rows and 0 countable candidates.
- `artifacts/v3_external_structural_tm_holdout_path_1025_all30.json` and
  `artifacts/v3_external_structural_cluster_index_1025_all30.json` now expand
  that structural surface to all 30 current external candidates. The all-30
  cache materializes 30/30 AlphaFold sidecars with 0 fetch failures, completes
  nearest-neighbor coverage for all 30 rows, covers 435/435 unordered nonself
  all-vs-all Foldseek pairs, and records 6 high-TM pairs across 26 pre-split
  clusters.
- `artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json`
  now assigns a review-only cluster-preserving split on the all-30 surface:
  6 test and 24 train candidates, one test row per external lane, 144/144
  cross-split pairs checked, max cross-split TM-score `0.6963`, and 0
  cross-split `TM >=0.7` violations. It remains non-countable and does not
  authorize label import.
- `artifacts/v3_external_source_transfer_gate_check_1025.json` passes 68/68
  checks for review-only evidence collection in the earlier control-repair
  pass; the later control-repair gates passed 38/38 and 41/41 as intermediate
  checkpoints, then 45/45 after sequence-alignment verification and the
  active-site sourcing queue. The current gate now passes 68/68 after the source
  exports, active-site sourcing resolution, representation-backend sample,
  blocker matrix, pilot review-only safeguards, selected-pilot representation
  sample coverage, pilot active-site evidence decisions, and current-reference
  sequence-screen audit. It uses the typed
  `ExternalSourceTransferGateInputs.v1` contract, validates both candidate
  lineage across high-fan-in external artifacts and artifact-path lineage across
  all supplied gate inputs, now includes the sequence-holdout audit and pilot
  representation sample in row-level lineage validation, and fails fast on
  mixed-slice paths, payload-declared slice contradictions, stale holdout rows,
  stale pilot representation rows, or pilot artifacts that stop being
  review-only/no-decision work products. It is still not ready for label import.

Sequence-similarity guardrail details:

- `O15527` overlaps `m_csa:185` and must stay a sequence-holdout control.
- `P42126` overlaps `m_csa:341` and must stay a sequence-holdout control.
- No external candidate is countable from exact-reference or lane membership
  alone.
- `artifacts/v3_external_source_sequence_neighborhood_plan_1025.json` turns the
  current sequence surface into 2 exact-holdout rows and 28 near-duplicate
  search requests.
- `artifacts/v3_external_source_sequence_neighborhood_sample_1025.json` is a
  bounded sequence screen only, not a final homology search. Absence of a
  high-similarity hit in that artifact must not be used as import evidence.
  The current sample resolves inactive demerged references `P03176` and
  `Q05489` conservatively to all listed replacement accessions, so the
  current-reference screen is complete, and the external all-vs-all sequence
  search is now complete for the 30-row sample, but neither is a UniRef-wide
  search.
- `artifacts/v3_external_source_sequence_alignment_verification_1025.json`
  checks only bounded top hits; it confirms the two exact-reference holdouts
  but does not replace full near-duplicate or UniRef-style search.

Reaction-context details:

- `artifacts/v3_external_source_reaction_evidence_sample_1025.json` queries Rhea
  for all 30 external candidates and records 64 reaction-context rows with 0
  fetch failures.
- `artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json` is
  guardrail-clean, with 0 countable candidates and 0 import-ready rows.
- The audit flags 16 broad-EC context rows across `1.1.1.-`, `1.11.1.-`,
  `1.8.-.-`, `2.1.1.-`, `2.7.1.-`, `3.2.2.-`, and `4.2.99.-`. Treat those
  rows as weak reaction context only, not specific mechanism evidence.
- `artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json` finds
  specific reaction context for all 3 broad-only repair rows; 2 still require
  substrate selection among multiple specific reactions.

Sequence-holdout details:

- `artifacts/v3_external_source_sequence_holdout_audit_1025.json` keeps
  `O15527` and `P42126` as exact-reference holdouts and marks the other 28
  external candidates for near-duplicate search before any future import
  decision.

The broader external structural sourcing surface is now durable:
`artifacts/v3_external_hard_negative_broader_structural_sourcing_1025.json`
merges both prior fresh sourcing artifacts, both prior terminal-decision
artifacts, and the P22830 deferral before selecting new rows. The selected
review-only source-evidence candidates are `P14550`, `P15428`, `Q969S2`,
`Q96FI4`, `P06744`, and `Q9BV20`, with a clean three-lane balance profile
(`oxidoreductase_long_tail`, `lyase`, and `isomerase`, two rows each). All six
were non-countable and not import-ready at sourcing time.

The first duplicate screens for those six rows are now complete through the
bounded current-countable structural layer. The current-reference MMseqs2 screen
records 6/6 no-signal rows, and the bounded external all-vs-all sequence screen
finds 0 exact/near-duplicate external sequence pairs. The six-row external
structural cluster index materializes all AlphaFold sidecars, covers 15/15
unordered pairs, and finds 0 high-TM external pairs. The current-countable
Foldseek screen completes
4,032/4,032 query-target pairs and rejects five rows as high-TM
current-countable duplicate risks. Only `P06744` remained deferred with no
current-countable structural duplicate signal before the follow-on duplicate,
terminal review, inverse-gate, and factory evidence cleared.

The follow-on `P06744` artifacts remove the current-reference UniRef duplicate
blocker and the inverse-gate blocker. Bounded duplicate evidence is clear;
targeted UniRef90/50 checks against the nearest current reference show no
shared cluster; the candidate UniRef90/50 current-reference screen has 0
current-reference overlaps; and all 8 current fingerprint scores stay below the
`0.4115` floor with top1 `metal_dependent_hydrolase` score `0.3066`.
`artifacts/v3_external_hard_negative_broader_structural_terminal_review_decisions_1025.json`
accepts `P06744` as out-of-scope pending factory gates, and
`artifacts/v3_external_hard_negative_broader_structural_factory_import_gate_1025.json`
imports exactly `uniprot:P06744` after the baseline label-factory and external
transfer gates pass.

Next bounded work should not retry the five broader duplicate-signal rows,
reopen the six original pilot repair lanes, or import P22830 without an
explicit decision that supersedes the deferral artifact.
