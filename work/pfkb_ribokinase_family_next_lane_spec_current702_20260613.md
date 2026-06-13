# PfkB Ribokinase-Family Next-Lane Scaffold (2026-06-13)

Status: non-importing scaffold for a possible strict kinase split after PfkA. This is **not** an
apply recommendation yet; the sampled source supply is weaker than PfkA and needs tighter admission
handles before a full 33fp pipeline.

Source basis from `artifacts/v3_strict_kinase_subclass_source_scout_after_dnk_current702_20260613.json`:

- Reviewed UniProt supply: 85.
- Sampled with entry JSON: 40 / 40.
- Likely wireable sample: 28 / 40.
- Sampled boundary signal: 0 / 40.
- Mechanism handles in sample: Rhea 40, phosphoryl reaction text 40, family text 40, active/binding
  site context 28.
- Sample EC mix: `2.7.1.4` 12, `2.7.1.20` 11, `2.7.1.15` 9, `2.7.1.-` 6, `2.7.1.73` 4,
  `2.7.1.3` 3, `2.7.1.213` 2, `2.7.1.56` 2, plus one sampled `5.3.1.6` side annotation.

Recommended strict query draft:

```text
(reviewed:true) AND (ec:2.7.1.*) AND
((protein_name:"ribokinase") OR
 (protein_name:"adenosine kinase") OR
 (protein_name:"inosine kinase") OR
 (protein_name:"fructokinase") OR
 (protein_name:"1-phosphofructokinase"))
NOT ((ec:2.7.11.*) OR (ec:2.7.13.*) OR (ec:3.*) OR
     (protein_name:"protein kinase") OR (protein_name:"histidine kinase") OR
     (protein_name:"deoxynucleoside kinase") OR
     (protein_name:"thymidine kinase") OR
     (protein_name:"deoxyguanosine kinase") OR
     (protein_name:"deoxycytidine kinase") OR
     (protein_name:"nucleoside diphosphate kinase") OR
     (protein_name:"nucleoside-diphosphate kinase") OR
     (protein_name:"hexokinase") OR (protein_name:"glucokinase") OR
     (protein_name:"glycerol kinase") OR
     (protein_name:"homoserine kinase") OR
     (protein_name:"mevalonate kinase") OR
     (protein_name:"phosphomevalonate kinase") OR
     (protein_name:"galactokinase") OR
     (protein_name:"6-phosphofructokinase"))
```

Admission design:

- Candidate fingerprint id: `pfkb_ribokinase_family`.
- Candidate ontology node: add a narrow ATP phosphoryl-transfer child for PfkB/ribokinase-family
  small-molecule kinases only if the preview confirms clean mechanism separation from ASKHA, GHMP,
  dNK, NDK, and PfkA.
- EC 2.7.1 is scope-only and must stay in `excluded_context`; it is never a counted corroborator.
- Counted mechanism axes should come from ATP/ADP phosphoryl-transfer Rhea participant text,
  ribokinase/PfkB/adenosine-kinase/inosine-kinase/1-phosphofructokinase family text, ATP/Mg or
  substrate active-/binding-site evidence, cofactor/cosubstrate handles, and structure-compatible
  evidence.
- `predictive_evidence` must remain `[]`; EC/name/Rhea/keyword/prose/feature handles are
  scope/admission evidence only.

Boundary guards:

- Hold protein kinases (`2.7.11.*`), two-component histidine kinases (`2.7.13.*`),
  hydrolase/nuclease side rows (`3.*`), NDK (`2.7.4.6` / NDP kinase text), dNK, ASKHA,
  GHMP, PfkA/6-phosphofructokinase, broad hexokinase/glucokinase/glycerol kinase rows, and
  multi-fingerprint-signal rows.
- Treat as chemistry-confusable and use cap 150 if this lane is ever applied.
- Do not use broad EC 2.7 or the presence of a kinase name as a counted mechanism corroborator.

Next exact implementation sequence:

1. Before adding a fingerprint, improve the source-supply scout to require active-/binding-site or
   substrate-specific evidence where possible and re-check the 28/40 wireability gap.
2. If the stricter scout remains viable, add `pfkb_ribokinase_family` fingerprint + ontology mapping
   and bump the fingerprint universe to the next version.
3. Re-freeze OOS preregistration for the new universe before any preview.
4. Add disambiguation rules/tests that hold PfkA, ASKHA, GHMP, dNK, NDK, protein kinase, histidine
   kinase, hydrolase/nuclease, and multi-signal rows.
5. Run non-destructive preview with `--max-records-per-lane 240 --cap-ceiling 150`; apply only if
   novelty, governor, dedup, trust-tier, and leakage gates pass.
