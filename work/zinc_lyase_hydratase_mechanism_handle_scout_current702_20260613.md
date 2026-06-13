# Zinc Lyase/Hydratase Mechanism Handle Scout

- Status: non_destructive_mechanism_handle_scout_no_registry_write.
- Entries examined: 80; fetch failures: 0.
- Wire 26fp lane now: True.
- Reason: Zinc/hydratase/Rhea/active-site handles appear frequent enough for guarded 26fp wiring..

## Counts
- active_binding_metal_site_context: 76
- boundary_keyword: 30
- likely_wireable: 50
- lyase_hydratase_text: 80
- not_likely_or_boundary: 30
- other_metal_boundary: 3
- rhea_cross_reference: 79
- rhea_hydration_elimination_or_carbonic_text: 79
- side_ec_boundary: 30
- zinc_context: 80

## Guardrails
- EC 4.2.1 is scope-only and must stay in excluded_context.
- Counted mechanism axes should come from zinc cofactor/site, Rhea hydration/elimination/carbonic reaction text, Lyase/hydratase keyword/domain, or active-/binding-/metal-site handles.
- Hold PLP, ThDP, hydrolase/transferase/aldolase/isomerase side rows, non-4.2.1 side ECs, and multi-fingerprint signals.

## Sample rows
- P13716 | Delta-aminolevulinic acid dehydratase (ALADH) (EC 4.2.1.24) (Porphobilinogen synthase) | EC ['4.2.1.24'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- Q96GX9 | Methylthioribulose-1-phosphate dehydratase (MTRu-1-P dehydratase) (EC 4.2.1.109) (APAF1-interacting protein) (hAPIP) | EC ['4.2.1.109'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- P00918 | Carbonic anhydrase 2 (EC 4.2.1.1) (Carbonate dehydratase II) (Carbonic anhydrase C) (CAC) (Carbonic anhydrase II) (CA-II) (Cyanamide hydratase CA2) (EC 4.2.1.69) | EC ['4.2.1.1', '4.2.1.69'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context', 'other_metal_boundary']
- Q9ULX7 | Carbonic anhydrase 14 (EC 4.2.1.1) (Carbonate dehydratase XIV) (Carbonic anhydrase XIV) (CA-XIV) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- P35218 | Carbonic anhydrase 5A, mitochondrial (EC 4.2.1.1) (Carbonate dehydratase VA) (Carbonic anhydrase VA) (CA-VA) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- P43166 | Carbonic anhydrase 7 (EC 4.2.1.1) (Carbonate dehydratase VII) (Carbonic anhydrase VII) (CA-VII) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- Q9Y2D0 | Carbonic anhydrase 5B, mitochondrial (EC 4.2.1.1) (Carbonate dehydratase VB) (Carbonic anhydrase VB) (CA-VB) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- O43570 | Carbonic anhydrase 12 (EC 4.2.1.1) (Carbonate dehydratase XII) (Carbonic anhydrase XII) (CA-XII) (Tumor antigen HOM-RCC-3.1.3) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- P23280 | Carbonic anhydrase 6 (EC 4.2.1.1) (Carbonate dehydratase VI) (Carbonic anhydrase VI) (CA-VI) (Salivary carbonic anhydrase) (Secreted carbonic anhydrase) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- Q16790 | Carbonic anhydrase 9 (EC 4.2.1.1) (Carbonate dehydratase IX) (Carbonic anhydrase IX) (CA-IX) (CAIX) (Membrane antigen MN) (P54/58N) (Renal cell carcinoma-associated antigen G250) (RCC-associated antigen G250) (pMW1) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- P00915 | Carbonic anhydrase 1 (EC 4.2.1.1) (Carbonate dehydratase I) (Carbonic anhydrase B) (CAB) (Carbonic anhydrase I) (CA-I) (Cyanamide hydratase CA1) (EC 4.2.1.69) | EC ['4.2.1.1', '4.2.1.69'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
- P22748 | Carbonic anhydrase 4 (EC 4.2.1.1) (Carbonate dehydratase IV) (Carbonic anhydrase IV) (CA-IV) | EC ['4.2.1.1'] | likely=True | evidence=['zinc_context', 'lyase_hydratase_text', 'rhea_cross_reference', 'rhea_hydration_elimination_or_carbonic_text', 'active_binding_metal_site_context']
