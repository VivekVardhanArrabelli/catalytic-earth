# M-CSA Mechanism Confusion Backlog Map (1025 slice)

Created: 2026-05-23T13:02:15Z

This artifact converts Vivek-reviewed current-target rejections into a scientific backlog. It does not promote labels or edit registries.

## Review State

- accepted: 22
- needs_more_evidence: 66
- rejected: 210
- reviewed current-target rejections used for backlog mapping: 210
- countable imports: 0

## Main Backlog Signals

| Routed family/lane | Count | Failure mode | Next action |
|---|---:|---|---|
| future unrepresented mechanism family | 56 | ontology_gap | cluster this bucket by EC, cofactor, and residue roles; choose next fingerprint family by burden and confusion frequency |
| oxidoreductase/redox family | 34 | ontology_gap_and_confusion | expand redox ontology beyond current flavin/heme seeds; prioritize NAD/PQQ/molybdenum/disulfide subclasses |
| transferase/thioester-transfer family | 31 | ontology_gap | add transferase/thioester ontology lanes before broad scaling |
| ATP-dependent phosphoryl-transfer/kinase family | 25 | heuristic_confusion | learned representation + explicit ATP-phosphoryl-transfer family ontology; add counterevidence separating water-mediated hydrolysis from acceptor phosphoryl transfer |
| lyase/dehydratase or Schiff-base lyase family | 19 | ontology_gap_and_confusion | add lyase/dehydratase/Schiff-base fingerprints and keep current rejections as hard negatives |
| glycoside hydrolase family | 14 | ontology_gap | add glycoside hydrolase fingerprints and avoid treating all hydrolases as current metal/Ser-His targets |
| isomerase/mutase family | 12 | ontology_gap | add isomerase/mutase fingerprint families and use these rows as negative controls for hydrolase/redox seeds |
| ePK/ePK-like ATP-phosphoryl-transfer family | 4 | heuristic_confusion | defer to ePK candidate-level evidence system; require kinase-specific fingerprint and hard countercontrols before positive labels |
| ASKHA sugar/acetate kinase ATP-phosphoryl-transfer family | 3 | ontology_gap_and_confusion | add ASKHA fingerprint/counterevidence lane |
| cysteine protease Cys-His-Asp hydrolase family | 3 | ontology_gap_and_policy_boundary | create separate cysteine protease fingerprint or explicit policy boundary; do not bulk-map to Ser-His hydrolase |
| heme/peroxide chemistry family | 3 | review_boundary | route to expert review or heme-family expansion; require heme ligand and peroxide/O2 activation evidence |
| GHMP or related small-molecule kinase ATP-phosphoryl-transfer family | 2 | ontology_gap_and_confusion | add GHMP kinase fingerprint/counterevidence lane |
| PLP-dependent enzyme family | 2 | review_boundary | review against PLP fingerprint criteria before promotion |
| PfkB/ribokinase ATP-phosphoryl-transfer family | 2 | ontology_gap_and_confusion | add PfkB/ribokinase fingerprint after family evidence packet; use as high-priority ATP sibling family |

## Largest Current-Target Confusions

