# FMO M-CSA Candidate Scout 20260527

Review-only scout over local M-CSA/current702 artifacts. No label imports, registry edits, ontology edits, threshold changes, or model training were performed.

## Bottom line

- Clean local FMO candidates beyond current `m_csa:131`/`m_csa:132`: `m_csa:551` phenol 2-monooxygenase and `m_csa:973` DszC protein.
- No additional clean named-target-family rows were found beyond the prior FMO closure.
- If `m_csa:551` and `m_csa:973` are expert-accepted later, local clean support rises from 2 to 4; two more clean rows are still needed before n>=6 promotion reconsideration.

## Named Target Search

| Target | Local hits | Decision | Next action |
| --- | --- | --- | --- |
| cyclohexanone_monooxygenase_or_classic_BVMO | none | blocked_needs_source | Source a reviewed/PDB-backed BVMO row outside current local M-CSA if available, then run source-free geometry and duplicate/leakage checks. |
| 4_hydroxyacetophenone_monooxygenase_HAPMO | none | blocked_needs_source | Source HAPMO externally/local if a reviewed structure-backed row exists; no current local M-CSA hit. |
| IucD_class_lysine_N6_hydroxylase | m_csa:781 | blocked_wrong_chemistry | Do not count local lysine N6 string hit; source true FAD-dependent N-hydroxylase/IucD row. |
| tryptophan_monooxygenase | m_csa:977 | blocked_wrong_chemistry | Preserve halogenase as negative; source true tryptophan monooxygenase separately. |
| salicylate_1_monooxygenase_or_aromatic_hydroxylase | none | blocked_needs_source | Source salicylate hydroxylase if a clean flavin C4a-peroxy reviewed row is available. |
| FMO1_FMO3_FMO5_or_dimethylaniline_monooxygenase | none | blocked_needs_source | Source mammalian FMO/dimethylaniline monooxygenase rows with explicit FAD/NADPH oxygenation and structure support. |
| local_non_target_clean_FMO | m_csa:551, m_csa:973 | clean_candidates_found | Expert-review both as future FMO support and pair with hard negatives before promotion reconsideration. |

## Candidate Rows

