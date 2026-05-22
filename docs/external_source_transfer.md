# External Source Transfer

The 1,025 preview shows that M-CSA-only tranche growth is no longer the right
path to 10,000 countable labels. The current M-CSA slice exposes 1,003 source
records, while the benchmark target is 10,000 countable labels. External-source
transfer is therefore a new methodology, not a continuation of M-CSA label
import.

## Current State

- Canonical countable labels now total 682: the accepted 679-label M-CSA
  surface plus three external out-of-scope hard negatives, `uniprot:P06744`,
  `uniprot:P78549`, and `uniprot:Q3LXA3`.
- The 1,025 preview passes 21/21 label-factory gates but adds 0 clean countable
  labels.
- All 329 preview review-state rows remain non-countable.
- Most external UniProtKB/Swiss-Prot artifacts remain review-only; the
  next-candidate factory/import gate was the first countable exception, the
  later explicit Q3LXA3 cycle was the second, and the broader structural
  factory/import gate is the third. Each authorizes exactly one external
  out-of-scope import.
- The current external deepening surface has five mechanism-match review-ready
  rows across heme and metal lanes, but none is import-ready.
  `artifacts/v3_external_mechanism_match_review_ready_uniref_payload_plan_20260522.json`
  screens those five rows against UniRef90/50 cluster members and all 735
  current countable reference accessions. All five have 0 current-reference
  cluster overlaps and 0 fetch failures, but the artifact remains review-only:
  full label-factory gates, external seed-fingerprint import policy, and any
  human label action are still absent, and the metal phosphatase rows still lack
  source-free phosphate/substrate specificity.
- `artifacts/v3_heme_peroxidase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522.json`
  closes the five remaining frozen heme-peroxidase rows from the 2026-05-21
  mini-campaign without adding external breadth. Four rows are exact current-
  reference sequence duplicates and terminal duplicate/leakage rejections.
  `P14532` remains blocked with a specific missing-evidence statement:
  source-free heme geometry and current-countable structural duplicate
  screening are still absent. The companion benchmark makes no geometry
  superiority claim because this packet is sequence-duplicate closure evidence.
- `artifacts/v3_flavin_dehydrogenase_third_deep_terminal_decision_packet_sequence_duplicate_closure_20260522.json`
  closes the six remaining frozen flavin dehydrogenase/reductase rows from the
  2026-05-21 mini-campaign without adding external breadth. Four rows are exact
  current-reference sequence duplicates and terminal duplicate/leakage
  rejections. `P33371` and `P32340` remain blocked with a specific
  missing-evidence statement: source-free FDR active-site geometry and
  current-countable structural duplicate screening are still absent. The
  companion benchmark makes no geometry superiority claim because this packet
  is sequence-duplicate closure evidence.
- `artifacts/v3_external_deep_remaining_blocker_queue_20260522.json` is the
  non-countable follow-up queue for the current external deepening surface. It
  keeps five mechanism-match rows blocked on explicit label-factory payload
  policy/gates and keeps `P14532`, `P33371`, and `P32340` blocked on
  coordinate materialization, source-free geometry, plus current-countable
  structural duplicate screening. It adds 0 rows, imports 0 labels, and
  excludes EC/name/source prose from predictive evidence.
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
- `artifacts/v3_external_hard_negative_next_candidate_factory_import_gate_1025.json`
  runs the full final gate for `P22830`, `P78549`, and `Q3LXA3`. All three pass
  the candidate factory gate; the single-import cap selects `P78549` because it
  has the lowest maximum current-fingerprint score (`0.1150`). The resulting
  accepted review item imports `uniprot:P78549` as an external `out_of_scope`
  hard-negative label with `fingerprint_id=null`.
- `artifacts/v3_external_hard_negative_q3lxa3_single_import_cycle_gate_1025.json`
  opens the explicit later single-import cycle recommended by the follow-up
  decision. It allows the prior `uniprot:P78549` label only as lineage, then
  imports exactly `uniprot:Q3LXA3` after the same terminal-review, duplicate,
  UniRef current-reference, all-8 inverse-gate, baseline label-factory, and
  external-transfer checks pass. `P22830` remains non-countable.