| Current target | Routed family/lane | Count | Why geometry was fooled | Representative IDs |
|---|---|---:|---|---|
| metal_dependent_hydrolase | future unrepresented mechanism family | 44 | M-CSA contains many real mechanism families outside the current seed space; broad geometry retrieval surfaces them as near misses. | m_csa:995, m_csa:806, m_csa:724, m_csa:559, m_csa:828 |
| metal_dependent_hydrolase | transferase/thioester-transfer family | 22 | Transferase and thioester chemistry is common in M-CSA but mostly outside the current 8-fingerprint seed space. | m_csa:840, m_csa:783, m_csa:700, m_csa:999, m_csa:873 |
| metal_dependent_hydrolase | ATP-dependent phosphoryl-transfer/kinase family | 20 | ATP/Mg phosphate-transfer sites resemble metal hydrolase pockets because both use phosphoryl groups, divalent metals, charged residues, and compact catalytic geometry. | m_csa:788, m_csa:534, m_csa:653, m_csa:779, m_csa:799 |
| metal_dependent_hydrolase | oxidoreductase/redox family | 16 | Redox active-site residue/cofactor pockets can mimic heme/flavin/metal geometry without matching the selected redox seed. | m_csa:980, m_csa:925, m_csa:938, m_csa:673, m_csa:725 |
| heme_peroxidase_oxidase | oxidoreductase/redox family | 10 | Redox active-site residue/cofactor pockets can mimic heme/flavin/metal geometry without matching the selected redox seed. | m_csa:918, m_csa:792, m_csa:974, m_csa:891, m_csa:711 |
| metal_dependent_hydrolase | lyase/dehydratase or Schiff-base lyase family | 9 | Lyase/dehydratase active sites often use acid/base residue geometry that can resemble hydrolase or heme-redox patterns, but bond changes differ. | m_csa:963, m_csa:962, m_csa:961, m_csa:960, m_csa:846 |
| heme_peroxidase_oxidase | lyase/dehydratase or Schiff-base lyase family | 8 | Lyase/dehydratase active sites often use acid/base residue geometry that can resemble hydrolase or heme-redox patterns, but bond changes differ. | m_csa:553, m_csa:947, m_csa:972, m_csa:910, m_csa:687 |
| metal_dependent_hydrolase | glycoside hydrolase family | 7 | Glycoside hydrolases are hydrolytic but not represented by the current Ser/His or metal hydrolase seeds; many use acid/base carboxylates rather than those signatures. | m_csa:510, m_csa:888, m_csa:1002, m_csa:913, m_csa:568 |
| metal_dependent_hydrolase | isomerase/mutase family | 5 | Isomerase/mutase chemistry is underrepresented; local acid/base geometry can resemble hydrolase/redox contexts while reaction topology differs. | m_csa:943, m_csa:959, m_csa:890, m_csa:979, m_csa:738 |
| flavin_dehydrogenase_reductase | future unrepresented mechanism family | 4 | M-CSA contains many real mechanism families outside the current seed space; broad geometry retrieval surfaces them as near misses. | m_csa:767, m_csa:748, m_csa:719, m_csa:819 |
| flavin_dehydrogenase_reductase | oxidoreductase/redox family | 4 | Redox active-site residue/cofactor pockets can mimic heme/flavin/metal geometry without matching the selected redox seed. | m_csa:804, m_csa:775, m_csa:752, m_csa:868 |
| flavin_dehydrogenase_reductase | isomerase/mutase family | 3 | Isomerase/mutase chemistry is underrepresented; local acid/base geometry can resemble hydrolase/redox contexts while reaction topology differs. | m_csa:680, m_csa:983, m_csa:874 |
| flavin_dehydrogenase_reductase | transferase/thioester-transfer family | 3 | Transferase and thioester chemistry is common in M-CSA but mostly outside the current 8-fingerprint seed space. | m_csa:781, m_csa:993, m_csa:872 |
| heme_peroxidase_oxidase | future unrepresented mechanism family | 3 | M-CSA contains many real mechanism families outside the current seed space; broad geometry retrieval surfaces them as near misses. | m_csa:676, m_csa:787, m_csa:764 |
| heme_peroxidase_oxidase | glycoside hydrolase family | 3 | Glycoside hydrolases are hydrolytic but not represented by the current Ser/His or metal hydrolase seeds; many use acid/base carboxylates rather than those signatures. | m_csa:834, m_csa:659, m_csa:807 |
| metal_dependent_hydrolase | ASKHA sugar/acetate kinase ATP-phosphoryl-transfer family | 3 | ASKHA kinase folds use ATP/Mg phosphoryl transfer and can look like metal-assisted hydrolysis at residue-geometry level. | m_csa:643, m_csa:696, m_csa:592 |
| metal_dependent_hydrolase | cysteine protease Cys-His-Asp hydrolase family | 3 | Cysteine proteases are genuine hydrolases but not the current Ser-nucleophile hydrolase seed and not metal hydrolases. | m_csa:761, m_csa:953, m_csa:682 |
| metal_dependent_hydrolase | ePK/ePK-like ATP-phosphoryl-transfer family | 3 | Protein kinase ATP/Mg active sites can satisfy metal/hydrolase-like geometric cues even though the chemistry is acceptor Ser/Thr/Tyr phosphoryl transfer. | m_csa:756, m_csa:760, m_csa:662 |
| ser_his_acid_hydrolase | transferase/thioester-transfer family | 3 | Transferase and thioester chemistry is common in M-CSA but mostly outside the current 8-fingerprint seed space. | m_csa:824, m_csa:602, m_csa:985 |
| flavin_dehydrogenase_reductase | glycoside hydrolase family | 2 | Glycoside hydrolases are hydrolytic but not represented by the current Ser/His or metal hydrolase seeds; many use acid/base carboxylates rather than those signatures. | m_csa:655, m_csa:825 |

## Interpretation

- ATP/Mg phosphoryl-transfer families are systematic hard negatives for the current metal-dependent hydrolase heuristic. These should drive learned-representation controls and ATP-family ontology expansion.
- The broad future-unrepresented bucket is an ontology backlog, not just cleanup. It should be clustered by EC/cofactor/residue role before adding new labels.
- Glycoside hydrolases and cysteine proteases are hydrolase-family boundary problems: they are real hydrolases, but not necessarily the current metal-dependent or Ser-nucleophile seed fingerprints.
- Accepted current-target rows should still be reviewed manually before any promotion; this map is about clearing current-target false positives and choosing next fingerprint families.
