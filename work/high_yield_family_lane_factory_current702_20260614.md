# High-Yield Family Lane Factory Scout

Run: 2026-06-14T01:09:00Z

Non-destructive scout/factory artifact. No labels or registries were written.
EC is used only for scope; corroborator handles are admission/source planning only.

## Result

- Candidate families ranked: 12.
- Ready existing lanes with >=150 projected clean admits: 0.
- High-yield lanes blocked by new fingerprint/rule/preregistration: 8.
- Existing lanes blocked by <150 cap room: 0.
- Combined label surface: 7742.
- Combined seed-fingerprint surface: 6046.
- Remaining gap to 10k seed surface: 3954.

## Ranking

| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | terpene_cyclase_synthase | blocked_new_fingerprint_oos_prereg_and_rule_required | 2335 | 2315 | 0.991 | 250 | 250 | clean_nonconfusable_cap_250 |
| 2 | short_chain_dehydrogenase_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 7709 | 0.988 | 150 | 150 | chemistry_confusable_cap_150 |
| 3 | aldo_keto_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 4147 | 0.531 | 150 | 150 | chemistry_confusable_cap_150 |
| 4 | had_like_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 4457 | 3477 | 0.78 | 150 | 150 | chemistry_confusable_cap_150 |
| 5 | protein_kinase_ser_thr_tyr | blocked_new_fingerprint_oos_prereg_and_rule_required | 5117 | 3470 | 0.678 | 150 | 150 | chemistry_confusable_cap_150 |
| 6 | aldehyde_dehydrogenase | blocked_new_fingerprint_oos_prereg_and_rule_required | 3160 | 3153 | 0.998 | 150 | 150 | chemistry_confusable_cap_150 |
| 7 | alpha_beta_hydrolase_esterase_lipase | blocked_new_fingerprint_oos_prereg_and_rule_required | 6160 | 1352 | 0.219 | 150 | 150 | chemistry_confusable_cap_150 |
| 8 | ser_thr_protein_phosphatase | blocked_new_fingerprint_oos_prereg_and_rule_required | 1142 | 943 | 0.826 | 150 | 150 | chemistry_confusable_cap_150 |
| 9 | serine_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 156 | 0.862 | 70 | 150 | chemistry_confusable_cap_150 |
| 10 | aminoglycoside_phosphotransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 14226 | 153 | 0.011 | 61 | 150 | chemistry_confusable_cap_150 |
| 11 | aminoglycoside_acetyltransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 9981 | 84 | 0.008 | 34 | 150 | chemistry_confusable_cap_150 |
| 12 | metallo_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 37 | 0.204 | 17 | 150 | chemistry_confusable_cap_150 |

## Top Lane Requirements

### terpene_cyclase_synthase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: terpene/cyclase functional keyword or protein-name handle; Mg/Mn diphosphate-binding handle or active-site metal context; Rhea reaction participant showing diphosphate release/cyclization where available.
- Holds: prenyltransferase chain-extension rows; lyase/hydratase rows without terpene cyclization evidence; multi-fingerprint metal-lyase signal rows.
- Rationale: Clean carbocation cyclization chemistry outside the current atlas; prefer reviewed EC 4.2.3 rows with metal/diphosphate corroboration.

### short_chain_dehydrogenase_reductase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: SDR family/name/domain handle; NAD(P) participant or Rossmann binding-site context; Ser-Tyr-Lys/Asn active-site evidence where available.
- Holds: AKR rows; zinc medium-chain alcohol dehydrogenase rows; flavin/metal redox rows.
- Rationale: Very large hydride-transfer family, but current source handles are weak; requires an SDR-specific rule instead of broad EC 1.1.1 padding.

### aldo_keto_reductase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: aldo-keto reductase family/name handle; NADP/NADPH cosubstrate participant or binding-site context; active-site Tyr/Lys/Asp catalytic tetrad evidence where available.
- Holds: short-chain dehydrogenase/reductase rows; medium-chain zinc alcohol dehydrogenase rows; flavin/metal redox rows.
- Rationale: Large NAD(P) hydride-transfer subclass; needs AKR-vs-SDR/MDR rules because the existing NAD(P) fingerprint is capped.

### had_like_phosphatase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: HAD family/domain/name handle; Asp nucleophile or Mg binding-site evidence; Rhea phosphomonoester hydrolysis equation where available.
- Holds: protein phosphatase rows; metal phosphomonoesterase rows with no HAD signal; phosphodiesterase/nuclease side rows.
- Rationale: Large phosphatase lane; only useful at scale after a HAD-specific split separates Asp-phosphoenzyme chemistry from metal phosphatases.

### protein_kinase_ser_thr_tyr
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Required non-EC corroborators: protein kinase family/name/domain handle; ATP/Mg binding-site or cofactor/cosubstrate context; protein-substrate phosphorylation Rhea equation where available.
- Holds: small-molecule kinase rows; histidine kinase/two-component rows; ATPase or ligase rows.
- Rationale: Massive ATP/Mg phosphoryl-transfer family; only useful after a protein-substrate kinase split and explicit histidine-kinase holds.

## Guardrails

- Registry written: False.
- Labels created: False.
- EC scope-only / never predictive: True.
- Future labels must be bronze / automation_curated in the uniprot namespace.
- Dedup against current702 and external bronze is required before apply.

## Next action

- No existing lane has >=150 cap room. Build the `terpene_cyclase_synthase` fingerprint/source runner first: ontology node, mechanism disambiguation rule, OOS preregistration, row guardrail audit, preview, tests, then apply only if gates pass.
