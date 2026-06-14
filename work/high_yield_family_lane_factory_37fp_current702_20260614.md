# High-Yield Family Lane Factory Scout

Run: 2026-06-14T02:43:26Z

Non-destructive scout/factory artifact. No labels or registries were written.
EC is used only for scope; corroborator handles are admission/source planning only.

## Result

- Candidate families ranked: 12.
- Ready existing lanes with >=150 projected clean admits: 1.
- High-yield lanes blocked by new fingerprint/rule/preregistration: 4.
- Existing lanes blocked by <150 cap room: 1.
- Combined label surface: 7915.
- Combined seed-fingerprint surface: 6219.
- Remaining gap to 10k seed surface: 3781.

## Ranking

| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | protein_kinase_ser_thr_tyr | ready_for_preview_not_apply | 5117 | 3470 | 0.678 | 150 | 150 | chemistry_confusable_cap_150 |
| 2 | had_like_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 4457 | 3477 | 0.78 | 150 | 150 | chemistry_confusable_cap_150 |
| 3 | aldehyde_dehydrogenase | blocked_new_fingerprint_oos_prereg_and_rule_required | 3160 | 3153 | 0.998 | 150 | 150 | chemistry_confusable_cap_150 |
| 4 | alpha_beta_hydrolase_esterase_lipase | blocked_new_fingerprint_oos_prereg_and_rule_required | 6160 | 1352 | 0.219 | 150 | 150 | chemistry_confusable_cap_150 |
| 5 | ser_thr_protein_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 1142 | 943 | 0.826 | 150 | 150 | chemistry_confusable_cap_150 |
| 6 | short_chain_dehydrogenase_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 241 | 0.031 | 84 | 150 | chemistry_confusable_cap_150 |
| 7 | terpene_cyclase_synthase | blocked_existing_cap_room_below_150 | 2335 | 2315 | 0.991 | 77 | 77 | clean_nonconfusable_cap_250 |
| 8 | serine_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 156 | 0.862 | 70 | 150 | chemistry_confusable_cap_150 |
| 9 | aminoglycoside_phosphotransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 14226 | 153 | 0.011 | 61 | 150 | chemistry_confusable_cap_150 |
| 10 | aldo_keto_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 125 | 0.016 | 44 | 150 | chemistry_confusable_cap_150 |
| 11 | aminoglycoside_acetyltransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 9981 | 84 | 0.008 | 34 | 150 | chemistry_confusable_cap_150 |
| 12 | metallo_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 37 | 0.204 | 17 | 150 | chemistry_confusable_cap_150 |

## Top Lane Requirements

### protein_kinase_ser_thr_tyr
- Status: ready_for_preview_not_apply.
- Required non-EC corroborators: protein kinase family/name/domain handle; ATP/Mg binding-site or cofactor/cosubstrate context; protein-substrate phosphorylation Rhea equation where available.
- Holds: small-molecule kinase rows; histidine kinase/two-component rows; ATPase or ligase rows.
- Rationale: Massive ATP/Mg phosphoryl-transfer family; only useful after a protein-substrate kinase split and explicit histidine-kinase holds.

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

## Guardrails

- Registry written: False.
- Labels created: False.
- EC scope-only / never predictive: True.
- Future labels must be bronze / automation_curated in the uniprot namespace.
- Dedup against current702 and external bronze is required before apply.

## Next action

- Run non-destructive previews for ready existing-runner lanes in ranking order; apply only after trust-tier, novelty, cap, dedup, and leakage gates pass.