- The post-import litmus regression now pins the expected count movement and
  invariants: label count 682, out-of-scope count 470, seed-fingerprint count
  212, zero overlap between in-scope and out-of-scope entry ids, unchanged
  1,000-slice in-scope retention (`0.9858`), and the sequence-distance holdout
  target (`max identity 0.284`, 43/43 retained held-out positives correct, 0
  held-out false non-abstentions).
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
  deferrals that initially require UniRef-wide duplicate screening, terminal
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
  structural, and current-countable structural controls are clear, but at this
  point UniRef-wide duplicate screening, terminal review acceptance, and full
  factory gates still block import. No replacement row is import-ready or
  countable.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_review_queue_1025.json`
  packages those 3 bounded-clear rows into review-only terminal review packets
  with explicit allowed outcomes and remaining non-human blockers. It removes
  only the review-packet scaffolding gap; 0 rows are accepted, import-ready, or
  countable.
- `artifacts/v3_external_hard_negative_next_candidate_targeted_uniref_check_1025.json`
  performs a targeted UniRef90/50 check against each deferred row's nearest
  current structural-reference accession. `P22830` vs `P00518`, `P78549` vs
  `P00750`, and `Q3LXA3` vs `P06213` all have no shared UniRef90/50 cluster.
- `artifacts/v3_external_hard_negative_next_candidate_uniref_current_reference_screen_1025.json`
  expands that duplicate check from nearest-reference pairs to each candidate's
  UniRef90 and UniRef50 cluster members against all 735 current countable
  reference accessions. `P22830`, `P78549`, and `Q3LXA3` all have 0
  current-reference cluster overlaps. This removes the UniRef current-reference
  duplicate blocker for those 3 rows.
- `artifacts/v3_external_hard_negative_next_candidate_inverse_gate_scores_1025.json`
  scores those 3 rows against all 8 current fingerprints from UniProt
  active-site features mapped onto the staged AlphaFold sidecars. All 3 pass
  the out-of-scope inverse gate at threshold `0.4115`: `P22830` top1
  `metal_dependent_hydrolase` `0.3686`, `P78549` top1
  `flavin_dehydrogenase_reductase` `0.1150`, and `Q3LXA3` top1
  `metal_dependent_hydrolase` `0.2929`.
- `artifacts/v3_external_hard_negative_next_candidate_terminal_review_decisions_1025.json`
  records all 3 as review-only `accepted_out_of_scope_pending_factory_gate`
  decisions. Terminal review acceptance is no longer the active blocker for
  this surface.
- `artifacts/v3_external_hard_negative_next_candidate_factory_import_gate_1025.json`
  then completes the full final gate for this surface. It marks all 3 rows as
  factory-gate pass candidates, selects `P78549` under the single-import cap,
  and imports exactly one external out-of-scope hard-negative label. `P22830`
  and `Q3LXA3` remain unimported and non-countable in this cycle.
- `artifacts/v3_external_hard_negative_next_candidate_followup_cycle_decision_1025.json`
  resolves the immediate follow-up without count growth. The post-import
  litmus remains green, `P22830` and `Q3LXA3` are review-only candidates for a
  later explicit single-import cycle, and `Q3LXA3` is the recommended next
  target because its max current-fingerprint score is lower (`0.2929`).
- `artifacts/v3_external_hard_negative_q3lxa3_single_import_cycle_gate_1025.json`
  then imports exactly `Q3LXA3` in that later explicit cycle. The follow-up
  artifact after that import leaves `P22830` review-only and requires another
  explicit cycle before any further count growth.
- `artifacts/v3_external_hard_negative_q3lxa3_post_import_followup_cycle_decision_1025.json`
  records the post-Q3LXA3 litmus: 681 total labels, 469 out-of-scope labels,
  unchanged in-scope and held-out sequence-distance invariants, and `P22830` as
  the only remaining factory-pass row eligible for a future explicit cycle.
- `artifacts/v3_external_hard_negative_p22830_cycle_deferral_1025.json` records
  the explicit P22830 no-go decision. The formal later-cycle probe would select
  P22830, but its inverse-gate margin is only `0.0429` below the active
  `0.4115` floor, inside the conservative deferral band after two successful
  imports. The canonical registry therefore remains 681 labels and P22830 stays
  review-only pending broader external structural sourcing or a later explicit
  user decision.
- `artifacts/v3_external_hard_negative_broader_structural_sourcing_1025.json`
  starts that broader review-only sourcing path with durable multi-prior
  exclusions. It excludes the original 30-row pool, second-tranche rejects,
  both prior fresh sourced surfaces, prior terminal duplicate rejections, and
  the explicit P22830 deferral, then applies a two-per-lane cap. The selected
  source-evidence rows are `P14550`, `P15428`, `Q969S2`, `Q96FI4`, `P06744`,
  and `Q9BV20`, spanning oxidoreductase, lyase, and isomerase lanes. The lane
  balance guardrail is clean, but all six rows remain non-countable and still
  require sequence, structural, UniRef-wide duplicate, terminal-review, and
  factory-gate screens before any import attempt.
- `artifacts/v3_external_hard_negative_broader_structural_backend_sequence_search_1025.json`
  completes the bounded current-reference MMseqs2 screen for those six rows:
  all six have no near-duplicate signal against the current countable reference
  FASTA, with 0 exact-reference and 0 near-duplicate rows. The audit is
  guardrail-clean and remains review-only.
- `artifacts/v3_external_hard_negative_broader_structural_all_vs_all_sequence_search_1025.json`
  completes the bounded six-row external all-vs-all sequence screen. It finds
  0 exact/near-duplicate external sequence pairs and remains review-only; this
  does not replace UniRef-wide duplicate screening.
- `artifacts/v3_external_hard_negative_broader_structural_tm_holdout_path_1025.json`
  and `artifacts/v3_external_hard_negative_broader_structural_cluster_index_1025.json`
  stage the six-row structural surface. All six AlphaFold sidecars are
  materialized, the external all-vs-all Foldseek cache covers 15/15 unordered
  pairs, and no external pair reaches `TM >=0.7`.
- `artifacts/v3_external_hard_negative_broader_structural_current_countable_structural_screen_1025.json`
  then screens the six rows against 672 current countable selected structures.
  Foldseek completes 4,032/4,032 query-target pairs: five rows have high-TM
  current-countable duplicate signals and only `P06744` has no current-countable
  structural duplicate signal. `artifacts/v3_external_hard_negative_broader_structural_terminal_decisions_1025.json`
  records the five duplicate-signal rows as review-only rejections and defers
  `P06744` behind UniRef-wide duplicate screening, terminal review, and full
  factory gates. No broader-surface row is import-ready or countable.
- `artifacts/v3_external_hard_negative_broader_structural_duplicate_evidence_review_1025.json`,
  `artifacts/v3_external_hard_negative_broader_structural_terminal_review_queue_1025.json`,
  `artifacts/v3_external_hard_negative_broader_structural_targeted_uniref_check_1025.json`,
  `artifacts/v3_external_hard_negative_broader_structural_uniref_current_reference_screen_1025.json`,
  and `artifacts/v3_external_hard_negative_broader_structural_inverse_gate_scores_1025.json`
  advance only `P06744`. Its bounded duplicate controls are clear, targeted
  UniRef90/50 nearest-reference checks find no shared cluster, the current-
  reference UniRef screen finds 0 current-reference cluster overlaps, and all
  8 current fingerprint scores remain below the `0.4115` out-of-scope floor
  with top1 `metal_dependent_hydrolase` score `0.3066`.
- `artifacts/v3_external_hard_negative_broader_structural_terminal_review_decisions_1025.json`
  accepts `P06744` as out-of-scope pending factory gates, and
  `artifacts/v3_external_hard_negative_broader_structural_factory_import_gate_1025.json`
  completes the full gate, allows prior external labels only as lineage, and
  imports exactly `uniprot:P06744` with `fingerprint_id=null` and
  `ontology_version_at_decision=label_factory_v1_8fp`.
- `artifacts/v3_external_hard_negative_post_p06744_sourcing_1025.json` starts
  the next review-only sourcing surface after the third external import. It
  excludes prior imported, deferred, and duplicate-signal rows, selects
  `P23921`, `P26439`, `P09104`, `P13929`, `Q15084`, and `Q96JJ7` across three
  covered lanes, and keeps import/count fields false. The companion bounded
  current-reference and external all-vs-all sequence screens both find 6/6
  no-signal rows with guardrail-clean audits. The structural follow-up
  materializes all six AlphaFold sidecars, completes the 15/15 external
  all-vs-all Foldseek cache, and the current-countable Foldseek screen rejects
  all six as structural duplicate signals. The terminal decision artifact
  records 0 import-ready rows and 0 countable candidates.
- `artifacts/v3_prospective_external_minicampaign_decision_packet_20260520.json`
  records the first post-ePK-synthesis prospective mini-campaign as a frozen
  12-row, three-lane review-only decision packet. MMseqs2 finds 11 bounded
  current-reference no-signal rows and one exact-reference holdout (`P07237`).
  The follow-on coordinate materialization artifact stages all 11 AlphaFold
  sidecars, and the current-countable Foldseek screen completes 7392/7392
  query-target pairs against 672 staged current countable coordinate groups.
  All 11 sequence-clean rows are rejected as current-countable structural
  duplicate signals, leaving 0 import-ready rows and 0 countable candidates.
- `artifacts/v3_prospective_external_minicampaign_sequence_baseline_diagnostic_20260520.json`
  compares that same frozen set against the bounded MMseqs2 result and a
  deterministic 5-mer nearest-neighbor baseline from committed FASTA sidecars.
  It now agrees with the terminal surface: 12/12 rows are rejected, including
  11 current-countable structural duplicate signals. It still flags `P31040`
  as a sequence-neighbor caveat, but the completed structural duplicate screen
  is the stronger terminal blocker. The diagnostic authorizes no import,
  superiority claim, registry edit, or production fingerprint change.
- `artifacts/v3_prospective_external_source_gap_minicampaign_freeze_20260520.json`
  freezes a second, different 18-row review-only mini-campaign from the
  post-P06744 sourcing surface before outcome scoring. It targets source-gap
  rows rather than rerunning the closed structural-duplicate set: six missing
  active-site-source rows, six source-specificity/sampling-gap rows, and six
  uncovered methyltransferase-lane rows. The companion decision packet,
  `artifacts/v3_prospective_external_source_gap_minicampaign_decision_packet_20260520.json`,
  records all 18 as terminal pre-scoring rejections, with 0 sequence-screened,
  0 Foldseek-screened, 0 inverse-gate-scored, 0 import-ready, and 0 countable
  rows. The baseline companion,
  `artifacts/v3_source_gap_minicampaign_baseline_comparison_20260520.json`,
  makes no superiority claim: EC/keyword routing would admit all 18 rows while
  source completeness detects all 18 blockers, and sequence/ESM/Foldseek/
  geometry comparisons remain unscored because the surface is pre-scoring.
- `artifacts/v3_source_complete_external_minicampaign_blocker_review_20260520.json`
  records that the current source-complete post-P06744 rows cannot be reused
  as a fresh prospective mini-campaign. All six already have bounded
  sequence-search, current-countable structural-screen, and terminal decision
  outcomes; all six are review-only rejections by current-countable structural
  duplicate signal. Future prospective external work therefore needs genuinely
  new sourcing or a different frozen surface before scoring.
- `artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_20260521.json`
  is the first deep packet over the 2026-05-21 current-fingerprint
  mini-campaign surfaces. It selects seven rows from the frozen
  metal-phosphatase campaign before geometry/Foldseek outcome scoring, stages
  seven AlphaFold sidecars, maps seven active-site residue sets, and scores all
  seven against the current eight fingerprints with 0 text/name/label fields
  used. The outcome is a precise review-only blocker rather than import
  readiness: the exact current-countable Foldseek duplicate screen did not
  complete, so all seven rows are `needs_new_extractor_or_structure` until a
  completed structural duplicate/leakage screen exists. The companion
  benchmark
  `artifacts/v3_metal_phosphatase_deep_packet_modern_baseline_benchmark_20260521.json`
  records EC/keyword, deterministic 5-mer, geometry, Foldseek, and ESM caveats
  with no superiority, mechanism-match, or label-import claim.
- `artifacts/v3_metal_phosphatase_deep_packet_chunked_current_countable_structural_screen_20260521.json`
  closes that exact missing-evidence item with a query-chunked Foldseek/TM
  screen. The same seven frozen rows are screened against the 672 staged
  current-countable structures, all 4,704 unique query-target structure pairs
  map cleanly, and all seven candidates have `TM >= 0.7` current-countable
  structural duplicate/leakage signals. The post-screen terminal packet
  `artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
  converts the seven rows to
  `terminal_rejection_duplicate_or_leakage`, keeps import-ready and countable
  candidate counts at 0, and preserves source separation: Foldseek/TM evidence
  is an import-gate duplicate/leakage screen, not positive mechanism evidence.
  The post-duplicate benchmark
  `artifacts/v3_metal_phosphatase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json`
  records EC/keyword, deterministic sequence, geometry, Foldseek, and missing
  ESM sidecar caveats with no superiority claim.
- `artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_20260521.json`
  is the second deep packet over the same frozen external surfaces. It selects
  seven rows from the serine-hydrolase mini-campaign before outcome scoring,
  excludes exact current-reference duplicate `P94388`, materializes six
  AlphaFold sidecars, and maps six Ser/Asp/His active-site triads. Geometry
  scoring uses 0 text/name/label fields; six rows top-rank the target
  `ser_his_acid_hydrolase` lane, but every target-lane score remains below the
  `0.4115` floor. The exact current-countable structural duplicate/leakage
  evidence is not complete: the blocker/probe artifacts record pair-cache
  completeness false, screened-candidate count 0, and no duplicate-clear
  claim, while `P31614` lacks a materialized coordinate sidecar. All seven rows
  therefore have the allowed terminal decision `needs_new_extractor_or_structure`.
  The companion benchmark
  `artifacts/v3_serine_hydrolase_deep_packet_modern_baseline_benchmark_20260521.json`
  compares EC/keyword routing, deterministic 5-mer, geometry, Foldseek, and ESM
  availability on the same frozen rows, with no superiority, mechanism-match,
  or label-import claim.
