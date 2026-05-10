# Geometry Features

## Purpose

The V2 baseline uses text and motif evidence. That is useful only as a scaffold.
The next scientific-quality step is geometry-aware active-site representation.

`build-geometry-features` converts M-CSA catalytic residue positions into simple
3D descriptors by fetching public PDB mmCIF files and measuring residue
coordinates.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-v1-graph \
  --max-mcsa 500 \
  --page-size 100 \
  --out artifacts/v1_graph_500.json

PYTHONPATH=src python -m catalytic_earth.cli graph-summary \
  --graph artifacts/v1_graph_500.json \
  --out artifacts/v1_graph_summary_500.json

PYTHONPATH=src python -m catalytic_earth.cli build-v2-benchmark \
  --graph artifacts/v1_graph_500.json \
  --out artifacts/v2_benchmark_500.json

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph_500.json \
  --max-entries 500 \
  --out artifacts/v3_geometry_features_500.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features_500.json \
  --out artifacts/v3_geometry_retrieval_500.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --out artifacts/v3_abstention_calibration_500.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_geometry_label_eval_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-failures \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_geometry_failure_analysis_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_in_scope_failure_analysis_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-coverage \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_cofactor_coverage_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-policy \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_cofactor_policy_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-seed-family-performance \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --abstain-threshold 0.4115 \
  --out artifacts/v3_seed_family_performance_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-score-margins \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --out artifacts/v3_geometry_score_margins_500.json

PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --out artifacts/v3_hard_negative_controls_500.json

PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates \
  --geometry artifacts/v3_geometry_features_500.json \
  --retrieval artifacts/v3_geometry_retrieval_500.json \
  --out artifacts/v3_label_expansion_candidates_500.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-structure-mapping-issues \
  --geometry artifacts/v3_geometry_features_500.json \
  --out artifacts/v3_structure_mapping_issues_500.json

PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices \
  --artifact-dir artifacts \
  --out artifacts/v3_geometry_slice_summary.json
