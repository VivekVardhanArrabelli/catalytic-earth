# High-Yield Family Lane Factory Scout

Run: 2026-06-16T00:15:32Z

Non-destructive scout/factory artifact. No labels or registries were written.
EC is used only for scope; corroborator handles are admission/source planning only.

## Result

- Candidate families ranked: 14.
- Ready existing lanes with >=150 projected clean admits: 0.
- High-yield lanes blocked by new fingerprint/preregistration/runner/rule infrastructure: 0.
- Existing lanes blocked by <150 cap room: 9.
- Combined label surface: 8522.
- Combined seed-fingerprint surface: 6826.
- Remaining gap to 10k seed surface: 3174.

## Ranking

| Rank | Family | status | scope supply | non-EC corroborated supply | corr. rate | projected clean admits | cap room | cap class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | terpene_cyclase_synthase | blocked_existing_cap_room_below_150 | 2335 | 2315 | 0.991 | 77 | 77 | clean_nonconfusable_cap_250 |
| 2 | serine_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 156 | 0.862 | 70 | 150 | chemistry_confusable_cap_150 |
| 3 | protein_kinase_ser_thr_tyr | blocked_existing_cap_room_below_150 | 5117 | 3470 | 0.678 | 50 | 50 | chemistry_confusable_cap_150 |
| 4 | short_chain_dehydrogenase_reductase | blocked_existing_cap_room_below_150 | 7804 | 241 | 0.031 | 50 | 50 | chemistry_confusable_cap_150 |
| 5 | aldo_keto_reductase | blocked_new_fingerprint_oos_prereg_and_rule_required | 7804 | 125 | 0.016 | 44 | 150 | chemistry_confusable_cap_150 |
| 6 | ser_thr_protein_phosphatase | blocked_existing_cap_room_below_150 | 1142 | 943 | 0.826 | 38 | 38 | chemistry_confusable_cap_150 |
| 7 | metal_independent_phosphodiesterase | blocked_projected_clean_admits_below_150 | 2726 | 1129 | 0.414 | 34 | 150 | chemistry_confusable_cap_150 |
| 8 | aminoglycoside_acetyltransferase | blocked_new_fingerprint_oos_prereg_and_rule_required | 9981 | 84 | 0.008 | 34 | 150 | chemistry_confusable_cap_150 |
| 9 | metallo_beta_lactamase | blocked_new_fingerprint_oos_prereg_and_rule_required | 181 | 37 | 0.204 | 17 | 150 | chemistry_confusable_cap_150 |
| 10 | had_like_phosphatase | blocked_existing_cap_room_below_150 | 4457 | 3477 | 0.78 | 4 | 4 | chemistry_confusable_cap_150 |
| 11 | aldehyde_dehydrogenase | blocked_existing_cap_room_below_150 | 3160 | 3153 | 0.998 | 0 | 0 | chemistry_confusable_cap_150 |
| 12 | n_ribosyl_hydrolase | blocked_existing_cap_room_below_150 | 1991 | 1991 | 1.0 | 0 | 0 | chemistry_confusable_cap_150 |
| 13 | alpha_beta_hydrolase_esterase_lipase | blocked_existing_cap_room_below_150 | 6160 | 1352 | 0.219 | 0 | 0 | chemistry_confusable_cap_150 |
| 14 | aminoglycoside_phosphotransferase | blocked_existing_cap_room_below_150 | 18 | 18 | 1.0 | 0 | 0 | chemistry_confusable_cap_150 |

## Top Lane Requirements

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

### protein_kinase_ser_thr_tyr
- Status: blocked_existing_cap_room_below_150.
- Source-wall rule status: implemented_existing_fingerprint.
- Required non-EC corroborators: protein kinase family/name/domain handle; ATP/Mg binding-site or cofactor/cosubstrate context; protein-substrate phosphorylation Rhea equation where available.
- Holds: small-molecule kinase rows; histidine kinase/two-component rows; ATPase or ligase rows.
- Rationale: Massive ATP/Mg phosphoryl-transfer family; only useful after a protein-substrate kinase split and explicit histidine-kinase holds.

### short_chain_dehydrogenase_reductase
- Status: blocked_existing_cap_room_below_150.
- Source-wall rule status: implemented_existing_fingerprint_runner_subscale_preview.
- Required non-EC corroborators: SDR family/name/domain handle; NAD(P) participant or Rossmann binding-site context; Ser-Tyr-Lys/Asn active-site evidence where available.
- Holds: AKR rows; zinc medium-chain alcohol dehydrogenase rows; flavin/metal redox rows.
- Rationale: Very large hydride-transfer family, but current source handles are weak; requires an SDR-specific rule instead of broad EC 1.1.1 padding.

### aldo_keto_reductase
- Status: blocked_new_fingerprint_oos_prereg_and_rule_required.
- Source-wall rule status: not_implemented.
- Required non-EC corroborators: aldo-keto reductase family/name handle; NADP/NADPH cosubstrate participant or binding-site context; active-site Tyr/Lys/Asp catalytic tetrad evidence where available.
- Holds: short-chain dehydrogenase/reductase rows; medium-chain zinc alcohol dehydrogenase rows; flavin/metal redox rows.
- Rationale: Large NAD(P) hydride-transfer subclass; needs AKR-vs-SDR/MDR rules because the existing NAD(P) fingerprint is capped.

## Guardrails

- Registry written: False.
- Labels created: False.
- EC scope-only / never predictive: True.
- Future labels must be bronze / automation_curated in the uniprot namespace.
- Dedup against current702 and external bronze is required before apply.

## Next action

- No candidate projects >=150 clean rows under current source handles; improve source handles or add external sources before registry mutation.
