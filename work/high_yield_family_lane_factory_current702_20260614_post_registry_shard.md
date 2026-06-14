# High-Yield Family Lane Factory Scout

Run: 2026-06-14T15:10:28Z

Non-destructive scout/factory artifact. No labels or registries were written.
EC is used only for scope; corroborator handles are admission/source planning only.

## Result

- Candidate families ranked: 12.
- Ready existing lanes with >=150 projected clean admits: 0.
- High-yield lanes blocked by new fingerprint/rule/preregistration: 4.
- Existing lanes blocked by <150 cap room: 2.
- Combined label surface: 7564.
- Combined seed-fingerprint surface: 5868.
- Remaining gap to 10k seed surface: 4132.

## Ranking

| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | had_like_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 4457 | 3477 | 0.78 | 150 | 150 | chemistry_confusable_cap_150 |
| 2 | aldehyde_dehydrogenase | blocked_new_fingerprint_oos_prereg_and_rule_required | 3160 | 3153 | 0.998 | 150 | 150 | chemistry_confusable_cap_150 |
| 3 | alpha_beta_hydrolase_esterase_lipase | blocked_new_fingerprint_oos_prereg_and_rule_required | 6160 | 1352 | 0.219 | 150 | 150 | chemistry_confusable_cap_150 |
| 4 | ser_thr_protein_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 1142 | 943 | 0.826 | 150 | 150 | chemistry_confusable_cap_150 |
| 5 | short_chain_dehydrogenase_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 241 | 0.031 | 84 | 150 | chemistry_confusable_cap_150 |
| 6 | terpene_cyclase_synthase | blocked_existing_cap_room_below_150 | 2335 | 2315 | 0.991 | 77 | 77 | clean_nonconfusable_cap_250 |
| 7 | serine_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 156 | 0.862 | 70 | 150 | chemistry_confusable_cap_150 |
| 8 | aminoglycoside_phosphotransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 14226 | 153 | 0.011 | 61 | 150 | chemistry_confusable_cap_150 |
| 9 | protein_kinase_ser_thr_tyr | blocked_existing_cap_room_below_150 | 5117 | 3470 | 0.678 | 50 | 50 | chemistry_confusable_cap_150 |
| 10 | aldo_keto_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 125 | 0.016 | 44 | 150 | chemistry_confusable_cap_150 |
| 11 | aminoglycoside_acetyltransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 9981 | 84 | 0.008 | 34 | 150 | chemistry_confusable_cap_150 |
| 12 | metallo_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 37 | 0.204 | 17 | 150 | chemistry_confusable_cap_150 |

## Top Lane Requirements

### had_like_phosphatase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: HAD family/domain/name handle; Asp nucleophile or Mg binding-site evidence; Rhea phosphomonoester hydrolysis equation where available.
- Holds: protein phosphatase rows; metal phosphomonoesterase rows with no HAD signal; phosphodiesterase/nuclease side rows.
- Rationale: Large phosphatase lane; only useful at scale after a HAD-specific split separates Asp-phosphoenzyme chemistry from metal phosphatases.

### aldehyde_dehydrogenase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: aldehyde dehydrogenase family/name handle; NAD(P) cosubstrate participant or binding-site context; catalytic Cys/Glu active-site evidence where available.
- Holds: molybdopterin aldehyde oxidoreductase rows; flavin aldehyde oxidase rows; generic NAD(P) dehydrogenase rows without ALDH signal.
- Rationale: Cys-thiohemiacetal hydride-transfer mechanism; a clean split is needed from generic NAD(P) and Mo/flavin aldehyde oxidoreductases.

### alpha_beta_hydrolase_esterase_lipase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: Ser-His-Asp/Glu catalytic triad active-site or binding-site evidence; esterase/lipase family keyword or protein-name handle; Rhea ester hydrolysis participant/equation where available.
- Holds: protease/amidase rows; glycoside hydrolase/transglycosylase rows; metal hydrolase rows; EC-only rows without active-site or family corroboration.
- Rationale: High-supply hydrolytic family but confusable with existing ser-his and metal hydrolase lanes; requires a split before import.

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

## Guardrails

- Registry written: False.
- Labels created: False.
- EC scope-only / never predictive: True.
- Future labels must be bronze / automation_curated in the uniprot namespace.
- Dedup against current702 and external bronze is required before apply.

## Next action

- No existing lane has >=150 cap room. Build the `had_like_phosphatase` fingerprint/source runner first: ontology node, mechanism disambiguation rule, OOS preregistration, row guardrail audit, preview, tests, then apply only if gates pass.
