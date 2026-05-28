# FMO Fingerprint Definition Audit - 2026-05-28

Run time: 2026-05-28T07:05:00Z

Review-only audit. No labels, registries, ontology files, thresholds, production scoring, imports, or model outputs were changed. No large downloads were performed; this pass used existing local artifacts, coordinate caches, source-review packets, and prior small metadata lookup artifacts as review context.

Machine-readable artifact: `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`.

## Bottom Line

The blocker is not true out-of-scope chemistry for CHMO/BVMO, HAPMO, or human FMO1. The current registry definition is broad enough for aromatic hydroxylases, BVMOs, two-component FMNH2 oxygenases, and class B FMOs. The active source-free geometry/counterevidence gate, however, is PHBH-leaning and generic-flavin-redox-prone, while the latest external pass is chiefly blocked by missing exact ligand-bearing coordinate materialization.

Recommendation: keep `flavin_monooxygenase` secondary-only, create review-only subtype panels, revise the silver/review evidence gate, and do not canonically promote any FMO child or parent label now.

## Current Encoded Assumptions

### Registry definition

`data/registries/mechanism_fingerprints.json` defines `flavin_monooxygenase` as flavin peroxide oxygen transfer across monooxygenases, Baeyer-Villiger monooxygenases, and hydroxylases. It expects FAD, FMN, and NADPH context; an oxidizable substrate near flavin C4a; oxygen access; a redox-compatible pocket; and evidence from a flavin-binding motif, flavin-proximal substrate pocket, NADPH-binding context, and oxygenase-family fold.

That definition is broad. The overfit risk comes less from the registry text and more from active source-free feature logic.

### Source-free geometry and counterevidence

The current geometry stack extracts a generic flavin redox site: FAD/FMN/RBF plus nearby generic flavin-binder, redox/acid-base, and electron-transfer residues. The contact cutoffs are 4.2 A for flavin binder and 5.0 A for redox/electron-path contacts. This is useful flavin-redox geometry, but it is not a direct detector for C4a oxygen insertion, BVMO carbonyl migration, class B FMO N/S oxygenation, or partner-supplied FMNH2 oxygenation.

The strongest PHBH-like bias is in counterevidence:

- `PHB` and `BR` are the only explicit FMO substrate ligand-code exceptions.
- FAD/FMN without a local NAD-family ligand is penalized for FMO unless `PHB`/`BR` context is present.
- `flavin_dehydrogenase_reductase` is penalized when `PHB`/`BR` appears without electron-transfer context.

The observed 2026-05-21 deep packet behavior matches that concern: all seven source-free rows scored top1 as `flavin_dehydrogenase_reductase`; `flavin_monooxygenase` was never top1. Only H3JQW0 reached the FMO floor, apparently helped by FAD plus NADP.

## Local Geometry Readout

| Row | Interpretation | Coordinate assumptions |
| --- | --- | --- |
| `m_csa:131` PHBH-like 4-hydroxybenzoate hydroxylase | Canonical current FMO context | FAD/NADPH, reduced flavin plus O2, C4a-peroxy/hydroperoxy FAD, aromatic hydroxylation. |
| `m_csa:132` alkanal monooxygenase | Canonical current FMO context but two-component/reduced-FMN boundary | Reduced FMN is supplied to oxygenase; NADPH is not necessarily local to the oxygenase component. |
| `m_csa:551` phenol 2-monooxygenase | Mechanism-clean secondary/future aromatic hydroxylase support | FAD and IPH are present. Prior mapped chain A has FAD C4X-to-IPH O1 at 7.10 A, but local adjudication found productive author chain C at 4.582 A and chain D at 4.649 A. No NADPH/NADP or peroxyflavin state is present; those are structural-state caveats. |
| `m_csa:973` DszC | Mechanism-clean two-component FMNH2 sulfur monooxygenase support, coordinate-clean false | FMN C4A is near Tyr96 OH at 3.37 A, Ser163 OG at 3.69 A, and His391 NE2 at 4.23 A. No substrate/analog or peroxyflavin state is present. NADPH/NADP absence is not a blocker because reduced FMNH2 is partner-supplied. |

The local artifacts show a real materialization/pose issue for `m_csa:551` and a real two-component reductant-context issue for `m_csa:973`. Neither supports rejecting broad FMO chemistry as out of scope.

## Subtype Comparison

### PHBH, salicylate, and KMO aromatic hydroxylases

This is the best represented current lane. `m_csa:131` and `m_csa:551` cover FAD/NAD(P)H aromatic hydroxylation through C4a-hydroperoxyflavin chemistry. Salicylate hydroxylase and KMO are chemically compatible, but the latest gates hold them as duplicate/family-overlap support: KMO has prior duplicate/leakage against `m_csa:131`, and salicylate overlaps the aromatic hydroxylase lane.

Decision: in scope, but not new clean non-duplicate evidence under current gates.

### CHMO/BVMO and HAPMO

CHMO, HAPMO, and OTEMO are genuine BVMO chemistry: FAD/NADPH, reduced flavin plus O2, peroxyflavin oxygen insertion into carbonyl substrates, and lactone/ester products. This is not PHBH-like aromatic ring hydroxylation, and it should be represented as a separate review panel.

Current blocker: exact-coordinate materialization. `P12015` and `Q93TJ5` have only exact AlphaFold protein-only models in the current pass. `H3JQW0` has exact FAD/NADP PDB material but is held as duplicate/family support and lacks substrate/analog/product in the selected coordinate.

Decision: genuine subtype diversity, not out-of-scope chemistry.

### Human FMO1 / class B FMO

