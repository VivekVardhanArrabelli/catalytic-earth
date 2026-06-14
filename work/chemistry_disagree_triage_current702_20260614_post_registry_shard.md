# Chemistry-Disagree Triage — post registry sharding

Run source: `artifacts/v3_mechanism_representation_loop_current702_20260614_post_registry_shard.json`

Non-destructive review artifact derived from the leakage-safe representation-loop confusion matrix and promotion review queue samples. No registry was written and no label was demoted.

## Counts

- Seed labels triaged: 5638.
- Promotion-preview `review_chemistry_disagrees`: 1344.
- Representation-loop review outliers: 1382.
- Leave-one-out self-consistency: 0.7549.
- Families below 0.70 self-consistency: 9.

## Top confusion pairs

| assigned fingerprint | nearest fingerprint | rows | assigned self-consistency | assigned fraction | sample entries |
| --- | --- | ---: | ---: | ---: | --- |
| metal_dependent_hydrolase | zinc_lyase_hydratase | 157 | 0.0 | 0.6978 | uniprot:O75844, uniprot:P0C1T0, uniprot:P24155, uniprot:Q21432, uniprot:Q93243 |
| metallopeptidase | zinc_lyase_hydratase | 110 | 0.2067 | 0.7333 | not in preview sample |
| pfkb_ribokinase_family | pfka_phosphofructokinase | 100 | 0.0 | 0.7812 | not in preview sample |
| ghmp_small_molecule_kinase | pfka_phosphofructokinase | 88 | 0.0 | 0.88 | not in preview sample |
| metal_racemase_epimerase_non_plp | cofactor_independent_isomerase | 88 | 0.3267 | 0.5867 | not in preview sample |
| molybdopterin_oxidoreductase | cobalamin_radical_rearrangement | 86 | 0.508 | 0.344 | not in preview sample |
| metallophosphoesterase_nuclease | manganese_iron_superoxide_dismutase | 64 | 0.38 | 0.4267 | not in preview sample |
| glycoside_hydrolase | ser_his_acid_hydrolase | 55 | 0.52 | 0.3667 | not in preview sample |
| metal_dependent_hydrolase | metallo_amidohydrolase_deaminase | 46 | 0.0 | 0.2044 | not in preview sample |
| thiamine_diphosphate_enzyme | metallophosphoesterase_nuclease | 31 | 0.7867 | 0.2067 | not in preview sample |
| glycosyltransferase | class_ii_metal_aldolase | 24 | 0.664 | 0.096 | not in preview sample |
| flavin_dehydrogenase_reductase | flavin_monooxygenase | 20 | 0.901 | 0.099 | not in preview sample |
| molybdopterin_oxidoreductase | flavin_dehydrogenase_reductase | 18 | 0.508 | 0.072 | not in preview sample |
| glycosyltransferase | terpene_cyclase_synthase | 17 | 0.664 | 0.068 | not in preview sample |
| metallophosphoesterase_nuclease | atp_amide_ligase | 16 | 0.38 | 0.1067 | not in preview sample |
| pfkb_ribokinase_family | nucleoside_diphosphate_kinase | 15 | 0.0 | 0.1172 | not in preview sample |
| glycosyltransferase | metal_dependent_hydrolase | 15 | 0.664 | 0.06 | not in preview sample |
| cofactor_independent_isomerase | ser_his_acid_hydrolase | 14 | 0.7933 | 0.0933 | not in preview sample |
| glycosyltransferase | manganese_iron_superoxide_dismutase | 13 | 0.664 | 0.052 | not in preview sample |
| ghmp_small_molecule_kinase | askha_sugar_acetate_kinase | 12 | 0.0 | 0.12 | not in preview sample |

## Low self-consistency families

| fingerprint | self-consistency | seed rows | top off-target nearest |
| --- | ---: | ---: | --- |
| ghmp_small_molecule_kinase | 0.0 | 100 | pfka_phosphofructokinase:88, askha_sugar_acetate_kinase:12 |
| metal_dependent_hydrolase | 0.0 | 225 | zinc_lyase_hydratase:157, metallo_amidohydrolase_deaminase:46, metallopeptidase:9, manganese_iron_superoxide_dismutase:6, metallophosphoesterase_nuclease:3 |
| pfkb_ribokinase_family | 0.0 | 128 | pfka_phosphofructokinase:100, nucleoside_diphosphate_kinase:15, askha_sugar_acetate_kinase:10, non_heme_iron_2og_dioxygenase:3 |
| metallopeptidase | 0.2067 | 150 | zinc_lyase_hydratase:110, metallophosphoesterase_nuclease:6, metal_dependent_hydrolase:2, manganese_iron_superoxide_dismutase:1 |
| metal_racemase_epimerase_non_plp | 0.3267 | 150 | cofactor_independent_isomerase:88, cobalamin_radical_rearrangement:4, manganese_iron_superoxide_dismutase:4, atp_amide_ligase:3, molybdopterin_oxidoreductase:1 |
| metallophosphoesterase_nuclease | 0.38 | 150 | manganese_iron_superoxide_dismutase:64, atp_amide_ligase:16, zinc_lyase_hydratase:6, glycoside_hydrolase:3, class_ii_metal_aldolase:2 |
| molybdopterin_oxidoreductase | 0.508 | 250 | cobalamin_radical_rearrangement:86, flavin_dehydrogenase_reductase:18, ser_his_acid_hydrolase:7, nad_p_dehydrogenase:5, class_ii_metal_aldolase:4 |
| glycoside_hydrolase | 0.52 | 150 | ser_his_acid_hydrolase:55, class_ii_metal_aldolase:6, manganese_iron_superoxide_dismutase:5, zinc_lyase_hydratase:4, metallophosphoesterase_nuclease:2 |
| glycosyltransferase | 0.664 | 250 | class_ii_metal_aldolase:24, terpene_cyclase_synthase:17, metal_dependent_hydrolase:15, manganese_iron_superoxide_dismutase:13, ser_his_acid_hydrolase:6 |

## Guardrails

- EC, names, UniProt prose, target lanes, labels, and the frozen benchmark were not used as representation features.
- This ranks review work only; it does not mutate tiers/status and does not treat EC as corroboration.
- Recommended next action: row-level source review for top pairs before any demotion; add leakage-safe chemistry axes only for repeated representation gaps.
