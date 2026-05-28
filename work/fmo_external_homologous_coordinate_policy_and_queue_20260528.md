# FMO Homologous Coordinate Policy and Queue - 2026-05-28

Run time: 2026-05-28T05:42:51Z

Review-only decision artifact: `artifacts/v3_fmo_external_homologous_coordinate_policy_and_queue_702_20260528.json`.

No labels, registries, ontology files, thresholds, production scoring, imports, or model outputs were changed.

## Policy

Exact UniProt/PDB ligand-bearing coordinates remain required for gold/countable FMO label import. Homologous ligand-bound coordinates are not countable labels. They may only be used as silver/review-only evidence, active-site representation diagnostics, acquisition targeting, or learned-representation stress panels.

This keeps the gold benchmark strict while still letting Wave 1.1 test whether representations capture C4a/FAD oxygen-transfer geometry instead of generic flavin redox features.

## Tier Split

| Tier | Rows | Decision |
| --- | --- | --- |
| Gold/countable labels | none new | No external FMO row is import-ready after exact-coordinate materialization. |
| Silver/review-only evidence | `P12015`, `Q01740`; limited broad support for `Q93TJ5` | Use homolog coordinates only for review, diagnostics, acquisition targeting, and stress panels. |
| Bronze/source-only leads | `P12015`, `Q93TJ5`, `Q01740` | Source-clean, non-countable, exact-coordinate acquisition backlog. |
| Duplicate/family holds | `H3JQW0`, `O15229`, `P23262` | Preserve holds; do not promote. |

## Candidate Decisions

### `uniprot:P12015` CHMO

Useful homologous ligand-bound coordinates exist and are close enough for silver CHMO/BVMO review.

| Homolog | Local identity / coverage | State | Geometry use |
| --- | --- | --- | --- |
| `pdb:3UCL` / `uniprot:C0STX7` | 58.4% identity, 93.4% query coverage | FAD + NADP + cyclohexanone | FAD C4X to CYH O1 = 3.008 angstrom; strong review-only substrate-pose support. |
| `pdb:4RG3` / `uniprot:C0STX7` | 58.4% identity, 93.4% query coverage | FAD + NADP + caprolactone | FAD C4X to ECE O = 3.529 angstrom; useful product-state support. |
| `pdb:8YU0` / `uniprot:A0A0A8XFY0` | 69.7% identity, 94.3% query coverage | FAD + reduced NADPH code NDP | Good cofactor/conformation review, no substrate/product ligand. |

Blocker to gold: these are homolog accessions, not exact P12015 coordinates. Exact P12015 remains AlphaFold protein-only in the consumed materialization pass.

### `uniprot:Q93TJ5` HAPMO

Homologous ligand-bound coordinates exist, but they are only limited broad BVMO support. They are not close or candidate-specific enough to claim HAPMO substrate geometry.

| Homolog | Local identity / coverage | State | Geometry use |
| --- | --- | --- | --- |
| `pdb:4AP3` / `uniprot:O50641` | 41.1% identity, 30.6% query coverage | FAD + NADP | Broad BVMO cofactor-pocket context only. |
| `pdb:2YM1` / `uniprot:Q47PU3` | 54.3% identity over a 70-aa local HSP, 10.8% query coverage | FAD + NADP + O2 | O2 is near FAD C4X at 3.485 angstrom; useful only as broad BVMO oxygen-pocket stress. |
| `pdb:3UOY` / `uniprot:H3JQW0` | 43.2% identity, 31.2% query coverage | FAD + NADP | Cofactor-only and H3JQW0 remains a duplicate hold, so do not use for promotion. |

Blocker to gold: no exact Q93TJ5 experimental ligand-bearing coordinate with FAD and 4-hydroxyacetophenone/product analog geometry.

### `uniprot:Q01740` Human FMO1

Homologous ligand-bound coordinates exist and are close enough for strong class B FMO silver review, but they still cannot become gold.

| Homolog | Local identity / coverage | State | Geometry use |
| --- | --- | --- | --- |
| `pdb:7AL4` / ancestral mammalian FMO1 | 90.3% identity, 98.9% query coverage | FAD + NADP | Strong cofactor/fold silver evidence; no substrate/product geometry. |
| `pdb:6SE3` / ancestral FMO3-6 | 56.8% identity, 99.8% query coverage | FAD + NADP + O2 | O2 near FAD C4X at about 5.18-5.84 angstrom; oxygen-pocket stress only. |

Blocker to gold: ancestral/synthetic homologs are not exact Q01740 coordinates and lack dimethylaniline, trimethylamine, hypotaurine/taurine, or product/analog geometry.

## Duplicate Holds

Preserve `H3JQW0` OTEMO, `O15229` KMO, and `P23262` salicylate 1-monooxygenase as duplicate/family holds. Existing exact coordinates do not reopen promotion because the controlling blockers remain duplicate/leakage, same-family overlap, or missing substrate/flavin geometry.

## Next Queue

Exact-coordinate acquisition targets:

1. `P12015` CHMO exact experimental FAD + cyclohexanone/caprolactone coordinate.
2. `Q01740` human FMO1 exact experimental FAD/NADP(H) + dimethylaniline, trimethylamine, hypotaurine/taurine, or analog/product coordinate.
3. `Q93TJ5` HAPMO exact experimental FAD/NADP(H) + 4-hydroxyacetophenone or 4-acetoxyphenol analog/product coordinate.

Homolog-silver review targets:

1. CHMO/BVMO: `3UCL`, `4RG3`, `4RG4`, `8YU0`.
2. Class B FMO: `7AL4`, `6SE3`.
3. Broad HAPMO/BVMO stress only: `4AP3`, `2YM1`.

Hard-negative controls for the FMO/redox panel:

- ordinary flavin hydride-transfer dehydrogenase/reductase
- flavin oxidase O2 acceptor, not monooxygenase
- flavin plus Fe-S relay / HCAR-like systems
- `m_csa:497` flavodiiron NO reductase
- `m_csa:750` radical flavin/Fe-S dehydratase
- `m_csa:123` covalent FAD-adduct APS reductase-like boundary
- heme oxygenases, P450s, and peroxidases
- pterin, non-heme iron, copper, ATP/luciferyl, and name-only oxygenase controls

## Wave 1.1 Routing

Wave 1.1 may consume homolog coordinates only with explicit metadata:

- `tier=silver_review_only`
- `homolog_not_gold=true`
- `source_accession_exact=false`
- `excluded_from_gold_benchmark=true`
- `excluded_from_threshold_tuning=true`
- `excluded_from_production_scoring=true`

The gold benchmark remains unchanged. Silver homologs should be paired with hard negatives to test whether learned representations separate C4a-peroxy flavin oxygen insertion from generic flavin/NAD(P)H/O2 or oxygenase-name signals.