- `artifacts/v3_serine_hydrolase_deep_packet_chunked_current_countable_structural_screen_20260521.json`
  attempts the next serine duplicate-screen step with bounded one-query
  Foldseek chunks. It is a blocker artifact, not a duplicate-clear artifact:
  all six materialized serine queries time out at 120 seconds and `P31614`
  remains coordinate-missing. The follow-up terminal packet
  `artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
  keeps all seven rows at `needs_new_extractor_or_structure`, with 0
  import-ready or countable rows. The next serine attempt needs smaller
  current-countable target subchunks or a coordinate/replacement path for
  `P31614`.
- `artifacts/v3_serine_hydrolase_deep_packet_targeted_current_ser_his_rescue_screen_20260521.json`
  removes most of that serine blocker with targeted duplicate/leakage evidence.
  It screens the six materialized serine rows against the 40 current-countable
  `ser_his_acid_hydrolase` structures and finds high-TM duplicate/leakage
  signals for all six. The follow-up terminal packet
  `artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_targeted_ser_his_rescue_screen_20260521.json`
  sets those six rows to `terminal_rejection_duplicate_or_leakage` while
  keeping coordinate-missing `P31614` at `needs_new_extractor_or_structure`.
  This targeted rescue does not claim duplicate-clear, mechanism-match,
  superiority, or import readiness; its companion benchmark
  `artifacts/v3_serine_hydrolase_deep_packet_post_targeted_ser_his_rescue_modern_baseline_benchmark_20260521.json`
  remains diagnostic only.
- `artifacts/v3_serine_hydrolase_p31614_pdb_replacement_coordinate_screen_20260521.json`
  narrows the remaining serine blocker. It materializes the frozen `P31614` PDB
  cross-references `4C7L` and `4C7W`, screens both replacement coordinates
  against the same 40 current-countable serine-hydrolase targets, and finds
  0 high-TM hits with max TM `0.5371`. The follow-up terminal packet
  `artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_pdb_replacement_screen_20260521.json`
  keeps six duplicate/leakage rejections and leaves `P31614` as the single
  `needs_new_extractor_or_structure` row, with the exact blocker now narrowed
  to PDB active-site residue mapping plus full-current duplicate/leakage
  screening or replacement in a newly frozen selection.
- `artifacts/v3_serine_hydrolase_p31614_pdb_active_site_mapping_blocker_20260521.json`
  sharpens that P31614 blocker while staying review-only. The replacement PDB
  coordinates do not carry a direct `P31614` struct-ref, catalytic position 45
  is observed as engineered Ser-to-Ala mutant context, and source charge-relay
  positions 342/345 are absent from atom-site auth numbering in both 4C7L and
  4C7W. This is blocker evidence only: it does not claim duplicate-clear,
  mechanism-match, superiority, import readiness, or any registry/fingerprint
  edit. The follow-up terminal packet
  `artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_active_site_mapping_20260521.json`
  keeps six serine rows at `terminal_rejection_duplicate_or_leakage` and
  preserves `P31614` as the single exact-blocked
  `needs_new_extractor_or_structure` row. The companion benchmark
  `artifacts/v3_serine_hydrolase_deep_packet_post_p31614_active_site_mapping_modern_baseline_benchmark_20260521.json`
  keeps EC/keyword, deterministic 5-mer, geometry, atom-site mapping,
  targeted Foldseek, and ESM caveats separated with no superiority claim.
- `artifacts/v3_serine_hydrolase_p31614_full_current_alignment_duplicate_probe_20260521.json`
  closes the last serine blocker as terminal duplicate/leakage evidence. It
  screens the two P31614 replacement PDB coordinates against all 672
  current-countable selected structures, completes 1,344/1,344 query-target
  pairs, and finds a high-TM current-countable signal for 4C7L against
  `pdb:1IR3` at max pair TM `0.7213`. The follow-up terminal packet
  `artifacts/v3_serine_hydrolase_deep_terminal_decision_packet_after_p31614_full_current_probe_20260521.json`
  records all seven serine rows as `terminal_rejection_duplicate_or_leakage`.
  The active-site triad mapping remains unresolved, duplicate-clear is not
  claimed, and no mechanism-match, import, superiority, registry, or
  fingerprint change is authorized. The benchmark
  `artifacts/v3_serine_hydrolase_deep_packet_post_p31614_full_current_probe_modern_baseline_benchmark_20260521.json`
  preserves the same source-separated caveats.
- `artifacts/v3_serine_hydrolase_second_deep_packet_selection_20260521.json`
  starts a second serine-hydrolase deep packet from five already frozen rows
  rather than adding new mini-campaign breadth. The source-free triad extractor
  finds coordinate-only Ser-His-Asp/Glu triads for `P16233`, `Q9FG13`,
  `P54318`, and `P0ADA1`, while `Q9NWW9` remains insufficient evidence. The
  targeted current-serine structural screen then compares the four above-floor
  rows against 40 current-countable `ser_his_acid_hydrolase` structures and
  finds duplicate/leakage signals for all four (`TM >= 0.7`, max `0.9755`).
  `artifacts/v3_serine_hydrolase_second_deep_terminal_decision_packet_after_targeted_ser_his_screen_20260521.json`
  therefore converts the packet to four
  `terminal_rejection_duplicate_or_leakage` rows plus one
  `terminal_rejection_insufficient_evidence` row, with no import, registry,
  fingerprint, or superiority claim.
- `artifacts/v3_external_deep_terminal_import_gate_readiness_check_post_second_serine_20260521.json`
  records the post-rollup import gate as closed. The registry invariants remain
  682 labels, 212 `seed_fingerprint`, 470 `out_of_scope`, and the only imported
  external labels remain `uniprot:P06744`, `uniprot:P78549`, and
  `uniprot:Q3LXA3` as out-of-scope/null-fingerprint
  `label_factory_v1_8fp` rows. The 57 current deep-packet rows contain 0
  countable candidates and 0 import-ready candidates, and the artifact
  explicitly treats mechanism-match-review-ready rows as review packets only
  until a full inverse-gate and label-factory payload passes.
- `artifacts/v3_flavin_dehydrogenase_deep_packet_selection_20260521.json`
  starts the next deepening ladder step without scoring it. It freezes seven
  nonduplicate flavin dehydrogenase/reductase rows from the existing
  mini-campaign after excluding exact current-reference duplicates `P15559`,
  `P0AEZ1`, `P38489`, and `P42593`. Selection uses the already frozen
  PDB/catalytic/active-or-binding-site/flavin context. The coordinate
  materialization companion stages all seven AlphaFold sidecars with 0 fetch
  failures, and the structure-mapping companion resolves active/cofactor-site
  coordinates for all seven rows as review-only mapping evidence. Geometry
  scoring then top-ranks six rows to `flavin_dehydrogenase_reductase`, with
  four target-lane scores above the `0.4115` floor and 0 text/name/label fields
  used. The terminal packet still records all seven as
  `needs_new_extractor_or_structure`, because Foldseek/TM current-countable
  duplicate evidence is not run and no duplicate-clear claim is allowed. The
  benchmark records EC/keyword, deterministic 5-mer, geometry, Foldseek, and
  ESM caveats with no superiority, mechanism-match, or label-import claim.
- `artifacts/v3_flavin_dehydrogenase_deep_packet_chunked_current_countable_structural_screen_20260521.json`
  now removes that exact duplicate-screen blocker. The same seven frozen rows
  are screened one query at a time against 672 current-countable structures,
  all 4,704 unique query-target structure pairs map with 0 raw-name failures,
  and all seven rows have `TM >= 0.7` current-countable duplicate/leakage
  signals. The terminal packet
  `artifacts/v3_flavin_dehydrogenase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
  converts all seven rows to
  `terminal_rejection_duplicate_or_leakage`, keeps import-ready/countable
  counts at 0, and preserves Foldseek/TM as import-gate duplicate/leakage
  evidence rather than source-free positive mechanism evidence. The
  post-duplicate benchmark
  `artifacts/v3_flavin_dehydrogenase_deep_packet_post_duplicate_modern_baseline_benchmark_20260521.json`
  remains review-only and makes no superiority claim. Fresh ePK follow-up is
  synthesized separately in
  `artifacts/v3_epk_fresh_lane_followup_synthesis_20260521.json` and does not
  reopen ePK production scoring, label import, or fingerprint expansion.
- `artifacts/v3_flavin_monooxygenase_deep_packet_selection_20260521.json`
  opens the frozen flavin-monooxygenase deep packet without new broad sourcing.
  It selects seven non-exact-reference rows from the existing 2026-05-21
  mini-campaign before deep geometry/Foldseek scoring, and the coordinate
  materialization companion stages all seven AlphaFold sidecars with 0 fetch
  failures. The targeted current-fingerprint rescue screen
  `artifacts/v3_flavin_monooxygenase_deep_packet_targeted_current_fmo_rescue_screen_20260521.json`
  checks only the two current-countable `flavin_monooxygenase` structures,
  finds three high-TM duplicate/leakage hits, and makes no duplicate-clear
  claim. The follow-up terminal packet
  `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_targeted_fmo_rescue_screen_20260521.json`
  records three `terminal_rejection_duplicate_or_leakage` rows and four
  `needs_new_extractor_or_structure` rows, with the exact remaining blocker
  stated as source-free flavin/cofactor geometry mapping plus full
  current-countable duplicate/leakage screening. The benchmark
  `artifacts/v3_flavin_monooxygenase_deep_packet_targeted_fmo_modern_baseline_benchmark_20260521.json`
  keeps EC/keyword, deterministic sequence, geometry-not-run, Foldseek, and ESM
  caveats diagnostic only and makes no superiority, mechanism-match, import, or
  production-scoring claim.
