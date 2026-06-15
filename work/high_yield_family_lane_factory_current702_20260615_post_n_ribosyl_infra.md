# High-Yield Family Lane Factory Scout

Run: 2026-06-15T16:08:05Z

Non-destructive scout/factory artifact. No labels or registries were written.
EC is used only for scope; corroborator handles are admission/source planning only.

## Result

- Candidate families ranked: 14.
- Ready existing lanes with >=150 projected clean admits: 1.
- High-yield lanes blocked by new fingerprint/preregistration/runner/rule infrastructure: 1.
- Existing lanes blocked by <150 cap room: 6.
- Combined label surface: 8122.
- Combined seed-fingerprint surface: 6426.
- Remaining gap to 10k seed surface: 3574.

## Ranking

| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | n_ribosyl_hydrolase | ready_for_preview_not_apply | 1991 | 1991 | 1.0 | 150 | 150 | chemistry_confusable_cap_150 |
| 2 | metal_independent_phosphodiesterase | blocked_new_fingerprint_oos_prereg_and_runner_required | 2726 | 1129 | 0.414 | 150 | 150 | chemistry_confusable_cap_150 |
| 3 | short_chain_dehydrogenase_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 241 | 0.031 | 84 | 150 | chemistry_confusable_cap_150 |
| 4 | terpene_cyclase_synthase | blocked_existing_cap_room_below_150 | 2335 | 2315 | 0.991 | 77 | 77 | clean_nonconfusable_cap_250 |
| 5 | serine_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 156 | 0.862 | 70 | 150 | chemistry_confusable_cap_150 |
| 6 | aminoglycoside_phosphotransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 14226 | 153 | 0.011 | 61 | 150 | chemistry_confusable_cap_150 |
| 7 | protein_kinase_ser_thr_tyr | blocked_existing_cap_room_below_150 | 5117 | 3470 | 0.678 | 50 | 50 | chemistry_confusable_cap_150 |
| 8 | aldo_keto_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 125 | 0.016 | 44 | 150 | chemistry_confusable_cap_150 |
| 9 | ser_thr_protein_phosphatase | blocked_existing_cap_room_below_150 | 1142 | 943 | 0.826 | 38 | 38 | chemistry_confusable_cap_150 |
| 10 | aminoglycoside_acetyltransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 9981 | 84 | 0.008 | 34 | 150 | chemistry_confusable_cap_150 |
| 11 | metallo_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 37 | 0.204 | 17 | 150 | chemistry_confusable_cap_150 |
| 12 | had_like_phosphatase | blocked_existing_cap_room_below_150 | 4457 | 3477 | 0.78 | 4 | 4 | chemistry_confusable_cap_150 |
| 13 | aldehyde_dehydrogenase | blocked_existing_cap_room_below_150 | 3160 | 3153 | 0.998 | 0 | 0 | chemistry_confusable_cap_150 |
| 14 | alpha_beta_hydrolase_esterase_lipase | blocked_existing_cap_room_below_150 | 6160 | 1352 | 0.219 | 0 | 0 | chemistry_confusable_cap_150 |

## Top Lane Requirements

### n_ribosyl_hydrolase
- Status: ready_for_preview_not_apply.
- Source-wall rule status: implemented_preview_only.
- Required non-EC corroborators: nucleoside hydrolase, N-ribosylhydrolase, or N-ribosidase family/name handle; Rhea N-glycosidic bond hydrolysis reaction with ribose/deoxyribose product; active-site acid/base or ribose/base-binding residue evidence where available.
- Holds: O-glycosidase/glycoside hydrolase rows; nucleoside phosphorylase phosphorolysis rows; nucleoside kinase or nucleotidyltransferase side rows; EC-only rows without N-ribosyl hydrolysis corroboration.
- Rationale: Discovery-compass ontology gap: N-glycosidic bond hydrolysis is distinct from O-glycoside hydrolase, kinase, and phosphorylase chemistry.

### metal_independent_phosphodiesterase
- Status: blocked_new_fingerprint_oos_prereg_and_runner_required.
- Source-wall rule status: implemented_preview_only.
- Required non-EC corroborators: phosphodiesterase/nuclease/phospholipase family or protein-name handle; Rhea phosphodiester or cyclic-nucleotide P-O cleavage reaction where available; active-site acid/base or substrate-binding evidence independent of EC scope.
- Holds: metal-dependent phosphodiesterase/nuclease rows; phosphomonoesterase and protein phosphatase rows; phospholipase C lyase rows without hydrolytic phosphodiester cleavage; EC-only rows without family, active-site, binding-site, or Rhea corroboration.
- Rationale: Discovery-compass ontology gap: phosphodiester P-O cleavage without the two-metal architecture covered by the existing metal phosphoesterase family.

### short_chain_dehydrogenase_reductase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Source-wall rule status: not_implemented.
- Required non-EC corroborators: SDR family/name/domain handle; NAD(P) participant or Rossmann binding-site context; Ser-Tyr-Lys/Asn active-site evidence where available.
- Holds: AKR rows; zinc medium-chain alcohol dehydrogenase rows; flavin/metal redox rows.
- Rationale: Very large hydride-transfer family, but current source handles are weak; requires an SDR-specific rule instead of broad EC 1.1.1 padding.

### terpene_cyclase_synthase
- Status: blocked_existing_cap_room_below_150.
- Source-wall rule status: implemented_existing_fingerprint.
- Required non-EC corroborators: terpene/cyclase functional keyword or protein-name handle; Mg/Mn diphosphate-binding handle or active-site metal context; Rhea reaction participant showing diphosphate release/cyclization where available.
- Holds: prenyltransferase chain-extension rows; lyase/hydratase rows without terpene cyclization evidence; multi-fingerprint metal-lyase signal rows.
- Rationale: Clean carbocation cyclization chemistry outside the current atlas; prefer reviewed EC 4.2.3 rows with metal/diphosphate corroboration.

### serine_beta_lactamase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Source-wall rule status: not_implemented.
- Required non-EC corroborators: beta-lactamase keyword/name handle; active-site Ser/Lys/Glu beta-lactamase motif evidence; Rhea beta-lactam hydrolysis equation where available.
- Holds: metallo-beta-lactamase zinc rows; general amidohydrolase rows; resistance proteins without catalytic beta-lactamase evidence.
- Rationale: Resistance-relevant covalent acyl-enzyme hydrolase split; keep separate from zinc metallo-beta-lactamases and generic amidohydrolases.

## Guardrails

- Registry written: False.
- Labels created: False.
- EC scope-only / never predictive: True.
- Future labels must be bronze / automation_curated in the uniprot namespace.
- Dedup against current702 and external bronze is required before apply.

## Next action

- Run non-destructive previews for ready existing-runner lanes in ranking order; apply only after trust-tier, novelty, cap, dedup, and leakage gates pass.