```

## Current Feature Set

For each M-CSA entry with structure positions:

- chosen PDB id
- catalytic residue nodes
- residue codes, chain ids, and residue ids
- residue centroids
- CA coordinates when present
- pairwise catalytic-residue distances
- missing-position counts and observed residue-code mismatch diagnostics
- auth-vs-label residue-number fallback for mmCIF structures that use different
  sequence numbering namespaces
- proximal non-polymer ligands from mmCIF `HETATM` records
- inferred cofactor families from nearby ligands (for example heme, flavin, PLP,
  cobalamin, metal ions, SAM, Fe-S clusters; `5PA` is treated as PLP-family
  context)
- structure-wide non-polymer ligand inventory, nearest active-site distances,
  and structure-wide inferred cofactor families for distinguishing missing
  local evidence from cofactors elsewhere in the selected structure
- cofactor evidence level for retrieval hits (`ligand_supported`,
  `role_inferred`, `absent`, or `not_required`)
- substrate-pocket residue context from nearby protein `ATOM` records
- pocket descriptors (hydrophobic/polar/charge/aromatic/sulfur fractions and
  mean residue distance to active site)

## Geometry-Aware Retrieval

`run-geometry-retrieval` ranks seed mechanism fingerprints with:

- residue signature overlap
- role hint overlap
- ligand-supported cofactor context
- substrate-pocket descriptor compatibility
- serine-hydrolase mechanistic coherence for the Ser nucleophile requirement
- cobalamin radical rearrangement scoring with explicit B12/cofactor evidence
- flavin dehydrogenase/reductase scoring separated from flavin monooxygenases
- counterevidence penalties for heme-only metal-role overlap, ATP/ADP/APC
  transfer context, carbon-transfer ligand context, thiamine/biotin/
  phosphomutase transfer contexts, hydrogenase and metal-redox ligand context,
  redox electron-transfer roles, histidine-only metal-role sites, molybdenum-
  center heme-like contexts, PLP-like lysine motifs without PLP, absent B12
  context, nonflavin Fe-S contexts, nonhydrolytic Ser/His electrophile sites,
  thiamine carboligation without local flavin redox/oxygenation evidence, zinc
  methyltransfer contexts, nonhydrolytic hydratase/dehydratase text contexts,
  phosphoenolpyruvate transfer, metal-bound dehydrogenase text, farnesyl/prenyl
  transfer context, alpha-ketoglutarate hydroxylation, heme dehydratase
  contexts, flavin mutases, and flavin contexts missing reductant or
  monooxygenase substrate support
- catalytic-cluster compactness from pairwise distances

This is still a weak baseline, but it is materially better than pure text
overlap because it makes catalytic residue identity and spatial arrangement part
of the retrieval score.

## Abstention And Hard Negatives

`calibrate-abstention` now records both the conservative zero-false threshold
and a positive-retention reference point. Its default `--thresholds auto`
includes observed score-boundary candidates, not only a coarse fixed grid.

Current slices:

- 20-entry regression slice: threshold 0.4104, 20/20 evaluable, 7/7 in-scope
  positives retained, 0 out-of-scope false non-abstentions, 0 hard negatives.
- 100-entry expanded slice: threshold 0.4115, 100/100 evaluable, 25/25
  in-scope positives retained, 0 out-of-scope false non-abstentions, 0 hard
  negatives.
- 125-entry expanded slice: threshold 0.4115, 124/125 evaluable, 38/38
  in-scope positives retained, 0 out-of-scope false non-abstentions, 0 hard
  negatives, 0 near misses, and score gap 0.0308.
- 150-entry expanded slice: threshold 0.4115, 148/150 evaluable, 43/44
  in-scope positives retained, 0 out-of-scope false non-abstentions, 0 hard
  negatives, 0 near misses, and 1 evidence-limited in-scope abstention. That
  remaining case is `m_csa:132`, where the selected `1LUC` structure lacks the
  expected flavin/NAD cofactor evidence.
- 225-entry stress slice: threshold 0.4115, 221/224 geometry entries evaluable,
  70/71 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 1 evidence-limited in-scope abstention.
  The remaining case is `m_csa:132`, where the selected `1LUC` structure lacks
  the expected flavin/NAD cofactor evidence.
- 275-entry stress slice: threshold 0.4115, 271/274 geometry entries evaluable,
  80/81 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 1 evidence-limited in-scope abstention.
  The remaining case is `m_csa:132`, where the selected `1LUC` structure lacks
  the expected flavin/NAD cofactor evidence.
- 300-entry stress slice: threshold 0.4115, 296/299 geometry entries evaluable,
  85/86 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 1 evidence-limited in-scope abstention.
- 325-entry stress slice: threshold 0.4115, 320/324 geometry entries evaluable,
  90/91 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 1 evidence-limited in-scope abstention.
- 350-entry stress slice: threshold 0.4115, 344/349 geometry entries evaluable,
  93/94 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 1 evidence-limited in-scope abstention.
- 450-entry stress slice: threshold 0.4115, 442/449 geometry entries evaluable,
  120/124 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 4 evidence-limited in-scope abstentions.
- 475-entry stress slice: threshold 0.4115, 467/474 geometry entries evaluable,
  123/127 in-scope positives retained, 0 out-of-scope false non-abstentions,
  0 hard negatives, 0 near misses, and 4 evidence-limited in-scope abstentions.
  The current abstained positives are `m_csa:132`, `m_csa:353`, `m_csa:372`,
  and `m_csa:430`; all are treated as evidence-limited rather than actionable
  scorer failures.
- 500-entry countable stress slice: threshold 0.4115, 490/498 evaluated
  labeled rows evaluable, 127/131 in-scope positives retained, 0 out-of-scope
  false non-abstentions, 0 hard negatives, 0 near misses, and 4
  evidence-limited in-scope abstentions. The only remaining 500-slice candidate
  is `m_csa:494`.

`artifacts/v3_geometry_slice_summary.json` summarizes the 20-, 30-, 40-, 50-,
60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-, 300-, 325-, 350-,
375-, 400-, 425-, 450-, 475-, and 500-entry slices. It
currently reports zero hard negatives, zero near misses, and zero out-of-scope
false non-abstentions across all slices. Total in-scope failures across slice
rows are 30, max in any slice is 4, and the actionable in-scope failure count
is 0 after separating selected-structure cofactor gaps from scorer failures.

`artifacts/v3_cofactor_coverage_500.json` tracks expected cofactor coverage for
in-scope labels. In the 500-entry countable slice, 105/131 in-scope positives
have local cofactor support, 3 have expected cofactor support only elsewhere in
the selected structure, 17 require no cofactor, and 6 lack
expected structure-wide cofactor evidence. Of the 6 absent-expected-cofactor
rows, 3 are retained and 3 are abstained. The coverage metadata exposes
`evidence_limited_retained_entry_ids`, currently `m_csa:41`, `m_csa:108`,
`m_csa:160`, `m_csa:446`, and `m_csa:486`, so these retained positives can be audited
separately from clean local cofactor matches without changing the abstention
threshold.

`artifacts/v3_cofactor_policy_500.json` sweeps small post-hoc penalties for
absent or structure-only cofactor evidence. It recommends
`audit_only_or_separate_stratum` because no tested policy reduces
evidence-limited retained positives without losing retained positives. The
smallest retained evidence-limited margin is now `0.013`.

## Label Expansion Queue

The 500-entry source slice is now accepted through the label factory except
for one non-countable review candidate:

- geometry entries in expansion artifact: 499
- countable curated labels: 499
- evaluated labeled rows: 498
- evaluable labeled active-site structures: 490
- unlabeled entries remaining: 1
- review notes: `work/label_queue_500_notes.md`
- active-learning review queue: `artifacts/v3_active_learning_review_queue_500.json`
- expert-review export: `artifacts/v3_expert_review_export_500.json`
- factory gate check: `artifacts/v3_label_factory_gate_check_500.json`

The remaining candidate, `m_csa:494`, must flow through the label factory
before it can count.

The structure-mapping issue artifacts currently list 0 non-OK entries for the
20-, 30-, 40-, 50-, 60-, 75-, and 100-entry slices after matching catalytic
residue positions against both mmCIF `auth_*` and `label_*` numbering. The
125-entry slice has 1 labeled out-of-scope mapping issue; the 150- and
175-entry slices each have 2 labeled out-of-scope mapping issues; the 200-,
225-, 250-, 275-, and 300-entry slices each have 3 labeled out-of-scope mapping
issues; the 325-, 350-, 375-, 400-, 425-, 450-, 475-, and 500-entry slices
have 4, 5, 7, 7, 7, 7, 7, and 8 mapping issues respectively.

## Curated Seed Labels

`data/registries/curated_mechanism_labels.json` provides 499 provisional labels,
covering all entries in the 475-entry source slice plus 24 accepted labels from
the 500-entry queue. Labels now carry explicit
`tier`, `review_status`, `confidence`, `evidence_score`, and `evidence`
provenance fields. Labels are intentionally conservative:

- `seed_fingerprint` means the entry maps to one of the current seed mechanism
  fingerprints.
- `out_of_scope` means the entry needs a more specific fingerprint before it
  should be used as a positive label.

These labels are curated enough to test retrieval behavior and abstention, but
they are not a substitute for expert mechanism review.

`docs/label_factory.md` describes the bronze/silver/gold schema, deterministic
promotion/demotion audit, adversarial negative mining, mechanism ontology,
active-learning queue, and expert-review export/import workflow that gates
future label batches.

## Why This Matters

Mechanism-first enzyme discovery cannot rely on EC labels or keyword overlap.
Catalytic function depends on residue identity, spatial arrangement, cofactors,
substrate access, and reaction chemistry. This artifact starts the move from
label retrieval toward active-site geometry retrieval.

## Limitations

- Distances are crude CA-or-centroid descriptors.
- Alternate conformations, insertion codes, and biological assemblies are not
  modeled yet.
- Static PDB structures can miss catalytically relevant conformations.
- Geometry features are evidence, not validation.
- The current retrieval baseline uses simple compactness heuristics, not a
  learned geometry model.