| Entry | Enzyme | EC | Current status | Type | Disposition | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `m_csa:551` | phenol 2-monooxygenase | 1.14.13.7 | current702:seed_fingerprint:flavin_dehydrogenase_reductase; confidence=high; review_status=automation_curated; tier=bronze | clean_FAD_aromatic_hydroxylase | clean_candidate | Expert review for future FMO acquisition; run duplicate/leakage and hard-negative separation before any primary promotion. |
| `m_csa:973` | DszC protein | 1.14.14.21 | current702:seed_fingerprint:flavin_dehydrogenase_reductase; confidence=high; review_status=automation_curated; tier=bronze | clean_FMN_sulfur_monooxygenase | clean_candidate | Expert review for future FMO acquisition; check duplicate/family leakage and pair with hard-negative flavin reductases. |
| `m_csa:141` | 4-cresol dehydrogenase (hydroxylating) | 1.17.9.1 | current702:seed_fingerprint:flavin_dehydrogenase_reductase; confidence=medium; review_status=automation_curated; tier=bronze | hydroxylating_dehydrogenase_boundary | hard_negative_control | Use as a hard-negative separator against clean C4a-peroxy FMO rows. |
| `m_csa:128` | Photinus-luciferin 4-monooxygenase (ATP-hydrolysing) | 1.13.12.7 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | ATP_luciferin_monooxygenase_nonflavin | hard_negative_control | Retain as name-only monooxygenase negative; do not count for FMO support. |
| `m_csa:133` | camphor 5-monooxygenase | 1.14.15.1 | current702:seed_fingerprint:heme_peroxidase_oxidase; confidence=medium; review_status=automation_curated; tier=bronze | heme_P450_monooxygenase_negative | hard_negative_control | Retain as heme monooxygenase hard negative. |
| `m_csa:134` | tyrosine 3-monooxygenase | 1.14.16.2 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | biopterin_nonheme_iron_monooxygenase_negative | hard_negative_control | Retain as nonflavin hydroxylase negative. |
| `m_csa:135` | peptidylglycine monooxygenase | 1.14.17.3 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | copper_monooxygenase_negative | hard_negative_control | Retain as copper monooxygenase hard negative. |
| `m_csa:600` | methane monooxygenase (soluble) | 1.14.13.25 | not_present_in_current702_registry | diiron_methane_monooxygenase_negative | hard_negative_control | Retain as metal monooxygenase hard negative. |
| `m_csa:768` | Renilla-luciferin 2-monooxygenase | 1.13.12.5 | not_present_in_current702_registry | luciferin_monooxygenase_nonflavin_negative | hard_negative_control | Retain as name-only monooxygenase negative. |
| `m_csa:977` | tryptophan 7-halogenase | 1.14.19.9 | not_present_in_current702_registry | flavin_halogenase_tryptophan_boundary | blocked_wrong_chemistry | Preserve as flavin-halogenase negative; source true tryptophan monooxygenase separately if needed. |
| `m_csa:781` | UDP-N-acetylmuramoylpentapeptide-lysine N6-alanyltransferase | 2.3.2.10 | not_present_in_current702_registry | IucD_lysine_N6_name_false_positive | blocked_wrong_chemistry | Do not count; source a true IucD-class FAD-dependent lysine N6-hydroxylase row externally/local if available. |
| `m_csa:130` | naphthalene 1,2-dioxygenase | 1.14.12.12 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | FAD_reductase_to_Rieske_nonheme_iron_dioxygenase_boundary | hard_negative_control | Retain as flavin reductase/dioxygenase-system negative. |
| `m_csa:930` | phthalate dioxygenase system | 1.14.12.7 | not_present_in_current702_registry | FMN_reductase_to_phthalate_dioxygenase_boundary | needs_structure_check | Keep out of clean FMO support; use only after structural/source review as a negative-control system. |
| `m_csa:699` | cytochrome P450 (BM-3) | 1.14.14.1 | current702:seed_fingerprint:heme_peroxidase_oxidase; confidence=high; review_status=automation_curated; tier=bronze | dual_flavin_P450_heme_boundary | hard_negative_control | Retain as dual-flavin/heme oxygenase separator. |
| `m_csa:935` | nitric-oxide synthase | 1.14.13.39 | current702:seed_fingerprint:heme_peroxidase_oxidase; confidence=high; review_status=automation_curated; tier=bronze | dual_flavin_NOS_heme_boundary | hard_negative_control | Retain as NOS flavin-domain/heme oxygenase separator. |
| `m_csa:109` | dihydroorotate oxidase (class II) | 1.3.5.2 | current702:seed_fingerprint:flavin_dehydrogenase_reductase; confidence=medium; review_status=automation_curated; tier=bronze | FMN_dehydrogenase_oxidase_boundary | hard_negative_control | Use as flavin hydride-transfer negative against FMO rows. |
| `m_csa:809` | polyamine oxidase (propane-1,3-diamine-forming) | 1.5.3.14 | not_present_in_current702_registry | FAD_C4a_adduct_oxidase_boundary | hard_negative_control | Retain as C4a-adduct non-monooxygenase negative. |
| `m_csa:978` | D-arginine dehydrogenase | 1.4.99.6 | current702:seed_fingerprint:flavin_dehydrogenase_reductase; confidence=high; review_status=automation_curated; tier=bronze | flavin_dehydrogenase_C4a_proposal_boundary | hard_negative_control | Retain as flavin dehydrogenase hard negative. |
| `m_csa:129` | taurine dioxygenase | 1.14.11.17 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | nonheme_iron_alphaKG_dioxygenase_negative | hard_negative_control | Retain as nonheme iron oxygenase negative. |
| `m_csa:34` | catechol 2,3-dioxygenase | 1.13.11.2 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | nonheme_iron_dioxygenase_negative | hard_negative_control | Retain as nonheme iron dioxygenase negative. |
| `m_csa:37` | prostaglandin-endoperoxide synthase | 1.14.99.1 | current702:seed_fingerprint:heme_peroxidase_oxidase; confidence=medium; review_status=automation_curated; tier=bronze | heme_cyclooxygenase_peroxidase_negative | hard_negative_control | Retain as heme oxygenase/peroxidase negative. |
| `m_csa:547` | homogentisate 1,2-dioxygenase | 1.13.11.5 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | iron_dioxygenase_negative | hard_negative_control | Retain as iron dioxygenase negative. |
| `m_csa:583` | linoleate 9S-lipoxygenase | 1.13.11.58 | current702:out_of_scope:none; confidence=medium; review_status=automation_curated; tier=bronze | iron_lipoxygenase_negative | hard_negative_control | Retain as lipoxygenase negative. |
| `m_csa:672` | protocatechuate 4,5-dioxygenase | 1.13.11.8 | not_present_in_current702_registry | extradiol_nonheme_iron_dioxygenase_negative | hard_negative_control | Retain as nonheme iron dioxygenase negative. |
| `m_csa:743` | quercetin 2,3-dioxygenase | 1.13.11.24 | not_present_in_current702_registry | copper_dioxygenase_negative | hard_negative_control | Retain as copper dioxygenase negative. |
| `m_csa:795` | heme oxygenase (biliverdin-producing) | 1.14.14.18 | current702:seed_fingerprint:heme_peroxidase_oxidase; confidence=high; review_status=automation_curated; tier=bronze | heme_oxygenase_negative | hard_negative_control | Retain as heme oxygenase negative. |
| `m_csa:936` | protocatechuate 3,4-dioxygenase | 1.13.11.3 | not_present_in_current702_registry | intradiol_iron_dioxygenase_negative | hard_negative_control | Retain as iron dioxygenase negative. |

