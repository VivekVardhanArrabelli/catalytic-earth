# AMR Enzyme-Only POC Scope And Queue - 2026-05-28

Run time: 2026-05-28T06:50:29Z

Scope: safety-scoped detection/classification benchmark design only. The target output is resistance mechanism class for known public AMR enzymes, not clinical resistant/susceptible phenotype. This pass did not design, optimize, mutate, engineer, synthesize, or improve antimicrobial resistance. No wet-lab protocols, variant suggestions, phenotype-enhancement guidance, labels, registries, ontology files, production scoring, imports, or thresholds were changed.

Primary artifact: `artifacts/v3_amr_enzyme_only_poc_scope_and_queue_20260528.json`

## Bottom Line

The best POC entry point is an enzyme-only AMR mechanism atlas that starts with antibiotic inactivation enzymes. The clean first benchmark is beta-lactamase mechanism classification:

- Ambler A serine beta-lactamases
- Ambler C serine beta-lactamases
- Ambler D serine beta-lactamases
- Ambler B metallo-beta-lactamases

This panel can test whether homology, sequence nearest neighbors, Foldseek, active-site geometry, metal context, and learned representations separate known public enzyme mechanism classes without making any clinical phenotype claim.

## Source Access

Public source checks were limited and non-bulk:

- CARD/ARO browse pages and the `arpcard/aro` mirror were accessible. CARD exposes relevant ARO mechanism and gene-family tags, including antibiotic inactivation enzyme, beta-lactamase subclasses, aminoglycoside modifying enzymes, macrolide inactivation enzymes, and tetracycline inactivation enzymes.
- AMRFinderPlus latest FTP metadata was accessible. The latest directory observed was dated 2026-05-19. Small metadata files such as `ReferenceGeneCatalog.txt`, `ReferenceGeneHierarchy.txt`, `fam.tsv`, and `version.txt` are suitable for the next source manifest. Large files such as `AMR.LIB` were not downloaded.
- ResFinder documentation was accessible, but the current install flow uses separate application and database packages and warns against cloning the historical repository because of size. Treat ResFinder as optional until a next-run manifest decides whether the database is necessary.
- MEGARes documentation was accessible and useful as an optional mechanism/class crosswalk, but it is optimized for high-throughput population/metagenomic profiling and includes biocide and metal determinants. Do not use it before enzyme-only filters are explicit.
- RCSB PDB CARD browser documentation was accessible and provides a path for structure availability scouting of PDB sequences annotated with CARD ARO terms.

## Proposed Vocabulary

`amr_enzyme_fingerprint_v0` should be review-only and mechanism-class focused. It should classify known public enzyme families while explicitly separating positives, near negatives, and OOS controls.

High-priority positives:

- `amr_serine_beta_lactamase_ambler_a`
- `amr_serine_beta_lactamase_ambler_c`
- `amr_serine_beta_lactamase_ambler_d`
- `amr_metallo_beta_lactamase_ambler_b`
- `amr_aminoglycoside_acetyltransferase`
- `amr_aminoglycoside_phosphotransferase`
- `amr_aminoglycoside_nucleotidyltransferase`
- `amr_chloramphenicol_acetyltransferase`
- `amr_macrolide_esterase`
- `amr_macrolide_phosphotransferase`
- `amr_tetracycline_destructase_flavin_monooxygenase`

Second-wave or structure-dependent positives:

- `amr_chloramphenicol_phosphotransferase`
- `amr_fosfomycin_inactivation_enzyme`
- `amr_rifampin_inactivation_enzyme`
- `amr_lincosamide_nucleotidyltransferase`
- `amr_streptogramin_acetyltransferase`
- `amr_streptothricin_acetyltransferase`

Deferred bucket:

- `amr_enzyme_target_modification_deferred`

This bucket is for enzyme-mediated target modification classes that may have active-site chemistry but should not be mixed into the first antibiotic-inactivation POC until substrate/target context is separately defined.

## Controls

Near negatives should test whether the benchmark is learning mechanism rather than a name:

- Same fold but non-AMR enzymes
- Same chemistry but different antibiotic class
- Same antibiotic class but different mechanism
- Public AMR families with ambiguous enzyme activity or missing active-site context

OOS/non-enzyme controls should be counted for abstention and scope discipline:

- Efflux pumps and efflux components
- Efflux regulators
- Porin loss or permeability mechanisms
- Target protection proteins without catalytic active sites
- Resistance-associated SNP-only records
- Clinical phenotype-only records
- AMR gene regulators
- Mobile element annotations without enzyme products

