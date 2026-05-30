# D11 Mechanism Relationship Evaluation v0

Run created: `2026-05-30T18:03:07Z`

## Decision

Relationship evaluation is now measurable, but only as a hygiene/feasibility pass. The real D11 pass is blocked because the selected organic cofactor channels have aggregate ESM metrics but no retained row-level score sidecars for flavin, heme, or PLP.

No labels, registries, ontologies, imports, production scoring, global thresholds, heldout splits, or model weights were changed. No model was trained or refit.

## Pre-Registered Relationships

Relationships were defined before reading row-level predictions from `data/registries/mechanism_ontology.json` and `data/registries/mechanism_fingerprints.json`: exact same fingerprint, shared ontology family, and shared normalized cofactor family. Heldout predictions were not used to define adjacency.

| Relationship pair | Types |
| --- | --- |
| `ser_his_acid_hydrolase` <-> `metal_dependent_hydrolase` | same_ontology_family |
| `radical_sam_enzyme` <-> `cobalamin_radical_rearrangement` | same_ontology_family |
| `flavin_monooxygenase` <-> `flavin_dehydrogenase_reductase` | same_ontology_family, shared_normalized_cofactor |

## Counts

- Current rows: 702
- Heldout current primary rows after 497/750 readthrough: 43
- Heldout secondary-probe rows: 3
- Heldout OOS rows: 94
- Tuning-adjacent flagged rows: 29

## Relationship Rank Metrics

| Surface | Variant | Queries | Exact top1 | Family top3 any | Family MRR | Notes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Experimental geometry per-fingerprint score vector | `cosine` | 45 | 0.977778 | 1 | 1 | high: derived from current hand-authored fingerprint scoring; hygiene only |
| Experimental geometry per-fingerprint score vector | `robust_l2` | 45 | 0.977778 | 1 | 1 | high: derived from current hand-authored fingerprint scoring; hygiene only |
| Predicted geometry score query vs experimental atlas score vector | `cosine` | 45 | 0.711111 | 0.8 | 0.771984 | high: derived from current hand-authored fingerprint scoring; hygiene only |
| Predicted geometry score query vs experimental atlas score vector | `robust_l2` | 45 | 0.711111 | 0.733333 | 0.739502 | high: derived from current hand-authored fingerprint scoring; hygiene only |
| Experimental geometry raw descriptor vector | `cosine` | 45 | 0.6 | 0.866667 | 0.747263 | moderate: active-site annotations and local ligand/cofactor context; no heldout predictions used |
| Experimental geometry raw descriptor vector | `robust_l2` | 45 | 0.733333 | 0.911111 | 0.843158 | moderate: active-site annotations and local ligand/cofactor context; no heldout predictions used |
| Predicted geometry raw query vs experimental atlas descriptor vector | `cosine` | 45 | 0.511111 | 0.666667 | 0.62561 | moderate: same descriptor schema, predicted queries lack ligand/cofactor context |
| Predicted geometry raw query vs experimental atlas descriptor vector | `robust_l2` | 45 | 0.511111 | 0.6 | 0.605816 | moderate: same descriptor schema, predicted queries lack ligand/cofactor context |
| Deterministic sequence k-mer control vector | `cosine` | 46 | 0.282609 | 0.652174 | 0.577469 | low: deterministic sequence composition/k-mer features; known weak control, not PLM |
| Deterministic sequence k-mer control vector | `robust_l2` | 46 | 0.26087 | 0.652174 | 0.591877 | low: deterministic sequence composition/k-mer features; known weak control, not PLM |

The hand-authored per-fingerprint score surface is the strongest hygiene surface, but it is explicitly tuning-adjacent. Raw geometry and k-mer controls are weaker; predicted geometry generally degrades placement relative to experimental geometry.

## Experimental vs Predicted Geometry

| Check | Overlap rows | Mean raw cosine | Mean robust L2 |
| --- | ---: | ---: | ---: |
| `raw_descriptor_predicted_vs_experimental_same_row` | 126 | 0.969725 | 3.570024 |
| `fingerprint_score_predicted_vs_experimental_same_row` | 126 | 0.949848 | 3.408777 |

