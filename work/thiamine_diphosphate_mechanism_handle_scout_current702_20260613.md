# Thiamine Diphosphate Mechanism Handle Scout

- Status: non_destructive_mechanism_handle_scout_no_registry_write.
- Entries examined: 80; fetch failures: 0.
- Wire 25fp lane now: True.
- Reason: ThDP/Mg/Rhea/active-site handles are frequent enough for a guarded lane; overlap with PLP/Mo/oxidoreductase EC requires explicit boundary guards..

## Counts
- active_or_binding_site_context: 73
- flavin_boundary: 11
- keyword_or_family_text: 80
- kinase_hydrolase_boundary: 48
- likely_wireable: 65
- mg_context: 77
- not_likely_or_boundary: 15
- rhea_carbonyl_decarboxylation_or_transfer: 62
- rhea_cross_reference: 80
- side_ec_boundary: 15
- thdp_context: 80

## Guardrails
- EC 2.2.1/4.1.1/1.2.4 is scope-only and must stay in excluded_context.
- Counted mechanism axes must come from ThDP/Mg/cofactor or cosubstrate context, Rhea participant/reaction text, ThDP/transketolase/decarboxylase family text, or active-/binding-site handles.
- Hold PLP, molybdopterin, heme/flavin, kinase/phosphotransferase, hydrolase, side-EC, and multi-fingerprint signal rows.

## Sample rows
- P06169 | Pyruvate decarboxylase isozyme 1 (EC 4.1.1.-) (EC 4.1.1.43) (EC 4.1.1.72) (EC 4.1.1.74) (Thiamine pyrophosphate-dependent 2-oxo-acid decarboxylase) (2ODC) | EC ['4.1.1.-', '4.1.1.43', '4.1.1.72', '4.1.1.74'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
- P08559 | Pyruvate dehydrogenase E1 component subunit alpha, somatic form, mitochondrial (EC 1.2.4.1) (PDHE1-A type I) | EC ['1.2.4.1'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
- P11177 | Pyruvate dehydrogenase E1 component subunit beta, mitochondrial (PDHE1-B) (EC 1.2.4.1) | EC ['1.2.4.1'] | likely=True | evidence=['thdp_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
- P26263 | Pyruvate decarboxylase isozyme 3 (EC 4.1.1.-) (EC 4.1.1.43) (EC 4.1.1.72) (EC 4.1.1.74) (Thiamine pyrophosphate-dependent 2-oxo-acid decarboxylase) (2ODC) | EC ['4.1.1.-', '4.1.1.43', '4.1.1.72', '4.1.1.74'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
- P16467 | Pyruvate decarboxylase isozyme 2 (EC 4.1.1.-) (EC 4.1.1.43) (EC 4.1.1.72) (EC 4.1.1.74) (Thiamine pyrophosphate-dependent 2-oxo-acid decarboxylase) (2ODC) | EC ['4.1.1.-', '4.1.1.43', '4.1.1.72', '4.1.1.74'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
- P77488 | 1-deoxy-D-xylulose-5-phosphate synthase (EC 2.2.1.7) (1-deoxyxylulose-5-phosphate synthase) (DXP synthase) (DXPS) | EC ['2.2.1.7'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context', 'kinase_hydrolase_boundary']
- P17597 | Acetolactate synthase, chloroplastic (AtALS) (EC 2.2.1.6) (Acetohydroxy-acid synthase) (Protein CHLORSULFURON RESISTANT 1) | EC ['2.2.1.6'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context', 'flavin_boundary', 'kinase_hydrolase_boundary']
- Q07471 | Thiamine metabolism regulatory protein THI3 (EC 4.1.1.72) (Keto isocaproate decarboxylase 1) (Thiamine pyrophosphate-dependent 2-oxo-acid decarboxylase) (2ODC) | EC ['4.1.1.72'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text']
- Q06408 | Transaminated amino acid decarboxylase (EC 4.1.1.-) (EC 4.1.1.43) (EC 4.1.1.72) (EC 4.1.1.74) (EC 4.1.1.80) (Thiamine diphosphate-dependent phenylpyruvate decarboxylase) (PPDC) (Thiamine pyrophosphate-dependent 2-oxo-acid decarboxylase) (2ODC) (Transaminated branched-chain amino acid decarboxylase) | EC ['4.1.1.-', '4.1.1.43', '4.1.1.72', '4.1.1.74', '4.1.1.80'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text']
- Q96HY7 | 2-oxoadipate dehydrogenase complex component E1 (E1a) (OADC-E1) (OADH-E1) (EC 1.2.4.-) (2-oxoadipate dehydrogenase, mitochondrial) (Alpha-ketoadipate dehydrogenase) (Alpha-KADH-E1) (Dehydrogenase E1 and transketolase domain-containing protein 1) (Probable 2-oxoglutarate dehydrogenase E1 component DHKTD1, mitochondrial) | EC ['1.2.4.-'] | likely=True | evidence=['thdp_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text']
- P12694 | 2-oxoisovalerate dehydrogenase subunit alpha, mitochondrial (EC 1.2.4.4) (Branched-chain alpha-keto acid dehydrogenase E1 component alpha chain) (BCKDE1A) (BCKDH E1-alpha) | EC ['1.2.4.4'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
- Q02218 | 2-oxoglutarate dehydrogenase complex component E1 (E1o) (HsOGDH) (OGDC-E1) (OGDH-E1) (EC 1.2.4.2) (2-oxoglutarate dehydrogenase, mitochondrial) (Alpha-ketoglutarate dehydrogenase) (Alpha-KGDH-E1) (Thiamine diphosphate (ThDP)-dependent 2-oxoglutarate dehydrogenase) | EC ['1.2.4.2'] | likely=True | evidence=['thdp_context', 'mg_context', 'rhea_cross_reference', 'rhea_carbonyl_decarboxylation_or_transfer', 'keyword_or_family_text', 'active_or_binding_site_context']
