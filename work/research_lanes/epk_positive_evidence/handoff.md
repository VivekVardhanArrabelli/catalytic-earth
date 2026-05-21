# ePK Positive Evidence Handoff

Last updated: 2026-05-21T05:19:08Z

Primary outcome: `evidence_for`.

This run source-adjudicated the full 84-row `epk_candidate_evidence_v1` backfill rather than emitting production labels or production scoring artifacts. The new all-row adjudication artifact keeps source review separate from source-free geometry and keeps every row review-only/non-countable.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/candidate_source_adjudication_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/candidate_source_adjudication_all_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/candidate_source_adjudication.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- `candidate_source_adjudication_all_20260521.json` reviews all 84 backfilled candidate rows across 48 unique PDB IDs.
- Coordinate states observed: 66 `active_gamma` and 18 `transition_analog`.
- The all-row pass found 39 source-supported review-only rows:
  - 17 active-gamma peptide/fragment rows with local metal.
  - 6 transition/pseudosubstrate rows.
  - 16 source-supported rows blocked by no-local-metal or equivalent non-countable context.
- Named stress anchors were covered: `23FC`, `5HVK`, `9UUR`/`9UUX`, `3X2U`/`3X2V`/`3X2W`, `1QMZ`, `1L3R`, `5LIH`, and `1HE1`.
- RCSB entry/polymer/mmCIF refresh plus UniProt feature checks reduced source-mapping/claim unresolved rows to zero. The remaining manual-review set is source-mapped but source-claim-unconfirmed.

## Evidence Against

- No source-supported folded-protein local-metal active-gamma candidate was upgraded. Folded or folded-like support remains no-local-metal, source-unconfirmed, or non-ePK ownership.
- The all-row pass found 38 counterexample/non-ePK ownership rows, dominated by MCM helicase ATPase, CydDC ABC transporter, 26S proteasome ATPase, F1-ATPase, KaiC, and ExoS/Rac GTPase contexts.
- Seven source-mapped rows remain source-claim-unconfirmed: `1L3R`, `4DFX`, `4DG0`, one `4EKK` row, `7B56`, and two `7KL1` rows.
- All adjudicated rows retain `policy_decision=review_only_abstain`, `countable_label_candidate=false`, `production_claim_allowed=false`, and `source_review_not_predictive_coordinate_feature=true`.

## Candidate-Row Notes

- Source support is review context only. It must not become a predictive coordinate feature.
- Product, analog, transition, no-local-metal, peptide/fragment, and ownership-confounded rows remain non-countable unless a future frozen policy is preregistered and survives stress review.
- The all-row artifact is the current review surface for the 84 backfilled rows. Prefer it over the sampled priority artifact unless specifically auditing first-priority rows.

## Blockers

- Startup `git fetch origin` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-positive-evidence` failed with the same `FETCH_HEAD` permission blocker.
- `git merge --ff-only origin/research/epk-positive-evidence` failed while creating `.git/worktrees/catalytic-earth-epk-positive/ORIG_HEAD.lock`.
- The local branch still reports behind `origin/research/epk-positive-evidence`; use temporary-index/ref-safe commit/push handling if normal git continues to reject linked-worktree metadata writes.

## Next Query

Manually adjudicate the seven source-mapped but source-claim-unconfirmed rows:

- `1L3R` PKI transition mimic.
- `4DFX`/`4DG0` SP20 PKA inhibitor rows.
- `4EKK` Akt/GSK3 row `D:6`.
- `7B56` CaMKII/alpha-actinin Ser822.
- `7KL1` CaMKII/GluN2B donor-ownership rows.

At the next RCSB weekly release, rerun current-date/2026 exact-ligand surfaces and the `23FC` publication metadata check.

Production claims/label changes remain forbidden: yes.