## Clean Candidate Evidence

### m_csa:551 phenol 2-monooxygenase

- Flavin evidence: M-CSA mechanism names FAD, NADPH, molecular oxygen, and reduced flavin; current label rationale reports ligand-supported cofactor context.
- Oxygen/C4a evidence: Reduced FAD reacts with oxygen to form C4a-hydroperoxyflavin/C4a-peroxoflavin before product release.
- Substrate oxygenation: Phenol or derivatives are hydroxylated at the ortho position.
- Confounds: Currently labeled flavin_dehydrogenase_reductase; mechanism is compared with p-hydroxybenzoate hydroxylase but described as operating differently.

### m_csa:973 DszC protein

- Flavin evidence: M-CSA mechanism uses FMNH2/FMNH2-derived chemistry and current label rationale reports ligand-supported cofactor context.
- Oxygen/C4a evidence: FMNH2 transfers reducing equivalents to dioxygen to form a C4a-hydroperoxyflavin/C4aOOH intermediate.
- Substrate oxygenation: Dibenzothiophene sulfur attacks the distal oxygen of C4aOOH to form DBT sulfoxide.
- Confounds: Currently labeled flavin_dehydrogenase_reductase; DszC sulfur oxygenation should stay secondary/future until expert review and support gates are complete.

## Negative Signal To Preserve

- `m_csa:141` is the closest flavin dehydrogenase boundary: FAD and hydroxylating language, but hydride transfer to FAD N5 and water-derived oxygen.
- `m_csa:977` is a targeted tryptophan/FAD/O2 confound: halogenation to 7-chlorotryptophan, not substrate oxygenation.
- `m_csa:699` and `m_csa:935` contain flavin reductase domains but oxygenate at heme/BH4 oxygenase domains.
- Nonflavin monooxygenases/dioxygenases in the table should be retained as hard negatives for future FMO separation checks.

## Source Artifacts

- `artifacts/mcsa_sample.json` sha256 `dcc40d0129c1327a47453979f754acaaeacd4cc461688d2d507db7d6f9e1c87d`
- `artifacts/v1_graph_1025.json` sha256 `efaf0e97e740373f647fdb8ace87f4d693eb40356e929ac1e5de1f25a0d56a25`
- `artifacts/v3_flavin_monooxygenase_acquisition_closure_702_20260527.json` sha256 `863a44bc76f3f2f58db4b4b3289a108edef7bb84cecc9db721d892548cff16be`
- `artifacts/v3_flavin_monooxygenase_acquisition_packet_702_20260527.json` sha256 `9d2059f7a7c8d8f4ca939258cae366b4376c41c4e447fec16220674d0feb6500`
- `artifacts/v3_imported_labels_batch_925.json` sha256 `aa63de991a754be4a292988e41163d34a415b72b891ee7447a1b5ae457afa0e4`
- `artifacts/v3_mcsa_ai_visual_decisions_298_reaudited_bulk_r_safe_20260523.json` sha256 `82b264b9bb5a2270f47742591ecdd320e629e267596d6720f527f393cf8dcfb5`
- `artifacts/v3_mechanism_fingerprint_v2_sublabel_audit_702_20260525.json` sha256 `afc80e7fa4f6f4db5521388803cae8fda24ec7cca9fbafa723cf3c1234ce951b`
- `artifacts/v3_packet3_v2_sublabel_decision_closure_702_20260527.json` sha256 `c0c6c5d8bb9b3898093f993e096b5d14a9982e95ffe24a8d71cf3df8e807ec0d`
- `data/registries/curated_mechanism_labels.json` sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`

## Verification Targets

- JSON parse: `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json`
- CLI validation: `PYTHONPATH=src python -m catalytic_earth.cli validate`
- Whitespace: `git diff --check`
