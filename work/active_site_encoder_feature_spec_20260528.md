# Active-Site Encoder Feature Spec And Feasibility (current702)

Generated: 2026-05-28

## Scope

This is a spec and feasibility artifact only. It does not edit labels, registries, ontologies, thresholds, production scoring, imports, or existing model outputs, and it does not run model training or a sweep.

Question: can active-site-local learned features add value beyond Foldseek, current geometry retrieval, and pretrained sequence models on the frozen Wave 1 split?

## Local Inputs Inspected

- `data/registries/curated_mechanism_labels.json`: 702 current labels.
- `artifacts/v3_geometry_features_1025.json`: active-site residue roles, CA/centroid coordinates, pairwise distances, proximal ligands/cofactors/metals, and pocket descriptors.
- `artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json`: selected-structure and local coordinate materialization status for all 702 rows.
- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`: frozen Wave 1 split assignment, 562 in-distribution and 140 heldout rows.
- `artifacts/v3_wave1_1_diagnostic_benchmark_result_702_20260527.json`: result-card-compatible diagnostic method/result shape.
- `artifacts/v3_mechanism_fingerprint_v2_sublabel_audit_702_20260525.json`: proposal-only v2 auxiliary target source; not canonical labels.

## Feasibility Summary

Minimal encoder-ready rule: geometry entry is present, status is `ok`, at least two active-site residues resolve, at least one residue has role annotations, and at least one pairwise active-site distance exists.

- Encoder-ready rows: 679/702.
- Encoder-ready split coverage: 544/562 in-distribution, 135/140 heldout.
- Current rows with pocket descriptors: 698.
- Current rows with local cofactor family evidence: 306.
- Current rows with structure-level cofactor family evidence: 395.
- Local staged mmCIF files: 692.

Rows not ready under the minimal rule:

- `missing_active_site_coordinates` (2): `m_csa:372`, `m_csa:501`
- `missing_active_site_roles` (4): `m_csa:422`, `m_csa:605`, `m_csa:618`, `m_csa:937`
- `missing_geometry_entry` (4): `m_csa:204`, `uniprot:P06744`, `uniprot:P78549`, `uniprot:Q3LXA3`
- `partial_single_residue_or_no_pairs` (13): `m_csa:105`, `m_csa:137`, `m_csa:193`, `m_csa:318`, `m_csa:327`, `m_csa:360`, `m_csa:531`, `m_csa:536`, `m_csa:604`, `m_csa:610`, `m_csa:620`, `m_csa:628`, `m_csa:649`

The main viable v0 track should train/evaluate on the 679 encoder-ready rows while preserving all 702 rows in manifests and all 140 heldout rows in coverage denominators. The 13 single-residue rows can support a node-only ablation but should not enter the pair-distance/equivariant edge baseline.

## Frozen v0 Feature Spec

Predictive tensors may use only active-site-local evidence:

- Active-site residue node features: residue type, role multihot, atom-count bucket, CA/centroid presence flags, selected-structure coordinate-state flags.
- Active-site pair features: complete graph over resolved active-site residues, CA distance when both CAs exist, centroid/side-chain proxy distance otherwise, distance bins `[0, 3, 4.5, 6, 8, 12, 16, 24, 40]`, and coordinate-source flags.
- Pocket features: hydrophobic, polar, positive, negative, charge-balance, aromatic, sulfur, and mean minimum active-site distance descriptors.
- Cofactor/metal features: local family presence, metal presence, nearest-distance bins, structure-only/absent flags.
- Provenance/evidence features: structural coordinate quality and local ligand evidence tiers only. Label tier, review status, entry IDs, and source paths stay non-predictive manifest fields.

Forbidden predictive tensors: EC, mechanism text, names, expert notes, review rationales, source IDs such as entry/PDB/UniProt IDs, post-hoc repair flags, target labels, and child-label IDs.

Leakage policy: freeze role vocabularies/scalers on in-distribution encoder-ready rows only; map unseen heldout roles to `role_other`; never refit from heldout.

## Model And Eval Plan

Use two small fixed tracks, no large sweeps:

- `active_site_gvp_gnn_v0`: 3-4 layer GVP-GNN or equivalent local equivariant graph model, preferably under 250k parameters.
- `active_site_local_graph_mlp_baseline_v0`: non-equivariant role/residue/distance-bin/pocket/cofactor pooling baseline to isolate model-complexity effects.

Heads:

- Parent v1 label-group head: eight seed fingerprints plus out-of-scope/abstention behavior.
- Binary in-scope vs OOS calibration head.
- Proposal-only v2 auxiliary head where existing v2 proposal rows are present; no canonical child metrics or imports.

Evaluation:

- Reuse the frozen Wave 1 split unchanged: 562 in-distribution, 140 heldout.
- Run exactly five seeds: 11, 23, 37, 53, 71.
- Report heldout primary-v1 accuracy, macro F1, OOS false non-abstention rate, unavailable/not-evaluable counts, and mean/std over seeds.
- Compare against Foldseek structural NN, active-site geometry retrieval, Sequence-NN 3-mer, and available pretrained sequence/structure tracks in the existing Wave 1 result-card shape.

## Cache Manifest Decision

A tensor cache was not emitted because no `build-active-site-encoder-cache` CLI exists in this repo, and this run is limited to spec/report artifacts. A cheap local cache is feasible for the 679 minimal rows using `artifacts/v3_geometry_features_1025.json`, `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`, `artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json`, and the local `artifacts/v3_foldseek_coordinates_1000/*.cif` cache.

Proposed future command contract:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-active-site-encoder-cache \
  --labels data/registries/curated_mechanism_labels.json \
  --geometry artifacts/v3_geometry_features_1025.json \
  --split artifacts/v3_sequence_nn_label_manifest_current702_20260525.json \
  --foldseek-readiness artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json \
  --coordinate-dir artifacts/v3_foldseek_coordinates_1000 \
  --out artifacts/v3_active_site_encoder_cache_current702_20260528.jsonl
```

The exact row-level cache manifest is embedded in `artifacts/v3_active_site_encoder_feature_spec_702_20260528.json` under `cheap_local_cache_manifest.cache_rows`.
