# D11 Residual → Rule-Gate Integration (Lever 2)

Run: 2026-06-02T00:02:57Z

D11 Lever 2 integration: add the confirmed out-of-span residual to the per-channel RULE gate as a third confounded-safe agnostic-lift channel, and measure its marginal operating-point lift over the geometry+cofactor gate, stratified, at the >=85% (and >=90% if reachable) in-scope retention floor.

Rule: `abstain if geometry_score < tg OR (cofactor_max < signature AND cofactor_max < tc) OR (cofactor_max < signature AND residual_novelty >= tr)`

In-scope 47 | OOS 79 (confounded 6, agnostic 73) | atlas 184

## Channel separation (AUC in-scope > OOS; 0.5 = chance)

| channel | all OOS | confounded | agnostic |
| --- | ---: | ---: | ---: |
| geometry_top1_score | 0.756935 | 0.840426 | 0.750073 |
| cofactor_max_score | 0.628064 | 0.280142 | 0.65666 |
| out_of_span_residual | 0.72098 | 0.663121 | 0.725736 |

The residual channel reproduces the confirmed signal here: all-OOS AUC 0.72098 (embedding eval 0.721; cross-check True).

## Rule gate: two-channel vs three-channel (with residual-agnostic-lift)

| floor | gate | retain | OOS-abstain | confounded | agnostic | tg / tc / tr |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 90pct_retention | 2ch geom+cof | — (no point clears floor) | | | | |
| 90pct_retention | 3ch +residual | — (no point clears floor) | | | | |
| 85pct_retention | 2ch geom+cof | 0.8511 | 0.3038 | 0.1667 | 0.3151 | 0.32 / 0.02 / None |
| 85pct_retention | 3ch +residual | 0.8511 | 0.3797 | 0.1667 | 0.3973 | 0.28 / 0.02 / 10.524882 |

## Verdict

- **90pct_retention**: inconclusive — no rule-gate point clears this retention floor for one/both gates
- **85pct_retention**: OOS 0.3038 → 0.3797 (lift 0.0759); confounded 0.1667 → 0.1667; adds lift: True, confounded-safe: True → **pass: True**
- Operative floor: **85pct_retention** (highest floor with a two-channel point)

The confirmed residual adds operating-point lift to the rule gate: at the 85pct_retention floor it raises OOS-abstain-recall from 0.3038 (geometry+cofactor) to 0.3797 (+0.0759) while preserving confounded safety (0.1667 vs 0.1667). The lift is real but research-grade: the residual threshold is eval-pool-relative (atlas calibration saturates).

The residual-agnostic-lift fires only where the cofactor signature is weak (cof < signature), exactly like the cofactor lift, so confounded rows remain gated by geometry alone -- the residual cannot make keep/abstain calls on the safety-critical subset, where it is weaker than geometry (AUC ~0.66 vs 0.84).

1.0 of held-out rows sit above the atlas residual maximum, so the atlas-percentile calibration saturates (True); the residual threshold tr is a research operating point, not a deployable constant. A deployable residual calibration or the Lever 4 expanded family set is needed before production.
