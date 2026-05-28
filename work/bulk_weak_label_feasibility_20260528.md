# Bulk Weak-Label Feasibility - 2026-05-28

Run time: 2026-05-28T07:18:11Z

Run mode: read-only feasibility artifact. No labels, registries, ontologies, thresholds, production scoring, imports, or model outputs were edited. No source download or bulk ingestion was attempted. The filesystem was already below the requested 10 GiB free-space guardrail when the run began, so all database download steps were treated as no-go.

Primary artifact: `artifacts/v3_bulk_weak_label_feasibility_20260528.json`

## Bottom Line

Bulk weak labels are conditionally feasible as bronze training or retrieval signal, not as evaluation truth. The strongest immediate source candidates are UniProt/Swiss-Prot reviewed EC/Rhea annotations, Rhea reaction mappings, and CARD/AMRFinder-style enzyme-family metadata for known public AMR enzyme classes. BRENDA and CAZy remain plausible but not locally verifiable in this run because the repo only has registered source definitions, not cached source metadata.

M-CSA and frozen external panels must remain gold/silver evaluation. Bronze source labels can help train, retrieve, stratify, or prioritize review only after release/version capture, deduplication, and leakage checks.

## Local Inventory

Verifiable local evidence:

| Source/surface | Local artifact | Verifiable local count/status |
|---|---|---:|
| M-CSA-centered graph | `artifacts/v1_graph_1025.json` | 1,003 M-CSA entry nodes; 874 EC nodes; 1,945 Rhea reaction nodes; 1,084 protein nodes |
| Rhea sample | `artifacts/rhea_sample.json` | 10 reaction records; 7 with mapped enzymes in the sample |
| Current sequence manifest | `artifacts/v3_sequence_manifest_current702_repaired_20260525.json` | 702 current labels; 702 sequence-covered labels; 760 current702 FASTA records |
| Current geometry features | `artifacts/v3_geometry_features_1025.json` | 1,002 entries; 963 with pairwise geometry; 998 with pocket context |
| AMR enzyme POC | `artifacts/v3_amr_enzyme_only_poc_scope_and_queue_20260528.json` | 18 review-only AMR enzyme mechanism classes |
| M-CSA x CARD scout | `artifacts/v3_mcsa_card_enzyme_crossmap_scout_20260528.json` | 9 candidate crossmap records; 8 current702 members |
| Source registry | `data/registries/source_registry.json` | UniProt, Rhea, BRENDA, CAZy, PDB, AlphaFold DB registered |

Not locally available as bulk source mirrors:

- Full UniProtKB/Swiss-Prot EC/Rhea source index
- BRENDA-like EC/substrate/product mapping table
- CARD sequence/model data
- AMRFinderPlus local database
- CAZy family/activity table

The repo does reference a ProtT5 Swiss-Prot H5 track in prior result-card artifacts, but the actual sidecar paths are outside this worktree and should not be counted as locally available bulk weak-label data.

## Bronze Schema

A bronze weak-label row should include:

- Stable label id from source, release, source record id, entity id, and normalized target.
- Source and source release/digest.
- Source record id and entity id.
- Evidence code or curation level, such as UniProt reviewed/evidence codes, Rhea reaction record, CARD/AMRFinder hierarchy, BRENDA literature/kinetic context, or CAZy curated family.
- EC/Rhea/reaction mapping with direct-vs-inferred flags.
- Structure availability: PDB, AlphaFold, ligand/cofactor/metal context, residue mapping, and quality caveats.
- Sequence availability: accession, reviewed status, local sequence presence, length, isoform policy, cluster ids.
- Family or fingerprint mapping confidence, counterevidence, and review-only flags.
- Leakage risk: M-CSA/gold/silver overlap, source-prose/name/EC leakage, sequence cluster overlap, structure cluster overlap.
- Label use: train only, retrieval-index only, review prior only, blocked, or unknown/abstain.
- OOS/unknown handling: positive, near negative, out of scope, unknown, ambiguous family, partial EC only, no sequence, no structure, or source conflict.

Minimum acceptance for bronze training/retrieval: exact source release or digest, stable entity id, known sequence/structure availability, direct-vs-inferred mapping status, split eligibility, and explicit exclusion of source text/name/EC/Rhea/family strings from predictive feature sets used for gold/silver claims.