- `artifacts/v3_flavin_monooxygenase_deep_packet_structure_mapping_20260521.json`
  narrows that blocker by mapping active/cofactor binding positions onto all
  seven selected AlphaFold coordinate sidecars with status `ok`. Binding-site
  ranges are expanded residue-by-residue before CA mapping, and EC/name/prose
  remain review context only. The follow-up terminal packet
  `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_structure_mapping_20260521.json`
  preserves the three duplicate/leakage rejections and four
  `needs_new_extractor_or_structure` rows, but the remaining blocker is now
  source-free FMO geometry scoring from mapped flavin/cofactor coordinates plus
  full current-countable duplicate/leakage screening. The benchmark
  `artifacts/v3_flavin_monooxygenase_deep_packet_post_structure_mapping_modern_baseline_benchmark_20260521.json`
  records mapped-candidate count 7, geometry-scored count 0, ESM unavailable,
  and no superiority, mechanism-match, import, or production-scoring claim.
- `artifacts/v3_flavin_monooxygenase_deep_packet_geometry_scores_20260521.json`
  and
  `artifacts/v3_flavin_monooxygenase_deep_packet_full_current_subchunk_screen_20260521.json`
  close the next FMO blocker without adding candidate breadth. The geometry
  artifact scores all seven frozen rows from mapped local flavin/cofactor
  coordinate evidence with 0 text/name/label fields used; only `H3JQW0` reaches
  the FMO floor and all rows top-rank to `flavin_dehydrogenase_reductase`, so
  no mechanism-match claim is made. The full-current screen completes for
  `H3JQW0` and `Q6F4M8`, finding current-countable `TM >= 0.7`
  duplicate/leakage signals, while `O94851` and `Q7RTP6` time out on their
  first target chunk and therefore have no duplicate-clear claim. The terminal
  packet
  `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_geometry_and_full_current_screen_20260521.json`
  now records five `terminal_rejection_duplicate_or_leakage` rows and two
  `needs_new_extractor_or_structure` rows with the exact blocker: complete the
  full current-countable duplicate/leakage screen after the subchunk timeout or
  pair-cache gap. The benchmark
  `artifacts/v3_flavin_monooxygenase_deep_packet_post_geometry_full_current_modern_baseline_benchmark_20260521.json`
  keeps EC/keyword and sequence routing diagnostic, records ESM unavailable,
  and makes no superiority, import, production-scoring, or duplicate-clear
  claim for incomplete rows.
- `artifacts/v3_flavin_monooxygenase_deep_packet_timeout_chunk000_rescue_probe_20260521.json`
  further narrows the remaining FMO duplicate-screen blocker. It splits the
  timed-out first full-current target chunk into eight six-target subchunks for
  `O94851` and `Q7RTP6`. `O94851` completes seven subchunks and times out only
  on subchunk 7; `Q7RTP6` completes five subchunks and times out on subchunks
  1, 6, and 7. The completed subchunks have 0 high-TM hits, but pair-cache
  completeness is still false for both rows, so the artifact is blocker
  localization only and authorizes no duplicate-clear, mechanism-match, import,
  or superiority claim.
- `artifacts/v3_flavin_monooxygenase_deep_packet_timeout_chunk000_size2_rescue_probe_20260521.json`
  retries the still-timed six-target subchunks at two targets per run. It
  resolves the `O94851` chunk-000 timeout surface with 0 high-TM hits and
  narrows `Q7RTP6` to one still-timed two-target retry under parent subchunk 1.
  Chunks 1-13 remain unrun for both nonterminal candidates, so this still only
  localizes the full-current duplicate-screen blocker.
- `artifacts/v3_flavin_monooxygenase_deep_packet_chunk000_chunk001_rescue_and_remaining_screen_20260521.json`
  closes the outstanding `Q7RTP6` chunk-000 retry and completes chunk 001 for
  both `O94851` and `Q7RTP6`. The completed follow-up targets have 0
  `TM >= 0.7` current-countable hits and maximum TM `0.6315`, so they do not
  create a duplicate/leakage rejection and still do not permit duplicate-clear.
  Chunk 002 times out for both rows and chunks 003-013 are unrun. The updated
  terminal packet
  `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk001_rescue_20260521.json`
  therefore keeps the packet at five duplicate/leakage rejections and two
  `needs_new_extractor_or_structure` rows, with the exact blocker now chunk-002
  subchunking/completion plus chunks 003-013. The companion benchmark
  `artifacts/v3_flavin_monooxygenase_deep_packet_chunk001_rescue_modern_baseline_benchmark_20260521.json`
  keeps EC/keyword and sequence baselines diagnostic, ESM unavailable, and
  Foldseek/TM as import-gate evidence only.
- `artifacts/v3_flavin_monooxygenase_deep_packet_chunk000_chunk002_rescue_and_remaining_screen_20260521.json`
  extends the same bounded duplicate-screen follow-up through chunk 002.
  Chunks 000, 001, and 002 are now complete for both remaining FMO rows with
  0 high-TM current-countable hits and maximum completed follow-up TM `0.6371`.
  The terminal packet
  `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk002_rescue_20260521.json`
  keeps the packet at five duplicate/leakage rejections and two
  `needs_new_extractor_or_structure` rows. The exact blocker is now chunks
  003-013, using smaller subchunks if a 48-target chunk times out. The
  benchmark
  `artifacts/v3_flavin_monooxygenase_deep_packet_chunk002_rescue_modern_baseline_benchmark_20260521.json`
  continues to make no duplicate-clear, superiority, import, or production
  scoring claim.
- `artifacts/v3_flavin_monooxygenase_deep_packet_chunk003_followup_screen_20260521.json`
  runs the next FMO full-current duplicate/leakage chunk as smaller subchunks.
  All 16 chunk-003 subchunks complete for `O94851` and `Q7RTP6`, and both rows
  find current selected `pdb:1DOC` high-TM signals at `TM >= 0.7`.
  `artifacts/v3_flavin_monooxygenase_deep_packet_chunk004_followup_screen_20260521.json`
  adds supplemental high-TM signals against `pdb:1EHK` before some chunk-004
  subchunks time out; it does not make a duplicate-clear claim. The terminal
  packet
  `artifacts/v3_flavin_monooxygenase_deep_terminal_decision_packet_after_chunk004_followup_20260521.json`
  converts the last two FMO blockers to
  `terminal_rejection_duplicate_or_leakage`, so all seven frozen FMO rows are
  terminal duplicate/leakage rejections. The benchmark
  `artifacts/v3_flavin_monooxygenase_deep_packet_chunk004_followup_modern_baseline_benchmark_20260521.json`
  keeps EC/keyword, sequence, and ESM/Foldseek comparisons diagnostic only,
  with no import, production-score, registry, fingerprint, upload/removal, or
  superiority claim.
- `artifacts/v3_plp_aminotransferase_deep_packet_selection_20260521.json`
  freezes seven non-exact-reference PLP aminotransferase rows from the existing
  mini-campaign before deep outcome scoring. The blocker packet
  `artifacts/v3_plp_aminotransferase_deep_blocker_packet_after_pdb_cofactor_probe_20260521.json`
  fetches selected PDB coordinates in memory only, observes PLP-like coordinate
  tokens for six rows, writes no raw coordinate files, scores no production
  fingerprint, runs no full-current duplicate screen, and records all seven
  rows as `needs_new_extractor_or_structure`. The exact next experiment is a
  source-free PLP/LLP/PMP/P5P covalent-anchor and catalytic-residue extractor,
  then full current-countable duplicate/leakage screening on the same frozen
  selection. The benchmark
  `artifacts/v3_plp_aminotransferase_deep_blocker_modern_baseline_benchmark_20260521.json`
  records EC/keyword, deterministic sequence, coordinate-token, Foldseek, and
  ESM caveats as diagnostic only with no import, production-score, registry,
  fingerprint, upload/removal, or superiority claim.
- The follow-up PLP extractor/screen closes that blocker as terminal
  review-only rejection evidence. `src/catalytic_earth/plp_active_site.py`
  extracts coordinate-only PLP/LLP/PMP/P5P-like cofactors, lysine anchors,
  acid/base residues, and phosphate binders without using EC, names, UniProt
  prose, PLP annotations, or labels as predictive inputs. The geometry artifact
  `artifacts/v3_plp_aminotransferase_deep_packet_source_free_active_site_geometry_scores_20260521.json`
  resolves six complete PLP active-site triplets and scores all six above the
  current PLP floor; `Q9NZ45`/`2QD0` has no selected-PDB PLP-like coordinate
  evidence. The targeted current-PLP Foldseek screen
  `artifacts/v3_plp_aminotransferase_deep_packet_targeted_current_plp_screen_20260521.json`
  finds `TM >= 0.7` current-countable PLP duplicate/leakage signals for all
  six scored rows. The terminal packet
  `artifacts/v3_plp_aminotransferase_deep_terminal_decision_packet_after_source_free_anchor_and_targeted_plp_screen_20260521.json`
  therefore records six `terminal_rejection_duplicate_or_leakage` rows and one
  `terminal_rejection_insufficient_evidence` row, with 0 import-ready rows and
  no superiority claim in the companion benchmark.
