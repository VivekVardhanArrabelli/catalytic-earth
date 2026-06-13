# Deoxynucleoside Kinase Next-Lane Scaffold (2026-06-13)

Status: non-importing scaffold for the next strict kinase split after ASKHA and GHMP applies.

Source basis from `artifacts/v3_strict_kinase_subclass_source_scout_after_ndk_current702_20260613.json`:

- Reviewed UniProt supply: 278.
- Sampled with entry JSON: 40 / 40.
- Likely wireable sample: 39 / 40.
- Sampled boundary signal: 1 / 40.
- Mechanism handles in sample: Rhea 40, phosphoryl reaction text 40, active/binding site 40,
  family text 40.

Recommended strict query:

```text
(reviewed:true) AND (ec:2.7.1.*) AND
((protein_name:"deoxynucleoside kinase") OR
 (protein_name:"thymidine kinase") OR
 (protein_name:"deoxyguanosine kinase") OR
 (protein_name:"deoxycytidine kinase"))
NOT ((ec:2.7.11.*) OR (ec:2.7.13.*) OR (ec:3.*) OR
     (protein_name:"protein kinase") OR (protein_name:"histidine kinase") OR
     (protein_name:"nucleoside diphosphate kinase") OR
     (protein_name:"nucleoside-diphosphate kinase") OR
     (protein_name:"hexokinase") OR (protein_name:"glucokinase") OR
     (protein_name:"glycerol kinase") OR (protein_name:"homoserine kinase") OR
     (protein_name:"mevalonate kinase") OR
     (protein_name:"phosphomevalonate kinase") OR
     (protein_name:"galactokinase") OR
     (protein_name:"phosphofructokinase") OR (protein_name:"ribokinase"))
```

Admission design:

- Fingerprint id: `deoxynucleoside_kinase`.
- Ontology node: existing ATP phosphoryl child `dnk`.
- EC 2.7.1 is scope-only and must stay in `excluded_context`; it is never a counted corroborator.
- Counted mechanism axes should come from ATP/ADP phosphoryl-transfer Rhea participant text,
  deoxynucleoside/thymidine/deoxyguanosine/deoxycytidine kinase family text, and active-/binding-site
  evidence for ATP, nucleoside substrate, or catalytic residues.
- `predictive_evidence` must remain `[]`; all EC/name/Rhea/keyword/prose/feature handles are
  scope/admission evidence only.

Boundary guards:

- Hold protein kinases (`2.7.11.*`), two-component histidine kinases (`2.7.13.*`), hydrolase/nuclease
  side rows (`3.*`), NDK (`2.7.4.6` / NDP kinase text), ASKHA (hexokinase/glucokinase/glycerol kinase),
  GHMP (homoserine/mevalonate/phosphomevalonate/galactokinase), PfkA/PfkB/ribokinase, and
  multi-fingerprint-signal rows.
- Use chemistry-confusable cap 150.

Next exact implementation sequence:

1. Add `deoxynucleoside_kinase` fingerprint and map it to ontology family `dnk`.
2. Extend `external_cofactor_ec_disambiguation.py` with dNK tokens, axes, rule, and synthesized
   ATP/deoxynucleoside provenance.
3. Add `deoxynucleoside_kinase_sourcing.py`, `scripts/source_deoxynucleoside_kinase_family.py`, and
   offline tests following the ASKHA/GHMP pattern.
4. Bump `CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to the next fp version and re-freeze OOS
   preregistration before preview/apply.
5. Run non-destructive preview with `--max-records-per-lane 240 --cap-ceiling 150`; apply only if
   dedup, novelty, governor, trust-tier, and leakage gates pass.
