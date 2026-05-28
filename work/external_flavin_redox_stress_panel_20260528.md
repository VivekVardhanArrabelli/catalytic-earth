# External Flavin/Redox Stress Panel - 2026-05-28

Run time: 2026-05-28T13:18:00Z

Scope: validation-panel design and source/evidence scouting only. No labels, registries, ontology files, thresholds, production scoring, imports, or model outputs were changed. No large downloads were performed; disk was checked before writing and had 13 GiB free, above the 10 GiB floor.

Machine-readable artifact: `artifacts/v3_external_flavin_redox_stress_panel_20260528.json`.

## Bottom Line

This panel deliberately moves beyond M-CSA-only and beyond the too-broad v1 flavin bucket. It defines 48 candidate rows/leads across clean flavin hydride-transfer, FMO/C4a-peroxy oxygen transfer, flavodiiron NO reduction, radical flavin/Fe-S dehydration, covalent FAD-adduct chemistry, flavin oxidase-only O2 acceptor chemistry, and non-flavin oxygenase hard negatives.

Tier split:

| Tier | Count | Use |
| --- | ---: | --- |
| Gold | 8 | M-CSA curated anchors for clean hydride transfer and current canonical FMO. |
| Silver/review-only | 9 | Mechanism-useful rows with future-child, coordinate, duplicate, or source caveats. |
| Bronze/source-only | 7 | External leads or boundary rows needing structure, duplicate/leakage, and terminal gates. |
| Hard-negative controls | 24 | Near-family flavin controls and heme/P450/pterin/non-heme-iron/copper/luciferase OOS controls. |

## Panel Axes

| Axis | Rows/leads | Purpose |
| --- | --- | --- |
| Clean flavin hydride-transfer dehydrogenase/reductase | `m_csa:3`, `6`, `353`, `381`, `506`, `892` | Positive anchors for ordinary FAD/FMN hydride or redox transfer without oxygen insertion. |
| Fe-S plus flavin relay/coupled reduction | `m_csa:990`, `108`, `114`, `142`, `294`, `800` | Stress generic flavin/Fe-S evidence and keep `m_csa:990` out of a plain hydride child. |
| Covalent FAD-substrate adduct | `m_csa:123` | Boundary/future child; not FMO and not ordinary hydride transfer. |
| Radical flavin/Fe-S dehydratase | `m_csa:750` | Future radical flavin/Fe-S family candidate; hard negative for v1 hydride and FMO. |
| Flavodiiron NO reductase | `m_csa:497` | Non-heme diiron catalytic locus with FMNH2 electron donor; hard negative for flavin-locus leakage. |
| FMO/C4a-peroxy oxygen transfer | `m_csa:131`, `132`, `551`, `973`, `P12015`, `Q93TJ5`, `Q01740`, `H3JQW0`, `O15229`, `P23262`, `P11295`, `P25535`, `Q6F4M8` | Separates PHBH-like, two-component FMNH2, BVMO, class B FMO, sulfur oxygenation, and medium-confidence source leads. |
| FMO boundary negative | `P06617` | Name/O2/FMN boundary without clean reductive/C4a evidence. |
| Flavin oxidase, O2 terminal acceptor only | `m_csa:109`, `110`, `113`, `354`, `822`, `852`, `895` | Must not satisfy FMO just because O2 is present. |
| Flavin/heme hydroxylating boundary | `m_csa:141` | Flavin plus heme and hydroxylating words, but not C4a-peroxy oxygen transfer. |
| Non-flavin oxygenase controls | `m_csa:128`, `129`, `130`, `133`, `134`, `135`, `600`, `601`, `699`, `768`, `795` | Heme/P450/pterin/non-heme iron/copper/luciferase hard negatives. |

## Gold

Gold rows are review-panel anchors, not new production labels. They have M-CSA curated mechanism context and local structure/cofactor evidence.