- The post-PLP rollup
  `artifacts/v3_external_deep_terminal_decision_rollup_post_plp_20260521.json`
  is planning context only. It summarizes the six existing deep-packet lanes
  without freezing new external rows: 42 frozen rows have non-`needs_review`
  terminal outcomes, with 40 duplicate/leakage rejections, one
  insufficient-evidence rejection, and one review-only
  `mechanism_match_review_ready` heme row. It derives aggregate counts from
  terminal-decision maps, records the stale serine summary-counter mismatch,
  and keeps import-ready and countable-label counts at 0.
- The second metal-phosphatase deep packet continues that post-PLP direction
  without new broad sourcing. It selects seven remaining rows from the already
  frozen 17-row metal-phosphatase campaign before new geometry/Foldseek
  scoring, materializes seven AlphaFold v6 coordinate sidecars, maps all seven
  active-site feature sets, and scores the current 8-fingerprint geometry
  surface with 0 text/name/label fields used. The bounded current-countable
  Foldseek screen completes five rows and finds `TM >= 0.7` duplicate/leakage
  signals for all five, so
  `artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_second_selection_20260521.json`
  records five `terminal_rejection_duplicate_or_leakage` rows. `Q99504` and
  `P05186` remain exact `needs_new_extractor_or_structure` blockers because
  their bounded Foldseek queries timed out; no duplicate-clear claim is made
  for them. The targeted timeout rescue
  `artifacts/v3_metal_phosphatase_deep_packet_second_timeout_targeted_rescue_screen_20260521.json`
  then checks only `Q99504` and `P05186` against current structures `1T7D`,
  `1RTF`, and `1ALK`. It converts `P05186` to
  `terminal_rejection_duplicate_or_leakage` and leaves only `Q99504` blocked
  because the targeted subset completed with no high-TM hit. The companion
  post-rescue rollup
  `artifacts/v3_external_deep_terminal_decision_rollup_post_second_metal_timeout_rescue_20260521.json`
  indexes 49 deep-packet rows across seven packet surfaces, with 48
  non-`needs_review` terminal outcomes and 0 import-ready candidates.
  `artifacts/v3_metal_phosphatase_q99504_current_metal_target_probe_20260521.json`
  narrows the single remaining Q99504 blocker by completing all 67 current
  `metal_dependent_hydrolase` target structures with 0 high-TM hits and
  nearest max TM `0.5324`; this is not duplicate-clear because non-metal
  current-countable targets remain unprobed after the all-current timeout.
  `artifacts/v3_metal_phosphatase_q99504_current_nonmetal_chunk000_probe_20260521.json`
  completes the first 80 non-metal current-countable targets with 0 high-TM
  hits and nearest max TM `0.5951`, further narrowing Q99504 to the remaining
  non-metal subchunks or alternate coordinate evidence. Chunk001
  `artifacts/v3_metal_phosphatase_q99504_current_nonmetal_chunk001_probe_20260521.json`
  completes another 80 non-metal targets with 0 high-TM hits and nearest max
  TM `0.5232`.
  The Q99504 closure pass then completes chunks002-007 plus the targeted
  rescue-only structures, yielding full 672/672 bounded current-countable
  selected-structure coverage with 0 `TM >= 0.7` hits and nearest max TM
  `0.6185` to `pdb:1EHK`.
  `artifacts/v3_metal_phosphatase_q99504_full_current_countable_duplicate_closure_20260521.json`
  therefore permits only a bounded current-countable duplicate-clear statement,
  not UniRef-wide clearance or import readiness. Because Q99504's source-free
  metal-hydrolase geometry score remains below the `0.4115` floor (`0.3742`)
  and only two active-site residues are resolved, the updated terminal packet
  `artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_second_after_q99504_duplicate_closure_20260521.json`
  converts Q99504 to `terminal_rejection_insufficient_evidence`. The updated
  rollup
  `artifacts/v3_external_deep_terminal_decision_rollup_post_q99504_duplicate_closure_20260521.json`
  now indexes 49 deep-packet rows with 49 non-`needs_review` terminal outcomes,
  0 import-ready candidates, and no registry/fingerprint edits.
- The remaining-metal targeted screen
  `artifacts/v3_metal_phosphatase_deep_packet_remaining_targeted_current_metal_screen_20260521.json`
  then deepens the last three rows from the same frozen metal-phosphatase
  campaign without adding external breadth. The selection artifact uses
  P75792, P77247, and P0A8Y5 only after the earlier 14 rows had already been
  selected, materializes three PDB coordinate sidecars, and screens them
  against the 67 current-countable `metal_dependent_hydrolase` structures.
  P77247 hits current `pdb:1RQL` at max TM `0.8110` and is terminal
  `terminal_rejection_duplicate_or_leakage`; P75792 and P0A8Y5 do not hit the
  targeted metal subset and remain `needs_new_extractor_or_structure` pending
  source-free geometry plus full current-countable duplicate screening. The
  post-screen rollup
  `artifacts/v3_external_deep_terminal_decision_rollup_post_remaining_metal_targeted_screen_20260521.json`
  covers 52 deep-packet rows: 47 duplicate/leakage rejections, two
  insufficient-evidence rejections, one mechanism-match review-ready row, and
  two exact blockers.
- The remaining-metal duplicate-closure follow-up then completes the non-metal
  half of those two blockers without selecting new rows.
  `artifacts/v3_metal_phosphatase_remaining_nonmetal_chunk000_probe_20260521.json`
  through
  `artifacts/v3_metal_phosphatase_remaining_nonmetal_chunk007_probe_20260521.json`
  cover 605 non-metal current-countable targets for P75792 and P0A8Y5 with
  0 `TM >= 0.7` hits. Combined with the 67-target current-metal screen,
  `artifacts/v3_metal_phosphatase_remaining_full_current_countable_duplicate_closure_20260521.json`
  covers 672/672 bounded current-countable targets per row, 1,344 blocker-row
  pairs total, 0 high-TM hits, nearest P75792 max TM `0.6855` to `pdb:2PHK`,
  and nearest P0A8Y5 max TM `0.6392` to `pdb:1L7N`. The follow-up packet
  `artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_full_current_duplicate_closure_20260521.json`
  keeps both rows at `needs_new_extractor_or_structure` because their
  source-free geometry scores are still missing. The exact remaining blocker is
  `source_free_geometry_scoring_missing_for_pdb_active_site_features_after_bounded_duplicate_clearance`.
  This closure is a bounded duplicate/leakage gate result only, not
  mechanism-match evidence, UniRef-wide clearance, or label-import readiness.
  The companion benchmark
  `artifacts/v3_metal_phosphatase_deep_packet_remaining_after_full_current_duplicate_closure_modern_baseline_benchmark_20260521.json`
  preserves the EC/sequence/ESM/Foldseek caveats and makes no superiority
  claim.
- `artifacts/v3_metal_phosphatase_remaining_source_free_geometry_scores_20260521.json`
  closes the remaining source-free geometry gap for that same already selected
  metal packet. P75792 and P0A8Y5 resolve coordinate-only Mg/Asp-Ser
  metal-ligand clusters and score above the current
  `metal_dependent_hydrolase` floor while retaining bounded current-countable
  duplicate clearance. The terminal packet
  `artifacts/v3_metal_phosphatase_deep_terminal_decision_packet_remaining_after_source_free_geometry_20260521.json`
  marks both rows `mechanism_match_review_ready` for the broad current lane,
  keeps P77247 at `terminal_rejection_duplicate_or_leakage`, and records that
  phosphate/substrate specificity is not source-free and no import is
  authorized. The rollup
  `artifacts/v3_external_deep_terminal_decision_rollup_post_remaining_metal_source_free_geometry_20260521.json`
  covers 52 deep rows with 0 exact blockers and 0 import-ready candidates.
- The follow-up AKR readiness recheck
  `artifacts/v3_akr_family_readiness_post_q99504_terminal_recheck_20260521.json`
  uses existing artifacts only after the Q99504 terminal closure. It keeps
  AKR/NADP redox at `needs_new_extractor_or_structure` for production
  readiness: C9JRZ8 remains the only source-traced positive-like AKR row,
  the frozen SDR/AKR control tranche still has 0 source-free axis-ready rows,
  direct local NADP geometry is missing, broader duplicate screening is
  unresolved for positive-like AKR rows, and EC/name/source prose remain
  excluded from predictive evidence.
- `artifacts/v3_heme_peroxidase_deep_packet_selection_20260521.json`
  freezes seven non-exact-reference heme-peroxidase rows from the existing
  campaign before geometry or duplicate scoring. Coordinate materialization and
  structure mapping resolve all seven AlphaFold sidecars and active/heme-binding
  feature sets. The source-free geometry artifact top-ranks all seven rows to
  `heme_peroxidase_oxidase` above the `0.4115` floor with 0 text/name/label
  fields used. The chunked all-current duplicate screen is mixed, so a targeted
  current-heme rescue screen adds three more high-TM current-countable heme hits
  without making a duplicate-clear claim. The terminal packet
  `artifacts/v3_heme_peroxidase_deep_terminal_decision_packet_after_chunked_duplicate_screen_20260521.json`
  records six `terminal_rejection_duplicate_or_leakage` rows and keeps `I2DBY1`
  at `needs_new_extractor_or_structure` pending a complete full-current
  subchunked duplicate/leakage screen. The post-duplicate benchmark records
  EC/keyword, deterministic sequence, Foldseek, ESM, and geometry caveats with
  no superiority, mechanism-match, or label-import claim. Fresh remote ePK lane
  pushes are synthesized separately in
  `artifacts/v3_epk_remote_lane_followup_synthesis_20260521.json` and remain
  review-only/no-go.
