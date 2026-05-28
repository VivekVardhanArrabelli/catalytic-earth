# M-CSA x CARD Enzyme Crossmap Scout 20260528

Read-only detection/classification benchmark design only. No antimicrobial resistance design, optimization, mutation, engineering, synthesis, wet-lab protocol, variant suggestion, phenotype-enhancement guidance, AMRFinderPlus baseline, label import, registry edit, ontology edit, scoring edit, or threshold edit was performed.

## Data Sources

Local artifacts used:

- `artifacts/v3_sequence_manifest_current702_repaired_20260525.json`
- `artifacts/v3_learned_retrieval_manifest_1025_current702_full_20260525.json`
- `artifacts/v1_graph_1025.json`
- `artifacts/v3_geometry_features_1025.json`
- `data/registries/curated_mechanism_labels.json` read only

Small public CARD metadata checks were used only to anchor AMR family names and scope: CARD overview, APH, ANT, CAT, FosA, and macrolide phosphotransferase ontology pages. No CARD downloads or AMR baseline runs were performed.

## Candidate Crossmap

| M-CSA | Current702 | UniProt | Selected PDB | Scout mechanism fingerprint | Public AMR class | Chemistry / cofactors | Role |
|---|---:|---|---|---|---|---|---|
| `m_csa:2` beta-lactamase Class A | yes | `P62593` | `1BTL` | serine_beta_lactam_acyl_enzyme_hydrolysis | class A beta-lactamase | Ser acyl-enzyme hydrolysis; no required metal | likely current702 positive |
| `m_csa:257` beta-lactamase Class C | yes | `P05364` | `1XX2` | serine_beta_lactam_acyl_enzyme_hydrolysis_class_c | class C beta-lactamase | Ser acyl-enzyme hydrolysis; no required metal | likely current702 positive |
| `m_csa:210` beta-lactamase Class D | yes | `P13661` | `1M6K` | serine_beta_lactam_acyl_enzyme_hydrolysis_class_d_carbamylated_lys | class D beta-lactamase | Ser acyl-enzyme hydrolysis with carboxylated Lys feature | likely current702 positive |
| `m_csa:15` beta-lactamase Class B1 | yes | `P25910` | `1ZNB` | current `metal_dependent_hydrolase`; scout zinc_metallo_beta_lactam_hydrolysis | class B metallo-beta-lactamase | Zn(II)-activated water/hydroxide hydrolysis | likely current702 positive |
| `m_csa:16` beta-lactamase Class B1 | yes | `P04190` | `1BC2` | current `metal_dependent_hydrolase`; scout zinc_metallo_beta_lactam_hydrolysis_monometal_context | class B metallo-beta-lactamase | Zn(II)-activated water/hydroxide hydrolysis | likely current702 positive |
| `m_csa:258` beta-lactamase Class B1 | yes | `P52700` | `1SML` | current `metal_dependent_hydrolase`; scout zinc_metallo_beta_lactam_hydrolysis_dinuclear_context | class B metallo-beta-lactamase | Zn(II)-activated water/hydroxide hydrolysis | likely current702 positive |
| `m_csa:640` kanamycin kinase | yes | `P0A3Y5` | `1L8T` | aminoglycoside_o_phosphoryl_transfer_atp_mg | aminoglycoside phosphotransferase APH-like | ATP/Mg-dependent phosphoryl transfer to aminoglycoside hydroxyl | likely current702 positive, underpowered family |
| `m_csa:647` kanamycin nucleotidyltransferase | yes | `P05057` | `1KNY` | aminoglycoside_o_nucleotidyl_transfer_nucleotide_mg | aminoglycoside nucleotidyltransferase ANT-like | nucleotide/Mg-dependent nucleotidyl transfer to aminoglycoside hydroxyl | likely current702 positive, underpowered family |
| `m_csa:934` chloramphenicol O-acetyltransferase | no | `P00484` | `3CLA` | acetyl_coa_antibiotic_o_acetyl_transfer | chloramphenicol acetyltransferase CAT | acetyl-CoA-dependent O-acetyl transfer | M-CSA scout-only; do not count for current702 |

All eight current702 likely positives have sequence coverage, selected PDB structures, and local active-site geometry evidence. Only three of the eight have current seed-fingerprint labels (`metal_dependent_hydrolase`); the other five are current `out_of_scope` rows and must remain scout-only unless a separate authorized review path changes labels later.

## Counts

| Mechanism class | Current702 likely positives | M-CSA scout-only positives |
|---|---:|---:|
| Serine beta-lactam acyl-enzyme hydrolysis | 3 | 0 |
| Zinc metallo-beta-lactam hydrolysis | 3 | 0 |
| Aminoglycoside O-phosphoryl transfer | 1 | 0 |
| Aminoglycoside O-nucleotidyl transfer | 1 | 0 |
| Chloramphenicol O-acetyl transfer | 0 | 1 |
| Aminoglycoside acetyltransferase | 0 | 0 |
| Tetracycline destructase | 0 | 0 |
| Macrolide esterase/phosphotransferase | 0 | 0 |
| Fosfomycin inactivation enzyme | 0 | 0 |

Near misses excluded from positive counts:

- `m_csa:303` beta-lactam synthase: beta-lactam biosynthesis-like chemistry, not antibiotic inactivation.
- `m_csa:369` UDP-N-acetylglucosamine enolpyruvyl transferase: fosfomycin-related target enzyme, not a fosfomycin-inactivation enzyme.
- `m_csa:466` fusarinine-C ornithinesterase: beta-lactamase-like similarity noted locally, but not beta-lactamase activity.

## Gate Decision

Gate: **do not proceed to a full enzyme-only AMR cross-domain transfer benchmark yet**.

The overlap is real but narrow. It supports a beta-lactamase-centric smoke panel and an AMR scout panel, because M-CSA/current702 contains six beta-lactamase examples with public sequence, structure, and active-site evidence. It does not support a broad CARD enzyme-mediated resistance benchmark: non-beta-lactamase current702 support is only two aminoglycoside-modifying rows, chloramphenicol acetyltransferase is outside current702, and aminoglycoside acetyltransferase, tetracycline destructase, macrolide inactivation, and fosfomycin inactivation families have no local current702 positives.

Proceed only after a separate, authorized review path can establish enough public enzyme entries with structures and active-site evidence across multiple non-beta-lactamase AMR families. Until then, keep AMR as a scout panel and do not run AMRFinderPlus baselines.