- Clean hydride-transfer anchors: `m_csa:3`, `m_csa:6`, `m_csa:353`, `m_csa:381`, `m_csa:506`, `m_csa:892`.
- Canonical current FMO anchors: `m_csa:131` PHBH-like FAD/NADPH aromatic hydroxylase and `m_csa:132` two-component FMNH2 alkanal monooxygenase.

## Silver / Review-Only

- `m_csa:990` remains broad v1 flavin support but must carry `fe_s_plus_flavin` and coupled dehydration/reduction caveats.
- `m_csa:123` is covalent FAD-adduct/boundary chemistry.
- `m_csa:750` is radical FAD semiquinone plus Fe-S dehydration, not ordinary hydride transfer.
- `m_csa:497` is flavodiiron NO reduction at a non-heme diiron locus with FMNH2 electron donor.
- `m_csa:551` and `m_csa:973` are mechanism-clean FMO review support but remain non-import/non-countable.
- `H3JQW0`, `O15229`, and `P23262` are source-positive FMO rows held by duplicate/family or coordinate-state blockers.

## Bronze / Source-Only

- Clean source leads: `P12015` CHMO/BVMO, `Q93TJ5` HAPMO/BVMO, `Q01740` human FMO1/class B FMO.
- Medium-confidence source leads: `P11295` IucD, `P25535` UbiI, `Q6F4M8` nitrophenol monooxygenase component.
- Boundary negative: `P06617` tryptophan 2-monooxygenase lacks the clean reductive/C4a-peroxy evidence needed here.

These rows are useful for stress-panel design and acquisition targeting only. They are not label imports.

## Hard Negatives

The hard negatives cover two distinct failure modes:

- Near-family flavin controls: oxidases and Fe-S/flavin relays that share FAD/FMN, NAD(P)H, O2, or redox vocabulary but lack FMO oxygen insertion.
- Out-of-scope oxygenases: heme/P450/pterin/non-heme iron/copper/luciferase chemistry where O2 activation is not at a flavin C4a-peroxy locus.

Any FMO call on the oxidase-only rows or non-flavin oxygenases is a regression. Any clean hydride-transfer call on `m_csa:497`, `m_csa:750`, or `m_csa:123` without preserving the non-heme diiron, radical Fe-S, or covalent-adduct mechanism locus is also a regression.

## What Would Prove Generalization

The router generalizes if it:

- keeps the six clean hydride-transfer anchors together without absorbing FMO or oxidase-only chemistry;
- routes `m_csa:131`/`132`/`551`/`973` and the external FMO leads by C4a/peroxyflavin oxygen-transfer evidence rather than by PHBH-only ligand exceptions;
- treats partner-supplied FMNH2 systems as valid FMO review support even when NADP(H) is absent from the oxygenase coordinate;
- separates `m_csa:497`, `m_csa:750`, and `m_csa:123` into flavodiiron, radical flavin/Fe-S, and covalent FAD-adduct boundary lanes;
- rejects heme/P450/pterin/non-heme-iron/copper/luciferase oxygenases as FMO despite oxygenase naming.

## What Would Prove The Ontology Is Still Too Broad

The FMO/flavin ontology is still too broad if:

- oxidase-only rows (`m_csa:109`, `110`, `113`, `354`, `822`, `852`, `895`) become FMO positives because they contain FAD/FMN plus O2;
- `m_csa:497`, `m_csa:750`, or `m_csa:123` are routed as ordinary flavin hydride-transfer rows;
- heme/P450/pterin/non-heme-iron/copper oxygenases are routed into FMO from oxygenase words alone;
- the router requires local NADP(H) ligand for two-component FMNH2 oxygenases and therefore rejects `m_csa:132`/`973`;
- BVMO/class B FMO/sulfur-oxygenation rows collapse into the PHBH-like aromatic hydroxylase lane without subtype metadata.

## Next Use

Use this artifact as a review-only stress-panel candidate list. Do not import, relabel, tune thresholds, or score production paths from it. The next real acquisition work would be exact ligand-bearing coordinate sourcing for `P12015`, `Q01740`, and `Q93TJ5`, plus explicit duplicate/leakage and terminal-review gates for the medium-confidence source leads.