- `artifacts/v3_heme_peroxidase_deep_packet_i2dby1_full_current_subchunk_screen_20260521.json`
  closes that single heme timeout blocker. It screens only `I2DBY1` against the
  same 672 staged current-countable structures in 14 target chunks, maps
  672/672 query-target pairs, finds 0 high-TM duplicate/leakage hits at
  `TM >= 0.7`, and records max current-countable TM `0.5890`. The follow-up
  terminal packet
  `artifacts/v3_heme_peroxidase_deep_terminal_decision_packet_after_i2dby1_subchunk_screen_20260521.json`
  sets `I2DBY1` to `mechanism_match_review_ready` while preserving the six
  duplicate/leakage terminal rejections. The companion benchmark
  `artifacts/v3_heme_peroxidase_deep_packet_post_i2dby1_subchunk_modern_baseline_benchmark_20260521.json`
  keeps EC/keyword and deterministic sequence baselines diagnostic only, records
  ESM as unavailable, and makes no superiority or import claim.
- `artifacts/v3_flavin_dehydrogenase_second_deep_packet_selection_20260521.json`
  starts a second flavin dehydrogenase/reductase deep packet from seven
  previously unselected rows in the already frozen campaign, with no new broad
  external row freeze. Coordinates materialize for all seven; source-free
  geometry uses 0 EC/name/label/prose fields and records 0 target-lane
  above-floor rows. The targeted current-FDR screen
  `artifacts/v3_flavin_dehydrogenase_second_deep_packet_targeted_current_fdr_screen_20260521.json`
  completes 343/343 query-target pairs against 49 current FDR structures and
  finds high-TM current-lane duplicate/leakage signals for every row. The
  terminal packet
  `artifacts/v3_flavin_dehydrogenase_second_deep_terminal_decision_packet_after_targeted_fdr_screen_20260521.json`
  records seven `terminal_rejection_duplicate_or_leakage` rows, 0 import-ready
  rows, 0 countable candidates, and no superiority claim.
- `artifacts/v3_heme_peroxidase_second_deep_packet_selection_20260521.json`
  starts a second heme-peroxidase deep packet from seven existing frozen rows.
  All seven coordinates and active/heme-binding feature mappings are available,
  and source-free geometry top-ranks all seven to `heme_peroxidase_oxidase`
  above the `0.4115` floor with 0 text/name fields used. The targeted
  current-heme screen
  `artifacts/v3_heme_peroxidase_second_deep_packet_targeted_current_heme_screen_20260521.json`
  completes 140/140 query-target pairs against 20 current heme structures:
  four rows have high-TM current-heme duplicate/leakage signals. The initial
  terminal packet
  `artifacts/v3_heme_peroxidase_second_deep_terminal_decision_packet_after_targeted_heme_screen_20260521.json`
  records four `terminal_rejection_duplicate_or_leakage` rows and three exact
  `needs_new_extractor_or_structure` blockers:
  `full_current_countable_duplicate_screen_missing_after_targeted_current_heme_screen`.
  The follow-up full current-countable screen
  `artifacts/v3_heme_peroxidase_second_deep_packet_full_current_countable_screen_20260521.json`
  closes that blocker for the three targeted-clear rows by covering 2016/2016
  query-target pairs against 672 unique current-countable selected structures.
  `P31545` hits current `pdb:1IR3` at `TM 0.7041` and becomes a terminal
  duplicate/leakage rejection; `P39597` and `K7N5M8` have no `TM >= 0.7` hit
  and become review-only `mechanism_match_review_ready` rows. The post-full
  terminal packet, rollup, and readiness artifacts
  `artifacts/v3_heme_peroxidase_second_deep_terminal_decision_packet_after_full_current_screen_20260521.json`,
  `artifacts/v3_external_deep_terminal_decision_rollup_post_second_heme_full_current_screen_20260521.json`,
  and
  `artifacts/v3_external_deep_terminal_import_gate_readiness_check_post_second_heme_full_current_screen_20260521.json`
  cover 71 deep rows with 0 exact blockers, 0 import-ready candidates, and the
  682-label registry invariant still closed. The independent rerun artifact
  `artifacts/v3_heme_peroxidase_second_deep_packet_full_current_countable_duplicate_screen_20260521.json`
  preserves the same 3-row status split as duplicate/leakage evidence only.
- `artifacts/v3_external_mechanism_match_review_ready_import_blocker_matrix_20260522.json`
  collects the five current `mechanism_match_review_ready` external deep rows
  across heme and metal lanes. It is review-only, freezes 0 new rows, imports 0
  labels, and records the exact remaining blockers before any label action:
  UniRef-wide duplicate evidence plus a full label-factory import payload under
  the unchanged 682-label, 8-fingerprint baseline.
- `artifacts/v3_prospective_external_methyltransferase_minicampaign_freeze_20260520.json`
  freezes that different surface: 20 Swiss-Prot EC 2.1.1.x methyltransferase
  rows selected before outcome scoring from a live UniProt query, requiring
  catalytic-activity text, active-site annotation, and at least one PDB
  cross-reference. The decision packet,
  `artifacts/v3_prospective_external_methyltransferase_minicampaign_decision_packet_20260520.json`,
  records all 20 as terminal review-only rejections by uncovered mechanism
  lane, with 0 current-fingerprint scores, 0 inverse-gate rows, 0 sequence or
  Foldseek screens, 0 import-ready rows, and 0 countable candidates. The
  baseline companion,
  `artifacts/v3_methyltransferase_minicampaign_baseline_comparison_20260520.json`,
  makes no superiority claim: EC/keyword routing detects methyltransferase
  context, and
  `artifacts/v3_methyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json`
  adds a deterministic 5-mer nearest-current-reference check with two crude
  near-neighbor alerts across 20 rows. Geometry, ESM, and Foldseek remain
  unrun because the pre-scoring lane blocker is decisive.
- `artifacts/v3_prospective_external_glycosyltransferase_minicampaign_freeze_20260520.json`
  freezes another prospective external surface: 20 reviewed UniProtKB/Swiss-Prot
  EC 2.4.1.* rows selected before scoring, requiring catalytic-activity text,
  active-site annotation, at least one PDB cross-reference, prior-pool
  exclusions, and a two-row cap per primary EC number. Its decision packet
  records all 20 as terminal review-only rejections by uncovered
  glycosyltransferase mechanism lane. The baseline companion,
  `artifacts/v3_glycosyltransferase_minicampaign_baseline_comparison_20260520.json`,
  makes no superiority claim: EC/keyword routing detects the lane, and
  `artifacts/v3_glycosyltransferase_minicampaign_sequence_baseline_diagnostic_20260520.json`
  adds a deterministic 5-mer nearest-current-reference check with one crude
  near-neighbor alert across 20 rows. Geometry, ESM, and Foldseek remain unrun
  because the pre-scoring uncovered-lane blocker is decisive.
- `artifacts/v3_ghkl_vs_neighbor_family_control_tranche_preregistration_20260520.json`,
  `artifacts/v3_ghkl_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`,
  and
  `artifacts/v3_ghkl_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json`
  freeze and close the GHKL-vs-neighbor ATP-family tranche as review-only
  terminal evidence. The 10-row tranche has two GHKL boundary rows, two current
  hydrolase controls, two ATP-grasp controls, and one ASKHA, GHMP, NDK, and
  PfkB countercontrol each. GHKL remains a no-go production family: both GHKL
  rows are terminal rejections, the source-free GHKL fold/acceptor axis is not
  ready, and no baseline superiority, threshold, registry edit, or import is
  authorized. The post-tranche ATP-family index,
  `artifacts/v3_atp_family_readiness_index_post_ghkl_20260520.json`, keeps
  ASKHA, ATP-grasp, and GHKL closed as review-only no-go tranches.
- `artifacts/v3_dnk_family_readiness_packet_20260520.json` adds the next
  review-only ATP-family packet without opening production scoring. The two
  dNK boundary rows (`m_csa:588` thymidine kinase and `m_csa:615`
  deoxyguanosine kinase) remain non-countable, expert-rejected mismatch lanes
  with no source-free dNK fold/substrate axis, no countable seeds, no
  calibrated threshold, and no import path. Its queue companion,
  `artifacts/v3_atp_family_readiness_index_post_dnk_packet_20260520.json`,
  marks dNK as `readiness_packet_no_go`; the only bounded next step is a
  frozen dNK-vs-neighbor ATP-family control tranche before any scoring.
- `artifacts/v3_dnk_vs_neighbor_family_control_tranche_preregistration_20260520.json`,
  `artifacts/v3_dnk_vs_neighbor_family_control_tranche_axis_decisions_20260520.json`,
  and
  `artifacts/v3_dnk_vs_neighbor_family_control_tranche_baseline_comparison_20260520.json`
  freeze and close that dNK tranche as review-only terminal evidence. The 10
  rows contain two dNK boundary rows, two current hydrolase controls, one NDK,
  one PfkA, one PfkB, one GHMP, one ASKHA, and one ATP-grasp countercontrol.
  dNK remains a no-go production family: both dNK rows are terminal
  rejections, six neighboring ATP-family rows are out of scope for dNK, and
  the source-free dNK fold/substrate axis is not ready. The post-tranche index,
  `artifacts/v3_atp_family_readiness_index_post_dnk_tranche_20260520.json`,
  keeps ASKHA, ATP-grasp, GHKL, and dNK closed as review-only no-go tranches.
