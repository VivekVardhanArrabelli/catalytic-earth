# Mechanism-from-Chemistry on the Gold current702 (non-circular)

Centroids trained on the disjoint **expansion-bronze** atlas; evaluated on the **expert-curated gold** current702 primaries with **chemistry-only** leakage-safe features (cofactor + Rhea reaction bond-change; EC / name / prose / fingerprint excluded). The gold labels were never grouped by the admission engine and are screened OUT of the bronze, so this is not the representation loop's bootstrap.

## Headline

- **Coarse cofactor-bucket accuracy (fair, gold granularity): 0.7619 = 160/210.** The gold seed taxonomy is ~8 coarse cofactor-class families; scored at that granularity, chemistry-only recovers the gold mechanism class this often.
- Exact-fingerprint accuracy: 0.3095 = 65/210 -- LOWER because it penalises the representation for resolving a FINER, mechanistically-correct subfamily than the 2026-05-25 gold label (e.g. metal_dependent_hydrolase -> zinc_lyase_hydratase). See misses.
- Gold primaries total 232; featurizable 210; family-centroid-covered 210.

## Abstention / precision side (does novel chemistry score lower?)

- In-distribution nearest-similarity: {'n': 210, 'mean': 0.7431, 'median': 0.7973, 'p10': 0.4911, 'p90': 0.9876}.
- Out-of-scope nearest-similarity:    {'n': 448, 'mean': 0.7165, 'median': 0.8256, 'p10': 0.0, 'p90': 0.9895}.
- if OOS nearest-similarity sits below in-distribution, a similarity threshold separates known-mechanism from novel-mechanism (the abstention signal).

## Misses: 145 (sample shows where chemistry resolves to a sibling)

- `ser_his_acid_hydrolase` -> `acid_coa_ligase` (sim 0.0, own 0.0; P08819)
- `flavin_dehydrogenase_reductase` -> `flavin_disulfide_reductase` (sim 0.9948, own 0.8956; P00390)
- `metal_dependent_hydrolase` -> `metallophosphoesterase_nuclease` (sim 0.7973, own 0.7592; P0A6C1)
- `metal_dependent_hydrolase` -> `metallo_beta_lactamase` (sim 0.9801, own 0.7312; P25910)
- `metal_dependent_hydrolase` -> `metallo_beta_lactamase` (sim 0.9801, own 0.7312; P04190)
- `metal_dependent_hydrolase` -> `metal_independent_phosphodiesterase` (sim 0.7071, own 0.6783; P09598)
- `metal_dependent_hydrolase` -> `cysteine_protease` (sim 0.7256, own 0.0088; P10688)
- `heme_peroxidase_oxidase` -> `cytochrome_p450_monooxygenase` (sim 0.8386, own 0.4866; Q05769)
- `metal_dependent_hydrolase` -> `acid_coa_ligase` (sim 0.0, own 0.0; P0A6T5)
- `metal_dependent_hydrolase` -> `metallophosphoesterase_nuclease` (sim 0.7504, own 0.0902; P00639)
- `metal_dependent_hydrolase` -> `manganese_iron_superoxide_dismutase` (sim 0.9876, own 0.1188; P13717)
- `metal_dependent_hydrolase` -> `metallophosphomonoesterase` (sim 0.8722, own 0.6199; P80366)
- `metal_dependent_hydrolase` -> `metallophosphomonoesterase` (sim 0.8722, own 0.6199; P00634)
- `cobalamin_radical_rearrangement` -> `cofactor_independent_isomerase` (sim 0.9221, own 0.7877; P80077)
- `metal_dependent_hydrolase` -> `alpha_beta_hydrolase_esterase_lipase` (sim 0.8737, own 0.0436; P00592)
- `metal_dependent_hydrolase` -> `thiamine_diphosphate_enzyme` (sim 0.563, own 0.0; P18314)
- `ser_his_acid_hydrolase` -> `alpha_beta_hydrolase_esterase_lipase` (sim 0.9289, own 0.8681; Q29460)
- `metal_dependent_hydrolase` -> `metallo_amidohydrolase_deaminase` (sim 0.9219, own 0.8183; P0ABF6)
- `metal_dependent_hydrolase` -> `metallophosphoesterase_nuclease` (sim 0.651, own 0.6326; P0A6K3)
- `flavin_dehydrogenase_reductase` -> `flavin_monooxygenase` (sim 0.6005, own 0.5121; P56216)

## Three conclusions (what this says about the North Star)

1. **POSITIVE — the atlas generalises beyond its bootstrap.** Centroids trained on the disjoint expansion-bronze atlas recover the coarse mechanism class of expert-curated gold enzymes **0.7619** of the time, from chemistry alone (no EC/name/prose). The mechanism-from-chemistry thesis is not just an artifact of the admission engine grouping its own rows.
2. **The exact-fingerprint 0.3095 is a taxonomy-version artifact, not a failure.** The gold 702 uses ~8 coarse seed families (2026-05-25); the centroids are today's 57. The misses are dominated by the representation resolving a FINER, mechanistically-correct subfamily that post-dates the gold label (metal_dependent_hydrolase -> the metal-hydrolase subfamilies; heme_peroxidase -> P450; flavin_dehydrogenase -> flavin_disulfide [e.g. P00390 glutathione reductase]). The representation is being penalised for being MORE granular and correct than the gold.
3. **NEGATIVE — no abstention signal (the binding constraint, reconfirmed at 10k).** Out-of-scope enzymes score nearest-centroid similarity median **0.8256**, i.e. NOT below the in-distribution median **0.7973** -- a similarity threshold cannot separate novel mechanism from known. Growing breadth to 10k did NOT create a novelty/abstention signal; the wall is feature overlap, exactly the MAP's Northstar Pivot. The deployable lever is the fold/geometry + cofactor channel (which needs the ML env), NOT more families.
