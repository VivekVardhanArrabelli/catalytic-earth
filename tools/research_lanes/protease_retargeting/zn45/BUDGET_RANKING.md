# Confidence filtering is not a retest ranking rule

Question: after the existing Zn45 confidence filter, do highest complex pLDDT
or lowest protein–substrate minimum PAE prioritize elevated reporter-screen
signals at the reconstructed 19-member shortlist size?

This is an exposed, retrospective decision analysis, not a preregistered
prediction experiment. Metrics, directions, author filter, executed assay
window and >1.5-fold threshold were inherited before this calculation. Stop
at these two ranks and this primary budget; preserve full curves without
choosing a favorable new cutoff. Lexical variant keys break ties, with the
possible boundary-tie capture range also reported.

| Policy within the 211 filter-passing variants | Signals in 19 selections | Boundary-tie range |
| --- | ---: | ---: |
| Highest five-sample mean complex pLDDT | 3 | 3–3 |
| Lowest five-sample mean ipae_min | 0 | 0–1 |
| Uniform selection, expected count | 1.711 | Not a measured selection |

The existing filter retains all 19 >1.5-fold signals from 378 screened variants.
Uniform selection of 19 from all 378 expects 0.955 signals, but that comparator
mixes filter enrichment with ranking and cannot isolate the latter. The
pLDDT shortlist captures 3/19 of the available signals (1.75 times the uniform
filtered expectation); this modest observed enrichment does not establish a
reliable prospective allocator. Lowest PAE is not supported as a retest
allocator on this retained landscape, even allowing its cutoff tie.
Keep the filter's utility distinct from rank-based activity prediction.
Neither shortlist outcome is statistically decisive: under uniform selection
from this fixed landscape, at least three signals occurs with probability about
0.237 and zero with probability about 0.153. These conditional references are
not biological uncertainty estimates.

These are one-well reporter slopes, not confirmed improved turnover, intended
bond cleavage or specificity. Shared WT/blank normalization and five model
samples are not biological replicates. The existing 360–720 versus commented
540–900 s fitting-window discrepancy changes threshold membership; the
executed window is unchanged. No threshold tuning, new model prediction,
source acquisition, inactive label or new biological experiment was performed.

The retained TDPn3 knockout lacks an exact substitution; deleting its catalytic
base also removes scored atoms. Zn45 low-signal variants use another scaffold
and substrate and have no inactivity bound. They cannot validate the frozen
TDPn3 geometry endpoint. This source-evidence route is closed on present inputs;
new matched primary construct/assay evidence would be required to reopen it.
The closed water/context comparisons remain closed.

The stronger feasible alternative was another control-source search for the
same geometry endpoint. The retained source limitations and critical review
show why that cannot presently unlock discrimination; this analysis instead
resolves the actionable filter-versus-rank distinction using existing measured
data. It does not make Atlas a validated designer. Atlas retains the useful
constraint that fold/interface confidence and activity-prioritization evidence
must be represented separately.

Next consequential action: establish whether existing author primary data can
support a sequence- and dose-matched intended-bond specificity comparison on
more than one target. Inspect exact construct aliases, reporter calibrations,
product identities and assay doses before any proposed model/geometry score.
Stop that bounded source feasibility inquiry if comparable endpoints are
absent; do not convert arbitrary fluorescence units into cross-reporter rates
or repeat the already-known TDPn3/TDPr3 identity ambiguity as a result.

Reproduction: `python tools/research_lanes/protease_retargeting/zn45/budget_ranking.py`.
`budget_ranking_result.json` pins the existing joined CSV hash and contains both
shortlists; `budget_ranking_curves.csv` retains all 422 budget/rank outcomes.
Primary-file provenance remains `Zn45-source-manifest-v1.json`; the existing
`zn45_activity_score_analysis.json` and `Zn45-score-definitions-v1.json` define
the reconstructed signals and confidence fields. No raw source was overwritten.
