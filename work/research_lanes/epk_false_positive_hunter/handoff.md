# ePK false-positive hunter handoff

- Last updated: 2026-05-21T03:19:02Z
- Started: 2026-05-21T02:30:35Z
- Ended: 2026-05-21T03:19:02Z
- Measured minutes: 48.45
- Primary outcome: evidence_against
- Pushed commit: 9a6530952dbcca394e06f5833a9ecc1ebb572a44 (remote run commit; local checked-out HEAD update is blocked by linked-worktree metadata permissions).
- Rule under attack: entry-level any-context `v4_oligomeric_atp_terminals_no_mg_required` review-only guard risk plus current ePK substrate-mode/source-free topology rules.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Executed the handoff next query in three bounded passes with compact artifacts only; no raw coordinate dumps were written.

- Helper: `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress.py`
- Broad source-context/later-offset pass: 340 entry rows, 750 coordinate contexts, 32 materializer contexts, 0 fetch/materializer errors.
- Targeted RAF/MEK/ERK/JNK/mTOR kinase-complex pass: 260 entry rows, 592 coordinate contexts, 37 materializer contexts, 0 fetch/materializer errors.
- ePK-query non-ePK contaminant pass: 160 entry rows, 349 coordinate contexts, 121 materializer contexts, 0 fetch/materializer errors.
- Total selected review work: 760 entry rows, 1,691 coordinate contexts, 190 materializer contexts.

## Result

Primary outcome is `evidence_against` on the explicit bounded surfaces.

- No source-context ePK overblock hit was found. `4UX9` and `9O0V` were the only non-fixed source-context ePK entry-level guard candidates; deposited plus biological assembly contexts produced 0 substrate-mode materializer hits.
- No later-offset non-ORC ATPase split-risk residual was found; broad and targeted later-offset passes found 0 deposited-v4/assembly-chain-floor split-risk entries.
- The contaminant pass found 48 ePK-query non-ePK v4 contaminants, 47 with assembly-v4 contexts, but 94 contaminant materializer contexts produced 0 substrate-mode hits.
- Fixed ORC/OCCM/MCM controls still showed 27 context-v4-blocked topology-clear non-ePK contexts.

## Evidence For / Against

Evidence against a new counterexample:

- 760 selected entries and 1,691 coordinate contexts across source-context ePK, later-offset ATPase, and ePK-query contaminant surfaces had no residual topology-clear non-ePK counterexample and no source-context ePK overblock hit.
- All three passes had 0 fetch errors and 0 materializer context errors.

Evidence for continued caution:

- Full-text peptide/substrate queries are strongly contaminated by non-ePK ATPase-like structures; future ePK overblock work needs source-valid kinase classification rather than full-text alone.
- Only two non-fixed source-context ePK guard candidates survived in these query quotas (`4UX9`, `9O0V`), so this is bounded evidence, not sufficiency.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- The normal linked-worktree index remains unwritable/stale: `git status` shows tracked lane files as staged deletions plus untracked replacements.
- Alternate-index commit/push succeeded for the run commit above; local HEAD/ref cleanup still requires external permission repair.

## Next Query

Build a source-valid ePK seed set from kinase-classified polymer/entity evidence rather than full-text peptide hits: RAF/MEK/ERK, JNK, CDK/cyclin, receptor tyrosine kinase dimer, and mTORC1/2 ATP/ANP assemblies with deposited-or-assembly v4 true; force the materializer on all deposited and biological assembly contexts. In parallel, prefilter non-ePK v4 contaminants for local Tyr or N-terminal Ser/Thr/Tyr gamma geometry before materialization to avoid no-hit rows. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress.py`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress_20260521_023614Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_stress_targeted_20260521_025652Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_epk_overblock_later_offset_contaminant_stress_20260521_030753Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`

Existing uncommitted prior lane artifacts from earlier runs are still present and were not reverted.