- `artifacts/v3_pfkb_family_readiness_packet_20260520.json` adds the next
  ATP-family review-only packet. The two PfkB/ribokinase boundary rows
  (`m_csa:663` ribokinase and `m_csa:670` hydroxymethylpyrimidine kinase)
  remain non-countable mismatch lanes with hydrolase top1 collapse and no
  accepted source-free PfkB fold or small-molecule hydroxyl-acceptor axis. The
  post-packet queue artifact,
  `artifacts/v3_atp_family_readiness_index_post_pfkb_packet_20260520.json`,
  marks PfkB as `readiness_packet_no_go`; the only bounded next step is a
  frozen PfkB-vs-neighbor ATP-family tranche before any scoring.
- `artifacts/v3_main_loop_small_win_register_post_atp_readiness_20260520.json`
  is the run-level rollup for these non-ePK small wins. It keeps ePK
  research-lane-only, preserves the glycosyltransferase terminal rejection
  after the sequence baseline diagnostic, records GHKL and dNK as closed
  review-only no-go tranches, and records PfkB as packet-only no-go.
- `artifacts/v3_schiff_base_lyase_readiness_packet_20260520.json`,
  `artifacts/v3_dna_glycosylase_lyase_readiness_packet_20260520.json`, and
  `artifacts/v3_mechanism_family_readiness_index_refresh_20260520.json` package
  two more non-ePK family-readiness decisions. Q9BXD5 and P06746 remain
  single-row, review-only positive-like controls with source-free-axis,
  duplicate-screening, and representation blockers; no production fingerprint,
  registry, or import path is opened.
- `artifacts/v3_schiff_base_lyase_control_tranche_preregistration_20260520.json`
  freezes the next Q9BXD5 review-only control tranche before scoring: one
  external Schiff-base lyase positive-like row, five current heme controls,
  five current PLP controls, two current ser-his hydrolase controls, and two
  current metal-hydrolase controls. It is only a preregistration; it does not
  run new axes, thresholds, inverse-gate scores, production scoring, or import.
- `artifacts/v3_schiff_base_lyase_control_tranche_axis_decisions_20260520.json`
  closes that same frozen tranche as review-only terminal evidence. Q9BXD5 is
  `needs_review` because its Schiff-base evidence is source-traced rather than
  source-free and duplicate/factory blockers remain open; the 14 current
  controls remain mechanism matches for their existing contexts. No production
  fingerprint or label import is authorized.
- `artifacts/v3_schiff_base_lyase_control_tranche_baseline_comparison_20260520.json`
  compares the frozen tranche against simple diagnostics without a superiority
  claim. EC/name keyword routing over-admits one PLP lyase control and cannot
  detect source-free-axis or duplicate/factory blockers; sequence and ESM
  sidecars cover only Q9BXD5, and Foldseek current-countable screening is not
  available for Q9BXD5 in this tranche.
- `artifacts/v3_dna_glycosylase_lyase_control_tranche_preregistration_20260520.json`
  and
  `artifacts/v3_dna_glycosylase_lyase_control_tranche_axis_decisions_20260520.json`
  freeze and close an 11-row P06746 review-only tranche against five current
  flavin controls and five current out-of-scope controls. P06746 remains
  `needs_review`; the source-free DNA-lyase geometry axis is not ready, and no
  production fingerprint, threshold, registry edit, or import is authorized.
- `artifacts/v3_dna_glycosylase_lyase_control_tranche_baseline_comparison_20260520.json`
  compares that tranche against simple diagnostics without a superiority
  claim. EC/name keyword routing finds only P06746 and cannot detect
  source-free geometry or duplicate/factory blockers; sequence and ESM evidence
  cover only P06746, and Foldseek current-countable screening is unavailable
  for that row in this tranche.
- `artifacts/v3_mechanism_family_readiness_index_post_tranche_refresh_20260520.json`
  rolls up the closed review-only family tranches. Glycoside hydrolase,
  Schiff-base lyase, DNA glycosylase/lyase, and SDR/AKR all remain no-go with
  0 source-free-axis-ready families; sugar-phosphate isomerase is now closed
  as a review-only no-go tranche too.
- `artifacts/v3_sdr_akr_nadp_control_tranche_preregistration_20260520.json`
  freezes the next SDR/AKR/NAD(P) boundary tranche before scoring: O14756,
  C9JRZ8, four clean SDR-like EC 1.1.1 abstention controls, four current
  flavin controls, and four current heme controls. It is preregistration only;
  no new axis scoring, threshold, registry edit, or import is authorized.
- `artifacts/v3_sdr_akr_nadp_control_tranche_axis_decisions_20260520.json`
  closes that frozen tranche as review-only terminal evidence. O14756 and
  C9JRZ8 remain `needs_review`, four external SDR-like abstention controls are
  `ambiguous`, and eight current redox controls remain `mechanism_match`; the
  source-free SDR/AKR axis-ready count is 0.
- `artifacts/v3_sdr_akr_nadp_control_tranche_baseline_comparison_20260520.json`
  compares the same tranche against simple diagnostics without a superiority
  claim. EC/name routing over-admits broad redox current controls, sequence
  and ESM context remain diagnostic only, and Foldseek current-countable
  screening is unavailable for the external positive-like rows in this tranche.
- `artifacts/v3_sugar_phosphate_isomerase_control_tranche_preregistration_20260520.json`
  freezes the next P34949 tranche before scoring: one external
  sugar-phosphate-isomerase positive-like row, four current
  flavin-dehydrogenase/reductase controls, two current flavin-monooxygenase
  controls, and four current out-of-scope controls. It is preregistration only;
  no axis scoring, threshold, registry edit, or import is authorized.
- `artifacts/v3_sugar_phosphate_isomerase_control_tranche_axis_decisions_20260520.json`
  closes that frozen tranche as review-only terminal evidence. P34949 remains
  `needs_review`, six current flavin controls remain `mechanism_match`, and
  four current controls remain `out_of_scope`; the source-free
  sugar-phosphate axis-ready count is 0.
- `artifacts/v3_sugar_phosphate_isomerase_control_tranche_baseline_comparison_20260520.json`
  adds the matching no-superiority diagnostic. EC/name routing finds P34949
  but cannot detect source-free geometry, duplicate/factory blockers, or the
  absence of Foldseek current-countable screening in this tranche.

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
- `artifacts/v3_sdr_family_readiness_packet_20260520.json` synthesizes the
  O14756 SDR repair-control row, SDR import-safety adjudication, SDR EC 1.1.1
  consistency check, AKR/NADP sibling controls, and modern baseline context into
  a simpler-family readiness packet. It is a review-only no-go for production
  fingerprint expansion: one positive-like row is insufficient, source-context
  active-site evidence is not a frozen predictive axis, EC 1.1.1 is too broad,
  and duplicate/review/factory blockers remain unresolved.
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
The original 10 pilot candidates and repaired lanes (`O14756`, `Q6NSJ0`,
`P34949`, `Q9BXD5`, `C9JRZ8`, `P06746`, `P55263`, `O60568`, `O95050`, and
`P51580`) are development/review evidence only and cannot be used as clean
held-out performance proof.