Largest predicted-vs-experimental geometry deltas are stored in the JSON under `experimental_vs_predicted_preservation_checks.*.largest_delta_rows`.

## Boundary Behavior

| Surface | Variant | Boundary rows | FMO/flavin focus | Top1 primary cluster | Top1 flavin/FMO cluster |
| --- | --- | ---: | ---: | ---: | ---: |
| Experimental geometry per-fingerprint score vector | `cosine` | 93 | 4 | 0.956989 | 0.311828 |
| Experimental geometry per-fingerprint score vector | `robust_l2` | 93 | 4 | 0.978495 | 0.11828 |
| Predicted geometry score query vs experimental atlas score vector | `cosine` | 84 | 4 | 0.97619 | 0.27381 |
| Predicted geometry score query vs experimental atlas score vector | `robust_l2` | 84 | 4 | 0.97619 | 0.059524 |
| Experimental geometry raw descriptor vector | `cosine` | 93 | 4 | 0.978495 | 0.193548 |
| Experimental geometry raw descriptor vector | `robust_l2` | 93 | 4 | 0.967742 | 0.225806 |
| Predicted geometry raw query vs experimental atlas descriptor vector | `cosine` | 84 | 4 | 0.988095 | 0.130952 |
| Predicted geometry raw query vs experimental atlas descriptor vector | `robust_l2` | 84 | 4 | 0.952381 | 0.059524 |
| Deterministic sequence k-mer control vector | `cosine` | 98 | 4 | 0.979592 | 0.489796 |
| Deterministic sequence k-mer control vector | `robust_l2` | 98 | 4 | 0.969388 | 0.367347 |

FMO/flavin-redox focus rows are reported row-by-row in JSON. `m_csa:497` and `m_csa:750` are read as current OOS boundary rows, not as primary flavin support.

## Hygiene vs True D11

- Hygiene status: `partial_hygiene_pass_only`.
- Real pass status: `blocked_missing_row_level_cofactor_channel_scores`.
- Missing blocker: retained row-level selected ESM cofactor scores for flavin/heme/PLP. Existing artifacts keep aggregate separability but not per-entry selected scores or bins.
- M-Ionic metal row scores exist, but metal alone is not the cofactor-augmented representation required for a true D11 pass.

## Concrete Next Gate

Persist row-aligned selected organic cofactor score sidecars with `entry_id`, `split_assignment`, `class`, `score`, threshold/bin, and source model for all 702 current rows. Then rerun this relationship eval with a cofactor-augmented predicted-geometry query representation and frozen class-conditional trust weights. Do not tune on heldout.

## Required Handoff

- Wall-clock start: `2026-05-30T12:50:46-0500`
- Wall-clock end: `2026-05-30T13:04:00-0500`
- Elapsed time: `13.23 minutes (794 seconds)`
- Git branch: `main`
- Git HEAD: `f8eb8add00dc942e757c467105078bffd53ff65d`
- Dirty files before write: `clean`
- Dirty files after write: `?? artifacts/v3_mechanism_relationship_eval_v0_20260530.json
?? work/mechanism_relationship_eval_v0_20260530.md`
- Disk after write: `/dev/disk3s5   228Gi   153Gi    35Gi    82%    1.9M  366M    1%   /System/Volumes/Data`
- Input artifacts: see JSON `source_artifacts` with SHA-256 provenance hashes.
- Output artifacts: `artifacts/v3_mechanism_relationship_eval_v0_20260530.json`, `work/mechanism_relationship_eval_v0_20260530.md`.
- Validation commands/results: `python -m json.tool artifacts/v3_mechanism_relationship_eval_v0_20260530.json >/dev/null` passed; `PYTHONPATH=src python -m catalytic_earth.cli validate` passed; `git diff --check` passed; unit tests not run because this was artifact/report-only.
- Blockers: real D11 pass blocked by missing retained row-level selected ESM cofactor scores for flavin/heme/PLP and no row-aligned cofactor-augmented predicted-geometry representation.
- Exact next action: persist row-level selected organic cofactor sidecars, then rerun this eval without heldout tuning.
- Next run should: `continue`.
