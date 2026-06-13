# PfkB/Biotin Alternate Source Scout

Generated: `2026-06-13T14:57:25Z`

Status: **source-supply scout only; no labels generated and no registry writes.**

Frozen current702 sha256: `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
Registry baseline: curated 702, external bronze 6238, known UniProt accessions 6241.

Guardrails: EC, names, Rhea IDs, keywords, and text handles in this scout are scope/admission handles only; EC is never a counted mechanism corroborator. Any future apply must still pass non-EC mechanism corroboration through `source_trust_tiers.evaluate_corroboration` and keep `predictive_evidence []`.

## Query Results

### biotin_raw_ec_6_4_1_without_biotin_handle

Family: `biotin_dependent_carboxylase`
Query: `(reviewed:true) AND (ec:6.4.1.*)`
Reason: Tests whether the current EC+biotin/name/cofactor lane missed reviewed EC 6.4.1 carboxylases because the biotin handle was too narrow. EC remains scope-only.
Future gate needed: Any future lane must still require non-EC mechanism evidence: biotin/carboxybiotin/cofactor handle, Rhea participant/equation, active/binding-site residue, or domain/structure corroboration.
UniProt reviewed total: **101**; sample size **25**; sample already labeled **22**; sample registry-new **3**.
Sample registry-new accessions: `P05166, Q8RM02, Q8RM03`.
Recommendation: **limited_supply_needs_manual_mechanism_review** - Sample has registry-new accessions, but total source supply is not clearly above prior lane coverage.

### biotin_raw_ec_6_3_4_carboxylase_name_no_biotin_handle

Family: `biotin_dependent_carboxylase`
Query: `(reviewed:true) AND (ec:6.3.4.*) AND (protein_name:carboxylase)`
Reason: Checks amidoligase/carboxylase supply without requiring a literal biotin keyword. EC/name are scope/admission handles only.
Future gate needed: Hold rows unless biotin-dependent carboxylase mechanism axes are present; avoid admitting generic ligases from EC alone.
UniProt reviewed total: **51**; sample size **25**; sample already labeled **17**; sample registry-new **8**.
Sample registry-new accessions: `P50747, P32528, Q9SL92, Q920N2, P06709, I6YFP0, P0CI75, P48445`.
Recommendation: **limited_supply_needs_manual_mechanism_review** - Sample has registry-new accessions, but total source supply is not clearly above prior lane coverage.

### biotin_floor_rhea_without_biotin_name_filter

Family: `biotin_dependent_carboxylase`
Query: `(reviewed:true) AND (rhea:11308 OR rhea:13501 OR rhea:13589 OR rhea:17701 OR rhea:18385 OR rhea:20425 OR rhea:20844 OR rhea:23720 OR rhea:28647 OR rhea:65292)`
Reason: Tests whether the floor-closure Rhea IDs have reviewed source supply outside the prior biotin/name/cofactor filter.
Future gate needed: Rhea IDs can support admission only with participant/equation context and another mechanism axis; EC is never counted.
UniProt reviewed total: **105**; sample size **25**; sample already labeled **19**; sample registry-new **6**.
Sample registry-new accessions: `Q8RM04, Q8RM02, Q8RM03, Q5P5G4, Q5P5G5, P05166`.
Recommendation: **limited_supply_needs_manual_mechanism_review** - Sample has registry-new accessions, but total source supply is not clearly above prior lane coverage.

### pfkb_existing_strict_reviewed_baseline

Family: `pfkb_ribokinase_family`
Query: `(reviewed:true) AND (ec:2.7.1.*) AND ((protein_name:"ribokinase" OR protein_name:"adenosine kinase" OR protein_name:"inosine kinase" OR protein_name:"1-phosphofructokinase" OR protein_name:"hydroxymethylpyrimidine kinase")) NOT ((ec:2.7.11.* OR ec:2.7.13.* OR ec:3.* OR ec:2.7.4.* OR protein_name:"protein kinase" OR protein_name:"histidine kinase" OR protein_name:"nucleoside diphosphate kinase" OR protein_name:"deoxynucleoside kinase" OR protein_name:"hexokinase" OR protein_name:"glucokinase" OR protein_name:"glycerol kinase" OR protein_name:"acetate kinase" OR protein_name:"homoserine kinase" OR protein_name:"mevalonate kinase" OR protein_name:"galactokinase" OR protein_name:"6-phosphofructokinase" OR protein_name:"ATP-dependent 6-phosphofructokinase"))`
Reason: Baseline current source path; expected exhausted at 46 admitted labels after duplicate/current-registry skips.
Future gate needed: Do not rerun for labels unless the upstream query or mechanism handles materially change.
UniProt reviewed total: **53**; sample size **25**; sample already labeled **22**; sample registry-new **3**.
Sample registry-new accessions: `Q5M731, O24767, O48881`.
Recommendation: **limited_supply_needs_manual_mechanism_review** - Sample has registry-new accessions, but total source supply is not clearly above prior lane coverage.

### pfkb_broad_names_without_ec_scope

Family: `pfkb_ribokinase_family`
Query: `(reviewed:true) AND ((protein_name:"ribokinase" OR protein_name:"adenosine kinase" OR protein_name:"inosine kinase" OR protein_name:"1-phosphofructokinase" OR protein_name:"hydroxymethylpyrimidine kinase")) NOT ((ec:2.7.11.* OR ec:2.7.13.* OR ec:3.* OR ec:2.7.4.* OR protein_name:"protein kinase" OR protein_name:"histidine kinase" OR protein_name:"nucleoside diphosphate kinase" OR protein_name:"deoxynucleoside kinase" OR protein_name:"hexokinase" OR protein_name:"glucokinase" OR protein_name:"glycerol kinase" OR protein_name:"acetate kinase" OR protein_name:"homoserine kinase" OR protein_name:"mevalonate kinase" OR protein_name:"galactokinase" OR protein_name:"6-phosphofructokinase" OR protein_name:"ATP-dependent 6-phosphofructokinase"))`
Reason: Looks for reviewed PfkB-like proteins with names but missing EC 2.7.1 annotations; name remains scope/admission only.
Future gate needed: A future lane must require ATP/ADP phosphoryl-transfer Rhea/participant context or active/binding-site/cofactor/domain mechanism axes before admission.
UniProt reviewed total: **53**; sample size **25**; sample already labeled **22**; sample registry-new **3**.
Sample registry-new accessions: `Q5M731, O24767, O48881`.
Recommendation: **limited_supply_needs_manual_mechanism_review** - Sample has registry-new accessions, but total source supply is not clearly above prior lane coverage.

### pfkb_specific_ecs_no_name_scope

Family: `pfkb_ribokinase_family`
Query: `(reviewed:true) AND ((ec:2.7.1.15) OR (ec:2.7.1.20) OR (ec:2.7.1.49) OR (ec:2.7.1.56) OR (ec:2.7.1.73)) NOT ((ec:2.7.11.* OR ec:2.7.13.* OR ec:3.* OR ec:2.7.4.* OR protein_name:"protein kinase" OR protein_name:"histidine kinase" OR protein_name:"nucleoside diphosphate kinase" OR protein_name:"deoxynucleoside kinase" OR protein_name:"hexokinase" OR protein_name:"glucokinase" OR protein_name:"glycerol kinase" OR protein_name:"acetate kinase" OR protein_name:"homoserine kinase" OR protein_name:"mevalonate kinase" OR protein_name:"galactokinase" OR protein_name:"6-phosphofructokinase" OR protein_name:"ATP-dependent 6-phosphofructokinase"))`
Reason: Tests whether strict PfkB EC subclasses have reviewed supply that does not match the current protein-name query. EC remains scope-only.
Future gate needed: Need non-EC corroboration before any label apply; this scout only estimates source supply.
UniProt reviewed total: **57**; sample size **25**; sample already labeled **18**; sample registry-new **7**.
Sample registry-new accessions: `O24767, Q5M731, C0SPC1, A0A0J9X285, O48881, A0A0H2ZQL5, Q2QWK9`.
Recommendation: **limited_supply_needs_manual_mechanism_review** - Sample has registry-new accessions, but total source supply is not clearly above prior lane coverage.

### pfkb_ribokinase_family_text_no_ec

Family: `pfkb_ribokinase_family`
Query: `(reviewed:true) AND (protein_name:"ribokinase family")`
Reason: Checks whether UniProt protein-name text exposes family-level PfkB rows not found by enzyme-specific names.
Future gate needed: Family text can be one mechanism axis only when paired with chemistry/Rhea/cofactor/site evidence; never predictive.
UniProt reviewed total: **0**; sample size **0**; sample already labeled **0**; sample registry-new **0**.
Recommendation: **not_a_new_supply_path** - First sample window is already represented or query is no broader than the exhausted lane.

## Next Concrete Action

Use the best `promising_*` query above to implement a non-destructive preview lane only if the sourcing code can add non-EC mechanism corroborator extraction. Do not admit scout rows directly. If no query is promising after manual sample inspection, select a new 10k-path fingerprint family instead of repeating the exhausted PfkB/biotin first-window probes.