Human FMO1 is a distinct class B FMO lane: FAD/NADPH chemistry forms a C4a-hydroperoxyflavin oxygenating species for N/S oxygenation. Its substrate chemistry and active-site framing differ from PHBH-like aromatic hydroxylases and BVMOs.

Current blocker: exact-coordinate materialization. `Q01740` is source-clean and non-duplicate but has only exact AlphaFold protein-only coordinates in the current pass. Homologs are useful only as silver/review diagnostics.

Decision: genuine subtype diversity requiring a review panel.

### DszC and two-component FMNH2 oxygenases

DszC and bacterial alkanal monooxygenase/luciferase-like rows show why a local NADPH ligand requirement is unsafe. The oxygenase component may consume reduced FMNH2 supplied by a partner. The FMO evidence contract should record reductant/partner context rather than require NADP(H) in the same coordinate.

Decision: genuine separate child stratum or review panel; not a generic FAD/NADPH single-component case.

### True hard negatives

The hard-negative axis should include ordinary flavin hydride-transfer dehydrogenases/reductases, flavin oxidases where O2 is terminal acceptor only, Fe-S plus flavin relays, covalent FAD-adduct chemistry, flavodiiron NO reductase, radical flavin/Fe-S dehydratase, heme/P450/peroxidase oxygenases, non-flavin metal/pterin/copper oxygenases, and ATP/luciferyl oxygenations.

Examples already captured in local artifacts include `m_csa:141`, `m_csa:109`, `m_csa:978`, `m_csa:977`, `m_csa:128`, `m_csa:497`, and `m_csa:750`.

## Blocker Decision

Primary blocker: missing exact ligand-bearing coordinate materialization.

Secondary blocker: valid subtype diversity requiring v2 child strata or review-only panels.

Tertiary blocker: the current silver/review gate is PHBH-biased and under-specified for non-PHBH FMO chemistry.

Not the blocker: CHMO/BVMO, HAPMO, and FMO1 being out-of-scope chemistry.

## Recommended Policy

Keep FMO secondary-only. Do not promote the parent or any child canonically.

Create review-only subtype panels:

- `fmo_aromatic_hydroxylase_c4a_peroxy`: `m_csa:131`, `m_csa:551`, KMO, salicylate.
- `fmo_baeyer_villiger_bvmo`: CHMO, HAPMO, OTEMO.
- `fmo_class_b_n_s_oxygenation`: FMO1/FMO3/FMO5-like rows.
- `fmo_two_component_fmnh2_oxygenation`: `m_csa:132`, DszC, related reduced-FMNH2 systems.

Revise the review/silver gate:

- Require reduced FAD/FMN plus O2 forming C4a-hydroperoxyflavin, C4a-peroxyflavin, or equivalent flavin-peroxy oxygenating chemistry.
- Require substrate oxygen insertion/oxygenation context: aromatic hydroxylation, oxidative decarboxylation, N-oxygenation, S-oxygenation, Baeyer-Villiger insertion, or aldehyde oxygenation.
- Treat local NADP(H) absence as a coordinate-state caveat when partner-supplied FMNH2 or missing nicotinamide state explains it.
- Do not rely on `PHB`/`BR` as the only FMO-positive substrate exceptions.
- Keep exact ligand-bearing coordinates as gold/countable only after duplicate/leakage and import gates; use homolog coordinates only as silver/review diagnostics.

## Next Acquisition Targets

Exact ligand-bearing targets:

1. `uniprot:P12015` CHMO: exact FAD plus NADP(H) plus cyclohexanone, caprolactone, or close analog/product coordinate.
2. `uniprot:Q01740` human FMO1: exact FAD/NADP(H) plus dimethylaniline, trimethylamine, hypotaurine/taurine, or product/analog coordinate.
3. `uniprot:Q93TJ5` HAPMO: exact FAD/NADP(H) plus 4-hydroxyacetophenone, 4-acetoxyphenol, or close analog/product coordinate.
4. `m_csa:973` DszC: FMN-bound DszC with dibenzothiophene-family substrate, sulfoxide/sulfone product, or substrate analog near FMN C4A.
5. `m_csa:551` phenol 2-monooxygenase: use pdb:1FOH author chain C for future pocket extraction, with chain D as corroborating geometry only.

Silver homolog targets, not countable:

- CHMO/BVMO: `3UCL`, `4RG3`, `4RG4`, `8YU0`.
- Class B FMO: `7AL4`, `6SE3`.
- Broad HAPMO/BVMO stress: `4AP3`, `2YM1`.

Hard-negative targets:

- Ordinary flavin hydride-transfer/dehydrogenase rows: `m_csa:3`, `m_csa:6`, `m_csa:353`, `m_csa:381`, `m_csa:506`, `m_csa:892`.
- Flavin oxidase O2-acceptor rows: `m_csa:109`, `m_csa:110`, `m_csa:113`, `m_csa:354`, `m_csa:822`, `m_csa:852`, `m_csa:895`.
- Flavin/Fe-S relay rows: `m_csa:990`, `m_csa:108`, `m_csa:114`, `m_csa:142`, `m_csa:294`, `m_csa:800`.
- OOS flavin controls: `m_csa:497`, `m_csa:750`.
- Covalent FAD-adduct boundary: `m_csa:123`.
- Heme/P450/peroxidase oxygenases: `m_csa:133`, `m_csa:699`, `m_csa:795`, `m_csa:601`.
- Non-flavin oxygenase/luciferase controls: `m_csa:128`, `m_csa:129`, `m_csa:130`, `m_csa:134`, `m_csa:135`, `m_csa:600`, `m_csa:768`.

## Verification Targets

- JSON parse: `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`
- CLI validation: `PYTHONPATH=src python -m catalytic_earth.cli validate`
- Whitespace: `git diff --check`