The next external hard-negative tranche is frozen before candidate selection in
`artifacts/v3_external_hard_negative_next_tranche_preregistration_1025.json`.
Future next-tranche imports must reference that artifact/version or a newer
documented pre-registration. The frozen policy records the 8-fingerprint
universe, `label_factory_v1_8fp`, the `0.4115` global threshold floor,
all-current-fingerprints-below-floor inverse gate, duplicate rules,
external-only structural-neighborhood rules, admissible source evidence,
excluded context, and success/failure criteria. The threshold provenance is in
`artifacts/v3_external_hard_negative_threshold_policy_1025.json`; candidate- or
tranche-specific threshold tuning is leakage and blocks import. Existing
external hard negatives (`uniprot:P06744`, `uniprot:P78549`, and
`uniprot:Q3LXA3`) are scoped only to `label_factory_v1_8fp` and must be
re-audited whenever the positive fingerprint universe expands, especially for
ePK, SDR, AKR, glycoside-hydrolase, isomerase, or lyase families.
The review-only ePK readiness packet
`artifacts/v3_epk_positive_fingerprint_readiness_packet_1025.json` therefore
does not expand the universe or reuse these external labels under ePK; it
records the re-audit blocker that must be cleared before any future ePK
counting or external hard-negative claim.
`artifacts/v3_epk_external_hard_negative_reaudit_plan_1025.json` keeps that
blocker concrete: all three current external labels are present and evidence
separated, but their ePK status is only `planned_not_scored` until a future ePK
scoring rule and inverse-gate policy are implemented and terminal review is
rerun under the expanded ontology.
`artifacts/v3_epk_draft_fingerprint_spec_1025.json` carries the same restriction
forward into the draft scorer plan: the three external hard negatives are listed
only as review-only re-audit rows, not as ePK evaluation evidence, until they are
rescored with a text-free ePK rule and pass the expanded-ontology terminal
review and label-factory gates.
`artifacts/v3_epk_local_evidence_audit_1025.json` does not change that external
contract. It only profiles local ePK-row evidence for future scorer design and
leaves every external label outside ePK predictive evidence until the scorer and
re-audit gates exist.
`artifacts/v3_epk_text_free_local_axis_prototype_1025.json` also stays inside
that boundary: it materializes only three ready local M-CSA ePK rows as binary
geometry-derived axes and still keeps all existing external hard negatives
unscored under ePK until an expanded-ontology scorer, threshold policy,
terminal-review rerun, and label-factory gate exist.
`artifacts/v3_epk_acceptor_geometry_axis_gap_plan_1025.json` remains local to
the same M-CSA ePK scorer-development lane. It does not score any external hard
negative under ePK and does not change the `label_factory_v1_8fp` contract for
`uniprot:P06744`, `uniprot:P78549`, or `uniprot:Q3LXA3`.
`artifacts/v3_epk_nonready_ligand_repair_plan_1025.json` is also local to the
M-CSA ePK preparation lane; it only records repair actions for `m_csa:282` and
`m_csa:662` and does not reopen external import evidence.
`artifacts/v3_epk_nonready_ligand_alternate_structure_plan_1025.json` remains
in that same local repair lane. It screens graph-linked alternates for those
two M-CSA rows, but still does not approve an override, rerun local evidence,
or score external hard negatives under ePK.
`artifacts/v3_epk_nonready_ligand_exclusion_decision_1025.json` is likewise
local to M-CSA ePK preparation. It excludes `m_csa:282` and `m_csa:662` from
current ePK threshold calibration because the alternate review found no
gamma-plus-metal mapped repair structure; it does not rescore or reinterpret
the imported external hard negatives.
`artifacts/v3_epk_acceptor_axis_threshold_design_1025.json` records candidate
local acceptor cutoffs for later ePK scorer work, but it selects no threshold
and therefore does not trigger any external hard-negative re-audit yet.
`artifacts/v3_epk_gamma_geometry_feasibility_plan_1025.json` only classifies
which local M-CSA ePK rows could support future atom-level gamma-phosphate
geometry measurement. It performs no measurement and still does not score
external labels under ePK.
`artifacts/v3_epk_gamma_geometry_measurement_sample_1025.json` measures
PG-to-candidate-hydroxyl distances for the two local gamma-capable M-CSA rows,
but it is still not an external hard-negative score or expanded-ontology
terminal review.
`artifacts/v3_epk_acceptor_identity_review_1025.json` reviews those measured
hydroxyl atoms as local source-supported acceptor candidates only. It keeps
mechanism text in review context, preserves text-free scoring boundaries, and
does not rescore or reinterpret `uniprot:P06744`, `uniprot:P78549`, or
`uniprot:Q3LXA3` under ePK.
`artifacts/v3_epk_atp_state_evidence_plan_1025.json` is also local to M-CSA
ePK preparation: it screens `m_csa:640` graph-linked PDB structures for
ATP-state analog context, finds gamma-capable ANP/Mg alternates with catalytic
residue mapping, and identifies `3TM0` as the only gamma-capable alternate with
acceptor-like `B31` context plus a 3.558 Angstrom ANP PG-to-B31 oxygen
measurement. It still does not run external ePK scoring.
`artifacts/v3_epk_gamma_threshold_control_plan_1025.json` remains inside that
same local scorer-design boundary. It uses the three review-only positive-like
distances to define threshold-control requirements, but it selects no
threshold, builds no ePK score, and keeps the external hard negatives outside
ePK predictive evidence until a future scored re-audit is implemented.
`artifacts/v3_epk_negative_control_gamma_distance_distribution_1025.json` is
also local review evidence only. It starts sibling ATP-phosphoryl-transfer
negative controls and finds a close dNK non-ePK control at 3.232 Angstrom,
which blocks gamma-distance-only threshold selection before any external
hard-negative ePK re-audit can be meaningful.
`artifacts/v3_epk_sibling_negative_control_alternate_structure_plan_1025.json`
extends only that local control surface: it screens bounded graph-linked
alternate PDB structures for unmeasured sibling controls and identifies three
future distance-measurement candidates. It still does not score ePK or touch
the external hard-negative labels.
`artifacts/v3_epk_sibling_negative_control_alternate_gamma_distance_sample_1025.json`
then measures those three local sibling alternate controls as review-only
counterevidence, with nearest ANP PG-to-hydroxyl distances of 4.175 Angstrom
for `m_csa:592`, 7.910 Angstrom for `m_csa:603`, and 9.920 Angstrom for
`m_csa:696`. It calibrates no threshold and still does not trigger external
hard-negative ePK scoring.
`artifacts/v3_epk_negative_control_calibration_sufficiency_decision_1025.json`
keeps that conclusion machine-readable: the combined local negative-control
surface remains `blocked_review_only`, threshold selection is
`do_not_select_threshold`, and four sibling ATP-family controls still lack
measured coverage.
`artifacts/v3_epk_missing_sibling_control_source_request_1025.json` and
`artifacts/v3_epk_sibling_control_repair_review_1025.json` remain local
sibling-control hygiene. The PfkB repair review verifies the mapped
gamma-capable `m_csa:663`/`1GQT` case but leaves it blocked by absent metal
context, and it finds no measurement-ready repaired PfkB structures. The same
local hygiene now covers the other missing direct graph-linked families through
`artifacts/v3_epk_sibling_control_repair_review_atp_grasp_1025.json`,
`artifacts/v3_epk_sibling_control_repair_review_ndk_1025.json`, and
`artifacts/v3_epk_sibling_control_repair_review_pfka_1025.json`: ATP-grasp,
NDK, and PfkA all remain at 0 gamma-capable and 0 measurement-ready repaired
structures. This does not open ePK scoring or external hard-negative
rescoring.
`artifacts/v3_epk_missing_sibling_control_post_repair_source_decision_1025.json`
keeps that outcome local to sibling-control sourcing: all six rows now need
external or homolog gamma-capable evidence, but no new candidates are fetched
and no external hard-negative labels are rescored.
`artifacts/v3_epk_precount_gate_status_1025.json` keeps the external lane
explicitly blocked: no ePK score exists, the external hard negatives have not
been rescored, the sibling negative-control distribution is not calibration
ready, and their `label_factory_v1_8fp` out-of-scope labels are unchanged. The
non-ready-row exclusion decision, sibling alternate-control screen, and
sibling alternate-control distance and sufficiency artifacts are local
calibration hygiene only. The later PfkB, PfkA, and ATP-grasp family-specific
homolog mapping and distance artifacts add review-only sibling counterevidence,
and `artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json` blocks
distance-only ePK threshold selection, but they still do not authorize external
hard-negative rescoring, ePK scoring, or label import.
The chain/ligand acceptor disambiguation pass now adds a review-only external
feature screen:
`artifacts/v3_epk_chain_ligand_external_hard_negative_feature_screen_1025.json`.
It records 3/3 imported external hard negatives as abstentions and 0
non-abstentions under the current chain/ligand feature, while keeping
`external_hard_negative_reaudit_scored=false` and
`clean_heldout_performance_claim_permitted=false`. This is useful fail-closed
counterevidence for ePK scorer design, not external-source performance evidence
or an import gate.
The later peptide-identity and outside-query source-expansion artifacts remain
inside the same boundary. The peptide hard-negative probe keeps
`uniprot:P06744`, `uniprot:P78549`, and `uniprot:Q3LXA3` abstained with 0
non-abstentions, while the same-query stress audit only proves the ANP/Mg EC
2.7.11.1 snapshot is exhausted. ATP/Mg, ADP/Mg, and AGS/Mg first-25 novel
scouts find 0 heteromeric topology leads; the AMP-PNP/Mg source expansion
accepts `1O6K`/`1O6L` as PKB/GSK3 review evidence and measures them at
3.542-3.566 Angstrom, but the control rerun stays fail-closed because the
evidence is source-authority dependent and no calibrated ePK scorer or scored
external re-audit exists. A broader ATP/Mg peptide-text scout surfaces
`9L3M`/`9L3U` topology hits, but source validation blocks both as outer
mitochondrial transmembrane helix translocase contexts, reinforcing that broad
source search hits are not external performance evidence.
The source-expansion peptide-role audit then makes the same boundary explicit:
`1O6K`/`1O6L` pass the review-only source-free peptide-role axis, `9L3M`/`9L3U`
remain blocked, and no imported external hard negative is rescored. The
substrate-mode gap audit combines five peptide-mode positives and three
protein-substrate positive-like controls. The follow-on unified
substrate-identity rule probe now hits all eight positive-like rows and keeps
the three imported external hard negatives at 0 review-only feature
non-abstentions, but it remains diagnostic only: `m_csa:640` ligand-analog
evidence is excluded, thresholds are uncalibrated, and no real external
hard-negative scored re-audit has been run.
The MEK1/ERK1 follow-up stays within that same external-hard-negative
boundary. Source adjudication and a source-free topology-ambiguity probe now
block the `7CAG`/`8BMS` residual broad-role false hits, but a broader stress
audit leaves `2JJ2`, `4HPU`, `7B56`, and `7ZDT` unblocked. These artifacts do
not rescore `uniprot:P06744`, `uniprot:P78549`, or `uniprot:Q3LXA3`, do not
claim clean held-out performance, and do not authorize label import.
