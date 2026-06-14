# High-Yield Family Lane Factory Scout

Run: 2026-06-14T21:39:33Z

Non-destructive scout/factory artifact. No labels or registries were written.
EC is used only for scope; corroborator handles are admission/source planning only.

## Result

- Candidate families ranked: 12.
- Ready existing lanes with >=150 projected clean admits: 0.
- High-yield lanes blocked by new fingerprint/rule/preregistration: 1.
- Existing lanes blocked by <150 cap room: 5.
- Combined label surface: 8010.
- Combined seed-fingerprint surface: 6314.
- Remaining gap to 10k seed surface: 3686.

## Ranking

| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ser_thr_protein_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 1142 | 943 | 0.826 | 150 | 150 | chemistry_confusable_cap_150 |
| 2 | short_chain_dehydrogenase_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 241 | 0.031 | 84 | 150 | chemistry_confusable_cap_150 |
| 3 | terpene_cyclase_synthase | blocked_existing_cap_room_below_150 | 2335 | 2315 | 0.991 | 77 | 77 | clean_nonconfusable_cap_250 |
| 4 | serine_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 156 | 0.862 | 70 | 150 | chemistry_confusable_cap_150 |
| 5 | aminoglycoside_phosphotransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 14226 | 153 | 0.011 | 61 | 150 | chemistry_confusable_cap_150 |
| 6 | protein_kinase_ser_thr_tyr | blocked_existing_cap_room_below_150 | 5117 | 3470 | 0.678 | 50 | 50 | chemistry_confusable_cap_150 |
| 7 | aldo_keto_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 125 | 0.016 | 44 | 150 | chemistry_confusable_cap_150 |
| 8 | aminoglycoside_acetyltransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 9981 | 84 | 0.008 | 34 | 150 | chemistry_confusable_cap_150 |
| 9 | metallo_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 37 | 0.204 | 17 | 150 | chemistry_confusable_cap_150 |
| 10 | had_like_phosphatase | blocked_existing_cap_room_below_150 | 4457 | 3477 | 0.78 | 4 | 4 | chemistry_confusable_cap_150 |
| 11 | aldehyde_dehydrogenase | blocked_existing_cap_room_below_150 | 3160 | 3153 | 0.998 | 0 | 0 | chemistry_confusable_cap_150 |
| 12 | alpha_beta_hydrolase_esterase_lipase | blocked_existing_cap_room_below_150 | 6160 | 1352 | 0.219 | 0 | 0 | chemistry_confusable_cap_150 |

## Top Lane Requirements

### ser_thr_protein_phosphatase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: protein-phosphatase family/name handle; dinuclear metal binding-site/cofactor context; Rhea phosphoprotein dephosphorylation equation where available.
- Holds: small-molecule phosphomonoesterase rows; protein kinase rows; HAD-like Asp-phosphatase rows; EC-only rows without protein substrate or metal corroboration.
- Rationale: Mechanistically useful protein-substrate phosphatase split, but it overlaps the existing metal phosphomonoesterase chemistry without a new rule.

### short_chain_dehydrogenase_reductase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: SDR family/name/domain handle; NAD(P) participant or Rossmann binding-site context; Ser-Tyr-Lys/Asn active-site evidence where available.
- Holds: AKR rows; zinc medium-chain alcohol dehydrogenase rows; flavin/metal redox rows.
- Rationale: Very large hydride-transfer family, but current source handles are weak; requires an SDR-specific rule instead of broad EC 1.1.1 padding.

### terpene_cyclase_synthase
- Status: blocked_existing_cap_room_below_150.
- Required non-EC corroborators: terpene/cyclase functional keyword or protein-name handle; Mg/Mn diphosphate-binding handle or active-site metal context; Rhea reaction participant showing diphosphate release/cyclization where available.
- Holds: prenyltransferase chain-extension rows; lyase/hydratase rows without terpene cyclization evidence; multi-fingerprint metal-lyase signal rows.
- Rationale: Clean carbocation cyclization chemistry outside the current atlas; prefer reviewed EC 4.2.3 rows with metal/diphosphate corroboration.

### serine_beta_lactamase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: beta-lactamase keyword/name handle; active-site Ser/Lys/Glu beta-lactamase motif evidence; Rhea beta-lactam hydrolysis equation where available.
- Holds: metallo-beta-lactamase zinc rows; general amidohydrolase rows; resistance proteins without catalytic beta-lactamase evidence.
- Rationale: Resistance-relevant covalent acyl-enzyme hydrolase split; keep separate from zinc metallo-beta-lactamases and generic amidohydrolases.

### aminoglycoside_phosphotransferase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: aminoglycoside phosphotransferase family/name handle; ATP/Mg participant or binding-site context; aminoglycoside phosphorylation reaction evidence where available.
- Holds: protein kinase rows; small-molecule kinase rows; aminoglycoside acetyltransferase/nucleotidyltransferase rows.
- Rationale: Resistance-relevant ATP phosphoryl transfer; needs explicit separation from protein and small-molecule kinase fingerprints.

## Guardrails

- Registry written: False.
- Labels created: False.
- EC scope-only / never predictive: True.
- Future labels must be bronze / automation_curated in the uniprot namespace.
- Dedup against current702 and external bronze is required before apply.

## Next action

- No existing lane has >=150 cap room. Build the `ser_thr_protein_phosphatase` fingerprint/source runner first: ontology node, mechanism disambiguation rule, OOS preregistration, row guardrail audit, preview, tests, then apply only if gates pass.