## Scale Estimate

Only local committed artifact counts are numeric. Full-source counts are not claimed here.

| Source | Feasibility | Scale status |
|---|---|---|
| UniProtKB/Swiss-Prot | High if a reviewed release metadata index is safely cached | Not locally verifiable |
| Rhea | High for reaction/EC crosswalk labels | Partially verifiable locally through 1,945 graph Rhea nodes and 10-record sample |
| BRENDA | Medium if terms and EC/substrate metadata storage are resolved | Not locally verifiable |
| CARD | Medium-high for known public enzyme mechanism classes | Scout-only locally; beta-lactamase strongest |
| AMRFinderPlus | Medium for family hierarchy metadata | Prior scout saw small metadata candidates, but none cached locally |
| CAZy | Medium for carbohydrate-family labels after terms check | Not locally verifiable |

Current registry family counts are useful only as local evaluation-surface context, not as source-scale estimates: `metal_dependent_hydrolase` 83, `flavin_dehydrogenase_reductase` 48, `ser_his_acid_hydrolase` 42, `plp_dependent_enzyme` 31, `heme_peroxidase_oxidase` 20, `cobalamin_radical_rearrangement` 3, `flavin_monooxygenase` 2, and `radical_sam_enzyme` 1.

## Train/Eval Separation

Gold/silver evaluation:

- Keep M-CSA expert/curated mechanism labels and frozen external expert panels as evaluation surfaces.
- Do not select silver/gold rows using the same weak source labels being evaluated.
- Preserve source-free geometry, duplicate screens, UniRef/current-reference checks, and explicit human review for external evaluation panels.

Bronze training/retrieval:

- Use source labels only for train, retrieval, review prioritization, or stratification.
- Exclude gold/silver entities and their close sequence/structure/family neighbors from bronze training or retrieval indexes used during evaluation.
- Use UniRef-like cluster separation when available; otherwise mark the split qualitative.
- Run source-label ablations before claiming generalization.

Feature exclusions for gold/silver claims:

- Source prose, protein names, EC numbers, Rhea ids, reaction text, CARD family names, AMRFinder class/subclass names, BRENDA text, CAZy family names, curated mechanism prose, target labels, and label ids.

Allowed predictive features for gold/silver claims:

- Sequence-derived features without source-label/name leakage.
- Structure-derived coordinates and geometry.
- Coordinate-derived ligand/cofactor/metal context under preregistered rules.
- Learned embeddings only after split leakage checks and source-label ablations.

Unknown source rows remain `unknown_abstain`, not negatives. Partial EC, broad family, and ambiguous hierarchy rows stay review-prior only unless a direct mechanism mapping exists.

## Next-Run Queue

1. `artifacts/v3_bulk_weak_label_source_access_manifest_20260529.json`
   - Report exact source versions, licenses/terms, file sizes, expected disk use, and metadata-only retrieval plans.
   - No-go: free disk below 10 GiB, undocumented license acceptance, full database mirror requirement, or any registry/label/scoring edit.

2. `artifacts/v3_bulk_weak_label_metadata_index_probe_20260529.json`
   - Build or locate small metadata-only indexes for UniProt/Swiss-Prot, Rhea, AMRFinderPlus hierarchy/catalog metadata, CARD/ARO ontology metadata, CAZy family/activity data if permitted, and BRENDA EC/substrate/product data if permitted.
   - No-go: source terms prohibit storage, release/digest cannot be recorded, or projected files violate disk guardrail.

3. `artifacts/v3_bulk_weak_label_dedup_and_leakage_audit_20260529.json`
   - Define dedup keys and leakage flags across M-CSA, external panels, accessions, Rhea/EC mappings, source families, sequence clusters, and structure clusters.
   - No-go: gold/silver rows cannot be excluded, cluster overlap cannot be measured or conservatively approximated, or dedup requires production import changes.

4. `artifacts/v3_bulk_weak_label_bronze_schema_fixture_20260529.json`
   - Emit a tiny fixture proving the schema, validation rules, OOS/unknown handling, and no-leakage feature manifest without importing labels.
   - No-go: fixture could be mistaken for production labels or requires editing registries/model outputs.

Stop after these planning/fixture artifacts unless disk is back above the 10 GiB guardrail and a reviewed source-access manifest authorizes small metadata ingestion.
