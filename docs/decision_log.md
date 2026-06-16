# Decision Log

This log records durable decisions that future agents should apply before
interpreting older artifacts. Dates are UTC artifact dates unless noted.

## 2026-06-16: PDE TIER-2 LOCAL-SLICE BATCH IS COUNTED BRONZE

Decision: `metal_independent_phosphodiesterase` is now a counted bronze fingerprint at the
100-row floor. The admitted rows use strict source-tier-2 GDPD/cyclic UniProt lanes as source and
admission evidence only. EC, names, source annotations, reaction text, and query handles remain
excluded context, never predictive features and never counted EC corroborators. Counted mechanism
axes are non-EC mechanism evidence such as cofactor/cosubstrate context, family/domain profile, and
Rhea reaction/participant pattern.

Implementation: stable local-slice previews at offsets **30/60/90** were combined with the prior
offset-0 GDPD/cyclic scout in
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_current702_20260616_run1302.json`.
The combined replay had **118** unique labels, admitted **116**, and throttled **2**. Preview
governor audit
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_governor_current702_20260616_run1302.json`
showed 116 rows would exceed the reaction-aware cap for a one-reaction tranche, so
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_reaction_cap_trimmed_preview_current702_20260616_run1302.json`
held **16** surplus rows and kept exactly **100**. Row audit
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_reaction_cap_trimmed_row_guardrail_audit_current702_20260616_run1302.json`
found **0** problems.

Apply result: explicit reuse-preview apply appended the reaction-cap-trimmed PDE batch to the
external registry only. A registry audit then found the 16 reaction-cap-held accessions present;
correction artifact
`artifacts/v3_metal_independent_phosphodiesterase_reaction_cap_surplus_registry_correction_current702_20260616_run1302.json`
removed only those surplus rows. Final external rows are **8026**, final PDE rows are **100**, and
frozen current702 remains byte-unchanged at sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Post-apply decision: no positive holes remain. Post-apply coverage
`artifacts/v3_coverage_redundancy_audit_current702_20260616_run1302_post_pde_apply.json` reports
combined labels **8728**, floor deficit **0**, Gini **0.1779**, and only
`metal_dependent_hydrolase` over cap. Do not pad PDE or reaction-saturated/balanced lanes; the next
mutation needs a new high-yield source-handle/source-tier strategy through the same gates.

## 2026-06-16: PDE HYDROLASE LANE IS ALLOWED BUT SUBFLOOR

Decision: `metal_independent_phosphodiesterase` may use the reviewed EC 3.1.4 + Hydrolase lane as
a source/fetch split only. EC and keyword evidence remain excluded context, never predictive
features and never counted mechanism corroborators. The lane is not apply authority unless the
usual dedup, source-trust, novelty, cap/floor, row-guardrail, and leakage/source-contract gates
also pass.

Implementation: added `metal_independent_pde_ec_3_1_4_hydrolase_non_metal`,
`metal_independent_pde_ec_3_1_4_actsite_catalytic_non_metal`, and stricter tier-2 GDPD/cyclic
source splits to `src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py`, offline
guarded-lane tests in `tests/test_metal_independent_phosphodiesterase_sourcing.py`, and reusable
preview row guardrails in `src/catalytic_earth/bronze_preview_row_guardrails.py` with
`scripts/audit_bronze_preview_row_guardrails.py`.

Measured result: the reviewed Hydrolase preview
`artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_preview_window0_120_current702_20260616_run0114.json`
fetched **120** rows, admitted **17** target PDE labels, held **22** off-target rows, and held
**69** rows for missing mechanism corroboration. Row audit
`artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_row_guardrail_audit_current702_20260616_run0114.json`
found **0** problems. Strict tier-2 sample
`artifacts/v3_metal_independent_phosphodiesterase_tier2_preview_size20_current702_20260616_run1209.json`
fetched **40** rows and admitted **0** target PDE labels.

Follow-up strict tier-2 GDPD/cyclic preview
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_size30_current702_20260616_run1235.json`
fetched **60** rows, admitted **28** target PDE labels, held **32** rows for missing mechanism
corroboration, and held **0** off-target rows. Row audit
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_row_guardrail_audit_current702_20260616_run1235.json`
found **0** problems.

Reviewed ACT_SITE+catalytic preview
`artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_preview_size40_current702_20260616_run1218.json`
fetched **40** rows, admitted **2** target PDE labels, held **4** off-target rows, and held
**23** rows for missing mechanism corroboration. Row audit
`artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_row_guardrail_audit_current702_20260616_run1218.json`
found **0** problems.

Decision: no registry mutation is authorized from these previews. Applying 17, 2, or 28 rows would
leave PDE below the 100-row floor, so each is a tiny topup rather than a floor-closing batch. The
next mutation needs a sharper PDE source wall or a beyond-reviewed source-tier expansion through
the full gated path.

Safety recovery: a stale worker from the dead prior automation briefly appended the **17** Hydrolase
rows to the external registry. That append was reverted before commit; the external registry is
back to **7926** rows and frozen current702 stayed unchanged.

Follow-up count scout
`artifacts/v3_metal_independent_phosphodiesterase_sharp_handle_count_scout_current702_20260616_run1207.json`
shows no obvious reviewed-source rescue: broad Hydrolase has **490** raw rows but already previewed
to **17** admits, while the best sharper non-baseline handle `actsite_catalytic_non_metal` has
only **119** raw rows before disambiguation/novelty. Do not rerun these reviewed PDE windows for
apply without a genuinely new mechanism-bearing source wall.

## 2026-06-16: SBL IS A GUARDED 46TH FINGERPRINT AND COUNTED BRONZE

Decision: add `serine_beta_lactamase` as the 46th positive fingerprint and keep the source wall
mechanism-first. EC 3.5.2.6 may scope/fetch candidate rows but is never a counted corroborator.
Serine-beta-lactamase names, active-site handles, UniProt prose, reaction text, and query handles
remain excluded context. Counted corroboration comes from non-EC mechanism axes:
serine-beta-lactamase family/domain context, beta-lactam hydrolysis reaction/participant evidence,
and Ser/Lys/Glu active-site context. Metallo/zinc beta-lactamases, PBPs/DD-peptidases,
beta-lactam synthases, generic amidohydrolases, side-EC, EC-only, and multi-fingerprint rows stay
held, and `predictive_evidence` remains empty.

Implementation: added `src/catalytic_earth/serine_beta_lactamase_sourcing.py`,
`scripts/source_serine_beta_lactamase_family.py`, the `serine_beta_lactamase` fingerprint,
ontology family `serine_acyl_enzyme_beta_lactam_hydrolysis`, deploy context
`ser_lys_glu_beta_lactam_acyl_enzyme_hydrolysis_context`, disambiguation/source-trust rules,
high-yield factory wiring, focused tests, and the 46fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_46fp_1025.json`. Updated the
current positive-fingerprint universe to `label_factory_v1_46fp`; frozen current702 labels stay
stamped with their historical decision version and were not written. Added a source-free
`bc_beta_lactam_hydrolysis` bond-change class so representation-loop audits separate SBL from
generic ester/Ser-His hydrolase chemistry without reading EC/name/prose/lane context.

Measured result: non-destructive preview
`artifacts/v3_serine_beta_lactamase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260616_run0014.json`
fetched **240** unreviewed tier-2 rows, produced **115** target mechanism-corroborated labels,
admitted **106** novelty-safe labels, held **0** off-target fingerprint matches, and reached the
**100** floor. Row audit
`artifacts/v3_serine_beta_lactamase_tier2_row_guardrail_audit_current702_20260616_run0014.json`
checked all **106** admitted rows with **0** problems. Explicit reuse-preview apply appended
**106** bronze SBL rows to the external registry, skipped **0** duplicates, changed external rows
**7820 -> 7926**, and changed combined label surface **8522 -> 8628**. Frozen current702 sha stayed
`5eec9bef...` before and after apply.

Decision: SBL reaches the floor at **106** rows and must not be padded without a new
reaction-diversity split. Post-apply coverage still shows `metal_independent_phosphodiesterase` as
the lone remaining hole/under-floor fingerprint. The high-yield factory has **0** ready existing
lanes >=150; top projected clean supply is **77** under current handles. Evidence-handle and
breadth-feasibility scouts are strategy inputs only, not apply authority. The next mutation should
build a sharper PDE source wall beyond EC/name counts or pursue a source-tier expansion beyond
reviewed Swiss-Prot through the full gated path.

## 2026-06-15: PDE PHOSPHOLIPASE-D SPLIT IS ALLOWED BUT SUBFLOOR

Decision: the `metal_independent_phosphodiesterase` source wall may count phospholipase-D family
context as admission evidence only when paired with explicit hydrolytic phosphodiester reaction
participants. EC 3.1.4 scopes/fetches rows only and is never counted. Protein names, UniProt prose,
and reaction text stay in excluded context, not predictive evidence. Phospholipase C remains a
boundary hold, metal-dependent phosphodiesterase/nuclease rows remain off-target/held, and
`predictive_evidence` remains empty.

Implementation: extended the PDE disambiguation tokens for `phospholipase D` and PLD reaction
participants (`phosphocholine`, phosphoethanolamide/glycosylinositol, and
glycero-3-phosphate), added the `metal_independent_pde_phospholipase_d_non_metal` source lane in
`src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py`, and added focused tests for
PLD admission plus phospholipase-C boundary hold. Also added per-fetch timeout support to
`scripts/source_terpene_cyclase_synthase_family.py` and fetcher pass-through in the terpene
sourcing writer so bounded cap-close previews can fail safely instead of hanging.

Measured result: PLD preview
`artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_preview_current702_20260615_run2314.json`
fetched **22** reviewed rows, produced **7** target mechanism-corroborated labels, admitted **7**
novelty-safe rows, and held **4** off-target metallophosphoesterase/nuclease rows. Row audit
`artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_row_guardrail_audit_current702_20260615_run2314.json`
found **0** problems. This is subfloor and must not be applied. Terpene cap-close window
`artifacts/v3_terpene_cyclase_synthase_capclose_window170_preview_current702_20260615_run2314.json`
fetched **138** rows but admitted **0** novelty-safe rows, so no cap-close apply was available.

Decision: no registry mutation is authorized from this run's PLD or terpene previews. PDE remains
the only hole. Do not retry the same broad PDE EC/name handles, the 7-row PLD preview, or terpene
window170 for apply. The next mutation needs a sharper mechanism-bearing PDE source split or a new
high-yield family/source-tier strategy through the full gated path.

## 2026-06-15: SDR IS A GUARDED 45TH FINGERPRINT AND COUNTED BRONZE

Decision: add `short_chain_dehydrogenase_reductase` as the 45th positive fingerprint and keep the
source wall mechanism-first. EC 1.1.1 may scope/fetch candidate rows but is never a counted
corroborator. SDR family/name/source handles and UniProt prose remain excluded context. Counted
corroboration comes from non-EC mechanism axes: SDR family/domain, NAD(P) cosubstrate, Rhea redox
reaction/participant, and active/binding-site context when present. AKR/MDR/ALDH/flavin/metal
redox boundary rows stay held, and `predictive_evidence` remains empty.

Implementation: added `src/catalytic_earth/short_chain_dehydrogenase_reductase_sourcing.py`,
`scripts/source_short_chain_dehydrogenase_reductase_family.py`, the
`short_chain_dehydrogenase_reductase` fingerprint, ontology family
`sdr_nicotinamide_hydride_transfer`, deploy context
`nad_p_sdr_ser_tyr_lys_hydride_transfer_context`, disambiguation/source-trust rules, high-yield
factory wiring, focused tests, and the 45fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_45fp_1025.json`. Updated the
current positive-fingerprint universe to `label_factory_v1_45fp`; frozen current702 labels stay
stamped with their historical decision version and were not written.

Measured result: non-destructive preview
`artifacts/v3_short_chain_dehydrogenase_reductase_sourcing_preview_named220_current702_20260615_run2213.json`
fetched **220** reviewed rows, produced **103** target mechanism-corroborated labels, admitted
**100** novelty-safe labels, held **0** off-target rows, and reached the **100** floor. Row audit
`artifacts/v3_short_chain_dehydrogenase_reductase_row_guardrail_audit_current702_20260615_run2213.json`
checked all **100** admitted rows with **0** problems. Explicit reuse-preview apply appended
**100** bronze SDR rows to the external registry, skipped **0** duplicates, changed external rows
**7720 -> 7820**, and changed combined label surface **8422 -> 8522**. Frozen current702 sha stayed
`5eec9bef...` before and after apply.

Decision: SDR is floor-closed at **100** rows and must not be padded without a fresh source split.
Post-apply coverage still shows `metal_independent_phosphodiesterase` as the lone remaining
hole/under-floor fingerprint. Representation loop remains leakage-safe; SDR is separable, but
generic `nad_p_dehydrogenase` is now reaction-chemistry-confusable with SDR under source-free
features. Do not repair that by injecting EC/name/prose/lane-derived predictors. The next mutation
should build a sharper PDE source wall beyond EC/name counts or pursue a new high-yield
family/source-tier strategy through the full gated path.

## 2026-06-15: APH TIER-2 SOURCE-HANDLE BATCH IS COUNTED BRONZE

Decision: APH unreviewed tier-2 source-handle expansion is allowed only as guarded bronze admission
evidence, with stricter trust requirements than reviewed Swiss-Prot. EC may scope/fetch candidate
rows but is never counted as mechanism evidence. Source tier 2 APH rows require at least three
independent non-EC mechanism axes; for the applied batch every row had active/binding-site,
cofactor/cosubstrate, family/domain, and Rhea/reaction-participant evidence. Protein names, EC,
query handles, reaction text, and prose remain excluded context, and `predictive_evidence` remains
empty.

Implementation: extended `src/catalytic_earth/aminoglycoside_phosphotransferase_sourcing.py` and
`scripts/source_aminoglycoside_phosphotransferase_family.py` with fail-closed unreviewed tier-2
lane switches and `source_tier` plumbing into `source_trust_tiers.evaluate_corroboration`. Added
focused tests proving tier-2 APH requires `source_tier_2`, has at least three non-EC mechanism
axes, keeps EC out of counted corroboration, and leaves predictive evidence empty.

Measured result: non-destructive preview
`artifacts/v3_aminoglycoside_phosphotransferase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260615.json`
fetched **240** rows, produced **239** target mechanism-corroborated labels, admitted **150**
novelty-safe labels, held **19** by novelty replay, and held **70** more at the APH cap. Row audit
`artifacts/v3_aminoglycoside_phosphotransferase_tier2_row_guardrail_audit_current702_20260615.json`
checked all **150** admitted rows with **0** problems. Explicit reuse-preview apply appended
**150** bronze APH rows to the external registry, skipped **0** duplicates, changed external rows
**7570 -> 7720**, and changed combined label surface **8272 -> 8422**. Frozen current702 sha stayed
`5eec9bef...` before and after apply.

Decision: APH is now closed at the 150 cap and must not be padded further. Post-apply coverage
shows `metal_independent_phosphodiesterase` as the lone remaining hole/under-floor fingerprint.
Prior PDE previews remain below gate (**14** reviewed admits; **0** tier-2 admits), and post-APH
exact-EC distribution scout
`artifacts/v3_metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.json`
shows exact cyclic-nucleotide PDE splits are also too small after the non-metal filter. The next
mutation must not reuse those handles blindly. Build a new mechanism-bearing PDE source wall beyond
EC/name counts, or a new high-yield family/source-tier strategy, through the full gated path before
any apply.

## 2026-06-15: APH IS A GUARDED 44TH FINGERPRINT, BUT NOT APPLIED

Decision: add `aminoglycoside_phosphotransferase` as the 44th positive fingerprint and keep the
source wall mechanism-first. EC may scope/fetch candidate rows but is never a counted corroborator.
Counted corroboration requires APH family/name context plus mechanism-bearing active/binding-site,
ATP/Mg, or aminoglycoside phosphorylation evidence. Protein kinase, small-molecule kinase,
aminoglycoside acetyltransferase/nucleotidyltransferase, side-EC, EC-only, and multi-fingerprint
rows stay held.

Important correction: the initial high-yield scout hypothesis that EC `2.7.1.130` and
`2.7.1.192` were APH exact scopes was false. Live reviewed UniProt search inspection showed those
surfaces are lipid-A kinase and PTS MurNAc phosphotransferase. The implemented APH scope is
restricted to reviewed aminoglycoside phosphotransferase/kinase ECs `2.7.1.95`, `2.7.1.72`,
`2.7.1.87`, `2.7.1.119`, and `2.7.1.163`.

Implementation: added `src/catalytic_earth/aminoglycoside_phosphotransferase_sourcing.py`,
`scripts/source_aminoglycoside_phosphotransferase_family.py`, the
`aminoglycoside_phosphotransferase` fingerprint, ontology family
`aminoglycoside_phosphoryl_transfer`, deploy context, coverage/governor signature, high-yield
factory wiring, focused tests, and the 44fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_44fp_1025.json`. Updated the
current positive-fingerprint universe to `label_factory_v1_44fp`; frozen current702 labels stay
stamped with their historical decision version and were not written.

Measured result: no bronze rows were applied. Corrected live preview
`artifacts/v3_aminoglycoside_phosphotransferase_sourcing_preview_corrected_active_binding_bounded50_current702_20260615.json`
fetched **18** reviewed rows, produced **17** target mechanism-corroborated labels, and admitted
**17** novelty-safe labels with **0** off-target holds. This is clean but below the >=150
clean-admit batch gate.

Decision: do not apply the 17-row APH preview. Current planning artifacts after 44fp infrastructure
show **0** ready existing lanes with >=150 projected clean admits, holes
`aminoglycoside_phosphotransferase` and `metal_independent_phosphodiesterase`, and top projected
clean supply `short_chain_dehydrogenase_reductase` at **84**. The next mass-growth action should
pivot to higher-yield mechanism-first source strategy, likely SDR/AKR or another source tier/family
whose source wall can plausibly clear the batch gate.

## 2026-06-15: METAL-INDEPENDENT PDE IS A GUARDED 43RD FINGERPRINT, BUT NOT APPLIED

Decision: add `metal_independent_phosphodiesterase` as the 43rd positive fingerprint and keep the
source wall mechanism-first. EC 3.1.4 / 4.6.1 may scope/fetch candidate rows but is never a counted
corroborator. Metal absence may filter out metal-dependent phosphoesterase/nuclease rows, but metal
absence itself is not evidence. Counted corroboration requires mechanism-bearing axes such as
phosphodiesterase family/name context, hydrolytic phosphodiester or cyclic-nucleotide Rhea/reaction
evidence, active-site or binding-site context, and source-tier-appropriate independent axes.
Keyword/name/query handles remain excluded source/admission context and do not become predictive
features.

Implementation: added `src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py`,
`scripts/source_metal_independent_phosphodiesterase_family.py`, the
`metal_independent_phosphodiesterase` fingerprint, ontology family
`metal_independent_phosphodiester_hydrolysis`, deploy context, coverage/governor signature,
high-yield factory wiring, focused tests, optional tier-2 lane support, and the 43fp OOS
preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_43fp_1025.json`. Updated the
current positive-fingerprint universe to `label_factory_v1_43fp`; frozen current702 labels stay
stamped with their historical decision version and were not written.

Measured result: no bronze rows were applied. The reviewed cursor preview
`artifacts/v3_metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.json`
fetched **265** reviewed rows, produced **18** target mechanism-corroborated labels, and admitted
only **14** novelty-safe labels. Alternate reviewed handles fetched **130** rows with **0** target /
**0** admitted labels. Tier-2 count scouts were large, but the live tier-2 preview
`artifacts/v3_metal_independent_phosphodiesterase_tier2_sourcing_preview_cursor_pages2_size100_current702_20260615.json`
fetched **400** rows with **0** target labels, **0** admits, **186** off-target holds, and **197**
`trust_tier_corroboration_insufficient` holds.

Decision: do not apply the 14-row reviewed preview and do not pad the same PDE UniProt handles.
Current planning artifacts after the 43fp infrastructure show `metal_independent_phosphodiesterase`
as the lone hole/under-floor fingerprint, no ready existing lanes with >=150 projected clean admits,
and top projected clean supply `short_chain_dehydrogenase_reductase` at **84** under current
handles. The next mass-growth action should improve source handles/source tiers in a
mechanism-first way before mutation: either design a materially sharper PDE split or move to a
higher-yield family/source strategy with a family-specific source wall, fresh OOS preregistration if
the fingerprint universe changes, non-destructive preview, row guardrail audit, novelty/governor
replay, leakage/source-contract validation, and explicit apply only if the batch gate is met.

## 2026-06-15: N-RIBOSYL HYDROLASE CURSOR BATCH IS COUNTED BRONZE

Decision: the `n_ribosyl_hydrolase` 42nd-fingerprint lane is now countable bronze after a
Link-header UniProt cursor-pagination source fix produced an apply-sized, mechanism-first batch.
The earlier 61-row aggregate remains historical and must not be applied, but it no longer blocks
the family floor.

Implementation: added reusable UniProt Link-header pagination in `src/catalytic_earth/adapters.py`
and wired `scripts/source_n_ribosyl_hydrolase_family.py` with
`--use-query-cursor-pagination` / `--query-pages-per-lane`. Also fixed the script timeout wrapper
so large child-process fetch payloads are read from the queue before join, avoiding false timeout
artifacts. The source handles remain admission/excluded context only; EC/name/prose stay outside
predictive evidence.

Measured result: cursor-paginated synonym preview
`artifacts/v3_n_ribosyl_hydrolase_sourcing_preview_cursor_synonym_pages5_size40_current702_20260615.json`
fetched **200** reviewed Swiss-Prot rows, found **181** target mechanism-corroborated labels,
admitted **150** novelty-safe labels, and held **31** at the per-fingerprint cap. Row audit
`artifacts/v3_n_ribosyl_hydrolase_row_guardrail_audit_current702_20260615_cursor_synonym_pages5_size40.json`
checked all **150** admitted rows with **0** problems; every row is UniProt namespace, bronze,
`automation_curated`, source tier 0, `predictive_evidence: []`, and has non-EC domain/family plus
Rhea reaction/participant mechanism axes. Applying through the explicit reuse-preview command
changed external rows **7420 -> 7570** and combined label surface **8122 -> 8272**; frozen
current702 sha stayed `5eec9bef...`.

Post-apply audits: coverage reports **8272** combined labels, no holes or under-floor
fingerprints, fingerprint Gini **0.1783**, and only `metal_dependent_hydrolase` over cap. Novelty
replay reports **7109** admit / **414** throttle / **47** reject across **7570** external rows.
Honest counters are now external rows **7570** = external seed **6346** + external OOS **1224**,
with external silver **30**; combined seed surface **6576**; positive bronze **6529**; OOS bronze
**1696**; silver_confirmed **47**; projected **0**.

Decision: next mass-growth lane is `metal_independent_phosphodiesterase`, not more N-ribosyl.
Build it as the 43rd fingerprint only through the full gated path: fingerprint + ontology node,
43fp OOS preregistration before candidate selection, reviewed-UniProt runner, bounded preview,
row guardrail audit, novelty/governor/dedup/cap replay, tests, and explicit apply.

Source-wall caveat: broad and targeted PDE previews are not yet apply-sized. The broad first
windows fetched **68** rows with **1** target label; targeted first windows fetched **157** rows
with **13** target / **11** novelty-admitted preview labels; cursor-paged active/binding-site,
hydrolase non-metal, and cyclic-nucleotide name handles fetched **244** rows with **18** target /
**14** novelty-admitted preview labels. These artifacts are source-strategy evidence only and
write no registry, fingerprint, or ontology state. The future 43fp runner needs sharper
mechanism-bearing source handles before any registry mutation.

Post-rebase representation safety: after `origin/main` merged the reaction-center separability
restore, the applied N-ribosyl rows exposed a detector gap rather than a registry problem.
N-ribosyl Rhea equations produce D-ribose or ribose-5-phosphate plus nucleobase, but the
reaction-center feature space had no N-glycosidic hydrolysis class; those rows were initially
pulled into the zero-feature hydrolase bucket and dropped real-registry leave-one-out
self-consistency to **0.7384**. Added leakage-safe `bc_n_glycosidic_hydrolysis`, derived only from
Rhea substrate/product strings, which restores overall self-consistency to **0.7598** while keeping
carbohydrate `bc_glycoside_hydrolysis` distinct.

## 2026-06-15: N-RIBOSYL HYDROLASE IS A GUARDED 42ND FINGERPRINT, BUT NOT APPLIED

Decision: add `n_ribosyl_hydrolase` as the 42nd positive fingerprint and keep the source wall
mechanism-first. EC 3.2.2 may scope/fetch candidate rows but is never a counted corroborator.
Counted corroboration requires non-EC mechanism axes such as N-ribosyl/nucleosidase family or name
context plus N-glycosidic hydrolysis Rhea/reaction-participant evidence. Broadened synonym handles
(`nucleosidase`, `uridine nucleosidase`, `purine nucleosidase`, `N-ribohydrolase`,
`nucleoside N-ribohydrolase`) are admission/source handles only, remain excluded/review-only
context, and do not become predictive features.

Implementation: added `src/catalytic_earth/n_ribosyl_hydrolase_sourcing.py`,
`scripts/source_n_ribosyl_hydrolase_family.py`, the `n_ribosyl_hydrolase` fingerprint, ontology
family `n_glycosidic_bond_hydrolysis`, deploy context, high-yield factory wiring,
coverage/governor signatures, focused tests, optional process-based UniProt fetch timeouts, lane
filtering, and the 42fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_42fp_1025.json`. Updated the
current positive-fingerprint universe to `label_factory_v1_42fp`; frozen current702 labels stay
stamped with their historical decision version and were not written.

Measured result: no bronze rows were applied. Synonym-expanded non-destructive previews produced
**61** unique novelty-safe `n_ribosyl_hydrolase` labels after aggregate dedup/novelty/cap replay
and **0** row guardrail problems. This is below the **150** clean-row batch gate, so the aggregate
is blocked from apply despite clean row-level checks. Offset-paged UniProt synonym probes produced
a raw mechanism-corroborated window sum of **166**, but overlapped the earlier accession set and
left only **61** unique labels. The historical `apply_candidate` filenames now carry corrected
statuses that block apply:
`non_destructive_aggregate_blocked_below_150_no_apply` and
`row_guardrails_pass_but_batch_gate_blocks_apply`.

Decision: do not apply the 61-row N-ribosyl aggregate and do not pad it with tiny topups. The next
source action is reliable UniProt cursor pagination or another reviewed, mechanism-bearing source
path that can produce a clean >=150-row aggregate. If that source is exhausted, pivot to
`metal_independent_phosphodiesterase` as the next new-fingerprint lane with a fresh OOS
preregistration for the then-current fingerprint universe.

## 2026-06-15: REPRESENTATION SEPARABILITY RESTORE LANDED (implements the spec below)

Decision: implemented the validated fix from
`work/next_instance_representation_separability_fix_spec.md` in
`src/catalytic_earth/mechanism_representation_loop.py` (+ tests). Four leakage-safe
reaction-center classes were added, each derived ONLY from the Rhea substrate->product
equation (never EC/name/prose/fingerprint/fold): `bc_ester_hydrolysis` and
`bc_glycoside_hydrolysis` (hydrolyses), `bc_aldehyde_oxidation` (water-consuming NAD redox,
in the non-hydrolytic bucket), and the reused `acc_protein` tag on protein dephosphorylation
(no new feature dim). Measured on the live sharded registry (6196 seed labels), overall
leave-one-out self-consistency was restored **0.713 -> 0.7542**, matching the prototype: per
family `alpha_beta_hydrolase_esterase_lipase` 0.200 -> 0.68, `glycoside_hydrolase` 0.500 ->
0.81, `nad_p_dehydrogenase` 0.547 -> 0.96 (with `aldehyde_dehydrogenase` staying ~0.99),
`ser_thr_protein_phosphatase` 0.000 -> 0.875. The relaxed real-registry test assertions were
RESTORED to these validated numbers (LOO > 0.74; nad_p > 0.9; aldehyde-DH >= 0.95; +new
floors for the restored families), not left accommodating the regression. DOCUMENTED PRINCIPLED
CEILING (not hacked): `ser_his_acid_hydrolase` 0.908 -> 0.667 — alpha/beta-hydrolases and
Ser-His acid hydrolases are BOTH Ser-His-Asp serine esterases, so `bc_ester_hydrolysis`
correctly fires for both and blurs them; the residual separation is FOLD-level, which a
reaction-equation representation cannot and should not force (narrowing to lipase-only does
not help — 22/87 ser_his rows are genuine lipase/phospholipase reactions). Also closed the
governor coverage gap: `ser_thr_protein_phosphatase` was the one registry fingerprint missing
from `coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES` (40/41); it is now registered
(EC 3.1.3.16/48, scope-only/non-predictive) so the coverage/reaction-saturation view covers
all 42. Frozen current702 byte-unchanged; `validate` ok (702 / 41 fp); representation code
only, no registry write. This unblocks the new ester-hydrolase / phosphatase / NAD-redox-subtype
families to reach silver and be visible to the discovery probe.

## 2026-06-15: REPRESENTATION SEPARABILITY REGRESSED BY NEW LANES — validated fix spec written

Finding (read-only health check before scaling further): the new family lanes
(aldehyde_dehydrogenase, alpha_beta_hydrolase_esterase_lipase, ser_thr_protein_phosphatase,
had_like_phosphatase) were added faster than the reaction-center vocabulary, so overall
leave-one-out self-consistency regressed 0.755 -> 0.713 and the regression was ACCOMMODATED by
lowering test thresholds (nad_p `>0.85->>0.5`; metallophosphomonoesterase flipped `>0.8`->`<0.4`)
rather than fixed. ser_thr_protein_phosphatase collapsed to 0.0, alpha_beta_hydrolase to 0.2.
A measure-first prototype VALIDATED a leakage-safe fix: add `bc_ester_hydrolysis`,
`bc_glycoside_hydrolysis`, `bc_aldehyde_oxidation` + reuse `acc_protein` for protein
dephosphorylation -> overall 0.713 -> 0.754, four families restored (alpha_beta_hydrolase 0.68,
glycoside 0.81, nad_p 0.96 with aldehyde-DH staying ~1.0, ser_thr_protein_phosphatase 0.88), with
one documented principled cost (ser_his_acid_hydrolase 0.91 -> 0.67 — a Ser-His-Asp serine-esterase
FOLD overlap with alpha/beta-hydrolase, not hackable by reaction features). Full implement-ready
spec (exact detectors, measured deltas, test re-baseline, + the governor signature gap:
ser_thr_protein_phosphatase missing from FINGERPRINT_SOURCING_SIGNATURES, 40/41) is in
`work/next_instance_representation_separability_fix_spec.md`. Decision: land this BEFORE sourcing
more ester-hydrolase / phosphatase / NAD-redox-subtype families, or that growth is un-promotable
(piles up as review_chemistry_disagrees / low-cohesion bronze). One owner for the representation
module at a time (the spec is the hand-off so two automations don't both edit it).

## 2026-06-15: DISCOVERY-COMPASS LANES HAVE PREVIEW-ONLY SOURCE WALLS; REGISTRY STILL BLOCKED

Decision: use the 2026-06-15 discovery/de novo compass as a scaleout guide, but do not treat its
candidate lanes as registry-ready. Implemented preview-only source-wall rules for
`n_ribosyl_hydrolase` and `metal_independent_phosphodiesterase` in
`src/catalytic_earth/external_cofactor_ec_disambiguation.py`; no fingerprints, ontology nodes,
labels, or registries were written.

Mechanism discipline: EC 3.2.2 / 3.1.4 / 4.6.1 are scope/fetch context only and are never counted.
N-ribosyl admission requires non-EC family/name text plus N-glycosidic hydrolysis reaction evidence,
with phosphorylase, kinase, transferase, O-glycosidase, EC-only, and multi-signal rows held.
Metal-independent phosphodiesterase admission requires non-EC phosphodiesterase family text plus
hydrolytic phosphodiester/cyclic-nucleotide reaction evidence; metal presence is a hold/filter and
metal absence is not counted as evidence.

Measured planning result: refreshed factory artifact
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_discovery_compass.json` ranks
`n_ribosyl_hydrolase` first (**1991** reviewed non-EC-corroborated supply, projected **150**) and
`metal_independent_phosphodiesterase` second (**1129** supply, projected **150**). Both are
`blocked_new_fingerprint_oos_prereg_and_runner_required` with
`source_wall_rule_status=implemented_preview_only`. Design-only preregistrations live at
`artifacts/v3_n_ribosyl_hydrolase_lane_preregistration_current702_20260615_discovery_compass.json`
and
`artifacts/v3_metal_independent_phosphodiesterase_lane_preregistration_current702_20260615_discovery_compass.json`.

Decision: next registry mutation should build `n_ribosyl_hydrolase` through the full 42fp path:
fingerprint + ontology node, OOS preregistration refresh, reviewed-UniProt source runner,
non-destructive preview, row guardrail audit, novelty/governor/dedup/cap replay, and explicit
apply. Do not apply labels from the preview-only source wall alone.

## 2026-06-15: DISCOVERY & DE NOVO STRATEGY (see docs/discovery_and_de_novo_strategy.md)

Decision (direction, conversation-derived; no code change): keep scaling the atlas via
DIVERSE new families + silver grounding (= ontology completion), because that is precisely
what unblocks mechanism discovery later. Key conclusions captured in the dedicated doc:
(1) de novo splits into ENZYME DESIGN (model-central, far; atlas is grounding/eval only) vs
MECHANISM DISCOVERY/annotation (atlas-central, near); (2) raw row count creates no capability
— diversity x groundedness does (the novelty gate is an effective-sample-size gate);
(3) a read-only evidence-quality-vs-family-match probe (2026-06-15) WORKS but its hits are
dominated by OUR incompleteness (missing fingerprints + missing bond-change primitives), not
world-new chemistry — e.g. it surfaced metal-INDEPENDENT phosphodiesterases (a coverage gap,
not new chemistry) and known glycosidase/ester/N-ribosyl hydrolyses our classifier lacks a
class for; (4) certifying WORLD-new chemistry requires a comprehensive reference (full Rhea/
KEGG/MetaCyc/BRENDA) + experiment — "unlike our ~41 fingerprints" almost always means "known
but unsampled". METHOD TRAP recorded: an evidence score that counts "has a recognised
bond-change" as evidence bakes in the known-vocabulary bias and can only surface coverage gaps;
evidence quality MUST be vocabulary-independent. Use the read-only probe as a COMPASS to aim
scaling at the highest-evidence missing families; revisit new-chemistry seriously only once
the ontology is broad enough that "novel" is a strong word.

## 2026-06-14: SER/THR PROTEIN PHOSPHATASE BATCH IS COUNTED BRONZE AFTER RHEA TOKEN FIX

Decision: keep `ser_thr_protein_phosphatase` as the 41st positive fingerprint, but fix the
mechanism-reaction admission handle to recognize curated protein-substrate Rhea/UniProt forms using
`O-phospho-L-seryl-[protein]` and `O-phospho-L-threonyl-[protein]`. These are reaction participant
patterns and count as Rhea/reaction-axis mechanism evidence. EC 3.1.3.16/48 remains scope/fetch
context only and is never a counted corroborator.

Measured result: contiguous bounded windows after the fix produced an aggregate preview with
**743** fetched candidates, **170** unique mechanism-corroborated Ser/Thr candidates, **112**
novelty-safe admitted rows, **58** novelty-throttled/rejected rows, and **2** off-target
metallophosphomonoesterase holds. The row guardrail audit found **0** problems: all admitted rows
are UniProt namespace, `bronze`, `automation_curated`, source tier 0, and have
`predictive_evidence: []`; EC was not counted as a mechanism axis.

Decision: apply the **112** guarded rows despite the original 150 cap preference because the
corrected contiguous source lane was clean, bounded, and meaningful, while later windows showed
novelty-throttling and only **38** cap room remains. Applying changed external rows **7308 -> 7420**
and combined labels **8010 -> 8122**; frozen current702 sha stayed `5eec9bef...`.

Decision: do not continue Ser/Thr as a mass-growth lane without improved novelty/source handles.
The refreshed factory reports **0** ready existing lanes >=150; top projected clean admits is
`short_chain_dehydrogenase_reductase` at **84**, captured as design-only preregistration. Any next
registry mutation should first improve source handles or source tiers, then rerun OOS
preregistration, bounded preview aggregation, novelty/cap replay, and row guardrail audit.
Post-apply breadth feasibility projects reviewed Swiss-Prot clean-only positive bronze to **9067**
with a **933** positive gap, so 10k positive bronze still requires source expansion or a broader
honest-counter target definition.

## 2026-06-14: SER/THR PROTEIN PHOSPHATASE IS A GUARDED 41ST FINGERPRINT, BUT NOT YET APPLIED

Decision: add `ser_thr_protein_phosphatase` as the 41st positive fingerprint and keep the source
wall mechanism-first. EC 3.1.3.16/48 may scope/fetch/admit candidate rows but is never a counted
corroborator. The counted axes are protein-phosphatase family/name context, dinuclear
metal/cofactor or binding-site context, and Rhea/reviewed phosphoprotein dephosphorylation reaction
context. Protein names, keywords, EC, lane names, source prose, and broadened handles remain
excluded context and are not predictive features.

Implementation: added `src/catalytic_earth/ser_thr_protein_phosphatase_sourcing.py`,
`scripts/source_ser_thr_protein_phosphatase_family.py`, the `ser_thr_protein_phosphatase`
fingerprint, ontology family `dinuclear_metal_phosphoprotein_dephosphorylation`, 41fp OOS
preregistration artifact `artifacts/v3_external_hard_negative_next_tranche_preregistration_41fp_1025.json`,
and focused tests. Updated the current positive-fingerprint universe to `label_factory_v1_41fp`;
frozen current702 labels stay stamped with their historical decision version and were not written.

Measured result: no bronze rows were applied. Full, 20-row, 5-row, and 1-row live previews stalled
on UniProt REST reads before complete preview artifacts could be written. After adding per-fetch
timeouts, bounded windows across offsets 0-14 wrote non-destructive artifacts with **13** fetched
candidate rows, **0** target mechanism-corroborated rows, **13** `no_mechanism_corroboration`
holds, **0** novelty-admitted rows, and **26** fetch failures. The lane is now recognized by the
high-yield factory as an existing runner with **150** projected clean admits, but it still needs a
completed larger preview and row guardrail audit before any apply.

Decision: do not demote chemistry-disagree rows or relax cohesion thresholds from refreshed
post-41fp previews. `artifacts/v3_chemistry_disagree_triage_current702_20260614_post_ser_thr_runner.json`
and `artifacts/v3_cohesion_threshold_calibration_current702_20260614_post_ser_thr_runner.json`
are review-only summaries; they changed no labels, no thresholds, and no predictive evidence.

## 2026-06-14: ALPHA/BETA HYDROLASE ESTERASE/LIPASE IS A COUNTED BRONZE FAMILY WITH NON-EC CORROBORATION

Decision: add `alpha_beta_hydrolase_esterase_lipase` as the 40th positive fingerprint and keep
the source wall mechanism-first. EC 3.1.1 may scope/fetch/admit candidate rows but is never a
counted corroborator. The counted axes are alpha/beta hydrolase family/domain context,
Ser-His-Asp/Glu active-site context, and Rhea ester-hydrolysis reaction/participant context.
Protein names, keywords, EC, lane names, source prose, and broadened handles remain excluded
context and are not predictive features.

Implementation: added `src/catalytic_earth/alpha_beta_hydrolase_esterase_lipase_sourcing.py`,
`scripts/source_alpha_beta_hydrolase_esterase_lipase_family.py`, the
`alpha_beta_hydrolase_esterase_lipase` fingerprint, ontology family
`ser_his_acid_ester_hydrolysis`, 40fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_40fp_1025.json`, and focused
tests. Updated the current positive-fingerprint universe to `label_factory_v1_40fp`; frozen
current702 labels stay stamped with their historical decision version and were not written.

Measured result: bounded UniProt windows produced an aggregate preview with **795** fetched rows,
**161** unique target mechanism-corroborated rows, and capped **150** novelty-safe admits. The row
guardrail audit found **0** problems across all applied rows; `predictive_evidence` stayed empty.
Applying the exact aggregate changed external rows **7158 -> 7308** and combined labels
**7860 -> 8010**. Frozen current702 sha stayed `5eec9bef...`.

Decision: do not immediately rerun alpha/beta hydrolase esterase/lipase for mass growth. The lane
is now at its chemistry-confusable cap. The refreshed high-yield factory reports no existing lane
with >=150 cap room and selects `ser_thr_protein_phosphatase` as the next new-fingerprint runner
to build, with protein-phosphatase family/name, dinuclear metal context, and phosphoprotein
dephosphorylation Rhea evidence as required non-EC corroborators.

## 2026-06-14: ALDEHYDE DEHYDROGENASE IS A COUNTED BRONZE FAMILY WITH NON-EC CORROBORATION

Decision: add `aldehyde_dehydrogenase` as the 39th positive fingerprint and keep the source wall
mechanism-first. EC 1.2.1 may scope/fetch/admit candidate rows but is never a counted corroborator.
The counted axes are ALDH family/domain context, NAD(P) cosubstrate or binding-site context, Rhea
aldehyde oxidation reaction/participant context, and catalytic Cys/Glu active-site evidence where
available. Protein names, keywords, EC, lane names, source prose, and broadened handles remain
excluded context and are not predictive features.

Implementation: added `src/catalytic_earth/aldehyde_dehydrogenase_sourcing.py`,
`scripts/source_aldehyde_dehydrogenase_family.py`, the `aldehyde_dehydrogenase` fingerprint,
ontology node `cys_thiohemiacetal_aldehyde_oxidation`, 39fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_39fp_1025.json`, and focused
tests. Updated the current positive-fingerprint universe to `label_factory_v1_39fp`; frozen
current702 labels stay stamped with their historical decision version and were not written.

Measured result: live preview admitted the capped **150** rows from **264** fetched records after
mechanism-corroboration, dedup, novelty, and cap gates. The row guardrail audit found **0**
problems across all applied rows; `predictive_evidence` stayed empty. Applying the exact preview
changed external rows **7008 -> 7158** and combined labels **7710 -> 7860**. Frozen current702 sha
stayed `5eec9bef...`.

Decision: do not immediately rerun ALDH for mass growth. The lane reached its chemistry-confusable
cap and the refreshed high-yield factory reports no existing lane with >=150 cap room. It selects
`alpha_beta_hydrolase_esterase_lipase` as the next new-fingerprint runner. A design-only
preregistration artifact,
`artifacts/v3_alpha_beta_hydrolase_esterase_lipase_lane_preregistration_current702_20260614_post_aldehyde_dehydrogenase_apply.json`,
records esterase/lipase family, Ser-His-Asp/Glu active/binding-site, and Rhea ester-hydrolysis
non-EC corroborators plus hard holds for protease/amidase, glycoside/transglycosylase, metal
hydrolase, EC-only, and unresolved multi-fingerprint confounds; it writes no labels or registry
rows.

Decision: the representation loop must treat the ALDH/NAD(P)-dehydrogenase overlap honestly. ALDH
rows are self-consistent under current source-free features, but generic `nad_p_dehydrogenase`
rows often confuse into ALDH. This is a representation gap for future leakage-safe feature or
geometry design, not justification to relax source admission, cohesion thresholds, or silver
geometry promotion.

## 2026-06-14: HAD-LIKE PHOSPHATASE IS A COUNTED BRONZE FAMILY WITH NON-EC CORROBORATION

Decision: add `had_like_phosphatase` as the 38th positive fingerprint and keep the source wall
mechanism-first. EC 3.1.3 may scope/fetch/admit candidate rows but is never a counted corroborator.
The counted axes are HAD family/domain context, Mg/Asp aspartyl-phosphoenzyme context,
active/binding-site residue evidence, and Rhea phosphomonoester hydrolysis. Protein names,
keywords, EC, lane names, source prose, and broadened handles remain excluded context and are not
predictive features.

Implementation: added `src/catalytic_earth/had_like_phosphatase_sourcing.py`,
`scripts/source_had_like_phosphatase_family.py`, the `had_like_phosphatase` fingerprint, ontology
node `had_aspartyl_phosphoenzyme_hydrolysis`, 38fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_38fp_1025.json`, and focused
tests. Updated the current positive-fingerprint universe to `label_factory_v1_38fp`; frozen
current702 labels stay stamped with their historical decision version and were not written.

Measured result: live preview admitted **146** rows from **354** fetched records after
mechanism-corroboration, dedup, novelty, and cap gates. The row guardrail audit found **0**
problems across all applied rows; `predictive_evidence` stayed empty. Applying the exact preview
changed external rows **6862 -> 7008** and combined labels **7564 -> 7710**. Frozen current702 sha
stayed `5eec9bef...`.

Decision: do not immediately rerun HAD for mass growth. A broader 500-record probe admitted only
**145** rows under the same gates, so the lane is saturated around the applied **146** rows without
a new evidence handle. The refreshed high-yield factory therefore selects `aldehyde_dehydrogenase`
as the next new-family runner. A design-only preregistration artifact,
`artifacts/v3_aldehyde_dehydrogenase_lane_preregistration_current702_20260614_post_had_apply.json`,
records ALDH family/NAD(P)/Cys-Glu non-EC corroborators and hard holds for molybdopterin, flavin,
generic NAD(P), SDR, AKR, and EC-only confounds; it writes no labels or registry rows.

Decision: the representation loop must treat the HAD/metallophosphomonoesterase overlap honestly.
HAD rows are highly self-consistent under source-free features, but generic
`metallophosphomonoesterase` rows often confuse into HAD. This is a representation gap for future
leakage-safe feature design, not justification to relax source admission, cohesion thresholds, or
silver geometry promotion.

## 2026-06-14: SILVER GEOMETRY CONFIRMATION IS A LOCAL-GEOMETRY GATE, NOT ANNOTATION

Decision: implement and apply the separate silver geometry-confirmation gate for rows that already
passed silver runnability. Added `src/catalytic_earth/silver_geometry_confirmation_run.py` and
`scripts/run_silver_geometry_confirmation.py`. The gate requires the prior runnability inputs
(recorded holo PDB confirmation, sha-matched local coordinate, and explicit PDB residue mappings),
then builds local geometry features from the mmCIF and uses the existing geometry retrieval plus
label-factory promotion rule. UniProt binding-site prose/roles, EC, Rhea, names, and source text are
not scoring features.

Measured result: the apply artifact
`artifacts/v3_silver_geometry_confirmation_run_current702_20260614_apply.json` scored **154**
runnable rows; **30** passed and were flipped to silver; **124** were held. The pass rows were
limited to flavin dehydrogenase/reductase (**12**), metallo-amidohydrolase/deaminase (**17**), and
PLP-dependent enzyme (**1**) under the current geometry representation. Frozen current702 sha stayed
`5eec9bef...`; `predictive_evidence` stayed unchanged; row count stayed **6862**.

Decision: the bronze->silver preview must no longer requeue rows already promoted to silver. It now
keeps all seed rows for centroid/count context, but only bronze seed rows are eligible for pending
promotion decisions; already silver/silver_confirmed rows are counted separately. Post-apply audit
therefore reports **230** pending silver-ready rows (**124** runnable and **106** blocked), not the
pre-apply **260**.

Decision: cohesion thresholds were reviewed but not relaxed. The non-destructive artifact
`artifacts/v3_cohesion_threshold_calibration_current702_20260614_post_silver_apply.json` found
**1759** low-cohesion holds and **232** near-threshold rows, but changed no thresholds and wrote no
registry. Low-self-consistency families remain representation/scope-gap review, not candidates for
count-driven threshold lowering.

Decision: the next high-yield bronze lane is `had_like_phosphatase`, but it remains blocked on new
fingerprint, OOS preregistration, and a source runner. The design-only preregistration artifact
`artifacts/v3_had_like_phosphatase_lane_preregistration_current702_20260614_post_silver_apply.json`
fixes the required non-EC corroborators, hard-negative holds, novelty/dedup gates, and excluded
context/predictive-evidence separation before any implementation. No labels, ontology entries, or
registry rows were written by that artifact.

Decision: fresh downstream evaluation must be built as a new frozen surface, not by reusing the
spent heldout one-shot. `docs/fresh_leakage_safe_downstream_eval_design.md` is a design artifact
only: it defines train/cal development, a prospective shadow-eval queue, and a future frozen
downstream eval surface with row/hash freeze requirements. It is not a benchmark result.

## 2026-06-14: SILVER GEOMETRY MATERIALS MUST BE SHA- AND ALIGNMENT-BACKED

Decision: local holo coordinate files count toward silver geometry runnability only when their
sha256 matches the recorded `holo_pdb_confirmation.coordinate_sha256`. Added this guard to
`src/catalytic_earth/silver_geometry_confirmation.py`; mismatched historical coordinate files are
reported as `local_coordinate_sha_mismatch_holo_confirmation` and are not treated as geometry-ready
material.

Decision: explicit PDB residue mappings may be backfilled only through structure alignment evidence,
not by copying UniProt sequence positions. Added
`src/catalytic_earth/silver_holo_coordinate_materialization.py` /
`scripts/materialize_silver_holo_coordinates.py` and
`src/catalytic_earth/silver_pdb_residue_mapping.py` /
`scripts/map_silver_pdb_residues.py`. The first lane reuses/fetches only sha-verified holo PDB
mmCIFs; the second maps exact UniProt active-site residues to PDB chain/residue positions through
mmCIF `_struct_ref_seq` plus `_pdbx_poly_seq_scheme` alignment tables. Both are provenance-only
external-registry writes; they do not run/fake geometry scoring, change tiers, alter predictive
evidence, or write frozen current702.

Measured result: bounded coordinate materialization raised verified local holo-coordinate rows to
**260**, clearing the local-coordinate blocker for the current silver-ready queue, and explicit PDB
residue-mapped rows to **162**. Final audit
`artifacts/v3_silver_geometry_confirmation_audit_current702_20260614_post_fetch257_mapping.json`
found **154/260** silver-ready rows ready for the separate geometry-confirmation run, **106** still
blocked, and **0** silver flips. Remaining blockers are missing explicit PDB residue mapping **98**
and insufficient exact active-site residues **20**. Frozen current702 sha stayed `5eec9bef...`; all
external rows remain bronze.

## 2026-06-14: SILVER GEOMETRY CONFIRMATION REQUIRES EXPLICIT PDB RESIDUE MAPPING

Decision: the 260 `silver_ready_pending_geometry_run` rows are a queue, not a tier flip, until the
separate geometry gate can actually run. Added a non-destructive audit
(`src/catalytic_earth/silver_geometry_confirmation.py`,
`scripts/audit_silver_geometry_confirmation.py`) that consumes the bronze->silver preview and
checks for the remaining runnable materials: recorded holo PDB confirmation, a local holo coordinate
file, and explicit PDB chain/residue mappings. It does not run/fake geometry scoring, write a
registry, or change tiers.

Measured result:
`artifacts/v3_silver_geometry_confirmation_audit_current702_20260614.json` found **0/260** runnable
rows and **0** silver flips. All 260 rows lack explicit PDB chain/residue mappings; 259 lack a local
holo coordinate file; 20 have insufficient exact active-site residues. UniProt sequence positions
must not be treated as PDB residue mappings. Therefore holo confirmation is necessary but not
sufficient for silver; the next silver action is a SIFTS/PDB residue-mapping and local holo-coordinate
materialization lane, followed by this audit and only then a geometry-gate apply for passing rows.

Decision: continuing UniProt PDB-ID backfill is useful only while it yields new PDB handles. This
run applied additional bounded chunks and moved external rows with PDB IDs **1298 -> 2020** (+722)
without changing row count, tiers, or predictive evidence; frozen current702 sha stayed
`5eec9bef...`. A final 3000-row probe backfilled **0** rows and mostly rechecked no-xref rows, so
future large PDB chunks should first add a no-xref skip/recheck policy or use a different curated
source. A bounded RCSB holo-confirmation apply was attempted after the second PDB chunk but stalled
on TLS/network and was interrupted before any registry write; silver-ready remains **260**.

## 2026-06-14: REGISTRY SHARDING, FULL-SUITE RECOVERY, AND PDB-ID BACKFILL PATH

Decision: stop treating the monolithic external bronze registry as safe for continued growth.
`data/registries/external_bronze_labels.json` had grown to ~54 MB, above the repo's GitHub-safe
operating threshold. Added transparent sharded-registry support in
`src/catalytic_earth/registry_io.py` and migrated readers/writers that consume or rewrite the
external registry. The canonical row order and all 6,862 external labels are preserved; the checked-in
registry path is now a 1,203-byte manifest plus four shard files (largest 17,996,716 bytes). Frozen
current702 remains the unsharded 702-row benchmark and is never written by growth/backfill paths.

Decision: full-suite failures after latest origin were stale expanded-universe pins unless proven
otherwise. The first full run produced five failures: two source-lane tests still counted newly
explicit off-target fingerprints in the older disambiguation bucket, one EPK test still expected the
old 15-fingerprint count, one geometry-ablation test assumed the metal hydrolase reason stayed in
top-20 after the 37-fingerprint expansion, and one SDR inverse-gate fixture listed only the older
missing-fingerprint set. Each assertion was updated to the measured 37-fingerprint state with count
rationale. Final validation from the actual final state: full suite **2238 passed, 1 warning, 244
subtests in 163.10s**; focused changed-state tests **39 passed**; `python -m catalytic_earth.cli
validate` and `git diff --check` passed.

Decision: PDB-ID backfill is allowed only as external structure provenance, not as predictive
evidence or silver evidence by itself. Added `src/catalytic_earth/label_pdb_id_backfill.py` and
`scripts/backfill_label_pdb_ids.py`. The writer fills empty external
`evidence.structure_provenance.pdb_ids` from curated UniProt `xref_pdb`, records
`pdb_id_backfill_provenance`, validates rows before writing, refuses to target frozen current702, and
writes through the sharded registry writer. Applied a bounded first chunk (`--limit 120`): 19 rows
backfilled, 101 queried rows lacked UniProt PDB xrefs, 5463 deferred; frozen sha `5eec9bef...`
unchanged. A bounded holo preview after the backfill found 0 additional holo confirmations, so the
silver-ready queue remains 260 pending geometry run and no tier was changed.

## 2026-06-14: FIRST SILVER-READY ROWS via HOLO EXPERIMENTAL-PDB CONFIRMATION

Decision: act on the measured finding that offline silver promotion was at a hard ZERO and
that the ONLY honest lever was new structural data (the user authorized the holo-coordinate
lane). Diagnosis: the bronze->silver gate scores `silver_ready` only when the annotated
cofactor is PRESENT in the coordinates (true holo), but the registry's staged coordinates are
AlphaFoldDB predictions, which are inherently apo -- so silver_ready was stuck at 0 with every
corroborated row in `blocked_pending_structure`/`blocked_apo`. Measured candidate pool: 371
chemistry-corroborated, cofactor-defined rows carry experimental `pdb_ids`; a sample fetch
confirmed 5/6 are genuinely holo (FAD/HEM/SF4/PLP/Zn present).

Implementation: new `src/catalytic_earth/holo_structure_promotion.py` +
`scripts/promote_holo_structures.py`. For each bronze seed label that the gate already scores
as chemistry-corroborated (nearest centroid == assigned AND own cohesion >= threshold) and
that carries experimental `pdb_ids` + an annotated cofactor, it fetches the experimental PDB
mmCIF (RCSB) and tests whether the annotated cofactor is present as a HETATM -- the SAME holo
test the gate uses. When present it records a sha-pinned
`evidence.structure_provenance.holo_pdb_confirmation` (pdb_id, cofactor comp ids present,
sha256, atoms). `bronze_silver_promotion_preview.structure_confirmability` now returns `holo`
when that confirmation block is present (the experimental coordinate is regeneratable from the
PDB id, so the determination -- not the bulky mmCIF -- is what is stored/honoured, mirroring
the AFDB-backfill philosophy). Candidate selection is chemistry-only; structure stays
review-only mechanism context, never a predictive feature (leakage wall intact).

Applied in two passes (a diverse bounded `--per-fingerprint-cap 8` batch, then the full
corroborated pool): 260 holo confirmed across 24 fingerprints (~70-80% hit-rate; 111
candidates had only apo PDBs). Gate: `silver_ready_pending_geometry_run` 0 -> 260;
`blocked_pending_structure` 2534 -> 2275; `blocked_apo` 1 -> 0; review/hold unchanged.
HONEST: `blocked_pending_structure` (2426) still dominates -- the ~5500 rows with no
experimental PDB are not inflated -- and silver_ready is `*_pending_geometry_run`: the actual
geometry-confirmation run is a SEPARATE authorized step; this only proves the gate is meetable
with real holo evidence rather than abstaining on apo. Label counts/tiers UNCHANGED (apply
added only provenance; all rows stay bronze): expansion 6862, combined 7564, positive_bronze
5851, silver_confirmed 17. The honest counters stay SEPARATE -- silver_ready is the promotion
gate's queue, NOT a tier flip.

Discipline: the apply is a non-destructive expansion-registry rewrite (row count unchanged,
each kept label re-validated via MechanismLabel.from_dict); the runner printed the frozen
current702 sha (`5eec9bef…`) identical before and after; frozen NEVER written; mmCIFs never
committed (regeneratable from PDB id); validate ok (702 / 37 fp); leakage wall intact. The
`honest_about_apo` real-registry test was updated to the new reality (silver_ready > 0 from
recorded holo, blocked_pending_structure still dominant, geometry never faked) -- this is an
honest re-baseline, not a relaxation. New-label sourcing was PAUSED during this work (the holo
apply rewrites the same `external_bronze_labels.json`, so concurrent sourcing would race/clobber;
the registry is also at GitHub's 51 MB soft limit). Resume sourcing only on a clean registry
after this commits. Next: run the SEPARATE authorized geometry-confirmation on the 260
silver_ready rows to actually flip tiers to silver.

## 2026-06-14: C-C LYASE / ALDOL SEPARATION (class II metal aldolases)

Decision: measure-first follow-on to the kinase separation. With the fold-defined kinases
(frontier A) ruled a principled ceiling and apo->holo silver promotion (frontier B) ruled a
data ceiling (only 104/5638 seed rows carry coordinates, 103 apo / 1 holo, 5534 unresolved
-- the geometry gate genuinely abstains and the heldout one-shot is spent), the remaining
worst non-fold, non-umbrella family was `class_ii_metal_aldolase` at leave-one-out 0.013.
Diagnosis: 100% of its rows DO carry a Rhea reaction (not a data ceiling), and the dominant
reaction shape is one organic substrate -> two organic products with no water -- a C-C bond
cleavage (retro-aldol / isocitrate-lyase / HMG-CoA-lyase / fructose-bisP aldolase). The
representation had no feature for it, so the family carried only the shared divalent-metal
cofactor and collapsed into the generic metal cluster (SOD / zinc_lyase_hydratase).

Fix (leakage-safe, Rhea substrate->product equation only): added one non-hydrolytic
bond-change class `bc_carbon_carbon_lyase` to `classify_reaction_nonhydrolytic`. It fires
when one organic substrate is cleaved into two organic fragments (or the reverse aldol
condensation), with no water and no NTP anhydride. Organic fragments are counted via a new
`_organic_fragments` helper that splits on Rhea's ` + ` separator (so charged ions
`NH4(+)`/`H(+)` stay intact -- a bare `+` split shreds them) and drops protons / water /
small inorganic leaving groups (`_INORGANIC_FRAGMENTS`). Because a CO2 / phosphate / ammonia
leaving group is inorganic (not a second carbon fragment), decarboxylation / dehydratase /
deamination do NOT trip the class -- verified by negative unit tests. This is the legitimate
North Star axis (reaction-center bond change), NOT substrate-identity patterns and NOT a
fold axis. Feature dims 35 -> 36; `COFACTOR_CLASSES` stays the vector prefix.

Result (leave-one-out): overall expansion-only 0.719 -> 0.755 (+0.036); frozen+exp
0.699 -> 0.7335. `class_ii_metal_aldolase` 0.013 -> 0.813; bonus
`metallophosphoesterase_nuclease` 0.120 -> 0.380, `non_heme_iron_2og_dioxygenase`
0.872 -> 0.972, `coa_acyltransferase` 0.948 -> 0.984, `thiamine_diphosphate_enzyme`
0.733 -> 0.787; cobalamin unchanged 0.825 (no regression; worst single-family move -0.020 on
molybdopterin). Promotion gate `review_chemistry_disagrees` 1572 -> 1344. `silver_ready`
stays 0 (the holo-coordinate / Problem-2 ceiling is unchanged -- correctly the next gate, not
masked). The C-C lyase class fires across several cofactor-distinct families (ThDP, glycoside,
heme) but is harmless there because those carry strong orthogonal cofactor signals -- the
empirical no-regression test, not raw firing counts, was the acceptance criterion.

CEILINGS DOCUMENTED, NOT HACKED: frontier A (fold kinases) and frontier B (apo->holo) per the
prior bullets; plus `metallopeptidase`/`metallophosphoesterase_nuclease` dominated by
`(no reaction)` rows (data ceiling) and `metal_racemase` vs `cofactor_independent_isomerase`
distinguished only by an under-annotated metal (annotation gap). None were forced. No registry
written; frozen current702 byte-unchanged; leakage wall intact.

## 2026-06-14: KINASE ACCEPTOR-SPECIFICITY + ATP-LIGATION SEPARATION

Decision: follow on from the cosubstrate/bond-change extension to separate the ATP-driven
sub-cluster that still collapsed. Diagnosis: `bc_phosphoryl_transfer` was effectively broken
-- it fired only for protein kinase (whose product string contains "phospho-"); every other
ATP->ADP kinase fired only generic `divalent_metal_other` and separated accidentally on
residue noise, so pfkb/ghmp/atp_amide_ligase collapsed.

Fix (all leakage-safe, derived only from the Rhea equation): (1) corrected
`bc_phosphoryl_transfer` to fire for any ATP->ADP anhydride that transfers phosphate to an
organic acceptor (no FREE phosphate token, no water) -- so all kinases fire it; (2) added
`bc_atp_dependent_ligation` for ATP->ADP+Pi (water/free-phosphate) and ATP->AMP+PPi
(adenylylation), which splits the *ligase* atp_amide_ligase out of the kinase cluster; (3)
added phospho-ACCEPTOR classes `acc_protein`/`acc_nucleoside`/`acc_sugar` that fire ONLY
inside a phosphoryl-transfer reaction (so a sugar in a glycosidase does not trip acc_sugar).
Feature dims 31 -> 35.

Result (leave-one-out): overall 0.645 -> 0.699 (frozen+exp; 0.66 -> 0.719 expansion-only).
atp_amide_ligase 0.05 -> 0.87; pfka/ndp/deoxynucleoside -> 1.0; protein_kinase 0.98.
Promotion gate `review_chemistry_disagrees` 1883 -> 1572. Cumulative across both
representation commits this turn: 0.36 -> 0.699 (+94% relative).

PRINCIPLED CEILING (documented, accepted -- NOT to be hacked around): pfkb_ribokinase_family
and ghmp_small_molecule_kinase remain ~0 because they are FOLD-defined families (PfkB/
ribokinase fold; GHMP superfamily) whose reaction chemistry overlaps the sugar kinases
(pfka/askha). A reaction-equation representation cannot separate families that share reaction
chemistry and differ only by protein fold; adding substrate-identity patterns (galactose vs
fructose) to force it would be metric-gaming, not mechanism. Their separation, if ever needed,
belongs to a sequence/structure (fold) axis, not the leakage-safe reaction representation.
No registry written; frozen byte-unchanged; leakage wall intact.

## 2026-06-14: MECHANISM-REPRESENTATION SEPARABILITY EXTENSION (cosubstrate + non-hydrolytic bond change)

Decision: attack the root North Star bottleneck for de novo grounding. Bronze->silver
promotion (the "earn silver by reconstructing deploy-missing context" step) was structurally
blocked: the chemistry-feature representation predated the ontology expansion and could not
SEPARATE the new families, so the promotion chemistry gate rejected ~63% of bronze positives
as `review_chemistry_disagrees`. Leave-one-out diagnosis: overall self-consistency 0.36, with
12 of 37 families at exactly 0.0 -- every family defined by a dissociable cosubstrate/donor
(NAD(P), CoA, sugar-nucleotide, prenyl-PP) or a non-hydrolytic bond change collapsed, because
the feature space carried only cofactor classes + four HYDROLYSIS bond-change classes. The
families that separated were exactly those whose chemistry was already represented (p450,
radical_sam, plp, flavin, sam).

Fix: extended `mechanism_representation_loop.featurize` with leakage-safe cosubstrate classes
(`cos_nad`, `cos_coa`, `cos_nucleotide_sugar`, `cos_2_oxoglutarate`, `cos_prenyl_diphosphate`)
and non-hydrolytic reaction-center bond-change classes (`bc_redox_hydride`,
`bc_phosphoryl_transfer`, `bc_glycosyl_transfer`, `bc_acyl_transfer`, `bc_methyl_transfer`,
`bc_oxygenation`, `bc_decarboxylation`, `bc_carboxylation`, `bc_diphosphate_lyase`,
`bc_isomerization`), via a new `classify_reaction_nonhydrolytic` + `cosubstrate_classes`. Both
read ONLY the Rhea substrate->product equation string (and the cofactor/binding-ligand
chemical-identity terms) -- never EC/name/prose/fingerprint, the same leakage-safe basis as
the existing features. `COFACTOR_CLASSES` is kept as the feature-vector PREFIX so the
positional cofactor-presence helpers (`_significant_centroid_cofactors`, the promotion
preview's cofactor mapping) are unaffected. Feature dims 16 -> 31.

Result (measured, leave-one-out): overall self-consistency 0.36 -> 0.645 (+78% relative).
nad_p_dehydrogenase/coa_acyltransferase/protein_kinase/terpene/biotin/non_heme_iron_2og all
rose from ~0 to 0.87-1.0; sam_methyltransferase 0.60 -> 0.96. In the promotion gate,
`review_chemistry_disagrees` 3558 -> 1883 (nearly halved); those rows moved to honest
`blocked_pending_structure`. silver_ready remains 0 -- that needs HOLO coordinates and the
registry is overwhelmingly apo (the documented Problem-2 structural frontier, now correctly
the next gate). Remaining low separability is the coarse `metal_dependent_hydrolase` umbrella
(correctly scatters to its v2 sub-families) and the ATP kinase sub-families (identical
phosphoryl-transfer + ATP chemistry, differ only by acceptor -- a finer unsolved sub-problem).

Test discipline: the dormant `test_build_on_real_registry_is_leakage_safe` (stale behind a
1716 seed-count pin since the bronze expansion; its >0.8 metal-sub-family thresholds reflect a
12-family M-CSA world) was re-baselined honestly to the measured 37-family reality -- the
leakage guardrails (its core purpose) kept, count refreshed to 5638, thresholds set to the
current numbers, with the new findings asserted (nad_p/coa/protein_kinase/terpene/biotin >
0.85). The bronze_silver promotion stale count pin refreshed likewise. No registry written;
frozen current702 byte-unchanged; leakage wall intact.

## 2026-06-14: NEAR-SATURATED TRIM APPLIED (3 families)

Decision: take the optional backward follow-up flagged when the reaction-aware caps were
wired in. The 3 families that sat over the rate-8 reaction-aware cap but below the
labels/rxn>10 default ratio (`cobalamin_radical_rearrangement` 141/15rxn/9.40,
`pfkb_ribokinase_family` 150/16rxn/9.38, `radical_sam_enzyme` 213/23rxn/9.26) were the
last reaction-saturated growth not yet bounded. Trimmed them to their reaction-aware caps
with `scripts/trim_reaction_saturation.py --saturation-ratio-threshold 9.0` (9.0 is below
the lowest ratio 9.26, so it captures exactly those 3 -- they are the only families over
the reaction-aware cap; no other family is touched). Previewed, then APPLIED on explicit
authorization; the runner printed the frozen current702 sha (`5eec9bef…`) identical before
and after the rewrite.

Result: 72 rows demoted, expansion 6934 -> 6862, combined 7636 -> 7564, positive_bronze
5923 -> 5851 (oos_bronze unchanged 1696; counters stay SEPARATE). Per family: cobalamin
141->120, pfkb 150->128, radical_sam 213->184; all to labels/rxn 8.0. Reaction diversity
fully preserved (15/15, 16/16, 23/23) -- only redundant orthologs demoted. Post-apply
governor: combined 7564, Gini 0.1891 (rises by design), holes [], under-floor [], over-cap
['metal_dependent_hydrolase'] (intentional), reaction_saturated [] -- no family remains
over its reaction-aware cap. Discipline held: frozen NEVER written (apply is a
non-destructive expansion-registry rewrite dropping only the 72 demoted entry_ids,
re-validating every kept label through MechanismLabel.from_dict); demoted rows are bronze,
never frozen; leakage wall unchanged. Real-registry count pins refreshed to 6862/7564.

## 2026-06-14: REACTION-AWARE CAPS WIRED INTO THE LIVE SOURCING PATH

Decision: the prior turn built the reaction-aware family cap and the per-reaction admission
gate but left them un-wired into the forward runners -- the climb could still source flat
150/250-per-family ceilings. Wire the diversity-earned cap and the per-reaction gate into
the live sourcing path so growth is mechanism-diverse BY CONSTRUCTION, and close the
governor's coverage gap. Engine/governor/script wiring only -- no registry written, frozen
current702 byte-unchanged (sha `5eec9bef…`), combined stays 7636, counters unchanged.

- Added shared `stage1_hole_sourcing._reaction_aware_cap_guard` +
  `_distinct_reactions_by_fingerprint`; all three runners (stage1 holes, stage2 hydrolase
  sub-families, NAD/glycosyltransferase) now route their cap guard through it. New opt-in
  `reaction_aware_caps` (default `False` = historical flat ceiling, byte-stable for
  existing tests/replays) makes the per-family cap `clamp(rate*distinct_reactions, floor,
  base_cap)`, where base_cap is the runner's flat `cap_ceiling` or NAD's per-family
  150/250. Depth is earned by reaction diversity: a single-reaction family is bounded at
  the 100 floor (not dropped -- the floor is preserved so holes still fill), a
  reaction-rich family reaches its base ceiling. distinct_reactions is computed over
  combined (frozen+expansion) seed rows PLUS this run's gate-admitted rows, so newly
  sourced reactions earn headroom. floor_projection gains
  `effective_cap`/`distinct_reactions`/`projected_over_effective_cap`.
- Runners thread the gate's `per_reaction_cap` (default `None` = unchanged) into
  `evaluate_batch`, so at admission time no single Rhea reaction accumulates endless
  orthologs even when each new row brings a new organism (enforced only at/above floor).
- The three forward scripts expose `--reaction-aware-caps/--no-reaction-aware-caps`
  (default ON in the live path), `--reaction-cap-rate` (8), `--per-reaction-cap` (12,
  negative disables). Library defaults stay off; the live path defaults on = diverse by
  construction. Backward-compatible: existing runner tests (which call the library with
  defaults) are unaffected; only genuine forward callers opt in.
- Closed the governor coverage gap flagged last turn: added `terpene_cyclase_synthase`
  (EC 4.2.3) and `protein_kinase_ser_thr_tyr` (EC 2.7.10/2.7.11) to
  `coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES` (35 -> 37), so the
  governor's `reaction_saturated`/acquisition view now covers all 37 registry
  fingerprints. Coverage-accounting metadata only -- EC stays scope-only, never
  predictive. This raises `breadth_feasibility_scout`'s `live_fingerprint_count` to 37
  (no test pinned it).

Guardrails: frozen current702 NEVER written; validate ok (702 frozen / 37 fingerprints);
`git diff --check` clean; leakage wall unchanged. New offline tests:
`tests/test_reaction_aware_cap_wiring.py` plus runner-propagation/back-compat and
governor-coverage assertions. The optional backward trim of the 3 near-saturated families
was NOT taken (no authorization to demote more rows).

## 2026-06-14: REACTION-AWARE CAPS + REACTION-SATURATION TRIM APPLIED

Decision: pivot from volume growth to diversity-quality. Growth has become
reaction-saturated in single-reaction families -- 9 of 37 families (1329 labels, ~21%
of expansion positives) exceed 10 labels per distinct Rhea reaction. These are real,
distinct, novelty-gated, leakage-clean orthologs, but they add organism/sequence
breadth, not reaction/mechanism diversity ("chasing volume manufactures redundancy").
The fix is to bound a family's depth ABOVE what its reaction diversity earns -- NOT to
drop single-reaction mechanisms (the 100-floor itself forces ~100 labels/reaction on a
genuinely single-reaction mechanism, so the floor is preserved).

Engine changes (forward prevention):
- Added `coverage_redundancy_audit.reaction_aware_cap(distinct_reactions, rate, floor,
  ceiling)` = `clamp(rate * distinct_reactions, floor, ceiling)` (default rate 8, floor
  100, ceiling 250). The governor's acquisition policy now computes a per-family
  reaction-aware cap, sets `reaction_saturated` / `reaction_aware_surplus`, lists
  `reaction_saturated` families (11 over the cap at rate 8; surplus 451), and emits a
  TRIM recommendation. `rate` and the bounds are parameters, not magic constants.
  Flagged gap: the governor's `FINGERPRINT_SOURCING_SIGNATURES` still lists 35 families,
  so its `reaction_saturated` count excludes the two newest registry fingerprints
  (`terpene_cyclase_synthase`, `protein_kinase_ser_thr_tyr`); the trim is data-driven
  over all 37 registry fingerprints and is unaffected. Add the two to the signature list
  next.
- Added an opt-in `per_reaction_cap` to `novelty_admission_gate.evaluate_candidate` /
  `evaluate_batch` / `self_audit` (default `None` = unchanged historical behavior, so
  retrospective replays are byte-stable). When set (~10-15) it throttles a candidate
  whose every reaction is already at the ceiling -- even with a new organism -- but
  only once the fingerprint is at/above floor, so holes still reach the floor.
  `DiversityState` tracks per-reaction occupancy per scope. This is the durable
  systemic fix; forward callers opt in, the gate's own default stays conservative.

Backward cleanup (the deliverable): new non-destructive module
`src/catalytic_earth/reaction_saturation_trim.py` + runner
`scripts/trim_reaction_saturation.py` + CLI `build-reaction-saturation-trim` + offline
synthetic-registry tests `tests/test_reaction_saturation_trim.py`. For each
reaction-saturated family (labels/rxn > `saturation_ratio_threshold` 10 AND over the
reaction-aware cap) it keeps a reaction- and sequence-diverse subset down to the
reaction-aware cap: `select_diverse_keep` keeps >=1 row per distinct reaction first
(reaction diversity fully preserved), then maximizes organism/sequence-length/cluster
spread via the governor's `(fingerprint, full-EC, organism, length-bin)` near-dup proxy
(deterministic, diversity-ranked, never recency-ranked; the artifact notes local mmseqs
sequence clustering is the stronger dedup when available). The apply path
`apply_reaction_saturation_trim_to_registry` is a non-destructive expansion-registry
REWRITE that drops only the demoted entry_ids and re-validates every kept label through
`MechanismLabel.from_dict`. It was previewed, then APPLIED on explicit authorization (the
runner printed the frozen current702 sha identical before and after the rewrite).

Result (`artifacts/v3_reaction_saturation_trim_preview_current702_20260614.json`,
`work/...md`; measured after rebasing onto the protein-kinase 37fp lane on main): 9
families trimmed, 429 rows demoted, expansion 7363 -> 6934, combined 8065 -> 7636,
positive_bronze 6352 -> 5923 (oos_bronze unchanged 1696; counters stay separate). Per
family (all clamp to the floor because none earns >100 at rate 8): SOD 166->100 (1 rxn),
pfka 150->100 (2), ghmp 150->100 (4), deoxynucleoside 150->100 (7),
zinc_lyase_hydratase 113->100 (6), biotin 150->100 (8), askha 150->100 (9), ndp
150->100 (10), protein_kinase_ser_thr_tyr 150->100 (10). Reaction diversity preserved in
all 9 (every distinct reaction retained). Fingerprint Gini 0.1352 -> 0.1872 -- it RISES
BY DESIGN: Gini measures count evenness, and depth is now proportional to reaction
diversity; the true quality metric (labels-per-reaction) drops to the cap in every
trimmed family. Near-saturated held (over the rate-8 cap but below the labels/rxn>10
ratio, not trimmed at default threshold): cobalamin_radical_rearrangement,
pfkb_ribokinase_family, radical_sam_enzyme.

Discipline: frozen current702 NEVER written (sha256 `5eec9bef...` byte-unchanged,
printed identical before and after the rewrite); the shrink went only to
`data/registries/external_bronze_labels.json`; demoted rows are bronze, never frozen;
leakage wall intact (EC/name/lane excluded-context; reaction accounting uses
mechanism_evidence only); this is a diversity-quality lever, not reconstruction (the
separate silver/deploy axis). `validate` ok (12 source / 37 fingerprints / 34 ontology /
702 curated labels); `git diff --check` clean; frozen registry byte-unchanged.

Post-apply audits: governor
`artifacts/v3_coverage_redundancy_audit_current702_20260614_reaction_trim_applied.json`
reports combined 7636, fingerprint Gini 0.1872, holes `[]`, under-floor `[]` (no family
fell below the 100 floor), over-cap `['metal_dependent_hydrolase']`, next-batch floor
deficit 0. Novelty replay
`artifacts/v3_novelty_admission_gate_audit_current702_20260614_reaction_trim_applied.json`
over 6934 rows reports `{'admit': 6478, 'reject': 47, 'throttle': 409}`, would-not-readmit
456 (0.0658).

Count-pins: refreshed the two live-registry pins to the post-trim values
(`test_coverage_redundancy_audit` 8065/7363 -> 7636/6934, `test_novelty_admission_gate`
7363 -> 6934) -- a genuine change from this apply. Left FLAGGED, not fixed (pre-existing,
broken by the expansion / SDR / epk work): epk readiness fingerprint-count,
atp_amide_ligase disambiguation_hold, pfka_sourcing counts, bronze_silver_promotion,
cofactor_channel_probe, cofactor_presence_calibration, generalization holdout pin,
geometry_retrieval, mechanism_representation_loop, sequence_cofactor_channel,
transfer_scope SDR; plus the numpy-missing collection error on
`test_active_site_supervised_smoke`.

Next decision: add the two newest fingerprints to the governor's
`FINGERPRINT_SOURCING_SIGNATURES`, and wire the reaction-aware cap + per-reaction cap
into the live runners (stage2/nad_glyco/stage1) so future growth stays mechanism-diverse
by construction. Optionally tune `--reaction-cap-rate` / `--saturation-ratio-threshold`
to also trim the 3 near-saturated families (cobalamin/pfkb/radical_sam). The atlas is now
7636 labels (5923 positive bronze); resume diverse new-family sourcing only through the
full gated pipeline.
## 2026-06-14: PROTEIN KINASE 37FP HIGH-YIELD LANE APPLIED

Decision: after `terpene_cyclase_synthase` left only **77** cap slots, stop top-ups and build the
next high-yield lane that could clear the >=150 clean-row gate. `protein_kinase_ser_thr_tyr` was
chosen because the refreshed factory marked it as the only immediately ready existing >=150 lane
after wiring, while SDR/AKR still had prior no-import/source-free mechanism-rule blockers and
HAD-like phosphatase needed stronger hydrolase/phosphatase boundary work.

Mechanism rule: EC 2.7.10/2.7.11 is scope-only. Counted corroboration must come from non-EC
protein-kinase family context plus ATP/Mg cosubstrate context and Rhea protein-phosphoryl-transfer
or active/binding-site evidence. Histidine kinases, small-molecule kinases, ATP ligases,
hydrolases, side-EC rows, EC-only rows, and multi-fingerprint rows stay held. Broadened handles
remain excluded-context source/admission evidence only; `predictive_evidence` remains `[]`.

Implementation: added `protein_kinase_ser_thr_tyr` to the fingerprint registry, added
`protein_substrate_phosphoryl_transfer` to the ontology, bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_37fp`, wired
deploy-missing context, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_37fp_1025.json`. Added
`src/catalytic_earth/protein_kinase_sourcing.py`,
`scripts/source_protein_kinase_family.py`, and `tests/test_protein_kinase_sourcing.py`; extended
`external_cofactor_ec_disambiguation` with protein-kinase evidence axes and boundary holds.

Apply result: the first preview admitted **72** rows and was not applied because it missed the
>=150 gate. The enlarged preview
`artifacts/v3_protein_kinase_sourcing_preview470_current702_20260614.json` fetched **470**,
mechanism-corroborated **248**, held **0** off-target rows, novelty-admitted **150**, and held
**0** at cap. Row audit
`artifacts/v3_protein_kinase_preview470_row_guardrail_audit_current702_20260614.json` found **0**
problems. Applied **150** rows: external bronze **7213 -> 7363**; combined label surface
**7915 -> 8065**; `protein_kinase_ser_thr_tyr` **0 -> 150**, exactly at its chemistry-confusable
cap **150**.

Counts after apply: combined seed-fingerprint surface **6369**, remaining gap **3631** to 10k
seed surface. Honest counters stay separate: **positive_bronze_count 6352**,
**oos_bronze_count 1696**, **silver_ready_count 0**, **silver_confirmed_count 17**,
**projected_provisional_count 0**. Frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

Validation: focused pytest passed (**302 passed, 14 subtests passed**). `PYTHONPATH=src python -m
catalytic_earth.cli validate` passed (12 source records, 37 fingerprints, 34 ontology families,
702 curated labels). Coverage audit reports **8065** combined, **7363** expansion, fingerprint
Gini **0.1385**, holes `[]`, under-floor `[]`, next-batch floor deficit **0**, and over-cap
`['metal_dependent_hydrolase']`. Novelty replay reports **7363** expansion rows, decisions
`{'admit': 6907, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0619).

Next decision: do not continue protein kinase under the current cap policy. Rerun the high-yield
factory against the 37fp applied state. Prefer `aldehyde_dehydrogenase` or
`alpha_beta_hydrolase_esterase_lipase` for cleaner next-family boundaries, or
`had_like_phosphatase` only with a hard boundary against over-cap `metal_dependent_hydrolase`.

## 2026-06-14: TERPENE CYCLASE/SYNTHASE 36FP HIGH-YIELD LANE APPLIED

Decision: build and apply the high-yield `terpene_cyclase_synthase` new-family lane from the
factory ranking. Do not replay capped/tiny top-ups. EC 4.2.3 is scope-only; counted mechanism
corroboration must come from non-EC terpene/cyclase family context plus Mg/Mn or diphosphate
context and Rhea/site evidence. Prenyltransferase chain-extension, generic hydratase/lyase,
side-EC, EC-only, off-target, and multi-fingerprint rows stay held.

Implementation: added `terpene_cyclase_synthase` to the fingerprint registry, added
`terpene_carbocation_cyclization` to the ontology, bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_36fp`, and re-froze
OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_36fp_1025.json`. Added
`src/catalytic_earth/terpene_cyclase_synthase_sourcing.py`,
`scripts/source_terpene_cyclase_synthase_family.py`, and
`tests/test_terpene_cyclase_synthase_sourcing.py`; extended
`external_cofactor_ec_disambiguation` with terpene-specific evidence axes and boundary holds.

Apply result: the first narrow preview admitted **112** rows and was not applied because it missed
the >=150 gate. The broader preview
`artifacts/v3_terpene_cyclase_synthase_broad250_sourcing_preview_current702_20260614.json` fetched
**416**, mechanism-corroborated **188**, held **48** off-target rows, held **134**
no-corroboration rows, novelty-admitted **173**, and held **0** at cap. Row audit
`artifacts/v3_terpene_cyclase_synthase_broad250_row_guardrail_audit_current702_20260614.json`
found **0** problems. Applied **173** rows: external bronze **7040 -> 7213**; combined label
surface **7742 -> 7915**; `terpene_cyclase_synthase` **0 -> 173** under clean cap **250**.

Counts after apply: combined seed-fingerprint surface **6219**, remaining gap **3781** to 10k
seed surface. Honest counters stay separate: **positive_bronze_count 6202**,
**oos_bronze_count 1696**, **silver_ready_count 0**, **silver_confirmed_count 17**,
**projected_provisional_count 0**. Frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

Validation: focused pytest passed (**278 passed, 14 subtests passed**). `PYTHONPATH=src python -m
catalytic_earth.cli validate` passed (12 source records, 36 fingerprints, 33 ontology families,
702 curated labels). Coverage audit reports **7915** combined, **7213** expansion, fingerprint
Gini **0.1385**, holes `[]`, under-floor `[]`, next-batch floor deficit **0**, and over-cap
`['metal_dependent_hydrolase']`. Novelty replay reports **7213** expansion rows, decisions
`{'admit': 6757, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0632).

Next decision: do not continue terpene as a high-yield lane under the current objective because
only **77** cap slots remain. Build the next new-family lane through the same OOS preregistration,
rule, source runner, preview, row audit, and apply gates; `short_chain_dehydrogenase_reductase` is
the leading candidate only after an SDR-specific rule separates it from capped
`nad_p_dehydrogenase`, AKR/MDR, and flavin/metal redox boundaries.

## 2026-06-14: HIGH-YIELD FAMILY SCOUT + LANE FACTORY BUILT; NO CURRENT >=150 APPLY

Decision: stop spending automation runs on exhausted/capped/tiny top-ups. Current existing
fingerprint lanes do not have a safe >=150-row clean batch under the current cap/source evidence.
No registry apply should be attempted until a new-family lane is wired through fingerprint,
ontology, OOS preregistration, disambiguation, preview, row audit, and validation gates.

Implementation: added `src/catalytic_earth/high_yield_family_lane_factory.py`,
`scripts/build_high_yield_family_lane_factory.py`, and
`tests/test_high_yield_family_lane_factory.py`. The factory is non-destructive and creates no
labels. It ranks family-lane specs from reviewed UniProt scope supply, non-EC corroborator-reachable
supply, current registry counts/cap room, cap class, OOS preregistration need, disambiguation
holds, and preview/apply guardrail templates. EC remains scope-only and never predictive; non-EC
handles are source/admission planning evidence only.

Recon results:
- `artifacts/v3_high_yield_family_supply_scout_current702_20260614.json`: **18** broad families
  probed; **14** clean/floor-reachable under broad source-supply cap math; estimated **2641** new
  capped clean bronze (**1504** diversity-discounted); projected positive bronze **8687**, gap
  **1313** to 10k from reviewed Swiss-Prot alone.
- `artifacts/v3_high_yield_family_lane_factory_current702_20260614.json`: **12** concrete family
  specs ranked; **0** existing lanes ready for >=150; **8** high-yield lanes blocked by new
  fingerprint/OOS preregistration/disambiguation-rule infrastructure. Top ranked lane is
  `terpene_cyclase_synthase`: scope supply **2335**, non-EC corroborator supply **2315**,
  estimated corroboration rate **0.991**, projected clean admits **250**, clean cap **250**.

Counts after run: no registry change. External bronze remains **7040**; combined label surface
**7742**; combined seed-fingerprint surface **6046**; remaining gap to 10k seed surface **3954**.
Frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Validation: focused pytest passed
(`PYTHONPATH=src pytest tests/test_high_yield_family_lane_factory.py tests/test_breadth_feasibility_scout.py tests/test_leakage_closure.py tests/test_source_only_contract.py -q`
-> **213 passed, 14 subtests passed**). `PYTHONPATH=src python -m catalytic_earth.cli validate`
passed (12 source records, 35 fingerprints, 32 ontology families, 702 curated labels). JSON parse
checks and `git diff --check` passed.

Next decision: build `terpene_cyclase_synthase` first, not another cap-room top-up. Required work:
add fingerprint + ontology node; preregister the fingerprint-universe/OOS change; add a
mechanism-first rule requiring non-EC terpene/cyclase + Mg/Mn/diphosphate/Rhea evidence; hold
prenyltransferase, lyase/hydratase, and multi-signal boundary rows; add a source runner and row
audit; preview non-destructively; apply only after dedup, novelty, cap, trust-tier, leakage, and
frozen-sha gates pass.

References:
`artifacts/v3_high_yield_family_supply_scout_current702_20260614.json`,
`work/high_yield_family_supply_scout_current702_20260614.md`,
`artifacts/v3_high_yield_family_lane_factory_current702_20260614.json`,
`work/high_yield_family_lane_factory_current702_20260614.md`,
`src/catalytic_earth/high_yield_family_lane_factory.py`,
`scripts/build_high_yield_family_lane_factory.py`, and
`tests/test_high_yield_family_lane_factory.py`.

## 2026-06-14: STAGE-1 RADICAL-SAM POST-PREFIX TOP-UP APPLIED; FMO/HEME WINDOWS NO-YIELD

Decision: do not replay capped or exhausted current lanes. The latest state showed
`non_heme_iron_2og_dioxygenase` capped at **250/250**, current copper selectors exhausted beyond
their fetched prefix, Mn/Fe SOD's guarded reviewed query already fully fetched at **252** rows, and
zinc post-apply previews redundant/no-yield. Use the existing Stage-1 cofactor mechanism-first
pipeline to process remaining non-confusable cofactor surface in bounded windows.

Implementation: added fetch-only row-window controls to `src/catalytic_earth/stage1_hole_sourcing.py`
and `scripts/stage1_source_holes.py`: `--record-offset-per-lane` and
`--record-limit-per-lane`. These controls affect only source fetch slicing before entry/Rhea fetch;
they do not alter disambiguation, source-trust tier evaluation, novelty, caps, or predictive
evidence. The Stage-1 `--apply` path now prints frozen current702 sha256 before and after append.

Apply result:
`PYTHONPATH=src python scripts/stage1_source_holes.py --holes radical_sam_enzyme cobalamin_radical_rearrangement --max-records-per-lane 180 --record-offset-per-lane 100 --record-limit-per-lane 40 --out artifacts/v3_stage1_radical_cobalamin_window100_40_sourcing_preview_current702_20260614.json --report work/stage1_radical_cobalamin_window100_40_sourcing_current702_20260614.md --apply`.
The preview fetched **160**, disambiguated **82**, applied **81** `radical_sam_enzyme` rows, held
**78** no-corroboration rows, skipped **0**, and cap-held **1** off-target `coa_acyltransferase`
row. `radical_sam_enzyme` moved **133 -> 214** combined; `cobalamin_radical_rearrangement` stayed
**144**.

Counts after apply: external bronze **6959 -> 7040**; combined label surface **7661 -> 7742**.
External-only split is **5816** seed-fingerprint rows and **1224** OOS rows. Combined
seed-fingerprint surface is **6046**, leaving **3954** to 10k by that surface convention. Strict
counters remain separate: **positive_bronze_count 6029**, **oos_bronze_count 1696**,
**silver_ready_count 0**, **silver_confirmed_count 17**, **projected_provisional_count 0**.

Guardrails held: all added rows are bronze, automation-curated, `uniprot:*`, `source_tier_0`, with
`predictive_evidence []`; EC/name/prose/Rhea/cofactor/feature handles remain excluded-context
admission evidence only; EC is never counted as a mechanism corroborator; dedup and novelty ran
against frozen current702 and the external bronze registry; frozen current702 stayed byte-unchanged
with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Row audit found
**0** problems across the **81** newly applied rows. Coverage audit reports **35** fingerprints,
Gini **0.1385**, holes `[]`, under-floor `[]`, over-cap `['metal_dependent_hydrolase']`, and
next-batch floor deficit **0**. Novelty replay reports **7040** expansion rows, decisions
`{'admit': 6584, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0648).

Follow-on scouts:
- FMO/heme window `0:30` fetched **125**, disambiguated **12**, final novelty-admitted **0**.
- FMO/heme window `30:30` fetched **107**, disambiguated **21**, final novelty-admitted **0**.
Do not apply those two artifacts. If continuing Stage-1 cofactor surface, preview
`radical_sam_enzyme` at `--record-offset-per-lane 140 --record-limit-per-lane 40` only while cap
room remains (**214/250**), or choose a clean under-cap family/source scout with explicit non-EC
mechanism corroborators.

References:
`artifacts/v3_stage1_radical_cobalamin_window100_40_sourcing_preview_current702_20260614.json`,
`work/stage1_radical_cobalamin_window100_40_sourcing_current702_20260614.md`,
`artifacts/v3_stage1_flavin_heme_window0_30_sourcing_preview_current702_20260614.json`,
`work/stage1_flavin_heme_window0_30_sourcing_current702_20260614.md`,
`artifacts/v3_stage1_flavin_heme_window30_30_sourcing_preview_current702_20260614.json`,
`work/stage1_flavin_heme_window30_30_sourcing_current702_20260614.md`,
`artifacts/v3_stage1_radical_sam_window100_40_row_guardrail_audit_current702_20260614.json`,
`work/stage1_radical_sam_window100_40_row_guardrail_audit_current702_20260614.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.json`,
`work/coverage_redundancy_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.json`,
and `work/novelty_admission_gate_audit_current702_20260614_stage1_radical_cobalamin_window100_40_applied.md`.

## 2026-06-13/14: NON-HEME IRON 2OG CAPPED; COPPER CURRENT LANES SOURCE-EXHAUSTED

Decision: continue the documented `non_heme_iron_2og_dioxygenase` windowed path only while it
remained under cap and mechanism-first gates admitted clean rows. EC/name/Rhea/keyword/prose/
feature handles remained excluded-context admission evidence only; EC was never counted and
`predictive_evidence` remained `[]`.

Apply results:
- window `140:10`: fetched **10**, mechanism **7**, applied **6**, throttled **1**, skipped **3**.
- window `150:10`: fetched **10**, mechanism **6**, applied **5**, throttled **1**, skipped **4**.
- window `160:10`: fetched **10**, mechanism **6**, applied **5**, throttled **1**, skipped **4**.
- window `170:10`: fetched **10**, mechanism **6**, applied **3**, throttled **3**, skipped **4**.
- window `180:10`: fetched **10**, mechanism **6**, applied **4**, held **1** no-corroboration
  row, throttled **2**, skipped **3**.
- window `190:10`: fetched **10**, mechanism **6**, gate-admitted **5**, applied **4**, held@cap
  **1**, held **3** no-corroboration rows, skipped **1**.

Counts after apply: external bronze **6932 -> 6959**; combined label surface **7634 -> 7661**.
`non_heme_iron_2og_dioxygenase` moved **223 -> 250**, exactly at cap **250**. External-only split
is **5735** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
**5965**, leaving **4035** to 10k by that surface convention. Strict counters remain separate:
**positive_bronze_count 5948**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**.

Guardrails held: all added rows are bronze, automation-curated, `uniprot:*`, `source_tier_0`, with
nested `predictive_evidence []`; dedup and novelty ran against frozen current702 and external
bronze; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; row audit found **0**
problems across all **250** non-heme 2OG rows. Coverage audit reports **35** fingerprints, Gini
**0.137**, holes `[]`, under-floor `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch
floor deficit **0**. Novelty replay reports **6959** expansion rows, decisions
`{'admit': 6503, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0655).

Follow-on decision: add only source-fetch window controls to the copper oxidoreductase runner, then
test whether the current lanes have post-prefix supply. The controls do not alter admission,
trust-tier evaluation, novelty, caps, or predictive evidence. The post-prefix preview
`--max-records-per-lane 320 --record-offset-per-lane 240 --record-limit-per-lane 40` fetched
**0** rows. Current copper lanes have only **153** laccase/oxidase rows and **69** amine oxidase
rows, so `copper_oxidoreductase` remains **140/250** but these source selectors are exhausted
beyond the already-fetched prefix. Do not replay them; scout alternate non-EC mechanism-corroborated
copper handles or choose another clean under-cap source-supply lane. Do not continue capped
non-heme 2OG under current cap policy.

References:
`artifacts/v3_non_heme_iron_2og_window140_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window150_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window160_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window170_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window180_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window190_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_capped_row_guardrail_audit_current702_20260613.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_non_heme_2og_capped_applied.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_non_heme_2og_capped_applied.json`,
and
`artifacts/v3_copper_oxidoreductase_postprefix_window240_40_sourcing_preview_current702_20260613.json`.

## 2026-06-13: NON-HEME IRON 2OG WINDOWED BRONZE EXTENSION APPLIED

Decision: after all former floor families were closed at cap, continue the 10k path with an
existing under-cap mechanism-first family lane rather than relaxing admission or repeating capped
lanes. `non_heme_iron_2og_dioxygenase` was **172/250** with prior source-supply evidence and a
duplicate-heavy first-window probe. The run added source-window controls to the non-heme 2OG source
runner: `--record-offset-per-lane` and `--record-limit-per-lane`. These controls are source-fetch
selectors only and do not change scope, admission, trust-tier evaluation, novelty, caps, or
predictive evidence. EC/name/Rhea/keyword/prose/feature handles remain excluded-context admission
evidence only; EC is never counted as a mechanism corroborator and `predictive_evidence` remains
`[]`.

Apply results:
- window `80:10`: fetched **20**, mechanism **18**, applied **17**, throttled **1**, skipped **2**.
- window `90:10`: fetched **20**, mechanism **13**, applied **13**, skipped **7**.
- window `100:10`: fetched **18**, mechanism **15**, applied **15**, skipped **3**.
- window `110:10`: fetched **10**, mechanism **3**, applied **3**, skipped **7**.
- window `120:10`: fetched **10**, mechanism **2**, applied **2**, skipped **8**.
- window `130:10`: fetched **10**, mechanism **1**, applied **1**, skipped **9**.

Counts after apply: external bronze **6881 -> 6932**; combined label surface **7583 -> 7634**.
`non_heme_iron_2og_dioxygenase` moved **172 -> 223** under cap **250**. External-only split is
**5708** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
**5938**, leaving **4062** to 10k by that surface convention. Strict counters remain separate:
**positive_bronze_count 5921**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**.

Guardrails held: all **51** added rows are bronze, automation-curated, `uniprot:*`,
`source_tier_0`, with `predictive_evidence []`; dedup and novelty ran against frozen current702 and
the external bronze registry; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; row audit found **0**
problems across all **223** non-heme 2OG rows. Coverage audit reports **35** fingerprints, Gini
**0.135**, holes `[]`, under-floor `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch
floor deficit **0**. Novelty replay reports **6932** expansion rows, decisions
`{'admit': 6476, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0658).

Follow-on decision: this lane still has **27** cap slots, but yield tapered after offset 100. If
continued, preview `--record-offset-per-lane 140 --record-limit-per-lane 10` first and apply only
if novelty/trust-tier/cap/leakage gates pass. If the next window is redundant or zero-yield, scout
a clean new family/source lane rather than padding balanced families.

References:
`artifacts/v3_non_heme_iron_2og_window80_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window90_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window100_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window110_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window120_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_window130_10_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_windowed_row_guardrail_audit_current702_20260613.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_non_heme_2og_windowed_applied.json`,
and
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_non_heme_2og_windowed_applied.json`.

## 2026-06-13: TIER-2 PFKB/BIOTIN/GLYCOSIDE FLOOR EXPANSION CAPPED

Decision: use unreviewed UniProt only through an explicit tier-2 source path, not by relaxing the
default reviewed/tier-0 mechanism-first pipeline. The cofactor/EC disambiguation path now accepts a
`source_tier` parameter; default behavior remains `source_tier_0`. Opt-in unreviewed lanes for
`glycoside_hydrolase`, `biotin_dependent_carboxylase`, and `pfkb_ribokinase_family` require
`--source-tier source_tier_2` and the existing `source_trust_tiers.evaluate_corroboration`
three-axis mechanism gate. EC/name/Rhea/keyword/prose/feature handles remain excluded-context
admission evidence only; EC is never counted as a mechanism corroborator and `predictive_evidence`
remains `[]`.

Apply results:
- `glycoside_hydrolase` windows `0:40`, `40:40`, and `80:40` applied **66** rows and moved
  **84 -> 150**. The final window admitted exactly the remaining **9** rows to cap.
- `biotin_dependent_carboxylase` windows `0:40` and `40:40` applied **66** rows and moved
  **84 -> 150**. PfkB/biotin row-window controls were added before continuation windows so
  already-applied source rows were skipped without changing admission.
- `pfkb_ribokinase_family` windows `0:80` and `80:40` applied **104** rows and moved
  **46 -> 150**.

Counts after apply: external bronze **6645 -> 6881**; combined label surface **7347 -> 7583**.
External-only split is **5657** seed-fingerprint rows and **1224** OOS rows. Combined
seed-fingerprint label surface is **5887**, leaving **4113** to 10k by that surface convention.
Strict counters remain separate: **positive_bronze_count 5870**, **oos_bronze_count 1696**,
**silver_ready_count 0**, **silver_confirmed_count 17**, **projected_provisional_count 0**.

Guardrails held: all **236** added rows are bronze, automation-curated, `uniprot:*`,
`source_tier_2`, with `predictive_evidence []`; dedup and novelty ran against frozen current702 and
the external bronze registry; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; row audit found **0**
problems. Coverage audit reports **35** fingerprints, Gini **0.1312**, holes `[]`, under-floor
`[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **0**. Novelty replay
reports **6881** expansion rows, decisions `{'admit': 6425, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0663).

Follow-on decision: all three former floor lanes are now **150/150** and should stay paused under
the current chemistry-confusable cap. Do not treat tier-2 bronze rows as silver, silver-ready, or
projected rows. The next 10k-path action should be a clean new family/source scout or spec, with
OOS preregistration if the fingerprint universe changes.

References:
`artifacts/v3_glycoside_hydrolase_tier2_unreviewed_window0_40_sourcing_preview_current702_20260613.json`,
`artifacts/v3_glycoside_hydrolase_tier2_unreviewed_window40_40_sourcing_preview_current702_20260613.json`,
`artifacts/v3_glycoside_hydrolase_tier2_unreviewed_window80_40_sourcing_preview_current702_20260613.json`,
`artifacts/v3_biotin_dependent_carboxylase_tier2_unreviewed_window0_40_sourcing_preview_current702_20260613.json`,
`artifacts/v3_biotin_dependent_carboxylase_tier2_unreviewed_window40_40_sourcing_preview_current702_20260613.json`,
`artifacts/v3_pfkb_ribokinase_family_tier2_unreviewed_window0_80_sourcing_preview_current702_20260613.json`,
`artifacts/v3_pfkb_ribokinase_family_tier2_unreviewed_window80_40_sourcing_preview_current702_20260613.json`,
`artifacts/v3_tier2_floor_expansion_row_guardrail_audit_current702_20260613.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_tier2_floor_expansion_capped_applied.json`,
and `artifacts/v3_novelty_admission_gate_audit_current702_20260613_tier2_floor_expansion_capped_applied.json`.

## 2026-06-13: WINDOWED COA/P450/MOLYBDOPTERIN CAP-FILLS APPLIED; ALL THREE NOW PAUSED AT CAP

Decision: use existing mechanism-first family pipelines and add only source-window controls to avoid
monolithic UniProt entry fetches. `--record-offset-per-lane` and `--record-limit-per-lane` were
exposed for CoA acyltransferase, cytochrome P450, and molybdopterin source runners. These controls
do not change scope, admission, trust-tier evaluation, novelty, caps, or predictive evidence.
EC/name/Rhea/keyword/prose/feature handles remain excluded-context admission evidence only; EC is
never counted as a mechanism corroborator and `predictive_evidence` remains `[]`.

Apply results:
- `molybdopterin_oxidoreductase` windows `80:8`, `88:8`, and `96:8` applied **43** rows and moved
  **207 -> 250**. The final window held **1** row at cap.
- `cytochrome_p450_monooxygenase` window `240:8` applied **2** rows and moved **248 -> 250**. The
  window held **4** rows at cap.
- `coa_acyltransferase` windows `80:8`, `88:8`, `96:8`, `104:8`, and `112:8` applied **62** rows
  and moved **188 -> 250**. The final window held **5** rows at cap.

Counts after apply: external bronze **6538 -> 6645**; combined label surface **7240 -> 7347**.
External-only split is **5421** seed-fingerprint rows and **1224** OOS rows. Combined
seed-fingerprint label surface is **5651**, leaving **4349** to 10k by that surface convention.
Strict counters remain separate: **positive_bronze_count 5634**, **oos_bronze_count 1696**,
**silver_ready_count 0**, **silver_confirmed_count 17**, **projected_provisional_count 0**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; dedup and novelty ran against frozen current702 and the external bronze
registry; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; row audit found **0**
problems across **750** CoA/P450/molybdopterin rows. Coverage audit reports **35** fingerprints,
Gini **0.1704**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **86**. Novelty replay reports
**6645** expansion rows, decisions `{'admit': 6189, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0686).

Follow-on decision: do **not** continue CoA, P450, or molybdopterin under the current cap policy;
all three are now **250/250**. A strict-kinase GHMP-like entry/Rhea scout generated **0** labels and
should not be wired next because GHMP is already **150/150** and registry-new supply was sparse.
Remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase **84/100**.
Prefer a genuinely new non-EC mechanism corroborator/source path for those floors, or scout/spec a
clean new family not already capped.

References:
`artifacts/v3_molybdopterin_oxidoreductase_window80_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_molybdopterin_oxidoreductase_window88_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_molybdopterin_oxidoreductase_window96_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_cytochrome_p450_window240_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_coa_acyltransferase_window80_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_coa_acyltransferase_window88_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_coa_acyltransferase_window96_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_coa_acyltransferase_window104_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_coa_acyltransferase_window112_8_sourcing_preview_current702_20260613.json`,
`artifacts/v3_windowed_capfills_row_guardrail_audit_current702_20260613.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_windowed_capfills_applied.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_windowed_capfills_applied.json`,
and `artifacts/v3_strict_kinase_ghmp_like_entry_mechanism_scout_current702_20260613.json`.

## 2026-06-13: ISOMERASE CAP-FILL APPLIED; ISOMERASE NOW PAUSED AT CAP

Decision: keep remaining under-floor work mechanism-first and do not relax EC-scope rules. A base
glycoside hydrolase page-2 continuation over rows **581-660** fetched **80** and admitted **0**
because all registry-new candidates lacked non-EC mechanism corroboration. The run added
`--only-alternate-name-lanes` to the glycoside source runner as a source-fetch-only selector; it
does not alter admission, trust-tier evaluation, novelty, caps, or predictive evidence. The first
untried alternate-only glycoside name window fetched **80** and admitted **0** because all **80**
rows lacked non-EC mechanism corroboration. Do not apply those artifacts.

Decision: after the current under-floor source paths no-yielded and the latest handoff had already
identified `cofactor_independent_isomerase` **142/150** as the smallest approved under-cap retry,
run the bounded 120-row cap-fill. EC 5.3, Isomerase keyword, Rhea equations, names, UniProt prose,
and feature annotations remain scope/admission excluded-context evidence. Counted mechanism axes
remain non-EC isomerase/domain/active-site/Rhea evidence. EC is never a counted corroborator and
`predictive_evidence` remains `[]`.

Apply:
`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md --apply`.
Result: fetched **405**, target mechanism-corroborated **91**, novelty gate admitted **80** before
the cap guard, applied **8**, held@cap **72**, novelty-throttled/rejected **11**, held **61**
off-target `nad_p_dehydrogenase` rows, held **90** no-corroboration rows, skipped **163**, and
recorded **0** fetch failures on the apply rerun. Final `cofactor_independent_isomerase` count is
**150/150** under the chemistry-confusable cap; do not continue this lane under the current cap
policy.

Counts after apply: external bronze **6530 -> 6538**; combined label surface **7232 -> 7240**.
External-only split is **5314** seed-fingerprint rows and **1224** OOS rows. Combined
seed-fingerprint label surface is **5544**, leaving **4456** to 10k by that surface convention.
Strict source-trust counters remain separate: **positive_bronze_count 5527**,
**oos_bronze_count 1696**, **silver_ready_count 0**, **silver_confirmed_count 17**,
**projected_provisional_count 0**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; dedup and novelty ran against frozen current702 and the external bronze
registry; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; row audit found **0**
problems across all **150** isomerase rows. Coverage audit reports **35** fingerprints, Gini
**0.1611**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **86**. Novelty replay reports
**6538** expansion rows, decisions `{'admit': 6082, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0697).

Follow-on decision: remaining floors are still PfkB **46/100**, biotin **84/100**, and glycoside
hydrolase **84/100**. Prefer genuinely new non-EC mechanism corroborator/source paths for those
lanes, or scout/spec a clean new family not already at cap. Isomerase, racemase, GHMP, ThDP, and
other chemistry-confusable 150-cap lanes at cap should stay paused unless the cap policy changes.

References:
`artifacts/v3_glycoside_hydrolase_page2_window580_80_sourcing_preview_current702_20260613.json`,
`work/glycoside_hydrolase_page2_window580_80_sourcing_current702_20260613.md`,
`artifacts/v3_glycoside_hydrolase_alt_name_only_window40_80_sourcing_preview_current702_20260613.json`,
`work/glycoside_hydrolase_alt_name_only_window40_80_sourcing_current702_20260613.md`,
`artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json`,
`work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`,
`artifacts/v3_cofactor_independent_isomerase_capfill_row_guardrail_audit_current702_20260613.json`,
`work/cofactor_independent_isomerase_capfill_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_isomerase_capfill_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_isomerase_capfill_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_isomerase_capfill_applied.json`,
and `work/novelty_admission_gate_audit_current702_20260613_isomerase_capfill_applied.md`.

## 2026-06-13: RACEMASE WINDOW400:80 BRONZE CAP-FILL APPLIED; RACEMASE NOW PAUSED AT CAP

Decision: after under-floor PfkB/biotin/glycoside source paths remained documented no-yield or
source-limited under mechanism-first gates, continue only the bounded non-PLP metal
racemase/epimerase cap-fill window identified in the previous handoff. EC 5.1, protein names,
Rhea equations, keywords, UniProt prose, and feature annotations remain scope/admission
excluded-context evidence. Counted mechanism axes remain non-EC racemase/epimerase mechanism text,
Rhea reaction/participant context, active-/binding-site evidence, metal/cofactor/cosubstrate
context, and domain/family profile. EC is never a counted corroborator and `predictive_evidence`
remains `[]`.

Apply:
`PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 400 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_metal_racemase_epimerase_non_plp_window400_80_sourcing_preview_current702_20260613.json --report work/metal_racemase_epimerase_non_plp_window400_80_sourcing_current702_20260613.md --apply`.
Result: fetched **80**, mechanism-corroborated **34**, novelty gate admitted **28** before cap,
applied **21**, held@cap **7**, novelty-throttled/rejected **6**, held **23** off-target
`nad_p_dehydrogenase` rows, held **22** no-corroboration rows, skipped **1**, and recorded **0**
fetch failures. Final `metal_racemase_epimerase_non_plp` count is **150/150** under the
chemistry-confusable cap; do not continue this lane under the current cap policy.

Counts after apply: external bronze **6509 -> 6530**; combined label surface **7211 -> 7232**.
External-only split is **5306** seed-fingerprint rows and **1224** OOS rows. Combined
seed-fingerprint label surface is **5536**, leaving **4464** to 10k by that surface convention.
Strict source-trust counters remain separate: **positive_bronze_count 5519**,
**oos_bronze_count 1696**, **silver_ready_count 0**, **silver_confirmed_count 17**,
**projected_provisional_count 0**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; dedup and novelty ran against frozen current702 and the external bronze
registry; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; row audit found **0**
problems across all **150** racemase rows. Coverage audit reports **35** fingerprints, Gini
**0.1619**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **86**. Novelty replay reports
**6530** expansion rows, decisions `{'admit': 6074, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0698).

Follow-on decision: a broad strict-kinase fingerprint should not be forced. A bounded entry/Rhea
scout over hexokinase/glucokinase, glycerol kinase, and galactokinase/mevalonate/homoserine
blocked in UniProt entry TLS handshake before artifact write; the completed source-supply TSV scout
is only a source scaffold and generated **0** labels. It ranks
`galactokinase_mevalonate_homoserine` first by reviewed supply (**613** total), but its first
20-row sample was only **1/20 registry-new**. Future work must run a deeper windowed source scout
and a small entry/Rhea mechanism corroborator scout before any fingerprint/ontology/OOS prereg work,
or return to genuinely new PfkB/biotin/glycoside source paths.

References:
`artifacts/v3_metal_racemase_epimerase_non_plp_window400_80_sourcing_preview_current702_20260613.json`,
`work/metal_racemase_epimerase_non_plp_window400_80_sourcing_current702_20260613.md`,
`artifacts/v3_metal_racemase_epimerase_non_plp_window400_80_row_guardrail_audit_current702_20260613.json`,
`work/metal_racemase_epimerase_non_plp_window400_80_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_window400_80_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_racemase_window400_80_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_racemase_window400_80_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_racemase_window400_80_applied.md`,
`artifacts/v3_strict_kinase_subclass_entry_fetch_blocker_after_racemase_cap_current702_20260613.json`,
`work/strict_kinase_subclass_entry_fetch_blocker_after_racemase_cap_current702_20260613.md`,
`artifacts/v3_strict_kinase_subclass_source_supply_scout_after_racemase_cap_current702_20260613.json`,
and `work/strict_kinase_subclass_source_supply_scout_after_racemase_cap_current702_20260613.md`.

## 2026-06-13: RACEMASE WINDOWED BRONZE TOP-UP APPLIED AFTER UNDER-FLOOR NO-YIELD SCOUTS

Decision: keep PfkB/biotin/glycoside floor work mechanism-first and do not relax EC-scope rules.
The run added optional source selectors for biotin alternate floor closure and glycoside alternate
names, but both are source/admission handles only and did not change predictive features or counted
corroboration. Biotin alternate preview fetched **139** and admitted **0**; glycoside alternate-name
window fetched **80** and admitted **0**; zinc hydratase under-cap preview fetched **160** and
admitted **0** because all **3** target rows were novelty-throttled as redundant. Do not apply those
artifacts.

Decision: add row-window support to the non-PLP metal racemase/epimerase source runner so unspent
UniProt search slices can be processed without refetching the already-applied 320-row prefix. The
new controls (`--record-offset-per-lane`, `--record-limit-per-lane`) are source-fetch controls
only. EC 5.1, protein names, Rhea equations, keywords, UniProt prose, and feature annotations remain
scope/admission excluded-context evidence; counted mechanism axes remain racemase/epimerase
mechanism text, Rhea isomerization/racemization context, active-/binding-site evidence, metal or
cofactorless context. EC is never a counted corroborator and `predictive_evidence` remains `[]`.

Apply:
`PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 320 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_metal_racemase_epimerase_non_plp_window320_80_sourcing_preview_current702_20260613.json --report work/metal_racemase_epimerase_non_plp_window320_80_sourcing_current702_20260613.md --apply`.
Result: fetched **80**, mechanism-corroborated **21**, applied **21**, held **49** off-target
`nad_p_dehydrogenase` rows, held **10** no-corroboration rows, skipped **0**, novelty-throttled
**0**, held@cap **0**, and recorded **0** fetch failures. Final
`metal_racemase_epimerase_non_plp` count is **129/150**.

Counts after apply: external bronze **6488 -> 6509**; combined label surface **7190 -> 7211**.
Honest counters stay separate: **positive_bronze 5515**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. External-only bronze split is **5285** seed-fingerprint
rows and **1224** OOS rows; remaining positive-bronze gap to 10k is **4485**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; dedup and novelty ran against frozen current702 and the external bronze
registry; EC was not counted as a mechanism axis; row audit found **0** problems across all **129**
racemase rows. Coverage audit reports **35** fingerprints, Gini **0.1643**, holes `[]`,
under-floor `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`,
over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **86**. Novelty replay
reports **6509** expansion rows, decisions `{'admit': 6053, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0701).

Follow-on decision: remaining under-floor lanes are still PfkB **46/100**, biotin **84/100**, and
glycoside hydrolase **84/100**. Prefer genuinely new non-EC mechanism corroborator/source paths for
those lanes. If no floor path is ready, a bounded racemase cap-fill continuation can start at
`--record-offset-per-lane 400 --record-limit-per-lane 80`, but cap 150 and novelty gates must be
inspected before any apply.

References:
`artifacts/v3_biotin_dependent_carboxylase_alt_floor_closure_sourcing_preview_current702_20260613.json`,
`work/biotin_dependent_carboxylase_alt_floor_closure_sourcing_current702_20260613.md`,
`artifacts/v3_glycoside_hydrolase_alt_name_window40_sourcing_preview_current702_20260613.json`,
`work/glycoside_hydrolase_alt_name_window40_sourcing_current702_20260613.md`,
`artifacts/v3_zinc_lyase_hydratase_under_cap_sourcing_preview_current702_20260613.json`,
`work/zinc_lyase_hydratase_under_cap_sourcing_current702_20260613.md`,
`artifacts/v3_metal_racemase_epimerase_topup_live_fetch_blocker_current702_20260613.json`,
`work/metal_racemase_epimerase_topup_live_fetch_blocker_current702_20260613.md`,
`artifacts/v3_metal_racemase_epimerase_non_plp_window320_80_sourcing_preview_current702_20260613.json`,
`work/metal_racemase_epimerase_non_plp_window320_80_sourcing_current702_20260613.md`,
`artifacts/v3_metal_racemase_epimerase_non_plp_window_row_guardrail_audit_current702_20260613.json`,
`work/metal_racemase_epimerase_non_plp_window_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_window320_80_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_racemase_window320_80_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_racemase_window320_80_applied.json`,
and `work/novelty_admission_gate_audit_current702_20260613_racemase_window320_80_applied.md`.

## 2026-06-13: GLYCOSIDE HYDROLASE FLOOR-WINDOW BRONZE APPLY COMPLETED

Decision: continue `glycoside_hydrolase` as an under-floor `label_factory_v1_35fp` family through
the existing mechanism-first admission pipeline, and add row-window/paging controls so the
source runner can process durable UniProt search slices instead of monolithic entry/Rhea fetches.
The new controls (`--record-offset-per-lane`, `--record-limit-per-lane`, `--query-pages-per-lane`)
are source-fetch controls only. EC 3.2.1, protein names, glycosidase keywords, Rhea equations, and
active-/binding-site annotations remain scope/admission context only; counted mechanism axes remain
reviewed glycosidic-bond hydrolysis reaction context, glycosidase family/domain text, and active-/
binding-site acid/base or nucleophile evidence. Growth goes only to
`data/registries/external_bronze_labels.json`; frozen current702 remains byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Apply:
`PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 500 --record-offset-per-lane 420 --record-limit-per-lane 80 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_floor500_window420_80_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_floor500_window420_80_sourcing_current702_20260613.md --apply`.
Result: fetched **80**, mechanism-corroborated **14**, applied **12**, held **66**
no-corroboration rows, skipped **0**, off-target held **0**, novelty-throttled **2**, held@cap
**0**, and recorded **0** fetch failures on the apply rerun. Final glycoside hydrolase count is
**84/150** and still below the 100 floor.

Counts after apply: external bronze **6476 -> 6488**; combined label surface **7178 -> 7190**.
Honest counters stay separate: **positive_bronze 5494**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. External-only bronze split is
**5264** seed-fingerprint rows and **1224** OOS rows; remaining positive-bronze gap to 10k is
**4506**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; EC/name/Rhea/keyword/prose/feature handles are excluded-context
admission evidence only; EC is never a counted corroborator; dedup and novelty ran against frozen
current702 and the external registry; glycosyltransferase, transglycosylase, phosphorylase, lyase,
side-EC, EC-only, and multi-signal rows are held. Row audit found **0** problems across all **84**
glycoside hydrolase rows. Coverage audit reports **35** fingerprints, Gini **0.1675**, holes `[]`,
under-floor `['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`,
over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **86**. Novelty replay
reports **6488** expansion rows, decisions `{'admit': 6032, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0703).

Follow-on decision: do not repeat the applied `420:80` glycoside window. A second-page preview
using `--query-pages-per-lane 2 --record-offset-per-lane 500 --record-limit-per-lane 80` fetched
**80** rows but mechanism-corroborated/admitted **0**; do not apply that artifact. Remaining floors
are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase **84/100**. The next 10k-path work
should build a genuinely new strict source/corroborator path for PfkB or biotin, or an alternate
glycoside source lane with non-EC mechanism corroboration.

References:
`artifacts/v3_glycoside_hydrolase_floor500_window420_80_sourcing_preview_current702_20260613.json`,
`work/glycoside_hydrolase_floor500_window420_80_sourcing_current702_20260613.md`,
`artifacts/v3_glycoside_hydrolase_floor500_window_row_guardrail_audit_current702_20260613.json`,
`work/glycoside_hydrolase_floor500_window_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_floor500_window_applied.md`,
`artifacts/v3_glycoside_hydrolase_page2_window500_80_sourcing_preview_current702_20260613.json`, and
`work/glycoside_hydrolase_page2_window500_80_sourcing_current702_20260613.md`.

## 2026-06-13: GLYCOSIDE HYDROLASE TOP-UP BRONZE APPLY COMPLETED

Decision: continue `glycoside_hydrolase` as an under-floor `label_factory_v1_35fp` family through
the existing mechanism-first admission pipeline. This was a top-up of the already-approved
fingerprint, not a new fingerprint-universe expansion. EC 3.2.1, protein names, glycosidase
keywords, Rhea equations, and active-/binding-site annotations remain scope/admission context only;
counted mechanism axes remain reviewed glycosidic-bond hydrolysis reaction context, glycosidase
family/domain text, and active-/binding-site acid/base or nucleophile evidence. Growth goes only to
`data/registries/external_bronze_labels.json`; frozen current702 remains byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Apply:
`PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 420 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_topup_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_topup_sourcing_current702_20260613.md --apply`.
Result: fetched **420**, mechanism-corroborated **27**, applied **27**, held **290**
no-corroboration rows, skipped **103**, off-target held **0**, novelty-throttled **0**, held@cap
**0**, and recorded **0** fetch failures. Final glycoside hydrolase count is **72/150** and still
below the 100 floor.

Counts after apply: external bronze **6449 -> 6476**; combined label surface **7151 -> 7178**.
Honest counters stay separate: **positive_bronze 5482**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. External-only bronze split is
**5252** seed-fingerprint rows and **1224** OOS rows; remaining positive-bronze gap to 10k is
**4518**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; EC/name/Rhea/keyword/prose/feature handles are excluded-context
admission evidence only; EC is never a counted corroborator; dedup and novelty ran against frozen
current702 and the external registry; glycosyltransferase, transglycosylase, phosphorylase, lyase,
side-EC, EC-only, and multi-signal rows are held. Row audit found **0** problems across all **72**
glycoside hydrolase rows. Coverage audit reports **35** fingerprints, Gini **0.1699**, holes `[]`,
under-floor `['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`,
over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **98**. Novelty replay
reports **6476** expansion rows, decisions `{'admit': 6020, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0704).

Follow-on decision: `glycoside_hydrolase` is closer to floor but still under-floor at **72/100**.
The runner rejects `--max-records-per-lane` above 500; a 500-row preview was stopped for closeout
before artifact write while in UniProt entry TLS/connect work. Next 10k-path work should retry that
500-row preview early in a run, or add paging/resume support before deeper windows. Remaining
floors are PfkB **46/100**, glycoside hydrolase **72/100**, and biotin **84/100**.

References:
`artifacts/v3_glycoside_hydrolase_topup_sourcing_preview_current702_20260613.json`,
`work/glycoside_hydrolase_topup_sourcing_current702_20260613.md`,
`artifacts/v3_glycoside_hydrolase_topup_row_guardrail_audit_current702_20260613.json`,
`work/glycoside_hydrolase_topup_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_topup_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_topup_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_topup_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_topup_applied.md`,
`artifacts/v3_glycoside_hydrolase_floor_topup_live_fetch_blocker_current702_20260613.json`, and
`work/glycoside_hydrolase_floor_topup_live_fetch_blocker_current702_20260613.md`.

## 2026-06-13: GLYCOSIDE HYDROLASE 35FP BRONZE LANE APPLIED

Decision: add `glycoside_hydrolase` as a deliberate `label_factory_v1_35fp` fingerprint only through
the mechanism-first admission pipeline. EC 3.2.1, protein names, glycosidase keywords, Rhea
equations, and active-/binding-site annotations remain scope/admission context only; counted
mechanism axes are reviewed glycosidic-bond hydrolysis reaction context, glycosidase family/domain
text, and active-/binding-site acid/base or nucleophile evidence. Growth goes only to
`data/registries/external_bronze_labels.json`; frozen current702 remains byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Implementation: added `glycoside_hydrolase` fingerprint, ontology node
`glycosidic_bond_hydrolysis`, deploy-missing context
`glycosidic_substrate_ordered_water_hydrolysis_context`, coverage source signature, source
module/script, disambiguation/trust-tier rules, leakage/coverage/ontology/source tests, and OOS
preregistration re-freeze
`artifacts/v3_external_hard_negative_next_tranche_preregistration_35fp_1025.json`.

Apply:
`PYTHONPATH=src python scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 240 --cap-ceiling 150 --out artifacts/v3_glycoside_hydrolase_sourcing_preview_current702_20260613.json --report work/glycoside_hydrolase_sourcing_current702_20260613.md --apply`.
Result: fetched **240**, mechanism-corroborated **45**, applied **45**, held **155**
no-corroboration rows, skipped **40**, off-target held **0**, novelty-throttled **0**, held@cap
**0**, and recorded **1** Rhea timeout (`P19531`). Final glycoside hydrolase count is **45/150**
and below floor.

Counts after apply: external bronze **6404 -> 6449**; combined label surface **7106 -> 7151**.
Honest counters stay separate: **positive_bronze 5438**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. External-only bronze split is
**5225** seed-fingerprint rows and **1224** OOS rows; remaining positive-bronze gap to 10k is
**4562**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; EC/name/Rhea/keyword/prose/feature handles are excluded-context
admission evidence only; EC is never a counted corroborator; dedup and novelty ran against frozen
current702 and the external registry; glycosyltransferase, transglycosylase, phosphorylase, lyase,
side-EC, EC-only, and multi-signal rows are held. Row audit found **0** problems across **45**
rows. Coverage audit reports **35** fingerprints, Gini **0.1753**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **125**. Novelty replay reports
**6449** expansion rows, decisions `{'admit': 5993, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0707).

Follow-on decision: glycoside hydrolase is now a valid but still under-floor positive family. The
next 10k-path work should close remaining floors through a gated glycoside hydrolase top-up/new
source path (**45/100**), PfkB (**46/100**), or biotin (**84/100**). Do not repeat the weak GHKL
histidine-kinase scout as a production lane; it found only **1** likely wireable reviewed row.

References:
`artifacts/v3_ghkl_histidine_kinase_mechanism_handle_scout_current702_20260613.json`,
`work/ghkl_histidine_kinase_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_glycoside_hydrolase_mechanism_handle_scout_current702_20260613.json`,
`work/glycoside_hydrolase_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_35fp_1025.json`,
`artifacts/v3_glycoside_hydrolase_sourcing_preview_current702_20260613.json`,
`work/glycoside_hydrolase_sourcing_current702_20260613.md`,
`artifacts/v3_glycoside_hydrolase_row_guardrail_audit_current702_20260613.json`,
`work/glycoside_hydrolase_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_glycoside_hydrolase_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_glycoside_hydrolase_applied.md`.

## 2026-06-13: MN/FE SUPEROXIDE DISMUTASE 34FP BRONZE EXPANSION APPLIED

Decision: promote the prior Mn/Fe SOD source/spec lane into a deliberate
`label_factory_v1_34fp` fingerprint only through the existing mechanism-first admission pipeline.
EC 1.15.1.1 and protein-name tokens remain scope/admission context only; counted mechanism axes are
Rhea/reaction superoxide dismutation, Mn/Fe metal or metal-site evidence, active/binding/metal-site
evidence, and SOD family/domain text. Growth goes only to
`data/registries/external_bronze_labels.json`; frozen current702 remains byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Implementation: added `manganese_iron_superoxide_dismutase` fingerprint, ontology node
`metal_superoxide_dismutation`, deploy-missing context
`mn_fe_superoxide_redox_dismutation_context`, source module/script, disambiguation/trust-tier rules,
leakage/ontology/source tests, and OOS preregistration re-freeze
`artifacts/v3_external_hard_negative_next_tranche_preregistration_34fp_1025.json`.

Initial apply:
`PYTHONPATH=src python scripts/source_manganese_iron_superoxide_dismutase_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_manganese_iron_superoxide_dismutase_sourcing_preview_current702_20260613.json --report work/manganese_iron_superoxide_dismutase_sourcing_current702_20260613.md --apply`.
Result: fetched **240**, mechanism-corroborated **181**, applied **164**, held **59**
no-corroboration rows, novelty-throttled **17**, off-target held **0**, held@cap **0**.

Bounded top-up:
`PYTHONPATH=src python scripts/source_manganese_iron_superoxide_dismutase_family.py --max-records-per-lane 320 --cap-ceiling 250 --out artifacts/v3_manganese_iron_superoxide_dismutase_topup_sourcing_preview_current702_20260613.json --report work/manganese_iron_superoxide_dismutase_topup_sourcing_current702_20260613.md --apply`.
Result: fetched **252**, skipped **164** already-existing rows, mechanism-corroborated **19**,
applied **2**, held **69** no-corroboration rows, novelty-throttled **17**, off-target held **0**,
held@cap **0**. Final SOD count is **166/250** and above floor.

Counts after apply: external bronze **6238 -> 6404**; combined label surface **6940 -> 7106**.
Honest counters stay separate: **positive_bronze 5393**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. External-only bronze split is
**5180** seed-fingerprint rows and **1224** OOS rows; remaining positive-bronze gap to 10k is
**4607**.

Guardrails held: every added row is bronze, automation-curated, `uniprot:*`, with
`predictive_evidence []`; EC/name/Rhea/keyword/prose/feature handles are excluded-context
admission evidence only; EC is never a counted corroborator; dedup and novelty ran against frozen
current702 and the external registry; Cu/Zn SOD, heme/peroxidase/cytoglobin/hemoglobin,
nitrite/nitric-oxygen dioxygenase, superoxide reductase, side-EC, EC-only, and multi-signal rows
are held. Row audit found **0** problems across **166** SOD rows. Coverage audit reports **34**
fingerprints, Gini **0.1608**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **70**. Novelty replay reports
**6404** expansion rows, decisions `{'admit': 5948, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0712).

Follow-on decision: do not repeat the SOD first-window or top-up previews. The current guarded
reviewed query is largely exhausted at **166** useful rows; the next 10k-path work should build a
new strict source/corroborator path for PfkB **46/100** or biotin **84/100**, or scout/spec the next
clean fingerprint family through fingerprint/ontology/OOS-preregistration/preview/apply gates.

References:
`artifacts/v3_manganese_iron_superoxide_dismutase_sourcing_preview_current702_20260613.json`,
`work/manganese_iron_superoxide_dismutase_sourcing_current702_20260613.md`,
`artifacts/v3_manganese_iron_superoxide_dismutase_topup_sourcing_preview_current702_20260613.json`,
`work/manganese_iron_superoxide_dismutase_topup_sourcing_current702_20260613.md`,
`artifacts/v3_manganese_iron_superoxide_dismutase_row_guardrail_audit_current702_20260613.json`,
`work/manganese_iron_superoxide_dismutase_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_mn_fe_sod_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_mn_fe_sod_applied.md`.

## 2026-06-13: MN/FE SUPEROXIDE DISMUTASE SOURCE BLOCKER CLEARED; 34FP SPEC WRITTEN

Decision: do not force the remaining PfkB/biotin floor deficits or repeat the bounded no-yield
under-cap probes. A PfkB/biotin alternate-source scout found only limited registry-new reviewed
supply and boundary-heavy samples. The cleaner 10k-path move is to revive the
`manganese_iron_superoxide_dismutase` candidate using a better source handle: the previous
breadth-feasibility scout undercounted Mn/Fe SOD because it required UniProt COFACTOR comments;
the corrected reviewed EC/name/cofactor query finds **252** rows.

Non-destructive scout results: the guarded Mn/Fe SOD query sampled **80** reviewed rows with **0**
JSON fetch failures. The sample had **80/80** registry-new rows, **80/80** RHEA:20696/superoxide
dismutation reaction context, **80/80** Mn/Fe metal context, **80/80** SOD family text, **77/80**
active/binding/metal-site evidence, and **0** explicit Cu/Zn/heme/side-EC boundary flags. No labels
were generated, no `--apply` was run, and frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Follow-on decision: wire `manganese_iron_superoxide_dismutase` only as a deliberate
`label_factory_v1_34fp` lane through the full pipeline: fingerprint spec,
`metal_superoxide_dismutation` ontology node, deploy-missing context
`mn_fe_superoxide_redox_dismutation_context`,
OOS preregistration re-freeze, disambiguation/trust-tier/leakage tests, non-destructive preview,
and explicit `--apply` only if novelty/dedup/governor/cap/trust-tier gates pass. Counted mechanism
axes should be Rhea/reaction superoxide dismutation, Mn/Fe metal or metal-site evidence,
active/binding/metal-site evidence, and SOD family/domain text. EC 1.15.1.1 and protein-name tokens
are scope/admission context only and never counted. Required guards: hold Cu/Zn SOD, heme/
cytoglobin/hemoglobin/peroxidase/nitrite/nitric-oxygen dioxygenase, superoxide reductase, side-EC,
EC-only, and multi-fingerprint-signal rows.

References:
`artifacts/v3_pfkb_biotin_alternate_source_scout_current702_20260613.json`,
`work/pfkb_biotin_alternate_source_scout_current702_20260613.md`,
`artifacts/v3_manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.json`,
`work/manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.md`,
`artifacts/v3_manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.json`,
`work/manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.md`.

## 2026-06-13: BOUNDED UNDER-CAP PREVIEWS CLEAR FETCH BLOCKER BUT ADMIT 0 ROWS

Decision: after user feedback, resume the previous blocked run and isolate the live-preview issue
instead of treating it as final. The family runners do complete and write preview artifacts at small
`--max-records-per-lane` values; the earlier no-artifact behavior came from larger sequential
UniProt entry/Rhea evidence-fetch workloads before artifact write. No `--apply` was run because all
bounded preview windows yielded **0 novelty-admitted labels**.

Bounded preview results:
`cofactor_independent_isomerase` at 5 rows/lane fetched **14**, target mechanism-corroborated **0**,
admitted **0**; the same lane at 20 rows/lane fetched **67**, mechanism **0**, admitted **0**.
`coa_acyltransferase` at 20 rows/lane fetched **75**, mechanism **0**, admitted **0**.
`non_heme_iron_2og_dioxygenase` at 20 rows/lane fetched **66**, mechanism **3**, admitted **0**;
all 3 were novelty-throttled as `redundant_no_novelty_signal`. `molybdopterin_oxidoreductase` at
20 rows/lane fetched **67**, mechanism **2**, admitted **0**; both were throttled as redundant.
`zinc_lyase_hydratase` at 20 rows/lane fetched **20**, mechanism **0**, admitted **0**.
`copper_oxidoreductase` at 20 rows/lane fetched **40**, mechanism **1**, admitted **0**; the row was
throttled as redundant.

Counts remain external bronze **6238**, combined surface **6940**, honest counters
**positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. Frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Follow-on decision: do not repeat these same bounded first-window probes. Next work should build a
new PfkB/biotin source path with stronger mechanism corroboration, run a targeted deeper under-cap
extension only when enough closeout time remains, or start a new-family mechanism/source-supply
scout/spec if evidence is cleaner than further top-ups.

References:
`artifacts/v3_under_cap_bounded_preview_no_yield_current702_20260613.json`,
`work/under_cap_bounded_preview_no_yield_current702_20260613.md`,
`artifacts/v3_cofactor_independent_isomerase_micro_capfill_sourcing_preview_current702_20260613.json`,
`artifacts/v3_cofactor_independent_isomerase_bounded_capfill_sourcing_preview_current702_20260613.json`,
`artifacts/v3_coa_acyltransferase_bounded_extension_sourcing_preview_current702_20260613.json`,
`artifacts/v3_non_heme_iron_2og_bounded_extension_sourcing_preview_current702_20260613.json`,
`artifacts/v3_molybdopterin_oxidoreductase_bounded_extension_sourcing_preview_current702_20260613.json`,
`artifacts/v3_zinc_lyase_hydratase_bounded_extension_sourcing_preview_current702_20260613.json`,
`artifacts/v3_copper_oxidoreductase_bounded_extension_sourcing_preview_current702_20260613.json`.

## 2026-06-13: UNDER-CAP EXTENSION PREVIEWS BLOCKED; NO REGISTRY WRITE

Decision: do not relax the mechanism-first rules to force `pfkb_ribokinase_family` or
`biotin_dependent_carboxylase` floor closure. Their current strict reviewed source paths remain
exhausted. This run attempted bounded approved under-cap extension/cap-fill previews instead, but
the live UniProt fetch/evidence-extraction path did not return preview artifacts quickly enough for a
safe inspect/apply/validate cycle. No `--apply` was run and no labels changed.

Attempted commands:
`PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 500 --cap-ceiling 250 --out artifacts/v3_coa_acyltransferase_extension_sourcing_preview_current702_20260613.json --report work/coa_acyltransferase_extension_sourcing_current702_20260613.md`,
then the same CoA preview at `--max-records-per-lane 280`, then
`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`.
All were terminated after producing no preview artifact; frozen current702 stayed byte-unchanged
with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Counts remain external bronze **6238**, combined surface **6940**, honest counters
**positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. Current under-cap approved lanes include `cofactor_independent_isomerase` 142/150,
`coa_acyltransferase` 188/250, `non_heme_iron_2og_dioxygenase` 172/250,
`molybdopterin_oxidoreductase` 207/250, and `copper_oxidoreductase` 140/250. Do not add more P450
without explicit new reaction/organism justification because it is 248/250.

Follow-on decision: retry the smallest bounded cap-fill first:
`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`.
Apply only after inspecting the generated `floor_projection`, novelty gate, held@cap, trust-tier,
namespace/tier/review-status, `predictive_evidence`, and excluded-context fields.

References:
`artifacts/v3_under_cap_extension_live_fetch_blocker_current702_20260613.json`,
`work/under_cap_extension_live_fetch_blocker_current702_20260613.md`.

## 2026-06-13: P450 + COPPER EXTENSION BRONZE APPLIES COMPLETED

Decision: after the strict PfkB floor-extension scout found no new admissible rows and the biotin
floor-closure path remained source-limited, use existing non-confusable, already approved
mechanism-first extension lanes with remaining reviewed supply before attempting a new fingerprint
family. Growth went only to `data/registries/external_bronze_labels.json`; frozen current702 stayed
byte-unchanged with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

P450 extension command:
`PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json --report work/cytochrome_p450_extension_sourcing_current702_20260613.md`.
Result: fetched **337**, target mechanism-corroborated **189**, applied **138**,
no-corroboration holds **35**, duplicate/current-registry skips **113**, novelty-throttled **51**,
held@cap **0**, off-target held **0**. `cytochrome_p450_monooxygenase` **110 -> 248** under cap
250.

Copper extension command:
`PYTHONPATH=src python scripts/source_copper_oxidoreductase_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json --report work/copper_oxidoreductase_extension_sourcing_current702_20260613.md`.
Result: fetched **222**, target mechanism-corroborated **81**, applied **21**,
no-corroboration holds **20**, duplicate/current-registry skips **121**, novelty-throttled **60**,
held@cap **0**, off-target held **0**. `copper_oxidoreductase` **119 -> 140**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose/feature handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; per-fingerprint cap 250 held. Row audits found **0** problems
across **138** P450 and **21** copper rows; every row has cofactor/cosubstrate, domain/family,
active-site/residue-role, and Rhea participant axes.

External bronze **6079 -> 6238**; combined surface **6781 -> 6940**. Honest counters after apply
are **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**; do not merge them. External-only bronze split is 5014 seed-fingerprint rows and
1224 OOS rows. Fresh post-apply coverage/redundancy audit reports **6940** combined labels,
**33** fingerprints, seed positives **5227**, fingerprint Gini **0.1633**, holes `[]`,
under-floor `['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **70**. Novelty replay reports
**6238** expansion rows, decisions `{'admit': 5782, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.0731).

Follow-on decision: do **not** add more P450 without explicit new reaction/organism justification
because it is now **248/250**. PfkB remains **46/100** and biotin remains **84/100**, but current
reviewed strict lanes are exhausted; next work should design a genuinely new PfkB/biotin source
path with stronger corroboration or scout/spec a new fingerprint family if evidence is cleaner than
further balanced-lane top-ups.

References:
`artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json`,
`work/cytochrome_p450_extension_sourcing_current702_20260613.md`,
`artifacts/v3_cytochrome_p450_extension_row_guardrail_audit_current702_20260613.json`,
`work/cytochrome_p450_extension_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json`,
`work/copper_oxidoreductase_extension_sourcing_current702_20260613.md`,
`artifacts/v3_copper_oxidoreductase_extension_row_guardrail_audit_current702_20260613.json`,
`work/copper_oxidoreductase_extension_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_p450_copper_extensions_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_p450_copper_extensions_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_p450_copper_extensions_applied.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: STRICT PFKB/RIBOKINASE-FAMILY 33FP BRONZE EXPANSION APPLIED

Decision: continue the strict kinase-subclass path instead of broad-wiring EC 2.7. The latest
handoff left `pfkb_ribokinase_family` as a guarded candidate after the PfkA apply; this run
tightened the boundary guard and applied PfkB through the full mechanism-first pipeline. Growth went
only to `data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with
sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Added `pfkb_ribokinase_family` fingerprint spec and mapped it to ontology family `pfkb`; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_33fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`. EC 2.7.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from ATP/ADP
phosphoryl-transfer Rhea participant context with PfkB/ribokinase-family acceptors, PfkB family
text, ATP/Mg/substrate active-/binding-site evidence, cofactor/cosubstrate handles, or
structure-compatible evidence. Protein kinases, two-component histidine kinases,
hydrolase/nuclease rows, NDK, dNK, ASKHA, GHMP, PfkA, side-EC, and multi-fingerprint rows are held.
Generic `fructokinase` is not counted as PfkB family evidence because it matched inside
`6-phosphofructokinase` and shadowed PfkA.

PfkB apply command:
`PYTHONPATH=src python scripts/source_pfkb_ribokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **88**, target mechanism-corroborated **46**, applied **46**,
no-corroboration holds **36**, disambiguation skips **2**, off-target held **4** as
`askha_sugar_acetate_kinase`, novelty-throttled/rejected **0**, held@cap **0**, duplicate skipped
**0**. `pfkb_ribokinase_family` **0 -> 46** and remains under floor by 54.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose/feature handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; per-fingerprint cap 150 held. Row audit
`artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json` found **0**
problems across all **46** PfkB rows; all rows have active-site/residue-role,
cofactor/cosubstrate, domain/family, and Rhea participant axes. External bronze **6033 -> 6079**;
combined surface **6735 -> 6781**. Honest counters after apply are **positive_bronze 5085**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge
them. External-only bronze split is 4855 seed-fingerprint rows and 1224 OOS rows. Fresh post-PfkB
coverage/redundancy audit reports **6781** combined labels, **33** fingerprints, seed positives
**5085**, fingerprint Gini **0.162**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **70**. Novelty replay reports
**6079** expansion rows, decisions `{'admit': 5623, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.075).

Follow-on decision: `pfkb_ribokinase_family` is now a real 33fp lane but still below the 100 floor.
Do **not** broad-wire EC 2.7 or merge ASKHA/GHMP/NDK/dNK/Pfk kinase subclasses. A post-apply
floor-extension scout
`artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json` reran the
strict reviewed lane with `--max-records-per-lane 500` and found **0** new PfkB labels (48 skipped
as already covered, 36 no-corroboration holds, 4 off-target ASKHA rows), so the current reviewed
PfkB query is exhausted at **46/100**. Next work should return to the biotin 16-row deficit, design a
genuinely new PfkB source/handle path with stronger corroboration, or choose a new non-kinase
10k-path family through the same fingerprint/ontology/preregistration/preview/apply gates.

References:
`src/catalytic_earth/pfkb_ribokinase_family_sourcing.py`,
`scripts/source_pfkb_ribokinase_family.py`,
`tests/test_pfkb_ribokinase_family_sourcing.py`,
`artifacts/v3_pfkb_ribokinase_family_sourcing_preview_current702.json`,
`work/pfkb_ribokinase_family_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`,
`artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json`,
`work/pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json`,
`work/pfkb_ribokinase_family_floor_extension_scout_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_pfkb_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_pfkb_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfkb_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_pfkb_applied.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: STRICT PFKA PHOSPHOFRUCTOKINASE 32FP BRONZE EXPANSION APPLIED

Decision: continue the strict kinase-subclass path instead of broad-wiring EC 2.7. The latest
handoff selected `pfka_phosphofructokinase` after the dNK apply and PfkA/PfkB scout; this run
applied PfkA through the full mechanism-first pipeline. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Added `pfka_phosphofructokinase` fingerprint spec and mapped it to ontology family `pfka`; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_32fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`. EC 2.7.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from ATP/ADP
phosphoryl-transfer Rhea participant context with fructose-6-phosphate, PfkA/ATP-dependent
6-phosphofructokinase family text, ATP/Mg/substrate active-/binding-site evidence,
cofactor/cosubstrate handles, or structure-compatible evidence. Protein kinases, two-component
histidine kinases, hydrolase/nuclease rows, NDK, dNK, ASKHA, GHMP, PfkB/ribokinase, and
multi-fingerprint rows are held.

PfkA apply command:
`PYTHONPATH=src python scripts/source_pfka_phosphofructokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **233**, applied **150**,
no-corroboration holds **5**, disambiguation skips **2**, novelty-throttled/rejected **0**,
held@cap **83**, off-target held **0**, duplicate skipped **0**. `pfka_phosphofructokinase`
**0 -> 150**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose/feature handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; per-fingerprint cap 150 held. Row audit
`artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json` found **0**
problems across all **150** PfkA rows; all rows have active-site/residue-role,
cofactor/cosubstrate, domain/family, and Rhea participant axes. External bronze **5883 -> 6033**;
combined surface **6585 -> 6735**. Honest counters after apply are **positive_bronze 5039**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge
them. Fresh post-PfkA coverage/redundancy audit reports **6735** combined labels, **32**
fingerprints, seed positives **5039**, fingerprint Gini **0.1465**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **16**. Novelty replay reports **6033** expansion rows, decisions
`{'admit': 5577, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0756).

Follow-on decision: `pfkb_ribokinase_family` is only a guarded candidate, not an approved apply lane
yet. The scaffold `work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md` records the
source basis from the previous scout: reviewed supply **85**, sampled likely wireable **28/40**,
boundary signal **0/40**, and active-/binding-site context **28/40**. Tighten/re-scout PfkB before
any 33fp pipeline, or choose a stronger current scaling-plan family if evidence is cleaner. Do
**not** broad-wire EC 2.7 or merge ASKHA/GHMP/NDK/dNK/Pfk kinase subclasses.

References:
`src/catalytic_earth/pfka_phosphofructokinase_sourcing.py`,
`scripts/source_pfka_phosphofructokinase_family.py`,
`tests/test_pfka_phosphofructokinase_sourcing.py`,
`artifacts/v3_pfka_phosphofructokinase_sourcing_preview_current702.json`,
`work/pfka_phosphofructokinase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`,
`artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json`,
`work/pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_pfka_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_pfka_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_pfka_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_pfka_applied.md`,
`work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: STRICT DEOXYNUCLEOSIDE KINASE 31FP BRONZE EXPANSION APPLIED

Decision: continue the strict kinase-subclass path instead of broad-wiring EC 2.7. The latest
handoff selected `deoxynucleoside_kinase` after ASKHA/GHMP; this run applied that lane through the
full mechanism-first pipeline and then ran a non-destructive PfkA/PfkB scout. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Added `deoxynucleoside_kinase` fingerprint spec and mapped it to ontology family `dnk`; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_31fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_31fp_1025.json`. EC 2.7.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from ATP/ADP
phosphoryl-transfer Rhea participant context with deoxynucleoside substrates, dNK/thymidine/
deoxycytidine/deoxyguanosine kinase family text, ATP/substrate active-/binding-site evidence,
cofactor/cosubstrate handles, or structure-compatible evidence. Protein kinases, two-component
histidine kinases, hydrolase/nuclease rows, NDK, ASKHA, GHMP, PfkA/PfkB, and multi-fingerprint rows
are held.

dNK apply command:
`PYTHONPATH=src python scripts/source_deoxynucleoside_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **237**, applied **150**, disambiguation
holds **0**, novelty-throttled/rejected **0**, held@cap **87**, off-target held **0**, duplicate
skipped **0**. `deoxynucleoside_kinase` **0 -> 150**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose/feature handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; per-fingerprint cap 150 held. Row audit
`artifacts/v3_deoxynucleoside_kinase_row_guardrail_audit_current702_20260613.json` found **0**
problems across all **150** dNK rows; all rows have active-site/residue-role, cofactor/cosubstrate,
domain/family, and Rhea participant axes. External bronze **5733 -> 5883**; combined surface
**6435 -> 6585**. Honest counters after apply are **positive_bronze 4889**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh post-dNK
coverage/redundancy audit reports **6585** combined labels, **31** fingerprints, seed positives
**4889**, fingerprint Gini **0.1534**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **16**. Novelty replay reports **5883** expansion rows, decisions
`{'admit': 5427, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0775).

Follow-on decision: `pfka_phosphofructokinase` is the next strict kinase split, based on
`artifacts/v3_strict_kinase_subclass_source_scout_after_dnk_current702_20260613.json`, which
generated **0** labels and wrote no registry. PfkA reviewed supply **386**, sampled likely wireable
**40/40**, boundary signal **0/40**; PfkB reviewed supply **85**, sampled likely wireable
**28/40**, boundary signal **0/40**. Do **not** broad-wire EC 2.7 or merge ASKHA/GHMP/NDK/dNK/Pfk
kinase subclasses. Next run should wire PfkA only through the full 32fp path: fingerprint/ontology
spec, OOS prereg re-freeze, disambiguation guards/tests, non-destructive preview, and gated apply.

References:
`src/catalytic_earth/deoxynucleoside_kinase_sourcing.py`,
`scripts/source_deoxynucleoside_kinase_family.py`,
`tests/test_deoxynucleoside_kinase_sourcing.py`,
`artifacts/v3_deoxynucleoside_kinase_sourcing_preview_current702.json`,
`work/deoxynucleoside_kinase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_31fp_1025.json`,
`artifacts/v3_deoxynucleoside_kinase_row_guardrail_audit_current702_20260613.json`,
`work/deoxynucleoside_kinase_row_guardrail_audit_current702_20260613.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_dnk_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_dnk_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_dnk_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_dnk_applied.md`,
`artifacts/v3_strict_kinase_subclass_source_scout_after_dnk_current702_20260613.json`,
`work/strict_kinase_subclass_source_scout_after_dnk_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: STRICT ASKHA + GHMP 30FP BRONZE EXPANSIONS APPLIED

Decision: continue the strict kinase-subclass path instead of broad-wiring EC 2.7. The latest
handoff selected `askha_sugar_acetate_kinase`; after ASKHA applied cleanly and time remained, this
run applied the next clean scout lane, `ghmp_small_molecule_kinase`. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

**ASKHA lane.** Added `askha_sugar_acetate_kinase` fingerprint spec and `askha` ontology node;
bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_29fp`;
re-froze OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_29fp_1025.json`. EC 2.7.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from ATP/ADP
sugar-or-acetate phosphoryl-transfer Rhea participant context, ASKHA/sugar kinase/acetate kinase
family text, ATP/Mg or substrate active-/binding-site evidence, cofactor/cosubstrate handles, or
structure-compatible evidence. Protein kinases, two-component histidine kinases, hydrolase/nuclease
rows, NDK, dNK, GHMP/Pfk, and multi-fingerprint rows are held.

ASKHA apply command:
`PYTHONPATH=src python scripts/source_askha_sugar_acetate_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **227**, applied **150**, no-corroboration
holds **9**, novelty-throttled **7**, held@cap **70**, off-target held **0**, duplicate skipped
**0**. `askha_sugar_acetate_kinase` **0 -> 150**.

**GHMP lane.** Added `ghmp_small_molecule_kinase` fingerprint spec and `ghmp` ontology node;
bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_30fp`;
re-froze OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_30fp_1025.json`. EC 2.7.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from ATP/ADP
small-molecule phosphoryl-transfer Rhea participant context, GHMP/homoserine/mevalonate/
galactokinase family text, ATP/Mg or substrate active-/binding-site evidence, cofactor/cosubstrate
handles, or structure-compatible evidence. Protein kinases, two-component histidine kinases,
hydrolase/nuclease rows, ASKHA, NDK, dNK, Pfk, and multi-fingerprint rows are held.

GHMP apply command:
`PYTHONPATH=src python scripts/source_ghmp_small_molecule_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **228**, applied **150**, no-corroboration
holds **10**, novelty-throttled **0**, held@cap **78**, off-target held **0**, duplicate skipped
**0**. `ghmp_small_molecule_kinase` **0 -> 150**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose/feature handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; per-fingerprint cap 150 held. Row audits found **0** problems
across all **150** ASKHA and **150** GHMP rows; both lanes have active-site/residue-role,
cofactor/cosubstrate, domain/family, and Rhea participant axes on every admitted row. External
bronze **5433 -> 5733**; combined surface **6135 -> 6435**. Honest counters after apply are
**positive_bronze 4739**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**; do not merge them. Fresh post-GHMP coverage/redundancy audit reports **6435**
combined labels, **30** fingerprints, seed positives **4739**, fingerprint Gini **0.1534**, holes
`[]`, under-floor `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, and
next-batch floor deficit **16**. Novelty replay reports **5733** expansion rows, decisions
`{'admit': 5277, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0795).

Follow-on decision: `deoxynucleoside_kinase` is the next strict kinase split. The scaffold
`work/deoxynucleoside_kinase_next_lane_spec_current702_20260613.md` records reviewed supply **278**,
sampled likely wireable **39/40**, boundary signal **1/40**, required guards, and the exact 31fp
implementation path. Do **not** broad-wire EC 2.7 or merge ASKHA/GHMP/NDK/dNK/Pfk kinase
subclasses.

References:
`src/catalytic_earth/askha_sugar_acetate_kinase_sourcing.py`,
`scripts/source_askha_sugar_acetate_kinase_family.py`,
`tests/test_askha_sugar_acetate_kinase_sourcing.py`,
`src/catalytic_earth/ghmp_small_molecule_kinase_sourcing.py`,
`scripts/source_ghmp_small_molecule_kinase_family.py`,
`tests/test_ghmp_small_molecule_kinase_sourcing.py`,
`artifacts/v3_askha_sugar_acetate_kinase_sourcing_preview_current702.json`,
`work/askha_sugar_acetate_kinase_sourcing_current702.md`,
`artifacts/v3_ghmp_small_molecule_kinase_sourcing_preview_current702.json`,
`work/ghmp_small_molecule_kinase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_29fp_1025.json`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_30fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_ghmp_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_ghmp_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_ghmp_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_ghmp_applied.md`,
`work/deoxynucleoside_kinase_next_lane_spec_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: BIOTIN FLOOR-CLOSURE + STRICT NDK 28FP BRONZE EXPANSION APPLIED

Decision: the biotin floor-closure scout did not find enough reviewed source supply to close the
100-label floor under the mandatory ATP + hydrogencarbonate/CO2/carboxylation gate, so the run
applied only the 3 safe biotin rows and then followed the handoff fallback: split a strict kinase
subclass instead of broad-wiring EC 2.7. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

**Biotin floor closure.** Added an optional Rhea-first source lane to
`scripts/source_biotin_dependent_carboxylase_family.py` and
`src/catalytic_earth/biotin_dependent_carboxylase_sourcing.py`. Command:
`PYTHONPATH=src python scripts/source_biotin_dependent_carboxylase_family.py --include-floor-closure-lanes --max-records-per-lane 500 --cap-ceiling 150 --out artifacts/v3_biotin_dependent_carboxylase_floor_closure_scout_current702_20260613.json --report work/biotin_dependent_carboxylase_floor_closure_scout_current702_20260613.md --apply`.
The Rhea-first lane fetched 105 reviewed rows already inside the existing candidate universe.
Result: fetched **126**, applied **3**, held **42** no-corroboration rows, skipped **81** duplicates,
off-target held **0**. `biotin_dependent_carboxylase` **81 -> 84**; floor deficit **16** remains.
Do not admit EC 6.3.4.15 biotin-protein ligase rows, and do not relax the carboxylation gate to
close this floor.

**Strict NDK lane.** Broad EC 2.7 remains blocked. A strict NDK scout excluding protein-kinase
EC 2.7.11, two-component histidine kinase EC 2.7.13, hydrolase/nuclease EC 3.*, and NMP kinase side
ECs found **714** reviewed rows with **80/80** sampled entries wireable and **0** sampled side-EC
boundaries. Added `nucleoside_diphosphate_kinase` fingerprint spec and
`phosphohistidine_ntp_transfer` ontology family; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_28fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_28fp_1025.json`. EC 2.7.4.6 is
scope-only (`ec_scope_hint`, never counted). Counted corroboration comes from Rhea NTP/NDP
phosphoryl-transfer participant text, NDK family/domain/name text, active-site phosphohistidine or
catalytic-His evidence, ATP/ADP/GTP/GDP binding-site context, or structure. Protein kinases,
two-component histidine kinases, hydrolase/nuclease side rows, adenylate/guanylate/NMP kinase side
rows, and multi-fingerprint rows are held.

NDK apply command:
`PYTHONPATH=src python scripts/source_nucleoside_diphosphate_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **238**, gate-admitted **237**, applied
**150**, held@cap **87**, novelty-throttled **1**, disambiguation holds **0**, off-target held
**0**, duplicate skipped **0**. `nucleoside_diphosphate_kinase` **0 -> 150** (chemistry-confusable
cap 150; floor reached). External bronze **5280 -> 5433** across the run; combined surface
**5982 -> 6135**.

Guardrails held: all new rows are `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose/feature handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; per-fingerprint cap 150 held. Row audits found **0** problems across
all **84** biotin and **150** NDK rows. Honest counters after apply are
**positive_bronze 4439**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**; do not merge them. Fresh post-NDK coverage/redundancy audit reports **6135**
combined labels, **28** fingerprints, seed positives **4439**, fingerprint Gini **0.1608**, holes
`[]`, under-floor `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, and
next-batch floor deficit **16**. Novelty replay reports **5433** expansion rows, decisions
`{'admit': 4977, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0839).

Follow-on decision from the same run: a non-destructive strict kinase-subclass scout
(`artifacts/v3_strict_kinase_subclass_source_scout_after_ndk_current702_20260613.json`) generated
no labels and wrote no registry, but selected `askha_sugar_acetate_kinase` as the next full
pipeline candidate. Sampled reviewed supply / likely wireable / boundary signals:
`deoxynucleoside_kinase` **278 / 39-of-40 / 1**, `ghmp_small_molecule_kinase`
**613 / 37-of-40 / 0**, and `askha_sugar_acetate_kinase` **667 / 39-of-40 / 0**. Next run should
wire ASKHA only through the full 29fp path: fingerprint/ontology spec, OOS prereg re-freeze,
disambiguation guards/tests, non-destructive preview, and gated apply. Do **not** broad-wire EC 2.7,
merge kinase subclasses, or spend time trying to force the remaining biotin 16-row deficit unless a
genuinely new source can satisfy the same mechanism-first gate.

References:
`src/catalytic_earth/nucleoside_diphosphate_kinase_sourcing.py`,
`scripts/source_nucleoside_diphosphate_kinase_family.py`,
`tests/test_nucleoside_diphosphate_kinase_sourcing.py`,
`artifacts/v3_biotin_dependent_carboxylase_floor_closure_scout_current702_20260613.json`,
`artifacts/v3_nucleoside_diphosphate_kinase_strict_subclass_scout_current702_20260613.json`,
`artifacts/v3_nucleoside_diphosphate_kinase_sourcing_preview_current702.json`,
`work/nucleoside_diphosphate_kinase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_28fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_ndk_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_ndk_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_ndk_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_ndk_applied.md`,
`artifacts/v3_strict_kinase_subclass_source_scout_after_ndk_current702_20260613.json`,
`work/strict_kinase_subclass_source_scout_after_ndk_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: BIOTIN-DEPENDENT CARBOXYLASE 27FP BRONZE EXPANSION APPLIED

Decision: broad EC 2.7 kinase remains blocked by subclass mixing, so this run selected the guarded
`biotin_dependent_carboxylase` lane from the latest handoff. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `biotin_dependent_carboxylase` fingerprint spec and
`biotin_carboxyl_transfer` ontology family; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_27fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_27fp_1025.json`. EC 6.4.1 /
6.3.4 is scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from
biotin/biotinyl-Lys cofactor or modified-residue evidence, Rhea ATP/hydrogencarbonate/
carboxybiotin participant text, carboxylase family text, active-/binding-site evidence, or
structure. Kinase/phosphotransferase, hydrolase, transferase side EC, non-scope side EC,
PLP/ThDP/Mo/heme/flavin, multi-fingerprint rows, and EC 6.3.4.15 biotin-protein ligases are held.

**Live apply and correction.** Command:
`PYTHONPATH=src python scripts/source_biotin_dependent_carboxylase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
The first pass fetched **126** and admitted 93, but row audit caught **12** EC 6.3.4.15
biotin-protein ligase rows with biotin/ATP annotations and no hydrogencarbonate/carboxybiotin
carboxylation reaction. The rule now requires ATP-dependent carboxylation chemistry for every
`biotin_dependent_carboxylase` import, and those 12 rows were removed from both the registry append
and preview artifact. Corrected result: target mechanism-corroborated **81**, novelty-admitted/
applied **81**, **44** no-corroboration holds, off-target held **0**, novelty-throttled/rejected
**0**, held at cap **0**, duplicate skipped **1**. `biotin_dependent_carboxylase` **0 -> 81**
(chemistry-confusable cap 150, floor not reached; deficit **19**). External bronze **5199 -> 5280**;
combined surface **5901 -> 5982**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target/multi-signal rows are held; per-fingerprint cap 150 held.
Row audit found **0** leakage/trust-tier/tier/namespace/reaction problems across 81 biotin rows;
mechanism axes present: cofactor/cosubstrate **81**, domain/family **81**, Rhea participant **81**,
active-site/residue-role **74**. Honest counters after apply are **positive_bronze 4269**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge
them. Fresh post-biotin coverage/redundancy audit reports **5982** combined labels, **27**
fingerprints, seed positives **4286**, fingerprint Gini **0.1655**, expansion holes `[]`,
under-floor `['biotin_dependent_carboxylase']`, over-cap `['metal_dependent_hydrolase']`, and
next-batch floor deficit **19**. Novelty replay reports **5280** expansion rows, decisions
`{'admit': 4824, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0864).

Next decision: run a **non-destructive biotin floor-closure source scout** before any further apply.
The scout must keep ATP + hydrogencarbonate/CO2/carboxybiotin reaction chemistry mandatory and must
not admit EC 6.3.4.15 biotin-protein ligases. If reviewed source supply cannot safely close the
19-row deficit, leave `biotin_dependent_carboxylase` under floor and return to a narrow kinase
subclass scout; do not broad-wire EC 2.7.

References:
`src/catalytic_earth/biotin_dependent_carboxylase_sourcing.py`,
`scripts/source_biotin_dependent_carboxylase_family.py`,
`tests/test_biotin_dependent_carboxylase_sourcing.py`,
`artifacts/v3_biotin_dependent_carboxylase_sourcing_preview_current702.json`,
`work/biotin_dependent_carboxylase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_27fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_biotin_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_biotin_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_biotin_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_biotin_applied.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: ZINC LYASE/HYDRATASE 26FP BRONZE EXPANSION APPLIED

Decision: the latest handoff explicitly recommended guarded `zinc_lyase_hydratase` wiring after
the ThDP apply. Growth went only to `data/registries/external_bronze_labels.json`; frozen current702
stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `zinc_lyase_hydratase` fingerprint spec and `zinc_hydro_lyase`
ontology family; bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to
`label_factory_v1_26fp`; re-froze OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_26fp_1025.json`. EC 4.2.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from Zn cofactor
or metal-site evidence, Rhea hydration/dehydration/carbonic reaction text, Lyase/hydratase family
text, active-/binding-/metal-site evidence, or structure. PLP, ThDP, hydrolase/transferase/
aldolase/isomerase side rows, non-4.2.1 side ECs, and multi-fingerprint rows are held.

**Live apply.** Command:
`PYTHONPATH=src python scripts/source_zinc_lyase_hydratase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **116**, novelty-admitted/applied **113**.
Other holds: **57** off-target fingerprint matches
(`nad_p_dehydrogenase` 47, `metallophosphomonoesterase` 6,
`metallo_amidohydrolase_deaminase` 4), **10** no-corroboration holds, **3** novelty-throttled, held
at cap **0**, duplicate skipped **0**. `zinc_lyase_hydratase` **0 -> 113** (chemistry-confusable cap
150, floor reached). External bronze **5086 -> 5199**; combined surface **5788 -> 5901**. Row audit
found **0** leakage/trust-tier/tier/namespace problems across 113 zinc rows; axes present include
cofactor/cosubstrate, domain/family, active-site/residue-role, and mostly Rhea participant context.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target/multi-signal rows are held; per-fingerprint cap 150 held.
Honest counters after apply are **positive_bronze 4188**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh post-zinc
coverage/redundancy audit reports **5901** combined labels, seed positives **4205**, fingerprint
Gini **0.1559**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch
floor deficit **0**. Novelty replay reports **5199** expansion rows, decisions
`{'admit': 4743, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0877).

Next decision: do **not** broad-wire EC 2.7 kinase; the latest mechanism scout still blocks it due
to multi-subclass mixing. With ThDP and zinc applied, the remaining post-class-II candidates are
weaker: `enolase_superfamily_lyase` is reaction-poor (1 distinct full EC in the 200-row sample),
`biotin_dependent_carboxylase` is below floor under current cofactor/keyword supply, and
Mn/Fe SOD is not floor-reachable. The next useful action is a focused mechanism/source-supply scout
that either splits a narrow kinase subclass with clean non-EC mechanism handles or designs a
guarded biotin-carboxylase handle around biotinyl-Lys/Rhea ATP-hydrogencarbonate evidence.

References:
`artifacts/v3_zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.json`,
`work/zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.md`,
`src/catalytic_earth/zinc_lyase_hydratase_sourcing.py`,
`scripts/source_zinc_lyase_hydratase_family.py`,
`tests/test_zinc_lyase_hydratase_sourcing.py`,
`artifacts/v3_zinc_lyase_hydratase_sourcing_preview_current702.json`,
`work/zinc_lyase_hydratase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_26fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_zinc_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_zinc_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_zinc_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_zinc_applied.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: THIAMINE DIPHOSPHATE 25FP BRONZE EXPANSION APPLIED

Decision: broad EC 2.7 kinase remains blocked by subclass mixing, so this run selected the next
clean fallback from the post-class-II scout: `thiamine_diphosphate_enzyme`. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Mechanism scout.** `artifacts/v3_thiamine_diphosphate_mechanism_handle_scout_current702_20260613.json`
examined **80** reviewed UniProt entries with **0** fetch failures. Non-EC handles were strong:
ThDP context **80/80**, Rhea cross-reference **80/80**, Mg context **77/80**, active/binding-site
context **73/80**, Rhea carbonyl/decarboxylation/transfer text **62/80**, and likely wireable rows
**65/80**. Boundary signals required explicit guards: flavin **11/80**, side EC **15/80**, and
kinase/hydrolase-ish boundary text **48/80**.

**Family/gate surface.** Added `thiamine_diphosphate_enzyme` fingerprint spec and
`thiamine_diphosphate_ylide` ontology family; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_25fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_25fp_1025.json`. EC
2.2.1/4.1.1/1.2.4 is scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration
comes from ThDP/Mg cofactor or binding context, Rhea decarboxylation/carbonyl-transfer/ThDP
participant evidence, ThDP-family keyword/domain text, active-/binding-site evidence, or structure.
PLP, molybdopterin/flavin/heme, kinase/phosphotransferase, hydrolase, non-scope side EC, and
multi-fingerprint rows are held.

**Live apply.** Command:
`PYTHONPATH=src python scripts/source_thiamine_diphosphate_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **181**, novelty-admitted/applied **150**.
Other holds: **14** off-target `coa_acyltransferase` rows, **37** no-corroboration holds, duplicate
skipped **0**. `thiamine_diphosphate_enzyme` **0 -> 150** (chemistry-confusable cap 150, floor
reached). External bronze **4936 -> 5086**; combined surface **5638 -> 5788**. Row audit found
**0** leakage/trust-tier problems across 150 rows; axes present: cofactor/cosubstrate **150**,
domain/family **150**, Rhea participant **150**, active-site/residue-role **144**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, namespace
`uniprot`; EC/name/keyword/Rhea/prose handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target/multi-signal rows are held; per-fingerprint cap 150 held.
Honest counters after apply are **positive_bronze 4075**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh post-ThDP
coverage/redundancy audit reports **5788** combined labels, fingerprint Gini **0.1541**, expansion
holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **0**. Novelty
replay reports **5086** expansion rows, decisions `{'admit': 4630, 'reject': 47, 'throttle': 409}`,
and would-not-readmit **456** (0.0897).

Next decision: `zinc_lyase_hydratase` is the next viable unapplied lane, but it requires guarded
26fp wiring before any preview/apply. Mechanism scout
`artifacts/v3_zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.json` examined
**80** entries with **0** fetch failures and found zinc context **80/80**, lyase/hydratase text
**80/80**, Rhea hydration/elimination/carbonic text **79/80**, active/binding/metal-site context
**76/80**, and likely wireable rows **50/80**. It also found side-EC and boundary rows **30/80**, so
EC 4.2.1 must remain scope-only and the next runner must hold PLP/ThDP, hydrolase/transferase/
aldolase/isomerase side rows, non-4.2.1 side ECs, and multi-fingerprint signals.

References:
`artifacts/v3_thiamine_diphosphate_mechanism_handle_scout_current702_20260613.json`,
`work/thiamine_diphosphate_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_thiamine_diphosphate_sourcing_preview_current702.json`,
`work/thiamine_diphosphate_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_25fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_thdp_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_thdp_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_thdp_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_thdp_applied.md`,
`artifacts/v3_zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.json`,
`work/zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: ATP AMIDE LIGASE 23FP + CLASS-II METAL ALDOLASE 24FP BRONZE EXPANSIONS APPLIED

Decision: the latest handoff state superseded the older P450 prompt direction because P450,
non-heme 2OG, CoA, cofactor-independent isomerase, molybdopterin oxidoreductase, copper
oxidoreductase, and non-PLP racemase/epimerase were already applied. The run first applied the
recommended `atp_amide_ligase` lane, then used current evidence to select and apply
`class_ii_metal_aldolase` as the next clean 10k-path lane. Growth went only to
`data/registries/external_bronze_labels.json`; the frozen current702 registry stayed byte-unchanged
with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after
both applies.

**ATP amide ligase family/gate surface.** Added `atp_amide_ligase` fingerprint spec and attached the
lane to the existing `atp_grasp` ontology context; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_23fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_23fp_1025.json`. EC 6.3 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from
ATP/ADP/phosphate/Mg context, Ligase/ATP-grasp keyword/domain, Rhea amide/C-N/acyl-phosphate
chemistry, active-/binding-site evidence, or structure. Biotin/carboxylase, kinase/
phosphotransferase, hydrolase/transferase side-EC, and multi-fingerprint rows are held.

**ATP live apply.** Command:
`PYTHONPATH=src python scripts/source_atp_amide_ligase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **171**, gate-admitted/applied **150**. Other
holds: **8** off-target rows, duplicate skipped **0**. `atp_amide_ligase` **0 -> 150** (cap 150,
floor reached). External bronze **4636 -> 4786**; combined surface **5338 -> 5488**. Row audit found
**0** leakage/trust-tier problems across 150 rows; axes present: cofactor/cosubstrate **150**,
domain/family **150**, Rhea participant **150**, active-site/residue-role **124**.

**Post-ATP lane decision.** Source-supply scout
`artifacts/v3_next_lane_source_supply_scout_after_atp_ligase_current702_20260613.json` selected
`class_ii_metal_aldolase` as the next clean lane. Mechanism scout
`artifacts/v3_class_ii_metal_aldolase_mechanism_handle_scout_current702_20260613.json` examined
**80** entries with **0** fetch failures and found active/binding/metal site **80/80**, metal
**80/80**, Lyase **80/80**, Rhea **80/80**, aldolase/oxoacid **61/80**, and C-C reaction text
**58/80**, with side-EC **20/80**, PLP **2/80**, ThDP **5/80**, Schiff/class-I **4/80**, hydrolase
**8/80**, and transferase **9/80** recorded as boundary signals. This authorized a guarded 24fp
class-II metal aldolase lane, not broad EC 4.1 admission.

**Class-II metal aldolase family/gate surface.** Added `class_ii_metal_aldolase` fingerprint spec and
`carbon_carbon_lyase` ontology family; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_24fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_24fp_1025.json`. EC 4.1.2/4.1.3
is scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from metal,
Lyase keyword/domain, aldolase/C-C/Rhea chemistry, active-/binding-/metal-site evidence, or
structure. PLP, ThDP, Schiff/class-I, hydrolase, transferase, oxidoreductase, side-EC, and
multi-fingerprint rows are held.

**Class-II live apply.** Command:
`PYTHONPATH=src python scripts/source_class_ii_metal_aldolase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`.
Result: fetched **240**, target mechanism-corroborated **182**, gate-admitted/applied **150**. Other
holds: **7** off-target rows, duplicate skipped **0**. `class_ii_metal_aldolase` **0 -> 150** (cap
150, floor reached). External bronze **4786 -> 4936**; combined surface **5488 -> 5638**. Row audit
found **0** leakage/trust-tier problems across 150 rows; axes present: cofactor/cosubstrate **150**,
domain/family **150**, Rhea participant **150**, active-site/residue-role **149**.

Guardrails held for both applies: every added row is `tier=bronze`, `review_status=automation_curated`,
entry namespace `uniprot`; EC/name/keyword/Rhea/prose handles are admission/excluded-context evidence
only; `predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target/multi-signal rows are held; per-fingerprint cap 150 held.
Honest counters after both applies are **positive_bronze 3925**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh
post-class-II coverage/redundancy audit reports **5638** combined labels, fingerprint Gini
**0.1581**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **0**. Novelty replay reports **4936** expansion rows, decisions
`{'admit': 4480, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0924).

Next decision: do **not** broad-wire `atp_phosphotransferase_kinase` from EC 2.7. The follow-on
source-supply scout ranked it first, but mechanism scout
`artifacts/v3_atp_phosphotransferase_kinase_mechanism_handle_scout_current702_20260613.json`
examined 80 entries with 0 failures and found broad ATP/Rhea/kinase handles alongside **75/80**
multi-subclass boundary rows and only **4** likely wireable rows. Split a narrow kinase subclass with
clean non-EC handles, or choose the next cleaner lane from the scout ranking; **ThDP enzyme** is the
best fallback candidate.

References:
`artifacts/v3_atp_amide_ligase_mechanism_handle_scout_current702_20260613.json`,
`work/atp_amide_ligase_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_atp_amide_ligase_sourcing_preview_current702.json`,
`work/atp_amide_ligase_sourcing_current702.md`,
`artifacts/v3_next_lane_source_supply_scout_after_atp_ligase_current702_20260613.json`,
`work/next_lane_source_supply_scout_after_atp_ligase_current702_20260613.md`,
`artifacts/v3_class_ii_metal_aldolase_mechanism_handle_scout_current702_20260613.json`,
`work/class_ii_metal_aldolase_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_class_ii_metal_aldolase_sourcing_preview_current702.json`,
`work/class_ii_metal_aldolase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_23fp_1025.json`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_24fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_class_ii_aldolase_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_class_ii_aldolase_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_class_ii_aldolase_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_class_ii_aldolase_applied.md`,
`artifacts/v3_atp_phosphotransferase_kinase_mechanism_handle_scout_current702_20260613.json`,
`work/atp_phosphotransferase_kinase_mechanism_handle_scout_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: COPPER OXIDOREDUCTASE 21FP + NON-PLP RACEMASE/EPIMERASE 22FP BRONZE EXPANSIONS APPLIED

Decision: the latest handoff state superseded the older P450 prompt direction because P450,
non-heme 2OG, CoA, cofactor-independent isomerase, and molybdopterin oxidoreductase were already
applied. The run first applied the recommended `copper_oxidoreductase` lane, then used current
evidence to select and apply `metal_racemase_epimerase_non_plp` as the next clean 10k-path lane.
Growth went only to `data/registries/external_bronze_labels.json`; the frozen current702 registry
stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after both applies.

**Copper family/gate surface.** Added `copper_oxidoreductase` fingerprint spec and `copper_redox`
ontology node; bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to
`label_factory_v1_21fp`; re-froze OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_21fp_1025.json`. EC 1.10.3/1.4.3
is scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from copper
cofactor/site evidence, Rhea oxygen/redox equation text, Copper keyword/domain, active-/binding-/
metal-site evidence, or structure. Heme/flavin/molybdopterin, hydrolase, non-oxidoreductase side-EC,
and multi-fingerprint rows are held.

**Copper live apply.** Command:
`PYTHONPATH=src python scripts/source_copper_oxidoreductase_family.py --max-records-per-lane 80 --apply`.
Result: fetched **149**, target mechanism-corroborated **140**, gate-admitted/applied **119**.
Other holds: **21** novelty-throttled/rejected, **7** disambiguation holds
(`no_mechanism_corroboration`), **2** skipped, **0** off-target fingerprint matches, **0** held at
cap, duplicate skipped **0**. `copper_oxidoreductase` **0 -> 119** (cap 250, floor reached).
External bronze **4409 -> 4528**; combined surface **5111 -> 5230**.

**Post-copper lane decision.** Source-supply scout
`artifacts/v3_next_lane_source_supply_scout_after_copper_current702_20260613.json` selected
`metal_racemase_epimerase_non_plp` over the remaining clean lanes because it had reviewed supply
**2141**, EC-only ceiling **2319**, handle capture **0.923**, distinct full EC sample **52**, no
reaction-poor warning, and a reachable floor under the chemistry-confusable cap **150**. Mechanism
scout `artifacts/v3_metal_racemase_epimerase_mechanism_handle_scout_current702_20260613.json`
examined **80** entries with **0** fetch failures and found Isomerase keyword **80/80**, Rhea
cross-reference **80/80**, isomerization text **80/80**, racemase/epimerase text **78/80**,
binding-site **70/80**, active-site **59/80**, metal **26/80**, cofactorless **42/80**, and PLP
boundary **2/80**. This authorized wiring a guarded 22fp lane, not broad EC 5.1 admission.

**Racemase/epimerase family/gate surface.** Added `metal_racemase_epimerase_non_plp` fingerprint spec
and `stereochemical_isomerization` ontology node; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_22fp`; re-froze OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_22fp_1025.json`. EC 5.1 is
scope-only (`ec_scope_hint`, never counted). Counted mechanism corroboration comes from
racemase/epimerase/mutarotase text, Rhea isomerization/racemization equation text, Isomerase
keyword/domain, active-/binding-site evidence, metal context, or structure. Cofactorless context is
boundary/admission context, not a predictive feature. PLP/pyridoxal-phosphate rows, non-5.1 side-EC,
transferase, hydrolase, oxidoreductase, and multi-fingerprint rows are held.

**Racemase/epimerase live apply.** Command:
`PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 320 --cap-ceiling 150 --apply`.
Result: fetched **320**, target mechanism-corroborated **108**, gate-admitted/applied **108**.
Other holds: **133** off-target fingerprint matches held (`nad_p_dehydrogenase`), **48**
disambiguation holds (`no_mechanism_corroboration`), **31** skipped, **0** novelty-throttled/rejected,
**0** held at cap, duplicate skipped **0**. `metal_racemase_epimerase_non_plp` **0 -> 108** (cap
150, floor reached). External bronze **4528 -> 4636**; combined surface **5230 -> 5338**.

Guardrails held for both applies: every added row is `tier=bronze`, `review_status=automation_curated`,
entry namespace `uniprot`; EC/name/keyword/Rhea/prose handles are admission/excluded-context evidence
only; `predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target/multi-signal rows are held; per-fingerprint caps held.
Spot-check over all 108 racemase preview/applied rows found **0** leakage/trust-tier problems; axes
present: Rhea participant **108**, domain/family **108**, active-site/residue-role **96**,
cofactor/cosubstrate **69**. Honest counters after both applies are **positive_bronze 3625**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge
them. Fresh post-racemase coverage/redundancy audit reports **5338** combined labels, fingerprint
Gini **0.1665**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **0**. Novelty replay reports **4636** expansion rows, decisions
`{'admit': 4180, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.0984).

Next decision: after removing already-applied `metal_racemase_epimerase_non_plp`, the next clean
source-supply candidate is **`atp_amide_ligase`** (EC 6.3, reviewed supply 13599, distinct full EC
sample 51, confusable cap 150). Do a mechanism-handle scout before any 23fp wiring. EC must remain
scope-only; counted corroborators should come from ATP/Mg or acyl-phosphate/amide-ligase Rhea
participants, Ligase/ATP-grasp keyword/domain, active-/binding-site evidence, or structure. Guard
kinases, biotin carboxylases, generic ATP transferases, hydrolase side rows, and multi-fingerprint
signals.

References:
`artifacts/v3_copper_oxidoreductase_sourcing_preview_current702.json`,
`work/copper_oxidoreductase_sourcing_current702.md`,
`artifacts/v3_next_lane_source_supply_scout_after_copper_current702_20260613.json`,
`work/next_lane_source_supply_scout_after_copper_current702_20260613.md`,
`artifacts/v3_metal_racemase_epimerase_mechanism_handle_scout_current702_20260613.json`,
`work/metal_racemase_epimerase_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_metal_racemase_epimerase_non_plp_sourcing_preview_current702.json`,
`work/metal_racemase_epimerase_non_plp_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_21fp_1025.json`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_22fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_racemase_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_racemase_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_racemase_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_racemase_applied.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: MOLYBDOPTERIN OXIDOREDUCTASE 20FP BRONZE EXPANSION APPLIED

Decision: after the cofactor-independent isomerase 19fp lane was applied, the current
source-supply scout recommended molybdopterin oxidoreductase over copper. A focused
mechanism-handle scout confirmed enough non-EC mechanism evidence, so the lane was wired and applied
as a deliberate **20-fingerprint universe change**. Growth went only to the separate external bronze
registry. The frozen current702 registry stayed byte-unchanged: sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `molybdopterin_oxidoreductase` fingerprint spec and
`molybdopterin_redox` ontology node; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_20fp`; re-froze the OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_20fp_1025.json` (supersedes 19fp;
older preregistration files remain historical). The admission rule uses EC 1.* oxidoreductase as
scope-only (`ec_scope_hint`, never counted), with molybdopterin/Mo-cofactor, Rhea redox/oxo-transfer,
Molybdenum keyword/domain, Mo-pterin feature/ligand, and active-/binding-/metal-site evidence as
mechanism corroboration. Hydrolase, non-oxidoreductase side-EC, peroxide/peroxidase, biosynthesis,
and off-target multi-fingerprint rows are held.

**Mechanism scout.** `artifacts/v3_molybdopterin_oxidoreductase_mechanism_handle_scout_current702_20260613.json`
examined **80** reviewed UniProt entries with **0** fetch failures. Handles in sample:
Mo-cofactor **80/80**, Molybdenum keyword **80/80**, Rhea cross-reference **78/80**, catalytic
activity **78/80**, Mo feature/ligand context **65/80**, redox reaction text **49/80**, oxo-transfer
reaction text **71/80**. Boundary signals were present (flavin 33/80, heme 13/80, peroxide/peroxidase
26/80), so the apply path required explicit boundary and multi-signal holds rather than broad EC
admission.

**Live preview/apply.** Command:
`PYTHONPATH=src python scripts/source_molybdopterin_oxidoreductase_family.py --max-records-per-lane 80 --apply`.
Result: fetched **255** reviewed Swiss-Prot rows -> target mechanism-corroborated **210** ->
gate-admitted before cap **207** -> appended **207** rows. Per-family result:
`molybdopterin_oxidoreductase` **0 -> 207** (cap 250, floor reached, **0 held at cap**). Other
holds: **3** novelty-throttled, **41** disambiguation holds (`no_mechanism_corroboration`), **0**
off-target fingerprint matches held, **4** skipped, duplicate skipped at registry apply **0**.
External bronze **4202 -> 4409**; combined surface **4904 -> 5111**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, entry
namespace `uniprot`; molybdopterin handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target/multi-signal rows are held; per-fingerprint cap held.
Spot-check over all 207 added rows found **0** leakage/trust-tier problems; axes present:
cofactor/cosubstrate **207**, active-site/residue-role **206**, domain/family **206**, Rhea
participant **206**. Honest counters after apply are **positive_bronze 3398**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh
coverage/redundancy audit after the apply reports **5111** combined labels, fingerprint Gini
**0.1613**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **0**. Novelty replay reports **4409** expansion rows, decisions
`{'admit': 3953, 'reject': 47, 'throttle': 409}`, and would-not-readmit **456** (0.1034).

Next decision: the next 10k-path lane is **copper oxidoreductase** if the completed scout can be
turned into a clean guarded design. Follow-on scout
`artifacts/v3_copper_oxidoreductase_mechanism_handle_scout_current702_20260613.json` examined 80
entries with 0 fetch failures and found Rhea 78/80, redox text 77/80, copper feature/ligand context
31/80, and explicit copper cofactor comments 20/80, plus heme/side-EC/glycosyltransferase boundary
signals. Use EC as scope only; counted corroborators should be copper cofactor/keyword/domain, Rhea
redox participants, active-/binding-/metal-site evidence, or structure. Add guards versus heme,
flavin, molybdopterin, hydrolase, and glycosyltransferase side rows; re-freeze OOS preregistration to
21fp before any registry apply.

References:
`artifacts/v3_molybdopterin_oxidoreductase_mechanism_handle_scout_current702_20260613.json`,
`work/molybdopterin_oxidoreductase_mechanism_handle_scout_current702_20260613.md`,
`artifacts/v3_molybdopterin_oxidoreductase_sourcing_preview_current702.json`,
`work/molybdopterin_oxidoreductase_sourcing_current702.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_20fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_molybdopterin_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_molybdopterin_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_molybdopterin_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_molybdopterin_applied.md`,
`artifacts/v3_copper_oxidoreductase_mechanism_handle_scout_current702_20260613.json`,
`work/copper_oxidoreductase_mechanism_handle_scout_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: COFACTOR-INDEPENDENT ISOMERASE 19FP BRONZE EXPANSION APPLIED

Decision: after the CoA acyltransferase 18fp lane was applied, the current scout-recommended next
lane was wired and applied as a deliberate **19-fingerprint universe change**. Growth went only to
the separate external bronze registry. The frozen current702 registry stayed byte-unchanged: sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `cofactor_independent_isomerase` fingerprint spec and `isomerization`
ontology node; bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to
`label_factory_v1_19fp`; re-froze the OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_19fp_1025.json` (supersedes 18fp;
older preregistration files remain historical). The admission rule uses EC 5.3 as scope-only
(`ec_scope_hint`, never counted), with Rhea isomerization equation text, Isomerase keyword/domain,
and active-/binding-site/base evidence as mechanism corroboration. Non-5.3 side-EC rows and
off-target fingerprint matches are held.

**Live preview/apply.** Command:
`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 80 --apply`.
Result: fetched **266** reviewed Swiss-Prot rows -> target mechanism-corroborated **147** ->
gate-admitted before cap **142** -> appended **142** rows. Per-family result:
`cofactor_independent_isomerase` **0 -> 142** (cap 150 because chemistry-confusable, floor reached,
**0 held at cap**). Other holds: **5** novelty-throttled, **70** disambiguation holds
(`no_mechanism_corroboration`), **28** off-target fingerprint matches held (`nad_p_dehydrogenase`),
**21** skipped, fetch failures **0**, duplicate skipped at registry apply **0**. External bronze
**4060 -> 4202**; combined surface **4762 -> 4904**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, entry
namespace `uniprot`; isomerase handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target rows were held; per-fingerprint cap held. Honest counters
after apply are **positive_bronze 3191**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**; do not merge them. Fresh coverage/redundancy audit after
the apply reports **4904** combined labels, fingerprint Gini **0.1613**, expansion holes `[]`,
over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **0**. Novelty replay reports
**4202** expansion rows, decisions `{'admit': 3746, 'reject': 47, 'throttle': 409}`, and
would-not-readmit **456** (0.1085).

Productive follow-on: a non-destructive source-supply scout compared the remaining oxidoreductase
lanes and recommends **molybdopterin oxidoreductase** next: **460** reviewed Swiss-Prot rows and
**33** distinct full EC labels in a 200-row sample, ahead of `copper_oxidoreductase` (**222** /
**12**). Both are reaction-poor.

Next decision: the next high-value scaling lane is **molybdopterin oxidoreductase**, but it must
start with a mechanism-handle scout and subclass/boundary guard design. Treat it as a possible
20-fingerprint universe change only if non-EC mechanism corroborators are strong: molybdopterin or
Mo-cofactor handles, Mo-pterin domain/keyword, Rhea redox/oxo-transfer participants,
active-/binding-site metal/ligand evidence, or structure. EC remains scope-only; add heme/flavin/
copper/metal-hydrolase and EC-subclass guards; re-freeze the OOS preregistration to 20fp before any
registry apply.

References:
`artifacts/v3_cofactor_independent_isomerase_sourcing_preview_current702.json`,
`work/cofactor_independent_isomerase_sourcing_current702.md`,
`work/cofactor_independent_isomerase_apply_current702_20260613.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_19fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_isomerase_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_isomerase_applied.md`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260613_isomerase_applied.json`,
`work/novelty_admission_gate_audit_current702_20260613_isomerase_applied.md`,
`artifacts/v3_next_lane_source_supply_scout_after_isomerase_current702_20260613.json`,
`work/next_lane_source_supply_scout_after_isomerase_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: CoA ACYLTRANSFERASE 18FP BRONZE EXPANSION APPLIED

Decision: after the non-heme iron 2OG 17fp lane was applied, the documented next lane was wired and
applied as a deliberate **18-fingerprint universe change**. Growth went only to the separate external
bronze registry. The frozen current702 registry stayed byte-unchanged: sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `coa_acyltransferase` fingerprint spec and `acyl_transfer` ontology
node; bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_18fp`;
re-froze the OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_18fp_1025.json` (supersedes 17fp;
older preregistration files remain historical). The admission rule uses EC 2.3.1 as scope-only
(`ec_scope_hint`, never counted), with CoA/acyl-CoA Rhea participant, CoA/acyl-CoA feature text,
Acyltransferase keyword/domain, and active-/binding-site evidence as mechanism corroboration.
Hydrolase side-EC rows and off-target fingerprint matches are held.

**Live preview/apply.** Command:
`PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 80 --apply`.
Result: fetched **218** reviewed Swiss-Prot rows -> target mechanism-corroborated **204** ->
gate-admitted before cap **188** -> appended **188** rows. Per-family result:
`coa_acyltransferase` **0 -> 188** (cap 250, floor reached, **0 held at cap**). Other holds:
**16** novelty-throttled, **11** disambiguation holds (`no_mechanism_corroboration`), **1**
off-target fingerprint match held (`metallo_amidohydrolase_deaminase`), **2** skipped, fetch failures
**0**, duplicate skipped at registry apply **0**. External bronze **3872 -> 4060**; combined surface
**4574 -> 4762**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, entry
namespace `uniprot`; CoA/acyltransferase handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; off-target rows were held; per-fingerprint cap held. Honest counters
after apply are **positive_bronze 3049**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**; do not merge them. Fresh coverage/redundancy audit after
the apply reports **4762** combined labels, fingerprint Gini **0.1652**, expansion holes `[]`,
over-cap `['metal_dependent_hydrolase']`, and next-batch floor deficit **0**.

Productive follow-on: a non-destructive source-supply scout compared the next named lanes after CoA
and recommends **cofactor-independent isomerase** next: **5273** reviewed Swiss-Prot rows and **51**
distinct full EC labels in a 200-row sample with no reaction-poor warning, ahead of
`molybdopterin_oxidoreductase` (460/33, reaction-poor) and `copper_oxidoreductase` (222/12,
reaction-poor). A mechanism-handle scout over 80 reviewed entries found catalytic activity context
**80/80**, Rhea cross-reference **62/80**, active-or-binding-site context **65/80**, isomerization
reaction text **62/80**, and fetch failures **0**. It also surfaced multi-EC boundary rows
(`2.5.1.18`, `1.11.1.-` in the top sample).

Next decision: the next high-value scaling lane is **cofactor-independent isomerase**. Treat it as a
deliberate **19-fingerprint universe change**: add fingerprint spec + ontology node; use EC 5.3 as
scope only; count Rhea isomerization equation/participant or Isomerase keyword/domain with active-/
binding-site/base evidence as mechanism corroboration; add mutase/racemase/epimerase/isomerase
subclass guards and off-target EC 2.5/1.11 boundary holds; add offline leakage/trust-tier tests;
re-freeze the OOS pre-registration to 19fp; preview before any apply.

References:
`artifacts/v3_coa_acyltransferase_sourcing_preview_current702.json`,
`work/coa_acyltransferase_sourcing_current702.md`,
`work/coa_acyltransferase_apply_current702_20260613.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_18fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260613_coa_applied.json`,
`work/coverage_redundancy_audit_current702_20260613_coa_applied.md`,
`artifacts/v3_next_lane_source_supply_scout_after_coa_current702_20260613.json`,
`work/next_lane_source_supply_scout_after_coa_current702_20260613.md`,
`artifacts/v3_cofactor_independent_isomerase_mechanism_handle_scout_current702_20260613.json`,
`work/cofactor_independent_isomerase_mechanism_handle_scout_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: NON-HEME IRON 2OG 17FP BRONZE EXPANSION APPLIED

Decision: after the P450 16fp lane was applied in the same automation block, the documented next
lane was wired and applied as a deliberate **17-fingerprint universe change**. Growth went only to
the separate external bronze registry. The frozen current702 registry stayed byte-unchanged: sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `non_heme_iron_2og_dioxygenase` fingerprint spec and
`non_heme_iron_oxygenation` ontology node; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_17fp`; re-froze the OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_17fp_1025.json` (supersedes 16fp;
older preregistration files remain historical). The admission rule uses EC 1.14.11 as scope-only
(`ec_scope_hint`, never counted), with Fe(II), 2-oxoglutarate/succinate/CO2 Rhea participant,
Dioxygenase keyword/domain, and active/binding-site evidence as mechanism corroboration. Heme,
flavin, and peroxide rows are guarded out; the runner holds off-target fingerprint matches.

**Live preview/apply.** Command:
`PYTHONPATH=src python scripts/source_non_heme_iron_2og_family.py --max-records-per-lane 80 --apply`.
Result: fetched **212** reviewed Swiss-Prot rows -> target mechanism-corroborated **198** ->
gate-admitted before cap **172** -> appended **172** rows. Per-family result:
`non_heme_iron_2og_dioxygenase` **0 -> 172** (cap 250, floor reached, **0 held at cap**). Other
holds: **26** novelty-throttled, **12** disambiguation holds
(`multi_fingerprint_signal_conflict` 5, `no_mechanism_corroboration` 7), **2** skipped, fetch
failures **0**, duplicate skipped at registry apply **0**. External bronze **3700 -> 3872**;
combined surface **4402 -> 4574**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, entry
namespace `uniprot`; Fe(II)/2OG/dioxygenase handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; multi-fingerprint-signal rows were held; per-fingerprint cap held.
Honest counters after apply are **positive_bronze 2861**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh
coverage/redundancy audit after the apply reports **4574** combined labels, fingerprint Gini
**0.1657**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **0**.

Productive follow-on: a focused non-destructive source-supply scout compared remaining named lanes
and recommends **CoA acyltransferase** next: `coa_acyltransferase` has **7728** reviewed Swiss-Prot
rows and **82** distinct full EC labels in a 200-row sample with no reaction-poor warning, ahead of
cofactor-independent isomerase, molybdopterin oxidoreductase, and copper oxidoreductase. A CoA
lane-design scout then confirmed the key handle shape: Acyltransferase keyword supply **7728**,
UniProt `cc_cofactor:coa` supply only **23**, EC-only ceiling **9981**, and **108** distinct EC labels
in a 500-row sample. A mechanism-handle scout over 80 reviewed entries found Rhea cross-references
**80/80**, CoA/acyl-CoA reaction text **72/80**, active/binding-site context **56/80**, CoA/acyl-CoA
feature text **24/80**, and fetch failures **0**. The next runner should not rely on the
cofactor-comment handle alone and should hold multi-EC/multi-fingerprint boundary rows.

Validation so far: targeted pytest over P450/2OG/NAD/SAM sourcing, disambiguation/import,
trust-tier, leakage-preregistration, coverage, novelty, and fingerprints passed (**275 passed,
14 subtests**).

Next decision: the next high-value scaling lane is **CoA acyltransferase**. Treat it as a deliberate
**18-fingerprint universe change**: add fingerprint spec + ontology node; add EC 2.3.1 scope-only
lanes plus CoA/acyl-CoA Rhea participant or Acyltransferase keyword/domain and catalytic
His/Cys/active-site mechanism corroborators; add non-CoA transferase and multi-fingerprint-signal
guards; add offline leakage/trust-tier tests; re-freeze the OOS pre-registration to 18fp; then run a
non-destructive preview before any apply.

References:
`artifacts/v3_non_heme_iron_2og_sourcing_preview_current702.json`,
`work/non_heme_iron_2og_sourcing_current702.md`,
`work/non_heme_iron_2og_apply_current702_20260612.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_17fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260612_2og_applied.json`,
`work/coverage_redundancy_audit_current702_20260612_2og_applied.md`,
`artifacts/v3_next_lane_source_supply_scout_after_p450_2og_current702_20260613.json`,
`work/next_lane_source_supply_scout_after_p450_2og_current702_20260613.md`,
`artifacts/v3_coa_acyltransferase_lane_design_scout_current702_20260613.json`,
`work/coa_acyltransferase_lane_design_scout_current702_20260613.md`,
`artifacts/v3_coa_acyltransferase_mechanism_handle_scout_current702_20260613.json`,
`work/coa_acyltransferase_mechanism_handle_scout_current702_20260613.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-13: CYTOCHROME P450 16FP BRONZE EXPANSION APPLIED

Decision: the documented post-SAM scaling lane was wired and applied as a deliberate
**16-fingerprint universe change**. Growth went only to the separate external bronze registry. The
frozen current702 registry stayed byte-unchanged: sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `cytochrome_p450_monooxygenase` fingerprint spec and
`heme_monooxygenation` ontology node; bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_16fp`; re-froze the OOS
next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_16fp_1025.json` (supersedes the
15fp preregistration; 15fp/14fp/12fp/8fp remain historical). The admission rule uses EC 1.14 as
scope-only (`ec_scope_hint`, never counted), with heme plus O2/Rhea participant,
P450/monooxygenase keyword/domain, active/binding-site, or heme-thiolate evidence as mechanism
corroboration. A non-peroxidase/peroxide guard blocks heme peroxidase chemistry from
`cytochrome_p450_monooxygenase`; the runner also holds off-target fingerprint matches.

**Live preview/apply.** Command:
`PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 80 --apply`.
Result: fetched **142** reviewed Swiss-Prot rows -> target mechanism-corroborated **128** ->
gate-admitted before cap **110** -> appended **110** rows. Per-family result:
`cytochrome_p450_monooxygenase` **0 -> 110** (cap 250, floor reached, **0 held at cap**). Other
holds: **18** throttled/rejected by novelty, **14** disambiguation holds
(`no_mechanism_corroboration`), fetch failures **0**, duplicate skipped at registry apply **0**.
External bronze **3590 -> 3700**; combined surface **4292 -> 4402**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, entry
namespace `uniprot`; P450/O2/heme handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; EC is never a counted corroborator; dedup ran against both frozen
current702 and external bronze; multi-fingerprint-signal rows were held; per-fingerprint cap held.
Honest counters after apply are **positive_bronze 2689**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them. Fresh
coverage/redundancy audit after the apply reports **4402** combined labels, fingerprint Gini
**0.1657**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch floor
deficit **0**.

Productive follow-on: a focused non-destructive source-supply scout for
`non_heme_iron_2og_dioxygenase` confirmed the next lane is viable: EC 1.14.11 + iron/dioxygenase
handle has **870** reviewed Swiss-Prot rows, the iron-only handle has **854**, and a 200-row sample
has **36** distinct specific ECs. No labels or registry writes were made by the scout.

Validation: targeted pytest over P450/NAD/SAM sourcing, disambiguation/import, trust-tier,
leakage-preregistration, coverage, novelty, and fingerprints passed (**264 passed, 14 subtests**);
`PYTHONPATH=src python -m catalytic_earth.cli validate` passed (12 source records, 16 mechanism
fingerprints, 19 ontology families, 702 curated labels).

Next decision: the immediate low-risk P450 floor is closed; the next high-value scaling lane is
**non-heme iron 2OG dioxygenase**. Treat it as a deliberate **17-fingerprint universe change**:
add fingerprint spec + ontology node; add Fe(II)/2OG/succinate/CO2 Rhea participant or Dioxygenase
keyword/binding-site/active-site mechanism corroborator with heme/flavin/peroxide guards; add offline
leakage/trust-tier tests; re-freeze the OOS pre-registration to 17fp; then run a non-destructive
preview before any apply.

References:
`artifacts/v3_cytochrome_p450_sourcing_preview_current702.json`,
`work/cytochrome_p450_sourcing_current702.md`,
`work/cytochrome_p450_apply_current702_20260612.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_16fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260612_p450_applied.json`,
`work/coverage_redundancy_audit_current702_20260612_p450_applied.md`,
`artifacts/v3_non_heme_iron_2og_next_lane_scout_current702_20260612.json`,
`work/non_heme_iron_2og_next_lane_scout_current702_20260612.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-12: SAM METHYLTRANSFERASE 15FP BRONZE EXPANSION APPLIED

Decision: after the NAD(P)-dehydrogenase + glycosyltransferase floor/cap expansion was already
complete, the next documented scaling lane was wired and applied as a deliberate **15-fingerprint
universe change**. Growth still went only to the separate external bronze registry. The frozen
current702 registry stayed byte-unchanged: sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after apply.

**Family/gate surface.** Added `sam_methyltransferase` fingerprint spec and `methyl_transfer`
ontology node; bumped `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to
`label_factory_v1_15fp`; re-froze the OOS next-tranche preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_15fp_1025.json` (supersedes the
14fp preregistration; 14fp/12fp/8fp remain historical). The admission rule uses EC 2.1.1 as
scope-only (`ec_scope_hint`, never counted), with SAM/SAH Rhea participant/cofactor/cosubstrate or
Methyltransferase keyword/domain as mechanism corroboration. A no-Fe-S/radical-SAM guard blocks
radical-SAM methylases from `sam_methyltransferase`; the runner also holds off-target fingerprint
matches instead of importing them from this family lane.

**Live preview/apply.** Command:
`PYTHONPATH=src python scripts/source_sam_methyltransferase_family.py --max-records-per-lane 120 --apply`.
Result: fetched **315** reviewed Swiss-Prot rows -> target mechanism-corroborated **304** ->
gate-admitted before cap **264** -> appended **250** rows. Per-family result:
`sam_methyltransferase` **0 -> 250** (cap 250, floor reached, **14 held at cap**). Other holds:
**2** multi-fingerprint-signal rows held, **28** throttled as redundant, **12** rejected over-cap/no
new chemistry, **9** skipped, fetch failures **0**. External bronze **3340 -> 3590**; combined
surface **4042 -> 4292**; duplicate skipped at registry apply **0**.

Guardrails held: every added row is `tier=bronze`, `review_status=automation_curated`, entry
namespace `uniprot`; broadened SAM/SAH/keyword handles are admission/excluded-context evidence only;
`predictive_evidence` is `[]`; dedup ran against both frozen current702 and external bronze;
multi-fingerprint-signal rows were held; per-fingerprint cap held. Honest counters after apply are
**positive_bronze 2579**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**; do not merge them. Fresh coverage/redundancy audit after the apply reports
**4292** combined labels, fingerprint Gini **0.1657**, expansion holes `[]`, over-cap
`['metal_dependent_hydrolase']`, and next-batch floor deficit **0**.

Validation: targeted pytest over SAM/NAD sourcing, disambiguation/import, trust-tier,
leakage-preregistration, coverage, novelty, fingerprints, and CLI readiness passed (**82 passed**);
`PYTHONPATH=src python -m catalytic_earth.cli validate` passed (12 source records, 15 mechanism
fingerprints, 18 ontology families, 702 curated labels); `git diff --check` and JSON parse checks
clean.

Next decision: the immediate low-risk within-15fp cap fill is exhausted; the next high-value scaling
lane is **cytochrome P450 monooxygenase**. Treat it as a deliberate **16-fingerprint universe
change**: add fingerprint spec + ontology node; add heme/thiolate + oxygenase Rhea participant or
P450 keyword/domain mechanism corroborator with a non-peroxidase guard; add offline
leakage/trust-tier tests; re-freeze the OOS pre-registration to 16fp; then run a non-destructive
preview before any apply.

References:
`artifacts/v3_sam_methyltransferase_sourcing_preview_current702.json`,
`work/sam_methyltransferase_sourcing_current702.md`,
`work/sam_methyltransferase_apply_current702_20260612.md`,
`artifacts/v3_external_hard_negative_next_tranche_preregistration_15fp_1025.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260612_sam_methyl_applied.json`,
`work/coverage_redundancy_audit_current702_20260612_sam_methyl_applied.md`,
`artifacts/v3_source_trust_tier_policy_current702.json`,
`data/registries/external_bronze_labels.json`.

## 2026-06-12: NAD(P)-DEHYDROGENASE + GLYCOSYLTRANSFERASE BRONZE EXPANSION APPLIED

Decision: the prior broadened-handle NAD(P)/glyco preview was authorized by this automation prompt
and applied to the **separate external bronze registry only**. The frozen current702 registry stayed
byte-unchanged: sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before
and after both applies. The apply path was the canonical
`catalytic_earth.cli apply-external-annotation-anchored-import`, wrapped with explicit frozen-sha
checks.

**Applied batch 1 (floor run).** Reran `scripts/source_nad_glycosyltransferase_families.py` with
`--max-records-per-lane 100` over both families. Live UniProt result: fetched **794** rows ->
mechanism-corroborated **709** -> gate-admitted before cap **486** -> applied **373** rows.
Per-family result: **nad_p_dehydrogenase 0 -> 150** (chemistry-confusable cap 150, floor reached,
**113 held at cap**) and **glycosyltransferase 0 -> 223** (cap 250, floor reached). No fetch
failures. External bronze **2940 -> 3313**; combined **3642 -> 4015**; duplicate skipped 0.

**Applied batch 2 (glycosyltransferase cap fill).** After batch 1, reran glycosyltransferase only at
`--max-records-per-lane 150` to use the remaining cap space without opening a new universe version.
Result: fetched **445** -> mechanism-corroborated **157** -> gate-admitted before cap **37** ->
applied **27** rows; glycosyltransferase **223 -> 250** and **10 held at cap**. No fetch failures.
External bronze **3313 -> 3340**; combined **4015 -> 4042**; duplicate skipped 0.

Guardrails held on both previews/applies: EC remained scope-only (`ec_scope_hint`, never counted);
every added row is `tier=bronze`, `review_status=automation_curated`, `entry_id` namespace
`uniprot`; broadened keyword/cosubstrate/Rhea/active-site handles are admission/excluded-context
evidence only; `predictive_evidence` is `[]`; dedup ran against both frozen current702 and external
bronze; multi-fingerprint-signal rows were not forced; per-fingerprint caps held (NAD(P) 150, glyco
250). Honest counters after apply are **positive_bronze 2329**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**; do not merge them.
Fresh coverage/redundancy audit after the applies reports **4042** combined labels, fingerprint
Gini **0.1578**, expansion holes `[]`, over-cap `['metal_dependent_hydrolase']`, and next-batch
floor deficit **0**.

Validation: targeted pytest
`tests/test_nad_glycosyltransferase_subfamily_sourcing.py tests/test_source_trust_tiers.py
tests/test_leakage_closure.py tests/test_external_annotation_anchored_import.py
tests/test_coverage_redundancy_audit.py tests/test_novelty_admission_gate.py tests/test_fingerprints.py`
passed (**231 passed, 14 subtests**); `PYTHONPATH=src python -m catalytic_earth.cli validate` passed
(12 source records, 14 mechanism fingerprints, 17 mechanism ontology families, 702 curated labels);
`git diff --check` clean. Real-registry test pins were updated from expansion 2940 / combined 3642 to
expansion 3340 / combined 4042.

Next decision: the immediate low-risk within-14fp cap fill is exhausted; the next high-value scaling
lane is **SAM methyltransferase**. Treat it as a deliberate **15-fingerprint universe change**:
add fingerprint spec + ontology node; add EC 2.1.1 scope with SAM/SAH Rhea participant or
Methyltransferase keyword corroborator and a **no Fe-S** guard to keep radical-SAM separate; add
offline leakage/trust-tier tests; re-freeze the OOS pre-registration to 15fp; then run a
non-destructive preview before any apply.

References:
`artifacts/v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702.json`,
`artifacts/v3_glycosyltransferase_cap_fill_preview_current702.json`,
`work/nad_glycosyltransferase_subfamily_sourcing_current702.md`,
`work/glycosyltransferase_cap_fill_current702.md`,
`work/nad_glyco_floor_expansion_apply_current702_20260612.md`,
`artifacts/v3_coverage_redundancy_audit_current702_20260612_nad_glyco_applied.json`,
`work/coverage_redundancy_audit_current702_20260612_nad_glyco_applied.md`,
`data/registries/external_bronze_labels.json`.

## 2026-06-12: BROADENED EVIDENCE HANDLES WIRED INTO THE ADMISSION ENGINE — nad_p_dehydrogenase + glycosyltransferase (preview only)

Decision: wired the broadened (non-cofactor) MECHANISM handles into the admission engine
family-by-family, so families whose defining evidence is NOT a UniProt cofactor comment can be
admitted honestly. NON-DESTRUCTIVE preview only — no `--apply`, no registry/label write; the frozen
current702 benchmark is byte-unchanged (`sha256:5eec9bef…`); the separate expansion registry stays
2940. This is the concrete next step the prior EC-axis-split entry handed off.

**Engine generalization (the core).** `external_cofactor_ec_disambiguation` corroborated family
scope ONLY via `cofactor_evidence` (the UniProt COFACTOR comment). Generalized it to a per-family
MECHANISM CORROBORATOR (`mechanism_corroborator_axes`) that, in addition to cofactor, reads:
cosubstrate / Rhea reaction participant (from the catalytic-activity reaction text already on the
ingestion row), functional keyword (UniProt entry `keywords`, now extracted in
`adapters.normalize_uniprot_entry_json` and carried on the ingestion row), and binding-/active-site
feature presence (normalized residue locators). "Exactly one rule fires" is preserved: the EC-prefix
predicate stays the SCOPE selector (which lane), and a mechanism axis CONFIRMS membership. Each
admission now maps to `source_trust_tiers.evaluate_corroboration(source_tier="source_tier_0",
present_axes=[…])` and must ADMIT (≥1 counted MECHANISM axis) before a label is built; **EC is passed
as `ec_scope_hint` and is NEVER a counted corroborator** (tier_0 still needs ≥1 mechanism axis, so
EC alone can never admit a row). The broadened handles (keyword / binding / active-site / cosubstrate
Rhea participant) are SCOPE/ADMISSION evidence → recorded under `evidence.source_trust_tier` +
`import_gate_evidence` + `excluded_context`, **never predictive features** (`predictive_evidence`
stays `[]`; the leakage wall is unchanged).

**First batch (two families).** (1) `nad_p_dehydrogenase` — EC 1.1.1, SPLIT into capped EC-subclass
lanes (the scout's "huge, ortholog-padded pool"); corroborator = NAD(P) cosubstrate (Rhea
nicotinamide participant or NAD/NADP keyword) + active-site/Rossmann; deploy-missing context =
NAD(P) cosubstrate; chemistry-confusable → cap 150. (2) `glycosyltransferase` — EC 2.4; corroborator
= sugar-nucleotide donor (Rhea participant) or Glycosyltransferase keyword; deploy-missing context =
sugar-nucleotide donor; cap 250. For EACH: fingerprint spec (`mechanism_fingerprints.json`, with the
declared deploy-missing context), ontology node (`mechanism_ontology.json`: `nicotinamide_redox`,
`glycosyl_transfer`), disambiguation rule (broadened corroborator + EC-scope predicate), lane queries
+ the `DEPLOY_MISSING_CONTEXT_FOR_FINGERPRINT` analog (`external_annotation_anchored_import.py`),
governor signature (`coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES`), and OFFLINE tests
(injected fetchers). Runner modeled on the Stage-2 hydrolase runner:
`nad_glycosyltransferase_subfamily_sourcing.py` / `scripts/source_nad_glycosyltransferase_families.py`.

**Live preview (real UniProt, `--max-records-per-lane 25`, non-destructive).** fetched **149** rows →
mechanism-corroborated **128** (EC scope + ≥1 mechanism axis) → novelty-admitted **127** →
cap-guarded **127** (0 held@cap) → projected: **nad_p_dehydrogenase 0→93** (cap 150),
**glycosyltransferase 0→34** (cap 250); combined 3642 → **3769 if merged**; 2 lane search timeouts
(sandbox network), so true supply is higher and **neither family reached the 100-floor at 25/lane**
— re-run at a higher per-lane size (and retry the 2 timed-out lanes) to reach the floor. The recovery
is real: e.g. P16152 (an SDR) — invisible to the cofactor-only handle — is admitted via 4 mechanism
axes (active-site, cofactor_or_cosubstrate=NAD, domain/keyword, Rhea participant) with EC as a
non-counted scope hint and `predictive_evidence []`. Counters stay SEPARATE (this is positive_bronze;
OOS/silver untouched).

**Universe 12 → 14 (Stage-3-style re-freeze, mirrors the 8→12 Stage-2 bump).** Adding two positive
fingerprints expanded the live universe to 14, which invalidated the 12fp OOS hard-negative
pre-registration. Per the established pattern: bumped
`labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` → `label_factory_v1_14fp`; re-froze the OOS
prereg as `artifacts/v3_external_hard_negative_next_tranche_preregistration_14fp_1025.json`
(supersedes the 12fp one; 12fp/8fp kept as historical records); added
`transfer_scope.EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_14FP_ARTIFACT`. The historical
label stamp `DEFAULT_ONTOLOGY_VERSION_AT_DECISION` STAYS `label_factory_v1_8fp` (decoupled, never
rewrites history). Consequence (documented, not a regression): the OOS inverse gate now reports
`incomplete_current_fingerprint_coverage` until the two new positive fingerprints gain atlas
coverage, so a NEW OOS hard-negative tranche stays blocked until then — exactly the Stage-3
behavior. Governor correctly lists the two new families as expansion holes (by construction, until
the preview is applied). `validate` ok (14 fingerprints / 17 ontology families / 702 frozen labels);
full offline suite green except the 6 known env-backend failures; `git diff --check` clean.

**STOP before --apply.** The preview is reported for authorization of the registry merge; nothing is
applied. References: `src/catalytic_earth/external_cofactor_ec_disambiguation.py` (broadened
corroborator), `src/catalytic_earth/nad_glycosyltransferase_subfamily_sourcing.py`,
`scripts/source_nad_glycosyltransferase_families.py`,
`tests/test_nad_glycosyltransferase_subfamily_sourcing.py`,
`artifacts/v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702.json`,
`work/nad_glycosyltransferase_subfamily_sourcing_current702.md`.

## 2026-06-12: EC IS SCOPE-ONLY, NEVER A COUNTED CORROBORATOR — Trust-Tier Axis Split + Mechanism-First Affirmation

Decision: after a review of "why do we depend so much on EC," affirmed the principle and fixed one
genuine inconsistency. EC stays ALLOWED for fetch / scope / stratification and `excluded_context` —
that is the deliberate, sound leakage-wall design (EC decides scope, is never a predictive feature),
NOT a drift to refactor away. The predictor/atlas is already EC-free by that wall (features = cofactor
identity, Rhea bond-change, active-site roles, geometry; 1c reads Rhea, not EC). What WAS inconsistent:
the new `source_trust_tiers.CORROBORATOR_AXES` lumped Rhea with EC under `reaction_or_rhea_or_ec_family`,
contradicting its own rule that EC is not a corroborator. Split it — counted MECHANISM axis
`rhea_reaction_or_participant_pattern`; non-counted scope axis `ec_scope_hint` (recognized + allowed,
but can never satisfy any part of the N-of-M rule). `evaluate_corroboration` now reports
`scope_hint_axes_present_not_counted` separately from unknown axes; new tests prove EC alone cannot
admit a label even at tier_0 and cannot inflate the corroborator count at any tier. Net principle
(durable): **fetch broadly (EC/keyword), decide membership by MECHANISM evidence (Rhea, cofactor/
cosubstrate, active-site, domain, cluster, structure); EC is the scope selector + stratifier only.**
Next step (prompt handed to the user): wire the broadened mechanism handles (keyword / binding-site /
active-site / cosubstrate-Rhea) into the admission engine family-by-family, with EC as the scope
selector and the trust-tier N-of-M requiring ≥1 mechanism corroborator. Non-destructive; no registry/
label written; frozen current702 untouched (`sha256:5eec9bef…`); module tests green.

References: `src/catalytic_earth/source_trust_tiers.py`, `tests/test_source_trust_tiers.py`,
`artifacts/v3_source_trust_tier_policy_current702.json`.

## 2026-06-12: EVIDENCE-HANDLE EXPANSION + SOURCE TRUST-TIER POLICY — Fix Within-Swiss-Prot Handles First, Then Expand Sources Honestly (Separate Counters)

Decision (user direction, 2026-06-12): the breadth scout's "reviewed Swiss-Prot can't reach 10k
positive bronze" is TWO findings, and they get two different responses. (1) Some apparent shortage
is an EVIDENCE-HANDLE problem, not a supply problem — fix the within-Swiss-Prot corroborators
BEFORE leaving Swiss-Prot. (2) The genuine remainder needs source expansion beyond Swiss-Prot, but
through trust tiers with escalating multi-corroborator requirements — and the 10k target must NOT
be redefined to paper over a positive-label gap (positives / OOS / silver depth stay separate
counters). Two non-destructive modules deliver this; neither writes a registry or a label; frozen
current702 untouched (`sha256:5eec9bef…`).

**(1) Evidence-handle expansion (measured).** New `evidence_handle_expansion.py` /
`scripts/scout_evidence_handle_expansion.py` (offline-tested) measures, per family, how much
reviewed supply each alternative within-Swiss-Prot corroborator handle recovers — `cc_cofactor`
vs `keyword` (controlled-vocab functional/family) vs `ft_binding` (binding-site) vs `ft_act_site`
(active-site). EC scope is the ceiling but is NOT counted as a corroborator (EC decides scope only,
stays excluded). The decision-grade result (live UniProt): **NAD(P) dehydrogenases (EC 1.1.1):
`cc_cofactor:nad/nadp` reaches 7 of 7804 reviewed; `keyword:NAD/NADP` reaches 7700** (NAD(P) is a
cosubstrate recorded as KW-0520/0521, not a cofactor comment — exactly the ser_his lesson: a
family whose defining evidence isn't a cofactor needs a different corroborator). Also SAM-MTase
`cc_cofactor` 691 → `keyword:Methyltransferase` 14279; broad NAD(P) oxidoreductase 50 →
`ft_binding` 28669; biotin carboxylase 60 → `ft_binding` 3831; glycosyltransferase (no cofactor
handle) → `keyword` 10281. Across 6 families the broader handles recover **~64k raw reviewed
entries** the cofactor handle misses (RAW/illustrative — the broad EC 1.* lane OVERLAPS EC 1.1.1,
so pools overlap, not additive) and **~741 additional reachable POSITIVE bronze** once cap +
novelty discount are applied (the bounded figure); 4 families cross the 100-floor only with the
better handle. These winning handles are the corroborators to wire into the import gate per family;
the big pools (broad oxidoreductase) must be split by EC-subclass into capped lanes, not sourced as
one bucket. Leakage: every handle is reviewed annotation used for SCOPE/admission only
(`excluded_context`, never predictive) — same basis as the existing cofactor+EC handle.

**(2) Source trust-tier + N-of-M corroboration + separate-counters policy.** New
`source_trust_tiers.py` (offline-tested) encodes the durable governance the future admission engine
consumes: `SOURCE_TRUST_TIERS` 0–4 (0 reviewed Swiss-Prot → 4 model projection), only **0–2
bronze-eligible** with escalating `min_independent_corroborators` (1 / 2 / 3), tiers **3–4 are
hypotheses, never countable bronze** (upgrade-only); `CORROBORATOR_AXES` (6 independent evidence
axes) + `evaluate_corroboration` (the N-of-M rule, distinct axes only); and `HONEST_COUNTER_AXES`
— `positive_bronze` / `oos_bronze` / `silver_ready` / `silver_confirmed` / `projected_provisional`,
which **must never be merged into one victory number**. `build_counter_ledger` over the current
registries at that decision point: **positive_bronze 1929, oos_bronze 1696, silver_ready 0, silver_confirmed 17,
projected 0** (the 17 silver are the already-promoted positives; 1929 bronze + 17 silver = 1946
total positives — the counters separate tiers honestly). Trust tiers ADD a gate; the governor,
novelty gate, dedup-vs-both-registries, and leakage gate stay mandatory for every candidate.

Net plan (replaces "reviewed Swiss-Prot → 10k bronze", which the scout disproved): reviewed
Swiss-Prot with broadened family-specific evidence handles + curated external (tier 1) + carefully
gated TrEMBL/UniRef (tier 2, N-of-M) + new family ontology breadth (Stage 2) + the mandatory
governor/novelty gate = a path to 10k DIVERSE positive bronze, with OOS and silver tracked
separately, never count-inflated. `validate` ok (702/12/15); full suite green except the 6 known
env-backend failures; no registry written.

References:
- `src/catalytic_earth/evidence_handle_expansion.py`, `scripts/scout_evidence_handle_expansion.py`,
  `tests/test_evidence_handle_expansion.py`,
  `artifacts/v3_evidence_handle_expansion_current702.json`,
  `work/evidence_handle_expansion_current702.md`.
- `src/catalytic_earth/source_trust_tiers.py`, `tests/test_source_trust_tiers.py`,
  `artifacts/v3_source_trust_tier_policy_current702.json`.

## 2026-06-11: STAGE-3 PREREQS — OOS Hard-Negative Pre-Registration Re-Frozen To The 12fp Universe + Clean Ontology Version Bump (Decoupled)

Decision: completed the two deferred Stage-3 prerequisites the Stage-2 split created, so a NEW
OOS hard-negative tranche can be imported. Both are required BEFORE any new OOS import; neither
writes a label or touches the frozen 702 (`sha256:5eec9bef…` unchanged; registries unchanged).

**(1) Re-froze the OOS hard-negative pre-registration to the 12fp universe.** New governance
artifact `artifacts/v3_external_hard_negative_next_tranche_preregistration_12fp_1025.json`
(generated from the 8fp template + the LIVE `load_fingerprints()`, so its `fingerprint_universe`
is guaranteed to equal the gate's `expected`): `fingerprint_universe` = the live 12,
`ontology_version_at_decision` = `label_factory_v1_12fp`, `registration_status` =
`frozen_before_candidate_selection`, `candidate_selection_started` = false, same
`version`/`threshold_policy_version`/`abstain_threshold`/`inverse_gate_rule`, plus `supersedes`
+ `re_freeze_reason`. The 8fp-era artifact
(`v3_external_hard_negative_next_tranche_preregistration_1025.json`) is KEPT on disk as the
superseded historical record (the two existing supersession leakage tests stay green; it is now
blocked by BOTH the universe-match AND the ontology-version checks).

**(2) Clean ontology version bump — DECOUPLED, not a global rename (the load-bearing decision).**
`label_factory_v1_8fp` is NOT a free-floating string: it is stamped as `ontology_version_at_decision`
on EVERY existing label (frozen 702 + 2940 expansion), on the spent-heldout / threshold leakage
contracts, and on 60+ `transfer_scope` decision/gate artifacts; ~20 tests pin it. Globally renaming
it would rewrite history and (via the `MechanismLabel` field default + re-dumps) risk the frozen-702
hash. So the bump is decoupled: `labels.DEFAULT_ONTOLOGY_VERSION_AT_DECISION` STAYS
`label_factory_v1_8fp` (the historical label/decision stamp, retained for provenance), and a NEW
constant `labels.CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION = "label_factory_v1_12fp"` denotes
the CURRENT live positive universe. The OOS hard-negative import gate
(`transfer_scope._validate_pre_registration`) now requires the pre-registration to declare the
CURRENT version (`…ontology_version_at_decision != CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION`
→ blocker), so a new tranche must be pre-registered against the live 12fp universe. The candidate-row
ontology-consistency checks (`…!= DEFAULT_ONTOLOGY_VERSION_AT_DECISION` at the terminal-row level)
correctly STAY `_8fp` — they verify a row matches the registry's label stamp, a different concept
from the inverse-gate universe version.

Tests (updated intentionally): the accept-test now loads the real 12fp artifact and asserts the gate
accepts it (universe + ontology both current); a new `test_12fp_pre_registration_is_frozen_for_live_universe`
asserts the artifact is frozen-before-selection against the live 12 with `_12fp`; the stale-8fp test
now asserts BOTH the `fingerprint_mismatch` AND `ontology_mismatch` blockers fire. The historical
`_8fp` assertions (threshold-policy pins, migration, transfer/scaling fixtures) are untouched.

Validation: `validate` ok (702/12/15). Full suite green except the 6 known env-backend failures.
Frozen current702 `sha256:5eec9bef…` before and after; registries unchanged; `git diff --check` clean.
Stage 3's OOS hard-negative import is now unblocked (still gated by the full label-factory +
external-transfer gates and explicit authorization — re-freeze ≠ import).

References:
- `src/catalytic_earth/labels.py` (`CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION`),
  `src/catalytic_earth/transfer_scope.py` (gate check + the 12fp artifact path constant),
  `artifacts/v3_external_hard_negative_next_tranche_preregistration_12fp_1025.json`,
  `tests/test_leakage_closure.py`.

## 2026-06-11: BREADTH FEASIBILITY SCOUT — Real Numbers Say 10k Diverse POSITIVE Bronze Is NOT Reachable From Reviewed Swiss-Prot Alone

Decision: before spending more windows sourcing bronze, REPLACED the scaling-plan cap-math
*estimate* ("~2k positives + diverse OOS") with REAL reviewed-Swiss-Prot numbers. New reusable,
non-destructive recon module `breadth_feasibility_scout.py` + `scripts/scout_breadth_feasibility.py`
(offline-tested with injected fetchers) probes 18 curated candidate mechanism families BEYOND the
current 12 (non-hydrolase first), measuring per narrow EC/cofactor lane: reviewed-entry supply (the
cheap `x-total-results` header count — no paging, no sequence transfer), the EC supply ceiling
(same EC prefixes with NO cofactor filter), reaction diversity (distinct full-EC over a ≤200-row
sample = a sampled LOWER bound → labels/reaction is a conservative UPPER bound on redundancy), the
150-vs-250 cap (Stage-2 lesson: 150 when chemistry is confusable), and EC-overlap redundancy vs
`coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES`. It writes NO registry and creates NO
labels (nothing for the leakage wall to gate); EC/cofactor are used for supply/scope estimation
only, never as predictive features.

Headline verdict (live UniProt): **`ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone`.**
Current combined positive bronze is **1946** across 12 fingerprints. Beyond those, **15 of 18**
candidate families are "clean" (distinct + floor-reachable + non-redundant) and **0** are redundant
with an existing lane — so breadth genuinely exists. But the honest discounts are large: the clean
families' capped, novelty-discounted supply projects to only **~4737** diverse positive bronze
(cap-sum +2791), a **gap of 5263** to 10k; and **9 of 15** clean families are reaction-poor
(ortholog padding — many entries, few distinct reactions), dropping the diversity-discounted new
bronze to **~1936**; and **8 of 18** families have a WEAK cofactor handle (it reaches <25% of the EC
supply ceiling). The biggest weak-handle case is decision-grade: **NAD(P)-dependent dehydrogenases
(EC 1.1.1) have ~7804 reviewed entries but the `cc_cofactor:nad/nadp` handle captures only 7**
(0.001) — NAD(P) is a *cosubstrate*, not a UniProt COFACTOR comment, so the entire largest
oxidoreductase pool is unreachable by the current cofactor-anchored import gate without a new
**sequence-motif / EC-only handle** (Rossmann GxxxGxG). SOD (EC 1.15.1.1) and biotin carboxylases
are similarly handle-blocked.

What this means for the target (honest, plainly): reviewed Swiss-Prot yields **low thousands of
diverse POSITIVE bronze, not 10k**. 10k is reachable only if it is DEFINED as positives + diverse
novelty-gated OOS + bronze→silver depth (not positive bronze alone), OR if sources beyond reviewed
Swiss-Prot are admitted (TrEMBL/UniRef cluster representatives, BRENDA, structure-anchored families).
The clean non-hydrolase families worth sourcing first (real chemistry breadth, defensible handles):
`non_heme_iron_2og_dioxygenase`, `cytochrome_p450_monooxygenase`, `copper_oxidoreductase`,
`molybdopterin_oxidoreductase`, `glycosyltransferase`, `coa_acyltransferase`,
`cofactor_independent_isomerase` (cofactorless → apo-confirmable like ser_his). Reaction-poor or
weak-handle lanes (`enolase_superfamily`, `sam_methyltransferase` EC 2.1.1.- partial-EC,
`nad_p_sdr`) are NOT clean wins by volume.

This is the artifact the user uses to decide scope; TASK 3 (source one new non-hydrolase family) is
gated on that decision. New `fetch_uniprot_query_count` / `fetch_uniprot_ec_sample` adapters
(header-count + EC-only sample) are the reusable cheap-recon primitives. `validate` ok (702/12/15);
full suite green except the 6 known env-backend failures. Frozen current702 untouched
(`sha256:5eec9bef…`); no registry written.

References:
- `src/catalytic_earth/breadth_feasibility_scout.py`, `scripts/scout_breadth_feasibility.py`,
  `tests/test_breadth_feasibility_scout.py`, `src/catalytic_earth/adapters.py` (count + EC sampler),
  `artifacts/v3_breadth_feasibility_scout_current702.json`,
  `work/breadth_feasibility_scout_current702.md`.

## 2026-06-11: TRACK 1 (context depth) — 1c Leakage-Safe Row-Specific Bond-Change Feature (Metal Sub-Families Now Separable)

Decision: closed the Stage-2 deferred-feature gap. The Stage-2 split was honest at the
EC/reaction/bronze level, but the leakage-safe CHEMISTRY representation
(`mechanism_representation_loop`) could not separate the four metal sub-families — they share
the divalent-metal cofactor and His/Asp/Glu water-activator residue roles, and differ only by
the reaction-center BOND hydrolysed (peptide C-N vs phosphodiester P-O vs phosphomonoester P-O
vs non-peptide amide/amidine C-N). 1c adds that bond change as a leakage-safe, row-specific
feature derived from the Rhea reaction.

Leakage discipline (the crux): the feature is derived ONLY from the reaction equation's
substrate→product chemistry (`evidence.mechanism_evidence.reaction_equations[].reaction`) — the
legitimate North Star axis, exactly like cofactor identity. It is NOT:
- the fingerprint's DECLARED bond_change (`mechanism_fingerprints.json`) — using that would
  leak the label directly;
- the EC number (an excluded predictive field; the co-stored `reaction_equations[].ec_number`
  is never read);
- protein name / prose / lane / fingerprint id.
The classifier fires only for HYDROLYSIS (water on the substrate side), which is precisely what
the four metal hydrolase sub-families do and what distinguishes them; non-hydrolase chemistries
(lyases/transferases — e.g. cobalamin ethanolamine ammonia-lyase, "ethanolamine = acetaldehyde
+ NH4(+)", no water) yield NO bond-change class and stay out of the bond space.

What was built/changed:
- `mechanism_representation_loop.py`: four bond-change feature dimensions
  (`bc_phosphomonoester`, `bc_phosphodiester`, `bc_peptide_cn`, `bc_amide_cn`) added to
  `FEATURE_NAMES` (after the cofactor classes, which stay the prefix the centroid helpers
  index). A deterministic `classify_reaction_bond_change(reaction)` reads only the reaction
  string; `featurize` sets the bond-change features at full weight (co-equal with cofactor —
  NOT tuned to the metric). `promotion_triage` now also reports
  `self_consistency_by_fingerprint`. The feature_space basis and leakage guardrails record the
  new axis explicitly (`bond_change_derived_from_reaction_substrate_product_only: true`,
  `fingerprint_declared_bond_change_used_as_feature: false`,
  `reaction_ec_number_used_as_feature: false`).
- Tests: `tests/test_mechanism_representation_loop.py` gained classifier unit tests (the four
  hydrolysis classes; lyase-without-water → no class; featurize sets bond-change and ignores
  the co-stored reaction ec_number) and the real-registry guard was rewritten to assert the
  measured win.

Result (LOO self-consistency, measured honestly — not forced): overall **0.679 → 0.751**;
metal-only **0.49 → 0.64** (dragged down only by the v1 umbrella, see below). The four v2
sub-families, ~indistinct before, are now strongly separable: metallopeptidase **0.95**,
metallophosphoesterase_nuclease **0.93**, metallophosphomonoesterase **0.89**,
metallo_amidohydrolase_deaminase **0.75** (v2-only ≈ **0.88**). Non-metal separability is
PRESERVED exactly at **0.854** (the water constraint excludes the non-metal lyase reactions
that would otherwise pollute the bond space). The coarse v1 umbrella `metal_dependent_hydrolase`
now (correctly) scatters to its sub-families — it has no single bond-change signature — so its
own self-consistency drops to ~0; that is the split working as intended, not a regression.

Honest limitations (disclosed, not hidden): (1) reviewed metallopeptidase entries largely lack
a small-molecule Rhea reaction (110/150 have none — the substrate is a generic protein), so
their separation is partly "metal hydrolase with NO hydrolysis-reaction bond-change" by
elimination; phosphomono/diester/amide are cleanly reaction-driven. (2) The flavin
monooxygenase vs dehydrogenase/reductase confusion (a pre-existing flavin-subtype issue, same
"needs a reaction-derived feature" shape but for redox, not hydrolysis) is unchanged — the
hydrolysis-only bond-change does not touch it.

This is the discriminator for ALL future fine splits, not just the metal family. It is a
research/triage diagnostic for the expansion's self-organisation (promotion triage + hole
proposal); it is NEVER a benchmark scorer, and the frozen 702 benchmark is never read.

Validation: `validate` ok (702/12/15). Full suite green except the 6 known env-backend
failures. Frozen current702 untouched (`sha256:5eec9bef…`); this commit writes no registry.

References:
- `src/catalytic_earth/mechanism_representation_loop.py`,
  `tests/test_mechanism_representation_loop.py`,
  `artifacts/v3_mechanism_representation_loop_current702_20260610.json`,
  `work/mechanism_representation_loop_current702_20260610.md`.

## 2026-06-11: TRACK 1 (context depth) — 1b Stage AlphaFoldDB v6 Coordinate Provenance For Expansion Labels

Decision: continued Track 1 (rich per-label context) by staging the predicted STRUCTURE for
every expansion label. With the deploy-input sequence on every label (1a), the next missing
context is the coordinate — it unlocks geometry / active-site context and the bronze→silver
promotion path for all families (the geometry inverse-gate, foldseek near-duplicate screen,
etc.). Recorded under `evidence.structure_provenance.afdb_v6_coordinate`. Frozen current702
byte-unchanged (`sha256:5eec9bef…`; 702 labels) before and after.

Why hash-only (regeneratable, not committed): the AFDB v6 CIFs are ~0.5 MB each and are
fully regeneratable from the handle (`AF-{accession}-F1-model_v6.cif`). Committing ~2.9k CIFs
(~2 GB) would bloat the repo for zero information gain. So each CIF is staged to a temp dir,
hashed (sha256) + measured (bytes, atom-record count), and discarded; only the hash + handle
+ provenance are stored. This is the `ser_his_hole_sourcing.py` staging pattern generalized.

What was built/changed:
- **New reusable module** `src/catalytic_earth/label_structure_backfill.py` +
  `scripts/backfill_label_structures.py`. The `afdb_v6_coordinate` block carries
  structure_handle, model_url, model_version (`v6`), coordinate_sha256, coordinate_bytes,
  atom_record_count, retrieved_utc, status (`afdb_v6_predicted_coordinate_staged` or
  `afdb_v6_unavailable`), and `coordinate_committed=false` / `regeneratable_from_handle=true`.
  A retry-aware fetcher distinguishes a genuine 404 (no AFDB prediction → recorded
  `unavailable`) from transient errors (retried with backoff; raises rather than caching a
  blip as permanent). Non-destructive: a small summary preview artifact + work report are
  written always; `--apply` writes the expansion registry ONLY (via the canonical compact
  `_dump_registry`), and the writer refuses to target the frozen benchmark. A resumable cache
  under the git-ignored `data/cache/` (flushed every 100 fetches) shares one network pass
  across preview→apply and survives interruption; `--limit` supports chunked runs.
- **Additive to existing structure_provenance:** the block is nested under each row's existing
  `structure_provenance`; the existing `coordinate_status` / `coordinate_path` (incl. the
  ser_his triad-confirmed status and the 317 committed wave2 paths) are preserved untouched.
- **Tests:** new `tests/test_label_structure_backfill.py` (offline, injected CIF fetcher:
  stage+hash without keeping the CIF, 404→unavailable, additive-preserve, `--limit` deferral,
  idempotent re-run, resumable cache, preview-non-destructive vs apply-writes-expansion-only,
  refuses-frozen-target).

Result (live AFDB egress): 2940 expansion labels → **2890 staged (98.3%); 50
`afdb_v6_unavailable`** (AFDB has no v6 prediction — typically very long sequences; recorded
honestly, never fabricated). Row counts UNCHANGED; the count-pins (combined 3642, expansion
2940, seed_labels 1716) stay valid. The only registry diff is the added
`structure_provenance.afdb_v6_coordinate` key per row (verified: stripping it makes all 2940
rows byte-identical to HEAD); no CIFs committed; `git diff --check` clean.

Validation: `validate` ok (702 frozen intact; 12 fingerprints; 15 families). Full suite green
except the 6 known env-backend failures. Frozen current702 sha `5eec9bef…` before and after.

Honesty: structure is review-only mechanism context (a deferred bronze→silver confirmation
signal), NEVER a predictive feature — bronze stays honest. The staged coordinate is the AFDB
**apo** prediction (cofactor-missing), so the geometry inverse-gate still abstains on it; the
hash provenance is what makes the bronze→silver geometry/foldseek work *runnable* later, not a
silver promotion itself.

References:
- `src/catalytic_earth/label_structure_backfill.py`,
  `scripts/backfill_label_structures.py`,
  `tests/test_label_structure_backfill.py`,
  `artifacts/v3_label_structure_backfill_preview_current702.json`,
  `work/label_structure_backfill_current702.md`.

## 2026-06-11: TRACK 1 (context depth) — 1a Backfill The Deploy-Input Sequence Onto Every Expansion Label

Decision: began Track 1 of the scaling plan (rich per-label context / depth — the user
approved "depth first") by closing the most basic gap: the atlas maps a raw protein
**SEQUENCE → mechanism**, yet the expansion registry stored only the UniProt handle +
length — never the sequence. So the one input a deployed model actually predicts FROM was
absent for all 2940 expansion labels (the frozen-702 sequences live in a separate
manifest, `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`). Backfilled
the reviewed UniProt sequence onto every expansion label under
**`evidence.sequence_provenance`**. Frozen current702 byte-unchanged
(`sha256:5eec9bef…`; 702 labels) before and after.

Why the sequence is allowed (the leakage distinction, restated): the leakage wall keeps
EC / protein name / UniProt prose / `target_family_lane` in `excluded_context`, never
predictive (`predictive_evidence` stays `[]`; `tests/test_leakage_closure.py` enforces
it). The raw **sequence is the deploy INPUT** — what we predict FROM — and is NOT
EC/name/prose, so it is stored as DATA under `evidence.sequence_provenance`. It must never
appear in `excluded_context` or `predictive_evidence`; the wall is unchanged. Proven: the
block survives `MechanismLabel.from_dict().to_dict()` for both seed and out_of_scope
labels, and the OOS leakage validator accepts it (re-verified by round-trip on all 2940).

What was built/changed:
- **New reusable module** `src/catalytic_earth/label_sequence_backfill.py` +
  `scripts/backfill_label_sequences.py`. The `sequence_provenance` block carries: `sequence`,
  `sequence_sha256`, `sequence_length`, `source_accession`, `source` (=`reviewed_uniprot`),
  `retrieval` provenance (endpoint/fields/batch/reviewed_status), and `retrieved_utc`. The
  fetched length is cross-checked against the stored `source_provenance.sequence_length`; on
  mismatch a `length_conflict_note` is recorded and the stored length is **preserved, not
  overwritten** (0 conflicts on this run). Fetching reuses
  `adapters._fetch_text/_chunked/_split_accessions/USER_AGENT/UNIPROT_SEARCH_URL` with a field
  set that INCLUDES the sequence (the default `fetch_uniprot_accessions` omits it), batched 25;
  a small fetch cache under the git-ignored `data/cache/` lets preview and `--apply` share one
  network pass. Non-destructive: a small **summary** preview artifact + work report are written
  always; `--apply` writes the expansion registry ONLY, via the same compact `_dump_registry`
  serializer, and the writer refuses to target the frozen benchmark path.
- **Source-time wiring** so future sourced labels get the sequence natively:
  `external_source_ingestion._candidate_row` now carries `sequence` + `sequence_sha256` from the
  reviewed search record, and `external_annotation_anchored_import._build_label` populates
  `evidence.sequence_provenance` from the row when present (omitted gracefully when absent — the
  synthetic anchored-import test rows that lack a sequence are unaffected).
- **Tests:** new `tests/test_label_sequence_backfill.py` (offline, injected fetcher: seed+OOS
  backfill, row-count/frozen guardrails, length-conflict note, fetch-miss never fabricated,
  idempotent re-run, fetch-cache reuse, preview-non-destructive vs apply-writes-expansion-only,
  refuses-frozen-target, canonical-serializer round-trip). Updated the stage1/stage2 + anchored
  offline tests' synthetic rows + assertions intentionally to assert the source-time block.

Result (live UniProt egress): 2940 expansion labels → **2940/2940 backfilled (100% coverage,
0 fetch-missing, 0 length-conflicts)**; seed 1716/1716 and OOS 1224/1224 both carry the
sequence. Row counts UNCHANGED (a block added in place); the count-pins (combined 3642,
expansion 2940, seed_labels 1716) stay valid and were not changed. The only registry diff is
the added `sequence_provenance` key per row (verified: stripping it makes all 2940 rows
byte-identical to HEAD); `git diff --check` clean.

Validation: `validate` ok (702 frozen intact; 12 fingerprints; 15 ontology families). Full
suite green except the 6 known env-backend failures (numpy/esm2/mmseqs). Frozen current702 sha
printed before AND after the apply — `5eec9bef…` both times (it did not move).

Next (Track 1, separate commits): 1b stage AlphaFoldDB v6 coordinates
(`.../AF-{acc}-F1-model_v6.cif`) for expansion labels with a handle and record
`evidence.structure_provenance` (hash + path-handle; coordinates are regeneratable so large
CIFs are NOT committed); 1c build the leakage-safe row-specific BOND-CHANGE feature from Rhea
reactions (substrate→product chemistry, NOT the fingerprint's own bond_change — that would
leak) — the discriminator that makes the four metal sub-families predictively separable.

References:
- `src/catalytic_earth/label_sequence_backfill.py`,
  `scripts/backfill_label_sequences.py`,
  `tests/test_label_sequence_backfill.py`,
  `artifacts/v3_label_sequence_backfill_preview_current702.json`,
  `work/label_sequence_backfill_current702.md`.

## 2026-06-11: STAGE 2 STARTED — metal_dependent_hydrolase v2 Split Into Four Sub-Families (+600 bronze)

Decision: began Stage 2 (grow the ontology — the real 10k lever) by splitting the
coarse, over-cap `metal_dependent_hydrolase` umbrella into **four mechanistically
distinct v2 sub-families**, separated by reaction-center bond change (not by metal
alone), and sourced fresh annotation-anchored bronze for each to the floor. Frozen
current702 byte-unchanged (`sha256:5eec9bef…`; 702 labels) before and after.

The four sub-families (each carries a catalytic divalent metal; the EC-class
disambiguation rule enforces the bond-change distinction):

- `metallopeptidase`                 — peptide C-N hydrolysis        (EC 3.4.24/17/11; Zn2+, HExxH/dizinc)
- `metallophosphoesterase_nuclease`  — phosphodiester P-O hydrolysis (EC 3.1.4, 3.1.1x-3.1.3x; two-metal Mg/Mn)
- `metallophosphomonoesterase`       — phosphomonoester P-O hydrolysis (EC 3.1.3; dinuclear Zn/Mg/Mn/Fe)
- `metallo_amidohydrolase_deaminase` — non-peptide amide/amidine C-N (EC 3.5.2/4/1; Zn2+, mono/di-nuclear)

Why a split (the cap math): 8 fingerprints x 250 cap ~= 2,000 positives is the honest
v1 ceiling. 10k requires more mechanism families. `metal_dependent_hydrolase` was the
lone over-cap (308) and the coarsest bucket (collapsing proteases / nucleases-PDEs /
phosphatases / deaminases). Splitting it is Lever-4 (expand the family set) and the
designated Stage-2 on-ramp. The user approved a 4-way split + define-and-source-to-floor.

What was built/changed:
- **Registry specs (checklist 1):** four fingerprint specs added to
  `mechanism_fingerprints.json` (cofactor + active-site residue-role signature +
  reaction-center bond change), each declaring its **deploy-missing active-site
  context** (all `metal`; checklist 3) in a `deploy_missing_active_site_context`
  field. Four ontology nodes added to the `hydrolysis` family in
  `mechanism_ontology.json` with a v2-split note + boundary guardrails. The coarse
  `metal_dependent_hydrolase` is KEPT as the v1 umbrella (its 83 frozen + 225 expansion
  rows cannot move; **no new labels are added to it**).
- **Disambiguation (checklist 2):** added a `metal` cofactor-evidence detector and four
  metal+EC rules to `external_cofactor_ec_disambiguation.DISAMBIGUATION_RULES`
  (mutually-exclusive EC prefixes + a required catalytic metal -> "exactly one rule
  fires"; the metal requirement excludes Ser/Cys peptidases and Cys-based
  protein-tyrosine phosphatases 3.1.3.48, which carry no catalytic metal). Lane maps +
  `COFACTOR_FOR_FINGERPRINT` (all metal) added in
  `external_annotation_anchored_import.py`. Governor `FINGERPRINT_SOURCING_SIGNATURES`
  gained the four sub-families.
- **Runner (checklist 4):** new `stage2_hydrolase_subfamily_sourcing.py` +
  `scripts/source_stage2_hydrolase_subfamilies.py` (reuses the Stage-1 chain: fetch ->
  metal/EC disambiguation -> novelty gate -> cap guard -> non-destructive preview;
  `--apply` appends to the expansion registry only). Offline tests added.

Result (live UniProt egress; `--cap-ceiling 150`): 1530 reviewed rows over 13 narrow
EC/metal lanes (1 fetch failure) -> 1167 disambiguated bronze -> **600 novelty-admitted**
(150 per sub-family) appended to the expansion registry (**2340 -> 2940**; combined
**3042 -> 3642**). Each sub-family: **0 -> 150** (floor reached). Governor: holes `[]`;
fingerprint Gini **0.1917 -> 0.1518** (most balanced yet); seed positives 1346 -> 1946;
positive:OOS 0.79 -> 1.15; the only over-cap remains the intentional umbrella
`metal_dependent_hydrolase` (308, untouched).

**Cap choice (honesty):** a first split is sourced to **cap 150, not the 250 system
ceiling.** Filling chemistry-confusable sub-families to 250 manufactured redundancy
(a 250-cap dry run put `metallopeptidase` at 7.14 labels/distinct-reaction — *worse*
than the 2.96 parent it splits). At 150: peptidase 5.56, nuclease 2.88, phosphomono
1.25, amidohydrolase 2.63 labels/rxn. `metallopeptidase` stays the most ortholog-heavy
because reviewed metallo-peptidase **reaction** diversity is genuinely limited (~27
distinct reactions); reaching the 100 floor requires cross-organism (ortholog) breadth.
Disclosed, not hidden.

**Key finding (deferred-feature implication):** the leakage-safe **chemistry**
representation (`mechanism_representation_loop`) CANNOT yet distinguish the four metal
sub-families. LOO self-consistency fell ~0.90 (8fp) -> **0.679** (12fp), and the drop is
**entirely within the metal super-family** (metal-only self-consistency 0.49; non-metal
fingerprints stay 0.85). Reason: the sub-families share the available chemistry features
(metal cofactor + His/Asp/Glu water-activator roles) and are separated only by
reaction-center **bond change**, which is not yet a feature (the deferred row-specific
bond-change work; using the fingerprint's own bond-change would leak the label). So the
split is real and honest at the EC/reaction/bronze level, but **separating the metal
sub-families predictively needs the bond-change feature.** The repr-loop test now guards
non-metal self-consistency > 0.8 (preserving the original protection where chemistry can
separate) and overall > 0.6.

**OOS re-audit consequence (the documented guardrail firing):** expanding the positive
fingerprint universe (8 -> 12) correctly invalidates the **8fp-era OOS hard-negative
pre-registration** (`v3_external_hard_negative_next_tranche_preregistration_1025.json`):
the import gate's universe-match check now blocks it
(`external_hard_negative_pre_registration_fingerprint_mismatch`). This is the
"re-audit OOS on positive expansion" rule working as designed; the OOS hard-negative
tranche must be **re-frozen against the 12fp universe** before the next OOS import
(Stage-3 work). Two leakage tests were updated to assert the supersession (the stale
prereg is blocked; a current-universe prereg is accepted). The v1 eval contract
(`v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`) recorded the 8fp
`mechanism_fingerprints.json` hash; that file legitimately grew (append-only — the
original 8 ids unchanged), so the contract's whole-file pin is superseded (test updated
to assert the v1 fingerprints still exist; the frozen-702 label hash is untouched).
The **ontology version key stays `label_factory_v1_8fp`** (it is referenced by the
spent-heldout/threshold leakage contracts; a clean version bump + OOS re-freeze is
deferred Stage-3 work) even though the universe is now 12 — documented here so the name
is not mistaken for a literal count.

Guardrails (verified post-apply): frozen current702 never written; `tier=bronze`,
`review_status=automation_curated`; uniprot namespace; EC/name/prose in
`excluded_context`, `predictive_evidence` empty on all 600; deduped + novelty-gated vs
BOTH registries; multi-fingerprint-signal rows held; per-fingerprint cap guard enforced
(no fingerprint over cap).

Validation: `validate` ok (702 frozen intact; 12 fingerprints; 15 ontology families).
Full suite green except the 6 known env-backend failures (numpy/esm2/mmseqs). Count-pins
refreshed (combined 3042->3642, expansion 2340->2940, seed_labels 1116->1716). Added 8
stage2 offline tests; updated the cli/leakage/automation/repr-loop/transfer-scope tests
for the 12-fingerprint universe (see above). `git diff --check` clean.

**Honest cap-math note:** this one split added +600 positives (seed 1346 -> 1946). Three
more comparable splits/new families would clear the ~2k v1 ceiling, but 10k still
requires sustained **family breadth** (non-hydrolase chemistries too — the hydrolysis
family now holds 6 of 12 fingerprints). Closing/balancing does not get to 10k; breadth
does. Next Stage-2 candidates: glycosidases, oxidoreductase/transferase families, and
re-freezing the OOS hard-negative tranche to 12fp (Stage 3).

References:
- `src/catalytic_earth/stage2_hydrolase_subfamily_sourcing.py`,
  `scripts/source_stage2_hydrolase_subfamilies.py`,
  `tests/test_stage2_hydrolase_subfamily_sourcing.py`.
- `data/registries/mechanism_fingerprints.json` (+4 specs),
  `data/registries/mechanism_ontology.json` (+4 nodes),
  `src/catalytic_earth/external_cofactor_ec_disambiguation.py` (metal evidence + 4 rules),
  `src/catalytic_earth/external_annotation_anchored_import.py` (lane maps),
  `src/catalytic_earth/coverage_redundancy_audit.py` (signatures).
- `artifacts/v3_stage2_hydrolase_subfamily_sourcing_preview_current702.json`,
  `work/stage2_hydrolase_subfamily_sourcing_current702.md`,
  `artifacts/v3_coverage_redundancy_audit_current702_20260611_stage2.json`.
- `data/registries/external_bronze_labels.json` (2340 -> 2940).

## 2026-06-11: ser_his Hole CLOSED — Cofactorless Triad Sourcing (Stage 1 complete)

Decision: built and ran the cofactorless `ser_his_acid_hydrolase` sourcing loop — the
last open Stage-1 hole, and the one the cofactor/EC engine structurally cannot reach.
New module `ser_his_hole_sourcing.py` + runner `scripts/source_ser_his_hole.py` wire
the `ser_his_triad_locator` acquisition contract into a live pipeline: fetch reviewed
serine-hydrolase Swiss-Prot rows (EC 3.4.21/3.4.16/3.1.1, ACT_SITE annotated, **no
cofactor**) → stage the **AlphaFoldDB v6** predicted coordinate → confirm the
Ser/Cys/Thr-His-Asp/Glu catalytic triad coincides (≥2 overlap) with the annotated
catalytic ACT_SITE → novelty gate → cap guard → preview/apply. Frozen current702
byte-unchanged (`sha256:5eec9bef…`; 702 labels).

Why this works where the cofactor engine cannot: ser_his is cofactorless, so there is
no cofactor to corroborate — the corroborator is the **coordinate triad** instead. And
AlphaFoldDB models are 1:1 with the UniProt sequence (UniProt numbering), so the
predicted residue numbers equal the annotated ACT_SITE positions; the triad is present
in the **apo** predicted structure (a protein triad, no ligand needed), which is
exactly why this fingerprint is apo-confirmable (unlike the cofactor families). This
also required structure egress (AFDB v6), which is open in this environment alongside
UniProt — so the loop is both buildable and runnable here, not just a contract.

Result: 180 reviewed rows over 3 EC lanes (0 fetch failures) → 159 AFDB coordinates
staged (0 unavailable) → **98 triad-confirmed** (held: 48 no-triad, 13
triad-resolved-but-uncorroborated, 5 dup/non-serine — conservative by design) → **87
novelty-admitted** (11 throttled) appended to the expansion registry (**2253 →
2340**; combined **2955 → 3042**). `ser_his_acid_hydrolase` **42 → 129** — HOLE
CLOSED, floor reached.

**Stage 1 is now complete.** The governor's hole list is **empty** (`holes: []`);
**all 8 fingerprints are at/above the 100-floor** (7 BALANCED, plus the one intentional
over-cap `metal_dependent_hydrolase` 308); fingerprint Gini **0.2608 → 0.1917**
(originally 0.51); next-batch floor deficit **0**. Seed positives 1259 → 1346. The only
remaining governor action is the metal over-cap, which is the **Stage-2** on-ramp (its
v2 split), not a sourcing target.

Honesty notes: the corroboration is the coordinate triad, **not** a cofactor — every
label records `cofactor_evidence_level=cofactorless_triad` and the triad confirmation
(triad residue ids + ACT_SITE overlap) on `structure_provenance`; the committed label
carries no transient staged path (the AFDB v6 coordinate is regeneratable from the
handle). The triad is confirmed on the AFDB **apo** predicted structure — honest as a
bronze entry gate; structure/geometry confirmation remains a deferred bronze→silver
signal for the cofactor families. EC stays scope-only (`excluded_context`), never
predictive. Held rows (no-triad / uncorroborated) are correct conservative behavior,
not a bug.

Validation: `validate` ok (702 frozen intact). Full suite green except the 6 known
env-backend failures (numpy/esm2/mmseqs); added 5 ser_his sourcing tests (offline,
synthetic CIF). Refreshed the RealRegistry pins (combined 2955→3042, expansion
2253→2340, seed_labels 1029→1116); updated the coverage-redundancy test (no holes
remain) and the triad-locator scan test (87 ser_his expansion rows). `git diff --check`
clean. Staged CIFs are written to a temp dir, never committed.

References:

- `src/catalytic_earth/ser_his_hole_sourcing.py`, `scripts/source_ser_his_hole.py`,
  `tests/test_ser_his_hole_sourcing.py`; primitive `ser_his_triad_locator.py`
  (`assess_ser_his_candidate`, `confirm_catalytic_triad`).
- `artifacts/v3_ser_his_hole_sourcing_preview_current702.json`,
  `work/ser_his_hole_sourcing_current702.md`.
- `data/registries/external_bronze_labels.json` (2253 → 2340).

## 2026-06-11: Stage-1 Under-Floor Closure — flavin/heme Fingerprints To Floor (+ runner cap guard)

Decision: finished Stage 1 in-env by sourcing the three **under-floor** cofactor
fingerprints to the 100-floor, via the same `scripts/stage1_source_holes.py` runner
(now generalized from the two holes to all five cofactor-defined Stage-1 fingerprints).
Frozen current702 byte-unchanged
(`sha256:5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; 702 labels).

Result: 602 reviewed Swiss-Prot rows over 8 narrow EC/cofactor lanes (0 fetch
failures) -> 390 disambiguated bronze (106 held no-cofactor-EC, 10 multi-signal) ->
**286 novelty-admitted** appended to the expansion registry (1967 -> 2253; combined
2669 -> 2955). Per-fingerprint combined:

- `flavin_monooxygenase`: **43 -> 116** (UNDER -> BALANCED).
- `heme_peroxidase_oxidase`: **69 -> 119** (UNDER -> BALANCED).
- `flavin_dehydrogenase_reductase`: **87 -> 250** (UNDER -> BALANCED, at the cap).

Governor: fingerprint Gini **0.3408 -> 0.2608** (originally 0.51); **7 of 8
fingerprints now at/above floor and BALANCED**; the only remaining hole is
`ser_his_acid_hydrolase` (42) and the only over-cap is `metal_dependent_hydrolase`
(308, untouched). Seed positives 973 -> 1259.

Cap guard (the load-bearing fix this batch): the novelty gate admits diverse rows
greedily above the floor and even permits `over_cap_but_new_reaction_chemistry`, so
the first under-floor preview pushed `flavin_dehydrogenase_reductase` to **253 —
over the 250 ceiling**. Stage 1 must close to the FLOOR, never manufacture an
over-cap fingerprint, so the runner now enforces a hard per-fingerprint cap guard
(`cap_ceiling=DEFAULT_CAP_CEILING=250`): each fingerprint's admitted set is trimmed
so projected combined never exceeds the cap; the surplus stays HELD (a review queue),
not imported. Re-run landed flavin_DR at exactly 250 (3 held at cap),
`no_fingerprint_pushed_over_cap=True`. Note flavin_DR is highly diverse (~0.5
labels/distinct-reaction), so filling it toward the cap is honest supply, not the
redundancy the cap guards against — and balance (Gini) **improved**, confirming it.

Guardrails (verified post-apply): frozen current702 never written; `tier=bronze`,
`review_status=automation_curated`; uniprot namespace; EC/name/prose in
`excluded_context`, `predictive_evidence` empty on all 286; deduped + novelty-gated
vs BOTH registries; multi-fingerprint-signal rows held.

Validation: `validate` ok (702 frozen intact). Full suite green except the 6 known
env-backend failures (numpy/esm2/mmseqs). RealRegistry count pins refreshed (combined
2669->2955, expansion 1967->2253, seed_labels 743->1029); new stage1 tests added
(under-floor routing + the SOURCEABLE_FINGERPRINTS coverage). `git diff --check` clean.

Stage 1 is now complete except `ser_his_acid_hydrolase` (the cofactorless hole),
which needs the live fetch + AF/PDB coordinate-staging + triad-confirm loop its
acquisition contract describes — not reachable by the cofactor/EC runner.

References:

- `src/catalytic_earth/stage1_hole_sourcing.py` (`UNDER_FLOOR_LANE_QUERIES`,
  `STAGE1_LANE_QUERIES`, `SOURCEABLE_FINGERPRINTS`, the cap guard),
  `scripts/stage1_source_holes.py`, `tests/test_stage1_hole_sourcing.py`.
- `artifacts/v3_stage1_underfloor_sourcing_preview_current702.json`,
  `work/stage1_underfloor_sourcing_current702.md`.
- `data/registries/external_bronze_labels.json` (1967 -> 2253).

## 2026-06-10: Stage-1 Hole Sourcing — radical_sam + cobalamin Holes Closed To Floor (+ cobalamin cofactor-name fix)

Decision: ran `docs/stage1_hole_sourcing_runbook.md` (Stage 1 of
`docs/scaling_plan_to_10k.md`) with live UniProt egress, sourcing the two
cofactor-defined holes to the 100-label floor. Verified egress (HTTP 200), previewed
non-destructively, reviewed, then applied the novelty-admitted bronze to the SEPARATE
expansion registry. The frozen current702 benchmark is byte-unchanged
(`sha256:5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; 702 labels).

Result: 548 reviewed Swiss-Prot rows fetched across 10 narrow EC/cofactor lanes (0
fetch failures) -> 259 disambiguated bronze (277 held for no cofactor+EC
corroboration, 12 dup-screened) -> **257 novelty-admitted** (2 throttled as
redundant). Expansion registry **1710 -> 1967**; combined **2412 -> 2669**.
Per-fingerprint combined (frozen + expansion):

- `radical_sam_enzyme`: **10 -> 133** (expansion 9 -> 132) — HOLE closed, floor reached.
- `cobalamin_radical_rearrangement`: **10 -> 144** (expansion 7 -> 141) — HOLE closed, floor reached.

The governor confirms both moved off the hole list: holes are now
`['ser_his_acid_hydrolase']` only (was [ser_his, radical_sam, cobalamin]); fingerprint
Gini **0.51 -> 0.3408**; `metal_dependent_hydrolase` stays the lone over-cap (added none).

Cobalamin cofactor-name fix (the load-bearing change): the first preview admitted
**0** cobalamin despite all 156 fetched rows carrying a genuine adenosylcobalamin
annotation AND a matching mutase/eliminase EC (5.4.99/5.4.3/4.2.1.28/30/4.3.1.7).
Root cause: UniProt records B12 cofactors with the cobalt oxidation state spelled
inline — `adenosylcob(III)alamin`, `cob(II)alamin`, `methylcob(III)alamin` — so the
substring `"cobalamin"` in `external_cofactor_ec_disambiguation.cofactor_evidence`
never matched the canonical names (this defeated the cobalamin half of the runbook,
not the documented conservative-hold caveat). Fix: also match the
`cob(i/ii/iii)alamin` stems. This is a scope-only read of reviewed cofactor
annotation; EC/name/prose stay in `excluded_context` and never become predictive
features — the leakage wall is unchanged. Re-preview then admitted 134 cobalamin.
Regression test added.

ser_his_acid_hydrolase (separate, cofactorless): ran `build-ser-his-triad-locator-scan`.
It is coordinate-confirmation-only and **network-free by design**, so live egress does
not change its outcome (its `blocked_http_403` note is a static string from the
blocked-network era, left untouched). With the local candidate pool drained it
confirmed **0** recoveries and the hole stays at **42** (combined). The acquisition
contract is ready; closing it needs the live fetch + AF/PDB coordinate-staging +
`assess_ser_his_candidate` triad-confirm loop the contract describes, which is not
wired into this CLI command.

Guardrails (all asserted on the preview and verified post-apply): frozen current702
never written; `tier=bronze`, `review_status=automation_curated`; uniprot namespace;
EC/name/prose in `excluded_context`, `predictive_evidence` empty on all 257; deduped
and novelty-gated vs BOTH registries; multi-fingerprint-signal rows held.

Validation: `validate` ok (702 frozen intact). Full suite green except the 6 known
env-backend failures (missing numpy/esm2/mmseqs). The 4 RealRegistry count pins were
updated to the new registry state (combined 2412->2669, expansion 1710->1967,
representation/promotion `seed_labels` 486->743). `git diff --check` clean.

References:

- `docs/stage1_hole_sourcing_runbook.md`; `scripts/stage1_source_holes.py`;
  `src/catalytic_earth/stage1_hole_sourcing.py`.
- `src/catalytic_earth/external_cofactor_ec_disambiguation.py` (cobalamin oxidation-state
  name match), `tests/test_external_cofactor_ec_disambiguation.py`.
- `artifacts/v3_stage1_hole_sourcing_preview_current702.json`,
  `work/stage1_hole_sourcing_current702.md`;
  `artifacts/v3_ser_his_triad_locator_scan_current702_20260610.json`.
- `data/registries/external_bronze_labels.json` (1710 -> 1967).

## 2026-06-10: Stage-1 Hole-Sourcing Runner — Fresh Bronze For The radical_sam + cobalamin Holes (non-destructive)

Decision: add a runnable Stage-1 (close-the-holes) sourcing path for the two
**cofactor-defined** holes the governor flags below the 100-label floor —
`radical_sam_enzyme` (combined 10) and `cobalamin_radical_rearrangement` (combined
10). New code is **orchestration only**; it chains the existing, tested pipeline and
introduces no new label logic:
`adapters.fetch_uniprot_query/entry` → `build_external_source_ingestion_pilot`
(hole-targeted EC/cofactor lane queries → canonical rows) →
`build_cofactor_ec_disambiguation` (cofactor+EC scope assignment, `_build_label`,
dedup vs BOTH registries, multi-fingerprint-signal rows held) →
`novelty_admission_gate.evaluate_batch` (admit only rows that add a new
cluster/reaction/organism) → non-destructive preview → (separate `--apply`)
`apply_external_annotation_anchored_import_to_registry`.

`ser_his_acid_hydrolase` is deliberately **excluded** from this runner: it is
cofactorless, so the cofactor/EC engine structurally cannot reach it (the runner
raises on it). It routes through the existing `build-ser-his-triad-locator-scan`
(triad locator + acquisition contract, confirmed against coordinates).

Integration fix found and corrected while wiring this: the ingestion pilot records
its current702 screen under `duplicate_current_registry_conflict`, but the
cofactor/EC re-screen reads the upstream verdict from `duplicate_status`. Without
re-keying, **every fresh pilot row is rejected as upstream-not-confirmed (0
imports)**. `_bridge_pilot_rows_for_disambiguation` re-exposes the pilot's own
verdict under the expected key; the authoritative accession/sequence re-check still
runs vs both registries.

Relationship to the 2026-06-09 pending-candidate inventory (scaling-plan §"Pending
candidate inventory"): the existing held pools already ran the disambiguation and
left **~730 held** for lacking unique cofactor+EC corroboration, plus a 275-row
"controlled_import_review_ready" set awaiting human approval. This runner does
**fresh, EC+cofactor-targeted** sourcing aimed at cleanly corroborated rows, and
routes through the **same** governor/novelty gate the inventory says to apply — so it
is complementary, not a re-source of the same drained lanes. Do not deepen paging on
drained lanes; split into new EC/keyword subqueries (the runner already does).

Guardrails (asserted on the output): frozen current702 benchmark never written
(expansion registry only); EC/name/prose stay `excluded_context`, never predictive;
`tier=bronze`, `review_status=automation_curated`; novelty-gated vs both registries;
non-destructive without `--apply`. **Live UniProt egress is required to run** (the
cloud sandbox 403s UniProt/Rhea/AlphaFold by default), so the actual fetch/apply
happens in a network-enabled session; the wiring is validated offline via injected
synthetic fetchers. CLI `validate` green (702 labels unchanged); new tests 8/8;
`git diff --check` clean; full suite unchanged (same 7 pre-existing env-backend
failures — torch/esm/mmseqs/numpy absent — none from this change). Merged to `main`
via PR #18.

References:

- `src/catalytic_earth/stage1_hole_sourcing.py` (`HOLE_LANE_QUERIES`,
  `build_stage1_hole_sourcing`, `_bridge_pilot_rows_for_disambiguation`),
  `scripts/stage1_source_holes.py` (runner + egress preflight + `--apply`),
  `tests/test_stage1_hole_sourcing.py`, `docs/stage1_hole_sourcing_runbook.md`.
- When run it writes a non-destructive preview under `artifacts/` and a report under
  `work/` (exact paths in the runbook); neither exists until a network-enabled run.
  **Update (this run):** that network-enabled run has now happened and applied —
  see the "Closed To Floor" entry above; the preview/report now exist.

## 2026-06-10: CORRECTION — Promotion Confirmability Is Cofactor PRESENCE, Not Experimental-vs-Predicted Provenance

Decision: correct the bronze->silver promotion preview's structure-confirmability
signal. The first version equated `coordinate_status ==
experimental_pdb_coordinate_provenance_available` with "holo / geometry
confirmation runnable" and reported **47 silver-ready**. That ignored the standing
Problem-2 degradation finding (already in this log): the deferred geometry
inverse-gate **abstains on apo coordinates** because the cofactor is missing
(predicted-apo: router 45/45 -> 23/45, 100% abstain), and the binding axis is
therefore **cofactor PRESENCE in the coordinates, not experimental-vs-predicted
provenance** — an experimental PDB can be apo too.

Empirical check that forced the correction: of the 104 coordinate-bearing seed
labels, **only 1 actually contains its annotated cofactor in the coordinates**
(Q8IV48 / MG); the other 103 are apo — including 51/52 of the "experimental" rows.
So the original 47 "silver-ready" were overwhelmingly apo structures the gate would
abstain on — the exact degradation the repo documented.

Fix: `structure_confirmability` now parses the coordinates and checks whether the
annotated cofactor's PDB HETATM comp id is present. `holo` = cofactor present (gate
meetable); `apo` = coordinates exist but cofactor absent (gate abstains; covers
experimental-apo AND predicted-apo — unified, as the degradation requires); `none`
= no coordinates. Corrected result on the 486 seed labels: **silver-ready 0**
(the one holo row, Q8IV48, has chemistry that disagrees with its label -> review),
blocked_apo_needs_cofactor_fusion 97 (was 50), blocked_pending_structure 295,
hold_low_chemistry_cohesion 67, review_chemistry_disagrees 27. The honest takeaway:
bronze->silver promotion is currently gated by apo cofactor-loss across the whole
coordinate-bearing set — which is exactly why the project deferred geometry
confirmation and adopted bronze tier; the lever is **cofactor fusion/restoration**
(restoration recovers 22/22 lost primaries, per the 2026-06-04 entry), not waiting
for more predicted structures. Non-destructive; full suite green except the 6 known
env-backend failures.

References:

- `src/catalytic_earth/bronze_silver_promotion_preview.py` (cofactor-presence
  confirmability), `tests/test_bronze_silver_promotion_preview.py`.
- `artifacts/v3_bronze_silver_promotion_preview_current702_20260610.json`,
  `work/bronze_silver_promotion_preview_current702_20260610.md`.

## 2026-06-10: Bronze->Silver Promotion Preview — The Queue, Not A Faked Confirmation

Decision: turn the representation loop's promotion triage into an explicit,
non-destructive bronze->silver promotion QUEUE. Every expansion label is bronze
because structure/cofactor-fused geometry confirmation was deferred to a
bronze->silver promotion signal (2026-06-09). This stages which labels are *ready*
for that confirmation — but is scrupulous about NOT faking it: the gating
`geometry_inverse_gate_confirmation` audit **abstains on predicted-apo coordinates**
(the cofactor is absent — the step-4 finding), so this preview does not run or
fabricate it and flips no tier.

Silver-ready is defined by signals that ARE checkable here, with the gating geometry
run kept explicitly separate: (1) **chemistry corroboration** — the representation
loop's cofactor/ligand chemistry independently agrees with the assigned fingerprint
(nearest centroid == assigned, cohesion >= 0.92); this is an INDEPENDENT axis from
the original annotation-anchored scope, so agreement is real corroboration and is
leakage-safe (chemistry only, never EC/name/label). (2) **structure confirmability**
— whether the geometry gate can even run: `holo` (experimental coordinates →
runnable), `apo_only` (AFDB predicted → gate abstains, needs cofactor fusion), or
`none`. ser_his is handled as the cofactorless special case (its structural
confirmation is the Ser-His-Asp triad, runnable on apo via the locator).

Result on the 486 expansion seed labels: **47 silver-ready** (chemistry-corroborated
+ holo structure where the confirmation can actually run — 43 metal + 4 PLP), 50
blocked_apo_needs_cofactor_fusion, 295 blocked_pending_structure (no coordinates), 67
hold_low_chemistry_cohesion, and **27 review_chemistry_disagrees** (chemistry points
at a different fingerprint — the QA queue to resolve before any promotion). The
47-row silver-ready queue is exactly the set to feed the geometry-confirmation run
when holo structures / backends are available (e.g. locally); the tier flip and that
confirmation run remain separate authorized steps. Non-destructive: no registry
written, no tier changed, gate neither run nor faked. Full suite green except the 6
known env-backend failures.

References:

- `src/catalytic_earth/bronze_silver_promotion_preview.py` (reuses
  `mechanism_representation_loop.assess_row_against_centroids` and
  `ser_his_triad_locator.assess_ser_his_candidate`),
  `tests/test_bronze_silver_promotion_preview.py`, CLI
  `build-bronze-silver-promotion-preview`.
- `artifacts/v3_bronze_silver_promotion_preview_current702_20260610.json`,
  `work/bronze_silver_promotion_preview_current702_20260610.md`.

## 2026-06-10: Mechanism Representation Loop — Leakage-Safe Self-Feeding Supply (Phase 3 start)

Decision: begin the self-feeding loop that eventually replaces hand-sourcing (the
hand pools are drained). We have been banking rich review-only `mechanism_evidence`
on every bronze label for exactly this. The first iteration learns a representation
that organises the bronze labels, triages bronze->silver promotion, and proposes
hole-filling candidates from our own out_of_scope pile — all WITHOUT network.

THE LEAKAGE WALL IS ABSOLUTE AND TEST-ENFORCED. The representation is built ONLY
from review-only **structural/chemical** evidence — cofactor + binding-ligand
chemical identities (ChEBI names) and active-site residue role counts. It never
reads `ec_numbers`, protein name / prose / curated text, `target_family_lane`, the
`fingerprint_id`/`label_type` target, or the frozen 702 benchmark. A unit test
mutates EC + protein-name + lane + fingerprint and asserts `featurize` is
byte-identical, proving none of them enter the representation. Cofactor/ligand
chemical identity is the legitimate deploy-available structural basis the eight
fingerprints are *defined* by — distinct from the excluded name/prose/EC fields.
This loop is for the expansion's self-organisation and promotion triage ONLY; it is
**never** a benchmark scorer and must not be used as one.

Feature space (12 dims): 9 cofactor classes (flavin, plp, heme, iron_sulfur, sam,
cobalamin, zinc, divalent_metal_other, calcium) dominating, plus 3 down-weighted
residue-role ratios (catalytic/binding fraction, log-scaled active-site size).

Results on the 486 expansion seed labels:

- **Leave-one-out self-consistency 0.895** — chemistry alone (no EC/name/label)
  recovers the assigned fingerprint 89.5% of the time, each row scored against
  centroids that exclude it. This is an honest coherence/QA read (the centroids
  encode the cofactor-corroboration assignment policy, so it measures internal
  coherence, not independent validation).
- **368 promotion candidates** (cohesion >= 0.92 with the assigned fingerprint) —
  bronze->silver promotion-ready pending the actual geometry gate.
- **51 review outliers** — rows whose chemistry points at a *different* fingerprint
  than their label (possible mislabels / genuinely ambiguous); the highest-value
  QA targets.
- **Hole proposals from out_of_scope:** 14 radical_sam_enzyme candidates, each
  sharing genuine `sam` or `iron_sulfur` chemistry with the radical-SAM centroid —
  model-proposed re-review candidates to help close that hole, network-free.
  cobalamin: 0 (no OOS cofactor overlap); ser_his: 0 (no expansion centroid — the
  known hole). Proposals REQUIRE non-empty cofactor-chemistry overlap with the
  target (a cofactor-less row is never proposed for a cofactor-defined
  fingerprint) AND the target must be the candidate's nearest centroid.

How it composes with the climb: the representation triages what the engine already
imported (promotion vs review) and proposes what to source/predict next for the
holes, feeding Phase 1; the novelty gate then governs admission of whatever is
sourced. Non-destructive: writes no registry, emits no label, never touches the
benchmark. Full suite green except the 6 known env-backend failures.

References:

- `src/catalytic_earth/mechanism_representation_loop.py`,
  `tests/test_mechanism_representation_loop.py`, CLI
  `build-mechanism-representation-loop`.
- `artifacts/v3_mechanism_representation_loop_current702_20260610.json`,
  `work/mechanism_representation_loop_current702_20260610.md`.

## 2026-06-10: Novelty / Saturation Admission Gate — The Governor Becomes An Online Filter

Decision: promote the 2026-06-10 governor from a *report* into the *gate* it
implies. We had deduped only on EXACT accession/sequence-SHA, so near-duplicate
orthologs and saturated lanes flowed straight in. This installs a non-destructive,
online novelty filter that sits AFTER the exact-dedup screen and admits an incoming
candidate only when it adds genuine diversity. It is ready to govern the next
sourced batch so volume grows diversely instead of re-saturating the flagged lanes.

Mechanism (module `novelty_admission_gate.py`, CLI
`build-novelty-admission-gate-audit`): reuses the governor's cluster key
`(fingerprint_or_scope, full_EC, organism, sequence_length_bin)` (single source of
truth — the field extractors are imported from `coverage_redundancy_audit`) plus
reaction-id novelty, folded into the balance policy:

- HOLE / under-floor fingerprints → **admit** greedily (we need their volume),
  unless the row is a pure redundant ortholog (cluster already at the per-cluster
  cap of 3, no new reaction/organism) → throttle.
- Over-cap fingerprints → **reject** unless the row brings a genuinely new reaction
  (new chemistry).
- Balanced seed / out_of_scope → **admit only on novelty** (new cluster, reaction,
  or organism); throttle saturated clusters.

It operates on registry-shaped label dicts — exactly what an engine preview's
`applied_labels` are — so it plugs directly into the existing apply path: run a
preview's `applied_labels` through `evaluate_batch` against
`build_diversity_state(frozen, expansion)`, then apply only the ADMIT set via
`apply-external-annotation-anchored-import`. `evaluate_batch` updates state as it
admits, so within-batch duplicates also gate, and it evaluates hole/under-floor
candidates first so scarce-fingerprint volume is admitted before the per-cluster
budget is spent on common lanes.

Retrospective self-audit (existing 1,710 expansion replayed through the gate,
seeded with the frozen benchmark only): **456 rows (26.7%) would NOT be re-admitted**
— 409 throttled (redundant orthologs / no novelty), 47 rejected (over-cap metal
with no new chemistry). The non-admit is concentrated exactly where the governor
predicted: out_of_scope (373) and metal_dependent_hydrolase (71). This both
validates the gate on real data and quantifies the baked-in redundancy we now stop
adding to. Non-destructive: nothing is removed; the gate is advisory and the
authorized apply step is what writes. Full suite green except the 6 known
env-backend failures.

References:

- `src/catalytic_earth/novelty_admission_gate.py`,
  `tests/test_novelty_admission_gate.py`, CLI `build-novelty-admission-gate-audit`.
- `artifacts/v3_novelty_admission_gate_audit_current702_20260610.json`,
  `work/novelty_admission_gate_audit_current702_20260610.md`.

## 2026-06-10: Ser/Cys-His-Asp Triad Locator — The Corroborator That Unblocks The Cofactorless ser_his Hole

Decision: supply the missing structural corroborator for `ser_his_acid_hydrolase`,
the one seed fingerprint the annotation-anchored engine **structurally cannot
reach**. The engine's positive policy is "annotation-derived lane corroborated by
the matching **cofactor** class" — but serine hydrolases are **cofactorless**, so
that rule can never fire, which is exactly why the 2026-06-10 governor found
ser_his as the sharpest HOLE (42 frozen, **0 expansion**). This resolves the open
2026-06-03 design item (a source-free catalytic-triad geometric locator for serine
hydrolases). Non-destructive: no registry written, no label emitted.

The corroborator: for a cofactorless serine hydrolase, catalysis is the
Ser/Cys/Thr-His-Asp/Glu charge-relay triad, readable from coordinates alone. The
geometry primitive already existed (`serine_active_site.extract_source_free_ser_his_acid_triad`),
but **raw geometric triad resolution is not specific** — the control panel measured
it firing on **31/120 (≈26%)** of arbitrary local structures (incidental
Ser/His/acid proximities). Precision comes from corroboration: the geometric triad
must coincide with the **annotated catalytic ACT_SITE residues** (≥2 overlap) of a
**serine-hydrolase EC family** (3.4.21/3.4.16/3.1.1, explicitly excluding the
3.1.11/3.1.13/3.1.16 nucleases that share the 3.1.1 text), with **no catalytic
cofactor** annotated. EC is used for **scope assignment only** (excluded_context,
never predictive); triad confirmation consumes coordinates only. This is the
cofactorless analogue of the engine's cofactor corroboration.

Recovery scan over the registries: 13 serine-hydrolase-EC rows exist in the
expansion, and **all 13 correctly HELD** — 9 carry a catalytic cofactor (so they
are not cofactorless triad hydrolases), 1 lacks staged coordinates, the rest
uncorroborated — **0 false positives, 0 confirmed recoveries**. That is the honest
result: there is no clean cofactorless serine-triad supply locally.

Why a ready-to-run **acquisition contract** and not filled labels: in this
environment the hand-curated pools are drained, UniProt is network-blocked (HTTP
403), and the registries carry no clean local serine-hydrolase-triad rows — so the
hole genuinely cannot be filled here. The deliverable mirrors the project's
established staged-contract pattern (ESMFold2 contract, banked Lever-2 locators):
the engine plus a precise contract (EC families, no-cofactor, triad-confirm-against-
ACT_SITE, dedup vs BOTH registries, bronze/automation_curated; deficit 58 to the
governor's 100 floor) that fills ser_his the moment network/sourcing is authorized.
Full suite green except the 6 known env-backend failures.

References:

- `src/catalytic_earth/ser_his_triad_locator.py` (reuses
  `serine_active_site.extract_source_free_ser_his_acid_triad`),
  `tests/test_ser_his_triad_locator.py`, CLI `build-ser-his-triad-locator-scan`.
- `artifacts/v3_ser_his_triad_locator_scan_current702_20260610.json`,
  `work/ser_his_triad_locator_scan_current702_20260610.md`.

## 2026-06-10: Coverage/Redundancy Governor — Balance-Capped Acquisition Policy For The Climb

Decision: before scaling expansion *volume* 4x, install a non-destructive
diversity/coverage governor. The constraint has shifted from "can we accept
candidates" (solved) to "diverse, non-redundant supply + honest quality." We had
deduped only on EXACT accession/sequence-SHA; we had never measured near-duplicate
redundancy or class balance of the 1,710. This entry records the measurement and
the policy it implies. **No registry was written** — the audit emits a reporting
artifact only, so the real distribution can be inspected before the next batch is
fed.

What was built (module `coverage_redundancy_audit.py`, CLI
`build-coverage-redundancy-audit`; metadata-only — no network/mmseqs/embeddings):
an audit of all **2,412** combined labels (702 frozen + 1,710 expansion) by
fingerprint × lane × organism × EC-class × sequence-length, with (a) class-imbalance
flags, (b) a metadata-only redundancy/saturation read, and (c) a prioritized,
balance-capped acquisition target list. EC/lane/organism are coverage-accounting
metadata only and are never emitted as predictive features (the module emits no
labels at all); the frozen 702 benchmark is read-only.

Headline findings:

- **Class balance is skewed.** Seed positives 716 vs out_of_scope 1,696
  (positive:OOS = 0.42); fingerprint Gini 0.51 / normalized entropy 0.78; the
  largest fingerprint (metal_dependent_hydrolase, 308) outweighs the smallest
  non-zero (radical_sam / cobalamin, 10 each) **30.8×**.
- **Holes (sharpest priority):** `ser_his_acid_hydrolase` (42 frozen, **0 in
  expansion** — still the one fingerprint the expansion never reaches),
  `radical_sam_enzyme` (10), `cobalamin_radical_rearrangement` (10). Under the
  100-label floor too: `flavin_monooxygenase` (43), `heme_peroxidase_oxidase` (69),
  `flavin_dehydrogenase_reductase` (87).
- **Over-cap:** `metal_dependent_hydrolase` (308, 58 over the 250 ceiling) — and it
  is the *most redundant* (2.96 labels per distinct reaction). `plp_dependent_enzyme`
  (147) is the only BALANCED in-scope fingerprint.
- **Redundancy is real but bounded:** 254 of 1,558 metadata-measurable rows (16.3%)
  fall in near-duplicate ortholog clusters keyed on
  `(fingerprint/scope, full-EC, organism, sequence-length bin)`. The biggest are
  OOS human kinases (EC 2.7.11.1) and Arabidopsis heme peroxidases (EC 1.11.1.7) —
  i.e. the broad OOS lanes (kinase/phosphatase/glycoside) are saturated.

Policy for the rest of the climb (drives more-sourcing OR a self-feeding model
loop): **close holes first, raise under-floor fingerprints to the 100 floor
(next-batch positive deficit ≈ 339), cap/pause + dedup the over-supplied
metal-hydrolase, and pause broad OOS draining until positive holes close** — the
binding constraint is diverse positive supply, not raw count. Per-fingerprint
sourcing hints (EC prefixes + cofactor + lanes, mirroring the 2026-06-09
disambiguation rules) are emitted for the three holes (notably ser_his: EC
3.4.21/3.1.1/3.5.1, Ser/Cys-His-Asp triad, no cofactor — which the cofactor-anchored
engine structurally cannot source, so it needs a triad-geometry route).

The floor/cap (100/250) and hole threshold (25) are explicit, overridable policy
params, not tuned constants. Full suite green except the 6 known env-backend
failures.

References:

- `src/catalytic_earth/coverage_redundancy_audit.py`,
  `tests/test_coverage_redundancy_audit.py`, CLI `build-coverage-redundancy-audit`.
- `artifacts/v3_coverage_redundancy_audit_current702_20260610.json`,
  `work/coverage_redundancy_audit_current702_20260610.md`.

## 2026-06-09: Cofactor/EC Disambiguation Makes Held Redox + Radical-SAM/Cobalamin Countable (2269 -> 2412)

Decision: the held cofactor-confounded redox and secondary-probe
radical-SAM/cobalamin rows are made countable where — and only where — an annotated
cofactor and a uniquely matching reviewed reaction/EC class agree. This adds **143
seed_fingerprint bronze labels**; combined total **702 frozen + 1,710 expansion =
2,412** (was 2,269). The frozen current702 benchmark is byte-unchanged.

Why this is not a guess (the held lanes' standing guardrail): scope is still decided
ONLY from reviewed Swiss-Prot/EC/Rhea/cofactor annotation, and **EC is used for the
scope assignment only — it stays in `excluded_context` and is NEVER a predictive
feature** (the benchmark scorer never sees it). A row is assigned a fingerprint only
when exactly one cofactor+EC rule fires; rows that match two fingerprints' rules
(7) or none (723) stay held. Each rule is the textbook cofactor + EC-class signature
of one fingerprint:

- `heme_peroxidase_oxidase` — heme + EC 1.11.1 (peroxidase).
- `flavin_monooxygenase` — flavin (FAD/FMN), no heme + EC 1.14.13/1.14.14.
- `flavin_dehydrogenase_reductase` — flavin, no heme + EC 1.3 / 1.6 / 1.8.1
  (hydride/electron transfer, no oxygen insertion).
- `radical_sam_enzyme` — CX3CX2C motif, or [4Fe-4S] + SAM both annotated.
- `cobalamin_radical_rearrangement` — adenosylcobalamin/B12 + mutase/eliminase EC
  (5.4.99 / 5.4.3 / 4.2.1.28/30 / 4.3.1.7).

Recovered (143): 49 heme_peroxidase_oxidase + 41 flavin_monooxygenase + 39
flavin_dehydrogenase_reductase + 9 radical_sam_enzyme + 7 cobalamin_radical_
rearrangement. The cofactor/EC evidence overrides the shard's coarse lane bucket
(e.g. flavin-redox-boundary rows split into monooxygenase vs dehydrogenase by EC;
"heme peroxidase/oxidase-like" rows that actually carry flavin + a dehydrogenase EC
are routed to the flavin reductase fingerprint). The two flavin-redox-boundary
accessions already imported by the scale-out batch are correctly deduped out. With
this, the expansion registry now represents **7 of the 8 fingerprints** (only
ser_his_acid_hydrolase remains absent — not present in these pools). Rows lacking
clean corroboration (Cu/Mo oxidases, dioxygenases, SOD, etc. — outside the eight
fingerprints, or ambiguous) stay a review queue. Cumulative expansion: 486
seed_fingerprint (225 metal + 116 PLP + 49 heme + 41 flavin-mono + 39 flavin-DR + 9
radical-SAM + 7 cobalamin) + 1,224 out_of_scope. Full suite green except the 6 known
env-backend failures.

References:

- `src/catalytic_earth/external_cofactor_ec_disambiguation.py`,
  `tests/test_external_cofactor_ec_disambiguation.py`, CLI
  `build-external-cofactor-ec-disambiguation`.
- `artifacts/v3_external_cofactor_ec_disambiguation_preview_current702_20260609.json`,
  `work/external_cofactor_ec_disambiguation_preview_current702_20260609.md`.
- `data/registries/external_bronze_labels.json` (expansion registry, now 1,710 bronze).

## 2026-06-09: Scale-Out Drain Of The Annotation-Anchored Engine (888 -> 2269 combined)

Decision: drain the already-materialized import-ready candidate pools through the SAME
conservative annotation-anchored engine, adding **1,381 bronze expansion labels** (no new
sourcing, no env-blocked deps). Combined total **702 frozen + 1,567 expansion = 2,269**
(was 888). The frozen current702 benchmark registry, its coherence-audit baseline, and its
eval-contract SHA-256 are byte-unchanged (regression tests green).

What was drained and how (module `external_scaleout_bronze_import.py`, CLI
`build-external-scaleout-bronze-import`; applied via the existing
`apply-external-annotation-anchored-import` writer):

- **The 324 Wave 2 skipped rows** had been held ONLY because their current702
  accession/sequence duplicate screen was never promoted to the top-level field the engine
  reads. Their screen was re-run and independently re-verified — accession overlap re-checked
  against BOTH registries + current702, sequence-SHA overlap re-checked against current702
  where the precomputed digest was present, and the upstream current702 sequence screen
  required to read clear. All 324 cleared (0 registry/sequence collisions). Through the engine
  they yield 131 labels (4 seed: 2 flavin + 1 metal + 1 PLP; 127 OOS), 193 held.
- **Four shard pools** classified by the same policy over an extended lane vocabulary
  (additive, frozen engine untouched): metal_phosphoryl_glycoside (1,049) -> 1,006 import
  (129 metal seed + 877 OOS), 43 held (no metal corroboration); plp_radical_cobalamin (168)
  -> 110 PLP seed (specific PLP catalytic lanes corroborated by reviewed
  `cofactor_family_flags.plp_evidence_present`), 58 held (radical-SAM/cobalamin + broad PLP
  context); near_orphan_diversity (142) -> 142 OOS (terpene/isomerase/transferase/lyase tail);
  **redox_cofactor_confounded (743) -> 0 import, fully HELD** (cofactor-confounded redox; the
  ~64 flavin-redox-boundary + radical lanes are exactly the rows the optional cofactor/EC
  disambiguation task is meant to make countable later).

New labels by lane diversity (1,381 = 242 seed + 1,139 OOS): seed = 130
metal_dependent_hydrolase + 110 plp_dependent_enzyme + 2 flavin_dehydrogenase_reductase; OOS
spans phosphoryl transfer/phosphatase (396), kinase (225), glycoside/nucleoside (296),
dehydratase/hydratase (37), terpene synthase/lyase (49), isomerase/racemase (30), C-C
lyase/decarboxylase (12), transferase tail (9), and the near-orphan tail. Cumulative
expansion registry: 343 seed_fingerprint (225 metal + 116 PLP + 2 flavin) + 1,224 out_of_scope.

Guardrails carried forward verbatim: predictive leakage discipline absolute (EC/name/prose in
`excluded_context`, `predictive_evidence` empty, scorer never sees them); positives only on an
annotation-derived primary lane corroborated by the matching cofactor class; clear OOS only
for non-eight-fingerprint lanes; HOLD cofactor-confounded redox and secondary-probe
radical-SAM/cobalamin; every label tier=bronze / review_status=automation_curated / uniprot
namespace with rich review-only `mechanism_evidence`; deduped against BOTH registries and
schema-validated; frozen 702 benchmark + split/heldout never touched. Full suite green except
the 6 known env-backend failures.

References:

- `src/catalytic_earth/external_scaleout_bronze_import.py`,
  `tests/test_external_scaleout_bronze_import.py`, CLI
  `build-external-scaleout-bronze-import`.
- `artifacts/v3_external_scaleout_bronze_import_preview_current702_20260609.json`,
  `work/external_scaleout_bronze_import_preview_current702_20260609.md`.
- `data/registries/external_bronze_labels.json` (expansion registry, now 1,567 bronze labels).

## 2026-06-09: Annotation-Anchored Bronze Is An Accepted External Label Basis (the 10k unlock)

Decision (owner: Vivek): to scale toward 10k labels, **reviewed Swiss-Prot/EC/Rhea/cofactor
annotation is an accepted bronze label source.** Scope/fingerprint may be decided from
reviewed annotation; structure/geometry confirmation is demoted from an entry gate to a
deferred **bronze->silver promotion** signal.

Why this was the real blocker (not ceremony): scoring the 276 coordinate-bearing Wave 2
rows through the project's own text-free geometry inverse-gate abstained on **100%** of them
— the AlphaFold **apo** coordinates lack the cofactor, the same predicted-apo degradation the
step-4 work characterized. So "scope must be geometry-confirmed" is unmeetable on predicted
structures and produced zero counted labels from thousands of candidates. The fix separates
the two things the old bar conflated: (1) **predictive leakage discipline** — the benchmark
scorer must never see EC/name/prose — stays ABSOLUTE; (2) **label evidence basis** — adopt the
field-standard reviewed annotation, recorded transparently as `evidence_basis` + bronze tier.

**Frozen benchmark stays clean — expansion labels live in a SEPARATE registry.** The
current702 `curated_mechanism_labels.json` IS the frozen evaluation benchmark: its label
count, the `mechanism_fingerprint_v1_coherence_audit_702` baseline, and the
`mechanism_prediction_oos_and_diversity_eval_contract_702` SHA-256 are deliberately pinned
(regression tests enforce all three). Expansion bronze labels are therefore written to
`data/registries/external_bronze_labels.json`, NOT the benchmark. Total label count =
frozen benchmark (702) + expansion; the benchmark and its contracts are byte-unchanged.

Load-bearing gates kept: leakage-safe split (expansion uniprot rows are NOT in the frozen
702 split — heldout untouched), current702 accession/sequence duplicate screen (deduped
against BOTH registries), EC/name/prose in `excluded_context` (never predictive), honest
bronze/automation_curated tiering, and per-lane diversity. Conservative scope policy:
positives only when an annotation-derived primary lane is corroborated by the matching
cofactor class (metal/PLP/flavin); clear OOS for non-eight-fingerprint lanes; **hold**
cofactor-confounded redox and secondary-probe radical-SAM/cobalamin lanes for review. The
external out_of_scope evidence validator (`labels.py`) now accepts the annotation basis with
empty `predictive_evidence` (geometry confirmation deferred), keeping the leakage separation.

First batch (applied to the expansion registry): 186 bronze labels (101 seed_fingerprint =
95 metal_dependent_hydrolase + 6 plp_dependent_enzyme; 85 out_of_scope) -> combined total
**702 + 186 = 888**; 90 held, 324 skipped (current702 duplicate screen not yet confirmed —
the next batch). Each label carries rich review-only `mechanism_evidence` (Rhea reaction
equations, active-site catalytic/binding residues with ligand ChEBI ids, cofactor identities,
EC) for future representation learning — provenance only, never predictive.

References:

- `src/catalytic_earth/external_annotation_anchored_import.py`,
  `tests/test_external_annotation_anchored_import.py`, CLI
  `build-external-annotation-anchored-import` + `apply-external-annotation-anchored-import`.
- `data/registries/external_bronze_labels.json` (expansion registry, 186 bronze labels).
- `artifacts/v3_external_annotation_anchored_import_preview_wave2_current702_20260609.json`,
  `work/external_annotation_anchored_import_preview_wave2_current702_20260609.md`.

## 2026-06-09: Step-4 Precision Side Measured — Recalibrated-Threshold Dial Beats Suppression (leakage-safe)

Decision: the Problem-2 step-4 operating-point question now has its missing
*precision* side measured on a leakage-safe train/cal surface, and on that surface
the **recalibrated-abstention-threshold dial dominates the sequence-supported
suppression dial**. This is a research diagnostic; it changes no production
threshold and reads no heldout row.

Why this was the open gate: the confirmed heldout one-shot (23 -> 37/45 primary)
came with a precision cost (OOS/sec FP 12.3% -> 25.9%), but that read is SPENT.
The in-distribution recovery harness measured the recall side leakage-safe yet had
**no OOS rows**, so the precision cost was unmeasured on any reusable surface. New
module `cofactor_fusion_operating_point.py` (CLI
`build-cofactor-fusion-operating-point`) scores the in-distribution **OOS** rows of
the train/cal split through the SAME frozen cofactor-fusion router and counts every
non-abstained primary call as a false positive, so both dials compare on one
out-of-sample surface.

Result (calibration = out-of-sample for the channel; in-scope 35, OOS 26 scored;
predicted-apo coordinates from train/cal-safe staged bundles only, heldout bundles
excluded):

- apo baseline: recall 17/35 (0.486), OOS FP 9/26 (0.346).
- raw fusion @ frozen 0.4115: recall **30/35** (0.857), OOS FP 9/26 (0.346)
  — fusion buys +13 in-scope recall; the precision cost shows on the larger train
  surface (FP 0.402 -> 0.480) and is small on the thin 26-row cal OOS set.
- **recalibrated threshold @ 0.44**: recall **30/35** (no loss), OOS FP **8/26**
  (0.308) — reaches the suppression dial's precision for free.
- suppression dial @ 0.4115: recall **23/35** (0.657), OOS FP 8/26 (0.308) — same
  precision as the 0.44 threshold but at the cost of **7 in-scope primaries**.

Decision/consequence: prefer the recalibrated abstention threshold over the
suppression dial as the default precision lever; the suppression dial sacrifices
recall for precision a small threshold bump achieves at no recall cost. Layer the
complementary **Lever-2 electron-flow** OOS lift (+0.04 abstain-recall at primary
retention 1.0, measured on the geometry/fold gate — a *different* surface, not
merged here). Caveats kept front and center: the cal OOS surface is thin (26 rows,
1 row = 0.038), coordinate coverage is partial (128/342 OOS rows have staged
predicted-apo CIFs; gaps are NOT true negatives), and selecting a *deployable*
operating point is still a separately authorized decision that must not be tuned
against the spent heldout one-shot.

References:

- `src/catalytic_earth/cofactor_fusion_operating_point.py`,
  `tests/test_cofactor_fusion_operating_point.py`, CLI
  `build-cofactor-fusion-operating-point`.
- `artifacts/v3_cofactor_fusion_operating_point_train_cal_oos_current702_20260609.json`,
  `work/cofactor_fusion_operating_point_train_cal_oos_current702_20260609.md`.

## 2026-06-06: Branch Consolidation Complete — `main` Is The Single Source Of Truth

Decision: unify every research track into `main` and stop maintaining parallel branches.

State: PRs #4 (cofactor-presence-channel), #5 (youthful-babbage Problem-2 diagnosis), and
#6 (lever-2 electron-flow, incl. trailing sensitivity + approved-sidecar-import commits) are
merged; earlier branches (representation shootout esm-c / esm2-150m / prott5 / prostt5-3di /
saprot / foldseek-pocket, `automation/lomo-frozen-snapshot`, organic-cofactor-resolution,
targeted-bin-expansion, peaceful-mayer, happy-ride, Lever-2 PRs #2/#3) were already in main.
Verified exhaustively (2026-06-06): only `main` is a live remote branch, and every other
local branch / worktree HEAD is an ancestor of main — nothing dangling, nothing lost.

Consequence: develop on `main` (or short-lived isolated worktrees that PR back). `work/handoff.md`
is an auto-generated ledger; `docs/project_state.md` + `docs/session_decision_record_*` are the
durable human handoff. The 5 ePK tracks are the only unmerged work, archived as tags (next entry).

## 2026-06-06: ePK Family Expansion Is NO-GO — Archived As Recoverable Tags (learnings retained)

Decision: do NOT merge the 5 ePK (eukaryotic protein kinase) research tracks into main; archive
them as recoverable tags and retain their learnings by reference.

Rationale: ePK expansion is a NO-GO for heuristic geometry
(`docs/epk_heuristic_geometry_no_go_20260521.md`). The tracks forked 2026-05-20 (~455 commits
behind) and are concluded; merging concluded dead-ends would add noise, not capability. Their
conclusions are already in main (the NO-GO doc + refs in `external_source_transfer.md`,
`label_factory.md`).

Retained learnings (in the archive tags only, under `artifacts/research_lanes/epk_*`):
candidate-conflict decision, false-negative state-topology probe, source-free adjudication
requirement, terminal blocker-class decisions. Tags: `archive/epk-false-positive-hunter`,
`archive/epk-policy-harness`, `archive/epk-positive-evidence`, `archive/epk-sibling-controls`,
`archive/epk-substrate-role-identity`. Restore with `git checkout archive/epk-<track>` only if
ePK is revisited with a non-heuristic-geometry approach.

## 2026-06-06: Lever 2 Electron-Flow Adds A Real, Primary-Safe OOS-Abstain Lift (research-grade) — Integrated

Event: the Lever-2 electron-flow research track (formerly `lever-2-research-track`,
now in main; also preserved at tag `archive/lever-2-research-track`) is unified into
main. Earlier I mis-archived it as a concluded dead-end; it had in fact made real,
recent (2026-06-06), leakage-safe train/cal progress that was never written to this
log. This entry records that finding.

Result (train/cal, source-free, fixed operating point vs the current geometry/fold
surface; `lever2_mechanism_incremental_readout.py` +
`build-lever2-*` CLI): a direct electron-flow OR overlay raises OOS abstain-recall
0.4667 -> 0.5067 (**+0.04**) while holding **primary retention at 1.0**. Three
independent components each add value: PQQ (`m_csa:104`), NAD-family (`m_csa:464`),
Fe-S/iron (`m_csa:119`). Status: research-grade, **not deployable** — the only
remaining gap is explicit protected-import authorization + an approved-sidecar
rerun; no heldout was scored, no thresholds/labels/registries changed.

Why it matters / how it composes: this is the **complement** to the cofactor
channel. The cofactor one-shot (entry below) recovers primaries 23 -> 37/45 but at a
precision cost (OOS FP 12.3% -> 25.9%); electron-flow adds OOS-abstention WITHOUT
costing primary retention. It is exactly the kind of orthogonal, mechanism-
discriminative feature the 2026-05-31 Northstar Pivot called for, and a candidate
precision lever to offset the cofactor channel's over-opening. Treat it as a
research signal pending its authorized import, not a deployed gate.

References:

- `src/catalytic_earth/lever2_mechanism_incremental_readout.py`
- `work/lever2_source_free_electron_flow_current_split_operating_point_readout_current702_20260606.md`
- tag `archive/lever-2-research-track` (full track history)

## 2026-06-04: HELDOUT ONE-SHOT SPENT — Cofactor Fusion 23 -> 37/45 Primary (OOS FP 12.3% -> 25.9%)

Event: the one-shot heldout read was authorized as a single blind pass and is now
spent. The FROZEN leakage-safe cofactor-presence channel (heads fit on train,
thresholds/backend on calibration) was applied to heldout via raw cofactor fusion
at the frozen router threshold 0.4115. Per the authorization, **nothing was
refit, retuned, or changed in response to the result.**

Result (canonical 45-primary mask):
- Baseline predicted-apo (no channel): 23/45 primary, 17 abstained, 5 wrong,
  OOS/sec FP 0.1235 -- reproduces the known baseline exactly.
- Raw cofactor fusion (frozen channel): 37/45 primary, 2 abstained, 6 wrong,
  OOS/sec FP 0.2593.
- Net: +14 primaries recovered (14 of the 22 apo-lost = 63.6%), abstentions
  17 -> 2, at a precision cost of roughly doubled OOS/secondary false positives
  and +1 wrong primary.

Interpretation: the leakage-safe development methodology held -- the out-of-sample
calibration recovery (70.6%) accurately predicted heldout (63.6%); the projected
~38/45 landed at 37/45. The in-distribution out-of-sample surface was a faithful
proxy. Raw fusion buys large primary recovery at a genuine precision cost (OOS
over-opening) that the in-distribution surface could not measure (no OOS rows
there).

Discipline / consequence: this is a RECORDED result only. The one-shot is spent;
do not re-run it or tune any threshold/policy against it. Any operating point that
trades recovery for precision (the pre-built sequence-supported suppression dial,
or a recalibrated abstention threshold) is a SEPARATE decision requiring its own
separately authorized evaluation -- it must not be selected by peeking at this
result.

References:

- `artifacts/v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json`
- `work/heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.md`

## 2026-06-04: Cofactor Recovery Is Channel-Recall-Limited; Hard Misses Are Not Sequence-Recoverable

Decision: the in-distribution cofactor recovery (12/17 apo-lost primaries, 70.6%
out-of-sample) is at a presence-channel ceiling. The remaining 5 misses are not
recoverable by channel tuning; the next lever for them is cofactor localization
or transplant, not more presence-channel work.

Rationale (diagnosis of the 5 unrecovered calibration rows): all 5 are
channel-misses, not geometry-floor. The geometry put each near the 0.4115
threshold, but the channel failed to supply the right cofactor:
- m_csa:120 (flavin): flavin head 0.12 / 0.01 across backends; no Rossmann motif.
- m_csa:181 (metal): metal head 0.57 (< 0.86 threshold); apo score 0.3974, a hair
  under threshold -- the only threshold-fixable row, but lowering the metal
  threshold amplifies the spurious metal calls below.
- m_csa:274 / m_csa:275 (flavin): flavin head ~0.05-0.10, metal head 0.99 (wrong);
  pure single-cofactor rows, so the metal prediction is a false positive.
- m_csa:935 (heme): heme head 0.04, metal head 0.99 (wrong) -> harmful, boosted a
  wrong metal_dependent_hydrolase call. b-type peroxidase, so no c-type CxxCH motif.
The flavin/heme heads score true-flavin/heme rows near zero, and the larger ESM-2
model does not fix it. These enzymes' sequences do not look like cofactor binders
to ESM-2 or to motifs.

Result: added leakage-safe cofactor-binding sequence-motif features (Rossmann
G.G..G, c-type heme C..CH, zinc-hydrolase HE..H / close His pair) appended to the
embedding before fitting (opt-in `--use-motif-features`, baseline artifact
unchanged). Motifs improved channel calibration AUC -- heme 0.88 -> 0.93, flavin
0.9263 -> 0.9355 -- with zero regressions, but in-distribution recovery is
unchanged at 12/17: the motif-augmented flavin/heme scores for the hard rows
stayed ~0.10 (e.g. m_csa:274 flavin 0.054 -> 0.101), far below any non-degenerate
threshold. The motif channel is therefore a better-ranked channel to carry to the
eventual heldout one-shot, but it does not move this surface's recovery count.

Consequence / next gate: do not chase the 5 hard misses with more presence-channel
tuning. The genuinely different levers are (a) cofactor **localization** (predict
the binding residues so geometry is evaluated with the cofactor's position) and
(b) cofactor **transplant** (graft a sequence/fold-found holo template's cofactor
onto the predicted backbone; numpy is available). The metal head (cal AUC ~0.77,
spurious 0.99 on flavin/heme rows) is the systemic weak point and the main driver
of OOS over-opening risk, so improving it is the highest-leverage channel work.

References:

- `artifacts/v3_cofactor_presence_calibration_motif_current702_20260604.json`
- `artifacts/v3_in_distribution_predicted_geometry_recovery_motif_current702_20260604.json`
- `work/cofactor_presence_calibration_motif_current702_20260604.md`
- `work/in_distribution_predicted_geometry_recovery_motif_current702_20260604.md`

## 2026-06-04: Cofactor Channel Recovers ~70% of the Apo Drop (in-distribution, out-of-sample)

Decision: the sequence cofactor-presence channel is the right lever for the
predicted-apo primary drop, validated leakage-safe on in-distribution rows
before any heldout read is spent.

Rationale: the headline 45/45 -> predicted 23/45 drop is a heldout number and
the heldout read is one-shot. The new in-distribution recovery harness
reproduces the same question on in-distribution rows, which are never the
benchmark. The router classifies active-site geometry against the eight
mechanism fingerprint templates (no per-row self-match), so the
experimental-minus-apo and fused-minus-apo deltas are meaningful. The cofactor
channel was fit on the train split, so the headline is reported on the
calibration rows (out-of-sample for the channel); train is an in-sample
reference only.

Result (calibration, out-of-sample, 35 rows, threshold 0.4115): experimental
holo geometry 34/35 correct, predicted-apo 17/35 (a ~50% drop mirroring the
heldout 45->23), and predicted-apo + injected sequence cofactor presence
30/35 -- recovering 12 of the 17 apo-lost primaries (70.6%) with **0**
regressions. Train (in-sample reference) recovers 56/59 (94.9%); the
in-sample/out-of-sample gap is why the calibration number is the one to trust.
The router consumes the injected `ligand_context.cofactor_families` through the
0.18-weight `cofactor_context_score` term, which is enough to un-abstain a
cofactor-dependent primary at 0.4115. Sequence-supported suppression lowers
recall on this all-in-scope surface (it protects the OOS-FP side, which is not
measured here).

Consequence / next gate: this projects to roughly 23 -> ~38/45 on heldout if the
out-of-sample recovery rate holds, but that is a PROJECTION; the heldout read
stays one-shot and authorization-gated. Next levers to push recovery further and
cut the residual FP: cofactor localization (which residues), pLDDT active-site
abstention, and a real Kabsch cofactor transplant (numpy is now available).

References:

- `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json`
- `work/in_distribution_predicted_geometry_recovery_current702_20260604.md`
- `src/catalytic_earth/predicted_geometry_recovery.py`
- `tests/test_predicted_geometry_recovery.py`

## 2026-06-04: Leakage-Safe Cofactor-Presence Channel (train/cal only)

Decision: the sequence -> cofactor-presence channel must select its per-class
operating thresholds and per-class embedding backend on a held-in calibration
split, never on heldout. The original `sequence_cofactor_channel` fits the
presence heads on `in_distribution` but reads the heldout cofactor labels both
to report ROC-AUC/AP and to pick the best backend per class; even though the
cofactor-presence label is structural (ligand context, not the mechanism
target), reading heldout to score and to choose sources entangles the one-shot
heldout surface with channel design. Per the active instruction to abstain on
the heldout, the channel is rebuilt train/cal-only.

Result: new `cofactor_presence_calibration` module fits one-vs-rest presence
heads (metal_ion/flavin/plp/heme) on the 410 train rows of the frozen
mechanism-feature embedding split, selects max-F1 thresholds and the per-class
backend on the 103 calibration rows, and emits per-entry predictions for all
702 rows (heldout included) without ever reading heldout labels. Calibration
ROC-AUC: metal_ion 0.7707, flavin 0.9263, plp 0.9924, heme 0.88; plp (4
calibration positives) and heme (3) are flagged `low_calibration_support` and
are report-only operating points. A unit test flips every heldout label and
asserts the fitted heads, selected sources, and predictions are byte-identical,
proving heldout is never read. These calibration-honest numbers are
deliberately more conservative than the prior heldout-evaluated channel.

Consequence / next gate: the per-entry predictions are drop-in compatible with
the router `ligand_context` injection (`_fused_geometry_features`). Applying them
to the heldout mechanism router (the cofactor-restoration recovery ceiling) reads
the one-shot heldout mechanism labels and is NOT run here; it stays explicitly
authorization-gated. Built on isolated worktree branch
`claude/cofactor-presence-channel`.

References:

- `artifacts/v3_cofactor_presence_calibration_current702_20260604.json`
- `work/cofactor_presence_calibration_current702_20260604.md`
- `src/catalytic_earth/cofactor_presence_calibration.py`
- `tests/test_cofactor_presence_calibration.py`

## 2026-06-04: Lever 3 Current Evidence Still Blocks Deployment Closure

Decision: keep Lever 3 fail-closed. Do not rerun or retune threshold `0.44155`
from the current residual surface. The local repository does not contain
approved deployment-valid predicted coordinates for the four AFDB-unavailable
coordinate-source blockers, and Q43088 still lacks two approved source-free
locator positions or an equivalent geometry sidecar.

Result: local deployment-input preflight found 0 approved predicted-coordinate
hits for `m_csa:416`/P07071, `m_csa:562`/P07658, `m_csa:586`/P00806, and
`m_csa:637`/P04531. Experimental CIF shortcuts exist for P07658, P00806, and
P04531, but they are explicitly disallowed as deployment inputs. P07071 has no
local CIF hit. Q43088 has a local predicted structure and one Tyr287 anchor; a
review-only neighbor scout generated 12 candidate positions, all pending
review, with 0 locator approvals and 0 rescore readiness. An additional
repo-wide CIF sanity scan over 1,636 local CIFs found only those same three
experimental shortcuts and no P07071 local CIF hit.

Consequence / next gate: the smallest surface-completeness experiment is an
approval/staging manifest for predicted coordinates for P07071, P07658, P00806,
and P04531 with provider/model/version/path/checksum provenance, plus explicit
approval of two Q43088 locator positions or an equivalent geometry sidecar. The
smallest calibration experiment remains the frozen 16-row high-cofactor
train/cal OOS probe; the 170-row same-family structural acquisition remains the
larger calibration blocker.

Artifacts:
`artifacts/v3_fold_augmented_confounded_proxy_deployment_input_preflight_current702_20260604.json`,
`artifacts/v3_fold_augmented_confounded_proxy_repo_wide_coordinate_sanity_scan_current702_20260604.json`,
`artifacts/v3_fold_augmented_q43088_source_free_locator_candidate_scout_current702_20260604.json`,
`artifacts/v3_fold_augmented_confounded_proxy_current_evidence_blocker_after_input_preflight_current702_20260604.json`.

## 2026-06-04: Lever 2 Partial Surface Read Once, Not Deployable

Decision: accept the deterministic missing-locator abstention operating contract
only as a fail-closed readout contract, spend the frozen heldout read exactly
once, and reject the resulting partial-surface Lever 2 channel as deployable.
Do not rerun, retune, lower the threshold, refit the model, or treat the 87
missing-locator rows as feature values.

Result: the accepted partial source-free surface scored 53 feature-complete
heldout rows and carried 87 missing-locator rows as deterministic abstentions.
At the frozen residual threshold, OOS abstain recall is **1.0** but primary
retain recall is **0.0**. The post-readout recovery queue has 119 rows: 32
feature-complete primaries abstain by residual, 16 additional primaries abstain
because their source-free locators are missing, and 71 OOS rows remain
missing-locator coverage rows.

Consequence / next gate: coverage repair alone is not sufficient. Continue Lever
2 with train/cal-safe feature or materialization repair for feature-complete
primary abstentions, then recover primary source-free locator coverage. Treat the
heldout readout as final evidence for this surface.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_operating_contract_decision_current702_20260604.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_heldout_threshold_readout_current702_20260604.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_heldout_threshold_readout_retention_decision_current702_20260604.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_post_readout_recovery_queue_current702_20260604.json`.
## 2026-06-04: Problem 2 Solution Architecture — Reconstruct Deploy-Missing Context From Sequence

Decision (planning, not a result): adopt a generalized solution architecture for
the predicted-geometry robustness problem, and make the next build the sequence
cofactor-presence channel. The experimental-cofactor atom-level graft is demoted
to an optional oracle and is NOT on the critical path.

First-principles framing: the router was validated on experimental active-site
geometry but deploys on sequence (-> predicted apo structure). The degradation is a
train/deploy feature-shift — the router leans on active-site context that
experimental structures contain and predicted apo ones lack. For the v1 families
that context is the cofactor/metal; for future classes it will be substrate,
metal, PTM, oligomeric interface, or ordered water. The general problem is therefore
"reconstruct the deploy-missing active-site context from the only deploy-available
signal (sequence), and abstain when you cannot."

Generalized method (reusable for any future class):
1. Diagnose which missing context drives the drop — `failure_decomposition`
   (built, class/backend-agnostic).
2. Bound the ceiling if that context were restored — `cofactor_restoration_probe`
   plus the coordinate-free `cofactor_graft_fidelity_probe` (built, generic).
3. Reconstruct the channel from sequence — train a sequence -> missing-context head
   on train/cal only, supervised by STRUCTURAL observations (ligand context /
   cofactor-locus sidecars), never by the mechanism fingerprint, EC, Rhea, or
   mechanism text (else it is circular/leaky). This is the next build.
4. Fuse + abstain — feed the reconstructed context into the router where the
   experimental ligand_context used to plug in, and domain-adapt: calibrate the
   threshold on the predicted-apo-plus-reconstruction regime (not the experimental
   regime), using reconstruction confidence + pLDDT for principled abstention. The
   3 distorted-backbone rows (`m_csa:213`, `m_csa:854`, `m_csa:714`) are abstention
   cases and the ESMFold2 secondary-lever boundary.

Two deploy paths for step 3/4: (A) feature-channel — predicted cofactor presence
fed as a feature; lighter, most general, needs no atom placement. (B)
structure-restoration — graft a CANONICAL/template cofactor (not the experimental
one) into the predicted apo pocket and recompute real geometry; heavier, reuses the
graft machinery with a de-circularized template. Default to (A); keep (B) and the
graft machinery in reserve.

Why the experimental-cofactor atom graft is not needed: it transplants the
experimental cofactor, which is unavailable at deploy time (circular), so it can
only be an oracle that (i) sharpens the 19-22/22 ceiling to one integer and (ii)
one-time-validates the cheap coordinate-free proxy for future classes. Both are
optional; neither blocks the channel. Revisit only if scaling the diagnostic to
many classes (validate the proxy once) or if choosing deploy-path (B).

Next step: build step 3 — the leakage-safe train/cal sequence -> cofactor-presence
channel — starting from an audit of `sequence_cofactor_channel.py` and the
materialized cofactor-locus sidecars, measured against the 19-22/22 ceiling.

## 2026-06-04: Cofactor Graft Is Realistic For 19/22 (3 Need Better Predicted Geometry)

Decision: the idealized 22/22 cofactor-restoration recovery holds up under a
realistic rigid graft for **19/22** rows; the 3 exceptions are where the predicted
backbone itself is distorted, which is the boundary where the ESMFold2 secondary
lever (better predicted geometry) matters. This refines, and does not overturn,
the cofactor-awareness conclusion.

Method (coordinate-free fidelity proxy, no fit): the restoration probe assumed
perfect cofactor placement. This probe measures whether the predicted active-site
scaffold is preserved well enough that a real rigid graft keeps the cofactor
proximal. It compares catalytic-residue internal pairwise distances (CA/centroid,
rotation/translation invariant) between experimental and predicted structures, and
flags a row graft-realistic when it recovered idealized AND the worst active-site
distance distortion is within the cofactor's experimental proximity margin
(6.0 A cutoff minus the cofactor's experimental min distance).

Result: graft-realistic recovery **19/22**; active-site faithful (internal RMSD
<= 1.5 A) 20/22 — most pockets are near-rigid (RMSD 0.12–0.6 A). The distorted
rows are `m_csa:213` (RMSD 18.6 A) and `m_csa:854` (RMSD 8.2 A); `m_csa:714` is
faithful by RMSD but fails the proximity-margin test on its worst pair. These 3
are exactly the rows where cofactor restoration alone is insufficient and a better
predicted backbone would help.

Why coordinate-free: numpy is unavailable in this environment (no Kabsch SVD), and
proximal-ligand atom coordinates are not stored in the geometry features, so a
full atom-level superposition is not run here. The internal-distance metric is
invariant to frame and needs no superposition. The true atom-level graft
(superpose on catalytic residue atoms, transplant cofactor atoms, recompute
proximity, re-score) is the documented next escalation; the predicted heldout CIFs
are already staged locally under
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/queries_all_heldout/`.

Artifacts:
`artifacts/v3_cofactor_graft_fidelity_probe_current702_20260604.json`,
`work/cofactor_graft_fidelity_probe_current702_20260604.md`.

## 2026-06-04: Cofactor Restoration Recovers 22/22 Lost Primaries (Backbone Is Faithful)

Decision: cofactor-restoration is confirmed as the Problem-2 lever with a perfect
ceiling. A no-fit counterfactual that restores the experimental cofactor onto the
predicted apo backbone recovers **22/22 cofactor_apo_loss lost primary rows**
(100%; Wave 1 readthrough 20/20). The predicted backbone is therefore faithful
enough that the missing cofactor is the entire loss; a better apo folder
(ESMFold2) is not needed for primary recovery and cannot supply the cofactor.

Method (counterfactual, no fit, frozen threshold/fingerprints): for each
cofactor_apo_loss lost primary row, inject the experimental proximal cofactor/metal
`ligand_context` onto the predicted (apo) geometry entry, keep the predicted
residue geometry, and re-score with the frozen `run_geometry_retrieval` and hand
router at 0.4115. Recovered = restored call is non-abstained and matches the true
fingerprint. An apo control rescore (no injection) **reproduces the audit exactly**
(`apo_control_rescore_matches_audit: true`), validating the harness.

Result: all 22 lost primaries recover; per-row score lifts are 0.08–0.41 and every
row flips from abstain/`metal_dependent_hydrolase`-misroute to the correct
fingerprint (flavin/PLP/heme/metal/Fe-S). This is an UPPER BOUND (perfect cofactor
placement); real docking is imperfect.

Implication: the next build is a real cofactor-restoration feature — graft/dock the
cofactor into the predicted active site, or a sequence cofactor-presence channel
(`sequence_cofactor_channel.py` / `cofactor_channel_probe.py`) — selected on
train/cal, heldout one-shot. ESMFold2 stays scoped to its secondary value (OOS
false-positive reduction + pLDDT abstention). The probe is backend-agnostic; re-run
it on a future ESMFold2 audit to confirm the same pattern.

Artifacts:
`artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json`,
`work/cofactor_restoration_recovery_probe_current702_20260604.md`.

## 2026-06-03: Predicted-Geometry Degradation Is Cofactor-Loss-Dominated

Decision: Problem 2's primary lever is **cofactor-awareness, not a better apo
structure predictor**. A no-fit failure decomposition of the AlphaFoldDB-v6
robustness audit shows the 45/45 -> 23/45 primary drop is driven entirely by
missing cofactor geometry, so swapping AlphaFoldDB for ESMFold2 (also apo) cannot
recover the lost primary rows. ESMFold2 is demoted from "expected primary-recovery
lever" to a secondary role: OOS false-positive reduction and pLDDT-gated
abstention only.

Method (descriptive, no fit, no new heldout read): for each predicted-geometry
hand-router row, compare experimental vs predicted proximal cofactor/metal context
and missing residues, and classify each lost primary / OOS false positive as
`cofactor_apo_loss` (cofactor/metal proximal experimentally, absent in the apo
prediction), `fold_or_sidechain` (residues resolved, no experimental cofactor
dependence), or `missing_residue`. This only categorizes outcomes the robustness
audit already computed.

Result: of 22 lost primary rows, **22/22 are `cofactor_apo_loss`** (flavin 10,
PLP 6, metal 4, heme 4, Fe-S 2; all with `predicted_missing_positions == 0`) and
**0 are `fold_or_sidechain`**. Wave 1 readthrough (excluding `m_csa:497`/`m_csa:750`)
is 20/20 cofactor_apo_loss. The 10 OOS false positives are 7 cofactor_apo_loss + 3
fold_or_sidechain (9/10 mis-called `metal_dependent_hydrolase`). Control: 13/23
correctly-called primaries also had an experimental cofactor, proving apo geometry
can suffice for some rows — the lost rows are exactly where stripping the cofactor
breaks the signal.

Implication: the ESMFold2 coordinate-swap primary-recovery upper bound is **0**
(no fold/side-chain-limited row exists for a better apo folder to grab). The
right Problem-2 lever is cofactor-aware (place/dock the cofactor into the
predicted structure, or a sequence cofactor-presence channel — the repo already
has `sequence_cofactor_channel.py` / `cofactor_channel_probe.py`). The staged
ESMFold2 experiment remains worth running only for (a) OOS false-positive
reduction via better apo pocket packing and (b) pLDDT-gated abstention — both
selected on train/cal, heldout one-shot.

Reusable: the decomposition is backend-agnostic and should be re-run on a future
ESMFold2 robustness audit to confirm the same cofactor-loss-dominated pattern.

Artifacts:
`artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json`,
`work/predicted_geometry_failure_decomposition_current702_20260603.md`.

## 2026-06-03: ESMFold2 Robustness Experiment Staged (No-Fit), Backend Added

Decision: address Problem 2 (robustness to predicted vs experimental active-site
geometry degradation) by **staging the ESMFold2 experiment as a no-fit,
leakage-safe contract** plus a runnable `esmfold2` coordinate-supplier backend.
No ESMFold2 inference was run, no weights were downloaded, no threshold was
changed, and no heldout row was read. ESMFold2 was verified real before building
(Biohub / A. Rives, released 2026-05-27, MIT/open weights; corroborated by
Nature, Scientific American, Axios, PR Newswire, GenEngNews).

Why staged, not run: this environment cannot run the experiment. `torch`/`esm`
are not installed, `foldseek` is absent, and every predicted-structure host is
network-blocked (HTTP 403 for Hugging Face, ESM Atlas, and even
`alphafold.ebi.ac.uk` — the source the existing `alphafold_db` backend uses).
Only GitHub and the web-search proxy are reachable. This mirrors the prior
`esmfold` backend, which has been a deliberate blocked stub since 2026-05-29.

What was built (additive, AlphaFoldDB path byte-unchanged):
- `predicted_geometry_robustness.py` now supports `backend="esmfold2"` in the
  robustness, distillation, and in-distribution atlas builders. With no staged
  coordinates it returns a precise `blocked` audit
  (`esmfold2_runtime_or_staged_coordinates_unavailable`). Given a directory of
  pre-staged ESMFold2 mmCIFs keyed by accession (`esmfold2_staged_dir=` or the
  `CE_ESMFOLD2_STAGED_DIR` env var), the `make_esmfold2_staged_supplier` fetcher
  feeds the frozen geometry router and Foldseek/TM fold channel unchanged.
- A no-fit experiment contract that enumerates the exact prediction work list
  (184 in-distribution+fingerprint atlas rows, 140 heldout rows, 323 unique
  accessions), fixes the train/cal-selects-thresholds / heldout-final-only
  discipline, records the AlphaFoldDB-v6 baseline to beat (hand router 23/45
  primary, 12.3% OOS FP; fold/TM AUC 0.814; geometry+fold mean AUC 0.908), plans
  six comparison metrics including pLDDT-gated abstention vs the fixed 0.44155
  fold-augmented gate, and lists exact rerun commands.
- New CLI: `build-esmfold2-robustness-experiment-contract`, plus `--backend
  esmfold2` and `--esmfold2-staged-dir` on the three predicted-geometry commands.
- Seven new unit tests (staged supplier, blocked-when-unstaged, contract
  shape/counts/leakage flags, ready-when-staged).

Apo caveat (kept front and center): ESMFold2, like every sequence folder,
predicts apo structures. It will not place FAD/PLP/heme/Zn or substrate, and the
active-site signal leans heavily on cofactor/metal coordination. ESMFold2 can
improve the protein side-chain part and supply pLDDT confidence, but cannot
supply cofactor geometry. Expect partial help; measure it on train/cal, do not
assume it, and keep the heldout read one-shot.

To run when coordinates can be staged: predict the 323 accessions with ESMFold2
(open `esm` + weights, the Biohub platform, or the ESM Atlas), write them as
mmCIF keyed by accession into a directory, then run the three commands with
`--backend esmfold2 --esmfold2-staged-dir <DIR>`. Select all thresholds/models
on the in-distribution train/cal split; read heldout once.

Artifacts:
`artifacts/v3_esmfold2_predicted_geometry_robustness_experiment_contract_current702_20260603.json`,
`work/esmfold2_predicted_geometry_robustness_experiment_contract_20260603.md`.

## 2026-06-03: Lever 2 Source-Free Token Re-Selection — No Token Clears The Bar

Decision: defer the Lever 2 source-free row-specific feature. A train/cal-only
re-selection (heldout never read) shows **no source-free-replicable token clears a
useful bar**, so the one-shot heldout read will not be spent on any Lever 2 token.
The 53 approved source-free locators remain a banked, split-protected asset; the
source-free discriminative value lives in the geometry/fold structural channel.

Method: on the 43 OOS-augmented train/cal rows (15 in-scope primary, 28 OOS), the
only source-free-replicable feature family is residue-identity counts
(`event_residue_code` / `event_residue_code_count` — countable from a source-free
locator). All role/bond/event-type families are source-derived and excluded.
Labels were used only as the selection target, never as a predictive feature.

Result: multivariate LOO-CV AUC of all source-free residue counts = **0.538**
(≈ random). Best univariate token is His at dir-adjusted AUC 0.601 but
**OOS-pointing** (His is higher in OOS rows). The calibrated His-count fallback
(0.643) was role-dependent: stripped to a raw source-free His count, `HIS>=3`
fires on 4 train/cal rows, all OOS (in-scope precision 0.000). The Lever 2 signal
is entirely in M-CSA role/event bindings, which do not survive source-free.

Contrast: the predicted-structure fold/TM channel is AUC 0.814 (in vs all OOS) and
0.908 for the no-fit geometry+fold mean — a different structural channel and the
project's real source-free signal.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_source_free_token_reselection_train_cal_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_source_free_token_reselection_train_cal_current702_20260603.md`.

## 2026-06-03: Lever 2 Source-Free Event Axis Reviewed, NOT Signed Off (Too Thin)

Decision: the source-free proton-transfer / electrostatic-stabiliser event-axis
linker drafted for Path A is **not signed off**. The one-shot heldout read will
not be spent on it. The reviewer judged the source-free feature too thin to
justify the irreplaceable heldout-read budget. No event-axis linker was
materialized, no application surface built, no frozen residual threshold applied,
no heldout row read.

What was drafted: a deterministic, label-blind structural rubric (residue
identity + contacting atoms + distance + source-free role hints only; no label,
fingerprint, EC/Rhea, source text, curated role, or target name) over the 53
approved source-free locators. Result: **14/53 rows carry the token** (both roles
evidenced; 12 in-scope + 2 boundary-OOS, concentrated in PLP/flavin/heme
phosphate-cofactor enzymes), **39 token-absent**, all confidences modest
(0.21–0.47).

Root-cause diagnosis: the source-free locators anchor on the cofactor/metal, so
the electrostatic-stabiliser role only fires when a cation clamps a cofactor
phosphate (PLP/flavin), and the pair requires a co-located proton-transfer axis.
Metal-hydrolase and many heme sites therefore cannot evidence the pair
source-free — the catalytic proton-transfer / oxyanion machinery is
substrate-proximal, not cofactor-proximal, and is not captured by a
cofactor-proximity locator. The 12/14 in-scope skew emerged from structure, not
the label (no leakage), but the surface is too sparse and low-confidence to read
once.

Consequence / next gate: do not feed this axis to the heldout read. Reconsider
the strengthening strategy before spending the one-shot budget. The 53 approved
locators remain a banked, split-protected asset. The draft and its full per-row
evidence are retained as review-only documentation, not approved inputs.

Artifacts (review-only, not signed off):
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_review_packet_current702_20260603.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_draft_rows_for_signoff_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_draft_rows_for_signoff_current702_20260603.md`.

## 2026-06-03: Lever 2 Locator Rewrites — 53 Approved, 2 Rejected (723, 599)

Decision: after a full per-row review of the 55 priority-1 current702 source-free
locator rewrites, record explicit reviewer decisions: **approve 53, reject
`m_csa:723` and `m_csa:599`**. Decisions are recorded in a separate
approval-decisions artifact with candidate and planned-payload hashes preserved
unchanged; the committed review-only approval packet and materialization gate are
left pending and untouched (they remain regression-pinned to the pre-decision
state). No locator sidecars were copied, no heldout rows read, and no frozen
residual threshold applied.

Rationale: the 55 heldout rows split into 32 in-scope primaries
(`seed_fingerprint`, which the model must retain) and 23 out-of-scope negatives
(which it must abstain on). In-scope rows require the locator to land on the
genuine catalytic center; OOS rows only require a faithful source-free pointer to
the real cofactor/metal site. All 55 are integrity-clean (hashes match, zero
forbidden-feature flags, split-protected). 30/32 in-scope rows anchor correctly
(PLP catalytic-Lys Schiff base ~1.3 A, covalent 8a-His-FAD, Cys-ligated heme,
His/Asp/Glu-metal first shells, 4Fe-4S Cys ligation). All 23 OOS rows are
faithful source-free anchors (structural-metal anchors such as KDM4A Cys3His zinc
and MetRS zinc knuckle remain out-of-distribution).

The two rejected rows are both in-scope `ser_his_acid_hydrolase`:
`m_csa:723` (subtilisin) anchored on the structural Ca loop, not the Ser-His-Asp
triad; `m_csa:599` anchored on a crystallographic Cd ion (curated rationale: "no
metal required"), missing the Ser nucleophile. They expose a method gap:
ligand-proximity locators structurally cannot reach cofactorless catalytic
triads.

Materialization (done): the 53 approved source-free locator sidecars were copied
into the audited locator directory
`artifacts/family_panel_source_free_active_site_locators_current702_20260601/`
(now 5 family-panel + 53 Lever 2 = 58 sidecars) via the write-enabled
materialization gate. Each sidecar carries `manual_review_approval.approved_by:
VivekVardhanArrabelli`, `locator_policy:
human_approved_structure_local_ligand_geometry_without_source_text`,
`ready_for_predicted_geometry_scoring: True`, and stays split-protected
(review_only, not for training/threshold/import). The 2 rejected rows
(`m_csa:723`, `m_csa:599`) were not written. The audited-dir regression snapshot
test was updated to the 58-sidecar post-approval state. No heldout rows were read
and no frozen residual threshold was applied.

Consequence / next gate: (1) the approved source-free locator surface now exists;
the frozen residual threshold and any heldout read remain blocked on the
source-free event-axis proton-transfer linker (0 linker rows) or an explicit
His-count fallback acceptance, plus the heldout-safe application surface. (2)
Build a source-free catalytic-triad geometric locator for serine hydrolases
(decision: design): detect a Ser/Cys/Thr-His-Asp/Glu triad from coordinates +
residue identity only, under the same forbidden-feature contract, emitting the
same `residue_locators` schema, then re-decide `m_csa:723`/`m_csa:599`.

Verification: write-enabled materialization gate reports 53
`approved_locator_sidecars_written`, 0 critical violations,
`approved_source_free_locator_surface_ready: True`, with
`heldout_rows_evaluated: False` and `frozen_residual_threshold_applied: False`;
intake preflight reports status ready with 53 locator-materialization-ready
approvals, 2 rejections, 0 invalid, 0 source-edit-contract violations.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_decisions_current702_20260603.json`,
`artifacts/v3_active_lever_source_decision_intake_preflight_lever2_decision_applied_current702_20260603.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_materialized_current702_20260603.json`,
the 53 materialized sidecars under
`artifacts/family_panel_source_free_active_site_locators_current702_20260601/`,
and
`work/active_lever_lever2_locator_rewrite_reviewer_decision_record_current702_20260603.md`.

## 2026-06-03: Organic-Score Follow-Up Proxy Axis Scored, Still Partial

Decision: keep the `organic_score_0_30_to_below_high_axis_threshold` Lever 3
follow-up proxy axis as a bounded train/cal-only tranche readout. It excludes
the already scored overlap row `m_csa:89`, scores only the four remaining
contracted rows, and does not authorize a global fixed-threshold proxy audit
rerun or deployment closure claim. No labels, registries, ontologies, imports,
production thresholds, splits, model weights, source decisions, or heldout
threshold tuning changed.

Result: the follow-up contract selects `m_csa:60`, `m_csa:75`, `m_csa:214`,
and `m_csa:288`. All four now have AFDB-v6 query coordinates, nearest-train
Foldseek/TM hits, predicted-geometry scores, selected cofactor scores, and
combined geometry/fold channel scores. At fixed threshold `0.44155`, only
`m_csa:288` abstains. The composed train/cal OOS surface expands to 196/202
full-channel rows and remains partial because six prior/base blockers are still
unresolved. The post-follow-up background-axis scout now reports 160 remaining
background-only rows, 0 active-site-count candidates, 0 organic-score
candidates, and 8 unsupported-geometry rows that remain data-quality blockers
rather than countable abstention evidence. A repair-only queue now records all
eight unsupported-geometry rows with accessions and required coordinate/locus
repair gates; 0/8 expected AFDB-v6 coordinate files are local and 0 rows are
ready to score.

Consequence / next gate: do not promote this readout to an operating-point
claim. First clear the remaining prior/base full-channel and policy/calibration
blockers, starting with the P10746 decision if reviewed, or pre-register another
non-overlapping train/cal-only source-free proxy-axis contract before further
scoring.

Artifacts:
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_contract_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_contract_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scoring_input_manifest_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scoring_input_manifest_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scored_extension_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scored_extension_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_fixed_threshold_readout_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_fixed_threshold_readout_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_extended_train_cal_oos_surface_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_extended_train_cal_oos_surface_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_blocker_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_blocker_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_scout_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_scout_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_post_followup_unsupported_geometry_repair_queue_current702_20260603.json`,
and
`work/fold_augmented_confounded_proxy_train_cal_post_followup_unsupported_geometry_repair_queue_current702_20260603.md`.

## 2026-06-03: Active-Site-Count Proxy Axis Scored, Not Closure-Sufficient

Decision: keep the new `active_site_residue_count_10_plus` Lever 3 proxy axis
as a bounded train/cal-only readout. It is pre-registered and fully scored, but
it does not authorize a global fixed-threshold proxy audit rerun or deployment
closure claim. No labels, registries, ontologies, imports, production
thresholds, splits, model weights, source decisions, or heldout threshold tuning
changed.

Result: the contract selects six train/cal rows and the scoring extension gives
6/6 full-channel geometry/fold/cofactor rows. The appended surface has 192/198
train/cal OOS full-channel rows and remains partial because six prior/base
blockers are still unresolved. At fixed threshold `0.44155`, the new proxy axis
abstains only `m_csa:466` and retains the other five rows.

Consequence / next gate: do not promote this readout to an operating-point
claim. First clear the remaining prior/base full-channel and policy/calibration
blockers, or pre-register another train/cal-only source-free proxy-axis contract
before further scoring.

Artifacts:
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scoring_input_manifest_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scoring_input_manifest_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_extended_train_cal_oos_surface_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_extended_train_cal_oos_surface_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_current702_20260603.md`,
`artifacts/v3_active_lever_mechanical_actionability_audit_current702_20260603.json`,
and
`work/active_lever_mechanical_actionability_audit_current702_20260603.md`.

## 2026-06-03: Source-Free Locator Policy Queue Closed For Automation

Decision: close the remaining family-panel source-free locator policy queue for
automation. This is not an import/countability unlock: all five locator rows
remain blocked, no locator copy/scoring is authorized, and no labels,
registries, ontologies, imports, thresholds, splits, model weights, or
coordinates changed.

Result: the consolidated closure status composes the `mh_065`/`mh_072`,
external glycoside, Q59490, and `mh_064` block decisions with the import-preview
blocker gate. It records 5 blocked locator rows, 0 automation-clearable locator
decisions, 0 rows approved for locator copy or predicted-geometry scoring, 0
import-preview-ready rows, and 0 countable label candidates.

Consequence / next gate: do not continue locator automation on these five rows
until external approval/evidence is supplied. If evidence arrives, rerun the
relevant locator schema/integrity and import-preview blocker gates before
scoring or countability claims.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_policy_closure_status_current702_20260603.json`
and
`work/family_panel_source_free_locator_policy_closure_status_current702_20260603.md`.

## 2026-06-03: mh_064 Locator Left Blocked; No Alternate Fetch Authorized

Decision: leave `mh_064` blocked. Do not fetch alternate coordinates in this
automation run, do not copy locator sidecars, and do not run predicted-geometry
scoring. No import, label, registry, ontology, threshold, split, or model-weight
change is authorized.

Rationale: the local-cache preflight found zero of five bounded alternate
coordinate files cached for `3RKJ`, `3RKK`, `3SBL`, `3SFP`, and `3SPU`. The
selected `3PG4` coordinate and requested AFDB coordinate are cached but do not
clear the no-ligand alternate-coordinate blocker. Fetching new coordinates is a
policy action and is not authorized by this automation run.

Consequence / next gate: unblock only after explicit approval to fetch one or
more bounded alternate coordinates, then rerun candidate extraction and locator
schema/integrity review before predicted-geometry scoring. The remaining
locator-policy queue is now closed for automation: all unresolved rows require
external approval/evidence before copy, fetch, scoring, import, or label action.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_mh064_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_mh064_block_decision_current702_20260603.md`.

## 2026-06-03: Q59490 Locator Left Blocked; No Alternate Source Or Fabricated Locators

Decision: leave `secondary_probe::cobalamin_radical_rearrangement` / Q59490
blocked. Do not authorize alternate-source substitution, do not fabricate
residue locators from panel identity or source prose, and do not run
predicted-geometry scoring. No coordinate fetch, locator copy, import, label,
registry, ontology, threshold, split, or model-weight change is authorized.

Rationale: the nonlabel-locator feasibility audit found no coordinate anchor
that can safely provide at least two source-free sequence-position locators for
Q59490. The alternate-source cache scout found zero eligible alternate cobalamin
source rows and zero excluded rows with local coordinates. The three primary
Q59490 local coordinate paths do not by themselves authorize locator
fabrication.

Consequence / next gate: unblock only with an explicitly authorized alternate
source row/coordinate or a nonlabel locator strategy with at least two
source-free sequence-position locators, then rerun locator schema/integrity
review before predicted-geometry scoring. The remaining open locator-policy
decision is now `mh_064` alternate-coordinate fetch approval.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_q59490_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_q59490_block_decision_current702_20260603.md`.

## 2026-06-03: External Glycoside Locator Left Blocked; No Acetate/NAG Copy

Decision: leave `external_glycoside_panel` blocked. Do not copy the 7QQF
acetate locator, NAG/glycan-derived locator, or any raw glycan/buffer
retargeting into the audited source-free locator directory. No predicted-
geometry scoring, coordinate fetch, import, label, registry, ontology,
threshold, split, or model-weight change is authorized.

Rationale: the NAG validator already rejected glycan-context retargeting. The
local-cache substrate-coordinate scout scanned 60 coordinate files and found
four same-accession coordinate records but zero substrate-like coordinate
candidates. The only same-accession PDB coordinate with non-water HETATMs has
ACT/BMA/FUC/MAN/MLI/NAG glycan or buffer ligands, which cannot clear the
non-glycan substrate-coordinate gate.

Consequence / next gate: unblock only with an explicit substrate-complex
coordinate or expert-approved non-glycan active-site locator, then rerun
locator schema/integrity review before predicted-geometry scoring. The remaining
open locator-policy decisions are now `mh_064` alternate-coordinate fetch
approval and Q59490 nonlabel locator or alternate-source authorization.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.md`.

## 2026-06-03: Expanded Train/Cal OOS Threshold Regeneration Keeps 0.44155

Decision: materialize the post-rerun expanded train/cal OOS-negative surface
and regenerate the OOS-calibrated fold-augmented threshold contract from that
surface. This is a research calibration artifact only: no production threshold,
label, registry, ontology, import, split, model weight, or heldout-tuned surface
changed.

Result: the expanded surface composes the four fixed-threshold combined readout
rows into the prior train/cal OOS negative surface, increasing full-channel
coverage from 71/76 to 75/76 rows. `m_csa:204`/P10746 remains the sole
fold-only policy caveat and the surface is still partial. The regenerated
OOS-calibrated research contract keeps the primary
`combined_mean_geometry_fold` threshold at `0.44155`; calibration OOS
abstention is 30/75, and the heldout final readout remains 45/47 in-scope rows
retained, 44/79 OOS rows abstained, and 5/6 cofactor-confounded OOS rows
abstained.

Consequence / next gate: do not rerun this threshold-selection step unless the
train/cal surface changes again. Lever 3 deployment closure is still blocked by
the P10746 fold-only caveat: either explicitly accept that caveat for
deployment closure or provide an approved non-residue sidecar.

Artifacts:
`artifacts/v3_fold_augmented_expanded_train_cal_oos_negative_surface_scores_current702_20260603.json`,
`work/fold_augmented_expanded_train_cal_oos_negative_surface_scores_current702_20260603.md`,
`artifacts/v3_fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.json`,
and
`work/fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.md`.

## 2026-06-03: mh_065/mh_072 Remapped Locators Rejected; Leave Blocked

Decision: leave `mh_065` and `mh_072` blocked. Do not copy the raw
`1DDK`/`1E9I` locators and do not approve alignment/remapped locators from the
current evidence.

Rationale: the matching-coordinate scout scanned 712 local coordinate files and
found 0 matching non-AFDB replacement coordinates. The selected PDBs map by
`struct_ref` to `Q932P5` and `P08324`, not the requested source rows `Q79MP6`
and `P0A6P9`. The only same-accession AFDB options already failed residue-code
transfer with 0/6 expected residue-code matches. Approving remapped locators
would accept the unverified-transfer failure mode the locator schema is meant
to block.

Consequence / next gate: these rows remain review-only/non-countable and
source-free predicted-geometry scoring stays blocked. Unblock only with a
matching frozen coordinate whose `struct_ref` maps to the requested source
accession, or with a real expert alignment/remapping that resolves the
residue-code mismatch, followed by locator schema/integrity review.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_mh065_mh072_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_mh065_mh072_block_decision_current702_20260603.md`.

## 2026-06-03: Lever 3 Human Decisions Applied; Combined Rerun Readout Lands

Decision: record the five Lever 3 production-blocker human/policy decisions as
a decision-application artifact, materialize the three approved source-feature
sidecars, fetch/hash the authorized P00889 ortholog surrogate coordinate, and
compose a fixed-threshold pre-rerun readiness gate. P10746 is kept fold-only
with the non-residue-sidecar policy caveat. No Foldseek/TM or combined-channel
rerun was performed before the readiness gate. A follow-on fixed-threshold
readout then reran only the P00889 surrogate Foldseek query against the existing
train atlas, scored the four combined rows at threshold `0.44155`, and kept
P10746 fold-only. No labels, registries, ontologies, imports, thresholds,
splits, model weights, or heldout-tuned surfaces changed.

Result: the human/policy decision blockers are now 0, but deployment closure is
still false. The approved source-feature sidecar surface has been materialized
for rerun input with 3 rows and 18 source-feature support records. The P00889
AFDB CIF has been fetched and hashed (`8e41533a...`). The pre-rerun readiness
gate reports ready=true with 0 remaining pre-rerun blockers. The fixed-threshold
combined readout scores four rows: `m_csa:78` and `uniprot:P78549` abstain,
while `m_csa:531` and `uniprot:Q3LXA3` are retained. The calibration-impact
audit expands the train/cal OOS combined-score surface from 71/76 to 75/76
rows, with 30/75 abstained at the fixed threshold and only `m_csa:204` still
blocked from combined scoring. The post-rerun closure-status gate therefore
reduces the prior five production blockers to one unresolved P10746 fold-only
caveat, while preserving the existing 5/6 heldout confounded OOS abstention
readout from the prior readiness artifact. The post-rerun confounded closure
audit now composes the expanded threshold contract directly and records the
current state as research-ready with one P10746 caveat, not five production
blockers.

Consequence / next gate: carry the fixed-threshold impact and P10746 fold-only
caveat into the deployment decision. Either explicitly accept the P10746
fold-only caveat for deployment closure or provide an approved non-residue
sidecar. A 2026-06-03 UniProtKB refresh for P10746 returned HTTP 200 and 63
features, but 0 eligible active-site/binding-site source-feature rows, so it
does not open an automation-clearable sidecar path. A P10746 decision packet now
stages the one remaining accept/reject choice with an unchanged context hash;
the companion application gate validates the current packet as hash-matched
but still pending. The post-decision closure gate therefore remains blocked
only by the unaccepted P10746 caveat. No caveat was accepted and deployment
remains unclosed. A separate OOS-calibrated threshold regeneration may be run
from the expanded train/cal surface only if wanted; do not tune on heldout rows.

Artifacts:
`artifacts/v3_fold_augmented_blocker_human_decision_application_current702_20260603.json`,
`work/fold_augmented_blocker_human_decision_application_current702_20260603.md`,
`artifacts/v3_fold_augmented_approved_source_feature_active_site_sidecar_materialization_current702_20260603.json`,
`work/fold_augmented_approved_source_feature_active_site_sidecar_materialization_current702_20260603.md`,
`artifacts/v3_fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current702_20260603.json`,
`work/fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current702_20260603.md`,
`artifacts/v3_fold_augmented_fixed_threshold_rerun_readiness_current702_20260603.json`,
`work/fold_augmented_fixed_threshold_rerun_readiness_current702_20260603.md`,
`artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_readout_current702_20260603.json`,
`work/fold_augmented_fixed_threshold_combined_rerun_readout_current702_20260603.md`,
`artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current702_20260603.json`,
`work/fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current702_20260603.md`,
`artifacts/v3_fold_augmented_p10746_source_feature_refresh_audit_current702_20260603.json`,
`work/fold_augmented_p10746_source_feature_refresh_audit_current702_20260603.md`,
`artifacts/v3_fold_augmented_post_rerun_deployment_closure_status_current702_20260603.json`,
`work/fold_augmented_post_rerun_deployment_closure_status_current702_20260603.md`,
`artifacts/v3_fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.json`,
`work/fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.md`,
`artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_packet_current702_20260603.json`,
`work/fold_augmented_p10746_deployment_caveat_decision_packet_current702_20260603.md`,
`artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_application_current702_20260603.json`,
`work/fold_augmented_p10746_deployment_caveat_decision_application_current702_20260603.md`,
`artifacts/v3_fold_augmented_post_decision_deployment_closure_status_current702_20260603.json`,
and
`work/fold_augmented_post_decision_deployment_closure_status_current702_20260603.md`.

## 2026-06-03: Lever 4 Local-Cache Locator Discovery Closes With Five Human/Policy Blockers

Decision: treat the remaining family-panel source-free locator blockers as
human/policy decisions, not automation-discovery tasks. No coordinates were
fetched, no locator sidecars were copied, no predicted-geometry scoring was
run, no import preview was written, and no labels, registries, ontologies,
thresholds, splits, model weights, or heldout-tuned surfaces changed.

Result: local-cache scouts found 0 non-AFDB replacement coordinates for
`mh_065`/`mh_072`, 0 same-accession substrate-like coordinates for
`external_glycoside_panel`, and 0 eligible alternate source rows for Q59490.
The human-decision matrix now tracks 5 remaining blocker rows across 4 decision
classes, with 0 automation-clearable rows. The refreshed family-panel
import-preview blocker gate still reports 0/22 import-preview-ready rows and
0 countable label candidates.

Consequence / next gate: decide the `mh_065`/`mh_072` matching-coordinate or
remapped-locator policy first, then rerun the relevant locator schema/candidate
audit and the import-preview blocker gate before any copy, fetch, scoring,
import preview, or label-factory action.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072_current702_20260602.json`,
`work/family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072_current702_20260602.md`,
`artifacts/v3_family_panel_source_free_locator_glycoside_substrate_coordinate_scout_external_glycoside_panel_current702_20260602.json`,
`work/family_panel_source_free_locator_glycoside_substrate_coordinate_scout_external_glycoside_panel_current702_20260602.md`,
`artifacts/v3_family_panel_source_free_locator_q59490_alternate_source_cache_scout_current702_20260602.json`,
`work/family_panel_source_free_locator_q59490_alternate_source_cache_scout_current702_20260602.md`,
`artifacts/v3_family_panel_source_free_locator_human_decision_matrix_current702_20260601.json`,
`work/family_panel_source_free_locator_human_decision_matrix_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_import_preview_blocker_gate_current702_20260602.json`,
and
`work/fold_augmented_family_panel_import_preview_blocker_gate_current702_20260602.md`.

## 2026-06-02: Lever 3 Blocker-Specific Gates Cover All Five Remaining Fold Deployment Rows

Decision: keep the predicted-structure-vs-atlas fold channel at the fixed
OOS-calibrated operating threshold `0.44155` and treat the five remaining
production blocker rows as explicit review/policy gates, not as fold-only or
automatic sidecar escapes. No sidecar was approved or copied, no alternate
accession was authorized, no coordinate was fetched, no Foldseek/TM scores were
rerun, and no thresholds, labels, registries, ontologies, imports, or model
weights changed.

Result: the source-feature sidecar review gate covers the three
coordinate-available source-feature blocker rows (`m_csa:531`,
`uniprot:P78549`, and `uniprot:Q3LXA3`) with 3 strict-audit-clean draft rows
and 3 manual approval decisions required. The P23007 alternate-accession policy
gate exposes 4 AFDB-backed pattern-compatible citrate-synthase candidates
(`O75390`, `P00889`, `Q8VHF5`, and `Q9CZU6`) but authorizes 0 replacements and
0 coordinate fetches. The P10746 non-residue interaction preflight keeps
`m_csa:204` blocked with 0 source-feature rows, 0 curated residue nodes, and 0
approved non-residue policy rows; mechanism text remains forbidden as a
predictive sidecar source.

Consequence / next gate: decide the three draft source-feature sidecar
approvals, decide exactly one P23007 alternate accession or reject the
substitution path, and approve a concrete P10746 non-residue interaction
sidecar policy or keep it fold-only. Only after those decisions should the
combined predicted-geometry/fold channel be rerun at the fixed threshold.

Artifacts:
`artifacts/v3_fold_augmented_source_feature_active_site_sidecar_review_gate_current702_20260602.json`,
`work/fold_augmented_source_feature_active_site_sidecar_review_gate_current702_20260602.md`,
`artifacts/v3_fold_augmented_p23007_alternate_accession_policy_gate_current702_20260602.json`,
`work/fold_augmented_p23007_alternate_accession_policy_gate_current702_20260602.md`,
`artifacts/v3_fold_augmented_non_residue_interaction_sidecar_policy_preflight_current702_20260602.json`,
`work/fold_augmented_non_residue_interaction_sidecar_policy_preflight_current702_20260602.md`,
`artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json`,
and
`work/predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.md`.

## 2026-06-03: Priority-1 Source-Free Locator Preflight Is Not Copy Approval

Decision: the 55 priority-1 current702 heldout coordinate-anchor locator rows
that passed rewrite preflight remain blocked until an explicit approval-decision
artifact supplies matching candidate and planned-payload hashes. Preflight alone
does not authorize copying locator sidecars into the audited directory, scoring
heldout rows, or applying the frozen row-specific residual threshold.
The approval packet is an intake worksheet, not an approval artifact: it stages
55 pending approve/reject records with immutable candidate and planned-payload
hashes, while recording 0 approvals.

Rationale: the calibrated Lever 2 row-specific feature pair still needs a
source-free heldout locator surface and a source-free proton-transfer event
axis. Copying from preflight without explicit approval would bypass the manual
forbidden-feature review gate that separates source-free locator evidence from
heldout M-CSA mechanism text and curated role labels. The approval packet now
names the exact hash-matched records reviewers must produce; the new gate
consumes approvals mechanically when they exist but fails closed now: 55
preflight rows, 0 explicit approvals, 0 locator writes, and 0 heldout reads.
The composed pre-threshold readiness gate additionally requires materialized
source-free event-axis linkers and a complete heldout-safe pair application
surface before the frozen residual threshold can be applied once.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_current702_20260603.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_current702_20260603.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_current702_20260603.json`,
and
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_current702_20260603.md`.

## 2026-06-02: Source-Free Pair Deployment Blocks On Event Linker; His-Only Fallback Is Lower Recall

Decision: keep the calibrated row-specific best-token follow-up pair as
calibration-only until a source-free event/residue-role linker exists. The pair
uses `event_residue_role:proton_transfer|electrostatic_stabiliser` plus
`residue_code_count:his=3`; the first token cannot be computed from the current
source-free heldout surface without a source-free proton-transfer event axis.
Do not substitute the M-CSA curated heldout active-site role graph as a
deployment feature.

Result: the event-linker blocker audit confirms 0 current702 heldout locator
sidecars, 0 source-free event/residue-role feature rows, and 132 M-CSA curated
heldout role-graph rows that remain forbidden as deployment inputs. The
calibrated pair keeps calibration OOS abstention at 0.857143. A separate
His-count-only fallback contract avoids the event axis but drops calibration OOS
abstention to 0.642857 (AUC 0.758929), so it is not accepted as a deployable
replacement without an explicit policy decision. The fallback is also blocked
by the same source-free locator surface: 55 preflight-passed locator rewrites
remain pending explicit approval, including 6 warning rows and 0 approved
rewrites.

Consequence / next gate: choose one of two explicit paths before any heldout
read. Preferred path: build the source-free proton-transfer event-axis linker
for `proton_transfer|electrostatic_stabiliser`, then rerun the source-free
application surface and heldout-safe surface plan. Fallback path: explicitly
accept the lower-recall His-count-only contract, approve/copy audited
current702 heldout locator sidecars, and only then apply the frozen fallback
threshold once. No labels, registries, ontologies, imports, production
thresholds, model weights, or heldout readouts changed.

Schema gate: the source-free event-axis linker schema is now staged. It requires
an approved current702 heldout locator sidecar, accession-compatible
UniProt-validated residue positions, a source-free residue-role assignment, and
source-free proton-transfer event-axis evidence. It explicitly forbids M-CSA
heldout mechanism text, curated heldout active-site roles, labels/outcomes,
source IDs, target names, and EC/Rhea IDs as predictive inputs. It materializes
0 linker rows.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker_audit_current702_20260602.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker_audit_current702_20260602.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_current702_20260602.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_current702_20260602.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_current702_20260602.json`,
and
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_current702_20260602.md`.

## 2026-06-02: P0 Approved Rows Materialized Train/Cal-Only; No-Template Rerun Now Blocks On Calibration Review

Decision: materialize only the three reviewer-approved P0 M-CSA-only source
rows (`m_csa:5`, `m_csa:11`, and `m_csa:169`) into a partial train/cal
row-specific bond/proton/electron feature sidecar. The sidecar copies only
label-stripped event-count/boolean features from approved source evidence; it
does not copy draft rows, heldout rows, source text, source IDs, reviewer IDs,
labels, fingerprints, or accessions as predictive features. No model weights,
thresholds, labels, registries, ontologies, imports, or production scorers
changed.

Result: all three approved rows are assigned to the train split, so the partial
feature surface is materialized but not sufficient for a no-template centroid or
residual rerun. It contains 3 feature rows and 0 calibration rows, with approved
event counts of 3 `bond_broken`, 2 `bond_formed`, 2 `electron_transfer`, and 2
`proton_transfer` events. A strict train/cal feature guardrail audit passes with
0 critical violations and confirms the predictive payload is restricted to
numeric/boolean event features. The remaining 12 P0 source-evidence rows stay
draft and non-consumable.

Consequence / next gate: the coverage-gap audit identifies four
calibration-assigned draft rows as the next manual review gate:
`m_csa:186`, `m_csa:147`, `m_csa:6`, and `m_csa:133`. `m_csa:186` and
`m_csa:147` also add the currently unmaterialized `bond_order_changed` event
type. A manual calibration review packet now carries those four rows and 16
event-review records, but records no approvals. After human approve/rewrite/reject
decisions are copied into the source-evidence sidecar, rerun the strict
sidecar/readiness/materialization artifacts before attempting the no-template
centroid pilot or the out-of-span residual on the richer feature surface.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_calibration_review_packet_current702_20260601.json`,
and
`work/mechanism_feature_row_specific_bond_change_p0_calibration_review_packet_current702_20260601.md`.

## 2026-06-02: P0 Rhea-Absent Rows Approved As M-CSA-Only Source Evidence With Split-Filtered Use Only

Decision: approve all three P0 row-specific bond-change rows that official
Rhea/UniProt lookup could not Rhea-resolve: `m_csa:5`, `m_csa:11`, and
`m_csa:169`. The reviewer decision is `approve_m_csa_only_source_evidence`,
with reviewer provenance recorded as Vivek Vardhan Arrabelli in the P0 source
evidence sidecar. UniProt confirms matching EC activity for all three rows, but
Rhea returns no EC/accession cross-reference; these are explicitly
reviewer-approved M-CSA-only source-evidence rows, not Rhea-resolved rows.

Consequence: the strict sidecar audit now passes with 3 approved consumable rows
and 12 remaining draft rows. The Rhea lookup manifest has 0 remaining rows, the
Rhea consumption audit reports 3 reviewer-approved M-CSA-only rows, and the
reviewer decision matrix is copy-ready for those three rows. Full 15-row
no-template feature-contract refresh remains blocked until the remaining draft
rows are reviewed, but partial train/cal feature materialization is allowed for
only the three approved rows.

Load-bearing guardrail: these bond-change/proton/electron features are
M-CSA-derived. They are safe only because the feature materialization path must
filter to train/cal rows and keep the 140 heldout M-CSA rows excluded from
training and threshold selection. Do not train, calibrate, or tune deployment
thresholds on heldout M-CSA rows using these features.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_rhea_resolution_consumption_audit_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_reviewer_decision_matrix_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit_current702_20260601.json`,
and
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit_current702_20260601.json`.

## 2026-06-02: Lever 2 Integrated — Two Independent Builds Become One Result; The Closed-Form Residual Is The Live Deployable Signal, The Centroid Pilot's Discipline And Feature Track Are Retained

Decision: integrate the two independent Lever 2 implementations rather than
choosing one and discarding the other. The closed-form information-preserving
metric (the "residual line") and the standardized nearest-primary centroid pilot
(the "centroid line") are both agent-built, treated as equals, and kept; the
genuine advancement of each is carried forward into a single Lever 2 result.

Synthesis:
- Consolidated negative (robust precisely because two independent builds agree):
  a learned or standardized embedding over the CURRENT feature surface does not
  deployably beat the geometry baseline. The metric's predeclared primary is a
  clean negative (AUC 0.616 vs top1_score 0.757). The centroid pilot's strong
  numbers (calibration AUC 0.948, heldout 0.881) are reaction-template dependent;
  its deployment-valid no-template ablation is at chance (heldout AUC 0.489).
  Neither full-contract score is deployment evidence.
- Live deployable signal: the residual line's unsupervised out-of-atlas-span
  residual is the surviving win — deployment-valid (sequence-only), confirmed
  (PCA cutoff-robust sweep + a held-out-from-design confirmatory split with a
  label-permutation null, p=0.0005), and integrated into the per-channel rule
  gate for a +0.076 confounded-safe OOS-abstain lift at the >=85% retention floor.
  The residual threshold remains research-grade pending deployable calibration.
- Retained from the centroid line (genuine advancements, not discarded): (1) its
  train/cal/heldout fitting discipline (fit on 418 train rows, threshold on 106
  calibration rows, once-only heldout readout) becomes the standard the residual's
  deployable calibration must meet; (2) the audited mechanism-feature contract
  surface and the P0 source-evidence sidecar / bond-change / proton-transfer /
  electron-flow feature-materialization track (with Rhea provenance) is the kept
  forward path to the genuinely-new mechanism feature.

Consequence / unified next: materialize the row-specific bond-change/proton/
electron features (resolve open Rhea rows `m_csa:11`, `m_csa:169`, `m_csa:5` and
reviewer provenance first), then re-run BOTH the no-template centroid pilot and
the out-of-span residual on that template-free surface under the centroid line's
train/cal/heldout discipline; give the residual a deployable calibration; and
close a deployment-valid confounded-safe channel (Lever 3). No code or artifacts
from either build were removed.

Work/artifacts: `work/mechanism_feature_embedding_current702_20260601.md`,
`work/mechanism_feature_residual_robustness_current702_20260601.md`,
`work/mechanism_residual_gate_integration_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json`,
`artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`.

## 2026-06-02: Confirmed Residual Adds A Confounded-Safe Operating-Point Lift To The Rule Gate (Research-Grade Threshold)

Decision: integrate the now-confirmed out-of-span residual into the per-channel
RULE gate as a third orthogonal lift channel and measure its marginal
operating-point contribution, rather than promoting it on AUC alone. The deployed
rule (geometry leads; cofactor adds abstentions only where its signature is weak)
is extended with a residual term carrying the SAME confounded-safe guard:

    abstain = geom < tg
              OR (cof < signature AND cof < tc)              # cofactor-agnostic-lift
              OR (cof < signature AND residual_novelty >= tr)  # residual-agnostic-lift

The residual is concentrated on the cofactor-agnostic majority and is NOT
confounded-safe (confounded AUC ~0.66 vs geometry 0.84), so gating it on
`cof < signature` keeps confounded rows decided by geometry alone. The
three-channel search space contains the two-channel gate (a high tr disables the
term), so a three-channel optimum can never be worse; the question was the lift
magnitude and confounded-safety preservation. Predeclared PASS = residual adds
OOS-abstain-recall AND preserves confounded-abstain-recall, at the operative
retention floor.

Result (deployment pool 47 in-scope / 79 OOS; 6 confounded / 73 agnostic; residual
channel all-OOS AUC reproduced live at 0.72098, matching the embedding eval). The
operative floor is >=85% in-scope retention: neither gate has a >=90% point because
the agnostic-lift terms unavoidably abstain too many low-cofactor in-scope rows at
the minimum threshold. At >=85% retention the two-channel gate abstains on 0.3038
of OOS (confounded 0.1667, agnostic 0.3151); adding the residual-agnostic-lift
raises OOS-abstain-recall to 0.3797 (+0.0759), ENTIRELY from the agnostic subset
(0.3151 -> 0.3973), with the confounded subset UNCHANGED at 0.1667 -- the
predeclared PASS holds (adds lift, confounded-safe). The confounded subset remains
the binding constraint, exactly motivating the Lever 3 fold channel.

Deployability (honest scope). tg and tc are thresholds on calibrated [0,1]
confidences and are deployable constants; the residual threshold tr is NOT. 100% of
held-out rows sit above the atlas residual maximum, so the residual's
atlas-percentile calibration SATURATES and the signal survives only in raw/relative
form -- tr is an eval-pool-relative RESEARCH operating point (a calibration-free ROC
sweep over observed residual values), not a production threshold. The reported lift
is the residual's marginal operating-point contribution; a deployable residual
calibration, or the Lever 4 expanded family set, is required before production
promotion. An exploratory ungated variant (residual firing on all rows) is recorded
for transparency but is not the predeclared agnostic-lift form.

Consequence: the confirmed residual translates into a real, confounded-safe
operating-point lift on the cofactor-agnostic majority (+0.076 OOS-abstain-recall at
85% retention), banking the Lever 2 win at the gate level -- but it does NOT close
the operational gap, because the safety-critical confounded subset is unmoved and
the residual threshold is not yet deployable. The next gains must come from a
confounded-safe channel (Lever 3, deployment-valid fold/structure novelty) and a
deployable residual calibration or the wider Lever 4 surface. No labels, registries,
ontologies, splits, thresholds, or production scorers changed; the residual is
sequence-only and atlas-only-fit, M-CSA rows are eval-only, the deployable
thresholds are untuned, and the cofactor channel is read-only for stratification.

Reproduce: `PYTHONPATH=src python -m catalytic_earth.cli
eval-mechanism-residual-gate-integration`. Module:
`src/catalytic_earth/mechanism_residual_gate_integration.py`. Tests:
`tests/test_mechanism_residual_gate_integration.py` (3 fast + 1 slow integration
gated behind `CATALYTIC_RUN_SLOW`). Artifacts:
`artifacts/v3_mechanism_residual_gate_integration_current702_20260601.json`,
`work/mechanism_residual_gate_integration_current702_20260601.md`.

## 2026-06-01: Out-Of-Span Residual Survives The Cutoff-Robustness And Predeclared Confirmatory Tests

Decision: before treating the out-of-atlas-span residual (the AUC 0.721 Lever 2
lead) as more than an eval-pool hypothesis, run the two checks that were
predeclared as its gate -- a PCA variance-cutoff robustness sweep (leakage/overfit
test) and a held-out-from-its-own-design confirmatory split -- with the pass/fail
bars, fold salt, and permutation seed all fixed a priori. Both pass, so the
residual graduates from exploratory readout to a confirmed candidate third
orthogonal lift channel.

Robustness sweep (leakage/overfit). The residual is the representation energy
outside the atlas PCA span, and the span size is a fixed variance cutoff. Sweeping
it (95% / 97% / 99%) re-derives the residual off a single shared atlas
eigendecomposition (an anchor assertion confirms the 99%/128-dim point reproduces
the committed 0.72098). Deployment-pool all-OOS AUC is 0.7072 (95%, 81-dim span),
0.7215 (97%, 98-dim), 0.7210 (99%, 128-dim cap, 0.9891 variance) -- range 0.0143,
inside the predeclared <=0.05 band; all three >=0.65; and agnostic-subset AUC
exceeds confounded-subset AUC at every cutoff. Note the 99% target is cap-limited
to 128 dims, so the 95%/97% points genuinely shrink the span (81/98 dims) -- the
sweep tests real span-size sensitivity, not a no-op. S1/S2/S3 all hold: the 0.721
is NOT an artifact of the chosen cutoff.

Confirmatory split (held out from the lead's own design). The lead was surfaced on
the whole deployment pool, so its 47/79 sample could be lucky. The held-out rows
were partitioned into two folds by a salted hash of the entry id
(`sha256('residual_confirm::'+id) % 2`) -- a split independent of the residual
values and of how the lead was found -- with fold 1 reserved as the confirmation
fold and the pass criteria committed before reading it. Significance is a
label-permutation null (2000 shuffles, seed 20260601) over the fixed residual
scores. The confirmation fold (29 in / 30 OOS) scores AUC 0.7885 at permutation
p=0.0005; the design-echo fold (18/49) scores 0.654 at p=0.029; pooled 0.721 at
p=0.0005. H1 (confirmation AUC>=0.65 AND p<0.05), H2 (both folds AUC>=0.60), and
H3 (confirmation agnostic AUC >= confounded AUC) all hold: the separation is real
and significant on data that played no role in the discovery, and the
cofactor-agnostic directional structure replicates.

Consequence: the out-of-span residual is a stable, generalizing novelty signal,
not a cutoff/eval-pool artifact -- it is promoted to a candidate third orthogonal
lift channel (geometry-led gate + cofactor-agnostic-lift + residual-agnostic-lift)
for predeclared threshold work. It remains NOT confounded-safe (confounded AUC
~0.66 vs geometry 0.84), so it must still be paired with a confounded-safe channel
(Lever 3, fold) before any threshold promotion -- the confirmatory test validated
the lift, not standalone gating. Lever 4 (an expanded family set) is the stronger
confirmation surface but is a proposal only today; this test used the design-split
route on the existing eval pool and should be re-run once an expanded set is
materialized. No labels, registries, ontologies, splits, thresholds, or production
scorers changed; the atlas-only fit and M-CSA-eval-only constraints are preserved,
and the fold split is independent of the residual scores.

Reproduce: `PYTHONPATH=src python -m catalytic_earth.cli
eval-mechanism-residual-robustness`. Module:
`src/catalytic_earth/mechanism_feature_residual_robustness.py`. Tests:
`tests/test_mechanism_feature_residual_robustness.py` (8 fast + 1 slow integration
gated behind `CATALYTIC_RUN_SLOW`). Artifacts:
`artifacts/v3_mechanism_feature_residual_robustness_current702_20260601.json`,
`work/mechanism_feature_residual_robustness_current702_20260601.md`.

## 2026-06-01: Lever 2 Learned Mechanism-Feature Embedding Is A Clean Negative With An Out-Of-Span Residual Lead

Decision: implement Lever 2 (a learned mechanism-feature embedding) as a
closed-form, information-preserving supervised metric rather than a trainable
network, and report the result honestly at the operating point. The space is
sequence-only (ESM2-150M), fit ONLY on the in-distribution atlas: robust
standardize (atlas median/IQR) -> PCA over the atlas span (keep >=99% atlas
variance, capped at 128 dims; here 128 dims capturing 0.9891) -> within-class
whitening (a regularized full-rank Mahalanobis metric, fixed 0.10 shrinkage,
condition number 99.4). All hyperparameters are fixed a priori, NOT tuned on
heldout. A trainable GNN/classifier was explicitly rejected for this lever: the
supervised surface is only 184 atlas rows across 7 represented classes (the 8th
fingerprint, `radical_sam_enzyme`, has zero in-distribution rows; classes range
1-66 rows), there is no deployment-valid per-residue graph on disk, the
no-heldout-tuning guardrail forbids validation-based training, and a
high-capacity discriminative model worsens novelty by pulling OOS confidently
onto class manifolds.

Result (deployment pool: 47 in-scope / 79 OOS; 6 confounded / 73 agnostic;
baseline geometry top1_score reproduced live at AUC 0.757). The PREDECLARED
primary signal (equal-weight percentile mean of nearest-prototype, kNN-density,
and out-of-span residual) does NOT beat the baseline: AUC 0.616 and
OOS-abstain-recall 0.165 at >=90% retention vs 0.757 / 0.215. The supervised
whitening DISTANCE signals (prototype 0.606, kNN 0.613) are near the bare-PLM
level, confirming that discriminative reshaping is the wrong lever for novelty
(the linear discriminant-energy signal was already at chance, AUC 0.524). The
one genuinely new, orthogonal signal is the UNSUPERVISED out-of-atlas-span
residual (sequence-representation mass outside the directions known mechanism
chemistry occupies): AUC 0.721, and at the operating point it abstains on 0.241
of OOS at >=90% retention -- ABOVE the geometry baseline's 0.215 -- concentrated
on the cofactor-agnostic OOS majority. It is NOT safe on the safety-critical
cofactor-confounded subset (confounded abstain-recall 0.333 vs baseline 0.500;
confounded AUC 0.663 vs 0.840), so it is a COMPLEMENTARY LIFT channel, not a
replacement gate -- the same role the cofactor channel plays. The predeclared
percentile combiner washes out the residual (every held-out row sits below the
atlas residual distribution, so its atlas-percentile saturates to 0); the
residual carries signal only in RAW form and must be used as its own channel.

Consequence: Lever 2 does not by itself make de novo abstention operational, and
that is a valid, expected outcome cleanly reported. The actionable lead is the
out-of-span residual as a third, orthogonal lift channel (geometry-led gate +
cofactor-agnostic-lift + residual-agnostic-lift), to be validated with a
PREDECLARED confirmatory test (not the exploratory readout here) and paired with
a confounded-safe channel before any threshold promotion. The committed row-keyed
learned embedding (702 rows, 128-d whitened coords + residual) is reusable for
downstream de novo work. No labels, registries, ontologies, splits, thresholds,
or production scorers changed; M-CSA heldout rows were eval-only, never trained.

Reproduce: `PYTHONPATH=src python -m catalytic_earth.cli
eval-mechanism-feature-embedding`. Module:
`src/catalytic_earth/mechanism_feature_embedding.py`. Tests:
`tests/test_mechanism_feature_embedding.py` (10 fast + 1 slow integration gated
behind `CATALYTIC_RUN_SLOW`). Artifacts:
`artifacts/v3_mechanism_feature_embedding_eval_current702_20260601.json`,
`artifacts/v3_mechanism_feature_embedding_current702_20260601.jsonl`,
`work/mechanism_feature_embedding_current702_20260601.md`.
## 2026-06-01: Mechanism-Feature Embedding Pilot Is Implemented, But Template-Dependent

Decision: move the learned mechanism-feature lane from a no-fit scaffold to a
real train/cal-only pilot. The pilot consumes the audited
`v3_mechanism_feature_embedding_feature_contract_current702_20260601.json`
surface, fits standardized nearest-primary centroids on the 418 assigned train
rows, and selects the operating threshold only on the 106 assigned calibration
rows. No heldout rows are used for fitting, threshold selection, or evaluation;
no labels, registries, ontologies, imports, production scorers, or production
thresholds changed.

Result: the full contract variant reaches calibration AUC `0.948491` for
primary-vs-OOS nearest-primary similarity and abstains on 100% of calibration
OOS rows at 91.43% primary retention. The stricter
`no_reaction_template_ablation` drops to calibration AUC `0.549698` and 14.08%
OOS abstention at the same retention target.

Follow-up: materialize the same feature surface for heldout rows and apply the
train-fit/calibration-thresholded pilot once. Existing sidecars cover 132/140
heldout rows; 8 remain blocked by accession-compatible role-graph gaps. The
full-contract heldout readout reaches AUC `0.8812` and abstains on 100% of
ready OOS rows, but retains only 75% of ready primary rows at the
calibration-selected threshold. The no-template ablation is near chance on
heldout with AUC `0.488591` and 9.52% OOS abstention at 85.42% primary
retention.

Consequence: treat the pilot as implemented but not yet scientifically
sufficient. The strong full-contract result is largely reaction-template
dependent; the next useful mechanism-feature work is to materialize
row-specific bond-change, proton-transfer, and electron-flow evidence. Do not
cite the full-contract train/cal or heldout scores as deployment evidence.

Artifact:
`artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json`;
`artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`.

## 2026-06-01: Fold-Augmented Threshold Contract Selects Thresholds On Train/Calibration Rows, Not Heldout

Decision: promote the fold-augmented heldout-only diagnostic into a bounded
thresholding contract. The run used deterministic, fingerprint-stratified
partitioning over the in-distribution predicted atlas rows: 134 train targets and
34 calibration queries. AlphaFoldDB v6 CIFs were materialized transiently, and
Foldseek exact TM scoring was run only for the 34 calibration queries against the
133 available train-target CIFs. The resulting small TSV and parsed
JSON/report are committed; persistent coordinate files are not. No label,
registry, ontology, import, split, production scorer, or production threshold
changed.

Result: the primary predeclared channel, `combined_mean_geometry_fold`, selected
threshold `0.44155` at the >=90% calibration in-scope retention target, retaining
31/34 calibration rows (`0.9118`). Applying that threshold once to heldout rows
retains 45/47 in-scope rows (`0.9574`), abstains on 44/79 OOS rows (`0.557`),
and abstains on 5/6 cofactor-confounded OOS rows (`0.8333`). The
cofactor-including mean abstains on more all-OOS heldout rows (`0.6329`) but
still abstains on none of the cofactor-confounded OOS rows, matching the earlier
safety warning.

Consequence: the fold-augmented gate now has a leakage-safe research threshold
contract rather than a post-hoc heldout threshold. It is still not an authorized
production threshold because train/cal provides in-scope retention calibration
only: the current predicted atlas does not include train/cal OOS negatives for
threshold optimization. Next work should either add a frozen train/cal OOS
negative surface for threshold selection or move to the mechanism-feature
embedding gap with this threshold contract as the current fold-aware baseline.

Artifacts:
`artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/in_distribution_atlas_self_vs_atlas.tsv`,
`work/fold_augmented_abstention_threshold_contract_current702_20260601.md`.

Follow-up: add a review-only matched-retention delta audit between the frozen
predicted-atlas geometry operating grid and the frozen fold-augmented operating
grid. At the 90% in-scope-retention diagnostic, fold augmentation lifts OOS
abstention from `0.2278` to `0.7722` and cofactor-confounded OOS abstention
from `0.3333` to `0.8333`. This comparison reads existing heldout diagnostic
artifacts only and does not select, tune, or promote a threshold.

## 2026-06-01: Fold-Augmented Research Gate Applied To Review-Only Family Panels

Decision: add a downstream readout that applies the already selected
OOS-calibrated `combined_mean_geometry_fold` research threshold to the seven
review-only family-expansion evidence packets. This consumes the
research-sufficient 71/76 train/cal OOS-negative surface decision and the
family-panel coverage audit. It does not select thresholds on family-panel rows,
fit a model, promote rows, import labels, or mutate registries/ontologies.

Result: after the M-CSA repair follow-up, 12/22 review rows are score-complete
for the primary geometry-plus-predicted-fold channel. Of those, 6 remain
non-abstained at the fixed `0.44155` research threshold: `m_csa:267`,
`m_csa:131`, `m_csa:750`, `m_csa:551`, `m_csa:132`, and `m_csa:116`. Six
score-complete rows abstain, including `m_csa:973` after joining its frozen
train/calibration fold score, and 10 rows remain blocked by missing predicted
active-site geometry evidence. Those 10 rows now have source-backed
AFDB-vs-predicted-atlas fold scores from the P0/P1 materialization follow-up.

Consequence: the next review work should keep the six source-checked
non-abstained boundary rows review-only, while working the 10 remaining
primary-channel-missing rows through source-free predicted-geometry sidecars.
This readout is review-only and must not be interpreted as a family promotion,
production threshold, or training signal.

Follow-up: the rank-1 queue row, `m_csa:267`, was source-checked against frozen
local M-CSA graph and label artifacts. The check keeps it as a review-only OOS
boundary control: local mechanism evidence supports dihydrodipicolinate
synthase lysine Schiff-base aldol/cyclization chemistry, not a current
seed-family promotion.

Second follow-up: the rank-2 row, `m_csa:131`, was source-checked against
frozen local M-CSA graph and label artifacts. The check confirms direct flavin
monooxygenase/oxygen-transfer support for the existing secondary-probe row, but
does not authorize primary FMO promotion while the project-state FMO blockers
remain active.

Third follow-up: the rank-3 row, `m_csa:750`, was source-checked through the
current registry and the existing `m_csa:750` revision artifact. The check
keeps it as OOS/boundary evidence and a future radical flavin/Fe-S dehydratase
candidate, not a current v1 flavin, FMO, cobalamin, or radical-SAM promotion.

Fourth follow-up: the rank-4 row, `m_csa:551`, was source-checked through
frozen M-CSA graph evidence and the existing FMO local-candidate adjudication.
The check confirms mechanism-clean future FMO support, but the prior
adjudication explicitly blocks import and registry edits, so no label or
promotion state changed.

Repair follow-up: apply the existing accession-compatible predicted-geometry
repair policy to the two queued M-CSA rows. `m_csa:132` switches from manifest
accession `P07739` to real-sequence accession `P07740`, resolves 5/5 catalytic
positions, and scores nearest-atlas Foldseek/TM `0.6879`. `m_csa:116` uses the
manifest accession-compatible residue subset on `Q2RSB2`, resolves 5/5 scored
positions, and scores nearest-atlas Foldseek/TM `0.5417`. Both become
score-complete and non-abstained at the fixed research threshold. The refreshed
missing queue now has 10 rows, all secondary-probe or external/placeholder rows
that required source-backed sidecars and coordinate materialization before the
later P0/P1 materialization follow-up.

Fifth/sixth follow-up: the newly non-abstained repaired M-CSA rows were
source-checked from frozen local graph, registry, repair, and readout artifacts.
`m_csa:132` is confirmed only as secondary FMO support after geometry repair,
with no primary FMO promotion. `m_csa:116` stays a review-only OOS
NAD(P)+-transhydrogenase/hydride-transfer control. No label, registry, import,
threshold, split, or production scorer changed.

Queue follow-up: add and refresh a separate review-only materialization queue
for the family-panel rows that lack primary geometry-plus-predicted-fold channel
scores. The first queue/diagnosis showed `m_csa:973` already had frozen
train/calibration fold evidence in the threshold contract. The family-panel
readout now joins that score without rerunning Foldseek/TM, so `m_csa:973`
becomes score-complete and abstained at the fixed research threshold
(`combined_mean_geometry_fold=0.41` versus `0.44155`). After the M-CSA repair,
the remaining queue has 10 rows, all secondary-probe or external/placeholder
rows requiring source-backed row sidecars and coordinate materialization.

FMO subtype follow-up: add and refresh a review-only subtype/hard-negative
packet for the FMO lane. It keeps `m_csa:131` and repaired `m_csa:132` as
secondary-probe support, `m_csa:551` and `m_csa:973` as future support only,
and `m_csa:750` as radical flavin/Fe-S boundary negative. No row is
import-ready or registry-edit-ready, so primary FMO promotion remains blocked.

Materialization-plan follow-up: stage the next review-only carryover for the
10 remaining missing primary-channel rows without fetching coordinates or
scoring them. The plan selects source-backed representatives from frozen
artifacts: Q59490 for `secondary_probe::cobalamin_radical_rearrangement`,
A0A1M6T2I7 for `secondary_probe::radical_sam_enzyme`, Q6NSJ0 for
`external_glycoside_panel`, and the seven prior-resolved `mh_*` rows from the
external identifier scout. It records exact PDB/AFDB candidate commands and
sidecar fields while keeping every row review-only and non-countable.

P0/P1 materialization follow-up: materialize and hash the selected PDB
coordinates plus AFDB-v6 predicted coordinates for all 10 queued source-backed
representatives, then run Foldseek exact TM against the frozen predicted
in-distribution atlas. All 10 rows now have real predicted-fold hits, including
`0.4655` for Q59490, `0.7039` for A0A1M6T2I7, `0.6259` for Q6NSJ0, and
metal-hydrolase/boundary nearest TM scores from `0.5936` to `1.004`. The family
packets, readout, missing-channel queue, and diagnosis were refreshed. The rows
remain primary-channel incomplete because source-free predicted active-site
geometry top1 scores are still missing. No labels, registries, imports,
thresholds, splits, or production scorers changed.

Source-free geometry follow-up: validate that the real fold channel and the
10-row source-backed materialization are not runtime-blocked, then stage the
source-free predicted-geometry sidecar manifest. All 10 rows have AFDB-v6 CIF
hashes and source-backed Foldseek/TM scores, but 0/10 have approved source-free
active-site locator sidecars. The blocker-clearing attempts checked existing
predicted-geometry retrieval rows, current702 label-manifest membership,
source-backed sidecars, and coordinate/Foldseek runtime state. The result is a
semantic blocker, not a Foldseek or coordinate blocker: these rows are
secondary/external review rows outside the current702 graph-backed residue
locator surface. A companion strict locator schema now requires at least two
source-free sequence-position residue locators per row and explicitly forbids
entry names, EC/Rhea identifiers, source prose, mechanism text, labels,
benchmark roles, and panel IDs as predictive geometry features. No labels,
registries, imports, thresholds, splits, or production scorers changed.
The companion schema audit is staged and currently reports 0/10 locator
sidecars present, with `locator_sidecar_missing` as the only critical violation
class. A materialization plan now records the exact locator sidecar paths and
rerun commands for all 10 rows; eight rows start from a
structure-local-ligand-geometry policy candidate, while `mh_067` and `mh_068`
carry same-accession current702 geometry matches and require split-safe
train/cal-template checks before any locator use. A template-only bundle now
stages the 10 planned locator sidecar shells outside the audited locator
directory. The templates are review-only, contain no residue locators, create no
audited sidecars, and are not ready for predicted-geometry scoring.

Candidate-audit follow-up: a coordinate-only candidate extractor now stages
review-only locator candidates outside the audited locator directory. It uses
only selected mmCIF atom coordinates, residue/ligand comp IDs, atom names,
distances, and `_struct_ref_seq` accession mappings; no source prose, labels,
EC/Rhea IDs, or mechanism text are admitted as predictive features. Eight rows
have at least two candidate locators from selected-structure ligand/metal
contacts, and six of those rows have all candidate positions prevalidated
against matching UniProt mapping metadata. Q59490 and C7C422 remain blocked
because their selected PDB coordinates expose no non-water/non-metal ligand
candidate under this extractor; Q79MP6 and P0A6P9 still need UniProt
position-validation review. No candidate is scoring-ready: all still require
manual forbidden-feature review, and `mh_067`/`mh_068` need a split-safe
template check before any sidecar can be copied to the audited locator
directory.

Candidate-integrity follow-up: audit the staged locator candidate sidecar files
against the candidate-audit payload before manual review. All 10 candidate files
are present, payload-matched, outside the audited locator directory, and
guardrail-clean; 0 are scoring-ready. This keeps the next step as manual
scientific/forbidden-feature review rather than predicted-geometry scoring.

Review-queue follow-up: rank the candidate sidecars by the next validation
blocker. Three rows are priority-1 for manual forbidden-feature review
(`mh_066`, `mh_073`, and `secondary_probe::radical_sam_enzyme`). Q6NSJ0 needs
ligand-specificity review because the selected ligand candidate is acetate;
P00918/P15289 need split-safe template checks; Q79MP6/P0A6P9 still need UniProt
position-validation review; Q59490/C7C422 require a new source-free locator path
or alternate coordinate. The queue still creates no audited locator sidecars and
scores no predicted geometry.

Manual-review packet follow-up: combine candidate sidecar SHA-256s, integrity
status, review priority, and per-row checklists into a single handoff artifact.
The packet is ready for human review with 10 integrity-passed rows, three
priority-1 manual review rows, 0 copy-ready rows, and 0 scoring-ready rows.

Priority-1 preflight follow-up: dry-run the three priority-1 manual-review
rows (`mh_066`, `mh_073`, and
`secondary_probe::radical_sam_enzyme`) against the locator schema, candidate
guardrails, and coordinate-contact plausibility checks. All three pass this
automation preflight, with `mh_073` flagged because it sits exactly at the
minimum two-locator floor. This does not approve or copy sidecars: human
approval remains required before rewriting any locator into the audited
directory and rerunning the schema audit.

Blocked-row rescue follow-up: inspect the two source-free locator rows blocked
by no non-water/non-metal ligand candidate. Both selected local coordinates
contain only water HETATMs. `mh_064` has five frozen source alternate PDB IDs
from the existing identifier scout (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, and
`3SPU`), so the manifest stages exact fetch commands pending manual approval.
Q59490 has only `1L1L` in the frozen cobalamin blocker artifact, so it remains
blocked on a new nonlabel locator strategy or an explicitly authorized
alternate source row. No coordinate fetch, locator copy, predicted geometry
scoring, label/import, registry, ontology, split, threshold, or production
scorer change occurred.

Approved-locator scoring follow-up: after human approval moved `mh_066`,
`mh_073`, and `secondary_probe::radical_sam_enzyme` into the audited
source-free locator directory, run a bounded review-only predicted-geometry
retrieval over those three rows. The run uses only approved sequence-position
locators, residue codes, generic locator role hints, local AFDB-v6 CIFs, and
geometry-derived pocket context; it does not use source prose, entry names,
panel IDs, labels, EC/Rhea IDs, benchmark roles, heldout training, or new
downloads. All three rows resolve at least two predicted residues and receive
top1 geometry scores, and all three are retained when joined to their existing
source-backed fold scores under the fixed `combined_mean_geometry_fold`
research threshold. The review-only family-panel readout was refreshed to
consume those scores: 15/22 rows are now primary score-complete, 9 are
non-abstained, 6 abstain, and 7 remain missing primary-channel scores. Seven
rows remain blocked on approved source-free locators. No labels, imports,
registries, ontology entries, splits, thresholds, model weights, production
scorers, source fetches, or coordinate downloads changed.

Source-check preflight follow-up: package those three newly non-abstained
source-free geometry rows for local review before any family-panel action. The
preflight keeps all three rows in `hold_review_only_pending_source_check`,
identifies `mh_066` as the first source-check target because its geometry and
fold fingerprints agree, and flags `mh_073` plus
`secondary_probe::radical_sam_enzyme` for mechanism-locus and duplicate/leakage
review. No source adjudication, family admission, labels, imports, registries,
thresholds, splits, or production scorers changed.

`mh_066` source-check follow-up: complete a frozen-local review-only source
check for the IMP-1 metallo-beta-lactamase row. The source-free geometry and
predicted-fold channels agree on `metal_dependent_hydrolase`, local 1DD6
coordinate metadata supports a zinc metallo-beta-lactamase hydrolase context,
and current702 has no exact P52699 accession duplicate. The nearest predicted
fold atlas row is still an occupied B1 beta-lactamase seed (`m_csa:15`), and
the external row lacks an extracted row-specific bond-change/residue-role
sidecar plus duplicate/split/expert admission. Keep `mh_066` review-only and
non-countable; do not promote or import it without a future explicitly
authorized admission packet.

`mh_073` source-check follow-up: complete a frozen-local review-only source
check for the H-Ras row. Local 121P coordinate metadata supports an Mg/GTPase
nucleotide locus, the external panel predeclares it as a hard negative against
Mg/nucleotide leakage, and the source-free geometry channel disagrees with the
metal-hydrolase fold hit. The nearest predicted-fold atlas row is `m_csa:535`,
a current702 GTPase-like seed currently labeled `metal_dependent_hydrolase`,
which makes `mh_073` a boundary/leakage diagnostic rather than promotion
evidence. Keep it review-only and non-countable unless a future authorized
GTPase-boundary policy reopens current702 scope.

Radical-SAM source-check follow-up: complete a frozen-local review-only source
check for `secondary_probe::radical_sam_enzyme` using the freeze artifact,
local 8VPO coordinate metadata, the approved SF4-contact locator, and current
family-panel readouts. The evidence supports a TigE radical-SAM/Fe-S locus, but
the source-free geometry channel calls `metal_dependent_hydrolase` and the
nearest predicted-fold atlas row is the PLP-dependent seed `m_csa:358`.
Current702 has no exact A0A1M6T2I7 duplicate and only one radical-SAM secondary
probe row, so this is useful radical/Fe-S panel evidence but remains
review-only and non-importable pending row-specific bond-change, duplicate/split
review, and expert admission.

Remaining-locator queue follow-up: classify the seven family-panel rows still
blocked on approved source-free active-site locators after the three source
checks. All seven have AFDB coordinate hashes and source-backed fold scores, but
none is scoring-ready. Two rows need UniProt position validation (`mh_065`,
`mh_072`), two need split-safe same-accession template checks (`mh_067`,
`mh_068`), one needs ligand-specificity review (`external_glycoside_panel`),
one has manually approved alternate-coordinate fetch commands but requires
approval before any fetch (`mh_064`), and Q59490 needs a new nonlabel locator
strategy or explicitly authorized alternate source row. No sidecars were copied,
coordinates fetched, geometry scored, labels/imports changed, or thresholds
touched.

UniProt-position validation follow-up: attempt the `mh_065`/`mh_072`
sequence-position validation using only frozen local candidate sidecars and
selected PDB mmCIF mappings. Both rows remain blocked because the selected PDB
`struct_ref` accessions do not match the source-row accessions: `1DDK` maps to
`Q932P5` rather than `Q79MP6`, and `1E9I` maps to `P08324` rather than
`P0A6P9`. The candidate contacts remain review evidence, but no source-free
locator sidecar can be copied and no predicted-geometry score can be produced
without an explicit representative-accession equivalence policy or a frozen
coordinate whose mapping matches the requested source accession.

Split-safe template follow-up: check `mh_067` and `mh_068` against the current702
manifest before any locator copy. Both candidates have validated
sequence-position locators, no forbidden source/label predictive fields, and
same-accession current702 matches that are in-distribution seed rows
(`m_csa:216` for P00918 and `m_csa:158` for P15289), not heldout rows. This
clears the split-safety question as review-only evidence, but it does not copy
sidecars or authorize predicted-geometry scoring; manual locator-copy approval
is still required before either row can enter the audited locator directory.

Ligand-specificity follow-up: review the `external_glycoside_panel` selected
coordinate ligand before any locator copy. The current candidate selected
acetate (`ACT`) in local unliganded MYORG structure `7QQF`; that ligand is too
nonspecific for a glycoside-hydrolase active-site locator. Frozen NAG contacts
exist in the same candidate extraction, but local annotations include
glycan/N-glycosylation context, so they are not an automatic catalytic-substrate
replacement. Keep the row blocked until a dedicated glycoside-ligand validator
or an explicitly approved substrate-complex coordinate is available.

No-ligand policy-blocker follow-up: isolate the remaining no-ligand/metal
source-free locator blockers. `mh_064` cannot proceed from selected structure
`3PG4`; it has five frozen alternate-coordinate fetch commands but those
require explicit approval before any download. Q59490 has no detected ligand or
metal site in selected `1L1L` and no frozen alternate PDB IDs, so it needs a
reviewed nonlabel locator strategy or approved alternate source row. No
coordinates were fetched, no locator sidecars were copied, and no scoring was
run.

Resolution-status follow-up: consolidate the seven unresolved source-free
locator blockers into one current status artifact. Automation discovery is now
complete for all seven, 0/7 are scoring-ready, and every remaining action is a
policy or human-review decision: accession equivalence or matching coordinates
for `mh_065`/`mh_072`, copy approval for `mh_067`/`mh_068`, ligand validator or
substrate coordinate for `external_glycoside_panel`, alternate-coordinate fetch
approval for `mh_064`, and a nonlabel locator strategy or alternate source row
for Q59490.

Integrity follow-up: index the current run's 10 new JSON artifacts and 10 work
reports in a parse/presence audit. The audit records no label/registry/ontology
mutation, no production-threshold mutation, no coordinate fetches, no model
fit, and no predicted-geometry scoring; validation results are captured for
pytest, unittest discovery, compileall, `validate`, and diff-check.

Artifacts:
`artifacts/v3_fold_augmented_family_panel_research_readout_current702_20260601.json`,
`work/fold_augmented_family_panel_research_readout_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_queue_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa267_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa267_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa131_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa131_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa750_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa750_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa551_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa551_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.json`,
`work/fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa132_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa132_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa116_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa116_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json`,
`work/fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json`,
`work/fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.md`,
`artifacts/v3_family_panel_source_backed_sidecar_materialization_plan_current702_20260601.json`,
`work/family_panel_source_backed_sidecar_materialization_plan_current702_20260601.md`,
`artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601.json`,
`work/family_panel_source_backed_sidecar_materialization_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_retrieval_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_retrieval_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.json`,
`work/family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_uniprot_position_validation_mh065_mh072_current702_20260601.json`,
`work/family_panel_source_free_locator_uniprot_position_validation_mh065_mh072_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_split_safe_template_check_mh067_mh068_current702_20260601.json`,
`work/family_panel_source_free_locator_split_safe_template_check_mh067_mh068_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_ligand_specificity_review_external_glycoside_panel_current702_20260601.json`,
`work/family_panel_source_free_locator_ligand_specificity_review_external_glycoside_panel_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_policy_blockers_mh064_q59490_current702_20260601.json`,
`work/family_panel_source_free_locator_policy_blockers_mh064_q59490_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json`,
`work/family_panel_source_free_locator_blocker_resolution_status_current702_20260601.md`,
`artifacts/v3_current_run_artifact_integrity_audit_current702_20260601.json`,
`work/current_run_artifact_integrity_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_schema_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_schema_audit_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_schema_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_template_bundle_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_template_bundle_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_review_queue_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_review_queue_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.json`,
`work/family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.md`,
`artifacts/v3_fmo_subtype_hard_negative_packet_current702_20260601.json`,
`work/fmo_subtype_hard_negative_packet_current702_20260601.md`.

## 2026-06-01: Predicted-Structure Fold Channel Contract Audit Passes

Decision: add a strict validation layer for the already-scored AlphaFoldDB
predicted-structure Foldseek/TM channel rather than regenerating the scored
artifact. The audit checks frozen current702 row counts, parsed Foldseek TSV
coverage, source artifact hashes, guardrails, score ranges, expected command
tokens, and the allowed computed blockers. No label, registry, ontology, import,
split, threshold, production scorer, or scored fold-channel value changed.

Result: the contract audit passes with zero critical violations. It confirms
126/126 ok heldout rows have nearest-atlas Foldseek/TM hits, all six priority
cofactor-confounded OOS rows have parsed priority hits, and the only fold-channel
blockers are persistent coordinate-file provenance blockers. The all-heldout TSV
has 11,297 mapped pairs; the priority TSV has 402 mapped pairs.

Consequence: downstream fold-augmented gate work can treat the scored predicted
fold channel as validated for current702. Persistent predicted-CIF provenance is
still useful reproducibility infrastructure, but it is not a score-completeness
blocker under this contract.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json`,
`work/predicted_structure_fold_channel_contract_audit_current702_20260601.md`.

Reproduction-manifest follow-up: add a validation-only reproduction manifest
for the same scored channel. It records the 299 expected AFDB-v6 coordinate
paths across 293 deduplicated accessions, exact Foldseek rerun commands, scored
TSV SHA-256 hashes, contract/provenance audit hashes, and the single blocker
class `persistent_afdb_v6_coordinate_bundle_missing`. No coordinate download,
Foldseek/TM rerun, label, registry, ontology, import, split, threshold, or
production scorer change occurred.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json`,
`work/predicted_structure_fold_channel_reproduction_manifest_current702_20260601.md`.

Carryover-resolution follow-up: add a validation-only audit for stale
automation prompts that still ask to build or stage the predicted-structure fold
channel. It consumes the scored channel, contract audit, coordinate provenance
audit, reproduction manifest, predicted-atlas retrieval, and fold-level signal.
The audit confirms the requested fold-channel artifact/report are present,
126/126 ok heldout rows and 6/6 priority cofactor-confounded rows are scored,
the contract has zero critical violations, and no Foldseek/TM rerun is needed.
The remaining `persistent_afdb_v6_coordinate_bundle_missing` blocker is only for
byte-level reproduction.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_carryover_resolution_current702_20260601.json`,
`work/predicted_structure_fold_channel_carryover_resolution_current702_20260601.md`.

2026-06-02 persistence follow-up: materialized the exact AFDB-v6 coordinate
bundle recorded by the predicted-structure fold channel: 299 expected CIF paths
across 293 deduplicated accessions. No Foldseek/TM score was recomputed, no
threshold changed, and no label/import/registry surface changed. The fold-channel
manifest, contract audit, deployment-input audit, coordinate-provenance audit,
reproduction manifest, carryover-resolution audit, and confounded readiness
artifact were regenerated against the persisted bytes. The coordinate-provenance
gate is now complete, byte-level reproduction is ready, and Lever 3 deployment
closure remains blocked only by the five production blocker rows plus the
rejected fold-only escape hatch.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_coordinate_provenance_audit_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_carryover_resolution_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json`.

## 2026-06-01: Train/Cal OOS Negatives Add A Partial OOS Calibration Surface For The Fold-Augmented Gate

Decision: score the hash-selected in-distribution OOS calibration negatives
staged by the train/cal negative-surface manifest, then build a separate
OOS-calibrated research threshold contract. The run used frozen current702
inputs, transient AlphaFoldDB v6 CIF materialization under `/private/tmp`, exact
Foldseek/TM scoring against the threshold-contract train atlas, and the existing
selected organic cofactor sidecar. Heldout rows stayed final-only. No label,
registry, ontology, import, split, production scorer, or production threshold
changed.

Result: 71/76 selected calibration OOS candidates have full channel scores
(`predicted_geometry`, selected organic cofactor, and nearest-train Foldseek/TM).
Foldseek produced nearest-train hits for 75 candidates. The six
accession-compatible active-site mapping blockers (`m_csa:57`, `m_csa:106`,
`m_csa:178`, `m_csa:284`, `m_csa:314`, and `m_csa:503`) have been cleared with
bounded current702-safe accession/subset repair; `m_csa:284` uses `O66188` for
predicted geometry and the Foldseek query because the manifest accession
`O66186` has only one usable catalytic residue. `m_csa:78`/`P23007` still lacks
an AFDB query coordinate. The OOS-calibrated primary channel,
`combined_mean_geometry_fold`, keeps the same >=90% in-scope threshold,
`0.44155`, as the in-scope-only contract. At that threshold calibration OOS
abstain recall is 28/71 (`0.3944`), while heldout final readout remains
45/47 in-scope retained, 44/79 OOS abstained, and 5/6 cofactor-confounded OOS
abstained.

Consequence: the fold-augmented gate now has a real train/cal OOS-negative
surface, but it is partial and does not justify a production threshold. The next
decision is whether the 71-row surface is sufficient for a research operating
point or whether to clear the remaining five blockers first: AFDB coordinate
replacement for `m_csa:78`, source-geometry repair for `m_csa:204` and
`m_csa:531`, and active-site sidecars for `uniprot:P78549` and
`uniprot:Q3LXA3`. Four of the missing combined-channel rows have fold-only
scores and are preserved in a separate diagnostic salvage surface.

Artifacts:
`artifacts/v3_fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/train_cal_oos_negatives_vs_train_atlas.tsv`,
`artifacts/v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json`,
`artifacts/v3_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601.json`,
`artifacts/v3_fold_only_train_cal_oos_negative_surface_current702_20260601.json`,
`work/fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.md`,
`work/fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601.md`,
`work/fold_only_train_cal_oos_negative_surface_current702_20260601.md`,
`work/fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.md`.

## 2026-06-01: Partial Train/Cal OOS Surface Is Sufficient For The Research Contract

Decision: resolve the handoff question about whether to block downstream
fold-augmented research diagnostics on the remaining five train/cal OOS-negative
surface gaps. The decision artifact applies a bounded, explicit policy: at least
90% score-complete coverage, no unresolved accession-compatible mapping
blockers, OOS-calibrated contract total matching the score-complete rows, and no
movement in the primary threshold relative to the in-scope-only contract. No
label, registry, ontology, import, split, production scorer, or threshold value
changed.

Result: the 71/76 surface is sufficient for the current research contract with
blocker disclosure. Coverage is `0.934211`; the OOS-calibrated contract consumes
exactly 71 calibration OOS rows; all accession-compatible mapping blockers are
cleared; and the primary `combined_mean_geometry_fold` threshold remains
`0.44155`. The surface is not sufficient for production-like claims while
`m_csa:78`, `m_csa:204`, `m_csa:531`, `uniprot:P78549`, and
`uniprot:Q3LXA3` remain unresolved.

Consequence: future runs should proceed with downstream diagnostics using this
research contract and disclosed blockers, rather than redoing the sufficiency
decision. Clear the five blockers before making any stronger threshold claim.

Artifacts:
`artifacts/v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json`,
`work/fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.md`.

## 2026-06-01: Remaining Train/Cal OOS Blockers Require New Source Evidence Or Coordinate Policy

Decision: inspect the five remaining score-surface blockers after the research
sufficiency decision and record whether any can be cleared from frozen current702
inputs. No label, registry, ontology, import, split, threshold, production
scorer, active-site sidecar, or coordinate policy changed.

Result: no blocker can be safely cleared in-repo from current inputs. `m_csa:78`
still exposes only P23007 locally and the scorer already recorded AFDB v1-v6
404s; experimental PDB 1AL6 does not clear the deployment predicted-coordinate
requirement. `m_csa:204` has no catalytic residue nodes in the current graph.
`m_csa:531` has only one catalytic residue and remains below geometry
eligibility. `uniprot:P78549` and `uniprot:Q3LXA3` are UniProt-only external
hard negatives without current active-site sidecars. Four rows have fold-only
evidence and should remain fold-only until source-backed sidecars exist.

Consequence: proceed with the research-sufficient 71/76 surface for downstream
diagnostics. Clear the five blockers only after new source-backed active-site
evidence, an alternate predicted coordinate, or an explicitly authorized
experimental-coordinate-only policy exists.

Artifacts:
`artifacts/v3_fold_augmented_train_cal_oos_remaining_blocker_clearance_attempts_current702_20260601.json`,
`work/fold_augmented_train_cal_oos_remaining_blocker_clearance_attempts_current702_20260601.md`.

## 2026-06-01: Active-Site Role Graph Sidecar Closes One Mechanism-Feature Embedding Gap

Decision: materialize a normalized row-level active-site residue-role graph
sidecar from the frozen current702 manifest and existing M-CSA graph. This is a
feature-readiness artifact only: it does not fit a model, tune a threshold, edit
labels, import rows, or change registries.

Result: 656/702 current702 rows have an accession-compatible active-site role
graph. The sidecar normalizes 53 residue-role vocabulary terms and 669
same-entry role co-occurrence edges. Remaining gaps are not inferred here:
directed proton/electron-transfer edges and row-specific bond-change mappings
still need a source-backed sidecar before a learned mechanism-feature embedding
pilot. A companion reaction-center template sidecar row-aligns fingerprint-level
chemical operations and bond-change descriptors for 232 rows, but it remains
template evidence rather than row-specific reaction evidence.

Consequence: the learned mechanism-feature embedding plan has one concrete
row-level feature sidecar available for future train/cal-only pilots, but it is
not itself model evidence and must not be used to train on heldout rows.

Artifacts:
`artifacts/v3_mechanism_feature_active_site_role_graph_sidecar_current702_20260601.json`,
`artifacts/v3_mechanism_feature_reaction_center_template_sidecar_current702_20260601.json`,
`work/mechanism_feature_active_site_role_graph_sidecar_current702_20260601.md`,
`work/mechanism_feature_reaction_center_template_sidecar_current702_20260601.md`.

## 2026-06-01: Mechanism-Feature Sidecar Schema Audit Passes

Decision: add a strict schema and row-alignment audit over the two current
mechanism-feature sidecars: active-site residue-role graphs and reaction-center
templates. The audit validates one row per current702 manifest entry, split /
accession / fingerprint alignment, required keys, allowed status values,
internal role/residue counts, template status consistency, and source status.
No model was fit and no label, registry, ontology, import, threshold, split, or
sidecar value changed.

Result: the schema audit passes with zero critical violations. Both sidecars
cover all 702 manifest rows. The active-site sidecar has 656 ok role-graph rows,
42 accession-position blockers, one missing catalytic-residue-node row, and
three non-M-CSA rows. The reaction-center template sidecar has 232 template rows
and 470 OOS/unlabeled rows without mechanism-fingerprint templates. The learned
mechanism-feature embedding plan now records this schema audit and marks the
current sidecars schema-safe for train/cal-only pilots.

Consequence: the current mechanism-feature sidecars are validated for
train/cal-only embedding pilots as schema-safe inputs. The scientific feature
gap remains directed electron/proton-transfer edges and row-specific bond-change
evidence.

Follow-up: tighten the cofactor-catalytic-locus gap into a review-only schema
and materialization queue for `metal_ion_locus`, `cobalamin_locus`,
`radical_sam_locus`, and `iron_sulfur_locus`. The schema uses existing current702
geometry ligand context only: 176 rows have proximal metal context, 4 cobalamin,
8 SAM, and 17 Fe-S cluster context. No sidecar values were emitted yet; the next
safe implementation is a metal-ion locus sidecar with proximal versus
structure-wide-only status.

Second follow-up: materialize the first such sidecar, `metal_ion_locus`, for all
702 current rows from existing geometry ligand context only. It records 175 rows
with proximal metal context, 85 with structure-wide-only metal context, 422 with
no metal context, and 20 unsupported/missing-geometry rows. All records are
review-only and have `predictive_use_allowed=false` and `ready_for_label_import=false`.
A matching strict schema audit passes with zero critical violations.

Third follow-up: materialize and audit `cobalamin_locus` with the same
review-only pattern and explicit structure-wide-only guardrail. It records 4
proximal cobalamin rows, 678 no-context rows, 20 unsupported/missing-geometry
rows, and no structure-wide-only B12 rows in the current geometry source. The
schema audit passes with zero critical violations.

Fourth follow-up: materialize and audit `radical_sam_locus` and
`iron_sulfur_locus` separately, preserving SAM/Fe-S copresence as an explicit
row status. The radical-SAM sidecar records 8 proximal SAM rows, 2
structure-wide-only SAM rows, and 20 unsupported/missing-geometry rows. The
Fe-S sidecar records 17 proximal Fe-S rows, 11 structure-wide-only Fe-S rows,
and 20 unsupported/missing-geometry rows. Both remain review-only, keep all
predictive/import flags false, and pass strict schema audits with zero critical
violations.

Completion audit follow-up: validate that all four schema-named
cofactor-locus sidecar classes are now materialized and schema-passing. The
completion audit records 4/4 materialized classes, 4/4 passing schema audits,
702 rows per class, zero critical violations, and zero predictive/import-ready
rows. The next mechanism-feature step is a train/cal-only embedding pilot; no
labels, registries, imports, thresholds, splits, or production scorers changed.

Train/cal input-manifest follow-up: stage the no-fit input surface for that
future embedding pilot. The manifest enumerates only the 562 in-distribution
candidate rows and keeps all 140 heldout rows excluded from training and
threshold tuning. It finds 524 rows with the minimal active-site role-graph plus
organic cofactor plus inorganic cofactor-locus feature bundle, records 184
train/cal reaction-template rows, and does not fit weights, select thresholds,
or evaluate heldout rows.

Train/cal split-manifest follow-up: deterministically partition only the 524
minimal-bundle-ready rows into 418 train rows and 106 calibration rows across
six strata. The split manifest carries heldout only as an excluded count, records
38 blocked train/cal candidates by role-graph readiness class, and still does
not fit weights, select thresholds, or evaluate heldout rows.

Feature-contract follow-up: add a no-fit, label-stripped feature contract for
the 524 ready train/cal rows. It records four allowed feature groups
(active-site role graph, reaction-center template, organic cofactor scores, and
inorganic cofactor loci), strips `fingerprint_id`, `label_type`, stratum, and
split fields out of the feature-row surface, and keeps heldout absent from
feature rows. It is a materialization contract only; feature-vector code, model
weights, thresholds, directed electron/proton-transfer edges, and row-specific
bond-change mappings remain blocked until explicitly authorized.

Strict-audit follow-up: add a no-fit audit for that feature contract. It
validates 524/524 feature rows against the train/cal split manifest, confirms
forbidden label/outcome fields are absent from feature groups, keeps heldout
absent from feature rows, and reports zero critical violations. This does not
authorize feature-vector materialization or model fitting.

Train/cal guardrail follow-up: add a no-fit audit across the input manifest,
split manifest, and feature contract. It confirms that the 524 feature rows
exactly match the 524 train/cal split rows, split rows are a subset of the 562
input rows, 140 heldout rows remain excluded, and fingerprint/label/stratum
fields remain outside the feature surface. No model fit, threshold selection,
heldout evaluation, import, label change, or production scorer change occurred.

Row-specific bond-change priority follow-up: intersect the staged
row-specific bond-change schema with the current no-fit feature contract and
train/cal split manifest. The priority manifest partitions 232 evidence-required
rows into 171 P0 train/cal feature-contract gap rows, 13 P1 in-distribution rows
that need upstream feature-bundle repair before contract use, and 48 P2 heldout
final-only rows. It also stages a balanced 15-row P0 pilot seed queue across the
five current primary fingerprints. No source evidence was materialized and no
feature contract, label, split, threshold, model weight, import, registry,
ontology, or production scorer changed.

P0 source-graph readiness follow-up: audit that balanced 15-row P0 seed queue
against the frozen local M-CSA graph. All 15 rows have entry-node,
mechanism-text, catalytic-residue, and EC context; 11/15 have EC-to-Rhea
mappings; 0/15 have structured row-specific bond-change event predicates. This
does not materialize source evidence or authorize feature-contract consumption;
it converts the next work into manual/source-backed extraction of reaction
participant mappings and bond-change events.

P0 extraction-work-package follow-up: turn the readiness audit into a bounded
manual extraction package with 15 row templates, nine required source-backed
fields, event/mapping acceptance criteria, and per-row Rhea lookup flags. The
package is templates-only: every row remains `manual_extraction_not_started`,
and no source evidence, feature row, model input, threshold, label, registry,
ontology, import, or production scorer changed.

P0 extraction-package strict-audit follow-up: add a schema/guardrail audit for
that work package. It validates 15/15 template rows, 0 non-null extracted
values, 0 rows allowed for feature-contract or model use, and 0 critical
violations. The next safe step remains filling those templates from
source-backed evidence, then auditing the resulting sidecar before any no-fit
feature-contract refresh.

P0 extraction-worksheet follow-up: export the same 15 P0 template rows as a TSV
manual-fill worksheet. All source-evidence fields are blank by construction and
four rows are flagged for Rhea lookup. The worksheet is not a sidecar and must
not be consumed by a feature contract unless it is later filled from
source-backed evidence and passes a strict evidence audit.

P0 source-evidence sidecar-schema follow-up: stage the schema and audit plan
for the future filled sidecar. It requires 12 row fields, six event fields, and
four participant-mapping fields, names forbidden predictive fields, and defines
evidence/leakage checks. This remains schema-only with 0 materialized source
values.

P0 source-evidence draft-sidecar follow-up: fill the 15-row P0 worksheet into a
draft sidecar from frozen local M-CSA graph evidence. All rows now have M-CSA
source spans and draft bond-change events; 11/15 also have Rhea equations and
4/15 remain Rhea-missing. A strict audit confirms row alignment, required
fields, forbidden-field absence, and 0 critical violations. The sidecar remains
non-consumable: 0 rows are approved, no feature contract was refreshed, and no
model, threshold, label, registry, ontology, import, or production scorer
changed.

P0 source-evidence review-queue follow-up: add a manual-only queue over the
draft sidecar and strict audit. It ranks four Rhea-missing rows first
(`m_csa:124`, `m_csa:11`, `m_csa:169`, and `m_csa:5`), then four
high-complexity multi-event rows, then seven standard draft-review rows. This
does not approve or reject any row, refresh a feature contract, fit a model,
select a threshold, or mutate labels, registries, ontologies, imports, or
production scoring.

P0 Rhea lookup-manifest follow-up: stage exact manual lookup targets for those
four Rhea-missing rows from the frozen source-graph readiness evidence. The
manifest records `ec:1.9.3.1`, `ec:3.1.21.2`, `ec:3.4.14.5`, and
`ec:3.4.16.6` as the lookup targets, with rerun instructions for the strict
sidecar audit after any manual source update. No source fetch, source import,
approval, feature-contract refresh, model fit, threshold selection, label edit,
registry edit, ontology edit, or production-scorer change occurred.

P0 Rhea lookup-resolution follow-up: run a bounded official Rhea lookup for the
four staged rows. Exact EC queries returned zero Rhea records for all four
worksheet ECs; accession query `uniprot:P00396` resolved `m_csa:124` to
`RHEA:11436` with equation
`4 Fe(II)-[cytochrome c] + O2 + 8 H(+)(in) = 4 Fe(III)-[cytochrome c] + 2 H2O + 4 H(+)(out)`
and Rhea EC `7.1.1.9`. The source-evidence sidecar now records that official
Rhea equation as review-only evidence, increasing Rhea-covered rows from 11/15
to 12/15. The refreshed manual review queue leaves three Rhea-missing rows
(`m_csa:11`, `m_csa:169`, and `m_csa:5`) and moves `m_csa:124` into
high-complexity manual review. All rows remain draft/non-consumable: no
approval, feature-contract refresh, model fit, threshold selection, label edit,
registry edit, ontology edit, import, or production-scorer change occurred.

P0 Rhea resolution-consumption follow-up: add a strict audit tying the bounded
Rhea lookup resolution to the refreshed sidecar, review queue, remaining lookup
manifest, and feature-readiness audit. It confirms `m_csa:124` carries
`RHEA:11436` in the sidecar, is absent from the remaining lookup manifest, and
stays draft/non-consumable; `m_csa:11`, `m_csa:169`, and `m_csa:5` remain in
the lookup manifest and readiness blockers. The audit reports 0 critical
violations, 0 approved rows, 0 feature-contract-consumable rows, and 0
model-training-eligible rows.

P0 unresolved-Rhea official-source follow-up: recheck the three remaining rows
(`m_csa:11`, `m_csa:169`, and `m_csa:5`) against bounded Rhea EC queries with
and without the `ec:` prefix, Rhea accession queries, and current UniProtKB
catalytic-activity records. Rhea returns 0 records for all nine bounded queries.
UniProt confirms matching EC catalytic activity for all three accessions but
provides no Rhea cross-references. The rows remain non-consumable and cannot be
automation-resolved from official Rhea/UniProt alone; the next gate is reviewer
provenance for M-CSA-only approval, rejection/hold, or an explicitly authorized
alternate reaction source.

P0 reviewer-decision matrix follow-up: stage the review-only decision matrix
for those three unresolved rows. It records each row's draft event count,
readiness blockers, official-source status, and three allowed reviewer choices:
approve M-CSA-only source evidence with reviewer provenance, reject/rewrite
draft events, or hold for an alternate reaction source. It records no reviewer
decision, approval, feature-contract consumption, model-training eligibility,
label edit, registry edit, ontology edit, import, threshold change, or
production-scorer change.

P0 feature-readiness follow-up: audit the draft source-evidence sidecar against
the strict audit, manual review queue, Rhea lookup manifest, and current
feature contract. All 15 rows are structurally ready as drafts, with draft
coverage for 10 bond-change rows, 6 proton-transfer rows, and 9
electron-transfer rows. Zero rows are approved or consumable, and the current
feature contract contains no row-specific bond/proton/electron fields. The
next blocker remains the three unresolved Rhea rows plus reviewer-provenance approval
before any train/cal-only no-template feature refresh.

P0 refresh-blocker follow-up: add a compact automation decision audit over the
strict sidecar audit, feature-readiness audit, Rhea consumption audit,
unresolved official-source audit, reviewer decision matrix, and feature-contract
gap audit. It confirms automation must not refresh the no-template
mechanism-feature contract: all 15 draft rows are structurally ready, but 0 are
approved/consumable, 0 reviewer IDs are present, 0 copy-ready decisions exist,
and `m_csa:5`, `m_csa:11`, and `m_csa:169` still require reviewer provenance.
No feature contract, model, threshold, label, registry, ontology, import, or
production scorer changed.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_learned_mechanism_feature_embedding_plan_current702_20260601.json`,
`work/learned_mechanism_feature_embedding_plan_current702_20260601.md`,
`artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json`,
`work/mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.md`,
`artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_metal_ion_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_cobalamin_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_radical_sam_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.json`,
`work/mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`,
`work/mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`,
`work/mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_feature_contract_current702_20260601.json`,
`work/mechanism_feature_embedding_feature_contract_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_feature_contract_strict_audit_current702_20260601.json`,
`work/mechanism_feature_embedding_feature_contract_strict_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_train_cal_guardrail_audit_current702_20260601.json`,
`work/mechanism_feature_embedding_train_cal_guardrail_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.tsv`,
`work/mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit_current702_20260601.md`.

## 2026-06-01: Thiol/Disulfide Redox Boundary Panel Packet Added

Decision: build one additional review-only family-set expansion evidence packet
for the `thiol_disulfide_oxidoreductase_isomerase_boundary` panel. This uses
existing frozen current702 predicted geometry, predicted-atlas novelty variants,
selected organic cofactor scores, selected-PDB fold proxy evidence, and the real
predicted-structure fold channel. No label, registry, ontology, import,
promotion, threshold, split, or production scorer changed.

Result: the packet covers `m_csa:191` and is ready for review. The row has ok
predicted geometry, selected cofactor scores, selected-PDB fold proxy evidence,
and a real predicted-structure nearest-atlas TM score of `0.3863` against
`m_csa:631` / `ser_his_acid_hydrolase`.

Consequence: this widens the review-only family expansion evidence set for a
cofactor-confounded redox boundary without promoting any row. The next review
step is source-checking row-level bond-change and redox-partner evidence before
any countable family discussion.

Artifacts:
`artifacts/v3_family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.json`,
`work/family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.md`.

## 2026-06-01: Family Panel Packets Use All-Heldout Predicted-Fold Hits

Decision: update the family-panel evidence packet builder to use
all-heldout predicted-structure Foldseek/TM hits whenever available, while still
preserving priority cofactor-confounded hits. Then build a review-only
`flavin_monooxygenase_and_flavin_oxygen_transfer` evidence packet. No label,
registry, ontology, import, promotion, threshold, split, or production scorer
changed.

Result: the FMO/flavin oxygen-transfer packet covers four review rows:
`m_csa:131`, `m_csa:132`, `m_csa:551`, and `m_csa:973`. Three rows have ok
predicted geometry; `m_csa:132` remains a geometry gap. The all-heldout fold
channel supplies predicted-fold TM hits for `m_csa:131` (`0.751`) and
`m_csa:551` (`0.7309`), which were not available through the priority-only hit
lookup.

Consequence: review-only family expansion packets can now consume the completed
all-heldout fold channel, making non-priority panels better populated without
changing benchmark labels or training data. FMO remains secondary/review-only.

Artifacts:
`artifacts/v3_family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.json`,
`work/family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.md`.

## 2026-06-01: Remaining Family-Expansion Panels Have Review Packets

Decision: complete the review-only evidence packet set for the remaining
family-expansion panels after the panel builder was updated to consume
all-heldout predicted-fold hits. No label, registry, ontology, import,
promotion, threshold, split, or production scorer changed.

Result: new packets now cover `cobalamin_and_radical_rearrangement_panel`,
`no_reliable_structure_metal_hydrolase_controls`, and
`near_orphan_glycoside_or_nucleoside_hydrolase_controls`. The cobalamin/radical
packet has one current row with ok predicted geometry (`m_csa:750`) and two
secondary-probe geometry gaps. The no-reliable-structure metal hydrolase packet
originally had only geometry gaps, as expected for the panel definition. The
near-orphan glycoside/nucleoside packet has one current row with ok predicted
geometry (`m_csa:10`) and three gaps.

Follow-up: after the source-free predicted-geometry retrieval became available,
refresh the affected family-panel evidence packets to consume approved
source-free geometry scores for `secondary_probe::radical_sam_enzyme`, `mh_066`,
and `mh_073`. The packet coverage audit now has 15/22 predicted-geometry-ok rows
and 21 predicted-fold hits; the cobalamin/radical, no-reliable-structure metal
hydrolase, and near-orphan packets each retain one or more explicit geometry gaps
that still need approved source-free locators. No labels, imports, thresholds,
splits, registries, or production scorers changed.

Consequence: all seven family-set expansion target panels now have review-only
evidence packets. Use them for source/materialization triage only; none authorize
countable imports, label promotions, or training use.

Artifacts:
`artifacts/v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json`,
`work/family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.md`,
`artifacts/v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json`,
`work/family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.md`,
`artifacts/v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json`,
`work/family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.md`.

## 2026-06-01: Real Predicted-Structure Foldseek Channel Is Scored For All Ok Heldout Rows

Decision: move beyond the selected-PDB fold proxy by staging the real
AlphaFoldDB-predicted fold channel for heldout rows against the predicted
in-distribution atlas. The run used exact AFDB v6 CIF requests derived from the
current702 predicted-geometry atlas artifact, staged coordinates transiently
under `/private/tmp`, and committed only the small Foldseek TSVs plus parsed
JSON/report. No label, registry, ontology, threshold, production scoring, import,
or split changed.

Result: Foldseek exact TM scoring completed for all 126 heldout rows with ok
predicted geometry against 167 unique predicted atlas CIFs, yielding 11,297
mapped heldout-vs-atlas pairs and 0 unmapped names. The nearest-atlas TM signal
separates in-scope heldout from OOS at AUC `0.814301` overall and `0.829787`
against the six cofactor-confounded OOS rows. At the diagnostic >=90% in-scope
retention point it abstains on `0.4177` of all OOS and `0.3333` of confounded
OOS; at >=85% retention it abstains on `0.5063` of all OOS and `0.5` of
confounded OOS. Priority nearest-atlas TM scores were: `m_csa:30` 0.4988,
`m_csa:31` 0.3809, `m_csa:80` 0.5109, `m_csa:191` 0.3863, `m_csa:267` 0.7389,
and `m_csa:448` 0.5106.

Consequence: the real predicted-structure fold channel is now an all-heldout
rank signal, not only a manifest. It clears the 0.75 rank bar and is partly
aligned with the desired confounded-OOS behavior, but the high-retention operating
point is still not standalone deployment. Next work should combine this fold
channel with geometry/cofactor signals and decide whether persistent predicted-CIF
coordinate provenance should be committed.

Artifacts: `artifacts/v3_predicted_structure_fold_channel_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/cofactor_confounded_oos_vs_atlas.tsv`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/all_heldout_vs_atlas.tsv`,
`work/predicted_structure_fold_channel_current702_20260601.md`.

## 2026-06-01: Fold-Augmented Predicted-Geometry Gate Is The Strongest No-Fit Abstention Diagnostic So Far

Decision: combine the real predicted-structure nearest-atlas Foldseek/TM score
with frozen predicted-geometry confidence in a bounded heldout-only diagnostic.
This is explicitly no-fit and post-hoc: it selects no production threshold, does
not train on heldout, and changes no label, registry, ontology, import, split, or
production scorer.

Result: among raw and simple combined channels, `combined_mean_geometry_fold` is
best. It separates in-scope heldout rows from all OOS rows at AUC `0.907622` and
from the six cofactor-confounded OOS rows at AUC `0.911348`, above standalone
predicted geometry (`0.756935`/`0.840426`) and standalone nearest-atlas fold TM
(`0.814301`/`0.829787`). At the diagnostic >=90% in-scope retention point it
retains `0.9149` of in-scope rows while abstaining on `0.7215` of all OOS rows
and `0.8333` of cofactor-confounded OOS rows; at >=85% retention it abstains on
`0.7722` of all OOS rows and `0.8333` of cofactor-confounded OOS rows.

Consequence: the next deployment-gate work should promote this from a
heldout-only diagnostic into a leakage-safe train/cal/heldout thresholding
contract, with any fitted weights or threshold selected on train/cal only. Do
not treat these post-hoc operating points as authorized production thresholds.

Follow-up: add a companion novelty-variant artifact that recomputes the same
geometry-plus-predicted-fold combinations from existing scored artifacts, without
rerunning Foldseek/TM or fetching coordinates. It confirms the best existing
channel is the mean of predicted-geometry top1 score and nearest-atlas predicted
fold TM (`mean_top1_raw_and_tm`, equivalent to the earlier
`combined_mean_geometry_fold`) with AUC `0.907622` overall and `0.911348` on the
six confounded OOS rows.

Operating-grid follow-up: enumerate 0.95/0.90/0.85/0.80 retention diagnostics for
all 11 frozen geometry-plus-predicted-fold variant signals using the existing
variant rows only. The best variant artifact signal (`mean_top1_raw_and_tm`)
abstains on `0.7215` of OOS rows and `0.8333` of cofactor-confounded OOS rows at
>=90% in-scope retention. The best signal at the 0.90 target is
`mean_top1_atlas_percentile_and_tm`, with `0.7722` OOS abstain recall. This
remains post-hoc heldout evidence and does not authorize a deployment threshold.

Artifacts: `artifacts/v3_fold_augmented_abstention_gate_current702_20260601.json`,
`work/fold_augmented_abstention_gate_current702_20260601.md`,
`artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json`,
`work/predicted_structure_fold_augmented_novelty_variants_current702_20260601.md`,
`artifacts/v3_predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.json`,
`work/predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.md`.

## 2026-06-01: Predicted-Atlas Geometry Robust-Distance Variant Adds Modest Rank Lift, But Not An Operating-Point Breakthrough

Decision: after the in-distribution predicted-geometry atlas was materialized,
rerun the blocked atlas-normalized novelty variants rather than combining only raw
heldout scores. The bounded rerun used predicted-geometry retrieval rows only:
168 in-distribution atlas rows, 47 in-scope heldout rows, 79 OOS heldout rows,
and the six cofactor-confounded OOS rows already identified by the current gate.
All normalization was atlas-only; no labels, thresholds, registries, imports, or
splits changed.

Result: the best variant is a robust feature-distance signal to the nearest
in-distribution mechanism class centroid over top1 geometry subfeatures. It
improves novelty rank AUC over raw predicted-geometry top1 score:
`0.776461` vs `0.756935` overall, and `0.847518` vs `0.840426` on the
cofactor-confounded subset. The lift is real but bounded: at the diagnostic
>=90% in-scope retention point it abstains on only `0.2278` of OOS rows and
`0.3333` of confounded rows. Relaxing to >=85% retention reaches `0.5949` OOS
abstain recall and `0.6667` confounded abstain recall, still post-hoc and not a
deployment threshold.

Consequence: predicted-atlas robust-distance geometry is the best in-repo
geometry-only novelty variant so far, but it does not erase the operating-point
feature-overlap problem. Future work should treat it as a diagnostic/possible
feature input, not as a standalone deployable gate. The next distinct lever is
the real predicted-structure Foldseek/TM channel or a mechanism-feature embedding
gap closure, not another raw geometry subfeature recombination.

A follow-up operating-grid readout now enumerates 0.95/0.90/0.85/0.80
retention diagnostics for all 10 frozen predicted-atlas geometry novelty
signals without recomputing retrieval or Foldseek/TM. The best geometry-only
signal remains `negative_nearest_class_centroid_robust_distance`; at >=90%
in-scope retention it abstains on only 22.78% of OOS rows and 2/6
cofactor-confounded OOS rows. At >=85% retention it abstains on 59.49% of OOS
and 4/6 confounded OOS rows, reinforcing that this is evidence for a later
fold/mechanism-feature channel rather than a standalone threshold.

Artifacts: `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json`,
`work/predicted_atlas_geometry_novelty_variants_current702_20260601.md`,
`artifacts/v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json`,
`work/predicted_atlas_geometry_novelty_operating_grid_current702_20260601.md`.

## 2026-05-31: Ruled Out In-Repo Lever — Richer Geometry Sub-Features Do NOT Beat Collapsed top1_score For Novelty

Decision: before reaching for a new external feature, test whether the
novelty signal is already in the repo but hidden -- the predicted-geometry
retrieval collapses a rich per-row fingerprint match (mechanistic_coherence_score,
role_match_fraction, substrate_pocket_score, compactness_score,
cofactor_context_score, counterevidence_penalty, distance stats) into one
top1_score. Measured each sub-field's individual novelty AUC (in-scope > OOS) on
the deployment held-out pool (47 in-scope, 79 OOS).

Result: top1_score (AUC 0.757) is already the best single geometry novelty signal.
No sub-field beats it -- next best are cofactor_context_score 0.688 and
role_match_fraction 0.655; mechanistic_coherence, residue_match, substrate_pocket,
compactness, counterevidence_penalty, plp_anchor are all 0.50-0.55 (near chance). A
naive mean of the positive sub-fields (0.724) DILUTES the score rather than
improving it. The atlas-standardized (Mahalanobis) variant is blocked by the
known no-predicted-geometry-atlas issue.

Consequence: the in-repo geometry decomposition has no headroom over the score
that already integrates it. This rules out "unpack the features we have" and
confirms the northstar redirect from the entry below: the next lever must be a
GENUINELY NEW mechanism-discriminative feature (learned active-site/electron-flow
embeddings, fold-level novelty, or a predicted-geometry retrieval that also scores
the in_distribution atlas), not a recombination of existing channels. Probe-only
(negative result); no module/artifact added. Atlas-free, deployment regime,
M-CSA eval-only.

## 2026-05-31: Operational Gate Architecture Settled — Binding Constraint Is Feature Overlap, Not Combiner Design (Northstar Pivot)

Decision: act on the operating-point gap. Built the per-channel RULE gate that the
prior entry pointed to: `abstain if geometry_score < tg OR (cofactor_max <
signature_threshold AND cofactor_max < tc)` -- geometry leads (safe on the
cofactor-confounded subset), and the cofactor channel may only ADD abstentions
where it is trustworthy (no strong known-cofactor signature), never KEEP a row
geometry flags. Swept a fixed untuned 2D threshold grid (0.02 steps); no tuning on
eval labels.

Result (predicted/apo deployment geometry; 47 in-scope, 79 OOS, 6 confounded, 73
agnostic):
  * At 90% in-scope retention there is STILL no viable operating point -- for any
    combiner. The geometry score distributions overlap hard: in-scope median 0.434
    (min 0.291), agnostic-OOS median 0.370 (max 0.676), confounded-OOS median 0.358.
    Known and novel chemistry are not linearly separable on this feature.
  * Relaxing to 85% retention, the per-channel rule gives a REAL lift: OOS
    abstain-recall 0.139 (geometry only) -> 0.304 (rule), +0.165, entirely on the
    cofactor-agnostic subset (0.315). The confounded subset stays hard (~0.17)
    until retention drops to ~80%.

Northstar consequence: the per-channel rule is the correct OPERATIONAL ARCHITECTURE
(geometry-led, cofactor-as-agnostic-lift, confounded-safe) and is now committed.
But the binding constraint on de novo abstention is no longer combiner design or
thresholding -- it is FEATURE OVERLAP. The current channels (predicted-geometry
fingerprint-retrieval confidence + organic-cofactor head probability) do not place
novel chemistry far enough from known chemistry to abstain at deployable retention.
This redirects the northstar: the next lever is a stronger mechanism-discriminative
FEATURE (e.g. learned active-site/electron-flow embeddings, predicted-geometry role
decomposition for atlas rows, or fold-level novelty signals), evaluated at the
operating point -- not another way to combine the features we already have.

Guardrails: predicted-geometry deployment regime, sequence-only PLM input, no atlas,
no training/refit, fixed untuned threshold grid; geometry fingerprint score is
tuning-adjacent; M-CSA eval-only. `compute_deployment_gate` now emits
`per_channel_rule_gate`. Refines the operating-point entry below; both stand.

## 2026-05-31: Sobering Operating-Point Reality — De Novo AUC 0.852 Does NOT Yield A Usable Abstention Threshold

Decision: the pivotal entry showed the deployment abstention AUC clears 0.75, but
AUC is rank-only. Convert the gate to an actual decision (a threshold) and report
its behavior, so the headline AUC is not mistaken for deployability. Thresholds are
a fixed, untuned grid over the calibrated [0,1] scores — not fit to eval labels.

Result (predicted/apo geometry; 47 in-scope, 79 OOS, 6 confounded; threshold chosen
to retain >=90% of in-scope rows):
  * geometry-led gate (thr 0.35): abstains on only **19% of OOS** at 91% in-scope
    retention. The score distributions overlap heavily; there is a cliff near 0.40
    where OOS-recall jumps to 0.84 but in-scope retention collapses to 0.64. No
    threshold gives both high novelty-catch and high retention.
  * blind mean-combined gate (thr 0.25): catches 59% of OOS but abstains on **NONE
    of the 6 safety-critical cofactor-confounded rows** (confounded_abstain_recall
    0.0) — the exact failure the AUC hid. The mean's aggregate edge comes entirely
    from the cofactor-agnostic majority.

Consequence: the de novo precondition is achievable in ranking (AUC 0.852) but NOT
yet operational — there is no fixed threshold that abstains usefully while retaining
known chemistry, and the blind mean is actively unsafe on the confounded subset. The
gate now commits a full operating curve and the >=90%-retention operating points so
this gap is explicit, not hidden behind the AUC. Future work: per-channel
thresholds (geometry-led with a cofactor-agnostic-only cofactor lift), or a
calibrated score, evaluated at the operating point, not by AUC.

Guardrails: predicted-geometry deployment regime, sequence-only PLM input, no atlas,
no training/refit, no heldout tuning (threshold grid is fixed/untuned); geometry
fingerprint score is tuning-adjacent; M-CSA eval-only. Refines (does not overturn)
the pivotal AUC entry below. Artifacts regenerated in place:
`artifacts/v3_mechanism_deployment_abstention_gate_eval_current702_20260531.json`,
`work/mechanism_deployment_abstention_gate_eval_current702_20260531.md`
(`compute_deployment_gate` now emits `operating_points_at_90pct_retention` and
`geometry_led_operating_curve`).

## 2026-05-31: PIVOTAL — De Novo Abstention Precondition IS MET On Deployment (Predicted) Geometry

Decision: the prior "deployment-valid gate is blocked — no predicted-geometry
atlas rows" entry below was solving the wrong problem. The two-channel gate does
not need a predicted-geometry atlas at all. Both channels are already calibrated
[0,1] confidences:
  * predicted-geometry fingerprint-retrieval `top1_score` (from
    `predicted_geometry_retrieval.results` in the robustness audit), and
  * the strongest organic-cofactor head probability (`cofactor max_score`).
They can be combined directly over the held-out pool with NO atlas normalization
and NO eval-pool leakage. This makes the deployment-valid de novo gate computable
from artifacts already in the repo.

Result (predicted/apo deployment geometry; 47 in-scope, 79 OOS, 6 confounded, 73
agnostic; held-out only, no atlas, no tuning):
  * combined_mean: AUC **0.852 overall — CLEARS the 0.75 de novo precondition bar**.
  * geometry_top1_score: 0.757 overall and the single SAFEST channel — no stratum
    below chance, and strongest exactly on the dangerous cofactor-confounded OOS
    (0.840), where the cofactor channel is fooled (0.280, worse than chance).
  * cofactor_max_score: 0.628 overall (good 0.657 on agnostic, fooled on confounded).
  * combined_min: 0.609 (the strict-concordance combiner is the worst here).

This is the decisive de novo result: on the real deployment regime, mechanism
novelty IS detectable with leakage-free, already-available signals. The recommended
deployment gate LEADS WITH GEOMETRY CONFIDENCE (uniformly safe, best on the
confounded cases) and adds the cofactor channel as a complementary lift on the
cofactor-agnostic OOS majority — NOT a blind mean, which scores higher in aggregate
(0.852) only by sacrificing safety on the confounded subset (0.330). Pick the
combiner by the safety profile, not the aggregate AUC.

Caveat: the geometry fingerprint score is hand-authored / tuning-adjacent (D4); the
result is a relationship/abstention AUC, not a calibrated probability, and is bounded
to the current 8-fingerprint family set. Guardrails: sequence-only PLM input,
predicted-geometry deployment regime, no atlas, no training/refit, no heldout tuning,
M-CSA eval-only.

Artifacts: `artifacts/v3_mechanism_deployment_abstention_gate_eval_current702_20260531.json`,
`work/mechanism_deployment_abstention_gate_eval_current702_20260531.md`. Module:
`src/catalytic_earth/mechanism_abstention_gate_eval.py`
(`compute_deployment_gate`, tests in `tests/test_mechanism_abstention_gate_eval.py`;
CLI: `eval-mechanism-deployment-abstention-gate`). Supersedes the "blocked" entry below.

## 2026-05-31: Deployment-Valid Two-Channel Gate Is Blocked — No Predicted-Geometry Atlas Rows

Decision: attempted the deployment-valid rerun of the two-channel abstention gate
flagged as the next step by the teacher-side entry below, pointing
`--geometry-retrieval` at the `predicted_geometry_retrieval` block of
`v3_predicted_geometry_robustness_audit_current702_20260529.json`.

Finding (verified, no scoring claim): that block contains ONLY held-out rows — 47
in-scope (heldout, has fingerprint) + 79 OOS (heldout, no fingerprint), and ZERO
in_distribution rows. The gate needs in-distribution atlas rows to (a) build the
cofactor-augmented PLM class centroids and (b) compute the geometry channel's
atlas-percentile normalization. With atlas=0 the gate returns
`status=insufficient_rows` and no AUC. The broken run artifact was deleted, not
committed; no numbers were produced.

Consequence: the deployment-valid two-channel gate is blocked on a
predicted-geometry retrieval that also covers the ~124 in_distribution atlas rows
(the current audit only re-scored the held-out evaluation set on predicted
structure). Concrete next gate: regenerate geometry retrieval on predicted
(AlphaFold) structures for the in_distribution atlas rows too, persisting per-row
`role_match_fraction`, then rerun `eval-mechanism-abstention-gate
--geometry-retrieval <that artifact>`. The separate predicted-geometry-confidence
finding (raw `top1_score` AUC 0.757) stands because it is a single-channel
rank-based AUC over the held-out pool only and needs no atlas.

## 2026-05-31: Two-Channel Abstention Gate (cofactor + geometry role) — Source-Agnostic, Clears Bar On Teacher Geometry

Decision: productionize the two-channel abstention gate implied by the confounded-
OOS diagnosis. Channel 1 is the cofactor-augmented PLM nearest-centroid; channel 2
is geometry `top1_score x role_match_fraction` (novel chemistry shows the right
active-site residues with the wrong catalytic roles). Each channel is mapped to its
in-distribution ATLAS percentile (atlas-only, deployable, no eval-pool leakage) and
combined by mean.

Result on experimental/teacher geometry (47 in-scope, 88 OOS, 8 confounded): the
combined-mean gate reaches overall AUC 0.830 and clears the 0.75 de novo bar, with
geometry rescuing the cofactor-confounded set (cofactor 0.339 -> combined 0.503;
geometry alone 0.652 there). Per channel: cofactor 0.684, geometry 0.801,
combined-mean 0.830, combined-min 0.733.

Relation to the predicted-geometry finding below: that entry correctly establishes
the deployment-valid signal lives in predicted (apo) geometry, not this
experimental retrieval, and that predicted top1 score alone hits AUC 0.757. This
gate module is SOURCE-AGNOSTIC on `--geometry-retrieval`, so once a predicted-
geometry retrieval persisting per-row `role_match_fraction` exists, the
deployment-valid two-channel number is a one-line rerun. Until then this is a
teacher-side proof the precondition is achievable with the right two channels, not
a deployment claim — the report carries that caveat explicitly.

Guardrails: sequence-only PLM input, atlas-only statistics/percentiles, no
training/refit/heldout tuning; geometry fingerprint score is tuning-adjacent
(role_match_fraction is structural); M-CSA eval-only. Module:
`src/catalytic_earth/mechanism_abstention_gate_eval.py` (tests:
`tests/test_mechanism_abstention_gate_eval.py`; CLI: `eval-mechanism-abstention-gate`;
artifacts: `artifacts/v3_mechanism_abstention_gate_eval_current702_20260531.json`,
`work/mechanism_abstention_gate_eval_current702_20260531.md`).

## 2026-05-31: Predicted-Geometry Confidence Is The Strongest Abstention Signal

Decision: test whether geometry-channel confidence flags the cofactor-confounded
OOS rows where the cofactor channel is confidently wrong — on deployment-valid
PREDICTED (AlphaFold) geometry, not experimental teacher geometry.

First rejected a trap: `v3_geometry_retrieval_1025.json` is experimental/teacher-
side (retains ligand/cofactor context, scores a non-deployment-valid AUC 1.0). The
honest signal is `top1_score` from `hand_router_on_predicted_geometry.rows` in
`v3_predicted_geometry_robustness_audit_current702_20260529.json` (predicted, apo).

Result (heldout split, predicted regime): predicted-geometry top1 score separates
in-scope from OOS at AUC 0.757 (in vs all-OOS, 47 vs 79) — the first single signal
to reach the 0.75 usability bar, beating cofactor-augmented 0.694 and bare-PLM
0.596. It is strongest exactly where the cofactor channel fails: AUC 0.840 on the
cofactor-confounded OOS (n=6 with usable predicted geometry; m_csa:549 fetch-failed,
m_csa:563 excluded) vs the cofactor channel's worse-than-chance 0.443 there. The
channels are complementary.

Consequence: the de novo abstention gate should be geometry-confidence-led with
the cofactor channel complementary. Next: a combined weakest-channel gate
(predicted-geometry confidence AND cofactor agreement) and fold the
predicted-geometry signal into the novelty eval as first-class. Existing per-row
scores only; nothing fit on heldout; no labels/registries/thresholds changed;
M-CSA eval-only. Artifact: `work/predicted_geometry_abstention_finding_current702_20260531.md`;
reproduce with `scripts/predicted_geometry_abstention_probe.py`.

## 2026-05-31: Abstention Leak Is 8 Named Cofactor-Confounded OOS Rows, Not A Uniform Ceiling

Decision: diagnose *why* novel-chemistry abstention plateaus at AUC ~0.69 instead
of treating it as a generic ceiling. Tested two things and stratified the result.

(1) A supervised, atlas-only mechanism-feature readout does NOT beat the
unsupervised cofactor-augmented signal: per-class diagonal-Gaussian log-likelihood
in the between-class subspace gives AUC 0.521 (chance) and a one-vs-rest
mean-difference margin gives 0.637 — both below the cofactor-augmented 0.694. So
the ceiling is not a method-sophistication problem solvable by learning directions
on the current 8-class atlas (probe-only, not committed).

(2) Stratifying the 92 OOS rows by whether they carry a known cofactor signature
(max organic-cofactor score >= 0.5, untuned) splits the aggregate sharply:
   - 84 cofactor-agnostic OOS rows abstain well: AUC 0.718 (near the 0.75 bar).
   - 8 cofactor-signature OOS rows are confidently misplaced: AUC 0.443 (worse
     than chance) — the channel pulls them into occupied clusters.
The residual abstention leak is therefore concentrated in 8 named false-confident
novelty cases (m_csa:30, 31, 80, 191, 267, 448, 549, 563), not spread uniformly.
These are novel-mechanism enzymes that happen to use a known cofactor family, the
single most dangerous failure mode for an abstention gate, and now enumerated.

Consequence: an abstention gate built on the cofactor-augmented signal is viable
for the cofactor-agnostic majority; the named cofactor-confounded OOS rows are the
explicit target for the next mechanism-feature signal (fold/active-site geometry
beyond cofactor identity). This stratified diagnostic is now part of the committed
novelty eval (`stratified_by_cofactor_signature`).

## 2026-05-31: Novelty-Abstention Rerun On Strict t6/t12 Scores (Fallback Removed)

Update to the de novo precondition result below: after the ESM2-150M fallback
cofactor sidecar was replaced with the strict original t6/t12 selected scores
(`trained:esm2_t6_8m` + `trained:esm2_t12_35m`), the source-agnostic
novelty-abstention eval was re-run with no code change. The real cofactor heads
improve separation over the fallback — cofactor-augmented best AUC rises from
0.654 to **0.694**, and the raw cofactor-confidence signal reaches AUC 0.636 with
novel chemistry carrying markedly lower in-class cofactor confidence (in-scope
0.380 vs OOS 0.165). Bare-PLM distance is unchanged at 0.596. The signal is still
below the 0.75 usability bar, so the conclusion stands: distance/cofactor
abstention is not yet sufficient for de novo, but the stronger channel
measurably helps. Artifact and report regenerated in place.

## 2026-05-31: D11 De Novo Precondition — Distance Cannot Abstain On Novelty; Cofactor Helps But Falls Short

Decision: measure the D11 de novo validity check directly — can a cheap,
unsupervised signal separate in-scope held-out queries (known mechanism
fingerprint) from out-of-scope held-out rows (novel chemistry, no fingerprint)?
Abstention-on-novelty is the de novo precondition, so this is a gate, not a
nicety.

Result (48 in-scope, 92 OOS, 184 atlas; all atlas-only statistics, no tuning):
bare ESM2-150M distance signals are near chance — nearest-atlas cosine AUC 0.547,
nearest-centroid 0.596, top1/top2 margin 0.567, between-class subspace projnorm
0.524 (best 0.596). A general-purpose PLM encodes overall protein similarity, so
novel enzymes still look like ordinary proteins and sit inside occupied regions.
Adding the row-level organic-cofactor channel (the now-unblocked, source-agnostic
sidecar) moves the signal in the right direction — augmented nearest-centroid AUC
0.654, with OOS carrying lower in-class cofactor confidence (in 0.716 vs OOS
0.601) — but still below the 0.75 usability bar.

Consequence: distance-thresholded abstention is insufficient for de novo today.
The cofactor channel is a genuine but partial mechanism-discriminative signal;
the precondition needs a stronger one (recovered t6/t12 cofactor heads instead of
the ESM2-150M fallback, and/or explicit mechanism-feature supervision). The
novelty eval is source-agnostic, so re-running it once the fallback is removed is
a one-line change.

Guardrails held: sequence-only PLM input, no training/refit, no held-out tuning,
atlas-only statistics/centroids/subspace, M-CSA eval-only.

Artifacts: `artifacts/v3_mechanism_novelty_abstention_eval_current702_20260530.json`,
`work/mechanism_novelty_abstention_eval_current702_20260530.md`. Module:
`src/catalytic_earth/mechanism_novelty_abstention_eval.py`
(tests: `tests/test_mechanism_novelty_abstention_eval.py`; CLI:
`eval-mechanism-novelty-abstention`).

## 2026-05-30: D11 Hygiene Surface — Real PLM Beats k-mer Control

Decision: add a real protein-language-model sequence surface (persisted
ESM2-150M whole-sequence embeddings) to the D11 relationship faithfulness
measurement, evaluated under one identical, committed, rank-based pipeline
against the deterministic k-mer control.

Result: on the held-out query / in-distribution atlas split (48 queries, 184
candidates), the ESM2-150M surface beats the k-mer control on all 24 reported
metrics with zero losses — exact-top1 rises from ~0.31 to ~0.52 (cosine),
family-top3-any from 0.67 to 0.90, family-MRR from 0.60 to 0.80. The k-mer
control reproduces the prior D11 hygiene eval's ballpark (family-top3-any cosine
0.667 vs 0.652), which cross-validates the new pipeline.

Scope and guardrails: this is a hygiene-tier sequence-surface comparison, not the
real D11 pass. The real pass remains `blocked_missing_row_level_cofactor_channel_scores`
because row-level selected organic-cofactor scores (flavin/heme/PLP) and a
cofactor-augmented predicted-geometry query representation are still missing.
Inputs are amino-acid-sequence-only; no geometry-derived cofactor evidence, no
training/refit, no held-out tuning (robust scaling uses atlas-only statistics).
M-CSA remains eval-only.

Artifacts: `artifacts/v3_mechanism_relationship_plm_surface_current702_20260530.json`,
`work/mechanism_relationship_plm_surface_current702_20260530.md`. Module:
`src/catalytic_earth/mechanism_relationship_surface_eval.py`; reproduce via its
`write_mechanism_relationship_surface_eval(...)` entrypoint, exercised by
`tests/test_mechanism_relationship_surface_eval.py::test_build_from_real_artifacts_if_present`.
A convenience CLI subcommand `eval-mechanism-relationship-surface` is also wired
into `src/catalytic_earth/cli.py`.

## 2026-05-30: Session D1-D11 Decision Record

Decision: preserve the D1-D11 session reasoning as a durable project-memory
record before running D11 relationship-eval automation.

Rationale: the session established the current line of reasoning from Wave 1
decoder/join confounds, through predicted-geometry information loss, sequence
cofactor-channel reconstruction, concordance gating, and the D11 mechanism
relationship-space framing. Future agents should read this record before
interpreting route-policy, LOMO, targeted expansion, or D11 relationship-eval
outputs.

Reference:

- `docs/session_decision_record_20260530.md`

## 2026-05-25: Current702 Benchmark Contract

Decision: freeze the current702 sequence benchmark and mechanism-prediction
contract before interpreting sequence-NN, PLM, or hybrid results.

Rationale: current702 has complete sequence coverage and repaired split
assignments, but representation claims need a fixed target universe, OOS policy,
diversity bins, and active-site evidence-budget rules.

References:

- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- `artifacts/v3_sequence_nn_metrics_current702_20260525.json`

## 2026-05-27: `m_csa:497` Is Out Of Scope

Decision: relabel `m_csa:497` from
`flavin_dehydrogenase_reductase` to `out_of_scope` for v1 benchmark use.

Rationale: the row is flavodiiron nitric oxide reduction. Catalysis occurs at a
non-heme Fe(II)Fe(II) center, with FMNH2 acting as an electron donor to the
di-iron nitrosyl complex rather than as the v1 flavin hydride-transfer catalytic
locus. It should be retained as a hard OOS/boundary negative for flavin-cofactor
leakage, not as primary flavin support.

References:

- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json`
- `artifacts/v3_packet1_wave1_decision_closure_702_20260527.json`
- `data/registries/curated_mechanism_labels.json`

## 2026-05-27: `m_csa:750` Is Not A Primary Flavin Canary

Decision: remove `m_csa:750` from primary flavin metrics and from Wave 1
Foldseek-success/learned-failure canary use. The current registry label is
`out_of_scope`.

Rationale: 4-hydroxybutanoyl-CoA dehydratase uses radical FAD semiquinone plus
Fe-S dehydration chemistry. That is a future radical-flavin/Fe-S dehydratase
family candidate, not ordinary v1 flavin hydride-transfer
dehydrogenase/reductase chemistry. Older wins against the previous flavin label
are stale.

References:

- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_wave1_metric_canary_impact_702_20260527.json`
- `artifacts/v3_packet1_wave1_decision_closure_702_20260527.json`
- `data/registries/curated_mechanism_labels.json`

## 2026-05-27/28: FMO Stays Secondary-Only

Decision: keep flavin monooxygenase as secondary OOD/acquisition context only.
Do not promote it to a primary supervised metric, do not add a canonical child
registry entry, and do not import FMO candidates.

Rationale: the source evidence supports real FMO-like chemistry for rows such
as `m_csa:131`, `m_csa:132`, and review-ready future rows `m_csa:551` and
`m_csa:973`, but the current support is underpowered and gate-limited. The
active geometry/counterevidence gate is PHBH-leaning, exact ligand-bearing
coordinates are missing or unsuitable for important external subtype rows, and
subtype panels plus hard-negative controls are still needed.

References:

- `artifacts/v3_fmo_source_evidence_scout_702_20260527.json`
- `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json`
- `artifacts/v3_fmo_admission_gate_and_benchmark_impact_702_20260527.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
- `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`
- `artifacts/v3_fmo_external_hard_negative_duplicate_gate_702_20260528.json`

## 2026-05-28/29: Wave 1 Decoder And Geometry-Join Confounds

Decision: use the Wave 1.2 decoder/join confound audit as the current
representation comparison gate.

Rationale: the older geometry preview joined only 135/140 heldout rows, while
the current re-export joins 140/140. Decoder choice is also a real confound:
the same ESM-C representation behaves very differently under a logistic head
versus cosine NN. ProtT5 and SaProt matched logistic reruns are blocked by
missing local raw sidecars/weights, not by a negative result.

References:

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `artifacts/v3_wave1_1_model_by_cell_report_702_20260528.json`
- `artifacts/v3_wave1_representation_shootout_result_card_20260526.json`

## 2026-05-29: Geometry-First Router Interpretation

Decision: prefer a geometry-first router for the next gate. Do not scale
learned models first and do not treat Wave 1 learned-representation diagnostics
as proof of mechanism prediction superiority.

Rationale: current hand-scored geometry resolves the audited join gap, reaches
45/45 canonical primary heldout accuracy, and has 0/92 pure-OOS false positives
under the frozen 0.4115 threshold. The local geometry-feature logistic probe and
PLM heads are useful diagnostics, but they do not displace the hand geometry
router.

References:

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `work/northstar_wave1_to_engine_handoff_20260526.md`

## 2026-05-29: Predicted Geometry Is Not Deployment-Ready

Decision: do not interpret the clean experimental-coordinate 45/45 hand-router
result as bare-sequence deployment readiness.

Rationale: when current702 heldout M-CSA rows with experimental geometry and
sequence-position mappings are re-scored on AlphaFoldDB predicted coordinates,
the hand router drops to 23/45 canonical primary correct, with 17 primary
abstentions, 5 wrong non-abstained primary calls, and a 12.3% OOS/secondary
false-positive rate. The OOS-aware geometry MLP trained on experimental
geometry stays disciplined on OOS but reaches only 16/45 primary correct via
abstention. The learned-model job is now explicitly robustness to predicted
active-site geometry degradation, not beating clean M-CSA geometry in isolation.

References:

- `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json`
- `work/predicted_geometry_robustness_audit_current702_20260529.md`
- `artifacts/v3_predicted_geometry_robustness_audit_current702_esmfold_20260529.json`

## 2026-05-29: Review And Import Posture

Decision: review artifacts are not imports. Countable label changes require a
dedicated review decision, import preview, label-factory gates, batch
acceptance, and registry summary refresh. This cleanup pass does not edit
labels, registries, ontologies, imports, production scoring, or global
thresholds.

Rationale: the repo intentionally separates review evidence from benchmark
labels to avoid leakage, stale claims, and accidental count growth. External
seed-fingerprint imports remain 0, and the three imported external rows are
out-of-scope hard negatives only.

References:

- `docs/label_factory.md`
- `artifacts/v3_mcsa_ai_visual_review_support_index_20260524.json`
- `artifacts/v3_mcsa_ai_visual_remaining_manual_expert_holds_index_20260525.json`
- `artifacts/v3_mcsa_positive_clean9_import_preview_20260523.json`
- `artifacts/v3_mcsa_ai_visual_clean10_accept7_vivek_20260524_import_summary.json`
- `artifacts/v3_artifact_migration_execution_1025.json`

## 2026-05-29: README Becomes The Front Door

Decision: keep `README.md` concise and move active project memory into
dedicated docs.

Rationale: the previous README mixed front-door onboarding with a long
chronological research dump. Future agents need a stable source-of-truth order:
project state, decisions, artifact index, then runbook.

References:

- `docs/project_state.md`
- `docs/decision_log.md`
- `docs/artifact_index.md`
- `docs/agent_runbook.md`
- `README.md`
