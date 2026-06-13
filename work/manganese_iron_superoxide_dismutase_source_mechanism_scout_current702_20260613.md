# Mn/Fe Superoxide Dismutase Source + Mechanism Scout

Generated: `2026-06-13T15:04:32Z`

Status: **non-destructive scout only; no labels generated and no registry writes.**

Frozen current702 sha256: `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
Registry baseline: curated 702, external bronze 6238, known UniProt accessions 6241.

## Why This Lane

The older breadth-feasibility row treated Mn/Fe SOD as source-poor because the `cc_cofactor:manganese/iron` query only captured one reviewed entry. A guarded EC+name/cofactor query captures the Mn/Fe SOD reviewed surface while excluding Cu/Zn SOD names. EC and names remain scope/admission handles only; any future labels still need non-EC mechanism corroboration.

## Source Counts

- `sod_ec_all`: **456** reviewed rows; query `(reviewed:true) AND (ec:1.15.1.1)`
- `sod_keyword_or_name`: **456** reviewed rows; query `(reviewed:true) AND (ec:1.15.1.1) AND ((keyword:"Superoxide dismutase") OR (protein_name:"superoxide dismutase"))`
- `mn_fe_sod_guarded_query`: **252** reviewed rows; query `(reviewed:true) AND (ec:1.15.1.1) AND ((cc_cofactor:manganese) OR (cc_cofactor:iron) OR (protein_name:manganese) OR (protein_name:iron) OR (protein_name:Mn) OR (protein_name:Fe)) NOT ((cc_cofactor:copper) OR (cc_cofactor:zinc) OR (protein_name:"Cu-Zn") OR (protein_name:"Cu/Zn") OR (protein_name:copper) OR (protein_name:zinc))`

## Sample Mechanism Axes

Sampled **80** rows from the guarded Mn/Fe query with **0** JSON fetch failures.
Registry-new sample rows: **80**; likely wireable under mechanism-first gate: **77**; registry-new likely wireable: **77**.
Axis counts: `{'active_binding_or_metal_site_axis': 77, 'mn_fe_metal_axis': 80, 'reaction_superoxide_text': 80, 'rhea_superoxide_dismutation': 80, 'sod_family_text_axis': 80}`.
Boundary counts: `{}`.

Rhea EC 1.15.1.1 records include:
- `RHEA:20696`: 2 superoxide + 2 H(+) = H2O2 + O2

## Guardrails For Any Future Lane

- Keep EC 1.15.1.1 and protein-name tokens as source/admission context only; EC is never a counted corroborator.
- Counted mechanism axes should include superoxide dismutation Rhea/reaction text, Mn/Fe metal or metal-site evidence, SOD family/keyword text, and active/binding/metal-site handles.
- Hold Cu/Zn SOD, heme/cytoglobin/peroxidase/nitrite/nitric-oxygen dioxygenase, superoxide reductase, side-EC, and multi-fingerprint-signal rows.
- Before preview/apply, add a deliberate fingerprint + ontology node, re-freeze OOS preregistration, add offline leakage/trust-tier/disambiguation tests, then run a non-destructive preview before any `--apply`.

## Recommendation

Recommended next lane: **manganese_iron_superoxide_dismutase**.
Wire next lane now: **True**.
Guarded reviewed query has floor-capable source supply and the sampled rows carry non-EC superoxide-dismutation, Mn/Fe metal, SOD family text, and active/binding/metal-site axes; future implementation must add Cu/Zn/heme/cytoglobin/superoxide-reductase/side-EC guards and run OOS prereg before preview/apply.

Representative registry-new likely-wireable accessions:
- `P04179` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
- `Q9K4V3` - Superoxide dismutase [Mn/Fe] (EC 1.15.1.1)
- `O81235` - Superoxide dismutase [Mn] 1, mitochondrial (EC 1.15.1.1) (Protein MANGANESE SUPEROXIDE DISMUTASE 1) (AtMSD1) (Protein MATERNAL EFFECT EMBRYO ARREST 33)
- `P09671` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
- `P07895` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
- `P00448` - Superoxide dismutase [Mn] (EC 1.15.1.1) (MnSOD)
- `Q00637` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
- `P54375` - Superoxide dismutase [Mn] (EC 1.15.1.1) (General stress protein 24) (GSP24)
- `P0AGD3` - Superoxide dismutase [Fe] (EC 1.15.1.1)
- `Q9FMX0` - Superoxide dismutase [Fe] 3, chloroplastic (EC 1.15.1.1) (Protein FE SUPEROXIDE DISMUTASE 3)
- `J9VWW9` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
- `Q9UQX0` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
- `P21276` - Superoxide dismutase [Fe] 1, chloroplastic (EC 1.15.1.1) (Protein FE SUPEROXIDE DISMUTASE 1) (FeSOD)
- `Q94EG3` - Nectarin-1 (EC 1.15.1.1) (Superoxide dismutase [Mn])
- `Q9LU64` - Superoxide dismutase [Fe] 2, chloroplastic (EC 1.15.1.1) (Protein ALBINO OR PALE GREEN 8) (Protein FE SUPEROXIDE DISMUTASE 2)
- `P09233` - Superoxide dismutase [Mn] 3.1, mitochondrial (EC 1.15.1.1)
- `P9WGE7` - Superoxide dismutase [Fe] (EC 1.15.1.1)
- `P19665` - Superoxide dismutase [Mn/Fe] (EC 1.15.1.1)
- `Q9LYK8` - Superoxide dismutase [Mn] 2, mitochondrial (EC 1.15.1.1) (Protein MANGANESE SUPEROXIDE DISMUTASE 2) (AtMSD2)
- `P41976` - Superoxide dismutase [Mn], mitochondrial (EC 1.15.1.1)