## Beta-Lactamase Panel

Panel ID: `amr_beta_lactamase_ambler_serine_vs_metallo_v0`

Target classes:

- Ambler A: public families such as TEM, SHV, CTX-M, KPC, GES, SME, and BlaC
- Ambler C: public families such as CMY/LAT/MOX, DHA, ACC, ACT/MIR, ADC, PDC, and FOX
- Ambler D: OXA-like public families
- Ambler B: public families such as NDM, VIM, IMP, SPM, GIM, SIM, GOB, and L1

These names are source-seed examples only. They are not variant suggestions and are not phenotype claims.

What the benchmark should test:

- CARD/AMRFinder homology: source-derived family and mechanism-class mapping for known public enzymes.
- Sequence nearest neighbor: whether simple sequence similarity already explains the task under family-level holdout.
- Foldseek: whether structural retrieval separates Ambler B metallo-beta-lactamase fold neighborhoods from Ambler A/C/D serine beta-lactamases, and where it over-calls PBPs, DD-peptidases, or non-AMR MBL-fold hydrolases.
- Active-site geometry: role-level serine beta-lactamase geometry versus metal-dependent beta-lactamase geometry, with abstention when residue, ligand, metal, chain, or assembly context is missing.
- Metal/cofactor context: Ambler B geometry claims require metal-context review; Ambler A/C/D should not be classified as metal-dependent because of incidental ions.
- Learned representations: compare sequence or structure embeddings only after source/panel artifacts exist, with family-level holdout and OOS abstention reporting.

No thresholds are proposed here. No outperforming claim is made.

## Baseline Comparison

CARD/RGI and AMRFinderPlus are the expected known-family reference baselines. They should be strong for close public homologs but are not geometry mechanism tests.

Sequence nearest neighbor is the simplest leakage detector. If it performs well under weak splits, that is not evidence of mechanism learning; use family-level holdout.

Foldseek can test fold-level separation and find near negatives, but fold similarity is not function proof.

Active-site geometry is the most mechanism-oriented baseline but depends on reliable coordinates, residue mapping, metal/cofactor state, and abstention rules.

Learned representations can be useful as orthogonal retrieval signals but must be audited for naming, phylogeny, and split leakage.

## Next-Run Queue

1. `artifacts/v3_amr_public_source_access_manifest_20260529.json`
   - Report: `work/amr_public_source_access_manifest_20260529.md`
   - Decide exact public source versions, license/click-through state, and download limits.

2. `artifacts/v3_amr_enzyme_public_db_class_index_20260529.json`
   - Report: `work/amr_enzyme_public_db_class_index_20260529.md`
   - Map CARD/AMRFinder family and hierarchy metadata into the review-only `amr_enzyme_fingerprint_v0` classes.

3. `artifacts/v3_amr_enzyme_structure_availability_probe_20260529.json`
   - Report: `work/amr_enzyme_structure_availability_probe_20260529.md`
   - Probe RCSB CARD/PDB and AlphaFold coverage by family; record holo/apo/metal/cofactor caveats without bulk coordinate materialization.

4. `artifacts/v3_amr_beta_lactamase_panel_v0_20260529.json`
   - Report: `work/amr_beta_lactamase_panel_v0_20260529.md`
   - Define the Ambler A/C/D/B panel, source seeds, split policy, leakage controls, near negatives, and OOS lanes.

5. `artifacts/v3_amr_homology_sequence_nn_baseline_contract_20260529.json`
   - Report: `work/amr_homology_sequence_nn_baseline_contract_20260529.md`
   - Define CARD/AMRFinder homology and sequence-nearest-neighbor baseline inputs and outputs.

6. `artifacts/v3_amr_beta_lactamase_foldseek_geometry_contract_20260529.json`
   - Report: `work/amr_beta_lactamase_foldseek_geometry_contract_20260529.md`
   - Define Foldseek and active-site geometry contracts. No production thresholds.

7. `artifacts/v3_amr_learned_representation_baseline_contract_20260529.json`
   - Report: `work/amr_learned_representation_baseline_contract_20260529.md`
   - Define learned-representation comparison only after source and panel artifacts exist.

Stop the next run if a step requires undocumented license acceptance, huge downloads without manifest justification, registry/label/scoring edits, threshold edits, or any wet-lab/variant/resistance-improvement guidance.
